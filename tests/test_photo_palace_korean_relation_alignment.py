"""Source-guided palace alias regressions; use after installing the reviewed DATA edit.

Loads the real full merged registry and index. These deterministic tests do not
measure natural-query recall or image quality. Complete legacy-positive gate loss
is diagnostic evidence, not a permanent required behavior of this test suite.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as g

# Pin only the reviewed aliases and selected relations, not complete profiles.
CASES = {'pf_window_seat': {'ko_clauses': ('붙박이 좌석이 조적 벽의 창 오목부 깊이 안에 자리한다', '창 측벽이 그 좌석 공간을 바깥 창과 연결한다',
                                   '바깥 개구부는 좌석 면보다 바깥쪽에 놓이며 가구 하나를 창 앞에 둔 장면과 구별된다'),
                    'english_duties': ('a built-in seat occupies the depth of the masonry recess',
                                       'the side reveals connect the seat space to the outer window',
                                       'the outer opening sits beyond the seat plane'),
                    'compatible_negatives': ('건축 사진을 만들어 주세요: 좌석이 벽 깊이 안에 들어간다; 창 측벽과 바깥 개구부가 연결된다; 가구 '
                                             '하나를 창 앞에 둔 장면과 구별된다. 벽은 두꺼운 원목 구조이며, 벽 속 고정 좌석과 창 측벽도 '
                                             '원목으로 이어진다. 같은 벽체와 깊은 창 측벽은 통원목으로 이루어져 있고, 벽 깊이 전체에서 원목 '
                                             '단면과 짜맞춤이 보인다.',
                                             'Make an architectural photograph: the seat is set within '
                                             'the depth of the wall; the window side reveals connect to '
                                             'the outer opening; the scene is distinguishable from a '
                                             'piece of furniture placed in front of a window. The wall '
                                             'is a thick solid-timber structure, and the fixed seat '
                                             'inside the wall and the window side reveals continue in '
                                             'solid timber. This same wall and its deep window side '
                                             'reveals are solid timber, with exposed timber end grain '
                                             'and timber joinery visible through the full wall depth.'),
                    'relation_substitution': ('조적 벽', '통원목 벽')},
 'pf_double_helix': {'ko_clauses': ('서로 다른 두 나선형 계단 구간이 하나의 중심부 둘레를 감아 돈다',
                                    '두 계단이 공유하는 중심부는 속이 빈 상태로 보인다',
                                    '각 계단은 서로 분리된 연속 동선을 유지하여 두 경로가 각각 추적되며 중간에서 임의로 합쳐지거나 충돌하지 않는다'),
                     'english_duties': ('two distinct helical stair flights wind around one core',
                                        'the shared central core remains visibly hollow',
                                        'each flight retains a separate continuous circulation path'),
                     'compatible_negatives': ('건축 사진을 만들어 주세요: 두 개의 계단 경로가 추적된다; 공유 중심부가 비어 보인다; 두 경로가 '
                                              '중간에서 임의로 합쳐지거나 충돌하지 않는다. 두 계단은 빈 중앙 공간의 양쪽에서 곧게 오르는 평행 '
                                              '직선 계단이다.',
                                              'Make an architectural photograph: two stair routes can '
                                              'be traced; the shared central core is visibly hollow; '
                                              'the two routes do not arbitrarily merge or collide '
                                              'midway. The two stairs are parallel straight flights '
                                              'rising straight along opposite sides of the empty '
                                              'central space.'),
                     'relation_substitution': ('서로 다른 두 나선형 계단 구간이 하나의 중심부 둘레를 감아 돈다',
                                               '서로 다른 두 직선 계단 구간이 하나의 중심부 양옆에서 평행하게 오른다')},
 'pf_roofless_ruin': {'ko_clauses': ('지붕이 없어 옛 방 안에서 그 방 위의 열린 하늘이 보인다',
                                     '남아 있는 벽과 창 개구부가 그 방의 옛 실내 바닥을 둘러싼다',
                                     '파손된 상부 구조 아래에 떨어진 조적 잔해가 국소적으로 놓여 있고 파손은 구조 경계와 연결되어 단순한 이끼와 '
                                     '구별된다'),
                      'english_duties': ('open sky appears above the former room where its roof is '
                                         'missing',
                                         'surviving walls and window openings enclose the former '
                                         'interior floor',
                                         'localized fallen masonry lies below the broken upper '
                                         'structure'),
                      'compatible_negatives': ('건축 사진을 만들어 주세요: 지붕이 없어 방 안에서 하늘이 보인다; 남은 벽·창·바닥이 이전 실내를 '
                                               '이룬다; 파손이 구조 경계와 연결되며 단순 이끼가 아니다. 파손된 상부 벽의 잘린 단면이 선명하며, '
                                               '바닥의 떨어진 돌과 벽돌은 모두 치워져 매끈한 석판만 남아 있다.',
                                               'Make an architectural photograph: the sky is visible '
                                               'from inside the room because the roof is missing; the '
                                               'remaining walls, windows and floor form the former '
                                               'interior; the damage is connected to structural '
                                               'boundaries and is more than merely moss. The cut '
                                               'sections of the damaged upper walls are clearly '
                                               'visible, and all fallen stones and bricks have been '
                                               'cleared from the floor, leaving only smooth stone '
                                               'slabs.'),
                      'relation_substitution': ('파손된 상부 구조 아래에 떨어진 조적 잔해가 국소적으로 놓여 있고',
                                                '파손된 상부 구조 아래에는 잔해를 모두 치운 석판 바닥만 있고')}}

class PalaceKoreanRelationAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = g.load_visual_obligation_registry(
            SKILL / "assets/photo_prompt_visual_obligations.json"
        )
        cls.index = g.load_visual_profile_index(
            SKILL / "assets/photo_prompt_visual_profile_index.json", cls.registry
        )
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}
        cls.data = {
            g.VISUAL_OBLIGATIONS_DATA_KEY: cls.registry,
            g.VISUAL_PROFILE_INDEX_DATA_KEY: cls.index,
        }

    def resolve(self, text):
        return g.resolve_visual_profile_hits(
            self.registry,
            [{"source": "concept_lock", "text": text, "polarity": "required",
              "priority": "critical", "mandatory": True}],
            visual_profile_index=self.index,
            adult_context=False,
        )

    def hard(self, text):
        return {h["profile_id"] for h in self.resolve(text)["hits"]
                if h.get("hard_eligible")}

    def obligation(self, text, profile_id):
        result = {"provenance": {
            "prompt_id": "palace-alignment-regression", "concept_lock": [text]
        }}
        contract = g.candidate_pack_visual_obligations(
            self.data, result, {}, None, self.resolve(text)
        )
        return next(o for o in contract["obligations"] if o["id"] == profile_id)

    def test_reviewed_korean_and_english_aliases_are_present(self):
        # Additional genuinely equivalent aliases are allowed in future.
        for pid, case in CASES.items():
            with self.subTest(profile=pid):
                terms = self.profiles[pid]["activation"]["exact_terms"]
                self.assertIn("; ".join(case["ko_clauses"]), terms)
                self.assertIn("; ".join(case["english_duties"]), terms)

    def test_selected_component_evidence_and_gate_invariants(self):
        for pid, case in CASES.items():
            with self.subTest(profile=pid):
                components = self.profiles[pid]["authored_components"]["components"]
                by_id = {c["id"]: c for c in components}
                self.assertEqual(set(by_id), {f"component_{i}" for i in (1, 2, 3)})
                for i, duty in enumerate(case["english_duties"], 1):
                    component = by_id[f"component_{i}"]
                    self.assertEqual(component["match_terms"], [duty])
                    self.assertEqual(component["evidence_terms"], [duty])
                    self.assertEqual(component["evidence_field"], f"component_{i}_phrase")
                    self.assertGreaterEqual(component["min_content_words"], 3)
                    gate = component["render_gate"]
                    self.assertEqual(gate["id"], f"vo_{pid}_{i}")
                    self.assertEqual(gate["review_scale"], "native" if i == 2 else "both")
                    self.assertIn(duty, gate["description"])

    def test_korean_and_english_activate_the_same_required_contract(self):
        for pid, case in CASES.items():
            with self.subTest(profile=pid):
                en, ko = ("; ".join(case[k]) for k in ("english_duties", "ko_clauses"))
                self.assertEqual(self.hard(en), {pid})
                self.assertEqual(self.hard(ko), {pid})
                a, b = self.obligation(en, pid), self.obligation(ko, pid)
                for field in ("component_semantics", "prompt_binding",
                              "evidence_requirements", "render_gates"):
                    self.assertEqual(a[field], b[field])
                self.assertEqual(
                    b["prompt_binding"]["required_evidence_fields"],
                    [f"component_{i}_phrase" for i in (1, 2, 3)],
                )
                self.assertEqual(
                    [gate["id"] for gate in b["render_gates"]],
                    [f"vo_{pid}_{i}" for i in (1, 2, 3)],
                )

    def test_compatible_korean_and_english_negatives_do_not_force_selected_variant(self):
        # Same-owner timber, straight flights and a cleared ruin floor contradict
        # the selected duty while satisfying the inherited Korean description.
        for pid, case in CASES.items():
            for language, text in zip(("ko", "en"), case["compatible_negatives"]):
                with self.subTest(profile=pid, language=language):
                    self.assertNotIn(pid, self.hard(text))

    def test_missing_clauses_and_substituted_relations_remain_nonhard(self):
        for pid, case in CASES.items():
            clauses = case["ko_clauses"]
            for index in range(len(clauses)):
                with self.subTest(profile=pid, omitted_clause=index + 1):
                    self.assertNotIn(pid, self.hard("; ".join(
                        clauses[:index] + clauses[index + 1:]
                    )))
            old, new = case["relation_substitution"]
            canonical = "; ".join(clauses)
            self.assertEqual(canonical.count(old), 1)
            with self.subTest(profile=pid, substituted_relation=True):
                self.assertNotIn(pid, self.hard(canonical.replace(old, new)))

    def test_generic_names_do_not_force_selected_geometry_or_material(self):
        for text in ("an architectural photograph of a window seat",
                     "an architectural photograph of two stair routes",
                     "an architectural photograph of a roofless hall"):
            with self.subTest(text=text):
                self.assertFalse(set(CASES) & self.hard(text))


if __name__ == "__main__":
    unittest.main()
