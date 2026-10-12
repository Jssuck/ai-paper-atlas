"""Deterministic examples; these labels are invented for this teaching exercise."""
import json
from model import HornSystem, Rule, filter_evidence


def serial_trace(trace):
    return [sorted(state) for state in trace]


def support_record(system, anchors=(), withdrawn=()):
    least = system.fixed_point("least", anchors, withdrawn)
    greatest = system.fixed_point("greatest", anchors, withdrawn)
    return {"anchors": sorted(anchors), "withdrawn": sorted(withdrawn),
            "least_trace": serial_trace(least.states),
            "greatest_trace": serial_trace(greatest.states),
            "least": sorted(least.result), "greatest": sorted(greatest.result)}


def examples():
    hypotheses = {"copper", "iron", "wood"}
    observations = ({"copper", "iron"}, {"iron"})
    cycle = HornSystem({"A", "B", "C"}, (
        Rule({"A"}, "B"), Rule({"B"}, "C"), Rule({"C"}, "A")))
    chain = HornSystem({"A", "B", "C"}, (
        Rule({"A"}, "B"), Rule({"B"}, "C")))
    alternatives = HornSystem({"A", "B", "C", "D"}, (
        Rule({"A"}, "B"), Rule({"B"}, "C"), Rule({"D"}, "C")))
    lexical = {"q_means_warm", "q_means_bright"}
    return {
        "evidence": {
            "faithful_trace": serial_trace(filter_evidence(hypotheses, observations)),
            "reversed_trace": serial_trace(filter_evidence(hypotheses, reversed(observations))),
            "missing_truth_trace": serial_trace(filter_evidence(hypotheses, observations, {"copper", "wood"})),
            "bad_evidence_trace": serial_trace(filter_evidence(hypotheses, ({"copper"}, {"iron"}))),
            "nonidentifying_trace": serial_trace(filter_evidence(hypotheses, ({"copper", "iron"},) * 3)),
        },
        "support": {
            "unanchored_cycle": support_record(cycle),
            "anchored_cycle": support_record(cycle, {"A"}),
            "anchor_removed_cycle": support_record(cycle),
            "one_claim_withdrawn_cycle": support_record(cycle, (), {"B"}),
            "anchored_chain": support_record(chain, {"A"}),
            "anchor_removed_chain": support_record(chain),
            "alternative_anchor": support_record(alternatives, {"A", "D"}),
            "one_anchor_removed_alternative": support_record(alternatives, {"D"}),
            "withdrawal_overrides_anchor": support_record(cycle, {"A"}, {"A"}),
        },
        "lexical": {
            "warm_bright_examples_only": serial_trace(filter_evidence(lexical, (lexical, lexical))),
            "contrasting_example": serial_trace(filter_evidence(lexical, (lexical, {"q_means_warm"}))),
            "note": "All observed examples were warm and bright; a warm, dark example labeled q separates the two stipulated interpretations."
        },
    }


if __name__ == "__main__":
    print(json.dumps(examples(), ensure_ascii=False, indent=2, sort_keys=True))
