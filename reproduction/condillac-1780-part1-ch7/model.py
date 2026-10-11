"""A bounded teaching model, not an empirical model of Condillac's psychology.

Python 3.10+, standard library only. Every public constructor/function validates
its inputs with explicit exceptions; required checks survive -O and -OO.
"""
from dataclasses import dataclass
from itertools import product

MAX_FEATURES = 8
MAX_OBJECTS = 32
MAX_VALUES = 8
MAX_CONCEPTS = 4096
MAX_ATOMS = 12
MAX_RULES = 128


def _symbol(value, label):
    if type(value) is not str or not value or value.strip() != value:
        raise ValueError(f"{label} must be a nonempty, trimmed string")


def _tuple(value, label, maximum=None):
    if type(value) is not tuple:
        raise ValueError(f"{label} must be a tuple")
    if maximum is not None and len(value) > maximum:
        raise ValueError(f"{label} exceeds the teaching budget {maximum}")


def _names(value, label, maximum=None):
    _tuple(value, label, maximum)
    for name in value:
        _symbol(name, label)
    if len(set(value)) != len(value):
        raise ValueError(f"{label} must be distinct")


@dataclass(frozen=True)
class Catalog:
    features: tuple
    domains: tuple
    objects: tuple

    def __post_init__(self):
        _names(self.features, "features", MAX_FEATURES)
        if not self.features:
            raise ValueError("at least one feature is required")
        _tuple(self.domains, "domains", MAX_FEATURES)
        if len(self.domains) != len(self.features):
            raise ValueError("one domain per feature is required")
        for domain in self.domains:
            _names(domain, "domain", MAX_VALUES)
            if not domain:
                raise ValueError("feature domains must be nonempty")
        _tuple(self.objects, "objects", MAX_OBJECTS)
        object_names = []
        for entry in self.objects:
            _tuple(entry, "object entry")
            if len(entry) != 2:
                raise ValueError("object entry must contain name and values")
            name, values = entry
            _symbol(name, "object name")
            object_names.append(name)
            _tuple(values, "object values", MAX_FEATURES)
            if len(values) != len(self.features):
                raise ValueError("object must have exactly one value per feature")
            for value, domain in zip(values, self.domains):
                _symbol(value, "feature value")
                if value not in domain:
                    raise ValueError("object value is outside its feature domain")
        if len(set(object_names)) != len(object_names):
            raise ValueError("object names must be distinct")


def _catalog(catalog):
    if type(catalog) is not Catalog:
        raise ValueError("a Catalog is required")
    catalog.__post_init__()


def _selection(catalog, features):
    _names(features, "selected features", MAX_FEATURES)
    if any(feature not in catalog.features for feature in features):
        raise ValueError("unknown feature")


def _object(catalog, name):
    _symbol(name, "object name")
    for object_name, values in catalog.objects:
        if name == object_name:
            return dict(zip(catalog.features, values))
    raise ValueError("unknown object")


@dataclass(frozen=True)
class Observation:
    object_name: str
    attributes: tuple
    provenance: str

    def __post_init__(self):
        _symbol(self.object_name, "object name")
        if type(self.provenance) is not str or self.provenance not in ("current", "recalled"):
            raise ValueError("provenance must be current or recalled")
        _tuple(self.attributes, "attributes", MAX_FEATURES)
        features = []
        for pair in self.attributes:
            _tuple(pair, "attribute")
            if len(pair) != 2:
                raise ValueError("an attribute requires feature and value")
            feature, value = pair
            _symbol(feature, "feature")
            _symbol(value, "value")
            features.append(feature)
        if len(set(features)) != len(features):
            raise ValueError("observed features must be distinct")


def _observation(catalog, observation):
    if type(observation) is not Observation:
        raise ValueError("an Observation is required")
    observation.__post_init__()
    actual = _object(catalog, observation.object_name)
    for feature, value in observation.attributes:
        if feature not in actual or actual[feature] != value:
            raise ValueError("observation must agree with the static catalog")


def attend(catalog, object_name, features, provenance="current"):
    """Project one named object onto selected features; other objects are omitted."""
    _catalog(catalog)
    _selection(catalog, features)
    actual = _object(catalog, object_name)
    return Observation(object_name, tuple((f, actual[f]) for f in features), provenance)


def compare(catalog, left, right, feature):
    """One feature judgment: unknown does not mean equal or different."""
    _catalog(catalog)
    _observation(catalog, left)
    _observation(catalog, right)
    _symbol(feature, "feature")
    _selection(catalog, (feature,))
    left_values, right_values = dict(left.attributes), dict(right.attributes)
    if feature not in left_values or feature not in right_values:
        return "unknown"
    return "equal" if left_values[feature] == right_values[feature] else "different"


def reflect(catalog, left, right, features):
    """An explicit sequence of comparisons, not a physiological mechanism."""
    _catalog(catalog)
    _selection(catalog, features)
    _observation(catalog, left)
    _observation(catalog, right)
    return tuple((feature, compare(catalog, left, right, feature)) for feature in features)


def equivalence_classes(catalog, features):
    """Partition the complete catalog by exact equality on selected features."""
    _catalog(catalog)
    _selection(catalog, features)
    indices = tuple(catalog.features.index(f) for f in features)
    groups = {}
    for name, values in catalog.objects:
        signature = tuple(values[index] for index in indices)
        groups.setdefault(signature, []).append(name)
    return tuple(tuple(group) for group in groups.values())


@dataclass(frozen=True)
class Concept:
    attributes: tuple
    witnesses: tuple

    def __post_init__(self):
        # Reuse structural attribute validation; no invented catalog object.
        Observation("concept", self.attributes, "recalled")
        _names(self.witnesses, "witnesses", MAX_OBJECTS)


def imagine(catalog, observations, features):
    """Cartesian recombination plus catalog witnesses, with an explicit cost cap."""
    _catalog(catalog)
    _tuple(observations, "observations", MAX_OBJECTS)
    _selection(catalog, features)
    if not features:
        raise ValueError("imagination requires at least one selected feature")
    for observation in observations:
        _observation(catalog, observation)
    pools = []
    count = 1
    for feature in features:
        values = sorted({value for obs in observations for key, value in obs.attributes if key == feature})
        if not values:
            raise ValueError("every selected feature needs an observed value")
        pools.append(values)
        count *= len(values)
    if count > MAX_CONCEPTS:
        raise ValueError("Cartesian product exceeds the teaching budget")
    concepts = []
    for values in product(*pools):
        attributes = tuple(zip(features, values))
        witnesses = tuple(name for name, actual in catalog.objects
                          if all(actual[catalog.features.index(f)] == v for f, v in attributes))
        concepts.append(Concept(attributes, witnesses))
    return tuple(concepts)


@dataclass(frozen=True)
class Rule:
    name: str
    premises: tuple
    conclusion: str

    def __post_init__(self):
        _symbol(self.name, "rule name")
        _names(self.premises, "premises", MAX_ATOMS)
        _symbol(self.conclusion, "conclusion")


@dataclass(frozen=True)
class Theory:
    atoms: tuple
    facts: tuple
    rules: tuple

    def __post_init__(self):
        _names(self.atoms, "atoms", MAX_ATOMS)
        _names(self.facts, "facts", MAX_ATOMS)
        if not set(self.facts).issubset(self.atoms):
            raise ValueError("facts must be declared atoms")
        _tuple(self.rules, "rules", MAX_RULES)
        names = []
        for rule in self.rules:
            if type(rule) is not Rule:
                raise ValueError("rules must be Rule instances")
            rule.__post_init__()
            if rule.conclusion not in self.atoms or not set(rule.premises).issubset(self.atoms):
                raise ValueError("rule mentions an undeclared atom")
            names.append(rule.name)
        if len(set(names)) != len(names):
            raise ValueError("rule names must be distinct")


def _theory(theory):
    if type(theory) is not Theory:
        raise ValueError("a Theory is required")
    theory.__post_init__()


@dataclass(frozen=True)
class Step:
    atom: str
    rule_name: object = None

    def __post_init__(self):
        _symbol(self.atom, "step atom")
        if self.rule_name is not None:
            _symbol(self.rule_name, "step rule")


def closure(theory):
    """Return a forward, acyclic certificate for the least Horn closure."""
    _theory(theory)
    known = set(theory.facts)
    steps = [Step(atom) for atom in theory.facts]
    changed = True
    while changed:
        changed = False
        for rule in theory.rules:
            if rule.conclusion not in known and all(p in known for p in rule.premises):
                known.add(rule.conclusion)
                steps.append(Step(rule.conclusion, rule.name))
                changed = True
    return tuple(steps)


def verify_certificate(theory, steps, target):
    """Independent local proof checking; malformed input raises, invalid proof is False."""
    _theory(theory)
    _tuple(steps, "steps", MAX_ATOMS)
    _symbol(target, "target")
    if target not in theory.atoms:
        raise ValueError("target must be declared")
    for step in steps:
        if type(step) is not Step:
            raise ValueError("certificate items must be Step instances")
        step.__post_init__()
    known = set()
    rules = {rule.name: rule for rule in theory.rules}
    for step in steps:
        if step.atom not in theory.atoms or step.atom in known:
            return False
        if step.rule_name is None:
            if step.atom not in theory.facts:
                return False
        else:
            rule = rules.get(step.rule_name)
            if rule is None or rule.conclusion != step.atom:
                return False
            if not set(rule.premises).issubset(known):
                return False
        known.add(step.atom)
    return target in known


def semantic_oracle(theory):
    """Truth-table entailment. Does not call closure or the proof checker.

    Return (entailed atoms in declaration order, number of satisfying valuations).
    The interpretation with all atoms true always models a positive Horn theory.
    """
    _theory(theory)
    forced = set(theory.atoms)
    model_count = 0
    for bits in product((False, True), repeat=len(theory.atoms)):
        valuation = dict(zip(theory.atoms, bits))
        if any(not valuation[fact] for fact in theory.facts):
            continue
        satisfies = True
        for rule in theory.rules:
            antecedent = True
            for premise in rule.premises:
                antecedent = antecedent and valuation[premise]
            if antecedent and not valuation[rule.conclusion]:
                satisfies = False
                break
        if satisfies:
            model_count += 1
            forced.intersection_update(atom for atom in theory.atoms if valuation[atom])
    return tuple(atom for atom in theory.atoms if atom in forced), model_count


def subset_syllogism(universe, small, middle, large):
    """Finite universal inclusion; no existential import is assumed."""
    _names(universe, "universe", MAX_OBJECTS)
    for label, group in (("small", small), ("middle", middle), ("large", large)):
        _names(group, label, MAX_OBJECTS)
        if not set(group).issubset(universe):
            raise ValueError("subset contains an element outside the universe")
    a, b, c = set(small), set(middle), set(large)
    premises = a.issubset(b) and b.issubset(c)
    conclusion = a.issubset(c)
    return {"premises": premises, "conclusion": conclusion,
            "implication": not premises or conclusion, "small_nonempty": bool(a)}
