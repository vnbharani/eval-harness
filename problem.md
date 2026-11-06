# Monday, Nov 2, 2026 — Evaluating a support-ticket agent in production: eval harness, failure-mode taxonomy, and thresholds that change routing

**Status: To do**

**Scenario:** Your support-ticket agent is live. Analyses carry high/medium/low confidence, low-confidence analyses go to a human, code issues create a ticket for the dev agent, and humans review analyses in batches every 8 hours against a 24-hour SLA. An in-flow evaluator (a different model) already scores each analysis, and outcome measurement has just started. Now the hard part: last week a batch of analyses read fluent and confident — and two of them quoted runbooks that had been superseded. Nothing in the pipeline flagged them, because nothing was measuring that failure. Eval budget is real: every evaluator call costs money and latency, and the human review batch cannot grow.

**The task — write it as a short applied design paper, not a quiz answer:** Design the evaluation harness for this agent. Cover: (a) how you build the golden set from reviewed tickets and how big it needs to be before you trust it; (b) the metric set — routing accuracy, stale-quote rate, SLA breach rate, and escalation precision — and which single metric you would gate a release on; (c) where the in-flow evaluator stays and where offline sampled eval takes over, with the cost/latency budget for each; (d) the threshold rule that changes routing — e.g., what eval signal demotes an analysis to human review or retires an episode — and how eval results feed the episode store without poisoning it.

**Self-check:** Would your harness catch a silent regression where analyses stay fluent and confident but start quoting retired runbooks — and how many bad analyses would ship before it fired?
