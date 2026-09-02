from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402


class PhotoVisualProfileRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.index = prompt_generator.load_visual_profile_index(
            INDEX_PATH,
            cls.registry,
        )

    def fake_index(self) -> dict:
        vectors = {
            str(profile["id"]): (
                [1.0, 0.0]
                if profile["id"] == "inner_thigh_negative_space"
                else [0.0, 1.0]
            )
            for profile in self.registry["profiles"]
        }
        return prompt_generator.build_visual_profile_index_payload(
            self.registry,
            vectors=vectors,
            dimensions=2,
        )

    @staticmethod
    def core(source: str) -> dict:
        return prompt_generator.normalize_authorial_core(
            {
                "contract_version": "photo-authorial-core/v1",
                "provenance": "agent_prepack",
                "source_request": source,
                "interpreted_intent": (
                    "An adult fashion portrait emphasizing an attractive narrow pocket of "
                    "background between close upper inner-thigh contours"
                ),
                "subject": "one self-possessed adult woman",
                "setting": "a quiet neutral fashion studio",
                "event": "she keeps her legs close in a balanced standing pose",
                "visual_priorities": [
                    "attractive inner-thigh negative space",
                    "clear close-leg geometry",
                ],
                "baseline_prompt_en": (
                    "A self-possessed adult woman stands in a quiet neutral fashion studio, "
                    "keeping her legs close while a narrow pocket of background between the "
                    "actual upper inner-thigh contours becomes deliberate focal geometry."
                ),
                "user_definitions": [],
                "interpretation_provenance": [
                    {
                        "term": "허벅지 사이의 공간",
                        "source_text": "허벅지 사이의 공간",
                        "basis": "request_context",
                        "resolution": (
                            "a visually attractive background opening bounded by close upper inner thighs"
                        ),
                        "sources": [],
                    }
                ],
                "unresolved_ambiguities": [],
                "user_exclusions": [],
                "style": {
                    "domain": "general_photo",
                    "family": "restrained adult fashion editorial",
                    "evidence": ["clean soft light", "balanced close-leg framing"],
                },
                "variation_key": "visual-profile-retrieval-test",
            }
        )

    def test_index_is_registry_bound_and_separates_exact_from_semantic_text(self):
        exact_terms = {
            row["term"]
            for row in self.index["exact_lookup"]
            if row["profile_id"] == "inner_thigh_negative_space"
        }
        self.assertIn("절대공역", exact_terms)
        self.assertNotIn("허벅지 사이 공간", exact_terms)
        self.assertNotIn("허벅지 사이의 공간", exact_terms)
        semantic_text = self.index["entries"]["inner_thigh_negative_space"]["text"]
        self.assertIn("허벅지 사이의 공간", semantic_text)
        contained_terms = {
            row["term"]
            for row in self.index["exact_lookup"]
            if row["profile_id"] == "contained_affect_self_presentation"
        }
        self.assertEqual(contained_terms, {"menhera", "멘헤라", "メンヘラ"})
        self.assertIn(
            "controlled social presentation",
            self.index["entries"]["contained_affect_self_presentation"][
                "text"
            ],
        )
        reality_terms = {
            row["term"]
            for row in self.index["exact_lookup"]
            if row["profile_id"] == "diegetic_reality_invariant_failure"
        }
        self.assertIn("현실 오류", reality_terms)
        self.assertNotIn(
            "the world itself obeys one broken rule while the photograph stays clean",
            reality_terms,
        )
        self.assertIn(
            "the world itself obeys one broken rule while the photograph stays clean",
            self.index["entries"]["diegetic_reality_invariant_failure"]["text"],
        )
        self.assertEqual(self.index["retrieval_policy"]["minimum_similarity"], 0.7)

        changed = copy.deepcopy(self.registry)
        changed["profiles"][0]["semantics"]["definition"] += " changed"
        with self.assertRaisesRegex(ValueError, "registry_sha256"):
            prompt_generator.validate_visual_profile_index_metadata(
                self.index,
                changed,
            )

    def test_composition_relation_embedding_lane_remains_optional(self):
        profile_ids = [
            "third_grid_focal_anchor_relation",
            "centered_primary_anchor_relation",
            "axial_bilateral_symmetry_relation",
            "asymmetric_counterbalance_relation",
            "leading_line_target_continuity",
            "look_motion_room_direction_relation",
            "subject_field_negative_space_relation",
            "frame_within_frame_boundary_relation",
            "three_plane_depth_chain",
            "pattern_break_focal_exception",
            "primary_secondary_figure_ground_hierarchy",
            "peak_action_event_phase",
        ]
        dimensions = len(profile_ids)
        uniform = [dimensions ** -0.5] * dimensions
        vectors = {
            str(profile["id"]): list(uniform)
            for profile in self.registry["profiles"]
        }
        for index, profile_id in enumerate(profile_ids):
            vector = [0.0] * dimensions
            vector[index] = 1.0
            vectors[profile_id] = vector
        fake_index = prompt_generator.build_visual_profile_index_payload(
            self.registry,
            vectors=vectors,
            dimensions=dimensions,
        )
        profiles = {profile["id"]: profile for profile in self.registry["profiles"]}

        for index, profile_id in enumerate(profile_ids):
            with self.subTest(profile_id=profile_id):
                query_vector = [0.0] * dimensions
                query_vector[index] = 1.0
                resolution = prompt_generator.resolve_visual_profile_hits(
                    self.registry,
                    [
                        {
                            "source": "authorial_core_interpretation",
                            "text": profiles[profile_id]["semantics"][
                                "paraphrase_examples"
                            ][0],
                            "polarity": "advisory",
                        }
                    ],
                    visual_profile_index=fake_index,
                    query_vector=query_vector,
                    adult_context=True,
                )
                hit = next(
                    row
                    for row in resolution["hits"]
                    if row["profile_id"] == profile_id
                )
                self.assertEqual(hit["match_basis"], "embedding")
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])

    def test_embedding_only_paraphrase_projects_optional_candidate_from_one_resolution(self):
        source = "허벅지 사이의 공간이 매력적인 여성의 패션 사진"
        core = self.core(source)
        fake_index = self.fake_index()
        result = {
            "provenance": {
                "prompt_id": "embedding-only-pack",
                "concept_lock": [source],
                "authorial_core": core,
            }
        }
        data = {
            prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY: self.registry,
            prompt_generator.VISUAL_PROFILE_INDEX_DATA_KEY: fake_index,
            prompt_generator.VISUAL_PROFILE_QUERY_VECTORS_DATA_KEY: {
                "embedding-only-pack": [1.0, 0.0]
            },
        }
        resolution = prompt_generator.candidate_pack_resolve_visual_profiles(
            data,
            result,
            {},
            None,
        )
        hit = next(
            row
            for row in resolution["hits"]
            if row["profile_id"] == "inner_thigh_negative_space"
        )
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

        obligations = prompt_generator.candidate_pack_visual_obligations(
            data,
            result,
            {},
            None,
            resolution,
        )
        self.assertIsNone(obligations)
        concepts = prompt_generator.candidate_pack_visual_concept_candidates(
            data,
            result,
            {},
            None,
            obligations,
            resolution,
        )
        self.assertIsNotNone(concepts)
        candidate = concepts["candidates"][0]
        self.assertEqual(candidate["id"], "visual-concept:inner_thigh_negative_space")
        self.assertNotIn("score", candidate)
        self.assertNotIn("matched_terms", candidate)
        clarification = prompt_generator.candidate_pack_semantic_clarification(
            data,
            result,
            {},
            obligations,
            concepts,
            resolution,
        )
        profile_row = next(
            row
            for row in clarification["candidates"]
            if row.get("profile_id") == "inner_thigh_negative_space"
        )
        self.assertEqual(profile_row["applicability"]["status"], "eligible")
        self.assertFalse(profile_row["required_in_final_prompt"])

    def test_bm25f_only_paraphrase_is_optional_and_cannot_create_an_obligation(self):
        source = "허벅지 사이의 공간이 매력적인 여성의 패션 사진"
        fake_index = self.fake_index()
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "authorial_core_interpretation",
                    "text": "an adult fashion portrait with close-leg negative space",
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text=source,
            query_fields={
                "active_request": source,
                "interpreted_intent": "매력적인 허벅지 사이 공간",
            },
            adult_context=True,
        )
        hit = next(
            row
            for row in resolution["hits"]
            if row["profile_id"] == "inner_thigh_negative_space"
        )
        self.assertEqual(hit["match_basis"], "bm25f")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])
        self.assertTrue(resolution["bm25f_evaluated"])
        self.assertFalse(resolution["embedding_evaluated"])

    def test_bm25f_and_embedding_fuse_without_promoting_to_hard(self):
        source = "허벅지 사이의 공간이 매력적인 여성의 패션 사진"
        fake_index = self.fake_index()
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "authorial_core_interpretation",
                    "text": "an adult fashion portrait with close-leg negative space",
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text=source,
            query_fields={"active_request": source},
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        hit = next(
            row
            for row in resolution["hits"]
            if row["profile_id"] == "inner_thigh_negative_space"
        )
        self.assertEqual(hit["match_basis"], "bm25f+embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_exact_hit_stays_hard_while_negation_and_user_definition_cannot_resurrect(self):
        fake_index = self.fake_index()
        fake_index["entries"]["deliberate_underarm_salience"]["vector"] = [
            0.8,
            0.6,
        ]
        exact_rows = [
            {
                "source": "concept_lock",
                "text": "성인 여성의 절대공역 사진",
                "polarity": "required",
            },
            {
                "source": "authorial_core_interpretation",
                "text": "close inner-thigh focal geometry on an adult woman",
                "polarity": "advisory",
            },
        ]
        exact = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            exact_rows,
            visual_profile_index=fake_index,
            query_text="성인 여성의 절대공역 사진",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        exact_hit = next(
            row
            for row in exact["hits"]
            if row["profile_id"] == "inner_thigh_negative_space"
        )
        self.assertEqual(exact_hit["match_basis"], "exact")
        self.assertTrue(exact_hit["hard_eligible"])
        self.assertFalse(exact_hit["optional_eligible"])
        self.assertNotIn(
            "deliberate_underarm_salience",
            {row["profile_id"] for row in exact["hits"]},
        )

        aligned = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            exact_rows,
            visual_profile_index=fake_index,
            query_text="성인 여성의 절대공역 사진",
            query_vector=[1.0, 0.0],
            user_definitions=[
                {
                    "term": "절대공역",
                    "source_text": "절대공역",
                    "interpreted_meaning": (
                        "true negative space bounded by close upper inner thigh contours"
                    ),
                    "prompt_evidence": (
                        "a narrow opening between close upper inner-thigh contours"
                    ),
                }
            ],
            adult_context=True,
        )
        aligned_hit = next(
            row
            for row in aligned["hits"]
            if row["profile_id"] == "inner_thigh_negative_space"
        )
        self.assertEqual(aligned_hit["applicability_status"], "required")
        self.assertTrue(aligned_hit["hard_eligible"])

        negated = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "concept_lock",
                    "text": "성인 여성의 절대공역 없는 사진",
                    "polarity": "required",
                }
            ],
            visual_profile_index=fake_index,
            query_text="성인 여성의 절대공역 없는 사진",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        self.assertNotIn(
            "inner_thigh_negative_space",
            {row["profile_id"] for row in negated["hits"]},
        )

        overridden = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            exact_rows,
            visual_profile_index=fake_index,
            query_text="성인 여성의 절대공역 사진",
            query_vector=[1.0, 0.0],
            user_definitions=[
                {
                    "term": "절대공역",
                    "source_text": "절대공역",
                    "interpreted_meaning": "the requester's unrelated private definition",
                }
            ],
            adult_context=True,
        )
        override_hit = next(
            row
            for row in overridden["hits"]
            if row["profile_id"] == "inner_thigh_negative_space"
        )
        self.assertEqual(
            override_hit["applicability_status"],
            "user_definition_override",
        )
        self.assertFalse(override_hit["hard_eligible"])
        self.assertFalse(override_hit["optional_eligible"])

    def test_adult_woman_context_is_allowing_not_blocking(self):
        for text in (
            "a fashion portrait of one woman",
            "여성 한 명의 패션 사진",
        ):
            with self.subTest(text=text):
                self.assertTrue(
                    prompt_generator.candidate_pack_visual_obligation_adult_context(
                        [
                            {
                                "source": "concept_lock",
                                "text": text,
                                "polarity": "required",
                            }
                        ],
                        None,
                    )
                )

    def test_sensitive_contained_affect_term_requires_visual_character_context(self):
        eligible_rows = [
            {
                "source": "concept_lock",
                "text": "성인 고스로리 멘헤라 캐릭터 사진",
                "polarity": "required",
            },
            {
                "source": "authorial_core_interpretation",
                "text": (
                    "an adult character portrait with a controlled social surface, "
                    "contained affect leak, and interrupted regulating gesture"
                ),
                "polarity": "advisory",
            },
        ]
        eligible = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            eligible_rows,
            visual_profile_index=self.index,
            adult_context=True,
        )
        hit = next(
            row
            for row in eligible["hits"]
            if row["profile_id"] == "contained_affect_self_presentation"
        )
        self.assertEqual(hit["applicability_status"], "required")
        self.assertTrue(hit["hard_eligible"])

        for interpretation in (
            "explain the word history and dictionary entry",
            "a technical terminology note with no character or portrait",
        ):
            with self.subTest(interpretation=interpretation):
                mismatch = prompt_generator.resolve_visual_profile_hits(
                    self.registry,
                    [
                        {
                            "source": "concept_lock",
                            "text": "멘헤라",
                            "polarity": "required",
                        },
                        {
                            "source": "authorial_core_interpretation",
                            "text": interpretation,
                            "polarity": "advisory",
                        },
                    ],
                    visual_profile_index=self.index,
                    adult_context=True,
                )
                mismatch_hit = next(
                    row
                    for row in mismatch["hits"]
                    if row["profile_id"]
                    == "contained_affect_self_presentation"
                )
                self.assertEqual(
                    mismatch_hit["applicability_status"],
                    "context_mismatch",
                )
                self.assertFalse(mismatch_hit["hard_eligible"])

    def test_embedding_score_is_positive_context_proof_but_shared_negatives_still_win(self):
        vectors = {
            str(profile["id"]): (
                [0.0, 1.0]
                if profile["id"] == "embodied_corruption_transition"
                else [1.0, 0.0]
            )
            for profile in self.registry["profiles"]
        }
        fake_index = prompt_generator.build_visual_profile_index_payload(
            self.registry,
            vectors=vectors,
            dimensions=2,
        )
        semantic = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "concept_lock",
                    "text": (
                        "옛 밝은 정체성과 어두운 현재 상태가 몸 위 경계에서 "
                        "동시에 보이는 진행 중인 성인 캐릭터 변신"
                    ),
                    "polarity": "required",
                },
                {
                    "source": "authorial_core_interpretation",
                    "text": (
                        "former bright identity and a dark present state remain visible "
                        "across an unfinished boundary on the adult character"
                    ),
                    "polarity": "advisory",
                },
            ],
            visual_profile_index=fake_index,
            query_text="semantic transformation paraphrase",
            query_vector=[0.0, 1.0],
            adult_context=True,
        )
        semantic_hit = next(
            row
            for row in semantic["hits"]
            if row["profile_id"] == "embodied_corruption_transition"
        )
        self.assertEqual(semantic_hit["match_basis"], "embedding")
        self.assertTrue(semantic_hit["optional_eligible"])

        exact_mismatch = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "concept_lock",
                    "text": "adult corruption fashion portrait",
                    "polarity": "required",
                },
                {
                    "source": "authorial_core_interpretation",
                    "text": "a composed ordinary fashion model with no character transformation",
                    "polarity": "advisory",
                },
            ],
            visual_profile_index=fake_index,
            query_text="ordinary fashion",
            query_vector=[0.0, 1.0],
            adult_context=True,
        )
        mismatch_hit = next(
            row
            for row in exact_mismatch["hits"]
            if row["profile_id"] == "embodied_corruption_transition"
        )
        self.assertEqual(mismatch_hit["applicability_status"], "context_mismatch")
        self.assertFalse(mismatch_hit["hard_eligible"])
        self.assertFalse(mismatch_hit["optional_eligible"])

    def test_relation_profile_requires_component_evidence_for_semantic_discovery(self):
        vectors = {
            str(profile["id"]): (
                [1.0, 0.0]
                if profile["id"] == "yandere_affection_control_relation"
                else [0.0, 1.0]
            )
            for profile in self.registry["profiles"]
        }
        fake_index = prompt_generator.build_visual_profile_index_payload(
            self.registry,
            vectors=vectors,
            dimensions=2,
        )

        unrelated = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "concept_lock",
                    "text": (
                        "An adult woman smiles in a blue-sea reality error portrait"
                    ),
                    "polarity": "required",
                },
                {
                    "source": "authorial_core_interpretation",
                    "text": (
                        "Her face and reflection diverge under one spatial rule, with "
                        "no affection target, boundary action, or relationship consequence"
                    ),
                    "polarity": "advisory",
                },
            ],
            visual_profile_index=fake_index,
            query_text="adult woman warm smile uncanny face reality error",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        self.assertNotIn(
            "yandere_affection_control_relation",
            {row["profile_id"] for row in unrelated["hits"]},
        )
        self.assertIn(
            "diegetic_reality_invariant_failure",
            {row["profile_id"] for row in unrelated["hits"]},
        )

        related = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "authorial_core_interpretation",
                    "text": (
                        "Devoted care toward the same adult counterpart takes control "
                        "of the schedule, and that counterpart's choice has visibly "
                        "narrowed."
                    ),
                    "polarity": "advisory",
                }
            ],
            visual_profile_index=fake_index,
            query_text="possessive care relation",
            query_vector=[1.0, 0.0],
            adult_context=True,
        )
        relation_hit = next(
            row
            for row in related["hits"]
            if row["profile_id"] == "yandere_affection_control_relation"
        )
        self.assertEqual(relation_hit["match_basis"], "embedding")
        self.assertTrue(relation_hit["optional_eligible"])

    def test_role_and_garment_exact_terms_require_their_visual_context(self):
        positives = {
            "aircraft_pilot_operation": (
                "파일럿",
                "adult aircraft pilot in an aircraft cockpit with flight controls, instrument panel, and runway state",
            ),
            "cabin_crew_safety_role": (
                "스튜어디스",
                "adult cabin crew in an aircraft cabin performing a cabin-safety check at the emergency exit",
            ),
            "school_uniform_institutional_system": (
                "교복",
                "coordinated uniform garments with a uniform blazer, uniform shirt, and one school clothing system",
            ),
            "one_piece_dress_construction": (
                "원피스",
                "dress garment with bodice-to-hem continuity, neckline and skirt, closure, and dress drape",
            ),
            "sheer_garment_optical_layering": (
                "시스루",
                "translucent textile and sheer fabric layer over an opaque underlayer with visible weave and edge",
            ),
            "military_uniform_duty_system": (
                "군복",
                "military garment system with service-uniform components aligned to one military duty context",
            ),
            "wearable_protective_armor_system": (
                "갑옷",
                "human-scale armor with worn protective plates, articulated armor joints, and plate-and-mail underlayers",
            ),
            "commercial_appeal_revealing_armor": (
                "상업적인 방어력 높은 갑옷",
                "clearly adult original fantasy character in deliberately high-exposure armor with opaque intimate coverage",
            ),
        }
        for expected_id, (term, interpretation) in positives.items():
            with self.subTest(expected_id=expected_id):
                resolution = prompt_generator.resolve_visual_profile_hits(
                    self.registry,
                    [
                        {
                            "source": "concept_lock",
                            "text": term,
                            "polarity": "required",
                        },
                        {
                            "source": "authorial_core_interpretation",
                            "text": interpretation,
                            "polarity": "advisory",
                        },
                    ],
                    visual_profile_index=self.index,
                    adult_context=True,
                )
                hard_ids = {
                    hit["profile_id"]
                    for hit in resolution["hits"]
                    if hit["hard_eligible"]
                }
                self.assertIn(expected_id, hard_ids)
                if expected_id == "commercial_appeal_revealing_armor":
                    self.assertNotIn("wearable_protective_armor_system", hard_ids)

        negatives = {
            "aircraft_pilot_operation": (
                "파일럿 프로젝트",
                "trial rollout and experimental program, not an aircraft operation",
            ),
            "cabin_crew_safety_role": (
                "열차 승무원",
                "rail carriage and train-platform passenger service",
            ),
            "school_uniform_institutional_system": (
                "교복",
                "a school dress-code essay about uniform cost policy, with no garment image",
            ),
            "one_piece_dress_construction": (
                "원피스 애니",
                "an anime franchise and straw-hat pirate crew",
            ),
            "sheer_garment_optical_layering": (
                "시스루뱅",
                "a bangs hairstyle and hair fringe",
            ),
            "military_uniform_duty_system": (
                "군복",
                "a camouflage fashion trend and civilian streetwear editorial",
            ),
            "wearable_protective_armor_system": (
                "갑옷",
                "vehicle hull and tank chassis protection",
            ),
            "commercial_appeal_revealing_armor": (
                "상업적 방어력",
                "actual battlefield protection with a real ballistic rating and full coverage armor",
            ),
        }
        for blocked_id, (term, interpretation) in negatives.items():
            with self.subTest(blocked_id=blocked_id):
                resolution = prompt_generator.resolve_visual_profile_hits(
                    self.registry,
                    [
                        {
                            "source": "concept_lock",
                            "text": term,
                            "polarity": "required",
                        },
                        {
                            "source": "authorial_core_interpretation",
                            "text": interpretation,
                            "polarity": "advisory",
                        },
                    ],
                    visual_profile_index=self.index,
                    adult_context=True,
                )
                hard_ids = {
                    hit["profile_id"]
                    for hit in resolution["hits"]
                    if hit["hard_eligible"]
                }
                self.assertNotIn(blocked_id, hard_ids)

    def test_commercial_defense_glossary_honors_alignment_override_and_negation(self):
        rows = [
            {
                "source": "concept_lock",
                "text": "상업적인 방어력 높은 갑옷",
                "polarity": "required",
            },
            {
                "source": "authorial_core_interpretation",
                "text": (
                    "an adult original fantasy character wearing deliberately high-exposure "
                    "armor with opaque intimate coverage and visible armor attachments"
                ),
                "polarity": "advisory",
            },
        ]
        aligned = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            rows,
            visual_profile_index=self.index,
            user_definitions=[
                {
                    "term": "상업적인 방어력",
                    "source_text": "상업적인 방어력 높은 갑옷",
                    "interpreted_meaning": (
                        "unmistakably adult original fantasy character in a deliberately "
                        "high-exposure armor design with stable opaque chest and pelvis "
                        "coverage and visible straps, buckles, and structural connections"
                    ),
                }
            ],
            adult_context=True,
        )
        aligned_hit = next(
            hit
            for hit in aligned["hits"]
            if hit["profile_id"] == "commercial_appeal_revealing_armor"
        )
        self.assertEqual(aligned_hit["applicability_status"], "required")
        self.assertTrue(aligned_hit["hard_eligible"])

        overridden = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            rows,
            visual_profile_index=self.index,
            user_definitions=[
                {
                    "term": "상업적인 방어력",
                    "source_text": "상업적인 방어력 높은 갑옷",
                    "interpreted_meaning": "an unrelated retail pricing score",
                }
            ],
            adult_context=True,
        )
        override_hit = next(
            hit
            for hit in overridden["hits"]
            if hit["profile_id"] == "commercial_appeal_revealing_armor"
        )
        self.assertEqual(
            override_hit["applicability_status"],
            "user_definition_override",
        )
        self.assertFalse(override_hit["hard_eligible"])
        self.assertFalse(override_hit["optional_eligible"])

        negated = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
                {
                    "source": "concept_lock",
                    "text": "상업적인 방어력 없는 성인 판타지 갑옷",
                    "polarity": "required",
                },
                {
                    "source": "authorial_core_interpretation",
                    "text": "adult original fantasy character with ordinary covered armor",
                    "polarity": "advisory",
                },
            ],
            visual_profile_index=self.index,
            adult_context=True,
        )
        self.assertNotIn(
            "commercial_appeal_revealing_armor",
            {
                hit["profile_id"]
                for hit in negated["hits"]
                if hit["hard_eligible"] or hit["optional_eligible"]
            },
        )

    def test_new_profile_embedding_paraphrases_remain_optional_only(self):
        paraphrases = {
            profile["id"]: profile["semantics"]["paraphrase_examples"][0]
            for profile in self.registry["profiles"]
            if profile["id"]
            in {
                "aircraft_pilot_operation",
                "cabin_crew_safety_role",
                "school_uniform_institutional_system",
                "one_piece_dress_construction",
                "sheer_garment_optical_layering",
                "military_uniform_duty_system",
                "wearable_protective_armor_system",
                "commercial_appeal_revealing_armor",
            }
        }
        self.assertEqual(len(paraphrases), 8)
        for expected_id, paraphrase in paraphrases.items():
            with self.subTest(expected_id=expected_id):
                vectors = {
                    profile["id"]: (
                        [1.0, 0.0]
                        if profile["id"] == expected_id
                        else [0.0, 1.0]
                    )
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
                            "text": paraphrase,
                            "polarity": "advisory",
                        }
                    ],
                    visual_profile_index=fake_index,
                    query_text=paraphrase,
                    query_vector=[1.0, 0.0],
                    adult_context=True,
                )
                hit = next(
                    hit
                    for hit in resolution["hits"]
                    if hit["profile_id"] == expected_id
                )
                self.assertEqual(hit["match_basis"], "embedding")
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])


if __name__ == "__main__":
    unittest.main()
