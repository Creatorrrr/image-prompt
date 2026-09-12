"""Unit tests for opt-in semantic anchor-pool expansion."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
GENERATOR_PATH = SKILL_DIR / "scripts" / "prompt_generator.py"
WRAPPER_PATH = SKILL_DIR / "scripts" / "generate_photo_prompt.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_index(vectors: dict[str, list[float]]) -> dict:
    return {"entries": {key: {"vector": vector} for key, vector in vectors.items()}}


class AnchorExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_module("ppg_anchor_expansion", GENERATOR_PATH)

    def make_fixture(self, expansion: dict):
        data = {
            "slots": {
                "location": [
                    {"id": "castle"},
                    {"id": "palace"},
                    {"id": "fortress"},
                    {"id": "beach"},
                ]
            }
        }
        # castle is nearly parallel to palace and fortress, orthogonal to beach.
        vectors = {
            "slot:location:castle": [1.0, 0.0],
            "slot:location:palace": [0.99, 0.14],
            "slot:location:fortress": [0.95, 0.31],
            "slot:location:beach": [0.0, 1.0],
        }
        policy = {
            "enabled": True,
            "anchor_expansion": expansion,
            "anchors": [
                {"slot": "location", "ids": ["castle"], "pool": ["castle"], "critical": False}
            ],
        }
        contract = {"soft_anchor_policy": policy, "events": {}}
        context = {"index": make_index(vectors), "creativity": None}
        return data, policy, contract, context

    def test_disabled_config_is_noop(self) -> None:
        data, policy, contract, context = self.make_fixture({"enabled": False})
        self.g.expand_soft_anchor_pools(contract, context, data)
        self.assertEqual(policy["anchors"][0]["pool"], ["castle"])

    def test_expansion_adds_similar_neighbors_with_reduced_weight(self) -> None:
        data, policy, contract, context = self.make_fixture(
            {"enabled": True, "top_k": 2, "min_similarity": 0.9, "weight_ratio": 0.5}
        )
        self.g.expand_soft_anchor_pools(contract, context, data)
        anchor = policy["anchors"][0]
        self.assertIn("palace", anchor["pool"])
        self.assertIn("fortress", anchor["pool"])
        self.assertNotIn("beach", anchor["pool"])
        self.assertEqual(anchor["pool_weights"]["palace"], 0.5)
        self.assertEqual(anchor["pool_weights"]["fortress"], 0.5)
        self.assertNotIn("castle", anchor["pool_weights"])

    def test_min_similarity_filters_neighbors(self) -> None:
        data, policy, contract, context = self.make_fixture(
            {"enabled": True, "top_k": 3, "min_similarity": 0.98, "weight_ratio": 0.5}
        )
        self.g.expand_soft_anchor_pools(contract, context, data)
        anchor = policy["anchors"][0]
        self.assertIn("palace", anchor["pool"])
        self.assertNotIn("fortress", anchor["pool"])

    def test_critical_anchor_is_never_expanded(self) -> None:
        data, policy, contract, context = self.make_fixture(
            {"enabled": True, "top_k": 2, "min_similarity": 0.9, "weight_ratio": 0.5}
        )
        policy["anchors"][0]["critical"] = True
        self.g.expand_soft_anchor_pools(contract, context, data)
        self.assertEqual(policy["anchors"][0]["pool"], ["castle"])

    def test_rule_mode_without_context_is_noop(self) -> None:
        data, policy, contract, _context = self.make_fixture(
            {"enabled": True, "top_k": 2, "min_similarity": 0.9}
        )
        self.g.expand_soft_anchor_pools(contract, None, data)
        self.assertEqual(policy["anchors"][0]["pool"], ["castle"])

    def test_creativity_relaxes_similarity_floor(self) -> None:
        settings_low = self.g.anchor_expansion_settings(
            {"anchor_expansion": {"enabled": True, "top_k": 3, "min_similarity": 0.8}},
            {"creativity": 0.0},
        )
        settings_high = self.g.anchor_expansion_settings(
            {"anchor_expansion": {"enabled": True, "top_k": 3, "min_similarity": 0.8}},
            {"creativity": 1.0},
        )
        self.assertLess(settings_high["min_similarity"], settings_low["min_similarity"])
        self.assertEqual(settings_high["top_k"], 4)
        self.assertEqual(settings_low["top_k"], 3)


class AnchorExpansionWrapperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wrapper = load_module("ppg_wrapper_expansion", WRAPPER_PATH)

    def test_recipe_override_wins_over_defaults(self) -> None:
        recipes = {
            "soft_anchor_defaults": {
                "anchor_expansion": {"enabled": False, "top_k": 3, "min_similarity": 0.78}
            }
        }
        applied = [{"anchor_expansion": {"enabled": True, "top_k": 5}}]
        merged = self.wrapper.anchor_expansion_config(recipes, applied)
        self.assertTrue(merged["enabled"])
        self.assertEqual(merged["top_k"], 5)
        self.assertEqual(merged["min_similarity"], 0.78)

    def test_spec_includes_expansion_config(self) -> None:
        spec = self.wrapper.build_soft_anchor_spec(
            [
                {
                    "slot": "location",
                    "ids": ["castle"],
                    "pool": ["castle"],
                    "terms": ["castle"],
                    "source": "role",
                }
            ],
            [1],
            "test",
            {"enabled": True, "top_k": 2},
        )
        self.assertEqual(spec["anchor_expansion"], {"enabled": True, "top_k": 2})


if __name__ == "__main__":
    unittest.main()
