"""Root rerun of the actual seven-source checks plus every precise effect property."""
import copy,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama'}:raise AssertionError('model/API import forbidden: '+fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_embedding_provider as provider,photo_local_embedding as local

def no_inference(*args,**kwargs):raise AssertionError('model inference forbidden')
provider.embed=provider.embed_many=local.infer=no_inference
p=R/'authored/native_06250_first20_149_02.check.py';code=p.read_text();assert "out={'schema':"in code
ns={'__file__':str(p),'__name__':'root_reviewed_worker_rerun'};exec(compile(code.split("out={'schema':",1)[0],str(p),'exec'),ns)
c=ns['c'];e=ns['e'];g=ns['g'];layout=ns['layout'];S=ns['S'];B=ns['B'];fixture=ns['fixture'];extra=[];qualified=[]
for row in B['records']:
 if row['proof']is None:continue
 cid=row['candidate_id'];rec=copy.deepcopy(row['source_after']);rec['content']['role_evidence']=copy.deepcopy(row['proof']);data={**S,'candidates':{**S['candidates'],cid:rec}};role=next(iter(row['proof']['roles']));actualrole=row['proof']['owner_maps']['base']['bindings'][0]['core_role'];dim=row['proof']['facts'][0]['dimension'];bid=next(k for k,v in S['slot_bindings'].items()if v['candidate_id']==cid)
 for label in ['full','compact']:
  view=data if label=='full'else{**data,'candidates':{**data['candidates'],cid:layout.guard_record(rec,data)}}
  q=e.qualification(S['slot_catalog'][role],view['candidates'][cid],source_data=data);assert q['status']=='eligible';qualified.append({'ordinal':row['ordinal'],'view':label,'role':role,'full_source_authority_qualification':q})
  for binding in [None,bid]:
   entry=c.entry(view,cid,binding,realization_id='base');core=fixture(dim,actualrole);dims,properties,graph=e.permission_scope(entry,core)
   for atom in properties:
    for alias in [False,True]:
     locked=fixture(dim,actualrole,anchor=('locked_alias'if alias else atom['target'],atom['property']),alias=alias);assert not e.property_scope_allowed(locked,dims,properties,record=entry);assert not g.core_entry_eligible(view,locked,ns['contract'],ns['picked'],role,entry)
     extra.append({'ordinal':row['ordinal'],'view':label,'binding_id':binding,'property':atom,'exact_alias':alias,'property_scope_and_consumer_denied':True})
assert len(ns['results'])==7 and sum(len(x['matrix'])for x in ns['results'])==28 and len(extra)==72
mods={k:str(Path(v.__file__).resolve())for k,v in sys.modules.items()if k.startswith('photo_')and getattr(v,'__file__',None)};assert all(Path(x).is_relative_to(G)for x in mods.values())
report={'schema':'photo-root-first20-seven-source-controlled-check/v1','actor':'/root','worker_script':str(p.relative_to(ROOT)),'worker_script_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'worker_authored_matrix_root_rerun':ns['results'],'matrix_count':28,'root_added_every_actual_property_and_alias_checks':extra,'root_added_property_check_count':72,'source_qualification_full_authority':qualified,'batch_shape':{k:v for k,v in ns['verified'].items()if k!='records'},'all_passed':True,'module_paths':mods,'OS_network_denied':True,'model_provider_Gemini_calls':0,'operating_changes':0,'root_acceptance_written':False,'boundary':'Root personally reads all20 original/current sources, all7 native payloads9facts14units, and9 full149 specs. Worker20exact5B/provenance/full44spec reads are delegated evidence, not root personal new reads. Root reruns28 reviewed worker-authored matrices and adds72 exact/alias checks covering every actual property including both lens effects. This is controlled synthetic input, no real request/hybrid retrieval/compose/runtime/pixels.'}
out=R/'ROOT-FIRST20-149-CONSUMER-CHECK-01.json'
with out.open('x')as f:json.dump(report,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'worker_matrices_root_rerun':28,'additional_all_actual_property_alias_checks':72,'approved_shape':7,'pending_shape':13,'Gemini_calls':0}))
