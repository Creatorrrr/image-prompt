from __future__ import annotations

import copy
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/photo-prompt-image-generator/scripts"))
import audit_composed_prompt as auditor
import compose_pack_view as view
import photo_contextual_appeal as contextual
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
    ]}, "presets": [], "candidate_semantic_policy": {"slot_dimensions": {"garment_detail": ["appearance"]}},
        generator.QUALITY_LAYERS_DATA_KEY: {"adult_appeal": {
            "contextual_retrieval": {"contract_version": contextual.VERSION},
            # These old admission gates must not affect the bound v6 path.
            "entry_min_intensity": {"seam": 3, "cuff": 3},
            "inventory_preset_id": "missing", "axes": {},
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


if __name__ == "__main__":
    unittest.main()
