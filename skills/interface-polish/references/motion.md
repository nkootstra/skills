# Motion

Use this for section 3, and whenever you add, review or tune an animation. Motion that has no job is noise; motion with a job, done well, is one of the clearest signals that someone cared.

## Purpose test

Before animating anything, name its job. It must do at least one of:

1. **Communicate**: where something came from, where it went, what changed, that an action registered, that something is interactive.
2. **Feel physical**: make an interactive element respond like an object (follows the finger, has momentum, resists at bounds).
3. **Delight**: a rare, deliberate moment of personality in a place the user isn't rushing.

If it does none of these, remove it. "It looks cool" is not a job. "Everything else is animated" is not a job.

## Origin and continuity

- **Animate from the trigger.** A popover, dropdown or menu scales from the edge or corner nearest its trigger: set `transform-origin` accordingly (Radix exposes `--radix-popover-content-transform-origin`; similar variables exist in other primitives). A modal opened from a specific control scales from that control too; only a centered modal with no clear trigger (on load, from a shortcut) scales from center.
- **Keep continuity.** If an element moves between states, animate the same element rather than fading one out and another in. Thumbnails expand into detail views; list items move to their new position on reorder; tabs indicators slide between tabs.
- **Direction carries meaning.** Forward navigation slides in from the trailing edge, back from the leading edge (mirrored in RTL). Sheets enter from the edge they're attached to and leave the same way.
- **Don't animate from nothing.** Never `scale(0)`. Start entering elements at `scale(0.95)` with `opacity: 0`, or a few pixels offset, so the motion reads as arriving rather than inflating.

## Frequency rule

How often someone sees an animation decides how much motion it can carry.

| Frequency | Examples | Motion budget |
|---|---|---|
| 100+ times a day | Typing, keyboard shortcuts, command palette, list navigation, toggling a checkbox | None, or near-instant (under 100ms) feedback only |
| Tens of times a day | Opening menus, dropdowns, tooltips, switching tabs | Short and subtle: 120-200ms |
| A few times a day | Modals, sheets, page transitions, toasts | Standard: 200-300ms |
| Rare | Onboarding, first success, empty state, celebrations | Room for personality: 300-600ms, choreography allowed |

Tooltips and menus: animate the first open, then skip the delay and animation when moving between adjacent triggers.

## Duration and easing defaults

| Use | Duration | Easing |
|---|---|---|
| Hover color / background | 100-150ms | `ease` or `ease-out` |
| Button press scale | 100-160ms press, release up to ~200ms | `ease-out` |
| Tooltip | 120-180ms | `ease-out` |
| Dropdown / popover enter | 150-200ms | `cubic-bezier(0.23, 1, 0.32, 1)` (strong ease-out) |
| Dropdown / popover exit | 100-150ms | `ease-in` or same curve, shorter |
| Modal / dialog enter | 200-300ms | strong ease-out |
| Sheet / drawer | 300-500ms | `cubic-bezier(0.32, 0.72, 0, 1)` (iOS-like) |
| Toast enter | 250-400ms | strong ease-out or spring |
| Element moving on screen | 200-300ms | `ease-in-out` (`cubic-bezier(0.77, 0, 0.175, 1)`) |
| Page / route transition | 200-350ms | ease-out or ease-in-out |

Rules of thumb:
- UI motion stays under 300ms unless it covers large distance (sheets) or is rare.
- **Ease-out** for things entering or responding to the user: fast start feels responsive.
- **Ease-in-out** for things moving from one on-screen position to another.
- **Ease-in** almost never on its own for entrances: it feels sluggish at the start, exactly when the user is watching.
- **Linear** only for continuous, non-spatial motion (spinners, progress, marquees).
- Built-in CSS `ease-out` is weak; use a custom curve for more punch.

## Springs for interactive elements

Use springs when the element is driven by or responds to direct input: drags, swipes, toggles, things that can be interrupted.

- Springs carry velocity: a flicked sheet keeps the speed of the finger instead of restarting from zero.
- Defaults to start from: `stiffness: 500, damping: 40` for snappy UI (damping ratio ~0.9); or in duration terms `duration: 0.3-0.5, bounce: 0-0.15`.
- Bounce stays low (0-0.2) for productivity UI. Higher bounce only for playful moments.
- Toggles, switches, segmented controls and drag release are prime spring candidates.
- Non-interactive fades and color changes don't need springs.

## Interruptibility

- Every animation the user can trigger must be interruptible: reversing a hover, closing a menu mid-open, grabbing a sheet mid-dismiss.
- Prefer CSS transitions over keyframes for state toggles: transitions retarget from the current value; keyframes restart.
- With JS libraries, animate from the current value, never snap to a start value.
- Never block input while an animation runs. The user is always faster than your choreography.

## Enter vs exit asymmetry

- Exits are faster than entrances: roughly 70-80% of the enter duration.
- Entrances can carry more character (slight scale, offset); exits are plain (fade, small offset).
- Something the user dismissed should get out of the way immediately. Something new deserves a moment to be noticed.
- Exit in the direction it came from, or toward where it's going (a deleted item collapses; an archived item moves toward the archive).

## Stagger

- Stagger only small groups: up to ~5-8 items, 30-50ms apart.
- Total stagger time stays under ~300ms. Long lists: stagger the first few visible items, show the rest together.
- Never stagger content the user is waiting to read or act on repeatedly (search results on every keystroke).
- Stagger once on first appearance, not on every re-render.

## Rubber-banding and bounds

- When a drag hits a limit, keep moving with increasing resistance instead of stopping dead: offset = overshoot dampened (for example `limit + overshoot * 0.2`, or a logarithmic curve).
- On release, spring back to the bound.
- Applies to sheets dragged past fully open, sliders pulled past the end, carousels at their first or last item, pull-to-refresh before threshold.
- Rubber-banding communicates "this is the end" more gracefully than a hard stop.

## Reduced motion

`prefers-reduced-motion: reduce` means less movement, not less feedback.

- Replace movement (translate, scale, rotate, parallax, zoom) with an opacity fade or an instant state change.
- Keep feedback: a pressed button still visibly responds (color change instead of scale); a toast still appears (fade instead of slide); a success state still shows.
- Remove: parallax, autoplaying motion, looping attention effects, large page transitions, scroll-linked transforms.
- Keep: spinners and progress indicators (they carry information), but slow or simplify them.
- Autoplaying video and GIFs get a pause control or don't autoplay.
- Implement it for every animation, not as a global `* { animation: none }` that also kills feedback.

```css
@media (prefers-reduced-motion: reduce) {
  .menu { transition: opacity 150ms ease-out; transform: none; }
}
```

## Performance

- Animate only `transform` and `opacity` where possible. They are composited and skip layout and paint.
- Avoid animating `width`, `height`, `top`, `left`, `margin`, `padding`: each frame triggers layout. Use `transform: scale/translate` or FLIP techniques (or a layout animation library) instead.
- `filter: blur()` and `box-shadow` are expensive at large sizes; keep blur values small or animate opacity of a pre-blurred layer.
- `will-change: transform` only on elements about to animate, and remove it afterwards; it costs memory.
- In React, drive frame-by-frame values through motion values or CSS variables, not state that re-renders every frame.
- Test on a mid-range phone and with CPU throttling (4x) in DevTools; a 60fps animation on a MacBook can drop to 20 on a cheap Android device.
- Avoid animating on page load what the user needs to read: delayed content feels slow regardless of frame rate.

## Quick review questions

- What is this animation's job? Could the interface communicate it without motion?
- Does it originate from the thing that caused it?
- How many times a day will someone see it?
- Can it be interrupted at any point without jumping?
- Is the exit faster than the entrance?
- What does it become under reduced motion, and does the feedback survive?
- Does it touch anything other than transform and opacity?
