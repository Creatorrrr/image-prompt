"""Real-corpus regression for occasion ownership and grounded retrieval."""
import copy
import json
import unittest
from pathlib import Path

from tests import photo_prompt_fixtures
import prompt_generator as g
import audit_composed_prompt as audit
import photo_candidate_context as context
from photo_contracts import property_effects_allowed

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
FIXTURES=ROOT/'tests/fixtures/photo_prompt/slot_retrieval_natural_v1'


class OccasionContextRetrievalTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=g.load_json(ASSETS/'photo_prompt_tags.json')
  cls.data[g.QUALITY_LAYERS_DATA_KEY]=g.load_quality_layers(ASSETS/'photo_prompt_quality_layers.json')
  cls.entries={e['id']:e for e in cls.data['slots']['occasion_context']}

 def inputs(self,key):
  row=json.loads((FIXTURES/key/'fixture.json').read_text())
  controls=row['creative_controls']
  core=g.normalize_authorial_core(row['authorial_core_input'],
       request_envelope=g.normalize_request_envelope(row['request_envelope_input']),
       creative_control_snapshot=controls)
  return core,controls

 def retrieved(self,key):
  core,controls=self.inputs(key);before=copy.deepcopy(core)
  slots,binding,_=g.retrieve_core_slots(self.data,core,controls)
  self.assertEqual(core,before)
  self.assertEqual(binding['candidate_adoption'],'optional')
  self.assertEqual(audit.audit_core_retrieval(dict(slots=slots,core_retrieval=binding,authorial_core=core,creative_controls=controls),self.data),[])
  return {r['entry_id'] for r in slots.get('occasion_context',{}).get('candidates',[])}

 def test_real_graduation_and_workshop_are_retrievable(self):
  for key,target in [('holdout-01-graduation-ko','graduation_after_ceremony'),('holdout-02-workshop-en','workshop_class_session'),('holdout-03-opening-en','opening_day_setup'),('holdout-04-eclipse-ko','eclipse_evening_watch')]:
   with self.subTest(key=key):self.assertIn(target,self.retrieved(key))

 def test_world_contexts_are_grounded_in_the_frozen_scene_without_internal_ids(self):
  for key,target in [('holdout-05-world-treaty-en','diegetic_larp_world_checkpoint_occasion'),('holdout-06-isekai-ko','isekai_frontier_guild_frontier_occasion')]:
   with self.subTest(key=key):
    core,_=self.inputs(key)
    self.assertNotIn('_scene',core['source_request'])
    self.assertIn(target,self.retrieved(key))

 def test_context_alternatives_preserve_existing_guards_and_do_not_borrow_candidate_tags(self):
  item={'requires_primary_any_tags':['legacy_scene'],'primary_context_alternatives':[['isekai','frontier','guild']]}
  primary={'subject':{'tags':['human']},'prop':{'tags':['isekai','frontier','guild']}}
  self.assertFalse(g.compatible_with_slot_context('occasion_context',item,primary))
  primary['location']={'tags':['isekai','frontier','guild']}
  self.assertTrue(g.compatible_with_slot_context('occasion_context',item,primary))
  self.assertFalse(context.primary_context_matches(item,{'frontier','guild'}))
  self.assertTrue(context.primary_context_matches(item,{'legacy_scene'}))
  item['exclude_any_tags']=['human']
  self.assertFalse(g.compatible_with_slot_context('occasion_context',item,primary))

 def test_nearest_world_contexts_do_not_open_the_wrong_occasion(self):
  cases=[('holdout-05-world-treaty-en','diegetic_larp_world_checkpoint_occasion',
          'at an ordinary real-world diplomatic meeting',
          'review a border treaty'),
         ('holdout-05-world-treaty-en','diegetic_larp_world_checkpoint_occasion',
          'in a fictional live-action roleplaying world',
          'review the local market accounts'),
         ('holdout-06-isekai-ko','isekai_frontier_guild_frontier_occasion',
          'at an isekai frontier village',
          'repair a fence before the caravan departs')]
  for key,target,setting,event in cases:
   with self.subTest(setting=setting,event=event):
    core,controls=self.inputs(key);core=copy.deepcopy(core)
    core.update(setting=setting,event=event,semantic_assertions=[],visual_priorities=[])
    if 'frontier village' in setting:core['subject']='Adult settlers'
    contract,picked=g.frozen_core_context(self.data,core,controls)
    self.assertFalse(g.core_slot_entry_eligible(self.data,core,contract,picked,'occasion_context',self.entries[target]))

 def test_ordinary_context_metadata_cannot_be_removed_after_retrieval(self):
  core,controls=self.inputs('holdout-05-world-treaty-en')
  slots,binding,_=g.retrieve_core_slots(self.data,core,controls)
  pack=dict(slots=slots,core_retrieval=binding,authorial_core=core,creative_controls=controls)
  self.assertEqual(audit.audit_core_retrieval(pack,self.data),[])
  candidate=next(r for r in pack['slots']['occasion_context']['candidates']
                 if r['entry_id']=='diegetic_larp_world_checkpoint_occasion')
  candidate.pop('context_prerequisites')
  self.assertTrue(audit.audit_core_retrieval(pack,self.data))

 def test_alternative_contract_requires_every_fact_of_one_final_context(self):
  entry={'requires_primary_any_tags':['legacy_scene'],'primary_context_alternatives':[['roleplaying','world','treaty']]}
  candidate={'id':'example'};candidate.update(context.compile_context(entry,'example'))
  contract=candidate['context_prerequisites'];self.assertEqual(contract['contract_version'],context.ALTERNATIVE_VERSION)
  prompt='Adult delegates in a roleplaying world review a border treaty together at a table.'
  review={'requirement_evidence':[{'requirement_id':'entry:primary_any','fact':fact,'state':'present',
           'prompt_evidence':prompt,'reason':'The retained scene contains the stated primary context.',
           'origin':'retained','affected_dimensions':[]} for fact in ['roleplaying','world','treaty']]}
  core={'baseline_prompt_en':prompt,'intent_lock':{'contract_version':'photo-intent-lock/v2','semantic_anchors':[]}}
  self.assertEqual(context.audit_context(candidate,review,prompt_en=prompt,core=core,brief={},subject_category='human',allowed=set()),[])
  review['requirement_evidence'].pop()
  self.assertTrue(context.audit_context(candidate,review,prompt_en=prompt,core=core,brief={},subject_category='human',allowed=set()))
  for invalid in [[],[[]],[['guild','guild']],[[None]],'guild']:
   with self.subTest(invalid=invalid),self.assertRaises(ValueError):context.primary_context_alternatives(invalid)

 def test_final_context_is_required_only_when_the_real_candidate_is_adopted(self):
  core,controls=self.inputs('holdout-05-world-treaty-en')
  slots,_,_=g.retrieve_core_slots(self.data,core,controls)
  candidate=next(r for r in slots['occasion_context']['candidates']
                 if r['entry_id']=='diegetic_larp_world_checkpoint_occasion')
  cid=candidate['id'];prompt=core['baseline_prompt_en'];evidence=prompt.split('. ')[0]
  row={'candidate_id':cid,'context_review':{'requirement_evidence':[
       {'requirement_id':'entry:primary_any','fact':fact,'state':'present',
        'prompt_evidence':evidence,'reason':'The retained scene explicitly carries this primary context.',
        'origin':'retained','affected_dimensions':[]} for fact in ['roleplaying','world','treaty']]}}
  pack={'authorial_core':core,'creative_controls':controls};candidates={cid:candidate}
  self.assertEqual(audit.audit_declared_candidate_contexts(pack,prompt,set(),candidates,[]),[])
  self.assertTrue(audit.audit_declared_candidate_contexts(pack,prompt,{cid},candidates,[]))
  self.assertEqual(audit.audit_declared_candidate_contexts(pack,prompt,{cid},candidates,[row]),[])
  row['context_review']['requirement_evidence'].pop()
  failures=audit.audit_declared_candidate_contexts(pack,prompt,{cid},candidates,[row])
  self.assertTrue(failures)
  self.assertTrue(all(f['check']=='candidate_context_prerequisites' for f in failures))

 def test_unrelated_still_life_and_plant_receive_no_occasion_padding(self):
  for key in ['dev-02-blue-cup-en','dev-07-dew-leaf-ko','holdout-07-cup-ko','holdout-09-landscape-en']:
   with self.subTest(key=key):self.assertEqual(self.retrieved(key),set())

 def test_special_world_context_is_not_satisfied_by_an_ordinary_graduate(self):
  ids=self.retrieved('holdout-01-graduation-ko')
  self.assertTrue(ids)
  self.assertFalse(any(self.entries[key].get('requires_primary_any_tags')==['diegetic_larp_world_checkpoint_scene'] for key in ids))
  self.assertTrue(all(key in {'graduation_after_ceremony'} for key in ids))

 def test_occasion_phase_and_actual_clock_effects_cannot_bypass_partial_locks(self):
  phase={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'timing','target':'scene','property':'occasion.phase'}]}
  clock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'timing','target':'scene','property':'time_of_day'}]}
  for key in ['graduation_after_ceremony','afterparty_dawn_cleanup','eclipse_evening_watch']:
   entry=self.entries[key]
   self.assertFalse(property_effects_allowed(phase,entry['affected_dimensions'],entry['affected_properties']))
  for key in ['afterparty_dawn_cleanup','eclipse_evening_watch','blackout_night_gathering','last_summer_evening']:
   entry=self.entries[key]
   self.assertFalse(property_effects_allowed(clock,entry['affected_dimensions'],entry['affected_properties']))

 def test_all_registered_occasion_sources_have_complete_declared_scope(self):
  self.assertEqual(len(self.entries),106)
  self.assertEqual(g.photo_candidate_semantics.slot_dimensions('occasion_context',self.data['candidate_semantic_policy']),['event','timing'])
  for key,entry in self.entries.items():
   with self.subTest(key=key):
    self.assertTrue(entry['affected_dimensions'])
    self.assertEqual(set(entry['affected_dimensions']),{row['dimension'] for row in entry['affected_properties']})
    self.assertTrue(entry['requires_primary_any_tags'])

 def test_base_occasion_meaning_does_not_impose_unrequested_text_suppression(self):
  raw=json.loads((ASSETS/'photo_prompt_tags.json').read_text())
  for entry in raw['slots']['occasion_context']:
   text=' '.join(str(entry.get(k,'')) for k in ['en','ko','embedding_text','phrase_en','phrase_ko']).lower()
   for phrase in ['no readable','kept unreadable','without readable','non-graphic','읽히는 현수막 없이']:
    self.assertNotIn(phrase,text,entry['id'])
   self.assertNotIn('no_text',entry.get('tags',[]))


if __name__=='__main__':unittest.main()
