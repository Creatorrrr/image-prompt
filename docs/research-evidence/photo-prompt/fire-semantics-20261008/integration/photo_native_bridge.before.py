"""Thin bridge source for the Codex tool environment and native observations."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path

from photo_workflow_state import WorkflowError, atomic_write, bound_path, digest, encode, load_state, value

# The bridge calls the native tool exactly once. The supplied observer may use
# only fields actually returned by that tool; absent a concrete file, it returns
# preview_only. No cache probing, download, or paid fallback is performed.
BRIDGE_JAVASCRIPT = r'''
async function runPhotoNative({tools, run, workflowScript, python, ledger, observe}) {
  const quote = s => "'" + String(s).replaceAll("'", "'\\''") + "'";
  async function command(argv) {
    const answer = await tools.exec_command({cmd: argv.map(quote).join(" "), max_output_tokens: 2000});
    if (answer.exit_code !== 0) throw new Error("native_bridge_command_failed");
    return JSON.parse(answer.output);
  }
  const started = await command([python, workflowScript, "native-started", "--run", run]);
  let result;
  try {
    result = await tools.image_gen__imagegen(started.payload);
  } catch (error) {
    const capture = {type: error?.name || typeof error, message: String(error)};
    await command([python, workflowScript.replace(/photo_workflow\.py$/, "photo_native_bridge.py"),
      "observe", "--run", run, "--ledger", ledger, "--error-json", JSON.stringify(capture)]);
    return {outcome: "tool_error", operation_id: started.operation_id};
  }
  if (result?.isError === true) {
    await command([python, workflowScript.replace(/photo_workflow\.py$/, "photo_native_bridge.py"),
      "observe", "--run", run, "--ledger", ledger, "--error-json", JSON.stringify(result)]);
  } else {
    const observed = await observe(result);
    await command([python, workflowScript.replace(/photo_workflow\.py$/, "photo_native_bridge.py"),
      "observe", "--run", run, "--ledger", ledger, "--observation-json", JSON.stringify({operation_id: started.operation_id, ...observed})]);
  }
  return result;
}
'''


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("source")
    p = sub.add_parser("observe"); p.add_argument("--run", type=Path, required=True); p.add_argument("--ledger", type=Path, required=True)
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--error-json"); group.add_argument("--observation-json")
    args = parser.parse_args(argv)
    if args.command == "source":
        print(BRIDGE_JAVASCRIPT); return 0
    try:
        state = load_state(args.run); plan = value(state, "native_plan")
        if args.error_json:
            from image_attempt_evidence import capture_native_error, write_evidence
            raw = json.loads(args.error_json)
            composed = value(state, "composed")
            operation = next(op for op in state["operations"] if op["operation_id"] == plan["operation_id"])
            evidence = capture_native_error(raw, {"tool": "image_gen", "generation_environment": "native_imagegen",
                "attempt": 1, "started_at": operation["timestamp"], "ended_at": datetime.now(timezone.utc).isoformat(),
                "invocation_outcome": "rejected", "provider_outcome": "unknown",
                "request": {"prompt_en": composed["prompt_en"], "negative_en": composed.get("negative_en"), "runtime_prompt_en": plan["payload"]["prompt"]}})
            path = args.run.resolve() / "operations" / (plan["operation_id"] + ".error.json")
            if path.exists():
                # Preserve the first observation; a different capture conflicts.
                if read_existing := value_from_path(path):
                    if read_existing != evidence:
                        raise WorkflowError("native_error_capture_conflict")
                sha = digest(path.read_bytes())
            else: sha = write_evidence(path, evidence)
            observation = {"operation_id": plan["operation_id"], "outcome": "rejected", "evidence_path": str(path), "evidence_sha256": sha}
        else: observation = json.loads(args.observation_json)
        path = args.run.resolve() / "operations" / (plan["operation_id"] + ".observation.json")
        if path.exists() and value_from_path(path) != observation:
            raise WorkflowError("native_observation_conflict")
        atomic_write(path, encode(observation))
        from photo_workflow import native_result
        args.result = path
        print(json.dumps(native_result(args)))
        return 0
    except (ValueError, OSError, KeyError, TypeError, StopIteration) as error:
        print(json.dumps({"status": "error", "code": getattr(error, "code", "native_observation_invalid")}))
        return 2


def value_from_path(path):
    return json.loads(Path(path).read_bytes())


def validate_native_record(path, expected_sha, entry):
    """Reaudit the original tuple and bind the exact observed native payload."""
    raw = Path(path).read_bytes()
    if digest(raw) != expected_sha:
        raise WorkflowError("stale_native_plan")
    plan = json.loads(raw)
    if plan.get("schema_version") != "photo-native-plan/v1" or entry.get("workflow_operation_id") != plan["operation_id"] + ":1" or entry["ts"] != plan["timestamp"]:
        raise WorkflowError("native_record_operation_mismatch")
    from photo_workflow_worker import audit_bound
    from photo_workflow import one
    state = {"artifacts": plan["inputs"], "source_binding": {"runtime_store": plan["runtime_store"]}}
    for role in state["artifacts"]: bound_path(state, role)
    result = audit_bound(state, runtime=True)
    if any(result[k]["status"] != "pass" or result[k]["failures"] for k in ("composed_audit", "runtime_audit")):
        raise WorkflowError("native_record_audit_failed")
    pack, composed, request = (one(value(state, role)) for role in ("pack", "composed", "render_request"))
    expected_payload = {"prompt": request["runtime_prompt_en"], "transparent_background": request.get("transparent_background", False)}
    if request.get("referenced_image_paths"): expected_payload["referenced_image_paths"] = request["referenced_image_paths"]
    if request.get("num_last_images_to_include") or plan["payload"] != expected_payload:
        raise WorkflowError("native_record_payload_mismatch")
    expected = {"pack_id": pack["pack_id"], "prompt_en": composed["prompt_en"], "negative_en": composed.get("negative_en"),
        "authorial_core_sha256": pack["authorial_core"]["canonical_sha256"], "intent_lock_sha256": pack["authorial_core"]["intent_lock"]["canonical_sha256"],
        "chosen_candidate_ids": composed["chosen_candidate_ids"], "chosen_visual_concept_ids": composed["chosen_visual_concept_ids"]}
    if any(entry.get(k) != v for k, v in expected.items()):
        raise WorkflowError("native_record_input_mismatch")
    return {"native_render_plan_json": str(Path(path).resolve()), "native_render_plan_sha256": expected_sha,
            "runtime_prompt_sha256": digest(plan["payload"]["prompt"].encode("utf-8"))}


if __name__ == "__main__":
    raise SystemExit(main())
