"""Verify frozen review hashes and exact streams inside the compact audit logs."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_log(path):
    data = path.read_bytes()
    cursor = 0
    blocks = []
    while cursor < len(data):
        end = data.index(b"\n", cursor)
        header = data[cursor:end]
        require(header.startswith(b"=== COMMAND ") and header.endswith(b" ==="), "invalid command delimiter")
        record = json.loads(header[len(b"=== COMMAND "):-len(b" ===")])
        cursor = end + 1
        stdout_marker = f"--- STDOUT ({record['stdout_bytes']} bytes) ---\n".encode()
        require(data[cursor:cursor+len(stdout_marker)] == stdout_marker, "invalid stdout delimiter")
        cursor += len(stdout_marker)
        stdout = data[cursor:cursor+record["stdout_bytes"]]
        cursor += record["stdout_bytes"]
        stderr_marker = f"\n--- STDERR ({record['stderr_bytes']} bytes) ---\n".encode()
        require(data[cursor:cursor+len(stderr_marker)] == stderr_marker, "invalid stderr delimiter")
        cursor += len(stderr_marker)
        stderr = data[cursor:cursor+record["stderr_bytes"]]
        cursor += record["stderr_bytes"]
        tail = b"\n=== END COMMAND ===\n\n"
        require(data[cursor:cursor+len(tail)] == tail, "invalid end delimiter")
        cursor += len(tail)
        blocks.append((record, stdout, stderr))
    return blocks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--current-run-only", action="store_true",
                        help="After a rerun, check frozen reviewed inputs and current command streams, not old evidence hashes")
    args = parser.parse_args()
    binding = json.loads((ROOT / "audit/code_review.json").read_text())
    checked_files = 0
    sections = ("reviewed_inputs",) if args.current_run_only else ("reviewed_inputs", "evidence_files")
    for section in sections:
        for record in binding[section]:
            data = (ROOT / record["path"]).read_bytes()
            require(len(data) == record["bytes"], f"review size mismatch: {record['path']}")
            require(sha(data) == record["sha256"], f"review hash mismatch: {record['path']}")
            checked_files += 1
    report = json.loads((ROOT / "audit/execution_report.json").read_text())
    require(report["success"] is True, "audit run did not pass")
    logs = {mode: read_log(ROOT / "audit/logs" / f"{mode}.log") for mode in ("normal", "O", "OO")}
    for record in report["commands"]:
        header, stdout, stderr = logs[record["mode"]][record["log_block"] - 1]
        for key in ("name", "mode", "command", "cwd", "environment_overrides", "exit_code", "expected_exit_code", "stdout_bytes", "stderr_bytes"):
            require(header[key] == record[key], f"command metadata mismatch: {record['name']}/{key}")
        require(sha(stdout) == record["stdout_sha256"], "stdout hash mismatch")
        require(sha(stderr) == record["stderr_sha256"], "stderr hash mismatch")
        require(record["exit_code"] == record["expected_exit_code"], "unexpected command exit")
    require(sum(len(v) for v in logs.values()) == len(report["commands"]) == 54, "command count mismatch")
    print(json.dumps({"status": "passed", "verification_mode": "current_run" if args.current_run_only else "frozen_delivery",
                      "bound_files_verified": checked_files,
                      "exact_command_streams_verified": 54, "compact_logs": 3}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
