# Skills moved to `.claude/skills/`

This directory used to hold a working copy of the AI SDR skill as a loose file,
`voxmerch-sdr-contact-enrichment-SKILL.md`. That was a trap and it cost a week.

A loose markdown file in this folder is documentation. It is not a skill and no session ever
loads it. The copy that actually ran came from the account-level skill store, and on 2026-08-05
those two files were found to have diverged badly: the corrected post-rebuild version written on
2026-08-01 was sitting here, while the version sessions loaded was still the pre-rebuild one that
targeted the deprecated sequence `69e5407d76f3d1001dda3c7b`, enrolled everyone paused, led with
President and CEO titles, and had no resale test and no off-limits groups.

**The skill now lives at `.claude/skills/voxmerch-sdr-contact-enrichment/SKILL.md`.** Claude loads
skills from that path automatically when working in this repo, so the version in git is the version
that runs, and a change to it is a reviewable commit.

## If you add another skill

Put it at `.claude/skills/<skill-name>/SKILL.md`. One directory per skill, frontmatter with `name`
and `description`. Do not keep a second copy anywhere.

## The account-level copy still needs replacing by hand

Repo skills only load for sessions working in this repo. Sessions started from claude.ai chat
without it still load the account-level copy. Until that one is replaced with the file in
`.claude/skills/`, the stale version can still be picked up outside this repo. Replacing it is a
manual step in Claude's skill settings and cannot be done from a session here.
