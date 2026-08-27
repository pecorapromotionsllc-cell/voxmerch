#!/usr/bin/env python3
"""
Apollo to Monday sequence-stage reconciler.

Why this exists
---------------
Nothing in the stack ever wrote Sequence Stage on the Sales Development Pipeline board
except the SDR skill setting it to "Queued" at contact creation. Every "Touch 1 Sent" and
"Touch 2 Sent" value on the board up to 2026-08-05 was typed in by hand during a chat
session. The four bridge automations on that board are all *triggered by* Sequence Stage,
so with nothing writing the column they could never fire. In particular a prospect reply
never reached Monday, which is why the reply chain looked broken for a week.

On 2026-08-05 this reconciler found 13 of 25 batch-1 contacts showing "Touch 1 Sent" when
Apollo had already sent them email 2.

What it does
------------
Pure mapping, no network. The caller (a Claude session, scheduled or interactive) fetches
the data with MCP tools, saves the raw JSON, and passes the file paths here. This script
derives the correct stage per contact and emits the exact `update_items` payload to apply.
Keeping the network out of the script is deliberate: the MCP tool results are large and
this way they never have to pass through a model's context to be processed.

Inputs
------
  --apollo   one or more JSON files from apollo_contacts_search (paginate until
             pagination.page == pagination.total_pages). The tool result is often written
             to a file by the harness because it exceeds the response limit; pass that
             file directly, leading prose and all.
  --board    one JSON file from get_board_items_page on board 18409325257, requesting at
             least columns color_mm2jstfm and text_mm2jzqfy.

Output
------
  stdout: a human-readable diff, then the JSON array for update_items.
  --out:   optional path to write just the JSON array.

Usage
-----
  python3 stage_sync.py --apollo p1.txt p2.txt p3.txt --board board.txt --out updates.json

Exit codes: 0 always, including when there is nothing to change. "No drift" is a normal
and desirable result, not an error.
"""

import argparse
import json
import os
import sys
import time

# The one live sequence. Deprecated 69e5407d76f3d1001dda3c7b and deferred
# 69e5434ea954b4001d4e951b are deliberately ignored: contacts sitting in those are not
# part of the current campaign and must not drive board state.
LIVE_SEQUENCE_ID = "6a6ab19632f101001070b98d"

# Step id to position, read from the sequence object's emailer_steps. Bulk
# apollo_contacts_search omits current_step_position but always returns current_step_id,
# so the id is the reliable key. Re-read these if the sequence is ever rebuilt.
STEP_POSITION = {
    "6a6ab19632f101001070b98e": 1,
    "6a6ab19632f101001070b990": 2,
    "6a6ab19632f101001070b992": 3,
}

SEQUENCE_STAGE_COLUMN = "color_mm2jstfm"
APOLLO_ID_COLUMN = "text_mm2jzqfy"
COLD_COMPANY_COLUMN = "text_mm2jqj2b"
COLD_TITLE_COLUMN = "text_mm2j4wc9"
COLD_EMAIL_COLUMN = "email_mm2jf16f"
COLD_PHONE_COLUMN = "phone_mm6k1xd8"
WARM_PHONE_COLUMN = "phone_mm6kh8xa"

# ---------------------------------------------------------------------------
# Promotion to the warm board.
#
# A board automation was supposed to do this: Sequence Stage becomes "Replied",
# Monday creates an item on the Outreach Pipeline and notifies Mary Anne. It never fired.
# Michael Junne at Creative Riff replied on 2026-08-07, the sync wrote Replied on 10 Aug,
# and two days later there was still no warm-board item and no notification. The likely
# reason is that a "when status changes" trigger does not respond to a column change made
# through the API, only to one made in the UI. Rather than depend on that, the sync now
# creates the item itself.
WARM_BOARD_ID = 18407308519
WARM_EMAIL_COLUMN = "email_mm2p17ty"

# Which cold stages earn a place on the warm board, and where each lands.
# Status is deliberately "New": it means untouched and needing work, and it is inert.
# Never write "Demo Attended" from here — on a HALO AE that label sends the prospect a
# real email from Mary Anne's mailbox.
PROMOTE = {
    "Replied": {
        "group": "group_mm24zx22",   # Event Activation Companies
        "source": "Cold Sequence Reply",
        "why": "replied to the cold sequence",
    },
    "Meeting Booked": {
        "group": "group_mm2432bm",   # Event Booked
        "source": "Cold Meeting Booked",
        "why": "booked a meeting off the cold sequence",
    },
}
WARM_STATUS_ON_ARRIVAL = "New"
WARM_SEGMENT = "Event Activation"

# The board's groups restate the stage, so they drift the same way the column did. Derive
# them from the same source of truth rather than moving cards by hand.
#
# Two stages are deliberately absent. "Meeting Booked" is omitted because an active board
# automation moves that item off this board entirely onto the Outreach Pipeline; emitting a
# group move for it would race the automation. "Replied" is included because its automation
# only *copies* the person to the other board and leaves this item in place.
STAGE_TO_GROUP = {
    "Queued": "group_mm2j71js",        # Queued for Outreach
    "Touch 1 Sent": "group_mm2jbc0j",  # In Sequence
    "Touch 2 Sent": "group_mm2jbc0j",  # In Sequence
    "Touch 3 Sent": "group_mm2j93xf",  # Sequence Complete
    "Replied": "group_mm2jt8h8",       # Replied
    "Bounced": "group_mm2jst5v",       # Not Interested / Bounced
}

# Never pull an item back out of these. They are curation decisions a human made, and the
# four off-limits groups in particular exist to keep people from being emailed again.
PROTECTED_GROUPS = {
    "group_mm5rb5mg",  # Archive - Company Placeholders
    "group_mm5rxery",  # Deferred - Distributors (Jan 1)
    "group_mm5rsxn3",  # Do Not Enroll - Prior Sequence (Call Only)
    "group_mm5r45k1",  # Out of Scope - Non-US
    "group_mm2j6gqq",  # Meeting Booked
    "group_mm2jst5v",  # Not Interested / Bounced
}

# current_step_position is the step the contact is waiting *on*, not the last one sent.
# A contact at position 3 has already received emails 1 and 2. Position 1 means nothing
# has gone out yet, which is still "Queued".
POSITION_TO_STAGE = {1: "Queued", 2: "Touch 1 Sent", 3: "Touch 2 Sent"}

# How far along each stage is, purely so a backwards move can be spotted. Replied, Bounced
# and Meeting Booked are terminal and sit outside the ladder, so they are absent here and
# never count as a regression.
RANK = {"Queued": 0, "Touch 1 Sent": 1, "Touch 2 Sent": 2, "Touch 3 Sent": 3}

# Stages that end the story. Once the board carries one, the sync leaves it alone.
TERMINAL_STAGES = {"Replied", "Meeting Booked", "Not Interested", "Bounced"}


# A stale input is the one way this script can do real damage. On 2026-08-13 it was run
# against Apollo files a week old and proposed pushing 51 contacts backwards to "Queued",
# which would have made two thirds of the campaign look unsent. The data itself carries no
# fetch timestamp, so file age is the only signal available. Refuse rather than warn.
MAX_INPUT_AGE_HOURS = 6


def check_freshness(paths, max_age_hours=MAX_INPUT_AGE_HOURS):
    """Abort if any input file is old enough to describe a different world."""
    stale = []
    for path in paths:
        age_hours = (time.time() - os.path.getmtime(path)) / 3600
        if age_hours > max_age_hours:
            stale.append((path, age_hours))
    if stale:
        print(
            f"REFUSING TO RUN: input older than {max_age_hours}h. Re-fetch before syncing.",
            file=sys.stderr,
        )
        for path, age_hours in stale:
            print(f"  {age_hours:.1f}h old: {path}", file=sys.stderr)
        print(
            "Stale input makes contacts look less far along than they are, and the sync would "
            "write that backwards onto the board.",
            file=sys.stderr,
        )
        raise SystemExit(2)


def load_json(path):
    """Read a tool-result file that may have explanatory prose before the JSON body."""
    text = open(path).read()
    start = text.find("{")
    if start == -1:
        raise ValueError(f"{path}: no JSON object found")
    return json.loads(text[start:])


def derive_stage(status, position, reason=None):
    """Map an Apollo campaign status onto a board Sequence Stage label.

    Terminal states win over step position, because a contact who replied or bounced
    stops advancing and the position it stopped at says nothing useful.
    """
    # "finished" alone is ambiguous and reading it as end-of-cadence is a trap. Apollo sets
    # it both when all three touches have gone out and when the sequence was cut short,
    # recording which in inactive_reason. Michael Junne replied on 2026-08-07 and Apollo
    # marked him finished/replied; without this branch the sync would have overwritten his
    # Replied stage with "Touch 3 Sent" and quietly erased the only reply in the campaign.
    if status == "finished" and reason:
        if reason in ("replied", "interested"):
            return "Replied"
        if reason in ("bounced", "hard_bounced", "spam_blocked"):
            return "Bounced"
        if reason == "unsubscribed":
            return "Not Interested"

    if status in ("bounced", "failed"):
        # "failed" is undocumented but real: Apollo used it on 2026-08-05 for a contact
        # whose send produced a soft bounce and a spam block. It behaves as terminal, so it
        # belongs with Bounced rather than falling through to the step position, which would
        # have left the person looking like a healthy in-sequence contact.
        return "Bounced"
    if status in ("replied", "interested"):
        return "Replied"
    if status == "finished":
        # Finished without replying means all three touches went out.
        return "Touch 3 Sent"
    if status not in ("active", "paused"):
        # Do not silently treat an unknown status as progress. Leaving the stage alone is
        # safer than guessing, and the caller is told to escalate.
        return None
    return POSITION_TO_STAGE.get(position, "Queued")


def collect_apollo(paths):
    """Return {apollo_contact_id: {...}} for every contact on the live sequence."""
    states = {}
    pages_seen = []
    for path in paths:
        payload = load_json(path)
        pagination = payload.get("pagination") or {}
        pages_seen.append((pagination.get("page"), pagination.get("total_pages")))
        for contact in payload.get("contacts") or []:
            live = [
                cs
                for cs in (contact.get("contact_campaign_statuses") or [])
                if cs.get("emailer_campaign_id") == LIVE_SEQUENCE_ID
            ]
            if not live:
                continue
            campaign_status = live[0]
            states[contact["id"]] = {
                "name": contact.get("name"),
                "status": campaign_status.get("status"),
                "reason": campaign_status.get("inactive_reason"),
                "position": STEP_POSITION.get(campaign_status.get("current_step_id")),
            }
    # A missing page silently understates drift, so say so rather than letting it pass.
    totals = {tp for _, tp in pages_seen if tp}
    if totals:
        expected = max(totals)
        got = {p for p, _ in pages_seen if p}
        missing = set(range(1, expected + 1)) - got
        if missing:
            print(
                f"WARNING: apollo pages {sorted(missing)} of {expected} were not supplied. "
                "Contacts on those pages cannot be reconciled.",
                file=sys.stderr,
            )
    return states


def _phone_text(value):
    """Monday returns phone columns as either a plain string or {'phone': ...}."""
    if isinstance(value, dict):
        return value.get("phone") or ""
    return value or ""


def load_board_pages(paths):
    """Merge one or more get_board_items_page result files into a single item list.

    Boards past ~300 items paginate. Refuse when the supplied files still say has_more,
    because a missing page makes every contact on it look absent from the board, and the
    "in Apollo but not on the board" alert would fire for all of them.
    """
    items = []
    open_cursors = 0
    for path in paths:
        payload = load_json(path)
        items.extend(payload.get("items") or [])
        if (payload.get("pagination") or {}).get("has_more"):
            open_cursors += 1
    if open_cursors >= len(paths):
        print(
            "REFUSING TO RUN: the board fetch is incomplete (pagination.has_more is true and no "
            "continuation file was supplied). Re-call get_board_items_page with the nextCursor "
            "value until has_more is false, and pass every page file to this script.",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return items


def collect_board(paths):
    """Return {apollo_contact_id: {item_id, name, stage}} for items carrying an Apollo id."""
    items = load_board_pages(paths)
    board = {}
    for item in items:
        values = item.get("column_values") or {}
        apollo_id = values.get(APOLLO_ID_COLUMN)
        if not apollo_id:
            continue
        board[apollo_id] = {
            "item_id": int(item["id"]),
            "name": item.get("name"),
            "stage": values.get(SEQUENCE_STAGE_COLUMN),
            "group_id": (item.get("group") or {}).get("id"),
            "company": values.get(COLD_COMPANY_COLUMN) or "",
            "title": values.get(COLD_TITLE_COLUMN) or "",
            "email": values.get(COLD_EMAIL_COLUMN) or "",
            "phone": _phone_text(values.get(COLD_PHONE_COLUMN)),
        }
    return board


def normalise(text):
    """Loose key for duplicate detection: lowercased, trimmed."""
    return (text or "").strip().lower()


def collect_warm(paths):
    """Return the emails and names already present on the Outreach Pipeline.

    This is what makes the sync safe to run every weekday. A contact sits at Replied
    indefinitely, so without a duplicate check the sync would mint a fresh warm-board item
    for the same person every morning.
    """
    items = load_board_pages(paths)
    emails, names = set(), set()
    for item in items:
        values = item.get("column_values") or {}
        email = normalise(values.get(WARM_EMAIL_COLUMN))
        if email:
            emails.add(email)
        names.add(normalise(item.get("name")))
    return emails, names


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apollo", nargs="+", required=True, help="apollo_contacts_search result files")
    parser.add_argument("--board", nargs="+", required=True, help="get_board_items_page result file(s), cold board; pass every page when the board paginates")
    parser.add_argument("--warm", nargs="+", help="get_board_items_page result file(s), Outreach Pipeline 18407308519")
    parser.add_argument("--out", help="write the update_items payload here")
    args = parser.parse_args()

    inputs = list(args.apollo) + list(args.board) + (list(args.warm) if args.warm else [])
    check_freshness(inputs)

    apollo = collect_apollo(args.apollo)
    board = collect_board(args.board)
    if args.warm:
        warm_emails, warm_names = collect_warm(args.warm)
    else:
        warm_emails, warm_names = None, None

    updates = []
    group_moves = []
    promotions = []
    regressions = []
    already_warm = []
    unmatched = []
    unknown_status = []
    for apollo_id, state in sorted(apollo.items(), key=lambda kv: kv[1]["name"] or ""):
        target = derive_stage(state["status"], state["position"], state.get("reason"))
        if target is None:
            unknown_status.append((state["name"], state["status"]))
            continue
        item = board.get(apollo_id)
        if item and item["stage"] in TERMINAL_STAGES and target not in TERMINAL_STAGES:
            # A terminal stage is worth more than any ladder position, and it is often set
            # from knowledge Apollo does not have. Never downgrade one.
            continue
        if not item:
            # Expected for the internal test contact. Anything else here means a contact
            # is being emailed with no board record, which is worth chasing.
            unmatched.append(state["name"])
            continue
        if item["stage"] != target:
            arrow = "  stage "
            if RANK.get(item["stage"], -1) > RANK.get(target, -1):
                # Regression. Legitimate when a reply or bounce ends the sequence, suspicious
                # otherwise, and the loudest early symptom of stale input.
                arrow = "  STAGE\u2193"
                regressions.append((state["name"], item["stage"], target))
            print(f"{arrow} {state['name']:<26} {item['stage']} -> {target}   (item {item['item_id']})")
            updates.append(
                {
                    "itemId": item["item_id"],
                    "columnValues": json.dumps({SEQUENCE_STAGE_COLUMN: {"label": target}}),
                }
            )
        # Promote a reply or a booked meeting onto the warm board, once.
        if target in PROMOTE:
            if warm_emails is None:
                already_warm.append((state["name"], "warm board not supplied, cannot dedupe"))
            elif normalise(item["email"]) in warm_emails or normalise(item["name"]) in warm_names:
                already_warm.append((state["name"], "already on the warm board"))
            else:
                spec = PROMOTE[target]
                note = (
                    f"Promoted from the cold board because they {spec['why']}. "
                    f"Apollo contact {apollo_id}. Cold board item {item['item_id']}. "
                    "Created by the Apollo to Monday stage sync, not by a board automation. "
                    "Check for an existing duplicate record before working it."
                )
                column_values = {
                    "text_mm24nn4v": item["company"],
                    "text_mm24vp7s": item["title"],
                    "color_mm24v105": {"label": WARM_STATUS_ON_ARRIVAL},
                    "color_mm2tryes": {"label": WARM_SEGMENT},
                    "color_mm2tsj69": {"label": spec["source"]},
                    "long_text_mm24bypr": note,
                }
                if item["email"]:
                    column_values["email_mm2p17ty"] = {"email": item["email"], "text": item["email"]}
                if item.get("phone"):
                    column_values[WARM_PHONE_COLUMN] = item["phone"]
                print(f"  PROMOTE {state['name']:<26} -> Outreach Pipeline ({target})")
                promotions.append(
                    {
                        "name": item["name"],
                        "groupId": spec["group"],
                        "columnValues": json.dumps(column_values),
                    }
                )

        target_group = STAGE_TO_GROUP.get(target)
        if (
            target_group
            and item["group_id"] != target_group
            and item["group_id"] not in PROTECTED_GROUPS
        ):
            print(f"  group  {state['name']:<26} {item['group_id']} -> {target_group}   (item {item['item_id']})")
            group_moves.append({"itemId": item["item_id"], "groupId": target_group})

    print(f"\non live sequence: {len(apollo)}   board records matched: {len(apollo) - len(unmatched)}")
    if unmatched:
        print(f"in Apollo but not on the board: {', '.join(n or '?' for n in unmatched)}")
    if unknown_status:
        print("\nESCALATE: unrecognised Apollo status, stage left untouched:")
        for name, status in unknown_status:
            print(f"  {name}: status={status!r}")
    if already_warm:
        for name, reason in already_warm:
            print(f"  skip promotion: {name} ({reason})")
    print(f"stage changes needed: {len(updates)}")
    print(f"group moves needed: {len(group_moves)}")
    print(f"promotions to the warm board: {len(promotions)}")
    if regressions:
        print(
            f"\nWARNING: {len(regressions)} contact(s) would move BACKWARDS along the ladder. "
            "With fresh input this is rare. Check the Apollo pull before applying."
        )

    payload = json.dumps(updates, separators=(",", ":"))
    moves_payload = json.dumps(group_moves, separators=(",", ":"))
    promotions_payload = json.dumps(promotions, separators=(",", ":"))
    if args.out:
        open(args.out, "w").write(payload)
        print(f"stage payload written to {args.out}")
        moves_path = args.out.replace(".json", "") + ".groups.json"
        open(moves_path, "w").write(moves_payload)
        print(f"group moves written to {moves_path}")
        promo_path = args.out.replace(".json", "") + ".promotions.json"
        open(promo_path, "w").write(promotions_payload)
        print(f"promotions written to {promo_path}")
    else:
        print("\nstage updates:\n" + payload)
        print("\ngroup moves:\n" + moves_payload)
        print("\npromotions:\n" + promotions_payload)


if __name__ == "__main__":
    main()
