#!/bin/bash
# Custom status line for Claude Code
# Shows model and token usage

# Get environment variables passed by Claude Code
MODEL="${CLAUDE_MODEL:-}"
TOKENS_USED="${CLAUDE_TOKENS_USED:-0}"
TOKENS_TOTAL="${CLAUDE_TOKENS_TOTAL:-200000}"
TOKENS_REMAINING="${CLAUDE_TOKENS_REMAINING:-200000}"

# Calculate percentage
if [ "$TOKENS_TOTAL" -gt 0 ]; then
    PERCENT=$((TOKENS_USED * 100 / TOKENS_TOTAL))
else
    PERCENT=0
fi

# Format numbers with commas
format_number() {
    printf "%'d" "$1" 2>/dev/null || echo "$1"
}

TOKENS_USED_FMT=$(format_number $TOKENS_USED)
TOKENS_REMAINING_FMT=$(format_number $TOKENS_REMAINING)
TOKENS_TOTAL_FMT=$(format_number $TOKENS_TOTAL)

# Build status line
echo "📊 Model: ${MODEL} | Tokens: ${TOKENS_USED_FMT}/${TOKENS_TOTAL_FMT} (${PERCENT}% used) | Remaining: ${TOKENS_REMAINING_FMT}"
