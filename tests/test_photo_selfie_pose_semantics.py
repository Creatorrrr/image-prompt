"""Selfie contact, reflection, activation and property-scope regressions."""
from __future__ import annotations
import copy, json, unittest
from pathlib import Path
from tests import photo_prompt_fixtures
import prompt_generator as generator
from photo_contracts import property_effects_allowed
from photo_candidate_semantics import digest
from visual_profile_contracts import validate_visual_profile_source, compile_visual_profile

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
EVIDENCE=ROOT/'docs/research-evidence/photo-prompt/selfie-pose-integration-20261008'

class SelfiePoseSemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension=json.loads((ASSETS/'photo_prompt_selfie_pose_extension.json').read_text())
        cls.source=json.loads((ASSETS/'photo_prompt_visual_obligations_selfie_pose.json').read_text())
        cls.registry=generator.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
        cls.profiles={p['id']:p for p in cls.source['profiles']}
        cls.candidates={c['id']:c for rows in cls.extension['slots'].values()for c in rows}
        # Keep compiler/activation unit checks focused; full corpus/index checks
        # and live packs are exercised separately after index rebuilding.
        cls.focus_registry=dict(cls.registry)
        cls.focus_registry['profiles']=[p for p in cls.registry['profiles']if p['id'].startswith('sf_profile_')or p['id']=='mirror_selfie_reflection_device_topology']
        cls.exact_index=generator.build_visual_profile_index_payload(cls.focus_registry)
    def matches(self,text):
        r=generator.resolve_visual_profile_hits(self.focus_registry,[{'source':'concept_lock','text':text,'polarity':'required','priority':'critical','mandatory':True}],visual_profile_index=self.exact_index,adult_context=True)
        return {h['profile_id']for h in r['hits']if h['match_basis']=='exact'and h['hard_eligible']}
    def test_all_numbered_units_have_a_reviewed_runtime_path(self):
        rows=json.loads((EVIDENCE/'coverage-180.json').read_text())
        self.assertEqual({r['research_unit_id']for r in rows},{f'SF{n:03d}'for n in range(1,181)})
        self.assertEqual(len(self.candidates),104);self.assertEqual(len(self.profiles),101)
        for row in rows:
            with self.subTest(unit=row['research_unit_id']):
                self.assertTrue(row['new_variants']or row['existing_component_refs'])
                for variant in row['new_variants']:
                    self.assertIn(variant['candidate_id'],self.candidates);self.assertIn(variant['profile_id'],self.profiles)
    def test_each_exact_activation_is_narrow_and_has_complete_source_contract(self):
        for profile in self.profiles.values():
            with self.subTest(profile=profile['id']):
                validate_visual_profile_source(profile);compiled=compile_visual_profile(profile)
                self.assertEqual(len(compiled['render_gates']),3)
                for term in profile['activation']['exact_terms']:
                    context='A human photographic portrait pose with two declared people: 'if profile['id']in ['sf_profile_141_base','sf_profile_143_base','sf_profile_147_base','sf_profile_149_base']else'A human photographic portrait pose: '
                    self.assertIn(profile['id'],self.matches(context+term))
    def test_negated_exact_terms_do_not_create_the_corresponding_hard_duty(self):
        for profile in self.profiles.values():
            term=profile['activation']['exact_terms'][-1]
            with self.subTest(profile=profile['id']):
                self.assertNotIn(profile['id'],self.matches('A human photographic portrait pose without '+term))
    def test_mirror_phone_half_cover_does_not_mean_hand_half_cover(self):
        hand=self.matches('A human portrait pose: 얼굴 반 가리기')
        self.assertNotIn('sf_profile_092_base',hand)
        phone=self.matches('A human portrait pose: physical mirror selfie Half face cover')
        # Use the source-qualified spelling rather than inventing a label translation.
        term=self.profiles['sf_profile_092_base']['activation']['exact_terms'][0]
        self.assertIn('sf_profile_092_base',self.matches('A human portrait pose: '+term))
        self.assertNotIn('sf_profile_034_base',phone)
    def test_neutral_mouth_eye_smile_does_not_claim_every_smize_is_neutral(self):
        self.assertIn('sf_profile_004_base',self.matches('A human portrait pose: 입 중립형 눈웃음'))
        self.assertNotIn('sf_profile_004_base',self.matches('A human portrait pose: 눈웃음'))
        self.assertNotIn('sf_profile_004_base',self.matches('A human portrait pose: Smize'))
    def test_unverified_names_and_nonhuman_objects_are_not_exact_duties(self):
        for phrase in ['고양이 하트','cat heart','밤비 포즈','bambi pose','a T-Rex dinosaur toy','a V-shaped antenna','a political Gen Z stare']:
            with self.subTest(phrase=phrase):
                self.assertFalse(any(p.startswith('sf_profile_')for p in self.matches(phrase)))
        self.assertFalse(self.candidates['sf_056_base']['aliases'])
    def test_finger_heart_shaka_and_rock_have_different_digit_configuration(self):
        shaka=self.candidates['sf_050_base']['en'];rock=self.candidates['sf_168_base']['en'];heart=self.candidates['sf_051_base']['en']
        self.assertIn('thumb',shaka);self.assertIn('little',shaka)
        self.assertIn('index',rock);self.assertIn('little',rock)
        self.assertIn('thumb',heart);self.assertIn('index',heart)
        self.assertNotEqual(shaka,rock)
    def test_one_and_two_hand_book_grips_remain_separate(self):
        one=self.candidates['sf_133_one_hand'];two=self.candidates['sf_133_two_hand']
        self.assertNotEqual(one['concept_units'][0],two['concept_units'][0])
        self.assertEqual(one['requires_any_tags'],['book'])
        self.assertEqual(two['requires_all_tags'],['book'])
        self.assertNotIn('book',two['requires_any_tags'])
    def test_cosmetic_tool_contacts_are_separate(self):
        for variant,needle in [('lipstick','lip'),('brush','cheek'),('puff','cheek')]:
            c=self.candidates['sf_135_'+variant]
            self.assertIn(needle,c['en']);self.assertTrue(c['requires_any_tags'])
            self.assertTrue(any(e['dimension']=='appearance'for e in c['affected_properties']))
    def test_camera_target_and_axes_preserve_requester_height_and_direction(self):
        for cid in ['sf_071_base','sf_072_base','sf_073_base','sf_074_base','sf_075_base','sf_076_base','sf_088_base','sf_150_base']:
            c=self.candidates[cid]
            self.assertTrue(all(e['target']=='camera'for e in c['affected_properties']if e['dimension']=='camera'))
            lock={'contract_version':'photo-intent-lock/v2','open_dimensions':c['affected_dimensions'],'semantic_anchors':[{'dimension':'camera','target':'camera','property':'viewpoint.height'}]}
            self.assertFalse(property_effects_allowed(lock,c['affected_dimensions'],c['affected_properties']),cid)
    def test_locked_hand_hair_and_crop_properties_block_conflicting_candidates(self):
        for cid,dimension,target,prop in [('sf_044_base','pose','main_subject','body.hand_configuration'),('sf_061_base','appearance','main_subject','hair.arrangement'),('sf_079_base','framing','image','crop')]:
            c=self.candidates[cid];lock={'contract_version':'photo-intent-lock/v2','open_dimensions':c['affected_dimensions'],'semantic_anchors':[{'dimension':dimension,'target':target,'property':prop}]}
            self.assertFalse(property_effects_allowed(lock,c['affected_dimensions'],c['affected_properties']))
    def test_group_roles_and_panel_counts_remain_literal(self):
        self.assertIn('another actor',self.candidates['sf_143_base']['en'])
        self.assertIn('four distinct panels',self.candidates['sf_148_base']['en'])
        self.assertTrue(any(e['dimension']=='format'for e in self.candidates['sf_148_base']['affected_properties']))
        for cid in ['sf_141_base','sf_143_base','sf_147_base','sf_149_base']:
            self.assertEqual(self.candidates[cid]['requires_any_tags'],['partner','pair','couple','group'])
        self.assertEqual(self.candidates['sf_147_base']['requires_all_tags'],['mirror'])
    def test_capture_inputs_are_not_promoted_into_unmeasured_pixel_gates(self):
        for cid in ['sf_capture_direct_handheld','sf_capture_physical_mirror','sf_capture_fixed_self_portrait']:
            self.assertIn(cid,self.candidates)
        for pid in ['sf_profile_072_base','sf_profile_075_base','sf_profile_089_base']:
            profile=self.profiles[pid]
            self.assertTrue(all('actual camera' in g['render_gate']['description']for g in profile['authored_components']['components']))
    def test_capture_mechanics_are_reachable_without_a_social_genre_declaration(self):
        data=generator.load_json(ASSETS/'photo_prompt_tags.json')
        contract={'subject_category':'human','domains':[]}
        self.assertIsNone(generator.slot_block_reason(data,'capture_mode',contract))
        self.assertEqual(generator.slot_block_reason(data,'capture_context',contract),'request_domain_not_allowed')
        self.assertEqual(len(self.extension['slots']['capture_mode']),12)
        self.assertNotIn('capture_context',self.extension['slots'])
        queries,fields=generator.core_slot_focus_queries(data,{
            'contract_version':'photo-authorial-core/v3','subject':'a person',
            'setting':'a craft workshop','event':'repairing an object',
            'style':{'domain':'portrait','family':'a handheld self portrait','evidence':[]},'visual_priorities':[],
            'request_binding':{'active_spans':[]},'intent_lock':{'semantic_anchors':[]},
            'semantic_assertions':[]},'capture_mode')
        self.assertTrue(any('handheld self portrait'in q for q in queries))
        self.assertIn('style',fields)
    def test_embedding_paraphrase_can_discover_an_optional_profile_without_literal_components(self):
        index=copy.deepcopy(self.exact_index)
        index['embedding_dimensions']=2
        for pid,entry in index['entries'].items():entry['vector']=[1.0,0.0]if pid=='sf_profile_050_base'else[0.0,1.0]
        text='A photographed person extends the little digit and opposable digit while the three middle digits curl inward.'
        self.assertIsNone(generator.candidate_pack_visual_component_match(
            next(p for p in self.focus_registry['profiles']if p['id']=='sf_profile_050_base'),text))
        r=generator.resolve_visual_profile_hits(self.focus_registry,
            [{'source':'authorial_core_baseline','text':text,'polarity':'advisory'}],
            visual_profile_index=index,query_text=text,query_vector=[1.0,0.0],adult_context=False)
        target=next(h for h in r['hits']if h['profile_id']=='sf_profile_050_base')
        self.assertEqual(target['match_basis'],'embedding')
        self.assertTrue(target['optional_eligible']);self.assertFalse(target['hard_eligible'])
    def test_mirror_topology_preserves_request_age_count_gender_and_occlusion(self):
        profile=next(p for p in self.registry['profiles']if p['id']=='mirror_selfie_reflection_device_topology')
        self.assertFalse(profile['activation']['requires_adult_character'])
        self.assertNotIn('one clearly adult',json.dumps(profile))
        self.assertIn('preserving declared actor count',next(g for g in profile['render_gates']if g['id']=='vo_social_mirror_subject_and_phone_inside')['description'])
        self.assertIn(profile['id'],self.matches('거울 셀카'))
    def test_source_registration_and_maintenance_record_are_bound(self):
        inventory=generator.photo_source_manifest.SourceInventory.load(ASSETS)
        self.assertIn('photo_prompt_selfie_pose_extension.json',inventory.files('candidate'))
        self.assertIn('photo_prompt_visual_obligations_selfie_pose.json',inventory.files('visual_profile'))
        self.assertEqual(self.extension['maintenance_ref']['sha256'],digest(json.loads((EVIDENCE/'maintenance-record.json').read_text())))

if __name__=='__main__':unittest.main()
