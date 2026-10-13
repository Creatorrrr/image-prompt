import copy,unittest
from tests import test_photo_global_retrieval as fixtures
import photo_candidate_corpus as c,photo_global_retrieval as search,photo_native_pack as n,audit_global_retrieval as a

class IndependentReplayTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):fixtures.GlobalDiscoveryTests.setUpClass()
 def setUp(self):
  helper=fixtures.GlobalDiscoveryTests();self.addCleanup(helper.doCleanups);self.data=helper.lazy();self.ctx=helper.context();self.core=helper.core;self.controls=helper.controls
  roles,binding,_=__import__('photo_slot_retrieval').retrieve(self.data,self.core,self.controls,self.ctx)
  work=n.WorkingPack({'contract_version':n.CONTRACT,'global_retrieval':binding,'authorial_core':self.core,'creative_controls':self.controls},roles)
  self.pack=n.finalize(work,self.data,binding['selected_candidate_ids'],self.ctx)
 def failures(self):return a.audit(self.pack,self.data,self.ctx)
 def rehash(self):
  r=self.pack['global_retrieval'];r['canonical_sha256']=c.digest({k:v for k,v in r.items() if k!='canonical_sha256'})
 def test_independent_replay_matches(self):self.assertEqual(self.failures(),[])
 def test_authored_owner_meaning_tamper(self):
  row=next(iter(self.pack['candidate_pool'].values()));row['authored_record']['content']['en']='different owner and right edge';self.assertTrue(self.failures())
 def test_candidate_omission_even_with_new_checksum(self):
  cid=next(iter(self.pack['candidate_pool']));self.pack['candidate_pool'].pop(cid);self.pack['global_retrieval']['selected_candidate_ids'].remove(cid);self.rehash();self.assertTrue(self.failures())
 def test_role_guard_tamper(self):
  b=next(iter(self.pack['candidate_bindings'].values()));b['conditions']['subject_applicability']={};self.assertTrue(self.failures())
 def test_foreign_tag_tamper(self):
  self.pack['role_views']['color']=self.pack['role_views'].pop('lighting');self.assertTrue(self.failures())
 def test_false_hybrid_flag_rejected(self):
  self.pack['global_retrieval']['lanes']['embedding']['state']='not_requested';self.rehash();self.assertTrue(self.failures())
 def test_rank_substitution_rejected(self):
  self.pack['global_retrieval']['slot_searches']['lighting']['lanes']['embedding']['ranks'].reverse();self.rehash();self.assertTrue(self.failures())
 def test_query_from_another_core_rejected(self):
  self.ctx['slots']['lighting']['binding']['core_sha256']='f'*64;self.ctx['canonical_sha256']=c.digest({k:v for k,v in self.ctx.items() if k!='canonical_sha256'});self.assertTrue(self.failures())
 def test_v6_is_rejected_without_reader(self):
  self.pack['contract_version']='photo-candidate-pack/v6';self.assertTrue(self.failures());self.assertRaises(ValueError,n.read_view,self.pack)
 def test_native_dereference_keeps_wire_hash(self):
  self.assertEqual(c.digest(n.read_view(self.pack)),c.digest(self.pack))
if __name__=='__main__':unittest.main()
