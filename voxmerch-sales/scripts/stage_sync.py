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
import sys

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


def load_json(path):
    """Read a tool-result file that may have explanatory prose before the JSON body."""
    text = open(path).read()
    start = text.find("{")
    if start == -1:
        raise ValueError(f"{path}: no JSON object found")
    return json.loads(text[start:])


def derive_stage(status, position):
    """Map an Apollo campaign status onto a board Sequence Stage label.

    Terminal states win over step position, because a contact who replied or bounced
    stops advancing and the position it stopped at says nothing useful.
    """
    if status == "bounced":
        return "Bounced"
    if status in ("replied", "interested"):
        return "Replied"
    if status == "finished":
        # Finished without replying means all three touches went out.
        return "Touch 3 Sent"
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


def collect_board(path):
    """Return {apollo_contact_id: {item_id, name, stage}} for items carrying an Apollo id."""
    items = load_json(path).get("items") or []
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
        }
    return board


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apollo", nargs="+", required=True, help="apollo_contacts_search result files")
    parser.add_argument("--board", required=True, help="get_board_items_page result file")
    parser.add_argument("--out", help="write the update_items payload here")
    args = parser.parse_args()

    apollo = collect_apollo(args.apollo)
    board = collect_board(args.board)

    updates = []
    group_moves = []
    unmatched = []
    for apollo_id, state in sorted(apollo.items(), key=lambda kv: kv[1]["name"] or ""):
        target = derive_stage(state["status"], state["position"])
        item = board.get(apollo_id)
        if not item:
            # Expected for the internal test contact. Anything else here means a contact
            # is being emailed with no board record, which is worth chasing.
            unmatched.append(state["name"])
            continue
        if item["stage"] != target:
            print(f"  stage  {state['name']:<26} {item['stage']} -> {target}   (item {item['item_id']})")
            updates.append(
                {
                    "itemId": item["item_id"],
                    "columnValues": json.dumps({SEQUENCE_STAGE_COLUMN: {"label": target}}),
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
    print(f"stage changes needed: {len(updates)}")
    print(f"group moves needed: {len(group_moves)}")

    payload = json.dumps(updates, separators=(",", ":"))
    moves_payload = json.dumps(group_moves, separators=(",", ":"))
    if args.out:
        open(args.out, "w").write(payload)
        print(f"stage payload written to {args.out}")
        moves_path = args.out.replace(".json", "") + ".groups.json"
        open(moves_path, "w").write(moves_payload)
        print(f"group moves written to {moves_path}")
    else:
        print("\nstage updates:\n" + payload)
        print("\ngroup moves:\n" + moves_payload)


if __name__ == "__main__":
    main()
