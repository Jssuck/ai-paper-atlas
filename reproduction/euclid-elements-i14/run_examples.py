import json
from cases import run_cases
print(json.dumps(run_cases(),ensure_ascii=False,indent=2))
