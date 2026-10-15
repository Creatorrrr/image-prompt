"""Direct, executed relation support; synthetic fixtures never approve a CID."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock

from tests.test_photo_semantic_evidence import A,source,owner_map,seal,reattest,core,assertion,reviewed_source
from tests.test_photo_native_compound_evidence import B,dependencies
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_candidate_realizations as r
import photo_semantic_evidence as e
import photo_search_layout as layout
import photo_role_proposals as proposals
import photo_slot_semantics as semantics
import photo_native_pack as packs
import audit_composed_prompt as audit
import prompt_generator as g


def endpoint(target,cid=A):return {'kind':'source_target','candidate_id':cid,'target':target}


def support(data,*,cid=A,rid='base',index=0,pointer='/content/en',quote=None,
            projection=None,targets=None,fid='owned_relation'):
    rec=data['candidates'][cid];p=rec['content']['role_evidence']
    conditions=p['guard_sets'][rid]['source_conditions'][index]
    block=conditions['native_guards'];rule=block['rules'][0]
    v2=block['schema']==e.SOURCE_TARGET_GUARD_SCHEMA
    return {'schema':e.GUARD_SUPPORT_SCHEMA,'id':fid,'realization_id':rid,
        'pointer':pointer,'quote':quote or e.positive_string(rec,pointer,realization_id=rid),
        'mode':'prerequisite','guard':{'schema':block['schema'],'declaring_candidate_id':cid,
            'declaring_realization_id':rid,'source_condition_index':index,
            'conditions_sha256':c.digest(conditions),'rule_id':rule['id'],'rule_sha256':c.digest(rule)},
        'endpoints':targets or ({key:{field:rule[key][field] for field in ('candidate_id','target')}
            for key in ('left','right')} if v2 else
            {'left_role':{'candidate_id':cid,'target':'face'},'right_role':{'candidate_id':cid,'target':'actor'}}),
        'semantic_projection':projection or {'dimension':'body_geometry','target':'face','property':'anatomy.connection.ownership'}}


def attach(data,rows,tag,*,cid=A):
    p=data['candidates'][cid]['content']['role_evidence'];p['guard_supports']=rows
    for unit in p['source_units']:
        refs=[row['id'] for row in rows if row['realization_id']==unit['realization_id'] and row['pointer']==unit['pointer']]
        if refs:unit.update(disposition='semantic',guard_refs=refs)
    ids=sorted({row['realization_id'] for row in rows})
    p['roles'][tag]={'spec_sha256':c.digest(data['slot_catalog'][tag]),
        'scope':'whole_record' if set(ids)==set(r.ids(data['candidates'][cid])) else 'positive_alternative',
        'realization_ids':ids,'fact_refs':[],'guard_refs':[row['id'] for row in rows],'support_modes':['prerequisite']}
    reattest(data,cid)
    from tests.test_photo_semantic_evidence import trust_fixture_authority
    trust_fixture_authority(data)
    return data


def relation_source(schema='v1',kind='owner_relation',relation='part_of',cid=A):
    text='The existing face is part of its already declared actor.'
    projection={'dimension':'body_geometry','target':'face','property':'anatomy.connection.ownership'}
    if kind=='frozen_entity_relation':
        text='The existing face has the declared holder link to its existing actor.'
        projection={'dimension':'relationship','target':'face','property':'relationship.fixture_holder'}
    elif relation=='disjoint':
        text='The existing face and the other existing actor are explicitly separate.'
        projection={'dimension':'relationship','target':'face','property':'relationship.fixture_distinct'}
    tag='anatomical_connection' if projection['dimension']=='body_geometry' else 'fixture_relation'
    data=source(text,[],{tag:slot(tag,[projection['dimension']],property_prefixes=[projection['property']])},
        {'base':owner_map(('face','primary_face'),('actor','main_subject'))})
    rec=data['candidates'].pop(A);rec['id']=cid;data['candidates'][cid]=rec
    rule={'id':'declared_relation','kind':kind}
    if schema=='v1':rule.update(left_role='primary_face',right_role='main_subject')
    else:rule.update(left=endpoint('face',cid),right=endpoint('actor',cid))
    if kind=='owner_relation':rule['relation']=relation
    else:rule.update(dimension=projection['dimension'],property=projection['property'],value_type='entity.owner_id/v1')
    rec['conditions']={'native_guards':{'schema':e.SOURCE_GUARD_SCHEMA if schema=='v1' else e.SOURCE_TARGET_GUARD_SCHEMA,'rules':[rule]}}
    seal(data,{},cid=cid)
    return attach(data,[support(data,cid=cid,projection=projection)],tag,cid=cid)


def relation_core(relation='part_of',*,frozen_link=False,alias=False):
    frozen=core(['actual_face','actual_actor'],edges=[(relation,'actual_face','actual_actor')] if not frozen_link else [],
        role_bindings={'primary_face':'actual_face','main_subject':'actual_actor'})
    if frozen_link:
        frozen['intent_lock']['locked_dimensions'].append('relationship')
        target='actual_actor'
        if alias:
            frozen['semantic_assertions'] += [assertion('alias_owner','owner',owner='actor_alias',owner_kind='entity'),
                assertion('explicit_alias','equivalent',left='actor_alias',right='actual_actor')]
            target='actor_alias'
        frozen['semantic_assertions'].append(assertion('frozen_holder','fact',dimension='relationship',owner='actual_face',
            property='relationship.fixture_holder',value_type='entity.owner_id/v1',value=target))
    return frozen


def entries(data,cid=A,rid='base',**kwargs):
    return [c.entry(data,cid,realization_id=rid,**kwargs),
        c.entry({**data,'candidates':{**data['candidates'],cid:layout.guard_record(data['candidates'][cid],data)}},
            cid,realization_id=rid,**kwargs)]


class GuardRoleSupportTests(unittest.TestCase):
    def test_absent_guard_supports_preserves_independent_source_unit_validation(self):
        # This existing helper accepts a local unit inventory, before a full
        # proof/CID/review envelope is available. The opt-in cannot require one.
        record={'content':{'en':'A directly named blue surface.'}}
        fact={'id':'blue','realization_id':'base','pointer':'/content/en','quote':'blue surface'}
        unit={'realization_id':'base','pointer':'/content/en','quote':record['content']['en'],
            'fact_refs':['blue'],'disposition':'semantic'}
        proof={'source_units':[unit]}
        e._validate_source_units(record,proof,{'blue':fact},'base')
        unit['fact_refs']=['unknown']
        self.assertRaisesRegex(ValueError,'foreign fact/source',e._validate_source_units,
            record,proof,{'blue':fact},'base')

    def test_guard_only_positive_field_full_compact_rolefit_and_actual_receipts(self):
        for schema in ['v1','v2']:
            data=relation_source(schema);c.validate(data);p=data['candidates'][A]['content']['role_evidence']
            self.assertEqual(p['facts'],[]);self.assertEqual(p['source_units'][0]['fact_refs'],[])
            spec=data['slot_catalog']['anatomical_connection'];full=semantics.fit(spec,data['candidates'][A],'')
            self.assertTrue(full['guard_admission_required']);self.assertEqual(full['matched_properties'],[])
            self.assertEqual(full['support_modes'],['prerequisite'])
            self.assertEqual(full,semantics.fit(spec,layout.guard_record(data['candidates'][A],data),''))
            receipts=[]
            for entry in entries(data):
                result=e.admission(entry,relation_core());self.assertTrue(result['allowed'],result)
                item=result['resolved_guard_supports'][0];self.assertEqual(item['guard_support_id'],'owned_relation')
                self.assertEqual(item['execution']['declaring_candidate_id'],A)
                self.assertEqual(item['execution']['source_condition_index'],0)
                self.assertEqual(item['execution']['guard_schema'],'photo-native-source-guards/'+schema)
                self.assertEqual(e.permission_scope(entry,relation_core())[:2],([],[]))
                receipts.append(result)
                self.assertFalse(e.admission(entry,relation_core('disjoint'))['allowed'])
            self.assertEqual(*receipts)
            proposal=proposals.propose(data,'anatomical_connection',A,[])
            self.assertTrue(proposal['semantic_fit']['guard_admission_required'])
            proposals.validate(data,proposal,[])

    def test_executed_predicate_not_allowed_boolean_or_other_layer_receipt(self):
        data=relation_source();entry=entries(data)[0];real=e.evaluate_native_guards
        for defect in ['boolean','other_layer','rule_hash','condition_hash','owner','graph_hash','source','missing_status','missing_core_receipt']:
            def forged(*args,**kwargs):
                value=real(*args,**kwargs)
                if defect=='boolean':return {'allowed':True,'rules':[],'search_only':False}
                row=value['rules'][0]
                if defect=='other_layer':row['source_condition_index']=1
                elif defect=='rule_hash':row['rule_sha256']='0'*64
                elif defect=='condition_hash':row['conditions_sha256']='0'*64
                elif defect=='owner':row['owners']['left_role']='actual_actor'
                elif defect=='graph_hash':row['owner_graph_sha256']='0'*64
                elif defect=='source':row['declaring_candidate_id']=B
                elif defect=='missing_status':row.pop('status')
                else:row['canonical_owners']={}
                return value
            with self.subTest(defect=defect),mock.patch.object(e,'evaluate_native_guards',side_effect=forged):
                self.assertFalse(e.admission(entry,relation_core())['allowed'])

    def test_explicit_disjoint_and_frozen_entity_relation_v1_raw_v2_canonical(self):
        for schema in ['v1','v2']:
            data=relation_source(schema,relation='disjoint');c.validate(data)
            for entry in entries(data):
                self.assertTrue(e.admission(entry,relation_core('disjoint'))['allowed'])
                self.assertFalse(e.admission(entry,relation_core())['allowed'])
            data=relation_source(schema,kind='frozen_entity_relation');c.validate(data)
            for entry in entries(data):
                for alias,expected in [(False,True),(True,schema=='v2')]:
                    result=e.admission(entry,relation_core(frozen_link=True,alias=alias))
                    self.assertEqual(result['allowed'],expected,result)
                    if expected:self.assertEqual(result['resolved_guard_supports'][0]['execution']['core_assertion_id'],'frozen_holder')
                frozen=relation_core(frozen_link=True);frozen['semantic_assertions'][-1]['axes']['value']='actual_face'
                self.assertFalse(e.admission(entry,frozen)['allowed'])

    def test_direct_quote_source_unit_and_no_scalar_fact_borrowing(self):
        for defect in ['quote','negative','foreign_pointer','no_unit','unit_other_pointer','unit_foreign_ref',
                       'nonsemantic','reference_only','empty_guard_refs','empty_facts_without_guard','fake_scalar_ref']:
            data=relation_source();p=data['candidates'][A]['content']['role_evidence'];row=p['guard_supports'][0];unit=p['source_units'][0]
            if defect=='quote':row['quote']='unknown invented anatomy'
            elif defect=='negative':
                data['candidates'][A]['content']['aliases']=['The face belongs to actor.'];row.update(pointer='/content/aliases/0',quote='face')
            elif defect=='foreign_pointer':row['pointer']='/content/realization_content/foreign/en'
            elif defect=='no_unit':unit.pop('guard_refs');unit['disposition']='nonsemantic'
            elif defect=='unit_other_pointer':unit['pointer']='/content/ko'
            elif defect=='unit_foreign_ref':unit['guard_refs']=['foreign']
            elif defect=='nonsemantic':unit['disposition']='nonsemantic'
            elif defect=='reference_only':unit.update(disposition='semantic_reference',reference_relation='same_selected_owner',retained_constraint_rationale='reference only')
            elif defect=='empty_guard_refs':unit['guard_refs']=[]
            elif defect=='empty_facts_without_guard':unit.pop('guard_refs')
            else:unit['fact_refs']=['owned_relation']
            reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)

    def test_source_guard_locator_rid_schema_endpoints_and_modes_fail_closed(self):
        for defect in ['cid','rid','index_bool','index','condition','rule','schema','kind','endpoint','origin',
                       'projection_target','dimension','property','mode','extra','duplicate','empty','ref','role_prefix','role_mode','extra_role_mode']:
            data=relation_source();rec=data['candidates'][A];p=rec['content']['role_evidence'];row=p['guard_supports'][0];role=p['roles']['anatomical_connection']
            if defect=='cid':row['guard']['declaring_candidate_id']=B
            elif defect=='rid':row['realization_id']='foreign'
            elif defect=='index_bool':row['guard']['source_condition_index']=False
            elif defect=='index':row['guard']['source_condition_index']=1
            elif defect=='condition':row['guard']['conditions_sha256']='0'*64
            elif defect=='rule':row['guard']['rule_sha256']='0'*64
            elif defect=='schema':row['guard']['schema']=e.SOURCE_TARGET_GUARD_SCHEMA
            elif defect=='kind':
                rec['conditions']['native_guards']['rules'][0]={'id':'declared_relation','kind':'frozen_value','owner_role':'main_subject','dimension':'subject','property':'entity.presence','value':{'type':'entity.presence/v1','value':'present'}}
                p['guard_sets']['base']=e.source_guard_set(rec,'base',data)
                row['guard'].update(conditions_sha256=c.digest(rec['conditions']),rule_sha256=c.digest(rec['conditions']['native_guards']['rules'][0]))
                p['meaning_sha256']=e.meaning_sha256(rec)
            elif defect=='endpoint':row['endpoints']['left_role']['target']='actor'
            elif defect=='origin':p['owner_maps']['base']['bindings'][0].update(origin='introduced',introduced_by='missing')
            elif defect=='projection_target':row['semantic_projection']['target']='unbound'
            elif defect=='dimension':row['semantic_projection']['dimension']='action'
            elif defect=='property':row['semantic_projection']['property']='body.form'
            elif defect=='mode':row['mode']='effect'
            elif defect=='extra':row['value']={'type':'fake/v1','value':'present'}
            elif defect=='duplicate':p['guard_supports'].append(copy.deepcopy(row))
            elif defect=='empty':p['guard_supports']=[]
            elif defect=='ref':role['guard_refs']=['foreign']
            elif defect=='role_prefix':role['spec_sha256']='0'*64
            elif defect=='role_mode':role['support_modes']=['effect']
            else:role['support_modes']=['prerequisite','effect']
            reattest(data)
            with self.subTest(defect=defect):self.assertRaises(ValueError,c.validate,data)

    def test_frozen_relation_cannot_relabel_actual_taxonomy_or_use_boolean_evidence(self):
        data=relation_source('v2',kind='frozen_entity_relation');p=data['candidates'][A]['content']['role_evidence']
        p['guard_supports'][0]['semantic_projection']['property']='relationship.different';reattest(data)
        self.assertRaises(ValueError,c.validate,data)

    def test_guard_support_ids_bounds_and_projection_types_are_explicit(self):
        for defect in ['rid_limit','total_limit','scalar_id_collision','projection_type','projection_value']:
            data=relation_source();p=data['candidates'][A]['content']['role_evidence']
            if defect in {'rid_limit','total_limit'}:
                count=e.MAX_RID_GUARD_SUPPORTS+1 if defect=='rid_limit' else e.MAX_GUARD_SUPPORTS+1
                p['guard_supports']=[{**copy.deepcopy(p['guard_supports'][0]),'id':'relation_'+str(i)} for i in range(count)]
            elif defect=='scalar_id_collision':p['guard_supports'][0]['id']='scalar_id';p['facts']=[{'id':'scalar_id'}]
            elif defect=='projection_type':p['guard_supports'][0]['semantic_projection']=[]
            else:p['guard_supports'][0]['semantic_projection']['dimension']=[]
            # These bounded local shape checks do not require a forged full
            # proof signature or fabricate a valid scalar fact.
            with self.subTest(defect=defect):self.assertRaises(ValueError,e._validate_guard_supports,p)

    def test_old_no_extra_fields_bytes_hashes_fit_and_receipts_stay_exact(self):
        # Independent old raw module 7d9f7e7c... from published 07143a62...;
        # exact inputs/outputs are frozen in the implementation portable-baseline
        # note. These expectations require no old cache, model, or network.
        data=reviewed_source();rec=data['candidates'][A];before=c.canonical_bytes(rec);c.validate(data)
        self.assertEqual(c.digest(rec),'ddd232f5f182431ac9de51d528e7c28404e7315ac0ec607c48de5e494cb4cd11')
        self.assertEqual(e.native_contract_sha256(rec['content']['role_evidence']),
            'd06822b7d4348deac6770eb14493b136f36ca72a7c788196dea67de3c6e3b02a')
        self.assertEqual(c.digest(e.compact(rec,data)),
            'cfd371fbb83dccceadc6bb3c89660093930b2703a1516cb6a492118f5fbc0c28')
        self.assertEqual(e.qualification(data['slot_catalog']['surface_material'],rec),{
            'status':'eligible','reason':'source_reviewed_mode_specific_evidence','native_qualification':'qualified',
            'matched_properties':[{'dimension':'material','target':'main_subject','property':'surface.material'}],
            'meaning_terms':[],'fact_refs':['satin'],'support_modes':['effect']})
        entry=c.entry(data,A);frozen=core(['main_subject'])
        self.assertEqual(e.admission(entry,frozen),{
            'status':'qualified','allowed':True,'reason':'whole_native_obligations_verified',
            'resolved_frozen_facts':[],'dependencies':[],'native_guards':{'allowed':True,
                'reason':'all_native_guards_verified','rules':[],'preserved_scopes':[],'search_only':False},
            'used_dependency_ids':[]})
        self.assertNotIn('resolved_guard_supports',e.admission(entry,frozen));self.assertEqual(before,c.canonical_bytes(rec))
        # Actual old v1 receipt keeps its original shape too.
        data=relation_source();p=data['candidates'][A]['content']['role_evidence'];p.pop('guard_supports');p['roles']={}
        p['owner_maps']['base']=owner_map();p['source_units'][0].pop('guard_refs');p['source_units'][0]['disposition']='nonsemantic';reattest(data)
        c.validate(data)
        from tests.test_photo_semantic_evidence import trust_fixture_authority
        trust_fixture_authority(data)
        entry=c.entry(data,A)
        self.assertEqual(c.digest(data['candidates'][A]),'21033d5d364addb53e267241234ddc46aae8f0bf8d204a35fe9c1c16e99a5c3b')
        self.assertEqual(e.admission(entry,relation_core()),{
            'status':'qualified','allowed':True,'reason':'whole_native_obligations_verified',
            'resolved_frozen_facts':[],'dependencies':[],'native_guards':{'allowed':True,
                'reason':'all_native_guards_verified','rules':[{'layer':0,'rule_id':'declared_relation',
                    'kind':'owner_relation','owners':{'left_role':'actual_face','right_role':'actual_actor'}}],
                'preserved_scopes':[],'search_only':False},'used_dependency_ids':[]})


class GuardRoleClosureTests(unittest.TestCase):
    def test_guard_support_keeps_scalar_prerequisites_effect_receivers_and_permission_locks(self):
        from tests import test_photo_native_source_guards_v2 as fixtures
        data=fixtures.hands_source();frozen=fixtures.hands_core();p=data['candidates'][A]['content']['role_evidence']
        scalar=c.canonical_bytes(p['facts']);effects=c.canonical_bytes(p['effect_sets'])
        data['slot_catalog']['anatomical_connection']=slot('anatomical_connection',['body_geometry'],
            property_prefixes=['anatomy.connection'])
        seal(data,{'pose':['holding']})
        row=support(data,projection={'dimension':'body_geometry','target':'hand_a','property':'anatomy.connection.ownership'})
        attach(data,[row],'anatomical_connection');c.validate(data)
        self.assertEqual(scalar,c.canonical_bytes(p['facts']));self.assertEqual(effects,c.canonical_bytes(p['effect_sets']))
        for entry in entries(data,owner_selections=fixtures.choices(data,frozen)):
            result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result)
            self.assertEqual(len(result['resolved_frozen_facts']),3)
            self.assertEqual(len(result['resolved_guard_supports']),1)
            self.assertEqual({x['target'] for x in e.permission_scope(entry,frozen)[1]},{'a2','b2','mug2'})
        for entry in entries(data):
            self.assertFalse(e.admission(entry,frozen)['allowed'])
            probe=e.admission(entry,frozen,allow_unselected=True)
            self.assertTrue(probe['search_only']);self.assertNotIn('resolved_guard_supports',probe)
            self.assertRaises(ValueError,e.permission_scope,entry,frozen)
        frozen['intent_lock']['semantic_anchors']=[{'dimension':'pose','target':'mug2','property':'body.pose'}]
        fixtures.sign_core(frozen)
        for entry in entries(data,owner_selections=fixtures.choices(data,frozen)):
            self.assertTrue(e.admission(entry,frozen)['allowed'])
            self.assertFalse(fixtures.SourceTargetGuardTests.eligible(self,data,frozen,entry))
        frozen['intent_lock']['semantic_anchors']=[]
        next(x for x in frozen['semantic_assertions'] if x['axes'].get('property')=='entity.kind' and x['axes'].get('owner')=='a2')['axes']['value']='stone'
        fixtures.sign_core(frozen)
        for entry in entries(data,owner_selections=fixtures.choices(data,frozen)):
            self.assertFalse(e.admission(entry,frozen)['allowed'])

    def test_source_common_support_binds_required_child_endpoint_to_exact_selected_closure(self):
        from tests import test_photo_native_source_guards_v2 as fixtures
        data=fixtures.compound();rec=data['candidates'][A]
        rec['content']['en']+=' The existing parent hand A is part of the explicitly selected child holder.'
        rec['conditions']['native_guards']['rules'].insert(0,fixtures.relation('parent_child_holder',
            endpoint('hand_a'),endpoint('holder',B)))
        data['slot_catalog']['anatomical_connection']=slot('anatomical_connection',['body_geometry'],property_prefixes=['anatomy.connection'])
        seal(data,{'pose':['holding']},cid=B);dependencies(data,A,'base',[B]);seal(data,{'pose':['holding']})
        row=support(data,quote='The existing parent hand A is part of the explicitly selected child holder.',
            projection={'dimension':'body_geometry','target':'hand_a','property':'anatomy.connection.ownership'})
        attach(data,[row],'anatomical_connection');c.validate(data);frozen=fixtures.hands_core()
        for background in [False,True]:
            for entry in entries(data,owner_selections=fixtures.compound_choices(data,frozen,background)):
                result=e.admission(entry,frozen);self.assertEqual(result['allowed'],not background,result)
                if not background:
                    receipt=result['resolved_guard_supports'][0]['execution']
                    self.assertEqual(receipt['endpoints']['right'],endpoint('holder',B))
                    self.assertEqual(receipt['owners']['right'],'secondary')
        bad=copy.deepcopy(data);p=bad['candidates'][A]['content']['role_evidence']
        p['guard_supports'][0]['guard']['declaring_candidate_id']=B;reattest(bad)
        self.assertRaises(ValueError,c.validate,bad)

    def test_compact_support_seal_covers_projection_locator_and_endpoint(self):
        data=relation_source('v2');c.validate(data);entry=entries(data)[1]
        for defect in ['projection','locator','endpoint','support_refs','empty_supports']:
            bad=copy.deepcopy(entry);p=e.proof_of(bad)
            if defect=='projection':p['guard_supports'][0]['semantic_projection']['property']='anatomy.connection.fake'
            elif defect=='locator':p['guard_supports'][0]['guard']['rule_sha256']='0'*64
            elif defect=='endpoint':p['guard_supports'][0]['endpoints']['left']['target']='actor'
            elif defect=='empty_supports':p['guard_supports']=[]
            else:p['roles']['anatomical_connection']['guard_refs']=[]
            with self.subTest(defect=defect):self.assertFalse(e.admission(bad,relation_core())['allowed'])

    def compound(self,optional):
        data=reviewed_source();child=relation_source('v2',cid=B)
        data['slot_catalog'].update(child['slot_catalog']);data['candidates'][B]=child['candidates'][B]
        # Refresh mechanical fixture catalog/signature bindings, not semantic rows.
        cp=data['candidates'][B]['content']['role_evidence'];cp['catalog_sha256']=c.digest(data['slot_catalog']);reattest(data,B)
        rec=data['candidates'][A];rec['record_kind']='visual_bundle';rec['content']['member_candidates']=[
            {'candidate_id':B,'adoption':'optional' if optional else 'required','requirements':{}}]
        dependencies(data,A,'base',[B])
        if optional:rec['content']['role_evidence']['dependencies']['base'][0]['selection']='explicit_optional'
        seal(data,{'surface_material':['satin']});c.validate(data);return data

    def test_required_selected_optional_and_unselected_member_do_not_borrow_roles(self):
        for optional in [False,True]:
            data=self.compound(optional);frozen=relation_core();frozen['semantic_assertions'].append(assertion('parent_role','role',role='secondary_subject',owner='actual_actor'))
            # Parent fixed main_subject resolves actual actor; no new scalar owner witness needed.
            for entry in entries(data,dependency_selections={B:'base'} if optional else {}):
                result=e.admission(entry,frozen);self.assertTrue(result['allowed'],result)
                self.assertEqual(result['dependencies'][0]['admission']['resolved_guard_supports'][0]['guard']['declaring_candidate_id'],B)
                self.assertFalse(e.admission(entry,relation_core('disjoint'))['allowed'])
            if optional:
                for entry in entries(data):
                    result=e.admission(entry,relation_core('disjoint'));self.assertTrue(result['allowed'],result)
                    self.assertEqual(result['dependencies'],[])
            self.assertEqual(e.qualification(data['slot_catalog']['anatomical_connection'],data['candidates'][A])['status'],'incompatible')

    def test_actual_branch_source_layer_cannot_borrow_common_or_sibling(self):
        data=relation_source('v2');rec=data['candidates'][A];p=rec['content']['role_evidence'];block=rec['conditions'].pop('native_guards')
        rec['effects']['realizations']={'mode':'one','branches':[{'id':rid,'conditions':{'native_guards':copy.deepcopy(block)},
            'context_terms':[],'effects':{'dimensions':[],'properties':[]}} for rid in ['left','right']]}
        p.pop('guard_supports');p['roles']={};p['owner_maps']={rid:owner_map(('face','primary_face'),('actor','main_subject')) for rid in ['left','right']}
        seal(data,{})
        rows=[support(data,rid=rid,index=1,fid='own_'+rid) for rid in ['left','right']];attach(data,rows,'anatomical_connection');c.validate(data)
        for rid in ['left','right']:
            for entry in entries(data,rid=rid):
                result=e.admission(entry,relation_core());self.assertTrue(result['allowed'],result)
                self.assertEqual(result['resolved_guard_supports'][0]['execution']['source_layer'],'source_branch')
                self.assertEqual(result['resolved_guard_supports'][0]['execution']['declaring_realization_id'],rid)
        p['guard_supports'][1]['guard']['declaring_realization_id']='left';reattest(data);self.assertRaises(ValueError,c.validate,data)

    def test_public_pack_roundtrip_carries_direct_full_support_without_role_source_copies(self):
        data=relation_source('v2');c.validate(data);proposal=proposals.propose(data,'anatomical_connection',A,[])
        working=packs.WorkingPack({'global_retrieval':{'role_proposals':{proposal['proposal_id']:proposal}}},
            {'anatomical_connection':{'candidates':[{'id':A,'proposal_id':proposal['proposal_id'],'realization_id':'base'}]}})
        public=packs.finalize(working,data,[A],None);packs.validate(public)
        decoded=json.loads(json.dumps(public));packs.validate(decoded)
        self.assertEqual(set(public['candidate_pool']),{A})
        self.assertEqual(public['candidate_pool'][A]['authored_record'],data['candidates'][A])
        self.assertEqual(packs.role_cards(decoded)['anatomical_connection']['candidates'][0]['proposal_id'],proposal['proposal_id'])
        before=c.canonical_bytes(decoded);decoded['authorial_core']=relation_core()
        composed={'chosen_candidate_ids':[A],'candidate_interpretations':[{'candidate_id':A,'realization_id':'base'}],
            'prompt_en':'The same existing face remains part of its declared actor.'}
        # This small core is a contract fixture; the separate real-freeze test
        # below exercises the complete authorial context without this stub.
        with mock.patch.object(g,'frozen_core_context',return_value=({'subject_category':'human','intent_constraints':{'domains':[]}}, {'subject':{}})):
            self.assertEqual(audit.audit_native_adoptions(decoded,composed,data),[])
            decoded['authorial_core']=relation_core('disjoint');self.assertTrue(audit.audit_native_adoptions(decoded,composed,data))
        decoded.pop('authorial_core');self.assertEqual(before,c.canonical_bytes(decoded))


def transport_source():
    from tests import test_photo_native_owner_selection as fixtures
    data=fixtures.texture_source();cid=fixtures.P;rec=data['candidates'][cid];p=rec['content']['role_evidence']
    rec['content']['en']+=' The existing selected leather surface is separate from the already declared primary subject.'
    p['owner_maps']['base']['bindings'].append({'target':'subject','origin':'existing','introduced_by':None,
        'selector':{'kind':'core_role','role':'main_subject'}})
    rec['conditions']={'native_guards':{'schema':e.SOURCE_TARGET_GUARD_SCHEMA,'rules':[{
        'id':'separate_from_primary','kind':'owner_relation','relation':'disjoint',
        'left':endpoint('surface',cid),'right':endpoint('subject',cid)}]}}
    data['slot_catalog']['carrier_relation']=slot('carrier_relation',['relationship'],property_prefixes=['relationship.carrier_distinct'])
    seal(data,{'texture':['cracks']},cid=cid)
    row=support(data,cid=cid,quote='The existing selected leather surface is separate from the already declared primary subject.',
        projection={'dimension':'relationship','target':'surface','property':'relationship.carrier_distinct'})
    return attach(data,[row],'carrier_relation',cid=cid)


class GuardRoleRealTransportTests(unittest.TestCase):
    def test_real_lazy_retrieval_immutable_public_pack_and_fresh_runtime_request(self):
        from tests import test_photo_native_owner_selection as fixtures
        data=transport_source();c.validate(data)
        with mock.patch.object(fixtures,'texture_source',return_value=data):
            fixtures.OwnerSelectionPackTests.test_real_freeze_retrieval_public_pack_stays_immutable_and_composed_audit_resolves(self)
            fixtures.OwnerSelectionFinalAuditTests.test_real_runtime_request_reaudits_exact_public_pack_and_composed_mapping(self)


if __name__=='__main__':unittest.main()
