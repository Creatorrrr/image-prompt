"""Serialize only the explicit15166 reassessment; no registration/canonical/Git/network operations."""
import copy,hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as dr
import photo_candidate_realizations as pr
L=runpy.run_path(str(R/'authored/review_06250_07250_15166_amend_literals.py'))
D=dr.source();P=json.loads((R/'packets/15000-250.json').read_text());cid=P['ids'][166];record=D['candidates'][cid]
assert cid=='cand_10e70faca7705a7aa70b4dc580194f29'
assert record==P['records'][cid] and record['record_kind']=='visual_bundle' and pr.ids(record)==['base']
assert len(record['content']['components'])==15 and all(x['minimum_realizations']==1 for x in record['content']['components'])
assert record['conditions']=={} and len(record['effects']['properties'])==8
assert [x['property'] for x in record['effects']['properties']]==[x[0] for x in L['PARENT_EFFECT_SCOPE']]
assert len(dr.closure(D,cid))==10 and len(L['MEMBER_ASSESSMENTS'])==5
before_file='authored/review_06250_07250_15000_15250.json';before_bytes=(R/before_file).read_bytes()
assert hashlib.sha256(before_bytes).hexdigest()=='60619ad364782c41d0c78d72c5b2bd925827ed059f8243dfe22aa922a7de30d5'
before=json.loads(before_bytes)['decisions'][166];assert before['candidate_id']==cid and before['status']=='needs_boundary_review'
corrections=[dict(pointer=p,before=b,after=a,reason=r) for p,b,a,r in L['BOUNDARY_CORRECTIONS']]
after=dr.corrected_record(record,corrections)
assert after['content']['components']==record['content']['components'] and after['effects']==record['effects'] and after['conditions']==record['conditions']
assert after['content']['member_candidates']==record['content']['member_candidates']
assert after['content']['associated_profile_ids']==record['content']['associated_profile_ids']
assert pr.ids(after)==['base'] and pr.effects(after,'base')==record['effects']
roles={};facts=[]
for index,tag,dim,target,prop,quote,reason in L['FACTS']:
 pointer=f'/content/components/{index}/concept_units/0';assert dr.pointer(after,pointer)==quote
 fact=dict(pointer=pointer,quote=quote,dimension=dim,target=target,property=prop)
 if tag not in roles:roles[tag]=dict(slot_id=tag,semantic_role=D['slot_catalog'][tag]['semantic_role'],scope='whole_record',realization_ids=['base'],rationale='This role belongs to the adopted parent base conjunction itself, not to an automatically activated optional child. '+reason,evidence=[])
 roles[tag]['evidence'].append(fact);facts.append(dict(fact,realization_id='base'))
decision=dict(candidate_id=cid,meaning_summary=L['MEANING'],recommended_kind='visual_bundle',corrections=corrections,roles=list(roles.values()),facts=facts,rejected_boundaries=[L['REJECTED']],uncertainties=[],status='approved',all_roles_considered=True)
output=R/'authored/review_06250_07250_15166_amend.json'
compiled={**dr.binding(D,cid),**decision,'schema':dr.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':dr.c.digest(P),'authored_decision':dict(file=str(output.relative_to(dr.ROOT)),item=1,sha256=dr.c.digest(decision))}
dr.validate_decision(compiled,D)
member_ledger=[]
for mc,bid,profile,indices,assessment in L['MEMBER_ASSESSMENTS']:
 m=next(x for x in record['content']['member_candidates'] if x['candidate_id']==mc);b=D['slot_bindings'][bid];assert m['binding_id']==bid and b['candidate_id']==mc
 member_ledger.append(dict(member=copy.deepcopy(m),source_binding=copy.deepcopy(b),member_record_sha256=dr.c.digest(D['candidates'][mc]),associated_profile_id=profile,profile_record_sha256=dr.c.digest(D['candidates'][profile]),parent_component_pointers=[f'/content/components/{i}/concept_units/0' for i in indices],parent_positive_quotes=[dr.pointer(record,f'/content/components/{i}/concept_units/0') for i in indices],child_own_conditions=copy.deepcopy(D['candidates'][mc]['conditions']),child_own_effects=copy.deepcopy(D['candidates'][mc]['effects']),profile_own_conditions=copy.deepcopy(D['candidates'][profile]['conditions']),profile_own_effects=copy.deepcopy(D['candidates'][profile]['effects']),intended_binding_role='Historical garment_detail/direct optional binding is recorded without remapping; selected dependencies must retain their own conditions/effects and root must bind qualified roles explicitly.',assessment=assessment))
item=dict(ordinal=15166,candidate_id=cid,before_authored_file=before_file,before_authored_item=167,before_authored_row_sha256=dr.c.digest(before),before_authored_artifact_sha256=hashlib.sha256(before_bytes).hexdigest(),reread_id='review_06250_07250-15166-amend-r1',model='gpt-6.1-sol',reasoning_effort='high',source_record_sha256=dr.c.digest(record),catalog_sha256=dr.c.digest(D['slot_catalog']),reference_sha256=dr.binding(D,cid)['reference_sha256'],source_reread_complete=True,reference_reread_complete=True,after_proposal_conditions=copy.deepcopy(after['conditions']),after_proposal_effects=copy.deepcopy(after['effects']),full_after_proposal_record=after,full_after_proposal_reread=True,reassessment_rationale=L['RATIONALE'],previous_uncertainty_disposition='Resolved by distinguishing optional parent adoption, mandatory adopted-parent conjunction, local OR and independently selected optional dependencies. The previous review scope interpretation was incorrect; the source own components/effects were not optionalized.',parent_effect_scope=[dict(property=prop,source_effect=copy.deepcopy(next(x for x in record['effects']['properties'] if x['property']==prop)),component_pointers=[f'/content/components/{i}/concept_units/0' for i in indices],exact_parent_quotes=[dr.pointer(record,f'/content/components/{i}/concept_units/0') for i in indices],assessment=assessment) for prop,indices,assessment in L['PARENT_EFFECT_SCOPE']],member_binding_ledger=member_ledger,native_qualification=dict(actual_realizations=['base'],semantic_proposal_and_current_decision_validation_passed=True,parent_fifteen_components_and_eight_effects_preserved=True,dependency_selection_contract_expected=['required','explicit_optional'],unselected_optional_adds_conditions_effects_adoption=False,associated_profile_guard_preserved=True,runtime_selection_integration_executed=False,native_or_catalog_followup_roles_proposed=[],canonical_source_applied=False),decision=decision)
body=dict(schema='photo-codex-direct-review-amendment/v1',source_sha256=dr.c.digest(D),source_snapshot_file_sha256=hashlib.sha256((R/'SOURCE.json.gz').read_bytes()).hexdigest(),catalog_sha256=dr.c.digest(D['slot_catalog']),packet_sha256=dr.c.digest(P),packet_file_sha256=hashlib.sha256((R/'packets/15000-250.json').read_bytes()).hexdigest(),amendments=[item])
if '--write' in sys.argv:
 assert not output.exists(),'Never overwrite frozen amendment';output.write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=decision['status'],roles=len(roles),facts=len(facts),parent_components=len(after['content']['components']),parent_effects=len(after['effects']['properties']),closure=10,bindings=5,actual_rids=pr.ids(after),before_row_sha256=dr.c.digest(before),before_artifact_sha256=hashlib.sha256(before_bytes).hexdigest(),after_authored_sha256=hashlib.sha256(output.read_bytes()).hexdigest() if output.exists() else None,source_record_sha256=dr.c.digest(record),written='--write' in sys.argv),ensure_ascii=False))
