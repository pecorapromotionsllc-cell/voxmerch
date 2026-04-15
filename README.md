# VoxMerch

The consolidated VoxMerch project repo. Everything is organized into five binders so Claude Code, Cowork, and Claude in general can find the right context for the work at hand.

## Layout

| Binder | Purpose |
|---|---|
| `voxmerch-platform/` | The SaaS product itself. Code, AI artwork generation, data capture. Developer territory. |
| `voxmerch-marketing-site/` | Public website (voxmerch.com). Landing pages, sales pages, how-it-works pages. |
| `voxmerch-content/` | All written marketing. Social captions, LinkedIn posts, email sequences, blog drafts, content calendar, ad copy. |
| `voxmerch-sales/` | Outreach and sales materials. Dual-track playbooks for event planners vs. merch salespeople, decks, one-pagers, demo scripts, follow-up templates. |
| `voxmerch-launch-ops/` | Launch PM. Monday.com integration, launch checklists, timelines, the five-board workspace. |

## Shared configuration

- `.claude/` holds the brand voice guidelines and local Claude settings. Loaded automatically by Claude Code when working in this repo.
- `docs/external-skills.md` indexes the third-party Claude skill plugins bundled under each binder's `external-skills/` folder, with their upstream source URLs.

## Sync

This folder is intended to be version-controlled with Git and synced to GitHub so the project is available across devices.

- Run `git init` at the root on first use.
- `.gitignore` already excludes local Claude settings, OS junk, and temporary files.
- Large binary assets (video, full artwork libraries) are intentionally kept in Dropbox and are not tracked here.
