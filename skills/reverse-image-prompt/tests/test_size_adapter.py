#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from size_adapter import is_valid_size, recommend_size  # noqa: E402


class SizeAdapterTests(unittest.TestCase):
    def test_keeps_valid_size(self) -> None:
        self.assertEqual(recommend_size(1024, 1536), (1024, 1536))

    def test_adjusts_non_multiple_source_nearby(self) -> None:
        width, height = recommend_size(748, 1280)
        self.assertTrue(is_valid_size(width, height))
        self.assertLess(abs((width / height) / (748 / 1280) - 1), 0.01)

    def test_upscales_tiny_source_into_allowed_pixel_range(self) -> None:
        width, height = recommend_size(200, 300)
        self.assertTrue(is_valid_size(width, height))

    def test_rejects_invalid_source(self) -> None:
        with self.assertRaises(ValueError):
            recommend_size(0, 100)


if __name__ == "__main__":
    unittest.main()
