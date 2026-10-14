"""Prepare immutable research packet; preparation is not source reading."""
import sys,json,hashlib,copy,gzip
from pathlib import Path

G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_semantic_evidence as pinned_native,photo_candidate_corpus as pinned_corpus,photo_precore_bridge as pinned_bridge,photo_candidate_realizations as pinned_realizations
for module in [pinned_native,pinned_corpus,pinned_bridge,pinned_realizations]:assert Path(module.__file__).resolve().is_relative_to(G)
assert hashlib.sha256(Path(pinned_native.__file__).read_bytes()).hexdigest()=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d;import photo_candidate_realizations as rr
start=9750;stop=9800;S=d.source();O=json.loads((R/'ORDER.json').read_text());snapshot=R/'native-inputs/11870-01250-01300-plan-04/CURRENT-PROPOSAL.json.gz';raw=snapshot.read_bytes();C=json.loads(gzip.decompress(raw));assert d.c.digest(C)=='88614a52f5e4148efc57806c641717107c2b045acfc205e934f96246af8a81d8';SNAPCAT=json.loads((R/'CATALOG-FINAL-146-V5.json').read_text());assert C['slot_catalog']==SNAPCAT;CAT=json.loads((R/'CATALOG-FINAL-149-V6.json').read_text());assert d.c.digest(CAT)=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15';assert sum(CAT[k]==v for k,v in SNAPCAT.items())==145;wanted=set(O[start:stop]);old={}
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
doc=dict(schema='photo-worker-native-research-input/v2',source_sha256=d.c.digest(S),current_snapshot_file=str(snapshot.relative_to(d.ROOT)),current_snapshot_raw_sha256=hashlib.sha256(raw).hexdigest(),current_snapshot_sha256=d.c.digest(C),source_snapshot_catalog_file='CATALOG-FINAL-146-V5.json',source_snapshot_catalog_sha256=d.c.digest(SNAPCAT),review_catalog_separately_root_pinned=True,review_catalog_read_provenance='Direct full4spec after read on20261015 from rootFINAL149V6; other145 exact146V5 values mechanicallychecked, no newwhole149personalread claim; source88614snapshot unchanged.',catalog_file='CATALOG-FINAL-149-V6.json',catalog_sha256=d.c.digest(CAT),prepared_count=50,actual_read_count_at_preparation=0,records=rows)
p=R/'authored/native_12250_09250_10250.09750_09800.input.json'
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
