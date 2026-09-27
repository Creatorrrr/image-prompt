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
    SKILL_DIR / "assets" / "photo_prompt_violence_crime_extension.json"
)
REGISTRY_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_obligations.json"
INDEX_PATH = SKILL_DIR / "assets" / "photo_prompt_visual_profile_index.json"
EVIDENCE_PATH = (
    ROOT
    / "docs"
    / "research-evidence"
    / "photo-prompt"
    / "violence-crime-visual-semantics-20260901"
    / "evidence.jsonl"
)

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import validate_photo_prompt_dictionary  # noqa: E402


PROFILE_ROUTES = {
    "구체적 위해 협박을 가하는 특정 사람과 강압 요구가 있는 대인 위협": (
        "interpersonal_credible_threat_relation"
    ),
    "대인 폭행에서 가해자와 피해자 사이 원치 않는 물리력과 충격": (
        "interpersonal_physical_assault_event"
    ),
    "강도 범행에서 피해자의 지갑 재물을 폭력으로 빼앗아 이동": (
        "robbery_forced_property_transfer"
    ),
    "납치 사건에서 가해자가 피랍자의 퇴로를 차단하고 강제 이동": (
        "forced_relocation_abduction_event"
    ),
    "인질극에서 억류자가 인질을 두고 정부인 제3자에게 요구": (
        "hostage_third_party_compulsion"
    ),
    "허구 살해 사건에서 허구 가해자가 피해자에게 치명적 행위": (
        "fictional_intentional_homicide_causality"
    ),
    "허구의 조직범죄에서 구조화된 집단의 역할 분담과 물질적 이익": (
        "fictional_organized_crime_operation"
    ),
    "고의 방화에서 방화범이 표적 재산의 발화점에 점화": (
        "deliberate_arson_causality"
    ),
    "침입절도에서 침입자가 파손된 잠금장치를 넘어 표적 재물을 탐색": (
        "burglary_forced_entry_crime_event"
    ),
    "보복 폭력에서 선행 피해와 동일 당사자의 복수 대상이 연결": (
        "retaliatory_violence_prior_harm_relation"
    ),
    "범죄현장 감식에서 전경 중경 근접과 증거번호표 측정 눈금 현장 기록": (
        "forensic_scene_documentation_process"
    ),
    "혈흔 감식에서 전체 사진과 패턴 경계 방향 측정 눈금을 기록": (
        "bloodstain_observation_documentation"
    ),
    "구금 고문에서 공적 통제 아래 극심한 고통과 정보 획득 목적": (
        "custodial_torture_purpose_relation"
    ),
    "집단학살에서 보호 집단 파괴 의도와 조직적 캠페인으로 집단 구성원을 표적화": (
        "genocidal_group_destruction_campaign"
    ),
    "전쟁범죄에서 무력충돌 연계 속 보호 민간인 의료 시설에 금지 행위": (
        "armed_conflict_protected_status_breach"
    ),
    "공개처형에서 사형수와 집행자가 구금된 포로에게 명령된 살해": (
        "controlled_execution_custody_causality"
    ),
    "성인 대상 성폭력에서 원치 않는 성적 행위와 유효한 동의 없음 및 강압": (
        "adult_nonconsensual_sexual_violence_relation"
    ),
    "미성년자 대상 범죄에서 명시된 미성년자에게 성인 가해자가 구체적 범죄 행위": (
        "declared_minor_targeted_crime_relation"
    ),
    "성인 인신매매에서 성인 피해자의 모집 운송 은닉 인수와 폭력 사기 강압 및 착취 목적": (
        "adult_human_trafficking_exploitation_chain"
    ),
    "테러 공격에서 민간 대상을 대중 위협하고 정부 강요를 목적으로 공개 협박": (
        "terrorism_civilian_coercion_purpose_relation"
    ),
}

PROFILE_IDS = set(PROFILE_ROUTES.values())

CLUSTER_PROFILES = {
    "interpersonal_violence": {
        "interpersonal_credible_threat_relation",
        "interpersonal_physical_assault_event",
        "retaliatory_violence_prior_harm_relation",
    },
    "coercive_capture_property": {
        "robbery_forced_property_transfer",
        "forced_relocation_abduction_event",
        "hostage_third_party_compulsion",
        "burglary_forced_entry_crime_event",
    },
    "fatal_fire_execution": {
        "fictional_intentional_homicide_causality",
        "deliberate_arson_causality",
        "controlled_execution_custody_causality",
    },
    "organized_crime_operation": {"fictional_organized_crime_operation"},
    "forensic_documentation": {
        "forensic_scene_documentation_process",
        "bloodstain_observation_documentation",
    },
    "custodial_torture": {"custodial_torture_purpose_relation"},
    "mass_atrocity": {
        "genocidal_group_destruction_campaign",
        "armed_conflict_protected_status_breach",
    },
    "adult_sexual_violence": {
        "adult_nonconsensual_sexual_violence_relation"
    },
    "minor_targeted_crime": {"declared_minor_targeted_crime_relation"},
    "human_trafficking": {"adult_human_trafficking_exploitation_chain"},
    "terrorism_civilian_coercion": {
        "terrorism_civilian_coercion_purpose_relation"
    },
}


class PhotoViolenceCrimeVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.extension = json.loads(EXTENSION_PATH.read_text(encoding="utf-8"))
        cls.registry = prompt_generator.load_visual_obligation_registry(REGISTRY_PATH)
        cls.routing_index = prompt_generator.build_visual_profile_index_payload(
            cls.registry
        )
        cls.tags = prompt_generator.load_json(TAGS_PATH)
        cls.profiles = {
            str(profile["id"]): profile for profile in cls.registry["profiles"]
        }
        cls.by_slot = {
            slot: {str(row["id"]): row for row in rows}
            for slot, rows in cls.tags["slots"].items()
        }

    def hard_visual_matches(self, text: str) -> set[str]:
        resolution = prompt_generator.resolve_visual_profile_hits(
            self.registry,
            [
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
            ],
            visual_profile_index=self.routing_index,
            adult_context=True,
        )
        return {
            str(hit["profile_id"])
            for hit in resolution["hits"]
            if hit.get("match_basis") == "exact"
            and hit.get("hard_eligible") is True
        }

    def test_twenty_profiles_have_relation_evidence_and_pixel_gates(self):
        self.assertLessEqual(PROFILE_IDS, set(self.profiles))
        gate_ids: list[str] = []
        for profile_id in PROFILE_IDS:
            with self.subTest(profile=profile_id):
                profile = self.profiles[profile_id]
                components = profile["semantics"]["component_semantics"]
                self.assertIs(
                    profile["activation"][
                        "semantic_discovery_requires_component_evidence"
                    ],
                    True,
                )
                self.assertEqual(components["minimum_component_groups"], 4)
                self.assertEqual(
                    set(components["required_group_ids"]),
                    {row["id"] for row in components["groups"]},
                )
                self.assertEqual(len(profile["required_evidence_fields"]), 4)
                self.assertEqual(
                    set(profile["required_evidence_fields"]),
                    set(profile["evidence_requirements"]),
                )
                self.assertEqual(len(profile["render_gates"]), 4)
                self.assertEqual(len(profile["reject_substitutes"]), 4)
                gate_ids.extend(str(gate["id"]) for gate in profile["render_gates"])
        self.assertEqual(len(gate_ids), len(set(gate_ids)))

    def test_direct_contextual_terms_route_only_to_intended_new_profile(self):
        for text, profile_id in PROFILE_ROUTES.items():
            with self.subTest(profile=profile_id):
                self.assertEqual(
                    self.hard_visual_matches(text) & PROFILE_IDS,
                    {profile_id},
                )

    def test_broad_vocabulary_remains_advisory(self):
        broad_terms = (
            "crime",
            "violence",
            "blood",
            "injury",
            "death",
            "horror",
            "noir",
            "gang",
            "war",
            "revenge",
            "corruption",
            "fear",
            "red",
            "dark",
            "weapon",
            "prison",
            "police tape",
            "범죄",
            "폭력",
            "피",
            "상처",
            "죽음",
            "공포",
            "누아르",
            "갱",
            "전쟁",
            "복수",
            "부패",
            "붉은색",
            "어두운",
            "무기",
            "감옥",
            "폴리스라인",
        )
        for term in broad_terms:
            with self.subTest(term=term):
                self.assertTrue(self.hard_visual_matches(term).isdisjoint(PROFILE_IDS))

    def test_nearest_substitutes_do_not_activate_new_profiles(self):
        substitutes = (
            "A villain portrait holding a weapon with no target",
            "A consensual boxing match",
            "A normal retail payment at a counter",
            "Paramedics moving a patient into an ambulance",
            "A kidnapping scene with no third-party demand",
            "An accidental fall with no perpetrator",
            "Friends in dark suits meeting at a lawful warehouse",
            "A building already burning after an electrical accident",
            "A locksmith opening an owner's door",
            "An angry revenge-themed fashion portrait with no prior harm",
            "Yellow police tape as a noir backdrop",
            "Red paint splatter photographed without scale",
            "An ordinary interrogation with no severe suffering",
            "A generic battlefield massacre with no group-destruction intent",
            "Ordinary fighting between combatants",
            "A ceremonial firing-squad drill with no captive",
            "Consensual adult intimacy",
            "A school safety drill",
            "Voluntary international job travel",
            "A peaceful public protest",
        )
        for text in substitutes:
            with self.subTest(text=text):
                self.assertTrue(self.hard_visual_matches(text).isdisjoint(PROFILE_IDS))

    def test_extension_has_eleven_complete_six_slot_clusters(self):
        self.assertIn(
            EXTENSION_PATH.name,
            prompt_generator.RESEARCH_EXTENSION_FILENAMES,
        )
        self.assertEqual(
            {slot: len(rows) for slot, rows in self.extension["slots"].items()},
            {
                "aesthetic_trend": 11,
                "subject": 11,
                "action": 11,
                "location": 11,
                "prop": 11,
                "composition": 11,
            },
        )
        extension_ids: list[str] = []
        for slot, rows in self.extension["slots"].items():
            for row in rows:
                with self.subTest(slot=slot, candidate=row["id"]):
                    candidate_id = str(row["id"])
                    extension_ids.append(candidate_id)
                    self.assertIn(candidate_id, self.by_slot[slot])
                    self.assertTrue(row.get("ko"))
                    self.assertTrue(row.get("en"))
                    self.assertTrue(row.get("aliases"))
                    self.assertTrue(row.get("keywords"))
                    self.assertGreaterEqual(
                        len(str(row.get("embedding_text") or "").split()), 8
                    )
                    self.assertIn(
                        "violence_crime_visual_semantics", row.get("tags", [])
                    )
                    self.assertNotIn("rank", row)
                    self.assertNotIn("score", row)
        self.assertEqual(len(extension_ids), 66)
        self.assertEqual(len(extension_ids), len(set(extension_ids)))

    def test_cluster_manifest_binds_every_profile_and_candidate_once(self):
        rows = {
            str(row["id"]): row for row in self.extension["visual_semantics"]
        }
        self.assertEqual(set(rows), set(CLUSTER_PROFILES))
        all_candidate_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        bound_profiles: set[str] = set()
        bound_candidates: list[str] = []
        for cluster_id, expected_profiles in CLUSTER_PROFILES.items():
            with self.subTest(cluster=cluster_id):
                row = rows[cluster_id]
                self.assertEqual(set(row["hard_profile_ids"]), expected_profiles)
                self.assertTrue(expected_profiles <= PROFILE_IDS)
                self.assertEqual(len(row["candidate_ids"]), 6)
                self.assertTrue(set(row["candidate_ids"]) <= all_candidate_ids)
                self.assertEqual(len(row["component_groups"]), 4)
                self.assertEqual(len(row["confusion_boundaries"]), 4)
                bound_profiles.update(row["hard_profile_ids"])
                bound_candidates.extend(row["candidate_ids"])
        self.assertEqual(bound_profiles, PROFILE_IDS)
        self.assertEqual(set(bound_candidates), all_candidate_ids)
        self.assertEqual(len(bound_candidates), len(set(bound_candidates)))

    def test_extension_adds_no_separate_safety_contract_or_slot(self):
        serialized = json.dumps(self.extension, ensure_ascii=False).casefold()
        self.assertNotIn("safety_profile", serialized)
        self.assertNotIn("moderation_tier", serialized)
        self.assertNotIn("automatic_negative", serialized)
        self.assertNotIn("safety_profile", self.extension["slots"])
        for profile_id in PROFILE_IDS:
            profile = self.profiles[profile_id]
            self.assertNotIn("safety", profile)
            self.assertEqual(profile["runtime_expression"]["forbidden_prompt_terms"], [])
            self.assertEqual(
                profile["runtime_expression"]["runtime_forbidden_labels"], []
            )

    def test_research_evidence_is_approved_and_contract_bound(self):
        rows = [
            json.loads(line)
            for line in EVIDENCE_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        self.assertEqual(len(rows), 15)
        extension_ids = {
            str(row["id"])
            for slot_rows in self.extension["slots"].values()
            for row in slot_rows
        }
        covered_profiles: set[str] = set()
        for row in rows:
            with self.subTest(evidence=row["id"]):
                self.assertEqual(row["schema_version"], "photo-research-evidence/v1")
                self.assertEqual(row["domain"], "violence_crime_visual_semantics")
                self.assertEqual(row["status"], "approved")
                self.assertTrue(str(row["source_url"]).startswith("https://"))
                self.assertGreaterEqual(len(row["abstracted_dimensions"]), 3)
                self.assertGreaterEqual(len(row["research_limitations"]), 2)
                self.assertTrue(row["reuse_note"])
                self.assertTrue(set(row["candidate_ids"]) <= extension_ids)
                for contract_id in row["affected_contract_ids"]:
                    self.assertTrue(contract_id.startswith("visual_obligation:"))
                    profile_id = contract_id.split(":", 1)[1]
                    self.assertIn(profile_id, PROFILE_IDS)
                    covered_profiles.add(profile_id)
        self.assertEqual(covered_profiles, PROFILE_IDS)

    def test_real_generated_index_contains_new_profiles_and_vectors(self):
        real_index = prompt_generator.load_visual_profile_index(
            INDEX_PATH,
            self.registry,
        )
        self.assertEqual(
            real_index["registry_sha256"],
            prompt_generator.visual_profile_registry_sha256(self.registry),
        )
        for profile_id in PROFILE_IDS:
            with self.subTest(profile=profile_id):
                entry = real_index["entries"][profile_id]
                self.assertEqual(len(entry["vector"]), 768)
                self.assertTrue(entry["text"])

    def test_registry_schema_accepts_violence_crime_profiles(self):
        errors: list[str] = []
        validate_photo_prompt_dictionary.validate_visual_obligation_registry(
            REGISTRY_PATH,
            errors,
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
