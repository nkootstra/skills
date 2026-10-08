# Parameter Ranges

Starting defaults and slider ranges for the tuning panel. Defaults are where good UI usually lands; ranges are wide enough to reach "clearly too much" on both sides so the user can feel the edges. Existing values in the code always win over these defaults.

Schema tuples below are `[default, min, max, step]`, ready to paste into [tuning-panel.md](tuning-panel.md).

## Durations

The more often something happens, the shorter it should be. Something seen hundreds of times a day should be near-instant or not animated at all. Exits run at about 70 to 80 percent of the enter duration: the user has already decided and is waiting on you.

| Interaction | Default | Slider | Rationale |
| --- | --- | --- | --- |
| Press feedback (scale, darken) | 120ms | `[120, 0, 300, 10]` | Must feel attached to the finger; a press above ~160ms reads as lag. Release may run to ~200ms |
| Hover (color, background, lift) | 150ms | `[150, 0, 400, 10]` | Fast enough to track a moving pointer; sweeping a list should not leave trails |
| Tooltip, dropdown, popover enter | 180ms | `[180, 80, 400, 10]` | Small surfaces travel little distance; longer feels sluggish |
| Small UI exit | 140ms | `[140, 0, 300, 10]` | Get out of the way |
| Toast enter | 300ms | `[300, 150, 600, 10]` | Arrives unprompted, so a little more time helps it register |
| Modal / dialog | 240ms | `[240, 150, 500, 10]` | Larger surface, still blocking the user's next action |
| Drawer / sheet | 400ms | `[400, 200, 700, 10]` | Travels the full viewport height; pairs with a strong ease-out |
| Page or route transition | 350ms | `[350, 200, 800, 10]` | Covers the whole screen; keep under ~500ms for frequent navigation |
| Tooltip hover delay (first) | 400ms | `[400, 0, 1000, 50]` | Prevents tooltips flashing while the pointer passes; skip the delay when moving between adjacent tooltips |
| Stagger per item | 40ms | `[40, 0, 150, 5]` | See Stagger |

## Easing

Ease-out for anything entering or responding to the user: it moves fast at the start, which reads as responsive. Ease-in-out for things already on screen moving from A to B. Avoid ease-in for UI: the slow start is exactly the moment the user is watching, so it feels delayed. Linear only for things tied to time or progress (progress bars, spinners, marquees, scrubbing).

The built-in `ease-out` keyword is weak. Prefer a custom curve:

| Curve | `cubic-bezier` | Use for |
| --- | --- | --- |
| Ease-out quad | `0.25, 0.46, 0.45, 0.94` | Subtle hover and color changes |
| Ease-out cubic | `0.215, 0.61, 0.355, 1` | General enter, a safe default |
| Ease-out quart | `0.165, 0.84, 0.44, 1` | Popovers, dropdowns |
| Ease-out quint | `0.23, 1, 0.32, 1` | Snappy enters, press release |
| Ease-out expo | `0.19, 1, 0.22, 1` | Dramatic enters, large surfaces |
| Drawer (iOS-like) | `0.32, 0.72, 0, 1` | Sheets and drawers |
| Ease-in-out cubic | `0.645, 0.045, 0.355, 1` | On-screen movement, reordering |
| Ease-in-out quart | `0.77, 0, 0.175, 1` | Larger on-screen movement, morphs |
| Ease-in-out quint | `0.86, 0, 0.07, 1` | Emphatic movement between states |

Expose easing as a select of named curves rather than four raw sliders; the user is choosing a character, not a coordinate. If raw control is needed, slide the four control points over `[0, 1]` for x and `[-0.5, 1.5]` for y.

## Springs

Use springs for anything gesture-driven or interruptible: a spring retargets from its current velocity, a tween restarts. Two equivalent models:

**Perceptual (Motion `visualDuration` + `bounce`, SwiftUI `duration` + `bounce`).** Easier to tune because the parameters are independent: duration is how long it appears to take, bounce is how much it overshoots.

| Feel | `visualDuration` | `bounce` |
| --- | --- | --- |
| Snappy | 0.2 | 0 |
| Smooth | 0.4 | 0 |
| Bouncy | 0.5 | 0.35 |

Sliders: `visualDuration: [0.3, 0.1, 1, 0.01]`, `bounce: [0.15, 0, 0.6, 0.01]`. Keep UI bounce under ~0.25; above that, reserve it for playful or gesture-release moments where overshoot means something (a thrown card settling).

**Physical (`stiffness`, `damping`, `mass`).** Stiffness is how hard it pulls toward the target, damping is friction, mass is inertia. Whether it overshoots depends on the damping ratio `damping / (2 * sqrt(stiffness * mass))`: 1 is critically damped (no overshoot), below 1 bounces, above 1 is sluggish. Motion's `bounce` is roughly `1 - ratio`.

| Feel | `stiffness` | `damping` | `mass` | Ratio |
| --- | --- | --- | --- | --- |
| Snappy | 500 | 40 | 1 | ~0.9 |
| Smooth | 200 | 28 | 1 | ~1.0 |
| Bouncy | 300 | 15 | 1 | ~0.43 |

Sliders: `stiffness: [300, 50, 1000, 10]`, `damping: [30, 5, 80, 1]`, `mass: [1, 0.1, 5, 0.1]`. Leave mass at 1 unless simulating weight; it couples with the other two and makes tuning confusing. Motion's default (100, 10, 1) is quite bouncy for UI.

## Stagger

| Parameter | Default | Slider | Rationale |
| --- | --- | --- | --- |
| Delay per item | 40ms | `[40, 0, 150, 5]` | Below ~20ms reads as simultaneous; above ~80ms the list feels like it is loading |
| Max staggered items | 8 | `[8, 1, 20, 1]` | Cap so the last item is not waiting; items past the cap enter with the last one |
| Total stagger budget | 300ms | `[300, 0, 800, 10]` | Alternative to a cap: divide the budget across visible items |

## Scale

| Parameter | Default | Slider | Rationale |
| --- | --- | --- | --- |
| Press, small button | 0.97 | `[0.97, 0.85, 1, 0.005]` | Visible but not toy-like |
| Press, large card | 0.985 | `[0.985, 0.9, 1, 0.005]` | Large surfaces move more pixels for the same ratio |
| Enter from (popover, modal) | 0.96 | `[0.96, 0.5, 1, 0.01]` | Never from 0: nothing in the world appears from a point. Set `transform-origin` to the trigger |
| Hover grow | 1.02 | `[1.02, 1, 1.1, 0.005]` | Use sparingly; lift or shadow often reads better |

## Translate

| Parameter | Default | Slider | Rationale |
| --- | --- | --- | --- |
| Small UI enter offset (tooltip, menu) | 6px | `[6, 0, 24, 1]` | Hints direction without traveling |
| Card or toast enter offset | 12px | `[12, 0, 48, 1]` | Enough to read as arriving |
| Section reveal offset | 24px | `[24, 0, 80, 1]` | Larger elements need more travel to register |
| Hover lift | -2px | `[-2, -8, 0, 0.5]` | Pair with a slightly larger shadow |
| Drawer, sheet | 100% | n/a | Translate its own size so it enters from fully off-screen |

## Shadows

Single shadows look flat or muddy. Layer several shadows that double in offset and blur while keeping opacity low and constant; together they approximate how real light falls off.

```css
--shadow-sm:
  0 0 0 1px rgb(0 0 0 / 0.06),
  0 1px 2px rgb(0 0 0 / 0.05),
  0 2px 4px rgb(0 0 0 / 0.05);
--shadow-md:
  0 0 0 1px rgb(0 0 0 / 0.06),
  0 1px 2px rgb(0 0 0 / 0.04),
  0 2px 4px rgb(0 0 0 / 0.04),
  0 4px 8px rgb(0 0 0 / 0.04),
  0 8px 16px rgb(0 0 0 / 0.04);
```

Generator for the tuning panel, with the four sliders that matter:

```js
// layers: [4, 1, 6, 1], y: [1, 0, 8, 0.5], blur: [2, 0, 16, 0.5], alpha: [0.04, 0, 0.2, 0.005]
const layeredShadow = ({ layers, y, blur, alpha }) =>
  Array.from({ length: layers }, (_, i) => `0 ${y * 2 ** i}px ${blur * 2 ** i}px rgb(0 0 0 / ${alpha})`).join(', ');
```

| Parameter | Default | Slider | Rationale |
| --- | --- | --- | --- |
| Layers | 4 | `[4, 1, 6, 1]` | Each layer doubles reach; past 5 the tail is invisible |
| Base y offset | 1px | `[1, 0, 8, 0.5]` | Light from above; larger means higher elevation |
| Base blur | 2px | `[2, 0, 16, 0.5]` | Usually about twice the offset |
| Per-layer alpha | 0.04 | `[0.04, 0, 0.2, 0.005]` | Low per layer; layers add up |
| Ring alpha | 0.06 | `[0.06, 0, 0.2, 0.01]` | A 1px spread ring defines the edge better than a border on tinted backgrounds |

Tint the shadow toward the background hue instead of pure black on colored surfaces. In dark mode shadows barely show; rely on the ring and a slightly lighter surface for elevation.

## Blur

| Parameter | Default | Slider | Rationale |
| --- | --- | --- | --- |
| Backdrop glass | 14px | `[14, 0, 40, 1]` | Below ~8px content behind stays legible and distracting; pair with `saturate(1.4)` |
| Enter blur (`filter: blur`) | 4px | `[4, 0, 12, 0.5]` | Softens an enter or crossfade; above ~8px it smears. Animating blur is expensive on large areas, so check frame rate |
| Shadow blur | see Shadows | | |

## Radius

| Element | Default | Slider | Rationale |
| --- | --- | --- | --- |
| Small control (checkbox, tag) | 6px | `[6, 0, 12, 1]` | |
| Button, input | 8px | `[8, 0, 20, 1]` | Match inputs and buttons that sit side by side |
| Card | 16px | `[16, 0, 32, 1]` | |
| Sheet, modal | 20px | `[20, 0, 40, 1]` | Large surfaces can carry larger radii |
| Pill | 999px | n/a | |

Nested corners must be concentric: inner radius = outer radius minus the padding between them. Expose the outer radius and padding, and derive the inner one, so tuning one never breaks the other.

## Opacity

| Use | Default | Slider | Rationale |
| --- | --- | --- | --- |
| Hover overlay | 0.05 | `[0.05, 0, 0.2, 0.005]` | |
| Pressed overlay | 0.1 | `[0.1, 0, 0.3, 0.005]` | Roughly double the hover |
| Secondary text | 0.6 | `[0.6, 0.3, 1, 0.01]` | Check contrast; below ~0.55 on white usually fails for body text |
| Disabled | 0.45 | `[0.45, 0.2, 0.8, 0.01]` | Pair with a non-color cue |
| Modal scrim | 0.4 | `[0.4, 0, 0.8, 0.01]` | Dims without blacking out context |
| Enter from | 0 | `[0, 0, 1, 0.05]` | Fine to start at 0, as long as a transform also moves |
