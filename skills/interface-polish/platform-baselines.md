# Platform Baselines

Use this for section 1. The baseline is what users already get from the platform's own apps. Match it first, then exceed it. Anything below this floor reads as poorly made even when nobody can say why.

## iOS

**Navigation**
- Tab bar for 2-5 top-level destinations; navigation stack with large titles that collapse on scroll.
- Back button top-left with the previous title; edge swipe from the left goes back and must never be blocked.
- Modals as sheets (`.sheet`, page or form sheet) with detents where partial height makes sense.

**Type**
- SF Pro via the system font; use Dynamic Type text styles (Large Title 34, Title 1 28, Title 2 22, Title 3 20, Headline 17 semibold, Body 17, Callout 16, Subheadline 15, Footnote 13, Caption 12/11).
- Support Dynamic Type up to accessibility sizes; layouts reflow rather than truncate.

**Hit targets**: 44x44pt minimum.

**Sheets and modals**: grabber on resizable sheets, swipe down to dismiss, confirm before discarding edits (`interactiveDismissDisabled` plus a prompt). Action sheets for destructive choices; alerts only for critical interruptions.

**Gestures**: swipe back, swipe actions on list rows, pull to refresh, long press for context menus with preview, pinch to zoom on media. Never override system edge gestures.

**Haptics**: selection feedback on pickers and toggles, impact on snaps and drops, notification success/warning/error on outcomes. Sparse: haptics on every tap become noise.

**Focus and keyboard**: full keyboard access and hardware keyboard shortcuts on iPad; Return key labelled for the action (Next, Search, Done); keyboard avoids covering the focused field.

**Dark mode**: semantic system colors (`label`, `systemBackground`, `secondarySystemBackground`); elevated surfaces get lighter in dark mode, not shadows.

**Safe areas**: respect notch, Dynamic Island and home indicator; content scrolls under translucent bars; bottom actions sit above the home indicator.

**Scroll**: native momentum and rubber-banding, tap status bar to scroll to top, large title collapse.

## Android

**Navigation**
- Navigation bar (bottom) for 3-5 destinations; navigation rail on tablets; drawer for many destinations.
- Top app bar with up arrow; system back (button or predictive back gesture) must always work and behave predictably.
- Support predictive back animation on Android 14+.

**Type**
- Roboto or the device font through Material 3 type roles (Display, Headline, Title, Body, Label; Body Large 16sp, Body Medium 14sp, Label Large 14sp).
- Use `sp` for text so system font scaling applies; test at 200% font scale.

**Hit targets**: 48x48dp minimum, with 8dp spacing between targets.

**Sheets and modals**: modal bottom sheets with drag handle, dialogs for confirmations, full-screen dialogs on small screens for complex input. Scrim dismisses non-critical sheets.

**Gestures**: system back from either edge, swipe to dismiss on list items and notifications, pull to refresh, long press for selection mode.

**Haptics**: `HapticFeedbackConstants` (CONFIRM, REJECT, CLOCK_TICK, LONG_PRESS); respect the system haptics setting.

**Focus and keyboard**: visible focus for D-pad and keyboard (ChromeOS, tablets, TV); IME action matches the field (`imeOptions`); content resizes when the keyboard opens.

**Dark mode**: Material 3 color roles with tonal surfaces; support dynamic color (Material You) where it fits the brand.

**Safe areas**: edge-to-edge is the default on Android 15; handle window insets for status bar, navigation bar, cutouts and IME.

**Scroll**: stretch overscroll (Android 12+), collapsing top app bar, FAB that hides on scroll where appropriate.

## Web app

**Navigation**: persistent sidebar or top nav; current location marked with `aria-current`; URLs reflect state (tabs, filters, selected item) so back, refresh and sharing work; breadcrumbs for deep hierarchies.

**Type**: system stack or one well-chosen sans (Inter, Geist); body 14-16px for dense apps, 16px for content; line-height 1.4-1.6 for body; tabular numbers in tables; `text-wrap: balance` on headings.

**Hit targets**: Fitts's law: time to hit a target grows with distance and shrinks with size, so frequent and primary actions get large targets near where the pointer or thumb already is; screen edges and corners are effectively infinite targets on desktop. At least 24x24px (WCAG 2.2 AA minimum); 44x44px preferred for primary actions and anything used on touch. Expand small icons' hit areas with padding or pseudo-elements.

**Semantic HTML**: `<button>` for actions, `<a href>` for navigation, `<label>` on every input, landmarks (`<nav>`, `<main>`), headings in order. A `<div onClick>` loses keyboard, focus and screen reader support that the right element gives for free.

**Sheets and modals**: native `<dialog>` or an accessible primitive (Radix, React Aria, Base UI); focus trap, Escape closes, focus returns to trigger, scroll lock without layout shift. Drawers on mobile breakpoints.

**Gestures**: none required on desktop; on touch, swipe-to-dismiss for drawers and toasts. Hover reveals must have a non-hover equivalent.

**Haptics**: generally unavailable; don't fake it with sound.

**Focus and keyboard**: `:focus-visible` rings with 3:1 contrast; logical tab order; skip link; arrow keys within composite widgets (menus, tabs, listboxes); command palette (Cmd/Ctrl+K) for apps with many actions; shortcuts discoverable in menus or tooltips.

**System fonts**: `font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif` as the baseline; `-webkit-font-smoothing: antialiased` on macOS.

**Dark mode**: follow `prefers-color-scheme` by default with a manual override; set `color-scheme` so native controls and scrollbars match; no flash of wrong theme on load.

**Safe areas**: `viewport-fit=cover` plus `env(safe-area-inset-*)` for fixed bars on mobile; `100dvh` instead of `100vh`.

**Scroll**: scroll restoration on back; `overscroll-behavior: contain` on modals and side panels; no scroll hijacking; sticky headers that don't eat half the screen on mobile.

## Marketing site

**Navigation**: simple top nav, 4-7 items, clear primary CTA; collapses to a menu on mobile that's usable one-handed; logo links home.

**Type**: larger scale than apps: body 17-20px, hero 48-96px with tight letter-spacing and `text-wrap: balance`; max line length ~65-75 characters.

**Hit targets**: 44px+ for all CTAs and nav links on mobile.

**Modals**: avoid them. No newsletter popup on first visit. Video lightboxes close with Escape and overlay click.

**Focus and keyboard**: every link and CTA reachable; visible focus styled to match the brand rather than removed.

**Performance**: LCP under 2.5s, CLS under 0.1; images sized and lazy-loaded below the fold; fonts preloaded with `font-display: swap` and fallback metrics matched.

**Dark mode**: optional, but if supported, art and screenshots need dark variants.

**Scroll**: native scroll; reveal animations subtle, once only, and never hide content from no-JS or reduced-motion users.

**Meta**: Open Graph image per page, favicon in all sizes, sensible 404.

## How to exceed it

### iOS
- Interactive, interruptible transitions: a sheet that follows the finger and can be caught mid-dismiss.
- Context menus with real previews and useful actions, not a duplicate of the visible buttons.
- Haptics paired with visual snaps so a drag feels like it has detents.
- Matched-geometry transitions from a thumbnail into its detail view.
- Live Activities, widgets and Shortcuts support where the app has glanceable or repeatable tasks.
- Empty states and onboarding that feel written by a person.

### Android
- Predictive back that previews the destination with a custom shared-element transition.
- Dynamic color that still keeps brand accents legible.
- Thoughtful tablet and foldable layouts (list-detail, posture-aware) instead of stretched phone UI.
- Material motion (container transform) used for genuine continuity, not decoration.
- Widgets and quick settings tiles for frequent actions.

### Web app
- Optimistic UI everywhere it's safe: actions feel instant, sync quietly, roll back clearly.
- Command palette and keyboard shortcuts that make power users faster than mouse users.
- URL-addressable everything: every view, filter and selection is linkable.
- Undo instead of confirmation dialogs for reversible destructive actions.
- Prefetch on hover or intent so navigation feels instant.
- Polished micro-interactions: press scale, popovers that grow from their trigger, toasts that stack.
- Copy-to-clipboard confirmations, drag-and-drop with clear drop targets, paste-to-upload.

### Marketing site
- The product shown working (interactive demo, real UI, short loops) instead of abstract illustrations.
- Typography with real attention: optical sizes, kerning on display type, hanging punctuation.
- A memorable detail in an overlooked place: a considered 404, a footer easter egg, a cursor that reacts.
- Fast enough that it feels static even with motion; zero layout shift.
- Social cards that are designed, not default.
