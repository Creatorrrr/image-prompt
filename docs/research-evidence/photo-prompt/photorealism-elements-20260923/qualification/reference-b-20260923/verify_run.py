#!/usr/bin/env python3
"""Verify the immutable inputs, audits, and saved outputs of the three-arm replay."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[5]


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


reference = read(BASE / "reference_manifest.json")
snapshot = read(BASE / "source_snapshot.json")
assert sha(Path(reference["reference_path"])) == reference["reference_sha256"]
assert hashlib.sha256(reference["request_text"].encode()).hexdigest() == reference["request_sha256"]
for name, expected in snapshot["files_sha256"].items():
    assert sha(REPO / name) == expected, name

arms = {}
settings = set()
for arm in "abc":
    directory = BASE / f"arm_{arm}"
    envelope = read(directory / "request_envelope.json")
    core = read(directory / "authorial_core.json")
    pack_data = json.loads((directory / "candidate_pack.json").read_text(encoding="utf-8"))
    pack = pack_data[0] if isinstance(pack_data, list) else pack_data
    composed = read(directory / "composed_prompt.json")
    manifest = read(directory / "run_manifest.json")
    render_request = read(directory / {
        "a": "render_request.json",
        "b": "image_render_request.json",
        "c": "exact_render_request.json",
    }[arm])
    composed_audit = read(directory / "composed_audit.json")
    runtime_audit = read(directory / {
        "a": "render_request_audit.json",
        "b": "image_render_request_audit.json",
        "c": "render_request_audit.json",
    }[arm])
    review = read(directory / {
        "a": "native_pixel_review.json",
        "b": "native_pixel_review.json",
        "c": "native_pixel_review.json",
    }[arm])

    assert envelope["request_text"] == reference["request_text"]
    assert envelope["request_sha256"] == reference["request_sha256"]
    assert core["source_request"] == reference["request_text"]
    settings.add(core["setting"])
    assert pack["pack_id"] == manifest["pack_id"]
    assert composed_audit["status"] == runtime_audit["status"] == "pass"
    assert manifest["image_call_count"] == 1
    assert manifest["cross_arm_inputs_used"] is False
    assert manifest["reference_sha256"] == [reference["reference_sha256"]]
    assert len(render_request["references"]) == 1
    assert render_request["references"][0]["sha256"] == reference["reference_sha256"]
    assert Path(render_request["references"][0]["path"]).resolve() == Path(reference["reference_path"]).resolve()
    assert len(manifest["image_hashes"]) == 1
    image = manifest["image_hashes"][0]
    assert sha(Path(image["path"])) == image["sha256"]
    assert review.get("image_sha256", review.get("result_sha256")) == image["sha256"]
    assert manifest["source_ref"] in (
        snapshot["git_head"],
        "source-snapshot-sha256:" + sha(BASE / "source_snapshot.json"),
    )

    if arm == "a":
        targets = [row for row in read(directory / "target_contract.json")["targets"] if row["profile_id"].startswith("pr_")]
        statuses = {row["gate_id"].removeprefix("target_"): row["status"] for row in review["gates"] if row["lane"] == "primary_pr"}
    elif arm == "b":
        targets = read(directory / "selected_target_contract.json")["targets"]
        statuses = {row["profile_id"]: row["complete_relation_status"] for row in review["targets"]}
    else:
        targets = read(directory / "selected_target_contract.json")["targets"]
        statuses = {row["profile_id"]: row["status"] for row in review["profile_results"]}

    candidate_ids = {row["id"] for row in pack["visual_concept_candidates"]["candidates"]}
    selected = set(composed["chosen_visual_concept_ids"])
    profile_ids = [row["profile_id"] for row in targets]
    assert len(profile_ids) == len(set(profile_ids)) == 3
    assert all(name.startswith("pr_") for name in profile_ids)
    assert set(profile_ids) == set(statuses)
    exposed = [name for name in profile_ids if f"visual-concept:{name}" in candidate_ids]
    opted_in = [name for name in profile_ids if f"visual-concept:{name}" in selected]
    assert set(opted_in).issubset(exposed)
    passed = sum(status == "pass" for status in statuses.values())
    assert passed == 2 and all(status in ("pass", "fail") for status in statuses.values())
    arms[arm] = {
        "setting": core["setting"],
        "event": core["event"],
        "pack_id": pack["pack_id"],
        "candidate_exposed": exposed,
        "candidate_opted_in": opted_in,
        "target_statuses": statuses,
        "target_passed": passed,
        "target_total": len(targets),
        "whole_scene_status": "fail",
        "image_path": image["path"],
        "image_sha256": image["sha256"],
        "composed_audit_status": composed_audit["status"],
        "runtime_audit_status": runtime_audit["status"],
        "image_call_count": manifest["image_call_count"],
    }

assert len(settings) == 3
verification = {
    "schema_version": "photorealism-three-arm-reference-b-verification/v1",
    "reference_sha256": reference["reference_sha256"],
    "source_snapshot_sha256": sha(BASE / "source_snapshot.json"),
    "arms": arms,
    "totals": {
        "saved_images": 3,
        "image_calls": 3,
        "composed_audit_passed": 3,
        "runtime_audit_passed": 3,
        "target_profiles_passed": 6,
        "target_profiles_total": 9,
        "candidate_exposed": sum(len(row["candidate_exposed"]) for row in arms.values()),
        "candidate_opted_in": sum(len(row["candidate_opted_in"]) for row in arms.values()),
        "whole_scenes_passed": 0,
        "whole_scenes_total": 3,
    },
}
(BASE / "verification.json").write_text(json.dumps(verification, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(verification["totals"], ensure_ascii=False))
