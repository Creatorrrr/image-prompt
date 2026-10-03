"""Frozen scene, fresh bilingual owner holdouts, and authoring entry-point checks."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest import mock

from tests import photo_prompt_fixtures as fixtures
import generate_photo_prompt as cli
import photo_camera_evidence as camera
import prompt_generator as pg


ROOT = Path(__file__).resolve().parents[1]
HOLDOUT = ROOT / "tests/fixtures/photo_prompt/camera_owned_clause_holdout_v1.json"
HOLDOUT_SHA256 = "49949e329be314f81c2f49205266a85967a4a01f4670076fd5c8b7f81c1b6f0a"


class CameraOwnedClauseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(HOLDOUT.read_text())["cases"]

    def query_core(self, case):
        return {**case, "contract_version": "photo-authorial-core/v3",
                "intent_lock": {"semantic_anchors": []}, "semantic_assertions": [],
                "visual_priorities": ["clear object shape", "natural surface detail"],
                "style": {"domain": "general_photo", "family": "quiet study"}, "user_exclusions": []}

    def test_prepatch_holdout_bytes_and_literal_projection(self):
        self.assertEqual(hashlib.sha256(HOLDOUT.read_bytes()).hexdigest(), HOLDOUT_SHA256)
        self.assertEqual({c["id"].split("_")[0] for c in self.cases}, {"en", "ko"})
        for case in self.cases:
            before = copy.deepcopy(case)
            for axis in camera.CAMERA_AXES:
                with self.subTest(case=case["id"], axis=axis):
                    clauses = camera.legacy_camera_clauses(case, axis)
                    self.assertEqual(clauses, case[axis])
                    self.assertTrue(all(clause in case["baseline_prompt_en"] for clause in clauses))
            self.assertEqual(case, before)

    def test_query_uses_only_the_owned_clause_and_keeps_frozen_core(self):
        for case in self.cases:
            core = self.query_core(case)
            before = copy.deepcopy(core)
            for axis in camera.CAMERA_AXES:
                slot = "camera_" + axis
                data = {"slots": {slot: []}, "candidate_semantic_policy": {"slot_dimensions": {slot: ["camera"]}}}
                queries, fields = pg.core_slot_focus_queries(data, core, slot)
                with self.subTest(case=case["id"], slot=slot):
                    if case[axis]:
                        self.assertEqual(queries, case[axis])
                        self.assertEqual(fields, ["baseline_prompt_en.camera_clause"])
                        self.assertNotIn(core["subject"], queries)
                    else:
                        self.assertNotIn("baseline_prompt_en.camera_clause", fields)
            self.assertEqual(core, before)

    def test_height_alone_cannot_establish_upward_direction(self):
        core = {"subject": "a wicker hamper", "baseline_prompt_en": "Place the camera below the hamper."}
        self.assertEqual(camera.legacy_camera_clauses(core, "height"), ["Place the camera below the hamper"])
        self.assertEqual(camera.legacy_camera_clauses(core, "direction"), [])

    def test_unrelated_background_clause_does_not_remove_an_owned_camera_clause(self):
        core = {"subject": "a hanging mobile", "baseline_prompt_en":
                "Position the camera below the mobile and tilt it upward. Use soft light and a simple background, letting the low camera position define the photograph."}
        self.assertEqual(camera.legacy_camera_clauses(core, "direction"),
                         ["Position the camera below the mobile and tilt it upward"])

    def test_passive_camera_action_is_literal_and_does_not_supply_height(self):
        core = {"subject": "a mossy stone", "baseline_prompt_en":
                "The camera is tilted downward toward the stone, while the flower faces upward."}
        self.assertEqual(camera.legacy_camera_clauses(core, "direction"),
                         ["The camera is tilted downward toward the stone"])
        self.assertEqual(camera.legacy_camera_clauses(core, "height"), [])

    def test_a_new_object_actor_cannot_supply_camera_direction(self):
        for text in (
            "The camera records the sculpture while its head points upward.",
            "The camera views a statue whose eyes look upward.",
            "The camera views the sculpture and the statue looks upward.",
            "The camera looks at a sculpture with its head pointing upward.",
        ):
            with self.subTest(text=text):
                self.assertEqual(camera.legacy_camera_clauses({"subject": "a sculpture", "baseline_prompt_en": text}, "direction"), [])

    def test_bare_coordinated_actors_are_not_part_of_a_camera_query(self):
        core = {"subject": "an ornament", "baseline_prompt_en":
                "Place the camera below the ornament and children look upward beside it."}
        self.assertEqual(camera.legacy_camera_clauses(core, "height"), ["Place the camera below the ornament"])
        self.assertEqual(camera.legacy_camera_clauses(core, "direction"), [])

    def test_coordinated_background_does_not_describe_the_camera(self):
        core = {"subject": "a lampshade", "baseline_prompt_en":
                "The camera looks upward toward the lampshade and the background stays plain."}
        self.assertEqual(camera.legacy_camera_clauses(core, "direction"),
                         ["The camera looks upward toward the lampshade"])

    def test_depicted_camera_subject_needs_explicit_owner_evidence(self):
        for subject in ("an old camera", "진열된 카메라"):
            core = {"subject": subject, "baseline_prompt_en": "The camera points upward toward a shelf."}
            self.assertEqual(camera.legacy_camera_clauses(core, "direction"), [])

    def test_unresolved_multiple_camera_ownership_fails_closed(self):
        for text in (
            "The camera looks upward. Another camera looks downward.",
            "The shooting camera looks upward while a backup camera faces left.",
            "Two cameras stand in the studio. The camera looks upward.",
        ):
            self.assertEqual(camera.legacy_camera_clauses({"subject": "a lamp", "baseline_prompt_en": text}, "direction"), [])

    def test_negation_and_quoted_descriptions_cannot_create_positive_queries(self):
        for text in (
            "Do not point the camera upward.",
            "The camera doesn't point upward.",
            "The camera points downward rather than upward.",
            "A sign reads 'The camera points upward'.",
            "The camera's reflection points upward.",
        ):
            self.assertEqual(camera.legacy_camera_clauses({"subject": "a vase", "baseline_prompt_en": text}, "direction"), [])

    def test_excluded_clause_is_not_reused_as_a_redacted_positive_fragment(self):
        core = self.query_core(self.cases[0])
        core["user_exclusions"] = ["upward"]
        data = {"slots": {"camera_direction": []}, "candidate_semantic_policy": {"slot_dimensions": {"camera_direction": ["camera"]}}}
        queries, fields = pg.core_slot_focus_queries(data, core, "camera_direction")
        self.assertNotIn("baseline_prompt_en.camera_clause", fields)
        self.assertNotIn("upward", " | ".join(queries))

    def test_explicit_owner_has_priority_over_a_legacy_baseline_clause(self):
        core = self.query_core(self.cases[0])
        core["intent_lock"]["semantic_anchors"] = [{"dimension": "camera", "target": "camera",
            "property": "viewpoint.direction", "prompt_evidence": "independently scoped camera evidence"}]
        data = {"slots": {"camera_direction": []}, "candidate_semantic_policy": {"slot_dimensions": {"camera_direction": ["camera"]}}}
        self.assertEqual(pg.core_slot_focus_queries(data, core, "camera_direction"),
                         (["independently scoped camera evidence"], ["intent_lock.semantic_anchors"]))


class NewCameraAuthoringChecks(unittest.TestCase):
    def inputs(self):
        request = "Photograph a woven basket. Position the camera below the basket and tilt it upward."
        evidence = "Position the camera below the basket and tilt it upward"
        raw = fixtures.core(request, subject="a woven basket", event="a woven basket rests on a table",
            visual_priorities=("visible woven reeds", "readable curved rim"),
            baseline_prompt_en="A woven basket rests on a table beside a plain linen cloth. " + evidence +
                ". Soft window light reveals the crossed reeds, the curved rim, and the small marks of use. The quiet surrounding room keeps the handmade structure distinct and its natural color plausible.")
        controls = pg.creative_controls.resolve(request, context={"subject_category": "nonhuman"}, seed=47)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        return raw, controls, evidence

    def add_anchor(self, raw, evidence, property_path):
        raw["intent_lock"]["semantic_anchors"].append({"anchor_id": property_path, "dimension": "camera",
            "target": "camera", "property": property_path, "source_text": raw["source_request"], "prompt_evidence": evidence})

    def test_declared_direction_and_height_require_separate_or_combined_typed_evidence(self):
        raw, _, evidence = self.inputs()
        for axis in camera.CAMERA_AXES:
            with self.assertRaisesRegex(ValueError, f"camera {axis} requires"):
                camera.require_camera_evidence(raw, [axis])
        self.add_anchor(raw, evidence, "viewpoint.height")
        camera.require_camera_evidence(raw, ["height"])
        with self.assertRaisesRegex(ValueError, "camera direction requires"):
            camera.require_camera_evidence(raw, ["direction"])
        self.add_anchor(raw, evidence, "viewpoint.direction")
        camera.require_camera_evidence(raw, ["direction", "height"])
        combined, _, evidence = self.inputs()
        self.add_anchor(combined, evidence, "viewpoint.height_and_direction")
        camera.require_camera_evidence(combined, ["direction", "height"])

    def test_focus_and_concept_evidence_do_not_satisfy_camera_requirements(self):
        raw, _, evidence = self.inputs()
        self.add_anchor(raw, evidence, "focus.depth")
        with self.assertRaisesRegex(ValueError, "camera direction requires"):
            camera.require_camera_evidence(raw, ["direction"])
        with self.assertRaisesRegex(ValueError, "direction or height"):
            camera.require_camera_evidence(raw, ["focus"])

    def test_whole_camera_lock_and_legacy_unchecked_input_keep_their_contract(self):
        raw, _, evidence = self.inputs()
        camera.require_camera_evidence(raw, [])
        raw["intent_lock"]["open_dimensions"].remove("camera")
        raw["intent_lock"]["locked_dimensions"].append("camera")
        raw["intent_lock"]["semantic_anchors"].append({"dimension": "camera", "prompt_evidence": evidence})
        camera.require_camera_evidence(raw, ["direction", "height"])

    def test_cli_rejects_missing_declared_camera_evidence_before_loading_candidate_data(self):
        raw, controls, _ = self.inputs()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            inputs = {"request-envelope": fixtures.envelope(raw["source_request"]), "authorial-core": raw,
                      "creative-controls": controls, "embodiment-review": fixtures.review(raw["baseline_prompt_en"])}
            args = []
            for name, payload in inputs.items():
                p = path / (name + ".json")
                p.write_text(json.dumps(payload))
                args.extend(["--" + name + "-json", str(p)])
            with mock.patch.object(cli.generator, "load_runtime_data") as load:
                with self.assertRaisesRegex(ValueError, "camera direction requires"):
                    cli.main(args + ["--require-camera-evidence", "direction"])
                load.assert_not_called()


class FrozenUpwardCameraRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_runtime_data()

    def test_both_frozen_arms_reach_upward_candidates_without_rewriting_the_core_or_unlocking_effects(self):
        archive = ROOT / "docs/research-evidence/photo-prompt/renewed-blind-scene-retrieval-20261003/diagnostic-evidence.tar.gz"
        correct = {"worms_eye", "extreme_low_angle_under_subject", "extreme_low_hero_angle"}
        with tarfile.open(archive) as tar:
            for arm in ("public-cli", "public-cli-property"):
                base = arm + "/inputs/blind_scene_006/"
                inputs = {name: json.load(tar.extractfile(base + name + ".json"))
                          for name in ("authorial-core", "request-envelope", "creative-controls", "embodiment-review")}
                core = pg.normalize_authorial_core(inputs["authorial-core"],
                    request_envelope=pg.normalize_request_envelope(inputs["request-envelope"]),
                    creative_control_snapshot=inputs["creative-controls"])
                before = copy.deepcopy(core)
                with mock.patch.object(pg, "cached_gemini_client", side_effect=AssertionError("offline test")):
                    pack = pg.generate_candidate_pack(self.data, core, inputs["creative-controls"], inputs["embodiment-review"], seed=829)
                rows = pack["slots"].get("camera_direction", {}).get("candidates", [])
                with self.subTest(arm=arm):
                    self.assertTrue(correct & {c["entry_id"] for c in rows})
                    self.assertEqual(core, before)
                    self.assertEqual(sum(len(s["candidates"]) for s in pack["slots"].values()), 64)
                    self.assertEqual(pack["authorial_composition"]["candidate_order"], "seed_shuffled_non_preferential")
                    self.assertEqual(pack["core_retrieval"]["candidate_adoption"], "optional")
                    if arm == "public-cli-property":
                        self.assertTrue(all(c["applicability"]["status"] == "ineligible" for c in rows))


if __name__ == "__main__":
    unittest.main()
