# The ledger

The ledger is the working record: every finding, what was decided about it and what happened. It survives context compaction and it becomes the report. Keep it in a scratch file outside the repo, or in the PR description; don't commit it unless the user asks.

## Contents

- [Entry format](#entry-format)
- [Dispositions](#dispositions)
- [Closing an entry](#closing-an-entry)
- [Grouping under a cause](#grouping-under-a-cause)
- [Ranking](#ranking)
- [Worked example](#worked-example)
- [Report template](#report-template)

## Entry format

One line per finding:

```md
- [Q2] `billing/export.py:88` reads `settings.CURRENT_TENANT`, set by the request middleware. Evidence: 3 tests patch the global; `export.py` and `middleware.py` co-change in 6 of 9 commits with no import between them.
```

- **Tag**: the question it fails (`Q1` to `Q5`), or `W` for a workaround.
- **Location**: `path:line`. For something spread out, the worst site plus a count ("and 11 more, `git grep -n 'status =='`").
- **What**: one sentence in terms of the code, with no verdict words ("messy", "bad", "smelly").
- **Evidence**: a number or a command result someone else can reproduce.

## Dispositions

| Disposition | Use when | Then |
|---|---|---|
| **FIX** | The change is local, mechanical and covered by a check | Do it in rank order |
| **REDESIGN** | The entry shares a cause with others | Move it under the cause it belongs to; the cause gets the rank |
| **LEAVE** | The area has no commits in the window, nothing that changes depends on it and nothing in the plan touches it; or the fix touches more than it saves; or it is a real exception | Write the reason in five words or so. An unexplained LEAVE reads as an oversight. |
| **ASK** | The fix changes observable behavior, a public or published interface, a stored data shape, a wire format, or adds, removes or upgrades a dependency | Write the decision the user has to make and what each answer costs. Carry on with the rest. |

Tests for the boundary cases:

- A bug found on the way is ASK, not FIX, even when the correct behavior looks obvious. Someone may depend on the current behavior. Put the reproduction in the report: the input, what happens, and what you expected.
- Exported symbols of a library, HTTP routes, CLI flags, database columns, event names and config keys are public. Inside an application, a module's exports are internal as long as every caller is in the repo: check with grep before treating one as free to change.
- Deleting code is FIX only when the confirm step in the problem catalog found no reference, including dynamic ones. Otherwise ASK.
- When choosing between FIX and LEAVE on thin evidence about an area you have no other reason to open, LEAVE. A wrong LEAVE costs nothing new; a wrong FIX costs a review and a risk.
- That does not apply inside files the plan already changes. There the review and the risk are already being paid, so a confirmed finding with a mechanical fix is FIX. "These lines themselves rarely change" is not a reason to keep three copies of a rule in three files you are editing anyway.
- Copies that differ on purpose are still copies. When the difference is a value (a divisor, a rate, a limit), the rule is one function and the value is its parameter: FIX. When the steps themselves differ, they are different rules: LEAVE, and say which step differs.

## Grouping under a cause

After the first pass, sort entries by the requirement or the piece of knowledge they concern, not by file or by question. Signs that entries share a cause:

- They mention the same value, field or concept ("status", "tenant", "the current locale").
- Their files co-change.
- Fixing one alone would make another worse, or would have to be redone when the other is fixed.
- They are workarounds for the same situation.

Name the cause as a missing or misplaced thing: "no single owner for X", "the state of Y isn't modeled", "Z is decided in three layers". Then write the fix as the design you would pick today, with the current requirements in hand. Test the candidate fix before adopting it:

1. Does each entry under it go away, or does one need its own workaround afterwards? An entry that still needs one belongs to another cause.
2. Does it introduce a new shape from the catalog (a pass-through layer, an option nobody sets, an interface with one implementation)?
3. Can it be reached in steps that each keep the checks green (safe-changes.md)? If not, shrink it.

Entries with no shared cause stay as single FIX items.

## Closing an entry

An entry is done when its evidence no longer reproduces, not when the commit that was meant to fix it has landed. After each batch, rerun the command or count recorded in the entry and write the new number next to the old one (`14 sites -> 0`). If the number has not moved, the entry is open: finish it, or change its disposition and write why. At the end no FIX or REDESIGN entry is left without one of the two.

## Ranking

Score each group: **commits to its files in the window × entries it resolves**. Then adjust:

- Move a group up when a later group's fix depends on it.
- Move a group down one place when no check covers its files; pinning behavior comes first and is part of its cost.
- Among equals, the smaller change goes first.

Number the groups in the order they will be done, and write the score and any adjustment next to each, so the order can be questioned.

## Worked example

A clinic booking service. The first pass, in the order found:

```md
- [W]  `reminders/send.py:41` loads the appointment again just before sending and drops the reminder if `cancelled_at` is set, because the queue can still hold reminders for cancelled appointments. Evidence: comment at :40; 1 site.
- [Q1] `api/appointments.py:77`, `reminders/send.py:52` and `billing/invoice.py:30` each decide whether an appointment is still active with their own combination of `cancelled_at`, `no_show` and `rescheduled_to`. Evidence: 3 sites, 3 different expressions; the three files co-change in 7 of 11 commits.
- [Q3] `models/appointment.py:12` has `status: str`; the values in use are "booked", "confirmed", "cancelled", "done" and, in `billing/invoice.py:33`, "canceled". Evidence: `git grep -n "status =="`, 14 sites.
- [W]  `billing/invoice.py:58` skips invoicing when `appointment.id in LEGACY_FREE_IDS`. Evidence: 1 site; the list last changed 26 months ago.
- [Q2] `calendar/slots.py:19` reads the clinic's time zone from `os.environ["CLINIC_TZ"]`; `api/appointments.py:25` and `reminders/schedule.py:14` convert times with their own offset arithmetic. Evidence: 3 sites; 4 fix commits in 12 months mention "timezone" or "DST".
- [Q5] `tests/test_reminders.py:60` asserts that `send_sms` was called once and nothing about the message or the recipient. Evidence: returning early from `build_message` leaves it green.
- [Q4] `calendar/providers/base.py` defines `CalendarProvider` with one implementation and no test double. Evidence: 1 class implements it; 0 commits in 18 months.
- [W]  `api/appointments.py:102` deletes the old reminder row and inserts a new one by hand when rescheduling; `reminders/schedule.py` has no function for either. Evidence: 1 site, raw SQL; added in the commit "fix duplicate reminder after reschedule".
- [Q1] The reschedule flow updates the appointment in `api/appointments.py:95`, then repeats the overlap check from `calendar/slots.py:40` inline. Evidence: two copies, one missing the buffer-minutes rule.
- [Q3] `reminders/schedule.py:31` is named `get_due` and also marks reminders as sent. Evidence: body, lines 31 to 58.
```

Grouped, with dispositions and rank:

```md
1. FIX — `tests/test_reminders.py:60` asserts the recipient and the message text. Score 6 commits × 1 entry; moved to the top because group 2 relies on this test.

2. REDESIGN — Model the appointment's lifecycle in one place: a `Status` enum and a `transition()` function that owns which moves are legal and what each one triggers. Score 23 commits × 5 entries.
   - [Q3] `status: str` with five spellings in use, 14 comparison sites.
   - [Q1] Three files each decide "still active" their own way.
   - [W]  The sender's second look at `cancelled_at`: a cancel becomes a transition that removes the pending reminder, so the queue never holds one for a cancelled appointment.
   - [W]  Reminder rows deleted and inserted by hand in the API: a reschedule becomes a transition that replaces the reminder.
   - [Q3] `get_due` that also marks as sent: split once sending is driven by transitions.
   ASK inside this group: `billing/invoice.py:33` compares against "canceled", which never matches, so cancelled appointments are invoiced today. Keeping that is behavior; fixing it changes invoices. Reported, not changed.

3. FIX — Give time one owner: a `ClinicTime` value created at the boundary from the clinic record, and no offset arithmetic elsewhere. Score 9 commits × 1 entry.
   - [Q2] Time zone read from the environment in one place and recomputed in two others.

4. FIX — Reschedule calls `slots.overlaps()` and loses its inline copy. Score 8 commits × 1 entry.
   ASK: the inline copy omits the buffer-minutes rule, so rescheduling currently allows back-to-back bookings that a new booking refuses. Calling the shared check changes that.

LEAVE — `CalendarProvider` with one implementation: no commits in 18 months, nothing in the plan touches it.
LEAVE — `LEGACY_FREE_IDS`: a real exception for a fixed set of old records. Add a comment naming the agreement it comes from.
```

Two things to copy from this: item 1 has the lowest score and still goes first because another item depends on it, and both ASK notes sit inside the group that surfaced them so the reader sees them in context.

## Report template

```md
## What this was
Scope, mode (audit or improve), branch, and the five-line map.

## What changed
One line per commit, in order: the cause it addressed and the entries it closed.

## Numbers
| | Before | After |
|---|---|---|
| Tests | 212 pass, 3 pre-existing failures | 219 pass, same 3 failures |
| Type check / lint / build | pass / 14 warnings / pass | pass / 9 warnings / pass |
| Sites comparing `status` | 14 | 2 |
| Edges against the intended direction | 6 | 1 |
| Files a status change touches | 5 | 1 |

Report only numbers you measured. Leave a cell out when you have no measurement for it.

## Decisions for you
Each ASK: what was found, the options, what each costs, and where the evidence is.

## Left as is
Each LEAVE with its reason.

## Not verified
Areas with no checks, commands that could not be run, behavior confirmed only by reading.
```

In audit mode, replace "What changed" with the ranked plan and drop the After column.

Keep facts and judgment apart. "`export.py` reads a global that three tests patch" is a fact. "This makes export hard to test" is a judgment; say it in its own sentence, after the fact it rests on.
