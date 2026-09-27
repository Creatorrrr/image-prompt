from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
ASSETS = SCRIPTS.parent / "assets"
sys.path.insert(0, str(SCRIPTS))

import audit_composed_prompt
import prompt_generator as pg
import validate_photo_prompt_dictionary as validator
from visual_profile_contracts import compile_visual_profile


class PhotoDataSemanticCorrectionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}
        routing_ids = {
            "deliberate_underarm_salience", "aircraft_pilot_operation", "cabin_crew_safety_role",
            "rembrandt_face_light_pattern", "broad_face_light_orientation_relation",
            "short_face_light_orientation_relation", "yandere_affection_control_relation",
            "contained_affect_self_presentation",
        }
        routing_ids.update(p["id"] for p in cls.registry["profiles"] if p["category"] == "professional_role")
        cls.routing_registry = {**cls.registry, "profiles": [p for p in cls.registry["profiles"] if p["id"] in routing_ids]}
        cls.index = pg.build_visual_profile_index_payload(cls.routing_registry)

    def resolve(self, text, baseline=None):
        rows = [{"source": "concept_lock", "text": text, "polarity": "required"}]
        if baseline is not None:
            rows.append({"source": "authorial_core_baseline", "text": baseline, "polarity": "required"})
        result = pg.resolve_visual_profile_hits(self.routing_registry, rows, visual_profile_index=self.index, adult_context=True)
        return {row["profile_id"]: row for row in result["hits"]}

    def test_role_identity_is_advisory_without_requested_duty(self):
        cases = {
            "aircraft_pilot_operation": [
                "An adult aircraft pilot rests in the aircraft cockpit with hands folded and eyes closed.",
                "항공기 조종석에서 눈을 감고 쉬는 성인 항공기 조종사",
                "An adult pilot models a uniform beside the aircraft cockpit.",
            ],
            "cabin_crew_safety_role": [
                "An adult flight attendant reads a paperback while resting inside the aircraft cabin.",
                "항공기 객실에서 책을 읽으며 쉬는 성인 승무원",
                "An adult flight attendant serves tea in the aircraft cabin.",
                "항공기 화장실 스튜어디스 허벅지",
            ],
        }
        for profile_id, texts in cases.items():
            for text in texts:
                with self.subTest(profile=profile_id, text=text):
                    hit = self.resolve(text)[profile_id]
                    self.assertFalse(hit["hard_eligible"])
                    self.assertTrue(hit["optional_eligible"])
                    self.assertEqual(hit["applicability_status"], "requires_explicit_mechanism")

    def test_explicit_operational_roles_keep_hard_causal_contract(self):
        cases = [
            ("aircraft_pilot_operation", "An adult aircraft pilot is operating flight controls in the aircraft cockpit."),
            ("aircraft_pilot_operation", "성인 항공기 조종사가 조종석 체크리스트로 비행 전 점검을 한다."),
            ("cabin_crew_safety_role", "An adult flight attendant gives a passenger safety demonstration inside the aircraft cabin."),
            ("cabin_crew_safety_role", "성인 승무원이 항공기 객실에서 비상 장비를 점검한다."),
        ]
        for profile_id, text in cases:
            with self.subTest(text=text):
                self.assertTrue(self.resolve(text, text)[profile_id]["hard_eligible"])
                profile = self.profiles[profile_id]
                self.assertGreaterEqual(len(profile["required_evidence_fields"]), 5)
                self.assertTrue(any("consequence" in g["id"] or "flight_state" in g["id"] for g in profile["render_gates"]))

    def test_freely_authored_duty_does_not_relabel_the_user_role(self):
        hit = self.resolve(
            "Adult flight attendant in an aircraft cabin",
            "An adult flight attendant gives a passenger safety demonstration inside the aircraft cabin.",
        )["cabin_crew_safety_role"]
        self.assertFalse(hit["hard_eligible"])

    def test_every_professional_role_separates_rest_from_operational_action(self):
        names = {
            "aircraft_pilot_operation": "aircraft pilot",
            "cabin_crew_safety_role": "flight attendant",
            "clinical_nursing_duty_system": "nurse",
            "police_public_safety_duty_system": "police officer",
            "firefighter_protective_response_system": "firefighter",
            "emergency_medical_transport_system": "emergency medical technician",
            "maritime_safety_coast_guard_role": "coast guard officer",
            "rail_driver_operation": "train driver",
            "rail_platform_dispatch_operation": "platform dispatcher",
            "private_security_access_control": "security guard",
        }
        self.assertEqual(set(names), {p["id"] for p in self.registry["profiles"] if p["category"] == "professional_role"})
        for profile_id, name in names.items():
            profile = self.profiles[profile_id]
            context = profile["activation"]["context_disambiguation"]["any_terms"][0]
            action = profile["activation"]["hard_activation"]["required_any_groups"][0]["any_terms"][0]
            with self.subTest(profile=profile_id):
                rest = f"An adult {name} rests with folded hands, with {context} in the background."
                hit = self.resolve(rest, rest)[profile_id]
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])
                active = f"An adult {name} performs {action}, with {context} visible in the same frame."
                self.assertTrue(self.resolve(active, active)[profile_id]["hard_eligible"])

    def test_nursing_uniform_and_yandere_relation_do_not_request_patient_care(self):
        for text in [
            "An adult nurse rests in a scrub uniform at the clinical bedside.",
            "성인 간호사가 임상 병상 옆에서 쉬며 스크럽 제복을 입고 있다.",
            "An adult fictional yandere nurse holds an axe at the clinical bedside in a scrub uniform.",
            "도끼를 든 성인 얀데레 간호사 캐릭터 사진, 임상 병상 배경",
        ]:
            with self.subTest(text=text):
                hits = self.resolve(text, text)
                self.assertFalse(hits["clinical_nursing_duty_system"]["hard_eligible"])
                if "yandere" in text or "얀데레" in text:
                    self.assertTrue(hits["yandere_affection_control_relation"]["hard_eligible"])
        for text in [
            "An adult nurse checks patient identifier before vital-sign assessment at the clinical bedside.",
            "성인 간호사가 임상 병상에서 환자 식별 정보를 확인하고 활력 징후를 확인한다.",
        ]:
            with self.subTest(text=text):
                self.assertTrue(self.resolve(text, text)["clinical_nursing_duty_system"]["hard_eligible"])

    def test_negated_duty_cannot_support_hard_activation(self):
        hit = self.resolve("An adult flight attendant in an aircraft cabin without a safety demonstration.")["cabin_crew_safety_role"]
        self.assertFalse(hit["hard_eligible"])

    def test_body_area_product_and_incidental_detail_stay_advisory(self):
        for text in [
            "An adult hand holds a bottle of underarm deodorant.",
            "An adult runner with a small underarm tattoo ties a shoe.",
            "겨드랑이 작은 문신이 보이는 성인 러너가 신발 끈을 묶는 장면",
            "成人が腋用デオドラント製品を手に持つ写真",
        ]:
            with self.subTest(text=text):
                hit = self.resolve(text)["deliberate_underarm_salience"]
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])

    def test_explicit_body_area_salience_stays_hard_in_three_languages(self):
        for text in [
            "Adult portrait emphasizing the underarm with a raised arm.",
            "성인 인물의 겨드랑이를 강조하는 팔 올린 포즈",
            "成人の腋を強調する腕を上げたポーズ",
        ]:
            with self.subTest(text=text):
                self.assertTrue(self.resolve(text)["deliberate_underarm_salience"]["hard_eligible"])

    def test_rembrandt_preserves_geometry_for_both_camera_orientations(self):
        profile = self.profiles["rembrandt_face_light_pattern"]
        surfaces = json.dumps({k: profile[k] for k in ["semantics", "composition_instruction", "evidence_requirements", "render_gates"]})
        self.assertNotIn("near side", surfaces)
        self.assertNotIn("far eye", surfaces)
        self.assertNotIn("far cheek", surfaces)
        self.assertIn("shadow-side eye", surfaces)
        self.assertIn("nose shadow", surfaces)
        for orientation in ["broad_face_light_orientation_relation", "short_face_light_orientation_relation"]:
            for direction in ["camera-left", "camera-right"]:
                with self.subTest(orientation=orientation, direction=direction):
                    text = "Adult portrait with Rembrandt face-light pattern and " + self.profiles[orientation]["activation"]["exact_terms"][0] + f" from {direction}."
                    hits = self.resolve(text)
                    self.assertTrue(hits[profile["id"]]["hard_eligible"])
                    self.assertTrue(hits[orientation]["hard_eligible"])

    def test_telephoto_uses_narrow_field_of_view(self):
        definition = self.profiles["telephoto_distance_compression_relation"]["semantics"]["definition"]
        self.assertIn("narrow field of view", definition)
        self.assertNotIn("long field of view", definition)

    def test_yandere_retains_same_target_action_and_consequence_without_scene_recipe(self):
        profile = self.profiles["yandere_affection_control_relation"]
        self.assertEqual(set(profile["semantics"]["component_semantics"]["required_group_ids"]), {
            "specific_affection_target", "affectionate_surface_or_care", "boundary_intrusion_or_access_control", "visible_same_target_consequence"
        })
        hard_text = json.dumps({k: profile[k] for k in ["semantics", "composition_instruction", "evidence_requirements", "render_gates"]}, ensure_ascii=False).casefold()
        for token in ["herself", "her face", "female nurse", "keycard", "syringe", "patient", "one tiny dim", "exactly one of these modes"]:
            self.assertNotIn(token, hard_text)
        self.assertIn("same_target_consequence", hard_text)
        self.assertTrue(self.resolve("An adult fictional character portrait with a yandere concept")[profile["id"]]["hard_eligible"])

    def test_bare_menhera_label_does_not_claim_the_project_interpretation(self):
        hit = self.resolve("An adult menhera character portrait.")["contained_affect_self_presentation"]
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])
        scope = self.profiles["contained_affect_self_presentation"]["semantics"]["interpretation_scope"]
        self.assertEqual(scope["kind"], "project_visual_interpretation")
        self.assertTrue(self.resolve("An adult menhera portrait with a contained affect leak.")[hit["profile_id"]]["hard_eligible"])

    def test_related_exact_match_survives_the_compatibility_candidate_path(self):
        rows = [{"source": "concept_lock", "text": "An adult menhera character portrait.", "polarity": "required"}]
        candidates = pg.candidate_pack_auto_visual_concept_matches(self.routing_registry, rows)
        self.assertIn("contained_affect_self_presentation", candidates)
        self.assertTrue(candidates["contained_affect_self_presentation"])

    def test_claim_limits_do_not_enter_positive_retrieval(self):
        profile = self.profiles["inner_thigh_negative_space"]
        self.assertIn("fertility", " ".join(profile["semantics"]["claim_limits"]))
        positive_text = pg.visual_profile_semantic_text(profile).casefold()
        for term in ["health", "weight", "fertility", "body fat"]:
            self.assertNotIn(term, positive_text)
        expression = self.profiles["composite_overwhelmed_expression"]
        self.assertNotIn("fully clothed", pg.visual_profile_semantic_text(expression).casefold())
        self.assertNotIn("nonsexual", pg.visual_profile_semantic_text(expression).casefold())
        self.assertNotIn("fully clothed", " ".join(g["description"] for g in expression["render_gates"]))
        for profile_id in [
            "slender_linear_build", "soft_full_figure_volume", "toned_muscular_build",
            "bust_prominence_relation", "oval_central_torso_silhouette_relation",
            "diamond_central_torso_silhouette_relation",
        ]:
            with self.subTest(profile=profile_id):
                text = pg.visual_profile_semantic_text(self.profiles[profile_id]).casefold()
                for claim_term in ["health", "fertility", "body weight", "medical inference"]:
                    self.assertNotIn(claim_term, text)
        crime = pg.visual_profile_semantic_text(self.profiles["declared_minor_targeted_crime_relation"]).casefold()
        self.assertNotIn("nonsexual", crime)
        self.assertNotIn("fully clothed", crime)

    def test_authored_components_derive_every_evidence_gate_and_group(self):
        raw = json.loads((ASSETS / "photo_prompt_visual_obligations.json").read_text())
        rows = [p for p in raw["profiles"] if "authored_components" in p]
        self.assertEqual(len(rows), 3)
        for profile in rows:
            with self.subTest(profile=profile["id"]):
                for field in ["required_evidence_fields", "evidence_requirements", "render_gates", "composition_instruction"]:
                    self.assertNotIn(field, profile)
                self.assertNotIn("component_semantics", profile["semantics"])
                compiled = compile_visual_profile(profile)
                components = profile["authored_components"]["components"]
                self.assertEqual(compiled["required_evidence_fields"], [c["evidence_field"] for c in components])
                self.assertEqual(compiled["render_gates"], [c["render_gate"] for c in components])
                changed = copy.deepcopy(profile)
                changed["authored_components"]["components"][0]["evidence_terms"][0] = "changed authored invariant remains concretely observable"
                self.assertEqual(compile_visual_profile(changed)["evidence_requirements"][components[0]["evidence_field"]]["must_mention_any"][0], "changed authored invariant remains concretely observable")

    def clamshell_obligation(self, text):
        return pg.candidate_pack_visual_profile_obligation(
            self.profiles["clamshell_dual_source_portrait_light"], self.registry,
            activation_source="explicit_request_semantics", source_intent_ids=["request:test"],
            context_text=text, request_text=text,
        )

    def test_closed_eyes_omit_only_clamshell_catchlight_evidence(self):
        normal = self.clamshell_obligation("Adult clamshell portrait")
        closed = self.clamshell_obligation("Adult clamshell portrait with eyes closed")
        normal_fields = set(normal["prompt_binding"]["required_evidence_fields"])
        closed_fields = set(closed["prompt_binding"]["required_evidence_fields"])
        self.assertEqual(normal_fields - closed_fields, {"clam_catchlight_phrase"})
        self.assertEqual(len(closed_fields), 4)
        self.assertNotIn("vo_capture_clam_vertical_catchlight_pair", {g["id"] for g in closed["render_gates"]})
        self.assertNotIn("catchlight", closed["composition_instruction"])
        self.assertNotIn("clam_vertical_catchlights", closed["component_semantics"]["required_group_ids"])

    def test_explicit_catchlight_request_is_not_silently_dropped(self):
        obligation = self.clamshell_obligation("Adult clamshell portrait with eyes closed and a vertical catchlight pair")
        self.assertIn("clam_catchlight_phrase", obligation["prompt_binding"]["required_evidence_fields"])

    def test_negated_visibility_and_catchlight_phrases_do_not_change_obligations(self):
        open_eyes = self.clamshell_obligation("Adult clamshell portrait, not eyes closed")
        self.assertIn("clam_catchlight_phrase", open_eyes["prompt_binding"]["required_evidence_fields"])
        closed_eyes = self.clamshell_obligation("Adult clamshell portrait with eyes closed, without a catchlight pair")
        self.assertNotIn("clam_catchlight_phrase", closed_eyes["prompt_binding"]["required_evidence_fields"])
        with self.assertRaisesRegex(ValueError, "negation-aware request matcher"):
            compile_visual_profile(self.profiles["clamshell_dual_source_portrait_light"], context_text="not eyes closed")

    def test_diopter_gate_checks_visible_continuity_not_production_history(self):
        profile = self.profiles["split_diopter_dual_focus_planes"]
        self.assertIn("production process", " ".join(profile["semantics"]["claim_limits"]))
        for gate in profile["render_gates"]:
            self.assertNotIn("prove", gate["description"])
        continuity = profile["evidence_requirements"]["diopter_continuity_phrase"]
        self.assertTrue(all("prove" not in phrase for phrase in continuity["must_mention_any"]))

    def test_compiled_evidence_stays_literal_and_missing_invariants_fail_audit(self):
        obligation = self.clamshell_obligation("Adult clamshell portrait with eyes closed")
        evidence = {field: spec["must_mention_any"][-1] for field, spec in obligation["evidence_requirements"].items()}
        prompt = ". ".join(evidence.values()) + "."
        pack = {"visual_obligations": {"enabled": True, "obligations": [obligation]}}
        composed = {"visual_obligation_evidence": {obligation["id"]: evidence}}
        self.assertEqual(audit_composed_prompt.audit_visual_obligations(pack, composed, prompt), [])
        missing_literal = prompt.replace(evidence["clam_lower_fill_phrase"], "lower light becomes dominant")
        failures = audit_composed_prompt.audit_visual_obligations(pack, composed, missing_literal)
        self.assertTrue(failures)
        missing_invariant = copy.deepcopy(composed)
        del missing_invariant["visual_obligation_evidence"][obligation["id"]]["clam_lower_fill_phrase"]
        self.assertTrue(audit_composed_prompt.audit_visual_obligations(pack, missing_invariant, prompt))

    def test_invalid_authored_component_and_activation_are_rejected(self):
        profile = copy.deepcopy(self.profiles["clamshell_dual_source_portrait_light"])
        profile["authored_components"]["components"][0]["ignore_this_invariant"] = True
        with self.assertRaisesRegex(ValueError, "invalid authored component keys"):
            compile_visual_profile(profile)
        contradictory = copy.deepcopy(self.profiles["clamshell_dual_source_portrait_light"])
        contradictory["evidence_requirements"]["clam_lower_fill_phrase"]["must_mention_any"] = ["the lower light is dominant"]
        with self.assertRaisesRegex(ValueError, "conflicts with its authored component source"):
            compile_visual_profile(contradictory)
        errors = []
        validator.validate_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json", errors)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
