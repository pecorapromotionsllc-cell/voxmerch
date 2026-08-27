# VoxMerch: Net New Activation Companies and Meeting Planners

## Context

VoxMerch is a SaaS platform startup, live since June 1, 2026, at zero net revenue. It licenses
AI voice-to-artwork event activation technology through channel partners. An attendee speaks
about 20 seconds, AI generates artwork unique to their voice, and it prints on merchandise
on-site. The brand gets first-party audience intelligence from what the room actually said.

**This plan covers one thing: acquiring net new event activation companies and meeting planners.**

**Explicitly out of scope.** The HALO AE pipeline is working and Mary Anne is running it herself.
Nothing in this plan touches it, depends on it, or asks anything of it. In particular, HALO AEs
will not introduce VoxMerch to agencies, because they would rather keep that business than hand
it to a competitor for the same client. Any plan built on AE referrals into the agency segment is
dead on arrival, and an earlier draft of this plan made exactly that mistake.

**What the founder asked for that earlier drafts got wrong:**
- Larger scale. The small stuff is not working. Cutting the target list was the wrong direction.
- Meeting planners added as a second buyer alongside experiential agencies.
- Prospecting and campaign execution built *for* her. She finds Apollo confusing and should not
  have to operate it.
- Alex Hormozi and Zig Ziglar as the sales frameworks, with an argument required if something
  else fits better.

**Timeline: three months, August through October, with first revenue targeted by Oct 1.**

Three months is the shortest honest evaluation window, because each stage has an irreducible
clock. Cold infrastructure needs 2 to 3 weeks of warmup before it sends at volume. A multi-touch
sequence takes about 3 weeks to run. A deal in this price band takes 30 to 90 days from first
meeting to signature. Month one builds, month two produces meetings, month three produces closes.
Judging the campaign at week four measures setup, not performance.

The Sept 4 target has moved to **Oct 1**, which converts 27 business days into roughly 45. That is
the difference between a sprint that cannot finish and a campaign that can.

**Constraints confirmed:**
- Execution is Mary Anne and Debra Sammon.
- Existing paid media: **$2,500/month already running**, split roughly $1,900 LinkedIn and $600
  Meta. Incremental campaign budget to be set (see budget section).
- **The $600/month Meta spend is close to wasted today.** Meta is configured as retargeting only,
  but the LinkedIn page has 29 followers and July produced 372 impressions and 20 clicks in total.
  There is effectively no audience to retarget. Reallocate it to a channel where planners are
  reachable cold. The $1,900 LinkedIn half is defensible and should be measured against its
  under-$150 CPL target before being changed.
- Cold sequences may send without per-email approval. Warm outreach never does.
- Optum is not cleared for cold outbound. Proof reads "a Fortune 500 healthcare company."
  A release from Brown & Brown for the Aug 11 GRIT activation is pending through the HALO rep.
- **Stripe is already wired into the client portal**, so payment collection is largely solved.
  Where procurement is required, it happens before a partner signs up for an event.
- **Agencies own their garment printing equipment.** Licensing-only is a real product. Where a
  partner lacks equipment, they can print art pieces on-site and offer Encore products as the
  client-facing upsell.

---

## Pricing: tier follows the event, not the buyer

The published prices are what the **partner resells at.** Partner cost is 40% below, and partner
cost is VoxMerch revenue:

| Tier | Activations | Partner resells at | Partner cost | **VoxMerch collects** | Partner margin |
|---|---|---|---|---|---|
| Essential | 150 | $3,500 | $2,100 | $2,100 | $1,400 |
| Plus | 300 | $7,000 | $4,200 | $4,200 | $2,800 |
| Advanced | 500 | $11,700 | $7,020 | $7,020 | $4,680 |
| Enterprise | 750 | $17,500 | $10,500 | **$10,500** | $7,000 |

Data insights reports and white-label attach as add-ons to any tier, so tier selection is driven
by activation volume alone.

**Two earlier errors in this plan, both corrected.** It treated resale price as VoxMerch revenue,
overstating every revenue figure by 40%. And it recommended "lead with Enterprise," which is
wrong: the tier has to match the event.

### What the product actually is

**The deliverable is a finished art piece the attendee takes home**, not a garment. Voice capture
runs **5 to 30 seconds** and artwork generates from it. Partners who want apparel can print it
on-site themselves if they choose, and Encore products are the client-facing upsell. This matters
for positioning: VoxMerch is not a garment decoration service, so a partner does not need apparel
equipment to run it, which widens the addressable partner base considerably.

### Throughput: the kiosk-day is the pricing unit

**Verified capacity is 150 activations per kiosk per 8-hour day**, roughly 19 per hour. That
figure is the operator's, not an estimate, and it maps exactly onto the tier structure:

| Tier | Activations | Kiosk-days | Example configurations |
|---|---|---|---|
| Essential | 150 | 1 | 1 kiosk, 1 day |
| Plus | 300 | 2 | 1 kiosk 2 days, or 2 kiosks 1 day |
| Advanced | 500 | 3.3 | 2 kiosks 2 days (600 capacity) |
| Enterprise | 750 | 5 | 2 kiosks 3 days, or 3 kiosks 2 days (900) |

Because partners supply their own equipment, **kiosk count scales with what the partner runs**, so
no tier is out of reach.

**The qualifying question that sets price, and it is the whole sales motion, in one sentence:**
how many days, and how many kiosks running each day? A two-day show with two kiosks is 600
capacity, which is Advanced. This is consultative needs analysis in the Ziglar tradition and it
upsells structurally rather than negotiating on price.

**Reality check on the proof point.** Optum SCOPE produced **198 activations across two days**
against a 300 capacity, so 66% utilization. Externally, state 198 activations and nothing more.
Internally the shortfall is instructive: day one had no kiosk stands, so the team approached
attendees holding an iPad, which reads as a survey ambush and triggers refusal. **Kiosk stands are
required equipment, not an accessory**, and that belongs in the partner setup checklist.

**Targeting consequence, and it is the biggest lever on revenue per deal.** Weight the campaign
toward **multi-day conferences and trade show booth activations**, while taking single-day
corporate meetings as they come. Same sales effort, three to five times the revenue per close.

---

## Diagnosis: why the current outbound produces nothing

| Finding | Evidence |
|---|---|
| **35 emails delivered, lifetime** | Event Activation sequence, against a 1,550/day limit. Under 2 sends/day. |
| Zero replies is arithmetically expected | 35 sends predicts well under one reply at any published benchmark. |
| Second sequence never ran | `active: false`, 0 sends since creation 2026-04-19. |
| Cold engine idle 10 weeks | Last send on board 18409325257 was 2026-05-18. |
| 67 contacts queued, never touched | Sitting in "Queued for Outreach." |
| **Two manual gates block every send** | The SDR skill enrolls every contact `paused` by design, and the sequence is set to `manual_approve`. |
| 7 weeks where sending was impossible | Sequences built 2026-04-19; mailbox connected 2026-06-08. |
| No revenue tracked anywhere | Revenue empty on all 209 records. Deals board has 0 items. Deal-creation automation switched off. |
| One mailbox only | Scaling it hard would burn the primary domain. |
| Three dead email channels | Joan Terrenzi (zero emails ever sent, Email 1 stuck in outbox 9 days), Caitlyn Brady and Matt Cicero both bouncing on verified addresses. |
| **The audience was wrong** | Company names with no person attached, international companies out of scope, and titles skewed to producers and CEOs rather than account leads. |
| **The sequence was misconstructed from the start** | Founder assessment, and it means no performance figure from it can be trusted. |

**Three separate failures, not one.** The campaign never ran (35 emails), it could not run
unattended (two approval gates requiring a founder who is busy closing to also be the send
button), and what little did run went to a list that was partly companies rather than people and
partly outside the target geography. Each would have been sufficient to produce zero on its own.

That is why the fix is not "work the tool harder." The gates come out, the sequence gets rebuilt
from scratch against a clean people-level US list, and Mary Anne comes out of execution entirely.

**Treat all prior Apollo performance data as void.** The reported 42.9% open and 25.7% click
cannot be trusted: the sequence was not built correctly, n is 35, there were 0 replies and 0
unsubscribes, and a high click rate with no replies is also the signature of link-scanning security
appliances. Apollo separately reports 15 lifetime opens against 1 in the last 30 days on the same
35 sends. There is no usable baseline here. Establish one on the rebuilt sequence with verified
tracking, and do not let anyone cite the old numbers as evidence the copy works.

---

## Positioning and segmentation, confirmed

**Meeting planners are a variant of the agency track**, not a third buyer with separate
calibration. They share the agency message with light adjustment. This roughly halves the
month-one asset build and keeps VoxMerch's "never blend audiences" doctrine intact, since the
underlying pain is genuinely shared.

**The core pain is two things at once, and the offer has to hit both:**
1. **The intelligence asset.** They cannot answer "what did we learn?" with photo counts and
   badge scans. VoxMerch produces a real read on what the room believes.
2. **Differentiating their pitch.** They lose bids because every agency and every planner
   proposes the same activations. VoxMerch is something no competitor is putting in the deck.

These combine into a single proposition that is stronger than either alone: *the activation no
competitor is proposing, which also answers the one question your client always asks and nobody
can answer.* Pain 2 wins the bid. Pain 1 wins the renewal. Lead with 2 for cold attention and
land on 1 for the close.

This is also why the category problem matters. VoxMerch's own paid media doctrine notes it is
"building a category that buyers do not yet know to search for." That is a positioning and
commercial-teaching problem, not a volume problem, which is why the framework recommendation
below layers a category-creation method on top of Hormozi and Ziglar.

### Sending readiness, corrected

The mailbox has been connected since 2026-06-08, giving roughly seven weeks of domain age with
**zero hard bounces, zero unsubscribes, and one soft bounce.** That is a clean foundation and it
means no cold-start ramp is required.

**Confirmed: Apollo's warmup has been running for weeks alongside those 35 real sends.** That is
the good case. Warmup traffic builds the sending reputation that 35 real emails could never build
on their own, so the constraint is now velocity discipline rather than reputation from zero.

**Ramp from here: roughly two weeks to full volume, not four to six.** About 25/day in week one,
40 in week two, 50 or more from week three. The one rule that still binds is avoiding a sudden
jump, because velocity spikes trigger classification independently of content or reputation.
Warmup traffic also counts against the per-mailbox ceiling, so confirm what Apollo is sending
automatically before setting the real-send cap.

---

## The framework: what to use and why

Mary Anne asked for Hormozi and Ziglar, and invited an argument for something better. The honest
answer is that both are right for parts of this and neither addresses the biggest problem.

**Zig Ziglar: keep it, it is already built.** `voxmerch-brain/references/sales-system.md` is
already a Ziglar system: needs-based questioning, feature-to-benefit translation, ethical use of
emotion through future pictures, objections as buying signals, and the three closes (Summary,
Question, Alternative Choice). It suits a relationship-led channel sale and it suits Mary Anne's
voice. The station-count conversation described above is textbook Ziglar needs analysis. No
change needed beyond fixing the three stale scripts listed later.

**Alex Hormozi: use the Value Equation for the offer and the Core Four for lead volume. Ignore
the rest.** His Value Equation is the right diagnostic tool here:

```
Value  =  (Dream Outcome  ×  Perceived Likelihood of Achievement)
          ────────────────────────────────────────────────────────
              (Time Delay  ×  Effort and Sacrifice)
```

Scoring VoxMerch honestly against a partner buyer:

| Variable | Current state | Verdict |
|---|---|---|
| Dream outcome | Win the bid with something no competitor has, then answer "what did we learn?" | **Strong.** Both stated pains. |
| Perceived likelihood | New company, one proof activation, client name not cleared, nothing the partner can show their own client | **Weak. This is the binding constraint.** |
| Time delay | Fast once running, but training and onboarding sit before the event | Moderate |
| Effort and sacrifice | Partner supplies equipment, crew, staffing, and carries on-site risk in front of their client | **High. Second binding constraint.** |

The two weak variables are the whole problem. **More outbound volume does not move either one.**
That is why the previous three weeks produced nothing that more sending alone would have fixed,
and it is why the offer section below spends its effort on raising perceived likelihood and
lowering partner effort rather than on writing better subject lines.

**Where Hormozi actively misleads here, and this matters.** His material is built on
direct-response, local service, and SMB high-velocity sales, where the buyer feels the pain and
pays the money. In a B2B2B channel sale those are two different people. "Make an offer so good
they feel stupid saying no" does not work on a reseller, because a reseller's yes is not gated on
their own desire. It is gated on two questions: *can I make margin* and *will this embarrass me
in front of my client.* An agency can love VoxMerch and still never buy, because their client
never approved it.

**The correct translation, and it is the single most important idea in this plan: construct the
offer for the partner's client, and deliver it through the partner.** VoxMerch's revenue rides
the partner's sales motion, so the highest-value thing VoxMerch can give a partner is not
technology. It is something that helps them **win the pitch.**

**Two additions Hormozi and Ziglar do not cover:**

- **April Dunford's positioning method**, because VoxMerch's own paid media doctrine states it is
  "building a category that buyers do not yet know to search for." Dunford's sequence (competitive
  alternatives, then unique attributes, then value, then who cares most, then market category) is
  the right tool. The critical insight it produces: **the competitive alternative is not another
  voice-AI vendor. It is badge scanning, photo booths, and branded giveaways.** That is what the
  budget currently buys and what VoxMerch displaces. Positioning against those, never against
  hypothetical AI competitors, is why the "swap the merch line item" framing works.
- **Challenger commercial teaching for the cold opener.** Cold outreach should lead with an
  insight about the reader's business, not a product. The teachable insight is already sitting in
  the proof data: post-event measurement is broken, badge scanning captures 15 to 20% of a room,
  and what the room believes is recoverable. Teach that, then reveal the mechanism.

**Recommended combination:** Dunford to name the category, Challenger to open cold, Hormozi's
Value Equation to build the offer, Ziglar to run the conversation and close. Each does a job the
others cannot.

---

## The offer: the Pitch Kit

This follows directly from the Value Equation diagnosis and from Hormozi's "give away the
secrets, sell the implementation" principle applied properly to a channel.

**The insight it is built on: an agency's or planner's actual job to be done is winning the
business, not running an activation.** They are judged on whether the client picks their proposal.
So the offer leads with the thing that helps them win, and the license is what they buy once they
have won.

**What the Pitch Kit is.** A client-ready activation proposal, built by VoxMerch for one specific
named opportunity the partner is currently bidding, at no cost:

- A branded proposal section they drop straight into their deck, carrying **their** logo
- Artwork mockups on merchandise using their prospective client's actual brand
- The intelligence-asset framing, with a sample post-event report showing exactly what the client
  receives
- Attendee-count and station math for that specific event, so pricing is already solved
- ROI framing against what the client currently spends on giveaways and badge scanning

**What VoxMerch asks in return: nothing until they win.** The partner pays when the client
approves and the event is booked. That is not a discount, it is a payment trigger aligned to how
agencies already operate, since they do not spend before a client commits.

**Why this works on every weak variable at once:**

| Value Equation variable | How the Pitch Kit moves it |
|---|---|
| Dream outcome | Reframed from "run a cool activation" to "win this specific bid" |
| Perceived likelihood | They see the finished proposal and mockups before risking anything |
| Time delay | Value arrives during their current bid, not after a future event |
| Effort and sacrifice | VoxMerch does the proposal work, which is the work they least want to do |

**It also functions as a qualifying mechanism.** Only a partner with a live, dated opportunity
will accept, because the kit requires them to name the client and the event. Everyone who says
yes is by definition in-market, which is the opposite of what a cold list gives you.

**Guarantees, in Hormozi's taxonomy. Only guarantee what VoxMerch controls.**

1. *Implied, structural:* no cost until the client approves the activation. Risk is zero by
   construction, and this is the strongest of the three because it needs no policing.
2. *Capacity and deliverables guarantee, replacing an earlier bad idea.* An earlier draft proposed
   guaranteeing an opt-in rate. **That is unworkable and has been cut.** Attendance is outside
   VoxMerch's control: a client expecting 3,000 who gets 1,500 because of weather has fewer
   activations for reasons no one can attribute, and there is no way to measure the denominator.
   Guarantee the things VoxMerch owns instead:
   - **Capacity:** 150 activations per kiosk per 8-hour day, or the shortfall is credited.
   - **Function:** if the platform fails to generate and print artwork during the event, the
     license fee is refunded.
   - **Report SLA:** the intelligence report delivered within a stated number of business days.
   These are checkable, defensible, and entirely within VoxMerch's control.
3. *Effort reversal on the first event, gated.* VoxMerch co-staffs the partner's first activation
   at no additional fee. This is the largest trust lever available and it directly answers the fear
   that actually blocks these deals, which is something failing on-site in front of their client.
   **But it costs founder travel and cannot be offered universally.** Restrict it to **Advanced and
   Enterprise tiers with partners of real scale.** Offering it to a small planner with one client
   and little revenue is unaffordable and sets a precedent that cannot be honored at volume.
   Gating it also creates a concrete reason to move up a tier, which is a feature rather than a
   compromise.

**Honest scarcity, no manufactured urgency.** Onboarding a first-time partner takes real founder
hours, so capacity is genuinely finite. "I can take four new partners onto the Q4 delivery
calendar" is true, checkable, and creates a real deadline. Event dates supply the rest. Never
invent a discount deadline.

**The Encore upsell** sits naturally here: a partner without printing equipment can still run the
art-piece activation and offer Encore products to their client, which widens the addressable
partner base beyond those who own decoration equipment.

---

## Segments and how to reach them at scale

Meeting planners are an agency-track variant, so one message with light adjustment serves both.
But they are not one market, and one distinction decides whether a planner is viable at all.

**The resale test.** VoxMerch's model requires the partner to buy at cost and resell at a markup.
Sub-segments differ sharply on whether they can:

| Sub-segment | Can they resell at markup? | Priority |
|---|---|---|
| Experiential and activation agencies | Yes, standard practice, 20 to 40% | **Primary** |
| Independent and third-party planners | Usually yes, via markup or commission | **Primary** |
| DMCs and production companies | Yes, they mark up subcontracted vendors | **Primary** |
| Exhibit houses and booth builders | Yes | **Primary** |
| Corporate in-house event teams | **No.** They buy direct, they do not resell | Route to a partner |
| Association meeting planners | Mixed, often buy direct on behalf of the association | Qualify case by case |

**This is a qualifying question that belongs in the first 60 seconds of every conversation**, and
it is currently missing from the ICP definitions in
`voxmerch-sdr-contact-enrichment/SKILL.md`. Corporate in-house planners are not bad leads, but
they are *end clients*, and per VoxMerch's direct-brand routing protocol they must be routed
through a partner rather than sold directly.

**Where the volume actually is.** The experiential agency universe is small, in the low hundreds,
anchored by Event Marketer's 2026 It List of the top 100 plus mid-size regional shops. The
planner universe is far larger, in the tens of thousands, reachable through MPI, PCMA, IAEE, ILEA,
NACE, SITE and the CMP certificant population. **Adding planners is what makes "larger scale"
arithmetically possible**, since no amount of budget produces thousands of qualified experiential
agencies. They do not exist.

**Target bias, per the confirmed decision:** both segments, weighted toward multi-day conferences
and trade show booth activations, because those are Advanced and Enterprise deals at three to five
times the revenue of a single-day event.

**Route to the account lead, not the producer.** The account director or account lead owns budget
and the client relationship and has an incentive to bring a client something new. A producer's job
is preventing on-site problems, so new scope inside a sold program draws a reflexive no. Bring the
producer in second, holding an operations answer sheet rather than a pitch. The current ICP title
list leads with President, CEO and Director of Activations and needs editing.

**Job-posting signal monitoring: tested and cut on 2026-08-01. Do not rebuild.** An earlier version
of this plan called event staffing job postings the highest-fidelity targeting signal, on the theory
that an agency hiring twelve brand ambassadors in Orlando for December 6 to 9 has a booked, budgeted,
dated program. Two live Apify pulls disproved the premise:

- **Discovery by job title:** 50 US event-staffing postings from the last 7 days at agency-sized
  companies yielded **exactly one** real target. The rest were CPG brands running their own in-store
  sampling, home-improvement companies staffing mall kiosks (one accounted for 17 of the 50), caterers,
  venues, a law firm, and a job board. A 2% hit rate.
- **Monitoring our own target list:** across 30 named target companies over six months, roughly five
  postings carried any event-activity signal, and **not one named a city and a date for a specific
  event.** They were full-time hires at the agency's home office, which indicates the agency is busy,
  not that a program is booked. Separately, fuzzy company-name matching produced about 58% false
  positives ("Bluewater" matched a school board, an oil and gas contractor, and a federal IT firm).
  That part is fixable with exact LinkedIn company IDs; the weak underlying signal is not.

Event agencies largely do not post per-event staffing publicly. They use their own bench, staffing
partners, or word of mouth. Cost of learning this: about twenty cents.

**Trade show exhibitor lists: also cut, for a structural reason.** Exhibitors are brands, and VoxMerch
does not sell to brands. Turning an exhibitor list into a prospect requires knowing which agency built
each booth, which is not public and does not scrape. More decisively, a brand-side list only becomes
useful once there are signed partners to hand it to, and there are currently zero. Revisit only if
partners exist and want target lists as ammunition, which is a month-2-or-later question at the earliest.

---

## Campaign architecture: what runs without Mary Anne

The governing rule, and the fix for the actual root cause: **Mary Anne is removed from execution
entirely. She takes qualified conversations and she closes. She is never the send button.**

| Function | Who or what does it | Mary Anne's involvement |
|---|---|---|
| List building, agencies and planners | ZoomInfo plus association directories, built once per month | None |
| Cold email sequences | Apollo, rebuilt from scratch, auto-send | None |
| LinkedIn outreach | Manual, from her own profile, capped at 100 requests/week | 20 minutes/day |
| Dial queue and qualification | Debra, ranked daily list from Monday | None |
| Pitch Kit production | Built to a repeatable template on request | Approves before send |
| Warm and named-account email | Outlook | Approves every message |
| Call recording to CRM | Granola or Zoom into `sales-call-analyzer` into Monday | None |
| Inbox to CRM sync | `crm-updater` skill, already built | None |
| Paid media | LinkedIn Thought Leader Ads from her profile | Records the video or post |
| Reporting | Supermetrics plus `voxmerch-exec-reporting`, weekly | Reads it |

### Apollo: rebuild the sequence from scratch

**Both sequences are now off and the Event Activation sequence is being scrapped deliberately.**
That is the right call, and it supersedes an earlier recommendation in this plan to simply remove
the approval gates. There is nothing worth salvaging, for reasons the founder identified directly:

- The audience pulled **company names with no person attached.** Nine `[PROSPECT]` company-level
  placeholders sat mixed in with real contacts.
- It pulled **international companies**, which are out of scope for now.
- **The sequence was not constructed correctly from the beginning**, which means the reported
  42.9% open and 25.7% click figures cannot be trusted and should not be used as evidence of
  anything. Treat all prior Apollo performance data as void rather than as a baseline.

**Distributor outreach outside HALO is deferred to January 1.** The Promo Distributors sequence
stays off. Only one sequence gets built now, for event activation companies and meeting planners.

**Build specification for the new sequence:**
- People-level contacts only. Never enroll a company placeholder.
- `person_locations: ["United States"]` enforced without exception.
- Titles targeting the **account lead or account director**, not producers, and not President or
  CEO as the lead title.
- Verified email required before enrollment. No unverified sends.
- Planner sub-segments filtered to those that **can resell at a markup**. Corporate in-house
  planners are end clients and route to a partner instead.
- Configured to **auto-send from day one.** No `manual_approve`, and no `paused` enrollment. Edit
  `voxmerch-sdr-contact-enrichment/SKILL.md` to remove both, and delete the "Mary Anne must
  manually activate" step.
- Clean tracking verified before the first send, so the data means something this time.
- Maximum 3 emails in the cadence. Phone and LinkedIn carry the remaining touches.

**On tool choice.** After these changes Mary Anne does not operate Apollo at all; the skill runs
enrichment, enrollment and Monday sync on a schedule. If it stays painful once the sequence is
rebuilt cleanly, the simpler replacements are Instantly or Smartlead, which handle inbox rotation
and warmup automatically. Treat that as a month-two decision, because switching now would forfeit
the domain age and warmup already banked.

---

## Budget: three months, August through October

Existing spend is $2,500/month, roughly $1,900 LinkedIn and $600 Meta. Recommended reallocation
and incremental spend, per month:

| Line | Monthly | Notes |
|---|---|---|
| LinkedIn Thought Leader Ads | $1,900 | Keep. Her 1,500+ followers make this the strongest channel. Measure against the under-$150 CPL target. |
| Meta | **$0** | Pause. Retargeting with no audience to retarget. Redeploy the $600. |
| Contact data, agencies and planners | $600 to $1,000 | Verified emails plus mobile direct dials. Connect rate roughly doubles on verified mobiles. |
| Trade publication newsletter placement | $1,000 to $2,500 | **Needs real quotes.** Meetings-industry press likely reaches more qualified buyers per dollar than cold email. Request rate cards from BizBash, Smart Meetings, MeetingsNet, Northstar, Skift Meetings, Event Marketer. |
| Sending infrastructure and tooling | $200 to $400 | Additional mailboxes, warmup, sequence tool. |
| **Total monthly** | **$3,700 to $5,800** | Against $2,500 already committed, incremental is roughly $1,200 to $3,300/month. |
| **Three-month total** | **$11,100 to $17,400** | Incremental over existing: roughly $3,600 to $9,900. |

**Optional, only if the founder-led motion proves it converts first:** a done-for-you outbound
provider or fractional SDR, roughly $3,000 to $8,000/month on retainer, or $300 to $1,000 per
qualified meeting on pay-per-meeting terms. *These are approximate market rates and need direct
quotes.* **Do not buy this in month one.** Outsourced SDRs fail predictably when the offer and
messaging are unproven, because they cannot iterate on either. Prove the Pitch Kit converts with
Debra dialing first, then buy volume against a known conversion rate in month two or three.

**Anti-recommendation: skip AI SDR products for now.** The category is real but immature, and
paying for autonomous prospecting before the offer is validated repeats the current failure with
more automation on top.

---

## Month by month

**Month 1, August: build the offer and prove it converts.**
Week 1 (Jul 29 to 31, three business days): re-authorize the Apollo connector and **rebuild the
event activation and planner sequence from scratch** to the build specification above. Build the
first three Pitch Kits by hand for the warmest named opportunities. Deb requests trade publication
rate cards on her return.
Weeks 2 to 4: Pitch Kit offer goes out to the 58 existing agency contacts and the 8 records
already scored 70 to 95 and sitting idle. Debra begins dialing. Build the planner list. Ramp
sending 10, 20, 35 per day across the three weeks. GRIT runs Aug 11: capture footage against a
shot list, chase the Brown & Brown release before the event, and ask about their next event on
site. Build the agency and planner one-pager, which does not exist. Fix the three stale objection
scripts.
**Month 1 success test: at least 5 Pitch Kits accepted.** Not closes. Acceptances. If partners
will not accept a free client-ready proposal, the offer is wrong and no amount of scale fixes it.

**Month 2, September: scale what converted.**
Sending at 50/day. Planner segment enters the sequence. Trade publication placement runs.
Pitch Kit production moves to a template so it takes an hour, not a day. First closes expected here,
since month-1 conversations reach the 30 to 90 day close window. Decide on outsourced SDR based on
month-1 conversion data.

**Month 3, October: harvest and compound.**
Q4 events are being finalized, so this is peak buying season for November and December
activations. Close month-1 and month-2 pipeline. GRIT and any new activations become named case
studies. IMEX America (Oct 13 to 15, Las Vegas) is the largest meeting-planner gathering in the
window and registration is free for qualified industry professionals, so it is worth attending
even without a booth.

---

## Verification

**Primary metric: cash collected, then signed partners with a dated activation.** Both read from
Monday. Revenue is currently empty on all 209 records and the Deals board has 0 items, so week 1
turns tracking on and opens a Deal per qualified conversation.

| Metric | Aug | Sep | Oct |
|---|---|---|---|
| Pitch Kits accepted | 5 | 12 | 20 |
| Qualified conversations | 8 | 20 | 30 |
| Signed partners with a dated event | 0 to 1 | 1 to 3 | 3 to 6 |
| Cash collected | $0 to $2K | $4K to $15K | $15K to $45K |

**Diagnostic rules, so a miss tells you where to look:**
- Pitch Kits accepted below 5 in August means **the offer is wrong.** Stop scaling and rebuild it.
- Kits accepted but conversations not converting means **the price or the tier fit is wrong.**
- Conversations converting but nothing closing means **the client-side approval is the blocker**,
  and the Pitch Kit needs to speak past the partner to their client.
- Everything working but volume too low means **and only means** scale spend.

**Honest expectation.** Three to six signed partners with dated activations by Oct 31, most in
Advanced or Plus, producing roughly $15,000 to $45,000 collected. The Pitch Kit is the mechanism
most likely to break the current zero, because it removes partner risk entirely and attaches to a
bid they are already working.

**What I will not claim.** I cannot be 99% certain of a specific count by a specific date, and
saying otherwise would be the least useful thing in this document. What I am confident of is the
causal chain: the current campaign produced nothing because 35 emails went out, and because the
offer asks a risk-averse reseller to carry cost and on-site risk to sell an unproven category to
their own client. This plan fixes the volume problem and the offer problem separately, and the
month-1 test tells you within four weeks whether the offer works before you spend to scale it.

---

## Open items

| # | Item | Status |
|---|---|---|
| 1 | **Trade publication rate cards** from BizBash, Smart Meetings, MeetingsNet, Northstar, Skift Meetings, Event Marketer. Potentially the highest-yield planner channel and currently unpriced. | **Deb owns, when back from vacation.** |
| 2 | Warmup tool status | **Resolved.** Apollo warmup running for weeks. Ramp compresses to ~2 weeks. |
| 3 | **Brown & Brown release** for GRIT, through the HALO rep. Determines whether Q4 selling uses a named, dated case study or an anonymized one. | **Pending.** Chase before Aug 11. |
| 4 | Apollo's conflicting open and click data | **Resolved by decision.** The sequence was not built correctly from the start, so all prior performance data is void. Do not use it as a baseline. Clean tracking gets verified on the rebuilt sequence before the first send. |
| 5 | **Association list purchase** for MPI, PCMA, IAEE and similar. Cheapest route to planner scale if licensing permits. | **Being investigated.** Confirm licensing terms allow outreach use, not just membership access. |

---

## Corrections log

Recorded because several of these were my errors and the reasoning matters if the plan gets
revisited.

| Was | Corrected to |
|---|---|
| Revenue figured at the published tier price | Published price is partner resale. VoxMerch collects 60% of it. Every earlier revenue figure was 40% too high. |
| "Lead with Enterprise" | Tier follows the event. Kiosk-days set the price. |
| 20 to 30 activations per hour per station, from a print-and-press estimate | 150 per kiosk per 8-hour day, roughly 19 per hour. Verified by the operator. |
| Finished garments printed on-site | Finished **art pieces.** Apparel is optional and partner-run. Encore is the client upsell. |
| Voice capture "about 20 seconds" | **5 to 30 seconds.** |
| Optum: 198 recordings across three days | **198 activations across two days.** State only the number externally. |
| Guarantee an opt-in rate | Unworkable, attendance is uncontrollable. Guarantee capacity, function, and report SLA instead. |
| Co-staff every partner's first event | Gate to Advanced and Enterprise with partners of real scale. Unaffordable otherwise. |
| Remove the Apollo approval gates | Sequence scrapped entirely and rebuilt from scratch with a clean people-level, US-only audience. |
| HALO AEs as an introduction source into agencies | Dead. AEs keep that business rather than hand it to a competitor for the same client. |
| Distributor outreach in scope | Deferred to January 1. HALO covers the segment until then. |
| Job postings as the highest-fidelity targeting signal, worked daily via Apify | **Cut 2026-08-01 after live testing.** 2% hit rate on title-based discovery; monitoring our own target list produced ~5 weak signals across 30 companies over 6 months and not one named a city and a date. Agencies do not post per-event staffing publicly. Do not rebuild. |
| Q4 trade show exhibitor lists as a prospect source | **Cut 2026-08-01.** Exhibitors are brands and VoxMerch does not sell to brands. Brand-to-agency attribution is not public and does not scrape, and a brand-side list is worthless until signed partners exist to receive it. |
| Voice capture "5 to 30 seconds" with artwork following | Externally: attendees speak **up to 30 seconds** and the artwork appears **40 seconds later**. Use this phrasing in all copy. |
