"""Unit tests for the --creativity lever and semantic_policy numeric overrides."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "skills" / "photo-prompt-image-generator" / "scripts" / "prompt_generator.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("ppg_creativity", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load generator module: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CreativitySettingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_generator()

    def test_anchor_points_match_named_profiles(self) -> None:
        for value, profile, novelty in ((0.0, "conservative", "low"), (0.5, "balanced", "medium"), (1.0, "exploratory", "high")):
            derived = self.g.creativity_settings(value)
            self.assertEqual(derived["profile_label"], profile)
            self.assertEqual(derived["novelty_label"], novelty)
            expected_config = self.g.SEMANTIC_PROFILE_CONFIGS[profile]
            for key, expected in expected_config.items():
                self.assertAlmostEqual(
                    float(derived["profile_config"][key]), float(expected), places=6,
                    msg=f"creativity={value} key={key}",
                )
            expected_novelty = self.g.NOVELTY_SETTINGS_DEFAULTS[novelty]
            self.assertAlmostEqual(derived["novelty_settings"][0], expected_novelty[0], places=6)
            self.assertAlmostEqual(derived["novelty_settings"][1], expected_novelty[1], places=6)

    def test_interpolation_is_monotonic(self) -> None:
        values = [self.g.creativity_settings(c) for c in (0.0, 0.25, 0.5, 0.75, 1.0)]
        temperatures = [v["novelty_settings"][0] for v in values]
        windows = [v["profile_config"]["preset_window"] for v in values]
        self.assertEqual(temperatures, sorted(temperatures, reverse=True))
        self.assertEqual(windows, sorted(windows))

    def test_candidate_limits_stay_integers(self) -> None:
        derived = self.g.creativity_settings(0.3)
        self.assertIsInstance(derived["profile_config"]["preset_candidate_limit"], int)
        self.assertIsInstance(derived["profile_config"]["slot_candidate_limit"], int)

    def test_out_of_range_values_are_clamped(self) -> None:
        low = self.g.creativity_settings(-1.0)
        high = self.g.creativity_settings(5.0)
        self.assertEqual(low["profile_label"], "conservative")
        self.assertEqual(high["profile_label"], "exploratory")

    def test_creativity_override_takes_precedence_in_lookups(self) -> None:
        source = {
            "creativity_overrides": {
                "novelty_settings": (0.9, 0.3),
                "profile_config": {"preset_window": 0.2, "temperature_multiplier": 0.9},
            }
        }
        self.assertEqual(self.g.novelty_settings("low", source), (0.9, 0.3))
        config = self.g.semantic_profile_config("conservative", source)
        self.assertEqual(config["preset_window"], 0.2)


class SemanticPolicyOverrideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_generator()

    def test_profile_config_policy_overlay(self) -> None:
        source = {"semantic_policy": {"profiles": {"balanced": {"preset_window": 0.5}}}}
        config = self.g.semantic_profile_config("balanced", source)
        self.assertEqual(config["preset_window"], 0.5)
        # Untouched keys keep code defaults.
        self.assertEqual(
            config["temperature_multiplier"],
            self.g.SEMANTIC_PROFILE_CONFIGS["balanced"]["temperature_multiplier"],
        )
        # Other profiles are unaffected.
        self.assertEqual(
            self.g.semantic_profile_config("conservative", source)["preset_window"],
            self.g.SEMANTIC_PROFILE_CONFIGS["conservative"]["preset_window"],
        )

    def test_novelty_settings_policy_overlay(self) -> None:
        source = {"semantic_policy": {"novelty": {"high": {"temperature": 0.5}}}}
        temperature, scale = self.g.novelty_settings("high", source)
        self.assertEqual(temperature, 0.5)
        self.assertEqual(scale, self.g.NOVELTY_SETTINGS_DEFAULTS["high"][1])

    def test_batch_diversity_policy_overlay_merges_scope_weights(self) -> None:
        source = {
            "semantic_policy": {
                "batch_diversity": {
                    "medium": {"exact_decay": 0.5, "scope_weights": {"mood": 0.9}}
                }
            }
        }
        config = self.g.batch_diversity_config("medium", source)
        self.assertEqual(config["exact_decay"], 0.5)
        self.assertEqual(config["scope_weights"]["mood"], 0.9)
        self.assertEqual(
            config["scope_weights"]["preset"],
            self.g.BATCH_DIVERSITY_CONFIGS["medium"]["scope_weights"]["preset"],
        )

    def test_soft_anchor_weight_multipliers_policy_override(self) -> None:
        default = self.g.soft_anchor_weight_multipliers(None)
        self.assertEqual(
            default,
            (
                self.g.SOFT_ANCHOR_WEIGHT_MULTIPLIER,
                self.g.SOFT_ANCHOR_PROMOTED_WEIGHT_MULTIPLIER,
                self.g.SOFT_ANCHOR_CRITICAL_WEIGHT_MULTIPLIER,
                self.g.SOFT_ANCHOR_PRIMARY_WEIGHT_MULTIPLIER,
            ),
        )
        source = {"semantic_policy": {"soft_anchor_weights": {"critical": 80}}}
        self.assertEqual(self.g.soft_anchor_weight_multipliers(source)[2], 80.0)

    def test_make_batch_context_uses_creativity_config(self) -> None:
        context = self.g.make_batch_context("semantic", "medium", 4, creativity=1.0)
        self.assertIsNotNone(context)
        self.assertEqual(
            context["config"]["exact_decay"],
            self.g.BATCH_DIVERSITY_CONFIGS["high"]["exact_decay"],
        )
        default_context = self.g.make_batch_context("semantic", "medium", 4)
        self.assertEqual(
            default_context["config"]["exact_decay"],
            self.g.BATCH_DIVERSITY_CONFIGS["medium"]["exact_decay"],
        )


if __name__ == "__main__":
    unittest.main()
