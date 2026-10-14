import sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=json.loads((R/'authored/native_12250_04250_05250.04250_04300.input.json').read_text());seen={}
def enc(v,path):
 s=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
 if s in seen:
  ref={'EXACT_AS':seen[s]}
  if len(json.dumps(ref,separators=(',',':')))<len(s):return ref
 seen[s]=path
 if isinstance(v,dict):return {k:enc(x,path+'/'+k) for k,x in v.items()}
 if isinstance(v,list):return [enc(x,path+'/'+str(i)) for i,x in enumerate(v)]
 return v
start,stop=map(int,sys.argv[1:]);assert 4255<=start<stop<=4300
# Earlier rows here must actually have been completely read. The caller controls start/stop.
for row in p['records']:
 n=row['ordinal']
 if n>=stop:break
 v=enc(row,'R'+str(n))
 if n>=start:print(n,json.dumps(v,ensure_ascii=False,separators=(',',':')))
