#!/usr/bin/env python3
"""Read-only hash and binding verification for the frozen five-case replay."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = ROOT / "generated_images/photo-data-five-case-20260906"
FROZEN = [
    ("11724b87515ee8b6169f1d49d5d99cb4f76d6af4360261827a31d90c3d676d99", "2db6cdbc448698dd5ebc35bc28f5a8f79023a234d82f933f2d5af563e85462e2", "7cf3ea9076733a9d0b6a1c8da697a3202e7be590526c71403a2b1bf4799d1ebb"),
    ("77a4f3b95b243804505bda6e96cabc6e86145b1704e02f686932464ff72d7517", "6dce057b201780a568c0c136d2e146e78928dcc844111ced9b5e868cb2d1dc98", "a1f39a432f351644aa6cad6725be294e1c8dd0342b165e540066d9350bae14c0"),
    ("09d05850d37c6099881e53ebff3521c75ada1b53d89b2a6e793d36717e6bb8f0", "f07221b12b3207c13eb6a624bb79c33497cff70b6541ce089c49777182ae9a70", "27ace6b2c0b47be5fabfa2a78dd22200a1551cac55fd5d98cdef3e53ced334a3"),
    ("cba48ebc9080e146917350449bd1f89b85276b50a497c261b8e3999f580535a9", "68e5603303092b908178a888f5c77fecea937f0ecd1403af3822bc7725be8985", "6005abbae9cfba05fe255fbf6520f2f4393ad2cfd5a2998ca29b496108041156"),
    ("18b4f964b726fa75b7275f8a47daed6e2153c184bb9a4fbb29935e1afefadbbc", "01b8ac30cd515cff14170a067c3d41c9007144428d536d51c7062db409f2dac9", "3b30bcc5dda092ca27170134f999403fbc38ed5bd87ba0ee1c2b82d2fc6db635"),
]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def source_files(folder):
    return {str(p.relative_to(folder)): sha(p) for p in sorted(folder.rglob("*"))
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"}


def first(folder, names):
    return next(folder / name for name in names if (folder / name).exists())


def main():
    design = read(RUN / "evaluation-manifest.json")
    source = read(RUN / "candidate-source/source-manifest.json")
    files = source_files(RUN / "candidate-source/skills/photo-prompt-image-generator")
    source_sha = text_sha(json.dumps(files, sort_keys=True, separators=(",", ":")))
    working_files = source_files(ROOT / "skills/photo-prompt-image-generator")
    final_manifest_path = RUN / "final-source-manifest.json"
    final_manifest = read(final_manifest_path) if final_manifest_path.exists() else source
    working_sha = text_sha(json.dumps(working_files, sort_keys=True, separators=(",", ":")))
    delta = sorted(k for k in set(files) | set(working_files) if files.get(k) != working_files.get(k))
    final_source_matches = working_files == final_manifest["files"] and working_sha == final_manifest["skill_sha256"]
    allowed_delta = [] if not final_manifest_path.exists() else final_manifest["post_generation_changed_paths"]
    diagnostic_patch_only = delta == allowed_delta and set(delta) <= {"scripts/validate_photo_prompt_dictionary.py"}
    rows = []
    for i, case in enumerate(design["cases"]):
        env = Path(case["environment"])
        out = env / "outputs"
        manifest = read(env / "run_manifest.json")
        pack_list = read(out / "candidate_pack.json")
        pack = pack_list[0] if isinstance(pack_list, list) else pack_list
        core = pack["authorial_core"]
        composed = read(out / "composed_prompt.json")
        runtime = read(out / "runtime_request.json")
        args_path = first(out, ["native_tool_arguments.json", "native_tool_args.json", "runtime_tool_args.json"])
        tool_args = read(args_path)
        composed_audit_path = first(out, ["composed_audit.json", "composed-audit.json"])
        runtime_audit_path = first(out, ["runtime_audit.json", "runtime-audit.json"])
        composed_audit = read(composed_audit_path)
        runtime_audit = read(runtime_audit_path)
        ledger = [json.loads(line) for line in (env / "runs/image_runs.ndjson").read_text().splitlines() if line.strip()]
        record = next(row for row in ledger if row["run_id"] == manifest["ledger_run_id"])
        envelope = read(env / "inputs/request_envelope.json")
        reference_paths = [x["path"] for x in case["references"]]
        reference_hashes = [x["sha256"] for x in case["references"]]
        checks = {
            "source_exact_files": source_files(env / "skills/photo-prompt-image-generator") == source["files"],
            "source_manifest_identical": read(env / "source-manifest.json") == source,
            "source_binding": manifest["skill_sha256"] == record["skill_sha256"] == source_sha == source["skill_sha256"],
            "request_envelope_raw_hash": sha(env / "inputs/request_envelope.json") == case["envelope_file_sha256"],
            "request_text_hash": text_sha(envelope["request_text"]) == case["request_sha256"],
            "raw_core_unchanged": sha(env / "authorial_core.json") == FROZEN[i][0],
            "baseline_unchanged": sha(env / "baseline_prompt.txt") == FROZEN[i][1],
            "precore_freeze_unchanged": sha(env / "precore-freeze.json") == FROZEN[i][2],
            "one_pack_artifact": not isinstance(pack_list, list) or len(pack_list) == 1,
            "pack_binding": pack["pack_id"] == composed["pack_id"] == runtime["pack_id"] == manifest["pack_id"] == record["pack_id"],
            "canonical_core_binding": core["canonical_sha256"] == manifest["authorial_core_sha256"] == record["authorial_core_sha256"],
            "intent_binding": core["intent_lock"]["canonical_sha256"] == manifest["intent_lock_sha256"] == record["intent_lock_sha256"] == runtime["source_intent_lock_sha256"],
            "baseline_embedded_after_core_whitespace_normalization": core["baseline_prompt_en"] == " ".join((env / "baseline_prompt.txt").read_text().split()),
            "seed_and_mode": pack["provenance"]["seed"] == 6101 + i and pack["provenance"]["selection_mode"] == "semantic" and pack["provenance"]["creativity"] == 0.5,
            "composed_audit_pass": composed_audit["status"] == "pass" and not composed_audit["failures"],
            "runtime_audit_pass": runtime_audit["status"] == "pass" and not runtime_audit["failures"],
            "runtime_literal_prompt": runtime["runtime_prompt_en"] == tool_args["prompt"] == record["prompt_en"] == (out / "runtime_prompt.txt").read_text(),
            "runtime_literal_negative": runtime["runtime_negative_en"] == composed["negative_en"] == pack["negative_en"] == record["negative_en"],
            "runtime_prompt_hash_binding": text_sha(runtime["runtime_prompt_en"])[:16] == manifest["prompt_id"] == record["prompt_id"],
            "reference_input_hashes": [sha(Path(p)) for p in reference_paths] == reference_hashes,
            "reference_argument_binding": tool_args.get("referenced_image_paths", []) == reference_paths,
            "reference_runtime_binding": runtime["references"] == case["references"],
            "reference_ledger_binding": manifest["reference_sha256"] == record.get("reference_sha256", []) == reference_hashes,
            "image_call_count_recorded": manifest["image_call_count"] == record["image_call_count"] == 1,
            "single_ledger_record": len(ledger) == 1,
            "cross_arm_inputs_declared_false": manifest["cross_arm_inputs_used"] is False and record["cross_arm_inputs_used"] is False,
            "image_manifest_hashes": all(sha(Path(x["path"])) == x["sha256"] for x in manifest["image_hashes"]),
            "image_path_binding": manifest["image_paths"] == record["image_paths"],
            "delivery_status_binding": manifest["status"] == record["status"],
        }
        rows.append({"arm": case["arm"], "status": "pass" if all(checks.values()) else "fail",
                     "checks": checks, "failures": [k for k, v in checks.items() if not v],
                     "pack_id": pack["pack_id"], "image_paths": manifest["image_paths"],
                     "delivery": manifest["status"], "ledger_run_id": manifest["ledger_run_id"],
                     "native_tool_args_path": str(args_path), "native_tool_args_file_sha256": sha(args_path),
                     "composed_audit_path": str(composed_audit_path), "runtime_audit_path": str(runtime_audit_path)})
    result = {
        "schema_version": "photo-five-case-artifact-verification/v1", "source_sha256": source_sha,
        "source_file_count": len(files), "generation_snapshot_matches_manifest": files == source["files"],
        "root_source_matches_generation_snapshot": working_files == files,
        "final_working_tree_sha256": working_sha, "final_working_tree_matches_manifest": final_source_matches,
        "post_generation_changed_paths": delta, "post_generation_change_is_declared_cli_validator_only": diagnostic_patch_only,
        "status": "pass" if files == source["files"] and final_source_matches and diagnostic_patch_only and all(r["status"] == "pass" for r in rows) else "fail",
        "evidence_boundary": "Exact artifact readback; image call counts and cross-arm access are corroborated by child-agent execution records, not independent OS/network telemetry. Pixel truth is separately reviewed.",
        "arms": rows,
    }
    target = RUN / "evaluation/artifact-verification.json"
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "source_file_count": len(files), "arms": [{"arm": r["arm"], "failures": r["failures"]} for r in rows]}, indent=2))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
