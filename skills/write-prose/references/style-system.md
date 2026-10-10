# Style system

## Voice and tone

Sound like a thoughtful practitioner explaining something they understand. Be confident about demonstrated claims and candid about uncertainty. Favor intellectual generosity over point-scoring. Keep the prose conversational through direct syntax and reader awareness, not slang or forced informality.

Avoid sales language, inflated stakes, empty superlatives, false inevitability, and claims that something is “revolutionary,” “seamless,” or “powerful” without showing the underlying fact. Avoid reflexive hedging too: qualify the claim precisely instead of surrounding it with timid language.

## Openings

A strong opening creates useful forward pressure. Begin with one of these when appropriate:

- an observable fact whose significance is not yet obvious
- a claim the piece will earn
- a specific moment that contains the larger issue
- a tension between two desirable goals
- a question precise enough to investigate
- a familiar assumption followed by the detail it misses

Move quickly from the hook to the real subject. Do not begin with dictionary definitions, sweeping history, “in today’s world,” generic importance claims, or a preview of everything the piece will cover. A single sentence naming the two to four questions the piece answers, in the order it answers them, is a promise rather than a preview; see [explaining.md](explaining.md).

## Sentence rhythm

Let syntax reflect thought. Use longer sentences to connect dependent ideas and shorter ones to mark a turn, boundary, or consequence. Keep the subject and verb close when a sentence carries technical detail. Prefer coordination only when the ideas truly have equal weight.

Use fragments rarely and intentionally. Avoid strings of one-line paragraphs, repeated rhetorical questions, slogan-like triads, and the predictable cadence of claim-colon-list. Read aloud for accidental repetition and synthetic punchiness.

Do not use em dashes. They are the most visible signature of AI-flavored prose and mechanical pacing: they let a sentence avoid deciding how two thoughts relate, so the writing reads as a series of dramatic beats instead of reasoned steps. Write the relationship with a period to separate, a colon to introduce, a comma to attach, or a restructure that makes the connection explicit. Preserve an em dash only inside a direct quotation that the source actually wrote.

## Paragraph construction

Give each paragraph a dominant function: claim, explanation, evidence, example, qualification, transition, or consequence. A paragraph may perform a second function, but it should not contain an entire essay in miniature.

Start a new paragraph when the reasoning changes direction, scale, evidence type, or speaker perspective. Keep a dense paragraph intact when splitting it would obscure a single continuous mechanism. Use one-sentence paragraphs only when the sentence genuinely deserves isolation.

## Transitions

Build transitions from logical relationships. Useful forms include:

- “That works while…” to introduce a boundary condition
- “The distinction matters because…” to connect definition to consequence
- “At small scale… At larger scale…” to shift scope
- “This explains the symptom, but not…” to deepen an inquiry
- “The practical result is…” to return from mechanism to effect

Do not rely on “moreover,” “furthermore,” “it is worth noting,” or repeated preview language to simulate coherence.

## Explanatory technique

Prefer a mental model over an inventory. Identify the few entities involved, how they interact, and what changes under different conditions. Expose intermediate steps when the conclusion would otherwise look magical.

Use analogy only when its correspondence is clear; state where it stops matching if the limitation matters. Test a comparison before keeping it: if deleting it leaves the meaning intact, if the shared mechanism is never named, if different topic nouns would drop in unchanged, or if it merely restates the literal sentence nearby, cut it. End an extended metaphor once it stops producing a new inference; continue it only when each return pays a consequence the literal language could not. Use examples as evidence or clarification, not decoration. For procedures, explain checkpoints and failure states as well as the happy path.

Move deliberately across three layers:

1. observation: what the reader can see
2. mechanism: what produces it
3. implication: why it changes a decision or understanding

Not every passage needs all three, but unexplained jumps between them create weak prose.

## Argument development

Make the claim no broader than the support. Distinguish fact, inference, judgment, and recommendation. Order reasons by dependency or force rather than by the order in which they occurred to the writer.

When reframing a problem, first show why the initial framing is reasonable. Then identify the evidence it cannot explain and offer a framing with greater explanatory power. Do not use a reframe merely to sound contrarian.

Vary argumentative form. Causal chains are useful when cause is genuinely at issue, but other pieces may depend on classification, comparison, accumulation of evidence, first-principles derivation, chronological discovery, or close interpretation.

## Examples and evidence

Choose the smallest example that preserves the important constraint. Prefer examples with visible consequences. When using numbers, give a baseline, denominator, time frame, or comparison when needed to interpret them.

In data-driven pieces, make the baseline structural: compare every headline number against a stated cohort, prior period, or control, and put the sample size next to the claim it qualifies. Attach each caveat to the finding it limits, followed by why the finding survives.

Do not fabricate specificity. If evidence is absent, write a bounded claim, mark a placeholder, or ask for the missing fact. Separate illustrative scenarios from actual events. Cite or attribute when the genre and stakes require it.

## Objections and alternatives

Address the strongest plausible objection, not a convenient weak version. Place it near the claim it challenges. A useful response may rebut it, concede it, distinguish contexts, or revise the claim.

Describe alternatives by their real advantages, costs, and operating assumptions. Avoid declaring a universal winner when the evidence supports a contextual choice.

## Technical depth

Choose detail by reader need:

- orientation: define the system and why it matters
- working understanding: explain components, interactions, and common failure modes
- implementation: provide interfaces, constraints, edge cases, and verification
- expert analysis: surface tradeoffs, invariants, performance characteristics, and unresolved questions

Do not confuse code, jargon, or low-level detail with rigor. Rigor means the explanation supports the claim and survives obvious questions.

## Endings

End with the most consequential thing now visible: a decision, changed mental model, cost, practical instruction, or unresolved tension. Keep the ending proportionate: usually one paragraph, often one sentence. The ending must add something the piece has not yet said; a closing paragraph or section that restates earlier points, however compactly, is a recap and gets cut. For an explainer or product piece, the ending is what changes for the user, stated concretely, not a final metric or a call to action.

End one step before the material settles. Do not resolve a tradeoff the evidence leaves open, convert uncertainty into a finished lesson, turn one experience into a universal lesson, or give every recurring image a ceremonial callback.

Avoid “in conclusion,” generic inspiration, sudden calls to action, a closing heading that repeats the title's thesis, and summaries that replay earlier sections.

## Editing rules

- Replace abstract nominalizations with actors and actions when accuracy permits.
- Cut openings that delay the first meaningful sentence.
- Remove tautological sentences: ones that repeat the previous sentence or the paragraph's point in other words without extending it.
- Turn vague intensifiers into evidence or delete them.
- Resolve ambiguous pronouns and buried antecedents.
- Keep parallel ideas grammatically parallel.
- Prefer positive statements, while preserving necessary exceptions.
- Check that headings name real distinctions and are not excessive.
- Prefer a heading that states the finding over one that only names the topic.
- Retain useful texture, wit, and individual phrasing; clarity is not sterility.

## Anti-patterns

Reject these unless the genre specifically calls for them:

- generic scene-setting and universal claims
- feature lists disguised as explanation
- rigid problem → agitation → solution copy
- a causal formula applied without causal evidence
- fake quotations, anecdotes, metrics, or personal experience
- breathless fragments and a one-sentence-paragraph drumbeat
- excessive headings that break a short piece into scraps
- jargon introduced before the underlying idea
- false binaries and straw-man alternatives
- repeated conclusions and redundant summaries
- “not just X, but Y” used as a habitual flourish
- meta-commentary about what the piece is about to say
- polished language that removes the author's actual point of view
- a punchline, metaphor, or coinage at the end of every paragraph; conspicuous voice moves need spacing more than presence
- research that certifies a settled conclusion instead of answering a live question; cut studies that change no judgment
- aphoristic lines portable enough to move to an unrelated essay with the topic nouns swapped; see [residue-checks.md](residue-checks.md)
