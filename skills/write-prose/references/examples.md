# Calibration examples

These examples demonstrate moves, not phrases to imitate.

## Opening

Weak:

> In today's rapidly evolving software landscape, performance is more important than ever.

Stronger:

> The page felt instant in testing. With a year of customer data, the same click took four seconds.

Why it works: it starts with an observable change and creates a precise question without announcing importance.

## Explaining a mechanism

Weak:

> The new cache dramatically improves performance and provides a seamless experience.

Stronger:

> The cache keeps the last successful result on the device. Returning users see that result immediately while the app checks for newer data in the background.

Why it works: it replaces praise with behavior and sequence.

## Word-level residue

Weak:

> Three takeaways. The new importer leverages a robust validation layer, and the spreadsheet transforms into clean records. This really matters for finance.

Stronger:

> The importer now rejects a row with a missing account number and names the row in the error, so finance fixes the spreadsheet before anything is saved.

Why it works: the count opener, the impressive verbs, the object acting on its own and the empty emphasis all give way to who does what and what it prevents. Any takeaway the notes actually support gets its own sentence where it applies; the rest go.

## Fair comparison

Weak:

> The old approach was brittle and could not scale.

Stronger:

> A single configuration file was the right tradeoff when five people changed it. It became risky when dozens of services began deploying independently: an edit for one service could invalidate settings for the rest.

Why it works: it explains both the earlier fit and the later boundary.

## Moving between abstraction and example

Weak:

> Small inconsistencies compound over time and create operational complexity.

Stronger:

> Small inconsistencies become policy. If one team records time in seconds and another in milliseconds, every shared report needs a conversion rule. The cost is not the conversion itself; it is remembering where the exception applies.

Why it works: the example makes the abstract claim visible, then extracts the deeper consequence.

## Handling an objection

Weak:

> Some may disagree, but this is clearly the best design.

Stronger:

> This design adds a network request to the first launch. That cost matters for offline tools. For a collaborative editor, however, the request also establishes the shared version that every later edit depends on.

Why it works: it concedes a real cost and narrows the judgment by context.

## Technical depth

Too shallow:

> Requests are retried automatically, making the system resilient.

Too deep for a product overview:

> The client applies truncated binary exponential backoff with full jitter, using a 2^n multiplier capped at 32 seconds.

Calibrated:

> Temporary failures are retried with increasing delays, so a brief outage does not become a flood of simultaneous requests. Permanent errors return immediately.

Why it works: it gives the governing mechanism and meaningful boundary without unnecessary implementation detail.

## Sentence rhythm

Flat:

> The import runs in the background. The user can close the tab. The server keeps processing. The results appear later.

Stronger:

> The import runs on the server, so closing the tab does not interrupt it. When processing finishes, the results appear in the workspace. The browser is no longer part of the job.

Why it works: dependent ideas are joined, while the final short sentence lands the changed model.

## Em dashes

Weak:

> We merged straight to main — which was fine for two people — but it stopped working when the team grew.

Stronger:

> We merged straight to main. That was fine for two people. It stopped working when the team grew.

Why it works: splitting into separate sentences makes each idea stand on its own and varies the rhythm; the em dash version hides the same logic behind a manufactured beat.

## Ending

Weak:

> In conclusion, we have explored the challenges, solutions, and benefits of the new system.

Stronger:

> The useful shift was not making each retry faster. It was removing retries from the path the user had to wait for.

Why it works: it ends on the insight earned by the explanation rather than replaying the outline.

## Short non-technical example

> A meeting does not become useful because everyone attends. It becomes useful when the people in the room can change the decision. Invite contributors whose knowledge alters the options and owners whose commitment alters what happens next. Send everyone else the result. Attendance is a cost; participation is the reason to pay it.

This uses a claim, distinction, practical rule, and compact ending without relying on a change-story formula.

## Compact technical example

> An offline indicator should answer a narrower question than “Is the internet working?” The application rarely knows that. It knows whether its last request reached this service, whether local changes are waiting, and when synchronization last succeeded. Showing those facts separately gives the user something actionable; collapsing them into a red dot turns several failure modes into one vague warning.

This moves from reframing to observable states and consequence. It introduces only the technical detail needed for the product decision.
