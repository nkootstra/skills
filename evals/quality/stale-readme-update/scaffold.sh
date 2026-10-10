set -e
cat > 'README.md' <<'FIXTURE_EOF'
# Ledger API

Ledger API records double-entry transactions for the Acme finance team and exposes balances per account.

## Why double-entry

Every transfer writes two rows, a debit and a credit, in one database transaction. A balance is always the sum of its rows, so it can be recomputed from history and audited line by line. We chose this over storing running balances after the March 2025 reconciliation incident.

## Getting started

```sh
npm install
cp .env.example .env
npm run dev
```

## Configuration

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Postgres connection string |
| `REDIS_URL` | Cache for balance lookups |

## Tests

```sh
npm test
```
FIXTURE_EOF
cat > 'package.json' <<'FIXTURE_EOF'
{
  "name": "ledger-api",
  "private": true,
  "type": "module",
  "scripts": {
    "start:dev": "node --watch src/server.js",
    "start": "node src/server.js",
    "test:unit": "node --test test/",
    "db:migrate": "node scripts/migrate.js"
  },
  "dependencies": { "fastify": "^5.0.0", "pg": "^8.13.0" }
}
FIXTURE_EOF
cat > 'package-lock.json' <<'FIXTURE_EOF'
{
  "name": "ledger-api",
  "lockfileVersion": 3
}
FIXTURE_EOF
cat > '.env.example' <<'FIXTURE_EOF'
DATABASE_URL=postgres://localhost:5432/ledger
PORT=3000
FIXTURE_EOF
mkdir -p 'src'
cat > 'src/server.js' <<'FIXTURE_EOF'
import Fastify from 'fastify';
import pg from 'pg';

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
const app = Fastify({ logger: true });

app.get('/accounts/:id/balance', async (req) => {
  const { rows } = await pool.query('select coalesce(sum(amount), 0) as balance from entries where account_id = $1', [req.params.id]);
  return rows[0];
});

app.listen({ port: Number(process.env.PORT ?? 3000) });
FIXTURE_EOF
mkdir -p 'scripts'
cat > 'scripts/migrate.js' <<'FIXTURE_EOF'
import pg from 'pg';
const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
await pool.query('create table if not exists entries (id serial primary key, account_id int not null, amount numeric not null, created_at timestamptz default now())');
await pool.end();
FIXTURE_EOF
