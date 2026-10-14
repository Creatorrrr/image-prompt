"""Manually authored research literals, not a proof/status/qualification generator.

Every source edit, tuple, mode, value, owner, receiver, quote and role below is
an individual direct Codex judgement. Loops only serialize/check already authored
literals and provenance. No tags, classifier, inference, or operating file writes.
"""
from pathlib import Path
import copy,gzip,hashlib,json

R=Path(__file__).resolve().parents[1]
ROOT=R.parents[3]
OUT=R/'authored/native_source_guard_v2_1278_1296_proposal_v1.json'
def canonical(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(v):return hashlib.sha256(canonical(v)).hexdigest()
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
current_path=R/'native-inputs/11870-01250-01300-plan-03/CURRENT-PROPOSAL.json.gz'
current=read(current_path);catalog=read(R/'CATALOG-FINAL-144-V4.json');original=read(R/'SOURCE.json.gz')
assert digest(current)=='30924a72de7d3011af26b7ef7c0192ff12edd732131f3c18ed29748e805d5477'
assert digest(catalog)=='5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
C1278='cand_7f96b80af091533cb700db081b3dbbaf';C1296='cand_1b714a345bd35bc08d6592bf94caca29'

def endpoint(cid,target):return {'kind':'source_target','candidate_id':cid,'target':target}
def part(cid,fid,left,right):return {'id':fid,'kind':'owner_relation','relation':'part_of','left':endpoint(cid,left),'right':endpoint(cid,right)}
def distinct(cid,fid,left,right):return {'id':fid,'kind':'owner_relation','relation':'disjoint','left':endpoint(cid,left),'right':endpoint(cid,right)}
def selected(*targets):return {'schema':'photo-native-owner-bindings/v3','bindings':[
    {'target':t,'origin':'existing','introduced_by':None,'selector':{'kind':'selected_existing_owner'}} for t in targets]}
def P(fid,owner,dimension,prop,typ,value,pointer,quote):
    return {'id':fid,'realization_id':'base','pointer':pointer,'quote':quote,'dimension':dimension,
        'target':owner,'property':prop,'mode':'prerequisite','value':{'type':typ,'value':value},'requires':[]}
def E(fid,owner,dimension,prop,typ,value,receivers,pointer,quote):
    return {'id':fid,'realization_id':'base','pointer':pointer,'quote':quote,'dimension':dimension,
        'target':owner,'property':prop,'mode':'effect','value':{'type':typ,'value':value},'requires':[],
        'operation':'set_value','receivers':receivers}

# 1278: preserve the current three actual effects. Hand impression never becomes
# an expression-face fact, a helping action or measured thermal state.
a1278=copy.deepcopy(current['candidates'][C1278])
a1278['content']['application_contract']=(
    'Apply only to the independently declared existing face and existing hands-region of the same independently declared existing human character, with all three actual owners explicitly selected by the caller. '
    'The hands-region is the already declared region containing the hands named by this cue; it neither creates a group nor specifies an exact total hand count. '
    'Select the blank facial response, the warm helpful presentation of those hands, and the contrast between that blank face and those warm helpful hands. '
    'Do not add body parts, prescribe a particular helping gesture, or assert temperature, private emotion or successful help. No main, primary or foreground role is assigned.')
a1278['conditions']={'for_any':['human'],'native_guards':{'schema':'photo-native-source-guards/v2','rules':[
    part(C1278,'face_belongs_to_character','face','character'),
    part(C1278,'hands_region_belongs_to_character','hands','character'),
    distinct(C1278,'face_and_hands_are_distinct_regions','face','hands'),
    {'id':'selected_character_is_explicitly_human','kind':'frozen_value','owner':endpoint(C1278,'character'),
     'dimension':'subject','property':'entity.category','value':{'type':'entity.category/v1','value':'human'}}]}}
f1278=[
 P('face_present_en','face','subject','anatomy.face.presence','anatomy.face.presence/v1','present','/content/en','face'),
 P('hands_region_en','hands','body_geometry','body.part.presence','body.part.presence/v1','hands','/content/en','hands'),
 E('face_blank_en','face','expression','expression.face','expression.face/v1','blank',[],'/content/en','blank face'),
 E('hands_impression_en','hands','character_response','response.presentation','response.presentation/v1','warm_helpful_impression',[],'/content/en','warm helpful hands'),
 E('contrast_en','hands','character_response','character.contrast','character.contrast/v1','blank_face_vs_warm_helpful_hands',['face'],'/content/en','blank face with warm helpful hands'),
 P('face_present_ko','face','subject','anatomy.face.presence','anatomy.face.presence/v1','present','/content/ko','얼굴'),
 P('hands_region_ko','hands','body_geometry','body.part.presence','body.part.presence/v1','hands','/content/ko','손'),
 E('face_blank_ko','face','expression','expression.face','expression.face/v1','blank',[],'/content/ko','무표정한 얼굴'),
 E('hands_impression_ko','hands','character_response','response.presentation','response.presentation/v1','warm_helpful_impression',[],'/content/ko','따뜻하고 도움을 주는 인상의 손'),
 E('contrast_ko','hands','character_response','character.contrast','character.contrast/v1','blank_face_vs_warm_helpful_hands',['face'],'/content/ko','무표정한 얼굴과 따뜻하고 도움을 주는 인상의 손'),
 P('face_present_app','face','subject','anatomy.face.presence','anatomy.face.presence/v1','present','/content/application_contract','existing face'),
 P('hands_region_app','hands','body_geometry','body.part.presence','body.part.presence/v1','hands','/content/application_contract','existing hands-region'),
 E('face_blank_app','face','expression','expression.face','expression.face/v1','blank',[],'/content/application_contract','blank facial response'),
 E('hands_impression_app','hands','character_response','response.presentation','response.presentation/v1','warm_helpful_impression',[],'/content/application_contract','warm helpful presentation of those hands'),
 E('contrast_app','hands','character_response','character.contrast','character.contrast/v1','blank_face_vs_warm_helpful_hands',['face'],'/content/application_contract','contrast between that blank face and those warm helpful hands'),
]

# 1296: explicitly proposed participating-pair reading, not a silently asserted
# exact total anatomical inventory. Root must adjudicate this reading anew.
a1296=copy.deepcopy(current['candidates'][C1296])
a1296['content']['application_contract']=(
    'Use only the independently declared existing mug and two independently declared existing hands of the same independently declared existing holder, all explicitly selected by the caller. '
    'The two selected hands are distinct, and the mug is distinct from either hand. '
    'Here both hands names the two participating hands in this holding action; it does not assert that the holder has exactly two hands in its entire anatomy. '
    'Select holding that same mug with both selected hands together and the mug held wrapped by both selected hands at the selected instant. '
    'Select the declared qualitative warm physical state of that mug; this is an actual selected state, not an assumed already-warm prerequisite or a numerical temperature. '
    'Do not add a mug, hands, holder, drink, steam or a heating process, and do not prescribe finger geometry or a comforting emotion. No main, primary or foreground role is assigned.')
a1296['conditions']={'native_guards':{'schema':'photo-native-source-guards/v2','rules':[
    part(C1296,'first_hand_belongs_to_holder','hand_a','holder'),
    part(C1296,'second_hand_belongs_to_holder','hand_b','holder'),
    distinct(C1296,'participating_hands_are_distinct','hand_a','hand_b'),
    distinct(C1296,'mug_is_distinct_from_first_hand','mug','hand_a'),
    distinct(C1296,'mug_is_distinct_from_second_hand','mug','hand_b')]}}
a1296['effects']={'dimensions':['action','material','relationship'],'properties':[
    {'dimension':'material','target':'mug','property':'object.temperature.declared'},
    {'dimension':'action','target':'hand_a','property':'action.holding'},
    {'dimension':'action','target':'hand_b','property':'action.holding'},
    {'dimension':'relationship','target':'mug','property':'contact.held_by'}]}
f1296=[
 P('mug_type_en','mug','subject','props.type','props.type/v1','mug','/content/en','mug'),
 P('first_hand_en','hand_a','body_geometry','body.part.presence','body.part.presence/v1','hand','/content/en','both hands'),
 P('second_hand_en','hand_b','body_geometry','body.part.presence','body.part.presence/v1','hand','/content/en','both hands'),
 E('mug_warm_en','mug','material','object.temperature.declared','object.temperature.declared/v1','warm',[],'/content/en','warm mug'),
 E('first_holding_en','hand_a','action','action.holding','action.holding/v1','holding_same_mug_with_other_selected_hand',['mug','hand_b'],'/content/en','held in both hands'),
 E('second_holding_en','hand_b','action','action.holding','action.holding/v1','holding_same_mug_with_other_selected_hand',['mug','hand_a'],'/content/en','held in both hands'),
 E('held_contact_en','mug','relationship','contact.held_by','contact.held_by/v1','held_wrapped_by_both_selected_hands',['hand_a','hand_b'],'/content/en','held in both hands'),
 P('mug_type_ko','mug','subject','props.type','props.type/v1','mug','/content/ko','머그'),
 P('first_hand_ko','hand_a','body_geometry','body.part.presence','body.part.presence/v1','hand','/content/ko','두 손'),
 P('second_hand_ko','hand_b','body_geometry','body.part.presence','body.part.presence/v1','hand','/content/ko','두 손'),
 E('mug_warm_ko','mug','material','object.temperature.declared','object.temperature.declared/v1','warm',[],'/content/ko','따뜻한 머그'),
 E('first_holding_ko','hand_a','action','action.holding','action.holding/v1','holding_same_mug_with_other_selected_hand',['mug','hand_b'],'/content/ko','두 손으로 감싼'),
 E('second_holding_ko','hand_b','action','action.holding','action.holding/v1','holding_same_mug_with_other_selected_hand',['mug','hand_a'],'/content/ko','두 손으로 감싼'),
 E('held_contact_ko','mug','relationship','contact.held_by','contact.held_by/v1','held_wrapped_by_both_selected_hands',['hand_a','hand_b'],'/content/ko','두 손으로 감싼'),
 P('mug_type_emb','mug','subject','props.type','props.type/v1','mug','/content/embedding_text','mug'),
 P('first_hand_emb','hand_a','body_geometry','body.part.presence','body.part.presence/v1','hand','/content/embedding_text','both hands'),
 P('second_hand_emb','hand_b','body_geometry','body.part.presence','body.part.presence/v1','hand','/content/embedding_text','both hands'),
 E('mug_warm_emb','mug','material','object.temperature.declared','object.temperature.declared/v1','warm',[],'/content/embedding_text','warm mug'),
 E('first_holding_emb','hand_a','action','action.holding','action.holding/v1','holding_same_mug_with_other_selected_hand',['mug','hand_b'],'/content/embedding_text','held in both hands'),
 E('second_holding_emb','hand_b','action','action.holding','action.holding/v1','holding_same_mug_with_other_selected_hand',['mug','hand_a'],'/content/embedding_text','held in both hands'),
 E('held_contact_emb','mug','relationship','contact.held_by','contact.held_by/v1','held_wrapped_by_both_selected_hands',['hand_a','hand_b'],'/content/embedding_text','held in both hands'),
 P('mug_type_app','mug','subject','props.type','props.type/v1','mug','/content/application_contract','independently declared existing mug'),
 P('first_hand_app','hand_a','body_geometry','body.part.presence','body.part.presence/v1','hand','/content/application_contract','two independently declared existing hands'),
 P('second_hand_app','hand_b','body_geometry','body.part.presence','body.part.presence/v1','hand','/content/application_contract','two independently declared existing hands'),
 E('mug_warm_app','mug','material','object.temperature.declared','object.temperature.declared/v1','warm',[],'/content/application_contract','declared qualitative warm physical state of that mug'),
 E('first_holding_app','hand_a','action','action.holding','action.holding/v1','holding_same_mug_with_other_selected_hand',['mug','hand_b'],'/content/application_contract','holding that same mug with both selected hands together'),
 E('second_holding_app','hand_b','action','action.holding','action.holding/v1','holding_same_mug_with_other_selected_hand',['mug','hand_a'],'/content/application_contract','holding that same mug with both selected hands together'),
 E('held_contact_app','mug','relationship','contact.held_by','contact.held_by/v1','held_wrapped_by_both_selected_hands',['hand_a','hand_b'],'/content/application_contract','mug held wrapped by both selected hands'),
]

# Exact role reference lists are authored, never inferred from a tag or keyword.
def role(key,refs,modes):return {'spec_sha256':digest(catalog[key]),'scope':'whole_record','realization_ids':['base'],
    'fact_refs':refs,'support_modes':modes}
roles1278={
 'expression':role('expression',['face_blank_en','face_blank_ko','face_blank_app'],['effect']),
 'character_contrast':role('character_contrast',['contrast_en','contrast_ko','contrast_app'],['effect'])}
roles1296={
 'prop':role('prop',['mug_type_en','mug_type_ko','mug_type_emb','mug_type_app'],['prerequisite']),
 'thermal_state':role('thermal_state',['mug_warm_en','mug_warm_ko','mug_warm_emb','mug_warm_app'],['effect']),
 'action':role('action',['first_holding_en','second_holding_en','first_holding_ko','second_holding_ko','first_holding_emb','second_holding_emb','first_holding_app','second_holding_app'],['effect']),
 'contact_point':role('contact_point',['held_contact_en','held_contact_ko','held_contact_emb','held_contact_app'],['effect'])}

paths=[current_path,R/'SOURCE.json.gz',R/'ORDER.json',R/'CATALOG-FINAL-144-V4.json',R/'CATALOG-FINAL-144-V4-ACCEPTANCE.json',
 R/'native_batches/review11870-01250-01300-02/BATCH.json',R/'native_batches/review11870-01250-01300-02/NOTE.json',
 R/'native_batches/review11870-01250-01300-02/ROOT-SEMANTIC-REOPEN-02.json',
 R/'native-inputs/11870-01250-01300-plan-03/ROOT-REVIEW-REQUIREMENTS.json',R/'native-inputs/11870-01250-01300-plan-03/SOURCE-APPROVAL.json',
 R/'authored/native_11870_first50_pending_resolution_v1.json',R/'native-inputs/first50-pending-source-plan-03/ROOT-SOURCE-SELECTION.json',
 R/'decisions/review_01250_02250_01250_01500.json',ROOT/'skills/photo-prompt-image-generator/precore/photo_semantic_witnesses.md',
 R/'worker-notes/native-source-guards-v2-handoff-20261015.json']
manifest=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
latest_specs=['expression','character_contrast','social_cue','character_intent','mood','sensory_cue','contact_point','thermal_state','prop','prop_state','hand_pose','body_region','anatomical_connection','action','relational_action','light_color','surface_material','physical_motion','body_pose','prop_placement','participant_role','narrative_clue','aftermath_trace']
rows=[]
for ordinal,cid,after,facts,maps,roles in [
 (1278,C1278,a1278,f1278,selected('face','hands','character'),roles1278),
 (1296,C1296,a1296,f1296,selected('mug','hand_a','hand_b','holder'),roles1296)]:
 before=current['candidates'][cid]
 deltas=[{'pointer':'/conditions','before_exists':True,'after_exists':True,'before':copy.deepcopy(before['conditions']),'after':copy.deepcopy(after['conditions']),
          'reason':'Explicit source-local actual-owner relations on existing selected owners; no fixed primary role or inferred graph.'},
         {'pointer':'/content/application_contract','before_exists':True,'after_exists':True,'before':before['content']['application_contract'],'after':after['content']['application_contract'],
          'reason':'Individually reviewed literal application clarification; see semantic clause and both-hands adjudication in companion note.'}]
 if before['effects']!=after['effects']:deltas.append({'pointer':'/effects','before_exists':True,'after_exists':True,'before':copy.deepcopy(before['effects']),'after':copy.deepcopy(after['effects']),
     'reason':'Replace ambiguous aggregate hands mutation address with both actually selected existing hand owners. Preserve warm state and the whole joint holding/wrapped-contact meaning; no effect-mode waiver.'})
 units=[{'realization_id':'base','pointer':'/content/'+key,'quote':after['content'][key],
         'fact_refs':[f['id'] for f in facts if f['pointer']=='/content/'+key],'disposition':'semantic'} for key in ['en','ko']+(['embedding_text'] if ordinal==1296 else [])+['application_contract']]
 row={'ordinal':ordinal,'candidate_id':cid,'record_kind':'visual_option','actual_realization_ids':['base'],
      'root_source_approval_required':True,'native_proof':None,'native_signature':None,'new_native_approval':False,
      'original_source_sha256':digest(original['candidates'][cid]),'current_source_sha256':digest(before),
      'proposed_source_sha256':digest(after),'source_before_current_full':before,'source_after_proposed_full':after,'exact_source_correction_proposals':deltas,
      'current_own_bindings_preserved_full':[v for v in current['slot_bindings'].values() if v['candidate_id']==cid],
      'new_cid_dependencies':[],'new_binding_references':[],'proposed_manual_authoring_material':{
         'facts':facts,'source_units':units,'roles':roles,'owner_maps':{'base':maps},'effect_sets':{'base':{'dimensions':sorted(after['effects']['dimensions']),
             'properties':sorted(copy.deepcopy(after['effects']['properties']),key=lambda p:(p['dimension'],p['target'],p['property']))}}},
      'guard_only_existing_targets':['character'] if ordinal==1278 else ['holder'],
      'owner_resolution_protocol_obligations':{'all_selected_targets':'independent required subject/entity.presence/entity.presence/v1/present on each actual owner, plus exact authored P and graph witnesses',
          'source_to_core_mapping':'existing photo-request-owner-selections/v1 only; no request owner UUID, first match, primary-role guess or pre-core supplementation in global source'},
      'native_review_not_completed':['Root must reread/approve the entire proposed literal and interpretation, prepare a fresh immutable input, then a reviewer must author a fresh complete proof/signature. These material fragments are not a proof.',
          'No runtime, images, full corpus semantic qualification or native acceptance is proved by literal integrity checks.']}
 rows.append(row)
rows[0]['untagged_whole_effect_fact_refs']=['hands_impression_en','hands_impression_ko','hands_impression_app']
rows[0]['manual_role_decisions']={
 'expression':'Only the face blank-response effect; no hand-presentation support is assigned to expression.',
 'character_contrast':'Actual selected contrast with hands target and face receiver. Contextual role does not turn the contrast effect into context/no-op.',
 'action':'Not proposed: helpful-looking hands do not declare a performed helping action.',
 'thermal_state':'Not proposed: warm is a warm/helpful presentation impression, not physical temperature.',
 'sensory_cue':'Not proposed: no specific touch/heat proxy is supplied.',
 'hand_pose':'Not proposed: no hand/finger shape or articulation is specified.',
 'character_intent':'Not proposed: helpful presentation does not establish a goal or private intent.',
 'social_cue':'Not proposed: no other participant reaction, attention or resource allocation is supplied.',
 'body_region/anatomical_connection':'The named carrier/part relations remain existing prerequisites; no new region selection or anatomical mutation is proposed from guard-only evidence.'}
rows[0]['custom_tuple_warning']={'shared_neutral_guide':['subject/entity.presence/entity.presence/v1/present','subject/anatomy.face.presence/anatomy.face.presence/v1/present'],
 'existing_custom_namespace_example':'body_geometry/body.part.presence/body.part.presence/v1/hand was actually read in formal02 ordinal1271; it is not in the shared presence table.',
 'new_exact_source_specific_values_or_namespaces':['body_geometry/body.part.presence/body.part.presence/v1/hands on one independently declared hands-region owner','subject/entity.category/entity.category/v1/human on the selected character'],
 'not_interchangeable':'hand != hands; a generic human category, owner_kind, primary donor or role does not supply either custom tuple. No conversion, inherited face witness or whole-set subset query.',
 'reason_for_human_guard':'Retain intrinsic human on the actual selected character instead of borrowing only a different primary subject category. This explicit additional source clarification requires root adjudication; no human/adult/anatomy is inferred.'}
rows[1]['manual_role_decisions']={
 'prop':'Existing mug identity is positively declared and required under the selected existing-object application; props.type P supports the prop role, without add_entity or a new count effect.',
 'thermal_state':'Qualitative warm physical state on that same mug is an E; no already-warm P, numerical temperature, Kelvin light or heating process.',
 'action':'Each of the two declared hands performs the joint holding action on that same mug, with the other hand and mug as exact receivers.',
 'contact_point':'Mug held wrapped by the exact two selected hand owners; contact is a new selected relation, never a frozen already-held prerequisite.',
 'prop_state':'The historical props.state.warm classification is not retained; warmth belongs to material thermal_state under the approved latest spec.',
 'hand_pose/body_pose':'No specific finger articulation or whole-body posture is authored; wrapping is retained as contact pattern without inventing angles.',
 'prop_placement':'No position/orientation beyond the selected contact relation is specified.',
 'sensory_cue/physical_motion/light_color':'No proxy, trajectory, steam, flow or illumination color temperature is supplied.',
 'relational_action':'Concrete joint holding is already retained, but the selected properties do not match this spec\'s interaction prefixes; do not manufacture another effect only to add that role.'}
rows[1]['both_hands_manual_adjudication']={
 'recommended_interpretation_for_root_review':'Exactly the two participating hand owners named by this holding action, not the holder\'s entire anatomical hand inventory.',
 'source_evidence':[{'pointer':'/content/en','quote':'held in both hands'},{'pointer':'/content/ko','quote':'두 손으로 감싼'},{'pointer':'/content/embedding_text','quote':'held in both hands'}],
 'reason':'Korean explicitly counts the hands participating in wrapping/holding. Neither language says the holder has only two hands in total, and no human-only intrinsic condition licenses a typical-anatomy inference. The proposed application makes this interpretive scope visible rather than silently changing the body.',
 'body_literals_preserved':True,'root_semantic_adjudication_required':True,
 'what_guards_prove':'Two distinct existing selected hand owners share one existing holder; mug is a distinct contact endpoint. They do not prove no third hand exists.',
 'selected_effect_scope':'Both hand E assignments and mug contact E specify the same participating pair and exact receiver membership at the selected instant. This is not a general hand-total or visible-framing count claim.',
 'total_inventory_alternative_unresolved':'If root reads both as every hand anatomically owned by the holder and exactly two total, these guards are insufficient. Keep that interpretation pending until independent exhaustive inventory/count evidence and an explicit supported source contract are reviewed. No count fact/capability is generated here.',
 'no_hidden_count_waiver':'No participant/subject/count modification or protected contact membership may be hidden by a selector. Any explicit global/visible count meaning in a later source must be separately authored and checked.'}
rows[1]['custom_tuple_warning']={'shared_neutral_guide':['subject/entity.presence/entity.presence/v1/present on mug, each hand, holder'],
 'existing_custom_namespaces':['body_geometry/body.part.presence/body.part.presence/v1/hand (actually read at1271)','subject/props.type/props.type/v1 (actually read at1254 and1271)'],
 'new_exact_source_specific_value':'mug for props.type/v1; this is manually grounded in the original mug/머그 noun, not old tags or a slot name.',
 'not_shared_defaults':'These hand and prop tuples are not common-guide presence defaults and do not follow from generic entity.presence, owner_kind, a category or a part_of edge. No human/body anatomy is automatically supplied.'}
payload={'schema':'photo-manual-source-local-guard-proposals/v1','author_task':'/root/native_evidence','date':'2026-10-15',
 'basis':'Direct individual original/current source, exact prior rows, selected nine proposals/root choices, latest full relevant specs and frozen source-guard-v2 implementation read. No synthetic source judgement conversion.',
 'root_source_approval_required':True,'canonical_applied':False,'native_proofs_created':0,'native_signatures_created':0,'new_native_approvals':0,'old_statuses_changed':False,
 'current_source_canonical_sha256':digest(current),'catalog_canonical_sha256':digest(catalog),'input_manifest':manifest,
 'actual_read_scope':{'target_original_and_current_whole_records':[1278,1296],'formal02_target_whole_rows':[1278,1296],
   'exact_original_5B_rows':[1278,1296],'nine_source_proposal_before_after_and_root_selected_deltas':[1258,1264,1265,1272,1275,1278,1280,1286,1296],
   'latest_full_specs_and_neighbors':latest_specs,'old142_embedded_target_specs':['action','character_contrast','expression','sensory_cue','contact_point','hand_pose','prop','prop_state'],
   'all_45_whole_records_reread_claimed':False,'whole144_new_read_count_claimed':False,'metadata_hashing_is_not_semantic_read':True},
 'records':rows,
 'mechanical_checks_are_not_qualification':{'exact_positive_quotes':True,'full_literal_top_delta':True,'same_local_assignment_value_type_operation_receiver_set':True,'exact_effect_property_coverage':True,'role_dimension_prefix_integrity':True,
  'does_not_prove':['semantic correctness of every clause','future actual owner/core matching','locked-property permission','exhaustive anatomical count','native or root approval','runtime acquisition','image pixels']}}
# Structural inspection only: no proof assembly, no status/category judgement.
for row in rows:
 a=row['source_after_proposed_full'];material=row['proposed_manual_authoring_material'];facts=material['facts'];byid={f['id']:f for f in facts};assignments={}
 assert len(byid)==len(facts) and 'role_evidence' not in a['content']
 assert a['id']==row['candidate_id'] and a['record_kind']==row['record_kind']
 for f in facts:
  val=a
  for key in f['pointer'][1:].split('/'):val=val[key]
  assert isinstance(val,str) and f['quote'] and f['quote'] in val,(row['ordinal'],f['id'])
  assert f['realization_id']=='base'
  if f['mode']=='effect':
   key=(f['realization_id'],f['dimension'],f['target'],f['property']);value=(canonical(f['value']),f['operation'],frozenset(f['receivers']))
   assert key not in assignments or assignments[key]==value,key
   assignments[key]=value
 assert {(f['dimension'],f['target'],f['property']) for f in facts if f['mode']=='effect'}=={(p['dimension'],p['target'],p['property']) for p in a['effects']['properties']}
 assert {f['dimension'] for f in facts if f['mode']=='effect'}==set(a['effects']['dimensions'])
 for unit in material['source_units']:
  assert unit['quote']==a['content'][unit['pointer'].rsplit('/',1)[-1]]
  assert set(unit['fact_refs'])=={f['id'] for f in facts if f['pointer']==unit['pointer']}
 for key,rolevalue in material['roles'].items():
  spec=catalog[key]
  for fid in rolevalue['fact_refs']:
   f=byid[fid];assert f['dimension'] in spec['dimensions']
   assert any(f['property']==p.rstrip('.') or f['property'].startswith(p if p.endswith('.') else p+'.') for p in spec['property_prefixes'])
 assert all(a[k]==current['candidates'][a['id']][k] for k in ['id','record_kind','provenance'])
 for key in ['en','ko','embedding_text','tags']:
  if key in a['content']:assert a['content'][key]==current['candidates'][a['id']]['content'][key]
assert not OUT.exists(), 'immutable proposal already exists'
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
print(str(OUT));print('raw_sha256',hashlib.sha256(OUT.read_bytes()).hexdigest());print('canonical_sha256',digest(payload));print('manual_facts',len(f1278),len(f1296))
