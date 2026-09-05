from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "skills/photo-prompt-image-generator/scripts"
sys.path.insert(0, str(SCRIPT_DIR))
import compose_pack_view as view


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

    def test_unknown_candidate_and_legacy_pack_are_rejected(self):
        with self.assertRaises(ValueError):
            view.build_view(fixture(), ["absent"])
        pack = fixture()
        pack["contract_version"] = "photo-candidate-pack/v5"
        with self.assertRaises(ValueError):
            view.build_view(pack)


if __name__ == "__main__":
    unittest.main()
