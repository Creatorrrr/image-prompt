"""Lossless bounded source reader, no semantic decisions or review mutation."""
import json,gzip,hashlib,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review11870-01250-01300-03';I=json.loads((D/'INPUT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());A=json.loads((D/'ASSIGNMENT.json').read_text())
assert hashlib.sha256((D/'INPUT.json').read_bytes()).hexdigest()=='cc08fc8f766704bd5ef1cb5c58f98224c60143c0ab14d01dd82cbf7ff1064d40'
S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));O=json.loads(gzip.decompress(Path(I['original_snapshot']['file']).read_bytes()));C=I['catalog_review']['after']
def compact(v):
 seen={}
 def f(x,path):
  k=json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')) if isinstance(x,(dict,list,str)) else ''
  if len(k)>30:
   if k in seen:return {'$exact_same_full_value_at':seen[k]}
   seen[k]=path
  if isinstance(x,dict):return {k:f(y,path+'/'+k.replace('~','~0').replace('/','~1')) for k,y in x.items()}
  if isinstance(x,list):return [f(y,path+'/'+str(i)) for i,y in enumerate(x)]
  return x
 return f(v,'')
a,b=int(sys.argv[1]),int(sys.argv[2]);mode=sys.argv[3];out={}
for n in range(a,b):
 cid=A['ids'][n-1250]
 if mode=='source':out[str(n)]={'original':P['original_records'][cid],'current':P['current_records'][cid],'ownbindings':{bid:row for bid,row in S['slot_bindings'].items() if row['candidate_id']==cid},'references':P['references'][cid],'reference_bindings':P['reference_bindings'][cid]}
 elif mode=='compiled':out[str(n)]={'old_full_compiled':P['historical_compiled_rows'][cid],'locator':I['original_decisions'][cid],'original_packet':I['original_packets'][cid],'revision':I['required_revisions'][cid]}
 elif mode=='prior':out[str(n)]=json.loads((R/'native_batches/review11870-01250-01300-02/BATCH.json').read_text())['records'][n-1250]
 else:raise ValueError(mode)
print(json.dumps(compact(out),ensure_ascii=False))
