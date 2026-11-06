"""Illustrative sketch: a small eval harness for a support-ticket agent.
Core mechanism only (NOT a solution to problem 09).

Design decisions this sketch demonstrates:
  * A GOLDEN SET of human-reviewed cases is the ground truth -- metrics
    are computed over it, not over the agent's own confidence scores.
  * The metric set includes a STALE-QUOTE rate, the failure that
    fluency and confidence cannot catch: an analysis can read perfectly
    and still quote a superseded runbook.
  * A THRESHOLD RULE changes routing: when a metric breaches its limit,
    analyses are demoted to human review instead of auto-shipping.
  * The harness catches a SILENT REGRESSION: fluent, high-confidence
    output whose quoted sources are retired.
"""

from dataclasses import dataclass, field

# --- Thresholds (illustrative; the paper should justify them) ---
MAX_STALE_QUOTE_RATE = 0.02   # >2% of analyses quoting retired sources
MIN_ROUTING_ACCURACY = 0.90   # routing must match the golden labels
MAX_SLA_BREACH_RATE = 0.05


@dataclass
class GoldenCase:
    case_id: str
    correct_route: str          # "human" | "dev-agent" | "auto-answer"
    runbook_is_current: bool    # is the quoted runbook still valid?
    quoted_runbook: str | None  # which runbook the analysis cited


@dataclass
class Analysis:
    case_id: str
    route: str
    confidence: str             # high / medium / low
    quoted_runbook: str | None
    sla_hours: float            # hours from ticket to answer


@dataclass
class EvalResult:
    routing_accuracy: float
    stale_quote_rate: float
    sla_breach_rate: float
    escalation_precision: float
    breached: list = field(default_factory=list)


def run_eval(golden: list[GoldenCase], analyses: list[Analysis]) -> EvalResult:
    by_id = {g.case_id: g for g in golden}
    n = len(golden)

    correct_routes = sum(1 for a in analyses
                         if by_id[a.case_id].correct_route == a.route)
    stale = sum(1 for a in analyses
                if a.quoted_runbook
                and not by_id[a.case_id].runbook_is_current)
    sla_breaches = sum(1 for a in analyses if a.sla_hours > 24)
    escalated = [a for a in analyses if a.route == "human"]
    correct_escalations = sum(1 for a in escalated
                              if by_id[a.case_id].correct_route == "human")

    result = EvalResult(
        routing_accuracy=correct_routes / n,
        stale_quote_rate=stale / n,
        sla_breach_rate=sla_breaches / n,
        escalation_precision=(correct_escalations / len(escalated)
                              if escalated else 1.0),
    )
    # Threshold rule: a breach changes routing, it doesn't just log.
    if result.stale_quote_rate > MAX_STALE_QUOTE_RATE:
        result.breached.append(
            f"stale-quote rate {result.stale_quote_rate:.0%} "
            f"> {MAX_STALE_QUOTE_RATE:.0%} -- demote all analyses "
            "to human review until the runbook index is refreshed")
    if result.routing_accuracy < MIN_ROUTING_ACCURACY:
        result.breached.append(
            f"routing accuracy {result.routing_accuracy:.0%} "
            f"< {MIN_ROUTING_ACCURACY:.0%} -- demote low-confidence "
            "analyses to human review")
    if result.sla_breach_rate > MAX_SLA_BREACH_RATE:
        result.breached.append(
            f"SLA breach rate {result.sla_breach_rate:.0%} "
            f"> {MAX_SLA_BREACH_RATE:.0%} -- escalate queue triage")
    return result


def demo() -> None:
    # Golden set: 10 reviewed cases. Runbook RB-7 was superseded last
    # week; RB-3 is still current.
    golden = [
        GoldenCase("T-01", "auto-answer", True, "RB-3"),
        GoldenCase("T-02", "human", True, None),
        GoldenCase("T-03", "dev-agent", True, None),
        GoldenCase("T-04", "auto-answer", False, "RB-7"),  # retired!
        GoldenCase("T-05", "auto-answer", False, "RB-7"),  # retired!
        GoldenCase("T-06", "auto-answer", True, "RB-3"),
        GoldenCase("T-07", "human", True, None),
        GoldenCase("T-08", "dev-agent", True, None),
        GoldenCase("T-09", "auto-answer", True, "RB-3"),
        GoldenCase("T-10", "auto-answer", True, "RB-3"),
    ]
    # The silent regression: T-04 and T-05 read fluent and confident,
    # but quote the retired runbook RB-7.
    analyses = [
        Analysis("T-01", "auto-answer", "high", "RB-3", 3.0),
        Analysis("T-02", "human", "low", None, 5.0),
        Analysis("T-03", "dev-agent", "high", None, 6.0),
        Analysis("T-04", "auto-answer", "high", "RB-7", 2.0),
        Analysis("T-05", "auto-answer", "high", "RB-7", 2.5),
        Analysis("T-06", "auto-answer", "high", "RB-3", 4.0),
        Analysis("T-07", "human", "low", None, 7.0),
        Analysis("T-08", "dev-agent", "medium", None, 8.0),
        Analysis("T-09", "auto-answer", "high", "RB-3", 3.5),
        Analysis("T-10", "auto-answer", "high", "RB-3", 3.0),
    ]

    result = run_eval(golden, analyses)
    print("Eval over golden set of 10 reviewed cases:")
    print(f"  routing accuracy:     {result.routing_accuracy:.0%}")
    print(f"  stale-quote rate:     {result.stale_quote_rate:.0%} "
          "(fluent + confident, quoting retired RB-7)")
    print(f"  SLA breach rate:      {result.sla_breach_rate:.0%}")
    print(f"  escalation precision: {result.escalation_precision:.0%}")
    if result.breached:
        print("\nTHRESHOLD BREACH -- routing changes:")
        for b in result.breached:
            print(f"  ! {b}")
    else:
        print("\nNo threshold breached; routing unchanged.")


if __name__ == "__main__":
    demo()
