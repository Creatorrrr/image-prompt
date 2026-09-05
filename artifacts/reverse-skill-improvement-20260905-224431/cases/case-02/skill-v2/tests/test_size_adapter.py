#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import sys
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from size_adapter import is_valid_size, recommend_size, result_payload  # noqa: E402


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

    def test_explicitly_applied_exact_target_passes_frame_delivery(self) -> None:
        target_width, target_height = recommend_size(1111, 777)
        payload = result_payload(
            1111,
            777,
            binding_status="explicitly-applied",
            delivered_width=target_width,
            delivered_height=target_height,
        )
        evidence = payload["size_binding"]
        self.assertEqual(evidence["frame_delivery_status"], "pass")
        self.assertTrue(evidence["exact_target_match"])

    def test_explicitly_applied_mismatched_delivery_fails_without_tolerance(self) -> None:
        payload = result_payload(
            900,
            1400,
            binding_status="explicitly-applied",
            delivered_width=1024,
            delivered_height=1536,
        )
        evidence = payload["size_binding"]
        self.assertEqual(evidence["frame_delivery_status"], "fail")
        self.assertFalse(evidence["exact_target_match"])

    def test_unbound_delivery_is_unscored_with_continuous_ratio_errors(self) -> None:
        payload = result_payload(
            969,
            1280,
            binding_status="unbound",
            delivered_width=927,
            delivered_height=1697,
        )
        evidence = payload["size_binding"]
        self.assertEqual(evidence["frame_delivery_status"], "unscored")
        self.assertEqual(evidence["tool_support"], "unverified")
        self.assertGreater(evidence["source_to_delivery_relative_ratio_error"], 0)
        self.assertGreater(evidence["target_to_delivery_relative_ratio_error"], 0)

    def test_auto_or_unsupported_size_never_claims_bound_frame_delivery(self) -> None:
        auto = result_payload(913, 1207, binding_status="auto")
        unsupported = result_payload(1200, 800, binding_status="unsupported")
        self.assertEqual(auto["size_binding"]["frame_delivery_status"], "unscored")
        self.assertEqual(
            unsupported["size_binding"]["frame_delivery_status"], "unscored"
        )

    def test_delivery_dimensions_must_be_supplied_as_a_pair(self) -> None:
        with self.assertRaises(ValueError):
            result_payload(
                640,
                960,
                binding_status="unbound",
                delivered_width=768,
            )


if __name__ == "__main__":
    unittest.main()
