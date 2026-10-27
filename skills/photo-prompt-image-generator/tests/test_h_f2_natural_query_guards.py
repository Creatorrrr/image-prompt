"""Held-out behavioral guards for generic H-F2 query/source matching.

Run against an implementation directory containing both helper modules with:
    H_F2_HELPER_DIR=/path/to/helper-overlay python -m unittest \
      generated/trend-scout/raw/reactorprompt-pose-composition-20261026/remaining-20261027/guards/test_query_source_guard_minipairs.py

The cases assert observable source/effect ownership and ranking outcomes. They
do not inspect implementation patterns or query benchmark/CID results.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[3]
HELPER_DIR = Path(os.environ.get(
    "H_F2_HELPER_DIR",
    ROOT / "skills/photo-prompt-image-generator/scripts",
)).resolve()
sys.path.insert(0, str(HELPER_DIR))

from photo_h_f2_source_relevance import compile_profiles, order_source_relevance  # noqa: E402
from photo_h_f2_single_property import query_recognizer, source_witness  # noqa: E402


class QuerySourceGuardMinipairs(unittest.TestCase):
    def evaluate(self, query, identity_to_texts, identity_to_effects, selected="case|r1"):
        units = {}
        for identity, text_rows in identity_to_texts.items():
            digest = hashlib.sha256(text_rows[0][1].encode("utf-8")).hexdigest()
            units[identity] = [
                {
                    "pointer": pointer,
                    "text": text,
                    "literal_id": f"{identity}:{index}",
                    "source_sha256": digest,
                    "candidate_id": identity.split("|", 1)[0],
                    "realization_id": identity.split("|", 1)[1],
                }
                for index, (pointer, text) in enumerate(text_rows)
            ]
        profiles = compile_profiles(
            {identity: "" for identity in units},
            source_units=lambda identity: units[identity],
            source_effects=lambda identity: identity_to_effects.get(identity, {}),
        )
        row = {"id": selected, "cid": selected.split("|", 1)[0],
               "rid": selected.split("|", 1)[1], "rrf": 0.01,
               "bm25": 1.0, "cosine": 0.5}
        ordered, trace = order_source_relevance([row], query, profiles)
        self.assertEqual(ordered, [row])
        self.assertFalse(trace["candidate_filter"])
        self.assertFalse(trace["query_rewritten"])
        self.assertFalse(trace["embedding_input_changed"])
        self.assertEqual(trace.get("additional_search_calls", 0), 0)
        self.assertFalse(trace["native_approval"])
        self.assertFalse(trace["semantic_approval"])
        return units, trace

    def witness_features(self, trace, identity="case|r1"):
        witness = next((item for item in trace.get("top8_source_witnesses", [])
                        if item.get("id") == identity), {})
        return witness.get("supported_features", [])

    def assert_rankable(self, trace):
        self.assertGreater(trace.get("candidates_rankable", 0), 0)
        self.assertGreater(
            sum(item.get("source_lane_contribution", 0.0)
                for item in trace.get("top8_source_witnesses", [])),
            0.0,
        )

    def assert_not_rankable(self, trace):
        self.assertEqual(trace.get("candidates_rankable", 0), 0)
        self.assertEqual(
            sum(item.get("source_lane_contribution", 0.0)
                for item in trace.get("top8_source_witnesses", [])),
            0.0,
        )

    def assert_exact_primary_effect_witnesses(self, trace, identity, text,
                                             expected_feature_ids=None):
        features = self.witness_features(trace, identity)
        if expected_feature_ids is not None:
            features = [feature for feature in features
                        if feature.get("feature_id") in expected_feature_ids]
            self.assertEqual({feature.get("feature_id") for feature in features},
                             set(expected_feature_ids))
        self.assertTrue(features)
        for feature in features:
            source = feature.get("source") or {}
            self.assertEqual(source.get("pointer"), "/content/en")
            self.assertTrue(source.get("effect_properties"), feature)
            self.assertEqual(source.get("source_unit"), text)
            for span in source.get("relation_witnesses", []):
                self.assertEqual(text[span["start"]:span["end"]], span["quote"])

    @staticmethod
    def props(*pairs):
        return {"properties": [
            {"dimension": "pose_or_composition", "property": path, "target": target}
            for path, target in pairs
        ]}

    def test_body_direction_and_gaze_need_both_facts_on_the_same_primary_rid(self):
        query = "Is the woman's body facing the camera while her eyes look toward a window?"
        full = "The woman's body faces the camera while her eyes look toward a window."
        effects = self.props(
            ("body.orientation.direction", "body faces camera"),
            ("eyes.gaze.direction", "eyes look away from lens"),
        )
        units, trace = self.evaluate(query, {"case|r1": [("/content/en", full)]},
                                     {"case|r1": effects})
        self.assertGreaterEqual(len(trace.get("recognized_features", [])), 2)
        self.assert_rankable(trace)
        self.assert_exact_primary_effect_witnesses(
            trace, "case|r1", full, {"body_orientation", "gaze_direction"})

        one_fact = "The woman's body faces the camera; a window is visible behind her."
        _, partial = self.evaluate(query, {"case|r1": [("/content/en", one_fact)]},
                                   {"case|r1": self.props(
                                       ("body.orientation.direction", "body faces camera"),
                                       ("eyes.gaze.direction", "eyes look away from lens"),
                                   )})
        self.assert_not_rankable(partial)

        # The right effect exists, but only on another RID. It must not fill
        # the selected RID's missing gaze property.
        _, cross_rid = self.evaluate(
            query,
            {"case|r1": [("/content/en", one_fact)],
             "case|r2": [("/content/en", "The subject looks away from the lens.")]},
            {"case|r1": self.props(("body.orientation.direction", "body faces camera")),
             "case|r2": self.props(("eyes.gaze.direction", "eyes look away from lens"))},
        )
        self.assert_not_rankable(cross_rid)

    def test_natural_lens_destination_in_gaze_is_not_a_focal_length_requirement(self):
        query = "Is the woman's body facing the camera while her eyes look away from the lens?"
        source = "The woman's body faces the camera while her eyes look away from the lens."
        effects = self.props(("body.orientation.direction", "body faces camera"),
                             ("eyes.gaze.direction", "eyes look away from lens"))
        _, good = self.evaluate(query, {"case|r1": [("/content/en", source)]},
                                {"case|r1": effects})
        self.assert_rankable(good)
        self.assert_exact_primary_effect_witnesses(
            good, "case|r1", source, {"body_orientation", "gaze_direction"})

        wrong_owner = "The woman's body faces the camera; the portrait uses an 85 mm lens."
        _, bad = self.evaluate(
            query, {"case|r1": [("/content/en", wrong_owner)]},
            {"case|r1": self.props(("body.orientation.direction", "body faces camera"),
                                    ("camera.focal_length", "85 mm lens"))},
        )
        self.assert_not_rankable(bad)

    def test_open_head_or_frame_alternative_accepts_either_explicit_answer(self):
        recognized = query_recognizer(
            "Is the woman's head tilted, or is the image frame tilted?"
        )
        self.assertEqual(recognized["kind"], "tilt_owner_disambiguation")
        branches = (
            ("The woman's head is tilted while the image frame stays level.",
             self.props(("pose.head.orientation.tilted", "woman's head")), "head_tilt"),
            ("The image frame is canted while the woman's head stays level.",
             self.props(("camera.roll.tilted_horizon", "image frame relative to horizon")),
             "frame_roll"),
        )
        for text, effects, expected_state in branches:
            with self.subTest(state=expected_state):
                units = [{"pointer": "/content/en", "literal_id": "primary", "text": text,
                          "source_sha256": "a" * 64, "candidate_id": "case",
                          "realization_id": "r1"}]
                result = source_witness(recognized["kind"], units, effects)
                self.assertTrue(result and result.get("promoted"))
                self.assertEqual(result["state"], expected_state)
                self.assertEqual(len(result.get("effect_witnesses", [])), 1)
                self.assertEqual(text[result["source_span"]["start"]:
                                      result["source_span"]["end"]], result["source_quote"])
                for span in result.get("evidence_spans", []):
                    self.assertEqual(text[span["start"]:span["end"]], span["quote"])

    def test_strong_answer_effect_cannot_leak_across_selected_rids(self):
        query = "Is the woman's head tilted, or is the image frame tilted?"
        text = "The woman's head is tilted while the image frame stays level."
        identities = ("case|r1", "case|r2")
        units = {
            identity: [{"pointer": "/content/en", "literal_id": f"{identity}:en",
                        "text": text, "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
                        "candidate_id": "case", "realization_id": identity.split("|")[1]}]
            for identity in identities
        }
        effects = {
            "case|r1": self.props(("camera.roll.tilted_horizon", "image frame relative to horizon")),
            "case|r2": self.props(("pose.head.orientation.tilted", "woman's head")),
        }
        profiles = compile_profiles(
            {identity: "" for identity in identities},
            source_units=lambda identity: units[identity],
            source_effects=lambda identity: effects[identity],
        )
        rows = [
            {"id": identity, "cid": "case", "rid": identity.split("|")[1],
             "rrf": 0.01, "bm25": 1.0, "cosine": 0.5}
            for identity in identities
        ]
        ordered, trace = order_source_relevance(rows, query, profiles)
        self.assertEqual([row["id"] for row in ordered], ["case|r2", "case|r1"])
        lane = trace.get("single_property_lane", {})
        self.assertTrue(lane.get("effects_read_from_same_selected_rid_profile"))
        self.assertTrue(lane.get("query_property_value_unbound"))
        self.assertTrue(lane.get("query_alternatives_unbound"))
        self.assertEqual(lane.get("source_witness_candidate_count"), 1)
        self.assertEqual([row["id"] for row in lane.get("top8_witnesses", [])], ["case|r2"])

    def test_bilateral_arms_do_not_reduce_to_one_arm_or_an_unrelated_arm_action(self):
        query = "Are both arms raised while the woman's knees stay bent?"
        props = self.props(("arms.position.bilateral", "both arms raised"),
                           ("legs.knee.position", "knees bent"))
        positive = "The woman raises both arms and keeps her knees bent."
        _, good = self.evaluate(query, {"case|r1": [("/content/en", positive)]},
                                {"case|r1": props})
        self.assert_rankable(good)

        for text in (
            "The woman raises only one arm and keeps her knees bent.",
            "The woman hangs both arms at her sides and keeps her knees bent.",
        ):
            with self.subTest(text=text):
                _, trace = self.evaluate(query, {"case|r1": [("/content/en", text)]},
                                         {"case|r1": props})
                self.assert_not_rankable(trace)

    def test_advisory_negation_keeps_its_explicit_negative_answer_polarity(self):
        query = "Is the woman's body facing the camera while her eyes look toward a window?"
        text = "The woman's body faces away from the camera while her eyes look toward a window."
        _, trace = self.evaluate(
            query, {"case|r1": [("/content/en", text)]},
            {"case|r1": self.props(("body.orientation.direction", "body faces away"),
                                    ("eyes.gaze.direction", "eyes look toward lens"))},
        )
        self.assertTrue(trace.get("recognized_features"))
        body = next(feature for feature in self.witness_features(trace)
                    if feature.get("feature_id") == "body_orientation")
        self.assertEqual(body["query"].get("polarity"), "unbound")
        self.assertEqual(body["source"].get("source_polarity"), "negative")
        self.assertFalse(trace.get("semantic_controller_verified"))

    def test_single_property_uncertainty_quotes_and_negation_are_not_strong_answers(self):
        kind = "tilt_owner_disambiguation"
        effect = self.props(("camera.roll.tilted_horizon", "image frame relative to horizon"))
        texts = (
            "The frame is not tilted while the head remains level.",
            "The frame may be tilted while the head remains level.",
            'The caption says “the frame is tilted rather than the head.”',
        )
        for text in texts:
            with self.subTest(text=text):
                units = [{"pointer": "/content/en", "literal_id": "primary", "text": text,
                          "source_sha256": "a" * 64, "candidate_id": "case",
                          "realization_id": "r1"}]
                result = source_witness(kind, units, effect)
                self.assertFalse(result and result.get("promoted"))

    def test_effect_only_cannot_create_direct_source_support(self):
        query = "Is the woman's body facing the camera while her eyes look toward a window?"
        effects = self.props(("body.orientation.direction", "body faces camera"),
                             ("eyes.gaze.direction", "eyes look away from lens"))
        _, effect_only = self.evaluate(
            query, {"case|r1": [("/content/en", "A woman stands beside a window.")]},
            {"case|r1": effects},
        )
        self.assert_not_rankable(effect_only)

        text = "The woman's body faces the camera while her eyes look toward a window."
        _, text_only = self.evaluate(
            query, {"case|r1": [("/content/en", text)]},
            {"case|r1": self.props(("head.orientation.direction", "head toward camera"),
                                    ("camera.height", "camera at eye level"))},
        )
        self.assertGreater(text_only.get("candidates_with_primary_support", 0), 0)
        self.assertFalse(text_only.get("semantic_controller_verified"))
        for feature in self.witness_features(text_only):
            self.assertFalse((feature.get("source") or {}).get("effect_properties"))

    def test_knee_position_is_not_established_by_a_low_camera_or_floor_context(self):
        query = "Are the woman's knees bent while the camera is at a low angle?"
        source = "The woman's knees are bent, and the camera is positioned at a low angle."
        props = self.props(("legs.knee.position", "knees bent"),
                           ("camera.height", "camera at a low angle"))
        _, good = self.evaluate(query, {"case|r1": [("/content/en", source)]},
                                {"case|r1": props})
        self.assert_rankable(good)

        floor_only = "The woman is in a room, and the camera is positioned at a low angle."
        _, bad = self.evaluate(query, {"case|r1": [("/content/en", floor_only)]},
                               {"case|r1": props})
        self.assert_not_rankable(bad)

    def test_natural_knee_position_question_does_not_become_person_frame_placement(self):
        query = "Where are the woman's knees positioned, and how high is the camera?"
        source = "The woman's knees are bent, and the camera is positioned at floor level."
        props = self.props(("legs.knee.position", "knees bent"),
                           ("camera.height", "camera at floor level"))
        _, good = self.evaluate(query, {"case|r1": [("/content/en", source)]},
                                {"case|r1": props})
        self.assert_rankable(good)
        self.assert_exact_primary_effect_witnesses(
            good, "case|r1", source, {"knee_state", "camera_height"})

        wrong_owner = "The woman is positioned at frame left, and the camera is positioned at floor level."
        _, bad = self.evaluate(
            query, {"case|r1": [("/content/en", wrong_owner)]},
            {"case|r1": self.props(("layout.subject_position", "person at frame left"),
                                    ("camera.height", "camera at floor level"))},
        )
        self.assert_not_rankable(bad)

    def test_person_placement_and_open_landscape_remain_distinct_relations(self):
        query = "Where is the person placed in the frame, and what landscape is visible behind them?"
        source = "The woman is positioned at frame left, with an open field visible behind her."
        props = self.props(("layout.subject_position", "person at frame left"),
                           ("spatial.background_context", "open field behind person"))
        _, good = self.evaluate(query, {"case|r1": [("/content/en", source)]},
                                {"case|r1": props})
        self.assert_rankable(good)

        landscape_only = "An open field is visible behind the woman; her frame position is not specified."
        _, bad = self.evaluate(query, {"case|r1": [("/content/en", landscape_only)]},
                               {"case|r1": props})
        self.assert_not_rankable(bad)

    def test_stair_line_and_camera_viewpoint_require_separate_support(self):
        query = "What leading line do the stairs form, and from what camera angle was the scene photographed?"
        source = "The stairs rise diagonally across the frame, photographed from a high camera angle."
        props = self.props(("composition.leading_lines", "stairs form a diagonal line"),
                           ("camera.angle", "high angle"))
        _, good = self.evaluate(query, {"case|r1": [("/content/en", source)]},
                                {"case|r1": props})
        self.assert_rankable(good)

        viewpoint_only = "The stairs are visible in the room, photographed from a high camera angle."
        _, bad = self.evaluate(query, {"case|r1": [("/content/en", viewpoint_only)]},
                               {"case|r1": props})
        self.assert_not_rankable(bad)

    def test_hand_frame_occupancy_is_not_anatomical_size_or_bent_arm(self):
        query = "Does the foreground hand occupy most of the frame?"
        source = "The foreground hand occupies a large portion of the image."
        props = self.props(("frame_occupancy.subject", "foreground hand occupies most of frame"))
        _, good = self.evaluate(query, {"case|r1": [("/content/en", source)]},
                                {"case|r1": props})
        self.assert_exact_primary_effect_witnesses(
            good, "case|r1", source, {"frame_occupancy"})

        anatomy_only = "The woman has a large hand and bends her arm at the elbow."
        _, bad = self.evaluate(query, {"case|r1": [("/content/en", anatomy_only)]},
                               {"case|r1": props})
        self.assertFalse(any(feature.get("feature_id") == "frame_occupancy"
                             for feature in self.witness_features(bad)))

    def test_natural_hand_occupancy_and_background_blur_are_not_visibility(self):
        query = "Does the foreground hand occupy most of the frame while the background stays blurred?"
        source = "The foreground hand takes up most of the frame; the background stays blurred."
        effects = self.props(("frame_occupancy.subject", "foreground hand occupies most of frame"),
                             ("focus.background", "background blurred"))
        _, good = self.evaluate(query, {"case|r1": [("/content/en", source)]},
                                {"case|r1": effects})
        self.assert_rankable(good)
        self.assert_exact_primary_effect_witnesses(
            good, "case|r1", source, {"frame_occupancy", "focus_plane"})

        wrong_owner = "The woman's hand is anatomically large, with a landscape visible behind her."
        _, bad = self.evaluate(
            query, {"case|r1": [("/content/en", wrong_owner)]},
            {"case|r1": self.props(("frame_occupancy.subject", "hand is anatomically large"),
                                    ("spatial.background_context", "landscape visible behind woman"))},
        )
        self.assert_not_rankable(bad)

    def test_face_focus_does_not_transfer_from_background_focus(self):
        query = "Is the woman's face sharp?"
        face_sharp = "The woman's face is sharp while the background is blurred."
        _, good = self.evaluate(query, {"case|r1": [("/content/en", face_sharp)]},
                                {"case|r1": self.props(
                                    ("focus.face", "face sharp"),
                                    ("focus.background", "background blurred"),
                                )})
        self.assertIn("focus_plane", {feature.get("id")
                                       for feature in good.get("recognized_features", [])})
        self.assertNotIn("body_orientation", {feature.get("id")
                                               for feature in good.get("recognized_features", [])})
        self.assertNotIn("head_orientation", {feature.get("id")
                                              for feature in good.get("recognized_features", [])})
        self.assert_exact_primary_effect_witnesses(
            good, "case|r1", face_sharp, {"focus_plane"})

        swapped = "The woman's face is blurred while the background is sharp."
        _, bad = self.evaluate(query, {"case|r1": [("/content/en", swapped)]},
                               {"case|r1": self.props(
                                   ("focus.face", "face blurred"),
                                   ("focus.background", "background sharp"),
                               )})
        self.assertFalse(any(feature.get("feature_id") == "focus_plane"
                             for feature in self.witness_features(bad)))

        hand_query = "Is the foreground hand sharp?"
        background_only = "The foreground hand is blurred while the background is sharp."
        _, hand_bad = self.evaluate(
            hand_query, {"case|r1": [("/content/en", background_only)]},
            {"case|r1": self.props(("focus.hand", "foreground hand blurred"),
                                    ("focus.background", "background sharp"))},
        )
        self.assertFalse(any(feature.get("feature_id") == "focus_plane"
                             for feature in self.witness_features(hand_bad)))

    def test_still_life_arrangement_requires_a_direct_layout_fact(self):
        query = "How are the ingredients arranged within the frame?"
        source = "Tomatoes and herbs are arranged in a balanced still life across the frame."
        effects = self.props(("layout.still_life.arrangement", "ingredients balanced across frame"))
        _, good = self.evaluate(query, {"case|r1": [("/content/en", source)]},
                                {"case|r1": effects})
        self.assertTrue(self.witness_features(good))
        self.assert_exact_primary_effect_witnesses(
            good, "case|r1", source, {"composition_layout"})

        inventory_only = "The still life contains tomatoes, herbs, and bowls in the frame."
        _, bad = self.evaluate(query, {"case|r1": [("/content/en", inventory_only)]},
                               {"case|r1": effects})
        self.assertFalse(self.witness_features(bad))

    def test_frame_tilt_query_does_not_accept_head_tilt(self):
        query = "Is the image frame tilted?"
        text = "The woman's head is tilted while the image frame stays level."
        _, trace = self.evaluate(
            query, {"case|r1": [("/content/en", text)]},
            {"case|r1": self.props(("pose.head.orientation.tilted", "woman's head"))},
        )
        self.assertFalse(self.witness_features(trace))

        # The direct single-property path must likewise require an effect for
        # the observed owner state, rather than accepting whichever tilt path
        # happens to exist on the selected RID.
        recognized = query_recognizer(
            "Is the woman's head tilted, or is the image frame tilted?"
        )
        self.assertEqual(recognized["kind"], "tilt_owner_disambiguation")
        units = [{"pointer": "/content/en", "literal_id": "primary", "text": text,
                  "source_sha256": "a" * 64, "candidate_id": "case", "realization_id": "r1"}]
        wrong_effect = source_witness(
            recognized["kind"], units,
            self.props(("camera.roll.tilted_horizon", "image frame relative to horizon")),
        )
        self.assertFalse(wrong_effect and wrong_effect.get("promoted"))

    def test_frame_roll_is_not_subject_body_rotation(self):
        query = "Is the camera frame rolled?"
        text = "The woman turns her body to the side while the image frame stays level."
        _, trace = self.evaluate(
            query, {"case|r1": [("/content/en", text)]},
            {"case|r1": self.props(("body.orientation.direction", "woman turned to the side"))},
        )
        self.assertFalse(self.witness_features(trace))


if __name__ == "__main__":
    unittest.main()
