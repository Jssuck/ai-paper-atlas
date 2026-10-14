"""Print a deterministic JSON report: python3 demo.py > report.json."""

from dataclasses import asdict
import json

from logic import Language, Model, Prop, ValidationError, entails, evaluate
from proofs import Step, check_certificate


def describe_model(model: Model | None) -> dict | None:
    if model is None:
        return None
    return {
        "terms_in_bit_order": list(model.terms),
        "universe_representatives": list(model.support),
        "term_extensions": {t: list(model.members(t)) for t in model.terms},
    }


def existential_witness(prop: Prop, model: Model) -> int | None:
    """A realized representative for a true I/O claim; otherwise None."""
    if prop.kind not in ("I", "O"):
        return None
    for representative in model.support:
        if evaluate(prop, Model(model.terms, (representative,))):
            return representative
    return None


def argument_report(language: Language, premises: tuple[Prop, ...], conclusion: Prop) -> dict:
    result = entails(language, premises, conclusion)
    model = result.countermodel
    return {
        "premises": [asdict(p) for p in premises],
        "conclusion": asdict(conclusion),
        "required_nonempty": sorted(language.required_nonempty),
        "holds": result.holds,
        "admissible_supports": result.admissible_models,
        "premise_satisfying_supports": result.satisfying_premise_models,
        "countermodel": describe_model(model),
        "countermodel_premise_truths": None if model is None else [evaluate(p, model) for p in premises],
        "countermodel_conclusion_truth": None if model is None else evaluate(conclusion, model),
    }


def rejected_certificate(language, premises, conclusion, steps) -> dict:
    try:
        check_certificate(language, premises, conclusion, steps)
    except ValidationError as error:
        return {"accepted": False, "reason": str(error)}
    raise RuntimeError("the intentionally invalid certificate was unexpectedly accepted")


def build_report() -> dict:
    language = Language(("S", "M", "P"))
    chain_premises = (Prop("A", "S", "M"), Prop("A", "M", "P"))
    chain_conclusion = Prop("A", "S", "P")
    false_model = Model(language.terms, (1, 2))
    chain_steps = (
        Step(chain_premises[0], "assume", assumption=0),
        Step(chain_premises[1], "assume", assumption=1),
        Step(chain_conclusion, "a_trans", (0, 1)),
    )
    valid_false = argument_report(language, chain_premises, chain_conclusion)
    valid_false.update({
        "particular_model": describe_model(false_model),
        "particular_premise_truths": [evaluate(p, false_model) for p in chain_premises],
        "particular_conclusion_truth": evaluate(chain_conclusion, false_model),
        "certificate": asdict(check_certificate(language, chain_premises, chain_conclusion, chain_steps)),
    })
    invalid_premises = (Prop("A", "S", "M"), Prop("A", "P", "M"))
    true_model = Model(language.terms, (7,))
    true_but_invalid = argument_report(language, invalid_premises, chain_conclusion)
    true_but_invalid.update({
        "particular_model": describe_model(true_model),
        "particular_premise_truths": [evaluate(p, true_model) for p in invalid_premises],
        "particular_conclusion_truth": evaluate(chain_conclusion, true_model),
        "invalid_converse_certificate": rejected_certificate(
            language, invalid_premises, chain_conclusion,
            (Step(invalid_premises[0], "assume", assumption=0),
             Step(invalid_premises[1], "assume", assumption=1),
             Step(chain_conclusion, "a_trans", (0, 1))),
        ),
    })
    two_terms = Language(("S", "P"))
    universal = Prop("A", "S", "P")
    existential = Prop("I", "S", "P")
    converted_premises = (Prop("A", "S", "M"), Prop("E", "P", "M"))
    converted_conclusion = Prop("E", "S", "P")
    converted_steps = (
        Step(converted_premises[0], "assume", assumption=0),
        Step(converted_premises[1], "assume", assumption=1),
        Step(Prop("E", "M", "P"), "e_sym", (1,)),
        Step(converted_conclusion, "e_down", (0, 2)),
    )
    converted = argument_report(language, converted_premises, converted_conclusion)
    converted["certificate"] = asdict(check_certificate(
        language, converted_premises, converted_conclusion, converted_steps))
    imported = rejected_certificate(
        language, (chain_premises[0],), chain_conclusion,
        (Step(chain_premises[0], "assume", assumption=0),
         Step(chain_premises[1], "assume", assumption=1),
         Step(chain_conclusion, "a_trans", (0, 1))),
    )
    repeat = check_certificate(
        two_terms, (universal,), universal,
        (Step(universal, "assume", assumption=0),),
    )
    mixed_truth_model = Model(language.terms, (1, 6))
    converse_model = Model(two_terms.terms, (2, 3))
    hand_examples = {
        "mixed_true_false_premises": {
            "named_objects": [1, 2],
            "named_extensions": {"S": [1], "M": [2], "P": [2]},
            "named_object_to_truth_type": {"1": 1, "2": 6},
            "compressed_model": describe_model(mixed_truth_model),
            "premises": [asdict(p) for p in chain_premises],
            "conclusion": asdict(chain_conclusion),
            "premise_truths": [evaluate(p, mixed_truth_model) for p in chain_premises],
            "conclusion_truth": evaluate(chain_conclusion, mixed_truth_model),
        },
        "A_is_not_symmetric": {
            "named_objects": [1, 2],
            "named_extensions": {"S": [1], "P": [1, 2]},
            "named_object_to_truth_type": {"1": 3, "2": 2},
            "compressed_model": describe_model(converse_model),
            "A_S_P_truth": evaluate(Prop("A", "S", "P"), converse_model),
            "A_P_S_truth": evaluate(Prop("A", "P", "S"), converse_model),
        },
    }
    witness_examples = []
    for second_kind, conclusion_kind, rule, support in (
        ("A", "I", "i_up", (7,)), ("E", "O", "o_from_i_e", (3,)),
    ):
        witness_premises = (Prop("I", "S", "M"), Prop(second_kind, "M", "P"))
        witness_conclusion = Prop(conclusion_kind, "S", "P")
        witness_model = Model(language.terms, support)
        witness_steps = (
            Step(witness_premises[0], "assume", assumption=0),
            Step(witness_premises[1], "assume", assumption=1),
            Step(witness_conclusion, rule, (0, 1)),
        )
        example = argument_report(language, witness_premises, witness_conclusion)
        example.update({
            "rule": rule,
            "particular_model": describe_model(witness_model),
            "particular_premise_truths": [evaluate(p, witness_model) for p in witness_premises],
            "particular_conclusion_truth": evaluate(witness_conclusion, witness_model),
            "premise_existential_witnesses": [existential_witness(p, witness_model) for p in witness_premises],
            "conclusion_existential_witness": existential_witness(witness_conclusion, witness_model),
            "certificate": asdict(check_certificate(language, witness_premises, witness_conclusion, witness_steps)),
        })
        witness_examples.append(example)
    return {
        "model": "modern extensional unary A/E/I/O teaching model; not an Aristotle algorithm",
        "assumptions": {
            "universe_nonempty": True,
            "terms_may_be_empty_by_default": True,
            "number_of_terms": "1 to 3",
            "objects_with_the_same_truth_type_are_collapsed": True,
            "does_not_classify": ["demonstrative truth/source", "historical perfect/imperfect", "genuinely through the premises"],
        },
        "support_counts_without_nonempty_term_policy": {"1": 3, "2": 15, "3": 255},
        "named_object_hand_examples": hand_examples,
        "valid_form_with_false_premises_in_one_model": valid_false,
        "true_conclusion_in_one_model_but_invalid_argument": true_but_invalid,
        "A_does_not_imply_I_with_empty_terms": argument_report(two_terms, (universal,), existential),
        "A_implies_I_when_S_explicitly_nonempty": argument_report(
            Language(("S", "P"), frozenset(("S",))), (universal,), existential),
        "valid_proof_using_E_conversion": converted,
        "unsupported_imported_premise": imported,
        "same_conclusion_as_assumption": asdict(repeat),
        "explicit_witness_propagation": witness_examples,
        "inconsistent_premises_make_classical_consequence_vacuous": argument_report(
            two_terms, (Prop("E", "S", "S"), Prop("I", "S", "S")), universal),
        "interpretation_warning": "support checks and syntactic dependency tracking do not by themselves settle Aristotle's historical definitions",
    }


if __name__ == "__main__":
    print(json.dumps(build_report(), ensure_ascii=False, sort_keys=True, indent=2))
