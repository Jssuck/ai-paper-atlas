"""Original finite categorical-syllogism teaching model; Python standard library."""
import itertools
import json

MOODS = tuple(''.join(x) for x in itertools.product('AEIO', repeat=3))


def proposition(kind, subject, predicate):
    if kind == 'A':
        return subject <= predicate
    if kind == 'E':
        return subject.isdisjoint(predicate)
    if kind == 'I':
        return bool(subject & predicate)
    if kind == 'O':
        return bool(subject - predicate)
    raise ValueError('kind must be A, E, I, or O')


def terms(world):
    if type(world) is not int or not 0 <= world < 256:
        raise ValueError('world must be an integer in 0..255')
    # Each occupied cell has one representative; cell bits encode S, P, M.
    occupied = {i for i in range(8) if world & (1 << i)}
    return tuple(frozenset(i for i in occupied if i & bit) for bit in (1, 2, 4))


def premises(figure, mood, s, p, m):
    if figure not in (1, 2, 3):
        raise ValueError('figure must be 1, 2, or 3')
    if mood not in MOODS:
        raise ValueError('mood must be a three-letter AEIO string')
    major, minor = {1: ((m, p), (s, m)), 2: ((p, m), (s, m)),
                    3: ((m, p), (m, s))}[figure]
    return proposition(mood[0], *major) and proposition(mood[1], *minor)


def evaluate(figure, mood, nonempty_terms=False):
    witnesses = 0
    failures = []
    for world in range(256):
        s, p, m = terms(world)
        if nonempty_terms and not all((s, p, m)):
            continue
        if premises(figure, mood, s, p, m):
            witnesses += 1
            if not proposition(mood[2], s, p):
                failures.append(world)
    return {'premise_worlds': witnesses, 'counterexample_worlds': len(failures),
            'first_counterexample': failures[0] if failures else None,
            'valid_in_enumeration': not failures}


def reductions(s, p, m):
    """Material implications validating three explicitly stated reductions."""
    cesare = not premises(2, 'EAE', s, p, m) or (
        proposition('E', m, p) and premises(1, 'EAE', s, p, m)
        and proposition('E', s, p))
    # Camestres: E(S,M)->E(M,S); Celarent on subject P, predicate S;
    # then E(P,S)->E(S,P). Do not silently keep the old term ordering.
    camestres = not premises(2, 'AEE', s, p, m) or (
        proposition('E', m, s) and premises(1, 'EAE', p, s, m)
        and proposition('E', p, s) and proposition('E', s, p))
    datisi = not premises(3, 'AII', s, p, m) or (
        proposition('I', s, m) and premises(1, 'AII', s, p, m)
        and proposition('I', s, p))
    return {'Cesare_via_Celarent': cesare, 'Camestres_via_Celarent': camestres,
            'Datisi_via_Darii': datisi}


def run():
    policies = {}
    for nonempty in (False, True):
        rows = {str(f): {m: evaluate(f, m, nonempty) for m in MOODS} for f in (1, 2, 3)}
        valid = {f: [m for m, result in table.items() if result['valid_in_enumeration']]
                 for f, table in rows.items()}
        policies['all_terms_nonempty' if nonempty else 'empty_terms_allowed'] = {
            'worlds': sum(not nonempty or all(terms(w)) for w in range(256)),
            'valid_moods': valid,
            'figure_2_affirmative_valid': [m for m in valid['2'] if m[2] in 'AI'],
            'figure_3_universal_valid': [m for m in valid['3'] if m[2] in 'AE'],
            'rows': rows}
    reduction_failures = {name: 0 for name in reductions(*terms(0))}
    for world in range(256):
        for name, ok in reductions(*terms(world)).items():
            reduction_failures[name] += int(not ok)
    return {'scope': 'original finite teaching model, not a reconstruction of all scientific demonstration',
            'cell_bits': {'S': 1, 'P': 2, 'M': 4}, 'moods_per_figure': len(MOODS),
            'policies': policies, 'reduction_failures': reduction_failures}

if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
