"""Verify the reviewed content snapshot without changing any files."""

from hashlib import sha256
import json
from pathlib import Path


def main():
    location = Path(__file__).resolve()
    root = location.parents[3]
    record = json.loads(location.with_name("bindings.json").read_text(encoding="utf-8"))
    for name, expected in record["sha256"].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root) or sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Reviewed snapshot mismatch: {name}")
    print(f"PASS: {len(record['sha256'])} reviewed file hashes match")


if __name__ == "__main__":
    main()
