"""Deterministic finite tests. All ordered nondegenerate grid pairs hit the API."""

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from euclid_i4 import (Certificate, InputError, Triangle, compare_sas, cross, dot,
                       json_exact, result_record, verify_certificate)


def ensure(condition, message):
    if not condition:
        raise RuntimeError(message)


def moved(source, certificate):
    return Triangle(*(certificate.apply(p) for p in source.vertices))


def examples():
    base = Triangle((0, 0), (3, 0), (0, 2))
    rotation = Certificate(((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5))), (F(7, 3), F(-5, 2)))
    reflection = Certificate(((1, 0), (0, -1)), (2, 3))
    sheared_source = Triangle((0, 0), (1, 0), (F(-1, 2), 1))
    shear = Certificate(((1, 1), (0, 1)), (0, 0))
    sheared_target = moved(sheared_source, shear)
    ssa_one = Triangle((0, 0), (4, 0), (1, 1))
    ssa_two = Triangle((0, 0), (4, 0), (3, 3))
    return json_exact({
        "rational_rotation": {"source": base.vertices, "target": moved(base, rotation).vertices,
                              "result": result_record(compare_sas(base, moved(base, rotation)))},
        "reflection_allowed": result_record(compare_sas(base, moved(base, reflection))),
        "reflection_direct_policy": result_record(compare_sas(base, moved(base, reflection), require_direct=True)),
        "wrong_scalene_correspondence": result_record(compare_sas(base, Triangle(base.a, base.c, base.b))),
        "shear": {"source": sheared_source.vertices, "target": sheared_target.vertices,
                  "Q": shear.q, "det_Q": shear.determinant,
                  "source_gram": sheared_source.gram, "target_gram": sheared_target.gram,
                  "result": result_record(compare_sas(sheared_source, sheared_target)),
                  "independent_certificate_checks": verify_certificate(sheared_source, sheared_target, shear)},
        "ssa_nonincluded_angle_counterexample": {
            "source": ssa_one.vertices, "target": ssa_two.vertices,
            "side_squares_AB_AC_BC": [ssa_one.side_squares, ssa_two.side_squares],
            "same_AB_squared": ssa_one.side_squares[0] == ssa_two.side_squares[0],
            "same_BC_squared": ssa_one.side_squares[2] == ssa_two.side_squares[2],
            "same_ray_AC": cross(ssa_one.v, ssa_two.v) == 0 and dot(ssa_one.v, ssa_two.v) > 0,
            "angle_explanation": "AB is unchanged; AC rays coincide positively. Angle at A is not the angle between AB and BC.",
            "result": result_record(compare_sas(ssa_one, ssa_two)),
        },
    })


def run_enumeration():
    vectors = list(product(range(-2, 3), repeat=2))
    triangles, rejected = [], 0
    for u, v in product(vectors, repeat=2):
        try:
            triangles.append(Triangle((0, 0), u, v))
        except InputError:
            rejected += 1
    counts = Counter()
    for source, target in product(triangles, repeat=2):
        # Independent expected Gram data using raw integer coordinates.
        a, b = source.b, source.c
        c, d = target.b, target.c
        expected = (int(a[0])**2 + int(a[1])**2,
                    int(b[0])**2 + int(b[1])**2,
                    int(a[0])*int(b[0]) + int(a[1])*int(b[1])) == (
                    int(c[0])**2 + int(c[1])**2,
                    int(d[0])**2 + int(d[1])**2,
                    int(c[0])*int(d[0]) + int(c[1])*int(d[1]))
        r = compare_sas(source, target)
        ensure(r.accepted == expected, "grid classification disagrees with integer oracle")
        counts["ordered_triangle_pairs"] += 1
        if r.congruent:
            ensure(all(dict(r.checks).values()), "positive grid certificate failed")
            ensure(r.certificate.determinant == target.determinant / source.determinant,
                   "orientation ratio failed")
            counts["accepted_sas"] += 1
            counts["direct_isometries" if r.orientation_preserving else "orientation_reversing_isometries"] += 1
        else:
            counts["rejected_sas"] += 1
    transforms = [
        Certificate(((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5))), (F(7, 3), F(-5, 2))),
        Certificate(((F(3, 5), F(4, 5)), (F(4, 5), F(-3, 5))), (F(-2, 7), F(11, 3))),
    ]
    rational_count = 0
    for source, cert in product(triangles, transforms):
        target = moved(source, cert)
        r = compare_sas(source, target, require_direct=True)
        ensure(r.certificate == cert and r.congruent, "rational transform not recovered")
        ensure(r.accepted == (cert.determinant == 1), "direct-motion policy failed")
        rational_count += 1
    expected_counts = {"ordered_triangle_pairs": 246016, "accepted_sas": 4096,
                       "direct_isometries": 2048, "orientation_reversing_isometries": 2048,
                       "rejected_sas": 241920}
    ensure(dict(counts) == expected_counts, "unexpected finite-grid counts")
    ensure(rejected == 129 and len(triangles) == 496 and rational_count == 992,
           "unexpected input or rational-transform count")
    return {
        "schema_version": 1,
        "model": "modern real inner-product plane, exact rational coordinate samples",
        "scope": "finite exhaustive grid test plus rational-transform checks; not a universal formal proof",
        "angle_scope": "Gram entries and vertex angle data, no independent arbitrary angle function",
        "grid": {"coordinate_min": -2, "coordinate_max": 2, "anchor": [0, 0],
                 "vectors": 25, "ordered_vector_pairs": 625,
                 "degenerate_inputs_rejected": rejected, "nondegenerate_triangles": len(triangles)},
        "exhaustive_grid_api_results": dict(counts),
        "rational_transform_cases": {"total": rational_count, "direct": 496, "reflection": 496,
                                     "translation_nonzero": True, "all_recovered_exactly": True},
        "examples": examples(),
    }


if __name__ == "__main__":
    report = run_enumeration()
    destination = Path("results/enumeration.json")
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"grid": report["grid"],
                      "exhaustive_grid_api_results": report["exhaustive_grid_api_results"],
                      "rational_transform_cases": report["rational_transform_cases"]},
                     ensure_ascii=False, indent=2))
    print("Wrote results/enumeration.json")
