---
name: design-exploration
description: Generate genuinely different design directions, then refine the chosen one through many deliberate levels of quality. Use whenever the user is designing a feature, flow, component, screen, interaction, landing page or product concept and wants ideas, options, alternatives, or to make something "better", "great" or "less generic", or asks to brainstorm concepts or generate many variations of an idea. Also use when the user seems stuck on their first idea or is iterating on a single component.
effort: high
metadata:
  author: Niels Kootstra
  version: "1.1.0"
---

# Design Exploration: Range, then Depth

Two disciplines, done in order. **Range**: explore structurally different concepts before committing. **Depth**: push the chosen concept far past where most work stops. Throughout, prefer doing fewer things exceptionally well over adding more.

## Reference files

- Load [range-techniques.md](references/range-techniques.md) before generating directions, and whenever two directions start to share a mechanism. It has the job-to-be-done framing, the mechanism axes, a range-or-variant test, visual movements to borrow, the generic AI aesthetic to avoid, a prompt bank per technique, a worked example, and the presentation and recommendation format.
- Load [depth-ladder.md](references/depth-ladder.md) once a direction is chosen, to show the climb. It has level descriptions, moves per band, a worked climb, a levels log template, ceiling signs, and the what-to-cut checklist.

## Part 1: Range

The first idea usually arrives fast because it's something already seen. It may be fine, but committing to it immediately means optimizing inside an unexamined assumption. Often the best answer questions whether the task needs the user at all, for instance making a manual chore automatic so no interface is needed.

**Variants are not range.** Three styles of numeric keypad are depth on one concept. Range means changing the *core mechanism*: presets vs. a slider vs. a game vs. no UI at all.

Techniques for widening range:

- **Remove or add a constraint.** What if it weren't a screen? Happened automatically? Had to work one-handed or in three seconds? Ignore real constraints temporarily, then adapt good ideas back.
- **Borrow from another domain.** What if it were a game, a physical object, a ritual, or made by a brand with a strong point of view?
- **Invert the problem.** Instead of helping people pick what they want, help them eliminate what they don't.
- **Set a quota.** Force 5, 12 or 20 directions. The later ones are where surprises live.
- **Max out one quality.** What's the 10/10 version on durability? On delight? On speed? On distinctiveness?

When presenting range, give each direction a short name, a one-line description of its core mechanism, and its main trade-off. Make them meaningfully different; if two share a mechanism, merge them. Range also protects against limited taste: exploring unfamiliar directions is how taste expands.

## Part 2: Depth

Picture the chosen idea on a 1–10 scale. Level 1 technically works. Level 10 is the version where everything has been considered, tried, edited and improved until nothing is left to improve. Most shipped work sits at 2–3, not because more was impossible but because pushing stopped.

The work changes character as you climb:

- **Early levels: fixing.** Close obvious gaps, broken states, edge cases, inconsistencies.
- **Later levels: inventing.** It's no longer obvious what "better" is. Progress comes from discovery, sometimes sudden, sometimes from relentlessly stripping things away. Either you reach a remarkable result or you find the concept's ceiling and know to revisit range.

Moves for when you don't know what better looks like:

- **Zoom in** on one element and ask what world-class looks like if it were the only thing.
- **Remove** something. Was it actually needed?
- **Name what's wrong** even without a fix; articulating the problem often reveals the fix.
- **Study the best examples** in the category and let them expose gaps. Search for the exact surface ("sidebar with nested items and unread counts"), not a mood ("modern clean dashboard"). Prefer shipped products over Dribbble-style mockups nobody had to ship, and only cite what you actually opened.
- **Make more versions** and select, rather than theorizing.
- **Critique against the product's quality facets** (see the design-critique skill if available).

When iterating on something concrete, show the levels explicitly ("Level 1: default. Level 2: fixed X. Level 3: added Y. Level 4: removed Z because...") so the user sees the climb and can choose to stop or keep pushing.

## Less, but better

Dieter Rams' principle, applied to scope. Constantly resist adding features, scope and flourish. A deliberately small scope executed at a very high bar usually outperforms a broad one executed adequately. When proposing a direction, suggest what to cut: fewer typefaces, sizes, colors and actions, and one signature interaction done beautifully.

## Companion skills

Use these if available:

- **design-critique**: score directions against the product's quality facets when choosing, and critique each level during the climb.
- **intentional-prototyping**: build the breakable toy that answers whether a direction actually works before investing in depth.
- **interface-polish**: the states, edges and motion sweep for levels 2 to 6 of the climb.
