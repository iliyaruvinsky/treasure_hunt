slca# StatusLine Variations Plugin

Professional statusline configurations for Claude Code with multiple presets designed for DevOps teams and developers who need better visibility into their AI coding sessions.

## Overview

This plugin provides three statusline variations, each designed for different use cases:

1. **Minimal** - Clean, distraction-free view
2. **Developer** - Balanced view with git integration
3. **Detailed** - Full DevOps visibility with cost tracking

## Features

- **Time Display** - Always know when you started your session
- **Model Information** - See which Claude model you're using
- **Git Branch Tracking** - Stay aware of your current branch
- **Cost Monitoring** - Track session costs in real-time (USD)
- **User Context** - Display current username
- **PowerShell Implementation** - Native Windows support with cross-platform potential

## Installation

### Automatic Installation (Recommended)

```bash
# Install from Skywind Plugin Marketplace
# (Requires marketplace configuration in .claude/settings.json)
```

### Manual Installation

1. Copy the desired statusline script to your `.claude` directory:
   ```powershell
   # For detailed view (recommended)
   Copy-Item statusline-detailed.ps1 .claude/statusline.ps1
   ```

2. Update your `.claude/settings.json`:
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "powershell -NoProfile -File \".claude\\statusline.ps1\""
     }
   }
   ```

## Variations

### 1. Minimal (`statusline-minimal.ps1`)

**Output:** `02:15PM | Sonnet 4.5`

**Use Case:**
- Focused work sessions where you want minimal distractions
- Quick coding tasks
- When screen real estate is limited

**Configuration:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "powershell -NoProfile -File \".claude\\statusline-scripts\\statusline-minimal.ps1\""
  }
}
```

### 2. Developer (`statusline-developer.ps1`)

**Output:** `02:15PM | Sonnet 4.5 | USER [GitBranch: main]`

**Use Case:**
- Standard development work
- Teams using git flow or feature branches
- When you need branch awareness without extra noise

**Configuration:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "powershell -NoProfile -File \".claude\\statusline-scripts\\statusline-developer.ps1\""
  }
}
```

### 3. Detailed (`statusline-detailed.ps1`)

**Output:** `02:15PM | Sonnet 4.5 | USER [GitBranch: main] | Cost: $0.0234`

**Use Case:**
- DevOps teams monitoring AI usage costs
- Enterprise environments with budget tracking requirements
- Long-running sessions where cost awareness is important
- Teams that need comprehensive session visibility

**Configuration:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "powershell -NoProfile -File \".claude\\statusline-scripts\\statusline-detailed.ps1\""
  }
}
```

## Understanding Cost Tracking

The cost displayed in the detailed variation represents:
- **Cumulative session cost** - Total USD spent since session start
- **Real-time updates** - Updates approximately every 300ms
- **API call tracking** - Based on actual token usage and model pricing
- **Session scope** - Resets when you start a new Claude Code session

**Note:** Cost tracking may show $0.0000 at the start of a session and will update as API calls are made.

## Customization

### Modifying Scripts

All scripts are PowerShell-based and can be customized. Common modifications:

1. **Change time format:**
   ```powershell
   $time = Get-Date -Format 'HH:mm:ss'  # 24-hour format with seconds
   ```

2. **Add custom information:**
   ```powershell
   $projectName = Split-Path -Leaf (Get-Location)
   Write-Output "$time | $model | $projectName"
   ```

3. **Change cost format:**
   ```powershell
   $cost = if ($input.cost.total_cost_usd) {
     '{0:C}' -f $input.cost.total_cost_usd  # Currency format
   } else { '$0.00' }
   ```

### Creating Your Own Variation

1. Copy an existing script as a template
2. Modify the output format
3. Update your `.claude/settings.json` to point to your custom script

## Troubleshooting

### StatusLine Not Appearing

- Ensure the script path is correct in settings.json
- Check that PowerShell can execute the script: `powershell -NoProfile -File ".claude\statusline.ps1"`
- Verify the script has proper line endings (CRLF for Windows)

### Cost Shows $0.0000

- This is normal at session start
- Cost accumulates as you use Claude Code
- If it remains $0 after significant usage, the cost tracking API may not be populating the data yet

### Git Branch Not Showing

- Ensure you're in a git repository
- The script defaults to "main" if no branch is detected
- Check git is accessible: `git branch --show-current`

## Platform Compatibility

- **Windows**: Fully supported (PowerShell native)
- **Linux/Mac**: Requires PowerShell Core installation or conversion to bash scripts

## DevOps Best Practices

### Team Standardization

Create a team-wide default by committing the configuration to your repository:

```json
// .claude/settings.json (committed to repo)
{
  "statusLine": {
    "type": "command",
    "command": "powershell -NoProfile -File \".claude\\statusline-scripts\\statusline-detailed.ps1\""
  }
}
```

### Cost Monitoring

For teams monitoring AI costs:
1. Use the **Detailed** variation
2. Document session costs in pull requests
3. Set up cost alerts based on statusline readings
4. Track costs across team members and projects

### Branch Strategy Integration

For teams using git-flow:
1. Use **Developer** or **Detailed** variations
2. StatusLine helps prevent commits to wrong branches
3. Provides quick visual confirmation of current context

## JSON Input Fields

The statusline scripts receive JSON input with the following structure:

```json
{
  "session_id": "...",
  "model": {
    "id": "claude-sonnet-4-5-20250929",
    "display_name": "Sonnet 4.5"
  },
  "cost": {
    "total_cost_usd": 0.0234,
    "total_duration_ms": 45000,
    "total_lines_added": 156,
    "total_lines_removed": 23
  },
  "workspace": {
    "current_dir": "/path/to/project",
    "project_dir": "/path/to/project"
  }
}
```

You can access any of these fields to create custom statusline variations.

## Contributing

Contributions are welcome! Ideas for new variations:
- **Compact** - Ultra-short format for small terminals
- **Multilingual** - Support for non-English labels
- **Color-coded** - Using ANSI colors for different states
- **Performance** - Including API duration metrics
- **Session** - Showing session duration and activity

## License

MIT License - See LICENSE file for details

## Author

Skywind Platform DevOps Team
- Email: devops@skywind.com
- Repository: https://github.com/iliyaruvinsky/skywind-plugin-marketplace

## Version History

See CHANGELOG.md for detailed version history.
