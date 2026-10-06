"""Horror proposals require complete owner relations without broad hard authority."""
from __future__ import annotations
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as semantics
from photo_contracts import property_effects_allowed

class PhotoHorrorVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
        full = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']:p for p in full['profiles'] if p['id'].startswith('hvr_profile_')}
        cls.registry = {**full,'profiles':list(cls.profiles.values())}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)
        cls.entries = {e['id']:(s,e) for s,rows in cls.data['slots'].items() for e in rows if e['id'].startswith('hr_')}

    def hard(self, text, source='user_requirement', polarity='required'):
        hits = pg.resolve_visual_profile_hits(self.registry,[{'text':text,'source':source,'polarity':polarity}],visual_profile_index=self.index,adult_context=True)
        return {h['profile_id'] for h in hits['hits'] if h['hard_eligible']}

    def test_complete_request_proposition_is_the_only_new_hard_authority(self):
        for pid,p in self.profiles.items():
            term = p['activation']['exact_terms'][0]
            with self.subTest(profile=pid):
                self.assertIn(pid,self.hard(term))
                self.assertNotIn(pid,self.hard(term,polarity='excluded'))
                self.assertNotIn(pid,self.hard(term,source='authorial_core_interpretation',polarity='advisory'))
        for text in ['호러','공포','uncanny','folk horror','body horror','거울','귀신','미소','metal','smiling portrait','calm visitor beside a crowd','a metal bracelet worn on skin']:
            with self.subTest(control=text):
                self.assertFalse(self.hard(text))

    def test_missing_comparison_component_cannot_qualify_optional_discovery(self):
        for pid,p in self.profiles.items():
            parts = p['semantics']['visual_components']
            with self.subTest(profile=pid,complete=True):
                self.assertEqual(pg.candidate_pack_visual_component_match(p,'; '.join(parts)),'component_semantics')
            for omitted in range(len(parts)):
                with self.subTest(profile=pid,omitted=omitted):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(t for i,t in enumerate(parts) if i!=omitted)))

    def test_opt_in_preserves_all_evidence_and_native_gates(self):
        for pid,p in self.profiles.items():
            obligation = pg.candidate_pack_visual_profile_obligation(p,self.registry,activation_source='authorial_opt_in',source_intent_ids=[])
            with self.subTest(profile=pid):
                n = len(p['semantics']['visual_components'])
                self.assertEqual(len(obligation['prompt_binding']['required_evidence_fields']),n)
                self.assertEqual(len(obligation['render_gates']),n)
                self.assertEqual({g['review_scale'] for g in obligation['render_gates']},{'native'})
                self.assertEqual(set(obligation['evidence_requirements']),set(obligation['prompt_binding']['required_evidence_fields']))

    def test_wrong_owner_substitutes_do_not_qualify_three_test_mechanisms(self):
        cases = {
            'reflection_pose_disagreement':'two different women wear matching clothes; both mouths smile; the mirror frame tilts',
            'folk_horror_collective_boundary':'a visitor mingles inside a friendly crowd; several open roads cross a bright meadow',
            'bodily_fusion_shared_junction':'a metal cuff lies on skin; an unattached cable crosses behind the elbow',
        }
        for slug,text in cases.items():
            with self.subTest(slug=slug):
                self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['hvr_profile_'+slug],text))

    def test_general_alternative_components_propose_full_meaning_without_hard_authority(self):
        variants = {
            'folk_horror_collective_boundary':'community enclosure; visitor outside the gathering; single escape route',
            'bodily_fusion_shared_junction':'skin meets metal; unbroken tissue-metal continuity',
            'shadow_independent_pose':'actual hands lowered; cast shadow lifts an arm; single light source',
            'reflection_pose_disagreement':'matching reflected wardrobe; real mouth stays neutral; only reflection smiles',
        }
        for slug,text in variants.items():
            p = self.profiles['hvr_profile_'+slug]
            with self.subTest(slug=slug):
                self.assertEqual(pg.candidate_pack_visual_component_match(p,text),'component_semantics')
                self.assertNotIn(p['id'],self.hard(text,source='authorial_core_interpretation',polarity='advisory'))
                for omitted in range(len(text.split('; '))):
                    partial='; '.join(t for i,t in enumerate(text.split('; ')) if i!=omitted)
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p,partial))

    def test_secondary_carriers_do_not_claim_primary_subject_mutation(self):
        for cid in ['hr_folk_horror_collective_boundary','hr_bodily_fusion_shared_junction','hr_recording_local_discrepancy']:
            _,entry = self.entries[cid]
            with self.subTest(candidate=cid):
                self.assertNotIn('subject',entry['affected_dimensions'])
                self.assertTrue(set(entry['affected_dimensions']) <= pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS-{'subject','concept','event','reference_use'})
        self.assertIn('count',self.entries['hr_folk_horror_collective_boundary'][1]['affected_dimensions'])
        self.assertIn('body_geometry',self.entries['hr_bodily_fusion_shared_junction'][1]['affected_dimensions'])

    def test_parent_effect_scope_protects_children_across_comparison_owners(self):
        for cid,dimension,target,prop in [
            ('hr_reflection_pose_disagreement','expression','main_subject','mouth.corners'),
            ('hr_folk_horror_collective_boundary','setting','orchard','spatial_structure.exit'),
            ('hr_bodily_fusion_shared_junction','body_geometry','main_subject','anatomy.forearm'),
            ('hr_palette_daylight_ritual','color','flowers','palette.white'),
        ]:
            slot,e = self.entries[cid]
            source = semantics.semantic_source(e,slot,self.data['candidate_semantic_policy'])
            lock = {'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':dimension,'target':target,'property':prop}]}
            with self.subTest(candidate=cid):
                self.assertFalse(property_effects_allowed(lock,source['affected_dimensions'],source['affected_properties']))

    def test_profile_association_does_not_force_reflection_only_neighbor(self):
        mirror = next(b for b in self.data['candidate_bundles'] if b['id']=='hvb_07_mirror_pose_disagreement')
        self.assertEqual(mirror['adoption'],'optional')
        self.assertEqual(mirror['profile_activation'],'independent_request_evidence_only')
        self.assertEqual({m['entry_id'] for m in mirror['member_candidates']},{'hr_reflection_pose_disagreement'})
        self.assertNotIn('appearing_only_in_reflection',str(mirror))
        self.assertFalse(self.hard('hvb_07_mirror_pose_disagreement'))

    def test_audio_time_and_unqualified_cultural_variants_are_not_visual_duties(self):
        for cid in ['hr_water_ghost_variant','hr_jangsanbeom_modern_variant','hr_virgin_ghost_media_variant','hr_yurei_named_variant','hr_ghoul_grave_relation','hr_penanggalan_variant']:
            self.assertNotIn(cid,self.entries)
        self.assertNotIn('hvb_10_water_ghost_variant',{b['id'] for b in self.data['candidate_bundles']})
        self.assertFalse(self.hard('a sudden jump scare sound followed by a recurring breathing rhythm'))

    def test_provenance_and_failure_boundaries_do_not_pollute_positive_retrieval(self):
        for pid,p in self.profiles.items():
            text = pg.visual_profile_semantic_text(p)
            with self.subTest(profile=pid):
                for unwanted in ['research-evidence','RESEARCH_DRAFT_NOT_ADOPTED','universal cultural appearance','chemical identity','source_refs']:
                    self.assertNotIn(unwanted,text)
        for cid,(slot,e) in self.entries.items():
            fields = pg.semantic_bm25f_fields_for_entry(e,slot,kind='slot')
            self.assertNotIn('contextual_usage',fields)

if __name__ == '__main__':
    unittest.main()
