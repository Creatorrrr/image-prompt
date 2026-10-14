# Read-only mechanical lossless exact-value factoring. No semantic decision or model generation.
import copy,hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P=R/'native-inputs/prepared/review08250-17437-05/PREPARED-PACKET.json';B=R/'native_batches/review08250-17437-05/BATCH.json'
def compact(value):
 seen={};table={}
 def walk(v,path):
  key=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')) if isinstance(v,(dict,list,str)) else ''
  if len(key)>38:
   if key in seen:return {'$exact_same_value_at':seen[key]}
   seen[key]=path
  table[path]=copy.deepcopy(v)
  if isinstance(v,dict):return {k:walk(x,path+'/'+k.replace('~','~0').replace('/','~1')) for k,x in v.items()}
  if isinstance(v,list):return [walk(x,path+'/'+str(i)) for i,x in enumerate(v)]
  return v
 result=walk(value,'')
 def back(v):
  if isinstance(v,dict) and set(v)=={'$exact_same_value_at'}:return copy.deepcopy(table[v['$exact_same_value_at']])
  if isinstance(v,dict):return {k:back(x) for k,x in v.items()}
  if isinstance(v,list):return [back(x) for x in v]
  return v
 assert back(result)==value
 return result
if __name__=='__main__':
 p=json.loads(P.read_text());b=json.loads(B.read_text())['records'][0];cid=b['candidate_id'];mode=sys.argv[1]
 if mode=='current':v=p['current_records'][cid]
 elif mode=='proof':v=b['proof']
 elif mode=='precision':v=json.loads((R/'authored/native_fresh_08250_17437_05_precision.json').read_text())
 elif mode=='delta':v=b['delta']
 else:raise ValueError(mode)
 q=R/'worker-notes'/f'native-09250-special17437-05-peer-20261015.{mode}.factored.json'
 if not q.exists():q.write_text(json.dumps(compact(v),ensure_ascii=False,indent=2)+'\n')
 text=q.read_text();a=int(sys.argv[2]) if len(sys.argv)>2 else 0;z=int(sys.argv[3]) if len(sys.argv)>3 else a+22000
 print(json.dumps(dict(mode=mode,total_chars=len(text),range=[a,min(z,len(text))],file=str(q.relative_to(R)),file_sha256=hashlib.sha256(q.read_bytes()).hexdigest(),roundtrip_exact=True)))
 print(text[a:z])
