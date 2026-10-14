"""Validate17 separately authored re-read decisions; never register or edit source."""
import copy,hashlib,json,runpy,sys
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as dr
import photo_candidate_realizations as pr
L=runpy.run_path(str(R/'authored/review_11870_12250_final17_reread_literals.py'));A=L['A']
p=json.loads((R/'packets/12000-250.json').read_text());d=dr.source()
assert dr.c.digest(d)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
assert dr.c.digest(d['slot_catalog'])=='4723660c37d3f665f883a81f0e8d35b8c690307406d18d63ade654527d5bec9c'
assert dr.c.digest(p)=='c5b08af3da0123f2736c87aa53b8fd8aa011a866e2a3b2aef83718f399acc2fc'
prior_file='authored/review_11870_12250_amend48.json';prior=json.loads((R/prior_file).read_text());before={x['candidate_id']:x['decision'] for x in prior['amendments'] if x['decision']['status']=='needs_boundary_review'}
assert len(before)==17 and len(A)==17 and len({x[0] for x in A})==17
output=R/'authored/review_11870_12250_final17_reread.json';rows=[];cache={}
for o,result,meaning,rationale,extra in A:
 cid=p['ids'][o-12000];old=before[cid];record=d['candidates'][cid]
 assert pr.ids(record)==['base'] and dr.closure(d,cid)=={} and record['conditions']=={} and record['effects']==dict(dimensions=[],properties=[])
 decision=copy.deepcopy(old);decision['meaning_summary']=meaning;decision['rejected_boundaries'].append(rationale)
 decision['status']='approved' if result=='approved' else 'needs_boundary_review'
 if result=='approved':decision['uncertainties']=[]
 for slot,dim,owner,prop,quote,why in extra:
  f=dict(pointer='/content/definition',quote=quote,dimension=dim,target=owner,property=prop)
  decision['facts'].append(dict(f,realization_id='base'))
  assert slot not in {x['slot_id'] for x in decision['roles']}
  decision['roles'].append(dict(slot_id=slot,semantic_role=d['slot_catalog'][slot]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale=why,evidence=[f]))
 if o==12165:
  assert pr.MECHANISM_PROJECTION_CONTRACT=='photo-relationship-realization-content/v1'
  decision['corrections']=[dict(pointer='/effects',before=copy.deepcopy(record['effects']),after=copy.deepcopy(L['PROPOSED_12165_EFFECTS']),reason='Make the existing exclusive practical-makeup OR reflected-color choices explicit, with empty shared effects and separate owned effects. No hue, light source, actor, identity, guard or kind is added.'),dict(pointer='/content/realization_content',before=record['content'].get('realization_content'),after=copy.deepcopy(L['PROPOSED_12165_CONTENT']),reason='Preserve complete selected English/Korean text including selected definition and shared visible social-action evidence in either branch. Canonical positive OR text and relationship_mechanism kind remain unchanged.')]
  for slot,rid,dim,prop,text,why in [
   ('cheek_makeup','practical_makeup','appearance','makeup.cheek.placement',L['MAKEUP_EN'],'Only the selected practical-makeup branch owns cosmetic placement on the stated cheek area; no pigment hue or emotion is supplied.'),
   ('color','reflected_color','color','color.cheeks.reflected_appearance',L['REFLECTED_EN'],'Only the selected reflected-color branch owns local reflected cheek appearance; no illumination source, temperature or fixed hue is supplied.')]:
   f=dict(pointer=f'/content/realization_content/{rid}/definition',quote=text,dimension=dim,target='declared_cheeks',property=prop)
   decision['facts'].append(dict(f,realization_id=rid))
   decision['roles'].append(dict(slot_id=slot,semantic_role=d['slot_catalog'][slot]['semantic_role'],scope='positive_alternative',realization_ids=[rid],rationale=why,evidence=[dict(f,realization_id=rid)]))
 corrected=dr.corrected_record(record,decision['corrections'])
 if o==12165:
  assert pr.ids(corrected)==['practical_makeup','reflected_color']
  for rid,full in corrected['content']['realization_content'].items():
   projection=pr.project_content(corrected,rid)
   assert projection['definition']==full['definition'] and projection['en']==full['en'] and projection['ko']==full['ko']
 row={**dr.binding(d,cid,cache=cache),**decision,'schema':dr.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':dr.c.digest(p),'authored_decision':dict(file=str(output.relative_to(dr.ROOT)),item=len(rows)+1,sha256=dr.c.digest(decision))}
 try:dr.validate_decision(row,d,binding_cache=cache)
 except Exception as e:raise ValueError((o,str(e))) from e
 item=dict(ordinal=o,candidate_id=cid,before_authored_file=prior_file,before_authored_row_sha256=dr.c.digest(old),reread_id=f'review_11870_12250-final17-{o}-r2',model='gpt-6.1-sol',reasoning_effort='high',source_record_sha256=dr.c.digest(record),catalog_sha256=dr.c.digest(d['slot_catalog']),reference_sha256={},source_reread_complete=True,reference_reread_complete=True,after_proposal_conditions=copy.deepcopy(corrected['conditions']),after_proposal_effects=copy.deepcopy(corrected['effects']),native_qualification_issues_retained=copy.deepcopy(old['uncertainties']) if result=='approved' else [],reassessment_rationale=rationale,decision=decision)
 if o==12165:item.update(full_after_proposal_record=corrected,full_after_proposal_reread=True,tooling_dependency=dict(contract=pr.MECHANISM_PROJECTION_CONTRACT,source_meaning_and_branch_roles_approved=True,current_native_shape_and_decision_validation_passed=True,shared_tooling_edited_by_this_worker=False,toolworker_final_tests_and_root_integration='not_claimed_pending_root_verification',canonical_source_applied=False))
 rows.append(item)
assert {x['candidate_id'] for x in rows}==set(before)
body=dict(schema='photo-codex-direct-review-amendment/v1',source_sha256=dr.c.digest(d),source_snapshot_file_sha256=hashlib.sha256((R/'SOURCE.json.gz').read_bytes()).hexdigest(),catalog_sha256=dr.c.digest(d['slot_catalog']),packet_sha256=dr.c.digest(p),packet_file_sha256=hashlib.sha256((R/'packets/12000-250.json').read_bytes()).hexdigest(),amendments=rows)
if '--write' in sys.argv:
 assert not output.exists(),'never overwrite frozen output';output.write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(count=len(rows),statuses=dict(Counter(x['decision']['status'] for x in rows)),approved=[x['ordinal'] for x in rows if x['decision']['status']=='approved'],pending=[x['ordinal'] for x in rows if x['decision']['status']!='approved'],source_corrections_12165='typed-proposal-with-kind-preserving-native-branches',toolworker_final_tests_and_root_integration='not_claimed',written='--write' in sys.argv)))
