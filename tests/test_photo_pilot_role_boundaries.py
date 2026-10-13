"""Carrier confusions discovered by the candidate-centred tagging pilot."""
import copy
import json
from pathlib import Path
import sys
import unittest

SKILL = Path(__file__).resolve().parents[1] / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))

import photo_candidate_corpus as c
import photo_slot_semantics as semantics
import photo_slot_queries as queries
from tests.test_photo_global_retrieval import GlobalDiscoveryTests
from tests.test_photo_slot_queries import synthetic_set

class PilotRoleBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = c.decode((SKILL / "assets/photo_candidate_slot_catalog.json").read_bytes())["slot_catalog"]

    def fit(self, tag, path, target, text, dimension="appearance"):
        record = {"effects": {"dimensions": [dimension], "properties": [
            {"dimension": dimension, "property": path, "target": target}]}}
        return semantics.fit(self.catalog[tag], record, text)["status"]

    def test_eye_axis_does_not_follow_head_rotation_or_eye_shape(self):
        self.assertEqual(self.fit("gaze_direction", "eyes.eyeline", "main_subject", "irises point upward", "expression"), "eligible")
        for path in ("head.orientation", "eyes.pupil_shape", "eyes.closure", "gaze.target", "gaze.engagement"):
            with self.subTest(path=path):
                self.assertEqual(self.fit("gaze_direction", path, "main_subject", "eye direction", "expression"), "incompatible")

    def test_nail_plate_owner_is_separate_from_skin_and_joint_pose(self):
        self.assertEqual(self.fit("nail_appearance", "nails.free_edge.color", "selected_plate", "nail plate light free-edge band"), "review_required")
        self.assertEqual(self.fit("nail_appearance", "nails.free_edge.color", "left_fingernails", "nail plate light free-edge band"), "eligible")
        self.assertEqual(self.fit("nail_appearance", "nails.free_edge.color", "left_nails", "nail plate light free-edge band"), "eligible")
        for path, target in (("skin.marking", "left_hand"), ("hand.joint_pose", "left_hand"), ("nails.color", "image_plane")):
            with self.subTest(path=path, target=target):
                self.assertEqual(self.fit("nail_appearance", path, target, "nails"), "incompatible")

    def test_body_form_is_not_relative_proportion_topology_pose_or_clothing(self):
        self.assertEqual(self.fit("body_form", "body.muscle.contour", "main_subject", "visible muscle contour", "body_geometry"), "eligible")
        for path in ("body.proportion", "body.region", "body.connection", "body.pose", "wardrobe.fit"):
            with self.subTest(path=path):
                self.assertEqual(self.fit("body_form", path, "main_subject", "body form", "body_geometry"), "incompatible")

    def test_apparent_skin_color_keeps_capture_reference_without_identity_inference(self):
        self.assertEqual(self.fit("skin_tone", "body.skin.apparent_color", "main_subject", "apparent skin color under declared light and white balance"), "eligible")
        for path, target in (("makeup.cheek.color", "main_subject"), ("rendering.grade", "image_plane"), ("wardrobe.lining.color", "main_subject")):
            with self.subTest(path=path):
                self.assertEqual(self.fit("skin_tone", path, target, "skin color"), "incompatible")
        self.assertTrue(any("identity" in x for x in self.catalog["skin_tone"]["excludes"]))

    def test_empty_or_wildcard_effects_remain_review_required_for_new_roles(self):
        for tag in ("gaze_direction", "nail_appearance", "body_form"):
            spec = self.catalog[tag]
            for properties in ([], [{"dimension": spec["dimensions"][0], "property": "*", "target": "main_subject"}]):
                with self.subTest(tag=tag, properties=properties):
                    record = {"effects": {"dimensions": spec["dimensions"], "properties": properties}}
                    self.assertEqual(semantics.fit(spec, record, " ".join(spec["evidence_terms"]))["status"], "review_required")

    def test_changed_boundary_invalidates_old_query_context(self):
        GlobalDiscoveryTests.setUpClass()
        core, controls = GlobalDiscoveryTests.core, GlobalDiscoveryTests.controls
        context = synthetic_set(core, controls, self.catalog, ["skin_tone"])
        altered = copy.deepcopy(self.catalog)
        altered["skin_tone"]["description"] += " changed boundary"
        with self.assertRaises(ValueError):
            queries.validate_set(context, core, controls, altered, ["skin_tone"])
        for language in ("en", "ko"):
            texts = [queries.inputs(core, controls, self.catalog, tag, language)[0]
                for tag in ("gaze_direction", "nail_appearance", "body_form")]
            self.assertEqual(len(set(texts)), 3)


if __name__ == "__main__":
    unittest.main()
