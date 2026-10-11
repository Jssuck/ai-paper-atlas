#!/usr/bin/env python3
"""Produce deterministic, transparent results; no training, network, or randomness."""
import argparse
import json
from pathlib import Path
from fixtures import garden
from model import (Item, Truth, boundary_name, claims_are_accurate, common_refinement,
                   is_refinement, is_sufficient, normalize_partition,
                   observation_conflicts, observation_partition, observed_truth,
                   task_partition)


def experiments() -> dict:
    items = garden()
    stages = []
    definitions = (
        ("no_distinction_needed", ()),
        ("harvest", ("harvest",)),
        ("sort_fruit", ("sort_fruit",)),
        ("sort_and_shade", ("sort_fruit", "shade")),
    )
    for name, needs in definitions:
        partition = task_partition(items, needs)
        stages.append({"stage": name, "needs": list(needs), "classes": len(partition),
                       "partition": partition, "sufficient": is_sufficient(items, partition, needs)})
    individual = normalize_partition((item.object_id,) for item in items)
    sort_partition = task_partition(items, ("sort_fruit",))
    shade_partition = task_partition(items, ("shade",))
    joint_partition = task_partition(items, ("sort_fruit", "shade"))
    coarse = task_partition(items, ())
    renamed_classes = {f"renamed-{i}": block for i, block in enumerate(sort_partition)}
    renamed_partition = normalize_partition(renamed_classes.values())
    stages.append({"stage": "one_name_per_individual", "needs": ["sort_fruit", "shade"],
                   "classes": len(individual), "partition": individual,
                   "sufficient": is_sufficient(items, individual, ("sort_fruit", "shade")),
                   "unnecessary_extra_classes_for_current_needs": len(individual) - len(joint_partition)})
    stages.append({"stage": "shade_need_removed", "needs": ["sort_fruit"],
                   "classes": len(sort_partition), "partition": sort_partition,
                   "sufficient": is_sufficient(items, sort_partition, ("sort_fruit",))})

    observed = ("visible_green",)
    conflicts = observation_conflicts(items, observed, ("harvest",))
    boundary = tuple(Item(oid, {"height": height}, {"display": "keep"}) for oid, height in
                     (("b1", 3.0), ("b2", 4.0), ("b3", 5.0), ("b4", 6.0), ("b5", 7.0), ("b6", None)))
    names: dict[str, list[str]] = {}
    for item in boundary:
        names.setdefault(boundary_name(item.attributes["height"]), []).append(item.object_id)
    fine_names = normalize_partition(names.values())
    parent_name = normalize_partition(([item.object_id for item in boundary],))
    accuracy_truth = {"visible_green": True, "height": 5.0, "fruit_kind": "none"}
    partial_claim = {"visible_green": True}
    overclaim = {"visible_green": True, "height": 7.0}
    unknowns = [True, False, None]
    all_counts = [stage["classes"] for stage in stages]
    if all_counts != [1, 2, 5, 7, 8, 5]:
        raise AssertionError(all_counts)
    return {
        "status": "modern_teaching_reconstruction_not_historical_algorithm_or_empirical_psychology",
        "source_scope": "Condillac, La Logique, I.IV, printed pp.32–48; IA PDF pp.40–56",
        "data_status": "All 8 objects, attributes, outputs and thresholds are invented inputs.",
        "objects": [{"object_id": item.object_id, "attributes": dict(item.attributes),
                     "targets": dict(item.targets)} for item in items],
        "naming": {"first_encounter": {"object_id": "a1", "assigned_name": "tree"},
                   "later_reuse": {"assigned_name": "tree", "objects": sorted(item.object_id for item in items)},
                   "sufficient_for_harvest": is_sufficient(items, coarse, ("harvest",)),
                   "disclaimer": "This sequence is scripted, not inferred child behavior."},
        "stages": stages,
        "refinement": {"joint_equals_common_refinement": joint_partition == common_refinement(sort_partition, shade_partition),
                       "added_need_refines": is_refinement(joint_partition, sort_partition),
                       "removed_need_allows_coarsening": is_refinement(joint_partition, sort_partition),
                       "renaming_changes_membership": renamed_partition != sort_partition},
        "observation_limit": {
            "observed_fields": list(observed),
            "observed_partition": observation_partition(items, observed),
            "target_needs": ["harvest"], "conflicting_pairs_count": len(conflicts),
            "first_witness": conflicts[0],
            "enriched_observation_fields": ["fruit_kind"],
            "remaining_conflicts_after_enrichment": observation_conflicts(items, ("fruit_kind",), ("harvest",)),
        },
        "boundary_names": {
            "convention": "height below 4: shrub; above 6: tree; inclusive [4,6] or unknown: plant",
            "rows": [{"id": item.object_id, "height": item.attributes["height"],
                      "name": boundary_name(item.attributes["height"]), "display_action": "keep"}
                     for item in boundary],
            "report_label_classes": len(fine_names), "all_plant_classes": len(parent_name),
            "label_scope": "The three report-label groups are not concept extensions: plant as a parent concept includes every tree and shrub too.",
            "all_plant_sufficient_for_display": is_sufficient(boundary, parent_name, ("display",)),
            "warning": "The coarse name is acceptable only for this declared common action; it is not always safe for new tasks.",
        },
        "unknown": {"observations": [{"observed": value, "truth": observed_truth(value).value}
                                        for value in unknowns],
                    "unknown_equals_false": observed_truth(None) is Truth.FALSE,
                    "unknown_objects_can_need_different_actions": observation_conflicts(
                        (Item("u1", {"shade_ready": None}, {"shade": "use"}),
                         Item("u2", {"shade_ready": None}, {"shade": "skip"})),
                        ("shade_ready",), ("shade",))},
        "accuracy_and_completeness": {
            "finite_reference": accuracy_truth,
            "partial_claim": partial_claim, "partial_claim_accurate": claims_are_accurate(accuracy_truth, partial_claim),
            "partial_claim_covers_all_reference_fields": set(partial_claim) == set(accuracy_truth),
            "overclaim": overclaim, "overclaim_accurate": claims_are_accurate(accuracy_truth, overclaim),
            "disclaimer": "Completeness is only relative to the finite table, never to all properties of a real object.",
        },
    }


def summary(result: dict) -> str:
    lines = ["Condillac I.IV：现代有限分类教学模型（非原作者算法）", "数据全部虚构；没有心理学经验复现。", ""]
    for stage in result["stages"]:
        lines.append(f"{stage['stage']}: {stage['classes']} classes; sufficient={stage['sufficient']}")
    witness = result["observation_limit"]["first_witness"]
    obs = result["observation_limit"]
    boundary = result["boundary_names"]
    accuracy = result["accuracy_and_completeness"]
    lines.extend(["", f"合并需要 = 分区共同细化: {result['refinement']['joint_equals_common_refinement']}",
                  f"只有绿色观测：{obs['conflicting_pairs_count']} 对冲突；首例 {witness['objects']}",
                  f"增加 fruit_kind 观测后的采收冲突数: {len(obs['remaining_conflicts_after_enrichment'])}",
                  f"当前陈列任务：全部改用 plant 后仍充分: {boundary['all_plant_sufficient_for_display']}",
                  f"未知 = 假: {result['unknown']['unknown_equals_false']}",
                  f"部分断言：准确 {accuracy['partial_claim_accurate']}；覆盖有限参照表所有字段 {accuracy['partial_claim_covers_all_reference_fields']}",
                  "", "结论只对已声明的对象、需要与证据成立；不自动推广到新对象。"])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "results")
    args = parser.parse_args()
    result = experiments()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report = summary(result)
    (args.output_dir / "summary.txt").write_text(report, encoding="utf-8")
    print(report, end="")


if __name__ == "__main__":
    main()
