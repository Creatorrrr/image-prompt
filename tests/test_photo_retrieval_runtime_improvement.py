"""Regression and owner-negative controls for the bounded core retrieval path."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest
from unittest import mock

from tests import photo_prompt_fixtures as fixtures
import audit_composed_prompt as auditor
import prompt_generator as pg


HOLDOUT = Path(__file__).parent / "fixtures/photo_prompt/retrieval_runtime_holdout_v1.json"


class PhotoRetrievalAdmissionTests(unittest.TestCase):
    def inputs(self):
        raw = fixtures.core("Photograph a copper lantern with a legible wick and a rough surface.",
            subject="a copper lantern", event="the copper lantern rests on a rough surface",
            visual_priorities=("copper lantern wick", "rough copper surface"),
            baseline_prompt_en="A copper lantern rests on a rough surface beside an open window. The copper lantern wick is clearly legible through the glass, and the rough copper surface catches a gentle sheen. A dark tabletop supports the quiet still life. Soft window light reveals the shallow dents and preserves the warm metal color across the frame.")
        controls = pg.creative_controls.resolve(raw["source_request"],
            context={"subject_category": "nonhuman"}, overrides={"sensual": 0, "fetish": 0}, seed=19)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        core = pg.normalize_authorial_core(raw,
            request_envelope=pg.normalize_request_envelope(fixtures.envelope(raw["source_request"])),
            creative_control_snapshot=controls)
        names = [f"a_detail_{n:03d}" for n in range(35)] + ["focus", "texture"]
        data = {"slots": {s: [{"id": f"{s}_{n}", "en": "copper lantern wick rough surface"}
                              for n in range(3)] for s in names},
                "candidate_semantic_policy": {"slot_dimensions": {s: ["material"] for s in names}}}
        return data, core, controls

    def test_late_supported_slots_get_admission_without_increasing_budget(self):
        data, core, controls = self.inputs()
        slots, binding, _ = pg.retrieve_core_slots(data, core, controls)
        self.assertIn("focus", slots)
        self.assertIn("texture", slots)
        ids = [c["id"] for s in slots.values() for c in s["candidates"]]
        self.assertEqual(len(ids), 64)
        self.assertEqual(len(set(ids)), len(ids))
        self.assertTrue(all(len(s["candidates"]) <= s["candidate_limit"] for s in slots.values()))
        self.assertTrue(all(s["candidates"] for s in slots.values()))
        self.assertEqual(binding["candidate_adoption"], "optional")
        self.assertEqual(binding["candidate_allocation"], "one_supported_hit_per_slot_per_round")

    def test_source_iteration_order_does_not_change_admission(self):
        data, core, controls = self.inputs()
        expected = pg.retrieve_core_slots(data, core, controls)
        data["slots"] = dict(reversed(list(data["slots"].items())))
        self.assertEqual(pg.retrieve_core_slots(data, core, controls), expected)

    def test_empty_or_guarded_slots_do_not_receive_a_quota(self):
        data, core, controls = self.inputs()
        data["slots"]["texture"] = [{"id": "unrelated", "en": "interplanetary navigation"}]
        data["slots"]["focus"] = [{"id": "blocked", "en": "copper lantern wick rough surface",
                                    "requires_all": ["missing_primary_context"]}]
        data["slots"]["unowned"] = [{"id": "padding", "en": "copper lantern wick rough surface"}]
        slots, _, _ = pg.retrieve_core_slots(data, core, controls)
        self.assertFalse({"texture", "focus", "unowned"} & set(slots))


class PhotoRetrievalPropertyEligibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_runtime_data()

    def core(self, *, partial=True):
        raw = fixtures.core("Photograph a blue porcelain teacup viewed from below.",
            baseline_prompt_en="A blue porcelain teacup rests on a dark kitchen counter while delicate rising steam catches rainlit window reflections. The camera views the cup from below, showing its raised rim against the window. The curved handle and soft reflections establish depth, while quiet domestic colors hold the frame together.")
        if partial:
            raw["intent_lock"]["semantic_anchors"].append({
                "anchor_id": "camera_direction", "source_text": raw["source_request"],
                "dimension": "camera", "target": "camera", "property": "viewpoint.direction",
                "prompt_evidence": "The camera views the cup from below",
            })
        controls = pg.creative_controls.resolve(raw["source_request"],
            context={"subject_category": "nonhuman"}, overrides={"sensual": 0, "fetish": 0}, seed=19)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        core = pg.normalize_authorial_core(raw,
            request_envelope=pg.normalize_request_envelope(fixtures.envelope(raw["source_request"])),
            creative_control_snapshot=controls)
        return core, controls

    def corpus(self):
        entries = []
        for name, dimension, target, prop in (
            ("missing", "camera", None, None),
            ("empty", "camera", None, None),
            ("other_target", "camera", "background_camera", "viewpoint.direction"),
            ("other_property", "camera", "camera", "focus.depth"),
            ("parent_overlap", "camera", "camera", "viewpoint"),
            ("cross_carrier_overlap", "lighting", "camera", "viewpoint.direction"),
            ("other_dimension", "lighting", None, None),
        ):
            entry = {"id": name, "en": "blue porcelain teacup viewed from below",
                     "affected_dimensions": [dimension]}
            if name != "missing" and name != "other_dimension":
                entry["affected_properties"] = ([{"dimension": dimension, "target": target, "property": prop}] if target else [])
            entries.append(entry)
        return {**self.data, "slots": {"camera_direction": entries}}

    def pack(self, partial=True):
        core, controls = self.core(partial=partial)
        # Exercise every effect control in the same pack, independently of the
        # production admission limits tested below.
        with mock.patch.object(pg, "candidate_pack_slot_limit", return_value=8):
            return pg.generate_candidate_pack(self.corpus(), core, controls,
                fixtures.review(core["baseline_prompt_en"]), seed=19)

    def test_missing_and_empty_effects_do_not_claim_partial_lock_compatibility(self):
        pack = self.pack()
        rows = {c["entry_id"]: c for c in pack["slots"]["camera_direction"]["candidates"]}
        # Query rank is irrelevant: every returned unknown or overlapping effect
        # must be annotated, including a lock carried through another dimension.
        for name, row in rows.items():
            with self.subTest(entry=name):
                self.assertEqual(row["applicability"]["status"],
                    "eligible" if name in {"other_target", "other_property", "other_dimension"} else "ineligible")
        self.assertIn("missing", rows)
        self.assertIn("empty", rows)

    def test_no_property_lock_preserves_legacy_eligibility(self):
        pack = self.pack(partial=False)
        self.assertTrue(all(c["applicability"]["status"] == "eligible"
                            for c in pack["slots"]["camera_direction"]["candidates"]))

    def test_selection_audit_rechecks_unknown_source_scope_even_if_annotation_is_forged(self):
        pack = self.pack()
        row = next(c for c in pack["slots"]["camera_direction"]["candidates"] if c["entry_id"] == "missing")
        row["applicability"]["status"] = "eligible"
        with mock.patch.object(pg, "load_json", return_value=self.corpus()):
            failures = auditor.audit_candidate_semantic_contracts(pack, pack["authorial_core"]["baseline_prompt_en"],
                {row["id"]}, {row["id"]: row}, [{"candidate_id": row["id"]}])
        self.assertTrue(any("property effects" in f["reason"] for f in failures), failures)


if __name__ == "__main__":
    unittest.main()
