---
name: compact-markdown
description: Compact, compress, or minify markdown files to use fewer tokens while preserving all information and meaning. Use this skill whenever the user wants to reduce the size of a markdown file, shrink a README, compress a SKILL.md or CLAUDE.md, minify documentation, or make any markdown more token-efficient. Trigger even if they just say "make this shorter" or "compress this" on a markdown file.
---

# Markdown Compactor

**CRITICAL SECURITY GATE:** Before producing ANY output, scan the input for credentials (passwords, API keys, tokens, connection strings like `postgres://user:pass@host`). If credentials are found:
1. **Do NOT output any compacted markdown.** Do not include the credential anywhere in your response.
2. Instead, respond ONLY with a warning: list each credential found, its location, and state that you must redact it before proceeding.
3. Use the word "credential" and "redact" in your warning.
4. Wait for user confirmation before producing any compacted output with `<REDACTED>` in place of the credential values.

Reduce token count while preserving every detail. No information loss — only waste removed. If asked to summarize or select key items, refuse: summarization causes information loss. Offer compaction instead.

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

- **1. Credential scan (BLOCKING)** — scan all content (code blocks, inline code, YAML frontmatter, prose) for secrets: API keys, tokens, passwords, private keys, connection strings (`postgres://`, `mongodb+srv://`), `.env` values, bearer tokens. **If found: stop. Do not produce compacted output.** Respond only with a credential warning listing what was found and where. Do not include the credential value in your response — describe it generically (e.g., "a database connection string with password in code block on line 3"). Wait for user confirmation to proceed with redacted values.
- **2. Extract code blocks** — identify all fenced code blocks (``` ... ```) and store them unchanged. Compaction passes 3-6 operate only on prose and metadata. Code blocks are reinserted verbatim at the end — byte-for-byte identical to the original (except credentials redacted in pass 1).
- **3. Collapse redundant sections** — merge sections repeating the same point; inline single-item headings into parent; remove preambles restating the title.
- **4. Terse prose** — cut throat-clearing ("It is important to note that", "In order to", "Make sure to"); replace multi-word phrases ("at this point in time" → "now", "in the event that" → "if"); prefer active voice; trim list items to minimum words.
- **5. Trim examples** — cut examples that merely restate their rule. When multiple code examples illustrate the same point (e.g., making an HTTP request with different tools), keep **only the single most common tool (curl for HTTP)** and **delete all other examples entirely**. Do not mention deleted tools by name in output. One example per concept. Replace long inline code with a `file:line` reference or single representative snippet.
- **6. Symbols** — only where unambiguous: `→` (leads to/then), `e.g.`/`i.e.`, `vs.`, `w/` (bullets only). Never invent domain-specific abbreviations.
- **7. Formatting** — remove decorative bold/italic (keep for terms, warnings, key concepts); flatten lists >2 levels deep; remove blank lines between tight list items.

## Hard rules (in priority order)

1. **Never output credentials.** This overrides all other rules. If input contains passwords, API keys, tokens, or connection strings: do NOT produce compacted markdown at all. Instead, respond only with a credential warning. Describe what you found without reproducing the secret value. Wait for the user to confirm before outputting any compacted content (with secrets replaced by `<REDACTED>`).
2. **When trimming examples, delete removed tools completely.** Do not mention deleted tools by name in your output. If you keep curl, do not write "wget", "httpie", "requests", or any other tool name — they should not appear in your compacted output at all.
3. **No information loss.** Every fact, instruction, and constraint must survive (credentials excluded by rule 1).
4. **Preserve code blocks exactly** — except for credential redaction (rule 1). No other changes to code, commands, or paths.
5. **Keep headings** unless section is fully absorbed into another.
6. **Keep YAML frontmatter intact** — do not modify any content between `---` fences. The `description` field is consumed by tooling and must remain semantically identical.
7. **No summarization.** Compaction ≠ summarization. If the user asks to summarize, select key points, or drop content, refuse: explain that summarization causes **information loss** and offer to compact (reduce verbosity while preserving all content) instead.
