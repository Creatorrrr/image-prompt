from __future__ import annotations

import copy
import hashlib
import random
import tempfile
import unittest
from pathlib import Path

from tests import test_photo_authorial_core_v6 as fixtures
from tests import test_photo_authorship_policy as authorship_fixtures

import audit_moe_render_review as auditor


generator = fixtures.prompt_generator
prompt_auditor = fixtures.audit_composed_prompt


class PhotoCharacterRenderReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = fixtures.PhotoAuthorialCoreV6Tests()
        core = fixture.normalize(fixtures.core())
        data = fixture.runtime_data()
        result = generator.generate_once(
            data, random.Random(9501), None, ["en"], True, 12, True,
            selection_mode="rule", include_trace=True,
            concept_locks=[fixtures.REQUEST], seed=9501, creativity=0.0,
            authorial_core=core,
        )
        cls.pack = generator.build_candidate_pack(result, data, "v6")
        cls.composed = authorship_fixtures.PhotoAuthorshipPolicyTests.composed(cls.pack)
        contract = cls.pack["character_response"]
        evidence = contract["frozen_evidence"]
        cls.composed["character_response"] = {
            "source_contract_sha256": contract["canonical_sha256"],
            "evidence": {
                field: evidence[field]
                for field in contract["prompt_binding"]["required_evidence_fields"]
            },
            "selected_advisory_candidate_ids": [],
        }
        cls.composed["authored_slots"] = {
            row["slot"]: {
                "prompt_evidence": evidence["actor_phrase"],
                "artistic_rationale": "preserves the frozen adult subject",
                "constraint_acknowledgments": [
                    row.get("constraints", {}).get("scene_family", "")
                ],
            }
            for row in cls.pack.get("authorial_open_slots", [])
        }
        cls.composed["viewer_experience"] = {
            "target_audience": {"literacy": "general", "required_prior_knowledge": "none"},
            "viewing_context": "full_screen",
            "primary_viewer_need": "insight",
            "intended_experience": "notice practical care beneath a guarded manner",
            "viewer_promise": "a specific response to an injured coworker",
            "first_glance_hook": evidence["primary_action_phrase"],
            "interpretive_question": "how does the helping action differ from the guarded posture?",
            "attachment_channel": "none",
            "commercial_objective": "none",
            "reinspection_reward": {"mode": "none", "description": ""},
            "affect_evidence": {
                "actor": evidence["actor_phrase"],
                "action": evidence["primary_action_phrase"],
                "target": evidence["target_phrase"],
                "consequence": evidence["immediate_consequence_phrase"],
            },
            "prompt_evidence": {
                "first_glance_hook_phrase": evidence["primary_action_phrase"],
                "affect_actor_phrase": evidence["actor_phrase"],
                "affect_action_phrase": evidence["primary_action_phrase"],
                "affect_target_phrase": evidence["target_phrase"],
                "affect_consequence_phrase": evidence["immediate_consequence_phrase"],
            },
        }
        if cls.pack.get("visual_concept_candidates", {}).get("enabled"):
            cls.composed["chosen_visual_concept_ids"] = []
        preflight = prompt_auditor.audit_composed_prompt(cls.pack, cls.composed)
        if preflight["status"] != "pass":
            raise AssertionError(preflight["failures"])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.image_path = Path(self.temp.name) / "recorded-image.bin"
        self.image_path.write_bytes(b"fixed bytes for review-integrity tests; not pixel evidence")

    def review(self, pack=None, composed=None):
        pack = self.pack if pack is None else pack
        composed = self.composed if composed is None else composed
        contract = pack["character_response"]
        gates = [row["id"] for row in contract["render_gates"]]
        effective, failures = prompt_auditor.derive_effective_visual_obligation_contract(pack, composed)
        self.assertEqual(failures, [])
        gates.extend((effective or {}).get("required_hard_gates", []))
        return {
            "schema_version": "moe-render-review/v1",
            "pack_id": pack["pack_id"],
            "contract_version": "photo-character-response/v1",
            "source_character_response_contract_sha256": contract["canonical_sha256"],
            "reviewer": "synthetic review-record validator",
            "result_image": str(self.image_path),
            "result_sha256": hashlib.sha256(self.image_path.read_bytes()).hexdigest(),
            "hard_gates": {
                gate: {"status": "pass", "evidence": "Synthetic gate observation for validation only."}
                for gate in gates
            },
            "user_judgment": {
                "baseline_available": False,
                "genuinely_moe": "pending",
                "better_than_baseline": "not_applicable",
                "source": "not_yet_received",
                "evidence": "",
            },
        }

    def audit(self, review, pack=None, composed=None):
        return auditor.audit_moe_render_review(
            self.pack if pack is None else pack,
            review,
            composed=self.composed if composed is None else composed,
        )

    def test_typed_only_review_requires_all_nine_gates_without_promoting_preference(self):
        result = self.audit(self.review())
        self.assertTrue(result["technical_qualified"], result)
        self.assertEqual(result["required_hard_gate_count"], 9)
        self.assertFalse(result["representative_eligible"])
        self.assertEqual(result["qualification_status"], "character_response_technical_qualified_user_judgment_pending")
        self.assertEqual(result["source_character_response_contract_sha256"], self.pack["character_response"]["canonical_sha256"])

    def test_missing_extra_partial_or_unsubstantiated_gates_fail_closed(self):
        for gate in self.review()["hard_gates"]:
            with self.subTest(missing=gate):
                review = self.review()
                del review["hard_gates"][gate]
                result = self.audit(review)
                self.assertFalse(result["technical_qualified"])
                self.assertIn(gate, {row["gate"] for row in result["failed_hard_gates"]})
        for value in ("partial", "fail"):
            with self.subTest(status=value):
                review = self.review()
                review["hard_gates"]["character_response_affect_leak"]["status"] = value
                self.assertFalse(self.audit(review)["technical_qualified"])
        review = self.review()
        review["hard_gates"]["unrequested_fixed_pose"] = {"status": "pass", "evidence": "An invented pose was never a required gate."}
        self.assertFalse(self.audit(review)["technical_qualified"])
        review = self.review()
        review["hard_gates"]["character_response_actor"]["evidence"] = ""
        self.assertFalse(self.audit(review)["technical_qualified"])

    def test_complete_audited_composition_is_required(self):
        missing = auditor.audit_moe_render_review(self.pack, self.review())
        self.assertIn("character_response.composed_prompt", {row["check"] for row in missing["schema_failures"]})
        changed = copy.deepcopy(self.composed)
        changed["character_response"]["evidence"]["trigger_phrase"] = "unrequested trigger"
        result = self.audit(self.review(), composed=changed)
        self.assertFalse(result["technical_qualified"])
        self.assertIn("composed_prompt.character_response_evidence", {row["check"] for row in result["schema_failures"]})
        mutated_pack = copy.deepcopy(self.pack)
        mutated_pack["negative_en"] = ""
        result = self.audit(self.review(), pack=mutated_pack)
        self.assertIn("composed_prompt.pack_integrity", {row["check"] for row in result["schema_failures"]})

    def test_rehashed_gate_deletion_duplication_or_rebinding_cannot_shrink_duties(self):
        for mutation in ("delete", "duplicate", "rebind"):
            with self.subTest(mutation=mutation):
                pack = copy.deepcopy(self.pack)
                composed = copy.deepcopy(self.composed)
                contract = pack["character_response"]
                if mutation == "delete":
                    contract["render_gates"].pop()
                elif mutation == "duplicate":
                    contract["render_gates"].append(copy.deepcopy(contract["render_gates"][0]))
                else:
                    contract["render_gates"][0]["evidence_field"] = "baseline_phrase"
                contract.pop("canonical_sha256")
                contract["canonical_sha256"] = generator.canonical_json_sha256(contract)
                composed["character_response"]["source_contract_sha256"] = contract["canonical_sha256"]
                generator.candidate_pack_recompute_id(pack)
                composed["pack_id"] = pack["pack_id"]
                result = self.audit(self.review(pack, composed), pack, composed)
                self.assertIn("character_response.render_gates", {row["check"] for row in result["schema_failures"]})
                self.assertEqual(result["required_hard_gate_count"], 9)
                self.assertFalse(result["technical_qualified"])

    def test_missing_typed_contract_is_detected_from_frozen_required_assertion(self):
        pack = copy.deepcopy(self.pack)
        del pack["character_response"]
        generator.candidate_pack_recompute_id(pack)
        composed = copy.deepcopy(self.composed)
        composed["pack_id"] = pack["pack_id"]
        review = self.review()
        review["pack_id"] = pack["pack_id"]
        result = self.audit(review, pack, composed)
        self.assertFalse(result["technical_qualified"])
        self.assertIn("composed_prompt.character_response_contract", {row["check"] for row in result["schema_failures"]})
        self.assertEqual(result["required_hard_gate_count"], 9)

    def test_visual_obligations_and_only_selected_optional_gates_join_typed_gates(self):
        pack = copy.deepcopy(self.pack)
        composed = copy.deepcopy(self.composed)
        phrase = pack["character_response"]["frozen_evidence"]["actor_phrase"]
        obligation = {
            "id": "recorded_actor_visibility",
            "prompt_binding": {"required_evidence_fields": ["actor_phrase"]},
            "bindings": {"actor_phrase": phrase},
            "render_gates": [{"id": "vo_recorded_actor_visibility"}],
        }
        optional = copy.deepcopy(obligation)
        optional["id"] = "optional_actor_visibility"
        optional["render_gates"] = [{"id": "vo_selected_actor_visibility"}]
        pack["visual_obligations"] = {
            "enabled": True, "contract_version": "photo-visual-obligations/v1",
            "obligations": [obligation], "required_hard_gates": ["vo_recorded_actor_visibility"],
        }
        pack["visual_concept_candidates"] = {
            "enabled": True, "contract_version": "photo-visual-concepts/v1",
            "candidate_order": "seed_shuffled_non_preferential",
            "selection_field": "chosen_visual_concept_ids",
            "selection_policy": {key: True for key in (
                "all_candidates_optional", "selection_list_required_even_when_empty",
                "unselected_candidates_add_no_prompt_or_review_duty",
                "selected_candidates_promote_opt_in_contract_to_hard_obligation",
                "matched_terms_scores_and_routing_reasons_not_exposed",
            )},
            "candidates": [{
                "id": "visual-concept:optional_actor_visibility",
                "content_form": "unordered_inspiration_terms", "concept_terms": ["actor", "visibility"],
                "applicability": {"status": "eligible"},
                "opt_in_contract": {
                    "effect": "promote_to_hard_visual_obligation",
                    "visual_obligations_contract_version": "photo-visual-obligations/v1",
                    "obligation": optional,
                },
            }],
        }
        generator.candidate_pack_recompute_id(pack)
        composed["pack_id"] = pack["pack_id"]
        for selected in (False, True):
            with self.subTest(selected=selected):
                composed["chosen_visual_concept_ids"] = ["visual-concept:optional_actor_visibility"] if selected else []
                composed["visual_obligation_evidence"] = {obligation["id"]: {"actor_phrase": phrase}}
                if selected:
                    composed["visual_obligation_evidence"][optional["id"]] = {"actor_phrase": phrase}
                review = self.review(pack, composed)
                result = self.audit(review, pack, composed)
                self.assertTrue(result["technical_qualified"], result)
                self.assertEqual(result["required_hard_gate_count"], 11 if selected else 10)
                self.assertEqual("vo_selected_actor_visibility" in result["required_hard_gates"], selected)
                del review["hard_gates"]["vo_recorded_actor_visibility"]
                self.assertFalse(self.audit(review, pack, composed)["technical_qualified"])

    def test_review_hash_and_image_bytes_remain_bound(self):
        review = self.review()
        review["source_character_response_contract_sha256"] = "0" * 64
        self.assertFalse(self.audit(review)["technical_qualified"])
        review = self.review()
        self.image_path.write_bytes(b"changed result image bytes")
        result = self.audit(review)
        self.assertIn("result_sha256", {row["check"] for row in result["schema_failures"]})


if __name__ == "__main__":
    unittest.main()
