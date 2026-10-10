"""Assemble the delivery from immutable arm evidence; never invoke generation."""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]


def read(relative):
    return json.loads((HERE / relative).read_text())


def artifact(path):
    path = Path(path)
    return {
        "path": str(path.resolve()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


counts = read("INTEGRATION-COUNTS.json")
validation = read("VALIDATION.json")
scope = read("SCOPE-VERIFICATION.json")
provenance = read("NATIVE-PROVENANCE-VERIFICATION.json")
authorial = read("AUTHORIAL-BYTE-VERIFICATION.json")
links = read("ALL-NEW-LINKS-v2.json")
coordinator = read("PARENT-PIXEL-OBSERVATIONS.json")
a = read("arms/a/final_report.json")
b = read("arms/b/ARM_B_REPORT.json")
c = read("arms/c/requalification/result_summary.json")
a_gates = read("arms/a/native_gate_summary.json")
b_pixels = read("arms/b/pixel_review_not_run.json")
c_supplemental = read("arms/c/requalification/supplemental_pixel_review.json")

assert counts["new_candidates"] == counts["new_profiles"] == counts["new_bundles"] == 146
assert validation["status"] == scope["status"] == provenance["status"] == "PASS"
assert links["status"] == "PASS" and links["count"] == 146
assert validation["focused_tests_passed"] == 72
assert provenance["actual_native_calls"] == 3
assert provenance["delivered_images"] == 2 and provenance["blocked_attempts"] == 1
assert all(len(arm["roles"]) == 14 and all(role["bytes_equal"] for role in arm["roles"])
           for arm in authorial["arms"])
assert a_gates["technical_qualification"] == c["native_review_record"]["technical_qualification"] == "fail"
assert b_pixels["qualification"] == "UNOBSERVABLE_NOT_PASS"

generation = counts["runtime_generation_id"]
fingerprint = counts["runtime_source_fingerprint"]
skill_path = PROJECT / "skills/photo-prompt-image-generator/SKILL.md"
skill = artifact(skill_path)
assert skill["sha256"] == scope["canonical_skill_sha256"]
reference = artifact("/tmp/codex-remote-attachments/01a1212e-a00b-7170-8446-16480b2873ff/BAA7D121-91EF-4AF5-A73E-C42EEEE77809/1-사진-1.jpg")
assert reference["sha256"] == "048adbd3e4343a3725fec6aa0455aa1f367878560bc15d4493a18fde1ce8604c"
assert links["generation_id"] == generation and links["source_fingerprint"] == fingerprint

p_arms = {arm["arm"]: arm for arm in provenance["arms"]}
authorial_arms = {arm["arm"]: arm for arm in authorial["arms"]}
root_observations = {arm["arm"]: arm for arm in coordinator["observations"]}
for arm in p_arms.values():
    assert arm["image_call_count"] == 1 and all(arm["checks"].values())
    for image in arm["images"]:
        assert artifact(image["path"])["sha256"] == image["sha256"]

rows = []
for profile in a["selected_new_profiles"]:
    profile_id = profile["candidate_id"].split(":", 1)[1]
    rows.append({
        "arm": "a",
        "profile_id": profile_id,
        "selected_id": profile["candidate_id"],
        "assessment_role": "auditor_derived_required_hard_gate",
        "gate_id": profile["full_relation_native_gate_id"],
        "status": profile["full_relation_native_status"].upper(),
        "evidence": profile["native_evidence"],
        "review_scale": "native original; unresampled crops retained separately",
        "image": p_arms["a"]["images"][0],
        "pack_id": p_arms["a"]["pack_id"],
        "review": artifact(HERE / "arms/a/native_pixel_review_02.json"),
        "coordinator_observation": next(item for item in root_observations["a"]["new_relation_observations"] if item["profile_id"] == profile_id),
    })
for profile_id in ["wkr_wk074_selected_relation", "wkr_wk025_selected_relation"]:
    gate = next(gate for gate in b_pixels["required_visual_gates"] if gate["source_obligation_id"] == profile_id)
    rows.append({
        "arm": "b",
        "profile_id": profile_id,
        "selected_id": "visual-concept:" + profile_id,
        "assessment_role": "required_gate_not_run_no_image_artifact",
        "gate_id": gate["id"],
        "status": "UNOBSERVABLE_NOT_PASS",
        "evidence": gate["reason"],
        "review_scale": None,
        "image": None,
        "pack_id": p_arms["b"]["pack_id"],
        "error_evidence": artifact(HERE / "arms/b/attempt01_native_error.json"),
        "not_run_record": artifact(HERE / "arms/b/pixel_review_not_run.json"),
    })
for profile_id in ["wkr_wk047_selected_relation", "wkr_wk095_selected_relation"]:
    observation = next(item for item in c_supplemental["observations"] if item["id"] == profile_id)
    required = profile_id == "wkr_wk047_selected_relation"
    rows.append({
        "arm": "c",
        "profile_id": profile_id,
        "selected_id": "visual-concept:" + profile_id if required else "slot:body_pose:wkr_wk095_selected_relation_candidate",
        "assessment_role": "auditor_derived_required_hard_gate" if required else "supplemental_complete_relation_from_selected_ordinary_candidate",
        "gate_id": "vo_wkr_wk047_selected_relation_1" if required else None,
        "status": observation["status"].upper(),
        "evidence": observation["evidence"],
        "claim_limit": observation.get("claim_limit"),
        "review_scale": "native original; unresampled crops retained separately",
        "region_xyxy": observation["region_xyxy"],
        "image": p_arms["c"]["images"][0],
        "pack_id": p_arms["c"]["pack_id"],
        "review": artifact(HERE / "arms/c/requalification/supplemental_pixel_review.json"),
        "coordinator_observation": next(item for item in root_observations["c"]["new_relation_observations"] if item["profile_id"] == profile_id),
    })
assert len(rows) == 6
save("NATIVE-QUALIFICATION-LEDGER.json", {
    "schema": "wardrobe-native-qualification-ledger/v1",
    "generation_id": generation,
    "source_fingerprint": fingerprint,
    "review_policy": "same saved original image; all components and endpoints required; partial or hidden evidence is not pass",
    "rows": rows,
    "boundary": "Six selected relations across three independent arms. WK095 is supplemental, not an invented automatic hard gate. No estimate for all 146 new candidates, no causal improvement claim, and no requesting-user acceptance is inferred.",
})

follow_up = {
    "schema": "wardrobe-native-follow-up-plan/v1",
    "status": "planned_not_rendered",
    "source_generation": generation,
    "runtime_definition_change": "none; observed geometry/detail failures do not invalidate the current owner-bound definitions",
    "items": [
        {"arm": "a", "evidence": "WK008 gap occlusion", "next_validation": "Expose the same coat side panel and torso edge at native scale. Plan arm placement and camera projection without substituting a front opening or changing the locked body/garment meaning."},
        {"arm": "a", "evidence": "Buckle contact and planted-foot mismatch", "next_validation": "Show the mating tongue, separate housing and actual contact in one coherent state; keep each hand owner clear and both requested feet visibly supported."},
        {"arm": "c", "evidence": "WK047 unresolved fine interlacing/stitch separation", "next_validation": "Choose framing and garment-edge placement that give the weave and distinct stitched boundary sufficient original-resolution area. Grain, hat braiding and enlargement of an unresolved image are not substitute evidence."},
        {"arm": "c", "evidence": "Needle/thread/stitch endpoints and crossbody route", "next_validation": "Expose the right-hand needle grip, left-hand pinning contact, needle-eye-to-stitch thread and opposite-shoulder bag route in the same image; preserve exact counts and roles."},
        {"arm": "c", "evidence": "Supplemental pleat, ribbon anchor and boot-color drift", "next_validation": "Trace the adopted skirt pleats and ribbon anchor without hidden endpoints; retain separate clothing and accessory color owners."},
        {"arm": "b", "evidence": "Explicit output moderation block, no image returned", "next_validation": "Preserve the exact error and unobservable result. Do not retry unchanged or near-identically to bypass the block. Any later validation must be a distinct permitted task or an authorized alternative with its own provenance; none was executed here."},
        {"arm": "all", "evidence": "Limited coverage and B/C changed retrieval seeds", "next_validation": "Use held-out concepts and keep retrieval seeds identical when testing source changes. Predeclare reference, frozen authorial inputs, complete relation gates, native detail requirements and user-acceptance separation."},
    ],
    "maintenance_scope": "The qualification ledger and this plan are external maintenance evidence. Pixel failures are not silently converted into universal negative prompts, keywords, ranking boosts or stronger runtime activation.",
    "additional_generation_calls": 0,
}
save("FOLLOW-UP-PLAN.json", follow_up)

case_specs = {
    "a": {"concept": a["scene"], "random_seed": a["random_selection_evidence"]["random_seed"],
          "report": "arms/a/final_report.md", "report_json": "arms/a/final_report.json", "prompt": "arms/a/final_prompt.txt",
          "hard_gate_count": a_gates["derived_exact_gate_set"].__len__(), "passed": len(a_gates["pass_gate_ids"]), "failed": len(a_gates["fail_gate_ids"]), "not_observable": 0,
          "qualification": "FAIL", "failed_gate_ids": a_gates["fail_gate_ids"]},
    "b": {"concept": b["random_selection"]["selected"]["direction"], "random_seed": b["random_selection"]["seed"],
          "report": "arms/b/ARM_B_REPORT.md", "report_json": "arms/b/ARM_B_REPORT.json", "prompt": "arms/b/final_prompt_en.txt",
          "hard_gate_count": b_pixels["required_hard_gate_count"], "passed": b_pixels["passed_gate_count"], "failed": 0, "not_observable": b_pixels["not_observable_gate_count"],
          "qualification": "UNOBSERVABLE_NOT_PASS", "failure_inference": "No pixel/anatomy diagnosis from a provider error without an image."},
    "c": {"concept": c["concept"], "random_seed": c["concept_random_seed"],
          "report": "arms/c/requalification/REPORT.md", "report_json": "arms/c/requalification/result_summary.json", "prompt": "arms/c/requalification/prompt_en.txt",
          "hard_gate_count": c["native_review_record"]["required_hard_gates"], "passed": c["native_review_record"]["passed"], "failed": c["native_review_record"]["failed"], "not_observable": 0,
          "qualification": "FAIL", "failed_gate_ids": c["native_review_record"]["failed_gate_ids"]},
}
cases = []
for key, spec in case_specs.items():
    p = p_arms[key]
    neutral = authorial_arms[key]
    case = dict(spec)
    for role in ["report", "report_json", "prompt"]:
        case[role] = artifact(HERE / spec[role])
    case.update({
        "arm": key,
        "native_calls": p["image_call_count"],
        "generation_outcome": p["generation_outcome"],
        "images": p["images"],
        "pack_id": p["pack_id"],
        "ledger_run_id": p["ledger_run_id"],
        "ledger": artifact(p["ledger_path"]),
        "manifest": artifact(p["manifest_path"]),
        "prompt_word_count": len((HERE / spec["prompt"]).read_text().split()),
        "all_fourteen_neutral_roles_byte_identical": all(role["bytes_equal"] for role in neutral["roles"]),
        "retrieval_seeds": {"diagnostic": neutral["original_retrieval_seed"], "qualification": neutral["new_retrieval_seed"], "identical": neutral["retrieval_seed_identical"]},
        "selected_new_relation_results": [{"profile_id": row["profile_id"], "status": row["status"], "assessment_role": row["assessment_role"]} for row in rows if row["arm"] == key],
        "user_acceptance": "pending_not_yet_received",
    })
    cases.append(case)

asset_dir = PROJECT / "skills/photo-prompt-image-generator/assets"
runtime_sources = [artifact(asset_dir / name) for name in [
    "photo_prompt_wardrobe_owner_relations_extension.json",
    "photo_prompt_visual_obligations_wardrobe_owner_relations.json",
    "photo_prompt_source_manifest.json",
]]

save("DELIVERY.json", {
    "schema": "wardrobe-integration-delivery/v1",
    "finalized_at": datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
    "status": {
        "data_integration": "COMPLETE_LOCAL",
        "source_and_focused_validation": "PASS",
        "independent_test_execution": "COMPLETE_THREE_FIRST_NATIVE_INVOCATIONS",
        "native_semantic_qualification": "NO_WHOLE_IMAGE_FULL_PASS",
        "user_acceptance": "PENDING_NOT_YET_RECEIVED",
    },
    "integration": counts,
    "runtime_sources": runtime_sources,
    "source_binding": {"generation_id": generation, "source_fingerprint": fingerprint},
    "canonical_skill": skill,
    "reference": {**reference, "scope": "visible face and hair guidance only; no identity, actual age or body similarity inference"},
    "validation": {"focused_tests_passed": 72, "explicit_current_candidate_bundle_profile_links_verified": 146,
                   "full_suite": validation["full_unittest_discover"], "evidence": artifact(HERE / "VALIDATION.json")},
    "native_totals": {"calls": 3, "returned_images": 2, "blocked_attempts_without_image": 1, "repair_calls": 0, "fallback_calls": 0, "fully_qualified_whole_images": 0, "observed_model": None},
    "independence": {"agents": 3, "other_arm_material_used": False, "authorial_roles_rechecked_per_arm": 14,
                     "all_roles_byte_identical": True, "evidence": artifact(HERE / "AUTHORIAL-BYTE-VERIFICATION.json"),
                     "causal_limit": "B/C retrieval seeds changed; exposure differences are not a matched-seed causal experiment. Three selected cases do not measure all 146 candidates."},
    "cases": cases,
    "maintenance_evidence": {
        "native_qualification": artifact(HERE / "NATIVE-QUALIFICATION-LEDGER.json"),
        "coordinator_pixel_observations": artifact(HERE / "PARENT-PIXEL-OBSERVATIONS.json"),
        "native_provenance_verification": artifact(HERE / "NATIVE-PROVENANCE-VERIFICATION.json"),
        "follow_up_plan": artifact(HERE / "FOLLOW-UP-PLAN.json"),
        "source_maintenance_record": artifact(PROJECT / "docs/research-evidence/photo-prompt/extension-maintenance/wardrobe-owner-relations-20261010-v6.json"),
    },
    "preservation": {
        "existing_dirty_files_byte_unchanged": scope["existing_dirty_files_byte_unchanged"],
        "existing_asset_files_checked": scope["existing_asset_files_checked"],
        "directory_status_entries_not_byte_snapshotted": len(scope["directory_status_entries_not_byte_snapshotted"]),
        "all_original_manifest_rows_retained_exactly": scope["all_original_manifest_rows_retained_exactly"],
        "canonical_skill_byte_unchanged": scope["canonical_skill_byte_unchanged"],
        "evidence": artifact(HERE / "SCOPE-VERIFICATION.json"),
    },
    "git": {"original_head": scope["original_head"], "current_head": scope["current_head"], "commit_created": scope["commit_created"], "push_performed": scope["push_performed"]},
    "reader_report": artifact(HERE / "RESULTS.md"),
    "boundary": "Source, index, audit-record validity, actual generation, original pixels, whole-image semantic qualification and requesting-user acceptance remain distinct. Evidence assembly does not call an image generator or alter authored runtime definitions.",
})

print(json.dumps({"status": "DELIVERY_RECORDED", "data_entries_each": 146, "focused_tests_passed": 72,
                  "native_calls": 3, "images": 2, "blocked": 1, "whole_image_qualified": 0,
                  "reports": ["DELIVERY.json", "RESULTS.md", "NATIVE-QUALIFICATION-LEDGER.json", "FOLLOW-UP-PLAN.json"]}, ensure_ascii=False))
