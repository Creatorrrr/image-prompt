"""Source-authority, joint/closure, source-only and final real-auditor regressions."""
import copy
import unittest
from unittest import mock
from tests.test_photo_native_permission_envelope import (source_fixture,core_fixture,entries,freeze_inputs,freeze,after_evidence)
from tests.test_photo_semantic_evidence import A,fact,source,seal,reattest
from tests.test_photo_native_source_guards_v2 import selected_map,choices
from tests.test_photo_native_compound_evidence import B,dependencies
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import photo_native_permission as permission
import photo_permission_comparison as comparison
import photo_search_layout as layout
import prompt_generator as g
import audit_composed_prompt as audit


def paired_source(prop='layout.arrangement',*,compound=False):
    data=source_fixture()
    text=('On the independently declared existing image select a grid layout arrangement. '
          'The same existing image and item are preserved as entities; no visibility state changes.') if prop=='layout.arrangement' else (
          'On the independently declared existing image select detailed macro shot scale. '
          'This source changes a child property within the same shot scale family.')
    f=fact('secondE','framing','second_image',prop,'effect','grid' if prop=='layout.arrangement' else 'detailed_macro',['secondP'],quote='select a grid layout arrangement' if prop=='layout.arrangement' else 'select detailed macro shot scale',operation='set_value',receivers=[])
    second=source(text,[fact('secondP','subject','second_image','entity.presence','prerequisite','present',[],quote='independently declared existing image'),f],
       {'second':slot('second',['framing'],property_prefixes=[prop])},{'base':selected_map('second_image')})
    rec=second['candidates'].pop(A);rec['id']=B;data['candidates'][B]=rec;data['slot_catalog'].update(second['slot_catalog'])
    seal(data,{'fixture_shot':['macroE']});seal(data,{'second':['secondE']},cid=B)
    if compound:
        rec['record_kind']='visual_bundle';rec['content']['member_candidates']=[{'candidate_id':A,'adoption':'required','requirements':{}}]
        dependencies(data,B,'base',[A]);seal(data,{'second':['secondE']},cid=B)
    c.validate(data)
    return data


def paired_inputs(data,frozen,*,compound=False):
    sa=choices(data,frozen,{'item':'X','image':'I'});sb=choices(data,frozen,{'second_image':'I'},cid=B)
    selected=copy.deepcopy(sa);selected['entries']+=sb['entries']
    es=[c.entry(data,cid,realization_id='base',owner_selections=selected)for cid in ([B] if compound else [A,B])]
    # This fixture's request inventory is independent of source selection. Only
    # the source-specific exhaustive impact review is rebuilt for the two nodes.
    a,i,_,_=freeze_inputs(data,frozen,c.entry(data,A,realization_id='base',owner_selections=sa))
    context=n._resolve_selected_native_contracts(es,frozen);view=context['view']
    contracts={A:copy.deepcopy(data['candidates'][A]['content']['permission_envelope']['realizations']['base']),
       B:{'canonical_effect_refs':['secondE'],'basis':[{'fact_ref':'secondE','unit_pointer':'/content/en',
       'rationale':'Manually read same-image grid control or deliberately overlapping shot-detail negative; no new E/receiver inferred.'}],'preservation':[]}}
    bound={cid:permission._source_context(permission._payload(a,'source authority'),node,contracts[cid])[0]for cid,node in context['nodes'].items()}
    pins={cid:comparison.source_binding(b)for cid,b in bound.items()}
    review={'schema':'research-source-anchor-impact-review/v1','inventory_sha256':c.digest(i),'resolved_view_sha256':c.digest(view),
        'source_bindings_sha256':c.digest(pins),'reviewer':'independent synthetic two-source review','anchors':[],'joint':[]}
    effects={c.digest({k:f[k]for k in ['candidate_id','realization_id','fact_id','expansion_index','target']}):f for node in view['nodes']for f in node['expanded_facts']if f['mode']=='effect'}
    for key,f in effects.items():
        for anchor in i['anchors']:
            review['anchors'].append({'effect_key':key,'anchor_key':c.digest(anchor),'impact':'disjoint',
                'reason':'Explicit synthetic reading: grid/shot scale preserve declared identity, count, age, entity presence, event, concept and same-item visibility/image correspondence.',
                'input_ids':['request'],'span_ids':['request_1'],'preservation_ref':None})
    keys=sorted(effects)
    review['joint']=[{'effect_keys':keys,'impact':'disjoint','reason':'Independent synthetic disjoint proposal; the mechanical property-path primitive must still veto the shot-parent/child negative.',
                     'input_ids':['request'],'span_ids':['request_1']}]
    inv=permission.freeze_permission_inventory(frozen,i,expected_inventory_sha256=c.digest(i),reviewer='independent pre-discovery author')
    return a,inv,review,contracts,es


class NativePermissionTransportTests(unittest.TestCase):
    def test_stripped_rehashed_compact_is_not_source_authority_any_strict_route(self):
        data=source_fixture();frozen=core_fixture();full,compact=entries(data,frozen)
        for defect in ['removed_optin','new_qualification','changed_fact','removed_all_proof']:
            forged=copy.deepcopy(compact);p=forged['_semantic_evidence_guard'];p.pop('permission_envelopes')
            if defect=='new_qualification':p['qualification_sha256']='b'*64
            elif defect=='changed_fact':next(f for f in p['facts']if f['id']=='macroE')['value']['value']='wide'
            elif defect=='removed_all_proof':forged.pop('_semantic_evidence_guard');forged.pop('permission_envelope',None);forged.pop('role_evidence',None)
            if '_semantic_evidence_guard'in forged:p['compact_sha256']=c.digest({k:v for k,v in p.items()if k!='compact_sha256'})
            with self.subTest(defect=defect):
                self.assertFalse(n.admission(forged,frozen,source_data=data)['allowed'])
                self.assertFalse(g.core_entry_eligible(data,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'',forged))
                with self.assertRaises(ValueError):n.permission_scope(forged,frozen,source_data=data)
                if defect!='removed_all_proof':self.assertFalse(n.admission(forged,frozen)['allowed'])
    def test_full_qualification_cannot_replace_actual_corpus_source(self):
        data=source_fixture();record=copy.deepcopy(data['candidates'][A]);p=record['content']['role_evidence']
        record['content'].pop('permission_envelope');p.pop('permission_envelopes');p['meaning_sha256']=n.meaning_sha256(record)
        p['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(p)
        with self.assertRaisesRegex(ValueError,'actual full corpus'):n.validate(record,data['slot_catalog'],corpus=data)
    def test_source_only_declared_application_can_prepare_but_not_adopt_or_freeze(self):
        data=source_fixture();data['candidates'][A]['content'].pop('role_evidence');c.validate(data)
        self.assertEqual(n.native_status(data['candidates'][A]),'unqualified')
        entry=c.entry(data,A,realization_id='base');self.assertFalse(n.admission(entry,core_fixture())['allowed'])
        with self.assertRaises(ValueError):permission.freeze_source_authority(data,expected_snapshot_sha256=c.digest(data),reviewer='reviewer')
        for defect in ['pointer','rid','schema','missing_refs']:
            bad=copy.deepcopy(data);d=bad['candidates'][A]['content']['permission_envelope']
            if defect=='pointer':d['realizations']['base']['basis'][0]['unit_pointer']='/content/tags'
            elif defect=='rid':d['realizations']['other']=d['realizations'].pop('base')
            elif defect=='schema':d['schema']='unknown'
            else:d['realizations']['base']['canonical_effect_refs']=[]
            with self.subTest(defect=defect),self.assertRaises(ValueError):c.validate(bad)
    def test_compact_selfhash_without_verified_transport_registration_denied(self):
        data=source_fixture();frozen=core_fixture();entry=entries(data,frozen)[0]
        saved=copy.deepcopy(permission._TRANSPORTS);permission._TRANSPORTS.clear()
        try:self.assertFalse(n.admission(entry,frozen)['allowed'])
        finally:permission._TRANSPORTS.update(saved)
    def test_joint_parent_child_cannot_be_waived_but_unrelated_same_owner_passes(self):
        frozen=core_fixture()
        for prop,allowed in [('shot.scale.detail',False),('layout.arrangement',True)]:
            data=paired_source(prop);a,i,review,contracts,es=paired_inputs(data,frozen)
            if not allowed:
                with self.assertRaisesRegex(ValueError,'joint property-path overlap'):permission.freeze_permission_plan(a,frozen,es,inventory=i,assessment=review,contracts=contracts,reviewer='reviewer')
            else:
                plan=permission.freeze_permission_plan(a,frozen,es,inventory=i,assessment=review,contracts=contracts,reviewer='reviewer')
                with permission.trusted_permission_session(a,plan),n.bound_selected_resolution(es,frozen):
                    n.validate_joint_effect_assignments(es,frozen)
                    for entry in es:self.assertTrue(n.admission(entry,frozen)['allowed'])
    def test_required_child_cannot_hide_mandatory_contract_in_full_or_compact_root(self):
        data=paired_source(compound=True);frozen=core_fixture();a,i,r,cs,es=paired_inputs(data,frozen,compound=True)
        plan=permission.freeze_permission_plan(a,frozen,es,inventory=i,assessment=r,contracts=cs,reviewer='reviewer')
        for entry in [es[0],c.entry({**data,'candidates':{**data['candidates'],B:layout.guard_record(data['candidates'][B],data)}},B,realization_id='base',owner_selections=es[0]['_native_owner_selections'])]:
            self.assertFalse(n.admission(entry,frozen)['allowed'])
            with permission.trusted_permission_session(a,plan):self.assertTrue(n.admission(entry,frozen)['allowed'])
    def test_actual_final_auditor_consumes_plan_and_typed_state(self):
        data=source_fixture();frozen=core_fixture();entry=entries(data,frozen)[0];a,p=freeze(data,frozen,entry)
        result=permission.freeze_after_state(p,frozen,expected_after_sha256=c.digest(frozen),evidence=after_evidence(p),reviewer='independent result author')
        pack={'authorial_core':frozen,'creative_controls':{}};composed={'chosen_candidate_ids':[A],
            'candidate_interpretations':[{'candidate_id':A,'realization_id':'base'}],
            'owner_selections':entry['_native_owner_selections'],'prompt_en':'Existing item stays visible in image I with macro framing.'}
        # Only unrelated categorical policy setup is isolated; native source,
        # closure, whole consumer, joint, PR and all actual locks execute.
        with mock.patch.object(g,'frozen_core_context',return_value=({'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}})):
            self.assertTrue(audit.audit_native_adoptions(pack,composed,data))
            with permission.trusted_permission_session(a,p):self.assertTrue(audit.audit_native_adoptions(pack,composed,data))
            with permission.trusted_permission_session(a,p,after_state=result):
                output={};self.assertEqual(audit.audit_native_adoptions(pack,composed,data,resolution_out=output),[])
                self.assertTrue(output['native_preservation_receipt']['receipts'][0]['result_source_spans'])
    def test_validate_compact_and_self_rehash_never_issue_source_authority(self):
        actual=source_fixture();frozen=core_fixture();original=entries(actual,frozen)[0]
        forged=copy.deepcopy(actual);r=forged['candidates'][A];p=r['content']['role_evidence']
        r['content'].pop('permission_envelope');p.pop('permission_envelopes')
        p['meaning_sha256']=n.meaning_sha256(r)
        p['review']['native_review']['native_contract_sha256']=n.native_contract_sha256(p)
        before=copy.deepcopy(permission._TRANSPORTS)
        n.validate(r,forged['slot_catalog'])
        n.validate(r,forged['slot_catalog'],corpus=forged)
        n.compact(r,forged)
        self.assertEqual(permission._TRANSPORTS,before)
        self.assertTrue(permission.transport(original)['required'])
        for entry in entries(forged,frozen):
            self.assertFalse(n.admission(entry,frozen)['allowed'])
            with self.assertRaises(ValueError):n.permission_scope(entry,frozen)
            self.assertFalse(g.core_entry_eligible(forged,frozen,{'subject_category':'object','intent_constraints':{'domains':[]}},{'subject':{}},'',entry))
        self.assertEqual(n.qualification(forged['slot_catalog']['fixture_shot'],r)['reason'],'independent_source_transport_authority_required')
        # An explicit independently pinned trusted replacement is a different
        # action from shape validation. It issues only the reviewed new bytes.
        permission.freeze_source_authority(forged,expected_snapshot_sha256=c.digest(forged),reviewer='explicit authorized synthetic source replacement')
        self.assertTrue(n.admission(entries(forged,frozen)[0],frozen)['allowed'])
        self.assertTrue(permission.transport(original)['required'])
    def test_untrusted_validator_with_no_preexisting_registry_cannot_mint(self):
        data=source_fixture();frozen=core_fixture();saved=copy.deepcopy(permission._TRANSPORTS);permission._TRANSPORTS.clear()
        try:
            n.validate(data['candidates'][A],data['slot_catalog'],corpus=data)
            n.compact(data['candidates'][A],data)
            self.assertEqual(permission._TRANSPORTS,{})
            self.assertFalse(n.admission(entries(data,frozen)[0],frozen)['allowed'])
        finally:permission._TRANSPORTS.update(saved)
    def test_production_runtime_loader_issues_only_after_verified_generation(self):
        import shutil,tempfile,json
        from pathlib import Path
        import photo_runtime_sources as runtime
        from photo_search_reader import SearchReader
        from tests.test_photo_native_owner_selection import owner_pack,texture_source,chosen_composition
        with tempfile.TemporaryDirectory() as temporary:
            directory=Path(temporary);_,pack,lazy,query=owner_pack(directory)
            self.addCleanup(lazy.reader.close)
            data=texture_source();data['policies']=copy.deepcopy(lazy['policies'])
            self.assertEqual(c.digest(data),lazy['_corpus_sha256'])
            root=directory/'trusted-source'
            for name in ['scripts','precore']:
                shutil.copytree(runtime.SKILL_ROOT/name,root/name,ignore=shutil.ignore_patterns('__pycache__'))
            assets=root/'assets';shutil.copytree(lazy.reader.assets,assets)
            modules=[]
            for field,schema in c.MODULE_SCHEMAS.items():
                filename='photo_candidate_'+field+'.json';modules.append({'file':filename,'kind':field})
                (assets/filename).write_bytes(c.canonical_bytes({'schema':schema,field:data[field]}))
            (assets/c.MANIFEST_NAME).write_bytes(c.canonical_bytes({'schema':c.MANIFEST_SCHEMA,'modules':modules}))
            provider=runtime.RuntimeSnapshotProvider(root,directory/'isolated-store');provider.publisher.publish()
            permission._TRANSPORTS.clear()
            raw=SearchReader(assets);raw.close();self.assertEqual(permission._TRANSPORTS,{})
            snapshot=provider.acquire();self.addCleanup(snapshot.data.reader.close)
            qualified=[r for r in snapshot.data['_guard_source']['candidates'].values() if n.native_status(r)=='qualified']
            self.assertTrue(qualified);self.assertTrue(all(permission.transport(r)for r in qualified))
            composed=chosen_composition(pack,snapshot.data)
            report=audit.audit_composed_prompt(pack,composed,source_data=snapshot.data,query_context=query)
            self.assertEqual(report['status'],'pass',report)

    def test_public_review_packet_is_mechanical_and_not_a_plan_capability(self):
        data=source_fixture();frozen=core_fixture();entry=entries(data,frozen)[0]
        a,i,review,contracts=freeze_inputs(data,frozen,entry)
        inv=permission.freeze_permission_inventory(frozen,i,expected_inventory_sha256=c.digest(i),reviewer='independent pre-discovery reviewer')
        packet=permission.prepare_permission_review(a,inv,frozen,[entry],contracts=contracts)
        self.assertFalse(packet['manual_impact_decisions_authored']);self.assertFalse(packet['native_approval'])
        self.assertEqual(c.digest(packet['source_bindings']),review['source_bindings_sha256'])
        self.assertEqual(packet['whole_selected_source_contexts'][A]['source_record'],data['candidates'][A])
        with self.assertRaises(ValueError):
            with permission.trusted_permission_session(a,packet):pass

    def test_every_scalar_preservation_needs_declared_final_obligation(self):
        data=source_fixture();r=data['candidates'][A];d=r['content']['permission_envelope'];d['realizations']['base']['preservation']=[]
        r['content']['role_evidence']['permission_envelopes']=copy.deepcopy(d);seal(data,{'fixture_shot':['macroE']})
        with self.assertRaisesRegex(ValueError,'every source scalar preservation'):c.validate(data)

if __name__=='__main__':unittest.main()
