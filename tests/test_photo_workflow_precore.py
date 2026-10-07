"""Current authored inputs work in a process with candidate reads prohibited."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "skills/photo-prompt-image-generator/precore"
FIXTURE = ROOT / "tests/fixtures/photo_prompt/camera_authoring_path_v1/en_open"
sys.path.insert(0, str(PRE))
import prepare_photo_run as preparation
import photo_run_files as files
import photo_authoring_wire as wire


def freeze_fixture(directory, *, mode="prompt_only", overrides=None):
    request = json.loads((FIXTURE / "request-envelope.json").read_bytes())
    raw_path = directory / "request.txt"; raw_path.write_bytes(request["request_text"].encode("utf-8"))
    spans = directory / "spans.json"; spans.write_text(json.dumps([{k: row[k] for k in ("span_id", "start", "end")} for row in request["active_spans"]]))
    run = directory / "run"
    preparation.init(argparse.Namespace(request=raw_path, spans=spans, whole_request=False, request_id=request["request_id"], run=run, mode=mode))
    controls = json.loads((FIXTURE / "creative-controls.json").read_bytes())
    context = directory / "context.json"; context.write_text(json.dumps(controls["context"]))
    override = directory / "overrides.json"; override.write_text(json.dumps({**{k: v["value"] for k, v in controls["controls"].items()}, **(overrides or {})}))
    preparation.controls(argparse.Namespace(run=run, context=context, overrides=override, seed=17))
    core = json.loads((FIXTURE / "authorial-core.json").read_bytes()); core.pop("creative_controls_sha256")
    selection = json.loads((FIXTURE / "precore_feature_selection.json").read_bytes()); selection = {"selected": selection["selected"]}
    review = json.loads((FIXTURE / "embodiment-review.json").read_bytes()); review.pop("prompt_sha256")
    paths = {}
    for label, payload in (("core", core), ("selection", selection), ("review", review)):
        paths[label] = directory / (label + ".json"); paths[label].write_text(json.dumps(payload, ensure_ascii=False))
    args = argparse.Namespace(run=run, **paths)
    preparation.freeze(args)
    return run, args


class PhotoWorkflowPrecoreTests(unittest.TestCase):
    def test_freeze_same_normalizers_and_raw_wire_reentry(self):
        with tempfile.TemporaryDirectory() as temp:
            run, args = freeze_fixture(Path(temp))
            state = files.load_state(run)
            envelope, core, _ = files.verify_freeze(state)
            self.assertEqual(envelope["request_text"].encode(), files.bound_path(state, "request_raw").read_bytes())
            self.assertNotIn("canonical_sha256", files.value(state, "request_envelope_input"))
            self.assertEqual(core["canonical_sha256"], files.value(state, "freeze_receipt")["contracts"]["core"])
            self.assertTrue(preparation.freeze(args)["reused"])
            args.review.write_text(args.review.read_text() + "\n")
            with self.assertRaisesRegex(ValueError, "frozen_inputs_changed"):
                preparation.freeze(args)

    def test_utf8_crlf_and_explicit_repeated_offsets(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp); text = "한글😀\r\n반복 반복"; raw = text.encode("utf-8")
            request = directory / "request"; request.write_bytes(raw)
            spans = directory / "spans"; spans.write_text(json.dumps([{"span_id": "last", "start": len(text) - 2, "end": len(text)}]))
            run = directory / "run"
            preparation.init(argparse.Namespace(request=request, spans=spans, whole_request=False, request_id="unicode", run=run, mode="prompt_only"))
            envelope = files.value(files.load_state(run), "request_envelope_input")
            self.assertEqual(envelope["request_sha256"], hashlib.sha256(raw).hexdigest())
            self.assertEqual(envelope["active_spans"][0]["text"], "반복")
            self.assertEqual(files.bound_path(files.load_state(run), "request_raw").read_bytes(), raw)
            with self.assertRaises(ValueError): wire.normalize_request_envelope({**envelope, "envelope_id": "extra"})

    def test_missing_decisions_and_noncanonical_review_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp); run, args = freeze_fixture(directory)
            other = directory / "other"; other.mkdir()
            request = files.value(files.load_state(run), "request_envelope_input")
            # Deliberately stale a frozen byte, without updating its receipt.
            core_path = files.bound_path(files.load_state(run), "authorial_core_input")
            core_path.write_bytes(core_path.read_bytes() + b" ")
            with self.assertRaisesRegex(ValueError, "stale_artifact"): files.verify_freeze(files.load_state(run))

    def test_full_neutral_flow_denies_assets_scripts_network(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            # Inputs copied before the restricted process starts. It cannot read fixtures.
            import shutil
            for label in ("request-envelope", "creative-controls", "authorial-core", "precore_feature_selection", "embodiment-review"):
                shutil.copy2(FIXTURE / (label + ".json"), directory / (label + ".json"))
            code = r'''
import sys, pathlib, json, argparse
directory, pre = map(pathlib.Path, sys.argv[1:])
def guard(event, args):
    if event in {"socket.connect", "socket.getaddrinfo"}: raise AssertionError("network access")
    if event == "open" and isinstance(args[0], (str, bytes)):
        p = pathlib.Path(args[0]).resolve()
        if any(part in {"assets", "scripts", "references", "fixtures", "generations"} for part in p.parts):
            raise AssertionError("forbidden read")
sys.addaudithook(guard)
sys.path.insert(0, str(pre))
import prepare_photo_run as tool
from photo_run_files import load_state, value
envelope = json.loads((directory / "request-envelope.json").read_bytes())
(directory / "request.txt").write_bytes(envelope["request_text"].encode())
(directory / "spans.json").write_text(json.dumps([{k: v[k] for k in ("span_id", "start", "end")} for v in envelope["active_spans"]]))
run = directory / "run"
tool.init(argparse.Namespace(run=run, request=directory / "request.txt", spans=directory / "spans.json", whole_request=False, mode="prompt_only", request_id=envelope["request_id"]))
snapshot = json.loads((directory / "creative-controls.json").read_bytes())
(directory / "context").write_text(json.dumps(snapshot["context"]))
(directory / "overrides").write_text(json.dumps({k: v["value"] for k,v in snapshot["controls"].items()}))
tool.controls(argparse.Namespace(run=run, context=directory / "context", overrides=directory / "overrides", seed=17))
core_path = directory / "authorial-core.json"
core = json.loads(core_path.read_bytes()); core.pop("creative_controls_sha256"); core_path.write_text(json.dumps(core))
tool.freeze(argparse.Namespace(run=run, core=core_path, selection=directory / "precore_feature_selection.json", review=directory / "embodiment-review.json"))
assert not any("prompt_generator" in k or "photo_runtime_sources" in k for k in sys.modules)
'''
            child = subprocess.run([sys.executable, "-c", code, str(directory), str(PRE)], capture_output=True, text=True)
            self.assertEqual(child.returncode, 0, child.stderr)


if __name__ == "__main__": unittest.main()
