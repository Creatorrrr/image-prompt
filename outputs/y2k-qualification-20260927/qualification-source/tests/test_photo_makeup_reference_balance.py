from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "makeup_reference_balance_cases_v1.jsonl"
)
RUN_ROOT = (
    ROOT
    / "artifacts"
    / "photo-runs"
    / "20260831-makeup-reference-five-arm-v1"
)
SOURCE_IMAGE = Path(
    "/Users/chasoik/Downloads/7A2759F9-F4D0-46BC-AB4C-63F661226CD4.jpeg"
)
PROFILE_ID = "restrained_polished_natural_makeup_balance"
PRESET_ID = "restrained_polished_natural_makeup_closeup"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


class PhotoMakeupReferenceBalanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.index = prompt_generator.load_visual_profile_index(INDEX_PATH, cls.registry)
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.profile = next(
            row for row in cls.registry["profiles"] if row["id"] == PROFILE_ID
        )
        cls.preset = next(row for row in cls.tags["presets"] if row["id"] == PRESET_ID)

    def hard_matches(self, text: str) -> set[str]:
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

    def test_profile_is_an_eight_component_fail_closed_pixel_contract(self) -> None:
        components = self.profile["semantics"]["component_semantics"]
        self.assertEqual(components["minimum_component_groups"], 8)
        self.assertEqual(len(components["required_group_ids"]), 8)
        self.assertEqual(len(self.profile["required_evidence_fields"]), 8)
        self.assertEqual(len(self.profile["render_gates"]), 8)
        self.assertEqual(
            {gate["review_scale"] for gate in self.profile["render_gates"]},
            {"thumbnail", "both", "native"},
        )
        runtime = self.profile["runtime_expression"]
        self.assertEqual(runtime["default_mode"], "definition_only")
        self.assertEqual(runtime["prompt_label_terms"], [])
        self.assertTrue(
            set(self.profile["activation"]["exact_terms"])
            <= set(runtime["runtime_forbidden_labels"])
        )
        self.assertTrue(self.profile["reject_substitutes"])

    def test_exact_terms_activate_and_negations_or_confusers_fail_closed(self) -> None:
        cases = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertEqual(
                    self.hard_matches(case["text"]),
                    set(case["expected_profile_ids"]),
                )

    def test_generated_index_is_registry_bound_for_new_profile(self) -> None:
        self.assertIn(PROFILE_ID, self.index["entries"])
        exact_terms = {
            row["term"]
            for row in self.index["exact_lookup"]
            if row["profile_id"] == PROFILE_ID
        }
        self.assertEqual(
            exact_terms,
            set(self.profile["activation"]["exact_terms"]),
        )

    def test_candidate_preset_routes_existing_independent_makeup_axes(self) -> None:
        expected_filters = {
            "complexion_coverage": {
                "sheer_translucent_complexion_coverage",
                "light_selective_complexion_evening",
            },
            "brow_style": {"soft_straight_low_arch_brow"},
            "eyeshadow_style": {"monochrome_diffused_lid_wash"},
            "eye_makeup_line": {"clean_interlash_tightline"},
            "lash_style": {"clean_separated_defined_lashes"},
            "cheek_makeup": {"muted_monochrome_cheek_wash"},
            "lip_color_placement": {"center_saturated_gradient_lip"},
            "lip_finish": {"satin_creme_lip_finish", "natural_balm_lip_sheen"},
            "makeup_wear_state": {"fresh_precise_makeup_application"},
        }
        for slot, expected in expected_filters.items():
            with self.subTest(slot=slot):
                self.assertEqual(set(self.preset["filters"][slot]["ids"]), expected)
                known = {row["id"] for row in self.tags["slots"][slot]}
                self.assertTrue(expected <= known)
        family = self.tags["semantic_policy"]["families"]["inclusive_makeup_beauty"]
        self.assertIn(PRESET_ID, family["preset_policy"]["allow_ids"])
        self.assertIn(
            PRESET_ID,
            self.tags["coherence_rules"]["family_strength"][
                "inclusive_makeup_beauty"
            ]["strong"],
        )

    def test_source_observation_is_hash_bound_and_identity_independent(self) -> None:
        observation = json.loads(
            (RUN_ROOT / "shared" / "source_observation.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(observation["source_path"], str(SOURCE_IMAGE))
        self.assertEqual(
            observation["source_sha256"],
            hashlib.sha256(SOURCE_IMAGE.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            observation["reference_role"],
            "makeup placement color-distribution and surface-finish reference only",
        )
        self.assertIn("original adult subject", observation["identity_policy"])

    def test_five_frozen_cores_are_distinct_and_share_only_the_makeup_contract(self) -> None:
        core_paths = sorted((RUN_ROOT / "arms").glob("arm-*/authorial_core.json"))
        self.assertEqual(len(core_paths), 5)
        cores = [json.loads(path.read_text(encoding="utf-8")) for path in core_paths]
        self.assertEqual(len({core["variation_key"] for core in cores}), 5)
        self.assertEqual(len({core["subject"] for core in cores}), 5)
        self.assertEqual(len({core["setting"] for core in cores}), 5)
        self.assertEqual(len({core["event"] for core in cores}), 5)
        for core in cores:
            with self.subTest(variation_key=core["variation_key"]):
                baseline = core["baseline_prompt_en"]
                for phrase in (
                    "sheer-to-light satin complexion correction leaves fine skin texture and natural tonal variation readable",
                    "softly groomed low-arch brows retain individual hairs",
                    "a neutral taupe wash is deepest at the upper lash line and diffuses through the crease",
                    "a slim interlash line ends in a very short tapered outer extension",
                    "lashes are clean and separated",
                    "a muted rose flush stays soft on the cheeks",
                    "muted rosy-coral lip color is strongest near the inner center",
                    "Eye, cheek, and lip contrast remain mutually restrained so the complexion leads the hierarchy",
                    "the subject has an original facial identity",
                ):
                    self.assertIn(phrase, baseline)
                self.assertEqual(
                    set(core["intent_lock"]["locked_dimensions"]),
                    {"concept", "subject", "event", "appearance", "reference_use"},
                )
                self.assertGreaterEqual(len(core["intent_lock"]["open_dimensions"]), 2)

    def test_semantics_do_not_encode_demographic_or_value_inference(self) -> None:
        payload = json.dumps(
            {"profile": self.profile, "preset": self.preset},
            ensure_ascii=False,
        ).casefold()
        for forbidden in (
            "healthy",
            "youthful",
            "attractive",
            "flattering",
            "ethnicity",
            "for women",
            "for men",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, payload)


if __name__ == "__main__":
    unittest.main()
