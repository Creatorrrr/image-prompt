"""Read-only audit packet creation; selected preparation never counts as reading."""
import sys,json,hashlib,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d
selected=[1255,1258,1262,1266,4286,4529,4714,4733,4871,4998,5030,5033,5113,5197,5202,5209,5210,5234]
S=d.source();O=json.loads((R/'ORDER.json').read_text());wanted={O[n] for n in selected};old={}
for p in (R/'decisions').glob('*.json'):
 a=json.loads(p.read_text())
 for i,x in enumerate(a.get('decisions',[])):
  if x['candidate_id'] in wanted:old[x['candidate_id']]=dict(file=str(p.relative_to(d.ROOT)),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),item=i+1,row=x,row_sha256=d.c.digest(x))
def refs(v):
 if isinstance(v,str) and (d.c.ID.fullmatch(v) or d.c.BINDING_ID.fullmatch(v)):yield v
 elif isinstance(v,dict):
  for k,x in v.items():yield from refs(k);yield from refs(x)
 elif isinstance(v,list):
  for x in v:yield from refs(x)
rows=[]
for ordinal in selected:
 cid=O[ordinal];r=S['candidates'][cid];closure={};todo=set(refs(r))-{cid}
 while todo:
  k=todo.pop()
  if k in closure or k==cid:continue
  v=S['slot_bindings' if d.c.BINDING_ID.fullmatch(k) else 'candidates'][k];closure[k]=v;todo.update(set(refs(v))-{cid}-set(closure))
 rows.append(dict(ordinal=ordinal,candidate_id=cid,original=r,historical5B=old[cid],historical5B_after=d.corrected_record(r,old[cid]['row']['corrections']),own_bindings={k:v for k,v in S['slot_bindings'].items() if v['candidate_id']==cid},closure=closure))
catpath=R/'CATALOG-FINAL-146-V5.json';cat=json.loads(catpath.read_text());p=R/'authored/native_12250_taxonomy_mechanics_articulation_relational_20261015.input.json'
a=dict(schema='photo-readonly-taxonomy-audit-input/v1',prepared_count=len(rows),actual_read_count_at_preparation=0,source_sha256=d.c.digest(S),catalog_file=str(catpath.relative_to(d.ROOT)),catalog_sha256=d.c.digest(cat),catalog_raw_sha256=hashlib.sha256(catpath.read_bytes()).hexdigest(),rows=rows,production_modified=False)
if not p.exists():
 with p.open('x') as f:json.dump(a,f,ensure_ascii=False,indent=2);f.write('\n')
assert json.loads(p.read_text())==a
if len(sys.argv)==1:print(json.dumps(dict(path=str(p),prepared_count=len(rows),actual_read_count=0)))
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
 requested=set(map(int,sys.argv[1:]))
 for x in rows:
  # Reuse only prior actually read rows in this bounded sequential audit.
  if x['ordinal']>max(requested):break
  v=enc(x,'A'+str(x['ordinal']))
  if x['ordinal'] in requested:print(x['ordinal'],json.dumps(v,ensure_ascii=False,separators=(',',':')))
