# Recreation

The recreate-to-learn loop in detail: observe precisely, guess the technique, build the gist, then close the gap one difference at a time.

## 1. Observe

Describe the effect in observable terms before guessing how it was built. Watch it several times at full speed for the feel, then slowed down for the mechanics. Answer each question; "not sure" is a fine answer and tells you where to look closer.

**What moves**
- Which elements change? List them separately, including the ones that only fade or dim.
- Which properties change: position, size, rotation, opacity, color, blur, shape, content?
- Is it one element transforming, or one element being swapped for another (crossfade, shared element)?

**Origin and path**
- Where does motion start from: the element's center, a corner, the trigger, the pointer, the edge of the screen?
- Straight line or curve? Does it travel along an arc?
- Does the start point change depending on where you clicked?

**Deformation**
- Does the shape stay rigid, or does it stretch, squash, bend, ripple, or curve at the edges?
- Do edges stay straight? Do corners keep their radius as it grows?
- Is the content inside distorted with it, or does it stay crisp while the container changes?

**Timing**
- Roughly how long? Count frames in a recording (see Frame-by-frame study).
- Fast start then settle (ease-out), smooth both ends (ease-in-out), or overshoot and settle (spring)?
- Do parts start at the same time, or stagger? In which order?
- Does anything wait for something else to finish?

**Layering**
- What is in front of what during the motion? Does that change midway?
- Is anything clipped or masked: content revealed by a growing shape, or cut off at a container edge?
- Is there blur, a shadow change, or a light/highlight moving across?

**Interactivity**
- Is it triggered (click, hover, scroll into view) or tracked (follows the pointer, scroll position, drag)?
- If tracked, is it 1:1 with input or smoothed/lagging behind it?
- What happens on release: snap back, continue with momentum, settle to the nearest point?

**Interruption**
- Trigger it again mid-animation. Does it restart, reverse from where it is, or ignore you?
- Reverse direction mid-drag. Does it follow immediately?
- Reversing smoothly from the current position points to springs or a velocity-aware system; jumping to the start points to keyframes or a restarted tween.

Write the result as one paragraph, e.g.: "The card scales from the tap point to fill the screen over ~400ms with a slight overshoot. Its corners stay rounded until the last 20 percent. The content behind dims and scales down to ~0.94. Tapping during the expansion reverses it from wherever it is."

## 2. Pick a technique

Start from the tell-tale sign, not from the tool you know best. The simplest technique that produces the sign wins.

| Technique | Use when | Tell-tale sign in the reference |
| --- | --- | --- |
| CSS transforms (`translate`, `scale`, `rotate`) | Rigid movement, growth, rotation | Shape stays rigid; content scales with the container; text may look soft mid-scale |
| CSS transitions / keyframes | State A to state B, or a fixed loop | Same path every time; restarts or jumps when interrupted |
| Springs (Motion, React Spring, WAAPI with a generated curve) | Gesture release, interruptible UI | Overshoot and settle; reverses smoothly from mid-animation |
| FLIP (measure, invert, play) | Layout changes: reordering, resizing, moving between containers | Element moves between positions that are determined by layout, not hardcoded offsets |
| Shared element / `layoutId` | One element appears to become another across views | A thumbnail grows into a detail view; two separate elements, one continuous motion |
| View Transitions API | Whole-page or large-region state changes, route changes | Old and new states crossfade or morph as snapshots; content is briefly not interactive |
| `clip-path` (`inset`, `circle`, `polygon`) | Reveals and wipes with geometric edges | Content appears through a growing rectangle or circle without scaling; edges are sharp |
| CSS / SVG masks (gradient or image masks) | Soft-edged reveals, fades along a direction | Reveal edge is soft or follows a gradient; content does not move |
| SVG paths (`d` morphing, `stroke-dashoffset`) | Line drawing, icon morphs, shape interpolation | A stroke draws itself; one icon shape morphs into another |
| SVG filters (`feTurbulence` + `feDisplacementMap`, `feGaussianBlur` + `feColorMatrix`) | Organic distortion, liquid, gooey merging | Wobbly or rippling edges; blobs merge with smooth necks (gooey); noise-like warping |
| Canvas 2D | Many particles, generative drawing, trails | Hundreds of independent elements; motion trails; nothing selectable in the DOM |
| WebGL / shaders | Mesh deformation, per-pixel effects, lighting, refraction | Surfaces bend non-rigidly (page curl, cloth, jelly); chromatic aberration, refraction, glow that reacts to content |
| Scroll-driven animations (`animation-timeline`, `useScroll`) | Progress linked to scroll position | Scrubbing back and forth with the scroll reverses the motion exactly |

Mixed effects are common: a card expand may be FLIP for position, `clip-path` for the reveal, and a spring for timing. Name each layer separately.

Inspect the source when you can: DevTools Elements panel (look for `canvas`, inline `svg` with `filter`, `view-transition-name`, `clip-path` in computed styles), the Animations panel, and the Network tab for shader or Lottie files. If it is a Lottie or video, the "technique" is an asset; decide whether to recreate it in code or with a motion tool.

## 3. Build the gist, then the hard part

1. Build the simplest version that captures the gist with blank shapes, usually a transform with a spring or ease-out curve.
2. Put the timing parameters in the tuning panel from the start ([tuning-panel.md](tuning-panel.md)); recreation is mostly tuning.
3. Add the hard part one layer at a time, naming the technique and why: "edges curve inward, so the container is not a rigid rect: try a `clip-path` path or an SVG mask".
4. After each step, compare with the reference and log the difference (template below).
5. Stop when the learning goal is met. Recreations do not need to be polished.

## Frame-by-frame study

- **Slow-motion screen recording.** Record the reference (QuickTime, Cmd+Shift+5 on macOS, or a phone at 120/240fps for device UI). Step through frames in QuickTime with the arrow keys, or in a video editor. At 60fps, 6 frames is 100ms; count frames from first movement to rest to get the duration.
- **Record both side by side.** Put your recreation next to the reference and record both at once; differences in timing are obvious when played together and invisible when compared from memory.
- **DevTools Animations panel** (Chrome: More tools > Animations). Captures CSS animations, transitions and WAAPI: shows duration, delay and easing, and lets you replay at 25% or 10% speed and scrub. Does not capture JS-driven per-frame animation (most spring libraries, canvas, WebGL).
- **Slow down JS animation.** For Motion, set a long `transition` duration temporarily; for rAF-driven code, scale the time delta. In Chrome DevTools Rendering, enable "Paint flashing" and "Layer borders" to see what repaints and what is composited.
- **Performance panel.** Record the interaction to see which properties change per frame and whether it is layout, paint, or composite only; this often reveals the technique (a `transform` on a layer versus a canvas redraw).
- **Pause on a frame.** In the Animations panel, pause and inspect the element: computed `transform`, `clip-path`, and `filter` show the exact intermediate values.
- **Reduce to one property.** Mentally (or in the recording) track one property at a time across frames: first only position, then only scale, then only opacity. Effects that feel magical are usually three simple curves with offset start times.

## Comparison log

Keep a short log per recreation. It turns a vague "still feels off" into the next concrete step, and becomes a reusable note on how the effect works.

```markdown
## Recreation: <effect name>

Reference: <link or recording path>
Learning goal: <what you want to understand, e.g. "how the corners stay round while it expands">
Observation: <the one-paragraph description from step 1>

| Step | Change made | Technique | Still differs from reference | Next |
| --- | --- | --- | --- | --- |
| 1 | Scale + translate from tap point | Transform, spring 0.4 / 0.1 | No overshoot; background does not dim | Raise bounce, add scrim |
| 2 | Added scrim and background scale 0.94 | Opacity, transform | Corners square off when scaled | Animate width/height via FLIP or clip-path instead of scale |
| 3 | | | | |

Final values: <JSON copied from the tuning panel>
What I learned: <the trick, in one or two sentences>
Open questions: <anything still unexplained>
```
