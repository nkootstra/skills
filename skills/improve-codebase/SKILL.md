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

- **Behavior stays the same.** Structure changes and behavior changes never share a commit. A change that alters behavior, a public interface, a stored data shape or a dependency is the user's decision: it goes in the report, and the run continues without it.
- **Evidence ranks the work.** Code that is ugly but never changes costs nothing. Rank by how often an area changes and how many places a change touches, measured from git, before judging by taste.
- **Every step is proven.** Run the checks after each step. A step that turns a check red is fixed or reverted before the next one starts.

## Reference files

- When mapping the codebase and collecting git evidence, load [mapping.md](references/mapping.md) for the commands.
- When looking for problems, load [problem-catalog.md](references/problem-catalog.md): the five questions, what each finding looks like, and how to confirm it.
- When writing findings, choosing dispositions, grouping them under a cause, or writing the final report, load [ledger.md](references/ledger.md).
- Before changing code, load [safe-changes.md](references/safe-changes.md): pinning behavior, step sequences for moves and interface changes, and the rules for comments and tests.

## 1. Set the mode and the limits

Pick the mode from the request. **Audit**: the user asked to assess, audit, review or say what to fix first; produce the ledger and the ranked plan, then stop, changing nothing. **Improve**: anything else; carry the work through to the stop rule in step 7 without pausing for approval between steps.

If the user named an area or concern, that is the scope; otherwise it is the whole repo. Then check the ground: work on a branch, treat uncommitted changes as the user's and leave them alone, and never push, merge or rewrite history unless asked.

## 2. Record a baseline

Find how the project checks itself (CI config first, then scripts and manifests) and run it: tests, type check, lint, build. Write down the commands, the results and how long they take. Failures that exist before you start are recorded as pre-existing, not fixed in passing and not blamed on your changes later. For each area in scope, note whether a check would catch a break there. An area with none is **report-only** until you pin its current behavior with tests (safe-changes.md). Never restructure code nothing checks.

## 3. Map the codebase

Read mapping.md first. Build a picture small enough to reason about whole: a skeleton of files and signatures without bodies, the dependency edges between modules, and from git the files that change most and the files that change together. For a large repo, have subagents summarize one area each and return its public surface, what it depends on and anything odd. The churn list decides where to read closely. Start with the files in the top fifth by commits over the last 12 months.

## 4. Fill the ledger

Read problem-catalog.md first: it has the confirm step for every kind of finding. Then go through the code with its five questions and write down every place the code gives a bad answer. Change nothing yet.

1. **Where does a change land?** One place, or several that must be found by memory.
2. **What does this lean on?** Dependencies you can see and that change less often than it does, or hidden inputs and volatile details.
3. **Can the reader trust it?** Names, types and comments that match what the code does, and one way to do each thing.
4. **Does each piece earn its place?** Every layer, option and file has a reason to exist today.
5. **Will a break be noticed?** A check fails when behavior changes, and only then.

Record **workarounds** too: code that serves one situation by stepping around the normal path (the catalog lists the kinds). Tag each with the situation it serves. A cluster of workarounds around one situation is what step 5 groups on, so don't plan their removal individually. Each entry gets a location (`path:line`), the question it fails, and the evidence as something that can be run again: a grep and its count, a commit count, a list of files that co-change. An entry without evidence is an opinion and stays out.

## 5. Decide, group and rank

Read ledger.md first. Give every entry one disposition:

- **FIX**: local and mechanical.
- **REDESIGN**: shares a cause with other entries, and one structural change resolves the group.
- **LEAVE**: nothing in the area changed in the window and nothing in the plan touches it, or the fix costs more than it saves. Write the reason.
- **ASK**: fixing it changes behavior, a public interface, a data shape or a dependency.

Before fixing anything, sort the entries by the requirement or piece of knowledge they concern. Several entries about one requirement usually mean the code has no concept for it: the fix is to add that concept once, and it rarely resembles any of the workarounds it replaces. Sketch the design you would pick today with the current requirements in hand, then put it through the same five questions. Rank the groups by how often their files change times how many entries they resolve, and put the ones that later work depends on first. Be willing to choose LEAVE for an area: old code is not a finding, and neither is code you would have written differently. LEAVE is not a way to skip an entry, though. A confirmed finding in a file the plan already changes, or in one that changed in the window, is FIX whenever the fix is mechanical; copies that differ in one value are one rule with a parameter. In audit mode, stop here and report.

## 6. Change in verified steps

Read safe-changes.md first. One cause per commit, in rank order. Before each step, confirm a check covers the code you are about to move; if none does, pin the behavior first. After each step run the fast checks, and run the full baseline before each commit. Keep each commit to something a reviewer can verify in one read: a move, a rename, an extraction, a deletion, a replaced interface. When a step turns out to need a behavior change, stop that group, mark it ASK, revert the partial work and continue with the next group. Delete what the redesign made unnecessary, workarounds included, in the same commit that makes them unnecessary.

## 7. Look again, stop, report

After each batch, close the loop in two ways. Rerun the evidence of every entry you marked done: if the grep still matches or the count has not dropped, the entry is still open. Then read the changed areas again as if for the first time, or hand them to a subagent that has not seen the ledger, and add what turns up. Do at most three such passes. Stop when a pass adds no FIX or REDESIGN entry in the top half of files by churn, or when every remaining entry is LEAVE or ASK. Every FIX and REDESIGN entry must end done, or moved to LEAVE or ASK with a reason; none stays open without a word. Then run the full baseline once more and compare it with step 2.

Report with the template in ledger.md: what changed and why, the numbers before and after, every ASK with the decision it needs, what was left and why, and what you could not verify. Keep observed facts and judgment in separate sentences.

## Companion skills

This is the only skill in the engineering category so far, so there is nothing to hand off to. Bugs, features, upgrades and performance problems found on the way go in the report as ASK entries.
