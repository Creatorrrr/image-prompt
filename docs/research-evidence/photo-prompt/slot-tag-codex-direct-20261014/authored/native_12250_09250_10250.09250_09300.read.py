"""Prepare immutable research packet; preparation is not source reading."""
import sys,json,hashlib,copy,gzip
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d;import photo_candidate_realizations as rr
start=9250;stop=9300;S=d.source();O=json.loads((R/'ORDER.json').read_text());snapshot=R/'native-inputs/11870-01250-01300-plan-04/CURRENT-PROPOSAL.json.gz';raw=snapshot.read_bytes();C=json.loads(gzip.decompress(raw));assert d.c.digest(C)=='88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8';CAT=json.loads((R/'CATALOG-FINAL-146-V5.json').read_text());assert C['slot_catalog']==CAT;wanted=set(O[start:stop]);old={}
for path in (R/'decisions').glob('*.json'):
 a=json.loads(path.read_text())
 for i,row in enumerate(a.get('decisions',[])):
  if row['candidate_id'] in wanted:old[row['candidate_id']]=dict(file=str(path.relative_to(d.ROOT)),file_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),item=i+1,row_sha256=d.c.digest(row),row=row)
def refs(v):
 if isinstance(v,str) and (d.c.ID.fullmatch(v) or d.c.BINDING_ID.fullmatch(v)):yield v
 elif isinstance(v,dict):
  for k,x in v.items():yield from refs(k);yield from refs(x)
 elif isinstance(v,list):
  for x in v:yield from refs(x)
def closure(corpus,cid):
 todo=set(refs(corpus['candidates'][cid]))-{cid};seen={}
 while todo:
  k=todo.pop()
  if k in seen or k==cid:continue
  v=corpus['slot_bindings' if d.c.BINDING_ID.fullmatch(k) else 'candidates'][k];seen[k]=v;todo.update(set(refs(v))-{cid}-set(seen))
 return seen
rows=[]
for ordinal in range(start,stop):
 cid=O[ordinal];orig=S['candidates'][cid];current=C['candidates'][cid];cl=closure(C,cid)
 rows.append(dict(ordinal=ordinal,candidate_id=cid,original_source=orig,source_before=current,current_equals_original=current==orig,historical5B_after_correction_proposal=d.corrected_record(orig,old[cid]['row']['corrections']),actual_rids=rr.ids(current),actual_rids_original=rr.ids(orig),own_bindings={k:v for k,v in C['slot_bindings'].items() if v['candidate_id']==cid},original_own_bindings={k:v for k,v in S['slot_bindings'].items() if v['candidate_id']==cid},reference_records={k:v for k,v in cl.items() if d.c.ID.fullmatch(k)},reference_bindings={k:v for k,v in cl.items() if d.c.BINDING_ID.fullmatch(k)},original_reference_closure=closure(S,cid),registered5B=old[cid]))
doc=dict(schema='photo-worker-native-research-input/v2',source_sha256=d.c.digest(S),current_snapshot_file=str(snapshot.relative_to(d.ROOT)),current_snapshot_raw_sha256=hashlib.sha256(raw).hexdigest(),current_snapshot_sha256=d.c.digest(C),catalog_file='CATALOG-FINAL-146-V5.json',catalog_sha256=d.c.digest(CAT),prepared_count=50,actual_read_count_at_preparation=0,records=rows)
p=R/'authored/native_12250_09250_10250.09250_09300.input.json'
if not p.exists():
 with p.open('x') as f:json.dump(doc,f,ensure_ascii=False,indent=2);f.write('\n')
assert json.loads(p.read_text())==doc
if len(sys.argv)==1:print(json.dumps(dict(file=str(p),prepared_count=50,actual_read_count=0)))
else:
 seen={}
 def enc(v,path):
  s=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
  if s in seen:
   ref={'EXACT_AS':seen[s]}
   if len(json.dumps(ref))<len(s):return ref
  seen[s]=path
  if isinstance(v,dict):return {k:enc(x,path+'/'+k) for k,x in v.items()}
  if isinstance(v,list):return [enc(x,path+'/'+str(i)) for i,x in enumerate(v)]
  return v
 lo,hi=map(int,sys.argv[1:]);assert start<=lo<hi<=stop
 for row in rows:
  if row['ordinal']>=hi:break
  value=enc(row,'R'+str(row['ordinal']))
  if row['ordinal']>=lo:print(row['ordinal'],json.dumps(value,ensure_ascii=False,separators=(',',':')))
