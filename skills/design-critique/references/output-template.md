# Output Template

Copy-ready skeletons for the report described in SKILL.md. Fill every bracket; delete sections the user explicitly didn't ask for. Findings follow the formula and severity scale in [rubric.md](rubric.md); facets follow [facets.md](facets.md).

## Single design

```markdown
## Overall read

[2–3 sentences. What it is, what works, the single biggest problem.] Relative to [platform or reference products, e.g. "current iOS system apps" or "Linear and Notion"], this sits [below / at / above] the baseline: [one concrete reason].

## Observations

| # | Severity | Where | Observation | Why it matters | Direction |
| --- | --- | --- | --- | --- | --- |
| 1 | Blocker | [Screen > region] | **[Issue]**: [what is there, with counts, quoted text, values] | [Impact on task or facet] | [Where to go] |
| 2 | Major | | | | |
| 3 | Minor | | | | |
| 4 | Polish | | | | |

**What works** (keep these):
- **[Strength]**: [specific observation and why it works, same precision as problems].
- **[Strength]**: [...]

## Facet scores

| Rank | Facet | Score | Evidence |
| --- | --- | --- | --- |
| 1 | [Facet] | [1–5] | [One observable line] |
| 2 | [Facet] | | |
| 3 | [Facet] | | |

[Text radar or chart, see facets.md]

[One sentence on ship-readiness given the top-ranked facet.]

## Next moves

1. **[Change]**: [what to do, which findings it resolves (#1, #3), which facet it raises and by roughly how much].
2. **[Change]**: [...]
3. **[Change]**: [...]
```

Notes:

- Order observations by impact: severity first, then reach (how many users, how often).
- Keep table cells short. If an observation needs more than ~40 words, put the finding in the table with a short label and expand below the table under `### #N detail`.
- If facets aren't confirmed yet, replace the facet section with the draft list from facets.md and stop after observations, or score provisionally and mark the table "provisional".
- Tables render badly in some terminals. If the output is plain text, use a numbered list with the same fields in the same order.

## Comparing two versions (A vs B)

```markdown
## Overall read

[2–3 sentences. Which is stronger overall and on which facet the difference is largest.] A sits [below / at / above] baseline; B sits [below / at / above]. [Recommendation: ship A, ship B, or combine: name what to take from each.]

## What changed

- [Concrete difference 1, e.g. "B removes the sidebar and moves filters into a popover"]
- [Concrete difference 2]
- [Concrete difference 3]

## Facet comparison

| Rank | Facet | A | B | Delta | Evidence |
| --- | --- | --- | --- | --- | --- |
| 1 | [Facet] | 3 | 4 | +1 | [What in B moves it] |
| 2 | [Facet] | 4 | 2 | -2 | [What B lost] |

[Side-by-side text radar or overlaid radar chart]

## Observations

| # | Version | Severity | Where | Observation | Why it matters | Direction |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | B | Major | | **[Issue]**: [...] | | |
| 2 | Both | Minor | | | | |
| 3 | A | Polish | | | | |

**Regressions** (worse in B than A): [list by # or "none"]
**Improvements kept** (better in B, protect them): [list]

## Next moves

1. [Highest-leverage change to the recommended version]
2. [What to port from the other version]
3. [Optional: what to test if the choice is still unclear]
```

Notes:

- Compare on the same facets and the same scale. Don't add facets mid-comparison.
- Mark which version each observation applies to: A, B, or Both. Issues present in both are often the real problem and get overlooked.
- A version can win on facets and still lose on a blocker. Call it out.

## Critique language

Rewrite vague, judgmental or unactionable phrasing into findings. Each pair: bad, then good.

1. Bad: "The layout feels cluttered."
   Good: "**Competing regions**: the dashboard has 9 cards of equal size and weight, 4 with charts. With no summary card, the eye scans all 9 before finding the health status."

2. Bad: "The colors are off."
   Good: "**Two competing accents**: links use #2563EB and primary buttons use #7C3AED, both at full saturation. Neither reads as 'the' action color, which dilutes 'focused'."

3. Bad: "Make the text bigger."
   Good: "**Small body text**: descriptions are 13px #6B7280 at 1.35 line height. That's below comfortable reading for paragraphs of 3+ lines; 15–16px in a darker neutral would fix it."

4. Bad: "It feels slow."
   Good: "**Late feedback**: tapping 'Save' shows nothing for ~800ms, then a full-screen spinner for 1.2s. The user taps twice. Show the pressed state immediately and update optimistically."

5. Bad: "This isn't very intuitive."
   Good: "**Hidden affordance**: rows are draggable, but there's no handle and the cursor stays default on hover. Nobody will discover reordering without being told."

6. Bad: "I don't like the font."
   Good: "**Type undercuts 'editorial'**: headings and body are both Inter 400/600, so the article page reads like a settings screen. A display or serif pairing for headings would carry the editorial facet, currently at 2."

7. Bad: "Error handling needs work."
   Good: "**Dead-end error**: a failed upload shows 'Error 413' in a toast that disappears after 3s. Say 'File is over 25 MB', keep it inline next to the file, and offer 'Compress' or 'Choose another'."

8. Bad: "Nice job, looks great!"
   Good: "**Clear landing point**: the single filled 'Start trial' button is the only saturated element above the fold, so the eye lands there in under a second. Keep that restraint when adding the pricing toggle."

9. Bad: "Spacing is inconsistent."
   Good: "**No spacing scale**: card padding measures 20, 24 and 18px across the three pricing tiers, and gaps between them are 28 and 32px. Snap to 24 and 32 from the existing 8px scale."

10. Bad: "The modal animation is weird."
    Good: "**Wrong origin**: the share modal scales up from screen center, but it's triggered from a button in the top-right corner. Scaling from the trigger would connect cause and effect."

11. Bad: "You should just use a different approach here."
    Good: "**Concept mismatch**: the wizard has 6 steps for a task expert users do daily, which caps 'expert-fast' at 2 regardless of polish. Worth exploring a single-form or inline-edit alternative before refining this flow."

12. Bad: "Accessibility could be better."
    Good: "**Invisible focus**: `outline: none` on all buttons with no replacement. Keyboard users can't see where they are on any screen. Blocker; add a 2px ring at 3:1 contrast."

Patterns behind the rewrites: name the thing, count or measure it, say what it does to the user or a facet, point a direction. Praise gets the same treatment.
