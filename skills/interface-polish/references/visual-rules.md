# Visual Rules

Build rules for surfaces, color, type, layout, actions and dark mode. They are defaults, not law: the project's existing design system wins, and so does a reference the user chose on purpose. When you break a rule for either reason, say so in one line.

## Defaults to decide, not inherit

These are what a model reaches for when nobody chose. Choosing one on purpose is fine; landing on it by default is the failure. For every row that applies to the surface, write one line saying what you chose and why.

| Default | Decide instead |
| --- | --- |
| Framework blue or indigo primary | Take the primary from the brand, the content or the mood. If it ends up blue, say why. |
| Inter or the system stack everywhere | One face for UI and body, optionally one for display. One face everywhere is fine if it was chosen. |
| Three equal feature columns | Match the count to the content. Two strong items beat three padded ones. |
| Uniform spacing | Related things sit closer than unrelated things. |
| Large radius on everything | Radius signals role. Buttons, inputs, cards and media get two or three values assigned by role. |
| Gradient text, purple-to-pink backgrounds | Usually a placeholder for an idea. Use only when the brand already owns it. |
| Cards inside cards | One surface change per level of hierarchy. |
| Everything centered | Center short, symmetric content only. Long copy, lists and forms are left-aligned. |
| Emoji as icons | One icon set, used everywhere. |
| Glass, blur, glow | Only when the surface behind it earns it. On a flat page it reads as decoration. |
| Placeholder copy | Write the real words. "Feature one" and lorem ipsum hide layout problems. |

## Surfaces

Use the lightest separation that works, in this order:

1. **Whitespace**, when the content has its own contrast (a big number over a small label).
2. **A divider or hairline**, for siblings that need a boundary: list rows, stat rows, settings groups.
3. **A well**, a background slightly darker than the page, for secondary or nested content.
4. **A card**, only for things that are independently interactive or a different kind of content from their neighbors.

- Make borders and dividers from the text color at 5 to 10% opacity, not a solid light gray. They then sit correctly on tinted backgrounds and in dark mode.
- A border and a shadow doing the same job is one too many. Pick one.
- Elevated surfaces are never darker than what they float over. Darker fills are for inset wells, which have no shadow.
- Shadows are small and tight at rest; large only for things actually floating (menus, popovers, dialogs). A shadow that reads as blur is wrong.
- Shadows and borders on a colored background carry that hue. Gray on color looks like dirt.
- A surface that differs from the page by less than about 1.2:1 is invisible. Make it a real surface or remove it.
- A header that shares the page background with only a hairline under it doesn't read as a header. Give it a surface change, a stronger rule, or a shadow on scroll.
- Long tables and lists sit on the page, not inside a card.

## Color

- One dominant color, for the primary action and little else. If the brand color is everywhere, there is no primary action.
- Pick the neutral scale on purpose: cool grays read clinical, warm grays editorial. Tint neutrals slightly toward the brand hue so text, borders and backgrounds feel like one system.
- Three text levels at most: primary, secondary, hint/disabled.
- Semantic colors (success, warning, danger) stay muted at rest so they stand out when they matter.
- Secondary text is still readable. If you squint at a timestamp, it is too light.

## Typography

- One type scale. Application UI uses a smaller, tighter scale than marketing; don't mix them on one surface.
- Let size carry hierarchy; heavy bold on every heading reads as shouting.
- Large headings get slightly tighter tracking, body none, small uppercase labels looser.
- `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs. A single word alone on the last line of a heading or card is a defect.
- Constrain measure on the text element itself, in characters: 60 to 75 for body, roughly 20 to 35 for large headings. Don't cap a whole heading group, so each line wraps on its own and they share an edge.
- Tabular figures for any number that changes while the page is open.
- The smallest size in the scale is for timestamps and footnotes, never for anything needed to complete a task.

## Layout

- Space siblings with the parent's `gap`, not margins on children. Margins break when the layout wraps or reorders.
- Sections are two elements: an outer one for background and vertical padding, an inner one for max width and horizontal padding. Every section uses the same inner width so edges line up while scrolling.
- Never more centered sections than left-aligned ones. Don't stack a centered section directly under a left-aligned one without a background change or divider between them.
- A flex child that must shrink below its content (truncated label, fluid content beside a sidebar) needs `min-width: 0`. One that must never shrink (icon, avatar, logo) gets `flex-shrink: 0`.
- Content never touches the viewport edge on a phone. Multi-column app layouts collapse through a menu or disclosure, never by squeezing columns.
- Components that depend on their own width (dashboard widgets, cards, pricing tiers) use container queries, not viewport media queries.

## Actions and navigation

- One primary button per view (a dialog counts as its own view). No secondary is higher contrast than the primary.
- Inline actions inside a form (resend code, add item) are smaller and secondary, never the height of the submit button.
- A badge is metadata. If it does nothing on click, it doesn't look clickable.
- Hover effects belong only to things that do something. A non-clickable card doesn't lift.
- Nav items never change width between default, hover and active; it reflows the row. Change weight only with an invisible bold copy reserving the width (see react-components.md). Mark active with color and background, not a solid primary block.
- If a list has a length the user cares about, its nav item and header show the count.
- Sibling pages match: same header treatment, icon set and action placement. Name the page you are matching.
- Every page has its own title.
- On marketing pages, the same kind of thing gets the same treatment everywhere: one secondary-action style, one card style, one column gap. In pricing, tier buttons align to one baseline and the recommended tier is marked by button style and a label, not a different card color.

## Dark mode

- Keep the same contrast relationships as light mode; it is not an inversion.
- Elevation comes from a slightly lighter surface and a faint light ring, not shadows. Cards are one step lighter than the page, not several.
- Body text is off-white, not pure white.
- Borders are white at low opacity, the mirror of the light rule.
- Every raster image (screenshots, mockups, photos with white backgrounds) gets a dark version or an explicit decision. A CSS invert or dim is not a final treatment.
- Set `color-scheme` so native controls and scrollbars follow.

## Quick defect scan

For looking at a rendered screen. Most frequent first.

- Orphaned word on the last line of a heading or card
- Content or nav touching the edge on a phone
- Two borders, or a border plus a shadow, doing one job
- A card or button under ~1.2:1 against the page
- Inner radius equal to or larger than its container's
- Gray shadow on a colored ground
- Nav item with no count for a list the user cares about
- Icon-only button with no label or tooltip
- Empty state with no explanation and no next step
- Sibling pages with different header, icon set or action placement
- The same page title on every page
- Internal jargon, or copy that narrates the mechanism instead of the outcome
