"""Actual isolated lazy/public/compose/runtime transport; no operating source IO."""
import copy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
from tests import test_photo_native_manual_role_views as m
from tests import test_photo_native_member_scope_transport as t
from tests import test_photo_native_existing_member_scope as scoped
from tests import test_photo_native_compound_evidence as compound
from tests.test_photo_semantic_evidence import seal
import photo_candidate_corpus as c
import photo_semantic_evidence as e
import photo_native_owner_resolution as resolver
import photo_role_proposals as roles
import photo_native_pack as packs
import audit_composed_prompt as audit
import audit_image_render_request as render
A=m.A;B=compound.B


def view_pack(directory):
    from tests.test_photo_global_retrieval import GlobalDiscoveryTests
    from tests.test_photo_slot_queries import synthetic_set
    from photo_search_reader import SearchReader,LazyRuntimeData
    import photo_search_layout as layout
    import photo_global_index as index
    import prompt_generator as g
    import hashlib
    # Write the complete explicit fixture AFTER the independent core is frozen.
    # Local holder is explicitly the secondary holder declared by that core;
    # do not compile a view and silently change its owner map afterwards.
    run,core,controls=t.frozen_scope_run(directory);data=m._BASE_SCOPE_SOURCE()
    spec=data['slot_catalog']['surface_material']
    spec.update(description='Visible optical response of an actual existing surface.',
        description_ko='실제 기존 표면의 가시적인 광학 반응.',dimensions=['appearance'],property_prefixes=['surface.presentation'],
        includes=['The explicitly rendered glossy response.'],excludes=['An inferred material replacement.'])
    data['candidates'][A]['content']['role_evidence']['owner_maps']['base']['bindings'][1]['selector']['role']='secondary_subject'
    seal(data,{'surface_material':['gloss']});m.attach(data,'surface_material',['gloss'],{'gloss':'glossy'});c.validate(data)
    data['policies']=t.views.source(GlobalDiscoveryTests().data())['policies'];data['policies']['bundle_refs']=[]
    data['policies']['_quality_layers']={'adult_appeal':{'contextual_retrieval':{'contract_version':'photo-contextual-appeal/v2'}}}
    vectors={'schema':index.SCHEMA,'space':index.SPACE,'query_recipe':index.QUERY_RECIPE,'corpus_sha256':c.digest(data),'entries':{}}
    for cid,record in data['candidates'].items():
        recipe,text=index.text(record);vectors['entries'][cid]={'id':cid,'recipe':recipe,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':[1.0]+[0.0]*767}
    assets=directory/'synthetic-search';layout.build(assets,data,vectors,activate=True)
    runtime=LazyRuntimeData(SearchReader(assets)).for_core(core);query=synthetic_set(core,controls,data['slot_catalog'],['surface_material'])
    pack=g.generate_candidate_pack(runtime,core,controls,t.files.value(t.files.load_state(run),'embodiment_review'),seed=5,query_context=query,requested_slots=['surface_material'])
    return run,pack,runtime,query


def member_views(optional=False):
    data=t.MemberScopeClosureTests().compound(optional)
    spec=data['slot_catalog']['surface_material']
    spec.update(description='Visible optical response of actual existing surfaces.',
        dimensions=['appearance'],property_prefixes=['surface.presentation'])
    seal(data,{'surface_material':['gloss']},cid=B)
    m.attach(data,'surface_material',['gloss'],{'gloss':'glossy'},cid=B)
    compound.dependencies(data,A,'base',[B])
    if optional:data['candidates'][A]['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
    seal(data,{'surface_material':['gloss']})
    m.attach(data,'surface_material',['gloss'],{'gloss':'glossy'})
    c.validate(data);return data


class NativeManualRoleViewTransportTests(unittest.TestCase):
    def test_actual_lazy_immutable_pack_compose_and_fresh_runtime_with_one_expansion(self):
        with tempfile.TemporaryDirectory() as temp:
            _,pack,data,query=view_pack(Path(temp));self.addCleanup(data.reader.close)
            before=c.canonical_bytes(pack);proposal=next(iter(pack['role_proposals'].values()))
            support=proposal['semantic_fit']['matched_manual_role_views'][0]
            self.assertEqual(support['fact']['dimension'],'material');self.assertEqual(support['fact']['property'],'surface.optical_response')
            self.assertGreater(data.reader.metrics['payload_reads'],0)
            self.assertNotIn('owner_selections',pack)
            with mock.patch.object(e,'_lookup_manual_view_authority',wraps=e._lookup_manual_view_authority) as authority:
                replay=roles.propose(data,'surface_material',A,[],realization_ids=['base'])
                self.assertEqual(replay['semantic_fit'],proposal['semantic_fit']);self.assertEqual(authority.call_count,1)
            composed=t.composition(pack,data)
            with audit.bound_native_source(data,query):
                with mock.patch.object(resolver,'resolve_selected_contracts',wraps=resolver.resolve_selected_contracts) as call:
                    report=audit.audit_composed_prompt(pack,composed)
                    self.assertEqual(report['status'],'pass',report);self.assertEqual(call.call_count,1)
                resolved=report['native_owner_resolution'];request={'native_owner_resolution_sha256':resolved['canonical_sha256'],'source_composed_sha256':resolved['composed_sha256']}
                runtime=render.audit_image_render_request(pack,composed,request)
                self.assertFalse(any(x['check']=='native_owner_resolution' for x in runtime['failures']),runtime)
            self.assertEqual(before,c.canonical_bytes(pack))

    def test_public_source_and_compact_receipt_selfhash_cannot_mint_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            _,pack,data,query=view_pack(Path(temp));self.addCleanup(data.reader.close);composed=t.composition(pack,data)
            published=data['candidates'][A];guard=copy.deepcopy(data.reader.meta['guards'][A]);p=e.proof_of(guard)
            # Recompute all local receipt/compact hashes, while the independent
            # published full source remains exact and unchanged.
            p['manual_role_view_bindings']['bindings'][0]['fact']['value']['value']='matte'
            receipt=p['manual_role_view_bindings'];receipt['receipt_sha256']=c.digest({k:v for k,v in receipt.items() if k!='receipt_sha256'})
            p['compact_sha256']=c.digest({k:v for k,v in p.items() if k!='compact_sha256'})
            self.assertNotEqual(e.qualification(data['slot_catalog']['surface_material'],guard,source_data=data)['status'],'eligible')
            bad=copy.deepcopy(pack);rec=bad['candidate_pool'][A]['authored_record'];proof=rec['content']['role_evidence']
            proof['manual_role_views'][0]['manual_semantic_facet']='Forged public-pack interpretation.'
            proof['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(proof)
            # Refresh the visible public source hash and its proposal IDs too.
            proposals={}
            for old,row in bad['role_proposals'].items():
                row['source_record_sha256']=c.digest(rec);row['proposal_id']='role_'+c.digest({k:v for k,v in row.items() if k!='proposal_id'})[:32];proposals[old]=row['proposal_id']
            def rename(value):
                if isinstance(value,str):return proposals.get(value,value)
                if isinstance(value,list):return [rename(x) for x in value]
                if isinstance(value,dict):return {proposals.get(k,k):rename(v) for k,v in value.items()}
                return value
            bad=rename(bad);bad['global_retrieval']['role_proposals']=copy.deepcopy(bad['role_proposals'])
            bad['global_retrieval']['canonical_sha256']=c.digest({k:v for k,v in bad['global_retrieval'].items() if k!='canonical_sha256'})
            with audit.bound_native_source(data,query):
                report=audit.audit_composed_prompt(bad,composed);self.assertEqual(report['status'],'fail')
                self.assertTrue(any(row['check']=='global_retrieval_contract' for row in report['failures']),report)
            self.assertEqual(data['candidates'][A],published)

    def test_lazy_missing_pinned_payload_cannot_fall_back_to_guard_or_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            _,pack,data,query=view_pack(Path(temp));self.addCleanup(data.reader.close)
            block=data.reader.meta['payload_locator'][A];path=data.reader.assets/data.reader.meta['payload_shards'][block]['path']
            data.reader.cache.clear();data.reader.cache_bytes=0;path.unlink()  # Isolated synthetic file only.
            value=roles.propose(data,'surface_material',A,[],realization_ids=['base'])
            self.assertNotEqual(value['semantic_fit']['status'],'eligible')
            self.assertEqual(value['native_qualification'],'invalid')

    def test_non_opt_in_role_lookup_never_loads_full_payload_or_adds_view_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            _,pack,data,query=t.scope_pack(Path(temp));self.addCleanup(data.reader.close)
            count=data.reader.metrics['payload_reads']
            with mock.patch.object(e,'_lookup_manual_view_authority',side_effect=AssertionError('old lookup must not hydrate view authority')):
                proposal=roles.propose(data,'surface_material',A,[],realization_ids=['base'])
            self.assertNotIn('matched_manual_role_views',proposal['semantic_fit'])
            self.assertEqual(data.reader.metrics['payload_reads'],count)

    def test_required_selected_optional_and_unselected_child_keep_their_own_views(self):
        frozen=scoped.scope_core()
        for optional in [False,True]:
            data=member_views(optional);mapping=scoped.choices(data,frozen);mapping['entries']+=scoped.choices(data,frozen,cid=B)['entries']
            for entry in scoped.entries(data,frozen,mapping=mapping,dependency_selections={B:'base'}):
                with mock.patch.object(resolver,'resolve_selected_contracts',wraps=resolver.resolve_selected_contracts) as call:
                    result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result);self.assertEqual(call.call_count,1)
                self.assertEqual(result['dependencies'][0]['candidate_id'],B)
                self.assertTrue(e.qualification(data['slot_catalog']['surface_material'],data['candidates'][A],source_data=data)['matched_manual_role_views'])
            if optional:
                for entry in scoped.entries(data,frozen):self.assertEqual(e.admission(entry,frozen)['dependencies'],[])
            bad=copy.deepcopy(data);p=bad['candidates'][A]['content']['role_evidence'];p['manual_role_views'][0]['candidate_id']=B
            p['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(p)
            self.assertRaises(ValueError,c.validate,bad)

    def test_workflow_stored_resolution_matches_fresh_source_qualified_runtime(self):
        import argparse
        from tests.test_photo_workflow_state import workflow
        import photo_workflow_worker as worker
        with tempfile.TemporaryDirectory() as temp:
            directory=Path(temp);run,pack,data,query=view_pack(directory);self.addCleanup(data.reader.close)
            with t.files.locked_state(run) as state:t.files.commit_stage(run,state,'pack_bound',{'pack':t.files.encode(pack),'runtime_receipt':t.files.encode({})})
            composed=t.composition(pack,data);path=directory/'composed.json';path.write_text(json.dumps(composed))
            def direct(state,**kwargs):return {'composed_audit':audit.audit_composed_prompt(t.files.value(state,'pack'),t.files.value(state,'composed'),source_data=data,query_context=query)}
            with mock.patch.object(worker,'audit_bound',side_effect=direct):
                self.assertEqual(workflow.compose_audit(argparse.Namespace(run=run,composed=path))['status'],'pass')
                self.assertEqual(workflow.compose_audit(argparse.Namespace(run=run,composed=path))['status'],'pass')
            parameters=directory/'parameters';parameters.write_text(json.dumps({'references':[]}))
            with mock.patch('photo_runtime_sources.RuntimeSnapshotProvider.from_receipt',return_value=SimpleNamespace(data=data,query_context=query)):
                result=workflow.prepare_render(argparse.Namespace(run=run,parameters=parameters,lane='native',model=None,size=None));self.assertEqual(result['status'],'pass',result)
                state=t.files.load_state(run);stored=t.files.value(state,'composed_audit')['native_owner_resolution'];request=t.files.value(state,'render_request')
                self.assertEqual(request['native_owner_resolution_sha256'],stored['canonical_sha256'])
                with t.files.locked_state(run) as state:
                    report=t.files.value(state,'composed_audit');report['native_owner_resolution']['canonical_sha256']='0'*64
                    t.files.commit_stage(run,state,'composition_audited',{'composed_audit':t.files.encode(report)})
                fresh=worker.audit_bound(t.files.load_state(run),runtime=True)
                self.assertTrue(any(row['check']=='native_owner_resolution' for row in fresh['composed_audit']['failures']))


if __name__=='__main__':unittest.main()
