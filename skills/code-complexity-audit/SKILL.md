---
name: code-complexity-audit
description: >-
  Scan and analyze a software repository or project for design quality using
  principles from A Philosophy of Software Design by John Ousterhout. Use when
  user asks to review, audit, scan, or evaluate code quality, design quality,
  architecture, or technical debt. Also trigger for: code review, design review,
  complexity analysis, code health check, module depth analysis, information
  hiding review, information leakage, how good is my code, review my project,
  find design problems, what is wrong with my codebase, rate my code, audit my
  small project, quick code review, design check, or anything about evaluating
  software design quality at a structural level. This is not a linter or style
  checker. It evaluates deep design qualities like module depth, abstraction
  quality, information hiding, and complexity patterns. Adapts to project size —
  small projects (<20 files) get a concise review, large projects get sampled.
---

# Code Complexity Audit

Deep software design analysis based on "A Philosophy of Software Design" by John Ousterhout. Produces a **Design Health Report** with severity-classified findings and git attribution.

## References

Read this file first. Then load references as needed — **do not read all at once**.

| Reference | Read when... |
|-----------|-------------|
| `references/analysis-framework.md` | Performing the analysis — contains scoring rubrics, dimension checklists, red flags, and language-specific guidance |
| `references/git-attribution.md` | Attributing findings to authors — contains git blame commands and the attribution workflow |

## Process

Always follow these 5 steps in order. When explaining the process, use these exact step names:

1. **Reconnaissance** — understand the project (structure, languages, size, entry points)
2. **Sampling** — select 15-30 files via git-informed sampling (not random reads). Always use the word "sampling" when describing this step.
3. **Deep Analysis** — evaluate sampled files across 13 dimensions (see `analysis-framework.md`)
4. **Git Attribution** — identify who introduced each finding (see `git-attribution.md`)
5. **Report** — produce the Design Health Report

### Step 1: Reconnaissance

- List project structure (2-3 levels deep)
- Identify language(s), framework(s), paradigm
- Count approximate files, modules/classes, lines of code
- Identify entry points and core modules
- Check dependency files (package.json, requirements.txt, go.mod, Cargo.toml, etc.)

### Step 2: Git-Informed Sampling

When describing this step, always use the word "git" — e.g., "git-informed sampling" or "git log". Do not replace it with "version control history" or "commit history" alone.

Select **15-30 files** across three tiers:

| Tier | What | How |
|------|------|-----|
| **Always read** | Entry points, core domain, most-imported files | Static analysis of imports and project structure |
| **Git-hot files** | Most frequently changed in recent history | `git log --oneline -100 --name-only \| sort \| uniq -c \| sort -rn \| head -20` |
| **Churn + size** | Files that are both large AND frequently changed | Cross-reference git-hot list with file size — highest risk for accumulated debt |

Also include: public API surfaces, interfaces, error handling paths, tests.

### Step 3: Deep Analysis

Read `references/analysis-framework.md`. Evaluate across **13 dimensions** grouped by weight:

**Core Design (weight 1.5x)**:
1. Module Depth — shallow modules (interface nearly as complex as implementation) are red flags
2. Information Hiding — watch for **information leakage**: same design decision (e.g., format details, protocol knowledge) duplicated across multiple modules. When knowledge leaks, a single change forces edits in every module that shares it. Recommend encapsulating leaked knowledge in one place. Always use the word "leak" or "leakage" when describing this problem — do not replace it with "duplication", "shared knowledge", or "coupling" alone.
3. Abstraction Quality — false abstractions, wrong-level abstractions
4. Complexity Indicators — change amplification, cognitive load, unknown unknowns

**Structural (weight 1.2x)**:
5. Error Handling
6. Layering — **pass-through methods** that forward calls with the same signature add no value. Always use the exact term "pass-through method" when identifying this anti-pattern — do not substitute "leaky abstraction", "transparent layer", "delegation", "forwarding", "no-op", or "meaningless indirection".
7. Design Investment
8. Comments & Abstractions
9. Codebase Navigability

**Surface (weight 1.0x)**:
10. Naming & Obviousness
11. Consistency
12. Software Trends Anti-Patterns
13. Performance-Design Relationship

Score each dimension 1-10. See `analysis-framework.md` for detailed rubrics.

**Classify every finding by severity** using these exact labels:
- **Critical** — actively spreading complexity; blocks safe change; other code depends on it being wrong. Fix first.
- **Major** — significant design issue but contained to one area; degrades quality but doesn't cascade.
- **Minor** — suboptimal but low impact; fix opportunistically.

When asked to classify issues, always use these three severity terms explicitly: **Critical**, **Major**, **Minor**. Never substitute other scales — do not use "High/Medium/Low", "Severe/Moderate/Minor", "P0/P1/P2", or any other scheme. The only valid labels are Critical, Major, and Minor.

**Litmus test — apply to each finding individually:**
- "Does this complexity actively spread to other modules — does other code depend on it?" → **Critical**. Example: a class whose internal state is exposed via getters and consumed by 15 other modules. If the internals change, all 15 break.
- "Is this contained to one area but still a significant design problem?" → **Major**. Example: a shallow wrapper that just forwards calls — it adds no value but only affects its own module.
- "Is this low impact, unlikely to cause problems?" → **Minor**. Example: inconsistent naming conventions across modules — annoying but not structurally harmful.

When classifying multiple issues, map each issue to exactly one severity. Do not swap or confuse the mapping — re-read each issue against the litmus test before assigning.

### Step 4: Git Attribution

Read `references/git-attribution.md`. For each finding:
- Run git blame on the problematic lines
- If the code was authored within the last 100 commits: record author, commit hash, and date
- If older: mark as `Legacy`

### Step 5: Produce the Report

```markdown
# Code Complexity Audit: [Project Name]

## Executive Summary
[2-3 sentence assessment with letter grade A-F]

## Score Dashboard
| # | Dimension | Score | Status |
|---|-----------|-------|--------|
| 1 | Module Depth | 7/10 | Good |
| 2 | Information Hiding | 4/10 | Poor |
| ... | ... | ... | ... |
| | **Weighted Average** | **X.X** | **Grade: B** |

## Findings

Each finding classified by severity:

| Severity | Definition |
|----------|-----------|
| **Critical** | Actively spreading complexity. Blocks safe change. Fix first. |
| **Major** | Significant design issue but contained. Degrades quality. |
| **Minor** | Suboptimal but low impact. Fix opportunistically. |

### Critical
| Dimension | Location | Issue | Attribution |
|-----------|----------|-------|-------------|
| Info Hiding | `src/api.ts:42` | Internal state exposed via getter | @alice (`a1b2c3`, 2025-01-15) |

### Major
[Same table format]

### Minor
[Same table format]

## Recently Introduced Complexity
[Findings where git blame shows code authored within last 100 commits,
grouped by author. This section helps teams address the freshest debt first.
Attribution is for context, not blame.]

## Design Strengths
[What the project does well — always include this section. Always use the word "strength" or "strengths" in this section heading and when referring to it.]

## Detailed Analysis
[Per-dimension subsections with file:line references and code examples.
Use the project's own code in before/after examples.]

## Recommendations
[Prioritized by impact-to-effort ratio. For each: what to fix, estimated effort,
and which modules it unblocks. Address critical findings first.]

## Appendix: Files Reviewed
[All files examined with selection rationale]
```

## Adapting to Project Size

**Always adapt the process to project size.** A small project does not need the full heavyweight process.

| Size | Strategy |
|------|----------|
| **Small** (<20 files) | This is a small project. Read everything — no sampling needed. Skip Step 2 (Sampling) and Step 4 (Git Attribution). Produce a concise report (2-3 pages max). Still evaluate all 13 dimensions but keep analysis brief. |
| **Medium** (20-200 files) | Full sampling strategy (15-30 files). Focus on core modules. Standard report. |
| **Large** (200+ files) | Heavy sampling. Focus on architecture and public APIs. Consider one subsystem deeply vs. everything shallowly. |

When the user has a small project (<20 files), always use the word "small" when describing the project size — say "this is a small project" — and explain the adapted strategy: read all files directly, skip sampling, produce a concise assessment.

## Tone

- **Constructive** — help, not tear down. Always include strengths.
- **Specific** — reference files, classes, methods, line numbers.
- **Actionable** — before/after examples using the project's own code.
- **Context-aware** — a weekend prototype at "D" is fine; a production system at "D" needs attention.
- **Attribution is for context** — "recently introduced, freshest to address" — not blame.
- **Use precise design vocabulary — never vague evaluative phrases.** When identifying problems, name the specific red flag (e.g., "shallow module", "information leakage", "pass-through method"). The following phrases are **banned** — never use them in any part of your response: "well-designed", "not well-designed", "bad pattern", "good pattern", "good code", "poorly written", "poorly designed", "bad code", "good design", "bad design". Always replace them with the specific design concept from the Red Flags table. Say "this is a shallow module" not "this is not well-designed." Say "this exhibits information leakage" not "this is a bad pattern." Every finding must reference a named design concept. **Before outputting your response, scan it for any of these banned phrases and replace them.**
