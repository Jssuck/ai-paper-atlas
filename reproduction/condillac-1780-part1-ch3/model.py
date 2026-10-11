"""An original modern teaching model; not a historical Condillac algorithm.

Only standard-library Python is used. Public validation does not rely on assert.
Trees describe syntax, not physical machines or a model of human cognition.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class Leaf:
    value: int

    def __post_init__(self) -> None:
        if type(self.value) is not int:
            raise TypeError("a leaf value must have exact type int (not bool)")


@dataclass(frozen=True, slots=True)
class Branch:
    op: str
    left: Tree
    right: Tree

    def __post_init__(self) -> None:
        if type(self.op) is not str:
            raise TypeError("an operation must have exact type str")
        if self.op not in ("ADD", "SUB"):
            raise ValueError("operation must be ADD or SUB")
        if type(self.left) not in (Leaf, Branch) or type(self.right) not in (Leaf, Branch):
            raise TypeError("children must be exact Leaf or Branch instances")


Tree: TypeAlias = Leaf | Branch
Token: TypeAlias = tuple[str, int] | tuple[str]
Prefix: TypeAlias = tuple[Token, ...]


def validate_tree(tree: Tree) -> None:
    """Reject invalid fields and cycles; shared subtrees mean repeated occurrences.

    Constructors suffice for ordinary inputs. Revalidation also protects public
    functions from accidental invalid instances produced by bypassing constructors.
    """
    active: set[int] = set()
    completed: set[int] = set()
    stack: list[tuple[object, bool]] = [(tree, False)]
    while stack:
        node, leaving = stack.pop()
        if type(node) not in (Leaf, Branch):
            raise TypeError("tree nodes must be exact Leaf or Branch instances")
        identity = id(node)
        if leaving:
            active.remove(identity)
            completed.add(identity)
            continue
        if identity in active:
            raise ValueError("cyclic objects are not finite expression trees")
        if identity in completed:
            continue
        if type(node) is Leaf:
            try:
                value = node.value
            except AttributeError as exc:
                raise TypeError("leaf has no value") from exc
            if type(value) is not int:
                raise TypeError("a leaf value must have exact type int (not bool)")
            completed.add(identity)
        else:
            try:
                op, left, right = node.op, node.left, node.right
            except AttributeError as exc:
                raise TypeError("branch is missing a field") from exc
            if type(op) is not str:
                raise TypeError("an operation must have exact type str")
            if op not in ("ADD", "SUB"):
                raise ValueError("operation must be ADD or SUB")
            active.add(identity)
            stack.extend(((node, True), (right, False), (left, False)))


def serialize(tree: Tree) -> Prefix:
    """Preorder typed prefix: ('LEAF', n), ('ADD',), or ('SUB',)."""
    validate_tree(tree)
    tokens: list[Token] = []
    stack = [tree]
    while stack:
        node = stack.pop()
        if type(node) is Leaf:
            tokens.append(("LEAF", node.value))
        else:
            tokens.append((node.op,))
            stack.extend((node.right, node.left))
    return tuple(tokens)


def parse(tokens: Prefix) -> Tree:
    """Strictly consume one complete expression; no coercion or ignored suffix.

    Prefix is a Python tuple of typed token tuples, not a text/eval format.
    A reverse scan is an iterative equivalent of the prefix grammar's parser.
    """
    if type(tokens) is not tuple:
        raise TypeError("the prefix container must have exact type tuple")
    if not tokens:
        raise ValueError("empty prefix has no tree")
    for token in tokens:
        if type(token) is not tuple:
            raise TypeError("each token must have exact type tuple")
        if not token or type(token[0]) is not str:
            raise ValueError("each token needs a string tag")
        if token[0] == "LEAF":
            if len(token) != 2:
                raise ValueError("LEAF token must have exactly two fields")
            if type(token[1]) is not int:
                raise TypeError("LEAF payload must have exact type int (not bool)")
        elif token[0] in ("ADD", "SUB"):
            if len(token) != 1:
                raise ValueError("operation token must have exactly one field")
        else:
            raise ValueError("unknown prefix token tag")
    stack: list[Tree] = []
    for token in reversed(tokens):
        if token[0] == "LEAF":
            stack.append(Leaf(token[1]))
        else:
            if len(stack) < 2:
                raise ValueError("truncated prefix: operation needs two children")
            left, right = stack.pop(), stack.pop()
            stack.append(Branch(token[0], left, right))
    if len(stack) != 1:
        raise ValueError("surplus prefix: exactly one complete tree is required")
    return stack[0]


def ordered_leaves(tree: Tree) -> tuple[int, ...]:
    return tuple(token[1] for token in serialize(tree) if token[0] == "LEAF")


def leaf_bag(tree: Tree) -> tuple[int, ...]:
    """A multiset encoded by a sorted tuple, preserving multiplicities."""
    return tuple(sorted(ordered_leaves(tree)))


def evaluate(tree: Tree) -> int:
    """Exact integer interpretation. SUB always means left minus right."""
    stack: list[int] = []
    for token in reversed(serialize(tree)):
        if token[0] == "LEAF":
            stack.append(token[1])
        else:
            left, right = stack.pop(), stack.pop()
            stack.append(left + right if token[0] == "ADD" else left - right)
    return stack[0]


def leaf_count(tree: Tree) -> int:
    return len(ordered_leaves(tree))


def display(tree: Tree) -> str:
    """Human-readable fully parenthesized view, not an accepted input language."""
    stack: list[str] = []
    for token in reversed(serialize(tree)):
        if token[0] == "LEAF":
            stack.append(str(token[1]))
        else:
            left, right = stack.pop(), stack.pop()
            symbol = "+" if token[0] == "ADD" else "-"
            stack.append(f"({left} {symbol} {right})")
    return stack[0]


def generate_trees(leaves: int, values: tuple[int, ...] = (0, 1, 2)) -> tuple[Tree, ...]:
    """All ordered full binary trees of exactly `leaves` leaves, once each."""
    if type(leaves) is not int:
        raise TypeError("leaves must have exact type int")
    if leaves < 1:
        raise ValueError("leaves must be positive")
    if type(values) is not tuple:
        raise TypeError("values must have exact type tuple")
    if not values or any(type(value) is not int for value in values):
        raise ValueError("values must be a nonempty tuple of exact integers")
    if len(set(values)) != len(values):
        raise ValueError("duplicate alphabet values would duplicate trees")
    levels: dict[int, tuple[Tree, ...]] = {1: tuple(Leaf(value) for value in values)}
    for size in range(2, leaves + 1):
        levels[size] = tuple(
            Branch(op, left, right)
            for left_size in range(1, size)
            for left in levels[left_size]
            for right in levels[size - left_size]
            for op in ("ADD", "SUB")
        )
    return levels[leaves]
