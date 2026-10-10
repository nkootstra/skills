---
name: write-prose
description: Draft or edit substantive prose with a clear argument and a natural voice, including articles, explanations, data reports, commit messages and PR descriptions. Use whenever the user wants a draft, rewrite or edit of a blog post, essay, explanation, report, changelog piece, commit message or pull request description; says a text reads like AI wrote it, sounds generic, buries the point or overclaims; or hands over notes to turn into prose without inventing facts. Not for ad copy, social posts, press releases, translations, summaries or code.
metadata:
  author: Niels Kootstra
  version: "1.0.0"
---

# Write Prose

Infer audience, purpose, format, length, and factual constraints from the request. Preserve meaning, certainty, terminology, citations, and house style. In a targeted edit, preserve unaffected claims and conclusions; removing a generalization does not require weakening the author's own conclusion. Do not invent evidence, experience, quotations, motives, results, or reasoning. A cause, justification, or generalization the source does not state is an unwarranted inference and counts as invented: leave it out or ask about it. Do not write it and then flag it in a note.

## Match the work to the request

For a light edit (wording, a passage, a quote), make the minimal diff: change only the sentences a rule below hits, the way a good code review touches only the lines at fault, and leave every other sentence as the writer wrote it. When the user asks to restructure a draft or strip its narration, the minimal diff still holds for sentences no rule hits, but every match of the sweep goes, including clauses inside sentences you otherwise keep: a kept sentence that still narrates the journey has not been fixed. Apply Chesterton's fence before cutting: know what a sentence does for the piece (a judgment, an adjudication, a voice move) before deciding it is residue. For a draft or substantial rewrite, establish what the reader should understand, then choose a structure that fits the material. Do not force a problem-solution story or resolve uncertainty the source leaves open.

## Write the tests first

Before drafting or rewriting, write down the tests the finished piece must pass, as in test-driven development. Keep them in your working notes, not in the reply:

1. **Spine.** One sentence: what the reader should hold by the end. The opening states or sets it up; nothing before it is throat-clearing.
2. **Provenance.** Every fact, number, quote, cause and reason in the draft traces to a line of the source, and every count the prose states ("three defenses", "two reasons") matches the items it lists. List the source lines you will use.
3. **Ending.** The last paragraph carries the piece's most consequential sentence: a consequence, a cost, a decision, or the one open question the source leaves, stated once. Test it by deleting the last paragraph: if nothing of consequence is lost, it was a recap or a trailing aside, and the ending has to be rewritten, not trimmed. A closing section that lists the findings or hunches again fails, even under a fresh heading such as "Where this leaves me". When the notes state a conclusion, the ending earns it with its consequence instead of repeating it as a slogan.
4. **Genre.** For a data report, explainer, or other genre in [Adaptation](references/adaptation.md), its checklist items.

Draft, then run each test against the text and fix what fails before returning it. A draft that passes every test but reads worse than the source is also a failure: the tests check integrity, not voice.

| Need | Read |
| --- | --- |
| Structure for a genre, audience, or length | [Adaptation](references/adaptation.md) |
| A voice, pacing, explanation, or argument problem | The relevant section of [Style system](references/style-system.md) |
| Machine-drafted text, self-commentary, portable one-liners, unsupported closure, or buried openings | [Residue checks](references/residue-checks.md) |
| Calibration for a weak passage | [Examples](references/examples.md) |
| A piece that explains how something works or why it was built that way: an engineering article, system-design explainer, deep-dive, incident write-up, concept essay | [Explaining](references/explaining.md) |
| A commit message or PR description | [Commits and PRs](references/commits-and-prs.md) |

For a draft or a rewrite of existing text, always read [Residue checks](references/residue-checks.md) before returning the result. When the piece is a genre with its own structure (a data report, an explainer, a technical article, an essay, a changelog piece), also read [Adaptation](references/adaptation.md) before drafting. When the piece's job is to make a reader understand a system, mechanism, result, or concept, also read [Explaining](references/explaining.md) before drafting and use its checks as part of test 4. Read the other references when they help with the specific writing decision. This skill covers substantive prose, commit messages and PR descriptions, not ad copy, social posts, press releases, translations, summaries, or code.

## Core writing rules

- Open on the subject. Add background when the reader needs it. Put the bottom line first in the reader's own words: for a reader who doesn't know the term, lead with the problem or the action in plain language and bring in the term only after the problem has been shown.
- Use concrete nouns, active verbs, and visible reasoning. Explain relationships rather than relying on adjectives or claims of importance.
- Give each paragraph one job. Vary sentence length naturally. Cut lines that only repeat the previous point in a more quotable form; keep a striking line when concrete evidence earns it.
- Add examples and technical detail when they improve understanding. Keep claims within the evidence, and represent alternatives fairly.
- Keep personal evidence with “I.” Do not assign experiences to the reader through “you” or “we.”
- Use no em dashes in authored prose. Preserve the punctuation of exact direct quotations.
- End on the consequence, decision, or uncertainty that the material supports.

## Check and return

Check factual integrity and the issues relevant to the requested edit: argument, structure, explanation, voice, rhythm, or compression. Combine checks where practical; a short edit does not need seven separate passes. Stop when the requested text is complete and supported.

Before returning a draft or rewrite, sweep it sentence by sentence and delete or convert what survives from the writer's process instead of serving the reader:

- throat-clearing: a running start before the spine (bottom line up front)
- arrival and discovery narration: "it turned out", "I finally saw", "surprisingly", "what I learned was", "I didn't expect". A failed approach whose reason explains the mechanism stays, restated as a fact about the system
- thinking out loud: "one might wonder", "this raises the question", "I used to wonder". A question that voices the reader's objection and is answered by the next sentence is not thinking out loud; keep it
- leftover hedges: "I think", "I believe", "in hindsight" on the writer's own findings and their explanation of them. Uncertainty the source has (suspected, partial, possibly coincidental) stays, stated precisely, and so does a hedge on a generalization about other people or teams
- metadiscourse, text about the text: self-rating ("the cleanest finding", "the good part is"), signposting ("then there's", "the deeper half of this") and epistemic labels ("the open question is", "two things stay provisional"). Replace each with the fact it points at
- tautology: a sentence that restates the previous one in other words or at a higher register, including a quotable line after the literal claim. Keep one version
- quote characterization: "X put it best", "the complaint was unanimous"
- lessons assigned to the reader: "you will", "every team faces", "do X". Phrase a lesson as what the writer saw or would offer, not as an instruction
- unwarranted inference: a reason, cause or generalization with no source line behind it (test 2)
- the ending: if the last paragraph summarizes, moralizes or calls to action, cut it and end on the paragraph before, or on the consequence, cost or open question the material supports (test 3)

Apply the deletion test from the residue checks to each match: if the argument stands without the sentence, cut it or turn it into the fact it pointed at. The sweep removes process, not personality: keep the writer's casual phrasing, fragments, concrete details and asides that carry the voice. When the input is the writer's own draft, most sentences should come back unchanged.

Return finished prose first unless analysis is requested. Keep distinctive authorial choices that serve the piece. Note consequential gaps or assumptions only when useful; omit a routine edit list.

## Companion skills

- **write-readme**: hand off when the text is a project's README or setup documentation, which has to be built from what the repo contains before it can be written well.
