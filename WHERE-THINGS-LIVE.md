# Where things live

Written 2026-07-31. The short version: **the automation does not depend on a file store at all.**
Operational data lives in Apollo and Monday, both reached over APIs. Files are documentation and
deliverables, not the machine. So the storage question is real but lower-stakes than it looks.

**Nothing is on OneDrive.** Everything created for the outbound rebuild went to this GitHub repo.

## Systems of record, by kind of data

| What | Lives in | Why there |
|---|---|---|
| Contacts, sequences, email sending, enrollment | **Apollo** | It owns verified emails and the send engine. Never mirror contacts into a spreadsheet; a stale copy is worse than no copy. |
| Pipeline, contact stage, deals, revenue | **Monday** | The revenue system of record. Boards 18409325257 (Sales Development), 18407308519 (Outreach), 18393236419 (Deals). |
| Sent and received mail, out-of-office replies | **Outlook / Microsoft 365** | maryanne@voxmerch.com is an Exchange mailbox. This is not something to move, and it is the reason a Microsoft tenant exists at all. |
| Payments | **Stripe** | Already wired into the client portal. |
| Plans, specs, audience lists, dashboard source | **GitHub** (this repo) | Versioned, diffable, readable by automation. |
| Client-facing and binary assets | **Dropbox** | Artwork mockups, Pitch Kit PDFs, event photo and video, sample reports. |
| The live dashboard | **claude.ai artifact** | Private URL, source HTML versioned here so it is reproducible. |

## GitHub or Dropbox

Not a choice. They do different jobs, and using both is the correct answer rather than a compromise.

**GitHub for anything text, versioned, or read by automation.** The plan, this file, sequence
specs, audience tranches, skill definitions, the dashboard HTML. The reason is version history:
every decision in the rebuild is committed with the reasoning attached, including the corrections.
That record is the institutional memory of why the campaign is built the way it is, and it is worth
more than the files themselves.

**Dropbox for anything binary or client-facing.** Nobody at an experiential agency is going to
clone a repo to look at artwork mockups. Git handles large binaries badly and non-developers worse.
Dropbox gives shareable links and opens for Debra, Christie, and Anna without anyone learning git.

**Rule of thumb:** if a partner or teammate should be able to open it from a link, Dropbox. If its
history matters, GitHub.

## What would actually impede automation

Storage choice barely touches it. These would:

1. **Putting operational data in files.** A contact list in a Dropbox spreadsheet cannot send email,
   cannot dedupe, and goes stale the day it is written. Contacts belong in Apollo, stage belongs in
   Monday.
2. **Storing something only where there is no API.** Both GitHub and Dropbox are reachable
   programmatically here, so neither is a dead end. A local desktop folder would be.
3. **Relying on this container.** Sessions run in an ephemeral cloud container that gets reclaimed
   after inactivity, and the repo is cloned fresh each time. That is why work is committed and
   pushed after every step rather than at the end. Anything uncommitted dies with the container.

## One thing worth fixing

The connected Dropbox is a team account under **maryannekeane@gmail.com**, a personal address,
not maryanne@voxmerch.com. That is fine today and a problem later: business assets on a personal
account complicate bringing on staff, granting access, and any future diligence. Worth moving to a
company-domain Dropbox before it fills up with client work.
