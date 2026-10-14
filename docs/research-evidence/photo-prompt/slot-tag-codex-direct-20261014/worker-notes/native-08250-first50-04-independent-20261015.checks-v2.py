"""Read-only structural and isolated synthetic consumer checks; no semantic status inference."""
import sys,json,gzip,copy,hashlib,os
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/07143a62ae23201a5cceedf155a985e204256740da96fc083e703d8ac5e7ba07')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n,photo_candidate_realizations as real
assert hashlib.sha256(Path(n.__file__).read_bytes()).hexdigest().startswith('7d9f7e7c')
B=R/'native_batches/review11870-01250-01300-04';D=R/'native-inputs/prepared/review11870-01250-01300-04'
b=json.loads((B/'BATCH.json').read_text());i=json.loads((D/'INPUT.json').read_text());s=json.loads(gzip.decompress(Path(i['current_snapshot']['file']).read_bytes()));cat=i['catalog_review']['after']
assert c.digest(b)=='4d55aef65775e0dc7f85e3446196195be8875b6700c590f3e5894620b0259c94'
checks=[];conflicts=[];allgroups=0
for row in b['records']:
 assert row['source_after']==s['candidates'][row['candidate_id']]
 if row['proof'] is None:assert row['status']=='pending';continue
 rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=row['proof'];before=c.digest(row['proof'])
 try:n.validate(rec,cat,catalog_sha256=c.digest(cat),corpus=s);n.compact(rec,corpus=s);checks.append({'ordinal':row['ordinal'],'full_validate_and_compact':True})
 except Exception as e:checks.append({'ordinal':row['ordinal'],'full_validate_and_compact':False,'error':type(e).__name__+': '+str(e)})
 assert before==c.digest(row['proof'])
 s['candidates'][row['candidate_id']]=rec
 groups={}
 for f in row['proof']['facts']:
  if f['mode']!='effect':continue
  key=(f['realization_id'],f['dimension'],f['target'],f['property']);val=c.digest({'value':f['value'],'operation':f['operation'],'receivers':f['receivers']})
  groups.setdefault(key,{}).setdefault(val,[]).append(f['id'])
 allgroups+=len(groups)
 for key,v in groups.items():
  if len(v)>1:conflicts.append({'ordinal':row['ordinal'],'group':list(key),'assignments':v})
# Independently authored actual owners/requirements, not generated from candidate proof.
def core(text,owners,values,relations,opened):
 def a(aid,kind,d='subject',**axes):return {'assertion_id':aid,'dimension':d,'polarity':'required','source_span_ids':['independent_fixture'],'affected_dimensions':[d],'axes':{'native_schema':'photo-frozen-semantics/v1','kind':kind,**axes},'evidence':{'meaning':text}}
 assertions=[a('o'+str(z),'owner',owner=x,owner_kind='entity')for z,x in enumerate(owners)]+[a('f'+str(z),'fact',d,owner=x,property=p,value_type=t,value=v)for z,(d,x,p,t,v)in enumerate(values)]+[a('r'+str(z),kind,left=l,right=r)for z,(kind,l,r)in enumerate(relations)]
 return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,'request_binding':{'active_spans':[{'source_span_id':'independent_fixture','text':text}]},'semantic_assertions':assertions,'user_exclusions':[],'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':['concept','count','event','identity','subject'],'open_dimensions':opened,'semantic_anchors':[]}}
text='Independent synthetic request: existing skin regions R and Y are skin, both distinct actual parts of same existing owner O. Existing mug M and actual hands A and B, distinct hands of existing holder H; mug distinct from each hand. No heat, holding, wrapping, aged or young appearance fixed in advance. Not a real requester.'
sk=core(text,['R','Y','O'],[('subject',x,'entity.presence','entity.presence/v1','present')for x in ['R','Y','O']]+[('subject',x,'body.region.kind','body.region.kind/v1','skin')for x in ['R','Y']],[('part_of','R','O'),('part_of','Y','O'),('disjoint','R','Y')],['appearance','age'])
mg=core(text,['M','A','B','H'],[('subject',x,'entity.presence','entity.presence/v1','present')for x in ['M','A','B','H']]+[('subject','M','props.type','props.type/v1','mug')]+[('subject',x,'entity.type','entity.type/v1','hand')for x in ['A','B']],[('part_of','A','H'),('part_of','B','H'),('disjoint','A','B'),('disjoint','M','A'),('disjoint','M','B')],['action','material','relationship'])
controls=[]
def run(o,k,bindings,label,want):
 row=next(x for x in b['records']if x['ordinal']==o);e=c.entry(s,row['candidate_id'],realization_id='base');k=copy.deepcopy(k);k['canonical_sha256']=c.digest(k);g=n.frozen_witnesses(k)['graph'];e['_native_owner_selections']={'schema':n.OWNER_SELECTION_SCHEMA,'core_sha256':k['canonical_sha256'],'owner_graph_sha256':c.digest(g),'entries':[{'candidate_id':e['id'],'realization_id':'base','meaning_sha256':row['proof']['meaning_sha256'],'qualification_sha256':c.digest(row['proof']),'bindings':[{'target':t,'owner_id':v}for t,v in bindings]}]}
 for view in ['full','compact']:
  z=copy.deepcopy(e);z.pop('_semantic_evidence_guard'if view=='full'else'role_evidence',None);got=n.admission(z,k);controls.append({'ordinal':o,'case':label,'view':view,'want':want,'got':got,'pass':got['allowed']==want})
SB=[('aged_region','R'),('young_region','Y'),('aged_owner','O'),('young_owner','O')];MB=[('mug','M'),('hand_a','A'),('hand_b','B'),('holder','H')]
for o,k,bind in [(1295,sk,SB),(1296,mg,MB)]:
 run(o,k,bind,'actual_independent_open',True)
 z=copy.deepcopy(k);z['semantic_assertions']=[a for a in z['semantic_assertions']if a['axes']['kind']!='disjoint'];run(o,z,bind,'missing_distinctness',False)
 z=copy.deepcopy(k);z['semantic_assertions']=[a for a in z['semantic_assertions']if a['axes']['kind']!='part_of'];run(o,z,bind,'missing_owned_parts',False)
 z=copy.deepcopy(k);next(a for a in z['semantic_assertions']if a['axes']['kind']=='fact')['axes']['owner']='Y'if o==1295 else'A';run(o,z,bind,'required_presence_wrong_owner',False)
 for dim in k['intent_lock']['open_dimensions']:
  z=copy.deepcopy(k);z['intent_lock']['open_dimensions'].remove(dim);z['intent_lock']['locked_dimensions'].append(dim);run(o,z,bind,'locked_'+dim,False)
# Research verifier is repository tooling; semantic/corpus/realization imports stay exact published generation.
sys.path.append(str(R));import direct_review as dr;sys.path[:0]=[str(G/'scripts'),str(G/'precore')];import native_reviews as nr
try:batch_result={'ok':True,'result':nr.verify_batch(D/'ASSIGNMENT.json',B/'BATCH.json',B/'NOTE.json',root=ROOT,here=R)}
except Exception as e:batch_result={'ok':False,'error':type(e).__name__+': '+str(e)}
mods={}
for name,m in sorted(sys.modules.items()):
 f=getattr(m,'__file__',None)
 if f and(name.startswith('photo_')or name in ['native_reviews','direct_review']):
  p=Path(f).resolve()
  if name not in ['native_reviews','direct_review']:assert p.is_relative_to(G),(name,p)
  mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out={'schema':'photo-native-independent-checks/v1','task':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high','frozen_generation':str(G),'modules':mods,'fullproof_structural_results':checks,'canonical_E_groups':allgroups,'conflicting_E_groups':conflicts,'isolated_controls':controls,'controls_all_passed':all(x['pass']for x in controls),'verify_batch_actual_files':batch_result,'os_network_denied':True,'provider_keys_absent':all(not os.environ.get(x)for x in ['GEMINI_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY','ANTHROPIC_API_KEY']),'semantic_accuracy_inferred_from_checks':False,'original_artifact_mutations':0}
f=R/'worker-notes/native-08250-first50-04-independent-20261015.checks-v2.json';assert not f.exists();f.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'structural':len(checks),'structural_errors':[x for x in checks if not x['full_validate_and_compact']],'Egroups':allgroups,'conflicts':conflicts,'controls':len(controls),'control_errors':[x for x in controls if not x['pass']],'verify_batch':batch_result,'result_sha256':hashlib.sha256(f.read_bytes()).hexdigest()},ensure_ascii=False))
