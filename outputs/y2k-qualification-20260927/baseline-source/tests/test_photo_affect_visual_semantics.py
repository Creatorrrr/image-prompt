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
RESEARCH_DIR = ROOT / "docs" / "research-evidence" / "photo-prompt" / "affect_display"
PIXEL_CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "affect_semantics_pixel_test_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_CONTRACTS = {
    "achievement_reward_smile": {
        "exact_term": "성취 보상 미소",
        "required_groups": {
            "authored_success_result",
            "symmetric_positive_face_action",
            "result_directed_attention",
            "post_success_consequence",
        },
        "required_fields": {
            "successful_result_phrase",
            "symmetric_smile_action_phrase",
            "result_attention_phrase",
            "post_success_consequence_phrase",
        },
    },
    "affiliative_reassurance_smile": {
        "exact_term": "안심시키는 친화 미소",
        "required_groups": {
            "concerned_peer_target",
            "restrained_affiliative_face",
            "concrete_support_action",
            "peer_response_consequence",
        },
        "required_fields": {
            "concerned_peer_phrase",
            "restrained_smile_phrase",
            "support_action_phrase",
            "peer_response_phrase",
        },
    },
    "decision_uncertainty_display": {
        "exact_term": "선택지 사이 혼란",
        "required_groups": {
            "two_visible_alternatives",
            "comparison_gaze",
            "restrained_face_tension",
            "paused_choice_action",
            "unresolved_decision_state",
        },
        "required_fields": {
            "visible_alternatives_phrase",
            "comparison_gaze_phrase",
            "facial_tension_phrase",
            "paused_action_phrase",
            "unresolved_choice_phrase",
        },
    },
    "embarrassment_repair_display": {
        "exact_term": "당황 수습 반응",
        "required_groups": {
            "minor_visible_mishap",
            "brief_gaze_break_face_cue",
            "concrete_repair_action",
            "peer_acceptance_response",
        },
        "required_fields": {
            "minor_mishap_phrase",
            "gaze_break_face_cue_phrase",
            "repair_action_phrase",
            "peer_acceptance_phrase",
        },
    },
    "verified_safety_relief": {
        "exact_term": "안전 확인 뒤 안도",
        "required_groups": {
            "prior_risk_marker",
            "explicit_safety_verification",
            "visible_tension_release",
            "post_verification_consequence",
        },
        "required_fields": {
            "prior_risk_phrase",
            "safety_verification_phrase",
            "main_subject_check_eyeline_phrase",
            "tension_release_phrase",
            "post_verification_phrase",
        },
    },
}


class PhotoAffectVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {
            profile["id"]: profile for profile in cls.registry["profiles"]
        }

    @staticmethod
    def source_rows(text: str) -> list[dict]:
        return [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            }
        ]

    def test_registry_profiles_are_narrow_context_bound_contracts(self) -> None:
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertFalse(
            [error for error in errors if "visual profile index registry_sha256" not in error],
            errors,
        )

        broad_terms = {
            "smile",
            "happy",
            "happiness",
            "relief",
            "confusion",
            "embarrassment",
            "미소",
            "행복",
            "안도",
            "혼란",
            "당황",
        }
        for profile_id, contract in PROFILE_CONTRACTS.items():
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                activation = profile["activation"]
                self.assertEqual(profile["category"], "context_bound_affect_display")
                self.assertTrue(activation["requires_adult_character"])
                self.assertTrue(
                    activation["semantic_discovery_requires_component_evidence"]
                )
                self.assertTrue(
                    broad_terms.isdisjoint(
                        {term.casefold() for term in activation["exact_terms"]}
                    )
                )
                components = profile["semantics"]["component_semantics"]
                self.assertEqual(
                    set(components["required_group_ids"]),
                    contract["required_groups"],
                )
                self.assertEqual(
                    components["minimum_component_groups"],
                    len(contract["required_groups"]),
                )
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    contract["required_fields"],
                )
                self.assertEqual(
                    set(profile["evidence_requirements"]),
                    contract["required_fields"],
                )
                self.assertGreaterEqual(len(profile["render_gates"]), 4)
                self.assertTrue(profile["reject_substitutes"])

    def test_exact_composite_terms_harden_but_components_stay_optional(self) -> None:
        for profile_id, contract in PROFILE_CONTRACTS.items():
            profile = self.profiles[profile_id]
            with self.subTest(profile_id=profile_id, lane="exact"):
                hard = prompt_generator.candidate_pack_auto_visual_obligation_matches(
                    self.registry,
                    self.source_rows(f"성인 인물의 {contract['exact_term']} 장면"),
                )
                self.assertIn(profile_id, hard)
                optional = prompt_generator.candidate_pack_auto_visual_concept_matches(
                    self.registry,
                    self.source_rows(f"성인 인물의 {contract['exact_term']} 장면"),
                )
                self.assertNotIn(profile_id, optional)

            groups = profile["semantics"]["component_semantics"]["groups"]
            component_text = "; ".join(group["any_terms"][0] for group in groups)
            with self.subTest(profile_id=profile_id, lane="component"):
                hard = prompt_generator.candidate_pack_auto_visual_obligation_matches(
                    self.registry,
                    self.source_rows(component_text),
                )
                self.assertNotIn(profile_id, hard)
                optional = prompt_generator.candidate_pack_auto_visual_concept_matches(
                    self.registry,
                    self.source_rows(component_text),
                )
                self.assertIn(profile_id, optional)
                self.assertTrue(
                    all(
                        row["match_kind"] == "component_semantics"
                        for row in optional[profile_id]
                    )
                )

    def test_broad_emotion_words_do_not_create_hard_obligations(self) -> None:
        broad_requests = [
            "성인 인물의 미소",
            "성인 인물이 행복해 보이는 사진",
            "성인 인물의 혼란",
            "성인 인물의 당황",
            "성인 인물의 안도",
            "an adult with a relieved smile",
        ]
        affect_ids = set(PROFILE_CONTRACTS)
        for request in broad_requests:
            with self.subTest(request=request):
                hard = prompt_generator.candidate_pack_auto_visual_obligation_matches(
                    self.registry,
                    self.source_rows(request),
                )
                self.assertTrue(affect_ids.isdisjoint(hard))

    def test_observed_render_substitutes_are_encoded_for_future_packs(self) -> None:
        achievement = self.profiles["achievement_reward_smile"]
        self.assertIn(
            "camera_facing_gaze_at_viewer",
            achievement["reject_substitutes"],
        )
        self.assertIn(
            "still_gripping_or_operating_control",
            achievement["reject_substitutes"],
        )
        self.assertIn("not at the viewer", achievement["composition_instruction"])

        uncertainty = self.profiles["decision_uncertainty_display"]
        self.assertIn(
            "impossible_simultaneous_split_gaze",
            uncertainty["reject_substitutes"],
        )
        self.assertIn(
            "cannot show eyes looking in two directions at once",
            uncertainty["composition_instruction"],
        )

        relief = self.profiles["verified_safety_relief"]
        self.assertIn(
            "main_subject_check_eyeline_phrase",
            relief["required_evidence_fields"],
        )
        self.assertIn(
            "colleague_only_verification",
            relief["reject_substitutes"],
        )
        self.assertIn(
            "main adult looks directly at the colleague being checked",
            relief["evidence_requirements"][
                "main_subject_check_eyeline_phrase"
            ]["must_mention_any"],
        )

    def test_exact_terms_materialize_candidate_pack_render_gates(self) -> None:
        data = {prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY: self.registry}
        moe_response = {
            "enabled": True,
            "render_qualification": {"required_hard_gates": ["adult_role_identity"]},
        }
        for profile_id, contract in PROFILE_CONTRACTS.items():
            with self.subTest(profile_id=profile_id):
                result = {
                    "provenance": {
                        "concept_lock": [
                            f"Photorealistic adult scene with {contract['exact_term']}"
                        ]
                    }
                }
                materialized = prompt_generator.candidate_pack_visual_obligations(
                    data,
                    result,
                    {},
                    moe_response,
                )
                self.assertIsNotNone(materialized)
                obligation = next(
                    row
                    for row in materialized["obligations"]
                    if row["id"] == profile_id
                )
                self.assertEqual(
                    set(obligation["prompt_binding"]["required_evidence_fields"]),
                    contract["required_fields"],
                )
                gate_ids = {gate["id"] for gate in obligation["render_gates"]}
                self.assertEqual(gate_ids, set(materialized["required_hard_gates"]))

    def test_affect_research_shard_is_three_source_per_topic_and_hash_bound(self) -> None:
        manifest = json.loads(
            (RESEARCH_DIR / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["schema_version"], "photo-research-evidence-shards/v1")
        self.assertEqual(manifest["research_scope"], "context_bound_affect_display")
        self.assertEqual(manifest["logical_row_count"], 15)
        self.assertEqual(manifest["topic_count"], 5)
        self.assertEqual(manifest["rows_per_topic"], 3)
        self.assertEqual(len(manifest["shards"]), 1)

        shard = manifest["shards"][0]
        raw = (RESEARCH_DIR / shard["file"]).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), shard["sha256"])
        rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line]
        self.assertEqual(len(rows), 15)
        self.assertEqual(len({row["id"] for row in rows}), 15)
        rows_by_id = {row["id"]: row for row in rows}
        self.assertEqual(
            list(dict.fromkeys(row["topic_id"] for row in rows)),
            shard["topic_ids"],
        )

        for topic_id in shard["topic_ids"]:
            topic_rows = [row for row in rows if row["topic_id"] == topic_id]
            matrices = [row for row in topic_rows if row["record_role"] == "topic_matrix"]
            supports = [
                row for row in topic_rows if row["record_role"] == "independent_source"
            ]
            with self.subTest(topic_id=topic_id):
                self.assertEqual(len(topic_rows), 3)
                self.assertEqual(len(matrices), 1)
                self.assertEqual(len(supports), 2)
                matrix = matrices[0]
                self.assertEqual(
                    set(matrix["synthesis_evidence_ids"]),
                    {row["id"] for row in supports},
                )
                self.assertEqual(
                    set(matrix["candidate_definitions"]),
                    set(matrix["candidate_ids"]),
                )
                self.assertEqual(
                    set(matrix["photographic_evidence_definitions"]),
                    set(matrix["photographic_evidence"]),
                )
                self.assertEqual(
                    [row["mechanism"] for row in matrix["mechanism_provenance"]],
                    matrix["mechanisms"],
                )
                self.assertTrue(
                    all(
                        set(row["candidate_ids"]) <= set(matrix["candidate_ids"])
                        for row in supports
                    )
                )
                for provenance in matrix["mechanism_provenance"]:
                    self.assertTrue(provenance["evidence_ids"])
                    self.assertTrue(
                        set(provenance["evidence_ids"]) <= set(rows_by_id)
                    )
                    self.assertTrue(
                        all(
                            rows_by_id[evidence_id]["topic_id"] == topic_id
                            for evidence_id in provenance["evidence_ids"]
                        )
                    )

    def test_five_arm_pixel_cases_are_seeded_gate_complete_and_consensus_bound(
        self,
    ) -> None:
        rows = [
            json.loads(line)
            for line in PIXEL_CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line
        ]
        self.assertEqual(len(rows), 5)
        self.assertEqual({row["arm_id"] for row in rows}, {f"arm-0{i}" for i in range(1, 6)})
        self.assertEqual({row["profile_id"] for row in rows}, set(PROFILE_CONTRACTS))
        self.assertEqual(len({row["seed"] for row in rows}), 5)
        self.assertEqual(len({row["case_id"] for row in rows}), 5)
        self.assertEqual(len({row["concept"] for row in rows}), 5)

        for row in rows:
            with self.subTest(case_id=row["case_id"]):
                self.assertEqual(
                    row["schema_version"],
                    "photo-affect-pixel-test-case/v1",
                )
                profile = self.profiles[row["profile_id"]]
                expected_gate_ids = {
                    gate["id"] for gate in profile["render_gates"]
                }
                self.assertEqual(
                    set(row["expected_hard_gate_ids"]),
                    expected_gate_ids,
                )
                self.assertIn(
                    row["exact_activation_term"].casefold(),
                    {
                        term.casefold()
                        for term in profile["activation"]["exact_terms"]
                    },
                )

                self_passed = set(row["self_passed_gate_ids"])
                blind_passed = set(row["blind_passed_gate_ids"])
                self.assertLessEqual(self_passed, expected_gate_ids)
                self.assertLessEqual(blind_passed, expected_gate_ids)
                strict_failed = expected_gate_ids - (self_passed & blind_passed)
                self.assertEqual(
                    set(row["strict_consensus_failed_gate_ids"]),
                    strict_failed,
                )
                self.assertEqual(
                    row["strict_pixel_status"],
                    "pass" if not strict_failed else "fail",
                )
                self.assertRegex(row["result_sha256"], r"^[0-9a-f]{64}$")
                self.assertTrue(row["prompt_path"].startswith("artifacts/"))
                self.assertTrue(row["result_image_path"].startswith("artifacts/"))


if __name__ == "__main__":
    unittest.main()
