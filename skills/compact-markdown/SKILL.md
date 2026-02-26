---
name: compact-markdown
description: Compact, compress, or minify markdown files to use fewer tokens while preserving all information and meaning. Use this skill whenever the user wants to reduce the size of a markdown file, shrink a README, compress a SKILL.md or CLAUDE.md, minify documentation, or make any markdown more token-efficient. Trigger even if they just say "make this shorter" or "compress this" on a markdown file.
---

# Markdown Compactor

Reduce token count while preserving every detail. No information loss — only waste removed.

## Output

Infer preference from context (uploaded file → file output; pasted text → inline), or ask.

File output path: `/mnt/user-data/outputs/<original-name>.min.md`.

After compacting, report:

```
Original: ~N tokens (~N lines)
Compacted: ~N tokens (~N lines)
Reduction: N%
```

Estimate tokens as `words × 1.3`.

## Compaction passes (apply in order)

- **1. Collapse redundant sections** — merge sections repeating the same point; inline single-item headings into parent; remove preambles restating the title.
- **2. Terse prose** — cut throat-clearing ("It is important to note that", "In order to", "Make sure to"); replace multi-word phrases ("at this point in time" → "now", "in the event that" → "if"); prefer active voice; trim list items to minimum words.
- **3. Trim examples** — cut examples that merely restate their rule; keep one (most concrete) when multiples illustrate the same point; replace long inline code with a `file:line` reference or single representative snippet.
- **4. Symbols** — only where unambiguous: `→` (leads to/then), `e.g.`/`i.e.`, `vs.`, `w/` (bullets only). Never invent domain-specific abbreviations.
- **5. Formatting** — remove decorative bold/italic (keep for terms, warnings, key concepts); flatten lists >2 levels deep; remove blank lines between tight list items.

## Hard rules

- **No information loss.** Every fact, instruction, and constraint must survive.
- **Preserve code blocks exactly.** No changes to code, commands, or paths.
- **Keep headings** unless section is fully absorbed into another.
- **Keep YAML frontmatter intact.**
- **No summarization.** Compaction ≠ summarization — shorter, not lossy.
