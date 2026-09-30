from __future__ import annotations

import copy
import unittest

from tests import photo_prompt_fixtures as fixtures

generator = fixtures.prompt_generator
auditor = fixtures.audit_composed_prompt


def fixture():
    request = "Two adult friends exchange a book at a station."
    raw = fixtures.core(
        request,
        interpreted_intent="The requested exchange is staged with gloves and a central crop.",
        subject="two adult friends",
        setting="a busy train station",
        event="one offers a book to the other",
        visual_priorities=("gloved hands", "a central crop"),
        baseline_prompt_en=(
            "Two adult friends meet at a busy train station. One offers a book to the other, "
            "and the recipient reaches for that same book. Their gloved hands meet around "
            "the cover in a central crop. Soft window light falls across the worn paper "
            "and the station activity continues behind the exchange."
        ),
        anchor_evidence=(
            "the recipient reaches for that same book",
            "Two adult friends",
            "One offers a book to the other",
        ),
        open_dimensions=("appearance", "pose", "composition", "lighting", "camera"),
    )
    raw["semantic_assertions"] = [{
        "assertion_id": "handoff", "dimension": "event", "polarity": "required",
        "source_span_ids": ["scope_1"], "affected_dimensions": ["event"],
        "axes": {"interaction": "book_exchange"},
        "evidence": {"target_phrase": "the recipient reaches for that same book"},
    }]
    envelope = generator.normalize_request_envelope(fixtures.envelope(request))
    core = generator.normalize_authorial_core(raw, request_envelope=envelope)
    contract = generator.candidate_pack_semantic_clarification(
        {}, {"provenance": {"authorial_core": core}}, {}, None, None,
        visual_profile_resolution={"hits": []},
    )
    pack = {"authorial_core": core, "semantic_clarification": contract}
    composed = {"semantic_clarification_decisions": [{
        "clarification_id": row["id"], "decision": "applied",
        "rationale": "The same requested exchange remains visible.",
        "prompt_evidence": "One offers a book to the other",
    } for row in contract["candidates"]]}
    return pack, composed


class PhotoAuthorialDirectionScopeTests(unittest.TestCase):
    def test_required_projection_contains_meaning_not_incidental_direction(self):
        pack, _ = fixture()
        contract = pack["semantic_clarification"]
        meaning = contract["candidates"][0]
        self.assertEqual(set(meaning["meaning_components"]), {
            "the recipient reaches for that same book",
            "Two adult friends",
            "One offers a book to the other",
        })
        self.assertTrue(meaning["required_in_final_prompt"])
        self.assertFalse(meaning["revisable"])
        direction = contract["authorial_direction"]
        self.assertEqual(direction["visual_priorities"], ["gloved hands", "a central crop"])
        self.assertFalse(direction["creates_additional_locks"])

    def test_changing_only_the_initial_direction_does_not_change_requester_duties(self):
        pack, _ = fixture()
        before = generator.authorial_meaning_clarification(pack["authorial_core"])
        changed = copy.deepcopy(pack["authorial_core"])
        changed["interpreted_intent"] = "A handoff with bare hands near the edge of the frame."
        changed["visual_priorities"] = ["bare hands", "an asymmetric crop"]
        self.assertEqual(before, generator.authorial_meaning_clarification(changed))
        self.assertNotEqual(
            generator.authorial_direction_context(changed),
            generator.authorial_direction_context(pack["authorial_core"]),
        )

    def test_clarification_allows_open_staging_change_without_demoting_meaning(self):
        pack, composed = fixture()
        prompt = pack["authorial_core"]["baseline_prompt_en"].replace(
            "gloved hands", "bare hands"
        ).replace("a central crop", "an asymmetric crop")
        self.assertEqual(auditor.audit_semantic_clarification(pack, composed, prompt), [])
        removed_meaning = prompt.replace("One offers a book to the other", "They stand quietly")
        self.assertIn("semantic_clarification_binding", {
            row["check"] for row in auditor.audit_semantic_clarification(
                pack, composed, removed_meaning
            )
        })

    def test_mixed_direction_cannot_be_promoted_into_required_clarification(self):
        pack, composed = fixture()
        for mutation in ("add_choice", "drop_duty", "lock_direction", "omit_direction"):
            changed = copy.deepcopy(pack)
            contract = changed["semantic_clarification"]
            if mutation == "add_choice":
                contract["candidates"][0]["meaning_components"].append("gloved hands")
            elif mutation == "drop_duty":
                contract["candidates"][0]["meaning_components"].pop()
            elif mutation == "lock_direction":
                contract["authorial_direction"]["creates_additional_locks"] = True
            else:
                contract.pop("authorial_direction")
            with self.subTest(mutation=mutation):
                self.assertIn("semantic_clarification_authority", {
                    row["check"] for row in auditor.audit_semantic_clarification(
                        changed, composed, pack["authorial_core"]["baseline_prompt_en"]
                    )
                })


if __name__ == "__main__":
    unittest.main()
