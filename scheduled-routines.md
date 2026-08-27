# Scheduled routines and the daylight saving problem

Written 2026-08-24. Every Claude routine on this account is a cron expression **evaluated in UTC**.
Chicago is not UTC and its offset changes twice a year, so a cron that is correct in August is wrong
by an hour in December unless somebody moves it.

- **CDT = UTC-5**, roughly the second Sunday in March to the first Sunday in November.
- **CST = UTC-6**, the rest of the year.

To hold a fixed local time, the UTC hour goes **up by one** at the November fall-back and **down by
one** at the March spring-forward.

## Who does the shifting

Trigger `trig_01Ns34qxeJuDdXsNwM3uJobk`, "DST cron shift for all VoxMerch routines", fires every
Sunday and does nothing on about fifty of them. On the first Sunday of November and the second
Sunday of March it walks the table below and rewrites each cron.

Until 2026-08-24 that routine named exactly one trigger id, the 2:00 AM daily housekeeping run, and
left the other eleven to drift. This file is the canonical table; the routine carries a copy of it
in its own prompt, because it runs in a cloud session that has no guarantee of a repo clone.

**If you change a cron by hand, change it here too.** The routine compares each trigger against both
columns and refuses to touch anything matching neither, so an undocumented hand edit does not get
clobbered. It gets skipped and reported, and then it drifts. Silence is the failure mode.

## The table

Local times are America/Chicago. The two cron columns are the same wall-clock moment expressed for
each offset.

| Trigger id | Name | Local | CDT cron | CST cron |
|---|---|---|---|---|
| `trig_01JVD2riMmKBBiETC75BF2kF` | VoxMerch Second Brain — Daily Housekeeping | 2:00 AM daily | `0 7 * * *` | `0 8 * * *` |
| `trig_01QbNjW5kYTQHNJhLY3XS5Qi` | Voxmerch meeting prep | 4:15 AM Mon-Fri | `15 9 * * 1-5` | `15 10 * * 1-5` |
| `trig_01Ns34qxeJuDdXsNwM3uJobk` | DST cron shift for all VoxMerch routines | 4:00 AM Sunday | `0 9 * * 0` | `0 10 * * 0` |
| `trig_0153Ljh1jbUU1tk6Qy5zHf6d` | Voxmerch daily briefing | 5:00 AM Mon-Fri | `0 10 * * 1-5` | `0 11 * * 1-5` |
| `trig_01SyoicQWryJcHtVyeKbwGoW` | Apollo to Monday Sequence Stage Sync | 7:00 AM Mon-Fri | `0 12 * * 1-5` | `0 13 * * 1-5` |
| `trig_01Rn12DM3dvShH1NKsahkQ8B` | Weekly Grant Applications Run | 7:00 AM Monday | `0 12 * * 1` | `0 13 * * 1` |
| `trig_018YGYeQAQUmDXjnRqgph4XY` | VoxMerch Pipeline Dashboard — Daily Refresh | 8:00 AM daily | `0 13 * * *` | `0 14 * * *` |
| `trig_012foHTATGMmm2NgAuyp6tkj` | Inbox Triage and Draft | 8:00 AM Mon-Fri | `0 13 * * 1-5` | `0 14 * * 1-5` |
| `trig_0186VSN7qdKFmW2zAqJaCFk9` | Inbound Demo Lead Enrichment and Handoff | 8:00 AM and 2:00 PM daily | `0 13,19 * * *` | `0 14,20 * * *` |
| `trig_01TcTo6os9dJgknmouV96Qdt` | Weekly Deep Pass | 8:00 AM Saturday | `0 13 * * 6` | `0 14 * * 6` |
| `trig_01PRGp61GvSMr8qSv1jsdTVD` | Monthly prune pass: VoxMerch learned rules | 8:00 AM on the 1st | `0 13 1 * *` | `0 14 1 * *` |
| `trig_01BcLhZpsgGXmdCoU4M419m1` | Sunday week-ahead meeting prep | 8:00 PM Sunday | `0 1 * * 1` | `0 2 * * 1` |

Twelve rows, which is every recurring routine on the account. One-shot triggers set with
`run_once_at` are not in scope; they carry an absolute timestamp and cannot drift.

### Two rows that read oddly, and why they are right

**Sunday week-ahead meeting prep runs on a Monday cron.** 8:00 PM Sunday Central is 01:00 UTC
Monday, so the day-of-week field says Monday. It is the only row where the UTC date and the local
date differ, and it is the row most likely to get "fixed" by somebody who has not checked. Leave it.

**The DST routine shifts itself, last.** It fires at 09:00 UTC, which on the November Sunday is
3:00 AM CST, comfortably after the 2:00 AM local transition. So it is awake and correct at the
moment it needs to act, and moving its own cron afterwards only affects the following week.

## Testing the table

`scripts/dst_sim.py` reproduces the routine's decision rule offline: no network, no tools, no
mutation. **Run it after editing the table here or in the routine's prompt.**

    python3 scripts/dst_sim.py

It checks table integrity (twelve rows, unique ids, and that each CST cron is its CDT cron plus
exactly one hour with every other field untouched), the Sunday gate against the real transition
dates from 2026 to 2035, a full fall-back then spring-forward round trip that has to land every
routine back where it started, that firing twice on the same Sunday is a no-op, that a cron changed
by hand is reported rather than overwritten, and that the dashboard still refreshes one hour after
the Apollo sync under both offsets. Exit code is non-zero on any failure.

Last run 2026-08-24: all checks passed.

## Ordering on transition day

The sequence that matters most is Apollo sync at 7:00 AM feeding the dashboard refresh at 8:00 AM.
Both rows shift by the same hour in the same direction, so the gap is preserved through the
transition whether or not the routine runs. If the routine fails entirely, the whole schedule slides
an hour together rather than breaking apart. That is the intended failure mode.

## Weekend gap, unrelated to DST but worth knowing

The dashboard refreshes seven days a week and the Apollo sync runs weekdays only, so Saturday and
Sunday dashboards render Friday's Sequence Stage data. Not stale in any dangerous way, but a weekend
snapshot is not a fresh read of Apollo.
