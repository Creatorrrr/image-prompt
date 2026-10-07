"""Meaning, ownership and optionality checks; never rendered-image proof."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/photo-prompt-image-generator"
sys.path.insert(0, str(SKILL / "scripts"))
import prompt_generator as pg
import photo_candidate_semantics as cs
from photo_contracts import property_effects_allowed
from photo_visual_retrieval import positive_visual_profile_text
from visual_profile_contracts import compile_visual_profile


class VisualGrammarIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = json.loads((SKILL / "assets/photo_prompt_visual_grammar_extension.json").read_text())
        cls.data = pg.load_json(SKILL / "assets/photo_prompt_tags.json")
        cls.registry = pg.load_visual_obligation_registry(SKILL / "assets/photo_prompt_visual_obligations.json")
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"] if p["id"].startswith("vg_")}
        cls.scoped = {**cls.registry, "profiles": list(cls.profiles.values())}
        cls.index = pg.build_visual_profile_index_payload(cls.scoped)
        cls.entries = {e["id"]: e for rows in cls.extension["slots"].values() for e in rows}

    def hard(self, text, polarity="required"):
        result = pg.resolve_visual_profile_hits(self.scoped,
            [{"source": "concept_lock", "text": text, "polarity": polarity, "mandatory": True}],
            visual_profile_index=self.index, adult_context=False)
        return {h["profile_id"] for h in result["hits"] if h.get("hard_eligible")}

    def test_complete_names_negation_and_exclusion_have_distinct_authority(self):
        for pid, profile in self.profiles.items():
            for phrase in profile["activation"]["exact_terms"]:
                with self.subTest(profile=pid, phrase=phrase):
                    self.assertEqual(self.hard(phrase), {pid})
                    self.assertNotIn(pid, self.hard("not " + phrase))
                    self.assertNotIn(pid, self.hard(phrase, "excluded"))

    def test_broad_labels_and_adjacent_owners_do_not_create_new_hard_duties(self):
        negatives = ["a candid laugh", "closed lips", "a pencil-shaped eyebrow",
            "a pencil hovering above a printed page", "a hand merely holding a page",
            "water ripples caused by a voice", "a hand hovering over water",
            "a miniature-looking full-size city with tilt-shift blur", "silk fabric",
            "a loose ribbon next to a seam", "a flower placed beside a printed drawing",
            "a blue-orange image grade", "a romantic gothic mood", "wide negative space"]
        for text in negatives:
            with self.subTest(text=text):
                self.assertFalse(self.hard(text))

    def test_approximate_complete_relation_is_optional_even_with_perfect_fake_vector(self):
        pid = "vg_pencil_paper_trace_profile"
        vectors = {p: ([1., 0.] if p == pid else [0., 1.]) for p in self.profiles}
        index = pg.build_visual_profile_index_payload(self.scoped, vectors=vectors, dimensions=2)
        text = "The pencil grip belongs to her hand; its pencil tip touches a supported paper sheet and a graphite trace extends at contact."
        result = pg.resolve_visual_profile_hits(self.scoped,
            [{"source": "authorial_core_interpretation", "text": text, "polarity": "advisory"}],
            visual_profile_index=index, query_text=text, query_vector=[1., 0.], adult_context=False)
        hit = next(h for h in result["hits"] if h["profile_id"] == pid)
        self.assertTrue(hit["optional_eligible"])
        self.assertFalse(hit["hard_eligible"])
        partial = "A pencil grip and a paper sheet are visible."
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles[pid], partial))

    def test_contact_and_transformation_keep_their_own_connected_endpoints(self):
        pencil = self.entries["vg_pencil_paper_trace"]
        self.assertIn(("contacts", "pencil_tip", "same_paper_sheet"),
                      {(r["type"], r["subject"], r["object"]) for r in pencil["relations"]})
        self.assertIn("continues_from", {r["type"] for r in pencil["relations"]})
        water = self.entries["vg_hand_water_local_ripples"]
        self.assertIn(("centers_on", "local_ripples", "same_contact_region"),
                      {(r["type"], r["subject"], r["object"]) for r in water["relations"]})
        transition = self.entries["vg_graphite_thread_raised_flower"]
        self.assertEqual({r["type"] for r in transition["relations"]},
                         {"lies_on", "rises_at", "continues_into", "connects"})
        self.assertTrue(all(p["target"] == "depicted_artifact" for p in transition["affected_properties"]))
        scale = self.entries['vg_artifact_common_plane_scale']
        self.assertEqual(set(scale['affected_dimensions']), {'composition'})
        self.assertEqual({r['type'] for r in scale['relations']}, {'shares_depth_with', 'compares_local_size_with'})
        self.assertNotIn('camera', scale['affected_dimensions'])

    def test_artifact_scale_discovery_requires_a_reference_and_shared_depth(self):
        profile = self.profiles['vg_artifact_common_plane_scale_profile']
        complete = 'The miniature model has a coin as a known-size reference at the same depth, allowing a local relative size comparison.'
        self.assertIsNotNone(pg.candidate_pack_visual_component_match(profile, complete))
        for partial in ['A miniature model seen with a blurred background.',
                        'A distant model behind a familiar coin.',
                        'A full-size city photographed through tilt-shift blur.']:
            with self.subTest(text=partial):
                self.assertIsNone(pg.candidate_pack_visual_component_match(profile, partial))
                self.assertFalse(self.hard(partial))

    def test_locked_contact_weave_or_artifact_junction_cannot_be_changed_by_alias(self):
        for eid, target, prop in [("vg_pencil_paper_trace", "main_subject", "body.hand_tool_contact"),
                ("vg_hand_water_local_ripples", "main_subject", "body.hand_water_contact"),
                ("vg_faille_crossgrain_ribs", "existing_cloth", "surface.weave"),
                ("vg_graphite_thread_raised_flower", "depicted_artifact", "surface.junction")]:
            entry = self.entries[eid]
            lock = {"contract_version": "photo-intent-lock/v2", "semantic_anchors": [
                {"dimension": "appearance", "target": target, "property": prop}]}
            with self.subTest(candidate=eid):
                self.assertFalse(property_effects_allowed(lock, entry["affected_dimensions"], entry["affected_properties"]))
                lock["semantic_anchors"][0]["property"] = prop.split(".")[0]
                self.assertFalse(property_effects_allowed(lock, entry["affected_dimensions"], entry["affected_properties"]))
        for entry in self.entries.values():
            self.assertFalse(set(entry["affected_dimensions"]) & {"identity", "age", "count", "sexual_tone"})

    def test_bundles_require_every_member_and_do_not_implicitly_activate_a_profile(self):
        for bundle in self.data["candidate_bundles"]:
            if not bundle["id"].startswith("vg_"):
                continue
            self.assertEqual(bundle["profile_activation"], "independent_request_evidence_only")
            slots, dims = {}, set()
            for member in bundle["member_candidates"]:
                dims.update(member["affected_dimensions"])
                slots.setdefault(member["slot"], {"candidates": []})["candidates"].append(
                    {"id": member["id"], "applicability": {"status": "eligible"}})
            pack = {"slots": slots, "authorial_core": {"intent_lock": {"open_dimensions": list(dims)}}}
            data = {**self.data, "candidate_bundles": [bundle]}
            self.assertEqual(len(cs.public_bundles(data, pack)["candidates"]), 1)
            for dim in dims:
                blocked = copy.deepcopy(pack)
                blocked["authorial_core"]["intent_lock"]["open_dimensions"].remove(dim)
                self.assertEqual(cs.public_bundles(data, blocked)["candidates"], [])

    def test_every_adopted_relation_requires_all_component_evidence_and_pixel_gates(self):
        for pid, profile in self.profiles.items():
            with self.subTest(profile=pid):
                compiled = compile_visual_profile(profile)
                source = profile["authored_components"]
                self.assertEqual(len(compiled["required_evidence_fields"]), len(source["components"]))
                self.assertEqual(len(compiled["render_gates"]), len(source["components"]))
                self.assertTrue(all("partial" in g["description"] and "fails" in g["description"] for g in compiled["render_gates"]))
                broken = copy.deepcopy(profile)
                broken["authored_components"]["obligations"][0]["component_ids"] = ["missing_owner"]
                with self.assertRaises(ValueError):
                    compile_visual_profile(broken)

    def test_maintenance_claims_and_false_substitutes_are_not_positive_retrieval_text(self):
        ref = self.extension["maintenance_ref"]
        ledger = json.loads((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (ref["record_id"] + ".json")).read_text())
        self.assertEqual(ref["sha256"], cs.digest(ledger))
        self.assertEqual({p["id"] for p in ledger["proposals"]}, {f"G{i:02d}" for i in range(1, 41)})
        self.assertTrue(all(not p["effect_verified_by_controlled_comparison"] for p in ledger["proposals"]))
        for pid, profile in self.profiles.items():
            poisoned = copy.deepcopy(profile)
            sentinel = "QZX provenance source false substitute claim"
            poisoned["semantics"]["claim_limits"] = [sentinel]
            poisoned["semantics"]["contrast_examples"] = [sentinel]
            self.assertEqual(positive_visual_profile_text(profile), positive_visual_profile_text(poisoned))
            self.assertNotIn("https://", positive_visual_profile_text(profile))
        for slot, entries in self.extension["slots"].items():
            for entry in entries:
                poisoned = copy.deepcopy(entry)
                poisoned["contextual_usage"] = {"contexts": [{"id": "sentinel", "definition": "QZX provenance"}]}
                self.assertEqual(pg.semantic_text_for_entry(entry, slot), pg.semantic_text_for_entry(poisoned, slot))

    def test_additive_contexts_preserve_all_existing_fields_and_scope_guards(self):
        inventory = pg.photo_source_manifest.SourceInventory.for_test(SKILL / 'assets',
            candidate_files=tuple(name for name in pg.RESEARCH_EXTENSION_FILENAMES
                if name not in {'photo_prompt_visual_grammar_extension.json', 'photo_prompt_vel_appearance_relations_extension.json'}))
        before = pg.load_json(SKILL / 'assets/photo_prompt_tags.json', inventory=inventory)
        for slot, additions in self.extension['existing_slot_context_extensions'].items():
            old = {e['id']: e for e in before['slots'][slot]}
            live = {e['id']: e for e in self.data['slots'][slot]}
            for eid, added in additions.items():
                with self.subTest(slot=slot, candidate=eid):
                    retained = set(old[eid]) - {'paraphrases', 'contextual_usage'}
                    self.assertEqual({k: live[eid].get(k) for k in retained}, {k: old[eid][k] for k in retained})
                    self.assertTrue(set(old[eid].get('paraphrases', [])) <= set(live[eid].get('paraphrases', [])))
                    old_contexts = old[eid].get('contextual_usage', {}).get('contexts', [])
                    new_contexts = live[eid].get('contextual_usage', {}).get('contexts', [])
                    self.assertTrue(all(c in new_contexts for c in old_contexts + added['contexts']))


if __name__ == "__main__":
    unittest.main()
