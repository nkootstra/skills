# React Prototypes

Use this when the prototype lives in a React, TSX or Next.js codebase. The rules are the same as any prototype: answer one question, make the answer visible, throw away what doesn't answer it. React adds a few ways to get that wrong and a few shortcuts.

## Isolate the question in one component

- **One file, one question.** Put the prototype in its own component (`PressFeedbackPrototype.tsx`) rendered on a scratch route or a story, not woven into the real screen. The real screen's data fetching, auth and layout are noise for a question about how a press feels.
- **Fake everything that isn't the question.** Hardcode the list, the user, the latency. If the question is "does the empty state read", the prototype renders the empty state on mount; nobody should have to delete twelve items to see it.
- **Render the state that matters.** If the question is about the pressed, open or error state, add a toggle that pins it, so it can be judged at rest and compared across variants.
- **Keep the real context around it** when the question depends on it: the same font, surface color and neighbouring controls. A press effect judged on a white void tells you little about the toolbar it will live in.
- **Client component.** In the Next.js App Router, the prototype file starts with `"use client"`; it uses state, effects and the tuner.

## One config object, wired to the tuner

Every value that might change goes in one object at the top of the prototype, and that object comes from `useTuner(schema)` (see [tuning-panel.md](tuning-panel.md); don't redefine the hook). No literal durations, distances or colors further down.

```tsx
"use client";
import { motion } from "motion/react";
import { useTuner } from "./useTuner";

export function SheetPrototype() {
  const t = useTuner({
    visualDuration: [0.3, 0.05, 1, 0.01],
    bounce: [0.1, 0, 0.6, 0.01],
    offsetY: [24, 0, 120, 1],
    dimOpacity: [0.4, 0, 1, 0.05],
    replay: false,
  });
  const spring = { type: "spring", visualDuration: t.visualDuration, bounce: t.bounce } as const;

  return (
    <motion.div
      key={String(t.replay)} // flipping the toggle remounts and replays the entrance
      initial={{ opacity: 0, y: t.offsetY }}
      animate={{ opacity: 1, y: 0 }}
      transition={spring}
    />
  );
}
```

- **Defaults are the current values.** If the production component uses a 0.16s spring, the slider starts there.
- **Pass values straight into the render.** Don't memoize them away or copy them into state on mount; each change must re-render.
- **Name keys for the decision**, not the CSS: `pressDepth`, not `boxShadowSpread`. The names become the vocabulary of the handoff.

## Per-frame values are motion values, not state

The tuner's values change at human speed, so state is fine for them. Values that change every frame are not:

- **Pointer, drag, scroll and progress** go into motion values (`useMotionValue`, `useScroll`, `useSpring`) and reach the DOM through `style`. Derive dependent values with `useTransform` from the same source so everything lands on the same frame.
- **Tuned parameters configure the motion value; they don't replace it.** `useSpring(x, { stiffness: t.stiffness, damping: t.damping })` re-reads the config on re-render while the per-frame value stays out of React.
- **Check with the profiler.** If dragging shows a re-render per frame, the prototype will feel janky and you'll misjudge the design for a performance bug.

```tsx
const x = useMotionValue(0);
const follow = useSpring(x, { stiffness: t.stiffness, damping: t.damping });
const opacity = useTransform(follow, [-t.range, 0, t.range], [0.3, 1, 0.3]);

<motion.div
  onPointerMove={(e) => x.set(e.nativeEvent.offsetX - t.range)}
  style={{ x: follow, opacity }}
/>
```

## Switch variants quickly

- **Variants are a select, not a branch in your head.** When comparing structurally different options, render them behind one `variant` key: `variant: { options: ["inset", "scale", "shadow"] }` and a `switch` in the render. Same data, same container, so only the variant differs.
- **Keep each variant small and parallel.** Three 20-line functions with the same props compare cleanly; one 200-line component with flags does not.
- **Use the tuner's variations grid** to explore combinations of continuous values, then load the winner and fine-tune.
- **Record the outcome in the file.** When a variant loses, leave a one-line comment with why, then delete its code. The comment survives into the handoff; the code doesn't.

## Hardening a prototype into a production component

A prototype that answered its question is evidence, not a component. Promote the answer, not the file:

1. **Freeze the values.** Read the final numbers off the panel. Map each to the nearest existing token; if one is deliberately off-token, give it one named export with a comment saying why.
2. **Remove the tooling.** No `useTuner`, no replay key, no pinned-state toggles, no fake data. The tuner stays out of production builds.
3. **Rebuild on the real API.** Native props, forwarded ref, controlled and uncontrolled modes, composed event handlers, size from prop then provider.
4. **Add every state the prototype skipped.** Disabled, loading, error, focus-visible, empty, long content, touch. Prototypes usually only built rest and the one interaction under test.
5. **Add accessibility.** Roles, keyboard, focus restoration, announcements, reduced motion. A prototype that only worked with a mouse has not been validated for keyboard users.
6. **Check it in real contexts:** inside a dialog, in a compact region, in dark mode, at narrow widths.

The full standard for that last step is the interface-polish skill's react-components.md; use its checklist before calling the component done.
