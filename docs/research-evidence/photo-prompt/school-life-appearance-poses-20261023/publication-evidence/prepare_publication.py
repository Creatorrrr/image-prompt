"""Copy the reviewed school-only scope; never stage or clean a shared checkout."""
from pathlib import Path
import json,hashlib,subprocess,shutil,gzip,os,sys,datetime
ROOT=Path('/Users/chasoik/Projects/image-prompt')
WT=Path('/Users/chasoik/.codex/worktrees/school-life-publication/image-prompt')
CACHE=Path('/Users/chasoik/.cache/image-prompt/school-life-publication-20261023-01a1678d')
PREFIX=Path('docs/research-evidence/photo-prompt');TOPICS=['school-life-20261023','school-life-appearance-poses-20261023']
PUB=PREFIX/TOPICS[1]/'publication-evidence';S=Path('skills/photo-prompt-image-generator')
OWN=[str(S/'assets'/n) for n in ['photo_candidate_school_life_20261023.json','photo_candidate_school_life_bindings_20261023.json','photo_school_life_semantics_20261023.json','photo_candidate_school_appearance_poses_20261023.json','photo_candidate_school_appearance_poses_bindings_20261023.json','photo_school_appearance_poses_semantics_20261023.json']]+[str(S/'references'/n) for n in ['school-life-semantics.md','school-appearance-poses-semantics.md']]
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args,root=ROOT):return subprocess.check_output(['git',*args],cwd=root)
def owned(p):return p in OWN or any(p.startswith(str(PREFIX/t)+'/') for t in TOPICS)
def snapshot():
 CACHE.mkdir(parents=True,exist_ok=False)
 dirty=[x.decode() for x in git('diff','--name-only','-z').split(b'\0') if x]
 untracked=[x.decode() for x in git('ls-files','--others','--exclude-standard','-z').split(b'\0') if x]
 protected={}
 for rel in sorted(set(dirty+untracked+[str(S/'retrieval-runtime.json')])):
  if owned(rel):continue
  p=ROOT/rel
  protected[rel]={'state':'symlink','target':os.readlink(p)} if p.is_symlink() else {'state':'file','sha256':sha(p)} if p.is_file() else {'state':'missing'}
 index=Path(git('rev-parse','--git-path','index').decode().strip());index=index if index.is_absolute() else ROOT/index
 shutil.copyfile(index,CACHE/'primary-index.before')
 info={'HEAD':git('rev-parse','HEAD').decode().strip(),'branch':git('branch','--show-current').decode().strip(),'index_sha256':sha(index),'staged_names':git('diff','--cached','--name-only').decode().splitlines(),'protected':protected}
 assert info['staged_names']==[], 'Unexpected staged work; preserve it explicitly before publication'
 write(CACHE/'primary-before.json',info)
 write(WT/PUB/'primary-protection-before.json',{'HEAD':info['HEAD'],'protected_paths':len(protected),'staged_paths':0,'protected_inventory_sha256':sha(CACHE/'primary-before.json'),'scope':'Unrelated dirty/untracked bytes, deletions and runtime selection protected; private full inventory stays outside publication.'})
 print('protected paths',len(protected),flush=True)

def copy_scope():
 mapping=[];excluded=[]
 def copy(src,rel):
  if not src.is_file() or src.is_symlink():return
  data=src.read_bytes();dst=WT/rel;compressed=len(data)>1024*1024 and src.suffix in ['.json','.ndjson','.txt','.z']
  if compressed:dst=dst.with_name(dst.name+'.gz');payload=gzip.compress(data,mtime=0)
  else:payload=data
  dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(payload)
  assert (gzip.decompress(dst.read_bytes()) if compressed else dst.read_bytes())==data
  mapping.append({'original':str(src),'published':str(dst.relative_to(WT)),'original_sha256':hashlib.sha256(data).hexdigest(),'published_sha256':sha(dst),'compression':'gzip' if compressed else 'none'})
 for topic in TOPICS:
  q=ROOT/PREFIX/topic
  for p in sorted(q.rglob('*')):
   if not p.is_file() or p.is_symlink():continue
   rel=p.relative_to(q)
   if 'publication-evidence' in rel.parts:continue
   reason=None
   if set(rel.parts)&{'build','successor-store','successor-skill','__pycache__','.staging'}:reason='duplicate build/source/store or transient bytecode'
   if p.name in ['fashion-source.pdf','fashion-source.txt']:reason='temporary full publisher download; URL and content hash retained, no full-source republication'
   if p.name=='git-status-observed.z':reason='private unrelated-checkout observation; not research evidence'
   if 'LOCK' in p.name or p.suffix in ['.lock','.pyc','.tmp','.partial']:reason='transient'
   if reason:
    excluded.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p) if p.name in ['fashion-source.pdf','fashion-source.txt'] else None,'reason':reason});continue
   copy(p,PREFIX/topic/rel)
  for rel in ['successor.json','native-staged.json']:
   rp=q/'integration-evidence'/rel
   if not rp.exists():continue
   r=json.loads(rp.read_bytes());store=Path(r.get('store',str(q/'integration-evidence/successor-store')))
   for parent,k in [('h-f2-generations','generation_id'),('generations','native_generation_id')]:
    if r.get(k):
     f=store/parent/r[k]/'manifest.json'
     if f.exists():copy(f,PREFIX/topic/'integration-evidence/release-seals'/parent/r[k]/'manifest.json')
 for topic in TOPICS:
  for arm in 'abc':
   name=topic+'-'+arm;run=ROOT/'generated/photo-runs'/name
   if not run.exists():continue
   for p in sorted(run.rglob('*')):
    rel=p.relative_to(run)
    if set(rel.parts)&{'.staging','__pycache__'} or 'LOCK' in p.name or p.suffix in ['.pyc','.tmp','.partial']:continue
    copy(p,PREFIX/topic/'image-test-evidence'/arm/rel)
   outside=ROOT/'generated/images'/name
   if outside.exists():
    for p in sorted(outside.rglob('*')):copy(p,PREFIX/topic/'image-test-evidence'/arm/'native-images'/p.relative_to(outside))
 for rel in OWN:
  src=ROOT/rel;dst=WT/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);assert sha(src)==sha(dst)
 manifest=WT/S/'assets/photo_candidate_corpus_manifest.json';body=json.loads(manifest.read_bytes())
 for name,kind in [('photo_candidate_school_life_20261023.json','candidates'),('photo_candidate_school_life_bindings_20261023.json','slot_bindings'),('photo_candidate_school_appearance_poses_20261023.json','candidates'),('photo_candidate_school_appearance_poses_bindings_20261023.json','slot_bindings')]:
  row={'file':name,'kind':kind};assert row not in body['modules'];body['modules'].append(row)
 write(manifest,body)
 local=(ROOT/S/'references/maintenance.md').read_text();start=local.index('The [school-life extension]');end=local.index('The [Gaslamp Fantasy extension]',start);suffix=local[start:end].rstrip()+'\n'
 maintenance=WT/S/'references/maintenance.md';prior=maintenance.read_text();assert 'The [school-life extension]' not in prior;maintenance.write_text(prior.rstrip()+'\n\n'+suffix)
 write(WT/PUB/'PATH-MAP.json',{'schema':'school-life-publication-path-map/v1','historical_bytes_preserved':True,'source_reference_image_not_copied':True,'mappings':mapping})
 write(CACHE/'excluded-copy-inventory.json',excluded)
 write(WT/PUB/'archive-summary.json',{'published_evidence_files':len(mapping),'uncompressed_original_bytes':sum(Path(r['original']).stat().st_size for r in mapping),'large_duplicate_build_roots_excluded':True,'full_downloads_excluded':[x for x in excluded if 'publisher download' in x['reason']],'cleanup_requires_remote_push_proof':True,'old_pixel_outcomes':'all three FAIL','new_pixel_outcomes':'A/B FAIL, C PASS','new_data_final_influence':0})
 paths=[str(p.relative_to(WT)) for p in WT.rglob('*') if p.is_file() and not p.is_symlink() and (any(str(p.relative_to(WT)).startswith(str(PREFIX/t)+'/') for t in TOPICS))]+OWN+[str(S/'assets/photo_candidate_corpus_manifest.json'),str(S/'references/maintenance.md')]
 write(CACHE/'initial-allowlist.json',sorted(set(paths)))
 print('copied evidence',len(mapping),'allowed files',len(set(paths)),flush=True)
if __name__=='__main__':
 if sys.argv[1]=='snapshot':snapshot()
 elif sys.argv[1]=='copy':copy_scope()
