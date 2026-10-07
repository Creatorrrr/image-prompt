"""Grounded reasons, polarity and relation signatures without core revision."""
import copy
import json
import unittest
from pathlib import Path

from tests import test_photo_character_response_concepts as concept_fixtures
import prompt_generator as pg


class PhotoMeaningDiagnosticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = concept_fixtures.PhotoCharacterResponseConceptTests()
        concept_fixtures.PhotoCharacterResponseConceptTests.setUpClass()
        cls.data = cls.fixture.data

    def evaluate(self, mutation=lambda c: None, profile=None):
        core = self.fixture.normalize_core()
        mutation(core)
        frozen = copy.deepcopy(core)
        result = pg.evaluate_character_response_profile(core, self.data, profile or self.fixture.profile)
        self.assertEqual(core, frozen)
        return result

    def test_absent_value_and_unrecognized_text_are_distinct(self):
        absent = self.evaluate(lambda c: c["semantic_assertions"][0]["axes"].pop("surface_affect"))
        unknown = self.evaluate(lambda c: c["semantic_assertions"][0]["axes"].update(surface_affect="unregistered affect description"))
        self.assertIn("surface_affect", absent["missing_axes"])
        self.assertNotIn("surface_affect", unknown["missing_axes"])
        self.assertIn("surface_affect", unknown["unrecognized_axes"])
        self.assertEqual(unknown["status"], "incomplete")

    def test_same_operator_different_members_is_not_operator_absence(self):
        def change(c):
            next(r for r in c["semantic_assertions"][0]["relations"] if r["operator"] == "same_target")["members"].pop()
        result = self.evaluate(change)
        self.assertEqual(result["missing_relation_operators"], [])
        self.assertEqual(result["unmet_relations"][0]["code"], "relation_members_mismatch")

    def test_relation_absence_order_and_endpoints(self):
        for operator, code in [("same_target", "relation_operator_absent"), ("temporal_order", "relation_order_mismatch"), ("contrasts", "relation_endpoints_mismatch")]:
            def change(c):
                rows = c["semantic_assertions"][0]["relations"]
                row = next(r for r in rows if r["operator"] == operator)
                if operator == "same_target": rows.remove(row)
                elif operator == "temporal_order": row["first"], row["then"] = row["then"], row["first"]
                else: row["left"], row["right"] = row["right"], row["left"]
            with self.subTest(operator=operator):
                self.assertIn(code, [r["code"] for r in self.evaluate(change)["unmet_relations"]])

    def test_member_order_remains_immaterial(self):
        result = self.evaluate(lambda c: next(r for r in c["semantic_assertions"][0]["relations"] if r["operator"] == "same_target")["members"].reverse())
        self.assertEqual(result["status"], "consistent")

    def test_lexical_positive_context_failure_is_not_a_resolved_other_sense(self):
        profile = {"id": "generic", "activation": {"context_disambiguation": {"required_with_authorial_core": True, "any_terms": ["window reflection"], "exclude_if_any_terms": ["dictionary entry"]}}}
        missing = pg.visual_profile_context_diagnostics(profile, "gentle light", has_authorial_core_context=True)
        excluded = pg.visual_profile_context_diagnostics(profile, "dictionary entry", has_authorial_core_context=True)
        self.assertEqual(missing["checks"][0]["code"], "positive_context_unrecognized")
        self.assertEqual(missing["checks"][0]["evidence"], [])
        self.assertEqual(excluded["checks"][0]["code"], "context_exclusion_term_matched")
        self.assertEqual(excluded["checks"][0]["evidence"], ["dictionary entry"])

    def test_polarity_and_phrase_boundaries(self):
        for value in ["not openly affectionate", "never openly affectionate", "openly affectionateではない", "공개적인 애정이 아니다"]:
            with self.subTest(value=value):
                match = pg.character_axis_value_matches(self.data, "surface_affect", value)
                self.assertNotIn("open_warmth", match["classes"])
                self.assertIn("open_warmth", match["negated_classes"])
        self.assertNotIn("open_warmth", pg.character_axis_value_classes(self.data, "surface_affect", "openly indifferent and elsewhere affectionate"))
        match = pg.character_axis_value_matches(self.data, "surface_affect", "openly affectionate; not openly affectionate")
        self.assertIn("open_warmth", match["ambiguous_classes"])
        self.assertNotIn("open_warmth", match["classes"])

    def test_exclusion_evidence_is_literal_and_bounded(self):
        result = self.evaluate(lambda c: c["semantic_assertions"][0]["axes"].update(surface_affect="hostile"))
        check = next(r for r in result["diagnostics"]["checks"] if r.get("axis") == "surface_affect")
        self.assertEqual(check["code"], "axis_excluded_class")
        self.assertEqual(result["status"], "conflicting")
        self.assertEqual(check["raw_value"], ["hostile"])
        self.assertEqual(check["evidence"][0]["text"], "hostile")

    def test_diagnostics_preserve_original_spacing_and_offsets(self):
        raw = "  openly   affectionate  "
        result = self.evaluate(lambda c: c["semantic_assertions"][0]["axes"].update(surface_affect=raw))
        check = next(r for r in result["diagnostics"]["checks"] if r.get("axis") == "surface_affect")
        self.assertEqual(check["raw_value"], [raw])
        hit = next(r for r in check["evidence"] if r["class_id"] == "open_warmth")
        self.assertEqual(hit["text"], raw[hit["start"]:hit["end"]])
        self.assertEqual(hit["text"], "openly   affectionate")

    def test_baseline_decisions_preserved_with_more_precise_reasons(self):
        path = Path(__file__).resolve().parents[1] / "tests/fixtures/photo_prompt/meaning_diagnostics_v1.json"
        for case in json.loads(path.read_text())["cases"]:
            with self.subTest(case=case["case"]):
                actual = pg.evaluate_character_response_profile(case["core"], self.data, self.fixture.profile)
                self.assertEqual(actual["status"], case["result"]["status"])

    def test_reviewed_multilingual_expressions_and_unregistered_holdout(self):
        for value in ["affectionate warmth directed at the same duet partner", "같은 상대에게 향하는 다정한 애정", "同じ相手への優しい愛情"]:
            with self.subTest(value=value):
                self.assertIn("open_warmth", pg.character_axis_value_classes(self.data, "surface_affect", value))
        self.assertEqual(pg.character_axis_value_classes(self.data, "surface_affect", "her unfamiliar relational signal"), set())
        self.assertEqual(pg.character_axis_value_classes(self.data, "surface_affect", "not only openly affectionate"), set())

    def test_advisory_axis_does_not_relax_other_profile_or_required_relations(self):
        profile = self.fixture.yandere_profile
        def change(c):
            assertion = c["semantic_assertions"][0]
            assertion["axes"].update(surface_affect="affectionate warmth", underlying_affiliation="possessive", affect_leak_intentionality="absent")
            assertion["relations"] = copy.deepcopy(profile["required_relations"])
        result = self.evaluate(change, profile)
        self.assertEqual(result["status"], "consistent")
        advisory = next(r for r in result["diagnostics"]["checks"] if r.get("axis") == "affect_leak_intentionality")
        self.assertFalse(advisory["blocking_effect"])
        def different_target(c):
            change(c)
            next(r for r in c["semantic_assertions"][0]["relations"] if r["operator"] == "same_target")["members"].remove("relationship_target")
        self.assertEqual(self.evaluate(different_target, profile)["status"], "incomplete")
        self.assertIn("affect_leak_intentionality", self.fixture.profile["axis_requirements"])
        self.assertIn("affect_leak_intentionality", self.fixture.kuudere_profile["axis_requirements"])

    def test_composed_audit_rejects_fabricated_profile_diagnostic(self):
        import audit_composed_prompt as auditor
        from unittest import mock
        core = self.fixture.normalize_core()
        row = pg.authorial_meaning_clarification(core)
        pack = {"authorial_core": core, "semantic_clarification": {
            "contract_version": pg.SEMANTIC_CLARIFICATION_CONTRACT_VERSION, "affected_by_creativity": False,
            "affected_by_seed": False, "authorial_direction": pg.authorial_direction_context(core), "candidates": [row]},
            "character_response": {"advisory_retrieval": {"candidates": [{
                "candidate_type": "concept_profile", "candidate_id": "character_response_concept:" + self.fixture.profile["id"],
                "semantic_consistency": pg.evaluate_character_response_profile(core, self.data, self.fixture.profile)}]}}}
        composed = {"semantic_clarification_decisions": [{"clarification_id": row["id"], "decision": "applied",
            "rationale": "preserve frozen meaning", "prompt_evidence": core["baseline_prompt_en"]}]}
        with mock.patch.object(auditor, "_audit_source_data", return_value=self.data):
            baseline = auditor.audit_semantic_clarification(pack, composed, core["baseline_prompt_en"])
            self.assertNotIn("character_response_diagnostics", {r["check"] for r in baseline})
            pack["character_response"]["advisory_retrieval"]["candidates"][0]["semantic_consistency"]["diagnostics"]["checks"][0]["code"] = "fabricated_reason"
            changed = auditor.audit_semantic_clarification(pack, composed, core["baseline_prompt_en"])
            self.assertIn("character_response_diagnostics", {r["check"] for r in changed})
