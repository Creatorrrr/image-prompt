"""Mechanical immutable input preparation; no semantic judgements or approvals."""
import gzip,hashlib,json,re
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014')
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def info(p):return {'file':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'canonical_sha256':sha(read(p))}
currentp=R/'native-inputs/catalog149-source-pool-plan-09/CURRENT-PROPOSAL.json.gz';originalp=R/'SOURCE.json.gz';orderp=R/'ORDER.json';catalogp=R/'CATALOG-FINAL-149-V6.json'
current=read(currentp);original=read(originalp);order=read(orderp);catalog=read(catalogp)
assert sha(current)=='5ee63da71e477de1d52677fa768dd715eb6589c6f0f77ac213c11825b0c2fd44'
assert sha(catalog)=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
assert current['slot_catalog']==catalog and len(order)==18250 and len(set(order[10250:11250]))==1000
files=['review_09250_10500_10250_10500.json','review_03250_04250_10500_10750.json','review_03250_04250_10750_11000.json','review_03250_04250_11000_11250.json']
rows={}
for filename in files:
 p=R/'decisions'/filename;d=read(p)
 for i,x in enumerate(d['decisions']):
  if x['candidate_id'] in order[10250:11250]:
   assert x['candidate_id'] not in rows
   rows[x['candidate_id']]=(x,{'file':str(p),'pointer':'/decisions/'+str(i),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'row_sha256':sha(x)})
assert len(rows)==1000
provp=Path('docs/research-evidence/photo-prompt/slot-retrieval-stage05-20261012/CONTROLLED-FINAL-SOURCE.json');prov=read(provp)
def values(x):
 if isinstance(x,str):yield x
 elif isinstance(x,dict):
  for v in x.values():yield from values(v)
 elif isinstance(x,list):
  for v in x:yield from values(v)
def refs(record):
 ids=set();bs={}
 for text in values(record):
  if re.fullmatch(r'cand_[a-f0-9]{32}',text) and text!=record['id']:ids.add(text)
  if re.fullmatch(r'bind_[a-f0-9]{32}',text):
   b=current['slot_bindings'].get(text);bs[text]=b
   if b and b['candidate_id']!=record['id']:ids.add(b['candidate_id'])
 return ids,bs
records=[]
for ordinal in range(10250,11250):
 cid=order[ordinal];a=original['candidates'][cid];b=current['candidates'][cid];five,locator=rows[cid]
 direct,bs=refs(b);closure={};queue=list(direct)
 while queue:
  ref=queue.pop()
  if ref==cid or ref in closure:continue
  item=current['candidates'].get(ref);closure[ref]=item
  if item:
   child,bindings=refs(item);bs.update(bindings);queue.extend(child-set(closure))
 provenances=[]
 for p in a['provenance']:
  source=p['source'];match=re.fullmatch(r'slot:([^:]+):(.+)',source)
  found=[]
  if match:
   group,entryid=match.groups();container=prov['slots'].get(group,[])
   if isinstance(container,list):found=[(i,x) for i,x in enumerate(container) if x.get('id')==entryid]
  provenances.append({'declared':p,'matches':[{'pointer':'/slots/'+match.group(1)+'/'+str(i),'entry':x,'entry_sha256':sha(x),'hash_matches_declared':sha(x)==p['sha256']} for i,x in found]})
 records.append({'ordinal':ordinal,'candidate_id':cid,'original':a,'current':b,'original_sha256':sha(a),'current_sha256':sha(b),'original_equals_current':a==b,'existing5B':five,'existing5B_locator':locator,'own_bindings':{k:x for k,x in current['slot_bindings'].items() if x['candidate_id']==cid},'direct_reference_cids':sorted(direct),'reference_bindings':bs,'mechanically_discovered_closure':closure,'original_provenance_entries':provenances})
payload={'schema':'photo-native-mechanical-read-packet/v1','assignment':{'task':'/root/native_evidence','model':'gpt-6.1-sol','effort':'high','range':[10250,11250]},'prepared_count':1000,'actual_read_count':0,'prepared_only':True,'formal_native_proofs':0,'root_approvals':0,'inputs':[info(p) for p in [currentp,originalp,orderp,catalogp,provp]],'records':records}
p=R/'authored/native_extra_10250_11250.inputs.json';assert not p.exists();p.write_text(json.dumps(payload,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
manifest={'schema':'photo-native-input-preparation-manifest/v1','assignment':payload['assignment'],'inputs':payload['inputs'],'packet':{'file':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},'prepared':1000,'read_or_approved_by_preparation':0,'first_cid':order[10250],'last_cid':order[11249],'mechanical_original_current_changes':sum(not r['original_equals_current'] for r in records),'unresolved_reference_count':sum(sum(v is None for v in r['mechanically_discovered_closure'].values()) for r in records),'mechanical_provenance_hash_mismatch_count':sum(not m['hash_matches_declared'] for r in records for p in r['original_provenance_entries'] for m in p['matches'])}
p=R/'worker-notes/native_extra_10250_11250.input-manifest.json';assert not p.exists();p.write_text(json.dumps(manifest,sort_keys=True,ensure_ascii=False,indent=2)+'\n');print(json.dumps(manifest,ensure_ascii=False))
