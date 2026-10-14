"""Root rerun of reviewed exact actual-source repair tests, with models and network denied."""
import copy,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama'}:raise AssertionError('model/API import forbidden: '+fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_embedding_provider as provider,photo_local_embedding as local
def no_inference(*args,**kwargs):raise AssertionError('model inference forbidden')
provider.embed=provider.embed_many=local.infer=no_inference
path=R/'native_batches/review11870-01250-01300-06/check_1255_v1.py';code=path.read_text();assert "out={'schema':"in code
ns={'__file__':str(path),'__name__':'root_actual_source_controlled_rerun'};exec(compile(code.split("out={'schema':",1)[0],str(path),'exec'),ns)
assert len(ns['checks'])==66
sys.path.insert(0,str(R));import native_reviews as nr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
D=R/'native-inputs/prepared/review11870-01250-01300-06';O=R/'native_batches/review11870-01250-01300-06'
verified=nr.verify_batch(D/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json',root=ROOT,here=R)
a=json.loads((R/'native_batches/review11870-01250-01300-05/BATCH.json').read_bytes());b=json.loads((O/'BATCH.json').read_bytes());assert c.digest(a)=='0666d0c5035fac8818e95d818014e158336d1c04d4226a34064eee9ad1c77e90'and c.digest(b)=='1608aaf83463aaaf9150b49938e8b119c051aefa3b64139686e8ec23cc5f8203'
assert [i for i,(x,y)in enumerate(zip(a['records'],b['records']))if x!=y]==[5]
x=a['records'][5];y=b['records'][5]
for k in set(x)-{'proof','rationale','revision'}:assert x[k]==y[k]
p=x['proof'];q=y['proof'];assert q['facts']==[f for f in p['facts']if f['id']!='nearEn']
assert all(p[k]==q[k]for k in set(p)-{'facts','source_units','roles','review'})
expectedroles=copy.deepcopy(p['roles']);expectedroles['prop_placement']['fact_refs'].remove('nearEn');assert expectedroles==q['roles']
assert q['source_units'][0]=={**p['source_units'][0],'fact_refs':['holdingEn','neutralEn']};assert q['source_units'][1:3]==p['source_units'][1:3]
u=q['source_units'][3];assert u['disposition']=='semantic_reference'and u['reference_relation']=='partial_restatement'and u['pointer']=='/content/en'and u['fact_refs']==['nearApp']and u['quote']==y['source_after']['content']['en']
assert verified['statuses']=={'approved':49,'diagnostic_reviewed':0,'pending':1}
assert not (R/'native_batches/review11870-01250-01300-05/ROOT-ACCEPTANCE.json').exists()
mods={k:{'file':str(Path(v.__file__).resolve()),'file_sha256':hashlib.sha256(Path(v.__file__).read_bytes()).hexdigest()}for k,v in sys.modules.items()if k.startswith('photo_')and getattr(v,'__file__',None)};assert all(Path(v['file']).is_relative_to(G)for v in mods.values())
report={'schema':'photo-root-actual-source-field-repair-check/v1','actor':'/root','worker_script_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'controlled_checks':ns['checks'],'controlled_check_count':66,'actual_property_count':len(ns['props']),'qualification':ns['qualifications'],'same_source_batch_shape':{k:verified[k]for k in ['assignment_sha256','input_sha256','batch_sha256','note_sha256','prepared_count','actual_read_count','statuses','shape_valid']},'unchanged_complete_rows':49,'unchanged_proofs_resigned':0,'changed_source_records':0,'changed_native_row':1255,'literal_repair_assertions_passed':True,'module_paths':mods,'OS_network_denied':True,'model_provider_Gemini_calls':0,'root_acceptance_written':False,'operating_changes':0,'boundary':'Root reruns the reviewed worker-authored66 controlled full/compact actualsource1255 assertions and literal repair invariants; this is not an independently authored new66case suite, actual user request, final hybrid search/compose/runtime or pixels. Prior49 exactrow source/spec/consumer evidence is retained with no claim to49new source reads.'}
out=R/'ROOT-FIRST50-1255-CONSUMER-CHECK-01.json'
with out.open('x')as f:json.dump(report,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
print(json.dumps({'controlled_checks':66,'unchanged_complete_rows':49,'batch_statuses':verified['statuses'],'native_facts':sum(len(z['proof']['facts'])for z in b['records']if z['proof']),'root_acceptance_written':False,'operating_changes':0,'Gemini_calls':0}))
