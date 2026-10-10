notes: search API latency work (Q3)

- goal: p99 under 150ms for /search. it was 480ms in July. now 90ms.
- how we measure latency: time from the API server receiving the request to the last byte of the response sent. p99 over a 24h window, from the server's own histogram. client network time is NOT included.
- cause: N+1 queries. for every result (we return 40 per page) we ran one query to load its tags. 40 queries x ~6ms each = ~240ms just on tags at p99.
- first try: put a Redis cache in front of the tags query. barely helped, p99 went 480 -> 430. reason: each Redis lookup is still a network round trip, ~2ms in our cluster, and we still did 40 of them per request (~80ms), plus misses fall through to the db anyway.
- what worked: load tags for all 40 results in one query (WHERE result_id IN (...)), plus an in-process map from tag id to tag name. there are ~12,000 tags, ~60 bytes each, so the map is ~720KB per server process.
- memory per process went from 310MB to 311MB. throughput (req/s per instance at 60% CPU) unchanged within our run-to-run noise of about 3%.
- the in-process map refreshes every 5 minutes, so a renamed tag can show its old name for up to 5 minutes. product said that's fine.
- status: batch loading is on for everyone. the in-process map is behind a flag, default ON since release 3.2.
- why we stopped: of the remaining 90ms, about 70ms is the search engine ranking the query. the API side is now ~20ms. making the API faster won't move p99 much; the ranking work belongs to the search team.
- audience: backend engineers on other teams, who know SQL and caching but not our service.
