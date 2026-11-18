"""Finite exact checks; emit fresh run data to stdout, never claim a general proof."""
import json, platform, sys
from datetime import datetime, timezone
from fractions import Fraction as F
from geometry import Arc, make_arc, unit, dot, sub, add, scale


def check(ok, message):
    if not ok: raise RuntimeError(message)


def run():
    ts=[F(-5),F(-2),F(-1),F(-1,2),F(-1,5),None,F(1,5),F(1,2),F(1),F(2),F(5)]
    samples=[unit(F(i,5)) for i in range(-20,21)]+[(F(-1),F(0))]
    counts={"arcs":0,"inscribed_checks":0,"mapped_points":0,"membership_checks":0,"distance_checks":0,"unequal_radius_controls":0}
    for r in (F(1),F(3,2),F(5)):
        for t in ts:
            for ccw in (True,False):
                a=make_arc(r,t,ccw=ccw)
                b=make_arc(r,t,center=(7,-3),rotation=unit(F(2,3)),ccw=ccw)
                # Reflection reverses sweep orientation and swaps sign of endpoint y.
                tb=None if t is None else -t
                reflected=make_arc(r,tb,center=(-4,9),rotation=unit(F(-3,4)),ccw=not ccw)
                counts["arcs"]+=1
                for target in (b,reflected):
                    check(a.congruent_to(target),"transformed arc not congruent")
                    check(a.map_point_to(target,a.end)==target.end,"endpoint mapping failed")
                    for z in samples:
                        p=scale(r,z)
                        q=a.map_point_to(target,p)
                        check(a.contains_open(p)==target.contains_open(q),"membership not preserved")
                        counts["mapped_points"]+=1; counts["membership_checks"]+=1
                        check(dot(sub(p,a.start),sub(p,a.start))==dot(sub(q,target.start),sub(q,target.start)),"distance not preserved")
                        counts["distance_checks"]+=1
                        if p not in (a.start,a.end) and not a.contains_open(p):
                            c=a.inscribed_cot(p)
                            check(c==a.half_sweep_cot(),"inscribed half-sweep identity failed")
                            check(c==target.inscribed_cot(q),"inscribed angle not preserved")
                            counts["inscribed_checks"]+=1
                other=make_arc(2*r,t,ccw=ccw)
                check(a.half_sweep_cot()==other.half_sweep_cot() and not a.congruent_to(other),"radius negative control failed")
                counts["unequal_radius_controls"]+=1
    return {"timestamp_utc":datetime.now(timezone.utc).isoformat(),"python":sys.version,"platform":platform.platform(),"optimization":sys.flags.optimize,"arithmetic":"fractions.Fraction exact; no floating-point equality", "counts":counts,"result":"PASS","limits":"Finite sample checks only; not a formal proof, not old-run recovery, not remote publication validation."}


if __name__=="__main__": print(json.dumps(run(),ensure_ascii=False,indent=2))
