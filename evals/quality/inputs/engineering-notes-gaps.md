# Raw notes: onboarding conversion drop

Home page → workspace created conversion.
Two months of digging. March-April 2025.
Baseline: 34% (Jan-Feb). Now: 27%. Steady decline across six weeks, not a cliff.

Things I can see:
- Gateway logs only. No client telemetry from before March (feature shipped late Feb). So "what users did before the drop" is inferred from logs where they got far enough to hit the gateway.
- Mobile share of signups rose from 22% to 31% over the same window. Coincidence? Our mobile flow has always been worse. Could be composition, not cause. Can't separate yet, no per-platform conversion before March.

Lead 1: scaffold step. March release changed the default template. Median time-to-first-successful-deploy went from 11 min to 26 min. But 26 min is the median *successful*. Failures there doubled.Template regression is my strongest suspect. Only tested with staged accounts, n=41.

Lead 2: did the same regression hit staged accounts (old template)? Yes, coordination also dropped for them. Hmm. But staged accounts are employees, they get stuck differently. Not conclusive.

Lead 3: DNS propagation during the odd CF incident (Apr 9-10) lines up with the steepest week. But that week is also when we sent the pricing email. I cannot separate these. No good natural experiment available yet.

Lead 4: docs overlap. People who opened docs during onboarding converted at 48% vs 19% who didn't. Direction obvious, causation unclear. We've known forever that doc-openers are self-selected. Don't over-claim because of it.

Negative result: A/B of progress meter (shipped Apr 18, n≈9k) showed no effect. Slightly negative, within noise. Killed my earlier hunch that people felt lost.

What I could NOT find:
- No exit surveys this quarter. Last run was Q3.
- Support tickets: only 14 mention onboarding directly. Not enough to hang a thesis on.
- No data on which step users actually leave at before March. Inferred: most abandonment happens between deploy attempt 1 and template editing, from session lengths. Inference, not measurement.

My hunches, low confidence: template regression is real and explains some of it. Mobile composition explains some. Something with the pricing email I haven't been able to rule out.

Unresolved: per-platform split. Email-cohort analysis needs billing data I don't have access to.
