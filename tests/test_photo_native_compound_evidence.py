"""Selected source/member/profile/joint native effect coverage, without binding identity."""
import copy
import unittest
from tests.test_photo_semantic_evidence import (A, reviewed_source, face_source, source, fact,
    seal, owner_map, core, reattest)
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_semantic_evidence as e
import photo_search_layout as layout
import photo_role_proposals as proposals
import prompt_generator as g

B='cand_'+'b'*32
C='cand_'+'c'*32


def dependencies(data,parent,rid,children):
    rows=[]
    for cid in children:
        child=data['candidates'][cid]
        rows.append({'candidate_id':cid,'realization_ids':r.ids(child),
            'meaning_sha256':e.meaning_sha256(child),
            'qualification_sha256':c.digest(child['content']['role_evidence']),
            'selection':'required'})
    data['candidates'][parent]['content']['role_evidence']['dependencies'][rid]=rows


def bundle():
    data=reviewed_source();child=face_source();record=copy.deepcopy(child['candidates'][A]);record['id']=B
    data['slot_catalog'].update(child['slot_catalog']);data['candidates'][B]=record
    seal(data,{'light_direction':['underlight']},cid=B)
    parent=data['candidates'][A];parent['record_kind']='visual_bundle'
    # Candidate identity and selected RID are native proof inputs. No role or
    # binding ID can establish an effect, carrier or owner witness.
    parent['content']['member_candidates']=[{'candidate_id':B,'adoption':'required','requirements':{}}]
    dependencies(data,A,'base',[B]);seal(data,{'surface_material':['satin']})
    return data


class CompoundEvidenceTests(unittest.TestCase):
    def frozen(self,face=True):
        return core(['main_subject','face_A','image_A'],
            [('subject','face_A','anatomy.face.presence','present')] if face else [])
    def entry_views(self,data,**kwargs):
        full=c.entry(data,A,realization_id='base',**kwargs)
        guard=layout.guard_record(data['candidates'][A],data)
        guarded=c.entry({**data,'candidates':{A:guard}},A,realization_id='base',**kwargs)
        return [full,guarded]

    def test_member_prerequisite_is_enforced_without_a_displayed_member_role(self):
        data=bundle();c.validate(data)
        for entry in self.entry_views(data):
            self.assertFalse(e.admission(entry,self.frozen(False))['allowed'])
            result=e.admission(entry,self.frozen());self.assertTrue(result['allowed'])
            self.assertEqual(result['dependencies'][0]['candidate_id'],B)
            dims,props,_=e.permission_scope(entry,self.frozen())
            self.assertEqual(dims,['lighting','material'])
            self.assertEqual({row['property'] for row in props},{'surface.material','lighting.direction'})
        proposal=proposals.propose(data,'surface_material',A,[])
        self.assertEqual(proposal['native_qualification'],'qualified')

    def test_member_property_lock_is_not_hidden_by_the_parent_own_effects(self):
        data=bundle();frozen=self.frozen();frozen['intent_lock']['semantic_anchors']=[
            {'dimension':'lighting','target':'face_A','property':'lighting.direction'}]
        for entry in self.entry_views(data):
            self.assertFalse(g.core_entry_eligible(data,frozen,{'subject_category':'object'},
                {'subject':{}},'',entry))
        frozen['intent_lock']['semantic_anchors']=[];frozen['intent_lock']['open_dimensions'].remove('lighting')
        for entry in self.entry_views(data):
            self.assertFalse(g.core_entry_eligible(data,frozen,{'subject_category':'object'},
                {'subject':{}},'',entry))

    def test_reference_source_and_child_qualification_are_both_bound(self):
        for defect in ['reference_hash','source_change','child_proof_change','omitted_member','wrong_rid','unqualified_child']:
            data=bundle();parent=data['candidates'][A]['content']['role_evidence'];child=data['candidates'][B]
            if defect=='reference_hash':parent['reference_sha256'][B]='0'*64
            elif defect=='source_change':child['content']['en']+=' changed'
            elif defect=='child_proof_change':child['content']['role_evidence']['review']['basis']+=' revised'
            elif defect=='omitted_member':parent['dependencies']['base']=[]
            elif defect=='wrong_rid':parent['dependencies']['base'][0]['realization_ids']=['foreign']
            else:child['content'].pop('role_evidence')
            reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)

    def test_parent_joint_effect_cannot_hide_behind_complete_member_coverage(self):
        data=bundle();parent=data['candidates'][A];parent['effects']['dimensions'].append('composition')
        parent['effects']['properties'].append({'dimension':'composition','target':'image','property':'layout.arrangement'})
        seal(data,{'surface_material':['satin']});self.assertRaises(ValueError,c.validate,data)
        parent['content']['en']+=' arranged side by side'
        p=parent['content']['role_evidence'];p['facts'].append(fact('joint','composition','image',
            'layout.arrangement','effect','side_by_side',[],quote='side by side',operation='relocate',receivers=[]))
        p['owner_maps']['base']['bindings']+=owner_map(('image','image'))['bindings']
        seal(data,{'surface_material':['satin']});c.validate(data)
        for entry in self.entry_views(data):
            dims,_,_=e.permission_scope(entry,self.frozen());self.assertEqual(dims,['composition','lighting','material'])

    def test_profile_projection_effects_are_part_of_the_actual_whole_scope(self):
        data=reviewed_source();record=data['candidates'][A];record['record_kind']='visual_profile'
        record['content']['concept_candidate']={'concept_terms':['lateral illumination lookup'], 'composition_instruction':'side light',
            'affected_dimensions':['lighting'],'affected_properties':[
                {'dimension':'lighting','target':'main_subject','property':'lighting.direction'}]}
        seal(data,{'surface_material':['satin']});self.assertRaises(ValueError,c.validate,data)
        p=record['content']['role_evidence'];p['facts'].append(fact('profile_light','lighting','main_subject',
            'lighting.direction','effect','side',[],quote='side light',operation='set_value',receivers=[],
            pointer='/content/concept_candidate/composition_instruction'))
        seal(data,{'surface_material':['satin']});c.validate(data)
        full=e.qualification(data['slot_catalog']['surface_material'],record)
        guard=e.qualification(data['slot_catalog']['surface_material'],layout.guard_record(record,data))
        self.assertEqual(full,guard);self.assertEqual(full['status'],'eligible')
        for entry in self.entry_views(data):
            self.assertEqual(entry['affected_dimensions'],['lighting','material'])
            self.assertTrue(e.admission(entry,self.frozen())['allowed'])

    def test_relationship_mechanism_and_concept_use_complete_native_fact_modes(self):
        for kind in ['relationship_mechanism','relationship_concept']:
            row=fact('retained_relation','relationship','actor','relationship.same_target',
                'preservation','same_counterpart',[])
            data=seal(source('the same declared counterpart relation is retained',[row],
                {'relationship':slot('relationship',['relationship'],property_prefixes=['relationship.'])},
                {'base':owner_map(('actor','main_subject'))}),{'relationship':['retained_relation']})
            data['candidates'][A]['record_kind']=kind;seal(data,{'relationship':['retained_relation']});c.validate(data)
            frozen=core(['actor_A'],[('relationship','actor_A','relationship.same_target','same_counterpart')])
            for entry in self.entry_views(data):self.assertTrue(e.admission(entry,frozen)['allowed'])

    def test_nested_entity_bundle_keeps_all_selected_child_obligations(self):
        data=bundle();nested=copy.deepcopy(data['candidates'][A]);nested['id']=C
        data['candidates'][C]=nested;dependencies(data,C,'base',[B]);seal(data,{'surface_material':['satin']},cid=C)
        data['candidates'][A]['content']['member_candidates']=[{'candidate_id':C,'adoption':'required','requirements':{}}]
        dependencies(data,A,'base',[C]);seal(data,{'surface_material':['satin']});c.validate(data)
        for entry in self.entry_views(data):
            self.assertFalse(e.admission(entry,self.frozen(False))['allowed'])
            self.assertTrue(e.admission(entry,self.frozen())['allowed'])
            dims,props,_=e.permission_scope(entry,self.frozen());self.assertEqual(dims,['lighting','material'])
            self.assertEqual(len(props),2)

    def test_cyclic_members_or_missing_compact_dependency_guard_fail(self):
        data=bundle();guard=layout.guard_record(data['candidates'][A],data)
        guard['_semantic_evidence_guard']['dependency_guards']['base']=[]
        entry=c.entry({**data,'candidates':{A:guard}},A,realization_id='base')
        self.assertFalse(e.admission(entry,self.frozen())['allowed'])
        data['candidates'][B]['content']['member_candidates']=[{'candidate_id':A}]
        self.assertRaises(ValueError,c.validate,data)

    def test_unselected_source_member_does_not_contribute_an_effect_or_carrier(self):
        data=bundle();parent=data['candidates'][A];child=copy.deepcopy(data['candidates'][B]);child['id']=C
        data['candidates'][C]=child;seal(data,{'light_direction':['underlight']},cid=C)
        parent['content']['member_candidates'].append({'candidate_id':C,'adoption':'required','requirements':{}})
        props=parent['effects']['properties'];parent['effects']={'dimensions':[],'properties':[],
            'realizations':{'mode':'one','branches':[{'id':rid,'conditions':{},'context_terms':[],
                'member_candidate_ids':members,'effects':{'dimensions':['material'],'properties':props}}
                for rid,members in [('plain',[]),('face',[B])]]}}
        p=parent['content']['role_evidence'];original=p['facts'][0]
        p['facts']=[{**copy.deepcopy(original),'id':rid,'realization_id':rid} for rid in ['plain','face']]
        p['owner_maps']={rid:owner_map(('main_subject','main_subject')) for rid in ['plain','face']}
        p['dependencies']={'plain':[],'face':[]};dependencies(data,A,'face',[B])
        seal(data,{'surface_material':['plain','face']});c.validate(data)
        guard=layout.guard_record(parent,data)
        for view in [data,{**data,'candidates':{A:guard}}]:
            plain=c.entry(view,A,realization_id='plain');face=c.entry(view,A,realization_id='face')
            self.assertTrue(e.admission(plain,self.frozen(False))['allowed'])
            self.assertFalse(e.admission(face,self.frozen(False))['allowed'])
            self.assertEqual(e.permission_scope(plain,self.frozen(False))[0],['material'])

    def test_receiver_scope_participates_in_frozen_property_checks(self):
        data=reviewed_source();p=data['candidates'][A]['content']['role_evidence'];p['facts'][0]['receivers']=['garment']
        p['owner_maps']['base']['bindings']+=owner_map(('garment','primary_garment'))['bindings'];seal(data,{'surface_material':['satin']});c.validate(data)
        frozen=core(['main_subject','garment_A']);frozen['intent_lock']['semantic_anchors']=[
            {'dimension':'appearance','target':'garment_A','property':'surface.material'}]
        for entry in self.entry_views(data):
            _,props,graph=e.permission_scope(entry,frozen)
            self.assertIn('garment_A',{row['target'] for row in props})
            from photo_contracts import property_effects_allowed
            self.assertFalse(property_effects_allowed(frozen['intent_lock'],['material'],props,owner_graph=graph))

    def test_conditional_child_requires_an_actual_choice_and_never_unions_its_sibling(self):
        data=bundle();child=data['candidates'][B];p=child['content']['role_evidence']
        child['content']['en']='a broad image fill or an underlit centrally placed face'
        child['content']['realization_content']={rid:{'en':text,'ko':text,'embedding_text':text,
            'concept_units':[text],'relations':[]} for rid,text in
            [('fill','a broad image fill'),('face','an underlit centrally placed face')]}
        p['facts']=[
            fact('fill','lighting','image','lighting.direction','effect','broad',[],rid='fill',
                quote='broad image fill',pointer='/content/realization_content/fill/en',operation='set_value',receivers=[]),
            fact('face_present','subject','face_surface','anatomy.face.presence','prerequisite','present',[],
                rid='face',quote='face',pointer='/content/realization_content/face/en'),
            fact('underlit','lighting','face_surface','lighting.direction','effect','below',['face_present'],
                rid='face',quote='underlit',pointer='/content/realization_content/face/en',operation='set_value',receivers=[]),
            fact('center','composition','face_surface','layout.center','effect','center',['face_present'],
                rid='face',quote='centrally placed face',pointer='/content/realization_content/face/en',operation='relocate',receivers=[])]
        child['effects']={'dimensions':[],'properties':[],'realizations':{'mode':'one','branches':[
            {'id':rid,'conditions':{},'context_terms':[],'effects':{
                'dimensions':sorted({f['dimension'] for f in p['facts'] if f['realization_id']==rid and f['mode']=='effect'}),
                'properties':[{key:f[key] for key in e.PROPERTY_FIELDS} for f in p['facts']
                              if f['realization_id']==rid and f['mode']=='effect']}} for rid in ['fill','face']]}}
        p['owner_maps']={'fill':owner_map(('image','image')),'face':owner_map(('face_surface','primary_face'))}
        seal(data,{'light_direction':['fill','underlit']},cid=B);dependencies(data,A,'base',[B]);seal(data,{'surface_material':['satin']});c.validate(data)
        frozen=self.frozen(False);frozen['intent_lock']['open_dimensions'].remove('composition')
        self.assertEqual(proposals.propose(data,'surface_material',A,[])['applicability_status'],'review_required')
        selected=proposals.propose(data,'surface_material',A,[],dependency_selections={B:'fill'})
        self.assertEqual(selected['applicability_status'],'eligible')
        self.assertEqual(selected['native_effect_closure'][1]['realization_id'],'fill')
        self.assertEqual(selected['native_effect_closure'][1]['effects']['dimensions'],['lighting'])
        self.assertEqual(proposals.validate(data,selected,[])['_native_dependency_selections'],{B:'fill'})
        for entry in self.entry_views(data):
            self.assertFalse(e.admission(entry,frozen)['allowed'])
            self.assertTrue(e.admission(entry,frozen,allow_unselected=True)['allowed'])
            self.assertRaises(ValueError,e.permission_scope,entry,frozen)
            fill={**entry,'_native_dependency_selections':{B:'fill'}}
            self.assertTrue(e.admission(fill,frozen)['allowed'])
            self.assertEqual(e.permission_scope(fill,frozen)[0],['lighting','material'])
            wrong={**entry,'_native_dependency_selections':{B:'face'}}
            self.assertFalse(e.admission(wrong,frozen)['allowed'])
            foreign={**entry,'_native_dependency_selections':{B:'fill',C:'invented'}}
            self.assertFalse(e.admission(foreign,frozen)['allowed'])

    def test_selected_positive_member_requirements_bind_manual_modes_to_actual_child_facts(self):
        from tests.test_photo_semantic_evidence import reattest
        import photo_shared_views as views
        import audit_composed_prompt as audit
        data=bundle();parent=data['candidates'][A];pointer=parent['content']['member_candidates'][0]
        pointer['adoption']='optional'
        pointer['requirements']={'concept_units':['light strikes the already existing face from below'],'relations':[]}
        dependency=parent['content']['role_evidence']['dependencies']['base'][0]
        dependency['selection']='explicit_optional';path='/content/member_candidates/0/requirements/concept_units/0'
        # Both interpretations are directly authored; no mode is inferred from
        # the requirements label, selected role, or child property spelling.
        presence={'child_fact_id':'face','pointer':path,'quote':'existing face','dimension':'subject',
            'target':'face_surface','property':'anatomy.face.presence','mode':'prerequisite',
            'value':{'type':'anatomy.face.presence/v1','value':'present'},'requires':[]}
        lighting={'child_fact_id':'underlight','pointer':path,'quote':'from below','dimension':'lighting',
            'target':'face_surface','property':'lighting.direction','mode':'effect',
            'value':{'type':'lighting.direction/v1','value':'below'},'requires':['face'],
            'operation':'set_value','receivers':[]}
        dependency['requirement_bindings']={'source_sha256':c.digest(pointer['requirements']),
            'realizations':{'base':[presence,lighting]}}
        seal(data,{'surface_material':['satin']});c.validate(data)
        member=views.materialize_member(data,pointer,realization_id='base')
        self.assertEqual(member['member_requirements'],pointer['requirements'])
        self.assertEqual(member['en'],data['candidates'][B]['content']['en'])
        self.assertNotIn('concept_units',member) # no child-body replacement
        noface=self.frozen(False)
        for entry in self.entry_views(data):self.assertTrue(e.admission(entry,noface)['allowed'])
        for entry in self.entry_views(data,dependency_selections={B:'base'}):
            self.assertFalse(e.admission(entry,noface)['allowed']);self.assertTrue(e.admission(entry,self.frozen())['allowed'])
        guard=e.compact(parent,data)
        absent=e.effect_closure(A,guard,'base',{})
        audit.audit_native_member_requirement_evidence(data,absent,{}, {},'No optional child was adopted.')
        selected=e.effect_closure(A,guard,'base',{B:'base'})
        self.assertRaises(ValueError,audit.audit_native_member_requirement_evidence,data,selected,{B:'base'}, {},'face')
        phrase='A low light visibly reaches the existing face from below.'
        evidence={'member_requirement_evidence':{A:{B:{'concept_units':{'0':phrase},'relations':{}}}}}
        audit.audit_native_member_requirement_evidence(data,selected,{B:'base'},evidence,phrase)
        for defect in ['missing_binding','uncovered_unit','hidden_new_mutation','false_context','wrong_child_rid','wrong_source_quote']:
            broken=copy.deepcopy(data);dep=broken['candidates'][A]['content']['role_evidence']['dependencies']['base'][0]
            if defect=='missing_binding':dep.pop('requirement_bindings')
            elif defect=='uncovered_unit':dep['requirement_bindings']['realizations']['base']=[]
            elif defect=='hidden_new_mutation':dep['requirement_bindings']['realizations']['base'][1]['property']='skin.color'
            elif defect=='false_context':dep['requirement_bindings']['realizations']['base'][1]['mode']='context'
            elif defect=='wrong_child_rid':dep['requirement_bindings']['realizations']={'invented':[presence,lighting]}
            else:dep['requirement_bindings']['realizations']['base'][0]['quote']='invented anatomy'
            reattest(broken)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,broken)
