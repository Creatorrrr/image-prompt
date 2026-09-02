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
TAGS_PATH = ASSETS_DIR / "photo_prompt_tags.json"
EXTENSION_PATH = ASSETS_DIR / "photo_prompt_emotional_place_extension.json"
REGISTRY_PATH = ASSETS_DIR / "photo_prompt_visual_obligations.json"
VISUAL_INDEX_PATH = ASSETS_DIR / "photo_prompt_visual_profile_index.json"
SEMANTIC_INDEX_PATH = ASSETS_DIR / "photo_prompt_semantic_index.json"
CASES_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "photo_prompt"
    / "emotional_place_three_arm_pixel_test_cases_v1.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
from bm25f_retrieval import rank_bm25f  # noqa: E402


EXACT_ROUTES = {
    "창가 좌석의 작은 행동과 방향성 자연광": (
        "window_seat_daylight_activity_relation"
    ),
    "두 실제 공간을 잇는 건축 문턱 통과 장면": (
        "architectural_threshold_frame_depth_relation"
    ),
    "연속 골목길 위 중간 보폭과 세 깊이 표지": (
        "circulation_path_mid_action_depth_relation"
    ),
    "실제 간판 광원과 정렬된 젖은 노면 반사": (
        "wet_surface_light_reflection_owner_relation"
    ),
    "가까운 옥상 난간과 낮고 먼 도시 전망의 고도 관계": (
        "overlook_edge_foreground_vista_relation"
    ),
    "설치된 작품과 관람자 시선을 잇는 갤러리 장면": (
        "gallery_viewer_art_attention_relation"
    ),
    "진열 원위치와 반쯤 꺼낸 대상을 잇는 고르기 행동": (
        "retail_browse_source_selection_relation"
    ),
    "짐과 열차 상태가 연결된 승강장 대기 장면": (
        "transit_waiting_departure_relation"
    ),
    "남겨진 산업 공정 흔적과 새 공공 사용의 물리 접합": (
        "adaptive_reuse_old_new_material_junction"
    ),
    "방 마루 마당이 이어지는 한옥 안팎 관계": (
        "hanok_madang_maru_inside_outside_relation"
    ),
}

PROFILE_IDS = set(EXACT_ROUTES.values())
BROAD_CANDIDATE_ONLY = (
    "감성 사진",
    "인스타 감성",
    "카페 감성",
    "창가",
    "골목",
    "걷는 사진",
    "비 오는 골목",
    "네온 감성",
    "옥상 감성",
    "전시회 감성",
    "서점 감성",
    "역 감성",
    "산업 감성",
    "한옥 감성",
    "instagrammable place in Korea",
)


class PhotoEmotionalPlaceVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }
        cls.routing_registry = {
            **cls.registry,
            "profiles": [
                profile
                for profile in cls.registry["profiles"]
                if str(profile.get("id") or "") in PROFILE_IDS
            ],
        }
        cls.routing_index = prompt_generator.build_visual_profile_index_payload(
            cls.routing_registry
        )
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.merged_candidates = {
            str(row["id"]): (slot, row)
            for slot, rows in cls.tags["slots"].items()
            for row in rows
        }

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

    def exact_hard_matches(self, text: str) -> set[str]:
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

    def test_ten_profiles_are_complete_five_group_pixel_contracts(self) -> None:
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
        all_gate_ids = [
            str(gate["id"])
            for profile in self.registry["profiles"]
            for gate in profile["render_gates"]
        ]
        self.assertEqual(len(all_gate_ids), len(set(all_gate_ids)))
        for profile_id in PROFILE_IDS:
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
                self.assertEqual(
                    self.exact_hard_matches(text),
                    {expected_profile_id},
                )

    def test_broad_place_and_mood_terms_remain_candidate_only(self) -> None:
        for text in BROAD_CANDIDATE_ONLY:
            with self.subTest(text=text):
                self.assertEqual(self.exact_hard_matches(text), set())

    def test_excluded_substitutes_fail_closed(self) -> None:
        cases = (
            "창가 좌석의 작은 행동과 방향성 자연광 but only a studio softbox",
            "두 실제 공간을 잇는 건축 문턱 통과 장면 as a fantasy portal",
            "연속 골목길 위 중간 보폭과 세 깊이 표지 with floating feet",
            "실제 간판 광원과 정렬된 젖은 노면 반사 on a dry polished floor",
            "가까운 옥상 난간과 낮고 먼 도시 전망의 고도 관계 using a skyline backdrop",
            "설치된 작품과 관람자 시선을 잇는 갤러리 장면 with a blank wall",
            "진열 원위치와 반쯤 꺼낸 대상을 잇는 고르기 행동 as a staged product portrait",
            "짐과 열차 상태가 연결된 승강장 대기 장면 as a static fashion portrait",
            "남겨진 산업 공정 흔적과 새 공공 사용의 물리 접합 in a generic loft",
            "방 마루 마당이 이어지는 한옥 안팎 관계 as a generic East Asian pavilion",
        )
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(self.exact_hard_matches(text), set())

    def test_extension_merges_twenty_one_relation_candidates(self) -> None:
        self.assertEqual(len(self.extension["visual_semantics"]), 10)
        extension_rows = {
            str(row["id"]): (slot, row)
            for slot, rows in self.extension["slots"].items()
            for row in rows
        }
        self.assertEqual(len(extension_rows), 21)
        self.assertEqual(
            set(extension_rows),
            {
                candidate_id
                for candidate_id in self.merged_candidates
                if candidate_id.startswith("ep_")
            },
        )
        for cluster in self.extension["visual_semantics"]:
            with self.subTest(cluster_id=cluster["id"]):
                self.assertEqual(cluster["hard_profile_ids"], [cluster["id"]])
                self.assertEqual(len(cluster["component_groups"]), 5)
                self.assertEqual(len(cluster["confusion_boundaries"]), 5)
                self.assertLessEqual(
                    set(cluster["candidate_ids"]),
                    set(self.merged_candidates),
                )
        for candidate_id, (slot, row) in extension_rows.items():
            with self.subTest(candidate_id=candidate_id):
                self.assertEqual(self.merged_candidates[candidate_id][0], slot)
                self.assertIn("emotional_place_visual_semantics", row["tags"])
                self.assertIn(slot, row["tags"])
                self.assertGreaterEqual(len(row["embedding_text"].split()), 12)
                cluster_ids = [
                    tag for tag in row["tags"] if tag in PROFILE_IDS
                ]
                self.assertEqual(len(cluster_ids), 1)
                if slot != "composition":
                    self.assertEqual(row["requires_any_tags"], cluster_ids)

    def test_generated_visual_index_contains_every_profile_and_exact_term(self) -> None:
        generated = prompt_generator.load_visual_profile_index(
            VISUAL_INDEX_PATH,
            self.registry,
        )
        self.assertLessEqual(PROFILE_IDS, set(generated["entries"]))
        exact_pairs = {
            (str(row["term"]), str(row["profile_id"]))
            for row in generated["exact_lookup"]
        }
        for term, profile_id in EXACT_ROUTES.items():
            with self.subTest(term=term):
                self.assertIn((term, profile_id), exact_pairs)

    def test_generated_semantic_index_contains_every_extension_candidate(self) -> None:
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(semantic_index, self.tags)
        expected_entries = {
            f"slot:{slot}:{row['id']}"
            for slot, rows in self.extension["slots"].items()
            for row in rows
        }
        self.assertEqual(len(expected_entries), 21)
        self.assertLessEqual(expected_entries, set(semantic_index["entries"]))

    def test_bm25f_surfaces_each_new_relation_candidate(self) -> None:
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(semantic_index, self.tags)
        bm25f = prompt_generator.semantic_bm25f_payload_from_index(semantic_index)
        for slot, rows in self.extension["slots"].items():
            for row in rows:
                with self.subTest(candidate_id=row["id"]):
                    query = " ".join(
                        [row["en"], *row["aliases"], *row["keywords"]]
                    )
                    ranked = rank_bm25f(
                        bm25f,
                        {"active_request": query},
                        limit=8,
                    )
                    self.assertIn(
                        f"slot:{slot}:{row['id']}",
                        {str(hit["document_id"]) for hit in ranked},
                    )

    def test_three_arm_cases_are_frozen_distinct_and_reference_bound(self) -> None:
        rows = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 3)
        self.assertEqual(len({row["arm_id"] for row in rows}), 3)
        self.assertEqual(len({row["profile_id"] for row in rows}), 3)
        self.assertEqual(len({row["candidate_cluster_id"] for row in rows}), 3)
        self.assertEqual(
            len({row["request_envelope_file_sha256"] for row in rows}),
            3,
        )
        self.assertEqual(
            len({row["authorial_core_file_sha256"] for row in rows}),
            3,
        )
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
                    self.assertRegex(
                        row[hash_key],
                        r"^[0-9a-f]{64}$",
                    )
                    if artifact.is_file():
                        self.assertEqual(
                            hashlib.sha256(artifact.read_bytes()).hexdigest(),
                            row[hash_key],
                        )


if __name__ == "__main__":
    unittest.main()
