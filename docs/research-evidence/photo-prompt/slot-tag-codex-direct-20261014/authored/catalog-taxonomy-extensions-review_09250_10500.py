"""Explicit taxonomy judgments; mechanical offline serialization/binding only."""
import copy
import hashlib
import json
from pathlib import Path
import sys

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R))
import direct_review as dr
from photo_candidate_realizations import ids

NAME = 'catalog-taxonomy-extensions-review_09250_10500'
TASK = '/root/review_09250_10500'
ROOT_READS = [12382,12616,4555,5432,6616,10133,10187,10883,11832,10001,1741,
              915,9733,8176,10119,10423,10274,11467,5640,1122,1430,10730,10376]
SPEC_READS = ['composition','body_form','garment_detail','prop','prop_state','contact_point',
    'prop_placement','surface_material','texture','environment_detail','ambient_particle',
    'atmospheric_medium','image_detail','subject','silhouette_proportion','garment_state',
    'garment_fit','physical_motion','space_condition','scale_relation','anatomical_connection']

OBJECT_SPEC = {
    'id':'object_structure', 'semantic_role':'direct', 'priority':'support',
    'description':'Visible non-anatomical geometry, bounded parts and structural connections owned by one declared physical object or fixture, independent of its scene role, frame placement and current use state.',
    'description_ko':'선언된 물리적 물체·설비 자체의 비해부학적 형상, 경계가 있는 부품과 구조적 연결. 장면에서 맡는 용도·프레임 배치·현재 사용 상태와 구별하며, 몸·의복 특화 구조의 소유 범위를 보존한다.',
    'dimensions':['appearance'], 'owners':['object'],
    'property_prefixes':['object.structure','object.geometry','object.connection'],
    'core_fields':['subject','event','visual_priorities'], 'applicability':{},
    'evidence_terms':['bounded edge','part','hinge','connection','recess','strap path','부품','가장자리','힌지','연결','홈','끈 경로'],
    'includes':[
        'A declared case hinge and separately bounded disc recess; phone halves joined at their hinge.',
        'A named strap assembly with a bar and incoming/returning strap path; a generic attached textile panel with its own bounded edge.',
        'An identified fixture part and its structural joint; no claim of hidden manufacture or performance.'
    ],
    'excludes':[
        'Anatomical form, pose or continuity, including depicted anatomy whose representation ownership must remain explicit.',
        'Frame arrangement, camera viewpoint, relative prop placement or image acuity alone.',
        'Current open/closed, use, damage or readiness state without a separately evidenced structural feature.',
        'Material identity or repeated surface microstructure alone; abstract two-dimensional graphic-path geometry alone.',
        'A garment-specific construction fact already fully owned by garment_detail does not receive a duplicate generic role for that same fact. Simultaneous roles require separately evidenced properties or distinct owned components.',
        'An optional garment member/profile cannot supply unconditional garment ownership or garment type to a generic parent.'
    ],
    'neighbors':['garment_detail','anatomical_connection','prop','prop_state','prop_placement',
                 'composition','contact_point','texture','surface_material']
}
LIQUID_SPEC = {
    'id':'liquid_inclusion', 'semantic_role':'direct', 'priority':'support',
    'description':'Individually distinguishable particles, aggregates or bounded gas pockets located within an explicitly declared continuous liquid, including units at a submerged surface, with both units and liquid host grounded.',
    'description_ko':'명시된 연속 액체 내부에 있는 분리되어 보이는 입자·응집체·경계가 있는 기포와 그 배치. 잠긴 표면에 붙은 단위도 포함하되, 액체 매질과 내부 단위 각각의 근거를 요구한다.',
    'dimensions':['material'], 'owners':['entity'],
    'property_prefixes':['liquid.inclusion','liquid.suspended_structure'],
    'core_fields':['subject','setting','visual_priorities'], 'applicability':{},
    'evidence_terms':['inside liquid','underwater particles','bounded gas pockets','suspended aggregates',
                      'submerged surface bubbles','액체 내부','수중 입자','기포 경계','부유 응집체','잠긴 표면의 기포'],
    'includes':[
        'Separate suspended aggregates in a declared water column.',
        'Bounded gas pockets with the surrounding water continuing around them.',
        'Distinct illuminated particles in a declared underwater medium; small bubbles at submerged electrode surfaces.'
    ],
    'excludes':[
        'Airborne droplets or dust, unresolved fog/haze, and optical-path or image-plane artifacts.',
        'Surface foam texture without an explicit interior liquid host relation.',
        'Bubbles trapped in a declared solid ice body; a broad material-inclusion extension needs additional solid-host evidence.',
        'Liquid material, color, refraction or surface texture alone without distinct internal units.',
        'Unstated chemical identity, dissolved oxygen, reaction quantity, source cause, current, polarity, sinking speed, breathing or safety inferred from the units.'
    ],
    'neighbors':['ambient_particle','atmospheric_medium','texture','surface_material','lighting',
                 'light_shape','spatial_depth','physical_motion']
}

# Every item below is an individual judgment. Positive evidence is an exact
# manually selected pointer and quote, never a keyword-derived role assignment.
CASES = [
    (12382,'positive_generic_parent','object_structure',
     '/content/relations/0/object','조절 바; 들어가는 끈; 되돌아오는 끈',
     'declared_shoulder_or_bag_strap','object.structure.bar_incoming_returning_strap_path',
     'Parent components and relation identify the bar and the in/return path on 어깨/가방끈. The optional member is not needed to invent a scene prop function or a garment type. Preserve the parent relation and optional adoption; do not inherit all member tags.'),
    (12616,'positive_generic_parent','object_structure',
     '/content/components/0/concept_units/0','The same textile panel has a bounded crescent-shaped edge at its declared attachment.',
     'same_textile_panel','object.geometry.bounded_crescent_edge_at_declared_attachment',
     'Parent base positive text establishes the same textile panel, bounded crescent edge and declared attachment. It does not establish overlap direction, clothing type or a human wearer. Parent native wardrobe.garment_type/overlap effects are not positive semantic evidence.'),
    (7378,'conditional_member_generic_structure','object_structure',
     '/content/concept_units/2','되돌아간 끈 경로',
     'declared_shoulder_or_bag_strap','object.structure.returning_strap_path',
     'Optional member explicitly identifies a strap adjuster with a bar and return path, and its own relation names 어깨/가방끈. Evaluate only when this optional member is actually selected. Bag-strap structure does not establish a garment or wearer. Intrinsic for_any human remains a separate source-guard issue.'),
    (11105,'conditional_member_specific_garment','garment_detail',
     '/content/en','The same textile panel has a bounded crescent-shaped edge at its declared attachment.',
     'same_declared_garment_panel','garment.panel.bounded_crescent_edge',
     'This member has positive Korean 같은 의상 표면 and a selected-owner context. If this member is explicitly selected, garment_detail may express its panel geometry. Do not move that optional member ownership to parent12616 base, invent a named garment type, or duplicate this same fact under object_structure.'),
    (15049,'conditional_profile_specific_garment','garment_detail',
     '/content/concept_candidate/concept_terms/0','같은 의상 표면의 별도 패널 가장자리 · 초승달 패널',
     'same_declared_garment_panel','garment.panel.crescent_edge',
     'Associated profile has its own positive garment phrase and exact component/evidence obligations. It is independent-request-evidence only and is not mandatory in parent12616. Profile semantics require the complete selected owner/edge relation; no union of optional parent/member/profile roles.'),
    (4555,'positive_object_additional','object_structure',
     '/content/en','a transparent rectangular rigid case has a hinge and a separate circular disc recess',
     'rigid_case','object.structure.hinge_and_separate_circular_disc_recess',
     'Case-owned geometry, joint and recess are concrete. Transparent material can have separate support; geometry alone does not declare scene use. Empty native effects require later native review, not a fabricated prop purpose.'),
    (5432,'positive_object_additional','object_structure',
     '/content/en','two rigid phone halves connect at a hinge; the upper half has a small screen and the lower half has separate physical keys',
     'declared_phone','object.structure.hinged_halves_upper_screen_lower_keys',
     'Object-internal halves/hinge/screen/key topology remains true across primary subject category and frame placement. No need to relabel this intrinsic topology as prop_state or whole-frame composition. Empty native effects remain separately unqualified.'),
    (6616,'positive_object_additional_with_state_boundary','object_structure',
     '/content/en','a timber bridge deck raised partway about a hinge at the gate threshold, leaving a gap over the ditch',
     'declared_bridge_deck','object.connection.hinge_at_gate_threshold',
     'The bridge deck/hinge connection is a structural subfact in the complete phrase. Raised partway and the gap are present-state and spatial subfacts, not stable structure by themselves. Only the hinge connection is proposed for the new role; location/state roles require separate review.'),
    (10133,'positive_liquid_seed','liquid_inclusion',
     '/content/en','irregular pale suspended aggregates; separation between particle sizes; a coherent deep water background',
     'declared_water_column','liquid.suspended_structure.separate_pale_aggregates',
     'Parent relation explicitly suspends particle_aggregates in water_column. Not airborne snow, all bubbles or optical noise. Do not infer settling rate or organic composition.'),
    (10187,'positive_liquid_seed','liquid_inclusion',
     '/content/en','bounded gas pockets inside the water; bright curved rims; water and background continuing around the pockets',
     'declared_water_body','liquid.inclusion.bounded_gas_pockets_with_water_continuity',
     'Both bounded units and continuous water host are explicit. This is gas in liquid, not liquid droplets in air; oxygen content, breathing and bioluminescence are unsupported.'),
    (10883,'positive_liquid_additional','liquid_inclusion',
     '/content/en','small bright particles within the camera lighting path; foreground scatter over a more distant subject; a coherent underwater medium',
     'declared_underwater_medium','liquid.inclusion.illuminated_foreground_particles',
     'The full phrase and relation identify real foreground particles illuminated by camera light within underwater medium. Do not equate the particles with lens-only flare, marine-snow identity, bubbles or acoustic sonar. Camera/light relations are separate from the inclusion fact.'),
    (11832,'positive_liquid_additional','liquid_inclusion',
     '/content/en','two distinct electrodes enter the same liquid vessel; small gas bubbles cluster at their submerged surfaces; separate leads connect each electrode to one supply',
     'same_declared_liquid','liquid.inclusion.gas_bubbles_at_submerged_electrode_surfaces',
     'A benchtop liquid apparatus supplies a second setting beyond open-water ecology. Submerged-surface bubbles count even when not freely drifting. Preserve electrodes/leads separately; no gas identity, liquid chemistry, current/polarity or reaction yield is inferred.'),
    (10001,'negative_liquid_interior_surface_texture',None,
     '/content/en','many small bubbles packed into a patch; irregular foam edges; liquid visible beside the foam patch',None,None,
     'Surface foam patch and its edge are supported as texture. Liquid beside a patch and floats_on water_surface do not establish units inside a continuous liquid volume. Do not force every occurrence of bubbles into liquid_inclusion.'),
    (1741,'insufficient_host_relation_for_liquid_role',None,
     '/content/en','water refraction and tiny bubbles',None,None,
     'Names water/refraction/bubbles but does not resolve their interior host relation or boundary distribution. Conditions are contextual guards, not missing geometry. Keep a candidate-specific host clarification need rather than automatically tagging the new role.'),
    (915,'negative_object_frame_arrangement',None,
     '/content/en','top-down social flat-lay composition',None,None,
     'A frame/camera arrangement; no owned object-internal part geometry. Product/food tags do not identify a garment or any structural carrier.'),
    (9733,'negative_object_anatomy',None,
     '/content/en','four fingers fold into the palm; thumb remains visibly assigned outside or beside the folded digits; wrist continues to one forearm',None,None,
     'Owned hand pose and anatomical continuity remain anatomy/pose. A generic physical-object structure role must not absorb body geometry.'),
    (8176,'specific_garment_and_texture_boundary',None,
     '/content/en','interlocking metal rings forming a flexible mail mesh',None,None,
     'The positive relation identifies armour with visible construction. Garment-specific construction and repeated mesh texture can be assessed separately. Do not add a duplicate generic structure role solely for the very same ring-mesh fact.'),
    (10119,'negative_object_graphic_geometry',None,
     '/content/concept_units/0','the artwork line has two visibly separated endpoints',None,None,
     'Drawn path geometry is owned by a displayed artwork, not physical-object part topology. A possible separate graphic geometry taxonomy review is outside these two new-role proposals; do not stretch object_structure or whole-frame composition to hide it.'),
    (10423,'negative_liquid_air_medium',None,
     '/content/en','a low suspended haze near the ground or water; distant objects losing contrast; nearer edges remaining more legible',None,None,
     'Fog/haze layer in air, including near water, is atmospheric_medium. Near water does not mean inside water and unresolved attenuation does not establish distinguishable liquid inclusions. Existing immutable amendment2 handles its role correction.'),
    (10274,'negative_liquid_airborne_droplets',None,
     '/content/en','airborne droplets near a visible collision zone; a coherent spray fan; the same wave or outlet continuing into that zone',None,None,
     'The host is air and the units are liquid droplets. ambient_particle is appropriate to this property; reversing carrier and dispersed unit would corrupt meaning.'),
    (11467,'not_a_positive_nonhuman_garment_product',None,
     '/content/en','rigid mannequins repeat a shared pose; one adult figure among them has distinct skin and garment response',None,None,
     'Garment response is attached to the one adult figure, while mannequins are only stated to repeat a pose. This does not establish a garment construction on a mannequin or a nonhuman wearer.'),
    (5640,'garment_positive_but_not_standalone_product_proof',None,
     '/content/en','a tailored opaque garment with structurally placed sheer textile panels',None,None,
     'Actual garment construction is explicit, but no standalone product/nonhuman wearer is explicit; intrinsic human/adult conditions and adult embedding wording remain. An absent wearer in the short English phrase is not positive proof of an unworn garment product. Retain prior9 proposal scope and defer extra category removal.'),
    (1122,'negative_object_surface_texture',None,
     '/content/en','an open book page with visible paper grain',None,None,
     'Visible paper grain is surface organization, not a part-joint or contour geometry fact. The book object does not make every surface property object_structure.'),
    (1430,'negative_object_placement_and_garment_hypothesis',None,
     '/content/en','displayed neatly on a table',None,None,
     'Only table placement is stated. No item identity, garment construction or structure is provided; product/food guards cannot supply an absent garment.'),
    (10730,'negative_liquid_solid_host_optional_variant',None,
     '/content/en','a shaped continuous ice body; trapped bubbles or surface frost only in the chosen variant; melt droplets joined to its lower edges',None,None,
     'Trapped bubbles belong to a solid ice host and are optional against frost. Do not union those variants or call ice a liquid host; do not treat melt droplets at an exterior edge as interior units. A broad material_inclusion role remains deferred because this one optional solid-host example does not establish that extension sufficiently.'),
    (10376,'negative_liquid_optical_path',None,
     '/content/paraphrases/1','one declared bright source entering the camera path; a luminous veil across the captured image toward that source; reduced contrast in detail behind the veil',None,None,
     'Optical-path captured-image veiling flare is lens_artifact, not physical particles or liquid host inclusions. Existing immutable amendment2 handles its role correction.')
]

def rawsha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    out=R/'authored'/(NAME+'.json');note_path=R/'worker-notes'/(NAME+'.json')
    assert not out.exists() and not note_path.exists(), 'immutable extension already exists'
    protected = {
        'authored/catalog-applicability-proposals-review_09250_10500.json':'6aa9851638cb5c7609bee4f7fa4f23d82e3b3e2eaee19ef9d996400f65b5e825',
        'authored/review_09250_10500_amend_optical_medium_2.json':'cb5c4fbc2b61e5a5b3548ebe459215d878fc517fca63e06229371baf6686697a',
        'authored/review_09250_10500_10250_10500.json':'5fd00568685c48afac6b9c38698db7c2b1c2d11b4136a41afe1a03cbb43031e0'
    }
    for path,sha in protected.items(): assert rawsha(R/path)==sha, path
    data=dr.source();order=json.loads((R/'ORDER.json').read_text());bycid={cid:n for n,cid in enumerate(order)}
    assert dr.c.digest(data)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
    read_records={}
    for ordinal in ROOT_READS:
        cid=order[ordinal];read_records[cid]=data['candidates'][cid]
        read_records.update(dr.closure(data,cid))
    assert {order[c[0]] for c in CASES}==set(read_records)
    assert len(ROOT_READS)==23 and len(read_records)==26 and len(SPEC_READS)==21
    proposed_catalog=copy.deepcopy(data['slot_catalog'])
    for spec in [OBJECT_SPEC,LIQUID_SPEC]:
        assert spec['id'] not in proposed_catalog
        proposed_catalog[spec['id']]=spec
    findings=[]
    for n,verdict,role,path,quote,target,prop,reason in CASES:
        cid=order[n];record=read_records[cid]
        assert dr.pointer(record,path,positive=True)==quote,(n,path)
        item=dict(ordinal=n,candidate_id=cid,record_kind=record['record_kind'],actual_realization_ids=ids(record),
            directly_read_complete=True,meaning_and_boundary_judgment=reason,verdict=verdict,
            primary_positive_field=dict(pointer=path,quote=quote),
            source_binding=dr.binding(data,cid),root_revisit_required_before_any_tag_or_native_change=True)
        if role:
            fact=dict(pointer=path,quote=quote,dimension='material' if role=='liquid_inclusion' else 'appearance',
                      target=target,property=prop)
            dr.validate_fact(fact,record,proposed_catalog,role,realization_id='base')
            item['candidate_specific_role_proposal']=dict(slot_id=role,realization_id='base',
                fact=fact,activation='only_when_this_record_and_its_own_required_relation_are_explicitly_selected',
                status='advisory_semantic_fact_not_a_registered_whole_candidate_decision')
        findings.append(item)
    changes=[]
    for spec,positives,negatives in [
        (OBJECT_SPEC,[12382,12616,4555,5432,6616],[915,9733,10119,1122,1430,8176]),
        (LIQUID_SPEC,[10133,10187,10883,11832],[10001,10423,10274,10730,10376,1741])]:
        changes.append(dict(pointer='/slot_catalog/'+spec['id'],before=None,after=spec,
            change_type='proposed_new_semantic_role_only_not_applied',
            positive_ordinals=positives,negative_or_boundary_ordinals=negatives,
            query_scope_en=spec['description'],query_scope_ko=spec['description_ko'],
            carrier_contract=(
                'Every fact target must name an already grounded non-anatomical physical object/fixture and, where relevant, its own parts/endpoints. New slot selection does not create an object, person, garment or body. More specific anatomy/garment roles retain ownership; simultaneous tags need independent facts.'
                if spec['id']=='object_structure' else
                'Every fact must ground both a named continuous liquid host and distinguishable interior units. Host may be an environmental water body or an owned vessel liquid; primary subject human is not required. Neither a vessel alone nor a water tag grounds liquid or units. Preserve declared carrier targets and any source guards.'),
            native_followup='Reopen each affected record/selected realization, bind new catalog spec hash, and author exact source-supported native effects/carriers before qualification. No rehash-only approval, empty-binding guard bypass or automatic tag migration.'))
    result=dict(schema='photo-codex-catalog-taxonomy-extension-proposals/v1',task_name=TASK,
        model='gpt-6.1-sol',reasoning_effort='high',status='final_ready_frozen_proposals_only',
        source_sha256=dr.c.digest(data),catalog_sha256=dr.c.digest(data['slot_catalog']),
        original_catalog_count=139,prior_fullspec_direct_read_count=139,
        prior_fullspec_evidence='worker-notes/catalog-applicability-review-review_09250_10500.json',
        this_extension_fullspec_reread_count=21,this_extension_fullspec_reread_ids=SPEC_READS,
        directly_read_root_record_count=23,directly_read_unique_record_count_including_closure=26,
        complete_source_read_for_declared_review_inputs=True,
        review_method='individual_complete_source_and_full_required_closure_read_plus_manual_role_boundary_comparison',
        scope_limits=['Only these two new-role proposals and their individual case findings are authored; no source/catalog/native/global/Git changes or registration.',
            'Source parsing and case-insensitive literal searches were discovery only. No semantic classifier, regex tag assignment, quota or search-score objective was used.',
            'Candidate-specific role proposals describe selected owned facts, not complete new whole-candidate approvals; no automatic member/profile role union.',
            'Standalone garment/product and nonhuman garment hypotheses are not established by the actually read frozen examples; no further garment_detail category removal is proposed.'],
        exact_catalog_changes=changes,candidate_findings=findings,
        optional_parent_member_profile_separation={
            '12382':'Parent has its own bar/incoming/returning-strap relation. The optional member7378 can be evaluated on selection; its source guard and old garment provenance do not author a parent garment type.',
            '12616':'Parent base is generic same textile panel/crescent bounded edge/declared attachment. Optional member11105 and associated profile15049 have their own garment-positive wording only in those selected cases. optional adoption + requirements{} + independent_request_evidence_only do not impose those owners on parent.',
            'non_evidence':'Parent effects wardrobe.garment_type and wardrobe.panels.overlap do not prove a garment type or overlap direction in its positive content.',
            'implementation_direction_only':'If canonical authoring later represents a generic base plus an explicitly selected garment-specific case, keep the guards, exact complete relation and source ownership separate. This report creates no branch or source rewrite.'},
        alternatives_compared=[
            {'choice':'Reuse composition','decision':'reject_for_object_structure','reason':'Existing fullspec owns frame arrangement/negative space, not object-internal hinge/part/edge geometry.'},
            {'choice':'Reuse prop or prop_state','decision':'reject_as_geometry_fallback','reason':'Declared scene role/current use attachment/readiness is independent of stable part geometry. Structural joint and current secured/open state can coexist only with separate facts.'},
            {'choice':'Reuse body_form/silhouette_proportion/anatomical_connection','decision':'reject_for_nonanatomical_object','reason':'Anatomy and clothed body silhouette are not generic physical-object topology.'},
            {'choice':'Reuse garment_detail universally','decision':'reject_for_generic_parent','reason':'Garment ownership must be positive and selected. Hardware, case and bridge parts do not become garments; a generic textile panel is not automatically a named garment.'},
            {'choice':'Separate object_shape and object_connection slots','decision':'defer_split','reason':'Five directly read positive parent/object examples share one object-owned parts/boundaries/connection axis. A split would add distinction without demonstrated retrieval/semantic need; proposed property prefixes retain subtypes.'},
            {'choice':'Widen ambient_particle to all media','decision':'reject_here','reason':'Its actual definition and air.particles prefixes are airborne. Gas pockets in water reverse the continuous host and dispersed unit relative to droplets in air; blanket widening would obscure that boundary.'},
            {'choice':'Separate underwater_particle and underwater_bubble','decision':'prefer_one_liquid_inclusion_role','reason':'Both require distinguishable units inside an explicit continuous liquid. Properties preserve particle/aggregate/gas-pocket subtypes, while electrochemical liquid apparatus demonstrates applicability beyond underwater scenery.'},
            {'choice':'General material_inclusion including solids','decision':'defer','reason':'10730 supplies only one conditional solid-ice example with bubbles versus frost. More independently read solid-host positive and negative sources are needed before broadening; this proposal deliberately excludes solids.'},
            {'choice':'Use texture for every bubble or aggregate','decision':'reject_for_liquid_interior','reason':'Texture owns physical surface organization. Surface foam10001 fits that scope; particles and bounded gas pockets in liquid volume require a host-interior relation.'},
            {'choice':'Remove garment_detail human primary category now','decision':'defer_additional_change','reason':'Object-owned general definition makes the restriction questionable, but this extension did not establish explicit frozen standalone garment-product or nonhuman garment-construction positives. 5640,11467,1430,915 are not such evidence. Existing prior9 proposal remains frozen.'}
        ],
        impact_revisit_list=[dict(ordinal=f['ordinal'],candidate_id=f['candidate_id'],
            reason=f['meaning_and_boundary_judgment'],source_binding=f['source_binding'],
            action='manual_fullsource_selected_realization_and_qualification_revisit_before_any_change',
            automatic_tagging_authorized=False) for f in findings if f.get('candidate_specific_role_proposal')],
        discovery_limits={
            'standalone_garment':'Literal English/Korean short-field discovery followed by full-content discovery for explicit hanger/standalone product/nonhuman-wearing phrases returned no established positive. This is a finite discovery result, not proof that the whole corpus contains no such meaning.',
            'liquid_units':'Names/tags/effects alone were not used to decide. Full host/units/boundary/context/claim-limit fields were read in each declared review input.',
            'catalog':'139 original fullspecs were read in the frozen prior report. This extension actually reread21 relevant fullspecs, not a new claimed139 reread.'},
        read_input_bindings=[dict(ordinal=bycid[cid],candidate_id=cid,record_kind=rec['record_kind'],
            actual_realization_ids=ids(rec),source_record_sha256=dr.c.digest(rec),
            reference_sha256={k:dr.c.digest(v) for k,v in dr.closure(data,cid).items()})
            for cid,rec in sorted(read_records.items(),key=lambda kv:bycid[kv[0]])],
        complete_read_input_records=read_records,
        reread_fullspecs={key:data['slot_catalog'][key] for key in SPEC_READS},
        frozen_previous_artifacts_raw_sha256=protected,
        validation={'exact_positive_pointer_quotes':'passed26_of26',
            'candidate_specific_fact_contracts_on_in_memory_proposed_catalog':'passed12_of12',
            'source_and_closure_records_bound':'passed26_records',
            'production_catalog_or_native_qualification':'not_applied_not_certified'})
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    note=dict(schema='photo-codex-catalog-taxonomy-extension-worker-note/v1',task_name=TASK,agent_id=TASK,
        model='gpt-6.1-sol',reasoning_effort='high',status='final_ready_frozen_proposals_only',
        final_ready=True,complete_source_read=True,original_catalog_count=139,
        prior_fullspec_direct_read_count=139,this_extension_fullspec_reread_count=21,
        directly_read_root_record_count=23,directly_read_unique_record_count_including_closure=26,
        directly_read_ordinals=sorted(c[0] for c in CASES),
        source_sha256=dr.c.digest(data),catalog_sha256=dr.c.digest(data['slot_catalog']),
        read_input_records_sha256=dr.c.digest(read_records),new_role_proposal_count=2,
        new_role_ids=['object_structure','liquid_inclusion'],
        authored_paths=[str(out.relative_to(R)),str(Path(__file__).relative_to(R))],
        authored_file_sha256={str(out.relative_to(R)):rawsha(out),str(Path(__file__).relative_to(R)):rawsha(Path(__file__))},
        inherited_or_optional_member_roles_automatically_unioned=False,
        no_registration_or_source_catalog_global_code_git_mutation=True,
        no_model_network_or_embedding_calls=True,unresolved_items=[
            'No automatic candidate tag application: root must separately review fullsource/selected ownership/native effects and fresh spec hashes.',
            '1741 needs explicit host-boundary clarification before liquid_inclusion can be approved.',
            'Broader solid material inclusions, graphic-path geometry and garment_detail primary-category removal remain deferred with stated evidence limits.'
        ],
        protected_frozen_artifacts_raw_sha256=protected,
        validation=result['validation'])
    note_path.write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
    for path,sha in protected.items():assert rawsha(R/path)==sha,path
    print(json.dumps({'authored':str(out.relative_to(R)),'authored_raw_sha256':rawsha(out),
        'worker_note':str(note_path.relative_to(R)),'worker_note_raw_sha256':rawsha(note_path),
        'unique_records_directly_read':26,'fullspecs_reread':21,'new_role_proposals':2},ensure_ascii=False))

if __name__=='__main__':
    main()
