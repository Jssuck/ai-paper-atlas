"""A bounded, extensional teaching reconstruction of Prior Analytics I.38.

Qualifiers are opaque parts of predicate identity. This is not a theory of
knowledge, a natural-language parser, or a reconstruction of all ancient logic.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Term:
    name: str
    qualifier: str = ''

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError('term name must be a nonempty string')
        if not isinstance(self.qualifier, str):
            raise TypeError('qualifier must be a string')
        if self.qualifier and not self.qualifier.strip():
            raise ValueError('qualifier may be empty, but not whitespace-only')


@dataclass(frozen=True)
class Inclusion:
    subject: Term
    predicate: Term

    def __post_init__(self):
        if not isinstance(self.subject, Term) or not isinstance(self.predicate, Term):
            raise TypeError('inclusion endpoints must be Terms')


def chain_certificate(first, second, conclusion):
    """Check exactly C->B, B->A, C->A, preserving complete term labels.

    This checks certificate shape, not premise truth. False does not mean
    that the conclusion is false or that no other proof exists.
    """
    if any(not isinstance(e, Inclusion) for e in (first, second, conclusion)):
        raise TypeError('certificate entries must be Inclusions')
    return (first.predicate == second.subject and
            conclusion.subject == first.subject and
            conclusion.predicate == second.predicate)


class Model:
    def __init__(self, domain, extensions):
        self.domain = frozenset(domain)
        self.extensions = {}
        for term, members in extensions.items():
            if not isinstance(term, Term):
                raise TypeError('extension keys must be Terms')
            members = frozenset(members)
            if not members <= self.domain:
                raise ValueError('extension outside domain')
            self.extensions[term] = members

    def holds(self, inclusion):
        if not isinstance(inclusion, Inclusion):
            raise TypeError('expected an Inclusion')
        # An unknown extension is missing data, not an empty extension.
        return self.extensions[inclusion.subject] <= self.extensions[inclusion.predicate]
