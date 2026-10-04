"""Uniform equivalents keep component, wearer and optionality boundaries."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
ASSETS = SKILL / "assets"
EVIDENCE = ROOT / "docs/research-evidence/photo-prompt/uniform-costume-integration-20261004"
sys.path.insert(0, str(SKILL / "scripts"))
import photo_contracts as contracts
import prompt_generator as pg
from visual_profile_contracts import compile_visual_profile


class UniformCostumeParaphraseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ledger = json.loads((EVIDENCE / "INTEGRATION-LEDGER.json").read_text())
        cls.registry = pg.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}
        cls.index = pg.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", cls.registry)
        cls.data = pg.load_runtime_data(ASSETS / "photo_prompt_tags.json")
        cls.entries = {}
        for path in [ASSETS / "photo_prompt_tags.json", *ASSETS.glob("photo_prompt*extension*.json")]:
            for slot, rows in json.loads(path.read_text()).get("slots", {}).items():
                for entry in rows:
                    cls.entries[entry["id"]] = (slot, entry)
        cls.thin_registry = copy.deepcopy(cls.registry)
        cls.thin_registry["profiles"] = [cls.profiles[row["id"]] for row in cls.ledger["new_profiles"]]

    def hard(self, profile_id, text, *, polarity="required", source="user_requirement"):
        thin = copy.deepcopy(self.registry)
        thin["profiles"] = [self.profiles[profile_id]]
        result = pg.resolve_visual_profile_hits(thin, [{"text": text, "source": source, "polarity": polarity}], adult_context=True)
        return any(h["profile_id"] == profile_id and h["hard_eligible"] for h in result["hits"])

    def test_existing_equivalents_preserve_identity_activation_and_every_duty(self):
        for row in self.ledger["existing_profiles"]:
            raw = json.loads((EVIDENCE / "baseline" / row["file"]).read_text())
            before = compile_visual_profile(next(p for p in raw["profiles"] if p["id"] == row["id"]))
            after = self.profiles[row["id"]]
            with self.subTest(profile=row["id"]):
                for key in ["activation", "composition_instruction", "required_evidence_fields", "render_gates", "reject_substitutes", "runtime_expression"]:
                    self.assertEqual(before.get(key), after.get(key), key)
                self.assertEqual(before["semantics"]["definition"], after["semantics"]["definition"])
                for key in ["affected_dimensions", "affected_properties"]:
                    self.assertEqual(before["concept_candidate"].get(key), after["concept_candidate"].get(key))
                for field in before["required_evidence_fields"]:
                    self.assertEqual(before["evidence_requirements"][field]["min_content_words"], after["evidence_requirements"][field]["min_content_words"])
                    self.assertLessEqual(set(before["evidence_requirements"][field]["must_mention_any"]), set(after["evidence_requirements"][field]["must_mention_any"]))
                for phrase in row["added_paraphrases"]:
                    self.assertIsNotNone(pg.candidate_pack_visual_component_match(after, phrase))
                    self.assertFalse(self.hard(row["id"], phrase, source="authorial_core_baseline", polarity="advisory"))

    def test_candidate_equivalents_preserve_prior_labels_scope_and_guards(self):
        allowed = {"paraphrases", "keywords", "embedding_text"}
        for row in self.ledger["candidate_changes"]:
            if row["new"]:
                continue
            raw = json.loads((EVIDENCE / "baseline" / row["file"]).read_text())
            before = next(e for rows in raw["slots"].values() for e in rows if e["id"] == row["id"])
            after = self.entries[row["id"]][1]
            with self.subTest(candidate=row["id"]):
                self.assertEqual({k: v for k, v in before.items() if k not in allowed}, {k: v for k, v in after.items() if k not in allowed})
                for phrase in row["added_paraphrases"]:
                    self.assertIn(phrase, after["paraphrases"])
                    self.assertIn(phrase, after["embedding_text"])

    def test_all_component_variants_are_required_and_literal(self):
        for row in self.ledger["new_profiles"]:
            profile = self.profiles[row["id"]]
            groups = profile["semantics"]["component_semantics"]["groups"]
            for variant in range(4):
                pieces = [g["any_terms"][variant] for g in groups]
                with self.subTest(profile=row["id"], variant=variant):
                    self.assertEqual(pg.candidate_pack_visual_component_match(profile, "; ".join(pieces)), "component_semantics")
                for missing in range(len(pieces)):
                    with self.subTest(profile=row["id"], missing=missing, variant=variant):
                        self.assertIsNone(pg.candidate_pack_visual_component_match(profile, "; ".join(s for i, s in enumerate(pieces) if i != missing)))
            self.assertEqual(len(profile["required_evidence_fields"]), len(groups))
            self.assertEqual(len(profile["render_gates"]), len(groups))
            self.assertTrue(all(g["review_scale"] == "native" for g in profile["render_gates"]))
            self.assertTrue(all("partial" in g["description"] and "unobservable" in g["description"] for g in profile["render_gates"]))

    def test_exact_relation_negation_and_agent_choice_have_distinct_authority(self):
        for row in self.ledger["new_profiles"]:
            profile_id = row["id"]
            profile = self.profiles[profile_id]
            phrase = profile["activation"]["exact_terms"][0]
            with self.subTest(profile=profile_id):
                self.assertTrue(self.hard(profile_id, "The wearer shows " + phrase))
                self.assertFalse(self.hard(profile_id, "The wearer has no " + phrase))
                self.assertFalse(self.hard(profile_id, phrase, polarity="excluded"))
                self.assertFalse(self.hard(profile_id, phrase, source="authorial_core_baseline", polarity="advisory"))
                for alternative in profile["semantics"]["paraphrase_examples"]:
                    self.assertFalse(self.hard(profile_id, alternative))

    def test_nearby_structure_owner_and_version_are_not_complete_proof(self):
        cases = [
            ("uniform_sleeveless_robe_over_inner_sleeves", "A long sleeved outer robe hangs over a sleeveless inner top."),
            ("uniform_robe_waist_join_pleats", "A separately worn pleated skirt lies below a short upper jacket with no sewn join."),
            ("uniform_shoulder_draped_empty_sleeve", "Both arms fill the sleeves of a fur trimmed short coat worn normally over a jacket."),
            ("uniform_jacket_attached_false_vest", "A separately buttoned waistcoat is worn beneath an open short jacket."),
            ("uniform_helmet_connected_suit_neck", "A helmet lies on the floor beside an independent fabric flight suit."),
            ("uniform_neck_scarf_separate_hair_ornament", "One actor wears a neck scarf while another actor wears a hair ornament."),
            ("uniform_grey_yoke_black_body_color_neck", "A colored shoulder yoke sits above a black uniform body with a grey undershirt."),
            ("uniform_hood_belt_cape_layers", "A long cloak hangs from the collar while an independent belt remains below it."),
            ("uniform_kesa_patchwork_outer_border", "Patchwork covers the background wall while the robe has an unbroken plain surface."),
            ("uniform_sailor_lines_follow_collar", "Decorative white lines appear only on the sleeves of a jacket with a plain collar."),
            ("uniform_white_top_red_hakama_layers", "A red upper jacket is worn above white trousers."),
        ]
        for profile_id, text in cases:
            with self.subTest(profile=profile_id):
                self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[profile_id], text))
                self.assertFalse(self.hard(profile_id, text))

    def test_real_index_bm25f_and_fake_embedding_are_advisory_only(self):
        vectors = {p["id"]: [0.0, 1.0] for p in self.thin_registry["profiles"]}
        for row in self.ledger["new_profiles"]:
            pid = row["id"]
            phrase = self.profiles[pid]["semantics"]["paraphrase_examples"][0]
            sources = [{"source": "authorial_core_baseline", "text": phrase, "polarity": "advisory"}]
            with self.subTest(profile=pid, route="real_bm25f"):
                result = pg.resolve_visual_profile_hits(self.registry, sources, visual_profile_index=self.index, query_text=phrase, query_fields={"active_request": phrase}, adult_context=True)
                hit = next(h for h in result["hits"] if h["profile_id"] == pid)
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])
                self.assertTrue(result["bm25f_evaluated"])
                self.assertFalse(result["embedding_evaluated"])
            case_vectors = copy.deepcopy(vectors)
            case_vectors[pid] = [1.0, 0.0]
            fake = pg.build_visual_profile_index_payload(self.thin_registry, vectors=case_vectors, dimensions=2)
            with self.subTest(profile=pid, route="fake_embedding"):
                result = pg.resolve_visual_profile_hits(self.thin_registry, sources, visual_profile_index=fake, query_text=phrase, query_vector=[1.0, 0.0], adult_context=True)
                hit = next(h for h in result["hits"] if h["profile_id"] == pid)
                self.assertEqual(hit["match_basis"], "embedding")
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])
                partial = self.profiles[pid]["semantics"]["component_semantics"]["groups"][0]["any_terms"][2]
                rejected = pg.resolve_visual_profile_hits(self.thin_registry, [{"source": "authorial_core_baseline", "text": partial, "polarity": "advisory"}], visual_profile_index=fake, query_text=partial, query_vector=[1.0, 0.0], adult_context=True)
                self.assertFalse(any(h["profile_id"] == pid for h in rejected["hits"]))

    def test_effects_cannot_override_parent_color_or_hair_locks(self):
        for row in self.ledger["new_profiles"]:
            _, entry = self.entries[row["candidate_id"]]
            for parent in ["wardrobe", "wardrobe." + entry["affected_properties"][0]["property"].split(".")[1]]:
                lock = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [{"dimension": "appearance", "target": "main_subject", "property": parent}]}
                with self.subTest(candidate=entry["id"], locked=parent):
                    self.assertFalse(contracts.property_effects_allowed(lock, entry["affected_dimensions"], entry["affected_properties"]))
            self.assertEqual(entry["affected_dimensions"], ["appearance"])
            self.assertTrue(all(e["target"] == "main_subject" for e in entry["affected_properties"]))
            self.assertFalse(any(e["property"].startswith("body") for e in entry["affected_properties"]))
        for candidate_id, prop in [("unif_grey_yoke_black_body_color_neck", "wardrobe.color"), ("unif_neck_scarf_separate_hair_ornament", "hair")]:
            _, entry = self.entries[candidate_id]
            lock = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [{"dimension": "appearance", "target": "main_subject", "property": prop}]}
            self.assertFalse(contracts.property_effects_allowed(lock, entry["affected_dimensions"], entry["affected_properties"]))

    def test_optional_bundles_resolve_all_members_without_combining_alternative_versions(self):
        extension = json.loads((ASSETS / "photo_prompt_costume_cosplay_extension.json").read_text())
        bundles = [b for b in extension["visual_semantics"] if b["id"].startswith("uniform_")]
        for bundle in bundles:
            with self.subTest(bundle=bundle["id"]):
                self.assertTrue(bundle["candidate_only"])
                self.assertEqual(bundle["activation_mode"], "independent_component_request_evidence_only")
                for candidate_id in bundle["candidate_ids"]:
                    self.assertIn(candidate_id, self.entries)
                    self.assertEqual(bundle["candidate_slots"][candidate_id], self.entries[candidate_id][0])
                self.assertTrue(all(pid in self.profiles for pid in bundle["hard_profile_ids"]))
                self.assertNotIn("comparison_pool", json.dumps(bundle))
        self.assertFalse(any("patchwork_robe_waist_support" in b["id"] for b in bundles))

    def test_provenance_and_unverified_named_versions_do_not_leak_into_exact_runtime_terms(self):
        broad = {"전복", "철릭", "경찰", "군복", "JAL", "2B", "Starfleet", "DS9", "SQ", "AGSU", "ASU"}
        for row in self.ledger["new_profiles"]:
            profile = self.profiles[row["id"]]
            _, entry = self.entries[row["candidate_id"]]
            with self.subTest(profile=row["id"]):
                self.assertTrue(broad.isdisjoint(profile["activation"]["exact_terms"]))
                self.assertFalse(profile["activation"]["requires_adult_character"])
                public = " ".join([entry["en"], entry["ko"], entry["embedding_text"], *entry["paraphrases"]]).casefold()
                for term in ["http", "source_id", "research", "2026", "sexual", "rank mapping", "canonically accurate"]:
                    self.assertNotIn(term, public)
                self.assertTrue(entry["concept_units"])
                self.assertTrue(entry["relations"])
                self.assertEqual(entry["affected_properties"], profile["concept_candidate"]["affected_properties"])

    def test_concise_equivalents_keep_every_original_native_duty(self):
        receipt = json.loads((EVIDENCE / "NATURAL-ENHANCEMENT-LEDGER.json").read_text())
        for event in receipt["events"]:
            pid = event["profile_id"]
            profile = self.profiles[pid]
            for language in ["en", "ko"]:
                pieces = event["components_" + language]
                with self.subTest(profile=pid, language=language):
                    self.assertIsNotNone(pg.candidate_pack_visual_component_match(profile, "; ".join(pieces)))
                    self.assertFalse(self.hard(pid, "; ".join(pieces), source="authorial_core_baseline", polarity="advisory"))
                for missing in range(len(pieces)):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(profile, "; ".join(s for i, s in enumerate(pieces) if i != missing)))
            source = next(p for d in EVIDENCE.joinpath("before-natural-enhancement").glob("photo_prompt_visual_obligations*.json") for p in json.loads(d.read_text()).get("profiles", []) if p["id"] == pid)
            before = compile_visual_profile(source)
            for key in ["activation", "render_gates", "composition_instruction", "required_evidence_fields"]:
                self.assertEqual(before[key], profile[key])

    def test_same_frozen_independent_inputs_now_support_selected_relations(self):
        # These reproduce observed first-round failures. They are disclosed
        # diagnostic regressions, not an unseen generalization benchmark.
        cases = json.loads((EVIDENCE / "independent-round-1-regression-inputs.json").read_text())["cases"]
        for case in cases:
            pid = case["expected_profile_id"]
            sources = [{"source": "authorial_core_baseline", "text": case["baseline_prompt_en"], "polarity": "advisory"}, {"source": "authorial_core_interpretation", "text": case["interpreted_intent"], "polarity": "advisory"}]
            with self.subTest(arm=case["arm"]):
                self.assertIsNotNone(pg.candidate_pack_visual_component_match(self.profiles[pid], " ".join(s["text"] for s in sources)))
                result = pg.candidate_pack_resolve_visual_profiles(self.data, {"provenance": {"authorial_core": case["authorial_core"]}}, {}, None)
                hit = next(h for h in result["hits"] if h["profile_id"] == pid)
                self.assertFalse(hit["hard_eligible"])
                self.assertTrue(hit["optional_eligible"])
                self.assertEqual(hit["match_basis"], "bm25f_frozen_components")
                self.assertEqual(hit["source_intent_ids"], [])

    def test_component_discovery_preserves_opt_in_effect_locks_and_exclusions(self):
        cases = json.loads((EVIDENCE / "independent-round-1-regression-inputs.json").read_text())["cases"]
        for case in cases:
            pid = case["expected_profile_id"]
            for guard in ["closed_dimension", "locked_property", "excluded_relation", "partial_relation", "source_opt_out"]:
                core = copy.deepcopy(case["authorial_core"])
                data = self.data
                if guard == "closed_dimension":
                    core["intent_lock"]["open_dimensions"].remove("appearance")
                elif guard == "locked_property":
                    core["intent_lock"]["semantic_anchors"].append({"dimension": "appearance", "target": "main_subject", "property": "wardrobe"})
                elif guard == "excluded_relation":
                    core["user_exclusions"].append(self.profiles[pid]["semantics"]["definition"])
                elif guard == "partial_relation":
                    core["baseline_prompt_en"] = self.profiles[pid]["semantics"]["component_semantics"]["groups"][0]["any_terms"][0]
                    core["interpreted_intent"] = "A fictional adult wearer."
                else:
                    data = {**self.data, pg.VISUAL_OBLIGATIONS_DATA_KEY: copy.deepcopy(self.registry)}
                    next(p for p in data[pg.VISUAL_OBLIGATIONS_DATA_KEY]["profiles"] if p["id"] == pid)["concept_candidate"]["core_assertion_discovery"] = False
                with self.subTest(arm=case["arm"], guard=guard):
                    result = pg.candidate_pack_resolve_visual_profiles(data, {"provenance": {"authorial_core": core}}, {}, None)
                    self.assertFalse(any(h["profile_id"] == pid and h["match_basis"] == "bm25f_frozen_components" for h in result["hits"]))

    def test_version_and_attachment_boundaries_survive_shorter_expressions(self):
        cases = [
            ("uniform_full_trousers_gathered_cuffs", "straight trouser legs ending in wide open cuffs"),
            ("uniform_full_trousers_gathered_cuffs", "a voluminous skirt gathered around a single lower hem"),
            ("uniform_continuous_coverall_front_closure", "a separate jacket with a central front zipper worn above separate trousers"),
            ("uniform_neck_scarf_separate_hair_ornament", "a scarf end hangs downward, below a distinct ornament in the hair"),
            ("uniform_grey_yoke_black_body_color_neck", "colored shoulders over a grey body with a black inner collar"),
        ]
        for pid, text in cases:
            self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[pid], text))
            self.assertFalse(self.hard(pid, text))


if __name__ == "__main__":
    unittest.main()
