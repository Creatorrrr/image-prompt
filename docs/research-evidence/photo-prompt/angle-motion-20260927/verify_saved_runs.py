#!/usr/bin/env python3
"""Read back frozen inputs, audited requests and native image bytes; never render."""
import hashlib
import json
import re
import struct
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    source = load(BASE / "source-freeze.json")
    freeze = load(BASE / "coordinator-pre-render-freeze.json")
    assert all(sha(ROOT / name) == digest for name, digest in source["files_sha256"].items())
    assert sha(source["reference_path"]) == source["reference_sha256"]
    configuration = [
        ("high_angle", "composition_audit.json", "runtime_audit.json", "image_render_request.json", "native_tool_args.json", "native_result.json"),
        ("low_angle", "composed_audit.json", "runtime_request_audit.json", "image_render_request.json", "native_tool_arguments.json", "native_output.json"),
        ("dynamic_composition", "composed_audit.json", "runtime_request_audit.json", "render_request.json", "native_tool_args.json", "native_response.json"),
    ]
    arms, embodiment = [], Counter()
    for arm, composed_audit_name, runtime_audit_name, request_name, args_name, native_name in configuration:
        directory = BASE / arm
        frozen = freeze["arms"][arm]
        assert all(sha(directory / name) == digest for name, digest in frozen["files_sha256"].items())
        core = load(directory / "authorial_core.json")
        envelope = load(directory / "request_envelope.json")
        assert core["source_request"] == envelope["request_text"]
        assert hashlib.sha256(core["baseline_prompt_en"].encode()).hexdigest() == frozen["baseline_prompt_sha256"]
        packs = load(directory / "candidate_pack.json")
        assert isinstance(packs, list) and len(packs) == 1
        pack = packs[0]
        composed = load(directory / "composed_prompt.json")
        manifest = load(directory / "run_manifest.json")
        ledger = [json.loads(line) for line in (directory / "image_runs.ndjson").read_text().splitlines() if line.strip()]
        assert len(ledger) == 1 and ledger[0]["run_id"] == manifest["ledger_run_id"]
        assert pack["contract_version"] == "photo-candidate-pack/v6"
        assert pack["provenance"]["selection_mode"] == "semantic"
        assert pack["pack_id"] == composed["pack_id"] == manifest["pack_id"] == ledger[0]["pack_id"]
        assert manifest["image_call_count"] == ledger[0]["image_call_count"] == 1
        assert manifest["reference_sha256"] == ledger[0]["reference_sha256"] == [source["reference_sha256"]]
        assert manifest["cross_arm_inputs_used"] == ledger[0]["cross_arm_inputs_used"] == False
        catalog = load(directory / "composer_view.json")["candidate_catalog"]
        catalog_ids = {candidate["id"] for candidate in catalog}
        assert set(composed["chosen_candidate_ids"]).issubset(catalog_ids)
        assert composed["chosen_visual_concept_ids"] == manifest["chosen_visual_concept_ids"] == []
        binding = composed["authorial_core_binding"]
        assert binding["source_authorial_core_sha256"] == manifest["authorial_core_sha256"]
        assert binding["source_intent_lock_sha256"] == manifest["intent_lock_sha256"]
        for assertion in core["semantic_assertions"]:
            for phrase in assertion["evidence"].values():
                assert phrase in composed["prompt_en"]
        composed_audit = load(directory / composed_audit_name)
        runtime_audit = load(directory / runtime_audit_name)
        assert composed_audit["status"] == runtime_audit["status"] == "pass"
        assert composed_audit["failures"] == runtime_audit["failures"] == []
        request = load(directory / request_name)
        native_args = load(directory / args_name)
        assert native_args["prompt"] == request["runtime_prompt_en"]
        assert native_args["referenced_image_paths"] == [source["reference_path"]]
        assert composed["prompt_en"] in request["runtime_prompt_en"]
        assert request["runtime_negative_en"] == composed["negative_en"]
        assert request["source_intent_lock_sha256"] == manifest["intent_lock_sha256"]
        native = load(directory / native_name)
        native_path = native.get("concrete_returned_original_path", native.get("native_returned_path"))
        if native_path is None:
            match = re.search(r" as (/Users/[^\n]+\.png) by default", native["output_hint"])
            assert match
            native_path = match.group(1)
        original = directory / "generated.png"
        image_sha = sha(original)
        assert image_sha == sha(native_path)
        assert manifest["image_hashes"] == [{"path": str(original), "sha256": image_sha}]
        with original.open("rb") as stream:
            header = stream.read(24)
        assert header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR"
        dimensions = list(struct.unpack(">II", header[16:24]))
        review = load(directory / "pixel_review.json")
        assert review["result_sha256"] == image_sha and review["result_image"] == str(original)
        gates = Counter(item["status"] for item in review["hard_gates"].values())
        assert set(gates).issubset({"pass", "fail"})
        embodiment.update(gates)
        audit = load(directory / "pixel_review_audit.json")
        assert audit["schema_failures"] == []
        coordinator = load(directory / "coordinator_pixel_review.json")
        assert coordinator["image_sha256"] == image_sha
        assert set(core["semantic_assertions"][0]["evidence"]) == {item["field"] for item in coordinator["focal_assertion_fields"]}
        topic_components = Counter(item["status"] for item in coordinator["topic_components"])
        focal_fields = Counter(item["status"] for item in coordinator["focal_assertion_fields"])
        assert (coordinator["topic_status"] == "pass") == (topic_components["fail"] == focal_fields["fail"] == 0)
        summary = load(directory / "arm_summary.json")
        arms.append({
            "arm": arm, "seed": pack["provenance"]["seed"], "pack_id": pack["pack_id"],
            "run_id": manifest["ledger_run_id"], "prompt_id": manifest["prompt_id"],
            "dictionary_hash": pack["provenance"]["tags_hash"], "native_image_calls": 1,
            "image_path": str(original), "image_sha256": image_sha, "dimensions": dimensions,
            "coordinator_topic_status": coordinator["topic_status"], "full_scene_status": coordinator["full_scene_status"],
            "general_topic_components": dict(topic_components), "exact_focal_fields": dict(focal_fields),
            "embodiment_gates": dict(gates), "pixel_technical_qualified": audit["technical_qualified"],
            "selected_candidate_ids": composed["chosen_candidate_ids"], "selected_visual_concept_ids": [],
            "new_pc_candidates_exposed": sorted(candidate for candidate in catalog_ids if ":pc_" in candidate),
            "new_pc_candidates_selected": [candidate for candidate in composed["chosen_candidate_ids"] if ":pc_" in candidate],
            "canonical_core_sha256": manifest["authorial_core_sha256"], "intent_lock_sha256": manifest["intent_lock_sha256"],
            "core_file_sha256": frozen["files_sha256"]["authorial_core.json"],
            "test_case_sha256": frozen["files_sha256"]["test_case.json"],
            "prompt_audit_status": composed_audit["status"], "runtime_audit_status": runtime_audit["status"],
            "summary_sha256": sha(directory / "arm_summary.json"), "report_path": str(directory / "report.md"),
        })
    result = {
        "schema_version": "angle-motion-final-verification/v1", "verified_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "pass_for_saved_run_integrity", "source_files_unchanged": len(source["files_sha256"]),
        "frozen_arm_files_unchanged": sum(len(arm["files_sha256"]) for arm in freeze["arms"].values()),
        "source_data_changes": 0, "reference_sha256": source["reference_sha256"], "native_image_calls": 3,
        "strict_topic_pass": sum(arm["coordinator_topic_status"] == "pass" for arm in arms), "topic_total": 3,
        "full_scene_pass": sum(arm["full_scene_status"] == "pass" for arm in arms), "scene_total": 3,
        "embodiment_gates": dict(embodiment), "user_judgment": "not_yet_received",
        "claim_boundary": "Run integrity pass does not override recorded pixel failures. No new portrait-composition profile was selected; no additional profile or bundle pixel qualification is claimed.",
        "arms": arms,
    }
    assert result["strict_topic_pass"] == 2 and result["full_scene_pass"] == 1
    assert embodiment == {"pass": 12, "fail": 3}
    (BASE / "verification.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ["status", "source_files_unchanged", "frozen_arm_files_unchanged", "native_image_calls", "strict_topic_pass", "full_scene_pass", "embodiment_gates"]}))


if __name__ == "__main__":
    main()
