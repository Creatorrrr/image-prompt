from __future__ import annotations

import copy
import hashlib
import json
import random
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/photo-prompt-image-generator/assets"
sys.path.insert(0, str(ASSETS.parent / "scripts"))
import prompt_generator as generator
import photo_candidate_semantics as semantics
import audit_composed_prompt as auditor
import compose_pack_view as views
from tests import test_photo_authorial_core_v6 as v6


class PhotoCandidateSemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = generator.load_json(ASSETS / "photo_prompt_tags.json")
        cls.bundle = next(row for row in cls.data["candidate_bundles"] if row["id"] == "clean_beauty_clamshell")

    def source_pack(self):
        core = generator.normalize_authorial_core(v6.core(), request_envelope=generator.normalize_request_envelope(v6.envelope()))
        slots = {}
        for member in self.bundle["member_candidates"]:
            entry = generator.candidate_pack_slot_entry_by_id(self.data, member["slot"], member["entry_id"])
            candidate, _ = generator.candidate_pack_summarize_slot_candidate(
                self.data, member["slot"], {"id": member["entry_id"], "applicability_status": "eligible"}, 0.5, member["entry_id"])
            candidate["_v6_semantic_source"] = semantics.semantic_source(entry, member["slot"], self.data["candidate_semantic_policy"])
            slots.setdefault(member["slot"], {"slot": member["slot"], "candidates": []})["candidates"].append(candidate)
        pack = {"contract_version": "photo-candidate-pack/v6", "authorial_core": core,
                "slots": slots, "presets": [], "provenance": {"seed": 17}}
        pack["candidate_bundles"] = semantics.public_bundles(self.data, pack)
        return pack

    def pack(self):
        return generator.candidate_pack_project(self.source_pack(), "v6")

    def check(self, pack, chosen=(), evidence=None, prompt=""):
        return auditor.audit_candidate_semantic_contracts(pack, prompt, set(chosen),
                                                         auditor.candidate_objects_from_pack(pack), evidence or [])

    def test_all_127_authored_bundles_compile_and_profile_links_remain_advisory(self):
        sources = [row for path in ASSETS.glob("*extension.json")
                   for row in json.loads(path.read_text()).get("visual_semantics", [])]
        self.assertEqual(len(self.data["candidate_bundles"]), 127)
        self.assertEqual({row["id"] for row in sources}, {row["id"] for row in self.data["candidate_bundles"]})
        for bundle in self.data["candidate_bundles"]:
            self.assertEqual(bundle["adoption"], "optional")
            self.assertEqual(bundle["profile_activation"], "independent_request_evidence_only")
            self.assertTrue(bundle["member_candidates"])
        pack = self.pack()
        self.assertTrue(pack["candidate_bundles"]["candidates"])
        self.assertNotIn("visual_obligations", pack)
        self.assertFalse(self.check(pack))

    def test_unknown_runtime_keys_and_missing_or_ambiguous_references_fail(self):
        extension = {"schema_version": generator.RESEARCH_EXTENSION_SCHEMA, "runime_policy_typo": {}}
        with self.assertRaisesRegex(ValueError, "unsupported runtime keys"):
            generator.merge_research_extension({}, extension)
        extension = json.loads((ASSETS / "photo_prompt_lighting_extension.json").read_text())
        extension["visual_semantics"][0]["candidate_ids"][0] = "missing_member"
        with self.assertRaisesRegex(ValueError, "candidate references"):
            generator.merge_research_extension({"slots": {}}, extension)
        broken = copy.deepcopy(self.data)
        broken["candidate_bundles"][0]["associated_profile_ids"] = ["unknown_profile"]
        with self.assertRaisesRegex(ValueError, "unknown visual profiles"):
            semantics.validate_bundle_references(broken, [])
        emotional = next(row for row in self.data["candidate_bundles"] if row["id"] == "wet_surface_light_reflection_owner_relation")
        self.assertIn("slot:lighting:neon", {row["id"] for row in emotional["member_candidates"]})
        self.assertNotIn("slot:light_type:neon", {row["id"] for row in emotional["member_candidates"]})

    def test_semantic_units_relations_and_canonical_links_reject_malformed_authored_data(self):
        for mutation in ("string_units", "string_dimensions", "unknown_relation_field", "empty_subject", "duplicate_relation", "canonical_cycle"):
            with self.subTest(mutation=mutation):
                entry = {"id": "sample", "concept_units": ["upper soft key"],
                         "relations": [{"id": "above", "type": "above", "subject": "key", "object": "fill"}]}
                if mutation == "string_units":
                    entry["concept_units"] = "upper soft key"
                elif mutation == "string_dimensions":
                    entry["affected_dimensions"] = "lighting"
                elif mutation == "unknown_relation_field":
                    entry["relations"][0]["privately_required"] = True
                elif mutation == "empty_subject":
                    entry["relations"][0]["subject"] = ""
                elif mutation == "duplicate_relation":
                    entry["relations"].append(copy.deepcopy(entry["relations"][0]))
                else:
                    entry["canonical_concept_id"] = "sample"
                with self.assertRaises(ValueError):
                    semantics.validate_candidate_entries({"slots": {"lighting": [entry]}}, generator.AUTHORIAL_CORE_V3_INTENT_LOCK_DIMENSIONS)

    def test_required_extension_loss_fails_before_dictionary_use(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "photo_prompt_tags.json"
            path.write_text(json.dumps({"candidate_semantic_policy": self.data["candidate_semantic_policy"]}))
            with self.assertRaisesRegex(ValueError, "required candidate extensions are missing"):
                generator.load_json(path)

    def test_maintenance_prose_is_external_and_hash_bound(self):
        count = 0
        for path in ASSETS.glob("*extension.json"):
            extension = json.loads(path.read_text())
            reference = extension.get("maintenance_ref")
            if not reference:
                continue
            count += 1
            record = json.loads((ROOT / "docs/research-evidence/photo-prompt/extension-maintenance" / (reference["record_id"] + ".json")).read_text())
            self.assertEqual(reference["sha256"], semantics.digest(record))
            self.assertNotIn("semantic_policy", extension)
            self.assertNotIn("representation_modes", extension)
            self.assertTrue(record["maintenance_only"])
        self.assertEqual(count, 12)
        serialized = json.dumps(self.pack())
        self.assertNotIn("maintenance_ref", serialized)
        self.assertNotIn("judgment_boundary", serialized)

    def test_multiword_relations_survive_v6_pack_overview_and_full_details(self):
        pack = self.pack()
        row = pack["slots"]["light_intensity"]["candidates"][0]
        self.assertIn("small key-fill brightness difference", row["concept_units"])
        self.assertEqual(row["relations"][0]["subject"], "key")
        self.assertEqual(row["relations"][0]["object"], "fill")
        self.assertNotIn("semantics", row["concept_terms"])
        self.assertFalse(any(tag.endswith("_visual_semantics") for tag in row["tags"]))
        overview = views.build_view(pack)
        views.verify_view(pack, overview)
        catalog = next(item for item in overview["candidate_catalog"] if item["id"] == row["id"])
        self.assertEqual(catalog["relations"], row["relations"])
        bundle = pack["candidate_bundles"]["candidates"][0]
        detail = views.build_view(pack, [bundle["id"]])
        self.assertEqual(detail["candidates"][0]["candidate"], bundle)
        views.verify_view(pack, detail)

    def test_missing_member_ineligible_member_internal_conflict_or_locked_scope_hides_bundle(self):
        for mutation in ("missing", "ineligible", "conflict", "locked"):
            with self.subTest(mutation=mutation):
                source = self.source_pack()
                first = next(iter(source["slots"].values()))["candidates"][0]
                if mutation == "missing":
                    source["slots"].pop(first["slot"])
                elif mutation == "ineligible":
                    first["applicability"]["status"] = "ineligible"
                elif mutation == "conflict":
                    first["conflicts_with"] = [self.bundle["member_candidates"][1]["id"]]
                else:
                    source["authorial_core"]["intent_lock"]["open_dimensions"].remove("lighting")
                self.assertEqual(semantics.public_bundles(self.data, source)["candidates"], [])

    def test_scope_ownership_preserves_distinct_locked_dimensions(self):
        policy = self.data["candidate_semantic_policy"]
        for slot, dimension in (("composition", "composition"), ("subject_framing", "framing"),
                                ("format", "format"), ("expression", "expression"),
                                ("hand_pose", "pose"), ("action", "action")):
            self.assertEqual(semantics.slot_dimensions(slot, policy), [dimension])
        self.assertEqual(semantics.slot_dimensions("unreviewed_slot", policy), [])
        self.assertEqual(semantics.slot_dimensions("prop", policy), [])

    def test_real_generator_builds_an_adoptable_bundle_with_full_view_and_audit(self):
        from tests.test_photo_authorship_policy import PhotoAuthorshipPolicyTests as fixture
        request = "An adult beauty portrait with an upper soft key and weaker lower return, clear facial shadows and a warm-neutral clean finish."
        raw = fixture.raw_core(("lighting", "color", "camera", "framing", "composition"))
        raw.update(source_request=request,
                   interpreted_intent="A clean adult beauty portrait with a vertically paired soft lighting system.",
                   subject="one adult seated portrait subject", setting="a quiet professional photographic studio",
                   event="the adult subject holds a still seated portrait pose",
                   visual_priorities=["upper key with weaker lower return", "natural facial tonal detail"],
                   baseline_prompt_en="An adult portrait subject sits comfortably in a photographic studio, their face turned slightly toward the camera. An upper soft key and weaker lower return retain clean facial shadows while two catchlights remain vertically separated. Warm-neutral color preserves the skin and ivory wardrobe detail. Gentle background falloff and clear midtones keep the eyes and the curved cheek surfaces prominent without flattening the light.",
                   interpretation_provenance=[{"term": "beauty portrait", "source_text": request,
                                               "basis": "request_context", "resolution": "The upper key and weaker lower return create a restrained adult studio portrait.", "sources": []}])
        for anchor in raw["intent_lock"]["semantic_anchors"]:
            anchor["source_text"] = request
            anchor["prompt_evidence"] = {"concept": "An upper soft key and weaker lower return", "subject": "An adult portrait subject", "event": "sits comfortably in a photographic studio"}[anchor["dimension"]]
        envelope = {"contract_version": "photo-request-envelope/v1", "provenance": "requesting_user", "request_id": "candidate-bundle-integration",
                    "request_text": request, "request_sha256": hashlib.sha256(request.encode()).hexdigest(),
                    "active_spans": [{"span_id": "topic", "start": 0, "end": len(request), "text": request}]}
        core = generator.normalize_authorial_core(raw, request_envelope=generator.normalize_request_envelope(envelope))
        data = v6.PhotoAuthorialCoreV6Tests().runtime_data()
        result = generator.generate_once(data, random.Random(919), None, ["en"], True, 12, True,
                                         selection_mode="rule", include_trace=True, concept_locks=[request],
                                         seed=919, creativity=0.0, authorial_core=core)
        pack = generator.build_candidate_pack(result, data, "v6")
        bundles = pack["candidate_bundles"]["candidates"]
        self.assertTrue(bundles, "the normal generator must expose a usable bundle, not only compile a dead catalog")
        bundle = bundles[0]
        detail = views.build_view(pack, [bundle["id"]])
        views.verify_view(pack, detail)
        self.assertFalse(self.check(pack))
        self.assertEqual(bundle["id"], "bundle:clean_beauty_clamshell")
        phrases = [
            "A softbox above the forehead illuminates the face while a weaker reflector returns light below the chin.",
            "Both sources share a frontal vertical axis through the nose.",
            "The large diffuse key and lower bounce spread gently around the jaw.",
            "A modest key-fill difference retains shadow detail beside the nostrils.",
            "The open eyes show one bright reflection above a second lower catchlight.",
            "Warm-neutral light preserves the natural skin color.",
            "The ivory fabric retains detailed whites while the face keeps clear midtones.",
        ]
        composed = {"candidate_interpretations": [{
            "candidate_id": bundle["id"], "artistic_interpretation": "Model the subject through gentle graduated surface detail.",
            "transformation": "Arrange the lights around the specific ivory wardrobe and facial contours.",
            "prompt_evidence": phrases[0],
            "component_evidence": {component["id"]: phrase for component, phrase in zip(bundle["components"], phrases)},
            "relation_evidence": {relation["id"]: phrases[0] for relation in bundle["relations"]},
        }]}
        prompt = raw["baseline_prompt_en"] + " " + " ".join(phrases)
        self.assertFalse(auditor.audit_candidate_interpretations(pack, composed, prompt, {bundle["id"]}, auditor.candidate_objects_from_pack(pack)))
        forged = copy.deepcopy(pack)
        altered = forged["candidate_bundles"]["candidates"][0]
        altered["components"][0]["concept_units"] = ["a front ring light instead of an upper key"]
        altered["source_contract_sha256"] = semantics.digest(semantics.bundle_source_material(altered))
        generator.candidate_pack_recompute_id(forged)
        self.assertTrue(self.check(forged), "rehashing a forged source claim must not replace source recomputation")
        blocked_data = copy.deepcopy(data)
        blocked_entry = generator.candidate_pack_slot_entry_by_id(blocked_data, "light_direction", "lit_clean_vertical_frontal_axis")
        blocked_entry["requires_primary_any_tags"] = ["unproven_external_role"]
        self.assertNotIn(bundle["id"], {row["id"] for row in generator.candidate_pack_candidate_bundles(blocked_data, pack)["candidates"]})
        full_composed = fixture.composed(pack)
        full_composed.update(composed, prompt_en=prompt, chosen_candidate_ids=[bundle["id"]], chosen_visual_concept_ids=[])
        full_composed["authored_slots"] = {
            "action": {"prompt_evidence": "their face turned slightly toward the camera", "artistic_rationale": "Preserve the frozen quiet portrait action."},
            "location": {"prompt_evidence": "An adult portrait subject sits comfortably in a photographic studio", "artistic_rationale": "Preserve the frozen studio and seated subject."},
        }
        for decision in full_composed["authorial_core_binding"]["authorial_decisions"]:
            decision["decision"] = decision["decision"].replace("teacup", "portrait")
            decision["rationale"] = "preserves the requested facial modeling and studio subject"
        for decision in full_composed["semantic_clarification_decisions"]:
            decision["rationale"] = "the frozen baseline preserves the requested adult studio portrait"
        full_audit = auditor.audit_composed_prompt(pack, full_composed)
        self.assertEqual(full_audit["status"], "pass", full_audit["failures"])
        self.integration_artifacts = {"pack": pack, "detail": detail,
                                      "selection_evidence": dict(composed, prompt_en=prompt, chosen_candidate_ids=[bundle["id"]]),
                                      "composed": full_composed, "composed-audit": full_audit}

    def test_selected_bundle_requires_every_component_and_relation_literal_evidence(self):
        pack = self.pack()
        bundle = pack["candidate_bundles"]["candidates"][0]
        evidence = [
            "A softbox above the forehead illuminates the face while a weaker reflector returns light below the chin.",
            "Both sources share a frontal vertical axis through the nose.",
            "The large diffuse key and lower bounce spread gently around the jaw.",
            "A modest key-fill difference retains shadow detail beside the nostrils.",
            "The open eyes show one bright reflection above a second lower catchlight.",
            "Warm-neutral light preserves the natural skin color.",
            "The ivory fabric retains detailed whites while the face keeps clear midtones.",
        ]
        phrase = " ".join(evidence)
        row = {"candidate_id": bundle["id"],
               "component_evidence": {item["id"]: text for item, text in zip(bundle["components"], evidence)},
               "relation_evidence": {item["id"]: evidence[0] for item in bundle["relations"]}}
        self.assertFalse(self.check(pack, [bundle["id"]], [row], phrase))
        for mutation in ("component_missing", "relation_missing", "nonliteral"):
            altered = copy.deepcopy(row)
            if mutation == "component_missing":
                altered["component_evidence"].pop(next(iter(altered["component_evidence"])))
            elif mutation == "relation_missing":
                altered["relation_evidence"].pop(next(iter(altered["relation_evidence"])))
            else:
                altered["relation_evidence"][next(iter(altered["relation_evidence"]))] = "A phrase that is absent."
            self.assertTrue(self.check(pack, [bundle["id"]], [altered], phrase), mutation)
        # Rejecting the bundle creates no new prompt or profile obligation.
        self.assertFalse(self.check(pack))

    def test_source_contract_or_scope_tampering_fails_even_after_pack_hash_recompute(self):
        for mutation in ("component", "relation", "scope", "profile_promotion", "member_eligibility"):
            with self.subTest(mutation=mutation):
                pack = self.pack()
                bundle = pack["candidate_bundles"]["candidates"][0]
                if mutation == "component":
                    bundle["components"].pop()
                elif mutation == "relation":
                    bundle["relations"][0]["subject"] = "fill"
                elif mutation == "scope":
                    pack["authorial_core"]["intent_lock"]["open_dimensions"].remove("lighting")
                elif mutation == "member_eligibility":
                    pack["slots"]["lighting"]["candidates"][0]["applicability"]["status"] = "ineligible"
                else:
                    bundle["profile_activation"] = "automatically_required"
                generator.candidate_pack_recompute_id(pack)
                self.assertTrue(self.check(pack))

    def test_v4_v5_token_surfaces_and_legacy_v6_are_not_reinterpreted(self):
        row = {"id": "slot:light_intensity:test", "label_en": "low key-fill difference with shadows still present", "tags": ["lighting"]}
        generator.candidate_pack_v4_project_candidate(row, salt="old")
        self.assertNotIn("concept_units", row)
        self.assertNotIn("semantic_surface_version", row)
        self.assertNotIn("low key-fill difference with shadows still present", row["concept_terms"])
        self.assertFalse(self.check({"contract_version": "photo-candidate-pack/v6"}))

    def test_canonical_street_link_and_storefront_label_keep_stable_ids(self):
        street = generator.candidate_pack_slot_entry_by_id(self.data, "genre", "street_photography")
        self.assertEqual(street["canonical_concept_id"], "street")
        self.assertEqual(generator.candidate_pack_slot_entry_by_id(self.data, "genre", "street")["en"], street["en"])
        storefront = generator.candidate_pack_slot_entry_by_id(self.data, "location", "convenience_store_night")
        store = generator.candidate_pack_slot_entry_by_id(self.data, "location", "late_night_convenience_store")
        self.assertIn("outside", storefront["en"])
        self.assertNotEqual(storefront["en"], store["en"])


if __name__ == "__main__":
    unittest.main()
