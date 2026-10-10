# How we cut report generation from 40 minutes to 3

After months of digging, I finally understood why our monthly reports were so slow. It turned out the problem was not where anyone expected.

Each report filters orders by customer region. The region lives inside a JSON column, `orders.meta`, so every report scanned all 18 million rows and parsed the JSON of each one. That scan was 37 of the 40 minutes.

Why not just add an index? Because Postgres can't use a plain B-tree index on a key buried inside a JSON blob, and an expression index on `meta->>'region'` would have had to be rebuilt whenever the meta format changed, which happens about every quarter.

Surprisingly, our first fix made things worse. We cached parsed JSON in a materialized view, but refreshing the view locked the orders table for 6 minutes each night, and checkout writes queued behind the lock. We dropped it after two days.

What worked was moving region into its own column, `orders.region`, filled on write, with a normal index. The scan became an index lookup, and the report dropped to 3 minutes. The remaining 3 minutes are the PDF rendering, which we haven't touched.

## Lessons learned

- JSON columns are convenient but can hide expensive scans.
- Materialized views can lock tables.
- Moving region to its own column fixed it.

This is clearly where every data team is headed: away from JSON columns and back to plain schemas.
