"""Read-only byte/mode verification against this publication's original snapshot."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import time

parser=argparse.ArgumentParser()
parser.add_argument('--snapshot',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
data=json.loads(args.snapshot.read_text())
root=Path(data['root']); drift=[]; began=time.perf_counter()
for row in data['files']:
    path=root/row['path']
    if not path.exists() and not path.is_symlink():
        drift.append({'path':row['path'],'reason':'missing'}); continue
    mode=stat.S_IMODE(path.lstat().st_mode)
    if path.is_symlink():
        current=hashlib.sha256(str(path.readlink()).encode()).hexdigest(); kind='symlink'
    elif path.is_file():
        hasher=hashlib.sha256()
        with path.open('rb') as stream:
            while block:=stream.read(1024*1024): hasher.update(block)
        current=hasher.hexdigest(); kind='file'
    else:
        drift.append({'path':row['path'],'reason':'unexpected file kind'}); continue
    if current!=row['sha256'] or mode!=row['mode'] or kind!=row['kind']:
        drift.append({'path':row['path'],'reason':'byte/mode/kind drift','current_sha256':current,'current_mode':mode,'current_kind':kind})
result={'schema_version':'wardrobe-publication-primary-preservation/v1','status':'PASS' if not drift else 'FAIL',
        'root':str(root),'protected_files':len(data['files']),'protected_bytes':sum(row['bytes'] for row in data['files']),
        'drift':drift,'seconds':time.perf_counter()-began,'snapshot_sha256':hashlib.sha256(args.snapshot.read_bytes()).hexdigest()}
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({key:result[key] for key in ['status','protected_files','protected_bytes','seconds']}),flush=True)
if drift: print(json.dumps({'drift':drift},ensure_ascii=False),flush=True)
raise SystemExit(0 if not drift else 1)
