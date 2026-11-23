"""Finite teaching model for the two cases of Euclid VII.32."""
from dataclasses import dataclass
from math import isqrt


@dataclass(frozen=True)
class Certificate:
    branch: str
    prime: int
    path: tuple[int, ...]


def classify(n, *, largest=True):
    if type(n) is not int or n < 2:
        raise ValueError("a given number must be an integer greater than one")
    if type(largest) is not bool:
        raise ValueError("largest must be a boolean")
    path = [n]
    # Self-contained minimal adapter for the VII.31 composite case.
    while (d := next((j for j in range(2, isqrt(path[-1])+1)
                      if path[-1] % j == 0), None)) is not None:
        step = path[-1]//d if largest else d
        if not 1 < step < path[-1] or path[-1]%step or n%step:
            raise ArithmeticError("VII.31 descent invariant failed")
        path.append(step)
    return Certificate("prime-itself" if len(path) == 1 else "VII.31",
                       path[-1], tuple(path))


if __name__ == "__main__":
    print(classify(13))
    print(classify(84))
