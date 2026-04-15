#!/usr/bin/env bash
# Hook: validate Blotato post content before curl commands
# Triggered by PreToolUse on Bash commands containing curl + backend.blotato.com/v2/posts

set -euo pipefail

INPUT=$(cat)

# Extract the bash command from the hook input
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only check curl commands targeting the posts endpoint
if [[ -z "$COMMAND" ]]; then
  exit 0
fi

if ! echo "$COMMAND" | grep -q "curl" || ! echo "$COMMAND" | grep -q "backend.blotato.com/v2/posts"; then
  exit 0
fi

# Extract the JSON body from the curl command (-d or --data or --data-raw)
JSON_BODY=$(echo "$COMMAND" | grep -oP "(?<=-d\s')[^']*|(?<=--data\s')[^']*|(?<=--data-raw\s')[^']*|(?<=-d\s\")[^\"]+" || true)

if [[ -z "$JSON_BODY" ]]; then
  # Try extracting from heredoc or $'...' style
  JSON_BODY=$(echo "$COMMAND" | grep -oP "(?<=--data-raw\s\\$')[^']*|(?<=--data\s\\$')[^']*" || true)
fi

if [[ -z "$JSON_BODY" ]]; then
  exit 0
fi

ERRORS=""

# Extract main post text
POST_TEXT=$(echo "$JSON_BODY" | jq -r '.post.content.text // empty' 2>/dev/null || true)
PLATFORM=$(echo "$JSON_BODY" | jq -r '.post.content.platform // empty' 2>/dev/null || true)
MEDIA_URLS=$(echo "$JSON_BODY" | jq -r '.post.content.mediaUrls // [] | length' 2>/dev/null || echo "0")

# Also gather additional posts text for thread validation
ADDITIONAL_TEXTS=$(echo "$JSON_BODY" | jq -r '.post.content.additionalPosts[]?.text // empty' 2>/dev/null || true)

ALL_TEXT="$POST_TEXT"
if [[ -n "$ADDITIONAL_TEXTS" ]]; then
  ALL_TEXT="$POST_TEXT
$ADDITIONAL_TEXTS"
fi

if [[ -z "$POST_TEXT" ]]; then
  exit 0
fi

# ── CHECK 1: Em dashes ──
if echo "$ALL_TEXT" | grep -qP '\x{2014}|\x{2013}|—|–'; then
  ERRORS+="EM DASH DETECTED: Replace em dashes (—) or en dashes (–) with \"...\" per brand voice rules.
"
  # Show which lines contain them
  LINES_WITH_DASHES=$(echo "$ALL_TEXT" | grep -nP '\x{2014}|\x{2013}|—|–' || true)
  if [[ -n "$LINES_WITH_DASHES" ]]; then
    ERRORS+="  Found in: $LINES_WITH_DASHES
"
  fi
fi

# ── CHECK 2: Character limits ──
CHAR_COUNT=${#POST_TEXT}

case "$PLATFORM" in
  twitter)
    if [[ $CHAR_COUNT -gt 280 ]]; then
      ERRORS+="CHARACTER LIMIT EXCEEDED: Twitter post is ${CHAR_COUNT} chars (max 280). Use additionalPosts for threads.
"
    fi
    # Check each additional post too
    if [[ -n "$ADDITIONAL_TEXTS" ]]; then
      POST_NUM=1
      while IFS= read -r additional_text; do
        POST_NUM=$((POST_NUM + 1))
        ADDITIONAL_LEN=${#additional_text}
        if [[ $ADDITIONAL_LEN -gt 280 ]]; then
          ERRORS+="CHARACTER LIMIT EXCEEDED: Twitter thread post ${POST_NUM} is ${ADDITIONAL_LEN} chars (max 280).
"
        fi
      done <<< "$ADDITIONAL_TEXTS"
    fi
    ;;
  linkedin)
    if [[ $CHAR_COUNT -gt 3000 ]]; then
      ERRORS+="CHARACTER LIMIT EXCEEDED: LinkedIn post is ${CHAR_COUNT} chars (max 3000).
"
    fi
    ;;
  instagram)
    if [[ $CHAR_COUNT -gt 2200 ]]; then
      ERRORS+="CHARACTER LIMIT EXCEEDED: Instagram caption is ${CHAR_COUNT} chars (max 2200).
"
    fi
    ;;
  facebook)
    if [[ $CHAR_COUNT -gt 63206 ]]; then
      ERRORS+="CHARACTER LIMIT EXCEEDED: Facebook post is ${CHAR_COUNT} chars (max 63206).
"
    fi
    ;;
esac

# ── CHECK 3: Missing media URLs for platforms that require them ──
if [[ "$PLATFORM" == "instagram" && "$MEDIA_URLS" -eq 0 ]]; then
  ERRORS+="MISSING MEDIA: Instagram requires at least one media URL in mediaUrls[].
"
fi

# ── CHECK 4: Banned words ──
BANNED_WORDS=(
  "can" "may" "just" "that" "very" "really" "literally" "actually"
  "certainly" "probably" "basically" "could" "maybe"
  "delve" "embark" "enlightening" "esteemed"
  "craft" "crafting" "imagine" "realm" "game-changer"
  "unlock" "discover" "skyrocket" "abyss"
  "revolutionize" "disruptive"
  "utilize" "utilizing"
  "tapestry" "illuminate" "unveil" "pivotal" "intricate" "elucidate"
  "hence" "furthermore" "however" "harness"
  "exciting" "groundbreaking" "cutting-edge" "remarkable"
  "boost" "powerful" "inquiries" "ever-evolving"
)

BANNED_PHRASES=(
  "shed light"
  "not alone"
  "in a world where"
  "dive deep"
  "remains to be seen"
  "glimpse into"
  "navigating"
  "landscape"
  "stark"
  "testament"
  "in summary"
  "in conclusion"
  "moreover"
)

# Convert post text to lowercase for matching
ALL_TEXT_LOWER=$(echo "$ALL_TEXT" | tr '[:upper:]' '[:lower:]')

FOUND_BANNED=""

for word in "${BANNED_WORDS[@]}"; do
  # Word boundary match (whole words only)
  if echo "$ALL_TEXT_LOWER" | grep -qPi "\b${word}\b"; then
    FOUND_BANNED+="  - \"${word}\"
"
  fi
done

for phrase in "${BANNED_PHRASES[@]}"; do
  if echo "$ALL_TEXT_LOWER" | grep -qi "$phrase"; then
    FOUND_BANNED+="  - \"${phrase}\"
"
  fi
done

if [[ -n "$FOUND_BANNED" ]]; then
  ERRORS+="BANNED WORDS/PHRASES FOUND (per brand voice guidelines):
${FOUND_BANNED}"
fi

# ── Output result ──
if [[ -n "$ERRORS" ]]; then
  echo "BLOCKED" >&2
  echo "" >&2
  echo "Post validation failed. Fix the following before posting:" >&2
  echo "────────────────────────────────────────────────────────" >&2
  echo "$ERRORS" >&2
  echo "────────────────────────────────────────────────────────" >&2
  echo "Platform: $PLATFORM | Characters: $CHAR_COUNT | Media URLs: $MEDIA_URLS" >&2
  exit 2
fi

exit 0
