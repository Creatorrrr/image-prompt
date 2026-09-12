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
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "capture_elements_three_arm_pixel_test_cases_v1.jsonl"
)
RESEARCH_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "capture-elements-visual-semantics-20260902"
    / "source-research.md"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


EXACT_ROUTES = {
    "광각 근접 원근 과장 관계": "wide_angle_near_field_perspective",
    "망원 거리 압축 관계": "telephoto_distance_compression_relation",
    "얕은 심도 초점 이행 관계": "shallow_depth_focus_falloff_relation",
    "포커스 스태킹 전경 후경 합성": "focus_stacked_extended_depth_composite",
    "스플릿 디옵터 이중 초점면": "split_diopter_dual_focus_planes",
    "패닝 피사체 추적 모션 관계": "panning_subject_tracking_motion_relation",
    "후막 동조 플래시 모션 트레이스": "rear_curtain_flash_motion_trace",
    "롤링 셔터 판독 스큐": "rolling_shutter_readout_skew",
    "렘브란트 얼굴 조명 패턴": "rembrandt_face_light_pattern",
    "클램셸 상부 키 하부 필 조명": "clamshell_dual_source_portrait_light",
    "네거티브 필 그림자 심화 관계": "negative_fill_shadow_deepening_relation",
    "디퓨전 필터 하이라이트 헤일레이션": "diffusion_filter_highlight_halation",
    "혼합 광원 화이트밸런스 관계": "mixed_illuminant_white_balance_relation",
    "하이라이트 롤오프 톤 응답": "highlight_rolloff_tone_response",
}

PROFILE_IDS = set(EXACT_ROUTES.values())


class PhotoCaptureElementsVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }
        cls.routing_registry = {
            **cls.registry,
            "profiles": [
                profile
                for profile in cls.registry["profiles"]
                if str(profile.get("id") or "") in PROFILE_IDS
            ],
        }
        cls.routing_index = prompt_generator.build_visual_profile_index_payload(
            cls.routing_registry
        )
        cls.index = prompt_generator.load_visual_profile_index(
            INDEX_PATH,
            cls.registry,
        )
        cls.pixel_cases = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

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
            self.routing_registry,
            self.source_rows(text),
            visual_profile_index=self.routing_index,
            adult_context=True,
        )
        return {
            str(hit["profile_id"])
            for hit in resolution["hits"]
            if hit.get("match_basis") == "exact"
            and hit.get("hard_eligible") is True
        }

    def test_profiles_are_complete_five_group_pixel_contracts(self) -> None:
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
        all_gate_ids = [
            str(gate["id"])
            for profile in self.registry["profiles"]
            for gate in profile["render_gates"]
        ]
        self.assertEqual(len(all_gate_ids), len(set(all_gate_ids)))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                group_ids = {str(group["id"]) for group in components["groups"]}
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(set(components["required_group_ids"]), group_ids)
                self.assertEqual(len(group_ids), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                self.assertGreaterEqual(
                    len(profile["concept_candidate"]["concept_terms"]), 5
                )

    def test_narrow_exact_terms_route_to_one_profile(self) -> None:
        for text, expected_profile_id in EXACT_ROUTES.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_profile_id})

    def test_broad_equipment_and_look_labels_never_force_hard_profiles(self) -> None:
        broad_terms = (
            "85mm portrait",
            "24mm wide angle lens",
            "f/1.4 shallow depth of field",
            "cinematic bokeh",
            "motion blur",
            "soft portrait light",
            "mixed lighting",
            "film look",
            "ARRI color science",
            "Kodak film stock",
            "12-bit RAW ACES workflow",
            "medium format look",
            "high MTF lens",
        )
        for term in broad_terms:
            with self.subTest(term=term):
                self.assertEqual(self.hard_matches(term), set())

    def test_adjacent_visual_substitutes_fail_closed(self) -> None:
        adjacent = (
            "a digitally cropped portrait with background blur",
            "a fisheye filter curving the outer frame",
            "a uniformly soft beauty portrait",
            "an HDR panorama with sharp details",
            "a Dutch-angle street photograph",
            "a ring-light headshot",
            "an orange and teal split-tone grade",
            "atmospheric fog and global bloom",
            "a front-curtain flash streak ahead of a sharp subject",
            "a flat low-contrast image with gray highlights",
        )
        for text in adjacent:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_generated_index_is_current_and_contains_every_profile(self) -> None:
        self.assertLessEqual(PROFILE_IDS, set(self.index["entries"]))
        exact_pairs = {
            (str(row["term"]), str(row["profile_id"]))
            for row in self.index["exact_lookup"]
        }
        for term, profile_id in EXACT_ROUTES.items():
            with self.subTest(term=term):
                self.assertIn((term, profile_id), exact_pairs)

    def test_semantic_panning_paraphrase_projects_optional_candidate_only(self) -> None:
        target_id = "panning_subject_tracking_motion_relation"
        target_registry = {
            **self.routing_registry,
            "profiles": [self.profiles[target_id]],
        }
        vectors = {
            str(profile["id"]): (
                [1.0, 0.0] if profile["id"] == target_id else [0.0, 1.0]
            )
            for profile in target_registry["profiles"]
        }
        fake_index = prompt_generator.build_visual_profile_index_payload(
            target_registry,
            vectors=vectors,
            dimensions=2,
        )
        paraphrase = (
            "The moving subject's identity-bearing core remains comparatively sharp and "
            "readable. Environmental detail stretches into predominantly parallel "
            "directional streaks. Secondary moving parts retain plausible local motion or "
            "rotational blur. Background streaks subject travel and local motion cues "
            "agree on one lateral movement vector. "
            "상대적인 피사체 선명도가 전역 카메라 흔들림 방사형 줌 또는 합성 블러가 아닌 "
            "능동 추적을 증명함"
        )
        resolution = prompt_generator.resolve_visual_profile_hits(
            target_registry,
            [
                {
                    "source": "authorial_core_interpretation",
                    "text": paraphrase,
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text=paraphrase,
            query_fields={"interpreted_intent": paraphrase},
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(
            row for row in resolution["hits"] if row["profile_id"] == target_id
        )
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

        data = {
            prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY: target_registry,
            prompt_generator.VISUAL_PROFILE_INDEX_DATA_KEY: fake_index,
        }
        result = {
            "provenance": {
                "prompt_id": "capture-elements-optional-candidate-test",
                "concept_lock": [paraphrase],
            }
        }
        concepts = prompt_generator.candidate_pack_visual_concept_candidates(
            data,
            result,
            {},
            None,
            None,
            resolution,
        )
        self.assertIsNotNone(concepts)
        candidate = next(
            row
            for row in concepts["candidates"]
            if row["id"] == f"visual-concept:{target_id}"
        )
        self.assertEqual(
            candidate["opt_in_contract"]["effect"],
            "promote_to_hard_visual_obligation",
        )
        self.assertEqual(
            len(candidate["opt_in_contract"]["obligation"]["render_gates"]),
            5,
        )
        self.assertNotIn("score", candidate)
        self.assertNotIn("matched_terms", candidate)

    def test_research_note_preserves_metadata_and_evidence_boundaries(self) -> None:
        note = RESEARCH_PATH.read_text(encoding="utf-8")
        for phrase in (
            "장비 이름이나 분위기 라벨이 아니라",
            "신원, 동일인 여부",
            "exact term만 자동 hard obligation",
            "`partial`, 누락, 판단 불가, 근거 없는 판정은 실패",
            "이미지가 생성되지 않으면 품질 0점이 아니라 `UNSCORED`",
            "요청 사용자의 선호·수락은 별도 증거",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, note)

    def test_three_arm_render_fixture_is_hash_bound_and_fail_closed(self) -> None:
        expected_profiles = {
            "panning_subject_tracking_motion_relation",
            "rembrandt_face_light_pattern",
            "highlight_rolloff_tone_response",
        }
        self.assertEqual(len(self.pixel_cases), 3)
        self.assertEqual(
            {case["profile_id"] for case in self.pixel_cases},
            expected_profiles,
        )
        self.assertEqual(len({case["arm_id"] for case in self.pixel_cases}), 3)

        for case in self.pixel_cases:
            with self.subTest(case_id=case["case_id"]):
                self.assertEqual(
                    case["schema_version"],
                    "photo-capture-elements-independent-pixel-case/v1",
                )
                self.assertEqual(case["case_role"], "held-out")
                self.assertEqual(case["reference"]["role"], "appearance_reference")
                self.assertEqual(
                    case["reference"]["sha256"],
                    "3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea",
                )
                self.assertEqual(
                    case["required_gate_ids"],
                    [
                        gate["id"]
                        for gate in self.profiles[case["profile_id"]]["render_gates"]
                    ],
                )
                self.assertEqual(
                    set(case["observed_gate_statuses"]),
                    set(case["required_gate_ids"]),
                )
                self.assertLessEqual(
                    set(case["observed_gate_statuses"].values()),
                    {"pass", "fail"},
                )
                expected_verdict = (
                    "pass"
                    if all(
                        status == "pass"
                        for status in case["observed_gate_statuses"].values()
                    )
                    else "fail"
                )
                self.assertEqual(case["technical_pixel_verdict"], expected_verdict)
                self.assertEqual(case["package_status"], "pass")
                self.assertEqual(case["prompt_status"], "pass")
                self.assertEqual(case["runtime_status"], "pass")
                self.assertEqual(
                    case["generation_budget"],
                    {"image_calls": 1, "retries": 0, "fallbacks": 0},
                )
                self.assertIs(case["independence"]["cross_arm_inputs_used"], False)
                self.assertEqual(
                    case["verdict_rule"]["partial_missing_or_uninspectable"],
                    "fail",
                )
                self.assertEqual(
                    case["verdict_rule"]["user_judgment"],
                    "separate_pending",
                )

                for path_key, hash_key in (
                    ("request_envelope_path", "request_envelope_file_sha256"),
                    ("authorial_core_path", "authorial_core_file_sha256"),
                    ("candidate_pack_path", "candidate_pack_file_sha256"),
                    ("composed_prompt_path", "composed_prompt_file_sha256"),
                    ("render_request_path", "render_request_file_sha256"),
                    ("render_path", "render_sha256"),
                    ("review_path", "review_file_sha256"),
                    ("manifest_path", "manifest_file_sha256"),
                ):
                    artifact = ROOT / case[path_key]
                    self.assertTrue(artifact.is_file())
                    self.assertEqual(
                        hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        case[hash_key],
                    )

                pack = json.loads((ROOT / case["candidate_pack_path"]).read_text())
                composed = json.loads((ROOT / case["composed_prompt_path"]).read_text())
                request = json.loads((ROOT / case["render_request_path"]).read_text())
                review = json.loads((ROOT / case["review_path"]).read_text())
                manifest = json.loads((ROOT / case["manifest_path"]).read_text())
                self.assertEqual(pack[0]["pack_id"], case["pack_id"])
                self.assertEqual(composed["pack_id"], case["pack_id"])
                self.assertEqual(request["pack_id"], case["pack_id"])
                self.assertEqual(review["pack_id"], case["pack_id"])
                self.assertEqual(manifest["pack_id"], case["pack_id"])
                self.assertEqual(manifest["arm_id"], case["arm_id"])
                self.assertEqual(manifest["image_call_count"], 1)
                self.assertIs(manifest["cross_arm_inputs_used"], False)
                self.assertEqual(manifest["image_hashes"][0]["sha256"], case["render_sha256"])
                self.assertEqual(review["result_sha256"], case["render_sha256"])
                self.assertEqual(
                    {
                        gate_id: gate["status"]
                        for gate_id, gate in review["hard_gates"].items()
                    },
                    case["observed_gate_statuses"],
                )
                self.assertEqual(
                    review["user_judgment"]["source"],
                    "not_yet_received",
                )


if __name__ == "__main__":
    unittest.main()
