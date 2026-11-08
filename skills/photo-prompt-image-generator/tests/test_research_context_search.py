"""Acceptance checks for the bounded, research-only fetish context lookup."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
from photo_research_context_search import load_records, search


@pytest.mark.parametrize(("query", "expected"), [
    ("foot fetish", "FASHION-CONTEXT-014"), ("발 페티시", "FASHION-CONTEXT-014"),
    ("hand fetish", "FASHION-CONTEXT-015"), ("손 페티시", "FASHION-CONTEXT-015"),
    ("latex fetish", "FASHION-CONTEXT-033"), ("라텍스 페티시", "FASHION-CONTEXT-033"),
    ("shoe fetish", "FASHION-CONTEXT-028"), ("신발 페티시", "FASHION-CONTEXT-028"),
    ("uniform fetish", "FASHION-CONTEXT-036"), ("제복 페티시", "FASHION-CONTEXT-036"),
    ("fetish couture", "fashion-pose-context-FVP-10-075"),
    ("페티시 쿠튀르", "fashion-pose-context-FVP-10-075"),
    ("podophilia", "FASHION-CONTEXT-014"),
    ("trichophilia", "FASHION-CONTEXT-019"),
    ("라텍스 소재 페티시란", "FASHION-CONTEXT-033"),
    ("손을 좋아하는 페티시", "FASHION-CONTEXT-015"),
    ("발에 대한 페티시의 의미", "FASHION-CONTEXT-014"),
])
def test_real_lookup_ranks_requested_context_first(query, expected):
    result = search(query)
    assert result["results"][0]["id"] == expected
    assert result["results"][0]["tags"] == ["fetish"]
    assert result["results"][0]["context_only"] is True
    assert result["results"][0]["native_approval"] is False


def test_explicit_review_scope_and_general_fashion_boundary():
    reviewed = {f"FASHION-CONTEXT-{n:03d}" for n in (
        1, 2, 3, 4, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
        25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38,
    )} | {"fashion-pose-context-FVP-10-075"}
    records = load_records()
    assert {rid for rid, row in records.items() if "fetish" in row["tags"]} == reviewed
    for query in ("leather jacket", "가죽 재킷", "shoe", "발", "고양이 우주선"):
        result = search(query)
        assert not result["explicit_fetish_lookup"]
        assert all("fetish" not in row["tags"] for row in result["results"])
    # An explicit tag filter is an intentional request for the context.
    assert search("가죽", tag="fetish")["results"][0]["id"] == "FASHION-CONTEXT-032"


def test_each_reviewed_term_and_korean_alias_is_discoverable():
    reviewed = [r for r in load_records().values() if "fetish" in r["tags"]]
    assert len(reviewed) == 28
    for row in reviewed:
        for query in [row["term"], *row["search_aliases"]]:
            assert search(query)["results"][0]["id"] == row["id"], (row["id"], query)


def test_cli_returns_source_bound_context_not_candidate():
    run = subprocess.run(
        [sys.executable, str(SKILL / "scripts/photo_research_context_search.py"),
         "발 페티시", "--tag", "fetish", "--limit", "3"],
        capture_output=True, text=True, check=True,
    )
    result = json.loads(run.stdout)
    assert result["scope"] == "research_context_only"
    assert result["native_approval"] is False
    assert result["results"][0]["id"] == "FASHION-CONTEXT-014"
    assert len(result["results"][0]["source_sha256"]) == 64
    assert "candidate_id" not in result["results"][0]


def test_unrelated_visual_candidates_never_gain_fetish_tag():
    assets = SKILL / "assets"
    for path in assets.glob("photo_candidate_fashion_*20261108.json"):
        if "bindings" in path.name:
            continue
        rows = json.loads(path.read_text())["candidates"].values()
        for row in rows:
            assert "fetish" not in row.get("tags", [])
            assert "fetish" not in row["content"].get("tags", [])
