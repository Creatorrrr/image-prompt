from __future__ import annotations

import hashlib
import json
import struct
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
FIVE_ARM_FIXTURE_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "adult_appeal_semantics_five_arm_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_CONTRACTS = {
    "self_possessed_sensual_presence": {
        "exact_term": "자기주도적 관능미",
        "required_groups": {
            "adult_self_directed_agency",
            "grounded_composed_posture",
            "controlled_face_gaze",
            "material_body_relation",
        },
        "gate_ids": {
            "vo_self_possessed_adult_agency",
            "vo_self_possessed_grounded_posture",
            "vo_self_possessed_controlled_face",
            "vo_self_possessed_material_relation",
        },
    },
    "target_directed_seductive_display": {
        "exact_term": "상대지향적 유혹 표현",
        "required_groups": {
            "same_adult_target",
            "coordinated_target_orientation",
            "concrete_invitation_action",
            "visible_target_consequence",
        },
        "gate_ids": {
            "vo_target_seduction_same_adult_target",
            "vo_target_seduction_coordinated_orientation",
            "vo_target_seduction_invitation_action",
            "vo_target_seduction_visible_consequence",
        },
    },
    "playful_flirtation_interaction": {
        "exact_term": "장난스러운 플러팅 상호작용",
        "required_groups": {
            "adult_interaction_pair",
            "approach_withdrawal_event",
            "restrained_playful_face_action",
            "same_target_response",
        },
        "gate_ids": {
            "vo_playful_flirt_adult_pair",
            "vo_playful_flirt_approach_withdrawal",
            "vo_playful_flirt_face_action",
            "vo_playful_flirt_recipient_response",
        },
    },
    "controlled_languid_movement_display": {
        "exact_term": "통제된 나른한 움직임",
        "required_groups": {
            "unfinished_motion_phase",
            "stable_support_control",
            "alert_task_attention",
            "coherent_motion_lag",
        },
        "gate_ids": {
            "vo_languid_motion_unfinished_phase",
            "vo_languid_motion_stable_support",
            "vo_languid_motion_alert_attention",
            "vo_languid_motion_directional_lag",
        },
    },
    "decadent_languor_environment": {
        "exact_term": "퇴폐적 나른함 환경",
        "required_groups": {
            "former_luxury_material",
            "visible_decline_or_wear",
            "after_event_residue",
            "alert_adult_unfinished_action",
        },
        "gate_ids": {
            "vo_decadent_languor_former_luxury",
            "vo_decadent_languor_material_decline",
            "vo_decadent_languor_after_event",
            "vo_decadent_languor_alert_action",
        },
    },
}


EXPECTED_CANDIDATES = {
    "expression": {
        "engaged_lowered_lid_target_gaze",
        "small_asymmetric_closed_lip_target_smile",
    },
    "gaze_engagement": {
        "same_adult_target_coordinated_gaze",
        "returned_gaze_mid_partial_turn",
    },
    "motion": {"slow_controlled_transition_phase"},
    "relational_action": {
        "approach_withdrawal_object_exchange",
        "threshold_invitation_with_adult_response",
    },
    "partner_framing": {"same_adult_target_response_two_shot"},
    "garment_detail": {
        "bias_cut_body_skimming_drape",
        "selective_open_back_stable_front_coverage",
        "stride_revealed_slit",
    },
    "body_pose": {
        "open_grounded_self_directed_stance",
        "controlled_three_quarter_weight_shift",
    },
    "surface_material": {"opaque_satin_specular_flow_surface"},
    "aftermath_trace": {"faded_luxury_after_event_trace"},
}


class PhotoAdultAppealVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.candidates = {
            slot: {row["id"]: row for row in rows}
            for slot, rows in cls.tags["slots"].items()
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

    def hard_matches(self, text: str) -> set[str]:
        return set(
            prompt_generator.candidate_pack_auto_visual_obligation_matches(
                self.registry,
                self.source_rows(text),
            )
        )

    def test_profiles_are_narrow_adult_component_contracts(self) -> None:
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertFalse(errors, errors)

        for profile_id, contract in PROFILE_CONTRACTS.items():
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                activation = profile["activation"]
                self.assertTrue(activation["requires_adult_character"])
                self.assertTrue(
                    activation["semantic_discovery_requires_component_evidence"]
                )
                self.assertEqual(
                    profile["runtime_expression"]["default_mode"],
                    "definition_only",
                )
                self.assertEqual(profile["runtime_expression"]["prompt_label_terms"], [])
                self.assertTrue(
                    set(activation["exact_terms"])
                    <= set(profile["runtime_expression"]["forbidden_prompt_terms"])
                )
                self.assertTrue(
                    set(activation["exact_terms"])
                    <= set(profile["runtime_expression"]["runtime_forbidden_labels"])
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
                    {gate["id"] for gate in profile["render_gates"]},
                    contract["gate_ids"],
                )
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertTrue(profile["reject_substitutes"])

    def test_exact_composites_activate_only_their_profile(self) -> None:
        for profile_id, contract in PROFILE_CONTRACTS.items():
            with self.subTest(profile_id=profile_id):
                self.assertEqual(
                    self.hard_matches(
                        f"명백한 성인 인물을 위한 {contract['exact_term']} 사진"
                    ),
                    {profile_id},
                )

    def test_broad_labels_and_single_cues_remain_fail_closed(self) -> None:
        broad_requests = [
            "성인 여성의 색기",
            "성인 인물의 관능미",
            "요염한 성인 초상",
            "농염한 성인 인물",
            "매혹적이고 고혹적인 성인",
            "sultry adult portrait",
            "alluring adult fashion",
            "flirtatious direct eye contact",
            "coquette ribbon aesthetic",
            "sleepy half-lidded eyes",
            "over-the-shoulder pose",
            "red-light gothic glamour",
        ]
        new_ids = set(PROFILE_CONTRACTS)
        for text in broad_requests:
            with self.subTest(text=text):
                self.assertTrue(self.hard_matches(text).isdisjoint(new_ids), text)

    def test_component_language_is_optional_not_hard(self) -> None:
        for profile_id in PROFILE_CONTRACTS:
            profile = self.profiles[profile_id]
            groups = profile["semantics"]["component_semantics"]["groups"]
            text = "unmistakably adult subject; " + "; ".join(
                group["any_terms"][0] for group in groups
            )
            with self.subTest(profile_id=profile_id):
                self.assertNotIn(profile_id, self.hard_matches(text))
                optional = prompt_generator.candidate_pack_auto_visual_concept_matches(
                    self.registry,
                    self.source_rows(text),
                )
                self.assertIn(profile_id, optional)
                self.assertTrue(
                    all(
                        row["match_kind"] == "component_semantics"
                        for row in optional[profile_id]
                    )
                )

    def test_candidate_pack_contains_literal_non_intent_atoms(self) -> None:
        for slot, expected_ids in EXPECTED_CANDIDATES.items():
            with self.subTest(slot=slot):
                self.assertTrue(expected_ids <= set(self.candidates[slot]))

        sleepy = self.candidates["expression"]["engaged_lowered_lid_target_gaze"]
        self.assertIn("distinct from sleepy", sleepy["embedding_text"])
        smile = self.candidates["expression"][
            "small_asymmetric_closed_lip_target_smile"
        ]
        self.assertIn("does not by itself prove", smile["embedding_text"])
        invitation = self.candidates["relational_action"][
            "threshold_invitation_with_adult_response"
        ]
        self.assertIn("does not establish consent", invitation["embedding_text"])
        motion = self.candidates["motion"]["slow_controlled_transition_phase"]
        self.assertIn("distinct from a finished pose", motion["embedding_text"])

    def test_research_evidence_is_approved_and_candidate_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        evidence_rows = [
            row for row in rows if row["id"].startswith("adult_appeal_semantics_")
        ]
        self.assertEqual(len(evidence_rows), 9)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in evidence_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["status"], "approved")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_exact_profiles_materialize_their_pixel_gate_sets(self) -> None:
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
                            f"unmistakably adult photo with {contract['exact_term']}"
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
                    {gate["id"] for gate in obligation["render_gates"]},
                    contract["gate_ids"],
                )

    def test_five_arm_cases_bind_packs_prompts_reference_and_render_evidence(
        self,
    ) -> None:
        rows = [
            json.loads(line)
            for line in FIVE_ARM_FIXTURE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 5)
        self.assertEqual({row["arm_id"] for row in rows}, {f"arm-{n:02d}" for n in range(1, 6)})
        self.assertEqual({row["profile_id"] for row in rows}, set(PROFILE_CONTRACTS))
        self.assertEqual(len({row["seed"] for row in rows}), 5)
        self.assertEqual(
            {row["schema_version"] for row in rows},
            {"photo-adult-appeal-semantic-pixel-case/v2"},
        )
        self.assertEqual(len({row["blind_alias"] for row in rows}), 5)

        parent_review_paths = {row["parent_pixel_review_path"] for row in rows}
        self.assertEqual(len(parent_review_paths), 1)
        parent_review = json.loads(
            (ROOT / parent_review_paths.pop()).read_text(encoding="utf-8")
        )
        self.assertEqual(
            parent_review["blinding_integrity"],
            "partial_masking_not_strict_blind",
        )
        self.assertEqual(
            parent_review["aggregate"]["strict_consensus_profile_passes"],
            "5/5",
        )
        parent_by_arm = {
            result["arm_id"]: result
            for result in parent_review["decoded_results"]
        }

        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in rows:
            with self.subTest(arm_id=row["arm_id"]):
                profile_id = row["profile_id"]
                profile = self.profiles[profile_id]
                self.assertEqual(
                    row["exact_activation_term"],
                    PROFILE_CONTRACTS[profile_id]["exact_term"],
                )
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertGreaterEqual(len(row["concept"].split()), 12)

                for path_field, hash_field in (
                    ("request_envelope_path", "request_envelope_sha256"),
                    ("authorial_core_path", "authorial_core_sha256"),
                    ("candidate_pack_path", "candidate_pack_sha256"),
                    ("prompt_path", "prompt_sha256"),
                    ("reference_image_path", "reference_sha256"),
                    ("result_image_path", "result_sha256"),
                    ("thumbnail_path", "thumbnail_sha256"),
                ):
                    path = ROOT / row[path_field]
                    self.assertTrue(path.is_file(), path)
                    self.assertEqual(
                        hashlib.sha256(path.read_bytes()).hexdigest(),
                        row[hash_field],
                    )

                pack_data = json.loads(
                    (ROOT / row["candidate_pack_path"]).read_text(encoding="utf-8")
                )
                pack = pack_data[0] if isinstance(pack_data, list) else pack_data
                self.assertEqual(pack["contract_version"], "photo-candidate-pack/v6")
                self.assertEqual(pack["pack_id"], row["pack_id"])
                visual = pack["visual_obligations"]
                self.assertTrue(visual["strict_gate_set"])
                obligation = next(
                    item
                    for item in visual["obligations"]
                    if item["id"] == profile_id
                )
                self.assertEqual(
                    {gate["id"] for gate in obligation["render_gates"]},
                    set(row["expected_hard_gate_ids"]),
                )
                self.assertEqual(
                    set(row["expected_hard_gate_ids"]),
                    PROFILE_CONTRACTS[profile_id]["gate_ids"],
                )

                prompt_audit = json.loads(
                    (ROOT / row["prompt_audit_path"]).read_text(encoding="utf-8")
                )
                self.assertEqual(row["prompt_audit_status"], "pass")
                self.assertEqual(prompt_audit["status"], "pass")
                self.assertEqual(prompt_audit["pack_id"], row["pack_id"])
                final_prompt = (ROOT / row["prompt_path"]).read_text(
                    encoding="utf-8"
                )
                for forbidden in profile["runtime_expression"][
                    "runtime_forbidden_labels"
                ]:
                    self.assertNotIn(forbidden.casefold(), final_prompt.casefold())

                runtime_audit = json.loads(
                    (ROOT / row["runtime_audit_path"]).read_text(encoding="utf-8")
                )
                self.assertEqual(row["runtime_audit_status"], "pass")
                self.assertEqual(runtime_audit["status"], "pass")
                self.assertEqual(runtime_audit["pack_id"], row["pack_id"])
                self.assertTrue((ROOT / row["generation_attempt_path"]).is_file())

                self.assertEqual(row["reference_image_role"], "facial_appearance_only")
                self.assertEqual(
                    row["reference_delivery_status"],
                    "available_concrete_local_path",
                )
                self.assertEqual(
                    row["generation_status"],
                    "generated_reference_qualified",
                )
                result_bytes = (ROOT / row["result_image_path"]).read_bytes()
                self.assertTrue(result_bytes.startswith(b"\x89PNG\r\n\x1a\n"))
                width, height = struct.unpack(">II", result_bytes[16:24])
                self.assertEqual(
                    {"width": width, "height": height},
                    row["result_dimensions"],
                )

                self_review = json.loads(
                    (ROOT / row["self_pixel_review_path"]).read_text(encoding="utf-8")
                )
                self_gates = self_review.get("hard_gates") or self_review.get("gates")
                self.assertEqual(
                    {
                        gate.get("id") or gate.get("gate_id")
                        for gate in self_gates
                    },
                    set(row["expected_hard_gate_ids"]),
                )
                self.assertTrue(
                    all(gate["status"] == "pass" for gate in self_gates)
                )

                parent_result = parent_by_arm[row["arm_id"]]
                self.assertEqual(parent_result["alias"], row["blind_alias"])
                self.assertEqual(
                    {gate["id"] for gate in parent_result["gates"]},
                    set(row["expected_hard_gate_ids"]),
                )
                self.assertTrue(
                    all(
                        gate["parent_status"] == "pass"
                        for gate in parent_result["gates"]
                    )
                )
                self.assertEqual(parent_result["strict_consensus"], "pass")
                self.assertEqual(
                    set(row["strict_consensus_gate_statuses"]),
                    set(row["expected_hard_gate_ids"]),
                )
                self.assertTrue(
                    all(
                        status == "pass"
                        for status in row["strict_consensus_gate_statuses"].values()
                    )
                )
                self.assertEqual(
                    row["blind_observation_status"],
                    "complete_partial_masking",
                )
                self.assertEqual(row["strict_pixel_status"], "pass")
                self.assertEqual(row["identity"], "not_evaluated")
                self.assertEqual(row["user_judgment"], "pending")


if __name__ == "__main__":
    unittest.main()
