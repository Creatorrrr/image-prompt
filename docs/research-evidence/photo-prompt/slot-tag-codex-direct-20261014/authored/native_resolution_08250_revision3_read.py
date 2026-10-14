"""Lossless display only: exact subtree equality and reversible string deltas."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];J=json.loads((R/'authored/native_resolution_08250_revision3_sources.json').read_text());statepath=R/'authored/native_resolution_08250_revision3_read_state.json'
state=json.loads(statepath.read_text()) if statepath.exists() else {'seen':{},'strings':[]}
seen=state['seen'];strings=state['strings']
def show(v,p):
 key=json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'))
 if len(key)>45 and key in seen:return {'=exact':seen[key]}
 if isinstance(v,str):
  out=v
  if len(v)>120:
   best=None
   for oldp,old in strings:
    n=min(len(old),len(v));start=0
    while start<n and old[start]==v[start]:start+=1
    end=0
    while end<n-start and old[-end-1]==v[-end-1]:end+=1
    gain=start+end
    if best is None or gain>best[0]:best=(gain,oldp,start,len(old)-end,v[start:len(v)-end if end else len(v)],old)
   if best and best[0]>max(80,len(v)//3):
    gain,oldp,start,stop,repl,old=best;assert old[:start]+repl+old[stop:]==v
    out={'=delta':[oldp,start,stop,repl]}
  strings.append([p,v])
 elif isinstance(v,list):out=[show(x,p+'/'+str(i)) for i,x in enumerate(v)]
 elif isinstance(v,dict):out={k:show(x,p+'/'+k.replace('~','~0').replace('/','~1')) for k,x in v.items()}
 else:out=v
 if len(key)>45:seen[key]=p
 return out
if sys.argv[1]=='root':
 for family in ['resolution_proposed_records']:
  for cid,rec in J[family].items():
   if family=='resolution_proposed_records' and cid.endswith('a2cc8e0'):
    rec=json.loads(json.dumps(rec));rec['content'].pop('realization_content')
   print(family+'/'+cid,json.dumps(show(rec,family+'/'+cid),ensure_ascii=False,separators=(',',':')))
else:
 t=J['resolution_proposed_records']['cand_d15b4c6334a45b61a7407a022a2cc8e0']['content']['realization_content']
 for rid,_ in J['authored_actual_choices'][int(sys.argv[1]):int(sys.argv[2])]:
  p='resolution_proposed_records/cand_d15b4c6334a45b61a7407a022a2cc8e0/content/realization_content/'+rid
  print(rid,json.dumps(show(t[rid],p),ensure_ascii=False,separators=(',',':')))
statepath.write_text(json.dumps(state,ensure_ascii=False)+'\n')
