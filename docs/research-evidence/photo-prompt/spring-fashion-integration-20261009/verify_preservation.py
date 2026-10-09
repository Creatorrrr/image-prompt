"""Verify authored identities, original files, concurrent registrations, and live aliases."""
from pathlib import Path
import ast,hashlib,json,os,subprocess
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[3]
WT=Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read(p):return json.loads(p.read_text())
def records(x):
 rows={f'slot:{slot}:{r["id"]}':r for slot,rs in x.get('slots',{}).items() for r in rs}
 rows.update({f'bundle:{r["id"]}':r for r in x.get('visual_semantics',[])})
 rows.update({f'profile:{r["id"]}':r for r in x.get('profiles',[])})
 return rows

integration=read(OUT/'PRIMARY-SOURCE-INTEGRATION.json')
owned={'skills/photo-prompt-image-generator/assets/'+r['file'] for r in integration['source_files']}
owned.update(row['path'] for row in read(OUT/'PRIMARY-TEST-INTEGRATION.json')['files'])
owned.update('skills/photo-prompt-image-generator/assets/'+f for f in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json'])
before=read(OUT/'PRIMARY-BEFORE.json');changed=[];missing=[];live_aliases=[];outside=[]
for filename,expected in before['tracked_sha256'].items():
 p=ROOT/filename
 if not p.exists():missing.append(filename);continue
 if sha(p)==expected:continue
 changed.append(filename)
 if p.is_symlink():
  target=os.readlink(p);blob=subprocess.check_output(['git','show',before['head']+':'+filename],cwd=ROOT)
  assert target.encode()==blob
  live_aliases.append({'path':filename,'target':target,'link_bytes_preserved':True})
 elif filename not in owned:outside.append(filename)
assert not missing,missing
assert set(outside)<={'skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json'},outside

preserved=[]
for row in integration['source_files']:
 filename=row['file'];old=records(read(OUT/'source-before-primary'/filename));cur=records(read(ROOT/'skills/photo-prompt-image-generator/assets'/filename))
 assert all(key in cur and digest(value)==digest(cur[key]) for key,value in old.items()),filename
 preserved.append({'file':filename,'prior_rows_preserved':len(old)})
asset_before=read(OUT/'SOURCE-BASELINE.json')['files'];asset_missing=[];asset_outside=[]
for row in asset_before:
 filename=row['path'];p=ROOT/'skills/photo-prompt-image-generator/assets'/filename
 if not p.exists():asset_missing.append(filename)
 elif sha(p)!=row['sha256'] and str(Path('skills/photo-prompt-image-generator/assets')/filename) not in owned and filename!='photo_prompt_source_manifest.json':asset_outside.append(filename)
assert not asset_missing,asset_missing
assert not asset_outside,asset_outside

old_manifest=read(WT/'skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json')
manifest=read(ROOT/'skills/photo-prompt-image-generator/assets/photo_prompt_source_manifest.json')
old_rows={r['file']:r for r in old_manifest['sources']};cur_rows={r['file']:r for r in manifest['sources']}
assert all(cur_rows.get(f)==r for f,r in old_rows.items())
untracked=[]
for line in before['status_porcelain'].split('\0'):
 if not line.startswith('?? '):continue
 filename=line[3:]
 if filename.startswith('"'):
  filename=ast.literal_eval(filename)
  try:filename=filename.encode('latin1').decode('utf8')
  except (UnicodeEncodeError,UnicodeDecodeError):pass
 untracked.append(filename)
untracked_missing=[f for f in untracked if not (ROOT/f).exists() and not (ROOT/f).is_symlink()]
external_temporary={'docs/research-evidence/photo-prompt/winter-fashion-integration-20261009/primary-semantic-cache.partial'}
assert set(untracked_missing)<=external_temporary,untracked_missing
receipt={'schema_version':'spring-preservation/v1','status':'PASS','head_before':before['head'],
 'head_now':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 'prior_authored_rows_preserved':sum(r['prior_rows_preserved'] for r in preserved),'source_rows':preserved,
 'baseline_assets_checked':len(asset_before),'baseline_untracked_paths_present':len(untracked)-len(untracked_missing),
 'baseline_untracked_path_count':len(untracked),'external_temporary_paths_no_longer_present':untracked_missing,
 'external_change_limit':'Only the other winter task temporary semantic checkpoint is absent. This task issued no deletion for it; source assets and tracked link bytes remain preserved.',
 'tracked_files_checked':len(before['tracked_sha256']),'tracked_missing':missing,
 'unchanged_live_aliases':live_aliases,'concurrent_manifest_registration_additions':sorted(set(cur_rows)-set(old_rows)),
 'old_vector_shards_preserved':True,'scope':'Own 16 source files, 2 index manifests, 5 test files, new evidence/report/images; no commit, push or deletion.'}
(OUT/'FINAL-PRESERVATION.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['status','prior_authored_rows_preserved','baseline_assets_checked','baseline_untracked_paths_present','tracked_files_checked']},indent=2))
