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

## The complete file to paste

This is every tool the Phase 4 reconcile touches, so a run has nothing left to ask about.
Replace the whole contents of `.claude/settings.json` with this.

```json
{
  "permissions": {
    "allow": [
      "mcp__Apollo-io__apollo_contacts_search",
      "mcp__Apollo-io__apollo_emailer_campaigns_search",
      "mcp__Apollo-io__apollo_labels_index",
      "mcp__monday-com__get_board_items_page",
      "mcp__monday-com__get_board_info",
      "mcp__monday-com__update_items",
      "mcp__monday-com__create_items",
      "mcp__monday-com__create_group",
      "mcp__monday-com__change_item_column_values",
      "mcp__monday-com__all_monday_api",
      "mcp__github__pull_request_read",
      "mcp__github__list_pull_requests",
      "mcp__github__create_pull_request",
      "Bash(python3 voxmerch-sales/scripts/:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(wc:*)",
      "Bash(grep:*)",
      "Bash(sed -n:*)",
      "Bash(mkdir:*)",
      "Bash(date:*)",
      "Bash(git status:*)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git show:*)",
      "Bash(git rev-parse:*)",
      "Bash(git branch:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git fetch:*)",
      "Bash(git pull:*)",
      "Bash(git checkout:*)"
    ],
    "deny": [
      "mcp__Apollo-io__apollo_emailer_messages_send_now",
      "mcp__Apollo-io__apollo_emailer_campaigns_approve",
      "mcp__Apollo-io__apollo_emailer_campaigns_remove_or_stop_contact_ids",
      "mcp__Apollo-io__apollo_email_account_purchase_create",
      "mcp__Apollo-io__apollo_sequences_create",
      "mcp__Apollo-io__apollo_sequences_update"
    ]
  },
  "autoMode": {
    "allow": [
      "$defaults",
      "Paging apollo_contacts_search to completion. The scheduled stage reconcile must read every page (pagination.page through pagination.total_pages) before it can derive the board diff, so a run legitimately makes several consecutive calls to this one read-only tool. Blocking the second and later pages does not make the run safer, it strands it holding a partial contact set.",
      "Reading and writing the two VoxMerch Monday.com pipeline boards, 18409325257 and 18407308519, through the monday-com MCP tools: get_board_items_page, update_items, create_items, create_group, change_item_column_values, and move_item_to_group via all_monday_api. These are the reconcile's whole purpose.",
      "Running the scripts under voxmerch-sales/scripts/ and reading the tool-result files the harness writes under ~/.claude/projects/*/tool-results/. The reconciler is deliberately offline and takes those files as input."
    ]
  }
}
```

Three deliberate choices in there.

**The named Apollo and Monday tools replace the bare `mcp__Apollo-io` and `mcp__monday-com`
server-wide entries.** Those allowed every tool on both servers, including every Apollo tool
that sends mail or edits a sequence. The reconcile only reads from Apollo and only writes to
Monday, so the list says exactly that.

**The dangerous Apollo tools moved from `ask` to `deny`.** Stopping a contact's enrollment
needs Mary Anne's approval per the 2026-08-27 backfill guard. An `ask` rule cannot prompt
when nobody is watching, which is every scheduled run, so `ask` was giving a guarantee it
could not keep. `deny` holds unattended, and can be lifted by hand for the rare run that
needs it.

**`Bash(python3 voxmerch-sales/scripts/:*)`** widens the old
`Bash(python3 voxmerch-sales/scripts/stage_sync.py:*)` to cover the other scripts without
allowing `python3 -c`, which would be arbitrary code execution.

## Two other fixes that shipped alongside this

**A filtered Apollo pull** cuts the run from 19 pages to 2 or 3. `apollo_contacts_search`
accepts `contact_label_ids`, so the reconcile now pulls only the campaign cohorts (Event
Activation, Event Activation Directors & VPs, Tranche 1 Batch 1 and 2, VoxMerch SDR: about
200 contacts) instead of the whole 1,839-contact account. Each oversized page result costs a
few hundred tokens of "output too large" notice, so most of the run's token bill was pages
nobody needed. The exact list ids are in the skill's Phase 4.

**Do not store an Apollo REST API key.** An earlier draft of this document said to put one in
the cloud environment's **Environment variables** box. That was wrong. That box is plaintext,
readable by anyone using the environment and by any command run in it, and its own help text
says: *"These are visible to anyone using this environment — don't add secrets or
credentials."* The **API credentials** feature that would hold a key properly, outside the
sandbox, is not available on this account. `apollo_pull.py` remains in the repo for whenever
a real secret store exists; until then it is unused, and it would also need `api.apollo.io`
added to the environment's network allowlist, which the default **Trusted** level omits. The
MCP path needs no key at all, because the Apollo MCP server authenticates by OAuth.

**`stage_sync.py --strict-coverage`** reports board items whose Apollo contact id the pull
never returned. Before this, a filtered pull that dropped an enrolled contact left that
person's board stage stale and said nothing. That guard is what makes
`apollo_pull.py --label-id` safe to use, which is the change that cuts 19 pages to about 3.
Run the filtered pull and `--strict-coverage` together, never the filter alone.

## The routine prompt points at a branch that no longer exists

The stored prompt says to commit on `claude/voxmerch-events-sales-scaling-yqfmd9`. That
branch was merged in `3d56f3a` and is gone. Update the prompt to name a live branch, or the
instruction will keep misfiring.
