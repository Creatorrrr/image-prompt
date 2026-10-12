import copy
import unittest
from tools.photo_data_maintenance.corpus import make_inventory
from tools.photo_data_maintenance.links import build_links, query
from tools.photo_data_maintenance.common import canonical, digest

class NativeMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.a='cand_'+'a'*32;self.b='cand_'+'b'*32;self.p='cand_'+'c'*32
        def record(kind, content):
            return {'id':self.a,'record_kind':kind,'content':content,'effects':{'dimensions':[], 'properties':[]},'provenance':[]}
        candidates={self.a:record('visual_option',{'en':'window on camera left'}),
                    self.p:record('visual_profile',{'semantics':{'definition':'visible separate eye and hair owners'}}),
                    self.b:record('visual_bundle',{'member_candidates':[{'candidate_id':self.a,'binding_id':None}], 'hard_profile_ids':[self.p]})}
        for cid,r in candidates.items():r['id']=cid
        self.source={'candidates':candidates,'slot_bindings':{}}
        self.raw={'photo_candidate_candidates_000.json':canonical({'schema':'test','candidates':candidates})}
    def test_global_identity_and_reverse_links_preserve_one_owner(self):
        inv=make_inventory(self.source,self.raw);links=build_links(inv)
        self.assertEqual(len(inv['nodes']),3)
        self.assertTrue(all(r['source_refs'] and r['slot'] is None for r in inv['nodes']))
        path=[self.a,self.b,self.p]
        self.assertEqual(query(inv,links,self.a)['paths'][0]['nodes'],path)
        self.assertEqual(query(inv,links,self.p)['paths'][0]['nodes'],path)
    def test_binding_change_invalidates_entity_without_cloning_candidate(self):
        before=make_inventory(self.source,self.raw)
        self.source['slot_bindings']['bind_'+'d'*32]={'id':'bind_'+'d'*32,'candidate_id':self.a,'slot_id':'lighting','role':'optional','conditions':{}}
        after=make_inventory(self.source,self.raw)
        self.assertEqual(len(before['nodes']),len(after['nodes']))
        hashes=lambda inv:{r['id']:r['entity_sha256'] for r in inv['nodes']}
        self.assertNotEqual(hashes(before)[self.a],hashes(after)[self.a])
        self.assertEqual(hashes(before)[self.p],hashes(after)[self.p])
    def test_unknown_native_reference_cannot_publish_links(self):
        self.source['candidates'][self.b]['content']['hard_profile_ids']=['cand_'+'f'*32]
        self.assertRaises(ValueError,build_links,make_inventory(self.source,self.raw))
if __name__=='__main__':unittest.main()
