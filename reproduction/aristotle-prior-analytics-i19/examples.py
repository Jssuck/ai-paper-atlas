"""Concrete models; examples are modern constructions, not empirical facts."""
from modal_model import Model


def make(domain, rows, actual=0):
    return Model(domain, [dict(zip(('A', 'B', 'C'), row)) for row in rows], actual)


def examples():
    # x=0 is an actual C; A varies. x=1 is an actual B and never A.
    # C can become B in the third world: simple exclusion need not be necessary.
    weak_not_necessary = make([0, 1], [({0}, {1}, {0}),
                                      (set(), {1}, {0}),
                                      (set(), {0, 1}, {0})])
    # Same premises, but C never B: strong contingency is not guaranteed.
    weak_not_strong = make([0, 1], [({0}, {1}, {0}),
                                   (set(), {1}, {0})])
    # Actual A=0, actual B=1: neither actual B ever A, but 0 later B.
    conversion_fails = make([0, 1], [({0}, {1}, {0}),
                                    ({0}, {0, 1}, {0})])
    # Box(a,A,C) holds because C itself changes, while C0 overlaps B0.
    awake = make([0], [({0}, {0}, {0}), (set(), {0}, set())])
    # Necessary affirmative in the anchored interpretation forces exclusion.
    anchored_affirmative = make([0, 1], [({0, 1}, {1}, {0}),
                                        ({0}, {1}, {0})])
    # A belongs contingently to one B, but not to any C. Exchanging the
    # necessary-negative side changes the particular conclusion's direction.
    reverse_particular = make([0, 1], [({0}, {0, 1}, {1}),
                                      (set(), {0, 1}, {1})])
    # Necessary negative only particular does not separate all B from C.
    particular_negative = make([0, 1], [({0}, {0, 1}, {0}),
                                       (set(), {0, 1}, {0})])
    # Worldwise exclusion and anchored exclusion differ if B changes.
    box_negative = make([0], [(set(), {0}, {0}), ({0}, set(), {0})])
    return dict(weak_not_necessary=weak_not_necessary,
                weak_not_strong=weak_not_strong,
                conversion_fails=conversion_fails, awake=awake,
                anchored_affirmative=anchored_affirmative,
                reverse_particular=reverse_particular,
                particular_negative=particular_negative,
                box_negative=box_negative)


def observations():
    specs = {
        'weak_not_necessary': [('N','e','A','B'),('C','a','A','C'),
            ('D','e','B','C'),('P','e','B','C'),('N','e','B','C')],
        'weak_not_strong': [('N','e','A','B'),('C','a','A','C'),
            ('D','e','B','C'),('P','e','B','C'),('C','e','B','C')],
        'conversion_fails': [('N','e','A','B'),('N','e','B','A')],
        'awake': [('Box','a','A','C'),('C','a','A','B'),
            ('D','a','B','C'),('D','e','B','C'),('N','a','A','C')],
        'anchored_affirmative': [('N','a','A','C'),('C','a','A','B'),
            ('D','e','B','C')],
        'reverse_particular': [('N','e','A','C'),('C','i','A','B'),
            ('D','o','C','B'),('D','o','B','C')],
        'particular_negative': [('N','o','A','B'),('C','a','A','C'),
            ('D','e','B','C'),('D','o','B','C')],
        'box_negative': [('Box','e','A','B'),('C','a','A','C'),
            ('N','e','A','B'),('D','e','B','C')],
    }
    return {name: dict(model=m.as_dict(), values={','.join(s):m.eval(*s)
                    for s in specs[name]}) for name,m in examples().items()}
