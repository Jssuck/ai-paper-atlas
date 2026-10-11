#!/usr/bin/env python3
"""Independent finite-model oracle, contracts, traces, and CLI audit.

Oracle representation: two bit masks and two integers. It never uses the
implementation's domain generator, transition, examples, or reports as truth.
All writes stay in independent-review/. Python standard library only.
"""
from collections import Counter, deque
from dataclasses import fields, FrozenInstanceError, replace
from datetime import datetime, timezone
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "outputs"
LOGS = HERE / "logs"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("audited_memory_model", ROOT / "memory_model.py")
dut = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = dut
spec.loader.exec_module(dut)

NAMES = (None, "fire", "bell")
OPS = (("perceive", 1), ("perceive", 2), ("withdraw", 0),
       ("set_aside", 0), ("recall", 1), ("recall", 2),
       ("make_inaccessible", 1), ("make_inaccessible", 2), ("erase_all", 0))
EMPTY = (0, 0, 0, 0)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def portable(text):
    """Normalize path prefixes only; preserve messages, statuses, and timings."""
    return str(text).replace(str(ROOT), ".").replace(sys.executable, Path(sys.executable).name)


def bit(token):
    return 0 if token == 0 else 1 << (token - 1)


def valid(state):
    retained, available, attention, sensory = state
    return not (available & ~retained) and not (bit(attention) & ~available) and not (bit(sensory) & ~available)


DOMAIN = tuple(s for s in itertools.product(range(4), range(4), range(3), range(3)) if valid(s))


def oracle(state, action):
    """Independently expressed bitwise specification, not a DUT wrapper."""
    retained, available, attention, sensory = state
    operation, token = action
    recognized = recalled = None
    mask = bit(token)
    if operation == "make_inaccessible":
        if retained & mask == 0:
            return "unretained"
        if sensory == token:
            return "currently_presented"
    if operation == "perceive":
        recognized = bool(retained & mask)
        next_state = (retained | mask, available | mask, token, token)
    elif operation == "withdraw":
        next_state = (retained, available, attention, 0)
    elif operation == "set_aside":
        next_state = (retained, available, 0, sensory)
    elif operation == "recall":
        recalled = bool(available & mask)
        next_state = (retained, available, token if recalled else attention, sensory)
    elif operation == "make_inaccessible":
        next_state = (retained, available & ~mask, 0 if attention == token else attention, sensory)
    elif operation == "erase_all":
        next_state = EMPTY
    else:
        raise RuntimeError(operation)
    return next_state, (next_state[2], next_state[3], next_state[3], recognized, recalled)


def state_json(state):
    retained, available, attention, sensory = state
    return {"retained": sorted(NAMES[x] for x in (1, 2) if retained & bit(x)),
            "recallable": sorted(NAMES[x] for x in (1, 2) if available & bit(x)),
            "attention": NAMES[attention], "sensory": NAMES[sensory]}


def output_json(output):
    return dict(zip(("attention", "sensory_input", "current_existence_conviction", "recognized", "recall_succeeded"),
                    (NAMES[output[0]], NAMES[output[1]], NAMES[output[2]], output[3], output[4])))


def encode(state):
    return (sum(bit(NAMES.index(x.value)) for x in state.retained),
            sum(bit(NAMES.index(x.value)) for x in state.recallable),
            0 if state.attention is None else NAMES.index(state.attention.value),
            0 if state.sensory is None else NAMES.index(state.sensory.value))


def materialize(state):
    return dut.State(frozenset(dut.Cue(NAMES[x]) for x in (1, 2) if state[0] & bit(x)),
                     frozenset(dut.Cue(NAMES[x]) for x in (1, 2) if state[1] & bit(x)),
                     None if state[2] == 0 else dut.Cue(NAMES[state[2]]),
                     None if state[3] == 0 else dut.Cue(NAMES[state[3]]))


def materialize_action(action):
    return dut.Action(dut.Kind(action[0]), None if action[1] == 0 else dut.Cue(NAMES[action[1]]))


def actual(state, action, transition=None):
    transition = dut.transition if transition is None else transition
    before = materialize(state)
    operation = materialize_action(action)
    snapshot = before.to_dict(), operation.to_dict()
    try:
        after, output = transition(before, operation)
    except ValueError as exc:
        require(snapshot == (before.to_dict(), operation.to_dict()), "invalid operation mutated arguments")
        require(type(exc) is dut.PreconditionError, "unexpected ValueError masquerading as a precondition reject")
        return "unretained" if "unretained" in str(exc) else "currently_presented" if "withdraw" in str(exc) else type(exc).__name__
    require(snapshot == (before.to_dict(), operation.to_dict()), "transition mutated arguments")
    require(type(after) is dut.State and type(output) is dut.Output, "wrong return types")
    require(after.to_dict() == state_json(encode(after)), "state serialization does not represent returned fields")
    out = output.to_dict()
    # Distinguish false from 0 and null from false; Python equality alone cannot.
    for key in ("recognized", "recall_succeeded"):
        require(out[key] is None or type(out[key]) is bool, f"invalid report type: {key}")
    output_tuple = (NAMES.index(out["attention"]), NAMES.index(out["sensory_input"]),
                    NAMES.index(out["current_existence_conviction"]), out["recognized"], out["recall_succeeded"])
    return encode(after), output_tuple


def graph_audit():
    edges = []
    counts = Counter()
    per_action = {}
    reference = {}
    for state, action in itertools.product(DOMAIN, OPS):
        expected = oracle(state, action)
        observed = actual(state, action)
        require(expected == observed, f"oracle mismatch {state} {action}: {expected} != {observed}")
        reference[(state, action)] = observed
        label = expected if isinstance(expected, str) else "valid"
        counts[label] += 1
        per_action.setdefault(action[0] + (":" + NAMES[action[1]] if action[1] else ""), Counter())[label] += 1
        record = {"state": state_json(state), "action": {"kind": action[0], "cue": NAMES[action[1]]}, "status": label}
        if not isinstance(expected, str):
            after, output = expected
            require(valid(after) and after in DOMAIN, "oracle left its independently enumerated domain")
            record.update(next_state=state_json(after), output=output_json(output))
        edges.append(record)
    # Fresh objects, reverse order and interleaved complete histories expose history-dependent results.
    for state, action in reversed(list(itertools.product(DOMAIN, OPS))):
        actual((3, 3, 2, 1), ("erase_all", 0))
        actual(EMPTY, ("perceive", 2))
        require(actual(state, action) == reference[(state, action)], "result depends on call order/hidden history")
    def reachable(step):
        paths = {EMPTY: []}
        queue = deque([EMPTY])
        while queue:
            state = queue.popleft()
            for action in OPS:
                result = step(state, action)
                if isinstance(result, str):
                    continue
                after = result[0]
                if after not in paths:
                    paths[after] = paths[state] + [action]
                    queue.append(after)
        return paths
    oracle_paths, actual_paths = reachable(oracle), reachable(actual)
    require(set(oracle_paths) == set(DOMAIN) == set(actual_paths), "reachable graphs disagree")
    require({encode(s) for s in dut.all_states()} == set(DOMAIN), "DUT state enumeration differs from independent domain")
    require(len(dut.all_states()) == len(DOMAIN), "duplicate enumerated states")
    require({(a.kind.value, 0 if a.cue is None else NAMES.index(a.cue.value)) for a in dut.all_actions()} == set(OPS), "action alphabet differs")
    for state in DOMAIN:
        require(actual(state, ("erase_all", 0))[0] == EMPTY, "reset leaves state/history")
    require({f.name for f in fields(dut.State)} == {"retained", "recallable", "attention", "sensory"}, "unexpected state field")
    (OUT / "complete_graph.json").write_text(json.dumps(edges, indent=2) + "\n")
    (OUT / "reachability_witnesses.json").write_text(json.dumps([
        {"state": state_json(s), "shortest_path": [{"kind": a[0], "cue": NAMES[a[1]]} for a in oracle_paths[s]]} for s in DOMAIN], indent=2) + "\n")
    return {"states": len(DOMAIN), "reachable_states": len(actual_paths), "actions": len(OPS),
            "state_action_pairs": len(edges), "successful_transitions": counts["valid"],
            "rejected_preconditions": counts["unretained"] + counts["currently_presented"],
            "rejection_reasons": {k: v for k, v in counts.items() if k != "valid"},
            "longest_shortest_path": max(map(len, oracle_paths.values())), "per_action": per_action}


def contract_audit():
    records = []
    def reject(label, exc, thunk):
        try:
            thunk()
        except exc as caught:
            records.append({"case": label, "exception": type(caught).__name__})
        else:
            raise AssertionError(f"{label}: expected {exc.__name__}")
    f, b = dut.Cue.FIRE, dut.Cue.BELL
    for state in itertools.product(range(4), range(4), range(3), range(3)):
        if valid(state):
            require(encode(materialize(state)) == state, "valid constructor round trip failed")
        else:
            reject(f"invalid finite constructor {state}", ValueError, lambda s=state: materialize(s))
    bad_fields = {"retained": [None, [], {f}, "fire", 0, frozenset({"fire"}), frozenset({None}), frozenset({True})],
                  "recallable": [None, [], {f}, "fire", 0, frozenset({"fire"})],
                  "attention": [False, 0, "fire", {}, []], "sensory": [False, 0, "fire", {}, []]}
    for field, values in bad_fields.items():
        for i, value in enumerate(values):
            reject(f"state type {field}/{i}", TypeError, lambda field=field, value=value: dut.State(**{field: value}))
    for kind, cue, exception in [("recall", f, TypeError), (False, None, TypeError), (None, None, TypeError),
                                  (dut.Kind.RECALL, None, TypeError), (dut.Kind.RECALL, False, TypeError),
                                  (dut.Kind.PERCEIVE, "fire", TypeError), (dut.Kind.MAKE_INACCESSIBLE, 1, TypeError),
                                  (dut.Kind.WITHDRAW, f, ValueError), (dut.Kind.SET_ASIDE, b, ValueError),
                                  (dut.Kind.ERASE_ALL, f, ValueError)]:
        reject(f"action type/precondition {kind}/{cue}", exception, lambda k=kind, c=cue: dut.Action(k, c))
    class StateSubclass(dut.State):
        pass
    class ActionSubclass(dut.Action):
        pass
    for s, a in [(None, materialize_action(("withdraw", 0))), ({}, materialize_action(("withdraw", 0))),
                 (dut.State(), None), (dut.State(), {}), (StateSubclass(), materialize_action(("withdraw", 0))),
                 (dut.State(), ActionSubclass(dut.Kind.WITHDRAW))]:
        reject(f"transition argument type {type(s).__name__}/{type(a).__name__}", TypeError, lambda s=s, a=a: dut.transition(s, a))
    serialized = state_json(EMPTY)
    state_bad = [None, [], {}, {**serialized, "ever_seen": True}, {k: v for k, v in serialized.items() if k != "sensory"},
                 {**serialized, "retained": ("fire",)}, {**serialized, "retained": ["fire", "fire"]},
                 {**serialized, "retained": ["new-token"]}, {**serialized, "retained": [True]},
                 {**serialized, "recallable": ["fire"]}, {**serialized, "sensory": "fire"},
                 {**serialized, "attention": 0}, {**serialized, "recallable": [None]}]
    for i, data in enumerate(state_bad):
        reject(f"state deserialization {i}", (TypeError, ValueError), lambda d=data: dut.State.from_dict(d))
    for i, data in enumerate([None, [], {}, {"kind": "recall"}, {"kind": 1, "cue": None},
                              {"kind": "recall", "cue": None}, {"kind": "recall", "cue": "dragon"},
                              {"kind": "withdraw", "cue": "fire"}, {"kind": "erase_all", "cue": False},
                              {"kind": "erase_all", "cue": None, "extra": True}, {"kind": "missing", "cue": None}]):
        reject(f"action deserialization {i}", (TypeError, ValueError), lambda d=data: dut.Action.from_dict(d))
    for state in DOMAIN:
        s = materialize(state)
        require(encode(dut.State.from_dict(json.loads(json.dumps(state_json(state))))) == state, "serialized state mismatch")
        reject(f"immutable state {state}", FrozenInstanceError, lambda s=s: setattr(s, "attention", None))
    for action in OPS:
        a = materialize_action(action)
        require(dut.Action.from_dict(json.loads(json.dumps(a.to_dict()))) == a, "serialized action mismatch")
        reject(f"immutable action {action}", FrozenInstanceError, lambda a=a: setattr(a, "cue", None))
    (OUT / "invalid_and_immutable_cases.json").write_text(json.dumps(records, indent=2) + "\n")
    return {"constructor_domain_candidates": 144, "valid_constructors": len(DOMAIN),
            "invalid_constructors": 144 - len(DOMAIN), "negative_and_immutability_cases": len(records),
            "state_round_trips": len(DOMAIN), "action_round_trips": len(OPS)}


def expected_trace(actions):
    state = EMPTY
    result = {"initial_state": state_json(state), "steps": []}
    for index, action in enumerate(actions, 1):
        state, output = oracle(state, action)
        result["steps"].append({"step": index, "action": {"kind": action[0], "cue": NAMES[action[1]]},
                                "state": state_json(state), "output": output_json(output)})
    return result


CASES = {
    "retained_is_not_currently_attended": [("perceive", 1), ("withdraw", 0), ("set_aside", 0), ("set_aside", 0)],
    "recalled_fire_without_present_sensory_conviction": [("perceive", 1), ("withdraw", 0), ("set_aside", 0), ("recall", 1)],
    "inaccessible_then_recognized": [("perceive", 1), ("withdraw", 0), ("make_inaccessible", 1), ("recall", 1), ("perceive", 1)],
    "never_seen_then_not_recognized": [("recall", 1), ("perceive", 1)],
    "complete_erasure_then_not_recognized": [("perceive", 1), ("erase_all", 0), ("recall", 1), ("perceive", 1)],
    "recall_fire_while_perceiving_bell": [("perceive", 1), ("perceive", 2), ("recall", 1)],
    "recall_with_independent_current_fire_input": [("perceive", 1), ("recall", 1)],
}


def trace_audit():
    expected = {label: expected_trace(actions) for label, actions in CASES.items()}
    result = dut.demo()
    require(result["cases"] == expected, "demo differs from independently specified trace")
    require(result == dut.demo(), "demo not deterministic")
    witness = result["equal_state_witness"]
    require(witness["fresh_state"] == witness["erased_state"] == state_json(EMPTY), "reset witness mismatch")
    require(witness["same_complete_state"] is True and witness["same_next_state_and_output"] is True,
            "reset witness labels incorrect")
    require(witness["recognition_after_either_history"] is False, "reset witness recognition incorrect")
    # Failure-only reports coincide despite different complete states.
    require(oracle((1, 0, 0, 0), ("recall", 1))[1] == oracle(EMPTY, ("recall", 1))[1], "failure observations differ")
    require(oracle((1, 0, 0, 0), ("perceive", 1))[1][3] is True and
            oracle(EMPTY, ("perceive", 1))[1][3] is False, "retention distinction missing")
    require("not a historical algorithm or empirical simulation" in result["scope"], "missing scope warning")
    require("invented" in result["token_note"], "missing invented-token label")
    (OUT / "independent_expected_traces.json").write_text(json.dumps(expected, indent=2) + "\n")
    return {"traces": len(expected), "trace_steps": sum(len(v) for v in CASES.values()), "observer_witness_verified": True}


def mutation_audit():
    """Check that the oracle detects seven plausible pedagogical mistakes."""
    detected = []
    def mutated(label):
        def run(state, action):
            after, out = dut.transition(state, action)
            if label == "recognize_after_encoding" and action.kind is dut.Kind.PERCEIVE:
                out = replace(out, recognized=True)
            elif label == "recall_creates_sensory_input" and action.kind is dut.Kind.RECALL and out.recall_succeeded:
                after = replace(after, sensory=action.cue)
                out = replace(out, sensory_input=action.cue, current_existence_conviction=action.cue)
            elif label == "set_aside_erases_memory" and action.kind is dut.Kind.SET_ASIDE:
                after = dut.State()
                out = dut.Output(None, None, None)
            elif label == "inaccessibility_erases_retention" and action.kind is dut.Kind.MAKE_INACCESSIBLE:
                after = replace(after, retained=after.retained - {action.cue})
            elif label == "reset_keeps_history" and action.kind is dut.Kind.ERASE_ALL:
                after = dut.State(state.retained)
            elif label == "failed_recall_clears_attention" and action.kind is dut.Kind.RECALL and out.recall_succeeded is False:
                after = replace(after, attention=None)
                out = replace(out, attention=None)
            elif label == "conviction_follows_attention":
                out = replace(out, current_existence_conviction=after.attention)
            return after, out
        return run
    labels = ["recognize_after_encoding", "recall_creates_sensory_input", "set_aside_erases_memory",
              "inaccessibility_erases_retention", "reset_keeps_history", "failed_recall_clears_attention",
              "conviction_follows_attention"]
    for label in labels:
        for state, action in itertools.product(DOMAIN, OPS):
            if actual(state, action, mutated(label)) != oracle(state, action):
                detected.append({"mutation": label, "witness_state": state_json(state),
                                 "witness_action": {"kind": action[0], "cue": NAMES[action[1]]}})
                break
        else:
            raise AssertionError(f"oracle did not detect {label}")
    (OUT / "mutation_witnesses.json").write_text(json.dumps(detected, indent=2) + "\n")
    return {"plausible_mutations": len(labels), "detected": len(detected)}


def run_command(label, argv, expected_exit=0, cwd=ROOT, env_extra=None):
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0", **(env_extra or {})}
    started = datetime.now(timezone.utc).isoformat()
    start = time.perf_counter()
    result = subprocess.run(argv, cwd=cwd, env=environment, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    (LOGS / f"{label}.log").write_text(portable(f"Command: {shlex.join(argv)}\nCWD: {cwd}\nStarted UTC: {started}\n"
                                     f"Exit code: {result.returncode}\nElapsed seconds: {elapsed:.6f}\n"
                                     f"\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"))
    require(result.returncode == expected_exit, f"{label}: exit {result.returncode}, expected {expected_exit}: {result.stderr}")
    return result


def cli_audit(graph):
    module = str(ROOT / "memory_model.py")
    default = run_command("cli_default", [sys.executable, module])
    demo = run_command("cli_demo", [sys.executable, module, "--demo"])
    require(default.stdout == demo.stdout, "default CLI not demo")
    require(json.loads(demo.stdout) == dut.demo(), "CLI demo mismatch")
    report = json.loads(run_command("cli_check", [sys.executable, module, "--check"]).stdout)
    for key in ("states", "reachable_states", "actions", "state_action_pairs", "successful_transitions", "rejected_preconditions"):
        require(report[key] == graph[key], f"false CLI coverage label {key}")
    require(report["status"] == "PASS" and "not empirical cognition" in report["model_kind"], "CLI scope/status mismatch")
    optimized = run_command("cli_check_optimized", [sys.executable, "-O", module, "--check"])
    require(json.loads(optimized.stdout) == report, "optimized report mismatch")
    output = OUT / "nested" / "cli_demo.json"
    file_result = run_command("cli_output_file", [sys.executable, module, "--output", str(output)])
    require(file_result.stdout == "" and json.loads(output.read_text()) == json.loads(demo.stdout), "file-output CLI mismatch")
    run_command("cli_conflicting_modes", [sys.executable, module, "--demo", "--check"], 2)
    run_command("cli_unknown_argument", [sys.executable, module, "--invalid"], 2)
    run_command("cli_missing_output_argument", [sys.executable, module, "--output"], 2)
    run_command("cli_help", [sys.executable, module, "--help"])
    for seed in ("1", "91827"):
        seeded = run_command("cli_demo_hashseed_" + seed, [sys.executable, module], env_extra={"PYTHONHASHSEED": seed})
        require(seeded.stdout == demo.stdout, "serialized output changes with hash seed")
    # Fault injection in a separate interpreter; author's source remains untouched.
    probe = "import memory_model as m; from dataclasses import replace; original=m.transition; m.transition=lambda s,a: (lambda z:(z[0],replace(z[1],current_existence_conviction=None)))(original(s,a)); m.exhaustive_check()"
    for flags, suffix in (([], "normal"), (["-O"], "optimized")):
        detected = run_command("checker_mutation_" + suffix, [sys.executable, *flags, "-c", probe], 1)
        require("conviction/input mismatch" in detected.stderr, "checker did not identify injected defect")
    tests = run_command("author_tests_independent_rerun", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    require("\nOK\n" in tests.stderr, "author tests did not report OK")
    return {"CLI_commands": 13, "checker_fault_injection_detected_normal_and_optimized": True,
            "author_suite_passed": True, "author_test_count": int(re.search(r"Ran (\d+) tests", tests.stderr)[1]),
            "hash_seed_independent_output": True}


def packaged_runner_audit():
    """Rerun the supplied runner in an isolated copy, never overwrite author files."""
    published_record = json.loads((ROOT / "logs/run.json").read_text())
    for name, recorded in published_record["sha256"].items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == recorded,
                f"published source/result hash mismatch: {name}")
    require(all(c["exit_code"] == 0 for c in published_record["commands"]), "published run includes a failure")
    with tempfile.TemporaryDirectory(prefix="runner-copy-", dir=HERE) as tmp:
        sandbox = Path(tmp)
        (sandbox / "tests").mkdir()
        for name in ("memory_model.py", "run_all.py", "tests/test_memory_model.py"):
            shutil.copy2(ROOT / name, sandbox / name)
        run_command("isolated_packaged_runner", [sys.executable, "run_all.py"], cwd=sandbox)
        for name in ("demo.json", "exhaustive.json"):
            require((sandbox / "outputs" / name).read_bytes() == (ROOT / "outputs" / name).read_bytes(),
                    f"isolated runner produced different {name}")
        destination = LOGS / "isolated_runner"
        destination.mkdir(exist_ok=True)
        for path in (sandbox / "logs").glob("*"):
            (destination / path.name).write_text(portable(path.read_text()))
    return {"published_hashes_verified": len(published_record["sha256"]),
            "isolated_runner_exit_code": 0, "deterministic_output_files_matched": 2}


def main():
    OUT.mkdir(exist_ok=True)
    LOGS.mkdir(exist_ok=True)
    files = [ROOT / "memory_model.py", ROOT / "tests/test_memory_model.py", ROOT / "run_all.py", Path(__file__)]
    hashes_before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    environment = {"started_at_utc": datetime.now(timezone.utc).isoformat(), "python_version": sys.version,
                   "optimization_level": sys.flags.optimize,
                   "executable": Path(sys.executable).name, "platform": platform.platform(), "working_directory": portable(os.getcwd()),
                   "dependencies": "Python standard library only", "network_used": False,
                   "argv": [portable(arg) for arg in sys.argv], "source_sha256": hashes_before,
                   "path_note": "Absolute reproduction-root and interpreter paths are normalized to relative paths and executable basename in this public record. All other stdout/stderr content, exit codes, and measured timings are retained."}
    (LOGS / "environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    graph = graph_audit()
    result = {"status": "PASS", "scope": "Independent software verification of a stipulated modern teaching model; not historical or empirical validation.",
              "oracle": "independent integer/bit-mask specification; direct constructor domain and complete reachable graph",
              "graph": graph, "contracts": contract_audit(), "examples": trace_audit(), "mutation_tests": mutation_audit(),
              "CLI_and_author_tests": cli_audit(graph), "packaged_runner": packaged_runner_audit()}
    hashes_after = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    require(hashes_before == hashes_after, "audited files changed during audit; rerun against final files")
    result["source_sha256"] = hashes_after
    (OUT / "audit_summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
