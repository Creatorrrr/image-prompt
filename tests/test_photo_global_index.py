import copy,sys,unittest,tempfile
from pathlib import Path
SCRIPTS=Path(__file__).resolve().parents[1]/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(SCRIPTS))
import photo_candidate_corpus as c,photo_global_index as g
from photo_embedding_provider import validate_vector
from tests.photo_native_schema import slot

class NativeIndexTests(unittest.TestCase):
 def setUp(self):
  self.cid='cand_'+'a'*32
  self.c={'schema':c.SCHEMA,'candidates':{self.cid:{'id':self.cid,'record_kind':'visual_option','content':{'en':'left edge light','aliases':['왼쪽 윤곽 빛']},'conditions':{},'effects':{'dimensions':['lighting'],'properties':[]},'provenance':[{'source':'authored','sha256':'a'*64}]}},'slot_catalog':{},'slot_bindings':{},'policies':{}}
  recipe,body=g.text(self.c['candidates'][self.cid]);import hashlib
  self.i={'schema':g.SCHEMA,'space':g.SPACE,'query_recipe':g.QUERY_RECIPE,'corpus_sha256':c.digest(self.c),'entries':{self.cid:{'id':self.cid,'recipe':recipe,'text':body,'text_sha256':hashlib.sha256(body.encode()).hexdigest(),'vector':[1.0]+[0.0]*767}}}
 def test_untagged_global_document(self):
  self.assertEqual(set(g.documents(self.c)),{self.cid});g.validate(self.i,self.c)
 def test_role_addition_does_not_change_document(self):
  before=g.documents(self.c);self.c['slot_catalog']['lighting']=slot('lighting',['lighting'])
  for tag in ('lighting','light_type'):
   self.c['slot_catalog'][tag]=slot(tag,['lighting'])
   bid='bind_'+('a' if tag=='lighting' else 'b')*32;self.c['slot_bindings'][bid]={'id':bid,'candidate_id':self.cid,'slot_id':tag,'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{}},'weight':1}
  c.validate(self.c);self.assertEqual(before,g.documents(self.c));self.assertEqual(g.lexical(self.c)['document_count'],1)
 def test_diagnostics_have_no_positive_document(self):
  self.c['candidates'][self.cid]['record_kind']='diagnostic';self.assertEqual(g.documents(self.c),{})
 def test_rejects_wrong_recipe(self):
  self.i['entries'][self.cid]['recipe']='old-slot-text';self.assertRaises(ValueError,g.validate,self.i,self.c)
 def test_rejects_wrong_identity(self):
  self.i['entries'][self.cid]['id']='slot:lighting:x';self.assertRaises(ValueError,g.validate,self.i,self.c)
 def test_rejects_text_source_drift(self):
  self.c['candidates'][self.cid]['content']['en']='right edge light';self.assertRaises(ValueError,g.validate,self.i,self.c)
 def test_rejects_invalid_vector(self):
  for v in ([0.0]*768,[1.0]*767,[float('nan')]*768,[float('inf')]*768):self.assertRaises(ValueError,validate_vector,v)
 def test_native_extents_roundtrip_and_hash(self):
  import photo_search_layout as layout
  from photo_search_reader import SearchReader
  with tempfile.TemporaryDirectory() as d:
   layout.build(Path(d),self.c,self.i,activate=True);reader=SearchReader(d);self.addCleanup(reader.close)
   self.assertEqual(reader.block('vector',0).tolist(),self.i['entries'][self.cid]['vector'])
   shard=Path(d)/reader.meta['vector_shards'][0]['path'];shard.write_bytes(b'tampered')
   self.assertRaises(ValueError,reader.block,'vector',0)
 def test_lexical_exact_korean(self):
  from bm25f_retrieval import rank_bm25f
  self.assertEqual(rank_bm25f(g.lexical(self.c),{'frozen_core':'왼쪽 윤곽 빛'})[0]['document_id'],self.cid)
 def test_one_cosine_vote_for_multi_role_candidate(self):
  rows=g.cosine_rank(self.i,[1.0]+[0.0]*767)
  self.assertEqual(rows,[{'document_id':self.cid,'score':1.0}])

if __name__=='__main__':unittest.main()
