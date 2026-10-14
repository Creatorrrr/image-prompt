"""B2 source-qualified scopes; synthetic fixtures grant no actual source approval."""
import copy
import unittest
from unittest import mock
from tests import test_photo_native_member_scope_resolution as neutral
from tests.test_photo_semantic_evidence import A,source,fact,seal,core as scalar_core,reviewed_source,assertion
from tests.test_photo_native_compound_evidence import B,dependencies
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_semantic_evidence as e
import photo_search_layout as layout
import photo_native_owner_resolution as resolver


def endpoint(target,cid=A):return {'kind':'source_target','candidate_id':cid,'target':target}
def each(rule,*,cid=A,target='surfaces'):
    return {'id':'every_owned_surface','kind':'for_each_member','scope':endpoint(target,cid),
        'member_variable':'member','rule':rule}
def member():return {'kind':'bound_member','variable':'member'}
def scope_source(*,cid=A,receivers=(),guard=True,mode='effect',prerequisite=True,preserve=True):
    facts=[]
    if prerequisite:facts.append(fact('kind','subject','surfaces','entity.kind','prerequisite','garment',[]))
    if preserve:facts.append(fact('present','subject','surfaces','entity.presence','preservation','present',[]))
    facts.append(fact('gloss','material','surfaces','surface.optical_response',mode,'glossy',
        ['kind'] if prerequisite else [],operation='set_value',receivers=list(receivers)))
    bindings=[{'target':'surfaces','origin':'existing','introduced_by':None,'selector':{
        'kind':'selected_existing_member_scope','scope_schema':e.witnesses.MEMBER_SCOPE_SCHEMA,
        'target_semantics':'each_member','receiver_semantics':'all_members'}}]
    if guard or 'holder' in receivers:bindings.append({'target':'holder','origin':'existing','introduced_by':None,'selector':{'kind':'core_role','role':'main_subject'}})
    data=source('Each existing garment surface remains its declared garment kind and present; set every surface glossy while preserving its existing holder ownership.',facts,
        {'surface_material':slot('surface_material',['material'],property_prefixes=['surface.optical_response'])},
        {'base':{'schema':e.MEMBER_OWNER_SCHEMA,'bindings':bindings}})
    rec=data['candidates'].pop(A);rec['id']=cid;data['candidates'][cid]=rec
    if guard:rec['conditions']={'native_guards':{'schema':e.MEMBER_GUARD_SCHEMA,'rules':[each({
        'id':'owned','kind':'owner_relation','relation':'part_of','left':member(),'right':endpoint('holder',cid)},cid=cid)]}}
    return seal(data,{'surface_material':['gloss']},cid=cid)

def scope_core():
    value=neutral.core()
    value['semantic_assertions'] += [neutral.assertion('kind_'+str(i),'fact',owner=owner,property='entity.kind',value_type='entity.kind/v1',value='garment')
        for i,owner in enumerate(['coat_A','glove_A'])]
    value['semantic_assertions'] += [neutral.assertion('owned_'+str(i),'part_of',left=owner,right='holder_A') for i,owner in enumerate(['coat_A','glove_A'])]
    value['semantic_assertions'].append(neutral.assertion('separate_members','disjoint',left='coat_A',right='glove_A'))
    return neutral.reseal(value)

def choices(data,core,*,cid=A,rid='base',scope_id='local_members'):
    frozen=e.frozen_witnesses(core);scope=next(row for row in frozen['member_scopes'] if row['scope_id']==scope_id)
    p=data['candidates'][cid]['content']['role_evidence']
    return {'schema':e.MEMBER_SELECTION_SCHEMA,'core_sha256':core['canonical_sha256'],'owner_graph_sha256':c.digest(frozen['graph']),
        'member_scopes_sha256':c.digest(frozen['member_scopes']),'entries':[{'candidate_id':cid,'realization_id':rid,
            'meaning_sha256':p['meaning_sha256'],'qualification_sha256':c.digest(p),'bindings':[{'target':'surfaces','selection':{
                'kind':'existing_member_scope','scope_id':scope_id,'scope_sha256':c.digest(scope)}}]}]}

def entries(data,core,*,mapping=True,cid=A,**kwargs):
    selected=choices(data,core,cid=cid) if mapping is True else mapping if mapping is not False else None
    return [c.entry(data,cid,realization_id='base',owner_selections=selected,**kwargs),
        c.entry({**data,'candidates':{**data['candidates'],cid:layout.guard_record(data['candidates'][cid],data)}},cid,
            realization_id='base',owner_selections=selected,**kwargs)]


class ExistingMemberScopeTests(unittest.TestCase):
    def test_full_and_sealed_compact_share_one_view_and_all_frozen_members(self):
        data=scope_source();core=scope_core();c.validate(data);results=[]
        for entry in entries(data,core):
            with mock.patch.object(resolver,'resolve_selected_contracts',wraps=resolver.resolve_selected_contracts) as call:
                receipt=e.admission(entry,core)
                self.assertTrue(receipt['allowed'],receipt);self.assertEqual(call.call_count,1)
            self.assertEqual(len(receipt['resolved_frozen_facts']),4)
            rule=receipt['native_guards']['rules'][0]
            self.assertEqual([x['member']['owner_id'] for x in rule['member_results']],['coat_A','glove_A'])
            self.assertEqual(rule['status'],'verified')
            self.assertEqual({x['target'] for x in e.permission_scope(entry,core)[1]},{'coat_A','glove_A'})
            results.append(receipt)
        self.assertEqual(*results)

    def test_last_member_wrong_missing_P_or_PR_is_not_witnessed_by_first(self):
        data=scope_source()
        for prop in ['entity.kind','entity.presence']:
            for defect in ['wrong','missing']:
                core=scope_core();rows=core['semantic_assertions']
                row=next(x for x in rows if x['axes'].get('owner')=='glove_A' and x['axes'].get('property')==prop)
                if defect=='missing':rows.remove(row)
                else:row['axes']['value']='other'
                neutral.reseal(core)
                with self.subTest(prop=prop,defect=defect):
                    for entry in entries(data,core):self.assertFalse(e.admission(entry,core)['allowed'])

    def test_missing_discovery_vs_bad_supplied_or_strict_final(self):
        data=scope_source();core=scope_core()
        for entry in entries(data,core,mapping=False):
            probe=e.admission(entry,core,allow_unselected=True);self.assertTrue(probe['allowed'],probe);self.assertTrue(probe['search_only'])
            self.assertFalse(e.admission(entry,core)['allowed']);self.assertRaises(ValueError,e.permission_scope,entry,core)
        for defect in ['scope','table','core','graph','source','proof','empty','foreign']:
            mapping=choices(data,core)
            if defect=='scope':mapping['entries'][0]['bindings'][0]['selection']['scope_sha256']='0'*64
            elif defect=='table':mapping['member_scopes_sha256']='0'*64
            elif defect=='core':mapping['core_sha256']='0'*64
            elif defect=='graph':mapping['owner_graph_sha256']='0'*64
            elif defect=='source':mapping['entries'][0]['meaning_sha256']='0'*64
            elif defect=='proof':mapping['entries'][0]['qualification_sha256']='0'*64
            elif defect=='empty':mapping['entries'][0]['bindings']=[]
            else:mapping['entries'][0]['bindings'][0]['target']='foreign'
            for entry in entries(data,core,mapping=mapping):
                with self.subTest(defect=defect):self.assertFalse(e.admission(entry,core,allow_unselected=True)['allowed'])

    def test_last_member_guard_relation_and_frozen_value_are_all_required(self):
        data=scope_source();core=scope_core()
        core['semantic_assertions']=[x for x in core['semantic_assertions'] if x['assertion_id']!='owned_1'];neutral.reseal(core)
        for entry in entries(data,core):self.assertFalse(e.admission(entry,core)['allowed'])
        data=scope_source();rec=data['candidates'][A]
        rec['conditions']['native_guards']['rules']=[each({'id':'is_garment','kind':'frozen_value','owner':member(),
            'dimension':'subject','property':'entity.kind','value':{'type':'entity.kind/v1','value':'garment'}})]
        seal(data,{'surface_material':['gloss']});c.validate(data);core=scope_core()
        for entry in entries(data,core):self.assertTrue(e.admission(entry,core)['allowed'])
        next(x for x in core['semantic_assertions'] if x['assertion_id']=='kind_1')['axes']['value']='stone';neutral.reseal(core)
        for entry in entries(data,core):self.assertFalse(e.admission(entry,core)['allowed'])

    def test_quantified_frozen_entity_relation_uses_each_actual_rhs_canonical_owner(self):
        data=scope_source();rec=data['candidates'][A];rec['conditions']['native_guards']['rules']=[each({
            'id':'worn_by','kind':'frozen_entity_relation','left':member(),'right':endpoint('holder'),
            'dimension':'subject','property':'entity.owner_id','value_type':'entity.owner_id/v1'})]
        seal(data,{'surface_material':['gloss']});c.validate(data);core=scope_core()
        for i,owner in enumerate(['coat_A','glove_A']):core['semantic_assertions'].append(neutral.assertion('holder_'+str(i),'fact',owner=owner,
            property='entity.owner_id',value_type='entity.owner_id/v1',value='holder_A'))
        neutral.reseal(core)
        for entry in entries(data,core):self.assertTrue(e.admission(entry,core)['allowed'])
        core['semantic_assertions'][-1]['axes']['value']='image_A';neutral.reseal(core)
        for entry in entries(data,core):self.assertFalse(e.admission(entry,core)['allowed'])

    def test_every_receiver_and_equal_value_locked_E_is_still_denied(self):
        from photo_contracts import property_effects_allowed
        data=scope_source(receivers=['holder']);core=scope_core()
        for target in ['glove_A','holder_A']:
            locked=copy.deepcopy(core);locked['intent_lock']['semantic_anchors']=[{'dimension':'material','target':target,'property':'surface.optical_response'}];neutral.reseal(locked)
            for entry in entries(data,locked):
                self.assertTrue(e.admission(entry,locked)['allowed'])
                dims,props,graph=e.permission_scope(entry,locked)
                self.assertEqual({p['target'] for p in props},{'coat_A','glove_A','holder_A'})
                self.assertFalse(property_effects_allowed(locked['intent_lock'],dims,props,owner_graph=graph))
                self.assertFalse(e.property_scope_allowed(locked,dims,props,record=entry))

    def test_source_coverage_and_self_hashed_caller_projection_do_not_qualify(self):
        data=scope_source();c.validate(data);entry=entries(data,scope_core())[0]
        bad=copy.deepcopy(entry);proof=e.proof_of(bad);proof['facts']=[x for x in proof['facts'] if x['mode']!='effect']
        proof['compact_sha256']=c.digest({k:v for k,v in proof.items() if k!='compact_sha256'})
        self.assertFalse(e.admission(bad,scope_core())['allowed'])
        fake=neutral.node([neutral.scope_binding(scope_core())],[neutral.fact()])
        self.assertFalse(e.admission({'_semantic_evidence_guard':fake},scope_core())['allowed'])

    def test_quantifier_shapes_scalar_lifting_and_introduced_origin_fail(self):
        for defect in ['schema_v2','nested','unused_variable','unbound','scalar_scope','point_collection','origin','mode']:
            data=scope_source();p=data['candidates'][A]['content']['role_evidence'];rec=data['candidates'][A];rule=rec['conditions']['native_guards']['rules'][0]
            if defect=='schema_v2':rec['conditions']['native_guards']['schema']=e.SOURCE_TARGET_GUARD_SCHEMA
            elif defect=='nested':rule['rule']=copy.deepcopy(rule)
            elif defect=='unused_variable':rule['rule']['left']=endpoint('holder')
            elif defect=='unbound':rule['rule']['left']['variable']='other'
            elif defect=='scalar_scope':rec['conditions']['native_guards']['rules']=[{'id':'bad','kind':'owner_relation','relation':'part_of','left':endpoint('surfaces'),'right':endpoint('holder')}]
            elif defect=='point_collection':rule['scope']=endpoint('holder')
            elif defect=='origin':p['owner_maps']['base']['bindings'][0].update(origin='introduced',introduced_by='gloss')
            else:p['owner_maps']['base']['bindings'][0]['selector']['target_semantics']='collective'
            with self.subTest(defect=defect),self.assertRaises((ValueError,TypeError)):
                seal(data,{'surface_material':['gloss']});c.validate(data)

    def test_guard_support_v1_never_certifies_v3_quantified_role(self):
        from tests.test_photo_native_guard_role_support import support
        data=scope_source();p=data['candidates'][A]['content']['role_evidence']
        p['guard_supports']=[support(data,projection={'dimension':'material','target':'surfaces','property':'surface.optical_response'})]
        p['review']['native_review']['native_contract_sha256']=e.native_contract_sha256(p)
        self.assertRaisesRegex(ValueError,'unsupported predicate',c.validate,data)

    def test_old_fixed_point_receipt_and_compact_literal_remain_exact(self):
        from tests.test_photo_native_guard_role_support import GuardRoleSupportTests
        GuardRoleSupportTests.test_old_no_extra_fields_bytes_hashes_fit_and_receipts_stay_exact(self)
        data=reviewed_source();entry=c.entry(data,A);core=scalar_core(['main_subject'])
        with mock.patch.object(resolver,'resolve_selected_contracts',wraps=resolver.resolve_selected_contracts) as call:
            self.assertTrue(e.admission(entry,core)['allowed']);self.assertEqual(call.call_count,1)

    def test_scope_is_not_scalar_and_supplied_bad_hash_never_falls_back(self):
        data=scope_source();core=scope_core();entry=entries(data,core)[0]
        self.assertRaises(ValueError,e.resolve_owner_bindings,e.proof_of(entry),'base',e.frozen_witnesses(core)['graph'],core=core,owner_selections=choices(data,core))
        core['canonical_sha256']='0'*64
        self.assertFalse(e.admission(entry,core)['allowed'])

if __name__=='__main__':unittest.main()
