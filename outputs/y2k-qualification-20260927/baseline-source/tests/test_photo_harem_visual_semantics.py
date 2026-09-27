from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "photo-prompt-image-generator"
SCRIPT_DIR = SKILL_DIR / "scripts"
TAGS_PATH = SKILL_DIR / "assets" / "photo_prompt_tags.json"
EXTENSION_PATH = SKILL_DIR / "assets" / "photo_prompt_harem_extension.json"
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
VISUAL_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
SEMANTIC_INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_semantic_index.json"
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "harem-visual-semantics-20260902"
    / "evidence.jsonl"
)
RESEARCH_PATH = EVIDENCE_PATH.with_name("source-research.md")

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402
from bm25f_retrieval import rank_bm25f  # noqa: E402


PROFILE_ROUTES = {
    "adult Ottoman imperial harem household reconstruction": (
        "ottoman_imperial_harem_household_complex"
    ),
    "성인 톱카프 궁전 하렘 주거 복합체 재현": (
        "ottoman_imperial_harem_household_complex"
    ),
    "adult Mughal zenana courtyard household reconstruction": (
        "mughal_zenana_courtyard_household"
    ),
    "성인 무굴 제나나 안뜰 생활 재현": (
        "mughal_zenana_courtyard_household"
    ),
    "all-adult nineteenth-century Orientalist harem studio tableau": (
        "orientalist_harem_constructed_tableau"
    ),
    "성인 오달리스크 회화풍 구성 세트 타블로": (
        "orientalist_harem_constructed_tableau"
    ),
    "adult harem-romance ensemble scene": (
        "adult_multi_interest_harem_ensemble_relation"
    ),
    "성인 역하렘물 다중 구애 장면": (
        "adult_multi_interest_harem_ensemble_relation"
    ),
    "adult central-target romantic rivalry scene": (
        "adult_central_target_romantic_rivalry_event"
    ),
    "성인 히로인 레이스 경쟁 구도": (
        "adult_central_target_romantic_rivalry_event"
    ),
}

PROFILE_IDS = set(PROFILE_ROUTES.values())
CANDIDATE_ONLY_CLUSTERS = {
    "joseon_naemyeongbu_household_context",
    "ming_qing_inner_court_context",
    "otome_branching_route_key_art",
}
EXPECTED_EVIDENCE_IDS = {
    "harem_iranica_private_space_household_polysemy",
    "harem_topkapi_official_courtyard_service_residence",
    "harem_topkapi_official_domestic_rooms_tasks",
    "harem_ergin_ottoman_regulated_complex_not_fantasy",
    "harem_archnet_agra_private_courtyard_screening",
    "harem_va_mughal_women_palace_encampment_roles",
    "harem_met_orientalism_imagined_harem_art",
    "harem_met_fenton_staged_orientalist_photograph",
    "harem_waikato_three_plus_open_ended_genre_structure",
    "harem_tandf_reverse_harem_gender_boundary",
    "harem_macc_otome_game_genre_boundary",
    "harem_korea_museum_naemyeongbu_roles_not_stereotype",
    "harem_unesco_ming_qing_outer_inner_court_layout",
    "harem_apa_polyamory_consent_confound",
    "harem_nature_animal_social_system_confound",
    "harem_met_poiret_pants_fashion_confound",
}


class PhotoHaremVisualSemanticsTests(unittest.TestCase):
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
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }
        cls.extension_ids_by_slot = {
            slot: {str(row["id"]) for row in rows}
            for slot, rows in cls.extension["slots"].items()
        }
        cls.extension_ids = {
            candidate_id
            for candidate_ids in cls.extension_ids_by_slot.values()
            for candidate_id in candidate_ids
        }
        cls.evidence = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    @staticmethod
    def source_rows(text: str) -> list[dict[str, object]]:
        return [
            {
                "source": "concept_lock",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            },
            {
                "source": "authorial_core_interpreted_intent",
                "text": text,
                "polarity": "required",
                "priority": "critical",
                "mandatory": True,
            },
        ]

    def hard_visual_matches(self, text: str) -> set[str]:
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

    def test_five_profiles_are_complete_adult_five_group_pixel_contracts(self):
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
        all_gate_ids: list[str] = []
        for profile_id in PROFILE_IDS:
            with self.subTest(profile_id=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(profile["activation"]["requires_adult_character"], True)
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 5)
                self.assertEqual(len(components["required_group_ids"]), 5)
                self.assertEqual(len(components["groups"]), 5)
                self.assertEqual(
                    set(components["required_group_ids"]),
                    {str(row["id"]) for row in components["groups"]},
                )
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
                all_gate_ids.extend(
                    str(gate["id"]) for gate in profile["render_gates"]
                )
        self.assertEqual(len(all_gate_ids), len(set(all_gate_ids)))

    def test_narrow_context_complete_terms_route_to_one_profile(self):
        for text, expected_profile_id in PROFILE_ROUTES.items():
            with self.subTest(text=text):
                self.assertEqual(
                    self.hard_visual_matches(text),
                    {expected_profile_id},
                )

    def test_broad_polysemous_and_adjacent_terms_never_force_new_profiles(self):
        broad_terms = (
            "harem",
            "harim",
            "하렘",
            "reverse harem",
            "역하렘",
            "multiple love interests",
            "love polygon",
            "heroine race",
            "harem ending",
            "zenana",
            "purdah",
            "seraglio",
            "saray",
            "haremlik",
            "selamlik",
            "andarun",
            "odalisque",
            "inner court",
            "naemyeongbu",
            "내명부",
            "후궁",
            "宮鬥",
            "otome game",
            "joseimuke",
            "polyamory",
            "polygyny",
            "polyandry",
            "polycule",
            "animal harem",
            "one-male unit",
            "harem pants",
            "하렘 팬츠",
            "Hall's Harem theorem",
        )
        for term in broad_terms:
            with self.subTest(term=term):
                self.assertEqual(self.hard_visual_matches(term), set())

    def test_nearest_visual_substitutes_fail_closed(self):
        substitutes = (
            "adult friends pose together and look at the camera",
            "a fan crowd surrounds one famous adult",
            "one adult flirts while two coworkers remain in the background",
            "three guards escort one adult through a lobby",
            "an established consensual polyamorous adult relationship portrait",
            "a generic luxury room with tiles cushions and reclining adults",
            "a public throne audience in a palace",
            "a tourist hotel spa and public bath",
            "a generic hanbok fashion portrait inside a palace",
            "a Chinese fantasy palace costume group",
            "an adult otome cast poster with no route separation",
            "a wildlife group containing one male and several animals",
        )
        for text in substitutes:
            with self.subTest(text=text):
                self.assertEqual(self.hard_visual_matches(text), set())

    def test_complete_component_text_is_optional_not_hard(self):
        for profile_id in PROFILE_IDS:
            profile = self.profiles[profile_id]
            text = " | ".join(
                str(group["any_terms"][0])
                for group in profile["semantics"]["component_semantics"]["groups"]
            )
            with self.subTest(profile_id=profile_id):
                self.assertEqual(self.hard_visual_matches(text), set())
                optional = prompt_generator.candidate_pack_auto_visual_concept_matches(
                    self.routing_registry,
                    self.source_rows(text),
                )
                self.assertIn(profile_id, optional)

    def test_existing_harem_trouser_profile_remains_the_only_exact_owner(self):
        full_index = prompt_generator.build_visual_profile_index_payload(self.registry)
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            self.source_rows("adult model wearing harem pants"),
            visual_profile_index=full_index,
            adult_context=True,
        )
        exact_hard = {
            str(hit["profile_id"])
            for hit in resolution["hits"]
            if hit.get("match_basis") == "exact"
            and hit.get("hard_eligible") is True
        }
        self.assertIn("gathered_ankle_voluminous_trouser", exact_hard)
        self.assertTrue(exact_hard.isdisjoint(PROFILE_IDS))

    def test_extension_registers_eight_complete_six_candidate_clusters(self):
        self.assertIn(
            EXTENSION_PATH.name,
            prompt_generator.RESEARCH_EXTENSION_FILENAMES,
        )
        self.assertEqual(
            {slot: len(rows) for slot, rows in self.extension["slots"].items()},
            {
                "subject": 8,
                "action": 8,
                "location": 8,
                "prop": 8,
                "composition": 8,
                "aftermath_trace": 8,
            },
        )
        self.assertEqual(len(self.extension_ids), 48)

        manifest_ids: list[str] = []
        hard_profiles_from_manifest: set[str] = set()
        candidate_only_from_manifest: set[str] = set()
        for cluster in self.extension["visual_semantics"]:
            with self.subTest(cluster=cluster["id"]):
                self.assertEqual(len(cluster["component_groups"]), 5)
                self.assertGreaterEqual(len(cluster["confusion_boundaries"]), 5)
                self.assertEqual(len(cluster["candidate_ids"]), 6)
                manifest_ids.extend(str(value) for value in cluster["candidate_ids"])
                hard_ids = {str(value) for value in cluster["hard_profile_ids"]}
                hard_profiles_from_manifest.update(hard_ids)
                if not hard_ids:
                    candidate_only_from_manifest.add(str(cluster["id"]))
        self.assertEqual(hard_profiles_from_manifest, PROFILE_IDS)
        self.assertEqual(candidate_only_from_manifest, CANDIDATE_ONLY_CLUSTERS)
        self.assertEqual(set(manifest_ids), self.extension_ids)
        self.assertEqual(len(manifest_ids), len(set(manifest_ids)))

    def test_every_candidate_is_merged_source_bound_and_fail_closed(self):
        evidence_candidate_ids = {
            str(candidate_id)
            for row in self.evidence
            for candidate_id in row["candidate_ids"]
        }
        self.assertEqual(evidence_candidate_ids & self.extension_ids, self.extension_ids)
        for slot, rows in self.extension["slots"].items():
            for row in rows:
                with self.subTest(slot=slot, candidate=row["id"]):
                    candidate_id = str(row["id"])
                    self.assertIn(candidate_id, self.by_slot[slot])
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("en"))
                    self.assertGreater(float(row.get("weight", 0)), 0)
                    self.assertGreaterEqual(len(row.get("aliases") or []), 2)
                    self.assertGreaterEqual(len(row.get("keywords") or []), 4)
                    self.assertGreaterEqual(
                        len(str(row.get("embedding_text") or "").split()),
                        18,
                    )
                    self.assertEqual(len(row["requires_primary_any_tags"]), 1)
                    self.assertIn(
                        row["requires_primary_any_tags"][0],
                        row["tags"],
                    )
                    self.assertIn("harem_visual_semantics", row["tags"])
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)

    def test_research_evidence_covers_sources_profiles_and_candidate_clusters(self):
        self.assertEqual({row["id"] for row in self.evidence}, EXPECTED_EVIDENCE_IDS)
        self.assertTrue(
            all(
                row["schema_version"] == "photo-research-evidence/v1"
                and row["domain"] == "harem_visual_semantics"
                and row["status"] == "approved"
                and str(row["source_url"]).startswith("https://")
                and row["abstracted_dimensions"]
                and row["candidate_ids"]
                and row["affected_contract_ids"]
                and row["research_limitations"]
                and row["reuse_note"]
                for row in self.evidence
            )
        )
        affected = {
            str(contract_id)
            for row in self.evidence
            for contract_id in row["affected_contract_ids"]
        }
        self.assertTrue(
            {f"visual_obligation:{profile_id}" for profile_id in PROFILE_IDS}
            <= affected
        )
        self.assertTrue(
            {f"candidate_cluster:{cluster_id}" for cluster_id in CANDIDATE_ONLY_CLUSTERS}
            <= affected
        )

    def test_generated_indexes_contain_all_profiles_and_candidates(self):
        visual_index = prompt_generator.load_visual_profile_index(
            VISUAL_INDEX_PATH,
            self.registry,
            provider=prompt_generator.SEMANTIC_PROVIDER,
            model=prompt_generator.SEMANTIC_MODEL_ID,
            dimensions=prompt_generator.DEFAULT_SEMANTIC_DIMENSIONS,
        )
        self.assertTrue(PROFILE_IDS <= set(visual_index["entries"]))
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        expected_entry_ids = {
            f"slot:{slot}:{candidate_id}"
            for slot, candidate_ids in self.extension_ids_by_slot.items()
            for candidate_id in candidate_ids
        }
        self.assertTrue(expected_entry_ids <= set(semantic_index["entries"]))

    def test_bm25f_retrieval_surfaces_each_complete_cluster_near_the_top(self):
        semantic_index = prompt_generator.load_semantic_index_payload(
            SEMANTIC_INDEX_PATH
        )
        prompt_generator.validate_semantic_index_metadata(
            semantic_index,
            self.tags,
        )
        bm25f = prompt_generator.semantic_bm25f_payload_from_index(semantic_index)
        queries = {
            "ottoman_imperial_household_complex": (
                "adult Ottoman imperial private household controlled gate courtyard laundry storage kitchen domestic task"
            ),
            "mughal_zenana_courtyard_household": (
                "adult Mughal zenana offset entrance jali central courtyard textile music household activity"
            ),
            "orientalist_constructed_harem_tableau": (
                "all-adult nineteenth-century Orientalist constructed studio tableau overloaded set seam light spill"
            ),
            "adult_multi_interest_harem_ensemble": (
                "one central adult three potential partners different offers shared common room separate approach paths umbrella tool ticket hub spoke cross awareness unresolved overlap"
            ),
            "adult_central_target_romantic_rivalry": (
                "adult romantic rivals same limited time entrance competing invitations unresolved choice"
            ),
            "joseon_naemyeongbu_household_context": (
                "조선 내명부 성인 문서 인장 직물 의례 준비 주거 안뜰"
            ),
            "ming_qing_inner_court_context": (
                "Ming Qing rear inner court adult inventory ledger textile chamber preparation"
            ),
            "otome_branching_route_key_art": (
                "adult otome game protagonist three branching route tokens separate event lanes unresolved"
            ),
        }
        manifests = {
            str(cluster["id"]): {str(value) for value in cluster["candidate_ids"]}
            for cluster in self.extension["visual_semantics"]
        }
        candidate_entry_ids = {
            candidate_id: f"slot:{slot}:{candidate_id}"
            for slot, candidate_ids in self.extension_ids_by_slot.items()
            for candidate_id in candidate_ids
        }
        for cluster_id, query in queries.items():
            with self.subTest(cluster=cluster_id):
                ranked = rank_bm25f(
                    bm25f,
                    {"active_request": query},
                    limit=8,
                )
                top_ids = {str(row["document_id"]) for row in ranked}
                expected_ids = {
                    candidate_entry_ids[candidate_id]
                    for candidate_id in manifests[cluster_id]
                }
                self.assertLessEqual(expected_ids, top_ids)

    def test_registry_validator_accepts_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])

    def test_research_note_keeps_claim_and_identity_boundaries(self):
        note = RESEARCH_PATH.read_text(encoding="utf-8")
        for phrase in (
            "단독어는 하드 활성화 금지",
            "성별 배치는 사용자 요청이 소유하며 기본값이 아니다",
            "한 장의 야생동물 사진에서 성별·교미 체계·지속적 사회 구조를 개체 수만으로 확정할 수 없다",
            "partial 또는 누락은 실패",
            "생성 픽셀",
            "사용자 의미 판단",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, note)


if __name__ == "__main__":
    unittest.main()
