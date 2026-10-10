Feature: Background sync for Acme Notes (offline notes app)

Status: shipped in v2.4, July 2026

What changed:
- Notes are stored locally on the device (SQLite). Previously, sync was manual: you hit "Sync" or it synced when the app opened.
- Now sync runs automatically in the background whenever the device has a network connection, and when changes are made on one device they propagate to the others without the user doing anything.
- Conflict resolution: last-writer-wins per note, but a merged "version history" is kept so nothing is silently overwritten. Deleted notes are tombstoned for 30 days in case of accidental deletion.
- Offline-first: editing works with no connection; changes queue and sync when back online. No data is lost on app kill.
- Privacy: sync goes through our servers encrypted in transit; notes are not readable by us in plaintext (E2E optional for paid plan).

Why: users on multiple devices (phone + laptop) complained that they'd edit on one device and forget to sync, then lose track of which version was current. Manual sync was the #1 support request for two quarters.

Numbers: sync failures reduced from 11% of sync attempts to 0.4% after launch; support tickets about "lost edits" down ~70%.

Pricing impact: E2E sync is a paid-plan feature; background sync itself is free for all users.