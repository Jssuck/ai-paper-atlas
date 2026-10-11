"""Run deterministic examples; every world and measurement law is stipulated."""
import json
from dataclasses import asdict
from fractions import Fraction
from finite_model import FiniteModel
from ratios import (response, infer_product, calibrated_coefficient,
                    equivalent_parameters, relative_coefficient)


def example_model():
    model = FiniteModel.from_rows(("effect",), {
        "none": (0,), "A": (1,), "B": (1,), "A+B": (1,)})
    queries = {
        "cause_exists": {"none": False, "A": True, "B": True, "A+B": True},
        "number_of_causes": {"none": 0, "A": 1, "B": 1, "A+B": 2},
        "cause_identity": {state: state for state in model.states},
        "attribute": {"none": "absent", "A": "red", "B": "blue", "A+B": "red"},
    }
    return model, queries


def report():
    model, queries = example_model()
    named = model.with_labels({state: "force" for state in model.states})
    redundant = model.append_observation("effect_word", {
        state: row[0] + 100 for state, row in zip(model.states, model.signatures)})
    probe = model.append_observation("new_probe", {"none": 0, "A": 7, "B": 8, "A+B": 7})
    assumed = model.restrict(("B",))
    wide = FiniteModel.from_rows(("effect",), {
        **dict(zip(model.states, model.signatures)), "spontaneous": (1,)})
    existence_wide = {**queries["cause_exists"], "spontaneous": False}
    inputs = (Fraction(1), Fraction(2), Fraction(3))
    outputs = response(inputs, coefficient=3, gain=2)
    variants = [equivalent_parameters(3, 2, scale)
                for scale in (Fraction(1, 2), Fraction(1), Fraction(2))]
    return {
        "warning": "Modern stipulated model; not Condillac's algorithm or a physical/theological validation.",
        "finite": {
            "observed": [1], "fibers": model.fibers(),
            "queries": {name: asdict(model.answer((1,), query)) for name, query in queries.items()},
            "labels_preserve_fibers": named.fibers() == model.fibers(),
            "derived_word_preserves_fibers": redundant.fibers() == model.fibers(),
            "new_probe_candidates": probe.candidates((1, 7)),
            "new_probe_attribute": asdict(probe.answer((1, 7), queries["attribute"])),
            "new_probe_number": asdict(probe.answer((1, 7), queries["number_of_causes"])),
            "assume_B_identity": asdict(assumed.answer((1,), {"B": "B"})),
            "assumption_preserves_columns": assumed.columns == model.columns,
            "out_of_model_observation": asdict(model.answer((2,), queries["cause_exists"])),
            "wider_model_existence": asdict(wide.answer((1,), existence_wide)),
        },
        "ratios": {
            "inputs": inputs, "outputs": outputs, "product": asdict(infer_product(inputs, outputs)),
            "known_gain_2_coefficient": calibrated_coefficient(inputs, outputs, known_gain=2),
            "unknown_gain_equivalent_pairs_k_g": variants,
            "all_pairs_match": all(response(inputs, k, g) == outputs for k, g in variants),
            "all_zero_inputs": asdict(infer_product((0, 0), (0, 0))),
            "incompatible_data": asdict(infer_product((1, 2), (6, 13))),
            "shared_gain_relative_coefficient": relative_coefficient(inputs, outputs, response(inputs, 5, 2)),
        },
    }


def encode(value):
    if isinstance(value, Fraction):
        return str(value)
    raise TypeError(f"Cannot encode {type(value).__name__}")


if __name__ == "__main__":
    print(json.dumps(report(), ensure_ascii=False, indent=2, default=encode))
