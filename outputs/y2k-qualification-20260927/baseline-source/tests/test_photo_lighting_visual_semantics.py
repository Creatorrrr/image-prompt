from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
ASSETS_DIR = SKILL_DIR / "assets"
REGISTRY_PATH = ASSETS_DIR / "photo_prompt_visual_obligations.json"
INDEX_PATH = ASSETS_DIR / "photo_prompt_visual_profile_index.json"
SEMANTIC_INDEX_PATH = ASSETS_DIR / "photo_prompt_semantic_index.json"
TAGS_PATH = ASSETS_DIR / "photo_prompt_tags.json"
EXTENSION_PATH = ASSETS_DIR / "photo_prompt_lighting_extension.json"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "lighting_three_arm_pixel_test_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
from bm25f_retrieval import rank_bm25f  # noqa: E402


EXACT_ROUTES = {
    "하드라이트 선명 그림자 경계 관계": "hard_light_shadow_edge_relation",
    "소프트라이트 넓은 그림자 전이 관계": "soft_light_shadow_edge_relation",
    "루프 코 그림자 인물 조명": "loop_face_light_pattern",
    "버터플라이 중앙 코 그림자 조명": "butterfly_face_light_pattern",
    "스플릿 반면 인물 조명": "split_face_light_pattern",
    "브로드 얼굴 방향 조명 관계": "broad_face_light_orientation_relation",
    "쇼트 얼굴 방향 조명 관계": "short_face_light_orientation_relation",
    "키 필 분리 배경광 역할 관계": "key_fill_separation_background_roles",
    "역광 림 엣지 분리 관계": "backlit_rim_edge_separation_relation",
    "역광 실루엣 덩어리 관계": "backlit_silhouette_mass_relation",
    "하이키 밝은 톤 분포 관계": "high_key_tonal_distribution",
    "로우키 선택적 조명 관계": "low_key_selective_illumination",
    "키아로스쿠로 형태 모델링 관계": "chiaroscuro_form_modeling_relation",
    "테네브리즘 암흑장 고립광": "tenebrist_dark_field_isolation",
    "직광 온카메라 플래시 스냅 관계": "direct_on_camera_flash_snapshot_signature",
    "동기화된 프랙티컬 혼합광 실내": "motivated_practical_mixed_interior_relation",
    "볼류메트릭 차폐 광선 관계": "volumetric_occluded_light_shafts",
    "골든아워 낮은 태양 공간 관계": "golden_hour_low_sun_relation",
    "블루아워 주변광 실내등 균형": "blue_hour_ambient_practical_balance",
    "렌즈 고스팅 플레어 정렬 관계": "lens_ghosting_flare_alignment",
    "베일링 플레어 국소 대비 저하 관계": "veiling_flare_contrast_loss_relation",
    "필름 할레이션 하이라이트 경계 관계": "film_halation_highlight_edge_relation",
}

NEW_PROFILE_IDS = set(EXACT_ROUTES.values())
REUSED_PROFILE_IDS = {
    "rembrandt_face_light_pattern",
    "clamshell_dual_source_portrait_light",
    "negative_fill_shadow_deepening_relation",
}


class PhotoLightingVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {str(row["id"]): row for row in cls.registry["profiles"]}
        cls.routing_registry = {
            **cls.registry,
            "profiles": [
                row
                for row in cls.registry["profiles"]
                if str(row.get("id") or "") in NEW_PROFILE_IDS | REUSED_PROFILE_IDS
            ],
        }
        cls.routing_index = prompt_generator.build_visual_profile_index_payload(
            cls.routing_registry
        )
        cls.generated_index = prompt_generator.load_visual_profile_index(
            INDEX_PATH,
            cls.registry,
        )
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.merged_tags = prompt_generator.load_json(TAGS_PATH)

    @staticmethod
    def source_rows(text: str) -> list[dict[str, object]]:
        return [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            }
        ]

    def hard_matches(self, text: str) -> set[str]:
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.routing_registry,
            self.source_rows(text),
            visual_profile_index=self.routing_index,
            adult_context=True,
        )
        return {
            str(hit["profile_id"])
            for hit in resolution["hits"]
            if hit.get("match_basis") == "exact"
            and hit.get("hard_eligible") is True
        }

    def test_twenty_two_profiles_are_complete_pixel_contracts(self) -> None:
        self.assertLessEqual(NEW_PROFILE_IDS | REUSED_PROFILE_IDS, set(self.profiles))
        all_gate_ids = [
            str(gate["id"])
            for profile in self.registry["profiles"]
            for gate in profile["render_gates"]
        ]
        self.assertEqual(len(all_gate_ids), len(set(all_gate_ids)))
        for profile_id in NEW_PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                group_ids = {str(row["id"]) for row in components["groups"]}
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(set(components["required_group_ids"]), group_ids)
                self.assertEqual(len(group_ids), 5)
                self.assertEqual(len(profile["required_evidence_fields"]), 5)
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

    def test_narrow_exact_terms_route_to_one_profile(self) -> None:
        for text, expected_profile_id in EXACT_ROUTES.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), {expected_profile_id})

    def test_negation_and_adjacent_substitutes_fail_closed(self) -> None:
        cases = (
            "소프트라이트 넓은 그림자 전이 관계 없이 촬영",
            "필름 할레이션 하이라이트 경계 관계를 제외",
            "a dark image with a black background",
            "a global warm orange grade",
            "a ring-light disk and smooth skin retouch",
            "scene-wide fog with random god rays",
            "painted rainbow flare stickers",
            "global bloom and chromatic aberration",
            "a teal-orange LUT with an unlit lamp",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_equipment_and_measurement_metadata_do_not_hard_activate(self) -> None:
        cases = (
            "CRI 98 TLCI 99 SSI 90",
            "3200K tungsten and 5600K daylight",
            "a 120 cm softbox with a silver reflector",
            "Fresnel lamp, grid, flags, barn doors, C-stand",
            "18 percent gray card and incident-light meter",
            "cinematic lighting, dramatic light, studio quality",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_complete_component_description_is_optional_not_hard(self) -> None:
        profile = self.profiles["volumetric_occluded_light_shafts"]
        component_text = ". ".join(
            str(group["any_terms"][0])
            for group in profile["semantics"]["component_semantics"]["groups"]
        )
        self.assertEqual(self.hard_matches(component_text), set())
        self.assertEqual(
            prompt_generator.candidate_pack_visual_component_match(
                profile,
                component_text,
            ),
            "component_semantics",
        )

    def test_twelve_candidate_clusters_merge_as_eighty_four_candidates(self) -> None:
        semantics = self.extension["visual_semantics"]
        self.assertEqual(len(semantics), 12)
        expected_ids: set[str] = set()
        for cluster in semantics:
            with self.subTest(cluster_id=cluster["id"]):
                self.assertEqual(len(cluster["component_groups"]), 7)
                self.assertEqual(len(cluster["candidate_ids"]), 7)
                self.assertLessEqual(set(cluster["hard_profile_ids"]), set(self.profiles))
                expected_ids.update(cluster["candidate_ids"])

        merged_candidates = {
            str(row["id"]): row
            for slot_rows in self.merged_tags["slots"].values()
            for row in slot_rows
            if str(row.get("id") or "") in expected_ids
        }
        self.assertEqual(len(expected_ids), 84)
        self.assertEqual(set(merged_candidates), expected_ids)
        for cluster in semantics:
            for candidate_id in cluster["candidate_ids"]:
                candidate = merged_candidates[candidate_id]
                self.assertIn("lighting_visual_semantics", candidate["tags"])
                self.assertIn(cluster["id"], candidate["tags"])
                if candidate_id == cluster["candidate_ids"][0]:
                    self.assertNotIn("requires_primary_any_tags", candidate)
                    self.assertNotIn("requires_any_tags", candidate)
                else:
                    self.assertEqual(
                        candidate["requires_any_tags"],
                        [cluster["id"]],
                    )
                self.assertGreaterEqual(len(candidate["embedding_text"].split()), 12)

    def test_generated_visual_index_contains_every_lighting_profile(self) -> None:
        self.assertLessEqual(
            NEW_PROFILE_IDS | REUSED_PROFILE_IDS,
            set(self.generated_index["entries"]),
        )
        exact_pairs = {
            (str(row["term"]), str(row["profile_id"]))
            for row in self.generated_index["exact_lookup"]
        }
        for term, profile_id in EXACT_ROUTES.items():
            with self.subTest(term=term):
                self.assertIn((term, profile_id), exact_pairs)

    def test_generated_semantic_index_contains_every_lighting_candidate(self) -> None:
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(
            semantic_index,
            self.merged_tags,
        )
        expected_entries = {
            f"slot:{slot}:{row['id']}"
            for slot, rows in self.extension["slots"].items()
            for row in rows
        }
        self.assertEqual(len(expected_entries), 84)
        self.assertLessEqual(expected_entries, set(semantic_index["entries"]))

    def test_bm25f_surfaces_each_complete_lighting_cluster_near_the_top(self) -> None:
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(
            semantic_index,
            self.merged_tags,
        )
        bm25f = prompt_generator.semantic_bm25f_payload_from_index(semantic_index)
        entry_ids = {
            str(row["id"]): f"slot:{slot}:{row['id']}"
            for slot, rows in self.extension["slots"].items()
            for row in rows
        }
        for cluster in self.extension["visual_semantics"]:
            with self.subTest(cluster_id=cluster["id"]):
                query = " ".join(cluster["component_groups"])
                ranked = rank_bm25f(
                    bm25f,
                    {"active_request": query},
                    limit=14,
                )
                top_ids = {str(row["document_id"]) for row in ranked}
                expected_ids = {
                    entry_ids[candidate_id]
                    for candidate_id in cluster["candidate_ids"]
                }
                self.assertLessEqual(expected_ids, top_ids)

    def test_three_arm_cases_are_frozen_profile_distinct_and_reference_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({row["arm_id"] for row in rows}), 3)
        self.assertEqual(len({row["profile_id"] for row in rows}), 3)
        self.assertEqual(len({row["candidate_cluster_id"] for row in rows}), 3)
        for row in rows:
            with self.subTest(arm_id=row["arm_id"]):
                profile = self.profiles[row["profile_id"]]
                self.assertIs(row["randomized_complex_concept_required"], True)
                self.assertEqual(row["reference"]["role"], "appearance_reference")
                self.assertEqual(row["generation_budget"]["image_calls"], 1)
                self.assertEqual(row["generation_budget"]["retries"], 0)
                self.assertEqual(row["independence"]["cross_arm_inputs"], 0)
                self.assertEqual(row["verdict_rule"]["partial_or_missing"], "fail")
                self.assertEqual(
                    set(row["required_gate_ids"]),
                    {gate["id"] for gate in profile["render_gates"]},
                )
                for path_key, hash_key in (
                    ("request_envelope_path", "request_envelope_file_sha256"),
                    ("authorial_core_path", "authorial_core_file_sha256"),
                ):
                    artifact = ROOT / row[path_key]
                    self.assertTrue(artifact.is_file())
                    self.assertEqual(
                        hashlib.sha256(artifact.read_bytes()).hexdigest(),
                        row[hash_key],
                    )


if __name__ == "__main__":
    unittest.main()
