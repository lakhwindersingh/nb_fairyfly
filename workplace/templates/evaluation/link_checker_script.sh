#!/usr/bin/env bash
# Percipience Link & MDX Cross-Reference Integrity Checker
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
echo "🔍 Running Percipience Link & MDX Integrity Check across: ${REPO_ROOT}"

ERRORS=0
MD_FILES=$(find "${REPO_ROOT}/workplace/docs" "${REPO_ROOT}/workplace/src/content" -type f \( -name "*.md" -o -name "*.mdx" \))

for file in ${MD_FILES}; do
  # Extract file:// and relative markdown links [text](path)
  LINKS=$(grep -oE '\[[^]]+\]\(([^)]+)\)' "$file" | sed -E 's/.*\]\((.*)\)/\1/' || true)
  
  for link in ${LINKS}; do
    # Ignore web URLs, mailto, and anchor hashes on the same page
    if [[ "$link" =~ ^https?:// ]] || [[ "$link" =~ ^mailto: ]] || [[ "$link" =~ ^# ]]; then
      continue
    fi

    # Strip anchor fragments
    clean_link="${link%%#*}"
    
    # Handle file:// links
    if [[ "$clean_link" =~ ^file:// ]]; then
      resolved_path="${clean_link#file://}"
    elif [[ "$clean_link" =~ ^/ ]]; then
      resolved_path="${REPO_ROOT}${clean_link}"
    else
      file_dir="$(dirname "$file")"
      resolved_path="${file_dir}/${clean_link}"
    fi

    if [[ -n "$clean_link" && ! -e "$resolved_path" ]]; then
      echo "❌ Broken link in $file: '$link' (Target not found: $resolved_path)"
      ERRORS=$((ERRORS + 1))
    fi
  done
done

if [ "$ERRORS" -eq 0 ]; then
  echo "✅ All internal links, MDX references, and file URIs verified successfully!"
  exit 0
else
  echo "❌ Found $ERRORS broken link(s) in documentation. Please fix before merging."
  exit 1
fi
