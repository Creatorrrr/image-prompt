"""Bound no-people context at optional bundle and adult-inventory boundaries.

The bundle regression uses the shipped catalog. The adult guard fixture uses a
small, explicitly synthetic catalog; valid no-people snapshots already disable
adult axes, so forwarding/validation coverage must not be described as a
reachable active-inventory leak.
"""
from __future__ import annotations

import copy
from pathlib import Path
import unittest
from unittest.mock import patch

from tests import photo_prompt_fixtures as fixtures

import audit_composed_prompt as auditor
import photo_candidate_semantics as semantics
import photo_contextual_appeal as contextual
import prompt_generator as generator


ASSETS = Path(__file__).resolve().parents[1] / "skills/photo-prompt-image-generator/assets"
BUNDLE_ID = "bundle:ed_clean_room_reset"
MEMBER_ID = "ed_clean_room_reset_candidate"


def bound_inputs(no_people: bool):
    """Resolve and validate real v3 inputs with no legacy-parser/exclusion gate."""
    request = (
        "Photograph a bronze statue in a quiet gallery where one work area is now clear, "
        "with no living people."
    )
    snapshot = generator.creative_controls.resolve(
        request,
        context={"subject_category": "nonhuman", "no_people": no_people},
        overrides={"sensual": 1, "fetish": 1},
        seed=7,
    )
    raw = fixtures.core(
        request,
        subject="a weathered bronze statue",
        setting="a quiet spacious museum gallery",
        event="the sculpture stands on a plinth",
        interpreted_intent="A factual photographic study of a bronze sculpture beside a cleared work area",
        visual_priorities=("weathered bronze patina", "stone gallery plinth", "one work area is now clear"),
        baseline_prompt_en=(
            "A weathered bronze statue stands on a plinth in a quiet gallery. The bronze sculpture "
            "has a textured patina, lit by soft overhead illumination. In the gallery, one work "
            "area is now clear, and the camera keeps the complete sculpture and its stone support "
            "clearly readable."
        ),
        anchor_evidence=("bronze sculpture", "A weathered bronze statue", "stands on a plinth"),
        open_dimensions=("framing", "composition", "lighting", "camera", "color", "material",
                         "atmosphere", "relationship", "setting"),
    )
    raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
    core = generator.normalize_authorial_core(
        raw,
        request_envelope=generator.normalize_request_envelope(fixtures.envelope(request)),
        creative_control_snapshot=snapshot,
    )
    pack = {
        "contract_version": "photo-candidate-pack/v6",
        "candidate_semantic_surface_version": semantics.SURFACE_VERSION,
        "authorial_core": core,
        "creative_controls": snapshot,
        # No individually exposed members: only the real joint-admission path
        # can expose a bundle, so the counterexample is not a fallback artifact.
        "slots": {},
        "provenance": {"seed": 7},
    }
    result = {"provenance": {"prompt_id": "bound-context-test", "creative_controls": snapshot}}
    return core, snapshot, pack, result


class BoundContextSurfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = generator.load_json(ASSETS / "photo_prompt_tags.json")
        cls.data[generator.QUALITY_LAYERS_DATA_KEY] = generator.load_quality_layers(
            ASSETS / "photo_prompt_quality_layers.json"
        )

    def bundles(self, pack):
        return generator.candidate_pack_candidate_bundles(self.data, pack)

    def semantic_audit(self, pack):
        # This is the real semantic-contract auditor, including its own reload
        # of the shipped dictionary and real generator-helper recomputation.
        return auditor.audit_candidate_semantic_contracts(
            pack, "", set(), auditor.candidate_objects_from_pack(pack), []
        )

    def invalid_snapshots(self, core, snapshot):
        malformed = copy.deepcopy(snapshot)
        malformed["context"]["no_people"] = not snapshot["context"]["no_people"]
        stale = generator.creative_controls.resolve(
            core["source_request"], context=snapshot["context"],
            overrides=snapshot["overrides"], seed=8,
        )
        wrong_request = generator.creative_controls.resolve(
            "Photograph an entirely different gallery.", context=snapshot["context"],
            overrides=snapshot["overrides"], seed=7,
        )
        return {"malformed": malformed, "stale_core_binding": stale, "wrong_request": wrong_request}

    def synthetic_adult_data(self):
        # Explicit synthetic catalog isolates forwarding from catalog ranking,
        # while retaining the real policy, resolver, scope and retrieval code.
        rows = [
            {"id": "synthetic_human_light", "en": "soft overhead illumination on bronze patina",
             "concept_units": ["soft overhead illumination on bronze patina"],
             "tags": ["human"], "affected_dimensions": ["lighting"], "weight": 1},
            {"id": "synthetic_neutral_light", "en": "soft overhead illumination on stone plinth",
             "concept_units": ["soft overhead illumination on stone plinth"],
             "tags": [], "affected_dimensions": ["lighting"], "weight": 1},
        ]
        return {
            "slots": {"lighting": rows}, "presets": [],
            "candidate_semantic_policy": copy.deepcopy(self.data["candidate_semantic_policy"]),
            generator.QUALITY_LAYERS_DATA_KEY: copy.deepcopy(self.data[generator.QUALITY_LAYERS_DATA_KEY]),
        }

    def test_real_catalog_human_bundle_is_eligible_false_control_but_blocked_by_bound_true(self):
        entry = generator.candidate_pack_slot_entry_by_id(self.data, "space_condition", MEMBER_ID)
        self.assertIn("human", generator.entry_kinds(entry) | generator.entry_tags(entry))
        for no_people in (False, True):
            with self.subTest(no_people=no_people):
                core, snapshot, pack, _ = bound_inputs(no_people)
                before = copy.deepcopy(pack)
                self.assertFalse(core["user_exclusions"])
                self.assertFalse(generator.intent_explicitly_excludes_people(core["source_request"]))
                self.assertFalse(generator.authorial_core_generation_constraints(core)["no_people"])
                constraints = generator.authorial_core_generation_constraints(
                    core, creative_control_snapshot=snapshot
                )
                self.assertEqual(constraints["no_people"], no_people)
                contract = {"subject_category": "generic", "preset_domains": [],
                            "adult_allowed": False, "intent_constraints": constraints}
                self.assertEqual(generator.entry_block_reason(entry, "space_condition", contract),
                                 "explicit_no_people" if no_people else None)
                bundles = self.bundles(pack)["candidates"]
                ids = {row["id"] for row in bundles}
                if no_people:
                    self.assertNotIn(BUNDLE_ID, ids)
                else:
                    self.assertIn(BUNDLE_ID, ids, "the human-tagged bundle must actually be eligible")
                    exposed = next(row for row in bundles if row["id"] == BUNDLE_ID)
                    self.assertTrue(exposed["joint_admission"]["all_member_guards_satisfied"])
                    self.assertEqual(exposed["applicability"]["source"], "source_recomputed_joint_adoption")
                self.assertEqual(pack, before)

    def test_synthetic_neutral_bundle_is_preserved_while_human_peer_is_blocked(self):
        # A bounded synthetic counterexample prevents the fix from passing by
        # blanket-removing every optional bundle in a no-people scene.
        data = self.synthetic_adult_data()
        for entry in data["slots"]["lighting"]:
            entry["concept_units"] = ["weathered bronze patina", "soft overhead illumination"]
            semantics.compile_extension_bundles(data, {"visual_semantics": [{
                "id": entry["id"], "candidate_ids": [entry["id"]],
                "component_groups": ["weathered bronze patina"],
            }]})
        for no_people in (False, True):
            with self.subTest(no_people=no_people):
                _, _, pack, _ = bound_inputs(no_people)
                exposed = generator.candidate_pack_candidate_bundles(data, pack)
                ids = {row["id"] for row in exposed["candidates"]}
                self.assertIn("bundle:synthetic_neutral_light", ids)
                self.assertEqual("bundle:synthetic_human_light" in ids, not no_people)

    def test_real_auditor_recomputes_both_bound_bundle_surfaces_without_an_auditor_patch(self):
        self.assertIs(auditor.candidate_semantics_generator.candidate_pack_candidate_bundles,
                      generator.candidate_pack_candidate_bundles)
        for no_people in (False, True):
            with self.subTest(no_people=no_people):
                _, _, pack, _ = bound_inputs(no_people)
                pack["candidate_bundles"] = self.bundles(pack)
                ids = {row["id"] for row in pack["candidate_bundles"]["candidates"]}
                self.assertEqual(BUNDLE_ID in ids, not no_people)
                self.assertEqual(self.semantic_audit(pack), [])

    def test_auditor_rejects_rebound_human_bundle_in_bound_no_people_pack(self):
        _, _, control_pack, _ = bound_inputs(False)
        forged = self.bundles(control_pack)
        self.assertIn(BUNDLE_ID, {row["id"] for row in forged["candidates"]})
        core, _, pack, _ = bound_inputs(True)
        # Re-signing the declared core hashes is not authority to admit a member.
        for row in forged["candidates"]:
            row["joint_admission"]["source_authorial_core_sha256"] = core["canonical_sha256"]
            row["joint_admission"]["source_intent_lock_sha256"] = core["intent_lock"]["canonical_sha256"]
        pack["candidate_bundles"] = forged
        failures = self.semantic_audit(pack)
        self.assertTrue(any("contents or joint admission differ" in row["reason"] for row in failures), failures)

    def test_bundle_entrypoint_rejects_malformed_stale_and_wrong_request_snapshots(self):
        core, snapshot, pack, _ = bound_inputs(True)
        for label, invalid in self.invalid_snapshots(core, snapshot).items():
            with self.subTest(label=label):
                changed = copy.deepcopy(pack)
                changed["creative_controls"] = invalid
                with self.assertRaises(ValueError):
                    self.bundles(changed)

    def test_auditor_bundle_recomputation_rejects_invalid_snapshot(self):
        core, snapshot, pack, _ = bound_inputs(True)
        pack["candidate_bundles"] = self.bundles(pack)
        pack["creative_controls"] = self.invalid_snapshots(core, snapshot)["malformed"]
        failures = self.semantic_audit(pack)
        self.assertTrue(any("source recomputation failed" in row["reason"] for row in failures), failures)

    def test_adult_constraint_receives_bound_context_even_when_valid_axes_are_inactive(self):
        data = self.synthetic_adult_data()
        original = generator.authorial_core_generation_constraints
        for no_people in (False, True):
            with self.subTest(no_people=no_people):
                core, snapshot, _, result = bound_inputs(no_people)
                observed = []

                def capture(*args, **kwargs):
                    constraints = original(*args, **kwargs)
                    observed.append((kwargs.get("creative_control_snapshot"), constraints))
                    return constraints

                with patch.object(generator, "authorial_core_generation_constraints", side_effect=capture):
                    adult = generator.candidate_pack_contextual_adult_appeal(data, result, {}, authorial_core=core)
                self.assertEqual(len(observed), 1)
                self.assertEqual(observed[0][0], snapshot)
                self.assertEqual(observed[0][1]["no_people"], no_people)
                guard = {"subject_category": snapshot["context"]["subject_category"],
                         "adult_allowed": adult["eligibility"]["status"] == "eligible",
                         "intent_constraints": observed[0][1]}
                self.assertEqual(
                    generator.entry_block_reason(data["slots"]["lighting"][0], "lighting", guard),
                    "explicit_no_people" if no_people else None,
                )
                self.assertIsNone(generator.entry_block_reason(data["slots"]["lighting"][1], "lighting", guard))
                for axis in contextual.AXES:
                    row = adult["axes"][axis]
                    if no_people:
                        # Actual validated production behavior: no active axis,
                        # not proof of a reachable active-inventory guard effect.
                        self.assertEqual(snapshot["adult_appeal"][axis]["reason"], "explicit_no_people")
                        self.assertFalse(row["active"])
                        self.assertEqual(row["candidate_inventory"], [])
                    else:
                        self.assertTrue(row["active"])
                        self.assertEqual({item["entry_id"] for item in row["candidate_inventory"]},
                                         {"synthetic_human_light", "synthetic_neutral_light"})

    def test_adult_entrypoint_rejects_invalid_snapshots_even_with_inactive_axes(self):
        core, snapshot, _, result = bound_inputs(True)
        data = self.synthetic_adult_data()
        for label, invalid in self.invalid_snapshots(core, snapshot).items():
            with self.subTest(label=label):
                changed = copy.deepcopy(result)
                changed["provenance"]["creative_controls"] = invalid
                with self.assertRaises(ValueError):
                    generator.candidate_pack_contextual_adult_appeal(data, changed, {}, authorial_core=core)


if __name__ == "__main__":
    unittest.main()
