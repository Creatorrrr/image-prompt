from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_iteration_record.py"
SPEC = importlib.util.spec_from_file_location("validate_iteration_record", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def valid_record() -> dict:
    return {
        "schema_version": "image-prompt-skill-improvement/v1",
        "target": {
            "skill_path": "skills/example-image-prompt",
            "baseline_revision": "baseline-snapshot",
            "candidate_revision": "working-tree",
        },
        "goal": {
            "claim_scope": "render-fidelity",
            "request": "Improve source-relative visual fidelity without case-specific defaults.",
        },
        "evidence": [
            {
                "id": "e-source",
                "kind": "source-observation",
                "claim": "The primary relation remains stable across minor placement changes.",
                "artifact": "source-artifact",
            },
            {
                "id": "e-render",
                "kind": "render-observation",
                "claim": "The candidate render preserves the primary relation.",
                "artifact": "candidate-render",
            },
            {
                "id": "e-prompt",
                "kind": "prompt-evaluation",
                "claim": "A held-out prompt expresses the invariant without locking placement.",
                "artifact": "prompt-evaluation-report",
            },
            {
                "id": "e-package",
                "kind": "package-check",
                "claim": "Skill validation and focused tests pass.",
                "artifact": "test-command-output",
            },
        ],
        "perceptual_contract": {
            "primary_success_condition": "Preserve the primary relation while allowing incidental placement to vary.",
            "user_appeal": None,
            "invariants": [
                {
                    "id": "inv-relation",
                    "statement": "The primary relation remains first in the visual hierarchy.",
                    "evidence_ids": ["e-source"],
                    "causal_controls": ["relation ownership", "attention hierarchy"],
                }
            ],
            "flexible_dimensions": ["minor placement"],
        },
        "mismatches": [
            {
                "id": "m-priority",
                "scale": "global",
                "axis": "hierarchy",
                "source_state": "the relation is primary",
                "render_state": "inventory detail competes with the relation",
                "evidence_ids": ["e-source", "e-render"],
            }
        ],
        "hypotheses": [
            {
                "id": "h-owner",
                "stage": "representation",
                "statement": "The target skill lacks one owner for the primary relation.",
                "evidence_ids": ["e-source", "e-prompt"],
                "falsifier": "The baseline already assigns one owner and gives it primary prompt salience.",
            }
        ],
        "intervention": {
            "status": "implemented",
            "target_layers": ["module", "test"],
            "general_rule": "Assign each primary invariant one owner before emitting local inventory.",
            "generalization_basis": "Ownership and hierarchy apply across subjects and media.",
            "hypothesis_ids": ["h-owner"],
            "changed_paths": ["skills/example-image-prompt/modules/core.md"],
            "case_specific_runtime_defaults": [],
        },
        "evaluation": {
            "package": {"status": "pass", "evidence_ids": ["e-package"]},
            "prompt": {"status": "pass", "evidence_ids": ["e-prompt"]},
            "render": {"status": "pass", "evidence_ids": ["e-render"]},
            "user": {"status": "unscored", "evidence_ids": []},
            "holdouts": [
                {
                    "id": "holdout-unrelated",
                    "case_role": "held-out",
                    "status": "pass",
                    "covered_axes": ["relationship", "hierarchy"],
                    "evidence_ids": ["e-prompt", "e-render"],
                }
            ],
        },
        "decision": {
            "status": "promote",
            "claim_scope": "render-fidelity",
            "rationale": "The targeted behavior passed prompt and render holdouts under matched conditions.",
            "evidence_ids": ["e-package", "e-prompt", "e-render"],
        },
    }


class ValidateIterationRecordTests(unittest.TestCase):
    def test_cli_accepts_valid_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            record_path = Path(directory) / "iteration.json"
            record_path.write_text(json.dumps(valid_record()), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(record_path)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "ok")

    def test_valid_render_fidelity_promotion(self) -> None:
        self.assertEqual(MODULE.validate_record(valid_record()), [])

    def test_promotion_requires_render_pixels_for_render_claim(self) -> None:
        record = valid_record()
        record["evaluation"]["render"] = {"status": "blocked", "evidence_ids": []}
        errors = MODULE.validate_record(record)
        self.assertTrue(
            any("evaluation.render.status 'pass'" in error for error in errors)
        )

    def test_generation_outcome_cannot_prove_pixel_pass(self) -> None:
        record = valid_record()
        record["evidence"].append(
            {
                "id": "e-blocked",
                "kind": "generation-outcome",
                "claim": "The generator returned no image.",
                "artifact": "attempt-log",
            }
        )
        record["evaluation"]["render"] = {
            "status": "pass",
            "evidence_ids": ["e-blocked"],
        }
        errors = MODULE.validate_record(record)
        self.assertTrue(any("render-observation" in error for error in errors))

    def test_case_specific_runtime_defaults_are_rejected(self) -> None:
        record = valid_record()
        record["intervention"]["case_specific_runtime_defaults"] = [
            "one motivating image's desired value"
        ]
        errors = MODULE.validate_record(record)
        self.assertIn(
            "$.intervention.case_specific_runtime_defaults must remain empty",
            errors,
        )

    def test_unknown_evidence_reference_is_rejected(self) -> None:
        record = valid_record()
        record["hypotheses"][0]["evidence_ids"] = ["missing-evidence"]
        errors = MODULE.validate_record(record)
        self.assertTrue(
            any("unknown id 'missing-evidence'" in error for error in errors)
        )

    def test_prompt_promotion_requires_unrelated_holdout(self) -> None:
        record = valid_record()
        record["goal"]["claim_scope"] = "prompt-behavior"
        record["decision"]["claim_scope"] = "prompt-behavior"
        record["evaluation"]["holdouts"][0]["case_role"] = "motivating"
        errors = MODULE.validate_record(record)
        self.assertTrue(
            any("requires a passing held-out case" in error for error in errors)
        )

    def test_render_promotion_rejects_package_only_holdout(self) -> None:
        record = valid_record()
        record["evaluation"]["holdouts"][0]["evidence_ids"] = ["e-package"]
        errors = MODULE.validate_record(record)
        self.assertTrue(
            any("'render-observation' evidence" in error for error in errors)
        )

    def test_user_aesthetic_promotion_requires_user_judgment(self) -> None:
        record = valid_record()
        record["goal"]["claim_scope"] = "user-aesthetic"
        record["decision"]["claim_scope"] = "user-aesthetic"
        errors = MODULE.validate_record(record)
        self.assertTrue(
            any("evaluation.user.status 'pass'" in error for error in errors)
        )

    def test_user_appeal_requires_user_judgment_evidence(self) -> None:
        record = valid_record()
        record["perceptual_contract"]["user_appeal"] = "A direct stated preference."
        errors = MODULE.validate_record(record)
        self.assertTrue(any("user-judgment evidence" in error for error in errors))

    def test_empty_record_is_rejected(self) -> None:
        self.assertNotEqual(MODULE.validate_record({}), [])

    def test_external_hypothesis_accepts_generation_outcome(self) -> None:
        record = valid_record()
        record["decision"]["status"] = "blocked"
        record["evidence"].append(
            {
                "id": "e-outcome",
                "kind": "generation-outcome",
                "claim": "No image was delivered.",
                "artifact": "attempt-log",
            }
        )
        record["hypotheses"][0] = {
            "id": "h-external",
            "stage": "external",
            "statement": "The delivery failure prevents pixel evaluation.",
            "evidence_ids": ["e-outcome"],
            "falsifier": "A delivered image becomes available for inspection.",
        }
        record["intervention"] = {
            "status": "none",
            "target_layers": [],
            "general_rule": "Keep delivery outcomes separate from pixel judgments.",
            "generalization_basis": "The distinction applies to every generator route.",
            "hypothesis_ids": [],
            "changed_paths": [],
            "case_specific_runtime_defaults": [],
        }
        record["evaluation"]["render"] = {
            "status": "blocked",
            "evidence_ids": ["e-outcome"],
        }
        record["decision"]["evidence_ids"] = ["e-outcome"]
        self.assertEqual(MODULE.validate_record(record), [])


if __name__ == "__main__":
    unittest.main()
