# Originals to delete (review before removing anything)

Everything listed below was copied into the new `C:\Users\marya\Projects\VoxMerch\` structure. The originals still exist at their old locations. This file groups them into safety tiers so you can approve deletion tier-by-tier instead of all at once.

---

## Tier 1 — Safe to delete (pure duplicates or junk)

These are exact duplicates of what's now in the new structure, or leftover junk from prior editing sessions.

| Original | New home | Notes |
|---|---|---|
| `C:\Users\marya\OneDrive\Documents\Claude\Projects\VoxMerch\Vox Merch Launch Action Plan - April to June 2026.docx` | `voxmerch-launch-ops\Vox Merch Launch Action Plan - April to June 2026.docx` | 60 KB, Apr 5 version, copied verbatim. |
| `C:\Users\marya\OneDrive\Documents\Claude\Projects\VoxMerch\VoxMerch Launch Action Plan - April to June 2026.docx` | NOT copied | 53 KB, Apr 4 older draft. Per your "Yes, proceed with this mapping" answer, this was skipped. Delete. |
| `C:\Users\marya\OneDrive\Documents\Claude\Projects\VoxMerch\event-activations-are-having-a-moment-blog.md` | `voxmerch-content\event-activations-are-having-a-moment-blog.md` | Copied. |
| `C:\Users\marya\OneDrive\Documents\Claude\Projects\VoxMerch\unpacked\` | NOT copied | Extracted docx XML. Pure junk. |
| `C:\Users\marya\OneDrive\Documents\VoxMerch_Licensed_Client_SOP.docx` | `voxmerch-sales\VoxMerch_Licensed_Client_SOP.docx` | Was sitting loose at Documents root. Copied. |
| `C:\Users\marya\HALO Keane Dropbox\VoxMerch\AI\marketingskills-main (1)\` | NOT copied | Duplicate of `marketingskills-main`. |
| `C:\Users\marya\HALO Keane Dropbox\VoxMerch\AI\marketingskills-main (1).zip` | NOT copied | Same. |
| `C:\Users\marya\HALO Keane Dropbox\VoxMerch\AI\*.zip` (agent-skills-main, business-coach, claude-seo-main, marketingskills-main) | Extracted folders copied | The zips are redundant once the extracted versions are in the repo. |

---

## Tier 2 — Probably safe, but confirm first (the old VoxMerch OneDrive folder)

The entire old VoxMerch project folder becomes redundant once the new location is adopted. Before deleting, confirm that:

1. No other tool (Claude Code desktop shortcut, scheduled task, or launcher) still points at the OneDrive path.
2. You have Git-initialized and pushed the new location.
3. OneDrive is not the only offsite backup you rely on for these files.

| Original | New home | Notes |
|---|---|---|
| `C:\Users\marya\OneDrive\Documents\Claude\Projects\VoxMerch\.claude\` (folder) | `C:\Users\marya\Projects\VoxMerch\.claude\` | Full folder copied, including brand-voice guidelines and local settings. |
| `C:\Users\marya\OneDrive\Documents\Claude\Projects\VoxMerch\` (the whole folder) | Migrated contents | Only delete once everything above is confirmed. |
| `C:\Users\marya\HALO Keane Dropbox\VoxMerch\AI\AI Social Media Manager\` | `voxmerch-content\AI-Social-Media-Manager\` | Full folder copied. If you run this project directly from Dropbox, keep the Dropbox copy until you switch your workflow to open it from `C:\Users\marya\Projects\VoxMerch\`. |
| `C:\Users\marya\HALO Keane Dropbox\VoxMerch\AI\agent-skills-main\`, `business-coach\`, `claude-seo-main\`, `marketingskills-main\` | `external-skills/` under each binder | Same caveat: if any of these were installed as a Claude plugin pointing at the Dropbox path, update the plugin to point at the new location before deleting. |

---

## Tier 3 — DO NOT DELETE (live system dependency)

| Original | Reason to keep |
|---|---|
| `C:\Users\marya\OneDrive\Documents\Claude\Scheduled\voxmerch-daily-brief\` | This is an active Cowork scheduled task. Cowork reads from this path to run your daily brief. A copy is now also in `voxmerch-launch-ops\voxmerch-daily-brief\` for reference and Git tracking, but the running task still lives here. Leave this folder alone unless you deliberately re-register the scheduled task against the new location. |

---

## Tier 4 — Out of scope (not Claude/Cowork/Claude Code, so untouched)

Everything else in the `HALO Keane Dropbox\VoxMerch\` root (Artwork Samples, Blog, Clients, Competitor Info, Corporate Docs, Development, Dinsmore, Fogline Media LLC, HALO, Insurance, Katie Brown, Logos, Marketing, Monday.com, NDAs, Operations, POC, Pricing, Printify, Resumes, Social Media, Video, Website, iCloud Photos, plus loose PDFs and images) was intentionally left where it is. These are business assets, not Claude tooling, and a large chunk (Video folder alone is 5.5 GB) should never go into a GitHub repo.

---

## Recommended order

1. Init Git and push the new repo: `cd C:\Users\marya\Projects\VoxMerch && git init && git add . && git commit -m "Initial VoxMerch consolidation"` then push to GitHub.
2. Once push succeeds, delete **Tier 1** items.
3. Delete **Tier 2** items only after you have switched your daily workflow (Claude Code shortcuts, any launch scripts) to open from the new path.
4. Never touch **Tier 3**.
