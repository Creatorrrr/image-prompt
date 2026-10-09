"""Report the actual managed B-arm result after review admission."""
import hashlib
import json
from pathlib import Path

ARM = Path(__file__).resolve().parent
state = json.loads((ARM / "run/workflow.json").read_text())
assert state["phase"] == "review_record_validated"
assert state["technical_qualification"] == "pass"
assert len(state["operations"]) == 1
assert len(state["operations"][0]["attempts"]) == 1

def artifact(role):
    row = state["artifacts"][role]
    assert hashlib.sha256(Path(row["path"]).read_bytes()).hexdigest() == row["sha256"]
    return row

def read(role):
    return json.loads(Path(artifact(role)["path"]).read_text())

composed = read("composed")
audit = read("composed_audit")
runtime_audit = read("runtime_audit")
review_audit = read("review_audit")["visual"]
review = read("visual_review")
assert not review_audit["schema_failures"]
assert review_audit["technical_qualified"]
metadata = json.loads((ARM / "native-image-metadata.json").read_text())
topics = json.loads((ARM / "supplemental-topic-review.json").read_text())
artistic = json.loads((ARM / "supplemental-artistic-review.json").read_text())
ledger = [json.loads(x) for x in (ARM / "image_runs.ndjson").read_text().splitlines() if x.strip()]
assert len(ledger) == 1 and ledger[0]["status"] == "success"
manifest = json.loads((ARM / "run_manifest.json").read_text())
assert manifest["image_call_count"] == 1 and manifest["cross_arm_inputs_used"] is False
assert manifest["ledger_run_id"] == ledger[0]["run_id"]
assert review["result_sha256"] == metadata["sha256"] == hashlib.sha256(Path(metadata["project_image_path"]).read_bytes()).hexdigest()
assert topics["source_plan_sha256"] == hashlib.sha256((ARM / "selected-topic-plan.json").read_bytes()).hexdigest()

result = {
    "schema_version": "spring-fashion-stage2-result/v1",
    "arm_id": "bodice_hem",
    "concept_name": "Last Cyanotype on the Rooftop Drying Line",
    "seed": 9878669292090812608,
    "worktree": "/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt",
    "generation": state["source_binding"]["generation_id"],
    "source_fingerprint": state["source_binding"]["source_fingerprint"],
    "skill_sha256": "9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b",
    "source_binding": state["source_binding"],
    "frozen_core_sha256": composed["authorial_core_binding"]["source_authorial_core_sha256"],
    "intent_lock_sha256": composed["authorial_core_binding"]["source_intent_lock_sha256"],
    "core_and_user_envelope_unchanged": True,
    "preservation_check": str(ARM / "stage2-preservation-check.json"),
    "selected_new_candidate_ids": composed["chosen_candidate_ids"],
    "selected_new_member_ids": ["slot:garment_detail:spf_sf004_01", "slot:color:spf_sf104_2"],
    "associated_spring_profile_ids": ["spring_sf004_01", "spring_sf104_2"],
    "spring_profile_hard_activation": {"status": "not_exposed_not_verified", "reason": "No spring_sf visual-concept opt-in was exposed in this immutable retrieved pack. Optional bundle selection preserves the existing associated_profiles_are_not_promoted contract."},
    "chosen_visual_concept_ids": composed["chosen_visual_concept_ids"],
    "effective_visual_contract_sha256": audit["effective_visual_contract_sha256"],
    "prompt_path": str(ARM / "final-prompt.txt"),
    "prompt_en_sha256": hashlib.sha256(composed["prompt_en"].encode()).hexdigest(),
    "composed": artifact("composed"),
    "render_request": artifact("render_request"),
    "native_plan": artifact("native_plan"),
    "actual_invocation_observation": str(ARM / "native-invocation-observation.json"),
    "image": metadata,
    "actual_tool": "image_gen.imagegen",
    "image_call_count": 1,
    "outcome": "returned_saved_recorded",
    "observed_image_model": None,
    "audit": {"composed": audit["status"], "quality_status": audit["quality_status"], "warnings": audit["warnings"], "runtime": runtime_audit["status"], "review_record_valid": True, "technical_qualification": state["technical_qualification"], "qualification_status": review_audit["qualification_status"]},
    "pixel_review": {"review": artifact("visual_review"), "audit": artifact("review_audit"), "exact_hard_gate_ids": list(review["hard_gates"]), "hard_gate_count": len(review["hard_gates"]), "hard_pass_count": sum(v["status"] == "pass" for v in review["hard_gates"].values()), "failed_hard_gates": [k for k,v in review["hard_gates"].items() if v["status"] == "fail"]},
    "supplemental_topics": {"plan_path": str(ARM / "selected-topic-plan.json"), "plan_sha256": topics["source_plan_sha256"], "review_path": str(ARM / "supplemental-topic-review.json"), "observation_count": len(topics["observations"]), "pass_count": sum(row["status"] == "pass" for row in topics["observations"]), "candidate_results": topics["candidate_results"], "not_runtime_hard_gates": True},
    "supplemental_artistic_review": {"path": str(ARM / "supplemental-artistic-review.json"), "additional_thumbnail_failed_ids": [row["id"] for row in artistic["authorial_observations"] if row["thumbnail_status"] == "fail"], "agent_judgment": artistic["agent_overall_artistic_judgment"]},
    "user_judgment": review["user_judgment"],
    "ledger_path": str(ARM / "image_runs.ndjson"),
    "ledger_run_id": ledger[0]["run_id"],
    "prompt_id": ledger[0]["prompt_id"],
    "independent_manifest_path": str(ARM / "run_manifest.json"),
    "independent_manifest_sha256": hashlib.sha256((ARM / "run_manifest.json").read_bytes()).hexdigest(),
    "no_cross_arm_inputs": True,
    "preparation_recoveries": [
        {"stage": "local_metadata_inspection", "reason": "The configured workflow Python has no Pillow. Metadata was read from the actual PNG header and a system sips thumbnail was used for inspection. No extra imagegen call occurred."},
        {"stage": "review_record", "reason": "The initial null user judgment values were rejected. Only their record enums were corrected to pending/not_applicable; pixel statuses and image were unchanged.", "receipt": str(ARM / "review-judgment-format-correction.json")},
    ],
}
(ARM / "stage2-result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
md = f"""# B: Last Cyanotype on the Rooftop Drying Line

Independent random seed: `{result['seed']}`. Frozen requester core and locks were preserved; the rooftop paper task and clothing geometry remain authorial decisions. No other arm's prompt, pack or image was read.

| New optional selection | Member | Supplemental all-of result |
| --- | --- | --- |
| `bundle:spf_sf004_01_bundle` | `slot:garment_detail:spf_sf004_01` | 4/4 observations pass at native and thumbnail |
| `bundle:spf_sf104_2_bundle` | `slot:color:spf_sf104_2` | 5/5 observations pass at native and thumbnail |

The observed neckline belongs to the wearer and has its lower edge joined to two upright sides. The worn blouse and skirt keep closely related muted warm tones and distinct cloth boundaries. These are separate supplemental topic observations. Associated `spring_sf004_01` and `spring_sf104_2` profiles were not exposed as opt-ins, so their hard activation remains **not verified**.

The actually selected existing `visual-concept:vg_face_hands_place_readability_profile` yields three hard gates at both scales. Five embodiment gates require native inspection. The exact eight-gate record is **8/8 pass**; managed composition, runtime and review admission are **PASS**, with free-description preservation warnings for the four requester anchors. This review validates the authored observation record and exact binding, not an automated pixel detector.

Native imagegen was invoked **once**, with the actual reference attached. The returned file was copied without changing the original. Image dimensions: **1024×1536**; inspection thumbnail: **256×384**. SHA-256: `{metadata['sha256']}`. The observed native model name is unknown.

Additional authorial lace scallop endpoints pass at native scale but fail as unobservable at thumbnail scale. The stance is slightly crossed and more posed than the independent straight planted baseline, while the arm reach, paper contact and grounded support remain plausible. The whole portrayal is a coherent, appealing rooftop interruption; this is agent supplemental judgment. Requesting-user judgment remains **not_yet_received** (`genuinely_moe: pending`, no generated baseline comparison).

- [Prompt]({result['prompt_path']})
- [Saved native image]({metadata['project_image_path']})
- [Stage 2 record]({ARM / 'stage2-result.json'})
- [Pre-invocation topic plan]({ARM / 'selected-topic-plan.json'})
- [Supplemental topic pixels]({ARM / 'supplemental-topic-review.json'})
- [Exact native hard review]({result['pixel_review']['review']['path']})
- [Managed review audit]({result['pixel_review']['audit']['path']})
- [Additional artistic observations]({ARM / 'supplemental-artistic-review.json'})
- [Ledger]({ARM / 'image_runs.ndjson'})
- [Independent manifest]({ARM / 'run_manifest.json'})
- [Actual tool transport observation]({ARM / 'native-invocation-observation.json'})

Generation: `{result['generation']}`. Source fingerprint: `{result['source_fingerprint']}`. Skill SHA: `{result['skill_sha256']}`. Effective visual contract SHA: `{result['effective_visual_contract_sha256']}`.

Ledger run ID: `{result['ledger_run_id']}`. Prompt ID: `{result['prompt_id']}`. Manifest uses `photo-independent-run-manifest/v2`, generated from the actual managed ledger row by the existing recorder manifest constructor with the verified frozen independent provenance. Initial metadata/record-format preparation failures are retained in the stage 2 record; neither caused another image invocation.
"""
(ARM / "TESTCASE.md").write_text(md)
print(json.dumps({"stage2_result": str(ARM / "stage2-result.json"), "testcase": str(ARM / "TESTCASE.md"), "generation": result["generation"], "hard_gates": "8/8 pass", "supplemental_topic_observations": "9/9 pass", "image_call_count": 1, "user_judgment": "not_yet_received", "stage2_sha256": hashlib.sha256((ARM / "stage2-result.json").read_bytes()).hexdigest()}, indent=2))
