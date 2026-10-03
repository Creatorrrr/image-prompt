"""Owner relations, narrow authority, optional bundles and generated-index integrity.

These are inspectable contract tests, not independent visual-quality holdouts.
"""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
EVIDENCE = ROOT / "docs/research-evidence/photo-prompt/portrait-fashion-exposure-20260928"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
import photo_candidate_semantics as cs
from visual_profile_contracts import compile_visual_profile


class PortraitFashionExposureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ext = json.loads((SKILL / "assets/photo_prompt_portrait_fashion_exposure_extension.json").read_text())
        cls.all_registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
        cls.registry = {**cls.all_registry, "profiles": [p for p in cls.all_registry["profiles"] if p["id"].startswith("pfe_")]}
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}
        cls.index = pg.build_visual_profile_index_payload(cls.registry)
        cls.data = pg.load_json(SKILL / "assets/photo_prompt_tags.json")

    def hard(self, text, adult=True):
        r = pg.resolve_visual_profile_hits(self.registry, [{"source": "concept_lock", "text": text,
            "polarity": "required", "priority": "critical", "mandatory": True}],
            visual_profile_index=self.index, adult_context=adult)
        return {h["profile_id"] for h in r["hits"] if h.get("hard_eligible")}

    def test_complete_relation_has_authority_but_fragments_negation_and_nonadult_do_not(self):
        for p in self.profiles.values():
            phrase = p["activation"]["exact_terms"][0]
            with self.subTest(profile=p["id"]):
                self.assertEqual(self.hard(phrase), {p["id"]})
                self.assertEqual(self.hard("not " + phrase), set())
                self.assertEqual(self.hard(phrase, adult=False), set())
                for c in p["authored_components"]["components"]:
                    self.assertEqual(self.hard(c["evidence_terms"][0]), set())

    def test_broad_labels_and_adjacent_substitutes_do_not_create_hard_geometry(self):
        cases = ["가슴골", "cleavage", "large bust", "deep V-neck", "데콜타주", "판치라", "panchira", "パンチラ",
                 "브라치라", "brachira", "thirst trap", "boudoir", "sexy", "Vamp Romantic", "홀터넥",
                 "one-shoulder", "body-skimming", "side slit", "슬릿 스캔 촬영", "mineral cleavage",
                 "lace print", "safety shorts under a skirt", "petticoat hem", "a bra strap above a T-shirt",
                 "a thong waistband above low-rise trousers", "garment underarm seam", "bodycon dress",
                 "시스루뱅", "가슴골 없이 쇄골만 보이는 의상", "판치라가 아닌 속치마 밑단"]
        for q in cases:
            with self.subTest(query=q):
                self.assertEqual(self.hard(q), set())

    def test_embedding_discovery_is_advisory_even_for_a_required_query(self):
        for target in ["pfe_cleavage", "pfe_hem_foundation", "pfe_back_face"]:
            vectors = {p["id"]: [1.0, 0.0] if p["id"] == target else [0.0, 1.0] for p in self.registry["profiles"]}
            index = pg.build_visual_profile_index_payload(self.registry, vectors=vectors, dimensions=2)
            r = pg.resolve_visual_profile_hits(self.registry, [{"source": "concept_lock", "text": "adult fashion details",
                "polarity": "required", "mandatory": True}], visual_profile_index=index,
                query_text="an independently worded adult garment boundary", query_vector=[1.0, 0.0], adult_context=True)
            h = next(h for h in r["hits"] if h["profile_id"] == target)
            self.assertFalse(h["hard_eligible"])
            self.assertTrue(h["optional_eligible"])
            self.assertIn(h["match_basis"], {"embedding", "hybrid"})

    def test_each_selected_profile_retains_every_component_and_gate(self):
        for p in self.profiles.values():
            with self.subTest(profile=p["id"]):
                c = compile_visual_profile(p)
                self.assertEqual(len(c["required_evidence_fields"]), 3)
                self.assertEqual(len(c["render_gates"]), 3)
                malformed = copy.deepcopy(p)
                malformed["authored_components"]["components"][1]["evidence_field"] = "component_1_phrase"
                with self.assertRaises(ValueError):
                    compile_visual_profile(malformed)

    def test_unrelated_homonyms_are_filtered_even_with_an_adult_context(self):
        cases = {"mineral cleavage": "pfe_cleavage", "horse halter": "pfe_halter", "slit-scan photography": "pfe_slit", "navel orange": "pfe_navel"}
        for query, target in cases.items():
            with self.subTest(query=query):
                vectors = {p["id"]: [1.0, 0.0] if p["id"] == target else [0.0, 1.0] for p in self.registry["profiles"]}
                index = pg.build_visual_profile_index_payload(self.registry, vectors=vectors, dimensions=2)
                # Source records carry the authorial context; query_text only
                # supplies ranking text and is not a context authority.
                resolved = pg.resolve_visual_profile_hits(self.registry,
                    [{"source": "authorial_core_interpretation", "text": query, "polarity": "advisory"}],
                    visual_profile_index=index, query_text=query, query_vector=[1.0, 0.0], adult_context=True)
                hits = [h for h in resolved["hits"] if h["profile_id"] == target]
                self.assertFalse(any(h.get("hard_eligible") or h.get("optional_eligible") for h in hits))

    def test_candidate_eligibility_requires_an_adult_human_context(self):
        for slot, entries in self.ext["slots"].items():
            for e in entries:
                with self.subTest(candidate=e["id"]):
                    self.assertTrue(pg.compatible_with_slot_context(slot, e, {"subject": {"id": "adult", "tags": ["human", "adult", "fashion"]}}, self.data))
                    self.assertFalse(pg.compatible_with_slot_context(slot, e, {"subject": {"id": "child", "tags": ["human", "child", "fashion"]}}, self.data))
                    self.assertFalse(pg.compatible_with_slot_context(slot, e, {"subject": {"id": "statue", "tags": ["sculpture", "fashion"]}}, self.data))

    def test_bundles_are_joint_optional_and_respect_all_locked_dimensions(self):
        bundles = [b for b in self.data["candidate_bundles"] if b["id"].startswith("pfe_")]
        self.assertEqual(len(bundles), 14)
        for b in bundles:
            with self.subTest(bundle=b["id"]):
                self.assertEqual(b["adoption"], "optional")
                self.assertEqual(b["profile_activation"], "independent_request_evidence_only")
                slots, dims = {}, set()
                for m in b["member_candidates"]:
                    dims.update(m["affected_dimensions"])
                    slots.setdefault(m["slot"], {"candidates": []})["candidates"].append({"id": m["id"], "applicability": {"status": "eligible"}})
                pack = {"slots": slots, "authorial_core": {"intent_lock": {"open_dimensions": list(dims)}}}
                data = {**self.data, "candidate_bundles": [b]}
                self.assertEqual(len(cs.public_bundles(data, pack)["candidates"]), 1)
                for d in dims:
                    locked = copy.deepcopy(pack)
                    locked["authorial_core"]["intent_lock"]["open_dimensions"].remove(d)
                    self.assertEqual(cs.public_bundles(data, locked)["candidates"], [])
                missing = copy.deepcopy(pack)
                next(iter(missing["slots"].values()))["candidates"].clear()
                self.assertEqual(cs.public_bundles(data, missing)["candidates"], [])

    def test_research_sources_and_proposals_do_not_leak_into_runtime(self):
        record = json.loads((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_portrait_fashion_exposure_extension.json").read_text())
        self.assertEqual(cs.digest(record), self.ext["maintenance_ref"]["sha256"])
        authored = copy.deepcopy(self.ext)
        authored.pop("maintenance_ref")
        self.assertEqual(cs.digest(authored), record["authored_source_sha256"])
        self.assertNotIn("https://", json.dumps(authored))
        self.assertNotIn("source_ids", json.dumps(authored))
        for rows in self.ext["slots"].values():
            for e in rows:
                self.assertNotIn("identity", e["affected_dimensions"])
                self.assertNotIn("sexual_tone", e["affected_dimensions"])

    def test_real_generated_indexes_bind_sources_and_every_candidate(self):
        si = pg.load_semantic_index_payload(SKILL / "assets/photo_prompt_semantic_index.json")
        pg.validate_semantic_index_metadata(si, self.data)
        expected = {f"slot:{slot}:{e['id']}" for slot, rows in self.ext["slots"].items() for e in rows}
        self.assertTrue(expected <= set(si["entries"]))
        vi = json.loads((SKILL / "assets/photo_prompt_visual_profile_index.json").read_text())
        pg.validate_visual_profile_index_metadata(vi, self.all_registry)
        self.assertTrue(set(self.profiles) <= set(vi["entries"]))
        self.assertTrue(all(len(vi["entries"][ident]["vector"]) == 768 for ident in self.profiles))

    def test_appended_labels_do_not_imply_exposure_fit_anatomy_or_viewpoint(self):
        for query in ["sideboob", "underboob", "배꼽 노출", "bodycon", "second-skin fit", "fine mesh",
                      "illusion neckline", "sheer tights", "opaque tights", "wet-look finish", "back-seam stockings",
                      "garter belt", "절대영역", "絶対領域", "VPL", "치골", "장골능", "S-curve pose",
                      "high angle", "low angle", "micro-mini", "low-rise waist"]:
            with self.subTest(query=query):
                self.assertEqual(self.hard(query), set())

    def test_thigh_skin_band_does_not_change_the_existing_negative_space_profile(self):
        old = next(p for p in self.all_registry["profiles"] if p["id"] == "inner_thigh_negative_space")
        original = json.loads((EVIDENCE / "revisions/initial/photo_prompt_visual_profile_index.json").read_text())
        current = json.loads((SKILL / "assets/photo_prompt_visual_profile_index.json").read_text())
        # Reconstruct only the explicitly recorded later alternatives. The
        # frozen initial text stays exact; a new text needs a new vector.
        receipt = json.loads((ROOT / "docs/research-evidence/photo-prompt/neutral-expression-integration-20261003/DATA-CHANGE-RECEIPT.json").read_text())
        additions = next(p["added_paraphrases"] for f in receipt["existing_profile_updates"] for p in f["profiles"] if p["id"] == old["id"])
        historical = copy.deepcopy(old)
        historical["semantics"]["paraphrase_examples"] = [p for p in historical["semantics"]["paraphrase_examples"] if p not in additions]
        self.assertEqual(pg.visual_profile_semantic_text(historical), original["entries"][old["id"]]["text"])
        self.assertEqual(current["entries"][old["id"]]["text"], pg.visual_profile_semantic_text(old))
        self.assertEqual(len(current["entries"][old["id"]]["vector"]), 768)
        self.assertIn("절대공역", old["activation"]["project_glossary_aliases"])
        self.assertNotIn("절대영역", old["activation"]["project_glossary_aliases"])
        new = self.profiles["pfe_thigh_skin_band"]
        self.assertIn("절대영역", new["concept_candidate"]["concept_terms"])
        self.assertEqual(self.hard(new["activation"]["exact_terms"][0]), {new["id"]})
        self.assertEqual(self.hard("background space between the inner thighs"), set())

    def test_added_projection_preserves_initial_profiles_candidates_and_source_links(self):
        initial_profiles = json.loads((EVIDENCE / "revisions/initial/photo_prompt_visual_obligations_portrait_fashion_exposure.json").read_text())["profiles"]
        # Compare authored bytes with authored bytes; the runtime loader adds
        # compiled component and claim-policy fields to profile dictionaries.
        current_authored = {p["id"]: p for p in json.loads((SKILL / "assets/photo_prompt_visual_obligations_portrait_fashion_exposure.json").read_text())["profiles"]}
        self.assertEqual(len(initial_profiles), 14)
        for p in initial_profiles:
            comparable = copy.deepcopy(current_authored[p["id"]])
            # These three reviewed profiles now have append-only contextual
            # examples and scope notes. All initial values and every other
            # field, including activation, components and gates, stay frozen.
            if p["id"] in {"pfe_cowl", "pfe_one_shoulder", "pfe_ruching"}:
                for field in ("paraphrase_examples", "contrast_examples", "claim_limits"):
                    original = p["semantics"].get(field, [])
                    current = comparable["semantics"].get(field, [])
                    self.assertEqual(current[:len(original)], original)
                    if field in p["semantics"]:
                        comparable["semantics"][field] = original
                    else:
                        comparable["semantics"].pop(field, None)
            if p["id"] == "pfe_cleavage":
                original = p["semantics"]["paraphrase_examples"]
                current = comparable["semantics"]["paraphrase_examples"]
                self.assertEqual(current[:len(original)], original)
                receipt = json.loads((ROOT / "docs/research-evidence/photo-prompt/neutral-expression-integration-20261003/DATA-CHANGE-RECEIPT.json").read_text())
                additions = next(row["added_paraphrases"] for f in receipt["existing_profile_updates"] for row in f["profiles"] if row["id"] == p["id"])
                self.assertEqual(current[len(original):], additions)
                comparable["semantics"]["paraphrase_examples"] = original
            self.assertEqual(p, comparable)
        initial = json.loads((EVIDENCE / "revisions/initial/photo_prompt_portrait_fashion_exposure_extension.json").read_text())
        for slot, rows in initial["slots"].items():
            actual = {r["id"]: r for r in self.ext["slots"][slot]}
            for row in rows:
                self.assertEqual(actual[row["id"]], row)
        sources = {s["id"] for s in json.loads((EVIDENCE / "sources.json").read_text())["sources"]}
        proposals = json.loads((EVIDENCE / "proposals.json").read_text())["proposals"]
        self.assertTrue(all(set(p["source_ids"]) <= sources for p in proposals))
        self.assertEqual(len(proposals), 40)


if __name__ == "__main__":
    unittest.main()
