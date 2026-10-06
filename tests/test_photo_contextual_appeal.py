from __future__ import annotations

import copy
import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/photo-prompt-image-generator/scripts"))
import audit_composed_prompt as auditor
import compose_pack_view as view
import photo_contextual_appeal as contextual
import photo_candidate_context as candidate_context
import photo_creative_controls as controls
import prompt_generator as generator


def fixture():
    source = "An adult woman offers a handwritten letter in a white dress."
    snapshot = controls.resolve(source, context={"subject_category": "human"},
                                overrides={"sensual": 1, "fetish": 1}, seed=7)
    core = {
        "contract_version": "photo-authorial-core/v3", "source_request": source,
        "creative_controls_sha256": snapshot["canonical_sha256"],
        "baseline_prompt_en": "An adult woman offers a handwritten letter wearing a white corset dress.",
        "interpreted_intent": "A corset frames the letter gesture.",
        "request_binding": {"active_spans": [{"text": source}]},
        "intent_lock": {"contract_version": "photo-intent-lock/v2", "canonical_sha256": "a" * 64,
                        "locked_dimensions": ["subject", "event"], "open_dimensions": [],
                        "semantic_anchors": [
                            {"dimension": "appearance", "target": "main_subject", "property": "wardrobe.color", "prompt_evidence": "white dress"},
                            {"dimension": "appearance", "target": "main_subject", "property": "wardrobe.garment_type", "prompt_evidence": "white dress"}]},
    }
    def entry(eid, label, prop):
        return {"id": eid, "en": label, "ko": label, "weight": 1,
                "concept_units": [label], "affected_dimensions": ["appearance"],
                "affected_properties": [{"dimension": "appearance", "target": "main_subject", "property": prop}]}
    data = {"slots": {"garment_detail": [
        entry("seam", "A flowing dress seam follows posture and material drape", "wardrobe.construction.seam"),
        entry("cuff", "A deliberate glove cuff gesture presents the fastening in adult fashion", "accessories.gloves"),
        entry("whole", "A red leather corset dress leads sensual fashion", "wardrobe"),
    ]},  "candidate_semantic_policy": {"slot_dimensions": {"garment_detail": ["appearance"]}},
        generator.QUALITY_LAYERS_DATA_KEY: {"adult_appeal": {
            "contextual_retrieval": {"contract_version": contextual.VERSION},
            # These old admission gates must not affect the bound v6 path.
            "entry_min_intensity": {"seam": 3, "cuff": 3},
            "axes": {},
        }}}
    result = {"provenance": {"prompt_id": "test", "creative_controls": snapshot,
                              "adult_appeal": {"axes": {axis: {"intensity": 1} for axis in contextual.AXES}}}}
    return data, core, result


class ContextualAppealTests(unittest.TestCase):
    def adult(self, data=None, core=None, result=None):
        default_data, default_core, default_result = fixture()
        return generator.candidate_pack_contextual_adult_appeal(
            data or default_data, result or default_result, {}, authorial_core=core or default_core)

    def test_untagged_candidates_at_level_one_ignore_old_inventory_and_thresholds(self):
        adult = self.adult()
        self.assertNotIn("one_accepted_detail_per_active_axis", adult["composition_requirements"])
        for axis in contextual.AXES:
            rows = adult["axes"][axis]["candidate_inventory"]
            self.assertEqual({row["entry_id"] for row in rows}, {"seam", "cuff"})
            self.assertTrue(all(row["contextual_status"] == "unassessed" for row in rows))
            self.assertTrue(all("minimum_intensity" not in row for row in rows))
            self.assertEqual(adult["contextual_retrieval"]["axes"][axis]["lanes"], {"coherence": "keyword", "alternatives": "keyword"})

    def test_partial_locks_preserve_whole_garment_and_admit_real_detail(self):
        data, core, result = fixture()
        adult = self.adult(data, core, result)
        self.assertEqual(auditor.audit_adult_appeal_dimension_scope({"contract_version": "photo-candidate-pack/v6", "authorial_core": core}, adult), [])
        self.assertNotIn("whole", {row["entry_id"] for axis in adult["axes"].values() for row in axis["candidate_inventory"]})
        data["slots"]["garment_detail"][0]["affected_properties"][0]["property"] = "wardrobe.color"
        changed = self.adult(data, core, result)
        self.assertNotIn("seam", {row["entry_id"] for axis in changed["axes"].values() for row in axis["candidate_inventory"]})

    def test_alternative_query_does_not_copy_agent_outfit_and_exclusions_stay_negative(self):
        _, core, result = fixture()
        core["user_exclusions"] = ["gloves"]
        core["request_binding"]["active_spans"][0]["text"] += " no gloves"
        queries = contextual.queries(core, result["provenance"]["creative_controls"]["definitions"],
                                     {axis: 1 for axis in contextual.AXES}, generator.authorial_core_retrieval_text)
        for lanes in queries.values():
            self.assertIn("corset", lanes["coherence"])
            self.assertNotIn("corset", lanes["alternatives"])
            self.assertNotIn("gloves", lanes["alternatives"])

    def test_source_order_does_not_choose_prefix(self):
        data, core, result = fixture()
        first = self.adult(data, core, result)
        data["slots"]["garment_detail"].reverse()
        self.assertEqual(first, self.adult(data, core, result))

    def test_runtime_reports_semantic_use_only_for_matching_queries_and_vectors(self):
        data, core, result = fixture()
        queries = contextual.queries(core, result["provenance"]["creative_controls"]["definitions"],
                                     {axis: 1 for axis in contextual.AXES}, generator.authorial_core_retrieval_text)
        data[contextual.QUERY_CACHE] = {"test": {"queries": queries, "vectors": {
            axis: {lane: [1., 0.] for lane in queries[axis]} for axis in contextual.AXES}}}
        data[generator.SEMANTIC_INDEX_DATA_KEY] = {"entries": {
            "slot:garment_detail:seam": {"vector": [1., 0.]},
            "slot:garment_detail:cuff": {"vector": [0., 1.]}}}
        adult = self.adult(data, core, result)
        self.assertEqual(adult["contextual_retrieval"]["axes"]["sensual"]["lanes"]["alternatives"], "hybrid")
        data[contextual.QUERY_CACHE]["test"]["queries"] = {}
        self.assertEqual(self.adult(data, core, result)["contextual_retrieval"]["axes"]["sensual"]["lanes"]["alternatives"], "keyword")

    def test_embedding_runtime_uses_one_query_per_call_and_binds_all_active_lanes(self):
        data, core, result = fixture()
        snapshot = result["provenance"]["creative_controls"]
        with patch.object(generator, "embed_single_semantic_text", return_value=[1., 0.]) as embed:
            generator.prepare_contextual_appeal_queries(data, result, core, snapshot,
                                                       {"embedding_model": "test", "embedding_dimensions": 2})
            self.assertEqual(embed.call_count, 4)
        cached = data[contextual.QUERY_CACHE]["test"]
        self.assertEqual(set(cached["vectors"]), set(contextual.AXES))
        self.assertTrue(all(isinstance(call.args[0], str) for call in embed.call_args_list))
        self.assertNotIn("corset", cached["queries"]["fetish"]["alternatives"])
        data.pop(contextual.QUERY_CACHE)
        with patch.object(generator, "embed_single_semantic_text", side_effect=AssertionError("keyword run must not embed")):
            generator.prepare_contextual_appeal_queries(data, result, core, snapshot, None)
        self.assertNotIn(contextual.QUERY_CACHE, data)

    def test_unsatisfied_hard_facet_guard_is_not_relaxed_by_corpus_search(self):
        data, core, result = fixture()
        data["slots"]["garment_detail"][0]["hard_guards"] = {"requires_facets": ["subject:nonhuman"]}
        adult = self.adult(data, core, result)
        self.assertNotIn("seam", {row["entry_id"] for axis in adult["axes"].values() for row in axis["candidate_inventory"]})

    def test_axis_inventory_has_catalog_and_exact_detail_lookup_outside_creative_sample(self):
        adult = self.adult()
        pack = {"contract_version": "photo-candidate-pack/v6", "pack_id": None, "adult_appeal": adult}
        pack["pack_id"] = view.digest(pack)[:16]
        overview = view.build_view(pack)
        ids = adult["contextual_retrieval"]["review_candidate_ids"]
        self.assertTrue(set(ids) <= {row["id"] for row in overview["candidate_catalog"]})
        detail = view.build_view(pack, [ids[0]])
        self.assertEqual(detail["candidates"][0]["candidate"]["id"], ids[0])
        view.verify_view(pack, overview)
        with self.assertRaisesRegex(ValueError, "unsupported composer view"):
            view.build_view(pack, version="photo-composer-view/v1")

    def test_review_requires_context_and_comparison_but_allows_rejection_and_uncertainty(self):
        adult = self.adult()
        ids = adult["contextual_retrieval"]["review_candidate_ids"]
        self.assertTrue(contextual.audit_review(adult, {}, set()))
        brief = {"contextual_review": [{"candidate_id": cid, "reading": "uncertain", "reason": "Ordinary practical use remains equally plausible in this scene."} for cid in ids],
                 "contextual_comparison": "Keep the baseline at the same strengths: the proposed glove gesture would divert attention from the letter, and the seam contributes no new presence."}
        self.assertEqual(contextual.audit_review(adult, brief, set()), [])
        self.assertTrue(contextual.audit_review(adult, brief, {ids[0]}))
        brief["contextual_review"][0]["reading"] = "potential"
        self.assertTrue(contextual.audit_review(adult, brief, set()))
        brief["contextual_review"][0]["proposed_application"] = "Keep the dress and use a hand contact to connect fabric drape to the letter."
        self.assertEqual(contextual.audit_review(adult, brief, {ids[0]}), [])
        old = copy.deepcopy(adult)
        old.pop("contextual_retrieval")
        self.assertEqual(contextual.audit_review(old, {}, set()), [])

    def test_context_limits_are_not_positive_search_text(self):
        row = {"id": "ordinary", "en": "ordinary glove", "concept_units": ["practical wrist fastening"],
               "contextual_usage": {"limits": "fetish uniform school", "ordinary": "work glove"}}
        self.assertNotIn("fetish", generator.semantic_text_for_entry(row, "wearable_accessory"))
        self.assertNotIn("fetish", str(generator.semantic_bm25f_fields_for_entry(row, "wearable_accessory")))

    def test_short_relation_queries_keep_request_action_without_agent_outfit_or_control_syntax(self):
        _, core, result = fixture()
        core["request_binding"]["active_spans"].append({"text": "sensual=3, fetish=3"})
        core["intent_lock"]["semantic_anchors"].append({"dimension": "event",
            "source_text": "offers a handwritten letter", "prompt_evidence": "offers a handwritten letter"})
        queries = contextual.queries(core, result["provenance"]["creative_controls"]["definitions"],
                                     {axis: 3 for axis in contextual.AXES}, generator.authorial_core_retrieval_text)
        for lanes in queries.values():
            self.assertIn("offers a handwritten letter", lanes["relation_event"])
            self.assertNotIn("corset", lanes["relation_event"])
            self.assertNotIn("sensual=3", " ".join(lanes.values()))
            self.assertLess(len(lanes["relation_event"].split()), 60)

    def test_role_and_setting_effects_require_explicit_open_scope(self):
        lock = {"locked_dimensions": ["subject", "event"], "open_dimensions": []}
        for dimension in ("role", "setting", "relationship", "timing"):
            self.assertNotIn(dimension, contextual.allowed_dimensions(lock))
            lock["open_dimensions"] = [dimension]
            self.assertIn(dimension, contextual.allowed_dimensions(lock))
            lock["locked_dimensions"].append(dimension)
            self.assertNotIn(dimension, contextual.allowed_dimensions(lock))
            lock["locked_dimensions"].remove(dimension)



    def test_scene_preference_breaks_equal_generic_hits_without_claiming_applicability(self):
        def row(key, words):
            return {"source_candidate_id": key, "search_fields": {"labels": [words]},
                    "visual_text": [words], "expression_scope": "portrayal_or_scene_relation"}
        rows = [row("a", "adult shared scene glass pouring"), row("z", "adult shared scene letter handoff")]
        ranked, trace = contextual.rank_candidates(rows, {"coherence": "adult shared scene"},
            policy=generator.SEMANTIC_BM25F_POLICY, scene_query="letter handoff", limit=2)
        self.assertEqual(ranked[0]["source_candidate_id"], "z")
        self.assertTrue(ranked[0]["scene_retrieval_support"])
        self.assertEqual(ranked[0]["contextual_status"], "unassessed")
        self.assertIn("not_applicability_proof", trace["scene_reranking"])


class AdultSubjectPhraseThresholdTests(unittest.TestCase):
    def scenario(self, *, sensual=None, fetish=0, context=None):
        data, core, result = fixture()
        source = core["source_request"].replace("An adult woman", "A woman")
        snapshot = controls.resolve(source, context=context or {"subject_category": "human"},
                                    overrides=None if sensual is None else {"sensual": sensual, "fetish": fetish}, seed=7)
        core.update(source_request=source, creative_controls_sha256=snapshot["canonical_sha256"],
                    baseline_prompt_en=core["baseline_prompt_en"].replace("An adult woman", "A woman"))
        core["request_binding"]["active_spans"] = [{"text": source}]
        result["provenance"]["creative_controls"] = snapshot
        adult = generator.candidate_pack_contextual_adult_appeal(data, result, {}, authorial_core=core)
        brief = {
            "agency_phrase": "offers a handwritten letter",
            "axes": {axis: {"intensity": adult["axes"][axis]["intensity"], "realization": "baseline",
                            "affected_dimensions": [], "artistic_interpretation": "Retain the dress and letter gesture.",
                            "prompt_evidence": "white corset dress"} for axis in contextual.AXES},
            "blend": adult["blend"],
            "contextual_review": [{"candidate_id": cid, "reading": "irrelevant", "reason": "Preserve the letter gesture."}
                                  for cid in adult["contextual_retrieval"]["review_candidate_ids"]],
            "contextual_comparison": "At the same strengths, retain the dress and letter gesture rather than competing details.",
        }
        pack = {"contract_version": "photo-candidate-pack/v6", "authorial_core": core,
                "creative_controls": snapshot, "adult_appeal": adult}
        composed = {"prompt_en": core["baseline_prompt_en"], "adult_appeal_brief": brief}
        return pack, composed

    def audit(self, pack, composed):
        failures, _ = auditor.audit_adult_appeal(pack, composed, composed["prompt_en"], set(), {})
        return failures

    def test_default_human_prompt_needs_no_adult_word(self):
        pack, composed = self.scenario()
        self.assertEqual(pack["adult_appeal"]["axes"]["sensual"]["intensity"], 1)
        self.assertNotIn("adult", composed["prompt_en"])
        self.assertEqual(self.audit(pack, composed), [])
        composed["adult_appeal_brief"].pop("agency_phrase")
        self.assertEqual({row["check"] for row in self.audit(pack, composed)}, {"adult_appeal_agency"})

    def test_only_sensual_two_and_three_require_the_adult_word(self):
        for sensual in range(4):
            for fetish in range(4):
                with self.subTest(sensual=sensual, fetish=fetish):
                    pack, composed = self.scenario(sensual=sensual, fetish=fetish)
                    requirements = pack["adult_appeal"]["composition_requirements"]
                    self.assertEqual(requirements["adult_subject_phrase_required"], sensual >= 2)
                    self.assertEqual(requirements["explicit_adult_original_subject"], sensual >= 2)
                    self.assertEqual({row["check"] for row in self.audit(pack, composed)},
                                     {"adult_appeal_adult_subject"} if sensual >= 2 else set())

    def test_high_sensual_checks_the_word_and_its_literal_binding(self):
        for sensual in (2, 3):
            with self.subTest(sensual=sensual):
                pack, composed = self.scenario(sensual=sensual)
                pack["adult_appeal"]["composition_requirements"]["adult_subject_phrase_required"] = False
                pack["adult_appeal"]["composition_requirements"]["explicit_adult_original_subject"] = False
                composed["prompt_en"] += " The woman is thirty years old."
                brief = composed["adult_appeal_brief"]
                for phrase in ("", "The woman is thirty years old.", "The woman is an ADULT."):
                    brief["adult_subject_phrase"] = phrase
                    self.assertEqual({row["check"] for row in self.audit(pack, composed)}, {"adult_appeal_adult_subject"})
                composed["prompt_en"] += " The woman is an ADULT."
                self.assertEqual(self.audit(pack, composed), [])

    def test_optional_subject_evidence_still_needs_literal_binding(self):
        for sensual in (0, 1):
            with self.subTest(sensual=sensual):
                pack, composed = self.scenario(sensual=sensual, fetish=3)
                brief = composed["adult_appeal_brief"]
                brief["adult_subject_phrase"] = "A woman"
                self.assertEqual(self.audit(pack, composed), [])
                brief["adult_subject_phrase"] = "An adult woman"
                self.assertEqual({row["check"] for row in self.audit(pack, composed)}, {"adult_appeal_adult_subject"})
                brief.pop("adult_subject_phrase")
                self.assertEqual(self.audit(pack, composed), [])

    def test_nonsexual_context_uses_effective_sensual_intensity(self):
        pack, composed = self.scenario(sensual=3, fetish=3,
                                       context={"subject_category": "human", "explicit_nonsexual": True})
        self.assertEqual(pack["creative_controls"]["controls"]["sensual"]["value"], 3)
        self.assertEqual(pack["adult_appeal"]["axes"]["sensual"]["intensity"], 0)
        self.assertFalse(pack["adult_appeal"]["composition_requirements"]["adult_subject_phrase_required"])
        self.assertEqual(self.audit(pack, composed), [])


class FinalCandidateContextTests(unittest.TestCase):
    """Use an ordinary authored lighting candidate, not an appeal membership flag."""

    def scenario(self, *, slot="color", entry_id="lit_direct_flash_neutral_cool_balance",
                 asset="photo_prompt_lighting_extension.json", quality=None):
        data, core, result = fixture()
        path = Path(__file__).resolve().parents[1] / "skills/photo-prompt-image-generator/assets" / asset
        entry = next(row for row in json.loads(path.read_text())["slots"][slot]
                     if row["id"] == entry_id)
        data["slots"] = {slot: [entry]}
        dimensions = ["color"] if slot == "color" else ["action", "pose"]
        data["candidate_semantic_policy"]["slot_dimensions"] = {slot: dimensions}
        if quality:
            data[generator.QUALITY_LAYERS_DATA_KEY]["applicability_guards"] = quality
        adult = generator.candidate_pack_contextual_adult_appeal(data, result, {}, authorial_core=core)
        candidate = adult["axes"]["sensual"]["candidate_inventory"][0]
        brief = {"adult_subject_phrase": "An adult woman",
                 "axes": {"sensual": {"affected_dimensions": [*dimensions, "lighting"]}},
                 "contextual_review": [
                     {"candidate_id": cid, "reading": "irrelevant", "reason": "Keep the baseline."}
                     for cid in adult["contextual_retrieval"]["review_candidate_ids"]],
                 "contextual_comparison": "Preserve the letter and dress while comparing coherent lighting treatments."}
        review = next(row for row in brief["contextual_review"] if row["candidate_id"] == candidate["id"])
        review.update(reading="potential", proposed_application="Use the ordinary flash balance to connect the figure with the scene.")
        return data, core, adult, candidate, brief, review

    def witness(self, candidate, phrase, *, origin="authored", dimensions=None, rid=None, fact=None):
        requirement = next(row for row in candidate["context_prerequisites"]["requirements"]
                           if rid is None or row["id"] == rid)
        return {"requirement_id": requirement["id"], "fact": fact or requirement["values"][0],
                "state": "present", "prompt_evidence": phrase,
                "reason": "The final scene realizes the declared context.", "origin": origin,
                "affected_dimensions": dimensions if dimensions is not None else ["lighting"],
                "affected_properties": []}

    def audit(self, adult, core, candidate, brief, prompt):
        return contextual.audit_review(adult, brief, {candidate["id"]}, prompt_en=prompt,
                                       core=core, subject_category="human")

    def test_human_prerequisite_does_not_require_an_adult_phrase(self):
        for fact, supported in (("human", True), ("subject:human", True), ("adult", False), ("subject:adult", False)):
            with self.subTest(fact=fact):
                source_id = "slot:garment_detail:human_scope"
                candidate = {"id": "human_scope", "source_candidate_id": source_id,
                             **candidate_context.compile_context({"for_any": [fact]}, source_id)}
                failures = candidate_context.audit_context(
                    candidate, {"requirement_evidence": []}, prompt_en="A woman offers a letter.",
                    core={}, brief={}, subject_category="human", allowed=set())
                self.assertEqual(bool(failures), not supported)

    def test_search_scope_and_final_conditions_are_distinct(self):
        _, core, adult, candidate, brief, _ = self.scenario()
        self.assertEqual(candidate["retrieval_status"], "returned")
        self.assertEqual(candidate["applicability"]["basis"], "writable_scope")
        self.assertEqual(candidate["context_preflight"]["status"], "unassessed")
        self.assertNotIn("direct_flash_y2k_snapshot", core["baseline_prompt_en"])
        self.assertEqual(candidate["context_requirements"], {"requires_any_tags": ["direct_flash_y2k_snapshot"]})
        self.assertTrue(self.audit(adult, core, candidate, brief, core["baseline_prompt_en"]))
        for row in brief["contextual_review"]:
            row["reading"] = "irrelevant"
        self.assertEqual(contextual.audit_review(adult, brief, set()), [])

    def test_new_final_context_can_support_adoption_without_initial_tags(self):
        _, core, adult, candidate, brief, review = self.scenario()
        phrase = "Direct on-camera flash casts a hard-edged shadow behind her against the wall"
        review["requirement_evidence"] = [self.witness(candidate, phrase)]
        self.assertEqual(self.audit(adult, core, candidate, brief, core["baseline_prompt_en"] + " " + phrase), [])
        # Evidence in the draft cannot certify a final realization that omits it.
        core["baseline_prompt_en"] += " " + phrase
        self.assertTrue(self.audit(adult, core, candidate, brief, "An adult woman in a white dress offers a letter."))

    def test_short_real_scene_phrases_are_supported(self):
        _, core, adult, candidate, brief, review = self.scenario()
        review["requirement_evidence"] = [self.witness(candidate, "direct flash")]
        self.assertEqual(self.audit(adult, core, candidate, brief, core["baseline_prompt_en"] + " Photograph with direct flash."), [])
        glove = {"id": "ordinary-glove-detail", "axis": "sensual", "source_candidate_id": "slot:garment_detail:ordinary",
                 **candidate_context.compile_context({"requires_any_tags": ["cotton_gloves"]}, "slot:garment_detail:ordinary")}
        witness = self.witness(glove, "cotton gloves", dimensions=["appearance"])
        witness["affected_properties"] = [{"dimension": "appearance", "target": "main_subject", "property": "accessories.gloves"}]
        brief["axes"]["sensual"]["affected_dimensions"] = ["appearance"]
        self.assertEqual(candidate_context.audit_context(glove, {"requirement_evidence": [witness]},
                         prompt_en="She wears cotton gloves.", core=core, brief=brief,
                         subject_category="human", allowed=contextual.allowed_dimensions(core["intent_lock"])), [])

    def test_retained_context_must_be_literal_in_both_baseline_and_final(self):
        _, core, adult, candidate, brief, review = self.scenario()
        core["baseline_prompt_en"] += " Photograph with direct flash."
        review["requirement_evidence"] = [self.witness(candidate, "direct flash", origin="retained", dimensions=[])]
        self.assertEqual(self.audit(adult, core, candidate, brief, core["baseline_prompt_en"]), [])
        core["baseline_prompt_en"] = core["baseline_prompt_en"].replace("direct flash", "diffuse daylight")
        self.assertTrue(self.audit(adult, core, candidate, brief, core["baseline_prompt_en"] + " direct flash"))

    def test_new_context_respects_dimension_and_property_locks(self):
        _, core, adult, candidate, brief, review = self.scenario()
        phrase = "Direct flash casts a compact shadow behind her"
        review["requirement_evidence"] = [self.witness(candidate, phrase)]
        prompt = core["baseline_prompt_en"] + " " + phrase
        core["intent_lock"]["locked_dimensions"].append("lighting")
        self.assertTrue(self.audit(adult, core, candidate, brief, prompt))
        core["intent_lock"]["locked_dimensions"].remove("lighting")
        review["requirement_evidence"][0]["affected_properties"] = [
            {"dimension": "lighting", "target": "main_subject", "property": "wardrobe.color"}]
        self.assertTrue(self.audit(adult, core, candidate, brief, prompt))

    def test_machine_tag_and_pending_context_cannot_certify_adoption(self):
        _, core, adult, candidate, brief, review = self.scenario()
        tag = candidate["context_prerequisites"]["requirements"][0]["values"][0]
        review["requirement_evidence"] = [self.witness(candidate, tag)]
        self.assertTrue(self.audit(adult, core, candidate, brief, core["baseline_prompt_en"] + " " + tag))
        review["requirement_evidence"] = [self.witness(candidate, "direct flash")]
        for state in ("pending", "unsupported"):
            with self.subTest(state=state):
                review["requirement_evidence"][0]["state"] = state
                failures = self.audit(adult, core, candidate, brief, core["baseline_prompt_en"] + " direct flash")
                self.assertIn(state, {row.get("status") for row in failures})

    def test_primary_requirement_uses_new_open_context_but_not_an_unopened_relation(self):
        _, core, adult, candidate, brief, review = self.scenario(slot="action",
            entry_id="des_longing_incomplete_reach_action", asset="photo_prompt_desire_extension.json")
        phrase = "Her free hand reaches toward the photograph beyond a closed glass panel, stopping before contact while the visible gap keeps that target inaccessible"
        core["intent_lock"]["open_dimensions"] = ["relationship"]
        brief["axes"]["sensual"]["affected_dimensions"] = ["action", "pose", "relationship"]
        review["requirement_evidence"] = [self.witness(candidate, phrase, dimensions=["action", "pose", "relationship"])]
        prompt = core["baseline_prompt_en"] + " " + phrase
        self.assertEqual(self.audit(adult, core, candidate, brief, prompt), [])
        core["intent_lock"]["open_dimensions"] = []
        self.assertTrue(self.audit(adult, core, candidate, brief, prompt))

    def test_derived_quality_guards_keep_source_and_any_semantics(self):
        quality = json.loads((Path(__file__).resolve().parents[1] /
            "skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json").read_text())
        guard = next(row for row in quality["applicability_guards"]
                     if row["id"] == "underwater_modifier_requires_primary_context")
        data, core, result = fixture()
        data["slots"]["garment_detail"][0]["tags"] = ["underwater"]
        data[generator.QUALITY_LAYERS_DATA_KEY]["applicability_guards"] = [guard]
        adult = generator.candidate_pack_contextual_adult_appeal(data, result, {}, authorial_core=core)
        candidate = next(row for row in adult["axes"]["sensual"]["candidate_inventory"] if row["entry_id"] == "seam")
        contract = candidate["context_prerequisites"]
        self.assertEqual(contract["quality_layer_sources"], [{"id": guard["id"], "requires_primary_any_tags": sorted(guard["requires_primary_any_tags"])}])
        self.assertEqual(contract["requirements"][0]["operator"], "any")
        self.assertEqual(contract["requirements"][0]["sources"][0]["kind"], "quality_guard")
        # A matching source tag triggers a guard; it does not satisfy the guard.
        self.assertTrue(candidate_context.audit_context(candidate, {}, prompt_en=core["baseline_prompt_en"],
            core=core, brief={}, subject_category="human", allowed=contextual.allowed_dimensions(core["intent_lock"])))
        core["intent_lock"]["open_dimensions"] = ["setting"]
        brief = {"axes": {"sensual": {"affected_dimensions": ["appearance", "setting"]}}}
        witness = self.witness(candidate, "water surface", fact="water", dimensions=["setting"])
        pending = dict(witness, fact="ocean", state="pending")
        self.assertEqual(candidate_context.audit_context(candidate, {"requirement_evidence": [witness, pending]},
            prompt_en="She floats below the water surface.", core=core, brief=brief, subject_category="human",
            allowed=contextual.allowed_dimensions(core["intent_lock"])), [])

    def test_all_and_exclusion_require_explicit_supported_final_evidence(self):
        _, core, adult, candidate, brief, review = self.scenario()
        candidate.update(candidate_context.compile_context({
            "requires_any_tags": ["direct_flash_y2k_snapshot"],
            "requires_all_tags": ["wall_shadow", "neutral_skin"],
            "exclude_any_tags": ["color_shifted_skin"]}, candidate["source_candidate_id"]))
        phrase = "Direct flash leaves a compact wall shadow while the natural skin remains color-neutral"
        prompt = core["baseline_prompt_en"] + " " + phrase
        review["requirement_evidence"] = [self.witness(candidate, "Direct flash", rid="entry:any")]
        self.assertTrue(self.audit(adult, core, candidate, brief, prompt))
        review["requirement_evidence"].extend([
            self.witness(candidate, "a compact wall shadow", rid="entry:all", fact="wall_shadow"),
            self.witness(candidate, "natural skin", rid="entry:all", fact="neutral_skin")])
        self.assertTrue(self.audit(adult, core, candidate, brief, prompt))
        absent = self.witness(candidate, "skin remains color-neutral", rid="entry:exclude", fact="color_shifted_skin")
        absent["state"] = "absent"
        review["requirement_evidence"].append(absent)
        self.assertEqual(self.audit(adult, core, candidate, brief, prompt), [])
        absent["state"] = "present"
        self.assertTrue(self.audit(adult, core, candidate, brief, prompt))

    def test_sampled_and_canonical_paths_keep_original_metadata(self):
        _, core, adult, candidate, _, _ = self.scenario()
        original = copy.deepcopy(candidate)
        pack = {"authorial_core": core, "adult_appeal": adult}
        sample = generator.candidate_pack_creative_augmentation(pack, {})
        self.assertTrue(sample["candidates"])
        pack["creative_augmentation"] = sample
        for row in sample["candidates"]:
            source = auditor.candidate_objects_from_pack({"adult_appeal": adult})[row["id"]]
            for field in candidate_context.PRESERVED_FIELDS:
                self.assertEqual(row.get(field), source.get(field), field)
        self.assertEqual(contextual.audit_context_copies(adult, sample["candidates"]), [])
        row = sample["candidates"][0]
        row.pop("context_requirements")
        row["affected_dimensions"] = []
        self.assertTrue(contextual.audit_context_copies(adult, sample["candidates"]))
        canonical = auditor.candidate_objects_from_pack(pack)[row["id"]]
        self.assertTrue(canonical["context_requirements"])
        self.assertEqual(canonical["affected_dimensions"], ["color"])
        self.assertEqual(candidate, original)
        legacy = copy.deepcopy(pack)
        for axis in legacy["adult_appeal"]["axes"].values():
            for source in axis["candidate_inventory"]:
                source.pop("context_prerequisites")
        self.assertTrue(auditor.candidate_objects_from_pack(legacy)[row["id"]]["context_requirements"])

    def test_rehashed_missing_condition_and_missing_current_contract_fail(self):
        _, core, adult, candidate, brief, _ = self.scenario()
        contract = candidate["context_prerequisites"]
        contract["requirements"] = []
        contract["canonical_sha256"] = candidate_context.digest({key: value for key, value in contract.items()
                                                                 if key != "canonical_sha256"})
        self.assertTrue(self.audit(adult, core, candidate, brief, core["baseline_prompt_en"]))
        candidate.pop("context_prerequisites")
        failures = self.audit(adult, core, candidate, brief, core["baseline_prompt_en"])
        self.assertIn("adult_contextual_metadata", {row["check"] for row in failures})


if __name__ == "__main__":
    unittest.main()
