# Claude Code maintenance log

One dated entry per audit. Records what was cut, moved, or rewritten on purpose so the next audit
does not suggest putting it back. The audit itself is the `claude-code-maintenance` skill.

The container copy at `~/.claude/maintenance-log.md` is ephemeral; this file is the one that lasts.

## 2026-09-24 (audit run 2026-09-20, applied 2026-09-24)

Scope: project files in this repo only. No user-scope CLAUDE.md, rules, auto memory, or plugins were
visible from the cloud container. Claude Code 2.1.278. Always-loaded context before and after: about
628 tokens (rough estimate, characters / 4). This round was correctness, not cost.

**Cut, and why it should stay cut**
- `README.md`: the claim that `.claude/` brand-voice files "load automatically." No import exists.
- `README.md`: the `git init` first-use step. Repo has been on GitHub since July 2026.
- `validate-post.sh` banned words `can`, `may`, `just`, `that`, `very`, `really`, `literally`,
  `actually`, `certainly`, `probably`, `basically`, `could`, `maybe`, `however`, `hence`, `craft`,
  `crafting`, `imagine`, `discover`, `unlock`, `exciting`, `remarkable`, `boost`, `powerful`,
  `inquiries`, and phrases `not alone`, `stark`. They blocked essentially every post; a clean 145-char
  post failed on "that." Do not re-add ordinary English to that list.

**Moved to `docs/archive/`, and why they should stay there**
- `brand-voice-guidelines-2026-04.md`, `brand-voice.local-2026-04.md`: describe a direct-to-brand
  fulfillment vendor and position against "generic merchandise vendors." VoxMerch is B2B2B, sells
  through the events channel only, and treats the branded merchandise industry as a partner. Current
  voice lives in the account-level `voxmerch-voice` and `mary-anne-voice` skills.
- `DELETION-REVIEW-2026-migration.md`: completed one-time migration checklist.

**Rewritten**
- Daily brief schedule: 5:00 AM CT Mon-Fri, cron `0 10 * * 1-5` CDT / `0 11 * * 1-5` CST, in UTC.
  Was documented as "6:00 AM CST, cron `0 6 * * *`, local time," which matched no live trigger.
- Daily brief tools: `list_triggers` (not `list_scheduled_tasks`), Microsoft 365
  `outlook_create_draft` (not `gmail_create_draft`; the mailbox is Exchange). Draft only, never sends.
- `.claude/settings.json`: MCP permission rules use `Apollo_io` and `monday_com` (underscores). The
  hyphenated form matched nothing, so the `ask` gates on send-now and sequence mutation never fired.
- `validate-post.sh` em-dash check: literal `grep -e '—' -e '–'`. The `\x{2014}` PCRE form errors
  under a non-UTF-8 locale (grep exit 2), which made the check silently pass. Em dashes are never
  allowed; the message now says rewrite the sentence.
- `validate-post.sh` banned list now carries the house buzzwords (`innovative`, `seamless`, `synergy`,
  `cutting-edge`, `state-of-the-art`, `game-changing`, `leverage`, `world-class`) and the LinkedIn
  openers `excited to share`, `thrilled to announce`, `excited to announce`.
- AI-Social-Media-Manager hook command uses `"$CLAUDE_PROJECT_DIR"` so the path survives a `cd`.

**Business fact recorded**
- VoxMerch sells through the events channel only. There is no distributor track, deferred or
  otherwise. "Deferred to January 1" language in the SDR skill and the August sales plans is void
  (superseded notes added; dated plans were not rewritten). The one exception is HALO distributors
  who have already presented VoxMerch to their clients. Monday group `group_mm5rxery` is still named
  "Deferred - Distributors (Jan 1)"; the rename is a board change, not a repo change.

**Deliberately kept**
- Root `CLAUDE.md`, all 31 lines. Every rule is a non-default convention with its incident attached.
- SDR `SKILL.md` body, all 434 lines. The long passages are dated incidents; do not trim.
- `AI-Social-Media-Manager/CLAUDE.md:26` "No em dashes." Kept even though the hook enforces it,
  because draft-time guidance is what prevents the blocked call.

**Still open from this audit** (numbers from the report): 18 replace account-level SDR skill copy
(manual), 19 and 20 `disable-model-invocation: true` on SDR and plan-week, 21 header on daily-brief
SKILL.md, 24 narrow `git checkout`, 25 deny `git push --force`, 26 narrow `curl` in the social
project, 30 MCP write-scope review.

**Next audit:** 15 to 22 October 2026, or the day a new Claude model ships, whichever is first.
