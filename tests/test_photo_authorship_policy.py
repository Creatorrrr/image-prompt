from __future__ import annotations

from tests import photo_prompt_fixtures as current_fixtures

import copy
import hashlib
import random
import unittest
from unittest import mock

from tests import photo_prompt_fixtures as fixtures
from tests import test_photo_authorial_core_v6 as v6_fixtures


generator = fixtures.prompt_generator
auditor = fixtures.audit_composed_prompt

REQUEST = (
    "A blue porcelain teacup rests on a dark counter, with rising steam and "
    "rainlit window reflections."
)


class PhotoAuthorshipPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = v6_fixtures.PhotoAuthorialCoreV6Tests().runtime_data()
        cls.packs: dict[tuple[str, ...], dict] = {}

    @staticmethod
    def raw_core(opened: tuple[str, ...], version: str = "v3") -> dict:
        payload = fixtures.core(
            REQUEST, open_dimensions=opened
        )
        if version == "v3":
            payload.update(
                contract_version="photo-authorial-core/v3",
                semantic_assertions=[],
                request_lineage=None,
            )
        return payload

    @staticmethod
    def normalize(payload: dict) -> dict:
        envelope = generator.normalize_request_envelope(
            fixtures.envelope(REQUEST)
        )
        return generator.normalize_authorial_core(payload, request_envelope=envelope)

    def pack(self, opened: tuple[str, ...]) -> dict:
        if opened not in self.packs:
            core = self.normalize(self.raw_core(opened))
            result = current_fixtures.generate_once(
                self.data,
                random.Random(9100),
                None,
                ["en"],
                True,
                12,
                True,
                selection_mode="rule",
                include_trace=True,
                concept_locks=[REQUEST],
                seed=9100,
                creativity=0.0,
                authorial_core=core,
            )
            self.packs[opened] = generator.build_candidate_pack(result, self.data, "v6")
        return copy.deepcopy(self.packs[opened])

    @staticmethod
    def composed(pack: dict, *, legacy: bool = False) -> dict:
        core = pack["authorial_core"]
        lock = core["intent_lock"]
        decisions = [
            {
                "dimension": dimension,
                "decision": f"refine {dimension} around the teacup",
                "rationale": "keeps the requested material and steam readable",
            }
            for dimension in lock["open_dimensions"][:2]
        ] if legacy else []
        return {
            "pack_id": pack["pack_id"],
            "prompt_en": core["baseline_prompt_en"],
            "negative_en": pack["negative_en"],
            "chosen_candidate_ids": [],
            "chosen_visual_concept_ids": [],
            "composer": "agent",
            "embodiment_review": fixtures.composition_review(pack, core["baseline_prompt_en"]),
            "candidate_interpretations": [],
            "authorial_core_binding": {
                "source_authorial_core_sha256": core["canonical_sha256"],
                "source_intent_lock_sha256": lock["canonical_sha256"],
                "preserved_anchor_ids": [
                    row["anchor_id"] for row in lock["semantic_anchors"]
                ],
                "preserved_evidence": [
                    row["prompt_evidence"] for row in lock["semantic_anchors"]
                ] if legacy else [],
                "authorial_decisions": decisions,
            },
            "semantic_clarification_decisions": [
                {
                    "clarification_id": row["id"],
                    "decision": (
                        "applied" if row.get("required_in_final_prompt") else "rejected"
                    ),
                    "rationale": "the frozen baseline preserves the requested still life",
                    "prompt_evidence": lock["semantic_anchors"][0]["prompt_evidence"],
                }
                for row in pack["semantic_clarification"]["candidates"]
            ],
            "creative_augmentation_brief": {
                "decisions": [
                    {
                        "candidate_id": row["id"],
                        "decision": "rejected",
                        "rationale": "preserves the complete requested baseline",
                    }
                    for row in pack["creative_augmentation"]["candidates"]
                ]
            },
        }

    @staticmethod
    def core_failures(pack: dict, composed: dict) -> set[str]:
        return {
            row["check"]
            for row in auditor.audit_authorial_core(
                pack, composed, composed["prompt_en"]
            )
        }

    def test_zero_one_and_multiple_open_dimensions_pass_full_audit(self):
        for opened in ((), ("framing",), ("framing", "lighting", "camera")):
            with self.subTest(opened=opened):
                pack = self.pack(opened)
                composed = self.composed(pack)
                policy = pack["authorial_composition"]["authorship_policy"]
                self.assertEqual(policy["contract_version"], "photo-authorial-authorship-policy/v2")
                self.assertEqual(policy["minimum_authorial_decisions"], 0)
                self.assertEqual(policy["minimum_preserved_evidence_phrases"], 0)
                self.assertEqual(policy["allowed_dimensions"], list(opened))
                self.assertEqual(pack["authorial_core"]["intent_lock"]["open_dimensions"], list(opened))
                audit = auditor.audit_composed_prompt(pack, composed)
                self.assertEqual(audit["status"], "pass", audit["failures"])
                self.assertEqual(composed["prompt_en"], pack["authorial_core"]["baseline_prompt_en"])
                self.assertEqual(composed["authorial_core_binding"]["authorial_decisions"], [])
                self.assertEqual(composed["authorial_core_binding"]["preserved_evidence"], [])

    def test_closed_dimensions_and_missing_anchor_still_fail(self):
        pack = self.pack(())
        composed = self.composed(pack)
        composed["authorial_core_binding"]["authorial_decisions"] = [
            {
                "dimension": "subject",
                "decision": "replace the teacup with a vase",
                "rationale": "an unrequested substitution changes the primary subject",
            }
        ]
        self.assertIn("intent_lock_authorial_dimensions", self.core_failures(pack, composed))

        composed = self.composed(pack)
        composed["authorial_core_binding"]["preserved_anchor_ids"].pop()
        self.assertIn("intent_lock_anchor_binding", self.core_failures(pack, composed))

        composed = self.composed(pack)
        phrase = pack["authorial_core"]["intent_lock"]["semantic_anchors"][0]["prompt_evidence"]
        composed["prompt_en"] = composed["prompt_en"].replace(phrase, "unrelated glossy ornament")
        self.assertIn("intent_lock_prompt_evidence", self.core_failures(pack, composed))

    def test_optional_decisions_remain_distinct_substantive_and_explicit(self):
        pack = self.pack(("framing", "lighting", "camera"))
        composed = self.composed(pack, legacy=True)
        decisions = composed["authorial_core_binding"]["authorial_decisions"]
        decisions[1]["dimension"] = decisions[0]["dimension"]
        self.assertIn("authorial_core_decisions", self.core_failures(pack, composed))

        composed = self.composed(pack, legacy=True)
        composed["authorial_core_binding"]["authorial_decisions"][0]["rationale"] = "good"
        self.assertIn("authorial_core_decisions", self.core_failures(pack, composed))

        pack = self.pack(())
        for invalid in (None, {}, "", [None]):
            with self.subTest(invalid=invalid):
                composed = self.composed(pack)
                composed["authorial_core_binding"]["authorial_decisions"] = invalid
                self.assertIn("authorial_core_decisions", self.core_failures(pack, composed))
        composed = self.composed(pack)
        del composed["authorial_core_binding"]["authorial_decisions"]
        self.assertIn("authorial_core_decisions", self.core_failures(pack, composed))

    def test_optional_preserved_evidence_is_still_well_formed_and_literal(self):
        pack = self.pack(("composition",))
        for invalid in (None, {}, "", [None], [""], [42], ["invented photographic phrase"]):
            with self.subTest(invalid=invalid):
                composed = self.composed(pack)
                composed["authorial_core_binding"]["preserved_evidence"] = invalid
                self.assertIn("authorial_core_evidence", self.core_failures(pack, composed))
        composed = self.composed(pack)
        del composed["authorial_core_binding"]["preserved_evidence"]
        self.assertIn("authorial_core_evidence", self.core_failures(pack, composed))

    def test_unbound_staging_can_be_replaced_without_rewriting_the_core(self):
        pack = self.pack(("camera", "composition"))
        original_core = copy.deepcopy(pack["authorial_core"])
        composed = self.composed(pack)
        self.assertIn("shallow focus", composed["prompt_en"])
        composed["prompt_en"] = composed["prompt_en"].replace(
            "shallow focus", "depth extending from the cup to the rainlit room"
        )
        composed["authorial_core_binding"]["authorial_decisions"] = [{
            "dimension": "camera",
            "decision": "replace the shallow focus with legible room depth",
            "rationale": "lets the still life draw its presence from the surrounding room",
        }]
        composed["embodiment_review"] = fixtures.composition_review(pack, composed["prompt_en"])
        audit = auditor.audit_composed_prompt(pack, composed)
        self.assertEqual(audit["status"], "pass", audit["failures"])
        self.assertEqual(pack["authorial_core"], original_core)

        # The looser final-pass quotas cannot remove a requester-owned meaning.
        phrase = original_core["intent_lock"]["semantic_anchors"][0]["prompt_evidence"]
        composed["prompt_en"] = composed["prompt_en"].replace(phrase, "plain empty counter")
        self.assertIn("intent_lock_prompt_evidence", self.core_failures(pack, composed))

    def test_v3_requires_explicit_freedom_without_weakening_lock_validation(self):
        malformed = self.raw_core(())
        del malformed["intent_lock"]["open_dimensions"]
        with self.assertRaisesRegex(ValueError, "explicit open_dimensions list"):
            self.normalize(malformed)
        for opened, error in (
            (("framing", "framing"), "distinct open_dimensions"),
            (("subject",), "both locked and open"),
            (("invented_dimension",), "unknown dimensions"),
        ):
            with self.subTest(opened=opened):
                with self.assertRaisesRegex(ValueError, error):
                    self.normalize(self.raw_core(opened))
        missing_anchor = self.raw_core(())
        missing_anchor["intent_lock"]["semantic_anchors"].pop()
        with self.assertRaisesRegex(ValueError, "every locked dimension"):
            self.normalize(missing_anchor)

    def test_policy_deletion_or_forgery_cannot_grant_more_freedom(self):
        original = self.pack(("framing", "lighting", "camera"))
        mutations = []
        missing_policy = copy.deepcopy(original)
        del missing_policy["authorial_composition"]["authorship_policy"]
        mutations.append(missing_policy)
        missing_binding = copy.deepcopy(original)
        del missing_binding["authorial_composition"]["core_binding_contract"]
        mutations.append(missing_binding)
        forged = copy.deepcopy(original)
        policy = forged["authorial_composition"]["authorship_policy"]
        policy["minimum_authorial_decisions"] = 1
        del policy["canonical_sha256"]
        policy["canonical_sha256"] = generator.canonical_json_sha256(policy)
        binding = forged["authorial_composition"]["core_binding_contract"]
        binding["minimum_authorial_decisions"] = 1
        binding["source_authorship_policy_sha256"] = policy["canonical_sha256"]
        mutations.append(forged)
        wrong_dimensions = copy.deepcopy(original)
        wrong_dimensions["authorial_composition"]["authorship_policy"]["allowed_dimensions"].append("subject")
        mutations.append(wrong_dimensions)
        wrong_evidence = copy.deepcopy(original)
        policy = wrong_evidence["authorial_composition"]["authorship_policy"]
        policy["minimum_preserved_evidence_phrases"] = 1
        del policy["canonical_sha256"]
        policy["canonical_sha256"] = generator.canonical_json_sha256(policy)
        binding = wrong_evidence["authorial_composition"]["core_binding_contract"]
        binding["minimum_preserved_evidence_phrases"] = 1
        binding["source_authorship_policy_sha256"] = policy["canonical_sha256"]
        mutations.append(wrong_evidence)
        for index, pack in enumerate(mutations):
            with self.subTest(mutation=index):
                # Rehash the outer pack to isolate semantic recomputation from
                # the ordinary pack-integrity check.
                generator.candidate_pack_recompute_id(pack)
                composed = self.composed(pack)
                audit = auditor.audit_composed_prompt(pack, composed)
                self.assertIn("authorial_authorship_policy_contract", {row["check"] for row in audit["failures"]})

    def test_missing_current_policy_is_rejected(self):
        pack = self.pack(())
        del pack["authorial_composition"]["authorship_policy"]
        generator.candidate_pack_recompute_id(pack)
        self.assertIn("authorial_authorship_policy_contract", self.core_failures(pack, self.composed(pack)))

    def test_serialized_v1_policy_is_rejected(self):
        pack = self.pack(())
        pack["authorial_composition"]["authorship_policy"]["contract_version"] = "photo-authorial-authorship-policy/v1"
        generator.candidate_pack_recompute_id(pack)
        self.assertIn("authorial_authorship_policy_contract", self.core_failures(pack, self.composed(pack)))

    def test_obsolete_pack_and_core_versions_are_rejected(self):
        for version in ("v2", "v3", "v4", "v5"):
            with self.subTest(pack_version=version):
                pack = self.pack(())
                pack["contract_version"] = f"photo-candidate-pack/{version}"
                self.assertIn("authorial_authorship_policy_contract", self.core_failures(pack, self.composed(pack)))
        for version in ("v1", "v2"):
            raw = self.raw_core(())
            raw["contract_version"] = f"photo-authorial-core/{version}"
            with self.assertRaisesRegex(ValueError, "contract_version"):
                self.normalize(raw)

    def test_audit_does_not_call_producer_policy_or_core_normalizers(self):
        pack = self.pack(())
        composed = self.composed(pack)
        with (
            mock.patch.object(
                generator,
                "normalize_authorial_core",
                side_effect=AssertionError("producer used by audit"),
            ),
            mock.patch.object(
                generator,
                "normalize_intent_lock",
                side_effect=AssertionError("producer used by audit"),
            ),
            mock.patch.object(
                generator,
                "candidate_pack_compose_current",
                side_effect=AssertionError("producer used by audit"),
            ),
        ):
            self.assertEqual(self.core_failures(pack, composed), set())

    def test_shared_canonical_bytes_and_vocabulary_are_unchanged(self):
        payload = {"z": [True, 1], "a": "한글"}
        expected = hashlib.sha256('{"a":"한글","z":[true,1]}'.encode("utf-8")).hexdigest()
        self.assertEqual(generator.canonical_json_sha256(payload), expected)
        self.assertEqual(auditor.canonical_json_sha256(payload), expected)
        self.assertIs(generator.canonical_json_sha256, auditor.canonical_json_sha256)
        self.assertIs(generator.INTENT_LOCK_DIMENSIONS, auditor.INTENT_LOCK_DIMENSIONS)
        self.assertIs(
            generator.AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS,
            auditor.AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS,
        )
        core = {"user_exclusions": ["people or animals"]}
        for term, expected_allowed in (
            ("low resolution", True),
            ("people or animals", True),
            ("people", False),
            ("no contact", False),
        ):
            with self.subTest(term=term):
                for consumer in (generator, auditor):
                    self.assertEqual(
                        consumer.authorial_negative_term_allowed(term, core, identity_preservation_enabled=False),
                        expected_allowed,
                    )


if __name__ == "__main__":
    unittest.main()
