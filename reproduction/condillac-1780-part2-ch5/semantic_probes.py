"""Small explicit behavioral oracles for semantic mutation experiments."""


class CheckFailure(Exception):
    pass


def check(condition, message):
    if not condition:
        raise CheckFailure(message)


def base(module, edges=()):
    return module.ClassSystem(("x", "y"), ("A", "B", "C"),
                              (frozenset(("x", "y")), frozenset(("x",)), frozenset()), edges)


def inclusion(module):
    s = base(module)
    check(not s.includes("A", "B"), "one positive member cannot prove inclusion")
    check(s.includes("A", "A"), "inclusion must be reflexive")


def empty(module):
    s = base(module)
    check(s.includes("C", "A"), "empty antecedent must be a subset")


def witness(module):
    check(base(module).witness("A", "B") == "y", "missing concrete counterexample")


def reflexivity(module):
    check(base(module).find_path("A", "A") == ("A",), "missing zero-edge path")


def direction(module):
    s = base(module, (("B", "A"),))
    check(s.find_path("A", "B") is None, "edge direction reversed or path invented")
    check(s.find_path("B", "A") == ("B", "A"), "directed edge lost")


def chain(module):
    s = base(module, (("C", "B"), ("B", "A")))
    try:
        path = s.prove("C", "A")
    except module.InvalidGraph:
        raise CheckFailure("a known-valid graph was rejected") from None
    check(path == ("C", "B", "A"), "transitive chain lost")


def global_gate(module):
    s = base(module, (("A", "B"),))
    try:
        s.prove("C", "C")
    except module.InvalidGraph:
        return
    raise CheckFailure("invalid disconnected edge did not block whole-graph certification")


def synonyms(module):
    s = module.ClassSystem(("x",), ("A", "B"), (frozenset(("x",)),) * 2)
    check(s.components() == (("A",), ("B",)), "coincident extensions are not graph SCCs")


def renaming(module):
    s = base(module).rename(("P", "Q", "R"))
    check(s.extension("P") == frozenset(("x", "y")), "renaming changed an extension")
    check(s.objects == ("x", "y"), "renaming changed the object universe")


def missing_edge(module):
    s = base(module)
    check(s.includes("B", "A") and s.find_path("B", "A") is None,
          "semantic truth and encoded reachability were conflated")


PROBES = (inclusion, empty, witness, reflexivity, direction, chain,
          global_gate, synonyms, renaming, missing_edge)


def run_probes(module):
    failures, errors = [], []
    for probe in PROBES:
        try:
            probe(module)
        except CheckFailure as error:
            failures.append({"probe": probe.__name__, "message": str(error)})
        except Exception as error:
            errors.append({"probe": probe.__name__, "type": type(error).__name__, "message": str(error)})
    return {"failures": failures, "errors": errors}
