# Anti-Patterns

Flag these when auditing or reviewing an AGENTS.md.

- **Command dump** — inferrable commands listed in full (`dev`, `build`, `start`)
- **Deep tree** — directory structures >2 levels. Replace w/ a sentence.
- **Architecture tour** — system overviews in root. One sentence of purpose, or push to sub-file.
- **Style guide** — formatting rules. Use a linter.
- **Code museum** — large inline snippets. Use `file:line` references.
- **Hotfix graveyard** — accumulated one-off corrections. Delete them.
- **Auto-generated blob** — unedited `/init` output. Rewrite before committing.
- **Stale reference** — outdated paths or commands. Update or remove.
- **Duplicated siblings** — same fact in two sub-files. Hoist to LCA.
