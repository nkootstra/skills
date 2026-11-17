# Skills

Agent skills by Niels Kootstra. They are written primarily for Claude Code and work with any agent that supports the [Agent Skills](https://agentskills.io) format.

Skills are grouped into plugins by category:
- **Design:** critiquing, exploring, prototyping and finishing interfaces.
- **Writing:** prose with an argument and a voice, commit messages and PR descriptions, and READMEs built from what the repo contains.
- **Engineering:** improving the structure of a codebase in small verified steps, ranked by evidence from git history.

Each skill is a short workflow plus reference files that the agent loads only when a step needs them. The skills trigger on their own when a request matches, and they can also be called by name.

## Key features

- **Grouped by category:** each category is its own Claude Code plugin in one marketplace, so you install only what you need: `design-skills`, `writing-skills` and `engineering-skills`.
- **Two ways to install:** with the skills CLI (`npx skills add`) for any compatible agent, or as Claude Code plugins.
- **Progressive loading:** each `SKILL.md` stays under 80 lines. Rubrics, checklists, catalogs, ranges and code live in each skill's `references/` folder, and each file has an explicit trigger saying when to load it.
- **Claude Code frontmatter:** `effort: high` on the skills that need deep reasoning, and `argument-hint` on the skills you call with a target.
- **Tested triggering:** an eval checks that each skill loads for the right prompts and stays out of adjacent ones.
- **Versioned:** semver per skill and per plugin, stamped by a release workflow; [GitHub Releases](https://github.com/nkootstra/skills/releases) is the changelog.

## Table of contents

- [Skills](#skills-1)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How the skills work](#how-the-skills-work)
- [Repository layout](#repository-layout)
- [Local development](#local-development)
- [Evals](#evals)
- [Versioning and releases](#versioning-and-releases)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Skills

### Design skills

Plugin: `design-skills`. Four skills, each covering a different stage of interface work.

| Skill | What it does | Use it when |
|---|---|---|
| [design-critique](skills/design-critique) | Turns "something feels off" into specific, named observations, scored against the product's own facets of quality. | You want feedback, a UX audit, a heuristic evaluation, or a comparison of two versions. |
| [design-exploration](skills/design-exploration) | Generates structurally different directions (range), then climbs the chosen one through deliberate levels of quality (depth). | You want options, a brainstorm, or a way out of a generic first idea. |
| [intentional-prototyping](skills/intentional-prototyping) | Builds prototypes that answer one question, with a live tuning panel for timing, easing, springs and surfaces. | You want to test an interaction, dial in values, compare variations, or recreate an effect you saw. |
| [interface-polish](skills/interface-polish) | Meets the platform baseline, then exceeds it through states, edges, recovery and purposeful motion. | You are building or finishing UI and quality matters: a launch, a demo, a portfolio piece. |

#### design-critique

The workflow:
1. Look in several passes before judging.
2. Set 3 to 6 **facets**, the qualities this product should be perceived to have, such as "calm and trustworthy" or "dense and expert-fast".
3. Render the screen before critiquing it.
4. Separate the platform floor from real craft.

Findings follow one formula: observation, impact, direction, each with a severity.

| Reference file | Loaded when |
|---|---|
| `rubric.md` | Running the detailed passes. Per-dimension checks, severity levels, a Nielsen heuristics sweep, and dark patterns, which always count as blockers. |
| `facets.md` | Drafting or sharpening facets, and before scoring them. |
| `output-template.md` | Writing the report, comparing versions, or rewriting vague feedback. |

`effort: high`. Argument hint: `[screen, file, or URL]`. If the project has a `.design/facets.md`, the skill reads it, and it offers to save confirmed facets there. Rejected patterns can be saved to `.design/rejections.md`.

#### design-exploration

**Range:** directions that differ in mechanism, not just styling. Two directions that differ only in looks get merged. **Depth:** the chosen direction climbs a 1-to-10 ladder, ending with a "what can go?" pass.

| Reference file | Loaded when |
|---|---|
| `range-techniques.md` | Before generating directions. Covers job-to-be-done framing, mechanism axes, the range-or-variant test, visual movements to borrow, the generic AI aesthetic to avoid, a prompt bank, a worked example and the presentation format. |
| `depth-ladder.md` | Once a direction is chosen. Covers level descriptions, moves per band, a levels log and ceiling signs. |

`effort: high`.

#### intentional-prototyping

The workflow:
1. Name the one falsifiable question the prototype must answer, and build the minimum that answers it: blank shapes, a spike, or Wizard of Oz.
2. Expose the important values as live controls.
3. To learn an effect, rebuild it step by step against the reference.

| Reference file | Loaded when |
|---|---|
| `tuning-panel.md` | Building the control panel. A dependency-free floating panel (`createTuner`), a variations grid (`renderVariations`) and a React hook (`useTuner`), meant to be copied verbatim. |
| `parameter-ranges.md` | Choosing defaults and slider ranges for durations, easing, springs, stagger, scale, shadows, blur, radius and opacity. |
| `recreation.md` | Recreating an effect. Covers an observation checklist, a technique decision table and a comparison log. |
| `react-prototypes.md` | The prototype lives in a React, TSX or Next.js codebase. |

Argument hint: `[interaction to prototype]`.

#### interface-polish

The workflow:
1. Start from the platform default.
2. Show care where others stop: states, edges, errors and recovery.
3. Use motion only where it proves care.
4. Render at 1440px and 390px wide and look at the result.
5. Check against a ship list before calling the work done.

| Reference file | Loaded when |
|---|---|
| `platform-baselines.md` | Before designing: the floor for iOS, Android, web apps and marketing sites. |
| `states-and-edges.md` | Walking every component through its state matrix and the edge sweep. |
| `motion.md` | Adding, reviewing or tuning animation. |
| `visual-rules.md` | Building or restyling a surface. Covers defaults to decide rather than inherit, surfaces, color, type, layout, actions, dark mode and a quick defect scan. |
| `ship-checklist.md` | Before calling UI work done. |
| `react-components.md` | Building or hardening a reusable React component. |

#### How the design skills hand off

Each skill ends with a "Companion skills" section, so the agent knows when to switch:

```
design-exploration ──► intentional-prototyping ──► design-critique ──► interface-polish
  "which direction?"     "does this feel right?"    "what's weak?"      "make it finished"
```

### Writing skills

Plugin: `writing-skills`. Two skills: one for prose, one for READMEs.

| Skill | What it does | Use it when |
|---|---|---|
| [write-prose](skills/write-prose) | Drafts and edits prose with a visible argument and a natural voice, without inventing evidence or overstating certainty. Also writes commit messages and PR descriptions. | You have notes to turn into a post, a draft that reads like AI wrote it, or a change that needs a commit message or PR description. |
| [write-readme](skills/write-readme) | Writes or updates a README from what the repo actually contains: real commands, real env vars, no invented deploy steps. | A repo has no README, an outdated one, or setup docs a newcomer can't follow. |

#### write-prose

The skill infers audience, purpose and length from the request, then matches the work to it: a light edit fixes the affected wording, while a draft starts from what the reader should understand. Before drafting it writes down the tests the piece must pass (the spine, a source for every fact and reason, an ending that adds something), then checks the draft against them. Core rules: open on the subject, give each paragraph one job, keep claims within the evidence, and end on the consequence the material supports.

| Reference file | Loaded when |
|---|---|
| `adaptation.md` | Choosing a structure for a genre, audience or length. |
| `style-system.md` | Fixing a voice, pacing, explanation or argument problem. |
| `residue-checks.md` | Cleaning up machine-drafted text: self-commentary, portable one-liners, unsupported closure, buried openings. |
| `explaining.md` | Explaining how something works or why it was built that way: introducing concepts, tracing a mechanism, numbers that explain, tradeoffs, and shapes for deep-dives, system-design explainers and incident write-ups. |
| `examples.md` | Calibrating a weak passage against stronger versions. |
| `commits-and-prs.md` | Writing a commit message or PR description. |

#### write-readme

The workflow:
1. Read the repo: manifests, lockfiles, scripts, CI, env reads, deploy config.
2. If a README exists, update it instead of regenerating it.
3. Choose sections for the project type, leaving out any the repo can't fill with facts.
4. Write for a newcomer on a fresh machine.
5. Verify commands, versions, env vars and links, then report the gaps as `TODO:` lines.

| Reference file | Loaded when |
|---|---|
| `project-types.md` | Identifying the project type (app, library, CLI, monorepo, plugin repo, infra) and where each fact comes from. |
| `sections.md` | Choosing and writing sections: when each belongs and what it must contain. |
| `verification.md` | Before reporting back. |

Argument hint: `[path to the project, if not the current repo]`.

### Engineering skills

Plugin: `engineering-skills`. One skill so far.

| Skill | What it does | Use it when |
|---|---|---|
| [improve-codebase](skills/improve-codebase) | Finds what makes a codebase hard to change, ranks it with evidence from git history, and fixes it in small verified steps without changing behavior. | The code is a mess, every change touches many files, you want to pay down tech debt, or you want an audit that says what to refactor first. |

#### improve-codebase

Quality is measured as what the next change costs. Structure changes and behavior changes never share a commit: anything that would alter behavior, a public interface, a data shape or a dependency is reported as a decision for you, and the run continues without it.

The workflow:
1. Set the mode: **audit** (a ledger and a ranked plan, no changes) or **improve** (carry the work through to a stop rule). In improve mode it asks once which optional passes to add: **comments** (remove comments that only restate the code), **tests** (remove tests that can't catch a bug, rewrite tests tied to internals) and **bug fixes** (each in its own commit, with a test that fails first). It skips the question when the request already says, when you're away, or in audit mode, and without an answer it runs none.
2. Record a baseline: tests, type check, lint, build. Areas no check covers are report-only until their behavior is pinned with tests.
3. Map the codebase: a skeleton, the dependency edges, and from git the files that change most and the files that change together.
4. Fill a ledger with five questions: where does a change land, what does this lean on, can the reader trust it, does each piece earn its place, will a break be noticed. Every entry needs evidence.
5. Give each entry a disposition (FIX, REDESIGN, LEAVE or ASK), group entries under a shared cause, and rank the groups by churn times entries resolved.
6. Change in verified steps, one cause per commit, running the checks after each step.
7. Look again with fresh eyes (three passes at most), stop when nothing ranked is left, and report with before-and-after numbers.

| Reference file | Loaded when |
|---|---|
| `mapping.md` | Mapping the codebase. Commands and three short scripts for size, a declaration skeleton, import edges and cycles, churn, hotspots and co-change. |
| `problem-catalog.md` | Looking for problems. Per question: the shapes a bad answer takes, how to confirm each one, the usual fix, and what is not a finding. |
| `ledger.md` | Writing findings, choosing dispositions, grouping under a cause, ranking, and writing the report. Includes a worked example. |
| `safe-changes.md` | Before changing code. Pinning behavior with characterization tests, step sequences that stay green (move, expand-migrate-contract, merge duplicates, break a cycle), and the rules for comments and tests. |

`effort: high`. Argument hint: `[area or concern to focus on, or 'audit' for a report only]`.

## Prerequisites

| For | You need |
|---|---|
| Installing with the skills CLI | Node.js with `npx` |
| Installing as a plugin | [Claude Code](https://claude.com/claude-code) |
| Running the evals | Claude Code (`claude plugin eval`) and Python 3.9 or newer; Node.js 20 or newer to score the improve-codebase cases |

## Installation

### With the skills CLI

The [skills CLI](https://skills.sh) installs skills into any supported agent:

```bash
npx skills add nkootstra/skills                          # pick from a list
npx skills add nkootstra/skills --skill design-critique  # one skill
npx skills add nkootstra/skills --all                    # everything
```

To update, run the same command again.

### As Claude Code plugins

Add the marketplace once, then install the plugins you want:

```
/plugin marketplace add nkootstra/skills
/plugin install design-skills@nkootstra-skills
/plugin install writing-skills@nkootstra-skills
/plugin install engineering-skills@nkootstra-skills
```

| Plugin | Skills |
|---|---|
| `design-skills` | design-critique, design-exploration, intentional-prototyping, interface-polish |
| `writing-skills` | write-prose, write-readme |
| `engineering-skills` | improve-codebase |

The marketplace is `nkootstra-skills`. Plugin skills are namespaced, for example `/design-skills:design-critique`.

To update or remove a plugin:

```
/plugin marketplace update nkootstra-skills
/plugin uninstall design-skills@nkootstra-skills
```

## Usage

You don't need to name a skill; describe the task and the matching skill loads. Some examples:

| You say | Skill that loads |
|---|---|
| "Something about our onboarding screen feels off. What's wrong with it?" | design-critique |
| "Do a heuristic evaluation of the signup form." | design-critique |
| "Give me a few genuinely different directions for the empty state." | design-exploration |
| "Brainstorm 10 concepts for a habit tracker's daily check-in." | design-exploration |
| "I want to dial in the spring on our drawer. Make something I can tweak live." | intentional-prototyping |
| "How did they do that menu animation? I want to recreate it." | intentional-prototyping |
| "We launch Monday. Make the dashboard feel finished: empty, loading, error states." | interface-polish |
| "Polish the settings page so it feels premium." | interface-polish |
| "Our about page reads like an AI wrote it. Rewrite it so it sounds like a person." | write-prose |
| "Write a commit message for the changes I just made." | write-prose |
| "Write a README for this repo." | write-readme |
| "A new hire spent a day getting this running. Fix the docs." | write-readme |
| "Every time we add a payment method we touch nine files. Sort out the structure." | improve-codebase |
| "Do a code quality audit and tell me what to refactor first." | improve-codebase |

Or call a skill directly, with a target:

```
/design-critique src/pages/Checkout.tsx
/intentional-prototyping card flip on tap
```

As a plugin, use the namespaced form: `/design-skills:design-critique src/pages/Checkout.tsx`.

The skills stay out of adjacent tasks: UI code that needs no design judgment (fixing a TypeError, renaming a prop, setting up Tailwind), writing they don't cover (ad copy, press releases, translations, summaries, docstrings), and code changes that aren't about structure across a codebase (a one-function refactor, a dependency upgrade, lint fixes, making one endpoint faster, reviewing a diff).

## How the skills work

A skill is a folder with a `SKILL.md`. The frontmatter tells the agent what the skill is for:

```yaml
---
name: design-critique
description: Structured, specific critique of interfaces ... Use whenever the user asks for feedback on a design ...
argument-hint: "[screen, file, or URL]"
effort: high
metadata:
  author: Niels Kootstra
  version: "1.0.0"
---
```

| Field | Purpose |
|---|---|
| `name` | Equals the folder name. |
| `description` | What the agent reads to decide whether to load the skill. It leads with what the skill does, then lists the situations and phrasings that should trigger it. |
| `argument-hint` | Claude Code: shown when calling the skill by name. |
| `effort` | Claude Code: the reasoning effort while the skill is active. |
| `metadata` | Author and version, used by the skills ecosystem. Values are strings. |

Loading happens in three stages:

1. **Always in context:** only the name and description of each installed skill.
2. **When a request matches:** the agent loads `SKILL.md`, the workflow.
3. **When a step needs it:** the agent loads a reference file. Each link in `SKILL.md` says when to load it, for example `Load [rubric.md](references/rubric.md) on the second and third passes.`

This keeps the cost of having the skills installed small, while the detail is there when needed.

## Repository layout

```
.
├── .claude-plugin/
│   └── marketplace.json        marketplace; one plugin entry per category, each listing its skills
├── skills/                     all skills, flat, whatever their category
│   ├── design-critique/
│   │   ├── SKILL.md            the workflow
│   │   └── references/         rubric.md, facets.md, output-template.md
│   ├── design-exploration/     SKILL.md, references/
│   ├── intentional-prototyping/
│   ├── interface-polish/
│   ├── write-prose/
│   ├── write-readme/
│   └── improve-codebase/
├── evals/
│   ├── triggering/
│   │   ├── make_cases.py       source of truth for the cases; writes cases.md and the case folders
│   │   ├── summarize.py        per-skill recall and precision from a results file
│   │   ├── cases.md            generated, readable table of all cases (committed)
│   │   └── <case-id>/          generated before a run: prompt.md + graders/ (gitignored)
│   ├── quality/
│   │   ├── make_cases.py       writes one case folder per case from the JSON files (gitignored)
│   │   ├── <skill>.json        cases: prompt, input or fixture repo, expectations
│   │   ├── inputs/             drafts the writing cases start from
│   │   ├── fixtures/<name>.json  one repo per file, with its commit history and recorded outputs
│   │   ├── fixture_repo.py     rebuilds a fixture (history included); unpacks and packs it for editing
│   │   └── score.py            measures improve-codebase runs; `verify` checks the fixtures (CI)
│   └── results/                run output (gitignored)
├── scripts/
│   ├── check.py                structural checks, run by CI
│   └── stamp_versions.py       version stamping, run by the release workflow
├── .github/workflows/
│   ├── ci.yml                  checks on every push and PR
│   └── release.yml             manual release: stamp, tag, GitHub release
├── AGENTS.md                   instructions for agents working on this repo
├── CLAUDE.md                   imports AGENTS.md
└── LICENSE
```

The repo has no `plugin.json`. Each plugin entry in `marketplace.json` uses `strict: false` and lists its skill paths explicitly. The skills CLI reads the same file and groups skills by plugin. Skills stay flat in `skills/` whatever their category; only the marketplace says which plugin a skill belongs to.

## Local development

Clone the repo:

```bash
git clone https://github.com/nkootstra/skills.git
cd skills
```

Check that the plugin and skills are valid:

```bash
python3 scripts/check.py        # frontmatter, marketplace, links, eval cases; same as CI
python3 evals/quality/score.py verify   # eval fixtures still replay and print their recorded outputs; same as CI
claude plugin validate .        # expect: ✔ Validation passed
npx skills add . --list         # lists every skill, grouped by plugin
```

Try your local copy in Claude Code by adding the folder as a marketplace:

```
/plugin marketplace add ./
/plugin install design-skills@nkootstra-skills
```

After editing a skill, run `/plugin marketplace update nkootstra-skills` and start a new session.

### Adding or changing a skill

[AGENTS.md](AGENTS.md) has the full steps. In short:

1. Create `skills/<name>/SKILL.md` with `name`, `description` and `metadata` (`author`, `version`).
2. Keep `SKILL.md` lean. Put detail in reference files under `references/`, each linked with a trigger saying when to load it.
3. Add the path to its plugin's `skills` array in `.claude-plugin/marketplace.json` and a row to that category's table above. For a new category, add a new plugin entry (see [AGENTS.md](AGENTS.md)).
4. Add eval cases and run the eval.
5. Leave versions alone; the release workflow stamps them.

## Evals

Two evals run on `claude plugin eval`:
- **Triggering** checks which skill Claude loads for a prompt, for every skill.
- **Quality** checks output against concrete claims, judged by a separate model. The writing skills and improve-codebase have it; for improve-codebase a script also measures behavior and structure on the repos the runs leave behind.

### What it tests

The eval covers every skill in the repo, across categories, so it also catches a skill from one category firing on another's prompts. Today it has 80 synthesized prompts:
- **56 positives**, 8 per skill: direct, indirect and hard phrasings.
- **24 near-misses** that should load no skill: UI code without design judgment, writing the writing skills don't cover, and code changes that aren't about structure across a codebase.

Every case runs twice. A run passes when:
- the expected skill loads (`loads-expected` grader), and
- no other skill loads (one `not-<skill>` grader per sibling).

Where two skills both make sense, a case lists the second skill as `also_ok`, and it doesn't count as a false positive. All cases are listed in [`evals/triggering/cases.md`](evals/triggering/cases.md).

### Running

```bash
# 1. Generate the case folders (they are gitignored, so do this after every clone or edit)
python3 evals/triggering/make_cases.py

# 2. Run the eval
claude plugin eval . --tag triggering --runs 2 --ablation none --model claude-opus-5-5 \
  --trust-plugin --no-publish --threshold 0 --max-cost-usd 30 -j 4 \
  --json evals/results/run.json

# 3. Summarize
python3 evals/triggering/summarize.py evals/results/run.json
```

| Flag | Why |
|---|---|
| `--tag triggering` | All cases. Use `--tag triggering-<skill-name>` for one skill's cases, `--tag triggering-none` for the near-misses, or `--case triggering-<id>` for one case. |
| `--ablation none` | Skip the run without the plugin; the graders already cover "nothing loaded". |
| `--max-cost-usd` | Hard spending cap. A full run cost about $18 on Opus 5.5 at 67 cases; expect about $22 at 80. |
| `-j 4` | Four cases in parallel. |
| `--no-publish` | Keep the HTML report local. |

Output of the latest full run (67 cases, design and writing). The 13 improve-codebase cases were run on their own with the near-misses: recall 16/16, precision 16/16, near-misses 48/48, $4.82.

```
pass rate 100% over 134 runs (±0% 95% CI)
skill                      recall      precision
design-critique            16/16       16/16
design-exploration         16/16       16/16
intentional-prototyping    16/16       16/16
interface-polish           16/16       16/16
write-readme               16/16       16/16
write-prose                16/16       16/16
negatives specificity      38/38
cost/run   median $0.080  max $1.081  total $18.38
turns/run  median 5.0  max 9   seconds/run median 13.0  max 240
```

Any failures are listed below it, with the skill that loaded instead.

### Reading results

- **Recall:** how often the skill loads on its own prompts. The target is 16/16 per skill.
- **Precision:** how often a load was correct. The target is 100%.
- **Negatives specificity:** near-miss runs where nothing loaded. The target is all of them (38/38 in that run; 48/48 with the current 24 near-misses).
- **Timeouts and turn limits:** "Reached maximum number of turns" or a timeout on long prototyping runs isn't a failure by itself, because the skill has loaded by then and the graders still score.


### Quality

Each quality case gives Claude a realistic task and checks the result claim by claim, with one LLM grader per claim. The writing skills and improve-codebase have quality cases.

#### Writing skills

Each case is a realistic writing task:
- **write-prose** (17 cases): explaining for a given audience (a performance deep-dive, a system explainer for newcomers, an incident write-up, a concept for non-engineers), tightening a draft without cutting what earns its place, turning notes into a post without inventing facts, de-slopping an about page, keeping uncertainty a source leaves open, a light edit that preserves an exact quote, a PR body from given facts, a commit subject.
- **write-readme** (8 cases, each with a small fixture repo): a Node CLI, a Python library, an existing README with stale commands, a service whose version files and env example disagree with the code, a pnpm monorepo, a requested deploy section with no deploy config, an existing README with personality to preserve, and env vars read only in code. The checks cover the right package manager, real commands and options, no invented env vars or deploy sections, and keeping accurate content when updating.

```bash
python3 evals/quality/make_cases.py
claude plugin eval . --tag quality-write-prose --tag quality-write-readme --ablation none --model claude-opus-5-5 --judge-model sonnet \
  --scaffold --allow-tools Write Edit Bash --trust-plugin --no-publish --threshold 0 --max-cost-usd 15 -j 4 \
  --json evals/results/quality.json
```

`--scaffold` writes the fixture repos; `--allow-tools` lets the README cases write files. Add `--ablation with-without` to compare against Claude without the plugin.

Latest run with `--ablation with-without`, 3 runs per case (Opus 5.5, Sonnet as judge, about $50 for both arms):

| Skill | With the plugin | Without |
|---|---|---|
| write-prose | 277/345 checks (80%) | 234/345 (68%) |
| write-readme | 152/153 | 151/153 |

write-prose gains most on explaining and on drafts with residue to remove: tightening a draft 21/21 against 14/21, the incident write-up 20/24 against 15/24, the performance deep-dive 21/27 against 16/27, and the data report 23/30 against 16/30. Plain Opus already writes good READMEs for these fixture repos; the skill's value there is that it reads the repo, runs the tests and reports gaps as `TODO:` lines instead of guessing. Compare totals at 3 runs: a single case swings by ±4 checks between runs.

#### improve-codebase

Five cases on two fixture repos, each with planted structural problems, a commit history and a small test suite:
- **parcel**, a Python CLI for shipping quotes: the same carrier `if` chain in three files, an import cycle, a global flag one module sets for another, a discount known in three places, a rule copied four times, unused code. Four cases use it: the improvement, the improvement with all three optional passes, the improvement without saying which passes (no one answers the question), and an audit only.
- **deskline**, a Node CLI for help-desk tickets, organised by technical layer: priorities defined in four folders, scattered status checks, code reaching into the store's internals, a global clock, an import cycle.

The judge checks the final report: tests were run, behavior was kept or the changes are named, the planted bug is reported as a decision and not fixed, and decisions are listed apart from changes. What the judge can't check is measured afterwards by `evals/quality/score.py` on the repos the runs leave behind:
- **Behavior:** each fixture has about 70 recorded CLI outputs the agent never sees. Any difference is a behavior change.
- **Planted bug:** three more outputs exercise a real bug whose fix changes output. Unchanged means the run left the decision to the user.
- **Structure:** counts of each planted problem, before and after.

```bash
python3 evals/quality/make_cases.py
claude plugin eval . --tag quality-improve-codebase --runs 3 --ablation none --model claude-opus-5-5 --judge-model sonnet \
  --scaffold --allow-tools Write Edit Bash --keep-temp --trust-plugin --no-publish --threshold 0 --max-cost-usd 30 -j 3 \
  --json evals/results/improve-codebase.json

# --keep-temp prints "kept /private/tmp/e-..." per run, with the chmod that opens it. Then:
python3 evals/quality/score.py score parcel run1=/private/tmp/e-AAAA run2=/private/tmp/e-BBBB
python3 evals/quality/score.py score deskline run1=/private/tmp/e-CCCC
```

`score.py` copies each repo out before running anything; never run git inside a kept directory. Each fixture is one file, `evals/quality/fixtures/<name>.json`. To change its code, unpack it with `python3 evals/quality/fixture_repo.py unpack <name> <dir>`, edit, pack it back with `fixture_repo.py pack <name> <dir>`, then run `score.py record <name>`. CI runs `score.py verify`, which fails when a fixture no longer replays its history, fails its tests or prints different outputs than recorded.

Latest run, 3 runs per case (Opus 5.5, Sonnet as judge, $20.76):

| Case | Judge checks | Recorded outputs unchanged | Planted bug | Structure |
|---|---|---|---|---|
| improve-python-cli | 18/18 | 74/74 in all 3 | left for the user, 3/3 | carrier branches 14 → 0, import cycle and global flags gone, rule copies 4 → 1, unused code removed |
| improve-python-cli-all-passes | 18/18 | 74/74 in 2; 72/74 in 1, from a bug fix it named | fixed, 3/3 | same as above; tests 8 → 12–22 |
| improve-python-cli-no-answer | 9/9 | 74/74 in all 3 | left for the user, 3/3 | same as above |
| audit-python-cli | 17/18 | 0 files changed in all 3 | left, 3/3 | unchanged, as asked |
| improve-layered-node-cli | 18/18 | 70/70 in all 3 | left for the user, 3/3 | files defining priorities 4 → 1, status checks 9 → 2–5, import cycle and swallowed errors gone |

In the all-passes case, the user opted into bug fixes. One run also fixed the report's list price, which was a cent off from dividing a rounded number; it did so in its own commit and flagged that the warehouse scripts read that output. The audit's "claims no changes" check is noisy: it fails about one run in three when a reply mentions an experiment run in memory or a scratch copy. `score.py` is the reliable signal there and has shown 0 files changed in every audit run. "Recorded outputs unchanged" covers those outputs only. On deskline, all runs left the store internals, the global clock and the unused CSV export in place, each with a stated reason. That is a choice the skill allows, not a miss.

## Versioning and releases

Versions use semver at two levels:

| Version | Where |
|---|---|
| Plugin | `version` on the plugin's entry in `.claude-plugin/marketplace.json`. Claude Code uses it to decide when installed copies update. |
| Skill | `metadata.version` in each `SKILL.md`. |

Nobody edits them by hand. To release, run **Actions → Release → Run workflow** on `main` and pick the plugin and the part to raise:

| Part | When |
|---|---|
| patch | Wording only. |
| minor | New guidance, a new reference file, or wider triggering. |
| major | Renamed or removed skills, removed guidance, narrower triggering, or different output. Moving a reference file is not major on its own. |

The workflow:
1. Requires a green CI run.
2. Refuses to release when none of the plugin's skills changed since its last tag.
3. Stamps the new version on the plugin and on each changed skill, and commits that to `main`.
4. Tags the commit `<plugin>-v<version>`, for example `design-skills-v1.1.0`.
5. Creates a GitHub release with generated notes.

[GitHub Releases](https://github.com/nkootstra/skills/releases) is the changelog.

## Troubleshooting

**A skill doesn't load when expected.** The agent decides from the `description` alone. Phrase the request around the task the description names, or call the skill by name. If a real phrasing is missed, add it as an eval case and widen the description.

**`claude plugin validate .` fails.** Check that every path in each plugin's `skills` array exists, that no skill is listed in two plugins, and that each folder has a `SKILL.md` whose `name` matches the folder.

**A plugin doesn't pick up changes.** Run `/plugin marketplace update nkootstra-skills` and start a new session. Updates only arrive after a release, because the release raises the plugin `version`.

**Eval run finds no cases, or scores 0 on every positive.** The case folders are generated and gitignored: run both `make_cases.py` scripts first. Each case's `prompt.md` needs `plugins: ["../../.."]`, which the scripts write.

**Eval runs time out.** Prototyping prompts produce long answers and can run for 200+ seconds. Triggering is graded before the timeout, so scores stay valid. Raise `timeout_seconds` in `make_cases.py` if you need complete transcripts.

## Contributing

Issues and pull requests are welcome. Read [AGENTS.md](AGENTS.md) first: it covers the frontmatter, writing style, eval cases and version bumps that each change needs.

## License

[MIT](LICENSE) © 2026 Niels Kootstra
