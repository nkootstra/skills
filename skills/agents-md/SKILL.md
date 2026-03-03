---
name: agents-md
description: Write, audit, and improve agent context files (AGENTS.md, CLAUDE.md) for AI coding agents. Use when creating or improving agent context for a codebase.
---

This skill covers agent context files — AGENTS.md (OpenCode, multi-agent harnesses) and CLAUDE.md (Claude Code). The principles are the same; only the loading mechanics differ. When the user's harness uses CLAUDE.md, substitute accordingly. These principles apply regardless of language or framework.

Include only what genuinely helps, cut what doesn't earn its place — but never delete useful information without relocating it first.

## References

Read on demand — do not load all reference files at once.

| When the user mentions... | Read |
|---|---|
| Auditing an existing file | `references/audit-example.md` |
| Testing, TDD, test conventions | `references/tdd.md` |

## Core Principles

- **Minimum viable requirements.** Ask of each line: "Does this earn its cost on nearly every session?" If not, cut it. Every line loads on every session — brevity has direct cost benefits.
- **Two failure modes.** (1) *Length* — as instruction count grows, compliance degrades uniformly, not just for new instructions. (2) *Task-irrelevant requirements* — correct instructions not needed for the current task still get followed, increasing cost and reducing success.
- **Compaction is not summarization.** When reducing a file, relocate correct content to scoped sub-files or `@import` targets — never paraphrase or drop details. The goal is fewer lines *in the root file*, not fewer lines total.
- **Don't send an LLM to do a linter's job.** Style guidelines add instructions and irrelevant context. Use actual linters, wired to hooks if the harness supports it.
- **Don't ship auto-generated files unedited.** Tools like `/init` are a fine starting point, but auto-generated output is stuffed with documentation the agent can already read. Always rewrite by hand before committing.
- **Architecture and overview sections have weak evidence** in root files. Exception: scoped sub-files can carry richer context — they only load when the agent is already working in that area.

## Single File vs. Hierarchical System

**Single root file** for simple projects: one app, one language, one team. Target under 200 lines — long enough to cover real conventions, short enough that compliance doesn't degrade. Every line still needs to earn its place.

**Hierarchical system** for monorepos, large codebases, or multiple apps/packages/services. The harness auto-loads context files as the agent navigates — `apps/web/AGENTS.md` only loads when the agent works there.

### Managing File Size Without Losing Content

When a root file grows past ~200 lines, use these mechanisms to relocate content rather than delete it:

**`@import` pointers** — reference external files that load alongside the root file:
```markdown
## Reference
- @docs/api-conventions.md
- @docs/testing-strategy.md
```

**Path-scoped rules** (Claude Code `.claude/rules/`) — instructions that only load when the agent touches matching files:
```markdown
# .claude/rules/api-design.md
---
paths:
  - "src/api/**"
---
All API endpoints must include input validation and OpenAPI comments.
```

**Scoped sub-files** — AGENTS.md or CLAUDE.md in subdirectories, loaded on demand when the agent works in that area.

Choose the mechanism that matches the harness. The principle is the same: move content to where it loads only when relevant, instead of deleting it.

### Hierarchical Rules

**Place files at semantic boundaries** — where responsibilities shift or contracts matter. Not in every directory.

**Least Common Ancestor for shared knowledge** — shared facts belong in the shallowest file covering all relevant paths. Never duplicate across siblings.

**Downlink from parent to children** — reference child files so the agent can follow the hierarchy:

```
## Sub-areas
- `packages/ui/AGENTS.md` — component library conventions
- `apps/api/AGENTS.md` — API server, auth, database access
```

**Build leaf-first** — write deepest files first. Parents summarize children's AGENTS.md files, not raw code.

**Scoped files can be richer** — entry points, invariants, and pitfalls are appropriate in a file that only loads for one service.

## Writing a New AGENTS.md

```markdown
# Project or Area Name

One sentence: what it does and why it exists.

## Stack
Tech stack. Package manager or build tool (be explicit — agents assume defaults).
Path aliases if non-standard. Infrastructure if non-obvious (DB, cache, queue).
Directory tree only if ownership boundaries aren't obvious. 1-2 levels max.

## Development
Verification commands only: typecheck, lint, test. What to run before finishing.
Skip inferrable commands. Include non-obvious ones whose names don't reveal purpose
(e.g. `cf-typegen`, `db:migrate`, `dotnet ef database update`).

## Conventions
Only things the agent can't infer from reading the code.
No style rules — use a linter.
```

A Reference Docs section is fine — only add a pointer if the agent genuinely needs to read it before working in that area.

## Auditing an Existing AGENTS.md

**Auditing is refactoring, not summarization.** Every piece of correct, useful information must end up somewhere — in the root file, a scoped sub-file, a rules file, or an `@import` target. Never compress or summarize content to reduce line count. If a detail was worth writing, it's worth preserving in the right location.

### Audit Workflow

1. **Measure.** Count total lines, distinct instructions, style rules, overview sections.
2. **Classify each instruction:**
   - *Essential and universal* → keep in root file
   - *Correct but scoped to a specific area* → **move** to a scoped sub-file or path-scoped rule, add a pointer from root
   - *Style/lint rule* → remove (enforce via linter/hook instead)
   - *Redundant, stale, or inferrable* → remove
3. **Relocate before removing.** For any content classified as "move": create the destination file with the full original content, then replace it in the root with a pointer. Do not paraphrase or summarize the moved content.
4. **For hierarchical systems:** check whether root content belongs in a scoped sub-file, and whether sub-files duplicate knowledge that belongs at their LCA.
5. **Present results:** before/after line counts per file, what was moved and where, what was removed and why, and the complete rewritten file(s) including any new sub-files.

## Maintenance

On significant changes, update affected AGENTS.md files leaf-first. A CI agent that detects changed files and proposes updates is worth building.

### Testing Effectiveness

An AGENTS.md is working if the agent's behavior changes. After writing or auditing:

1. Run a representative task *without* the file and note where the agent deviates from your expectations.
2. Add/update instructions targeting those deviations.
3. Re-run the same task and verify the behavior shifts.

If the agent keeps doing something wrong despite having a rule against it, the file is likely too long and the rule is getting lost. If the agent asks questions that are answered in the file, the phrasing may be ambiguous.

### Monorepo Exclusions

In large monorepos, ancestor context files from other teams may load and add irrelevant context. Claude Code supports `claudeMdExcludes` in `.claude/settings.local.json` to skip specific files:

```json
{
  "claudeMdExcludes": [
    "**/other-team/CLAUDE.md",
    "/repo/root/unrelated-service/.claude/rules/**"
  ]
}
```

This keeps each team's agent context focused without affecting other teams.

## Anti-Patterns to Flag

**Command dump** — inferrable commands like `dev`, `build`, `start` listed in full.

**Deep tree** — directory structures more than 2 levels deep. Replace with a sentence.

**Architecture tour** — system overviews in a root file. One sentence of purpose, or push into a scoped sub-file.

**Style guide** — formatting rules. Use a linter.

**Code museum** — large inline snippets. Use `file:line` references.

**Hotfix graveyard** — accumulated one-off corrections. Delete them.

**Auto-generated blob** — output from auto-init commands. Rewrite by hand before committing.

**Stale reference** — outdated paths or commands. Update or remove.

**Duplicated siblings** — the same fact in two sub-files. Hoist to their LCA.
