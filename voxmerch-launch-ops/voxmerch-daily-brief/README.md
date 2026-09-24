# voxmerch-daily-brief (scheduled task)

This folder holds the **Git-tracked source of truth** for the VoxMerch daily brief scheduled task.

- **Schedule:** 5:00 AM CT, Mon-Fri. Trigger `trig_0153Ljh1jbUU1tk6Qy5zHf6d`. Cron `0 10 * * 1-5` under CDT and `0 11 * * 1-5` under CST; both are UTC, and the DST routine in `../../scheduled-routines.md` moves it twice a year.
- **Recipient:** maryanne@voxmerch.com
- **Data source:** Monday.com workspace "VoxMerch Launch" (workspace ID 14935930) across 5 boards.

## How the task actually runs

Claude's scheduled task system stores its own copy of `SKILL.md` at:

    C:\Users\marya\OneDrive\Documents\Claude\Scheduled\voxmerch-daily-brief\SKILL.md

That system copy is the file the scheduler actually executes. The copy in this folder is what you version-control. Edits to `SKILL.md` here will NOT affect the running task unless they are pushed to the scheduler.

## To edit the prompt

1. Edit `SKILL.md` in this folder and commit the change to Git.
2. Push the new prompt to the scheduler by asking Claude:
   > "Update the `voxmerch-daily-brief` scheduled task with the prompt from `C:\Users\marya\Projects\VoxMerch\voxmerch-launch-ops\voxmerch-daily-brief\SKILL.md`."
3. Verify with `list_triggers` that `next_run_at` is correct and `enabled: true`.

## To change the schedule

Ask Claude to update the trigger with a new 5-field cron **in UTC** (see the conversion rule in the root `CLAUDE.md`), then change the matching row in `../../scheduled-routines.md` so the DST routine keeps shifting it.

## Do NOT delete

The OneDrive `Claude\Scheduled\voxmerch-daily-brief\` folder is live system state. Deleting it would break the scheduler. This folder (the Git copy) can be edited freely, as long as you push changes to the scheduler afterward.

This was Tier 3 ("DO NOT DELETE, live system dependency") in the 2026 migration checklist, now archived at `docs/archive/DELETION-REVIEW-2026-migration.md`. Leave the OneDrive folder alone unless you deliberately re-register the scheduled task against the new location.
