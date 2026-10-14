"""Validate manual re-read amendments only. Never register or mutate source."""
import copy,hashlib,json,runpy,sys
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as dr
from photo_candidate_realizations import ids
A=runpy.run_path(str(R/'authored/review_11870_12250_amend48_literals.py'))['A']
p=json.loads((R/'packets/12000-250.json').read_text());d=dr.source();cache={};before={}
assert dr.c.digest(d)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
for rel in ['authored/review_11870_12250_checkpoint_12000_12078.json','authored/review_11870_12250_tail_12078_12250.json']:
 for original in json.loads((R/rel).read_text())['decisions']:
  if original['status']=='needs_boundary_review':before[original['candidate_id']]=(rel,original)
assert len(A)==48 and len(before)==48 and len({a[0] for a in A})==48
output=R/'authored/review_11870_12250_amend48.json';amendments=[]
for o,result,meaning,rationale,extra in A:
 cid=p['ids'][o-12000];oldfile,old=before[cid];record=d['candidates'][cid]
 assert ids(record)==['base'] and dr.closure(d,cid)=={} and record['conditions']=={} and record['effects']==dict(dimensions=[],properties=[])
 decision=copy.deepcopy(old);decision['meaning_summary']=meaning
 decision['rejected_boundaries'].append(rationale)
 decision['status']='approved' if result=='approved' else 'needs_boundary_review'
 if result=='approved':decision['uncertainties']=[]
 for slot,dimension,target,prop,quote,why in extra:
  fact=dict(pointer='/content/definition',quote=quote,dimension=dimension,target=target,property=prop)
  decision['facts'].append(dict(fact,realization_id='base'))
  found=next((q for q in decision['roles'] if q['slot_id']==slot),None)
  if found:
   found['evidence'].append(fact);found['rationale']+=' '+why
  else:decision['roles'].append(dict(slot_id=slot,semantic_role=d['slot_catalog'][slot]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=why,evidence=[fact]))
 row={**dr.binding(d,cid,cache=cache),**decision,'schema':dr.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':dr.c.digest(p),'authored_decision':dict(file=str(output.relative_to(dr.ROOT)),item=len(amendments)+1,sha256=dr.c.digest(decision))}
 try:dr.validate_decision(row,d,binding_cache=cache)
 except Exception as e:raise ValueError((o,str(e))) from e
 amendments.append(dict(ordinal=o,candidate_id=cid,before_authored_file=oldfile,before_authored_row_sha256=dr.c.digest(old),reread_id=f'review_11870_12250-amend48-{o}-r1',model='gpt-6.1-sol',reasoning_effort='high',source_record_sha256=dr.c.digest(record),source_reread_complete=True,reference_reread_complete=True,after_proposal_conditions=copy.deepcopy(record['conditions']),after_proposal_effects=copy.deepcopy(record['effects']),after_proposal_reference_sha256={},native_qualification_issues_retained=copy.deepcopy(old['uncertainties']) if result=='approved' else [],reassessment_rationale=rationale,decision=decision))
assert {x['candidate_id'] for x in amendments}==set(before)
if '--write' in sys.argv:
 assert not output.exists(),'do not overwrite a frozen amendment'
 output.write_text(json.dumps(dict(schema='photo-codex-direct-review-amendment/v1',source_sha256=dr.c.digest(d),packet_sha256=dr.c.digest(p),amendments=amendments),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(count=len(amendments),statuses=dict(Counter(x['decision']['status'] for x in amendments)),resolved=[x['ordinal'] for x in amendments if x['decision']['status']=='approved'],pending=[x['ordinal'] for x in amendments if x['decision']['status']!='approved'],written='--write' in sys.argv)))
