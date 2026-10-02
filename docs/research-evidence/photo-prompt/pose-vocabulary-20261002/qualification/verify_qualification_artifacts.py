"""Verify saved evidence bindings; this script does not judge image pixels."""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
SOURCE_SHA = "c4727e17671270b54c2766b3b62295086c58b1162796e2d678b8fb061e1eadff"
ARMS = {
    "arm-a-seated": ("phase1_freeze_manifest.json", "baseline_prompt_en.txt", "native_tool_args.json", "runtime_prompt_en.txt", "runtime_request.json", "native_call_record.json", "original_observed_path", "final_artifact_manifest.json", "artifact_sha256"),
    "arm-b-ballet": ("phase1_freeze_manifest.json", "baseline_prompt.txt", "native_tool_args.json", "runtime_prompt.txt", "render_request.json", "native_output.json", "source_path", "artifact_manifest.json", "files"),
    "arm-c-kneeling": ("phase1_freeze.json", "baseline_prompt_en.txt", "native_image_args.json", "runtime_prompt_en.txt", "runtime_request.json", "native_result.json", "native_source_path", "artifacts_manifest.json", "files"),
}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checks = []

    def check(name, value):
        checks.append({"check": name, "pass": bool(value)})

    source_path = HERE.parent / "implementation/implementation-source-manifest.json"
    source = read(source_path)
    check("source manifest frozen bytes", sha(source_path) == SOURCE_SHA)
    for name, expected in source["file_sha256"].items():
        check("runtime source " + name, sha(ROOT / name) == expected)
    inputs = read(HERE / "coordinator-inputs.json")
    reference = Path(inputs["reference_path"])
    check("reference original SHA", sha(reference) == inputs["reference_sha256"])
    summary = []
    for arm, configuration in ARMS.items():
        freeze_name, baseline_name, args_name, runtime_name, request_name, result_name, origin_key, inventory_name, inventory_key = configuration
        directory = HERE / arm
        frozen = read(directory / freeze_name)
        for name, expected in (frozen.get("file_sha256") or frozen["files"]).items():
            check(arm + " phase1 " + name, sha(directory / name) == expected)
        check(arm + " baseline bytes frozen", sha(directory / baseline_name) == frozen["baseline_prompt_sha256"])
        check(arm + " request exact envelope", sha(directory / "request_envelope.json") == inputs["arms"][arm]["envelope_file_sha256"])
        pack = read(directory / "candidate_pack.json")
        pack = pack[0] if isinstance(pack, list) else pack
        core = read(directory / "authorial_core.json")
        composed = read(directory / "composed_prompt.json")
        request = read(directory / request_name)
        arguments = read(directory / args_name)
        manifest = read(directory / "run_manifest.json")
        result = read(directory / result_name)
        image_path = Path(manifest["image_paths"][0])
        native_path = Path(result[origin_key])
        check(arm + " preserved independently authored baseline", core["baseline_prompt_en"] == pack["authorial_core"]["baseline_prompt_en"])
        check(arm + " pack IDs bound", pack["pack_id"] == composed["pack_id"] == request["pack_id"] == manifest["pack_id"])
        check(arm + " core retrieval runtime bound", request["core_retrieval_sha256"] == pack["core_retrieval"]["canonical_sha256"])
        check(arm + " native prompt equals audited runtime", arguments["prompt"] == request["runtime_prompt_en"] == (directory / runtime_name).read_text())
        check(arm + " positive prompt retained", composed["prompt_en"] in arguments["prompt"])
        check(arm + " negative retained", composed["negative_en"] == request["runtime_negative_en"])
        check(arm + " exact local reference argument", arguments["referenced_image_paths"] == [str(reference)])
        check(arm + " opaque photo output", arguments["transparent_background"] is False)
        check(arm + " one native image call", manifest["image_call_count"] == 1)
        check(arm + " independent inputs", manifest["cross_arm_inputs_used"] is False)
        check(arm + " no profile opt-in", manifest["chosen_visual_concept_ids"] == [])
        ledger_path = directory / ("runs/image_runs.ndjson" if arm == "arm-c-kneeling" else "image_runs.ndjson")
        ledger_rows = [json.loads(line) for line in ledger_path.read_text().splitlines() if line.strip()]
        check(arm + " one canonical generation record", len(ledger_rows) == 1)
        ledger = ledger_rows[0]
        check(arm + " canonical generation run bound", ledger["run_id"] == manifest["ledger_run_id"])
        check(arm + " ledger pack seed recorded", ledger["seed"] == pack["provenance"]["seed"])
        check(arm + " metadata correction is no extra call", ledger["image_call_count"] == 1)
        check(arm + " generation success recorded separately", ledger["status"] == "success")
        image_sha = sha(image_path)
        check(arm + " native original bytes preserved", image_sha == sha(native_path) == manifest["image_hashes"][0]["sha256"])
        raw = image_path.read_bytes()
        check(arm + " original PNG", raw[:8] == b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", raw[16:24])
        for name, expected in read(directory / inventory_name)[inventory_key].items():
            check(arm + " artifact " + name, sha(directory / name) == expected)
        summary.append({"arm": arm, "pack_id": pack["pack_id"], "pack_seed": pack["provenance"]["seed"], "image_path": str(image_path), "native_source_path": str(native_path), "image_sha256": image_sha, "width": width, "height": height, "native_calls": 1})
    failures = [check for check in checks if not check["pass"]]
    report = {"schema_version": "pose-evidence-integrity/v1", "status": "PASS" if not failures else "FAIL", "check_count": len(checks), "failures": failures, "checks": checks, "arms": summary, "scope": "Saved source, frozen inputs, exact native arguments, runtime bindings and image bytes only. Pixel judgments are human/agent observation records, not inferred by this script."}
    (HERE / "artifact-verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "check_count", "failures")}, ensure_ascii=False))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
