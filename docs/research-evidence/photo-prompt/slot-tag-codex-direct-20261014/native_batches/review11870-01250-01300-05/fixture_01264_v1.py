"""Literal independent synthetic fixtures only; no runtime/requester assertion or source change."""
import sys,json,copy,hashlib,importlib.abc
from pathlib import Path
sys.dont_write_bytecode=True
class DenyModels(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'photo_local_embedding','torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic'}:raise RuntimeError('Forbidden model/provider import: '+fullname)
sys.meta_path.insert(0,DenyModels())
O=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014/native_batches/review11870-01250-01300-05');R=O.parent.parent;G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n,prompt_generator as generator
TEXT='Independent synthetic request declares existing chair C and actual existing seat part S of that same chair. Exact chair type and exact seat-part kind are separately frozen. S part_of C is explicit, with separate actual scopes and no equivalence. Chair orientation, seat disturbed state and recent prior-disturbance history are not already frozen. Pose, role and timing selections are explicitly open. This is only an isolated test request, not a real requester/runtime assertion.'
def core():
 def a(aid,kind,d='subject',**axes):return {'assertion_id':aid,'dimension':d,'polarity':'required','source_span_ids':['independent_request'],'affected_dimensions':[d],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':TEXT}}
 return {'contract_version':'photo-authorial-core/v3','subject':TEXT,'baseline_prompt_en':TEXT,'request_binding':{'active_spans':[{'source_span_id':'independent_request','text':TEXT}]},'semantic_assertions':[a('chair_owner','owner',owner='C',owner_kind='object'),a('seat_owner','owner',owner='S',owner_kind='object'),a('chair_presence','fact',owner='C',property='entity.presence',value_type='entity.presence/v1',value='present'),a('seat_presence','fact',owner='S',property='entity.presence',value_type='entity.presence/v1',value='present'),a('chair_type','fact',owner='C',property='props.type',value_type='props.type/v1',value='chair'),a('seat_type','fact',owner='S',property='object.part.kind',value_type='object.part.kind/v1',value='seat'),a('actual_seat_of_same_chair','part_of',left='S',right='C')],'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject'],'open_dimensions':['pose','role','timing'],'semantic_anchors':[]}}
def delete(k,aid):
 v=copy.deepcopy(k);v['semantic_assertions']=[a for a in v['semantic_assertions']if a['assertion_id']!=aid];return v
def alter(k,aid,**axes):
 v=copy.deepcopy(k);next(a for a in v['semantic_assertions']if a['assertion_id']==aid)['axes'].update(axes);return v
def ent(S,cid,binding=True,view='full'):
 bid='bind_'+cid[5:] if binding else None;e=c.entry(S,cid,bid,realization_id='base');e.pop('_semantic_evidence_guard' if view=='full' else 'role_evidence',None);return e
def select(e,k,p,bindings=None):
 v=copy.deepcopy(k);v.pop('canonical_sha256',None);v['canonical_sha256']=c.digest(v);g=n.frozen_witnesses(v)['graph'];z=copy.deepcopy(e);z['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':v['canonical_sha256'],'owner_graph_sha256':c.digest(g),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':t,'owner_id':owner}for t,owner in (bindings or [('chair','C'),('seat','S')])]}]};return z,v
def contract(category='human',domains=None):return {'subject_category':category,'domains':domains or [],'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':domains or []}}
def picked(category='human'):return {'subject':{'kind':[category],'tags':[category]}}
def modules():
 out={}
 for name,m in sorted(sys.modules.items()):
  if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
   p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);out[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 return out
