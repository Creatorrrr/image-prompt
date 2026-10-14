"""Offline blind 5C source reader; no scoring, models, registration or tagging."""
import copy,json,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as dr
import photo_candidate_realizations as pr
PLAN=R/'inverse-baseline-01/query-plan.json';RESULT=R/'inverse-baseline-01/inverse-search-baseline-query-139-01.json'
p=json.loads(PLAN.read_text());b=json.loads(RESULT.read_text());d=dr.source();proposal=json.loads((R/'CATALOG-CORRECTED-PROPOSAL-01.json').read_text())
assert dr.c.digest(d)==p['source_sha256']==b['source_sha256']=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
assert dr.c.digest(d['slot_catalog'])==p['catalog_sha256']==b['catalog_sha256']=='4723660c37d3f665f883a81f0e8d35b8c690307406d18d63ade654527d5bec9c'
assert [q['slot_id'] for q in p['queries']]==sorted(d['slot_catalog'])
def discovery(i):
 s=b['searches'][i];assert s['slot_id']==p['queries'][i]['slot_id']
 lanes={'bm25f':[r['document_id'] for r in s['lanes']['bm25f']['ranks'][:3]],'dense':[r['document_id'] for r in s['lanes']['embedding']['ranks'][:3]],'rrf':[r['document_id'] for r in s['rrf'][:3]]}
 return lanes,list(dict.fromkeys(c for lane in lanes.values() for c in lane))
def blind(v,path=''):
 if isinstance(v,dict):
  out={}
  for k,x in v.items():
   if k in {'role_evidence','semantic_review','slot_id','semantic_role'} or path.startswith('/content') and k in {'tags','facets'}:out[k]={'HIDDEN_INITIAL_TAG_OR_REVIEW':True}
   elif path=='/provenance' and k=='source':out[k]={'HIDDEN_SOURCE_TAG_ROUTE':True}
   else:out[k]=blind(x,path+'/'+k)
  return out
 if isinstance(v,list):return [blind(x,path) for x in v]
 return v
cmd=sys.argv[1] if __name__=='__main__' else None
if cmd=='spec':
 for i in range(int(sys.argv[2]),int(sys.argv[3])):
  slot=p['queries'][i]['slot_id'];print('SLOT',i,slot);print('QUERY_TEXT',json.dumps(p['queries'][i]['fields'],ensure_ascii=False));print('FROZEN139_SPEC',json.dumps(d['slot_catalog'][slot],ensure_ascii=False));print('PROPOSED141_SPEC',json.dumps(proposal['catalog'].get(slot),ensure_ascii=False));print('DISCOVERY',json.dumps(discovery(i)))
elif cmd in {'read','record','refs'}:
 i=int(sys.argv[2]);u=discovery(i)[1]
 for n in range(int(sys.argv[3]),int(sys.argv[4])):
  cid=u[n];record=d['candidates'][cid];refs=dr.closure(d,cid)
  if cmd!='refs':
   print('BLIND_FULL_SOURCE',i,n,cid,'SHA',dr.c.digest(record),'REALIZATIONS',pr.ids(record));print(json.dumps(blind(record),ensure_ascii=False))
  print('FULL_REFERENCE_CLOSURE_COUNT',len(refs))
  if cmd=='refs': selected=list(refs.items())[int(sys.argv[5]):int(sys.argv[6])]
  elif cmd=='read': selected=list(refs.items())
  else:selected=[]
  for rcid,row in selected:print('BLIND_FULL_REFERENCE',rcid,'SHA',dr.c.digest(row),json.dumps(blind(row),ensure_ascii=False))
  binds=sorted({bid for row in [record,*refs.values()] for bid in dr.references(row) if bid.startswith('bind_')})
  for bid in binds:print('BLIND_FROZEN_BINDING',bid,json.dumps(blind(d['slot_bindings'][bid]),ensure_ascii=False))
elif cmd is not None:raise ValueError('spec, read, record or refs only')
