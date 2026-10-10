# React Components

Use this when building or reviewing a React component that will be reused: a button, a menu, a list, a field, a panel. The goal is a component that is hard to misuse, handles every state without being told, and moves like the rest of the app.

## Anatomy

- **One root, named parts.** Split a component into the parts a consumer might need to rearrange (`Menu`, `MenuTrigger`, `MenuContent`, `MenuItem`) and share state through context, not prop drilling. A monolith with twelve render props is harder to use than four parts.
- **Build on a headless primitive** for anything with focus management, dismissal or positioning (dialog, menu, select, popover, tooltip, tabs). Own the visuals and motion; let the primitive own roles, keyboard and focus trapping. Rebuild only what the primitive cannot do, and say why in a comment.
- **Keep the rationale in the source.** A comment explaining why a value or guard exists ("snaps here because the child's collapse changed the measurement") stops the next person from "fixing" it.

```tsx
const ListContext = createContext<ListState | null>(null);

export function List({ children, ...props }: ComponentProps<"ul">) {
  const state = useListState();
  return (
    <ListContext.Provider value={state}>
      <ul {...props}>{children}</ul>
    </ListContext.Provider>
  );
}

function useList() {
  const ctx = useContext(ListContext);
  if (!ctx) throw new Error("ListItem must be used inside <List>");
  return ctx;
}
```

## API rules

- **Extend the native element's props.** `ComponentProps<"button">` plus your own. Consumers expect `id`, `aria-*`, `data-*`, `onKeyDown` to just work.
- **Forward the ref** to the element that owns focus and layout (React 19: `ref` is a regular prop; earlier: `forwardRef`). Primitives, tooltips and measurement all need it.
- **Merge, don't overwrite.** `className` goes through a merge helper (`cn`) after your defaults. Event handlers the component depends on are composed with the consumer's, never replaced by a spread: if the consumer's `onClick` can disable your optimistic update, the component is fragile.

```tsx
function Tab({ onClick, className, ...props }: TabProps) {
  const { select, index } = useTabs();
  return (
    <button
      {...props}
      className={cn("relative h-control px-3", className)}
      onClick={(e) => {
        select(index); // optimistic: indicator moves before controlled state round-trips
        onClick?.(e);
      }}
    />
  );
}
```

- **Controlled and uncontrolled.** Accept `value`/`defaultValue`/`onValueChange` (or `open`/`defaultOpen`/`onOpenChange`). One hook resolves which mode applies; internal code only reads the resolved value. An uncontrolled dismissible hides itself; passing `open` lets the parent bring it back.

```tsx
function useControllable<T>(value: T | undefined, defaultValue: T, onChange?: (v: T) => void) {
  const [inner, setInner] = useState(defaultValue);
  const controlled = value !== undefined;
  const set = useCallback((v: T) => { if (!controlled) setInner(v); onChange?.(v); }, [controlled, onChange]);
  return [controlled ? value : inner, set] as const;
}
```

- **`asChild` (slot) for polymorphism.** When a button must render as a link, clone the consumer's element and pass your classes and internals into it rather than nesting a `<button>` in an `<a>`. Drop props that are invalid on the new root (`disabled` on an `<a>`) and do not add `role="button"` to a real link. If the project's primitive library uses a `render` prop instead, accept both spellings.
- **Variants are a short closed enum.** `variant: "primary" | "secondary" | "ghost"`, `size: "default" | "compact"`. Map them to classes in one table. No boolean soup (`isPrimary`, `isLarge`, `isGhostish`).
- **Resolution order for ambient settings:** explicit prop, then the nearest provider, then the default. Density, size and surface level are region decisions: one provider around a toolbar or sidebar and every control inside follows. Context crosses portals, so menus opened from the region follow too.
- **Expose state as data attributes** (`data-state="open"`, `data-disabled`, `data-highlighted`) so consumers style states without reaching into internals.
- **Export the motion defaults** as a named object (`bannerMotion`) and accept a `motion` override that is spread over it. Read values when an animation starts, so changing them never restarts one in flight.

## Required states

Every interactive component handles all of these without the consumer wiring them:

| State | Rule |
| --- | --- |
| Rest | Calm. Secondary affordances (shortcut chips, dismiss buttons, timestamps) can wait invisible. |
| Hover | Only for real pointers: check `pointerType === "mouse"` or gate on `(hover: hover)`, or touch leaves the element stuck. Hover-revealed controls stay visible on `(hover: none)` devices. |
| Press | Fast in (100-160ms), slower release (up to ~200ms). Prefer a fixed-pixel inset over `scale` on wide elements: 2% of a 400px button is 8px sideways but under 1px vertically. |
| Focus-visible | Ring only on `:focus-visible`, never on pointer focus. |
| Disabled | Not focusable, not clickable by any route. `pointer-events: none` only blocks the mouse; remove the overlay link or set `disabled`/`tabIndex={-1}` too. |
| Loading | Width never changes: keep the label mounted at `opacity: 0` and overlay the spinner in the same box. |
| Selected / active | Persistent state, distinct from hover. A held-open trigger (menu open) shows the pressed look. |
| Error | Ring or tint plus a message linked via `aria-describedby`. Not color alone. |
| Empty / overflow | Long labels truncate inside a `minmax(0, 1fr)` cell; zero items renders something deliberate. |

**Nothing moves when state changes.** These patterns keep layout still:

- **Weight change:** stack an invisible copy of the label at the heavier weight in the same grid cell, so the visible copy can change weight without reflowing neighbours. Same trick for a label that swaps text ("Copy" / "Copied"): reserve the widest variant.

```tsx
<span className="inline-grid">
  <span className="col-start-1 row-start-1 transition-[font-weight,color] duration-75"
        style={{ fontWeight: selected ? 550 : 400 }}>{label}</span>
  <span aria-hidden className="invisible col-start-1 row-start-1" style={{ fontWeight: 550 }}>{label}</span>
</span>
```

- **Icon swap:** both glyphs mounted in one icon-sized grid cell, crossfading opacity with a little scale and blur. The slot never resizes. The arriving glyph should take slightly longer than the leaving one.
- **Optional slots** (check mark, meta row, trailing action) are always rendered at fixed size so content appearing in them never resizes the parent popup or shifts the gap between rows.
- **Invisible means inert.** A control faded to `opacity: 0` also gets `pointer-events: none`, or it swallows taps meant for what is under it. A banner fading in or out ignores clicks below ~50% opacity.

## Accessibility

- **Roles match behaviour.** `role="menu"` only on a real popup menu; an always-visible list of actions is a `role="group"` with an `aria-label`. Errors and warnings use `role="alert"`; everything else that announces uses `role="status"`.
- **Roving tabindex for groups** (radios, tabs, toolbars): one tab stop. The selected item holds it; with no selection the first item does, or the group becomes unreachable.
- **`aria-activedescendant` for type-to-filter** (combobox, command menu): the input keeps DOM focus, arrows move a highlight, and `preventDefault` on row `pointerdown` stops a click from blurring the field. Scroll the highlighted row into view yourself (the browser won't, since focus didn't move) using offsets, not `scrollIntoView`, which can scroll the page.
- **Keyboard parity.** Arrows wrap, Home/End jump, Enter activates, Escape closes or clears. The keyboard highlight and the pointer highlight should be the same visual. When a list opens, highlight a sensible first target so Enter always does something.
- **Focus ring honesty.** Some browsers report script-driven `focus()` as `:focus-visible`. If a pointer interaction redirects focus programmatically, flag it and suppress the ring for that focus.
- **Restore focus on dismiss.** When something with focus inside closes, move focus to the next logical element (else the previous), never to `<body>`. Restore focus after a step change only if the user was keyboard-driving.
- **Closed means hidden, after the exit.** Keep a collapsing panel mounted through its exit animation, then set `hidden` so it leaves the accessibility tree. Primitives that apply `hidden` immediately freeze the exit mid-flight.
- **Stable announcements.** An animated or cycling label is `aria-hidden`; a static sr-only text carries the meaning. Accessible names track state ("Copy" / "Copied" / "Copy failed").
- **Don't nest interactive elements.** A clickable card uses a stretched overlay link with secondary actions layered above it.
- **Text input details.** Ignore Enter while `e.nativeEvent.isComposing` (IME). Editable fields render at 16px on touch devices so iOS doesn't zoom on focus; never disable zoom with `maximum-scale`.
- **Scope queries.** If a hidden native primitive shares a role with your visible row, query by your own data attribute, or arrow keys land on invisible elements.
- **Scope global shortcuts.** With several instances mounted, only the one containing focus (else the most recent) answers a key. Ignore bare-key shortcuts while typing in a field.

## Motion

- **A few tiers, tokenised.** Three speeds cover almost everything, chosen by the size of what moves: small and frequent (hover, focus ring, tooltip) fastest; indicators and short travel in the middle; dialogs and panels slowest. Import the token; never write a literal duration in a component. A deliberate one-off lives in one named export next to its owner.
- **Exits are quicker than enters**, and usually a plain tween, so a dismissal reads as final rather than the entrance replayed backwards. A state toggle without unmount picks the transition from state: `transition={open ? enter : exit}`.
- **Springs for anything interruptible.** A spring retargets from its current position and velocity. Reopening mid-close continues from where it is; it never snaps to a start frame.
- **Animate `transform` and `opacity`.** Layout properties are off the compositor and are often ignored by reduced-motion handling. Height that must animate goes to a measured pixel value or a `grid-template-rows: 0fr` to `1fr` track, never to `"auto"`, which some libraries resolve from the transformed visual size and overshoot under a scaled parent.
- **One traveling indicator.** Selection pills, hover highlights and focus rings are one element that moves between items, not one per item fading in and out. A fresh pointer entry fades in at the nearest item instead of sliding over from wherever it last was.
- **Don't animate on mount.** Pre-checked, pre-open and initially visible states render in place (`initial={false}`, or `duration: 0` for the first measurement).
- **Don't stack measured animations.** A wrapper animating to a measured height springs only when it toggles; when a child's change altered the measurement, snap. Two springs chasing each other land late and diverge mid-flight.
- **Gate on measurement.** Don't show an overlay until its target rect is measured, or it animates from a wrong position. Never publish zeroed rects from a hidden popup.
- **Acknowledge, then close.** A pick in a select holds the popup ~300ms so the check and selection indicator are seen. Escape and outside press still close immediately.
- **Origin follows the resolved side.** A popover flipped above its trigger grows from its bottom edge.
- **Reduced motion is fewer and gentler, not none.** Drop transforms, slides and layout motion; keep short opacity and color fades. Read the preference inside the component (`useReducedMotion`) so it works without the app setting it globally. Autoplay and infinite loops stop entirely and show a static equivalent.
- **Presence callbacks through a ref.** If a library hands out a new "safe to remove" callback each render, depending on it restarts the exit on every parent re-render.

## Performance

- **Per-frame values never go through React state.** Cursor-follow offsets, drag positions, progress fills and scroll-linked values are motion values (or refs plus direct style writes). Derive every dependent style from the same source value with `useTransform` so linked elements render the same frame; a change listener that sets state lags a frame.
- **Batch measurement.** Coalesce resize and registration triggers into one `requestAnimationFrame` pass. Cache parsed computed styles per element instead of calling `getComputedStyle` per keystroke.
- **Do work when it is decided, not in an effect.** Scroll a keyboard-highlighted row at the moment the move is chosen; an effect runs a frame later and the scroll lags the highlight.
- **Stable keys for morphing groups.** When contiguous selections merge into one block, reuse an ID when a run overlaps its previous version so it morphs instead of exiting and re-entering.

## Tokens and styling

- **Use the project's tokens; don't invent parallel ones.** Colors, radii, type sizes, durations and heights come from the existing system.
- **One control height ladder** shared by buttons, inputs, select triggers and menu rows (for example 36px default, 28px compact) so a popup row lines up with the trigger that opened it. Compact steps everything down together: text, icon, padding, gap.
- **State fills are relative overlays** (a foreground or background tint at a few percent) so hover and selected read on any surface level, light or dark.
- **Elevation through context.** A floating surface reads the current level and renders one step above it, so a menu inside a dialog doesn't melt into it. Keep the shadow weight constant so a popover always reads as a popover.
- **Concentric corners.** `inner = max(0, outer - inset - border)`. Don't reuse a fixed radius pair at a different padding.
- **Type by role, not pixel.** Pick from named roles (title, body, caption) that pair size with line height. Beware merge helpers that misread custom `text-*` utilities as colors and drop them.
- **Image edges.** Thumbnails and avatars get a 1px inset outline at ~10% black (light) or white (dark), so pale images keep their shape without a border changing the box.

## Before you call a component done

- [ ] Accepts and forwards native props, `ref` and `className`; consumer handlers compose with internal ones.
- [ ] Works controlled and uncontrolled; `size` follows prop, then provider, then default.
- [ ] Rest, hover (pointer only), press, focus-visible, disabled, loading, selected and error states all exist and none shifts layout.
- [ ] Full keyboard operation with visible focus only for keyboard; focus returns somewhere sensible on close.
- [ ] Correct roles and accessible names, including state changes; nothing announces repeatedly.
- [ ] Every duration and easing comes from a motion token; exits are faster than enters.
- [ ] Interrupting any animation mid-flight continues smoothly from the current value.
- [ ] Nothing animates on first render.
- [ ] Reduced motion keeps fades and removes movement; tested with the OS setting on.
- [ ] Per-frame updates cause zero React re-renders (check with the profiler).
- [ ] Touch: no stuck hover, hover-revealed controls visible, targets at least 24px (44px preferred), fields 16px.
- [ ] Inside a dialog, a scaled container and a compact region: still correct.
- [ ] Non-obvious values and guards have a comment explaining why.
