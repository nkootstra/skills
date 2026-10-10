---
name: intentional-prototyping
description: Workflow for building interaction and UI prototypes with clear intent, live-tunable parameters, and learning by recreation. Use whenever the user wants to prototype an interaction, animation, transition, gesture or component; asks how a UI effect was made or wants to recreate one; is dialing in timing, easing, springs, spacing, shadows or similar values; or wants several variations of an effect rendered side by side to pick from, or is about to build a high-fidelity prototype of everything at once.
argument-hint: "[interaction to prototype]"
metadata:
  author: Niels Kootstra
  version: "1.1.0"
---

# Intentional Prototyping

## Reference files

Load these only when the step calls for them:

- When building the control panel, load [tuning-panel.md](references/tuning-panel.md) and copy the module verbatim; adapt only the schema and the `onChange` binding. If the project already uses DialKit, Leva or Tweakpane, use that instead (the file says how to decide).
- When choosing defaults and slider ranges for durations, easing, springs, stagger, scale, translate, shadows, blur, radius or opacity, load [parameter-ranges.md](references/parameter-ranges.md). Values already in the code take precedence.
- When the user wants to recreate or understand an effect, load [recreation.md](references/recreation.md) for the observation checklist, technique decision table, frame-by-frame study tips and the comparison log template.
- When the prototype lives in a React/TSX/Next.js codebase, load [react-prototypes.md](references/react-prototypes.md): isolating the question in one component, tuning values through `useTuner`, motion values for per-frame updates, and turning a validated prototype into a production component.

## 1. Separate concerns: name the question first

Trying to resolve everything in one pass (layout, content, visuals, motion, data) leads to rework and rabbit holes. Slow is smooth, smooth is fast.

Before building, state the single question this prototype must answer, e.g. "Does this card interaction feel as good as imagined?" or "Is this navigation model understandable?" Make it falsifiable: decide up front what result would mean "no". A prototype that can only confirm the idea is a demo, not a test. Then build the minimum that answers it, a breakable toy (a spike, in XP terms: time-boxed and thrown away once it has answered):

- Testing an interaction? Use blank shapes. No real content, no final art, no copy.
- Testing layout or hierarchy? Static is fine; skip motion.
- Testing whether people grasp a concept? Rough is fine.
- Testing an experience whose hard part is expensive (AI output, search quality, a recommendation)? Wizard of Oz it: fake the hard part with canned or hand-picked results and test whether the experience is worth building.

Only invest in detail once the direction has earned it. Premature fidelity is the failure to watch for: polished visuals on an unanswered question make the prototype feel finished and make people react to the polish instead of the idea. If the answer is "no", go back and explore other directions rather than polishing.

Fidelity should also match the audience and decision. A sketch may be enough for one conversation; another needs something near-shippable before people can feel what you feel. The point isn't to always start rough, but to always know what you're resolving.

When building a prototype, tell the user which question it answers and what was intentionally left out.

## 2. Live tuning: expose the parameters

Editing a value, saving, reloading and squinting is slow and disconnects you from the feel. Instead, expose the important parameters as live controls and adjust them while watching the result.

For any prototype with motion or visual nuance, include a small floating control panel by default, with sliders and toggles for the values that matter:

- Motion: duration, delay, stagger, easing curve, spring stiffness/damping or bounce/visual duration
- Geometry: offsets, rotation, scale, spacing, radius
- Surface: shadow blur/opacity/offset, blur, opacity, color

Guidelines:

- Update in real time while dragging; no apply button.
- Show the current numeric value beside each control.
- Include reset-to-defaults and a way to copy the current values (as JSON or a code snippet) so dialed-in settings can go straight into production code.
- Keep the panel visually quiet, collapsible, and out of the way of the thing being tuned.
- For explorations, offer a "generate variations" mode that renders a grid of instances with randomized parameters within sensible ranges, with controls for count and columns. This surfaces combinations nobody would reach by tweaking one value at a time.

## 3. Recreate to learn

When the user admires an effect and doesn't know how it works, the fastest way to learn is to rebuild it right away, while curiosity is fresh:

1. Describe the effect precisely in observable terms: what moves, from where, how it deforms, how it feels.
2. Build the simplest version that captures the gist (e.g. scale and translate with a spring).
3. Add the hard part one step at a time, naming the likely technique (CSS transforms, clip-path, SVG filters, canvas, WebGL mesh deformation, shaders) and why.
4. Compare with the reference after each step and say concretely what still differs ("edges are straight; the original curves inward").
5. Stop when the learning goal is met. It doesn't need to be polished.

Encourage the user to share what they rebuilt; recreations compound into a personal toolkit.

## Companion skills

- **design-exploration**: hand off when the question is "which direction?" rather than "does this feel right?", i.e. several divergent concepts are needed before one is worth prototyping.
- **design-critique**: hand off when a prototype has answered its question and the result needs a structured review of hierarchy, consistency and craft.
- **interface-polish**: hand off when the direction is settled and the work moves from tuning a single interaction to finishing details across the whole interface.
