set -e
cat > 'package.json' <<'FIXTURE_EOF'
{
  "name": "orbit",
  "private": true,
  "packageManager": "pnpm@9.12.0",
  "scripts": {
    "dev": "pnpm -r --parallel dev",
    "test": "pnpm -r test",
    "build": "pnpm -r build"
  }
}
FIXTURE_EOF
cat > 'pnpm-workspace.yaml' <<'FIXTURE_EOF'
packages:
  - packages/*
FIXTURE_EOF
cat > 'pnpm-lock.yaml' <<'FIXTURE_EOF'
lockfileVersion: '9.0'
FIXTURE_EOF
mkdir -p 'packages/api'
cat > 'packages/api/package.json' <<'FIXTURE_EOF'
{
  "name": "@orbit/api",
  "scripts": { "dev": "node --watch src/server.js", "test": "node --test" },
  "dependencies": { "fastify": "^5.0.0", "@orbit/shared": "workspace:*" }
}
FIXTURE_EOF
mkdir -p 'packages/api'
cat > 'packages/api/README.md' <<'FIXTURE_EOF'
# @orbit/api

HTTP API for Orbit. Serves `/missions` and `/missions/:id` on port 4000.

## Environment

| Variable | Default |
|---|---|
| `PORT` | `4000` |
| `ORBIT_DB_PATH` | `./orbit.sqlite` |
FIXTURE_EOF
mkdir -p 'packages/api/src'
cat > 'packages/api/src/server.js' <<'FIXTURE_EOF'
import Fastify from 'fastify';
import { missionSchema } from '@orbit/shared';
const app = Fastify();
app.get('/missions', async () => []);
app.listen({ port: Number(process.env.PORT ?? 4000) });
FIXTURE_EOF
mkdir -p 'packages/web'
cat > 'packages/web/package.json' <<'FIXTURE_EOF'
{
  "name": "@orbit/web",
  "scripts": { "dev": "vite", "build": "vite build", "test": "vitest run" },
  "dependencies": { "@orbit/shared": "workspace:*" },
  "devDependencies": { "vite": "^5.4.0", "vitest": "^2.1.0" }
}
FIXTURE_EOF
mkdir -p 'packages/web'
cat > 'packages/web/index.html' <<'FIXTURE_EOF'
<!doctype html><title>Orbit</title><div id="app"></div><script type="module" src="/src/main.js"></script>
FIXTURE_EOF
mkdir -p 'packages/web/src'
cat > 'packages/web/src/main.js' <<'FIXTURE_EOF'
fetch('http://localhost:4000/missions').then((r) => r.json()).then(console.log);
FIXTURE_EOF
mkdir -p 'packages/shared'
cat > 'packages/shared/package.json' <<'FIXTURE_EOF'
{
  "name": "@orbit/shared",
  "main": "src/index.js",
  "scripts": { "test": "node --test" }
}
FIXTURE_EOF
mkdir -p 'packages/shared/src'
cat > 'packages/shared/src/index.js' <<'FIXTURE_EOF'
export const missionSchema = { id: 'string', name: 'string', launchDate: 'string' };
FIXTURE_EOF
