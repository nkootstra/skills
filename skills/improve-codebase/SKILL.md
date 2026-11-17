---
name: improve-codebase
description: Improve the structure of a codebase or module so changes get cheaper and safer. Finds what makes the code hard to change, ranks it with evidence from git history, and fixes it in small verified steps without changing behavior. Use whenever the user wants to clean up, restructure or pay down tech debt across a codebase, package or module; says the code is a mess, fragile, hard to change, or that every change touches many files; asks for a code quality or architecture audit, or what to refactor first; or wants a repo made easier for agents or new engineers to work in. Not for a single bug fix, a rename, a one-function refactor, lint or format fixes, dependency upgrades, performance work, new features or reviewing a diff.
argument-hint: "[area or concern to focus on, or 'audit' for a report only]"
effort: high
metadata:
  author: Niels Kootstra
  version: "1.0.0"
---

# Improve codebase

Quality here means one thing: **what the next change costs.** A codebase is in good shape when a typical change lands in one place, the reader can trust what they read, and a mistake shows up in a check instead of in production. Tidiness that doesn't lower that cost is not the goal, and neither is a style the code "should" follow.

Three rules govern everything below:
- **Behavior stays the same.** Structure changes and behavior changes never share a commit. A change that alters behavior, a public interface, a stored data shape or a dependency is the user's decision: it goes in the report, and the run continues without it. The one exception is the bug-fix pass, when the user chose it in step 1.
- **Evidence ranks the work.** Code that is ugly but never changes costs nothing. Rank by the hotspot score from mapping.md (commits in the last 12 months × lines) and by how many places a change touches, before judging by taste.
- **Every step is proven.** Run the checks after each step. A step that turns a check red is fixed or reverted before the next one starts.

## Reference files

- When mapping the codebase and collecting git evidence, load [mapping.md](references/mapping.md) for the commands.
- When looking for problems, load [problem-catalog.md](references/problem-catalog.md): the five questions, what each finding looks like, and how to confirm it.
- When writing findings, choosing dispositions, grouping them under a cause, or writing the final report, load [ledger.md](references/ledger.md). It holds the full definitions of the four dispositions.
- Before changing code, load [safe-changes.md](references/safe-changes.md): pinning behavior, step sequences for moves and interface changes, the rules for comments and tests, and how to run each optional pass.

## 1. Set the mode and the limits

Pick the mode from the request. **Audit**: the user asked to assess, audit, review or say what to fix first; produce the ledger and the ranked plan, then stop, changing nothing. **Improve**: anything else; carry the work through to the stop rule in step 7 without pausing for approval between steps.

If the user named an area or concern, that is the scope; otherwise it is the whole repo. Then check the ground: work on a new branch; if the working tree has uncommitted changes, they are the user's, so leave them alone, stage your own files by path and never use `git add -A`, `git reset --hard`, `git checkout .` or `git stash`. Never push, merge or rewrite history unless asked. Generated and vendored files (lockfiles, `vendor/`, generated clients, anything marked generated) are out of scope: change their source or generator, never the output.

In improve mode, ask once which optional passes to add, as one multi-select question with these descriptions:

- **Comments**: remove comments that restate the code or are commented-out code, and correct comments that contradict it.
- **Tests**: remove tests that can't catch a bug and rewrite tests tied to internals, after all other work.
- **Bug fixes**: fix the bugs found along the way, each in its own commit with a test that fails before the fix.

Run only the passes chosen. Don't ask in audit mode, when the request already names its passes (run those), or when the user said not to ask or is away. Without an answer, or without a question tool to ask with, run none and say so in the report.

## 2. Record a baseline

Find how the project checks itself (CI config first, then scripts and manifests) and run it: tests, type check, lint, build. Write down the commands, the results and how long they take. Failures that exist before you start are recorded as pre-existing, not fixed in passing and not blamed on your changes later. For each area in scope, note whether a check would catch a break there. An area with none is **report-only** until you pin its current behavior with tests (safe-changes.md); the smallest change that makes it testable is the one change allowed before that. If the project has no test runner at all, use the language's built-in one (`unittest`, `node --test`, `go test`); if there is none, adding one is an ASK and the run becomes an audit.

## 3. Map the codebase

Read mapping.md first. Build a picture small enough to reason about whole: a skeleton of files and signatures without bodies, the dependency edges between modules, and from git the files that change most and the files that change together. For a large repo, have subagents summarize one area each and return its public surface, what it depends on and anything odd. Read closely in hotspot order, starting with the top fifth.

## 4. Fill the ledger

Read problem-catalog.md first: it has the confirm step for every kind of finding. Then go through the code with its five questions and write down every place the code gives a bad answer. Change nothing yet.

1. **Where does a change land?** One place, or several that must be found by memory.
2. **What does this lean on?** Dependencies you can see and that change less often than it does, or hidden inputs and volatile details.
3. **Can the reader trust it?** Names, types and comments that match what the code does, and one way to do each thing.
4. **Does each piece earn its place?** Every layer, option and file has a reason to exist today.
5. **Will a break be noticed?** A check fails when behavior changes, and only then.

Record **workarounds** too: code that serves one situation by stepping around the normal path (the catalog lists the kinds). Tag each with the situation it serves; a cluster of them around one situation is what step 5 groups on. Each entry gets a location (`path:line`), the question it fails, and the evidence as something that can be run again: a grep and its count, a commit count, a list of files that co-change. An entry without evidence is an opinion and stays out.

## 5. Decide, group and rank

Read ledger.md first, and give every entry one disposition: **FIX**, **REDESIGN**, **LEAVE** or **ASK**. LEAVE is for an area nobody changes, never a way to skip a confirmed finding in a file the plan already touches.

Before fixing anything, sort the entries by the requirement or piece of knowledge they concern. Several entries about one requirement usually mean the code has no concept for it: the fix is to add that concept once, and it rarely resembles any of the workarounds it replaces. Sketch the design you would pick today with the current requirements in hand, then put it through the same five questions. Rank the groups by hotspot score times the entries they resolve, and put the ones that later work depends on first. Old code is not a finding, and neither is code you would have written differently. In audit mode, stop here and report.

## 6. Change in verified steps

Read safe-changes.md first. One cause per commit, in rank order. Before each step, confirm a check covers the code you are about to move; if none does, pin the behavior first. Run the fast checks after each step and the full baseline before each commit, or once per group when it takes longer than five minutes. Keep each commit to something a reviewer can verify in one read: a move, a rename, an extraction, a deletion, a replaced interface. When a step turns out to need a behavior change, stop that group, mark it ASK, undo your own uncommitted edits to its files and continue with the next group. Delete what the redesign made unnecessary, workarounds included, in the same commit that makes them unnecessary. The chosen optional passes come after all structural work, in this order: comments, bug fixes, tests.

## 7. Look again, stop, report

A batch is the commits for one group. After each batch, rerun the evidence of every entry you marked done: if the grep still matches or the count has not dropped, the entry is still open. Then read the changed areas again as if for the first time, or hand them to a subagent that has not seen the ledger, and add what turns up. Do this at most three times in a run. Stop when a fresh read adds no FIX or REDESIGN entry in the top half by hotspot score, or when every remaining entry is LEAVE or ASK. Every FIX and REDESIGN entry must end done, or moved to LEAVE or ASK with a reason. Then run the full baseline once more and compare it with step 2.

Report with the template in ledger.md: which optional passes ran, the result of every check after the last commit, what changed and why, the numbers before and after, every ASK with the decision it needs, what was left and why, and what you could not verify. Keep observed facts and judgment in separate sentences.

## Companion skills

This is the only skill in the engineering category so far, so there is nothing to hand off to.
