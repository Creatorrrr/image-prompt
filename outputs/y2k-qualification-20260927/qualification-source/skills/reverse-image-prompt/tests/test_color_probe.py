#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import json
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

from color_probe import (  # noqa: E402
    GroupSpec,
    RegionSpec,
    analyze_image,
    compare_group_reports,
    compare_reports,
    comparison_context,
    delta_e2000,
    load_sampling_spec,
    parse_group,
    parse_region,
    summarize_groups,
)


@unittest.skipIf(Image is None, "Pillow is required for color probe tests")
class ColorProbeTests(unittest.TestCase):
    def test_region_parser_accepts_normalized_bounds(self) -> None:
        self.assertEqual(
            parse_region("field=0.1,0.2,0.8,0.9"),
            RegionSpec("field", (0.1, 0.2, 0.8, 0.9)),
        )

    def test_region_parser_rejects_out_of_range_bounds(self) -> None:
        with self.assertRaisesRegex(ValueError, "0 <= x0"):
            parse_region("field=-0.1,0,1,1")

    def test_group_parser_requires_two_unique_regions(self) -> None:
        self.assertEqual(
            parse_group("target=patch-a,patch-b"),
            GroupSpec("target", ("patch-a", "patch-b")),
        )
        with self.assertRaisesRegex(ValueError, "at least two"):
            parse_group("target=patch-a")
        with self.assertRaisesRegex(ValueError, "must be unique"):
            parse_group("target=patch-a,patch-a")

    def test_solid_region_reports_stable_median_and_missing_profile(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "solid.png"
            Image.new("RGB", (32, 24), (200, 150, 100)).save(path)
            report = analyze_image(
                path,
                [RegionSpec("field", (0.0, 0.0, 1.0, 1.0))],
            )
        self.assertEqual(report["profile_status"], "missing-profile-assumed-srgb")
        self.assertEqual(report["regions"][0]["median"]["srgb"], [200.0, 150.0, 100.0])
        self.assertEqual(report["regions"][0]["iqr"]["lightness"], 0.0)

    def test_comparison_reports_source_relative_value_and_chroma_shift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "source.png"
            target_path = Path(temp_dir) / "target.png"
            Image.new("RGB", (20, 20), (200, 180, 170)).save(source_path)
            Image.new("RGB", (20, 20), (180, 120, 70)).save(target_path)
            region = [RegionSpec("field", (0.0, 0.0, 1.0, 1.0))]
            source = analyze_image(source_path, region)
            target = analyze_image(target_path, region)
            delta = compare_reports(source, target)[0]["target_minus_source"]
        self.assertLess(delta["lab_d65"][0], 0.0)
        self.assertGreater(delta["chroma"], 0.0)
        self.assertGreater(delta["delta_e76"], 0.0)
        self.assertGreater(delta["delta_e2000"], 0.0)

    def test_delta_e2000_matches_published_reference_pair(self) -> None:
        self.assertAlmostEqual(
            delta_e2000((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485)),
            2.0425,
            places=4,
        )

    def test_comparison_requires_matching_region_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "solid.png"
            Image.new("RGB", (16, 16), (128, 128, 128)).save(path)
            source = analyze_image(path, [RegionSpec("one", (0, 0, 1, 1))])
            target = analyze_image(path, [RegionSpec("two", (0, 0, 1, 1))])
        with self.assertRaisesRegex(ValueError, "matching region names"):
            compare_reports(source, target)

    def test_group_summary_equal_weights_region_medians(self) -> None:
        report = {
            "regions": [
                {
                    "name": "large",
                    "sample_count": 10000,
                    "median": {
                        "lab_d65": [20.0, 10.0, 0.0],
                        "chroma": 10.0,
                        "hue_degrees": 0.0,
                    },
                },
                {
                    "name": "small",
                    "sample_count": 10,
                    "median": {
                        "lab_d65": [80.0, 0.0, 10.0],
                        "chroma": 10.0,
                        "hue_degrees": 90.0,
                    },
                },
            ]
        }
        summary = summarize_groups(
            report, [GroupSpec("target", ("large", "small"))]
        )[0]
        self.assertEqual(summary["equal_region_median"]["lab_d65"], [50.0, 5.0, 5.0])
        self.assertEqual(summary["region_median_ranges"]["lightness"], [20.0, 80.0])

    def test_group_summary_rejects_unknown_region(self) -> None:
        report = {"regions": [{"name": "one", "median": {}}]}
        with self.assertRaisesRegex(ValueError, "unknown regions"):
            summarize_groups(report, [GroupSpec("target", ("one", "two"))])

    def test_group_comparison_and_profile_context_are_relative(self) -> None:
        source_groups = [
            {
                "name": "target",
                "region_names": ["a", "b"],
                "equal_region_median": {
                    "lab_d65": [70.0, 5.0, 5.0],
                    "chroma": 7.071,
                    "hue_degrees": 45.0,
                },
            }
        ]
        target_groups = [
            {
                "name": "target",
                "region_names": ["a", "b"],
                "equal_region_median": {
                    "lab_d65": [60.0, 10.0, 10.0],
                    "chroma": 14.142,
                    "hue_degrees": 45.0,
                },
            }
        ]
        delta = compare_group_reports(source_groups, target_groups)[0][
            "target_minus_source"
        ]
        self.assertEqual(delta["lab_d65"], [-10.0, 5.0, 5.0])
        self.assertGreater(delta["chroma"], 0.0)
        context = comparison_context(
            {"profile_status": "missing-profile-assumed-srgb"},
            {"profile_status": "embedded-profile-converted-to-srgb"},
        )
        self.assertEqual(context["scope"], "assumed-display-space-relative")

    def test_sampling_spec_keeps_independent_bounds_and_tone_zone_metadata(self) -> None:
        payload = {
            "regions": [
                {
                    "name": "target-a",
                    "source_bounds": [0.1, 0.1, 0.2, 0.2],
                    "comparison_bounds": [0.2, 0.1, 0.3, 0.2],
                    "semantic_role": "target",
                    "tone_zone": "midtone",
                    "purpose": "intrinsic-displayed-color",
                },
                {
                    "name": "target-b",
                    "source_bounds": [0.3, 0.1, 0.4, 0.2],
                    "comparison_bounds": [0.4, 0.1, 0.5, 0.2],
                    "semantic_role": "target",
                    "tone_zone": "midtone",
                    "purpose": "intrinsic-displayed-color",
                },
            ],
            "groups": [
                {
                    "name": "target",
                    "region_names": ["target-a", "target-b"],
                    "semantic_role": "target",
                    "tone_zone": "midtone",
                    "purpose": "intrinsic-displayed-color",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sampling.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            source, comparison, groups = load_sampling_spec(path)
        self.assertNotEqual(source[0].bounds, comparison[0].bounds)
        self.assertEqual(source[0].tone_zone, "midtone")
        self.assertEqual(groups[0].semantic_role, "target")

    def test_sampling_spec_rejects_mixed_intrinsic_group(self) -> None:
        payload = {
            "regions": [
                {
                    "name": "mixed-a",
                    "source_bounds": [0.1, 0.1, 0.2, 0.2],
                    "semantic_role": "target",
                    "tone_zone": "mixed",
                    "purpose": "intrinsic-displayed-color",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sampling.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "midtone or flat"):
                load_sampling_spec(path)

    def test_documented_sampling_spec_is_valid(self) -> None:
        reference = (
            Path(__file__).resolve().parents[1]
            / "references"
            / "color-reproduction-evaluation.md"
        ).read_text(encoding="utf-8")
        match = re.search(r"```json\n(.*?)\n```", reference, re.DOTALL)
        self.assertIsNotNone(match)
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sampling.json"
            path.write_text(match.group(1), encoding="utf-8")
            source, comparison, groups = load_sampling_spec(path)
        self.assertEqual(len(source), 4)
        self.assertEqual(len(comparison), 4)
        self.assertEqual({group.name for group in groups}, {"target-midtone", "context"})


if __name__ == "__main__":
    unittest.main()
