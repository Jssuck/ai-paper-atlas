"""Bounded exhaustive checks with independently enumerated finite oracles.

These checks are evidence about this implementation. They are not the general
proofs, which appear in README.md. No Python assert statement is used.
"""

from itertools import product

from model import (Multiset, descend_relation, descend_unary,
                   enumerate_policies, version_space)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def relation_checks():
    cases = successful = representation_tables = 0
    for size in range(4):
        domain = tuple(f"object_{i}" for i in range(size))
        pairs = tuple(product(domain, repeat=2))
        for codes in product(("a", "b"), repeat=size):
            representation_tables += 1
            representation = dict(zip(domain, codes))
            image = tuple(dict.fromkeys(codes))
            image_pairs = tuple(product(image, repeat=2))
            # Oracle: enumerate every potential quotient, rather than inspecting
            # constancy inside the fibers as the implementation does.
            candidates = tuple(dict(zip(image_pairs, bits))
                               for bits in product((False, True), repeat=len(image_pairs)))
            for bits in product((False, True), repeat=len(pairs)):
                relation = dict(zip(pairs, bits))
                valid = [candidate for candidate in candidates
                         if all(candidate[(representation[x], representation[y])] == relation[x, y]
                                for x, y in pairs)]
                result = descend_relation(domain, representation, relation)
                require(result.descends == bool(valid), "quotient existence mismatch")
                if valid:
                    require(len(valid) == 1, "quotient on image should be unique")
                    require(result.quotient == valid[0], "quotient value mismatch")
                    require(not result.conflicts, "successful descent has a conflict")
                    successful += 1
                else:
                    require(bool(result.conflicts), "failed descent lacks witness")
                    for conflict in result.conflicts:
                        for pair in (conflict.true_pair, conflict.false_pair):
                            require(tuple(representation[x] for x in pair) == conflict.representation_pair,
                                    "witness outside its fiber rectangle")
                        require(relation[conflict.true_pair] is True, "true witness is false")
                        require(relation[conflict.false_pair] is False, "false witness is true")
                cases += 1
    return {"domain_sizes": list(range(4)), "available_representation_labels": 2,
            "representation_tables": representation_tables, "relation_cases": cases,
            "successful_descents": successful, "failed_descents": cases - successful}


def unary_checks():
    cases = successful = 0
    for size in range(4):
        domain = tuple(f"object_{i}" for i in range(size))
        for codes in product(("a", "b"), repeat=size):
            representation = dict(zip(domain, codes))
            image = tuple(dict.fromkeys(codes))
            candidates = tuple(dict(zip(image, bits)) for bits in product((False, True), repeat=len(image)))
            for bits in product((False, True), repeat=size):
                predicate = dict(zip(domain, bits))
                valid = [candidate for candidate in candidates
                         if all(candidate[representation[x]] == predicate[x] for x in domain)]
                result = descend_unary(domain, representation, predicate)
                require((result.quotient is not None) == bool(valid), "unary existence mismatch")
                if valid:
                    require(len(valid) == 1 and result.quotient == valid[0], "unary value mismatch")
                    successful += 1
                else:
                    require(bool(result.conflicts), "failed unary descent lacks witness")
                    for label, yes, no in result.conflicts:
                        require(representation[yes] == representation[no] == label, "bad unary fiber")
                        require(predicate[yes] is True and predicate[no] is False, "bad unary witness")
                cases += 1
    return {"domain_sizes": list(range(4)), "predicate_cases": cases, "successful_descents": successful}


def multiset_checks():
    source = ("blue", "red")
    target = ("cool", "warm")
    multisets = tuple(Multiset(source, counts) for counts in product(range(3), repeat=2))
    zero = Multiset.from_pairs(source)
    renamings = tuple(dict(zip(source, image)) for image in product(target, repeat=2))
    projections = tuple(tuple(atom for atom, keep in zip(source, mask) if keep)
                        for mask in product((False, True), repeat=2))
    rename_cases = projection_cases = associative_cases = scale_cases = 0
    for left in multisets:
        require(left.add(zero) == left == zero.add(left), "identity failed")
        require(left.scale(0) == zero, "zero scale failed")
        for right in multisets:
            summed = left.add(right)
            # Independent coordinate formula, not a comparison of only two API paths.
            expected_counts = tuple(left.counts[i] + right.counts[i] for i in range(2))
            require(summed.counts == expected_counts, "coordinate addition failed")
            require(summed == right.add(left), "commutativity failed")
            for mapping in renamings:
                expected = tuple(sum(expected_counts[i] for i, atom in enumerate(source)
                                     if mapping[atom] == output) for output in target)
                renamed = summed.rename(target, mapping)
                require(renamed.counts == expected, "renaming count formula failed")
                require(renamed == left.rename(target, mapping).add(right.rename(target, mapping)),
                        "renaming homomorphism failed")
                require(renamed.total == summed.total, "renaming should preserve total multiplicity")
                rename_cases += 1
            for kept in projections:
                expected = tuple(expected_counts[source.index(atom)] for atom in kept)
                require(summed.project(kept).counts == expected, "projection coordinate formula failed")
                require(summed.project(kept) == left.project(kept).add(right.project(kept)),
                        "projection homomorphism failed")
                projection_cases += 1
            for factor in range(4):
                require(summed.scale(factor) == left.scale(factor).add(right.scale(factor)),
                        "scalar distribution failed")
                scale_cases += 1
            for third in multisets:
                require(left.add(right).add(third) == left.add(right.add(third)), "associativity failed")
                associative_cases += 1
    return {"alphabet_size": 2, "input_counts_per_atom": [0, 1, 2], "multisets": len(multisets),
            "ordered_addition_pairs": len(multisets) ** 2, "renaming_maps": len(renamings),
            "renaming_homomorphism_cases": rename_cases, "projection_subsets": len(projections),
            "projection_homomorphism_cases": projection_cases, "associativity_cases": associative_cases,
            "scale_factors": list(range(4)), "scale_distribution_cases": scale_cases}


def policy_checks():
    cases = prediction_checks = 0
    for size in range(4):
        stimuli = tuple(f"tile_{i}" for i in range(size))
        actions = ("left", "right")
        admissible = enumerate_policies(stimuli, actions)
        for truth in product(actions, repeat=size):
            for mask in product((False, True), repeat=size):
                observations = tuple((s, response) for s, response, keep in zip(stimuli, truth, mask) if keep)
                space = version_space(stimuli, actions, admissible, observations)
                # Counting oracle: each unobserved stimulus has two independent choices.
                require(len(space.survivors) == 2 ** (size - sum(mask)), "version-space cardinality mismatch")
                for stimulus, answer, observed in zip(stimuli, truth, mask):
                    expected = (answer,) if observed else tuple(sorted(actions))
                    require(space.possible_actions(stimulus) == expected, "prediction-set mismatch")
                    require(space.unanimous(stimulus) == (answer if observed else None), "unanimity mismatch")
                    prediction_checks += 1
                cases += 1
    return {"stimulus_sizes": list(range(4)), "actions": 2, "truth_observation_cases": cases,
            "individual_prediction_checks": prediction_checks}


def run_all():
    return {"relations": relation_checks(), "unary_predicates": unary_checks(),
            "multisets": multiset_checks(), "policies": policy_checks()}


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2, sort_keys=True))
