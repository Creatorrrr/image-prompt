from __future__ import annotations

from tests import photo_prompt_fixtures as current_fixtures

import copy
import random
import unittest

from tests import photo_prompt_fixtures as fixtures
from tests import test_photo_authorial_core_v6 as v6_fixtures
from tests import test_photo_authorship_policy as composition_fixtures
import prompt_generator as generator
import audit_composed_prompt as auditor
import audit_image_render_request as runtime_auditor
import validate_photo_prompt_dictionary as dictionary_validator
from photo_contracts import ADULT_APPEAL_AXIS_DIMENSIONS
import photo_contextual_appeal as contextual


class PhotoAdultAppealScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = v6_fixtures.PhotoAuthorialCoreV6Tests().runtime_data()
        source = "An adult woman in a Gothic portrait with CCD direct flash."
        raw = fixtures.core(
            source,
            interpreted_intent="A poised adult portrait keeps Gothic styling and CCD direct flash.",
            subject="one adult woman",
            setting="a quiet portrait studio",
            event="she stands confidently beside the window",
            visual_priorities=("Gothic styling", "CCD direct flash", "natural skin"),
            baseline_prompt_en=(
                "An adult woman stands confidently in a quiet portrait studio. Gothic styling "
                "and CCD direct flash establish the photographic treatment. She keeps a composed "
                "expression and relaxed posture beside a tall window, with textured clothing, "
                "natural skin, coherent depth, and a simple background supporting her presence in the frame."
            ),
            locked_dimensions=("concept", "subject", "event", "style", "lighting"),
            open_dimensions=("composition", "framing"),
            anchor_evidence=("quiet portrait studio", "An adult woman", "stands confidently", "Gothic styling", "CCD direct flash"),
        )
        raw["contract_version"] = "photo-authorial-core/v3"
        raw["semantic_assertions"] = []
        envelope = generator.normalize_request_envelope(fixtures.envelope(source))
        cls.core = generator.normalize_authorial_core(raw, request_envelope=envelope)
        cls.result = current_fixtures.generate_once(
            cls.data, random.Random(77), None, ["en"], True, 12, True,
            selection_mode="rule", include_trace=True, concept_locks=[source],
            seed=77, creativity=0.0, authorial_core=cls.core, fixture_context={"subject_category": "human"},
            sensual_intensity=2,
            fetish_intensity=1,
            adult_appeal_activation_source="skill_default",
        )
        cls.pack = generator.build_candidate_pack(cls.result, cls.data, "v6")

    def adult(self, *, locked=None, result=None):
        core = copy.deepcopy(self.core)
        if locked is not None:
            core["intent_lock"]["locked_dimensions"] = list(locked)
        return generator.candidate_pack_contextual_adult_appeal(
            self.data, result or self.result, {}, authorial_core=core,
        )

    def composed(self):
        composed = composition_fixtures.PhotoAuthorshipPolicyTests.composed(self.pack)
        sensual = "Her lowered shoulder softens the silhouette against the dark window"
        material = "Satin catches a narrow highlight along the existing garment seam"
        composed["prompt_en"] += f" {sensual}. {material}."
        composed["adult_appeal_brief"] = {
            "adult_subject_phrase": "An adult woman",
            "agency_phrase": "stands confidently",
            "axes": {
                "sensual": {
                    "intensity": 2,
                    "artistic_interpretation": "Use a relaxed shoulder to support her composed presence",
                    "affected_dimensions": ["pose"],
                    "prompt_evidence": sensual,
                },
                "fetish": {
                    "intensity": 1,
                    "artistic_interpretation": "Give the existing fabric a tactile surface response",
                    "affected_dimensions": ["material"],
                    "prompt_evidence": material,
                },
            },
            "blend": {"emphasis": self.pack["adult_appeal"]["blend"]["emphasis"]},
        }
        composed["adult_appeal_brief"]["contextual_review"] = [
            {"candidate_id": cid, "reading": "irrelevant", "reason": "Retain the authored shoulder and satin evidence; the alternative adds a competing scene detail."}
            for cid in self.pack["adult_appeal"]["contextual_retrieval"]["review_candidate_ids"]
        ]
        composed["adult_appeal_brief"]["contextual_comparison"] = "At the same requested strengths, the baseline shoulder and satin seam preserve the quiet portrait; the alternatives distract from its composed presence."
        composed["embodiment_review"] = fixtures.composition_review(self.pack, composed["prompt_en"])
        return composed

    def test_locked_style_and_flash_preserve_both_requested_intensities(self):
        adult = self.pack["adult_appeal"]
        self.assertEqual([adult["axes"][a]["intensity"] for a in ADULT_APPEAL_AXIS_DIMENSIONS], [2, 1])
        self.assertEqual(auditor.audit_adult_appeal_dimension_scope(self.pack, adult), [])
        allowed = adult["dimension_scope"]["axis_allowed_dimensions"]
        self.assertIn("expression", allowed["sensual"])
        self.assertNotIn("expression", self.core["intent_lock"]["open_dimensions"])
        candidates = generator.candidate_pack_adult_candidates(adult)
        self.assertTrue(candidates)
        self.assertTrue(adult["axes"]["fetish"]["candidate_inventory"])
        for row in candidates:
            self.assertTrue(row["affected_dimensions"])
            self.assertFalse(set(row["affected_dimensions"]) & {"style", "lighting"})

    def test_locked_garment_excludes_whole_conflicting_candidates(self):
        adult = self.adult(locked=[*self.core["intent_lock"]["locked_dimensions"], "appearance"])
        self.assertTrue(adult["axes"]["fetish"]["active"])
        self.assertIn("material", adult["dimension_scope"]["axis_allowed_dimensions"]["fetish"])
        for row in generator.candidate_pack_adult_candidates(adult):
            self.assertNotIn("appearance", row["affected_dimensions"])
            self.assertNotEqual(row["slot"], "fetish_styling")
            self.assertNotIn("adjusting_choker_gloves", row["id"])

    def test_inventory_override_cannot_erase_an_entry_declared_effect(self):
        data = dict(self.data, slots=dict(self.data["slots"]))
        data["slots"]["action"] = [
            dict(row, affected_dimensions=["lighting"]) if row["id"] == "posing_editorial" else row
            for row in self.data["slots"]["action"]
        ]
        adult = generator.candidate_pack_contextual_adult_appeal(data, self.result, {}, authorial_core=self.core)
        self.assertFalse(any(row["id"].endswith(":posing_editorial") for row in generator.candidate_pack_adult_candidates(adult)))

    def test_exhausted_current_scope_disables_axes_without_losing_requested_strengths(self):
        adult = self.adult(locked=set(self.core["intent_lock"]["locked_dimensions"]) | contextual.allowed_dimensions(self.core["intent_lock"]))
        self.assertFalse(adult["enabled"])
        for axis, requested in (("sensual", 2), ("fetish", 1)):
            self.assertEqual(adult["axes"][axis]["intensity"], 0)
            self.assertEqual(adult["axes"][axis]["requested_intensity"], requested)
        self.assertFalse(generator.candidate_pack_adult_candidates(adult))

    def test_explicit_opt_out_remains_off(self):
        result = copy.deepcopy(self.result)
        result["provenance"]["creative_controls"] = generator.creative_controls.resolve(
            self.core["source_request"], overrides={"sensual": 0, "fetish": 0},
            context={"subject_category": "human"}, seed=77)
        adult = self.adult(result=result)
        self.assertFalse(adult["enabled"])
        self.assertFalse(generator.candidate_pack_adult_candidates(adult))

    def test_full_composed_audit_accepts_unlocked_pose_and_material(self):
        report = auditor.audit_composed_prompt(self.pack, self.composed())
        self.assertEqual(report["status"], "pass", report["failures"])

    def test_exact_runtime_accepts_the_scoped_composition(self):
        composed = self.composed()
        report = auditor.audit_composed_prompt(self.pack, composed)
        request = {
            "schema_version": runtime_auditor.SCHEMA_VERSION,
            "pack_id": self.pack["pack_id"],
            "source_intent_lock_sha256": self.pack["authorial_core"]["intent_lock"]["canonical_sha256"],
            "source_embodiment_preflight_sha256": self.pack["embodiment_preflight"]["canonical_sha256"],
            "runtime_prompt_en": composed["prompt_en"] + "\n\nAvoid: " + composed["negative_en"],
            "runtime_negative_en": composed["negative_en"],
            "references": [],
            "audit_boundary": {
                "composed_prompt_audit_status": report["status"],
                "runtime_prompt_audit_status": "not_run",
                "inherits_composed_prompt_pass": False,
            },
        }
        runtime = runtime_auditor.audit_image_render_request(self.pack, composed, request)
        self.assertEqual(runtime["status"], "pass", runtime["failures"])

    def test_composed_audit_rejects_locked_and_undeclared_effects(self):
        for dimensions in (["lighting"], []):
            composed = self.composed()
            composed["adult_appeal_brief"]["axes"]["sensual"]["affected_dimensions"] = dimensions
            report = auditor.audit_composed_prompt(self.pack, composed)
            self.assertIn("adult_appeal_authored_dimensions", {r["check"] for r in report["failures"]})

    def test_scope_and_candidate_tampering_fail(self):
        pack = copy.deepcopy(self.pack)
        pack["adult_appeal"]["dimension_scope"]["axis_allowed_dimensions"]["sensual"].append("lighting")
        self.assertTrue(auditor.audit_adult_appeal_dimension_scope(pack, pack["adult_appeal"]))
        pack = copy.deepcopy(self.pack)
        candidate = pack["adult_appeal"]["axes"]["sensual"]["candidate_inventory"][0]
        candidate["affected_dimensions"] = ["lighting"]
        self.assertIn("adult_appeal_candidate_dimensions", {r["check"] for r in auditor.audit_adult_appeal_dimension_scope(pack, pack["adult_appeal"])})

    def test_adopted_candidate_requires_its_complete_effect_in_the_brief(self):
        candidate = copy.deepcopy(self.pack["adult_appeal"]["axes"]["fetish"]["candidate_inventory"][0])
        # Unit fixture proves the complete-effect requirement independently of retrieval rank.
        candidate["affected_dimensions"] = ["appearance", "material"]
        composed = self.composed()
        reviews = composed["adult_appeal_brief"]["contextual_review"]
        reviews[:] = [row for row in reviews if row["candidate_id"] != candidate["id"]]
        reviews.append({"candidate_id": candidate["id"], "reading": "relevant", "reason": "A tactile seam supports the composed Gothic portrait.", "proposed_application": "Keep the existing garment and express the effect as the narrow satin highlight."})
        failures, _ = auditor.audit_adult_appeal(self.pack, composed, composed["prompt_en"], {candidate["id"]}, {candidate["id"]: candidate})
        self.assertIn("adult_appeal_authored_dimensions", {r["check"] for r in failures})
        composed["adult_appeal_brief"]["axes"]["fetish"]["affected_dimensions"] = candidate["affected_dimensions"]
        reviews = composed["adult_appeal_brief"]["contextual_review"]
        reviews[:] = [row for row in reviews if row["candidate_id"] != candidate["id"]]
        reviews.append({"candidate_id": candidate["id"], "reading": "relevant", "reason": "A tactile seam supports the composed Gothic portrait.", "proposed_application": "Keep the existing garment and express the effect as the narrow satin highlight."})
        failures, _ = auditor.audit_adult_appeal(self.pack, composed, composed["prompt_en"], {candidate["id"]}, {candidate["id"]: candidate})
        self.assertEqual(failures, [])

    def test_sampled_adult_candidate_uses_same_scope_but_other_candidates_do_not(self):
        candidate = copy.deepcopy(self.pack["adult_appeal"]["axes"]["fetish"]["candidate_inventory"][0])
        # Unit fixture proves the complete-effect requirement independently of retrieval rank.
        candidate["affected_dimensions"] = ["appearance", "material"]
        pack = copy.deepcopy(self.pack)
        pack["creative_augmentation"]["candidates"] = [dict(candidate, semantic_band="near", source_kind="adult_appeal")]
        evidence = "A narrow band of reflected light traces the existing garment's stitched edge"
        decision = {
            "candidate_id": candidate["id"], "decision": "transformed",
            "rationale": "retain the existing Gothic portrait while emphasizing tactile garment structure",
            "artistic_interpretation": "translate the garment material into a restrained structural highlight",
            "transformation": "tie the material to the existing seam rather than a detached styling label",
            "affected_dimensions": candidate["affected_dimensions"], "prompt_evidence": evidence,
        }
        composed = {"creative_augmentation_brief": {"decisions": [decision]}}
        failures = auditor.audit_creative_augmentation(pack, composed, evidence, {candidate["id"]})
        self.assertEqual(failures, [])
        decision["affected_dimensions"] = ["lighting"]
        failures = auditor.audit_creative_augmentation(pack, composed, evidence, {candidate["id"]})
        self.assertIn("intent_lock_creative_dimensions", {r["check"] for r in failures})
        decision["affected_dimensions"] = ["material"]
        decision["candidate_id"] = "slot:texture:ordinary-test-candidate"
        pack["creative_augmentation"]["candidates"][0]["id"] = decision["candidate_id"]
        failures = auditor.audit_creative_augmentation(pack, composed, evidence, {decision["candidate_id"]})
        self.assertIn("intent_lock_creative_dimensions", {r["check"] for r in failures})

    def test_missing_current_dimension_scope_is_rejected(self):
        pack = copy.deepcopy(self.pack)
        pack["adult_appeal"].pop("dimension_scope")
        report = auditor.audit_composed_prompt(pack, self.composed())
        self.assertIn("adult_appeal_dimension_scope", {r["check"] for r in report["failures"]})

    def test_dimension_policy_rejects_unknown_source_and_dimension(self):
        quality = copy.deepcopy(self.data[generator.QUALITY_LAYERS_DATA_KEY])
        quality["adult_appeal"]["entry_dimensions"]["action:missing-entry"] = ["invented_dimension"]
        errors = []
        dictionary_validator.validate_quality_layer_adult_appeal(quality, self.data, errors)
        self.assertTrue(any("unknown candidate" in e for e in errors))
        self.assertTrue(any("unknown dimensions" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
