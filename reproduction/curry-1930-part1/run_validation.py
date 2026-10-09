"""Regenerate all execution evidence and SHA256SUMS using only the stdlib.

Run: python -B run_validation.py
This executes the trusted notebook and rewrites its saved outputs/logs.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

from curry import (
    Atom, B, I, app, parse, pretty, normalize, dot, AXIOM_ARITIES,
    saturated_axiom_check, cbi_identity_proof, right_identity_proof,
    distribution_proof, associativity_proof, check, proof_nodes, axiom_names_used,
)

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"


def run(name, *args):
    command = [sys.executable, "-B", *args]
    process = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (LOGS / name).write_text("Command: python -B " + " ".join(args) + "\n\n" + process.stdout,
                            encoding="utf-8")
    if process.returncode:
        raise SystemExit(f"FAIL: {' '.join(args)}; see logs/{name}")
    return process.stdout


def main():
    LOGS.mkdir(exist_ok=True)
    unit_log = run("unit-tests.txt", "-m", "unittest", "-v", "test_curry")
    run("worked-demo.txt", "run_demo.py")
    independent_log = run("independent-review.txt", "review_independent.py")
    run("notebook-execution.txt", "execute_notebook.py")
    run("notebook-rerun.txt", "execute_notebook.py", "--check")
    actions = []
    for name, arity in AXIOM_ARITIES.items():
        left, right = saturated_axiom_check(name, arity)
        actions.append({"axiom": name, "symbolic_arity": arity,
                        "left_steps": len(left.steps), "right_steps": len(right.steps),
                        "variable_only_normal_form": pretty(left.end)})
    x, y, z = map(Atom, "xyz")
    proofs = []
    for name, p in (("CBI=I", cbi_identity_proof()),
                    ("BXI=X", right_identity_proof(x)),
                    ("B distributes over dot", distribution_proof(x, y)),
                    ("dot associativity", associativity_proof(x, y, z))):
        lhs, rhs = check(p)
        proofs.append({"claim": name, "left": pretty(lhs), "right": pretty(rhs),
                       "proof_tree_nodes": proof_nodes(p),
                       "finite_axioms_used": sorted(axiom_names_used(p))})
    omega = normalize(parse("W W W"))
    notebook = json.loads((ROOT / "tutorial.ipynb").read_text(encoding="utf-8"))
    result = {
        "source": "Curry 1930 Teil I, American Journal of Mathematics 52(3), 509–536",
        "source_doi": "10.2307/2370619",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "runtime_dependencies": "Python standard library only",
        "unit_tests_passed": int(re.search(r"Ran (\d+) tests", unit_log).group(1)),
        "independent_random_terms": int(re.search(r"(\d+) random depth", independent_log).group(1)),
        "independently_recognized_steps": int(re.search(r"(\d+) emitted steps", independent_log).group(1)),
        "independent_review_seed": int(re.search(r"seed=(\d+)", independent_log).group(1)),
        "notebook_execution": notebook["metadata"]["execution_provenance"],
        "notebook_rerun_matches_saved_outputs": True,
        "finite_axiom_checks": actions,
        "bw_source_policy": "Use unambiguous p.534 left-associated product; p.521 literal-looking discrepancy preserved in test and notebook; no official erratum claimed",
        "equational_certificates": proofs,
        "www": {"status": omega.status, "steps": len(omega.steps),
                "cycle_start": omega.cycle_start, "cycle_length": omega.cycle_length},
        "not_claimed": ["full Q/Π/P/Λ formalization", "original theory consistency or completeness",
                        "general termination or confluence proof", "Part II reproduction",
                        "Jupyter kernel execution", "formal verification of the Python kernel"],
    }
    (ROOT / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    paths = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
    if any("__pycache__" in p.parts or p.suffix == ".pyc" for p in paths):
        raise SystemExit("Release contains Python caches; remove them before creating the manifest")
    hashes = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}" for p in paths]
    (ROOT / "SHA256SUMS").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    print(f"PASS: {result['unit_tests_passed']} tests; 16 symbolic axiom checks; independent review; "
          f"{result['notebook_execution']['code_cells_executed']} notebook code cells and exact output rerun")
    print(f"Evidence saved in logs/, results.json, SHA256SUMS ({len(paths)} files)")


if __name__ == "__main__":
    main()
