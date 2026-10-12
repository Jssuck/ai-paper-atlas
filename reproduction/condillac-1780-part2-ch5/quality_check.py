"""Source-level Markdown table, link, math-style, and Python-assert audit."""
import ast
import json
from pathlib import Path
import re
from semantic_probes import check


def cells(line):
    # An unescaped pipe is a delimiter; a backslash-escaped pipe belongs to a cell.
    parts, current = [], []
    backslashes = 0
    for char in line:
        if char == "|" and backslashes % 2 == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        backslashes = backslashes + 1 if char == "\\" else 0
    parts.append("".join(current).strip())
    check(parts[0] == "" and parts[-1] == "", "table row must have explicit outer delimiters")
    return parts[1:-1]


def run():
    root = Path(__file__).parent
    tables, docs = [], []
    for path in sorted(root.glob("*.md")):
        source = path.read_text(encoding="utf-8")
        check("\\operatorname" not in source and "\\phantom" not in source, "forbidden math macro")
        check(not re.search(r"</[A-Za-z]", source), "raw closing HTML tag")
        fence, expected, table = None, None, None
        for number, line in enumerate(source.splitlines(), 1):
            if line.startswith("```"):
                fence = None if fence is not None else line[3:]
                continue
            if fence is not None:
                continue
            if line.startswith("|"):
                values = cells(line)
                if expected is None:
                    expected = len(values)
                    table = {"file": path.name, "start_line": number, "columns": expected, "rows": []}
                    tables.append(table)
                check(len(values) == expected, f"table cell count mismatch at {path.name}:{number}")
                table["rows"].append({"line": number, "cells": len(values)})
            else:
                expected = None
            stripped = re.sub(r"\$`[^`\n]*`\$", "", line)
            check("$" not in stripped, f"non-GitHub inline math delimiters at {path.name}:{number}")
        check(fence is None, f"unclosed fenced block in {path.name}")
        for link in re.findall(r"\]\(([^)]+)\)", source):
            if "://" not in link and not link.startswith("#"):
                check((root / link.split("#", 1)[0]).exists(), f"missing local link: {path.name}: {link}")
        docs.append(path.name)
    python_files = []
    for path in sorted(root.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        check(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)), f"assert statement in {path.name}")
        python_files.append(path.name)
    return {"status": "passed", "markdown_files": docs, "source_tables": tables,
            "python_files_without_assert_statements": python_files,
            "boundary": "Source-level checks only; no claim of rendered Markdown or image inspection."}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
