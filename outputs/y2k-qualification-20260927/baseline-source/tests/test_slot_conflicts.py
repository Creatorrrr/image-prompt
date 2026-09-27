"""Unit tests for the declarative slot-conflict / slot-context-rule layer."""

from __future__ import annotations

import importlib.util
import json
import random
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
GENERATOR_PATH = SKILL_DIR / "scripts" / "prompt_generator.py"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("photo_prompt_generator_conflicts", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load generator module: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def make_source(slot_conflicts=None, slot_context_rules=None, builtin=None):
    rules = {}
    if slot_conflicts is not None:
        rules["slot_conflicts"] = slot_conflicts
    if slot_context_rules is not None:
        rules["slot_context_rules"] = slot_context_rules
    if builtin is not None:
        rules["builtin_slot_context_rules"] = builtin
    return {"coherence_rules": rules}


class SlotConflictRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()

    def test_hard_pair_conflict_blocks_candidate_by_id(self) -> None:
        source = make_source(
            slot_conflicts=[
                {
                    "id": "noon_vs_moonlight",
                    "left": {"slot": "time_of_day", "ids": ["harsh_noon_sun"]},
                    "right": {"slot": "lighting", "ids": ["moonlight"]},
                    "severity": "hard",
                }
            ]
        )
        picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "time_of_day": {"id": "harsh_noon_sun", "tags": []},
        }
        item = {"id": "moonlight", "tags": []}
        violations = self.generator.slot_conflict_violations("lighting", item, picked, source, "hard")
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["rule_id"], "noon_vs_moonlight")
        self.assertFalse(
            self.generator.compatible_with_slot_context("lighting", item, picked, source)
        )

    def test_hard_pair_conflict_is_bidirectional(self) -> None:
        # Same rule, but the lighting side is picked first and the
        # time_of_day side is the candidate: the rule must still bind.
        source = make_source(
            slot_conflicts=[
                {
                    "id": "noon_vs_moonlight",
                    "left": {"slot": "time_of_day", "ids": ["harsh_noon_sun"]},
                    "right": {"slot": "lighting", "ids": ["moonlight"]},
                    "severity": "hard",
                }
            ]
        )
        picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "lighting": {"id": "moonlight", "tags": []},
        }
        item = {"id": "harsh_noon_sun", "tags": []}
        violations = self.generator.slot_conflict_violations("time_of_day", item, picked, source, "hard")
        self.assertEqual(len(violations), 1)

    def test_facet_based_conflict(self) -> None:
        source = make_source(
            slot_conflicts=[
                {
                    "id": "day_vs_night_light",
                    "left": {"slot": "time_of_day", "facets": ["time_of_day:day"]},
                    "right": {"slot": "lighting", "facets": ["time_of_day:night"]},
                    "severity": "hard",
                }
            ]
        )
        picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "time_of_day": {"id": "noon_custom", "facets": {"time_of_day": ["day"]}},
        }
        night_item = {"id": "moon_custom", "facets": {"time_of_day": ["night"]}}
        day_item = {"id": "sun_custom", "facets": {"time_of_day": ["day"]}}
        self.assertTrue(
            self.generator.slot_conflict_violations("lighting", night_item, picked, source, "hard")
        )
        self.assertFalse(
            self.generator.slot_conflict_violations("lighting", day_item, picked, source, "hard")
        )

    def test_soft_conflict_penalizes_weight_without_blocking(self) -> None:
        source = make_source(
            slot_conflicts=[
                {
                    "id": "storm_vs_sun",
                    "left": {"slot": "weather", "ids": ["storm"]},
                    "right": {"slot": "lighting", "ids": ["sunny"]},
                    "severity": "soft",
                    "penalty": 0.2,
                }
            ]
        )
        picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "weather": {"id": "storm", "tags": []},
        }
        pool = [
            {"id": "sunny", "weight": 10},
            {"id": "lamp", "weight": 10},
        ]
        adjusted = self.generator.apply_slot_conflict_soft_penalties(
            "lighting", pool, picked, source, None
        )
        weights = {item["id"]: item.get("weight") for item in adjusted}
        self.assertEqual(weights["lamp"], 10)
        self.assertAlmostEqual(weights["sunny"], 2.0)
        # Hard filter must not remove the soft-penalized candidate.
        self.assertTrue(
            self.generator.compatible_with_slot_context("lighting", pool[0], picked, source)
        )

    def test_empty_matcher_side_never_matches(self) -> None:
        source = make_source(
            slot_conflicts=[
                {
                    "id": "broken_rule",
                    "left": {"slot": "time_of_day"},
                    "right": {"slot": "lighting", "ids": ["moonlight"]},
                    "severity": "hard",
                }
            ]
        )
        picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "time_of_day": {"id": "harsh_noon_sun", "tags": []},
        }
        item = {"id": "moonlight", "tags": []}
        self.assertFalse(
            self.generator.slot_conflict_violations("lighting", item, picked, source, "hard")
        )


class SlotContextRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()

    def test_declared_rule_replicates_builtin_moonlight_guard(self) -> None:
        source = make_source(
            slot_context_rules=[
                {
                    "id": "moonlight_needs_night_nature",
                    "slots": ["lighting", "light_type"],
                    "match_ids": ["moonlight"],
                    "requires_context_any": ["nature", "night", "landscape", "wild"],
                    "context_scope": "scene",
                    "severity": "hard",
                }
            ],
            builtin=False,
        )
        moonlight = {"id": "moonlight", "tags": []}
        urban_picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "location": {"id": "office", "tags": ["indoor", "office"]},
        }
        night_picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "location": {"id": "forest", "tags": ["nature", "night"]},
        }
        self.assertFalse(
            self.generator.compatible_with_slot_context("lighting", moonlight, urban_picked, source)
        )
        self.assertTrue(
            self.generator.compatible_with_slot_context("lighting", moonlight, night_picked, source)
        )

    def test_when_context_requires_item_tokens(self) -> None:
        source = make_source(
            slot_context_rules=[
                {
                    "id": "phone_context_lens",
                    "slots": ["lens"],
                    "when_context_any": ["phone"],
                    "requires_item_any": ["phone", "selfie", "social", "wide", "general"],
                    "severity": "hard",
                }
            ],
            builtin=False,
        )
        phone_picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "camera_type": {"id": "smartphone", "tags": ["phone"]},
        }
        telephoto = {"id": "telephoto_600", "tags": ["telephoto"]}
        wide = {"id": "wide_24", "tags": ["wide"]}
        self.assertFalse(
            self.generator.compatible_with_slot_context("lens", telephoto, phone_picked, source)
        )
        self.assertTrue(
            self.generator.compatible_with_slot_context("lens", wide, phone_picked, source)
        )
        # Rule is inactive without the phone context.
        plain_picked = {"subject": {"id": "person", "tags": ["human"]}}
        self.assertTrue(
            self.generator.compatible_with_slot_context("lens", telephoto, plain_picked, source)
        )

    def test_builtin_rules_still_apply_without_source(self) -> None:
        moonlight = {"id": "moonlight", "tags": []}
        urban_picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "location": {"id": "office", "tags": ["indoor", "office"]},
        }
        self.assertFalse(
            self.generator.compatible_with_slot_context("lighting", moonlight, urban_picked)
        )


class ShippedDictionaryConflictTests(unittest.TestCase):
    """The shipped dictionary must enforce its own declared hard conflicts."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()
        cls.data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))

    def test_builtin_rules_migrated_and_disabled(self) -> None:
        rules = self.data["coherence_rules"]
        self.assertFalse(rules["builtin_slot_context_rules"])
        rule_ids = {rule["id"] for rule in rules["slot_context_rules"]}
        self.assertIn("moonlight_needs_night_nature", rule_ids)
        self.assertIn("phone_context_lens", rule_ids)
        self.assertIn("adult_body_framing_context", rule_ids)

    def test_day_time_blocks_night_lighting_with_shipped_data(self) -> None:
        slots = self.data["slots"]
        noon = next(e for e in slots["time_of_day"] if e["id"] == "harsh_noon_sun")
        moonlight = next(e for e in slots["lighting"] if e["id"] == "moonlight")
        picked = {
            "subject": {"id": "person", "tags": ["human"]},
            "time_of_day": noon,
        }
        self.assertTrue(
            self.generator.slot_conflict_violations("lighting", moonlight, picked, self.data, "hard")
        )

    def test_rule_mode_generation_never_pairs_day_time_with_night_lighting(self) -> None:
        day_times = {
            e["id"]
            for e in self.data["slots"]["time_of_day"]
            if "day" in (e.get("facets", {}) or {}).get("time_of_day", [])
        }
        night_lights = {
            e["id"]
            for e in self.data["slots"]["lighting"]
            if "night" in (e.get("facets", {}) or {}).get("time_of_day", [])
        }
        self.assertTrue(day_times and night_lights)
        presets = ["street_documentary", "magazine_fashion", "cyberpunk_city"]
        for preset in presets:
            for seed in range(12):
                result = self.generator.generate_once(
                    data=self.data,
                    rng=random.Random(seed),
                    preset_id=preset,
                    langs=["en"],
                    include_negative=False,
                    negative_count=0,
                    include_choices=True,
                    detail_level="detailed",
                    selection_mode="rule",
                )
                choices = result.get("choices", {})
                time_id = choices.get("time_of_day")
                light_id = choices.get("lighting")
                if time_id in day_times:
                    self.assertNotIn(
                        light_id,
                        night_lights,
                        msg=f"{preset} seed={seed} paired {time_id} with {light_id}",
                    )


if __name__ == "__main__":
    unittest.main()


class PendingForcedLookAheadTests(unittest.TestCase):
    """Free-slot candidates that hard-conflict with EVERY upcoming forced
    candidate must be filtered before the forced slot is even picked."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()
        cls.data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))

    def test_rain_action_filtered_when_all_forced_locations_are_interior(self) -> None:
        pending = self.generator.pending_forced_conflict_entries(
            self.data, {"location": ["maid_cafe_interior", "tea_house_private_room"]}, {}
        )
        self.assertIn("location", pending)
        rain = next(e for e in self.data["slots"]["action"] if e["id"] == "walking_rain")
        self.assertTrue(
            self.generator.conflicts_with_all_pending_forced("action", rain, pending, self.data)
        )
        neutral = next(e for e in self.data["slots"]["action"] if e["id"] == "standing_silence")
        self.assertFalse(
            self.generator.conflicts_with_all_pending_forced("action", neutral, pending, self.data)
        )

    def test_mixed_forced_pool_does_not_block(self) -> None:
        # One outdoor candidate in the forced pool keeps the rain action viable.
        pending = self.generator.pending_forced_conflict_entries(
            self.data, {"location": ["maid_cafe_interior", "rooftop_city"]}, {}
        )
        rain = next(e for e in self.data["slots"]["action"] if e["id"] == "walking_rain")
        self.assertFalse(
            self.generator.conflicts_with_all_pending_forced("action", rain, pending, self.data)
        )

    def test_picked_forced_slot_not_treated_as_pending(self) -> None:
        picked = {"location": {"id": "maid_cafe_interior", "tags": ["interior"]}}
        pending = self.generator.pending_forced_conflict_entries(
            self.data, {"location": ["maid_cafe_interior"]}, picked
        )
        self.assertEqual(pending, {})


class RepairTierTests(unittest.TestCase):
    """리페어 완화 티어가 선언형 하드 규칙은 유지하는지 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()
        cls.data = json.loads(TAGS_PATH.read_text(encoding="utf-8"))

    def test_relaxed_tier_still_excludes_hard_conflicts(self) -> None:
        # 실내 location이 이미 선택된 상태에서 walking_rain은 완화 티어에서도 배제되어야 한다.
        picked = {
            "subject": next(e for e in self.data["slots"]["subject"] if e["id"] == "office_worker"),
            "location": next(e for e in self.data["slots"]["location"] if e["id"] == "maid_cafe_interior"),
        }
        ids = {"walking_rain", "standing_silence"}
        # standing_silence는 requires 태그 휴리스틱으로 tier1에서 살아남을 수도 있으므로,
        # tier2 강제 상황을 만들기 위해 requires가 까다로운 후보만 남긴 케이스도 확인한다.
        candidates = self.generator.soft_anchor_repair_candidates(
            self.data, {"id": "test_preset", "filters": {}}, "action", ids, picked, None
        )
        candidate_ids = {str(item.get("id")) for item in candidates}
        self.assertNotIn("walking_rain", candidate_ids)

    def test_post_render_allows_swapping_in_pool_member(self) -> None:
        slots = self.data["slots"]
        noon = next(e for e in slots["time_of_day"] if e["id"] == "harsh_noon_sun")
        picked = {
            "subject": next(e for e in slots["subject"] if e["id"] == "office_worker"),
            "time_of_day": noon,
        }
        ids = {"harsh_noon_sun", "civil_twilight"}
        # 기본(allow_current_in_pool=False): 현재 픽이 풀 멤버 → 빈 후보
        blocked = self.generator.soft_anchor_repair_candidates(
            self.data, {"id": "p", "filters": {}}, "time_of_day", ids, picked, None
        )
        self.assertEqual(blocked, [])
        # post-render 경로(allow_current_in_pool=True): 현재 픽 제외한 대체 풀 멤버 반환
        swappable = self.generator.soft_anchor_repair_candidates(
            self.data, {"id": "p", "filters": {}}, "time_of_day", ids, picked, None,
            allow_current_in_pool=True,
        )
        swap_ids = {str(item.get("id")) for item in swappable}
        self.assertIn("civil_twilight", swap_ids)
        self.assertNotIn("harsh_noon_sun", swap_ids)
