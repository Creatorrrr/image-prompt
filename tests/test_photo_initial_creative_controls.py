from __future__ import annotations

from tests import photo_prompt_fixtures as current_fixtures

import copy
import contextlib
import hashlib
import io
import json
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

from tests import test_photo_adult_appeal_scope as scope_fixtures
from tests import photo_prompt_fixtures as fixtures
from tests import test_photo_authorship_policy as composition_fixtures
import prompt_generator as generator
import audit_composed_prompt as auditor
import photo_creative_controls as controls
from photo_contracts import property_effects_allowed


class CreativeControlResolverTests(unittest.TestCase):
    def snapshot(self, **kwargs):
        return controls.resolve("An adult woman beside a window.", context={"subject_category": "human"}, seed=42, **kwargs)

    def test_defaults_meanings_and_sources_are_available_before_candidates(self):
        snapshot = self.snapshot()
        self.assertEqual([snapshot["controls"][a]["value"] for a in controls.AXES], [1, 0])
        self.assertIn("human attraction and desire", snapshot["definitions"]["controls"]["sensual"]["definition"])
        self.assertIn("clearly readable", snapshot["definitions"]["controls"]["sensual"]["levels"]["2"])
        self.assertEqual(snapshot["controls"]["sensual"]["source"], "saved_setting")
        self.assertEqual(snapshot["resolved_emphasis"], "sensual_led")
        self.assertEqual(snapshot["controls"]["surreal"], {"value": 0, "source": "saved_setting"})
        self.assertEqual(snapshot["controls"]["creativity"], {"value": 1, "source": "saved_setting"})
        self.assertEqual(snapshot["authoring_brief"], controls.authoring_brief(snapshot))

    def test_override_zero_is_an_addition_control_not_a_request_rewrite(self):
        request = "An adult woman wearing a sensual dress."
        snapshot = controls.resolve(request, context={"subject_category": "human"}, overrides={"sensual": 0, "fetish": 0}, seed=1)
        self.assertEqual(snapshot["source_request_sha256"], hashlib.sha256(request.encode()).hexdigest())
        self.assertEqual(snapshot["adult_appeal"]["sensual"]["effective_intensity"], 0)
        self.assertEqual(snapshot["controls"]["sensual"]["source"], "request_override")
        self.assertNotIn("negative", json.dumps(snapshot))

    def test_invalid_values_and_emphasis_fail(self):
        for overrides in ({"sensual": True}, {"sensual": 4}, {"creativity": float("nan")}, {"unknown": 1}, {"fetish": 0, "adult_appeal_emphasis": "fetish_led"}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                self.snapshot(overrides=overrides)

    def test_surreal_is_frozen_and_validation_uses_embedded_definitions(self):
        snapshot = self.snapshot(overrides={"surreal": 3})
        self.assertEqual(controls.runtime_values(snapshot)["surreal"], 3)
        with patch.object(controls._module, "load_definitions", side_effect=AssertionError("must not reload settings")):
            self.assertEqual(controls.validate(snapshot, "An adult woman beside a window."), snapshot)
        broken = copy.deepcopy(snapshot)
        broken["controls"]["surreal"]["value"] = 1
        with self.assertRaises(ValueError):
            controls.validate(broken, "An adult woman beside a window.")

    def test_surreal_levels_are_not_probabilistic_or_adult_eligibility_controls(self):
        for level in range(4):
            for seed in (0, 1, 42):
                with self.subTest(level=level, seed=seed):
                    snapshot = controls.resolve("A floating glass house without people.",
                        context={"subject_category": "nonhuman", "no_people": True, "explicit_nonsexual": True},
                        overrides={"surreal": level}, seed=seed)
                    self.assertEqual(controls.runtime_values(snapshot)["surreal"], level)
                    self.assertEqual(snapshot["adult_appeal"]["sensual"]["effective_intensity"], 0)
                    definition = snapshot["definitions"]["controls"]["surreal"]
                    self.assertIn(f"surreal: {level} (range: 0–3)", snapshot["authoring_brief"])
                    self.assertIn(definition["definition"], snapshot["authoring_brief"])
                    self.assertIn(definition["levels"][str(level)], snapshot["authoring_brief"])

    def test_surreal_rejects_removed_inputs_and_invalid_levels(self):
        for name, value in (("surreal_mode", "on"), ("surreal_probability", 1.0), ("surreal_intensity", "bold")):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "unsupported"):
                self.snapshot(overrides={name: value})
        for value in (-1, 4, True, 1.5, "auto"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.snapshot(overrides={"surreal": value})

    def test_creativity_levels_preserve_values_and_selected_meanings(self):
        for level in range(4):
            with self.subTest(level=level):
                snapshot = self.snapshot(overrides={"creativity": level})
                self.assertEqual(controls.runtime_values(snapshot)["creativity"], level)
                definition = snapshot["definitions"]["controls"]["creativity"]
                brief = snapshot["authoring_brief"]
                self.assertIn(f"creativity: {level} (range: 0–3)", brief)
                self.assertIn(definition["definition"], brief)
                self.assertIn(definition["levels"][str(level)], brief)
                self.assertEqual(snapshot["controls"]["viewer_experience"]["value"], False)
                self.assertEqual(snapshot["controls"]["reference_edit_mode"]["value"], "off")
                self.assertEqual(snapshot["controls"]["trend_layer"]["value"], "off")
        for value in (-1, 4, True, 0.5, 1.0, "3"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.snapshot(overrides={"creativity": value})

    def test_emphasis_stores_selected_and_effective_choices_without_changing_intensities(self):
        cases = [(3, 1, "auto", "sensual_led"), (1, 3, "auto", "fetish_led"),
                 (2, 2, "auto", "balanced"), (3, 1, "balanced", "balanced"),
                 (1, 3, "sensual_led", "sensual_led"), (3, 1, "fetish_led", "fetish_led"),
                 (0, 0, "auto", "balanced")]
        for sensual, fetish, selected, effective in cases:
            with self.subTest(sensual=sensual, fetish=fetish, selected=selected):
                snapshot = self.snapshot(overrides={"sensual": sensual, "fetish": fetish,
                                                   "adult_appeal_emphasis": selected})
                runtime = controls.runtime_values(snapshot)
                self.assertEqual((runtime["sensual_intensity"], runtime["fetish_intensity"]), (sensual, fetish))
                self.assertEqual(snapshot["controls"]["adult_appeal_emphasis"]["value"], selected)
                self.assertEqual(runtime["adult_appeal_emphasis"], effective)
                self.assertEqual(snapshot["emphasis_resolution"]["active"], bool(sensual or fetish))
                brief = snapshot["authoring_brief"]
                definition = snapshot["definitions"]["controls"]["adult_appeal_emphasis"]
                self.assertIn(definition["definition"], brief)
                self.assertIn(definition["choice_descriptions"][selected], brief)
                self.assertIn(snapshot["emphasis_resolution"]["reason"], brief)
                self.assertIn("Effective: " + (effective if sensual or fetish else "inactive"), brief)
                if sensual or fetish:
                    self.assertIn(definition["choice_descriptions"][effective], brief)
                controls.validate(snapshot, "An adult woman beside a window.")

    def test_level_and_choice_definitions_must_be_complete(self):
        for name, field, key in (("creativity", "levels", "2"),
                                 ("adult_appeal_emphasis", "choice_descriptions", "auto")):
            definitions = controls.load_definitions()
            del definitions["controls"][name][field][key]
            with self.subTest(name=name), self.assertRaises(ValueError):
                controls.resolve("A portrait.", definitions=definitions)

    def test_saved_brief_cannot_be_changed_even_with_a_recomputed_hash(self):
        snapshot = self.snapshot(overrides={"surreal": 2})
        snapshot["authoring_brief"] = "surreal: 0"
        snapshot.pop("canonical_sha256")
        snapshot["canonical_sha256"] = controls.digest(snapshot)
        with self.assertRaisesRegex(ValueError, "stale, malformed"):
            controls.validate(snapshot, "An adult woman beside a window.")

    def test_emphasis_resolution_is_hash_bound_and_recomputed(self):
        snapshot = self.snapshot(overrides={"sensual": 3, "fetish": 1})
        snapshot["emphasis_resolution"]["active"] = False
        snapshot.pop("canonical_sha256")
        snapshot["canonical_sha256"] = controls.digest(snapshot)
        with self.assertRaisesRegex(ValueError, "stale, malformed"):
            controls.validate(snapshot, "An adult woman beside a window.")

    def test_cli_rejects_fractional_creativity_before_loading_candidates(self):
        for value in ("0.5", "1.0", "-1", "4"):
            with self.subTest(value=value), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as exc:
                generator.main(["--creativity", value])
            self.assertEqual(exc.exception.code, 2)

    def test_resolver_cli_saves_the_same_complete_brief_it_returns(self):
        request = "A glass house above a lake. surreal=2"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, value in {"request": fixtures.envelope(request),
                                "context": {"subject_category": "nonhuman"},
                                "overrides": {"surreal": 2}}.items():
                (root / f"{name}.json").write_text(json.dumps(value))
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                controls._module.main(["--request-envelope-json", str(root / "request.json"),
                    "--context-json", str(root / "context.json"), "--overrides-json", str(root / "overrides.json"),
                    "--output", str(root / "controls.json"), "--seed", "7"])
            saved = json.loads((root / "controls.json").read_text())
            self.assertEqual(saved["authoring_brief"], json.loads(output.getvalue())["authoring_brief"])
            controls.validate(saved, request)
            for name in controls.LEVEL_CONTROLS:
                definition = saved["definitions"]["controls"][name]
                self.assertIn(definition["definition"], saved["authoring_brief"])
            self.assertIn("surreal: 2 (range: 0–3)", saved["authoring_brief"])

    def test_no_people_and_nonsexual_meaning_keep_requested_values_but_disable_additions(self):
        for context in ({"subject_category": "human", "no_people": True}, {"subject_category": "human", "explicit_nonsexual": True}, {"subject_category": "nonhuman"}):
            snapshot = controls.resolve("A precisely specified scene.", context=context, seed=1)
            self.assertEqual(snapshot["adult_appeal"]["sensual"]["requested_intensity"], 1)
            self.assertEqual(snapshot["adult_appeal"]["sensual"]["effective_intensity"], 0)

    def test_cli_rejects_post_core_control_change_before_loading_candidates(self):
        request = "An adult woman beside a window."
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "controls.json").write_text(json.dumps(self.snapshot()))
            (root / "request.json").write_text(json.dumps({"request_text": request}))
            for flag, value in (("--sensual-intensity", "3"), ("--surreal", "3"),
                                ("--creativity", "3"), ("--adult-appeal-emphasis", "sensual_led")):
                with self.subTest(flag=flag), self.assertRaisesRegex(ValueError, "conflicts with the frozen"):
                    generator.main(["--emit-candidate-pack", "--candidate-pack-version", "v6", "--request-envelope-json", str(root / "request.json"), "--creative-controls-json", str(root / "controls.json"), flag, value])


class InitialDirectionIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scope_fixtures.PhotoAdultAppealScopeTests.setUpClass()
        cls.fixture = scope_fixtures.PhotoAdultAppealScopeTests
        cls.data = cls.fixture.data
        source = cls.fixture.core["source_request"] + " She wears a torn white dress."
        cls.envelope = generator.normalize_request_envelope(fixtures.envelope(source))
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
        cls.snapshot = controls.resolve(source, context={"subject_category": "human"}, overrides={"sensual": 2, "fetish": 1}, seed=73)
        cls.raw["creative_controls_sha256"] = cls.snapshot["canonical_sha256"]
        cls.core = generator.normalize_authorial_core(cls.raw, request_envelope=cls.envelope)
        cls.result = current_fixtures.generate_once(cls.data, random.Random(73), None, ["en"], True, 12, True,
            selection_mode="rule", include_trace=True, concept_locks=[source], seed=73,
            authorial_core=cls.core, creative_control_snapshot=cls.snapshot)
        cls.pack = generator.build_candidate_pack(cls.result, cls.data, "v6")

    def composed(self):
        composed = composition_fixtures.PhotoAuthorshipPolicyTests.composed(self.pack)
        composed["adult_appeal_brief"] = {
            "adult_subject_phrase": "An adult woman", "agency_phrase": "stands confidently",
            "axes": {
                "sensual": {"intensity": 2, "realization": "baseline", "affected_dimensions": [], "artistic_interpretation": "Retain the coherent initial wardrobe and portrait direction", "prompt_evidence": "a softly draped neckline"},
                "fetish": {"intensity": 1, "realization": "baseline", "affected_dimensions": [], "artistic_interpretation": "Retain the existing material direction for separate visual assessment", "prompt_evidence": "textured clothing"},
            },
            "blend": {"emphasis": "sensual_led"},
            "contextual_review": [
                {"candidate_id": cid, "reading": "irrelevant", "reason": "This optional change does not improve the window portrait's preserved moment."}
                for cid in self.pack["adult_appeal"]["contextual_retrieval"]["review_candidate_ids"]
            ],
            "contextual_comparison": "Retain the baseline at 2/1: alternative presentation and construction would compete with the existing neckline and window gesture.",
        }
        return composed

    def test_frozen_controls_survive_generator_and_public_composer_pack(self):
        self.assertEqual(self.pack["creative_controls"], self.snapshot)
        self.assertEqual(auditor.audit_creative_controls(self.pack), [])
        self.assertEqual(self.pack["provenance"]["creativity"], 1)
        self.assertEqual(self.pack["provenance"]["candidate_pool_creativity"], 3)

    def test_surreal_level_and_saved_brief_survive_sampler_and_public_pack(self):
        for level in range(4):
            with self.subTest(level=level):
                raw = copy.deepcopy(self.raw)
                snapshot = controls.resolve(raw["source_request"], context={"subject_category": "human"},
                    overrides={"surreal": level, "sensual": 2, "fetish": 1}, seed=73)
                raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
                core = generator.normalize_authorial_core(raw, request_envelope=self.envelope,
                                                          creative_control_snapshot=snapshot)
                with patch.object(generator, "apply_surreal_layer", wraps=generator.apply_surreal_layer) as apply:
                    result = current_fixtures.generate_once(self.data, random.Random(73), None, ["en"], True, 12, True,
                        selection_mode="rule", include_trace=True, seed=73,
                        authorial_core=core, creative_control_snapshot=snapshot)
                self.assertEqual(apply.call_count, int(level > 0))
                if level:
                    self.assertEqual(apply.call_args.args[5], level)
                pack = generator.build_candidate_pack(result, self.data, "v6")
                self.assertEqual(pack["creative_controls"], snapshot)
                self.assertEqual(pack["provenance"]["creative_control_runtime"]["surreal"], level)
                self.assertEqual(pack["authorial_core"]["baseline_prompt_en"], raw["baseline_prompt_en"])
                self.assertEqual(auditor.audit_creative_controls(pack), [])

    def test_creativity_and_emphasis_reach_public_pack_with_their_initial_brief(self):
        cases = [(0, "auto", ["near"]), (1, "fetish_led", ["near"]),
                 (2, "balanced", ["near", "adjacent"]),
                 (3, "sensual_led", ["near", "adjacent", "lateral"])]
        for level, emphasis, bands in cases:
            with self.subTest(level=level, emphasis=emphasis):
                raw = copy.deepcopy(self.raw)
                snapshot = controls.resolve(raw["source_request"], context={"subject_category": "human"},
                    overrides={"creativity": level, "adult_appeal_emphasis": emphasis, "sensual": 2, "fetish": 1}, seed=73)
                raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
                core = generator.normalize_authorial_core(raw, request_envelope=self.envelope,
                                                          creative_control_snapshot=snapshot)
                result = current_fixtures.generate_once(self.data, random.Random(73), None, ["en"], True, 12, True,
                    selection_mode="rule", include_trace=True, seed=73,
                    authorial_core=core, creative_control_snapshot=snapshot)
                pack = generator.build_candidate_pack(result, self.data, "v6")
                self.assertEqual(pack["creative_controls"], snapshot)
                self.assertEqual(pack["provenance"]["creative_control_runtime"], controls.runtime_values(snapshot))
                self.assertEqual(pack["provenance"]["creativity"], level)
                self.assertEqual(pack["creative_augmentation"]["requested_creativity"], level)
                self.assertEqual(pack["creative_augmentation"]["distance_policy"]["allowed_bands"], bands)
                self.assertEqual(bool(pack.get("creative_direction")), level == 3)
                self.assertEqual(pack["authorial_core"]["baseline_prompt_en"], raw["baseline_prompt_en"])
                self.assertEqual(auditor.audit_creative_controls(pack), [])

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
        self.assertTrue(auditor.authorial_core_intent_contract_valid(self.core, minimum_open_dimensions=0))

    def test_sensual_wardrobe_candidates_exist_when_garment_is_open(self):
        adult = self.fixture.pack["adult_appeal"]
        self.assertIn("appearance", adult["dimension_scope"]["axis_allowed_dimensions"]["sensual"])
        self.assertTrue(any("appearance" in c["affected_dimensions"] for c in adult["axes"]["sensual"]["candidate_inventory"]))
        self.assertNotIn("configured_low_intensity_default", adult["composition_requirements"])

    def test_whole_garment_candidates_do_not_bypass_partial_property_locks(self):
        for axis in self.pack["adult_appeal"]["axes"].values():
            for candidate in axis["candidate_inventory"]:
                self.assertTrue(property_effects_allowed(self.core["intent_lock"], candidate["affected_dimensions"], candidate.get("affected_properties", [])))

    def test_baseline_realization_needs_no_extra_axis_detail(self):
        composed = self.composed()
        failures, _ = auditor.audit_adult_appeal(self.pack, composed, composed["prompt_en"], set(), {})
        self.assertEqual(failures, [])
        report = auditor.audit_composed_prompt(self.pack, composed)
        self.assertEqual(report["status"], "pass", report["failures"])

    def test_authored_refinement_must_declare_unlocked_property_effects(self):
        composed = self.composed()
        evidence = "The existing neckline drapes softly toward her relaxed shoulder"
        composed["prompt_en"] += " " + evidence + "."
        axis = composed["adult_appeal_brief"]["axes"]["sensual"]
        axis.update(realization="refined", affected_dimensions=["appearance"], prompt_evidence=evidence)
        failures, _ = auditor.audit_adult_appeal(self.pack, composed, composed["prompt_en"], set(), {})
        self.assertIn("adult_appeal_authored_properties", {f["check"] for f in failures})
        axis["affected_properties"] = [{"dimension": "appearance", "target": "main_subject", "property": "wardrobe.neckline"}]
        failures, _ = auditor.audit_adult_appeal(self.pack, composed, composed["prompt_en"], set(), {})
        self.assertEqual(failures, [])
        axis["affected_properties"][0]["property"] = "wardrobe.color"
        failures, _ = auditor.audit_adult_appeal(self.pack, composed, composed["prompt_en"], set(), {})
        self.assertIn("adult_appeal_authored_properties", {f["check"] for f in failures})

    def test_changed_snapshot_or_missing_binding_fails(self):
        pack = copy.deepcopy(self.pack)
        pack["creative_controls"]["controls"]["sensual"]["value"] = 3
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

    def test_historical_axis_scope_is_rejected(self):
        adult = copy.deepcopy(self.pack["adult_appeal"])
        adult["dimension_scope"]["contract_version"] = "photo-adult-appeal-dimension-scope/v1"
        self.assertTrue(auditor.audit_adult_appeal_dimension_scope(self.pack, adult))


if __name__ == "__main__":
    unittest.main()
