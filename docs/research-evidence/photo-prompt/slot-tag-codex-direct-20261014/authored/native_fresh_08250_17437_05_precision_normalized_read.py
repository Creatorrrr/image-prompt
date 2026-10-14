"""Lossless RID-prefix display only; no semantic classification or read counter."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'authored/native_fresh_08250_17437_05_precision_normalized_cache.json'
cache=json.loads(P.read_text()) if P.exists() else {}
rows=json.loads((R/'authored/native_fresh_08250_17437_04_precision.json').read_text())['resolutions']
def norm(v,rid):
 if isinstance(v,str):
  if v==rid:return '{RID}'
  if v.startswith(rid+'_'):return '{RID}_'+v[len(rid)+1:]
  return v.replace('/realization_content/'+rid+'/', '/realization_content/{RID}/')
 if isinstance(v,list):return [norm(x,rid) for x in v]
 if isinstance(v,dict):return {k:norm(x,rid) for k,x in v.items()}
 return v
def restore(v,rid):
 if isinstance(v,str):return v.replace('{RID}',rid)
 if isinstance(v,list):return [restore(x,rid) for x in v]
 if isinstance(v,dict):return {k:restore(x,rid) for k,x in v.items()}
 return v
for row in rows[int(sys.argv[1]):int(sys.argv[2])]:
 idx=row['reviewed_occurrence_index'];rid=row['realization_id']
 view={k:row[k] for k in ['issue_id','realization_id','exact_local_pointer','exact_local_quote','historical_narrow_quote','historical_mode','historical_target','historical_property','historical_typed_value','manual_disposition','fresh_canonical_fact','fresh_normal_anchor_unit','fresh_local_reference_unit','local_constraint_fact_ids']}
 nv=norm(view,rid);assert restore(nv,rid)==view
 key=json.dumps(nv,ensure_ascii=False,sort_keys=True,separators=(',',':'))
 if key in cache:print(idx,rid,'EXACT_RID_SUBSTITUTION_OF_INDEX',cache[key])
 else:print(idx,rid,key);cache[key]=idx
P.write_text(json.dumps(cache,ensure_ascii=False)+'\n')
