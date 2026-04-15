---
name: voxmerch-daily-brief
description: Daily 6:00 AM CST brief of tasks due today and overdue across all VoxMerch Launch boards, emailed to maryanne@voxmerch.com
---

You are generating a daily task brief for the Monday.com "VoxMerch Launch" workspace (workspace ID: 14935930). Your job is to pull all tasks due today and all overdue tasks from the 5 boards listed below, format them into a clean checklist email, and send it via Gmail draft or direct send to maryanne@voxmerch.com.

## Step 1: Pull tasks due today and overdue from each board

For each board below, run TWO queries using the get_board_items_page tool:
- **Due today**: Filter the date column with compareValue: ["TODAY"] using operator: "any_of", excluding items with status "Done" (status id 1, using not_any_of operator).
- **Overdue**: Filter the date column with compareValue: "TODAY" using operator: "lower_than", excluding items with status "Done" (status id 1, using not_any_of operator).

Include columns (set includeColumns: true) so you can read the item name, status, due date, owner, and priority (where available).

### Board 1: GTM Master Timeline
- Board ID: 18407308517
- Due Date column: date_mm24b8wh
- Status column: color_mm243xfq (Done = id 1)
- Priority column: color_mm24cyq3
- Owner column: multiple_person_mm244n2c

### Board 2: Outreach Pipeline
- Board ID: 18407308519
- Due Date column: date_mm24681w
- Status column: color_mm24v105 (Done = id 1)
- Next Action column: text_mm24rfwq

### Board 3: Social Media Content Calendar
- Board ID: 18407308521
- Publish Date column: date_mm24jtwd
- Draft Status column: color_mm245d39 (Done = id 1)
- Asset Status column: color_mm24kc7p
- Platform column: text_mm24wv2n

### Board 4: Sales Assets & Collateral
- Board ID: 18407308524
- Due Date column: date_mm24madc
- Status column: color_mm243033 (Done = id 1)
- Owner column: multiple_person_mm244z9p

### Board 5: Operations & Logistics
- Board ID: 18407308527
- Due Date column: date_mm24bec9
- Status column: color_mm24wycm (Done = id 1)
- Priority column: color_mm249m4x
- Owner column: multiple_person_mm24a4x1

## Step 2: Format the email

Compose an email with:
- **To:** maryanne@voxmerch.com
- **Subject:** "VoxMerch Daily Brief -- [Today's Date formatted as Month Day, Year]"
- **Body:** A clean, scannable HTML email structured as follows:

Start with a one-line greeting: "Good morning, Mary Anne! Here's your VoxMerch Launch brief for today."

Then organize results into two sections:

**OVERDUE** (use a red header or bold red text)
- Group overdue items by board name
- For each item, show: checkbox emoji (☐), item name, due date, status, priority (if available), and owner (if available)
- If no overdue items, say "No overdue items -- you're all caught up!"

**DUE TODAY** (use an orange/amber header or bold text)
- Group items by board name
- For each item, show: checkbox emoji (☐), item name, status, priority (if available), and owner (if available)
- If nothing due today, say "Nothing due today."

End with a brief sign-off: "Have a productive day!"

Keep formatting clean with simple HTML -- no complex CSS. Use bold board names as section headers, and bullet lists for items.

## Step 3: Send the email

Use the gmail_create_draft tool to create a draft email with the above subject and HTML body, addressed to maryanne@voxmerch.com. Review for final edit and email directly to Mary Anne.

## Important notes
- Always exclude items with status "Done" from both queries.
- If a board returns zero results for both queries, skip that board entirely in the email (do not include an empty section).
- Use the current date (the date this task runs) for all "TODAY" filters.
- Order overdue items by due date ascending (oldest first) so the most urgent appear at the top.