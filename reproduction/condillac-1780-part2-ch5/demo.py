"""Deterministic worked examples; no timing or unordered set output."""
import json
from examples import main_system, with_edges
from named_classes import InvalidGraph, prototype_accepts


def show(name, value):
    print(f"{name}: {json.dumps(value, ensure_ascii=False)}")


def main():
    system = main_system()
    show("对象顺序", system.objects)
    for label in system.labels:
        show(f"外延[{label}]", [x for x in system.objects if x in system.extension(label)])
    show("断言边", system.edges)
    for source, target in (("三边形", "图形"), ("红色", "图形"),
                           ("三角形", "红色"), ("红色", "三角形"),
                           ("三角形", "三边形"), ("空类", "三角形"),
                           ("三角形", "三角形")):
        show(f"查询[{source}→{target}]", {
            "有限域包含": system.includes(source, target),
            "图证明": system.prove(source, target),
            "反例": system.witness(source, target),
        })
    show("单例检查[红三角是否红色]", prototype_accepts(system, "三角形", "红色", "红三角"))
    show("原图强连通分量", system.components())
    cyclic = with_edges(system, ("三角形", "三边形"))
    show("加同义返回边后的分量", cyclic.components())
    renamed = system.rename(("A", "B", "C", "D", "Z"))
    show("改名后[D→B]", renamed.prove("D", "B"))
    show("改名后对象数", len(renamed.objects))
    invalid = with_edges(system, ("红色", "三角形"))
    show("坏边及反例", invalid.violations())
    show("坏图原始可达[图形→图形]", invalid.find_path("图形", "图形"))
    try:
        invalid.prove("图形", "图形")
    except InvalidGraph:
        show("坏图认证[图形→图形]", "拒绝：全图有效性前提不成立")
    else:
        raise RuntimeError("invalid graph was unexpectedly certified")


if __name__ == "__main__":
    main()
