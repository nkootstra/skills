# AGENTS.md

This repo holds agent skills by Niels Kootstra. They install with `npx skills add nkootstra/skills` or as Claude Code plugins, one per category. Today there is one category, design (`design-skills`); more will follow. They are written for Claude Code first and stay compatible with the Agent Skills format.

## Layout

```
.claude-plugin/marketplace.json   marketplace: one plugin entry per category, each listing its skills
skills/<name>/SKILL.md            the skill: frontmatter, workflow, load triggers
skills/<name>/*.md                reference files, loaded on demand
evals/triggering/                 does the right skill load, and only that one
evals/results/                    run output (gitignored)
CHANGELOG.md                      one entry per release
```

There is no `plugin.json`; each plugin entry uses `strict: false` and lists its skill paths explicitly. Skills stay flat in `skills/` whatever their category: the marketplace alone decides which plugin a skill belongs to. Don't nest skills in category folders; the skills CLI expects `skills/<name>/SKILL.md`.

## Creating or changing a skill

1. Create `skills/<name>/SKILL.md`. The folder name equals `name`, in kebab-case.
2. Frontmatter:
   ```yaml
   ---
   name: <name>
   description: <what it does, then "Use whenever ..." with the situations and phrasings that should trigger it>
   metadata:
     author: Niels Kootstra
     version: "1.0.0"
   ---
   ```
   - `description` is what decides triggering. Lead with what the skill does: the skills CLI picker shows about the first 150 characters. Keep it under 1024.
   - `metadata` values are strings, so quote the version.
   - Add Claude Code fields only when they help:
     - `effort: high` for skills that need deep reasoning (critique, exploration).
     - `argument-hint` for skills invoked with a target.
     - `disable-model-invocation: true` for skills that should run only when called by name.
3. Body:
   - Keep `SKILL.md` under 500 lines (ours are 65 to 80).
   - Put catalogs, templates, checklists and code in sibling reference files, one level deep.
   - Link each reference file under a "Reference files" heading, with a trigger that says when to load it (`When building the control panel, load [tuning-panel.md](tuning-panel.md)`).
   - End with a "Companion skills" section that says when to hand off to each sibling skill in the same category.
4. Add the skill path to its plugin's `skills` array in `.claude-plugin/marketplace.json` and a row to that category's README table. A skill belongs to exactly one plugin.
5. Check:
   - Run `claude plugin validate .` and `npx skills add . --list`.
   - Confirm every linked reference file exists.
6. Add eval cases (below) before calling the skill done.

## Adding a category

1. Add a plugin entry to `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "<category>-skills",
     "description": "<one line>",
     "version": "1.0.0",
     "author": { "name": "Niels Kootstra" },
     "source": "./",
     "strict": false,
     "skills": ["./skills/<skill>", "..."]
   }
   ```
2. Add the skills to `skills/` as usual.
3. In the README:
   - Add a `### <Category> skills` section under Skills, with the plugin name and a table.
   - Add a row to the plugin table under Installation.
4. Add a `## <category>-skills` section to `CHANGELOG.md`.
5. Add the skills to the triggering eval (below). It covers every skill in the repo, so prompts from one category also guard against skills from another firing.

Writing style for skills:
- Write in our own words. Don't copy text from other skills or repos.
- Don't name or credit other authors or skills anywhere in the repo, including evals and docs. Naming a library the skill tells the agent to use is fine.
- Name established principles where they sharpen an instruction (Fitts's law, Hick's law, Nielsen's heuristics), and only those that change what the agent does.
- Prefer concrete checks and numbers over adjectives.

## Evals

The eval measures triggering only: which skill Claude loads, not the quality of what it writes. It runs on `claude plugin eval`.

- Defined in `evals/triggering/make_cases.py` as `CASES` tuples: `(id, expected, also_ok, difficulty, prompt)`.
  - `expected` is a skill name or `none`.
  - `also_ok` lists sibling skills that may load without counting as a false positive.
- Running the script regenerates `cases.jsonl`, `cases.md` and one folder per case: `prompt.md` plus `graders/`.
  - The `loads-expected` grader requires the expected skill to load.
  - One `not-<skill>` grader per sibling forbids that sibling from loading.
- Never edit case folders by hand; edit `CASES` and rerun.
- For a new skill:
  - Add it to `SKILLS` in `make_cases.py` and `summarize.py`, and its short unique id prefix to `PREFIX` in `summarize.py`.
  - Every case forbids every other skill, so cases from all categories are checked against all skills.
  - Write about 8 positive prompts: direct, indirect, and hard ones phrased the way a user would actually ask.
  - Add near-miss `none` prompts that should load nothing.
  - Keep ids as `<prefix>-NN`.

### Running

```sh
python3 evals/triggering/make_cases.py
claude plugin eval . --tag triggering --runs 2 --ablation none --model claude-opus-5-5 \
  --trust-plugin --no-publish --threshold 0 --max-cost-usd 20 -j 4 --json evals/results/<name>.json
python3 evals/triggering/summarize.py evals/results/<name>.json
```

- Use `--tag <skill>` to run one skill's cases, or `--case <name>` for a single case; only the last `--case` flag counts.
- Cost on Opus 5.5 is about $13 for a full triggering run. Prototyping cases are the slowest and most expensive.
- Get approval before spending on a full run. After a description change, rerun the affected skill's cases plus the `none` cases.
- A run passes when every skill's recall is 16/16, its precision is 100%, and negatives are 24/24.
  - Timeouts and "Reached maximum number of turns" are not failures by themselves: the skill has loaded by then and the graders still score.
- Current baseline: 84/88 at the first full run; the two missed prompts pass after the description fixes, with no new false positives.

## Versions

Two version numbers exist, and both use semver.

- **Skill version**: `metadata.version` in each `SKILL.md`. Bump it when that skill changes:
  - **Patch** (`1.0.1`): wording, typos, clearer examples, no change in behavior or triggering.
  - **Minor** (`1.1.0`): new guidance, a new reference file, or a description change that widens triggering.
  - **Major** (`2.0.0`): renamed or removed skill, removed reference files, a narrowed description, or a workflow that produces different output.
- **Plugin version**: `version` on the plugin's entry in `.claude-plugin/marketplace.json`. Each plugin is versioned on its own.
  - Bump it in every release that changes any of its skills, using the highest level among the skill bumps.
  - Claude Code uses this field to decide whether installed copies need an update, so a skill change without a plugin bump never reaches plugin users.
- **Changelog**: add an entry under the plugin's section in `CHANGELOG.md` for each plugin version, listing each changed skill with its new version and a one-line reason.
  - Note eval results when a description changed.
  - No tool or model attribution lines.
- **Releases**: tag the commit `<plugin>-v<version>` (for example `design-skills-v1.1.0`) after the change and its eval run are committed.

Eval-only changes and README edits don't bump any version.


