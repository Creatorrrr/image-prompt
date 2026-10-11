"""Real-corpus guards for optional body/wardrobe attachment relations."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from tests import photo_prompt_fixtures
import prompt_generator as g
import audit_composed_prompt as audit
from photo_contracts import property_effects_allowed

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
FIXTURES=ROOT/'tests/fixtures/photo_prompt/slot_guard_roles_v1'

class SlotGuardRoleTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=g.load_json(ASSETS/'photo_prompt_tags.json')
  cls.data[g.QUALITY_LAYERS_DATA_KEY]=g.load_quality_layers(ASSETS/'photo_prompt_quality_layers.json')
  cls.review=json.loads((FIXTURES/'ROLE-DECISIONS.json').read_text())
  cls.retired={r['entry_id'] for r in cls.review['rows'] if r['decision']=='retire_control_candidate'}
  cls.migrated={r['entry_id'] for r in cls.review['rows'] if r['decision']=='migrate_optional_relation'}
  cls.entries={e['id']:e for e in cls.data['slots']['anatomical_connection']}

 def inputs(self,key):
  row=json.loads((FIXTURES/key/'fixture.json').read_text());controls=row['creative_controls']
  core=g.normalize_authorial_core(row['authorial_core_input'],request_envelope=g.normalize_request_envelope(row['request_envelope_input']),creative_control_snapshot=controls)
  self.assertEqual(core['canonical_sha256'],row['freeze_receipt']['contracts']['core'])
  return core,controls

 def packet(self,key):
  core,controls=self.inputs(key);original=copy.deepcopy(core)
  slots,binding,_=g.retrieve_core_slots(self.data,core,controls)
  self.assertEqual(core,original)
  self.assertEqual(binding['candidate_adoption'],'optional')
  pack=dict(slots=slots,core_retrieval=binding,authorial_core=core,creative_controls=controls)
  self.assertEqual(audit.audit_core_retrieval(pack,self.data),[])
  return pack

 def test_control_retirement_preserves_provenance_without_a_live_suppression_path(self):
  self.assertEqual(len(self.review['rows']),33);self.assertEqual(len(self.retired),28)
  self.assertEqual(len(self.migrated),5)
  ids={entry['id'] for rows in self.data['slots'].values() for entry in rows}
  self.assertFalse(ids & self.retired)
  for slot in ['safety_profile','costume_absorption_guard']:
   self.assertNotIn(slot,self.data['slots'])
   self.assertNotIn(slot,self.data['candidate_semantic_policy']['slot_dimensions'])
   self.assertNotIn(slot,self.data['slot_applicability']['slots'])
  for row in self.review['rows']:
   digest=hashlib.sha256(json.dumps(row['original_entry'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   self.assertEqual(digest,row['original_entry_sha256'])

 def test_both_requested_carriers_retrieve_the_relation_with_the_same_frozen_core(self):
  cases=[('horn-crown-en','ornate_headpiece_not_horn_guard'),('hood-ears-ko','hood_trim_not_ears_guard'),
   ('feathers-boa-en','stage_feathers_not_body_guard'),('rabbit-headband-ko','costume_bunny_ears_separate_from_anatomy_guard'),
   ('fur-lace-en','lace_frill_not_fur_guard'),('wardrobe-lock-positive-en','hood_trim_not_ears_guard')]
  for key,target in cases:
   with self.subTest(key=key):
    pack=self.packet(key)
    self.assertIn(target,{r['entry_id'] for r in pack['slots'].get('anatomical_connection',{}).get('candidates',[])})

 def test_single_carrier_and_ordinary_costume_scenes_do_not_invent_living_anatomy(self):
  for key in ['horn-ornament-only-en','hood-trim-only-ko','feather-accessory-only-en','rabbit-costume-only-ko',
    'lace-textile-only-en','horn-without-headpiece-en','closed-helmet-lock-ko','royal-selfie-en']:
   with self.subTest(key=key):
    core,controls=self.inputs(key);contract,picked=g.frozen_core_context(self.data,core,controls)
    for identifier in self.migrated:
     self.assertFalse(g.core_slot_entry_eligible(self.data,core,contract,picked,'anatomical_connection',self.entries[identifier]),identifier)
    ids={r['entry_id'] for rows in self.packet(key)['slots'].values() for r in rows['candidates']}
    self.assertFalse(ids & (self.migrated|self.retired))

 def test_optional_prop_or_candidate_tags_cannot_supply_a_required_body_context(self):
  entry=self.entries['hood_trim_not_ears_guard']
  picked={'subject':dict(tags=['human'],kind=['human']),'prop':dict(tags=['beastkin','hood'])}
  self.assertFalse(g.compatible_with_slot_context('anatomical_connection',entry,picked,self.data))
  picked['subject']['tags'] += ['beastkin','hood']
  self.assertTrue(g.compatible_with_slot_context('anatomical_connection',entry,picked,self.data))

 def test_wardrobe_locks_allow_attachments_and_block_worn_state_color_material_changes(self):
  core,_=self.inputs('wardrobe-lock-positive-en');entry=self.entries['hood_trim_not_ears_guard']
  self.assertTrue(property_effects_allowed(core['intent_lock'],entry['affected_dimensions'],entry['affected_properties']))
  for prop in ['wardrobe.hood.worn_state','wardrobe.hood.color','wardrobe.hood.trim.material_class','wardrobe.hood']:
   with self.subTest(prop=prop):
    self.assertFalse(property_effects_allowed(core['intent_lock'],['body_geometry'],[
     dict(dimension='body_geometry',target='main_subject',property=prop)]))

 def test_retrieved_context_mutation_is_recomputed_before_public_semantic_projection(self):
  pack=self.packet('hood-ears-ko')
  for field in ['context_prerequisites','context_requirements','context_preflight']:
   with self.subTest(field=field):
    changed=copy.deepcopy(pack)
    row=next(r for r in changed['slots']['anatomical_connection']['candidates'] if r['entry_id']=='hood_trim_not_ears_guard')
    row.pop(field)
    self.assertTrue(audit.audit_core_retrieval(changed,self.data))

 def test_positive_documents_exclude_control_directives_but_keep_both_attachment_owners(self):
  for identifier in self.migrated:
   row=self.entries[identifier];text=g.semantic_text_for_entry(row,'anatomical_connection',kind='slot')
   self.assertNotRegex(text,r'(?i)\b(?:anti[-_ ]|suppress|never|only|not the|do not)')
   self.assertIn('appearance',row['affected_dimensions']);self.assertIn('body_geometry',row['affected_dimensions'])
   self.assertEqual(row['for_any'],['human'])
   self.assertTrue(row['primary_context_alternatives'])
   for relation in row['relations']:
    self.assertIn(relation['subject'],text);self.assertIn(relation['object'],text)

if __name__=='__main__':unittest.main()
