"""Exact-equality display references only; no semantic classification or read attestation.
Seed is the explicitly already-read prefix, never future records. Every substitution
contains the original full-value canonical digest and exact source ordinal/pointer.
"""
from pathlib import Path
import json,hashlib,sys
P=Path(__file__).with_name('native_06250_08250_09250.v6.inputs.json')
data=json.loads(P.read_text());start,stop,read_stop=map(int,sys.argv[1:4]);assert 8625<=read_stop<=start<stop<=9250
canon=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
seen={};keys=['original_source','five_b_source_after','current_source','original_compiled','original_own_bindings','current_own_bindings','original_closure','current_closure']
def eligible(v):return isinstance(v,(str,list,dict)) and len(canon(v))>=90
def walk(v,loc,emit):
 raw=canon(v)
 if eligible(v) and raw in seen:
  return {'EXACT_EQUAL_PREVIOUSLY_READ':seen[raw],'canonical_sha256':hashlib.sha256(raw.encode()).hexdigest()} if emit else None
 if isinstance(v,dict):out={k:walk(c,loc+'/'+k.replace('~','~0').replace('/','~1'),emit) for k,c in v.items()}
 elif isinstance(v,list):out=[walk(c,loc+'/'+str(i),emit) for i,c in enumerate(v)]
 else:out=v
 if eligible(v):seen.setdefault(raw,loc)
 return out
for row in data['records'][:read_stop-8625]:
 for key in keys:walk(row[key],f"ordinal={row['ordinal']}/{key}",False)
for row in data['records'][start-8625:stop-8625]:
 print('WHOLE',row['ordinal'],row['candidate_id'],'actualRIDs',row['actual_current_realization_ids'])
 for key in keys:print(key,json.dumps(walk(row[key],f"ordinal={row['ordinal']}/{key}",True),ensure_ascii=False,separators=(',',':')))
