"""Deterministic, machine-readable worked cases; no external data or randomness."""
import json
from model import Language, pack, version_space


def cases():
    schema = {"agent": ("A", "B"), "patient": ("A", "B"), "act": ("help", "avoid")}
    language = Language(schema, (("agent", "act"), ("patient", "act")))
    message = ("A", "B", "help")
    tokens = language.encode(message, ("agent", "patient", "act"))
    alternate = language.encode(message, ("patient", "agent", "act"))
    swapped = ("B", "A", "help")
    codes = dict(language.lexicon)
    codes[("act", "avoid")] = codes[("act", "help")]
    colliding = Language(schema, language.edges, codes)
    collision_tokens = colliding.encode(message, language.orders[0])
    hypotheses = (("0", "1", "2"), ("0", "1", "4"), ("1", "2", "3"))
    remaining = version_space(hypotheses, ((0, "0"), (1, "1")))
    return {
        "scope": "Modern finite teaching abstraction; no historical algorithm or psychological validation.",
        "context": {"edges": sorted(language.edges), "legal_orders": language.orders},
        "serial": {"message": message, "tokens": tokens, "wire": pack(tokens),
                   "prefix_candidate_counts": [len(language.candidates(tokens[:k])) for k in range(4)],
                   "decoded": language.decode(pack(tokens)),
                   "alternate_decoded": language.decode(pack(alternate))},
        "binding_loss": {"first": message, "second": swapped,
                         "same_unlabeled_aggregate": language.aggregate(message) == language.aggregate(swapped),
                         "same_labeled_set": language.labeled(message) == language.labeled(swapped)},
        "dictionary_collision": {"injective": colliding.injective,
                                 "full_frame_candidates": sorted(colliding.candidates(collision_tokens))},
        "framing": {"first": ("a", "bc"), "second": ("ab", "c"),
                    "same_plain_concatenation": "a" + "bc" == "ab" + "c",
                    "same_json_frame": pack(("a", "bc")) == pack(("ab", "c"))},
        "analogy_limit": {"examples": ((0, "0"), (1, "1")), "remaining_tables": sorted(remaining),
                          "unseen_symbol_2_predictions": sorted({table[2] for table in remaining}),
                          "affine_prior_remaining": sorted(version_space((hypotheses[0], hypotheses[2]),
                                                                        ((0, "0"), (1, "1"))))}
    }


if __name__ == "__main__":
    print(json.dumps(cases(), ensure_ascii=False, indent=2))
