from __future__ import annotations

import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = ROOT / "skills" / "prompt-trend-scout"
SCRIPTS_DIR = SKILL_DIR / "scripts"
TARGET_TAGS = ROOT / "skills" / "photo-prompt-image-generator" / "assets" / "photo_prompt_tags.json"
TARGET_RECIPES = ROOT / "skills" / "photo-prompt-image-generator" / "assets" / "concept_recipes.json"

sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SKILL_DIR))

from analyze_corpus import analyze_records
from collect_sources import collect
from diff_against_photo_prompt import diff_candidates
from sanitize_examples import sanitize_records


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_registry(tmp_path: Path, *, x_enabled: bool = False) -> Path:
    inbox = tmp_path / "inbox"
    registry = {
        "registry_version": 1,
        "adapters": {
            "local_inbox": {
                "enabled": True,
                "collection_method": "local_inbox",
                "path": str(inbox),
                "rate_limit_per_run": 20,
            },
            "rss_atom": {"enabled": False, "collection_method": "allowed_feed", "feeds": []},
            "activitypub_public": {"enabled": False, "collection_method": "allowed_feed", "urls": []},
            "x_api": {
                "enabled": x_enabled,
                "collection_method": "official_api",
                "required_env": ["X_BEARER_TOKEN"],
                "endpoint": "https://api.x.com/2/tweets/search/recent",
                "query": "AI image prompt",
            },
            "threads_official": {"enabled": False, "collection_method": "official_api"},
        },
    }
    path = tmp_path / "registry.json"
    write_json(path, registry)
    return path


def make_inbox(tmp_path: Path) -> Path:
    inbox = tmp_path / "inbox"
    write_json(
        inbox / "sample.json",
        {
            "source_url": "https://example.invalid/thread/1",
            "platform": "local",
            "author_handle_raw": "@artist",
            "raw_text": "@artist neon colored rim light android on wet asphalt reflection. Do not repost. Follow me for more prompt by @artist",
            "image_description": "android portrait with panel seam, sensor eyes, cyan rim light, wet asphalt reflection",
        },
    )
    return inbox


def test_no_engagement_symbols_are_exposed():
    forbidden = {"like", "reply", "repost", "follow", "bookmark", "dm", "publish", "send_message"}
    for path in (SKILL_DIR / "adapters").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                assert node.name not in forbidden, f"{path} exposes {node.name}"
            if isinstance(node, ast.Attribute):
                assert node.attr not in forbidden, f"{path} calls {node.attr}"


def test_source_gates_skip_disabled_and_missing_token(tmp_path, monkeypatch):
    make_inbox(tmp_path)
    registry = make_registry(tmp_path, x_enabled=True)
    monkeypatch.delenv("X_BEARER_TOKEN", raising=False)
    result = collect(registry_path=str(registry), data_dir=str(tmp_path / "data"), limit=10)
    assert len(result["records"]) == 1
    assert any(item["adapter"] == "x_api" and item["reason"].startswith("missing_env") for item in result["skipped"])


def test_sanitize_strips_handles_promos_and_sets_reuse_flags(tmp_path):
    make_inbox(tmp_path)
    registry = make_registry(tmp_path)
    harvest = collect(registry_path=str(registry), data_dir=str(tmp_path / "data"))
    sanitized = sanitize_records(harvest["output"], data_dir=str(tmp_path / "data"))
    record = sanitized["records"][0]
    assert "@artist" not in record["sanitized_prompt"]
    assert "Follow me" not in record["sanitized_prompt"]
    assert record["no_raw_reuse"] is True
    assert "no_republish" in record["flags"]
    assert {item["type"] for item in record["stripped_segments"]} >= {"handle", "promo", "signature"}


def test_no_verbatim_rejects_candidate_that_matches_source_phrase(tmp_path):
    sanitized_path = tmp_path / "sanitized.json"
    write_json(
        sanitized_path,
        {
            "records": [
                {
                    "id": "s1",
                    "from_harvest_id": "h1",
                    "sanitized_prompt": "copied visual phrase",
                    "stripped_segments": [],
                    "image_observation": {"observed": ["copied_visual_phrase"]},
                    "abstract_visual_grammar": {"visual_elements": ["copied_visual_phrase"], "facets": {}},
                    "no_raw_reuse": False,
                    "flags": [],
                }
            ]
        },
    )
    candidates = analyze_records(str(sanitized_path), data_dir=str(tmp_path / "data"), verbatim_threshold=0.2)
    assert candidates["records"][0]["recommendation"] == "reject"


def test_diff_against_photo_prompt_marks_existing_and_new(tmp_path):
    candidate_path = tmp_path / "candidates.json"
    write_json(
        candidate_path,
        {
            "records": [
                {
                    "candidate_id": "existing",
                    "kind": "tag",
                    "target_asset": "photo_prompt_tags.json",
                    "proposed": {"slot": "lighting", "value": "soft_window", "en": "soft window light", "ko": "soft window light"},
                    "abstracted_from": ["s1"],
                    "frequency": 1,
                    "novelty": "new",
                    "overlap_with_existing": [],
                    "confidence": 0.5,
                    "rationale": "test",
                    "risk_flags": [],
                    "verbatim_similarity": 0,
                    "recommendation": "trial",
                },
                {
                    "candidate_id": "new",
                    "kind": "tag",
                    "target_asset": "photo_prompt_tags.json",
                    "proposed": {"slot": "lighting", "value": "trend_scout_new_light", "en": "trend scout new light", "ko": "trend scout new light"},
                    "abstracted_from": ["s2"],
                    "frequency": 1,
                    "novelty": "new",
                    "overlap_with_existing": [],
                    "confidence": 0.5,
                    "rationale": "test",
                    "risk_flags": [],
                    "verbatim_similarity": 0,
                    "recommendation": "trial",
                },
            ]
        },
    )
    diffed = diff_candidates(str(candidate_path), data_dir=str(tmp_path / "data"))
    by_id = {item["candidate_id"]: item for item in diffed["records"]}
    assert by_id["existing"]["novelty"] == "reinforce"
    assert by_id["new"]["novelty"] == "new"


def test_run_scout_report_and_no_auto_mutation(tmp_path):
    make_inbox(tmp_path)
    registry = make_registry(tmp_path)
    before = {TARGET_TAGS: sha(TARGET_TAGS), TARGET_RECIPES: sha(TARGET_RECIPES)}
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "run_scout.py"),
        "--registry",
        str(registry),
        "--data-dir",
        str(tmp_path / "data"),
        "--limit",
        "10",
    ]
    completed = subprocess.run(cmd, cwd=ROOT, check=True, text=True, capture_output=True)
    after = {TARGET_TAGS: sha(TARGET_TAGS), TARGET_RECIPES: sha(TARGET_RECIPES)}
    assert before == after
    report_line = [line for line in completed.stdout.splitlines() if line.startswith("Report markdown: ")][0]
    report_path = Path(report_line.split(": ", 1)[1])
    report_text = report_path.read_text(encoding="utf-8")
    assert "NO CHANGES APPLIED" in report_text
    assert "@artist" not in report_text
    assert "neon colored rim light" in report_text


def test_apply_reflection_requires_approval_and_defaults_to_dry_run(tmp_path):
    report = {
        "report_id": "r1",
        "generated_at": "2026-06-08T00:00:00Z",
        "no_changes_applied": True,
        "counts": {},
        "gate_status": {},
        "report_markdown": "NO CHANGES APPLIED",
        "candidates": [
            {
                "candidate_id": "c1",
                "kind": "tag",
                "target_asset": "photo_prompt_tags.json",
                "proposed": {"slot": "lighting", "value": "trend_scout_test", "en": "trend scout test", "ko": "trend scout test"},
                "abstracted_from": ["s1"],
                "frequency": 1,
                "novelty": "new",
                "overlap_with_existing": [],
                "confidence": 0.5,
                "rationale": "test",
                "risk_flags": [],
                "verbatim_similarity": 0,
                "recommendation": "trial",
            }
        ],
    }
    report_path = tmp_path / "report.json"
    write_json(report_path, report)
    missing_approval = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "apply_reflection.py"), "--report", str(report_path), "--select", "c1"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert missing_approval.returncode != 0
    dry_run = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "apply_reflection.py"),
            "--report",
            str(report_path),
            "--select",
            "c1",
            "--approved-by",
            "tester",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "DRY RUN" in dry_run.stdout
