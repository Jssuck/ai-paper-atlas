# Execution environment

- Runtime requirement: Python 3.10 or later.
- Dependencies: Python standard library only. No virtual environment or package installation is required.
- Recorded runtime: Python 3.12.14 on Linux; exact interpreter and platform details are saved by `run.sh` in `logs/execution.txt`.
- Network use: none.
- Deterministic logical output: all support enumeration, truth values, model counts, and figure contents are deterministic. Timing and environment lines in logs can vary.

The primary outputs are the executable source, tests, JSON/text reports, and SVG figure. `make_figures.py` uses only Python's standard library. A PNG preview is also included; it was rendered using preinstalled Inkscape, as recorded in `logs/render.txt`. An initial ImageMagick attempt could not find its SVG delegate; that failure and the successful Inkscape fallback are both retained in the log. Absolute runtime configuration paths in that log are explicitly redacted; warning text and exit codes are preserved. This optional renderer is not needed to run the model, tests, reports, or SVG generation. No renderer was installed for this task.

To rerun from this directory:

```sh
sh run.sh
```

To render the SVG again only if Inkscape is already available:

```sh
inkscape figures/membership-models.svg --export-type=png --export-filename=figures/membership-models.png
```

`run.sh` does not invoke that optional external renderer. It creates files only under this reproduction directory. Set `PYTHON` to use a different available interpreter, for example `PYTHON=python3.12 sh run.sh`.
