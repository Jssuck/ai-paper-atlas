"""Original finite teaching model, not a validator of Aristotelian knowledge."""
from dataclasses import dataclass
from typing import Optional

WORLD_COUNT = 8
UNIVERSE = (1 << WORLD_COUNT) - 1

def check_mask(mask):
    if type(mask) is not int or not 0 <= mask <= UNIVERSE:
        raise ValueError('truth mask must be an integer from 0 to 255')

def entails(premises, conclusion):
    """Truth preservation over eight valuations of three Boolean atoms."""
    check_mask(conclusion)
    joint = UNIVERSE
    for mask in premises:
        check_mask(mask)
        joint &= mask
    return (joint & (UNIVERSE ^ conclusion)) == 0

def counterworlds(premises, conclusion):
    check_mask(conclusion)
    joint = UNIVERSE
    for mask in premises:
        check_mask(mask)
        joint &= mask
    return tuple(w for w in range(WORLD_COUNT) if joint & (1 << w) and not conclusion & (1 << w))

@dataclass(frozen=True)
class Premise:
    name: str
    truth_mask: int
    primary_declared: bool
    immediate_declared: bool
    priority_rank: int
    confidence_rank: int

@dataclass(frozen=True)
class Candidate:
    premises: tuple[Premise, ...]
    conclusion_name: str
    conclusion_mask: int
    actual_world: int
    conclusion_priority: int
    conclusion_confidence: int
    cause_links_declared: frozenset[tuple[str, str]]

def inspect_candidate(c):
    """Check declared-data consistency, never establish genuine causes or knowledge.

    Requiring EVERY premise to outrank the conclusion is a deliberately strong
    teaching policy, not a necessary-and-sufficient reading of Part 2's some/all.
    """
    check_mask(c.conclusion_mask)
    if type(c.actual_world) is not int or not 0 <= c.actual_world < WORLD_COUNT:
        raise ValueError('invalid actual world')
    if not c.premises or len({p.name for p in c.premises}) != len(c.premises):
        raise ValueError('nonempty uniquely named premises required')
    for p in c.premises:
        check_mask(p.truth_mask)
        if type(p.primary_declared) is not bool or type(p.immediate_declared) is not bool:
            raise ValueError('declarations must be Boolean')
    if c.conclusion_name in {p.name for p in c.premises}:
        raise ValueError('distinct conclusion identifier required')
    checks = {
        'valid_on_finite_domain': entails([p.truth_mask for p in c.premises], c.conclusion_mask),
        'premises_true_at_actual_world': all(p.truth_mask & (1 << c.actual_world) != 0 for p in c.premises),
        'primary_declared': all(p.primary_declared for p in c.premises),
        'immediate_declared': all(p.immediate_declared for p in c.premises),
        'strict_confidence_policy': all(p.confidence_rank > c.conclusion_confidence for p in c.premises),
        'priority_policy': all(p.priority_rank < c.conclusion_priority for p in c.premises),
        'cause_links_declared': all((p.name, c.conclusion_name) in c.cause_links_declared for p in c.premises),
    }
    return {'checks': checks, 'declared_policy_pass': all(checks.values()),
            'scientific_knowledge_certified': False}

def classify_starting_point(*, indispensable_for_any_learning: bool, existence_assertion: Optional[bool]):
    """Classification of supplied teaching descriptors, not textual discovery.

    None means no existence assertion; False means asserts nonexistence, NOT
    missing information. Input already presupposes an immediate starting point.
    """
    if type(indispensable_for_any_learning) is not bool:
        raise ValueError('indispensability must be Boolean')
    if existence_assertion is not None and type(existence_assertion) is not bool:
        raise ValueError('existence assertion must be True, False or None')
    if indispensable_for_any_learning:
        return 'axiom'
    return 'definition' if existence_assertion is None else 'hypothesis'
