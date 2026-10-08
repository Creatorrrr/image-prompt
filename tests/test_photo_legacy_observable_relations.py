"""Legacy ideas require complete owner-bound evidence; no rendered-image claim."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as g
from photo_visual_retrieval import positive_visual_profile_text
from visual_profile_contracts import compile_visual_profile
from photo_contracts import property_effects_allowed

class LegacyObservableRelationsTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.extension=json.loads((SKILL/'assets/photo_prompt_legacy_observable_relations_extension.json').read_text())
  cls.raw_profiles=json.loads((SKILL/'assets/photo_prompt_visual_obligations_legacy_observable_relations.json').read_text())['profiles']
  registry=g.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
  cls.profiles={p['id']:p for p in registry['profiles'] if p['id'].startswith('lor_')}
  cls.scoped={**registry,'profiles':list(cls.profiles.values())};cls.index=g.build_visual_profile_index_payload(cls.scoped)

 def hard(self,text,polarity='required'):
  rows=[{'source':'concept_lock','text':text,'polarity':polarity,'mandatory':True}]
  result=g.resolve_visual_profile_hits(self.scoped,rows,visual_profile_index=self.index,adult_context=False)
  return {h['profile_id'] for h in result['hits'] if h.get('hard_eligible')}

 def test_precise_labels_negation_and_exclusion_preserve_distinct_authority(self):
  for pid,p in self.profiles.items():
   for label in p['activation']['exact_terms']:
    with self.subTest(profile=pid,label=label):
     self.assertEqual(self.hard(label),{pid})
     self.assertNotIn(pid,self.hard('not '+label))
     self.assertNotIn(pid,self.hard(label,'excluded'))

 def test_every_relation_requires_all_three_connected_components(self):
  for pid,p in self.profiles.items():
   units=p['semantics']['visual_components']
   with self.subTest(profile=pid):
    self.assertIsNotNone(g.candidate_pack_visual_component_match(p,'; '.join(units)))
    for omitted in range(len(units)):
     self.assertIsNone(g.candidate_pack_visual_component_match(p,'; '.join(u for i,u in enumerate(units) if i!=omitted)))

 def test_descriptive_discovery_remains_optional_even_with_perfect_vector(self):
  for pid,p in self.profiles.items():
   vectors={key:([1.,0.] if key==pid else [0.,1.]) for key in self.profiles}
   index=g.build_visual_profile_index_payload(self.scoped,vectors=vectors,dimensions=2)
   text=p['semantics']['definition']
   result=g.resolve_visual_profile_hits(self.scoped,[{'source':'authorial_core_interpretation','text':text,'polarity':'advisory'}],
    visual_profile_index=index,query_text=text,query_vector=[1.,0.],adult_context=False)
   with self.subTest(profile=pid):
    hit=next(h for h in result['hits'] if h['profile_id']==pid)
    self.assertTrue(hit['optional_eligible']);self.assertFalse(hit['hard_eligible'])

 def test_roles_objects_and_unseen_causes_cannot_activate_these_relations(self):
  for text in ['a guardian angel','a merciful doctor after a crisis','a miracle with anonymous kindness',
               'a witness telling the truth','two people near separate coats','a tool beside a floating part',
               'a crowd feeling awe','a newspaper and a press badge','a coat worn by one person']:
   with self.subTest(text=text):self.assertFalse(self.hard(text))

 def test_material_trace_does_not_turn_unseen_history_into_positive_evidence(self):
  p=self.profiles['lor_received_item_material_trace_profile'];text=positive_visual_profile_text(p).lower()
  for word in ['rescue','healing','miracle','anonymous kindness','afcd94e0','d22fb070']:
   self.assertNotIn(word,text)
  self.assertEqual(p['semantics']['visual_components'][0],
   'the already declared item rests on a visible support within the recipient reach')

 def test_locked_owner_properties_cannot_be_changed_by_new_candidate_names(self):
  for p in self.profiles.values():
   effect=p['concept_candidate']['affected_properties'][0]
   lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[dict(effect)]}
   with self.subTest(profile=p['id']):
    self.assertFalse(property_effects_allowed(lock,p['concept_candidate']['affected_dimensions'],[effect]))
    lock['semantic_anchors'][0]['property']=effect['property'].split('.')[0]
    self.assertFalse(property_effects_allowed(lock,p['concept_candidate']['affected_dimensions'],[effect]))

 def test_compiler_rejects_unowned_component_and_preserves_complete_duties(self):
  for raw in self.raw_profiles:
   compiled=compile_visual_profile(raw)
   with self.subTest(profile=raw['id']):
    self.assertEqual(len(compiled['required_evidence_fields']),3)
    self.assertEqual(len(compiled['render_gates']),3)
    bad=copy.deepcopy(raw);bad['authored_components']['obligations'].pop()
    with self.assertRaises(ValueError):compile_visual_profile(bad)

if __name__=='__main__':unittest.main()
