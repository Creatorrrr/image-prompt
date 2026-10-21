from pathlib import Path
import copy,re,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from photo_h_f2_query_scope import analyze
from photo_h_f2_event_phase import request,compile_contracts,order_phase,present_material,primary_units
T=lambda s:re.findall(r'[^\W_]+',s.casefold(),re.UNICODE)
GENERIC='Post-event residue across its owned surface'
QUIET='Quiet after-event state with chairs, cups, and traces left behind'
RECIPE='Failed recipe aftermath with harmless kitchen mess'
MAGIC='A smoke column from a just-extinguished candle with visible spell residue'
SYMBOL='A just-extinguished candle with a residual smoke trace that supports vanitas meaning'

def rec(text,label=None,lookup=''):
 return {'id':'fixture','meaning':{'primary':{'base':{'/content/en':'en','/content/embedding_text':'full'}},'literals':{'en':label or text,'full':text,'lookup':lookup},'search':{'fields':{'aliases':['lookup']}}}}

class ExpandedAftermathTests(unittest.TestCase):
 def req(self,q):return request(q,analyze(q,T),T)
 def project(self,q,texts):
  rows=[{'id':str(i),'bm25':9-i,'rrf':.5-i/100} for i in range(len(texts))];old=copy.deepcopy(rows)
  contracts=compile_contracts({str(i):x for i,x in enumerate(texts)},T,source_units=lambda key:primary_units(rec(texts[int(key)]),'base','a'*64))
  full,phase=order_phase(rows,q,analyze(q,T),contracts,T);out,p=present_material(full,phase)
  self.assertEqual(rows,old);self.assertEqual({r['id']:r for r in full},{r['id']:r for r in old});return out,p,phase
 def test_trace_synonym_does_not_require_negative_boilerplate(self):
  out,p,_=self.project('Show physical traces after an event has ended.',[GENERIC,QUIET]);self.assertEqual([r['id'] for r in out],['0']);self.assertEqual(p['returned'],1)
 def test_korean_generic_phase_and_particle_variations(self):
  for q in ['완료된 사건 뒤에 남은 물리적 잔여물을 보여주세요.','앞선 사건에 속한 사후 잔여 흔적을 보여줘.','정지 포즈와 구분해 끝난 동작의 물리적 흔적을 보여줘.']:
   with self.subTest(q=q):self.assertEqual(self.req(q)['scene_family'],'generic')
 def test_positive_witnesses_address_original_unicode(self):
  q='앞선 사건 뒤에 남은 물리적 흔적을 보여줘.'
  for w in self.req(q)['positive_witnesses']:self.assertEqual(q[w['start']:w['end']],w['quote'])
 def test_specific_quiet_event_recovers_trace_source_without_generic_padding(self):
  out,p,_=self.project('Show physical traces after a party has ended in a quiet room with chairs and cups left behind.',[GENERIC,QUIET,RECIPE]);self.assertEqual([r['id'] for r in out],['1']);self.assertEqual(p['returned'],1)
 def test_failed_recipe_requires_actual_failure_context(self):
  out,_,_=self.project('Show physical aftermath after a failed recipe attempt has ended, with harmless kitchen mess.',[GENERIC,QUIET,RECIPE]);self.assertEqual([r['id'] for r in out],['2'])
 def test_bare_kitchen_does_not_invent_recipe_failure(self):
  out,_,_=self.project('Show physical traces of a completed event in a kitchen.',[GENERIC,RECIPE]);self.assertFalse(out)
 def test_plain_candle_cannot_borrow_magic_or_mortality_meaning(self):
  out,p,_=self.project('Show physical smoke after a candle has been snuffed, without magic residue or vanitas symbolism.',[GENERIC,MAGIC,SYMBOL]);self.assertFalse(out);self.assertEqual(p['unfilled'],8)
 def test_positive_spell_context_returns_only_spell_source(self):
  out,_,_=self.project('Show physical aftermath of a declared spell with candle smoke.',[GENERIC,MAGIC,SYMBOL]);self.assertEqual([r['id'] for r in out],['1'])
 def test_required_vanitas_returns_only_symbolic_source(self):
  out,_,_=self.project('Show post-event candle smoke as a vanitas symbol.',[GENERIC,MAGIC,SYMBOL]);self.assertEqual([r['id'] for r in out],['2'])
 def test_optional_context_stays_optional(self):
  q='Show physical smoke after a candle has been snuffed; vanitas symbolism may be included optionally.'
  self.assertEqual(self.req(q)['context_permissions'],{'mortality_symbolism':'optional'});out,_,_=self.project(q,[GENERIC,MAGIC,SYMBOL]);self.assertEqual([r['id'] for r in out],['2'])
 def test_korean_negative_context_cannot_supply_permission(self):
  q='초가 꺼진 뒤 남은 물리적 연기 흔적을 보여줘. 마법 잔여물과 바니타스 상징은 제외해줘.'
  self.assertEqual(self.req(q)['context_permissions'],{});self.assertFalse(self.project(q,[MAGIC,SYMBOL])[0])
 def test_quote_is_not_a_symbolic_request(self):
  q='Show physical smoke after a candle has gone out. A separate label reads "vanitas symbol".'
  self.assertEqual(self.req(q)['context_permissions'],{});self.assertFalse(self.project(q,[SYMBOL])[0])
 def test_korean_negated_phase_and_quote_stay_ordinary(self):
  for q in ['사후 흔적이 아니라 진행 중인 동작을 보여줘.','완료된 사건의 물리적 사후 흔적을 보여주지 마.','표지판에 "사건 뒤 물리적 흔적"이라고 적어줘.']:
   with self.subTest(q=q):self.assertIsNone(self.req(q))
 def test_english_negation_and_future_stay_ordinary(self):
  for q in ['Do not show physical residue of a completed event.','Show preparations for a future event and its physical aftermath.','Show an ongoing action, not physical aftermath.']:
   with self.subTest(q=q):self.assertIsNone(self.req(q))
 def test_material_state_or_post_event_time_alone_is_insufficient(self):
  for text in ['A worn surface with dust.','Post-event hour after people have left.']:
   self.assertFalse(self.project('Show physical residue of a completed event.',[text])[0])
 def test_unknown_owner_cannot_acquire_generic_source_compatibility(self):
  out,p,_=self.project('Show muddy pawprints left on a floor after a dog has finished crossing it.',[GENERIC,QUIET]);self.assertFalse(out);self.assertEqual(p['reason'],'no_positive_source_contract')
 def test_lookup_only_after_event_label_is_not_primary_evidence(self):
  r=rec('An empty table.',lookup=GENERIC);c=compile_contracts({'x':GENERIC},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertNotIn('x',c)
 def test_later_selected_primary_field_can_supply_real_phase(self):
  r=rec(QUIET,label='An event room');c=compile_contracts({'x':'An event room\n'+QUIET},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertEqual(c['x']['phase'],'post_event_residue');self.assertEqual(c['x']['primary_phase_evidence'][0]['pointer'],'/content/embedding_text')
 def test_selected_primary_active_and_post_event_conflict_is_not_positive(self):
  r=rec('An ongoing action uses a tool.',label=GENERIC);c=compile_contracts({'x':GENERIC},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertEqual(c['x']['phase'],'mixed_phase')
 def test_unselected_branch_cannot_supply_scene_or_phase(self):
  r=rec('An empty room.');r['meaning']['primary']['other']={'/content/other':'other'};r['meaning']['literals']['other']=QUIET;c=compile_contracts({'x':'An empty room\n'+QUIET},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertNotIn('x',c)
 def test_source_evidence_keeps_ids_hash_pointer_and_exact_text(self):
  c=compile_contracts({'x':QUIET},T,source_units=lambda key:primary_units(rec(QUIET),'base','a'*64))['x'];w=c['context_requirements'][0];self.assertEqual(w['source_sha256'],'a'*64);self.assertEqual(w['candidate_id'],'fixture');self.assertEqual(w['realization_id'],'base');self.assertEqual(QUIET[w['start']:w['end']],w['quote']);self.assertEqual(w['context'],'quiet_event_setting')
 def test_incompatible_context_does_not_remove_full_pool_score_rows(self):
  out,p,phase=self.project('Show physical residue of a completed event.',[GENERIC,MAGIC,SYMBOL,QUIET,RECIPE]);self.assertEqual([r['id'] for r in out],['0']);self.assertEqual(len(phase['source_compatibility']),5);self.assertEqual(p['additional_search_calls'],0);self.assertFalse(p['native_approval'])
 def test_emerging_transformation_is_not_completed_aftermath(self):
  text='Aftermath trace: source-form residue follows the path into an emerging target surface.'
  self.assertFalse(self.project('Show physical residue of a completed event.',[text])[0])
 def test_negative_owner_mention_does_not_supply_source_family(self):
  r=rec(GENERIC+'. This is not a candle.');c=compile_contracts({'x':GENERIC},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertEqual(c['x']['source_profile']['scene_family'],'generic')
 def test_accepted_context_is_not_reported_as_withheld(self):
  out,p,_=self.project('Show post-event candle smoke as a vanitas symbol.',[SYMBOL,MAGIC]);self.assertEqual([r['id'] for r in out],['0']);self.assertIn('0',p['accepted_context_requirements']);self.assertNotIn('0',p['withheld_context_requirements']);self.assertIn('1',p['withheld_context_requirements'])
 def test_query_context_and_scene_evidence_use_original_offsets(self):
  q='초가 꺼진 뒤 남은 물리적 연기 흔적을 바니타스 상징으로 보여줘.';r=self.req(q)
  for w in r['context_witnesses']+r['scene_witnesses']:self.assertEqual(q[w['start']:w['end']],w['quote'])
 def test_absent_quiet_setting_does_not_become_a_requirement(self):
  r=rec(GENERIC+'. Quiet after-event state is absent.');c=compile_contracts({'x':GENERIC},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertFalse(c['x']['context_requirements'])
 def test_missing_recipe_failure_does_not_become_a_requirement(self):
  r=rec(GENERIC+'. Failed recipe is missing.');c=compile_contracts({'x':GENERIC},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertFalse(c['x']['context_requirements'])
 def test_korean_absent_quiet_setting_is_not_a_requirement(self):
  r=rec(GENERIC+'. 행사 직후 조용해진 공간은 없다.');c=compile_contracts({'x':GENERIC},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertFalse(c['x']['context_requirements'])
 def test_absent_candle_is_not_an_owned_source_scene(self):
  r=rec(GENERIC+'. A candle is absent.');c=compile_contracts({'x':GENERIC},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertEqual(c['x']['source_profile']['scene_family'],'generic')
 def test_raw_not_polarity_is_not_lost_after_masking(self):
  r=rec(GENERIC+'. A candle is not present.');c=compile_contracts({'x':GENERIC},T,source_units=lambda key:primary_units(r,'base','a'*64));self.assertEqual(c['x']['source_profile']['scene_family'],'generic')
 def test_negated_query_context_is_not_allowed_after_masking(self):
  q='Show physical smoke after a candle has gone out. Vanitas symbolism is not wanted.';self.assertNotIn('mortality_symbolism',self.req(q)['context_permissions'])
 def test_quiet_noun_phrase_absence_is_not_a_context_permission(self):
  q='Show physical traces after a party has ended. A quiet room is absent.';self.assertNotIn('quiet_event_setting',self.req(q)['context_permissions'])
 def test_korean_quiet_noun_phrase_absence_is_not_permission(self):
  q='파티가 끝난 뒤 물리적 사후 흔적을 보여줘. 조용한 공간은 없어.';self.assertNotIn('quiet_event_setting',self.req(q)['context_permissions'])

if __name__=='__main__':unittest.main()
