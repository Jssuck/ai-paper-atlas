"""Independent finite oracle: enumerate possible decoders, not fiber tests.

All H with 0..4 labelled states, all two-bit observation assignments,
and all Boolean queries. Also exhaustively check binary observation extension.
"""
import json
from itertools import product
from finite_model import FiniteModel


Y = tuple(product((0, 1), repeat=2))
DECODERS = tuple(dict(zip(Y, bits)) for bits in product((0, 1), repeat=len(Y)))


def run():
    if not __debug__:
        raise RuntimeError("Do not use -O: this oracle requires assertions")
    query_cases = extension_cases = local_answers = 0
    for n in range(5):
        states = tuple(f"h{i}" for i in range(n))
        for rows in product(Y, repeat=n):
            model = FiniteModel.from_rows(("x", "y"), dict(zip(states, rows)))
            for bits in product((0, 1), repeat=n):
                query = dict(zip(states, bits))
                # Oracle: is there ANY total decoder d:Y->{0,1} with q=d∘O?
                decodable = any(all(decoder[rows[i]] == bits[i] for i in range(n))
                                for decoder in DECODERS)
                assert model.globally_identifiable(query) == decodable
                for observed in Y + ((9, 9),):
                    possible = {bits[i] for i in range(n) if rows[i] == observed}
                    expected = ("inconsistent" if not possible else
                                "identified" if len(possible) == 1 else "ambiguous")
                    answer = model.answer(observed, query)
                    assert answer.status == expected
                    assert set(answer.values) == possible
                    local_answers += 1
                query_cases += 1
            for extra in product((0, 1), repeat=n):
                extension = model.append_observation("z", dict(zip(states, extra)))
                assert extension.refines(model)
                # Independent pairwise criterion for whether ANY split occurred.
                no_split = all(rows[i] != rows[j] or extra[i] == extra[j]
                               for i in range(n) for j in range(n))
                assert model.refines(extension) == no_split
                assert extension.signatures == tuple(rows[i] + (extra[i],) for i in range(n))
                extension_cases += 1
    return {"state_counts": [0, 1, 2, 3, 4], "observation_alphabet": list(Y),
            "boolean_queries_checked": query_cases, "current_answers_checked": local_answers,
            "observation_extensions_checked": extension_cases, "result": "PASS"}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
