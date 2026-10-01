from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import compose_pack_view as view
import photo_candidate_context as candidate_context


def fixture():
    pack = {
        "contract_version": "photo-candidate-pack/v6", "pack_id": None,
        "authorial_core": {"baseline_prompt_en": "frozen visible meaning", "canonical_sha256": "a" * 64},
        "visual_obligations": {"evidence": ["mandatory same-frame relation"]},
        "semantic_clarification": {"candidates": [{"id": "meaning", "required_in_final_prompt": True, "prompt_evidence": "frozen visible meaning"}]},
        "negative_en": "defocus defect",
        "future_required_contract": {"arbitrary_new_gate": "must survive unchanged"},
        "visual_concept_candidates": {"candidates": [{
            "id": "optional:one", "concept_terms": ["glass", "reflection"],
            "applicability": {"status": "eligible"},
            "opt_in_contract": {"obligation": {"evidence": "optional exact evidence", "render_gates": ["optional_gate"]}},
        }]},
    }
    pack["pack_id"] = view.digest(pack)[:16]
    return pack


class PhotoComposerViewTests(unittest.TestCase):
    def test_unknown_requirements_and_required_meaning_remain_exact(self):
        pack = fixture()
        original = copy.deepcopy(pack)
        result = view.build_view([pack])
        for key in ["authorial_core", "visual_obligations", "semantic_clarification", "negative_en", "future_required_contract"]:
            self.assertEqual(result["requirements"][key], pack[key])
        self.assertEqual(pack, original)
        self.assertEqual(result["candidate_catalog"][0]["id"], "optional:one")
        view.verify_view(pack, result)

    def test_selected_candidate_recovers_exact_obligation_and_gates(self):
        pack = fixture()
        detail = view.build_view(pack, ["optional:one"])
        self.assertEqual(detail["candidates"][0]["candidate"], pack["visual_concept_candidates"]["candidates"][0])
        view.verify_view(pack, detail)
        detail["candidates"][0]["candidate"]["opt_in_contract"]["obligation"]["render_gates"] = []
        with self.assertRaises(ValueError):
            view.verify_view(pack, detail)

    def test_required_candidate_is_never_deferred(self):
        pack = fixture()
        row = pack["visual_concept_candidates"]["candidates"][0]
        row["required_in_final_prompt"] = True
        pack["pack_id"] = view.digest(dict(pack, pack_id=None))[:16]
        self.assertEqual(view.build_view(pack)["requirements"]["visual_concept_candidates"], pack["visual_concept_candidates"])

    def test_pack_and_view_mutations_are_rejected(self):
        pack = fixture()
        result = view.build_view(pack)
        result["requirements"]["negative_en"] = ""
        with self.assertRaises(ValueError):
            view.verify_view(pack, result)
        pack["negative_en"] = ""
        with self.assertRaises(ValueError):
            view.build_view(pack)

    def test_review_sources_preserve_exact_request_and_lock_ownership(self):
        pack = fixture()
        pack["authorial_core"].update({
            "source_request": "창문 빛만, 사람 없이.  Keep the ceramic bowl white.",
            "user_exclusions": ["사람 없이"],
            "user_definitions": [{"source_text": "창문 빛만", "meaning": "window light only"}],
            "intent_lock": {
                "locked_dimensions": ["subject", "event", "concept"],
                "open_dimensions": ["lighting", "appearance"],
                "semantic_anchors": [{"dimension": "appearance", "target": "main_subject",
                                      "property": "surface.color", "source_text": "Keep the ceramic bowl white.",
                                      "prompt_evidence": "the white ceramic bowl"}],
            },
        })
        pack["pack_id"] = view.digest(dict(pack, pack_id=None))[:16]
        overview = view.build_view(pack)
        self.assertEqual(overview["requirements"]["authorial_core"], pack["authorial_core"])
        self.assertEqual(overview["source_pack_sha256"], view.digest(pack))
        view.verify_view(pack, overview)

    def test_full_bundle_detail_cannot_drop_actor_or_relation_for_partial_use(self):
        pack = fixture()
        bundle = {
            "id": "bundle:reflected-interaction", "concept_units": ["two adults reflected together"],
            "components": [{"id": "first_actor"}, {"id": "second_actor"}],
            "relations": [{"id": "shared_reflection", "subject": "first_actor",
                           "object": "second_actor", "relation_type": "reflected_together"}],
            "context_prerequisites": {"people": "required"},
            "adoption": "atomic",
        }
        pack["candidate_bundles"] = {"candidates": [bundle]}
        pack["pack_id"] = view.digest(dict(pack, pack_id=None))[:16]
        detail = view.build_view(pack, [bundle["id"]])
        self.assertEqual(detail["candidates"][0]["candidate"], bundle)
        for field in ("components", "relations", "context_prerequisites", "adoption"):
            modified = copy.deepcopy(detail)
            del modified["candidates"][0]["candidate"][field]
            with self.assertRaises(ValueError):
                view.verify_view(pack, modified)
        self.assertEqual(pack["candidate_bundles"]["candidates"][0], bundle)

    def test_unknown_candidate_and_legacy_pack_are_rejected(self):
        with self.assertRaises(ValueError):
            view.build_view(fixture(), ["absent"])
        pack = fixture()
        pack["contract_version"] = "photo-candidate-pack/v5"
        with self.assertRaises(ValueError):
            view.build_view(pack)

    def test_overview_exposes_requirements_and_detail_recovers_exact_source(self):
        pack = fixture()
        candidate = pack["visual_concept_candidates"]["candidates"][0]
        candidate.update(candidate_context.compile_context(
            {"requires_any_tags": ["direct_flash_y2k_snapshot"]}, "slot:color:ordinary"))
        candidate.update(source_candidate_id="slot:color:ordinary", retrieval_status="returned",
                         contextual_status="unassessed", scene_retrieval_support=False)
        candidate["applicability"]["basis"] = "writable_scope"
        pack["pack_id"] = view.digest(dict(pack, pack_id=None))[:16]
        original = copy.deepcopy(pack)
        overview = view.build_view(pack)
        summary = overview["candidate_catalog"][0]
        for key in ("context_requirements", "context_prerequisites", "context_preflight",
                    "source_candidate_id", "retrieval_status", "scene_retrieval_support"):
            self.assertEqual(summary[key], candidate[key])
        detail = view.build_view(pack, [candidate["id"]])
        self.assertEqual(detail["candidates"][0]["candidate"], candidate)
        view.verify_view(pack, overview)
        view.verify_view(pack, detail)
        self.assertEqual(pack, original)


if __name__ == "__main__":
    unittest.main()
