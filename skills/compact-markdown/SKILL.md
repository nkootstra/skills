---
name: compact-markdown
description: Compact, compress, or minify markdown files to use fewer tokens while preserving all information and meaning. Use this skill whenever the user wants to reduce the size of a markdown file, shrink a README, compress a SKILL.md or CLAUDE.md, minify documentation, or make any markdown more token-efficient. Trigger even if they just say "make this shorter" or "compress this" on a markdown file.
---

# Markdown Compactor

**CRITICAL: Never output real credentials.** Before ANY compaction, scan for passwords, API keys, tokens, connection strings (e.g., `postgres://user:pass@host`). If found, replace with `<REDACTED>` and warn the user. Never include the original credential value in your output — not even inside code blocks. This is a security requirement that overrides all other instructions.

Reduce token count while preserving every detail. No information loss — only waste removed.

## References

Read on demand — not needed for straightforward compaction tasks.

| When you need... | Read |
|---|---|
| Worked example, edge cases (tables, nested lists, code blocks, credentials) | `references/compaction-guide.md` |

## Output

Infer output format: uploaded file → write to `<original-name>.min.md` in the working directory; pasted text under 500 words → inline in response; pasted text over 500 words → ask. Override if the user specifies a preference.

After compacting, report:

```
Original: ~N tokens (~N lines)
Compacted: ~N tokens (~N lines)
Reduction: N%
```

Estimate tokens as `words × 1.3`.

## Compaction passes (apply strictly in order)

**Pass 1 is a gate — complete it before any other pass. If credentials are found, halt and warn the user. Do not proceed to pass 2 until credentials are resolved.**

- **1. Credential scan (BLOCKING)** — before any compaction, scan all content (code blocks, inline code, YAML frontmatter, prose) for patterns resembling secrets: API keys, tokens, passwords, private keys, connection strings (`postgres://`, `mongodb+srv://`), `.env` values (`DB_PASSWORD=`, `API_KEY=`, `SECRET=`), bearer tokens. If found: (a) warn the user listing each credential and its location, (b) replace with `<REDACTED>`, (c) do not output the original credential value. Preserve only if the user explicitly confirms they are dummy/example values.
- **2. Extract code blocks** — identify all fenced code blocks (``` ... ```) and store them unchanged. Compaction passes 3-6 operate only on prose and metadata. Code blocks are reinserted verbatim at the end — byte-for-byte identical to the original (except credentials redacted in pass 1).
- **3. Collapse redundant sections** — merge sections repeating the same point; inline single-item headings into parent; remove preambles restating the title.
- **4. Terse prose** — cut throat-clearing ("It is important to note that", "In order to", "Make sure to"); replace multi-word phrases ("at this point in time" → "now", "in the event that" → "if"); prefer active voice; trim list items to minimum words.
- **5. Trim examples** — cut examples that merely restate their rule. When multiple code examples illustrate the same point (e.g., making an HTTP request with different tools like curl, wget, httpie, Python requests), keep **only curl** and **delete all others entirely** — do not mention the removed tools by name, do not keep them as alternatives, do not reference them. One example per concept. Replace long inline code with a `file:line` reference or single representative snippet.
- **6. Symbols** — only where unambiguous: `→` (leads to/then), `e.g.`/`i.e.`, `vs.`, `w/` (bullets only). Never invent domain-specific abbreviations.
- **7. Formatting** — remove decorative bold/italic (keep for terms, warnings, key concepts); flatten lists >2 levels deep; remove blank lines between tight list items.

## Hard rules

- **Never output credentials.** If content contains what appear to be real API keys, tokens, passwords, private keys, or connection strings, redact them and warn the user. Halt compaction until resolved. Preserve only after explicit user confirmation they are dummy/example values.
- **No information loss.** Every fact, instruction, and constraint must survive (credentials excluded — see above).
- **Preserve code blocks exactly.** Extract all fenced code blocks before compacting prose. Reinsert them unchanged — byte-for-byte identical to the original. The only permitted modification inside code blocks is credential redaction (pass 1). No reformatting, no shortening, no altering commands or paths.
- **Keep headings** unless section is fully absorbed into another.
- **Keep YAML frontmatter intact** — do not modify any content between `---` fences. The `description` field is consumed by tooling and must remain semantically identical.
- **No summarization.** Compaction ≠ summarization — shorter, not lossy.
