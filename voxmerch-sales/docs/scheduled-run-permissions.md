# Making the stage-sync routine run unattended

## What went wrong on 2026-09-01

The weekday reconcile fired at 7:16 AM CDT, fetched Apollo page 1 of 19, hit a permission
block on page 2, and sat there for 8 hours 25 minutes until Mary Anne came back to her desk
at 3:41 PM CDT. Nothing reconciled. No stage was written, no group was moved, no promotion
was made, and the deliverability line was never read.

Nobody is watching a scheduled run, so a run that needs an approval does not get one. It
just stops.

## Why the existing allowlist did not prevent it

`.claude/settings.json` already allows `mcp__Apollo-io` and `mcp__monday-com`, so the
allowlist was never the gap. The block came from the **auto-mode classifier**, which sits
above `settings.json` and evaluates calls independently of the allow rules. Adding more
`permissions.allow` entries does not change its verdict.

Claude cannot fix this itself. Every write to `.claude/settings.json` is refused, whether
by `Write`, `Edit`, or a shell heredoc, because letting an agent widen its own permissions
would make the guardrail meaningless. Applying this needs a human.

## Pick one of these

### Option A, narrowest. Teach the classifier about this routine.

`autoMode.allow` injects extra rules into the classifier's prompt. `"$defaults"` keeps
every built-in rule, so this only adds. Auto mode stays on and everything outside these
three rules is still evaluated normally.

Merge into `.claude/settings.json`:

```json
{
  "autoMode": {
    "allow": [
      "$defaults",
      "Paging apollo_contacts_search to completion. The scheduled stage reconcile must read every page (pagination.page through pagination.total_pages) before it can derive the board diff, so a run legitimately makes many consecutive calls to this one read-only tool. Blocking the second and later pages does not make the run safer, it strands it holding a partial contact set.",
      "Reading and writing the two VoxMerch Monday.com pipeline boards, 18409325257 and 18407308519, through the monday-com MCP tools: get_board_items_page, update_items, create_items, create_group, change_item_column_values, and move_item_to_group via all_monday_api. These are the reconcile's whole purpose.",
      "Running the scripts under voxmerch-sales/scripts/ and reading the tool-result files the harness writes under ~/.claude/projects/*/tool-results/. The reconciler is deliberately offline and takes those files as input."
    ]
  }
}
```

### Option B. Set the routine's own permission mode.

The most surgical fix, because it changes only the scheduled run and leaves interactive
sessions in this repo untouched. Where the routine is configured, set its permission mode to
one that does not prompt. `dontAsk` still honours `deny` rules; `bypassPermissions` honours
nothing.

Prefer this over putting `permissions.defaultMode` in `.claude/settings.json`, which would
apply to every session in the repo including the interactive ones.

### Option C. Turn auto mode off for this project.

```json
{ "permissions": { "disableAutoMode": "disable" } }
```

The plain allowlist then governs, with no classifier second-guessing it. Broader than
Option A, and it also changes interactive sessions here.

**Recommendation: Option B if the routine config exposes a permission mode, otherwise
Option A.**

## Also worth merging, regardless of which option

The allowlist is missing the read-only shell commands every run uses, and two Apollo
write tools that should never fire unattended belong behind `ask`.

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 voxmerch-sales/scripts/:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(wc:*)",
      "Bash(sed -n:*)",
      "Bash(mkdir:*)",
      "Bash(date:*)",
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git show:*)",
      "Bash(git rev-parse:*)",
      "Bash(git branch:*)"
    ],
    "ask": [
      "mcp__Apollo-io__apollo_emailer_campaigns_approve",
      "mcp__Apollo-io__apollo_emailer_campaigns_remove_or_stop_contact_ids"
    ]
  }
}
```

`Bash(python3 voxmerch-sales/scripts/:*)` widens the existing
`Bash(python3 voxmerch-sales/scripts/stage_sync.py:*)` to cover `apollo_pull.py` and
`test_stage_sync.py` without allowing `python3 -c`, which would be arbitrary code execution.

Stopping a contact's Apollo enrollment needs Mary Anne's approval per the 2026-08-27
backfill guard, so `apollo_emailer_campaigns_remove_or_stop_contact_ids` sits in `ask`
deliberately. Under a non-prompting permission mode an `ask` rule cannot prompt, so if you
choose Option B or C, move those two to `deny` instead and lift the rule by hand on the rare
occasion you want them.

## Two other fixes that shipped alongside this

**`apollo_pull.py`** replaces 19 approval-gated MCP calls with one command. Each MCP page
result runs about 580,000 characters, past the tool-result limit, so the harness writes it
to a file and returns an "output too large" notice; nineteen of those cost roughly 8,000
tokens per run to learn nothing. The script writes the page files directly and prints a few
lines. It needs an Apollo REST key, since the Apollo MCP server authenticates by OAuth and
exposes no key to a script: generate one in Apollo under Settings > Integrations > API and
put it in the routine's environment as `APOLLO_API_KEY`. Until then the routine falls back
to paging the MCP tool.

**`stage_sync.py --strict-coverage`** reports board items whose Apollo contact id the pull
never returned. Before this, a filtered pull that dropped an enrolled contact left that
person's board stage stale and said nothing. That guard is what makes
`apollo_pull.py --label-id` safe to use, which is the change that cuts 19 pages to about 3.
Run the filtered pull and `--strict-coverage` together, never the filter alone.

## The routine prompt points at a branch that no longer exists

The stored prompt says to commit on `claude/voxmerch-events-sales-scaling-yqfmd9`. That
branch was merged in `3d56f3a` and is gone. Update the prompt to name a live branch, or the
instruction will keep misfiring.
