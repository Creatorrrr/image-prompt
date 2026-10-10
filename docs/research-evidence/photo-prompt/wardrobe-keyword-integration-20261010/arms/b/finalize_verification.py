"""Verify only this arm's saved artifacts; no retrieval or generation calls."""
from pathlib import Path
import ast
import datetime
import hashlib
import json

b = Path(__file__).resolve().parent
root = b.parents[5]
load = lambda p: json.loads(Path(p).read_text())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks = []


def check(name, actual, expected):
    checks.append({"check": name, "pass": actual == expected,
                   "actual": actual, "expected": expected})


s = load(b / "run_requalification_01/workflow.json")
old = load(b / "run/workflow.json")
report = load(b / "ARM_B_REPORT.json")
manifest = load(b / "run_manifest.json")
c = load(b / "composed_prompt_audited.json")
for prefix, state in [("managed_artifact", s), ("original_managed_artifact", old)]:
    for name, ref in state["artifacts"].items():
        check(prefix + ":" + name, sha(ref["path"]), ref["sha256"])
for role in load(b / "requalification_preparation.json")["pairs"]:
    check("neutral_byte_equality:" + role,
          Path(s["artifacts"][role]["path"]).read_bytes()
          == Path(old["artifacts"][role]["path"]).read_bytes(), True)
check("request_envelope_immutable", sha(b / "request_envelope.json"),
      "7faf539417a1cf780578a41a8b544423b834fb7f7a6b68993b3d6443f02389cd")
check("canonical_skill_hash", sha(root / "skills/photo-prompt-image-generator/SKILL.md"),
      manifest["skill_sha256"])
check("reference_hash", sha("/tmp/codex-remote-attachments/01a1212e-a00b-7170-8446-16480b2873ff/BAA7D121-91EF-4AF5-A73E-C42EEEE77809/1-사진-1.jpg"),
      manifest["reference_sha256"][0])
check("exact_error_evidence_hash", sha(b / "attempt01_native_error.json"),
      manifest["attempt_evidence_sha256"])
check("final_prompt_matches_audited", (b / "final_prompt_en.txt").read_text() == c["prompt_en"], True)
check("prompt_text_sha256", hashlib.sha256(c["prompt_en"].encode()).hexdigest(),
      report["integrity_bindings"]["prompt_text_sha256"])
check("prompt_words", len(c["prompt_en"].split()), 658)
rows = [json.loads(x) for x in (b / "image_runs.ndjson").read_text().splitlines() if x.strip()]
check("ledger_row_count", len(rows), 1)
check("ledger_manifest_run_id", rows[0]["run_id"], manifest["ledger_run_id"])
for key in ["arm_id", "image_call_count", "image_paths", "status", "effective_visual_contract_sha256",
            "runtime_prompt_sha256", "reference_sha256", "source_ref", "skill_sha256", "cross_arm_inputs_used"]:
    check("ledger_manifest:" + key, rows[0][key], manifest[key])
check("image_calls", manifest["image_call_count"], 1)
check("no_returned_image_paths", manifest["image_paths"], [])
check("no_returned_image_hashes", manifest["image_hashes"], [])
check("provider_status", s["operations"][0]["status"], "provider_blocked")
check("one_native_operation", len(s["operations"]), 1)
check("one_native_attempt", len(s["operations"][0]["attempts"]), 1)
check("terminal_native_event", s["operations"][0]["last_event"]["terminal"], True)
check("runtime_status", load(b / "runtime_audit_result.json")["status"], "pass")
check("compose_status", load(b / "compose_audit_attempt02_result.json")["status"], "pass")
check("hard_gates_not_observable", report["pixels"]["not_observable_gate_count"], 12)
check("no_pixel_passes", report["pixels"]["passed_gate_count"], 0)
check("no_image_fabrication", report["pixels"]["image_path"], None)
ast.parse((b / "native_result_with_provenance.py").read_text())
check("wrapper_parse", True, True)
# The managed workflow deliberately names raw requester text request_raw.json.
# Their exact bytes were checked above; they are not JSON document artifacts.
raw_paths = {Path(state["artifacts"]["request_raw"]["path"]).resolve() for state in [s, old]}
for p in b.rglob("*.json"):
    if p.resolve() not in raw_paths:
        load(p)
check("structured_arm_json_parse", True, True)
check("request_raw_exact_text", all(p.read_text() == (b / "source_request.txt").read_text() for p in raw_paths), True)
failures = [x for x in checks if not x["pass"]]
proof = {"schema_version": "independent-arm-final-verification/v1", "arm_id": "b",
         "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "status": "pass" if not failures else "fail", "check_count": len(checks),
         "checks": checks, "failures": failures,
         "scope": "Content integrity, artifact bindings and terminal invocation evidence only; no native pixel or aesthetic pass implied.",
         "model_observation": "The transport asks for gpt-image-2; the native error identifies no model."}
(b / "FINAL_VERIFICATION.json").write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": proof["status"], "checks": len(checks),
                  "failures": [x["check"] for x in failures], "counts": report["counts"]}, ensure_ascii=False))
assert not failures
