from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

from tests import test_photo_adult_appeal_scope as scope_fixtures
from tests import test_photo_authorial_core_v5 as v5_fixtures
from tests import test_photo_authorship_policy as composition_fixtures
import prompt_generator as generator
import audit_composed_prompt as auditor
import photo_creative_controls as controls
from photo_contracts import (LEGACY_ADULT_APPEAL_AXIS_DIMENSIONS,
                             LEGACY_ADULT_APPEAL_DIMENSION_SCOPE_CONTRACT_VERSION,
                             property_effects_allowed)


class CreativeControlResolverTests(unittest.TestCase):
    def snapshot(self, **kwargs):
        return controls.resolve("An adult woman beside a window.", context={"subject_category": "human"}, seed=42, **kwargs)

    def test_defaults_meanings_and_sources_are_available_before_candidates(self):
        snapshot = self.snapshot()
        self.assertEqual([snapshot["controls"][a]["value"] for a in controls.AXES], [2, 1])
        self.assertIn("wardrobe", snapshot["definitions"]["controls"]["sensual_editorial"]["definition"])
        self.assertIn("clearly readable", snapshot["definitions"]["controls"]["sensual_editorial"]["levels"]["2"])
        self.assertEqual(snapshot["controls"]["sensual_editorial"]["source"], "saved_setting")
        self.assertEqual(snapshot["resolved_emphasis"], "sensual_led")

    def test_override_zero_is_an_addition_control_not_a_request_rewrite(self):
        request = "An adult woman wearing a sensual dress."
        snapshot = controls.resolve(request, context={"subject_category": "human"}, overrides={"sensual_editorial": 0, "fetish_fashion": 0}, seed=1)
        self.assertEqual(snapshot["source_request_sha256"], hashlib.sha256(request.encode()).hexdigest())
        self.assertEqual(snapshot["adult_appeal"]["sensual_editorial"]["effective_intensity"], 0)
        self.assertEqual(snapshot["controls"]["sensual_editorial"]["source"], "request_override")
        self.assertNotIn("negative", json.dumps(snapshot))

    def test_invalid_values_and_emphasis_fail(self):
        for overrides in ({"sensual_editorial": True}, {"sensual_editorial": 4}, {"creativity": float("nan")}, {"unknown": 1}, {"fetish_fashion": 0, "adult_appeal_emphasis": "fetish_led"}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                self.snapshot(overrides=overrides)

    def test_auto_is_frozen_once_and_replay_uses_embedded_definitions(self):
        snapshot = self.snapshot(overrides={"surreal_mode": "auto", "surreal_probability": 1.0})
        self.assertTrue(snapshot["surreal_active"])
        self.assertEqual(controls.runtime_values(snapshot)["surreal_mode"], "on")
        with patch.object(controls._module, "load_definitions", side_effect=AssertionError("must not reload settings")):
            self.assertEqual(controls.validate(snapshot, "An adult woman beside a window."), snapshot)
        broken = copy.deepcopy(snapshot)
        broken["surreal_active"] = False
        with self.assertRaises(ValueError):
            controls.validate(broken, "An adult woman beside a window.")

    def test_no_people_and_nonsexual_meaning_keep_requested_values_but_disable_additions(self):
        for context in ({"subject_category": "human", "no_people": True}, {"subject_category": "human", "explicit_nonsexual": True}, {"subject_category": "nonhuman"}):
            snapshot = controls.resolve("A precisely specified scene.", context=context, seed=1)
            self.assertEqual(snapshot["adult_appeal"]["sensual_editorial"]["requested_intensity"], 2)
            self.assertEqual(snapshot["adult_appeal"]["sensual_editorial"]["effective_intensity"], 0)

    def test_cli_rejects_post_core_control_change_before_loading_candidates(self):
        request = "An adult woman beside a window."
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "controls.json").write_text(json.dumps(self.snapshot()))
            (root / "request.json").write_text(json.dumps({"request_text": request}))
            with self.assertRaisesRegex(ValueError, "conflicts with the frozen"):
                generator.main(["--emit-candidate-pack", "--candidate-pack-version", "v6", "--request-envelope-json", str(root / "request.json"), "--creative-controls-json", str(root / "controls.json"), "--sensual-editorial-intensity", "3"])


class InitialDirectionIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scope_fixtures.PhotoAdultAppealScopeTests.setUpClass()
        cls.fixture = scope_fixtures.PhotoAdultAppealScopeTests
        cls.data = cls.fixture.data
        source = cls.fixture.core["source_request"] + " She wears a torn white dress."
        cls.envelope = generator.normalize_request_envelope(v5_fixtures.PhotoAuthorialCoreV5Tests.envelope(source))
        cls.raw = {k: copy.deepcopy(v) for k, v in cls.fixture.core.items() if k not in {"request_binding", "canonical_sha256", "core_id"}}
        cls.raw["source_request"] = source
        cls.raw["baseline_prompt_en"] += " She wears a torn white dress with a softly draped neckline."
        cls.raw["intent_lock"] = {k: copy.deepcopy(v) for k, v in cls.raw["intent_lock"].items() if k in {"contract_version", "priority", "semantic_anchors", "locked_dimensions", "open_dimensions"}}
        cls.raw["intent_lock"]["contract_version"] = "photo-intent-lock/v2"
        cls.raw["intent_lock"]["open_dimensions"] += ["appearance", "material"]
        cls.raw["intent_lock"]["semantic_anchors"].extend([
            {"anchor_id": "dress_kind", "dimension": "appearance", "target": "main_subject", "property": "wardrobe.garment_type", "source_text": "torn white dress", "prompt_evidence": "torn white dress"},
            {"anchor_id": "dress_color", "dimension": "appearance", "target": "main_subject", "property": "wardrobe.color", "source_text": "white dress", "prompt_evidence": "white dress"},
        ])
        cls.snapshot = controls.resolve(source, context={"subject_category": "human"}, seed=73)
        cls.raw["creative_controls_sha256"] = cls.snapshot["canonical_sha256"]
        cls.core = generator.normalize_authorial_core(cls.raw, request_envelope=cls.envelope)
        cls.result = generator.generate_once(cls.data, random.Random(73), None, ["en"], True, 12, True,
            selection_mode="rule", include_trace=True, concept_locks=[source], seed=73,
            authorial_core=cls.core, creative_control_snapshot=cls.snapshot)
        cls.pack = generator.build_candidate_pack(cls.result, cls.data, "v6")

    def composed(self):
        composed = composition_fixtures.PhotoAuthorshipPolicyTests.composed(self.pack)
        composed["adult_appeal_brief"] = {
            "adult_subject_phrase": "An adult woman", "agency_phrase": "stands confidently",
            "axes": {
                "sensual_editorial": {"intensity": 2, "realization": "baseline", "affected_dimensions": [], "artistic_interpretation": "Retain the coherent initial wardrobe and portrait direction", "prompt_evidence": "a softly draped neckline"},
                "fetish_fashion": {"intensity": 1, "realization": "baseline", "affected_dimensions": [], "artistic_interpretation": "Retain the existing material direction for separate visual assessment", "prompt_evidence": "textured clothing"},
            },
            "blend": {"emphasis": "sensual_led"},
        }
        return composed

    def test_frozen_controls_survive_generator_and_public_composer_pack(self):
        self.assertEqual(self.pack["creative_controls"], self.snapshot)
        self.assertEqual(auditor.audit_creative_controls(self.pack), [])
        self.assertEqual(self.pack["provenance"]["creativity"], 0.5)
        self.assertEqual(self.pack["provenance"]["candidate_pool_creativity"], 1.0)

    def test_property_lock_preserves_color_and_type_but_allows_neckline(self):
        lock = self.core["intent_lock"]
        effect = [{"dimension": "appearance", "target": "main_subject", "property": "wardrobe.neckline"}]
        self.assertTrue(property_effects_allowed(lock, ["appearance"], effect))
        for path in ("wardrobe.color", "wardrobe.garment_type", "wardrobe", "*"):
            effect[0]["property"] = path
            self.assertFalse(property_effects_allowed(lock, ["appearance"], effect))
        self.assertFalse(property_effects_allowed(lock, ["appearance"], []))
        self.assertFalse(property_effects_allowed(lock, ["material"], [
            {"dimension": "material", "target": "main_subject", "property": "wardrobe.color"}
        ]))
        self.assertTrue(property_effects_allowed(lock, ["material"], [
            {"dimension": "material", "target": "main_subject", "property": "wardrobe.texture"}
        ]))
        self.assertTrue(auditor.authorial_core_v2_intent_contract_valid(self.core, minimum_open_dimensions=0))

    def test_sensual_wardrobe_candidates_exist_when_garment_is_open(self):
        adult = self.fixture.pack["adult_appeal"]
        self.assertIn("appearance", adult["dimension_scope"]["axis_allowed_dimensions"]["sensual_editorial"])
        self.assertTrue(any(c["carrier"] == "wardrobe_material" for c in adult["axes"]["sensual_editorial"]["candidate_inventory"]))
        self.assertNotIn("configured_low_intensity_default", adult["composition_requirements"])

    def test_whole_garment_candidates_do_not_bypass_partial_property_locks(self):
        for axis in self.pack["adult_appeal"]["axes"].values():
            for candidate in axis["candidate_inventory"]:
                self.assertNotIn("appearance", candidate["affected_dimensions"])

    def test_baseline_realization_needs_no_extra_axis_detail(self):
        composed = self.composed()
        failures, _ = auditor.audit_adult_appeal_v5(self.pack, composed, composed["prompt_en"], set(), {})
        self.assertEqual(failures, [])
        report = auditor.audit_composed_prompt(self.pack, composed)
        self.assertEqual(report["status"], "pass", report["failures"])

    def test_authored_refinement_must_declare_unlocked_property_effects(self):
        composed = self.composed()
        evidence = "The existing neckline drapes softly toward her relaxed shoulder"
        composed["prompt_en"] += " " + evidence + "."
        axis = composed["adult_appeal_brief"]["axes"]["sensual_editorial"]
        axis.update(realization="refined", affected_dimensions=["appearance"], prompt_evidence=evidence)
        failures, _ = auditor.audit_adult_appeal_v5(self.pack, composed, composed["prompt_en"], set(), {})
        self.assertIn("adult_appeal_authored_properties", {f["check"] for f in failures})
        axis["affected_properties"] = [{"dimension": "appearance", "target": "main_subject", "property": "wardrobe.neckline"}]
        failures, _ = auditor.audit_adult_appeal_v5(self.pack, composed, composed["prompt_en"], set(), {})
        self.assertEqual(failures, [])
        axis["affected_properties"][0]["property"] = "wardrobe.color"
        failures, _ = auditor.audit_adult_appeal_v5(self.pack, composed, composed["prompt_en"], set(), {})
        self.assertIn("adult_appeal_authored_properties", {f["check"] for f in failures})

    def test_changed_snapshot_or_missing_binding_fails(self):
        pack = copy.deepcopy(self.pack)
        pack["creative_controls"]["controls"]["sensual_editorial"]["value"] = 3
        self.assertTrue(auditor.audit_creative_controls(pack))
        pack = copy.deepcopy(self.pack)
        pack.pop("creative_controls")
        self.assertTrue(auditor.audit_creative_controls(pack))

    def test_ordinary_candidate_cannot_bypass_the_same_property_boundary(self):
        candidate = {"id": "slot:garment_detail:test", "slot": "garment_detail", "affected_dimensions": ["appearance"]}
        evidence = "A softly gathered neckline follows the existing white fabric"
        row = {"candidate_id": candidate["id"], "artistic_interpretation": "Connect the garment to her composed presence", "transformation": "Preserve the original garment and refine the neckline", "prompt_evidence": evidence}
        composed = {"candidate_interpretations": [row]}
        def checks():
            return {f["check"] for f in auditor.audit_candidate_interpretations(self.pack, composed, evidence, {candidate["id"]}, {candidate["id"]: candidate})}
        self.assertIn("candidate_interpretation_properties", checks())
        properties = [{"dimension": "appearance", "target": "main_subject", "property": "wardrobe.neckline"}]
        candidate["affected_properties"] = properties
        row["affected_properties"] = properties
        self.assertNotIn("candidate_interpretation_properties", checks())

    def test_historical_scope_keeps_original_sensual_dimensions(self):
        pack = copy.deepcopy(self.fixture.pack)
        adult = pack["adult_appeal"]
        scope = adult["dimension_scope"]
        scope["contract_version"] = LEGACY_ADULT_APPEAL_DIMENSION_SCOPE_CONTRACT_VERSION
        scope.pop("protected_properties")
        locked = set(scope["locked_dimensions"])
        scope["axis_allowed_dimensions"] = {axis: sorted(dimensions - locked) for axis, dimensions in LEGACY_ADULT_APPEAL_AXIS_DIMENSIONS.items()}
        for axis, value in adult["axes"].items():
            value["candidate_inventory"] = [row for row in value["candidate_inventory"] if set(row["affected_dimensions"]).issubset(scope["axis_allowed_dimensions"][axis])]
        self.assertEqual(auditor.audit_adult_appeal_dimension_scope(pack, adult), [])
        self.assertNotIn("appearance", scope["axis_allowed_dimensions"]["sensual_editorial"])


if __name__ == "__main__":
    unittest.main()
