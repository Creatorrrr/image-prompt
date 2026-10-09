"""Summer constructions retain optional adoption, complete scope and pixel duties."""
import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
EVIDENCE = ROOT / "docs/research-evidence/photo-prompt/summer-fashion-integration-20261009"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as pg
import photo_candidate_semantics as cs
import audit_composed_prompt as auditor
from photo_contracts import property_effects_allowed
from tests import test_photo_authorial_core_v6 as v6


class SummerFashionSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_json(ASSETS / "photo_prompt_tags.json")
        cls.full_registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.full_registry["profiles"] if p["id"].startswith("suf_")}
        cls.registry = {**cls.full_registry, "profiles": list(cls.profiles.values())}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)
        cls.entries = {e["id"]: (s, e) for s, es in cls.data["slots"].items() for e in es if e["id"].startswith("suf_")}
        cls.mapping = json.loads((EVIDENCE / "draft-to-runtime.json").read_text())

    def hard(self, text, source="concept_lock", polarity="required"):
        result = pg.resolve_visual_profile_hits(self.registry,
            [{"source": source, "text": text, "polarity": polarity,
              "priority": "critical", "mandatory": polarity == "required"}],
            visual_profile_index=self.index, adult_context=True)
        return {r["profile_id"] for r in result["hits"] if r.get("hard_eligible")}

    @staticmethod
    def lock(path, dimension="appearance", target="main_subject"):
        return {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [
            {"dimension": dimension, "target": target, "property": path}]}

    def test_all_research_variants_have_one_reviewed_action(self):
        promoted = [r for r in self.mapping if "draft_id" in r]
        reused = [r for r in promoted if r["action"].startswith("reuse_")]
        self.assertEqual(len(promoted), 166)
        self.assertEqual(len({r["draft_id"] for r in promoted}), 166)
        self.assertEqual(len(reused), 7)
        self.assertEqual(len(self.entries), 159)
        self.assertEqual(len(self.profiles), 159)
        self.assertEqual({r["card_id"] for r in self.mapping if "draft_id" not in r},
                         {"SF047", "SF054", "SF056", "SF092"})

    def test_complete_requester_variant_activates_only_its_own_obligation(self):
        for pid, p in self.profiles.items():
            with self.subTest(profile=pid):
                self.assertEqual(self.hard(p["activation"]["exact_terms"][0]), {pid})

    def test_optional_names_homonyms_specifications_and_negation_never_harden(self):
        terms = ["baby tee", "tube top", "milkmaid", "monokini", "modern cutout monokini",
                 "high-waist", "high-leg", "racerback", "cross-back", "TENCEL", "LYCRA",
                 "UPF 50", "braless", "unlined", "jelly dessert", "political corruption",
                 "bubble tea", "a princess with darting eyes", "an ordinary adult portrait"]
        for text in terms:
            with self.subTest(text=text):
                self.assertEqual(self.hard(text), set())
        for pid, p in self.profiles.items():
            with self.subTest(profile=pid):
                self.assertNotIn(pid, self.hard("not " + p["activation"]["exact_terms"][0]))
                self.assertNotIn(pid, self.hard(p["activation"]["exact_terms"][0],
                                               "authorial_core_interpretation", "advisory"))

    def test_every_visual_component_compiles_into_an_ordinary_native_gate(self):
        for pid, p in self.profiles.items():
            components = p["authored_components"]["components"]
            with self.subTest(profile=pid):
                self.assertGreaterEqual(len(components), 2)
                self.assertEqual(p["required_evidence_fields"], [c["evidence_field"] for c in components])
                self.assertEqual(len(p["render_gates"]), len(components))
                self.assertEqual(p["semantics"]["component_semantics"]["minimum_component_groups"], len(components))
                self.assertTrue(all(g["review_scale"] == "native" for g in p["render_gates"]))
                parts = [c["evidence_terms"][0] for c in components]
                self.assertEqual(pg.candidate_pack_visual_component_match(p, "; ".join(parts)), "component_semantics")
                self.assertEqual(self.hard(parts[0]), set())

    def test_material_length_and_topology_locks_cannot_be_bypassed_by_new_names(self):
        cases = [
            ("suf_sf013_v1_candidate", "wardrobe.surface.sheer_opacity", "appearance"),
            ("suf_sf013_v1_candidate", "wardrobe.material.transmission", "material"),
            ("suf_sf002_v1_candidate", "wardrobe.top.hem_relative_to_waist", "appearance"),
            ("suf_sf083_v1_candidate", "wardrobe.fit.waistband_landmark", "appearance"),
            ("suf_sf083_v1_candidate", "wardrobe.coverage.leg_opening", "appearance"),
            ("suf_sf114_v1_candidate", "footwear.material.transmission", "material"),
            ("suf_sf118_v2_candidate", "accessories.chain_connection", "appearance"),
            ("suf_sf116_v2_candidate", "hair.visibility", "appearance"),
        ]
        for cid, prop, dimension in cases:
            slot, e = self.entries[cid]
            source = cs.semantic_source(e, slot, self.data["candidate_semantic_policy"])
            with self.subTest(candidate=cid, prop=prop):
                self.assertFalse(property_effects_allowed(self.lock(prop, dimension), source["affected_dimensions"], source["affected_properties"]))
                self.assertTrue(property_effects_allowed(self.lock(prop, dimension, "secondary_subject"), source["affected_dimensions"], source["affected_properties"]))

    def test_color_carriers_respect_color_locks_in_both_dimensions(self):
        for cid in ["suf_sf030_v2_candidate", "suf_sf104_v1_candidate", "suf_sf106_v2_candidate", "suf_sf109_v2_candidate"]:
            slot, e = self.entries[cid]
            self.assertIn("color", e["affected_dimensions"])
            for dimension in ["appearance", "color"]:
                with self.subTest(candidate=cid, dimension=dimension):
                    self.assertFalse(property_effects_allowed(self.lock("wardrobe.color", dimension), e["affected_dimensions"], e["affected_properties"]))

    def test_independent_coverage_and_optical_alternatives_are_not_combined(self):
        _, high = self.entries["suf_sf083_v1_candidate"]
        properties = {r["property"] for r in high["affected_properties"]}
        self.assertIn("wardrobe.fit.waistband_landmark", properties)
        self.assertIn("wardrobe.coverage.leg_opening", properties)
        _, opaque = self.entries["suf_sf114_v3_candidate"]
        _, mesh = self.entries["suf_sf114_v2_candidate"]
        self.assertIn("opaque", opaque["en"])
        self.assertNotIn("translucent", opaque["en"])
        self.assertIn("net openings", mesh["en"])
        _, illusion = self.entries["suf_sf030_v2_candidate"]
        self.assertIn("seam and folded fabric edge", illusion["en"])
        self.assertNotIn("bare skin", illusion["en"])
        _, modern = self.entries["suf_sf081_v1_candidate"]
        self.assertNotIn("topless", modern["en"])
        self.assertEqual(len(modern["relations"]), 1)
        self.assertEqual(modern["relations"][0], {
            "id": "suf_sf081_v1_owner_relation", "type": "connects",
            "subject": "the narrow torso panel", "object": "the upper and lower swimsuit sections"})

    def test_bundles_remain_optional_with_explicit_owner_and_no_hidden_claims(self):
        bundles = [b for b in self.data["candidate_bundles"] if b["id"].startswith("suf_")]
        self.assertEqual(len(bundles), 159)
        for b in bundles:
            with self.subTest(bundle=b["id"]):
                self.assertEqual(b["adoption"], "optional")
                self.assertEqual(b["profile_activation"], "independent_request_evidence_only")
                self.assertEqual(len(b["associated_profile_ids"]), 1)
                self.assertEqual(len(b["member_candidates"]), 1)
                self.assertTrue(b["relations"][0]["subject"])
                self.assertTrue(b["relations"][0]["object"])
                self.assertNotIn("_or_", b["relations"][0]["type"])
        for cid, (_, e) in self.entries.items():
            with self.subTest(candidate=cid):
                self.assertNotIn("identity", e["affected_dimensions"])
                self.assertNotIn("body_geometry", e["affected_dimensions"])
                self.assertTrue(all(r["target"] == "main_subject" for r in e["affected_properties"]))
                self.assertNotIn("http", json.dumps(e).lower())
                self.assertNotIn("<bound_garment_id>", json.dumps(e))

    def test_selected_new_bundle_requires_every_component_and_relation(self):
        for bundle_id in ["suf_sf013_v1_bundle", "suf_sf081_v1_bundle", "suf_sf114_v2_bundle"]:
            bundle_source = next(b for b in self.data["candidate_bundles"] if b["id"] == bundle_id)
            raw_core = v6.core()
            raw_core["intent_lock"]["open_dimensions"].extend(["appearance", "material"])
            core = pg.normalize_authorial_core(raw_core, request_envelope=pg.normalize_request_envelope(v6.envelope()))
            slots = {}
            for member in bundle_source["member_candidates"]:
                entry = pg.candidate_pack_slot_entry_by_id(self.data, member["slot"], member["entry_id"])
                candidate, _ = pg.candidate_pack_summarize_slot_candidate(self.data, member["slot"],
                    {"id": member["entry_id"], "applicability_status": "eligible"})
                candidate["_v6_semantic_source"] = cs.semantic_source(entry, member["slot"], self.data["candidate_semantic_policy"])
                slots.setdefault(member["slot"], {"slot": member["slot"], "candidates": []})["candidates"].append(candidate)
            source = {"contract_version": "photo-candidate-pack/v6", "authorial_core": core,
                      "slots": slots, "provenance": {"seed": 20261009}}
            source["candidate_bundles"] = cs.public_bundles(self.data, source)
            pack = pg.candidate_pack_project(source, "v6")
            bundle = next(b for b in pack["candidate_bundles"]["candidates"] if b["id"] == "bundle:" + bundle_id)
            parts = {c["id"]: c["concept_units"][0] for c in bundle["components"]}
            relation = bundle["relations"][0]
            relation_phrase = f"{relation['subject']} {relation['type'].replace('_', ' ')} {relation['object']}"
            phrase = "; ".join([*parts.values(), relation_phrase])
            row = {"candidate_id": bundle["id"], "component_evidence": parts,
                   "relation_evidence": {relation["id"]: relation_phrase}}
            def check(item):
                return auditor.audit_candidate_semantic_contracts(pack, phrase, {bundle["id"]},
                    auditor.candidate_objects_from_pack(pack), [item])
            with self.subTest(bundle=bundle_id):
                self.assertFalse(check(row))
                for mutation in ["missing_component", "missing_relation", "nonliteral_relation"]:
                    altered = copy.deepcopy(row)
                    if mutation == "missing_component":
                        altered["component_evidence"].pop(next(iter(parts)))
                    elif mutation == "missing_relation":
                        altered["relation_evidence"].clear()
                    else:
                        altered["relation_evidence"][relation["id"]] = "An absent relation on another garment."
                    self.assertTrue(check(altered), mutation)

    def test_external_maintenance_references_authenticate_the_exact_sources(self):
        for path in ASSETS.glob("photo_prompt_summer_*_extension.json"):
            ext = json.loads(path.read_text())
            ref = ext.pop("maintenance_ref")
            rec = json.loads((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (ref["record_id"] + ".json")).read_text())
            with self.subTest(source=path.name):
                self.assertEqual(ref["sha256"], cs.digest(rec))
                self.assertEqual(rec["authored_source_sha256"], cs.digest(ext))

    def test_real_indexes_are_current_and_reject_source_drift(self):
        semantic = pg.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
        pg.validate_semantic_index_metadata(semantic, self.data)
        visual = pg.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", self.full_registry)
        self.assertTrue(set(self.profiles) <= set(visual["entries"]))
        self.assertTrue({f"slot:{s}:{cid}" for cid, (s, _) in self.entries.items()} <= set(semantic["entries"]))
        stale = copy.deepcopy(visual)
        stale["registry_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "registry_sha256"):
            pg.validate_visual_profile_index_metadata(stale, self.full_registry)


if __name__ == "__main__":
    unittest.main()
