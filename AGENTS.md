# AGENTS.md

This repo holds agent skills by Niels Kootstra. They install with `npx skills add nkootstra/skills` or as Claude Code plugins, one per category. Today there is one category, design (`design-skills`); more will follow. They are written for Claude Code first and stay compatible with the Agent Skills format.

## Layout

```
.claude-plugin/marketplace.json   marketplace: one plugin entry per category, each listing its skills
skills/<name>/SKILL.md            the skill: frontmatter, workflow, load triggers
skills/<name>/*.md                reference files, loaded on demand
evals/triggering/                 does the right skill load, and only that one
evals/results/                    run output (gitignored)
scripts/check.py                  structural checks (CI runs it on every push and PR)
scripts/stamp_versions.py         version stamping, used by the release workflow
.github/workflows/                ci.yml (checks), release.yml (manual release)
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
   - Run `python3 scripts/check.py`, `claude plugin validate .` and `npx skills add . --list`.
   - New skills start at `version: "1.0.0"`. Never bump versions by hand afterwards; the release workflow does it.
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
4. Add the plugin name to the `plugin` options in `.github/workflows/release.yml`. `check.py` fails until you do.
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

## Versions and releases

Versions use semver at two levels, and nobody edits them by hand:
- **Plugin**: `version` on the plugin's entry in `.claude-plugin/marketplace.json`. Claude Code uses it to decide when installed copies update. Plugins are versioned independently.
- **Skill**: `metadata.version` in each `SKILL.md`.

To release, run Actions → Release → Run workflow on `main`, then pick the plugin and the part to raise:
- **patch**: wording, typos, clearer examples; no change in behavior or triggering.
- **minor**: new guidance, a new reference file, or a description change that widens triggering.
- **major**: a renamed or removed skill or reference file, a narrowed description, or a workflow that produces different output.

The workflow:
1. Requires a green CI run on the commit.
2. Refuses to release if none of the plugin's skills changed since its last `<plugin>-v<version>` tag. Eval, docs and workflow changes don't release.
3. Raises the plugin version by the chosen part. It raises each changed skill by the same part, using `scripts/stamp_versions.py`.
4. Commits the stamp to `main` (signed, through the GitHub API).
5. Tags the commit `<plugin>-v<version>` and creates a GitHub release.

The first release of a plugin ships the version already on `main`, unchanged.

The release notes are generated from the commits and merged PRs since the last tag, so GitHub Releases is the changelog. Write commit subjects and PR titles for someone reading the release notes, without tool or model attribution lines. When a description changed, give the eval result in the PR description.
