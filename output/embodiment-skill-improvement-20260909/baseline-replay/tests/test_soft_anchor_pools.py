"""Unit tests for weighted anchor pools and per-recipe soft-mode promotion."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest import mock

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


class WeightedPoolNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wrapper = load_module("ppg_wrapper_pools", WRAPPER_PATH)

    def test_normalize_weighted_pool_mixes_strings_and_objects(self) -> None:
        ids, weights = self.wrapper.normalize_weighted_pool(
            [{"id": "main_anchor", "w": 3}, "alternate", {"id": "secondary", "w": 1.0}]
        )
        self.assertEqual(ids, ["main_anchor", "alternate", "secondary"])
        self.assertEqual(weights, {"main_anchor": 3.0})

    def test_normalize_weighted_pool_ignores_invalid_entries(self) -> None:
        ids, weights = self.wrapper.normalize_weighted_pool(
            [{"w": 5}, {"id": "bad_weight", "w": "abc"}, {"id": "neg", "w": -2}, ""]
        )
        self.assertEqual(ids, ["bad_weight", "neg"])
        self.assertEqual(weights, {})

    def test_anchor_pool_for_slot_accepts_weighted_entries(self) -> None:
        recipe = {"anchor_pool": {"location": [{"id": "castle", "w": 2}, "garden"]}}
        self.assertEqual(
            self.wrapper.anchor_pool_for_slot(recipe, "location", ["fallback"]),
            ["castle", "garden"],
        )
        self.assertEqual(
            self.wrapper.anchor_pool_weights_for_slot(recipe, "location"),
            {"castle": 2.0},
        )

    def test_specs_carry_pool_weights_into_built_spec(self) -> None:
        recipes = {"soft_anchor_defaults": {"anchor_slots": ["location"], "free_slots": []}}
        recipe = {
            "soft_anchor_slots": ["location"],
            "anchor_pool": {"location": [{"id": "castle", "w": 2}, "garden"]},
        }
        specs = self.wrapper.soft_anchor_specs_from_mapping(
            recipes, {"location": ["castle"]}, recipe, "role", set()
        )
        self.assertEqual(len(specs), 1)
        self.assertEqual(specs[0]["pool"], ["castle", "garden"])
        self.assertEqual(specs[0]["pool_weights"], {"castle": 2.0})
        spec = self.wrapper.build_soft_anchor_spec(specs, [1], "test")
        self.assertEqual(spec["anchors"][0]["pool_weights"], {"castle": 2.0})


class SoftAnchorPoolWeightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_module("ppg_generator_pools", GENERATOR_PATH)

    def make_policy(self) -> dict:
        return {
            "enabled": True,
            "anchors": [
                {
                    "slot": "location",
                    "ids": ["castle"],
                    "pool": ["castle", "garden"],
                    "pool_weights": {"castle": 3.0},
                }
            ],
        }

    def test_pool_weight_lookup(self) -> None:
        policy = self.make_policy()
        self.assertEqual(self.generator.soft_anchor_pool_weight(policy, "location", "castle"), 3.0)
        self.assertEqual(self.generator.soft_anchor_pool_weight(policy, "location", "garden"), 1.0)
        self.assertEqual(self.generator.soft_anchor_pool_weight(policy, "prop", "castle"), 1.0)

    def test_apply_soft_anchor_bias_uses_pool_weight(self) -> None:
        policy = self.make_policy()
        contract = {"soft_anchor_policy": policy}
        pool = [
            {"id": "castle", "weight": 1},
            {"id": "garden", "weight": 1},
            {"id": "alley", "weight": 1},
        ]
        adjusted = self.generator.apply_soft_anchor_bias("location", pool, None, contract)
        weights = {item["id"]: float(item.get("weight", 1)) for item in adjusted}
        # Both pool members get the soft anchor multiplier; castle also gets
        # its in-pool weight on top, garden does not.
        self.assertAlmostEqual(weights["castle"] / weights["garden"], 3.0)
        self.assertEqual(weights["alley"], 1.0)


class ConceptModeDefaultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.wrapper = load_module("ppg_wrapper_mode", WRAPPER_PATH)

    def test_recipe_default_soft_applies_when_mode_not_explicit(self) -> None:
        recipes = self.wrapper.load_concept_recipes()
        recipes["roles"]["회사원"]["concept_mode_default"] = "soft"
        with mock.patch.object(self.wrapper, "load_concept_recipes", return_value=recipes):
            _, explanations = self.wrapper.resolve_concepts(
                ["--seed", "42"], ["회사원"], "legacy", concept_mode_explicit=False
            )
            self.assertEqual(explanations[0]["concept_mode"], "soft")
            self.assertFalse(explanations[0]["forced_slots_applied"])

            # Explicit --concept-mode always wins over the recipe default.
            _, explanations = self.wrapper.resolve_concepts(
                ["--seed", "42"], ["회사원"], "legacy", concept_mode_explicit=True
            )
            self.assertEqual(explanations[0]["concept_mode"], "legacy")
            self.assertTrue(explanations[0]["forced_slots_applied"])

    def test_without_recipe_default_mode_stays_legacy(self) -> None:
        _, explanations = self.wrapper.resolve_concepts(
            ["--seed", "42"], ["회사원"], "legacy", concept_mode_explicit=False
        )
        self.assertEqual(explanations[0]["concept_mode"], "legacy")
        self.assertTrue(explanations[0]["forced_slots_applied"])


if __name__ == "__main__":
    unittest.main()


class SoftReliabilityImprovementTests(unittest.TestCase):
    """승격 보상·primary 티어·플로어 일반화·리페어 수선(soft 보편 개선) 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_module("ppg_soft_reliability", GENERATOR_PATH)

    def semantic_context(self, weight=0.75):
        return {"selection_mode": "semantic", "semantic_weight": weight}

    def test_semantic_base_power_table(self) -> None:
        cases = {1.0: 0.15, 0.75: 0.3625, 0.35: 0.7025, 0.0: 1.0}
        for weight, expected in cases.items():
            self.assertAlmostEqual(
                self.g.semantic_base_power(self.semantic_context(weight)), expected, places=6
            )
        self.assertEqual(self.g.semantic_base_power(None), 1.0)

    def test_bias_compensation_restores_nominal_factor(self) -> None:
        policy = {"enabled": True, "anchors": [{"slot": "location", "ids": ["castle"], "pool": ["castle"]}]}
        contract = {"soft_anchor_policy": policy}
        pool = [{"id": "castle", "weight": 1.0}, {"id": "alley", "weight": 1.0}]
        context = self.semantic_context(0.75)
        adjusted = self.g.apply_soft_anchor_bias("location", pool, context, contract)
        weights = {item["id"]: float(item.get("weight", 1)) for item in adjusted}
        bp = self.g.semantic_base_power(context)
        # 최종 가중 채널(weight**bp)에서 명목 24×가 복원되어야 한다.
        effective_ratio = (weights["castle"] ** bp) / (weights["alley"] ** bp)
        self.assertAlmostEqual(effective_ratio, self.g.SOFT_ANCHOR_WEIGHT_MULTIPLIER, places=4)

    def test_bias_without_semantic_context_keeps_raw_factor(self) -> None:
        policy = {"enabled": True, "anchors": [{"slot": "location", "ids": ["castle"], "pool": ["castle"]}]}
        contract = {"soft_anchor_policy": policy}
        pool = [{"id": "castle", "weight": 1.0}]
        adjusted = self.g.apply_soft_anchor_bias("location", pool, None, contract)
        self.assertAlmostEqual(float(adjusted[0]["weight"]), self.g.SOFT_ANCHOR_WEIGHT_MULTIPLIER, places=4)

    def test_primary_tier_between_base_and_critical(self) -> None:
        # critical 앵커는 풀 자체를 제약하므로 별도 슬롯으로 검증한다.
        policy = {
            "enabled": True,
            "anchors": [
                {"slot": "prop", "ids": ["plain"], "pool": ["plain"]},
                {"slot": "prop", "ids": ["prime"], "pool": ["prime"], "primary": True},
                {"slot": "location", "ids": ["crit"], "pool": ["crit"], "critical": True},
            ],
        }
        contract = {"soft_anchor_policy": policy}
        pool = [{"id": "plain", "weight": 1.0}, {"id": "prime", "weight": 1.0}]
        adjusted = self.g.apply_soft_anchor_bias("prop", pool, None, contract)
        weights = {item["id"]: float(item["weight"]) for item in adjusted}
        self.assertAlmostEqual(weights["plain"], 24.0, places=3)
        self.assertAlmostEqual(weights["prime"], 48.0, places=3)
        crit_adjusted = self.g.apply_soft_anchor_bias(
            "location", [{"id": "crit", "weight": 1.0}], None, contract
        )
        self.assertAlmostEqual(float(crit_adjusted[0]["weight"]), 64.0, places=3)
        # semantic_policy 오버라이드
        context = {"selection_mode": "semantic", "semantic_weight": 0.0,
                   "semantic_policy": {"soft_anchor_weights": {"primary": 50}}}
        adjusted = self.g.apply_soft_anchor_bias("prop", pool, context, contract)
        weights = {item["id"]: float(item["weight"]) for item in adjusted}
        self.assertAlmostEqual(weights["prime"], 50.0, places=3)

    def make_floor_args(self, ids_weights, anchor_pool, variant_group=""):
        candidates = [({"id": i}, [], None, w, 0.0, {}) for i, w in ids_weights]
        weights = [w for _, w in ids_weights]
        anchors = [{"slot": "prop", "ids": list(anchor_pool), "pool": list(anchor_pool)}]
        if variant_group:
            anchors[0]["variant_group"] = variant_group
        context = {"generation_contract": {"soft_anchor_policy": {"enabled": True, "anchors": anchors}}}
        return candidates, weights, context

    def test_slot_mass_floor_without_variant_group(self) -> None:
        # 앵커 1개·variant_group 없음 — 기존 코드라면 무동작이던 상황
        candidates, weights, context = self.make_floor_args(
            [("anchor_a", 1.0), ("free_b", 9.0), ("free_c", 10.0)], {"anchor_a"}
        )
        adjusted, summary = self.g.apply_soft_anchor_probability_floor("prop", candidates, weights, context)
        total = sum(adjusted)
        anchor_share = adjusted[0] / total
        self.assertGreaterEqual(anchor_share, 0.549)
        self.assertIn("slot_floor", summary["mode"])

    def test_slot_mass_cap(self) -> None:
        candidates, weights, context = self.make_floor_args(
            [("anchor_a", 990.0), ("free_b", 1.0)], {"anchor_a"}
        )
        adjusted, summary = self.g.apply_soft_anchor_probability_floor("prop", candidates, weights, context)
        anchor_share = adjusted[0] / sum(adjusted)
        self.assertLessEqual(anchor_share, 0.921)
        self.assertIn("slot_cap", summary["mode"])

    def test_floor_noop_without_anchor_pool(self) -> None:
        candidates = [({"id": "x"}, [], None, 1.0, 0.0, {}), ({"id": "y"}, [], None, 2.0, 0.0, {})]
        context = {"generation_contract": {"soft_anchor_policy": {"enabled": True, "anchors": []}}}
        adjusted, summary = self.g.apply_soft_anchor_probability_floor("prop", candidates, [1.0, 2.0], context)
        self.assertEqual(adjusted, [1.0, 2.0])
        self.assertIsNone(summary)

    def test_selected_rate_floor_spec_override(self) -> None:
        spec = {"mode": "soft", "min_anchors": 1, "selected_rate_floor": 0.5,
                "anchors": [{"slot": "prop", "ids": ["a"]}]}
        normalized = self.g.normalize_soft_anchor_spec(spec)
        self.assertEqual(normalized["selected_rate_floor"], 0.5)
        self.assertEqual(self.g.soft_anchor_selected_rate_floor(normalized), 0.5)
        default = self.g.normalize_soft_anchor_spec({"mode": "soft", "min_anchors": 1,
                                                     "anchors": [{"slot": "prop", "ids": ["a"]}]})
        self.assertEqual(self.g.soft_anchor_selected_rate_floor(default), self.g.SOFT_ANCHOR_SELECTED_RATE_FLOOR)


class OrphanFloorClampTests(unittest.TestCase):
    """dedupe가 앵커를 떨어뜨려도 group/source floor가 고아로 남지 않아야 한다."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.wrapper = load_module("ppg_wrapper_clamp", WRAPPER_PATH)

    def test_orphan_group_floor_is_clamped(self) -> None:
        specs = [
            {  # critical 슬롯의 role 앵커 (생존)
                "slot": "prop", "ids": ["role_prop"], "pool": ["role_prop"], "terms": ["prop"],
                "source": "role", "critical": True, "groups": ["role_primary"],
                "group_floors": {"role_primary": 1},
            },
            {  # 같은 슬롯의 비-critical mixin primary 앵커 (dedupe에서 탈락)
                "slot": "prop", "ids": ["mixin_prop"], "pool": ["mixin_prop"], "terms": ["prop"],
                "source": "mixin", "critical": False, "primary": True, "groups": ["mixin_primary"],
                "group_floors": {"mixin_primary": 1},
            },
        ]
        spec = self.wrapper.build_soft_anchor_spec(specs, [1], "테스트")
        slots = [(a["slot"], a.get("source")) for a in spec["anchors"]]
        self.assertEqual(len(spec["anchors"]), 1)  # 비-critical은 탈락
        self.assertNotIn("mixin_primary", spec["group_floors"])  # 고아 플로어 제거
        self.assertNotIn("mixin", spec["source_floors"])  # 캐리어 없는 소스 플로어 제거
        self.assertEqual(spec["group_floors"].get("role_primary"), 1)


class SteeringAnchorPreservationTests(unittest.TestCase):
    """intent steering이 soft 앵커 풀 후보를 제거하지 못함을 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_module("ppg_steering_preserve", GENERATOR_PATH)

    def steering_context(self):
        return {
            "selection_mode": "semantic",
            "intent_steering": {"mode": "auto", "enabled": True, "families": ["clinical"], "decisions": []},
        }

    def test_steering_preserves_anchor_pool_members(self) -> None:
        pool = [
            {"id": "clinical_lab", "weight": 1.0},
            {"id": "hospital_corridor", "weight": 1.0},
            {"id": "hospital_waiting_room", "weight": 1.0},
        ]
        context = self.steering_context()
        steered_only = [pool[0]]
        decision = {"slot": "location", "family": "clinical", "before": 3, "after": 1}
        with mock.patch.object(self.g, "intent_steering_enabled", return_value=True), \
                mock.patch.object(self.g, "ordered_steering_families", return_value=["clinical"]), \
                mock.patch.object(self.g, "apply_family_steering", return_value=(steered_only, decision)):
            result = self.g.steer_semantic_candidate_pool(
                "location", pool, context, anchor_ids={"hospital_corridor", "hospital_waiting_room"}
            )
        ids = {item["id"] for item in result}
        self.assertEqual(ids, {"clinical_lab", "hospital_corridor", "hospital_waiting_room"})
        recorded = context["intent_steering"]["decisions"][0]
        self.assertEqual(recorded["anchor_preserved"], ["hospital_corridor", "hospital_waiting_room"])
        self.assertEqual(recorded["after"], 3)

    def test_steering_without_anchor_ids_unchanged(self) -> None:
        pool = [{"id": "clinical_lab"}, {"id": "hospital_corridor"}]
        context = self.steering_context()
        decision = {"slot": "location", "family": "clinical", "before": 2, "after": 1}
        with mock.patch.object(self.g, "intent_steering_enabled", return_value=True), \
                mock.patch.object(self.g, "ordered_steering_families", return_value=["clinical"]), \
                mock.patch.object(self.g, "apply_family_steering", return_value=([pool[0]], decision)):
            result = self.g.steer_semantic_candidate_pool("location", pool, context, anchor_ids=set())
        self.assertEqual([item["id"] for item in result], ["clinical_lab"])
        self.assertNotIn("anchor_preserved", context["intent_steering"]["decisions"][0])


class SourceRateFloorTests(unittest.TestCase):
    """소스별 슬롯 매치 rate 플로어(게이트 정합)가 repair 계약을 트립함을 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_module("ppg_source_rate", GENERATOR_PATH)

    def policy_with_three_mixin_slots(self, **extra):
        return {
            "enabled": True,
            "min_anchors": 0,
            "anchors": [
                {"slot": "expression", "pool": ["obsessive_gaze"], "source": "mixin"},
                {"slot": "prop", "pool": ["ribbon_scissors"], "source": "mixin"},
                {"slot": "appearance_type", "pool": ["classic_elegant"], "source": "mixin"},
            ],
            **extra,
        }

    def picked(self, include_appearance: bool):
        picked = {
            "expression": {"id": "obsessive_gaze"},
            "prop": {"id": "ribbon_scissors"},
        }
        if include_appearance:
            picked["appearance_type"] = {"id": "classic_elegant"}
        return picked

    def test_mixin_rate_below_default_floor_fails(self) -> None:
        status = self.g.soft_anchor_match_status(
            self.policy_with_three_mixin_slots(), self.picked(include_appearance=False)
        )
        self.assertFalse(status["passed"])
        self.assertIn("source_rate_floor_not_met:mixin", status["failure_reasons"])
        miss = status["source_rate_misses"][0]
        self.assertEqual(miss["missing_slots"], ["appearance_type"])
        self.assertAlmostEqual(status["source_rates"]["mixin"], 0.6667, places=4)

    def test_full_match_passes(self) -> None:
        status = self.g.soft_anchor_match_status(
            self.policy_with_three_mixin_slots(), self.picked(include_appearance=True)
        )
        self.assertTrue(status["passed"])
        self.assertEqual(status["source_rate_misses"], [])

    def test_spec_override_relaxes_floor(self) -> None:
        policy = self.policy_with_three_mixin_slots(source_rate_floors={"mixin": 0.5})
        status = self.g.soft_anchor_match_status(policy, self.picked(include_appearance=False))
        self.assertNotIn("source_rate_floor_not_met:mixin", status["failure_reasons"])


class PresetDomainInferenceTests(unittest.TestCase):
    """cafe 문자열이 인물 프리셋에 food 도메인을 부여하지 않음을 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_module("ppg_domain_infer", GENERATOR_PATH)

    def test_cafe_portrait_is_not_food(self) -> None:
        domains = self.g.infer_preset_domains(
            {"id": "maid_cafe_cosplay_portrait", "en": "maid cafe cosplay portrait"}
        )
        self.assertNotIn("food", domains)
        self.assertIn("portrait", domains)

    def test_real_food_terms_still_match(self) -> None:
        for term in ("street_food stall", "pojangmacha night", "tteokbokki close-up"):
            domains = self.g.infer_preset_domains({"id": "x", "en": term})
            self.assertIn("food", domains)


class ContractReconcileTests(unittest.TestCase):
    """contract 진화로 뒤늦게 차단된 픽을 재선택(드롭 대신)함을 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_module("ppg_reconcile", GENERATOR_PATH)

    def make_contract(self, subject_category="object"):
        return {
            "subject_category": subject_category,
            "preset_domains": ["jewelry", "product"],
            "forced_slots": [],
            "adult_allowed": False,
            "reselect_events": [],
            "soft_anchor_policy": {},
        }

    def test_blocked_entry_is_reselected(self) -> None:
        import random as _random

        picked = {
            "subject": {"id": "ring", "en": "a ring", "tags": ["object", "jewelry"]},
            "genre": {"id": "beauty", "en": "beauty editorial", "tags": ["beauty"]},
        }
        contract = self.make_contract()
        replacement = {"id": "lifestyle", "en": "lifestyle", "tags": []}
        with mock.patch.object(self.g, "choose_slot", return_value=replacement), \
                mock.patch.object(self.g, "refresh_generation_contract", return_value=contract):
            self.g.reconcile_contract_blocked_picks(
                {}, {}, _random.Random(1), picked, None, None, contract
            )
        self.assertEqual(picked["genre"]["id"], "lifestyle")
        event = contract["reselect_events"][0]
        self.assertEqual(event["status"], "contract_reselected")
        self.assertEqual(event["reason"], "human_visual_signal_not_allowed")
        self.assertEqual(event["replacement"], "lifestyle")

    def test_blocked_entry_dropped_when_no_replacement(self) -> None:
        import random as _random

        picked = {"genre": {"id": "portrait", "en": "portrait", "tags": ["portrait"]}}
        contract = self.make_contract()
        with mock.patch.object(self.g, "choose_slot", return_value=None), \
                mock.patch.object(self.g, "refresh_generation_contract", return_value=contract):
            self.g.reconcile_contract_blocked_picks(
                {}, {}, _random.Random(1), picked, None, None, contract
            )
        self.assertNotIn("genre", picked)
        self.assertEqual(contract["reselect_events"][0]["status"], "contract_dropped")

    def test_clean_picks_untouched(self) -> None:
        import random as _random

        picked = {"genre": {"id": "still_life", "en": "still life", "tags": ["object"]}}
        contract = self.make_contract()
        self.g.reconcile_contract_blocked_picks(
            {}, {}, _random.Random(1), picked, None, None, contract
        )
        self.assertEqual(picked["genre"]["id"], "still_life")
        self.assertEqual(contract["reselect_events"], [])

    def test_forced_slot_protected(self) -> None:
        import random as _random

        picked = {"genre": {"id": "beauty", "en": "beauty", "tags": ["beauty"]}}
        contract = self.make_contract()
        contract["forced_slots"] = ["genre"]
        self.g.reconcile_contract_blocked_picks(
            {}, {}, _random.Random(1), picked, None, None, contract
        )
        self.assertEqual(picked["genre"]["id"], "beauty")
        self.assertEqual(contract["reselect_events"], [])


class AnchorReachabilityGuardTests(unittest.TestCase):
    """subject 선택이 다른 앵커 슬롯 도달성을 최대로 보존함을 검증."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.g = load_module("ppg_reachability", GENERATOR_PATH)
        cls.data = {
            "slot_applicability": {
                "slots": {
                    "makeup_style": {"subject_categories": ["human"]},
                    "surface_material": {"subject_categories": ["object"]},
                }
            },
            "slots": {},
        }

    def contract(self, anchors):
        return {"soft_anchor_policy": {"anchors": anchors}, "reselect_events": []}

    def test_min_denial_candidate_survives(self) -> None:
        pool = [
            {"id": "doll_cosplayer", "tags": ["human"], "kind": ["human"]},
            {"id": "automaton", "tags": ["robot", "object"], "kind": ["object"]},
        ]
        # human: surface_material 1개 차단 / object: makeup 1개 차단 → 동수면 무필터
        contract = self.contract([
            {"slot": "makeup_style", "pool": ["dark_makeup"]},
            {"slot": "surface_material", "pool": ["aluminum"]},
        ])
        out = self.g.apply_anchor_reachability_guard("subject", pool, self.data, contract)
        self.assertEqual({e["id"] for e in out}, {"doll_cosplayer", "automaton"})
        self.assertEqual(contract["reselect_events"], [])
        # expression(기본 정책: human/animal 전용)을 추가하면 object가 2개 차단 → human만 생존
        contract = self.contract([
            {"slot": "makeup_style", "pool": ["dark_makeup"]},
            {"slot": "expression", "pool": ["stare"]},
            {"slot": "surface_material", "pool": ["aluminum"]},
        ])
        out = self.g.apply_anchor_reachability_guard("subject", pool, self.data, contract)
        self.assertEqual([e["id"] for e in out], ["doll_cosplayer"])
        event = contract["reselect_events"][-1]
        self.assertEqual(event["status"], "anchor_reachability_filtered")
        self.assertEqual(event["filtered"][0]["id"], "automaton")

    def test_non_subject_slot_noop(self) -> None:
        pool = [{"id": "x"}]
        out = self.g.apply_anchor_reachability_guard("prop", pool, self.data, self.contract([]))
        self.assertEqual(out, pool)

    def test_no_anchors_noop(self) -> None:
        pool = [{"id": "x", "tags": ["human"]}]
        out = self.g.apply_anchor_reachability_guard("subject", pool, self.data, self.contract([]))
        self.assertEqual([e["id"] for e in out], ["x"])
