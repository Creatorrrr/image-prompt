"""Scope and leak invariants of the closed projection (no fake audit PASS)."""
import copy
from pathlib import Path
import tempfile
import unittest

from tests.test_photo_workflow_precore import freeze_fixture, files, wire
from tests.test_photo_workflow_state import SCRIPTS
from photo_retry_projection import DECISION_FIELDS, project, visual_obligation


class PhotoRetryContextTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        run, _ = freeze_fixture(Path(self.temp.name)); state = files.load_state(run)
        _, core, controls = files.verify_freeze(state)
        self.envelope = files.value(state, "request_envelope_input")
        self.decision = {"schema_version": "photo-repair-decision/v1", "current_source_span_ids": ["topic"],
            "source_text": self.envelope["request_text"], "preserved_dimensions": ["concept", "subject", "event"],
            "allowed_changes": ["lighting"], "requester_corrected_dimensions": [], "allowed_properties": [], "local_axes": ["lighting"],
            "failed_gate_ids": [], "failure_class": "artistic_revision", "additional_invocation_limit": 1, "obligation_dimensions": {}}
        self.parent = {"core": core, "controls": controls, "pack": {"pack_id": "abc", "candidate_inventories": {"secret": "FORBIDDEN_SENTINEL"}},
            "attempt": {"run_id": "run"}, "receipt": {"generation_id": "gen", "canonical_sha256": "receipt"},
            "runtime": {"references": []}, "audit": {}, "reviews": {}, "failed_gate_ids": []}
        self.sources = {role: {"sha256": "a" * 64} for role in ("authorial_core_normalized", "pack", "decision", "effective_visual", "attempt")}

    def test_closed_projection_does_not_expose_parent_optional_material(self):
        self.parent["core"]["future_optional"] = "FORBIDDEN_SENTINEL"
        self.parent["attempt"]["error_details"] = {"http_status": 400, "error_code": "FORBIDDEN_SENTINEL"}
        out = project(self.parent, self.envelope, self.decision, self.sources)
        self.assertNotIn("FORBIDDEN_SENTINEL", files.encode(out).decode())
        self.assertNotIn("baseline_prompt_en", out); self.assertEqual(out["allowed_scope"]["dimensions"], ["lighting"])
        self.assertNotIn("camera", out["allowed_scope"]["dimensions"])

    def test_unknown_fields_and_lock_widening_are_rejected(self):
        bad = {**self.decision, "invented": True}
        with self.assertRaisesRegex(ValueError, "invalid_repair_decision"): project(self.parent, self.envelope, bad, self.sources)
        bad = {**self.decision, "allowed_changes": ["subject"], "preserved_dimensions": ["concept", "event"]}
        with self.assertRaisesRegex(ValueError, "parent_lock_scope_conflict"): project(self.parent, self.envelope, bad, self.sources)

    def test_unrepresentable_local_scope_is_not_opened_for_convenience(self):
        decision = {**self.decision, "allowed_changes": [], "local_axes": ["contact_geometry"]}
        out = project(self.parent, self.envelope, decision, self.sources)
        self.assertEqual(out["lineage_status"], "scope_not_representable_in_lineage_v2")
        self.assertEqual(out["allowed_scope"]["dimensions"], [])

    def test_mixed_required_relation_fails_without_losing_endpoint(self):
        self.parent["core"]["semantic_assertions"].append({"dimension": "action", "polarity": "required", "affected_dimensions": ["subject", "action"], "axes": {"actor": "one"}, "evidence": {}})
        with self.assertRaisesRegex(ValueError, "projection_scope_unresolved"): project(self.parent, self.envelope, self.decision, self.sources)

    def test_parent_property_and_children_stay_locked(self):
        self.parent["core"]["intent_lock"]["semantic_anchors"].append({"dimension": "material", "target": "wardrobe", "property": "color", "prompt_evidence": "linen blanket"})
        decision = {**self.decision, "allowed_changes": ["material"], "local_axes": ["material"],
                    "allowed_properties": [{"dimension": "material", "target": "wardrobe", "property": "color.hue"}]}
        with self.assertRaisesRegex(ValueError, "locked_property_overlap"): project(self.parent, self.envelope, decision, self.sources)

    def test_failed_gate_is_not_inferred_from_artistic_judgment(self):
        decision = {**self.decision, "failed_gate_ids": ["invented_gate"]}
        with self.assertRaisesRegex(ValueError, "failed_gate_scope_conflict"): project(self.parent, self.envelope, decision, self.sources)
        decision = {**self.decision, "failure_class": "transient_http"}
        with self.assertRaisesRegex(ValueError, "observed_transient_code_required"): project(self.parent, self.envelope, decision, self.sources)

    def test_selected_obligation_retains_gate_without_unknown_fields(self):
        obligation = {"id": "chosen", "composition_instruction": "retain the owner and contact relation", "component_semantics": {"minimum_component_groups": 1, "required_group_ids": ["actor"], "groups": [{"id": "actor", "any_terms": ["one actor"]}]},
            "prompt_binding": {"required_evidence_fields": ["actor_phrase"]}, "evidence_requirements": {},
            "render_gates": [{"id": "actual_gate", "review_scale": "both", "criterion": "Owner contact stays visible", "future_optional": "FORBIDDEN_SENTINEL"}],
            "future_optional": "FORBIDDEN_SENTINEL"}
        self.parent["audit"]["effective_visual"] = {"obligations": [obligation]}
        decision = {**self.decision, "obligation_dimensions": {"chosen": ["concept"]}}
        out = project(self.parent, self.envelope, decision, self.sources)
        self.assertEqual(out["effective_obligations"][0]["value"]["render_gates"][0]["id"], "actual_gate")
        self.assertNotIn("FORBIDDEN_SENTINEL", files.encode(out).decode())
        bad = {**decision, "obligation_dimensions": {"chosen": ["lighting"]}}
        with self.assertRaisesRegex(ValueError, "projection_scope_unresolved"): project(self.parent, self.envelope, bad, self.sources)

    def test_unrecognized_nested_contract_stops_instead_of_clipping(self):
        with self.assertRaisesRegex(ValueError, "unsupported_obligation_projection_shape"):
            visual_obligation({"evidence_requirements": {"actor_phrase": {"new_relation_rule": "do not clip"}}})


if __name__ == "__main__": unittest.main()
