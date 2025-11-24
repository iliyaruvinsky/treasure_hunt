# CLAUDE.md - AI Assistant Guide for Skywind Repository

**Version:** 1.0.0
**Last Updated:** 2025-11-24
**Repository:** Skywind Plugin Marketplace & SAP Treasure Hunt

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Key Components](#key-components)
4. [Development Workflows](#development-workflows)
5. [Plugin Development Guidelines](#plugin-development-guidelines)
6. [Content Management](#content-management)
7. [Git Workflow](#git-workflow)
8. [Testing & Quality Assurance](#testing--quality-assurance)
9. [Common Tasks](#common-tasks)
10. [AI Assistant Behavior Rules](#ai-assistant-behavior-rules)

---

## 🎯 Project Overview

This repository serves **two primary purposes**:

### 1. Skywind Plugin Marketplace
A centralized marketplace for AI coding assistant plugins that work across multiple tools (Claude Code, Cursor, Windsurf). The marketplace provides reusable rule sets to:
- Reduce AI hallucinations
- Enforce code quality standards
- Standardize development workflows
- Improve AI accuracy and consistency

### 2. SAP Treasure Hunt Campaign
Marketing and sales content for Skywind's SAP assessment offering, including:
- Landing pages for SAP optimization services
- Case studies and client success stories
- ROI calculators and cost-saving documentation
- Campaign materials and email templates

### Technology Stack
- **Languages:** Bash, PowerShell, JavaScript (Node.js), HTML/CSS
- **Formats:** Markdown, JSON, DOCX, PDF
- **Version Control:** Git
- **Target Platforms:** Claude Code, Cursor, Windsurf, Cline, Aider

---

## 📁 Repository Structure

```
treasure_hunt/
├── .claude/                          # Claude Code configuration
│   └── rules/                        # Claude-specific rule files
│       └── strict-verification.md    # Anti-hallucination rules
│
├── .cursorrules                      # Cursor AI configuration (flat file)
│
├── About Us/                         # Skywind company information
│   ├── about-us.md
│   ├── Enhanced_About_Us_Skywind.md
│   └── [other marketing content]
│
├── MAIN PAGE/                        # SAP campaign content
│   ├── Cost Savings/                 # Cost-reduction documentation
│   │   ├── ReadMore_*.md             # Detailed cost-saving topics
│   │   ├── Cost Saving stories and examples/
│   │   │   ├── Alert Stories and Case Studies/
│   │   │   └── Brochures/
│   │   └── Strategic Cost Reduction Areas with Skywind SAP Optimization.md
│   │
│   ├── Empowering Every Role in the SAP Ecosystem/
│   │   ├── Role_Based_Solutions_Mapping.md
│   │   └── Web_Designer_Ready_4_Blocks.md
│   │
│   ├── Reveal Your SAP Vulnerabilities/
│   │   └── Streamlined SAP Vulnerability Assessment Landing Page.md
│   │
│   └── [various SAP topic files]
│
├── SoDA-Email-Templates-main/       # Email campaign templates
│   ├── examples/
│   └── README.md
│
├── cursor/                           # Cursor-specific files
│   └── rules.md
│
├── plugins/                          # Plugin marketplace
│   ├── anti-hallucination/          # Accuracy & verification plugins
│   │   └── strict-verification/
│   │       ├── plugin.json          # Plugin metadata
│   │       ├── rules.md             # Universal rules
│   │       ├── README.md            # Documentation
│   │       └── CHANGELOG.md         # Version history
│   │
│   ├── devops-tools/                # DevOps utilities
│   │   └── statusline-variations/
│   │
│   └── marketplace-tools/           # Marketplace development tools
│       └── plugin-development-agent/
│           ├── plugin.json
│           ├── rules.md
│           ├── README.md
│           └── CHANGELOG.md
│
├── scripts/                          # Installation & utility scripts
│   ├── install.sh                    # Unix/Mac plugin installer
│   ├── install.ps1                   # Windows plugin installer
│   └── list-plugins.js               # Plugin browser/lister
│
├── CONTRIBUTING.md                   # Plugin contribution guide
├── plugin-schema.json                # JSON schema for plugin metadata
├── README.md                         # Main repository documentation
├── SKYWIND-PLUGIN-MARKETPLACE-STRUCTURE.md  # Marketplace architecture
├── SEE-IT-IN-ACTION-README.md       # Landing page documentation
├── see-it-in-action.html            # Interactive demo landing page
│
└── [Various SAP content files]       # Additional marketing materials
    ├── ReadMore_*.md                 # Topic deep-dives
    ├── CONTENT-FOR-WEB-DESIGNER.md   # Web design specifications
    ├── Integrated_SAP_Treasure_Hunt_Landing_Page.md
    ├── Treasure_Hunt_*.docx/pdf      # Campaign materials
    └── [other files]
```

---

## 🔑 Key Components

### 1. Plugin System

#### Plugin Structure (Standard)
Every plugin follows this structure:
```
plugins/<category>/<plugin-name>/
├── plugin.json      # Metadata (required)
├── rules.md         # Universal rules (required)
├── README.md        # Documentation (required)
└── CHANGELOG.md     # Version history (required)
```

#### Plugin Metadata (`plugin.json`)
Conforms to `plugin-schema.json` with required fields:
- `id`: `"category/plugin-name"` format
- `name`: Human-readable name
- `version`: Semantic versioning (e.g., `"1.0.0"`)
- `description`: 10-200 character summary
- `category`: One of the predefined categories
- `compatibility`: Boolean flags for each AI tool
- `author`: Name, email, optional URL

#### Categories
- `anti-hallucination`: Accuracy and verification rules
- `code-quality`: Clean code and maintainability
- `security`: Secure coding practices
- `workflow`: Git, CI/CD, PR standards
- `performance`: Optimization guidelines
- `testing`: TDD, test coverage, QA
- `documentation`: Documentation standards
- `marketplace-tools`: Meta-tools for marketplace development
- `devops-tools`: DevOps utilities

### 2. Installation Scripts

#### `scripts/install.sh` (Unix/Mac)
```bash
./scripts/install.sh <plugin-id> [--tool <tool-name>] [--target <target-dir>]
```

#### `scripts/install.ps1` (Windows)
```powershell
.\scripts\install.ps1 -PluginId <plugin-id> [-Tool <tool-name>] [-Target <target-dir>]
```

#### Supported Tools
- `claude-code` (default): Installs to `.claude/rules/`
- `cursor`: Appends to `.cursorrules`
- `windsurf`: Installs to `.windsurf/rules/`

### 3. SAP Content Organization

#### Content Types
1. **Landing Pages**: Marketing pages for web designers (HTML + Markdown specs)
2. **Case Studies**: Real client examples (anonymized)
3. **ROI Documentation**: Cost-saving calculators and methodologies
4. **Email Templates**: Campaign outreach materials
5. **Topic Deep-Dives**: `ReadMore_*.md` files explaining specific SAP topics

#### Content Conventions
- **Anonymization**: Client names replaced with industry/region descriptors
- **Quantification**: All claims backed by specific numbers
- **Authenticity**: Real findings, no marketing fluff
- **Modularity**: Content organized by topic for reuse

---

## 🔄 Development Workflows

### Plugin Development Workflow

#### 1. Planning Phase
```bash
# Read the contribution guide
cat CONTRIBUTING.md

# Review existing plugins for patterns
ls -R plugins/

# Check plugin schema
cat plugin-schema.json
```

#### 2. Creation Phase
```bash
# Create plugin directory structure
mkdir -p plugins/<category>/<plugin-name>

# Create required files
touch plugins/<category>/<plugin-name>/plugin.json
touch plugins/<category>/<plugin-name>/rules.md
touch plugins/<category>/<plugin-name>/README.md
touch plugins/<category>/<plugin-name>/CHANGELOG.md
```

#### 3. Development Phase
1. Write `plugin.json` following the schema
2. Write `rules.md` with clear, actionable rules
3. Write `README.md` with installation & usage info
4. Initialize `CHANGELOG.md` with version 1.0.0

#### 4. Testing Phase
```bash
# Test installation
./scripts/install.sh <category>/<plugin-name> --tool claude-code

# Verify in target project
cd /path/to/test-project
cat .claude/rules/<plugin-name>.md

# Test with actual AI assistant
# (Manual: Use Claude Code/Cursor with the plugin installed)
```

#### 5. Documentation Phase
- Ensure README includes before/after examples
- Document all rules with WHY explanations
- Include compatibility matrix
- Add usage examples

### Content Update Workflow

#### For SAP Marketing Content
```bash
# 1. Read existing content to understand style/tone
cat "MAIN PAGE/[relevant-file].md"

# 2. Make updates maintaining consistency
# - Keep quantified benefits
# - Maintain anonymization
# - Use existing terminology

# 3. Update related files
# - Check for cross-references
# - Update summary documents if needed

# 4. Verify markdown formatting
# Use Read tool to verify changes
```

#### For Landing Pages
```bash
# 1. Update HTML if needed
# see-it-in-action.html

# 2. Update corresponding documentation
# SEE-IT-IN-ACTION-README.md

# 3. Test locally in browser
# (Open HTML file directly)
```

---

## 🔧 Plugin Development Guidelines

### Rule Writing Best Practices

#### ✅ DO: Be Specific and Actionable
```markdown
**ALWAYS verify file changes by reading the file after editing**
```

#### ❌ DON'T: Use Vague Language
```markdown
"Try to write good code"
```

#### ✅ DO: Use Strong Imperatives
Use words like: **MUST**, **ALWAYS**, **NEVER**, **REQUIRED**, **MANDATORY**

#### ✅ DO: Explain the "Why"
```markdown
### Rule: Verify Before Claiming
- NEVER report success without verification
- WHY: Unverified claims waste user time and money
```

#### ✅ DO: Provide Examples
```markdown
❌ Bad: "I've updated the file"
✅ Good: "Let me verify the update... Confirmed: file updated"
```

#### ✅ DO: Make Rules Measurable
AI should be able to determine compliance objectively.

### Plugin Metadata Best Practices

#### Version Numbers (Semantic Versioning)
- **MAJOR** (2.0.0): Breaking changes to rules
- **MINOR** (1.1.0): New rules added (backwards compatible)
- **PATCH** (1.0.1): Bug fixes, typos, clarifications

#### Compatibility Testing
Mark compatibility as `true` ONLY after actual testing:
```json
{
  "compatibility": {
    "claudeCode": true,  // ← Tested and works
    "cursor": true,      // ← Tested and works
    "windsurf": false,   // ← Not yet tested
    "copilot": false     // ← Not compatible
  }
}
```

#### Keywords for Discovery
Choose 5-10 keywords that users might search for:
```json
{
  "keywords": [
    "verification",
    "accuracy",
    "hallucination",
    "testing",
    "truth",
    "honest-reporting"
  ]
}
```

### Plugin Categories and Tags

#### Category Selection
Choose the PRIMARY purpose:
- If a plugin does multiple things, pick the most important
- Consider creating separate plugins if purposes are distinct

#### Tag Selection
Available tags:
- `stable`: Production-ready
- `recommended`: Strongly suggested for most projects
- `experimental`: Beta/testing phase
- `beginner-friendly`: Easy to understand and use
- `advanced`: For experienced users
- `enterprise`: Suitable for large organizations
- `strict`: Enforces rules rigidly
- `flexible`: Allows some discretion

---

## 📝 Content Management

### SAP Content Principles

#### 1. Authenticity First
- Use REAL client examples (anonymized)
- Include ACTUAL dollar amounts saved
- Reference SPECIFIC findings from assessments
- No hypotheticals or simulations

#### 2. Quantification Required
Every claim should have numbers:
- ✅ "$105K annual waste eliminated"
- ✅ "1,200 hours/year saved"
- ❌ "Significant savings achieved"

#### 3. Anonymization Standards
- Client names → "Financial Services • Middle East"
- Specific locations → General regions
- Exact dates → Relative timeframes
- Personal names → Role titles

#### 4. Content Reusability
Structure content for multiple uses:
- Standalone markdown files for each topic
- `ReadMore_*.md` pattern for deep-dives
- Modular case studies in arrays
- Cross-reference related content

### Content File Naming Conventions

#### Pattern: PascalCase with Underscores
```
ReadMore_AccessGovernance.md
ReadMore_BusinessControl.md
Treasure_Hunt_Findings_Report.pdf
Strategic_Cost_Savings_Landing_Page.md
```

#### Directory Names
- Space-separated for readability: `Cost Savings/`
- Descriptive hierarchy: `MAIN PAGE/Cost Savings/Cost Saving stories and examples/`

### Updating Case Studies

Location: `see-it-in-action.html` → `caseStudies` array

```javascript
const caseStudies = [
    {
        id: 1,
        category: 'fraud',                    // Filter category
        categoryDisplay: 'Business Protection', // Display name
        industry: 'Financial Services • Middle East',
        headline: 'The Quarterly Bank Account Fraud',
        impact: 'Multiple quarters of theft stopped',
        tags: ['fraud', 'vendor'],            // For filtering
        details: {
            discovery: '...',                  // Full story
            detection: '...',                  // How Skywind found it
            impactDetails: '...',              // Business impact
            quote: '...'                       // Client testimonial
        }
    },
    // ... more studies
];
```

---

## 🔀 Git Workflow

### Branch Strategy

#### Main Branch
- **Name**: Not explicitly defined in repo (check with `git branch`)
- **Purpose**: Stable, production-ready code
- **Protection**: Should require PR review (verify with team)

#### Feature Branches
**Naming Convention:**
```bash
# For plugins
git checkout -b plugin/category/plugin-name

# For content updates
git checkout -b content/topic-description

# For bug fixes
git checkout -b fix/brief-description

# For documentation
git checkout -b docs/what-changed
```

#### Current Working Branch
```
claude/claude-md-mid28tdkw5oxfru8-01WUtmVaMmnGqRnnxqcoLEes
```
This is a Claude-specific branch for this session.

### Commit Message Conventions

#### Format
```
<type>: <subject>

<body (optional)>
```

#### Types
- `feat:` New feature (plugin, content, script)
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code restructuring without behavior change
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

#### Examples
```bash
# Good commit messages
git commit -m "feat: Add Plugin Development Agent to marketplace"
git commit -m "docs: Update README with clearer DevOps installation instructions"
git commit -m "fix: Correct plugin schema validation for compatibility field"

# Poor commit messages (avoid)
git commit -m "updates"
git commit -m "fixed stuff"
git commit -m "WIP"
```

### Git Operations Best Practices

#### Push with Retry Logic
Network failures can occur. The system implements:
```bash
# Automatic retry with exponential backoff
# 1st attempt: immediate
# 2nd attempt: 2s wait
# 3rd attempt: 4s wait
# 4th attempt: 8s wait
# 5th attempt: 16s wait (final)
```

#### Branch Naming for Automated Pushes
- Must start with `claude/`
- Must end with matching session ID
- Otherwise: 403 HTTP error on push

#### Fetch/Pull Operations
```bash
# Prefer specific branches
git fetch origin <branch-name>
git pull origin <branch-name>

# Same retry logic applies
```

---

## ✅ Testing & Quality Assurance

### Plugin Testing Checklist

#### Pre-Installation Testing
- [ ] `plugin.json` validates against `plugin-schema.json`
- [ ] All required files present (plugin.json, rules.md, README.md, CHANGELOG.md)
- [ ] Version follows semantic versioning
- [ ] `id` field matches directory path

#### Installation Testing
```bash
# Test each supported tool
./scripts/install.sh <plugin-id> --tool claude-code
./scripts/install.sh <plugin-id> --tool cursor
./scripts/install.sh <plugin-id> --tool windsurf

# Verify files created in correct locations
ls -la .claude/rules/
cat .cursorrules
ls -la .windsurf/rules/
```

#### Functional Testing
1. Install plugin in a test project
2. Start AI assistant (Claude Code/Cursor/Windsurf)
3. Perform actions the plugin should affect
4. Verify AI follows the rules
5. Document behavior in README

#### Documentation Review
- [ ] README explains what the plugin does
- [ ] Installation instructions included
- [ ] Examples show before/after behavior
- [ ] Benefits clearly articulated
- [ ] Compatibility matrix accurate

### Content Testing Checklist

#### Markdown Validation
- [ ] No broken internal links
- [ ] Proper heading hierarchy (H1 → H2 → H3)
- [ ] Code blocks use correct syntax highlighting
- [ ] Lists formatted consistently

#### HTML/Web Content
- [ ] Opens correctly in major browsers
- [ ] Responsive on mobile devices
- [ ] All interactive elements work
- [ ] No console errors
- [ ] Links point to correct destinations

#### Factual Accuracy
- [ ] All numbers/statistics verified
- [ ] Client names properly anonymized
- [ ] Technical claims are accurate
- [ ] No outdated information

---

## 🚀 Common Tasks

### Task 1: Create a New Plugin

```bash
# 1. Choose category and name
CATEGORY="code-quality"
PLUGIN="clean-code-enforcer"

# 2. Create directory structure
mkdir -p plugins/$CATEGORY/$PLUGIN

# 3. Create files
cd plugins/$CATEGORY/$PLUGIN

# Create plugin.json
cat > plugin.json << 'EOF'
{
  "id": "code-quality/clean-code-enforcer",
  "name": "Clean Code Enforcer",
  "version": "1.0.0",
  "description": "Enforces clean code principles for maintainable software",
  "category": "code-quality",
  "compatibility": {
    "claudeCode": true,
    "cursor": true,
    "windsurf": false,
    "copilot": false
  },
  "author": {
    "name": "Your Name",
    "email": "your@email.com"
  },
  "keywords": ["clean-code", "maintainability", "standards"],
  "license": "MIT",
  "tags": ["stable", "recommended"],
  "createdAt": "2025-11-24T00:00:00Z",
  "updatedAt": "2025-11-24T00:00:00Z"
}
EOF

# Create rules.md
cat > rules.md << 'EOF'
# Clean Code Enforcer Rules

## RULE 1: Meaningful Names
- ALWAYS use descriptive variable and function names
- NEVER use single-letter names except in loops
...
EOF

# Create README.md
cat > README.md << 'EOF'
# Clean Code Enforcer

## Overview
This plugin enforces clean code principles...

## Installation
...
EOF

# Create CHANGELOG.md
cat > CHANGELOG.md << 'EOF'
# Changelog

## [1.0.0] - 2025-11-24

### Added
- Initial release
- Rule 1: Meaningful names
...
EOF

# 4. Test installation
cd ../../..
./scripts/install.sh code-quality/clean-code-enforcer

# 5. Commit
git add plugins/code-quality/clean-code-enforcer/
git commit -m "feat: Add Clean Code Enforcer plugin"
```

### Task 2: Update Existing Plugin

```bash
# 1. Read current plugin files
cat plugins/anti-hallucination/strict-verification/plugin.json
cat plugins/anti-hallucination/strict-verification/rules.md

# 2. Make changes to rules.md or other files
# (Use Edit tool)

# 3. Update version in plugin.json
# PATCH: 1.0.0 → 1.0.1 (typo fix)
# MINOR: 1.0.0 → 1.1.0 (new rule added)
# MAJOR: 1.0.0 → 2.0.0 (breaking change)

# 4. Update CHANGELOG.md
cat >> plugins/anti-hallucination/strict-verification/CHANGELOG.md << 'EOF'

## [1.1.0] - 2025-11-24

### Added
- New rule: XYZ

### Changed
- Clarified rule ABC
EOF

# 5. Update updatedAt timestamp in plugin.json

# 6. Test
./scripts/install.sh anti-hallucination/strict-verification

# 7. Commit
git add plugins/anti-hallucination/strict-verification/
git commit -m "feat: Add XYZ rule to strict-verification plugin (v1.1.0)"
```

### Task 3: Add SAP Case Study

```bash
# 1. Read existing case study structure
cat see-it-in-action.html | grep -A 20 "const caseStudies"

# 2. Edit HTML file to add new case study
# (Use Edit tool to add to caseStudies array)

# 3. Update documentation
cat >> SEE-IT-IN-ACTION-README.md << 'EOF'

11. **The [New Case Study Title]** - [Industry]
    - [Brief description]
    - [Impact quantified]
EOF

# 4. Test in browser
# (Open see-it-in-action.html)

# 5. Commit
git add see-it-in-action.html SEE-IT-IN-ACTION-README.md
git commit -m "feat: Add new case study - [Title]"
```

### Task 4: Update Marketing Content

```bash
# 1. Identify the content file
ls "MAIN PAGE/"
ls "MAIN PAGE/Cost Savings/"

# 2. Read existing content for style
cat "MAIN PAGE/ReadMore_AccessGovernance.md"

# 3. Make updates using Edit tool
# - Maintain quantification
# - Keep anonymization
# - Follow existing formatting

# 4. Update cross-references if needed
# Search for mentions of the updated content
grep -r "Access Governance" "MAIN PAGE/"

# 5. Commit
git add "MAIN PAGE/ReadMore_AccessGovernance.md"
git commit -m "docs: Update Access Governance content with latest findings"
```

### Task 5: List All Plugins

```bash
# Using the built-in script
node scripts/list-plugins.js

# Filter by category
node scripts/list-plugins.js --category anti-hallucination

# Manual listing
find plugins -name "plugin.json" -exec cat {} \; | grep -E '"id"|"name"|"description"'
```

### Task 6: Validate Plugin Structure

```bash
# Check required files exist
PLUGIN="anti-hallucination/strict-verification"
ls -la plugins/$PLUGIN/

# Expected output:
# plugin.json
# rules.md
# README.md
# CHANGELOG.md

# Validate JSON syntax
cat plugins/$PLUGIN/plugin.json | python -m json.tool

# Check version format
cat plugins/$PLUGIN/plugin.json | grep '"version"' | grep -E '"[0-9]+\.[0-9]+\.[0-9]+"'
```

---

## 🤖 AI Assistant Behavior Rules

### Universal Rules (Apply to All AI Assistants)

These rules are derived from the strict-verification plugin and represent the highest standards for AI assistant behavior in this repository.

#### RULE 1: VERIFY BEFORE CLAIMING
- **NEVER** report that a change was made unless you have READ THE FILE AFTERWARD to confirm
- **ALWAYS** use the Read tool IMMEDIATELY after any Edit or Write to verify the actual result
- **ONLY** report success after verification shows the change actually exists in the file
- **If** verification shows the change failed, ADMIT IT IMMEDIATELY and fix it properly

#### RULE 2: NO ASSUMPTIONS AS FACTS
- **NEVER** say "I have implemented" - instead say "I attempted to implement, let me verify"
- **NEVER** claim specific outcomes without reading actual file contents
- **ALWAYS** distinguish between "I tried to do X" and "I successfully completed X"
- **When** tools fail silently, ACKNOWLEDGE the failure instead of assuming success

#### RULE 3: MANDATORY VERIFICATION WORKFLOW
1. Execute change (Edit, Write, etc.)
2. IMMEDIATELY run Read to check actual result
3. Compare actual result with intended change
4. ONLY THEN report what actually happened
5. If change failed, try alternative method and repeat verification

#### RULE 4: HONEST REPORTING
- **NEVER** say "All files are updated" without reading each file to confirm
- **NEVER** report completion percentages without actual file verification
- **If** unsure about file state, READ THE FILE FIRST
- **When** caught in inaccuracy, ACKNOWLEDGE the error immediately and fix properly

#### RULE 5: COST CONSCIOUSNESS
- Remember user is paying for accurate work, not hallucinations
- Wasted iterations due to unverified claims cost real money
- Accuracy on first attempt is more valuable than speed with errors
- User's frustration is justified when paying for inaccurate reporting

#### RULE 6: TRUTH AS HIGHEST VALUE
- **TRUTH ABOVE ALL**: For the user, truth is of the highest value
- Honest uncertainty is more valuable than confident incorrectness
- Real problems require real solutions, not plausible-sounding evasions
- Admit uncertainty instead of making up plausible-sounding answers

#### RULE 7: NO "YESMAN" BEHAVIOR
- **DO NOT** be a "yesman" - Answer honestly and correctly, instead of "plausibly"
- If uncertain how to respond - provide HONEST answer, even if it's not promising or convenient
- Truth over politeness - even if the honest answer is disappointing
- Real limitations are more valuable than fake capabilities

### Repository-Specific Guidelines

#### When Working with Plugins
1. **ALWAYS** read the plugin schema before creating/modifying plugins
2. **ALWAYS** test installation after creating/modifying plugins
3. **ALWAYS** update version numbers according to semantic versioning
4. **ALWAYS** update CHANGELOG.md when changing plugins
5. **ALWAYS** verify compatibility claims through actual testing

#### When Working with SAP Content
1. **PRESERVE** anonymization in all client examples
2. **MAINTAIN** quantification - include specific numbers/dollar amounts
3. **VERIFY** cross-references when updating content
4. **FOLLOW** existing file naming conventions
5. **TEST** HTML/web content in browser after changes

#### When Working with Scripts
1. **READ** the entire script before modifying
2. **TEST** installation scripts with actual plugins
3. **PRESERVE** retry logic and error handling
4. **DOCUMENT** any new script functionality
5. **MAINTAIN** cross-platform compatibility (Unix/Windows)

### Context Management

#### Reading Files Strategically
- Read plugin schema BEFORE creating plugins
- Read existing similar content BEFORE creating new content
- Read CONTRIBUTING.md BEFORE submitting plugins
- Read related files to understand dependencies

#### Batch Operations
- When updating multiple files, verify EACH ONE individually
- Don't report "all files updated" until all are verified
- Provide specific status for each file

#### Error Recovery
- If Edit fails, try Read + Write approach
- If installation fails, check paths and permissions
- If git push fails, use retry logic (exponential backoff)

---

## 📚 Additional Resources

### Key Documentation Files
- `README.md` - Main repository overview
- `CONTRIBUTING.md` - Plugin contribution guidelines
- `SKYWIND-PLUGIN-MARKETPLACE-STRUCTURE.md` - Marketplace architecture
- `SEE-IT-IN-ACTION-README.md` - Landing page documentation
- `plugin-schema.json` - Plugin metadata specification

### Example Plugins to Study
- `plugins/anti-hallucination/strict-verification/` - Comprehensive anti-hallucination rules
- `plugins/marketplace-tools/plugin-development-agent/` - Meta-plugin for creating plugins

### External References
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [CommonMark Markdown Spec](https://commonmark.org/)
- [JSON Schema](https://json-schema.org/)

---

## 🔄 Maintenance

### Keeping CLAUDE.md Updated

This file should be updated when:
- [ ] New plugin categories are added
- [ ] Repository structure changes significantly
- [ ] New development workflows are established
- [ ] Git branch strategy changes
- [ ] New AI assistant behavior rules are discovered
- [ ] Installation scripts are modified
- [ ] Major content reorganization occurs

**Last Review:** 2025-11-24
**Next Review:** After major repository changes

---

## 📞 Support & Questions

### For Plugin-Related Questions
- Review: `CONTRIBUTING.md`
- Check: Existing plugins in `plugins/` directory
- Reference: `plugin-schema.json`

### For SAP Content Questions
- Review: Existing content in `MAIN PAGE/`
- Check: `ReadMore_*.md` files for examples
- Reference: `see-it-in-action.html` for case study format

### For Git/Workflow Questions
- Review: This file (CLAUDE.md) - Git Workflow section
- Check: `.git/config` for remote setup
- Reference: Recent commit history for patterns

---

**End of CLAUDE.md**

*This document is optimized for AI assistants working with the Skywind repository. Human developers should also refer to standard README and CONTRIBUTING files.*
