# Document Generator Template

Use this template when building a skill for producing structured documents — reports, proposals, memos, decks, handoff docs, or any formatted deliverable that follows a consistent pattern.

## How to Customize

Replace everything in `[brackets]` with the user's specifics. Delete sections that don't apply.

---

## Template SKILL.md

```markdown
---
name: [name]-doc-generator
description: Generates [document type] following [team/company]'s format and standards. Use when user asks to "create a report", "write a proposal", "generate a [doc type]", "make a deck", "draft a memo", or mentions [specific document names or workflows]. Also trigger for "put this into a document", "format this as a report", or any request to produce a polished [document type].
---

# [Document Type] Generator

## Purpose

This skill creates [document type] that [what they're used for — e.g., "summarize project progress for stakeholders", "propose new initiatives to leadership", "hand off designs to engineering"].

## Document Structure

Every [document type] follows this structure:

### Required Sections

1. **[Section 1, e.g., "Executive Summary"]**
   - Length: [e.g., 2-3 paragraphs]
   - Content: [what goes here]
   - Tone: [e.g., concise and outcome-focused]

2. **[Section 2, e.g., "Background / Context"]**
   - Length: [e.g., 1-2 paragraphs]
   - Content: [what goes here]
   - Include: [e.g., relevant data, timeline, stakeholders]

3. **[Section 3, e.g., "Key Findings / Recommendations"]**
   - Format: [e.g., numbered list with brief explanations]
   - Each item should include: [e.g., the finding, supporting evidence, recommended action]

4. **[Section 4, e.g., "Next Steps"]**
   - Format: [e.g., table with columns: Action, Owner, Deadline]
   - Keep it: [e.g., actionable and specific, no vague language]

### Optional Sections (include when relevant)

- **[Optional Section 1, e.g., "Appendix"]** — Use when: [condition]
- **[Optional Section 2, e.g., "Risk Assessment"]** — Use when: [condition]

## Formatting Standards

- **File format:** [e.g., .docx, .md, .pdf]
- **Headings:** [e.g., Title Case for H1/H2, Sentence case for H3+]
- **Font / style:** [e.g., use default professional formatting, match company template]
- **Tables:** [e.g., use tables for any comparison of 3+ items]
- **Length:** [e.g., 2-5 pages typical, never exceed 10]

## Tone and Language

- Write for [audience — e.g., "senior leadership who have 5 minutes to skim"]
- [e.g., Use active voice, avoid passive constructions]
- [e.g., Lead with conclusions, then support with evidence]
- [e.g., No jargon unless the audience expects it]
- [e.g., Every paragraph should earn its place — cut anything that doesn't add value]

## Process

1. **Gather inputs.** Ask the user for: [list of required inputs — e.g., "project name, date range, key metrics, any specific points to highlight"]. If information is missing, ask for it rather than guessing.

2. **Generate the document** following the structure and formatting standards above.

3. **Quality check before delivering:**
   - Does every required section have substantive content?
   - Is the executive summary genuinely useful on its own?
   - Are next steps specific (who, what, when)?
   - Is the total length appropriate?
   - Would the intended audience find this clear and actionable?

4. **Deliver** the document as a [file format] file. Give a brief summary of what's in it and ask if anything needs adjustment.

## Examples

### Good Executive Summary
> [Paste or write an example of what a good executive summary looks like for this document type. Be specific — use realistic-sounding content.]

### Bad Executive Summary
> [Paste or write an example of what to avoid — too vague, too long, missing key info, etc.]

## Common Variations

- **[Variation 1, e.g., "Quarterly Review"]:** [How it differs — e.g., "Include YoY comparison table, add metrics dashboard section"]
- **[Variation 2, e.g., "Quick Update"]:** [How it differs — e.g., "Skip background section, keep to 1 page, bullet-point format"]
```

---

## Customization Checklist

When filling in this template, make sure you've captured:

- [ ] Clear document structure with required vs optional sections
- [ ] Specific content guidance for each section (not just a title)
- [ ] Formatting standards (file type, length, heading style)
- [ ] Audience and tone
- [ ] At least one example of good output
- [ ] Common variations of the document
- [ ] Required inputs the user needs to provide
