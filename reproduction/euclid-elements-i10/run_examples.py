"""Run finite examples; raise explicitly so -O/-OO cannot remove checks."""
import hashlib
import json
from collections import Counter
from geometry import construct, check_certificate, encode
from cases import positive_cases, rejected_cases, example_report


def run():
    counts = Counter()
    digest = hashlib.sha256()
    total = 0
    for label, family, a, b, branch in positive_cases():
        cert = construct(a, b, branch)
        facts = check_certificate(a, b, cert)
        if not all(facts.values()):
            raise RuntimeError(f'positive case failed: {label}: {facts}')
        record = {'label': label, 'A': encode(a), 'B': encode(b), 'certificate': encode(cert), 'checks': facts}
        digest.update((json.dumps(record, sort_keys=True, separators=(',', ':')) + '\n').encode())
        total += 1
        counts[family] += 1
    negatives = []
    for label, a, b, cert in rejected_cases():
        facts = check_certificate(a, b, cert)
        if all(facts.values()):
            raise RuntimeError(f'negative case wrongly accepted: {label}')
        negatives.append({'name': label, 'checks': facts, 'accepted': False})
    return {'status': 'passed', 'positive_certificates': total,
            'positive_families': dict(sorted(counts.items())),
            'positive_records_sha256': digest.hexdigest(),
            'negative_certificates': len(negatives), 'negative_cases': negatives,
            'examples': example_report(),
            'scope': 'finite exact coordinate tests, not a proof for all inputs'}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
