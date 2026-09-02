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
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
SEMANTIC_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_semantic_index.json"
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
RESEARCH_PATH = ROOT / "docs" / "analysis" / "2026-09-02-suggestive-editorial-visual-semantics.md"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "suggestive_editorial_three_arm_pixel_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_TERMS = {
    "adult_everyday_controlled_reveal_moment": "성인 일상 동작의 조절된 가림-드러남 장면",
    "strategic_coverage_figure_study": "전략적 가림의 임플라이드 피겨 스터디",
    "underwear_as_outerwear_layer_system": "언더웨어 애즈 아우터웨어 레이어 시스템",
    "soft_window_private_room_adult_portrait": "소프트 윈도 사적 공간 성인 포트레이트",
}

EXPECTED_PROFILE_GATE_COUNTS = {
    "adult_everyday_controlled_reveal_moment": 9,
    "strategic_coverage_figure_study": 7,
    "underwear_as_outerwear_layer_system": 5,
    "soft_window_private_room_adult_portrait": 5,
}

EXPECTED_CANDIDATES = {
    "action": {
        "shirt_cuff_adjustment_mid_action",
        "hair_tie_mid_action",
        "jewelry_fastening_mirror_action",
        "curtain_draw_window_pause",
        "jacket_lapel_settle_action",
    },
    "composition": {
        "single_edge_layered_reveal_topology",
        "sheet_drape_stable_coverage_path",
        "forearm_coverage_contour_continuity",
        "environmental_three_quarter_face_body_context",
        "camera_acknowledged_observer_frame",
    },
    "garment_detail": {
        "single_edge_layered_reveal_garment",
        "sheet_drape_stable_coverage_detail",
        "lace_edge_over_opaque_base",
        "visible_bralette_tailored_blazer_layer",
        "camisole_slip_over_shirt_layer",
        "waistband_reveal_outer_garment_edges",
    },
    "surface_material": {
        "sheet_fold_contact_shadow_surface",
        "ribbed_knit_body_boundary_surface",
        "lace_opaque_layer_separation_surface",
        "curtain_diffused_window_gradient_surface",
    },
}

EXPECTED_PRESETS = {
    "adult_controlled_reveal_window_editorial",
    "strategic_coverage_figure_study_editorial",
    "underwear_outerwear_layered_editorial",
    "soft_window_private_room_editorial",
}

EXPECTED_ARM_PROFILES = {
    "arm-01-window-reveal": {
        "adult_everyday_controlled_reveal_moment",
        "soft_window_private_room_adult_portrait",
    },
    "arm-02-figure-coverage": {"strategic_coverage_figure_study"},
    "arm-03-layered-mirror": {
        "underwear_as_outerwear_layer_system",
        "mirror_selfie_reflection_device_topology",
    },
}

EXPECTED_ARM_GATE_COUNTS = {
    "arm-01-window-reveal": 10,
    "arm-02-figure-coverage": 5,
    "arm-03-layered-mirror": 10,
}


class PhotoSuggestiveEditorialVisualSemanticsTests(unittest.TestCase):
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
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.candidates = {
            slot: {row["id"]: row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.presets = {row["id"]: row for row in cls.tags["presets"]}

    @staticmethod
    def source_rows(text: str) -> list[dict[str, object]]:
        return [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            }
        ]

    def hard_matches(self, text: str) -> set[str]:
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            self.source_rows(text),
            visual_profile_index=self.visual_index,
            adult_context=True,
        )
        return {
            str(hit["profile_id"])
            for hit in resolution["hits"]
            if hit["match_basis"] == "exact" and hit["hard_eligible"] is True
        }

    def test_profiles_are_complete_definition_only_pixel_contracts(self) -> None:
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertFalse(errors, errors)
        for profile_id in PROFILE_TERMS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                group_ids = {row["id"] for row in components["groups"]}
                self.assertIs(profile["activation"]["requires_adult_character"], True)
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                expected_count = EXPECTED_PROFILE_GATE_COUNTS[profile_id]
                self.assertEqual(
                    components["minimum_component_groups"],
                    expected_count,
                )
                self.assertEqual(set(components["required_group_ids"]), group_ids)
                self.assertEqual(len(group_ids), expected_count)
                self.assertEqual(len(profile["render_gates"]), expected_count)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                runtime = profile["runtime_expression"]
                self.assertEqual(runtime["default_mode"], "definition_only")
                self.assertFalse(runtime["prompt_label_terms"])
                self.assertLessEqual(
                    set(profile["activation"]["exact_terms"]),
                    set(runtime["runtime_forbidden_labels"]),
                )
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)

    def test_controlled_reveal_requires_target_causality_salience_and_necessity(
        self,
    ) -> None:
        profile = self.profiles["adult_everyday_controlled_reveal_moment"]
        required_groups = set(
            profile["semantics"]["component_semantics"]["required_group_ids"]
        )
        self.assertLessEqual(
            {
                "everyday_reveal_bounded_target_relation",
                "everyday_reveal_action_boundary_causality",
                "everyday_reveal_thumbnail_salience",
                "everyday_reveal_counterfactual_necessity",
            },
            required_groups,
        )
        gate_ids = {gate["id"] for gate in profile["render_gates"]}
        self.assertLessEqual(
            {
                "vo_everyday_reveal_bounded_target",
                "vo_everyday_reveal_action_boundary_causality",
                "vo_everyday_reveal_thumbnail_dual_salience",
                "vo_everyday_reveal_counterfactual_necessity",
            },
            gate_ids,
        )
        self.assertLessEqual(
            {
                "generic_opaque_over_opaque_layering",
                "unrelated_gesture_beside_preexisting_opening",
                "thumbnail_incidental_boundary",
                "ordinary_fashion_survives_boundary_removal",
            },
            set(profile["reject_substitutes"]),
        )

    def test_figure_coverage_requires_primary_nonredundant_carrier(self) -> None:
        profile = self.profiles["strategic_coverage_figure_study"]
        required_groups = set(
            profile["semantics"]["component_semantics"]["required_group_ids"]
        )
        self.assertLessEqual(
            {
                "figure_coverage_primary_carrier",
                "figure_coverage_nonredundant_necessity",
            },
            required_groups,
        )
        gate_ids = {gate["id"] for gate in profile["render_gates"]}
        self.assertLessEqual(
            {
                "vo_figure_coverage_primary_carrier",
                "vo_figure_coverage_nonredundant_necessity",
            },
            gate_ids,
        )
        self.assertIn(
            "redundant_full_coverage_garment_behind_occluder",
            profile["reject_substitutes"],
        )

    def test_narrow_exact_terms_route_to_one_expected_profile(self) -> None:
        for profile_id, term in PROFILE_TERMS.items():
            with self.subTest(profile_id=profile_id):
                self.assertEqual(
                    self.hard_matches(f"명백한 성인 인물의 {term}"),
                    {profile_id},
                )

    def test_broad_slanga_genres_and_single_cues_remain_nonhard(self) -> None:
        broad = (
            "은꼴사",
            "대꼴사",
            "야짤",
            "세미 누드",
            "임플라이드 누드",
            "부두아르",
            "란제리 화보",
            "침실 사진",
            "소프트 윈도",
            "노출이 있는 성인 사진",
            "direct gaze and fitted clothing",
        )
        new_ids = set(PROFILE_TERMS)
        for text in broad:
            with self.subTest(text=text):
                self.assertTrue(self.hard_matches(text).isdisjoint(new_ids))

    def test_candidate_atoms_and_presets_are_reachable(self) -> None:
        for slot, expected_ids in EXPECTED_CANDIDATES.items():
            with self.subTest(slot=slot):
                self.assertLessEqual(expected_ids, set(self.candidates[slot]))
        self.assertLessEqual(EXPECTED_PRESETS, set(self.presets))
        all_expected = set().union(*EXPECTED_CANDIDATES.values())
        referenced: set[str] = set()
        for preset_id in EXPECTED_PRESETS:
            preset = self.presets[preset_id]
            self.assertTrue(preset["required_slots"])
            for rule in preset["filters"].values():
                referenced.update(rule.get("ids", []))
        intentionally_unbound_after_regression = {
            "camera_acknowledged_observer_frame",
            "forearm_coverage_contour_continuity",
        }
        self.assertLessEqual(
            all_expected - intentionally_unbound_after_regression,
            referenced,
        )
        self.assertTrue(intentionally_unbound_after_regression.isdisjoint(referenced))

    def test_presets_remove_uncoupled_or_redundant_choices(self) -> None:
        reveal_filters = self.presets[
            "adult_controlled_reveal_window_editorial"
        ]["filters"]
        self.assertEqual(
            reveal_filters["action"]["ids"],
            ["jacket_lapel_settle_action"],
        )
        self.assertNotIn(
            "sheet_drape_stable_coverage_detail",
            reveal_filters["garment_detail"]["ids"],
        )
        coverage_filters = self.presets[
            "strategic_coverage_figure_study_editorial"
        ]["filters"]
        self.assertEqual(
            coverage_filters["garment_detail"]["ids"],
            ["sheet_drape_stable_coverage_detail"],
        )
        self.assertEqual(
            coverage_filters["composition"]["ids"],
            [
                "sheet_drape_stable_coverage_path",
                "environmental_three_quarter_face_body_context",
            ],
        )

    def test_skill_fail_closes_uncovered_focal_meaning(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for phrase in (
            "explicitly makes a perceptual effect focal",
            "focal meaning is still uncovered",
            "A broad label, an embedding hit, or an optional candidate is not coverage",
            "Record this focal-coverage check separately from prompt, runtime, and pixel status",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, skill_text)

    def test_generated_indexes_include_new_profiles_and_candidates(self) -> None:
        self.assertLessEqual(set(PROFILE_TERMS), set(self.visual_index["entries"]))
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(
            semantic_index,
            self.tags,
        )
        expected_document_ids = {
            f"slot:{slot}:{candidate_id}"
            for slot, candidate_ids in EXPECTED_CANDIDATES.items()
            for candidate_id in candidate_ids
        } | {f"preset:{preset_id}" for preset_id in EXPECTED_PRESETS}
        self.assertLessEqual(expected_document_ids, set(semantic_index["entries"]))

    def test_research_evidence_is_approved_and_candidate_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        evidence_rows = [
            row
            for row in rows
            if row["id"].startswith("suggestive_editorial_semantics_")
        ]
        self.assertEqual(len(evidence_rows), 8)
        known_ids = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        } | set(self.presets)
        for row in evidence_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["status"], "approved")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertLessEqual(set(row["candidate_ids"]), known_ids)
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_research_note_records_reference_and_evidence_boundaries(self) -> None:
        note = RESEARCH_PATH.read_text(encoding="utf-8")
        for phrase in (
            "넓은 반응·유통 용어",
            "실제 동의의 증명이 아니다",
            "보이는 성인 얼굴 비율",
            "partial`, 누락, 판정 불가는 실패",
            "prompt/runtime audit PASS는 pixel PASS가 아니다",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, note)

    def test_three_arm_fixture_is_hash_bound_when_present(self) -> None:
        if not CASES_PATH.exists():
            self.skipTest("three-arm render fixture is created after independent arms")
        rows = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({row["arm_id"] for row in rows}), 3)
        self.assertEqual({row["arm_id"] for row in rows}, set(EXPECTED_ARM_PROFILES))
        reference_hash = "3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea"
        for row in rows:
            with self.subTest(arm_id=row["arm_id"]):
                arm_id = row["arm_id"]
                self.assertEqual(row["reference"]["sha256"], reference_hash)
                self.assertEqual(set(row["profile_ids"]), EXPECTED_ARM_PROFILES[arm_id])
                self.assertIsInstance(row["random_seed"], int)
                self.assertGreater(row["random_seed"], 0)
                self.assertGreaterEqual(
                    len(row["randomized_complex_concept"].split()),
                    8,
                )
                self.assertIs(row["generation_policy"]["independent_arm"], True)
                self.assertIs(row["generation_policy"]["single_generation_call"], True)
                self.assertIs(row["generation_policy"]["retry_allowed"], False)
                self.assertIs(row["generation_policy"]["fallback_allowed"], False)
                self.assertIs(row["generation_policy"]["cross_arm_inputs_allowed"], False)
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                self.assertIs(row["verdict_rule"]["unscored_is_not_zero"], True)
                self.assertIs(
                    row["verdict_rule"]["prompt_runtime_pass_is_not_pixel_pass"],
                    True,
                )
                self.assertEqual(row["package_status"], "pass")
                self.assertEqual(row["prompt_status"], "pass")
                self.assertEqual(row["runtime_status"], "pass")
                self.assertEqual(
                    len(row["required_gate_ids"]),
                    EXPECTED_ARM_GATE_COUNTS[arm_id],
                )
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    set(row["observed_gate_statuses"]),
                )
                for key in (
                    "source_snapshot_path",
                    "request_envelope_path",
                    "authorial_core_path",
                    "visual_intent_path",
                    "candidate_pack_path",
                    "composed_prompt_path",
                    "render_request_path",
                    "review_path",
                    "manifest_path",
                ):
                    artifact = ROOT / row[key]
                    self.assertTrue(artifact.is_file())
                    self.assertEqual(
                        hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        row[f"{key.removesuffix('_path')}_file_sha256"],
                    )
                if row["generation_status"] == "success":
                    self.assertEqual(row["technical_pixel_verdict"], "pass")
                    self.assertEqual(
                        set(row["observed_gate_statuses"].values()),
                        {"pass"},
                    )
                    render = ROOT / row["render_path"]
                    self.assertTrue(render.is_file())
                    self.assertEqual(
                        hashlib.sha256(render.read_bytes()).hexdigest(),
                        row["render_sha256"],
                    )
                else:
                    self.assertEqual(row["generation_status"], "safety_block_no_output")
                    self.assertEqual(row["technical_pixel_verdict"], "unscored")
                    self.assertEqual(
                        set(row["observed_gate_statuses"].values()),
                        {"unscored"},
                    )
                    self.assertIsNone(row["render_path"])
                    self.assertIsNone(row["render_sha256"])


if __name__ == "__main__":
    unittest.main()
