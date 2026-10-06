# Plan Space Reorganization - Generic Execution Prompt

## Context

This prompt guides the reorganization of a flat plan file structure into a plan-centric folder organization with dual-format documentation (concise + detailed), automated version synchronization, and comprehensive navigation.

## Objective

Transform a flat directory of plan files into a well-organized, maintainable structure where:
- Each plan has its own folder with all versions co-located
- Concise versions are optimized for agentic context (~500-1000 lines)
- Detailed versions provide complete implementation guidance (~1500-3000 lines)
- Version tracking is automated with content hashes
- Navigation is seamless for both agents and humans

---

## Step-by-Step Execution Guide

### Phase 1: Assessment & Planning (30 minutes)

**Task 1.1: Inventory Current Structure**
```
1. List all plan files in the current directory
2. Identify file naming patterns (e.g., l1-*, l2-*, l3-*, master-*)
3. Count total plans and categorize by level/type
4. Identify any existing documentation or meta-files
5. Note any cross-references between plans
```

**Task 1.2: Design Target Structure**
```
Target structure should follow this pattern:

.nb/plan/ (or equivalent)
├── PLAN_INDEX.md           # Agentic navigation (master index)
├── PLAN_GUIDE.md           # Human-readable guide
├── master/                 # Top-level orchestration
│   └── [plan-name]/
│       ├── MANIFEST.yaml   # Version tracking with SHA-256 hashes
│       ├── README.md       # Quick overview
│       ├── concise.md      # Agentic context (~500-1000 lines)
│       └── detailed.md     # Implementation guide (~1500-3000 lines)
├── l1/                     # Foundation layer plans
│   └── [plan-name]/
│       ├── MANIFEST.yaml
│       ├── README.md
│       ├── concise.md
│       └── detailed.md
├── l2/                     # Self-evolution layer plans
│   └── [plan-name]/
│       └── (same 4-file structure)
├── l3/                     # Production layer plans
│   └── [plan-name]/
│       └── (same 4-file structure)
├── architecture/           # Cross-cutting concerns (optional)
│   └── [plan-name]/
│       └── (same 4-file structure)
└── archive/
    └── old_structure/      # Archived original files
```

**Task 1.3: Create Mapping Document**
```
Create a mapping file (e.g., REORGANIZATION_MAP.md) listing:

OLD PATH → NEW PATH → PLAN TYPE
Example:
- l1-transmutative-reasoning.md → l1/transmutative-reasoning/concise.md → foundation
- l2-neural-architecture.md → l2/neural-architecture-foundation/concise.md → self-evolution
- master-parent-plan.md → master/parent-master-plan/concise.md → orchestration
```

---

### Phase 2: Create Target Structure (15 minutes)

**Task 2.1: Create Folder Hierarchy**
```bash
# Create main directories
mkdir -p master l1 l2 l3 architecture archive/old_structure

# For each identified plan, create its folder
# Example:
mkdir -p master/parent-master-plan
mkdir -p l1/transmutative-reasoning
mkdir -p l2/neural-architecture-foundation
mkdir -p l3/nlp-inference-dsl
```

**Task 2.2: Identify Concise vs Detailed Content**
```
For each existing file, determine:
- Is this already concise (optimized for context)?
- Is this detailed (human implementation guide)?
- Do we need to split one file into both formats?
- Do we need to create a detailed version from scratch?

Mark in your mapping document which files need:
- [COPY] - Direct copy to concise.md
- [SPLIT] - Split into concise + detailed
- [CREATE_DETAILED] - Need to write new detailed.md
- [CREATE_CONCISE] - Need to write new concise.md
```

---

### Phase 3: Content Migration (1-2 hours)

**Task 3.1: Copy Files to New Structure**
```bash
# For each plan in mapping:
# Example for direct copy:
cp old/l1-transmutative-reasoning.md l1/transmutative-reasoning/concise.md

# For plans needing both formats:
cp old/l2-neural-architecture-human-friendly.md l2/neural-architecture-foundation/detailed.md
cp old/l2-neural-architecture-concise.md l2/neural-architecture-foundation/concise.md
```

**Task 3.2: Check for Inverted Files**
```
Common issue: Files may be mislabeled
- Check line counts: concise should be SMALLER than detailed
- If concise > detailed, files are likely swapped
- Swap them during migration

Example check:
wc -l l2/*/concise.md l2/*/detailed.md
# If concise has more lines, swap them
```

**Task 3.3: Create README.md for Each Plan**
```markdown
# Template for README.md

# [Plan Level]: [Plan Name]

**Plan ID**: `[plan_id]`  
**Capability Rating**: [L1/L2/L3]  
**Version**: [version]

## Overview

[2-3 sentence description]

## Quick Links

- **Concise Plan**: [concise.md](./concise.md) - Complete specification (~XXX lines)
- **Detailed Plan**: [detailed.md](./detailed.md) - Implementation guide
- **Parent Plan**: [link to parent]
- **Dependencies**: [list dependencies]

## Key Features

- Feature 1
- Feature 2
- Feature 3

## Success Criteria

- Criterion 1
- Criterion 2
- Criterion 3

## Implementation Timeline

**Total Duration**: X weeks

- Phase 1: Description (Weeks X-Y)
- Phase 2: Description (Weeks Y-Z)
```

**Task 3.4: Create MANIFEST.yaml for Each Plan**
```yaml
# Template for MANIFEST.yaml

plan_id: [unique_plan_id]
plan_name: [Human Readable Name]
version: "X.Y"
capability_rating: [L1/L2/L3/Master]
plan_type: [foundation/self-evolution/production/orchestration]
status: [active/planned/archived]

parent_plan: [parent plan path]
dependencies:
  - [dependency_1]
  - [dependency_2]

file_versions:
  concise:
    path: concise.md
    version: "X.Y"
    last_modified: "YYYY-MM-DD"
    content_hash: [SHA-256 hash - compute later]
    line_count: [number]
    primary_purpose: Complete specification for agentic context

  detailed:
    path: detailed.md
    version: "X.Y"
    last_modified: "YYYY-MM-DD"
    content_hash: [SHA-256 hash - compute later]
    line_count: [number]
    primary_purpose: Extended implementation guide with code examples

  readme:
    path: README.md
    version: "X.Y"
    last_modified: "YYYY-MM-DD"
    content_hash: [SHA-256 hash - compute later]
    line_count: [number]
    primary_purpose: Quick reference and navigation

key_capabilities:
  - [capability 1]
  - [capability 2]

implementation_phases:
  phase_1: [description (Weeks X-Y)]
  phase_2: [description (Weeks Y-Z)]

success_metrics:
  metric_1: "[target]"
  metric_2: "[target]"

related_contracts:
  - [contract path 1]
  - [contract path 2]

related_rules:
  - [rule path 1]
  - [rule path 2]
```

---

### Phase 4: Create Missing Content (2-4 hours)

**Task 4.1: Identify Content Gaps**
```
Review each plan folder and identify:
- Plans missing detailed.md (need to create from concise)
- Plans missing concise.md (need to condense from detailed)
- Plans with identical concise/detailed (need to expand detailed)
- Plans with inverted ratios (concise > detailed - need to fix)
```

**Task 4.2: Create Detailed Versions**
```
For plans missing detailed.md:

1. Read the concise version completely
2. Create detailed.md with these expansions:
   - Add complete code examples for all algorithms
   - Add implementation phase breakdowns
   - Add verification/testing strategies
   - Add integration patterns
   - Add troubleshooting guides
   - Target: 2-3× the size of concise

Example structure for detailed.md:
---
# [Plan Name] - Detailed Implementation Guide

## Part I: Architecture Deep Dive
[Expand architectural concepts with diagrams]

## Part II: Mathematical Foundations
[Add complete proofs, derivations]

## Part III: Implementation Algorithms
[Full code examples with comments]

## Part IV: Verification Strategy
[Complete test suites, validation]

## Part V: Integration Patterns
[How to integrate with other plans]

## Part VI: Implementation Phases
[Detailed week-by-week breakdown]

## Part VII: Troubleshooting
[Common issues and solutions]
```

**Task 4.3: Create Concise Versions**
```
For plans missing concise.md:

1. Read the detailed version completely
2. Create concise.md by:
   - Keep mathematical formulations
   - Keep architecture diagrams (ASCII)
   - Keep key algorithms (pseudocode only)
   - Remove detailed code examples
   - Remove troubleshooting sections
   - Keep success metrics
   - Target: 500-1000 lines, <3000 tokens
```

**Task 4.4: Fix Inverted Ratios**
```
For plans where concise > detailed:

Option A: Swap the files
mv concise.md temp.md
mv detailed.md concise.md
mv temp.md detailed.md

Option B: Expand the detailed version
[Keep concise as-is, expand detailed with more examples]
```

---

### Phase 5: Archive Old Structure (15 minutes)

**Task 5.1: Move Original Files to Archive**
```bash
# Create archive structure mirroring original
mkdir -p archive/old_structure/master
mkdir -p archive/old_structure/l1
mkdir -p archive/old_structure/l2
mkdir -p archive/old_structure/l3

# Move all original files
mv master-*.md archive/old_structure/master/
mv l1-*.md archive/old_structure/l1/
mv l2-*.md archive/old_structure/l2/
mv l3-*.md archive/old_structure/l3/

# Move any human_friendly directories
mv human_friendly/ archive/old_structure/
```

**Task 5.2: Create Archive README**
```markdown
# Archive: Old Structure

This directory contains the original plan files before reorganization.

**Reorganization Date**: YYYY-MM-DD  
**Reason**: Transition to plan-centric folder organization  
**New Structure**: See ../PLAN_INDEX.md

## Original Structure

[Document what was here]

## Migration Map

See ../REORGANIZATION_MAP.md for complete file mapping.

## Note

These files are kept for historical reference only. 
All active development should use the new structure.
```

---

### Phase 6: Create Navigation Documents (1-2 hours)

**Task 6.1: Create PLAN_INDEX.md**
```markdown
# Template structure

---
index_type: "master_navigation"
purpose: "Unified entry point for agentic and human navigation of all plans"
last_updated: "YYYY-MM"
total_plans: [count]
organization_schema: "hierarchical_with_dual_format"
---

# 📋 Plan Index & Navigation Guide

## Quick Navigation

```
📦 .nb/plan/ (or equivalent)
├── 📖 PLAN_INDEX.md          ← YOU ARE HERE
├── 📚 PLAN_GUIDE.md          ← Human guide
├── 🎯 master/                ← Orchestration
├── 🏗️  l1/                    ← Foundation
├── 🧠 l2/                    ← Self-Evolution
├── 🚀 l3/                    ← Production
└── 🗄️  archive/               ← Historical
```

## 1. Master Orchestration Plans

### [Plan Name]
**Location**: `master/[plan-folder]/concise.md`  
**Detailed**: `master/[plan-folder]/detailed.md`  
**Overview**: `master/[plan-folder]/README.md`  
**Sync Status**: `master/[plan-folder]/MANIFEST.yaml`  
**Purpose**: [Brief description]

[Repeat for each master plan]

## 2. L1 Foundation Layer

### [Plan Name]
**Location**: `l1/[plan-folder]/concise.md`  
**Capability**: [Key capability]  
**Dependencies**: [List]

[Repeat for each L1 plan]

## 3. L2 Self-Evolution Layer

[Similar structure]

## 4. L3 Production Layer

[Similar structure]

## 5. Cross-Cutting Architecture

[If applicable]
```

**Task 6.2: Create PLAN_GUIDE.md**
```markdown
# Human-Readable Plan Guide

## Purpose

This guide provides a human-friendly overview of all plans in this repository.

## Organization Principles

### Dual-Format Documentation
- **Concise** (~500-1000 lines): Optimized for agentic context
- **Detailed** (~1500-3000 lines): Complete implementation guide

### Plan-Centric Folders
Each plan lives in its own folder with:
- MANIFEST.yaml - Version tracking
- README.md - Quick overview
- concise.md - Agentic specification
- detailed.md - Implementation guide

### Version Synchronization
All files tracked with SHA-256 content hashes in MANIFEST.yaml

## Plan Hierarchy

### Master Plans
[Describe orchestration layer]

### L1 Foundation
[Describe foundation layer]

### L2 Self-Evolution
[Describe self-evolution layer]

### L3 Production
[Describe production layer]

## How to Use This Guide

### For Developers
1. Start with PLAN_INDEX.md for navigation
2. Read README.md for quick overview
3. Use concise.md for architecture understanding
4. Reference detailed.md during implementation

### For Agents
1. Load PLAN_INDEX.md as context
2. Navigate to specific plan's concise.md
3. Use MANIFEST.yaml for version tracking

## Navigation Tips

[Add specific navigation patterns for your repository]
```

---

### Phase 7: Create Version Sync Tool (30 minutes)

**Task 7.1: Create sync_plan_versions.py**
```python
#!/usr/bin/env python3
"""
Automated plan version synchronization tool.
Computes SHA-256 hashes and updates MANIFEST.yaml files.
"""

import hashlib
import yaml
from pathlib import Path
from typing import Dict, Optional

class PlanVersionSync:
    def __init__(self, plan_root: Path):
        self.plan_root = Path(plan_root)
    
    def compute_hash(self, file_path: Path) -> Optional[str]:
        """Compute SHA-256 hash of file content."""
        if not file_path.exists():
            return None
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def get_line_count(self, file_path: Path) -> int:
        """Count lines in file."""
        if not file_path.exists():
            return 0
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    
    def update_manifest(self, plan_dir: Path):
        """Update MANIFEST.yaml with current file hashes."""
        manifest_path = plan_dir / 'MANIFEST.yaml'
        
        if not manifest_path.exists():
            print(f"⚠️  No MANIFEST.yaml in {plan_dir.name}")
            return
        
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)
        
        # Update file versions
        for file_type in ['concise', 'detailed', 'readme']:
            if file_type in manifest.get('file_versions', {}):
                file_name = manifest['file_versions'][file_type]['path']
                file_path = plan_dir / file_name
                
                # Update hash
                new_hash = self.compute_hash(file_path)
                if new_hash:
                    manifest['file_versions'][file_type]['content_hash'] = new_hash
                
                # Update line count
                line_count = self.get_line_count(file_path)
                manifest['file_versions'][file_type]['line_count'] = line_count
        
        # Write updated manifest
        with open(manifest_path, 'w') as f:
            yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ {manifest.get('plan_name', plan_dir.name)}: Updated")
    
    def check_sync_status(self, plan_dir: Path) -> Dict:
        """Check if files are in sync with MANIFEST."""
        manifest_path = plan_dir / 'MANIFEST.yaml'
        
        if not manifest_path.exists():
            return {'status': 'no_manifest'}
        
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)
        
        issues = []
        
        for file_type in ['concise', 'detailed']:
            if file_type not in manifest.get('file_versions', {}):
                continue
            
            file_info = manifest['file_versions'][file_type]
            file_path = plan_dir / file_info['path']
            
            # Check hash
            current_hash = self.compute_hash(file_path)
            stored_hash = file_info.get('content_hash')
            
            if current_hash != stored_hash:
                issues.append(f"{file_type}.md hash mismatch")
        
        return {
            'status': 'in_sync' if not issues else 'out_of_sync',
            'issues': issues
        }
    
    def sync_all_plans(self):
        """Sync all plan directories."""
        plan_dirs = []
        
        # Find all plan directories
        for category in ['master', 'l1', 'l2', 'l3', 'architecture']:
            category_path = self.plan_root / category
            if category_path.exists():
                plan_dirs.extend([d for d in category_path.iterdir() if d.is_dir()])
        
        # Update each plan
        for plan_dir in sorted(plan_dirs):
            self.update_manifest(plan_dir)
    
    def report_sync_status(self):
        """Report sync status for all plans."""
        plan_dirs = []
        
        for category in ['master', 'l1', 'l2', 'l3', 'architecture']:
            category_path = self.plan_root / category
            if category_path.exists():
                plan_dirs.extend([d for d in category_path.iterdir() if d.is_dir()])
        
        print("\n📊 Plan Sync Status Report\n")
        
        for plan_dir in sorted(plan_dirs):
            status = self.check_sync_status(plan_dir)
            
            if status['status'] == 'in_sync':
                print(f"✅ {plan_dir.name}: In sync")
            elif status['status'] == 'out_of_sync':
                print(f"❌ {plan_dir.name}: Out of sync")
                for issue in status['issues']:
                    print(f"   - {issue}")
            else:
                print(f"⚠️  {plan_dir.name}: No manifest")

if __name__ == '__main__':
    import sys
    
    plan_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.nb/plan')
    
    syncer = PlanVersionSync(plan_root)
    
    # Update all manifests
    syncer.sync_all_plans()
    
    # Report status
    syncer.report_sync_status()
```

**Task 7.2: Make Tool Executable**
```bash
chmod +x sync_plan_versions.py
```

---

### Phase 8: Verification & Quality Check (30 minutes)

**Task 8.1: Run Sync Tool**
```bash
# Compute all hashes and update MANIFESTs
python sync_plan_versions.py

# Check output for any issues
# Should see all green checkmarks
```

**Task 8.2: Verify Structure**
```bash
# Check all plans have 4 files
find master l1 l2 l3 -type d -mindepth 1 -maxdepth 1 | while read dir; do
    echo "Checking $dir:"
    ls -1 "$dir" | grep -E "^(MANIFEST.yaml|README.md|concise.md|detailed.md)$" | wc -l
    # Should output 4 for each directory
done
```

**Task 8.3: Check Line Count Ratios**
```bash
# Detailed should generally be larger than concise
find . -name "concise.md" | while read concise; do
    detailed="${concise/concise.md/detailed.md}"
    if [ -f "$detailed" ]; then
        c_lines=$(wc -l < "$concise")
        d_lines=$(wc -l < "$detailed")
        if [ $c_lines -gt $d_lines ]; then
            echo "⚠️  Inverted ratio: $(dirname $concise)"
            echo "   Concise: $c_lines, Detailed: $d_lines"
        fi
    fi
done
```

**Task 8.4: Validate YAML Files**
```bash
# Check all MANIFEST.yaml files are valid
find . -name "MANIFEST.yaml" -exec python -c "
import yaml
import sys
try:
    with open('{}', 'r') as f:
        yaml.safe_load(f)
    print('✅ {}')
except Exception as e:
    print('❌ {}: {}'.format('{}', e))
    sys.exit(1)
" \;
```

**Task 8.5: Check for Broken Links**
```bash
# Verify all referenced files exist
# (This is a simplified check - adjust grep patterns as needed)
grep -r "](\./" master l1 l2 l3 --include="*.md" | \
    grep -oP ']\(\./[^)]+\)' | \
    sed 's/](\.\///; s/)$//' | \
    while read link; do
        if [ ! -f "$link" ] && [ ! -d "$link" ]; then
            echo "❌ Broken link: $link"
        fi
    done
```

---

### Phase 9: Create Completion Report (15 minutes)

**Task 9.1: Generate Statistics**
```bash
# Count total plans
total_plans=$(find master l1 l2 l3 -name "MANIFEST.yaml" | wc -l)

# Count total lines across all concise files
concise_lines=$(find master l1 l2 l3 -name "concise.md" -exec wc -l {} + | tail -1 | awk '{print $1}')

# Count total lines across all detailed files
detailed_lines=$(find master l1 l2 l3 -name "detailed.md" -exec wc -l {} + | tail -1 | awk '{print $1}')

# Count archived files
archived_files=$(find archive/old_structure -type f | wc -l)

echo "Total Plans: $total_plans"
echo "Total Concise Lines: $concise_lines"
echo "Total Detailed Lines: $detailed_lines"
echo "Archived Files: $archived_files"
```

**Task 9.2: Create REORGANIZATION_COMPLETE.md**
```markdown
# Plan Reorganization - Completion Report

**Date**: YYYY-MM-DD  
**Status**: ✅ COMPLETE

## Executive Summary

Successfully reorganized [N] plans from flat file structure to plan-centric folder organization with dual-format documentation and automated version synchronization.

## Statistics

- **Total Plans**: [N]
- **Total Files Created**: [N × 4]
- **Concise Documentation**: [X,XXX] lines
- **Detailed Documentation**: [Y,YYY] lines
- **Archived Files**: [N]

## Structure Created

```
.nb/plan/
├── master/ ([N] plans)
├── l1/ ([N] plans)
├── l2/ ([N] plans)
├── l3/ ([N] plans)
└── archive/old_structure/ ([N] files)
```

## Completed Tasks

### Phase 1: Assessment ✅
- Inventoried [N] existing plan files
- Created reorganization map
- Designed target structure

### Phase 2: Structure Creation ✅
- Created [N] plan folders
- Established 4-file pattern

### Phase 3: Content Migration ✅
- Migrated all existing content
- Fixed [N] inverted file pairs
- Preserved all historical content

### Phase 4: Content Generation ✅
- Created [N] missing detailed.md files
- Created [N] missing concise.md files
- Created [N] README.md files
- Created [N] MANIFEST.yaml files

### Phase 5: Archive ✅
- Moved [N] files to archive/old_structure/
- Preserved original directory structure
- Created archive documentation

### Phase 6: Navigation ✅
- Created PLAN_INDEX.md
- Created PLAN_GUIDE.md
- Updated cross-references

### Phase 7: Tooling ✅
- Created sync_plan_versions.py
- Automated version tracking
- Implemented hash verification

### Phase 8: Verification ✅
- All plans have 4 files
- All MANIFEST.yaml files valid
- All content hashes computed
- No broken links found

### Phase 9: Documentation ✅
- Created completion report
- Documented maintenance procedures
- Created troubleshooting guide

## Sync Status

All [N] plans verified in sync:
```
✅ [plan 1]: In sync
✅ [plan 2]: In sync
...
```

## Next Steps

### Immediate
1. Commit all changes to version control
2. Update team documentation
3. Train team on new structure

### Ongoing Maintenance
1. Run sync_plan_versions.py after any plan modifications
2. Keep PLAN_INDEX.md updated when adding new plans
3. Maintain concise/detailed ratio guidelines
4. Review and update archived content periodically

## Success Metrics

- ✅ [N]/[N] plans fully reorganized
- ✅ [N × 4]/[N × 4] required files present
- ✅ 100% plans with version tracking
- ✅ 0 broken links or missing files
- ✅ Automated sync tool operational

## Maintenance Guide

### Adding a New Plan

1. Create folder: `mkdir -p [category]/[plan-name]`
2. Create 4 files: MANIFEST.yaml, README.md, concise.md, detailed.md
3. Run: `python sync_plan_versions.py`
4. Update PLAN_INDEX.md

### Updating Existing Plan

1. Edit concise.md and/or detailed.md
2. Run: `python sync_plan_versions.py`
3. Verify sync status

### Checking for Drift

```bash
python sync_plan_versions.py --check-only
```

## Troubleshooting

### Issue: "Out of sync" warning
**Solution**: Run `python sync_plan_versions.py` to recompute hashes

### Issue: Inverted ratio (concise > detailed)
**Solution**: Swap files or expand detailed version

### Issue: Missing MANIFEST.yaml
**Solution**: Create from template and run sync tool

---

**Project Status**: ✅ COMPLETE AND VERIFIED
```

---

### Phase 10: Final Review & Handoff (15 minutes)

**Task 10.1: Create Quick Start Guide**
```markdown
# Quick Start - Reorganized Plan Structure

## For New Users

1. **Start here**: Read `PLAN_INDEX.md` for navigation
2. **Understand**: Read `PLAN_GUIDE.md` for concepts
3. **Navigate**: Use folder structure to find plans
4. **Read**: Start with README.md, then concise.md

## For Agents

1. **Load context**: Include `PLAN_INDEX.md` in context
2. **Navigate**: Follow paths to specific plan's concise.md
3. **Reference**: Check MANIFEST.yaml for version info

## For Developers

1. **Implementation**: Use detailed.md as implementation guide
2. **Testing**: Follow verification sections
3. **Integration**: Check dependencies in MANIFEST.yaml

## Maintenance

- After editing plans: `python sync_plan_versions.py`
- Check sync status: `python sync_plan_versions.py --report`
```

**Task 10.2: Commit to Version Control**
```bash
# Stage all changes
git add master/ l1/ l2/ l3/ architecture/ archive/
git add PLAN_INDEX.md PLAN_GUIDE.md REORGANIZATION_COMPLETE.md
git add sync_plan_versions.py

# Commit with descriptive message
git commit -m "Complete plan reorganization: plan-centric folders with dual-format docs

- Reorganized [N] plans into hierarchical folder structure
- Created concise.md (agentic context) + detailed.md (implementation)
- Added MANIFEST.yaml version tracking with SHA-256 hashes
- Created sync_plan_versions.py automation tool
- Archived [N] original files to archive/old_structure/
- Created PLAN_INDEX.md and PLAN_GUIDE.md navigation
- All plans verified in sync"

# Create tag
git tag -a reorg-v1.0 -m "Plan reorganization complete"
```

**Task 10.3: Final Checklist**
```
□ All plan folders created with correct naming
□ All plans have 4 files (MANIFEST.yaml, README.md, concise.md, detailed.md)
□ All MANIFEST.yaml files have computed hashes
□ All concise files are optimized for agentic context
□ All detailed files provide implementation guidance
□ PLAN_INDEX.md includes all plans with correct paths
□ PLAN_GUIDE.md provides human-readable overview
□ sync_plan_versions.py tool is functional
□ Archive contains all original files
□ REORGANIZATION_COMPLETE.md documents entire process
□ No broken links or references
□ Version control committed and tagged
```

---

## Expected Outcomes

### Structure Quality
- **Consistency**: All plans follow identical 4-file pattern
- **Navigability**: Clear hierarchy with master index
- **Maintainability**: Automated sync tool prevents drift
- **Scalability**: Easy to add new plans

### Documentation Quality
- **Concise Format**: Optimized for LLM context windows
- **Detailed Format**: Complete for human implementation
- **Cross-References**: All dependencies documented
- **Version Tracking**: SHA-256 hashes for integrity

### Operational Benefits
- **Fast Navigation**: Agents can quickly find relevant plans
- **Clear Context**: Dual formats serve different audiences
- **Version Safety**: Automated drift detection
- **Historical Preservation**: Archive maintains original content

---

## Time Estimates

- **Phase 1 (Assessment)**: 30 minutes
- **Phase 2 (Structure)**: 15 minutes
- **Phase 3 (Migration)**: 1-2 hours
- **Phase 4 (Content)**: 2-4 hours (varies by number of missing files)
- **Phase 5 (Archive)**: 15 minutes
- **Phase 6 (Navigation)**: 1-2 hours
- **Phase 7 (Tooling)**: 30 minutes
- **Phase 8 (Verification)**: 30 minutes
- **Phase 9 (Reporting)**: 15 minutes
- **Phase 10 (Review)**: 15 minutes

**Total**: 6-10 hours (depends on plan count and content gaps)

---

## Adaptation Notes

This guide is generic and should be adapted based on:
- Your specific plan naming conventions
- Your capability rating system (L1/L2/L3 or other)
- Your repository structure
- Your team's workflow
- Your version control practices

Key areas to customize:
1. Folder names (master/l1/l2/l3 vs your hierarchy)
2. MANIFEST.yaml schema (add your specific fields)
3. README.md template (match your documentation style)
4. sync_plan_versions.py (adjust paths and logic)
5. Success metrics (define what matters for your team)

---

## Support & Troubleshooting

If you encounter issues during reorganization:

1. **Backup First**: Always have a complete backup before starting
2. **Go Incremental**: Do one plan at a time to catch issues early
3. **Verify Often**: Run checks after each phase
4. **Document Deviations**: Note any changes from this guide
5. **Ask for Review**: Have another team member spot-check

Common pitfalls to avoid:
- Don't delete original files until archive is verified
- Don't manually edit content hashes (use sync tool)
- Don't skip verification phase
- Don't forget to update cross-references
- Don't mix old and new paths in documentation

---

## Success Criteria

Your reorganization is complete when:
- ✅ All plans have identical 4-file structure
- ✅ All MANIFEST.yaml files have valid hashes
- ✅ Concise/detailed ratio is appropriate (concise < detailed)
- ✅ Navigation documents are complete and accurate
- ✅ Sync tool runs without errors
- ✅ Archive contains all original content
- ✅ No broken links or references
- ✅ Team can navigate and use new structure
- ✅ Changes committed to version control

**When all criteria met**: Your plan space is successfully reorganized! 🎉
