"""Independent finite audit: affine-coordinate oracle, not dot/cross reuse.

Run from the reproduction directory: python audit/independent_oracle.py
Only standard-library imports; fails with an explicit exception under -O/-OO.
"""
from collections import Counter
from decimal import Decimal
from fractions import Fraction as F
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from euclid_i3 import (Point, Certificate, verify, analytic_witness,
                       RationalWitnessUnavailable, rational_sqrt)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def p(raw):
    return Point(*raw)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def mul(k, a):
    return tuple(k * x for x in a)


def distance2(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def oracle(a, b, target2, d, e):
    """Find s from one nonzero coordinate; require BOTH affine equations.

    No production dot/cross/norm/domain helper is used. This directly checks
    the semantic contract, not the six named implementation predicates.
    """
    q = distance2(a, b)
    if not 0 < target2 < q:
        return False
    direction = tuple(y - x for x, y in zip(a, b))
    pivot = 0 if direction[0] else 1
    s = (e[pivot] - a[pivot]) / direction[pivot]
    return (0 < s < 1
            and e == add(a, mul(s, direction))
            and distance2(a, e) == target2
            and distance2(a, d) == target2)


def main():
    counts = Counter()
    failure_patterns = Counter()
    origins = ((F(0), F(0)), (F(13, 19), F(-17, 23)),
               (F(10**80), F(-10**80)))
    displacements = ((1, 0), (0, -2), (2, 1), (-1, 2), (3, -2),
                     (-2, -3), (4, 3), (F(1, 3), F(2, 5)), (0, 0))
    offsets = tuple(itertools.product(map(F, (-2, -1, F(-1, 2), 0,
                                               F(1, 2), 1, 2)), repeat=2))
    for a, v in itertools.product(origins, displacements):
        v = tuple(map(F, v))
        b = add(a, v)
        q = distance2(a, b)
        targets = (F(-1), F(0), F(1, 4), F(1, 2), F(1), F(2), F(4), q, q + 1)
        for w in offsets:
            e = add(a, w)
            ds = (e, add(a, (-w[1], w[0])), add(a, mul(2, w)), add(a, (F(1), F(0))))
            for target2, d in itertools.product(targets, ds):
                expected = oracle(a, b, target2, d, e)
                actual = verify(p(a), p(b), target2, Certificate(p(d), p(e)))
                require(actual.valid == expected, "lattice oracle disagreement")
                require(actual.as_dict()["valid"] == expected, "serialization disagreement")
                counts["coordinate_lattice_cases"] += 1
                counts["oracle_accepts" if expected else "oracle_rejects"] += 1
                if not actual.valid:
                    failure_patterns["|".join(actual.failures)] += 1

    # All selected q have irrational square roots, yet affine-rational E,D exist.
    for a, v, ratio in itertools.product(origins, ((2, 1), (3, 2), (-1, 3),
                            (F(2, 3), F(1, 5))), (F(1, 7), F(4, 11), F(12, 13))):
        v = tuple(map(F, v))
        b, e = add(a, v), add(a, mul(ratio, v))
        target2 = distance2(a, e)
        require(oracle(a, b, target2, e, e), "bad independent positive fixture")
        require(verify(p(a), p(b), target2, Certificate(p(e), p(e))).valid,
                "irrational lengths rational points rejected")
        try:
            analytic_witness(p(a), p(b), target2, p(e))
        except RationalWitnessUnavailable:
            counts["rational_certificate_accepted_builder_unsupported"] += 1
        else:
            raise RuntimeError("restricted builder unexpectedly supported irrational length")

    # Exact example added to the article: rational coordinates, irrational lengths.
    a, b, e = Point(0, 0), Point(2, 2), Point(1, 1)
    require(verify(a, b, F(2), Certificate(e, e)).valid,
            "article irrational-length example rejected")
    try:
        analytic_witness(a, b, F(2), e)
    except RationalWitnessUnavailable:
        counts["article_irrational_length_example"] += 1
    else:
        raise RuntimeError("article example unexpectedly generated")

    # Different generator parameters: integer Pythagorean vectors, not unit
    # direction fixtures; extra supplied-D direction is a 90-degree rotation.
    for a, mn, scale, ratio in itertools.product(origins, ((2, 1), (3, 2), (4, 1), (5, 3)),
                       (F(2, 7), F(11, 3)), (F(1, 7), F(4, 11), F(12, 13))):
        m, n = mn
        v = mul(scale, (F(m*m-n*n), F(2*m*n)))
        b, e = add(a, v), add(a, mul(ratio, v))
        w = mul(ratio, v)
        d = add(a, (-w[1], w[0]))
        target2 = distance2(a, e)
        cert = analytic_witness(p(a), p(b), target2, p(d))
        require((cert.e.x, cert.e.y) == e and (cert.d.x, cert.d.y) == d,
                "generator coordinate discrepancy")
        require(oracle(a, b, target2, d, e), "generated witness oracle failure")
        counts["independent_builder_cases"] += 1

    # No precision tolerance: three positive rational interior points separated
    # from endpoints by tiny exact quantities remain different from endpoints.
    tiny = F(1, 10**180)
    for ratio in (tiny, F(1, 2), 1-tiny):
        a, b = (F(10**180), F(-10**180)), (F(10**180)+1, F(-10**180))
        e = add(a, (ratio, F(0)))
        cert = analytic_witness(p(a), p(b), ratio**2)
        require((cert.e.x, cert.e.y) == e, "large translation/tiny ratio lost")
        require(oracle(a, b, ratio**2, (cert.d.x, cert.d.y), e), "extreme oracle failure")
        counts["extreme_exact_cases"] += 1

    a, b = Point(0, 0), Point(3, 0)
    cert = Certificate(Point(0, 1), Point(1, 0))
    invalid_values = (True, False, 1.0, float("nan"), float("inf"), "1", "1/2", None,
                      Decimal("1"), 1+0j, [1])
    for value in invalid_values:
        operations = (lambda: Point(value, 0), lambda: Point(0, value),
                      lambda: verify(a, b, value, cert),
                      lambda: analytic_witness(a, b, value), lambda: rational_sqrt(value))
        for operation in operations:
            try:
                operation()
            except TypeError:
                counts["unsupported_numeric_type_rejections"] += 1
            else:
                raise RuntimeError("unsupported numerical type not rejected")

    for target2, status in ((-1, "negative_squared_length"), (0, "zero_target"),
                             (9, "equal_target"), (10, "longer_target")):
        result = verify(a, b, target2, cert)
        require(not result.valid and result.domain == status, "strict input classification discrepancy")
        try:
            analytic_witness(a, b, target2)
        except ValueError as error:
            require(status in str(error), "builder misclassified invalid target")
            counts["non_strict_domain_rejections"] += 1
        else:
            raise RuntimeError("non-strict target not rejected")
    for target2 in (-1, 0, 1):
        result = verify(a, a, target2, cert)
        require(not result.valid and result.domain == "degenerate_segment",
                "degenerate classification priority mismatch")
        counts["degenerate_domain_cases"] += 1

    # API shape is not validated into a friendly schema; wrong objects raise
    # AttributeError/TypeError rather than producing a Verification result.
    for operation in (lambda: verify(None, b, 1, cert),
                      lambda: verify(a, b, 1, None),
                      lambda: verify(a, b, 1, Certificate(None, cert.e)),
                      lambda: verify(a, b, 1, Certificate(cert.d, (1, 0)))):
        try:
            operation()
        except (AttributeError, TypeError):
            counts["malformed_object_exceptions"] += 1
        else:
            raise RuntimeError("malformed object unexpectedly accepted")

    counts["total_checked_cases"] = sum(v for k, v in counts.items()
        if k not in ("oracle_accepts", "oracle_rejects"))
    print(json.dumps({"status": "PASS", "oracle": "coordinate-pivot affine parameter, exact Fraction distances",
                      "counts": dict(sorted(counts.items())),
                      "rejected_lattice_failure_patterns": dict(sorted(failure_patterns.items())),
                      "limitations": ["Finite inputs only; not a universal proof.",
                        "Malformed Python objects are exceptions, not a schema-safe verification API.",
                        "No ruler/compass operation history or I.2 construction is certified."]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
