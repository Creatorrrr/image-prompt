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
def norm(v,rid):
 if isinstance(v,str):
  if v==rid:return '{RID}'
  if v.startswith('g06_'+rid+'_'):return 'g06_{RID}_'+v[len('g06_'+rid+'_'):]
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

D=json.loads((R/'authored/native_fresh_08250_17437_06_unsigned.json').read_text());Q=D['proof_draft'];layouts=D['selected_layouts']
for layout in layouts[int(sys.argv[1]):int(sys.argv[2])]:
 rid=layout['rid'];v={'layout':layout,'facts':[f for f in Q['facts'] if f['realization_id']==rid],'source_units':[u for u in Q['source_units'] if u['realization_id']==rid],'guard_supports':[g for g in Q['guard_supports'] if g['realization_id']==rid],'owner_map':Q['owner_maps'][rid],'effect_set':Q['effect_sets'][rid],'guard_set':Q['guard_sets'][rid],'profile_contract':Q['profile_contracts'][rid]}
 nv=norm(v,rid);assert restore(nv,rid)==v
 print(rid,json.dumps(show(nv,'proof06/'+rid),ensure_ascii=False,separators=(',',':')))
STATE.write_text(json.dumps(cache,ensure_ascii=False)+'\n')
