# Safe changes

How to restructure without changing what the code does, and how to know that you didn't.

## Contents

- [Pin behavior first](#pin-behavior-first)
- [The loop](#the-loop)
- [Step sequences](#step-sequences)
- [When a step goes red](#when-a-step-goes-red)
- [Commits](#commits)
- [Comments](#comments)
- [Tests](#tests)
- [Optional passes](#optional-passes)

## Pin behavior first

Before moving code, name the check that would fail if you broke it. Prove it by breaking the code on purpose: change a condition or a return value in the area, run the check, see it fail, undo. This takes a minute and it is the only evidence that the net exists.

When nothing fails, write characterization tests: tests that record what the code does now, right or wrong.

1. Call the area through the outermost entry point you can reach (the HTTP handler, the CLI command, the public function), not through the internals you are about to move.
2. Feed it inputs that cover each branch you will touch. Take real ones from fixtures, logs or existing callers where you can.
3. Assert on what comes out: return values, written rows, emitted events, rendered output. Write the expected values as literals copied from an actual run.
4. If the output looks wrong, keep the assertion as it is and add an ASK entry. The test records behavior; it does not approve it.
5. Break the code again and confirm the new test fails.

Commit these tests on their own, before the change they protect. If the area can't be called from a test without restructuring it first (a hidden input, a hard-wired network call), make the smallest change that opens it, such as adding one parameter with the old value as its default, and verify that one change by reading the diff. When even that isn't possible, the area stays report-only.

## The loop

For every step:

1. State the step in one sentence: "move `overlaps()` to `calendar/slots.py` and update its three importers".
2. Make only that change.
3. Run the fast checks: the type checker and the tests for the touched area.
4. Green: continue or commit. Red: see [below](#when-a-step-goes-red).

Run the full baseline before each commit (once per group when it takes longer than five minutes), and compare the result with the baseline from step 2 of the workflow, including the pre-existing failures: the same tests should fail for the same reason.

Let tools do the mechanical parts. A language server's rename and move update every reference; a codemod (jscodeshift, ast-grep, a `sed` over a reviewed list) applies one edit to many sites the same way. After any automated edit, grep for the old name: strings, config files, templates and docs are where the tool doesn't look.

## Step sequences

Each sequence keeps the checks green at every step, so it can stop at any point and still leave a working tree.

**Move a function or file.** Move it and leave a re-export at the old path. Update the importers. Remove the re-export. For a handful of importers, do it in one step.

**Change an interface that has many callers** (expand, migrate, contract). Add the new form next to the old one and have the old one call it. Move callers over, in batches if there are many. Delete the old form when grep finds no caller. Never change a signature and its callers' meaning in one edit.

**Replace a component** (two implementations behind one seam). Put an interface in front of the existing implementation without changing it. Build the new one behind the same interface. Run the same tests against both. Switch, then delete the old one. Use this only when the replacement can't be reached by smaller edits.

**Merge duplicates.** Diff the copies first. Write down each difference and decide whether it is an accident or a rule: `git log -S` on the differing text shows whether someone introduced it on purpose. Accidental differences are an ASK when they change output. Then make one copy the definition, point the others at it one at a time, and run the checks after each.

**Remove a hidden input.** Add a parameter that defaults to the current global read. Pass it explicitly from each caller, starting from the outermost. Remove the default, then the global.

**Introduce a missing concept** (the fix for a group of workarounds). Add the new type or function and its tests, unused. Route one path through it and delete the workaround that path needed. Repeat per path. The last commit deletes what nothing uses any more.

**Break a cycle.** Find the smaller of the two edges. Move the thing it reaches for into a module both sides can import, or pass it in from the side that owns it.

**Delete dead code.** Confirm no reference, including strings, reflection, config, templates, scripts and other repos that consume this one if it is published. Delete. Run the full baseline and the build.

When a target needs a prerequisite that needs another, work the chain from the far end: try the change, note what breaks, revert, fix the leaf prerequisite first, and commit it. Repeat until the original change goes through cleanly.

## When a step goes red

1. Read the failure. If the test was asserting on internals (a mock's call order, a private name), it is a Q5 finding: fix the test in its own commit, then redo the step.
2. If behavior changed, the step was wrong. Revert it instead of adding a fix on top. Try a smaller step.
3. If the same step fails twice, stop that group: undo your own changes since the last green commit, by file (`git restore <path>`) or with `git revert` for your commits, record what blocked it, and mark it ASK or LEAVE with the reason. Never reset the whole tree: the user's uncommitted changes may be in it.
4. Never make a check pass by weakening it: no skipped tests, loosened assertions, widened types or added ignores.

## Commits

- One cause, or one single FIX, per commit. A reviewer should be able to confirm "no behavior change" by reading it once.
- Keep moves and edits apart: a commit that moves a file changes nothing inside it, so the diff shows as a rename.
- Tests that pin behavior go in before the change they protect.
- Subject in the imperative, naming the structural change and the reason: "Route reminders through appointment transitions so cancel no longer races the sender".
- No commit leaves the tree red.

## Comments

Nothing checks a comment, so comments fail question 3 more easily than code does. For each comment in a file you are already changing, ask who could confirm it:

| Who can confirm the comment | Do |
|---|---|
| Anyone reading the lines below it | Delete it. If the lines were unclear without it, rename or extract until they aren't. |
| Only someone who knows a fact from outside the repo (a vendor limit, a legal rule, a browser bug, an incident) | Keep it, add the link or date if it lacks one, and check the fact when you can |
| Someone who knows another part of this repo (it explains a workaround) | Keep it while the workaround stands; the commit that removes the cause removes both |
| Nobody: it disagrees with the code | Find which is right with `git log -L`. If the code is right, fix the comment. If the comment is right, the code has a bug: make the comment describe what the code does today and add the bug to the ledger as ASK |
| Nobody: it is commented-out code | Delete it |
| A user of the public interface (docstrings that feed generated docs or editor hints) | Keep it; update it when the signature changes |

Don't sweep the repo for comments. Touch them where you are already working, unless the user chose the comment pass (see [Optional passes](#optional-passes)).

## Tests

Tests are the safety net for everything above, so they never change in the commit that changes the code they cover. Two kinds of test work happen in place, each in its own commit: pinning behavior before a step, and rewriting a test that blocks a step because it watches internals. Everything else here is the tests pass, which runs last.

Run two experiments on a test before judging it. Break the behavior it claims to cover: it should go red. Restructure the code without changing behavior: it should stay green.

| Result | Do |
|---|---|
| Green when the behavior is broken | It asserts nothing useful. Rewrite it to assert an outcome when the behavior matters; delete it when another test already covers that behavior. |
| Red after a behavior-preserving restructure | It watches internals. Rewrite it against the public entry point before the refactor that would break it, then repeat the first experiment. |
| Its expected value is computed with the code's own formula | Both sides move together, so it passes whatever the formula is. Replace the computation with literal examples. |
| Same inputs and assertions as another test | Keep the one closer to the public entry point. |
| Skipped | Find out why from `git blame`. Re-enable it if it passes or once the cause is fixed; delete it if the behavior no longer exists; otherwise leave it and report it. |
| Slow or flaky | Report it. Slowness is no reason to delete a test. |

Deleting a test needs the same proof as deleting code: say in the commit message which other test covers the behavior, or that the behavior is gone. Report the test count before and after, with the reason for each removal.

## Optional passes

The user picks these in step 1. Each runs after all structural work, one commit per pass (per fix for bug fixes), and gets its own section in the report.

**Comments.** Apply the table in [Comments](#comments) to every comment in scope, not only the ones near changed code. Leave docstrings on public interfaces and comments that state an outside fact. Report how many comments were removed, and list any comment that contradicted the code with what you did about it.

**Bug fixes.** Take the bugs from the ledger's ASK entries one at a time, smallest first. For each:
1. Write a test that reproduces it and fails. If the bug can't be reproduced in a test, leave it as ASK.
2. Make the smallest change that turns that test green, without touching anything the structural commits already settled.
3. Run the full baseline. A pinned test that recorded this bug's wrong output on purpose is updated in the same commit, and the commit message says so. Any other test that changes result means the fix changes more than the bug: revert it and leave it as ASK.
4. Commit it alone, with a subject that starts with "Fix" and names the observable change.

Leave as ASK a fix that would rewrite stored data or break a published API's signature; those need a migration, not a fix. When a fix changes something another program reads (CLI output, a file format, an HTTP response), make it, and mark it in the report so the user checks those consumers before merging; the separate commit keeps it easy to drop. Say in the report which bugs were fixed, what each now does differently, and which were left and why.

**Tests.** Apply the two experiments in [Tests](#tests) to every test in scope, not only those near changed code. In a suite of more than about 200 tests, limit it to the tests of files you changed and of the top fifth by hotspot score, and say so in the report. Remove a test only with the proof that section asks for. Report the test count before and after, with one line per removed or rewritten test.
