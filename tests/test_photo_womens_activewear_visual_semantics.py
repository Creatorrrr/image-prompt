from __future__ import annotations

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
EVIDENCE_PATH = ROOT / "docs" / "research-evidence" / "photo-prompt" / "research_evidence.jsonl"
CASES_PATH = ROOT / "tests" / "fixtures" / "photo_prompt" / "womens_activewear_pixel_test_cases_v1.jsonl"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


PROFILE_IDS = {
    "racerback_sports_bra_strap_convergence",
    "longline_sports_bra_extended_underband",
    "encapsulated_sports_bra_separate_cups",
    "two_in_one_running_shorts_dual_layer",
    "split_running_shorts_side_opening",
    "active_skort_outer_skirt_inner_shorts",
    "exercise_dress_integrated_short_liner",
    "cycling_bib_shorts_strap_pad_continuity",
    "unitard_upper_crotch_leg_continuity",
    "stirrup_leggings_underfoot_loop",
}

EXPECTED_CANDIDATES = {
    "garment_detail": {
        "racerback_strap_yoke_convergence",
        "crossback_strap_intersection",
        "sports_bra_extended_longline_underband",
        "separate_molded_cup_encapsulation",
        "bra_tank_internal_shelf_band",
        "leggings_crossover_front_waistband",
        "leggings_v_back_waistband",
        "leggings_center_back_scrunch_channel",
        "leggings_absent_center_front_seam",
        "two_in_one_short_shell_inner_tight",
        "brief_lined_running_short_inner_brief",
        "split_running_short_overlap_opening",
        "exercise_dress_outer_skirt_inner_shorts",
        "cycling_bib_shoulder_strap_pad_continuity",
        "stirrup_legging_underfoot_loop",
        "thumbhole_cuff_hand_opening",
        "flat_multithread_activewear_seam",
        "low_profile_bonded_garment_edge",
        "athletic_gusset_panel",
        "integrated_mesh_or_perforated_panel",
    },
    "silhouette_proportion": {
        "seven_eighth_legging_ankle_landmark",
        "capri_legging_mid_calf_landmark",
        "biker_short_thigh_knee_landmark",
        "flare_legging_knee_to_hem_expansion",
        "high_rise_waist_navel_relation",
    },
    "surface_material": {
        "body_mapped_circular_knit_zones",
        "athletic_mesh_open_structure",
        "athletic_ripstop_grid_surface",
        "brushed_peached_matte_nap_surface",
    },
    "wardrobe_style": {
        "athletic_unitard_continuous_one_piece",
        "running_split_short_racerback_tank_ensemble",
        "studio_bra_tank_seven_eighth_legging_ensemble",
        "court_skort_racerback_top_ensemble",
        "exercise_dress_integrated_liner_ensemble",
        "cycling_jersey_bib_short_ensemble",
    },
}

REUSED_CANDIDATES = {
    "garment_detail": {"skort_outer_panel_inner_shorts"},
    "wardrobe_style": {"covered_track_jacket_training_set"},
    "surface_material": {"rib_knit_stretch_recovery_surface"},
}


class PhotoWomensActivewearVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.tags = json.loads(TAGS_PATH.read_text(encoding="utf-8"))
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"]}
        cls.candidates = {
            slot: {row["id"]: row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.pixel_cases = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

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

    def test_profiles_are_complete_five_group_pixel_contracts(self) -> None:
        self.assertTrue(PROFILE_IDS <= set(self.profiles))
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], False)
                self.assertIs(
                    profile["activation"]["semantic_discovery_requires_component_evidence"],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(len(components["groups"]), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
                self.assertEqual(len(profile["evidence_requirements"]), 5)
                self.assertEqual(len(profile["render_gates"]), 5)
                self.assertEqual(
                    {gate["review_scale"] for gate in profile["render_gates"]},
                    {"thumbnail", "both", "native"},
                )
                self.assertEqual(len(profile["reject_substitutes"]), 5)

    def test_exact_terms_route_to_one_profile(self) -> None:
        cases = {
            "adult athlete in a racerback sports bra": "racerback_sports_bra_strap_convergence",
            "롱라인 스포츠브라를 입은 성인 운동선수": "longline_sports_bra_extended_underband",
            "studio portrait of an encapsulation sports bra": "encapsulated_sports_bra_separate_cups",
            "trail runner wearing 2-in-1 running shorts": "two_in_one_running_shorts_dual_layer",
            "side view of split running shorts": "split_running_shorts_side_opening",
            "adult athlete wearing an athletic skort": "active_skort_outer_skirt_inner_shorts",
            "exercise dress with built-in shorts in motion": "exercise_dress_integrated_short_liner",
            "cyclist in cycling bib shorts": "cycling_bib_shorts_strap_pad_continuity",
            "full-body athletic unitard editorial": "unitard_upper_crotch_leg_continuity",
            "barefoot studio portrait in stirrup leggings": "stirrup_leggings_underfoot_loop",
        }
        for text, expected_id in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_id})

    def test_broad_performance_and_marketing_terms_do_not_create_hard_profiles(self) -> None:
        cases = (
            "women's activewear editorial",
            "generic sportswear and athleisure",
            "high support workout outfit",
            "compression leggings",
            "moisture-wicking quick-dry gymwear",
            "four-way stretch seamless leggings",
            "squat-proof and UPF training clothes",
            "buttery-soft sculpting yoga set",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_confounds_fail_closed(self) -> None:
        cases = (
            "a crossback bra whose two straps form one X",
            "a cropped tank hidden behind high-rise leggings",
            "brief-lined shorts with no longer inner-short layer",
            "dolphin shorts with a curved piped hem and no open side seam",
            "an ordinary dress worn above separate biker shorts",
            "matching top and leggings divided by a waistband gap",
            "same-color socks held by shoe straps",
            "ordinary suspenders clipped onto biker shorts",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_candidates_are_single_slot_owned_and_semantically_decomposed(self) -> None:
        expected = set().union(*EXPECTED_CANDIDATES.values())
        self.assertEqual(len(expected), 35)
        for slot, candidate_ids in EXPECTED_CANDIDATES.items():
            self.assertTrue(candidate_ids <= set(self.candidates[slot]))
            for candidate_id in candidate_ids:
                with self.subTest(slot=slot, candidate_id=candidate_id):
                    candidate = self.candidates[slot][candidate_id]
                    self.assertTrue(candidate.get("aliases"))
                    self.assertTrue(candidate.get("keywords"))
                    self.assertGreaterEqual(len(candidate.get("embedding_text", "").split()), 8)
                    self.assertIn("activewear", candidate.get("tags", []))
        owner_counts = {
            candidate_id: sum(
                candidate_id in candidates
                for candidates in self.candidates.values()
            )
            for candidate_id in expected
        }
        self.assertEqual(set(owner_counts.values()), {1})
        for slot, candidate_ids in REUSED_CANDIDATES.items():
            self.assertTrue(candidate_ids <= set(self.candidates[slot]))

    def test_embedding_only_component_paraphrase_remains_optional(self) -> None:
        target_id = "racerback_sports_bra_strap_convergence"
        component_context = "; ".join(
            group["any_terms"][0]
            for group in self.profiles[target_id]["semantics"]["component_semantics"]["groups"]
        )
        vectors = {
            profile["id"]: ([1.0, 0.0] if profile["id"] == target_id else [0.0, 1.0])
            for profile in self.registry["profiles"]
        }
        fake_index = prompt_generator.build_visual_profile_index_payload(
            self.registry,
            vectors=vectors,
            dimensions=2,
        )
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "authorial_core_interpretation",
                    "text": component_context,
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text="two shoulder paths merge into one central back yoke",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(row for row in resolution["hits"] if row["profile_id"] == target_id)
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_registry_index_contains_all_exact_terms_after_rebuild(self) -> None:
        index = prompt_generator.load_visual_profile_index(INDEX_PATH, self.registry)
        exact_by_profile = {
            profile_id: {
                row["term"]
                for row in index["exact_lookup"]
                if row["profile_id"] == profile_id
            }
            for profile_id in PROFILE_IDS
        }
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                self.assertIn(profile_id, index["entries"])
                self.assertEqual(
                    exact_by_profile[profile_id],
                    set(self.profiles[profile_id]["activation"]["exact_terms"]),
                )

    def test_research_evidence_is_approved_and_candidate_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        activewear_rows = [row for row in rows if row["id"].startswith("activewear_")]
        self.assertGreaterEqual(len(activewear_rows), 11)
        known_candidates = {
            candidate_id
            for candidates in self.candidates.values()
            for candidate_id in candidates
        }
        for row in activewear_rows:
            with self.subTest(evidence_id=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["status"], "approved")
                self.assertEqual(row["domain"], "womens_activewear_visual_semantics")
                self.assertTrue(row["source_url"].startswith("https://"))
                self.assertTrue(set(row["candidate_ids"]) <= known_candidates)
                self.assertTrue(row["abstracted_dimensions"])
                self.assertTrue(row["research_limitations"])
                self.assertTrue(row["reuse_note"])

    def test_five_arm_cases_bind_profile_gates_and_reference(self) -> None:
        self.assertEqual(len(self.pixel_cases), 5)
        self.assertEqual(len({row["arm_id"] for row in self.pixel_cases}), 5)
        self.assertEqual(len({row["profile_id"] for row in self.pixel_cases}), 5)
        for row in self.pixel_cases:
            with self.subTest(arm_id=row["arm_id"]):
                self.assertIn(row["profile_id"], PROFILE_IDS)
                profile = self.profiles[row["profile_id"]]
                self.assertIs(row["randomized_complex_concept_required"], True)
                self.assertTrue(row["randomized_complex_concept"])
                self.assertEqual(row["reference"]["role"], "appearance_reference")
                self.assertEqual(
                    row["reference"]["sha256"],
                    "3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea",
                )
                self.assertIn("not biometric identity verification", row["reference"]["boundary"])
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    {gate["id"] for gate in profile["render_gates"]},
                )
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                self.assertEqual(row["verdict_rule"]["blocked_or_no_image"], "unscored")


if __name__ == "__main__":
    unittest.main()
