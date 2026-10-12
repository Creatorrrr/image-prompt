"""Source-informed animal admission checks; these do not test rendered images."""
from __future__ import annotations

import copy
import unittest

from tests import photo_prompt_fixtures as fixtures
import audit_composed_prompt as audit
import prompt_generator as g


ANIMALS = (
    ("soil_e077", "one live earthworm", "damp soil beside a small burrow entrance",
     "the earthworm moves over the soil",
     "Macro photograph of one live earthworm on damp soil beside a small burrow entrance.",
     "젖은 흙의 작은 굴 입구 옆에 있는 살아 있는 지렁이 한 마리를 접사로 촬영해줘."),
    ("soil_e078", "one live ant", "a soil nest entrance with loose grains nearby",
     "the ant moves beside the nest entrance",
     "Macro photograph of one live ant beside a soil nest entrance with loose grains nearby.",
     "느슨한 흙 알갱이가 있는 흙 둥지 입구 옆의 살아 있는 개미 한 마리를 접사로 촬영해줘."),
    ("electric_eel_freshwater_visible_form", "one live electric eel",
     "a shallow freshwater habitat", "the electric eel swims through freshwater",
     "Photograph one live electric eel swimming in a freshwater habitat.",
     "담수 서식 환경에서 헤엄치는 살아 있는 전기뱀장어 한 마리를 촬영해줘."),
)


class PhotoAnimalSubjectRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = g.load_json(fixtures.SCRIPT_DIR.parent / "assets/photo_prompt_tags.json")

    def retrieve(self, request, subject, setting, event, category):
        baseline = (
            f"A natural photograph shows {subject} in {setting}. In the visible scene, {event}. "
            "The primary subject remains clearly separated from the nearby surface, and its outer shape is resolved. "
            "Soft available light describes the near contours without hiding the surrounding spatial relationships. "
            "A steady view keeps the primary subject and the local setting readable together across the frame."
        )
        raw = fixtures.core(request, subject=subject, setting=setting, event=event,
            interpreted_intent="A photographic study of the declared primary subject in its local setting",
            visual_priorities=(subject, "readable outer shape"), baseline_prompt_en=baseline)
        raw["semantic_assertions"] = [{
            "assertion_id": "primary_subject", "dimension": "subject", "polarity": "required",
            "source_span_ids": ["scope_1"], "affected_dimensions": ["subject"],
            "axes": {"subject_category": category}, "evidence": {"subject_phrase": subject},
        }]
        controls = g.creative_controls.resolve(request, context={"subject_category": "nonhuman"},
            overrides={"sensual": 0, "fetish": 0, "surreal": 0, "creativity": 1}, seed=41)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        core = g.normalize_authorial_core(raw,
            request_envelope=g.normalize_request_envelope(fixtures.envelope(request)),
            creative_control_snapshot=controls)
        before = copy.deepcopy(core)
        slots, binding, contract = g.retrieve_core_slots(self.data, core, controls)
        self.assertEqual(core, before)
        self.assertEqual(contract["subject_category"], category)
        self.assertEqual(binding["candidate_adoption"], "optional")
        self.assertLessEqual(sum(len(slot["candidates"]) for slot in slots.values()),
            g.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT)
        self.assertEqual(audit.audit_core_retrieval({"slots": slots, "core_retrieval": binding,
            "authorial_core": core, "creative_controls": controls}, self.data), [])
        return [row["id"] for row in slots.get("subject", {}).get("candidates", [])]

    def test_live_animal_targets_are_admitted_for_english_and_korean_requests(self):
        for entry_id, subject, setting, event, en, ko in ANIMALS:
            for language, request in (("EN", en), ("KO", ko)):
                with self.subTest(animal=entry_id, language=language):
                    candidates = self.retrieve(request, subject, setting, event, "animal")
                    self.assertIn("slot:subject:" + entry_id, candidates)

    def test_a_printed_animal_photograph_does_not_admit_the_live_animal_target(self):
        for entry_id, subject, *_ in ANIMALS:
            printed = "one printed photograph of " + subject
            request = "Photograph " + printed + " on a flat paper card in a quiet photography studio."
            with self.subTest(animal=entry_id):
                candidates = self.retrieve(request, printed, "a quiet photography studio",
                    "the paper card rests on a flat surface", "object")
                self.assertNotIn("slot:subject:" + entry_id, candidates)


if __name__ == "__main__":
    unittest.main()
