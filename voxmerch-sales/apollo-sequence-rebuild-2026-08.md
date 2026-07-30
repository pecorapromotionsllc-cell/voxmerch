# Apollo Sequence Rebuild: Event Agencies and Planners

Build date: 2026-07-30. Status: **built in Apollo, inactive, awaiting Mary Anne's copy approval
to activate.** New sequence ID: `6a6ab19632f101001070b98d`.

Executed 2026-07-30 after connector re-auth (full remove and reconnect fixed a read-only OAuth
grant): old sequence deactivated and renamed "[DEPRECATED - DO NOT USE]", its templates replaced
with deprecation notices; new sequence created inactive with all three touches verified in the
API response, 25/day cap on step 1. Remaining manual cleanup: the old sequence still holds 11
paused contacts at step 2. They are inert (sequence inactive and deprecated), and the contacts
search API cannot filter by sequence, so remove them in the Apollo UI from the deprecated
sequence's Contacts tab.

This replaces "VoxMerch - Event Activation 3-Touch" (69e5407d76f3d1001dda3c7b), which is being
scrapped: the audience contained company names without people, international companies out of
scope, and the sequence was misconstructed from the start. All performance data from it is void.
"VoxMerch - Promo Distributors 3-Touch" stays off until January 1.

## Verified state (checked live 2026-07-30)

- Sending mailbox: maryanne@voxmerch.com, Microsoft Exchange, active, default.
  Account ID `6a26172e997526000c9110f0`.
- Promo Distributors sequence: inactive. Correct, no action.
- **Old Event Activation sequence still reads `active: true` with 11 contacts in the scheduled
  queue.** Its manual_approve setting means nothing sends, but the off-switch did not persist.
  Execution step 1 below deactivates it and clears the queue.

## Execution steps (run in order once Apollo is re-authorized)

1. Deactivate old sequence 69e5407d76f3d1001dda3c7b and remove its 11 queued contacts.
2. Create the new sequence per the spec below, **inactive**.
3. Mary Anne reviews the copy and approves.
4. Verify tracking end to end with one internal test contact before any real enrollment.
5. Enroll the clean audience (spec below) and activate.

## Sequence spec

- **Name:** VoxMerch - Event Agencies and Planners - 3-Touch
- **Sender:** maryanne@voxmerch.com (ID above)
- **Schedule:** account default (weekday business hours)
- **Created inactive.** Activation only after Mary Anne approves copy. Once active, it auto-sends
  with no per-email approval and no paused enrollment. Those two gates are what stalled the last
  campaign.
- **Step 1 send cap: 25/day** for the first week of sending, then raise to 40, then 50+.
  Warmup traffic counts against the mailbox ceiling.
- Stop-on-reply: on. Pause on out-of-office: on.

## Email copy (for Mary Anne's approval)

Voice rules applied: subject 2 to 4 words lowercase, complete sentences throughout including the
ask, leads with the intelligence asset, one ask with named days, no banned phrases, no em-dashes,
additive framing that never disparages badge scanning or any activation category. Signature is
appended automatically by Apollo, so bodies do not repeat the name.

### Email 1, day 0. Subject: `what the room believes`

> Hi {{first_name}},
>
> Every post-event report says how many people stopped by. Almost none can say what those people
> believe about the problem the brand exists to solve.
>
> VoxMerch produces that second report. An attendee speaks for about 20 seconds, and 30 seconds
> later their voice has become one-of-a-kind artwork they take home. The brand keeps the read on
> what the room said. At a Fortune 500 healthcare company's event, 89% of attendees opted in.
>
> Do you have 15 minutes on Tuesday or Wednesday to see it live?

### Email 2, day 3. Subject: `your next pitch`

> Hi {{first_name}},
>
> A different thought from my last note. If {{company}} is pitching an event right now, I will
> build the activation section of that proposal for you at no cost: artwork mockups on your
> client's brand, a sample of the intelligence report they would receive, and the pricing already
> worked out, all presented under your name.
>
> There is no fee unless your client approves it and the event books. Which pitch should we build
> it around?

### Email 3, day 7. Subject: `198 activations`

> Hi {{first_name}},
>
> Last note from me. At a recent two-day conference for a Fortune 500 healthcare company, we ran
> 198 activations, and 89% of the attendees we invited opted in. The client left with artwork
> their people still talk about and a report on what their audience actually believes.
>
> If that would help {{company}} win a Q4 pitch, reply and I will build you a client-ready
> proposal this week. Otherwise I will check back in the new year.

Phone and LinkedIn carry the remaining touches outside Apollo: Debra dials from the Monday queue,
Mary Anne sends LinkedIn requests manually, capped at 100 per week.

## Audience spec (what gets enrolled, and nothing else)

- **People only.** Never a company placeholder. Real first and last name required.
- **United States only.** `person_locations: ["United States"]` on every search, no exceptions.
- **Verified email required** before enrollment. No unverified sends.
- **Titles, in priority order:** Account Director, Account Lead, VP Client Services, Director of
  Client Services, VP of Events, Director of Events, Director of Experiential Marketing, Head of
  Event Strategy, Managing Director. Producers are contacted second, by phone, with an operations
  answer sheet, never as the sequence entry point. President and CEO are not lead titles except
  at firms under roughly 25 employees, where the founder is the account lead.
- **Segments:** event activation companies and experiential agencies; meeting planner
  sub-segments that can resell at a markup (independent and third-party planners, DMCs,
  production companies, exhibit houses). Corporate in-house event teams are end clients: do not
  enroll, route to a partner.
- **Sources:** Event Marketer 2026 It List filtered to Trade Show Programs and User Conferences;
  the 56 verified mid-size independents already researched; existing clean CRM contacts;
  association lists (MPI, PCMA, IAEE) pending the licensing check.
- 2 to 3 contacts per company, one batched enrollment call per company, `run_dedupe: true`.

## Tracking (answering "how will analytics be tracked and where")

1. **Apollo, sequence level:** delivered, opens, clicks, replies, bounces, unsubscribes per step.
   Watch bounce rate (under 2%) and spam complaints (near zero). Opens and clicks are soft
   signals inflated by security scanners; the only Apollo numbers treated as real are replies
   and meetings booked.
2. **Monday, system of record:** Sales Development Pipeline board 18409325257 holds each
   contact's sequence stage, synced by the SDR skill. Active bridge automations already exist:
   a reply creates an item on the Outreach Pipeline board 18407308519 and notifies Mary Anne;
   a booked meeting notifies her. Deals and revenue live on the Deals board. Cash is Stripe.
3. **Weekly rollup, Fridays:** voxmerch-exec-reporting pulls sends, replies, meetings, Pitch
   Kits accepted, deals open, and cash collected, alongside LinkedIn spend from Supermetrics.

Nothing sends until the full chain is verified with one test contact: enrollment, send, reply,
Monday status change, Deal created.

## Related skill edits still to make

- `voxmerch-sdr-contact-enrichment/SKILL.md`: point at the new sequence ID once created, enroll
  cold contacts active rather than paused, remove the manual-activation step, and replace the
  title lists with the account-lead titles above.
- Partner setup checklist: kiosk stands are required equipment. At Optum SCOPE, day one ran
  without stands and approaching attendees with an iPad in hand read as a survey ambush.
