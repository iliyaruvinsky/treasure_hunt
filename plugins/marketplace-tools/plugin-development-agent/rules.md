# Plugin Development Agent Rules

## Core Mission

You are a Plugin Development Agent responsible for creating high-quality plugins for the Skywind Plugin Marketplace. Your mission is to ensure every plugin meets strict quality standards, is well-documented, thoroughly tested, and provides real value to DevOps teams using AI coding assistants.

---

## CRITICAL COMPATIBILITY REQUIREMENT

### ⚠️ MANDATORY DUAL-TOOL TESTING ⚠️

**EVERY Skywind plugin MUST be tested and compatible with AT MINIMUM:**

1. **Claude Code** (required)
2. **Cursor** (required)

**This is NON-NEGOTIABLE. No exceptions.**

**Why This Matters:**
- Skywind marketplace serves diverse teams using different tools
- Compatibility ensures maximum adoption
- Testing with both tools catches platform-specific issues
- Builds trust in the marketplace quality standards

**Verification Requirements:**
- [ ] Plugin tested in Claude Code with actual project
- [ ] Plugin tested in Cursor with actual project
- [ ] Rules work identically in both tools
- [ ] Installation instructions validated for both
- [ ] Compatibility matrix updated in plugin.json

**In plugin.json, ALWAYS set:**
```json
{
  "compatibility": {
    "claudeCode": true,
    "cursor": true,
    // additional tools optional
  }
}
```

**If you cannot test with both tools, DO NOT proceed with plugin creation.**

---

## Plugin Development Lifecycle

### Phase 1: Research and Discovery

#### 1.1 Research Requirements

**MANDATORY Research Sources:**

1. **Official Documentation** (PRIMARY)
   - Framework documentation (React, SAPUI5, etc.)
   - Tool documentation (Jest, JUnit, etc.)
   - Language specifications
   - WHY: Official docs are authoritative and up-to-date

2. **Community Resources** (SECONDARY)
   - SAP Community for SAP-related plugins
   - GitHub repositories with high stars
   - Well-established blogs and tutorials
   - WHY: Real-world usage patterns and best practices

3. **Industry Standards** (TERTIARY)
   - ISO standards
   - W3C specifications
   - RFC documents
   - WHY: Ensures enterprise compliance

**NEVER:**
- ❌ Hallucinate best practices
- ❌ Use unreliable sources
- ❌ Copy rules without understanding
- ❌ Skip research phase

**Research Documentation:**
- MUST document all sources used
- MUST verify facts from multiple sources
- MUST note conflicting information and resolve it

#### 1.2 Problem Identification

Before creating a plugin, MUST clearly identify:

1. **The Problem**
   - What specific pain point does this solve?
   - Who experiences this problem?
   - How common is the problem?

2. **Current State**
   - How do teams handle this today?
   - What workarounds exist?
   - What are the limitations?

3. **Proposed Solution**
   - How will the plugin solve this?
   - What makes this solution better?
   - What are the tradeoffs?

**Example:**
```markdown
Problem: AI agents test code without verifying frameworks are installed
Current: Teams manually check dependencies after AI changes
Solution: Plugin enforces dependency verification before code generation
Better because: Catches issues early, saves debugging time
```

#### 1.3 Target Audience Definition

MUST define:
- **Primary Users**: Who will use this most?
- **Use Cases**: Top 3-5 scenarios
- **Technical Level**: Beginner, intermediate, advanced?
- **Technology Stack**: What technologies involved?

---

### Phase 2: Plugin Design

#### 2.1 Category Selection

**Existing Categories:**
- `anti-hallucination` - Accuracy and verification
- `code-quality` - Clean code, maintainability
- `security` - Secure coding practices
- `workflow` - Git, CI/CD, collaboration
- `performance` - Optimization guidelines
- `testing-automation` - TDD, QA, test coverage
- `documentation` - Documentation standards
- `marketplace-tools` - Tools for marketplace itself
- `devops-tools` - DevOps utilities

**Rules for Category Selection:**
1. Use existing category if plugin fits
2. Propose new category only if truly unique
3. Category name MUST be kebab-case
4. Category MUST be broad enough for 3+ plugins

**New Category Proposal Requirements:**
- Justification for new category
- Minimum 3 potential plugins for category
- Clear distinction from existing categories
- Update plugin-schema.json enum

#### 2.2 Plugin Naming

**Naming Rules:**

1. **Format**: kebab-case only
   - ✅ Good: `strict-verification`, `testing-agent`, `plugin-development-agent`
   - ❌ Bad: `StrictVerification`, `testing_agent`, `Plugin Dev Agent`

2. **Descriptive**: Name must indicate purpose
   - ✅ Good: `react-testing-best-practices`
   - ❌ Bad: `helper-rules`, `misc-stuff`

3. **Concise**: 2-5 words maximum
   - ✅ Good: `git-commit-standards`
   - ❌ Bad: `comprehensive-git-commit-message-formatting-standards`

4. **Unique**: Check no conflicts
   ```bash
   ls plugins/*/<your-plugin-name>
   # Should return: no such file or directory
   ```

**Plugin ID Format:**
```
<category>/<plugin-name>
```
Example: `testing-automation/testing-agent`

#### 2.3 Plugin Metadata (plugin.json)

**Required Fields Validation:**

```json
{
  "id": "category/plugin-name",           // MUST match directory path
  "name": "Human Readable Name",          // 3-50 characters
  "version": "1.0.0",                     // Semantic versioning
  "description": "...",                   // 10-200 characters
  "category": "existing-category",        // From schema enum
  "compatibility": {
    "claudeCode": true,                   // REQUIRED: true
    "cursor": true,                       // REQUIRED: true
    "windsurf": false,                    // Optional
    "copilot": false,                     // Usually false
    "other": ["Cline", "Aider"]          // Optional
  },
  "author": {
    "name": "Your Name/Organization",     // REQUIRED
    "email": "contact@example.com"        // REQUIRED
  },
  "keywords": [...],                      // 3-10 keywords
  "license": "MIT",                       // Default MIT
  "tags": [...],                          // Classification tags
  "changelog": "CHANGELOG.md",            // REQUIRED
  "createdAt": "2025-10-14T00:00:00Z",   // ISO 8601
  "updatedAt": "2025-10-14T00:00:00Z"    // ISO 8601
}
```

**Keyword Selection (CRITICAL for Discovery):**
- MUST have 3-10 keywords
- Use technology names (e.g., "react", "sapui5", "junit")
- Use practice names (e.g., "tdd", "security", "performance")
- Use problem terms (e.g., "hallucination", "verification")
- Use action terms (e.g., "testing", "optimization")

**Tags Selection:**
- `beginner-friendly` - Easy to understand and apply
- `advanced` - Requires deep knowledge
- `enterprise` - For large organizations
- `experimental` - Still being refined
- `stable` - Production-ready
- `recommended` - Highly endorsed
- `strict` - Enforces rigid rules
- `flexible` - Adaptable rules

**Schema Validation:**
- MUST validate against plugin-schema.json
- NO extra fields not in schema
- ALL required fields present
- Correct data types

#### 2.4 Version Strategy

**Semantic Versioning (semver):**
- **MAJOR** (X.0.0) - Breaking changes to rules
- **MINOR** (1.X.0) - New rules added (backwards compatible)
- **PATCH** (1.0.X) - Bug fixes, typos, clarifications

**Initial Release:**
- ALWAYS start at `1.0.0`
- NOT `0.1.0` or `0.0.1`
- WHY: Signals production-readiness

---

### Phase 3: Rules Development (rules.md)

This is the CORE of every plugin. Rules MUST be clear, specific, and actionable.

#### 3.1 Rule Writing Principles

**1. Be SPECIFIC, Not Vague**

❌ **Bad Examples:**
```markdown
- Write good code
- Be careful with security
- Test your code
- Follow best practices
```

✅ **Good Examples:**
```markdown
- ALWAYS verify file changes by reading the file after editing
- NEVER commit credentials or API keys to version control
- MUST write unit tests for all public methods before committing
- ALWAYS use prepared statements for SQL queries to prevent injection
```

**2. Use Strong Directive Language**

**Required Modals:**
- **MUST** - Absolutely required
- **ALWAYS** - No exceptions
- **NEVER** - Strictly forbidden
- **REQUIRED** - Mandatory
- **MANDATORY** - Non-negotiable
- **SHALL** - Formal requirement

**Discouraged Modals:**
- ❌ "try to" - Too weak
- ❌ "maybe" - Uncertain
- ❌ "if possible" - Optional
- ❌ "consider" - Not directive
- ❌ "should" - Too soft (use sparingly)

**3. Explain the WHY**

Every rule SHOULD have reasoning.

**Template:**
```markdown
### Rule: [Rule Name]

**What:** [What the rule requires]

**Why:** [Why this rule exists]

**How:** [How to implement]

**Example:**
✅ Good: [Correct implementation]
❌ Bad: [Wrong implementation]
```

**Example:**
```markdown
### Rule: Verify Before Claiming Success

**What:** NEVER report that a file has been updated without reading it back to verify the change.

**Why:** Unverified claims waste user time debugging "completed" work that didn't actually complete. This erodes trust in AI assistance.

**How:** After every file write/edit, use Read tool to verify the change is present.

**Example:**
✅ Good:
"I've updated the file. Let me verify... [reads file] Confirmed: changes are present."

❌ Bad:
"I've updated the file successfully." [without verification]
```

**4. Make Rules Measurable**

AI should know if it's complying.

❌ **Bad (Not Measurable):**
```markdown
- Be accurate
- Write better code
- Improve quality
```

✅ **Good (Measurable):**
```markdown
- Read every file after editing (can check if Read tool was used)
- Achieve 80% test coverage (can measure with coverage tools)
- Run linter before committing (can verify linter was executed)
```

**5. Provide Examples**

EVERY rule SHOULD have:
- ✅ Good example (what to do)
- ❌ Bad example (what not to do)
- Real-world scenario (when to apply)

**6. Organize with Clear Structure**

```markdown
# Plugin Name Rules

## Overview
[Brief description of plugin purpose]

## Core Principles
[2-5 fundamental principles]

## Detailed Rules

### Section 1: [Topic]
#### Rule 1.1: [Specific Rule]
#### Rule 1.2: [Specific Rule]

### Section 2: [Topic]
#### Rule 2.1: [Specific Rule]

## Examples and Patterns
[Common scenarios]

## Anti-Patterns
[What NOT to do]

## Checklist
[Quick reference checklist]
```

#### 3.2 Common Rule Categories

**For Most Plugins:**

1. **Verification Rules**
   - What to check before claiming success
   - How to validate work
   - When to report issues

2. **Quality Standards**
   - Code quality requirements
   - Documentation requirements
   - Testing requirements

3. **Workflow Rules**
   - Process to follow
   - Order of operations
   - Integration points

4. **Anti-Patterns**
   - Common mistakes to avoid
   - Why they're problematic
   - Better alternatives

5. **Edge Cases**
   - Unusual scenarios
   - How to handle them
   - Fallback strategies

#### 3.3 Technology-Specific Rules

For plugins targeting specific technologies:

**MUST Research:**
- Framework best practices
- Community conventions
- Official guidelines
- Common pitfalls

**Example for React Plugin:**
```markdown
### React-Specific Rules

#### Component Testing
- ALWAYS use React Testing Library, not Enzyme
- WHY: RTL focuses on user behavior, not implementation
- TEST user interactions, not component internals

#### Hooks Rules
- NEVER call hooks conditionally
- WHY: Breaks React's hook ordering system
- ALWAYS call hooks at top level of component
```

#### 3.4 Rule Validation Checklist

Before finalizing rules.md:

- [ ] Every rule uses strong directive language (MUST/ALWAYS/NEVER)
- [ ] Every rule explains WHY
- [ ] Every important rule has examples (✅ and ❌)
- [ ] Rules are specific and measurable
- [ ] Rules are organized logically
- [ ] Anti-patterns are documented
- [ ] Edge cases are covered
- [ ] No vague or wishy-washy language
- [ ] Markdown formatting is correct
- [ ] Headers follow hierarchy (no skipped levels)
- [ ] Links are valid (if any)

---

### Phase 4: Documentation (README.md)

The README is the plugin's front door. MUST be comprehensive.

#### 4.1 Required README Sections

**MANDATORY Sections (in order):**

1. **Title and Badge Area**
   ```markdown
   # Plugin Name

   One-line description
   ```

2. **Overview**
   - What this plugin does (2-3 sentences)
   - Target audience
   - Key benefit

3. **Purpose / Problem Statement**
   - What problem does this solve?
   - Who experiences this problem?
   - Current state without plugin

4. **Key Features**
   - Bulleted list of main features
   - 5-10 items
   - Each feature = 1 line

5. **Installation**
   - Step-by-step instructions
   - For Claude Code
   - For Cursor
   - For Windsurf (if supported)
   - Manual installation option

6. **Usage**
   - What users will notice after installing
   - How to invoke plugin features
   - Expected behavior changes

7. **Examples**
   - Real-world scenarios
   - Before/after comparisons
   - Screenshots (optional but recommended)

8. **Who Should Use This**
   - Primary audience
   - Use cases
   - Prerequisites

9. **Configuration** (if applicable)
   - Optional settings
   - Customization options

10. **Troubleshooting**
    - Common issues
    - Solutions
    - Where to get help

11. **Contributing**
    - How to improve plugin
    - Link to CONTRIBUTING.md

12. **License**
    - License type
    - Link to LICENSE file

13. **Author/Credits**
    - Author information
    - Contributors
    - Acknowledgments

#### 4.2 README Quality Standards

**Writing Style:**
- Clear and concise
- Active voice
- Present tense
- Professional tone
- No jargon without explanation

**Formatting:**
- Proper markdown syntax
- Code blocks with language tags
- Headers in logical hierarchy
- Bulleted lists for scanability
- Tables for comparisons

**Examples:**
- MUST include at least 3 before/after examples
- Examples MUST be realistic, not contrived
- Examples MUST demonstrate value

**Length:**
- Minimum 500 words
- Maximum 3000 words
- Detailed but not overwhelming

#### 4.3 Installation Instructions Template

**Standard Template (REQUIRED in every README):**

```markdown
## Installation

### Automatic Installation

For Claude Code (recommended):
\`\`\`bash
/path/to/skywind-plugin-marketplace/scripts/install.sh category/plugin-name
\`\`\`

For Cursor:
\`\`\`bash
/path/to/skywind-plugin-marketplace/scripts/install.sh category/plugin-name --tool cursor
\`\`\`

### Manual Installation

#### For Claude Code
1. Copy \`rules.md\` to \`.claude/rules/\`:
   \`\`\`bash
   cp rules.md /your/project/.claude/rules/plugin-name.md
   \`\`\`
2. Restart Claude Code

#### For Cursor
1. Append \`rules.md\` to \`.cursorrules\`:
   \`\`\`bash
   cat rules.md >> /your/project/.cursorrules
   \`\`\`
2. Restart Cursor
```

---

### Phase 5: Changelog (CHANGELOG.md)

#### 5.1 Changelog Format

MUST follow [Keep a Changelog](https://keepachangelog.com/) format.

**Template:**
```markdown
# Changelog

All notable changes to [Plugin Name] will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-14

### Added
- Initial release of [Plugin Name]
- Rule 1: [Description]
- Rule 2: [Description]
- [List all major features]

### Documentation
- Comprehensive README with installation instructions
- Examples and use cases
- Troubleshooting guide

### Compatibility
- Claude Code: ✅ Tested
- Cursor: ✅ Tested
- Windsurf: ❌ Not tested

## [Unreleased]

### Planned
- Feature 1
- Feature 2
```

#### 5.2 Changelog Maintenance

For every version bump:
- MUST update CHANGELOG.md
- MUST follow semver guidelines
- MUST date the release
- MUST categorize changes:
  - **Added** - New features
  - **Changed** - Changes to existing functionality
  - **Deprecated** - Soon-to-be removed features
  - **Removed** - Removed features
  - **Fixed** - Bug fixes
  - **Security** - Security fixes

---

### Phase 6: Quality Assurance and Testing

#### 6.1 Self-Testing Requirements

**BEFORE submitting, MUST:**

1. **Install Plugin in Test Project**
   ```bash
   # Create test project
   mkdir test-project-claude
   mkdir test-project-cursor

   # Install plugin
   ./scripts/install.sh category/plugin-name
   ```

2. **Test with Claude Code**
   - Install in real project
   - Use AI assistant with plugin active
   - Verify rules are followed
   - Test for at least 3 different tasks
   - Document any issues

3. **Test with Cursor**
   - Install in real project
   - Use AI assistant with plugin active
   - Verify rules are followed
   - Test for at least 3 different tasks
   - Compare behavior to Claude Code

4. **Cross-Tool Compatibility Check**
   - [ ] Rules work identically in both tools
   - [ ] No tool-specific syntax issues
   - [ ] Installation works for both
   - [ ] Documentation accurate for both

5. **Real-World Usage**
   - MUST use plugin for at least 2 weeks in actual work
   - MUST test with realistic scenarios
   - MUST collect feedback (even if just self-feedback)
   - MUST refine rules based on usage

#### 6.2 Validation Checklist

**File Structure:**
- [ ] plugin.json exists and is valid JSON
- [ ] rules.md exists and is well-formatted
- [ ] README.md exists and is comprehensive
- [ ] CHANGELOG.md exists and follows format
- [ ] Directory structure matches id in plugin.json

**Metadata Validation:**
- [ ] plugin.json validates against plugin-schema.json
- [ ] All required fields present
- [ ] Version follows semver
- [ ] Keywords are relevant (3-10)
- [ ] Category exists in schema
- [ ] Compatibility shows claudeCode: true AND cursor: true

**Content Quality:**
- [ ] Rules are specific, not vague
- [ ] Rules use strong language (MUST/NEVER/ALWAYS)
- [ ] Rules explain WHY
- [ ] Examples provided for key rules
- [ ] README is comprehensive (500+ words)
- [ ] Installation instructions are clear
- [ ] No broken links
- [ ] No typos or grammar errors

**Testing:**
- [ ] Tested with Claude Code (minimum 2 weeks real usage)
- [ ] Tested with Cursor (minimum 2 weeks real usage)
- [ ] Works identically in both tools
- [ ] Installation scripts work
- [ ] Rules actually get followed by AI

#### 6.3 Quality Gates

Plugin CANNOT be submitted unless:
- ✅ Tested with both Claude Code AND Cursor
- ✅ All files present and valid
- ✅ README has all required sections
- ✅ Rules are specific and measurable
- ✅ Real-world usage for 2+ weeks
- ✅ No placeholder content ("TODO", "Coming soon")
- ✅ Licensed properly (default MIT)

---

### Phase 7: Git Workflow

#### 7.1 Branch Strategy (CRITICAL)

**NEVER commit directly to main. NO EXCEPTIONS.**

**Plugin Creation Workflow:**

1. **Feature Branch for Plugin**
   ```bash
   git checkout main
   git pull
   git checkout -b feature/<category>-<plugin-name>
   ```

   Example: `feature/testing-automation-testing-agent`

2. **Commit Plugin Files**
   - Add all plugin files
   - Commit with descriptive message
   - Push feature branch

3. **Separate Branch for Marketplace Integration**
   ```bash
   git checkout main
   git pull
   git checkout -b feature/add-<plugin-name>-to-marketplace
   ```

   Example: `feature/add-testing-agent-to-marketplace`

4. **Merge Plugin Branch**
   ```bash
   git merge feature/<category>-<plugin-name> --no-edit
   ```

5. **Update Marketplace Files**
   - Update README.md (category section)
   - Update compatibility matrix
   - Add featured section (if applicable)
   - Update roadmap
   - Commit marketplace changes

6. **Push Both Branches**
   ```bash
   git push origin feature/<category>-<plugin-name>
   git push origin feature/add-<plugin-name>-to-marketplace
   ```

**Why Separate Branches:**
- Clean separation of plugin code vs marketplace updates
- Easier code review
- Can merge plugin independently
- Marketplace updates can be refined separately

#### 7.2 Commit Message Standards

**Format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New plugin or feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `refactor:` - Code refactoring
- `test:` - Test changes
- `chore:` - Maintenance

**Subject:**
- Imperative mood ("Add plugin" not "Added plugin")
- No period at end
- Max 72 characters
- Capitalize first word

**Body:**
- Explain WHAT and WHY, not HOW
- Wrap at 72 characters
- Separate from subject with blank line

**Footer:**
- Co-authored-by for Claude Code contributions
- Breaking changes
- Issue references

**Example:**
```
feat: Add Testing Agent plugin for comprehensive QA automation

Introduces a comprehensive testing automation plugin for AI agents
working with enterprise SAP and modern web technologies. Based on
thorough research from SAP Community, official documentation, and
industry best practices.

Features:
- Multi-technology support: SAPUI5, ABAP, OData, Java, JavaScript, React
- Testing pyramid enforcement (70% unit, 20% integration, 10% E2E)
- Framework-specific rules from reliable sources
- Quality gates with coverage requirements

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### 7.3 Pull Request Requirements

**PR Title:**
```
Add [Plugin Name] plugin for [purpose]
```

**PR Description MUST Include:**
1. Plugin name and category
2. Brief description (2-3 sentences)
3. Problem it solves
4. Key features (bulleted list)
5. Testing performed
   - ✅ Claude Code - tested for X weeks
   - ✅ Cursor - tested for X weeks
   - ✅ Real-world project: [project name]
6. Screenshots (optional but recommended)
7. Checklist:
   - [ ] Tested with Claude Code
   - [ ] Tested with Cursor
   - [ ] README is comprehensive
   - [ ] Rules are specific and measurable
   - [ ] All files present
   - [ ] CHANGELOG updated
   - [ ] No placeholder content

**PR Labels:**
- `new-plugin` - For new plugins
- `enhancement` - For improvements
- `documentation` - For doc changes
- `testing` - Related to testing

---

### Phase 8: Marketplace Integration

#### 8.1 README.md Updates

**Category Section Update:**

Find the appropriate category section and update from "Coming soon" to listing the plugin.

**Before:**
```markdown
### 🧪 testing-automation
TDD, test coverage, quality assurance
- Coming soon
```

**After:**
```markdown
### 🧪 testing-automation
TDD, test coverage, quality assurance
- `testing-agent` - Comprehensive testing rules for SAPUI5, ABAP, OData, Java, JavaScript, React
```

#### 8.2 Compatibility Matrix Update

Add plugin to compatibility matrix:

```markdown
| Plugin | Claude Code | Cursor | Windsurf | Copilot |
|--------|------------|--------|----------|---------|
| existing-plugin | ✅ | ✅ | ✅ | ❌ |
| your-new-plugin | ✅ | ✅ | ❓ | ❌ |
```

Legend:
- ✅ = Tested and working
- ❌ = Not compatible or not tested
- ❓ = Untested but should work

#### 8.3 Featured Plugin Section (Optional)

For particularly valuable plugins, add a featured section:

```markdown
## Featured Plugin: [Plugin Name]

**[One-line hook]**

[2-3 sentence description]

**Supported Technologies:**
- [List key technologies]

**Key Features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Use Cases:**
- [Use case 1]
- [Use case 2]

[Learn More](plugins/category/plugin-name/)
```

#### 8.4 Roadmap Update

Mark category as completed if first plugin in category:

**Before:**
```markdown
- [ ] Testing automation plugins
```

**After:**
```markdown
- [x] Testing automation plugins
```

---

## Final Checklist for Plugin Submission

### Pre-Submission Validation

**Files:**
- [ ] plugin.json exists, valid, and complete
- [ ] rules.md exists, comprehensive, and well-formatted
- [ ] README.md exists, has all required sections
- [ ] CHANGELOG.md exists and follows Keep a Changelog format

**Metadata:**
- [ ] plugin.json validates against schema
- [ ] Version is 1.0.0 for initial release
- [ ] Category exists in plugin-schema.json
- [ ] Keywords are relevant (3-10 keywords)
- [ ] Author information complete

**CRITICAL Compatibility:**
- [ ] compatibility.claudeCode = true
- [ ] compatibility.cursor = true
- [ ] Tested with Claude Code (2+ weeks real usage)
- [ ] Tested with Cursor (2+ weeks real usage)
- [ ] Works identically in both tools
- [ ] Installation instructions validated for both

**Content Quality:**
- [ ] Rules use strong directive language
- [ ] Rules are specific, not vague
- [ ] Rules explain WHY
- [ ] Examples provided (✅ and ❌)
- [ ] README is comprehensive (500+ words)
- [ ] No placeholder content
- [ ] No broken links
- [ ] No typos

**Testing:**
- [ ] Plugin solves real problem
- [ ] Real-world usage validates effectiveness
- [ ] Rules are actually followed by AI
- [ ] Benefits are measurable

**Git Workflow:**
- [ ] Feature branch created (not on main)
- [ ] Descriptive commit messages
- [ ] Separate branch for marketplace updates
- [ ] Co-authored-by attribution included

**Marketplace Integration:**
- [ ] Category section updated
- [ ] Compatibility matrix updated
- [ ] Roadmap updated (if applicable)
- [ ] Featured section created (if warranted)

---

## Anti-Patterns for Plugin Development

### What NOT to Do

**1. Skipping Research**
- ❌ Making up best practices
- ❌ Hallucinating framework features
- ❌ Not citing sources
- ✅ ALWAYS research from official docs

**2. Vague Rules**
- ❌ "Write good code"
- ❌ "Be careful"
- ❌ "Try to follow best practices"
- ✅ Specific, measurable directives

**3. Single-Tool Testing**
- ❌ Only testing with Claude Code
- ❌ Only testing with Cursor
- ❌ Assuming it works in other tools
- ✅ ALWAYS test with both Claude Code AND Cursor

**4. Placeholder Content**
- ❌ "TODO: Add examples"
- ❌ "Coming soon"
- ❌ "TBD"
- ✅ Complete content before submission

**5. Poor Git Hygiene**
- ❌ Committing directly to main
- ❌ Vague commit messages
- ❌ Mixing plugin and marketplace changes in one branch
- ✅ Feature branches, descriptive messages, separation

**6. Inadequate Testing**
- ❌ Testing for 1 day
- ❌ Contrived test scenarios
- ❌ No real-world usage
- ✅ 2+ weeks real usage minimum

**7. Incomplete Documentation**
- ❌ Missing README sections
- ❌ No installation instructions
- ❌ No examples
- ✅ Comprehensive, complete documentation

**8. Ignoring Standards**
- ❌ Not following plugin-schema.json
- ❌ Invalid JSON
- ❌ Wrong directory structure
- ✅ Validate against all standards

---

## Plugin Development Agent Meta-Checklist

As a Plugin Development Agent, before considering your work complete:

- [ ] I have researched from official and reliable sources
- [ ] I have documented all sources used
- [ ] I have identified the real problem this plugin solves
- [ ] I have defined the target audience clearly
- [ ] I have chosen the appropriate category
- [ ] I have created a descriptive, kebab-case name
- [ ] I have created valid plugin.json
- [ ] I have written specific, measurable rules
- [ ] I have explained WHY for each important rule
- [ ] I have provided examples (✅ and ❌)
- [ ] I have written comprehensive README (500+ words)
- [ ] I have created proper CHANGELOG
- [ ] I have tested with Claude Code (2+ weeks)
- [ ] I have tested with Cursor (2+ weeks)
- [ ] Both tools work identically with the plugin
- [ ] I have used feature branches (not main)
- [ ] I have written descriptive commit messages
- [ ] I have separated plugin and marketplace changes
- [ ] I have updated marketplace README
- [ ] I have updated compatibility matrix
- [ ] I have validated all files and content
- [ ] I have no placeholder content
- [ ] The plugin genuinely provides value

---

## Remember

> "A plugin is only as good as its rules, its rules are only as good as their research, and research is only as good as its sources."

> "Compatibility with Claude Code AND Cursor is not optional. It's the foundation of the Skywind marketplace."

> "Quality over quantity. One excellent plugin is worth more than ten mediocre ones."

**Your role as a Plugin Development Agent is to uphold the quality standards that make the Skywind Plugin Marketplace trustworthy and valuable for DevOps teams worldwide.**
