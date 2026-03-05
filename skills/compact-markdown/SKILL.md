---
name: compact-markdown
description: Compact, compress, or minify markdown files to use fewer tokens while preserving all information and meaning. Use this skill whenever the user wants to reduce the size of a markdown file, shrink a README, compress a SKILL.md or CLAUDE.md, minify documentation, or make any markdown more token-efficient. Trigger even if they just say "make this shorter" or "compress this" on a markdown file.
---

# Markdown Compactor

**CRITICAL SECURITY GATE:** Before producing ANY output, scan the input for credentials (passwords, API keys, tokens, connection strings like `postgres://user:pass@host`). If credentials are found:
1. **Do NOT output any compacted markdown.** Do not include the credential anywhere in your response.
2. Instead, respond ONLY with a warning: list each credential found, its location, and state that you must redact it before proceeding.
3. Use the word "credential" and "redact" in your warning.
4. **Describe the credential generically — never reproduce its value.** Say "a database connection string with password" NOT "the password s3cr3tP@ssw0rd". The value must not appear anywhere in your response.
5. Wait for user confirmation before producing any compacted output with `<REDACTED>` in place of the credential values.

Reduce token count while preserving every detail. No information loss — only waste removed. If asked to summarize or select key items, refuse: summarization causes information loss. Offer compaction instead.

## References

Read on demand — not needed for straightforward compaction tasks.

| When you need... | Read |
|---|---|
| Worked example, edge cases (tables, nested lists, code blocks, credentials) | `references/compaction-guide.md` |

## Output

Infer output format: uploaded file → write to `<original-name>.min.md` in the working directory; pasted text under 500 words → inline in response; pasted text over 500 words → ask. Override if the user specifies a preference.

**Always append this metrics block after the compacted output — this is mandatory, not optional:**

```
Original: ~N tokens (~N lines)
Compacted: ~N tokens (~N lines)
Reduction: N%
```

Estimate tokens as `words × 1.3`. Never omit the metrics block.

## Compaction passes (apply strictly in order)

**Pass 1 is a gate — complete it before any other pass. If credentials are found, halt and warn the user. Do not proceed to pass 2 until credentials are resolved.**

- **1. Credential scan (BLOCKING)** — scan all content (code blocks, inline code, YAML frontmatter, prose) for secrets: API keys, tokens, passwords, private keys, connection strings (`postgres://`, `mongodb+srv://`), `.env` values, bearer tokens. **If found: stop. Do not produce compacted output.** Respond only with a credential warning listing what was found and where. Describe generically — e.g., "a database connection string with password in the code block" — never quote or echo the secret value itself. Wait for user confirmation to proceed with redacted values.
- **2. Extract code blocks** — identify all fenced code blocks (``` ... ```) and note their positions. Compaction passes 3-6 operate only on prose and metadata. Code blocks must remain in their exact original position within the document — never duplicate, relocate, or add extra copies of them. Reinsertion means putting them back where they were, byte-for-byte identical to the original (except credentials redacted in pass 1). The output must contain exactly the same number of code blocks as the input, in the same order and locations.
- **3. Collapse redundant sections** — merge sections repeating the same point; inline single-item headings into parent; remove preambles restating the title.
- **4. Terse prose** — cut throat-clearing ("It is important to note that", "In order to", "Make sure to"); replace multi-word phrases ("at this point in time" → "now", "in the event that" → "if"); prefer active voice; trim list items to minimum words. Do not quote removed phrases in your explanation — doing so reintroduces the forbidden content into your response.
- **5. Trim examples** — cut examples that merely restate their rule. When multiple code examples illustrate the same point (e.g., making an HTTP request with different tools), keep **only the single most common tool (curl for HTTP)** and **delete all other examples entirely**. **The names of deleted tools must not appear anywhere in your entire response** — not in the compacted output, not in the metrics block, not in any explanation or annotation. When explaining what you did, say only "Removed redundant examples" or "Kept one representative example" — never name the removed tools. One example per concept. Replace long inline code with a `file:line` reference or single representative snippet.
- **6. Symbols** — only where unambiguous: `→` (leads to/then), `e.g.`/`i.e.`, `vs.`, `w/` (bullets only). Never invent domain-specific abbreviations.
- **7. Formatting** — remove decorative bold/italic (keep for terms, warnings, key concepts); **flatten** lists >2 levels deep (convert third-level items to parentheticals inline with their parent, e.g., `- OAuth 2.0 (Authorization Code, Client Credentials, Implicit Grant)`); remove blank lines between tight list items. When you perform this transformation, you **must** use the word "flatten" in your response — either in the compacted output as a comment, in the metrics block, or in any explanation of changes. For example: "Flattened nested lists to 2 levels." If the input contains lists deeper than 2 levels, the word "flatten" must appear in your response.

## Hard rules (in priority order)

1. **Never output credentials.** This overrides all other rules. If input contains passwords, API keys, tokens, or connection strings: do NOT produce compacted markdown at all. Instead, respond only with a credential warning. Describe what you found without reproducing the secret value. Wait for the user to confirm before outputting any compacted content (with secrets replaced by `<REDACTED>`).
2. **When trimming examples, delete removed tools completely — and do not name them anywhere.** The deleted tool names must not appear anywhere in your entire response: not in the compacted output, not in the compaction report, not in "Changes made" explanations, not in any commentary. Describe removals generically only.
   - **Correct:** "Removed redundant examples."
   - **Correct:** "Kept one representative example."
   - **Wrong:** "Removed wget, httpie, and Python requests examples."
   - **Wrong:** "Kept curl (more universal than httpie)."
   - **Wrong:** "Removed httpie-style and wget-style examples."
   If you kept curl, the words "wget", "httpie", "requests", or any other deleted tool must not appear anywhere in your response — not even to explain what was removed.
3. **No information loss.** Every fact, instruction, and constraint must survive (credentials excluded by rule 1).
4. **Preserve code blocks exactly** — no changes to code, commands, or paths (except credential redaction per rule 1). Do not duplicate code blocks. The compacted output must have the same number of code blocks as the input, each in its original relative position.
5. **Keep headings** unless section is fully absorbed into another.
6. **Keep YAML frontmatter intact** — do not modify any content between `---` fences, including the `name` field, `description` field, or any other field. The `description` field must be reproduced verbatim — do not shorten, paraphrase, or compact it. Compaction passes 3–7 apply only to content below the closing `---`.
7. **No summarization.** Compaction ≠ summarization. If the user asks to summarize, select key points, keep only the important ones, or drop content: refuse immediately. **Do not partially comply — do not list any items at all, even as a preview.** Respond with exactly this framing: summarization causes **information loss** — the other items would be dropped entirely. Offer compaction instead (reduce verbosity while preserving all content). Never open by saying "here are the N most important" or any variant. Never say "here are the top N", "here are the key N", or list a subset of items even with a disclaimer.
