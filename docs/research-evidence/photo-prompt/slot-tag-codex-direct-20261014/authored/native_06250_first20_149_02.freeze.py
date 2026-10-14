"""Byte/delta bookkeeping after explicit human source/proposal/spec reads.
Does not assign semantic statuses or modify any prior artifact.
"""
import sys,json,copy,hashlib
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
raw=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import native_reviews as nr
sys.path[:]=[str(G/'scripts'),str(G/'precore')]+[p for p in sys.path if p not in {str(ROOT/'skills/photo-prompt-image-generator/scripts'),str(G/'scripts'),str(G/'precore')}]
P=R/'native-inputs/prepared/review06250-00000-00020-149-02';O=R/'native_batches/review06250-00000-00020-149-02'
A=json.loads((P/'ASSIGNMENT.json').read_text());I=nr.artifact(ROOT,A['input']);K=json.loads((P/'PREPARED-PACKET.json').read_text());S=nr.artifact(ROOT,I['current_snapshot']);B=json.loads((O/'BATCH.json').read_text());D=json.loads((O/'DIAGNOSTIC.json').read_text())
Q=R/'authored/native_06250_first20_149_02.source-alternatives.json';q=json.loads(Q.read_text())
assert len(q['records'])==14 and len({r['candidate_id'] for r in q['records']})==13
proposal_read=[]
for row in q['records']:
 cid=row['candidate_id'];before=row['source_before'];after=row['source_after']
 assert before==S['candidates'][cid] and after==nr.apply_delta(before,row['delta'])
 assert before['content']=={k:v for k,v in after['content'].items() if k!='application_contract'}
 assert before['conditions']==after['conditions'] and before['provenance']==after['provenance']
 assert set(before['effects']['dimensions'])<=set(after['effects']['dimensions'])
 assert row['source_before_sha256']==c.digest(before) and row['source_after_sha256']==c.digest(after)
 c.validate_conditions(after['conditions'],cid);c.validate_effects(after['effects'],cid)
 proposal_read.append({'ordinal':row['ordinal'],'candidate_id':cid,'alternative_id':row['alternative_id'],'whole_after_actually_read':True,'source_after_canonical_sha256':c.digest(after),'source_after_meaning_sha256':e.meaning_sha256(after),'current_before_canonical_sha256':c.digest(before),'editorial_selection':False,'native_proof':None})

# Explicit read inventory, not semantic inference from neighbor lists or SHA alone.
specs=['genre','medium','lens','motion_rendering','mood','location','light_type','light_quality','time_of_day','aesthetic_trend','world','capture_context','capture_configuration','staging_degree','camera_type','focus','depth_of_field','image_detail','camera_movement','physical_motion','action','body_pose','contact_point','hand_pose','background_element','environment_detail','publication_caption_context','space_condition','visible_text','aftermath_trace','character_contrast','character_intent','narrative_clue','offscreen_context','participant_role','proxemics','social_cue','lighting','light_color','light_direction','light_intensity','light_shape','shadow_relation','exposure']
guides=['native-v3-authoring-guide-20261014_v2.md','native-v4-authoring-supplement-20261014.md','native-owner-selector-authoring-supplement-20261014.md','native-08250-generic-role-view-supplement-20261015-v1.md']
legacy_path=ROOT/'docs/research-evidence/photo-prompt/slot-retrieval-stage05-20261012/CONTROLLED-FINAL-SOURCE.json';L=json.loads(legacy_path.read_text())
source_reads=[]
for ordinal,cid in zip(A['ordinals'],A['ids']):
 before=K['original_records'][cid];current=K['current_records'][cid]
 kind,slot,key=before['provenance'][0]['source'].split(':');assert kind=='slot'
 items=[(i,x) for i,x in enumerate(L['slots'][slot]) if x['id']==key];assert len(items)==1
 index,legacy=items[0];assert c.digest(legacy)==before['provenance'][0]['sha256']
 own=[v for v in S['slot_bindings'].values() if v['candidate_id']==cid];assert len(own)==1
 assert K['references'][cid]==K['reference_bindings'][cid]=={} and current['conditions']=={}
 assert own[0]['conditions']=={'subject_applicability':{}}
 if ordinal in [3,4,5,9,16,17,18]:
  condition_judgement='No source intrinsic guard or substantive own-binding guard is present. Keep the actually empty intrinsic and subject_applicability values; do not create an entity/category/domain requirement from tags or slot metadata. Preserve optional presentation role, semantic_role and exact weight as a proposed relationship intent; no binding is created, deleted or retargeted.'
 elif ordinal==14:
  condition_judgement='The old optional world relationship has no substantive guard and cannot supply positive world-system meaning. No new binding is retargeted. The separate aesthetic proposal needs current-spec policy treatment and root selection; original setting mutation footprint remains in the proposed source.'
 else:
  condition_judgement='Actual intrinsic and old own-binding guard bodies are empty; they do not discharge the unresolved application. Proposed new source/receiver/path/theme obligations are editorial additions requiring root selection and fresh manually grounded P/guard witnesses. No whole-condition copy, metadata category, automatic target or ID retarget is used.'
 source_reads.append({'ordinal':ordinal,'candidate_id':cid,'original_source_sha256':c.digest(before),'current_source_sha256':c.digest(current),'original_compiled':I['original_decisions'][cid],'whole_legacy_original':{'file':str(legacy_path.relative_to(ROOT)),'pointer':'/slots/'+slot+'/'+str(index),'entry':legacy,'canonical_sha256':c.digest(legacy),'source_provenance_match':True,'whole_entry_read':True},'actual_rids':['base'],'whole_original_current_exact5Brow_ownbindings_read':True,'whole_reference_closure_read':True,'reference_cids':[],'reference_binding_ids':[],'actual_own_binding':own[0],'binding_condition_judgement':condition_judgement,'status':B['records'][ordinal]['status']})

files=[P/n for n in ['INPUT.json','ASSIGNMENT.json','PREPARED-PACKET.json','PREPARATION.json']]+[O/n for n in ['BATCH.json','NOTE.json','DIAGNOSTIC.json']]+[R/'authored'/n for n in ['native_06250_first20_149_02.read.py','native_06250_first20_149_02.write.py','native_06250_first20_149_02.check.py','native_06250_first20_149_02.proposals.py','native_06250_first20_149_02.source-alternatives.json','native_06250_first20_149_02.freeze.py']]+[R/'native-inputs/first20-catalog149-recheck-plan-15'/n for n in ['PLAN.json','ROOT-REVIEW-REQUIREMENTS.json']]+[R/'CATALOG-FINAL-149-V6.json',legacy_path]
pins={str(p.relative_to(ROOT)):{'raw_sha256':raw(p),'byte_count':p.stat().st_size} for p in files}
result={'schema':'photo-fresh-first20-native149-worker-note/v1','task_name':'/root/review_06250_07250','model':'gpt-6.1-sol','reasoning_effort':'high','range':[0,20],'assignment_sha256':c.digest(A),'input_sha256':A['input']['sha256'],'current_source_sha256':c.digest(S),'catalog_sha256':c.digest(S['slot_catalog']),'generation':str(G),'actual_runtime_modules':D['actual_modules'],'artifact_pins':pins,
 'counts':{'prepared_count':20,'actual_whole_original_current_exact5B_binding_closure_reads':20,'actual_whole_hash_matched_legacy_entry_reads':20,'fresh_research_approved':7,'pending':13,'diagnostic_reviewed':0,'fresh_native_proofs':7,'full_compact_x_binding_cases':28,'root_acceptance':0,'operating_native':0,'source_current_applied':0,'proposed_unique_CIDs':13,'proposed_whole_after_variants':14,'actual_whole_new_proposal_after_reads':14,'root_editorial_source_selections':0},
 'source_reads':source_reads,'proposal_after_reads':proposal_read,'full_specs_actually_read':[{'id':key,'canonical_sha256':c.digest(S['slot_catalog'][key]),'whole_spec_read':True} for key in specs],'guide_reads':[{'file':str((R/'worker-notes'/name).relative_to(ROOT)),'raw_sha256':raw(R/'worker-notes'/name),'whole_read':True} for name in guides],
 'manual_boundaries':['This is separate from the frozen [250,1250) and [8250,9250) bulk drafts and the historical root first20 proof. Their files, statuses, signatures and hashes remain unchanged.',
 'Fresh approved ordinals 3/4/5/9/16/17/18 are individually judged against exact current65 effects, full primary source units and full149 specs. The coincident historical 7/13 tally is not a status conversion.',
 'Actual source reread covers 20 assigned records and their empty dependency closure, not the full18250 snapshot. Full snapshot hashes bind input history, not a semantic-read claim.',
 'An initial oversized metadata dump was truncated and credited zero source/spec read. Every counted record was then displayed in untruncated four-record calls; full used/neighbor specs were read in separately bounded groups, plus all20 whole legacy entries after exact provenance SHA matching.',
 'All seven image/scene/camera effects retain current canonical targets/properties. No desired effect value is fabricated as prerequisite. Explicit empty per-fact requires/receivers reflect the manually judged lack of a separate source prerequisite or receiver for those image, scene or recording-camera attributes.',
 'The14 proposal afters were read completely in groups4/4/3/3 after serialization; their creation artifact deliberately retains actual_whole_after_read_count0 at preparation. This later immutable attestation records actual14 reads across13 unique CIDs. No proposal is signed against current65.',
 'Lighting proposals explicitly select an existing-source/receiver application as an editorial alternative, not as the only possible meaning or a universal existing-only rule. Carrier/relation/scope witnesses are still unresolved. Named-lighting-look role gaps stay pending. Golden-hour alternatives are newly proposed interpretations, not original OR branches.',
 'Pet/food/interior genre qualifiers remain whole genre values and explicit theme obligations. Proposed independent compatibility restrictions are editorial additions, not automatic carrier or new-entity inference. Travel/street genre alternatives do not assert factual journey or physical location.',
 'Dieselpunk proposal keeps the actual original setting dimension and a setting-owned permission effect, exposes no world-system fact and is not automatically converted into style or context/no-op. Exact manual role-view support and root source selection remain pending.',
 'All full/compact tests are explicitly authored isolated request fixtures with independently declared neutral owners, not user request execution, native core certification, production adoption, generated pixels or user acceptance. Source/role truth still requires root review. No network/provider/model/Git/canonical/runtime/registry changes occurred.'],
 'pending_action':'Root may independently select or reject the explicit whole before/after alternatives, then prepare new exact source/input/assignment for fresh proof. Until then thirteen current-input rows remain pending; proposed source/type/owner/guard choices do not become approved through shape checks.'}
p=R/'worker-notes/native-06250-first20-149-02-final-20261015.json';assert not p.exists();p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(p,raw(p));print('all proposal deltas/retained dimensions/whole legacy SHA matches checked; final native root acceptance0')
