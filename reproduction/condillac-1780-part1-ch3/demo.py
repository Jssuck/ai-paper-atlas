"""Deterministic worked examples matching WALKTHROUGH.zh-CN.md."""
from model import Branch, Leaf, display, evaluate, leaf_bag, ordered_leaves, parse, serialize


def show(label, tree):
    print(label)
    print("  expression:", display(tree))
    print("  full prefix:", serialize(tree))
    print("  ordered leaves:", ordered_leaves(tree))
    print("  leaf bag:", leaf_bag(tree))
    print("  integer output:", evaluate(tree))
    print("  exact round trip:", parse(serialize(tree)) == tree)


def main():
    show("A: retain every operation, side, and bracket", Branch("SUB", Leaf(2), Branch("ADD", Leaf(0), Leaf(1))))
    show("B: change the operation", Branch("ADD", Leaf(0), Leaf(1)))
    show("C: same ordered leaves as B, different output", Branch("SUB", Leaf(0), Leaf(1)))
    show("D: exchange C's two parts", Branch("SUB", Leaf(1), Leaf(0)))
    show("E: left-associated subtraction", Branch("SUB", Branch("SUB", Leaf(0), Leaf(0)), Leaf(1)))
    show("F: right-associated subtraction", Branch("SUB", Leaf(0), Branch("SUB", Leaf(0), Leaf(1))))
    show("G: a bare zero", Leaf(0))
    show("H: same output as G, different parts", Branch("SUB", Leaf(1), Leaf(1)))
    print("STRICT PARSER REJECTIONS")
    malformed = [(), (("ADD",), ("LEAF", 0)), (("LEAF", 0), ("LEAF", 1)), (("LEAF", True),)]
    for prefix in malformed:
        try:
            parse(prefix)
        except (TypeError, ValueError) as exc:
            print(f"  {prefix!r} -> {type(exc).__name__}: {exc}")
        else:
            raise RuntimeError("malformed input was accepted")


if __name__ == "__main__":
    main()
