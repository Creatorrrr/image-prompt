import copy,json,sys,tempfile,unittest,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g
import photo_candidate_corpus as c,photo_global_index as idx,photo_global_retrieval as search,photo_shared_views as views,photo_slot_queries as query,photo_search_layout as layout,photo_slot_retrieval as slot_search
from photo_search_reader import SearchReader,LazyRuntimeData
from tests.photo_native_schema import slot

class GlobalDiscoveryTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  path=ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en'
  cls.controls=json.loads((path/'creative-controls.json').read_text());cls.core=g.load_authorial_core_arg(path/'authorial-core.json',request_envelope=g.load_request_envelope_arg(path/'request-envelope.json'),creative_control_snapshot=cls.controls)
 def data(self):
  pool={};bindings={};catalog={tag:slot(tag,['lighting']) for tag in ['lighting','light_type','color']}
  for letter,label in [('a','light from camera left on a blue ceramic cup'),('b','left edge illumination of a blue ceramic cup'),('c','right light on a human portrait')]:
   cid='cand_'+letter*32;pool[cid]={'id':cid,'record_kind':'visual_option','content':{'en':label},'conditions':{'for_any':['human']} if letter=='c' else {},'effects':{'dimensions':['lighting'],'properties':[]},'provenance':[{'source':'authored-test','sha256':'a'*64}]}
  for letter,tag in [('d','lighting'),('e','light_type')]:
   bid='bind_'+letter*32;bindings[bid]={'id':bid,'candidate_id':'cand_'+'a'*32,'slot_id':tag,'role':'optional','semantic_role':'direct','conditions':{'subject_applicability':{'subject_categories':['object']}},'weight':1}
  policies={'visual_meaning_contract':{'schema_version':'photo-native-visual-meaning-contract/v1'},'visual_profile_refs':[],'bundle_refs':[],'relationship_graph':{'runtime_node_refs':[],'concept_profile_refs':[]},'candidate_semantic_policy':{},'_quality_layers':{}}
  source={'schema':c.SCHEMA,'candidates':pool,'slot_catalog':catalog,'slot_bindings':bindings,'policies':policies};entries={}
  for cid,row in pool.items():
   recipe,text=idx.text(row);entries[cid]={'id':cid,'recipe':recipe,'text':text,'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'vector':[1.0]+[0.0]*767}
  vectors={'schema':idx.SCHEMA,'space':idx.SPACE,'query_recipe':idx.QUERY_RECIPE,'corpus_sha256':c.digest(source),'entries':entries};return views.assemble(source,vectors)
 def lazy(self,data=None):
  data=data or self.data();temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
  data['_global_index']['corpus_sha256']=c.digest(views.source(data))
  layout.build(Path(temp.name),views.source(data),data['_global_index'],activate=True)
  return LazyRuntimeData(SearchReader(temp.name)).for_core(self.core)
 def context(self):
  from tests.test_photo_slot_queries import synthetic_set
  return synthetic_set(self.core,self.controls,self.data()['slot_catalog'],['lighting','light_type','color'])
 def test_many_roles_and_untagged_found_from_whole_pool(self):
  data=self.data();roles,binding,_=slot_search.retrieve(self.lazy(data),self.core,self.controls,self.context())
  self.assertEqual(set(binding['selected_candidate_ids']),{'cand_'+'a'*32,'cand_'+'b'*32});self.assertEqual(set(roles),{'lighting','light_type','color'});self.assertFalse(binding['tag_admission_filter'])
  self.assertEqual(binding['slot_searches']['lighting']['lanes']['embedding']['positive_hits'],2)
 def test_retagging_does_not_change_discovery_or_guard(self):
  data=self.data();before=slot_search.retrieve(self.lazy(data),self.core,self.controls,self.context())[1]
  data['slot_bindings']['bind_'+'d'*32]['slot_id']='color'
  after=slot_search.retrieve(self.lazy(data),self.core,self.controls,self.context())[1]
  self.assertEqual(before['selected_candidate_ids'],after['selected_candidate_ids']);self.assertEqual(before['lanes'],after['lanes'])
 def test_role_does_not_add_votes(self):
  data=self.data();before=slot_search.retrieve(self.lazy(data),self.core,self.controls,self.context())[1]
  data['slot_bindings'].pop('bind_'+'e'*32)
  after=slot_search.retrieve(self.lazy(data),self.core,self.controls,self.context())[1]
  self.assertEqual(before['lanes'],after['lanes'])
 def test_intrinsic_guard_cannot_be_bypassed_by_good_vector_or_neutral_binding(self):
  data=self.data()
  data['candidates']['cand_'+'a'*32]['conditions']['subject_applicability']={'subject_categories':['human']}
  for b in data['slot_bindings'].values():b['conditions']['subject_applicability']={}
  rows=slot_search.retrieve(self.lazy(data),self.core,self.controls,self.context())[1]['selected_candidate_ids'];self.assertNotIn('cand_'+'a'*32,rows)
 def test_keyword_only_is_explicit_nonhybrid(self):
  roles,binding,_=slot_search.retrieve(self.lazy(),self.core,self.controls,mode='keyword_only');self.assertEqual(binding['lanes']['embedding']['state'],'not_requested');self.assertIsNone(binding['query_context_sha256'])
 def test_missing_or_foreign_vector_fails_hybrid(self):
  self.assertRaises((ValueError,TypeError,AttributeError),slot_search.retrieve,self.lazy(),self.core,self.controls,None)
  context=self.context();context['slots']['lighting']['binding']['core_sha256']='d'*64;context['canonical_sha256']=c.digest({k:v for k,v in context.items() if k!='canonical_sha256'})
  self.assertRaises(ValueError,slot_search.retrieve,self.lazy(),self.core,self.controls,context)

if __name__=='__main__':unittest.main()
