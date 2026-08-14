# Working conventions for this repo

## Time: always Central

**Every time shown to Mary Anne is Central time, labelled CT.** Not UTC, not "10:33" with no zone.
She reads this repo, the dashboard, and every status report at a glance, and a mixed-zone report is
how the 3 Aug and 4 Aug misreadings of the send window happened.

- Central Daylight Time, **CDT = UTC-5**, roughly early March to early November.
- Central Standard Time, **CST = UTC-6**, roughly early November to early March.
- Convert before writing. Say "7:00 AM CDT", not "12:00 UTC".
- Where a stored value is genuinely UTC and someone will need it to configure a system, give both:
  "7:00 AM CDT (cron `0 12 * * 1-5`, which is UTC)". Cron expressions on Claude routines are
  evaluated in UTC and must stay that way; only the human-facing description converts.
- Apollo, Monday, and Outlook all return UTC over their APIs. Treat that as raw input, never as
  something to hand back unconverted.

Watch the DST boundary. A cron fixed in UTC shifts by an hour in local terms twice a year, so a
routine that runs at 7:00 AM CDT in August runs at 6:00 AM CST in December unless the cron is moved.

## Dates and elapsed time

Sequence gaps count **business days**, not calendar days. Email 2 is three business days after email
1; email 3 is four business days after email 2. Three separate readings of the campaign went wrong
by assuming calendar days, so state the working out when a date matters.

## Naming the source of a number

Say where a figure came from when it could be contested: "Apollo says", "the board says", "counted in
Sent Items". Apollo's counters and the Monday board disagreed for a week without anyone noticing,
and the fix depended on being able to tell which one was being quoted.
