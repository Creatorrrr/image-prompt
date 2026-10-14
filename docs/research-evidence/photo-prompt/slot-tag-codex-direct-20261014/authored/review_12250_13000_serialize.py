import sys,json,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R));import direct_review as d
L=runpy.run_path(str(R/'authored/review_12250_13000_literals.py'));data=d.source();p=json.loads((R/'packets/12250-250.json').read_text());rows=[];cache={}
assert d.c.digest(data)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
start=12250; stop=start+len(L['D']); path=R/'authored'/f'review_12250_13000_{start}_{stop}.json'
for n,meaning,boundary,selected in L['D']:
 assert n==start+len(rows);cid=p['ids'][n-start];roles={};facts=[]
 for tag,dimension,owner,prop,pointer,quote,rationale in selected:
  f=dict(pointer=pointer,quote=quote,dimension=dimension,target=owner,property=prop)
  facts.append(dict(f,realization_id='base'))
  if tag not in roles:roles[tag]=dict(slot_id=tag,semantic_role=data['slot_catalog'][tag]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=rationale,evidence=[])
  else:roles[tag]['rationale']+=' '+rationale
  roles[tag]['evidence'].append(f)
 decision=dict(candidate_id=cid,meaning_summary=meaning,recommended_kind=L.get('K',{}).get(n,'visual_bundle'),corrections=[],roles=list(roles.values()),facts=facts,rejected_boundaries=[boundary],uncertainties=[],status='diagnostic_reviewed' if L.get('K',{}).get(n)=='diagnostic' else 'approved',all_roles_considered=True)
 full={**d.binding(data,cid,cache=cache),**decision,'schema':d.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':d.c.digest(p),'authored_decision':dict(file=str(path.relative_to(d.ROOT)),item=len(rows)+1,sha256=d.c.digest(decision))}
 d.validate_decision(full,data,binding_cache=cache);rows.append(decision)
d.write(path,dict(decisions=rows));print(json.dumps({'start':start,'stop':stop,'count':len(rows),'authored':str(path),'unresolved':[]}))
