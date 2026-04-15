# voxmerch-daily-brief (scheduled task)

This folder holds the **Git-tracked source of truth** for the VoxMerch daily brief scheduled task.

- **Schedule:** Every day at 6:00 AM CST (cron `0 6 * * *`)
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
3. Verify with `list_scheduled_tasks` that `nextRunAt` is still correct and `enabled: true`.

## To change the schedule

Ask Claude to update `voxmerch-daily-brief` with a new `cronExpression` (5-field cron in LOCAL time).

## Do NOT delete

The OneDrive `Claude\Scheduled\voxmerch-daily-brief\` folder is live system state. Deleting it would break the scheduler. This folder (the Git copy) can be edited freely, as long as you push changes to the scheduler afterward.
