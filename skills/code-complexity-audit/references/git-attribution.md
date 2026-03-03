# Git Attribution Reference

How to identify who introduced problematic code. Read when performing Step 4 of the audit.

---

## Purpose

Attribution helps teams prioritize fixes by distinguishing **recently introduced complexity** (fresh, easy to address) from **legacy complexity** (older, may require more context). It is for context, not blame.

## Commit Window

Look back **100 commits** from HEAD. Code older than this is marked `Legacy`.

### Find the boundary commit

```bash
# Get the hash of the 100th commit back
BOUNDARY=$(git log --oneline -100 --format='%H' | tail -1)
echo "Boundary commit: $BOUNDARY"

# Get its date for reference
git log -1 --format='%ai' $BOUNDARY
```

---

## Attribution Workflow

For each finding in the audit:

### 1. Identify the origin of the problematic code

```bash
# Blame a specific line range
git blame -L <start>,<end> -- <file>

# Blame with commit hash, author, and date
git blame -L <start>,<end> --format='%H %an %ai' -- <file>
```

### 2. Check if it falls within the 100-commit window

```bash
# Check if a commit is within the window
# Returns 0 (success) if the commit is an ancestor of HEAD within 100 commits
git merge-base --is-ancestor $BOUNDARY <commit_hash> && echo "Within window" || echo "Legacy"
```

Alternatively, compare the commit date against the boundary date.

### 3. Record the attribution

**Within window** — record all three fields:

| Field | Example |
|-------|---------|
| Author | `@alice` |
| Commit | `a1b2c3d` (short hash) |
| Date | `2025-01-15` |

Format in findings table: `@alice (a1b2c3d, 2025-01-15)`

**Outside window** — record as: `Legacy`

---

## Batch Attribution

When you have multiple findings, it's more efficient to get all blame data at once rather than per-finding:

```bash
# Get all authors for a file (within window)
git blame --since="$(git log -1 --format='%ai' $BOUNDARY)" -- <file>

# Get commit frequency by author in the last 100 commits
git log -100 --format='%an' | sort | uniq -c | sort -rn

# Get all files changed by a specific author in the last 100 commits
git log -100 --author="<name>" --name-only --format='' | sort -u
```

---

## "Recently Introduced Complexity" Section

After completing attribution for all findings, generate the report's "Recently Introduced Complexity" section:

1. Filter findings to only those within the 100-commit window
2. Group by author
3. For each author, list their findings sorted by severity (Critical > Major > Minor)

Example output:

```markdown
## Recently Introduced Complexity

Findings where git blame shows code authored within the last 100 commits.
This helps teams address the freshest debt first.

### @alice (3 findings)
| Severity | Dimension | Location | Issue |
|----------|-----------|----------|-------|
| Critical | Info Hiding | `src/api.ts:42` | Internal state exposed via getter |
| Major | Layering | `src/routes/index.ts:15` | Pass-through method adding no value |
| Minor | Naming | `src/utils.ts:88` | Vague variable name `data` |

### @bob (1 finding)
| Severity | Dimension | Location | Issue |
|----------|-----------|----------|-------|
| Major | Module Depth | `src/auth.ts:120` | Shallow wrapper around library call |

### Legacy (5 findings)
[Findings where code predates the 100-commit window — listed without author attribution]
```

---

## Edge Cases

- **File moved/renamed**: `git blame` follows renames by default. If it doesn't, use `git blame -C` for copy detection.
- **Bulk reformatting commits**: Use `git blame -w` to ignore whitespace changes, or `git blame --ignore-rev=<hash>` to skip known formatting commits.
- **Multiple authors on same lines**: Report the most recent author within the window.
- **No git history**: If the project has no git history (or fewer than 100 commits), note this in the report and skip attribution. Use total commit count as the window instead.
- **Shallow clone**: `git blame` may not work fully. Note this limitation if detected (`git rev-parse --is-shallow-repository`).
