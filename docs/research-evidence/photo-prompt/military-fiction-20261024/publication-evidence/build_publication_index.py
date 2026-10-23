"""Rebuild only derived data with the merged checkout's compatible recipe."""
import gc;gc.disable()
from pathlib import Path
import json,sys,shutil,time
ROOT=Path(__file__).resolve().parents[5];S=ROOT/'skills/photo-prompt-image-generator';A=S/'assets';O=Path(__file__).resolve().parent;CACHE=Path(sys.argv[1]);sys.path.insert(0,str(S/'scripts'))
import photo_candidate_corpus as c
import photo_search_layout as layout
from build_shared_candidate_index import build
from photo_local_embedding import close_worker
from photo_runtime_sources import source_update
from validate_photo_prompt_dictionary import validate_source_corpus

def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
t=time.monotonic();before=json.loads((A/layout.MANIFEST).read_bytes());corpus=c.load(A);c.validate(corpus);del corpus;gc.collect()
with source_update(S,CACHE/'source-guard'):
 result=build(A,CACHE,space=json.loads((S/'embedding-runtime.lock.json').read_bytes())['space'])
close_worker();gc.collect();write(O/'index-build.json',result)
current=json.loads((A/layout.MANIFEST).read_bytes());corpus=c.load(A);verified=layout.verify(A,corpus,current);write(O/'index-closure.json',verified)
errors=validate_source_corpus(S,corpus);write(O/'dictionary-validation.json',{'status':'pass' if not errors else 'fail','errors':errors});assert not errors,errors
if before['layout_id']!=current['layout_id']:
 old=A/'photo_candidate_search_shards'/before['layout_id'];assert before['layout_id'] not in json.dumps(current)
 if old.exists():shutil.rmtree(old)
write(O/'index-publication.json',{'status':'pass','source_union_rebuilt':True,'old_layout':before['layout_id'],'new_layout':current['layout_id'],'compatible_recipe':True,'installed_runtime_selection_changed':False,'superseded_worktree_derived_layout_removed':before['layout_id']!=current['layout_id'],'elapsed_seconds':round(time.monotonic()-t,3)})
print(json.dumps(result),flush=True)
