---
name: design-critique
description: Structured, specific critique of interfaces, products, screens, prototypes and interactions. Use whenever the user asks for feedback on a design, says something "feels off" or "isn't quite right", wants to evaluate quality, compare versions, decide what to improve next, or define what "good" means for their product, even if they don't use the word critique. Covers design review, UX audit and heuristic evaluation. Also use when reviewing UI code output for visual or interaction quality.
argument-hint: "[screen, file, or URL]"
effort: high
metadata:
  author: Niels Kootstra
  version: "1.1.0"
---

# Design Critique

Good critique turns a vague reaction ("it feels nice", "something's wrong") into a specific, named observation with a cause. Vague feedback cannot be acted on; precise feedback can.

## Reference files

- Load [rubric.md](references/rubric.md) on the second and third passes, and whenever a finding needs a concrete check, a number, a severity level, or phrasing. It ends with a Nielsen heuristics sweep, the dark patterns to flag, and what not to file.
- Load [facets.md](references/facets.md) when drafting facets from what the user said, when the user's facets need sharpening, and before scoring or drawing the facet chart.
- Load [output-template.md](references/output-template.md) when writing the final report, when comparing two versions, or when feedback reads vague and needs rewriting.

## 1. Look longer than feels necessary

First impressions are shallow: they catch the obvious and move on. Before giving feedback, do a second and third pass deliberately looking for what was skipped the first time. Treat every reaction (hesitation, delight, irritation, confusion) as data worth explaining.

Walk the interface through these lenses and note anything that registers:

- **Hesitation**: Where would a user pause? Unclear consequences, lack of trust, unclear affordance?
- **Expectation gaps**: Where does the mental model break? What would the user assume happens, and what would have met that expectation?
- **Emotional shifts**: Where does the experience turn annoying, or unexpectedly pleasant? Pinpoint the exact moment and trigger.
- **Absence**: What is someone looking for that isn't there? Does it matter?
- **Assumptions**: What does the design assume about the user? What is hidden versus surfaced, and why?
- **Visual quality**: Cheap or crafted? Is type comfortable to read? Do colors cooperate or compete? Is there a clear hierarchy, or is everything fighting for attention? Are radii, alignment and spacing consistent?
- **Feel**: Fast or sluggish? Does it respond as expected or is there a subtle disconnect? Does it feel sturdy or fragile? Where does motion originate, and does that origin make sense?

Always state *why*. "The button feels weak" is not critique. "The primary button has the same visual weight as the secondary links, so the eye has no landing point" is.

## 2. Judge against defined facets of quality

Generic virtues (usable, reliable, consistent) are table stakes, not goals. Real quality is situational. Before evaluating, establish 3–6 **facets**: the specific qualities this product should be *perceived* to have by its users. Examples of the shape: "playful and tactile", "calm and trustworthy", "dense and expert-fast", "feels hand-made", "feels like it keeps growing".

If the project has a `.design/facets.md`, read it first: those are the agreed facets. Also read `.design/rejections.md` if present, one line per pattern the user has sent back before, and check for those explicitly.

If the user hasn't defined facets, propose a draft set based on what they've said about the product and audience, and ask them to confirm or adjust. Keep it short. Once confirmed, offer to save them to `.design/facets.md` so the next critique starts from the same bar; when the user rejects a pattern, offer to add a line to `.design/rejections.md`.

Then:

1. **Score** each facet on a simple scale (1–5 works well). Define the ends: 1 = the minimum you'd accept, 5 = the best you can imagine.
2. **Present** the scores as a radar chart or compact table, with one line of evidence per score.
3. **Rank** facets by importance. A low score on the top-ranked facet is a reason not to ship; a low score on the bottom one may be acceptable for now.
4. **Plan**: name the one or two facets to raise next and what concretely would move each up a point.

Facets also sharpen feedback language. Instead of "needs more work", say "this is solid but less playful than the previous version; it reads as a 2 where we were at a 4."

## 3. Critique what you can see

Critique the rendered thing, not the code. If you can render it (a browser MCP, Playwright, a dev server), screenshot it at desktop and phone widths and look before writing a finding. If you can't, say the critique is from code or description only, and keep visual claims to what the code makes certain.

## 4. Know where the floor is

Users silently compare everything to the apps they use daily, and anything below that bar gets dismissed without explanation. Say explicitly whether the work is below, at, or above the expected baseline for its platform. Meeting the bar is the floor, not the goal.

## Output format

Unless the user asks for something else:

1. **Overall read**: 2–3 sentences, including where it sits relative to the platform baseline.
2. **Observations**: specific findings, each with what, where, why it matters, and a suggested direction. Ordered by impact.
3. **Facet scores**: table or chart, with brief evidence.
4. **Next moves**: the 1–3 highest-leverage changes.

Be direct and kind. Praise what works with the same precision as problems.

## Companion skills

- **design-exploration**: when critique shows the concept itself is the problem (polish can't lift the top-ranked facet), go back to range and generate genuinely different directions instead of refining this one.
- **intentional-prototyping**: to test a proposed fix (timing, easing, spacing, an interaction) with live-tunable values before committing to it.
- **interface-polish**: for meeting the platform baseline, covering states and edge cases, and the pre-ship sweep once the direction is settled.
