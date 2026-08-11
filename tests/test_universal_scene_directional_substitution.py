"""Focused polarity regressions independent of the universal asset hash chain."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "subculture-illustration-image-generator"
SCRIPT_ROOT = SKILL_ROOT / "scripts"
ASSET_ROOT = SKILL_ROOT / "assets"
sys.path.insert(0, str(SCRIPT_ROOT))

import universal_scene_runtime as runtime  # noqa: E402


class DirectionalSubstitutionPolarityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        semantic_bindings = json.loads(
            (
                ASSET_ROOT
                / "illustration_universal_semantic_bindings_v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.assets = SimpleNamespace(semantic_bindings=semantic_bindings)

    def assert_typed_truth(
        self,
        phrase: str,
        expectations: list[tuple[str, str]],
    ) -> None:
        groups = [
            {
                "alternatives": [alternative],
                "required_polarity": polarity,
            }
            for alternative, polarity in expectations
        ]
        validated = runtime._validate_contract_semantic_anchor_groups(
            groups,
            [phrase],
            fixed=True,
            where="probe.semantic_anchor_groups",
            assets=self.assets,
        )
        self.assertEqual(groups, validated)

        for group_index in range(len(groups)):
            unsafe = json.loads(json.dumps(groups))
            unsafe[group_index]["required_polarity"] = (
                "negated"
                if unsafe[group_index]["required_polarity"] == "affirmative"
                else "affirmative"
            )
            with self.assertRaisesRegex(
                runtime.InputContractError,
                "authenticate every group",
            ):
                runtime._validate_contract_semantic_anchor_groups(
                    unsafe,
                    [phrase],
                    fixed=True,
                    where="probe.semantic_anchor_groups",
                    assets=self.assets,
                )

    def test_asset_freezes_exact_locale_marker_directions(self) -> None:
        records = {
            record["locale"]: record["target_substitution_values"]
            for record in self.assets.semantic_bindings[
                "literal_polarity_contract"
            ]["negative_markers"]
        }
        self.assertEqual(
            {
                "ko": [
                    {
                        "value": "대신",
                        "marker_position_relative_to_negated_target": "after",
                    },
                    {
                        "value": "아니라",
                        "marker_position_relative_to_negated_target": "after",
                    },
                ],
                "en": [
                    {
                        "value": "instead of",
                        "marker_position_relative_to_negated_target": "before",
                    }
                ],
                "ja": [
                    {
                        "value": "代わり",
                        "marker_position_relative_to_negated_target": "after",
                    },
                    {
                        "value": "のではなく",
                        "marker_position_relative_to_negated_target": "after",
                    },
                    {
                        "value": "ではなく",
                        "marker_position_relative_to_negated_target": "after",
                    },
                ],
                "zh": [
                    {
                        "value": "代替",
                        "marker_position_relative_to_negated_target": "before",
                    },
                    {
                        "value": "而不是",
                        "marker_position_relative_to_negated_target": "before",
                    },
                ],
            },
            records,
        )

    def test_en_ja_zh_contrast_truth_table_and_unsafe_inverse(self) -> None:
        cases = [
            (
                "attach human hands instead of wings",
                [("attach human hands", "affirmative"), ("wings", "negated")],
            ),
            (
                "wings instead of attach human hands",
                [("attach human hands", "negated"), ("wings", "affirmative")],
            ),
            (
                "人間の手を付けるのではなく翼を使う",
                [("人間の手を付ける", "negated"), ("翼を使う", "affirmative")],
            ),
            (
                "翼ではなく人間の手を付ける",
                [("人間の手を付ける", "affirmative"), ("翼", "negated")],
            ),
            (
                "添加人手，而不是使用翅膀",
                [("添加人手", "affirmative"), ("使用翅膀", "negated")],
            ),
            (
                "用人手代替翅膀",
                [("用人手", "affirmative"), ("翅膀", "negated")],
            ),
            (
                "使用翅膀，而不是添加人手",
                [("添加人手", "negated"), ("使用翅膀", "affirmative")],
            ),
            (
                "用翅膀代替人手",
                [("人手", "negated"), ("用翅膀", "affirmative")],
            ),
        ]
        for phrase, expectations in cases:
            with self.subTest(phrase=phrase):
                self.assert_typed_truth(phrase, expectations)

    def test_c14_c21_concrete_value_anchors_survive_generic_role_negation(self) -> None:
        cases = [
            (
                "부러진 레버를 도구가 아니라 증거물로",
                [
                    ("부러진 레버", "affirmative"),
                    ("도구", "negated"),
                    ("증거물", "affirmative"),
                ],
            ),
            (
                "깨진 나침반을 길 찾는 도구가 아니라 누군가 항로를 조작했다는 증거로",
                [
                    ("깨진 나침반", "affirmative"),
                    ("도구", "negated"),
                    ("증거", "affirmative"),
                ],
            ),
        ]
        for phrase, expectations in cases:
            with self.subTest(phrase=phrase):
                self.assert_typed_truth(phrase, expectations)

    def test_reviewed_korean_anchor_stems_keep_local_predicate_scope(self) -> None:
        cases = [
            (
                "얼굴이 가려진 성인 방역 기술자",
                [("성인 방역 기술자", "affirmative")],
            ),
            (
                "각 손의 접촉과 하중이 충돌하지 않아야 해",
                [
                    ("접촉", "affirmative"),
                    ("하중", "affirmative"),
                    ("충돌", "negated"),
                ],
            ),
            (
                "고장 난 우산을 펴지 않고",
                [
                    ("고장 난 우산", "affirmative"),
                    ("펴지", "negated"),
                ],
            ),
            (
                "고장 난 우산을 펴지 않고 손잡이와 갈비살을 이용해",
                [
                    ("고장 난 우산", "affirmative"),
                    ("펴지", "negated"),
                    ("손잡이", "affirmative"),
                    ("갈비살", "affirmative"),
                ],
            ),
            (
                "깨진 나침반을 길 찾는 도구가 아니라 과거 사건의 증거로 함께 조사하는",
                [
                    ("깨진 나침반", "affirmative"),
                    ("도구", "negated"),
                    ("증거", "affirmative"),
                    ("함께 조사", "affirmative"),
                ],
            ),
        ]
        for phrase, expectations in cases:
            with self.subTest(phrase=phrase):
                self.assert_typed_truth(phrase, expectations)

    def test_contract_groups_may_span_owned_phrases_but_not_external_records(self) -> None:
        groups = [
            {
                "alternatives": ["attach human hands"],
                "required_polarity": "affirmative",
            },
            {"alternatives": ["wings"], "required_polarity": "negated"},
        ]
        validated = runtime._validate_contract_semantic_anchor_groups(
            groups,
            ["attach human hands", "instead of wings"],
            fixed=True,
            where="probe.semantic_anchor_groups",
            assets=self.assets,
        )
        self.assertEqual(groups, validated)
        with self.assertRaises(runtime.InputContractError):
            runtime._validate_contract_semantic_anchor_groups(
                groups,
                ["attach human hands"],
                fixed=True,
                where="probe.semantic_anchor_groups",
                assets=self.assets,
            )

    def test_raw_cjk_matching_does_not_promote_unrelated_compounds(self) -> None:
        polarities = runtime._literal_alias_occurrence_polarities(
            "公园代替博物馆",
            ["物"],
            self.assets,
            include_target_substitution=True,
        )
        self.assertEqual((), polarities)

    def test_all_contract_effects_keep_occurrence_local_polarity_in_four_locales(
        self,
    ) -> None:
        negative_clause = {
            "ko": lambda phrase: f"{phrase} 금지",
            "en": lambda phrase: f"do not include {phrase}",
            "ja": lambda phrase: f"{phrase} 禁止",
            "zh": lambda phrase: f"不要{phrase}",
        }
        profiles = self.assets.semantic_bindings["contract_effect_profiles"]
        self.assertEqual(9, len(profiles))
        observed = 0
        for profile in profiles:
            for alias_record in profile["literal_aliases"]:
                locale = alias_record["locale"]
                positive = alias_record["values"][0]
                negative = negative_clause[locale](positive)
                corpora = {
                    "negative_then_positive": f"{negative}. {positive}.",
                    "positive_then_negative": f"{positive}. {negative}.",
                    "all_negative": f"{negative}. {negative}.",
                }
                for order, corpus in corpora.items():
                    with self.subTest(
                        effect_id=profile["effect_id"],
                        locale=locale,
                        order=order,
                    ):
                        polarities = (
                            runtime._contract_effect_profile_direct_polarities(
                                profile,
                                [corpus],
                                self.assets,
                            )
                            | runtime._contract_effect_profile_compositional_polarities(
                                profile,
                                [corpus],
                                self.assets,
                            )
                        )
                        self.assertIn("negated", polarities)
                        if order == "all_negative":
                            self.assertNotIn("affirmative", polarities)
                        else:
                            self.assertIn("affirmative", polarities)
                        observed += 1
        self.assertEqual(108, observed)

    def test_coordinated_negative_lists_do_not_hide_independent_reassertions(
        self,
    ) -> None:
        negative_list = {
            "ko": lambda phrase: f"{phrase} 금지 그리고 {phrase} 금지",
            "en": lambda phrase: f"do not include {phrase} and repeat {phrase}",
            "ja": lambda phrase: f"{phrase} 禁止 そして {phrase} 禁止",
            "zh": lambda phrase: f"不要包含{phrase}并且重复{phrase}",
        }
        independent_reassertion = {
            "ko": lambda phrase: f"{phrase} 금지 그러나 장면은 {phrase}",
            "en": lambda phrase: (
                f"do not include {phrase} and the scene explicitly includes {phrase}"
            ),
            "ja": lambda phrase: f"{phrase} 禁止 しかし場面は {phrase}",
            "zh": lambda phrase: f"不要包含{phrase}但是场景明确包含{phrase}",
        }
        observed = 0
        for profile in self.assets.semantic_bindings["contract_effect_profiles"]:
            for alias_record in profile["literal_aliases"]:
                locale = alias_record["locale"]
                positive = alias_record["values"][0]
                for should_observe, corpus in (
                    (False, negative_list[locale](positive)),
                    (True, independent_reassertion[locale](positive)),
                ):
                    with self.subTest(
                        effect_id=profile["effect_id"],
                        locale=locale,
                        should_observe=should_observe,
                    ):
                        polarities = (
                            runtime._contract_effect_profile_direct_polarities(
                                profile,
                                [corpus],
                                self.assets,
                            )
                            | runtime._contract_effect_profile_compositional_polarities(
                                profile,
                                [corpus],
                                self.assets,
                            )
                        )
                        self.assertEqual(
                            should_observe,
                            "affirmative" in polarities,
                        )
                        observed += 1
        self.assertEqual(72, observed)

        weapon = next(
            profile
            for profile in self.assets.semantic_bindings["contract_effect_profiles"]
            if profile["effect_id"] == "active_weapon_discharge"
        )
        for corpus, should_observe in (
            ("Do not fire the machine gun and shoot the gun.", False),
            (
                "Weapon firing must not appear and the weapon fires a round.",
                True,
            ),
        ):
            with self.subTest(natural_weapon_control=corpus):
                polarities = (
                    runtime._contract_effect_profile_direct_polarities(
                        weapon,
                        [corpus],
                        self.assets,
                    )
                    | runtime._contract_effect_profile_compositional_polarities(
                        weapon,
                        [corpus],
                        self.assets,
                    )
                )
                self.assertEqual(should_observe, "affirmative" in polarities)


class SemanticFamilyPayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate_asset = json.loads(
            (
                ASSET_ROOT
                / "illustration_universal_scene_candidates_v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.candidate_by_id = {
            item["id"]: item for item in cls.candidate_asset["candidates"]
        }

    def test_apple_payload_matches_frozen_positive_control(self) -> None:
        profile = self.candidate_asset["proposal_profiles"][0]
        payload = runtime._proposal_semantic_family_payload(
            profile, self.candidate_by_id
        )
        self.assertEqual(profile["semantic_family_payload"], payload)
        self.assertEqual(
            "89805a24fc91b414199c257ca9c1420aae18868f0faf1f2960bfcdf31cb8cc0d",
            runtime.canonical_sha256(payload),
        )
        self.assertEqual(profile["semantic_family_signature"], runtime.canonical_sha256(payload))

    def test_raw_claim_reduction_sums_exclusive_and_maxes_shared(self) -> None:
        profile = {
            "slot_id": "prop",
            "value_id": "prop_apple",
            "candidate_ids": ["a", "b"],
            "event_roles": {role_id: None for role_id in runtime.EVENT_ROLE_IDS},
        }
        candidates = {
            "a": {
                "runtime_contract": {
                    "resource_claims": [
                        ["manipulator", "actor", 1, "exclusive"],
                        ["attention_channel", "actor", 1, "shared"],
                    ]
                }
            },
            "b": {
                "runtime_contract": {
                    "resource_claims": [
                        ["manipulator", "actor", 1, "exclusive"],
                        ["attention_channel", "actor", 2, "shared"],
                    ]
                }
            },
        }
        payload = runtime._proposal_semantic_family_payload(profile, candidates)
        self.assertEqual(
            [
                {
                    "owner_scope": "actor",
                    "resource_kind": "attention channel",
                    "mode": "shared",
                    "amount": 2,
                },
                {
                    "owner_scope": "actor",
                    "resource_kind": "manipulator",
                    "mode": "exclusive",
                    "amount": 2,
                },
            ],
            payload["resource_footprint"],
        )


class OwnerLocalBridgeIdTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidate_asset = json.loads(
            (
                ASSET_ROOT
                / "illustration_universal_scene_candidates_v1.json"
            ).read_text(encoding="utf-8")
        )
        compatibility = json.loads(
            (
                ASSET_ROOT
                / "illustration_universal_compatibility_graph_v1.json"
            ).read_text(encoding="utf-8")
        )
        semantic_bindings = json.loads(
            (
                ASSET_ROOT
                / "illustration_universal_semantic_bindings_v1.json"
            ).read_text(encoding="utf-8")
        )
        semantic_hash = runtime.canonical_sha256(semantic_bindings)
        cls.candidate_asset["semantic_bindings_asset_sha256"] = semantic_hash
        compatibility["semantic_bindings_asset_sha256"] = semantic_hash
        compatibility["candidate_asset_sha256"] = runtime.canonical_sha256(
            cls.candidate_asset
        )
        cls.assets = runtime.validate_universal_scene_assets(
            cls.candidate_asset,
            compatibility,
            semantic_bindings_asset=semantic_bindings,
        )
        cls.prompt_row = json.loads(
            (
                ASSET_ROOT / "universal_scene_prompt_holdout_v1.jsonl"
            ).read_text(encoding="utf-8").splitlines()[0]
        )
        cls.oracle_row = json.loads(
            (
                ASSET_ROOT / "universal_scene_current_holdout_v2.jsonl"
            ).read_text(encoding="utf-8").splitlines()[0]
        )
        cls.prompt_rows = [
            json.loads(line)
            for line in (
                ASSET_ROOT / "universal_scene_prompt_holdout_v1.jsonl"
            ).read_text(encoding="utf-8").splitlines()
        ]
        cls.oracle_rows = [
            json.loads(line)
            for line in (
                ASSET_ROOT / "universal_scene_current_holdout_v2.jsonl"
            ).read_text(encoding="utf-8").splitlines()
        ]

    def _build(self, creativity: float) -> dict[str, object]:
        scene = runtime.build_universal_scene_selection(
            concept=self.prompt_row["request_ko"],
            scene_contract=self.oracle_row["canonical_scene_contract"],
            topic_id=self.prompt_row["expected_topic_id"],
            format_id=self.prompt_row["expected_format"],
            creativity=creativity,
            seed=self.prompt_row["seed"],
            assets=self.assets,
        )
        return runtime.validate_universal_scene_selection(
            scene,
            self.prompt_row["request_ko"],
            self.assets,
            topic_id=self.prompt_row["expected_topic_id"],
            format_id=self.prompt_row["expected_format"],
            creativity=creativity,
            seed=self.prompt_row["seed"],
        )

    def _validate_mutated(
        self, scene: dict[str, object], creativity: float = 0.5
    ) -> dict[str, object]:
        return runtime.validate_universal_scene_selection(
            scene,
            self.prompt_row["request_ko"],
            self.assets,
            topic_id=self.prompt_row["expected_topic_id"],
            format_id=self.prompt_row["expected_format"],
            creativity=creativity,
            seed=self.prompt_row["seed"],
        )

    def _build_case(self, index: int, creativity: float = 0.5) -> dict[str, object]:
        prompt_row = self.prompt_rows[index]
        oracle_row = self.oracle_rows[index]
        return runtime.build_universal_scene_selection(
            concept=prompt_row["request_ko"],
            scene_contract=oracle_row["canonical_scene_contract"],
            topic_id=prompt_row["expected_topic_id"],
            format_id=prompt_row["expected_format"],
            creativity=creativity,
            seed=prompt_row["seed"],
            assets=self.assets,
        )

    def _role_payloads(
        self, scene: dict[str, object], case_index: int
    ) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        validated = runtime.validate_scene_contract(
            self.prompt_rows[case_index]["request_ko"],
            self.oracle_rows[case_index]["canonical_scene_contract"],
            assets=self.assets,
        )
        return runtime._role_projection_payloads(
            selection=scene,
            validated=validated,
            assets=self.assets,
        )

    @staticmethod
    def _core_bridge_pixel_rows(scene: dict[str, object]) -> list[dict[str, object]]:
        core_atom_id = next(
            atom["instance_id"]
            for atom in scene["atoms"]
            if atom["candidate_id"] == "usl_core_identity_anchor"
        )
        bridge_ids = {
            bridge["bridge_id"]
            for bridge in scene["bridges"]
            if bridge["bridge_id"].endswith(f"_{core_atom_id}")
        }
        return sorted(
            (
                item
                for item in scene["pixel_evidence_contract"]["items"]
                if item["source_kind"] == "bridge"
                and item["source_id"] in bridge_ids
            ),
            key=lambda item: item["item_id"],
        )

    def test_protected_bridge_pixels_keep_owner_local_ids_across_creativity(self) -> None:
        scenes = [self._build(value) for value in (0.2, 0.5, 0.85)]
        protected_rows = [self._core_bridge_pixel_rows(scene) for scene in scenes]
        self.assertTrue(protected_rows[0])
        self.assertEqual(protected_rows[0], protected_rows[1])
        self.assertEqual(protected_rows[1], protected_rows[2])

        for scene in scenes:
            bridge_ids = [bridge["bridge_id"] for bridge in scene["bridges"]]
            edge_ids = [edge["edge_id"] for edge in scene["selected_event"]["spine_edges"]]
            pixel_ids = [
                item["item_id"]
                for item in scene["pixel_evidence_contract"]["items"]
            ]
            self.assertEqual(len(bridge_ids), len(set(bridge_ids)))
            self.assertEqual(len(edge_ids), len(set(edge_ids)))
            self.assertEqual(len(pixel_ids), len(set(pixel_ids)))
            for bridge in scene["bridges"]:
                self.assertTrue(
                    bridge["bridge_id"].startswith(
                        f"bridge_{bridge['bridge_type']}_01_"
                    )
                )
                self.assertEqual(
                    [f"edge_{bridge['bridge_id']}"],
                    bridge["event_edge_ids"],
                )

    def test_creativity_invariant_trace_is_exactly_band_independent(self) -> None:
        scenes = [self._build(value) for value in (0.2, 0.5, 0.85)]
        traces = [scene["creativity_invariant_trace"] for scene in scenes]
        self.assertEqual(traces[0], traces[1])
        self.assertEqual(traces[1], traces[2])
        self.assertEqual(
            traces[0]["trace_sha256"], runtime._trace_self_hash(traces[0])
        )
        for scene in scenes:
            post = scene["postselection_run_trace"]
            self.assertEqual(32, len(post["guard_executions"]))
            self.assertEqual(7, len(post["universal_rule_executions"]))
            self.assertEqual(18, len(post["postselection_cardinality_decisions"]))
            self.assertEqual(post["trace_sha256"], runtime._trace_self_hash(post))
        distance_policy = self.assets.compatibility["distance_policy"]
        self.assertNotIn(
            "max_remote_or_high_load_optional_premises", distance_policy
        )
        self.assertTrue(
            all(
                "max_optional_remote" not in band
                for band in distance_policy["creativity_bands"]
            )
        )
        runtime_remote_limit = next(
            row
            for row in traces[0]["cardinality_limits"]
            if row["record_id"] == "runtime_limit__global_optional_remote"
        )
        self.assertEqual(runtime.GLOBAL_OPTIONAL_REMOTE_MAX, runtime_remote_limit["maximum"])

    def test_forged_invariant_partition_and_hash_fail_replay(self) -> None:
        scene = json.loads(json.dumps(self._build(0.5), ensure_ascii=False))
        trace = scene["creativity_invariant_trace"]
        trace["eligible_candidate_ids"].pop()
        trace["trace_sha256"] = runtime._trace_self_hash(trace)
        with self.assertRaises(runtime.SelectionError):
            self._validate_mutated(scene)

    def test_forged_postselection_guard_and_hash_fail_replay(self) -> None:
        scene = json.loads(json.dumps(self._build(0.5), ensure_ascii=False))
        post = scene["postselection_run_trace"]
        post["guard_executions"][0]["reason_codes"] = ["guard_not_applicable"]
        post["guard_executions_sha256"] = runtime.canonical_sha256(
            post["guard_executions"]
        )
        post["trace_sha256"] = runtime._trace_self_hash(post)
        with self.assertRaises(runtime.SelectionError):
            self._validate_mutated(scene)

    def test_runtime_selected_roles_require_exact_bidirectional_sources(self) -> None:
        proposal_scene = json.loads(json.dumps(self._build_case(0)))
        proposal_action = next(
            role
            for role in proposal_scene["selected_event"]["roles"]
            if role["role_id"] == "action"
        )
        proposal_action["source_id"] = proposal_scene["atoms"][1]["instance_id"]
        with self.assertRaisesRegex(
            runtime.SelectionError,
            "swapped away from its exact proposal",
        ):
            self._role_payloads(proposal_scene, 0)

        candidate_scene = json.loads(json.dumps(self._build_case(4)))
        phase = next(
            role
            for role in candidate_scene["selected_event"]["roles"]
            if role["role_id"] == "phase"
        )
        phase_source = next(
            atom
            for atom in candidate_scene["atoms"]
            if atom["instance_id"] == phase["source_id"]
        )
        phase_binding = next(
            binding
            for binding in phase_source["bindings"]
            if binding["role_id"] == "phase"
        )
        phase_source["bindings"].append(json.loads(json.dumps(phase_binding)))
        with self.assertRaisesRegex(
            runtime.SelectionError,
            "source atom does not declare and serialize",
        ):
            self._role_payloads(candidate_scene, 4)

        missing_source_scene = json.loads(json.dumps(self._build_case(4)))
        missing_phase = next(
            role
            for role in missing_source_scene["selected_event"]["roles"]
            if role["role_id"] == "phase"
        )
        missing_phase["source_id"] = "atom_missing_phase_authority"
        with self.assertRaisesRegex(runtime.SelectionError, "lacks an exact selected source"):
            self._role_payloads(missing_source_scene, 4)

        bridge_scene = json.loads(json.dumps(self._build_case(4)))
        result = next(
            role
            for role in bridge_scene["selected_event"]["roles"]
            if role["role_id"] == "result"
        )
        result["source_id"] = next(
            bridge["bridge_id"]
            for bridge in bridge_scene["bridges"]
            if bridge["bridge_id"] != result["source_id"]
        )
        with self.assertRaisesRegex(runtime.SelectionError, "does not own its exact typed endpoint"):
            self._role_payloads(bridge_scene, 4)

        duplicate_bridge_scene = json.loads(json.dumps(self._build_case(4)))
        duplicate_result = next(
            role
            for role in duplicate_bridge_scene["selected_event"]["roles"]
            if role["role_id"] == "result"
        )
        original_bridge = next(
            bridge
            for bridge in duplicate_bridge_scene["bridges"]
            if bridge["bridge_id"] == duplicate_result["source_id"]
        )
        duplicate_bridge = json.loads(json.dumps(original_bridge))
        duplicate_bridge["bridge_id"] = f"{original_bridge['bridge_id']}_duplicate"
        duplicate_bridge_scene["bridges"].append(duplicate_bridge)

        # The original generated bridge remains the canonical source even when
        # an otherwise identical later bridge is injected.
        self._role_payloads(duplicate_bridge_scene, 4)
        duplicate_result["source_id"] = duplicate_bridge["bridge_id"]
        with self.assertRaisesRegex(
            runtime.SelectionError,
            "does not cite the canonical exact typed bridge endpoint",
        ):
            self._role_payloads(duplicate_bridge_scene, 4)


if __name__ == "__main__":
    unittest.main()
