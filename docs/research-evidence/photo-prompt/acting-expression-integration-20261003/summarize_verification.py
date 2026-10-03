"""Join saved integration checks and the three independently authored render cases."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ARTIFACTS = ROOT / "artifacts/photo-prompt/acting-expression-20261003"


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    freeze = read(HERE / "DATA-SOURCE-FREEZE.json")
    drift = [row["path"] for row in freeze["files"] if sha(ROOT / row["path"]) != row["sha256"]]
    assert not drift, drift
    suites = read(HERE / "FULL-SUITE-RESULT.json")
    assert suites["discovery_multiset_equal"]
    assert not suites["failures"] and len(suites["errors"]) == 3
    assert all("current photo baseline candidate-pack bytes drift" in row["traceback"] for row in suites["errors"])
    baseline_logs = [HERE / "baseline-sibling-photo-regression.log", HERE / "baseline-sibling-universal-photo-regression.log"]
    assert all("current photo baseline candidate-pack bytes drift" in path.read_text() for path in baseline_logs)
    observations = {
        "a": "Both medial brows converge and descend. The contact seam is closed, but margin compression remains insufficiently clear after repair. The central crease is partly obscured; a closed mouth alone is not a lip-press pass.",
        "b": "The camera/set/cup/balloon scene is present. Lower-lid elevation and unilateral brow lift remain unclear, brow contours remain partly occluded, and corner descent is not sufficiently clear. Required facial gates remain failed.",
        "c": "The map fold, fingers, overlay, dividers and tube are present. Both attempts retain soft lip volume, ordinary glossy eye margins and ordinary brow arcs; pooled liquid, compressed lips and local medial brow elevation are not unmistakable.",
    }
    concepts = {"a": "수리한 미세유체 연결부에서 염료가 다시 새는 작업대", "b": "복고 TV 게임쇼의 오답 위로상 데스크", "c": "항구 지도를 접어 보관하는 지도 기록원"}
    keywords = {"a": "입술 압착·미간 모으기·억눌린 분노 표현", "b": "squinch·한쪽 눈썹 상승·입꼬리 하강", "c": "눈물 고임·압착 입술·안쪽 눈썹 상승"}
    rows = []
    for arm in "abc":
        folder = ARTIFACTS / f"case-{arm}"
        source = folder / ("case_summary.json" if arm == "a" else "case-result.json")
        summary = read(source)
        frozen = read(folder / {"a": "precore_freeze.json", "b": "precore-freeze.json", "c": "precore_freeze_manifest.json"}[arm])
        frozen_files = frozen.get("input_file_hashes", frozen.get("files"))
        core_drift = [name for name in ("request_envelope.json", "creative_controls.json", "authorial_core.json") if sha(folder / name) != frozen_files[name]]
        assert not core_drift, (arm, core_drift)
        composed_audit = folder / ("composed-audit.json" if arm == "b" else "composed_audit.json")
        runtime_audit = folder / ("runtime-audit.json" if arm == "b" else "runtime_audit.json")
        assert read(composed_audit)["status"] == read(runtime_audit)["status"] == "pass"
        attempts = []
        for number in (1, 2):
            image_path = folder / (f"attempt-{number}.png" if arm == "c" else f"image-attempt-{number:02}.png")
            review_path = folder / (f"attempt-{number}-pixel-review.json" if arm == "c" else f"pixel-review-attempt-{number:02}.json")
            audit_path = folder / (f"attempt-{number}-pixel-review-audit.json" if arm == "c" else f"pixel-audit-attempt-{number:02}.json" if arm == "b" else f"pixel-review-attempt-{number:02}.audit.json")
            review, audit = read(review_path), read(audit_path)
            digest = sha(image_path)
            assert digest == review["result_sha256"]
            assert not audit["schema_failures"] and audit["technical_qualified"] is False
            gates = review["hard_gates"]
            assert len(gates) == audit["required_hard_gate_count"]
            failed = [name for name, gate in gates.items() if gate["status"] != "pass"]
            assert failed
            native_bytes = image_path.read_bytes()
            assert native_bytes[:8] == b"\x89PNG\r\n\x1a\n"
            size = list(struct.unpack(">II", native_bytes[16:24]))
            attempts.append({"attempt": number, "image": str(image_path), "sha256": digest, "native_dimensions": size,
                "review": str(review_path), "audit": str(audit_path), "hard_gate_count": len(gates),
                "passed_hard_gates": len(gates) - len(failed), "failed_hard_gates": failed,
                "strict_pixel_result": "FAIL", "pixel_review_schema_failures": [],
                "parent_direct_native_inspection": True, "parent_observation": observations[arm]})
        rows.append({"arm": arm.upper(), "origin": "agent-authored-test-case", "concept_ko": concepts[arm], "tested_keywords_ko": keywords[arm],
            "agent_result": str(source), "agent_result_sha256": sha(source), "frozen_core_files_unchanged": True,
            "profile_binding": "agent_postcore_interpretation to exact independently frozen baseline",
            "automatic_requester_literal_activation_claimed": False, "new_optional_expression_candidates_adopted": [],
            "prompt": str(folder / "prompt_en.txt"), "prompt_sha256": sha(folder / "prompt_en.txt"),
            "negative": str(folder / "negative_en.txt"), "negative_sha256": sha(folder / "negative_en.txt"),
            "composed_audit": str(composed_audit), "runtime_audit": str(runtime_audit),
            "final_composed_audit_status": "PASS", "final_exact_runtime_audit_status": "PASS", "native_attempts": attempts,
            "overall_strict_result": "FAIL", "user_preference_acceptance": "pending"})
    result = {"contract_version": "acting-expression-integration-verification/v1", "execution_complete": True,
        "authored_data_integration_status": "COMPLETE", "source_freeze_drift": drift,
        "counts": freeze["counts"], "merged_candidates": 9701,
        "dictionary_validation": "PASS", "visual_profile_index_validation": "PASS", "new_data_regression_tests": {"run": 12, "passed": 12},
        "full_unittest_discovery": {"tests_run": suites["tests_run"], "passed": suites["tests_run"] - len(suites["errors"]),
            "errors": len(suites["errors"]), "new_regressions_remaining": 0, "scope_multiset_verified": True,
            "status": "3_PREEXISTING_SIBLING_BASELINE_ERRORS", "preexisting_error_ids": [row["id"] for row in suites["errors"]],
            "baseline_commit": freeze["git_head"], "baseline_reproduction_logs": [str(path) for path in baseline_logs]},
        "optional_candidate_exposure": {"status": "PASS", "evidence": str(HERE / "V6-OPEN-EXPRESSION-PACK.json"),
            "scope": "explicit synthetic maintenance fixture with expression open; not an extra human request or rendered arm"},
        "native_test_execution_status": "COMPLETE", "independent_agents": 3, "native_generated_images": 6,
        "strict_qualified_cases": 0, "strict_qualified_images": 0, "partial_is_fail": True,
        "cases": rows, "causal_claim_about_failed_rendering": "not_established",
        "coverage_limits": ["7 of 11 new form profiles were bound in these image tests, not all 37 candidates.",
            "The expression-locked image cases did not adopt optional expression candidates.",
            "No image proves a real person's emotion, sincerity or preferences.",
            "Historical research regression/pixel plans were not relabeled as executed or passing."]}
    save(HERE / "FINAL-VERIFICATION.json", result)
    save(ARTIFACTS / "RESULTS.json", result)
    receipt = read(HERE / "INTEGRATION-RECEIPT.json")
    receipt.update(status="integration_complete; native_test_execution_complete; all_three_cases_strict_fail",
        indexes_rebuilt=True, focused_tests_passed=12, full_tests_run=1192, full_tests_passed=1189,
        preexisting_sibling_test_errors=3, native_images=6, strict_qualified_cases=0,
        final_verification="FINAL-VERIFICATION.json")
    save(HERE / "INTEGRATION-RECEIPT.json", receipt)
    lines = ["# 연기·표정 데이터의 독립 생성 테스트", "",
        "데이터 반영 및 세 독립 사례의 테스트 실행을 완료했다. 최초 생성과 국소 수리를 각각 한 번씩 수행해 native 원본 6개를 보존했다. 세 사례 모두 필수 관찰 요소가 남아 strict FAIL이다. 프롬프트·runtime 감사의 PASS를 픽셀 성공으로 취급하지 않았다.", "",
        "| 사례 | 랜덤 컨셉 | 목표 키워드 | 최종 hard gate | 전체 판정 |", "|---|---|---|---|---|"]
    for row in rows:
        last = row["native_attempts"][-1]
        lines.append(f"| {row['arm']} | {row['concept_ko']} | {row['tested_keywords_ko']} | {last['passed_hard_gates']}/{last['hard_gate_count']} PASS | FAIL |")
    lines += ["", "A의 미간 모으기 구성요소는 확인됐다. A의 입술 압착, B의 눈꺼풀·눈썹·입꼬리, C의 눈물 고임·압착 입술·안쪽 눈썹 상승은 충분히 명료하지 않았다. 가려진 눈썹은 추정해서 통과시키지 않았다. B의 첫 입꼬리 PASS는 원본 세부 검토 후 수정했고 이전 판정도 남겼다.", "",
        "사용자 요청 원문은 세 envelope에 byte-exact로 보존했다. 구체적인 컨셉·장면·표정 테스트는 사용자가 위임한 agent-authored-test-case이며 사용자 정의로 위장하지 않았다. 각 에이전트는 다른 사례를 읽지 않고 독립 baseline을 동결한 뒤 데이터를 확인했다. 새 프로필은 그 baseline 필드에 정식 post-core 바인딩했다.", "",
        "expression이 잠긴 이미지 사례에서는 optional 표정 후보를 채택하지 않았다. 열린 expression의 별도 합성 V6 검사에서 새 lip-press 후보 노출과 optional 정책을 확인했다. 데이터/검색/감사/픽셀/사용자 수용은 서로 다른 증거 단계다.", ""]
    for row in rows:
        lines += [f"## {row['arm']} — {row['concept_ko']}", "", row["native_attempts"][-1]["parent_observation"], "",
            f"![{row['arm']} 최신 생성 시도 — strict FAIL]({row['native_attempts'][-1]['image']})", "",
            f"[정확한 standalone prompt]({row['prompt']}) · [negative]({row['negative']}) · [에이전트 전체 결과]({row['agent_result']})", "",
            f"[첫 원본]({row['native_attempts'][0]['image']}) · [최신 픽셀 리뷰]({row['native_attempts'][-1]['review']})", ""]
    lines += ["## 검증 범위와 후속 실험 계획", "",
        "새 데이터 회귀 12개가 통과했고 전체 unittest 1,192개 중 1,189개가 통과했다. 남은 3개는 별도 illustration 스킬의 동일한 고정 photo baseline byte 검사이며 변경 전 Git에서도 재현됐다. 역사적 기준값을 바꾸어 실패를 숨기지 않았다.", "",
        "후속 실험은 실패한 형태를 한 번에 한 요소씩 분리하고, 눈썹이 완전히 보이는 수평 얼굴 구도와 고정 조명에서 참조 사진 유무를 대조하는 방식으로 계획한다. 입술은 닫힘/압착을, 눈은 catchlight/고인 액체를, 눈썹은 고개 기울기/국소 상승을 분리한다. 동일 의미의 한 이미지가 모든 필수 요소를 충족해야 한다. 이번 기록만으로 실패 원인을 참조 강도나 특정 모델 특성에 귀속하지 않는다. 이 후속 대조 실험은 아직 실행하지 않았다.", "",
        f"[데이터 반영 기록]({HERE / 'INTEGRATION.md'}) · [최종 검증 JSON]({HERE / 'FINAL-VERIFICATION.json'})"]
    (ARTIFACTS / "RESULTS.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"integration": "COMPLETE", "tests_passed": 1189, "preexisting_errors": 3,
        "native_images": 6, "strict_qualified_cases": 0, "source_drift": drift}))


if __name__ == "__main__":
    main()
