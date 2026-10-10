# Triggering eval cases

67 cases. `expected` is the skill that should load (or `none`); `also ok` lists other skills that may load without counting as a false positive.

| id | expected | also ok | difficulty | prompt |
|---|---|---|---|---|
| crit-01 | design-critique |  | direct | Can you critique the settings page in src/pages/Settings.tsx? Be specific. |
| crit-02 | design-critique |  | indirect | Something about our onboarding screen just feels off and I can't put my finger on it. What's wrong with it? It's in src/pages/Onboarding.tsx. |
| crit-03 | design-critique |  | indirect | Here are two versions of the pricing card (PricingA.tsx and PricingB.tsx in src/components). Which one is better and why? |
| crit-04 | design-critique |  | indirect | Before I show this dashboard to my manager tomorrow, tell me honestly what's weak about it. src/pages/Dashboard.tsx |
| crit-05 | design-critique |  | indirect | We keep saying our app should feel 'calm and trustworthy'. Can you score the current UI against that and tell me where it falls short? |
| crit-06 | design-critique | interface-polish | hard | Is the checkout flow in src/pages/Checkout.tsx good enough to ship, visually? Just give me your assessment, don't change anything. |
| crit-07 | design-critique |  | hard | Do a heuristic evaluation of the signup form in src/components/SignupForm.tsx. |
| crit-08 | design-critique |  | hard | My designer friend said the header 'has no hierarchy'. Is she right? What does that even mean here? src/components/Header.tsx |
| expl-01 | design-exploration |  | direct | Give me a few genuinely different design directions for an empty state on the projects page. |
| expl-02 | design-exploration |  | indirect | I need to design how users split a bill with friends in our app. What are some ways this could work? Don't build anything yet. |
| expl-03 | design-exploration |  | indirect | Our file upload is a boring dropzone. How could it be way better? I want options, not code. |
| expl-04 | design-exploration |  | indirect | I keep landing on the same layout for the landing page hero and it looks like every other SaaS site. Help me get out of that rut. |
| expl-05 | design-exploration | design-critique | hard | Here's my first idea for the notification center (src/components/Notifications.tsx). Before I commit, what else could it be? |
| expl-06 | design-exploration |  | hard | What would onboarding look like if it had no screens at all? |
| expl-07 | design-exploration | interface-polish | hard | The search component works but it's a 3 out of 10. Walk me through taking it to a 9, step by step, as ideas first. |
| expl-08 | design-exploration |  | hard | Brainstorm 10 concepts for a habit tracker's daily check-in. Make the later ones weird. |
| prot-01 | intentional-prototyping |  | direct | Prototype a card that flips over when you tap it, I want to see if it feels good. |
| prot-02 | intentional-prototyping |  | indirect | I want to dial in the spring on our drawer opening. Can you make something where I can tweak stiffness and damping live? |
| prot-03 | intentional-prototyping |  | indirect | Saw this effect on a site where the button kind of melts into a toast when you click it. How would I rebuild that? |
| prot-04 | intentional-prototyping |  | indirect | Make a quick throwaway page to test whether a swipe-to-archive gesture on list rows makes sense. Just gray boxes is fine. |
| prot-05 | intentional-prototyping |  | indirect | I can't decide on the shadow for the floating panel. Build me something with sliders for blur, offset and opacity so I can try values. |
| prot-06 | intentional-prototyping |  | hard | How did Linear do that command menu open animation? I want to recreate it to understand it. |
| prot-07 | intentional-prototyping | design-exploration | hard | Show me 12 random variations of this tooltip's entrance animation in a grid so I can pick one. |
| prot-08 | intentional-prototyping |  | hard | Before we build the real thing, I want to know if a radial menu is even understandable. What's the fastest way to find out? |
| pol-01 | interface-polish |  | direct | Polish the settings page so it feels premium. src/pages/Settings.tsx |
| pol-02 | interface-polish |  | indirect | We're launching Monday. Go through src/pages/Dashboard.tsx and make it feel finished: empty states, loading, errors, all of it. |
| pol-03 | interface-polish |  | indirect | The app works but looks like a hackathon project. Make the team members list in src/components/TeamList.tsx not look generic. |
| pol-04 | interface-polish |  | indirect | Add proper loading, empty and error states to the invoices table in src/components/InvoiceTable.tsx. |
| pol-05 | interface-polish | design-critique | hard | This is going in my portfolio. Make the project card component as good as it can possibly be. src/components/ProjectCard.tsx |
| pol-06 | interface-polish |  | hard | Build a settings page for notification preferences. It should feel native and high quality, not like a default template. |
| pol-07 | interface-polish |  | hard | Make the modal in src/components/Modal.tsx feel right: how it opens, closes, focus, escape, all the details. |
| pol-08 | interface-polish |  | hard | Clean up the dark mode on the marketing page, the cards look washed out and the screenshots glow. src/pages/Home.tsx |
| readme-01 | write-readme |  | direct | Write a README for this repo. |
| readme-02 | write-readme |  | indirect | Our setup docs are out of date. Fix them so they match what the project actually does now. |
| readme-03 | write-readme |  | indirect | Document how to run this project locally, starting from a fresh clone. |
| readme-04 | write-readme |  | indirect | A new hire spent a whole day trying to get this running. Make sure the next one doesn't. |
| readme-05 | write-readme |  | hard | I renamed the npm scripts last week: dev is now start:dev and test is now test:unit. Make sure the docs keep up. |
| readme-06 | write-readme |  | hard | This is a pnpm monorepo with four packages and no top-level docs. What should someone see when they open the repo on GitHub? Write it. |
| readme-07 | write-readme |  | hard | We're open-sourcing this CLI next week and the repo landing page is just the project name. Sort it out. |
| readme-08 | write-readme |  | direct | Generate the docs for this library in the README: install, usage and an API overview. |
| prose-01 | write-prose |  | direct | I wrote this messy draft on our code-review process (notes/code-review.md) and want it turned into a proper blog post. Keep my voice as a working engineer and don't invent things I didn't say. |
| prose-02 | write-prose |  | indirect | Our about page (content/about.md) reads like an AI wrote it. Full of 'seamless', 'revolutionary', 'passionate team'. Rewrite it so it sounds like an actual person with a point of view, keeping the facts. |
| prose-03 | write-prose |  | hard | This article of mine (posts/caching.md) is grammatically clean but still feels machine-made. It narrates itself instead of arguing, and it resolves every open question by the end. Help. |
| prose-04 | write-prose |  | hard | Here are my raw notes on why churn spiked (notes/churn.md). The evidence is contradictory and I never reached a conclusion. Draft the blog post without writing a cleaner story than my notes support. |
| prose-05 | write-prose |  | indirect | My essay (drafts/essay.md) takes too long to get going; friends say the first half reads like a travel diary. Restructure it to start where it matters and cut the 'surprisingly, what I learned was' narration. |
| prose-06 | write-prose |  | indirect | We shipped a migration tool. I need a short changelog piece explaining what changed and why it matters, no marketing adjectives, under 300 words. The internal spec is in docs/migration-spec.md. |
| prose-07 | write-prose |  | direct | Write a commit message for the changes I just made. They fix a race in background sync. |
| prose-08 | write-prose |  | hard | Draft the PR description for this branch using our template in .github/pull_request_template.md. Unit tests passed; browser testing was not run. |
| none-01 | none |  | near-miss | Fix the TypeError in src/components/InvoiceTable.tsx: 'Cannot read properties of undefined (reading map)'. |
| none-02 | none |  | near-miss | Convert #4F46E5 to HSL and OKLCH. |
| none-03 | none |  | near-miss | Write three ad headlines for our launch and a punchy Twitter thread with hooks and hashtags. |
| none-04 | none |  | near-miss | Explain the difference between flexbox and CSS grid. |
| none-05 | none |  | near-miss | Rename the Button component's 'kind' prop to 'variant' everywhere. |
| none-06 | none |  | near-miss | Add a unit test for the formatCurrency util in src/utils/format.ts. |
| none-07 | none |  | near-miss | Change the primary button color to #0F766E. |
| none-08 | none |  | near-miss | Set up Tailwind in this project. |
| none-09 | none |  | near-miss | What's the CSS property for making text not wrap? |
| none-10 | none |  | near-miss | Write the API route that returns the list of invoices as JSON. |
| none-11 | none |  | near-miss | Update the copyright year in the footer to 2026. |
| none-12 | none |  | near-miss | Why is my Next.js build failing with 'Module not found: Can't resolve @/lib/db'? |
| none-13 | none |  | near-miss | Translate the German docs in docs/de to English. |
| none-14 | none |  | near-miss | Summarize this article in three bullet points for my notes: https://example.com/post |
| none-15 | none |  | near-miss | Commit these files and push the branch to GitHub. |
| none-16 | none |  | near-miss | Add a JSDoc comment to the formatCurrency function in src/utils/format.ts. |
| none-17 | none |  | near-miss | Fix the typo 'Instalation' in the README heading. |
| none-18 | none |  | near-miss | Generate an OpenAPI spec for the routes in src/api. |
| none-19 | none |  | near-miss | Write a press release announcing our Series A. |
