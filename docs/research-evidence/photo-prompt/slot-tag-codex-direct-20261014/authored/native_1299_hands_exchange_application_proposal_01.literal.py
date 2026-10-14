"""Read-only research proposal emitter. No production/native proof/status writes."""
import copy, gzip, hashlib, json
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014')
CID='cand_2e72784a26885ceaa1d645d25bd9a468'
def sha(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def file_info(p):return {'file':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
current_path=R/'native-inputs/catalog149-source-pool-plan-09/CURRENT-PROPOSAL.json.gz'
current=read(current_path);before=current['candidates'][CID]
assert sha(before)=='08f25720f6c1c234a428db16034db49ed2a7acd0d6878fbefe643f7b56abce2a'
original_path=R/'SOURCE.json.gz';original=read(original_path)['candidates'][CID]
assert original==before
catalog_path=R/'CATALOG-FINAL-149-V6.json';catalog=read(catalog_path)
assert catalog==current['slot_catalog'] and len(catalog)==149
bindings=[x for x in current['slot_bindings'].values() if x['candidate_id']==CID]
provenance_path=Path('docs/research-evidence/photo-prompt/slot-retrieval-stage05-20261012/CONTROLLED-FINAL-SOURCE.json')
provenance=read(provenance_path)['slots']['composition'];entry=next(x for x in provenance if x['id']=='hands_only_exchange_macro')
assert sha(entry)==before['provenance'][0]['sha256']
compiled_path=R/'decisions/review_01250_02250_01250_01500.json';compiled=next(x for x in read(compiled_path)['decisions'] if x['candidate_id']==CID)
formal_path=R/'native_batches/review11870-01250-01300-04/BATCH.json';formal=read(formal_path)['records'][49]
assert formal['candidate_id']==CID
prior_path=R/'authored/native_remaining12_owner_scope_revision_03.json';prior=next(x for x in read(prior_path)['records'] if x['ordinal']==1299)
# The following strings and decisions are manually authored, not inferred from metadata.
def ep(target):return {'kind':'source_target','candidate_id':CID,'target':target}
def point_rule(i,kind,**fields):return {'id':i,'kind':kind,**fields}
def each(i,rule):return {'id':i,'kind':'for_each_member','scope':ep('counterpart_hands'),'member_variable':'hand','rule':rule}
member={'kind':'bound_member','variable':'hand'}
hand_value={'type':'body.part.kind/v1','value':'hand'}
clauses=[
 'Editorial application choice: render the exchange as reciprocal visible hand gestures among the selected existing hands; this is a chosen interpretation of exchange, not a uniquely entailed reading of the original label.',
 'Use one independently declared existing initiating hand and the complete nonempty independently declared existing counterpart-hands scope selected by the caller; do not construct that scope by subtracting or discovering members from this candidate.',
 'Each counterpart hand must be explicitly disjoint from the initiating hand. The initiating hand must be part of the selected existing initiating owner, and every counterpart hand must be part of the selected existing counterpart owner. The two owner selections may identify the same actual owner or different actual owners; no person count or total hand count is asserted.',
 'Every selected hand must have independently grounded existing entity presence and an exact body.part.kind/v1 value hand. This proposed hand-kind protocol is an additional explicit authoring requirement, not an existing common atomic hand-presence default or an inference from roles, category or words.',
 'Set the image shot scale to macro and change the participant framing so that only the selected participating hand regions of the selected owners are visible. This deliberately chooses participant hands-only coverage; it does not exclude every non-hand scene object from the entire frame. Root must choose this scope explicitly before application.',
 'Perform the reciprocal visible hand-gesture exchange on the initiating hand and on every counterpart hand. The performed exchange, macro shot scale and hands-only participant coverage are effects; none is a prerequisite, preserved existing action, contextual label or no-op.',
 'The action and framing effect scopes include every selected actual hand and both selected actual owners, with explicit canonical aliases and part ownership retained. No hand, person, exchanged object, contact, finger pose, camera hardware, focal length, focus plane, depth of field or completed ownership transfer is introduced or inferred.'
]
after=copy.deepcopy(before);after['content']['application_contract']=' '.join(clauses)
after['conditions']={'native_guards':{'schema':'photo-native-source-guards/v3','rules':[
 point_rule('initiating_hand_owned','owner_relation',relation='part_of',left=ep('initiating_hand'),right=ep('initiating_owner')),
 point_rule('initiating_hand_kind','frozen_value',owner=ep('initiating_hand'),dimension='subject',property='body.part.kind',value=hand_value),
 each('each_counterpart_owned',point_rule('owned','owner_relation',relation='part_of',left=member,right=ep('counterpart_owner'))),
 each('each_counterpart_separate',point_rule('separate','owner_relation',relation='disjoint',left=member,right=ep('initiating_hand'))),
 each('each_counterpart_hand_kind',point_rule('hand_kind','frozen_value',owner=member,dimension='subject',property='body.part.kind',value=hand_value))
]}}
properties=[{'dimension':'framing','target':'image','property':'shot.scale'},
 {'dimension':'framing','target':'image','property':'framing.coverage'},
 {'dimension':'action','target':'initiating_hand','property':'action.interaction.exchange'},
 {'dimension':'action','target':'counterpart_hands','property':'action.interaction.exchange'}]
after['effects']={'dimensions':['framing','action'],'properties':properties}
plan_rows=[]
for target,selector in [('image',{'kind':'core_role','role':'image'}),('initiating_hand',{'kind':'selected_existing_owner'}),('initiating_owner',{'kind':'selected_existing_owner'}),('counterpart_hands',{'kind':'selected_existing_member_scope','scope_schema':'photo-frozen-existing-member-scope/v1','target_semantics':'each_member','receiver_semantics':'all_members'}),('counterpart_owner',{'kind':'selected_existing_owner'})]:
 plan_rows.append({'target':target,'origin':'existing','introduced_by':None,'selector':selector})
owner_plan={'schema':'photo-native-owner-bindings/v4','bindings':plan_rows}
intent=[]
for target in ['initiating_hand','initiating_owner','counterpart_hands','counterpart_owner']:
 intent.append({'mode':'prerequisite','dimension':'subject','target':target,'property':'entity.presence','value':{'type':'entity.presence/v1','value':'present'},'source_quote':clauses[1] if 'hand' in target else clauses[2]})
for target in ['initiating_hand','counterpart_hands']:
 intent.append({'mode':'prerequisite','dimension':'subject','target':target,'property':'body.part.kind','value':hand_value,'source_quote':clauses[3],'protocol_status':'proposed custom exact typed fact; not shipped common atomic hand vocabulary'})
rx=['initiating_hand','initiating_owner','counterpart_hands','counterpart_owner']
for prop,value in [('shot.scale',{'type':'shot.scale/v1','value':'macro'}),('framing.coverage',{'type':'framing.coverage/v1','value':'only_selected_participating_hands_of_selected_owners_visible'})]:
 intent.append({'mode':'effect','dimension':'framing','target':'image','property':prop,'value':value,'operation':'set_value','receivers':rx,'source_quote':clauses[4]})
for target,other in [('initiating_hand','counterpart_hands'),('counterpart_hands','initiating_hand')]:
 intent.append({'mode':'effect','dimension':'action','target':target,'property':'action.interaction.exchange','value':{'type':'action.interaction.exchange/v1','value':'reciprocal_visible_hand_gestures'},'operation':'set_value','receivers':[other,'initiating_owner','counterpart_owner'],'source_quote':clauses[5]})
relevant=['shot_scale','subject_framing','relational_action','action','contact_point','hand_pose','composition','anatomical_connection','subject_count','body_region','participant_role','prop','prop_placement','camera_distance','lens','focus','depth_of_field','situation_context','narrative_phase']
output={
 'schema':'photo-readonly-source-application-proposal/v1','ordinal':1299,'candidate_id':CID,
 'task':'independent bounded manual semantic/source application diagnosis; no qualification/acceptance',
 'recommended_disposition':'retain pending until root explicitly chooses coverage and exchange interpretation; the generic original range is not solved by the restricted option below',
 'root_choice_applied':False,'source_modified':False,'proof_or_signature_created':False,'native_status_changed':False,
 'whole_before_source':before,'before_source_sha256':sha(before),'whole_original_source':original,
 'whole_original_provenance_entry':{'entry':entry,'sha256':sha(entry),'pointer':'/slots/composition/'+str(provenance.index(entry))},
 'whole_own_bindings':bindings,'whole_original_5B_row':compiled,'whole_formal04_row49':formal,
 'prior_owner_scope_revision03_row':prior,
 'read_inputs':[file_info(p) for p in [current_path,original_path,catalog_path,provenance_path,compiled_path,formal_path,prior_path]],
 'catalog149_summary_read':[{'id':k,'dimensions':v['dimensions'],'property_prefixes':v['property_prefixes']} for k,v in catalog.items()],
 'whole_relevant_current_specs':{k:{'sha256':sha(catalog[k]),'whole_spec':catalog[k]} for k in relevant},
 'literal_meaning_review':[
  'Original EN/KO explicitly conjoin actual exchange, hands-only coverage and macro framing. Historical composition-only coarse effects are not evidence that action or framing can be omitted.',
  'The label does not uniquely specify transfer, greeting, gesture or information exchange, payload, completion, hand count, person count, ownership partition or whether hands-only covers participant anatomy versus every item in the complete frame.',
  'Current generic range cannot be made native-valid merely by labeling existing exchange as a P/context/no-op. Independent existing endpoints/topology can be P; the selected performed exchange remains E.',
  'No exact device/distance/focal length/DOF/focus claim follows from macro. No hand pose/contact/prop/participant role/body topology E follows solely from hands/exchange.',
  'No human/adult requirement is added to satisfy human-only hand_pose or participant_role. The selected actual hand identity must be independently declared, with its own exact protocol, not guessed from owner kind.'
 ],
 'unselected_restricted_editorial_option':{
  'option_id':'existing_point_plus_owned_counterpart_scope_reciprocal_gesture_exchange',
  'deliberate_choices':['exchange is reciprocal visible hand gestures','hands-only means participant-anatomy coverage, not a whole-frame ban on every non-hand object','one initiating hand plus a complete nonempty counterpart scope independently authored before candidate discovery','every counterpart hand has the same explicitly selected carrier owner; initiating owner can be same or different'],
  'range_loss_requires_root_choice':'This excludes original-compatible multi-owner counterpart sets, unspecified other kinds of exchange and potentially stricter whole-frame hands-only readings. It must not replace the original source silently or be called range-preserving.',
  'whole_proposed_after_source':after,'proposed_after_source_sha256':sha(after),
  'exact_top_delta':[{'pointer':'/content/application_contract','before_exists':False,'before':None,'after':after['content']['application_contract']},{'pointer':'/conditions','before_exists':True,'before':before['conditions'],'after':after['conditions']},{'pointer':'/effects','before_exists':True,'before':before['effects'],'after':after['effects']}],
  'owner_map_intent_only':owner_plan,'manual_mode_and_effect_intent_only_not_native_proof':intent,
  'intended_roles':['shot_scale','subject_framing','relational_action'],
  'cardinality_boundary':'Counterpart scope is complete and nonempty under existing StageA/B2 rules. Explicit disjoint from the initiating point establishes at least two participating actual hand entities without a count fact or a fixed total two. Counterpart cardinality varies within unchanged core32-owner/64-assertion and scope32-member limits; do not infer pairwise disjointness among counterpart members or extra owners.',
  'existing_core_requirements':'Candidate-independent full input inventory/source spans/graph, actual hand and carrier presence, custom exact hand-kind facts, explicit part_of and disjoint witnesses, complete counterpart membership. No after-discovery core supplementation or automatic scope partition/complement.',
  'P_E_boundary':'Existing topology/kind/presence are independent P/guards. E is applied to every actual hand plus image scale/coverage, and every listed receiver expands exactly. Existing already-exchanging state is neither required nor an excuse to remove E.',
  'receiver_and_lock_boundary':'Include hands and their actual carrier owners in whole E/Rx. Alias normalization does not merge part_of. Missing/unknown topology, incomplete selected members, missing selection, actual E conflict or relevant actual receiver/owner/part lock must fail final; selected closure cannot be truncated. This proposal has not run actual native admission and does not assert those outcomes as observed.',
  'binding_boundary':'Historical optional direct composition binding is preserved here as a read source record, not manufactured into a new binding. A future accepted source requires explicit manual role/binding review; the word composition does not justify an extra layout effect.',
  'application_is_not_approved':True
 },
 'range_preserving_contract_gap':{
  'current_supported':'Point selectors, nonempty complete existing member scopes, each-member E/P/PR, all-member receivers and for_each_member atomic comparisons to a point are supported shapes.',
  'missing_minimum_plural_relation':'An arbitrary one-scope hand set permits one member. No current source-bound cardinality/minimum-two or quantified member-pair disjoint predicate is available. Do not manufacture subject_count P or a fake aggregate.',
  'missing_member_carrier_projection':'There is no current source-qualified per-member hand-to-its-actual-carrier endpoint projection that expands a variable multi-owner hand set and its complete actual carrier receiver closure. A forall member part_of one point deliberately restricts ownership; it is not this generic function.',
  'remaining_semantic_choice':'A new relation/cardinality API alone would not choose exchange kind or resolve the meaning of hands-only. The source/application still needs a root-selected literal meaning and actual endpoint/whole mutation review.',
  'readonly_future_plan':['Specify an opt-in source-qualified finite member/endpoint relation contract with actual CID/RID/selected closure provenance; do not reinterpret guards/v3 or v4 owner maps silently.','Require independent exact frozen scope membership and actual member-to-carrier witnesses, core/input/graph/provenance hashes. Never infer a parent, set complement, payload, anatomy or count from candidate language.','If needed explicitly authorize a minimum-plural/pairwise-distinct constraint in a new version, not an invented current count P; preserve aliases versus part_of and existing finite caps.','Use one shared actual expansion for P/PR/E/all receivers, canonical joint assignment/lock ledger, active guards, immutable pack -> compose -> fresh runtime. All affected actual carriers and locked parts must be retained.','Only after a root-approved code release, add full/compact/lazy/member/pack/compose/runtime positive and adversarial tests; then manually reread the accepted literal source and author a fresh proof.'],
  'prospective_files_not_authorized':['scripts/photo_semantic_evidence.py shared source-qualified coordinator and versioned guard parser/evaluator','scripts/photo_native_owner_resolution.py shared actual member/carrier expansion only if a new explicit selector needs it','precore/photo_semantic_witnesses.py and photo_authoring_wire.py only if an independently grounded relation inventory cannot be expressed by the current neutral graph','transport consumers only on an observed drop trace; keep immutable public pack and strict final source authority'],
  'out_of_scope':['new people/hands/objects','noun creation','inferred human/adult identity','automatic exchange payload selection','arbitrary exact total hand/person count','native proof/status generation or approval','code implementation']
 },
 'unselected_object_handoff_alternative':'Root has not selected an existing exchanged object. A future literal handoff option must explicitly select the independent existing object and all actual endpoints, preserve holding/contact/position/ownership changes actually entailed, and review their dimensions/properties/Rx. It cannot be supplied implicitly by this gesture option or frozen as already performed P.',
 'proposed_adversarial_plan_not_executed':[
  'Positive restricted option: point + counterpart scope with two and with more counterpart hands, same carrier versus different carrier, every exact P/part_of/disjoint and all Rx supplied.',
  'Negative: one unpartitioned hand only; missing initiating point; empty/incomplete/stale scope; fake minimum-count P; candidate-authored core; custom hand-kind absent or different; role named hands but no anatomical witness.',
  'Negative: selected hand is not part_of its declared carrier; unknown/disallowed equivalence or disjoint; introduction/synthetic owner masquerades as existing; hidden extra selected child/member/receiver.',
  'Negative: missing action E, exchange reduced to P/context/no-op, only framing adopted, one member omitted from action or Rx, broad framing lock or carrier/part lock conflict.',
  'Positive P old -> E new remains allowed; negative conflicting same actual owner/property E across selected CIDs/aliases; consistent canonical values/receivers remain allowed.',
  'Whole-frame interpretation, object handoff and multi-owner counterpart range remain separate unselected/pending alternatives; do not reuse a restricted positive as proof of them.'
 ],
 'validation_boundary':'Exact research file hashes, record equality and proposed literal copies only. No native/source/schema/admission/runtime test executed for this1299 proposal; no corpus qualification or pixels proved.'
}
out=R/'authored/native_1299_hands_exchange_application_proposal_01.json'
if out.exists():raise SystemExit('immutable proposal already exists')
out.write_text(json.dumps(output,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(json.dumps({'proposal':file_info(out),'before_record_sha256':sha(before),'unselected_after_record_sha256':sha(after),'relevant_full_specs':len(relevant),'catalog_summary_slots':len(catalog)},ensure_ascii=False))
