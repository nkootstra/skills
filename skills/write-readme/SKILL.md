---
name: write-readme
description: Write or update a project's README from what the repository actually contains, so a newcomer can get from clone to a working setup without asking anyone. Use whenever the user asks to write, generate, update, fix or restructure a README; to document a repo, its setup, its scripts or how to run it locally; says the README or setup docs are outdated or that a new contributor couldn't get the project running; or renamed scripts, env vars or packages and the docs need to follow. Works for apps and services, libraries, CLIs, monorepos, plugin or skills repos and infrastructure code, in any language.
argument-hint: "[path to the project, if not the current repo]"
metadata:
  author: Niels Kootstra
  version: "1.0.0"
---

# Write README

A README has one job above the others: take a reader who has never seen the project from clone to a running or used project, without asking anyone. Everything else in it earns its place by helping that reader understand or change the project. Length follows from the project, never from a target.

Two rules govern everything below:

- **Document only what the repo shows.** Every command, env var, port, service, deploy target, badge and version comes from a file you read. Never recommend a tool or platform the project doesn't use. When something the reader needs is unknown, write a visible `TODO:` and list it in your report instead of guessing.
- **Link to the source of truth instead of copying it.** A README that duplicates a schema, a full env list or an API reference is wrong by the next commit. Summarize and link.

## Reference files

- When identifying what kind of project this is and where each fact comes from, load [project-types.md](references/project-types.md).
- When choosing and writing sections, load [sections.md](references/sections.md).
- Before reporting back, load [verification.md](references/verification.md) and run its checks.

## 1. Read the repo

Collect facts before writing a line. Read the manifests and lockfiles, scripts (`package.json` scripts, `Makefile`, `justfile`, `bin/`, task runners), CI workflows, `.env.example` and the env reads in the code, deploy config, existing docs and `CONTRIBUTING`, and the license. CI is the most reliable record of how the project is really installed, tested and built; prefer it over memory of how such projects usually work.

Ask the user only when a gap blocks the README's main purpose, such as what the project is for when neither code nor docs say. Otherwise proceed and report the gaps.

## 2. Decide: new README or update

If a README exists, update it rather than regenerate it:

- Keep what is still accurate, along with its voice, badges, section order and any content you can't verify but have no reason to doubt.
- Fix what is stale: renamed scripts, moved files, changed versions, removed env vars, dead links.
- Add what a newcomer is missing.

Report the changes in a few lines afterwards. A rewrite nobody asked for loses context the author put there on purpose.

## 3. Choose sections

Pick the sections the project type needs (project-types.md) and the repo can support with facts (sections.md). Leave a section out when there is nothing true to put in it; an empty Deployment or Troubleshooting section is worse than none. Add a table of contents when the README runs past about 200 lines.

## 4. Write

- Open with what the project is and who it is for, in two or three sentences. No marketing adjectives: say what it does instead of calling it powerful or seamless.
- Use plain words and one name per thing: if the CLI is `acme`, don't also call it "the tool" and "the binary". Write headings in sentence case and keep bold for the rare warning, not decoration.
- Assume a fresh machine. State prerequisites with versions taken from the repo.
- Make every command copy-pasteable, in a fenced block with a language hint, using the package manager the lockfile shows. Say what a command does when that isn't obvious, and show expected output when it helps the reader confirm success.
- Use tables for reference material: env vars, scripts, options.
- Keep explanation proportional: a library needs a usage example more than an architecture section; a service with several moving parts needs a short map of how they connect, drawn from code you traced.

## 5. Verify and report

Treat every command in the README as a test: run it, or trace it to the script, target or binary that defines it. A command that does neither comes out. Run the checks in verification.md. Then end your reply with a report of a few lines: what you wrote or changed (for an update, the stale items you fixed), which commands you ran and whether they passed, and every `TODO:` with what resolves it. Mention problems in the repo itself only when they block the README's instructions. Write to `README.md` at the project root unless the user named another path; put longer material in `docs/` only when the user asks for it.

## Companion skills

- **write-prose**: hand off when a section is long explanatory prose (a design rationale, a migration story, an architecture essay) whose argument matters more than its commands.
