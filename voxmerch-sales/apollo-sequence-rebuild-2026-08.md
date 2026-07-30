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

## Email copy (APPROVED by Mary Anne 2026-07-30, loaded into Apollo)

This is the live copy, verified against Apollo's stored templates. Mechanism facts corrected by
the founder: attendees speak for **up to 30 seconds**, and **40 seconds later** the
characteristics of their voice have become the artwork. Never write "about 20 seconds" or
"30 seconds later." Voice pass applied per mary-anne-voice: peer stance, reader's world first,
"Make it a great day!" close with the Outlook signature appending the name block after it.

### Email 1, day 0. Subject: `what the room believes`

> Hi {{first_name}},
>
> After every event, you can tell your client how many people stopped by. What you usually can't
> tell them is what those people actually think about the problem their brand is trying to solve.
>
> That second answer is what I built VoxMerch to deliver. An attendee steps up to the mic and
> talks for up to 30 seconds about a question your client cares about. Forty seconds later, the
> characteristics of their voice have become a one-of-a-kind piece of artwork they take home, and
> your client walks away with a real read on what the room believes. At a recent event for a
> Fortune 500 healthcare company, 89% of attendees said yes to it.
>
> Do you have 15 minutes on Tuesday or Wednesday? I would love to show you how it works live.
>
> Make it a great day!

### Email 2, day 3. Subject: `your next pitch`

> Hi {{first_name}},
>
> A different thought from my last note. If you have an event pitch on your desk right now, I
> will build the activation piece of it for you at no cost: artwork mockups on your client's
> brand, a sample of the report they would get back, and pricing already worked out, all under
> your name.
>
> If your client passes, it cost you nothing. If they book it, we run it together.
>
> Which pitch should we build it around?
>
> Make it a great day!

### Email 3, day 7. Subject: `the polite booth answer`

> Hi {{first_name}},
>
> Last note from me. One observation before I go, from the show floor.
>
> When attendees talk into a mic and watch their own words become artwork, they stop giving the
> polite booth answer. They say what they really think about the problem the brand exists to
> solve, and the brand gets to keep that. It is the difference between telling your client how
> many people came by and telling them what the room believes.
>
> If that is something the brands you work with would want, reply and I will set up 15 minutes
> to show you how it runs. And if the timing is off, I will check back in the new year.
>
> Make it a great day!

Email 3 was rewritten off the 198-activations case study because it duplicated email 1's proof.
The arc: email 1 is the idea with the proof, email 2 is the Pitch Kit offer, email 3 is the
observation that explains why it works.

### Operational note from this build, recorded so it is never repeated

Apollo normalizes plus-aliases when deduplicating: creating a "test contact" at
maryanne+seqtest@voxmerch.com matched and overwrote Mary Anne's own contact record (restored
immediately). There is no safe way to fabricate an internal test contact on the founder's own
address. The tracking test enrolls her real contact record instead, and her reply finishes her
out of the sequence via mark_finished_if_reply.

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
