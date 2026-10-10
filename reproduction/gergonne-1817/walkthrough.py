"""中文教学导览：python walkthrough.py；只使用 Python 标准库。"""

from gergonne import (
    FIGURES, MODERN_FIGURE, LETTERS, Literal, Model, Mood, conversion_targets,
    countermodel, models, relation_triple, valid_moods,
)
from reproduce import example_record, reductions_record


def main():
    print("1. 把一个对象的 P/M/G 归属写成三位码")
    for atom in range(1, 8):
        belonging = [name for name, bit in zip(("P", "M", "G"), (1, 2, 4)) if atom & bit]
        print(f"  原子 {atom}: {','.join(belonging)}")
    print("每个非空原子保留一个代表；忽略三个类之外的对象。")
    print("128 种占用模式中，P/M/G 都非空的模式数：", len(models()))
    print("\n2. 五种精确关系投影成 54 个三元组")
    print("固定顺序：(M,G),(P,M),(P,G)；D 是原文反向 C 的现代 ASCII 别名。")
    print("不同三元组数：", len({relation_triple(m) for m in models()}))
    print("\n3. 四种命题与换位")
    print("A=所有第一类都是第二类；N=全不；a=有些是；n=有些不是。")
    for k in LETTERS:
        print(f"  {k}(P,G) 可推出的反向命题种类：{conversion_targets(k)}")
    print("\n4. 必须保留作者的 figure 编号")
    for f, directions in FIGURES.items():
        print(f"  原文 {f}：{directions}；对应现代 {MODERN_FIGURE[f]}")
    print("\n5. 原文 §§51–52 的对照例")
    for section, figure in ((51, 2), (52, 4)):
        ex = example_record(figure, "A", "N")
        print(f"  §{section}：{ex['premises']}")
        print("   关系对", ex["relation_pairs"], "；结论关系", ex["possible_conclusion_relations"])
        print("   可推出", ex["entailed_conclusion_kinds"])
    print("\n6. 对 256 种候选逐一找反例")
    print("有效数：", len(valid_moods()))
    for f in FIGURES:
        print(f"  原文 {f}：", [m.original_ascii for m in valid_moods() if m.figure == f])
    invalid = Mood(1, *"ANA")
    witness = countermodel(invalid)
    print(f"  无效例 {invalid.id}，最小反例：{witness.as_dict()}")
    print("  两前提/结论的真值：", [x.holds(witness) for x in invalid.literals()])
    print("\n7. 24 → 14 → 11 → 6 → 2 不是同一种‘合并’")
    reduction = reductions_record()
    print("  前两步为换位等价；11→6 为包含关系；6→2 为反证法。")
    for certificate in reduction["four_reductio_certificates"]:
        print(" ", certificate["target"], "以", certificate["base"], "推出",
              certificate["derived"], "，与原前提矛盾。")
    print("\n8. 单独改变假设：允许空类")
    print("  有效式从 24 减少到", len(valid_moods(False)))
    lost = Mood(1, *"AAa")
    empty_witness = countermodel(lost, False)
    print("  AAa 的空类反例：", empty_witness.as_dict())
    print("  空类边界是现代对照实验，不是原文五关系表的一部分。")
    print("\n下一步：读 PROOF.md 的完备性证明，再运行 python run_checks.py。")


if __name__ == "__main__":
    main()
