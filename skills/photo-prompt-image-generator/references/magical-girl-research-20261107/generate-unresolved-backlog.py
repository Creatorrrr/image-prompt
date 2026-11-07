#!/usr/bin/env python3
"""Render an unresolved snapshot from existing research files; never fetch sources.

Run: python3 generate-unresolved-backlog.py > /tmp/magical-unresolved.md
Or:  python3 generate-unresolved-backlog.py --output /tmp/magical-unresolved.md
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parent
INPUTS = ("source-reconciliation.json", "review-progress.csv", "agent-source-quality-audit.md")
AUDIT_ROW = re.compile(r"^\| (MG-[^ |]+) \| (.+?) \| (.+)")
COUNT_FIELDS = ("unreviewed_lexical_match_count", "lexical_without_full_record_review",
                "full_record_comparisons", "core_only_comparisons", "review_depth_unreported")


def audit_rows(text: str) -> dict[str, tuple[str, str]]:
    result = {}
    for line in text.splitlines():
        match = AUDIT_ROW.match(line)
        if not match:
            continue
        row_id, _, tail = match.groups()
        cells = [cell.strip().replace("**", "") for cell in tail.split("|")]
        status = cells[0].split(" — ", 1)[0]
        note = cells[1] if len(cells) > 1 and cells[1] else cells[0].partition(" — ")[2]
        if row_id in result:
            raise ValueError(f"duplicate audit row: {row_id}")
        result[row_id] = (status, note)
    return result


def render() -> str:
    # Keep a byte-exact snapshot and reject concurrent modifications instead of
    # quietly joining files from different moments of a parallel update.
    raw = {name: (ROOT / name).read_bytes() for name in INPUTS}
    recon = json.loads(raw[INPUTS[0]])
    progress = list(csv.DictReader(io.StringIO(raw[INPUTS[1]].decode("utf-8"))))
    audit = audit_rows(raw[INPUTS[2]].decode("utf-8"))
    by_id = {row["id"]: row for row in recon["rows"]}
    csv_ids = [row["term_id"] for row in progress]
    if len(by_id) != len(recon["rows"]) or len(set(csv_ids)) != len(csv_ids):
        raise ValueError("duplicate row ID in reconciliation or progress")
    if set(by_id) != set(csv_ids) or set(by_id) != set(audit):
        raise ValueError("reconciliation, progress and audit row IDs do not match; retry after writers finish")
    for row in progress:
        for field in COUNT_FIELDS:
            if int(row[field] or "0") < 0:
                raise ValueError(f"negative count: {row['term_id']} {field}")
    if any((ROOT / name).read_bytes() != raw[name] for name in INPUTS):
        raise RuntimeError("input changed during snapshot; retry after writers finish")

    timestamp = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    lines = ["# 마법소녀 미해결 백로그 — 자동 집계", "",
        f"생성 시각: {timestamp}. 이 숫자는 생성 시점의 파일 스냅샷이며 병렬 작업 이후 달라질 수 있다.",
        "저장된 원장·진행 CSV·독립 감사표만 집계했다. 외부 URL에 접근하거나 후보 의미·조건을 재판정하지 않았다.",
        "같은 원문 행 또는 행–출처의 기존 검토가 3회에 이르면 재검토하지 않는다. "
        "입력 파일은 행–출처별 총 검토 횟수의 완전한 원장이 아니므로 이 스크립트는 3회 미만을 인증하지 않는다. "
        "파일별 해시는 기록하나 여러 파일이 같은 논리적 버전으로 갱신됐다고 보장하지 않는다.",
        "첫 기재 출처의 상태 기록은 행의 모든 원자 개념, 모든 출처나 후보, 런타임·픽셀 검증 완료를 뜻하지 않는다.", "",
        "입력 스냅샷 SHA-256:"]
    for name in INPUTS:
        lines.append(f"- `{name}`: `{hashlib.sha256(raw[name]).hexdigest()}`")
    lines += ["", f"## 출처: {len(audit)}행의 감사 상태", ""]
    grouped: dict[str, list[str]] = {}
    for row_id, (status, _) in audit.items():
        grouped.setdefault(status, []).append(row_id)
    for status, ids in sorted(grouped.items()):
        lines.append(f"- {status}: {len(ids)}행")
    lines += ["", "### 접근 제한·부분 확인 등 미해결", ""]
    pending = [(row_id, status, note) for row_id, (status, note) in audit.items()
               if status.startswith(("확인 불가", "부분 확인", "검색 발췌"))]
    for row_id, status, note in sorted(pending):
        lines.append(f"- [ ] `{row_id}` — {status}: {note}")
    lines += ["", "### 통합 원장의 행별 unresolved", ""]
    for row_id, item in sorted(by_id.items()):
        details = [str(detail.get("unresolved", "")).strip() for detail in item.get("external_review_details", [])]
        details = [detail for detail in details if detail]
        if details:
            lines.append(f"- [ ] `{row_id}` — " + " / ".join(details))
    lines += ["", "## 후보 미검토 및 검토 깊이", "",
        "수치는 행–후보 비교 또는 검색 단서 건수이며 중복 없는 후보 수가 아니다. "
        "표면 검색 0건은 관련 후보가 없거나 전수 검토했다는 증거가 아니다.", "",
        "| 행 | 상태 | 미검토 표면 단서 | 전체 레코드 미검토 단서 | 전체 레코드 비교 | 핵심만 비교 | 깊이 미기재 |",
        "|---|---|---:|---:|---:|---:|---:|"]
    for row in progress:
        values = [int(row[field] or "0") for field in COUNT_FIELDS]
        if row["candidate_review_status"] != "complete" or values[0] or values[1] or values[4]:
            lines.append("| " + " | ".join([row["term_id"], row["candidate_review_status"], *map(str, values)]) + " |")
    lines += ["", "### 별도 후보 검색의 미해결 기록", ""]
    for row_id, item in sorted(by_id.items()):
        for attempt in item.get("candidate_search_attempts", []):
            why = attempt.get("reason") or attempt.get("limitation") or attempt.get("status") or "추가 후보 및 표현은 미검토"
            source = attempt.get("review_file", "unknown")
            lines.append(f"- [ ] `{row_id}` — {why} (기록: `{source}`)")
    lines += ["", "## 일러스트·런타임", "",
        "- [ ] 일러스트 후보·바인딩·교차표 및 다른 연구 자산의 301행 의미 대응을 별도로 검토한다.",
        "- [ ] 사진·일러스트 정본, 검색 뷰, 인덱스 및 설치 런타임의 일치와 실제 노출을 확인한다.",
        "- [ ] 검색 적중·생성 성공과 픽셀 품질·인과적 개선을 분리해 평가한다.", ""]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write atomically here; otherwise print to stdout")
    args = parser.parse_args()
    result = render()
    if args.output is None:
        print(result, end="")
        return
    destination = args.output.resolve()
    # Do not silently overwrite one of the source ledgers.
    if destination in {(ROOT / name).resolve() for name in INPUTS}:
        raise ValueError("output must not overwrite an input ledger")
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=".magical-backlog-", dir=destination.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(result)
        os.replace(temp_name, destination)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


if __name__ == "__main__":
    main()
