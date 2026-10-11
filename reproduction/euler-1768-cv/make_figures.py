#!/usr/bin/env python3
"""Draw a new SVG membership diagram from the verified teaching models.

All drawing is generated with Python's standard library. Filled dots show
membership and open circles show nonmembership; there are no assumed regions.
"""

from html import escape
from pathlib import Path

from euler_cv import named_examples


COLORS = {"A": "#087f8c", "B": "#7556a0", "C": "#bd6424"}
parts = []


def text(x, y, content, size=22, fill="#203544", weight="normal"):
    parts.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(content)}</text>')


def rect(x, y, width, height, fill, stroke="none", radius=14):
    parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')


def card(x, y, width, title, subtitle, model, row_order, footer, witness):
    rect(x, y, width, 340, "#ffffff", "#d3dfe3")
    text(x + 24, y + 42, title, 25, weight="bold")
    text(x + 24, y + 77, subtitle, 18, "#526b79")
    text(x + 30, y + 120, "Object", 18, "#526b79")
    columns = [x + width * fraction for fraction in (0.48, 0.66, 0.84)]
    for name, column in zip(("A", "B", "C"), columns):
        text(column - 9, y + 120, name, 22, COLORS[name], "bold")
    for index, element in enumerate(row_order):
        row_y = y + 153 + index * 46
        if element == witness:
            rect(x + 16, row_y - 22, width - 32, 39, "#fff4ce", radius=8)
        text(x + 36, row_y + 6, element, 23, weight="bold" if element == witness else "normal")
        for name, column in zip(("A", "B", "C"), columns):
            present = element in model.term(name)
            fill = COLORS[name] if present else "#ffffff"
            stroke = COLORS[name] if present else "#aabac2"
            parts.append(f'<circle cx="{column}" cy="{row_y - 2}" r="9" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    text(x + 24, y + 305, footer, 18)


def main():
    examples = named_examples()
    parts.clear()
    parts.extend([
        '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1100" viewBox="0 0 1500 1100" role="img" aria-labelledby="title desc">',
        '<title id="title">Same witnesses, different conclusions: five finite membership models</title>',
        '<desc id="desc">The top three models satisfy E(A,B), I(B,C), and O(C,A), while C minus B is outside A, inside A, or partly inside A. The bottom two models both satisfy I(A,B) and E(B,C), but O(C,A) is false in the left model and true in the right. Filled dots show membership; open circles show nonmembership. Highlighted rows are the existential premise witnesses.</desc>',
    ])
    rect(0, 0, 1500, 1100, "#eef4f5", radius=0)
    text(48, 60, "Follow the same witness", 37, weight="bold")
    text(48, 99, "Three models of E(A,B) and I(B,C). In each, w proves O(C,A).", 23)
    text(48, 137, "Filled dot = member    Open circle = not a member    Highlight = premise witness", 20, "#526b79")
    for x, suffix, title, subtitle, rows, footer in (
        (48, "disjoint_A", "Remainder outside A", "C minus B = {r}", ("w", "r", "a"), "w is in B and C, but outside A."),
        (524, "subset_A", "Remainder inside A", "C minus B = {r}", ("w", "r"), "w is in B and C, but outside A."),
        (1000, "mixed_A", "Mixed remainder", "C minus B = {q, r}", ("w", "r", "q"), "w is in B and C, but outside A."),
    ):
        card(x, 168, 452, title, subtitle, examples[f"valid_remainder_{suffix}"], rows, footer, "w")
    text(48, 548, "These are possible models. A remainder, or an extra outside object, need not exist.", 22, "#526b79")
    text(48, 611, "Same premises, opposite outcomes", 32, weight="bold")
    text(48, 650, "Both models satisfy I(A,B) and E(B,C). The proposed O(C,A) is not guaranteed.", 23)
    card(48, 681, 690, "Countermodel: O(C,A) is false", "U = {s, v}; all three classes are nonempty", examples["invalid_countermodel_nonempty"], ("s", "v"), "Every C is A. The conclusion has no witness.", "s")
    card(762, 681, 690, "Alternative: O(C,A) is true", "U = {s, v}; all three classes are nonempty", examples["invalid_true_conclusion_alternative"], ("s", "v"), "v is a C outside A, so it witnesses the conclusion.", "s")
    text(48, 1065, "Original teaching diagram for Euler, Letter CV (1768 edition, pp. 119–126); modern finite-set models.", 19, "#526b79")
    parts.append("</svg>")
    destination = Path(__file__).parent / "figures" / "membership-models.svg"
    destination.parent.mkdir(exist_ok=True)
    destination.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("Wrote figures/membership-models.svg (original; generated from named_examples()).")


if __name__ == "__main__":
    main()
