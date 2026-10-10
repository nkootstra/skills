---
name: interface-polish
description: Raise UI work from functional to genuinely crafted, by meeting platform baseline expectations first and then exceeding them through care in details, edge cases and purposeful motion. Use whenever the user is building or reviewing a UI, app, website, component or user flow and wants it to feel polished, premium, delightful, native, high-quality or "not generic", or is preparing something for launch, a demo, a portfolio or stakeholders. Use it for ordinary UI builds too whenever quality matters.
metadata:
  author: Niels Kootstra
  version: "1.1.0"
---

# Interface Polish

## Reference files

Load these when the matching step comes up; don't preload them all.

- Load [platform-baselines.md](references/platform-baselines.md) for section 1: check the target platform's floor (navigation, type, hit targets, sheets, gestures, focus, dark mode, safe areas) before designing, and use its "how to exceed it" list for ideas.
- Load [states-and-edges.md](references/states-and-edges.md) for the section 2 sweep; walk every component on screen through its state matrix, then run the edge sweep and check errors against the recovery formula.
- Load [motion.md](references/motion.md) for section 3, and whenever adding, reviewing or tuning an animation: purpose test, origin, frequency, duration and easing defaults, springs, reduced motion, performance.
- Load [visual-rules.md](references/visual-rules.md) whenever building or restyling a surface: the defaults to decide rather than inherit, and rules for surfaces, color, type, layout, actions and dark mode. Its quick defect scan is for section 4.
- Load [ship-checklist.md](references/ship-checklist.md) for section 5, before calling any UI work done.
- Load [react-components.md](references/react-components.md) when working in a React/TSX/Next.js codebase and building, reviewing or hardening a reusable component (API shape, states, keyboard and focus, motion tokens, per-frame performance).

## 1. Start from the platform default, then improve

People judge software against the apps they use every day. Work below that invisible bar gets dismissed as poorly made, usually without anyone saying why. This affects portfolios, stakeholder demos and MVP sales alike: a good idea with below-baseline execution reads as a bad product.

This is Jakob's law: users spend most of their time in other products, so they expect yours to work the same way. So don't start from a blank page. Start from how the platform's own conventions would solve it:

- **Native mobile**: system navigation, list patterns, sheets, standard gestures, the system type scale, platform transitions, haptics.
- **Web apps**: a clean, conventional component baseline (an accessible component library on a utility CSS setup), with sensible spacing, focus states and keyboard support.

Then innovate on top: keep the familiar structure people trust and make each part noticeably better. The best products feel like they belong on the platform yet outperform its built-in equivalents. Meeting the baseline is the floor, never the target.

## 2. Care shows up where others stop

Users feel care most in places nobody would have blamed you for skipping. The default failure is happy-path bias: designing and building only the state where data exists, the network is fast and the user does everything right. Before calling work done, sweep these:

- **States**: empty, loading, error, offline, partial data, very long and very short content, first run, missing permissions.
- **Edges**: tiny and huge viewports, slow networks, rapid repeated input, undo after destructive actions, reduced motion, keyboard and screen reader paths.
- **Recovery**: does every error say what happened and what to do next?
- **Friction users must ask about**: anything requiring them to contact someone or use a manual workaround could probably be self-serve.
- **A signature detail**: one unexpected, considered touch in an overlooked place (a thoughtful empty state, a personal message, a clever small detail) is evidence someone cared.

When useful, ask the user: where is this stopping at good enough? What's the known-broken thing nobody has fixed? As generation gets cheap, passable work is everywhere; time saved by tools is best spent on the parts that can't be generated.

## 3. Motion as proof of care

Animation isn't required, doesn't show in screenshots, and frameworks don't add it by default, which is exactly why doing it well signals care. Use it with intent:

- **Communicate**: show where things come from and go (correct transform origin, continuity between states), confirm actions, reveal affordances on hover and press.
- **Feel physical**: prefer springs for interactive elements; respond to input immediately; let controls stretch with rubber-banding at their bounds and snap back; let elements glide to a clicked position instead of jumping.
- **Restraint**: subtle, short, purposeful. Confirmations should be gentle; looping attention effects quiet and rare. Respect reduced-motion preferences.
- **Delight sparingly**: an occasional playful moment or hidden reward for curious users makes a product memorable, as long as it never slows down core tasks.

Example of a considered control: a slider whose handle stays hidden until hover, eases in along with the fill, glides to wherever you click, tucks away near the ends, and stretches elastically if you drag past the bounds.

## 4. Look at it, then check

UI that was written, compiled and declared done without anyone looking at it is the most common thing that comes back. Before reporting, render it in a real browser at two widths minimum, desktop (1440) and phone (390), using whatever is available: a browser MCP, Playwright, agent-browser, or headless Chrome. Look at the screenshots yourself, fix what you see, re-render, and show the user the images, not a file path. If nothing can render, say **not rendered** and never describe a page you didn't see.

## 5. Before shipping, check

The short version:

- Is it at or above the platform baseline everywhere, not just on the hero screen?
- Have all states and edges been designed rather than left to defaults?
- Does every animation have a purpose and the right origin?
- Is there at least one place where it goes further than it had to?
- Would anything be better removed?

For the full, testable checklist load [ship-checklist.md](references/ship-checklist.md).

## Companion skills

- **design-critique**: structured, specific critique to find what's weak or "feels off" before or after polishing.
- **design-exploration**: generate genuinely different directions and refine the chosen one before polishing it.
- **intentional-prototyping**: prototype an interaction with clear intent and live-tunable values to dial in timing, easing and springs.
