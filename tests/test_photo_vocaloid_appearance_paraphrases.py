"""Observable-form enrichment must preserve duties, owners and optionality."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
EVIDENCE = ROOT / "docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_contracts as contracts
import prompt_generator as pg
from visual_profile_contracts import compile_visual_profile


class VocaloidAppearanceParaphraseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads((EVIDENCE / "INTEGRATION-LEDGER.json").read_text())
        cls.registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}
        cls.index = pg.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", cls.registry)
        cls.entries = {}
        for path in [ASSETS / "photo_prompt_tags.json", *ASSETS.glob("photo_prompt*extension*.json")]:
            for slot, rows in json.loads(path.read_text()).get("slots", {}).items():
                for entry in rows:
                    cls.entries[entry["id"]] = (slot, entry)

    def hard(self, profile_id, text, *, polarity="required", source="user_requirement"):
        thin = copy.deepcopy(self.registry)
        thin["profiles"] = [self.profiles[profile_id]]
        result = pg.resolve_visual_profile_hits(thin, [{"text": text, "source": source, "polarity": polarity}], adult_context=True)
        return any(h["profile_id"] == profile_id and h["hard_eligible"] for h in result["hits"])

    def test_equivalent_expansion_preserves_original_identity_and_every_duty(self):
        for row in self.ledger["existing_profiles"]:
            raw = json.loads((EVIDENCE / "baseline" / row["file"]).read_text())
            before = compile_visual_profile(next(p for p in raw["profiles"] if p["id"] == row["id"]))
            after = self.profiles[row["id"]]
            with self.subTest(profile=row["id"]):
                for key in ["activation", "composition_instruction", "required_evidence_fields", "render_gates", "reject_substitutes"]:
                    self.assertEqual(before.get(key), after.get(key), key)
                self.assertEqual(before["semantics"]["definition"], after["semantics"]["definition"])
                self.assertEqual(before["concept_candidate"].get("affected_dimensions"), after["concept_candidate"].get("affected_dimensions"))
                self.assertEqual(before["concept_candidate"].get("affected_properties"), after["concept_candidate"].get("affected_properties"))
                for field in before["required_evidence_fields"]:
                    self.assertEqual(before["evidence_requirements"][field]["min_content_words"], after["evidence_requirements"][field]["min_content_words"])
                    self.assertLessEqual(set(before["evidence_requirements"][field]["must_mention_any"]), set(after["evidence_requirements"][field]["must_mention_any"]))

    def test_new_relations_require_all_components_on_the_selected_carrier(self):
        for row in self.ledger["new_profiles"]:
            profile = self.profiles[row["id"]]
            groups = profile["semantics"]["component_semantics"]["groups"]
            for variant in [0, -1]:
                pieces = [g["any_terms"][variant] for g in groups]
                with self.subTest(profile=row["id"], variant=variant):
                    self.assertEqual(pg.candidate_pack_visual_component_match(profile, "; ".join(pieces)), "component_semantics")
                for missing in range(len(pieces)):
                    with self.subTest(profile=row["id"], missing=missing, variant=variant):
                        self.assertIsNone(pg.candidate_pack_visual_component_match(profile, "; ".join(s for i, s in enumerate(pieces) if i != missing)))

    def test_negation_and_agent_choices_cannot_promote_new_relations_to_hard(self):
        for row in self.ledger["new_profiles"]:
            profile_id = row["id"]
            phrase = self.profiles[profile_id]["activation"]["exact_terms"][0]
            with self.subTest(profile=profile_id):
                self.assertTrue(self.hard(profile_id, "The adult wearer with hair, skin, a top and a costume shows " + phrase))
                self.assertFalse(self.hard(profile_id, "The wearer has no " + phrase))
                self.assertFalse(self.hard(profile_id, phrase, polarity="excluded"))
                self.assertFalse(self.hard(profile_id, phrase, source="authorial_core_baseline", polarity="advisory"))

    def test_adjacent_owners_and_structures_are_not_complete_component_proof(self):
        cases = [
            ("sca_short_rear_long_sidelocks", "Her rear hair reaches the waist while two blunt side panels stop at the jaw."),
            ("accessory_earpiece_mouth_boom", "One person wears headphones while a different person holds a microphone beside their mouth."),
            ("sca_flat_equalizer_bars", "A separate monitor behind the wearer displays changing vertical audio bars; the skirt is plain."),
            ("sca_flat_keyboard_motif", "The musician's hands rest on a real keyboard instrument in front of a plain dress."),
            ("sca_flat_control_panel_motif", "Raised mechanical buttons and glass display boxes project from the jacket."),
            ("accessory_arm_circular_speaker_gear", "A circular loudspeaker stands on the floor beside the person's arm."),
            ("costume_external_membrane_wings", "A creature's anatomical wings grow directly from its body."),
            ("costume_external_thin_wing_plates", "Opaque feathered anatomical wings spread from a bird's shoulders."),
            ("accessory_cap_cross_glyph", "A cross is embroidered on the sleeve while the cap is plain."),
            ("sca_rigid_hair_tie_hardware", "A square symbol is printed on a loose lock without a gathered root."),
        ]
        for profile_id, text in cases:
            with self.subTest(profile=profile_id):
                self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[profile_id], text))
                self.assertFalse(self.hard(profile_id, text))

    def test_candidate_effects_cannot_bypass_parent_or_material_locks(self):
        pairs = [("vr_earpiece_mouth_boom", "wardrobe.accessories"), ("vr_flat_keyboard_motif", "wardrobe"), ("vr_rigid_hair_tie_hardware", "wardrobe.accessories"), ("vr_high_twin_tail_roots", "hair"), ("vr_external_thin_wing_plates", "wardrobe")]
        for candidate_id, property_path in pairs:
            _, entry = self.entries[candidate_id]
            lock = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [{"dimension": "appearance", "target": "main_subject", "property": property_path}]}
            with self.subTest(candidate=candidate_id):
                self.assertFalse(contracts.property_effects_allowed(lock, entry["affected_dimensions"], entry["affected_properties"]))
        wing = self.entries["vr_external_thin_wing_plates"][1]
        self.assertEqual(wing["affected_dimensions"], ["appearance"])
        self.assertTrue(all(effect["dimension"] == "appearance" for effect in wing["affected_properties"]))
        self.assertFalse(any(t in " ".join(wing["concept_units"]).lower() for t in ["transparent", "glowing", "light transmission"]))
        hidden = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [{"dimension": "appearance", "target": "main_subject", "property": "wardrobe.color"}]}
        self.assertFalse(contracts.property_effects_allowed(hidden, ["material"], [{"dimension": "material", "target": "main_subject", "property": "wardrobe.color"}]))

    def test_adult_and_source_boundaries_are_kept_out_of_positive_aliases(self):
        for profile_id in ["bm_stature_scale", "bm_head_body_ratio", "bm_torso_limb_ratio", "hourglass_silhouette_relation", "rectangle_silhouette_relation"]:
            with self.subTest(profile=profile_id):
                self.assertTrue(self.profiles[profile_id]["activation"]["requires_adult_character"])
        deferred = {x["card_id"] for x in self.ledger["card_dispositions"] if x["disposition"] == "bounded_or_deferred"}
        self.assertLessEqual({"K04", "K10", "K21", "K25", "K42", "K45", "K58", "K63", "K65", "K70", "K72"}, deferred)
        for row in self.ledger["new_profiles"]:
            _, entry = self.entries[row["candidate_id"]]
            public_text = " ".join([entry["en"], entry["ko"], entry["embedding_text"], *entry["paraphrases"]]).casefold()
            with self.subTest(candidate=entry["id"]):
                for term in ["http", "vocaloid", "nurse robot", "hatsune", "miku", "fukase", "yukari", "sapphire", "source_id"]:
                    self.assertNotIn(term, public_text)
                self.assertTrue(entry["affected_properties"])
                self.assertTrue(entry["concept_units"])
                self.assertTrue(entry["relations"])


if __name__ == "__main__":
    unittest.main()
