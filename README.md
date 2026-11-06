# Evaluating a support-ticket agent in production: eval harness, failure-mode taxonomy, and thresholds that change routing

**Date:** Monday, Nov 2, 2026 · **Status:** To do · **Problem 09 of 13** — Daily Architect Problems (CCA prep)

Part of *Daily Architect Problems* — thirteen applied agentic-design problems from Claude Certified Architect (CCA) prep, grounded in a real production agent. This folder is self-contained: publish it on its own as its own repo.

## The problem

The agent is live, with an in-flow evaluator and outcome measurement just started. Last week two fluent, confident analyses quoted runbooks that had been superseded — and nothing flagged them, because nothing measured that failure. Design the evaluation harness: golden set, metrics, and thresholds that change routing.

## How to use it

1. Read `problem.md` — the scenario, the task, and the self-check.
2. Write your answer as a design paper: the decision, the trade-offs, the numbers, and the failure case your design leaves uncovered.
3. Run the example to see one key mechanism as a working sketch: `python3 09_eval_harness.py`
4. Use the self-check at the end of `problem.md` to test whether your design holds up.

## The example code

`09_eval_harness.py` is an illustrative sketch of one core mechanism in this problem: a golden set of reviewed cases, metrics over it (routing accuracy, stale-quote rate, SLA breach rate, escalation precision), and a threshold rule that demotes analyses to human review when a metric breaches — catching a silent regression that fluency and confidence miss. It uses only the Python standard library. It is **not** the answer, **not** production code, and **not** the real agent's code — it is scaffolding to help you see the mechanism run.

## Files

- `problem.md` — the full problem statement (scenario, task, self-check)
- `09_eval_harness.py` — runnable example sketch
