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
        self.assertEqual({region.name for region in source}, {"major-plane-a", "supporting-field"})
        self.assertNotEqual(source[0].bounds, comparison[0].bounds)
        self.assertEqual(relations[0].name, "plane-to-field")
        self.assertEqual(profiles[0].samples, 64)
        self.assertNotEqual(profiles[0].line, comparison_profiles[0].line)

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


if __name__ == "__main__":
    unittest.main()
