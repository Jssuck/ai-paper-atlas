"""Compare production set operations with independent integer/Boolean oracles."""
import json
from itertools import product
from model import World, Ledger, derive, applicable, universal_truth, restricted_truth, semantic_check


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(n=3):
    ids = tuple(f'object-{i}' for i in range(n))
    domain = frozenset(ids)
    def members(mask): return frozenset(ids[i] for i in range(n) if mask >> i & 1)
    worlds = states = queries = applications = certified = false_outputs = restriction_gaps = 0
    for pm, qm in product(range(1 << n), repeat=2):
        worlds += 1
        world = World(domain, members(pm), members(qm))
        universal = all(not (pm >> i & 1) or (qm >> i & 1) for i in range(n))
        require(universal_truth(world) == universal, 'universal oracle mismatch')
        for recognized in range(1 << n):
            restricted = all(not ((pm >> i & 1) and (recognized >> i & 1)) or (qm >> i & 1) for i in range(n))
            require(restricted_truth(world, members(recognized)) == restricted, 'restricted oracle mismatch')
            restriction_gaps += int(restricted and not universal)
            for registered, accepted, meaning_mask in product(range(1 << n), (False, True), range(4)):
                states += 1
                meanings = frozenset(p for j,p in enumerate(('P','Q')) if meaning_mask >> j & 1)
                ledger = Ledger(meanings,accepted,members(registered),members(recognized))
                for i, oid in enumerate(ids):
                    queries += 1
                    expected = bool(accepted and meaning_mask == 3 and registered >> i & 1 and recognized >> i & 1)
                    require(applicable(ledger,oid) == expected,'applicability oracle mismatch')
                    if not expected:
                        try: derive(ledger,oid)
                        except ValueError: pass
                        else: raise RuntimeError('unsupported derivation accepted')
                        continue
                    applications += 1
                    after, cert = derive(ledger,oid)
                    require(after.derived_q == {oid},'wrong derived target')
                    truth_supported = bool(universal and pm >> i & 1)
                    require(semantic_check(world,ledger,cert) == truth_supported,'semantic oracle mismatch')
                    certified += int(truth_supported)
                    false_outputs += int(not (qm >> i & 1))
                    if truth_supported:
                        require(bool(qm >> i & 1),'sound premises produced false output')
    return {'domain_size':n,'worlds':worlds,'ledger_states':states,'target_queries':queries,
            'syntactic_applications':applications,'truth_supported_applications':certified,
            'false_outputs_from_unsupported_premises':false_outputs,
            'restricted_true_universal_false_pairs':restriction_gaps,
            'oracle_mismatches':0,
            'scope':'finite diagnostics of this declared teaching model, not a general proof or human experiment'}

if __name__ == '__main__': print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
