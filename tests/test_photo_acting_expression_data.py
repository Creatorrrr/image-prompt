from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest
from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as g
import photo_candidate_semantics as semantics
from photo_visual_retrieval import positive_visual_profile_text
from photo_contracts import property_effects_allowed


class ActingExpressionDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = g.load_json(ASSETS / "photo_prompt_tags.json")
        cls.registry = g.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.index = g.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", cls.registry)
        cls.profiles = [p for p in cls.registry["profiles"] if p["id"].startswith("ae_profile_")]
        cls.scoped_registry = {**cls.registry, "profiles": cls.profiles}
        cls.scoped_index = g.build_visual_profile_index_payload(cls.scoped_registry)

    def exact(self, text, polarity="positive"):
        hits = g.resolve_visual_profile_hits(self.scoped_registry, [{"source":"user_requirement", "text":text,"polarity":polarity}], visual_profile_index=self.scoped_index)["hits"]
        return {r["profile_id"] for r in hits if r["hard_eligible"] and r["profile_id"].startswith("ae_profile_")}

    def entry(self, slot, entry_id):
        return next(r for r in self.data["slots"][slot] if r["id"] == entry_id)

    def test_bilingual_form_requests_activate_but_negation_and_excluded_spans_do_not(self):
        for profile in self.profiles:
            ko = profile["activation"]["exact_terms"][0]
            en = next(t for t in profile["activation"]["exact_terms"] if t.isascii())
            with self.subTest(profile=profile["id"]):
                self.assertIn(profile["id"], self.exact("성인 배우 얼굴 클로즈업: " + ko))
                self.assertIn(profile["id"], self.exact("An adult actor face with " + en))
                self.assertNotIn(profile["id"], self.exact("An adult actor face with no " + en))
                self.assertNotIn(profile["id"], self.exact("An adult actor face with " + en,"excluded"))

    def test_form_word_in_non_actor_domain_and_broad_affect_never_harden(self):
        for text in ["Lip pressing machinery in a factory", "A single-brow raise discussion in a dictionary", "Smoldering embers on a sultry afternoon", "A neutral adult portrait shows a smug smile", "An adult actor portrays sadness and joy", "AU24 in a coding manual", "microexpression timing and voice quality"]:
            with self.subTest(text=text):
                self.assertFalse(self.exact(text))

    def test_new_forms_are_resolved_by_the_real_merged_registry_and_index(self):
        hits=g.resolve_visual_profile_hits(self.registry,[{"source":"user_requirement","text":"An adult actor face with pressed lips and one raised eyebrow"}],visual_profile_index=self.index)["hits"]
        required={r["profile_id"] for r in hits if r["hard_eligible"]}
        self.assertTrue({"ae_profile_lip_press","ae_profile_single_brow"} <= required)

    def test_current_v6_exposes_new_candidates_when_expression_is_open(self):
        # This is an explicitly synthetic maintenance fixture, not requester text
        # for one of the three independently authored image-generation arms.
        request = "A close portrait of an adult actor rehearsing a facial performance."
        baseline = (
            "An adult actor sits at a rehearsal desk and performs a precise facial reaction. "
            "The upper and lower lips press firmly together into a flattened contact line, "
            "with visibly compressed colored lip bands. The inner brow heads move inward "
            "and downward toward the glabella. Both brows, open eyes and the complete mouth "
            "remain clearly resolved in a near-frontal portrait under soft window light."
        )
        raw = fixtures.core(request, interpreted_intent="A performed facial reaction study",
            subject="An adult actor", setting="a quiet rehearsal room desk",
            event="performs a precise facial reaction", baseline_prompt_en=baseline,
            visual_priorities=("upper and lower lips compressed together", "inner brow heads move inward and downward"),
            open_dimensions=("expression", "framing", "composition", "lighting", "camera"),
            anchor_evidence=("a rehearsal desk", "An adult actor", "performs a precise facial reaction"))
        frozen = g.normalize_authorial_core(raw, request_envelope=g.normalize_request_envelope(fixtures.envelope(request)))
        runtime = g.load_runtime_data(ASSETS / "photo_prompt_tags.json")
        source = fixtures.candidate_source(runtime, frozen, seed=31003,
            context={"subject_category": "human", "no_people": False, "explicit_nonsexual": False})
        pack = g.candidate_pack_project(g.build_candidate_pack(source, runtime), "v6")
        candidates = pack["slots"]["expression"]["candidates"]
        exposed = {row["id"] for row in candidates}
        self.assertIn("slot:expression:ae_lip_press", exposed)
        new_rows = [row for row in candidates if ":ae_" in row["id"]]
        self.assertTrue(new_rows)
        self.assertEqual(pack["core_retrieval"]["candidate_adoption"], "optional")

    def test_press_tighten_and_mouth_opening_keep_distinct_requirements(self):
        self.assertEqual(self.exact("An actor face with lip pressing"), {"ae_profile_lip_press"})
        self.assertEqual(self.exact("An actor face with lip tightening"), {"ae_profile_lip_tighten"})
        self.assertFalse(self.exact("An adult face with parted lips and a relaxed jaw"))
        self.assertFalse(self.exact("An adult face showing a chin raised through head tilt"))

    def test_held_tears_requires_the_narrow_requested_compound(self):
        self.assertFalse(self.exact("An adult actor face holding back tears"))
        self.assertIn("ae_profile_held_tears_lips", self.exact("An adult actor face with pooled tears with pressed lips"))

    def test_context_guard_cannot_be_satisfied_by_its_own_candidate_tags(self):
        extension = json.loads((ASSETS / "photo_prompt_acting_expression_extension.json").read_text())
        for slot, rows in extension["slots"].items():
            for entry in rows:
                cues = entry.get("requires_primary_any_tags")
                if not cues:
                    continue
                with self.subTest(entry=entry["id"]):
                    picked = {"subject":{"tags":["human","adult"]}, "location":{"tags":["studio"]}, "action":{"tags":["portrait"]}}
                    polluted = copy.deepcopy(entry)
                    polluted["tags"] += cues
                    self.assertFalse(g.compatible_with_slot_context(slot,polluted,picked,self.data))
                    picked["action"]["tags"].append(cues[0])
                    self.assertTrue(g.compatible_with_slot_context(slot,entry,picked,self.data))

    def test_sultry_weather_does_not_unlock_attraction_or_adult_without_flirtation(self):
        picked={"subject":{"tags":["human","adult"]},"location":{"tags":["sultry","weather"]},"action":{"tags":["portrait"]}}
        self.assertFalse(g.compatible_with_slot_context("expression",self.entry("expression","ae_sultry_variant"),picked,self.data))
        self.assertFalse(g.compatible_with_slot_context("expression",self.entry("expression","ae_coquettish_variant"),picked,self.data))
        picked["action"]["tags"]=["flirting"]
        self.assertTrue(g.compatible_with_slot_context("expression",self.entry("expression","ae_coquettish_variant"),picked,self.data))
        picked["subject"]["tags"]=["human"]
        self.assertFalse(g.compatible_with_slot_context("expression",self.entry("expression","ae_coquettish_variant"),picked,self.data))

    def test_pose_and_gaze_effects_cannot_bypass_property_locks(self):
        entry=self.entry("body_orientation","ae_coy_variant")
        for dimension,prop in [("pose","head.orientation"),("expression","eyes.eyeline")]:
            lock={"contract_version":"photo-intent-lock/v2","semantic_anchors":[{"dimension":dimension,"target":"main_subject","property":prop}]}
            self.assertFalse(property_effects_allowed(lock,entry["affected_dimensions"],entry["affected_properties"]))

    def test_existing_specific_meanings_and_hand_ownership_are_preserved(self):
        self.assertIn("programmed", self.entry("expression","micro_precise_microexpression")["embedding_text"])
        self.assertIn("concentrating on a task",self.entry("expression","ctx_c126")["en"])
        self.assertIn("kindness",self.entry("expression","deadpan_kindness")["id"])
        own=self.entry("hand_pose","ae_hand_mouth")
        self.assertIn("own",own["en"])
        self.assertEqual(own["relations"][0]["subject"],"main_subject")
        self.assertFalse(any(r["id"]=="ae_mouth_cover_idiom" for r in self.data["slots"]["hand_pose"]))

    def test_negative_or_provenance_text_is_not_positive_retrieval_evidence(self):
        for profile in self.profiles:
            poisoned=copy.deepcopy(profile)
            poisoned["semantics"]["contrast_examples"].append("negative_surface_poison_marker")
            poisoned["semantics"]["claim_limits"].append("provenance_surface_poison_marker")
            positive=positive_visual_profile_text(poisoned)
            self.assertNotIn("poison_marker",positive)

    def test_runtime_bundles_are_advisory_and_maintenance_records_are_canonically_bound(self):
        bundles=[b for b in self.data["candidate_bundles"] if b["id"].startswith("ae_bundle_")]
        self.assertTrue(bundles)
        for b in bundles:
            self.assertEqual(b["adoption"],"optional")
            self.assertEqual(b["profile_activation"],"independent_request_evidence_only")
        ext=json.loads((ASSETS / "photo_prompt_acting_expression_extension.json").read_text())
        ref=ext["maintenance_ref"]
        record=json.loads((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (ref["record_id"]+".json")).read_text())
        self.assertEqual(ref["sha256"],semantics.digest(record))
        ids={r["id"] for rows in ext["slots"].values() for r in rows}
        self.assertFalse({"ae_microexpression","ae_voice","ae_explicit_terms","ae_methods"} & ids)


if __name__ == "__main__":
    unittest.main()
