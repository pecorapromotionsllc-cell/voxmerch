# Which status means what, who changes it, and when

Written 2026-08-05, because there was no answer to that question anywhere and the columns had no
descriptions in Monday.

Two boards carry status columns and they do different jobs. **Sequence Stage** on the cold board
tracks a machine sending email. **Status** on the warm board tracks a human having a conversation.
A contact normally has one or the other, not both, because replying or booking moves them from the
first board to the second.

**Three status values do something visible when set. Read that section before touching a chip.**

---

## Board 18409325257, Sales Development Pipeline (cold outbound)

The cold engine. People here are being emailed by Apollo and nobody has spoken to them.

### Sequence Stage (`color_mm2jstfm`)

Where a contact sits in the 3-touch Apollo sequence `6a6ab19632f101001070b98d`.

| Value | Means | Set when |
|---|---|---|
| Queued | In Apollo, not yet emailed | Contact created, or enrolled but email 1 has not gone out |
| Touch 1 Sent | Email 1 delivered, waiting on email 2 | Apollo advances the contact to step 2 |
| Touch 2 Sent | Email 2 delivered, waiting on email 3 | Apollo advances to step 3 |
| Touch 3 Sent | All three emails sent, no reply | Apollo marks the contact finished |
| Replied | The prospect wrote back | Apollo marks the contact replied |
| Bounced | The address failed | Apollo marks the contact `bounced` or `failed`, or finishes them with `inactive_reason` of bounced or spam_blocked |
| Not Interested | Explicit no | By hand, from reading the reply |
| Meeting Booked | A meeting is on the calendar | By hand, or from a booking |

**Who writes it.** The `Apollo to Monday Sequence Stage Sync` routine, weekday mornings, reading
each contact's real state out of Apollo. Before 2026-08-05 nothing wrote it past Queued and every
value was typed in during a chat session. That is why the board understated progress by 13 contacts
on the day the sync was built. Do not hand-edit this column; the sync will overwrite it on the next
run, and a hand-set `Replied` fires a real automation.

**`finished` does not mean the cadence completed.** Apollo sets `finished` both when all three
touches have gone out and when the sequence was cut short by a reply, recording which in
`inactive_reason`. Read plainly it would have overwritten Michael Junne's `Replied` with
`Touch 3 Sent` and erased the only reply the campaign has produced. The reconciler reads
`inactive_reason` first, and treats `Replied`, `Meeting Booked`, `Not Interested` and `Bounced` as
sticky: once the board carries one, nothing downgrades it back onto the touch ladder.

**`failed` is a real Apollo status and it is not in their documented list.** It appeared on
2026-08-05 on a contact whose send produced a soft bounce and a spam block. The reconciler treats it
as terminal and maps it to `Bounced`. Any other unrecognised status leaves the stage untouched and
escalates rather than guessing, because a wrong guess here can make a dead address look like a
healthy in-sequence contact.

**Cadence timing**, so the dates make sense: email 1 goes 30 minutes after enrollment, email 2 three
days later, email 3 four days after that. Apollo caps step 1 at 25 sends per day.

### Segment (`color_mm2j3sjs`)

Which ICP the contact belongs to: `Event Activation` or `Promo Distributor`. Set once at creation,
never changes. Note the singular form; the Apollo list name is plural and the board label is not.

### Groups on this board

Groups restate the stage, so the sync keeps them aligned rather than leaving them to drift:

| Group | Holds |
|---|---|
| Queued for Outreach | Stage Queued |
| In Sequence | Touch 1 Sent, Touch 2 Sent |
| Sequence Complete | Touch 3 Sent |
| Replied | Stage Replied |
| Not Interested / Bounced | Bounced, Not Interested |
| Meeting Booked | Emptied by automation, which moves the item to the warm board |

**Four groups are off limits and the sync will never move anyone out of them.** Archive - Company
Placeholders, Deferred - Distributors (Jan 1), Do Not Enroll - Prior Sequence (Call Only), and Out of
Scope - Non-US. The third one matters most: those 31 people already received the deprecated sequence,
and a fresh cold intro to them or a colleague is the mistake that damages a target account.

---

## Board 18407308519, Outreach Pipeline (warm)

Real relationships. People here have replied, been introduced, booked something, or come inbound.

### Status (`color_mm24v105`) — the main one

The human sales conversation. Nineteen labels, roughly in order:

| Stage of life | Labels |
|---|---|
| Not worked yet | New, Not Started |
| Working it | In Progress, LinkedIn Sent, Touch 2, Awaiting Feedback, Nurturing - No Response |
| In a sales process | Discovery, Demo Scheduled, No Show, Demo Attended, Demoed, Proposal Sent, Negotiation |
| Landed | Client Named, Event Booked, Event Ended |
| Dead for now | Closed - Not Now |

**Who writes it.** Mary Anne by hand, and the `crm-updater` skill after logging any interaction from
the inbox or a call transcript. There is no automatic progression, so this column is only as current
as the last conversation someone logged.

**Two labels do something when you set them:**

- **Demo Attended**, on a contact whose Segment is `HALO AE`, **sends that person an email** from
  maryanne@voxmerch.com. Subject "Thank you + everything I promised - VoxMerch", carrying the deck
  link and the try-VoxMerch link. This is a live send, not bookkeeping. Setting it on the wrong row
  emails the wrong person.
- **Event Booked** moves the item into the Event Booked group.

**Duplicate labels, resolved 2026-08-05.** Two pairs meant the same thing: New against Not Started,
and Demoed against Demo Attended. Both of the redundant halves turned out to be used by **zero** of
the 120 items on the board, so retiring them rewrites no history.

`Demo Attended` is the survivor of its pair. It already held 50-plus items and it is the label the
thank-you email hangs off. The open-a-Deal notification, which used to sit on the unused `Demoed`
label and therefore could never have fired, was rebuilt on `Demo Attended` (automation 7921570239).
The old one is switched off rather than deleted, because this API token can create and deactivate
automations but not delete them.

`New` is the survivor of its pair. A saved board view already filters on it.

**`Not Started` and `Demoed` still exist as options and have to be deleted in the Monday UI.** The
API cannot do it: `change_column_metadata` accepts only `title` and `description`, so status labels
are not editable programmatically at all. Open the Status column settings, remove those two labels,
save. Nothing moves, because nothing uses them.

**Still open:** the `crm-updater` skill is told to write "Closed Won", which is not a label on this
column and will fail when it tries.

### Outreach Stage (`color_mm5dhte2`)

The LinkedIn and email outbound queue, separate from the sales conversation above. Ready to Send is a
drafted touch waiting on Mary Anne. In Cadence means sent and running. Replied stops the cadence.
Cadence Complete means the 21-day sequence is exhausted. Managed by the daily prospector. No
automations hang off it.

### Activation Status (`color_mm4a6byb`)

Whether a HALO AE has been through the product themselves: `Notebook Received` or `Not Activated`.
Drives the two-track follow-up. One automation reads it, and that automation is currently off.

### Segment (`color_mm2tryes`) and Source (`color_mm2tsj69`)

Segment is the cohort: HALO AE, Promo Distributor, Event Activation, Brand. It gates the Demo
Attended email, so it is not decorative. Source records how they arrived, including
`Cold Sequence Reply` and `Cold Meeting Booked` for people the cold board promoted.

---

## How a cold contact crosses over

**The sync does this now, not a board automation.** Automation 7919396835 was built to create the
warm item when Sequence Stage becomes `Replied`, and it never fired once. Michael Junne's stage read
`Replied` from 10 to 13 August with no warm item and no notification. The likely reason is that a
"when status changes" trigger does not respond to a column change made through the API, only to one
made in the UI. The automation is left switched on; the sync's duplicate check means a late firing
costs nothing.

1. Sequence Stage becomes **Replied**. The weekday sync creates an item on the Outreach Pipeline in
   Event Activation Companies, at Status `New`, Source `Cold Sequence Reply`, carrying company, role,
   email and a note pointing back at the cold item. The cold item stays put and moves to the Replied
   group, so check for a duplicate before working it.
2. Sequence Stage becomes **Meeting Booked**. Automation 7918236607 moves the item onto Outreach
   Pipeline in the Event Booked group, carrying company, title, email, phone, notes, Apollo ID,
   segment and revenue. Automation 7919397410 notifies her separately.

Both depend entirely on Sequence Stage being written. That is the whole reason the sync exists.

---

## Automations, current state

### On 18409325257

| Trigger | Action | On |
|---|---|---|
| Sequence Stage becomes Meeting Booked | Move item to Outreach Pipeline, Event Booked group | Yes |
| Sequence Stage becomes Replied | Create item on Outreach Pipeline, notify Mary Anne | Yes |
| Sequence Stage becomes Meeting Booked | Notify Mary Anne | Yes |
| Sequence Stage becomes Meeting Booked | Create item and notify | No, correctly off, the mover already does it |
| Item created | Extract first name into First Name | Yes |

### On 18407308519

| Trigger | Action | On |
|---|---|---|
| Status becomes Demo Attended, Segment is HALO AE | **Send the thank-you email from Outlook** | Yes |
| Status becomes Demo Attended | Notify Mary Anne, "Demo attended - open a Deal" (7921570239) | Yes |
| Status becomes Event Booked | Move item to Event Booked group | Yes |
| Due Date arrives, 10:30 CT | Notify Mary Anne | Yes |
| Due Date minus 1 day, 13:45 CT | Notify Deb | Yes |
| Incoming and outgoing Outlook mail | Log onto the item | Yes |
| Status becomes Demoed | Notify "open a Deal" (7919397478) | No, superseded by 7921570239 |
| Due Date 9:00 CT with Activation Status check | Notify | No |

So a HALO AE moving to `Demo Attended` now does two things at once: they get the thank-you email, and
Mary Anne gets prompted to open a Deal. The missing Deal prompt was part of why the Deals board sits
empty.

One cosmetic flaw in 7921570239: the notification body reads "Check out {item name}" because the
automation builder overwrote the message text on creation. The **title** carries the instruction, so
it is still actionable. Editing the body is a UI change if it grates.
