"""Fixed source-informed food/carrier regressions, not rendered-image tests."""
from __future__ import annotations

import copy
import unittest

from tests import photo_prompt_fixtures as fixtures
import prompt_generator as g
import audit_composed_prompt as audit

SCENES = (
    ('rice-crust', 'fire_f116', True, 'food',
     'one curved crust of browned cooked rice', 'a plain ceramic serving plate',
     'the connected rice layer rests with individual cooked grains visible',
     'Photograph a curved crust of browned cooked rice on a plain serving plate, with recognizable cooked rice grains.',
     '흰 접시 위에서 익은 쌀알과 연결된 갈색 층이 보이는 곡면 누룽지를 촬영해줘.'),
    ('rice-photo-card', 'fire_f116', False, 'object',
     'one paper card with a printed photograph of browned cooked rice', 'a plain photography studio table',
     'the flat paper card rests on the table with its paper edge visible',
     'Photograph a paper card with a printed picture of browned cooked rice; the card itself is the subject.',
     '갈색 누룽지 사진이 인쇄된 종이 카드를 촬영해줘. 주 피사체는 평평한 종이 카드 자체야.'),
    ('empty-rice-pot', 'fire_f116', False, 'object',
     'one empty rice-cooking pot with its bare metal base visible', 'a plain kitchen work table',
     'the empty pot rests open with its continuous bare metal interior visible',
     'Photograph one empty rice-cooking pot showing its bare metal base and open interior.',
     '맨 금속 바닥과 빈 내부가 보이는 빈 밥솥 하나를 촬영해줘.'),
    ('existing-croissant', 'croissant', True, 'food',
     'one freshly baked croissant', 'a plain ceramic serving plate',
     'the croissant rests on the plate with its browned layered surface visible',
     'Photograph one freshly baked croissant on a plain serving plate.',
     '흰 접시 위에 놓인 갓 구운 크루아상 한 개를 촬영해줘.'),
    ('existing-ramen', 'steaming_ramen', True, 'food',
     'one steaming bowl of ramen', 'a plain kitchen work table',
     'steam rises from the ramen while the noodles remain visible inside the bowl',
     'Photograph one steaming bowl of ramen with noodles visible.',
     '면이 보이고 김이 오르는 라멘 한 그릇을 촬영해줘.'),
    ('existing-teacup', 'teacup_vessel_subject', True, 'object',
     'one plain teacup vessel with a joined handle', 'a plain kitchen work table',
     'the empty teacup rests with its curved wall, round opening and joined handle visible',
     'Photograph one plain teacup vessel with its round opening, curved wall and joined handle visible.',
     '둥근 입구와 이어진 손잡이, 곡면 벽이 보이는 찻잔 용기 하나를 촬영해줘.'),
    ('existing-coffee-vessel', 'coffee_cup', True, 'object',
     'one empty coffee cup vessel', 'a plain kitchen work table',
     'the empty coffee cup rests with its cup wall and open interior visible',
     'Photograph one empty coffee cup vessel on a plain kitchen table.',
     '평범한 주방 테이블 위의 빈 커피잔 용기 하나를 촬영해줘.'),
)

def freeze_inputs(request, subject, setting, event, category):
    baseline = (
        f'A natural photograph shows {subject} in {setting}. In the visible scene, {event}. '
        'The declared primary carrier remains clearly separate from nearby objects and background references. '
        'Its continuous outer contour and local surface remain readable within the physical scene. '
        'Soft available light describes the near contours without hiding the surrounding spatial relationships. '
        'A steady view keeps the primary subject and its immediate setting readable together across the frame.'
    )
    raw = fixtures.core(request, subject=subject, setting=setting, event=event,
        interpreted_intent='A photograph of the declared primary carrier in its local setting',
        visual_priorities=(subject, 'readable outer contour'), baseline_prompt_en=baseline)
    raw['semantic_assertions'] = [{'assertion_id':'primary_subject', 'dimension':'subject',
        'polarity':'required', 'source_span_ids':['scope_1'], 'affected_dimensions':['subject'],
        'axes':{'subject_category':category}, 'evidence':{'subject_phrase':subject}}]
    controls = g.creative_controls.resolve(request, context={'subject_category':'nonhuman'},
        overrides={'sensual':0,'fetish':0,'surreal':0,'creativity':1}, seed=43)
    raw['creative_controls_sha256'] = controls['canonical_sha256']
    envelope_raw = fixtures.envelope(request)
    envelope = g.normalize_request_envelope(envelope_raw)
    core = g.normalize_authorial_core(raw, request_envelope=envelope, creative_control_snapshot=controls)
    return {'raw':raw, 'envelope_raw':envelope_raw, 'controls':controls, 'core':core}

class PhotoFoodCarrierRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = g.load_runtime_data(fixtures.SCRIPT_DIR.parent / "assets/photo_prompt_tags.json")

    def check_scene(self, scene):
        name, target, expected, category, subject, setting, event, en, ko = scene
        for language, request in (("EN", en), ("KO", ko)):
            with self.subTest(scene=name, language=language):
                inputs = freeze_inputs(request, subject, setting, event, category)
                core, controls = inputs["core"], inputs["controls"]
                before = copy.deepcopy(core)
                slots, binding, contract = g.retrieve_core_slots(self.data, core, controls)
                self.assertEqual(core, before)
                self.assertEqual(contract["subject_category"], category)
                self.assertEqual(binding["candidate_adoption"], "optional")
                self.assertLessEqual(sum(len(slot["candidates"]) for slot in slots.values()),
                    g.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT)
                candidates = [row["id"] for row in slots.get("subject", {}).get("candidates", [])]
                self.assertEqual("slot:subject:" + target in candidates, expected)
                self.assertEqual(audit.audit_core_retrieval({"slots": slots, "core_retrieval": binding,
                    "authorial_core": core, "creative_controls": controls}, self.data), [])

    def test_cooked_rice_is_food_and_printed_or_empty_carriers_do_not_admit_it(self):
        for scene in SCENES[:3]:
            self.check_scene(scene)

    def test_existing_food_and_vessel_targets_remain_available(self):
        for scene in SCENES[3:]:
            self.check_scene(scene)


if __name__ == "__main__":
    unittest.main()
