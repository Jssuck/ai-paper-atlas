"""Finite teaching model, not a detector of essence or causal knowledge."""
from dataclasses import dataclass


def checked_mask(mask, width):
    if not isinstance(width, int) or isinstance(width, bool) or width < 0:
        raise ValueError('width must be a nonnegative integer')
    if not isinstance(mask, int) or isinstance(mask, bool) or not 0 <= mask < 1 << width:
        raise ValueError('mask outside the declared finite domain')
    return mask


def every_instance(subject, predicate, width):
    """All declared object/time positions in subject also satisfy predicate."""
    checked_mask(subject, width)
    checked_mask(predicate, width)
    return subject & ~predicate == 0


def counterexample(subject, predicate, objects, times):
    """Return earliest time-major (object, time) violating the inclusion, or None."""
    if not isinstance(objects, int) or isinstance(objects, bool) or objects < 1:
        raise ValueError('objects must be positive')
    if not isinstance(times, int) or isinstance(times, bool) or times < 1:
        raise ValueError('times must be positive')
    width = objects * times
    checked_mask(subject, width)
    checked_mask(predicate, width)
    missing = subject & ~predicate
    if not missing:
        return None
    bit = (missing & -missing).bit_length() - 1
    return bit % objects, bit // objects


def relative_partition(genus, left, right, width):
    """Two disjoint predicates cover genus; values outside genus are irrelevant."""
    for mask in (genus, left, right):
        checked_mask(mask, width)
    return (genus & (left | right) == genus
            and genus & left & right == 0)


def broadest_adequate(classes, predicate, width):
    """Return inclusion-maximal adequate NONEMPTY candidate class names.

    Only an extensional finite candidate diagnostic, not Aristotle's first
    explanatory subject. Coextensive names remain distinct; no identity inferred.
    """
    checked_mask(predicate, width)
    for name, mask in classes.items():
        if not isinstance(name, str) or not name:
            raise ValueError('class names must be nonempty strings')
        checked_mask(mask, width)
    good = {name: mask for name, mask in classes.items()
            if mask and every_instance(mask, predicate, width)}
    return tuple(sorted(name for name, mask in good.items()
                        if not any(mask != other and mask & ~other == 0
                                   for other in good.values())))


@dataclass(frozen=True)
class PerSeDeclarations:
    """External semantic declarations. They are not inferred from a sample."""
    # (subject, attribute) for an attribute included in subject's definition.
    attribute_in_subject_definition: frozenset = frozenset()
    # (subject, attribute) for a subject included in attribute's definition.
    subject_in_attribute_definition: frozenset = frozenset()
    # Names declared to subsist rather than be predicated of another bearer.
    independent_subjects: frozenset = frozenset()
    # (event, outcome) expressly declared causal, not merely contemporaneous.
    causal_links: frozenset = frozenset()

    def senses(self, subject, attribute):
        result = []
        if (subject, attribute) in self.attribute_in_subject_definition:
            result.append('definition-1')
        if (subject, attribute) in self.subject_in_attribute_definition:
            result.append('definition-2')
        if subject in self.independent_subjects:
            result.append('subsistence-3')
        if (subject, attribute) in self.causal_links:
            result.append('causal-4')
        return tuple(result)
