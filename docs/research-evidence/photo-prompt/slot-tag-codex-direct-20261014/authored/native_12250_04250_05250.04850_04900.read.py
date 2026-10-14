"""Prepare lossless native draft input; preparation is never reading/approval."""
import sys,json,hashlib,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d;import photo_candidate_realizations as rr
S=d.source();O=json.loads((R/'ORDER.json').read_text());start=4850;stop=4900;wanted=set(O[start:stop]);original={}
for path in (R/'decisions').glob('*.json'):
 doc=json.loads(path.read_text())
 for i,row in enumerate(doc.get('decisions',[])):
  if row['candidate_id'] in wanted:original[row['candidate_id']]=dict(file=str(path.relative_to(d.ROOT)),file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),item=i+1,row_sha256=d.c.digest(row),row=row)
def refs(v):
 if isinstance(v,str) and (d.c.ID.fullmatch(v) or d.c.BINDING_ID.fullmatch(v)):yield v
 elif isinstance(v,dict):
  for k,x in v.items():yield from refs(k);yield from refs(x)
 elif isinstance(v,list):
  for x in v:yield from refs(x)
rows=[]
for n in range(start,stop):
 cid=O[n];rec=S['candidates'][cid];seen={};todo=set(refs(rec))-{cid}
 while todo:
  key=todo.pop()
  if key in seen or key==cid:continue
  obj=S['slot_bindings' if d.c.BINDING_ID.fullmatch(key) else 'candidates'][key];seen[key]=obj;todo.update(set(refs(obj))-set(seen)-{cid})
 old=original[cid];after=d.corrected_record(rec,old['row']['corrections']);own={bid:b for bid,b in S['slot_bindings'].items() if b['candidate_id']==cid}
 rows.append(dict(ordinal=n,candidate_id=cid,source_before=rec,historical5B_after_correction_proposal=after,actual_rids=rr.ids(rec),actual_rids_after_5B=rr.ids(after),own_bindings=own,reference_records={k:v for k,v in seen.items() if d.c.ID.fullmatch(k)},reference_bindings={k:v for k,v in seen.items() if d.c.BINDING_ID.fullmatch(k)},registered5B=old))
p=R/'authored/native_12250_04250_05250.04850_04900.input.json';doc=dict(schema='photo-worker-native-draft-input/v1',source_sha256=d.c.digest(S),catalog_file='CATALOG-FINAL-144-V4.json',catalog_sha256='5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908',prepared_count=50,actual_read_count_at_preparation=0,records=rows)
if not p.exists():d.write(p,doc)
assert json.loads(p.read_text())==doc
if not sys.argv[1:]:print(json.dumps(dict(input=str(p),prepared_count=50,actual_read_count=0)))
else:
 for n in map(int,sys.argv[1:]):print(json.dumps(rows[n-start],ensure_ascii=False,separators=(',',':')))
