from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
RECIPES_PATH = SKILL_DIR / "assets" / "concept_recipes.json"
RESEARCH_EVIDENCE_PATH = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
)
WRAPPER_PATH = SCRIPT_DIR / "generate_photo_prompt.py"
SEMANTIC_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_semantic_index.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generate_photo_prompt  # noqa: E402
import prompt_generator  # noqa: E402
from bm25f_retrieval import rank_bm25f  # noqa: E402


WITCH_CANDIDATES = {
    "witch_practitioner_role_model",
    "broom_flight_across_moon",
    "working_broom_prop",
    "moonlit_rooftop_airspace",
}
TREASURE_CANDIDATES = {
    "treasure_hunter_role_model",
    "triangulating_ruin_clues",
    "annotated_treasure_map_prop",
    "search_before_discovery",
    "disturbed_dust_clue_trace",
    "revealing_sealed_cache_edge",
    "partially_revealed_sealed_cache_prop",
    "partial_reveal_moment",
    "documenting_find_in_place",
    "sealed_discovery_case_prop",
    "post_discovery_verification",
    "documented_find_marker_trace",
    "reviewing_wreck_anomaly",
    "sonar_anomaly_tablet_prop",
    "wreck_survey_documentation_capture",
    "logging_geocache_find",
    "geocache_log_container_prop",
    "collapsed_ruin_clue_chamber",
    "cliff_overlook_after_discovery",
    "coastal_wreck_survey_deck",
    "forest_geocache_search_site",
}
LOCAL_REPUTATION_CANDIDATES = {
    "multi_observer_recognition_cue",
    "press_lens_attention_cluster",
    "crowd_path_opening_for_subject",
    "local_press_recognition_capture",
    "local_reputation_beauty_context",
    "community_honor_arrival",
    "playful_hyperbole_public_entrance",
    "local_reputation_arrival",
    "self_aware_superlative_entrance",
}
NEW_EVIDENCE_IDS = {
    "witch_british_museum_print_iconography",
    "witch_wellcome_appearance_spectrum",
    "witch_museum_symbols_practice_boundary",
    "treasure_kotobank_hidden_target_definition",
    "treasure_noaa_detection_visual_survey_sequence",
    "treasure_nps_context_provenience",
    "treasure_unesco_in_situ_noncommercial_boundary",
    "treasure_geocaching_coordinates_log_return",
    "local_beauty_kotobank_komachi_reputation",
    "local_beauty_goo_superlative_intensifier",
    "local_beauty_plos_observer_variability",
    "local_beauty_kotobank_bishoujo_age_ambiguity",
}


class PhotoConceptCandidateExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.merged_tags = prompt_generator.load_json(TAGS_PATH)
        cls.recipes = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.all_candidate_ids = {
            candidate_id for rows in cls.by_slot.values() for candidate_id in rows
        }

    def explain(self, concept: str, seed: int = 42) -> dict[str, Any]:
        _args, explanations = generate_photo_prompt.resolve_concepts(
            ["--seed", str(seed), "--selection-mode", "rule", "--emit-candidate-pack"],
            [concept],
        )
        self.assertEqual(len(explanations), 1)
        return explanations[0]

    def candidate_pack(self, concept: str, seed: int) -> dict[str, Any]:
        completed = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--concept",
                concept,
                "--selection-mode",
                "rule",
                "--seed",
                str(seed),
                "--emit-candidate-pack",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr[-1000:])
        payload = json.loads(completed.stdout)
        self.assertEqual(len(payload), 1)
        return payload[0]

    def test_new_candidate_ids_exist_in_the_expected_slots(self) -> None:
        for candidate_id in WITCH_CANDIDATES | TREASURE_CANDIDATES | LOCAL_REPUTATION_CANDIDATES:
            with self.subTest(candidate_id=candidate_id):
                self.assertIn(candidate_id, self.all_candidate_ids)

        expected_slot_ids = {
            "subject": {"witch_practitioner_role_model", "treasure_hunter_role_model"},
            "action": {
                "broom_flight_across_moon",
                "triangulating_ruin_clues",
                "revealing_sealed_cache_edge",
                "documenting_find_in_place",
                "reviewing_wreck_anomaly",
                "logging_geocache_find",
            },
            "prop": {
                "working_broom_prop",
                "annotated_treasure_map_prop",
                "partially_revealed_sealed_cache_prop",
                "sealed_discovery_case_prop",
                "sonar_anomaly_tablet_prop",
                "geocache_log_container_prop",
            },
            "location": {
                "moonlit_rooftop_airspace",
                "collapsed_ruin_clue_chamber",
                "cliff_overlook_after_discovery",
                "coastal_wreck_survey_deck",
                "forest_geocache_search_site",
            },
            "capture_context": {
                "wreck_survey_documentation_capture",
                "local_press_recognition_capture",
            },
            "narrative_phase": {
                "search_before_discovery",
                "partial_reveal_moment",
                "post_discovery_verification",
                "local_reputation_arrival",
                "self_aware_superlative_entrance",
            },
            "social_cue": {
                "multi_observer_recognition_cue",
                "press_lens_attention_cluster",
                "crowd_path_opening_for_subject",
            },
            "aftermath_trace": {
                "disturbed_dust_clue_trace",
                "documented_find_marker_trace",
            },
            "situation_context": {
                "local_reputation_beauty_context",
                "community_honor_arrival",
                "playful_hyperbole_public_entrance",
            },
        }
        for slot, candidate_ids in expected_slot_ids.items():
            with self.subTest(slot=slot):
                self.assertLessEqual(candidate_ids, set(self.by_slot[slot]))

    def test_role_recipes_keep_identity_core_disjoint_from_rotating_scenes(self) -> None:
        expected = {
            "마녀": "witch_practitioner_role_model",
            "트레저헌터": "treasure_hunter_role_model",
        }
        for role, subject_id in expected.items():
            with self.subTest(role=role):
                recipe = self.recipes["roles"][role]
                self.assertEqual(recipe["identity_core"], {"subject": subject_id})
                self.assertEqual(len(recipe["scene_variants"]), 5)
                self.assertTrue(all("subject" not in row["set"] for row in recipe["scene_variants"]))
                self.assertGreaterEqual(recipe["soft_min_anchors"], 3)

                expected_variant_ids = {row["id"] for row in recipe["scene_variants"]}
                selected_variant_ids = {
                    generate_photo_prompt.select_recipe_scene_variant(
                        role,
                        recipe,
                        ["--seed", str(seed)],
                    )["id"]
                    for seed in range(256)
                }
                self.assertEqual(selected_variant_ids, expected_variant_ids)

    def test_aliases_are_narrow_and_adjacent_concepts_remain_distinct(self) -> None:
        aliases = self.recipes["aliases"]
        for alias in ("witch", "Witch", "魔女"):
            self.assertEqual(aliases[alias], "마녀")
        for alias in (
            "트레저 헌터",
            "보물 사냥꾼",
            "treasure hunter",
            "treasure-hunter",
            "トレジャーハンター",
        ):
            self.assertEqual(aliases[alias], "트레저헌터")
        for alias in (
            "도내 1등 초절정 미소녀",
            "도내 최상위 랭크 미소녀",
            "県内一の美少女",
            "local legendary beauty",
        ):
            self.assertEqual(aliases[alias], "지역 최상위 미모 평판")

        self.assertNotIn("미소녀", aliases)
        self.assertNotIn("미녀", aliases)
        self.assertNotIn("beauty", aliases)

        for confounder in ("탐험가", "고고학자", "도굴꾼", "약초상", "미소녀"):
            with self.subTest(confounder=confounder):
                explanation = self.explain(confounder)
                self.assertNotIn(explanation.get("role"), {"마녀", "트레저헌터"})
                self.assertNotIn("지역 최상위 미모 평판", explanation.get("applied_mixins", []))
        self.assertEqual(self.explain("마술사")["role"], "마술사")

    def test_local_reputation_mixin_never_owns_appearance_or_body_slots(self) -> None:
        mixin = self.recipes["mixins"]["지역 최상위 미모 평판"]
        forbidden = {
            "subject",
            "appearance_type",
            "hair_color",
            "hair_style",
            "eye_color",
            "eye_shape",
            "body_type",
            "body_framing",
            "costume_style",
            "wardrobe_style",
            "person_origin",
        }
        allowed = {
            "social_cue",
            "crowd_density",
            "capture_context",
            "situation_context",
            "narrative_phase",
            "camera_direction",
        }
        for bundle in mixin["bundles"]:
            with self.subTest(bundle=bundle["id"]):
                slots = set(bundle["set"])
                self.assertFalse(slots & forbidden)
                self.assertLessEqual(slots, allowed)
                self.assertGreaterEqual(bundle["soft_min_anchors"], 3)
                self.assertIn("minor-coded styling", bundle["safety_negative_floor"])

    def test_resolution_preserves_roles_and_emits_coherent_anchor_clusters(self) -> None:
        witch = self.explain("마녀", seed=11)
        self.assertEqual(witch["role"], "마녀")
        self.assertEqual(
            witch["combined_forced_slots"]["subject"],
            ["witch_practitioner_role_model"],
        )
        self.assertEqual(len(witch["selected_scene_variants"]), 1)

        treasure = self.explain("treasure hunter", seed=12)
        self.assertEqual(treasure["role"], "트레저헌터")
        self.assertEqual(
            treasure["combined_forced_slots"]["subject"],
            ["treasure_hunter_role_model"],
        )
        self.assertIn("narrative_phase", treasure["combined_forced_slots"])

        combined = self.explain("간호사 마녀", seed=14)
        self.assertEqual(combined["role"], "간호사")
        self.assertEqual(combined["applied_mixins"], ["마녀"])
        self.assertNotIn("costume_style", self.recipes["mixins"]["마녀"]["set"])
        self.assertIn("prop", combined["combined_forced_slots"])
        self.assertIn("surreal_physics_detail", combined["combined_forced_slots"])

        reputation = self.explain("도내 1등 초절정 미소녀", seed=13)
        self.assertIsNone(reputation["role"])
        self.assertEqual(reputation["applied_mixins"], ["지역 최상위 미모 평판"])
        self.assertEqual(len(reputation["selected_bundles"]), 1)
        self.assertEqual(
            set(reputation["combined_forced_slots"]),
            {
                "social_cue",
                "crowd_density",
                "capture_context",
                "situation_context",
                "narrative_phase",
                "camera_direction",
            },
        )
        self.assertEqual(reputation["soft_anchor_spec"]["min_anchors"], 3)
        self.assertEqual(len(reputation["soft_anchor_spec"]["anchors"]), 6)

    def test_research_rows_are_approved_and_reference_real_candidates(self) -> None:
        rows = [
            json.loads(line)
            for line in RESEARCH_EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        selected = {row["id"]: row for row in rows if row["id"] in NEW_EVIDENCE_IDS}
        self.assertEqual(set(selected), NEW_EVIDENCE_IDS)
        for evidence_id, row in selected.items():
            with self.subTest(evidence_id=evidence_id):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["candidate_ids"])
                self.assertLessEqual(set(row["candidate_ids"]), self.all_candidate_ids)
                reuse_note = row["reuse_note"].lower()
                self.assertIn("no ", reuse_note)
                self.assertIn("copied", reuse_note)

    def test_candidate_packs_cover_each_concept_and_surface_new_semantics(self) -> None:
        cases = (
            ("마녀", 11, {"surreal_physics_detail", "aftermath_trace"}),
            ("트레저헌터", 12, {"narrative_phase", "aftermath_trace"}),
            (
                "도내 1등 초절정 미소녀",
                13,
                {
                    "social_cue",
                    "crowd_density",
                    "capture_context",
                    "situation_context",
                    "narrative_phase",
                    "camera_direction",
                },
            ),
            ("간호사 마녀", 14, {"prop", "surreal_physics_detail"}),
        )
        for concept, seed, expected_slots in cases:
            with self.subTest(concept=concept):
                pack = self.candidate_pack(concept, seed)
                self.assertEqual(pack["uncovered_intents"], [])
                self.assertTrue(all(row["status"] == "covered" for row in pack["mandatory_intents"]))
                self.assertLessEqual(expected_slots, set(pack["slots"]))

    def test_semantic_index_ranks_new_keyword_families_near_the_top(self) -> None:
        index = prompt_generator.load_semantic_index_payload(SEMANTIC_INDEX_PATH)
        prompt_generator.validate_semantic_index_metadata(index, self.merged_tags)
        bm25f = prompt_generator.semantic_bm25f_payload_from_index(index)

        cases = (
            (
                "마녀 빗자루 달빛 주문 수행",
                {
                    "slot:prop:working_broom_prop",
                    "slot:subject:witch_practitioner_role_model",
                    "slot:action:broom_flight_across_moon",
                },
                4,
            ),
            (
                "트레저헌터 단서 지도 발견 직전",
                {
                    "slot:narrative_phase:search_before_discovery",
                    "slot:subject:treasure_hunter_role_model",
                    "slot:prop:annotated_treasure_map_prop",
                    "slot:action:triangulating_ruin_clues",
                },
                4,
            ),
            (
                "도내 1등 초절정 미소녀 지역 평판 여러 사람 시선",
                {
                    "slot:situation_context:playful_hyperbole_public_entrance",
                    "slot:situation_context:local_reputation_beauty_context",
                    "slot:narrative_phase:self_aware_superlative_entrance",
                    "slot:social_cue:multi_observer_recognition_cue",
                    "slot:capture_context:local_press_recognition_capture",
                },
                6,
            ),
        )
        for query, expected_ids, limit in cases:
            with self.subTest(query=query):
                ranked = rank_bm25f(
                    bm25f,
                    {"active_request": query},
                    limit=12,
                )
                top_ids = {row["document_id"] for row in ranked[:limit]}
                self.assertLessEqual(expected_ids, top_ids)


if __name__ == "__main__":
    unittest.main()
