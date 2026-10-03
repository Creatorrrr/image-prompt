"""Regression and owner-negative controls for the bounded core retrieval path."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import tarfile
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

    def test_multiple_discovered_options_survive_without_starving_supported_slots(self):
        data, core, controls = self.inputs()
        observed = ["slot:a_detail_034:a_detail_034_0", "slot:a_detail_034:a_detail_034_1"]
        # Isolate admission from discovery scoring. The existing three frozen
        # editing arms separately exercise actual production discovery.
        with mock.patch.object(pg, "candidate_pack_assertion_discovery", return_value=observed):
            slots, binding, _ = pg.retrieve_core_slots(data, core, controls)
        ids = [c["id"] for s in slots.values() for c in s["candidates"]]
        self.assertTrue(set(observed) <= set(ids))
        self.assertTrue({"focus", "texture"} <= set(slots))
        self.assertEqual(len(ids), 64)
        self.assertEqual(len(set(ids)), len(ids))
        self.assertTrue(all(len(s["candidates"]) <= s["candidate_limit"] for s in slots.values()))
        self.assertEqual(binding["candidate_adoption"], "optional")

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

    def core(self, *, partial=True, property_path="viewpoint.direction"):
        raw = fixtures.core("Photograph a blue porcelain teacup viewed from below.",
            baseline_prompt_en="A blue porcelain teacup rests on a dark kitchen counter while delicate rising steam catches rainlit window reflections. The camera views the cup from below, showing its raised rim against the window. The curved handle and soft reflections establish depth, while quiet domestic colors hold the frame together.")
        if partial:
            raw["intent_lock"]["semantic_anchors"].append({
                "anchor_id": "camera_direction", "source_text": raw["source_request"],
                "dimension": "camera", "target": "camera", "property": property_path,
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

    def pack(self, partial=True, *, property_path="viewpoint.direction"):
        core, controls = self.core(partial=partial, property_path=property_path)
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
        # Unknown camera effects must remain unknown for equivalent authored
        # owner paths; no candidate metadata is fitted to one fixture spelling.
        for property_path in ("viewpoint.height_and_direction", "viewpoint.orientation_to_cup"):
            pack = self.pack(property_path=property_path)
            rows = {c["entry_id"]: c for c in pack["slots"]["camera_direction"]["candidates"]}
            with self.subTest(property_path=property_path):
                self.assertTrue(all(rows[name]["applicability"]["status"] == "ineligible"
                                    for name in ("missing", "empty")))
                self.assertEqual(rows["other_dimension"]["applicability"]["status"], "eligible")

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


class PhotoRetrievalSubjectHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_runtime_data()
        cls.cases = json.loads(HOLDOUT.read_text())["category_cases"]

    def inputs(self, case, *, typed=True):
        subject = case["subject"]
        request = f"Photograph {subject} beside a window with a clear surface."
        baseline = (f"A natural photograph shows {subject} beside a window. The subject rests in a quiet arrangement, "
            "with its visible surface clearly described by gentle reflections. Soft light separates the near edge from "
            "the dark surroundings. A restrained background and a steady camera position keep the subject's shape "
            "readable across the whole frame.")
        raw = fixtures.core(request, subject=subject, baseline_prompt_en=baseline,
            interpreted_intent="A clear study of the primary subject and its visible surface",
            setting="a quiet window side arrangement", event="the primary subject rests beside a window",
            visual_priorities=("visible surface reflections", "readable subject shape"))
        if typed:
            raw["semantic_assertions"] = [{"assertion_id": "primary_subject", "dimension": "subject",
                "polarity": "required", "source_span_ids": ["scope_1"], "affected_dimensions": ["subject"],
                "axes": {"subject_category": case["category"]}, "evidence": {"subject_phrase": subject}}]
        context = "human" if case["category"] == "human" else "unspecified" if case["category"] == "unknown" else "nonhuman"
        controls = pg.creative_controls.resolve(request, context={"subject_category": context},
            overrides={"sensual": 0, "fetish": 0}, seed=31)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        return raw, controls

    def normalized(self, raw, controls):
        return pg.normalize_authorial_core(raw,
            request_envelope=pg.normalize_request_envelope(fixtures.envelope(raw["source_request"])),
            creative_control_snapshot=controls)

    def test_typed_categories_preserve_the_surface_slot_boundary_before_ranking(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                raw, controls = self.inputs(case)
                core = self.normalized(raw, controls)
                contract, picked = pg.frozen_core_context(self.data, core, controls)
                self.assertEqual(contract["subject_category"],
                                 "generic" if case["category"] == "unknown" else case["category"])
                count = sum(pg.core_slot_entry_eligible(self.data, core, contract, picked, "surface_material", e)
                            for e in self.data["slots"]["surface_material"])
                self.assertEqual(count > 0, case["surface_allowed"])
                self.assertEqual(core["source_request"], raw["source_request"])
                self.assertEqual(core["baseline_prompt_en"], raw["baseline_prompt_en"])
                self.assertTrue(auditor.authorial_core_v3_semantic_contract_valid(core, creative_control_snapshot=controls))

    def test_coarse_nonhuman_context_does_not_establish_object(self):
        raw, controls = self.inputs(self.cases[0], typed=False)
        core = self.normalized(raw, controls)
        contract, _ = pg.frozen_core_context(self.data, core, controls)
        self.assertEqual(contract["subject_category"], "generic")
        self.assertEqual(pg.slot_block_reason(self.data, "surface_material", contract), "subject_category_not_allowed")

    def test_invalid_or_conflicting_types_fail_normalization_and_independent_audit(self):
        for value in ("nonhuman", "generic", ["object", "animal"]):
            raw, controls = self.inputs(self.cases[0])
            raw["semantic_assertions"][0]["axes"]["subject_category"] = value
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "subject_category"):
                self.normalized(raw, controls)
        raw, controls = self.inputs(self.cases[0])
        other = copy.deepcopy(raw["semantic_assertions"][0])
        other["assertion_id"] = "contradictory_type"
        other["axes"]["subject_category"] = "animal"
        raw["semantic_assertions"].append(other)
        with self.assertRaisesRegex(ValueError, "disagree"):
            self.normalized(raw, controls)
        core = self.normalized(*self.inputs(self.cases[0]))
        core["semantic_assertions"][0]["axes"]["subject_category"] = "nonhuman"
        self.assertFalse(auditor.authorial_core_v3_semantic_contract_valid(core, creative_control_snapshot=controls))

    def test_type_cannot_override_human_or_no_people_context(self):
        raw, _ = self.inputs(self.cases[0])
        controls = pg.creative_controls.resolve(raw["source_request"], context={"subject_category": "human"}, seed=31)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.normalized(raw, controls)
        raw, _ = self.inputs(self.cases[-1])
        controls = pg.creative_controls.resolve(raw["source_request"], context={"subject_category": "human"}, seed=31)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.normalized(raw, controls)
        raw, _ = self.inputs(self.cases[-2])
        controls = pg.creative_controls.resolve(raw["source_request"],
            context={"subject_category": "nonhuman", "no_people": True}, seed=31)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        with self.assertRaisesRegex(ValueError, "conflicts"):
            self.normalized(raw, controls)


class PhotoRetrievalOwnerQueryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(HOLDOUT.read_text())["owner_cases"]

    def inputs(self, case):
        core = {"contract_version": "photo-authorial-core/v3", "canonical_sha256": "f" * 64,
            "source_request": case["evidence"], "subject": "a metal lantern",
            "setting": "a quiet workshop table", "event": "the lantern rests beside metal bolts",
            "baseline_prompt_en": case["evidence"] + ". " + case["irrelevant"],
            "visual_priorities": ["visible metal seams", "readable object shape"],
            "style": {"domain": "general_photo", "family": "quiet object study"},
            "request_binding": {"active_spans": [{"span_id": "request", "text": case["evidence"]}]},
            "semantic_assertions": [], "user_exclusions": [],
            "intent_lock": {"contract_version": "photo-intent-lock/v2", "locked_dimensions": ["subject", "event", "concept"],
                "open_dimensions": ["camera", "lighting"], "semantic_anchors": [{
                    "anchor_id": "owner", "dimension": case["dimension"], "target": case["target"],
                    "property": case["property"], "prompt_evidence": case["evidence"]}]}}
        controls = pg.creative_controls.resolve(core["source_request"],
            context={"subject_category": "nonhuman"}, overrides={"sensual": 0, "fetish": 0}, seed=37)
        core["creative_controls_sha256"] = controls["canonical_sha256"]
        data = {"slots": {case["slot"]: []}, "candidate_semantic_policy": {"slot_dimensions": {
            "light_direction": ["lighting"], "camera_direction": ["camera"], "focus": ["camera"]}}}
        return data, core, controls

    def test_direction_queries_carry_owner_evidence_without_unrelated_scene_prose(self):
        for case in self.cases[:-1]:
            with self.subTest(case=case["id"]):
                data, core, _ = self.inputs(case)
                query, fields = pg.core_slot_focus_text(data, core, case["slot"])
                self.assertEqual(query, case["evidence"])
                self.assertEqual(fields, ["intent_lock.semantic_anchors"])
                self.assertNotIn(case["irrelevant"], query)

    def test_background_source_and_other_carrier_do_not_establish_subject_light_direction(self):
        case = self.cases[-1]
        data, core, controls = self.inputs(case)
        data["slots"]["light_direction"] = [{"id": "wrong_owner", "en": case["evidence"]}]
        query, fields = pg.core_slot_focus_text(data, core, "light_direction")
        self.assertNotIn(case["evidence"], query)
        self.assertNotIn("intent_lock.semantic_anchors", fields)
        slots, _, _ = pg.retrieve_core_slots(data, core, controls)
        self.assertNotIn("light_direction", slots)

    def test_focus_property_is_not_camera_direction_evidence(self):
        case = {**self.cases[2], "property": "focus.sharpness", "evidence": "the rear lantern wick remains sharp"}
        data, core, _ = self.inputs(case)
        query, _ = pg.core_slot_focus_text(data, core, "camera_direction")
        self.assertNotIn(case["evidence"], query)
        focus_query, fields = pg.core_slot_focus_text(data, core, "focus")
        self.assertEqual(focus_query, case["evidence"])
        self.assertEqual(fields, ["intent_lock.semantic_anchors"])

    def test_excluded_owner_phrase_cannot_create_a_positive_slot_query(self):
        case = self.cases[0]
        data, core, controls = self.inputs(case)
        core["user_exclusions"] = [case["evidence"]]
        data["slots"][case["slot"]] = [{"id": "excluded", "en": case["evidence"]}]
        self.assertEqual(pg.core_slot_focus_text(data, core, case["slot"]), ("", []))
        self.assertNotIn(case["slot"], pg.retrieve_core_slots(data, core, controls)[0])

    def test_new_upward_scene_survives_broad_focal_intersection(self):
        case = self.cases[2]
        data, core, controls = self.inputs(case)
        data["slots"][case["slot"]] = [
            {"id": "upward", "en": "the camera looks upward from below the weather vane"},
            {"id": "distractor", "en": "quiet object study visible metal seams"},
        ]
        slots, _, _ = pg.retrieve_core_slots(data, core, controls)
        self.assertEqual({c["entry_id"] for c in slots[case["slot"]]["candidates"]}, {"upward"})

    def test_frozen_property_arm_retrieves_existing_upward_and_backlight_coverage(self):
        data = pg.load_runtime_data()
        root = Path(__file__).resolve().parents[1]
        archive = root / "docs/research-evidence/photo-prompt/renewed-blind-scene-retrieval-20261003/diagnostic-evidence.tar.gz"
        with tarfile.open(archive) as tar:
            for n, slot, expected in ((1, "light_direction", {"backlight", "pe_rear_rim"}),
                    (6, "camera_direction", {"worms_eye", "extreme_low_angle_under_subject", "extreme_low_hero_angle"})):
                path = f"public-cli-property/inputs/blind_scene_{n:03d}"
                inputs = {name: json.load(tar.extractfile(f"{path}/{name}.json"))
                          for name in ("authorial-core", "creative-controls", "request-envelope")}
                controls = inputs["creative-controls"]
                core = pg.normalize_authorial_core(inputs["authorial-core"],
                    request_envelope=pg.normalize_request_envelope(inputs["request-envelope"]),
                    creative_control_snapshot=controls)
                before = copy.deepcopy(core)
                slots, _, _ = pg.retrieve_core_slots(data, core, controls)
                ids = {c["entry_id"] for c in slots.get(slot, {}).get("candidates", [])}
                self.assertTrue(ids & expected, (n, slot, ids))
                self.assertEqual(core, before)


if __name__ == "__main__":
    unittest.main()
