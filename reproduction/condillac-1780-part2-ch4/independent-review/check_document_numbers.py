"""Independent arithmetic only; no production implementation is imported."""
from itertools import product
from pathlib import Path
import json
import hashlib
import platform
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent
DOCUMENTS = (
    "../../papers/1780/condillac-logic-part2-ch4.zh-CN.md",
    "MODEL.zh-CN.md",
    "WALKTHROUGH.zh-CN.md",
)
def document_snapshot():
    return {name: hashlib.sha256((MODEL / name).read_bytes()).hexdigest()
            for name in DOCUMENTS}

before = document_snapshot()
checks=[]
def check(name,r,h,f,n,expected):
    k=len(n[0]) if n else 1
    def loss(g):
        return sum(n[u][a] for u in range(len(r)) for a in range(k) if g[r[u]]!=a)
    got=(loss(h), min(loss(g) for g in product(range(k),repeat=len(h))), sum(h[r[u]]!=f[u] for u in range(len(r))))
    if got!=expected:
        raise RuntimeError((name,got,expected))
    checks.append({'case':name,'empirical':got[0],'minimum_empirical':got[1],'truth_errors':got[2]})

# Main text: distinct hand examples, not described as demo.py runs.
check('main_10.1_old',(0,0,1,1),(1,0),(1,0,1,1),((0,1),(1,0),(0,1),(0,1)),(3,1,3))
check('main_10.1_fit',(0,0,1,1),(0,1),(1,0,1,1),((0,1),(1,0),(0,1),(0,1)),(1,1,1))
check('main_10.2_old',(0,0,0),(0,),(1,0,0),((0,1),(0,0),(0,0)),(1,0,1))
check('main_10.2_fit',(0,0,0),(1,),(1,0,0),((0,1),(0,0),(0,0)),(0,0,2))
check('main_10.3_old',(0,),(0,),(0,),((0,1),),(1,0,0))
check('main_10.3_fit',(0,),(1,),(0,),((0,1),),(0,0,1))
# Model section 8: correct but uneven, complete coverage.
check('model_8_unequal_old',(0,0,0),(0,),(1,0,0),((0,10),(1,0),(1,0)),(10,2,1))
check('model_8_unequal_fit',(0,0,0),(1,),(1,0,0),((0,10),(1,0),(1,0)),(2,2,2))
# Walkthrough sections 1-7, including every displayed phase.
check('walk_1_transparent_wrong',(0,1),(1,0),(0,1),((1,0),(0,1)),(2,0,2))
check('walk_1_opaque_correct',(0,1),(0,1),(0,1),((1,0),(0,1)),(0,0,0))
for name,r,h,e in [('old',(0,0),(0,),(3,2,1)),('fit_coarse',(0,0),(1,),(2,2,1)),('transport_fine',(0,1),(1,1),(2,0,1)),('fit_fine',(0,1),(1,0),(0,0,0)),('bad_fine',(0,1),(0,1),(5,0,2))]:
    check('walk_2_'+name,r,h,(1,0),((0,3),(2,0)),e)
check('walk_3_old',(0,0,0),(0,),(1,0,0),((0,3),(0,0),(0,0)),(3,0,1))
check('walk_3_fit',(0,0,0),(1,),(1,0,0),((0,3),(0,0),(0,0)),(0,0,2))
check('walk_4_old',(0,0,1),(1,1),(0,1,1),((1,0),(0,1),(0,0)),(1,1,1))
check('walk_4_fit',(0,0,1),(0,1),(0,1,1),((1,0),(0,1),(0,0)),(1,1,1))
check('walk_5_old',(0,),(0,),(0,),((0,4),),(4,0,0))
check('walk_5_fit',(0,),(1,),(0,),((0,4),),(0,0,1))
check('walk_5_corrected_fit',(0,),(0,),(0,),((4,0),),(0,0,0))
for name,r,h,e in [('old',(0,0),(0,1),(0,0,0)),('unchanged_h',(0,1),(0,1),(1,0,1)),('transport_h',(0,1),(0,0),(0,0,0)),('refit',(0,1),(0,0),(0,0,0))]:
    check('walk_6_'+name,r,h,(0,0),((1,0),(1,0)),e)
check('walk_7_original',(0,0),(1,),(1,0),((0,3),(2,0)),(2,2,1))
check('walk_7_renamed',(0,0),(1,),(1,0),((0,3),(2,0)),(2,2,1))
if len(checks) != 28:
    raise RuntimeError("Declared fixture count differs from executed fixture count")
if document_snapshot() != before:
    raise RuntimeError("Reviewed documents changed while arithmetic was checked")
result = {
    "scope": "Independent direct arithmetic on manually transcribed hand examples. No production code is imported. This is neither a general proof nor an additional empirical experiment.",
    "command": "python3 -B independent-review/check_document_numbers.py",
    "cwd": ".",
    "finished_utc": datetime.now(timezone.utc).isoformat(),
    "python_version": platform.python_version(),
    "implementation": platform.python_implementation(),
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "document_sha256": before,
    "documents_unchanged": True,
    "case_count": len(checks),
    "status": "passed",
    "checks": checks,
}
(HERE / "document-numeric-results.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"cases": len(checks), "status": "passed",
                  "result": "independent-review/document-numeric-results.json"}))
