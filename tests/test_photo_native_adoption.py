"""Whole native admission reaches the final independent composed-prompt audit.

All source/role/vector inputs are synthetic fixtures, with no inference or publication.
"""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from tests import test_photo_native_fact_wire as wire_fixture
from tests.test_photo_workflow_precore import FIXTURE, files
from tests.test_photo_semantic_evidence import (A, source, fact, owner_map, seal, core, reviewed_source, face_source, reattest)
from tests.test_photo_native_compound_evidence import bundle, dependencies, B
from tests import test_photo_global_retrieval as retrieval_fixture
from tests.test_photo_slot_queries import synthetic_set
from tests.photo_native_runtime import compose_native
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_semantic_evidence as e
import photo_candidate_realizations as r
import photo_shared_views as views
import photo_search_layout as layout
import photo_global_index as index
from photo_search_reader import SearchReader, LazyRuntimeData
import prompt_generator as g
import audit_composed_prompt as audit


def lighting_source():
    rows=[fact('linen','material','main_subject','surface.material','prerequisite','linen',[],quote='linen'),
        fact('side','lighting','main_subject','lighting.direction','effect','side',['linen'],quote='side light',
            operation='set_value',receivers=[])]
    return seal(source('side light on the already declared linen surface',rows,
        {'light_direction':slot('light_direction',['lighting'],property_prefixes=['lighting.direction'])},
        {'base':owner_map(('main_subject','main_subject'))}),{'light_direction':['side']})


class NativeFinalAdoptionTests(unittest.TestCase):
    def full_pack(self, directory, bundled=False):
        run,_=wire_fixture.NativeFactWireTests().freeze(directory,wire_fixture.NativeFactWireTests().inputs(),control_overrides={'sensual':0,'fetish':0})
        _,frozen,controls=files.verify_freeze(files.load_state(run))
        data=lighting_source();data['policies']=views.source(retrieval_fixture.GlobalDiscoveryTests().data())['policies']
        data['policies']['_quality_layers']={'adult_appeal':{'contextual_retrieval':{'contract_version':'photo-contextual-appeal/v2'}}}
        if bundled:
            child=copy.deepcopy(face_source()['candidates'][A]);child['id']=B
            data['candidates'][B]=child;seal(data,{'light_direction':['underlight']},cid=B)
            record=data['candidates'][A];record['record_kind']='visual_bundle'
            record['content']['member_candidates']=[{'candidate_id':B,'adoption':'optional',
                'presentation_role':'light_direction','requirements':{}}]
            text=record['content']['en'];record['content']['components']=[{'id':'linen_light',
                'concept_units':[text],'minimum_realizations':1}]
            record['content']['role_evidence']['facts'].append(fact('component_side','lighting','main_subject',
                'lighting.direction','effect','side',['linen'],quote='side light',operation='set_value',receivers=[],
                pointer='/content/components/0/concept_units/0'))
            dependencies(data,A,'base',[B]);record['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
            seal(data,{'light_direction':['side']});data['policies']['bundle_refs']=[A]
        recipe,text=index.text(data['candidates'][A]);vectors={'schema':index.SCHEMA,'space':index.SPACE,
            'query_recipe':index.QUERY_RECIPE,'corpus_sha256':c.digest(data),'entries':{}}
        for cid,record in data['candidates'].items():
            recipe,text=index.text(record);vectors['entries'][cid]={'id':cid,'recipe':recipe,'text':text,
                'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':[1.0]+[0.0]*767}
        assets=directory/'synthetic-search';layout.build(assets,data,vectors,activate=True)
        lazy=LazyRuntimeData(SearchReader(assets)).for_core(frozen)
        context=synthetic_set(frozen,controls,data['slot_catalog'],['light_direction'])
        embodiment=json.loads((FIXTURE/'embodiment-review.json').read_bytes())
        pack=g.generate_candidate_pack(lazy,frozen,controls,embodiment,seed=5,query_context=context,requested_slots=['light_direction'])
        composed=compose_native(pack);evidence='Side light grazes the pale linen folds from the left.'
        composed['prompt_en']+=' '+evidence;composed['chosen_candidate_ids']=[A]
        composed['candidate_interpretations']=[{'candidate_id':A,'artistic_interpretation':'Keep the fine folds readable',
            'transformation':'Shape a restrained lateral highlight','prompt_evidence':evidence,
            'affected_properties':[{'dimension':'lighting','target':'main_subject','property':'lighting.direction'}]}]
        if bundled:
            composed['candidate_interpretations'][0].update(component_evidence={'linen_light':evidence},relation_evidence={})
        for decision in composed['creative_augmentation_brief']['decisions']:
            if decision['candidate_id']==A:
                decision.update(composed['candidate_interpretations'][0],decision='transformed',
                    rationale='Integrate the selected lateral light cue.',affected_dimensions=['lighting'])
                composed['candidate_interpretations']=[]
        composed['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
        return pack,composed,lazy,context

    def test_selected_qualified_primitive_passes_real_freeze_search_pack_and_full_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            pack,composed,data,context=self.full_pack(Path(temp))
            report=audit.audit_composed_prompt(pack,composed,source_data=data,query_context=context)
            self.assertEqual(report['status'],'pass',report)

    def test_absent_or_v2_proof_is_never_final_adoption_even_when_discovered(self):
        data=reviewed_source();frozen=core(['main_subject']);pack={'authorial_core':frozen,'creative_controls':{}}
        for proof in [None,{'schema':'photo-candidate-role-evidence/v2','complete':True}]:
            selected=copy.deepcopy(data)
            if proof is None:selected['candidates'][A]['content'].pop('role_evidence')
            else:selected['candidates'][A]['content']['role_evidence']=proof
            failures=audit.audit_native_adoptions(pack,{'chosen_candidate_ids':[A]},selected)
            self.assertTrue(failures);self.assertEqual(failures[0]['check'],'native_candidate_adoption')
        self.assertEqual(audit.audit_native_adoptions(pack,{'chosen_candidate_ids':[]},data),[])

    def test_full_audit_hook_reports_native_failure_with_otherwise_identical_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            pack,composed,data,context=self.full_pack(Path(temp))
            source={key:copy.deepcopy(data[key]) for key in c.CORPUS_FIELDS}
            source['candidates'][A]['content'].pop('role_evidence')
            report=audit.audit_composed_prompt(pack,composed,source_data=source,query_context=context)
            self.assertEqual(report['status'],'fail')
            self.assertTrue(any(row['check']=='native_candidate_adoption' for row in report['failures']))

    def test_optional_member_never_defaults_to_adopted_or_inherits_its_face(self):
        data=bundle();parent=data['candidates'][A];parent['content']['member_candidates'][0]['adoption']='optional'
        proof=parent['content']['role_evidence'];proof['dependencies']['base'][0]['selection']='explicit_optional'
        seal(data,{'surface_material':['satin']});c.validate(data)
        absent=core(['main_subject']);selected=core(['main_subject','face_A'],[('subject','face_A','anatomy.face.presence','present')])
        for record in [parent,layout.guard_record(parent,data)]:
            view={**data,'candidates':{**data['candidates'],A:record}}
            entry=c.entry(view,A,realization_id='base')
            self.assertTrue(e.admission(entry,absent)['allowed'])
            self.assertEqual(e.permission_scope(entry,absent)[0],['material'])
            self.assertEqual(e.effect_closure(A,e.proof_of(entry),'base',{})[0]['candidate_id'],A)
            self.assertEqual(len(e.effect_closure(A,e.proof_of(entry),'base',{})),1)
            entry=c.entry(view,A,realization_id='base',dependency_selections={B:'base'})
            self.assertFalse(e.admission(entry,absent)['allowed']);self.assertTrue(e.admission(entry,selected)['allowed'])
            self.assertEqual(e.permission_scope(entry,selected)[0],['lighting','material'])
        # Complete source facts remain mandatory even when all optional members are omitted.
        proof['facts']=[];proof['roles']={};reattest(data)
        self.assertRaises(ValueError,c.validate,data)

    def test_candidate_only_required_member_and_explicit_old_binding_conditions_are_anded(self):
        data=bundle();frozen=core(['main_subject','face_A'],[('subject','face_A','anatomy.face.presence','present')])
        contract,picked={'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}}
        self.assertEqual(r.eligible_ids(data,A,frozen,contract,picked),['base'])
        bid='bind_'+'e'*32;data['slot_bindings'][bid]={'id':bid,'candidate_id':B,'slot_id':'light_direction',
            'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{'subject_categories':['human']}},'weight':1}
        data['candidates'][A]['content']['member_candidates'][0]['binding_id']=bid
        seal(data,{'surface_material':['satin']});c.validate(data)
        self.assertEqual(r.eligible_ids(data,A,frozen,contract,picked),[])
        original_guard_hash=data['candidates'][A]['content']['role_evidence']['reference_sha256'][bid]
        data['slot_bindings'][bid]['conditions']={'subject_applicability':{}}
        self.assertRaises(ValueError,c.validate,data)
        seal(data,{'surface_material':['satin']});c.validate(data)
        self.assertNotEqual(data['candidates'][A]['content']['role_evidence']['reference_sha256'][bid],original_guard_hash)
        self.assertEqual(r.eligible_ids(data,A,frozen,contract,picked),['base'])

    def test_secondary_actor_property_check_uses_exact_explicit_role_graph(self):
        data=reviewed_source();record=data['candidates'][A];proof=record['content']['role_evidence']
        proof['owner_maps']['base']=owner_map(('main_subject','secondary_subject'));seal(data,{'surface_material':['satin']});c.validate(data)
        frozen=core(['first','second'],edges=[('disjoint','first','second')],
            role_bindings={'main_subject':'first','secondary_subject':'second'})
        frozen['intent_lock']['semantic_anchors']=[{'dimension':'material','target':'main_subject','property':'surface.material'}]
        effects=record['effects']
        self.assertTrue(g.native_property_scope_allowed(frozen,effects['dimensions'],effects['properties'],entry=c.entry(data,A)))
        with audit.bound_native_source(data):
            self.assertTrue(audit.native_property_effects_allowed(frozen,effects['dimensions'],effects['properties'],candidate_id=A))
        frozen['semantic_assertions']=[row for row in frozen['semantic_assertions'] if row['axes']['kind']!='disjoint']
        self.assertFalse(g.native_property_scope_allowed(frozen,effects['dimensions'],effects['properties'],entry=c.entry(data,A)))


    def test_candidate_only_optional_bundle_public_pack_and_full_audit_preserve_root_scope(self):
        import photo_candidate_semantics as semantics
        with tempfile.TemporaryDirectory() as temp:
            pack,composed,data,context=self.full_pack(Path(temp),bundled=True)
            public=semantics.public_bundles(views.RequestCandidates(data,[A]),pack)['candidates'][0]
            self.assertEqual(public['member_candidates'],[])
            self.assertEqual(public['affected_dimensions'],['lighting'])
            self.assertEqual(public['affected_properties'],[{'dimension':'lighting','target':'main_subject','property':'lighting.direction'}])
            self.assertEqual(public['native_dependency_choices'],{B:['base']})
            self.assertEqual(len(public['native_effect_closure']),1)
            self.assertTrue(public['native_bundle_contract'])
            report=audit.audit_composed_prompt(pack,composed,source_data=data,query_context=context)
            self.assertEqual(report['status'],'pass',report)
            # Selecting the previously absent face member needs its own exact frozen carrier.
            row=next(item for item in composed['creative_augmentation_brief']['decisions'] if item['candidate_id']==A)
            row['dependency_selections']={B:'base'}
            report=audit.audit_composed_prompt(pack,composed,source_data=data,query_context=context)
            self.assertEqual(report['status'],'fail')
            self.assertTrue(any(item['check']=='native_candidate_adoption' for item in report['failures']))

    def test_explicit_member_binding_and_binding_only_reference_changes_are_bound(self):
        data=bundle();bid='bind_'+'e'*32
        data['slot_bindings'][bid]={'id':bid,'candidate_id':B,'slot_id':'light_direction','role':'optional',
            'semantic_role':'direct','conditions':{'subject_applicability':{}},'weight':1}
        parent=data['candidates'][A];parent['content']['member_candidates'][0]['binding_id']=bid
        seal(data,{'surface_material':['satin']});c.validate(data)
        original=copy.deepcopy(parent['content']['role_evidence']['reference_sha256'])
        self.assertIn(bid,original);self.assertIn(B,original)
        for defect in ['conditions','resolved_cid','binding_only_member']:
            changed=copy.deepcopy(data)
            if defect=='conditions':changed['slot_bindings'][bid]['conditions']={'requires_adult_context':True}
            elif defect=='resolved_cid':changed['slot_bindings'][bid]['candidate_id']=A
            else:changed['candidates'][A]['content']['member_candidates'][0].pop('candidate_id')
            with self.subTest(defect=defect):
                self.assertRaises(ValueError,c.validate,changed)
                self.assertRaises(ValueError,e.compact,changed['candidates'][A],changed)
        independent=reviewed_source();independent['slot_catalog'].update(data['slot_catalog'])
        independent['candidates'][B]=copy.deepcopy(data['candidates'][B]);seal(independent,{'light_direction':['underlight']},cid=B)
        independent['slot_bindings'][bid]=copy.deepcopy(data['slot_bindings'][bid])
        independent['candidates'][A]['content']['support_binding_id']=bid
        seal(independent,{'surface_material':['satin']});c.validate(independent)
        self.assertIn(B,independent['candidates'][A]['content']['role_evidence']['reference_sha256'])
        independent['slot_bindings'][bid]['conditions']={'requires_adult_context':True}
        self.assertRaises(ValueError,c.validate,independent)

    def test_three_consumers_preserve_same_native_optional_public_contract(self):
        import photo_candidate_semantics as semantics
        with tempfile.TemporaryDirectory() as temp:
            pack,_,lazy,_=self.full_pack(Path(temp),bundled=True)
            source={key:copy.deepcopy(lazy[key]) for key in c.CORPUS_FIELDS};entries={}
            for cid,record in source['candidates'].items():
                recipe,text=index.text(record);entries[cid]={'id':cid,'recipe':recipe,'text':text,
                    'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':[1.0]+[0.0]*767}
            vectors={'schema':index.SCHEMA,'space':index.SPACE,'query_recipe':index.QUERY_RECIPE,
                'corpus_sha256':c.digest(source),'entries':entries}
            full=views.assemble(source,vectors)
            full_public=semantics.public_bundles(views.RequestCandidates(full,[A]),pack)
            lazy_public=semantics.public_bundles(views.RequestCandidates(lazy,[A]),pack)
            self.assertEqual(full_public,lazy_public)
            guards={cid:layout.guard_record(record,source) for cid,record in source['candidates'].items()}
            guarded={**source,'candidates':guards}
            full_entry=c.entry(source,A,realization_id='base');compact_entry=c.entry(guarded,A,realization_id='base')
            self.assertEqual(e.admission(full_entry,pack['authorial_core']),e.admission(compact_entry,pack['authorial_core']))
            self.assertEqual(e.permission_scope(full_entry,pack['authorial_core']),e.permission_scope(compact_entry,pack['authorial_core']))
