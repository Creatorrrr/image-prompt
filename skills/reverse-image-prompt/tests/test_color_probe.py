#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
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
    RegionSpec,
    analyze_image,
    compare_reports,
    parse_region,
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

    def test_comparison_requires_matching_region_names(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "solid.png"
            Image.new("RGB", (16, 16), (128, 128, 128)).save(path)
            source = analyze_image(path, [RegionSpec("one", (0, 0, 1, 1))])
            target = analyze_image(path, [RegionSpec("two", (0, 0, 1, 1))])
        with self.assertRaisesRegex(ValueError, "matching region names"):
            compare_reports(source, target)


if __name__ == "__main__":
    unittest.main()
