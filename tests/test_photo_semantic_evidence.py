"""Native v4 source fixtures: declared facts are not mutation permissions."""
import copy
import json
import unittest
from tests.test_photo_candidate_corpus import fixture, A
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_global_index as index
import photo_role_proposals as roles
import photo_search_layout as layout
import photo_semantic_evidence as e
import photo_slot_semantics as semantics
import prompt_generator as g
from photo_contracts import property_effects_allowed


def fact(fid, dimension, target, prop, mode, value, requires, *, rid='base', quote=None,
         operation=None, receivers=None, pointer='/content/en'):
    row={'id':fid,'realization_id':rid,'pointer':pointer,'quote':quote,
         'dimension':dimension,'target':target,'property':prop,'mode':mode,
         'value':{'type':prop+'/v1','value':value},'requires':requires}
    if mode=='effect':row.update(operation=operation,receivers=receivers)
    return row


def source(text, facts, specs, bindings, *, effects=None, correction=None):
    data=fixture();data['slot_bindings'].clear();data['slot_catalog']=specs
    record=data['candidates'][A];record['content']={'en':text}
    if effects is None:
        rows=[{key:f[key] for key in e.PROPERTY_FIELDS} for f in facts if f['mode']=='effect']
        effects={'dimensions':sorted({row['dimension'] for row in rows}),'properties':rows}
    record['effects']=effects
    for f in facts:
        if f['quote'] is None:f['quote']=text
    proof={'schema':e.SCHEMA,'meaning_sha256':e.meaning_sha256(record),'catalog_sha256':c.digest(specs),
        'complete':True,'facts':facts,'roles':{},'owner_maps':bindings,'effect_sets':{},'source_units':[],
        'dependencies':{},'reference_sha256':{},'guard_sets':{},'profile_contracts':{},
        'review':{'basis':'manually reviewed native fixture','whole_source_reviewed':True,'source_correction':correction,
            'original_review':{'candidate_id':record['id'],'source_record_sha256':'a'*64,
                'catalog_sha256':c.digest(specs),'decision_sha256':'b'*64,'artifact':'fixture/explicit-original-review.json'},
            'native_review':{'reviewer':'Codex native fixture author','method':'codex_direct_source_read',
                'native_contract_sha256':'pending'}}}
    record['content']['role_evidence']=proof
    return data


def owner_map(*owners):
    return {'schema':e.OWNER_SCHEMA,'bindings':[{'target':left,'core_role':right,'origin':'existing',
        'introduced_by':None} for left,right in owners]}


def trust_fixture_authority(data):
    """Explicit test-author trust act, distinct from structural validation.

    Fixture signatures/meaning are synthetic. Invalid adversarial structures
    receive no capability; production validators never issue authority.
    """
    try:
        e.permission_envelope.freeze_source_authority(data,expected_snapshot_sha256=c.digest(data),
            reviewer='explicit independently authored synthetic fixture source')
    except (ValueError,KeyError,TypeError,IndexError):
        pass  # Invalid fixture remains untrusted for its negative test.


def seal(data, support, *, cid=A):
    """Only fixture serialization; fact modes/values/owners are explicitly authored above."""
    record=data['candidates'][cid];proof=record['content']['role_evidence']
    proof['meaning_sha256']=e.meaning_sha256(record);proof['catalog_sha256']=c.digest(data['slot_catalog'])
    proof['effect_sets']={rid:e.effect_set(record,rid) for rid in r.ids(record)}
    proof['dependencies']={rid:proof['dependencies'].get(rid,[]) for rid in r.ids(record)}
    proof['reference_sha256']=e.referenced_records(record,data)
    proof['guard_sets']={rid:e.source_guard_set(record,rid,data) for rid in r.ids(record)}
    proof['profile_contracts']={rid:r.profile_contract(record,rid) for rid in r.ids(record)}
    proof['source_units']=[]
    for rid in r.ids(record):
        for pointer in sorted(e.primary_paths(record,rid)|{f['pointer'] for f in proof['facts'] if f['realization_id']==rid}):
            refs=[f['id'] for f in proof['facts'] if f['realization_id']==rid and f['pointer']==pointer]
            proof['source_units'].append({'realization_id':rid,'pointer':pointer,
                'quote':e.positive_string(record,pointer,realization_id=rid),'fact_refs':refs,
                'disposition':'semantic' if refs else 'nonsemantic'})
    for tag,refs in support.items():
        selected=[f for f in proof['facts'] if f['id'] in refs]
        ids=sorted({f['realization_id'] for f in selected})
        proof['roles'][tag]={'spec_sha256':c.digest(data['slot_catalog'][tag]),
            'scope':'whole_record' if set(ids)==set(r.ids(record)) else 'positive_alternative',
            'realization_ids':ids,'fact_refs':refs,'support_modes':sorted({f['mode'] for f in selected})}
    if proof['review']['source_correction'] is not None:
        proof['review']['source_correction']['after_sha256']=proof['meaning_sha256']
    proof['review']['original_review']['candidate_id']=record['id']
    proof['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(proof)
    trust_fixture_authority(data)
    return data


def reattest(data, cid=A):
    """A fresh fixture review signature lets structural adversaries reach the intended check."""
    proof=data['candidates'][cid]['content']['role_evidence']
    proof['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(proof)


def assertion(aid, kind, **axes):
    dim=axes.pop('dimension','subject')
    return {'assertion_id':aid,'dimension':dim,'polarity':'required','source_span_ids':['request_1'],
            'axes':{'native_schema':e.witnesses.SCHEMA,'kind':kind,**axes},
            'evidence':{'meaning':'An explicitly declared subject and photograph'},'affected_dimensions':[dim]}


def core(owners, values=(), edges=(), *, role_bindings=None, open_dimensions=('material','lighting','pose','appearance','action','composition','camera')):
    text='An explicitly declared subject and photograph'
    rows=[assertion('owner_'+str(i),'owner',owner=owner,owner_kind='entity') for i,owner in enumerate(owners)]
    # Explicit fixture declarations, never a production naming/semantic heuristic.
    defaults={'main_subject':'main_subject','actor_A':'main_subject','actor_B':'secondary_subject',
        'face_A':'primary_face','face_B':'secondary_face','image_A':'image','scene_A':'scene',
        'garment_A':'primary_garment'}
    bindings = role_bindings if role_bindings is not None else {defaults[owner]:owner for owner in owners if owner in defaults}
    rows += [assertion('role_'+str(i),'role',role=role,owner=owner) for i,(role,owner) in enumerate(bindings.items())]
    for i,(dim,owner,prop,value) in enumerate(values):
        rows.append(assertion('value_'+str(i),'fact',dimension=dim,owner=owner,property=prop,
            value_type=prop+'/v1',value=value))
    for i,(kind,left,right) in enumerate(edges):
        rows.append(assertion('edge_'+str(i),kind,left=left,right=right))
    locked={'concept','subject','identity','count','age','event'}|{row['dimension'] for row in rows}
    return {'contract_version':'photo-authorial-core/v3','subject':text,'baseline_prompt_en':text,
        'request_binding':{'active_spans':[{'source_span_id':'request_1','text':text}]},
        'semantic_assertions':rows,'user_exclusions':[],
        'intent_lock':{'contract_version':'photo-intent-lock/v2','locked_dimensions':sorted(locked),
            'open_dimensions':[dim for dim in open_dimensions if dim not in locked],'semantic_anchors':[]}}


def reviewed_source():
    row=fact('satin','material','main_subject','surface.material','effect','satin',[],operation='set_value',receivers=[])
    return seal(source('a satin garment surface',[row],
        {tag:slot(tag,['material'],property_prefixes=[path]) for tag,path in
         [('surface_material','surface.material'),('texture','surface.texture')]},
        {'base':owner_map(('main_subject','main_subject'))}),{'surface_material':['satin']})


def face_source():
    rows=[fact('face','subject','face_surface','anatomy.face.presence','prerequisite','present',[],quote='face'),
          fact('underlight','lighting','face_surface','lighting.direction','effect','below',['face'],
               operation='set_value',receivers=[],quote='underlit face')]
    return seal(source('underlit face',rows,{'light_direction':slot('light_direction',['lighting'],
        property_prefixes=['lighting.direction'])},{'base':owner_map(('face_surface','primary_face'))}),
        {'light_direction':['underlight']})


class SemanticEvidenceTests(unittest.TestCase):
    def assert_valid(self,data):c.validate(data)
    def allowed(self,data,frozen,rid='base'):
        try:return e.existing_owner_allowed(c.entry(data,A,realization_id=rid),frozen,{},data['slot_catalog'])
        except ValueError:return False
    def views(self,data):
        return [data,{**data,'candidates':{A:layout.guard_record(data['candidates'][A],data)}}]

    def test_explicit_invalid_or_v2_evidence_never_reactivates_fallback(self):
        for invalid in [None,{},False,{'schema':'photo-candidate-role-evidence/v2','complete':True}]:
            data=reviewed_source();record=data['candidates'][A];record['content']['role_evidence']=invalid
            with self.subTest(invalid=invalid):
                self.assertRaises(ValueError,c.validate,data)
                self.assertEqual(e.qualification(data['slot_catalog']['surface_material'],record)['native_qualification'],'invalid')
                self.assertFalse(e.admission(c.entry(data,A),{})['allowed'])
                self.assertFalse(e.admission({'_semantic_evidence_guard':invalid,'role_evidence':{}},{})['allowed'])

    def test_absent_proof_is_explicit_unqualified_search_only_not_eligible_native_fit(self):
        data=reviewed_source();data['candidates'][A]['content'].pop('role_evidence');c.validate(data)
        fit=semantics.fit(data['slot_catalog']['surface_material'],data['candidates'][A],'satin surface')
        self.assertEqual(fit['status'],'review_required');self.assertEqual(fit['native_qualification'],'unqualified')
        self.assertTrue(e.admission(c.entry(data,A),{})['allowed'])
        self.assertEqual(c.entry(data,A)['_native_qualification'],'unqualified')

    def test_native_source_and_spec_hashes_bind_complete_facts(self):
        for field in ['body','effects','conditions','spec']:
            data=reviewed_source();record=data['candidates'][A]
            if field=='body':record['content']['en']='plastic surface'
            elif field=='effects':record['effects']['properties'][0]['target']='background'
            elif field=='conditions':record['conditions']={'for_any':['human']}
            else:data['slot_catalog']['surface_material']['description']+=' changed'
            with self.subTest(field=field):self.assertRaises(ValueError,c.validate,data)

    def test_native_role_discovery_preserves_separate_effects_and_modes(self):
        data=reviewed_source();c.validate(data);proposal=roles.propose(data,'surface_material',A,[])
        self.assertEqual(proposal['schema'],'photo-request-role-proposal/v4')
        self.assertEqual(proposal['native_qualification'],'qualified');self.assertEqual(proposal['applicability_status'],'eligible')
        self.assertEqual(proposal['semantic_fit']['support_modes'],['effect'])
        self.assertEqual(proposal['effects'],data['candidates'][A]['effects'])
        self.assertEqual(roles.validate(data,proposal,[])['_native_qualification'],'qualified')

    def test_unreviewed_role_is_incompatible_despite_similar_words(self):
        data=reviewed_source()
        self.assertEqual(semantics.fit(data['slot_catalog']['texture'],data['candidates'][A],
            'satin texture surface weave')['status'],'incompatible')

    def test_metadata_does_not_change_search_or_embedding_projection(self):
        data=reviewed_source();record=data['candidates'][A];plain=copy.deepcopy(record);plain['content'].pop('role_evidence')
        self.assertEqual(index.fields(record),index.fields(plain));self.assertEqual(index.text(record),index.text(plain))

    def test_negative_routing_review_and_claim_limits_never_supply_positive_quotes(self):
        for key in sorted(e.NEGATIVE):
            data=reviewed_source();record=data['candidates'][A]
            if key=='role_evidence':continue
            record['content'][key]=['a satin garment surface']
            proof=record['content']['role_evidence'];proof['meaning_sha256']=e.meaning_sha256(record)
            proof['facts'][0]['pointer']='/content/'+key+'/0'
            reattest(data)
            with self.subTest(key=key):self.assertRaises(ValueError,c.validate,data)

    def test_wrong_quote_property_target_and_foreign_rid_rejected(self):
        for key,value in [('quote','invented'),('property','surface.texture'),('target','background'),('realization_id','foreign')]:
            data=reviewed_source();data['candidates'][A]['content']['role_evidence']['facts'][0][key]=value
            reattest(data)
            with self.subTest(key=key):self.assertRaises(ValueError,c.validate,data)

    def test_source_unit_and_every_fact_need_explicit_disposition(self):
        for defect in ['no_units','no_fact_refs','duplicate_unit','orphan_fact','no_mode','no_value','no_requires','no_operation','no_receivers']:
            data=reviewed_source();p=data['candidates'][A]['content']['role_evidence']
            if defect=='no_units':p['source_units']=[]
            elif defect=='no_fact_refs':p['source_units'][0]['fact_refs']=[]
            elif defect=='duplicate_unit':p['source_units'].append(copy.deepcopy(p['source_units'][0]))
            elif defect=='orphan_fact':p['roles']['surface_material']['fact_refs']=['foreign']
            else:p['facts'][0].pop(defect.removeprefix('no_'))
            reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)

    def test_compact_retains_whole_inventory_and_matches_full_role_and_admission(self):
        data=reviewed_source();c.validate(data);record=data['candidates'][A];guard=layout.guard_record(record,data)
        self.assertNotIn('quote',guard['_semantic_evidence_guard']['facts'][0])
        self.assertNotIn('source_units',guard['_semantic_evidence_guard'])
        self.assertEqual(e.qualification(data['slot_catalog']['surface_material'],record),
                         e.qualification(data['slot_catalog']['surface_material'],guard))
        for view in self.views(data):self.assertTrue(self.allowed(view,core(['main_subject'])))

    def test_face_light_requires_exact_frozen_face_fact_not_category_or_keyword(self):
        data=face_source();c.validate(data)
        for label in ['teacup','human','animal','wig','painted doll','robot','portrait Alice']:
            frozen=core(['face_A']);frozen['subject']=label
            with self.subTest(label=label):self.assertFalse(self.allowed(data,frozen))
        frozen=core(['face_A'],[('subject','face_A','anatomy.face.presence','present')])
        for view in self.views(data):self.assertTrue(self.allowed(view,frozen))

    def test_secondary_face_owner_and_typed_values_are_not_interchangeable(self):
        data=face_source()
        for owner,value,allowed in [('face_A','present',True),('face_B','present',False),('face_A','absent',False)]:
            frozen=core(['face_A','face_B'],[('subject',owner,'anatomy.face.presence',value)])
            self.assertEqual(self.allowed(data,frozen),allowed)
        data['candidates'][A]['content']['role_evidence']['facts'][0]['value']={'type':'generic_carrier/v1','value':'face'}
        self.assertFalse(self.allowed(data,core(['face_A'],[('subject','face_A','anatomy.face.presence','present')])))

    def test_age_prerequisite_does_not_require_age_mutation_permission(self):
        rows=[fact('adult','age','main_subject','age.declared','prerequisite','adult',[],quote='adult'),
              fact('skirt','appearance','main_subject','wardrobe.ensemble','effect','pencil_skirt',['adult'],
                   operation='set_value',receivers=[],quote='pencil skirt')]
        data=seal(source('adult wearing a pencil skirt',rows,
            {'age_presentation':slot('age_presentation',['age'],property_prefixes=['age.declared'])},
            {'base':owner_map(('main_subject','main_subject'))}),{'age_presentation':['adult']});c.validate(data)
        frozen=core(['actor_A'],[('age','actor_A','age.declared','adult')]);self.assertNotIn('age',frozen['intent_lock']['open_dimensions'])
        self.assertTrue(self.allowed(data,frozen));proposal=roles.propose(data,'age_presentation',A,[])
        self.assertEqual(proposal['semantic_fit']['support_modes'],['prerequisite'])
        self.assertEqual(proposal['effects']['dimensions'],['appearance'])
        for value in ['minor','unknown']:
            self.assertFalse(self.allowed(data,core(['actor_A'],[('age','actor_A','age.declared',value)])))
        self.assertFalse(self.allowed(data,core(['actor_A','actor_B'],[('age','actor_B','age.declared','adult')])))
        frozen['intent_lock']['open_dimensions'].remove('appearance')
        self.assertFalse(g.core_entry_eligible(data,frozen,{'subject_category':'human'}, {'subject':{}},'',c.entry(data,A)))

    def test_canonical_effect_cannot_be_waived_by_relabeling_it_prerequisite(self):
        data=reviewed_source();p=data['candidates'][A]['content']['role_evidence'];f=p['facts'][0]
        f['mode']='prerequisite';f.pop('operation');f.pop('receivers');p['roles']['surface_material']['support_modes']=['prerequisite']
        reattest(data);self.assertRaises(ValueError,c.validate,data)
        self.assertRaises(ValueError,layout.guard_record,data['candidates'][A],data)
        self.assertFalse(self.allowed(data,core(['main_subject'],[('material','main_subject','surface.material','satin')])))

    def test_preservation_binds_exact_frozen_value_but_does_not_select_new_focus(self):
        row=fact('keep_focus','camera','image','focus.plane','preservation','same',[])
        row['value']={'type':'frozen_property_reference/v1','value':'same'}
        data=seal(source('maintaining the same focus relationship',[row],
            {'focus':slot('focus',['camera'],property_prefixes=['focus.'])},
            {'base':owner_map(('image','image'))}),{'focus':['keep_focus']});c.validate(data)
        frozen=core(['image_A'],[('camera','image_A','focus.plane','eyes')])
        for view in self.views(data):
            result=e.admission(c.entry(view,A),frozen);self.assertTrue(result['allowed'])
            self.assertEqual(result['resolved_frozen_facts'][0]['value']['value'],'eyes')
        self.assertFalse(self.allowed(data,core(['image_A'])))
        new=copy.deepcopy(data);new['candidates'][A]['effects']={'dimensions':['camera'],'properties':[
            {'dimension':'camera','target':'image','property':'focus.plane'}]}
        self.assertRaises(ValueError,c.validate,new)

    def test_unrendered_context_is_not_a_mutation_or_missing_prerequisite_escape(self):
        row=fact('context','setting','scene','world.ordinary_usage','context','office_clothing',[])
        data=seal(source('ordinary office clothing context',[row],{'attire_context':slot('attire_context',
            ['setting'],semantic_role='contextual',property_prefixes=['world.'])},
            {'base':owner_map(('scene','scene'))}),{'attire_context':['context']});c.validate(data)
        self.assertTrue(self.allowed(data,core(['scene_A'])))
        self.assertEqual(roles.propose(data,'attire_context',A,[])['effects']['properties'],[])
        data['slot_catalog']['attire_context']['semantic_role']='direct'
        seal(data,{'attire_context':['context']});self.assertRaises(ValueError,c.validate,data)

    def test_all_actual_effects_need_independent_coverage_even_without_displayed_role(self):
        data=face_source();p=data['candidates'][A]['content']['role_evidence'];p['roles'].clear();seal(data,{});c.validate(data)
        for view in self.views(data):
            self.assertFalse(self.allowed(view,core(['face_A'])))
            self.assertTrue(self.allowed(view,core(['face_A'],[('subject','face_A','anatomy.face.presence','present')])))
        data=reviewed_source();record=data['candidates'][A]
        record['effects']['properties'].append({'dimension':'material','target':'main_subject','property':'surface.texture'})
        p=record['content']['role_evidence'];p['meaning_sha256']=e.meaning_sha256(record);p['effect_sets']['base']=e.effect_set(record,'base');reattest(data)
        self.assertRaises(ValueError,c.validate,data)

    def test_empty_coarse_or_extra_effect_dimensions_are_not_silently_narrowed(self):
        for effects in [{'dimensions':['material'],'properties':[]},
                        {'dimensions':['material','lighting'],'properties':[{'dimension':'material','target':'main_subject','property':'surface.material'}]}]:
            data=reviewed_source();record=data['candidates'][A];record['effects']=effects
            seal(data,{'surface_material':['satin']});self.assertRaises(ValueError,c.validate,data)

    def test_missing_and_malformed_owner_bindings_fail_without_anatomy_inference(self):
        for bindings in [[],[{'target':'main_subject','core_role':'main_subject','origin':'existing','introduced_by':'fake'}],
                         [{'target':'main_subject','core_role':'main_subject','origin':'existing','introduced_by':None}]*2]:
            data=reviewed_source();data['candidates'][A]['content']['role_evidence']['owner_maps']['base']['bindings']=bindings
            reattest(data);self.assertRaises(ValueError,c.validate,data)

    def test_owner_alias_and_part_hierarchy_block_same_frozen_property(self):
        lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'appearance','target':'actor_A','property':'skin.color'}]}
        effect=[{'dimension':'lighting','target':'face_A','property':'skin.color'}]
        self.assertFalse(property_effects_allowed(lock,['lighting'],effect))
        frozen=core(['actor_A','face_A'],edges=[('part_of','face_A','actor_A')]);graph=e.frozen_witnesses(frozen)['graph']
        self.assertFalse(property_effects_allowed(lock,['lighting'],effect,owner_graph=graph))
        alias=core(['actor_A','face_A'],edges=[('equivalent','face_A','actor_A')]);graph=e.frozen_witnesses(alias)['graph']
        self.assertFalse(property_effects_allowed(lock,['lighting'],effect,owner_graph=graph))

    def test_explicit_disjoint_secondary_actor_can_edit_its_own_property(self):
        lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'appearance','target':'actor_A','property':'skin.color'}]}
        effect=[{'dimension':'lighting','target':'face_B','property':'skin.color'}]
        frozen=core(['actor_A','actor_B','face_B'],edges=[('part_of','face_B','actor_B'),('disjoint','actor_A','actor_B')])
        graph=e.frozen_witnesses(frozen)['graph']
        self.assertTrue(property_effects_allowed(lock,['lighting'],effect,owner_graph=graph))
        self.assertFalse(property_effects_allowed(lock,['lighting'],effect))

    def test_cyclic_dangling_or_contradictory_owner_graphs_fail(self):
        for edges in [[('part_of','actor_A','actor_B'),('part_of','actor_B','actor_A')],
                      [('equivalent','actor_A','actor_B'),('disjoint','actor_A','actor_B')],
                      [('part_of','face','actor_A'),('part_of','face','actor_B'),('disjoint','actor_A','actor_B')],
                      [('part_of','unknown','actor_A')]]:
            with self.subTest(edges=edges):self.assertRaises(ValueError,e.frozen_witnesses,core(['actor_A','actor_B','face'],edges=edges))

    def test_nonrequired_foreign_span_or_foreign_frozen_evidence_never_witnesses_fact(self):
        data=face_source();base=core(['face_A'],[('subject','face_A','anatomy.face.presence','present')])
        for defect in ['advisory','excluded','span','evidence','unlocked']:
            frozen=copy.deepcopy(base);row=frozen['semantic_assertions'][-1]
            if defect in ['advisory','excluded']:row['polarity']=defect
            elif defect=='span':row['source_span_ids']=['foreign']
            elif defect=='evidence':row['evidence']={'carrier':'invented phrase'}
            else:frozen['intent_lock']['locked_dimensions'].remove('subject')
            with self.subTest(defect=defect):self.assertFalse(self.allowed(data,frozen))

    def test_core_witness_wire_rejects_coercion_and_preserves_exact_typed_axes(self):
        from photo_precore_bridge import load
        wire=load('photo_authoring_wire');frozen=core(['actor_A'])
        kwargs={'envelope':{'active_spans':frozen['request_binding']['active_spans']},
                'intent_lock':frozen['intent_lock'],'baseline_prompt_en':frozen['baseline_prompt_en']}
        rows=wire.normalize_semantic_assertions(frozen['semantic_assertions'],**kwargs)
        self.assertEqual(rows,frozen['semantic_assertions'])
        replay=json.loads(json.dumps(rows));self.assertEqual(e.witnesses.read(rows,
            kwargs['envelope']['active_spans'],kwargs['baseline_prompt_en']),
            e.witnesses.read(replay,kwargs['envelope']['active_spans'],kwargs['baseline_prompt_en']))
        for value in [True,42,{'id':'actor_A'},' actor_A','actor  A']:
            rows=copy.deepcopy(frozen['semantic_assertions']);rows[0]['axes']['owner']=value
            with self.subTest(value=value):self.assertRaises(ValueError,wire.normalize_semantic_assertions,rows,**kwargs)

    def test_named_korean_hyphenated_owner_ids_are_exact_not_renamed(self):
        for owner in ['actor:Alice','주인공 얼굴','Owner-42']:
            data=reviewed_source()
            seal(data,{'surface_material':['satin']});c.validate(data)
            self.assertTrue(self.allowed(data,core([owner],role_bindings={'main_subject':owner})))
            self.assertFalse(self.allowed(data,core([owner],role_bindings={})))

    def test_profile_local_effects_use_the_same_complete_mode_contract(self):
        data=reviewed_source();record=data['candidates'][A];record['record_kind']='visual_profile'
        seal(data,{'surface_material':['satin']});c.validate(data)

    def test_selected_rid_facts_quotes_effects_and_prerequisites_do_not_leak(self):
        data=reviewed_source();record=data['candidates'][A];p=record['content']['role_evidence']
        record['content']['en']='satin surface or ribbed surface';facts=[];branches=[]
        for rid,path,quote in [('satin','surface.material','satin'),('ribbed','surface.texture','ribbed')]:
            branches.append({'id':rid,'conditions':{},'context_terms':[],'effects':{'dimensions':['material'],
                'properties':[{'dimension':'material','target':'main_subject','property':path}]}})
            facts.append(fact(rid,'material','main_subject',path,'effect',quote,[],rid=rid,quote=quote,
                              operation='set_value',receivers=[]))
        record['effects']={'dimensions':[],'properties':[],'realizations':{'mode':'one','branches':branches}}
        p['facts']=facts;p['owner_maps']={rid:owner_map(('main_subject','main_subject')) for rid in ['satin','ribbed']}
        data['slot_catalog']['surface_material']['property_prefixes']=['surface.']
        seal(data,{'surface_material':['satin','ribbed']});c.validate(data)
        for rid,path in [('satin','surface.material'),('ribbed','surface.texture')]:
            full=e.qualification(data['slot_catalog']['surface_material'],record,rid)
            guard=e.qualification(data['slot_catalog']['surface_material'],layout.guard_record(record,data),rid)
            self.assertEqual(full,guard);self.assertEqual(full['matched_properties'][0]['property'],path)
            for view in self.views(data):self.assertTrue(self.allowed(view,core(['main_subject']),rid))
        p['facts'][1]['property']='surface.material';self.assertRaises(ValueError,c.validate,data)

    def test_realization_content_positive_string_cannot_borrow_foreign_rid(self):
        record={'content':{'realization_content':{'left':{'en':'left-only text'},'right':{'en':'right-only text'}}}}
        self.assertRaises(ValueError,e.positive_string,record,'/content/realization_content/right/en',realization_id='left')

    def test_source_correction_fixture_records_exact_before_after_and_rationale(self):
        data=reviewed_source();before=copy.deepcopy(data['candidates'][A]);record=data['candidates'][A]
        record['content']['en']='a matte garment surface';p=record['content']['role_evidence'];p['facts'][0]['quote']='matte'
        p['facts'][0]['value']['value']='matte';p['review']['source_correction']={
            'before_sha256':e.meaning_sha256(before),'after_sha256':'pending',
            'rationale':'Fixture only: explicitly replace satin material by matte material, then rereview the whole source.'}
        seal(data,{'surface_material':['satin']});c.validate(data)
        self.assertNotEqual(e.meaning_sha256(before),p['review']['source_correction']['after_sha256'])


if __name__=='__main__':unittest.main()


class NativeRoleAddressTests(unittest.TestCase):
    def test_one_source_reuses_stable_role_with_two_distinct_actual_owner_ids(self):
        data=reviewed_source();proof=data['candidates'][A]['content']['role_evidence']
        self.assertEqual(proof['owner_maps']['base']['bindings'][0]['core_role'],'main_subject')
        for actual in ['request-uuid-1','다음 요청의 옷감']:
            frozen=core([actual],role_bindings={'main_subject':actual})
            for record in [data['candidates'][A],layout.guard_record(data['candidates'][A],data)]:
                entry=c.entry({**data,'candidates':{A:record}},A)
                self.assertTrue(e.admission(entry,frozen)['allowed'])
                self.assertEqual(e.permission_scope(entry,frozen)[1][0]['target'],actual)
            wrong=core([actual],role_bindings={'secondary_subject':actual})
            self.assertFalse(e.admission(c.entry(data,A),wrong)['allowed'])

    def test_role_is_not_an_anatomy_witness_or_implicit_alias(self):
        data=face_source();frozen=core(['actual-cup-face'],role_bindings={'primary_face':'actual-cup-face'})
        self.assertFalse(e.admission(c.entry(data,A),frozen)['allowed'])
        frozen=core(['actual-cup-face'],[('subject','actual-cup-face','anatomy.face.presence','present')],
            role_bindings={'primary_face':'actual-cup-face'})
        self.assertTrue(e.admission(c.entry(data,A),frozen)['allowed'])
        rows=frozen['semantic_assertions'];rows.append(assertion('fake_role','role',role='source_specific_eyes',owner='actual-cup-face'))
        self.assertRaises(ValueError,e.frozen_witnesses,frozen)

    def test_routing_fragments_cannot_enlarge_meaning_even_with_fresh_attestation(self):
        for key in ['activation','match_terms','any_terms','all_terms','evidence_terms','must_mention_any',
                    'context_terms','project_glossary_aliases','aliases','keywords','terms','concept_terms','evidence_fields',
                    'family_ids','topic_ids','priority_dimension','unrecognized_source_id','field','review_scale']:
            data=reviewed_source();record=data['candidates'][A]
            record['content']['semantics']={key:['a satin garment surface']}
            proof=record['content']['role_evidence'];proof['meaning_sha256']=e.meaning_sha256(record)
            pointer='/content/semantics/'+key+'/0'
            self.assertNotIn(pointer,e.primary_paths(record,'base'))
            proof['facts'][0]['pointer']=pointer
            proof['source_units']=[{'realization_id':'base','pointer':pointer,'quote':'a satin garment surface',
                'fact_refs':['satin'],'disposition':'semantic'}]
            reattest(data)
            with self.subTest(key=key):self.assertRaisesRegex(ValueError,'metadata',c.validate,data)

    def test_reserved_preservation_reference_cannot_be_an_effect(self):
        data=reviewed_source();proof=data['candidates'][A]['content']['role_evidence']
        proof['facts'][0]['value']={'type':'frozen_property_reference/v1','value':'same'};reattest(data)
        self.assertRaisesRegex(ValueError,'preservation',c.validate,data)

    def test_qualified_introduced_prop_cannot_self_witness_or_occupy_existing_role(self):
        row=fact('add','appearance','prop','prop.presence','effect','present',[],operation='add_entity',receivers=[])
        bindings={'base':{'schema':e.OWNER_SCHEMA,'bindings':[{'target':'prop','core_role':'primary_prop',
            'origin':'introduced','introduced_by':'add'}]}}
        data=seal(source('add a small ceramic prop',[row],{'prop':slot('prop',['appearance'],property_prefixes=['prop.'])},bindings),{'prop':['add']})
        c.validate(data);empty=core(['main_subject'])
        self.assertTrue(e.admission(c.entry(data,A),empty)['allowed'])
        self.assertTrue(e.permission_scope(c.entry(data,A),empty)[1][0]['target'].startswith('native-introduced:'))
        occupied=core(['main_subject','existing-prop'],role_bindings={'main_subject':'main_subject','primary_prop':'existing-prop'})
        self.assertFalse(e.admission(c.entry(data,A),occupied)['allowed'])


    def test_metadata_suffix_rule_does_not_mistake_actual_rid_for_a_routing_key(self):
        record={'content':{'realization_content':{'topic_ids':{'en':'a satin garment surface'}}}}
        self.assertEqual(e.positive_string(record,'/content/realization_content/topic_ids/en',realization_id='topic_ids'),
            'a satin garment surface')
        self.assertRaises(ValueError,e.positive_string,record,'/content/realization_content/topic_ids/en',realization_id='other')

    def test_compact_guard_is_not_a_replacement_for_full_positive_source_validation(self):
        data=reviewed_source();guard=layout.guard_record(data['candidates'][A],data)
        self.assertRaisesRegex(ValueError,'full positive source',e.validate,guard,data['slot_catalog'])

    def test_explicit_wig_hair_support_does_not_invent_nails_or_evade_same_owner_lock(self):
        rows=[fact('hair','subject','hair_surface','anatomy.hair.presence','prerequisite','present',[],quote='existing wig hair'),
            fact('color','appearance','hair_surface','hair.color','effect','copper',['hair'],
                quote='copper',operation='set_value',receivers=[])]
        data=seal(source('copper color on the existing wig hair',rows,
            {'hair_color':slot('hair_color',['appearance'],property_prefixes=['hair.color'])},
            {'base':owner_map(('hair_surface','primary_hair'))}),{'hair_color':['color']});c.validate(data)
        wig=core(['wig-fiber'],[('subject','wig-fiber','anatomy.hair.presence','present')],
            role_bindings={'primary_hair':'wig-fiber'})
        self.assertTrue(e.admission(c.entry(data,A),wig)['allowed'])
        nails=[fact('nails','subject','nail_surface','anatomy.nails.presence','prerequisite','present',[],quote='existing nails'),
            fact('color','appearance','nail_surface','nail.color','effect','copper',['nails'],
                quote='copper',operation='set_value',receivers=[])]
        nail_data=seal(source('copper color on the existing nails',nails,
            {'nail_color':slot('nail_color',['appearance'],property_prefixes=['nail.color'])},
            {'base':owner_map(('nail_surface','primary_hands'))}),{'nail_color':['color']});c.validate(nail_data)
        self.assertFalse(e.admission(c.entry(nail_data,A),wig)['allowed'])
        wig['intent_lock']['semantic_anchors']=[{'dimension':'appearance','target':'wig-fiber','property':'hair.color'}]
        self.assertFalse(e.property_scope_allowed(wig,['appearance'],data['candidates'][A]['effects']['properties'],record=data['candidates'][A]))

    def test_object_has_only_its_explicitly_declared_depiction_face(self):
        frozen=core(['teacup','painted-face'],[('subject','painted-face','anatomy.face.presence','present')],
            edges=[('part_of','painted-face','teacup')],role_bindings={'main_subject':'teacup','primary_face':'painted-face'})
        data=face_source();self.assertTrue(e.admission(c.entry(data,A),frozen)['allowed'])
        frozen['intent_lock']['semantic_anchors']=[{'dimension':'lighting','target':'main_subject','property':'lighting.direction'}]
        self.assertFalse(e.property_scope_allowed(frozen,['lighting'],data['candidates'][A]['effects']['properties'],record=data['candidates'][A]))
        undeclared=core(['teacup'],role_bindings={'main_subject':'teacup'})
        self.assertFalse(e.admission(c.entry(data,A),undeclared)['allowed'])

    def test_neutral_bounds_are_sixty_four_total_rows_and_thirty_two_owners(self):
        frozen=core(['owner-'+str(i) for i in range(32)],role_bindings={})
        self.assertEqual(len(e.frozen_witnesses(frozen)['graph']['owners']),32)
        frozen['semantic_assertions'].append(assertion('overflow_owner','owner',owner='owner-32',owner_kind='entity'))
        self.assertRaises(ValueError,e.frozen_witnesses,frozen)
        frozen=core(['owner-'+str(i) for i in range(32)],role_bindings={})
        frozen['semantic_assertions'] += [assertion('bounded_fact_'+str(i),'fact',owner='owner-'+str(i),
            property='entity.presence',value_type='entity.presence/v1',value='present') for i in range(32)]
        self.assertEqual(len(e.frozen_witnesses(frozen)['facts']),32)
        frozen['semantic_assertions'].append(assertion('overflow_fact','fact',owner='owner-0',
            property='entity.count',value_type='entity.count/v1',value='one'))
        self.assertRaises(ValueError,e.frozen_witnesses,frozen)
