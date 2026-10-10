# Facets

Facets are the qualities a product should be *perceived* to have. They replace "is it good?" with "is it calm enough? is it fast enough to feel expert?" and give every finding a reason to exist.

## Drafting 3–6 facets

1. **Extract signals** from what the user said. Listen for:
   - Audience: who, how often, how expert, under what pressure ("ops engineers during incidents", "first-time savers").
   - Comparisons: products they admire or want to beat ("like Linear", "not like Jira").
   - Adjectives they already use, even casually ("it should feel light").
   - Stakes: money, health, data, reputation. High stakes pull toward trustworthy and precise.
   - Frequency: daily tools pull toward fast and dense; occasional ones toward effortless and guided.
2. **Pick from the library below, then sharpen.** Swap generic words for the product's own: "trustworthy" becomes "trustworthy with my money"; "fast" becomes "keyboard-fast for triage".
3. **Check for tension.** Good sets usually contain one pair in tension (dense vs. calm, playful vs. trustworthy). That pair is where the interesting decisions are. If nothing is in tension, the set is probably too generic.
4. **Drop table stakes.** "Usable", "consistent", "reliable", "accessible" are the floor, not facets. They're covered by the rubric.
5. **Rank** them. Ask the user which one they'd protect if they could only keep one.
6. **Present for confirmation** in 3–6 lines, one per facet with a single-sentence definition. Don't score until the user confirms or says "go ahead".

Draft format:

```
Proposed facets (ranked), confirm or adjust:
1. Calm under pressure: nothing shouts unless it's actually urgent.
2. Expert-fast: a regular can triage an alert without touching the mouse.
3. Trustworthy with data: numbers look exact and their source is obvious.
4. Quietly crafted: details reward a second look without drawing attention.
```

## Facet library

Each entry: definition, what a 1 looks like, what a 5 looks like, and the usual levers.

**Calm**
Nothing competes for attention unless it needs it.
- 1: Multiple accents, badges everywhere, motion on idle, red used decoratively.
- 5: Muted palette, one accent, generous whitespace, urgency reserved for real urgency.
- Levers: reduce accent count, soften neutrals, cut idle motion, remove nonessential badges, lower density in non-task areas.

**Trustworthy**
The user believes what they see and feels safe acting on it.
- 1: Vague consequences, inconsistent numbers, layout shifts, no confirmation on irreversible actions.
- 5: Explicit consequences, precise figures with sources, stable layout, undo everywhere it matters.
- Levers: name consequences in copy, add undo, show last-updated times, eliminate layout shift, consistent formatting of money and dates.

**Dense / expert-fast**
Experts get more done per glance and per keystroke.
- 1: One item per screen, mouse-only, deep navigation, big padding everywhere.
- 5: High information density that still scans, keyboard shortcuts for everything, command palette, inline editing.
- Levers: tighter spacing scale for data views, tabular figures, shortcuts with visible hints, bulk actions, remember last choices.

**Playful / tactile**
Interacting feels physical and a little fun.
- 1: Flat, static, instant state swaps, nothing responds to touch.
- 5: Springs, press states with depth, satisfying micro-feedback, surprise in low-stakes moments.
- Levers: spring physics, scale on press, haptics, sound, illustrated empty states, playful copy in safe places.

**Crafted / hand-made**
Someone clearly cared about every detail.
- 1: Default component library untouched, misaligned icons, mixed radii, stock illustrations.
- 5: Custom details, optical alignment, concentric radii, considered type pairings, bespoke iconography.
- Levers: optical corrections, custom icons, typography features (ligatures, tabular figures), consistent radii, texture or illustration with a point of view.

**Effortless**
Things happen without the user having to think.
- 1: Many fields, manual configuration, unclear next step, errors after submit.
- 5: Smart defaults, inferred values, one clear next step, problems prevented rather than reported.
- Levers: remove fields, prefill, progressive disclosure, inline validation, automatic saving.

**Premium**
Feels expensive, considered and confident.
- 1: Crowded, loud, discount-y, low-res imagery, generic type.
- 5: Restraint, strong type, high-quality imagery, slow confident motion, lots of space.
- Levers: fewer elements, larger type contrast, refined palette, high-quality assets, slower ease-out motion, no exclamation marks.

**Bold**
Has a strong point of view and is recognizable at a glance.
- 1: Indistinguishable from a template.
- 5: Distinctive color, type or layout you'd recognize from a cropped screenshot.
- Levers: signature color used with conviction, oversized type, unconventional layout in hero moments, a recurring visual motif.

**Warm / human**
Feels made by people for people.
- 1: Cold grays, system jargon, passive voice, no faces or personality.
- 5: Warm palette, conversational copy, human imagery or illustration, empathetic errors.
- Levers: warmer neutrals, plain-language copy, first-person where apt, rounded forms, human photography.

**Precise**
Exact, technical, nothing approximate.
- 1: Rounded numbers without units, fuzzy alignment, ambiguous states.
- 5: Exact values, units, monospace where it helps, pixel-aligned grids, explicit states.
- Levers: tabular and monospace figures, units on everything, strict grid, clear state labels, timestamps with timezone.

**Alive / growing**
The product feels like it's evolving and responds to the user.
- 1: Static, same every visit, no sense of progress or change.
- 5: Reflects user progress, surfaces what's new, subtle ambient life, content that accumulates.
- Levers: progress visualizations, "new" surfacing, personalized states, gentle ambient motion, history and streaks.

**Focused**
One thing at a time; the current task owns the screen.
- 1: Sidebars, banners, upsells and notifications surround every task.
- 5: Distraction-free modes, one primary action per view, chrome recedes during tasks.
- Levers: hide chrome during tasks, defer notifications, one primary action, full-screen editing.

**Fast**
Perceived speed: it responds before the user doubts it.
- 1: Spinners on every action, full-page reloads, input lag.
- 5: Optimistic updates, instant feedback, prefetching, no visible waiting on common paths.
- Levers: optimistic UI, skeletons that match layout, prefetch on hover, shorter animations, local-first data.

**Native-feeling**
Behaves like a first-class citizen of its platform.
- 1: Web-in-a-wrapper, wrong gestures, custom controls that ignore platform conventions.
- 5: Platform gestures, system fonts and controls where expected, respects dark mode, dynamic type, safe areas.
- Levers: platform components, correct back behavior, swipe gestures, system type scales, haptics, respect OS settings.

**Editorial**
Reads like a well-made publication: content first, strong typographic voice.
- 1: UI chrome dominates, type is uniform, images are thumbnails.
- 5: Clear typographic hierarchy, generous measure, considered image crops, pacing across the page.
- Levers: serif or display pairing, larger body and measure control, pull quotes, full-bleed images, rhythm in section spacing.

Combine or rename freely. "Calm + precise" can become "instrument-grade"; "warm + effortless" can become "like a helpful friend".

## Scoring

Score after the user confirms the set. Define both ends before scoring: 1 = the minimum you'd accept for this product, 5 = the best you can imagine for it. Whole numbers only; half points hide indecision. Every score needs one line of evidence pointing to something observable.

Template:

```
| Rank | Facet | Score | Evidence | To raise one point |
| --- | --- | --- | --- | --- |
| 1 | Calm under pressure | 2 | Three red elements on the default dashboard; only one is an alert. | Reserve red for active incidents; move "Upgrade" badge to settings. |
| 2 | Expert-fast | 4 | J/K navigation and command palette present; bulk actions need the mouse. | Add shortcut for "acknowledge selected". |
| 3 | Trustworthy with data | 3 | Values exact, but no last-updated time on any chart. | Timestamp each chart with relative time and tooltip for absolute. |
| 4 | Quietly crafted | 3 | Consistent 8px radii; icons misaligned with labels in sidebar. | Optical-center sidebar icons on x-height. |
```

Reading the scores:

- Low score on rank 1: a reason not to ship. Say so.
- Low score on rank 5–6: acceptable for now if the rest is strong. Say that too.
- All 4s and 5s: either the work is excellent or the facets are too easy. Check whether the 5 definition is ambitious enough.
- When comparing versions, show both scores and the delta.

## Text radar

When a chart isn't available, use a bar per facet. Five cells, filled `█` for the score, `░` for the rest. Keep facet names aligned.

```
Calm under pressure     ██░░░  2
Expert-fast             ████░  4
Trustworthy with data   ███░░  3
Quietly crafted         ███░░  3
```

For two versions, put them side by side:

```
                        A       B
Calm under pressure     ██░░░   ████░   +2
Expert-fast             ████░   ████░    0
Trustworthy with data   ███░░   ██░░░   -1
Quietly crafted         ███░░   ████░   +1
```

When the environment can render visuals (an artifact, HTML page, notebook, or image output), draw a real radar chart instead: one axis per facet, scale 0–5, and overlay versions in two distinguishable colors with a legend. Keep the table alongside it, because the evidence column is what makes the scores useful.
