"""Lossless pure preparation for750 new146V5/current88614 draft records. No source read/semantic decision claim."""
import json,gzip,hashlib,copy,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';AD=R/'authored';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/e9a03bb489e8b03cb7846787fcbe6c0f6e6ede02ac106a998ecbc6c57f6e9942');FROZEN=[str(G/'scripts'),str(G/'precore')];sys.path[:0]=FROZEN
import photo_candidate_corpus as c
sys.path.insert(0,str(R));import direct_review as dr
sys.path=[p for p in sys.path if p not in [str(dr.SKILL/'scripts'),str(R)]];sys.path[:0]=FROZEN
import photo_candidate_realizations as rr
import photo_semantic_evidence as ne

def read(p):
 raw=Path(p).read_bytes();return json.loads(gzip.decompress(raw)if str(p).endswith('.gz')else raw)
def rel(p):return str(Path(p).relative_to(ROOT))
def pin(p):
 p=Path(p);raw=p.read_bytes();return {'file':rel(p),'file_sha256':hashlib.sha256(raw).hexdigest(),'sha256':c.digest(read(p))}
original=read(R/'SOURCE.json.gz');current=read(R/'native-inputs/11870-01250-01300-plan-04/CURRENT-PROPOSAL.json.gz');cat=read(R/'CATALOG-FINAL-146-V5.json');order=read(R/'ORDER.json')
assert c.digest(original)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b';assert c.digest(current)=='88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8';assert c.digest(cat)=='3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645';assert current['slot_catalog']==cat
allrows={};loc={};files=[]
for p in sorted((R/'decisions').glob('*.json')):
 raw=p.read_bytes();obj=json.loads(raw);fh=hashlib.sha256(raw).hexdigest();files.append({'file':rel(p),'file_sha256':fh,'sha256':c.digest(obj)})
 for idx,row in enumerate(obj['decisions']):
  cid=row['candidate_id'];assert cid not in allrows;allrows[cid]=row;loc[cid]={'file':rel(p),'file_sha256':fh,'item':idx+1,'pointer':'/decisions/'+str(idx),'row_sha256':c.digest(row)}
five=copy.deepcopy(original)
for cid,row in allrows.items():five['candidates'][cid]=dr.corrected_record(original['candidates'][cid],row['corrections'])
def named(v,table):
 if isinstance(v,str):return {v}if v in table else set()
 if isinstance(v,list):return set().union(*(named(x,table)for x in v))
 if isinstance(v,dict):return set().union(*(named(k,table)|named(x,table)for k,x in v.items()))
 return set()
def closure(s,cid):
 foundC={};foundB={};pendingC={cid};pendingB=set();own={k:v for k,v in s['slot_bindings'].items()if v['candidate_id']==cid};pendingB|=set(own)
 while pendingC or pendingB:
  while pendingC:
   k=pendingC.pop()
   if k in foundC:continue
   obj=s['candidates'][k];foundC[k]=obj;pendingC|=named(obj,s['candidates'])-set(foundC);pendingB|=named(obj,s['slot_bindings'])-set(foundB)
  while pendingB:
   k=pendingB.pop()
   if k in foundB:continue
   obj=s['slot_bindings'][k];foundB[k]=obj;pendingC|=named(obj,s['candidates'])-set(foundC);pendingB|=named(obj,s['slot_bindings'])-set(foundB)
 foundC.pop(cid);requiredB={k:v for k,v in foundB.items()if k not in own};return {'required_cid_records':dict(sorted(foundC.items())),'required_binding_definitions':dict(sorted(requiredB.items())),'own_bindings_full':own}
ids=order[1500:2250];records={}
for ordinal,cid in enumerate(ids,1500):
 old=original['candidates'][cid];cur=current['candidates'][cid];cor=five['candidates'][cid];row=allrows[cid]
 records[cid]={'ordinal':ordinal,'candidate_id':cid,'original_full':old,'original_sha256':c.digest(old),'actual_current_full':cur,'actual_current_sha256':c.digest(cur),'compiled5B_full':row,'compiled5B_locator':loc[cid],'corrected5B_full':cor,'corrected5B_sha256':c.digest(cor),'original_closure':closure(original,cid),'actual_current_closure':closure(current,cid),'corrected5B_closure':closure(five,cid),'original_actual_rids':rr.ids(old),'current_actual_rids':rr.ids(cur),'corrected5B_actual_rids':rr.ids(cor)}
modules={m.__name__:{'file':str(Path(m.__file__).resolve()),'file_sha256':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()}for m in [dr,c,rr,ne]};assert all(Path(modules[m.__name__]['file']).is_relative_to(G)for m in [c,rr,ne]);assert modules['photo_semantic_evidence']['file_sha256'].startswith('309876')
prior=[p for p in AD.glob('native_11870_01250_02250.01500_015*')if p.is_file()]
body={'schema':'photo-native-manual-bulk-lossless-preparation/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','range':[1500,2250],'ids':ids,'prepared_count':750,'actual_read_count':0,'completed_native_draft_count':0,'native_proofs':0,'signatures':0,'root_acceptance':0,'source_original':pin(R/'SOURCE.json.gz'),'source_current':pin(R/'native-inputs/11870-01250-01300-plan-04/CURRENT-PROPOSAL.json.gz'),'order':pin(R/'ORDER.json'),'catalog146V5':pin(R/'CATALOG-FINAL-146-V5.json'),'catalog_full':cat,'records':records,'compiled_artifact_pins':files,'preparation_module_paths_sha256':modules,'frozen_generation':str(G),'prior_WIP_preserved_only_not_current_completion':{'previous1500_1510':'Old144V4 first10 source assessment/facts WIP, after proposals not reread or completed. Not converted or counted as fresh146V5 completion. Old1500:1550 prepared file also preserved, no claim previously unprepared. New750 prepared only at this stage.','files':[{'file':rel(p),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in sorted(prior)]},'os_network_denied':True,'provider_keys_absent':True,'production_registration_assets_runtime_Git_model_network_calls':0,'boundary':'Lossless mechanical expansion only. Prepared750/read0; no semantic tags, ownership, fact mode, approval, proof or signature generated.'};f=AD/'native_11870_01500_02250.inputs-146v5.json';assert not f.exists();f.write_text(json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print('PREPARED750_READ0',c.digest(body),hashlib.sha256(f.read_bytes()).hexdigest(),f.stat().st_size);print('MODULES',json.dumps(modules,ensure_ascii=False));print('REF_COUNTS',sum(bool(v['actual_current_closure']['required_cid_records'])for v in records.values()),sum(bool(v['actual_current_closure']['required_binding_definitions'])for v in records.values()))
