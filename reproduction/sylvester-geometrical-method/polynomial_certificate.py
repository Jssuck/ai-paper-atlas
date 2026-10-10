"""Exact polynomial certificate, represented by integer exponent-coefficient maps.

Independent of SymPy and of finite substitution tests. Zero output establishes
this polynomial identity; applying it to geometry still requires domain and
positivity reasoning, which is documented separately.
"""
from __future__ import annotations


def add(*polynomials):
    out = {}
    for p in polynomials:
        for exponent, coefficient in p.items():
            out[exponent] = out.get(exponent, 0) + coefficient
    return {e: c for e, c in out.items() if c}


def scale(p, scalar):
    return {e: c * scalar for e, c in p.items() if c * scalar}


def mul(*polynomials):
    out = {(0, 0, 0): 1}
    for p in polynomials:
        product = {}
        for e, c in out.items():
            for f, d in p.items():
                exponent = tuple(x + y for x, y in zip(e, f))
                product[exponent] = product.get(exponent, 0) + c * d
        out = {e: c for e, c in product.items() if c}
    return out


def certificate():
    a, b, c = ({(1, 0, 0): 1}, {(0, 1, 0): 1}, {(0, 0, 1): 1})
    aa, bb = mul(a, a), mul(b, b)
    ac2, bc2 = mul(add(a, c), add(a, c)), mul(add(b, c), add(b, c))
    left = add(mul(b, c, add(bc2, scale(aa, -1)), ac2),
               scale(mul(a, c, add(ac2, scale(bb, -1)), bc2), -1))
    P = add(mul(a, a, b), mul(a, b, b), scale(mul(a, b, c), 3),
            mul(a, c, c), mul(b, c, c), mul(c, c, c))
    right = mul(add(b, scale(a, -1)), c, add(a, b, c), P)
    residual = add(left, scale(right, -1))
    return {"left_nonzero_terms": len(left), "right_nonzero_terms": len(right),
            "residual_nonzero_terms": len(residual), "identity_verified": not residual,
            "arithmetic": "exact Python integers; coefficient comparison"}


if __name__ == '__main__':
    import json
    result = certificate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["identity_verified"]:
        raise SystemExit(1)
