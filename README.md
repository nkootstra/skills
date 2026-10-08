# Skills

Agent skills by Niels Kootstra. They are written primarily for Claude Code and work with any agent that supports the [Agent Skills](https://agentskills.io) format.

Skills are grouped into plugins by category. The first category is design: critiquing, exploring, prototyping and finishing interfaces.

Each skill is a short workflow plus reference files that the agent loads only when a step needs them. The skills trigger on their own when a request matches, and they can also be called by name.

## Key features

- **Grouped by category:** each category is its own Claude Code plugin in one marketplace, so you install only what you need. Today: `design-skills`.
- **Two ways to install:** with the skills CLI (`npx skills add`) for any compatible agent, or as Claude Code plugins.
- **Progressive loading:** each `SKILL.md` stays under 80 lines. About 2,500 lines of rubrics, checklists, ranges and code live in reference files, and each file has an explicit trigger saying when to load it.
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

## Prerequisites

| For | You need |
|---|---|
| Installing with the skills CLI | Node.js with `npx` |
| Installing as a plugin | [Claude Code](https://claude.com/claude-code) |
| Running the evals | Claude Code (`claude plugin eval`) and Python 3.9 or newer |

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
```

| Plugin | Skills |
|---|---|
| `design-skills` | design-critique, design-exploration, intentional-prototyping, interface-polish |

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

Or call a skill directly, with a target:

```
/design-critique src/pages/Checkout.tsx
/intentional-prototyping card flip on tap
```

As a plugin, use the namespaced form: `/design-skills:design-critique src/pages/Checkout.tsx`.

The skills stay out of tasks that only touch UI code, such as fixing a TypeError, renaming a prop, converting a color, or setting up Tailwind.

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
3. **When a step needs it:** the agent loads a reference file. Each link in `SKILL.md` says when to load it, for example `Load [rubric.md](rubric.md) on the second and third passes.`

This keeps the cost of having the skills installed small, while the detail is there when needed.

## Repository layout

```
.
├── .claude-plugin/
│   └── marketplace.json        marketplace; one plugin entry per category, each listing its skills
├── skills/                     all skills, flat, whatever their category
│   ├── design-critique/
│   │   ├── SKILL.md
│   │   ├── rubric.md
│   │   ├── facets.md
│   │   └── output-template.md
│   ├── design-exploration/
│   │   ├── SKILL.md
│   │   ├── range-techniques.md
│   │   └── depth-ladder.md
│   ├── intentional-prototyping/
│   │   ├── SKILL.md
│   │   ├── tuning-panel.md
│   │   ├── parameter-ranges.md
│   │   ├── recreation.md
│   │   └── react-prototypes.md
│   └── interface-polish/
│       ├── SKILL.md
│       ├── platform-baselines.md
│       ├── states-and-edges.md
│       ├── motion.md
│       ├── visual-rules.md
│       ├── ship-checklist.md
│       └── react-components.md
├── evals/
│   ├── triggering/
│   │   ├── make_cases.py       source of truth for the cases; generates everything below
│   │   ├── summarize.py        per-skill recall and precision from a results file
│   │   ├── cases.jsonl         generated
│   │   ├── cases.md            generated, readable table of all cases
│   │   └── <case-id>/          generated: prompt.md + graders/
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
2. Keep `SKILL.md` lean. Put detail in sibling reference files, each linked with a trigger saying when to load it.
3. Add the path to its plugin's `skills` array in `.claude-plugin/marketplace.json` and a row to that category's table above. For a new category, add a new plugin entry (see [AGENTS.md](AGENTS.md)).
4. Add eval cases and run the eval.
5. Leave versions alone; the release workflow stamps them.

## Evals

The eval checks **triggering**: which skill Claude loads for a prompt. It doesn't judge the quality of what Claude writes. It runs on `claude plugin eval`.

### What it tests

The eval covers every skill in the repo, across categories, so it also catches a skill from one category firing on another's prompts. Today it has 44 synthesized prompts:
- **32 positives**, 8 per skill: direct, indirect and hard phrasings.
- **12 near-misses** that should load no skill.

Every case runs twice. A run passes when:
- the expected skill loads (`loads-expected` grader), and
- no other skill loads (one `not-<skill>` grader per sibling).

Where two skills both make sense, a case lists the second skill as `also_ok`, and it doesn't count as a false positive. All cases are listed in [`evals/triggering/cases.md`](evals/triggering/cases.md).

### Running

```bash
# 1. Regenerate case folders (only needed after editing CASES in make_cases.py)
python3 evals/triggering/make_cases.py

# 2. Run the eval
claude plugin eval . --tag triggering --runs 2 --ablation none --model claude-opus-5-5 \
  --trust-plugin --no-publish --threshold 0 --max-cost-usd 20 -j 4 \
  --json evals/results/run.json

# 3. Summarize
python3 evals/triggering/summarize.py evals/results/run.json
```

| Flag | Why |
|---|---|
| `--tag triggering` | All cases. Use `--tag <skill-name>` for one skill's cases, or `--case triggering-<id>` for one case. |
| `--ablation none` | Skip the run without the plugin; the graders already cover "nothing loaded". |
| `--max-cost-usd` | Hard spending cap. A full run costs about $13 on Opus 5.5. |
| `-j 4` | Four cases in parallel. |
| `--no-publish` | Keep the HTML report local. |

Output of the first full run:

```
pass rate 95% over 88 runs (±4% 95% CI)
skill                      recall      precision
design-critique            16/16       16/16
design-exploration         14/16       14/14
intentional-prototyping    14/16       14/14
interface-polish           16/16       16/16
negatives specificity      24/24
cost/run   median $0.079  max $0.741  total $12.56
turns/run  median 5.0  max 9   seconds/run median 12.0  max 240
```

Any failures are listed below it, with the skill that loaded instead.

### Reading results

- **Recall:** how often the skill loads on its own prompts. The target is 16/16 per skill.
- **Precision:** how often a load was correct. The target is 100%.
- **Negatives specificity:** near-misses where nothing loaded. The target is 24/24.
- **Timeouts and turn limits:** "Reached maximum number of turns" or a timeout on long prototyping runs isn't a failure by itself, because the skill has loaded by then and the graders still score.

Current baseline: the two prompts missed above, a brainstorm and a variations grid, pass after description fixes, with no new false positives.

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
| major | Renamed or removed skills or files, narrower triggering, or different output. |

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

**Eval run scores 0 on every positive.** The plugin didn't load into the sandbox. Each case's `prompt.md` needs `plugins: ["../../.."]`. Regenerate with `make_cases.py`.

**Eval runs time out.** Prototyping prompts produce long answers and can run for 200+ seconds. Triggering is graded before the timeout, so scores stay valid. Raise `timeout_seconds` in `make_cases.py` if you need complete transcripts.

## Contributing

Issues and pull requests are welcome. Read [AGENTS.md](AGENTS.md) first: it covers the frontmatter, writing style, eval cases and version bumps that each change needs.

## License

[MIT](LICENSE) © 2026 Niels Kootstra
