#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from color_fidelity_eval import evaluate_report  # noqa: E402


def group(name: str, role: str, lab: list[float]) -> dict:
    return {
        "name": name,
        "region_names": [f"{name}-a", f"{name}-b"],
        "semantic_role": role,
        "tone_zone": "midtone" if role == "target" else "flat",
        "purpose": (
            "intrinsic-displayed-color"
            if role == "target"
            else "global-cast-and-exposure"
        ),
        "equal_region_median": {
            "lab_d65": lab,
            "chroma": (lab[1] ** 2 + lab[2] ** 2) ** 0.5,
            "hue_degrees": 0.0,
        },
        "region_median_ranges": {
            "lightness": [lab[0], lab[0]],
            "a": [lab[1], lab[1]],
            "b": [lab[2], lab[2]],
            "chroma": [0.0, 0.0],
        },
    }


def report(
    source_target: list[float],
    render_target: list[float],
    source_context: list[float],
    render_context: list[float],
) -> dict:
    return {
        "status": "ok",
        "comparison_context": {"scope": "assumed-display-space-relative"},
        "source": {
            "groups": [
                group("target", "target", source_target),
                group("context", "context", source_context),
            ]
        },
        "comparison": {
            "groups": [
                group("target", "target", render_target),
                group("context", "context", render_context),
            ]
        },
    }


POLICY = {
    "target": {
        "max_abs_delta_l": 4.0,
        "max_abs_delta_c": 4.0,
        "max_abs_hue_degrees": 12.0,
        "max_delta_e2000": 6.0,
    },
    "context": {"max_abs_delta_l": 3.0, "max_opponent_shift": 3.0},
}


class ColorFidelityEvalTests(unittest.TestCase):
    def test_identical_groups_pass(self) -> None:
        payload = report([80, 10, 10], [80, 10, 10], [40, 0, 0], [40, 0, 0])
        result = evaluate_report(payload, POLICY)
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["drift_class"], "within-policy")

    def test_target_only_shift_is_local(self) -> None:
        payload = report([80, 10, 10], [68, 16, 22], [40, 0, 0], [41, 1, 1])
        result = evaluate_report(payload, POLICY)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["drift_class"], "target-local")
        self.assertEqual(result["dominant_residual_axis"], "value")

    def test_shared_lightness_shift_is_global_exposure(self) -> None:
        payload = report([80, 10, 10], [70, 10, 10], [40, 0, 0], [30, 0, 0])
        result = evaluate_report(payload, POLICY)
        self.assertEqual(result["status"], "fail")
        self.assertEqual(result["drift_class"], "global-exposure")
        local = result["target_groups"][0]["context_corrected_local_residual"]
        self.assertEqual(local["abs_delta_l"], 0.0)

    def test_dominant_axis_uses_all_target_groups(self) -> None:
        payload = report([80, 10, 10], [80, 10, 10], [40, 0, 0], [40, 0, 0])
        payload["source"]["groups"].append(group("target-2", "target", [60, 5, 5]))
        payload["comparison"]["groups"].append(
            group("target-2", "target", [60, 20, 20])
        )
        result = evaluate_report(payload, POLICY)
        self.assertEqual(result["dominant_residual_axis"], "chroma")

    def test_without_policy_result_is_unscored(self) -> None:
        payload = report([80, 10, 10], [60, 20, 20], [40, 0, 0], [40, 0, 0])
        result = evaluate_report(payload)
        self.assertEqual(result["status"], "unscored")
        self.assertEqual(result["drift_class"], "inconclusive")

    def test_policy_requires_positive_tolerances(self) -> None:
        payload = report([80, 10, 10], [80, 10, 10], [40, 0, 0], [40, 0, 0])
        with self.assertRaisesRegex(ValueError, "positive number"):
            evaluate_report(payload, {"target": {"max_abs_delta_l": 0}})


if __name__ == "__main__":
    unittest.main()
