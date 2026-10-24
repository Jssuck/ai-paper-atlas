"""Original pedagogical model; not an implementation of Aristotle's psychology.

The inference engine only reads a ledger. Objective truth is checked separately.
All identifiers are opaque IDs, never display names. No logical omniscience.
"""
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class World:
    domain: frozenset[str]
    p: frozenset[str]
    q: frozenset[str]

    def __post_init__(self):
        if not self.p <= self.domain or not self.q <= self.domain:
            raise ValueError('extensions must lie within domain')

@dataclass(frozen=True)
class Ledger:
    meanings: frozenset[str] = frozenset()
    accepts_rule: bool = False
    registered: frozenset[str] = frozenset()
    recognizes_p: frozenset[str] = frozenset()
    derived_q: frozenset[str] = frozenset()

@dataclass(frozen=True)
class Certificate:
    object_id: str
    rule: str = 'all-P-are-Q'
    premise: str = 'P'
    conclusion: str = 'Q'


def universal_truth(world: World) -> bool:
    return world.p <= world.q


def restricted_truth(world: World, recognized: frozenset[str]) -> bool:
    """Objective truth of P -> Q only on a restricted, selected subdomain."""
    return (world.p & recognized) <= world.q


def applicable(ledger: Ledger, object_id: str) -> bool:
    return (ledger.meanings >= {'P', 'Q'} and ledger.accepts_rule
            and object_id in ledger.registered
            and object_id in ledger.recognizes_p)


def derive(ledger: Ledger, object_id: str):
    """One explicit application; lack of recorded support raises ValueError."""
    if not applicable(ledger, object_id):
        raise ValueError('missing meaning, rule, existence registration, or identification')
    cert = Certificate(object_id)
    return replace(ledger, derived_q=ledger.derived_q | {object_id}), cert


def syntactic_check(ledger: Ledger, cert: Certificate) -> bool:
    return (cert.rule == 'all-P-are-Q' and cert.premise == 'P'
            and cert.conclusion == 'Q' and applicable(ledger, cert.object_id))


def semantic_check(world: World, ledger: Ledger, cert: Certificate) -> bool:
    """A truth-based audit, not a complete definition of scientific knowledge."""
    return (syntactic_check(ledger, cert) and universal_truth(world)
            and cert.object_id in world.domain and cert.object_id in world.p
            and cert.object_id in world.q)
