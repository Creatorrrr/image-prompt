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
RESEARCH_EVIDENCE_PATH = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
)
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
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.all_candidate_ids = {
            candidate_id for rows in cls.by_slot.values() for candidate_id in rows
        }



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


    def test_semantic_index_ranks_new_keyword_families_in_owned_slots(self) -> None:
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
                owning_slots = {entry_id.split(":")[1] for entry_id in expected_ids}
                ranked = rank_bm25f(
                    bm25f,
                    {"active_request": query},
                    limit=12,
                    allowed_ids=[entry_id for entry_id in index["entries"]
                                 if entry_id.startswith("slot:")
                                 and entry_id.split(":")[1] in owning_slots],
                )
                top_ids = {row["document_id"] for row in ranked[:limit]}
                self.assertLessEqual(expected_ids, top_ids)


if __name__ == "__main__":
    unittest.main()
