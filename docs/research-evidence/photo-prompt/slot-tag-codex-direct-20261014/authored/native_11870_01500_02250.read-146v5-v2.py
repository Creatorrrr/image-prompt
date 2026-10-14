"""Bounded lossless reader. Exact duplicates reference a previously printed full canonical value; no semantic compression."""
import sys,json,hashlib
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');F=R/'authored/native_11870_01500_02250.inputs-146v5.json';raw=F.read_bytes();assert hashlib.sha256(raw).hexdigest()=='9d8c7497a70fa0d145af47cc2d25aa73e273c11432baf2d06483e6b2cfb8497c';I=json.loads(raw);a,b=map(int,sys.argv[1:3]);assert 1500<=a<b<=2250 and b-a<=5
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();digest=lambda x:hashlib.sha256(canon(x)).hexdigest()
origin=json.loads(Path('docs/research-evidence/photo-prompt/slot-retrieval-stage05-20261012/CONTROLLED-FINAL-SOURCE.json').read_text())
def compact(v):
 seen={}
 def walk(x,p):
  k=canon(x)if isinstance(x,(str,list,dict))else b''
  if len(k)>35:
   if k in seen:return {'$exact_full_canonical_equal_value_at':seen[k],'sha256':hashlib.sha256(k).hexdigest()}
   seen[k]=p
  if isinstance(x,dict):return {z:walk(y,p+'/'+z.replace('~','~0').replace('/','~1'))for z,y in x.items()}
  if isinstance(x,list):return [walk(y,p+'/'+str(j))for j,y in enumerate(x)]
  return x
 return walk(v,'')
for n in range(a,b):
 cid=I['ids'][n-1500];v=I['records'][cid];out={k:v[k]for k in ['ordinal','candidate_id','original_full','actual_current_full','corrected5B_full','original_actual_rids','current_actual_rids','corrected5B_actual_rids','original_closure','actual_current_closure','corrected5B_closure','compiled5B_full','compiled5B_locator','original_sha256','actual_current_sha256','corrected5B_sha256']};out['controlled_original_whole_if_sha_equal']=[]
 for prov in v['original_full']['provenance']:
  parts=prov['source'].split(':')
  if len(parts)==3 and parts[0]=='slot':
   rows=origin.get('slots',{}).get(parts[1],[]);found=[x for x in rows if x.get('id')==parts[2]]
   if len(found)==1 and digest(found[0])==prov['sha256']:out['controlled_original_whole_if_sha_equal'].append({'provenance':prov,'canonical_equality':True,'whole_entry':found[0]})
   else:out['controlled_original_whole_if_sha_equal'].append({'provenance':prov,'canonical_equality':False,'no_meaning_from_mismatch':True})
 print('ORDINAL',n);print(json.dumps(compact(out),ensure_ascii=False,indent=2))
