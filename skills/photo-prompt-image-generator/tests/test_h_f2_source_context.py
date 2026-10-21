from pathlib import Path
import copy,re,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from photo_h_f2_query_scope import analyze
from photo_h_f2_event_phase import primary_units,context_requirements,compile_contracts,order_phase,present_material
T=lambda s:re.findall(r'[^\W_]+',s.casefold(),re.UNICODE)
CANDLE='A thin smoke column rising from a just-snuffed candle'
ORDINARY='A just-extinguished candle with a localized smoke thread'
Q='Photographic role: Owned physical residue of a prior event, distinct from an ongoing process.'

def record(text,lookup='ordinary',tags='ordinary'):
 return {'id':'fixture','meaning':{'primary':{'base':{'/content/en':'label','/content/embedding_text':'full'}},'literals':{'label':CANDLE,'full':text,'lookup':lookup,'tags':tags},'search':{'fields':{'keywords':['lookup']}}},'native':{'tags':'tags'},'provenance':[{'source':tags}]}
def units(text):return primary_units(record(text),'base','a'*64)

class SourceContextTests(unittest.TestCase):
 def test_later_primary_field_carries_supernatural_effect(self):
  text=CANDLE+', visible spell residue and air movement anchor';w=context_requirements(units(text),T)
  self.assertEqual(len(w),1);self.assertEqual(w[0]['quote'],'spell residue');self.assertEqual(w[0]['pointer'],'/content/embedding_text');self.assertEqual(text[w[0]['start']:w[0]['end']],w[0]['quote'])
 def test_later_sentence_is_not_lost(self):self.assertTrue(context_requirements(units(CANDLE+'. Visible supernatural residue remains.'),T))
 def test_residue_caused_by_spell(self):self.assertTrue(context_requirements(units('A smoke trace from a spell remains.'),T))
 def test_ordinary_physical_smoke_has_no_extra_context(self):self.assertFalse(context_requirements(units(ORDINARY),T))
 def test_mortality_symbol_does_not_declare_a_magical_physical_effect(self):
  w=context_requirements(units(ORDINARY+' supports mortality or vanitas meaning without depicting a death event'),T)
  self.assertEqual({r['context'] for r in w},{'mortality_symbolism'})
  self.assertEqual(w[0]['quote'],'supports mortality or vanitas meaning')
 def test_magic_tag_provenance_and_nonprimary_lookup_are_not_facts(self):
  r=record(ORDINARY,lookup='visible spell residue',tags='magic surreal');self.assertFalse(context_requirements(primary_units(r,'base','a'*64),T))
 def test_magical_mood_and_lighting_are_not_supernatural_residue(self):
  for text in ['The candle smoke creates a magical atmosphere.','A magical mood surrounds ordinary smoke.','The ordinary candle has enchanted lighting.']:
   self.assertFalse(context_requirements(units(text),T))
 def test_quoted_label_does_not_declare_an_effect(self):self.assertFalse(context_requirements(units('The candle label reads "spell residue".'),T))
 def test_negative_mentions_do_not_supply_required_effect(self):
  for text in ['No spell residue is visible.','There is no visible spell residue.','The candle has ordinary smoke without magical residue.','Spell residue is absent.','Spell residue must not be introduced.']:
   with self.subTest(text=text):self.assertFalse(context_requirements(units(text),T))
 def test_contrast_counterpart_does_not_supply_effect(self):
  self.assertFalse(context_requirements(units('Ordinary candle smoke, rather than spell residue.'),T))
 def test_negation_does_not_bleed_across_positive_clause(self):
  self.assertTrue(context_requirements(units('Not just smoke, but visible spell residue remains.'),T))
 def test_not_only_still_asserts_magic(self):self.assertTrue(context_requirements(units('Not only spell residue remains.'),T))
 def test_conditional_effect_requires_context_instead_of_becoming_ordinary(self):
  w=context_requirements(units('If declared, the candle shows visible spell residue.'),T);self.assertTrue(w);self.assertEqual(w[0]['modality'],'conditional_or_modal')
 def test_korean_explicit_magic_residue(self):self.assertTrue(context_requirements(units('초에 마법의 잔여물이 남아 있다.'),T))
 def test_korean_negated_residue(self):self.assertFalse(context_requirements(units('마법 잔여물 없이 일반 연기만 남는다.'),T))
 def test_stage_magic_show_is_not_a_supernatural_cause(self):
  self.assertFalse(context_requirements(units('Smoke from a magic show remains.'),T))
 def test_unselected_branch_cannot_supply_context(self):
  r=record(ORDINARY);r['meaning']['primary']['magic_branch']={'/content/other':'other'};r['meaning']['literals']['other']='Visible spell residue';self.assertFalse(context_requirements(primary_units(r,'base','a'*64),T))
 def test_missing_source_provider_is_rejected(self):
  with self.assertRaises(TypeError):compile_contracts({'a':CANDLE},T)
 def test_generic_projection_keeps_ordinary_and_separates_mixed(self):
  docs={'a':CANDLE,'b':ORDINARY};rs={'a':record(CANDLE+', visible spell residue'),'b':record(ORDINARY)}
  contracts=compile_contracts(docs,T,source_units=lambda key:primary_units(rs[key],'base','a'*64));rows=[{'id':'a','rrf':.2},{'id':'b','rrf':.1}];old=copy.deepcopy(rows)
  full,phase=order_phase(rows,Q,analyze(Q,T),contracts,T);selected,p=present_material(full,phase)
  self.assertEqual([r['id'] for r in selected],['b']);self.assertEqual(set(phase['context_qualified']),{'a'});self.assertEqual(rows,old);self.assertEqual({r['id']:r for r in full},{r['id']:r for r in old});self.assertFalse(p['native_approval']);self.assertEqual(p['context_qualified_count'],1);self.assertEqual(p['withheld_context_requirements']['a'][0]['quote'],'spell residue')
 def test_explicit_spell_cause_requires_matching_context_in_same_full_pool(self):
  q='Show physical aftermath of a declared spell with candle smoke';docs={'a':CANDLE,'b':ORDINARY};rs={'a':record(CANDLE+', visible spell residue'),'b':record(ORDINARY)}
  contracts=compile_contracts(docs,T,source_units=lambda key:primary_units(rs[key],'base','a'*64));rows=[{'id':'a'},{'id':'b'}];full,phase=order_phase(rows,q,analyze(q,T),contracts,T);selected,p=present_material(full,phase)
  self.assertEqual({r['id'] for r in full},{'a','b'});self.assertEqual([r['id'] for r in selected],['a']);self.assertEqual(p['mode'],'post_event_source_witnesses')

 def test_symbolic_witness_binds_complete_primary_field(self):
  text=ORDINARY+'. Its smoke supports mortality or vanitas meaning without independently depicting a death event.'
  w=context_requirements(units(text),T);self.assertEqual(len(w),1)
  self.assertEqual(w[0]['pointer'],'/content/embedding_text');self.assertEqual(w[0]['literal_id'],'full');self.assertEqual(w[0]['source_sha256'],'a'*64)
  self.assertEqual(text[w[0]['start']:w[0]['end']],w[0]['quote']);self.assertEqual(w[0]['modality'],'affirmative')
 def test_symbolic_relations_require_interpretive_language(self):
  for text in ['Smoke supports vanitas meaning.','The candle is a symbol of mortality.','Smoke symbolizes death.','A mortality symbol remains.','초 연기는 죽음의 상징이다.']:
   with self.subTest(text=text):self.assertEqual({r['context'] for r in context_requirements(units(text),T)},{'mortality_symbolism'})
 def test_death_vocabulary_is_not_a_symbolic_relation(self):
  for text in ['Smoke remains after a death event.','The candle was extinguished after death.','Mortality statistics accompany a candle photograph.','The source does not independently depict a death event.']:
   with self.subTest(text=text):self.assertFalse(context_requirements(units(text),T))
 def test_symbolic_lookup_alias_tag_provenance_do_not_create_primary_facts(self):
  r=record(ORDINARY,lookup='supports mortality or vanitas meaning',tags='vanitas death symbolism');self.assertFalse(context_requirements(primary_units(r,'base','a'*64),T))
 def test_unselected_symbolic_branch_is_not_a_requirement(self):
  r=record(ORDINARY);r['meaning']['primary']['symbolic']={'/content/symbolic':'symbolic'};r['meaning']['literals']['symbolic']='A symbol of death';self.assertFalse(context_requirements(primary_units(r,'base','a'*64),T))
 def test_symbolic_negative_mentions_do_not_create_a_requirement(self):
  for text in ['It does not support vanitas meaning.','It is not a symbol of mortality.','Smoke without vanitas symbolism remains.','Vanitas symbolism is absent.','Vanitas symbolism must not be introduced.','죽음의 상징 없이 일반 연기만 남는다.']:
   with self.subTest(text=text):self.assertFalse(context_requirements(units(text),T))
 def test_symbolic_quotes_and_contrast_are_not_assertions(self):
  for text in ['The label reads "a symbol of death".','Ordinary smoke, rather than vanitas symbolism.']:
   with self.subTest(text=text):self.assertFalse(context_requirements(units(text),T))
 def test_negated_death_event_does_not_erase_positive_symbolic_relation(self):
  w=context_requirements(units('The candle does not depict a death event but supports vanitas meaning.'),T);self.assertEqual({r['context'] for r in w},{'mortality_symbolism'})
 def test_conditional_symbolic_use_still_requires_authored_context(self):
  w=context_requirements(units('If declared, the candle supports vanitas meaning.'),T);self.assertEqual(w[0]['modality'],'conditional_or_modal')
 def test_physical_and_symbolic_contexts_stay_distinct(self):
  w=context_requirements(units('Visible spell residue remains and supports vanitas meaning.'),T);self.assertEqual({r['context'] for r in w},{'supernatural_physical_effect','mortality_symbolism'})
 def test_generic_projection_separates_both_contexts_without_losing_pool(self):
  docs={'s':ORDINARY,'m':CANDLE,'p':ORDINARY};rs={'s':record(ORDINARY+' supports vanitas meaning'),'m':record(CANDLE+', visible spell residue'),'p':record(ORDINARY)}
  contracts=compile_contracts(docs,T,source_units=lambda key:primary_units(rs[key],'base','a'*64));rows=[{'id':key} for key in docs];full,phase=order_phase(rows,Q,analyze(Q,T),contracts,T);selected,p=present_material(full,phase)
  self.assertEqual([r['id'] for r in selected],['p']);self.assertEqual({r['id'] for r in full},set(docs));self.assertEqual(set(phase['context_qualified']),{'s','m'});self.assertEqual(p['context_qualified_count'],2)
 def test_only_symbolic_post_event_source_does_not_fill_generic_material(self):
  docs={'s':ORDINARY};contracts=compile_contracts(docs,T,source_units=lambda key:units(ORDINARY+' supports vanitas meaning'));rows=[{'id':'s'}];full,phase=order_phase(rows,Q,analyze(Q,T),contracts,T);selected,p=present_material(full,phase)
  self.assertEqual(full,rows);self.assertEqual(selected,[]);self.assertEqual(p['reason'],'no_positive_source_contract')
 def test_explicit_symbolic_query_keeps_ordinary_full_pool_branch(self):
  q='Show an extinguished candle supporting vanitas meaning.';docs={'s':ORDINARY};contracts=compile_contracts(docs,T,source_units=lambda key:units(ORDINARY+' supports vanitas meaning'));rows=[{'id':'s'}];full,phase=order_phase(rows,q,analyze(q,T),contracts,T);selected,p=present_material(full,phase)
  self.assertEqual(full,rows);self.assertEqual(selected,rows);self.assertEqual(p['mode'],'ordinary_top8')

class LuxuryContextTests(unittest.TestCase):
 def test_selected_primary_history_is_field_bound(self):
  text='Spent wax lies across worn velvet so former luxury decline and recent aftermath share the same physical surfaces.'
  w=context_requirements(units(text),T);self.assertEqual(len(w),1);self.assertEqual(w[0]['context'],'former_luxury_decline');self.assertEqual(w[0]['quote'],'former luxury decline');self.assertEqual(w[0]['pointer'],'/content/embedding_text');self.assertEqual(text[w[0]['start']:w[0]['end']],w[0]['quote']);self.assertEqual(w[0]['literal_id'],'full')
 def test_authored_past_opulence_and_decline_relations(self):
  for text in ['After-event residue across faded luxury materials.','Traces show the decline of former opulence.','A once-luxurious room in decline holds spent wax.','과거 호화의 쇠락과 최근 행사 흔적이 함께 보인다.','쇠락한 호화 공간에 행사 후 흔적이 남는다.']:
   with self.subTest(text=text):self.assertEqual({r['context'] for r in context_requirements(units(text),T)},{'former_luxury_decline'})
 def test_wear_and_luxury_alone_do_not_assert_a_former_wealth_history(self):
  for text in ['Spent wax lies across worn velvet and tarnished metal.','Displaced luxury glassware remains after an event.','Dust and wilted flowers remain on marble.','Faded paint covers a wooden chair.','행사 뒤 마모된 벨벳 위에 촛농이 남는다.']:
   with self.subTest(text=text):self.assertFalse(context_requirements(units(text),T))
 def test_history_lookup_tag_provenance_are_not_primary_facts(self):
  r=record('Spent wax remains on worn velvet.',lookup='former luxury decline',tags='faded luxury decay');self.assertFalse(context_requirements(primary_units(r,'base','a'*64),T))
 def test_unselected_history_branch_does_not_supply_context(self):
  r=record('Spent wax remains.');r['meaning']['primary']['history']={'/content/history':'history'};r['meaning']['literals']['history']='Former luxury decline';self.assertFalse(context_requirements(primary_units(r,'base','a'*64),T))
 def test_negated_history_is_not_an_affirmative_requirement(self):
  for text in ['No former luxury decline is shown.','The residue implies no faded luxury.','Ordinary residue without former luxury decline.','Former luxury decline is absent.','Faded luxury must not be introduced.','과거 호화의 쇠락 없이 최근 행사 흔적만 남는다.']:
   with self.subTest(text=text):self.assertFalse(context_requirements(units(text),T))
 def test_quotes_and_comparison_counterpart_are_not_history_facts(self):
  for text in ['The label reads "former luxury decline".','Recent physical aftermath, rather than faded luxury.']:
   with self.subTest(text=text):self.assertFalse(context_requirements(units(text),T))
 def test_history_in_later_primary_sentence_is_not_lost(self):
  self.assertTrue(context_requirements(units('Spent wax remains. The surface conveys former luxury decline.'),T))
 def test_negation_does_not_erase_a_separate_positive_history_clause(self):
  self.assertTrue(context_requirements(units('Not just worn velvet, but former luxury decline is shown.'),T))
 def test_conditional_history_still_needs_authored_context(self):
  w=context_requirements(units('If declared, the surfaces convey former luxury decline.'),T);self.assertEqual(w[0]['modality'],'conditional_or_modal')
 def test_generic_projection_keeps_plain_residue_and_withholds_history(self):
  docs={'h':'After-event residue across faded luxury materials','p':'Settling aftereffect with a visible residual trace'};rs={'h':record('Spent wax combines former luxury decline and recent aftermath.'),'p':record('A residual trace is settling while motion diminishes.')};contracts=compile_contracts(docs,T,source_units=lambda key:primary_units(rs[key],'base','a'*64));rows=[{'id':'h','rrf':.3},{'id':'p','rrf':.1}];old=copy.deepcopy(rows);full,phase=order_phase(rows,Q,analyze(Q,T),contracts,T);selected,p=present_material(full,phase)
  self.assertEqual([r['id'] for r in selected],['p']);self.assertEqual(p['context_qualified_count'],1);self.assertEqual({r['id'] for r in full},{'h','p'});self.assertEqual(rows,old);self.assertEqual(p['withheld_context_requirements']['h'][0]['context'],'former_luxury_decline')
 def test_only_history_source_cannot_pad_generic_material(self):
  docs={'h':'After-event residue across faded luxury materials'};contracts=compile_contracts(docs,T,source_units=lambda key:units('Former luxury decline is shown.'));rows=[{'id':'h'}];full,phase=order_phase(rows,Q,analyze(Q,T),contracts,T);selected,p=present_material(full,phase);self.assertEqual(full,rows);self.assertFalse(selected);self.assertEqual(p['reason'],'no_positive_source_contract')
 def test_explicit_luxury_history_query_keeps_ordinary_full_pool_branch(self):
  q='Show recent physical residue together with former luxury decline.';docs={'h':'After-event residue across faded luxury materials'};contracts=compile_contracts(docs,T,source_units=lambda key:units('Former luxury decline is shown.'));rows=[{'id':'h'}];full,phase=order_phase(rows,q,analyze(q,T),contracts,T);selected,p=present_material(full,phase);self.assertEqual(selected,rows);self.assertEqual(p['mode'],'ordinary_top8')
 def test_context_categories_do_not_replace_each_other(self):
  w=context_requirements(units('Visible spell residue supports vanitas meaning and the room shows former luxury decline.'),T);self.assertEqual({r['context'] for r in w},{'supernatural_physical_effect','mortality_symbolism','former_luxury_decline'})

if __name__=='__main__':unittest.main()
