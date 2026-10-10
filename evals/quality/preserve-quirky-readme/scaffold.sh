set -e
cat > 'README.md' <<'FIXTURE_EOF'
# Gull

[![CI](https://github.com/acme/gull/actions/workflows/ci.yml/badge.svg)](https://github.com/acme/gull/actions/workflows/ci.yml)

Gull steals your screenshots from Slack threads and files them in a folder, like a seagull with a filing habit.

## Why the name

Our first prototype ran on a laptop at the beach and a gull walked off with the sandwich next to it. The name stuck; the sandwich did not come back.

## Running it

```sh
npm install
npm run serve
```

Then open http://localhost:4000.

## FAQ

**Does it read my DMs?** No. It only sees channels you invite it to.

**Where do the files go?** Into `./gull-inbox`, one folder per channel.
FIXTURE_EOF
cat > 'package.json' <<'FIXTURE_EOF'
{
  "name": "gull",
  "version": "1.2.0",
  "scripts": {
    "dev": "node src/server.js",
    "test": "node --test"
  },
  "dependencies": { "@slack/bolt": "^4.1.0" }
}
FIXTURE_EOF
cat > 'package-lock.json' <<'FIXTURE_EOF'
{
  "lockfileVersion": 3
}
FIXTURE_EOF
mkdir -p 'src'
cat > 'src/server.js' <<'FIXTURE_EOF'
import bolt from '@slack/bolt';
import { mkdir } from 'node:fs/promises';

const app = new bolt.App({ token: process.env.SLACK_BOT_TOKEN, signingSecret: process.env.SLACK_SIGNING_SECRET });
const inbox = process.env.GULL_INBOX ?? './gull-inbox';

app.event('file_shared', async ({ event }) => {
  await mkdir(`${inbox}/${event.channel_id}`, { recursive: true });
});

await app.start(Number(process.env.PORT ?? 4000));
FIXTURE_EOF
mkdir -p '.github/workflows'
cat > '.github/workflows/ci.yml' <<'FIXTURE_EOF'
name: ci
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22 }
      - run: npm ci
      - run: npm test
FIXTURE_EOF
