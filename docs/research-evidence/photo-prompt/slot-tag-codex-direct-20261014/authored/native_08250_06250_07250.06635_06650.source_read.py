"""Lossless complete source display, never automatic read completion."""
import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'authored'
J=json.loads((A/'native_08250_06250_07250.prepared.json').read_text())
P=A/'native_08250_06250_07250.06635_06650.display-cache.json'
state=json.loads(P.read_text()) if P.exists() else {'seen':{},'strings':[]}
seen=state['seen'];strings=state['strings']
def show(v,p):
 key=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
 if len(key)>45 and key in seen:return {'=exact':seen[key]}
 if isinstance(v,str):
  out=v
  if len(v)>150:
   best=None
   for oldp,old in strings:
    n=min(len(v),len(old));i=0
    while i<n and v[i]==old[i]:i+=1
    j=0
    while j<n-i and v[-j-1]==old[-j-1]:j+=1
    if best is None or i+j>best[0]:best=(i+j,oldp,i,len(old)-j,v[i:len(v)-j if j else len(v)],old)
   if best and best[0]>max(100,len(v)//2):
    gain,oldp,i,stop,repl,old=best;assert old[:i]+repl+old[stop:]==v;out={'=delta':[oldp,i,stop,repl]}
  strings.append([p,v])
 elif isinstance(v,list):out=[show(x,p+'/'+str(i)) for i,x in enumerate(v)]
 elif isinstance(v,dict):out={k:show(x,p+'/'+k.replace('~','~0').replace('/','~1')) for k,x in v.items()}
 else:out=v
 if len(key)>45:seen[key]=p
 return out
lo,hi=map(int,sys.argv[1:3])
for row in J['records'][lo-6250:hi-6250]:
 view={k:v for k,v in row.items() if k!='compiled_5B_review'}
 view['compiled_source_judgement']={k:row['compiled_5B_review'][k] for k in ['status','recommended_kind','meaning_summary','rejected_boundaries','uncertainties','source_record_sha256']}
 view['compiled_roles']=[{k:r[k] for k in ['slot_id','scope','realization_ids','semantic_role']} for r in row['compiled_5B_review']['roles']]
 view['compiled_5B_status']=row['compiled_5B_review']['status'];view['exact_5B_corrections']=row['compiled_5B_review']['corrections']
 print(row['ordinal'],json.dumps(show(view,'ordinal'+str(row['ordinal'])),ensure_ascii=False,separators=(',',':')))
P.write_text(json.dumps(state,ensure_ascii=False)+'\n')
