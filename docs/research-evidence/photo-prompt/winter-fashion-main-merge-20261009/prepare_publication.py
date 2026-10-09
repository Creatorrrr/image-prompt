"""Preserve the current checkout and copy only the reviewed winter publication scope."""
from pathlib import Path
import hashlib,json,os,shutil,stat,subprocess,zipfile

PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
WORK=Path('/Users/chasoik/.codex/worktrees/winter-fashion-main-merge-20261009/image-prompt')
OUT=PRIMARY/'docs/research-evidence/photo-prompt/winter-fashion-main-merge-20261009'
SKILL='skills/photo-prompt-image-generator'

def git(*args):return subprocess.check_output(['git',*args],cwd=PRIMARY)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,d): (OUT/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

dirty=sorted(set(x.decode() for x in git('ls-files','-m','-o','--exclude-standard','-z').split(b'\0') if x))
snapshot={}
for rel in dirty:
    if rel.startswith(str(OUT.relative_to(PRIMARY))+'/'):continue
    p=PRIMARY/rel
    if p.is_symlink():snapshot[rel]={'type':'symlink','target':os.readlink(p)}
    elif p.is_file():snapshot[rel]={'type':'file','sha256':digest(p),'mode':stat.S_IMODE(p.stat().st_mode),'size':p.stat().st_size}
    elif not p.exists():snapshot[rel]={'type':'deleted'}
save('PRIMARY-BEFORE.json',{'head':git('rev-parse','HEAD').decode().strip(),'tracked_status':git('status','--porcelain=v1','-uno').decode(),'files':snapshot})
with zipfile.ZipFile(OUT/'PRIMARY-TRACKED-BEFORE.zip','w',zipfile.ZIP_DEFLATED) as z:
    for raw in git('ls-files','-m','-z').split(b'\0'):
        if raw:
            rel=raw.decode();p=PRIMARY/rel
            if p.is_file() and not p.is_symlink():z.write(p,rel)

selected=[];excluded=[]
exclude_components={'runtime-store','runtime_store','build-runtime-store','__pycache__','source-data','core-slot-index-data'}
for folder in ['docs/research-evidence/photo-prompt/winter-fashion-20261009','docs/research-evidence/photo-prompt/winter-fashion-integration-20261009']:
    for p in sorted((PRIMARY/folder).rglob('*')):
        if not p.is_file():continue
        rel=str(p.relative_to(PRIMARY))
        if p.is_symlink() or any(s in exclude_components for s in p.parts) or p.name.endswith(('.LOCK','.lock','.partial','.zip','.pyc')):
            excluded.append({'path':rel,'bytes':p.stat().st_size,'reason':'local_cache_lock_or_recovery_archive'});continue
        selected.append(rel)
selected += [
    'docs/analysis/2026-10-09-winter-fashion-visual-semantics-research.md',
    SKILL+'/assets/photo_prompt_winter_fashion_extension.json',
    SKILL+'/assets/photo_prompt_visual_obligations_winter_fashion.json',
    'tests/test_photo_winter_fashion_integration.py',
]
for rel in selected:
    src=PRIMARY/rel;dst=WORK/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
manifest=WORK/SKILL/'assets/photo_prompt_source_manifest.json'
data=json.loads(manifest.read_text());base=json.loads(manifest.read_text())
for name,kind in [('photo_prompt_winter_fashion_extension.json','candidate'),('photo_prompt_visual_obligations_winter_fashion.json','visual_profile')]:
    if any(s['file']==name for s in data['sources']):raise RuntimeError('Unexpected existing winter registration')
    data['sources'].append({'file':name,'kind':kind,'required':True,'load_order':max(s['load_order'] for s in data['sources'] if s['kind']==kind)+1})
manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
selected.append(str(manifest.relative_to(WORK)))
records=[{'path':rel,'sha256':digest(WORK/rel),'bytes':(WORK/rel).stat().st_size} for rel in sorted(selected)]
if any(s['bytes']>=100*1024*1024 for s in records):raise RuntimeError('Oversize selected blob')
# Report matching filenames only; never expose secret values.
secret_hits=[]
import re
secret=re.compile(rb'(?:sk-(?:proj-)?[A-Za-z0-9_-]{30,}|AIza[A-Za-z0-9_-]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)')
for row in records:
    if Path(row['path']).suffix in {'.json','.py','.md','.txt','.log','.ndjson','.csv'} and secret.search((WORK/row['path']).read_bytes()):secret_hits.append(row['path'])
if secret_hits:raise RuntimeError('Secret-shaped value in selected files: '+repr(secret_hits))
save('SCOPE.json',{'base_head':git('rev-parse','HEAD').decode().strip(),'selected':records,'excluded_local_only':excluded,'base_source_rows':len(base['sources']),'appended_source_rows':data['sources'][-2:],'existing_source_rows_byte_semantics_preserved':data['sources'][:-2]==base['sources'],'secret_scan':'PASS_no_secret_shaped_values'})
(OUT/'SCOPE.paths0').write_bytes(b''.join(s.encode()+b'\0' for s in sorted(selected)))
venv=WORK/'.venv'
if not venv.exists():venv.symlink_to(PRIMARY/'.venv',target_is_directory=True)
subprocess.run(['git','switch','-c','codex/winter-fashion-main-merge-20261009'],cwd=WORK,check=True)
subprocess.run(['git','add','--pathspec-from-file='+str(OUT/'SCOPE.paths0'),'--pathspec-file-nul'],cwd=WORK,check=True)
print(json.dumps({'preserved_files':len(snapshot),'selected_files':len(records),'selected_bytes':sum(r['bytes'] for r in records),'local_only_files':len(excluded),'manifest_base_rows_preserved':len(base['sources']),'worktree':str(WORK)}))
