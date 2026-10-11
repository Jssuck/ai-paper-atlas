"""Run deterministic, explicitly invented teaching traces (no external inputs)."""
from model import Belief, Model, Observation, judge


def show(label: str, belief: Belief) -> None:
    print(f"{label}: candidates={belief.candidates}, recognized={belief.recognizes()}")
    print(f"  retained={tuple((e.query, e.outcome) for e in belief.history)}")


def main() -> None:
    model = Model(
        ("nurse", "lookalike", "visitor"),
        (
            Observation("distant_view", ("familiar", "familiar", "unfamiliar")),
            Observation("closer_view", ("face_A", "face_B", "face_C")),
        ),
    )
    truth = "lookalike"
    initial = Belief(model)
    print("MODERN STIPULATED MODEL; not Condillac's algorithm or empirical psychology.")
    print("1. Hasty guess and correcting observation (invented scene).")
    show("initial", initial)
    first = initial.consult("distant_view", truth)
    show("distant", first)
    hasty = judge(model, "nurse", truth, satisfied=True)
    print(f"guess=nurse, correct={hasty.correct}, satisfied={hasty.satisfied}")
    print("The guess is not accepted evidence; the two candidates are retained.")
    print(f"closer_view distinguishes={first.distinguishes('closer_view')}")
    corrected = first.consult("closer_view", truth)
    show("closer", corrected)
    print(f"original state unchanged={initial.history == ()}")

    print("\n2. Refusal blocks this otherwise available correction.")
    refused = first.consult("closer_view", truth, accept=False)
    show("refused", refused)
    print(f"same state={refused is first}")
    print("Refusal is stipulated by accept=False; no psychology is inferred.")

    print("\n3. Available observations cannot separate every pair.")
    twins = Model(
        ("A", "B", "C"),
        (Observation("shape", ("round", "round", "square")),
         Observation("sound", ("soft", "soft", "loud"))),
    )
    ambiguous = Belief(twins)
    for query in ("shape", "sound", "shape", "sound"):
        ambiguous = ambiguous.consult(query, "A")
    show("after repeated queries", ambiguous)
    print(f"full signature fiber(A)={twins.fiber('A')}")

    print("\n4. Satisfaction is supplied independently of correctness.")
    for guess in ("nurse", "lookalike"):
        for satisfied in (False, True):
            value = judge(model, guess, truth, satisfied=satisfied)
            print(f"guess={guess}, correct={value.correct}, satisfied={value.satisfied}")
    print("This counterexample refutes only a proposed universal implication")
    print("within our stipulated model; it measures no real person's feelings.")

    print("\n5. Practice as repeated execution, without a skill-acquisition claim.")
    for world in model.worlds:
        state = Belief(model)
        for query in ("distant_view", "closer_view"):
            state = state.consult(query, world)
        print(f"case={world}, recognized={state.recognizes()}, observations={len(state.history)}")
    print("No training, speed-up, historical experiment, or empirical result is claimed.")


if __name__ == "__main__":
    main()
