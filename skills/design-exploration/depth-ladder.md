# Depth Ladder

What each level from 1 to 10 looks like, the moves that move you up a band, a worked climb, and how to tell when the concept itself has run out.

## The levels

| Level | Characterized by |
| --- | --- |
| **1** | It technically works on the happy path. Defaults everywhere. Breaks or looks wrong on anything unexpected. |
| **2** | Obvious gaps closed: empty, loading and error states exist. Still feels assembled rather than designed. |
| **3** | Consistent with the rest of the product: spacing, type, components and wording follow the system. Where most shipped work stops. |
| **4** | Clear hierarchy: the eye lands on the right thing first, and secondary things recede. Someone new knows what to do without reading. |
| **5** | Rhythm and proportion feel intentional. Copy is specific to this context, not generic. Edge cases (long names, slow networks, zero and many items) are handled gracefully. |
| **6** | Feedback and motion explain what happened. State changes are legible. It feels responsive and calm. Keyboard, screen reader and touch all work well. |
| **7** | It has a signature detail: one thing that is unmistakably considered and that people notice. The concept starts to feel like it has a point of view. |
| **8** | A new mechanism inside the concept: something that changes how it works, not just how it looks, discovered by living with it. Feels inevitable in hindsight. |
| **9** | Edited: things have been removed and it got better. Every remaining element earns its place. |
| **10** | Nothing left to add or remove. Rare, and usually reached only on a small scope. |

## Bands and their moves

### 1 to 3: Fixing

The question is "what is broken or missing?" Answers are usually obvious once you look.

- **Enumerate states**: empty, loading, partial, error, success, disabled, offline, first-use, hundredth-use.
- **Stress the content**: longest plausible string, zero items, one item, a thousand items, right-to-left text, missing image.
- **Check consistency**: does it use the same components, spacing scale, type ramp, icons and verbs as the surrounding product?
- **Close interaction gaps**: focus states, hover vs. touch, what happens on double-click, back button, refresh mid-action.
- **Fix the copy that's wrong**: placeholder text, developer wording, "Error: 500".

### 4 to 6: Refining

The question is "what would make this clearer, calmer, more confident?" Answers require judgment.

- **Hierarchy**: decide the single most important thing and make everything else quieter. Squint at it.
- **Rhythm**: align to a grid, make spacing relationships express grouping, remove one-off values.
- **Copy**: rewrite every string for this exact moment. Verbs on buttons, specifics in errors, no filler.
- **Motion**: make transitions explain cause and effect; remove motion that only decorates.
- **Feedback**: every action gets a visible response within 100ms, even if the result takes longer.
- **Accessibility as quality**: the keyboard path and screen reader output should be as considered as the visual one.

### 7 to 8: Inventing

The question is "what would make this remarkable?" There is no obvious answer, and the moves from SKILL.md (zoom in, remove, name what's wrong, study the best, make more versions) do most of the work here.

- **Signature detail**: one interaction, transition or piece of feedback that is crafted far beyond the rest. Pick one, not five.
- **New mechanism inside the concept**: a change to how it works that the concept allows but didn't ask for, such as anticipating the next action or collapsing two steps into one.
- **Live with it**: use it repeatedly, on real data, in the real context. Level 8 ideas almost never come from looking at a static mock.
- **Make five versions of the one key moment** and pick the best, rather than reasoning about which would be best.

### 9 to 10: Editing

The question is "what can go?" Progress is measured by what was removed.

- Remove each element in turn and see if anything was lost.
- Merge controls that do related things.
- Replace explanation with a design that doesn't need explaining.
- Cut the signature details that didn't make the final cut: one is stronger than three.
- Use the "what to cut" checklist below.

## Worked climb: a file upload dropzone

| Level | What changed | Why |
| --- | --- | --- |
| **1** | A dashed box with "Drop files here" and a hidden file input. Dropping a file uploads it. | It works on the happy path. |
| **2** | Added a click-to-browse fallback, a progress bar per file, an error message on failure, and a retry button. | Many people don't drag; uploads fail; failure without retry is a dead end. |
| **3** | Replaced custom colors and spacing with design system tokens; used the standard button and error components; matched the product's verbs ("Upload" not "Submit"). | It looked like it came from another product. |
| **4** | Made the drop target state obvious: the whole zone highlights on drag-over, and the primary label says what's accepted ("PDF or image, up to 20 MB"). | People hovered uncertainly, and found out about limits only after failing. |
| **5** | Handled edge cases: rejected files explain why per file, long filenames truncate in the middle so the extension stays visible, many files collapse into a summary with a count. | Real usage includes wrong types, huge batches and names like `Q3-final-final-v2-REVISED.pdf`. |
| **6** | Added motion that explains: files fly from the drop point into the list, progress fills smoothly, completed files settle with a short check. Full keyboard and screen reader support with announced progress. | The transition from "dropped" to "uploading" was abrupt and invisible to non-visual users. |
| **7** | Signature detail: dragging a file anywhere onto the page, not just the box, brings the dropzone to meet it, growing toward the cursor. | The box was a small target; letting the zone come to the file makes dropping feel effortless and is noticeably considered. |
| **8** | New mechanism: uploads start the moment a file is picked, before the person confirms the form, and the form's other fields are prefilled from the file (title from filename, date from metadata). | Living with it showed the real wait was the upload after submit, and that people retyped what the file already knew. |

Beyond 8, the next step would be editing: the per-file progress bars could become one aggregate bar now that uploads start early, and the "Drop files here" label could go entirely if the page-wide drop is discoverable enough.

## Levels log template

Keep this as you iterate and show it to the user, so they can see the climb and decide when to stop.

```markdown
## Levels log: <component or flow>

Concept: <one-line core mechanism of the chosen direction>
Facets: <the quality facets this is judged against>

- **Level 1**: <starting point>.
- **Level 2**: <what changed>. Because <reason>.
- **Level 3**: <what changed>. Because <reason>.
- **Level 4**: <what changed>. Because <reason>.
- **Level N**: removed <thing>. Because <it wasn't needed / it competed with X>.

Currently at: <level>, judged on <facet>.
Next candidate move: <move>, expected to <effect>.
Ceiling signs so far: <none / list>.
```

Rules for the log:

- Every entry has a **because**. A change without a reason isn't a level, it's churn.
- Removals count as levels, and are often the best ones.
- Be honest about the level. Calling something a 7 when it lacks a signature detail devalues the scale.
- Not every change is a full level. Batch small fixes into one entry.

## Signs you've hit the concept's ceiling

Go back to range when several of these are true:

- **Moves stop compounding.** Each change trades one problem for another instead of making things strictly better.
- **The same complaint survives every iteration.** If people still say "this takes too long" after five refinements, the mechanism is the problem, not the execution.
- **Polish is hiding a structural issue.** You're adding motion or copy to explain something the structure should make obvious.
- **The signature detail won't come.** At level 6 to 7, nothing distinctive suggests itself after several honest attempts.
- **The best idea you have doesn't fit.** A level 8 mechanism keeps occurring to you but requires breaking the concept. That idea is a new direction.
- **A direction you rejected keeps looking better.** Revisit it with what you've learned.

When going back, bring the levels log. What you learned climbing this concept usually reshapes the range: some directions become obviously wrong, and new ones appear.

## What to cut: less, but better

Run this checklist at every level from 5 upward, and as the main activity at 9 and 10.

- [ ] **Typefaces**: one family, two at most. Remove any used for a single element.
- [ ] **Type sizes**: can two sizes merge without losing hierarchy?
- [ ] **Colors**: is every color carrying meaning? Remove decorative ones.
- [ ] **Actions**: is there exactly one primary action? Can a secondary action move to a menu or disappear?
- [ ] **Options and settings**: could a good default replace this choice?
- [ ] **Explanatory text**: could the design make this sentence unnecessary?
- [ ] **Confirmation dialogs**: could undo replace them?
- [ ] **Borders, dividers, shadows**: can spacing do the grouping instead?
- [ ] **Icons**: does each one add recognition, or just decoration next to a label?
- [ ] **Animations**: does each one explain a change? Keep one signature interaction; cut the rest to simple transitions.
- [ ] **Steps**: can two steps merge, or one happen automatically?
- [ ] **Features**: what would happen if this shipped without it? If the honest answer is "nothing much", cut it.

Cut first, then see if anything was lost. It's easier to add back something missed than to justify removing something established.
