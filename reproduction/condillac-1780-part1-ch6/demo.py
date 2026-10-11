"""One connected fictional example. No historical or empirical inference."""

import json
from fractions import Fraction

from habit_model import action_inputs, habit_closed_form, habit_trace
from action_model import Policy, admissible_norms, behavioral_classes, compatible_intentions, normative_status


def example_policy():
    return Policy(
        contexts=("alarm", "quiet", "invitation"),
        intentions=("fear_harm", "desire_quiet", "desire_rest"),
        actions=("withdraw", "stay", "approach"),
        rows=(("withdraw", "stay", "approach"),
              ("withdraw", "withdraw", "withdraw"),
              ("withdraw", "stay", "stay")),
    )


def run_demo():
    policy = example_policy()
    actions = ("withdraw", "withdraw", "withdraw", "stay", "stay")
    inputs = action_inputs(actions, "withdraw")
    trace = habit_trace(Fraction(1, 2), 0, inputs)
    open_codes = admissible_norms(policy.actions)
    partial_codes = admissible_norms(policy.actions, ("stay",), ("approach",))
    full_codes = admissible_norms(policy.actions, ("stay", "withdraw"), ("approach",))
    observations = (("alarm", "withdraw"), ("quiet", "stay"), ("invitation", "approach"))
    transferred = Policy(policy.contexts, policy.intentions, policy.actions,
                         (policy.rows[1], policy.rows[0], policy.rows[2]))
    return {
        "scope": "Modern stipulated teaching model; not psychology, ethics, history, or theology proof.",
        "habit": {
            "tracked_action": "withdraw", "alpha": "1/2", "initial": "0",
            "actions": list(actions), "inputs": list(inputs),
            "trace": [str(h) for h in trace],
            "closed_form_final": str(habit_closed_form(Fraction(1, 2), 0, inputs)),
            "same_count_different_order": {"10": str(habit_trace(Fraction(1, 2), 0, (1, 0))[-1]),
                                           "01": str(habit_trace(Fraction(1, 2), 0, (0, 1))[-1])},
            "repetition_eight": str(habit_trace(Fraction(1, 2), 0, (1,) * 8)[-1]),
            "disuse_eight_from_one": str(habit_trace(Fraction(1, 2), 1, (0,) * 8)[-1]),
        },
        "inference": {
            "contexts": list(policy.contexts), "intentions": list(policy.intentions),
            "policy_rows": [list(row) for row in policy.rows],
            "observations": [list(o) for o in observations],
            "candidates_by_prefix": [list(compatible_intentions(policy, observations[:n])) for n in range(4)],
            "classes_alarm": behavioral_classes(policy, ("alarm",)),
            "classes_alarm_quiet": behavioral_classes(policy, ("alarm", "quiet")),
            "classes_all": behavioral_classes(policy, policy.contexts),
            "contradictory_record": compatible_intentions(policy, (("alarm", "withdraw"), ("alarm", "stay"))),
            "transfer_counterexample": {
                "target_true_intention": "desire_quiet",
                "target_observations": [[x, transferred.action("desire_quiet", x)] for x in policy.contexts],
                "inferred_with_observers_table": compatible_intentions(policy, [(x, transferred.action("desire_quiet", x)) for x in policy.contexts]),
            },
        },
        "norms": {
            "observed_feasible_actions": sorted(set(actions)),
            "feasibility_is_not_a_normative_bridge": True,
            "unconstrained_code_count": len(open_codes),
            "withdraw_unconstrained": normative_status("withdraw", policy.actions, open_codes),
            "partial_bridge": {"required": ["stay"], "forbidden": ["approach"],
                               "codes": [sorted(code) for code in partial_codes],
                               "withdraw_status": normative_status("withdraw", policy.actions, partial_codes)},
            "full_bridge": {"required": ["stay", "withdraw"], "forbidden": ["approach"],
                            "codes": [sorted(code) for code in full_codes],
                            "withdraw_status": normative_status("withdraw", policy.actions, full_codes)},
            "same_high_habit_opposite_judgments": {
                "habit_after_three_withdrawals": str(trace[3]),
                "code_1": ["stay"], "code_1_judgment": "forbid",
                "code_2": ["stay", "withdraw"], "code_2_judgment": "permit",
            },
            "contradictory_bridge_status": normative_status("withdraw", policy.actions,
                admissible_norms(policy.actions, ("withdraw",), ("withdraw",))),
        },
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), ensure_ascii=False, indent=2))
