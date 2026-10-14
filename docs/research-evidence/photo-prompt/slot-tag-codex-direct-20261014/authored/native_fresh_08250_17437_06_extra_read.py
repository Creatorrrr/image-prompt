"""Lossless display of formal INPUT only; equality/delta compression is not reading."""
import copy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'native-inputs/prepared/review08250-17437-06/PREPARED-PACKET.json';J=json.loads(P.read_text());CID=J['ids'][0];REC=J['current_records'][CID]
STATE=R/'authored/native_fresh_08250_17437_06_read_cache.json';cache=json.loads(STATE.read_text()) if STATE.exists() else {'seen':{},'strings':[]}
def show(v,p):
 key=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
 if len(key)>45 and key in cache['seen']:return {'=exact':cache['seen'][key]}
 if isinstance(v,str):
  out=v
  if len(v)>120:
   best=None
   for oldp,old in cache['strings']:
    n=min(len(old),len(v));a=0
    while a<n and old[a]==v[a]:a+=1
    b=0
    while b<n-a and old[-b-1]==v[-b-1]:b+=1
    gain=a+b
    if best is None or gain>best[0]:best=(gain,oldp,a,len(old)-b,v[a:len(v)-b if b else len(v)],old)
   if best and best[0]>max(80,len(v)//3):
    _,oldp,a,b,repl,old=best;assert old[:a]+repl+old[b:]==v;out={'=delta':[oldp,a,b,repl]}
  cache['strings'].append([p,v])
 elif isinstance(v,list):out=[show(x,p+'/'+str(i)) for i,x in enumerate(v)]
 elif isinstance(v,dict):out={k:show(x,p+'/'+k.replace('~','~0').replace('/','~1')) for k,x in v.items()}
 else:out=v
 if len(key)>45:cache['seen'][key]=p
 return out

import gzip
arg=sys.argv[1]
if arg in {'original_records','historical_compiled_rows','references','reference_bindings'}:
 print(json.dumps(show(J[arg][CID],arg),ensure_ascii=False,separators=(',',':')))
elif arg=='bindings':
 I=json.loads((R/'native-inputs/prepared/review08250-17437-06/INPUT.json').read_text())
 for key in ['original_snapshot','current_snapshot']:
  src=json.loads(gzip.decompress(Path(I[key]['file']).read_bytes()))
  print(key,json.dumps(show({k:v for k,v in src['slot_bindings'].items() if v['candidate_id']==CID},key+'/ownbindings'),ensure_ascii=False))
STATE.write_text(json.dumps(cache,ensure_ascii=False)+'\n')
