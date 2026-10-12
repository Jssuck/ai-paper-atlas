"""Print stable, small examples. Run: python3 -B demo.py"""
import json
from examples import cases
from finite_language import empirical_loss, minimum_empirical_loss, predictions, truth_errors


def main() -> None:
    for name, stages in cases().items():
        print(name)
        for stage, problem in stages:
            print(json.dumps({"stage": stage, "h": dict(zip(problem.labels, problem.h)),
                "predictions": predictions(problem), "empirical_loss": empirical_loss(problem),
                "minimum_empirical_loss": minimum_empirical_loss(problem),
                "truth_errors": truth_errors(problem)}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
