"""Finite premise-ablation tutorial, not a test of Aristotelian knowledge."""
from dataclasses import dataclass
from itertools import combinations
import json

WORLD_COUNT = 8
ALL = (1 << WORLD_COUNT) - 1

def validate(mask):
    if type(mask) is not int or not 0 <= mask <= ALL:
        raise ValueError("mask must be an integer in 0..255")
    return mask

def atom(bit):
    if type(bit) is not int or bit not in range(3):
        raise ValueError("atom index must be 0, 1, or 2")
    return sum(1 << w for w in range(WORLD_COUNT) if w & (1 << bit))

def implication(left, right):
    return (ALL ^ validate(left)) | validate(right)

def models(premises):
    result = ALL
    for premise in premises:
        result &= validate(premise)
    return result

def assess(premises, goal):
    goal = validate(goal)
    allowed = models(premises)
    counters = allowed & (ALL ^ goal)
    return {"models": allowed, "countermodels": counters,
            "entails": counters == 0, "consistent": allowed != 0}

def minimal_supports(premises, goal):
    """All inclusion-minimal index subsets with consistent entailment."""
    premises = tuple(premises)
    validate(goal)
    for p in premises:
        validate(p)
    found = []
    for size in range(len(premises) + 1):
        for indices in combinations(range(len(premises)), size):
            if any(set(old).issubset(indices) for old in found):
                continue
            verdict = assess([premises[i] for i in indices], goal)
            if verdict["entails"] and verdict["consistent"]:
                found.append(indices)
    return found

@dataclass(frozen=True)
class Declarations:
    # These are unverified human annotations, not properties inferred from masks.
    appropriate: bool
    causal_middle: bool
    same_domain: bool
    superior_route: bool = False
    bridge_attested: bool = False

def certificate(premises, goal, declarations):
    """A chosen pedagogical policy, not an equivalent definition of episteme."""
    if not isinstance(declarations, Declarations):
        raise ValueError("Declarations required")
    if any(type(value) is not bool for value in vars(declarations).values()):
        raise ValueError("declarations must be booleans")
    logical = assess(premises, goal)
    reasons = []
    if not logical["consistent"]:
        reasons.append("inconsistent-premises")
    if not logical["entails"]:
        reasons.append("countermodel-remains")
    if not declarations.appropriate:
        reasons.append("appropriateness-not-attested")
    if not declarations.causal_middle:
        reasons.append("causal-middle-not-attested")
    if not (declarations.same_domain or
            declarations.superior_route and declarations.bridge_attested):
        reasons.append("domain-route-not-attested")
    return {**logical, "policy_pass": not reasons, "reasons": reasons}

def experiment():
    # x: appropriate specific condition; y: intermediate fact; z: goal.
    x, y, z = map(atom, range(3))
    common = [implication(y, z)]
    specific = common + [x, implication(x, y)]
    alternative = [y, implication(y, z), x, implication(x, y)]
    cases = {
        "common_only": assess(common, z),
        "specific_route": assess(specific, z),
        "remove_specific_fact": assess([specific[0], specific[2]], z),
        "remove_specific_bridge": assess(specific[:2], z),
        "alternative_minimal_supports": minimal_supports(alternative, z),
        "logical_but_unattested": certificate([y, implication(y, z)], z,
            Declarations(False, False, True)),
        "same_masks_attested": certificate([y, implication(y, z)], z,
            Declarations(True, True, True)),
        "superior_without_bridge": certificate(specific, z,
            Declarations(True, True, False, True, False)),
        "superior_with_bridge": certificate(specific, z,
            Declarations(True, True, False, True, True)),
        "inconsistent": certificate([x, ALL ^ x], z,
            Declarations(True, True, True)),
    }
    disagreements = 0
    consistent_entailments = 0
    for premise in range(256):
        for goal in range(256):
            actual = assess([premise], goal)
            oracle = all(not (premise >> w & 1) or (goal >> w & 1)
                         for w in range(8))
            disagreements += actual["entails"] != oracle
            consistent_entailments += actual["entails"] and actual["consistent"]
    if disagreements:
        raise RuntimeError("finite truth oracle mismatch")
    return {"worlds": 8, "mask_pairs": 65536,
            "oracle_disagreements": disagreements,
            "consistent_entailment_pairs": consistent_entailments,
            "cases": cases,
            "limit": "Finite logical sufficiency and declared policy only; no cause or knowledge certification."}

if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2, ensure_ascii=False))
