"""Observable alternatives preserve owner, axis, scope and optionality."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as candidate_semantics
import photo_contracts as contracts
from tests import photo_prompt_fixtures as fixtures


class PhotoNeutralExpressionAlternativesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assets=SKILL/'assets'
        cls.registry=pg.load_visual_obligation_registry(assets/'photo_prompt_visual_obligations.json')
        cls.profiles={p['id']:p for p in cls.registry['profiles']}
        cls.index=pg.load_visual_profile_index(assets/'photo_prompt_visual_profile_index.json',cls.registry)
        cls.data=pg.load_json(assets/'photo_prompt_tags.json')
        cls.entries={e['id']:(s,e) for s,rows in cls.data['slots'].items() for e in rows}
        cls.original_entries={}
        for file in ('photo_prompt_tags.json',*pg.RESEARCH_EXTENSION_FILENAMES):
            raw=json.loads((assets/file).read_text())
            cls.original_entries.update({e['id']:e for rows in raw.get('slots',{}).values() for e in rows})

    def resolve(self,text,*,adult=True,source='user_requirement',polarity='required'):
        return pg.resolve_visual_profile_hits(self.registry,[{'source':source,'text':text,'polarity':polarity}],visual_profile_index=self.index,query_text=text,adult_context=adult)

    @staticmethod
    def hard(resolution):
        return {x['profile_id'] for x in resolution['hits'] if x['hard_eligible']}

    def test_narrow_current_expression_needs_a_face_and_is_not_static_lip_volume(self):
        self.assertIn('ne_current_lip_protrusion',self.hard(self.resolve('adult portrait with a current forward lip pout')))
        for text in ('a ceramic vessel has a current forward lip pout','adult portrait with thick upper and lower lips','an adult has naturally full lips','a plump cherry beside a smooth porcelain bowl'):
            with self.subTest(text=text):self.assertNotIn('ne_current_lip_protrusion',self.hard(self.resolve(text)))
        self.assertNotIn('bm_lip_volume',self.hard(self.resolve('adult portrait with a current forward lip pout')))

    def test_regional_volume_does_not_force_a_whole_body_build_or_curve(self):
        hard=self.hard(self.resolve('adult regional rounded soft volume in the upper arm'))
        self.assertIn('ne_regional_soft_volume',hard)
        self.assertTrue({'soft_full_figure_volume','curvilinear_figure_relation','bust_prominence_relation'}.isdisjoint(hard))
        self.assertFalse(self.hard(self.resolve('adult regional rounded soft volume',adult=False)))

    def test_exact_negation_and_advisory_source_do_not_create_requester_duties(self):
        for term in ('adult regional rounded soft volume','adult regional convex-concave contour transition','current forward lip pout'):
            with self.subTest(term=term):
                self.assertFalse(self.hard(self.resolve('an adult face with '+term,polarity='excluded')))
                self.assertFalse(self.hard(self.resolve('an adult face without '+term)))
                self.assertFalse(self.hard(self.resolve('an adult face with '+term,source='authorial_core_interpretation',polarity='advisory')))

    def test_complete_region_and_owner_proof_cannot_be_replaced_by_one_component(self):
        for profile_id in ('ne_regional_soft_volume','ne_regional_contour_transition','ne_current_lip_protrusion'):
            p=self.profiles[profile_id]; components=p['semantics']['visual_components']
            self.assertIsNotNone(pg.candidate_pack_visual_component_match(p,'; '.join(components)))
            for i in range(len(components)):
                self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(t for j,t in enumerate(components) if j!=i)))

    def test_component_alternatives_keep_anatomical_boundaries_and_common_owner(self):
        p=self.profiles['bm_eye_aperture']
        valid=['upper eye-opening border','lower eye-opening border','medial and lateral eye corners','the same adult subject and named body region']
        self.assertIsNotNone(pg.candidate_pack_visual_component_match(p,'; '.join(valid)))
        for index,wrong in ((1,'horizontal eye-opening width'),(2,'vertical eye-opening height'),(3,'a ceramic object')):
            altered=valid[:];altered[index]=wrong
            self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(altered)))
        skin=self.profiles['bm_skin_relief_texture']
        proof=['distribution of visible pores','low skin microrelief','specular finish is separately readable','the same adult subject and named body region']
        self.assertIsNotNone(pg.candidate_pack_visual_component_match(skin,'; '.join(proof)))
        self.assertIsNone(pg.candidate_pack_visual_component_match(skin,'; '.join(['a smooth cheek surface',*proof[1:]])))

    def test_broad_labels_and_material_polysemy_are_not_promoted_to_exact(self):
        for text in ('adult plump upper arm','adult sinewy forearm','adult willowy figure','adult face with pouty lips','supple leather with smooth folds','smooth porcelain with a plump fruit','a slender serif typeface','a curvaceous glass vase'):
            with self.subTest(text=text):self.assertFalse(self.hard(self.resolve(text)))

    def test_bm25f_paraphrases_remain_advisory(self):
        for profile_id,text in (
            ('bm_long_limb_build','elongated slender arms and legs compared with the same adult torso reference'),
            ('bm_wiry_definition','a sinewy adult build with narrow torso and limbs plus localized muscle planes and tendon contours'),
            ('bm_lip_volume','the thickness of both lip surfaces and their perimeter remain separately readable'),
        ):
            # A nearby adjective is not complete relational proof. Supply an
            # independently declared complete component context, then rank the
            # alternative language; neither lane may harden it.
            self.assertNotIn(profile_id,self.hard(self.resolve(text,source='authorial_core_interpretation',polarity='advisory')))
            groups=self.profiles[profile_id]['semantics']['component_semantics']['groups']
            proof='; '.join(g['any_terms'][0] for g in groups)
            r=pg.resolve_visual_profile_hits(self.registry,[{'source':'authorial_core_interpretation','text':text+'; '+proof,'polarity':'advisory'}],visual_profile_index=self.index,query_fields={'active_request':text},query_text=text,adult_context=True)
            hit=next(x for x in r['hits'] if x['profile_id']==profile_id)
            self.assertFalse(hit['hard_eligible'])
            self.assertIn(hit['match_basis'],('bm25f','embedding','bm25f+embedding'))

    def test_regional_candidates_cannot_evade_partial_body_property_locks(self):
        for candidate_id in ('ne_regional_soft_volume','ne_regional_contour_transition'):
            slot,entry=self.entries[candidate_id]
            semantic=candidate_semantics.semantic_source(entry,slot,self.data['candidate_semantic_policy'])
            lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'body_geometry','target':'main_subject','property':'body.lips.vermilion_contour_relation'}]}
            self.assertFalse(contracts.property_effects_allowed(lock,semantic['affected_dimensions'],semantic['affected_properties']))

    def test_structure_and_action_have_independent_carriers(self):
        for entry_id,expected in (('bm_lip_volume',{'body_geometry'}),('ae_pucker',{'expression'}),('pv_side_eye',{'expression'})):
            slot,entry=self.entries[entry_id]
            semantic=candidate_semantics.semantic_source(entry,slot,self.data['candidate_semantic_policy'])
            self.assertEqual(set(semantic['affected_dimensions']),expected)

    def test_interpretation_limits_do_not_pollute_positive_retrieval(self):
        for entry_id,blocked in (('pv_side_eye','scorn, desire or personality'),('ae_pucker','sulking or invitation'),('bm_skin_relief_texture','rebound or temporal elasticity')):
            slot,entry=self.entries[entry_id]
            fields=pg.semantic_bm25f_fields_for_entry(entry,slot,kind='slot')
            self.assertNotIn(blocked,str(fields))
            self.assertNotIn('contextual_usage',fields)

    def test_equivalent_extension_preserves_existing_labels_effects_and_guards(self):
        extension=pg.load_json(SKILL/'assets/photo_prompt_neutral_expression_extension.json')
        for slot,changes in extension['existing_slot_context_extensions'].items():
            for entry_id in changes:
                _,entry=self.entries[entry_id]
                stripped={k:v for k,v in entry.items() if k not in ('paraphrases','contextual_usage')}
                original=self.original_entries.get(entry_id)
                self.assertIsNotNone(original,entry_id)
                self.assertEqual(stripped,{k:v for k,v in original.items() if k not in ('paraphrases','contextual_usage')})

    def test_moral_corruption_does_not_request_bodily_transformation_through_full_core(self):
        source='이익 때문에 원칙을 포기한 성인 인물의 타락을 봉투를 받고 약속 문서를 접는 현재 선택으로 보여줘.'
        baseline='An adult office worker accepts a sealed envelope and folds a written promise on the desk. The current choice trades a stated principle for personal gain. The same person touches the envelope while the written promise remains readable beside it. A rainlit office contains a wooden desk and an ordinary lamp. The photograph keeps the adult face, the envelope and the folded commitment together in one coherent medium view.'
        core=fixtures.core(source,interpreted_intent=baseline,subject='one adult office worker',setting='a rainlit office with wooden furniture',event='accepts a sealed envelope and folds a written promise',baseline_prompt_en=baseline,visual_priorities=('adult office worker','written promise remains readable','rainlit office'),open_dimensions=('body_geometry','appearance','expression','pose','action','setting','framing','composition','lighting','camera'))
        pack=fixtures.run_current(core)
        self.assertNotIn('embodied_corruption_transition',[x['id'] for x in pack.get('visual_obligations',{}).get('obligations',[])])


if __name__=='__main__':unittest.main()
