"""Deterministic examples; JSON output is also the executable walkthrough data."""
import json
from model import EmbodiedMemory, Observation, SequenceMemory, Signal, WeightedHabits


def display_replay(memory, cue, context="", budget=20):
    result = memory.replay(cue, context, budget)
    return {"tokens": list(result.tokens), "stop": result.stop,
            "decision_count": len(result.decisions)}


def scenarios():
    output = {}
    m = SequenceMemory()
    m.practice(["do", "mi", "sol"], repetitions=2)
    output["exact_recovery"] = display_replay(m, "do")
    m.practice(["do", "fa", "la"], repetitions=2)
    output["shared_cue_tie"] = display_replay(m, "do")
    m.practice(["do", "mi", "sol"])
    output["practice_resolves_tie_but_not_intention"] = display_replay(m, "do")

    contextual = SequenceMemory()
    contextual.practice(["do", "mi", "sol"], "piece_A")
    contextual.practice(["do", "fa", "la"], "piece_B")
    output["context_repair"] = [display_replay(contextual, "do", c)
                                for c in ("piece_A", "piece_B")]
    repeated = SequenceMemory()
    repeated.practice(["A", "B", "A", "C"], "one_piece")
    output["within_piece_ambiguity"] = display_replay(repeated, "A", "one_piece")

    forgotten = SequenceMemory()
    forgotten.practice(["A", "B"], repetitions=3)
    forgotten.habits.forget(2)
    output["after_two_decay_units"] = {"edges": forgotten.habits.edge_count,
                                       "recall": display_replay(forgotten, "A")}
    forgotten.habits.forget(1)
    output["after_three_decay_units"] = {"edges": forgotten.habits.edge_count,
                                         "recall": display_replay(forgotten, "A")}
    limited = SequenceMemory(capacity=2)
    limited.practice(["A", "B", "C"])
    output["capacity_two"] = {"edges": limited.habits.edge_count,
                              "recall": display_replay(limited, "A")}

    left, right = SequenceMemory(), SequenceMemory()
    left.practice(["A", "B", "A", "C", "A", "B", "A", "C", "A"])
    right.practice(["A", "B", "A", "C", "A", "C", "A", "B", "A"])
    output["different_histories_same_weights"] = {
        "equal_snapshots": left.habits.snapshot() == right.habits.snapshot(),
        "equal_birth_metadata": left.habits._born == right.habits._born,
        "equal_serial": left.habits._serial == right.habits._serial,
        "left": display_replay(left, "A"), "right": display_replay(right, "A")}

    agent = EmbodiedMemory()
    agent.teach([Observation(x, Signal("ear_and_hand", x)) for x in ("do", "mi", "sol")],
                repetitions=2)
    agent.sense(Signal("ear_and_hand", "do"))
    recalled = agent.recall()
    before = agent.brain.habits.snapshot()
    body = recalled.outputs[-1]
    feedback = agent.feedback(body)
    agent.clear_active()
    output["reciprocal_paths_and_provenance"] = {
        "ideas": [{"idea": e.idea, "source": e.source,
                   "external_evidence": e.supports_external_object} for e in recalled.events],
        "body_signals": [e.signal.value if e is not None else None for e in recalled.outputs],
        "feedback_source": feedback.event.source,
        "feedback_external_evidence": feedback.event.supports_external_object,
        "active_after_clear": agent.active,
        "dispositions_unchanged": before == agent.brain.habits.snapshot()}
    agent.afferent_enabled = False
    output["blocked_incoming_path"] = agent.sense(Signal("ear_and_hand", "do")).status
    agent.set_cue("do")
    agent.efferent_enabled = False
    disconnected = agent.recall()
    output["central_replay_without_body_output"] = {
        "tokens": list(disconnected.replay.tokens),
        "nonempty_outputs": sum(x is not None for x in disconnected.outputs)}
    looping = SequenceMemory()
    looping.habits.reinforce(("", "A"), "A")
    output["cycle_guard"] = display_replay(looping, "A", budget=3)
    return output


if __name__ == "__main__":
    print(json.dumps(scenarios(), ensure_ascii=False, indent=2))
