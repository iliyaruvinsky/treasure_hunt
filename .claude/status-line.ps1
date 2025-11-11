# Custom status line for Claude Code (PowerShell version)
# Shows model and token usage

# Get environment variables passed by Claude Code
$MODEL = $env:CLAUDE_MODEL
if (-not $MODEL) { $MODEL = "Unknown" }

$TOKENS_USED = $env:CLAUDE_TOKENS_USED
if (-not $TOKENS_USED) { $TOKENS_USED = 0 } else { $TOKENS_USED = [int]$TOKENS_USED }

$TOKENS_TOTAL = $env:CLAUDE_TOKENS_TOTAL
if (-not $TOKENS_TOTAL) { $TOKENS_TOTAL = 200000 } else { $TOKENS_TOTAL = [int]$TOKENS_TOTAL }

$TOKENS_REMAINING = $env:CLAUDE_TOKENS_REMAINING
if (-not $TOKENS_REMAINING) { $TOKENS_REMAINING = 200000 } else { $TOKENS_REMAINING = [int]$TOKENS_REMAINING }

# Calculate percentage
if ($TOKENS_TOTAL -gt 0) {
    $PERCENT = [math]::Round(($TOKENS_USED * 100.0 / $TOKENS_TOTAL), 1)
} else {
    $PERCENT = 0
}

# Format numbers with commas
$TOKENS_USED_FMT = "{0:N0}" -f $TOKENS_USED
$TOKENS_REMAINING_FMT = "{0:N0}" -f $TOKENS_REMAINING
$TOKENS_TOTAL_FMT = "{0:N0}" -f $TOKENS_TOTAL

# Build and output status line
Write-Output "📊 Model: $MODEL | Tokens: $TOKENS_USED_FMT/$TOKENS_TOTAL_FMT ($PERCENT% used) | Remaining: $TOKENS_REMAINING_FMT"
