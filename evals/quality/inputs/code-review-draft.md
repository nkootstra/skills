Notes for blog post on our code review process

- we started doing code review last year, before that we just merged stuff directly. honestly it was fine when it was 2 of us but then we grew
- the main thing people worry about is that review is slow. it can be. but the slowness is usually a signal not the disease
- we do async review, no meetings. comments on the PR. author responds or fixes
- the best reviews we've had were the ones where someone caught a real bug not a style nit. one time sarah caught a race condition in the sync code that would've lost data. that was the moment we all believed
- rule of thumb: review for the thing that's hardest to fix later. style you can fix anytime. an architectural decision or a data migration is expensive to change later
- we set a rule: if you open a PR you review one. keeps the queue moving. feels fair
- nobody likes being told their baby is ugly. tone matters. say what's wrong and why, not "you should have done X"
- reviewer: you are the second pair of eyes, not the boss. author owns the change
- we don't require review for tiny docs/typo changes. judgment call
- tools: github, we tried other tools but github was fine
- what makes a review good: specific comments, linked to the code, asks questions not demands
- deadline stuff, sometimes we skip review for hotfixes and regret it sometimes
- conclusion: review is not a gate, it's a habit