"""Small inspectable countermodels; all outcomes printed as deterministic JSON."""
import json
from model import Affect, Beliefs, JudgmentHabit, World, evaluate

WORLDS = (
    World("failure_obstacle", False, False),
    World("failure_clear", False, True),
    World("success_obstacle", True, False),
    World("success_clear", True, True),
)
DESIRE = Affect(lacking=True, known=True, habitual_imagination=True, faculties_directed=True)
EXPERIENCE_HABIT = JudgmentHabit(established=True, from_experience=True)


def case(name, affect, support, actual, habit=EXPERIENCE_HABIT):
    beliefs = Beliefs(WORLDS, frozenset(support), actual)
    return {"case": name, "support": sorted(support), "actual": actual,
            "labels": evaluate(affect, beliefs, habit)}


def main():
    examples = [
        case("01_unknown_lack", Affect(lacking=True), ["success_clear"], "success_clear"),
        case("02_never_enjoyed_but_imagined", DESIRE, ["success_clear"], "success_clear"),
        case("03_hope_without_narrow_will", DESIRE, ["success_obstacle"], "success_obstacle"),
        case("04_narrow_will_without_bridge", DESIRE, ["failure_clear"], "failure_clear"),
        case("05_false_confidence", DESIRE, ["success_clear"], "failure_obstacle"),
        case("06_uncertain_support", DESIRE, ["success_clear", "failure_obstacle"], "success_clear"),
        case("07_experience_without_habit", DESIRE, ["success_clear"], "success_clear", JudgmentHabit(False, True)),
        case("08_suspended_passion", Affect(desire_habit=True), ["success_clear"], "success_clear"),
        case("09_active_passion", Affect(True, True, False, True, True, True), ["success_clear"], "success_clear"),
    ]
    before = Beliefs(WORLDS, frozenset(["success_clear", "failure_obstacle"]), "failure_obstacle")
    after = before.restrict(frozenset(["success_clear"]))
    try:
        before.restrict(frozenset())
    except ValueError as error:
        empty_error = str(error)
    else:
        raise RuntimeError("empty support unexpectedly accepted")
    print(json.dumps({"schema": "condillac-i8-teaching-v1", "examples": examples,
                      "support_restriction": {"before": sorted(before.support), "after": sorted(after.support),
                                              "before_judges_obtaining": before.judges("obtains"),
                                              "after_judges_obtaining": after.judges("obtains"),
                                              "actual_obtaining_before": before.actually("obtains"),
                                              "actual_obtaining_after": after.actually("obtains"),
                                              "actual_obtaining_unchanged": before.actually("obtains") == after.actually("obtains"),
                                              "empty_restriction_error": empty_error}}, indent=2))


if __name__ == "__main__":
    main()
