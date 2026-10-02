from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as generator
import photo_candidate_semantics as semantics
from bm25f_retrieval import rank_bm25f


class PhotoY2KVisualSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = json.loads((ASSETS / "photo_prompt_y2k_extension.json").read_text())
        cls.data = generator.load_json(ASSETS / "photo_prompt_tags.json")
        cls.registry = generator.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {row["id"]: row for row in cls.registry["profiles"] if row["id"].startswith("y2kr_")}
        cls.routing_registry = {**cls.registry, "profiles": list(cls.profiles.values())}
        cls.routing_index = generator.build_visual_profile_index_payload(cls.routing_registry)
        cls.bundles = {row["id"]: row for row in cls.data["candidate_bundles"] if row["id"].startswith("y2kr_")}
        cls.candidates = {row["id"]: (slot, row) for slot, rows in cls.extension["slots"].items() for row in rows}

    def hard_matches(self, text, polarity="required"):
        result = generator.resolve_visual_profile_hits(
            self.routing_registry,
            [{"source": "concept_lock", "text": text, "polarity": polarity, "mandatory": True}],
            visual_profile_index=self.routing_index,
            adult_context=True,
        )
        return {row["profile_id"] for row in result["hits"] if row.get("hard_eligible")}

    def bundle_pack(self, bundle_id, open_dimensions):
        bundle = self.bundles[bundle_id]
        slots = {}
        for member in bundle["member_candidates"]:
            slots.setdefault(member["slot"], {"candidates": []})["candidates"].append(
                {"id": member["id"], "applicability": {"status": "eligible"}})
        return {"slots": slots, "authorial_core": {"intent_lock": {"open_dimensions": open_dimensions}}, "provenance": {"seed": 17}}

    def test_broad_and_ambiguous_labels_never_impose_specific_forms(self):
        for text in ("Y2K", "McBling", "Cyber Y2K", "Pop Y2K", "Sporty Y2K", "Gyaru",
                     "Heisei", "Acubi", "Frutiger Aero", "metallic", "butterfly", "gloss", "flip phone"):
            with self.subTest(text=text):
                self.assertEqual(self.hard_matches(text), set())

    def test_complete_forms_activate_and_excluded_forms_do_not(self):
        for profile_id in ("y2kr_spiky_bun", "y2kr_zigzag_part", "y2kr_low_rise", "y2kr_bootcut",
                           "y2kr_butterfly_clips", "y2kr_velour", "y2kr_terry", "y2kr_flip_phone"):
            with self.subTest(profile_id=profile_id):
                definition = self.profiles[profile_id]["semantics"]["definition"]
                self.assertIn(profile_id, self.hard_matches(definition))
                self.assertEqual(self.hard_matches(definition, "excluded"), set())
                self.assertNotIn(profile_id, self.hard_matches("avoid " + definition))

    def test_hinge_alone_does_not_require_screen_and_keys(self):
        profile = self.profiles["y2kr_flip_phone"]
        first = profile["authored_components"]["components"][0]["match_terms"][0]
        self.assertNotIn(profile["id"], self.hard_matches(first))
        self.assertEqual(len(profile["required_evidence_fields"]), 2)
        self.assertEqual(len(profile["render_gates"]), 2)

    def test_wrong_owner_and_surface_substitutes_are_separate_meanings(self):
        for text, rejected in (
            ("a butterfly print on a T-shirt", "y2kr_butterfly_clips"),
            ("the zigzag pattern is printed on trousers", "y2kr_zigzag_part"),
            (self.profiles["y2kr_terry"]["semantics"]["definition"], "y2kr_velour"),
            (self.profiles["y2kr_flare"]["semantics"]["definition"], "y2kr_bootcut"),
            ("a modern phone screen folds in the middle", "y2kr_flip_phone"),
        ):
            with self.subTest(text=text):
                self.assertNotIn(rejected, self.hard_matches(text))

    def test_garment_materials_do_not_weaken_nonhuman_material_slot(self):
        contract = {"subject_category": "human", "domains": ["fashion"], "adult_allowed": True}
        self.assertEqual(generator.slot_block_reason(self.data, "surface_material", contract), "subject_category_not_allowed")
        self.assertIsNone(generator.slot_block_reason(self.data, "garment_detail", contract))
        for candidate_id in ("y2kr_velour_garment", "y2kr_metallic_garment", "y2kr_pvc_garment"):
            slot, candidate = self.candidates[candidate_id]
            self.assertEqual(slot, "garment_detail")
            self.assertEqual(set(candidate["affected_dimensions"]), {"appearance", "material"})
            self.assertTrue(all("selected garment surface" in unit for unit in candidate["concept_units"]))

    def test_clothing_proportions_preserve_anatomy(self):
        for candidate_id in ("y2kr_tiny_big", "y2kr_long_torso", "y2kr_mini_boots", "y2kr_crop_low"):
            slot, candidate = self.candidates[candidate_id]
            self.assertEqual(slot, "garment_detail")
            self.assertEqual(candidate["affected_dimensions"], ["appearance"])
            self.assertNotIn("body_geometry", semantics.semantic_source(candidate, slot, self.data["candidate_semantic_policy"])["affected_dimensions"])

    def test_owner_specific_palette_cannot_mutate_ornaments_under_color_permission_only(self):
        candidate = self.candidates["y2kr_bling_palette"][1]
        self.assertEqual(set(candidate["affected_dimensions"]), {"appearance", "color", "material"})
        bid = "y2kr_bundle_palette_roles"
        self.assertEqual(semantics.public_bundles(self.data, self.bundle_pack(bid, ["color"]))["candidates"], [])
        self.assertEqual(len(semantics.public_bundles(self.data, self.bundle_pack(bid, ["appearance", "color", "material"]))["candidates"]), 1)

    def test_unknown_prop_scope_stays_ineligible_and_bound_device_scope_is_explicit(self):
        self.assertEqual(semantics.slot_dimensions("prop", self.data["candidate_semantic_policy"]), [])
        self.assertEqual(self.candidates["y2kr_cd_player"][1]["affected_dimensions"], [])
        for name in ("early_devices", "mid_devices"):
            bid = "y2kr_bundle_" + name
            pack = self.bundle_pack(bid, ["setting"])
            public = semantics.public_bundles(self.data, pack)["candidates"]
            self.assertEqual([row["id"] for row in public], ["bundle:" + bid])
            self.assertTrue(all("_tabletop" in row["entry_id"] for row in self.bundles[bid]["member_candidates"]))
            self.assertEqual(semantics.public_bundles(self.data, self.bundle_pack(bid, ["appearance"]))["candidates"], [])

    def test_bundle_requires_every_member_and_every_open_dimension(self):
        bid = "y2kr_bundle_velour_set"
        pack = self.bundle_pack(bid, ["appearance", "material"])
        self.assertEqual(len(semantics.public_bundles(self.data, pack)["candidates"]), 1)
        pack["authorial_core"]["intent_lock"]["open_dimensions"].remove("material")
        self.assertEqual(semantics.public_bundles(self.data, pack)["candidates"], [])
        missing = self.bundle_pack(bid, ["appearance", "material"])
        next(iter(missing["slots"].values()))["candidates"].pop()
        self.assertEqual(semantics.public_bundles(self.data, missing)["candidates"], [])

    def test_owner_gates_are_complete_and_maintenance_is_external(self):
        self.assertEqual(len(self.profiles), 306)
        self.assertEqual(len(self.candidates), 343)
        self.assertEqual(len(self.bundles), 20)
        gates = []
        for profile in self.profiles.values():
            required = profile["semantics"]["component_semantics"]["required_group_ids"]
            self.assertEqual(len(required), len(profile["render_gates"]))
            self.assertEqual(len(required), len(profile["required_evidence_fields"]))
            for gate in profile["render_gates"]:
                self.assertIn("Owner:", gate["description"])
                self.assertIn("Minimum view:", gate["description"])
                self.assertIn("Partial is fail", gate["description"])
                gates.append(gate["id"])
        self.assertEqual(len(gates), len(set(gates)))
        ref = self.extension["maintenance_ref"]
        record = json.loads((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (ref["record_id"] + ".json")).read_text())
        self.assertEqual(ref["sha256"], semantics.digest(record))
        self.assertTrue(record["maintenance_only"])
        for row in self.candidates.values():
            positive = row[1]["en"]
            self.assertNotIn("https://", positive)
            self.assertNotIn("S08", positive)
            self.assertNotIn("qualified", positive)

    def test_generated_indexes_include_every_new_contract_with_current_source_hashes(self):
        visual = generator.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", self.registry)
        self.assertLessEqual(set(self.profiles), set(visual["entries"]))
        index = generator.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
        generator.validate_semantic_index_metadata(index, self.data)
        expected = {f"slot:{slot}:{row['id']}" for slot, rows in self.extension["slots"].items() for row in rows}
        self.assertLessEqual(expected, set(index["entries"]))

    def test_generated_lexical_index_exposes_owner_and_modifier_candidates(self):
        index = generator.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
        generator.validate_semantic_index_metadata(index, self.data)
        bm25f = generator.semantic_bm25f_payload_from_index(index)
        # Exercise the actual generated documents, with near-neighbour forms
        # competing in the same dictionary rather than a Y2K-only toy index.
        for candidate_id in ("y2kr_spiky_bun", "y2kr_zigzag_part", "y2kr_butterfly_clips",
                             "y2kr_low_rise", "y2kr_bootcut", "y2kr_flare", "y2kr_cargo_mini",
                             "y2kr_velour_garment", "y2kr_terry_garment", "y2kr_metallic_garment",
                             "y2kr_pvc_garment", "y2kr_wraparound", "y2kr_shield",
                             "y2kr_flip_phone_tabletop", "y2kr_cd_player_tabletop"):
            with self.subTest(candidate_id=candidate_id):
                slot, candidate = self.candidates[candidate_id]
                query = " ".join([candidate["en"], *candidate["aliases"]])
                ranked = rank_bm25f(bm25f, {"active_request": query}, limit=16)
                self.assertIn(f"slot:{slot}:{candidate_id}", {row["document_id"] for row in ranked})


if __name__ == "__main__":
    unittest.main()
