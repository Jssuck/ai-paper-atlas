"""Run explicit, deterministic examples; all rational output is exact text."""

import json
from fractions import Fraction

from model import (
    Add, Certificate, Const, Equation, FiniteSign, Mul, Var, check_certificate,
    evaluate_expr, evaluate_polynomial, first_counterexample, normalize,
    restrict_certificate, section16_example, substitute, triangle_cases,
)


def examples() -> dict:
    premises, target, certificate = section16_example()
    checked = check_certificate(premises, target, certificate)
    keep = ("alternate_a", "alternate_c", "straight_angle")
    reduced, reduced_certificate = restrict_certificate(premises, target, certificate, keep)
    transferred = check_certificate(reduced, target, reduced_certificate)
    special_target = Equation(target.variables, (0, 1, 0, 0, 0), 90)
    special_certificate = Certificate((0, 0, 0, 1, 0))
    special = check_certificate(premises, special_target, special_certificate)
    try:
        restrict_certificate(premises, special_target, special_certificate, keep)
    except ValueError as error:
        special_transfer = {"allowed": False, "reason": str(error)}
    else:
        raise RuntimeError("special-drawing certificate unexpectedly transferred")
    # A direct post-deletion check fails too; this is not just label inspection.
    deleted_special = check_certificate(reduced, special_target, Certificate((0, 0, 0)))
    cases = triangle_cases()
    all_triangles = FiniteSign("triangle", cases, frozenset(cases))
    representative = FiniteSign("representative", cases, frozenset((cases[0],)))
    witness = first_counterexample(all_triangles, lambda triangle: triangle.is_right())
    x, y, z = Var("x"), Var("y"), Var("z")
    left = Mul(x, Add(y, z))
    right = Add(Mul(x, y), Mul(x, z))
    values = {"x": Fraction(2, 3), "y": Fraction(-3, 5), "z": Fraction(7, 2)}
    simultaneous = substitute(x, {"x": Add(y, Const(1)), "y": Const(2)})
    return {
        "model_status": "modern teaching reconstruction; no historical code or cognition claim",
        "linear_certificate": {
            "variables": target.variables,
            "weights": tuple(map(str, certificate.weights)),
            "combined_coefficients": tuple(map(str, checked.combined.coefficients)),
            "combined_rhs": str(checked.combined.rhs),
            "valid": checked.valid,
            "nonzero_dependencies": checked.dependencies,
            "after_removing_special_drawing_facts": transferred.valid,
            "right_angle_target_initially_valid": special.valid,
            "right_angle_dependencies": special.dependencies,
            "right_angle_transfer": special_transfer,
            "right_angle_direct_check_after_deletion": deleted_special.valid,
            "nonright_countermodel_for_general_premises": {
                "a": 60, "b": 60, "c": 60, "u": 60, "v": 60,
            },
        },
        "finite_sign": {
            "domain_size": len(cases),
            "squared_side_lengths": [triangle.squared_sides() for triangle in cases],
            "right_angle_predicate": [triangle.is_right() for triangle in cases],
            "general_sign_covers_declared_domain": all_triangles.covers_domain(),
            "singleton_representative_covers_declared_domain": representative.covers_domain(),
            "counterexample_to_all_are_right": None if witness is None else witness.vertices,
            "scope": "three declared integer-coordinate triangles, not all Euclidean triangles",
        },
        "polynomial": {
            "identity": "x*(y+z) = x*y+x*z",
            "equal_canonical_forms": normalize(left) == normalize(right),
            "canonical_terms": [[monomial, str(coefficient)]
                                for monomial, coefficient in normalize(left).terms],
            "substitution": {name: str(value) for name, value in values.items()},
            "left_value": str(evaluate_expr(left, values)),
            "right_value": str(evaluate_expr(right, values)),
            "normalized_value": str(evaluate_polynomial(normalize(left), values)),
            "simultaneous_substitution_x_to_y_plus_1_and_y_to_2": {
                "result": "y+1" if simultaneous == Add(y, Const(1)) else "unexpected",
                "value_when_y_is_10": str(evaluate_expr(simultaneous, {"y": 10})),
            },
            "scope": "polynomials over Fraction; no division or rational-function simplification",
        },
    }


if __name__ == "__main__":
    print(json.dumps(examples(), ensure_ascii=False, indent=2))
