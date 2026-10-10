"""Run tests, record this environment, and regenerate the portable experiment."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone

from euler_semantics import FORMS, Mode, canonical_model, counterexample, representatives


ROOT = Path(__file__).resolve().parent


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def experiment():
    modes = {}
    for mode in Mode:
        models = representatives(mode)
        matrix = {}
        for premise in FORMS:
            matrix[premise] = {}
            for conclusion in FORMS:
                witness = counterexample([premise], conclusion, mode)
                matrix[premise][conclusion] = {
                    "valid": witness is None,
                    "counterexample": None if witness is None else witness.as_dict(),
                }
        patterns = {}
        for model in models:
            key = "".join(form for form in FORMS if model.truth()[form])
            patterns[key] = patterns.get(key, 0) + 1
        modes[mode.value] = {
            "representative_count": len(models),
            "true_counts": {f: sum(m.truth()[f] for m in models) for f in FORMS},
            "joint_truth_pattern_counts": dict(sorted(patterns.items())),
            "strict_overlap_count": sum(all(m.atoms()[i] for i in range(3)) for m in models),
            "implication_matrix": matrix,
            "models": [m.as_dict() for m in models],
        }
    examples = {
        "equality_A_and_I": canonical_model(1).as_dict(),
        "proper_subset_A_and_I": canonical_model(5).as_dict(),
        "disjoint_E_and_O": canonical_model(6).as_dict(),
        "strict_overlap_I_and_O": canonical_model(7).as_dict(),
        "proper_superset_I_and_O": canonical_model(3).as_dict(),
        "empty_subject_A_and_E": canonical_model(4).as_dict(),
        "empty_predicate_E_and_O": canonical_model(2).as_dict(),
    }
    return {
        "scope": "Modern nonempty-universe two-term A/E/I/O semantics; not Euler's full logic.",
        "atom_bit_order": ["S intersection P", "S minus P", "P minus S", "U minus (S union P)"],
        "max_canonical_universe_size": 4,
        "modes": modes,
        "examples": examples,
    }


def svg():
    # Original vector artwork.  Three dots denote the only domain members.
    return '''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="500" viewBox="0 0 900 500" role="img" aria-labelledby="title desc">
<title id="title">严格交叠：同时满足 I 和 O 的一个模型</title>
<desc id="desc">非空论域只有三个点。S={0,1}，P={0,2}。交集有0，S独有区有1，P独有区有2。因此I与O真，A与E假。这只是I与O的一种模型。</desc>
<rect width="900" height="500" fill="#f8fafc"/>
<g font-family="Noto Sans CJK SC,DejaVu Sans,sans-serif" fill="#152238">
<text x="44" y="43" font-size="24" font-weight="bold">严格交叠：I 与 O 同时为真</text>
<text x="44" y="74" font-size="16">现代有限模型示意，非原书摹图；论域只含三个标出的点</text>
<rect x="40" y="98" width="820" height="318" rx="12" fill="white" stroke="#aab7c9" stroke-width="2"/>
<text x="65" y="126" font-size="17">U = {0, 1, 2}</text>
<circle cx="335" cy="255" r="130" fill="#2876cd" fill-opacity="0.12" stroke="#236ab5" stroke-width="3"/>
<circle cx="465" cy="255" r="130" fill="#c07122" fill-opacity="0.12" stroke="#ab5910" stroke-width="3"/>
<text x="257" y="172" fill="#174f8c" font-size="23">S</text>
<text x="523" y="172" fill="#894309" font-size="23">P</text>
<circle cx="266" cy="254" r="6" fill="#152238"/>
<circle cx="400" cy="254" r="6" fill="#152238"/>
<circle cx="534" cy="254" r="6" fill="#152238"/>
<text x="246" y="284" font-size="18">1</text>
<text x="391" y="284" font-size="18">0</text>
<text x="529" y="284" font-size="18">2</text>
<text x="225" y="321" font-size="17">S 独有</text>
<text x="373" y="321" font-size="17">交集</text>
<text x="504" y="321" font-size="17">P 独有</text>
<text x="662" y="213" font-size="20">A 假　E 假</text>
<text x="662" y="248" font-size="20" fill="#176947">I 真　O 真</text>
<text x="662" y="293" font-size="16">S = {0, 1}</text>
<text x="662" y="321" font-size="16">P = {0, 2}</text>
<text x="44" y="451" font-size="17">I 只要求交集非空；O 只要求 S 独有区非空。</text>
<text x="44" y="480" font-size="17">P 独有区非空是这张图的额外条件，并非 I、O 的共同要求。</text>
</g></svg>\n'''


def main():
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "logs").mkdir(exist_ok=True)
    # Use the same interpreter, but record a portable invocation without exposing
    # the host's private absolute executable or workspace paths.
    command = [Path(sys.executable).name, "-m", "unittest", "discover", "-s", "tests", "-v"]
    started = datetime.now(timezone.utc).isoformat()
    result = subprocess.run(command, executable=sys.executable, cwd=ROOT,
                            text=True, capture_output=True, check=False)
    test_log = "$ " + " ".join(command) + "\n" + result.stdout + result.stderr
    test_log += f"\nexit_code={result.returncode}\n"
    (ROOT / "logs" / "tests.log").write_text(test_log, encoding="utf-8")
    environment = {
        "started_at_utc": started,
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "executable": Path(sys.executable).name,
        "platform": platform.platform(),
        "working_directory": ".",
        "run_command": "python3 run.py",
        "test_command": command,
        "test_exit_code": result.returncode,
        "third_party_runtime_dependencies": [],
    }
    write_json(ROOT / "results" / "environment.json", environment)
    print(test_log, end="")
    if result.returncode:
        print("Tests failed; experiment outputs were not regenerated.")
        return result.returncode
    results = experiment()
    write_json(ROOT / "results" / "results.json", results)
    with (ROOT / "results" / "models.csv").open("w", encoding="utf-8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["mode", "mask", "both", "s_only", "p_only", "outside", "U", "S", "P", *FORMS])
        for mode in Mode:
            for model in representatives(mode):
                writer.writerow([mode.value, model.occupancy(), *map(int, map(bool, model.atoms())),
                                 json.dumps(sorted(model.universe)), json.dumps(sorted(model.subject)),
                                 json.dumps(sorted(model.predicate)), *map(int, model.truth().values())])
    (ROOT / "results" / "strict-overlap.svg").write_text(svg(), encoding="utf-8")
    lines = ["Euler CII: modern finite-set experiment", "Universe is nonempty in both modes."]
    for mode, data in results["modes"].items():
        lines += [f"{mode}: {data['representative_count']} occupancy patterns",
                  "  true counts: " + ", ".join(f"{f}={v}" for f, v in data["true_counts"].items()),
                  "  joint truth patterns: " + json.dumps(data["joint_truth_pattern_counts"]),
                  f"  strict-overlap patterns: {data['strict_overlap_count']}"]
        valid = [f"{p}=>{q}" for p in FORMS for q in FORMS
                 if p != q and data["implication_matrix"][p][q]["valid"]]
        lines.append("  non-reflexive single-premise implications: " + (", ".join(valid) or "none"))
    lines += ["Exhaustive labeled cross-check in tests: sizes 1..4, 340 models; 284 have both terms nonempty.",
              "Consequence checks: 16 premise subsets x 4 conclusions x 2 modes = 128 queries.",
              "Bound: at most four elements suffice for these occupancy-invariant two-term formulas.",
              "NOT a reconstruction or completeness claim about Euler's historical logic."]
    summary = "\n".join(lines) + "\n"
    (ROOT / "results" / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
