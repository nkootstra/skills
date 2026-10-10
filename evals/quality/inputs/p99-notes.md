notes for the sales team explainer: why we report p99, not average response time

- readers: our sales and account managers. not engineers. they get asked by customers "how fast is your API?" and some prospects compare our "average response time" with competitors'.
- our API last month: average response time 120 ms. p99 (the time that 99 out of 100 requests finish within) 1.8 seconds.
- what that means: 1 in every 100 requests takes 1.8 s or longer, even though the average looks fast. the average hides them because the other 99 are quick.
- a customer's dashboard page makes about 30 API calls to load. if each call has a 1 in 100 chance of being slow, the chance that a page load hits at least one slow call is 1 - 0.99^30, about 26%. so roughly 1 in 4 page loads feels slow, while the average says 120 ms.
- this is why a customer can complain "your product is slow" while our average looks great.
- we commit to p99 in our SLA: under 2 seconds. we don't commit to an average.
- what sales should say: quote p99, and explain it as "99 out of 100 requests finish within X".
