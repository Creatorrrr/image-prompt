from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ASSETS.parent/'scripts'))
import prompt_generator as generator
import photo_candidate_semantics as semantics
import audit_composed_prompt as auditor
from photo_contracts import property_effects_allowed


class PhotoDomainAdultScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=generator.load_json(ASSETS/'photo_prompt_tags.json')
        cls.data[generator.QUALITY_LAYERS_DATA_KEY]=generator.load_quality_layers(ASSETS/'photo_prompt_quality_layers.json')
        cls.fixtures=ROOT/'tests/fixtures/photo_prompt/domain_adult_scope_v1'

    def frozen(self,key):
        values=json.loads((self.fixtures/key/'fixture.json').read_text())
        controls=values['creative_controls']
        core=generator.normalize_authorial_core(values['authorial_core_input'],
            request_envelope=generator.normalize_request_envelope(values['request_envelope_input']),creative_control_snapshot=controls)
        return core,controls

    def test_general_domains_are_grounded_in_frozen_positive_meaning(self):
        for key in ['portrait','fashion','beauty','social']:
            for language in ['en','ko']:
                with self.subTest(key=key,language=language):
                    core,controls=self.frozen(key+'-'+language)
                    contract,_=generator.frozen_core_context(self.data,core,controls)
                    self.assertIn(key,contract['domains'])
                    self.assertNotIn('adult',contract['domains'])

    def test_explicit_sexual_context_survives_zero_controls(self):
        for key in ['suggestive-social','fetish-fashion','nightlife']:
            for language in ['en','ko']:
                with self.subTest(key=key,language=language):
                    core,controls=self.frozen(key+'-'+language)
                    self.assertTrue(all(controls['adult_appeal'][a]['effective_intensity']==0 for a in ['sensual','fetish']))
                    contract,_=generator.frozen_core_context(self.data,core,controls)
                    self.assertIn('adult',contract['domains'])
                    self.assertTrue(contract['adult_allowed'])

    def test_age_and_controls_do_not_create_an_adult_domain(self):
        for key in ['age-only','controls-only','fit-check','original-design','material-study','latex-neutral','zipper-neutral']:
            for language in ['en','ko']:
                with self.subTest(key=key,language=language):
                    core,controls=self.frozen(key+'-'+language)
                    contract,_=generator.frozen_core_context(self.data,core,controls)
                    self.assertNotIn('adult',contract['domains'])
                    self.assertIsNotNone(generator.slot_block_reason(self.data,'adult_context',contract))
                    self.assertIsNotNone(generator.slot_block_reason(self.data,'fetish_styling',contract))
                    if key!='controls-only':self.assertFalse(contract['adult_allowed'])

    def test_style_domain_is_not_request_meaning(self):
        core,controls=self.frozen('age-only-en')
        for domain in ['adult','portrait','fashion','beauty','social']:
            with self.subTest(domain=domain):
                modified=copy.deepcopy(core);modified['style']['domain']=domain
                contract,_=generator.frozen_core_context(self.data,modified,controls)
                self.assertNotIn(domain,contract['domains'])

    def test_excluded_assertions_and_terms_never_route_positive_domains(self):
        core,controls=self.frozen('age-only-en')
        for term in ['fetish fashion','sexually suggestive','페티시 패션','성적 매력','beauty','portrait']:
            with self.subTest(term=term):
                modified=copy.deepcopy(core);modified['interpreted_intent']=term
                modified['user_exclusions']=[term]
                modified['semantic_assertions'].append(dict(polarity='excluded',axes={'meaning':term}))
                contract,_=generator.frozen_core_context(self.data,modified,controls)
                self.assertFalse(set(contract['domains']) & {'adult','fashion','beauty','portrait'})
        for text in ['without fetish fashion','avoid sexually suggestive','fetish fashion is excluded','페티시 패션은 제외','성적 매력 없는']:
            with self.subTest(negation=text):
                modified=copy.deepcopy(core);modified['interpreted_intent']=text
                contract,_=generator.frozen_core_context(self.data,modified,controls)
                self.assertNotIn('adult',contract['domains'])

    def test_nonhuman_and_no_people_do_not_gain_adult_subject_scope(self):
        for key in ['nonhuman-object-en','nonhuman-animal-ko']:
            with self.subTest(key=key):
                core,controls=self.frozen(key)
                contract,picked=generator.frozen_core_context(self.data,core,controls)
                self.assertNotIn('adult',contract['domains']);self.assertFalse(contract['adult_allowed'])
                self.assertIsNotNone(generator.slot_block_reason(self.data,'adult_context',contract))
                for entry in self.data['slots']['wardrobe_style']:
                    if entry['id']=='glossy_latex_look':self.assertFalse(generator.core_slot_entry_eligible(self.data,core,contract,picked,'wardrobe_style',entry))

    def test_migrations_preserve_identity_weight_labels_and_references(self):
        roles=json.loads((self.fixtures/'source_roles.json').read_text())
        self.assertEqual(len(roles),30);self.assertEqual(sum(r['source_slot']!=r['target_slot'] for r in roles),26)
        for role in roles:
            with self.subTest(identity=role['entry_id']):
                source=generator.candidate_pack_slot_entry_by_id(self.data,role['target_slot'],role['entry_id'])
                self.assertEqual(source['weight'],role['weight'])
                self.assertEqual(source['en'],role['en']);self.assertEqual(source['ko'],role['ko'])
                self.assertEqual(source['affected_dimensions'],role['dimensions'])
                self.assertEqual(source['affected_properties'],role['properties'])
                self.assertEqual(source.get('core_assertion_discovery',False),role['discovery'])
                if role['source_slot']!=role['target_slot']:
                    self.assertFalse(any(e['id']==role['entry_id'] for e in self.data['slots'][role['source_slot']]))
                    self.assertFalse(generator.adult_semantic_tokens(source)&{'adult','fetish','suggestive'})
                    self.assertNotIn('sexual_tone',source['affected_dimensions'])
                    for key in role['preserved']:
                        if key in role['preserved']:self.assertEqual(source.get(key),role['preserved'][key])
        policy=generator.candidate_pack_adult_policy(self.data)
        for source_key in policy['entry_dimensions']:
            slot,identity=source_key.split(':',1)
            self.assertTrue(generator.candidate_pack_slot_entry_by_id(self.data,slot,identity))
        for bundle in self.data['candidate_bundles']:
            for member in bundle['member_candidates']:
                self.assertTrue(generator.candidate_pack_slot_entry_by_id(self.data,member['slot'],member['entry_id']))

    def test_neutral_context_requires_the_actual_frozen_context(self):
        core,controls=self.frozen('age-only-en');contract,picked=generator.frozen_core_context(self.data,core,controls)
        for slot,identity in [('genre','adult_original_fantasy_character_context'),('genre','adult_fashion_material_study_context'),('platform_framing','adult_fit_check_body_check_context')]:
            with self.subTest(identity=identity):
                entry=generator.candidate_pack_slot_entry_by_id(self.data,slot,identity)
                self.assertFalse(generator.core_slot_entry_eligible(self.data,core,contract,picked,slot,entry))
        for key,slot,identity in [('original-design-en','genre','adult_original_fantasy_character_context'),('material-study-en','genre','adult_fashion_material_study_context'),('fit-check-en','platform_framing','adult_fit_check_body_check_context')]:
            with self.subTest(positive=key):
                core,controls=self.frozen(key);contract,picked=generator.frozen_core_context(self.data,core,controls)
                entry=generator.candidate_pack_slot_entry_by_id(self.data,slot,identity)
                self.assertTrue(generator.core_slot_entry_eligible(self.data,core,contract,picked,slot,entry))

    def test_complete_material_effect_rejects_closed_property_adoption(self):
        core,_=self.frozen('latex-property-lock-en')
        entry=generator.candidate_pack_slot_entry_by_id(self.data,'wardrobe_style','glossy_latex_look')
        self.assertFalse(property_effects_allowed(core['intent_lock'],entry['affected_dimensions'],entry['affected_properties']))
        candidate=semantics.semantic_source(entry,'wardrobe_style',self.data['candidate_semantic_policy'])
        candidate.update(id='slot:wardrobe_style:glossy_latex_look',slot='wardrobe_style',entry_id=entry['id'],concept_terms=['glossy latex-look fashion pieces'])
        phrase='The garment gains glossy latex-look material and smooth highlights.'
        pack=dict(contract_version='photo-candidate-pack/v6',authorial_core=core)
        composed={'candidate_interpretations':[dict(candidate_id=candidate['id'],artistic_interpretation='Emphasize the smooth reflective garment surface.',transformation='Use the glossy finish along the folds.',prompt_evidence=phrase,affected_properties=entry['affected_properties'])]}
        failures=auditor.audit_candidate_interpretations(pack,composed,phrase,{candidate['id']},{candidate['id']:candidate})
        self.assertIn('candidate_interpretation_properties',{row['check'] for row in failures})

    def test_closed_sexual_tone_disallows_complete_context_effect(self):
        core,_=self.frozen('sexual-tone-locked-en')
        candidate=generator.candidate_pack_slot_entry_by_id(self.data,'adult_context','adult_fetish_fashion_context')
        self.assertIn('sexual_tone',candidate['affected_dimensions'])
        self.assertFalse(set(candidate['affected_dimensions']).issubset(set(core['intent_lock']['open_dimensions'])))


if __name__=='__main__':unittest.main()
