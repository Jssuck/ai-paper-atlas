"""Fixed data for the Chinese walkthrough."""
from named_classes import ClassSystem


def main_system():
    objects = ("红三角", "蓝三角", "红方块", "蓝方块")
    return ClassSystem(
        objects,
        ("三角形", "图形", "红色", "三边形", "空类"),
        (frozenset(objects[:2]), frozenset(objects),
         frozenset((objects[0], objects[2])), frozenset(objects[:2]), frozenset()),
        (("三边形", "三角形"), ("三角形", "图形"), ("空类", "红色")),
    )


def with_edges(system, *extra):
    return ClassSystem(system.objects, system.labels, system.extensions, system.edges + extra)
