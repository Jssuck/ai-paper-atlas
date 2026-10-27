"""Deterministic finite teaching inputs and deliberately invalid certificates."""
from dataclasses import replace
from fractions import Fraction as R
from geometry import (Q3, point, add, sub, scale, construct, check_certificate,
                      accepted, encode, dist2)


def transform(p, origin, scale_factor, rotation, reflected=False):
    x, y = p
    if reflected:
        x = -x
    cosine, sine = rotation
    return add(origin, scale(scale_factor, (cosine * x - sine * y, sine * x + cosine * y)))


def positive_cases():
    """3 origins × 24 nonzero rational vectors × 5 similarities × 2 branches."""
    values = [R(-3), R(-1, 2), R(0), R(2, 3), R(5)]
    origins = [point(0, 0), point(R(2, 7), R(-3, 11)), point(-17, 29)]
    transforms = [
        ('identity', R(1), (R(1), R(0)), False),
        ('rational_rotation_and_scale', R(7, 3), (R(3, 5), R(4, 5)), False),
        ('reflection', R(1), (R(0), R(1)), True),
        ('tiny_1e-80', R(1, 10**80), (R(3, 5), R(4, 5)), False),
        ('large_1e80', R(10**80), (R(3, 5), R(4, 5)), True),
    ]
    for origin_index, origin in enumerate(origins):
        for x in values:
            for y in values:
                if x == 0 and y == 0:
                    continue
                for family, factor, rotation, reflected in transforms:
                    a = transform(point(0, 0), origin, factor, rotation, reflected)
                    b = transform(point(x, y), origin, factor, rotation, reflected)
                    for branch in (1, -1):
                        yield f'{family}/origin{origin_index}/v={x},{y}/branch={branch}', family, a, b, branch


def rejected_cases():
    a, b = point(0, 0), point(2, 0)
    cert = construct(a, b)
    # Equal distances alone are insufficient: C is off AB yet CA=CB.
    yield 'equidistant_but_not_midpoint', a, b, replace(cert, d=cert.c)
    # Reverse the same supporting line: equal angles still hold but ray is outward.
    reversed_f = sub(scale(2, cert.c), cert.f)
    yield 'reversed_equal_angle_ray', a, b, replace(cert, f=reversed_f, s=-cert.s)
    yield 'boundary_ray_not_bisector', a, b, replace(cert, f=a, d=a, s=Q3(1), t=Q3(0))
    yield 'wrong_interior_ray', a, b, replace(cert, f=point(R(1, 2), 0))
    yield 'zero_ray', a, b, replace(cert, f=cert.c)
    yield 'tampered_D', a, b, replace(cert, d=point(R(3, 4), 0))
    yield 'tampered_ray_parameter', a, b, replace(cert, s=Q3(R(1, 3)))
    yield 'tampered_segment_parameter', a, b, replace(cert, t=Q3(R(1, 3)))
    yield 'tampered_branch', a, b, replace(cert, branch=-1)
    yield 'tampered_C', a, b, replace(cert, c=point(1, 2))
    yield 'certificate_rebound_to_other_input', a, point(4, 0), cert
    yield 'coincident_input', a, a, cert


def example_report():
    report = []
    for label, a, b, branch in (
        ('horizontal_upper', point(0, 0), point(2, 0), 1),
        ('horizontal_lower', point(0, 0), point(2, 0), -1),
        ('oblique_rational', point(R(1, 3), R(-2, 5)), point(R(7, 3), R(8, 5)), 1),
        ('vertical', point(-2, 7), point(-2, 13), -1),
        ('article_hand_calculation', point(0, 0), point(6, 0), 1),
        ('article_exercise_7', point(-2, 1), point(4, 9), 1),
        ('tiny', point(0, 0), point(R(1, 10**80), R(2, 10**80)), 1),
        ('large_translated', point(10**80, -10**80), point(10**80 + 2, -10**80 + 4), -1),
    ):
        cert = construct(a, b, branch)
        report.append({'name': label, 'A': encode(a), 'B': encode(b),
                       'certificate': encode(cert), 'checks': check_certificate(a, b, cert),
                       'accepted': accepted(a, b, cert),
                       'squared_lengths': {name: encode(value) for name, value in {
                           'CA': dist2(cert.c, a), 'CB': dist2(cert.c, b),
                           'CD': dist2(cert.c, cert.d), 'AD': dist2(a, cert.d),
                           'BD': dist2(b, cert.d)}.items()}})
    return report
