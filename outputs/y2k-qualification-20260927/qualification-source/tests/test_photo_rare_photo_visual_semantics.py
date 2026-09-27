from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
VISUAL_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
SEMANTIC_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_semantic_index.json"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "rare_photo_three_arm_pixel_test_cases_v1.jsonl"
)
RESEARCH_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "rare-photo-visual-semantics-20260902"
    / "source-research.md"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "fan_side_public_event_telephoto",
    "camera_display_rephotographed_preview",
    "companion_viewpoint_everyday_candid",
    "production_gap_behind_scenes",
    "physical_print_scan_material_context",
    "early_2000s_compact_digicam_social_repost",
    "contact_sheet_selection_context",
}

CANDIDATE_IDS = {
    "fan_side_public_event_telephoto_capture",
    "camera_lcd_rephotographed_preview_capture",
    "off_camera_companion_everyday_capture",
    "between_takes_production_capture",
    "full_print_edge_scan_capture",
    "early_2000s_digicam_social_repost_capture",
    "contact_sheet_selection_capture",
}


class PhotoRarePhotoVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.visual_index = prompt_generator.load_visual_profile_index(
            VISUAL_INDEX_PATH,
            cls.registry,
            provider=prompt_generator.SEMANTIC_PROVIDER,
            model=prompt_generator.SEMANTIC_MODEL_ID,
            dimensions=prompt_generator.DEFAULT_SEMANTIC_DIMENSIONS,
        )
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.capture_candidates = {
            row["id"]: row for row in cls.tags["slots"]["capture_context"]
        }

    def hard_matches(self, text: str) -> set[str]:
        rows = [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            }
        ]
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            rows,
            visual_profile_index=self.visual_index,
            adult_context=True,
        )
        return {
            hit["profile_id"]
            for hit in resolution["hits"]
            if hit["match_basis"] == "exact" and hit["hard_eligible"] is True
        }

    def test_profiles_are_complete_five_group_pixel_contracts(self) -> None:
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        all_gate_ids = [
            gate["id"]
            for profile in self.registry["profiles"]
            for gate in profile["render_gates"]
        ]
        self.assertEqual(len(all_gate_ids), len(set(all_gate_ids)))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], True)
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(len(components["groups"]), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertEqual(len(profile["reject_substitutes"]), 5)
                self.assertTrue(profile["concept_candidate"]["concept_terms"])

    def test_narrow_exact_terms_route_to_one_profile(self) -> None:
        cases = {
            "팬사인회 관객석 망원 직찍": "fan_side_public_event_telephoto",
            "카메라 액정 프리뷰 사진": "camera_display_rephotographed_preview",
            "동행자가 맞은편에서 찍은 일상 사진": "companion_viewpoint_everyday_candid",
            "촬영 중간 비하인드 사진": "production_gap_behind_scenes",
            "물리 인화사진 스캔": "physical_print_scan_material_context",
            "2000년대 싸이월드 디카 사진": "early_2000s_compact_digicam_social_repost",
            "선택 표시가 있는 컨택트 시트": "contact_sheet_selection_context",
        }
        for text, expected_id in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_id})

    def test_broad_nonvisual_collection_terms_never_hard_activate(self) -> None:
        cases = (
            "희얼사",
            "희연사",
            "희귀사진 rare pics",
            "unseen unreleased photo",
            "과사 프리데뷔",
            "삭제된 게시물",
            "미공개컷 B컷",
            "outtake HQ",
            "팬아저 레전드 사진",
            "홈마 프리뷰",
            "직찍",
            "남친짤 여친짤",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_adjacent_visual_confounds_fail_closed(self) -> None:
        cases = (
            "a rare bird photograph",
            "BTS rare pics",
            "private airport paparazzi photo",
            "a polished 200 mm studio portrait",
            "a clean event photo with a fake camera UI overlay",
            "an arm-length mirror selfie",
            "a sepia filter on a clean digital portrait",
            "a modern HDR phone portrait with retro film grain",
            "a decorative scrapbook collage",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_broad_aliases_expose_multiple_optional_candidate_routes(self) -> None:
        self.assertTrue(CANDIDATE_IDS <= set(self.capture_candidates))
        aliases_by_id = {
            candidate_id: set(self.capture_candidates[candidate_id]["aliases"])
            for candidate_id in CANDIDATE_IDS
        }
        self.assertEqual(
            {
                candidate_id
                for candidate_id, aliases in aliases_by_id.items()
                if "희얼사" in aliases
            },
            {
                "off_camera_companion_everyday_capture",
                "full_print_edge_scan_capture",
                "early_2000s_digicam_social_repost_capture",
            },
        )
        self.assertEqual(
            {
                candidate_id
                for candidate_id, aliases in aliases_by_id.items()
                if "희연사" in aliases
            },
            {
                "fan_side_public_event_telephoto_capture",
                "camera_lcd_rephotographed_preview_capture",
                "between_takes_production_capture",
            },
        )
        for candidate_id in CANDIDATE_IDS:
            with self.subTest(candidate_id=candidate_id):
                candidate = self.capture_candidates[candidate_id]
                self.assertEqual(candidate.get("for_any"), ["human"])
                self.assertGreaterEqual(len(candidate.get("keywords", [])), 4)
                self.assertGreaterEqual(len(candidate.get("embedding_text", "").split()), 18)

    def test_generated_indexes_contain_current_profiles_and_candidates(self) -> None:
        self.assertTrue(PROFILE_IDS <= set(self.visual_index["entries"]))
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        expected_entry_ids = {
            f"slot:capture_context:{candidate_id}" for candidate_id in CANDIDATE_IDS
        }
        self.assertTrue(expected_entry_ids <= set(semantic_index["entries"]))

    def test_three_arm_fixture_is_frozen_and_reference_bound(self) -> None:
        if not CASES_PATH.exists():
            self.skipTest("three-arm fixture is written after randomized arm selection")
        rows = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({row["arm_id"] for row in rows}), 3)
        self.assertEqual(len({row["profile_id"] for row in rows}), 3)
        for row in rows:
            with self.subTest(arm_id=row["arm_id"]):
                profile = self.profiles[row["profile_id"]]
                self.assertIs(row["randomized_complex_concept_required"], True)
                self.assertEqual(row["reference"]["role"], "appearance_reference")
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    {gate["id"] for gate in profile["render_gates"]},
                )
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                for path_key, hash_key in (
                    ("request_envelope_path", "request_envelope_file_sha256"),
                    ("authorial_core_path", "authorial_core_file_sha256"),
                ):
                    artifact = ROOT / row[path_key]
                    self.assertTrue(artifact.is_file())
                    self.assertEqual(
                        hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        row[hash_key],
                    )

    def test_research_note_preserves_nonvisual_and_identity_boundaries(self) -> None:
        note = RESEARCH_PATH.read_text(encoding="utf-8")
        for phrase in (
            "희얼사와 희연사는 단일 hard visual profile이 아니다",
            "실제 촬영자, 연예인 여부, 희소성, 촬영 연도, 공개 여부를 추론하지 않는다",
            "보이는 성인 외형만 참조한다",
            "partial 또는 누락은 실패",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, note)


if __name__ == "__main__":
    unittest.main()
