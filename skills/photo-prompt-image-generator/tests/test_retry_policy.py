"""Failure routing and bounded execution regressions. No real provider calls.

PHOTO_RETRY_TEST_ROOT selects a reviewed/staged native closure; default is source.
"""
import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
import urllib.error

SKILL = Path(__file__).resolve().parents[1]
ROOT = Path(os.environ.get("PHOTO_RETRY_TEST_ROOT", SKILL))
sys.path[:0] = [str(ROOT / "scripts"), str(ROOT / "precore")]
import photo_retry_policy as policy
import photo_retry_projection as projection
import prepare_retry_context as coordinator
import photo_workflow as workflow
import photo_native_bridge as bridge
import generate_images_via_api as api


def fixture():
    text = "Keep the same input and retry within the authorized limit."
    envelope = {"contract_version": "photo-request-envelope/v1", "provenance": "requesting_user",
        "request_id": "retry-current", "request_text": text, "request_sha256": hashlib.sha256(text.encode()).hexdigest(),
        "active_spans": [{"span_id": "instruction", "text": text, "start": 0, "end": len(text)}]}
    parent = {"core": {"canonical_sha256": "a"*64, "request_binding": {"request_id": "parent", "request_sha256": "b"*64},
        "intent_lock": {"canonical_sha256": "c"*64, "locked_dimensions": ["identity"], "open_dimensions": ["lighting"], "semantic_anchors": []}},
        "pack": {"pack_id": "fixture"}, "attempt": {"status": "safety_block", "run_id": "parent-row", "attempt": 1,
            "error_details": {"error_code": "moderation_blocked", "http_status": 400}},
        "audit": {}, "failed_gate_ids": [], "reviews": {}, "runtime": {"references": []}, "controls": {"controls": {}},
        "receipt": {"generation_id": "generation", "canonical_sha256": "d"*64}, "provider_outcome": "rejected"}
    decision = {"schema_version": "photo-repair-decision/v1", "current_source_span_ids": ["instruction"], "source_text": text,
        "preserved_dimensions": ["identity"], "allowed_changes": [], "requester_corrected_dimensions": [], "allowed_properties": [],
        "local_axes": [], "failed_gate_ids": [], "failure_class": "provider_blocked", "additional_invocation_limit": 1, "obligation_dimensions": {}}
    return parent, envelope, decision


def project(parent, envelope, decision):
    return projection.project(parent, envelope, decision, {"decision": {"sha256": "e"*64}, "attempt": {"sha256": "f"*64}, "pack": {"sha256": "a"*64}})


class Routing(unittest.TestCase):
    def test_block_with_no_changes_is_representable_in_original_run(self):
        context = project(*fixture())
        self.assertEqual(context["retry_mode"], "same_input")
        self.assertEqual(context["lineage_status"], "existing_run_same_input")
        self.assertEqual(context["execution_scope"]["additional_invocation_limit"], 1)
        self.assertEqual(context["allowed_scope"], {"dimensions": [], "properties": [], "local_axes": []})

    def test_block_cannot_rewrite_content_or_be_relabeled(self):
        parent, envelope, decision = fixture()
        for change in ({"allowed_changes": ["lighting"]}, {"failure_class": "artistic_revision", "allowed_changes": ["lighting"]},
                       {"allowed_properties": [{"dimension": "lighting", "target": "scene", "property": "light"}]}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                project(parent, envelope, {**decision, **change})

    def test_changed_and_unchanged_routes_are_distinct(self):
        parent, envelope, decision = fixture()
        parent["attempt"]["status"] = "success"; parent["attempt"]["error_details"] = {}
        decision.update(failure_class="artistic_revision", allowed_changes=["lighting"])
        context = project(parent, envelope, decision)
        self.assertEqual(context["retry_mode"], "revised_content")
        self.assertEqual(context["lineage_status"], "representable")
        with self.assertRaisesRegex(ValueError, "content_revision_requires_changed_dimensions"):
            project(parent, envelope, {**decision, "allowed_changes": []})

    def test_mechanical_route_cannot_hide_unknown_or_nontransient_failure(self):
        parent, envelope, decision = fixture()
        parent["attempt"].update(status="error", error_details={"http_status": 400})
        for outcome in ("unknown", "returned", "rejected"):
            parent["provider_outcome"] = outcome
            with self.subTest(outcome=outcome), self.assertRaisesRegex(ValueError, "observed_failure_route_mismatch"):
                project(parent, envelope, {**decision, "failure_class": "artistic_revision", "allowed_changes": ["lighting"]})

    def test_transient_needs_observed_code(self):
        parent, envelope, decision = fixture()
        parent["attempt"].update(status="error", error_details={"http_status": 429})
        decision["failure_class"] = "transient_http"
        self.assertEqual(project(parent, envelope, decision)["retry_mode"], "same_input")
        parent["attempt"]["error_details"]["http_status"] = 400
        with self.assertRaises(ValueError): project(parent, envelope, decision)

    def test_recovery_routes_never_grant_calls(self):
        for failure in policy.RECOVERY_FAILURES:
            with self.subTest(failure=failure):
                self.assertEqual(policy.retry_mode(failure), "recovery_only")
                with self.assertRaises(ValueError): policy.retry_mode(failure, changed=True)
        parent, envelope, decision = fixture()
        parent["attempt"].update(status="error", error_details={})
        parent["provider_outcome"] = "returned"
        decision.update(failure_class="persistence_failed", additional_invocation_limit=0)
        self.assertEqual(project(parent, envelope, decision)["lineage_status"], "recovery_without_invocation")
        with self.assertRaisesRegex(ValueError, "failure_route_cannot_rerender"):
            project(parent, envelope, {**decision, "additional_invocation_limit": 1})

    def test_pixel_repeat_requires_real_failed_gate(self):
        parent, envelope, decision = fixture()
        parent["attempt"]["status"] = "success"; parent["attempt"]["error_details"] = {}
        decision["failure_class"] = "pixel_realization_mismatch"
        with self.assertRaisesRegex(ValueError, "failed_gate_scope_conflict"): project(parent, envelope, decision)
        parent["failed_gate_ids"] = ["gate"]
        parent["audit"]["embodiment_gates"] = ["gate"]
        decision["failed_gate_ids"] = ["gate"]
        self.assertEqual(project(parent, envelope, decision)["retry_mode"], "same_input")
        decision["allowed_changes"] = ["lighting"]
        self.assertEqual(project(parent, envelope, decision)["retry_mode"], "revised_content")

    def test_same_input_context_cannot_attach_to_child(self):
        context = project(*fixture())
        with patch.object(coordinator, "read_json", return_value={}), patch.object(coordinator, "recompute", return_value=(context, {})):
            with self.assertRaisesRegex(ValueError, "child_requires_content_revision"):
                coordinator.attach_child(NS(proof=Path("unused")))

    def test_locked_content_change_requires_current_requester_correction(self):
        parent, envelope, decision = fixture()
        text = "Change the subject identity; preserve the lighting."
        envelope.update(request_text=text, request_sha256=hashlib.sha256(text.encode()).hexdigest(),
            active_spans=[{"span_id": "instruction", "text": text, "start": 0, "end": len(text)}])
        parent["attempt"].update(status="success", error_details={})
        decision.update(source_text=text, failure_class="meaning_rebuild", preserved_dimensions=["lighting"], allowed_changes=["identity"])
        with self.assertRaisesRegex(ValueError, "parent_lock_scope_conflict"): project(parent, envelope, decision)
        decision["requester_corrected_dimensions"] = ["identity"]
        context = project(parent, envelope, decision)
        self.assertEqual(context["retry_mode"], "revised_content")
        self.assertEqual(context["allowed_scope"]["dimensions"], ["identity"])

    def test_authorized_revision_attaches_to_new_child_with_exact_current_envelope(self):
        parent, envelope, decision = fixture()
        parent["attempt"].update(status="success", error_details={})
        decision.update(failure_class="artistic_revision", allowed_changes=["lighting"])
        context = project(parent, envelope, decision)
        child = {"phase": "request_prepared", "artifacts": {}}
        with patch.object(coordinator, "read_json", side_effect=[{}, context]), patch.object(coordinator, "recompute", return_value=(context, parent)), \
                patch.object(coordinator, "locked_state", return_value=contextlib.nullcontext(child)), patch.object(coordinator, "value", return_value=envelope), \
                patch.object(coordinator, "commit_stage") as commit:
            with tempfile.TemporaryDirectory() as directory:
                proof = Path(directory)/"proof.json"; proof.write_text("{}")
                self.assertTrue(coordinator.attach_child(NS(run=Path(directory)/"child", proof=proof))["retry_attached"])
        self.assertIn("retry_context", commit.call_args.args[3])

    def test_docs_and_neutral_wire_agree_with_routes(self):
        doc = (SKILL / "references/image-runtime.md").read_text()
        for failure in policy.FAILURE_CLASSES:
            self.assertIn("`"+failure+"`", doc)
        self.assertNotIn("Explicit moderation blocks stop unchanged retries", doc)
        shape = json.loads((SKILL / "precore/photo_workflow_shapes.json").read_bytes())["repair_decision"]
        self.assertEqual(set(shape), projection.DECISION_FIELDS)
        self.assertIn("same_input", shape["allowed_changes"])


class ApiExecution(unittest.TestCase):
    def run_adapter(self, directory, outcomes, *, attempts=3, recorder_error=False, initial_attempt=1):
        execution = dict(prompt_en="Exact audited portrait.", negative_en="Exact negative.", runtime_prompt_en="Exact transport prompt.",
            pack_id="fixture", chosen_candidate_ids=[], chosen_visual_concept_ids=[], composer="agent", audit_status="pass",
            augmentation_brief=None, render_repair_contract_sha256=None, model="fixture-model", size="fixture-size",
            runtime_prompt_sha256="a"*64, authorial_core_sha256="b"*64, intent_lock_sha256="c"*64)
        prepared = NS(document={"execution": execution})
        def preflight(path, _):
            path.write_text("{}"); return "d"*64
        counter = []
        def record(flags):
            counter.append(flags)
            if recorder_error: raise RuntimeError("synthetic recorder failure")
            return {"run_id": "row-"+str(len(counter))}
        with patch.object(api, "prepare_api_render", return_value=prepared), patch.object(api, "save_preflight", side_effect=preflight), \
                patch.object(api, "call_api", side_effect=outcomes) as call, patch.object(api, "record", side_effect=record), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            okay = api.generate_for_request(Path("fixture.json"), receipt_file=Path("receipt"), composed_file=Path("composed"),
                request_file=Path("request"), model="fixture-model", size="fixture-size", attempts=attempts, concept=None, slug=None,
                out_base=Path(directory), timestamp="fixture", key="synthetic-not-a-real-key", initial_attempt=initial_attempt)
        return okay, call.call_args_list, counter

    def http(self, code, body):
        return urllib.error.HTTPError("https://example.invalid", code, "synthetic", {}, io.BytesIO(json.dumps(body).encode()))

    def block(self):
        return self.http(400, {"error": {"code": "moderation_blocked", "message": "synthetic rejection"}})

    def test_moderation_retry_keeps_exact_payload_and_failed_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            okay, calls, rows = self.run_adapter(directory, [self.block(), api.ApiImageResult(b"synthetic bytes")])
            self.assertTrue(okay); self.assertEqual(len(calls), 2); self.assertEqual(calls[0], calls[1])
            self.assertEqual(rows[0][rows[0].index("--status")+1], "safety_block")
            self.assertEqual(rows[1][rows[1].index("--retry-of")+1], "row-1")
            self.assertEqual(rows[0][rows[0].index("--prompt-id")+1], rows[1][rows[1].index("--prompt-id")+1])
            self.assertEqual(rows[1][rows[1].index("--attempt")+1], "2")
            evidence = json.loads(next(Path(directory).rglob("*.error.json")).read_bytes())
            self.assertEqual(evidence["outcome"]["error_code"], "moderation_blocked")

    def test_repeated_blocks_stop_at_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            okay, calls, rows = self.run_adapter(directory, [self.block() for _ in range(4)], attempts=2)
            self.assertFalse(okay); self.assertEqual(len(calls), 2); self.assertEqual(len(rows), 2)

    def test_all_transient_codes_repeat_identically(self):
        for code in policy.TRANSIENT_HTTP:
            with self.subTest(code=code), tempfile.TemporaryDirectory() as directory:
                okay, calls, _ = self.run_adapter(directory, [self.http(code, {}), api.ApiImageResult(b"bytes")])
                self.assertTrue(okay); self.assertEqual(calls[0], calls[1])

    def test_unknown_and_generic_safety_message_do_not_repeat(self):
        for error in (TimeoutError("synthetic timeout"), self.http(400, {"error": {"message": "safety mentioned without code"}})):
            with self.subTest(error=type(error).__name__), tempfile.TemporaryDirectory() as directory:
                okay, calls, _ = self.run_adapter(directory, [error])
                self.assertFalse(okay); self.assertEqual(len(calls), 1)

    def test_recorder_failure_stops_before_another_call(self):
        with tempfile.TemporaryDirectory() as directory:
            okay, calls, _ = self.run_adapter(directory, [self.block()], recorder_error=True)
            self.assertFalse(okay); self.assertEqual(len(calls), 1)

    def test_evidence_failure_stops_before_another_call(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(api, "write_evidence", side_effect=OSError("synthetic disk failure")):
            okay, calls, rows = self.run_adapter(directory, [self.block()])
            self.assertFalse(okay); self.assertEqual(len(calls), 1); self.assertEqual(rows, [])

    def test_returned_bytes_are_recovered_without_regeneration(self):
        original = Path.write_bytes
        def write(path, data):
            if path.suffix == ".png": raise OSError("synthetic image writer failure")
            return original(path, data)
        with tempfile.TemporaryDirectory() as directory, patch.object(Path, "write_bytes", write):
            okay, calls, rows = self.run_adapter(directory, [api.ApiImageResult(b"original returned bytes")])
            self.assertFalse(okay); self.assertEqual(len(calls), 1)
            self.assertEqual(next(Path(directory).rglob("*.returned-image.bin")).read_bytes(), b"original returned bytes")
            self.assertEqual(rows[0][rows[0].index("--status")+1], "error")

    def test_external_same_input_retry_increments_parent_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            okay, _, rows = self.run_adapter(directory, [self.block(), api.ApiImageResult(b"bytes")], initial_attempt=4)
            self.assertTrue(okay)
            self.assertEqual([row[row.index("--attempt")+1] for row in rows], ["4", "5"])


class ManagedExecution(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.run = Path(self.temporary.name)
        self.parent, envelope, decision = fixture(); self.context = project(self.parent, envelope, decision)
        self.ledger = self.run / "ledger.ndjson"; self.ledger.write_text(json.dumps({"run_id": "parent-row"})+"\n")
        self.proof = {"parent_run": str(self.run), "ledger": str(self.ledger), "projection_sha256": self.context["projection_sha256"]}
        self.proof_path = self.run / "proof.json"; self.proof_path.write_text(json.dumps(self.proof))
        bindings = {role: "a"*64 for role in ("pack", "runtime_receipt", "composed", "render_request")}
        self.state = {"mode": "image", "artifacts": {k: {"sha256": v} for k,v in bindings.items()},
            "render_scope": {"lanes": ["native"], "invocation_limit": 3, "authorization_source": "actual synthetic test instruction"},
            "operations": [{"operation_id": "a"*32, "lane": "native", "status": "provider_blocked", "input_bindings": bindings,
                "attempts": [{"attempt": 1, "run_id": "parent-row"}], "budget": 1}]}
        for target, kwargs in (("ensure", {"return_value": None}), ("status", {"return_value": {"stale_roles": []}}),
                ("locked_state", {"side_effect": lambda run: contextlib.nullcontext(self.state)}), ("save_state", {"return_value": None}),
                ("value", {"side_effect": lambda state, role: {}})):
            item = patch.object(workflow, target, **kwargs); item.start(); self.addCleanup(item.stop)
        item = patch.object(coordinator, "recompute", side_effect=lambda proof: (copy.deepcopy(self.context), copy.deepcopy(self.parent)))
        item.start(); self.addCleanup(item.stop)

    def test_same_input_reservation_uses_original_run_and_counts_budget(self):
        op = workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)
        self.assertEqual(op["retry_of"], "parent-row"); self.assertEqual(op["initial_attempt"], 2)
        self.assertEqual(op["input_bindings"], self.state["operations"][0]["input_bindings"])
        with self.assertRaisesRegex(ValueError, "pending_operation"):
            workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)

    def test_no_proof_or_changed_inputs_or_transport_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "same_input_retry_proof_required"): workflow.reserve(self.run, "native", 1)
        with self.assertRaisesRegex(ValueError, "same_input_retry_inputs_changed"):
            workflow.same_input_retry(self.state, self.run, self.proof, "api")
        self.state["artifacts"]["composed"]["sha256"] = "changed"
        with self.assertRaisesRegex(ValueError, "same_input_retry_inputs_changed"):
            workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)

    def test_exhausted_human_and_parent_budgets_stop(self):
        self.state["render_scope"]["invocation_limit"] = 1
        with self.assertRaisesRegex(ValueError, "invocation_budget_exhausted"):
            workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)
        self.state["render_scope"]["invocation_limit"] = 3
        self.context["execution_scope"]["additional_invocation_limit"] = 0
        with self.assertRaisesRegex(ValueError, "parent_retry_budget_exhausted"):
            workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)

    def test_recovery_states_and_preview_never_open_another_invocation(self):
        for failure in ("execution_unknown", "recorder_failed", "persistence_failed", "preview_only"):
            self.state["operations"][0]["status"] = failure
            with self.subTest(failure=failure), self.assertRaisesRegex(ValueError, "pending_operation"):
                workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)

    def test_old_parent_proof_cannot_retry_past_a_new_attempt(self):
        self.state["operations"][0]["attempts"].append({"run_id": "newer-row", "attempt": 2})
        with self.assertRaisesRegex(ValueError, "latest_attempt"):
            workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)

    def test_shared_reservation_prevents_reusing_parent_budget(self):
        original = copy.deepcopy(self.state)
        workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)
        # A second caller with the same previously completed state cannot reserve
        # the parent's one additional call again.
        self.state.clear(); self.state.update(original)
        with self.assertRaisesRegex(ValueError, "parent_retry_budget_exhausted"):
            workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)

    def test_known_no_call_preflight_failure_releases_same_input_reservation(self):
        op = workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)
        workflow.update_operation(self.run, op["operation_id"], {"stage": "preflight_failed", "known_no_invocations": True})
        reserved = json.loads(self.ledger.with_name(self.ledger.name+".retry-reservations.json").read_bytes())
        self.assertEqual(reserved[0]["reserved_invocations"], 0)
        self.assertEqual(workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)["budget"], 1)

    def test_one_additional_repair_cap_allows_second_but_not_third_call(self):
        pack = {"render_repair": {"retry_policy": {"maximum_additional_attempts": 1}}}
        with patch.object(workflow, "value", return_value=pack):
            op = workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)
            op["attempts"] = [{"run_id": "second", "attempt": 2}]; op["status"] = "complete"
            self.parent["attempt"].update(run_id="second", attempt=2)
            with self.assertRaisesRegex(ValueError, "invocation_budget_exhausted"):
                workflow.reserve(self.run, "native", 1, retry_proof=self.proof_path)

    def test_native_plan_start_and_record_preserve_payload_and_link_attempt(self):
        reference = self.run / "reference.bin"; reference.write_bytes(b"reference fixture")
        values = {"pack": {"contract_version": "photo-candidate-pack/v10", "pack_id": "fixture", "authorial_core": {
            "canonical_sha256": "b"*64, "intent_lock": {"canonical_sha256": "c"*64}}},
            "composed": {"prompt_en": "Exact original prompt.", "negative_en": "Exact negative.", "chosen_candidate_ids": [], "chosen_visual_concept_ids": []},
            "render_request": {"runtime_prompt_en": "Exact original transport.", "referenced_image_paths": [str(reference)],
                "references": [{"role": "appearance", "sha256": hashlib.sha256(reference.read_bytes()).hexdigest()}]}}
        self.state.update(transport={"lane": "native"}, source_binding={"runtime_store": str(self.run)})
        def commit(run, state, phase, outputs):
            for role, raw in outputs.items():
                path = self.run / (role+".json"); path.write_bytes(raw)
                state["artifacts"][role] = {"path": str(path), "sha256": hashlib.sha256(raw).hexdigest()}
                values[role] = json.loads(raw)
            state["phase"] = phase
        audits = {k: {"status": "pass", "failures": []} for k in ("composed_audit", "runtime_audit")}
        with patch.object(workflow, "load_state", return_value=self.state), patch.object(workflow, "value", side_effect=lambda state,role: values[role]), \
                patch.object(workflow, "commit_stage", side_effect=commit), patch("photo_workflow_worker.audit_bound", return_value=audits):
            plan = workflow.native_plan(NS(run=self.run, retry_proof=self.proof_path))
            started = workflow.native_started(NS(run=self.run))
            self.assertEqual(started["payload"], {"prompt": "Exact original transport.", "referenced_image_paths": [str(reference)], "transparent_background": False})
            with self.assertRaises(ValueError): workflow.native_started(NS(run=self.run))
            from image_attempt_evidence import capture_native_error, write_evidence
            evidence = capture_native_error({"code": "moderation_blocked"}, {"attempt": 2, "provider_outcome": "unknown",
                "request": {"prompt_en": values["composed"]["prompt_en"]}})
            path = self.run / "error.json"; sha = write_evidence(path, evidence)
            observation = self.run / "observation.json"
            observation.write_text(json.dumps({"operation_id": plan["operation_id"], "outcome": "rejected", "evidence_path": str(path), "evidence_sha256": sha}))
            with patch.object(api, "record", return_value={"run_id": "second-row"}) as record:
                workflow.native_result(NS(run=self.run, result=observation, ledger=self.ledger))
            flags = record.call_args.args[0]
            for name, expected in (("--attempt", "2"), ("--retry-of", "parent-row"), ("--image-call-count", "2"), ("--status", "safety_block")):
                self.assertEqual(flags[flags.index(name)+1], expected)
            self.assertEqual(self.state["operations"][-1]["status"], "provider_blocked")
            native_plan = values["native_plan"]
            entry = {"workflow_operation_id": plan["operation_id"]+":2", "ts": native_plan["timestamp"], "pack_id": "fixture",
                **values["composed"], "authorial_core_sha256": "b"*64, "intent_lock_sha256": "c"*64}
            with patch.object(bridge, "value", side_effect=lambda state,role: values[role]), patch.object(bridge, "bound_path", return_value=reference):
                self.assertEqual(bridge.validate_native_record(Path(plan["plan"]), self.state["artifacts"]["native_plan"]["sha256"], entry)["candidate_pack_version"], "v10")
                with self.assertRaisesRegex(ValueError, "operation_mismatch"):
                    bridge.validate_native_record(Path(plan["plan"]), self.state["artifacts"]["native_plan"]["sha256"], {**entry, "workflow_operation_id": plan["operation_id"]+":1"})

    def test_native_recorder_recovery_never_calls_provider(self):
        op = self.state["operations"][0]
        op["status"] = "recorder_failed"
        op["record_event"] = {"stage": "record_ready", "attempt": 1, "outcome": "safety_block", "provider_outcome": "rejected", "ledger_args": ["saved-exact-args"]}
        self.state["phase"] = "invocation_reserved"
        with patch.object(workflow, "load_state", return_value=self.state), patch.object(api, "record", return_value={"run_id": "parent-row"}) as record, \
                patch.object(api, "call_api", side_effect=AssertionError("must not call")):
            workflow.resume(NS(run=self.run))
        record.assert_called_once_with(["saved-exact-args"])
        self.assertEqual(op["status"], "provider_blocked")

    def test_new_authorization_can_extend_only_total_budget_and_keeps_history(self):
        scope = {**self.state["render_scope"], "invocation_limit": 4, "authorization_source": "new actual human instruction"}
        path = self.run / "scope.json"; path.write_text(json.dumps(scope))
        workflow.authorize(NS(run=self.run, scope=path))
        self.assertEqual(self.state["render_scope"]["invocation_limit"], 4)
        self.assertEqual(self.state["render_scope_history"][0]["invocation_limit"], 3)
        scope["invocation_limit"] = 5; path.write_text(json.dumps(scope))
        with self.assertRaisesRegex(ValueError, "new_source"): workflow.authorize(NS(run=self.run, scope=path))


if __name__ == "__main__":
    unittest.main()
