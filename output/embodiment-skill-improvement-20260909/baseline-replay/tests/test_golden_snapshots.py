"""Golden snapshot regression tests.

Rule-mode generation and concept resolution are fully deterministic for a
fixed seed, so these tests pin byte-stable snapshots of the CLI surface.
Any intentional data or behavior change must regenerate the fixtures:

    UPDATE_GOLDEN=1 .venv/bin/python -m pytest tests/test_golden_snapshots.py

and the resulting fixture diff is reviewed like code.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
WRAPPER_PATH = SKILL_DIR / "scripts" / "generate_photo_prompt.py"
GOLDEN_DIR = Path(__file__).resolve().parent / "golden"

UPDATE_GOLDEN = os.environ.get("UPDATE_GOLDEN") == "1"

GENERATION_PRESET_IDS = [
    "street_documentary",
    "magazine_fashion",
    "cyberpunk_city",
    "food_editorial",
    "wedding_candid_documentary",
]
GENERATION_SEEDS = [42, 1337]

GENERATION_CONCEPT_CASES = [
    {"id": "concept_company_worker", "concept": "회사원", "seed": 42},
    {"id": "concept_maid_vampire", "concept": "카리나 메이드 흡혈귀", "seed": 701},
    {"id": "concept_maid_beastkin", "concept": "카리나 메이드 수인", "seed": 317},
    {"id": "concept_princess_femmefatale", "concept": "설윤 공주 팜므파탈", "seed": 812},
    {"id": "concept_tracksuit_wizard", "concept": "운동복 마법사", "seed": 55},
]

EXPLAIN_CONCEPTS = [
    "회사원",
    "공주",
    "마법사",
    "수인",
    "흡혈귀",
    "카리나 메이드 흡혈귀",
    "유나 바니걸",
    "카리나 메이드 수인",
    "설윤 공주 팜므파탈",
    "윈터 간호사 구미호",
    "오피스룩",
    "직장인",
    "운동복 마법사",
    "산타복 수인",
    "방구석 집돌이",
]
EXPLAIN_SEED = 42


def run_wrapper(argv: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, str(WRAPPER_PATH), *argv],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        env={**os.environ, "GEMINI_API_KEY": "", "GOOGLE_API_KEY": ""},
    )
    if result.returncode != 0:
        raise AssertionError(
            f"wrapper failed ({result.returncode}) for argv={argv}\nstderr: {result.stderr[-2000:]}"
        )
    return result.stdout


def normalize_path_args(args: list[str]) -> list[str]:
    normalized = []
    for value in args:
        if isinstance(value, str) and str(ROOT) in value:
            value = value.replace(str(ROOT), "<ROOT>")
        normalized.append(value)
    return normalized


def normalize_generation_output(stdout: str) -> list[dict[str, Any]]:
    results = json.loads(stdout)
    normalized = []
    for item in results:
        provenance = item.get("provenance") or {}
        normalized.append(
            {
                "preset_id": item.get("preset_id"),
                "prompt_en": item.get("prompt_en"),
                "prompt_ko": item.get("prompt_ko"),
                "negative_en": item.get("negative_en"),
                "negative_ko": item.get("negative_ko"),
                "choices": item.get("choices"),
                "quality_verdict": (item.get("quality") or {}).get("verdict"),
                "prompt_id": provenance.get("prompt_id"),
                "negative_id": provenance.get("negative_id"),
                "seed": provenance.get("seed"),
                "selection_mode": provenance.get("selection_mode"),
            }
        )
    return normalized


def normalize_explanation(explanation: dict[str, Any]) -> dict[str, Any]:
    # Full recipe payloads are pinned by their own asset file; the golden pins
    # the resolver behavior (matching, bundle/species selection, forced slots).
    return {
        "concept": explanation.get("concept"),
        "concept_mode": explanation.get("concept_mode"),
        "name": explanation.get("name"),
        "role": explanation.get("role"),
        "applied_mixins": explanation.get("applied_mixins"),
        "matched": explanation.get("matched"),
        "selected_bundles": explanation.get("selected_bundles"),
        "selected_species_variants": explanation.get("selected_species_variants"),
        "combined_forced_slots": explanation.get("combined_forced_slots"),
        "soft_anchor_spec": explanation.get("soft_anchor_spec"),
        "forced_slots_applied": explanation.get("forced_slots_applied"),
        "gate_results": explanation.get("gate_results"),
    }


def load_or_update_golden(name: str, actual: Any) -> Any:
    path = GOLDEN_DIR / f"{name}.json"
    if UPDATE_GOLDEN:
        GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return actual
    if not path.exists():
        raise AssertionError(
            f"golden fixture missing: {path}. Run with UPDATE_GOLDEN=1 to create it."
        )
    return json.loads(path.read_text(encoding="utf-8"))


class GoldenSnapshotTests(unittest.TestCase):
    maxDiff = None

    def assert_golden(self, name: str, actual: Any) -> None:
        expected = load_or_update_golden(name, actual)
        self.assertEqual(
            expected,
            actual,
            msg=(
                f"golden snapshot mismatch: tests/golden/{name}.json. "
                "If this change is intentional, regenerate with UPDATE_GOLDEN=1 "
                "and review the fixture diff."
            ),
        )

    def test_preset_generation_snapshots(self) -> None:
        for preset_id in GENERATION_PRESET_IDS:
            for seed in GENERATION_SEEDS:
                with self.subTest(preset=preset_id, seed=seed):
                    stdout = run_wrapper(
                        [
                            "--preset",
                            preset_id,
                            "--seed",
                            str(seed),
                            "--selection-mode",
                            "rule",
                            "--include-choices",
                        ]
                    )
                    actual = normalize_generation_output(stdout)
                    self.assert_golden(f"preset_{preset_id}_seed{seed}", actual)

    def test_concept_generation_snapshots(self) -> None:
        for case in GENERATION_CONCEPT_CASES:
            with self.subTest(case=case["id"]):
                stdout = run_wrapper(
                    [
                        "--concept",
                        case["concept"],
                        "--seed",
                        str(case["seed"]),
                        "--selection-mode",
                        "rule",
                        "--include-choices",
                    ]
                )
                actual = normalize_generation_output(stdout)
                self.assert_golden(case["id"], actual)

    def test_explain_concept_snapshots(self) -> None:
        for concept in EXPLAIN_CONCEPTS:
            with self.subTest(concept=concept):
                stdout = run_wrapper(
                    [
                        "--concept",
                        concept,
                        "--seed",
                        str(EXPLAIN_SEED),
                        "--selection-mode",
                        "rule",
                        "--explain-concept",
                    ]
                )
                payload = json.loads(stdout)
                actual = {
                    "concepts": [
                        normalize_explanation(item) for item in payload.get("concepts", [])
                    ],
                    "forward_args": normalize_path_args(payload.get("forward_args", [])),
                }
                self.assert_golden(f"explain_{concept.replace(' ', '_')}", actual)


if __name__ == "__main__":
    unittest.main()
