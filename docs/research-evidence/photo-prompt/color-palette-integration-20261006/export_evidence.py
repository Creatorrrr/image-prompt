"""Copy the owned evidence package and verify every destination byte."""
from pathlib import Path
import hashlib
import json
import re
import shutil

E=Path(__file__).resolve().parent
W=E.parents[3]
P=Path('/Users/chasoik/Projects/image-prompt')
D=P/E.relative_to(W)
MANIFEST='PUBLISH-PACKAGE.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

files=[p for p in sorted(E.rglob('*')) if p.is_file() and p.name!=MANIFEST and '__pycache__' not in p.parts]
rows=[]
for p in files:
    target=D/p.relative_to(E)
    target.parent.mkdir(parents=True,exist_ok=True)
    raw=p.read_bytes()
    target.write_bytes(raw)
    expected=hashlib.sha256(raw).hexdigest()
    assert sha(target)==expected,str(target)
    rows.append({'path':str(p.relative_to(E)),'bytes':len(raw),'sha256':expected})

report=json.loads((D/'QUALIFICATION-REPORT.json').read_text())
assert report['native_image_calls']==5 and report['independent_arms']==3
for case in report['cases']:
    target=Path(case['primary_image_copy'])
    assert sha(target)==case['image_sha256']

broken=[]
for target in re.findall(r'\]\((/[^)]+)\)',(D/'README.md').read_text()):
    if not Path(target).is_file():broken.append(target)
assert not broken,broken

payload={'schema_version':'color-palette-evidence-package/v1','source_worktree':str(W),'primary_evidence_directory':str(D),'files':rows,'file_count':len(rows),'bytes':sum(r['bytes'] for r in rows),'copy_verified':True,'readme_file_links_verified':True,'native_image_calls':5,'generated_images_preserved':True,'frozen_arm_paths_rewritten':False}
raw=(json.dumps(payload,ensure_ascii=False,indent=2)+'\n').encode()
(E/MANIFEST).write_bytes(raw)
(D/MANIFEST).write_bytes(raw)
assert sha(E/MANIFEST)==sha(D/MANIFEST)
print(json.dumps({k:v for k,v in payload.items() if k!='files'},ensure_ascii=False,indent=2))
