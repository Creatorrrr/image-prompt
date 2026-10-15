"""Synthetic trusted-run integration; no actual source1299 approval or pixels."""
import copy
import hashlib
import unittest
from unittest import mock
from tests.test_photo_semantic_evidence import A, source, fact, seal, core, assertion, reattest
from tests.test_photo_native_source_guards_v2 import selected_map, choices
from tests.test_photo_native_owner_selection import sign_core
from tests.photo_native_schema import slot
import photo_candidate_corpus as c
import photo_semantic_evidence as n
import photo_native_permission as permission
import photo_permission_comparison as comparison
import photo_search_layout as layout
import prompt_generator as g
import audit_composed_prompt as audit


def source_fixture():
    text=('On the independently declared existing image select macro shot scale of the existing physical item. '
          'The same item remains visible in that selected image with a separate frozen framing.visible_in relation. '
          'Do not add an image, item, body or hidden part.')
    rows=[fact('itemP','subject','item','entity.presence','prerequisite','present',[],quote='existing physical item'),
          fact('imageP','subject','image','entity.presence','prerequisite','present',[],quote='independently declared existing image'),
          fact('visiblePR','framing','item','subject.visibility','preservation','visible',['itemP','imageP'],quote='same item remains visible in that selected image'),
          fact('macroE','framing','image','shot.scale','effect','macro',['itemP','imageP','visiblePR'],quote='select macro shot scale',operation='set_value',receivers=['item'])]
    data=source(text,rows,{'fixture_shot':slot('fixture_shot',['framing'],property_prefixes=['shot.scale'])},
                {'base':selected_map('item','image')})
    rec=data['candidates'][A];ep=lambda t:{'kind':'source_target','candidate_id':A,'target':t}
    rec['conditions']={'native_guards':{'schema':n.MEMBER_GUARD_SCHEMA,'rules':[{
        'id':'same_image','kind':'frozen_entity_relation','left':ep('item'),'right':ep('image'),
        'dimension':'framing','property':'framing.visible_in','value_type':'entity.owner_id/v1'}]}}
    contract={'canonical_effect_refs':['macroE'],'basis':[{'fact_ref':'macroE','unit_pointer':'/content/en',
          'rationale':'Manually read explicit macro selection; no alternate E or scope.'}],
        'preservation':[{'fact_ref':'visiblePR','image_target':'image','relation_guard_id':'same_image','relation_property':'framing.visible_in'}]}
    rec['content']['permission_envelope']={'schema':permission.SCHEMA,'realizations':{'base':contract}}
    rec['content']['role_evidence']['permission_envelopes']=copy.deepcopy(rec['content']['permission_envelope'])
    seal(data,{'fixture_shot':['macroE']});c.validate(data)
    return data


def core_fixture(image='I', visible='visible', *, anchor=None, part=False):
    text='The independent item X exists and is '+visible+' in image '+image+'. Images I and I2 exist separately. Macro framing is open.'
    frozen=core(['X','I','I2'],role_bindings={},open_dimensions=['framing'])
    frozen['subject']='Existing controlled item and images';frozen['baseline_prompt_en']=text;frozen['source_request']=text
    h=hashlib.sha256(text.encode()).hexdigest()
    frozen['request_binding']={'request_sha256':h,'request_envelope_sha256':c.digest({'text':text}),
        'input_inventory':{'schema':n.witnesses.INPUT_SCHEMA,'complete':True,'items':[{'id':'request','kind':'request_text','sha256':h}]},
        'active_spans':[{'span_id':'request_1','source_span_id':'request_1','text':text,'input_id':'request'}]}
    rows=frozen['semantic_assertions']
    for a in rows:a['evidence']={'meaning':text}
    for o in ['X','I','I2']:
        a=assertion('presence_'+o,'fact',owner=o,property='entity.presence',value_type='entity.presence/v1',value='present');a['evidence']={'meaning':text};rows.append(a)
    for aid,prop,typ,value in [('visible','subject.visibility','subject.visibility/v1',visible),('image_relation','framing.visible_in','entity.owner_id/v1',image)]:
        a=assertion(aid,'fact',dimension='framing',owner='X',property=prop,value_type=typ,value=value);a['evidence']={'meaning':text};rows.append(a)
    a=assertion('images_disjoint','disjoint',left='I',right='I2');a['evidence']={'meaning':text};rows.append(a)
    if part:
        a=assertion('item_part_image','part_of',left='X',right='I');a['evidence']={'meaning':text};rows.append(a)
    frozen['intent_lock']={'contract_version':'photo-intent-lock/v2','locked_dimensions':['subject','identity','count','age','event','concept'],
        'open_dimensions':['framing'],'semantic_anchors':[{'dimension':'framing','target':'X','property':'subject.visibility'}, {'dimension':'framing','target':'X','property':'framing.visible_in'}]+([] if anchor is None else [anchor])}
    return sign_core(frozen)


def entries(data,frozen):
    selected=choices(data,frozen,{'item':'X','image':'I'})
    full=c.entry(data,A,realization_id='base',owner_selections=selected)
    compact=c.entry({**data,'candidates':{A:layout.guard_record(data['candidates'][A],data)}},A,realization_id='base',owner_selections=selected)
    return full,compact


def freeze_inputs(data, frozen, entry, *, impact='disjoint'):
    """Serialization of manually enumerated synthetic protected whole meanings.

    The test author explicitly judges macro does not change already-declared
    identity/count/age/subject/event/concept. Custom anchor impact is a caller
    argument; unknown is never inferred disjoint from its spelling.
    """
    authority=permission.freeze_source_authority(data,expected_snapshot_sha256=c.digest(data),reviewer='independent synthetic source author')
    context=n._resolve_selected_native_contracts([entry],frozen);view=context['view'];graph=context['frozen']['graph']
    contracts={A:copy.deepcopy(data['candidates'][A]['content']['permission_envelope']['realizations']['base'])}
    a=permission._payload(authority,'source authority')
    bound,_=permission._source_context(a,context['nodes'][A],contracts[A]);pins={A:comparison.source_binding(bound)}
    inv={'schema':'research-independent-permission-inventory/v1','phase':'before_discovery','core_sha256':frozen['canonical_sha256'],
        'core_payload_sha256':c.digest(frozen),'input_binding':comparison.core_input_binding(frozen),'topology_sha256':c.digest(graph),
        'owners':list(graph['owners']),'scope_members':{},'anchors':comparison.anchors_from_core(frozen),
        'reviewed_input_ids':['request'],'reviewed_span_ids':['request_1'],'complete':True,'state':'known',
        'reviewer':'independent synthetic request reviewer','reason':'All three actual owners and every source input were explicitly reviewed before discovery.',
        'witnesses':[{'candidate_id':A,'source_fact_ref':'visiblePR','target':'X','image':'I','dimension':'framing',
          'property':'subject.visibility','value':{'type':'subject.visibility/v1','value':'visible'},'assertion_id':'visible','input_ids':['request'],'span_ids':['request_1'],'frozen':True}]}
    plan={'schema':'research-source-anchor-impact-review/v1','inventory_sha256':c.digest(inv),'resolved_view_sha256':c.digest(view),
        'source_bindings_sha256':c.digest(pins),'reviewer':'independent manual synthetic source review','anchors':[],'joint':[]}
    ef=next(f for f in view['nodes'][0]['expanded_facts'] if f['mode']=='effect')
    key=c.digest({k:ef[k] for k in ('candidate_id','realization_id','fact_id','expansion_index','target')})
    for anchor in inv['anchors']:
        whole=anchor['kind']=='whole_dimension'
        plan['anchors'].append({'effect_key':key,'anchor_key':c.digest(anchor),'impact':'disjoint' if whole else impact,
            'reason':'The manually read macro selection preserves independently declared whole entity identity/count/age/subject/event/concept.' if whole else 'Explicit independent custom-property impact judgment: '+impact,
            'input_ids':['request'],'span_ids':['request_1'],'preservation_ref':None})
    return authority,inv,plan,contracts


def freeze(data,frozen,entry,**kw):
    a,i,p,contracts=freeze_inputs(data,frozen,entry,**kw)
    return a,permission.freeze_permission_plan(a,frozen,[entry],inventory=permission.freeze_permission_inventory(frozen,i,expected_inventory_sha256=c.digest(i),reviewer='independent pre-discovery reviewer'),assessment=p,contracts=contracts,reviewer='independent plan author')


def after_evidence(plan):
    o=permission._payload(plan,'permission plan')['obligations'][0]
    return [{'candidate_id':A,'realization_id':'base','fact_ref':'visiblePR','original_assertion_sha256':o['core_assertion_sha256'],
        'original_relation_sha256':o['relation_assertion_sha256'],'scalar_assertion_id':'visible','relation_assertion_id':'image_relation'}]


class NativePermissionEnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.data=source_fixture();self.core=core_fixture();self.full,self.compact=entries(self.data,self.core)
    def eligible(self,entry,**kw):
        return g.core_entry_eligible(self.data,self.core,{'subject_category':'object','intent_constraints':{'domains':[]}}, {'subject':{}},'',entry,**kw)
    def test_missing_plan_denies_full_compact_consumer_and_no_scope_flag(self):
        for entry in [self.full,self.compact]:
            self.assertFalse(n.admission(entry,self.core)['allowed'])
            self.assertFalse(self.eligible(entry));self.assertFalse(self.eligible(entry,check_effect_scope=False))
            with self.assertRaises(ValueError):n.permission_scope(entry,self.core)
    def test_trusted_plan_full_compact_same_B1_receipt_and_original_scope(self):
        a,p=freeze(self.data,self.core,self.full)
        with permission.trusted_permission_session(a,p):
            receipts=[]
            for entry in [self.full,self.compact]:
                result=n.admission(entry,self.core);self.assertTrue(result['allowed'],result)
                receipts.append(result['permission_envelope']);self.assertTrue(self.eligible(entry))
                dims,props,_=n.permission_scope(entry,self.core)
                self.assertEqual(dims,['framing']);self.assertEqual({(v['target'],v['property']) for v in props},{('I','shot.scale'),('X','shot.scale')})
            self.assertEqual(receipts[0],receipts[1])
    def test_source_proof_symmetry_and_ordinary_basis(self):
        for defect in ['no_proof','no_declaration','changed_refs','reference_basis','extra_key']:
            data=copy.deepcopy(self.data);r=data['candidates'][A];p=r['content']['role_evidence']
            if defect=='no_proof':p.pop('permission_envelopes')
            elif defect=='no_declaration':r['content'].pop('permission_envelope')
            elif defect=='changed_refs':p['permission_envelopes']['realizations']['base']['canonical_effect_refs']=[]
            elif defect=='reference_basis':p['source_units'][0]['disposition']='semantic_reference'
            else:p['permission_envelopes']['extra']='unknown'
            p['meaning_sha256']=n.meaning_sha256(r);reattest(data)
            with self.subTest(defect=defect),self.assertRaises(ValueError):n.validate(r,data['slot_catalog'],corpus=data)
    def test_missing_proof_unqualified_required_source_is_rejected(self):
        data=copy.deepcopy(self.data);r=data['candidates'][A];r['content'].pop('role_evidence')
        n.validate(r,data['slot_catalog'],corpus=data)  # Source-only authoring remains unqualified.
        self.assertEqual(n.native_status(r),'unqualified')
        self.assertFalse(n.admission(r,self.core)['allowed'])
    def test_stale_source_core_choice_plan_and_candidate_injection(self):
        a,p=freeze(self.data,self.core,self.full)
        entry=copy.deepcopy(self.full);entry['permission_plan']=permission._payload(p,'permission plan')
        self.assertFalse(n.admission(entry,self.core)['allowed'])
        with self.assertRaises(TypeError):permission._Handle()
        with self.assertRaises(ValueError):permission.freeze_source_authority(self.data,expected_snapshot_sha256='a'*64,reviewer='reviewer')
        with permission.trusted_permission_session(a,p):
            changed=copy.deepcopy(self.core);changed['subject']+=' changed';sign_core(changed)
            self.assertFalse(n.admission(self.full,changed)['allowed'])
            wrong=copy.deepcopy(self.full);wrong['_native_owner_selections']['entries'][0]['bindings'][1]['owner_id']='I2'
            self.assertFalse(n.admission(wrong,self.core)['allowed'])
        self.assertFalse(n.admission(self.full,self.core)['allowed'])
    def test_inventory_incomplete_unknown_unread_owner_and_manual_pair_omission(self):
        for defect in ['incomplete','unknown','owner','input','span','pair']:
            a,i,p,cs=freeze_inputs(self.data,self.core,self.full)
            if defect=='incomplete':i['complete']=False
            elif defect=='unknown':i['state']='unknown'
            elif defect=='owner':i['owners'].remove('I2')
            elif defect=='input':i['reviewed_input_ids']=[]
            elif defect=='span':i['reviewed_span_ids']=[]
            else:p['anchors'].pop()
            p['inventory_sha256']=c.digest(i)
            with self.subTest(defect=defect),self.assertRaises(ValueError):permission.freeze_permission_plan(a,self.core,[self.full],inventory=permission.freeze_permission_inventory(self.core,i,expected_inventory_sha256=c.digest(i),reviewer='independent pre-discovery reviewer'),assessment=p,contracts=cs,reviewer='reviewer')
    def test_original_target_receiver_parent_whole_and_custom_locks(self):
        for anchor,impact in [({'dimension':'framing','target':'I','property':'shot'},'disjoint'),
                              ({'dimension':'framing','target':'X','property':'shot.scale'},'disjoint'),
                              ({'dimension':'framing','target':'I','property':'shot.*'},'disjoint'),
                              ({'dimension':'framing','target':'X','property':'custom.reflection'},'unknown'),
                              ({'dimension':'framing','target':'X','property':'custom.reflection'},'affects')]:
            frozen=core_fixture(anchor=anchor);entry=entries(self.data,frozen)[0]
            with self.subTest(anchor=anchor),self.assertRaises(ValueError):freeze(self.data,frozen,entry,impact=impact)
    def test_same_item_wrong_image_and_hidden_frozenPR_cannot_freeze(self):
        for image,visible in [('I2','visible'),('I','hidden')]:
            frozen=core_fixture(image,visible);entry=entries(self.data,frozen)[0]
            with self.subTest(image=image,visible=visible),self.assertRaises(ValueError):freeze(self.data,frozen,entry)
    def test_final_requires_independent_typed_after_state_and_source_receipt(self):
        a,p=freeze(self.data,self.core,self.full)
        with permission.trusted_permission_session(a,p):
            with self.assertRaises(ValueError):n.audit_final_scalar_preservation([self.full],self.core)
        state=core_fixture();result=permission.freeze_after_state(p,state,expected_after_sha256=c.digest(state),evidence=after_evidence(p),reviewer='independent result author')
        with permission.trusted_permission_session(a,p,after_state=result):
            for entry in [self.full,self.compact]:
                receipt=n.audit_final_scalar_preservation([entry],self.core)
                self.assertEqual(receipt['receipts'][0]['obligation']['target'],'X')
                self.assertEqual(receipt['receipts'][0]['obligation']['image'],'I')
                self.assertEqual(receipt['source_snapshot_sha256'],c.digest(self.data))
    def test_final_hidden_wrongimage_missing_incomplete_forged_source_refs(self):
        a,p=freeze(self.data,self.core,self.full)
        for defect in ['hidden','wrongimage','missing','incomplete','original','selfhash','topology']:
            after=core_fixture('I2' if defect=='wrongimage' else 'I','hidden' if defect=='hidden' else 'visible');evidence=after_evidence(p)
            if defect=='missing':after['semantic_assertions']=[x for x in after['semantic_assertions'] if x['assertion_id']!='visible']
            elif defect=='incomplete':after['request_binding']['input_inventory']['complete']=False
            elif defect=='original':evidence[0]['original_assertion_sha256']='a'*64
            elif defect=='topology':after['semantic_assertions']=[x for x in after['semantic_assertions'] if x['assertion_id']!='images_disjoint']
            sign_core(after)
            with self.subTest(defect=defect),self.assertRaises(ValueError):permission.freeze_after_state(p,after,expected_after_sha256='b'*64 if defect=='selfhash' else c.digest(after),evidence=evidence,reviewer='reviewer')
    def test_session_change_invalidates_same_resolution_cache(self):
        a,p=freeze(self.data,self.core,self.full)
        with permission.trusted_permission_session(a,p):
            with n.bound_selected_resolution([self.full],self.core) as context:self.assertTrue(context['permission_envelope_receipt'])
            with n.bound_selected_resolution([self.full],self.core):
                token=permission._ACTIVE.set(None)
                try:self.assertFalse(n.admission(self.full,self.core)['allowed'])
                finally:permission._ACTIVE.reset(token)
    def test_final_auditor_rechecks_and_rejects_composed_receipts(self):
        a,p=freeze(self.data,self.core,self.full)
        pack={'authorial_core':self.core};composed={}
        with permission.trusted_permission_session(a,p),mock.patch.object(audit,'_native_adoption_entries',return_value=[self.full]),mock.patch.object(audit,'_audit_native_adoptions',return_value=[]):
            failures=audit.audit_native_adoptions(pack,composed,self.data)
            self.assertTrue(failures)
        result=permission.freeze_after_state(p,self.core,expected_after_sha256=c.digest(self.core),evidence=after_evidence(p),reviewer='reviewer')
        with permission.trusted_permission_session(a,p,after_state=result),mock.patch.object(audit,'_native_adoption_entries',return_value=[self.full]),mock.patch.object(audit,'_audit_native_adoptions',return_value=[]):
            self.assertEqual(audit.audit_native_adoptions(pack,composed,self.data),[])
            self.assertTrue(audit.audit_native_adoptions(pack,{'native_preservation_receipt':{}},self.data))

if __name__=='__main__':unittest.main()
