#!/usr/bin/env python3
"""Independent finite checks for Peirce 1880, printed pp. 53–56.

Original operations -> this script:
    ab -> E(a,b); left superscript a on b -> G(a,b);
    right superscript b on a -> P(a,b); a circle b -> T(a,b).
All source formula IDs are mapped in peirce-relative-formulae.zh-CN.md.
This checks the central equalities, not a literal parse of every typographical
variant or negative-table entry. No source PDF or third-party code is included.

Run: python supplemental_relation_checks.py --json evidence/supplemental-relation-checks.json
No packages beyond Python's standard library are required.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
from functools import reduce
from pathlib import Path

N = 2
TOP = (1 << (N * N)) - 1
RELATIONS = range(TOP + 1)


def neg(a):
    return TOP ^ a


def holds(a, x, y):
    return bool(a & (1 << (x * N + y)))


def E(a, b):
    """Exists y: a(x,y) and b(y,z), encoded row-major as four bits."""
    return sum(
        1 << (x * N + z)
        for x in range(N) for z in range(N)
        if any(holds(a, x, y) and holds(b, y, z) for y in range(N))
    )


def G(a, b):
    return neg(E(a, neg(b)))


def P(a, b):
    return neg(E(neg(a), b))


def T(a, b):
    return E(neg(a), neg(b))


def atoms(a):
    """All singleton relations contained in a, including none when a=0."""
    return [1 << k for k in range(N * N) if a & (1 << k)]


def simples(a):
    """All coatoms containing a: complements of singleton atoms outside a."""
    return [TOP ^ (1 << k) for k in range(N * N) if not a & (1 << k)]


def cap(relations):
    return reduce(int.__and__, relations, TOP)


def cup(relations):
    return reduce(int.__or__, relations, 0)


def dom_total(a):
    return all(any(holds(a, x, y) for y in range(N)) for x in range(N))


def ran_total(a):
    return all(any(holds(a, x, y) for x in range(N)) for y in range(N))


def pairs(a):
    return [[x, y] for x in range(N) for y in range(N) if holds(a, x, y)]


# p55: row-major in the printed two-column table: left1, right1, left2, ...
DISTRIBUTION_SIMPLE = [
    lambda a,b,c: (E(a|b,c), E(a,c)|E(b,c)),
    lambda a,b,c: (E(a,b|c), E(a,b)|E(a,c)),
    lambda a,b,c: (P(a&b,c), P(a,c)&P(b,c)),
    lambda a,b,c: (P(a,b|c), P(a,b)&P(a,c)),
    lambda a,b,c: (G(a|b,c), G(a,c)&G(b,c)),
    lambda a,b,c: (G(a,b&c), G(a,b)&G(a,c)),
    lambda a,b,c: (T(a&b,c), T(a,c)|T(b,c)),
    lambda a,b,c: (T(a,b&c), T(a,b)|T(a,c)),
]

# p ranges over ALL 16 binary relations, not one arbitrarily selected relation.
DISTRIBUTION_DEVELOPED = [
    lambda a,b,c: (E(a&b,c), cap(E(a,c&p)|E(b,c&neg(p)) for p in RELATIONS)),
    lambda a,b,c: (E(a,b&c), cap(E(a&p,b)|E(a&neg(p),c) for p in RELATIONS)),
    lambda a,b,c: (P(a|b,c), cup(P(a,c&p)&P(b,c&neg(p)) for p in RELATIONS)),
    lambda a,b,c: (P(a,b&c), cup(P(a|p,b)&P(a|neg(p),c) for p in RELATIONS)),
    lambda a,b,c: (G(a&b,c), cup(G(a,c|p)&G(b,c|neg(p)) for p in RELATIONS)),
    lambda a,b,c: (G(a,b|c), cup(G(a&p,b)&G(a&neg(p),c) for p in RELATIONS)),
    lambda a,b,c: (T(a|b,c), cap(T(a,c|p)|T(b,c|neg(p)) for p in RELATIONS)),
    lambda a,b,c: (T(a,b|c), cap(T(a|p,b)|T(a|neg(p),c) for p in RELATIONS)),
]

# p56 simple table: entire left column, then entire right column.
ASSOCIATION_SIMPLE = [
    lambda a,b,c: (E(a,E(b,c)), E(E(a,b),c)),
    lambda a,b,c: (P(a,T(b,c)), G(T(a,b),c)),
    lambda a,b,c: (P(a,E(b,c)), P(P(a,b),c)),
    lambda a,b,c: (E(a,T(b,c)), T(G(a,b),c)),
    lambda a,b,c: (G(a,P(b,c)), P(G(a,b),c)),
    lambda a,b,c: (T(a,G(b,c)), T(P(a,b),c)),
    lambda a,b,c: (G(a,G(b,c)), G(E(a,b),c)),
    lambda a,b,c: (T(a,P(b,c)), E(T(a,b),c)),
]

# Class1/3 arguments are a,b,c; Class2/4 arguments are c,d,e.
# A and Q are atom indices, s is a coatom index, as defined above.
ASSOCIATION_DEVELOPED = {
    1: [
        lambda a,b,c: (G(a,E(b,c)), cap(E(G(A,b),c) for A in atoms(a))),
        lambda a,b,c: (T(a,E(b,c)), cup(P(T(s,b),c) for s in simples(a))),
        lambda a,b,c: (P(a,P(b,c)), cap(E(P(s,b),c) for s in simples(a))),
        lambda a,b,c: (E(a,P(b,c)), cup(P(E(A,b),c) for A in atoms(a))),
    ],
    2: [
        lambda c,d,e: (P(T(c,d),e), cap(T(c,E(d,Q)) for Q in atoms(e))),
        lambda c,d,e: (T(T(c,d),e), cup(P(c,G(d,s)) for s in simples(e))),
        lambda c,d,e: (G(P(c,d),e), cap(T(c,T(d,s)) for s in simples(e))),
        lambda c,d,e: (E(P(c,d),e), cup(P(c,P(d,Q)) for Q in atoms(e))),
    ],
    3: [
        lambda a,b,c: (T(a,T(b,c)), cup(G(P(s,b),c) for s in simples(a))),
        lambda a,b,c: (G(a,T(b,c)), cap(T(E(A,b),c) for A in atoms(a))),
        lambda a,b,c: (E(a,G(b,c)), cup(G(G(A,b),c) for A in atoms(a))),
        lambda a,b,c: (P(a,G(b,c)), cap(T(T(s,b),c) for s in simples(a))),
    ],
    4: [
        lambda c,d,e: (T(E(c,d),e), cup(G(c,T(d,s)) for s in simples(e))),
        lambda c,d,e: (P(E(c,d),e), cap(E(c,P(d,Q)) for Q in atoms(e))),
        lambda c,d,e: (E(G(c,d),e), cup(G(c,E(d,Q)) for Q in atoms(e))),
        lambda c,d,e: (G(G(c,d),e), cap(E(c,G(d,s)) for s in simples(e))),
    ],
}

CONDITIONS = {
    1: ("ran(c)=U", lambda c: ran_total(c)),
    2: ("dom(not c)=U", lambda c: dom_total(neg(c))),
    3: ("ran(not c)=U", lambda c: ran_total(neg(c))),
    4: ("dom(c)=U", lambda c: dom_total(c)),
}


def check_operation_oracles():
    """Check complement definitions against separately written direct quantifiers."""
    failures = 0
    for a,b in itertools.product(RELATIONS, repeat=2):
        direct = {
            "E": sum(1 << (x*N+z) for x in range(N) for z in range(N)
                     if any(holds(a,x,y) and holds(b,y,z) for y in range(N))),
            "G": sum(1 << (x*N+z) for x in range(N) for z in range(N)
                     if all(not holds(a,x,y) or holds(b,y,z) for y in range(N))),
            "P": sum(1 << (x*N+z) for x in range(N) for z in range(N)
                     if all(not holds(b,y,z) or holds(a,x,y) for y in range(N))),
            "T": sum(1 << (x*N+z) for x in range(N) for z in range(N)
                     if any(not holds(a,x,y) and not holds(b,y,z) for y in range(N))),
        }
        for name,fn in [("E",E),("G",G),("P",P),("T",T)]:
            failures += fn(a,b) != direct[name]
    return {"operation_evaluations": 4*16**2, "failures": failures}


def check_unconditional(prefix, functions):
    rows = []
    for i,fn in enumerate(functions, 1):
        failures = 0
        first = None
        for a,b,c in itertools.product(RELATIONS, repeat=3):
            left,right = fn(a,b,c)
            if left != right:
                failures += 1
                if first is None:
                    first = {"inputs": [a,b,c], "left": left, "right": right}
        row = {"formula": f"{prefix}{i}", "assignments": 16**3,
               "failures": failures, "first_failure": first}
        rows.append(row)
        print(f"{row['formula']}: {row['assignments']} assignments; failures={failures}")
    return rows


def check_conditional():
    results = []
    for cls in range(1,5):
        label,premise = CONDITIONS[cls]
        actual_good = set(RELATIONS)
        rows = []
        for i,fn in enumerate(ASSOCIATION_DEVELOPED[cls], 1):
            conditional_cases = conditional_failures = outside_failures = 0
            first_outside = None
            for c,u,v in itertools.product(RELATIONS, repeat=3):
                left,right = fn(u,v,c) if cls in (1,3) else fn(c,u,v)
                if premise(c):
                    conditional_cases += 1
                    conditional_failures += left != right
                elif left != right:
                    outside_failures += 1
                    if first_outside is None:
                        first_outside = {"c": c, "other_inputs": [u,v],
                                         "left": left, "right": right}
                if left != right:
                    actual_good.discard(c)
            row = {"formula": f"C{cls}.{i}", "all_assignments": 16**3,
                   "assignments_satisfying_premise": conditional_cases,
                   "conditional_failures": conditional_failures,
                   "failures_outside_premise": outside_failures,
                   "first_outside_counterexample": first_outside}
            rows.append(row)
            print(f"{row['formula']}: all={16**3}; premise={conditional_cases}; "
                  f"conditional failures={conditional_failures}; "
                  f"outside failures={outside_failures}")
        expected_good = {c for c in RELATIONS if premise(c)}
        result = {"class": cls, "modern_sufficient_condition": label,
                  "formulas": rows, "good_c_masks": sorted(actual_good),
                  "condition_c_masks": sorted(expected_good),
                  "finite_class_domain_matches": actual_good == expected_good}
        results.append(result)
        print(f"Class {cls}: condition {label}; good c={sorted(actual_good)}; "
              f"domain matches={actual_good == expected_good}")
    return results


def check_atomic_tools():
    failures = cases = 0
    for a,b,l in itertools.product(range(N),range(N),RELATIONS):
        q = 1 << (a*N+b)
        row_not_a = sum(1 << (x*N+z) for x in range(N) for z in range(N) if x != a)
        col_not_b = sum(1 << (x*N+z) for x in range(N) for z in range(N) if z != b)
        for left,right in [
            (P(l,q), E(l,q)|col_not_b),
            (G(q,l), E(q,l)|row_not_a),
            (P(neg(q),l), E(q,neg(l))|row_not_a),
            (G(l,neg(q)), E(neg(l),q)|col_not_b),
        ]:
            cases += 1
            failures += left != right
    return {"assignments": cases, "failures": failures}


def documented_counterexamples():
    identity = (1 << 0) | (1 << 3)
    swap = (1 << 1) | (1 << 2)
    q = 1 << 1  # (B_j,C_j)=(0,1)
    col_not_b = (1 << 1) | (1 << 3)  # z != B_j=0
    col_not_c = (1 << 0) | (1 << 2)  # z != C_j=1
    left = P(swap,swap)
    printed_right = E(swap,q) | col_not_b
    repaired_right = E(swap,q) | col_not_c
    # Independent one-object Boolean calculation of the printed p55 negative row.
    compose_one = lambda a, b: a and b
    a1, b1, c1 = True, True, False
    negative_left = not compose_one(a1, b1 or c1)
    negative_right = (not compose_one(a1, b1)) or (not compose_one(a1, c1))
    repaired_negative = (not compose_one(a1, b1)) and (not compose_one(a1, c1))
    return {
        "p55_negative_simple_right_first_row": {
            "domain": [0], "a": [[0,0]], "b": [[0,0]], "c": [],
            "printed_left": negative_left, "printed_right": negative_right,
            "printed_equation_false": negative_left != negative_right,
            "corrected_intersection_right": repaired_negative,
            "corrected_equation_true": negative_left == repaired_negative,
        },
        "p54_printed_coordinate_step": {
            "l": pairs(swap), "b": pairs(swap), "Q": pairs(q),
            "both_totally_unlimited": dom_total(swap) and ran_total(swap),
            "left_P_l_b": pairs(left), "printed_right": pairs(printed_right),
            "printed_inclusion_false": bool(left & neg(printed_right)),
            "repaired_right": pairs(repaired_right),
            "repaired_inclusion_true": not bool(left & neg(repaired_right)),
        },
        "unlicensed_mixed_reassociation": {
            "a": pairs(TOP), "b": pairs(identity), "c": pairs(TOP),
            "G_a_E_b_c": pairs(G(TOP,E(identity,TOP))),
            "E_G_a_b_c": pairs(E(G(TOP,identity),TOP)),
        },
        "class1_without_premise": {
            "a": [[0,0]], "b": [], "c": [],
            "left": pairs(G(1,E(0,0))),
            "right": pairs(cap(E(G(A,0),0) for A in atoms(1))),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", type=Path, help="Write machine-readable results here")
    args = parser.parse_args()
    print("Peirce 1880 supplemental relation checks")
    print("U={0,1}; all 16 relations; row-major bits 00,01,10,11.")
    print("DD p: all 16 relations; atoms: all singleton subsets; simples: all coatom supersets.")
    oracle = check_operation_oracles()
    atomic = check_atomic_tools()
    print("Direct quantifier oracle:", oracle)
    print("p53 atomic tools:", atomic)
    result = {
        "python": platform.python_version(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "domain": [0,1], "relation_count": 16,
        "encoding": "bit x*2+y denotes (x,y)",
        "scope": "Finite exhaustive reconstruction, not an arbitrary-domain proof or literal check of all negation variants.",
        "operation_oracles": oracle, "atomic_tools": atomic,
        "distribution_simple": check_unconditional("D",DISTRIBUTION_SIMPLE),
        "distribution_developed": check_unconditional("DD",DISTRIBUTION_DEVELOPED),
        "association_simple": check_unconditional("S",ASSOCIATION_SIMPLE),
        "association_developed": check_conditional(),
        "counterexamples": documented_counterexamples(),
    }
    failures = oracle["failures"] + atomic["failures"]
    for name in ("distribution_simple","distribution_developed","association_simple"):
        failures += sum(row["failures"] for row in result[name])
    for cls in result["association_developed"]:
        failures += sum(row["conditional_failures"] for row in cls["formulas"])
        failures += not cls["finite_class_domain_matches"]
    result["unexpected_failures"] = failures
    print("Counterexamples:", json.dumps(result["counterexamples"],ensure_ascii=False,sort_keys=True))
    print("Unexpected failures:", failures)
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
