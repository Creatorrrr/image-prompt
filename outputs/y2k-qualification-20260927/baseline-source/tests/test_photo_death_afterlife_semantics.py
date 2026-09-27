from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
RECIPES_PATH = SKILL_DIR / "assets" / "concept_recipes.json"
EVIDENCE_PATH = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "necromancer_dead_causality",
    "human_ghost_identity_breach",
    "korean_afterlife_guide_escort",
    "western_death_personification",
    "fictional_human_remains_inert_dignity",
}


class PhotoDeathAfterlifeSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.recipes = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.candidates = {
            slot: {row["id"]: row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }

    def hard_matches(self, text: str) -> set[str]:
        rows = [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            },
            {
                "source": "authorial_core_interpreted_intent",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            },
        ]
        return set(
            prompt_generator.candidate_pack_auto_visual_obligation_matches(
                self.registry,
                rows,
            )
        )

    def test_profiles_encode_relations_and_render_gates(self):
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(
                    profile["activation"]["semantic_discovery_requires_component_evidence"],
                    True,
                )
                self.assertGreaterEqual(len(components["required_group_ids"]), 3)
                self.assertGreaterEqual(components["minimum_component_groups"], 3)
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 4)
                self.assertGreaterEqual(len(profile["render_gates"]), 5)
                self.assertTrue(profile["reject_substitutes"])

    def test_exact_visual_terms_route_to_distinct_profiles(self):
        cases = {
            "네크로맨서 캐릭터가 특정 망자의 유품에 질문하고 현현의 응답을 받는 사진": {
                "necromancer_dead_causality"
            },
            "생전 초상과 같은 유령 인물이 거울에만 나타나는 사진": {
                "human_ghost_identity_breach"
            },
            "한국 저승사자가 한 망자를 문턱 너머로 인도하는 사진": {
                "korean_afterlife_guide_escort"
            },
            "grim reaper mortality action extinguishes a terminal clock in a fictional photograph": {
                "western_death_personification"
            },
            "허구의 시신이 시신보 아래 운반대에 완전히 지지되는 영안실 기록 사진": {
                "fictional_human_remains_inert_dignity"
            },
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), expected)

    def test_adjacent_concepts_fail_closed(self):
        cases = (
            "A dark-robed wizard holds a skull under green light",
            "A spirit medium listens passively to a voice",
            "A long-exposure dancer looks translucent through motion blur",
            "A holographic data ghost appears in a server dashboard",
            "A solitary fashion model wears black clothing and a gat",
            "A vanitas still life contains a skull and hourglass without an agent",
            "A pale person sleeps with closed eyes",
            "A standing zombie walks under its own power",
            "동물 사체를 기록하는 야생동물 조사 사진",
            "죽음이라는 추상 주제를 다룬 사진",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_korean_afterlife_guide_and_western_death_do_not_merge(self):
        guide = self.hard_matches(
            "저승사자가 망자와 함께 걸으며 저승 문턱을 열어 인도하는 사진"
        )
        western_death = self.hard_matches(
            "An embodied Western personification of Death performs a mortality action"
        )
        self.assertEqual(guide, {"korean_afterlife_guide_escort"})
        self.assertEqual(western_death, {"western_death_personification"})
        self.assertNotIn("western_death_personification", guide)
        self.assertNotIn("korean_afterlife_guide_escort", western_death)

    def test_candidate_pack_spans_subject_action_mechanism_trace_and_review(self):
        expected_by_slot = {
            "subject": {
                "necromancer_practitioner_role_model",
                "specific_human_ghost_former_identity",
                "korean_afterlife_guide_role_model",
                "western_death_personification_agent",
                "shrouded_fictional_human_remains",
                "korean_wongwi_unresolved_return",
                "mortality_symbol_still_life",
            },
            "action": {
                "questioning_named_dead_apparition",
                "commanding_single_reanimated_body",
                "releasing_bound_dead_presence",
                "appearing_only_in_reflection",
                "repeating_former_life_action",
                "guiding_deceased_across_threshold",
                "turning_final_hourglass_mortality_action",
                "dignified_two_person_remains_transfer",
                "seeking_former_identity_recognition",
            },
            "surreal_physics_detail": {
                "apparition_tethered_to_memorial_anchor",
                "reflection_presence_mismatch",
                "inert_to_commanded_transition",
                "threshold_footprint_transformation",
                "mortality_clock_extinguishing",
            },
            "aftermath_trace": {
                "shifted_instrument_response_trace",
                "depressed_key_dust_trace",
                "transformed_footprint_threshold_trace",
                "localized_extinguished_flame_trace",
                "bereavement_absence_trace",
            },
            "capture_context": {
                "causal_chain_four_part_capture",
                "reflection_only_apparition_wide_capture",
                "respectful_forensic_documentation_distance",
            },
            "safety_profile": {
                "non_instructional_necromancy_fiction",
                "culture_bounded_afterlife_original_mechanism",
                "human_remains_dignity_high_sensitivity",
            },
        }
        for slot, expected_ids in expected_by_slot.items():
            with self.subTest(slot=slot):
                self.assertTrue(expected_ids <= set(self.candidates[slot]))

    def test_recipe_defaults_preserve_semantic_boundaries(self):
        aliases = self.recipes["aliases"]
        mixins = self.recipes["mixins"]
        self.assertEqual(aliases["저승사자"], "한국 저승사자")
        self.assertEqual(aliases["necromancer"], "네크로맨서")
        self.assertEqual(aliases["human ghost"], "유령")
        self.assertEqual(aliases["human corpse"], "시신")
        self.assertNotIn("사체", aliases)
        self.assertNotIn("death", aliases)
        self.assertNotIn("죽음", aliases)
        self.assertEqual(
            mixins["원귀"]["set"]["subject"],
            "korean_wongwi_unresolved_return",
        )
        self.assertEqual(
            mixins["사신"]["set"]["action"],
            "turning_final_hourglass_mortality_action",
        )
        self.assertEqual(
            mixins["한국 저승사자"]["set"]["action"],
            "guiding_deceased_across_threshold",
        )

    def test_research_evidence_is_approved_and_candidate_bound(self):
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        evidence_rows = [
            row for row in rows if row["id"].startswith("death_semantics_")
        ]
        self.assertEqual(len(evidence_rows), 9)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in evidence_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertEqual(row["domain"], "death_and_afterlife_visual_semantics")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])


if __name__ == "__main__":
    unittest.main()
