"""Real pinned audits with a fake provider, including rejected-input calls=0."""
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from tests import photo_api_fixtures as fixtures
import generate_images_via_api as api
import photo_api_render as preflight
import record_image_run as recorder


class PhotoApiRenderPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.paths = fixtures.write_valid_inputs(self.directory)
        patch = mock.patch.object(preflight.RuntimeSnapshotProvider, "from_receipt", new=fixtures.verified_fixture_receipt)
        patch.start(); self.addCleanup(patch.stop)

    def prepare(self):
        p = self.paths
        return preflight.prepare_api_render(p["pack_file"], p["receipt_file"], p["composed_file"], p["request_file"],
            model="fixture-model", size="1024x1536", runtime_store=p["runtime_store"])

    def execute(self, **extra):
        def inline_record(flags):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                result = recorder.main(flags)
            if result: raise RuntimeError("fixture recorder rejected input")
            return json.loads(output.getvalue())
        self.stderr = io.StringIO()
        with mock.patch.object(api, "record", side_effect=inline_record), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(self.stderr):
            return api.generate_for_request(**self.paths, model="fixture-model", size="1024x1536", attempts=2,
                concept="fixture", slug=None, out_base=self.directory / "results", timestamp="offline", ledger=self.directory / "ledger.ndjson", **extra)

    def mutate(self, label, mutate):
        p = self.paths[label + "_file"]
        value = json.loads(p.read_text()); mutate(value); p.write_text(json.dumps(value))

    def test_real_dry_run_no_key_network_or_attempt(self):
        with mock.patch.object(api, "load_api_key", side_effect=AssertionError("key forbidden")) as key, mock.patch.object(api, "call_api", side_effect=AssertionError("call forbidden")) as call:
            self.assertTrue(self.execute(dry_run=True))
        self.assertEqual(key.call_count, 0); self.assertEqual(call.call_count, 0)
        self.assertFalse((self.directory / "ledger.ndjson").exists())
        self.assertEqual(len(list((self.directory / "results").rglob("preflight.json"))), 1)

    def test_bad_receipt_fails_before_key_or_provider(self):
        self.mutate("receipt", lambda r: r.update(generation_id="bad"))
        with mock.patch.object(api, "load_api_key", side_effect=AssertionError("key forbidden")) as key, mock.patch.object(api, "call_api") as call:
            self.assertFalse(self.execute())
        self.assertEqual(key.call_count, 0); self.assertEqual(call.call_count, 0)

    def test_pack_and_runtime_binding_tampering(self):
        for field in ["pack_id", "core_retrieval_sha256", "source_intent_lock_sha256", "source_embodiment_preflight_sha256", "render_repair_contract_sha256"]:
            self.paths = fixtures.write_valid_inputs(self.directory)
            self.mutate("request", lambda r: r.update({field: "0" * 64}))
            with self.subTest(field=field), mock.patch.object(api, "call_api") as call:
                self.assertFalse(self.execute(key="unused")); self.assertEqual(call.call_count, 0)

    def test_self_declared_pass_does_not_replace_audit(self):
        self.mutate("composed", lambda r: r.update(prompt_en="unrelated invented image", audit_status="pass"))
        with mock.patch.object(api, "call_api") as call:
            self.assertFalse(self.execute(key="unused")); self.assertEqual(call.call_count, 0)

    def test_negative_runtime_additions_and_references_fail_without_rewrite(self):
        reference = self.directory / "reference.png"; reference.write_bytes(b"reference fixture")
        import hashlib
        for mutation in [lambda r:r.update(runtime_negative_en="changed"), lambda r:r.update(runtime_prompt_en=r["runtime_prompt_en"]+" Add another adult."),
            lambda r:r.update(references=[{"path":str(reference),"sha256":hashlib.sha256(reference.read_bytes()).hexdigest(),"role":"identity"}]),
            lambda r:r.update(references=[{"path":"missing.png","sha256":"0"*64}])]:
            self.paths = fixtures.write_valid_inputs(self.directory); self.mutate("request", mutation)
            with mock.patch.object(api, "call_api") as call:
                self.assertFalse(self.execute(key="unused")); self.assertEqual(call.call_count, 0)

    def test_raw_prompt_and_multiple_objects_are_rejected(self):
        self.paths["pack_file"].write_text(json.dumps({"prompt_en":"raw prompt","audit_status":"pass"}))
        with mock.patch.object(api, "call_api") as call:
            self.assertFalse(self.execute(key="unused")); self.assertEqual(call.call_count, 0)
        self.paths = fixtures.write_valid_inputs(self.directory)
        value = json.loads(self.paths["pack_file"].read_text())
        self.paths["pack_file"].write_text(json.dumps([value,value]))
        with self.assertRaises(preflight.PreflightError): self.prepare()

    def test_exact_transport_and_successful_ledger_binding(self):
        prepared = self.prepare(); expected = prepared.document["execution"]
        with mock.patch.object(api, "call_api", return_value=api.ApiImageResult(b"offline image")) as call, mock.patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")):
            self.assertTrue(self.execute(key="unused"), self.stderr.getvalue())
        self.assertEqual(call.call_count, 1)
        self.assertEqual(call.call_args.args[2].encode(), expected["runtime_prompt_en"].encode())
        row = json.loads((self.directory / "ledger.ndjson").read_text())
        self.assertEqual(row["requested_image_model"], "fixture-model"); self.assertIsNone(row["observed_image_model"])
        self.assertEqual(row["image_call_count"], 1); self.assertEqual(row["runtime_prompt_sha256"], expected["runtime_prompt_sha256"])
        self.assertEqual(len(row["image_hashes"]),1)
        schema = json.loads((api.SCRIPT_DIR.parent/"assets/run_ledger.schema.json").read_text())
        self.assertFalse(set(row)-set(schema["properties"]))

    def test_authorized_transient_retry_keeps_input_and_immediate_link(self):
        import urllib.error
        error = urllib.error.HTTPError("https://offline.invalid", 429, "fixture", {}, io.BytesIO(b'{"error":{"code":"rate_limit_exceeded"}}'))
        with mock.patch.object(api, "call_api", side_effect=[error, api.ApiImageResult(b"offline", "observed-model", "response-id")]) as call:
            self.assertTrue(self.execute(key="unused"), self.stderr.getvalue())
        rows = [json.loads(line) for line in (self.directory / "ledger.ndjson").read_text().splitlines()]
        self.assertEqual(call.call_count, 2)
        self.assertEqual(call.call_args_list[0].args[2], call.call_args_list[1].args[2])
        self.assertEqual(rows[1]["retry_of"], rows[0]["run_id"])
        self.assertEqual([row["image_call_count"] for row in rows], [1, 2])
        self.assertEqual(rows[1]["observed_image_model"], "observed-model")

    def test_copies_are_immutable_and_sidecar_is_independently_checked(self):
        prepared = self.prepare(); document = prepared.document
        document["execution"]["runtime_prompt_en"] = "changed"
        self.paths["request_file"].write_text("{}"); self.assertNotEqual(prepared.document, document)
        p = self.directory / "preflight.json"; sha = preflight.save_preflight(p, prepared)
        p.write_text("{}"); self.assertRaises(ValueError, preflight.validate_api_render_input, p, sha, {})

    def test_mutable_files_are_not_reread_after_preflight(self):
        expected = self.prepare().document["execution"]["runtime_prompt_en"]
        original = api.save_preflight
        def save_then_change(path, prepared):
            result = original(path, prepared)
            self.paths["request_file"].write_text("{}")
            return result
        with mock.patch.object(api, "save_preflight", side_effect=save_then_change), mock.patch.object(api, "call_api", return_value=api.ApiImageResult(b"offline")) as call:
            self.assertTrue(self.execute(key="unused"), self.stderr.getvalue())
        self.assertEqual(call.call_args.args[2], expected)

    def test_rehashed_forged_pass_is_recomputed_before_recording(self):
        document = self.prepare().document
        row = document["inputs"]["request"]
        row["value"]["runtime_prompt_en"] += " Add something unreviewed."
        row["raw_utf8"] = json.dumps(row["value"])
        row["sha256"] = preflight.text_digest(row["raw_utf8"])
        path = self.directory / "forged.json"; path.write_bytes(preflight.json_bytes(document))
        import hashlib
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        with self.assertRaises(ValueError): preflight.validate_api_render_input(path, sha, {})

    def test_observed_provider_metadata_and_decoded_payload(self):
        import base64
        class Response:
            headers = {"x-request-id": "observed-request"}
            def __enter__(self): return self
            def __exit__(self, *args): return None
            def read(self): return json.dumps({"model": "observed-model", "data": [{"b64_json": base64.b64encode(b"offline").decode()}]}).encode()
        text = "Exact 한국어\n\nAvoid: blur"
        with mock.patch("urllib.request.urlopen", return_value=Response()) as transport:
            result = api.call_api("unused", "requested-model", text, "1024x1536")
        sent = json.loads(transport.call_args.args[0].data)
        self.assertEqual(sent["prompt"].encode(), text.encode())
        self.assertEqual(sent["model"], "requested-model")
        self.assertEqual(result.observed_model, "observed-model")
        self.assertEqual(result.request_id, "observed-request")

    def test_positive_attempts_and_retired_cli_fail(self):
        args = ["--pack",str(self.paths["pack_file"]),"--runtime-receipt",str(self.paths["receipt_file"]),"--composed",str(self.paths["composed_file"]),"--render-request",str(self.paths["request_file"])]
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit): api.main(args+["--attempts","0"])
        result = subprocess.run([sys.executable,str(api.SCRIPT_DIR/"generate_images_via_api.py"),"--prompt-json",str(self.paths["composed_file"])],capture_output=True)
        self.assertEqual(result.returncode,2)

    def test_cli_dry_run(self):
        with mock.patch.object(api, "load_api_key", side_effect=AssertionError("key forbidden")), mock.patch.object(api, "call_api", side_effect=AssertionError("provider forbidden")), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(api.main(["--pack",str(self.paths["pack_file"]),"--runtime-receipt",str(self.paths["receipt_file"]),"--composed",str(self.paths["composed_file"]),"--render-request",str(self.paths["request_file"]),"--runtime-store",str(self.paths["runtime_store"]),"--out-base",str(self.directory/"results"),"--dry-run"]),0)
