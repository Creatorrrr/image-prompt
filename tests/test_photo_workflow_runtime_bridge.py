"""Actual audited offline workflows and invocation/recorder crash boundaries."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

from tests.test_photo_workflow_precore import freeze_fixture, files, ROOT
from tests.test_photo_workflow_state import workflow, recorder
from tests import photo_api_fixtures as fixtures
from tests import test_photo_authorship_policy as authorship
import generate_images_via_api as api
import photo_api_render as preflight


def inline_record(flags):
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        status = recorder.main(flags)
    if status: raise RuntimeError("record rejected")
    return json.loads(output.getvalue())


class PhotoWorkflowRuntimeBridgeTests(unittest.TestCase):
    def test_native_observed_file_parent_coordinator_and_child_freeze(self):
        from prepare_retry_context import prepare, recompute, attach_child
        from tests.test_photo_workflow_precore import preparation
        from photo_retry_projection import DECISION_FIELDS
        from photo_workflow_worker import audit_bound
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            run, _ = freeze_fixture(directory, mode="image", overrides={"sensual": 0, "fetish": 0, "surreal": 0, "creativity": 0})
            args = argparse.Namespace(run=run, seed=27, runtime_store=directory / "runtime", source_mode="local_current",
                                      source_remote=None, source_ref="main", visual_intent=None)
            with patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")):
                workflow.retrieve(args)
                pack = workflow.one(files.value(files.load_state(run), "pack"))
                composed = directory / "composed.json"; composed.write_text(json.dumps(authorship.PhotoAuthorshipPolicyTests.composed(pack)))
                self.assertEqual(workflow.compose_audit(argparse.Namespace(run=run, composed=composed))["status"], "pass")
                parameters = directory / "parameters"; parameters.write_text('{"references":[]}')
                self.assertEqual(workflow.prepare_render(argparse.Namespace(run=run, parameters=parameters, lane="native", model="offline", size="1024x1536"))["status"], "pass")
                scope = directory / "scope"; scope.write_text('{"lanes":["native"],"invocation_limit":1,"authorization_source":"offline test only"}')
                workflow.authorize(argparse.Namespace(run=run, scope=scope))
                plan = workflow.native_plan(argparse.Namespace(run=run)); started = workflow.native_started(argparse.Namespace(run=run))
                self.assertEqual(started["payload"], files.value(files.load_state(run), "native_plan")["payload"])
                with self.assertRaisesRegex(ValueError, "not_ready"): workflow.native_started(argparse.Namespace(run=run))
                image = directory / "observed-native.png"; image.write_bytes(b"observed offline native tool bytes")
                result = directory / "result.json"; result.write_text(json.dumps({"operation_id": plan["operation_id"], "outcome": "returned", "image_path": str(image)}))
                ledger = directory / "ledger"
                recorded = workflow.native_result(argparse.Namespace(run=run, result=result, ledger=ledger))
                row = json.loads(ledger.read_bytes()); self.assertEqual(recorded["ledger_run_id"], row["run_id"])
                self.assertEqual(row["image_hashes"][0]["sha256"], files.digest(image.read_bytes()))
                attempt = directory / "attempt.json"; attempt.write_bytes(files.encode(row))
                current = files.value(files.load_state(run), "request_envelope_input")
                current["request_id"] = "current-child-request"
                current_file = directory / "current-envelope.json"; current_file.write_bytes(files.encode(current))
                decision = {"schema_version": "photo-repair-decision/v1", "current_source_span_ids": ["topic"], "source_text": current["request_text"],
                    "preserved_dimensions": ["concept", "subject", "event"], "allowed_changes": ["lighting"], "requester_corrected_dimensions": [],
                    "allowed_properties": [], "local_axes": ["lighting"], "failed_gate_ids": [], "failure_class": "artistic_revision",
                    "additional_invocation_limit": 1, "obligation_dimensions": {}}
                decision_file = directory / "decision"; decision_file.write_bytes(files.encode(decision))
                extraction = argparse.Namespace(run=run, attempt=attempt, ledger=ledger, current_envelope=current_file, decision=decision_file, output=directory / "retry")
                self.assertEqual(prepare(extraction)["status"], "pass")
                self.assertTrue(prepare(extraction)["reused"])
                proof_path = extraction.output / "retry_proof.json"; context = files.read_json(extraction.output / "retry_context.json")
                self.assertEqual(context["parent_binding"]["image_sha256"], files.digest(image.read_bytes()))
                self.assertNotIn("baseline_prompt_en", context)
                legacy_row = {k: v for k, v in row.items() if k not in {"workflow_operation_id", "native_render_plan_json", "native_render_plan_sha256", "runtime_prompt_sha256"}}
                legacy_ledger = directory / "legacy-ledger"; legacy_ledger.write_bytes(files.encode(legacy_row).replace(b"\n", b" ").strip() + b"\n")
                legacy_attempt = directory / "legacy-attempt"; legacy_attempt.write_bytes(files.encode(legacy_row))
                state = files.load_state(run)
                manifest = directory / "legacy-parent-manifest"
                manifest.write_bytes(files.encode({"schema_version": "photo-retry-parent-artifacts/v1", "runtime_store": state["source_binding"]["runtime_store"],
                    "artifacts": {role: state["artifacts"][role]["path"] for role in ("request_envelope_input", "authorial_core_input", "creative_controls", "pack", "runtime_receipt", "composed", "render_request")}}))
                imported = argparse.Namespace(run=directory / "historical-parent", attempt=legacy_attempt, ledger=legacy_ledger,
                    current_envelope=current_file, decision=decision_file, output=directory / "legacy-retry", parent_manifest=manifest)
                self.assertEqual(prepare(imported)["status"], "pass")
                self.assertEqual(files.read_json(imported.output / "retry_context.json")["parent_binding"]["core_sha256"], context["parent_binding"]["core_sha256"])
                # Child authoring uses its real current requester input and fresh
                # selection/review; only derived lineage hashes are stamped.
                child = directory / "child"
                request = directory / "child-request"; request.write_bytes(current["request_text"].encode())
                spans = directory / "child-spans"; spans.write_bytes(files.encode([{k: s[k] for k in ("span_id", "start", "end")} for s in current["active_spans"]]))
                preparation.init(argparse.Namespace(run=child, request=request, spans=spans, whole_request=False, mode="image", request_id=current["request_id"]))
                parent_controls = files.value(files.load_state(run), "creative_controls")
                control_context = directory / "child-context"; control_context.write_bytes(files.encode(parent_controls["context"]))
                overrides = directory / "child-overrides"; overrides.write_bytes(files.encode({k: v["value"] for k, v in parent_controls["controls"].items()}))
                preparation.controls(argparse.Namespace(run=child, context=control_context, overrides=overrides, seed=17))
                attach_child(argparse.Namespace(run=child, proof=proof_path))
                core = files.value(files.load_state(run), "authorial_core_input"); core.pop("creative_controls_sha256")
                core["request_lineage"] = {"preserved_dimensions": decision["preserved_dimensions"], "allowed_changes": decision["allowed_changes"]}
                core_file = directory / "child-core"; core_file.write_bytes(files.encode(core))
                selection = directory / "child-selection"; selection.write_bytes(files.encode({"selected": files.value(files.load_state(run), "feature_selection")["selected"]}))
                review = directory / "child-review"; review.write_bytes(files.encode(files.value(files.load_state(run), "embodiment_review")))
                self.assertEqual(preparation.freeze(argparse.Namespace(run=child, core=core_file, selection=selection, review=review))["phase"], "core_frozen")
                image.write_bytes(b"changed native bytes")
                with self.assertRaisesRegex(ValueError, "stale_retry_parent"): recompute(files.read_json(proof_path))

    def test_native_error_wrapper_preserves_observation_and_explicit_code(self):
        from image_attempt_evidence import capture_native_error
        observation = {"isError": True, "content": [{"type": "text", "text": 'Some({"error":{"code":"moderation_blocked","request_id":"actual-observed-id"}})'}]}
        evidence = capture_native_error(observation, {"tool": "image_gen"})
        self.assertEqual(evidence["outcome"]["status"], "safety_block")
        self.assertEqual(evidence["raw_error"]["value"], observation)
        self.assertEqual(evidence["outcome"]["request_id"], "actual-observed-id")
        uncertain = capture_native_error({"message": "some text says moderation_blocked, no structured code"}, {})
        self.assertEqual(uncertain["outcome"]["status"], "error")

    def test_prompt_only_retrieve_pair_real_audits_and_current_publication(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp); run, _ = freeze_fixture(directory, overrides={"sensual": 0, "fetish": 0, "surreal": 0, "creativity": 0})
            args = argparse.Namespace(run=run, seed=27, runtime_store=directory / "runtime", source_mode="local_current",
                                      source_remote=None, source_ref="main", visual_intent=None)
            with patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")):
                self.assertEqual(workflow.retrieve(args)["phase"], "pack_bound")
                self.assertTrue(workflow.retrieve(args)["reused"])
                state = files.load_state(run); pack = workflow.one(files.value(state, "pack"))
                composed_path = directory / "authored-composed.json"
                composed_path.write_text(json.dumps(authorship.PhotoAuthorshipPolicyTests.composed(pack), ensure_ascii=False))
                result = workflow.compose_audit(argparse.Namespace(run=run, composed=composed_path))
                self.assertEqual(result["status"], "pass", result)
                parameters = directory / "parameters.json"; parameters.write_text('{"references":[]}')
                result = workflow.prepare_render(argparse.Namespace(run=run, parameters=parameters, lane="api", model="offline-model", size="1024x1536"))
                self.assertEqual(result["status"], "pass", result)
                self.assertEqual(files.load_state(run)["operations"], [])
                with patch.object(api, "load_api_key", side_effect=AssertionError("key forbidden")):
                    result = workflow.render_api(argparse.Namespace(run=run, dry_run=True, concept=None, attempts=2, ledger=directory / "ledger"))
                self.assertEqual(result["image_call_count"], 0)
                self.assertFalse((directory / "ledger").exists())
                composed_path.write_text('{"chosen_candidate_ids":[],"chosen_visual_concept_ids":[],"prompt_en":"forged","authorial_core_binding":{}}')
                rejected = workflow.compose_audit(argparse.Namespace(run=run, composed=composed_path))
                self.assertEqual(rejected["status"], "fail")
                self.assertEqual(files.load_state(run)["phase"], "runtime_audited")
                self.assertEqual(files.value(files.load_state(run), "composed")["prompt_en"], pack["authorial_core"]["baseline_prompt_en"])
                generation = directory / "runtime/generations" / files.value(state, "runtime_receipt")["generation_id"]
                manifest = json.loads((generation / "manifest.json").read_bytes())
                self.assertIn("precore/photo_authoring_wire.py", manifest["source"]["code"])

    def execute_fixture(self, directory, **extra):
        paths = fixtures.write_valid_inputs(directory)
        with patch.object(preflight.RuntimeSnapshotProvider, "from_receipt", new=fixtures.verified_fixture_receipt), patch.object(api, "record", side_effect=inline_record), contextlib.redirect_stdout(io.StringIO()):
            return api.generate_for_request(**paths, model="offline-model", size="1024x1536", attempts=extra.pop("attempts", 2),
                concept=None, slug=None, out_base=directory / "results", timestamp="offline", ledger=directory / "ledger", key="unused",
                workflow_operation_id="a" * 32, execution_summary=directory / "summary.json", **extra)

    def test_call_hook_and_timestamp_durable_before_provider_and_initial_retry_link(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            def provider(*args):
                summary = json.loads((directory / "summary.json").read_bytes())
                self.assertEqual(summary["status"], "invocation_started")
                self.assertEqual(summary["image_call_count"], 1)
                self.assertTrue(summary["attempts"][-1]["timestamp"])
                return api.ApiImageResult(b"offline result")
            with patch.object(api, "call_api", side_effect=provider) as call:
                self.assertTrue(self.execute_fixture(directory, initial_retry_of="parent-run"))
            row = json.loads((directory / "ledger").read_bytes()); summary = json.loads((directory / "summary.json").read_bytes())
            self.assertEqual(row["retry_of"], "parent-run"); self.assertEqual(call.call_count, 1)
            self.assertEqual(row["workflow_operation_id"], "a" * 32 + ":1")
            reserved = next(e for e in summary["attempts"] if e["stage"] == "invocation_started")
            self.assertEqual(row["run_id"], reserved["run_id"])
            ready = next(e for e in summary["attempts"] if e["stage"] == "record_ready")
            original = (directory / "ledger").read_bytes(); inline_record(ready["ledger_args"])
            self.assertEqual(original, (directory / "ledger").read_bytes())

    def test_transient_observed_code_consumes_actual_bound_budget(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            error = urllib.error.HTTPError("https://offline.invalid", 429, "offline", {}, io.BytesIO(b'{"error":{"code":"rate_limit_exceeded"}}'))
            with patch.object(api, "call_api", side_effect=error) as call:
                self.assertFalse(self.execute_fixture(directory, attempts=1))
            self.assertEqual(call.call_count, 1)
            self.assertEqual(json.loads((directory / "summary.json").read_bytes())["image_call_count"], 1)

    def test_missing_key_records_known_zero_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp); paths = fixtures.write_valid_inputs(directory)
            with patch.object(preflight.RuntimeSnapshotProvider, "from_receipt", new=fixtures.verified_fixture_receipt), patch.object(api, "load_api_key", side_effect=SystemExit("offline missing key")), patch.object(api, "call_api", side_effect=AssertionError("must not invoke")), contextlib.redirect_stdout(io.StringIO()):
                self.assertFalse(api.generate_for_request(**paths, model="offline-model", size="1024x1536", attempts=1, concept=None, slug=None,
                    out_base=directory / "results", timestamp="offline", ledger=directory / "ledger", workflow_operation_id="b" * 32,
                    execution_summary=directory / "summary.json"))
            summary = files.read_json(directory / "summary.json")
            self.assertEqual(summary["image_call_count"], 0); self.assertEqual(summary["status"], "preflight_failed")
            self.assertFalse((directory / "ledger").exists())

    def test_recorder_crash_keeps_returned_bytes_and_replays_no_image_call(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp); paths = fixtures.write_valid_inputs(directory)
            with patch.object(preflight.RuntimeSnapshotProvider, "from_receipt", new=fixtures.verified_fixture_receipt), patch.object(api, "call_api", return_value=api.ApiImageResult(b"saved returned bytes")) as call, patch.object(api, "record", side_effect=RuntimeError("offline recorder crash")), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertFalse(api.generate_for_request(**paths, model="offline-model", size="1024x1536", attempts=2, concept=None, slug=None,
                    out_base=directory / "results", timestamp="offline", ledger=directory / "ledger", key="unused",
                    workflow_operation_id="a" * 32, execution_summary=directory / "summary.json"))
            self.assertEqual(call.call_count, 1)
            self.assertEqual(next((directory / "results").rglob("*.returned-image.bin")).read_bytes(), b"saved returned bytes")
            summary = json.loads((directory / "summary.json").read_bytes()); self.assertEqual(summary["status"], "recorder_failed")
            ready = next(e for e in summary["attempts"] if e["stage"] == "record_ready")
            with patch.object(preflight.RuntimeSnapshotProvider, "from_receipt", new=fixtures.verified_fixture_receipt), patch.object(api, "call_api", side_effect=AssertionError("must not rerender")):
                inline_record(ready["ledger_args"])
                inline_record(ready["ledger_args"])
            self.assertEqual(len((directory / "ledger").read_bytes().splitlines()), 1)

    def test_unknown_resume_never_calls_and_repair_budget_counts_unique_attempts(self):
        with tempfile.TemporaryDirectory() as temp:
            run, _ = freeze_fixture(Path(temp), mode="image")
            with files.locked_state(run) as state:
                files.commit_stage(run, state, "runtime_audited", {"pack": files.encode({"render_repair": {"retry_policy": {"maximum_additional_attempts": 1}}}),
                    "runtime_receipt": b'{}', "composed": b'{}', "render_request": b'{}'})
                state["render_scope"] = {"lanes": ["api"], "invocation_limit": 5, "authorization_source": "offline test"}; files.save_state(run, state)
            op = workflow.reserve(run, "api", 2); self.assertEqual(op["budget"], 1)
            workflow.update_operation(run, op["operation_id"], {"stage": "invocation_started", "attempt": 1, "timestamp": "offline", "run_id": "offline"})
            with patch.object(api, "call_api", side_effect=AssertionError("no unknown reexecution")):
                result = workflow.resume(argparse.Namespace(run=run))
                self.assertEqual(result["operations"][0]["status"], "execution_unknown")
                with self.assertRaisesRegex(ValueError, "pending_operation"): workflow.reserve(run, "api", 1)
            workflow.update_operation(run, op["operation_id"], {"stage": "attempt_recorded", "terminal": True})
            with self.assertRaisesRegex(ValueError, "budget_exhausted"): workflow.reserve(run, "api", 1)


if __name__ == "__main__": unittest.main()
