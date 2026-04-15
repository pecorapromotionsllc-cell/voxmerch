---
name: post
description: Create and publish social media posts to LinkedIn, Instagram, Twitter/X, and Facebook via Blotato. Use when the user wants to create, schedule, or publish social media content from topics, URLs, existing posts, or images. Supports "all" to post to every platform at once.
disable-model-invocation: true
argument-hint: "[platform or all] [topic/URL/instructions]"
---

# AI Social Media Manager

Create and publish social media posts to LinkedIn, Instagram, Twitter/X, and Facebook using the Blotato API.

## Workflow

### Step 1: Understand the User's Intent

The user may provide any combination of:
- **A platform**: linkedin, instagram, twitter, facebook, or **all** (required - ask if not provided)
- **A topic**: a subject to create original content about
- **An existing post**: text to adapt for the target platform
- **A URL**: youtube, tiktok, article, PDF, audio, website, blog to extract content from
- **Image/photo URLs**: to include as media in the post

**If platform is "all"**: skip to the **Multi-Platform Posting** section below.

Parse `$ARGUMENTS` to identify what was provided. If critical information is missing, ask **one clarifying question at a time** until you are 95% confident you can create a great post.

Key questions to consider (ask only if needed):
- Which platform? (if not specified)
- What tone/voice? (professional, casual, witty, etc.)
- Any specific call-to-action?
- Should this be a thread (Twitter) or single post?
- Any hashtags or mentions to include?

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

### Step 3: Extract Content from URLs (if provided)

If the user provided a URL, extract content using:

```bash
# Submit extraction request
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

IMPORTANT: The `source` fields MUST be wrapped in a `"source"` object. Do NOT place them at the top level.

Then poll for completion:
```bash
curl -s -H "blotato-api-key: $BLOTATO_API_KEY" "https://backend.blotato.com/v2/source-resolutions-v3/{id}"
```

Poll every 3-5 seconds until status is no longer "in-progress".

### Step 4: Create the Post Content

Based on the extracted content, topic, or adapted post, craft platform-appropriate content.

**WRITING STYLE (apply to all platforms):**

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
- IMPORTANT: Review every post and ensure no em dashes!

**BRAND VOICE SAMPLES (per platform):**

Twitter voice:
<PASTE TWITTER EXAMPLES>

LinkedIn voice:
Example 1:
"Some brands watch the tournament. Others activate around it.

March Madness is a reminder that the best branded merchandise does more than show up.

It becomes part of the moment.
The mini basketball fans keep on their desk
The rally towel waving during the game
The drinkware that shows up at every watch party

The right merch turns game day energy into a brand experience people remember.

Check out our Elite 8 fan favorite giveaways brands use during March Madness."

Instagram voice:
<PASTE INSTAGRAM EXAMPLES>

Facebook voice:
<PASTE FACEBOOK EXAMPLES>

**Platform guidelines:**

- **LinkedIn**: Professional tone, longer format, use line breaks for readability
- **Twitter/X**: Concise (280 chars for single tweet), punchy. Use threads (`additionalPosts`) for longer content
- **Instagram**: Visual-first, engaging caption, emoji-friendly
- **Facebook**: Conversational, moderate length

Present the draft to the user for approval before publishing.

### Step 5: Publish the Post

```bash
curl -s -X POST "https://backend.blotato.com/v2/posts" \
  -H "blotato-api-key: $BLOTATO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "accountId": "ACCOUNT_ID",
      "content": {
        "text": "POST_TEXT",
        "mediaUrls": [],
        "platform": "PLATFORM"
      },
      "target": {
        "targetType": "PLATFORM"
      }
    },
    "useNextFreeSlot": true
  }'
```

**CRITICAL RULES:**
- `content.platform` and `target.targetType` MUST be the same value
- Scheduling fields (`useNextFreeSlot`, `scheduledTime`) are ROOT-LEVEL fields, siblings of `"post"`, NOT nested inside `"post"`
- Default to `"useNextFreeSlot": true` so posts queue to the content calendar
- For Facebook: include `"pageId"` in `target`
- For LinkedIn pages: include `"pageId"` in `target` (omit for personal profile)

**Platform values**: "twitter", "linkedin", "instagram", "facebook"

**Thread creation** (Twitter, Bluesky, Threads):
```json
{
  "post": {
    "accountId": "ID",
    "content": {
      "text": "First post (1/3)",
      "mediaUrls": [],
      "platform": "twitter",
      "additionalPosts": [
        { "text": "Second post (2/3)", "mediaUrls": [] },
        { "text": "Third post (3/3)", "mediaUrls": [] }
      ]
    },
    "target": { "targetType": "twitter" }
  },
  "useNextFreeSlot": true
}
```

### Step 6: Poll for Publication Status

```bash
curl -s -H "blotato-api-key: $BLOTATO_API_KEY" "https://backend.blotato.com/v2/posts/{postSubmissionId}"
```

Poll until status is "published" or "failed". Extract the `publicUrl` from the response.

### Step 7: Log the Post

After successful publication or scheduling, append an entry to the post log file at the project root:

**File**: `post-log.md` (in the project root directory)

Append a new entry with:
- Date and time
- Platform
- Post content (truncated if very long)
- Status (published/scheduled)
- Public URL (if available)
- Source (topic/URL/adapted from)

## Scheduling Options

Three modes (explain to user if they ask):

1. **Next free slot** (DEFAULT): `"useNextFreeSlot": true` - queues to content calendar
2. **Specific time**: `"scheduledTime": "2025-12-25T15:00:00Z"` - publishes at exact time
3. **Immediate**: omit both fields - publishes right now

Always default to `useNextFreeSlot: true` unless the user explicitly asks to publish immediately or at a specific time.

## Visual Content Creation (Optional)

If the user wants a visual/image created for their post:

```bash
# List available templates
curl -s -H "blotato-api-key: $BLOTATO_API_KEY" "https://backend.blotato.com/v2/videos/templates"

# Generate visual
curl -s -X POST "https://backend.blotato.com/v2/videos/from-templates" \
  -H "blotato-api-key: $BLOTATO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "TEMPLATE_UUID",
    "inputs": {},
    "prompt": "Description of what to create",
    "render": true
  }'
```

Use bare UUID for templateId. Leave `inputs` empty and use `prompt` for AI-powered filling.
Poll `GET /videos/creations/{id}` until status is "done".

## Multi-Platform Posting (platform = "all")

When the user specifies "all" as the platform, post to every connected platform in parallel.

### All-Platform Workflow

**Phase 1: Setup (do this yourself, sequentially)**

1. Retrieve the API key from `BLOTATO_API_KEY` and fetch connected accounts (Step 2 above).
2. If a URL was provided, extract content (Step 3 above).
3. If the user wants a visual/image, generate it ONCE using the Visual Content Creation flow. Store the resulting media URL — it will be shared across all platforms.
4. Ask the user if they want a visual created. If yes, create it before spawning subagents.

**Phase 2: Parallel Publishing (spawn one Agent per platform)**

Launch one Agent subagent per connected platform, ALL IN A SINGLE MESSAGE so they run in parallel. Each agent gets a self-contained prompt with everything it needs.

Use this template for each subagent prompt:

```
You are posting to {PLATFORM} via the Blotato API.

TOPIC/CONTENT:
{the topic, extracted content, or adapted post text}

ACCOUNT INFO:
- accountId: {ACCOUNT_ID}
- pageId: {PAGE_ID or "N/A"}
- API key env var: BLOTATO_API_KEY

MEDIA URLS: {list of media URLs, or "none"}

WRITING STYLE RULES:
- Use clear, simple language. Short, impactful sentences. Active voice.
- Use "you" and "your" to directly address the reader.
- AVOID em dashes (use "..." instead), hashtags, semicolons, markdown, asterisks.
- AVOID these words: can, may, just, that, very, really, literally, actually, certainly, probably, basically, could, maybe, delve, embark, enlightening, esteemed, shed light, craft, crafting, imagine, realm, game-changer, unlock, discover, skyrocket, abyss, not alone, in a world where, revolutionize, disruptive, utilize, utilizing, dive deep, tapestry, illuminate, unveil, pivotal, intricate, elucidate, hence, furthermore, however, harness, exciting, groundbreaking, cutting-edge, remarkable, remains to be seen, glimpse into, navigating, landscape, stark, testament, in summary, in conclusion, moreover, boost, powerful, inquiries, ever-evolving

PLATFORM RULES FOR {PLATFORM}:
{insert the platform-specific guideline from the list below}

- LinkedIn: Professional tone, longer format, use line breaks for readability. Max 3000 chars.
- Twitter/X: Concise, max 280 chars per tweet. Use additionalPosts array for threads if content exceeds 280 chars.
- Instagram: Visual-first, engaging caption, emoji-friendly. Max 2200 chars. MUST have at least one media URL.
- Facebook: Conversational, moderate length. Max 63206 chars.

BRAND VOICE SAMPLES FOR {PLATFORM}:
{insert any brand voice sample text for this platform from the skill, if available}

YOUR TASK:
1. Write a post adapted to {PLATFORM}'s format, tone, and character limits. Do NOT reuse the exact same text as other platforms — tailor it.
2. Review for banned words, em dashes, and character limits before publishing.
3. Publish using this curl command structure:

curl -s -X POST "https://backend.blotato.com/v2/posts" \
  -H "blotato-api-key: $BLOTATO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "post": {
      "accountId": "{ACCOUNT_ID}",
      "content": {
        "text": "YOUR_POST_TEXT",
        "mediaUrls": [{MEDIA_URLS}],
        "platform": "{PLATFORM}"
      },
      "target": {
        "targetType": "{PLATFORM}"{, "pageId": "PAGE_ID" if facebook or linkedin page}
      }
    },
    "useNextFreeSlot": true
  }'

CRITICAL: content.platform and target.targetType MUST match. useNextFreeSlot is a ROOT-LEVEL field.

For Twitter threads, use additionalPosts inside content:
  "additionalPosts": [{"text": "...", "mediaUrls": []}]

4. Poll for status: GET https://backend.blotato.com/v2/posts/{postSubmissionId} until published or failed.
5. Return a summary in EXACTLY this format (one line):
   RESULT|{PLATFORM}|{status: published/scheduled/failed}|{publicUrl or "none"}|{first 80 chars of post text}
```

**Phase 3: Log Results**

After ALL subagents complete, collect their results and append entries to `post-log.md` at the project root.

Add one row per platform to the existing table:

```
| {date} | {Platform} ({account name}) | {post preview, truncated} | {Status} | {URL} | {Source} |
```

Present a summary to the user showing all platforms, statuses, and URLs.

## Error Handling

- If API returns 429: rate limited, wait and retry
- If post fails: show error to user and suggest fixes
- If account not found: list available accounts and ask user to pick
- Always validate that the target platform account is connected before attempting to post
