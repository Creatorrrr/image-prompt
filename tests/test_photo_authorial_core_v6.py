from __future__ import annotations

import copy
import hashlib
import json
import random
import sys
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "photo-prompt-image-generator" / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import prompt_generator  # noqa: E402
import audit_composed_prompt  # noqa: E402


REQUEST = "성인 네코미미 츤데레 메이드가 다친 동료를 퉁명스럽게 돌보는 장면"
BASELINE = (
    "An adult cat-eared maid in a quiet service corridor keeps her stern professional "
    "posture while an injured adult coworker sits beside her. A dropped first-aid tin "
    "triggers the moment. She wraps the coworker's scraped wrist with practical care, "
    "looks away before checking their reaction, and leaves a warm cup within reach. "
    "The coworker's relieved shoulders answer the gesture, while her compact ears tilt "
    "toward them and the same dark uniform keeps her identity continuous."
)


def envelope(request_id: str = "v6-request") -> dict:
    return {
        "contract_version": "photo-request-envelope/v1",
        "provenance": "requesting_user",
        "request_id": request_id,
        "request_text": REQUEST,
        "request_sha256": hashlib.sha256(REQUEST.encode("utf-8")).hexdigest(),
        "active_spans": [
            {"span_id": "topic", "start": 0, "end": len(REQUEST), "text": REQUEST}
        ],
    }


def core() -> dict:
    return {
        "contract_version": "photo-authorial-core/v3",
        "provenance": "agent_prepack",
        "source_request": REQUEST,
        "interpreted_intent": (
            "An adult guarded maid reveals concealed peer affection through practical care"
        ),
        "subject": "one adult cat-eared maid and one adult coworker",
        "setting": "a quiet staff service corridor after closing",
        "event": "she treats a coworker's scraped wrist after a dropped medical tin",
        "visual_priorities": [
            "guarded practical peer care",
            "recipient reaction and consequence",
            "restrained feline ear reflex",
        ],
        "baseline_prompt_en": BASELINE,
        "user_definitions": [],
        "interpretation_provenance": [
            {
                "term": "츤데레",
                "source_text": "츤데레",
                "basis": "agent_general_knowledge",
                "resolution": (
                    "guarded outward behavior with concealed positive affiliation toward a peer"
                ),
                "sources": [],
            }
        ],
        "unresolved_ambiguities": [],
        "user_exclusions": [],
        "runtime_forbidden_labels": [],
        "intent_lock": {
            "contract_version": "photo-intent-lock/v1",
            "priority": "requesting_user",
            "semantic_anchors": [
                {
                    "anchor_id": "concept",
                    "source_text": REQUEST,
                    "dimension": "concept",
                    "prompt_evidence": "wraps the coworker's scraped wrist with practical care",
                },
                {
                    "anchor_id": "subject",
                    "source_text": REQUEST,
                    "dimension": "subject",
                    "prompt_evidence": "An adult cat-eared maid",
                },
                {
                    "anchor_id": "event",
                    "source_text": REQUEST,
                    "dimension": "event",
                    "prompt_evidence": "A dropped first-aid tin triggers the moment",
                },
                {
                    "anchor_id": "character_response",
                    "source_text": REQUEST,
                    "dimension": "character_response",
                    "prompt_evidence": "looks away before checking their reaction",
                },
            ],
            "locked_dimensions": [
                "concept",
                "subject",
                "event",
                "character_response",
            ],
            "open_dimensions": [
                "framing",
                "composition",
                "lighting",
                "camera",
                "color",
            ],
        },
        "semantic_assertions": [
            {
                "assertion_id": "guarded_peer_care",
                "dimension": "character_response",
                "polarity": "required",
                "source_span_ids": ["topic"],
                "affected_dimensions": ["character_response"],
                "axes": {
                    "surface_affect": "guarded",
                    "underlying_affiliation": "positive",
                    "relationship_target": "adult_coworker",
                    "primary_action": "practical_care",
                    "affect_leak_timing": "delayed",
                    "affect_leak_channels": ["gaze"],
                    "event_phase": "unfinished",
                },
                "evidence": {
                    "actor_phrase": "An adult cat-eared maid",
                    "baseline_phrase": "keeps her stern professional posture",
                    "trigger_phrase": "A dropped first-aid tin triggers the moment",
                    "target_phrase": "an injured adult coworker sits beside her",
                    "primary_action_phrase": (
                        "wraps the coworker's scraped wrist with practical care"
                    ),
                    "visible_response_phrase": (
                        "The coworker's relieved shoulders answer the gesture"
                    ),
                    "immediate_consequence_phrase": "leaves a warm cup within reach",
                    "continuity_phrase": (
                        "the same dark uniform keeps her identity continuous"
                    ),
                    "affective_leak_phrase": "looks away before checking their reaction",
                    "nonhuman_reflex_phrase": "her compact ears tilt toward them",
                },
            }
        ],
        "request_lineage": None,
        "style": {
            "domain": "character_editorial",
            "family": "restrained narrative portrait",
            "evidence": ["quiet corridor depth", "tactile first-aid props"],
        },
        "variation_key": "typed-v6-test",
    }


class PhotoAuthorialCoreV6Tests(unittest.TestCase):
    def normalize(self, payload: dict, request_id: str = "v6-request") -> dict:
        normalized_envelope = prompt_generator.normalize_request_envelope(
            envelope(request_id)
        )
        return prompt_generator.normalize_authorial_core(
            payload,
            request_envelope=normalized_envelope,
        )

    def runtime_data(self) -> dict:
        assets = ROOT / "skills" / "photo-prompt-image-generator" / "assets"
        data = prompt_generator.load_json(assets / "photo_prompt_tags.json")
        data[prompt_generator.QUALITY_LAYERS_DATA_KEY] = (
            prompt_generator.load_quality_layers(
                assets / "photo_prompt_quality_layers.json"
            )
        )
        registry = prompt_generator.load_visual_obligation_registry(
            assets / "photo_prompt_visual_obligations.json"
        )
        data[prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY] = registry
        data[prompt_generator.VISUAL_PROFILE_INDEX_DATA_KEY] = (
            prompt_generator.load_visual_profile_index(
                assets / "photo_prompt_visual_profile_index.json",
                registry,
            )
        )
        data[prompt_generator.SEMANTIC_INDEX_DATA_KEY] = (
            prompt_generator.load_semantic_index_payload(
                assets / "photo_prompt_semantic_index.json"
            )
        )
        return data

    def test_v3_freezes_typed_character_response_evidence(self):
        normalized = self.normalize(core())
        assertion = normalized["semantic_assertions"][0]
        self.assertEqual(assertion["dimension"], "character_response")
        self.assertEqual(assertion["axes"]["surface_affect"], "guarded")
        self.assertIn(assertion["evidence"]["trigger_phrase"], BASELINE)
        self.assertRegex(normalized["canonical_sha256"], r"^[0-9a-f]{64}$")

    def test_required_assertion_rejects_unfrozen_or_unlocked_evidence(self):
        not_literal = core()
        not_literal["semantic_assertions"][0]["evidence"]["trigger_phrase"] = (
            "an invented trigger absent from the baseline"
        )
        with self.assertRaisesRegex(ValueError, "must occur in baseline_prompt_en"):
            self.normalize(not_literal)

        unlocked = core()
        unlocked["intent_lock"]["locked_dimensions"].remove("character_response")
        unlocked["intent_lock"]["semantic_anchors"] = [
            row
            for row in unlocked["intent_lock"]["semantic_anchors"]
            if row["dimension"] != "character_response"
        ]
        unlocked["intent_lock"]["open_dimensions"].append("character_response")
        with self.assertRaisesRegex(ValueError, "must affect only locked dimensions"):
            self.normalize(unlocked)

        multiple_actions = core()
        multiple_actions["semantic_assertions"][0]["axes"]["primary_action"] = [
            "wraps the scraped wrist",
            "hands over a warm drink",
        ]
        with self.assertRaisesRegex(ValueError, "exactly one primary_action"):
            self.normalize(multiple_actions)

    def test_retry_lineage_is_hash_bound_and_dimension_disjoint(self):
        payload = core()
        payload["request_lineage"] = {
            "parent_request_id": "v5-parent",
            "parent_core_sha256": "a" * 64,
            "preserved_dimensions": ["concept", "subject", "character_response"],
            "allowed_changes": ["framing", "lighting"],
        }
        normalized = self.normalize(payload)
        self.assertEqual(
            normalized["request_lineage"]["parent_core_sha256"],
            "a" * 64,
        )

        overlap = copy.deepcopy(payload)
        overlap["request_lineage"]["allowed_changes"].append("concept")
        with self.assertRaisesRegex(ValueError, "must be disjoint"):
            self.normalize(overlap)

    def test_character_response_compiles_only_frozen_generic_structure(self):
        normalized = self.normalize(core())
        data = self.runtime_data()
        semantic_index = data[prompt_generator.SEMANTIC_INDEX_DATA_KEY]
        contract = prompt_generator.compile_character_response_contract(
            normalized,
            data=data,
            semantic_index=semantic_index,
        )
        self.assertIsNotNone(contract)
        assert contract is not None
        self.assertEqual(
            contract["source"],
            "authorial_core_semantic_assertion",
        )
        self.assertEqual(contract["behavior_budget"]["primary_action_count"], 1)
        self.assertEqual(contract["primary_affect_leak_channel"], "gaze")
        self.assertEqual(
            contract["frozen_evidence"]["primary_action_phrase"],
            "wraps the coworker's scraped wrist with practical care",
        )
        retrieval = contract["advisory_retrieval"]
        self.assertTrue(retrieval["evaluated"])
        self.assertTrue(
            all(candidate["hard_eligible"] is False for candidate in retrieval["candidates"])
        )
        self.assertNotIn("score", json.dumps(retrieval, ensure_ascii=False))

    def test_v6_routing_never_calls_legacy_raw_moe_router(self):
        typed_core = {
            "contract_version": "photo-authorial-core/v3",
            "interpreted_intent": "an adult portrait whose styling suits the reference appearance",
            "subject": "one adult portrait subject",
            "setting": "a quiet neutral portrait studio",
            "event": "the subject holds a calm portrait pose",
            "visual_priorities": ["facial likeness", "restrained styling"],
            "semantic_assertions": [],
        }
        with mock.patch.object(
            prompt_generator,
            "resolve_moe_response_intent",
            side_effect=AssertionError("legacy raw router must not run"),
        ):
            resolved = prompt_generator.resolve_request_intent_constraints(
                {"presets": [], "slots": {}},
                {"intent": "외모에 어울리는 성인 인물 사진"},
                {},
                authorial_core=typed_core,
            )
        self.assertEqual(resolved["routing_input"], "authorial_core_typed_semantics")
        self.assertFalse(resolved["character_response"]["enabled"])
        self.assertNotIn(prompt_generator.MOE_RESPONSE_DOMAIN, resolved["domains"])

    def test_v6_generation_and_pack_never_call_legacy_raw_moe_router(self):
        data = self.runtime_data()
        normalized_envelope = prompt_generator.normalize_request_envelope(envelope())
        normalized_core = prompt_generator.normalize_authorial_core(
            core(),
            request_envelope=normalized_envelope,
        )
        with mock.patch.object(
            prompt_generator,
            "resolve_moe_response_intent",
            side_effect=AssertionError("legacy raw router must not run"),
        ):
            result = prompt_generator.generate_once(
                data,
                random.Random(42),
                "character_attribute_composition_scene",
                ["en"],
                True,
                12,
                True,
                selection_mode="rule",
                include_trace=True,
                concept_locks=[normalized_envelope["request_text"]],
                seed=42,
                creativity=0.0,
                authorial_core=normalized_core,
            )
            pack = prompt_generator.build_candidate_pack(result, data, "v6")
        self.assertEqual(pack["contract_version"], "photo-candidate-pack/v6")
        self.assertIn("character_response", pack)
        self.assertNotIn("moe_response", pack)
        self.assertTrue(
            pack["coverage"]["intent_constraints"]["character_response"]["enabled"]
        )
        self.assertEqual(
            pack["coverage"]["intent_constraints"]["routing_input"],
            "authorial_core_typed_semantics",
        )
        core_binding = {
            "source_authorial_core_sha256": normalized_core["canonical_sha256"],
            "source_intent_lock_sha256": normalized_core["intent_lock"][
                "canonical_sha256"
            ],
            "preserved_anchor_ids": [
                row["anchor_id"]
                for row in normalized_core["intent_lock"]["semantic_anchors"]
            ],
            "preserved_evidence": [
                row["prompt_evidence"]
                for row in normalized_core["intent_lock"]["semantic_anchors"][:3]
            ],
            "authorial_decisions": [
                {
                    "dimension": "composition",
                    "decision": "keep corridor depth",
                    "rationale": "preserves the visible causal sequence",
                },
                {
                    "dimension": "lighting",
                    "decision": "use restrained practical light",
                    "rationale": "keeps every small response readable",
                },
            ],
        }
        self.assertEqual(
            audit_composed_prompt.audit_authorial_core_v5(
                pack,
                {"authorial_core_binding": core_binding},
                BASELINE,
            ),
            [],
        )

    def test_v6_character_response_audit_binds_exact_frozen_evidence(self):
        normalized = self.normalize(core())
        contract = prompt_generator.compile_character_response_contract(normalized)
        assert contract is not None
        pack = {
            "authorial_core": normalized,
            "character_response": contract,
        }
        composed = {
            "character_response": {
                "source_contract_sha256": contract["canonical_sha256"],
                "evidence": {
                    field: contract["frozen_evidence"][field]
                    for field in contract["prompt_binding"][
                        "required_evidence_fields"
                    ]
                },
                "selected_advisory_candidate_ids": [],
            }
        }
        self.assertEqual(
            audit_composed_prompt.audit_character_response_v6(
                pack,
                composed,
                BASELINE,
            ),
            [],
        )
        broken = copy.deepcopy(composed)
        broken["character_response"]["evidence"]["trigger_phrase"] = (
            "an invented trigger"
        )
        failures = audit_composed_prompt.audit_character_response_v6(
            pack,
            broken,
            BASELINE,
        )
        self.assertIn(
            "character_response_evidence",
            {failure["check"] for failure in failures},
        )

    def test_cjk_exact_matching_is_boundary_aware(self):
        for text in ("외모에 어울리는", "규모에 맞는", "용모에 관한", "부모에게 전한"):
            self.assertFalse(
                prompt_generator.resolve_moe_response_intent([text])["requested"],
                text,
            )
        for text in ("모에", "모에하게", "모에를 강조"):
            self.assertTrue(
                prompt_generator.resolve_moe_response_intent([text])["requested"],
                text,
            )


if __name__ == "__main__":
    unittest.main()
