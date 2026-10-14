"""Mechanical test serialization only; all fixture facts and expected decisions supplied literally by author."""
import json,gzip,copy,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'native_batches/review11870-01285-05';D=R/'native-inputs/prepared/review11870-01285-05';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/07143a62ae23201a5cceedf155a985e204256740da96fc083e703d8ac5e7ba07');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import prompt_generator as generator
I=json.loads((D/'INPUT.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()))
def make_core(text,owners,roles,values,relations,opendims,extra_locked=None,anchors=None):
 def a(aid,kind,d='subject',**axes):return {'assertion_id':aid,'dimension':d,'polarity':'required','source_span_ids':['fixture_request'],'affected_dimensions':[d],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':text}}
 rows=[a('o'+str(j),'owner',owner=x,owner_kind='entity')for j,x in enumerate(owners)]+[a('r'+str(j),'role',owner=x,role=role)for j,(role,x)in enumerate(roles)]+[a('f'+str(j),'fact',d,owner=x,property=p,value_type=t,value=v)for j,(d,x,p,t,v)in enumerate(values)]+[a('rel'+str(j),kind,left=l,right=r)for j,(kind,l,r)in enumerate(relations)]
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'fixture_request','text':text}]},'semantic_assertions':rows,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['age','concept','count','event','identity','subject']+(extra_locked or []),'open_dimensions':opendims,'semantic_anchors':anchors or []}}
def remove(k,kind,prop=None,owner=None):
 z=copy.deepcopy(k);z['semantic_assertions']=[x for x in z['semantic_assertions']if not(x['axes']['kind']==kind and(prop is None or x['axes'].get('property')==prop)and(owner is None or x['axes'].get('owner')==owner))];return z
def change(k,prop,val):
 z=copy.deepcopy(k);next(x for x in z['semantic_assertions']if x['axes'].get('property')==prop)['axes']['value']=val;return z
def entry(j,o,rid='base',binding=False):
 row=next(x for x in j['records']if x['ordinal']==o);rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];S['candidates'][row['candidate_id']]=rec;bids=[k for k,v in S['slot_bindings'].items()if v['candidate_id']==row['candidate_id']];return c.entry(S,row['candidate_id'],bids[0]if binding else None,realization_id=rid)
def selected(j,e,k,bindings):
 k=copy.deepcopy(k);k.pop('canonical_sha256',None);k['canonical_sha256']=c.digest(k);p=next(x['proof']for x in j['records']if x['candidate_id']==e['id']);g=n.frozen_witnesses(k)['graph'];z=copy.deepcopy(e);z['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(g),'entries':[{'candidate_id':e['id'],'realization_id':e['_realization_id'],'meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':t,'owner_id':v}for t,v in bindings]}]};return z,k
def contract(category,domains=None):return {'subject_category':category,'domains':domains or [],'adult_allowed':False,'intent_constraints':{'subject_categories':[category],'domains':domains or []}}
def picked(category):return {'subject':{'kind':[category],'tags':[category]}}
def modules():
 out={}
 for name,m in sorted(sys.modules.items()):
  if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
   p=Path(m.__file__).resolve();assert p.is_relative_to(G);out[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 return out
