# What I Learned From Watching Our Data Get Deleted

For a long time I've been uneasy about backups, and last month I finally had a window into why. It started, as these things do, with a Tuesday morning and a slack message I'll remember for a while.

It was 7:42am. I was on call. I had coffee going. My phone buzzed. I remember standing in the kitchen, not sitting, and thinking: is this going to be one of those days.

The week before the incident, honestly, nothing about our posture was unusual. We had, like most teams, a vault of tools nobody fully trusted. I spent months, after months, digging through runbooks at odd hours, quietly getting more and more disturbed by what I found, or rather didn't find. Surprisingly, the thing that worried me most wasn't any single tool. It turned out to be a gap between two of them.

It took me a while to see it clearly, but here is what I finally understood, after a lot of restless digging: our restore test asked the database to restore, and our monitoring asked the database whether the restore was finished. Two different systems. Two different definitions of finished. Neither had ever met the other.

I didn't expect to find that. What I learned was that the restore job writes a completion record, and the monitor checks for the word written, not the record. The restore had failed on a dependency, three Tuesdays running. The monitor said fine every time.

One might wonder how three separate on-call rotations missed it. I think it's because the failure lived in a place neither tool's vocabulary covered, and I believe this is the case in most shops, most of the time. After much searching I concluded that the seam between two confident systems is where outages live.

The fix itself was small. RestoreShip now watches for the completion record, and pages if eighteen minutes pass without one. What I noticed in the following month now seems, in hindsight, almost predictable, but at the time it felt like luck turning: two more silent failures caught before they could lie.

This raises the question of definitions in your own stack. What does done mean where you work. I used to wonder if restore-testing was box-checking. Now I would answer differently.
