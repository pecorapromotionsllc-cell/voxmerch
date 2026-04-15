# AI Social Media Manager

This project is an AI-powered social media content pipeline for VoxMerch. It drafts, validates, and publishes posts across connected platforms using the Blotato API.

## API

- **Blotato API docs**: https://help.blotato.com/api/llm
- **API key**: stored in `.claude/settings.local.json` under `env.BLOTATO_API_KEY`. Reference it as `$BLOTATO_API_KEY` in curl commands.
- **curl convention**: always pass JSON payloads inline with `-d '{...}'`. Do not use heredocs, temp files, or `--data @file` for API calls.

## Key Files

- `.claude/skills/post/SKILL.md` — single-post publishing skill (includes brand voice rules and writing style guidelines)
- `.claude/skills/plan-week/SKILL.md` — weekly content planning skill
- `.claude/hooks/validate-post.sh` — quality gate hook that validates posts before publishing
- `.claude/settings.json` — hook config and permissions
- `post-log.md` — running log of all published/scheduled posts with dates, platforms, statuses, and URLs

## Brand Voice

Brand voice rules and writing samples live in `.claude/skills/post/SKILL.md` under "WRITING STYLE" and "BRAND VOICE SAMPLES." All skills reference these same rules. Key points:

- Clear, simple language. Short sentences. Active voice.
- Address the reader with "you" and "your."
- No em dashes. Use commas, periods, or "..." instead.
- No hashtags, semicolons, markdown, or asterisks in post text.
- Avoid banned words list (see SKILL.md for the full list).
- Platform-specific voice samples are in the same file under each platform heading.

## Quality Gate

`.claude/hooks/validate-post.sh` runs as a PreToolUse hook on every Bash command. It intercepts curl calls to the Blotato posts endpoint and checks:

1. Em dashes / en dashes
2. Character limits per platform (Twitter 280, LinkedIn 3000, Instagram 2200, Facebook 63206)
3. Missing media URLs for Instagram
4. Banned words and phrases

If any check fails, the hook blocks the command and prints the violations. Fix the post content and retry.

## Blotato API Patterns

### Connected accounts
```
GET /v2/users/me/accounts
```
For LinkedIn pages and Facebook pages, fetch the pageId via:
```
GET /v2/users/me/accounts/{accountId}/subaccounts
```

### Content extraction (YouTube, TikTok, articles, PDFs, audio)
```
POST /v2/source-resolutions-v3
Body: { "source": { "sourceType": "youtube", "url": "..." } }
```
Poll `GET /v2/source-resolutions-v3/{id}` until status is no longer "in-progress."

### Publishing
```
POST /v2/posts
```
Critical rules:
- `content.platform` and `target.targetType` must match.
- `useNextFreeSlot` and `scheduledTime` are root-level fields, siblings of `"post"`, not nested inside it.
- For Facebook and LinkedIn pages, include `"pageId"` in `target`.
- Default to `"useNextFreeSlot": true` unless the user says otherwise.

### Visual generation
```
GET /v2/videos/templates — list templates
POST /v2/videos/from-templates — generate visual (use bare UUID for templateId, empty inputs, prompt for AI fill)
GET /v2/videos/creations/{id} — poll until status is "done"
```

## Conventions

- Log every published or scheduled post to `post-log.md` with date, platform, content preview, status, URL, and source.
- When posting to multiple platforms, use parallel subagents (one per platform) for efficiency.
- When planning a week, write the plan to `content-plan.md`, get user approval, then publish.
- Adapt post text per platform. Never copy-paste identical text across platforms.
