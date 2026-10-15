"""Lossless exact whole-subtree equality references to actually read5 full source/proof records."""
from pathlib import Path
import json,hashlib,sys
O=Path(__file__).resolve().parent;R=O.parent;B=json.loads((R/'authored/native_12250_expression5_149_01/BATCH-v1.json').read_bytes());P=json.loads((R/'authored/native_12250_approval_pilot149_source25_plan_05.json').read_bytes());idx=int(sys.argv[1]);row=P['records'][idx];H=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest();cache={}
def visit(v,p):
 if isinstance(v,(dict,list,str)) and len(json.dumps(v,ensure_ascii=False))>240:cache.setdefault(H(v),(v,p))
 if isinstance(v,dict):
  for k,x in v.items():visit(x,p+'/'+k)
 elif isinstance(v,list):
  for i,x in enumerate(v):visit(x,p+'/'+str(i))
for i,b in enumerate(B['records']):visit(b,'/actually_read_batch_records/'+str(i))
def fold(v):
 if isinstance(v,(dict,list,str)):
  h=H(v)
  if h in cache and v==cache[h][0]:return {'exact_equal_previously_whole_read':cache[h][1],'sha256':h}
 if isinstance(v,dict):return {k:fold(x) for k,x in v.items()}
 if isinstance(v,list):return [fold(x) for x in v]
 return v
result=fold(row);text=json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n';assert len(text)<34000
p=O/(str(row['ordinal'])+'-plan05.read.json');assert not p.exists();p.write_text(text);print(text);print('FILE',p.name,'RAW',hashlib.sha256(p.read_bytes()).hexdigest())
