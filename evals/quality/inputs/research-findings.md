# API adoption analysis - raw notes

Period: March 2026 through September 2026. Source: our API gateway logs, all plans, all regions. Visibility caveat: we only see traffic that goes through our gateway, so calls made through self-hosted proxies or mirrored endpoints are invisible to this analysis.

Definitions I used:

- Active account: at least one billable action in the calendar month.
- SDK adopter: account that made its first SDK-authenticated call within 60 days of signup.
- Integration: a distinct third-party connection configured on the account.
- Time to first call: calendar days from account creation to the first call that returned 200. Failed attempts don't count, which flatters this number.

Findings:

1. API adoption among active accounts rose from 18% to 31% between March and September (N = 1,240 accounts active in both months).

2. SDK adopters shipped 2.4x more integrations in their first six months than non-adopters (median 5 vs 2; N = 318 adopters, N = 902 non-adopters). Known problem with this comparison: adopters skew toward larger accounts, and larger accounts ship more integrations regardless of the SDK. It's a comparison, not evidence the SDK causes anything.

3. Median time to first successful call dropped from 11 days to 4 after the quickstart launched in May.

4. Enterprise tier: only 41 accounts were active in both windows. Too small to publish a percentage for that tier alone; the trend looked similar but I wouldn't stake anything on it.

Where I want to land (push back if this is stronger than the data): the quickstart looks like the main driver of the adoption growth, and the SDK seems to compound it.
