"""Maintenance reuse is exact and never imports the removed index tree."""
import copy,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
import photo_candidate_corpus as c,photo_search_layout as layout,photo_shared_views as views
import build_shared_candidate_index as builder

class NativeSearchMaintenanceTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.assets=Path(self.temp.name)/'assets';self.assets.mkdir();fixture=GlobalDiscoveryTests().data();self.source=views.source(fixture)
  self.write_source();layout.build(self.assets,self.source,fixture['_global_index'],activate=True)
 def write_source(self):
  modules=[]
  for field,schema in c.MODULE_SCHEMAS.items():
   name='photo_candidate_'+field+'.json';modules.append({'file':name,'kind':field});(self.assets/name).write_bytes(c.canonical_bytes({'schema':schema,field:self.source[field]}))
  (self.assets/c.MANIFEST_NAME).write_bytes(c.canonical_bytes({'schema':c.MANIFEST_SCHEMA,'modules':modules}))
 def test_tag_edit_reuses_all_exact_vectors_without_provider_or_legacy_file(self):
  self.source['slot_bindings']['bind_'+'d'*32]['slot_id']='color';self.write_source()
  with patch.object(builder,'embed',side_effect=AssertionError('unnecessary document embedding')):
   report=builder.build(self.assets,Path(self.temp.name)/'cache')
  self.assertEqual(report['vector_reuse'],3);self.assertEqual(report['provider_calls'],0)
  self.assertFalse((self.assets/'photo_candidate_index.json').exists());self.assertFalse((self.assets/'photo_candidate_search.staging.json').exists())
  layout.verify(self.assets,c.load(self.assets),c.decode((self.assets/layout.MANIFEST).read_bytes()))
 def test_changed_text_embeds_only_that_document_and_preserves_unchanged_vectors(self):
  cid='cand_'+'a'*32;self.source['candidates'][cid]['content']['en']='right edge window lighting of a blue ceramic cup';self.write_source()
  reply={'vector':[1.]+[0.]*767,'execution':{'provider_executed':True,'http_status':200,'response_sha256':'c'*64},'cache_hit':False}
  with patch.object(builder,'embed',return_value=reply) as provider:report=builder.build(self.assets,Path(self.temp.name)/'cache')
  self.assertEqual(provider.call_count,1);self.assertEqual(provider.call_args.args[1]['candidate_id'],cid);self.assertEqual(report['vector_reuse'],2)
 def test_source_race_keeps_the_active_manifest(self):
  before=(self.assets/layout.MANIFEST).read_bytes();original=builder.c.load;calls=0
  def raced(assets):
   nonlocal calls
   calls+=1;value=original(assets)
   if calls>1:value['candidates']['cand_'+'a'*32]['content']['en']='a later edited owner'
   return value
  with patch.object(builder.c,'load',side_effect=raced),patch.object(builder,'embed',side_effect=AssertionError('unnecessary embedding')):
   self.assertRaises(ValueError,builder.build,self.assets,Path(self.temp.name)/'cache')
  self.assertEqual((self.assets/layout.MANIFEST).read_bytes(),before)
