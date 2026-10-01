"""Visible-variant routing, ambiguous-term boundaries and source-bound coverage."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
RESEARCH = ROOT / "docs/research-evidence/photo-prompt/clothing-terminology-20261001"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as pg
import photo_candidate_semantics as semantics
import validate_photo_prompt_dictionary as validation

MODULES = ("clothing_structure", "textile_surface", "accessory_structure", "traditional_clothing_detail")


class ClothingTerminologySemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_json(ASSETS / "photo_prompt_tags.json")
        cls.full_registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.full_registry["profiles"] if p["id"].startswith("clothing_ct")}
        cls.integration = json.loads((RESEARCH / "runtime-integration.json").read_text())
        # Exact routing can be checked against a small bounded profile cohort;
        # real generated indexes are checked separately below.
        cohort = {"clothing_ct001_v1", "clothing_ct030_v1", "clothing_ct030_v2", "clothing_ct044_v1",
                  "clothing_ct045_v2", "clothing_ct083_v2", "clothing_ct084_v2", "clothing_ct116_v1",
                  "clothing_ct122_v1", "clothing_ct122_v2", "clothing_ct135_v1", "clothing_ct137_v1",
                  "clothing_ct139_v1", "clothing_ct154_v1", "clothing_ct154_v2"}
        cls.registry = {**cls.full_registry, "profiles": [p for p in cls.profiles.values() if p["id"] in cohort]}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)

    def hard(self, text):
        result = pg.resolve_visual_profile_hits(
            self.registry, [{"source": "concept_lock", "text": text, "polarity": "required", "priority": "critical", "mandatory": True}],
            visual_profile_index=self.index, adult_context=True)
        return {h["profile_id"] for h in result["hits"] if h.get("hard_eligible")}

    def test_visible_variant_activates_in_english_and_korean_without_alternative(self):
        for p in self.registry["profiles"]:
            for phrase in p["activation"]["exact_terms"]:
                with self.subTest(profile=p["id"], phrase=phrase):
                    self.assertEqual(self.hard(phrase), {p["id"]})

    def test_homonyms_family_labels_negation_and_owner_changes_do_not_harden(self):
        for text in ["gore", "graphic gore", "a gore skirt", "bail", "베일", "a head veil",
                     "Oxford", "Oxford cloth", "Oxford University", "kimono sleeve", "kimono",
                     "jersey", "New Jersey", "cuff", "bracelet cuff", "stole", "a French tuck",
                     "raglan", "norigae", "한복", "herringbone", "princess seam",
                     "a pendant chain passing through a shirt buttonhole"]:
            with self.subTest(text=text):
                self.assertEqual(self.hard(text), set())
        for pid in ["clothing_ct044_v1", "clothing_ct116_v1", "clothing_ct139_v1", "clothing_ct154_v1"]:
            phrase = self.profiles[pid]["activation"]["exact_terms"][0]
            self.assertNotIn(pid, self.hard("not " + phrase))
        self.assertNotIn("clothing_ct154_v1", self.hard(self.profiles["clothing_ct154_v2"]["activation"]["exact_terms"][0]))

    def test_scope_has_no_body_geometry_or_provenance_only_promotion(self):
        held = {row["research_id"] for row in self.integration["backlog"] if row["variant"] == "all"}
        self.assertEqual(len(held), 10)
        self.assertEqual(self.integration["integrated_family_count"], 145)
        self.assertEqual(len(self.profiles), 287)
        self.assertEqual(sum(len(p["render_gates"]) for p in self.profiles.values()), 294)
        for module in MODULES:
            ext = json.loads((ASSETS / ("photo_prompt_" + module + "_extension.json")).read_text())
            for slot, rows in ext["slots"].items():
                for row in rows:
                    with self.subTest(slot=slot, candidate=row["id"]):
                        self.assertNotIn("body_geometry", row["affected_dimensions"])
                        self.assertTrue(row["affected_properties"])
                        self.assertTrue(row["relations"])
                        self.assertFalse(any(marker in row["en"] for marker in ["specified separately", "material metadata", "requested front number"]))
        self.assertNotIn("clothing_ct078_v1", self.profiles)
        self.assertNotIn("clothing_ct082_v1", self.profiles)
        self.assertNotIn("clothing_ct033_v1", self.profiles)

    def test_joint_bundles_are_optional_complete_and_scope_guarded(self):
        bundles = [b for b in self.data["candidate_bundles"] if b["id"].startswith("clothing_b_")]
        self.assertEqual(len(bundles), 30)
        for bundle in bundles:
            with self.subTest(bundle=bundle["id"]):
                self.assertEqual(bundle["profile_activation"], "independent_request_evidence_only")
                self.assertEqual(bundle["adoption"], "optional")
                slots = {}
                for member in bundle["member_candidates"]:
                    slots.setdefault(member["slot"], {"candidates": []})["candidates"].append({"id": member["id"], "applicability": {"status": "eligible"}})
                pack = {"slots": slots, "authorial_core": {"intent_lock": {"open_dimensions": ["appearance", "material"]}}}
                data = {**self.data, "candidate_bundles": [bundle]}
                self.assertEqual(len(semantics.public_bundles(data, pack)["candidates"]), 1)
                closed = copy.deepcopy(pack)
                closed["authorial_core"]["intent_lock"]["open_dimensions"] = []
                self.assertEqual(semantics.public_bundles(data, closed)["candidates"], [])
                next(iter(pack["slots"].values()))["candidates"].pop()
                self.assertEqual(semantics.public_bundles(data, pack)["candidates"], [])

    def test_authored_sources_and_generated_indexes_bind_every_registered_variant(self):
        semantic_index = pg.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
        pg.validate_semantic_index_metadata(semantic_index, self.data)
        visual_index = pg.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", self.full_registry)
        for module in MODULES:
            ext = json.loads((ASSETS / ("photo_prompt_" + module + "_extension.json")).read_text())
            ref = ext.pop("maintenance_ref")
            record = json.loads((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (ref["record_id"] + ".json")).read_text())
            self.assertEqual(ref["sha256"], semantics.digest(record))
            self.assertEqual(record["authored_source_sha256"], semantics.digest(ext))
            ids = {f"slot:{slot}:{row['id']}" for slot, rows in ext["slots"].items() for row in rows}
            self.assertTrue(ids <= set(semantic_index["entries"]))
        self.assertTrue(set(self.profiles) <= set(visual_index["entries"]))
        stale = copy.deepcopy(visual_index)
        stale["registry_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "registry_sha256"):
            pg.validate_visual_profile_index_metadata(stale, self.full_registry)

    def test_component_supported_embedding_discovery_is_optional(self):
        pid = "clothing_ct044_v1"
        registry = {**self.registry, "profiles": [self.profiles[pid]]}
        index = pg.build_visual_profile_index_payload(registry, vectors={pid: [1.0, 0.0]}, dimensions=2)
        phrase = self.profiles[pid]["authored_components"]["components"][0]["evidence_terms"][0]
        result = pg.resolve_visual_profile_hits(
            registry, [{"source": "authorial_core_interpretation", "text": phrase, "polarity": "advisory"}],
            visual_profile_index=index, query_text=phrase, query_vector=[1.0, 0.0], adult_context=True)
        hit = next(h for h in result["hits"] if h["profile_id"] == pid)
        self.assertFalse(hit["hard_eligible"])
        self.assertTrue(hit["optional_eligible"])
        unsupported = pg.resolve_visual_profile_hits(
            registry, [{"source": "authorial_core_interpretation", "text": "a plain round neck shirt", "polarity": "advisory"}],
            visual_profile_index=index, query_text="a plain round neck shirt", query_vector=[1.0, 0.0], adult_context=True)
        self.assertNotIn(pid, {h["profile_id"] for h in unsupported["hits"]})

    def test_registry_validator_accepts_scoped_discovery_and_rejects_unbounded_fields(self):
        errors = []
        validation.validate_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json", errors)
        self.assertEqual(errors, [])
        candidate = copy.deepcopy(self.profiles["clothing_ct044_v1"]["concept_candidate"])
        candidate.pop("affected_properties")
        with self.assertRaisesRegex(ValueError, "explicit property scope"):
            semantics.validate_candidate_entries({"slots": {"profile": [{**candidate, "id": "test",
                "concept_units": self.profiles["clothing_ct044_v1"]["semantics"]["visual_components"]}]}}, pg.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)


if __name__ == "__main__":
    unittest.main()
