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
        self.assertEqual(self.index["retrieval_policy"]["minimum_similarity"], 0.7)

        changed = copy.deepcopy(self.registry)
        changed["profiles"][0]["semantics"]["definition"] += " changed"
        with self.assertRaisesRegex(ValueError, "registry_sha256"):
            prompt_generator.validate_visual_profile_index_metadata(
                self.index,
                changed,
            )

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


if __name__ == "__main__":
    unittest.main()
