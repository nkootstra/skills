# Commits and PRs

A commit message or PR description is prose with one reader: someone deciding whether the change is right, now or years later in `git log`. The core rules still hold: open on the point, keep certainty where the evidence puts it, invent nothing. This file covers what is specific to the form. It is about the writing, not about running git or GitHub.

## Establish the change

Before writing, read the supplied diff, issue, task or PR context and identify:

- what changed
- why it changed
- who or what benefits
- constraints, tradeoffs or deliberate exclusions
- validation that actually ran

If the reason or the evidence is missing, say so or ask for it. Never infer a motivation, result, metric, test or user impact from filenames alone.

## Commit messages

Write a concise subject that states the meaningful change. Follow the repository's established style, and conventional commits when the repository uses them. Prefer an imperative verb and a specific scope, and leave out the implementation diary.

Add a body only when the subject cannot carry the reason, a tradeoff or important context. Keep it short. Do not list every changed file or claim validation that did not run.

## Pull request descriptions

Read and follow the repository's PR template when one exists. Keep its required headings, fields, order and checklists.

Lead with why the change matters and what is now different. Then include only the context a reviewer needs:

- outcome and user or maintainer impact
- important design decisions or tradeoffs
- scope and deliberate non-goals
- validation performed, including its limits
- follow-up work, only when it is known and relevant

Use the shortest structure that lets a reviewer understand the change and decide. Do not write a file inventory, restate the diff, narrate the implementation process or add marketing language.

## Output

Return the finished commit message or PR description first. If it needs context that is missing, name the exact gap instead of filling it with plausible prose. Add no tool, model or generator attribution lines unless the repository requires them. Do not commit, push, open, edit or merge anything unless the user separately asks for that operation.
