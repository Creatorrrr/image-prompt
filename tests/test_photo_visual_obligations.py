from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
WRAPPER_PATH = SCRIPT_DIR / "generate_photo_prompt.py"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
ROUTING_FIXTURE_PATH = (
    ROOT / "tests" / "fixtures" / "photo_prompt" / "visual_obligation_routing_v1.jsonl"
)
ROUTING_HOLDOUT_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "visual_obligation_routing_holdout_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_composed_prompt  # noqa: E402
import audit_image_render_request  # noqa: E402
import audit_moe_render_review  # noqa: E402
import prompt_generator  # noqa: E402
import record_image_run  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


class PhotoVisualObligationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)

    def run_wrapper(self, *args: str) -> dict:
        completed = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertIsInstance(payload, list)
        self.assertEqual(len(payload), 1)
        return payload[0]

    def moe_pack(self, concept: str, *, seed: int = 1401, extra: tuple[str, ...] = ()) -> dict:
        return self.run_wrapper(
            "--selection-mode",
            "rule",
            "--seed",
            str(seed),
            "--emit-candidate-pack",
            "--concept-lock",
            concept,
            *extra,
        )

    @staticmethod
    def visual_evidence_for_obligation(obligation: dict) -> dict[str, str]:
        requirements = obligation.get("evidence_requirements", {})
        bindings = obligation.get("bindings", {})
        evidence: dict[str, str] = {}
        for index, field in enumerate(
            obligation["prompt_binding"]["required_evidence_fields"],
            start=1,
        ):
            if field in bindings:
                evidence[field] = bindings[field]
                continue
            anchors = requirements.get(field, {}).get("must_mention_any", [])
            anchor = anchors[0] if anchors else field.replace("_phrase", "").replace("_", " ")
            evidence[field] = (
                f"{anchor} remains concretely readable in component {index} of this frame"
            )
        return evidence

    @staticmethod
    def prompt_for_obligation(obligation: dict, evidence: dict[str, str]) -> str:
        expression = obligation.get("runtime_expression", {})
        labels = expression.get("prompt_label_terms", [])
        prefix = f"{labels[0]}. " if expression.get("default_mode") == "label_plus_definition" else ""
        return prefix + "; ".join(evidence.values()) + "."

    def assert_routing_fixture(self, path: Path) -> None:
        cases = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for case in cases:
            with self.subTest(fixture=path.name, case=case["id"]):
                source_rows = [
                    {
                        "source": "concept_lock",
                        "text": case["text"],
                        "polarity": "required",
                        "priority": "critical",
                        "mandatory": True,
                    }
                ]
                hard_matches = prompt_generator.candidate_pack_auto_visual_obligation_matches(
                    self.registry,
                    source_rows,
                )
                concept_matches = prompt_generator.candidate_pack_auto_visual_concept_matches(
                    self.registry,
                    source_rows,
                )
                self.assertEqual(
                    sorted(hard_matches),
                    sorted(case["expected_profile_ids"]),
                )
                self.assertEqual(
                    sorted(concept_matches),
                    sorted(case["expected_candidate_profile_ids"]),
                )

                moe_response = {
                    "enabled": True,
                    "render_qualification": {
                        "required_hard_gates": ["adult_role_identity"]
                    },
                }
                data = {prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY: self.registry}
                result = {"provenance": {"concept_lock": [case["text"]]}}
                materialized = prompt_generator.candidate_pack_visual_obligations(
                    data,
                    result,
                    {},
                    moe_response,
                )
                actual_ids = (
                    [item["id"] for item in materialized["obligations"]]
                    if materialized is not None
                    else []
                )
                self.assertEqual(
                    sorted(actual_ids),
                    sorted(case["expected_profile_ids"]),
                )
                concepts = prompt_generator.candidate_pack_visual_concept_candidates(
                    data,
                    result,
                    {},
                    moe_response,
                    materialized,
                )
                actual_candidate_ids = (
                    [
                        candidate["opt_in_contract"]["obligation"]["id"]
                        for candidate in concepts["candidates"]
                    ]
                    if concepts is not None
                    else []
                )
                self.assertEqual(
                    sorted(actual_candidate_ids),
                    sorted(case["expected_candidate_profile_ids"]),
                )
                prompt_generator.candidate_pack_merge_visual_render_gates(
                    moe_response,
                    materialized,
                )
                if materialized is not None:
                    self.assertTrue(
                        set(materialized["required_hard_gates"])
                        <= set(
                            moe_response["render_qualification"]["required_hard_gates"]
                        )
                    )

    def test_registry_and_request_scoped_routing_fixture(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])
        self.assert_routing_fixture(ROUTING_FIXTURE_PATH)

    def test_frozen_visual_concept_routing_holdout(self):
        self.assert_routing_fixture(ROUTING_HOLDOUT_PATH)

    def test_named_challenge_materializes_prompt_and_render_obligations(self):
        pack = self.moe_pack(
            "Photorealistic explicitly nonsexual behavior-led moe scene of an adult "
            "woman, mid-twenties or older, doing a bubble tea challenge"
        )
        visual = pack["visual_obligations"]
        self.assertEqual(audit_composed_prompt.audit_v4_authorial_pack(pack), [])
        self.assertEqual(visual["contract_version"], "photo-visual-obligations/v1")
        self.assertTrue(visual["strict_gate_set"])
        self.assertEqual(
            [item["id"] for item in visual["obligations"]],
            ["hands_free_supported_drink_load"],
        )
        visual_gates = visual["required_hard_gates"]
        qualification = pack["moe_response"]["render_qualification"]
        self.assertEqual(qualification["request_specific_hard_gates"], visual_gates)
        self.assertTrue(set(visual_gates) <= set(qualification["required_hard_gates"]))

        ordinary = self.moe_pack(
            "Photorealistic explicitly nonsexual behavior-led moe cafe portrait of an "
            "adult woman, mid-twenties or older, holding bubble tea",
            seed=1402,
        )
        self.assertNotIn("visual_obligations", ordinary)

    def test_project_glossary_absolute_territory_expands_to_thigh_geometry(self):
        pack = self.moe_pack(
            "성인 여성의 일본 서브컬처 절대공역 모에 사진",
            seed=1405,
        )
        visual = pack["visual_obligations"]
        self.assertEqual(
            [item["id"] for item in visual["obligations"]],
            ["inner_thigh_negative_space"],
        )
        obligation = visual["obligations"][0]
        self.assertIn("actual upper inner-thigh contours", obligation["composition_instruction"])
        self.assertIn("legs remain adducted", obligation["composition_instruction"])
        self.assertEqual(
            obligation["prompt_binding"]["required_evidence_fields"],
            [
                "close_leg_geometry_phrase",
                "inner_thigh_boundary_phrase",
                "negative_space_phrase",
                "appeal_emphasis_phrase",
                "false_gap_exclusion_phrase",
                "thumbnail_crop_phrase",
            ],
        )
        self.assertIn("wide_stance_space", obligation["reject_substitutes"])
        self.assertIn("skirt_or_coat_opening", obligation["reject_substitutes"])
        self.assertEqual(
            {gate["id"] for gate in obligation["render_gates"]},
            {
                "vo_inner_thigh_legs_close",
                "vo_inner_thigh_true_negative_space",
                "vo_inner_thigh_attractive_composition",
                "vo_inner_thigh_not_false_gap",
                "vo_inner_thigh_thumbnail_legibility",
            },
        )

        negated = self.moe_pack(
            "성인 여성의 절대공역 없는 일본 서브컬처 모에 사진",
            seed=1406,
        )
        self.assertNotIn("visual_obligations", negated)

    def test_project_glossary_alias_cannot_own_multiple_profiles(self):
        mutated = copy.deepcopy(self.registry)
        mutated["profiles"][1]["activation"]["project_glossary_aliases"] = [
            "절대공역"
        ]
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "registry.json"
            registry_path.write_text(
                json.dumps(mutated, ensure_ascii=False),
                encoding="utf-8",
            )
            errors: list[str] = []
            validate_photo_prompt_dictionary.validate_visual_obligation_registry(
                registry_path,
                errors,
            )
        self.assertTrue(
            any("already owned by inner_thigh_negative_space" in error for error in errors),
            errors,
        )

    def test_prepack_visual_intent_is_hash_bound_and_source_grounded(self):
        source_text = (
            "The adult woman keeps her legs close while a narrow user-defined opening "
            "between the actual upper inner-thigh contours remains visible."
        )
        visual_intent = {
            "contract_version": "photo-visual-intent/v1",
            "provenance": "agent_prepack",
            "obligations": [
                {
                    "profile_id": "inner_thigh_negative_space",
                    "source": "requesting_user_definition",
                    "scope": "request_only",
                    "source_text": source_text,
                    "bindings": {
                        "close_leg_geometry_phrase": "her knees remain side by side",
                        "false_gap_exclusion_phrase": "not a wide stance or garment opening",
                    },
                }
            ],
        }
        pack = self.moe_pack(
            "Photorealistic explicitly nonsexual behavior-led moe scene of an adult "
            "woman, mid-twenties or older",
            seed=1403,
            extra=(
                "--additional-requirement",
                source_text,
                "--visual-intent-json",
                json.dumps(visual_intent, ensure_ascii=False),
            ),
        )
        visual = pack["visual_obligations"]
        self.assertEqual(audit_composed_prompt.audit_v4_authorial_pack(pack), [])
        obligation = visual["obligations"][0]
        self.assertEqual(obligation["id"], "inner_thigh_negative_space")
        self.assertEqual(
            obligation["activation"]["source"],
            "requesting_user_definition",
        )
        self.assertEqual(
            obligation["bindings"]["close_leg_geometry_phrase"],
            "her knees remain side by side",
        )
        self.assertRegex(visual["source_visual_intent_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(
            pack["visual_intent"]["canonical_sha256"],
            visual["source_visual_intent_sha256"],
        )
        required_fields = obligation["prompt_binding"]["required_evidence_fields"]
        self.assertEqual(set(required_fields), set(obligation["evidence_requirements"]))
        composed_evidence = self.visual_evidence_for_obligation(obligation)
        composed_prompt = self.prompt_for_obligation(obligation, composed_evidence)
        composed = {
            "prompt_en": composed_prompt,
            "visual_obligation_evidence": {
                obligation["id"]: composed_evidence,
            },
        }
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(
                pack,
                composed,
                composed_prompt,
            ),
            [],
        )
        tampered_pack = copy.deepcopy(pack)
        tampered_pack["visual_intent"]["obligations"][0]["source_text"] += " changed"
        tampered_failures = audit_composed_prompt.audit_visual_obligations(
            tampered_pack,
            composed,
            composed_prompt,
        )
        self.assertIn(
            "visual_intent_integrity",
            {failure["check"] for failure in tampered_failures},
        )

        ungrounded = copy.deepcopy(visual_intent)
        ungrounded["obligations"][0]["source_text"] = "A sentence absent from the request."
        completed = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--selection-mode",
                "rule",
                "--seed",
                "1404",
                "--emit-candidate-pack",
                "--concept-lock",
                "Photorealistic explicitly nonsexual adult behavior-led moe portrait",
                "--visual-intent-json",
                json.dumps(ungrounded, ensure_ascii=False),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("source_text must exactly match", completed.stderr)

    def test_composed_prompt_must_bind_every_distinct_visual_duty(self):
        profile = prompt_generator.visual_obligation_profile_by_id(
            self.registry,
            "composite_overwhelmed_expression",
        )
        self.assertIsNotNone(profile)
        fields = list(profile["required_evidence_fields"])
        evidence = {
            field: f"visible {field.replace('_phrase', '').replace('_', ' ')} cue {index}"
            for index, field in enumerate(fields, start=1)
        }
        gates = copy.deepcopy(profile["render_gates"])
        pack = {
            "visual_obligations": {
                "enabled": True,
                "contract_version": "photo-visual-obligations/v1",
                "strict_gate_set": True,
                "obligations": [
                    {
                        "id": profile["id"],
                        "prompt_binding": {
                            "required_evidence_fields": fields,
                            "minimum_distinct_evidence_phrases": len(fields),
                            "prompt_evidence_must_be_literal": True,
                        },
                        "render_gates": gates,
                        "bindings": {
                            "external_tongue_tip_phrase": evidence[
                                "external_tongue_tip_phrase"
                            ]
                        },
                    }
                ],
                "required_hard_gates": [gate["id"] for gate in gates],
            }
        }
        prompt_en = "; ".join(evidence.values()) + "."
        composed = {
            "prompt_en": prompt_en,
            "visual_obligation_evidence": {profile["id"]: evidence},
        }
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(pack, composed, prompt_en),
            [],
        )

        missing = copy.deepcopy(composed)
        missing["visual_obligation_evidence"][profile["id"]].pop(
            "external_tongue_tip_phrase"
        )
        failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            missing,
            prompt_en,
        )
        checks = {failure["check"] for failure in failures}
        self.assertIn("visual_obligation_evidence", checks)
        self.assertIn("visual_obligation_hard_binding", checks)

    def test_indirect_components_surface_optional_candidate_and_selection_promotes_gates(self):
        pack = self.moe_pack(
            "Photorealistic explicitly nonsexual behavior-led moe scene of an adult "
            "woman, mid-twenties or older, with knees together while a triangular "
            "opening remains between the upper inner thighs",
            seed=1410,
        )
        self.assertNotIn("visual_obligations", pack)
        concepts = pack["visual_concept_candidates"]
        self.assertEqual(concepts["contract_version"], "photo-visual-concepts/v1")
        self.assertEqual(concepts["candidate_order"], "seed_shuffled_non_preferential")
        self.assertEqual(len(concepts["candidates"]), 1)
        candidate = concepts["candidates"][0]
        self.assertEqual(candidate["content_form"], "unordered_inspiration_terms")
        self.assertNotIn("score", candidate)
        self.assertNotIn("matched_terms", candidate)
        self.assertNotIn("match_kind", candidate)
        obligation = candidate["opt_in_contract"]["obligation"]
        evidence = self.visual_evidence_for_obligation(obligation)
        prompt_en = self.prompt_for_obligation(obligation, evidence)
        composed = {
            "prompt_en": prompt_en,
            "chosen_visual_concept_ids": [candidate["id"]],
            "visual_obligation_evidence": {obligation["id"]: evidence},
        }
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(pack, composed, prompt_en),
            [],
        )
        effective, failures = (
            audit_composed_prompt.derive_effective_visual_obligation_contract(
                pack,
                composed,
            )
        )
        self.assertEqual(failures, [])
        self.assertEqual(
            [item["id"] for item in effective["obligations"]],
            ["inner_thigh_negative_space"],
        )
        self.assertEqual(
            set(effective["required_hard_gates"]),
            {gate["id"] for gate in obligation["render_gates"]},
        )

        unselected = {
            "prompt_en": "An adult portrait with a neutral standing pose.",
            "chosen_visual_concept_ids": [],
        }
        unselected_effective, unselected_failures = (
            audit_composed_prompt.derive_effective_visual_obligation_contract(
                pack,
                unselected,
            )
        )
        self.assertIsNone(unselected_effective)
        self.assertEqual(unselected_failures, [])
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(
                pack,
                unselected,
                unselected["prompt_en"],
            ),
            [],
        )

        missing_decision = {"prompt_en": unselected["prompt_en"]}
        decision_failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            missing_decision,
            missing_decision["prompt_en"],
        )
        self.assertIn(
            "chosen_visual_concept_ids",
            {failure["check"] for failure in decision_failures},
        )

    def test_semantic_evidence_and_sensitive_runtime_labels_fail_closed(self):
        pack = self.moe_pack(
            "Photorealistic fully clothed nonsexual adult character whose pupils "
            "drift upward asymmetrically while a small rounded open mouth shows "
            "comic composure loss",
            seed=1411,
        )
        candidate = pack["visual_concept_candidates"]["candidates"][0]
        obligation = candidate["opt_in_contract"]["obligation"]
        self.assertEqual(obligation["id"], "composite_overwhelmed_expression")
        evidence = self.visual_evidence_for_obligation(obligation)
        prompt_en = self.prompt_for_obligation(obligation, evidence)
        composed = {
            "prompt_en": prompt_en,
            "chosen_visual_concept_ids": [candidate["id"]],
            "visual_obligation_evidence": {obligation["id"]: evidence},
        }
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(pack, composed, prompt_en),
            [],
        )

        labeled = copy.deepcopy(composed)
        labeled["prompt_en"] = "Ahegao. " + prompt_en
        label_failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            labeled,
            labeled["prompt_en"],
        )
        self.assertIn(
            "visual_obligation_runtime_expression",
            {failure["check"] for failure in label_failures},
        )

        filler = copy.deepcopy(composed)
        first_field = obligation["prompt_binding"]["required_evidence_fields"][0]
        old_phrase = filler["visual_obligation_evidence"][obligation["id"]][first_field]
        filler_phrase = "visible evidence for this required cue"
        filler["visual_obligation_evidence"][obligation["id"]][first_field] = filler_phrase
        filler["prompt_en"] = filler["prompt_en"].replace(old_phrase, filler_phrase)
        filler_failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            filler,
            filler["prompt_en"],
        )
        self.assertIn(
            "visual_obligation_semantic_evidence",
            {failure["check"] for failure in filler_failures},
        )

    def test_selected_visual_concept_binds_runtime_and_render_review(self):
        pack = self.moe_pack(
            "Photorealistic explicitly nonsexual behavior-led moe scene of an adult "
            "woman with knees close and a narrow triangular opening bounded by the "
            "upper inner thighs",
            seed=1412,
        )
        candidate = pack["visual_concept_candidates"]["candidates"][0]
        obligation = candidate["opt_in_contract"]["obligation"]
        evidence = self.visual_evidence_for_obligation(obligation)
        prompt_en = self.prompt_for_obligation(obligation, evidence)
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": prompt_en,
            "negative_en": pack["negative_en"],
            "chosen_visual_concept_ids": [candidate["id"]],
            "visual_obligation_evidence": {obligation["id"]: evidence},
        }
        effective, derivation_failures = (
            audit_composed_prompt.derive_effective_visual_obligation_contract(
                pack,
                composed,
            )
        )
        self.assertEqual(derivation_failures, [])
        effective_sha = audit_composed_prompt.effective_visual_obligation_sha256(
            effective
        )
        runtime_prompt = prompt_en
        if pack["negative_en"] is not None:
            runtime_prompt += f"\nAvoid: {pack['negative_en']}"
        request = {
            "schema_version": "photo-image-render-request/v2",
            "pack_id": pack["pack_id"],
            "runtime_prompt_en": runtime_prompt,
            "runtime_negative_en": pack["negative_en"],
            "effective_visual_contract_sha256": effective_sha,
            "audit_boundary": {
                "composed_prompt_audit_status": "pass",
                "runtime_prompt_audit_status": "not_run",
                "inherits_composed_prompt_pass": False,
            },
            "references": [],
        }
        runtime_audit = audit_image_render_request.audit_image_render_request(
            pack,
            composed,
            request,
        )
        self.assertEqual(runtime_audit["status"], "pass", runtime_audit)
        missing_hash = copy.deepcopy(request)
        missing_hash.pop("effective_visual_contract_sha256")
        missing_hash_audit = audit_image_render_request.audit_image_render_request(
            pack,
            composed,
            missing_hash,
        )
        self.assertEqual(missing_hash_audit["status"], "fail")

        required_gates = list(
            dict.fromkeys(
                pack["moe_response"]["render_qualification"]["required_hard_gates"]
                + effective["required_hard_gates"]
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "candidate.png"
            image_path.write_bytes(b"selected-visual-concept-test-image")
            review = {
                "schema_version": "moe-render-review/v1",
                "pack_id": pack["pack_id"],
                "contract_version": pack["moe_response"]["contract_version"],
                "reviewer": "test pixel reviewer",
                "result_image": str(image_path),
                "result_sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
                "hard_gates": {
                    gate: {
                        "status": "pass",
                        "evidence": f"Thumbnail and native pixels visibly pass {gate}.",
                    }
                    for gate in required_gates
                },
                "user_judgment": {
                    "baseline_available": False,
                    "genuinely_moe": "pending",
                    "better_than_baseline": "not_applicable",
                    "source": "not_yet_received",
                    "evidence": "",
                },
            }
            reviewed = audit_moe_render_review.audit_moe_render_review(
                pack,
                review,
                composed=composed,
            )
            self.assertTrue(reviewed["technical_qualified"], reviewed)
            self.assertEqual(
                reviewed["effective_visual_contract_sha256"],
                effective_sha,
            )
            missing_composed = audit_moe_render_review.audit_moe_render_review(
                pack,
                review,
            )
            self.assertFalse(missing_composed["technical_qualified"])
            self.assertIn(
                "effective_visual_contract.chosen_visual_concept_ids",
                {failure["check"] for failure in missing_composed["schema_failures"]},
            )

    def test_run_ledger_preserves_visual_concept_selection_and_effective_hash(self):
        visual_id = "visual-concept:inner_thigh_negative_space"
        effective_sha = "a" * 64
        args = record_image_run.parse_args(
            [
                "--ts",
                "2026-08-14T12:00:00+09:00",
                "--prompt-en",
                "An audited adult visual concept prompt.",
                "--attempt",
                "1",
                "--status",
                "success",
                "--chosen-visual-concept-ids-json",
                json.dumps([visual_id]),
                "--effective-visual-contract-sha256",
                effective_sha,
            ]
        )
        entry = record_image_run.build_entry(args)
        self.assertEqual(entry["chosen_visual_concept_ids"], [visual_id])
        self.assertEqual(entry["effective_visual_contract_sha256"], effective_sha)

        empty_args = record_image_run.parse_args(
            [
                "--ts",
                "2026-08-14T12:00:01+09:00",
                "--prompt-en",
                "An audited prompt with an explicit empty concept selection.",
                "--attempt",
                "1",
                "--status",
                "success",
                "--chosen-visual-concept-ids-json",
                "[]",
            ]
        )
        empty_entry = record_image_run.build_entry(empty_args)
        self.assertEqual(empty_entry["chosen_visual_concept_ids"], [])

    def test_visual_render_gate_failure_and_uncontracted_gate_fail_closed(self):
        pack = self.moe_pack(
            "Photorealistic explicitly nonsexual behavior-led moe scene of an adult "
            "woman, mid-twenties or older, doing a bubble tea challenge",
            seed=1405,
        )
        required_gates = pack["moe_response"]["render_qualification"][
            "required_hard_gates"
        ]
        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "candidate.png"
            image_path.write_bytes(b"visual-obligation-test-image")
            review = {
                "schema_version": "moe-render-review/v1",
                "pack_id": pack["pack_id"],
                "contract_version": pack["moe_response"]["contract_version"],
                "reviewer": "test pixel reviewer",
                "result_image": str(image_path),
                "result_sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
                "hard_gates": {
                    gate: {
                        "status": "pass",
                        "evidence": f"Native and thumbnail pixels visibly pass {gate}.",
                    }
                    for gate in required_gates
                },
                "user_judgment": {
                    "baseline_available": False,
                    "genuinely_moe": "pending",
                    "better_than_baseline": "not_applicable",
                    "source": "not_yet_received",
                    "evidence": "",
                },
            }
            passed = audit_moe_render_review.audit_moe_render_review(pack, review)
            self.assertTrue(passed["technical_qualified"], passed)

            failed = copy.deepcopy(review)
            failed["hard_gates"]["vo_drink_visible_base_contact"] = {
                "status": "fail",
                "evidence": "The cup base floats above the fabric in native pixels.",
            }
            failed_result = audit_moe_render_review.audit_moe_render_review(pack, failed)
            self.assertFalse(failed_result["technical_qualified"])
            self.assertEqual(
                [row["gate"] for row in failed_result["failed_hard_gates"]],
                ["vo_drink_visible_base_contact"],
            )

            extra = copy.deepcopy(review)
            extra["hard_gates"]["uncontracted_custom_gate"] = {
                "status": "pass",
                "evidence": "This gate was never declared in the candidate pack.",
            }
            extra_result = audit_moe_render_review.audit_moe_render_review(pack, extra)
            self.assertFalse(extra_result["technical_qualified"])
            self.assertIn(
                "hard_gates",
                {failure["check"] for failure in extra_result["schema_failures"]},
            )

    def test_mamang_keeps_existing_nurturant_contract_without_new_profile(self):
        pack = self.moe_pack(
            "Photorealistic explicitly nonsexual behavior-led moe scene of an adult "
            "woman, mid-twenties or older, with calm protective 마망 warmth",
            seed=1406,
        )
        self.assertEqual(
            pack["moe_response"]["relationship_register"],
            "nurturant_benevolence",
        )
        self.assertEqual(
            pack["moe_response"]["render_qualification"]["mechanism_hard_gates"],
            [
                "relaxed_brow",
                "patient_soft_eyes",
                "reassuring_mouth",
                "calm_protective_attention",
            ],
        )
        self.assertNotIn("visual_obligations", pack)


if __name__ == "__main__":
    unittest.main()
