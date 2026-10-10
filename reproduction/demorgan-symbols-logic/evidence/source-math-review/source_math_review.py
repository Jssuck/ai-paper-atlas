#!/usr/bin/env python3
"""Independent, standard-library-only source/semantics audit.

Source: De Morgan, On the Symbols of Logic..., printed pp. 91, 94-95,
101-103. The p.95 table below was independently transcribed from the scan,
including its apparent printed error. Does not import the main implementation.
Finite verification is not a proof of unbounded completeness.
"""
from itertools import product
from pathlib import Path
import datetime
import hashlib
import json
import platform
import sys

FORMS = {
    '))': ('A', 'universal'), '((': ('a', 'universal'),
    ').(': ('E', 'universal'), '(.)': ('e', 'universal'),
    '()': ('I', 'particular'), ')(': ('i', 'particular'),
    '(.(': ('O', 'particular'), ').)': ('o', 'particular'),
}

def contrary_value(form, x, y, universe):
    return {
        '))': x <= y, '((': y <= x,
        ').(': not (x & y), '(.)': x | y == universe,
        '()': bool(x & y), ')(': bool(universe - (x | y)),
        '(.(': bool(x - y), ').)': bool(y - x),
    }[form]

def exemplar_value(form, x, y, universe):
    if form == ')(':
        return len(x) == len(y) == 1 and x == y
    if form == '(.)':
        return any(a != b for a in x for b in y)
    return contrary_value(form, x, y, universe)

def erase_middle(first, second):
    negative = ('.' in first) != ('.' in second)
    return first[0] + ('.' if negative else '') + second[-1]

def contrary_rule(first, second):
    first_u = FORMS[first][1] == 'universal'
    second_u = FORMS[second][1] == 'universal'
    return ((first[-1] == second[0] and (first_u or second_u))
            or (first[-1] != second[0] and first_u and second_u))

def exemplar_rule(first, second):
    has_affirmative = not ('.' in first and '.' in second)
    has_indefinite_middle = first[-1] == '(' or second[0] == ')'
    return has_affirmative and has_indefinite_middle

def choose_rules(predicate):
    return [(a, b, erase_middle(a, b))
            for a, b in product(FORMS, repeat=2) if predicate(a, b)]

def subsets(n, allow_empty, allow_full):
    universe = frozenset(range(1, n + 1))
    values = [frozenset(i + 1 for i in range(n) if mask >> i & 1)
              for mask in range(2 ** n)]
    return [s for s in values if (allow_empty or s)
            and (allow_full or s != universe)]

def finite_check(rules, valuation, allow_empty, allow_full, n=4):
    universe = frozenset(range(1, n + 1))
    classes = subsets(n, allow_empty, allow_full)
    failures = {}
    for x, y, z in product(classes, repeat=3):
        for first, second, conclusion in rules:
            if (valuation(first, x, y, universe)
                    and valuation(second, y, z, universe)
                    and not valuation(conclusion, x, z, universe)):
                key = first + ' ; ' + second + ' => ' + conclusion
                failures.setdefault(key, {'X': sorted(x), 'Y': sorted(y), 'Z': sorted(z)})
    return {'universe': sorted(universe), 'classes_per_term': len(classes),
            'model_count': len(classes) ** 3, 'rule_count': len(rules),
            'counterexample_rule_count': len(failures), 'first_countermodels': failures}

# Six columns, each with eight rows: (first premise, second premise, printed conclusion).
# Locations refer to the printed p.95 table, not to OCR line numbers.
TABLE_95 = {
 'upper-left': [('()', '))','()'),(')(','((' ,')('),(').)', '))',').)'),('(.(','((','(.('),('(.(','(.)','()'),(').)',').(',')('),('()',').(','(.('),(')(','(.)',').)')],
 'upper-middle':[('))','))','))'),('((','((','(('),('(.)','))','(.)'),(').(','((' ,').('),(').(','(.)','))'),('(.)',').(','(('),('))',').(',').('),('((','(.)','(.)')],
 'upper-right':[('((','))','()'),('))','((' ,')('),(').(','))',').)'),('(.)','((','(.('),('(.)','(.)','()'),(').(',').(',')('),('((' ,').(','(.('),('))','(.)',').)')],
 'lower-left':[('((','()','()'),('))',')(',')('),(').(','()',').)'),('(.)',')(','(.('),('(.)',').)','()'),(').(','(.(',')('),('((','(.(','(.('),('))',').)',').)')],
 'lower-middle':[('((','((','(('),('))','))','))'),(').(','((' ,').('),('(.)','))','(.)'),('(.)',').(','(('),(').(','(.)','))'),('((','(.)','(.)'),('))',').(',').(')],
 'lower-right':[('((','))','()'),('))','((' ,')('),(').(','))',').)'),('(.)','((','(.('),('(.)','(.)','()'),(').(',').(',')('),('((' ,').(','(.('),('))','(.)','(.(')],
}

def table_check():
    trace = []
    for column, rows in TABLE_95.items():
        for row, (a, b, printed) in enumerate(rows, 1):
            expected = erase_middle(a, b)
            trace.append({'column': column, 'row': row,
                          'first': a, 'second': b, 'printed_conclusion': printed,
                          'erasure_conclusion': expected, 'matches': printed == expected})
    return {'checked_cells': len(trace), 'mismatches': [r for r in trace if not r['matches']],
            'complete_cell_trace': trace}

def named_countermodels():
    u, x, y, z = {1,2,3}, {1}, {1,2}, {1,3}
    assert x <= y and y | z == u and not (x - z) and z - x
    x = y = {1,2}
    assert y <= x and not any(all(a == b for b in y) for a in x)
    assert all(any(a != b for b in y) for a in x)
    assert not any(all(a != b for a in x) for b in y)
    # Every vertex has an incoming and outgoing edge, but contrary conversion fails.
    u, x, y, relation = {1,2}, {1}, {2}, {(1,1), (1,2), (2,2)}
    assert all((a,c) in relation for a,b in relation for bb,c in relation if b == bb)
    assert all(any((a,b) in relation for b in u) for a in u)
    assert all(any((a,b) in relation for a in u) for b in u)
    assert all(any((a,b) in relation for b in y) for a in x)
    assert not all(any((a,b) in relation for a in u-x) for b in u-y)
    return {'table_95_typo': 'passed', 'selective_quantifier_scope': 'passed',
            'serial_and_converse_serial_insufficient_for_contrary_conversion': 'passed'}

def main():
    contraries = choose_rules(contrary_rule)
    exemplars = choose_rules(exemplar_rule)
    categories = {}
    for a,b,c in contraries:
        key = '/'.join(FORMS[s][1] for s in (a,b,c))
        categories[key] = categories.get(key, 0) + 1
    proper = finite_check(contraries, contrary_value, False, False)
    unrestricted = finite_check(contraries, contrary_value, True, True)
    exemplar_models = finite_check(exemplars, exemplar_value, False, True)
    intersection = sorted(set(contraries) & set(exemplars))
    table = table_check()
    assert len(contraries) == 32 and len(exemplars) == 36 and len(intersection) == 21
    assert sorted(categories.values()) == [8,8,8,8]
    assert proper['counterexample_rule_count'] == 0
    assert unrestricted['counterexample_rule_count'] == 8
    for triple in unrestricted['first_countermodels']:
        premises, conclusion = triple.split(' => ')
        first, second = premises.split(' ; ')
        assert [FORMS[s][1] for s in (first, second, conclusion)] == ['universal', 'universal', 'particular']
    assert exemplar_models['counterexample_rule_count'] == 0
    assert table['checked_cells'] == 48 and len(table['mismatches']) == 1
    assert table['mismatches'][0]['column'] == 'lower-right'
    assert table['mismatches'][0]['row'] == 8
    report = {
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python': sys.version, 'platform': platform.platform(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source': {'title': 'On the Symbols of Logic...', 'printed_pages': [91,94,95,101,102,103],
                   'scan': 'https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf',
                   'printed_to_full_pdf_page_offset': 16,
                   'p95_source_basis': 'Independent visual transcription; not OCR; printed mismatch retained.'},
        'contrary_categories': categories,
        'contrary_proper_nonempty': proper, 'contrary_unrestricted': unrestricted,
        'exemplar_nonempty': exemplar_models,
        'symbolic_intersection_count': len(intersection), 'symbolic_intersection': intersection,
        'page_95': table, 'named_countermodels': named_countermodels(),
        'limitation': 'Finite four-object verification; no claim of unbounded completeness.',
    }
    out = Path(__file__).with_name('results.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print('Source-math review: PASS')
    print('Contraries: 32 rules; categories 8 universal, 16 particular, 8 strengthened.')
    print('Nonempty proper model assignments: 2744; failed rules: 0.')
    print('Unrestricted model assignments: 4096; failed rules: 8 (all strengthened).')
    print('Exemplar: 36 rules; nonempty assignments: 3375; failed rules: 0.')
    print('Common symbolic triples: 21.')
    print('Page 95: 48 formula cells checked; lower-right row 8 is the sole mismatch.')
    print('Printed: ))(.)=(.( ; expected by p.94 rule: ))(.)=).) .')
    print('Named countermodels: PASS.')
    print('Detailed evidence: results.json (complete 48-cell trace included).')

if __name__ == '__main__':
    main()
