import json,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
old=json.loads((R/'authored/native_12250_approval_pilot149_source23_plan_03.json').read_text());cur=json.loads((R/'authored/native_12250_approval_pilot149_source25_plan_04.json').read_text())
def h(a):return hashlib.sha256(json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
seen={}
def index(x,path):
 s=json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'));seen[s]=path
 if isinstance(x,dict):
  for k,v in x.items():index(v,path+'/'+k)
 elif isinstance(x,list):
  for i,v in enumerate(x):index(v,path+'/'+str(i))
for x in old['records']:
 index(x['after'],'PLAN03/ordinal'+str(x['ordinal'])+'/after')
 index(x['facts'],'PLAN03/ordinal'+str(x['ordinal'])+'/facts')
def enc(x,path):
 s=json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'));ref=dict(EXACT_AS=seen.get(s),canonical_sha256=h(x))
 if s in seen and len(json.dumps(ref))<len(s):return ref
 seen[s]=path
 if isinstance(x,dict):return {k:enc(v,path+'/'+k) for k,v in x.items()}
 if isinstance(x,list):return [enc(v,path+'/'+str(i)) for i,v in enumerate(x)]
 return x
lo,hi=map(int,sys.argv[1:]);print('PLAN04',h(cur))
for x in cur['records']:
 if lo<=x['ordinal']<hi:print(x['ordinal'],json.dumps(enc(dict(after=x['after'],facts=x['facts'],role_views=x['manual_same_fact_role_view_plans'],source_unit_plans=x['positive_unit_entailment_plans']), 'PLAN04/ordinal'+str(x['ordinal'])),ensure_ascii=False,separators=(',',':')))
