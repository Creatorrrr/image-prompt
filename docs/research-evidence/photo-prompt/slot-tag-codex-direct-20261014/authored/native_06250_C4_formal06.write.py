"""Exact assembly of four individually reread C selections; no semantic inference/model.
Draft facts/units/owners are explicitly selected below after fresh source rereading.
"""
import sys,json,gzip,hashlib,copy
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(G/'scripts/photo_semantic_evidence.py')=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import photo_candidate_realizations as z
import native_reviews as nr
D=json.loads((R/'authored/native_06250_bare_props_01236_00259_00807_00924_C_20261015.json').read_text())
S=json.loads(gzip.decompress((R/'native-inputs/bare-prop-applications-plan-06/CURRENT-PROPOSAL.json.gz').read_bytes()))
assert c.digest(S)=='e6722134b6ca83eac12836512b2815a7d38b9e35e32cc121623705e7e01f738d'
# Four separately authored semantic decisions, not a bare-noun add rule.
DECISIONS={1236:'The expressly selected application adds one new astronaut-helmet scene prop, without a new head/person, wearing, occupation, space location, performance, material, color or placement. Korean helmet names only the helmet type component, not prop status. Original bare nouns do not uniquely imply addition.',259:'The expressly selected application adds one new socket-wrench prop, without worker/vehicle, repair, bolt contact, garage, material, color or placement. Both original fields literally remain English and name only the type component. No embedding is added. Original noun is not a universal add rule.',807:'The expressly selected application adds one new stethoscope prop, without doctor/patient/person, examination/contact, medical result, worn state, material, color or placement. Each original field names only the type; the explicit application alone grounds addition, existence and local one-object count.',924:'The expressly selected application adds one new conch-shell prop, without living conch, mermaid/animal/person, sea setting, sound, detailed shell structure, material, color or placement. Shell identity does not add an animal. Each bare field restates type only; explicit application grounds new/add/existence/local count.'}
for draft in D['records']:
 ordinal=draft['ordinal'];stem=f'review06250-{ordinal:05d}-06';P=R/'native-inputs/prepared'/stem
 assignment=json.loads((P/'ASSIGNMENT.json').read_text());inp=nr.artifact(ROOT,assignment['input']);cid=assignment['ids'][0]
 packet=json.loads((P/'PREPARED-PACKET.json').read_text());before=packet['original_records'][cid];after=packet['current_records'][cid]
 assert before==draft['source_before'] and after==draft['source_after']==S['candidates'][cid]
 assert packet['references'][cid]==packet['reference_bindings'][cid]=={}
 # Fresh manual selection of the exact authored C semantics, after all four whole sources and these fields were reread.
 facts=copy.deepcopy(draft['facts']);units=copy.deepcopy(draft['source_units']);owners=copy.deepcopy(draft['owner_maps'])
 assert len(facts)==3 and all(f['mode']=='effect' and f['pointer']=='/content/application_contract' for f in facts)
 assert [f['property'] for f in facts]==['entity.presence','props.type','entity.count']
 assert all(u['fact_refs']==['new_type'] for u in units[1:])
 # Only prop is a retrieval role. Local entity.count is not participant.count; presence adds an object, not primary subject.
 proof={'schema':e.SCHEMA,'meaning_sha256':e.meaning_sha256(after),'catalog_sha256':c.digest(S['slot_catalog']),'complete':True,
 'facts':facts,'source_units':units,'roles':{'prop':{'spec_sha256':c.digest(S['slot_catalog']['prop']),'scope':'whole_record','realization_ids':['base'],'fact_refs':['new_type'],'support_modes':['effect']}},
 'owner_maps':owners,'effect_sets':{'base':e.effect_set(after,'base')},'dependencies':{'base':[]},'reference_sha256':{},
 'guard_sets':{'base':{'source_conditions':[copy.deepcopy(after['conditions']),{}],'member_conditions':{}}},
 'profile_contracts':{'base':z.profile_contract(after,'base')},'review':{'basis':DECISIONS[ordinal]+' Fresh exact root06 input and whole original/current/5B/ownbinding/empty dependency closure reread. All three E remain permission-visible under subject/count locks. This approves the individually selected bounded application for root research review only.',
 'whole_source_reviewed':True,'source_correction':{'before_sha256':e.meaning_sha256(before),'after_sha256':e.meaning_sha256(after),'rationale':DECISIONS[ordinal]+' This is the explicit root-selected new application, preserving original fields/guards/provenance, rather than a claim about the original noun\'s unique interpretation.'},
 'original_review':{'candidate_id':cid,'source_record_sha256':packet['historical_compiled_rows'][cid]['source_record_sha256'],'catalog_sha256':packet['historical_compiled_rows'][cid]['catalog_sha256'],'decision_sha256':inp['original_decisions'][cid]['row_sha256'],'artifact':packet['original_compiled_artifacts'][cid]},
 'native_review':{'reviewer':'/root/review_06250_07250','method':'codex_subagent_direct_source_read','native_contract_sha256':'pending'}}}
 # Guard shape is exact technical serialization of the manually retained intrinsic human/no members, never an inferred condition.
 assert proof['guard_sets']['base']==e.source_guard_set(after,'base',S),e.source_guard_set(after,'base',S)
 proof['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(proof)
 record=copy.deepcopy(after);record['content']['role_evidence']=proof;e.validate(record,S['slot_catalog'],corpus={**S,'candidates':{**S['candidates'],cid:record}})
 delta=[{'pointer':'/content/application_contract','before_exists':False,'before':None,'after_exists':True,'after':after['content']['application_contract'],'reason':DECISIONS[ordinal]},
 {'pointer':'/effects','before_exists':True,'before':before['effects'],'after_exists':True,'after':after['effects'],'reason':'Explicit selected new-object application has presence/add_entity, type/set_value and local one-object count/set_value; retain all subject/count permission footprints.'}]
 req=inp['required_revisions'][cid]
 row={'candidate_id':cid,'ordinal':ordinal,'status':'approved','rationale':DECISIONS[ordinal], 'source_before':before,'source_after':after,'delta':delta,'original_compiled':inp['original_decisions'][cid],'proof':proof,'dependency_records':{},'reference_bindings':{},'source_reread_complete':True,'reference_reread_complete':True,'revision':{'prior_review':req['prior_review'],'memo_artifacts':req['memo_artifacts'],'rationale':'Fresh direct rereview after individual root C application selection and exact root06 input; complete current v4 facts/units/owners/three E, independent human policy and strict vacant introduced address. A/B/C historical drafts and source interpretation boundaries remain unchanged.'}}
 batch={'schema':nr.BATCH,'task_name':assignment['task_name'],'model':assignment['model'],'reasoning_effort':assignment['reasoning_effort'],'assignment_sha256':c.digest(assignment),'input_sha256':assignment['input']['sha256'],'prepared_count':1,'actual_read_count':1,'records':[row]}
 note={'schema':nr.NOTE,'task_name':assignment['task_name'],'model':assignment['model'],'reasoning_effort':assignment['reasoning_effort'],'assignment_sha256':c.digest(assignment),'input_sha256':assignment['input']['sha256'],'batch_sha256':c.digest(batch),'prepared_count':1,'actual_read_count':1,'whole_source_read_ids':[cid],'whole_dependency_read_ids':[cid]}
 O=R/'native_batches'/stem;O.mkdir(exist_ok=False)
 for name,value in [('BATCH.json',batch),('NOTE.json',note)]:
  (O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 print(ordinal,'full v4 literal proof passed',sha(O/'BATCH.json'))
