#!/usr/bin/env python3
"""Small, offline teaching driver. JSON, human-readable text, and CSV outputs."""
import argparse
import csv
import io
import json
from itertools import product

from categorical import (KINDS, MODES, ORIGINAL_ROUTES, Model, all_forms,
                         models, nonproductive_witnesses)


def build_report():
    results = {(mode, reverse): all_forms(mode=mode, reverse=reverse)
               for mode in MODES for reverse in (False, True)}
    table = []
    for major, minor in product(KINDS, repeat=2):
        pair = major + minor
        row = {"pair": pair, "original_strongest": ORIGINAL_ROUTES.get(pair, "")}
        for mode in MODES:
            for reverse in (False, True):
                direction = "reverse" if reverse else "forward"
                row[mode + "_" + direction] = "".join(
                    result.form[-1] for result in results[mode, reverse]
                    if result.form[:2] == pair and result.valid)
        table.append(row)
    example = Model((1, 6))
    return {
        "scope": "Prior Analytics I.4; modern teaching reconstruction, not author algorithm",
        "encoding": {"P": 4, "M": 2, "S": 1, "bits": "PMS"},
        "premises": ["major(M,P)", "minor(S,M)"],
        "forward_conclusion": "conclusion(S,P)",
        "reverse_conclusion": "conclusion(P,S); separate diagnostic only",
        "model_counts": {mode: len(models(mode)) for mode in MODES},
        "original_strongest_routes": ORIGINAL_ROUTES,
        "valid_forms": {mode: [r.form for r in results[mode, False] if r.valid]
                        for mode in MODES},
        "valid_reverse_forms": {mode: [r.form for r in results[mode, True] if r.valid]
                                for mode in MODES},
        "premise_pair_table": table,
        "forms": {mode: [r.as_dict() for r in results[mode, False]] for mode in MODES},
        "reverse_forms": {mode: [r.as_dict() for r in results[mode, True]] for mode in MODES},
        "nonproductive_witnesses": {mode: nonproductive_witnesses(mode=mode)
                                    for mode in MODES},
        "direction_example_IE": {
            "model": example.as_dict(),
            "I_MP": example.holds("I", "M", "P"),
            "E_SM": example.holds("E", "S", "M"),
            "O_PS": example.holds("O", "P", "S"),
            "I_SP": example.holds("I", "S", "P"),
        },
    }


def human_report(report):
    lines = [
        "《前分析篇》I.4：现代集合语义教学复现（非作者算法）",
        "固定前提：大前提(M,P)，小前提(S,M)；正向结论(S,P)。",
        "PMS 位编码：P=4，M=2，S=1；论域始终非空。",
        "原章四条最强路线：AA→A、EA→E、AI→I、EI→O。",
    ]
    for mode in MODES:
        lines.append(f"{mode}: {report['model_counts'][mode]} 个规范支撑；"
                     f"有效正向形式 {', '.join(report['valid_forms'][mode])}")
    lines += ["", "前提对 | 原章最强结论 | 允许空项 | 三项非空 | 反向允许空项 | 反向三项非空"]
    for row in report["premise_pair_table"]:
        lines.append(" | ".join(str(row[key]) or "无" for key in (
            "pair", "original_strongest", "empty-allowed_forward",
            "all-nonempty_forward", "empty-allowed_reverse", "all-nonempty_reverse")))
    lines += ["", "12 组非生产前提对（以下见证均令 P、M、S 非空）：",
              "A 见证使 S⊆P；E 见证使 S∩P=∅。因 S 非空，二者可排除全部四种必然结论。"]
    for row in report["nonproductive_witnesses"]["all-nonempty"]:
        lines.append(f"{row['pair']}: A 支撑={row['A_SP_witness']['support']}; "
                     f"E 支撑={row['E_SP_witness']['support']}")
    lines += ["", "IE 的反向诊断：I(M,P) 与 E(S,M) 可推出 O(P,S)。",
              "这不属于固定为 (S,P) 的正向结论；I(S,P) 也不随之成立。",
              "规范支撑穷举须结合文档中的压缩论证；有限检查本身不是任意论域证明。",
              "运行 --format json 可查每个无效形式的最小反模型及全部反向结果。"]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("human", "json", "pairs-csv", "forms-csv"),
                        default="human")
    args = parser.parse_args()
    report = build_report()
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    elif args.format == "human":
        print(human_report(report), end="")
    else:
        if args.format == "pairs-csv":
            rows = report["premise_pair_table"]
        else:
            rows = []
            for mode in MODES:
                for result in report["forms"][mode]:
                    rows.append({**{k: v for k, v in result.items() if k != "minimal_countermodel"},
                                 "minimal_countermodel": json.dumps(result["minimal_countermodel"],
                                                                     sort_keys=True)})
        output = io.StringIO(newline="")
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        print(output.getvalue(), end="")


if __name__ == "__main__":
    main()
