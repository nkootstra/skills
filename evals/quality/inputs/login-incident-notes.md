incident notes: login attack, 14-16 March (raw, in the order things happened)

- 14 Mar 09:10 alerts: /login at 42,000 requests/min. normal peak is about 1,500/min.
- traffic was credential stuffing: username/password pairs from other sites' leaks, tried against our login. ~0.4% of attempts matched a real account (we checked afterwards).
- 09:25 turned on per-IP rate limit (20 attempts/min per IP). helped for ~40 min. then the attack moved to ~30,000 distinct IPs (residential proxies), each under the limit. per-IP limit basically stopped mattering.
- 10:30 blocked the 3 hosting providers (ASNs) the first wave came from. worked for the first wave only; the proxy wave came from consumer ISPs we can't block.
- 11:15 added a per-account limit: after 5 failed attempts an account needs a second factor or waits 15 min. this is what actually protected accounts: from then on matched credentials couldn't log in without the second step.
- considered turning on a CAPTCHA for every login. didn't: our mobile app and partner API clients log in through the same endpoint and can't solve a CAPTCHA, so it would have locked them out. accepted cost: the attack traffic kept hitting us and we paid for the extra load (autoscaling to 3x instances for two days).
- 15 Mar: attackers ramped up and backed off every ~20 min, apparently testing our limits. per-account limit held throughout.
- 16 Mar 18:00 traffic back to normal.
- outcome: 2,310 accounts had a matching password tried; we forced a password reset on all of them. no evidence of any login completing without the second step after 11:15. between 09:10 and 11:15, 37 accounts were logged into by the attacker; we reset those, revoked their sessions and emailed the owners.
- now: per-account limit is permanent. per-IP limit kept but raised to 60/min because it was hurting offices behind one NAT.
- we don't think this is over; credential lists keep circulating. the per-account limit doesn't depend on where traffic comes from, which is why we trust it more than the IP-based ones.
- audience: our customers' engineering and security teams, on our public blog.
