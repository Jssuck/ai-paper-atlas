"""Finite teaching model for division versus demonstrated branch selection.

No claim to recover Aristotle's full semantics or certify empirical truth.
"""
from dataclasses import dataclass


def _members(value, label):
    if not isinstance(value, (set, frozenset)):
        raise TypeError(f'{label} must be set or frozenset')
    if any(type(x) is not int or x < 0 for x in value):
        raise ValueError(f'{label} members must be nonnegative integers (not bool)')
    return frozenset(value)


@dataclass(frozen=True)
class Step:
    parent: str
    left: str
    right: str
    side: str
    exclude_other: bool = False


class FiniteModel:
    def __init__(self, universe, terms):
        self.universe = _members(universe, 'universe')
        if not self.universe:
            raise ValueError('universe must be nonempty')
        if type(terms) is not dict or not terms:
            raise TypeError('terms must be a nonempty dict')
        checked = {}
        for name, value in terms.items():
            if type(name) is not str or not name or name.strip() != name:
                raise ValueError('term names must be nonempty stripped strings')
            members = _members(value, name)
            if not members <= self.universe:
                raise ValueError('term outside universe')
            checked[name] = members
        # Do not expose a mutable mapping: all subsequent checks use this snapshot.
        from types import MappingProxyType
        self.terms = MappingProxyType(checked)

    def term(self, name):
        if type(name) is not str:
            raise TypeError('term name must be string')
        if name not in self.terms:
            raise ValueError(f'unknown term {name!r}')
        return self.terms[name]

    def division_report(self, parent, left, right, target):
        a, b, c, d = (self.term(x) for x in (parent, left, right, target))
        coverage = a <= b | c
        target_in_parent = d <= a
        return {
            'coverage': coverage,
            'target_in_parent': target_in_parent,
            'premises': coverage and target_in_parent,
            'target_nonempty': bool(d),
            'disjoint_children': not b & c,
            'children_within_parent': b | c <= a,
            'pointwise_disjunction': d <= b | c,
            'all_left': d <= b,
            'all_right': d <= c,
            'uniform_disjunction': d <= b or d <= c,
        }

    def select_branch(self, parent, left, right, target, side, *, exclude_other=False):
        if side not in ('left', 'right') or type(side) is not str:
            raise ValueError('side must be left or right')
        if type(exclude_other) is not bool:
            raise TypeError('exclude_other must be bool')
        report = self.division_report(parent, left, right, target)
        if not report['premises']:
            raise ValueError('coverage and target membership premises are required')
        if not exclude_other:
            raise ValueError('explicit exclusion certificate is required')
        chosen, other = (left, right) if side == 'left' else (right, left)
        if self.term(target) & self.term(other):
            raise ValueError('claimed exclusion is false in the supplied model')
        if not self.term(target) <= self.term(chosen):
            raise RuntimeError('internal inference failure')
        return chosen

    def follow_path(self, target, steps):
        self.term(target)
        if type(steps) not in (list, tuple) or not steps:
            raise ValueError('steps must be a nonempty list or tuple')
        previous = None
        path = []
        for step in steps:
            if type(step) is not Step:
                raise TypeError('each step must be a Step')
            if previous is not None and step.parent != previous:
                raise ValueError('path must continue at the previously selected child')
            previous = self.select_branch(step.parent, step.left, step.right,
                                          target, step.side,
                                          exclude_other=step.exclude_other)
            path.append(previous)
        return tuple(path)

    def definition_report(self, target, description):
        d, e = self.term(target), self.term(description)
        return {'necessary': d <= e, 'sufficient': e <= d, 'coextensive': d == e}
