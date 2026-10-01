#!/usr/bin/env python3
"""Verify saved run bindings; aggregate existing native reviews, never grade pixels."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
Q = ROOT / "qualification"
DICT = "70379562ac6e618750d724a51659049174aec2e4cb95f3226e3bf6a1036f4ed4"
REGISTRY = "103e10149bcda2a0ba846b215c309d07ed3f0102d49d5b0a25741f5483e6d45c"
CONFIG = {
    "arm-a-film-optics": {
        "prompt": "prompt.en.txt", "negative": "negative.en.txt",
        "composed_audit": "audit.composed.json", "runtime_audit": "audit.runtime.json",
        "pixel_audit": "audit.pixel-record.json", "runtime": "render_request.json",
        "native_args": "native_tool_args.json", "review": "qualification_report.json",
        "pre_render": "test_cases.pre-render.json", "v1_effect_pass": 1,
        "targets": ["slot:grain_profile:pe_fine_midtonal_grain", "slot:film_emulation:pe_red_edge_halation", "slot:color_grading:pe_gentle_rolloff"],
        "original": "/Users/chasoik/.codex/generated_images/01a0f65d-ec17-77f0-be56-cc3c62d6c5c4/exec-197a7475-bc59-452d-8c00-3423257d9764.png",
    },
    "arm-b-digital-motion": {
        "prompt": "prompt.txt", "negative": "negative.txt",
        "composed_audit": "composed_audit.json", "runtime_audit": "runtime_audit.json",
        "pixel_audit": "visual_pixel_audit.json", "runtime": "runtime_request.json",
        "native_args": "actual_native_tool_request.json", "review": "editing_pixel_review.json",
        "pre_render": "pre_render_test_case.json", "v1_effect_pass": 2,
        "targets": ["slot:camera_type:pe_compact_flash_noisy_finish", "slot:grain_profile:pe_digital_chroma_noise", "slot:grain_profile:pe_digital_luma_noise", "slot:motion:pe_flash_core_shutter_trace"],
        "original": "/Users/chasoik/.codex/generated_images/01a0f65e-6e38-7d02-89cf-ca28b4500d17/exec-c7dd4682-efd1-4782-bca4-816eb71c3437.png",
    },
    "arm-c-tonal-skin": {
        "prompt": "prompt_en.txt", "negative": "negative_en.txt",
        "composed_audit": "composition_audit.json", "runtime_audit": "runtime_audit.json",
        "pixel_audit": "render_review_audit.json", "runtime": "render_request.json",
        "native_args": "native_tool_args.json", "review": "qualification_result.json",
        "pre_render": "pre_render_test_cases.json", "v1_effect_pass": 1,
        "targets": ["slot:color_grading:pe_red_object_splash", "slot:color_grading:pe_lifted_black_floor", "slot:skin_finish:pe_texture_preserving_tone_evening"],
        "original": "/Users/chasoik/.codex/generated_images/01a0f65e-f2f4-7ef2-be09-66ea7ecab5fe/exec-6b00365b-065b-4c8c-82f6-85913f758f55.png",
    },
}


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


checks = []


def check(name, condition, evidence=None):
    checks.append({"check": name, "status": "PASS" if condition else "FAIL", "evidence": evidence})


snapshot = Q / "source-snapshot-v2"
source = read(snapshot / "source-manifest.json")
check("source_revision", source["dictionary_sha256"] == DICT and source["registry_sha256"] == REGISTRY)
for rel, expected in source["files"].items():
    check("source_live_and_snapshot:" + rel,
          sha(REPO / rel) == expected == sha(snapshot / rel), expected)
check("source_file_count", len(source["files"]) == 95, len(source["files"]))
ref = read(Q / "reference-manifest.json")
check("reference_original_and_copy", sha(ref["path"]) == ref["sha256"] == sha(ref["preserved_copy_path"]))

rows = {}
for path in sorted(Q.glob("arm-*/**/image_runs.ndjson")):
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        run_id = row["run_id"]
        if run_id in rows:
            check("duplicate_ledger_row_identical:" + run_id, canonical(row) == canonical(rows[run_id]))
        rows[run_id] = row
expected_runs = {"e44edd2822f76b42", "6814f82691c58852", "1bbb3bc74c3502f8", "77a442926234cdf2", "a74369d920440caa", "598e8c9471e7c156", "9d2f2d49080ac1e9"}
check("seven_actual_native_attempts", set(rows) == expected_runs)
statuses = Counter(r["status"] for r in rows.values())
check("six_outputs_one_unscored_block", statuses == {"success": 6, "safety_block": 1}, dict(statuses))

arms = []
artifact_hashes = {}
for arm, cfg in CONFIG.items():
    d = Q / arm / "v2"
    manifest = read(d / "run_manifest.json")
    pack_list = read(d / "candidate_pack.json")
    check(arm + ":one_pack_emitted", len(pack_list) == 1)
    pack = pack_list[0]
    comp = read(d / "composed_prompt.json")
    runtime = read(d / cfg["runtime"])
    native = read(d / cfg["native_args"])
    review = read(d / cfg["review"])
    pixel_audit = read(d / cfg["pixel_audit"])
    row = rows[manifest["ledger_run_id"]]
    for name in ["authorial_core.json", "creative_controls.json", "request_envelope.json"]:
        check(arm + ":frozen_v1_v2_bytes:" + name, sha(d / name) == sha(Q / arm / name))
    check(arm + ":actual_user_envelope", sha(d / "request_envelope.json") == sha(Q / "request-envelope.json"))
    check(arm + ":dictionary", pack["provenance"]["tags_hash"] == DICT)
    check(arm + ":core_lock_binding",
          pack["authorial_core"]["canonical_sha256"] == manifest["authorial_core_sha256"] == row["authorial_core_sha256"]
          and pack["authorial_core"]["intent_lock"]["canonical_sha256"] == manifest["intent_lock_sha256"] == row["intent_lock_sha256"])
    slots = {c["id"]: c for slot in pack["slots"].values() for c in slot["candidates"]}
    bundles = {c["id"]: c for c in pack["candidate_bundles"]["candidates"]}
    selected_members = set(comp["chosen_candidate_ids"])
    for candidate_id in comp["chosen_candidate_ids"]:
        if candidate_id in bundles:
            selected_members.update(c["id"] for c in bundles[candidate_id]["member_candidates"])
    check(arm + ":all_target_ids_exposed", set(cfg["targets"]) <= set(slots), cfg["targets"])
    check(arm + ":all_target_ids_selected", set(cfg["targets"]) <= selected_members, sorted(selected_members))
    check(arm + ":ordinary_candidate_budget", len(slots) <= pack["coverage"]["candidate_limits"]["total"] == 64, len(slots))
    for label in ["composed_audit", "runtime_audit"]:
        audit = read(d / cfg[label])
        check(arm + ":" + label, audit["status"] == "pass" and not audit["failures"])
    check(arm + ":review_schema", not pixel_audit["schema_failures"])
    check(arm + ":prompt_negative_byte_content",
          (d / cfg["prompt"]).read_text().rstrip("\n") == comp["prompt_en"]
          and (d / cfg["negative"]).read_text().rstrip("\n") == comp["negative_en"])
    check(arm + ":actual_tool_runtime_prompt", native["prompt"] == runtime["runtime_prompt_en"])
    check(arm + ":actual_tool_reference", native["referenced_image_paths"] == [ref["path"]])
    check(arm + ":ledger_selection_and_prompt",
          row["pack_id"] == pack["pack_id"] == comp["pack_id"]
          and row["prompt_en"] == comp["prompt_en"] and row["negative_en"] == comp["negative_en"]
          and row["chosen_candidate_ids"] == comp["chosen_candidate_ids"]
          and row["chosen_visual_concept_ids"] == comp["chosen_visual_concept_ids"])
    check(arm + ":contract_hash_binding",
          pixel_audit["effective_visual_contract_sha256"] == manifest["effective_visual_contract_sha256"] == row["effective_visual_contract_sha256"] == runtime["effective_visual_contract_sha256"])
    im = manifest["image_hashes"][0]
    check(arm + ":unmodified_native_original", sha(im["path"]) == im["sha256"] == sha(cfg["original"]))
    check(arm + ":independence_record", row["cross_arm_inputs_used"] is False and manifest["cross_arm_inputs_used"] is False)
    required = pixel_audit["required_hard_gates"]
    failed = {g["gate"] for g in pixel_audit["failed_hard_gates"]}
    selected_gates = [g for g in required if g.startswith("vo_pe_")]
    physical = [g for g in required if g.startswith("embodiment_")]
    if arm == "arm-a-film-optics":
        effects = review["native_outcomes"]["original_effects"]
        reference_status = review["native_outcomes"]["reference_scope"]["status"]
    else:
        effects = review["effects"]
        reference_status = review.get("reference_scope_status", review.get("reference_result", {}).get("status"))
    check(arm + ":three_effect_reviews", len(effects) == 3 and all(e["status"] in ["pass", "fail"] for e in effects))
    effect_pass = sum(e["status"] == "pass" for e in effects)
    all_of = effect_pass == 3 and not failed and reference_status == "pass"
    check(arm + ":technical_record_consistency", bool(pixel_audit["technical_qualified"]) == all_of)
    record = {
        "arm": arm, "revision": "v2", "pack_id": pack["pack_id"],
        "scene_seed": pack["provenance"]["seed"], "image_model_seed_controlled": False,
        "v1_effect_pass": cfg["v1_effect_pass"], "effect_pass": effect_pass, "effect_total": 3,
        "strict_all_of": "PASS" if all_of else "FAIL", "effects": effects,
        "target_source_ids_exposed_and_selected": cfg["targets"],
        "chosen_candidate_ids": comp["chosen_candidate_ids"], "chosen_visual_concept_ids": comp["chosen_visual_concept_ids"],
        "selected_profile_gates": {"pass": len(set(selected_gates) - failed), "total": len(selected_gates)},
        "physical_gates": {"pass": len(set(physical) - failed), "total": len(physical)},
        "reference_status": reference_status, "user_acceptance": "pending", "ledger_run_id": manifest["ledger_run_id"],
        "image": im, "prompt_path": str(d / cfg["prompt"]), "negative_path": str(d / cfg["negative"]),
        "pre_render_tests": str(d / cfg["pre_render"]), "independent_review_path": str(d / cfg["review"]),
        "source_core_sha256": manifest["authorial_core_sha256"], "intent_lock_sha256": manifest["intent_lock_sha256"],
        "effective_visual_contract_sha256": manifest["effective_visual_contract_sha256"],
        "parent_review": "Root separately inspected the unchanged native original after generation and agrees with the recorded effect verdicts. This is not user acceptance.",
    }
    arms.append(record)
    for name in ["run_manifest.json", "candidate_pack.json", "composed_prompt.json", "authorial_core.json", "creative_controls.json", "request_envelope.json", "image_runs.ndjson", cfg["prompt"], cfg["negative"], cfg["pre_render"], cfg["native_args"], cfg["runtime"], cfg["composed_audit"], cfg["runtime_audit"], cfg["pixel_audit"], cfg["review"]]:
        artifact_hashes[str((d / name).relative_to(ROOT))] = sha(d / name)
    artifact_hashes[str(Path(im["path"]).relative_to(ROOT))] = im["sha256"]

aggregate = {
    "original_effect_tests": {"pass": sum(a["effect_pass"] for a in arms), "total": 9},
    "scene_all_of": {"pass": sum(a["strict_all_of"] == "PASS" for a in arms), "total": 3},
    "target_source_ids_exposed_and_selected": {"pass": sum(len(a["target_source_ids_exposed_and_selected"]) for a in arms), "total": 10},
    "selected_profile_gates": {"pass": sum(a["selected_profile_gates"]["pass"] for a in arms), "total": 14},
    "physical_gates": {"pass": sum(a["physical_gates"]["pass"] for a in arms), "total": 15},
    "reference_appearance_scope": {"pass": sum(a["reference_status"] == "pass" for a in arms), "total": 3},
    "successful_images": statuses["success"], "unscored_safety_blocks": statuses["safety_block"],
    "actual_image_tool_calls": len(rows), "v2_actual_image_tool_calls": 3,
    "successfully_emitted_candidate_packs": 6, "unemitted_snapshot_cli_failure": 1,
}
check("aggregate_matches_saved_verdicts", aggregate["original_effect_tests"]["pass"] == 5 and aggregate["scene_all_of"]["pass"] == 1 and aggregate["selected_profile_gates"]["pass"] == 10 and aggregate["physical_gates"]["pass"] == 15)
result = {
    "contract_version": "photo-editing-coordinator-qualification/v1", "revision": "v2", "date": "2026-10-01",
    "dictionary_sha256": DICT, "registry_sha256": REGISTRY, "source_file_count": len(source["files"]),
    "integrity_status": "PASS" if all(c["status"] == "PASS" for c in checks) else "FAIL",
    "integrity_check_count": len(checks), "integrity_failures": [c for c in checks if c["status"] == "FAIL"],
    "checks": checks, "aggregate": aggregate, "arms": arms, "artifact_sha256": artifact_hashes,
    "attempt_ledger": [{"run_id": r["run_id"], "arm": r["arm_id"], "attempt": r["attempt"], "status": r["status"], "pack_id": r["pack_id"]} for r in rows.values()],
    "qualification_boundary": "This script verifies saved artifacts and aggregates independent native-pixel review records. It does not read or judge pixels. Root's separate native-image inspection is recorded per arm. Gates and macro effect tests overlap and must not be summed as independent trials. Seeds control concept/pack selection; native image-model sampling is not controlled. 133 candidates are not all pixel-qualified; user acceptance is pending.",
}
(Q / "coordinator-review.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["integrity_status", "integrity_check_count", "integrity_failures", "aggregate"]}, ensure_ascii=False, indent=2))
raise SystemExit(0 if result["integrity_status"] == "PASS" else 1)
