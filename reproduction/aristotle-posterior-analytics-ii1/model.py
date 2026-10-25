"""Modern teaching reconstruction of APo II.1, not a knowledge verifier."""
from dataclasses import dataclass
from enum import Enum
from itertools import product
import json


class Status(str, Enum):
    UNKNOWN = 'unknown'
    YES = 'yes'
    NO = 'no'


@dataclass(frozen=True)
class InquiryKey:
    kind: str
    subject: str
    context: str
    attribute: str = ''

    def __post_init__(self):
        if self.kind not in ('attribute', 'existence'):
            raise ValueError('kind must be attribute or existence')
        if not self.subject.strip() or not self.context.strip():
            raise ValueError('subject and context required')
        if (self.kind == 'attribute') != bool(self.attribute.strip()):
            raise ValueError('only attribute inquiries require an attribute')


@dataclass(frozen=True)
class EvidenceState:
    status: Status = Status.UNKNOWN
    evidence: str = ''


class Ledger:
    """Caller-supplied verdict ledger; no empirical truth or cause certification."""
    def __init__(self):
        self._states = {}
        self._candidates = {}

    def state(self, key):
        return self._states.get(key, EvidenceState())

    def record(self, key, verdict, evidence):
        if not isinstance(key, InquiryKey):
            raise TypeError('InquiryKey required')
        if not isinstance(verdict, Status) or verdict is Status.UNKNOWN:
            raise ValueError('record requires explicit YES or NO; use withdraw')
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError('a nonempty evidence label is required, not verified')
        self._states[key] = EvidenceState(verdict, evidence)

    def withdraw(self, key):
        self._states.pop(key, None)

    def next_question(self, key):
        status = self.state(key).status
        if status is Status.NO:
            return 'closed_negative'
        if key.kind == 'attribute':
            return 'why' if status is Status.YES else 'fact'
        return 'what' if status is Status.YES else 'exists'

    def propose(self, key, candidate):
        if not isinstance(candidate, str) or not candidate.strip():
            raise ValueError('nonempty candidate label required')
        self._candidates.setdefault(key, []).append(candidate)

    def candidates(self, key):
        return tuple(self._candidates.get(key, ()))

    def certified_answer(self, key):
        # Deliberately impossible: this model checks bookkeeping, not causes/essences.
        return None


def exhaustive_check(max_length=4):
    """Check every finite action sequence for both inquiry types."""
    sequences = checks = 0
    for kind in ('attribute', 'existence'):
        key = InquiryKey(kind, 'subject', 'context-1', 'property' if kind == 'attribute' else '')
        other = InquiryKey(kind, 'subject', 'context-2', key.attribute)
        for length in range(max_length + 1):
            for actions in product(('yes', 'no', 'withdraw'), repeat=length):
                ledger = Ledger()
                sequences += 1
                for action in actions:
                    if action == 'withdraw':
                        ledger.withdraw(key)
                    else:
                        ledger.record(key, Status(action), 'synthetic evidence')
                    expected = ('why' if kind == 'attribute' else 'what') if action == 'yes' else ('closed_negative' if action == 'no' else ('fact' if kind == 'attribute' else 'exists'))
                    if ledger.next_question(key) != expected:
                        raise RuntimeError('route invariant violated')
                    if ledger.state(other).status is not Status.UNKNOWN:
                        raise RuntimeError('context isolation violated')
                    if ledger.certified_answer(key) is not None:
                        raise RuntimeError('fabricated explanation')
                    checks += 1
    return {'max_length': max_length, 'sequences': sequences, 'transitions': checks, 'violations': 0}


def demo():
    ledger = Ledger()
    eclipse = InquiryKey('attribute', 'sun', 'illustrative-event', 'eclipsed')
    centaur = InquiryKey('existence', 'centaur', 'actual-world')
    before = ledger.next_question(eclipse)
    ledger.record(eclipse, Status.YES, 'assumed teaching observation; not real astronomy')
    ledger.propose(eclipse, 'candidate explanation A')
    ledger.propose(eclipse, 'candidate explanation B')
    ledger.propose(centaur, 'understood nominal description')
    return {'eclipse_before': before, 'eclipse_after': ledger.next_question(eclipse),
            'candidate_count': len(ledger.candidates(eclipse)),
            'certified_cause': ledger.certified_answer(eclipse),
            'centaur_after_description': ledger.next_question(centaur),
            'new_context': ledger.next_question(InquiryKey('attribute', 'sun', 'different-event', 'eclipsed')),
            'exhaustive': exhaustive_check()}


if __name__ == '__main__':
    print(json.dumps(demo(), ensure_ascii=False, indent=2))
