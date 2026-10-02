"""Neutral descriptions must preserve full relations and frozen layer choices."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import audit_composed_prompt as audit
import prompt_generator as pg


NEUTRAL_RELATIONS = {
    "clothing_ct037_v1": (
        "the garment opening at the neck hangs in loose folds of the same continuous fabric",
        "a separate scarf hangs in loose folds around the neck",
        "the garment opening at the neck hangs in loose folds",
    ),
    "clothing_ct090_v2": (
        "fine threads form an evenly spaced network of actual open cells in the garment fabric",
        "a printed pattern forms evenly spaced dots on the garment fabric",
        "fine threads form an evenly spaced network in the garment fabric",
    ),
    "clothing_ct023_v2": (
        "a fitted paneled bodice has two center-front edges joined by a vertical row of metal loops engaging matching studs",
        "a nearby metal case has edges joined by a vertical row of loops and studs",
        "a fitted paneled bodice has two center-front edges and decorative metal loops",
    ),
}


class PhotoSemanticGuidanceDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}

    def bound_pack(self, profile_id, evidence):
        intent = pg.normalize_visual_intent({
            "contract_version": "photo-visual-intent/v1",
            "provenance": "agent_prepack",
            "obligations": [{
                "profile_id": profile_id,
                "source": "explicit_user_requirement",
                "scope": "request_only",
                "source_text": "Photograph this garment on an adult subject with the specified visible structure.",
                "bindings": evidence,
            }],
        }, self.registry)
        obligation = pg.candidate_pack_visual_profile_obligation(
            self.profiles[profile_id], self.registry,
            activation_source="agent_prepack", source_intent_ids=[intent["request_id"]],
            bindings=intent["obligations"][0]["bindings"],
        )
        return {"visual_intent": intent, "visual_obligations": {
            "enabled": True, "contract_version": "photo-visual-obligations/v1",
            "obligations": [obligation],
            "source_visual_intent_sha256": intent["canonical_sha256"],
            "required_hard_gates": [g["id"] for g in obligation["render_gates"]],
        }}

    @staticmethod
    def composed(profile_id, evidence):
        return {"chosen_visual_concept_ids": [],
                "visual_obligation_evidence": {profile_id: copy.deepcopy(evidence)},
                "prompt_en": "; ".join(evidence.values()) + "."}

    def test_neutral_relations_accept_complete_structure_and_reject_substitution(self):
        for pid, (complete, wrong_owner, incomplete) in NEUTRAL_RELATIONS.items():
            with self.subTest(profile=pid):
                requirement = self.profiles[pid]["evidence_requirements"]["visible_relation_phrase"]
                pg.validate_visual_intent_binding(obligation_index=0, field="visible_relation_phrase",
                                                phrase=complete, requirement=requirement)
                for invalid in (wrong_owner, incomplete, "an ordinary garment with decorative details"):
                    with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                        pg.validate_visual_intent_binding(obligation_index=0, field="visible_relation_phrase",
                                                        phrase=invalid, requirement=requirement)

    def test_neutral_component_matches_require_opt_in(self):
        cohort = {**self.registry, "profiles": [self.profiles[pid] for pid in NEUTRAL_RELATIONS]}
        for pid, (complete, wrong_owner, incomplete) in NEUTRAL_RELATIONS.items():
            with self.subTest(profile=pid):
                sources = [{"source": "concept_lock", "text": complete, "polarity": "required"}]
                self.assertNotIn(pid, pg.candidate_pack_auto_visual_obligation_matches(cohort, sources))
                self.assertIn(pid, pg.candidate_pack_auto_visual_concept_matches(cohort, sources))
                for invalid in (wrong_owner, incomplete):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[pid], invalid))

    def test_neutral_relation_evidence_must_remain_literal_in_composed_prompt(self):
        for pid, (complete, _, _) in NEUTRAL_RELATIONS.items():
            with self.subTest(profile=pid):
                evidence = {"visible_relation_phrase": complete}
                pack = self.bound_pack(pid, evidence)
                composed = self.composed(pid, evidence)
                self.assertEqual(audit.audit_visual_obligations(pack, composed, composed["prompt_en"]), [])
                composed["prompt_en"] = "An adult subject wears a garment with understated details."
                failures = audit.audit_visual_obligations(pack, composed, composed["prompt_en"])
                self.assertIn("visual_obligation_prompt_binding", {f["check"] for f in failures})

    @staticmethod
    def sheer_evidence():
        return {
            "translucent_textile_phrase": "A garment textile layer that partially transmits the view behind it covers the adult subject's upper arm",
            "visible_weave_edge_phrase": "The textile surface and folded edge remain visible around the sleeve cuff",
            "transmitted_light_phrase": "Soft light passes through the fabric along this single sleeve",
            "layer_contrast_phrase": "Underlying body contours remain partly visible beneath the readable garment fibers of that same sleeve",
            "material_behavior_phrase": "Folds become denser and less transparent where the sleeve bends at the adult elbow",
        }

    def test_sheer_underlying_surface_choices_are_valid_but_not_interchangeable_after_freezing(self):
        pid = "sheer_garment_optical_layering"
        evidence = self.sheer_evidence()
        pack = self.bound_pack(pid, evidence)
        composed = self.composed(pid, evidence)
        self.assertEqual(audit.audit_visual_obligations(pack, composed, composed["prompt_en"]), [])
        alternatives = (
            "The opaque underlayer remains partly visible beneath the adult subject's sleeve",
            "The requested lower garment remains partly visible beneath the transmitting textile",
            "The background remains partly visible through the same garment panel",
        )
        for alternative in alternatives:
            with self.subTest(layer=alternative):
                changed = {**evidence, "layer_contrast_phrase": alternative}
                self.bound_pack(pid, changed)  # Each choice is valid when it is requested independently.
                changed_composed = self.composed(pid, changed)
                failures = audit.audit_visual_obligations(pack, changed_composed, changed_composed["prompt_en"])
                self.assertIn("visual_obligation_hard_binding", {f["check"] for f in failures})

    def test_sheer_requires_every_textile_light_and_layer_field(self):
        pid = "sheer_garment_optical_layering"
        evidence = self.sheer_evidence()
        pack = self.bound_pack(pid, evidence)
        for field in evidence:
            with self.subTest(missing=field):
                incomplete = {k: v for k, v in evidence.items() if k != field}
                composed = self.composed(pid, incomplete)
                failures = audit.audit_visual_obligations(pack, composed, composed["prompt_en"])
                self.assertTrue(any(f["check"] == "visual_obligation_evidence" and field in f.get("missing", [])
                                    for f in failures), failures)


if __name__ == "__main__":
    unittest.main()
