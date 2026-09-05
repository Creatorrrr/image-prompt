#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import tempfile
import unittest

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional diagnostic dependency.
    Image = None

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from light_probe import (  # noqa: E402
    analyze_light,
    compare_light_reports,
    load_metric_policy,
    load_spec,
)


@unittest.skipIf(Image is None, "Pillow is required for lighting probe tests")
class LightProbeTests(unittest.TestCase):
    def test_documented_sampling_spec_is_valid(self) -> None:
        reference = (
            Path(__file__).resolve().parents[1]
            / "references"
            / "lighting-reproduction-evaluation.md"
        ).read_text(encoding="utf-8")
        match = re.search(r"```json\n(.*?)\n```", reference, re.DOTALL)
        self.assertIsNotNone(match)
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sampling.json"
            path.write_text(match.group(1), encoding="utf-8")
            source, comparison, relations, profiles, comparison_profiles = load_spec(path)
            metric_policy = load_metric_policy(path)
        self.assertEqual({region.name for region in source}, {"major-plane-a", "supporting-field"})
        self.assertNotEqual(source[0].bounds, comparison[0].bounds)
        self.assertEqual(relations[0].name, "plane-to-field")
        self.assertEqual(profiles[0].samples, 64)
        self.assertNotEqual(profiles[0].line, comparison_profiles[0].line)
        self.assertIsNotNone(metric_policy.bright_plateau_delta_l)

    def test_monotonic_gradient_reports_profile_without_inferring_direction(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            image_path = Path(temp_dir) / "gradient.png"
            image = Image.new("RGB", (128, 24))
            for x in range(image.width):
                value = round(30 + 200 * x / (image.width - 1))
                for y in range(image.height):
                    image.putpixel((x, y), (value, value, value))
            image.save(image_path)
            spec_path = Path(temp_dir) / "spec.json"
            spec_path.write_text(
                json.dumps(
                    {
                        "profiles": [
                            {
                                "name": "gradient",
                                "source_line": [0.0, 0.5, 1.0, 0.5],
                                "samples": 64,
                                "width_px": 3,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            _, _, relations, profiles, _ = load_spec(spec_path)
            report = analyze_light(image_path, [], relations, profiles)
        lightness = report["profiles"][0]["lightness"]
        self.assertGreater(lightness["net_change"], 50.0)
        self.assertGreater(lightness["monotonicity"], 0.95)
        self.assertIsNotNone(lightness["transition_width_fraction_10_90"])

    def test_region_relation_comparison_stays_diagnostic_and_relative(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "source.png"
            target_path = Path(temp_dir) / "target.png"
            source = Image.new("RGB", (40, 20), (0, 0, 0))
            target = Image.new("RGB", (40, 20), (0, 0, 0))
            for x in range(40):
                source_value = 210 if x < 20 else 90
                target_value = 180 if x < 20 else 120
                for y in range(20):
                    source.putpixel((x, y), (source_value,) * 3)
                    target.putpixel((x, y), (target_value,) * 3)
            source.save(source_path)
            target.save(target_path)
            spec_path = Path(temp_dir) / "spec.json"
            spec_path.write_text(
                json.dumps(
                    {
                        "regions": [
                            {"name": "left", "source_bounds": [0, 0, 0.5, 1]},
                            {"name": "right", "source_bounds": [0.5, 0, 1, 1]},
                        ],
                        "relations": [
                            {
                                "name": "left-to-right",
                                "left_region": "left",
                                "right_region": "right",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            source_regions, comparison_regions, relations, profiles, comparison_profiles = load_spec(spec_path)
            source_report = analyze_light(source_path, source_regions, relations, profiles)
            target_report = analyze_light(target_path, comparison_regions, relations, comparison_profiles)
            delta = compare_light_reports(source_report, target_report)
        self.assertEqual(delta["evaluation_status"], "diagnostic-unscored")
        self.assertLess(delta["relations"][0]["target_minus_source"], 0.0)

    def test_relation_rejects_unknown_region(self) -> None:
        payload = {
            "regions": [
                {"name": "known", "source_bounds": [0, 0, 1, 1]}
            ],
            "relations": [
                {
                    "name": "invalid",
                    "left_region": "known",
                    "right_region": "missing",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "spec.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown regions"):
                load_spec(path)

    def test_region_metrics_separate_key_level_from_local_range(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "source.png"
            target_path = Path(temp_dir) / "target.png"
            source = Image.new("RGB", (100, 20))
            target = Image.new("RGB", (100, 20))
            for x in range(100):
                source_value = 60 + round(100 * x / 99)
                target_value = min(255, source_value + 35)
                for y in range(20):
                    source.putpixel((x, y), (source_value,) * 3)
                    target.putpixel((x, y), (target_value,) * 3)
            source.save(source_path)
            target.save(target_path)
            spec_path = Path(temp_dir) / "spec.json"
            spec_path.write_text(
                json.dumps(
                    {
                        "regions": [
                            {
                                "name": "plane",
                                "role": "major-plane",
                                "source_bounds": [0, 0, 1, 1],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            source_regions, target_regions, relations, profiles, target_profiles = load_spec(spec_path)
            source_report = analyze_light(source_path, source_regions, relations, profiles)
            target_report = analyze_light(target_path, target_regions, relations, target_profiles)
            delta = compare_light_reports(source_report, target_report)["regions"][0]["metric_deltas"]
        self.assertGreater(delta["high_side_p90"], 10.0)
        self.assertLess(abs(delta["robust_range_p90_p10"]), 5.0)

    def test_bright_plane_coverage_and_shadow_floor_are_independent_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            broad_path = Path(temp_dir) / "broad.png"
            narrow_path = Path(temp_dir) / "narrow.png"
            broad = Image.new("RGB", (100, 20), (70, 70, 70))
            narrow = Image.new("RGB", (100, 20), (70, 70, 70))
            for x in range(80):
                for y in range(20):
                    broad.putpixel((x, y), (220, 220, 220))
            for x in range(20):
                for y in range(20):
                    narrow.putpixel((x, y), (220, 220, 220))
            broad.save(broad_path)
            narrow.save(narrow_path)
            spec_path = Path(temp_dir) / "spec.json"
            spec_path.write_text(
                json.dumps(
                    {
                        "metrics_policy": {"bright_plateau_delta_l": 4.0},
                        "regions": [
                            {
                                "name": "plane",
                                "role": "major-plane",
                                "source_bounds": [0, 0, 1, 1],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            source_regions, target_regions, relations, profiles, target_profiles = load_spec(spec_path)
            policy = load_metric_policy(spec_path)
            broad_report = analyze_light(broad_path, source_regions, relations, profiles, policy)
            narrow_report = analyze_light(narrow_path, target_regions, relations, target_profiles, policy)
            broad_region = broad_report["regions"][0]
            narrow_region = narrow_report["regions"][0]
        self.assertGreater(broad_region["bright_plateau_fraction"], narrow_region["bright_plateau_fraction"])
        self.assertAlmostEqual(broad_region["shadow_floor_p10"], narrow_region["shadow_floor_p10"], delta=0.5)

    def test_local_neighbor_metric_separates_microcontrast_from_region_range(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            smooth_path = Path(temp_dir) / "smooth.png"
            alternating_path = Path(temp_dir) / "alternating.png"
            smooth = Image.new("RGB", (100, 40))
            alternating = Image.new("RGB", (100, 40))
            for x in range(100):
                for y in range(40):
                    smooth_value = 80 if x < 50 else 160
                    alternating_value = 80 if (x + y) % 2 == 0 else 160
                    smooth.putpixel((x, y), (smooth_value,) * 3)
                    alternating.putpixel((x, y), (alternating_value,) * 3)
            smooth.save(smooth_path)
            alternating.save(alternating_path)
            spec_path = Path(temp_dir) / "spec.json"
            spec_path.write_text(
                json.dumps(
                    {
                        "regions": [
                            {
                                "name": "plane",
                                "role": "major-plane",
                                "source_bounds": [0, 0, 1, 1],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            regions, comparison_regions, relations, profiles, comparison_profiles = load_spec(spec_path)
            smooth_region = analyze_light(smooth_path, regions, relations, profiles)["regions"][0]
            alternating_region = analyze_light(
                alternating_path,
                comparison_regions,
                relations,
                comparison_profiles,
            )["regions"][0]
        self.assertAlmostEqual(
            smooth_region["within_region_iqr"],
            alternating_region["within_region_iqr"],
            delta=0.5,
        )
        self.assertGreater(
            alternating_region["local_neighbor_difference_p90"],
            smooth_region["local_neighbor_difference_p90"] + 10.0,
        )


if __name__ == "__main__":
    unittest.main()
