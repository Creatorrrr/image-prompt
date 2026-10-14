"""Serialize five individually authored, UNSELECTED source proposals. No native proof."""
import copy, gzip, hashlib, json, pathlib

R = pathlib.Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014')
BASE = 'native_05250_simple5-source-applications-source84-149-v1'
def digest(x):
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def raw(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(pathlib.Path(p).read_text())
def ref(p, value=None):
    p = pathlib.Path(p)
    return {'file':str(p), 'file_sha256':raw(p), 'sha256':digest(read(p) if value is None else value)}
def prop(dim, target, name): return {'dimension':dim, 'target':target, 'property':name}
def fact(fid, mode, dim, target, name, typ, value, pointer, quote, requires, **extra):
    return dict(id=fid, realization_id='base', mode=mode, dimension=dim, target=target,
                property=name, value={'type':typ,'value':value}, pointer=pointer,
                quote=quote, requires=requires, **extra)

CURRENT_PATH = R/'native-inputs/root-first20-source-plan-19/CURRENT-PROPOSAL.json.gz'
current = json.loads(gzip.decompress(CURRENT_PATH.read_bytes()))
assert digest(current) == '609e72864631ffccd711d2a6601ac060bea0a92f86985c7633a3fbea59d82ae5'
original = json.loads(gzip.decompress((R/'SOURCE.json.gz').read_bytes()))
plan_path = R/'authored/native_05250_05250_06250.simple-formal-readiness-149-v1.json'
plan = read(plan_path)
catalog_path = R/'CATALOG-FINAL-149-V6.json'
catalog = read(catalog_path)
assert digest(catalog) == 'd9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
original_packet_path = R/'packets/06000-250.json'
original_packet = read(original_packet_path)

APPS = {
6131: 'For this application, use the independently declared existing scene context as the setting carrier. Select its location as a card-tournament ruling-table setting unrelated to any proprietary game. The scene role is only an independently grounded address; this candidate does not establish that address or its existence. The selected location is an effect, not an already desired prerequisite. Retain the original primary card-adjudication tag condition. The ruling-table description does not require players, an active ruling, a ruling result, a branded game or a new separately owned table entity. Apply the setting change to that same scene only, retaining all original setting, actual-owner, alias, ancestor and whole-scope locks; do not avoid an original lock by moving the effect to a table or a different property.',
6162: 'For this application, use the independently declared existing scene context as the setting carrier. Select its location as a giant-machine maintenance hangar unrelated to any proprietary design. The scene role is only an independently grounded address; this candidate does not establish that address or its existence. The selected hangar location is an effect, not an already desired prerequisite. Retain the original primary mecha-sortie tag condition. The hangar purpose does not require a machine to be present, a visible repair operation, workers, a launch or a proprietary machine design. Apply the setting change to that same scene only, retaining all original setting, actual-owner, alias, ancestor and whole-scope locks; do not avoid an original lock by moving the effect to a hangar object or a different property.',
6191: 'For this application, use the independently declared existing scene context as the setting carrier. Select its location as the administrative hall at a secret-realm entrance in a fictional xianxia sect. The entrance adjacency and fictional sect setting belong to this selected location description; they do not establish a visible portal, an active registration procedure or a complete world-rule system. The scene role is only an independently grounded address; this candidate does not establish that address or its existence. The selected location is an effect, not an already desired prerequisite. Retain the original primary secret-realm tag condition. Apply the setting change to that same scene only, retaining all original setting, actual-owner, alias, ancestor and whole-scope locks; do not avoid an original lock by moving the effect to a hall object or a different property.',
6214: 'For this explicitly bounded interpretation, use the independently declared existing scene context as the carrier of all three selected effects: a cafe service-counter location, the cafe-closing event phase just before closing, and a quiet scene atmosphere. Here quiet means the proposed visually subdued atmosphere of this scene; it does not assert measured soundlessness, a private emotion, an empty cafe, reduced customer count, dim lighting or any particular action. This is a disclosed selection of the atmospheric reading of quiet rather than a claim that the original short phrase had only one possible interpretation. The scene address and its existence must be independently grounded; the selected location, event phase and atmosphere must not be prefrozen as desired prerequisites. The event is this same cafe closing; do not add a separate actor, a shutter-closing action, a completed closure, a night-time setting or a clock time. Retain the original primary affection-distance-scene tag condition and all original setting locks, together with the newly explicit timing and atmosphere effects and their actual-owner, alias, ancestor and whole-scope locks.',
6220: 'For this application, use the independently declared existing whole-image context as image_plane, on the same actual image addressed by the original applies_to whole_image relation. Apply clean continuous photographic edge rendering as the original style/image_plane/image.detail effect. Independently establish, on this same image, that the rendered object contours are continuous and the small surface details are readable, and preserve both of those properties throughout the selected change. These are two preservation obligations, not new contour or detail mutations; they do not create objects, surfaces or details. The image address and its existence must be independently grounded; neither the desired clean-edge value nor the two preservation witnesses may be fabricated from this candidate. Retain the original image.detail property and target exactly, the entire original whole-image scope, and every actual affected image-owner, alias, ancestor, property and whole-dimension lock. Do not move the effect to a physical object, rename its property to evade a lock, or treat preservation as permission to alter physical topology. If either preservation witness or the necessary complete actual affected scope is unknown, this application remains pending.'
}
REASONS = {
6131: 'The source selects a setting and names a ruling-table setting, without requiring an independently existing physical table object. Refining the coarse setting effect to setting.location on the explicitly selected scene carrier retains the selected location as E. The nonproprietary-game boundary is retained in the literal application and exact selected value; it supplies no game entity or proprietary rules. The scene address/existence must come from independent core input, not this source.',
6162: 'Maintenance hangar is the selected structural place; maintenance is its purpose, not a witnessed repair or an existing machine prerequisite. Refine the coarse setting E on an explicitly selected independent scene carrier. Do not prerequire a hangar-shaped desired scene or manufacture a giant machine. The unrelated-to-proprietary-design boundary remains part of the selected setting value and application.',
6191: 'The entire hall-at-entrance-in-fictional-sect phrase selects one location, including its declared adjacency and fiction context. Its specific location must stay E on an independent scene carrier. A portal owner, sect membership witness, registration event, or world-rule system is not required by this phrase and is not introduced. The explicit carrier selection is disclosed; it is not a claim that the source originally designated a primary scene.',
6214: 'Source84 still contains the obsolete generic Korean location, unlike the historical 5B correction. Restore that exact correction explicitly. The EN/embedding phrase includes location, just-before-closing phase and quiet. Adding timing/event-phase and atmosphere/quiet effects closes two omissions in the old coarse setting effect, rather than deleting phase or converting the desired state to P. Quiet is ambiguous between acoustics, activity and atmosphere; this proposal discloses a bounded atmospheric interpretation, with no silence/emotion/customer/lighting inference. Root must select this interpretive narrowing before a fresh proof can use it.',
6220: 'The original canonical effect is already style/image_plane/image.detail and remains byte-for-byte unchanged. Whole_image is the same image context, not an object receiver or a new owner. Both remain clauses are real preservation obligations. Use two literal typed PR values continuous/readable, rather than an unconstrained same-value sentinel that could preserve discontinuous/unreadable input. The source supports rendering/image properties, not changes to physical topology. Original and actual-scope locks remain cumulative; the App does not waive them.'
}
VALUES = {
6131:'card_tournament_ruling_table_unrelated_to_any_proprietary_game',
6162:'giant_machine_maintenance_hangar_unrelated_to_any_proprietary_design',
6191:'administrative_hall_at_secret_realm_entrance_in_fictional_xianxia_sect',
6214:'cafe_service_counter'
}
origin_paths = {
6131:('docs/research-evidence/photo-prompt/uniform-costume-integration-20261004/baseline/photo_prompt_cjk_worldbuilding_extension.json','/slots/location/33'),
6162:('docs/research-evidence/photo-prompt/uniform-costume-integration-20261004/baseline/photo_prompt_cjk_worldbuilding_extension.json','/slots/location/37'),
6191:('docs/research-evidence/photo-prompt/uniform-costume-integration-20261004/baseline/photo_prompt_cjk_worldbuilding_extension.json','/slots/location/4'),
6214:('docs/analysis/2026-10-07-photo-skill-session-review/p0-implementation/BEFORE-photo_prompt_character_moe_extension.json','/slots/location/3'),
6220:('docs/research-evidence/photo-prompt/slot-retrieval-stage02-20261011/before-runtime-store/generations/b9b706b2c56ddb15ac014b600c0c1c578767970a6d740dbb91e9cdc9f50e8788/assets/photo_prompt_editing_effects_extension.json','/slots/quality/1')
}
def pointer(x,p):
    for k in p.split('/')[1:]:x=x[int(k)] if isinstance(x,list) else x[k]
    return x
def differences(before, after, path=''):
    if isinstance(before,dict) and isinstance(after,dict):
        out=[]
        for k in sorted(before.keys()|after.keys()):
            pp=path+'/'+k.replace('~','~0').replace('/','~1')
            if k not in before:out.append({'pointer':pp,'before':None,'after':after[k],'operation':'add'})
            elif k not in after:out.append({'pointer':pp,'before':before[k],'after':None,'operation':'remove'})
            else:out += differences(before[k],after[k],pp)
        return out
    return [] if before==after else [{'pointer':path,'before':before,'after':after,'operation':'replace'}]

rows=[]
for old in plan['records']:
    ordinal=old['ordinal'];cid=old['candidate_id'];before=current['candidates'][cid]
    packet_path=pathlib.Path(old['whole_source_read_reuse']['packet']);packet=read(packet_path)
    pr=next(r for r in packet['records'] if r['ordinal']==ordinal)
    assert original['candidates'][cid] == pr['source_before']
    assert original_packet['records'][cid] == pr['source_before']
    loc=pr['original_compiled_locator']; compiled=read(loc['file'])['decisions'][loc['item']-1]
    assert raw(loc['file'])==loc['file_sha256'] and digest(compiled)==loc['row_sha256']
    assert compiled==pr['registered5B']
    bindings={k:v for k,v in current['slot_bindings'].items() if v['candidate_id']==cid}
    assert bindings==pr['own_existing_bindings']==old['existing_bindings']
    assert not pr['required_reference_records'] and not pr['explicit_reference_bindings']
    assert before == (pr['source_before'] if ordinal==6214 else pr['after_existing5B'])
    origin_file,origin_ptr=origin_paths[ordinal];origin=pointer(read(origin_file),origin_ptr)
    assert digest(origin)==before['provenance'][0]['sha256']
    after=copy.deepcopy(before);after['content']['application_contract']=APPS[ordinal]
    if ordinal in (6131,6162,6191,6214):
        after['effects']['properties']=[prop('setting','scene','setting.location')]
    if ordinal==6214:
        after['content']['ko']='폐점 직전의 조용한 카페 서비스 카운터'
        after['content']['aliases'][0]='폐점 직전의 조용한 카페 서비스 카운터'
        after['effects']['dimensions']=['setting','timing','atmosphere']
        after['effects']['properties'] += [prop('timing','scene','timing.event_phase'),prop('atmosphere','scene','mood.quiet')]
    target='image_plane' if ordinal==6220 else 'scene'
    facts=[fact('ownerP','prerequisite','subject',target,'entity.presence','entity.presence/v1','present','/content/application_contract','independently declared existing '+('whole-image context' if ordinal==6220 else 'scene context'),[])]
    if ordinal!=6220:
        facts.append(fact('locationE','effect','setting','scene','setting.location','setting.location/v1',VALUES[ordinal],'/content/en',before['content']['en'],['ownerP'],operation='set_value',receivers=[]))
    if ordinal==6214:
        facts += [fact('phaseE','effect','timing','scene','timing.event_phase','timing.event_phase/v1','cafe_closing_just_before','/content/en','just before closing',['ownerP'],operation='set_value',receivers=[]),
                  fact('quietE','effect','atmosphere','scene','mood.quiet','mood.quiet/v1','visually_subdued_scene_atmosphere','/content/application_contract','quiet means the proposed visually subdued atmosphere of this scene',['ownerP'],operation='set_value',receivers=[])]
    if ordinal==6220:
        facts += [fact('edgeE','effect','style','image_plane','image.detail','image.detail/v1','clean_continuous_photographic_edges','/content/en','clean continuous photographic edges',['ownerP','contoursPR','detailsPR'],operation='set_value',receivers=[]),
                  fact('contoursPR','preservation','style','image_plane','image.contour.continuity','image.contour.continuity/v1','continuous','/content/concept_units/0','object contours remain continuous',['ownerP']),
                  fact('detailsPR','preservation','style','image_plane','image.small_surface_detail.readability','image.small_surface_detail.readability/v1','readable','/content/concept_units/1','small surface details remain readable',['ownerP'])]
    for f in facts: assert f['quote'] in pointer(after,f['pointer'])
    roles=copy.deepcopy(old['role_plans'])
    rows.append({'ordinal':ordinal,'candidate_id':cid,'status':'unselected_source_application_proposal_pending_root_choice_and_fresh_native_input',
      'reason':REASONS[ordinal],'whole_original':pr['source_before'],'whole_historical_5B_after':pr['after_existing5B'],
      'whole_current_before':before,'whole_proposed_after':after,'before_sha256':digest(before),'after_sha256':digest(after),
      'source84_equals_prior_readiness_after':before==old['full_source_after'],
      'exact_deltas':differences(before,after),'own_bindings_unchanged':bindings,'required_closure':old['closure'],
      'actual_realization_ids':['base'],'profile_contract':None,'selected_dependencies':[],
      'intrinsic_conditions_before':before['conditions'],'intrinsic_conditions_after':after['conditions'],
      'binding_conditions_unchanged':{k:v['conditions'] for k,v in bindings.items()},
      'guard_refinement':'No existing structured condition is deleted, replaced or weakened. New App states the exact independent carrier requirement and same-carrier obligation; proposed P/PR are independently witnessed requirements, never candidate-derived core facts. There is no invented cross-owner relation or new native guard schema.',
      'proposed_manual_fact_plan_not_proof':facts,
      'owner_plan_not_actual_owner':{'source_target':target,'selector':{'kind':'core_role','role':'image' if ordinal==6220 else 'scene'},'origin':'existing','introduced_by':None,
          'independent_core_requirement':'An actual owner declaration, exact role binding, independent typed entity.presence/v1=present witness and complete actual lock topology must already be frozen independently. A controlled synthetic core may test a conditional contract, but is not evidence of an actual user request. No role-only existence or arbitrary main/foreground inference.'},
      'role_plans_not_approved':roles,'all_primary_source_unit_plan':{
          'en_ko_embedding':'Each complete EN, KO and embedding field independently retains its local positive clauses; partial fields may use reviewed one-hop references to ordinary positive units without strengthening their own quote. 6214 KO correction is an explicit proposal, not a presumed existing field.',
          'application_contract':'Entire exact App is a positive application unit. Direct facts must use their actual local clauses; negative limits, same-carrier constraints and original-lock duties remain binding in a retained-constraint reference. This proposal does not classify those duties away as nonsemantic metadata.',
          'facets':'The manifestation_mode/narrative_variant fields in 6131/6162/6191 remain routing context; they do not create objects, performed events or a world-rule system.',
          'concept_units_and_relations':'6220 both concept_units are ordinary preservation anchors; relation subject/type/object jointly retains same whole-image scope. It cannot be borrowed to identify a physical object or a second actual image.',
          'metadata':'Aliases, keywords and tags are retained but cannot supply positive facts or independent prerequisites.'},
      'permission_and_test_obligations':[
          'Keep original coarse dimension locks as well as the explicit refined property addresses; no role-prefix rename or receiver relocation.',
          'Test independently authored open-scope core, desired-value-as-P rejection, missing/wrong owner/role/presence, actual original-property lock, actual aliases/ancestors and whole dimensions; exact source and selected RID must bind both full and compact checks.',
          '6220 additionally requires separate missing/wrong/contradictory contour and detail PR tests and preservation conflicts in the complete selected effect union; retain the same image on both relation and actual effect.',
          '6214 timing and quiet atmosphere must remain actual effects and fail their own property/whole-dimension locks even when the setting property is open.'
      ],
      'remaining_gaps':['Root must select or reject this complete proposed after, including its disclosed application scope; no selection is presumed.',
          'Fresh exact sparse INPUT/ASSIGNMENT and actual full/compact/native/union-lock checks remain unrun.',
          'No generic feature or source text proves an actual compatible independently frozen core. Missing carrier/preservation/actual affected scope stays pending.'],
      'provenance':{'compiled_locator':loc,'original_packet':{**ref(original_packet_path,original_packet),'record_pointer':'/records/'+cid,'record_sha256':digest(pr['source_before'])},
          'bulk_read_packet':{**ref(packet_path,packet),'record_pointer':'/records/'+str(packet['records'].index(pr)),'record_sha256':digest(pr)},
          'origin':{**ref(origin_file),'pointer':origin_ptr,'entry_sha256':digest(origin),'whole_entry':origin},
          'historical_5B':compiled}})

for row in rows:
    assert row['intrinsic_conditions_before']==row['intrinsic_conditions_after']
    assert set(row['whole_current_before']['effects']['dimensions']) <= set(row['whole_proposed_after']['effects']['dimensions'])
    if row['ordinal']==6220:assert row['whole_current_before']['effects']==row['whole_proposed_after']['effects']
    assert not any(d['operation']=='remove' for d in row['exact_deltas'])

spec_ids=['location','narrative_phase','mood','image_detail','space_condition','environment_detail','background_element','world','focus','depth_of_field','sensory_cue','time_of_day','publication_caption_context','visible_text','lens','procedure_step','calendar_context','season','historical_period','transformation_stage']
out={'schema':'photo-manual-source-application-proposals/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high',
     'status':'unselected_proposals_only','source84':{'file':str(CURRENT_PATH),'file_sha256':raw(CURRENT_PATH),'sha256':digest(current)},
     'prior_readiness':ref(plan_path,plan),'catalog':ref(catalog_path,catalog),
     'direct_read_attestation':{'records':5,'whole_original_current_exact5B_bindings_empty_closure_reread':True,'whole_exact_provenance_entries_read':5,'used_and_needed_neighbor_fullspecs_read':spec_ids,'new_unique_bulk_read_count':0,
         'source84_equality':{'same_as_readiness_after':[6131,6162,6191,6220],'6214':'Actual source84 equals original; prior 5B corrected KO/alias was not incorporated. Proposal explicitly reapplies those two before/after corrections.'},
         'proofs_created':0,'formal_checks':0,'root_acceptance':0,'operating_changes':0,'Git':0,'model_calls':0,'network_calls':0},
     'full_specs':{k:{'sha256':digest(catalog[k]),'full_spec':catalog[k]} for k in spec_ids},'records':rows}
dest=R/'authored'/f'{BASE}.json'
note=R/'worker-notes'/f'{BASE}.json'
assert not dest.exists() and not note.exists()
dest.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
noteobj={'schema':'photo-worker-source-proposal-note/v1','task_name':'/root/review_05250_06250','model':'gpt-6.1-sol','reasoning_effort':'high',
         'artifact':ref(dest,out),'ordinals':[6131,6162,6191,6214,6220],'directly_rereviewed_count':5,'new_unique_bulk_count':0,
         'selected_source_count':0,'native_proofs_created':0,'formal_checks_run':0,'qualified_count':0,
         'issues':['6214 current KO/alias discrepancy explicitly preserved in before and repaired only as proposed delta.','6214 quiet atmospheric reading is a disclosed bounded choice, not uniquely entailed interpretation.','6220 original canonical style/image_plane/image.detail is unchanged; historical origin rendering.quality spelling is provenance only, not permission to rename the canonical effect.','Source84 ownbindings remain unchanged; proposed added semantic role plans do not authorize new bindings.'],
         'mechanical_checks':{'source84_catalog_hashes':True,'all_original_and_5B_rows_exact':True,'all_compiled_file_item_row_hashes':True,'all_packet_original_records':True,'all_origin_hashes':True,'all_fact_quotes_exact':True,'all_intrinsic_conditions_retained':True,'no_effect_dimension_removed':True,'6220_original_effect_exact':True},
         'native_boundary':'No proof, acceptance, admission, full/compact, consumer, pixel or operating qualification. Existing plans/prototype/diagnostic artifacts unchanged.'}
note.write_text(json.dumps(noteobj,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
for p in [dest,note]:
    print(json.dumps({'file':str(p),'raw_sha256':raw(p),'canonical_sha256':digest(read(p))},ensure_ascii=False))
