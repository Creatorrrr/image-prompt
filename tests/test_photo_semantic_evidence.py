"""Exact witnesses, owner scope, optional choices and lazy metadata regressions."""
import copy
import unittest
from tests.test_photo_candidate_corpus import fixture,A
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_global_index as index
import photo_role_proposals as roles
import photo_search_layout as layout
import photo_semantic_evidence as evidence
import photo_slot_semantics as semantics


def reviewed_source():
    data=fixture();data['slot_bindings'].clear()
    data['slot_catalog']={tag:slot(tag,['material'],property_prefixes=[path])
        for tag,path in [('surface_material','surface.material'),('texture','surface.texture')]}
    record=data['candidates'][A];record['content']={'en':'a satin garment surface'}
    record['effects']={'dimensions':['material'],'properties':[
        {'dimension':'material','target':'main_subject','property':'surface.material'}]}
    fact={'pointer':'/content/en','quote':'satin garment','dimension':'material',
          'target':'main_subject','property':'surface.material',
          'realization_id':'base','required_carriers':[]}
    record['content']['role_evidence']={'schema':evidence.SCHEMA,
        'meaning_sha256':evidence.meaning_sha256(record),'catalog_sha256':c.digest(data['slot_catalog']),
        'complete':True,'roles':{'surface_material':{
            'spec_sha256':c.digest(data['slot_catalog']['surface_material']),
            'scope':'whole_record','realization_ids':['base'],'evidence':[fact]}},
        'review':{'basis':'source review fixture','independent_human_review':False}}
    return data


class SemanticEvidenceTests(unittest.TestCase):
    def test_explicit_invalid_evidence_cannot_reactivate_an_unreviewed_fallback(self):
        for invalid in [None, {}, False]:
            data = reviewed_source(); record = data['candidates'][A]
            spec = data['slot_catalog']['surface_material']
            record['content']['role_evidence'] = invalid
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    c.validate(data)
                self.assertEqual(evidence.qualification(spec, record)['status'], 'review_required')
                self.assertFalse(evidence.existing_owner_allowed(
                    {'role_evidence': invalid}, {}, {}, data['slot_catalog']))
                # A present invalid compact guard cannot fall back to another proof.
                self.assertFalse(evidence.existing_owner_allowed(
                    {'_semantic_evidence_guard': invalid, 'role_evidence': {'schema': evidence.SCHEMA,
                     'complete': True, 'roles': {}}}, {}, {}, data['slot_catalog']))

    def actor_source(self,tag='nail_appearance',path='nails.color',text='bounded polish on fingernail plates',
                     carrier='fingernails',target='main_subject',owners=None,dimension='appearance'):
        data=reviewed_source();spec=slot(tag,[dimension],property_prefixes=[path]);spec['owners']=owners or ['actor']
        data['slot_catalog']={tag:spec};record=data['candidates'][A];record['content']={'en':text}
        record['effects']={'dimensions':[dimension],'properties':[{'dimension':dimension,'target':target,'property':path}]}
        record['content']['role_evidence']={'schema':evidence.SCHEMA,'meaning_sha256':evidence.meaning_sha256(record),
            'catalog_sha256':c.digest(data['slot_catalog']),'complete':True,'roles':{tag:{'spec_sha256':c.digest(spec),
            'scope':'whole_record','realization_ids':['base'],'evidence':[{'pointer':'/content/en','quote':text,
            'dimension':dimension,'target':target,'property':path,'realization_id':'base',
            'required_carriers':[{'target':target,'carrier':carrier}]}]}},'review':{}}
        c.validate(data);return data

    def core(self,text,carriers=(),target='main_subject'):
        return {'contract_version':'photo-authorial-core/v3',
                'request_binding':{'active_spans':[{'source_span_id':'request_1','text':text}]},
                'subject':text,'baseline_prompt_en':text,'user_exclusions':[],
                'semantic_assertions':([{'assertion_id':'carrier_1','dimension':'subject',
                    'polarity':'required','source_span_ids':['request_1'],
                    'axes':{'carrier_target':target,'existing_carriers':list(carriers)},
                    'evidence':{'carrier':text},'affected_dimensions':['subject']}] if carriers else [])}

    def test_nail_owner_requires_explicit_carrier_even_for_human_or_animal_category(self):
        data=self.actor_source();entry=c.entry(data,A)
        self.assertEqual(data['candidates'][A]['conditions'],{})
        for text,category in [('A single blue porcelain teacup','object'),
                              ('An adult model','human'),('A tabby cat','animal')]:
            with self.subTest(text=text):
                self.assertFalse(evidence.existing_owner_allowed(entry,self.core(text),
                    {'subject_category':category},data['slot_catalog']))
        self.assertTrue(evidence.existing_owner_allowed(entry,
            self.core('An adult model with visible fingernails',['fingernails']),
            {'subject_category':'human'},data['slot_catalog']))

    def test_depiction_wig_and_named_actor_words_do_not_invent_carriers(self):
        data=self.actor_source('hair_color','hair.color','pink exterior hair',carrier='hair')
        for text in ['A pink wig','A porcelain teacup','A painted doll',
                     'A humanoid robot','An abstract sculpture','A portrait of Alice']:
            with self.subTest(text=text):
                self.assertFalse(evidence.existing_owner_allowed(c.entry(data,A),self.core(text),
                    {'subject_category':'object'},data['slot_catalog']))
        wig=self.core('A pink wig with visible strands',['hair'])
        self.assertTrue(evidence.existing_owner_allowed(c.entry(data,A),wig,
            {'subject_category':'object'},data['slot_catalog']))
        nails=self.actor_source()
        self.assertFalse(evidence.existing_owner_allowed(c.entry(nails,A),wig,
            {'subject_category':'object'},nails['slot_catalog']))

    def test_compact_guard_enforces_the_same_existing_owner_requirement(self):
        data=self.actor_source();guard=layout.guard_record(data['candidates'][A])
        view={**data,'candidates':{A:guard}}
        for core,allowed in [(self.core('A single teacup'),False),
                (self.core('A model with fingernail plates',['fingernails']),True)]:
            for source in [data,view]:
                self.assertEqual(evidence.existing_owner_allowed(c.entry(source,A),core,
                    {'subject_category':'object'},data['slot_catalog']),allowed)

    def test_qualified_role_is_discovered_without_a_persistent_tag_or_keyword_quota(self):
        data=reviewed_source();c.validate(data)
        p=roles.propose(data,'surface_material',A,[])
        self.assertIsNone(p['source_binding_id']);self.assertEqual(p['applicability_status'],'eligible')
        self.assertEqual(p['semantic_fit']['reason'],'source_reviewed_owned_positive_evidence')

    def test_complete_review_rejects_an_unsupported_role_despite_similar_words(self):
        data=reviewed_source();record=data['candidates'][A]
        result=semantics.fit(data['slot_catalog']['texture'],record,'texture surface satin weave')
        self.assertEqual(result['status'],'incompatible')

    def test_metadata_and_tags_do_not_change_lexical_or_embedding_body(self):
        data=reviewed_source();record=data['candidates'][A];before=index.text(record)
        stripped=copy.deepcopy(record);stripped['content'].pop('role_evidence')
        self.assertEqual(index.fields(record),index.fields(stripped));self.assertEqual(before,index.text(stripped))

    def test_source_body_effects_and_conditions_cannot_change_without_review_rebinding(self):
        for field in ['body','effects','conditions']:
            data=reviewed_source();record=data['candidates'][A]
            if field=='body':record['content']['en']='a plastic surface'
            elif field=='effects':record['effects']['properties'][0]['target']='background'
            else:record['conditions']={'for_any':['human']}
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(data)

    def test_changed_catalog_requires_a_new_semantic_review(self):
        data=reviewed_source();data['slot_catalog']['surface_material']['description']+=' changed'
        self.assertRaises(ValueError,c.validate,data)

    def test_routing_and_negative_examples_cannot_qualify_positive_facts(self):
        for key in ['tags','facets','confusion_boundaries','contrast_examples','reject_substitutes',
                    'claim_limits','research_claim_limits','semantic_review','review','provenance','routing']:
            data=reviewed_source();record=data['candidates'][A];record['content'][key]=['satin garment']
            proof=record['content']['role_evidence'];proof['meaning_sha256']=evidence.meaning_sha256(record)
            proof['roles']['surface_material']['evidence'][0]['pointer']='/content/'+key+'/0'
            with self.subTest(field=key),self.assertRaises(ValueError):c.validate(data)

    def test_quote_property_and_owner_must_match_the_selected_source(self):
        for field,value in [('quote','invented satin'),('target','background'),('property','surface.texture')]:
            data=reviewed_source();role=data['candidates'][A]['content']['role_evidence']['roles']['surface_material']
            role['evidence'][0][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):c.validate(data)

    def test_lazy_guard_uses_the_validated_projection_without_full_quotes_or_payload(self):
        data=reviewed_source();record=data['candidates'][A];guard=layout.guard_record(record)
        self.assertNotIn('role_evidence',guard['content']);proof=guard['_semantic_evidence_guard']
        self.assertNotIn('quote',proof['roles']['surface_material']['evidence'][0])
        self.assertEqual(semantics.fit(data['slot_catalog']['surface_material'],record,'')['status'],
                         semantics.fit(data['slot_catalog']['surface_material'],guard,'')['status'])

    def test_a_role_supported_only_by_one_alternative_cannot_adopt_the_other(self):
        data=reviewed_source();record=data['candidates'][A];props=record['effects']['properties']
        record['effects']={'dimensions':[],'properties':[], 'realizations':{'mode':'one','branches':[
            {'id':'satin','conditions':{},'context_terms':[], 'effects':{'dimensions':['material'],'properties':props}},
            {'id':'plain_geometry','conditions':{},'context_terms':[], 'effects':{'dimensions':['composition'],
                'properties':[{'dimension':'composition','target':'image','property':'layout.center'}]}}]}}
        proof=record['content']['role_evidence'];proof['meaning_sha256']=evidence.meaning_sha256(record)
        role=proof['roles']['surface_material'];role.update(scope='positive_alternative',realization_ids=['satin'])
        role['evidence'][0]['realization_id']='satin'
        c.validate(data)
        for rid,status in [('satin','eligible'),('plain_geometry','incompatible')]:
            self.assertEqual(roles.propose(data,'surface_material',A,[],realization_ids=[rid])['applicability_status'],status)

    def test_no_positive_role_for_diagnostic_and_no_foreign_realization(self):
        for defect in ['diagnostic','foreign']:
            data=reviewed_source();record=data['candidates'][A];proof=record['content']['role_evidence']
            if defect=='diagnostic':record['record_kind']='diagnostic';proof['meaning_sha256']=evidence.meaning_sha256(record)
            else:proof['roles']['surface_material']['realization_ids']=['unwritten']
            with self.subTest(defect=defect),self.assertRaises(ValueError):c.validate(data)

    def branch_source(self):
        data=reviewed_source();record=data['candidates'][A]
        spec=data['slot_catalog']['surface_material'];spec['property_prefixes']=['surface.']
        record['content']={'en':'satin material or ribbed texture','realization_content':{}}
        branches=[];facts=[]
        for rid,path,text in [('satin','surface.material','satin material'),
                              ('ribbed','surface.texture','ribbed texture')]:
            branches.append({'id':rid,'conditions':{},'context_terms':[],
                'effects':{'dimensions':['material'],'properties':[
                    {'dimension':'material','target':'main_subject','property':path}]}})
            record['content']['realization_content'][rid]={'en':text,'ko':text,
                'embedding_text':text,'concept_units':[text],'relations':[]}
            facts.append({'pointer':'/content/realization_content/'+rid+'/en','quote':text,
                'dimension':'material','target':'main_subject','property':path,
                'realization_id':rid,'required_carriers':[]})
        record['effects']={'dimensions':[],'properties':[],
            'realizations':{'mode':'one','branches':branches}}
        record['content']['role_evidence']={'schema':evidence.SCHEMA,
            'meaning_sha256':evidence.meaning_sha256(record),'catalog_sha256':c.digest(data['slot_catalog']),
            'complete':True,'review':{},'roles':{'surface_material':{'spec_sha256':c.digest(spec),
                'scope':'whole_record','realization_ids':['satin','ribbed'],'evidence':facts}}}
        return data

    def test_each_rid_can_qualify_distinct_facts_without_fake_common_properties(self):
        data=self.branch_source();c.validate(data);record=data['candidates'][A]
        guard=layout.guard_record(record);spec=data['slot_catalog']['surface_material']
        for rid,path in [('satin','surface.material'),('ribbed','surface.texture')]:
            expected=[{'dimension':'material','target':'main_subject','property':path}]
            full=evidence.qualification(spec,record,rid)
            compact=evidence.qualification(spec,guard,rid)
            self.assertEqual(full,compact);self.assertEqual(full['status'],'eligible')
            self.assertEqual(full['matched_properties'],expected)
            self.assertEqual(roles.propose(data,'surface_material',A,[],realization_ids=[rid])[
                'semantic_fit']['matched_properties'],expected)

    def test_every_fact_must_match_its_own_rid_and_every_qualified_rid_needs_a_fact(self):
        for defect in ['foreign_property','uncovered_rid','foreign_rid','duplicate_fact']:
            data=self.branch_source();facts=data['candidates'][A]['content']['role_evidence'][
                'roles']['surface_material']['evidence']
            if defect=='foreign_property':facts[1]['property']='surface.material'
            elif defect=='uncovered_rid':facts.pop()
            elif defect=='foreign_rid':facts[1]['realization_id']='unwritten'
            else:facts.append(copy.deepcopy(facts[0]))
            with self.subTest(defect=defect),self.assertRaises(ValueError):c.validate(data)

    def test_realization_text_cannot_be_borrowed_from_another_actual_branch(self):
        data=self.branch_source();record=data['candidates'][A]
        first=record['content']['role_evidence']['roles']['surface_material']['evidence'][0]
        first.update(pointer='/content/realization_content/ribbed/en',quote='ribbed texture')
        self.assertRaises(ValueError,c.validate,data)

    def test_missing_native_rid_or_carrier_review_is_never_assumed_complete(self):
        for field in ['realization_id','required_carriers']:
            data=reviewed_source();record=data['candidates'][A]
            record['content']['role_evidence']['roles']['surface_material']['evidence'][0].pop(field)
            with self.subTest(field=field):
                self.assertRaises(ValueError,c.validate,data)
                self.assertEqual(evidence.qualification(data['slot_catalog']['surface_material'],record)[
                    'status'],'review_required')
                self.assertFalse(evidence.existing_owner_allowed(c.entry(data,A),self.core('A blue teacup'),
                    {},data['slot_catalog']))

    def test_noncanonical_or_missing_positive_pointers_raise_value_errors(self):
        for pointer in ['/content/en/missing','/content/missing','/content/tags/0',
                        '/content/aliases/-1','/content/aliases/00']:
            data=reviewed_source();record=data['candidates'][A];record['content']['aliases']=['satin garment']
            proof=record['content']['role_evidence'];proof['meaning_sha256']=evidence.meaning_sha256(record)
            proof['roles']['surface_material']['evidence'][0]['pointer']=pointer
            with self.subTest(pointer=pointer),self.assertRaises(ValueError):c.validate(data)

    def test_carrier_review_requires_explicit_exact_target_and_unique_typed_rows(self):
        for requirements in [None,{},['face'],[{'target':'*','carrier':'face'}],
                [{'target':'main_subject','carrier':'face','invented':True}],
                [{'target':'main_subject','carrier':'face'}]*2]:
            data=reviewed_source();record=data['candidates'][A]
            record['content']['role_evidence']['roles']['surface_material']['evidence'][0][
                'required_carriers']=requirements
            with self.subTest(requirements=requirements),self.assertRaises(ValueError):c.validate(data)

    def test_carrier_independent_material_and_image_light_are_not_blanket_blocked(self):
        data=reviewed_source();entry=c.entry(data,A)
        self.assertTrue(evidence.existing_owner_allowed(entry,self.core('A blue teacup'),
            {'subject_category':'object'},data['slot_catalog']))
        for owner in ['image','surface']:
            data=self.actor_source('lighting','lighting.fill','A broad image fill',
                carrier='face',target='image',owners=[owner],dimension='lighting')
            record=data['candidates'][A]
            fact=record['content']['role_evidence']['roles']['lighting']['evidence'][0]
            fact['required_carriers']=[]
            self.assertTrue(evidence.existing_owner_allowed(c.entry(data,A),self.core('A blue teacup'),
                {'subject_category':'object'},data['slot_catalog']))

    def test_face_lighting_requires_carrier_even_when_role_owner_is_not_actor(self):
        data=self.actor_source('face_light','lighting.face_side','sidelight across face planes',
            carrier='face',owners=['light'],dimension='lighting')
        for text,carriers,allowed in [('A blue porcelain teacup',[],False),
                ('A faceless abstract sculpture',[],False),('A generic robot',[],False),
                ('A carved face on a ceramic teacup',['face'],True),
                ('A portrait of Alice with a visible face',['face'],True)]:
            with self.subTest(text=text):
                self.assertEqual(evidence.existing_owner_allowed(c.entry(data,A),self.core(text,carriers),
                    {'subject_category':'object'},data['slot_catalog']),allowed)

    def test_face_framing_requires_existing_face_without_actor_slot_ownership(self):
        data=self.actor_source('framing','framing.face_crop','tight crop around existing facial planes',
            carrier='face',owners=['image'],dimension='framing')
        entry=c.entry(data,A)
        self.assertFalse(evidence.existing_owner_allowed(entry,self.core('A teacup on a table'),
            {'subject_category':'object'},data['slot_catalog']))
        self.assertTrue(evidence.existing_owner_allowed(entry,
            self.core('A face-bearing ceramic depiction',['face']),
            {'subject_category':'object'},data['slot_catalog']))

    def test_primary_object_can_have_separately_declared_secondary_face(self):
        data=self.actor_source('face_light','lighting.face_side','sidelight across secondary face',
            carrier='face',target='secondary_depiction',owners=['light'],dimension='lighting')
        entry=c.entry(data,A);text='A teacup beside a painted face on a separate panel'
        for target,allowed in [('main_subject',False),('secondary_depiction',True)]:
            self.assertEqual(evidence.existing_owner_allowed(entry,self.core(text,['face'],target),
                {'subject_category':'object'},data['slot_catalog']),allowed)

    def test_image_effect_can_require_a_distinct_subject_carrier(self):
        data=self.actor_source('face_light','lighting.face_side','image sidelight across face planes',
            carrier='face',target='image',owners=['image'],dimension='lighting')
        fact=data['candidates'][A]['content']['role_evidence']['roles']['face_light']['evidence'][0]
        fact['required_carriers']=[{'target':'main_subject','carrier':'face'}]
        self.assertTrue(evidence.existing_owner_allowed(c.entry(data,A),
            self.core('A portrait with visible face planes',['face']),{},data['slot_catalog']))

    def test_named_and_korean_owner_ids_preserve_exact_authored_identity(self):
        for owner in ['actor:Alice','주인공 얼굴','Owner-42']:
            data=self.actor_source('face_light','lighting.face_side','light across the named face',
                carrier='face',target=owner,owners=['light'],dimension='lighting')
            record=data['candidates'][A]
            for carrier_owner,allowed in [(owner,True),('main_subject',False)]:
                core=self.core('A named depiction with a visible face',['face'],carrier_owner)
                for source in [data,{**data,'candidates':{A:layout.guard_record(record)}}]:
                    with self.subTest(owner=owner,carrier_owner=carrier_owner):
                        self.assertEqual(evidence.existing_owner_allowed(c.entry(source,A),core,
                            {},data['slot_catalog']),allowed)

    def test_carriers_require_required_subject_assertions_and_grounded_frozen_evidence(self):
        data=self.actor_source();entry=c.entry(data,A)
        base=self.core('A model with visible fingernails',['fingernails'])
        for defect in ['advisory','excluded','wrong_dimension','foreign_span','no_span',
                       'no_evidence','foreign_evidence','no_subject_effect','wrong_target','scalar_carriers']:
            core=copy.deepcopy(base);row=core['semantic_assertions'][0]
            if defect in ['advisory','excluded']:row['polarity']=defect
            elif defect=='wrong_dimension':row['dimension']='appearance'
            elif defect=='foreign_span':row['source_span_ids']=['absent']
            elif defect=='no_span':core['request_binding']['active_spans']=[]
            elif defect=='no_evidence':row['evidence']={}
            elif defect=='foreign_evidence':row['evidence']={'carrier':'imagined anatomy'}
            elif defect=='no_subject_effect':row['affected_dimensions']=['appearance']
            elif defect=='wrong_target':row['axes']['carrier_target']='another_actor'
            else:row['axes']['existing_carriers']='fingernails'
            with self.subTest(defect=defect):
                self.assertFalse(evidence.existing_owner_allowed(entry,core,{},data['slot_catalog']))

    def test_carrier_axes_are_accepted_by_existing_core_v3_wire_without_new_noun_classifier(self):
        from photo_precore_bridge import load
        wire=load('photo_authoring_wire')
        core=self.core('A blue teacup bearing a carved face',['face'])
        result=wire.normalize_semantic_assertions(core['semantic_assertions'],
            envelope={'active_spans':core['request_binding']['active_spans']},
            intent_lock={'locked_dimensions':['subject'],'open_dimensions':['lighting']},
            baseline_prompt_en=core['baseline_prompt_en'])
        core['semantic_assertions']=result
        self.assertEqual(evidence.grounded_carriers(core),{('main_subject','face')})

    def test_existing_carrier_does_not_unlock_frozen_property_on_the_same_owner(self):
        from photo_contracts import property_effects_allowed
        data=self.actor_source();entry=c.entry(data,A)
        core=self.core('A model with red polished fingernails',['fingernails'])
        self.assertTrue(evidence.existing_owner_allowed(entry,core,{},data['slot_catalog']))
        lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[
            {'dimension':'appearance','target':'main_subject','property':'nails.color'}]}
        self.assertFalse(property_effects_allowed(lock,entry['affected_dimensions'],entry['affected_properties']))

    def test_compact_carrier_and_qualification_filter_only_the_selected_rid(self):
        data=self.branch_source();record=data['candidates'][A]
        facts=record['content']['role_evidence']['roles']['surface_material']['evidence']
        facts[1]['required_carriers']=[{'target':'main_subject','carrier':'face'}]
        c.validate(data);guard=layout.guard_record(record)
        for source in [data,{**data,'candidates':{A:guard}}]:
            for rid,allowed in [('satin',True),('ribbed',False)]:
                self.assertEqual(evidence.existing_owner_allowed(c.entry(source,A,realization_id=rid),
                    self.core('A blue teacup'),{},data['slot_catalog']),allowed)

if __name__=='__main__':unittest.main()
