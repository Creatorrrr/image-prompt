"""Serialize seven individually authored semantic rechecks; never rewrite a batch."""
import copy,gzip,hashlib,json,pathlib
R=pathlib.Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014')
BASE='native_diag70_05250_recheck7'
def H(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def read(p):return json.loads(pathlib.Path(p).read_text())
def raw(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def ref(p,x=None):return {'file':str(p),'file_sha256':raw(p),'sha256':H(read(p) if x is None else x)}
def at(x,p):
 for k in p.split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k]
 return x
def save(p,x):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
 print(json.dumps(ref(p,x),ensure_ascii=False))
packetpath=R/'authored/native_diag70_05250_read-packet-v1.json';packet=read(packetpath)
originpath=pathlib.Path(packet['origin']['file']);origin=read(originpath)
graph=origin['character_mechanism_graph']
assert raw(originpath)=='e9583cde4ce74e46e6f28501c976f9fe8b1efd1691546416b751fe774c13bb42'
assert {k:graph[k] for k in packet['origin_graph_context']}==packet['origin_graph_context']
currentpath=R/'native-inputs/root-first20-source-plan-19/CURRENT-PROPOSAL.json.gz'
current=json.loads(gzip.decompress(currentpath.read_bytes()))
assert H(current)=='609e72864631ffccd711d2a6601ac060bea0a92f86985c7633a3fbea59d82ae5'
batchpath=R/'native_batches/review05250-diagnostic70-149-01/BATCH.json';batch=read(batchpath)
assert H(batch)=='93c29b1bea8f5e55a8443bc336a378157820c8d902795977767ce8abf25e7247'
catalogpath=R/'CATALOG-FINAL-149-V6.json';catalog=read(catalogpath)
assert H(catalog)=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'

JUDGMENTS={
12005:{
 'recommendation':'HOLD_source_purpose_ambiguity_do_not_accept_prior_nonsemantic_proof',
 'positive_clause':'an authored delay between a relationship trigger and an observable prosocial response',
 'why_prior_basis_insufficient':'The absence of a concrete response, measurable delay or current request does not prove that this definition lacks a conditional temporal obligation. An authored delay is an affirmative temporal relation, just as the restored12027 feature-retention definition has affirmative continuity without a fixed feature. A still image cannot measure a sequence, but a source can declare event timing as narrative context. Treating that limit as proof that all timing meaning is nonsemantic was too strong.',
 'source_purpose_evidence':'The exact node is affection_latency_axis. Its family says affect is made legible through action/expression/gaze/context; dere compatibility requires relationship_trigger, care_or_protection_action and affect_latency_or_distance. The axis itself is not a selectable node in that compatibility list. This is substantive evidence for an authoring-axis purpose, but the family and concrete action example also give a positive trigger-to-delayed-response use. The node body does not expressly say it is only a storage/check instruction.',
 'comparison':'Unlike12027, the noun axis and absence from the route selectable-node list favor routing. Like12027, the exact definition still states an authored relation. Neither contrast settles the candidate emission contract without an explicit editorial choice.',
 'role_and_mode_limits':'narrative_phase needs an explicit selected instant/phase in an event; delay alone does not select that instant or seconds. relational_action/action need an actual response and supported endpoints. A declared temporal relation may later support context or a selected timing E; do not invent a caring action, actor, recipient, duration or classify the entire definition nonsemantic merely to force E0.',
 'A_definition':'Authoring-axis metadata for recording a separately specified relationship-trigger-to-prosocial-response delay. This record is a routing/check definition only: adopting it does not select a trigger, response, temporal phase, duration, actor or visible action. Any such selected obligation must be carried by separately reviewed positive source records.',
 'A_cost':'This chooses the storage/check interpretation and expressly removes this record as an emitter of the affirmative delay relation. It is a disclosed narrowing, not a synonym-only repair.',
 'B_gap':'Restore visual_option while retaining the entire existing delay definition. Keep proof null until the intended trigger/response relation, carrier, selected temporal phase if any, current source conditions and actual P/PR/context/E interpretation are explicitly selected. No new measurable-duration or past-event proof follows.',
 'specs':['narrative_phase','character_intent','action','relational_action','narrative_clue','character_contrast'],
 'comparison_ordinals':[12027],
},
12023:{
 'recommendation':'HOLD_positive_presentation_template_not_purely_diagnostic',
 'positive_clause':'A user-selected mixed or ambiguous presentation axis',
 'why_prior_basis_insufficient':'The body says user-selected mixed or ambiguous presentation, not merely an unselected vocabulary of possible identities. Lack of a concrete garment, hair or anatomy value does not erase that visual-presentation selection. The separate identity/personality/role/affect storage boundary constrains the selection but does not make the selected presentation nonvisual.',
 'source_purpose_evidence':'The adult cultural family and exact presentation_axes_do_not_infer_identity guard keep presentation separate from identity and orientation; their policy does not prohibit positive gender presentation. Compatibility lists caring_action_evidence and competence_vulnerability_gap rather than this axis, which supports an architectural axis role. Yet the independent slot subject explicitly selects an adult androgynous technician. That example shows intended visible presentation is compatible, without becoming a mandatory member or granting its concrete technician/coworker features to this node.',
 'comparison':'The restored12038 generic nonhuman subject did not require a named species before positive treatment. Similarly mixed/ambiguous presentation need not specify a fixed gender identity or anatomy to remain a positive conditional template. Mixed OR ambiguous stays an alternative, not two simultaneous values.',
 'role_and_mode_limits':'gender_presentation is the relevant full149 role for explicit visual presentation and forbids identity/sex/personality/orientation inference. presentation_style may apply only if actual personal styling is selected. User-selected does not mean already present: do not prefreeze the desired mixed/ambiguous value as P or fabricate masculine/feminine feature sets. Adult policy in original context is not a candidate-local explicit age witness.',
 'A_definition':'Routing-schema metadata that stores a presentation-axis selection separately from identity, personality, role and affect. This record only describes the storage boundary and does not select or require any visible mixed or ambiguous presentation. Any user-selected visible presentation must be represented by a separately reviewed positive source record.',
 'A_cost':'This explicitly removes the original user-selected mixed/ambiguous visual obligation from this candidate; selecting it is a semantic narrowing of purpose.',
 'B_gap':'Restore visual_option with the definition unchanged, retaining mixed OR ambiguous and all non-inference limits. Keep proof null until actual selected carrier, branch/value, complete appearance effects or actual preservation requirements and route adult/non-inference conditions have a source-supported contract.',
 'specs':['gender_presentation','presentation_style','age_presentation','wardrobe_style','character_intent'],
 'comparison_ordinals':[12038],
},
12034:{
 'recommendation':'HOLD_positive_presentation_cues_template_not_purely_diagnostic',
 'positive_clause':'A user-selected set of culturally masculine presentation cues',
 'why_prior_basis_insufficient':'The selected cue set is an affirmative visual-presentation parameter. The fact that its individual features are not filled does not make it an empty authoring rule. Non-inference of identity is necessary but cannot erase the selected masculine-presentation requirement.',
 'source_purpose_evidence':'The adult cultural family, route policy and presentation guard make identity/orientation non-inference explicit. The axis is not in the compatibility selectable-node list; this favors storage architecture, while the family/subject/action examples show visible mixed presentation intentionally coexists with competence/care. None of these examples chooses the actual cue set for this node. They are separate original slot records rather than native member dependencies.',
 'comparison':'As12038 can remain a positive generic nonhuman description without a species, culturally masculine presentation can remain positive without invented biological sex, facial hair, outfit or demeanor. The restored12027 also preserves an unfilled feature parameter. Unfilled cue identities are an authoring gap, not a diagnostic criterion.',
 'role_and_mode_limits':'gender_presentation directly admits explicit visual presentation without identity inference. Specific wardrobe_style/hair/body/face tags require their own selected actual cue facts and owners; no such cues are supplied here. The culturally qualified selected set must not become a universal masculine anatomy rule. Desired cue selection remains E when it changes appearance, not an already desired P.',
 'A_definition':'Routing-schema metadata for storing a separately specified culturally masculine presentation-cue set independently from identity, personality, role and affect. This record only defines the storage/non-inference boundary; it does not select, add or preserve any visible masculine cue. Actual selected presentation cues belong to separately reviewed positive source records.',
 'A_cost':'This removes the original selected cue-set obligation from this candidate and is therefore a disclosed check-only narrowing.',
 'B_gap':'Restore visual_option, retaining the complete definition. Proof stays null pending source-supported selected set, independently grounded carrier, actual P/PR/E and full effects/guards. Do not invent a stereotyped cue list or infer identity, orientation or adulthood from the presentation.',
 'specs':['gender_presentation','presentation_style','wardrobe_style','age_presentation','character_intent'],
 'comparison_ordinals':[12038,12027],
},
12050:{
 'recommendation':'HOLD_positive_same_subject_two_anchor_contract_with_router_purpose_ambiguity',
 'positive_clause':'linking one explicitly same subject across ordinary and transformed states through at least two continuity anchors',
 'why_prior_basis_insufficient':'The definition has actual positive same-subject, two-state and minimum-two-anchor requirements. Calling the prefix base router is evidence of architectural purpose, but it does not make these remaining obligations nonsemantic. Missing concrete anchors is not sufficient, as restored12051 also has unfilled continuity alternatives.',
 'source_purpose_evidence':'The performance family explicitly links transforming characters across states by action/continuity. Transformation compatibility requires civilian_powered_continuity, responsibility_or_burden and recovery_or_repair, and lists transformation_continuity_anchor_pair. The base node is not itself in the selectable list. Original ordinary pager/protective-glove/color-echo examples make continuity meaningful but are not mandatory members; they cannot fill the two anchors in this record.',
 'comparison':'12051 allows a goal OR value OR object OR posture OR behavior to retain one character. This record is stricter: explicitly same subject, ordinary AND transformed states, and at least two continuity anchors. Those cardinality/conjunction requirements must remain if the positive interpretation is restored; neither two people nor an animation sequence follows.',
 'role_and_mode_limits':'character_contrast may expose an actually declared role/state contrast, while transformation_stage requires an observable selected transformation stage and cannot be supplied merely from ordinary/transformed state labels. reality_anchor needs an ordinary reference explicitly related to an extraordinary concept; the generic word anchor is insufficient. Actual identity continuity, state display and two complete anchors need explicit source-native P/PR/context/E mapping, not an invented set fact or count waiver.',
 'A_definition':'Base routing/check metadata for evaluating separately authored ordinary and transformed state records: the authored records must explicitly designate the same subject and supply at least two continuity anchors. This metadata record does not itself select, depict, preserve or add either state, a subject or an anchor; those obligations must be carried by the separately reviewed positive records.',
 'A_cost':'This expressly transfers the positive state/continuity duties to other records, narrowing this record to a checker. It cannot be treated as a no-meaning-change diagnostic repair.',
 'B_gap':'Restore visual_option with the exact positive definition unchanged. Keep proof null until the same-subject state carriers, minimum-two-anchor contract, any existing identity P/PR, complete selected effects and all scope locks are explicitly representable and source-selected. No new states/anchors, fake count or partial proof.',
 'specs':['character_contrast','transformation_stage','reality_anchor','narrative_clue','narrative_core','subject'],
 'comparison_ordinals':[12051],
},
12082:{
 'recommendation':'HOLD_strong_positive_four_part_readability_preservation',
 'positive_clause':'A generic action, relationship, location, and prop remain readable',
 'why_prior_basis_insufficient':'Remain readable is an affirmative preservation requirement on all four coordinated meanings. Generic/unfilled values do not make that requirement a pure checklist, as12027 keeps an unfilled feature-retention requirement. The national-style non-inference limit is negative; it does not negate the positive four-part legibility clause.',
 'source_purpose_evidence':'The exact CJK compatibility names culture_neutral_scene_anchor as its only selectable node, minimum_nodes=maximum_nodes=1 and primary_required=true. The cjk_market_terms_are_nonvisual guard requires this node for market-term routers. The source separates nonvisual market labels from their required visible fallback; this node is that positive fallback, not itself one of the market labels. Original action/location/prop examples corroborate that purpose without supplying this candidate with their handoff, studio or cards.',
 'comparison':'This is at least as preservation-like as12027 ranked-feature retention and12093 visible backstage separation. Its action AND relationship AND location AND prop must all remain readable. It neither creates those four carriers nor permits one legible element to substitute for the rest.',
 'role_and_mode_limits':'Actual action/relationship/location/prop facts and their owners must come from independent selected inputs. A bounded existing-contract interpretation can require their separate readability PR values, but cannot silently add actors/props or assume a universal image.detail/visual_hierarchy fact. Reading priority/order is not stated; visual_hierarchy therefore is not already supported. Restoration is not an automatic four-tag union.',
 'A_definition':'Diagnostic review checklist for testing separately authored scene records: check that the independently specified generic action, relationship, location and prop remain readable without national-style inference. This checklist does not itself select or preserve any scene element or readability property; those positive obligations must be represented in the separately reviewed scene records.',
 'A_cost':'This removes this node as the required positive culture-neutral fallback and would require reviewing the original compatibility/guard purpose. It is an explicit semantic narrowing, particularly weak as a neutral repair because the original graph selects this node as its sole visual anchor.',
 'B_gap':'Restore visual_option with the original definition unchanged and keep proof null. A later source application must independently identify all four contracts/carriers and preserve their readability with correct complete P/PR/effects/guards. The existing empty effect set is not evidence that E0 is valid or that the four obligations may be ignored.',
 'specs':['action','relational_action','location','prop','visual_hierarchy','composition','narrative_core','visible_text'],
 'comparison_ordinals':[12027,12093],
},
12156:{
 'recommendation':'HOLD_strong_positive_single_motif_governing_selected_features',
 'positive_clause':'One coherent animal, plant, object, or invented motif governs the selected nonhuman features',
 'why_prior_basis_insufficient':'The definition positively binds selected nonhuman features to one coherent motif. Animal/plant/object/invented are alternatives for that one motif, not an absence of meaning or a requirement for all four. Lack of a named motif/species does not justify erasing the selected-feature relation, just as a generic nonhuman subject12038 remains positive.',
 'source_purpose_evidence':'The exact nonhuman compatibility directly includes character_moe_nonhuman_motif_anchor among its selectable visual nodes and requires original_species_motif together with functional_nonhuman_marker and gaze_head_body_alignment. The governing motif is part of the route positive evidence, while no-feature-piling is a limiting constraint. The courier-ear-tail example is separate and cannot supply missing anatomy or an actual motif to this node.',
 'comparison':'12027 retains a ranked feature across counterparts; this node retains coherent control of selected nonhuman features by one motif. Both may need a conditional source application. A coherence rule can be a positive relational/preservation contract; being a rule does not make it automatically nonsemantic.',
 'role_and_mode_limits':'species_marker requires actual anatomical species cues on a declared subject; body_form requires stated nonfacial anatomical form. Animal/plant/object motif words alone establish neither anatomy nor a real animal/plant/object. A feature could be represented or ornamental. Modes depend on whether selected actual features/motif are to be preserved or newly changed, so E0/PR cannot be assumed from governs. No added ear, tail or body inventory.',
 'A_definition':'Diagnostic motif-coherence checklist for separately authored nonhuman feature records: check whether their independently selected animal, plant, object or invented motif is coherent and avoids feature piling. This checklist does not itself select, govern, change or preserve any motif or feature; all positive feature and motif obligations belong to separately reviewed records.',
 'A_cost':'This removes this node as a positive governing-motif contract and changes the original selectable-visual-node purpose. It is a disclosed narrowing, not a clarification justified by an unfilled parameter.',
 'B_gap':'Restore visual_option without changing definition or OR/conjunction scope; keep proof null. Root must choose a complete source application identifying actual motif/features/carrier, preservation versus mutation and full effects/guards. Do not invent a named species, living plant or physical prop from the motif class.',
 'specs':['species_marker','body_form','subject','presentation_style','character_contrast'],
 'comparison_ordinals':[12027,12038],
},
12159:{
 'recommendation':'HOLD_source_purpose_ambiguity_positive_same_character_state_comparison',
 'positive_clause':'comparing two or more explicitly same-character states through action, relation, material history, or responsibility rather than rarity UI',
 'why_prior_basis_insufficient':'Design-heuristic router is stronger purpose evidence than a role header alone, but the body still contains a positive same-character comparison with a minimum-two-state requirement and specified kinds of comparison evidence. Unselected action/relation/history/responsibility alternatives do not prove there is no comparison contract. The prior E0/nonsemantic decision did not resolve this tension.',
 'source_purpose_evidence':'The performance family says transforming characters remain linked across states by action/continuity. Growth compatibility requires earned_skill_or_role_change, material_history and identity_continuity and lists actual branch-continuity, fluency, posture and relationship-change nodes. This base design-heuristic router is absent from that selectable-node list, supporting a checker interpretation. Yet the concrete action/used-repaired-tool examples and family purpose also support a positive state-comparison mechanism; they cannot automatically instantiate it.',
 'comparison':'Like12050, it explicitly compares at least two states of the same character. Unlike12050, it does not require ordinary/transformed states or at least two anchors; action OR relation OR material history OR responsibility are alternative comparison bases. Like12051, retaining an unspecified continuity relation may still be a positive source obligation.',
 'role_and_mode_limits':'character_contrast needs a declared visible/local role/status contrast, narrative_clue an owned visible clue to a declared event, and transformation_stage an explicitly selected observable transformation stage. Progression does not itself prove a body transformation or elapsed history in a still. Rarity-UI avoidance does not authorize deleting an existing UI or create a visible_text mutation. Actual state comparison/modes/owners remain unresolved.',
 'A_definition':'Design-heuristic routing/check metadata for comparing separately authored records of two or more explicitly same-character states using separately specified action, relation, material-history or responsibility evidence instead of relying on rarity UI. This metadata record does not itself select, depict, change or preserve states or comparison evidence; those positive duties must be carried by separately reviewed source records.',
 'A_cost':'This explicitly narrows the candidate to the authoring tool and relocates all state-comparison duties. The design-heuristic prefix supports that choice, but does not make it a harmless rewrite of the full original clause.',
 'B_gap':'Restore visual_option with the complete original definition unchanged; proof remains null until actual same-character states, selected comparison evidence, minimum-state requirement and every P/PR/context/E and original-scope lock are explicitly source-selected. Do not force all four comparison bases or create a progression sequence.',
 'specs':['character_contrast','narrative_clue','transformation_stage','participant_role','action','relational_action','narrative_core'],
 'comparison_ordinals':[12050,12051],
}}

topics={'dere_behavior_spectrum','adult_masculine_androgynous_moe','transformation_heroine_double_life','cjk_term_character_grammar_comparison','kemonomimi_nonhuman_anthropomorphism','growth_evolution_rarity_variants'}
parents=[]
for slot,rs in origin['slots'].items():
 for i,r in enumerate(rs):
  if set(r.get('tags',[]))&topics:parents.append({'pointer':f'/slots/{slot}/{i}','sha256':H(r),'whole_record':r})
specs=['gender_presentation','presentation_style','age_presentation','wardrobe_style','character_contrast','species_marker','body_form','character_intent','action','relational_action','narrative_phase','narrative_clue','narrative_core','reality_anchor','subject','composition','visual_hierarchy','participant_role','location','prop','visible_text','transformation_stage']
context={'schema':'photo-diagnostic-recheck-context/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high',
 'origin_file':ref(originpath,origin),'whole_graph_context':packet['origin_graph_context'],
 'whole_root_metadata':{k:origin[k] for k in ['maintenance_ref','schema_version','slot_applicability','coherence_rules']},
 'parent_route_records_read':parents,'parent_relation_boundary':'These are original contextual route examples and graph rules, not required native candidate/binding closure. No member union or inheritance of their actors, actions, tools, anatomy or age facts.',
 'catalog':ref(catalogpath,catalog),'full_specs':{k:{'sha256':H(catalog[k]),'full_spec':catalog[k]} for k in specs},
 'fullspec_read_boundary':'Full gender/presentation/age/wardrobe/contrast/species/body/intent/action/relational/narrative/subject/composition/hierarchy/participant specs directly read; exact same location/narrative_phase and other earlier directly read relevant specs reused from fixed149. No all149 fresh-read claim.',
 'source84':{'file':str(currentpath),'file_sha256':raw(currentpath),'sha256':H(current)},'prior_batch_immutable':ref(batchpath,batch)}
contextpath=R/'authored'/f'{BASE}.context-v1.json';save(contextpath,context)
index=[]
for ordinal,j in JUDGMENTS.items():
 row=next(r for r in packet['records'] if r['ordinal']==ordinal);cid=row['candidate_id']
 assert current['candidates'][cid]==row['original']==row['current66']
 assert not {k:v for k,v in current['slot_bindings'].items() if v['candidate_id']==cid}
 assert not row['required_original_closure'] and not row['required_current_closure']
 assert at(origin,row['origin']['pointer'])==row['origin']['record']
 assert H(row['origin']['record'])==row['origin']['canonical_sha256']==row['original']['provenance'][0]['sha256']
 compiled=read(row['original5B']['file'])['decisions'][row['original5B']['item']-1]
 assert compiled==row['original5B']['row'] and H(compiled)==row['original5B']['row_sha256']
 assert raw(row['original5B']['file'])==row['original5B']['file_raw_sha256']
 old=next(r for r in batch['records'] if r['ordinal']==ordinal)
 assert j['positive_clause'] in row['original']['content']['definition']
 A=copy.deepcopy(row['original']);A['content']['definition']=j['A_definition']
 B=copy.deepcopy(row['original']);B['record_kind']='visual_option'
 relevant=row['original']['content']['topic_ids']
 family=row['original']['content']['family_ids']
 source_before=row['original']
 obj={'schema':'photo-independent-diagnostic-purpose-recheck/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high',
  'ordinal':ordinal,'candidate_id':cid,'recommendation':j['recommendation'],'whole_source_before':source_before,
  'source_before_sha256':H(source_before),'exact_source84_equals_source66_and_original':True,
  'whole_origin':row['origin'],'original_compiled_5B':row['original5B'],'own_bindings':{},'required_closure':{},
  'prior_native_row':{'artifact':ref(batchpath,batch),'pointer':'/records/'+str(batch['records'].index(old)),'sha256':H(old),'prior_rationale':old['rationale'],'proof_sha256':H(old['proof'])},
  'context':ref(contextpath,context),'exact_family_pointers':[{'pointer':f'/character_mechanism_graph/families/{i}','sha256':H(v)} for i,v in enumerate(graph['families']) if v['id'] in family],
  'exact_compatibility_pointers':[{'pointer':f'/character_mechanism_graph/compatibility_edges/{i}','sha256':H(v),'whole_rule':v} for i,v in enumerate(graph['compatibility_edges']) if v['topic_id'] in relevant],
  'exact_parent_route_pointers':[{'pointer':v['pointer'],'sha256':v['sha256']} for v in parents if set(v['whole_record'].get('tags',[]))&set(relevant)],
  'positive_clause':j['positive_clause'],'why_prior_nonsemantic_basis_is_not_sufficient':j['why_prior_basis_insufficient'],
  'whole_original_source_purpose_assessment':j['source_purpose_evidence'],'comparison_with_restored_positive_templates':j['comparison'],
  'full149_role_mode_boundary':j['role_and_mode_limits'],'used_specs':{k:{'sha256':H(catalog[k]),'context_pointer':'/full_specs/'+k} for k in j['specs']},
  'comparison_source_records':[{'ordinal':r['ordinal'],'candidate_id':r['candidate_id'],'whole_original':r['original'],'whole_source84':current['candidates'][r['candidate_id']],'origin':r['origin'],'same_native_body_except_root_kind_restore':current['candidates'][r['candidate_id']].get('content')==r['original']['content']} for r in packet['records'] if r['ordinal'] in j['comparison_ordinals']],
  'unselected_minimal_alternatives':[
    {'id':'A_explicit_check_only_narrowing','status':'unselected_editorial_purpose_change','whole_before':source_before,'whole_after':A,
     'delta':[{'pointer':'/content/definition','before':source_before['content']['definition'],'after':j['A_definition'],'reason':j['A_cost']}],
     'consequence':'record_kind remains diagnostic only if root deliberately selects this narrower source purpose. All other fields unchanged; new source/input and semantic proof required. This is not approval of the existing all-nonsemantic proof.'},
    {'id':'B_preserve_positive_contract_restore_kind_only','status':'unselected_positive_recovery_hold','whole_before':source_before,'whole_after':B,
     'delta':[{'pointer':'/record_kind','before':'diagnostic','after':'visual_option','reason':'Preserve the exact existing positive/template obligation pending complete source-native application, without claiming its unresolved facts/effects are already valid.'}],
     'remaining_gap':j['B_gap'],'proof':None}],
  'selected_alternative':None,'native_or_source_modifications':0,'new_proofs_created':0,'native_validation_run':0,'root_acceptance':0,'qualified':0,
  'recheck_attestation':'Whole original/current, exact origin, 5B/ownbindings/empty closure reread; full graph family/compatibility/policy/guard context and relevant full original parent route examples directly reread. Empty effect set, old kind, router/visual_atom metadata and unfilled values are never sufficient reasons for diagnostic acceptance. Prior artifacts remain historical and unmodified.'}
 path=R/'authored'/f'{BASE}.{ordinal}.memo-v1.json';save(path,obj);index.append({'ordinal':ordinal,'candidate_id':cid,'artifact':ref(path,obj),'recommendation':j['recommendation']})
note={'schema':'photo-worker-diagnostic-recheck-note/v1','task_name':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high',
 'context':ref(contextpath,context),'memos':index,'directly_rereviewed_count':7,'new_unique_corpus_count':0,
 'recommendations':{'additional_semantic_holds':7,'new_diagnostic_acceptances':0,'positive_native_approvals':0},
 'prior_65_boundary':'The old shape-valid65 diagnostic proofs are immutable history, not semantic acceptance. These7 recommendations withdraw reliance on their prior all-nonsemantic rationale. This memo does not revalidate or approve the other58; root decides any final58/12 partition after independent review and fresh input.',
 'differences_in_strength':'12082 and12156 have direct selectable visual-node/required-fallback context and strong positive obligations.12023/12034 have selected-presentation meaning despite storage/identity separation.12050 has explicit same-subject/two-anchor obligations despite a base-router prefix.12005 and12159 have stronger axis/design-tool purpose evidence, yet their affirmative temporal/state-comparison clauses leave purpose ambiguity unresolved without disclosed source selection.',
 'all_seven_A_and_B_unselected':True,'original_batch_unchanged':raw(batchpath)==ref(batchpath,batch)['file_sha256'],
 'all_exact_origin_and_compiled_hashes_checked':True,'formal_checks':0,'consumer_checks':0,'source_changes':0,'operating_changes':0,'Git':0,'model_calls':0,'network_calls':0}
save(R/'worker-notes'/f'{BASE}.note-v1.json',note)
