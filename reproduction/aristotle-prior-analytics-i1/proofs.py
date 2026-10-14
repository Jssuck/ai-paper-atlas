"""A small sound, intentionally incomplete modern proof-certificate checker."""

from dataclasses import dataclass

from logic import Language, Prop, ValidationError, _revalidate, validate_problem


RULE_ARITY = {
    "assume": 0,
    "a_trans": 2,
    "e_sym": 1,
    "e_down": 2,
    "i_up": 2,
    "o_from_i_e": 2,
}


@dataclass(frozen=True, slots=True)
class Step:
    claim: Prop
    rule: str
    refs: tuple[int, ...] = ()
    assumption: int | None = None

    def __post_init__(self) -> None:
        if type(self.claim) is not Prop:
            raise ValidationError("step claim must be a Prop")
        if type(self.rule) is not str or self.rule not in RULE_ARITY:
            raise ValidationError("unknown certificate rule")
        if type(self.refs) is not tuple:
            raise ValidationError("step refs must be a tuple")
        if any(type(ref) is not int or ref < 0 for ref in self.refs):
            raise ValidationError("step refs must be nonnegative integers, not bools")
        if len(self.refs) != RULE_ARITY[self.rule]:
            raise ValidationError("wrong number of references for this rule")
        if self.rule == "assume":
            if type(self.assumption) is not int or self.assumption < 0:
                raise ValidationError("assume requires a nonnegative premise index")
        elif self.assumption is not None:
            raise ValidationError("derived steps cannot import assumptions")


@dataclass(frozen=True, slots=True)
class ProofReport:
    accepted: bool
    conclusion: Prop
    used_assumptions: tuple[int, ...]
    unused_assumptions: tuple[int, ...]
    repeats_assumption: bool
    step_count: int


def _derived_claim(rule: str, inputs: tuple[Prop, ...]) -> Prop:
    if rule == "e_sym":
        (p,) = inputs
        if p.kind == "E":
            return Prop("E", p.predicate, p.subject)
    else:
        p, q = inputs
        if p.predicate == q.subject:
            if rule == "a_trans" and (p.kind, q.kind) == ("A", "A"):
                return Prop("A", p.subject, q.predicate)
            if rule == "e_down" and (p.kind, q.kind) == ("A", "E"):
                return Prop("E", p.subject, q.predicate)
            if rule == "i_up" and (p.kind, q.kind) == ("I", "A"):
                return Prop("I", p.subject, q.predicate)
            if rule == "o_from_i_e" and (p.kind, q.kind) == ("I", "E"):
                return Prop("O", p.subject, q.predicate)
    raise ValidationError("referenced claims do not match the rule's pattern")


def check_certificate(
    language: Language,
    premises: tuple[Prop, ...],
    conclusion: Prop,
    steps: tuple[Step, ...],
) -> ProofReport:
    """Reject malformed proofs; return dependency data for accepted proofs.

    Premise indices and step indices are both zero-based and distinct. Derived
    steps may reference only earlier steps. Every step is checked, including
    unused ones. Dependencies mean syntactic use, not logical indispensability.
    There is no rule using required_nonempty and no completeness claim.
    """
    validate_problem(language, premises, conclusion)
    if type(steps) is not tuple or not steps:
        raise ValidationError("certificate must be a nonempty tuple of Steps")
    dependencies: list[frozenset[int]] = []
    for index, step in enumerate(steps):
        _revalidate(step, Step, "certificate entry")
        validate_problem(language, (), step.claim)
        if step.rule == "assume":
            # The boundary check above verifies exact type and nonnegativity.
            premise_index = step.assumption
            if premise_index is None or premise_index >= len(premises):
                raise ValidationError(f"step {index}: undeclared premise index")
            if step.claim != premises[premise_index]:
                raise ValidationError(f"step {index}: claim differs from declared premise")
            dependencies.append(frozenset((premise_index,)))
        else:
            if any(ref >= index for ref in step.refs):
                raise ValidationError(f"step {index}: references must point strictly backward")
            inputs = tuple(steps[ref].claim for ref in step.refs)
            expected = _derived_claim(step.rule, inputs)
            if expected != step.claim:
                raise ValidationError(f"step {index}: claimed conclusion does not follow by rule")
            dependencies.append(frozenset().union(*(dependencies[ref] for ref in step.refs)))
    if steps[-1].claim != conclusion:
        raise ValidationError("last step does not match requested conclusion")
    used = dependencies[-1]
    return ProofReport(
        True, conclusion, tuple(sorted(used)),
        tuple(i for i in range(len(premises)) if i not in used),
        conclusion in premises, len(steps),
    )
