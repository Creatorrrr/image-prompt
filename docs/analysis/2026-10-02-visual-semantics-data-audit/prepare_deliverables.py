"""Build the executed companion notebook and reviewed inline Data inputs.

Reads local audit artifacts and current sources. Never writes runtime assets.
The notebook cells are executed here; outputs are captured, not invented.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
os.chdir(ROOT)


def load(name):
    return json.loads((OUT / name).read_text())


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    metrics = load("metrics.json")
    notebook_cells = []
    namespace = {"__name__": "__notebook__"}

    def markdown(text):
        notebook_cells.append({"cell_type": "markdown", "metadata": {},
                               "source": text.splitlines(keepends=True)})

    def execute(code):
        stream = io.StringIO()
        count = 1 + sum(c["cell_type"] == "code" for c in notebook_cells)
        with contextlib.redirect_stdout(stream):
            exec(compile(code, f"notebook-cell-{count}", "exec"), namespace)
        notebook_cells.append({"cell_type": "code", "metadata": {},
            "execution_count": count, "source": code.splitlines(keepends=True),
            "outputs": [{"output_type": "stream", "name": "stdout",
                         "text": stream.getvalue().splitlines(keepends=True)}]})
        return code

    markdown("# 시각 의미 데이터 분석 재현\n\n"
             "2026-10-02 소스 스냅샷. 저장소 루트를 작업 디렉터리로 사용한다. "
             "원본 해시와 현재 레지스트리를 직접 확인하고, 저장된 resolver 진단을 집계한다. "
             "소스에서 파생한 진단은 독립 holdout이나 이미지 품질 측정이 아니다.\n")
    execute('''import collections, csv, hashlib, json, sys
from pathlib import Path
ROOT = Path.cwd()
OUT = ROOT / "docs/analysis/2026-10-02-visual-semantics-data-audit"
metrics = json.loads((OUT / "metrics.json").read_text())
manifest = json.loads((OUT / "source-manifest.json").read_text())
inventory = list(csv.DictReader((OUT / "profile-inventory.csv").open()))
print("commit:", metrics["commit"])
print("captured_at_kst:", metrics["captured_at_kst"])
''')
    inventory_code = execute('''source_counts = []
for entry in manifest["files"]:
    path = ROOT / entry["path"]
    if path.name.startswith("photo_prompt_visual_obligations") and path.suffix == ".json":
        source_counts.append((path.name, len(json.loads(path.read_text())["profiles"])))
profiles = sum(count for _, count in source_counts)
groups = sum(int(row["component_groups"]) for row in inventory)
assert len(source_counts) == metrics["totals"]["files"]
assert profiles == len(inventory) == metrics["totals"]["compiled_profiles"]
assert groups == metrics["totals"]["component_groups"]
print(json.dumps({"registry_files": len(source_counts), "profiles": profiles,
                  "component_groups": groups}, ensure_ascii=False))
''')
    execute('''mismatches = [entry["path"] for entry in manifest["files"]
              if hashlib.sha256((ROOT / entry["path"]).read_bytes()).hexdigest() != entry["sha256"]]
assert not mismatches, mismatches
print("Source hashes unchanged:", len(manifest["files"]))
print("Existing index validation:", metrics["structure_checks"])
''')
    distribution_code = execute('''distribution = metrics["source_distribution"]
groups_total = metrics["totals"]["component_groups"]
chart_rows = []
labels = ["기본", "Y2K", "의복", "코스튬", "장신구", "수영복"]
grouped = [(label, row["profiles"], row["component_groups"])
           for label, row in zip(labels, distribution[:6])]
grouped.append(("기타", sum(row["profiles"] for row in distribution[6:]),
                sum(row["component_groups"] for row in distribution[6:])))
for family, profile_count, component_count in grouped:
    for basis, count, denominator in [("프로필 비중", profile_count, profiles),
                                      ("구성 요소 비중", component_count, groups_total)]:
        chart_rows.append({"family": family, "basis": basis, "count": count,
                           "denominator": denominator,
                           "share": round(count / denominator * 100, 2)})
assert sum(count for _, count, _ in grouped) == profiles
assert sum(count for _, _, count in grouped) == groups_total
print(json.dumps(chart_rows, ensure_ascii=False, indent=2))
''')
    language_code = execute('''flags = metrics["profile_flags"]
guard = metrics["discovery_guard_details"]
language_rows = [
    {"metric": "한국어 exact/alias 존재", "count": flags["exact_has_korean"], "denominator": profiles},
    {"metric": "한국어 positive 검색 텍스트 존재", "count": flags["semantic_text_has_korean"], "denominator": profiles},
    {"metric": "모든 구성 요소 그룹에 한국어 대안 존재", "count": flags["all_component_groups_have_korean"], "denominator": profiles},
    {"metric": "guarded 중 한국어 구성 요소 대안 전무", "count": guard["guarded_with_no_korean_component_terms"], "denominator": guard["guarded_profiles"]},
]
for row in language_rows:
    row["share_pct"] = round(row["count"] / row["denominator"] * 100, 1)
print(json.dumps(language_rows, ensure_ascii=False, indent=2))
''')
    markdown("## 자체 구성 요소와 제외 조건의 일관성\n\n"
             "현재 운영 함수를 실행한다. 그룹 첫 표현을 이어 만든 문맥은 소스 기반 진단이며 "
             "실제 스킬의 공개 authorial core를 대신하지 않는다.\n")
    conflict_code = execute('''sys.path.insert(0, str(ROOT / "skills/photo-prompt-image-generator/scripts"))
import prompt_generator as pg
registry = pg.load_visual_obligation_registry(ROOT / "skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json")
conflict_rows = []
for profile in registry["profiles"]:
    context = "; ".join(group["any_terms"][0] for group in profile["semantics"]["component_semantics"]["groups"])
    eligible, reason = pg.visual_profile_context_applicability(
        profile, context, has_authorial_core_context=True, require_positive_context_terms=False)
    if not eligible and reason == "request_exclusion":
        conflict_rows.append({"profile_id": profile["id"], "reason": reason})
recorded = json.loads((OUT / "source-component-context-conflicts.json").read_text())
assert {row["profile_id"] for row in conflict_rows} == {row["profile_id"] for row in recorded}
print("Self-context request exclusions:", len(conflict_rows), "/", len(registry["profiles"]))
print(json.dumps(conflict_rows, ensure_ascii=False, indent=2))
''')
    markdown("## Resolver 진단 집계\n\n"
             "조회 결과는 retrieval_probes.py가 실제 resolver를 실행해 저장한 28건이다. "
             "여기서는 전체 resolver를 다시 돌리지 않고 결과를 집계한다. "
             "질의 임베딩 API, 후보 채택, 생성·픽셀 평가는 포함하지 않는다.\n")
    execute('''probes = json.loads((OUT / "retrieval-probes.json").read_text())
assert probes["completed"] is True
assert len(probes["cases"]) == 28
probe_summary = []
for tier in ["natural_request_only", "source_derived_exact_control", "source_derived_component_control", "broad_or_negative_control"]:
    cases = [case for case in probes["cases"] if case["tier"] == tier]
    probe_summary.append({"tier": tier, "cases": len(cases),
        "target_hits": sum(case["target_hit"] is not None for case in cases),
        "target_hard": sum(bool(case["target_hit"] and case["target_hit"]["hard_eligible"]) for case in cases),
        "any_hard": sum(bool(case["hard_profile_ids"]) for case in cases)})
print(json.dumps(probe_summary, ensure_ascii=False, indent=2))
''')
    vector_code = execute('''pairs = json.loads((OUT / "near-duplicate-vector-pairs.json").read_text())
contrast_pairs = [{"left": row["left"], "right": row["right"], "cosine": row["cosine"]}
                  for row in pairs if row["cosine"] >= 0.95]
assert len(contrast_pairs) == metrics["vector_checks"]["pair_counts_by_threshold"]["0.95"] == 6
print(json.dumps(contrast_pairs, ensure_ascii=False, indent=2))
''')
    markdown("## 해석과 개선 순서\n\n"
             "자기 모순 21개를 먼저 고치고, 한국어 구성 요소 표현과 반대 의미 대조를 보강한다. "
             "높은 벡터 유사도는 실제 오검색률이나 중복의 증거가 아니다. "
             "수요 자료 없이 분야별 개수를 같은 비율로 늘리지 않는다. "
             "다음 검증에서는 요청과 baseline을 데이터 조회 전에 고정하고, "
             "등록·검색·채택·프롬프트·픽셀·사용자 수용을 구별한다.\n")
    dump("visual-semantics-audit.ipynb", {
        "nbformat": 4, "nbformat_minor": 5, "cells": [
            {**cell, "id": f"audit-{i:02d}"} for i, cell in enumerate(notebook_cells, 1)],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python", "version": sys_version()},
                     "audit_source_commit": metrics["commit"],
                     "audit_captured_at_kst": metrics["captured_at_kst"]}})

    # Source disclosures contain reviewed relative file labels, never host paths.
    date_scope = "2026-10-02 소스 스냅샷; commit 0e5cc0d1"

    def source(files, definitions, caveats):
        return {"label": "로컬 시각 의미 데이터 전수 분석", "files": [{"label": f} for f in files],
                "metricDefinitions": [{"label": k, "definition": v} for k, v in definitions],
                "filters": ["photo-prompt-image-generator 현재 로더가 읽는 레지스트리 23개", date_scope],
                "caveats": caveats}

    def item(id_, title, source_, columns, rows, code, assumptions=None):
        result = {"id": id_, "title": title, "queries": [{"id": id_ + "-query", "source": source_,
            "reportingPeriod": date_scope, "capturedAt": metrics["captured_at_kst"],
            "columns": columns, "rows": rows, "methods": [{"language": "python", "code": code}]}]}
        if assumptions:
            result["assumptions"] = assumptions
        return result

    chart_rows = namespace["chart_rows"]
    chart_source = source(["source-distribution.csv", "metrics.json", "profile-inventory.csv"], [
        ("프로필 비중", "한 계열의 프로필 개수 / 전체 1,385개 × 100"),
        ("구성 요소 비중", "한 계열의 구성 요소 그룹 수 / 전체 3,289개 × 100")], [
        "구성 요소와 프로필의 의미 크기는 동일하지 않다; 두 비중은 서로 다른 분모를 사용한다.",
        "프로필 개수 상위 6개 파일과 나머지 17개 파일을 묶었다.",
        "사용 빈도·개념 범위·이미지 성공률을 측정한 비중이 아니다."])
    dump("distribution-chart-input.json", {"schemaVersion": 1, "id": "visual-semantics-distribution",
        "queryId": "source-distribution", "title": "계열별 구성 비중",
        "chart": {"type": "horizontalBar", "x": "family", "y": "share", "series": "basis",
                  "xLabel": "전체 대비 비중 (%)", "yLabel": "파일 계열",
                  "showXAxisLabel": True, "showYAxisLabel": True},
        "rows": chart_rows, "source": chart_source, "theme": "codex-classic"})
    dump("distribution-sources-input.json", {"schemaVersion": 1, "items": [item(
        "distribution", "개수 기준에 따라 분포가 어떻게 달라지는가?", chart_source,
        ["family", "basis", "count", "denominator", "share"], chart_rows, distribution_code)]})

    inventory_rows = [{"metric": k, "count": v} for k, v in [
        ("운영 레지스트리 파일", metrics["totals"]["files"]),
        ("프로필", metrics["totals"]["compiled_profiles"]),
        ("exact 검색 행", metrics["totals"]["exact_lookup_rows"]),
        ("구성 요소 그룹", metrics["totals"]["component_groups"]),
        ("프로필 ID 중복", metrics["structure_checks"]["duplicate_profile_ids"]),
        ("exact 검색어 충돌 그룹", metrics["structure_checks"]["exact_term_collision_groups"])]]
    items = [item("inventory", "현재 규모와 구조적 일관성은 어떠한가?", source(
        ["source-manifest.json", "metrics.json", "profile-inventory.csv", "analyze.py"],
        [("프로필", "현재 운영 로더로 컴파일한 레코드 하나"),
         ("인덱스 검증", "기존 validate_visual_profile_index_metadata를 실행한 결과")],
        ["등록·컴파일·인덱스의 일관성을 확인한 결과이며 이미지 품질을 인증하지 않는다."]),
        ["metric", "count"], inventory_rows, inventory_code)]
    items.append(item("self-context", "제외 조건과 자체 구성 요소가 충돌하는가?", source(
        ["source-component-context-conflicts.json", "prompt_generator.py", "analyze.py"],
        [("자기 문맥 충돌", "그룹 any_terms의 첫 표현을 이어 현재 context applicability에 넣었을 때 request_exclusion인 프로필")],
        ["소스 파생 진단이며 정상 공개 core나 독립 요청 평가가 아니다.",
         "21건을 모든 실사용 요청의 실패로 일반화할 수 없다."]),
        ["profile_id", "reason"], namespace["conflict_rows"], conflict_code))
    items.append(item("korean-access", "한국어 구성 요소 표현을 어디부터 보강할 것인가?", source(
        ["profile-inventory.csv", "metrics.json", "analyze.py"],
        [("한국어 존재", "가-힣 범위의 한글 문자 존재; 표현의 정확도는 별도 검토"),
         ("guarded", "semantic_discovery_requires_component_evidence=true인 프로필")],
        ["한글 표현 부재가 질의 이해 실패를 뜻하지 않는다; 실제 baseline 경로와 함께 검증해야 한다."]),
        ["metric", "count", "denominator", "share_pct"], namespace["language_rows"], language_code))
    items.append(item("contrast-pairs", "가장 유사한 여섯 쌍을 합쳐도 되는가?", source(
        ["near-duplicate-vector-pairs.json", "metrics.json", "photo_prompt_visual_profile_index.json"],
        [("cosine", "기존 768차원 문서 벡터를 L2 정규화해 계산한 서로 다른 프로필 쌍의 내적")],
        ["정의를 검토한 여섯 쌍은 역할·주체·방향이 반대인 의미다.",
         "질의 임베딩이나 실제 오검색률을 측정하지 않았다; 유사도는 중복 판정이 아니다."]),
        ["left", "right", "cosine"], namespace["contrast_pairs"], vector_code))
    dump("findings-sources-input.json", {"schemaVersion": 1, "items": items})
    print(json.dumps({"notebook_code_cells": sum(c["cell_type"] == "code" for c in notebook_cells),
                      "reviewed_chart_rows": len(chart_rows), "sources_items": len(items)}, ensure_ascii=False))


def sys_version():
    import sys
    return sys.version.split()[0]


if __name__ == "__main__":
    main()
