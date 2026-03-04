# Compaction Passes

Apply in order when user selected compact or both.

1. **Collapse** — merge sections repeating the same point; inline single-item headings into parent; remove preambles restating the title.
2. **Terse** — cut filler ("It is important to note that", "In order to", "Make sure to"); prefer active voice; trim list items to minimum words.
3. **Trim examples** — cut examples that restate their rule; keep one when multiples illustrate the same point.
4. **Formatting** — remove decorative bold/italic (keep for terms, warnings); flatten lists >2 levels deep.

## Hard Rules

- No information loss — every fact, instruction, and constraint must survive.
- Preserve code blocks exactly.
- Keep YAML frontmatter intact.
- Keep headings unless section is fully absorbed into another.
- Compaction is not summarization — shorter, not lossy.
