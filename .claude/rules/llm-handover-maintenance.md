# LLM Handover Document Maintenance Rule

## Purpose
This rule ensures that the `llm_handover.md` document at the project root is kept up-to-date systematically to provide comprehensive context for AI agents working on the Treasure Hunt Analyzer project.

## Rule: Mandatory Handover Updates

### When to Update llm_handover.md

You MUST update the `llm_handover.md` document in the following situations:

1. **After Verified Milestones**
   - A feature is completed and tested
   - A bug is fixed and verified
   - A deployment is successful
   - A major refactoring is completed

2. **After Significant Changes**
   - New dependencies added (npm packages, pip packages)
   - Database schema changes
   - API endpoint changes (new, modified, deprecated)
   - Configuration changes (environment variables, Docker setup)
   - Architecture changes (new services, components, patterns)

3. **Project State Updates**
   - Git status changes (new branches, merges)
   - Environment changes (ports, URLs, credentials)
   - Known issues discovered or resolved
   - Testing results and validation
   - Deployment status changes

4. **Documentation Updates**
   - New .md files created
   - README updates
   - API documentation changes

### What to Update in llm_handover.md

#### Required Sections to Maintain:

1. **Header Information**
   - Update "Last Updated" date
   - Update "Project Status"
   - Update "Current Version" if applicable

2. **Current Project State**
   - Add newly working features to ✅ list
   - Update feature status
   - Document new capabilities

3. **Recent Milestones**
   - Add new milestone with date
   - Mark as verified (✅)
   - Include relevant metrics/data
   - Document what was fixed/added

4. **Known Issues**
   - Add new issues discovered
   - Move resolved issues to "Resolved" section with strikethrough
   - Update issue status

5. **Architecture Overview**
   - Update directory structure if changed
   - Update database schema if tables/columns added
   - Update data flow diagrams if applicable

6. **API Endpoints**
   - Add new endpoints
   - Mark deprecated endpoints
   - Update endpoint descriptions

7. **Environment Configuration**
   - Add new environment variables
   - Update port mappings
   - Update configuration examples

8. **Git & Version Control Status**
   - Update branch information
   - Update uncommitted changes count
   - Update GitHub sync status
   - Note new files/modifications

9. **Common Issues & Solutions**
   - Add new issues encountered and their solutions
   - Update existing solutions if improved

10. **Next Steps & Roadmap**
    - Check off completed items
    - Add new planned features
    - Update priorities

11. **Changelog**
    - Add dated entry with all changes made
    - Use clear, concise bullet points
    - Group related changes together

### How to Update

#### Update Format:
```markdown
### YYYY-MM-DD
- **CREATED/ADDED/FIXED/UPDATED/VERIFIED/REMOVED**: Brief description
- **DOCUMENTED**: What was documented
- **IDENTIFIED**: Issues or gaps found
```

#### Best Practices:
1. **Be Specific**: Include file paths, function names, exact error messages
2. **Be Concise**: One line per change when possible
3. **Be Accurate**: Only mark as verified if you've tested
4. **Be Complete**: Don't skip sections - update all relevant parts
5. **Be Systematic**: Follow the same format each time

### Verification Checklist

Before marking a milestone as complete, verify:
- [ ] All code changes are tested
- [ ] All tests pass (if applicable)
- [ ] Documentation is updated
- [ ] llm_handover.md is updated with the changes
- [ ] Changelog entry is added to llm_handover.md
- [ ] Git status is documented (committed or uncommitted)
- [ ] Known issues section is current

### Examples

#### Good Update:
```markdown
### 2025-11-23: Dashboard Enhancement ✅
- **ADDED**: Money Loss Over Time chart using Recharts (frontend/src/components/charts/MoneyLossChart.tsx)
- **VERIFIED**: Chart displays historical data correctly with 1000+ data points
- **UPDATED**: Dashboard.tsx to integrate new chart component
- **TESTED**: Data aggregation performance with large datasets
- **DOCUMENTED**: Updated API Endpoints section with new /api/v1/dashboard/trends endpoint
```

#### Poor Update:
```markdown
### 2025-11-23
- Added some charts
- Fixed bugs
- Updated stuff
```

### AI Agent Responsibilities

When you (the AI agent) are working on this project:

1. **Start Each Session**:
   - Read llm_handover.md FIRST
   - Check the "Last Updated" date
   - Review "Recent Milestones" and "Known Issues"
   - Understand current project state

2. **During Development**:
   - Take notes of changes made
   - Track issues encountered and solutions
   - Keep a mental/temporary list of updates needed

3. **Before Completing Work**:
   - Update llm_handover.md with ALL changes
   - Add changelog entry with today's date
   - Update relevant sections (features, APIs, issues, etc.)
   - Verify all information is accurate

4. **When Handing Off**:
   - Ensure llm_handover.md is complete and current
   - Highlight any unfinished work in "Next Steps"
   - Document any blocking issues in "Known Issues"
   - Update git status accurately

### Automation Reminder

Set a mental trigger to update llm_handover.md:
- ✅ After every successful feature completion
- ✅ After fixing any bug
- ✅ After every testing cycle
- ✅ Before ending a development session
- ✅ When discovering new issues
- ✅ When making infrastructure changes

### Non-Negotiable Rule

**You MUST NOT mark a task as complete without updating llm_handover.md.**

This document is the project's memory. Without it, future AI agents (and humans) will waste time rediscovering context, repeating work, or introducing bugs due to lack of understanding.

---

## Quick Reference

**File Location**: `/llm_handover.md` (project root)

**Update Trigger Events**:
- Feature complete ✅
- Bug fixed ✅
- Test passed ✅
- Deployment ✅
- Schema change ✅
- New API ✅
- Config change ✅
- Issue discovered ⚠️
- Session ending 🏁

**Minimum Update**:
1. Date + milestone name
2. What changed (bullet points)
3. Verification status
4. Updated git status
5. Changelog entry

**Remember**: The handover document is as important as the code itself. Keep it current, accurate, and comprehensive.
