"""Emit deterministic, machine-readable teaching examples to stdout."""
import json
from dataclasses import asdict
from model import (Catalog, Rule, Theory, attend, compare, reflect,
                   equivalence_classes, imagine, closure, verify_certificate,
                   semantic_oracle, subset_syllogism)


def reasoning_case(theory):
    proof = closure(theory)
    entailed, model_count = semantic_oracle(theory)
    if {step.atom for step in proof} != set(entailed):
        raise RuntimeError("closure and independent semantic oracle disagree")
    verified = all(verify_certificate(theory, proof, atom) for atom in entailed)
    if not verified:
        raise RuntimeError("generated proof was rejected")
    return {"facts": theory.facts, "rules": [asdict(rule) for rule in theory.rules],
            "proof": [asdict(step) for step in proof], "entailed": entailed,
            "satisfying_valuations": model_count, "certificates_verified": verified}


def main():
    c = Catalog(("color", "shape", "material"),
                (("red", "blue"), ("round", "square"), ("wood", "metal")),
                (("a", ("red", "round", "wood")),
                 ("b", ("red", "round", "metal")),
                 ("c", ("blue", "square", "wood"))))
    left = attend(c, "a", ("color", "shape"))
    recalled = attend(c, "b", ("color", "shape"), "recalled")
    other = attend(c, "c", ("color", "shape"), "recalled")
    atoms = ("air_has_weight", "pressure_bridge", "column_supported")
    rules = (Rule("illustrative_bridge", ("air_has_weight", "pressure_bridge"), "column_supported"),)
    report = {
        "scope": "modern finite teaching model; no psychological or physical validation",
        "attention": {"current": asdict(left), "recalled": asdict(recalled)},
        "comparison": {"color": compare(c, left, recalled, "color"),
                       "material": compare(c, left, recalled, "material")},
        "reflection": {"sequence": reflect(c, left, recalled, ("color", "shape", "material")),
                       "selected_classes": equivalence_classes(c, ("color", "shape")),
                       "all_feature_classes": equivalence_classes(c, c.features)},
        "imagination": [asdict(concept) for concept in imagine(c, (left, other), ("color", "shape"))],
        "reasoning": {
            "intermediate_chain": reasoning_case(Theory(("p", "q", "r"), ("p",),
                                      (Rule("qr", ("q",), "r"), Rule("pq", ("p",), "q")))),
            "missing_bridge": reasoning_case(Theory(atoms, ("air_has_weight",), rules)),
            "bridge_assumed": reasoning_case(Theory(atoms, ("air_has_weight", "pressure_bridge"), rules)),
            "unseeded_cycle": reasoning_case(Theory(("p", "q"), (),
                                      (Rule("pq", ("p",), "q"), Rule("qp", ("q",), "p"))))},
        "subset_example": subset_syllogism(("x", "y", "z"), ("x",), ("x", "y"), ("x", "y", "z")),
        "empty_small_set": subset_syllogism(("x", "y", "z"), (), ("x",), ("x", "y", "z"))}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
