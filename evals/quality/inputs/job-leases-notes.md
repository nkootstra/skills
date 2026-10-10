notes: how background jobs run (for the onboarding wiki)

- readers: new hires in their first week. some are backend engineers, some are frontend or data folks who have never seen our job system.
- jobs live in a postgres table. a worker claims a job by setting worker_id and lease_expires_at = now + 30s, in one UPDATE ... WHERE lease_expires_at < now() so two workers can't claim the same job at the same time.
- while running, the worker extends the lease every 10s (heartbeat).
- if the worker crashes or loses its connection, it stops heartbeating, the lease runs out after at most 30s, and another worker can claim the job and run it again.
- consequence: a job can run more than once. so every job handler must be idempotent: the effect is keyed by job id (e.g. the "send invoice" handler checks invoices.sent_for_job_id before sending).
- the rule we rely on: a job's effect happens once, even if the job runs twice.
- known edge case: a worker that freezes for longer than 30s (we've seen long GC pauses) keeps running after its lease expired. a second worker claims the job. both run it. without the idempotency key, the customer would get two invoices. with it, the second run sees the key and does nothing.
- what we considered instead: a message broker (RabbitMQ) with ack-on-completion. we didn't, because brokers also redeliver on failure, so handlers would still need to be idempotent, and it's one more system to operate. postgres was already there.
- when this stops being the right call: jobs that take many minutes. a crash halfway means redoing all of it. for those (the nightly export, ~25 min) we split the work into chunks and record progress per chunk.
- most jobs finish in under 2 seconds.
