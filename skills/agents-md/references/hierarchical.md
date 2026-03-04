# Hierarchical Systems

For monorepos, large codebases, and multi-app/package/service setups.

## Managing File Size

When root exceeds ~200 lines, relocate content (don't delete):

**`@import` pointers** — load alongside the root file:
```markdown
## Reference
- @docs/api-conventions.md
- @docs/testing-strategy.md
```

**Path-scoped rules** (Claude Code `.claude/rules/`) — load only when matching files are touched:
```markdown
# .claude/rules/api-design.md
---
paths:
  - "src/api/**"
---
All API endpoints must include input validation and OpenAPI comments.
```

**Scoped sub-files** — AGENTS.md/CLAUDE.md in subdirectories, loaded on demand.

Match the mechanism to the harness. Move content to where it loads only when relevant.

## Hierarchical Rules

- **Semantic boundaries** — place files where responsibilities shift or contracts matter. Not every directory.
- **Least Common Ancestor** — shared facts in the shallowest file covering all relevant paths. Never duplicate across siblings.
- **Downlink parent → children:**
```
## Sub-areas
- `packages/ui/AGENTS.md` — component library conventions
- `apps/api/AGENTS.md` — API server, auth, database access
```
- **Build leaf-first** — deepest files first. Parents summarize children's AGENTS.md, not raw code.
- **Scoped files can be richer** — entry points, invariants, pitfalls are appropriate when only loaded for one service.

## Monorepo Exclusions

Ancestor context files from other teams may add irrelevant context. Claude Code supports `claudeMdExcludes` in `.claude/settings.local.json`:

```json
{
  "claudeMdExcludes": [
    "**/other-team/CLAUDE.md",
    "/repo/root/unrelated-service/.claude/rules/**"
  ]
}
```
