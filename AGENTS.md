# AGENTS.md

This repo holds agent skills by Niels Kootstra. They install with `npx skills add nkootstra/skills` or as Claude Code plugins, one per category. Today there are three categories: design (`design-skills`), writing (`writing-skills`) and engineering (`engineering-skills`); more will follow. They are written for Claude Code first and stay compatible with the Agent Skills format.

## Layout

```
.claude-plugin/marketplace.json   marketplace: one plugin entry per category, each listing its skills
skills/<name>/SKILL.md            the skill: frontmatter, workflow, load triggers
skills/<name>/references/*.md     reference files, loaded on demand
evals/triggering/                 does the right skill load, and only that one
evals/quality/                    is the output good: LLM-graded checks per case (writing skills, improve-codebase)
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
   - Put catalogs, templates, checklists and code in `references/`, one level deep. Nothing but `SKILL.md` sits at the skill's root.
   - Link each reference file under a "Reference files" heading, with a trigger that says when to load it (`When building the control panel, load [tuning-panel.md](references/tuning-panel.md)`).
   - End with a "Companion skills" section that says when to hand off to each sibling skill in the same category.
4. Add the skill path to its plugin's `skills` array in `.claude-plugin/marketplace.json` and a row to that category's README table. A skill belongs to exactly one plugin.
5. Check:
   - Run `python3 scripts/check.py`, `python3 evals/quality/score.py verify`, `claude plugin validate .` and `npx skills add . --list`.
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

Two evals, both on `claude plugin eval`:
- **Triggering** (`evals/triggering/`): which skill Claude loads. Every skill needs it.
- **Quality** (`evals/quality/`): whether the output meets concrete checks. The writing skills have it, because their output can be checked claim by claim, and improve-codebase has it, with a script that measures the repos its runs leave behind.

- Defined in `evals/triggering/make_cases.py` as `CASES` tuples: `(id, expected, also_ok, difficulty, prompt)`.
  - `expected` is a skill name or `none`.
  - `also_ok` lists sibling skills that may load without counting as a false positive.
- Running the script writes `cases.md` (committed) and one folder per case: `prompt.md` plus `graders/`. The folders are gitignored: generate them before every run.
  - The `loads-expected` grader requires the expected skill to load.
  - One `not-<skill>` grader per sibling forbids that sibling from loading.
- Never edit case folders by hand; edit `CASES` and rerun. `scripts/check.py` fails when `cases.md` is out of date, a case names an unknown skill, or a skill has fewer than 8 positive cases.
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
  --trust-plugin --no-publish --threshold 0 --max-cost-usd 30 -j 4 --json evals/results/<name>.json
python3 evals/triggering/summarize.py evals/results/<name>.json
```

- Use `--tag triggering-<skill>` to run one skill's triggering cases and `--tag triggering-none` for the near-misses, or `--case <name>` for a single case; only the last `--case` flag counts. A bare `--tag <skill>` also matches that skill's quality cases.
- Cost on Opus 5.5 was about $13 for a full triggering run at 44 cases; expect about $20 at 67 and about $22 at 80. Prototyping cases are the slowest and most expensive.
- Get approval before spending on a full run. After a description change, rerun the affected skill's cases plus the `none` cases.
- A run passes when every skill's recall is full (8 prompts × 2 runs = 16/16), its precision is 100%, and every negative run loads nothing.
  - Timeouts and "Reached maximum number of turns" are not failures by themselves: the skill has loaded by then and the graders still score.
- Current baseline: 134/134 runs at 67 cases (all six design and writing skills 16/16, negatives 38/38), $18.38. The 13 improve-codebase cases (80 in total) were run afterwards with the near-misses: improve-codebase 16/16 recall and precision, near-misses 48/48, $4.82.

### Quality eval

- Defined in `evals/quality/<skill>.json`: per case an `id`, a `prompt`, and `expectations`, one concrete, checkable claim each.
  - write-prose cases inline their input text from `evals/quality/inputs/`.
  - write-readme cases carry a `fixture` (path → contents). A scaffold script writes it into the run's workspace, and the claims are judged against the `README.md` the run leaves behind.
  - An expectation can be `{"criteria": ..., "focus": "last_message"}` to judge the reply instead of the file.
  - improve-codebase cases name a `fixture`, one file each in `evals/quality/fixtures/<name>.json` with `files` (the repo), `history` (commits as text replacements on those files), `checks` (how to measure a run) and `golden` (recorded outputs). The claims are judged against the final report. To edit a fixture's code: `fixture_repo.py unpack <name> <dir>`, edit, `fixture_repo.py pack <name> <dir>`, then `score.py record <name>`.
- `python3 evals/quality/make_cases.py` writes one case folder per case (gitignored, so generate before a run): a `loads-skill` grader plus one LLM grader per expectation. Never edit the case folders by hand.
- Run with a judge that is not the agent model:
  ```sh
  python3 evals/quality/make_cases.py
  claude plugin eval . --tag quality-write-prose --tag quality-write-readme --ablation none --model claude-opus-5-5 --judge-model sonnet \
    --scaffold --allow-tools Write Edit Bash --trust-plugin --no-publish --threshold 0 --max-cost-usd 15 -j 4 \
    --json evals/results/<name>.json
  ```
- For improve-codebase, add `--keep-temp` and score the kept workspaces afterwards: `python3 evals/quality/score.py score <fixture> <label>=<kept dir> ...`. It reports whether the recorded CLI outputs are unchanged, whether the planted bug was left for the user, and the count of each planted problem. Open a kept directory with the `chmod` the eval prints, and never run git inside it. CI runs `python3 evals/quality/score.py verify`, which fails when a fixture no longer replays its history, fails its own tests, or prints different outputs than recorded.
- `--ablation with-without` adds a run without the plugin, which shows what the skill adds over the bare model. It doubles the cost.
- Get approval before a run. After changing a skill's guidance, rerun that skill's cases with `--tag quality-<skill>`. Repeated `--tag` flags match any of the tags, not all of them, so `--tag quality --tag <skill>` also runs that skill's triggering cases. `--tag quality` alone runs every quality case, improve-codebase's included, which need `--keep-temp` and a higher cost cap.
- Current baseline (3 runs per case): write-prose 311/375 against 230/375 without the plugin (18 cases), write-readme 152/153 against 151/153. improve-codebase 80/81 judge checks (5 cases, no without-arm yet; the miss is the audit case's "claims no changes" check, which is noisy at about one run in three). `score.py` showed the recorded outputs unchanged in every run except one opted-in bug fix the run named, the planted bug fixed only when the bug-fix pass was chosen, and no files changed in any audit; $20.76. The two `stockroom` cases (`audit-warehouse-cli`, `improve-warehouse-cli`) were added later and have no recorded judge baseline yet; in 16 improve runs on Opus 5.5 and Sonnet 5.5, `score.py` showed the recorded outputs unchanged, the tests passing and no outside code left writing to the shelf's stock. Judge a change by the with/without gap over all cases at 3 runs, never by one case: a single case swings by ±4 checks between runs of the same skill.
- The judge's votes come without reasons, so a score alone can't tell a weak output from a bad check. Before changing a skill to fix a check that keeps failing, re-judge one failing output with `claude -p --model sonnet`, asking for a verdict, a reason and whether the claim is satisfiable from the source. A check that can only pass by inventing content (a reason the notes never give, a point of view the source lacks) is a bad check: reword it, then rerun both arms, since that changes the baseline.

## Versions and releases

Versions use semver at two levels, and nobody edits them by hand:
- **Plugin**: `version` on the plugin's entry in `.claude-plugin/marketplace.json`. Claude Code uses it to decide when installed copies update. Plugins are versioned independently.
- **Skill**: `metadata.version` in each `SKILL.md`.

To release, run Actions → Release → Run workflow on `main`, then pick the plugin and the part to raise:
- **patch**: wording, typos, clearer examples; no change in behavior or triggering.
- **minor**: new guidance, a new reference file, or a description change that widens triggering.
- **major**: a renamed or removed skill, removed guidance, a narrowed description, or a workflow that produces different output.

Reference-file paths are internal: nobody calls them, so moving or renaming one counts by what changed in its content, not by the move.

The workflow:
1. Requires a green CI run on the commit.
2. Refuses to release if none of the plugin's skills changed since its last `<plugin>-v<version>` tag. Eval, docs and workflow changes don't release.
3. Raises the plugin version by the chosen part. It raises each changed skill by the same part, using `scripts/stamp_versions.py`.
4. Commits the stamp to `main` (signed, through the GitHub API).
5. Tags the commit `<plugin>-v<version>` and creates a GitHub release.

The first release of a plugin ships the version already on `main`, unchanged.

The release notes list each commit since the last tag that touched one of the plugin's skills, by subject, with a link to its PR, so GitHub Releases is the changelog and a PR that changes two plugins appears in each only with its own commits. Write commit subjects for someone reading the release notes, one plugin per commit, without tool or model attribution lines. When a description changed, give the eval result in the PR description.
