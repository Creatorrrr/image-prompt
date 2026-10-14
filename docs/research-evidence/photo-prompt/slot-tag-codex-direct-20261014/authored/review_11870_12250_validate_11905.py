"""Validate only individually authored literal decisions; no model/source classifier."""
import json,runpy,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R));import direct_review as dr
L=runpy.run_path(str(H/'review_11870_12250_literals_11905.py'));D=L['D']
p=json.loads((R/'packets/11870-130.json').read_text());data=dr.source()
assert dr.c.digest(data)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
rows=[];cache={};target=H/f'review_11870_12250_11905_{11905+len(D)}.json'
for ordinal,meaning,boundary,selected in D:
 assert ordinal==11905+len(rows)
 roles={};facts=[]
 for tag,dim,owner,prop,pointer,quote,why in selected:
  f=dict(pointer=pointer,quote=quote,dimension=dim,target=owner,property=prop)
  facts.append(dict(f,realization_id='base'))
  if tag not in roles:roles[tag]=dict(slot_id=tag,semantic_role=data['slot_catalog'][tag]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=why,evidence=[])
  else:roles[tag]['rationale']+=' '+why
  roles[tag]['evidence'].append(f)
 decision=dict(candidate_id=p['ids'][ordinal-11870],meaning_summary=meaning,recommended_kind='visual_option',corrections=L.get('CORRECTIONS',{}).get(ordinal,[]),roles=list(roles.values()),facts=facts,rejected_boundaries=[boundary],uncertainties=L.get('UNCERTAINTIES',{}).get(ordinal,[]),status='needs_source_fix' if ordinal in L.get('UNCERTAINTIES',{}) else 'approved',all_roles_considered=True)
 assert not p['references'][decision['candidate_id']]
 row={**dr.binding(data,decision['candidate_id'],cache=cache),**decision,'schema':dr.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':dr.c.digest(p),'authored_decision':dict(file=str(target.relative_to(dr.ROOT)),item=len(rows)+1,sha256=dr.c.digest(decision))}
 try:dr.validate_decision(row,data,binding_cache=cache)
 except Exception as exc:raise ValueError((ordinal,str(exc))) from exc
 rows.append(decision)
if '--write' in sys.argv:
 assert not target.exists(), 'never overwrite a checkpoint'
 target.write_text(json.dumps(dict(decisions=rows),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(start=11905,stop=11905+len(rows),validated=len(rows),written='--write' in sys.argv)))
