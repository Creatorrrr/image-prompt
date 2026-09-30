"""Offline checks for native capture, complete HTTP errors, and recorder binding."""
from __future__ import annotations

import base64
import contextlib
import copy
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPTS))
import generate_images_via_api as api
import image_attempt_evidence as evidence
import record_image_run as recorder

PROMPT, NEGATIVE = "A copper bell in window light.", "low resolution"
RUNTIME = PROMPT + "\n\nAvoid: " + NEGATIVE


def context(attempt=1):
    return {"tool": "openai_images_api", "generation_environment": "openai_images_api", "attempt": attempt,
            "invocation_outcome": "rejected", "request": {"prompt_en": PROMPT, "negative_en": NEGATIVE, "runtime_prompt_en": RUNTIME}}


def provider_body(message="Rejected", code="moderation_blocked"):
    return json.dumps({"error": {"message": message, "code": code, "type": "image_generation_user_error",
        "request_id": "body-request-id", "moderation_details": {"moderation_stage": "output", "categories": ["sexual"]}}}).encode()


class ApiErrorEvidenceTests(unittest.TestCase):
    def run_wrapper(self, body, *, attempts=1, recorder_failure=False, local_save_failure=False, evidence_save_failure=False):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            prompt = temp / "fixture.prompt.json"
            prompt.write_text(json.dumps({"prompt_en": PROMPT, "negative_en": NEGATIVE}))
            ledger = temp / "ledger.ndjson"
            recorder_calls = []
            def record(flags):
                recorder_calls.append(flags)
                if recorder_failure:
                    raise RuntimeError("fixture recorder failure")
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    status = recorder.main(flags + ["--ledger", str(ledger)])
                if status:
                    raise RuntimeError("fixture recorder rejected evidence")
                return json.loads(output.getvalue())
            error = urllib.error.HTTPError("https://offline.invalid", 400, "fixture", {"x-request-id": "header-request-id"}, body if hasattr(body, "read") else io.BytesIO(body))
            original_write_bytes = Path.write_bytes
            def write_bytes(path, data):
                if local_save_failure and path.suffix == ".png":
                    raise OSError("fixture image save failed")
                return original_write_bytes(path, data)
            api_response = {"return_value": b"offline image bytes"} if local_save_failure else {"side_effect": error}
            evidence_writer = {"side_effect": OSError("fixture evidence save failed")} if evidence_save_failure else {"wraps": evidence.write_evidence}
            with mock.patch.object(api, "call_api", **api_response) as calls, mock.patch.object(api, "record", side_effect=record), mock.patch.object(api, "write_evidence", **evidence_writer), mock.patch.object(Path, "write_bytes", new=write_bytes), mock.patch("urllib.request.urlopen", side_effect=AssertionError("network forbidden")), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                ok = api.generate_for_file(prompt, key="unused-fixture", model="fixture-model", size="1024x1536", attempts=attempts, concept=None, slug=None, out_base=temp / "results", timestamp="offline")
            rows = [json.loads(line) for line in ledger.read_text().splitlines()] if ledger.exists() else []
            captured = [json.loads(p.read_text()) for p in sorted((temp / "results").rglob("*.error.json"))]
            if rows:
                row = rows[0]
                self.assertEqual(row["attempt_evidence_sha256"], hashlib.sha256(Path(row["attempt_evidence_path"]).read_bytes()).hexdigest())
                schema = json.loads((SCRIPTS.parent / "assets/run_ledger.schema.json").read_text())
                self.assertFalse(set(row) - set(schema["properties"]))
                self.assertEqual(set(row["error_details"]), set(schema["properties"]["error_details"]["required"]))
            return ok, calls.call_count, rows, captured, len(recorder_calls)

    def test_long_http_error_retains_full_bytes_and_structured_fields(self):
        body = provider_body("Rejected by safety system. " + "x" * 800)
        ok, count, rows, captured, _ = self.run_wrapper(body)
        self.assertFalse(ok)
        self.assertEqual(count, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "safety_block")
        self.assertEqual(rows[0]["error_details"]["request_id"], "header-request-id")
        self.assertEqual(rows[0]["error_details"]["request_id_source"], "response_header")
        self.assertEqual(rows[0]["error_details"]["moderation_stage"], "output")
        self.assertEqual(rows[0]["error_details"]["categories"], ["sexual"])
        self.assertEqual(base64.b64decode(captured[0]["raw_error"]["value"]["base64"]), body)
        self.assertEqual(captured[0]["raw_error"]["fidelity"], "exact_bytes")
        self.assertLessEqual(len(rows[0]["failure_reason"]), 280)

    def test_non_utf8_response_is_recorded_with_exact_bytes(self):
        body = b"\xff\xfe gateway safety moderation error"
        _, count, rows, captured, _ = self.run_wrapper(body)
        self.assertEqual(count, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "error")
        self.assertEqual(base64.b64decode(captured[0]["raw_error"]["value"]["base64"]), body)
        self.assertIn("display_utf8_replacement", captured[0]["raw_error"]["limitations"])

    def test_safety_word_and_malformed_payload_do_not_classify_moderation(self):
        for body in (b'{"error":{"message":"Invalid safety parameter","code":"invalid_value"}}', b"<html>safety gateway moderation</html>", b'{"error":broken'):
            with self.subTest(body=body):
                _, _, rows, _, _ = self.run_wrapper(body)
                self.assertEqual(rows[0]["status"], "error")
                self.assertEqual(rows[0]["error_details"]["classification_source"], "unclassified")

    def test_body_read_failure_records_unavailable_fidelity(self):
        class BrokenStream(io.BytesIO):
            def read(self, *args):
                raise OSError("fixture body read failed")
        _, count, rows, captured, _ = self.run_wrapper(BrokenStream())
        self.assertEqual(count, 1)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "error")
        self.assertEqual(rows[0]["error_capture_fidelity"], "unavailable")
        self.assertEqual(rows[0]["error_details"]["request_id"], "header-request-id")
        self.assertIn("http_body_read_failed", captured[0]["raw_error"]["limitations"][0])

    def test_recorder_failure_stops_retries_and_keeps_error_evidence(self):
        _, count, rows, captured, recorder_calls = self.run_wrapper(provider_body(), attempts=4, recorder_failure=True)
        self.assertEqual((count, recorder_calls, len(rows), len(captured)), (1, 1, 0, 1))

    def test_local_image_save_failure_records_returned_call_without_regeneration(self):
        ok, count, rows, captured, recorder_calls = self.run_wrapper(b"", attempts=4, local_save_failure=True)
        self.assertFalse(ok)
        self.assertEqual((count, recorder_calls, len(rows), len(captured)), (1, 1, 1, 1))
        self.assertEqual(rows[0]["status"], "error")
        self.assertEqual(rows[0]["attempt"], 1)
        self.assertEqual(captured[0]["invocation_outcome"], "returned")
        self.assertEqual(captured[0]["raw_error"]["kind"], "python_exception")
        self.assertIn("image save failed", rows[0]["failure_reason"])

    def test_evidence_save_failure_stops_before_retry_or_unbound_ledger_row(self):
        _, count, rows, captured, recorder_calls = self.run_wrapper(provider_body(), attempts=4, evidence_save_failure=True)
        self.assertEqual((count, recorder_calls, len(rows), len(captured)), (1, 0, 0, 0))


class EvidenceBindingTests(unittest.TestCase):
    def test_schema_keeps_error_fields_bound_and_supported_fidelities_in_sync(self):
        schema = json.loads((SCRIPTS.parent / "assets/run_ledger.schema.json").read_text())
        self.assertEqual(set(schema["properties"]["error_capture_fidelity"]["enum"]), evidence.CAPTURE_FIDELITIES)
        for key in ("attempt_evidence_sha256", "error_capture_fidelity", "error_details"):
            self.assertIn("attempt_evidence_path", schema["dependencies"][key])
        required_with_path = {"attempt_evidence_sha256", "error_capture_fidelity", "error_details", "generation_environment"}
        self.assertTrue(required_with_path <= set(schema["dependencies"]["attempt_evidence_path"]))

    def test_legacy_namespace_without_optional_evidence_fields_keeps_output(self):
        args = recorder.parse_args(["--ts", "2026-09-30T00:00:00Z", "--prompt-en", PROMPT, "--attempt", "1", "--status", "error", "--failure-reason", "raw original failure"])
        expected = recorder.build_entry(args)
        for name in ("generation_environment", "attempt_evidence_json", "attempt_evidence_sha256"):
            delattr(args, name)
        self.assertEqual(recorder.build_entry(args), expected)
        self.assertEqual(expected["failure_reason"], "raw original failure")

    def test_writer_cli_retains_unicode_and_refuses_existing_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "작업 ' $().json"
            record = evidence.capture_api_error(RuntimeError("원문 오류 🧭"), context())
            command = [sys.executable, "-B", str(SCRIPTS / "image_attempt_evidence.py"), "--write-json", str(path)]
            completed = subprocess.run(command, input=json.dumps(record), capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(path.read_text()), record)
            self.assertEqual(json.loads(completed.stdout)["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            repeated = subprocess.run(command, input=json.dumps(record), capture_output=True, text=True)
            self.assertEqual(repeated.returncode, 2)
            self.assertEqual(json.loads(path.read_text()), record)

    def test_context_and_sha_mutations_are_rejected_before_ledger_write(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            record = evidence.capture_api_error(RuntimeError("fixture"), context())
            path = temp / "evidence.json"
            digest = evidence.write_evidence(path, record)
            base = ["--ts", "2026-09-30T00:00:00Z", "--prompt-en", PROMPT, "--negative-en", NEGATIVE, "--attempt", "1", "--status", "error", "--tool", "openai_images_api", "--generation-environment", "openai_images_api", "--attempt-evidence-json", str(path), "--attempt-evidence-sha256", digest, "--ledger", str(temp / "ledger.ndjson")]
            valid = recorder.build_entry(recorder.parse_args(base))
            self.assertEqual(valid["attempt_evidence_sha256"], digest)
            self.assertEqual(valid["failure_reason"], "fixture")
            for flag, wrong in (("--attempt", "2"), ("--tool", "image_gen"), ("--status", "safety_block"), ("--prompt-en", "changed prompt"), ("--negative-en", "changed negative"), ("--generation-environment", "ChatGPT"), ("--attempt-evidence-sha256", "0" * 64)):
                with self.subTest(flag=flag):
                    flags = list(base)
                    flags[flags.index(flag) + 1] = wrong
                    with contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(recorder.main(flags), 2)
                    self.assertFalse((temp / "ledger.ndjson").exists())
            changed = copy.deepcopy(record)
            changed["request"]["runtime_prompt_en"] = RUNTIME + " extra runtime prose"
            path.write_text(json.dumps(changed))
            flags = [x for x in base]
            flags[flags.index("--attempt-evidence-sha256") + 1] = hashlib.sha256(path.read_bytes()).hexdigest()
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(recorder.main(flags), 2)
            self.assertFalse((temp / "ledger.ndjson").exists())

    def test_evidence_writer_does_not_replace_a_previous_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "attempt.json"
            record = evidence.capture_api_error(RuntimeError("first error"), context())
            digest = evidence.write_evidence(path, record)
            with self.assertRaises(FileExistsError):
                evidence.write_evidence(path, evidence.capture_api_error(RuntimeError("second error"), context()))
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)

    def test_error_evidence_is_copied_into_independent_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "attempt.json"
            record = evidence.capture_api_error(RuntimeError("fixture"), context())
            evidence.write_evidence(path, record)
            args = recorder.parse_args(["--ts", "2026-09-30T00:00:00Z", "--prompt-en", PROMPT, "--negative-en", NEGATIVE, "--attempt", "1", "--status", "error", "--tool", "openai_images_api", "--attempt-evidence-json", str(path), "--arm-id", "arm", "--worktree-id", "fixture", "--skill-sha256", "a" * 64, "--source-ref", "fixture", "--candidate-pack-version", "v6", "--authorial-core-sha256", "b" * 64, "--intent-lock-sha256", "c" * 64, "--image-call-count", "1", "--independent-no-cross-arm-inputs"])
            row = recorder.build_entry(args)
            manifest = recorder.build_independent_manifest(row, args)
            for key in ("attempt_evidence_path", "attempt_evidence_sha256", "error_capture_fidelity", "error_details", "generation_environment"):
                self.assertEqual(manifest[key], row[key])


@unittest.skipUnless(shutil.which("node"), "Node is required to exercise the native V8 helper offline")
class NativeCaptureTests(unittest.TestCase):
    def native(self, code):
        script = "const fs=require('fs'),vm=require('vm');const capture=vm.runInNewContext(fs.readFileSync(" + json.dumps(str(SCRIPTS / "capture_image_tool_error.js")) + ",'utf8'));const context={tool:'image_gen.imagegen',generation_environment:'codex_native',attempt:1,prompt_en:" + json.dumps(PROMPT) + ",negative_en:" + json.dumps(NEGATIVE) + ",runtime_prompt_en:" + json.dumps(RUNTIME) + "};" + code
        result = subprocess.run([shutil.which("node"), "-e", script], capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_string_and_plain_object_provider_errors_preserve_metadata(self):
        result = self.native("const provider={error:{message:'Rejected; request ID fixture-request-id',code:'moderation_blocked',moderation_details:{moderation_stage:'output',categories:['sexual']}}};const raw='image generation failed: http 400 Bad Request: Some('+JSON.stringify(JSON.stringify(provider))+')';console.log(JSON.stringify([raw,capture(raw,context),capture(provider,context)]));")
        raw, string, obj = result
        self.assertEqual(string["raw_error"]["value"], raw)
        self.assertEqual(string["raw_error"]["fidelity"], "exact_string")
        for record in (string, obj):
            self.assertEqual(record["outcome"]["status"], "safety_block")
            self.assertEqual(record["outcome"]["request_id"], "fixture-request-id")
            self.assertEqual(record["outcome"]["moderation_stage"], "output")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "native.json"
            digest = evidence.write_evidence(path, string)
            entry = recorder.build_entry(recorder.parse_args(["--ts", "2026-09-30T00:00:00Z", "--prompt-en", PROMPT, "--negative-en", NEGATIVE, "--attempt", "1", "--status", "safety_block", "--tool", "image_gen.imagegen", "--attempt-evidence-json", str(path), "--attempt-evidence-sha256", digest]))
            self.assertEqual(entry["generation_environment"], "codex_native")

    def test_non_error_values_cycles_getters_and_proxies_cannot_break_capture(self):
        result = self.native("let getterCalls=0;const cycle={};cycle.self=cycle;const getter=Object.defineProperty({},'message',{get(){getterCalls++;throw Error('getter');}});const proxy=new Proxy({},{ownKeys(){throw Error('proxy');}});const revoked=Proxy.revocable({},{});revoked.revoke();const error=new Error('outer',{cause:new Error('inner')});const values=[null,undefined,4n,Symbol('fixture'),NaN,cycle,getter,proxy,revoked.proxy,error];console.log(JSON.stringify({getterCallsBefore:getterCalls,results:values.map(v=>capture(v,context)),getterCallsAfter:getterCalls}));")
        self.assertEqual(result["getterCallsAfter"], 0)
        records = result["results"]
        self.assertEqual(len(records), 10)
        self.assertTrue(all(row["outcome"]["status"] == "error" for row in records))
        self.assertEqual(records[1]["raw_error"]["value"]["type"], "undefined")
        self.assertEqual(records[2]["raw_error"]["value"], {"type": "bigint", "value": "4"})
        self.assertEqual(records[5]["raw_error"]["value"]["properties"]["self"]["type"], "reference")
        self.assertIn("accessor_not_evaluated", records[6]["raw_error"]["limitations"])
        self.assertIn("property_capture_failed", records[7]["raw_error"]["limitations"])
        self.assertEqual(records[-1]["raw_error"]["value"]["properties"]["cause"]["properties"]["message"], "inner")

    def test_generic_safety_word_stays_unclassified(self):
        result = self.native("console.log(JSON.stringify(capture({message:'Invalid safety parameter',code:'invalid_value'},context)));")
        self.assertEqual(result["outcome"]["status"], "error")
        self.assertEqual(result["outcome"]["classification_source"], "unclassified")

    def test_category_limits_keep_fidelity_truthful_and_exact_strings_intact(self):
        result = self.native("const p={error:{code:'moderation_blocked',moderation_details:{categories:Array.from({length:129},(_,i)=>'category'+i)}}};console.log(JSON.stringify([capture(p,context),capture(JSON.stringify(p),context)]));")
        obj, string = result
        self.assertEqual(len(obj["outcome"]["categories"]), 128)
        self.assertIn("category_limit", obj["raw_error"]["limitations"])
        self.assertEqual(obj["raw_error"]["fidelity"], "limited_capture")
        self.assertIn("category_limit", string["raw_error"]["limitations"])
        self.assertEqual(string["raw_error"]["fidelity"], "exact_string")

    def test_lone_surrogate_raw_string_survives_file_and_ledger_binding(self):
        record = self.native("console.log(JSON.stringify(capture('raw \\ud800 and 🧭',context)));")
        self.assertEqual(record["raw_error"]["value"], "raw \ud800 and 🧭")
        self.assertEqual(record["raw_error"]["fidelity"], "exact_string")
        self.assertIn("display_surrogate_replacement", record["raw_error"]["limitations"])
        self.assertEqual(record["outcome"]["display_message"], "raw \ufffd and 🧭")
        with tempfile.TemporaryDirectory() as directory:
            path, ledger = Path(directory) / "native.json", Path(directory) / "ledger.ndjson"
            digest = evidence.write_evidence(path, record)
            self.assertIn(b"\\ud800", path.read_bytes())
            self.assertEqual(json.loads(path.read_bytes()), record)
            flags = ["--ts", "2026-09-30T00:00:00Z", "--prompt-en", PROMPT, "--negative-en", NEGATIVE, "--attempt", "1", "--status", "error", "--tool", "image_gen.imagegen", "--attempt-evidence-json", str(path), "--attempt-evidence-sha256", digest, "--ledger", str(ledger)]
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(recorder.main(flags), 0)
            row = json.loads(ledger.read_text())
            self.assertEqual(row["attempt_evidence_sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(row["failure_reason"], "raw \ufffd and 🧭")

    def test_documented_native_template_saves_literal_shell_text_and_stops_on_write_failure(self):
        document = (SCRIPTS.parent / "references/image-runtime.md").read_text()
        blocks = re.findall(r"```javascript\n([\s\S]*?)\n```", document)
        template = next(block for block in blocks if 'const capture = eval(load("photo_error_capture_source"))' in block)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "native ' `touch injected` $(touch injected).json"
            script = "\n".join([
                "const fs=require('fs'),cp=require('child_process');const values=new Map();",
                "const store=(k,v)=>values.set(k,v),load=k=>values.get(k);const text=()=>{};let calls=0;",
                "const tools={image_gen__imagegen:async()=>{calls++;throw 'original \\ud800 \\nPHOTO_NATIVE_ERROR_JSON\\n$(touch injected)';},exec_command:async args=>{const r=cp.spawnSync('/bin/zsh',['-c',args.cmd],{cwd:args.workdir,encoding:'utf8'});return {exit_code:r.status,output:r.stdout};}};",
                "store('photo_error_capture_source',fs.readFileSync(" + json.dumps(str(SCRIPTS / "capture_image_tool_error.js")) + ",'utf8'));",
                "store('photo_runtime_workdir'," + json.dumps(str(ROOT)) + ");",
                "store('photo_native_args',{prompt:" + json.dumps(RUNTIME) + "});",
                "store('photo_composed',{prompt_en:" + json.dumps(PROMPT) + ",negative_en:" + json.dumps(NEGATIVE) + "});",
                "store('photo_attempt',1);store('photo_error_evidence_path'," + json.dumps(str(path)) + ");",
                "const run=async()=>{", template, "};",
                "(async()=>{await run();const first=fs.readFileSync(load('photo_error_evidence_path'),'utf8');let writeFailure=null;try{await run();}catch(e){writeFailure=e.message;}console.log(JSON.stringify({calls,first,unchanged:first===fs.readFileSync(load('photo_error_evidence_path'),'utf8'),writeFailure,evidence:load('photo_attempt_error_evidence'),saved:load('photo_attempt_error_file')}));})().catch(e=>{console.error(e);process.exitCode=1;});",
            ])
            result = subprocess.run([shutil.which("node"), "-e", script], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            saved = json.loads(result.stdout)
            self.assertEqual(saved["calls"], 2)  # One mock invocation for each explicit template run.
            self.assertTrue(saved["unchanged"])
            self.assertIn("do not retry", saved["writeFailure"])
            self.assertEqual(json.loads(saved["first"])["raw_error"], saved["evidence"]["raw_error"])
            self.assertEqual(saved["saved"]["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(list(Path(directory).iterdir()), [path])
            self.assertFalse((ROOT / "injected").exists())


if __name__ == "__main__":
    unittest.main()
