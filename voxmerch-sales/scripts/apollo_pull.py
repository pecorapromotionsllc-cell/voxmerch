#!/usr/bin/env python3
"""
Fetch the Apollo contact set to disk, without passing it through a model's context.

Why this exists
---------------
stage_sync.py was built on the principle that the raw data never has to cross a model's
context to be processed: the caller fetches, saves to disk, and passes file paths. The
fetch itself was the last piece still going through the model, and it was expensive in
three separate ways.

On 2026-09-01 the scheduled reconcile fired at 7:16 AM CDT, pulled page 1 of 19 through
the Apollo MCP tool, hit an approval prompt on page 2, and sat blocked for eight and a
half hours until Mary Anne came back to her desk. Nothing reconciled. That failure had
three causes and this script removes all three:

1. Nineteen separate approval-gated tool calls are nineteen separate chances to stall.
   This is one command.
2. Each MCP page result runs about 580,000 characters, far past the tool-result limit, so
   the harness writes it to a file and hands back an "output too large" notice. Nineteen
   of those cost roughly 8,000 tokens per run to learn nothing. This writes the files
   directly and prints a handful of lines.
3. A stalled run leaves half-fetched pages whose mtimes age past the 6-hour freshness
   guard in stage_sync.py, so the retry has to re-pull everything from page 1. A single
   command either completes or fails fast.

Authentication
--------------
The Apollo MCP server uses OAuth and does not expose a key to this script. The REST API
uses a master API key instead, which is generated in Apollo under Settings > Integrations
> API. Put it in the environment as APOLLO_API_KEY. This script refuses to run without
one rather than pulling a partial set.

Usage
-----
  python3 voxmerch-sales/scripts/apollo_pull.py --out-dir /tmp/apollo

  # narrowed to one Apollo list, which is what makes the pull cheap; pair it with
  # stage_sync.py --strict-coverage so a contact the filter drops fails loudly
  # instead of silently keeping a stale board stage
  python3 voxmerch-sales/scripts/apollo_pull.py --out-dir /tmp/apollo \
      --label-id 6a90ba545271f0000cfa59ff

Writes apollo_page_001.json, apollo_page_002.json, ... into --out-dir and prints the
paths, one per line, so the caller can hand them straight to stage_sync.py --apollo.

Exit codes: 0 on a complete pull, 2 on anything that would produce a partial one. A
partial pull is worse than no pull: every contact on a missing page looks absent from
Apollo, and stage_sync.py would leave their board stage stale without saying so.
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

APOLLO_SEARCH_URL = "https://api.apollo.io/api/v1/contacts/search"

# Apollo caps this endpoint at 100 per page and 500 pages. Asking for more per page is
# silently clamped, so ask for exactly the cap.
MAX_PER_PAGE = 100

# A pull that needs more pages than this means the filter is wrong, not that the account
# grew. 1,839 contacts across 19 pages was already most of the cost of the old run.
SANE_PAGE_CEILING = 60

RETRY_STATUSES = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 5


def build_ssl_context():
    """Honour the agent proxy's CA bundle without ever disabling verification."""
    context = ssl.create_default_context()
    # create_default_context already reads SSL_CERT_FILE. The proxy bundle is a documented
    # fallback for this environment when that variable is not set.
    if not os.environ.get("SSL_CERT_FILE"):
        fallback = "/root/.ccr/ca-bundle.crt"
        if os.path.exists(fallback):
            context.load_verify_locations(fallback)
    return context


def fetch_page(api_key, page, per_page, label_id, context):
    """One page of contacts/search, with backoff on the statuses worth retrying."""
    body = {"page": page, "per_page": per_page}
    if label_id:
        body["contact_label_ids"] = [label_id]

    request = urllib.request.Request(
        APOLLO_SEARCH_URL,
        data=json.dumps(body).encode(),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "X-Api-Key": api_key,
        },
    )

    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, context=context, timeout=120) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as error:
            # 401 and 403 will not improve with a retry, and burning four more attempts on
            # a bad key just delays a clear message.
            if error.code in (401, 403):
                detail = error.read().decode(errors="replace")[:400]
                print(
                    f"REFUSING TO RUN: Apollo rejected the API key (HTTP {error.code}).\n"
                    f"  {detail}\n"
                    "  Generate a key in Apollo under Settings > Integrations > API and set "
                    "APOLLO_API_KEY. The key must have the Contacts scope enabled.",
                    file=sys.stderr,
                )
                raise SystemExit(2)
            if error.code not in RETRY_STATUSES or attempt == MAX_ATTEMPTS:
                raise
            last_error = f"HTTP {error.code}"
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            if attempt == MAX_ATTEMPTS:
                raise
            last_error = str(error)

        backoff = 2 ** attempt
        print(f"  page {page}: {last_error}, retrying in {backoff}s", file=sys.stderr)
        time.sleep(backoff)

    raise SystemExit(2)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out-dir", required=True, help="directory to write the page files into")
    parser.add_argument(
        "--label-id",
        help="restrict to one Apollo list id. Cheaper, but pair it with "
        "stage_sync.py --strict-coverage so a dropped contact fails loudly.",
    )
    parser.add_argument("--per-page", type=int, default=MAX_PER_PAGE)
    args = parser.parse_args()

    api_key = os.environ.get("APOLLO_API_KEY")
    if not api_key:
        print(
            "REFUSING TO RUN: APOLLO_API_KEY is not set.\n"
            "  The Apollo MCP server authenticates by OAuth and does not expose a key to "
            "this script, so the REST API needs its own.\n"
            "  Generate one in Apollo under Settings > Integrations > API, then add it to "
            "the environment this routine runs in.\n"
            "  Until then the reconcile has to fall back to paging apollo_contacts_search "
            "through the MCP tool.",
            file=sys.stderr,
        )
        raise SystemExit(2)

    per_page = min(args.per_page, MAX_PER_PAGE)
    os.makedirs(args.out_dir, exist_ok=True)
    context = build_ssl_context()

    written = []
    page = 1
    total_pages = None
    total_entries = None

    while True:
        payload = fetch_page(api_key, page, per_page, args.label_id, context)
        pagination = payload.get("pagination") or {}

        if total_pages is None:
            total_pages = pagination.get("total_pages")
            total_entries = pagination.get("total_entries")
            if not total_pages:
                print(
                    "REFUSING TO RUN: Apollo returned no pagination.total_pages, so there is "
                    "no way to tell whether the pull is complete.",
                    file=sys.stderr,
                )
                raise SystemExit(2)
            if total_pages > SANE_PAGE_CEILING:
                print(
                    f"REFUSING TO RUN: Apollo reports {total_pages} pages "
                    f"({total_entries} contacts). That is past the {SANE_PAGE_CEILING}-page "
                    "ceiling, which means the pull is unfiltered or the account grew a "
                    "cohort. Narrow it with --label-id, or raise the ceiling deliberately.",
                    file=sys.stderr,
                )
                raise SystemExit(2)
            print(f"pulling {total_entries} contacts across {total_pages} page(s)")

        path = os.path.join(args.out_dir, f"apollo_page_{page:03d}.json")
        with open(path, "w") as handle:
            json.dump(payload, handle)
        written.append(path)

        contacts = payload.get("contacts") or []
        print(f"  page {page}/{total_pages}: {len(contacts)} contacts -> {path}")

        if page >= total_pages:
            break
        page += 1

    # The freshness guard in stage_sync.py reads file mtimes, so a pull that takes longer
    # than the guard's window would poison its own output. Say so rather than letting the
    # next step refuse with a misleading "re-fetch" message.
    oldest_age_hours = (time.time() - min(os.path.getmtime(p) for p in written)) / 3600
    if oldest_age_hours > 1:
        print(
            f"WARNING: the pull took {oldest_age_hours:.1f}h, so the first pages are already "
            "ageing against the 6-hour freshness guard. Run stage_sync.py now.",
            file=sys.stderr,
        )

    print(f"\n{len(written)} page file(s) written to {args.out_dir}")
    print("pass these to stage_sync.py --apollo:")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
