"""Unit tests for concept guide collection and review-gate auto-evaluation."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
WRAPPER_PATH = SKILL_DIR / "scripts" / "generate_photo_prompt.py"
RECIPES_PATH = SKILL_DIR / "assets" / "concept_recipes.json"

GUIDED_CONCEPTS = [
    "수인",
    "회사원",
    "공주",
    "흡혈귀",
    "팜므파탈",
    "멘헤라",
    "츤데레",
    "천사",
    "로봇",
    "악마",
    "얀데레",
    "암살자",
    "마법사",
]


def load_wrapper():
    spec = importlib.util.spec_from_file_location("ppg_wrapper_gates", WRAPPER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load wrapper module: {WRAPPER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GateAssertTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.w = load_wrapper()

    def test_mixin_shape_assert(self) -> None:
        spec = {"type": "mixin_shape", "mixin": "흡혈귀"}
        ok, _ = self.w.evaluate_gate_assert(spec, {"applied_mixins": ["흡혈귀"], "role": "메이드"}, None)
        self.assertTrue(ok)
        ok, _ = self.w.evaluate_gate_assert(spec, {"applied_mixins": ["흡혈귀", "수인"]}, None)
        self.assertFalse(ok)

    def test_forced_slot_any_assert(self) -> None:
        explanation = {"combined_forced_slots": {"subject": ["beastkin_subject"]}}
        ok, _ = self.w.evaluate_gate_assert(
            {"type": "forced_slot_any", "slot": "subject", "any_of": ["beastkin_subject"]}, explanation, None
        )
        self.assertTrue(ok)
        ok, _ = self.w.evaluate_gate_assert(
            {"type": "forced_slot_any", "slot": "subject", "any_of": ["office_worker"]}, explanation, None
        )
        self.assertFalse(ok)
        # Presence-only check.
        ok, _ = self.w.evaluate_gate_assert(
            {"type": "forced_slot_any", "slot": "species_marker"}, explanation, None
        )
        self.assertFalse(ok)

    def test_forced_slot_absent_assert(self) -> None:
        explanation = {"combined_forced_slots": {"prop": ["sheathed_utility_knife_prop"]}}
        ok, _ = self.w.evaluate_gate_assert(
            {"type": "forced_slot_absent", "slot": "prop", "values": ["sheathed_utility_knife_prop"]},
            explanation,
            None,
        )
        self.assertFalse(ok)
        ok, _ = self.w.evaluate_gate_assert(
            {"type": "forced_slot_absent", "slot": "prop", "values": ["other_prop"]}, explanation, None
        )
        self.assertTrue(ok)

    def test_role_costume_preserved_assert(self) -> None:
        role_recipe = {"set": ["costume_style=akihabara_maid_cafe_uniform"]}
        preserved = {"combined_forced_slots": {"costume_style": ["akihabara_maid_cafe_uniform"]}, "role": "메이드"}
        replaced = {"combined_forced_slots": {"costume_style": ["gothic_lolita_dress"]}, "role": "메이드"}
        ok, _ = self.w.evaluate_gate_assert({"type": "role_costume_preserved"}, preserved, role_recipe)
        self.assertTrue(ok)
        ok, _ = self.w.evaluate_gate_assert({"type": "role_costume_preserved"}, replaced, role_recipe)
        self.assertFalse(ok)

    def test_unknown_assert_type_fails(self) -> None:
        ok, detail = self.w.evaluate_gate_assert({"type": "bogus"}, {}, None)
        self.assertFalse(ok)
        self.assertIn("unknown", detail)

    def test_manual_gates_report_manual_status(self) -> None:
        gates = [{"id": "g1", "check": "look at it", "machine_checkable": False, "source": "x"}]
        results = self.w.evaluate_review_gates(gates, {}, None)
        self.assertEqual(results[0]["status"], "manual")


class ShippedGuidedConceptTests(unittest.TestCase):
    """Every migrated concept must expose a guide and pass its machine gates."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.recipes = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))

    def explain(self, concept: str) -> dict:
        result = subprocess.run(
            [
                sys.executable,
                str(WRAPPER_PATH),
                "--concept",
                concept,
                "--seed",
                "42",
                "--selection-mode",
                "rule",
                "--explain-concept",
            ],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr[-500:])
        return json.loads(result.stdout)["concepts"][0]

    def test_guided_concepts_have_guides_and_passing_machine_gates(self) -> None:
        for concept in GUIDED_CONCEPTS:
            with self.subTest(concept=concept):
                explanation = self.explain(concept)
                self.assertTrue(explanation.get("guide"), msg=f"{concept} has no guide")
                gate_results = explanation.get("gate_results") or []
                self.assertTrue(gate_results, msg=f"{concept} has no gate results")
                failures = [g for g in gate_results if g.get("status") == "fail"]
                self.assertEqual(failures, [], msg=f"{concept} machine gate failures: {failures}")

    def test_role_plus_mixin_gates_pass(self) -> None:
        explanation = self.explain("카리나 메이드 흡혈귀")
        statuses = {g["id"]: g["status"] for g in explanation["gate_results"]}
        self.assertEqual(statuses.get("mixin_shape"), "pass")
        self.assertEqual(statuses.get("role_costume_preserved"), "pass")

    def test_guide_definitions_exist_in_data(self) -> None:
        mixins = self.recipes["mixins"]
        for name in ("수인", "흡혈귀", "로봇", "얀데레"):
            guide = mixins[name].get("guide") or {}
            self.assertTrue(str(guide.get("definition_ko") or "").strip(), msg=name)
            self.assertTrue(mixins[name].get("review_gates"), msg=name)


if __name__ == "__main__":
    unittest.main()
