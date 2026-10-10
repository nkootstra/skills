# Small Ships

I've shipped three rewrites and lived to regret each one. So I want to argue for the boring thing: breaking big changes into small ships, and staging each one where it can be turned off.

A plan without a rollback is just a wish. That's the sentence I keep coming back to.

The literature on staged rollouts is clear: you deploy to 1% and halt before it hurts everybody. The best big change is the one you never make. That's not cynicism, it's scheduling.

Why small? Because a small change tells you the truth in six hours, while a rewrite tells you in six months that your original guess was wrong. What gets measured gets managed. And big bangs are managed closely: war rooms, exec updates, popcorn.

When you stage ships, each one is reviewed by someone who can still hold the whole change in mind. Nobody reviews a 40k-line PR with judgment. They eyeball it and approve. Trust is the engine of velocity, and it compounds.

In 2023 we rewrote an ingest pipeline instead of adding a partition step as we'd discussed. Committed in March. Cost 4.5 months and two engineers, worse p99 at launch, one quarter with customer escalations. Parity arrives in month four. What killed us wasn't ambition; it was arithmetic we refused to do in March. If we had added the partition step first (two weeks, PR #4821), the traffic doubled in Q3 without incident.

You get the picture. Big firms stage and so do small firms. The upshot: stage your big change into five small ones, each shippable, each reversible, and let the fifth tell you what the first four couldn't have.

At the end of the day, shipping is a conversation with the dark side of your architecture. Have it in small sentences.
