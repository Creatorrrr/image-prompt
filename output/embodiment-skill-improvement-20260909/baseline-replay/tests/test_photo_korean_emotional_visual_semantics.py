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
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "research_evidence.jsonl"
)
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "korean_emotional_photo_three_arm_pixel_cases_v1.jsonl"
)
RESEARCH_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "korean-emotional-photo-semantics-20260902"
    / "source-research.md"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "mirror_selfie_reflection_device_topology",
    "overhead_social_snapshot_relation",
    "intentional_face_occluded_mood_portrait",
    "sheer_complexion_texture_preservation",
    "under_eye_high_cheek_blush_distribution",
    "cheekbone_temple_blush_drape",
    "photobooth_four_cut_sequence",
}

CANDIDATE_IDS = {
    "korean_candy_gloss_lip_family",
    "mirror_selfie",
    "photodump_candid_sequence_context",
    "off_camera_companion_everyday_capture",
    "overhead_social_snapshot_relation",
    "mirror_selfie_reflection_device_topology",
    "intentional_face_occluded_mood_portrait",
    "phone_0_5x_ultrawide",
    "four_cut_grid",
    "korean_good_vibe_social_portrait",
    "adult_first_love_nostalgia",
    "clear_serene_softness",
    "airy_delicate_styling_without_body_inference",
    "sheer_complexion_texture_preservation",
    "high_shine_glossy_lip",
    "cheekbone_to_temple_blush_drape",
    "under_eye_high_cheek_blush",
    "translucent_base_makeup_skin",
    "soft_milky_low_contrast_grading",
    "profile_picture_crop_safe",
}


class PhotoKoreanEmotionalVisualSemanticsTests(unittest.TestCase):
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
            row["id"]: (slot, row)
            for slot, rows in cls.tags["slots"].items()
            for row in rows
            if isinstance(row, dict) and row.get("id")
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
            str(hit["profile_id"])
            for hit in resolution["hits"]
            if hit["match_basis"] == "exact" and hit["hard_eligible"] is True
        }

    def test_profiles_are_complete_four_or_five_group_pixel_contracts(self) -> None:
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
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
                group_ids = {group["id"] for group in components["groups"]}
                evidence_fields = set(profile["required_evidence_fields"])
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertIn(components["minimum_component_groups"], {4, 5})
                self.assertEqual(set(components["required_group_ids"]), group_ids)
                self.assertEqual(evidence_fields, set(profile["evidence_requirements"]))
                self.assertEqual(len(profile["render_gates"]), len(group_ids))
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                self.assertTrue(profile["concept_candidate"]["concept_terms"])

    def test_narrow_exact_terms_route_to_expected_profiles(self) -> None:
        cases = {
            "거셀": "mirror_selfie_reflection_device_topology",
            "MZ 항공샷": "overhead_social_snapshot_relation",
            "얼굴 안 보이는 감성샷": "intentional_face_occluded_mood_portrait",
            "맑고 투명한 얇은 피부 표현": "sheer_complexion_texture_preservation",
            "언더아이 블러셔": "under_eye_high_cheek_blush_distribution",
            "드레이핑 블러셔": "cheekbone_temple_blush_drape",
            "인생네컷": "photobooth_four_cut_sequence",
        }
        for text, expected_id in cases.items():
            with self.subTest(text=text):
                exact_ids = {
                    str(row["profile_id"])
                    for row in self.visual_index["exact_lookup"]
                    if str(row["term"]).casefold() == text.casefold()
                }
                self.assertEqual(exact_ids, {expected_id})
        self.assertEqual(
            self.hard_matches(" ; ".join(cases)),
            set(cases.values()),
        )

    def test_broad_or_metadata_terms_never_hard_activate(self) -> None:
        cases = (
            "느좋",
            "추구미",
            "프사각",
            "여리여리",
            "뽀용",
            "탕후루 립",
            "포토덤프",
            "0.5배샷",
            "남찍사",
            "첫사랑 재질",
            "청순",
        )
        self.assertEqual(self.hard_matches(" ; ".join(cases)), set())

    def test_adjacent_visual_confounds_fail_closed(self) -> None:
        cases = (
            "direct front-camera selfie with no mirror",
            "empty mirror beside an adult",
            "drone landscape with one tiny person",
            "eye-level portrait with one stretched arm",
            "a face lost only to missed focus and motion blur",
            "opaque poreless full-coverage beauty filter",
            "dark circles under the eyes from cast shadow",
            "contour stripes and colored light near the temples",
            "four unrelated portraits placed in a collage",
        )
        self.assertEqual(self.hard_matches(" ; ".join(cases)), set())

    def test_candidate_aliases_and_nonvisual_boundaries_are_encoded(self) -> None:
        self.assertLessEqual(CANDIDATE_IDS, set(self.candidates))
        expected_aliases = {
            "korean_good_vibe_social_portrait": "느좋",
            "adult_first_love_nostalgia": "첫사랑 재질",
            "clear_serene_softness": "청초",
            "airy_delicate_styling_without_body_inference": "여리여리",
            "soft_milky_low_contrast_grading": "뽀용",
            "profile_picture_crop_safe": "프사각",
            "phone_0_5x_ultrawide": "0.5배샷",
            "photodump_candid_sequence_context": "포토덤프",
            "off_camera_companion_everyday_capture": "남찍사",
            "korean_candy_gloss_lip_family": "탕후루 립",
        }
        for candidate_id, alias in expected_aliases.items():
            with self.subTest(candidate_id=candidate_id):
                candidate = self.candidates[candidate_id][1]
                self.assertIn(alias, candidate["aliases"])
                self.assertGreaterEqual(len(candidate.get("keywords", [])), 3)
                self.assertGreaterEqual(len(candidate.get("embedding_text", "").split()), 8)
        self.assertIn(
            "does not prove overhead geometry",
            self.candidates["phone_0_5x_ultrawide"][1]["embedding_text"],
        )
        self.assertIn(
            "never to literal candy or fruit props",
            self.candidates["high_shine_glossy_lip"][1]["embedding_text"],
        )
        self.assertIn(
            "must not be converted into claims about body size",
            self.candidates["airy_delicate_styling_without_body_inference"][1][
                "embedding_text"
            ],
        )
        self.assertIn(
            "without school uniform, minor coding, an actual relationship claim",
            self.candidates["adult_first_love_nostalgia"][1]["embedding_text"],
        )

    def test_bm25f_routes_researched_shorthand_to_expected_candidates(self) -> None:
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(
            semantic_index,
            self.tags,
        )
        bm25f = prompt_generator.semantic_bm25f_payload_from_index(semantic_index)
        cases = {
            "느좋녀 인스타 감성": "slot:aesthetic_trend:korean_good_vibe_social_portrait",
            "0.5배샷": "slot:lens:phone_0_5x_ultrawide",
            "탕후루 립": "slot:makeup_style:korean_candy_gloss_lip_family",
            "언더아이 블러셔": "slot:cheek_makeup:under_eye_high_cheek_blush",
            "포토덤프": "slot:capture_context:photodump_candid_sequence_context",
            "프사각": "slot:platform_framing:profile_picture_crop_safe",
            "첫사랑 재질": "slot:aesthetic_trend:adult_first_love_nostalgia",
            "청순 청초": "slot:aesthetic_trend:clear_serene_softness",
            "여리여리": "slot:aesthetic_trend:airy_delicate_styling_without_body_inference",
            "뽀용 뽀얀": "slot:color_grading:soft_milky_low_contrast_grading",
            "남찍사": "slot:capture_context:off_camera_companion_everyday_capture",
            "얼굴 안 보이는 감성샷": "slot:composition:intentional_face_occluded_mood_portrait",
            "MZ 항공샷": "slot:camera_direction:overhead_social_snapshot_relation",
            "인생네컷": "slot:format:four_cut_grid",
            "드레이핑 블러셔": "slot:cheek_makeup:cheekbone_to_temple_blush_drape",
            "맑고 투명한 얇은 피부 표현": "slot:complexion_coverage:sheer_complexion_texture_preservation",
        }
        for query, expected_id in cases.items():
            with self.subTest(query=query):
                ranked = prompt_generator.rank_bm25f(
                    bm25f,
                    {"active_request": query},
                    limit=5,
                )
                self.assertTrue(ranked)
                self.assertEqual(ranked[0]["document_id"], expected_id)
        mirror_ranked = prompt_generator.rank_bm25f(
            bm25f,
            {"active_request": "거셀"},
            limit=2,
        )
        self.assertEqual(
            {row["document_id"] for row in mirror_ranked},
            {
                "slot:action:mirror_selfie",
                "slot:composition:mirror_selfie_reflection_device_topology",
            },
        )

    def test_definition_only_profiles_hide_labels_at_runtime(self) -> None:
        for profile_id in (
            "intentional_face_occluded_mood_portrait",
            "sheer_complexion_texture_preservation",
        ):
            with self.subTest(profile_id=profile_id):
                runtime = self.profiles[profile_id]["runtime_expression"]
                self.assertEqual(runtime["default_mode"], "definition_only")
                self.assertFalse(runtime["prompt_label_terms"])
                self.assertTrue(runtime["runtime_forbidden_labels"])

    def test_generated_indexes_contain_current_profiles_and_candidates(self) -> None:
        self.assertLessEqual(PROFILE_IDS, set(self.visual_index["entries"]))
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        expected_ids = {
            f"slot:{slot}:{candidate_id}"
            for candidate_id, (slot, _row) in self.candidates.items()
            if candidate_id in CANDIDATE_IDS
        }
        self.assertLessEqual(expected_ids, set(semantic_index["entries"]))

    def test_three_arm_fixture_is_frozen_independent_and_reference_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({row["arm_id"] for row in rows}), 3)
        for row in rows:
            with self.subTest(arm_id=row["arm_id"]):
                expected_gates = {
                    gate["id"]
                    for profile_id in row["profile_ids"]
                    for gate in self.profiles[profile_id]["render_gates"]
                }
                self.assertEqual(set(row["required_gate_ids"]), expected_gates)
                self.assertEqual(row["reference"]["role"], "appearance_reference")
                reference = Path(row["reference"]["path"])
                self.assertTrue(reference.is_file())
                self.assertEqual(
                    hashlib.sha256(reference.read_bytes()).hexdigest(),
                    row["reference"]["sha256"],
                )
                policy = row["generation_policy"]
                self.assertIs(policy["independent_arm"], True)
                self.assertIs(policy["single_generation_call"], True)
                self.assertIs(policy["retry_allowed"], False)
                self.assertIs(policy["fallback_allowed"], False)
                self.assertIs(policy["cross_arm_inputs_allowed"], False)
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                for path_key, hash_key in (
                    ("request_envelope_path", "request_envelope_file_sha256"),
                    ("authorial_core_path", "authorial_core_file_sha256"),
                    ("visual_intent_path", "visual_intent_file_sha256"),
                    ("candidate_pack_path", "candidate_pack_file_sha256"),
                ):
                    artifact = ROOT / row[path_key]
                    self.assertTrue(artifact.is_file())
                    self.assertEqual(
                        hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        row[hash_key],
                    )
                pack = json.loads((ROOT / row["candidate_pack_path"]).read_text())
                self.assertEqual(len(pack), 1)
                self.assertEqual(pack[0]["contract_version"], "photo-candidate-pack/v6")
                self.assertEqual(
                    {item["id"] for item in pack[0]["visual_obligations"]["obligations"]},
                    set(row["profile_ids"]),
                )

    def test_research_note_preserves_semantic_and_identity_boundaries(self) -> None:
        note = RESEARCH_PATH.read_text(encoding="utf-8")
        for phrase in (
            "추구미와 느좋은 단일 hard visual profile이 아니다",
            "0.5배샷은 렌즈 후보만으로 항공샷 기하를 증명하지 않는다",
            "첫사랑 재질은 분명한 성인 피사체로만 해석한다",
            "보이는 성인 외형만 참조한다",
            "partial 또는 누락은 실패",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, note)

    def test_research_evidence_is_approved_source_and_candidate_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        scoped = [
            row
            for row in rows
            if row.get("domain") == "korean_emotional_social_photo_visual_semantics"
        ]
        self.assertEqual(len(scoped), 7)
        self.assertEqual(len({row["id"] for row in scoped}), 7)
        for row in scoped:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                self.assertLessEqual(set(row["candidate_ids"]), CANDIDATE_IDS)


if __name__ == "__main__":
    unittest.main()
