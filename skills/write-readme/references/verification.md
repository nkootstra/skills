# Verification

Run these before reporting back. A README that fails on step two of its own setup costs the reader more than having no README.

## Checks

- **Commands exist.** Every command in the README maps to a script, binary, make target or CI step in the repo, spelled the same way.
- **Commands run.** Run the safe ones where the environment allows: `--help`, install, build, test, lint. Don't run anything that deploys, writes to external services, deletes data or needs credentials. Report which commands you ran and which you couldn't.
- **Package manager matches.** Commands use the manager the lockfile shows, never a mix.
- **Versions match.** Prerequisite versions agree with the version files, `engines` or `requires-python`, and the CI matrix.
- **Env vars match.** Every documented variable is read somewhere in the code or listed in `.env.example`, and every variable needed to run locally is documented.
- **Links resolve.** Every relative link and anchor points to a file or heading that exists.
- **Nothing invented.** No deploy target, service, port, badge, screenshot or feature appears without a source in the repo. Unknowns are visible `TODO:` lines, not guesses.
- **Update mode kept what was right.** When updating, accurate content from the previous README is still there, and every removal has a reason you can state.

## Common failures

| Failure | How it happens | Catch it by |
|---|---|---|
| Stale script name | A script was renamed, the README wasn't | Comparing each command against the manifest |
| Wrong package manager | Habit: `npm install` in a pnpm repo | Checking the lockfile |
| Version drift | `.nvmrc`, `engines` and CI disagree | Reading all three, documenting what CI runs |
| Undocumented env var | A command fails because it needs a key nobody listed | Reading the code's env reads, not only `.env.example` |
| Moved file | Links still point to the old path | Resolving every relative link |
| Copied reference rot | A pasted schema or env list that no longer matches | Linking the source file instead of copying it |
