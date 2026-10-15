"""Lossless selected5 display only; equal repeated strings reference whole read source paths."""
from pathlib import Path
import json,sys,hashlib
R=Path(__file__).resolve().parent.parent;W=R/'authored/native_12250_expression5_149_01';B=json.loads((W/'BATCH-v1.json').read_bytes());row=B['records'][int(sys.argv[1])];mode=sys.argv[2];H=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
if mode=='source':
 before=row['source_before'];after=row['source_after'];reduced=json.loads(json.dumps(after));del reduced['content']['application_contract'];assert reduced==before
 result={k:row[k] for k in row if k not in {'source_before','source_after','proof'}};result.update(source_before_whole=before,full_new_application_contract=after['content']['application_contract'],full_source_after_sha256=H(after),lossless_after_rule='Complete before plus this exact one App addition; every other path including conditions/effects/provenance byte equal')
else:
 p=row['proof'];r=row['source_after'];strings={}
 def find(x,path):
  if isinstance(x,str):strings.setdefault(x,path)
  elif isinstance(x,dict):
   for k,v in x.items():find(v,path+'/'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):find(v,path+'/'+str(i))
 find(r,'/source_after')
 def reduce(x,key=None):
  if isinstance(x,str) and key in {'quote'} and x in strings:return {'exact_whole_source_string_ref':strings[x],'sha256':H(x)}
  if isinstance(x,dict):return {k:reduce(v,k) for k,v in x.items()}
  if isinstance(x,list):return [reduce(v) for v in x]
  return x
 result={'ordinal':row['ordinal'],'candidate_id':row['candidate_id'],'proof':reduce(p)}
text=json.dumps(result,ensure_ascii=False,indent=2)+'\n';assert len(text)<37000
out=Path(__file__).resolve().parent/(str(row['ordinal'])+'-'+mode+'.read.json');assert not out.exists();out.write_text(text);print(text);print('READFILE',out.name,hashlib.sha256(out.read_bytes()).hexdigest())
