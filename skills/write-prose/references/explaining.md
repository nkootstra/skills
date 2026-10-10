# Explaining technical knowledge

Use this reference when the piece exists to make a reader understand how something works or why it was built that way: an engineering article, a system-design explainer, a performance or debugging deep-dive, an incident write-up, a concept essay. Each technique is phrased as a check the draft can pass or fail. Use the ones the material supports; never invent a number, trace, or tradeoff to satisfy a check. When the source lacks what a check needs, leave the device out or ask for the missing fact.

## Introduce concepts

- **Problem before name.** Show the behavior, failure, or need first, then give it a name. A term the reader meets before they have seen what it names is jargon even when defined. Check: every coined or specialist term appears after the paragraph that shows the thing it names.
- **First use is the definition site.** Terms and headline numbers usually first appear in the opening, so that is where they get defined. Give a metric's definition in the same sentence as its first number or the next one, and keep a label (a pattern name, an acronym, a percentile) out of the opening unless the opening also says what it means. For a non-specialist reader, open on the problem in their own terms and bring in the term after it.
- **Define by job, in the same sentence.** Gloss a term with what it does, in a clause, at first use: "the write-ahead log, a file where every change lands before it touches the table". Put the specialist label after the plain description when the reader may not know it: "a fingerprint of the TLS handshake (JA3)". Expand an acronym once. Mark a local coinage as local: "what the team calls the cold path".
- **Nearest neighbor, one difference.** Define a new concept by the familiar thing it most resembles and the one axis where it differs: "a shard splits data by key; a cell splits the whole stack by blast radius". Check: each central new concept has a sentence that says what it is not.
- **Connect to what the reader already does.** After describing an unfamiliar process, name the familiar workflow it resembles and the one thing that changes.
- **Make the concept testable.** For each key idea, give the reader a symptom they could observe or a question they could ask of their own system: "if an on-call engineer needs a spreadsheet to know which service owns an alert, the ownership model has failed". An abstract principle with no test stays abstract.

## Show the mechanism

- **Trace one case end to end.** For a system with several parts, follow a single request, job, or event through it in numbered steps, then state the rule the trace shows ("no step after 3 writes to the primary"). Check: the piece has at least one complete trace, and the trace is followed by the invariant it demonstrates.
- **State the invariant before the change.** Before describing a new design, name the rule the old design obeyed that the new one must keep (ordering, exactly-once, no data loss), then show how the new design keeps it.
- **Walk the failure.** For concurrency, caching, or recovery problems, write the failing sequence as 3 to 5 short steps ending in a named bad state ("Suppose the worker reads the lease, pauses for a GC, ..."), and only then the fix.
- **Classify, then map.** When the right strategy depends on the case, name the property that sorts the cases (rate of change, size, trust level), list the classes, and give each class its treatment. Check: no class is left without one.
- **Constraint, then decision, in one paragraph.** Each constraint the system lives under sits next to the design choice it forced. A list of constraints in one place and the choices in another makes the reader do the joining.

## Make numbers explain

- **Define the metric before the number.** Say what is measured, from which event to which event, and which percentile or aggregate: "latency here is keypress to rendered results, at p99". A number with an undefined metric is a decoration.
- **Show the arithmetic.** When a number is derived, put the derivation inline so the reader can check it: "40 bytes per entry × 2 million entries is 80 MB, which fits in memory on the smallest instance".
- **Translate into a familiar unit.** Give one comparison the reader already judges: what a standard component handles, how long a familiar action takes, the size of a common file. A peak of 5 million requests per minute means little until it is set against the normal load or what one proxy can serve.
- **Predict, then measure.** Where the design implies a result, say what it should achieve and why before reporting what it did. A prediction that missed is worth keeping, with the reason.
- **Report what did not regress.** Next to the metric that improved, give the one that could have got worse (throughput, memory, error rate, cost) and say whether it moved beyond run-to-run noise.
- **Attach status and the remaining gap.** For each result say whether it is the default, opt-in, or experimental, and how far it sits from the best known number. A result without its status reads as a promise.

## Tradeoffs and limits

- **The option turned down.** Name the obvious alternative, what it would have broken or cost, and what the chosen path gives up in return.
- **Where the choice flips.** State the condition under which the rejected option would win: "restarting beats checkpointing while jobs finish in seconds; for jobs that run for minutes, checkpoint".
- **Who should not use it.** Bracket the audience by scale (the smallest and the largest realistic case) and name at least one situation where the approach is a poor fit.
- **Why the work stopped.** In an optimization or investigation story, say where the bottleneck moved and why further work would not pay.
- **A verdict for every listed method.** When the piece lists techniques, tools, or defenses, say for each whether it worked here and why. A list without verdicts is an inventory.
- **Every outcome state.** When describing a test, check, or decision, cover the null and broken outcomes too: inconclusive is not passed, and a broken check is not a failed system.

## Orient the reader

- **Promise the questions, then answer them in order.** In a medium or long piece, the opening may end with one sentence naming two to four questions the piece answers. The sections then answer them in that order. This is a promise, not a preview: name questions, not section topics.
- **Plant a case, resolve it in the body.** Open with one concrete case whose outcome is left open (a request halfway through when a node dies), and resolve it by name in the section that explains the mechanism, not in the ending.
- **The reader's objection, answered at once.** A question heading or sentence is allowed when it voices the objection a reader would raise and the next sentence answers it with a fact, number, or decision. A question that only stalls is still thinking out loud.
- **Keep a dead end that teaches.** A failed approach stays when the reason it failed explains the mechanism. State the reason as a fact about the system ("the counter misses partial pages"), not as a story of the writer finding out.
- **Result first for an iterated system.** Describe the system as it stands before the history of how it got there, then give each earlier version's failure a name and resolve each named failure later.
- **Chronology only where order is the cause.** An incident write-up is organized by mechanism: what the problem was, why each defense worked or did not. Use a timeline only for the stretch where one action triggered the next.

## Figures and code

- A caption states what to conclude from the figure, and for a diagram, the likely misreading it rules out ("schematic: worker counts are not fixed").
- Before-and-after diagrams use the same parts and labels, so the one difference is the only thing that changes; the caption names it.
- A code sample states its own limits ("assumes one writer thread"). Show the smallest sample that runs or reads as real; elide the rest with a comment, not silently.

## Genre shapes

### Technical deep-dive (performance, debugging, a hard problem)

Constraint or goal, with its number and how it is measured; the budget derived from first principles; the design and its predicted effect; the measurement against the prediction, with what did not regress; dead ends that teach; why the work stopped and what remains.

### System-design explainer

The constraint that drives the design; the obvious options and why they fall short; the unit or boundary the design is built on, defined against its nearest familiar neighbor; the components, each with the constraint that forced it; one request traced end to end and the invariant it shows; the failure path; the tradeoffs with costs and flip conditions.

### Incident write-up

What happened and its scale against a normal baseline, in the first paragraph; how this incident differed from earlier ones; the mechanism of the attack or failure; each defense or fix with its verdict and cost; the option turned down; the state now, with a bounded claim about the future. A closing lessons list that restates the sections fails the ending test; keep only a lesson the sections did not already state.
