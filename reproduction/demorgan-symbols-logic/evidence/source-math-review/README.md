# Source-math review evidence

Independent audit of the De Morgan source notation and its stated finite-model reconstruction. This script does not import the reproduction's main implementation.

## Run

From this directory, with Python 3 and no third-party dependencies:

```sh
python source_math_review.py
```

The standalone script writes `results.json`. The integrated project command `python run_checks.py` runs this script from the reproduction root and records actual output, command, exit code, and duration in this directory’s `run.log`. It refreshes this directory’s `SHA256SUMS` for the script, results, log, and README, then includes that local manifest in the reproduction-wide manifest. To reproduce these logs and both manifests together, run `python run_checks.py` from the reproduction root.

## Evidence

- `run.log`: successful actual execution, including all count summaries.
- `results.json`: 32 contrary-system forms, their four 8-form categories, all eight failure patterns when empty/full classes are admitted, 36 exemplar forms, the 21 common symbolic triples, and all 48 table-cell comparisons.
- The page-95 table is a manual diplomatic transcription from a 4-times PDF-scale image. The printed final cell is intentionally preserved as `))(.)=(.(`. The script reports that the page-94 elimination rule instead gives `))(.)=).)`; the upper table's corresponding cell and the original letter annotation corroborate this correction.
- Named countermodels check the printed error, selective-quantifier scope, and why giving every object incoming/outgoing edges is insufficient for the page-115 contrary conversion.

## Primary source

[Full primary scan](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf). Printed page + 16 = full-volume PDF page.

- [91: eight forms and existence assumption](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=107)
- [94: validity rule and 32-form classification](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=110)
- [95: complete printed table](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=111)
- [101: exemplar interpretation and 36 forms](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=117)
- [103: 21 common forms](https://archive.org/download/transactionsofca09camb/transactionsofca09camb.pdf#page=119)

## Limits

These runs exhaust assignments in a four-element universe, not arbitrary domains. Passing checks are not a proof of unbounded completeness. General proofs and source/modern-notation distinctions are supplied in the Chinese source audit. The 48-cell test checks consistency with the printed elimination rule; identifying the actual printed marks still depends on inspection of the linked scan.
