#!/usr/bin/env python3
"""Run and record the independent audit without changing production artifacts."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "review"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
CORE = ("euler_cv.py", "test_euler_cv.py", "make_figures.py", "run.sh",
        "logs/report.json", "logs/report.txt", "figures/membership-models.svg",
        "figures/membership-models.png")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_svg():
    root = ET.parse(ROOT / "figures/membership-models.svg").getroot()
    ns = {"s": "http://www.w3.org/2000/svg"}
    circles = root.findall("s:circle", ns)
    actual = {(float(item.attrib["cx"]), float(item.attrib["cy"])):
              item.attrib["fill"] != "#ffffff" for item in circles}
    # Literal table transcribed from the mathematical specification, not from code.
    panels = (
        (48, 168, 452, ((False, True, True), (False, False, True), (True, False, False))),
        (524, 168, 452, ((False, True, True), (True, False, True))),
        (1000, 168, 452, ((False, True, True), (True, False, True), (False, False, True))),
        (48, 681, 690, ((True, True, False), (True, False, True))),
        (762, 681, 690, ((True, True, False), (False, False, True))),
    )
    expected = {}
    for x, y, width, rows in panels:
        for row, memberships in enumerate(rows):
            for fraction, present in zip((0.48, 0.66, 0.84), memberships):
                expected[(x + width * fraction, y + 151 + 46 * row)] = present
    assert len(circles) == 36 and len(actual) == 36
    assert actual == expected
    assert root.attrib["width"] == "1500" and root.attrib["height"] == "1100"
    return "PASS: SVG XML valid; all 36 membership dots match an independent literal table; canvas 1500 x 1100."


def main():
    before = {name: digest(ROOT / name) for name in CORE}
    with (REVIEW / "execution.txt").open("w", encoding="utf-8") as log:
        def emit(message):
            print(message, file=log, flush=True)
        def run(command, cwd, label=None):
            emit("\n$ " + (label or " ".join(command)))
            started = time.perf_counter()
            result = subprocess.run(command, cwd=cwd, env=ENV, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True)
            emit(result.stdout.rstrip())
            emit(f"exit_code={result.returncode}; elapsed_seconds={time.perf_counter() - started:.3f}")
            if result.returncode:
                raise RuntimeError("Audit command failed; see review/execution.txt")
            return result.stdout
        emit("Independent Euler Letter CV audit")
        emit("started_utc=" + datetime.now(timezone.utc).isoformat())
        emit("working_directory=reproduction/euler-1768-cv (release-relative)")
        emit("interpreter=" + sys.version.replace("\n", " "))
        emit("platform=" + platform.platform())
        emit("network_calls=none; package_installations=none")
        unit = run(["python3", "-m", "unittest", "-v", "test_euler_cv.py"], ROOT)
        (REVIEW / "unit-tests.txt").write_text(unit, encoding="utf-8")
        oracle = run(["python3", "review/independent_check.py"], ROOT)
        (REVIEW / "independent-results.json").write_text(oracle, encoding="utf-8")
        # Stage only declared program inputs. No generated report or figure is copied.
        with tempfile.TemporaryDirectory(prefix="euler-cv-audit-") as temporary:
            target = Path(temporary)
            for name in ("euler_cv.py", "test_euler_cv.py", "make_figures.py", "run.sh"):
                shutil.copy2(ROOT / name, target / name)
            run(["sh", "run.sh"], target, "sh run.sh  [isolated copy of the four declared input files]")
            for name in ("logs/report.json", "logs/report.txt", "figures/membership-models.svg"):
                assert (target / name).read_bytes() == (ROOT / name).read_bytes(), name
            emit("PASS: regenerated JSON report, text report, and SVG equal delivered files byte for byte.")
        emit("\n" + verify_svg())
        assert before == {name: digest(ROOT / name) for name in CORE}
        emit("PASS: audited production source, script, reports, SVG and PNG remained unchanged.")
        emit("finished_utc=" + datetime.now(timezone.utc).isoformat())
        emit("AUDIT_STATUS=PASS")
    (REVIEW / "input-sha256.json").write_text(json.dumps(before, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS: audit saved in review/execution.txt; independent-results.json; unit-tests.txt; input-sha256.json")


if __name__ == "__main__":
    main()
