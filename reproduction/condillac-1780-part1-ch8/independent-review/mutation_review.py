"""Independent semantic mutations and negative controls, with strict outcomes.

Temporary copies only. Syntax/import/runtime exceptions and timeouts are harness
failures, never successful detection. Uses review_model.py, not author tests.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent / "model.py"
REVIEW = HERE / "review_model.py"
FLAGS = ["-" + "O" * sys.flags.optimize] if sys.flags.optimize else []
MUTATIONS = (
    ("mere_lack_as_deprivation", "return self.lacking and self.known and (self.habitual_enjoyment or self.habitual_imagination)", "return self.lacking"),
    ("require_both_pleasure_histories", "return self.lacking and self.known and (self.habitual_enjoyment or self.habitual_imagination)", "return self.lacking and self.known and (self.habitual_enjoyment and self.habitual_imagination)"),
    ("deny_imagined_pleasure_path", "return self.lacking and self.known and (self.habitual_enjoyment or self.habitual_imagination)", "return self.lacking and self.known and self.habitual_enjoyment"),
    ("allow_unknown_pleasure_object", "if (self.habitual_enjoyment or self.habitual_imagination) and not self.known:", "if False:"),
    ("erase_need_stipulation", "return self.deprivation", "return False"),
    ("ignore_faculty_direction", "return self.need and self.faculties_directed", "return self.need"),
    ("desire_from_direction_alone", "return self.need and self.faculties_directed", "return self.faculties_directed"),
    ("erase_latent_passion", "return self.desire_habit", "return self.desire_habit and self.desire"),
    ("enjoyment_habit_is_passion", "return self.desire_habit", "return self.habitual_enjoyment"),
    ("activate_all_dispositions", "return self.passion_disposition and self.desire", "return self.passion_disposition"),
    ("existential_judgment", "return all(getattr(w, predicate) for w in self.worlds if w.name in self.support)", "return any(getattr(w, predicate) for w in self.worlds if w.name in self.support)"),
    ("judge_entire_universe", "return all(getattr(w, predicate) for w in self.worlds if w.name in self.support)", "return all(getattr(w, predicate) for w in self.worlds)"),
    ("inject_actual_into_support", "return all(getattr(w, predicate) for w in self.worlds if w.name in self.support)", "return all(getattr(w, predicate) for w in self.worlds if w.name in self.support or w.name == self.actual)"),
    ("actuality_from_first_world", "return getattr(next(w for w in self.worlds if w.name == self.actual), predicate)", "return getattr(self.worlds[0], predicate)"),
    ("claim_actual_always_supported", "return self.actual in self.support", "return True"),
    ("hope_without_desire", '"hope": affect.desire and obtain_judgment,', '"hope": obtain_judgment,'),
    ("hope_from_actuality", '"hope": affect.desire and obtain_judgment,', '"hope": affect.desire and beliefs.actually("obtains"),'),
    ("ignore_experience_origin", "return self.established and self.from_experience", "return self.established"),
    ("ignore_established_habit", "return self.established and self.from_experience", "return self.from_experience"),
    ("will_ignores_current_judgment", '"narrow_will": affect.desire and habit.experience_backed and obstacle_judgment,', '"narrow_will": affect.desire and habit.experience_backed,'),
    ("will_requires_hope_without_bridge", '"narrow_will": affect.desire and habit.experience_backed and obstacle_judgment,', '"narrow_will": affect.desire and habit.experience_backed and obstacle_judgment and obtain_judgment,'),
    ("identify_obstacles_with_attainment", 'obstacle_judgment = beliefs.judges("obstacle_free")', 'obstacle_judgment = beliefs.judges("obtains")'),
    ("reverse_bridge", "return all((not w.obstacle_free) or w.obtains for w in self.worlds if w.name in self.support)", "return all((not w.obtains) or w.obstacle_free for w in self.worlds if w.name in self.support)"),
    ("allow_empty_support", "if not self.support:", "if False:"),
    ("allow_duplicate_world_names", "if not names or len(names) != len(set(names)):", "if not names:"),
    ("allow_evidence_expansion", "if not retained.issubset(self.support):", "if False:"),
    ("ignore_evidence_restriction", "return Beliefs(self.worlds, retained, self.actual)", "return Beliefs(self.worlds, self.support, self.actual)"),
    ("truthiness_instead_of_bool_contract", "if type(value) is not bool:", "if False:"),
)


def run_review(target, timeout=90):
    try:
        run = subprocess.run([sys.executable, *FLAGS, "-B", str(REVIEW), str(target)],
                             text=True, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"status": "harness_failure", "exception": type(error).__name__}
    try:
        report = json.loads(run.stdout)
    except (ValueError, TypeError):
        return {"status": "harness_failure", "exit_code": run.returncode,
                "reason": "missing or invalid structured verifier output"}
    if not isinstance(report, dict) or report.get("optimization") != sys.flags.optimize:
        return {"status": "harness_failure", "exit_code": run.returncode,
                "reason": "invalid report or optimization mismatch"}
    if run.returncode == 0 and report.get("status") == "PASS":
        status = "survived"
    elif run.returncode == 1 and report.get("status") == "SEMANTIC_FAILURE":
        status = "detected_by_behavior"
    else:
        status = "harness_failure"
    return {"status": status, "exit_code": run.returncode, "verifier_report": report}


def main():
    source_bytes = MODEL.read_bytes()
    source = source_bytes.decode("utf-8")
    baseline = run_review(MODEL)
    if baseline["status"] != "survived":
        print(json.dumps({"status": "HARNESS_FAILURE", "baseline": baseline}, indent=2))
        return 2

    def run_mutant(mutation):
        name, before, after = mutation
        if source.count(before) != 1:
            return {"name": name, "status": "harness_failure", "reason": "mutation site not unique"}
        with tempfile.TemporaryDirectory(prefix=".mutation-", dir=HERE) as folder:
            target = Path(folder) / "model.py"
            target.write_text(source.replace(before, after), encoding="utf-8")
            return {"name": name, **run_review(target)}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run_mutant, MUTATIONS))
    controls = []
    controls_source = (
        ("syntax_error", "def broken(:\n", 90),
        ("import_exception", "raise RuntimeError('deliberate import failure')\n", 90),
        ("runtime_exception", source.replace('obtain_judgment = beliefs.judges("obtains")',
                                            'raise RuntimeError("deliberate runtime failure")'), 90),
        ("timeout", "import time\ntime.sleep(60)\n", 0.5),
    )
    for name, contents, timeout in controls_source:
        with tempfile.TemporaryDirectory(prefix=".control-", dir=HERE) as folder:
            target = Path(folder) / "model.py"
            target.write_text(contents, encoding="utf-8")
            controls.append({"name": name, **run_review(target, timeout=timeout)})
    detected = sum(row["status"] == "detected_by_behavior" for row in results)
    controls_ok = all(row["status"] == "harness_failure" for row in controls)
    unchanged = MODEL.read_bytes() == source_bytes
    success = detected == len(MUTATIONS) and controls_ok and unchanged
    report = {
        "status": "PASS" if success else "FAIL", "optimization": sys.flags.optimize,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "review_script_sha256": hashlib.sha256(REVIEW.read_bytes()).hexdigest(),
        "mutation_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "baseline": baseline, "results": results, "detected": detected, "total": len(MUTATIONS),
        "negative_controls": controls, "controls_correctly_classified": controls_ok,
        "production_source_unchanged": unchanged,
        "scope": "These specified semantic mutants only; exceptions, syntax/import errors, timeouts and unknown exits never count as detection.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
