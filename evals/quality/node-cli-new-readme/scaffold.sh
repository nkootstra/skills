set -e
cat > 'package.json' <<'FIXTURE_EOF'
{
  "name": "tally-cli",
  "version": "0.3.1",
  "description": "Count rows, words and unique values in CSV files",
  "license": "MIT",
  "type": "module",
  "bin": { "tally": "dist/cli.js" },
  "engines": { "node": ">=20" },
  "scripts": {
    "build": "tsc -p .",
    "test": "vitest run",
    "lint": "eslint ."
  },
  "dependencies": { "commander": "^12.1.0", "csv-parse": "^5.5.6" },
  "devDependencies": { "typescript": "^5.6.0", "vitest": "^2.1.0", "eslint": "^9.12.0" }
}
FIXTURE_EOF
cat > 'pnpm-lock.yaml' <<'FIXTURE_EOF'
lockfileVersion: '9.0'
FIXTURE_EOF
cat > '.nvmrc' <<'FIXTURE_EOF'
20
FIXTURE_EOF
cat > 'LICENSE' <<'FIXTURE_EOF'
MIT License

Copyright (c) 2026 Tally contributors
FIXTURE_EOF
mkdir -p 'src'
cat > 'src/cli.ts' <<'FIXTURE_EOF'
#!/usr/bin/env node
import { Command } from 'commander';
import { countRows, countUnique } from './count.js';

const program = new Command('tally').version('0.3.1');

program
  .command('rows <file>')
  .description('Count data rows, excluding the header')
  .option('--json', 'print the result as JSON')
  .action(async (file, opts) => print(await countRows(file), opts));

program
  .command('unique <file> <column>')
  .description('Count distinct values in a column')
  .option('--json', 'print the result as JSON')
  .option('--top <n>', 'also list the n most common values', '0')
  .action(async (file, column, opts) => print(await countUnique(file, column, Number(opts.top)), opts));

function print(result: unknown, opts: { json?: boolean }) {
  const color = !process.env.NO_COLOR;
  console.log(opts.json ? JSON.stringify(result) : format(result, color));
}

function format(result: unknown, color: boolean) { return String(result); }

program.parseAsync();
FIXTURE_EOF
mkdir -p 'src'
cat > 'src/count.ts' <<'FIXTURE_EOF'
import { parse } from 'csv-parse';
import { createReadStream } from 'node:fs';

export async function countRows(file: string) {
  let n = 0;
  for await (const _ of createReadStream(file).pipe(parse({ columns: true }))) n++;
  return { rows: n };
}

export async function countUnique(file: string, column: string, top: number) {
  const counts = new Map<string, number>();
  for await (const row of createReadStream(file).pipe(parse({ columns: true }))) {
    const v = row[column];
    counts.set(v, (counts.get(v) ?? 0) + 1);
  }
  const sorted = [...counts].sort((a, b) => b[1] - a[1]);
  return { unique: counts.size, top: sorted.slice(0, top) };
}
FIXTURE_EOF
mkdir -p '.github/workflows'
cat > '.github/workflows/ci.yml' <<'FIXTURE_EOF'
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm test
      - run: pnpm build
FIXTURE_EOF
