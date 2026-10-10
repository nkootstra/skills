set -e
cat > 'package.json' <<'FIXTURE_EOF'
{
  "name": "invoice-worker",
  "private": true,
  "engines": { "node": ">=20" },
  "scripts": {
    "dev": "node --watch src/index.js",
    "start": "node src/index.js",
    "test": "node --test"
  },
  "dependencies": { "pg": "^8.13.0", "stripe": "^17.0.0" }
}
FIXTURE_EOF
cat > 'yarn.lock' <<'FIXTURE_EOF'
# yarn lockfile v1
FIXTURE_EOF
cat > '.nvmrc' <<'FIXTURE_EOF'
18
FIXTURE_EOF
cat > '.env.example' <<'FIXTURE_EOF'
DATABASE_URL=postgres://localhost:5432/invoices
FIXTURE_EOF
mkdir -p 'src'
cat > 'src/index.js' <<'FIXTURE_EOF'
import pg from 'pg';
import Stripe from 'stripe';

const db = new pg.Pool({ connectionString: process.env.DATABASE_URL });
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const interval = Number(process.env.POLL_INTERVAL_MS ?? 60000);

async function tick() {
  const { rows } = await db.query("select id, customer_id, amount_cents from invoices where status = 'pending' limit 50");
  for (const inv of rows) {
    await stripe.invoiceItems.create({ customer: inv.customer_id, amount: inv.amount_cents, currency: 'eur' });
    await db.query("update invoices set status = 'sent' where id = $1", [inv.id]);
  }
}

setInterval(tick, interval);
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
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: yarn }
      - run: yarn install --frozen-lockfile
      - run: yarn test
FIXTURE_EOF
