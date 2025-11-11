# Merge Strategy: Treasure Hunt Context Repository

## Overview
Merging content from `GIT Repo TH` (https://github.com/iliyaruvinsky/treasure_hunt) into `treasure-hunt-analyzer` project.

## Merge Plan

### 1. Documentation & Context Files
**Source**: `GIT Repo TH/` root and subdirectories
**Destination**: `treasure-hunt-analyzer/docs/th-context/`

**Files to merge:**
- `Treasure_Hunt_Findings_Report.pdf` → `docs/th-context/`
- `Treasure_Hunt_Template.docx` → `docs/th-context/`
- `Treasure_Hunt_Campaign_Blurb.docx` → `docs/th-context/`
- `Skywind_Treasure_Hunting_Methodology_and_PoC_Steps.pdf` → `docs/th-context/`
- `Integrated_SAP_Treasure_Hunt_Landing_Page.md` → `docs/th-context/`
- `Treasure_Hunt_Cost_Data_Research_Questions.md` → `docs/th-context/`
- All `ReadMore_*.md` files → `docs/th-context/readmore/`

### 2. Case Studies & Examples
**Source**: `GIT Repo TH/MAIN PAGE/Cost Savings/`
**Destination**: `treasure-hunt-analyzer/docs/case-studies/`

**Content:**
- Alert Stories
- Case Studies (CBC, Maccabi, etc.)
- Cost saving examples
- Brochures and presentations

### 3. Product Documentation
**Source**: `GIT Repo TH/MAIN PAGE/` and `About Us/`
**Destination**: `treasure-hunt-analyzer/docs/product-docs/`

**Content:**
- Skywind 4C documentation
- Skywind SoDA documentation
- Skywind JAM documentation
- Skywind AG documentation
- About Us materials

### 4. SoDA Email Templates
**Source**: `GIT Repo TH/SoDA-Email-Templates-main/`
**Destination**: `treasure-hunt-analyzer/docs/soda-templates/`

**Purpose**: Reference for SoDA report email notifications

### 5. Plugins (Already Exists)
**Source**: `GIT Repo TH/plugins/`
**Destination**: Already in `treasure-hunt-analyzer/skywind-plugin-marketplace/plugins/`

**Action**: Compare and merge if different versions exist

## Files to NOT Merge
- `.claude/` and `.cursorrules` (project-specific, already handled)
- `cursor.rar` (archive file)
- Duplicate files that already exist in THA project

## Execution Steps

1. Copy documentation files
2. Copy case studies
3. Copy product documentation
4. Copy SoDA templates
5. Create index/README for easy navigation
6. Update main README with links to context

## Benefits
- All TH context in one place
- Easy reference for development
- Case studies for testing/validation
- Product docs for understanding Skywind platform
- Preserves original structure for reference

