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
YANDERE_REQUEST = (
    "성인 얀데레 간호사가 같은 성인 환자를 다정히 돌보면서 "
    "퇴원 일정과 병실 출입을 통제하는 장면"
)
YANDERE_BASELINE = (
    "An adult fictional nurse gently adjusts a blanket for the same adult patient in "
    "a quiet recovery room. A signed discharge note triggers the moment. Her sincere "
    "devoted care stays visible as she takes control of the patient's discharge schedule "
    "and quietly keeps the visitor pass, with a slightly asymmetric tender smile under "
    "an overfocused steady gaze and faint lower-lid tension. The same adult patient's "
    "reaching hand stops at the missing visitor pass, and the altered discharge schedule "
    "is already visible on the bedside chart. Affection and boundary control coexist in "
    "one frame, while the same white clinical uniform keeps her identity continuous."
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
                    "affect_leak_intentionality": "minimized",
                    "event_phase": "unfinished",
                },
                "relations": [
                    {
                        "operator": "contrasts",
                        "left": "surface_affect",
                        "right": "underlying_affiliation",
                    },
                    {
                        "operator": "same_target",
                        "members": [
                            "relationship_target",
                            "primary_action",
                            "affect_leak",
                        ],
                    },
                    {
                        "operator": "temporal_order",
                        "first": "surface_affect",
                        "then": "affect_leak",
                    },
                ],
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


def yandere_envelope(request_id: str = "v6-yandere-request") -> dict:
    return {
        "contract_version": "photo-request-envelope/v1",
        "provenance": "requesting_user",
        "request_id": request_id,
        "request_text": YANDERE_REQUEST,
        "request_sha256": hashlib.sha256(YANDERE_REQUEST.encode("utf-8")).hexdigest(),
        "active_spans": [
            {
                "span_id": "topic",
                "start": 0,
                "end": len(YANDERE_REQUEST),
                "text": YANDERE_REQUEST,
            }
        ],
    }


def yandere_core() -> dict:
    return {
        "contract_version": "photo-authorial-core/v3",
        "provenance": "agent_prepack",
        "source_request": YANDERE_REQUEST,
        "interpreted_intent": (
            "An adult fictional nurse directs sincere care and possessive access control "
            "toward the same adult patient"
        ),
        "subject": "one adult fictional nurse and one adult patient",
        "setting": "a quiet adult recovery room",
        "event": "care for the patient becomes control of discharge and visitor access",
        "visual_priorities": [
            "sincere care and boundary control in one frame",
            "same adult affection target",
            "visible changed access consequence",
        ],
        "baseline_prompt_en": YANDERE_BASELINE,
        "user_definitions": [],
        "interpretation_provenance": [
            {
                "term": "얀데레",
                "source_text": "얀데레",
                "basis": "agent_general_knowledge",
                "resolution": (
                    "sincere affection toward one adult target escalating into a "
                    "boundary-crossing control action toward that same target"
                ),
                "sources": [],
            }
        ],
        "unresolved_ambiguities": [],
        "user_exclusions": [],
        "runtime_forbidden_labels": ["얀데레"],
        "intent_lock": {
            "contract_version": "photo-intent-lock/v1",
            "priority": "requesting_user",
            "semantic_anchors": [
                {
                    "anchor_id": "concept",
                    "source_text": YANDERE_REQUEST,
                    "dimension": "concept",
                    "prompt_evidence": "Affection and boundary control coexist in one frame",
                },
                {
                    "anchor_id": "subject",
                    "source_text": YANDERE_REQUEST,
                    "dimension": "subject",
                    "prompt_evidence": "An adult fictional nurse",
                },
                {
                    "anchor_id": "event",
                    "source_text": YANDERE_REQUEST,
                    "dimension": "event",
                    "prompt_evidence": (
                        "takes control of the patient's discharge schedule and quietly "
                        "keeps the visitor pass"
                    ),
                },
                {
                    "anchor_id": "character_response",
                    "source_text": YANDERE_REQUEST,
                    "dimension": "character_response",
                    "prompt_evidence": "Her sincere devoted care stays visible",
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
                "assertion_id": "affection_control_same_target",
                "dimension": "character_response",
                "polarity": "required",
                "source_span_ids": ["topic"],
                "affected_dimensions": ["character_response"],
                "axes": {
                    "surface_affect": "openly affectionate",
                    "underlying_affiliation": "possessive",
                    "relationship_target": "same_adult_patient",
                    "primary_action": "appropriates_access",
                    "affect_leak_timing": "immediate",
                    "affect_leak_channels": ["gaze"],
                    "event_phase": "unfinished",
                    "affect_leak_intentionality": "deliberate",
                },
                "relations": [
                    {
                        "operator": "same_target",
                        "members": [
                            "relationship_target",
                            "surface_affect",
                            "primary_action",
                            "immediate_consequence",
                        ],
                    },
                    {
                        "operator": "temporal_order",
                        "first": "trigger",
                        "then": "primary_action",
                    },
                    {
                        "operator": "contrasts",
                        "left": "surface_affect",
                        "right": "immediate_consequence",
                    },
                ],
                "evidence": {
                    "actor_phrase": "An adult fictional nurse",
                    "baseline_phrase": "Her sincere devoted care stays visible",
                    "trigger_phrase": "A signed discharge note triggers the moment",
                    "target_phrase": "the same adult patient",
                    "primary_action_phrase": (
                        "takes control of the patient's discharge schedule and quietly "
                        "keeps the visitor pass"
                    ),
                    "affective_leak_phrase": (
                        "a slightly asymmetric tender smile under an overfocused steady "
                        "gaze and faint lower-lid tension"
                    ),
                    "visible_response_phrase": (
                        "The same adult patient's reaching hand stops at the missing visitor pass"
                    ),
                    "immediate_consequence_phrase": (
                        "the altered discharge schedule is already visible on the bedside chart"
                    ),
                    "continuity_phrase": (
                        "the same white clinical uniform keeps her identity continuous"
                    ),
                },
            }
        ],
        "request_lineage": None,
        "style": {
            "domain": "character_editorial",
            "family": "restrained relational narrative portrait",
            "evidence": ["quiet recovery room", "bedside access traces"],
        },
        "variation_key": "typed-v6-yandere-test",
    }


def core_with_concept_assertion() -> dict:
    payload = core()
    payload["semantic_assertions"].append(
        {
            "assertion_id": "guarded_care_concept",
            "dimension": "concept",
            "polarity": "required",
            "source_span_ids": ["topic"],
            "affected_dimensions": ["concept"],
            "axes": {
                "controlled_surface": "stern_professional_posture",
                "contained_affect_leak": "delayed_gaze_check",
                "connection_trace": "practical_peer_care",
            },
            "evidence": {
                "controlled_surface_phrase": "keeps her stern professional posture",
                "contained_affect_leak_phrase": (
                    "looks away before checking their reaction"
                ),
                "connection_trace_phrase": (
                    "wraps the coworker's scraped wrist with practical care"
                ),
            },
        }
    )
    return payload


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
        self.assertEqual(
            {row["operator"] for row in assertion["relations"]},
            {"contrasts", "same_target", "temporal_order"},
        )
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

        malformed_relation = core()
        malformed_relation["semantic_assertions"][0]["relations"][1]["members"] = [
            "relationship_target",
            "relationship_target",
        ]
        with self.assertRaisesRegex(ValueError, "distinct semantic members"):
            self.normalize(malformed_relation)

        unknown_relation_member = core()
        unknown_relation_member["semantic_assertions"][0]["relations"][1][
            "members"
        ].append("invented_relation_member")
        with self.assertRaisesRegex(ValueError, "distinct semantic members"):
            self.normalize(unknown_relation_member)

        missing_target_member = core()
        missing_target_member["semantic_assertions"][0]["relations"][1][
            "members"
        ].remove("relationship_target")
        with self.assertRaisesRegex(ValueError, "distinct semantic members"):
            self.normalize(missing_target_member)

    def test_authorial_core_and_composed_prompt_use_advisory_and_absolute_budgets(self):
        over_recommended = core()
        baseline_count = audit_composed_prompt.english_prompt_word_count(
            over_recommended["baseline_prompt_en"]
        )
        over_recommended["baseline_prompt_en"] += " " + " ".join(
            ["detail"] * (181 - baseline_count)
        )
        normalized_over_recommended = self.normalize(over_recommended)
        self.assertEqual(
            audit_composed_prompt.english_prompt_word_count(
                normalized_over_recommended["baseline_prompt_en"]
            ),
            181,
        )

        too_long = core()
        too_long_count = audit_composed_prompt.english_prompt_word_count(
            too_long["baseline_prompt_en"]
        )
        too_long["baseline_prompt_en"] += " " + " ".join(
            ["detail"] * (321 - too_long_count)
        )
        with self.assertRaisesRegex(ValueError, "24 to 320 English words"):
            self.normalize(too_long)

        data = self.runtime_data()
        normalized = self.normalize(core())
        result = prompt_generator.generate_once(
            data,
            random.Random(1416),
            "character_attribute_composition_scene",
            ["en"],
            True,
            12,
            True,
            selection_mode="rule",
            include_trace=True,
            concept_locks=[REQUEST],
            seed=1416,
            creativity=0.0,
            authorial_core=normalized,
        )
        pack = prompt_generator.build_candidate_pack(result, data, "v6")
        self.assertEqual(
            pack["authorial_composition"]["prompt_budget"],
            prompt_generator.authorial_prompt_budget_contract(),
        )
        prompt_count = audit_composed_prompt.english_prompt_word_count(BASELINE)
        advisory_prompt = BASELINE + " " + " ".join(
            ["detail"] * (181 - prompt_count)
        )
        binding = {
            "source_authorial_core_sha256": normalized["canonical_sha256"],
            "source_intent_lock_sha256": normalized["intent_lock"][
                "canonical_sha256"
            ],
            "preserved_anchor_ids": [
                row["anchor_id"]
                for row in normalized["intent_lock"]["semantic_anchors"]
            ],
            "preserved_evidence": [
                row["prompt_evidence"]
                for row in normalized["intent_lock"]["semantic_anchors"][:3]
            ],
            "authorial_decisions": [
                {
                    "dimension": "composition",
                    "decision": "retain the corridor depth",
                    "rationale": "keeps the causal response sequence readable",
                },
                {
                    "dimension": "lighting",
                    "decision": "use restrained practical light",
                    "rationale": "keeps the small affect leak visible",
                },
            ],
        }
        warnings = []
        failures = audit_composed_prompt.audit_authorial_core_v5(
            pack,
            {"authorial_core_binding": binding},
            advisory_prompt,
            warnings,
        )
        self.assertNotIn(
            "authorial_core_prompt_budget",
            {row["check"] for row in failures},
        )
        advisory_warning = next(
            row
            for row in warnings
            if row["check"] == "authorial_prompt_recommended_budget"
        )
        self.assertEqual(advisory_warning["actual_words"], 181)
        self.assertEqual(advisory_warning["recommended_maximum_words"], 180)
        self.assertEqual(advisory_warning["absolute_maximum_words"], 320)
        self.assertIn(
            "authorial_prompt_optional_prose_budget",
            {row["check"] for row in warnings},
        )

        legacy_pack = copy.deepcopy(pack)
        legacy_pack["authorial_composition"].pop("prompt_budget")
        legacy_failures = audit_composed_prompt.audit_authorial_core_v5(
            legacy_pack,
            {"authorial_core_binding": binding},
            advisory_prompt,
            [],
        )
        legacy_budget_failure = next(
            row
            for row in legacy_failures
            if row["check"] == "authorial_core_prompt_budget"
        )
        self.assertEqual(legacy_budget_failure["maximum_words"], 180)
        self.assertEqual(legacy_budget_failure["actual_words"], 181)

        mutated_pack = copy.deepcopy(pack)
        mutated_pack["authorial_composition"]["prompt_budget"][
            "recommended_maximum_words"
        ] = 200
        mutated_failures = audit_composed_prompt.audit_authorial_core_v5(
            mutated_pack,
            {"authorial_core_binding": binding},
            BASELINE,
            [],
        )
        self.assertIn(
            "authorial_prompt_budget_contract",
            {row["check"] for row in mutated_failures},
        )

        absolute_prompt = BASELINE + " " + " ".join(
            ["detail"] * (321 - prompt_count)
        )
        failures = audit_composed_prompt.audit_authorial_core_v5(
            pack,
            {"authorial_core_binding": binding},
            absolute_prompt,
            [],
        )
        budget_failure = next(
            row
            for row in failures
            if row["check"] == "authorial_core_prompt_budget"
        )
        self.assertEqual(budget_failure["actual_words"], 321)
        self.assertEqual(budget_failure["absolute_maximum_words"], 320)

    def test_authorial_budget_expands_advisory_ceiling_for_required_evidence(self):
        required_phrase = " ".join(f"required{index}" for index in range(150))
        prompt = required_phrase + " " + " ".join(
            f"optional{index}" for index in range(70)
        )
        pack = {
            "authorial_core": {
                "intent_lock": {
                    "semantic_anchors": [
                        {"prompt_evidence": required_phrase},
                    ]
                }
            }
        }
        metrics = audit_composed_prompt.authorial_prompt_budget_metrics(
            pack,
            {},
            prompt,
        )
        self.assertEqual(metrics["actual_words"], 220)
        self.assertEqual(metrics["required_evidence_words"], 150)
        self.assertEqual(metrics["optional_prose_words"], 70)
        self.assertEqual(metrics["effective_recommended_maximum_words"], 230)

    def test_blanket_negative_rewrite_is_rejected_before_core_freeze(self):
        payload = core()
        payload["baseline_prompt_en"] += (
            " No injection, contact, gore, sexuality, cleavage, or extra people."
        )
        with self.assertRaisesRegex(ValueError, "blanket negative directives"):
            self.normalize(payload)

        inline = core()
        inline["baseline_prompt_en"] = inline["baseline_prompt_en"].replace(
            "with practical care,",
            "with practical care, never touching anyone,",
        )
        with self.assertRaisesRegex(ValueError, "blanket negative directives"):
            self.normalize(inline)

        self.assertEqual(
            prompt_generator.find_blanket_negative_directives(
                "Keep the scene intense. Constraints: no contact or gore."
            ),
            ["no contact or gore"],
        )

    def test_negative_intent_guard_filters_semantic_defaults_and_is_auditable(self):
        normalized = self.normalize(core())
        entries = [
            {"en": "low resolution", "ko": "저해상도"},
            {"en": "unrealistic hands", "ko": "비현실적인 손"},
            {"en": "awkward expression", "ko": "어색한 표정"},
            {"en": "extra people", "ko": "추가 인물"},
            {"en": "no contact", "ko": "접촉 없음"},
            {"en": "gore", "ko": "고어"},
        ]
        kept, suppressed = prompt_generator.filter_authorial_negative_entries(
            entries,
            normalized,
            identity_preservation_enabled=False,
        )
        self.assertEqual(
            [entry["en"] for entry in kept],
            ["low resolution", "unrealistic hands"],
        )
        self.assertEqual(
            suppressed,
            ["awkward expression", "extra people", "no contact", "gore"],
        )

        requester_exclusion_core = copy.deepcopy(normalized)
        requester_exclusion_core["user_exclusions"] = ["No gore."]
        requester_kept, requester_suppressed = (
            prompt_generator.filter_authorial_negative_entries(
                [
                    {"en": "gore", "ko": "고어"},
                    {"en": "no contact", "ko": "접촉 없음"},
                ],
                requester_exclusion_core,
                identity_preservation_enabled=False,
            )
        )
        self.assertEqual(
            [entry["en"] for entry in requester_kept],
            ["gore"],
        )
        self.assertEqual(requester_suppressed, ["no contact"])

        identity_kept, identity_suppressed = (
            prompt_generator.filter_authorial_negative_entries(
                [
                    {
                        "en": "dollified facial proportions",
                        "ko": "인형화된 얼굴 비율",
                    }
                ],
                normalized,
                identity_preservation_enabled=True,
            )
        )
        self.assertEqual(
            [entry["en"] for entry in identity_kept],
            ["dollified facial proportions"],
        )
        self.assertEqual(identity_suppressed, [])

        data = self.runtime_data()
        result = prompt_generator.generate_once(
            data,
            random.Random(1415),
            "character_attribute_composition_scene",
            ["en"],
            True,
            12,
            True,
            selection_mode="rule",
            include_trace=True,
            concept_locks=[REQUEST],
            seed=1415,
            creativity=0.0,
            authorial_core=normalized,
        )
        pack = prompt_generator.build_candidate_pack(result, data, "v6")
        guard = pack["negative_intent_guard"]
        self.assertEqual(
            guard["contract_version"],
            "photo-negative-intent-guard/v1",
        )
        self.assertEqual(
            guard["emitted_terms"],
            prompt_generator.split_negative_prompt_terms(pack["negative_en"]),
        )
        self.assertTrue(
            set(term.casefold() for term in guard["emitted_terms"])
            <= prompt_generator.AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS
        )
        self.assertEqual(
            audit_composed_prompt.audit_negative_intent_guard(pack, BASELINE),
            [],
        )

        harmful_prompt_failures = (
            audit_composed_prompt.audit_negative_intent_guard(
                pack,
                BASELINE
                + " No injection, contact, gore, sexuality, cleavage, or extra people.",
            )
        )
        self.assertIn(
            "negative_intent_guard_prompt",
            {row["check"] for row in harmful_prompt_failures},
        )

        tampered = copy.deepcopy(pack)
        tampered["negative_en"] = f"{pack['negative_en']}, no contact"
        tampered["negative_intent_guard"] = (
            prompt_generator.build_negative_intent_guard(
                normalized,
                tampered["negative_en"],
                identity_preservation_enabled=False,
            )
        )
        tampered_failures = audit_composed_prompt.audit_negative_intent_guard(
            tampered,
            BASELINE,
        )
        self.assertIn(
            "negative_intent_guard_terms",
            {row["check"] for row in tampered_failures},
        )

    def test_negative_intent_guard_generator_and_auditor_vocabularies_match(self):
        self.assertEqual(
            prompt_generator.AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS,
            audit_composed_prompt.AUTHORIAL_INTENT_NEUTRAL_NEGATIVE_TERMS,
        )
        self.assertEqual(
            prompt_generator.AUTHORIAL_IDENTITY_PRESERVATION_NEGATIVE_TERMS,
            audit_composed_prompt.AUTHORIAL_IDENTITY_PRESERVATION_NEGATIVE_TERMS,
        )

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
            contract["semantic_relations"],
            normalized["semantic_assertions"][0]["relations"],
        )
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

    def test_yandere_core_binds_same_target_affection_control_relation(self):
        normalized_envelope = prompt_generator.normalize_request_envelope(
            yandere_envelope()
        )
        normalized = prompt_generator.normalize_authorial_core(
            yandere_core(),
            request_envelope=normalized_envelope,
        )
        assertion = normalized["semantic_assertions"][0]
        self.assertEqual(assertion["axes"]["underlying_affiliation"], "possessive")
        self.assertEqual(
            assertion["relations"],
            [
                {
                    "operator": "same_target",
                    "members": [
                        "relationship_target",
                        "surface_affect",
                        "primary_action",
                        "immediate_consequence",
                    ],
                },
                {
                    "operator": "temporal_order",
                    "first": "trigger",
                    "then": "primary_action",
                },
                {
                    "operator": "contrasts",
                    "left": "surface_affect",
                    "right": "immediate_consequence",
                },
            ],
        )
        data = self.runtime_data()
        profile = next(
            row
            for row in prompt_generator.character_response_concept_profiles(data)
            if row["id"] == "yandere"
        )
        evaluation = prompt_generator.evaluate_character_response_profile(
            normalized,
            data,
            profile,
        )
        self.assertEqual(evaluation["status"], "consistent", evaluation)
        contract = prompt_generator.compile_character_response_contract(
            normalized,
            data=data,
            semantic_index=data[prompt_generator.SEMANTIC_INDEX_DATA_KEY],
        )
        self.assertIsNotNone(contract)
        assert contract is not None
        self.assertEqual(contract["semantic_relations"], assertion["relations"])

    def test_yandere_v6_pack_carries_relation_and_visual_obligation(self):
        data = self.runtime_data()
        normalized_envelope = prompt_generator.normalize_request_envelope(
            yandere_envelope()
        )
        normalized_core = prompt_generator.normalize_authorial_core(
            yandere_core(),
            request_envelope=normalized_envelope,
        )
        result = prompt_generator.generate_once(
            data,
            random.Random(1415),
            "character_attribute_composition_scene",
            ["en"],
            True,
            12,
            True,
            selection_mode="rule",
            include_trace=True,
            concept_locks=[YANDERE_REQUEST],
            seed=1415,
            creativity=0.0,
            authorial_core=normalized_core,
        )
        pack = prompt_generator.build_candidate_pack(result, data, "v6")
        self.assertEqual(pack["contract_version"], "photo-candidate-pack/v6")
        self.assertEqual(
            pack["character_response"]["semantic_relations"],
            normalized_core["semantic_assertions"][0]["relations"],
        )
        concept_candidates = pack["character_response"]["advisory_retrieval"][
            "candidates"
        ]
        yandere_candidate = next(
            row
            for row in concept_candidates
            if row["candidate_id"] == "character_response_concept:yandere"
        )
        self.assertEqual(
            yandere_candidate["semantic_consistency"]["status"],
            "consistent",
        )
        self.assertFalse(yandere_candidate["hard_eligible"])
        self.assertEqual(
            [
                row["id"]
                for row in pack["visual_obligations"]["obligations"]
            ],
            ["yandere_affection_control_relation"],
        )
        obligation = pack["visual_obligations"]["obligations"][0]
        self.assertEqual(
            obligation["runtime_expression"]["default_mode"],
            "definition_only",
        )
        self.assertIn(
            "syringe_weapon_blood_or_red_light_only",
            obligation["reject_substitutes"],
        )

    def test_retry_preserves_yandere_as_a_hard_visual_obligation(self):
        retry_request = "실패한 이미지를 같은 의미로 다시 생성해줘"
        raw_envelope = yandere_envelope("v6-yandere-retry")
        raw_envelope["request_text"] = retry_request
        raw_envelope["request_sha256"] = hashlib.sha256(
            retry_request.encode("utf-8")
        ).hexdigest()
        raw_envelope["active_spans"] = [
            {
                "span_id": "retry",
                "start": 0,
                "end": len(retry_request),
                "text": retry_request,
            }
        ]
        normalized_envelope = prompt_generator.normalize_request_envelope(
            raw_envelope
        )
        raw_core = yandere_core()
        raw_core["source_request"] = retry_request
        raw_core["runtime_forbidden_labels"] = []
        raw_core["interpretation_provenance"] = [
            {
                "term": "same meaning retry",
                "source_text": retry_request,
                "basis": "request_context",
                "resolution": (
                    "preserve the parent concept subject event and character response"
                ),
                "sources": [],
            }
        ]
        for anchor in raw_core["intent_lock"]["semantic_anchors"]:
            anchor["source_text"] = retry_request
        raw_core["semantic_assertions"][0]["source_span_ids"] = ["retry"]
        raw_core["request_lineage"] = {
            "parent_request_id": "v6-yandere-request",
            "parent_core_sha256": "a" * 64,
            "preserved_dimensions": [
                "concept",
                "subject",
                "event",
                "character_response",
            ],
            "allowed_changes": ["framing", "composition", "lighting", "camera"],
        }
        normalized_core = prompt_generator.normalize_authorial_core(
            raw_core,
            request_envelope=normalized_envelope,
        )
        data = self.runtime_data()
        visual_intent = prompt_generator.normalize_visual_intent(
            {
                "contract_version": "photo-visual-intent/v1",
                "provenance": "agent_prepack",
                "obligations": [
                    {
                        "profile_id": "yandere_affection_control_relation",
                        "source": "agent_postcore_interpretation",
                        "scope": "request_only",
                        "source_text": normalized_core["baseline_prompt_en"],
                        "bindings": {},
                    }
                ],
            },
            data[prompt_generator.VISUAL_OBLIGATIONS_DATA_KEY],
            data[prompt_generator.VISUAL_PROFILE_INDEX_DATA_KEY],
        )
        result = prompt_generator.generate_once(
            data,
            random.Random(1417),
            "character_attribute_composition_scene",
            ["en"],
            True,
            12,
            True,
            selection_mode="rule",
            include_trace=True,
            concept_locks=[retry_request],
            seed=1417,
            creativity=0.0,
            authorial_core=normalized_core,
        )
        result.setdefault("provenance", {})["visual_intent"] = visual_intent
        pack = prompt_generator.build_candidate_pack(result, data, "v6")
        self.assertEqual(
            [row["id"] for row in pack["visual_obligations"]["obligations"]],
            ["yandere_affection_control_relation"],
        )
        self.assertEqual(
            pack["visual_obligations"]["obligations"][0]["activation"]["source"],
            "agent_postcore_interpretation",
        )
        self.assertNotIn(
            "visual-concept:yandere_affection_control_relation",
            {
                row["id"]
                for row in (pack.get("visual_concept_candidates") or {}).get(
                    "candidates", []
                )
            },
        )

    def test_required_non_character_assertion_binds_final_prompt_evidence(self):
        normalized = self.normalize(core_with_concept_assertion())
        contract = prompt_generator.compile_semantic_assertion_obligations(
            normalized
        )
        self.assertIsNotNone(contract)
        assert contract is not None
        self.assertEqual(
            contract["contract_version"],
            "photo-semantic-assertion-obligations/v1",
        )
        self.assertEqual(
            [row["assertion_id"] for row in contract["obligations"]],
            ["guarded_care_concept"],
        )
        evidence = contract["obligations"][0]["frozen_evidence"]
        pack = {
            "authorial_core": normalized,
            "semantic_assertion_obligations": contract,
        }
        composed = {
            "semantic_assertion_evidence": {
                "source_contract_sha256": contract["canonical_sha256"],
                "evidence": {"guarded_care_concept": copy.deepcopy(evidence)},
            }
        }
        self.assertEqual(
            audit_composed_prompt.audit_semantic_assertion_obligations_v6(
                pack,
                composed,
                BASELINE,
            ),
            [],
        )

        changed = copy.deepcopy(composed)
        changed["semantic_assertion_evidence"]["evidence"][
            "guarded_care_concept"
        ]["contained_affect_leak_phrase"] = "an invented emotional shorthand"
        changed_failures = (
            audit_composed_prompt.audit_semantic_assertion_obligations_v6(
                pack,
                changed,
                BASELINE,
            )
        )
        self.assertIn(
            "semantic_assertion_evidence",
            {failure["check"] for failure in changed_failures},
        )

        missing_contract_failures = (
            audit_composed_prompt.audit_semantic_assertion_obligations_v6(
                {"authorial_core": normalized},
                composed,
                BASELINE,
            )
        )
        self.assertIn(
            "semantic_assertion_obligations_contract",
            {failure["check"] for failure in missing_contract_failures},
        )

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
            core_with_concept_assertion(),
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
        self.assertIn("semantic_assertion_obligations", pack)
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

        missing_contract = audit_composed_prompt.audit_character_response_v6(
            {"authorial_core": normalized},
            composed,
            BASELINE,
        )
        self.assertIn(
            "character_response_contract",
            {failure["check"] for failure in missing_contract},
        )

        mutated_contract = copy.deepcopy(contract)
        mutated_contract["semantic_axes"]["surface_affect"] = "cheerful"
        mutated_failures = audit_composed_prompt.audit_character_response_v6(
            {
                "authorial_core": normalized,
                "character_response": mutated_contract,
            },
            composed,
            BASELINE,
        )
        self.assertIn(
            "character_response_contract",
            {failure["check"] for failure in mutated_failures},
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
