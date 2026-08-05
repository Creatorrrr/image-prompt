from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
WRAPPER_PATH = SCRIPT_DIR / "generate_photo_prompt.py"
EVAL_PATH = SCRIPT_DIR / "eval_semantic.py"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
GENERALIZATION_PATH = SKILL_DIR / "assets" / "generalization_cases.jsonl"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_composed_prompt  # noqa: E402
import eval_semantic  # noqa: E402
import generate_photo_prompt  # noqa: E402


class PhotoPromptContractV2Tests(unittest.TestCase):
    def run_wrapper(self, *args: str):
        completed = subprocess.run(
            [sys.executable, str(WRAPPER_PATH), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_safety_contract_defaults_to_pass_and_evaluates_only_on_request(self):
        base_args = (
            "--concept",
            "유나 바니걸",
            "--selection-mode",
            "rule",
            "--seed",
            "11",
            "--emit-candidate-pack",
        )
        default_pack = self.run_wrapper(*base_args)[0]
        self.assertEqual(
            default_pack["safety"],
            {
                "mode": "automatic",
                "evaluation_requested": False,
                "status": "pass",
                "requires_user_approval": False,
                "items": [],
            },
        )

        evaluated_pack = self.run_wrapper(*base_args, "--safety-evaluation")[0]
        self.assertEqual(evaluated_pack["safety"]["mode"], "explicit_evaluation")
        self.assertTrue(evaluated_pack["safety"]["evaluation_requested"])
        self.assertEqual(evaluated_pack["safety"]["status"], "pass")
        self.assertFalse(evaluated_pack["safety"]["requires_user_approval"])
        self.assertTrue(evaluated_pack["safety"]["items"])
        self.assertTrue(all(item["status"] == "pass" for item in evaluated_pack["safety"]["items"]))

    def test_candidate_pack_integrity_and_assertions_fail_closed(self):
        pack = self.run_wrapper(
            "--preset",
            "product_hero_on_riser",
            "--selection-mode",
            "rule",
            "--seed",
            "17",
            "--emit-candidate-pack",
        )[0]
        chosen_id = next(
            candidate["id"]
            for candidate in pack["presets"]
            if candidate.get("selected_by_sampler")
        )
        composed = {
            "pack_id": pack["pack_id"],
            "prompt_en": "A restrained product still life with believable contact shadow, no text or watermark.",
            "negative_en": pack.get("negative_en"),
            "chosen_candidate_ids": [chosen_id],
            "composer": "agent",
        }
        passed = audit_composed_prompt.audit_composed_prompt(pack, composed)
        self.assertEqual(passed["status"], "pass", passed)

        tampered = copy.deepcopy(pack)
        tampered["provenance"]["seed"] = 999
        tampered_result = audit_composed_prompt.audit_composed_prompt(tampered, composed)
        self.assertIn("pack_integrity", {failure["check"] for failure in tampered_result["failures"]})

        spoofed = {**composed, "coverage_assertions": {"not-a-mandatory-intent": "product"}}
        spoofed_result = audit_composed_prompt.audit_composed_prompt(pack, spoofed)
        self.assertIn("coverage_assertions", {failure["check"] for failure in spoofed_result["failures"]})

        with self.assertRaisesRegex(ValueError, "exactly one pack"):
            audit_composed_prompt.first_pack([])
        with self.assertRaisesRegex(ValueError, "exactly one pack"):
            audit_composed_prompt.first_pack([pack, pack])

    def test_korean_no_people_intent_never_inverts_to_a_human_subject(self):
        pack = self.run_wrapper(
            "--preset",
            "environmental_portrait_composition",
            "--selection-mode",
            "rule",
            "--seed",
            "23",
            "--additional-requirement",
            "사람 없는 quiet brutalist reading room, no people",
            "--emit-candidate-pack",
        )[0]
        mandatory = {item["text"] for item in pack["mandatory_intents"]}
        self.assertTrue({"사람 없는", "no people"} <= mandatory)
        selected_subject = next(
            candidate
            for candidate in pack["slots"]["subject"]["candidates"]
            if candidate.get("selected_by_sampler")
        )
        self.assertNotIn("human", selected_subject.get("kind", []))
        active_axes = {axis["id"] for axis in pack["photographic_integration"]["active_axes"]}
        self.assertNotIn("person_presence", active_axes)

    def test_role_scene_variants_rotate_while_identity_core_stays_fixed(self):
        variant_ids = set()
        for seed in range(1, 13):
            _args, explanations = generate_photo_prompt.resolve_concepts(
                ["--selection-mode", "rule", "--seed", str(seed)],
                ["회사원"],
                concept_mode="soft",
            )
            explanation = explanations[0]
            variant_ids.add(explanation["selected_scene_variants"][0]["id"])
            forced = explanation["combined_forced_slots"]
            self.assertEqual(forced["subject"], ["office_worker"])
            self.assertEqual(forced["appearance_type"], ["corporate_professional"])
            self.assertEqual(forced["wardrobe_style"], ["clean_blazer_trousers"])
            self.assertNotIn("person_origin", forced)
        self.assertGreaterEqual(len(variant_ids), 2)

    def test_visual_review_contract_rejects_empty_or_unprovenanced_payloads(self):
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "review.json"
            review_path.write_text(json.dumps({"cases": []}), encoding="utf-8")
            summary = eval_semantic.summarize_visual_review(review_path)["visual_review"]
        self.assertFalse(summary["passed"])
        self.assertGreaterEqual(summary["contract_failure_count"], 3)
        self.assertEqual(summary["failed_case_count"], 0)

    def test_generalization_suite_is_executable_and_green(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(EVAL_PATH),
                "--tags",
                str(TAGS_PATH),
                "--generalization-cases",
                str(GENERALIZATION_PATH),
                "--generalization-check",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        payload = json.loads(completed.stdout)["generalization_check"]
        self.assertEqual(payload["case_count"], 7)
        self.assertEqual(payload["failed_case_count"], 0)


if __name__ == "__main__":
    unittest.main()
