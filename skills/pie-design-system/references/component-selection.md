# PIE Component Selection Guide

When multiple components could serve a need, use these decision guides.

> **Figma first:** The PIE Figma library embeds "when to use / when not to use" annotations and do/don't examples directly on component frames. If the user has access to the PIE Figma file, use `get_design_context` on the relevant component node to pull richer visual guidance. The decision guides below are a text summary — the Figma design may have more nuance or reflect newer decisions.

---

## Overlays: Modal vs Bottom Sheet vs Side Sheet

### Modal (`pie-modal`)
**Use when:**
- You need to interrupt the user to drive a decision or gather input
- Confirming a destructive or irreversible action (e.g. "Delete order?")
- Displaying urgent information that requires acknowledgement before continuing
- Content is short and focused — a single task with clear completion

**Don't use when:**
- Content is long or requires scrolling — use a side sheet instead
- The action is non-critical or informational — use a notification or toast
- You're on a mobile-primary flow where a bottom sheet is more natural
- You need multiple modals at once (avoid this pattern entirely)

### Bottom Sheet (`pie-bottom-sheet`)
**Use when:**
- The surface is mobile or small-screen-first
- Presenting supplementary actions or information without fully obscuring main content
- You want a natural thumb-reachable interaction on mobile
- Content is secondary to what's on screen (filters, quick settings, action menus)

**Don't use when:**
- Designing primarily for desktop — use a modal or side sheet instead
- Content is complex or long-form — use a full page or side sheet

### Side Sheet (`pie-side-sheet`)
**Use when:**
- Displaying secondary content that complements the main view (e.g. filters, details panel)
- The user needs to reference main content while interacting with the sheet
- Content is too long for a modal but doesn't warrant a full page navigation
- Providing a secondary navigation layer or contextual detail view

**Don't use when:**
- The task requires full focus and background interaction should be blocked — use a modal
- On small screens where a full-width bottom sheet would be more appropriate

### Quick decision
```
Requires user decision or confirmation?         → Modal
Mobile-first, supplementary content?           → Bottom Sheet
Long content, user needs to see main view?      → Side Sheet
```

---

## Feedback: Notification vs Toast

### Notification (`pie-notification`)
**Use when:**
- The message is persistent and contextually relevant to the current page or form
- You need a warning or error that stays visible until the user resolves it
- Providing inline feedback next to the relevant content (e.g. form error summary at top of form)
- The message relates to the user's broader context, not just a single completed action

**Variants:**
- **info** — supplementary info, no urgent action needed, can auto-dismiss
- **success** — confirms task completion, may auto-dismiss
- **warning** — persists until dismissed or user proceeds; action may be needed
- **error** — always persists until resolved; never auto-dismiss
- **neutral** — generic, non-action messages

**Don't use when:**
- Providing brief feedback after a completed action — use a toast instead
- Pinning to the top of the page as a fixed banner — that's toast's role

### Toast (`pie-toast`)
**Use when:**
- Confirming that a user action completed (e.g. "Item added to basket", "Copied to clipboard")
- The message is temporary and the user doesn't need to act on it
- Feedback is low-stakes and shouldn't interrupt the user's flow

**Don't use when:**
- The message is an error that needs resolution — use a notification
- The message needs to persist — toasts auto-dismiss
- Multiple simultaneous messages — queue them or use inline notifications

### Quick decision
```
Persists until user acts?            → Notification
Brief confirmation of completed action? → Toast
Inline, next to relevant content?    → Notification
Bottom of screen, non-blocking?      → Toast
```

---

## Loading: Spinner vs Skeleton vs Progress Bar

### Spinner (`pie-spinner`)
**Use when:**
- Wait time is approximately 2–5 seconds
- Loading a single discrete piece of content (data fetch, form submission)
- You don't know the shape of the content being loaded

**Don't use when:**
- Multiple spinners would appear on the same page — use skeleton instead
- Loading an entire page layout — skeleton gives better perceived performance
- The operation is > 5 seconds — show a progress bar if determinate

### Skeleton (`pie-skeleton`)
**Prefer over spinner for page-level and list loading.** Skeletons give better perceived performance because they show the shape of incoming content — the page feels like it's already partly loaded. Use spinner only for small, isolated fetches where the content shape is unknown.

**Use when:**
- Loading a full page, feed, list, or card grid
- You know the approximate shape of the content (you can mirror the real layout in skeleton blocks)
- You want to reduce perceived loading time — skeletons reliably feel faster than a centered spinner

**Don't use when:**
- Loading a small, isolated element (e.g. one button's data) — spinner is simpler
- Content shape is entirely unknown — spinner is more honest than a skeleton that doesn't match

### Progress Bar (`pie-progress-bar`)
**Use when:**
- The operation has a known duration or step count (file upload, multi-step process)
- You can communicate meaningful progress (not just "loading...")

**Don't use when:**
- Duration is unknown — use a spinner instead

### Quick decision
```
Short, isolated fetch (2–5s)?         → Spinner
Large page/list, known content shape? → Skeleton
Known duration or step count?         → Progress Bar
```

---

## Interactive Labels: Chip vs Tag vs Badge

### Chip (`pie-chip`)
**Use when:**
- The user needs to interact with it: select, filter, or trigger an action
- Representing selectable options (e.g. cuisine filters: "Pizza", "Sushi")
- User can add, remove, or toggle the chip

**Variants:** selection, filter, action

**Don't use when:**
- No interaction is required — use a tag instead

### Tag (`pie-tag`)
**Use when:**
- Displaying a label or category that is purely informational
- Showing metadata, taxonomies, or status labels with no action
- Examples: "New", "Sponsored", "Vegetarian"

**Don't use when:**
- The user needs to interact with it — use a chip instead

### Badge (`pie-badge`)
**Use when:**
- Showing a count or short status overlaid on or adjacent to another element
- Displaying notification counts ("3 unread"), status labels ("Beta"), or emphasis tags

**Don't use when:**
- You need an interactive filter — use a chip
- The label is a long category name — use a tag

### Quick decision
```
User can click / toggle it?           → Chip
Informational category label?         → Tag
Count or short status overlay?        → Badge
```

---

## Form Inputs: Text Input vs Textarea vs Select

### Text Input (`pie-text-input`)
**Use when:** Single-line free-text entry (name, email, search, phone number, card number)

**Don't use when:** Input is likely to be more than one line — use textarea

### Textarea (`pie-textarea`)
**Use when:** Multi-line free-text entry (addresses, descriptions, comments, messages)

### Select (`pie-select`)
**Use when:** Choosing one option from a predefined list (country, category, sort order)
**Don't use when:** The list is very long and needs search — consider a custom dropdown/combobox

### Checkbox vs Radio vs Switch
- **Checkbox** — multiple independent selections (can select 0, 1, or many)
- **Radio** — exactly one from a group (mutually exclusive options)
- **Switch** — single on/off toggle with immediate effect (settings, preferences)

---

## Buttons: Button vs Icon Button vs FAB vs Link

### Button (`pie-button`)
**Use when:** Primary, secondary, or destructive actions with a text label. Most buttons on a page.

**Size guidance:**
- `large` (56px) — wide layouts, primary search/CTA
- `medium` (48px) — default for most page actions
- `small` (40px) — compact UIs, tables, inline actions
- `xsmall` (32px) — very constrained spaces; not available for primary variant

### Icon Button (`pie-icon-button`)
**Use when:** A button with only an icon (no visible text). Always include `aria-label` for accessibility.

**Don't use when:** The action isn't obvious from the icon alone — use a labeled button

### FAB — Floating Action Button (`pie-fab`)
**Use when:** The single most important action on a screen (e.g. "Add to basket")
**Rules:** One FAB per screen. Reserve for the primary action.

### Link (`pie-link`)
**Use when:** Navigation to another page or URL; inline text links within copy

**Don't use when:** The action modifies state (submits, deletes, creates) — use a button

---

## Tooltip vs Popover

### Tooltip (`pie-tooltip`)
**Use when:** Brief label or hint for an icon/control that has no visible text. Appears on hover/focus.

**Rules:** Single line of text only. Never contain interactive elements.

### Popover (`pie-popover`)
**Use when:** Richer contextual content — multiple lines, interactive elements, or a small form

**Don't use when:** A single short hint is enough — tooltip is lighter-weight
