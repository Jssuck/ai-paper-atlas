"""I.30 teaching model: labelled inclusion paths, not a truth-discovery engine."""
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class Premise:
    id: str
    subject: str
    predicate: str
    basis: str
    source: str


def _name(value):
    if type(value) is not str or not value or value != value.strip():
        raise ValueError('names must be nonempty, trimmed strings')


def _validate(nodes, premises, mode):
    if type(nodes) not in (list, tuple) or not nodes:
        raise ValueError('nodes must be a nonempty list or tuple')
    for node in nodes:
        _name(node)
    if len(set(nodes)) != len(nodes):
        raise ValueError('duplicate node')
    if type(mode) is not str or mode not in ('truth', 'dialectic'):
        raise ValueError('unknown mode')
    if type(premises) not in (list, tuple):
        raise ValueError('premises must be a list or tuple')
    ids = set()
    for p in premises:
        if type(p) is not Premise:
            raise ValueError('expected Premise')
        for field in (p.id, p.subject, p.predicate, p.source):
            _name(field)
        if p.id in ids:
            raise ValueError('duplicate premise id')
        ids.add(p.id)
        if p.subject not in nodes or p.predicate not in nodes:
            raise ValueError('undeclared term')
        if type(p.basis) is not str or p.basis not in ('verified', 'endoxon'):
            raise ValueError('unknown basis')
    return 'verified' if mode == 'truth' else 'endoxon'


def _query(nodes, start, goal):
    _name(start)
    _name(goal)
    if start not in nodes or goal not in nodes:
        raise ValueError('undeclared query term')


def find_path(nodes, premises, start, goal, mode='truth'):
    """Return a shortest admissible edge-ID tuple, or None (unknown here).

    A zero-edge path proves only reflexive inclusion. Input order breaks ties.
    A 'verified' label is a supplied claim, not verification by this function.
    """
    basis = _validate(nodes, premises, mode)
    _query(nodes, start, goal)
    queue = deque([(start, ())])
    seen = {start}
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        for p in premises:
            if p.basis == basis and p.subject == current and p.predicate not in seen:
                seen.add(p.predicate)
                queue.append((p.predicate, path + (p.id,)))
    return None


def verify_path(nodes, premises, start, goal, certificate, mode='truth'):
    """Check a finite supplied path; return False for well-typed invalid proof."""
    basis = _validate(nodes, premises, mode)
    _query(nodes, start, goal)
    if type(certificate) not in (list, tuple):
        raise ValueError('certificate must be a list or tuple')
    for item in certificate:
        _name(item)
    by_id = {p.id: p for p in premises}
    current = start
    for ident in certificate:
        p = by_id.get(ident)
        if p is None or p.basis != basis or p.subject != current:
            return False
        current = p.predicate
    return current == goal


def interpretation_holds(nodes, premises, extensions, domain, mode='truth'):
    """Evaluate selected inputs in one explicitly supplied finite interpretation."""
    basis = _validate(nodes, premises, mode)
    if type(domain) not in (set, frozenset) or not domain:
        raise ValueError('finite domain must be a nonempty set')
    if type(extensions) is not dict or set(extensions) != set(nodes):
        raise ValueError('provide exactly one extension for every term')
    for extension in extensions.values():
        if type(extension) not in (set, frozenset) or not extension <= domain:
            raise ValueError('extension outside domain or not a set')
    return all(extensions[p.subject] <= extensions[p.predicate]
               for p in premises if p.basis == basis)


def sample_support(subject, predicate, observed, domain):
    """Classify evidence for subject-in-predicate, not infer a universal law."""
    if type(domain) not in (set, frozenset) or not domain:
        raise ValueError('nonempty set domain required')
    for s in (subject, predicate, observed):
        if type(s) not in (set, frozenset) or not s <= domain:
            raise ValueError('sets must be contained in domain')
    sampled = subject & observed
    if not sampled:
        return 'no_subject_observations'
    return 'sample_support' if sampled <= predicate else 'sample_counterexample'
