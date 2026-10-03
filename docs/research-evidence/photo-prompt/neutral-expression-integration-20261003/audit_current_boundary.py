"""Review the whole public sibling pack before any current golden refresh."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/subculture-illustration-image-generator/assets'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def diff(a, b, path='$'):
    if type(a) is not type(b): return [{'path':path,'before':a,'after':b}]
    if isinstance(a,dict):
        out=[]
        for key in sorted(set(a)|set(b)):
            if key not in a or key not in b:out.append({'path':path+'.'+key,'before':a.get(key),'after':b.get(key)})
            else:out.extend(diff(a[key],b[key],path+'.'+key))
        return out
    if isinstance(a,list):
        if len(a)!=len(b):return [{'path':path,'before':a,'after':b}]
        return [row for i,(aa,bb) in enumerate(zip(a,b)) for row in diff(aa,bb,f'{path}[{i}]')]
    return [] if a==b else [{'path':path,'before':a,'after':b}]

def main():
    golden=ASSETS/'photo_regression_baseline_v5.json'
    before_asset=golden.read_bytes();baseline=json.loads(before_asset)
    (HERE/'current-boundary-v5-before.json').write_bytes(before_asset)
    before=ROOT/'docs/research-evidence/photo-prompt/acting-expression-merge-20261003/merged-current-photo-pack.json'
    assert sha(before)==baseline['sha256']
    command=baseline['command'][:]
    output_index=command.index('--output-file')+1
    env=dict(os.environ,GEMINI_API_KEY='',GOOGLE_API_KEY='')
    for filename in ('current-boundary-after.json','current-boundary-repeat.json'):
        command[output_index]=str(HERE/filename)
        proc=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=90)
        (HERE/(filename+'.log')).write_text(proc.stdout+proc.stderr)
        if proc.returncode:raise RuntimeError(proc.stdout+proc.stderr)
    after=HERE/'current-boundary-after.json';repeat=HERE/'current-boundary-repeat.json'
    assert after.read_bytes()==repeat.read_bytes()
    changes=diff(json.loads(before.read_text()),json.loads(after.read_text()))
    allowed={'$[0].pack_id','$[0].provenance.tags_hash','$[0].core_retrieval.canonical_sha256','$[0].core_retrieval.slot_corpus_sha256','$[0].core_retrieval.slot_ownership_sha256'}
    report={'before_asset_sha256':hashlib.sha256(before_asset).hexdigest(),'before_pack_path':str(before.relative_to(ROOT)),'before_pack_sha256':sha(before),'after_pack_sha256':sha(after),'repeat_bytes_equal':True,'diff_count':len(changes),'diff':changes,'all_differences_are_reviewed_corpus_provenance':all(row['path'] in allowed for row in changes),'historical_baseline_hashes':{f'v{i}':sha(ASSETS/f'photo_regression_baseline_v{i}.json') for i in range(1,5)},'runtime_goldens_not_yet_changed':True}
    save(HERE/'CURRENT-BOUNDARY-COMPARISON.json',report)
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
