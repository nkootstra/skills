# Sections

In the usual order. Include a section when the project type needs it and the repo supplies its facts. Each entry says what the section must contain and what to link instead of copy. The skeletons show shape only; fill them from the repo.

## Title and overview

Always. The project name, then two or three sentences: what it does, who it is for, and what makes it different from the obvious alternative if the repo says so. Badges only for things that exist (a CI workflow, a published package, a license file).

## Features

Only when the project does several distinct things a reader would choose it for. Each bullet is a capability stated concretely ("exports to CSV and Parquet"), never an adjective ("blazing fast") unless a benchmark in the repo backs it.

## Prerequisites

When anything must be installed first. Tools with versions from the repo, and services such as a database. Say how to check each one when a command exists (`node --version`).

## Installation or getting started

Always for apps, CLIs and libraries. For a library or CLI published to a registry, lead with the one-line registry install (`npm install <name>`, `pip install <name>`, `cargo add <name>`) and put clone-and-develop steps under a Development heading. For everything else, numbered steps from clone to a working result on a fresh machine: clone, install dependencies, configure, prepare data, run. Each step is a command block plus one line on what it does when that isn't obvious. End with how the reader knows it worked: a URL to open, output to expect, a command that succeeds.

```sh
<install command from the lockfile's package manager>
<run command from the scripts>
```

## Usage

For libraries and CLIs, the most valuable section. The smallest complete example that does something real, then the common variations. For a CLI, the main commands with their important flags; link to `--help` output or reference docs for the rest.

## Configuration

When the project reads env vars or a config file. A table with name, purpose, whether it is required, and the default. Take the list from `.env.example` and the code's env reads; if the list is long, document the ones needed to run locally and link the full source.

| Variable | Required | Default | Purpose |
|---|---|---|---|

## Scripts

When the project has more than a few scripts. A table of command and what it does, copied from the manifest, `Makefile` or task runner, never from memory.

## Architecture or how it works

When the project has moving parts a contributor must understand before changing it. A short map: the main components, how a request or job flows through them, where state lives. Keep the directory tree to the top two levels with a one-line note per entry. Draw a diagram only of a flow you traced in the code. Link to the schema, migrations or design docs instead of reproducing them.

## Testing

When tests exist. How to run all of them, one file, and anything the tests need (a database, env vars, a build step). How to write tests belongs in `CONTRIBUTING`, not here.

## Deployment

Only when the repo contains deploy config or a deploy workflow. Describe the deploy that config defines: the target, the command or trigger, the required secrets by name, how to roll back if the config supports it. With no deploy config, leave the section out; if the user asked for one, write a `TODO:` that names what is missing.

## Troubleshooting

Only for problems this project actually has: workarounds in CI, version pins with a comment explaining them, recurring issues, known platform quirks in the code. Each entry is the symptom as the reader sees it (the error text), the cause, and the fix. Generic advice that fits any project is noise.

## Contributing

When the project accepts contributions. The workflow in a few lines, or a link to `CONTRIBUTING.md` if it exists.

## License

When a license file exists. The license name and a link to the file.
