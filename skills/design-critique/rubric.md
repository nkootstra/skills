# Critique Rubric

Concrete checks per dimension, a severity scale, and the phrasing rules that turn a reaction into a finding. Use it on the second and third passes: the first pass is for gut reaction, this is for finding what the gut skipped.

## Rules for every finding

**Count things, quote text, name colors and values.** "Too many buttons" is an opinion; "seven buttons above the fold, four of them filled" is a finding. Quote the exact label ("Submit", not "the button text"). Name the hex, the pixel value, the weight, the duration. If you cannot measure it, describe it precisely enough that someone else could find it in ten seconds.

**Formula:**

```
**[Issue]**: observation. Impact. Direction.
```

- **Issue**: 2–5 words naming the problem, not the fix. "Competing primary actions", not "Make one button secondary".
- **Observation**: what is there, with location and numbers.
- **Impact**: what it does to the user or to a facet.
- **Direction**: where to go, not a full spec. Leave room for the designer.

Example: **Competing primary actions**: the header has "New project" and "Invite team" both as filled #4F46E5 buttons at 40px height, 16px apart. The eye lands on neither, and first-run users don't know which comes first. Demote "Invite team" to a ghost button, or move it into the empty state where it's contextual.

**Where** is always specific: screen name plus region ("Settings > Billing, plan card, bottom right"), a component name, a file and line, or a timestamp in a recording.

## Severity

| Level | Definition | Examples |
| --- | --- | --- |
| **Blocker** | Prevents a task, loses data, misleads about consequences, or fails a legal accessibility floor. Do not ship. | Destructive action with no confirm or undo. Body text at 2.1:1 contrast. Form submits but shows no result. Keyboard trap in a modal. Any dark pattern (see below). |
| **Major** | Task completes but with real friction, error, or a clear hit to the top-ranked facet. Fix before ship unless there's a reason. | Primary action not identifiable in under 2 seconds. No loading state on a 3s request. Error message "Something went wrong" with no next step. Layout breaks at 375px. |
| **Minor** | Noticeable to an attentive user, inconsistent with the rest of the product, or below platform baseline in a small way. Fix in the next pass. | Three different radii (4, 6, 8px) on sibling cards. Hover state missing on table rows. Title case and sentence case mixed in one menu. |
| **Polish** | Only noticed side by side or by a designer, but contributes to "crafted versus cheap". Batch these. | Icon 1px off optical center. 200ms ease-in on a dropdown open (should be ease-out). Numbers in a table not using tabular figures. |

Calibration rules:

- Severity follows user impact, not effort to fix. A one-line CSS change can fix a blocker.
- A minor issue repeated on every screen can be major: say so and count the instances.
- A polish issue on the hero moment of a facet like "premium" or "crafted" can be minor or major. State the facet.
- If unsure between two levels, pick the lower one and say what would raise it.

## 1. Hierarchy and focus

Look for:

- **One focal point per view.** Squint or blur the screen: one element should win. If two or more tie, that's a finding. The isolation effect (Von Restorff) explains why: the one thing that differs gets noticed, so when everything is emphasized, nothing is.
- **Primary action identifiable in under 2 seconds** without reading labels.
- **Count filled/high-emphasis buttons per view.** More than one primary per decision area is suspect.
- **Reading order** matches task order: does the eye path (usually top-left to bottom-right, or F/Z pattern) hit things in the sequence the user needs them?
- **Size steps are meaningful**: heading levels differ by at least ~1.2x, or differ in weight/color clearly. Two sizes 1–2px apart read as a mistake.
- **Grouping** follows Gestalt: proximity and similarity first, common region (cards, borders) only when spacing can't do it. Related items closer together than unrelated ones. Boxes around everything usually mean the spacing failed.
- **Density matches audience**: expert tools can be dense; onboarding cannot.

Common failures: everything bold; every card the same weight so nothing is a summary; decorative elements (illustrations, gradients) outweigh content; secondary nav as loud as primary; badges and counts on everything.

Phrase as: "The eye lands on X first, but the task starts at Y."

## 2. Typography

Look for:

- **Body text size**: 16px minimum on web for long reading, 14–15px acceptable for dense UI, 13px floor for secondary labels, 11–12px only for tertiary metadata. iOS body 17pt, Android 14–16sp.
- **Line length**: 45–75 characters for prose. Over 90 is tiring.
- **Line height**: 1.4–1.6 for body, 1.1–1.3 for headings. Tight body (under 1.3) or loose headings (over 1.4) both read as unconsidered.
- **Number of sizes**: count distinct font sizes on one screen. More than 5–6 usually means no scale.
- **Weights**: count them. More than 3 in one view is noise. Faux bold or faux italic (font not loaded) is a finding.
- **Tabular figures** in tables, prices, timers, anything that updates or aligns vertically.
- **Letter spacing**: all-caps labels need positive tracking (around 0.05em); large display text often needs slight negative tracking.
- **Wrapping**: orphans on headings, awkward breaks in buttons, truncation without tooltip or full value available.
- **Text on images** without scrim or sufficient contrast.

Common failures: gray body text at 14px on white; headings only differ by weight; two typefaces that are too similar to contrast and too different to match; centered paragraphs longer than 3 lines.

Phrase as: "Body copy is 13px #6B7280 on #FFFFFF at 1.3 line height, so long descriptions are tiring to read."

## 3. Color

Look for:

- **Contrast**: text 4.5:1 minimum (WCAG AA), large text (24px, or 18.66px bold) 3:1, UI components and focus rings 3:1 against adjacent colors. Measure, don't eyeball.
- **Count accent colors** per screen. One brand accent plus semantic colors (success, warning, danger, info) is the norm. A second accent used for no reason competes.
- **Semantic consistency**: red means destructive or error everywhere, never decoration. Green isn't used for both "success" and "primary".
- **Color is not the only signal**: status, errors, and chart series also differ by icon, label, or pattern.
- **Neutrals** share a temperature: mixing cool grays (#6B7280) and warm grays (#78716C) reads as accidental.
- **Dark mode**: not inverted light mode. Surfaces get lighter as they elevate; pure #000 backgrounds with pure #FFF text cause halation; saturated accents need desaturating.
- **Disabled vs. secondary**: are they distinguishable?

Common failures: brand color on every link, button, icon and heading so nothing stands out; low-contrast placeholder used as label; gradients that band or muddy in the middle; hover colors that barely differ (under 5% lightness change).

Phrase as: "Placeholder text #9CA3AF on #F9FAFB measures 2.4:1 and is the only label on the field."

## 4. Spacing and alignment

Look for:

- **A spacing scale**: values should come from a set (4/8/12/16/24/32/48/64 or similar). Measure five gaps: if you find 13, 17 and 22px, there's no scale.
- **Internal ≤ external**: padding inside a group is smaller than space between groups.
- **Consistent padding** on sibling components (cards, list rows, inputs).
- **Alignment edges**: count distinct left edges in a column. Each extra edge needs a reason.
- **Optical alignment**: icons next to text centered on cap height or x-height, not bounding box; play triangles shifted right; round shapes slightly overshooting.
- **Radii**: count distinct values. Nested elements follow concentric radius (inner = outer minus padding).
- **Hit targets**: 44x44pt iOS, 48x48dp Android, 24x24px WCAG 2.2 minimum on web with spacing; 44px+ preferred for touch.
- **Responsive**: check at 375px, 768px, 1280px and 1920px. Look for horizontal scroll, crushed columns, or line lengths that explode on wide screens.

Common failures: equal space everywhere so nothing groups; cards with 24px padding next to cards with 16px; text baseline misaligned with adjacent icon; a lone centered element in a left-aligned layout.

Phrase as: "Gaps between form sections are 16px and between label and field are 12px, so sections don't separate."

## 5. States

Check every interactive element and every data-driven view for:

| State | Check |
| --- | --- |
| Default | Affordance clear without hover. |
| Hover | Visible change on pointer devices; not required to understand the control. |
| Focus | Visible ring at 3:1 contrast, not removed, not clipped by overflow. |
| Active / pressed | Feedback starts on pointer down (100-160ms in, release may be slower), e.g. scale 0.97 or darker fill. |
| Disabled | Distinguishable, and the reason is discoverable. |
| Loading | Appears if work takes over ~300ms; skeletons match final layout; no layout shift on resolve. |
| Empty | Explains what goes here and offers the first action. Not a blank table header. |
| Error | Says what happened, why if known, and what to do. Inline near the cause. Preserves input. |
| Success | Confirms the result and where it went. |
| Partial / overflow | Long names, 0 items, 1 item, 1,000 items, missing avatar, very long numbers. |
| Offline / slow | Behavior on failed or slow network. |

Common failures: only the happy path designed; spinner replaces the whole page for a small update; error clears the form; empty state is an illustration with no action; optimistic update with no rollback on failure.

Phrase as: "Submitting with an invalid email clears all five fields and shows a red banner at the top, out of view on mobile."

## 6. Motion and feel

Look for:

- **Purpose**: each animation explains a change (where something came from or went), gives feedback, or directs attention. Decoration-only motion on frequent actions is a finding.
- **Duration**: micro-interactions 100–200ms, small transitions 200–300ms, larger layout changes 300–500ms. Anything over 500ms on a frequent action feels slow.
- **Easing**: ease-out for entrances and responses to input; ease-in-out for on-screen movement; avoid ease-in, even on exits a strong ease-out reads faster. Linear only for progress and continuous loops.
- **Origin**: popovers, and modals opened from a control, scale from their trigger, not from center. Sheets come from the edge they dismiss to.
- **Interruptibility**: can a user act mid-animation, reverse a gesture, close before open completes?
- **Response time**: input feedback under 100ms; anything over 1s needs a progress indicator.
- **Frame rate**: drops, jank on scroll, layout shift during load (CLS).
- **Reduced motion**: large movement, parallax and autoplay are replaced or removed under `prefers-reduced-motion`.

Common failures: everything fades at 300ms ease-in-out regardless of size; modal animates from screen center while triggered from a corner; hover animations on touch; scroll-jacking.

Phrase as: "The dropdown opens with a 400ms ease-in, so the first 150ms show almost nothing and the menu feels late."

## 7. Copy and microcopy

Look for:

- **Labels say what happens**: verbs on buttons ("Save changes", "Delete 3 files"), not "OK", "Submit", "Yes".
- **Consistency**: one term per concept (don't mix "workspace", "project", "team" for the same thing). Count the variants.
- **Case**: one convention (sentence case is the modern default) across buttons, menus and headings.
- **Error messages**: what happened, why, what to do. No blame, no codes alone, no "Oops".
- **Confirmation dialogs** name the object and consequence: "Delete 'Q3 report'? This can't be undone." with buttons "Delete" and "Cancel".
- **Front-loading**: the important word comes first in labels and list items.
- **Length**: tooltips under ~80 characters; button labels 1–3 words.
- **Voice** matches facets: a "calm" product doesn't use exclamation marks; a "playful" one isn't corporate.

Common failures: placeholder text as the only instruction; jargon from the codebase ("sync job failed: 409"); "Click here" links; marketing tone inside a utility flow.

Phrase as: "The confirm dialog reads 'Are you sure?' with buttons 'Yes' and 'No', so the user can't tell what 'Yes' does without rereading the trigger."

## 8. Accessibility basics

Not a full audit; the floor every critique should check:

- Contrast per section 3.
- **Keyboard**: tab through the screen. Order is logical, every action is reachable, focus is visible, no traps, Escape closes overlays, focus returns to the trigger.
- **Labels**: every input has a visible label; icon-only buttons have an accessible name.
- **Zoom**: 200% browser zoom without loss of content or horizontal scroll at 1280px width.
- **Targets** per section 4.
- **Semantics**: headings in order, buttons are buttons, links are links.
- **Motion** per section 6.
- **Don't rely on color, hover, or position alone** to convey meaning.

Anything failing here on a primary flow is at least major; contrast or keyboard failure on body text or a primary action is a blocker.

## Nielsen's heuristics as a final sweep

After the dimensions above, run the 10 heuristics as a fast cross-check. Each line is the question to ask; most findings will already be filed, and this catches what fell between dimensions.

1. **Visibility of system status**: does every action get feedback within ~100ms, and every wait over ~1s a progress signal?
2. **Match with the real world**: does it use the user's words, not the database's?
3. **User control and freedom**: is there undo, cancel, back, and a way out of every flow?
4. **Consistency and standards**: does it behave like the platform and like itself? (Jakob's law: users spend most of their time in other products.)
5. **Error prevention**: are destructive or irreversible actions guarded, and invalid input prevented rather than reported?
6. **Recognition over recall**: are options visible, or does the user have to remember them from a previous screen?
7. **Flexibility and efficiency**: do frequent users get shortcuts, bulk actions, keyboard paths?
8. **Aesthetic and minimalist design**: does every element earn its place against the focal point?
9. **Help users recover from errors**: what happened, why, what to do next, in plain language?
10. **Help and documentation**: when help is needed, is it in context rather than in a separate manual?

## Dark patterns: always a blocker

Name them explicitly when found; "slightly pushy" undersells them. Common ones: **confirmshaming** ("No thanks, I like paying full price"), **roach motel** (easy to sign up, hard to cancel), **preselected opt-ins**, **disguised ads**, **fake urgency or scarcity** (timers that reset), **hidden costs** revealed at the last step, **trick questions** (double negatives on consent), **nagging** (repeated prompts after a decline). File each as a blocker regardless of how small it looks, and state who it benefits at the user's expense.

## Exempt: don't file these

Noise reduces trust in the findings that matter. Skip or fold into a single line:

- **Personal taste without a facet behind it.** "I'd prefer a serif" is not a finding. "A serif would support 'editorial', which currently scores 2" is.
- **Re-litigating confirmed decisions**: brand color, typeface, or concept the user said is fixed. Critique the execution instead.
- **Platform conventions followed correctly** that you happen to dislike.
- **Hypothetical edge cases** with no realistic user (unless they cause data loss).
- **Duplicate instances**: file once, count the occurrences, list locations.
- **Fixes disguised as findings**: "Use Inter" without an observed problem.
- **Out-of-scope areas** the user didn't ask about, unless blocker severity.
- **Content placeholders** (lorem ipsum, stock photos) in an explicitly early draft, unless they hide a layout problem real content would cause.
- **Sub-pixel differences** nobody will see outside a zoomed screenshot, unless the facet is "precise" or "crafted" and it's the hero element.
