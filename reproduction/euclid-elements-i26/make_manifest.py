"""Hash public artifacts, excluding this generated manifest and Python caches."""
import hashlib,json
from pathlib import Path
root=Path('.')
files={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
       for p in sorted(root.rglob('*'))
       if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.json'}
Path('SHA256SUMS.json').write_text(json.dumps(files,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'hashed_files':len(files),'algorithm':'SHA-256','excludes':['SHA256SUMS.json','__pycache__']},ensure_ascii=False))
