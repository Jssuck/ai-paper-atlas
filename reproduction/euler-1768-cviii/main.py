"""Usage: python main.py demo | python main.py check path/to/input.json"""
import argparse
import json
import sys
from experiments import run
from logic import Theory


def check_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")
    required = {"atoms", "premises", "conclusion"}
    permitted = required | {"constraints", "allowed_worlds"}
    if not required <= set(payload):
        raise ValueError("required keys: atoms, premises, conclusion")
    if set(payload) - permitted:
        raise ValueError("unknown input keys: " + ", ".join(sorted(set(payload) - permitted)))
    return Theory(payload["atoms"], payload.get("constraints", []),
                  payload.get("allowed_worlds")).check(
                      payload["premises"], payload["conclusion"])


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("demo", help="run the CVIII teaching experiments")
    check = commands.add_parser("check", help="check a JSON argument")
    check.add_argument("input")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            result = run()
        else:
            with open(args.input, encoding="utf-8") as source:
                payload = json.load(source, object_pairs_hook=unique_object)
            result = check_payload(payload)
    except (ValueError, OSError, RecursionError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0  # invalid arguments are findings, not program failures


if __name__ == "__main__":
    sys.exit(main())
