"""Pose research promotion: real retrieval, meaning boundaries and scope.

These are contract tests, not anatomical or rendered-image qualification.
"""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest import mock

from tests import photo_prompt_fixtures as fixtures
import prompt_generator as generator
import photo_candidate_semantics as semantics
import audit_composed_prompt as auditor
from photo_contracts import property_effects_allowed

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
RESEARCH = ROOT / "docs/research-evidence/photo-prompt/pose-vocabulary-20261002"
EXTENSION = "photo_prompt_pose_vocabulary_extension.json"


class PhotoPoseVocabularySemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = generator.load_json(ASSETS / "photo_prompt_tags.json")
        cls.data[generator.QUALITY_LAYERS_DATA_KEY] = generator.load_quality_layers(ASSETS / "photo_prompt_quality_layers.json")
        cls.extension = json.loads((ASSETS / EXTENSION).read_text())
        cls.registry = generator.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}
        cls.ledger = json.loads((RESEARCH / "implementation/implementation-disposition-ledger.json").read_text())

    def hard_matches(self, text):
        return set(generator.candidate_pack_auto_visual_obligation_matches(self.registry, [{
            "source": "concept_lock", "text": text, "polarity": "required", "priority": "critical", "mandatory": True,
        }]))

    def frozen(self, event, subject="an adult woman", *, pose_open=True):
        request = "A complex photographic portrait showing a readable bodily configuration."
        prompt = ("A complex photographic portrait shows " + subject + " in an open studio with a visible support surface. "
                  + event + ". The complete contact arrangement is readable, with controlled warm-neutral light, "
                  "natural fabric texture, a clear focal hierarchy, and enough separation between the subject and the background.")
        raw = fixtures.core(request, subject=subject, setting="an open studio with a visible support surface", event=event,
                            baseline_prompt_en=prompt, interpreted_intent="An independently authored complex portrait with readable pose and contact.",
                            anchor_evidence=("A complex photographic portrait", subject, "The complete contact arrangement is readable"),
                            open_dimensions=tuple(["relationship", "expression", "framing", "composition", "lighting", "camera", "action"] + (["pose"] if pose_open else [])))
        controls = generator.creative_controls.resolve(request, context={"subject_category": "human", "no_people": False, "explicit_nonsexual": False},
                                                       overrides={"sensual": 0, "fetish": 0, "surreal": 0, "creativity": 1}, seed=19)
        raw["creative_controls_sha256"] = controls["canonical_sha256"]
        core = generator.normalize_authorial_core(raw, request_envelope=generator.normalize_request_envelope(fixtures.envelope(request)),
                                                 creative_control_snapshot=controls)
        return core, controls

    def test_promotions_have_traceable_dispositions_and_unreviewed_terms_stay_out(self):
        rows = {row["research_id"]: row for row in self.ledger["dispositions"]}
        self.assertEqual(set(rows), {row["id"] for row in json.loads((RESEARCH / "candidate-data.proposed.json").read_text())["candidates"]})
        runtime_ids = {entry["id"] for entries in self.extension["slots"].values() for entry in entries}
        for row in rows.values():
            self.assertTrue(row["source_ids"])
            self.assertTrue(row["confusion_boundaries"])
            if row["status"] == "deferred_variant_or_source_review":
                self.assertNotIn(row["research_id"], runtime_ids)
                self.assertIsNone(row["runtime_candidate"])
                self.assertTrue(row["reason"])
        for name in ("pv_finger_heart", "pv_m_leg_variant", "pv_passe_phase", "pv_bakasana", "pv_squinch"):
            self.assertEqual(rows[name]["status"], "deferred_variant_or_source_review")
        self.assertTrue(self.ledger["maintenance_only"])
        self.assertEqual(self.extension["maintenance_ref"]["sha256"], semantics.digest(self.ledger))

    def test_reuse_appends_context_without_changing_existing_meaning_or_guards(self):
        # Acting context reuses pose-owned facial entries; exclude that later
        # dependent overlay while reconstructing the pre-pose historical state.
        filenames = tuple(name for name in generator.RESEARCH_EXTENSION_FILENAMES
                          if name not in {EXTENSION, "photo_prompt_acting_expression_extension.json",
                                          "photo_prompt_neutral_expression_extension.json",
                                          "photo_prompt_slang_visual_extension.json"})
        with mock.patch.object(generator, "RESEARCH_EXTENSION_FILENAMES", filenames):
            before = generator.load_json(ASSETS / "photo_prompt_tags.json")
        for slot, additions in self.extension["existing_slot_context_extensions"].items():
            original = {entry["id"]: entry for entry in before["slots"][slot]}
            current = {entry["id"]: entry for entry in self.data["slots"][slot]}
            for entry_id, addition in additions.items():
                with self.subTest(slot=slot, entry=entry_id):
                    fields = set(original[entry_id]) - {"paraphrases", "contextual_usage"}
                    self.assertEqual({field: original[entry_id][field] for field in fields},
                                     {field: current[entry_id][field] for field in fields})
                    self.assertTrue(set(addition["paraphrases"]) <= set(current[entry_id]["paraphrases"]))

    def test_seated_crossing_and_kneeling_variants_do_not_share_hard_meaning(self):
        pairs = [("figure-four sitting pose", "pv_profile_figure_four", "pv_profile_knee_over_knee"),
                 ("knee-over-knee pose", "pv_profile_knee_over_knee", "pv_profile_figure_four"),
                 ("upright kneeling pose", "pv_profile_tall_kneel", "pv_profile_heel_sit"),
                 ("heel-sitting pose", "pv_profile_heel_sit", "pv_profile_tall_kneel"),
                 ("reverse-chair pose", "pv_profile_reverse_chair", "pv_profile_chair_straddle"),
                 ("chair-straddle pose", "pv_profile_chair_straddle", "pv_profile_reverse_chair")]
        for phrase, expected, substitute in pairs:
            with self.subTest(phrase=phrase):
                matches = self.hard_matches("an adult woman in a " + phrase)
                self.assertIn(expected, matches)
                self.assertNotIn(substitute, matches)

    def test_negation_and_bare_homonyms_do_not_activate_new_pose_profiles(self):
        for text in ("an arabesque ornament on a ceramic vessel", "a prone-to-failure circuit", "a V-sign antenna",
                     "a violin chin rest", "a four-legged quadruped animal", "a ballet portrait with an arabesque wall motif",
                     "an adult woman, no arabesque pose", "an adult woman without upright kneeling pose"):
            with self.subTest(text=text):
                self.assertFalse(any(profile.startswith("pv_profile_") for profile in self.hard_matches(text)))
        terms = {term.casefold() for profile in self.profiles.values() if profile["id"].startswith("pv_profile_")
                 for term in profile["activation"]["exact_terms"]}
        self.assertNotIn("bambi pose", terms)
        self.assertNotIn("밤비 포즈", terms)

    def test_profile_components_bind_every_gate_and_require_visible_complete_relations(self):
        for profile in self.profiles.values():
            if not profile["id"].startswith("pv_profile_"):
                continue
            components = profile["authored_components"]["components"]
            self.assertEqual(profile["required_evidence_fields"], [item["evidence_field"] for item in components])
            self.assertEqual(profile["render_gates"], [item["render_gate"] for item in components])
            self.assertEqual(profile["semantics"]["component_semantics"]["minimum_component_groups"], len(components))
            self.assertTrue(all("partial" in gate["description"] and "unobservable" in gate["description"] for gate in profile["render_gates"]))
            self.assertIn("A locked crop is preserved", " ".join(profile["semantics"]["claim_limits"]))

    def test_property_scope_cannot_change_a_locked_hand_configuration_or_reference_appearance(self):
        entry = next(row for row in self.extension["slots"]["hand_pose"] if row["id"] == "pv_v_sign")
        lock = {"contract_version": "photo-intent-lock/v2", "open_dimensions": ["pose"], "semantic_anchors": [
            {"dimension": "pose", "target": "main_subject", "property": "body.hand_configuration"},
            {"dimension": "appearance", "target": "main_subject", "property": "hair"},
        ]}
        self.assertFalse(property_effects_allowed(lock, entry["affected_dimensions"], entry["affected_properties"]))
        lock["semantic_anchors"].pop(0)
        self.assertTrue(property_effects_allowed(lock, entry["affected_dimensions"], entry["affected_properties"]))
        for entries in self.extension["slots"].values():
            for candidate in entries:
                self.assertFalse(set(candidate["affected_dimensions"]) & {"appearance", "identity", "count", "framing", "sexual_tone"})

    def test_real_core_retrieval_exposes_the_matching_geometry_and_is_recomputable(self):
        cases = [("body_pose", "pv_figure_four"), ("body_pose", "pv_tall_kneel"),
                 ("hand_pose", "pv_v_sign"), ("body_pose", "pv_arabesque")]
        for slot, entry_id in cases:
            entry = next(row for row in self.extension["slots"][slot] if row["id"] == entry_id)
            core, controls = self.frozen(entry["en"])
            raw = copy.deepcopy(core)
            for field in ("core_id", "canonical_sha256", "request_binding"):
                raw.pop(field, None)
            raw["intent_lock"] = {key: value for key, value in raw["intent_lock"].items()
                                  if key in {"contract_version", "priority", "semantic_anchors", "locked_dimensions", "open_dimensions"}}
            raw["semantic_assertions"] = [{"assertion_id": "observed_pose", "dimension": "pose", "polarity": "advisory",
                                            "source_span_ids": ["scope_1"], "affected_dimensions": ["pose"],
                                            "axes": {"configuration": entry["concept_units"]}, "evidence": {}}]
            core = generator.normalize_authorial_core(raw, request_envelope=generator.normalize_request_envelope(fixtures.envelope(raw["source_request"])),
                                                     creative_control_snapshot=controls)
            unchanged = copy.deepcopy(core)
            slots, binding, _ = generator.retrieve_core_slots(self.data, core, controls)
            with self.subTest(entry=entry_id):
                candidate = next(row for row in slots[slot]["candidates"] if row["entry_id"] == entry_id)
                self.assertEqual(candidate["label_en"], entry["en"])
                source = generator.candidate_pack_slot_entry_by_id(self.data, slot, candidate["entry_id"])
                surface = semantics.semantic_source(source, slot, self.data["candidate_semantic_policy"])
                self.assertEqual(surface["concept_units"], entry["concept_units"])
                self.assertEqual(surface["affected_properties"], entry["affected_properties"])
                self.assertEqual(auditor.audit_core_retrieval({"slots": slots, "core_retrieval": binding, "authorial_core": core,
                                                             "creative_controls": controls}, self.data), [])
                self.assertEqual(core, unchanged)

    def test_partner_contacts_require_grounded_partner_context_and_bundle_links_are_optional(self):
        entry = next(row for row in self.extension["slots"]["contact_point"] if row["id"] == "pv_handholding_pair")
        core, controls = self.frozen("one hand gently contacts the other hand belonging to the same woman")
        contract, picked = generator.frozen_core_context(self.data, core, controls)
        self.assertFalse(generator.core_slot_entry_eligible(self.data, core, contract, picked, "contact_point", entry))
        core, controls = self.frozen(entry["en"], "an adult woman with an adult partner in a pair")
        contract, picked = generator.frozen_core_context(self.data, core, controls)
        self.assertTrue(generator.core_slot_entry_eligible(self.data, core, contract, picked, "contact_point", entry))
        for bundle in self.data["candidate_bundles"]:
            if bundle["id"].startswith("pv_bundle_"):
                self.assertEqual(bundle["adoption"], "optional")
                self.assertEqual(bundle["profile_activation"], "independent_request_evidence_only")
                self.assertTrue(set(bundle["associated_profile_ids"]) <= set(self.profiles))


if __name__ == "__main__":
    unittest.main()
