from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
RESEARCH = ROOT / "docs/research-evidence/photo-prompt/photo-editing-effects-20261001"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as generator
import photo_candidate_semantics as semantics
import audit_composed_prompt as auditor
from photo_contracts import property_effects_allowed
from tests import test_photo_authorial_core_v6 as v6


class PhotoEditingEffectsSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = generator.load_json(ASSETS / "photo_prompt_tags.json")
        cls.registry = generator.load_visual_obligation_registry(ASSETS / "photo_prompt_visual_obligations.json")
        cls.extension = json.loads((ASSETS / "photo_prompt_editing_effects_extension.json").read_text())
        cls.profiles = {p["id"]: p for p in cls.registry["profiles"]}
        cls.bundle = next(b for b in cls.data["candidate_bundles"] if b["id"] == "pe_bundle_muted_grain_finish")
        cls.semantic_index = generator.load_semantic_index_payload(ASSETS / "photo_prompt_semantic_index.json")
        generator.validate_semantic_index_metadata(cls.semantic_index, cls.data)
        cls.data[generator.SEMANTIC_INDEX_DATA_KEY] = cls.semantic_index
        cls.bm25 = generator.semantic_bm25f_payload_from_index(cls.semantic_index)
        cls.visual_index = generator.load_visual_profile_index(ASSETS / "photo_prompt_visual_profile_index.json", cls.registry)
        cls.data[generator.VISUAL_OBLIGATIONS_DATA_KEY] = cls.registry
        cls.data[generator.VISUAL_PROFILE_INDEX_DATA_KEY] = cls.visual_index

    def entry(self, slot, entry_id):
        return generator.candidate_pack_slot_entry_by_id(self.data, slot, entry_id)

    def pack(self, bundle=None, protected=False):
        bundle = bundle or self.bundle
        core = generator.normalize_authorial_core(v6.core(), request_envelope=generator.normalize_request_envelope(v6.envelope()))
        core["intent_lock"]["open_dimensions"].append("style")
        core["intent_lock"]["locked_dimensions"] = [d for d in core["intent_lock"]["locked_dimensions"] if d != "style"]
        core["baseline_prompt_en"] += " " + " ".join(unit for m in bundle["member_candidates"] for unit in m["concept_units"])
        if protected:
            core["intent_lock"]["semantic_anchors"].append({
                "dimension": "appearance", "target": "main_subject", "property": "wardrobe.color",
                "meaning": "keep the declared blue garment color"})
        slots = {}
        for m in bundle["member_candidates"]:
            e = self.entry(m["slot"], m["entry_id"])
            c, _ = generator.candidate_pack_summarize_slot_candidate(self.data, m['slot'], {'id': m['entry_id'], 'applicability_status': 'eligible'})
            c["_v6_semantic_source"] = semantics.semantic_source(e, m["slot"], self.data["candidate_semantic_policy"])
            slots.setdefault(m["slot"], {"slot": m["slot"], "candidates": []})["candidates"].append(c)
        pack = {"contract_version": "photo-candidate-pack/v6", "authorial_core": core, "slots": slots,
                 "provenance": {"seed": 311}}
        pack["candidate_bundles"] = generator.candidate_pack_candidate_bundles(self.data, pack)
        return pack

    def test_all_reference_rows_have_reviewed_dispositions_and_no_metadata_aesthetic(self):
        ledger = json.loads((RESEARCH / "implementation-disposition-ledger.json").read_text())
        self.assertEqual(len(ledger["rows"]), 245)
        self.assertEqual(len({row["reference_row"] for row in ledger["rows"]}), 245)
        self.assertEqual(len({row["proposal_group_id"] for row in ledger["rows"]}), 88)
        known = {f"slot:{s}:{e['id']}" for s, vs in self.data["slots"].items() for e in vs}
        for row in ledger["rows"]:
            self.assertTrue(set(row["candidate_ids"]) <= known)
            if row["route"] == "workflow_or_operator_metadata_no_automatic_visual_projection":
                self.assertEqual(row["candidate_ids"], [])
                self.assertIn("pixels cannot prove", row["workflow_contract"])
        labels = [e["en"].casefold() for vs in self.extension["slots"].values() for e in vs]
        self.assertNotIn("raw development", labels)
        self.assertNotIn("icc profile", labels)
        self.assertNotIn("frequency separation", labels)

    def test_declared_owners_preserve_legacy_compounds_and_add_atomic_effects(self):
        legacy = self.entry("texture", "halation")
        self.assertEqual(legacy["en"], "film halation and soft light bloom")
        self.assertEqual(legacy["affected_dimensions"], ["style", "color"])
        self.assertEqual(self.entry("texture", "fine_grain")["affected_dimensions"], ["style"])
        self.assertEqual(self.entry("grain_profile", "pe_fine_midtonal_grain")["affected_dimensions"], ["style"])
        self.assertNotIn("material", self.entry("grain_profile", "pe_fine_midtonal_grain")["affected_dimensions"])
        self.assertEqual(self.entry("surface_material", "pe_watercolor_print")["affected_properties"][0]["target"], "depicted_artifact")
        self.assertEqual(self.entry("color_grading", "pe_red_object_splash")["affected_properties"][0]["target"], "*")

    def test_profile_components_are_single_source_all_of_native_gates(self):
        source = json.loads((ASSETS / "photo_prompt_visual_obligations_editing_effects.json").read_text())
        self.assertEqual(len(source["profiles"]), 22)
        all_gate_ids = [g["id"] for p in self.registry["profiles"] for g in p["render_gates"]]
        self.assertEqual(len(all_gate_ids), len(set(all_gate_ids)))
        for p in source["profiles"]:
            compiled = self.profiles[p["id"]]
            components = p["authored_components"]["components"]
            self.assertEqual(compiled["semantics"]["component_semantics"]["minimum_component_groups"], len(components))
            self.assertEqual(len(compiled["render_gates"]), len(components))
            self.assertFalse(p["activation"]["requires_adult_character"])
            self.assertEqual(compiled["required_evidence_fields"], [c["evidence_field"] for c in components])
            self.assertTrue(all("partial" in g["description"] for g in compiled["render_gates"]))

    def test_source_property_effects_survive_pack_and_cannot_bypass_partial_color_lock(self):
        e = self.entry("grain_profile", "pe_fine_midtonal_grain")
        source = semantics.semantic_source(e, "grain_profile", self.data["candidate_semantic_policy"])
        self.assertEqual(source["affected_properties"], e["affected_properties"])
        source["affected_properties"][0]["target"] = "tampered"
        self.assertEqual(e["affected_properties"][0]["target"], "image_plane")
        lock = self.pack(protected=True)["authorial_core"]["intent_lock"]
        self.assertTrue(property_effects_allowed(lock, e["affected_dimensions"], e["affected_properties"]))
        color = self.entry("color_grading", "pe_muted_chroma")
        self.assertFalse(property_effects_allowed(lock, color["affected_dimensions"], color["affected_properties"]))
        projected = generator.candidate_pack_project(self.pack(), "v6")
        c = projected["slots"]["grain_profile"]["candidates"][0]
        self.assertEqual(c["affected_properties"], e["affected_properties"])

    def test_partial_lock_blocks_both_visible_and_joint_bundle_admission(self):
        pack = self.pack()
        ids = {b["id"] for b in generator.candidate_pack_candidate_bundles(self.data, pack)["candidates"]}
        self.assertIn("bundle:pe_bundle_muted_grain_finish", ids)
        pack = self.pack(protected=True)
        ids = {b["id"] for b in semantics.public_bundles(self.data, pack)["candidates"]}
        self.assertNotIn("bundle:pe_bundle_muted_grain_finish", ids)
        pack["slots"] = {}
        ids = {b["id"] for b in generator.candidate_pack_candidate_bundles(self.data, pack)["candidates"]}
        self.assertNotIn("bundle:pe_bundle_muted_grain_finish", ids)

    def test_forged_selected_property_effects_fail_source_recomputed_audit(self):
        pack = generator.candidate_pack_project(self.pack(), "v6")
        row = pack["slots"]["grain_profile"]["candidates"][0]
        row["affected_properties"] = [{"dimension": "style", "target": "elsewhere", "property": "none"}]
        failures = auditor.audit_candidate_semantic_contracts(pack, "", {row["id"]},
                    auditor.candidate_objects_from_pack(pack), [])
        self.assertTrue(any("must match the source" in f["reason"] for f in failures))

    def test_all_simultaneous_bundle_units_have_their_own_required_component(self):
        for b in self.extension["visual_semantics"]:
            slots = b["candidate_slots"]
            self.assertEqual(len(set(slots.values())), len(slots))
            self.assertTrue(all(len(c["visible_evidence"]) == 1 for c in b["component_groups"]))
            compiled = next(r for r in self.data["candidate_bundles"] if r["id"] == b["id"])
            self.assertEqual(compiled["adoption"], "optional")
            self.assertEqual(compiled["profile_activation"], "independent_request_evidence_only")
            expected = [u for m in compiled["member_candidates"] for u in m["concept_units"]]
            self.assertEqual(expected, [c["visible_evidence"][0] for c in b["component_groups"]])

    def test_coexisting_effects_remain_applicable_but_substitution_only_is_rejected(self):
        pairs = [
            ("highlight_rolloff_tone_response", "highlight-rolloff tone response with localized bloom", "bloom only"),
            ("diffusion_filter_highlight_halation", "diffusion-filter highlight halation with film halation", "film halation only"),
            ("panning_subject_tracking_motion_relation", "panning subject-tracking motion relation with rear-curtain flash", "rear-curtain flash only"),
        ]
        for pid, positive, negative in pairs:
            p = self.profiles[pid]
            self.assertTrue(generator.visual_profile_context_applicability(p, positive,
                            has_authorial_core_context=True, require_positive_context_terms=False)[0])
            self.assertFalse(generator.visual_profile_context_applicability(p, negative,
                             has_authorial_core_context=True, require_positive_context_terms=False)[0])
            registry = {**self.registry, "profiles": [p]}
            index = generator.build_visual_profile_index_payload(registry)
            resolution = generator.resolve_visual_profile_hits(registry,
                [{"source": "concept_lock", "text": positive, "polarity": "required", "priority": "critical", "mandatory": True}],
                visual_profile_index=index, adult_context=False)
            self.assertTrue(any(h["profile_id"] == pid and h.get("hard_eligible") for h in resolution["hits"]))

    def test_malformed_property_declarations_fail_before_candidate_use(self):
        for mutation in ("unknown_dimension", "unknown_key", "duplicate", "empty_target"):
            e = copy.deepcopy(self.entry("grain_profile", "pe_fine_midtonal_grain"))
            if mutation == "unknown_dimension":
                e["affected_properties"][0]["dimension"] = "appearance"
            elif mutation == "unknown_key":
                e["affected_properties"][0]["trusted"] = True
            elif mutation == "duplicate":
                e["affected_properties"].append(copy.deepcopy(e["affected_properties"][0]))
            else:
                e["affected_properties"][0]["target"] = ""
            with self.assertRaisesRegex(ValueError, "malformed affected properties"):
                semantics.validate_candidate_entries({"slots": {"grain_profile": [e]}}, generator.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)

    def test_frozen_three_arm_effects_remain_retrievable_after_core_freeze(self):
        cases = {
            "arm-a-film-optics": {"slot:grain_profile:pe_fine_midtonal_grain", "slot:film_emulation:pe_red_edge_halation", "slot:color_grading:pe_gentle_rolloff"},
            "arm-b-digital-motion": {"slot:camera_type:pe_compact_flash_noisy_finish", "slot:grain_profile:pe_digital_luma_noise", "slot:grain_profile:pe_digital_chroma_noise", "slot:motion:pe_flash_core_shutter_trace"},
            "arm-c-tonal-skin": {"slot:color_grading:pe_red_object_splash", "slot:color_grading:pe_lifted_black_floor", "slot:skin_finish:pe_texture_preserving_tone_evening"},
        }
        for arm, expected in cases.items():
            with self.subTest(arm=arm):
                root = RESEARCH / "qualification" / arm
                raw = json.loads((root / "authorial_core.json").read_text())
                old = json.loads((root / "candidate_pack.json").read_text())
                old = old[0] if isinstance(old, list) else old
                controls = old["creative_controls"]
                core = old["authorial_core"]
                slots, binding, _ = generator.retrieve_core_slots(self.data, core, controls)
                candidates = {c["id"] for p in slots.values() for c in p["candidates"]}
                self.assertTrue(expected <= candidates, expected - candidates)
                self.assertLessEqual(sum(len(p["candidates"]) for p in slots.values()), generator.CANDIDATE_PACK_TOTAL_CANDIDATE_LIMIT)
                self.assertEqual(binding["source_authorial_core_sha256"], core["canonical_sha256"])
                self.assertEqual(core, old["authorial_core"])
                self.assertEqual(core["baseline_prompt_en"], raw["baseline_prompt_en"])

    def test_advisory_discovery_adds_no_requester_duty_and_obeys_closed_and_partial_locks(self):
        core = json.loads((RESEARCH / "qualification/arm-c-tonal-skin/authorial_core.json").read_text())
        documents = {f"slot:{s}:{e['id']}": e for s, values in self.extension["slots"].items() for e in values}
        found = generator.candidate_pack_assertion_discovery(self.data, core, documents, self.bm25)
        self.assertIn("slot:color_grading:pe_red_object_splash", found)
        no_assertions = {**core, "semantic_assertions": []}
        self.assertEqual(generator.candidate_pack_assertion_discovery(self.data, no_assertions, documents, self.bm25), [])
        closed = copy.deepcopy(core)
        closed["intent_lock"]["open_dimensions"] = []
        self.assertEqual(generator.candidate_pack_assertion_discovery(self.data, closed, documents, self.bm25), [])
        protected = copy.deepcopy(core)
        protected["intent_lock"]["semantic_anchors"].append({"dimension": "appearance", "target": "main_subject", "property": "wardrobe.color", "meaning": "keep blue shirt"})
        allowed = generator.candidate_pack_assertion_discovery(self.data, protected, documents, self.bm25)
        self.assertNotIn("slot:color_grading:pe_red_object_splash", allowed)
        self.assertNotIn("slot:color_grading:pe_lifted_black_floor", allowed)
        self.assertIn("slot:skin_finish:pe_texture_preserving_tone_evening", allowed)
        excluded = copy.deepcopy(core)
        excluded["semantic_assertions"][0]["polarity"] = "excluded"
        self.assertNotIn("slot:color_grading:pe_red_object_splash", generator.candidate_pack_assertion_discovery(self.data, excluded, documents, self.bm25))

    def test_focused_profile_matches_remain_optional_until_separate_opt_in(self):
        for arm, expected in {
            "arm-a-film-optics": {"pe_fine_midtonal_grain_relation"},
            "arm-b-digital-motion": {"pe_digital_luma_noise_relation", "pe_digital_chroma_noise_relation"},
            "arm-c-tonal-skin": {"pe_red_object_splash_relation", "pe_lifted_black_floor_relation", "pe_texture_preserving_tone_evening_relation"},
        }.items():
            with self.subTest(arm=arm):
                core = json.loads((RESEARCH / "qualification" / arm / "authorial_core.json").read_text())
                result = {"provenance": {"authorial_core": core}}
                resolution = generator.candidate_pack_resolve_visual_profiles(self.data, result, {}, None)
                # Equivalent expressions can expose the same optional profile
                # through whole-scene BM25F before the focused discovery lane.
                # Authority and coverage must survive that ranking change.
                discovered = [h for h in resolution["hits"] if h["profile_id"] in expected]
                self.assertTrue(expected <= {h["profile_id"] for h in discovered})
                self.assertTrue(all(h["optional_eligible"] and not h["hard_eligible"] and not h["source_intent_ids"] for h in discovered))

    def test_retrieval_cannot_bypass_declared_context_guards(self):
        old = json.loads((RESEARCH / "qualification/arm-a-film-optics/candidate_pack.json").read_text())
        old = old[0] if isinstance(old, list) else old
        core, controls = old["authorial_core"], old["creative_controls"]
        slots, _, _ = generator.retrieve_core_slots(self.data, core, controls)
        self.assertIn("slot:grain_profile:pe_fine_midtonal_grain", {c["id"] for p in slots.values() for c in p["candidates"]})
        blocked = copy.deepcopy(self.data)
        grain = generator.candidate_pack_slot_entry_by_id(blocked, "grain_profile", "pe_fine_midtonal_grain")
        grain["requires_all"] = ["undeclared_context_for_test"]
        slots, _, _ = generator.retrieve_core_slots(blocked, core, controls)
        self.assertNotIn("slot:grain_profile:pe_fine_midtonal_grain", {c["id"] for p in slots.values() for c in p["candidates"]})

    def test_discovery_configuration_rejects_unbounded_or_unscoped_source_opt_in(self):
        for key, value in (("maximum_candidates", 10000), ("maximum_per_assertion", 5), ("minimum_shared_content_words", 1)):
            policy = copy.deepcopy(self.data["candidate_semantic_policy"])
            policy["core_assertion_discovery"][key] = value
            with self.assertRaisesRegex(ValueError, "core assertion discovery"):
                semantics.validate_semantic_policy(policy, generator.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)
        entry = copy.deepcopy(self.entry("grain_profile", "pe_fine_midtonal_grain"))
        entry.pop("affected_properties")
        with self.assertRaisesRegex(ValueError, "explicit property scope"):
            semantics.validate_candidate_entries({"slots": {"grain_profile": [entry]}}, generator.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)


if __name__ == "__main__":
    unittest.main()
