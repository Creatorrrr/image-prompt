import copy
import hashlib
import unittest
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
import photo_candidate_corpus as c
import photo_slot_queries as q
import photo_role_proposals as roles


def synthetic_set(core, controls, catalog, slots, language='en'):
    rows = {}
    for slot in slots:
        text, _, binding = q.inputs(core, controls, catalog, slot, language)
        row = {'schema': 'photo-slot-query-vector/v1', 'text': text, 'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
               'binding': binding, 'space': q.SPACE, 'vector': [1.0] + [0.0] * 767,
               'execution': {'provider_executed': True, 'http_status': 200, 'response_sha256': 'a'*64}, 'cache_hit': False}
        row['vector_sha256'] = c.digest(row['vector']); row['canonical_sha256'] = c.digest(row); rows[slot] = row
    value = {'schema': q.SCHEMA, 'slots': rows}; value['canonical_sha256'] = c.digest(value)
    return value


class SlotQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GlobalDiscoveryTests.setUpClass(); cls.core=GlobalDiscoveryTests.core; cls.controls=GlobalDiscoveryTests.controls
        cls.catalog=GlobalDiscoveryTests().data()['slot_catalog']

    def test_slots_have_distinct_bound_texts_and_same_global_context(self):
        value=synthetic_set(self.core,self.controls,self.catalog,['lighting','color'])
        fields=q.validate_set(value,self.core,self.controls,self.catalog,['lighting','color'])
        self.assertEqual(fields['lighting']['global_context'],fields['color']['global_context'])
        self.assertNotEqual(fields['lighting']['slot_focus'],fields['color']['slot_focus'])

    def test_cross_slot_even_rehashed_context_is_rejected(self):
        value=synthetic_set(self.core,self.controls,self.catalog,['lighting','color'])
        value['slots']['lighting']=value['slots']['color'];value['canonical_sha256']=c.digest({k:v for k,v in value.items() if k!='canonical_sha256'})
        self.assertRaises(ValueError,q.validate_set,value,self.core,self.controls,self.catalog,['lighting','color'])

    def test_missing_slot_and_old_query_are_rejected(self):
        value=synthetic_set(self.core,self.controls,self.catalog,['lighting'])
        self.assertRaises(ValueError,q.validate_set,value,self.core,self.controls,self.catalog,['lighting','color'])
        self.assertRaises(ValueError,q.validate_set,{'schema':'photo-frozen-query-vector/v1'},self.core,self.controls,self.catalog,['lighting'])

    def test_korean_role_is_distinct_and_unknown_slot_fails(self):
        en=q.inputs(self.core,self.controls,self.catalog,'lighting')[0]
        ko=q.inputs(self.core,self.controls,self.catalog,'lighting','ko')[0]
        self.assertNotEqual(en,ko);self.assertIn('조명',ko)
        self.assertRaises(ValueError,q.inputs,self.core,self.controls,self.catalog,'safety_profile')

    def test_untagged_and_other_tag_can_propose_without_mutating_source(self):
        data=GlobalDiscoveryTests().data(); before=c.digest(data)
        row=roles.propose(data,'color','cand_'+'b'*32,[])
        self.assertIsNone(row['source_binding_id']);self.assertEqual(row['scope'],'request')
        other=roles.propose(data,'color','cand_'+'a'*32,list(data['slot_bindings']))
        self.assertEqual(other['target_slot_id'],'color');self.assertFalse(other['persistent_tag_write'])
        self.assertEqual(c.digest(data),before)
        roles.validate(data,other,list(data['slot_bindings']))
        edited=copy.deepcopy(other);edited['conditions']={}
        self.assertRaises(ValueError,roles.validate,data,edited,list(data['slot_bindings']))
