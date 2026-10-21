# Verification record

Completed (UTC): 2026-10-21T11:50:08.578759+00:00

These are actual subprocess runs, not inferred results. Full stdout/stderr, commands, exit codes and timings are retained in `logs/`. Commands use portable `python3` spellings and relative working directories instead of private local paths. Environment and file hashes are recorded in `logs/environment.json` and `logs/verification.json`.

Report generation exit code: **0**.

| Mode | Observed optimization | Tests | Exit | Result |
|---|---:|---:|---:|---|
| normal | 0 | 41 | 0 | PASS |
| optimized | 1 | 41 | 0 | PASS |
| double-optimized | 2 | 41 | 0 | PASS |

## Coverage and limits

The suite independently checks all 192 mood-policy cases, all 176 invalid-case witnesses and their cardinality minimality, all 9,180 atomic clause evaluations, all 255 support realizations, and compression for all 584 labeled models with domain sizes one through three. It also checks reversal, vacuity, strict input validation, deterministic reports and CLI behavior.

Passing finite tests is not by itself a proof over arbitrary universes, nor a historical validation. The support-preservation argument is given separately in WALKTHROUGH.md. The three modes run the same test suite, not three independent implementations. The set-based oracle is independent of the production atom evaluator but belongs to the same authored package.
