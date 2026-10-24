"""Resume this task's failed layout revision; complete only its exact token."""
import gc,json,sys
from pathlib import Path
gc.disable()
S=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator');O=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'scripts'))
from photo_runtime_sources import _pointer_directory,default_store,complete_source_update
from build_shared_candidate_index import build
from photo_local_embedding import space
P=_pointer_directory(Path(default_store()),S,'local_current')/'SOURCE.json'
prior=json.loads(P.read_bytes());assert prior=={'editing':'4fcef7330ac945dfa64ee1030a9aa959','epoch':173},'Maintenance ownership changed; do not clear it'
(O/'working-index-repair-ownership.json').write_text(json.dumps({'prior':prior,'source_path':str(P),'evidence':'Revision timestamp 01:36:50 agrees with this task first build; first build failed 01:42:55 with source changed before layout activation. Its context intentionally retained pending token. Rebuild attempt 01:45 rejected before entering. Exact token required at completion.'},indent=2)+'\n')
result=build(S/'assets',O/'working-index-cache',space=space(),batch_size=16)
complete_source_update(S,token=prior['editing'])
(O/'working-index-final.json').write_text(json.dumps({'status':'pass','build':result,'completed_own_revision_token':prior['editing'],'source_after':json.loads(P.read_bytes())},indent=2)+'\n')
print(json.dumps(result),flush=True)
