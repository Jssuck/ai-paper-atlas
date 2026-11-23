"""Finite exact demonstration of the descent in Euclid VII.31."""
from math import isqrt


def smallest_proper(n):
    return next((d for d in range(2,isqrt(n)+1) if n%d == 0), None)


def descend(n, choice="largest"):
    if type(n) is not int or n < 2:
        raise ValueError("a given number must be an integer greater than one")
    if choice not in ("largest","smallest","middle"):
        raise ValueError("unknown choice")
    if smallest_proper(n) is None:
        raise ValueError("a composite start is required")
    chain = [n]
    while (d := smallest_proper(chain[-1])) is not None:
        a = chain[-1]
        if choice == "largest":
            nxt = a//d
        elif choice == "smallest":
            nxt = d
        else:
            candidates = [i for i in range(2,a) if a%i == 0]
            nxt = candidates[len(candidates)//2]
        if not 1 < nxt < a or a % nxt or n % nxt:
            raise ArithmeticError("proper-descent invariant failed")
        chain.append(nxt)
    return tuple(chain)


if __name__ == "__main__":
    for choice in ("largest","smallest","middle"):
        print(choice,descend(84,choice))
