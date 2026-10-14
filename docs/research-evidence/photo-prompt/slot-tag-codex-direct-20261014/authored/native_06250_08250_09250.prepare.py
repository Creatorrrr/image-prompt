"""Prepare lossless, exact-CID direct-reading input; no semantic decisions."""
from pathlib import Path
import copy
import gzip
import hashlib
import json
import re
import sys
R=Path(__file__).resolve().parent.parent
ROOT=R.parents[3]
sys.path.insert(0,str(R));sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import direct_review as review
import photo_candidate_corpus as c
import photo_candidate_realizations as realizations
OUT=Path(__file__).with_name('native_06250_08250_09250.inputs.json')
assert not OUT.exists()
rawsha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load(path):
 raw=path.read_bytes();return json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw)
source=load(R/'SOURCE.json.gz');currentpath=R/'native-inputs/11870-01250-01300-plan-04/CURRENT-PROPOSAL.json.gz';current=load(currentpath);catalogpath=R/'CATALOG-FINAL-146-V5.json';catalog=load(catalogpath);order=load(R/'ORDER.json')
assert c.digest(source)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
assert c.digest(current)=='88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8'
assert c.digest(catalog)=='3655a006e69500662987c829361711a7194c3e297bfc4c408297bcf94f35d645'
assert len(order)==len(set(order))==18250 and len(current['candidates'])==18250
compiled={};files={}
for filename in ['review_08250_09250_08250_08500.json','review_08250_09250_08500_08750.json','review_08250_09250_08750_09000.json','review_08250_09250_09000_09250.json']:
 path=R/'decisions'/filename;data=load(path);files[str(path.relative_to(ROOT))]=rawsha(path)
 for item,row in enumerate(data['decisions'],1):
  cid=row['candidate_id'];assert cid not in compiled
  compiled[cid]={'file':str(path.relative_to(ROOT)),'item':item,'artifact':str(path.relative_to(ROOT))+'#item='+str(item),'file_sha256':rawsha(path),'row_sha256':c.digest(row),'row':row}
assert set(compiled)==set(order[8250:9250])
ID=re.compile(r'^(?:cand|bind)_[0-9a-f]{32}$')
def refs(value):
 if isinstance(value,str) and ID.fullmatch(value):yield value
 elif isinstance(value,dict):
  for key,child in value.items():yield from refs(key);yield from refs(child)
 elif isinstance(value,list):
  for child in value:yield from refs(child)
def closure(data,cid):
 records={};bindings={};pending=set(refs(data['candidates'][cid]))-{cid}
 while pending:
  key=pending.pop()
  if key==cid or key in records or key in bindings:continue
  if key in data['candidates']:
   value=data['candidates'][key];records[key]=value
  elif key in data['slot_bindings']:
   value=data['slot_bindings'][key];bindings[key]=value
  else:raise ValueError('missing exact reference '+key)
  pending.update(set(refs(value))-{cid}-records.keys()-bindings.keys())
 return {'candidate_records':dict(sorted(records.items())),'reference_bindings':dict(sorted(bindings.items()))}
def own(data,cid):return [b for b in data['slot_bindings'].values() if b['candidate_id']==cid]
rows=[]
for ordinal in range(8250,9250):
 cid=order[ordinal];original=source['candidates'][cid];registered=compiled[cid]
 assert registered['row']['source_record_sha256']==c.digest(original)
 five_b=review.corrected_record(original,registered['row']['corrections'])
 rows.append({'ordinal':ordinal,'candidate_id':cid,'original_source':original,'original_source_sha256':c.digest(original),
  'original_compiled':registered,'five_b_source_after':five_b,'five_b_source_after_sha256':c.digest(five_b),
  'current_source':current['candidates'][cid],'current_source_sha256':c.digest(current['candidates'][cid]),
  'original_own_bindings':own(source,cid),'current_own_bindings':own(current,cid),
  'original_closure':closure(source,cid),'current_closure':closure(current,cid),
  'actual_current_realization_ids':realizations.ids(current['candidates'][cid])})
report={'schema':'photo-native-lossless-direct-reading-input/v1','task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','range':[8250,9250],'prepared_count':1000,'actual_read_count_at_preparation':0,'semantic_review_or_approval_count_at_preparation':0,
 'source':{'file':str((R/'SOURCE.json.gz').relative_to(ROOT)),'raw_sha256':rawsha(R/'SOURCE.json.gz'),'canonical_sha256':c.digest(source)},
 'current_source':{'file':str(currentpath.relative_to(ROOT)),'raw_sha256':rawsha(currentpath),'canonical_sha256':c.digest(current)},
 'catalog':{'file':str(catalogpath.relative_to(ROOT)),'raw_sha256':rawsha(catalogpath),'canonical_sha256':c.digest(catalog)},
 'order':{'file':str((R/'ORDER.json').relative_to(ROOT)),'raw_sha256':rawsha(R/'ORDER.json')},'compiled_files':files,
 'mechanical_modules':{m.__name__:{'path':str(Path(m.__file__).relative_to(ROOT)),'raw_sha256':rawsha(Path(m.__file__))} for m in [review,c,realizations]},
 'full_policy_snapshot':current['policies'],'full_catalog_snapshot':catalog,'records':rows,
 'boundary':'Preparation only. No role/fact/mode/owner/value/operation/condition/approval classification. Actual read counts live in separate immutable checkpoints; this prepared input remains read0.'}
OUT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(str(OUT.relative_to(ROOT)),rawsha(OUT),'bytes',OUT.stat().st_size,'prepared1000 actualread0')
print('record kinds',sorted(set(row['current_source']['record_kind'] for row in rows)))
print('full5Bafter differs original',sum(row['five_b_source_after']!=row['original_source'] for row in rows),'current differs original',sum(row['current_source']!=row['original_source'] for row in rows))
