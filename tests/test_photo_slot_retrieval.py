import tempfile
import unittest
from pathlib import Path
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
from tests.test_photo_slot_queries import synthetic_set
import photo_search_layout as layout
import photo_shared_views as views
import photo_slot_retrieval as slots
from photo_search_reader import SearchReader,LazyRuntimeData


class SlotExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GlobalDiscoveryTests.setUpClass();cls.core=GlobalDiscoveryTests.core;cls.controls=GlobalDiscoveryTests.controls

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        source=GlobalDiscoveryTests().data();layout.build(Path(self.temp.name),views.source(source),source['_global_index'],activate=True)
        self.data=LazyRuntimeData(SearchReader(self.temp.name)).for_core(self.core)
        self.requested=['lighting','light_type','color'];self.context=synthetic_set(self.core,self.controls,self.data['slot_catalog'],self.requested)

    def test_all_slots_search_whole_pool_before_unique_allocation(self):
        cards,record,_=slots.retrieve(self.data,self.core,self.controls,self.context,requested_slots=self.requested)
        self.assertEqual(set(cards),set(self.requested));self.assertEqual(record['eligible_candidates'],2)
        for row in record['slot_searches'].values():
            self.assertEqual(row['eligible_candidates'],2);self.assertFalse(row['tag_admission_filter'])
            self.assertEqual(row['lanes']['embedding']['positive_hits'],2)
        self.assertTrue(any(p['source_binding_id'] is None for p in record['role_proposals'].values()))
        self.assertTrue(any(p['target_slot_id']=='color' for p in record['role_proposals'].values()))
        self.assertEqual(len(record['selected_candidate_ids']),2)

    def test_slot_order_is_irrelevant_and_budget_does_not_skip_search(self):
        a=slots.retrieve(self.data,self.core,self.controls,self.context,requested_slots=self.requested,unique_limit=1)
        b=slots.retrieve(self.data,self.core,self.controls,self.context,requested_slots=list(reversed(self.requested)),unique_limit=1)
        self.assertEqual(a,b);self.assertEqual(len(a[1]['selected_candidate_ids']),1)
        self.assertEqual(len(a[1]['slot_searches']),3)
        self.assertTrue(any(r['status']=='budget_partial' for r in a[0].values()))

    def test_missing_lane_context_fails_and_keyword_is_explicit(self):
        self.assertRaises(ValueError,slots.retrieve,self.data,self.core,self.controls,None,requested_slots=self.requested)
        _,record,_=slots.retrieve(self.data,self.core,self.controls,mode='keyword_only',requested_slots=self.requested)
        for row in record['slot_searches'].values():self.assertEqual(row['lanes']['embedding']['state'],'not_requested')

    def test_explicit_unknown_slot_is_rejected(self):
        self.assertRaises(ValueError,slots.active_slots,self.data,self.core,self.controls,['safety_profile'])
