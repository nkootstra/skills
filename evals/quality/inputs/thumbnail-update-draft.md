## Thumbnail Cache Rollout · Week 34

We're excited to share a pivotal milestone: the thumbnail cache is now live for all workspaces. This really matters for anyone who opens large boards.

Previously, every board load re-rendered each thumbnail from the original upload. With 400–600 images on a typical large board, that meant 9–12 seconds before the board was usable. The new system leverages a robust content-hash lookup, so a thumbnail transforms into a reusable asset the first time anyone renders it. Subsequent loads fetch the cached preview, the stored tile, or the saved snapshot instead of rendering again.

This means large boards now open in about 2 seconds at the median. The cache-first pipeline also cut renderer CPU by 63% during the Tuesday peak.

Two open risks. First, a cache entry is keyed on the file's hash, so an edited image gets a new entry and the old one lingers until the 30-day cleanup job removes it. Second, we haven't measured boards with more than 2,000 images yet, in the long run.

Honestly, this speaks volumes about how much the render path was costing us.
