"""Configuration proves a value, never the clothing chosen to express it."""
from __future__ import annotations

from tests import photo_prompt_fixtures as current_fixtures

import contextlib
import copy
import hashlib
import io
import random
import unittest

from tests import test_photo_initial_creative_controls as initial_fixtures
import audit_composed_prompt as auditor
import photo_creative_controls as controls
import prompt_generator as generator


class ControlSpanOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initial_fixtures.InitialDirectionIntegrationTests.setUpClass()
        cls.original = initial_fixtures.InitialDirectionIntegrationTests.raw

    def inputs(self, tail="sensual=3, fetish=3"):
        raw = copy.deepcopy(self.original)
        topic = raw["source_request"]
        request = topic + "\n" + tail
        raw["source_request"] = request
        envelope = generator.normalize_request_envelope({
            "contract_version": "photo-request-envelope/v1", "provenance": "requesting_user",
            "request_id": "control-span", "request_text": request,
            "request_sha256": hashlib.sha256(request.encode()).hexdigest(),
            "active_spans": [{"span_id": "topic", "start": 0, "end": len(topic), "text": topic},
                             {"span_id": "settings", "start": len(topic) + 1, "end": len(request), "text": tail}],
        })
        snapshot = controls.resolve(request, context={"subject_category": "human"},
                                    overrides={"sensual": 3, "fetish": 3}, seed=9)
        raw["creative_controls_sha256"] = snapshot["canonical_sha256"]
        return raw, envelope, snapshot

    def normalize(self, raw, envelope, snapshot):
        return generator.normalize_authorial_core(raw, request_envelope=envelope,
                                                  creative_control_snapshot=snapshot)

    def test_config_only_span_needs_no_visual_anchor_and_survives_audit(self):
        raw, envelope, snapshot = self.inputs()
        core = self.normalize(raw, envelope, snapshot)
        self.assertEqual(core["source_request"], envelope["request_text"])
        self.assertEqual(core["request_binding"]["active_spans"], envelope["active_spans"])
        self.assertEqual(core["intent_lock"]["semantic_anchors"], raw["intent_lock"]["semantic_anchors"])
        self.assertTrue(auditor.authorial_core_intent_contract_valid(
            core, minimum_open_dimensions=0, creative_control_snapshot=snapshot))
        self.assertTrue(auditor.authorial_core_interpretation_contract_valid(core, creative_control_snapshot=snapshot))
        self.assertFalse(auditor.authorial_core_intent_contract_valid(core, minimum_open_dimensions=0))

    def test_control_spans_survive_pack_composition_and_retrieval_hash_audit(self):
        raw, envelope, snapshot = self.inputs()
        core = self.normalize(raw, envelope, snapshot)
        data = initial_fixtures.InitialDirectionIntegrationTests.data
        result = current_fixtures.generate_once(data, random.Random(9), None, ["en"], True, 12, True,
            selection_mode="rule", include_trace=True, seed=9,
            authorial_core=core, creative_control_snapshot=snapshot)
        pack = generator.build_candidate_pack(result, data, "v6")
        composing = initial_fixtures.InitialDirectionIntegrationTests()
        composing.pack = pack
        composed = composing.composed()
        for axis in composed["adult_appeal_brief"]["axes"].values():
            axis["intensity"] = 3
            # One realization may support both controls; no separate prop or
            # mandatory extra detail is needed just to satisfy the auditor.
            axis["prompt_evidence"] = "a softly draped neckline"
        composed["adult_appeal_brief"]["blend"]["emphasis"] = "balanced"
        composed["adult_appeal_brief"]["contextual_comparison"] = "Retain the window portrait at 3/3; optional alternatives would divert the established gesture."
        report = auditor.audit_composed_prompt(pack, composed)
        self.assertEqual(report["status"], "pass", report["failures"])

    def test_control_source_cannot_lock_agent_outfit_even_if_literal_evidence_exists(self):
        for source in ("sensual=3, fetish=3", "sensual", "fetish=3"):
            raw, envelope, snapshot = self.inputs()
            raw["intent_lock"]["locked_dimensions"].append("sexual_tone")
            raw["intent_lock"]["open_dimensions"] = [d for d in raw["intent_lock"]["open_dimensions"] if d != "sexual_tone"]
            raw["baseline_prompt_en"] += " A corset-like bodice has silver rings."
            raw["intent_lock"]["semantic_anchors"].append({"anchor_id": "false_outfit", "source_text": source,
                "dimension": "sexual_tone", "prompt_evidence": "A corset-like bodice has silver rings"})
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, "not grounded"):
                self.normalize(raw, envelope, snapshot)

    def test_mixed_span_keeps_each_visual_fragment_and_explicit_property(self):
        raw, envelope, snapshot = self.inputs("sensual=3, her red scarf; fetish=3, she waves")
        visual, _ = controls.split_request_spans(envelope, snapshot)
        self.assertEqual([row["text"] for row in visual[1:]], ["her red scarf", "she waves"])
        for fragment in visual:
            self.assertEqual(envelope["request_text"][fragment["start"]:fragment["end"]], fragment["text"])
        with self.assertRaisesRegex(ValueError, "semantic-anchor coverage"):
            self.normalize(raw, envelope, snapshot)
        raw["baseline_prompt_en"] += " Her red scarf hangs loosely as she waves gently."
        raw["intent_lock"]["semantic_anchors"].append({"anchor_id": "scarf", "source_text": "her red scarf",
            "dimension": "appearance", "target": "main_subject", "property": "accessories.scarf.color",
            "prompt_evidence": "Her red scarf"})
        with self.assertRaisesRegex(ValueError, "semantic-anchor coverage.*visual2"):
            self.normalize(raw, envelope, snapshot)
        if "action" not in raw["intent_lock"]["open_dimensions"]:
            raw["intent_lock"]["open_dimensions"].append("action")
        raw["intent_lock"]["semantic_anchors"].append({"anchor_id": "wave", "source_text": "she waves",
            "dimension": "action", "target": "main_subject", "property": "hands.gesture",
            "prompt_evidence": "she waves gently"})
        for term in ("her red scarf", "she waves"):
            raw["interpretation_provenance"].append({"term": term, "source_text": term, "basis": "request_context",
                "resolution": "Preserve this separately requested visible feature", "sources": []})
        raw["semantic_assertions"].append({"assertion_id": "scarf_detail", "dimension": "appearance",
            "polarity": "advisory", "source_span_ids": ["settings"], "axes": {"color": "red"},
            "evidence": {"color_phrase": "Her red scarf"}, "affected_dimensions": ["appearance"]})
        core = self.normalize(raw, envelope, snapshot)
        self.assertTrue(auditor.authorial_core_intent_contract_valid(
            core, minimum_open_dimensions=0, creative_control_snapshot=snapshot))
        self.assertTrue(auditor.authorial_core_interpretation_contract_valid(core, creative_control_snapshot=snapshot))
        self.assertTrue(auditor.authorial_core_v3_semantic_contract_valid(core, creative_control_snapshot=snapshot))
        self.assertIn("Her red scarf", auditor.authorial_required_prompt_evidence({"authorial_core": core}, {}))

    def test_missing_stale_or_mismatched_settings_do_not_exempt_spans(self):
        raw, envelope, snapshot = self.inputs()
        with self.assertRaises(ValueError):
            self.normalize(raw, envelope, None)
        wrong = controls.resolve(raw["source_request"], context={"subject_category": "human"}, seed=9)
        raw["creative_controls_sha256"] = wrong["canonical_sha256"]
        with self.assertRaisesRegex(ValueError, "frozen override"):
            self.normalize(raw, envelope, wrong)
        for tail in ("sensual=3, sensual=2", "sensual=true", "sensual=4", "sensual=3foo"):
            raw, envelope, snapshot = self.inputs(tail)
            with self.subTest(tail=tail), self.assertRaises(ValueError):
                self.normalize(raw, envelope, snapshot)

    def test_span_name_does_not_grant_configuration_status(self):
        raw, envelope, snapshot = self.inputs("her red scarf")
        with self.assertRaisesRegex(ValueError, "semantic-anchor coverage.*settings"):
            self.normalize(raw, envelope, snapshot)

    def test_quoted_image_text_is_not_configuration_or_removed_from_search(self):
        _, envelope, _ = self.inputs('a sign reads "sensual=3, fetish=3"')
        visual, assignments = controls.split_request_spans(envelope)
        self.assertEqual(assignments, [])
        self.assertEqual(visual, envelope["active_spans"])
        text = 'a sign reads "sensual=3, fetish=3", sensual=1'
        self.assertIn('"sensual=3, fetish=3"', controls.strip_assignments(text))
        self.assertNotIn('sensual=1', controls.strip_assignments(text))

    def test_pure_setting_span_cannot_supply_a_visual_assertion(self):
        raw, envelope, snapshot = self.inputs()
        raw["semantic_assertions"].append({"assertion_id": "not_a_requirement", "dimension": "appearance",
            "polarity": "advisory", "source_span_ids": ["settings"], "axes": {"fabric": "draped"},
            "evidence": {"fabric_phrase": "softly draped neckline"}, "affected_dimensions": ["appearance"]})
        with self.assertRaisesRegex(ValueError, "active source_span_ids"):
            self.normalize(raw, envelope, snapshot)

    def test_brief_uses_effective_levels_and_previous_names_are_not_aliases(self):
        _, _, snapshot = self.inputs()
        brief = controls.authoring_brief(snapshot)
        for axis in controls.AXES:
            self.assertIn(f"{axis}: 3 (range: 0–3)", brief)
            self.assertIn(snapshot["definitions"]["controls"][axis]["definition"], brief)
        for old in ("sensual_editorial", "fetish_fashion"):
            self.assertNotIn(old, brief)
            with self.assertRaisesRegex(ValueError, "unsupported"):
                controls.resolve("a portrait", overrides={old: 3})
        for old in ("--sensual-editorial-intensity", "--fetish-fashion-intensity"):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                generator.main([old, "3"])
        inactive = controls.resolve("no people", overrides={"sensual": 3, "fetish": 3}, context={"no_people": True}, seed=1)
        self.assertIn("sensual: 0", controls.authoring_brief(inactive))


if __name__ == "__main__":
    unittest.main()
