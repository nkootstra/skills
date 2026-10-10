# The Monitoring Essay

I ran maintenance for eight years. Then I ran a team that owns monitoring quality. I want to talk about what I looked at when I had to judge whether a monitoring change was good.

Then there's the map I ended up using.

It has three sections: does the change catch the failures it claims to catch, is it quiet when nothing is wrong, and is it cheap to maintain. Each section has a question, evidence, and a decision. It's not exotic. I want to defend plainness.

The artifact that convinced me is the one we asked to be scannable. It's a page for on-call engineers. The good part is measurable: median time to acknowledge went from nine minutes to three. The benchmarks are less charming. They're the part where the page fires on things nobody fixes, and we had eleven of those in a quarter.

Nadia put it best: "If I can't skim your alert in fifteen seconds, I'll skim it in thirty and learn nothing." The complaint was unanimous and differently worded. Alerts aimed at humans need a glance path. Screens aimed at dashboards need density. We stopped trying to make one page serve both.

There are two findings from the rollout quarter worth setting side by side, because they point at different pages.

- Speed: the median acknowledge drop of six minutes is real and held for six weeks. The cleanest thing we found, and the most expensive: it took two maintainers three weeks of deleting rules.
- Quiet: false-page rate went from 41% to 17% among the pages that survived review. Not zero. The remaining ones are the cases where we genuinely don't know yet.

The open question is whether the quietness holds as the fleet grows. Two things stay provisional: the fleet has doubled since June, and our rule-review cadence hasn't changed with it.

The deeper half of this read is about deleting rules. We deleted 214 of 700. Nothing in our tooling forced the deletion. It happened because the rollout asked "what does this rule buy you" in a form a maintainer had to answer in writing.

What sets the boundary on the optimistic version is the maintenance contract. Six minutes of acknowledge speed bought with zero maintenance budget is a loan. Our estimate: 0.5 engineer-days per month, forever, for this page shape.

Deleting rules is the actual lever. Dashboards are decoration until something is paging.
