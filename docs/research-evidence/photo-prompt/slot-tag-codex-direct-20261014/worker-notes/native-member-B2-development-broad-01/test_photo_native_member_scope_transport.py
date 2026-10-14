"""B2 complete source scopes through lazy packs and audited composition.

All data/vectors/inputs below are explicit isolated fixtures; no model execution.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
from tests import test_photo_native_existing_member_scope as f
from tests import test_photo_native_member_scope_resolution as neutral
from tests import test_photo_native_fact_wire as wire_fixture
from tests.test_photo_workflow_precore import FIXTURE,files,wire
from tests.test_photo_semantic_evidence import assertion,seal
from tests.test_photo_native_compound_evidence import dependencies
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_semantic_evidence as e
import photo_search_layout as layout
import photo_shared_views as views
import photo_role_proposals as roles
import photo_native_pack as packs
import photo_native_owner_resolution as resolver
import prompt_generator as g
import audit_composed_prompt as audit
import audit_image_render_request as render
A=f.A;B=f.B


def frozen_scope_run(directory):
    helper=wire_fixture.NativeFactWireTests();raw=helper.inputs()
    statement=('An existing secondary holder wears the existing coat_A garment and the existing glove_A garment. '
        'Both garments are present and are explicitly parts of that same holder. '
        'They are separate from the linen blanket and each other. '
        'The complete local garment collection contains exactly coat_A and glove_A.')
    raw['source_request']+=' '+statement;raw['baseline_prompt_en']+=' '+statement
    raw['intent_lock']['locked_dimensions'].remove('material');raw['intent_lock']['open_dimensions'].append('material')
    next(x for x in raw['intent_lock']['semantic_anchors'] if x['anchor_id']=='declared_linen').update(target='main_subject',property='surface.material')
    text=raw['source_request'];sha=hashlib.sha256(text.encode()).hexdigest()
    inputs={'schema':e.witnesses.INPUT_SCHEMA,'complete':True,'items':[{'id':'request','kind':'request_text','sha256':sha}]}
    request=json.loads((FIXTURE/'request-envelope.json').read_text())
    envelope=wire.normalize_request_envelope({**request,'request_text':text,'request_sha256':sha,
        'active_spans':[{'span_id':'topic','start':0,'end':len(text),'text':text}],'input_inventory':inputs})
    rows=[]
    for owner in ['coat_A','glove_A','holder_A']:
        rows += [assertion('owner_'+owner,'owner',owner=owner,owner_kind='explicitly_declared_existing_entity'),
            assertion('presence_'+owner,'fact',owner=owner,property='entity.presence',value_type='entity.presence/v1',value='present')]
    rows.append(assertion('holder_role','role',role='secondary_subject',owner='holder_A'))
    for owner in ['coat_A','glove_A']:
        rows += [assertion('kind_'+owner,'fact',owner=owner,property='entity.kind',value_type='entity.kind/v1',value='garment'),
            assertion('part_'+owner,'part_of',left=owner,right='holder_A'),
            assertion('separate_'+owner,'disjoint',left=owner,right='main_subject')]
    rows += [assertion('separate_members','disjoint',left='coat_A',right='glove_A'),
        assertion('separate_holder','disjoint',left='holder_A',right='main_subject')]
    inventory={'schema':e.witnesses.MEMBER_SCOPE_SCHEMA,'complete':True,'state':'known_present','input_binding':e.witnesses.input_binding(envelope),
        'reviewed_input_ids':['request'],'members':[{'owner_id':owner,'source_span_ids':['topic'],'source_input_ids':['request']} for owner in ['coat_A','glove_A']]}
    rows.append(assertion('local_collection','existing_member_scope',scope_id='local_members',inventory=e.witnesses.canonical(inventory)))
    for row in rows:row['source_span_ids']=['topic'];row['evidence']={'independent_request':statement}
    raw['semantic_assertions']+=rows
    run,_=helper.freeze(directory,raw,text,control_overrides={'sensual':0,'fetish':0},input_inventory=inputs)
    _,core,controls=files.verify_freeze(files.load_state(run));return run,core,controls


def scope_pack(directory):
    from tests.test_photo_global_retrieval import GlobalDiscoveryTests
    from tests.test_photo_slot_queries import synthetic_set
    from photo_search_reader import SearchReader,LazyRuntimeData
    import photo_global_index as index
    run,core,controls=frozen_scope_run(directory)
    data=f.scope_source();data['candidates'][A]['content']['role_evidence']['owner_maps']['base']['bindings'][1]['selector']['role']='secondary_subject'
    seal(data,{'surface_material':['gloss']});c.validate(data)
    data['policies']=views.source(GlobalDiscoveryTests().data())['policies'];data['policies']['bundle_refs']=[]
    data['policies']['_quality_layers']={'adult_appeal':{'contextual_retrieval':{'contract_version':'photo-contextual-appeal/v2'}}}
    vectors={'schema':index.SCHEMA,'space':index.SPACE,'query_recipe':index.QUERY_RECIPE,'corpus_sha256':c.digest(data),'entries':{}}
    for cid,record in data['candidates'].items():
        recipe,text=index.text(record);vectors['entries'][cid]={'id':cid,'recipe':recipe,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':[1.0]+[0.0]*767}
    assets=directory/'synthetic-search';layout.build(assets,data,vectors,activate=True)
    runtime=LazyRuntimeData(SearchReader(assets)).for_core(core);query=synthetic_set(core,controls,data['slot_catalog'],['surface_material'])
    pack=g.generate_candidate_pack(runtime,core,controls,files.value(files.load_state(run),'embodiment_review'),seed=5,query_context=query,requested_slots=['surface_material'])
    return run,pack,runtime,query


def composition(pack,data):
    from tests.photo_native_runtime import compose_native
    value=compose_native(pack);phrase='A glossy optical response is visible across each existing coat_A and glove_A garment surface, preserving their holder and identity.'
    value['prompt_en']+=' '+phrase;value['chosen_candidate_ids']=[A]
    properties=[{'dimension':'material','target':owner,'property':'surface.optical_response'} for owner in ['coat_A','glove_A']]
    row={'candidate_id':A,'realization_id':'base','artistic_interpretation':'Preserve every independently declared existing garment and holder.',
        'transformation':'Apply the expressly chosen glossy optical response to every scoped member.','prompt_evidence':phrase,'affected_properties':properties}
    value['candidate_interpretations']=[row]
    for decision in value['creative_augmentation_brief']['decisions']:
        if decision['candidate_id']==A:
            decision.update(row,decision='transformed',rationale='Apply only the declared all-member response with whole property permission.',affected_dimensions=['material']);value['candidate_interpretations']=[]
    value['owner_selections']=f.choices(data,pack['authorial_core'])
    value['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(value['prompt_en'].encode()).hexdigest();return value


class MemberScopeClosureTests(unittest.TestCase):
    def compound(self,optional=False,value='glossy'):
        data=f.scope_source();child=f.scope_source(cid=B)
        rec=child['candidates'][B];rec['content']['en']=rec['content']['en'].replace('glossy',value)
        next(x for x in rec['content']['role_evidence']['facts'] if x['id']=='gloss')['value']['value']=value
        for row in rec['content']['role_evidence']['facts']:row['quote']=row['quote'].replace('glossy',value)
        seal(child,{'surface_material':['gloss']},cid=B);data['candidates'][B]=rec
        parent=data['candidates'][A];parent['record_kind']='visual_bundle'
        parent['content']['member_candidates']=[{'candidate_id':B,'adoption':'optional' if optional else 'required','requirements':{},
            'conditions':{'native_guards':{'schema':e.SOURCE_TARGET_GUARD_SCHEMA,'rules':[{'id':'same_holder','kind':'owner_relation','relation':'disjoint',
                'left':f.endpoint('holder'),'right':f.endpoint('surfaces',B)}]}}}]
        # Scalar predicate cannot lift child scope; a valid member layer uses an
        # explicit member quantifier whose scalar RHS is the parent point.
        parent['content']['member_candidates'][0]['conditions']={'native_guards':{'schema':e.MEMBER_GUARD_SCHEMA,'rules':[f.each({
            'id':'owned_by_parent_holder','kind':'owner_relation','relation':'part_of','left':f.member(),'right':f.endpoint('holder')},cid=B)]}}
        dependencies(data,A,'base',[B])
        if optional:parent['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
        seal(data,{'surface_material':['gloss']});c.validate(data);return data

    def test_required_selected_optional_and_materialized_child_share_one_view(self):
        for optional in [False,True]:
            data=self.compound(optional);core=f.scope_core();mapping=f.choices(data,core);mapping['entries']+=f.choices(data,core,cid=B)['entries']
            for entry in f.entries(data,core,mapping=mapping,dependency_selections={B:'base'}):
                with mock.patch.object(resolver,'resolve_selected_contracts',wraps=resolver.resolve_selected_contracts) as call:
                    result=e.admission(entry,core);self.assertTrue(result['allowed'],result);self.assertEqual(call.call_count,1)
                member=views.materialize_member(data,data['candidates'][A]['content']['member_candidates'][0],realization_id='base',owner_selections=mapping,guard_root=entry)
                self.assertTrue(e.admission(member,core)['allowed'])
                self.assertEqual(e.permission_scope(member,core)[1],e.permission_scope(entry,core)[1])
                self.assertEqual(r.eligible_ids(data,A,core,{}, {'subject':{}},owner_selections=mapping,dependency_selections={B:'base'}),['base'])
                trace=result['dependencies'][0]['admission']['native_guards']['rules'][-1]
                self.assertEqual((trace['declaring_candidate_id'],trace['activation_candidate_id']),(A,B))
            if optional:
                for entry in f.entries(data,core):
                    result=e.admission(entry,core);self.assertTrue(result['allowed'],result);self.assertEqual(result['dependencies'],[])

    def test_joint_independent_required_and_optional_conflict_not_hidden_by_scope(self):
        core=f.scope_core()
        for optional in [False,True]:
            data=self.compound(optional,value='matte');mapping=f.choices(data,core);mapping['entries']+=f.choices(data,core,cid=B)['entries']
            for entry in f.entries(data,core,mapping=mapping,dependency_selections={B:'base'}):self.assertFalse(e.admission(entry,core)['allowed'])
            if optional:
                for entry in f.entries(data,core):self.assertTrue(e.admission(entry,core)['allowed'])
        data=f.scope_source();child=f.scope_source(cid=B);rec=child['candidates'][B];rec['content']['en']=rec['content']['en'].replace('glossy','matte')
        next(x for x in rec['content']['role_evidence']['facts'] if x['id']=='gloss')['value']['value']='matte'
        for row in rec['content']['role_evidence']['facts']:row['quote']=row['quote'].replace('glossy','matte')
        seal(child,{'surface_material':['gloss']},cid=B);data['candidates'][B]=rec;c.validate(data)
        mapping=f.choices(data,core);mapping['entries']+=f.choices(data,core,cid=B)['entries']
        entries=[c.entry(data,cid,realization_id='base',owner_selections=mapping) for cid in [A,B]]
        self.assertRaisesRegex(ValueError,'conflicting joint',e.validate_joint_effect_assignments,entries,core)

    def test_source_scope_role_and_profile_descriptors_are_unresolved(self):
        data=f.scope_source();core=f.scope_core();proposal=roles.propose(data,'surface_material',A,[])
        self.assertEqual(proposal['owner_selection_requirements']['schema'],'photo-owner-selection-requirements/v2')
        self.assertEqual(proposal['semantic_fit']['status'],'review_required')
        self.assertTrue(e.admission(roles.entry(data,proposal,owner_selections=f.choices(data,core)),core)['allowed'])
        from tests import test_photo_native_v4_guards as profiles
        data=profiles.profile_source();p=data['candidates'][A]['content']['role_evidence']
        for mapping in p['owner_maps'].values():
            mapping['schema']=e.MEMBER_OWNER_SCHEMA
            for row in mapping['bindings']:
                role=row.pop('core_role');row['selector']=(copy.deepcopy(f.scope_source()['candidates'][A]['content']['role_evidence']['owner_maps']['base']['bindings'][0]['selector'])
                    if row['target']=='surface' else {'kind':'core_role','role':role})
        seal(data,{'light_direction':[x['id'] for x in p['facts'] if x['mode']=='effect']});c.validate(data)
        core['intent_lock']['open_dimensions'].append('lighting');neutral.reseal(core)
        choices=profiles.NativeV4ProfileTests().choices(data,core)
        alone=next(x for x in choices['profiles'][0]['choices'] if x['realization_id']=='alone')
        self.assertEqual(alone['owner_selection_requirements']['schema'],'photo-owner-selection-requirements/v2')
        selection=f.choices(data,core,rid='alone');selection['entries'][0]['bindings'][0]['target']='surface'
        for record in [data['candidates'][A],layout.guard_record(data['candidates'][A],data)]:
            entry=c.entry({**data,'candidates':{A:record}},A,realization_id='alone',owner_selections=selection)
            self.assertTrue(e.admission(entry,core)['allowed']);self.assertEqual({x['target'] for x in e.permission_scope(entry,core)[1]},{'coat_A','glove_A'})
            phrase='Side light grazes the declared linen surface from the left.'
            audit.audit_selected_native_profile(entry,{'realization_id':'alone','selected_profile_contract':entry['_selected_profile_contract'],
                'selected_profile_evidence':{'side_light_phrase':phrase}},phrase)


class MemberScopeRealTransportTests(unittest.TestCase):
    def test_actual_freeze_lazy_pack_compose_and_fresh_runtime(self):
        with tempfile.TemporaryDirectory() as temp:
            _,pack,data,query=scope_pack(Path(temp));self.addCleanup(data.reader.close);before=c.canonical_bytes(pack)
            self.assertIn(A,pack['candidate_pool']);self.assertNotIn('owner_selections',pack)
            self.assertEqual(pack['candidate_pool'][A]['owner_selection_requirements']['schema'],'photo-owner-selection-requirements/v2')
            composed=composition(pack,data)
            with mock.patch.object(resolver,'resolve_selected_contracts',wraps=resolver.resolve_selected_contracts) as call:
                output={};self.assertEqual(audit.audit_native_adoptions(pack,composed,data,resolution_out=output),[]);self.assertEqual(call.call_count,1)
            self.assertEqual(output['schema'],'photo-native-owner-resolution/v2');self.assertEqual(len(output['resolved_view']['effect_assignments']),2)
            with audit.bound_native_source(data,query):
                report=audit.audit_composed_prompt(pack,composed);self.assertEqual(report['status'],'pass',report)
                receipt=report['native_owner_resolution'];request={'native_owner_resolution_sha256':receipt['canonical_sha256'],'source_composed_sha256':receipt['composed_sha256']}
                self.assertFalse(any(x['check']=='native_owner_resolution' for x in render.audit_image_render_request(pack,composed,request)['failures']))
                for field in request:
                    bad={**request,field:'0'*64};self.assertTrue(any(x['check']=='native_owner_resolution' for x in render.audit_image_render_request(pack,composed,bad)['failures']))
                for defect in ['missing','table','scope','unused','receipt_input']:
                    bad=copy.deepcopy(composed)
                    if defect=='missing':bad.pop('owner_selections')
                    elif defect=='table':bad['owner_selections']['member_scopes_sha256']='0'*64
                    elif defect=='scope':bad['owner_selections']['entries'][0]['bindings'][0]['selection']['scope_sha256']='0'*64
                    elif defect=='unused':bad['owner_selections']['entries'].append({**copy.deepcopy(bad['owner_selections']['entries'][0]),'candidate_id':B})
                    else:bad['native_owner_resolution']=receipt
                    with self.subTest(defect=defect):self.assertEqual(audit.audit_composed_prompt(pack,bad)['status'],'fail')
            self.assertEqual(before,c.canonical_bytes(pack))

    def test_workflow_failure_correction_success_rebind_and_stored_runtime_equality(self):
        from tests.test_photo_workflow_state import workflow
        import photo_workflow_worker as worker
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp);run,pack,data,query=scope_pack(directory);self.addCleanup(data.reader.close)
            with files.locked_state(run) as state:files.commit_stage(run,state,'pack_bound',{'pack':files.encode(pack),'runtime_receipt':files.encode({})})
            composed=composition(pack,data);path=directory/'composed.json'
            def direct(state,**kwargs):return {'composed_audit':audit.audit_composed_prompt(files.value(state,'pack'),files.value(state,'composed'),source_data=data,query_context=query)}
            bad=copy.deepcopy(composed);bad.pop('owner_selections');path.write_text(json.dumps(bad))
            with mock.patch.object(worker,'audit_bound',side_effect=direct):
                self.assertEqual(workflow.compose_audit(argparse.Namespace(run=run,composed=path))['status'],'fail');self.assertNotIn('composed',files.load_state(run)['artifacts'])
                path.write_text(json.dumps(composed));self.assertEqual(workflow.compose_audit(argparse.Namespace(run=run,composed=path))['status'],'pass')
                self.assertEqual(workflow.compose_audit(argparse.Namespace(run=run,composed=path))['status'],'pass')
                changed=copy.deepcopy(composed);changed['owner_selections']['entries'][0]['bindings'][0]['selection']['scope_id']='other';path.write_text(json.dumps(changed))
                self.assertRaisesRegex(ValueError,'owner_selection_rebinding_requires_new_run',workflow.compose_audit,argparse.Namespace(run=run,composed=path))
            parameters=directory/'parameters';parameters.write_text(json.dumps({'references':[]}))
            with mock.patch('photo_runtime_sources.RuntimeSnapshotProvider.from_receipt',return_value=SimpleNamespace(data=data,query_context=query)):
                result=workflow.prepare_render(argparse.Namespace(run=run,parameters=parameters,lane='native',model=None,size=None))
                self.assertEqual(result['status'],'pass',result)
                state=files.load_state(run);request=files.value(state,'render_request');stored=files.value(state,'composed_audit')['native_owner_resolution']
                self.assertEqual(request['native_owner_resolution_sha256'],stored['canonical_sha256'])
                with files.locked_state(run) as state:
                    report=files.value(state,'composed_audit');report['native_owner_resolution']['canonical_sha256']='0'*64
                    files.commit_stage(run,state,'composition_audited',{'composed_audit':files.encode(report)})
                result=worker.audit_bound(files.load_state(run),runtime=True)
                self.assertTrue(any(x['check']=='native_owner_resolution' for x in result['composed_audit']['failures']))

if __name__=='__main__':unittest.main()
