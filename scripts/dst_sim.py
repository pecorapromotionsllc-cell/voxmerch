#!/usr/bin/env python3
"""Test the DST cron table without touching a live trigger.

The routine `trig_01Ns34qxeJuDdXsNwM3uJobk` rewrites twelve crons on two Sundays a
year. Those two firings are the only time its logic runs in anger, so a mistake in
the table sits undetected for months and then moves every routine by an hour in the
wrong direction. This reproduces the routine's decision rule offline.

Run it after editing the table in scheduled-routines.md or in the routine's prompt.
No network, no tools, no mutation.

    python3 scripts/dst_sim.py
"""
import datetime as dt
import sys

# Mirror of the table in scheduled-routines.md and in the routine's own prompt.
# id, name, local time (America/Chicago), CDT cron, CST cron
TABLE = [
 ("trig_01JVD2riMmKBBiETC75BF2kF","Second Brain Daily Housekeeping","2:00 AM daily","0 7 * * *","0 8 * * *"),
 ("trig_01QbNjW5kYTQHNJhLY3XS5Qi","Voxmerch meeting prep","4:15 AM Mon-Fri","15 9 * * 1-5","15 10 * * 1-5"),
 ("trig_01Ns34qxeJuDdXsNwM3uJobk","DST cron shift (itself)","4:00 AM Sunday","0 9 * * 0","0 10 * * 0"),
 ("trig_0153Ljh1jbUU1tk6Qy5zHf6d","Voxmerch daily briefing","5:00 AM Mon-Fri","0 10 * * 1-5","0 11 * * 1-5"),
 ("trig_01SyoicQWryJcHtVyeKbwGoW","Apollo to Monday Sequence Stage Sync","7:00 AM Mon-Fri","0 12 * * 1-5","0 13 * * 1-5"),
 ("trig_01Rn12DM3dvShH1NKsahkQ8B","Weekly Grant Applications Run","7:00 AM Monday","0 12 * * 1","0 13 * * 1"),
 ("trig_018YGYeQAQUmDXjnRqgph4XY","Pipeline Dashboard Daily Refresh","8:00 AM daily","0 13 * * *","0 14 * * *"),
 ("trig_012foHTATGMmm2NgAuyp6tkj","Inbox Triage and Draft","8:00 AM Mon-Fri","0 13 * * 1-5","0 14 * * 1-5"),
 ("trig_0186VSN7qdKFmW2zAqJaCFk9","Inbound Demo Lead Enrichment","8:00 AM + 2:00 PM daily","0 13,19 * * *","0 14,20 * * *"),
 ("trig_01TcTo6os9dJgknmouV96Qdt","Weekly Deep Pass","8:00 AM Saturday","0 13 * * 6","0 14 * * 6"),
 ("trig_01PRGp61GvSMr8qSv1jsdTVD","Monthly prune pass","8:00 AM on the 1st","0 13 1 * *","0 14 1 * *"),
 ("trig_01BcLhZpsgGXmdCoU4M419m1","Sunday week-ahead meeting prep","8:00 PM Sunday","0 1 * * 1","0 2 * * 1"),
]

# Live crons as of 2026-08-24, all at their CDT values.
BASELINE = {tid: cdt for tid, _, _, cdt, _ in TABLE}

failures = []

def check(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{'  ' + detail if detail else ''}")
    if not ok:
        failures.append(label)

def nth_sunday(year, month, n):
    d = dt.date(year, month, 1)
    d += dt.timedelta(days=(6 - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)

def gate(d):
    """The routine's STEP 1. Returns the target column, or None to do nothing."""
    if d.weekday() != 6:
        return None
    if d.month == 11 and 1 <= d.day <= 7:
        return "CST"
    if d.month == 3 and 8 <= d.day <= 14:
        return "CDT"
    return None

def apply(state, today):
    """The routine's STEP 4. Returns (new state, changed, noop, reported)."""
    target = gate(today)
    if not target:
        return dict(state), [], [], []
    out, changed, noop, reported = dict(state), [], [], []
    for tid, name, local, cdt, cst in TABLE:
        want, other = (cst, cdt) if target == "CST" else (cdt, cst)
        cur = state.get(tid)
        if cur is None:
            reported.append((name, "not found"))
        elif cur == want:
            noop.append(name)
        elif cur == other:
            changed.append((name, local, cur, want))
            out[tid] = want
        else:
            reported.append((name, f"cron {cur!r} matches neither column"))
    return out, changed, noop, reported


print("\n1. Table integrity")
ids = [r[0] for r in TABLE]
check("twelve rows", len(TABLE) == 12, f"got {len(TABLE)}")
check("no duplicate trigger ids", len(set(ids)) == len(ids))
for tid, name, local, cdt, cst in TABLE:
    c, s = cdt.split(), cst.split()
    same_shape = c[0] == s[0] and c[2:] == s[2:]
    hours_ok = [(int(h) + 1) % 24 for h in c[1].split(",")] == [int(h) for h in s[1].split(",")]
    check(f"{name}: CST is CDT plus one hour, nothing else changed",
          same_shape and hours_ok, f"{cdt!r} vs {cst!r}")

print("\n2. Gate, 2026 through 2035")
for y in range(2026, 2036):
    fb, sf = nth_sunday(y, 11, 1), nth_sunday(y, 3, 2)
    check(f"{y} fall-back {fb} opens as CST", gate(fb) == "CST")
    check(f"{y} spring-forward {sf} opens as CDT", gate(sf) == "CDT")
false_pos = [dt.date(y, m, d)
             for y in range(2026, 2036) for m, lo, hi in ((11, 1, 7), (3, 8, 14))
             for d in range(lo, hi + 1)
             if dt.date(y, m, d).weekday() == 6
             and dt.date(y, m, d) not in (nth_sunday(y, 11, 1), nth_sunday(y, 3, 2))]
check("no non-transition Sunday falls inside either window", not false_pos, str(false_pos))
for d in (dt.date(2026, 8, 30), dt.date(2026, 12, 6), dt.date(2026, 11, 2), dt.date(2027, 3, 15)):
    check(f"{d:%a %d %b %Y} stays closed", gate(d) is None)

print("\n3. Fall back, then spring forward, from live state")
after_fb, changed, noop, reported = apply(BASELINE, dt.date(2026, 11, 1))
check("all twelve shift to CST", (len(changed), len(noop), len(reported)) == (12, 0, 0),
      f"{len(changed)} changed / {len(noop)} no-op / {len(reported)} reported")
_, c2, n2, r2 = apply(after_fb, dt.date(2026, 11, 1))
check("firing twice the same day is a no-op", (len(c2), len(n2), len(r2)) == (0, 12, 0))
after_sf, c3, _, _ = apply(after_fb, dt.date(2027, 3, 14))
check("all twelve shift back to CDT", len(c3) == 12)
check("round trip returns every routine to where it started", after_sf == BASELINE)

print("\n4. A cron changed by hand is reported, not clobbered")
tampered = dict(BASELINE)
tampered["trig_018YGYeQAQUmDXjnRqgph4XY"] = "30 15 * * *"   # someone moved the dashboard to 10:30 AM CT
out, c4, _, r4 = apply(tampered, dt.date(2026, 11, 1))
check("the other eleven still shift", len(c4) == 11)
check("the hand-edited row is left alone", out["trig_018YGYeQAQUmDXjnRqgph4XY"] == "30 15 * * *")
check("and is named in the report", len(r4) == 1 and "matches neither" in r4[0][1])

print("\n5. Ordering the morning read depends on")
sync, dash = "trig_01SyoicQWryJcHtVyeKbwGoW", "trig_018YGYeQAQUmDXjnRqgph4XY"
for label, st in (("CDT", BASELINE), ("CST", after_fb)):
    gap = int(st[dash].split()[1]) - int(st[sync].split()[1])
    check(f"under {label}, dashboard still refreshes one hour after the Apollo sync", gap == 1)

print(f"\n{'ALL CHECKS PASSED' if not failures else str(len(failures)) + ' FAILED: ' + '; '.join(failures)}\n")
sys.exit(1 if failures else 0)
