"""Offline frozen-runtime research harness; no provider/model execution or operating writes."""
import copy,datetime,gzip,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path('/Users/chasoik/Projects/image-prompt');R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';O=Path(__file__).resolve().parent
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class DenyModels(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama'}:raise AssertionError('model/provider import forbidden: '+fullname)
sys.meta_path.insert(0,DenyModels());sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import photo_semantic_role_views as v
import photo_candidate_realizations as real
# direct_review prepends working scripts, so preload all frozen modules before research helper and restore priority.
import direct_review as dr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import native_reviews as nr
D=R/'native-inputs/prepared/review12250-expression5-149-01';A=json.loads((D/'ASSIGNMENT.json').read_text());I=nr.artifact(ROOT,A['input']);S=nr.artifact(ROOT,I['current_snapshot']);ORIGINAL=nr.artifact(ROOT,I['original_snapshot']);PACK=json.loads((D/'PREPARED-PACKET.json').read_text());PLAN=json.loads((R/'authored/native_12250_approval_pilot149_source25_plan_05.json').read_text());CAT=S['slot_catalog'];CH=c.digest(CAT)
assert c.digest(S)=='d353a2f3282415e682fb6623aa34f395c82d20f2310ce77fbec3bea592360f05';assert CH=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15';assert c.digest(PLAN)=='644991678f9a8241de3cea3d476b71787ebd0c85dfdbe1a81b6271227fa92185'
for p in PLAN['records']:
 cid=p['candidate_id'];assert S['candidates'][cid]==p['after'];assert PACK['current_records'][cid]==p['after'];assert {k:b for k,b in S['slot_bindings'].items() if b['candidate_id']==cid}==p['own_bindings'];assert n.referenced_records(p['after'],S)=={}
def save(path,value):
 with path.open('x') as f:json.dump(value,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
def modules():
 out={}
 for name,m in sys.modules.copy().items():
  if (name.startswith('photo_') or name in ['prompt_generator','direct_review','native_reviews']) and getattr(m,'__file__',None):
   p=Path(m.__file__).resolve();assert p.is_relative_to(G) or name in ['direct_review','native_reviews'];out[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 return out
