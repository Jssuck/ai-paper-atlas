import json
from cases import evaluate
print(json.dumps(evaluate(),ensure_ascii=False,indent=2))
