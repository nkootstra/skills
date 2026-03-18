# Product Verification Template

Use this template when building a skill that tests or verifies code is working correctly. These skills pair with external tools (Playwright, tmux, headless browsers) to confirm behavior programmatically rather than relying on manual inspection.

## How to Customize

Replace everything in `[brackets]` with the user's specifics. Delete sections that don't apply.

---

## Template SKILL.md

```markdown
---
name: [name]-verifier
description: Verifies [what it tests] by [how it tests]. Use when user asks to "test the [feature]", "verify [flow] is working", "check [behavior]", "run the [feature] test", or mentions [specific testing scenarios]. Also trigger for "does this actually work", "prove it works", or any request to validate [feature] behavior end-to-end.
---

# [Feature/Flow] Verifier

## Purpose

Verifies that [feature/flow] works correctly by driving it end-to-end and asserting state at each step. This is not a unit test — it's a full integration check that confirms real user-facing behavior.

## Prerequisites

- [Tool 1, e.g., "Playwright installed (`npm install playwright`)"]
- [Tool 2, e.g., "Test environment running (`turbo dev`)"]
- [Credentials/config, e.g., "Stripe test keys in `.env.test`"]

## Verification Flow

### Step 1: Setup
[What to set up before the test — clean state, test data, environment]
- [e.g., "Reset test database to known state"]
- [e.g., "Create test user with known credentials"]

Assert: [What should be true after setup, e.g., "Test user exists in database, no prior session data"]

### Step 2: [First action, e.g., "Navigate to signup page"]
[What to do]

Assert: [What should be true, e.g., "Page loads without errors, form fields are present"]

### Step 3: [Next action, e.g., "Submit signup form"]
[What to do, including specific test data to use]

Assert: [What should be true, e.g., "Redirect to email verification page, user record created in database with status 'pending'"]

### Step 4: [Continue for each step...]
[...]

Assert: [...]

### Final Assertion
[The end-state check that proves the whole flow worked]
- [e.g., "User can log in with created credentials"]
- [e.g., "Dashboard shows correct initial state"]
- [e.g., "All expected database records exist with correct values"]

## Recording

[Optional: instructions for recording the test run for human review]
- [e.g., "Record the browser session as a video using Playwright's `recordVideo` option"]
- [e.g., "Save screenshots at each assertion point to `outputs/screenshots/`"]
- [e.g., "Save the video to `outputs/recording.webm`"]

## Failure Handling

When a step fails:
1. [e.g., "Capture a screenshot of the current state"]
2. [e.g., "Log the page HTML and console errors"]
3. [e.g., "Report which step failed, what was expected, and what was found"]
4. [e.g., "Do NOT continue to subsequent steps — the state is likely invalid"]

## Gotchas

- [e.g., "The email verification step has a 5-second delay — wait for it rather than polling"]
- [e.g., "Stripe test mode webhooks need the Stripe CLI listener running"]
- [e.g., "The test database must be reset between runs — leftover data causes false passes"]
```

---

## Customization Checklist

When filling in this template, make sure you've captured:

- [ ] Clear prerequisites (tools, environment, credentials)
- [ ] Every step in the flow with specific test data
- [ ] Assertions at each step (not just the final state)
- [ ] Recording instructions so a human can review what happened
- [ ] Failure handling (what to capture when something breaks)
- [ ] Gotchas (timing issues, external dependencies, state cleanup)
- [ ] Scripts in `scripts/` for any deterministic verification logic
