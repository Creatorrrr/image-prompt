"""A revised request rebinds provenance without changing preserved scope facts."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from prepare_retry_context import _preserved_assertion_matches
from photo_precore_bridge import load
witnesses = load('photo_semantic_witnesses')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


class ScopeRebindingTests(unittest.TestCase):
    def setUp(self):
        self.fact = {'assertion_id':'face', 'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'fact','source_input_ids':['portrait']}}
        def binding(request, envelope):
            return {'request_sha256':request, 'request_envelope_sha256':envelope,
                    'input_inventory':{'schema':'photo-request-input-inventory/v1','complete':True,
                    'items':[{'id':'request','kind':'request_text','sha256':request},
                             {'id':'portrait','kind':'reference_image','sha256':'a'*64}]}}
        self.parent = {'request_binding':binding('b'*64,'c'*64),'semantic_assertions':[self.fact]}
        self.child = {'request_binding':binding('d'*64,'e'*64),'semantic_assertions':[copy.deepcopy(self.fact)]}
        self.inventory = {'schema':'photo-frozen-scope-inventory/v1','complete':True,
            'input_binding':witnesses.input_binding(self.parent['request_binding']),
            'reviewed_input_ids':['request','portrait'],'state':'known_present',
            'items':[{'assertion_id':'face','dimension':'appearance','target':'person','property':'appearance.face',
                      'value':{'type':'appearance.face/v1','value':'reference face'}}]}
        self.expected = {'dimension':'subject','polarity':'required','affected_dimensions':['subject'],
            'axes':{'native_schema':'photo-frozen-semantics/v1','kind':'scope_inventory','owner':'person',
                    'scope_kind':'reference_appearance','inventory':canonical(self.inventory)},
            'evidence':{'baseline_phrase':'the reference-guided person'}}
        self.actual = copy.deepcopy(self.expected)
        rebound=copy.deepcopy(self.inventory);rebound['input_binding']=witnesses.input_binding(self.child['request_binding'])
        self.actual['axes']['inventory']=canonical(rebound)

    def matches(self):
        return _preserved_assertion_matches(self.expected,self.actual,self.parent,self.child)

    def change_inventory(self,key,value):
        inv=json.loads(self.actual['axes']['inventory']);inv[key]=value;self.actual['axes']['inventory']=canonical(inv)

    def test_current_binding_preserves_identical_scope(self): self.assertTrue(self.matches())
    def test_stale_parent_binding_is_rejected(self):
        self.actual=copy.deepcopy(self.expected);self.assertFalse(self.matches())
    def test_wrong_current_envelope_is_rejected(self):
        bound=witnesses.input_binding(self.child['request_binding']);bound['request_envelope_sha256']='f'*64
        self.change_inventory('input_binding',bound);self.assertFalse(self.matches())
    def test_missing_reviewed_current_input_is_rejected(self):
        self.change_inventory('reviewed_input_ids',['portrait']);self.assertFalse(self.matches())
    def test_added_scope_fact_is_rejected(self):
        self.change_inventory('items',self.inventory['items']*2);self.assertFalse(self.matches())
    def test_removed_scope_fact_is_rejected(self):
        self.change_inventory('items',[]);self.assertFalse(self.matches())
    def test_changed_scope_state_is_rejected(self):
        self.change_inventory('state','known_absent');self.assertFalse(self.matches())
    def test_changed_completeness_is_rejected(self):
        self.change_inventory('complete',False);self.assertFalse(self.matches())
    def test_changed_owner_is_rejected(self):
        self.actual['axes']['owner']='other';self.assertFalse(self.matches())
    def test_changed_scope_kind_is_rejected(self):
        self.actual['axes']['scope_kind']='requester_identity';self.assertFalse(self.matches())
    def test_changed_evidence_is_rejected(self):
        self.actual['evidence']['baseline_phrase']='different person';self.assertFalse(self.matches())
    def test_changed_reference_bytes_are_rejected(self):
        self.child['request_binding']['input_inventory']['items'][1]['sha256']='f'*64
        bound=witnesses.input_binding(self.child['request_binding']);self.change_inventory('input_binding',bound)
        self.assertFalse(self.matches())
    def test_added_identity_reference_is_rejected(self):
        self.child['request_binding']['input_inventory']['items'].append({'id':'new_identity','kind':'identity_reference','sha256':'f'*64})
        self.change_inventory('input_binding',witnesses.input_binding(self.child['request_binding']))
        self.change_inventory('reviewed_input_ids',['request','portrait','new_identity']);self.assertFalse(self.matches())
    def test_ordinary_required_assertions_stay_exact(self):
        old={'dimension':'action','evidence':{'contact':'pen touches register'}}
        self.assertTrue(_preserved_assertion_matches(old,copy.deepcopy(old),self.parent,self.child))
        self.assertFalse(_preserved_assertion_matches(old,{'dimension':'action','evidence':{'contact':'pen touches loose sheet'}},self.parent,self.child))
    def test_absent_identity_scope_keeps_empty_meaning(self):
        self.expected['axes']['scope_kind']='requester_identity';self.actual['axes']['scope_kind']='requester_identity'
        for row in (self.expected,self.actual):
            inv=json.loads(row['axes']['inventory']);inv['state']='known_absent';inv['items']=[];row['axes']['inventory']=canonical(inv)
        self.assertTrue(self.matches())
    def test_malformed_inventory_is_rejected(self):
        self.actual['axes']['inventory']='invalid';self.assertFalse(self.matches())


if __name__=='__main__': unittest.main()
