# Project types

Identify the type from evidence in the repo, not from the name or the user's description alone. A repo can be more than one type (a library that ships a CLI, a monorepo of services); cover each part the reader will use, and lead with the one most readers come for.

## Evidence to type

| Evidence | Type | Sections it needs |
|---|---|---|
| A `bin` field in `package.json`, `[project.scripts]` in `pyproject.toml`, `cmd/` in Go, an argument parser such as clap, cobra, click or commander | CLI | install, commands and flags, examples, config file and exit codes if any |
| A published package (`name` and `version` meant for a registry, `exports`, a `src/` layout) and no app entry point | Library | install, minimal usage, API overview or link to reference docs, supported language and runtime versions |
| A server or app entry point, a `Dockerfile`, a database config, env reads | App or service | prerequisites, configuration, run locally, test, deploy (only from config in the repo) |
| Workspaces in the manifest, `packages/*`, `apps/*`, `go.work`, a Cargo workspace | Monorepo | what each package is, root commands, how packages depend on each other, links to package READMEs |
| `.claude-plugin/`, `skills/*/SKILL.md`, an extension or plugin manifest | Plugin or skills repo | what it contains, install per supported tool, how it is structured, how to add to it |
| `*.tf`, `k8s/`, `helm/`, Pulumi or CDK code | Infrastructure | what it provisions, required inputs and variables, plan/apply/destroy, where state lives |

## Where each fact comes from

| Fact | Look in |
|---|---|
| Language and runtime version | `.nvmrc`, `.node-version`, `.tool-versions`, `.python-version`, `engines`, `requires-python`, `go.mod`, `rust-toolchain.toml`, the CI setup step |
| Package manager | The lockfile: `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`, `bun.lockb`, `uv.lock`, `poetry.lock`, `Pipfile.lock` |
| Install, build, test, lint commands | Manifest scripts, `Makefile`, `justfile`, `Taskfile.yml`, `bin/`, and the CI steps that run them |
| Env vars | `.env.example` or `.env.sample`, then the code's env reads (`process.env`, `os.environ`, `os.Getenv`, `env::var`) and config schemas; mark which ones have defaults |
| Services the app needs | `docker-compose.yml`, database and cache config, client libraries in the dependencies |
| Deploy target | Deploy config such as `fly.toml`, `vercel.json`, `netlify.toml`, `render.yaml`, `Procfile`, `serverless.yml`, a deploy workflow; nothing else counts |
| Supported versions | CI matrix, `engines`, classifiers, `peerDependencies` |
| License | `LICENSE` file and the manifest's license field; flag it when they disagree |

When two sources disagree (an `.nvmrc` says 18, CI runs 20), document what CI runs and mention the mismatch in your report.
