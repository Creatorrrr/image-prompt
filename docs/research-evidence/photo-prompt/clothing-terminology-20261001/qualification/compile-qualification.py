"""Verify artifact bindings and compile recorded native-pixel qualification.

Pixel judgments come from named direct viewers, not from this program. The
runtime source remains frozen; qualification is a separate evidence overlay.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
EVIDENCE = Path(__file__).resolve().parent.parent
QUALIFICATION = EVIDENCE / "qualification"
SCRIPTS = ROOT / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPTS))
import audit_moe_render_review


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, payload):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


freeze = read(QUALIFICATION / "data-freeze.json")
integration = read(EVIDENCE / "runtime-integration.json")
for item in freeze["runtime_files"]:
    assert sha(ROOT / item["path"]) == item["sha256"], item["path"]
freeze_sha = sha(QUALIFICATION / "data-freeze.json")
coordinator = read(QUALIFICATION / "coordinator-review.json")
assert coordinator["source_data_freeze_sha256"] == freeze_sha

names = {
    "arm-1": {"image": "generated_image-1.png", "review": "pixel_review.json", "keyword_key": "keyword_results", "request": "runtime_request.json", "args": "native_tool_args.json", "concept": "도서관 건축 투어 / 구조적 테일러링", "seed": 2389700930},
    "arm-2": {"image": "first-native.png", "review": "native_pixel_review.json", "keyword_key": "pre_registered_keyword_results", "request": "image_render_request.json", "args": "native_image_args.json", "concept": "도예 작업실 / 니트와 카고 팬츠", "seed": 884213793},
    "arm-3": {"image": "generated-first.png", "review": "native_pixel_review.json", "keyword_key": "keyword_gates", "request": "runtime_request.json", "args": "native_args.json", "concept": "역 보관함 / 한복과 장신구", "seed": 1372153937},
}
arms = []
all_keywords = Counter()
all_hard = Counter()
profile_observations = {}
all_exposed = []
all_adopted = []
for arm, spec in names.items():
    path = QUALIFICATION / arm
    manifest = read(path / "run_manifest.json")
    image = path / spec["image"]
    assert manifest["image_call_count"] == 1
    assert manifest["cross_arm_inputs_used"] is False
    assert len(manifest["image_paths"]) == 1
    assert manifest["image_hashes"][0]["sha256"] == sha(image)
    assert freeze_sha in manifest["source_ref"]
    ledger = [json.loads(line) for line in (path / "image_runs.ndjson").read_text().splitlines() if line.strip()]
    assert len(ledger) == 1 and ledger[0]["image_call_count"] == 1
    assert ledger[0]["run_id"] == manifest["ledger_run_id"]
    assert ledger[0]["status"] == "success"
    pack = read(path / "candidate_pack.json")
    if isinstance(pack, list):
        assert len(pack) == 1
        pack = pack[0]
    assert pack["pack_id"] == manifest["pack_id"]
    assert pack["provenance"]["selection_mode"] == "semantic"
    composed = read(path / "composed_prompt.json")
    request = read(path / spec["request"])
    args = read(path / spec["args"])
    assert args["prompt"] == request["runtime_prompt_en"]
    assert args["referenced_image_paths"] == [ref["path"] for ref in request["references"]]
    for reference in request["references"]:
        assert sha(Path(reference["path"])) == reference["sha256"]
    assert request["runtime_negative_en"] == ledger[0]["negative_en"]
    assert read(path / "composed_audit.json")["status"] == "pass"
    assert read(path / "runtime_audit.json")["status"] == "pass"
    formal_path = path / ("moe_render_review.json" if arm == "arm-2" else "render_review.json")
    formal_review = read(formal_path)
    audited = audit_moe_render_review.audit_moe_render_review(
        pack, formal_review, composed=composed, review_path=formal_path.resolve()
    )
    assert not audited["schema_failures"]
    assert audited["qualification_status"] == "failed_technical_hard_gates"
    write(path / "coordinator-render-audit.json", audited)
    pixel_review = read(path / spec["review"])
    keyword_rows = pixel_review[spec["keyword_key"]]
    assert len(keyword_rows) == 8
    keyword_counts = Counter(row["status"] for row in keyword_rows)
    all_keywords.update(keyword_counts)
    all_hard.update(row["status"] for row in formal_review["hard_gates"].values())
    exposure = read(path / "exposure_adoption.json")
    if arm == "arm-3":
        exposed = [row["id"] for row in exposure["new_exposed"]]
        adopted = exposure["adopted_new_candidate_ids"] + exposure["adopted_new_visual_concepts"]
    else:
        exposed = exposure["new_exposed_ids"]
        adopted = (exposure["new_adopted_slot_ids"] + exposure["new_opted_profile_ids"]
                   if arm == "arm-1" else exposure["new_adopted_ids"])
    assert set(adopted) <= set(exposed)
    all_exposed.extend(exposed)
    all_adopted.extend(adopted)
    for binding in integration["variant_bindings"]:
        selected = "visual-concept:" + binding["profile_id"]
        if selected not in manifest["chosen_visual_concept_ids"]:
            continue
        gate_rows = {gate: formal_review["hard_gates"][gate] for gate in binding["render_gate_ids"]}
        profile_observations[binding["profile_id"]] = {
            "arm": arm, "candidate_id": binding["candidate_id"],
            "result_sha256": sha(image), "source_data_freeze_sha256": freeze_sha,
            "review_sha256": sha(formal_path),
            "gates": gate_rows,
            "native_profile_gate_status": "PASS" if all(row["status"] == "pass" for row in gate_rows.values()) else "FAIL",
            "whole_case_status": "FAIL", "user_acceptance": "pending",
        }
    arms.append({
        "arm": arm, "concept": spec["concept"], "seed": spec["seed"],
        "candidate_pack_count": 1, "selection_mode": "semantic", "fallback_observed": False,
        "native_image_calls": 1, "quality_retries": 0,
        "image_path": str(image.resolve()), "image_sha256": sha(image),
        "case_sha256": sha(path / "test_case.json"), "pack_id": pack["pack_id"],
        "pack_file_sha256": sha(path / "candidate_pack.json"),
        "composed_sha256": sha(path / "composed_prompt.json"),
        "runtime_request_sha256": sha(path / spec["request"]),
        "run_id": manifest["ledger_run_id"], "prompt_audit": "PASS", "runtime_audit": "PASS",
        "composed_quality": "warn; four non-blocking free-description coverage warnings preserved",
        "keyword_counts": dict(keyword_counts), "keyword_results": keyword_rows,
        "whole_case_status": "FAIL", "typed_hard_gate_count": len(formal_review["hard_gates"]),
        "typed_hard_gate_failed_count": len(audited["failed_hard_gates"]),
        "typed_schema_failures": [], "new_exposed_ids": exposed, "new_adopted_ids": adopted,
        "user_acceptance": "pending",
    })

# Preserve the initial coordinator observation and disclose disagreement.
# The independent arm's stricter unresolved geometry is retained in the final result.
reconciliation = {
    "contract_version": "clothing-pixel-review-reconciliation/v1",
    "coordinator_initial_review_sha256": sha(QUALIFICATION / "coordinator-review.json"),
    "arm_2_agent_review_sha256": sha(QUALIFICATION / "arm-2/native_pixel_review.json"),
    "initial_coordinator_arm_2": "8 PASS; whole-case PASS",
    "independent_agent_arm_2": "5 PASS, 3 PARTIAL; whole-case FAIL",
    "final_rule": "A visible approximation does not prove the complete predeclared construction. Unresolved geometry stays PARTIAL and makes the case FAIL.",
    "resolved_disagreements": [
        {"keyword": "raglan", "final_status": "PARTIAL", "reason": "Sloped knit lines do not independently trace the whole neckline-to-underarm construction seam; cable relief and folds remain confounds."},
        {"keyword": "cargo pocket", "final_status": "PARTIAL", "reason": "Attached flap and patch are clear, but their side border does not unambiguously show an expanded gusset wall."},
        {"keyword": "drawstring", "final_status": "PARTIAL", "reason": "The bow and ends are visible; both separate waistband casing exits are unresolved in the dark region."},
    ],
    "unchanged_criteria": True,
    "arm_1_and_arm_3_keyword_agreement": True,
    "final_whole_case_status": {arm: "FAIL" for arm in names},
    "new_image_calls": 0,
}
write(QUALIFICATION / "review-reconciliation.json", reconciliation)

overlay = {
    "contract_version": "clothing-variant-qualification-overlay/v1",
    "source_data_freeze_sha256": freeze_sha,
    "scope": "Only actually opted-in profile gates are qualified; this is separate from whole-case success and is not a matched baseline comparison.",
    "integrated_profiles": integration["profile_count"],
    "opted_in_profiles_tested": len(profile_observations),
    "profile_gate_status_counts": dict(Counter(row["native_profile_gate_status"] for row in profile_observations.values())),
    "untested_profile_count": integration["profile_count"] - len(profile_observations),
    "profiles": profile_observations,
    "other_profiles": "not_tested",
    "user_acceptance": "pending",
}
write(QUALIFICATION / "variant-qualification-overlay.json", overlay)

summary = {
    "contract_version": "clothing-integrated-three-arm-qualification/v1",
    "source_data_freeze_sha256": freeze_sha,
    "runtime_files_integrity": "PASS", "reference_files_integrity": "PASS",
    "runtime_integration": {key: integration[key] for key in (
        "research_record_count", "integrated_family_count", "candidate_count", "profile_count",
        "native_gate_count", "joint_bundle_count", "slot_counts", "backlog")},
    "three_independent_agents": True, "per_arm_independence_attested_in_manifest": True,
    "packs": 3, "native_image_calls": 3, "quality_retries": 0,
    "pixel_policy": "partial_is_fail", "keyword_observation_counts": dict(all_keywords),
    "whole_case_pass_count": 0, "whole_case_fail_count": 3,
    "typed_hard_gate_counts": dict(all_hard),
    "new_exposure_surface_counts": dict(Counter(item.split(":")[0] for item in all_exposed)),
    "exposure_note": "Adult-appeal augmentation surfaces repeat two already present source candidates; surfaces are not independent source variants.",
    "new_adopted_surface_count": len(all_adopted),
    "opted_in_new_profile_count": len(profile_observations),
    "baseline_render_comparison": "not_run", "causal_improvement": "not_established",
    "reference_scope": "visible adult-generated face/hair appearance; no identity, actual age, body or personality inference",
    "user_acceptance": "pending", "arms": arms,
    "validation": {
        "new_clothing_tests": "7 PASS",
        "dictionary_metadata": "PASS",
        "semantic_index_check": "PASS",
        "visual_index_check": "PASS: 1385 profiles, 3305 exact terms",
        "adjacent_traditional_costume_tests": "15 methods run; six pre-existing fixture mismatches unchanged; two pre-existing schema failures repaired",
        "broader_contract_tests": "53 methods run during index rebuild; seven stale-index failures passed on final-index rerun; eight unrelated routing fixture mismatches reproduce against byte-verified HEAD registry",
        "all_regressions_pass": False,
        "routing_baseline_same_outcomes": read(EVIDENCE / "validation/routing-baseline-comparison.json")["same_outcomes"],
    },
    "reconciliation": str((QUALIFICATION / "review-reconciliation.json").resolve()),
    "variant_overlay": str((QUALIFICATION / "variant-qualification-overlay.json").resolve()),
}
write(QUALIFICATION / "qualification-summary.json", summary)
print(json.dumps({"images": 3, "whole_case_pass": 0, "keywords": dict(all_keywords), "profile_gates": overlay["profile_gate_status_counts"], "source_integrity": "PASS"}))
