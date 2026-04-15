---
name: plan-week
description: Plan and schedule a full week of social media content across all platforms. Accepts topics, URLs, drafts, or images. Produces an editable content-plan.md, then publishes on approval using parallel subagents.
argument-hint: "[topic/URL/draft/instructions]"
---

# Weekly Content Planner

Plan, draft, and schedule a full week of social media posts across LinkedIn, Twitter/X, Instagram, and Facebook using the Blotato API.

## Workflow

### Step 1: Understand the User's Intent

The user may provide any combination of:
- **A topic or list of topics**: subjects to create content around for the week
- **Existing draft posts**: text to adapt and schedule across the week
- **URLs**: youtube, tiktok, article, PDF, audio, website, blog to extract content from
- **Image/photo URLs**: to include as media in posts

Parse `$ARGUMENTS` to identify what was provided.

**Ask clarifying questions ONE AT A TIME until 95% confident.** Key questions to consider (ask only if needed):
- What platforms should this week cover? (default: all connected accounts)
- How many posts per day or per week? Any days to skip?
- Any specific themes, campaigns, or events this week?
- Preferred scheduling: next free slot, specific times, or publish immediately?
- Should visuals be generated for any/all posts?
- Any URLs or references to draw content from?

Do NOT proceed until you have enough to plan confidently.

### Step 2: Get Blotato Account Info

Retrieve the API key from environment variable `BLOTATO_API_KEY`.

```bash
# Verify API key and get user info
curl -s -H "blotato-api-key: $BLOTATO_API_KEY" https://backend.blotato.com/v2/users/me

# List connected social accounts
curl -s -H "blotato-api-key: $BLOTATO_API_KEY" https://backend.blotato.com/v2/users/me/accounts
```

For Facebook and LinkedIn pages, also fetch subaccounts to get the `pageId`:
```bash
curl -s -H "blotato-api-key: $BLOTATO_API_KEY" "https://backend.blotato.com/v2/users/me/accounts/{accountId}/subaccounts"
```

Record all connected account IDs, platforms, names, and pageIds for use later.

### Step 3: Research and Extract Content

**If topics were provided**: research each topic using WebSearch to gather current, relevant angles. Focus on practical insights, data points, and trends the target audience would find valuable.

**If URLs were provided**: extract content from each using the Blotato Source API:

```bash
curl -s -X POST "https://backend.blotato.com/v2/source-resolutions-v3" \
  -H "blotato-api-key: $BLOTATO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "sourceType": "SOURCE_TYPE",
      "url": "THE_URL"
    }
  }'
```

**sourceType options**: "text", "article", "youtube", "twitter", "tiktok", "perplexity-query", "audio", "pdf"

IMPORTANT: The `source` fields MUST be wrapped in a `"source"` object.

Poll for completion:
```bash
curl -s -H "blotato-api-key: $BLOTATO_API_KEY" "https://backend.blotato.com/v2/source-resolutions-v3/{id}"
```

Poll every 3-5 seconds until status is no longer "in-progress".

### Step 4: Fetch Available Visual Templates

If visuals are desired, fetch the template catalog:

```bash
curl -s -H "blotato-api-key: $BLOTATO_API_KEY" "https://backend.blotato.com/v2/videos/templates"
```

Select the most appropriate template for each day's content theme. Each day's posts should share one visual (generated once, reused across platforms for that day).

### Step 5: Build the Content Plan

Write the plan to `content-plan.md` in the project root.

**WRITING STYLE (apply to all draft text — same rules as /post skill):**

- Use clear, simple language.
- Use short, impactful sentences.
- Use active voice; avoid passive voice.
- Focus on practical, actionable insights.
- Use "you" and "your" to directly address the reader.
- AVOID em dashes. Use commas, periods, or ellipsis "..." instead.
- AVOID constructions like "...not just this, but also this".
- AVOID metaphors and cliches.
- AVOID generalizations.
- AVOID unnecessary adjectives and adverbs.
- AVOID hashtags, semicolons, markdown, asterisks.
- AVOID these words: "can, may, just, that, very, really, literally, actually, certainly, probably, basically, could, maybe, delve, embark, enlightening, esteemed, shed light, craft, crafting, imagine, realm, game-changer, unlock, discover, skyrocket, abyss, not alone, in a world where, revolutionize, disruptive, utilize, utilizing, dive deep, tapestry, illuminate, unveil, pivotal, intricate, elucidate, hence, furthermore, however, harness, exciting, groundbreaking, cutting-edge, remarkable, remains to be seen, glimpse into, navigating, landscape, stark, testament, in summary, in conclusion, moreover, boost, powerful, inquiries, ever-evolving"
- IMPORTANT: Review every draft and ensure no em dashes!

**Platform guidelines:**

- **LinkedIn**: Professional tone, longer format, use line breaks for readability. Max 3000 chars.
- **Twitter/X**: Concise, max 280 chars per tweet. Use threads (note in plan) for longer content.
- **Instagram**: Visual-first, engaging caption, emoji-friendly. Max 2200 chars. MUST have media.
- **Facebook**: Conversational, moderate length. Max 63206 chars.

**Brand voice samples** — refer to the /post skill's SKILL.md for platform-specific voice examples.

**content-plan.md format:**

```markdown
# Weekly Content Plan: {Week of DATE}

Source: {topic, URL, or description of input}
Platforms: {list of platforms}
Scheduling: {next free slot / specific times / immediate}

---

## Monday — {Day Theme/Angle}

### Post 1: {Platform}
- **Topic**: {specific angle}
- **Visual**: Yes / No
- **Template**: {template name or "N/A"}
- **Draft**:

{FULL post text here, formatted exactly as it will be published.
Use line breaks for readability.
Short sentences. Active voice.
This is the real post, not a summary.}

### Post 2: {Platform}
- **Topic**: {specific angle}
- **Visual**: Yes / No
- **Template**: {template name or "N/A"}
- **Draft**:

{FULL post text here, adapted for this platform's format and limits.
Different wording than Post 1 — tailored to the platform.}

---

## Tuesday — {Day Theme/Angle}

### Post 3: {Platform}
...

---

(continue for each day with posts)
```

**Rules for the plan:**
- Each day gets its own section with a theme/angle
- Each post is numbered sequentially across the week (Post 1, Post 2, ... Post N)
- Draft text must be the FULL post content, properly formatted — not a summary or outline
- Adapt text per platform (don't copy-paste the same text across platforms)
- If a day has multiple platform posts, they share the same visual (generated once)
- Mark Visual as "Yes" and specify the template name if a visual should be generated
- Instagram posts MUST have Visual: Yes

### Step 6: Present the Plan for Approval

Show the user the full plan and ask for approval. Let them know they can:
- Edit `content-plan.md` directly and tell you when ready
- Ask you to revise specific posts
- Change days, platforms, or scheduling
- Add or remove posts

Do NOT proceed to publishing until the user explicitly approves.

### Step 7: Generate Visuals

After approval, generate visuals for each day that has Visual: Yes.

Generate ONE visual per day (all posts on that day share it):

```bash
# Generate visual
curl -s -X POST "https://backend.blotato.com/v2/videos/from-templates" \
  -H "blotato-api-key: $BLOTATO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "TEMPLATE_UUID",
    "inputs": {},
    "prompt": "Description based on the day theme and post content",
    "render": true
  }'
```

Use bare UUID for templateId. Leave `inputs` empty and use `prompt` for AI-powered filling.

Poll `GET /v2/videos/creations/{id}` every 3-5 seconds until status is "done". Extract the rendered media URL.

### Step 8: Publish with Parallel Subagents

Re-read `content-plan.md` to pick up any edits the user made.

Launch one Agent subagent per post, ALL IN A SINGLE MESSAGE so they run in parallel. Each agent gets a self-contained prompt.

Use this template for each subagent prompt:

```
You are publishing a scheduled social media post via the Blotato API.

POST DETAILS:
- Day: {DAY}
- Post number: {N}
- Platform: {PLATFORM}
- Post text (publish EXACTLY as written, do not modify):

{DRAFT TEXT FROM PLAN}

ACCOUNT INFO:
- accountId: {ACCOUNT_ID}
- pageId: {PAGE_ID or "N/A"}
- API key env var: BLOTATO_API_KEY

MEDIA URLS: {visual URL for this day, or "none" — for Instagram this is REQUIRED}

SCHEDULING: {useNextFreeSlot: true | scheduledTime: "ISO_DATE" | immediate (omit both fields)}

YOUR TASK:
1. Publish the post using this curl command:

curl -s -X POST "https://backend.blotato.com/v2/posts" \
  -H "blotato-api-key: $BLOTATO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "accountId": "{ACCOUNT_ID}",
      "content": {
        "text": "{POST_TEXT}",
        "mediaUrls": [{MEDIA_URLS}],
        "platform": "{PLATFORM}"
      },
      "target": {
        "targetType": "{PLATFORM}"{, "pageId": "PAGE_ID" if facebook or linkedin page}
      }
    },
    "useNextFreeSlot": true
  }'

CRITICAL RULES:
- content.platform and target.targetType MUST be the same value
- useNextFreeSlot / scheduledTime are ROOT-LEVEL fields (siblings of "post"), NOT nested
- For Facebook: include "pageId" in target
- For LinkedIn pages: include "pageId" in target (omit for personal profile)
- For Twitter threads: use additionalPosts inside content

2. Poll for status: GET https://backend.blotato.com/v2/posts/{postSubmissionId} until published, scheduled, or failed.
3. Return a summary in EXACTLY this format (one line):
   RESULT|{DAY}|Post {N}|{PLATFORM}|{status}|{publicUrl or "none"}|{first 60 chars of post text}
```

### Step 9: Log Results and Update Plan

After ALL subagents complete:

1. **Update content-plan.md**: Add a status line to each post section:
   - `- **Status**: Published / Scheduled / Failed`
   - `- **URL**: {public URL}`

2. **Append to post-log.md**: Add one row per published/scheduled post to the existing table:

```
| {date} | {Platform} ({account name}) | {post preview, truncated} | {Status} | {URL} | {Source: "Weekly plan: {topic}"} |
```

3. **Present summary** to the user: show a table of all posts with day, platform, status, and URL.

## Error Handling

- If API returns 429: rate limited, wait and retry
- If a post fails: log the failure, continue with other posts, report all failures at the end
- If account not found: list available accounts and ask user to pick
- Always validate that target platform accounts are connected before building the plan
- If visual generation fails: log it, publish the post without media (except Instagram — report the failure and skip)
