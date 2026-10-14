"""Explicit synthetic v4 guard/inventory/profile fixtures; never corpus approval."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from tests.test_photo_semantic_evidence import (A,source,fact,owner_map,seal,core,assertion,reattest)
from tests.test_photo_native_compound_evidence import dependencies,B
from tests import test_photo_native_fact_wire as wire_fixture
from tests.test_photo_workflow_precore import FIXTURE,files,preparation,wire
from tests.photo_native_schema import slot
import photo_semantic_evidence as e
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_search_layout as layout
import prompt_generator as g
import audit_composed_prompt as audit


def preserve(kind='reference_appearance'):
    return dict(id='preserve_'+kind,kind='preserve_established_scope',owner_role='main_subject',scope_kind=kind,
        known_absent='not_applicable',known_present='preserve_all_frozen_items',unknown='review_required')


def block(*rules):return {'schema':e.SOURCE_GUARD_SCHEMA,'rules':list(rules)}


def guarded(rules,*,prop='pose.standing',target='actor',role='main_subject',receivers=()):
    dim='pose' if prop.startswith('pose.') else 'appearance'
    row=fact('effect',dim,target,prop,'effect','standing' if dim=='pose' else 'ivory',[],operation='set_value',receivers=list(receivers))
    owners=[(target,role)]
    if receivers:owners += [(receiver,'primary_face') for receiver in receivers]
    data=source('The existing actor assumes a standing pose with the declared local rendering.',[row],
        {'test_role':slot('test_role',[dim],property_prefixes=[prop])},{'base':owner_map(*owners)})
    data['candidates'][A]['conditions']={'native_guards':block(*rules)} if rules else {}
    return seal(data,{'test_role':['effect']})


def scoped_core(state='known_present',*,scope_kind='reference_appearance',owner='actor_A',
                complete=True,host_complete=True,has_value=True):
    frozen=core(['actor_A','face_A','actor_B','image_A'],
        [('appearance','face_A','skin.tone','ivory')] if has_value else [],
        [('part_of','face_A','actor_A'),('disjoint','actor_A','actor_B')])
    text=frozen['baseline_prompt_en'];sha=hashlib.sha256(text.encode()).hexdigest()
    inventory={'schema':e.witnesses.INPUT_SCHEMA,'complete':host_complete,'items':[
        {'id':'request','kind':'request_text','sha256':sha},
        {'id':'reference','kind':'reference_image','sha256':hashlib.sha256(b'explicit isolated reference bytes').hexdigest()}]}
    frozen['request_binding'].update(request_sha256=sha,request_envelope_sha256='e'*64,input_inventory=inventory)
    if has_value:
        row=next(row for row in frozen['semantic_assertions'] if row['axes']['kind']=='fact')
        row['axes'].update(scope_kinds=[scope_kind],source_input_ids=['reference'])
    # Keep appearance partially open; only the exact existing skin.tone is locked.
    frozen['intent_lock']['locked_dimensions']=[x for x in frozen['intent_lock']['locked_dimensions'] if x!='appearance']
    frozen['intent_lock']['open_dimensions'].append('appearance')
    frozen['intent_lock']['semantic_anchors']=[{'dimension':'appearance','target':'face_A','property':'skin.tone'}] if has_value else []
    facts=e.frozen_witnesses(frozen)['facts']
    items=[{key:row[key] for key in ('assertion_id','dimension','target','property','value')} for row in facts] if state=='known_present' else []
    payload={'schema':e.witnesses.SCOPE_SCHEMA,'complete':complete,'input_binding':e.witnesses.input_binding(frozen['request_binding']),
        'reviewed_input_ids':[item['id'] for item in inventory['items']],'state':state,'items':items}
    frozen['semantic_assertions'].append(assertion('scope','scope_inventory',owner=owner,scope_kind=scope_kind,
        inventory=e.witnesses.canonical(payload)))
    return frozen


class NativeV4GuardTests(unittest.TestCase):
    def entries(self,data,**kwargs):
        c.validate(data)
        return [c.entry(data,A,realization_id='base',**kwargs),
                c.entry({**data,'candidates':{**data['candidates'],A:layout.guard_record(data['candidates'][A],data)}},A,realization_id='base',**kwargs)]

    def test_known_absence_present_and_unknown_remain_distinct_in_full_compact(self):
        data=guarded([preserve()])
        absent=scoped_core('known_absent',has_value=False)
        present=scoped_core()
        for entry in self.entries(data):
            for frozen,state in [(absent,'known_absent'),(present,'known_present')]:
                result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result)
                self.assertEqual(result['native_guards']['rules'][0]['state'],state)
                self.assertEqual(result['resolved_frozen_facts'],[])
            for frozen in [scoped_core('unknown'),scoped_core(complete=False),scoped_core(host_complete=False),core(['actor_A'])]:
                self.assertFalse(e.admission(entry,frozen)['allowed'])
        self.assertEqual(e.frozen_witnesses(absent)['facts'],[])

    def test_present_inventory_input_binding_completeness_value_and_owner_are_exact(self):
        data=guarded([preserve()]);entry=self.entries(data)[0]
        for defect in ['input_hash','reviewed_inputs','missing_item','item_value','item_owner','wrong_owner','missing_host','no_lock','advisory']:
            frozen=scoped_core();row=frozen['semantic_assertions'][-1];payload=json.loads(row['axes']['inventory'])
            if defect=='input_hash':payload['input_binding']['input_inventory_sha256']='0'*64
            elif defect=='reviewed_inputs':payload['reviewed_input_ids'].pop()
            elif defect=='missing_item':payload['items']=[]
            elif defect=='item_value':payload['items'][0]['value']['value']='red'
            elif defect=='item_owner':payload['items'][0]['target']='actor_B'
            elif defect=='wrong_owner':row['axes']['owner']='actor_B'
            elif defect=='missing_host':frozen['request_binding'].pop('input_inventory')
            elif defect=='no_lock':frozen['intent_lock']['semantic_anchors']=[]
            else:row['polarity']='advisory'
            row['axes']['inventory']=e.witnesses.canonical(payload)
            with self.subTest(defect=defect):self.assertFalse(e.admission(entry,frozen)['allowed'])
        frozen=scoped_core();frozen['semantic_assertions'][-1]['axes']['inventory']=' '+frozen['semantic_assertions'][-1]['axes']['inventory']
        self.assertRaises(ValueError,e.frozen_witnesses,frozen)

    def test_same_value_and_receiver_mutations_cannot_bypass_preservation(self):
        frozen=scoped_core()
        for data in [guarded([preserve()],prop='skin.tone',target='face',role='primary_face'),
                     guarded([preserve()],prop='skin.tone',target='image',role='image',receivers=['face'])]:
            for entry in self.entries(data):
                result=e.admission(entry,frozen)
                self.assertFalse(result['allowed']);self.assertEqual(result['reason'],'native_established_scope_effect_overlap')
        # A different explicit property on the same face remains available.
        data=guarded([preserve()],prop='wardrobe.neckline',target='face',role='primary_face')
        for entry in self.entries(data):self.assertTrue(e.admission(entry,frozen)['allowed'])

    def test_optional_dependency_adds_only_selected_effect_and_guard_conjunction(self):
        data=guarded([preserve()]);child=guarded([dict(id='child_value',kind='frozen_value',owner_role='primary_face',
            dimension='appearance',property='skin.tone',value={'type':'skin.tone/v1','value':'ivory'})],
            prop='skin.tone',target='face',role='primary_face')
        child_record=copy.deepcopy(child['candidates'][A]);child_record['id']=B
        data['slot_catalog']['child_role']=copy.deepcopy(child['slot_catalog']['test_role']);data['slot_catalog']['child_role']['id']='child_role'
        data['candidates'][B]=child_record;child_record['content']['role_evidence']['roles']={}
        seal(data,{'child_role':['effect']},cid=B)
        parent=data['candidates'][A];parent['record_kind']='visual_bundle'
        parent['content']['member_candidates']=[{'candidate_id':B,'adoption':'optional','requirements':{}}]
        dependencies(data,A,'base',[B]);parent['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
        seal(data,{'test_role':['effect']});frozen=scoped_core()
        for entry in self.entries(data):self.assertTrue(e.admission(entry,frozen)['allowed'])
        for entry in self.entries(data,dependency_selections={B:'base'}):
            self.assertFalse(e.admission(entry,frozen)['allowed'])
        # An explicit member condition is conjunctive even without a binding ID.
        parent['content']['member_candidates'][0]['conditions']={'native_guards':block(dict(id='wrong_value',kind='frozen_value',
            owner_role='primary_face',dimension='appearance',property='skin.tone',value={'type':'skin.tone/v1','value':'red'}))}
        seal(data,{'test_role':['effect']})
        for entry in self.entries(data):self.assertTrue(e.admission(entry,frozen)['allowed'])
        for entry in self.entries(data,dependency_selections={B:'base'}):self.assertFalse(e.admission(entry,frozen)['allowed'])

    def test_child_preserve_guard_sees_parent_effect_even_without_child_property_overlap(self):
        data=guarded([],prop='skin.tone',target='face',role='primary_face')
        child=guarded([preserve()]);child_record=copy.deepcopy(child['candidates'][A]);child_record['id']=B
        data['candidates'][B]=child_record
        data['slot_catalog']['child_pose']=copy.deepcopy(child['slot_catalog']['test_role']);data['slot_catalog']['child_pose']['id']='child_pose'
        child_record['content']['role_evidence']['roles']={};seal(data,{'child_pose':['effect']},cid=B)
        parent=data['candidates'][A];parent['record_kind']='visual_bundle'
        parent['content']['member_candidates']=[{'candidate_id':B,'adoption':'optional','requirements':{}}]
        dependencies(data,A,'base',[B]);parent['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
        seal(data,{'test_role':['effect']});frozen=scoped_core()
        for entry in self.entries(data):self.assertTrue(e.admission(entry,frozen)['allowed'])
        for entry in self.entries(data,dependency_selections={B:'base'}):self.assertFalse(e.admission(entry,frozen)['allowed'])

    def test_typed_relation_frozen_value_and_entity_owner_value_need_exact_witnesses(self):
        rules=[dict(id='part',kind='owner_relation',relation='part_of',left_role='primary_face',right_role='main_subject'),
               dict(id='different',kind='owner_relation',relation='disjoint',left_role='main_subject',right_role='secondary_subject'),
               dict(id='value',kind='frozen_value',owner_role='primary_face',dimension='appearance',property='skin.tone',
                    value={'type':'skin.tone/v1','value':'ivory'}),
               dict(id='relation',kind='frozen_entity_relation',left_role='main_subject',right_role='secondary_subject',
                    dimension='relationship',property='relationship.peer_to',value_type='entity.owner_id/v1')]
        frozen=scoped_core();row=assertion('entity_relation','fact',dimension='relationship',owner='actor_A',
            property='relationship.peer_to',value_type='entity.owner_id/v1',value='actor_B')
        frozen['semantic_assertions'].append(row);frozen['intent_lock']['locked_dimensions'].append('relationship')
        data=guarded(rules)
        for entry in self.entries(data):self.assertTrue(e.admission(entry,frozen)['allowed'])
        for defect in ['part','disjoint','value','relation','role']:
            bad=copy.deepcopy(frozen)
            if defect in {'part','disjoint'}:
                bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['axes'].get('kind')!=('part_of' if defect=='part' else 'disjoint')]
                # The reference scope itself also correctly denies an unowned part.
                bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['axes'].get('kind')!='scope_inventory']
                for x in bad['semantic_assertions']:
                    x['axes'].pop('scope_kinds',None);x['axes'].pop('source_input_ids',None)
            elif defect=='value':next(x for x in bad['semantic_assertions'] if x['axes'].get('property')=='skin.tone')['axes']['value']='red'
            elif defect=='relation':bad['semantic_assertions'][-1]['axes']['value']='image_A'
            else:bad['semantic_assertions']=[x for x in bad['semantic_assertions'] if x['axes'].get('role')!='secondary_subject']
            with self.subTest(defect=defect):self.assertFalse(e.admission(c.entry(data,A,realization_id='base'),bad)['allowed'])

    def test_intrinsic_selected_and_presentation_conditions_are_anded_and_compact_sealed(self):
        good=dict(id='good',kind='frozen_value',owner_role='primary_face',dimension='appearance',property='skin.tone',
                  value={'type':'skin.tone/v1','value':'ivory'})
        bad={**good,'id':'bad','value':{'type':'skin.tone/v1','value':'red'}}
        data=guarded([good]);rec=data['candidates'][A];p=rec['content']['role_evidence']
        rec['effects']['realizations']={'mode':'one','branches':[dict(id='chosen',conditions={'native_guards':block(bad)},
            context_terms=[],effects={'dimensions':[],'properties':[]})]}
        p['facts'][0]['realization_id']='chosen';p['owner_maps']={'chosen':p['owner_maps']['base']}
        seal(data,{'test_role':['effect']});c.validate(data)
        self.assertFalse(e.admission(c.entry(data,A,realization_id='chosen'),scoped_core())['allowed'])
        rec['effects']['realizations']['branches'][0]['conditions']={'native_guards':block(good)}
        seal(data,{'test_role':['effect']});bid='bind_'+'d'*32
        data['slot_bindings'][bid]=dict(id=bid,candidate_id=A,slot_id='test_role',role='optional',semantic_role='direct',weight=1,
            conditions={'subject_applicability':{},'native_guards':block(bad)})
        c.validate(data)
        self.assertFalse(e.admission(c.entry(data,A,bid,realization_id='chosen'),scoped_core())['allowed'])
        entry=c.entry(data,A,realization_id='chosen');self.assertTrue(e.admission(entry,scoped_core())['allowed'])
        entry['_semantic_evidence_guard']['guard_sets']['chosen']['source_conditions']=[{},{}]
        self.assertFalse(e.admission(entry,scoped_core())['allowed'])

    def test_final_scope_preservation_requires_exact_owner_value_and_literal_phrase(self):
        data=guarded([preserve()]);frozen=scoped_core();entry=c.entry(data,A,realization_id='base')
        result=e.admission(entry,frozen);self.assertTrue(result['allowed'])
        item=e.frozen_witnesses(frozen)['scope_inventories'][0]['inventory']['items'][0]
        phrase='The same ivory skin tone is preserved.'
        interpretation={'scope_preservation_evidence':{'scope':{item['assertion_id']:{'owner':item['target'],
            'value':item['value'],'prompt_evidence':phrase}}}}
        e.audit_scope_preservation(result,interpretation,phrase)
        for defect in ['missing','value','owner','phrase','extra']:
            bad=copy.deepcopy(interpretation)
            if defect=='missing':bad={}
            elif defect=='extra':bad['scope_preservation_evidence']['foreign']={}
            else:bad['scope_preservation_evidence']['scope'][item['assertion_id']][{'value':'value','owner':'owner','phrase':'prompt_evidence'}[defect]]=({'type':'skin.tone/v1','value':'red'} if defect=='value' else 'other')
            with self.subTest(defect=defect):self.assertRaises(ValueError,e.audit_scope_preservation,result,bad,phrase)
        pack={'authorial_core':frozen};composed={'chosen_candidate_ids':[A],'candidate_interpretations':[{'candidate_id':A,'realization_id':'base',**interpretation}],'prompt_en':phrase}
        with mock.patch.object(g,'frozen_core_context',return_value=({'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}})):
            self.assertEqual(audit.audit_native_adoptions(pack,composed,data),[])
            composed['candidate_interpretations'][0].pop('scope_preservation_evidence')
            self.assertTrue(audit.audit_native_adoptions(pack,composed,data))


class NativeV4WireTests(unittest.TestCase):
    def inputs(self):
        helper=wire_fixture.NativeFactWireTests();raw=helper.inputs()
        request=json.loads((FIXTURE/'request-envelope.json').read_text())
        inventory={'schema':e.witnesses.INPUT_SCHEMA,'complete':True,'items':[
            {'id':'request','kind':'request_text','sha256':request['request_sha256']}]}
        envelope=wire.normalize_request_envelope({**request,'input_inventory':inventory})
        linen=next(row for row in raw['semantic_assertions'] if row['assertion_id']=='blanket_material')
        linen['axes'].update(scope_kinds=['requester_identity'],source_input_ids=['request'])
        item={'assertion_id':'blanket_material','dimension':'material','target':'main_subject',
              'property':'surface.material','value':{'type':'surface.material/v1','value':'linen'}}
        payload={'schema':e.witnesses.SCOPE_SCHEMA,'complete':True,'input_binding':e.witnesses.input_binding(envelope),
            'reviewed_input_ids':['request'],'state':'known_present','items':[item]}
        row=assertion('declared_material_scope','scope_inventory',owner='main_subject',scope_kind='requester_identity',
                      inventory=e.witnesses.canonical(payload))
        row['source_span_ids']=['topic'];row['evidence']={'material':'linen blanket'}
        raw['semantic_assertions'].append(row)
        return helper,raw,inventory

    def test_explicit_caller_input_inventory_freeze_independent_audit_and_replay(self):
        helper,raw,inventory=self.inputs()
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp);run,args=helper.freeze(directory,raw,input_inventory=inventory)
            state=files.load_state(run);envelope,frozen,controls=files.verify_freeze(state)
            self.assertEqual(envelope['input_inventory'],inventory)
            self.assertEqual(frozen['request_binding']['input_inventory'],inventory)
            self.assertEqual(frozen['semantic_assertions'][-1]['axes']['inventory'],raw['semantic_assertions'][-1]['axes']['inventory'])
            self.assertTrue(audit.authorial_core_intent_contract_valid(frozen,creative_control_snapshot=controls))
            self.assertTrue(audit.authorial_core_v3_semantic_contract_valid(frozen,creative_control_snapshot=controls))
            self.assertTrue(preparation.freeze(args)['reused'])
            replay=g.normalize_authorial_core(files.value(state,'authorial_core_input'),request_envelope=envelope,creative_control_snapshot=controls)
            self.assertEqual(replay['canonical_sha256'],frozen['canonical_sha256'])
            self.assertEqual(e.frozen_witnesses(replay),e.frozen_witnesses(frozen))
            bad=copy.deepcopy(frozen);bad['request_binding']['input_inventory']['items'][0]['kind']='text'
            self.assertFalse(audit.authorial_core_intent_contract_valid(bad,creative_control_snapshot=controls))
            self.assertRaises(ValueError,e.frozen_witnesses,bad)
            # Native admission consumes this exact independently frozen identity
            # scope from text, even though there is no reference image entry.
            row=fact('side','lighting','main_subject','lighting.direction','effect','side',[],operation='set_value',receivers=[])
            data=source('A declared linen blanket receives side light.',[row],
                {'light_direction':slot('light_direction',['lighting'],property_prefixes=['lighting.direction'])},
                {'base':owner_map(('main_subject','main_subject'))})
            data['candidates'][A]['conditions']={'native_guards':block(preserve('requester_identity'))}
            seal(data,{'light_direction':['side']});c.validate(data)
            for view in [data,{**data,'candidates':{A:layout.guard_record(data['candidates'][A],data)}}]:
                receipt=e.admission(c.entry(view,A,realization_id='base'),frozen)
                self.assertTrue(receipt['allowed'],receipt)
                self.assertEqual(receipt['native_guards']['preserved_scopes'][0]['inventory']['state'],'known_present')

    def test_no_inventory_default_and_noncanonical_scope_axes_are_rejected(self):
        helper,raw,inventory=self.inputs()
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp)
            with self.assertRaises(ValueError):helper.freeze(directory,raw)
        raw['semantic_assertions'][-1]['axes']['inventory']=json.loads(raw['semantic_assertions'][-1]['axes']['inventory'])
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):helper.freeze(Path(temp),raw,input_inventory=inventory)
        with self.assertRaises(ValueError):e.witnesses.validate_input_inventory(
            {'schema':e.witnesses.INPUT_SCHEMA,'complete':True,'items':[]},'a'*64)


def profile_source():
    """Manually authored two-choice source; helper presence is selected-only.

    Repeated source phrases repeat explicit fixture facts at their exact paths.
    This serialization does not classify or convert any corpus source judgement.
    """
    side='Side light grazes the declared linen surface from the left.'
    helper='An already declared helper stands beside the existing subject.'
    common={'contract_version':'photo-authored-visual-components/v2',
        'components':[{'id':'side_light','match_terms':['lateral illumination']}],
        'discovery':{'minimum_component_groups':1,'required_group_ids':['side_light']},
        'obligations':[{'component_ids':['side_light'],
            'evidence':[{'field':'side_light_phrase','requirement':{'min_content_words':4,'must_mention_any':['side light']}}],
            'instruction':side,'render_gates':[{'id':'vo_side_light','review_scale':'both','description':side}]}]}
    choices={}
    for rid in ['alone','helper']:
        ac=copy.deepcopy(common)
        if rid=='helper':ac['obligations'].append({'component_ids':['side_light'],
            'evidence':[{'field':'helper_phrase','requirement':{'min_content_words':4,'must_mention_any':['helper']}}],
            'instruction':helper,'render_gates':[{'id':'vo_helper','review_scale':'both','description':helper}]})
        choices[rid]={'en':side if rid=='alone' else side+' '+helper,'ko':side,
            'embedding_text':side,'concept_units':[side]+([helper] if rid=='helper' else []),'relations':[],
            'authored_components':ac,'semantics':{'definition':side,'paraphrase_examples':[side]}}
    data=source(side,[],{'light_direction':slot('light_direction',['lighting'],property_prefixes=['lighting.direction'])},
        {rid:owner_map(('surface','main_subject'),*([('helper','secondary_subject')] if rid=='helper' else [])) for rid in choices},
        effects={'dimensions':['lighting'],'properties':[{'dimension':'lighting','target':'surface','property':'lighting.direction'}],
                 'realizations':{'mode':'one','branches':[{'id':rid,'conditions':{},'context_terms':[],
                    'effects':{'dimensions':[],'properties':[]},'concept_units':choices[rid]['concept_units']} for rid in choices]}})
    rec=data['candidates'][A];rec['record_kind']='visual_profile';rec['content'].update(
        authored_components=common,semantics={'definition':side,'paraphrase_examples':[side]},
        realization_content=choices,activation={'exact_terms':['lateral illumination'],'project_glossary_aliases':[]},
        concept_candidate={'concept_terms':['lateral illumination'],'affected_dimensions':['lighting'],
            'affected_properties':[{'dimension':'lighting','target':'surface','property':'lighting.direction'}]})
    p=rec['content']['role_evidence'];supports=[]
    for rid in choices:
        for path in sorted(e.primary_paths(rec,rid)):
            text=e.positive_string(rec,path,realization_id=rid)
            # Every semantic fixture clause has an explicit declared mode/value.
            if side in text:
                fid=f'side_{len(p["facts"])}';supports.append(fid)
                p['facts'].append(fact(fid,'lighting','surface','lighting.direction','effect','side',[],rid=rid,
                    pointer=path,quote=side,operation='set_value',receivers=[]))
            if helper in text:
                p['facts'].append(fact(f'helper_{len(p["facts"])}','subject','helper','entity.presence',
                    'prerequisite','present',[],rid=rid,pointer=path,quote=helper))
            if text not in {'both'} and side not in text and helper not in text:
                raise AssertionError('fixture semantic clause must have an explicit judgement: '+text)
    return seal(data,{'light_direction':supports})


class NativeV4ProfileTests(unittest.TestCase):
    def views(self,data):
        return [data,{**data,'candidates':{A:layout.guard_record(data['candidates'][A],data)}}]

    def test_selected_seven_field_projection_obligation_and_helper_are_exact(self):
        data=profile_source();c.validate(data)
        frozen=core(['main_subject']);with_helper=core(['main_subject','actor_B'],
            [('subject','actor_B','entity.presence','present')],[('disjoint','main_subject','actor_B')])
        for view in self.views(data):
            alone=c.entry(view,A,realization_id='alone');helper=c.entry(view,A,realization_id='helper')
            self.assertTrue(e.admission(alone,frozen)['allowed'])
            self.assertFalse(e.admission(helper,frozen)['allowed'])
            self.assertTrue(e.admission(helper,with_helper)['allowed'])
            for selected,fields in [(alone,['side_light_phrase']),(helper,['side_light_phrase','helper_phrase'])]:
                obligation=g.candidate_pack_visual_profile_obligation(selected,{},activation_source='native_actual_realization',source_intent_ids=[])
                self.assertEqual(obligation['prompt_binding']['required_evidence_fields'],fields)
                self.assertEqual(obligation['native_profile_contract'],selected['_selected_profile_contract'])
                self.assertEqual(selected['_selected_profile_contract']['compiled_sha256'],c.digest(r.compiled_profile_material(selected)))
            self.assertNotIn('helper',alone['en']);self.assertNotIn('helper_phrase',alone['evidence_requirements'])
        self.assertEqual(c.entry(data,A,realization_id='helper')['_selected_profile_contract'],
            c.entry(self.views(data)[1],A,realization_id='helper')['_selected_profile_contract'])
        self.assertRaises(ValueError,g.candidate_pack_visual_profile_obligation,c.entry(data,A),{},activation_source='x',source_intent_ids=[])

    def test_positive_leakage_and_common_discovery_evidence_replacement_are_rejected(self):
        for defect in ['extra_field','semantics','components','discovery','common_obligation','branch','unprojected','stale_compile','v3']:
            data=profile_source();rec=data['candidates'][A];selected=rec['content']['realization_content']['alone']
            if defect=='extra_field':selected['definition']='foreign'
            elif defect=='semantics':selected['semantics']['semantic_caption']='foreign'
            elif defect=='components':selected['authored_components']['components'][0]['match_terms']=['foreign']
            elif defect=='discovery':selected['authored_components']['discovery']['required_group_ids']=[]
            elif defect=='common_obligation':selected['authored_components']['obligations'][0]['instruction']='A replacement source adds a different positive duty.'
            elif defect=='branch':rec['effects']['realizations']['branches'][0]['concept_units']=['foreign']
            elif defect=='unprojected':rec['content']['composition_instruction']='Unselected helper appears in every shared view.'
            elif defect=='v3':rec['content']['role_evidence']['schema']='photo-candidate-role-evidence/v3'
            else:rec['content']['role_evidence']['profile_contracts']['alone']['compiled_sha256']='0'*64;reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)

    def test_final_selected_only_literal_evidence_and_render_contract(self):
        import photo_native_pack as packs
        data=profile_source();entry=c.entry(data,A,realization_id='alone')
        contract=entry['_selected_profile_contract'];phrase=entry['en']
        interpretation={'candidate_id':A,'realization_id':'alone','selected_profile_contract':contract,
            'selected_profile_evidence':{'side_light_phrase':phrase}}
        audit.audit_selected_native_profile(entry,interpretation,phrase)
        for defect in ['contract','rid','missing','extra','phrase']:
            bad=copy.deepcopy(interpretation)
            if defect=='contract':bad['selected_profile_contract']['meaning_sha256']='0'*64
            elif defect=='rid':bad['selected_profile_contract']['realization_id']='helper'
            elif defect=='missing':bad['selected_profile_evidence']={}
            elif defect=='extra':bad['selected_profile_evidence']['helper_phrase']='A helper stands nearby.'
            else:bad['selected_profile_evidence']['side_light_phrase']='not in final prompt'
            with self.subTest(defect=defect):self.assertRaises(ValueError,audit.audit_selected_native_profile,entry,bad,phrase)
        choice=self.choices(data,core(['main_subject']))
        pack={'contract_version':packs.CONTRACT,'candidate_pool':{A:{'id':A,'authored_record':data['candidates'][A]}},
            'role_proposals':{},'role_views':{},'native_profile_choices':choice,'authorial_core':core(['main_subject'])}
        composed={'chosen_candidate_ids':[A],'candidate_interpretations':[interpretation],'prompt_en':phrase}
        effective,failures=audit.derive_effective_visual_obligation_contract(pack,composed)
        self.assertEqual(failures,[]);self.assertEqual(effective['required_hard_gates'],['vo_side_light'])
        self.assertEqual(audit.audit_visual_obligations(pack,composed,phrase),[])
        self.assertEqual(audit.derive_effective_visual_obligation_contract(pack,{'chosen_candidate_ids':[]})[0],None)
        audit.audit_native_profile_choices(pack,composed,data,{A},{A:interpretation})
        choice['profiles'][0]['required']=True
        self.assertRaises(ValueError,audit.audit_native_profile_choices,pack,{},data,set(),{})
        self.assertTrue(audit.derive_effective_visual_obligation_contract(pack,{'chosen_candidate_ids':[]})[1])

    def choices(self,data,frozen,required=False):
        runtime={**data,g.VISUAL_OBLIGATIONS_DATA_KEY:{'profiles':[c.entry(data,A)]}}
        result={'provenance':{'authorial_core':frozen,'creative_controls':{},'global_candidate_ids':[A]}}
        resolution={'hits':[{'profile_id':A,'match_basis':'exact' if required else 'global_bm25f+embedding',
                             'hard_eligible':required,'optional_eligible':True}]}
        with mock.patch.object(g,'frozen_core_context',return_value=({'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}})):
            return g.candidate_pack_native_profile_choices(runtime,result,{},resolution)

    def test_malformed_profile_choice_and_guard_shapes_fail_as_bounded_contract_errors(self):
        data=profile_source();choice=self.choices(data,core(['main_subject']))
        for defect in ['container','profile','choice','qualification','obligation']:
            value=copy.deepcopy(choice)
            if defect=='container':value=True
            elif defect=='profile':value['profiles'][0]['unknown']=True
            elif defect=='choice':value['profiles'][0]['choices'][0]['unknown']=True
            elif defect=='qualification':value['profiles'][0]['choices'][0]['qualification']=[]
            else:value['profiles'][0]['choices'][0]['obligation']=[]
            with self.subTest(defect=defect):self.assertRaises(ValueError,audit.native_profile_choice_rows,{'native_profile_choices':value})
        for field in ['owner_role','scope_kind']:
            rule=preserve();rule[field]=[]
            with self.subTest(field=field):self.assertRaises(ValueError,e.validate_source_guards,block(rule))
        for text in ['{"x":1,"x":2}','{"x":NaN}',' {"x":1}','{"x": 1}']:
            with self.subTest(json=text):self.assertRaises(ValueError,e.witnesses.decode_inventory,text)

    def test_lazy_materialized_choices_preserve_only_eligible_actual_rids(self):
        from tests import test_photo_global_retrieval as retrieval_fixture
        from photo_search_reader import SearchReader,LazyRuntimeData
        import photo_shared_views as views
        import photo_global_index as index
        data=profile_source();data['policies']=views.source(retrieval_fixture.GlobalDiscoveryTests().data())['policies']
        data['policies']['visual_profile_refs']=[A]
        vectors={'schema':index.SCHEMA,'space':index.SPACE,'query_recipe':index.QUERY_RECIPE,
                 'corpus_sha256':c.digest(data),'entries':{}}
        recipe,text=index.text(data['candidates'][A]);vectors['entries'][A]={'id':A,'recipe':recipe,'text':text,
            'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':[1.0]+[0.0]*767}
        frozen=core(['main_subject'])
        with tempfile.TemporaryDirectory() as temp:
            assets=Path(temp);layout.build(assets,data,vectors,activate=True)
            reader=SearchReader(assets);lazy=LazyRuntimeData(reader).for_core(frozen).presentations([A])
            materialized=views.assemble(data,vectors)
            for runtime in [lazy,materialized]:
                choices=self.choices(runtime,frozen)
                self.assertEqual([row['realization_id'] for row in choices['profiles'][0]['choices']],['alone'])
                self.assertEqual(choices['profiles'][0]['choices'][0]['obligation']['native_profile_contract'],
                    c.entry(data,A,realization_id='alone')['_selected_profile_contract'])
            self.assertEqual(e.admission(c.entry(lazy['_guard_source'],A,realization_id='alone'),frozen),
                             e.admission(c.entry(materialized,A,realization_id='alone'),frozen))
            reader.close()

class NativeV4CompletePackTests(unittest.TestCase):
    def test_real_frozen_core_lazy_search_public_pack_composed_and_gate_projection(self):
        from tests import test_photo_native_adoption as adoption_fixture
        data=profile_source()
        with tempfile.TemporaryDirectory() as temp,mock.patch.object(adoption_fixture,'lighting_source',return_value=data):
            pack,composed,runtime,context=adoption_fixture.NativeFinalAdoptionTests().full_pack(Path(temp))
            choices=pack['native_profile_choices']['profiles'][0]['choices']
            self.assertEqual([row['realization_id'] for row in choices],['alone'])
            self.assertEqual(set(pack['candidate_pool'][A]['realization_views']),{'alone'})
            selected=c.entry(runtime,A,realization_id='alone')
            rows=composed['candidate_interpretations']+[row for row in composed['creative_augmentation_brief']['decisions']
                if row.get('candidate_id')==A and row.get('decision')=='transformed']
            for row in rows:row.update(realization_id='alone',affected_properties=copy.deepcopy(selected['affected_properties']),selected_profile_contract=selected['_selected_profile_contract'],
                selected_profile_evidence={'side_light_phrase':'Side light grazes the pale linen folds from the left.'})
            report=audit.audit_composed_prompt(pack,composed,source_data=runtime,query_context=context)
            self.assertEqual(report['status'],'pass',report)
            effective,failures=audit.derive_effective_visual_obligation_contract(pack,composed)
            self.assertEqual(failures,[]);self.assertEqual(effective['required_hard_gates'],['vo_side_light'])
            self.assertEqual(effective['obligations'][0]['native_profile_contract'],selected['_selected_profile_contract'])
            rows[0]['realization_id']='helper'
            self.assertTrue(audit.audit_native_adoptions(pack,composed,runtime))
            runtime.reader.close()

    def test_actual_request_hard_activation_cannot_drop_or_downgrade_profile_choices(self):
        from tests import test_photo_native_adoption as adoption_fixture
        data=profile_source();data['candidates'][A]['content']['activation']['exact_terms']=['linen blanket']
        seal(data,{'light_direction':data['candidates'][A]['content']['role_evidence']['roles']['light_direction']['fact_refs']})
        with tempfile.TemporaryDirectory() as temp,mock.patch.object(adoption_fixture,'lighting_source',return_value=data):
            pack,composed,runtime,context=adoption_fixture.NativeFinalAdoptionTests().full_pack(Path(temp))
            self.assertTrue(pack['native_profile_choices']['profiles'][0]['required'])
            self.assertTrue(audit.audit_native_adoptions(pack,{'chosen_candidate_ids':[]},runtime))
            for defect in ['drop','downgrade','empty','stale','foreign']:
                bad=copy.deepcopy(pack)
                if defect=='drop':bad.pop('native_profile_choices')
                elif defect=='downgrade':bad['native_profile_choices']['profiles'][0]['required']=False
                elif defect=='empty':bad['native_profile_choices']['profiles']=[]
                elif defect=='stale':bad['native_profile_choices']['profiles'][0]['source_record_sha256']='0'*64
                else:bad['native_profile_choices']['profiles'][0]['choices'][0]['realization_id']='helper'
                with self.subTest(defect=defect):
                    self.assertTrue(audit.audit_native_adoptions(bad,{'chosen_candidate_ids':[A],
                        'candidate_interpretations':[{'candidate_id':A,'realization_id':'alone'}]},runtime))
            runtime.reader.close()


class NativeV4BoundsTests(unittest.TestCase):
    def test_actual_rid_limit_32_accepts_and_33_rejects_without_default_or_truncation(self):
        def fixture(count):
            text='The existing actor assumes a standing pose.'
            ids=['choice_'+str(i) for i in range(count)]
            data=source(text,[fact('pose_'+rid,'pose','actor','pose.standing','effect','standing',[],rid=rid,
                operation='set_value',receivers=[]) for rid in ids],
                {'pose':slot('pose',['pose'],property_prefixes=['pose.standing'])},
                {rid:owner_map(('actor','main_subject')) for rid in ids},
                effects={'dimensions':['pose'],'properties':[{'dimension':'pose','target':'actor','property':'pose.standing'}],
                    'realizations':{'mode':'one','branches':[{'id':rid,'conditions':{},'context_terms':[],
                        'effects':{'dimensions':[],'properties':[]}} for rid in ids]}})
            return seal(data,{'pose':['pose_'+rid for rid in ids]})
        valid=fixture(32);c.validate(valid);self.assertEqual(len(r.ids(valid['candidates'][A])),32)
        self.assertRaises(ValueError,c.validate,fixture(33))
        optional=copy.deepcopy(valid['candidates'][A]['effects']);optional['realizations']['mode']='optional'
        self.assertRaises(ValueError,c.validate_effects,optional,'optional_33_actual')
        optional['realizations']['branches'].pop();c.validate_effects(optional,'optional_32_actual')
        self.assertEqual(e.MAX_REALIZATIONS,32);self.assertEqual(e.witnesses.MAX_ROWS,64);self.assertEqual(e.witnesses.MAX_OWNERS,32)

    def test_source_unit_and_fact_limits_are_complete_not_truncated(self):
        text='The existing actor assumes a standing pose.'
        for label,count,extra in [('units',2048,2049),('facts',4096,4097)]:
            with self.subTest(limit=label):
                rows=[fact('pose_'+str(i),'pose','actor','pose.standing','effect','standing',[],
                    operation='set_value',receivers=[],pointer=('/content/en' if i==0 or label=='facts'
                        else '/content/manifestations/'+str(i-1))) for i in range(count)]
                data=source(text,rows,{'pose':slot('pose',['pose'],property_prefixes=['pose.standing'])},
                            {'base':owner_map(('actor','main_subject'))},effects={'dimensions':['pose'],
                                'properties':[{'dimension':'pose','target':'actor','property':'pose.standing'}]})
                if label=='units':data['candidates'][A]['content']['manifestations']=[text]*(count-1)
                seal(data,{'pose':[row['id'] for row in rows]});c.validate(data)
                proof=data['candidates'][A]['content']['role_evidence']
                self.assertEqual(len(proof['source_units'] if label=='units' else proof['facts']),count)
                self.assertEqual(len(e.compact(data['candidates'][A],data)['facts']),count)
                if label=='units':
                    data['candidates'][A]['content']['manifestations'].append(text)
                    new=fact('overflow','pose','actor','pose.standing','effect','standing',[],operation='set_value',
                        receivers=[],pointer='/content/manifestations/'+str(count-1),quote=text)
                else:new={**copy.deepcopy(proof['facts'][0]),'id':'overflow'}
                proof['facts'].append(new);seal(data,{'pose':[row['id'] for row in proof['facts']]})
                self.assertEqual(len(proof['source_units'] if label=='units' else proof['facts']),extra)
                self.assertRaises(ValueError,c.validate,data)
