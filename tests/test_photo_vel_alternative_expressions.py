"""Precision and ownership regression tests for descriptive alternatives."""
from pathlib import Path
import json
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ASSETS.parent/'scripts'))
import prompt_generator as pg
from bm25f_retrieval import rank_bm25f

class VelAlternativeExpressionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
        cls.index=pg.load_visual_profile_index(ASSETS/'photo_prompt_visual_profile_index.json',cls.registry)
        cls.profiles={p['id']:p for p in cls.registry['profiles']}
        cls.data=pg.load_json(ASSETS/'photo_prompt_tags.json')
        cls.extension=json.loads((ASSETS/'photo_prompt_vel_appearance_relations_extension.json').read_text())
        cls.new=[p for p in cls.registry['profiles'] if p['id'].startswith('vel_')]

    def test_alternatives_are_searchable_without_becoming_exact_hard_aliases(self):
        for profile in self.new:
            exact={r['term'] for r in self.index['exact_lookup'] if r['profile_id']==profile['id']}
            for phrase in profile['semantics']['paraphrase_examples']:
                with self.subTest(profile=profile['id'],phrase=phrase):
                    self.assertIn(phrase,self.index['entries'][profile['id']]['text'])
                    self.assertNotIn(phrase,exact)
                    resolved=pg.resolve_visual_profile_hits(self.registry,[{'source':'user_requirement','polarity':'required','text':phrase}],visual_profile_index=self.index,adult_context=True)
                    self.assertFalse(any(h['profile_id']==profile['id'] and h['hard_eligible'] for h in resolved['hits']))

    def test_bilingual_component_descriptions_retrieve_the_same_optional_relation(self):
        for profile in self.new:
            for language in (1,2):
                phrase='; '.join(c['match_terms'][language] for c in profile['authored_components']['components'])
                hits=rank_bm25f(self.index['bm25f'],{'request':phrase})
                with self.subTest(profile=profile['id'],language=language):
                    self.assertIn(profile['id'],[h['document_id'] for h in hits[:12]])

    def test_partial_labels_do_not_require_added_layers_contact_or_actors(self):
        for phrase in ['초커','a towel','wet fabric','거울','한쪽 어깨','red light','손짓','soft bedding','유리']:
            with self.subTest(phrase=phrase):
                resolved=pg.resolve_visual_profile_hits(self.registry,[{'source':'user_requirement','text':phrase,'polarity':'required'}],visual_profile_index=self.index,adult_context=True)
                self.assertFalse(any(h['profile_id'].startswith('vel_') and h['hard_eligible'] for h in resolved['hits']))

    def test_confounds_and_research_limits_never_enter_positive_semantic_documents(self):
        for profile in self.new:
            text=pg.visual_profile_semantic_text(profile)
            for excluded in profile['semantics']['contrast_examples']+profile['semantics']['claim_limits']:
                with self.subTest(profile=profile['id'],excluded=excluded):
                    self.assertNotIn(excluded,text)

    def test_existing_candidate_extensions_preserve_relational_owner_and_surface(self):
        expected={('wardrobe_style','y2kr_rib_tank'):'sleeveless',('surface_material','y2kr_satin'):'cloth',('garment_detail','water_w159'):'wraps',('wearable_accessory','unif_lapel_chain_separate_inner_neck'):'maroon',('prop','real_holstered_service_pistol'):'holster'}
        for (slot,eid),owner in expected.items():
            row=next(r for r in self.data['slots'][slot] if r['id']==eid)
            variants=self.extension['existing_slot_context_extensions'][slot][eid]['paraphrases']
            self.assertTrue(any(owner in p.casefold() for p in variants))
            self.assertTrue(all(p in row['paraphrases'] for p in variants))

    def test_crossed_owner_holdouts_remain_separate(self):
        pairs=[('y2kr_rib_tank','vg_faille_crossgrain_ribs_profile'),('pfe_one_shoulder','vel_slipped_attached_shoulder_strap_profile'),('rb_glass_reflection_transmission','vel_mirror_surface_condensation_face_profile'),('vel_soft_contact_glass_patch_profile','vel_hand_face_visible_clearance_profile')]
        for a,b in pairs:
            one=self.profiles[a];other=self.profiles[b]
            self.assertTrue(set(one['semantics']['paraphrase_examples']).isdisjoint(other['semantics']['paraphrase_examples']))
            self.assertNotEqual(one['activation']['exact_terms'],other['activation']['exact_terms'])

    def test_same_towel_contact_and_support_are_complete_directed_relations(self):
        rows={r['id']:r for values in self.extension['slots'].values() for r in values}
        towel=rows['vel_held_towel_continuous_front']
        grips=[r for r in towel['relations'] if r['type']=='grips']
        self.assertEqual({r['subject'] for r in grips},{'left_hand','right_hand'})
        self.assertEqual({r['object'] for r in grips},{'same_towel_upper_edge'})
        self.assertIn('pose',towel['affected_dimensions'])
        self.assertIn('appearance',towel['affected_dimensions'])
        shoe=rows['vel_shoe_chest_contact_separate_support']
        self.assertEqual({(r['subject'],r['object']) for r in shoe['relations']},{('contact_shoe','other_actor_chest_garment'),('opposite_foot','floor')})
        self.assertIn('relationship',shoe['affected_dimensions'])

    def test_no_blood_limit_keeps_red_emission_positive_and_separately_owned(self):
        profile=self.profiles['vel_airborne_red_code_metal_receiver_profile']
        text=pg.visual_profile_semantic_text(profile)
        self.assertIn('red luminous',text)
        self.assertIn('metal',text)
        self.assertNotIn('bloodstain',text)
        self.assertTrue(all('no blood' not in x.casefold() for x in profile['activation']['exact_terms']))

if __name__=='__main__':unittest.main()
