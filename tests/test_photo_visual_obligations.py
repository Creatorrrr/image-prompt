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

    def test_general_visual_profiles_route_without_adult_character_context(self):
        reality_result = {
            "provenance": {
                "concept_lock": [
                    "A clean photographic beach scene governed by one reality error"
                ]
            }
        }
        data = {prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY: self.registry}
        materialized = prompt_generator.candidate_pack_visual_obligations(
            data,
            reality_result,
            {},
            None,
        )
        self.assertIsNotNone(materialized)
        self.assertEqual(
            [row["id"] for row in materialized["obligations"]],
            ["diegetic_reality_invariant_failure"],
        )

        glitch_result = {
            "provenance": {
                "concept_lock": [
                    "A video compression stream develops motion-vector displacement "
                    "inside one bounded failure zone while the scene remains recognizable"
                ]
            }
        }
        candidates = prompt_generator.candidate_pack_visual_concept_candidates(
            data,
            glitch_result,
            {},
            None,
            None,
        )
        self.assertIsNotNone(candidates)
        self.assertEqual(
            [row["id"] for row in candidates["candidates"]],
            ["visual-concept:medium_native_glitch"],
        )

    def test_glitch_and_reality_error_require_prompt_independent_authored_legibility(
        self,
    ):
        expected = {
            "medium_native_glitch": {
                "evidence": "authored_mechanism_legibility_phrase",
                "gates": {
                    "vo_glitch_authored_mechanism_legibility",
                    "vo_glitch_not_generation_defect_substitute",
                },
                "rejects": {
                    "isolated_synthesis_defect_without_medium_pattern",
                    "malformed_anatomy_or_object_merge_as_glitch",
                    "viewer_can_only_identify_generic_image_failure",
                },
            },
            "diegetic_reality_invariant_failure": {
                "evidence": "authored_rule_legibility_phrase",
                "gates": {
                    "vo_reality_error_affected_surface_coherence",
                    "vo_reality_error_authored_rule_legibility",
                    "vo_reality_error_not_generation_defect_substitute",
                    "vo_reality_error_reveal_legibility",
                },
                "rejects": {
                    "visible_translucent_shell_or_water_sheet",
                    "enclosing_splash_ring_as_field_boundary",
                    "flat_image_plane_slice_ignoring_depth_and_material",
                    "particle_dissolve_without_measurable_cross_surface_correspondence",
                    "facial_texture_stamped_onto_unrelated_surface",
                    "isolated_generation_defect_without_inferable_rule",
                    "malformed_anatomy_object_merge_or_texture_failure",
                    "anomaly_requires_prompt_or_caption_to_be_understood",
                    "viewer_can_only_say_something_looks_wrong",
                },
            },
        }
        for profile_id, contract in expected.items():
            with self.subTest(profile_id=profile_id):
                profile = prompt_generator.visual_obligation_profile_by_id(
                    self.registry,
                    profile_id,
                )
                self.assertIsNotNone(profile)
                self.assertIn(
                    contract["evidence"],
                    profile["required_evidence_fields"],
                )
                self.assertIn(
                    contract["evidence"],
                    profile["evidence_requirements"],
                )
                self.assertTrue(
                    contract["gates"]
                    <= {gate["id"] for gate in profile["render_gates"]}
                )
                self.assertTrue(
                    contract["rejects"] <= set(profile["reject_substitutes"])
                )
                self.assertIn(
                    "without prompt text or a caption",
                    profile["composition_instruction"],
                )

        reality_profile = prompt_generator.visual_obligation_profile_by_id(
            self.registry,
            "diegetic_reality_invariant_failure",
        )
        self.assertIsNotNone(reality_profile)
        self.assertIn(
            "affected_surface_material_coherence",
            reality_profile["semantics"]["component_semantics"][
                "required_group_ids"
            ],
        )
        self.assertIn(
            "affected_surface_coherence_phrase",
            reality_profile["required_evidence_fields"],
        )
        self.assertIn(
            "reveal_legibility_phrase",
            reality_profile["required_evidence_fields"],
        )
        self.assertNotIn(
            "delayed_discovery_phrase",
            reality_profile["required_evidence_fields"],
        )
        self.assertIn(
            "immediate authored contradiction",
            reality_profile["evidence_requirements"]["reveal_legibility_phrase"][
                "must_mention_any"
            ],
        )
        self.assertIn(
            "quiet second-look contradiction",
            reality_profile["evidence_requirements"]["reveal_legibility_phrase"][
                "must_mention_any"
            ],
        )
        obligation = {
            "id": reality_profile["id"],
            "prompt_binding": {
                "required_evidence_fields": reality_profile[
                    "required_evidence_fields"
                ],
                "minimum_distinct_evidence_phrases": len(
                    reality_profile["required_evidence_fields"]
                ),
                "prompt_evidence_must_be_literal": True,
            },
            "evidence_requirements": reality_profile["evidence_requirements"],
            "render_gates": copy.deepcopy(reality_profile["render_gates"]),
            "bindings": {},
        }
        evidence = self.visual_evidence_for_obligation(obligation)
        pack = {
            "visual_obligations": {
                "enabled": True,
                "contract_version": "photo-visual-obligations/v1",
                "strict_gate_set": True,
                "obligations": [obligation],
                "required_hard_gates": [
                    gate["id"] for gate in obligation["render_gates"]
                ],
            }
        }
        prompt_en = "; ".join(evidence.values()) + "."
        composed = {
            "prompt_en": prompt_en,
            "visual_obligation_evidence": {reality_profile["id"]: evidence},
        }
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(
                pack,
                composed,
                prompt_en,
            ),
            [],
        )
        missing_legibility = copy.deepcopy(composed)
        missing_legibility["visual_obligation_evidence"][reality_profile["id"]].pop(
            "authored_rule_legibility_phrase"
        )
        failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            missing_legibility,
            prompt_en,
        )
        self.assertIn(
            "visual_obligation_evidence",
            {failure["check"] for failure in failures},
        )

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
        self.assertIn("both feet touch or nearly touch", obligation["composition_instruction"])
        self.assertEqual(
            obligation["prompt_binding"]["required_evidence_fields"],
            [
                "close_leg_geometry_phrase",
                "inner_thigh_boundary_phrase",
                "negative_space_phrase",
                "false_gap_exclusion_phrase",
                "thumbnail_crop_phrase",
            ],
        )
        self.assertIn("wide_stance_space", obligation["reject_substitutes"])
        self.assertIn("crossed_leg_accidental_opening", obligation["reject_substitutes"])
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

    def test_general_profile_adult_eligibility_must_be_an_explicit_boolean(self):
        mutated = copy.deepcopy(self.registry)
        profile = next(
            row
            for row in mutated["profiles"]
            if row["id"] == "diegetic_reality_invariant_failure"
        )
        profile["activation"]["requires_adult_character"] = "false"
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
            any(
                "activation.requires_adult_character: must be boolean" in error
                for error in errors
            ),
            errors,
        )

    def test_semantic_discovery_component_guard_must_be_boolean(self):
        mutated = copy.deepcopy(self.registry)
        profile = next(
            row
            for row in mutated["profiles"]
            if row["id"] == "yandere_affection_control_relation"
        )
        profile["activation"][
            "semantic_discovery_requires_component_evidence"
        ] = "true"
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
            any(
                "semantic_discovery_requires_component_evidence: must be boolean"
                in error
                for error in errors
            ),
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

    def test_contained_affect_profile_uses_components_and_blocks_labels_at_runtime(self):
        pack = self.moe_pack(
            "Photorealistic adult character portrait with a menhera gothic-lolita concept",
            seed=1413,
        )
        obligation = pack["visual_obligations"]["obligations"][0]
        self.assertEqual(
            obligation["id"],
            "contained_affect_self_presentation",
        )
        component_semantics = obligation["component_semantics"]
        self.assertEqual(component_semantics["minimum_component_groups"], 3)
        self.assertEqual(
            set(component_semantics["required_group_ids"]),
            {
                "controlled_social_surface",
                "contained_affect_leak",
                "regulation_or_connection_trace",
            },
        )
        self.assertNotIn(
            "phone",
            " ".join(component_semantics["required_group_ids"]),
        )
        self.assertEqual(
            obligation["runtime_expression"]["runtime_forbidden_labels"],
            ["menhera", "멘헤라", "メンヘラ"],
        )

        evidence = self.visual_evidence_for_obligation(obligation)
        prompt_en = self.prompt_for_obligation(obligation, evidence)
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": prompt_en,
            "negative_en": pack["negative_en"],
            "chosen_visual_concept_ids": [],
            "visual_obligation_evidence": {obligation["id"]: evidence},
        }
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(
                pack,
                composed,
                prompt_en,
            ),
            [],
        )
        runtime_prompt = prompt_en + f"\nAvoid: {pack['negative_en']}"
        request = {
            "schema_version": "photo-image-render-request/v2",
            "pack_id": pack["pack_id"],
            "runtime_prompt_en": runtime_prompt,
            "runtime_negative_en": pack["negative_en"],
            "audit_boundary": {
                "composed_prompt_audit_status": "pass",
                "runtime_prompt_audit_status": "not_run",
                "inherits_composed_prompt_pass": False,
            },
            "references": [],
        }
        passed = audit_image_render_request.audit_image_render_request(
            pack,
            composed,
            request,
        )
        self.assertEqual(passed["status"], "pass", passed)

        positive_leak = copy.deepcopy(request)
        positive_leak["runtime_prompt_en"] += "\nmenhera"
        positive_audit = audit_image_render_request.audit_image_render_request(
            pack,
            composed,
            positive_leak,
        )
        self.assertIn(
            "runtime_forbidden_label",
            {failure["check"] for failure in positive_audit["failures"]},
        )

        negative_pack = copy.deepcopy(pack)
        negative_pack["negative_en"] += ", menhera"
        negative_composed = copy.deepcopy(composed)
        negative_composed["negative_en"] = negative_pack["negative_en"]
        negative_request = copy.deepcopy(request)
        negative_request["runtime_negative_en"] = negative_pack["negative_en"]
        negative_request["runtime_prompt_en"] = (
            prompt_en + f"\nAvoid: {negative_pack['negative_en']}"
        )
        negative_audit = audit_image_render_request.audit_image_render_request(
            negative_pack,
            negative_composed,
            negative_request,
        )
        runtime_failure = next(
            failure
            for failure in negative_audit["failures"]
            if failure["check"] == "runtime_forbidden_label"
        )
        self.assertIn(
            "runtime_negative_en",
            runtime_failure["hits"][0]["surfaces"],
        )

        core_pack = copy.deepcopy(pack)
        core_pack["authorial_core"] = {
            "runtime_forbidden_labels": ["private concept"]
        }
        core_leak = copy.deepcopy(request)
        core_leak["runtime_prompt_en"] += "\nprivate concept"
        core_audit = audit_image_render_request.audit_image_render_request(
            core_pack,
            composed,
            core_leak,
        )
        self.assertIn(
            "runtime_forbidden_label",
            {failure["check"] for failure in core_audit["failures"]},
        )

    def test_yandere_profile_requires_affection_control_relation_not_role_prop(self):
        pack = self.moe_pack(
            "Photorealistic adult fictional nurse character portrait with a yandere concept",
            seed=1414,
        )
        obligation = pack["visual_obligations"]["obligations"][0]
        self.assertEqual(obligation["id"], "yandere_affection_control_relation")
        self.assertEqual(
            set(obligation["component_semantics"]["required_group_ids"]),
            {
                "specific_affection_target",
                "affectionate_surface_or_care",
                "boundary_intrusion_or_access_control",
                "visible_same_target_consequence",
            },
        )
        component_group_ids = {
            row["id"] for row in obligation["component_semantics"]["groups"]
        }
        self.assertTrue(
            {
                "supporting_affiliative_outward_signal",
                "supporting_target_fixation_signal",
                "direct_obsessive_madness_display",
                "supporting_face_mode_sweet_threat_mismatch",
                "supporting_target_triggered_face_mismatch",
                "supporting_meso_scale_facial_mechanics",
                "supporting_face_mode_dead_eye_devotion",
                "supporting_face_mode_ecstatic_face_cradle",
                "supporting_face_mode_manic_possessive",
                "supporting_face_mode_abandonment_fracture",
            }
            <= component_group_ids
        )
        self.assertEqual(
            obligation["prompt_binding"]["required_evidence_fields"],
            [
                "adult_fictional_subject_phrase",
                "specific_affection_target_phrase",
                "affectionate_surface_phrase",
                "boundary_intrusion_action_phrase",
                "visible_choice_consequence_phrase",
                "outward_affection_signal_phrase",
                "target_fixation_signal_phrase",
                "direct_obsessive_madness_phrase",
                "single_frame_coexistence_phrase",
            ],
        )
        self.assertEqual(
            obligation["runtime_expression"]["runtime_forbidden_labels"],
            ["yandere", "얀데레", "ヤンデレ"],
        )
        gate_ids = {row["id"] for row in obligation["render_gates"]}
        self.assertIn("vo_yandere_same_affection_target", gate_ids)
        self.assertIn("vo_yandere_affection_and_control_coexist", gate_ids)
        self.assertIn("vo_yandere_same_target_consequence", gate_ids)
        self.assertIn("vo_yandere_not_role_prop_horror", gate_ids)
        self.assertIn("vo_yandere_two_channel_outward_supports", gate_ids)
        self.assertIn("vo_yandere_direct_obsessive_madness", gate_ids)
        self.assertIn("vo_yandere_face_mode_not_generic", gate_ids)
        self.assertIn("vo_yandere_eye_physics_and_target_lock", gate_ids)
        self.assertIn("vo_yandere_non_graphic_fictional_intensity", gate_ids)
        self.assertNotIn("vo_yandere_nonviolent_safe_staging", gate_ids)
        two_channel_gate = next(
            row
            for row in obligation["render_gates"]
            if row["id"] == "vo_yandere_two_channel_outward_supports"
        )
        self.assertEqual(two_channel_gate["review_scale"], "both")
        self.assertIn(
            "syringe_weapon_blood_or_red_light_only",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "reference_face_treated_as_personality_evidence",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "single_affiliative_face_or_fixed_stare_only",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "affection_and_fixation_without_direct_visible_madness",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "pupil_size_used_as_love_or_possession_proof",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "face_cradle_pose_without_same_target_control_relation",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "incompatible_dead_eye_tear_bright_tiny_pupil_mode_stack",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "sparkling_beauty_irises_or_large_catchlights_erasing_selected_face_mode",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "broad_friendly_smile_or_playful_head_tilt_erasing_eye_mouth_contradiction",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "target_reaction_changes_mouth_and_eyes_together",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "pale_iris_texture_only_while_lids_head_and_mouth_remain_friendly",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "Choose exactly one of these modes",
            obligation["composition_instruction"],
        )
        self.assertIn(
            "freeze one mouth corner partway through a fractional deepening while the eyes remain fixed and unchanged",
            obligation["composition_instruction"],
        )
        self.assertIn(
            "changing iris texture alone is insufficient",
            obligation["composition_instruction"],
        )
        face_mode_gate = next(
            row
            for row in obligation["render_gates"]
            if row["id"] == "vo_yandere_face_mode_not_generic"
        )
        self.assertIn("bright detailed beauty irises", face_mode_gate["description"])
        eye_gate = next(
            row
            for row in obligation["render_gates"]
            if row["id"] == "vo_yandere_eye_physics_and_target_lock"
        )
        self.assertIn("one tiny dim scene-coherent catchlight", eye_gate["description"])

        target_trigger_group = next(
            row
            for row in obligation["component_semantics"]["groups"]
            if row["id"] == "supporting_target_triggered_face_mismatch"
        )
        self.assertIn(
            "the same target's reaching hand is visible while one mouth corner is frozen partway through a fractional deepening and the eyes remain fixed",
            target_trigger_group["any_terms"],
        )
        meso_scale_group = next(
            row
            for row in obligation["component_semantics"]["groups"]
            if row["id"] == "supporting_meso_scale_facial_mechanics"
        )
        self.assertIn(
            "meso-scale facial mechanics break the friendly beauty read rather than relying on pale irises alone",
            meso_scale_group["any_terms"],
        )

        evidence = self.visual_evidence_for_obligation(obligation)
        prompt_en = self.prompt_for_obligation(obligation, evidence)
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": prompt_en,
            "negative_en": pack["negative_en"],
            "chosen_visual_concept_ids": [],
            "visual_obligation_evidence": {obligation["id"]: evidence},
        }
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(
                pack,
                composed,
                prompt_en,
            ),
            [],
        )

        role_prop_only = copy.deepcopy(composed)
        role_prop_only["visual_obligation_evidence"][obligation["id"]][
            "boundary_intrusion_action_phrase"
        ] = "a nurse holds a syringe as an ordinary clinical prop"
        role_prop_prompt = self.prompt_for_obligation(
            obligation,
            role_prop_only["visual_obligation_evidence"][obligation["id"]],
        )
        role_prop_only["prompt_en"] = role_prop_prompt
        failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            role_prop_only,
            role_prop_prompt,
        )
        self.assertIn(
            "visual_obligation_semantic_evidence",
            {failure["check"] for failure in failures},
        )

        mode_phrases = [
            "warm mouth against an overfocused tense gaze",
            "precisely target-locked yet unnervingly lifeless",
            "both palms cradle her cheeks and jaw beneath an adoring flushed gaze",
            "wide sclera and tiny pupils beneath a loving crooked smile",
            "moist eyes and a tightening mouth track the withdrawing beloved",
            "her smile deepens by a fraction while her eyes remain unchanged",
        ]
        for mode_phrase in mode_phrases:
            with self.subTest(face_mode=mode_phrase):
                mode_composed = copy.deepcopy(composed)
                mode_evidence = mode_composed["visual_obligation_evidence"][
                    obligation["id"]
                ]
                mode_evidence["direct_obsessive_madness_phrase"] = (
                    f"{mode_phrase} while the same-target action remains visible"
                )
                mode_prompt = self.prompt_for_obligation(obligation, mode_evidence)
                mode_composed["prompt_en"] = mode_prompt
                self.assertEqual(
                    audit_composed_prompt.audit_visual_obligations(
                        pack,
                        mode_composed,
                        mode_prompt,
                    ),
                    [],
                )

        restrained_without_madness = copy.deepcopy(composed)
        restrained_without_madness["visual_obligation_evidence"][obligation["id"]][
            "direct_obsessive_madness_phrase"
        ] = "a gentle affectionate portrait remains calm and composed"
        restrained_prompt = self.prompt_for_obligation(
            obligation,
            restrained_without_madness["visual_obligation_evidence"][obligation["id"]],
        )
        restrained_without_madness["prompt_en"] = restrained_prompt
        failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            restrained_without_madness,
            restrained_prompt,
        )
        self.assertIn(
            "visual_obligation_semantic_evidence",
            {failure["check"] for failure in failures},
        )

        one_channel_only = copy.deepcopy(composed)
        one_channel_only["visual_obligation_evidence"][obligation["id"]][
            "target_fixation_signal_phrase"
        ] = "an intense gaze supplies generic horror styling"
        one_channel_prompt = self.prompt_for_obligation(
            obligation,
            one_channel_only["visual_obligation_evidence"][obligation["id"]],
        )
        one_channel_only["prompt_en"] = one_channel_prompt
        failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            one_channel_only,
            one_channel_prompt,
        )
        self.assertIn(
            "visual_obligation_semantic_evidence",
            {failure["check"] for failure in failures},
        )

    def test_generic_face_cues_do_not_hard_activate_yandere_relation(self):
        generic_prompts = [
            "Photorealistic adult portrait with dead eyes, dim catchlights, and low-contrast irises",
            "Photorealistic adult portrait with both palms cradling her cheeks and an adoring gaze",
            "Photorealistic adult portrait with very small pupils and wide sclera",
            "Photorealistic beauty portrait with sparkling gray irises, large catchlights, a broad friendly smile, and a playful head tilt",
        ]
        for text in generic_prompts:
            with self.subTest(text=text):
                source_rows = [
                    {
                        "source": "concept_lock",
                        "text": text,
                        "polarity": "required",
                        "priority": "critical",
                        "mandatory": True,
                    }
                ]
                self.assertNotIn(
                    "yandere_affection_control_relation",
                    prompt_generator.candidate_pack_auto_visual_obligation_matches(
                        self.registry,
                        source_rows,
                    ),
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

    def test_visual_only_render_review_uses_effective_visual_gate_contract(self):
        data = {prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY: self.registry}
        result = {
            "provenance": {
                "concept_lock": ["adult portrait with a twin-tail hairstyle"]
            }
        }
        visual_contract = prompt_generator.candidate_pack_visual_obligations(
            data,
            result,
            {},
            None,
        )
        self.assertIsNotNone(visual_contract)
        pack = {
            "pack_id": "visual-only-render-pack",
            "visual_obligations": visual_contract,
        }
        required_gates = visual_contract["required_hard_gates"]
        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "candidate.png"
            image_path.write_bytes(b"visual-only-render-review-image")
            review = {
                "schema_version": "moe-render-review/v1",
                "pack_id": pack["pack_id"],
                "contract_version": visual_contract["contract_version"],
                "reviewer": "visual-only pixel reviewer",
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
            audited = audit_moe_render_review.audit_moe_render_review(pack, review)
            self.assertTrue(audited["technical_qualified"], audited)
            self.assertFalse(audited["representative_eligible"])
            self.assertEqual(audited["schema_failures"], [])
            self.assertEqual(
                audited["qualification_status"],
                "visual_technical_qualified_user_judgment_pending",
            )
            self.assertEqual(
                audited["contract_version"],
                "photo-visual-obligations/v1",
            )

        unqualified = audit_moe_render_review.audit_moe_render_review(
            {"pack_id": "no-render-contract"},
            {
                "schema_version": "moe-render-review/v1",
                "pack_id": "no-render-contract",
                "contract_version": "",
                "reviewer": "fail-closed reviewer",
                "result_image": "missing.png",
                "result_sha256": "0" * 64,
                "hard_gates": {},
                "user_judgment": {
                    "baseline_available": False,
                    "genuinely_moe": "pending",
                    "better_than_baseline": "not_applicable",
                    "source": "not_yet_received",
                    "evidence": "",
                },
            },
        )
        self.assertFalse(unqualified["technical_qualified"])
        self.assertIn(
            "render_qualification_contract",
            {failure["check"] for failure in unqualified["schema_failures"]},
        )

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

    def test_kuudere_profile_requires_stable_composure_and_same_target_care(self):
        pack = self.moe_pack(
            "Photorealistic adult fictional coworker character portrait with a "
            "kuudere concept",
            seed=1421,
        )
        obligation = pack["visual_obligations"]["obligations"][0]
        self.assertEqual(
            obligation["id"],
            "kuudere_composed_warmth_relation",
        )
        self.assertEqual(
            set(obligation["component_semantics"]["required_group_ids"]),
            {
                "composed_low_expression_surface",
                "specific_trusted_target",
                "quiet_target_directed_support",
                "localized_warmth_leak",
                "visible_same_target_consequence",
            },
        )
        group_ids = {
            row["id"] for row in obligation["component_semantics"]["groups"]
        }
        self.assertTrue(
            {
                "supporting_low_amplitude_face",
                "supporting_economical_posture",
                "supporting_restrained_styling",
            }
            <= group_ids
        )
        self.assertEqual(
            obligation["prompt_binding"]["required_evidence_fields"],
            [
                "adult_fictional_subject_phrase",
                "composed_surface_phrase",
                "specific_trusted_target_phrase",
                "quiet_support_action_phrase",
                "localized_warmth_leak_phrase",
                "same_target_consequence_phrase",
                "stable_surface_coexistence_phrase",
                "appearance_nonproof_phrase",
            ],
        )
        self.assertEqual(
            obligation["runtime_expression"]["runtime_forbidden_labels"],
            [
                "kuudere",
                "cooldere",
                "cool-dere",
                "쿨데레",
                "쿠데레",
                "쿨 데레",
                "クーデレ",
            ],
        )
        self.assertIn(
            "Hair, eyes, costume, gender, role, posture",
            next(
                row["description"]
                for row in obligation["render_gates"]
                if row["id"] == "vo_kuudere_appearance_is_optional_support"
            ),
        )
        self.assertIn(
            "hair_eye_color_or_hairstyle_as_personality_evidence",
            obligation["reject_substitutes"],
        )
        self.assertIn(
            "same-target action and consequence",
            obligation["composition_instruction"],
        )

        evidence = self.visual_evidence_for_obligation(obligation)
        prompt_en = self.prompt_for_obligation(obligation, evidence)
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": prompt_en,
            "negative_en": pack["negative_en"],
            "chosen_visual_concept_ids": [],
            "visual_obligation_evidence": {obligation["id"]: evidence},
        }
        self.assertEqual(
            audit_composed_prompt.audit_visual_obligations(
                pack,
                composed,
                prompt_en,
            ),
            [],
        )

        role_only = copy.deepcopy(composed)
        role_only["visual_obligation_evidence"][obligation["id"]][
            "quiet_support_action_phrase"
        ] = "routine professional service performed for every client"
        role_only_prompt = self.prompt_for_obligation(
            obligation,
            role_only["visual_obligation_evidence"][obligation["id"]],
        )
        role_only["prompt_en"] = role_only_prompt
        failures = audit_composed_prompt.audit_visual_obligations(
            pack,
            role_only,
            role_only_prompt,
        )
        self.assertIn(
            "visual_obligation_semantic_evidence",
            {failure["check"] for failure in failures},
        )

    def test_role_garment_and_revealing_armor_profiles_are_structurally_complete(self):
        expected = {
            "aircraft_pilot_operation": {
                "adult": True,
                "required_groups": {
                    "pilot_station_identity",
                    "control_or_checklist_contact",
                    "matched_flight_state",
                },
                "gate": "vo_pilot_flight_state_coherence",
                "reject": "pilot_helmet_or_flight_suit_only",
            },
            "cabin_crew_safety_role": {
                "adult": True,
                "required_groups": {
                    "aircraft_cabin_identity",
                    "safety_procedure",
                    "governed_safety_target",
                },
                "gate": "vo_cabin_crew_not_service_or_uniform_only",
                "reject": "service_tray_or_cart_only",
            },
            "school_uniform_institutional_system": {
                "adult": False,
                "required_groups": {
                    "coordinated_garment_set",
                    "institutional_consistency",
                    "school_identity_context",
                },
                "gate": "vo_school_uniform_not_generic_prep",
                "reject": "random_plaid_skirt_or_tie",
            },
            "one_piece_dress_construction": {
                "adult": False,
                "required_groups": {
                    "continuous_garment_unit",
                    "dress_silhouette",
                    "construction_and_drape",
                },
                "gate": "vo_one_piece_not_adjacent_sense",
                "reject": "matching_two_piece_separates",
            },
            "sheer_garment_optical_layering": {
                "adult": False,
                "required_groups": {
                    "translucent_textile_surface",
                    "transmission_relationship",
                    "garment_boundary_and_layer",
                },
                "gate": "vo_sheer_not_optical_or_generation_substitute",
                "reject": "transparent_body_or_missing_clothing_artifact",
            },
            "military_uniform_duty_system": {
                "adult": False,
                "required_groups": {
                    "uniform_variant_identity",
                    "component_system_consistency",
                    "duty_context_alignment",
                },
                "gate": "vo_military_uniform_not_adjacent_role",
                "reject": "camouflage_streetwear_only",
            },
            "wearable_protective_armor_system": {
                "adult": False,
                "required_groups": {
                    "wearable_protective_geometry",
                    "articulated_mobility",
                    "underlayer_attachment_and_gap_control",
                },
                "gate": "vo_armor_underlayer_and_attachment",
                "reject": "robot_or_vehicle_armor_shell",
            },
            "commercial_appeal_revealing_armor": {
                "adult": True,
                "required_groups": {
                    "unmistakably_adult_original_character",
                    "armor_identity_structure",
                    "deliberate_high_exposure_pattern",
                    "opaque_intimate_coverage",
                },
                "gate": "vo_revealing_armor_opaque_intimate_coverage",
                "reject": "ordinary_bikini_or_lingerie_without_armor",
            },
        }
        profiles = {profile["id"]: profile for profile in self.registry["profiles"]}
        self.assertTrue(set(expected) <= set(profiles))
        for profile_id, contract in expected.items():
            with self.subTest(profile_id=profile_id):
                profile = profiles[profile_id]
                self.assertIs(
                    profile["activation"]["requires_adult_character"],
                    contract["adult"],
                )
                self.assertEqual(
                    set(
                        profile["semantics"]["component_semantics"][
                            "required_group_ids"
                        ]
                    ),
                    contract["required_groups"],
                )
                self.assertIn(
                    contract["gate"],
                    {gate["id"] for gate in profile["render_gates"]},
                )
                self.assertIn(contract["reject"], profile["reject_substitutes"])

        revealing = profiles["commercial_appeal_revealing_armor"]
        self.assertEqual(
            set(revealing["activation"]["project_glossary_aliases"]),
            {
                "상업적 방어력",
                "상업적인 방어력",
                "상업적 방어력이 높은 갑옷",
                "상업적인 방어력 높은 갑옷",
            },
        )
        self.assertEqual(
            revealing["runtime_expression"]["default_mode"],
            "definition_only",
        )
        self.assertTrue(
            set(revealing["activation"]["project_glossary_aliases"])
            <= set(revealing["runtime_expression"]["runtime_forbidden_labels"])
        )
        base_armor = profiles["wearable_protective_armor_system"]
        self.assertTrue(
            set(revealing["activation"]["project_glossary_aliases"])
            <= set(base_armor["activation"]["exclude_if_any_terms"])
        )


if __name__ == "__main__":
    unittest.main()
