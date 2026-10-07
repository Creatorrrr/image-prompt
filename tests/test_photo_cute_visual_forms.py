"""Equivalent paraphrases, owner boundaries and advisory retrieval contracts."""
from __future__ import annotations
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(SCRIPTS))
import prompt_generator as g
import photo_candidate_semantics as semantics
from photo_contracts import property_effects_allowed

ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
EXT='photo_prompt_cute_visual_forms_extension.json'

class CuteVisualFormsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension=json.loads((ASSETS/EXT).read_text())
        cls.data=g.load_json(ASSETS/'photo_prompt_tags.json')
        cls.registry=g.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
        cls.profiles={p['id']:p for p in cls.registry['profiles']}
        cls.new_profiles=json.loads((ASSETS/'photo_prompt_visual_obligations_cute_visual_forms.json').read_text())['profiles']

    def matches(self,text):
        return set(g.candidate_pack_auto_visual_obligation_matches(self.registry,[dict(source='concept_lock',text=text,polarity='required',priority='critical',mandatory=True)]))

    def test_equivalent_overlay_preserves_all_existing_meaning_effects_and_guards(self):
        inventory=g.photo_source_manifest.SourceInventory.for_test(ASSETS,candidate_files=tuple(n for n in g.RESEARCH_EXTENSION_FILENAMES if n not in {EXT,'photo_prompt_visual_grammar_extension.json'}))
        before=g.load_json(ASSETS/'photo_prompt_tags.json',inventory=inventory)
        for slot,updates in self.extension['existing_slot_context_extensions'].items():
            old={e['id']:e for e in before['slots'][slot]};new={e['id']:e for e in self.data['slots'][slot]}
            for eid,addition in updates.items():
                with self.subTest(candidate=eid):
                    retained=set(old[eid])-{'paraphrases','contextual_usage'}
                    self.assertEqual({k:old[eid][k] for k in retained},{k:new[eid][k] for k in retained})
                    old_usage=old[eid].get('contextual_usage',{})
                    new_usage=new[eid].get('contextual_usage',{})
                    old_contexts=old_usage.get('contexts',[])
                    self.assertEqual(new_usage.get('contexts',[])[:len(old_contexts)],old_contexts)
                    self.assertEqual({k:new_usage[k] for k in old_usage if k!='contexts'},
                                     {k:v for k,v in old_usage.items() if k!='contexts'})
                    self.assertTrue(set(old[eid].get('paraphrases',[]))<=set(new[eid]['paraphrases']))
                    self.assertTrue(set(addition['paraphrases'])<=set(new[eid]['paraphrases']))
                    positive=g.semantic_text_for_entry(new[eid],slot)
                    for phrase in addition['paraphrases']:self.assertIn(phrase,positive)
                    self.assertNotIn('No emotion, age, universal cuteness',positive)

    def test_cultural_and_unreviewed_labels_do_not_create_fixed_form_obligations(self):
        for text in ['an adult woman in a kawaii portrait','an adult woman showing aegyo','an adult woman with tehepero',
                     'an adult woman with gyaru peace','an adult woman making a finger heart','an adult woman with cute aggression',
                     'an adult woman, no small O-shaped mouth','an adult woman without one-heel-raised stance',
                     'a corneal catchlight reflection diagram','a robot with a small O-shaped mouth']:
            with self.subTest(text=text):self.assertFalse(any(x.startswith('cv_profile_') for x in self.matches(text)))

    def test_each_narrow_form_is_human_scoped_and_every_component_is_a_native_gate(self):
        for raw in self.new_profiles:
            with self.subTest(profile=raw['id']):
                term=raw['activation']['exact_terms'][0]
                self.assertIn(raw['id'],self.matches('an adult human actor showing '+term))
                p=self.profiles[raw['id']];components=p['authored_components']['components']
                self.assertEqual(len(components),len(p['render_gates']))
                self.assertEqual(p['semantics']['component_semantics']['minimum_component_groups'],len(components))
                for gate in p['render_gates']:
                    self.assertEqual(gate['review_scale'],'native')
                    self.assertIn('partial evidence fails',gate['description'])
                    self.assertIn('occlusion is unobservable',gate['description'])

    def test_contact_and_expression_effects_do_not_cross_partial_locks(self):
        entries={e['id']:e for rows in self.extension['slots'].values() for e in rows}
        for eid,dim,prop in [('cv_two_cheek_press','expression','face.expression'),('cv_hand_heart_tips','pose','body.hand_configuration'),
                             ('cv_partner_sleeve_pinch','relationship','partner_sleeve.contact')]:
            e=entries[eid]
            lock=dict(contract_version='photo-intent-lock/v2',open_dimensions=e['affected_dimensions'],semantic_anchors=[dict(dimension=dim,target='main_subject',property=prop)])
            self.assertFalse(property_effects_allowed(lock,e['affected_dimensions'],e['affected_properties']))

    def test_deferred_original_finger_heart_is_not_silently_restored(self):
        self.assertNotIn('pv_finger_heart',{e['id'] for rows in self.data['slots'].values() for e in rows})
        entry=next(e for e in self.extension['slots']['hand_pose'] if e['id']=='cv_thumb_index_cross')
        self.assertNotIn('finger heart',entry['aliases'])
        self.assertNotIn('money',entry['aliases'])

    def test_bundle_selection_is_optional_and_does_not_activate_the_linked_profile(self):
        for b in self.extension['visual_semantics']:
            self.assertTrue(b['candidate_only'])
            self.assertEqual(len(b['hard_profile_ids']),1)
            self.assertTrue(b['component_groups'])

    def test_maintenance_sources_and_deferred_names_stay_out_of_positive_search(self):
        record=json.loads((ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/cute-visual-forms-20261005-v1.json').read_text())
        self.assertEqual(semantics.digest(record),self.extension['maintenance_ref']['sha256'])
        for rows in self.extension['slots'].values():
            for e in rows:
                positive=g.semantic_text_for_entry(e,next(slot for slot,values in self.extension['slots'].items() if e in values))
                self.assertNotIn('https://',positive)
                self.assertNotIn('Historical deferred',positive)

if __name__=='__main__':unittest.main()
