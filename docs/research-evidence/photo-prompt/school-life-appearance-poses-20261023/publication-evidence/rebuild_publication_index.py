"""Validate a source union and rebuild with its own checked-out recipe."""
import gc;gc.disable()
import json,sys,subprocess,hashlib,shutil,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';O=Path(__file__).resolve().parent
CACHE=Path('/Users/chasoik/.cache/image-prompt/school-life-publication-20261023-01a1678d')
sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
from photo_runtime_sources import source_update
from build_shared_candidate_index import build
from photo_local_embedding import close_worker
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
def main():
 t=time.monotonic();before=read(A/'photo_candidate_search.json');oldid=before['layout_id']
 base=git('rev-parse','HEAD').decode().strip();base_manifest=json.loads(git('show',base+':skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json'))
 checked=[]
 for m in base_manifest['modules']:
  rel='skills/photo-prompt-image-generator/assets/'+m['file'];old=git('show',base+':'+rel);actual=(ROOT/rel).read_bytes()
  assert actual==old, 'Existing module bytes modified: '+rel
  checked.append({'file':m['file'],'sha256':hashlib.sha256(old).hexdigest()})
 corpus=c.load(A);c.validate(corpus);modules=['photo_candidate_school_life_20261023.json','photo_candidate_school_appearance_poses_20261023.json'];fresh={}
 for m in modules:
  rows=read(A/m)['candidates'];assert set(fresh).isdisjoint(rows);fresh.update(rows)
 assert len(fresh)==258 and sum(r['record_kind']=='visual_option' for r in fresh.values())==206
 assert sum(r['record_kind']=='diagnostic' for r in fresh.values())==52
 write(O/'source-preservation.json',{'status':'pass','base_commit':base,'existing_module_bytes_preserved':len(checked),'modules':checked,'new_school_CIDs':258,'new_visual_options':206,'new_excluded_diagnostics':52,'total_candidates':len(corpus['candidates']),'total_bindings':len(corpus['slot_bindings']),'corpus_sha256':c.digest(corpus),'schema':read(A/c.MANIFEST_NAME)['schema']})
 del corpus;gc.collect()
 with source_update(S,CACHE/'runtime-source-guard'):
  result=build(A,CACHE/'index-build',space=read(S/'embedding-runtime.lock.json')['space'])
 close_worker();gc.collect();write(O/'index-build.json',result)
 new=read(A/'photo_candidate_search.json');assert new['layout_id']==result['layout_id']
 if oldid!=new['layout_id']:
  olddir=A/'photo_candidate_search_shards'/oldid
  assert not any(oldid in str(v) for v in new.values()),'Old layout still referenced'
  if olddir.exists():shutil.rmtree(olddir)
 write(O/'index-publication.json',{'status':'pass','source_union_rebuilt':True,'old_layout':oldid,'new_layout':new['layout_id'],'embedding_space':new['space'],'foreign_recipe_relabelled':False,'installed_runtime_selection_changed':False,'superseded_worktree_layout_removed':oldid!=new['layout_id'],'elapsed_seconds':time.monotonic()-t})
 print(json.dumps(result),flush=True)
if __name__=='__main__':main()
