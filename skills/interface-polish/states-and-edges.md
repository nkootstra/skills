# States and Edges

Use this for the section 2 sweep. Walk every component on screen through its row in the state matrix, then run the edge sweep against the whole flow. A state that was never designed still exists: it just falls back to whatever the framework renders, which is usually wrong.

## State vocabulary

| State | What it means | What good looks like |
|---|---|---|
| Default | Resting, nothing happening | Clear affordance: it looks like what it does |
| Hover | Pointer over it (pointer devices only) | Subtle shift in background or border; gated behind `@media (hover: hover)` so touch never sticks |
| Active / pressed | Being pressed right now | Feedback starts on pointer down: slight scale (0.97) or darker fill, 100-160ms in, release may be slower |
| Focus-visible | Keyboard focus | High-contrast ring, 2px+, offset from the element, never removed without replacement |
| Disabled | Not available right now | Lowered contrast but still legible; explain why (tooltip or helper text) when the reason isn't obvious |
| Loading | Work in progress | Spinner or progress in place, layout doesn't shift, control can't be re-triggered |
| Success | Work completed | Brief, proportional confirmation; returns to default or moves on |
| Error | Something failed | Says what happened and what to do; keeps user input |
| Empty | No data yet | Explains what goes here and offers the first action |
| Skeleton | Structure known, data pending | Matches final layout closely; shown only after ~300ms to avoid flash |
| Partial | Some data loaded or some items failed | Show what you have, mark what's missing, offer retry for the failed part |
| Overflow | More content than space | Deliberate truncation, wrapping or scrolling; full value reachable |

## Per-component matrix

### Buttons
- Required: default, hover, active, focus-visible, disabled, loading, success (for async actions).
- Loading keeps the button width fixed (spinner replaces or sits beside the label) and blocks re-submission.
- Destructive buttons: distinct color, confirm or offer undo.
- Icon-only buttons have an accessible label and a hit area of at least 24px web / 44pt touch, even if the glyph is 16px.
- Label overflow: long translated labels wrap or truncate predictably; never clip mid-glyph.

### Text inputs
- Required: default, hover, focus-visible, filled, disabled, read-only, error, success (when validation matters), overflow.
- Label always visible; placeholder is an example, never the label.
- Correct `type`, `inputmode` and `autocomplete` so mobile keyboards and password managers work.
- Error appears below the field, linked with `aria-describedby`, and the input value is preserved.
- Font size 16px+ on mobile web so iOS doesn't zoom on focus.
- Long values scroll inside the field; clear button for search fields.
- Postel's law: accept liberal input, store strict output. Trim pasted whitespace, accept phone numbers with spaces or dashes, dates in the user's locale, card numbers with or without spaces. Reformat on blur instead of rejecting.

### Selects and comboboxes
- Required: default, hover, focus-visible, open, option hover/active, selected, disabled, loading (async options), empty results, error.
- Arrow keys move, Enter selects, Escape closes and returns focus to the trigger, typing filters or jumps.
- Empty search result says "No matches for 'xyz'" and, where possible, offers to create it.
- Long option labels truncate with full text available; menu flips when near the viewport edge.
- Async: show loading inside the list, debounce input, handle stale responses arriving out of order.
- Hick's law: decision time grows with the number of equal-weight options. Past ~7, group them, surface recent or suggested options first, or switch to a searchable combobox.

### Lists and tables
- Required: default, row hover, row selected, focus-visible, loading, skeleton, empty, empty-after-filter, error, partial, overflow.
- Distinguish "nothing here yet" from "nothing matches your filter" (the latter offers a clear-filter action).
- Zero, one and many items all look intentional; one item doesn't look like a broken list.
- Columns: numbers right-aligned with tabular figures; long text truncates with tooltip; table scrolls horizontally inside its container, not the page.
- Large sets: pagination or virtualization; keep scroll position on back navigation.
- Bulk selection shows count and a way to clear.

### Async views and data fetching
- Required: initial loading, skeleton, loaded, empty, error, partial, refreshing, stale, offline.
- Doherty threshold: responses under ~400ms keep people in flow. Aim for it with optimistic updates and prefetching; where you can't, delay loading indicators ~300ms, then keep them visible at least ~500ms to avoid flicker.
- Refreshing keeps existing content visible; never blank the screen to reload.
- Optimistic updates for low-risk actions, with rollback and a visible message on failure.
- Error view offers retry and keeps any context (filters, scroll) intact.

### Forms and validation
- Required: pristine, editing, field error, form-level error, submitting, success, disabled submit (only when the reason is shown).
- Validate on blur or submit, not on every keystroke; clear an error as soon as it is fixed.
- On submit failure, move focus to the first invalid field and summarize errors at the top for long forms.
- Never wipe the form on error. Preserve drafts across navigation for long forms.
- Submit button disables while submitting; server must also be idempotent.
- Enter submits single-line forms; Cmd/Ctrl+Enter submits textareas.

### Modals, sheets and popovers
- Required: closed, opening, open, closing, loading content, error content, overflow (scrolling body).
- Focus moves inside on open, is trapped while open, returns to the trigger on close.
- Escape closes; overlay click closes non-critical dialogs; unsaved changes prompt before discard.
- Body scroll locked without layout shift (compensate for scrollbar width).
- Long content scrolls inside the panel with header and actions pinned.
- Sheets respect safe areas and support swipe-to-dismiss on touch.
- Popovers position relative to the trigger, flip at edges, and animate from the trigger.

### Toasts
- Required: entering, visible, hover-paused, exiting, stacked, with action (undo).
- Auto-dismiss after 4-6s, paused on hover and focus; errors that need action don't auto-dismiss.
- Announced via `aria-live="polite"` (assertive only for urgent errors).
- Don't cover primary actions or the thing the toast is about; respect safe areas on mobile.
- Multiple toasts stack and collapse instead of piling up endlessly.

### Navigation
- Required: default, hover, active (current page), focus-visible, disabled, collapsed (mobile), overflow (too many items), badge/notification.
- Current location always indicated, with `aria-current="page"`.
- Back preserves state (scroll, filters, tab). Deep links work and restore the same view.
- Too many items: overflow menu or horizontal scroll with a visible affordance, not wrapping into chaos.
- Skip link to main content on web.

### Media and images
- Required: loading (placeholder with correct aspect ratio), loaded, error (broken source), missing (no image provided), overflow (unusual aspect ratios).
- Reserve dimensions to prevent layout shift; blur-up or solid dominant-color placeholder.
- Broken images fall back to a designed placeholder or initials avatar, not the browser's broken icon.
- `object-fit` chosen deliberately; faces not cropped off.
- Meaningful `alt`; decorative images `alt=""`.
- Video: poster frame, no autoplay with sound, controls reachable by keyboard.

### File upload
- Required: idle, drag-over, invalid drag (wrong type), uploading with progress, processing, success, error per file, cancelled, limit reached.
- State accepted types and size limits before the user tries.
- Show per-file progress and allow cancel; failed files retry individually.
- Reject wrong types and oversized files with a specific message ("PDF only, max 10 MB. This file is 24 MB").
- Clicking the zone opens the file picker; works with keyboard; paste support where natural.
- Uploads survive a brief network drop or at least fail clearly.

## Edge sweep

Run each test against the full flow, not just one screen.

| Edge | How to test | What to look for |
|---|---|---|
| Narrow viewport | DevTools at 320px wide; real small phone | No horizontal page scroll, nothing clipped, tap targets still large enough |
| Ultra-wide | 2560px+ window, or browser zoomed out | Content has a max width, lines stay under ~75 characters, nothing stretched absurdly |
| Slow network | DevTools throttling "Slow 3G" | Skeletons and spinners appear, no double requests, nothing looks frozen, timeouts handled |
| Offline | DevTools "Offline", airplane mode | Clear offline message, queued or blocked actions explained, recovery when back online |
| Double-submit / rapid input | Double-click submit, hammer Enter, click a toggle 10 times fast | One request only, final state matches last input, no race conditions |
| Long strings | Paste a 200-character name, a 40-character unbroken word, a 12-digit number, a long email | Truncation or wrapping is deliberate, layout holds, full value reachable |
| Short strings | Single character names, empty optional fields | Layout doesn't collapse, no orphan separators ("Name ·  · ") |
| Zero / one / many | Seed 0, 1, 2, 1000+ items | Empty state designed, singular grammar ("1 item"), performance and pagination at scale |
| RTL and translation | `dir="rtl"`; pseudo-localize with +30% text length and accented characters | Layout mirrors correctly, icons that imply direction flip, nothing truncates important text |
| Permission denied | Revoke camera, location, notifications; use a role without access | Explains what's missing and how to grant it; no dead buttons |
| Timezone and locale | Change system timezone and locale; test around midnight and DST | Dates, numbers, currencies formatted for the locale; "today" is correct for the user |
| Reduced motion | Enable OS reduce-motion setting | Movement replaced by fades; feedback still present |
| Keyboard only | Unplug the mouse; Tab through everything | Logical order, visible focus everywhere, no traps, all actions reachable |
| Screen reader | VoiceOver (macOS/iOS), TalkBack, NVDA | Every control named, state changes announced, headings structure the page |
| Zoom 200-400% | Browser zoom to 200%, then 400% at 1280px wide; iOS Dynamic Type at largest | Text resizes to 200% without loss; at 400% (320 CSS px wide) content reflows with no horizontal scroll; nothing overlaps or clips |
| First run | Fresh account, cleared storage | Onboarding or empty states guide the first action |
| Session expiry | Expire the token mid-task | User re-authenticates without losing work |
| Destructive actions | Delete, archive, remove | Undo available or confirmation proportional to the cost |

## Recovery

Every error message follows one formula:

1. **What happened**, in plain words. "We couldn't save your changes."
2. **Why**, only if it helps the user act. "Your connection dropped."
3. **What to do next**, as an action. "Try again" button, or "Check your connection and retry."

Rules:
- Never blame the user; never show raw codes or stack traces as the only content (an error ID for support is fine as secondary text).
- Keep what the user entered. Losing input is worse than the error itself.
- Place the message where the problem is: inline for fields, in-place for failed regions, toast only for background actions.
- Offer the action in the message itself (retry, undo, contact with context prefilled) rather than describing it.
- Replace "Something went wrong" with the specific failure every time you can identify it.

Examples:
- Bad: "Error 403." Good: "You don't have access to this project. Ask an owner to invite you." with a "Request access" button.
- Bad: "Invalid input." Good: "Enter a date after today."
- Bad: "Upload failed." Good: "This file is 24 MB. The limit is 10 MB. Compress it or choose a smaller file."
