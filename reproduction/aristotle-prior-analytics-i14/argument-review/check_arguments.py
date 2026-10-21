"""Independent finite checks of the explicitly modern teaching claims.

No imports from the author model; no finite enumeration is a general proof.
"""
import itertools
import json
import platform

counts = {"attribute_pairs": 0, "bridge_instances": 0, "checks": 0}

def check(condition, label):
    counts["checks"] += 1
    if not condition:
        raise RuntimeError(label)

def mixed(worlds, x):
    bits = [bool(w & (1 << x)) for w in worlds]
    return any(bits) and not all(bits)

def universal(subject, worlds, n):
    return all(mixed(worlds, x) for x in range(n) if subject & (1 << x))

def particular(subject, worlds, n):
    return any(mixed(worlds, x) for x in range(n) if subject & (1 << x))

for n in (1, 2, 3):
    full = (1 << n) - 1
    seqs = list(itertools.product(range(full + 1), repeat=2))
    for a, b in itertools.product(seqs, repeat=2):
        counts["attribute_pairs"] += 1
        possible_b = b[0] | b[1]
        for s in range(full + 1):
            ca = tuple(full ^ w for w in a)
            check(universal(s, a, n) == universal(s, ca, n), "universal complement")
            check(particular(s, a, n) == particular(s, ca, n), "particular complement")
            check(not (s and universal(s, a, n)) or particular(s, a, n), "existential import")
            for t in range(full + 1):
                if possible_b & ~t:
                    continue
                counts["bridge_instances"] += 1
                major = universal(t, a, n)
                check(not (major and universal(s, b, n)) or universal(s, a, n), "universal bridge")
                check(not (major and particular(s, b, n)) or particular(s, a, n), "particular bridge")

# All three actual terms nonempty: actual-subject contingency is not transitive.
n = 2
a, b, c = (2, 0), (2, 1), (1, 1)
check(bool(a[0] and b[0] and c[0]), "nonempty actual terms")
check(universal(b[0], a, n), "countermodel major")
check(universal(c[0], b, n), "countermodel minor")
check(not universal(c[0], a, n), "countermodel universal conclusion fails")
check(not particular(c[0], a, n), "countermodel particular conclusion fails")
check(not universal(b[0] | b[1], a, n), "stronger bridge excludes countermodel")
# Empty subject does not supply a particular witness.
check(universal(0, a, n) and not particular(0, a, n), "empty subject")
# Paired teaching realizations for a particular major; terms are artificial.
n = 3
a, b = (5, 1), (4, 3)
for subject, necessary_positive in ((1, True), (2, False)):
    check(particular(b[0], a, n), "paired particular major")
    check(universal(subject, b, n), "paired universal minor")
    check(particular(subject, b, n), "paired particular minor")
    check(not universal(subject, a, n), "paired contingent universal fails")
    check(not particular(subject, a, n), "paired contingent particular fails")
    for aw in a:
        check((subject & ~aw == 0) == necessary_positive, "paired positive relation")
        check((subject & aw == 0) != necessary_positive, "paired negative relation")
# Author's smaller displayed pair, independently recomputed without imports.
n = 2
for a, b, subject, positive in (((3, 2), (3, 0), 2, True), ((1, 0), (3, 0), 2, False)):
    check(particular(b[0], a, n), "displayed particular major")
    check(universal(subject, b, n), "displayed universal minor")
    check(particular(subject, b, n), "displayed particular minor")
    check(not universal(subject, a, n), "displayed universal contingency fails")
    check(not particular(subject, a, n), "displayed particular contingency fails")
    check(all(subject & ~aw == 0 for aw in a) == positive, "displayed necessary positive")
    check(all(subject & aw == 0 for aw in a) != positive, "displayed necessary negative")
# Independently reproduce the manuscript's enumerated counts without model.py.
observed = dict(models=0, actual_premises=0, actual_failures=0,
                nonempty_premises=0, nonempty_failures=0,
                universal_bridge_premises=0, particular_bridge_premises=0)
for n in (1, 2):
    for bits in itertools.product(range(1 << n), repeat=6):
        a, b, c = (bits[0], bits[3]), (bits[1], bits[4]), (bits[2], bits[5])
        observed["models"] += 1
        premise = universal(b[0], a, n) and universal(c[0], b, n)
        conclusion = universal(c[0], a, n)
        observed["actual_premises"] += premise
        observed["actual_failures"] += premise and not conclusion
        nonempty = bool(a[0] and b[0] and c[0])
        observed["nonempty_premises"] += premise and nonempty
        observed["nonempty_failures"] += premise and nonempty and not conclusion
        strong = universal(b[0] | b[1], a, n)
        observed["universal_bridge_premises"] += strong and universal(c[0], b, n)
        observed["particular_bridge_premises"] += strong and particular(c[0], b, n)
check(observed == dict(models=4160, actual_premises=1332, actual_failures=276,
                      nonempty_premises=302, nonempty_failures=72,
                      universal_bridge_premises=812, particular_bridge_premises=584),
      "manuscript execution counts")
print(json.dumps({"status": "passed", "python": platform.python_version(), "counts": counts, "manuscript_counts": observed,
                  "scope": "Finite two-world modern semantic checks, not an ancient completeness/soundness proof."}, ensure_ascii=False, indent=2))
