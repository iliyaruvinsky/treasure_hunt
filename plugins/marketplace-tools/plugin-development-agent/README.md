# Plugin Development Agent

**Comprehensive rules for AI agents creating high-quality Skywind marketplace plugins**

Ensures every plugin meets strict quality standards, is well-documented, thoroughly tested with both Claude Code AND Cursor, and provides real value to DevOps teams.

## Overview

The Plugin Development Agent is a meta-plugin that guides AI coding assistants through the complete plugin development lifecycle for the Skywind Plugin Marketplace. It enforces standards, best practices, quality gates, and proper git workflow to ensure consistent, high-quality plugins.

## Purpose

### The Problem

Without standardized guidance, plugin creation is inconsistent:
- Plugins lack proper research and documentation
- Rules are vague and not actionable
- Testing is inadequate or skipped entirely
- Git workflow is chaotic (direct commits to main)
- Marketplace integration is forgotten or done incorrectly
- **Critical:** Single-tool testing leads to compatibility issues

### The Solution

This plugin provides a comprehensive framework covering:
- Research methodology from reliable sources
- Plugin design and metadata standards
- Rule writing best practices (specific, measurable, with examples)
- Documentation requirements
- Quality assurance and testing protocols
- Git workflow (feature branches, commit standards)
- Marketplace integration process

### The Critical Requirement

**EVERY plugin MUST be tested with BOTH:**
1. **Claude Code** (minimum 2 weeks real usage)
2. **Cursor** (minimum 2 weeks real usage)

This is non-negotiable and enforced throughout the rules.

## Key Features

- **8-Phase Development Lifecycle**: Research → Design → Rules → Documentation → QA → Git → Marketplace → Submission
- **Dual-Tool Compatibility Enforcement**: Mandatory Claude Code AND Cursor testing
- **Research Standards**: Official docs, SAP Community, GitHub - no hallucinations
- **Rule Writing Framework**: Specific, measurable rules with WHY explanations
- **Documentation Template**: 13 required README sections with examples
- **Quality Gates**: Cannot submit without passing all checks
- **Git Workflow Standards**: Feature branches, descriptive commits, separation of concerns
- **Marketplace Integration**: Automated README updates, compatibility matrix, roadmap
- **Meta-Compliance**: This plugin itself follows all rules it enforces

## Target Audience

### Primary Users
- **AI Coding Assistants** (Claude, Cursor AI) creating Skywind plugins
- **Plugin Developers** using AI assistance for plugin development
- **DevOps Teams** maintaining marketplace quality standards

### Use Cases
1. Creating new plugins for the marketplace
2. Ensuring consistent plugin quality across contributors
3. Standardizing plugin documentation
4. Enforcing compatibility requirements
5. Maintaining marketplace integrity

## Installation

### Automatic Installation

**For Claude Code:**
```bash
/path/to/skywind-plugin-marketplace/scripts/install.sh marketplace-tools/plugin-development-agent
```

**For Cursor:**
```bash
/path/to/skywind-plugin-marketplace/scripts/install.sh marketplace-tools/plugin-development-agent --tool cursor
```

### Manual Installation

#### For Claude Code
1. Copy `rules.md` to `.claude/rules/`:
   ```bash
   cp rules.md /your/project/.claude/rules/plugin-development-agent.md
   ```
2. Restart Claude Code

#### For Cursor
1. Append `rules.md` to `.cursorrules`:
   ```bash
   cat rules.md >> /your/project/.cursorrules
   ```
2. Restart Cursor

## Usage

Once installed, the AI agent will automatically follow plugin development standards when:

- Creating new plugins
- Updating existing plugins
- Writing documentation
- Performing quality checks
- Managing git workflow
- Integrating with marketplace

### Example Interactions

**Creating a New Plugin:**
```
User: "Create a new plugin for React testing best practices"

AI (with plugin active):
"I'll create a React testing plugin following Skywind standards. Let me start with research phase:

Phase 1: Research
- Searching official React Testing Library documentation...
- Reviewing Jest documentation...
- Checking React community best practices...
[Documents sources]

Phase 2: Plugin Design
- Category: testing-automation
- Name: react-testing-best-practices
- Validating against plugin-schema.json...

[Continues through all 8 phases]

IMPORTANT: Before submission, this plugin MUST be tested with:
✅ Claude Code (2+ weeks real usage required)
✅ Cursor (2+ weeks real usage required)
```

**Validating Plugin Quality:**
```
User: "Review my plugin for quality"

AI (with plugin active):
"Running quality validation checklist...

❌ FAILED: Rules use weak language ('should', 'try to')
❌ FAILED: No WHY explanations for rules
❌ FAILED: Only tested with Claude Code - Cursor testing REQUIRED
✅ PASSED: plugin.json validates against schema
✅ PASSED: README has all required sections

Cannot submit until all checks pass."
```

## The 8-Phase Development Lifecycle

### Phase 1: Research and Discovery
- Research from official documentation (PRIMARY)
- Community resources (SECONDARY - SAP Community, GitHub)
- Industry standards (TERTIARY)
- Problem identification and validation
- Target audience definition

### Phase 2: Plugin Design
- Category selection (use existing or propose new)
- Plugin naming (kebab-case, descriptive)
- Metadata design (plugin.json)
- Keyword selection for discoverability
- Version strategy (semantic versioning)

### Phase 3: Rules Development
- Write specific, measurable rules
- Use strong directive language (MUST, NEVER, ALWAYS)
- Explain WHY for each rule
- Provide examples (✅ Good, ❌ Bad)
- Organize logically with clear structure
- Document anti-patterns

### Phase 4: Documentation
- 13 required README sections
- Installation instructions (Claude Code, Cursor, manual)
- Real-world examples
- Before/after comparisons
- Troubleshooting guide
- CHANGELOG following Keep a Changelog format

### Phase 5: Quality Assurance
- Install in test projects
- Test with Claude Code (minimum 2 weeks)
- Test with Cursor (minimum 2 weeks)
- Verify identical behavior in both tools
- Real-world usage validation
- Self-validation checklist

### Phase 6: Git Workflow
- Feature branch for plugin code
- Separate branch for marketplace updates
- Descriptive commit messages
- Pull request with comprehensive description
- NEVER commit directly to main

### Phase 7: Marketplace Integration
- Update README.md category section
- Add to compatibility matrix
- Create featured section (if applicable)
- Update roadmap
- Validate all links

### Phase 8: Final Submission
- Complete pre-submission checklist
- Verify all quality gates passed
- Ensure dual-tool compatibility verified
- Submit pull request
- Respond to reviewer feedback

## Critical Compatibility Requirement

### ⚠️ Dual-Tool Testing is MANDATORY ⚠️

Every Skywind plugin MUST be tested with:

1. **Claude Code** ✅
2. **Cursor** ✅

**Minimum Testing:**
- 2 weeks real-world usage per tool
- Multiple realistic scenarios
- Verify identical behavior
- Document any issues

**In plugin.json:**
```json
{
  "compatibility": {
    "claudeCode": true,  // REQUIRED
    "cursor": true,      // REQUIRED
    "windsurf": false,   // Optional
    "copilot": false     // Usually false
  }
}
```

**Why This Matters:**
- Skywind marketplace serves diverse teams
- Maximum adoption requires broad compatibility
- Catches platform-specific issues early
- Builds trust in marketplace quality

## Rule Writing Best Practices

### ✅ Good Rules (Specific and Measurable)

```markdown
### Rule: Verify File Changes

**What:** ALWAYS read the file after editing to verify changes were applied.

**Why:** Unverified claims waste user time debugging incomplete work.

**How:** Use Read tool immediately after Write/Edit tool.

**Example:**
✅ Good: "I've updated user.service.ts. Let me verify... [reads file] Confirmed: changes applied."
❌ Bad: "I've updated user.service.ts successfully." [no verification]
```

### ❌ Bad Rules (Vague and Unmeasurable)

```markdown
- Write good code
- Be careful with security
- Try to follow best practices
- Consider adding tests
```

### Directive Language

**Use:**
- MUST, ALWAYS, NEVER, REQUIRED, MANDATORY

**Avoid:**
- "try to", "maybe", "if possible", "consider", "should" (too weak)

## Documentation Requirements

### Required README Sections

1. Title and one-line description
2. Overview (what it does)
3. Purpose / Problem statement
4. Key features (bulleted)
5. Target audience
6. Installation (automatic + manual for Claude Code and Cursor)
7. Usage examples
8. Before/after comparisons
9. Who should use this
10. Configuration (if applicable)
11. Troubleshooting
12. Contributing
13. License and credits

**Minimum Length:** 500 words
**Maximum Length:** 3000 words

## Quality Gates

### Cannot Submit Until:

**Files:**
- [ ] plugin.json exists and validates
- [ ] rules.md is comprehensive
- [ ] README.md has all 13 sections
- [ ] CHANGELOG.md follows format

**Compatibility (CRITICAL):**
- [ ] Tested with Claude Code (2+ weeks)
- [ ] Tested with Cursor (2+ weeks)
- [ ] Works identically in both tools
- [ ] compatibility.claudeCode = true
- [ ] compatibility.cursor = true

**Content:**
- [ ] Rules are specific and measurable
- [ ] Rules use strong language
- [ ] Rules explain WHY
- [ ] Examples provided
- [ ] No placeholder content
- [ ] No broken links

**Testing:**
- [ ] Real-world usage validates effectiveness
- [ ] Rules actually get followed by AI
- [ ] Benefits are measurable

**Git:**
- [ ] Feature branch used (not main)
- [ ] Descriptive commit messages
- [ ] Marketplace updates in separate branch

## Git Workflow Example

```bash
# Step 1: Create plugin feature branch
git checkout main
git pull
git checkout -b feature/marketplace-tools-plugin-development-agent

# Step 2: Create plugin files
mkdir -p plugins/marketplace-tools/plugin-development-agent
# Create plugin.json, rules.md, README.md, CHANGELOG.md

# Step 3: Commit plugin
git add plugins/marketplace-tools/
git commit -m "feat: Add Plugin Development Agent

Comprehensive rules for creating high-quality Skywind plugins..."

# Step 4: Push plugin branch
git push origin feature/marketplace-tools-plugin-development-agent

# Step 5: Create marketplace integration branch
git checkout main
git checkout -b feature/add-plugin-dev-agent-to-marketplace

# Step 6: Merge plugin
git merge feature/marketplace-tools-plugin-development-agent --no-edit

# Step 7: Update marketplace files
# Update README.md, compatibility matrix, etc.

# Step 8: Commit marketplace changes
git add README.md
git commit -m "feat: Add Plugin Development Agent to marketplace"

# Step 9: Push marketplace branch
git push origin feature/add-plugin-dev-agent-to-marketplace
```

## Anti-Patterns to Avoid

### What NOT to Do

1. **❌ Skipping Research**
   - Making up best practices
   - Hallucinating features
   - ✅ ALWAYS research from official docs

2. **❌ Vague Rules**
   - "Write good code", "Be careful"
   - ✅ Specific, measurable directives

3. **❌ Single-Tool Testing**
   - Only testing with one tool
   - ✅ MUST test with both Claude Code AND Cursor

4. **❌ Placeholder Content**
   - "TODO", "Coming soon", "TBD"
   - ✅ Complete before submission

5. **❌ Poor Git Hygiene**
   - Direct commits to main
   - ✅ Feature branches always

6. **❌ Inadequate Testing**
   - Testing for 1 day
   - ✅ Minimum 2 weeks per tool

## Examples

### Example 1: Creating Testing Plugin

**Before (Without Plugin Development Agent):**
```
AI: "I'll create a testing plugin."
[Creates vague rules like "Write tests"]
[No research documented]
[Only tests with Claude Code]
[Commits directly to main]
[Forgets marketplace integration]
```

**After (With Plugin Development Agent):**
```
AI: "I'll create a testing plugin following Skywind standards.

Phase 1: Research
- Reviewed Jest documentation (https://jestjs.io/docs/...)
- Studied React Testing Library docs (https://testing-library.com/...)
- Analyzed SAP UI5 QUnit guide (https://sapui5.hana.ondemand.com/...)
[Documents all sources]

Phase 2: Plugin Design
- Category: testing-automation
- Name: comprehensive-testing-agent
- Keywords: testing, qa, jest, junit, qunit...

Phase 3: Rules Development
RULE: ALWAYS write unit tests before committing
WHY: Catches bugs early, documents behavior
HOW: Use appropriate framework (Jest, JUnit, QUnit)
EXAMPLE:
✅ "Let me write tests first... [writes tests] Tests passing, now implementing."
❌ "Implementation complete. I'll add tests later."

[Continues through all phases]

Phase 5: Quality Assurance
- Installing in test project for Claude Code...
- Will test for 2+ weeks with realistic scenarios
- Then repeat with Cursor before submission

Phase 6: Git Workflow
- Creating feature/testing-automation-comprehensive-testing-agent branch
- NOT committing to main
```

### Example 2: Quality Validation

**Scenario:** AI reviews plugin before submission

```
AI: "Running pre-submission validation for react-hooks-best-practices plugin...

✅ PASSED: plugin.json validates against schema
✅ PASSED: README has all 13 required sections
✅ PASSED: Rules use strong language (MUST, NEVER, ALWAYS)
✅ PASSED: Rules explain WHY
✅ PASSED: Examples provided (✅ and ❌)
❌ FAILED: Only tested with Claude Code - Cursor testing REQUIRED
❌ FAILED: Real-world usage only 1 week - need 2+ weeks per tool
✅ PASSED: Feature branch used (not main)
❌ FAILED: Marketplace README not updated

CANNOT SUBMIT: 3 critical checks failed
Actions needed:
1. Test with Cursor for 2+ weeks
2. Continue Claude Code testing for 1 more week
3. Update marketplace README.md

Estimated time to submission: 2+ weeks (for testing requirements)
```

## Troubleshooting

### Plugin Rules Not Being Followed

**Issue:** AI isn't following the plugin development rules

**Solutions:**
1. Verify plugin is installed correctly
2. Check rules.md was copied/appended properly
3. Restart the AI coding assistant
4. Try reinstalling the plugin
5. Ensure no conflicting plugins

### Validation Failing

**Issue:** Quality gates keep failing

**Solutions:**
1. Review the specific failed checks
2. Use the provided checklists in rules.md
3. Validate plugin.json against schema:
   ```bash
   node scripts/validate.js plugins/category/plugin-name
   ```
4. Check for placeholder content ("TODO", etc.)
5. Ensure both tools tested (not just one)

### Git Workflow Confusion

**Issue:** Unclear about branching strategy

**Solutions:**
1. Review Phase 6 in rules.md
2. Always create feature branch first
3. Never commit to main
4. Separate plugin code from marketplace updates
5. Follow the example in this README

## Contributing

Want to improve this plugin?

1. Fork the Skywind Plugin Marketplace repository
2. Create a feature branch
3. Make your improvements
4. Test with both Claude Code and Cursor
5. Submit a pull request

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for detailed guidelines.

## Who Should Use This

### Perfect For

- **AI Agents** creating Skywind plugins
- **Plugin Developers** using AI assistance
- **DevOps Teams** maintaining marketplace quality
- **Contributors** submitting to the marketplace

### Prerequisites

- Access to Claude Code OR Cursor (both preferred)
- Understanding of git workflow
- Familiarity with markdown
- Access to Skywind Plugin Marketplace repository

### Not Suitable For

- Creating non-Skywind plugins (different standards)
- Quick prototyping without quality requirements
- Single-tool-only environments (both tools required)

## Benefits

### For AI Agents
- Clear workflow to follow
- Reduces errors and rework
- Ensures quality standards
- Validates compatibility

### For Plugin Developers
- Consistent process
- Quality assurance built-in
- Proper documentation templates
- Git workflow guidance

### For Marketplace
- Higher quality plugins
- Consistent structure
- Verified compatibility
- Trustworthy standards

### For Users (DevOps Teams)
- Reliable plugins
- Comprehensive documentation
- Known compatibility
- Quality guarantee

## Meta-Compliance

This plugin itself follows all the rules it enforces:

- ✅ Researched from existing marketplace structure
- ✅ Uses specific, measurable rules
- ✅ Explains WHY for each requirement
- ✅ Provides examples throughout
- ✅ Comprehensive README (this document)
- ✅ Proper CHANGELOG
- ✅ Will be tested with Claude Code and Cursor
- ✅ Uses feature branch workflow
- ✅ Complete documentation
- ✅ No placeholder content

## Resources

- [Skywind Plugin Marketplace](https://github.com/iliyaruvinsky/skywind-plugin-marketplace)
- [CONTRIBUTING.md](../../../CONTRIBUTING.md)
- [plugin-schema.json](../../../plugin-schema.json)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

## License

MIT License - See [LICENSE](../../../LICENSE) file for details

## Author

Skywind Platform DevOps Team
- Email: devops@skywind.com
- Repository: https://github.com/iliyaruvinsky/skywind-plugin-marketplace

## Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

**Remember:** Quality over quantity. Every plugin in the Skywind marketplace should be trustworthy, well-documented, and thoroughly tested with both Claude Code AND Cursor. This plugin helps ensure that standard is met consistently.
