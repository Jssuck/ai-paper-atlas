"""Deterministic finite families; evidence, not a universal theorem."""
from fractions import Fraction as F
from euclid_i3 import Point, Certificate, analytic_witness, verify

DIRECTIONS = (
    Point(1, 0), Point(0, 1), Point(-1, 0), Point(0, -1),
    Point(F(3, 5), F(4, 5)), Point(F(-3, 5), F(4, 5)),
    Point(F(5, 13), F(-12, 13)), Point(F(-8, 17), F(-15, 17)),
)
ORIGINS = (Point(0, 0), Point(2, -3), Point(F(-7, 3), F(11, 5)))
LENGTHS = (F(1), F(5, 2), F(13, 7), F(10**12), F(1, 10**12))
RATIOS = (F(1, 10), F(1, 3), F(1, 2), F(2, 3), F(9, 10))


def families():
    for direction in DIRECTIONS:
        for a in ORIGINS:
            for length in LENGTHS:
                b = a + direction.scale(length)
                for ratio in RATIOS:
                    yield a, b, (ratio * length)**2, ratio


def mutations(a, b, certificate):
    w = certificate.e - a
    # A rational rotation preserves length and positive projected position;
    # only the incidence-on-AB test rejects this specific mutation.
    rotated = Point(F(3, 5)*w.x-F(4, 5)*w.y,
                    F(4, 5)*w.x+F(3, 5)*w.y)
    return {
        "opposite_circle_point": Certificate(certificate.d, a-w),
        "off_line_same_distance": Certificate(certificate.d, a+rotated),
        "beyond_B": Certificate(certificate.d, a+(b-a).scale(2)),
        "incorrect_transferred_radius": Certificate(a+(certificate.d-a).scale(2), certificate.e),
    }


def run_families():
    accepted = 0
    rejected = {key: 0 for key in mutations(Point(0, 0), Point(2, 0),
                Certificate(Point(0, 1), Point(1, 0)))}
    for a, b, c, ratio in families():
        certificate = analytic_witness(a, b, c)
        if certificate.e != a+(b-a).scale(ratio):
            raise RuntimeError("witness disagrees with independent family ratio")
        if not verify(a, b, c, certificate).valid:
            raise RuntimeError("valid family certificate rejected")
        accepted += 1
        for kind, mutant in mutations(a, b, certificate).items():
            if verify(a, b, c, mutant).valid:
                raise RuntimeError("invalid mutation accepted: " + kind)
            rejected[kind] += 1
    return {"valid_certificates_accepted": accepted,
            "invalid_certificates_rejected": sum(rejected.values()),
            "rejections_by_kind": rejected,
            "family_dimensions": {"unit_directions": len(DIRECTIONS),
                                  "origins": len(ORIGINS),
                                  "rational_lengths": len(LENGTHS),
                                  "strict_ratios": len(RATIOS)}}


if __name__ == "__main__":
    import json
    print(json.dumps(run_families(), indent=2))
