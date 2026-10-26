"""Independent finite audit, using raw-coordinate squared distances as oracle.

Run from the reproduction directory:
    python independent-review/check_independently.py

This imports the public API under test, not its vector/matrix/Gram helpers.
It is an independent testing pass, not a formal proof or human peer review.
"""

from collections import Counter
from decimal import Decimal
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from euclid_i4 import (  # noqa: E402
    Certificate, InputError, Triangle, compare_sas, verify_certificate,
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def distance2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def sides(vertices):
    a, b, c = vertices
    return distance2(a, b), distance2(a, c), distance2(b, c)


def signed_area2(vertices):
    a, b, c = vertices
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))


def scalar_map(cert, p):
    # Do not use Certificate.apply, matvec, dot, or any other tested helper.
    (a, b), (c, d) = cert.q
    h, k = cert.t
    return a * p[0] + b * p[1] + h, c * p[0] + d * p[1] + k


def metric_angle_data(vertices):
    # Polarization using three pairwise distances, not stored Gram data.
    ab, ac, bc = sides(vertices)
    return ((ab, F(ab + ac - bc) / 2, ac),
            (ab, F(ab + bc - ac) / 2, bc),
            (ac, F(ac + bc - ab) / 2, bc))


def validate_witness(source, target, cert):
    # An affine map is orthogonal iff images of (0,0), (1,0), (0,1)
    # have squared distances 1,1,2. This uses the separate distance oracle.
    image_basis = tuple(scalar_map(cert, p) for p in ((0, 0), (1, 0), (0, 1)))
    require(sides(image_basis) == (1, 1, 2), "witness is not an isometry")
    require(tuple(scalar_map(cert, p) for p in source) == target,
            "witness fails the declared vertex correspondence")
    require(sides(source) == sides(target), "witness sides mismatch")
    require(metric_angle_data(source) == metric_angle_data(target),
            "distance-derived angle data mismatch")
    # Exercise boundary and interior convex combinations, plus a point outside.
    # The universal closed-triangle argument remains the prose algebraic proof.
    for weights in ((F(1), F(0), F(0)), (F(0), F(1), F(0)),
                    (F(0), F(0), F(1)), (F(1, 2), F(1, 2), F(0)),
                    (F(1, 6), F(1, 3), F(1, 2)), (F(-1), F(1), F(1))):
        p = tuple(sum(w * v[j] for w, v in zip(weights, source)) for j in (0, 1))
        q = tuple(sum(w * v[j] for w, v in zip(weights, target)) for j in (0, 1))
        require(scalar_map(cert, p) == q, "affine combination mismatch")
    (a, b), (c, d) = cert.q
    determinant = a * d - b * c
    require(determinant in (-1, 1), "invalid determinant")
    require(determinant == F(signed_area2(target)) / signed_area2(source),
            "oriented-area ratio mismatch")
    # Exact inverse from orthogonality, tested away from the original vertices.
    for p in ((F(-7, 11), F(9, 13)), (F(5, 3), F(-4, 7))):
        image = scalar_map(cert, p)
        dx, dy = image[0] - cert.t[0], image[1] - cert.t[1]
        require((a * dx + c * dy, b * dx + d * dy) == p,
                "transpose inverse did not recover arbitrary probe point")


def exhaustive_grid():
    vertices = list(product(range(-2, 3), repeat=2))
    cases, degenerate = [], 0
    for b, c in product(vertices, repeat=2):
        raw = ((0, 0), b, c)
        if signed_area2(raw) == 0:
            degenerate += 1
            try:
                Triangle(*raw)
            except InputError:
                pass
            else:
                raise RuntimeError("degenerate grid input accepted")
        else:
            cases.append((raw, Triangle(*raw), sides(raw)))
    counts = Counter()
    for (raw_s, obj_s, metric_s), (raw_t, obj_t, metric_t) in product(cases, repeat=2):
        # The oracle is three labelled squared side lengths. It never reads
        # triangle.gram or calls the implementation's scalar/matrix helpers.
        expected = metric_s == metric_t
        result = compare_sas(obj_s, obj_t)
        require(result.congruent == expected and result.accepted == expected,
                "classification disagrees with squared-side oracle")
        counts["ordered_pairs"] += 1
        if expected:
            validate_witness(raw_s, raw_t, result.certificate)
            direct = signed_area2(raw_s) * signed_area2(raw_t) > 0
            require(result.orientation_preserving == direct, "orientation mismatch")
            constrained = compare_sas(obj_s, obj_t, require_direct=True)
            require(constrained.congruent and constrained.accepted == direct,
                    "reflection policy conflates congruence and acceptance")
            counts["congruent"] += 1
            counts["direct" if direct else "reversing"] += 1
        else:
            require(result.certificate is None and result.reason == "sas_mismatch",
                    "mismatch returned a certificate or incorrect reason")
            counts["not_congruent_under_fixed_labels"] += 1
    return {"nondegenerate_triangles": len(cases), "degenerate_rejected": degenerate,
            **dict(counts)}, cases


def transformed_cases(cases):
    count = 0
    for raw, _, _ in cases:
        # A rational rotation and a rational reflection, written as direct
        # coordinate formulas rather than generated through Certificate.apply.
        targets = (
            tuple((F(3, 5) * x - F(4, 5) * y + F(7, 3),
                   F(4, 5) * x + F(3, 5) * y - F(5, 2)) for x, y in raw),
            tuple((F(3, 5) * x + F(4, 5) * y - F(2, 7),
                   F(4, 5) * x - F(3, 5) * y + F(11, 3)) for x, y in raw),
        )
        for direct, target in zip((True, False), targets):
            result = compare_sas(raw, target, require_direct=True)
            require(result.congruent and result.accepted == direct,
                    "rational transformation or policy failed")
            validate_witness(raw, target, result.certificate)
            count += 1
    # Both origins now vary, avoiding accidental reliance on source A=(0,0).
    additional = 0
    for offset in ((F(1, 7), F(-2, 3)), (10**40, F(1, 10**40))):
        for _, source, _ in cases[::31]:
            raw = tuple((x + offset[0], y + offset[1]) for x, y in source.vertices)
            for flip in (1, -1):
                target = tuple((F(5, 13) * x - F(12, 13) * flip * y - F(3, 2),
                                F(12, 13) * x + F(5, 13) * flip * y + F(8, 9))
                               for x, y in raw)
                result = compare_sas(raw, target)
                require(result.congruent, "nonzero-origin rational transform failed")
                validate_witness(raw, target, result.certificate)
                additional += 1
    return {"grid_source_transforms": count, "nonzero_origin_transforms": additional}


def exact_article_examples():
    base = ((0, 0), (3, 0), (0, 4))
    rotation = ((2, -1), (2, 2), (-2, -1))
    reflection = ((10, 1), (13, 1), (10, -3))
    r = compare_sas(base, rotation)
    validate_witness(base, rotation, r.certificate)
    require(r.certificate.q == ((0, -1), (1, 0)) and r.certificate.t == (2, -1),
            "article rotation certificate wrong")
    require(sides(rotation) == (9, 16, 25), "article rotation sides wrong")
    rr = compare_sas(base, reflection, require_direct=True)
    require(rr.congruent and not rr.accepted and rr.certificate.q == ((1, 0), (0, -1)),
            "article reflection counterexample wrong")
    validate_witness(base, reflection, rr.certificate)
    no_angle = ((0, 0), (3, 0), (F(12, 5), F(16, 5)))
    require(sides(no_angle) == (9, 16, F(53, 5)), "two-side example wrong")
    require(compare_sas(base, no_angle).sas_equal == (True, True, False),
            "two-side counterexample misclassified")
    ssa1 = ((0, 0), (1, F(3, 4)), (5, 0))
    ssa2 = ((0, 0), (F(27, 5), F(81, 20)), (5, 0))
    require(sides(ssa1) == (F(25, 16), 25, F(265, 16)), "first SSA data wrong")
    require(sides(ssa2) == (F(729, 16), 25, F(265, 16)), "second SSA data wrong")
    require(ssa2[1][0] / ssa1[1][0] == ssa2[1][1] / ssa1[1][1] == F(27, 5),
            "SSA rays are not positively proportional")
    require(not compare_sas(ssa1, ssa2).congruent, "SSA accidentally accepted")
    # Compare squared cosines: both dots positive; unequal squared values
    # therefore establish unequal ordinary angles without evaluating acos.
    require(F(1, 2) != F(1, 5), "equal-dot counterexample has equal angles")
    dot_one = metric_angle_data(((0, 0), (1, 0), (1, 1)))[0]
    dot_two = metric_angle_data(((0, 0), (2, 0), (F(1, 2), 1)))[0]
    require(dot_one[1] == dot_two[1] == 1, "equal-dot example incorrect")
    require(dot_one[1] ** 2 / (dot_one[0] * dot_one[2]) == F(1, 2), "first cosine wrong")
    require(dot_two[1] ** 2 / (dot_two[0] * dot_two[2]) == F(1, 5), "second cosine wrong")
    require(not compare_sas(base, (base[0], base[2], base[1])).congruent,
            "article wrong-correspondence example accepted")
    return {"rotation": "exact Q,t and all side squares verified",
            "reflection": "congruent; direct-only rejected",
            "two_sides_only_BC_squared": "53/5",
            "ssa_BC_squared": "265/16", "ssa_AB_squared": ["25/16", "729/16"],
            "equal_dot_squared_cosines": ["1/2", "1/5"],
            "wrong_correspondence": "rejected"}


def adversarial_and_input_cases():
    base = ((0, 0), (3, 0), (0, 4))
    rejected = 0

    def must_reject(call):
        nonlocal rejected
        try:
            call()
        except InputError:
            rejected += 1
        else:
            raise RuntimeError("invalid input did not raise InputError")

    class IntegerSubclass(int):
        pass

    class FractionSubclass(F):
        pass

    bad_scalars = (True, False, 0.0, float("nan"), float("inf"), float("-inf"),
                   "1/2", Decimal("0.5"), 1 + 0j, None, [], {}, IntegerSubclass(1),
                   FractionSubclass(1, 2))
    for value in bad_scalars:
        must_reject(lambda value=value: compare_sas(((value, 0), (3, 0), (0, 4)), base))
        must_reject(lambda value=value: Certificate(((1, value), (0, 1)), (0, 0)))
    for value in (None, {}, "abc", [], [(0, 0)], iter(base)):
        must_reject(lambda value=value: compare_sas(value, base))
    for value in ((0,), (0, 0, 0), "00", {0: 0, 1: 0}, iter((0, 0))):
        must_reject(lambda value=value: compare_sas((value, (3, 0), (0, 4)), base))
    for invalid in (((0, 0), (1, 0), (2, 0)), ((0, 0), (0, 0), (1, 2))):
        must_reject(lambda invalid=invalid: compare_sas(invalid, base))
        must_reject(lambda invalid=invalid: compare_sas(base, invalid))
    for value in (None, 0, 1, "false"):
        must_reject(lambda value=value: compare_sas(base, base, require_direct=value))
    must_reject(lambda: verify_certificate(base, base, {"q": ((1, 0), (0, 1)), "t": (0, 0)}))
    for representation in (list(map(list, base)), tuple(map(tuple, base)),
                           tuple(tuple(F(x) for x in point) for point in base), Triangle(*base)):
        require(compare_sas(representation, base).accepted, "valid representation rejected")
    # A determinant-one shear maps vertices and preserves area, yet is not an isometry.
    shear = Certificate(((1, 1), (0, 1)), (0, 0))
    source = ((0, 0), (1, 0), (F(-1, 2), 1))
    target = ((0, 0), (1, 0), (F(1, 2), 1))
    checks = verify_certificate(source, target, shear)
    require(all(checks[k] for k in ("maps_A_to_D", "maps_B_to_E", "maps_C_to_F")),
            "shear should match all three declared vertices")
    require(not checks["orthogonal"] and not all(checks.values()), "shear certificate accepted")
    forged = 0
    for q, t in ((((2, 0), (0, 2)), (0, 0)), (((1, 0), (0, 0)), (0, 0)),
                 (((1, 0), (0, 1)), (1, 0)), (((0, -1), (1, 0)), (0, 0))):
        require(not all(verify_certificate(base, base, Certificate(q, t)).values()),
                "forged certificate passed all checks")
        forged += 1
    # All six unilateral label choices: only identity works for this scalene input.
    unilateral = sum(compare_sas(base, tuple(base[i] for i in p)).accepted
                     for p in permutations(range(3)))
    require(unilateral == 1, "scalene triangle accepted a wrong labelling")
    equal_leg = ((0, 0), (1, 0), (0, 1))
    require(compare_sas(equal_leg, (equal_leg[0], equal_leg[2], equal_leg[1])).congruent,
            "valid symmetry mislabeled as mismatch")
    return {"invalid_input_calls_rejected": rejected, "valid_representations": 4,
            "false_certificates_rejected": forged + 1,
            "unilateral_scalene_permutations_checked": 6,
            "unilateral_scalene_permutations_accepted": unilateral,
            "symmetric_relabelling_accepted": True}


def main():
    grid, cases = exhaustive_grid()
    report = {
        "schema_version": 1,
        "python_version": platform.python_version(),
        "optimization_level": sys.flags.optimize,
        "oracle": "labelled raw-coordinate squared distances; separate scalar certificate checks",
        "scope": "finite independent tests, not a formal proof or full Euclidean-geometry verification",
        "grid": grid,
        "transforms": transformed_cases(cases),
        "article_examples": exact_article_examples(),
        "adversarial_and_inputs": adversarial_and_input_cases(),
        "source_sha256": {name: sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ("euclid_i4.py", "test_euclid_i4.py", "enumerate_cases.py")},
        "audit_script_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "result": "PASS",
    }
    destination = Path(__file__).with_name("results.json")
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
