from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EXTENSION_PATH = (
    SKILL_DIR / "assets" / "photo_prompt_natural_environment_extension.json"
)
RECIPES_PATH = SKILL_DIR / "assets" / "concept_recipes.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
EVIDENCE_PATH = (
    ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generate_photo_prompt  # noqa: E402
import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


EXPECTED_SLOT_COUNTS = {
    "aesthetic_trend": 12,
    "subject": 12,
    "action": 12,
    "location": 12,
    "surface_material": 11,
    "composition": 12,
    "weather": 4,
}

MIXIN_ROUTES = {
    "old-growth forest structure": "노령림 구조",
    "wetland hydrology mosaic": "습지 수문 모자이크",
    "riparian floodplain gradient": "하천변 범람원 구배",
    "intertidal vertical zonation": "조간대 수직 대상",
    "karst surface subsurface drainage": "카르스트 배수 지형",
    "active glacier flow landform": "활동 빙하 지형",
    "aeolian dune wind structure": "풍성사구 과정",
    "volcanic hydrothermal field process": "화산 열수지대",
    "cumulonimbus convective storm structure": "적란운 구조",
    "alpine treeline ecotone gradient": "고산 수목한계 전이지대",
    "mangrove intertidal root sediment system": "맹그로브 조석 뿌리 체계",
    "coral reef cross-shore zonation": "산호초 횡단 대상",
}

PROFILE_ROUTES = {
    "old-growth forest structure": (
        "old_growth_forest_multilayer_deadwood_structure"
    ),
    "wetland hydrology vegetation mosaic": (
        "wetland_hydrology_soil_vegetation_mosaic"
    ),
    "intertidal vertical zonation": "intertidal_high_low_exposure_zonation",
    "karst surface subsurface drainage": (
        "karst_closed_depression_losing_stream_resurgence"
    ),
    "active glacier flow landform": "active_glacier_flow_valley_moraine_system",
    "aeolian dune wind structure": "aeolian_dune_stoss_crest_slipface_transport",
    "cumulonimbus convective storm structure": (
        "cumulonimbus_tower_anvil_precipitation_outflow"
    ),
    "alpine treeline ecotone gradient": (
        "alpine_treeline_forest_krummholz_tundra_gradient"
    ),
}

CANDIDATE_ONLY_TERMS = {
    "riparian floodplain gradient": "하천변 범람원 구배",
    "volcanic hydrothermal field process": "화산 열수지대",
    "mangrove intertidal root sediment system": "맹그로브 조석 뿌리 체계",
    "coral reef cross-shore zonation": "산호초 횡단 대상",
}

NEW_EVIDENCE_IDS = {
    "natural_environment_usfs_old_growth_structure",
    "natural_environment_epa_wetland_hydrology",
    "natural_environment_usgs_riparian_gradient",
    "natural_environment_noaa_intertidal_zonation",
    "natural_environment_usgs_karst_drainage",
    "natural_environment_usgs_glacial_landforms",
    "natural_environment_nps_aeolian_dunes",
    "natural_environment_usgs_hydrothermal_fields",
    "natural_environment_wmo_cumulonimbus_structure",
    "natural_environment_nps_alpine_treeline",
    "natural_environment_noaa_mangrove_roots",
    "natural_environment_noaa_coral_reef_zones",
}


class PhotoNaturalEnvironmentSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.recipes = json.loads(RECIPES_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.profiles = {
            str(profile["id"]): profile
            for profile in cls.registry["profiles"]
        }

    def explain(self, concept: str, seed: int = 17):
        _args, explanations = generate_photo_prompt.resolve_concepts(
            [
                "--seed",
                str(seed),
                "--selection-mode",
                "rule",
                "--emit-candidate-pack",
            ],
            [concept],
        )
        self.assertEqual(len(explanations), 1)
        return explanations[0]

    def hard_visual_matches(self, text: str) -> set[str]:
        rows = [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            }
        ]
        return set(
            prompt_generator.candidate_pack_auto_visual_obligation_matches(
                self.registry,
                rows,
            )
        )

    def test_extension_has_75_decomposed_candidates_and_is_runtime_loaded(self):
        self.assertIn(
            EXTENSION_PATH.name,
            prompt_generator.RESEARCH_EXTENSION_FILENAMES,
        )
        self.assertEqual(
            {
                slot: len(rows)
                for slot, rows in self.extension["slots"].items()
            },
            EXPECTED_SLOT_COUNTS,
        )
        extension_ids: list[str] = []
        for slot, rows in self.extension["slots"].items():
            for row in rows:
                with self.subTest(slot=slot, candidate=row["id"]):
                    extension_ids.append(str(row["id"]))
                    self.assertIn(row["id"], self.by_slot[slot])
                    self.assertTrue(row.get("en"))
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("aliases"))
                    self.assertTrue(row.get("keywords"))
                    self.assertGreaterEqual(
                        len(str(row.get("embedding_text") or "").split()),
                        8,
                    )
                    self.assertIn("natural_environment", row.get("tags", []))
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)
        self.assertEqual(len(extension_ids), 75)
        self.assertEqual(len(extension_ids), len(set(extension_ids)))

    def test_every_extension_candidate_is_owned_by_one_research_mixin(self):
        extension_ids = {
            str(row["id"])
            for rows in self.extension["slots"].values()
            for row in rows
        }
        routed_ids = {
            str(candidate_id)
            for mixin_name in MIXIN_ROUTES.values()
            for candidate_id in self.recipes["mixins"][mixin_name]["set"].values()
            if str(candidate_id) in extension_ids
        }
        self.assertEqual(routed_ids, extension_ids)

    def test_precise_terms_route_one_mixin_with_environment_slots(self):
        for term, mixin_name in MIXIN_ROUTES.items():
            with self.subTest(term=term):
                explanation = self.explain(term)
                self.assertEqual(explanation["applied_mixins"], [mixin_name])
                self.assertGreaterEqual(
                    len(explanation["combined_forced_slots"]),
                    6,
                )

    def test_broad_nature_terms_do_not_activate_new_routes(self):
        new_mixins = set(MIXIN_ROUTES.values())
        hard_profiles = set(PROFILE_ROUTES.values())
        for broad in (
            "forest",
            "숲",
            "wetland",
            "습지",
            "glacier",
            "빙하",
            "desert",
            "사막",
            "volcano",
            "화산",
            "storm",
            "폭풍",
            "reef",
            "산호초",
            "nature",
            "자연환경",
        ):
            with self.subTest(term=broad):
                explanation = self.explain(broad)
                self.assertTrue(
                    set(explanation["applied_mixins"]).isdisjoint(new_mixins)
                )
                self.assertTrue(
                    self.hard_visual_matches(broad).isdisjoint(hard_profiles)
                )

    def test_environment_mixins_do_not_own_human_body_or_identity_slots(self):
        forbidden_slots = {
            "appearance_type",
            "hair_color",
            "hair_style",
            "eye_color",
            "eye_shape",
            "body_type",
            "body_framing",
            "person_origin",
            "species_marker",
            "facial_structure",
            "garment_detail",
            "wardrobe_style",
        }
        for mixin_name in MIXIN_ROUTES.values():
            with self.subTest(mixin=mixin_name):
                mixin = self.recipes["mixins"][mixin_name]
                self.assertGreaterEqual(mixin["soft_min_anchors"], 4)
                self.assertTrue(set(mixin["set"]).isdisjoint(forbidden_slots))
                self.assertTrue(
                    set(mixin.get("anchor_pool") or {}).isdisjoint(
                        forbidden_slots
                    )
                )

    def test_eight_hard_profiles_are_complete_fail_closed_contracts(self):
        self.assertLessEqual(set(PROFILE_ROUTES.values()), set(self.profiles))
        gate_ids: list[str] = []
        for profile_id in PROFILE_ROUTES.values():
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], False)
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 4)
                self.assertEqual(len(components["required_group_ids"]), 4)
                self.assertEqual(len(components["groups"]), 4)
                self.assertEqual(len(profile["required_evidence_fields"]), 4)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertGreaterEqual(len(profile["reject_substitutes"]), 5)
                gate_ids.extend(str(gate["id"]) for gate in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_exact_hard_routes_and_paired_confusion_negatives(self):
        for term, profile_id in PROFILE_ROUTES.items():
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), {profile_id})

        negatives = (
            "generic green forest portrait with uniform trees",
            "ordinary ornamental pond with reeds along one dry edge",
            "rocky beach sunset with no vertical exposure bands",
            "decorative cave interior with stalactites",
            "snowy mountain above a frozen blue lake",
            "symmetric studio sand pile on a seamless backdrop",
            "dark overcast with a lightning graphic and smoke",
            "one twisted tree isolated on a mountain slope",
        )
        hard_profiles = set(PROFILE_ROUTES.values())
        for negative in negatives:
            with self.subTest(negative=negative):
                self.assertTrue(
                    self.hard_visual_matches(negative).isdisjoint(hard_profiles)
                )

    def test_candidate_only_grammars_route_without_hard_pixel_contracts(self):
        for term, mixin_name in CANDIDATE_ONLY_TERMS.items():
            with self.subTest(term=term):
                explanation = self.explain(term)
                self.assertEqual(explanation["applied_mixins"], [mixin_name])
                self.assertGreaterEqual(
                    len(explanation["combined_forced_slots"]),
                    6,
                )
                self.assertEqual(self.hard_visual_matches(term), set())

    def test_research_evidence_is_approved_and_bound_to_current_data(self):
        known_candidates = {
            str(row["id"])
            for rows in self.tags["slots"].values()
            for row in rows
            if isinstance(row, dict) and row.get("id")
        }
        rows = {
            row["id"]: row
            for row in (
                json.loads(line)
                for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
            if row["id"] in NEW_EVIDENCE_IDS
        }
        self.assertEqual(set(rows), NEW_EVIDENCE_IDS)
        for evidence_id, row in rows.items():
            with self.subTest(evidence=evidence_id):
                self.assertEqual(row["domain"], "natural_environment_visual_semantics")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])
                for contract_id in row["affected_contract_ids"]:
                    kind, value = contract_id.split(":", 1)
                    if kind == "visual_obligation":
                        self.assertIn(value, self.profiles)
                    elif kind == "mixin":
                        self.assertIn(value, self.recipes["mixins"])
                    else:
                        self.fail(f"unexpected contract kind: {contract_id}")

    def test_registry_schema_is_valid_before_derived_index_check(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

