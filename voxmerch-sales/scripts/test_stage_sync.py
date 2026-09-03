#!/usr/bin/env python3
"""
Fixture tests for the stage_sync.py coverage guard.

The guard's whole job is to turn a silent failure into a loud one, so it is worth proving
it actually fires. A filtered Apollo pull that drops an enrolled contact used to leave that
person's board stage stale with nothing printed anywhere; these cases pin down that it now
warns by default and refuses under --strict-coverage.

Run: python3 voxmerch-sales/scripts/test_stage_sync.py
"""

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SYNC = os.path.join(HERE, "stage_sync.py")

LIVE = "6a6ab19632f101001070b98d"
STEP_2 = "6a6ab19632f101001070b990"


def apollo_page(contacts, page=1, total_pages=1):
    return {
        "pagination": {"page": page, "total_pages": total_pages, "per_page": 100},
        "contacts": contacts,
    }


def contact(contact_id, name, status="active", step=STEP_2, reason=None):
    return {
        "id": contact_id,
        "name": name,
        "contact_campaign_statuses": [
            {
                "emailer_campaign_id": LIVE,
                "status": status,
                "current_step_id": step,
                "inactive_reason": reason,
            }
        ],
    }


def board_item(item_id, name, apollo_id, stage, group="group_mm2jbc0j"):
    return {
        "id": str(item_id),
        "name": name,
        "group": {"id": group},
        "column_values": {
            "text_mm2jzqfy": apollo_id,
            "color_mm2jstfm": stage,
            "text_mm2jqj2b": "Test Agency",
            "text_mm2j4wc9": "Account Director",
            "email_mm2jf16f": f"{name.split()[0].lower()}@example.com",
        },
    }


def run(tmp, apollo_contacts, board_items, extra_args=()):
    """Write fixtures fresh (so the 6h guard passes) and run the reconciler."""
    apollo_path = os.path.join(tmp, "apollo.json")
    board_path = os.path.join(tmp, "board.json")
    warm_path = os.path.join(tmp, "warm.json")

    with open(apollo_path, "w") as handle:
        json.dump(apollo_page(apollo_contacts), handle)
    with open(board_path, "w") as handle:
        json.dump({"items": board_items, "pagination": {"has_more": False}}, handle)
    with open(warm_path, "w") as handle:
        json.dump({"items": [], "pagination": {"has_more": False}}, handle)

    return subprocess.run(
        [sys.executable, SYNC, "--apollo", apollo_path, "--board", board_path,
         "--warm", warm_path, *extra_args],
        capture_output=True,
        text=True,
    )


def main():
    failures = []

    def check(label, condition, detail=""):
        if condition:
            print(f"  pass  {label}")
        else:
            print(f"  FAIL  {label} {detail}")
            failures.append(label)

    with tempfile.TemporaryDirectory() as tmp:
        # A contact the pull covered and the board understates: the ordinary case, and the
        # baseline that proves the guard is not firing on everything.
        print("full pull, one genuine drift:")
        result = run(
            tmp,
            [contact("c1", "Ada Reeve")],
            [board_item(1, "Ada Reeve", "c1", "Queued")],
        )
        check("exits 0", result.returncode == 0, f"got {result.returncode}")
        check("writes the drift", "Queued -> Touch 1 Sent" in result.stdout)
        check("reports zero uncovered", "board items not covered by it: 0" in result.stdout)
        check("stays quiet about coverage", "never returned" not in result.stderr)

        # The failure mode the guard exists for: the board carries an Apollo id the pull
        # never mentioned. Before the guard, this printed nothing at all.
        print("\nfiltered pull dropping an enrolled contact:")
        result = run(
            tmp,
            [contact("c1", "Ada Reeve")],
            [board_item(1, "Ada Reeve", "c1", "Touch 1 Sent"),
             board_item(2, "Bo Nakamura", "c2", "Queued")],
        )
        check("still exits 0 by default", result.returncode == 0, f"got {result.returncode}")
        check("counts the gap", "board items not covered by it: 1" in result.stdout)
        check("names the person", "Bo Nakamura" in result.stderr)
        check("names the apollo id", "c2" in result.stderr)

        print("\nsame input under --strict-coverage:")
        result = run(
            tmp,
            [contact("c1", "Ada Reeve")],
            [board_item(1, "Ada Reeve", "c1", "Touch 1 Sent"),
             board_item(2, "Bo Nakamura", "c2", "Queued")],
            extra_args=("--strict-coverage",),
        )
        check("refuses", result.returncode == 2, f"got {result.returncode}")
        check("says why", "REFUSING TO RUN" in result.stderr)
        check("emits no payload", "stage updates:" not in result.stdout)

        # Terminal states still outrank coverage noise, and a reply must still promote.
        print("\na reply still promotes with the guard in place:")
        result = run(
            tmp,
            [contact("c1", "Ada Reeve", status="finished", reason="replied")],
            [board_item(1, "Ada Reeve", "c1", "Touch 2 Sent")],
        )
        check("exits 0", result.returncode == 0, f"got {result.returncode}")
        check("derives Replied", "-> Replied" in result.stdout)
        check("promotes once", "promotions to the warm board: 1" in result.stdout)

    print()
    if failures:
        print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
