"""Freeze this worker's unsigned draft provenance; no original-review rewrite."""
import json,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'authored'
sys.path.insert(0,str(Path.cwd()/'skills/photo-prompt-image-generator/scripts'))
import photo_candidate_corpus as c
import photo_semantic_evidence as s
I=json.loads((R/'native-inputs/diverse-08250-11128-12165-17437.json').read_text())
J=json.loads((A/'native_resolution_08250_revision4_sources.json').read_text())
F=json.loads((A/'native_resolution_08250_revision4_facts.json').read_text())
K=json.loads((A/'native_resolution_08250_revision4_checks.json').read_text())
CAT=json.loads((R/'CATALOG-FINAL-142.json').read_text())
assert c.digest(CAT)=='e7ad376ae1e195ada8268259015b29751f33a24f47e23899c7b7e9329b4a3e28'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reviews={}
for cid in J['resolution_proposed_records']:
 old=I['original_registered_reviews'][cid]
 current=json.loads(Path(old['file']).read_text())['decisions'][old['item']-1]
 assert current['candidate_id']==cid
 reviews[cid]={'frozen_input_original':{k:v for k,v in old.items() if k!='row'},'frozen_input_row_verified':c.digest(old['row'])==old['row_sha256'],'current_observed_locator':{'artifact':old['file']+'#item='+str(old['item']),'row_sha256':c.digest(current),'source_record_sha256':current['source_record_sha256']},'same_row_as_initial_input':current==old['row'],'unsigned_no_original_review_rebinding':True}
cid=F['candidate_id'];assert reviews[cid]['current_observed_locator']['row_sha256']=='5589091c1c3a1fb7cd17f66c32f9bf171b2900b426643e3675faa40ca6a6d92c'
chains=[]
for name in ['native_resolution_08250_sources.json','native_resolution_08250_revision2_sources.json','native_resolution_08250_revision3_sources.json','native_resolution_08250_revision4_sources.json']:
 p=A/name;x=json.loads(p.read_text());rec=x['resolution_proposed_records'][cid]
 chains.append({'path':str(p),'raw_sha256':sha(p),'record_sha256':c.digest(rec),'meaning_sha256':s.meaning_sha256(rec),'historical_preparation_status':x['status']})
files=sorted(p for p in A.glob('native_resolution_08250_revision[34]_*') if p.is_file())
code=[Path('skills/photo-prompt-image-generator/scripts')/x for x in ['photo_semantic_evidence.py','photo_candidate_realizations.py','photo_candidate_corpus.py','visual_profile_contracts.py','photo_contracts.py']]+[Path('skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.py')]
note={
 'schema':'native-resolution-revision4-worker-note/v1','task_name':'/root/review_08250_09250','model':'gpt-6.1-sol','reasoning_effort':'high',
 'status':'immutable_unsigned_source_and_manual_fact_inventory_draft_awaiting_fresh_input_and_v4_handoff',
 'preparation_and_reading':{
  'source_prepared':True,'after_11128_complete_unchanged_source_directly_read':True,
  'after_17437_complete_root_conditions_effects_components_discovery_obligations_semantics_directly_read':True,
  'after_17437_actual_selected_body_RIDs_directly_read':18,'required_reference_closure':{},
  'read_method':'Direct whole-source reading through lossless exact subtree references and reversible literal deltas. Referenced revision2/3 values had already been directly read. Revision4 has only6 property spelling changes; content and conditions are exactly the directly reread revision3 values. Reader caches are displays, not automated reading certification.',
  'historical_prepared_status_preserved':'Source artifacts retain their preparation-time status. This separate note records the later actual direct reread; no old file was re-signed.'},
 'manual_semantic_authoring':{
  'decisions':'I directly judged the actual source positive clauses, selected manifestations, original paraphrases and render gates, then authored exact quote/mode/value/operation/owner/requires lists in Python literals. These are not inferred from prior5B tags or source keywords.',
  'literal_expansion':'3555 is the count of expanded fact rows, not3555 independently composed semantic assertions. Scripts repeat the explicitly authored bilingual clause lists only at explicitly enumerated source paths and the manually authored18RID choice table. Each combined selected body had been directly read. Identical repeated clauses retain the same decisions; no model/classifier decides a mode, role or owner.',
  'roles':'The role/property/mode table is an explicit manual final142-spec decision. Script collection of matching already-authored fact IDs is literal indexing, not discovery of new tags.',
  'nonfacts':'498 schema-field/review-scale/negative-lexical source units are explicitly nonsemantic. Optional-selection and owner-application controls, negative exclusions and existing-only context remain in exact canonical proposal text and source guards; they are not fabricated positive metadata facts.',
  'remaining_proof_boundary':'Pointer coverage and fact count do not prove every judgement correct. This inventory is unsigned and has no attached native proof. Full guard/profile consumption, v4 full/compact admission and final audit remain unverified.'},
 'actual_inventory':{'candidate_id':cid,'RIDs':18,'facts':3555,'source_units':1011,'nonsemantic_units':498,'semantic_string_units':513,'source_guard_applications':51,
  'by_RID':[{k:x[k] for k in ['rid','fact_count','source_unit_count','mode_counts']} for x in F['summaries']],
  'owner_maps':F['owner_maps'],'dependencies':F['dependencies'],'reference_sha256':{},
  'no_common_second_person':'Only existing actor/main_subject and owned face/primary_face are common. Existing helper/secondary_subject is active only in6 selected help RIDs. No relationship_target or common counterpart is added.'},
 'root_adjudications_applied':J['root_adjudication'],
 'quote_specific_literal_refinements':[
  'adult peer / peer supports participant.role.peer, not independent rival declaration. Whole application separately supplies the peer-rival prerequisite.',
  'adult haughty eye baseline remains readable / 성인다운 도도한 눈의 기본선은 읽힌다 supports frozen adult face-presentation preservation, not an independent declared/biological-age assertion.',
  'Local mouth-corner softening gate value does not alone assert brief duration; exact selected-body clauses separately supply the brief local manifestation.',
  'Cheek/recovery gate anaphors refer only to their explicit selected manifestation. No specific red hue, literal heat, gratitude, hidden suppression, completed recovery or elapsed sequence is inferred.'],
 'exact_spelling_revision':{'source_property_fields':6,'fact_property_fields':48,'before':'event.small_setback','after':'situation.small_setback','all_other_fact_fields_identical_to_revision3':True,'addresses_and_before_after':str(A/'native_resolution_08250_revision4_checks.json')},
 'roles_manually_decided_against_final142':list(F['roles']),'sexual_context_tags_added':False,
 'catalog142_canonical_sha256':c.digest(CAT),'input_canonical_sha256':c.digest(I),'proposed_meaning_sha256':s.meaning_sha256(J['resolution_proposed_records'][cid]),
 'original_review_provenance':reviews,
 'root_historical_provenance_adjudication':'Root reports207213a11 historical sparse amendment changed current17437 compiled row, preserving old raw row/file in revisions/ROOT-NORMALIZE-08250-17437-* archive and REVISION/manifest. Fresh formal native input will explicitly select current item188 SHA5589091c... . This worker preserves initial30678input/oldpilot hashes and does not automatically overwrite original_review.',
 'source_correction_chain':chains,
 'executed_isolated_checks':{
  'source_quote_shape_same_RID_requires_owner_coverage_and_effect_set':True,'selected_profile_compiler_RIDs':18,'independent_literal_request_frozen_obligation_positive_RIDs':18,
  'missing_wrong_owner_negative_cases':sum(2*len(x['missing_wrong_owner_negatives']) for x in K['checks']),
  'actual_property_lock_negative_cases':sum(len(x['all_actual_property_lock_negatives']) for x in K['checks']),
  'whole_age_lock_negative_RIDs':18,'same_value_age_property_lock_negative_RIDs':18,
  'whole_appearance_lock_negative_RIDs':18,'appearance_boundary':'Whole cue is denied by its independent appearance styling/eye effects. Isolated age effect is not automatically an appearance effect; no cross-dimension alias was added.',
  'adult_permission_without_age_fact_rejected':True,
  'scope':'Minimal independently authored literal core/request fixtures plus current neutral reader/exact typed matcher/permission primitives. Not production normalized cores or v4 full/compact/native-source-guard admission.'},
 'runtime_concurrency':'native_evidence implemented v4 while this worker authored facts. Earlier revision3 isolated selected_contract passed before the change. Current revision4 mini inventory is correctly rejected: native v4 guard/profile inventory missing. No monkeypatch, fake complete proof or cap bypass was supplied. Hashes are an observed implementation-in-progress snapshot, not a frozen handoff.',
 'current_mini_contract_rejections':[{'rid':x['rid'],'reason':x['current_selected_contract_expected_rejection']} for x in F['summaries']],
 'generic_resource_contract':'Root authorized implementation of generic maxRID32/units2048/facts4096. Actual3555/1011/18 fits those budgets; this worker changes no cap/schema and has no final handoff certification.',
 'stage6_8_conditions':'No actual member binding or candidate reference is removed in these two records.11128 preserve-if-established constraints remain explicit source guards. A future old member binding removal still needs exact applicability conjunction and source provenance through all consumers; positive requirements or ignored conditions fields do not preserve it.',
 'native_proof_attached':False,'production_native_qualified_count':0,
 'authored_artifacts':{str(p):sha(p) for p in files},'observed_code_sha256':{str(p):sha(p) for p in code},
 'old_frozen_artifacts_changed':False,'canonical_operating_git_model_or_network_writes_by_this_worker':False}
p=R/'worker-notes/native-resolution-08250-revision4-full-inventory.json';p.write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'note':str(p),'note_raw_sha256':sha(p),'source_raw_sha256':sha(A/'native_resolution_08250_revision4_sources.json'),'facts_raw_sha256':sha(A/'native_resolution_08250_revision4_facts.json'),'checks_raw_sha256':sha(A/'native_resolution_08250_revision4_checks.json'),'facts':3555,'units':1011},ensure_ascii=False,indent=2))
