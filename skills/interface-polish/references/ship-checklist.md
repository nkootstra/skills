# Ship Checklist

Run this before calling UI work done. Every item is a yes/no test you can perform. Walk it on the real device or browser at the real size, not just in a design tool or the hero screen.

## Baseline

- [ ] Navigation follows the platform convention (tab bar / navigation bar / sidebar) and system back works everywhere.
- [ ] Type uses the platform scale or a deliberate scale; body text is 16px+ on mobile web, 17pt Dynamic Type on iOS, sp-based on Android.
- [ ] All interactive targets are at least 44pt (iOS), 48dp (Android), 24px minimum / 44px preferred (web).
- [ ] Sheets and modals use platform-appropriate primitives with standard dismissal (swipe down, Escape, overlay click).
- [ ] Dark mode is supported and checked on every screen, including native controls and scrollbars, with no flash of the wrong theme.
- [ ] Safe areas are respected: no content under notches, home indicator or system bars.
- [ ] Secondary screens (settings, errors, empty pages) meet the same bar as the hero screen.

## States

- [ ] Every button has hover, pressed, focus-visible, disabled and (for async) loading states.
- [ ] Every input has focus, filled, error and disabled states; labels are always visible.
- [ ] Every data view has designed loading, empty, error and partial states.
- [ ] "Empty because new" and "empty because filtered" are different states with different actions.
- [ ] Loading indicators are delayed ~300ms and don't flash for fast responses.
- [ ] Skeletons match the final layout; content arriving causes no layout shift.
- [ ] Success is confirmed proportionally (inline change or toast, not a modal).
- [ ] First-run experience is designed: a brand-new account doesn't look broken.

## Edges

- [ ] Works at 320px wide with no horizontal page scroll.
- [ ] Holds together at 2560px+: content has a max width.
- [ ] Usable on Slow 3G throttling: feedback appears, nothing looks frozen.
- [ ] Offline shows a clear message and recovers when the connection returns.
- [ ] Double-clicking submit sends one request.
- [ ] A 200-character name, a 40-character unbroken string and a 12-digit number don't break any layout.
- [ ] Zero, one and 1000+ items all render correctly, with singular/plural grammar right.
- [ ] Pseudo-localized text (+30% length) and RTL don't break layout.
- [ ] Denied permissions explain what's missing and how to grant it.
- [ ] Dates, times, numbers and currency are correct in another timezone and locale.
- [ ] Session expiry mid-task doesn't lose work.

## Recovery

- [ ] Every error message states what happened, why (if useful) and what to do next.
- [ ] No error shows only a code, stack trace or "Something went wrong".
- [ ] User input survives every error.
- [ ] Failed requests offer retry in place.
- [ ] Destructive actions offer undo or a confirmation proportional to the cost.
- [ ] Nothing requires contacting support that could reasonably be self-serve.

## Motion

- [ ] Every animation passes the purpose test (communicate, feel physical or delight).
- [ ] Popovers, menus and tooltips animate from their trigger (`transform-origin` set).
- [ ] Actions performed 100+ times a day have no or near-instant motion.
- [ ] UI animations are under 300ms unless large-distance or rare.
- [ ] Entrances use ease-out or springs; nothing enters with ease-in.
- [ ] Exits are faster than entrances.
- [ ] Every animation can be interrupted mid-flight without jumping.
- [ ] Drags track the finger 1:1 and rubber-band at their bounds.
- [ ] Nothing scales from 0.
- [ ] Stagger is limited to small groups and under ~300ms total.

## Accessibility

- [ ] Every flow can be completed keyboard-only, with visible focus at every step and no focus traps.
- [ ] Focus moves into dialogs on open and returns to the trigger on close.
- [ ] Every control has an accessible name; icon-only buttons are labelled.
- [ ] Screen reader (VoiceOver / TalkBack / NVDA) announces state changes, errors and toasts.
- [ ] Text contrast is 4.5:1 (3:1 for large text and UI components and focus rings).
- [ ] Color is never the only carrier of meaning.
- [ ] Page works at 200% zoom and largest Dynamic Type / font scale without clipping.
- [ ] Reduced motion replaces movement with fades and keeps all feedback.
- [ ] Headings form a logical outline; landmarks are present on web.

## Performance feel

- [ ] Pressing anything gives visible feedback within 100ms.
- [ ] Low-risk actions update optimistically and roll back clearly on failure.
- [ ] Refreshing data keeps existing content visible.
- [ ] Animations hold 60fps on a mid-range device with 4x CPU throttling.
- [ ] Only `transform` and `opacity` are animated in hot paths.
- [ ] Images reserve their dimensions; CLS under 0.1.
- [ ] Back navigation restores scroll position and state.
- [ ] Likely next screens are prefetched on hover or intent where cheap.

## Care and signature detail

- [ ] There is at least one considered detail in an overlooked place (empty state, 404, confirmation, onboarding copy).
- [ ] Copy reads as written by a person: specific, plain, consistent in tone.
- [ ] Icons, radii, spacing and shadows are consistent across screens.
- [ ] The known-broken thing nobody fixed has been fixed or consciously deferred.
- [ ] At least one interaction goes further than the platform's built-in equivalent.

## Subtraction

- [ ] Every element on each screen has a reason to exist; anything decorative without purpose is gone.
- [ ] No animation that fails the purpose test remains.
- [ ] No duplicate actions competing for the same job.
- [ ] Confirmations that could be undo instead have been replaced.
- [ ] Settings that only exist to avoid a decision have been decided.
- [ ] The screen still works and reads clearly with one more thing removed; if so, remove it.
