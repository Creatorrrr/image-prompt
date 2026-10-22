"""Verify saved artifacts and record the coordinator's direct visual review.

The observations below were authored after viewing all three exact originals.
This script checks bytes/provenance; it does not automate visual judgments.
"""
from pathlib import Path
import hashlib
import json
import struct
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
GEN = "ef02180fc06f390a079ecb7727ece11c2dd30e54394f9e1ae8b9112217bd29ac"
REF = Path("/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg")
EXPECTED_SKILL = "f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089"

def read(p):
    return json.loads(Path(p).read_text())

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")

def gate(name, status, evidence, observability="visible"):
    return dict(id=name, status=status, observability=observability, evidence_ko=evidence)

reviews = {
    "A": [
        gate("scene_daily_outdoors", "pass", "공원 길·나무·벤치, 작업복 인물, 노출된 뿌리와 미완의 제거 작업이 한 화면에 보인다."),
        gate("system_personal_status", "pass", "GARDENER LV 12, STAMINA 8/100, 짧은 황색 바, ROOTBREAK 00:42가 읽힌다. 정지된 표시 상태까지의 증거다."),
        gate("status_owner_connection", "pass", "패널에서 같은 인물의 손목 장치까지 황색 선이 이어지고 얼굴과 눈이 패널 쪽을 향한다."),
        gate("resource_action_consequence", "pass", "같은 인물·낮은 자원 표시·쉬는 자세·지면에 놓인 도구·남은 뿌리가 함께 보인다. 피로의 실제 원인이나 시간 경과는 확인하지 않는다."),
        gate("reference_appearance_guidance", "pass", "짧은 어두운 단발과 가는 앞머리, 얼굴의 전반적 외형 참고가 보인다. 신원 일치 판정은 하지 않는다."),
        gate("embodiment_complete", "fail", "화면 왼쪽의 인물 오른손이 도구를 잡고 인물 왼팔이 올라온 무릎에 놓였다. 사전 지정한 왼손 도구·오른팔 무릎과 반대다. 지지와 도구-발 간격은 자연스럽다."),
    ],
    "B": [
        gate("B1_genre_system_item_relation", "pass", "유리 공방과 중앙 바이알이 보이며 LANTERN VIAL/UNCOMMON/MIST SIGHT +12/VALUE 18 SILVER 패널의 선이 같은 바이알 내부 빛에 닿는다."),
        gate("B2_craft_progress_owner", "pass", "제작자 몸 가까운 GLASSCRAFT Lv.7, XP 84/100과 바가 읽히고 작업복·도구가 직업 문맥을 제공한다."),
        gate("B3_trade_causality", "pass", "같은 작업대의 제작자·구매자·평가된 물건·가죽 위 동전에 닿는 구매자 손과 물건 쪽 주의가 함께 보인다. 구매 순간의 개연성까지이며 실제 마음의 변화나 거래 이력은 증명하지 않는다."),
        gate("B4_reference_scope", "pass", "참고 사진과 유사한 어두운 단발·가는 앞머리·얼굴 표현이 충분한 크기로 보인다."),
        gate("B5_physical_coherence", "pass", "작용하는 손의 소유자, 바이알·동전·작업대 접촉과 지지가 자연스럽고 패널-물체 연결 끝점이 보인다. 이 일반 판정은 정확한 받침 지지 판정과 구분한다."),
        gate("B6_I01_complete_information_structure", "pass", "한 패널에 물건 이름 위계, 라벨/값 행, 구분선 아래 독립 CHARGE 6/6 자원 블록이 모두 읽힌다. 값은 표시 내용이며 실제 효과의 증거가 아니다."),
        gate("managed_embodiment_contact_and_space", "fail", "생성 전 검토한 엄지·검지의 넓은 받침 지지가 실제로는 바이알 하부 몸통을 감싸는 접촉으로 바뀌었다. 일반 접촉의 물리적 결함이라고 해석하지 않는다."),
    ],
    "C": [
        gate("c_choice_hand", "pass", "같은 탐험가가 따로 든 ECHO STEP 선택 카드와 STONE/SPARK 미사용 카드 두 장이 보인다."),
        gate("c_full_tactical_causal_chain", "fail", "카드-청록 선-왼쪽 발자국은 이어지지만 나팔/머리가 그 발자국을 향하는지 명확하지 않다. 앞으로 내민 발은 화면 아래 잘려 출구 문턱 접촉이 비관측이다.", "partial"),
        gate("c_bounded_skill_resource", "pass", "카드의 ECHO STEP과 같은 인물 근처 패널의 ECHO STEP, MP 0/2가 읽힌다. 실제 자원 감소를 증명하지 않는다."),
        gate("c_reference_appearance", "pass", "어두운 턱 길이 단발·가는 앞머리와 참고 얼굴의 전반적 외형이 보인다."),
        gate("c_dungeon_route", "fail", "결정질 벽·광산 등불·깊은 왼쪽 통로·밝은 오른쪽 출구가 보이지만 앞쪽 부츠가 잘려 양발 지지와 출구 통과 전체를 판단할 수 없다.", "partial"),
    ],
}

specs = {
    "A": dict(image="image.png", ledger="image-runs.ndjson", testcase="testcase-preimage-final.json", child_review="litrpg-pixel-review.json", occurrences=32, unique=30, new_exposed=[], new_retained=[], topic="pass", original_scene="fail", seed=10685162680402208503),
    "B": dict(image="generated-original.png", ledger="image_runs.ndjson", testcase="registered-scene-testcase.json", child_review="scene-pixel-review.json", occurrences=32, unique=32, new_exposed=["cand_821f6992d66a5e5bbc1fc22ad7ac9191"], new_retained=["cand_821f6992d66a5e5bbc1fc22ad7ac9191"], topic="pass", original_scene="pass", seed=12844093950900881390),
    "C": dict(image="image-original.png", ledger="image-runs.ndjson", testcase="testcase-precall.json", child_review="pixel-testcase-review.json", occurrences=40, unique=40, new_exposed=["cand_e4cb826520795860bac4494c97427c1c"], new_retained=[], topic="partial_fail", original_scene="fail", seed=1721707340431656770),
}

skill_path = ROOT / "skills/photo-prompt-image-generator/SKILL.md"
assert sha(skill_path) == EXPECTED_SKILL, "Skill drift: do not claim all arms used current version"
assert read(ROOT / "skills/photo-prompt-image-generator/retrieval-runtime.json")["generation_id"] == GEN
reference_sha = sha(REF)
source_changes = read(OUT / "SOURCE-CHANGES.json")
shared_files = {"skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json", "skills/photo-prompt-image-generator/references/maintenance.md"}
source_hash_observations = []
for f in source_changes["files"]:
    unchanged = sha(ROOT / f["path"]) == f["sha256"]
    source_hash_observations.append(dict(path=f["path"], integration_sha256=f["sha256"], current_sha256=sha(ROOT / f["path"]), unchanged=unchanged))
    if f["path"] not in shared_files:
        assert unchanged, f"Own module/config drift: {f['path']}"
# Shared workspace files acquired other concurrent additions after registration.
# Preserve them; verify our exact module registrations instead of reverting bytes.
manifest = read(ROOT / "skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json")
for module in (dict(file="photo_candidate_litrpg_system_20261022.json", kind="candidates"), dict(file="photo_candidate_litrpg_system_bindings_20261022.json", kind="slot_bindings")):
    assert manifest["modules"].count(module) == 1
assert "litrpg" in (ROOT / "skills/photo-prompt-image-generator/references/maintenance.md").read_text().lower()
dump("FINAL-SOURCE-HASH-OBSERVATION.json", dict(scope="Final read-only observation; shared-file drift is retained, own LitRPG modules and installed config are unchanged", files=source_hash_observations, own_module_registrations_intact=True))

registered = read(OUT / "PRECALL-REGISTRATION-FINAL.json")
for arm in registered["arms"]:
    for f in arm["files"]:
        assert sha(f["path"]) == f["sha256"], f"Pre-call gate drift: {f['path']}"

arms = []
for arm, spec in specs.items():
    run = ROOT / f"generated/photo-runs/litrpg-20261022-arm-{arm.lower()}"
    manifest = read(run / "run_manifest.json")
    ledger = [json.loads(x) for x in (run / spec["ledger"]).read_text().splitlines() if x.strip()]
    assert len(ledger) == 1 and ledger[0]["run_id"] == manifest["ledger_run_id"]
    assert manifest["image_call_count"] == ledger[0]["image_call_count"] == 1
    assert manifest["skill_sha256"] == EXPECTED_SKILL
    assert manifest["reference_sha256"] == [reference_sha]
    assert manifest["cross_arm_inputs_used"] is False
    assert GEN in manifest["source_ref"]
    prompt = run / "final-prompt.txt"
    native_plan = read(ledger[0]["native_render_plan_json"])
    actual_prompt = native_plan["payload"]["prompt"]
    assert ledger[0]["prompt_en"] == actual_prompt
    assert prompt.read_text() == actual_prompt + "\n", "Exported prompt must differ only by its terminal newline"
    assert hashlib.sha256(actual_prompt.encode()).hexdigest() == manifest["runtime_prompt_sha256"]
    assert native_plan["payload"]["referenced_image_paths"] == [str(REF)], "Native reference path missing"
    assert sha(ledger[0]["native_render_plan_json"]) == ledger[0]["native_render_plan_sha256"]
    image = run / spec["image"]
    assert sha(image) == manifest["image_hashes"][0]["sha256"]
    raw = image.read_bytes()
    assert raw[:8] == b"\x89PNG\r\n\x1a\n"
    dimensions = list(struct.unpack(">II", raw[16:24]))
    meta_file, original_key = {
        "A": ("native-tool-output-metadata.json", "tool_returned_path"),
        "B": ("image-tool-result-metadata.json", "returned_original_path"),
        "C": ("generation-observation.json", "returned_original"),
    }[arm]
    provider_original = Path(read(run / meta_file)[original_key])
    assert sha(provider_original) == sha(image), "Saved copy differs from provider original"
    if arm == "C":
        audit = json.loads(read(run / "review-audit-cli.json")["stdout"])
        workflow = read(run / "managed/workflow.json")
    else:
        audit = read(run / "review-audit-output.json")
        workflow = read(run / "workflow.json")
    assert audit["status"] == "pass" and audit["record_valid"] is True
    assert audit["technical_qualification"] == "fail"
    assert workflow["phase"] == "review_record_validated"
    entry = dict(arm=arm, random_seed=spec["seed"], run_path=str(run), image_path=str(image), image_sha256=sha(image), dimensions=dimensions,
                 prompt_path=str(prompt), prompt_file_sha256=sha(prompt), runtime_prompt_sha256=manifest["runtime_prompt_sha256"], prompt_file_has_terminal_newline=True, testcase_path=str(run / spec["testcase"]), testcase_sha256=sha(run / spec["testcase"]),
                 child_review_path=str(run / spec["child_review"]), manifest_path=str(run / "run_manifest.json"), ledger_run_id=manifest["ledger_run_id"],
                 provider_original_path=str(provider_original), provider_copy_hash_equal=True, review_record_valid=True, managed_technical_qualification="fail", managed_phase=workflow["phase"],
                 call_count=1, retry=False, generation_id=GEN, skill_sha256=EXPECTED_SKILL, source_occurrences=spec["occurrences"], unique_sources_within_arm=spec["unique"],
                 new_sources_exposed=spec["new_exposed"], new_sources_retained_as_general_inspiration=spec["new_retained"], native_whole_sources_adopted=[],
                 direct_original_review=True, root_review_blinded=False, gate_results=reviews[arm], topic_relation=spec["topic"], original_registered_scene=spec["original_scene"], full_arm="fail")
    if arm == "B":
        entry["new_information_structure"] = "pass"
        entry["full_rule"] = "AND(B1..B6, all managed gates); exact preimage contact gate fails"
    arms.append(entry)

review = dict(schema="litrpg-root-original-pixel-review/v1", reviewed_at_utc=datetime.now(timezone.utc).isoformat(), reviewer="Codex coordinator", inspection="view_image(detail=original), all three saved originals; qualitative human-readable model review, not an automated vision score",
              blind_review=False, prior_child_observations_available=True, reference_path=str(REF), reference_sha256=reference_sha,
              policy="partial_is_fail; UNOBSERVABLE_NOT_PASS; static visual claims and complete scene gates remain distinct", arms=arms,
              full_arm_passes=0, full_arm_tests=3, focal_relation_passes=2, focal_relation_partial_failures=1,
              no_matched_baseline_images=True, causal_quality_improvement_proved=False, native_source_qualification=False, requester_acceptance="pending")
dump("ROOT-PIXEL-REVIEW.json", review)
summary = dict(schema="litrpg-integration-image-test-summary/v1", evidence_integrity="pass", visual_test_aggregate="fail", actual_calls=3, saved_originals=3, retries=0,
               full_scene_passes=0, full_scene_tests=3, topic_relation_passes=2, topic_relation_partial_failures=1,
               all_predeclared_gate_hashes_unchanged=True, all_source_change_hashes_unchanged=all(f["unchanged"] for f in source_hash_observations), own_modules_and_runtime_config_unchanged=True,
               shared_file_drift=[f["path"] for f in source_hash_observations if not f["unchanged"]], own_module_registrations_intact=True,
               current_skill_sha256=EXPECTED_SKILL, shared_generation_id=GEN, shared_reference_sha256=reference_sha,
               data_validation_path=str(OUT / "DATA-VALIDATION.json"), root_review_path=str(OUT / "ROOT-PIXEL-REVIEW.json"), arms=arms,
               contribution_limit="A new exposure/use 0; B I01 exposed, retained general structure and visible; C Q11 exposed, rejected. No native whole-source adoption or causal image-quality improvement is established.", requester_acceptance="pending")
dump("IMAGE-TEST-SUMMARY.json", summary)
dump("FINALIZATION-NOTES.json", dict(scope="Coordinator evidence-check development; no image rerender or criterion changes", observations=[
    "An initial raw all-source-hash assertion detected concurrent changes to the shared corpus manifest and maintenance reference. Their drift is recorded, own module bytes/config remain equal, and exact LitRPG module registrations are asserted without reverting other work.",
    "An initial raw exported-prompt-file hash assertion found the terminal newline in all three text exports. Verification now asserts exact payload/ledger equality, export equals payload plus one newline, and both file-byte and actual-runtime hashes are preserved.",
    "The byte/provenance script does not assert a visual pass; all three full scenes remain FAIL."
]))
print(json.dumps({k: summary[k] for k in ("evidence_integrity", "visual_test_aggregate", "actual_calls", "saved_originals", "full_scene_passes", "topic_relation_passes")}, ensure_ascii=False))
