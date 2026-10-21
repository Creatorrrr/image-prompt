from pathlib import Path
import copy,re,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from photo_h_f2_query_scope import analyze
from photo_h_f2_event_phase import compile_contracts,order_phase,present_material
T=lambda s:re.findall(r'[^\W_]+',s.casefold(),re.UNICODE)
Q='Photographic role: Owned physical residue of an earlier event, distinct from an ongoing process.'
POST='Post-event residue across a workshop floor'

class MaterialProjectionTests(unittest.TestCase):
 def project(self,texts,query=Q):
  rows=[{'id':str(i),'rrf':1/(i+10),'cosine':.9-i/100,'bm25':20-i} for i in range(len(texts))];old=copy.deepcopy(rows)
  full,phase=order_phase(rows,query,analyze(query,T),compile_contracts(dict(zip(map(str,range(len(texts))),texts)),T,source_units=lambda key:[{'pointer':'/content/en','text':texts[int(key)]}]),T)
  selected,projection=present_material(full,phase);self.assertEqual(rows,old);self.assertEqual({r['id']:r for r in full},{r['id']:r for r in old});return full,selected,projection,phase
 def test_four_positive_sources_do_not_get_four_neutral_fillers(self):
  full,out,p,_=self.project([POST]*4+['A surface texture','A stationary pose','A photographic capture context','A glass plate'])
  self.assertEqual(len(full),8);self.assertEqual(len(out),4);self.assertEqual(p['unfilled'],4);self.assertFalse(p['unknown_phase_padding'])
 def test_no_positive_witness_returns_empty_without_fallback(self):
  full,out,p,_=self.project(['A textured surface','An ongoing process'])
  self.assertEqual(len(full),2);self.assertEqual(out,[]);self.assertEqual(p['reason'],'no_positive_source_contract');self.assertEqual(p['additional_search_calls'],0)
 def test_more_than_eight_positive_sources_remain_capped(self):
  full,out,p,_=self.project([POST]*11);self.assertEqual(len(full),11);self.assertEqual(len(out),8);self.assertEqual(p['available'],11)
 def test_single_positive_source_is_returned_without_padding(self):
  full,out,p,_=self.project(['A stationary pose',POST]+['A capture context']*8);self.assertEqual([r['id'] for r in out],['1']);self.assertEqual(p['unfilled'],7);self.assertEqual(len(full),10)
 def test_ordinary_query_keeps_original_eight(self):
  full,out,p,_=self.project(['A photographic context']*10,query='A portrait with readable surface detail')
  self.assertEqual(out,full[:8]);self.assertEqual(p['mode'],'ordinary_top8')
 def test_specific_scene_cannot_borrow_unrelated_generic_material(self):
  full,out,p,_=self.project([POST]+['A pose']*9,query=Q+' Scene context: A kitchen.')
  self.assertEqual(out,[]);self.assertEqual(p['mode'],'post_event_source_witnesses');self.assertEqual(p['reason'],'no_positive_source_contract')
 def test_negated_or_quoted_source_does_not_supply_return_material(self):
  for text in ['No '+POST,'"'+POST+'"','A surface. '+POST]:
   with self.subTest(text=text):self.assertEqual(self.project([text])[1],[])
 def test_residual_motion_is_still_returned(self):
  _,out,p,_=self.project(['Settling aftereffect phase with a visible residual trace and diminishing motion','A smoke column from a just-extinguished candle'])
  self.assertEqual(len(out),2);self.assertEqual(p['returned'],2)
 def test_disordered_positive_prefix_fails_instead_of_borrowing_unknown(self):
  full,_,_,phase=self.project([POST,'A surface']);full.reverse()
  with self.assertRaises(ValueError):present_material(full,phase)
 def test_foreign_phase_policy_fails_closed(self):
  with self.assertRaises(ValueError):present_material([{'id':'a'}],{'schema':'old-policy'})
 def test_ordinary_short_pool_returns_all_available(self):
  full,out,p,_=self.project(['A surface'],query='A portrait');self.assertEqual(full,out);self.assertEqual(p['returned'],1)
 def test_projection_binds_exact_returned_ids_without_adoption_authority(self):
  _,out,p,_=self.project([POST]*3+['An ongoing process']);self.assertEqual(p['returned_ids'],[r['id'] for r in out]);self.assertFalse(p['native_approval']);self.assertFalse(p['pre_search_filter'])

if __name__=='__main__':unittest.main()
