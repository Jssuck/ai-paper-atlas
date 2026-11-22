"""VII.3 teaching model: reduce the first pair, then decide which branch applies."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    first_measure: int
    final_measure: int
    branch: str
    first_rows: tuple
    second_rows: tuple


def pair(a,b):
    """Modern bundled subtraction trace."""
    rows=[]
    a,b=max(a,b),min(a,b)
    while b:
        q,r=divmod(a,b)
        rows.append((a,b,q,r))
        a,b=b,r
    return a,tuple(rows)


def three(a,b,c,ancient_domain=False):
    if any(type(x) is not int or x<1 for x in (a,b,c)):
        raise ValueError("positive integers required")
    d,first=pair(a,b)
    if c%d==0:
        out=Result(d,d,"direct",first,())
    else:
        g,second=pair(d,c)
        out=Result(d,g,"reduce",first,second)
    if ancient_domain and out.final_measure==1:
        raise ValueError("VII.3 assumes that a common nonunit measures the triple")
    return out


def direct_common(*values):
    return tuple(k for k in range(1,min(values)+1) if all(not (v%k) for v in values))
