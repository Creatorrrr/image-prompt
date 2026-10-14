"""Additional handoff alternative, research-only; proposal01 stays immutable."""
import copy, hashlib, json
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014')
first=R/'authored/native_1299_hands_exchange_application_proposal_01.json'
d=json.loads(first.read_text());CID=d['candidate_id'];before=d['whole_before_source']
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def info(p):return {'file':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def ep(target):return {'kind':'source_target','candidate_id':CID,'target':target}
member={'kind':'bound_member','variable':'hand'}
def each(i,rule):return {'id':i,'kind':'for_each_member','scope':ep('other_hands'),'member_variable':'hand','rule':rule}
def atom(i,kind,**fields):return {'id':i,'kind':kind,**fields}
handkind={'type':'body.part.kind/v1','value':'hand'}
clauses=[
 'Deliberate application choice: depict a physical handoff in progress involving the selected existing exchange item and all selected existing participating hands. This is one editorial application of exchange, not its uniquely established original meaning.',
 'Select one independently declared existing initiating hand, a complete nonempty independently declared existing other-hands scope, and one independently declared existing generic physical exchange item. All selections and scope membership must come from the frozen candidate-independent request/input/core inventory; do not create a hand, person, body owner or item, or construct a counterpart subset after discovery.',
 'Require exact existing entity presence for each selected hand and the item, exact body.part.kind/v1 hand evidence for each selected hand, explicit disjointness between each other hand and the initiating hand, and explicit disjointness between the item and every selected hand. The generic physical item must be independently established as a physical item, without selecting a particular item class from this label.',
 'Retain independently declared ownership and part relationships as they are. Do not require human identity, a common carrier, two different carriers, a hand-to-person part_of relation or a fixed total number of hands or people. This source neither supplies missing anatomy nor establishes an owner from a role or category.',
 'Set macro shot scale and hands-only participant framing. Here hands-only means that the visible anatomical participation of this exchange consists of the selected participating hands; it does not require deletion of the exchange item or unrelated background. This participant-coverage interpretation must be explicitly selected; it does not resolve a stricter whole-frame reading by assumption.',
 'Apply the performed physical handoff as an exchange action effect to the selected item with the initiating hand and every other hand as actual receivers. Apply macro scale and hands-only participant framing as image effects with the item and every participating hand included in their actual receiver scope. Do not replace performed exchange with existing-action prerequisites, context, preservation or an empty mutation.',
 'Do not select a completed ownership transfer, fixed contact geometry, finger pose, a prescribed item coordinate or trajectory, item subtype, camera hardware, focal length, focus plane or depth of field from this label. This does not authorize omission of any such actual additional mutation: if an application specifies contact, support, placement, ownership change or other facts, its literal whole effects and exact affected receivers need a separate complete review before adoption.',
 'Preserve independent frozen identity, topology and visibility requirements. If hands-only framing would alter a locked affected carrier or body region, the application must be rejected; a selected hand address is not permission to omit that actual receiver. The source does not invent a carrier in order to make the crop applicable.'
]
after=copy.deepcopy(before);after['content']['application_contract']=' '.join(clauses)
rules=[
 atom('initiating_hand_kind','frozen_value',owner=ep('initiating_hand'),dimension='subject',property='body.part.kind',value=handkind),
 atom('item_not_initiating_hand','owner_relation',relation='disjoint',left=ep('exchange_item'),right=ep('initiating_hand')),
 each('each_other_hand_kind',atom('kind','frozen_value',owner=member,dimension='subject',property='body.part.kind',value=handkind)),
 each('each_other_hand_separate',atom('separate_hand','owner_relation',relation='disjoint',left=member,right=ep('initiating_hand'))),
 each('each_other_hand_not_item',atom('separate_item','owner_relation',relation='disjoint',left=member,right=ep('exchange_item')))
]
after['conditions']={'native_guards':{'schema':'photo-native-source-guards/v3','rules':rules}}
after['effects']={'dimensions':['framing','action'],'properties':[
 {'dimension':'framing','target':'image','property':'shot.scale'},
 {'dimension':'framing','target':'image','property':'framing.coverage'},
 {'dimension':'action','target':'exchange_item','property':'action.interaction.exchange'}]}
owner_plan={'schema':'photo-native-owner-bindings/v4','bindings':[
 {'target':target,'origin':'existing','introduced_by':None,'selector':selector}
 for target,selector in [('image',{'kind':'core_role','role':'image'}),('initiating_hand',{'kind':'selected_existing_owner'}),('other_hands',{'kind':'selected_existing_member_scope','scope_schema':'photo-frozen-existing-member-scope/v1','target_semantics':'each_member','receiver_semantics':'all_members'}),('exchange_item',{'kind':'selected_existing_owner'})]]}
intent=[]
for target in ['initiating_hand','other_hands','exchange_item']:
 intent.append({'mode':'prerequisite','dimension':'subject','target':target,'property':'entity.presence','value':{'type':'entity.presence/v1','value':'present'},'quote':clauses[2],'protocol':'shipped common exact presence tuple; each scope member separately'})
for target in ['initiating_hand','other_hands']:
 intent.append({'mode':'prerequisite','dimension':'subject','target':target,'property':'body.part.kind','value':handkind,'quote':clauses[2],'protocol':'proposed custom exact hand-kind tuple, not a shipped common hand-presence default'})
intent.append({'mode':'prerequisite','dimension':'subject','target':'exchange_item','property':'entity.kind','value':{'type':'entity.kind/v1','value':'physical_item'},'quote':clauses[2],'protocol':'proposed generic physical-item tuple only; root must select/accept its exact independent protocol, no cup/key/card subtype or model-generated fact'})
for prop,value in [('shot.scale',{'type':'shot.scale/v1','value':'macro'}),('framing.coverage',{'type':'framing.coverage/v1','value':'only_selected_exchange_hands_as_visible_participant_anatomy'})]:
 intent.append({'mode':'effect','dimension':'framing','target':'image','property':prop,'value':value,'operation':'set_value','receivers':['initiating_hand','other_hands','exchange_item'],'quote':clauses[4]})
intent.append({'mode':'effect','dimension':'action','target':'exchange_item','property':'action.interaction.exchange','value':{'type':'action.interaction.exchange/v1','value':'physical_handoff_in_progress_with_all_selected_hands'},'operation':'set_value','receivers':['initiating_hand','other_hands'],'quote':clauses[5]})
result={
 'schema':'photo-readonly-source-application-proposal/v1','ordinal':1299,'candidate_id':CID,
 'supplements_immutable_proposal01':info(first),'supersedes_no_bytes':True,
 'root_additional_question':'holder-free point + nonempty other-hands scope, deliberate physical handoff with one existing generic item, no forced common carrier/human/fixed total two',
 'recommended_disposition':'root choice still required; operating source/formal04 pending remain unchanged. The following complete source literal is an unselected editorial restriction, not a proof or approval.',
 'whole_before_source':before,'before_source_sha256':sha(before),'whole_own_bindings':d['whole_own_bindings'],
 'whole_proposed_after_source':after,'proposed_after_source_sha256':sha(after),
 'exact_top_delta':[{'pointer':'/content/application_contract','before_exists':False,'before':None,'after':after['content']['application_contract']},{'pointer':'/conditions','before':before['conditions'],'after':after['conditions']},{'pointer':'/effects','before':before['effects'],'after':after['effects']}],
 'owner_map_intent_not_native_proof':owner_plan,'manual_P_E_intent_not_native_proof':intent,
 'intended_roles':['shot_scale','subject_framing','relational_action'],
 'answer_no_forced_owner':'Yes: the current point/member source-target guard shapes need no person, common owner, parent target or hand part_of condition merely to establish plural existing hands. Nonempty other_hands plus explicit member-to-initiating-hand disjoint gives variable 1+N. Preserve independently declared existing graph relations; neither infer nor require a person carrier absent from source. Introduced synthetic endpoints are excluded by existing-only selectors.',
 'cardinality':'No scalar count P or exact total two. Each other member is explicitly separate from initiating_hand. Existing member-scope canonical alias duplicate rejection remains, part_of is not equivalence, and no unexpressed pairwise disjoint relation among all other hands is asserted. Core32 owners/64 assertions and finite member limits still apply; a required complete closure exceeding them is rejected, never truncated.',
 'scope_partition_restriction':'The initiating point and exact complete other-hands scope must already be independently specified before discovery. Current B2 cannot create a set complement, choose an arbitrary subset of a frozen whole scope, or add missing ownership/hand facts after candidate discovery. Absence of that independent partition remains pending even if the whole hands set exists.',
 'item_choice_boundary':'Exactly one selected existing exchange item is a deliberate application restriction, not an original-source exact object count claim or the invention of a new object. Generic physical_item is an explicit proposed independently grounded P protocol, not a verified common-core default; no item subtype is inferred. Root may reject this restriction or choose another literal.',
 'why_exchange_remains_E':'The existing object and hands/topology are P. The performed physical handoff is E on item with all participating actual hands as Rx. It is not an existing possession P or a context/event wrapper. No completed ownership transfer is asserted; if chosen later it is an additional actual E, not entity.owner_id frozen relation evidence.',
 'whole_footprint_open_issue':'Current B2 can expand these literal target/Rx shapes and v3 predicates. This read-only proposal has not demonstrated actual native admission, source qualification, image pixels or every participant crop lock. Image/framing.coverage is deliberately broad. If an actual frozen graph has separately named affected non-hand carrier/body-region visibility, those actual receivers/locks must be included and checked, not treated as disjoint merely because only hand addresses were selected. No current API automatically derives an arbitrary complete carrier/region Rx set from hands. A source-compatible application that cannot explicitly close that actual footprint must remain pending; do not declare all-Rx complete on this literal alone.',
 'contact_position_ownership_boundary':'A selected instant of a physical handoff does not uniquely declare the exact contact/support configuration, coordinates, endpoint ownership result or trajectory. They are neither silently P nor automatically inferred E here. If the application actually commits such a change, expand the reviewed source/effects/receivers before qualification; the action label cannot exempt a real mutable footprint.',
 'range_preservation':'This option handles variable multiple hands within finite caps and does not impose two people or a common holder. It intentionally selects physical handoff, one item, an initiating-vs-other independent partition and participant-only coverage. Original-compatible gesture/information exchanges, multiple simultaneous exchange items and strict whole-frame-only-hands readings are not qualified by it. Keeping original en/ko does not preserve those paths after restricting application_contract. Leave the original record unchanged/pending unless root explicitly approves narrowing or separately authors a faithful application/RID design covering remaining meanings; no automatic OR branch, legacy fallback or unreviewed base branch.',
 'current_B2_scope_claim':'Static source/API read only: owner-map/v4 existing point/member selectors and guards/v3 scalar+for_each_member shape can express the listed hand/item/disjoint/kind selections. This is not an observed validation or admission result. Future complete proof must freshly review every positive unit, exact original/after hash, actual RID, independent core tuple spelling, selected closure, all E/Rx and final locks.',
 'remaining_API_gap_if_original_range_required':[
  'One arbitrary whole hands scope with required plural needs an explicit versioned source-qualified minimum-plural/distinct-member constraint or an already independently declared point+other partition; no fake count P.',
  'If actual hands-only framing changes separately declared participant carrier/region visibility, generic member-to-carrier/affected-region closure and receiver projection needs an explicit source-qualified contract, or exact manually selected complete receiver scopes with supporting current source conditions. Do not invent a human owner or ignore locked actual parts.',
  'Actual dynamically selected exchange kind, item-count variants or transfer-endpoint/cardinality semantics require root-selected literal source applications and complete manual mutation review; current static typed values do not supply those meanings automatically.'
 ],
 'proposed_tests_not_executed':[
  'Variable 1+N with more than one other hand, no human/common holder/part_of P; exact independent handkind/presence, existing item distinct from each hand.',
  'Reject one-hand alias, same initiating member, item aliasing any hand, missing/stale/partial scope, introduced item, missing exact hand-kind/physical-item evidence, forced default primary owner.',
  'Preserve same-holder and different-holder independent core topology; part_of must not merge entities or fabricate disjoint.',
  'Actual broad/partial framing locks on item/hands/affected carrier regions, whole action Rx locks and joint actual-owner E consistency, full/compact/lazy/pack/compose/runtime parity.',
  'Reject action hidden as P/context and incomplete contact/position/ownership footprint when an actual selected application declares them; old P to new E remains legal only when permissions allow.'
 ],
 'no_changes':{'production_tests':True,'actual_source_catalog_binding':True,'proof_status_signature':True,'runtime_index_registry_git':True,'model_provider_network_embedding_Gemini_calls':0},
 'read_evidence':{'proposal01_inputs_and_whole19specs':info(first),'extra_code_reads':['photo_semantic_evidence.py owner_binding_plan/_validate_target_guards/_check_endpoint_plans/_guard_context/evaluate_native_guards/permission_scope','photo_native_owner_resolution.py finite caps/_facts','photo_contracts.py property_effects_allowed owner-relation lock overlap','precore/photo_semantic_witnesses.md exact role/part_of/disjoint/common presence protocol']}
}
out=R/'authored/native_1299_hands_exchange_application_proposal_02.json'
if out.exists():raise SystemExit('immutable proposal already exists')
out.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':str(out),'raw_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'after_sha256':sha(after)},ensure_ascii=False))
