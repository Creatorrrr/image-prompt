"""Regional morphology must retain ownership, context and opt-in boundaries."""
from __future__ import annotations

import json
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))

import photo_candidate_semantics as candidate_semantics
import photo_contracts as contracts
import prompt_generator as pg


class PhotoBodyMorphologySemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assets = SKILL / "assets"
        cls.registry = pg.load_visual_obligation_registry(assets / "photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}
        cls.index = pg.load_visual_profile_index(assets / "photo_prompt_visual_profile_index.json", cls.registry)
        cls.data = pg.load_json(assets / "photo_prompt_tags.json")
        cls.entries = {e["id"]: (slot, e) for slot, rows in cls.data["slots"].items() for e in rows}

    def resolve(self, text, *, core_text="", adult=True, excluded=False):
        rows = [{"source": "user_requirement", "text": text,
                 "polarity": "excluded" if excluded else "required"}]
        if core_text:
            rows.append({"source": "authorial_core_interpretation", "text": core_text, "polarity": "advisory"})
        return pg.resolve_visual_profile_hits(self.registry, rows, visual_profile_index=self.index,
                                              adult_context=adult)

    @staticmethod
    def hard_ids(resolution):
        return {r["profile_id"] for r in resolution["hits"] if r["hard_eligible"]}

    def test_local_exact_terms_do_not_replace_global_owners(self):
        cases = {
            "adult bilateral shoulder width relation": "bm_shoulder_width",
            "adult neck-to-shoulder slope relation": "bm_shoulder_slope",
            "adult regional muscle bulk": "bm_muscle_volume",
            "adult bilateral hip width relation": "bm_hip_width",
            "adult localized lateral hip indentation": "bm_hip_dip_local",
            "adult finger-to-palm proportion relation": "bm_finger_proportion",
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(self.hard_ids(self.resolve(text)), {expected})
        self.assertEqual(self.hard_ids(self.resolve("adult hip dip side view")),
                         {"lateral_waist_hip_contour_transition"})
        self.assertEqual(self.hard_ids(self.resolve("성인 여성 글래머 체형")), {"curvilinear_figure_relation"})

    def test_non_body_words_exclusion_and_adult_scope_fail_closed(self):
        for text in ("a shoulder bag on a table", "a branching river in a map",
                     "a stocky typeface", "a long finger of land", "a painted vein pattern"):
            with self.subTest(text=text):
                self.assertFalse(self.hard_ids(self.resolve(text)))
        self.assertFalse(self.hard_ids(self.resolve("adult bilateral shoulder width relation", excluded=True)))
        self.assertFalse(self.hard_ids(self.resolve("no bilateral shoulder width relation")))
        resolution = self.resolve("bilateral shoulder width relation", adult=False)
        self.assertFalse(self.hard_ids(resolution))
        hit = next(r for r in resolution["hits"] if r["profile_id"] == "bm_shoulder_width")
        self.assertEqual(hit["applicability_status"], "requires_existing_adult_context")

    def test_neutral_anatomical_topology_needs_actual_anatomical_context(self):
        profile = self.profiles["bm_perineal_location"]
        term = profile["activation"]["exact_terms"][0]
        ordinary = self.resolve(term, core_text="an adult in an unrelated ordinary portrait")
        self.assertNotIn(profile["id"], self.hard_ids(ordinary))
        anatomical = self.resolve(term, core_text="a neutral adult anatomical diagram")
        self.assertIn(profile["id"], self.hard_ids(anatomical))

    def test_complete_component_proof_is_required_for_semantic_discovery(self):
        profile = self.profiles["bm_shoulder_width"]
        units = profile["semantics"]["visual_components"]
        owner = profile["semantics"]["component_semantics"]["groups"][-1]["any_terms"][0]
        complete = "; ".join([*units, owner])
        self.assertIsNotNone(pg.candidate_pack_visual_component_match(profile, complete))
        for missing in range(len(units)):
            with self.subTest(missing=missing):
                partial = "; ".join([u for i, u in enumerate(units) if i != missing] + [owner])
                self.assertIsNone(pg.candidate_pack_visual_component_match(profile, partial))
        self.assertIsNone(pg.candidate_pack_visual_component_match(profile, "; ".join(units)))

    def test_embedding_discovery_cannot_promote_body_geometry_to_hard(self):
        profile = self.profiles["bm_shoulder_width"]
        small_registry = dict(self.registry, profiles=[profile])
        index = pg.build_visual_profile_index_payload(small_registry,
            vectors={profile["id"]: [1.0, 0.0]}, dimensions=2)
        text = "; ".join(g["any_terms"][0] for g in profile["semantics"]["component_semantics"]["groups"])
        resolution = pg.resolve_visual_profile_hits(small_registry,
            [{"source": "authorial_core_interpretation", "text": text, "polarity": "advisory"}],
            visual_profile_index=index, query_vector=[1.0, 0.0], adult_context=True)
        hit = next(r for r in resolution["hits"] if r["profile_id"] == profile["id"])
        self.assertEqual(hit["match_basis"], "embedding")
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])

    def test_coupled_contact_and_stance_obey_property_locks(self):
        for entry_id, required in {
            "bm_compression_contour": {"appearance", "body_geometry"},
            "bm_thigh_gap": {"body_geometry", "pose"},
            "bm_pose_surface_change": {"pose", "body_geometry", "appearance"},
            "bm_nail_shape": {"body_geometry"},
        }.items():
            with self.subTest(entry=entry_id):
                slot, entry = self.entries[entry_id]
                semantic = candidate_semantics.semantic_source(entry, slot, self.data["candidate_semantic_policy"])
                self.assertEqual(set(semantic["affected_dimensions"]), required)
                effects = semantic["affected_properties"]
                locked = dict(effects[0])
                intent = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [locked]}
                self.assertFalse(contracts.property_effects_allowed(intent, required, effects))
                # The same property cannot bypass a lock through another carrier dimension.
                alternate = dict(locked, dimension="material")
                self.assertFalse(contracts.property_effects_allowed(intent, ["material"], [alternate]))
                unrelated = dict(locked, property="wardrobe.color")
                self.assertTrue(contracts.property_effects_allowed(
                    {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [unrelated]}, required, effects))

    def test_render_gate_ownership_is_not_replaced_by_neighboring_surface(self):
        extension = json.loads((SKILL / "assets" / "photo_prompt_visual_obligations_body_morphology.json").read_text())
        for source in extension["profiles"]:
            profile = self.profiles[source["id"]]  # Evidence and gates are generated from this source.
            with self.subTest(profile=profile["id"]):
                self.assertIn("owner_state_phrase", profile["required_evidence_fields"])
                self.assertIn("wrong_owner_or_body_region", profile["reject_substitutes"])
                self.assertIn("occluded_required_component", profile["reject_substitutes"])
                self.assertEqual(len(profile["render_gates"]), len(profile["required_evidence_fields"]))
                self.assertIs(profile["activation"]["requires_adult_character"], True)
                self.assertIs(profile["activation"]["semantic_discovery_requires_component_evidence"], True)

    def test_frozen_visual_priorities_can_find_options_without_inventing_assertions(self):
        entries = {
            "slot:prop:handle": {"id": "handle", "en": "blue porcelain cup with a curved handle",
                "concept_units": ["blue porcelain cup", "curved handle"],
                "core_assertion_discovery": True, "affected_dimensions": ["material"],
                "affected_properties": [{"dimension": "material", "target": "cup", "property": "surface.material"}]},
            "slot:prop:blocked": {"id": "blocked", "en": "blue porcelain cup with a curved handle",
                "concept_units": ["blue porcelain cup"], "affected_dimensions": ["material"]},
        }
        documents = {key: pg.semantic_bm25f_fields_for_entry(e, "prop", kind="slot") for key,e in entries.items()}
        index = pg.build_bm25f_index(documents, policy=pg.SEMANTIC_BM25F_POLICY)
        data = {"candidate_semantic_policy": {"core_assertion_discovery": {
            "maximum_candidates": 15, "maximum_per_assertion": 3, "minimum_shared_content_words": 3}}}
        core = {"visual_priorities": ["blue porcelain cup"], "semantic_assertions": [],
                "user_exclusions": [], "intent_lock": {"contract_version": "photo-intent-lock/v2",
                    "open_dimensions": ["material"], "semantic_anchors": []}}
        before = copy.deepcopy(core)
        found = pg.candidate_pack_assertion_discovery(data, core, entries, index, include_visual_priorities=True)
        self.assertEqual(found, ["slot:prop:handle"])
        self.assertEqual(core, before)
        self.assertEqual(pg.candidate_pack_assertion_discovery(data, core, entries, index), [])
        for altered in (dict(core, user_exclusions=["blue porcelain cup"]),
                        dict(core, intent_lock={**core["intent_lock"], "open_dimensions": []}),
                        dict(core, intent_lock={**core["intent_lock"], "semantic_anchors": [
                            {"dimension": "material", "target": "cup", "property": "surface.material"}]})):
            with self.subTest(altered=altered):
                self.assertEqual(pg.candidate_pack_assertion_discovery(
                    data, altered, entries, index, include_visual_priorities=True), [])

    def test_piloerection_is_not_a_metaphorical_reaction_or_plain_pore_texture(self):
        self.assertEqual(self.hard_ids(self.resolve("visible goosebumps on adult skin")), {"bm_skin_piloerection"})
        self.assertNotIn("bm_skin_piloerection", self.hard_ids(self.resolve("that photograph gives me goosebumps")))
        profile = self.profiles["bm_skin_piloerection"]
        self.assertIsNone(pg.candidate_pack_visual_component_match(profile, "adult skin pores with fine surface relief"))


if __name__ == "__main__":
    unittest.main()
