#!/usr/bin/env python3
"""Deterministic, concept-independent scene selection for illustration v3.

The module is intentionally isolated from ``illustration_runtime``.  A caller
must dispatch legacy v1/v2 requests before importing or invoking this module so
that historical packs never read universal assets or validate a scene contract.

The runtime is not a natural-language semantic parser.  It consumes the exact
request bytes together with a literal-bound ``scene-contract/v1`` prepared by
the skill workflow.  Ambiguity remains open; no regex or keyword rule promotes
an unstated personality, emotion, relationship, intent, culture, diagnosis, or
body capability into a fixed fact.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence
import unicodedata


SCENE_CONTRACT_SCHEMA = "subculture-illustration-scene-contract/v2"
CANDIDATE_SCHEMA = "subculture-illustration-universal-scene-candidates/v1"
COMPATIBILITY_SCHEMA = "subculture-illustration-universal-compatibility/v1"
SEMANTIC_BINDINGS_SCHEMA = "subculture-illustration-universal-semantic-bindings/v1"
SELECTION_SCHEMA = "illustration-universal-scene-selection/v1"
COMPOSITION_CARRIERS_SCHEMA = "illustration-universal-composition-carriers/v1"
SEMANTIC_EFFECT_REGISTRY_SCHEMA = "illustration-universal-semantic-effect-registry/v1"
HARD_GATE_SNAPSHOT_SCHEMA = "illustration-universal-hard-gate-snapshot/v1"
SEMANTIC_FAMILY_KEY_SCHEMA = "subculture-illustration-semantic-family-key/v1"
CREATIVITY_INVARIANT_TRACE_SCHEMA = (
    "illustration-universal-scene-creativity-invariant-trace/v1"
)
POSTSELECTION_RUN_TRACE_SCHEMA = (
    "illustration-universal-scene-postselection-run-trace/v1"
)
PRESELECTION_TRIAL_SCHEMA = "illustration-universal-scene-preselection-trial/v1"

CANDIDATE_FILENAME = "illustration_universal_scene_candidates_v1.json"
COMPATIBILITY_FILENAME = "illustration_universal_compatibility_graph_v1.json"
SEMANTIC_BINDINGS_FILENAME = "illustration_universal_semantic_bindings_v1.json"
RESEARCH_MANIFEST_FILENAME = "research_evidence_universal_scene/manifest.json"

NORMALIZATION_ID = "NFKC+casefold+whitespace-collapse"
SCENE_SLOT_IDS = (
    "expression",
    "pose",
    "action",
    "relation",
    "prop",
    "environment",
)
EVENT_ROLE_IDS = (
    "actor",
    "action",
    "target",
    "instrument",
    "recipient",
    "result",
    "location",
    "phase",
)
PROPOSAL_REJECTION_REASON_IDS = (
    "proposal_path_not_open",
    "slot_state_ineligible",
    "requires_all_unsatisfied",
    "forbidden_predicate_satisfied",
    "policy_explicit_only",
    "policy_active_violence",
    "fixed_role_conflict",
    "closed_role_conflict",
)
DECISION_REASON_CODE_IDS = (
    "all_guard_predicates_passed",
    "capability_unsatisfied",
    "cardinality_feasible",
    "cardinality_limit",
    "closed_facet",
    "closed_prop_slot",
    "closed_role_conflict",
    "event_spine_cardinality",
    "fixed_facet_conflict",
    "fixed_role_conflict",
    "forbidden_predicate_satisfied",
    "guard_not_applicable",
    "guard_predicate_failed",
    "identity_overwrite",
    "policy_active_violence",
    "policy_explicit_only",
    "policy_not_applicable",
    "policy_pass",
    "policy_platform_blocked",
    "precondition_unsatisfied",
    "proposal_path_not_open",
    "remote_budget_exceeded",
    "requires_all_unsatisfied",
    "resource_capacity",
    "resource_feasible",
    "rule_satisfied",
    "slot_state_ineligible",
    "trigger_unsatisfied",
    "visible_bridge_required",
)
UNIVERSAL_RULE_REASON_CODE_BY_ID = MappingProxyType(
    {
        "rule_closed_prop": "closed_prop_slot",
        "rule_exactly_one_event": "event_spine_cardinality",
        "rule_fixed_identity_precedence": "identity_overwrite",
        "rule_policy_independent_of_creativity": "policy_platform_blocked",
        "rule_remote_budget": "remote_budget_exceeded",
        "rule_resource_capacity": "resource_capacity",
        "rule_visible_middle_far_bridge": "visible_bridge_required",
    }
)
CONTEXT_FIELD_IDS = (
    "theme_tags",
    "era_technology",
    "tone",
    "violence",
    "social",
    "scale",
)
CANDIDATE_ROLE_IDS = ("visual_atom", "router", "guard", "metric")
FACET_IDS = (
    "expression",
    "perceived_affect",
    "attention",
    "pose",
    "gesture",
    "action",
    "phase",
    "contact",
    "relation",
    "prop",
    "prop_state",
    "environment",
    "consequence",
    "bridge",
    "salience",
)
DISTANCE_AXIS_IDS = (
    "theme",
    "era_technology",
    "tone",
    "violence",
    "social",
    "scale",
    "salience_displacement",
)
LOAD_AXIS_IDS = (
    "physical",
    "occupancy",
    "affective_valence",
    "affective_arousal",
    "violence",
    "visual_salience",
    "scene_importance",
    "theme_displacement",
)
PIXEL_EVIDENCE_KIND_IDS = (
    "contact",
    "orientation",
    "state_boundary",
    "support",
    "path",
    "residue",
    "display",
)
SEMANTIC_EFFECT_IDS = (
    "active_weapon_discharge",
    "combat_opponent_assignment",
    "combat_target_assignment",
    "human_face_attachment",
    "human_hand_attachment",
    "human_limb_attachment",
    "navigation_instrument_use",
    "romantic_contact",
    "scene_promise_hijack",
)
SEMANTIC_EFFECT_SOURCE_KIND_IDS = (
    "visual_candidate",
    "proposal_profile",
    "context_profile",
    "bridge_type",
    "resource_kind",
)
CONTRACT_EFFECT_SOURCE_KIND_IDS = (
    "request",
    "identity_fact",
    "slot",
    "event_role",
    "context",
)
CONTRACT_EFFECT_SUBJECT_BINDINGS = (
    "source_entity",
    "actor",
    "target",
    "recipient",
    "scene",
)

GUARD_EXECUTION_PREDICATE_BY_ID = MappingProxyType(
    {
        "action_temporal_phases_single_phase_guard": "single_phase_present",
        "atomic_general_actions_static_ambiguity_guard": "dynamic_action_present",
        "dpa_cultural_universality_guard": "display_cues_contextualized",
        "dpa_inner_state_nonclaim_guard": "display_inner_state_not_claimed",
        "event_role_frames_role_assignment_guard": "event_roles_coherent",
        "gha_intention_nonclaim_guard": "attention_intention_not_claimed",
        "nxc_context_binding_guard": "nonhuman_channel_context_bound",
        "nxc_emotion_truth_guard": "nonhuman_inner_state_not_claimed",
        "ofm_inner_state_inference_guard": "facial_motion_inner_state_not_claimed",
        "uao_weapon_event_guard": "weapon_event_safe",
        "ubp_embodiment_capability_guard": "resource_capacity_within_declared",
        "uer_narrative_inference_guard": "narrative_effects_absent",
        "uer_weapon_role_target_guard": "weapon_role_target_safe",
        "ugf_context_binding_guard": "gesture_context_bound",
        "ugf_cultural_emblem_guard": "gesture_cultural_emblem_absent",
        "usc_cbg_orphan_novelty_guard": "bridge_path_connected",
        "usc_cbg_pixel_grounded_bridge_guard": "bridge_pixel_grounded",
        "usc_contact_contact_readability_gate": "contact_pixel_grounded",
        "usc_contact_reachable_contact_guard": "contact_resource_within_capacity",
        "usc_ecs_crop_safe_evidence_guard": "consequence_review_scale_declared",
        "usc_ecs_event_edge_guard": "atom_event_edges_connected",
        "usc_lexical_sense_ambiguity_guard": "prop_literal_sense_bound",
        "usc_relation_relation_truth_guard": "relation_event_edges_connected",
        "usc_sdc_hard_gate_invariance_guard": "creativity_invariant_pool_traced",
        "usc_sdc_remote_single_premise_guard": "remote_budget_within_global",
        "usc_sdc_visible_bridge_requirement_guard": "remote_premise_has_visible_bridge",
        "usc_sptg_capability_resource_gate": "resource_claims_within_capability",
        "usc_sptg_explicit_identity_core_guard": "identity_core_preserved",
        "usc_sptg_physical_relation_gate": "physical_relation_grounded",
        "ush_history_inference_guard": "history_claim_pixel_grounded",
        "usl_policy_separation_guard": "local_policy_authority_separated",
        "usl_theme_hijack_guard": "theme_load_within_limit",
    }
)

ENTRY_BRIDGE_TYPES = ("affordance", "motivation", "identity_contrast")
MEDIATION_BRIDGE_TYPES = ("mechanics", "ownership")
EXIT_BRIDGE_TYPES = ("state_change", "consequence")
KNOWN_BRIDGE_TYPES = {
    *ENTRY_BRIDGE_TYPES,
    *MEDIATION_BRIDGE_TYPES,
    *EXIT_BRIDGE_TYPES,
}
CONTEXT_PROFILE_CARRIER_CANDIDATE_IDS = frozenset(
    {
        "usc_cbg_affordance_bridge_atom",
        "usc_cbg_consequence_bridge_atom",
        "usc_cbg_identity_contrast_bridge_atom",
        "usc_cbg_mechanics_bridge_atom",
        "usc_cbg_motivation_bridge_atom",
        "usc_cbg_state_change_bridge_atom",
    }
)
MAX_CONTEXT_PROFILE_CARRIERS = len(CONTEXT_PROFILE_CARRIER_CANDIDATE_IDS)
GLOBAL_OPTIONAL_REMOTE_MAX = 1

ENTITY_RESOURCE_KINDS = {
    "manipulator",
    "attention_channel",
    "head_orientation",
    "support_contact",
    "mouth",
    "appendage",
    "locomotor_contact",
    "facial_display",
    "body_contour_display",
    "internal_luminance_display",
    "wing_appendage",
    "body_orientation",
    "light_emission",
    "surface_signal",
    "mobile_ear_pair",
    "wing_axis_pair",
    "tail_axis",
    "mechanical_state_displacement",
    "external_anchor",
}
SCENE_RESOURCE_KINDS = {
    "focal_primary",
    "focal_secondary",
    "foreground_salience",
    "event_peak",
    "prop_slot",
}

SUPPORTED_PREDICATE_KINDS = {
    "slot",
    "event_role",
    "capability",
    "resource_available",
    "context",
    "candidate",
    "candidate_tag",
    "guard_contract",
    "facet_evidence",
    "normalized_prop_concept",
    "policy",
    "cardinality",
    "bridge",
    "visible_evidence",
    "rule",
    "axis_max",
    "axis_sum",
}

SLOT_FOR_FACET = {
    "expression": "expression",
    "perceived_affect": "expression",
    "attention": "expression",
    "pose": "pose",
    "gesture": "pose",
    "action": "action",
    "phase": "action",
    "contact": "relation",
    "relation": "relation",
    "prop": "prop",
    "prop_state": "prop",
    "environment": "environment",
    "consequence": "environment",
    "bridge": "environment",
    "salience": "environment",
}

# A fixed literal may authorize an observable realization in a different but
# semantically adjacent facet (for example, an action phrase can expose its
# release phase).  The table is deliberately closed: a data record cannot use
# an arbitrary source slot as authority for an unrelated visual mechanism.
LITERAL_REALIZATION_FACETS_BY_SLOT = MappingProxyType(
    {
        "expression": frozenset({"expression", "perceived_affect", "attention"}),
        "pose": frozenset({"pose", "gesture", "contact"}),
        "action": frozenset({"attention", "pose", "action", "phase", "contact", "consequence"}),
        "relation": frozenset({"relation", "attention", "contact"}),
        "prop": frozenset({"prop", "prop_state"}),
        "environment": frozenset({"environment", "consequence", "contact"}),
    }
)
LITERAL_REALIZATION_SCOPE_IDS = (
    "fixed_value_bindings",
    "slot_phrases",
    "request_text",
)
LITERAL_REALIZATION_MECHANISM_IDS = (
    "action_observable_relation",
    "prop_contact_region",
    "facial_asymmetry",
    "mixed_display",
    "nonhuman_light_display",
    "shared_attention",
    "shared_target_relation",
    "visible_support_map",
    "release_recovery_phase",
    "contact_commitment_phase",
    "material_leak_trace",
    "environment_response",
    "directed_recipient_effect",
    "environmental_support_contact",
    "multi_contact_support",
    "handoff_chain",
    "visible_wear",
    "visible_repair",
    "inactive_hazard_orientation",
    "directed_attention",
    "typed_prop_identity",
    "context_anchor_relation",
    "material_identity_boundary",
    "functional_configuration_state",
    "layered_state_history",
    "locomotor_surface_path",
)
MAX_LITERAL_REALIZATION_ATOMS_PER_FACET = 2
MAX_LITERAL_REALIZATION_ATOMS_TOTAL = 10
MAX_SELECTED_VISUAL_ATOMS_TOTAL = 18
MAX_SELECTED_RESOURCE_CLAIMS_TOTAL = 32
NEUTRAL_FIXED_VALUE_PROJECTION_GROUPS: Mapping[str, tuple[str, ...]] = MappingProxyType({})

_HEX_DIGITS = frozenset("0123456789abcdef")
_MISSING = object()


class UniversalSceneRuntimeError(Exception):
    """Base failure with a stable category for a wrapping CLI."""

    exit_code = 1


class InputContractError(UniversalSceneRuntimeError):
    """The caller supplied an invalid or over-claiming scene contract."""

    exit_code = 2


class AssetValidationError(UniversalSceneRuntimeError):
    """A universal asset is missing, malformed, or internally inconsistent."""

    exit_code = 3


class SelectionError(UniversalSceneRuntimeError):
    """No coherent one-event selection satisfies all immutable gates."""

    exit_code = 4


@dataclass(frozen=True)
class UniversalSceneAssets:
    """Validated immutable asset view plus raw-byte hashes."""

    asset_dir: Path | None
    candidates: Mapping[str, Any]
    compatibility: Mapping[str, Any]
    semantic_bindings: Mapping[str, Any]
    candidate_by_id: Mapping[str, Mapping[str, Any]]
    proposal_by_id: Mapping[str, Mapping[str, Any]]
    prop_by_id: Mapping[str, Mapping[str, Any]]
    embodiment_by_id: Mapping[str, Mapping[str, Any]]
    prop_sense_by_catalog_id: Mapping[str, tuple[Mapping[str, Any], ...]]
    capability_assertions_by_id: Mapping[str, tuple[Mapping[str, Any], ...]]
    visual_carrier_by_candidate_id: Mapping[str, Mapping[str, Any]]
    resource_carrier_by_kind: Mapping[str, Mapping[str, Any]]
    asset_hashes: Mapping[str, str]

    @property
    def hashes(self) -> Mapping[str, str]:
        """Alias used by v3 pack assembly."""

        return self.asset_hashes


@dataclass(frozen=True)
class ValidatedSceneContract:
    """Canonical deep copy of a validated literal-bound contract."""

    contract: Mapping[str, Any]
    request_text: str
    sha256: str
    request_sha256: str
    slot_by_id: Mapping[str, Mapping[str, Any]]
    role_by_id: Mapping[str, Mapping[str, Any]]
    participant_by_role: Mapping[str, Mapping[str, Any]]
    entity_by_id: Mapping[str, Mapping[str, Any]]
    capability_capacities: tuple[Mapping[str, Any], ...]


def _normalize_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _semantic_tokens(value: str) -> tuple[str, ...]:
    normalized = _normalize_text(value)
    for delimiter in ("_", "-", "/", ".", ":"):
        normalized = normalized.replace(delimiter, " ")
    return tuple(normalized.split())


def _contains_token_subsequence(
    haystack: Sequence[str],
    needle: Sequence[str],
) -> bool:
    if not needle or len(needle) > len(haystack):
        return False
    return any(
        tuple(haystack[index:index + len(needle)]) == tuple(needle)
        for index in range(len(haystack) - len(needle) + 1)
    )


def _ascii_alnum_tokens(value: str) -> tuple[str, ...]:
    """Return closed ASCII word tokens for literal catalog binding.

    ASCII catalog aliases are matched as complete token subsequences so a
    semantic ``apple`` cannot be authenticated by a literal such as
    ``pineapple``.  Non-ASCII aliases use the deliberately separate normalized
    substring rule in ``_literal_catalog_alias_match`` because CJK scripts do
    not consistently expose whitespace-delimited word boundaries.
    """

    normalized = unicodedata.normalize("NFKC", value).casefold()
    return tuple(
        "".join(
            character if character.isascii() and character.isalnum() else " "
            for character in normalized
        ).split()
    )


def _literal_catalog_alias_match(alias: str, phrase: str) -> bool:
    normalized_alias = _normalize_text(alias)
    normalized_phrase = _normalize_text(phrase)
    if not normalized_alias or not normalized_phrase:
        return False
    if normalized_alias.isascii():
        return _contains_token_subsequence(
            _ascii_alnum_tokens(normalized_phrase),
            _ascii_alnum_tokens(normalized_alias),
        )
    # Hangul and kana catalog aliases need a word-boundary analogue.  A raw
    # substring promotes unrelated compounds (for example ``망치상어``) into a
    # hammer prop.  Accept a delimited occurrence or a reviewed grammatical
    # suffix, while leaving Chinese/Japanese unsegmented prose conservative.
    suffixes = (
        "을", "를", "이", "가", "은", "는", "과", "와", "의", "에",
        "에서", "에게", "으로", "로", "도", "만", "처럼", "보다", "랑",
        "이라고", "라고", "이며", "이나", "라도", "까지", "부터", "조차",
        "마저", "께서", "한테", "하고", "を", "が", "は", "の", "に",
        "で", "と", "も", "へ",
    )
    start = 0
    while True:
        index = normalized_phrase.find(normalized_alias, start)
        if index < 0:
            return False
        before = normalized_phrase[index - 1:index]
        after_index = index + len(normalized_alias)
        after = normalized_phrase[after_index:]
        before_ok = not before or before.isspace() or not before.isalnum()
        after_ok = (
            not after
            or after[0].isspace()
            or not after[0].isalnum()
            or any(after.startswith(suffix) for suffix in suffixes)
        )
        if before_ok and after_ok:
            return True
        start = index + 1


_LITERAL_CLAUSE_SEPARATORS = (
    ".", ",", ";", ":", "!", "?", "。", "，", "；", "：", "！", "？",
    " — ", " – ", " but ", " and ", " then ", " while ", " however ",
    " whereas ", " and then ", " even though ", " although ",
    " 하지만 ", " 그러나 ", " 반면 ", " 동안 ", "하면서 ", "하고 ",
    " しかし ", " 一方 ", " ながら ", " 但 ", " 但是 ", " 然而 ", " 同时 ",
)
_LITERAL_AUTHENTICATION_HARD_SEPARATORS = (
    ".", ";", ":", "!", "?", "。", "；", "：", "！", "？",
    " but ", " however ", " although ", " even though ",
    " 하지만 ", " 그러나 ", " 반면 ",
    " しかし ", " 一方 ", " 但 ", " 但是 ", " 然而 ",
)


def _normalized_alias_spans(alias: str, phrase: str) -> tuple[tuple[int, int], ...]:
    """Return every boundary-valid normalized alias span."""

    normalized_alias = _normalize_text(alias)
    normalized_phrase = _normalize_text(phrase)
    if not normalized_alias or not normalized_phrase:
        return ()
    result: list[tuple[int, int]] = []
    start = 0
    while True:
        index = normalized_phrase.find(normalized_alias, start)
        if index < 0:
            break
        fragment = normalized_phrase[index:index + len(normalized_alias)]
        # Reuse the single-match boundary contract on a local context.  The
        # surrounding padding preserves beginning/end word boundaries.
        context_start = max(0, index - 1)
        context_end = min(len(normalized_phrase), index + len(normalized_alias) + 8)
        context = normalized_phrase[context_start:context_end]
        if _literal_catalog_alias_match(fragment, context):
            result.append((index, index + len(normalized_alias)))
        start = index + max(1, len(normalized_alias))
    return tuple(result)


def _normalized_substring_spans(value: str, phrase: str) -> tuple[tuple[int, int], ...]:
    """Return every normalized substring span without promoting it generally."""

    normalized_value = _normalize_text(value)
    normalized_phrase = _normalize_text(phrase)
    if not normalized_value or not normalized_phrase:
        return ()
    result: list[tuple[int, int]] = []
    start = 0
    while True:
        index = normalized_phrase.find(normalized_value, start)
        if index < 0:
            return tuple(result)
        result.append((index, index + len(normalized_value)))
        start = index + max(1, len(normalized_value))


def _literal_alias_occurrence_polarities(
    phrase: str,
    aliases: Sequence[str],
    assets: UniversalSceneAssets,
    *,
    include_target_absence: bool = False,
    include_target_substitution: bool = False,
    allow_postposed_logical: bool = True,
    allow_korean_postposed_copular: bool = False,
    allow_authenticated_nonascii_substrings: bool = False,
    allow_reviewed_nonascii_marker_affixes: bool = False,
    postposed_logical_barrier_aliases: Sequence[str] = (),
) -> tuple[str, ...]:
    """Classify every reviewed alias occurrence as affirmative or negated.

    The scope is occurrence-local.  Coordination and punctuation delimiters
    prevent an earlier ``no`` from negating a later positive reassertion, and
    a short token/character window prevents an unrelated clause noun from
    borrowing the marker.
    """

    normalized = _normalize_text(phrase)
    marker_fields = ["logical_values"]
    if include_target_absence:
        marker_fields.append("target_absence_values")
    marker_specs: list[tuple[str, str | None]] = [
        (str(marker), None)
        for record in assets.semantic_bindings["literal_polarity_contract"]["negative_markers"]
        for field in marker_fields
        for marker in record[field]
    ]
    if include_target_substitution:
        marker_specs.extend(
            (
                str(marker["value"]),
                str(marker["marker_position_relative_to_negated_target"]),
            )
            for record in assets.semantic_bindings["literal_polarity_contract"]["negative_markers"]
            for marker in record["target_substitution_values"]
        )
    directional_marker_spans = {
        span
        for marker, marker_position in marker_specs
        if marker_position is not None
        for span in _normalized_substring_spans(marker, normalized)
    }
    separator_spans: list[tuple[int, int]] = []
    for separator in _LITERAL_CLAUSE_SEPARATORS:
        normalized_separator = unicodedata.normalize("NFKC", separator).casefold()
        if not normalized_separator:
            continue
        cursor = 0
        while True:
            index = normalized.find(normalized_separator, cursor)
            if index < 0:
                break
            separator_spans.append((index, index + len(normalized_separator)))
            cursor = index + len(normalized_separator)
    separator_spans.sort()

    def local_bounds(start: int, end: int) -> tuple[int, int]:
        left = max((boundary_end for _, boundary_end in separator_spans if boundary_end <= start), default=0)
        right = min((boundary_start for boundary_start, _ in separator_spans if boundary_start >= end), default=len(normalized))
        return left, right

    results: list[tuple[int, str]] = []
    for alias in aliases:
        alias_spans = set(_normalized_alias_spans(str(alias), normalized))
        if allow_authenticated_nonascii_substrings and not str(alias).isascii():
            # Contract semantic anchors have already been validated as exact
            # substrings of their own bound request phrase.  Permit their
            # Hangul/kana/han stems to survive ordinary grammatical suffixes
            # (for example ``충돌`` in ``충돌하지``), without weakening the
            # catalog matcher used for free-form prop and identity aliases.
            alias_spans.update(_normalized_substring_spans(str(alias), normalized))
        # CJK substitution prose is commonly unsegmented.  Raw substring
        # matching remains unsafe as a general catalog rule, but exact
        # adjacency to a reviewed directional marker authenticates the target
        # occurrence without promoting unrelated compounds elsewhere.
        alias_spans.update(
            (start, end)
            for start, end in _normalized_substring_spans(str(alias), normalized)
            if any(
                marker_end == start or marker_start == end
                for marker_start, marker_end in directional_marker_spans
            )
        )
        for start, end in sorted(alias_spans):
            left, right = local_bounds(start, end)
            clause = normalized[left:right]
            alias_start = start - left
            alias_end = end - left
            clause_directional_marker_spans = {
                span
                for marker, marker_position in marker_specs
                if marker_position is not None
                for span in _normalized_substring_spans(marker, clause)
            }
            clause_barrier_spans = {
                span
                for barrier_alias in postposed_logical_barrier_aliases
                for span in (
                    _normalized_substring_spans(str(barrier_alias), clause)
                    if not str(barrier_alias).isascii()
                    else _normalized_alias_spans(str(barrier_alias), clause)
                )
            }
            negated = False
            for marker, marker_position in marker_specs:
                marker_spans = list(
                    _normalized_substring_spans(marker, clause)
                    if marker_position is not None
                    else _normalized_alias_spans(marker, clause)
                )
                if (
                    marker_position is None
                    and allow_reviewed_nonascii_marker_affixes
                    and not marker.isascii()
                ):
                    marker_spans.extend(_normalized_substring_spans(marker, clause))
                # Korean contrastive copular negation inflects the reviewed
                # logical root ``아니`` as ``아니라``.  Only semantic-effect
                # composition opts into this implicit morphology; target
                # substitution uses its explicit directional marker record.
                if allow_korean_postposed_copular and marker == "아니":
                    marker_spans.extend(_normalized_alias_spans("아니라", clause))
                for marker_start, marker_end in sorted(set(marker_spans)):
                    if marker_position is None and any(
                        directional_start <= marker_start
                        and marker_end <= directional_end
                        for directional_start, directional_end in clause_directional_marker_spans
                    ):
                        # A grammatical root such as Korean ``아니`` may be
                        # contained in the reviewed directional substitution
                        # marker ``아니라``.  The directional record owns that
                        # occurrence; replaying it as a broad logical marker
                        # would negate both sides of the contrast.
                        continue
                    if (
                        marker_position is None
                        and marker == "않"
                        and marker_end <= alias_start
                    ):
                        # Korean ``않`` is a postposed auxiliary attached to
                        # the preceding predicate stem.  Its reviewed raw-stem
                        # match (``않고``, ``않아``) must not leak forward into
                        # later affirmative nouns in the same phrase.
                        continue
                    if (
                        marker_position is None
                        and marker_start >= alias_end
                        and any(
                            alias_end <= barrier_start
                            and barrier_end <= marker_start
                            for barrier_start, barrier_end in clause_barrier_spans
                        )
                    ):
                        # A fixed semantic record may explicitly preserve an
                        # affirmative object/state while negating a later
                        # predicate (``contact and load do not conflict`` or
                        # ``broken umbrella, without unfolding``).  A reviewed
                        # negated anchor between this affirmative target and a
                        # postposed logical marker is the scope boundary.
                        continue
                    if marker_position == "before" and marker_end > alias_start:
                        continue
                    if marker_position == "after" and marker_start < alias_end:
                        continue
                    if (
                        marker_position is None
                        and marker_start >= alias_end
                        and not allow_postposed_logical
                    ):
                        continue
                    if marker_end <= alias_start:
                        between = clause[marker_end:alias_start]
                    elif marker_start >= alias_end:
                        between = clause[alias_end:marker_start]
                    else:
                        between = ""
                    if marker_end <= alias_start or marker_start >= alias_end:
                        if marker.isascii() and str(alias).isascii():
                            close = len(_ascii_alnum_tokens(between)) <= 2
                        elif marker_position is not None:
                            # A directional substitution marker owns only its
                            # nearest CJK/Korean target chunk.  The larger
                            # logical-negation window would make ``broken
                            # lever ... tool 아니라 evidence`` negate the
                            # concrete lever as well as the immediately
                            # preceding generic tool role.
                            close = len(between.replace(" ", "")) <= 2
                        else:
                            close = len(between.replace(" ", "")) <= 8
                        if close:
                            negated = True
                            break
                if negated:
                    break
            results.append((start, "negated" if negated else "affirmative"))
    # Overlapping target aliases can describe the same occurrence.  Polarity
    # is still stable, so only exact (position, polarity) duplicates collapse.
    return tuple(polarity for _, polarity in sorted(set(results)))


def _literal_clauses(value: str) -> tuple[str, ...]:
    normalized = _normalize_text(value)
    for separator in _LITERAL_CLAUSE_SEPARATORS:
        normalized = normalized.replace(separator, "\n")
    return tuple(part.strip() for part in normalized.splitlines() if part.strip())


def _literal_authentication_clauses(value: str) -> tuple[str, ...]:
    """Split only hard sentence/contrast boundaries for AND-group proofs."""

    normalized = _normalize_text(value)
    for separator in _LITERAL_AUTHENTICATION_HARD_SEPARATORS:
        normalized = normalized.replace(_normalize_text(separator), "\n")
    return tuple(part.strip() for part in normalized.splitlines() if part.strip())


def _clause_has_reviewed_negative_marker(
    clause: str,
    assets: UniversalSceneAssets,
) -> bool:
    return any(
        _literal_catalog_alias_match(str(marker), clause)
        for record in assets.semantic_bindings["literal_polarity_contract"]["negative_markers"]
        for field in (
            "logical_values",
            "target_absence_values",
        )
        for marker in record[field]
    ) or any(
        _literal_catalog_alias_match(str(marker["value"]), clause)
        for record in assets.semantic_bindings["literal_polarity_contract"]["negative_markers"]
        for marker in record["target_substitution_values"]
    )


def _literal_group_matches(group: Sequence[str], phrase: str) -> bool:
    """Return whether one reviewed OR-group is present in one literal span."""

    return any(_literal_catalog_alias_match(str(alternative), phrase) for alternative in group)


def _required_literal_groups_match(
    groups: Sequence[Sequence[str]],
    phrases: Sequence[str],
) -> bool:
    """Require every AND-group inside the same literal-bound request span."""

    return any(
        all(_literal_group_matches(group, str(phrase)) for group in groups)
        for phrase in phrases
    )


def _profile_literal_matches(profile: Mapping[str, Any], phrases: Sequence[str]) -> bool:
    return _required_literal_groups_match(profile["required_literal_groups"], phrases)


def _affirmative_required_literal_groups_match(
    groups: Sequence[Sequence[str]],
    phrases: Sequence[str],
    assets: UniversalSceneAssets,
) -> bool:
    """Match every reviewed group affirmatively inside one authenticated span."""

    return any(
        all(
            (
                polarities := _literal_alias_occurrence_polarities(
                    str(phrase),
                    [str(alternative) for alternative in group],
                    assets,
                    allow_postposed_logical=False,
                    allow_korean_postposed_copular=False,
                )
            )
            and set(polarities) == {"affirmative"}
            for group in groups
        )
        for phrase in phrases
    )


def _polarized_required_literal_group_matches(
    group_index: int,
    group: Mapping[str, Any],
    groups: Sequence[Mapping[str, Any]],
    phrase: str,
    assets: UniversalSceneAssets,
) -> bool:
    """Replay one typed group against one literal-bound phrase."""

    peer_anchor_aliases = [
        str(value)
        for peer_index, peer_group in enumerate(groups)
        if peer_index != group_index
        for value in peer_group["alternatives"]
    ]
    polarities = _literal_alias_occurrence_polarities(
        str(phrase),
        [str(value) for value in group["alternatives"]],
        assets,
        # Visibility modifiers such as ``covered``/``가려진`` are not a
        # generic existential-negation grammar.  Typed semantic anchors use
        # logical or directional substitution markers; target-specific
        # visibility closure remains in reviewed slot/role target profiles.
        include_target_absence=False,
        include_target_substitution=True,
        allow_postposed_logical=True,
        allow_korean_postposed_copular=False,
        allow_authenticated_nonascii_substrings=True,
        allow_reviewed_nonascii_marker_affixes=True,
        # A postposed logical auxiliary owns the nearest reviewed target span.
        # Earlier object/state anchors do not borrow the negation across a
        # later predicate anchor in the same phrase.
        postposed_logical_barrier_aliases=peer_anchor_aliases,
    )
    return bool(polarities) and set(polarities) == {
        str(group["required_polarity"])
    }


def _polarized_required_literal_groups_match(
    groups: Sequence[Mapping[str, Any]],
    phrases: Sequence[str],
    assets: UniversalSceneAssets,
) -> bool:
    """Require every typed realization group in one authenticated span."""

    return any(
        all(
            _polarized_required_literal_group_matches(
                group_index,
                group,
                groups,
                str(phrase),
                assets,
            )
            for group_index, group in enumerate(groups)
        )
        for phrase in phrases
    )


def _contract_semantic_anchor_groups_match(
    groups: Sequence[Mapping[str, Any]],
    phrases: Sequence[str],
    assets: UniversalSceneAssets,
) -> bool:
    """Authenticate each anchor inside one phrase owned by the same record."""

    return all(
        any(
            _polarized_required_literal_group_matches(
                group_index,
                group,
                groups,
                str(phrase),
                assets,
            )
            for phrase in phrases
        )
        for group_index, group in enumerate(groups)
    )


def _literal_visual_realization_value_bindings(
    profile: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> list[Mapping[str, Any]]:
    """Return only exact v2 value bindings that own a reviewed mechanism."""

    slot_id = str(profile["source_slot_id"])
    slot = validated.slot_by_id[slot_id]
    if slot["state"] != "fixed":
        return []
    for participant in profile["participant_roles"]:
        binding = validated.participant_by_role[str(participant["role_id"])]
        if not binding["entity_ids"] or (
            participant["entity_quantifier"] == "primary"
            and binding["primary_entity_id"] is None
        ):
            return []
    scope = str(profile["literal_scope"])
    groups = profile["required_literal_groups"]
    if scope == "fixed_value_bindings":
        if not slot["value_phrase_bindings"]:
            return []
        # The opaque-prop neutral projection additionally requires an
        # authenticated fixed target or instrument phrase for the same literal
        # span.  A free noun in a fixed prop slot is not permission to invent
        # handling semantics.
        if profile["mechanism_class_id"] == "prop_contact_region":
            if any(str(value_id) in assets.prop_by_id for value_id in slot["value_ids"]):
                return []
            slot_phrases = {
                _normalize_text(str(phrase))
                for binding in slot["value_phrase_bindings"]
                for phrase in binding["request_phrases"]
            }
            role_phrases = {
                _normalize_text(str(phrase))
                for role_id in ("target", "instrument")
                for role in (validated.role_by_id[role_id],)
                if role["state"] == "fixed"
                for phrase in role["request_phrases"]
            }
            if not slot_phrases.intersection(role_phrases):
                return []
        if not groups:
            return [
                _deep_canonical_copy(binding)
                for binding in slot["value_phrase_bindings"]
            ]
        return [
            _deep_canonical_copy(binding)
            for binding in slot["value_phrase_bindings"]
            if _polarized_required_literal_groups_match(
                groups,
                [str(phrase) for phrase in binding["request_phrases"]],
                assets,
            )
        ]
    phrases = (
        [str(phrase) for phrase in slot["request_phrases"]]
        if scope == "slot_phrases"
        else list(_literal_authentication_clauses(validated.request_text))
    )
    if not _polarized_required_literal_groups_match(groups, phrases, assets):
        return []
    if scope == "slot_phrases":
        matched = [
            _deep_canonical_copy(binding)
            for binding in slot["value_phrase_bindings"]
            if _polarized_required_literal_groups_match(
                groups,
                [str(phrase) for phrase in binding["request_phrases"]],
                assets,
            )
        ]
        if matched:
            return matched
    return [
        _deep_canonical_copy(binding)
        for binding in slot["value_phrase_bindings"]
    ]


def _literal_visual_realization_profile_matches(
    profile: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> bool:
    """Replay one mandatory data-owned literal realization requirement."""

    return bool(
        _literal_visual_realization_value_bindings(profile, validated, assets)
    )


def _matching_literal_visual_realization_profiles(
    candidate: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> list[Mapping[str, Any]]:
    """Return the unambiguous matched requirement owning one candidate."""

    matches = [
        profile
        for profile in assets.semantic_bindings["literal_visual_realization_profiles"]
        if candidate["id"] in profile["candidate_group"]
        and _literal_visual_realization_profile_matches(profile, validated, assets)
    ]
    matches.sort(key=lambda item: (int(item["selection_rank"]), str(item["id"])))
    if len(matches) > 1:
        raise SelectionError(
            f"candidate {candidate['id']} has ambiguous literal realization profiles"
        )
    return matches


def _literal_realization_parameters(
    profile: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> dict[str, Any]:
    slot_id = str(profile["source_slot_id"])
    resolved_owner_refs: list[dict[str, str]] = []
    for participant in profile["participant_roles"]:
        role_id = str(participant["role_id"])
        binding = validated.participant_by_role[role_id]
        if participant["entity_quantifier"] == "primary":
            entity_ids = [str(binding["primary_entity_id"])]
        else:
            entity_ids = [str(entity_id) for entity_id in binding["entity_ids"]]
        resolved_owner_refs.extend(
            {"role_id": role_id, "entity_id": entity_id}
            for entity_id in entity_ids
        )
    return {
        "literal_realization_profile_id": str(profile["id"]),
        "mechanism_class_id": str(profile["mechanism_class_id"]),
        "source_slot_id": slot_id,
        "resolved_owner_refs": resolved_owner_refs,
        "value_phrase_bindings": _literal_visual_realization_value_bindings(
            profile, validated, assets
        ),
        "request_text_sha256": validated.request_sha256,
    }


def _context_literal_profile_matches(
    profile: Mapping[str, Any],
    request_text: str,
    assets: UniversalSceneAssets,
) -> bool:
    """Authenticate one executable context value from reviewed request prose."""

    expected_polarity = str(profile["polarity"])
    normalized = _normalize_text(request_text)
    hard_separators = (
        ".", ";", ":", "!", "?", "。", "；", "：", "！", "？",
        " but ", " while ", " however ", " although ",
        " even though ", " 하지만 ", " 그러나 ", " 동안 ",
        " しかし ", " 一方 ", " 但是 ", " 然而 ", " 同时 ",
    )
    separator_spans = sorted(
        {
            (index, index + len(separator))
            for separator in hard_separators
            for index in range(len(normalized))
            if normalized.startswith(separator, index)
        }
    )
    if expected_polarity == "negated":
        groups = profile["required_literal_groups"]
        if len(groups) != 2:
            return False
        target_spans = sorted(
            {
                span
                for alternative in groups[0]
                for span in _normalized_alias_spans(str(alternative), normalized)
            }
        )
        directive_spans = sorted(
            {
                span
                for alternative in groups[1]
                for span in _normalized_alias_spans(str(alternative), normalized)
            }
        )
        if not target_spans or not directive_spans:
            return False
        affirmative_conflict_terms = (
            "include", "add", "show", "depict", "visible", "present",
            "넣어", "추가", "보여", "사용해", "사용한다",
            "追加", "表示", "描く", "包含", "添加", "展示",
        )
        for target_start, target_end in target_spans:
            left = max(
                (end for _start, end in separator_spans if end <= target_start),
                default=0,
            )
            right = min(
                (start for start, _end in separator_spans if start >= target_end),
                default=len(normalized),
            )
            local_directives = [
                (start, end)
                for start, end in directive_spans
                if left <= start and end <= right
            ]
            if not local_directives:
                return False
            if not any(
                (
                    len(_ascii_alnum_tokens(normalized[min(target_end, end):max(target_start, start)]))
                    <= 16
                    if normalized[target_start:target_end].isascii()
                    else len(
                        normalized[min(target_end, end):max(target_start, start)].replace(" ", "")
                    ) <= 64
                )
                for start, end in local_directives
            ):
                return False
            local_clause = normalized[left:right]
            conflict_polarities = _literal_alias_occurrence_polarities(
                local_clause,
                affirmative_conflict_terms,
                assets,
                allow_korean_postposed_copular=True,
            )
            if "affirmative" in conflict_polarities:
                return False
            absence_polarities = _literal_alias_occurrence_polarities(
                local_clause,
                (
                    "omit", "remove", "exclude", "erase",
                    "빼", "제외", "생략", "지워",
                    "省く", "除外", "削除", "省略", "排除", "删除",
                ),
                assets,
                allow_korean_postposed_copular=True,
            )
            if "negated" in absence_polarities:
                return False
        return True
    if expected_polarity == "affirmative":
        target_spans = sorted(
            {
                span
                for group in profile["required_literal_groups"]
                for alternative in group
                for span in _normalized_alias_spans(str(alternative), normalized)
            }
        )
        directive_spans = sorted(
            {
                span
                for record in assets.semantic_bindings["literal_polarity_contract"]["negative_markers"]
                for alternative in record["affirmative_conflict_values"]
                for span in _normalized_alias_spans(str(alternative), normalized)
            }
        )
        intervening_affirmative_terms = (
            "include", "included", "add", "added", "show", "shown",
            "depict", "depicted", "visible", "present", "use", "used",
            "넣어", "추가", "보여", "사용해", "사용한다",
            "追加", "表示", "描く", "含める", "包含", "添加", "展示",
        )
        for target_start, target_end in target_spans:
            left = max(
                (end for _start, end in separator_spans if end <= target_start),
                default=0,
            )
            right = min(
                (start for start, _end in separator_spans if start >= target_end),
                default=len(normalized),
            )
            for directive_start, directive_end in directive_spans:
                if not (left <= directive_start and directive_end <= right):
                    continue
                between_start = min(target_end, directive_end)
                between_end = max(target_start, directive_start)
                between = normalized[between_start:between_end]
                close_enough = (
                    len(_ascii_alnum_tokens(between)) <= 16
                    if normalized[target_start:target_end].isascii()
                    else len(between.replace(" ", "")) <= 64
                )
                if not close_enough:
                    continue
                if _literal_alias_occurrence_polarities(
                    between,
                    intervening_affirmative_terms,
                    assets,
                    allow_postposed_logical=False,
                    allow_korean_postposed_copular=False,
                ):
                    continue
                return False
    for clause in _literal_clauses(request_text):
        matched = True
        for group in profile["required_literal_groups"]:
            polarities = _literal_alias_occurrence_polarities(
                clause,
                [str(value) for value in group],
                assets,
                allow_postposed_logical=expected_polarity != "affirmative",
                allow_korean_postposed_copular=expected_polarity != "affirmative",
            )
            if expected_polarity == "affirmative":
                if not polarities or set(polarities) != {"affirmative"}:
                    matched = False
                    break
            elif not polarities or set(polarities) != {"negated"}:
                matched = False
                break
        if matched:
            return True
    return False


def _capability_profile_literal_matches(
    profile: Mapping[str, Any],
    phrases: Sequence[str],
    assets: UniversalSceneAssets,
) -> bool:
    """Match a reviewed capability assertion with its literal polarity.

    Available profiles require an affirmative occurrence from every AND-group;
    unavailable profiles encode an absence phrase and are invalidated by an
    additional nearby negator (for example ``not limbless``).  Mixed positive
    and negated occurrences fail closed in both directions.
    """

    assertion = str(profile["assertion"])
    for phrase in phrases:
        phrase_matches = True
        for group in profile["required_literal_groups"]:
            polarities = _literal_alias_occurrence_polarities(
                str(phrase),
                [str(item) for item in group],
                assets,
            )
            if assertion == "available":
                if not polarities or set(polarities) != {"affirmative"}:
                    phrase_matches = False
                    break
            else:
                # The reviewed alternatives themselves denote absence.  A
                # surrounding negator reverses that assertion.
                if not polarities or "negated" in polarities:
                    phrase_matches = False
                    break
        if phrase_matches:
            return True
    return False


def _semantic_value_has_token(value_ids: Sequence[str], token: str) -> bool:
    needle = _semantic_tokens(token)
    return any(
        _contains_token_subsequence(_semantic_tokens(str(value_id)), needle)
        for value_id in value_ids
    )


def _distinct_prop_sense_matches(
    profile: Mapping[str, Any],
    literal_phrases: Sequence[str],
    semantic_values: Sequence[str],
) -> bool:
    aliases = [
        str(alias)
        for record in profile["literal_aliases"]
        for alias in record["values"]
    ]
    return (
        any(
            _literal_catalog_alias_match(alias, phrase)
            for alias in aliases
            for phrase in literal_phrases
        )
        and any(
            _semantic_value_has_token(semantic_values, str(token))
            for token in profile["accepted_semantic_tokens"]
        )
    )


def _literal_target_polarities(
    phrase: str,
    *,
    target_kind: str,
    target_id: str,
    assets: UniversalSceneAssets,
) -> tuple[str, ...]:
    contract = assets.semantic_bindings["literal_polarity_contract"]
    target = next(
        (
            profile
            for profile in contract["target_profiles"]
            if profile["target_kind"] == target_kind
            and profile["target_id"] == target_id
        ),
        None,
    )
    if target is None:
        raise InputContractError(
            f"semantic bindings lack a polarity target for {target_kind}:{target_id}"
        )
    return _literal_alias_occurrence_polarities(
        phrase,
        [str(alias) for alias in target["literal_alternatives"]],
        assets,
        include_target_absence=True,
        include_target_substitution=True,
    )


def _phrase_has_closed_polarity(
    phrase: str,
    *,
    target_kind: str,
    target_id: str,
    assets: UniversalSceneAssets,
) -> bool:
    polarities = _literal_target_polarities(
        phrase,
        target_kind=target_kind,
        target_id=target_id,
        assets=assets,
    )
    # Every target occurrence must be negated.  A later positive reassertion
    # invalidates the closure even when an earlier occurrence was negative.
    return bool(polarities) and set(polarities) == {"negated"}


def _literal_identity_carrier_groups(
    phrases: Sequence[str],
    assets: UniversalSceneAssets,
) -> list[list[str]]:
    """Bind identity prose to reviewed literals, never to caller-authored IDs."""

    reviewed_groups: list[list[str]] = []
    uncovered_phrases: list[str] = []
    for phrase in phrases:
        phrase_fully_covered = False
        for profile in assets.semantic_bindings["identity_literal_profiles"]:
            aliases = [
                str(alias)
                for record in profile["literal_aliases"]
                for alias in record["values"]
            ]
            polarities = _literal_alias_occurrence_polarities(
                str(phrase), aliases, assets
            )
            if not polarities or set(polarities) != {"affirmative"}:
                continue
            phrase_fully_covered = phrase_fully_covered or any(
                _normalize_text(alias) == _normalize_text(phrase)
                for alias in aliases
            )
            for group in profile["required_lexeme_groups"]:
                normalized_group = [str(item) for item in group]
                if normalized_group not in reviewed_groups:
                    reviewed_groups.append(normalized_group)
        if not phrase_fully_covered:
            uncovered_phrases.append(str(phrase))

    def collapse(groups: Sequence[Sequence[str]]) -> list[str]:
        words: list[str] = []
        for group in groups:
            for word in _normalize_text(str(group[0])).split():
                if word not in words:
                    words.append(word)
        return [" ".join(words)]

    raw_group_count = 1 if uncovered_phrases else 0
    reviewed_budget = 3 - raw_group_count
    if len(reviewed_groups) > reviewed_budget:
        if reviewed_budget == 1:
            reviewed_groups = [collapse(reviewed_groups)]
        else:
            reviewed_groups = [
                *reviewed_groups[:reviewed_budget - 1],
                collapse(reviewed_groups[reviewed_budget - 1:]),
            ]
    result = list(reviewed_groups)
    if uncovered_phrases:
        result.append(list(uncovered_phrases))
    if not result:
        raise SelectionError("literal-bound semantic carrier has no request phrase")
    return result[:3]


def _literal_value_carrier_groups(
    phrases: Sequence[str],
    semantic_values: Sequence[str],
    assets: UniversalSceneAssets,
) -> list[list[str]]:
    """Use catalog/sense semantics when reviewed, else retain the literal span."""

    result: list[list[str]] = []
    fully_covered = False
    exact_identity_groups: list[list[str]] = []
    all_phrases_identity_covered = bool(phrases)
    for phrase in phrases:
        phrase_covered = False
        for identity_profile in assets.semantic_bindings["identity_literal_profiles"]:
            aliases = [
                str(alias)
                for record in identity_profile["literal_aliases"]
                for alias in record["values"]
            ]
            if not any(
                _normalize_text(alias) == _normalize_text(str(phrase))
                for alias in aliases
            ):
                continue
            if set(
                _literal_alias_occurrence_polarities(str(phrase), aliases, assets)
            ) != {"affirmative"}:
                continue
            phrase_covered = True
            for group in identity_profile["required_lexeme_groups"]:
                normalized_group = [str(value) for value in group]
                if normalized_group not in exact_identity_groups:
                    exact_identity_groups.append(normalized_group)
        all_phrases_identity_covered = all_phrases_identity_covered and phrase_covered
    prop_ids = _semantic_prop_ids_from_values(semantic_values, assets)
    for prop_id in sorted(prop_ids):
        english_aliases = [
            str(alias)
            for record in assets.prop_by_id[prop_id]["aliases"]
            if record["locale"] == "en"
            for alias in record["values"]
        ]
        if english_aliases and english_aliases not in result:
            result.append(english_aliases)
        fully_covered = fully_covered or any(
            _normalize_text(alias) == _normalize_text(phrase)
            for alias in english_aliases
            for phrase in phrases
        )
    for profiles in assets.prop_sense_by_catalog_id.values():
        for profile in profiles:
            if _distinct_prop_sense_matches(profile, phrases, semantic_values):
                group = [str(token).replace("_", " ") for token in profile["accepted_semantic_tokens"]]
                if group not in result:
                    result.append(group)
                fully_covered = fully_covered or any(
                    _normalize_text(alias) == _normalize_text(phrase)
                    for record in profile["literal_aliases"]
                    for alias in record["values"]
                    for phrase in phrases
                )
    if result:
        result = result[:1]
        if not fully_covered and all_phrases_identity_covered:
            compact_terms: list[str] = []
            for group in exact_identity_groups:
                for token in _normalize_text(str(group[0])).split():
                    if token not in compact_terms:
                        compact_terms.append(token)
            result.append([" ".join(compact_terms)])
        elif not fully_covered:
            result.append([str(phrase) for phrase in phrases])
        return result
    return _literal_identity_carrier_groups(phrases, assets)[:2]


def _semantic_prop_ids_from_values(
    value_ids: Sequence[str],
    assets: UniversalSceneAssets,
) -> set[str]:
    value_token_sets = [_semantic_tokens(str(item)) for item in value_ids]
    result: set[str] = set()
    for prop_id, prop in assets.prop_by_id.items():
        prop_id_tokens = _semantic_tokens(prop_id)
        if prop_id_tokens and prop_id_tokens[0] == "prop":
            prop_id_tokens = prop_id_tokens[1:]
        semantic_names = [
            _semantic_tokens(value)
            for record in prop["aliases"]
            if record["locale"] == "en"
            for value in record["values"]
        ]
        semantic_names.append(prop_id_tokens)
        if any(
            _contains_token_subsequence(value_tokens, semantic_name)
            for value_tokens in value_token_sets
            for semantic_name in semantic_names
        ):
            result.add(str(prop_id))
    return result


def canonical_json_bytes(value: Any) -> bytes:
    """Return the single canonical JSON representation used for hashes."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _semantic_family_normalize(value: str | None) -> str:
    """Normalize one semantic-family value under the frozen v1 contract."""

    if value is None:
        return "null"
    normalized = unicodedata.normalize("NFKC", str(value)).casefold().strip()
    if normalized in {"$identity_actor", "$actor"}:
        return "$actor"
    if normalized in {"$scene_location", "$location"}:
        return "$location"
    normalized = normalized.replace("_", " ").replace("-", " ")
    return " ".join(normalized.split())


def _proposal_semantic_family_payload(
    profile: Mapping[str, Any],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Build the identifier-free, creativity-invariant family payload.

    Raw claims are deliberately aggregated without set-deduplication: equal
    exclusive claims from different member candidates consume twice, while
    equal shared claims consume their maximum.
    """

    reduced_claims: dict[tuple[str, str, str], int] = {}
    for candidate_id in profile["candidate_ids"]:
        candidate = candidate_by_id.get(str(candidate_id))
        if candidate is None:
            raise AssetValidationError(
                f"proposal semantic family references unknown candidate {candidate_id!r}"
            )
        for raw_claim in candidate["runtime_contract"]["resource_claims"]:
            if not isinstance(raw_claim, list) or len(raw_claim) != 4:
                raise AssetValidationError(
                    f"proposal semantic family candidate {candidate_id!r} has a malformed resource claim"
                )
            resource_kind, raw_owner_scope, amount, mode = raw_claim
            if (
                not isinstance(resource_kind, str)
                or not resource_kind
                or raw_owner_scope not in {"actor", "scene", *EVENT_ROLE_IDS}
                or mode not in {"exclusive", "shared"}
                or isinstance(amount, bool)
                or not isinstance(amount, int)
                or amount <= 0
            ):
                raise AssetValidationError(
                    f"proposal semantic family candidate {candidate_id!r} has an invalid resource claim"
                )
            owner_scope = (
                str(raw_owner_scope)
                if raw_owner_scope in {"actor", "scene"}
                else f"role:{_semantic_family_normalize(str(raw_owner_scope))}"
            )
            key = (
                owner_scope,
                _semantic_family_normalize(resource_kind),
                str(mode),
            )
            if mode == "exclusive":
                reduced_claims[key] = reduced_claims.get(key, 0) + amount
            else:
                reduced_claims[key] = max(reduced_claims.get(key, 0), amount)

    payload = {
        "schema": SEMANTIC_FAMILY_KEY_SCHEMA,
        "slot": _semantic_family_normalize(str(profile["slot_id"])),
        "prop_concept": _semantic_family_normalize(str(profile["value_id"])),
        "event_frame": {
            role_id: _semantic_family_normalize(profile["event_roles"][role_id])
            for role_id in EVENT_ROLE_IDS
        },
        "resource_footprint": [
            {
                "owner_scope": owner_scope,
                "resource_kind": resource_kind,
                "mode": mode,
                "amount": amount,
            }
            for (owner_scope, resource_kind, mode), amount in sorted(
                reduced_claims.items(),
                key=lambda item: item[0],
            )
        ],
    }
    return payload


def _proposal_semantic_family_signature(
    profile: Mapping[str, Any],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
) -> str:
    return canonical_sha256(
        _proposal_semantic_family_payload(profile, candidate_by_id)
    )


def _raw_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and set(value) <= _HEX_DIGITS
    )


def _require_mapping(value: Any, where: str, error_type: type[Exception]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise error_type(f"{where} must be an object")
    return value


def _require_list(value: Any, where: str, error_type: type[Exception]) -> list[Any]:
    if not isinstance(value, list):
        raise error_type(f"{where} must be an array")
    return value


def _require_exact_keys(
    value: Mapping[str, Any],
    keys: Iterable[str],
    where: str,
    error_type: type[Exception],
) -> None:
    expected = set(keys)
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise error_type(f"{where} key mismatch: missing={missing}, extra={extra}")


def _require_nonempty_string(value: Any, where: str, error_type: type[Exception]) -> str:
    if not isinstance(value, str) or not value.strip():
        raise error_type(f"{where} must be a non-empty string")
    return value


def _require_string_list(
    value: Any,
    where: str,
    error_type: type[Exception],
    *,
    allow_empty: bool = True,
    unique: bool = True,
) -> list[str]:
    items = _require_list(value, where, error_type)
    if not allow_empty and not items:
        raise error_type(f"{where} must not be empty")
    for index, item in enumerate(items):
        _require_nonempty_string(item, f"{where}[{index}]", error_type)
    if unique and len(items) != len(set(items)):
        raise error_type(f"{where} must not contain duplicates")
    return items


def _require_int_range(
    value: Any,
    low: int,
    high: int,
    where: str,
    error_type: type[Exception],
) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        raise error_type(f"{where} must be an integer in {low}..{high}")
    return value


def _require_number_range(
    value: Any,
    low: float,
    high: float,
    where: str,
    error_type: type[Exception],
) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise error_type(f"{where} must be a number in {low}..{high}")
    result = float(value)
    if not math.isfinite(result) or not low <= result <= high:
        raise error_type(f"{where} must be a finite number in {low}..{high}")
    return result


def _load_json_object(path: Path) -> tuple[Mapping[str, Any], bytes]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise AssetValidationError(f"cannot read universal asset {path}: {exc}") from exc
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AssetValidationError(f"universal asset is not UTF-8 JSON: {path}: {exc}") from exc
    return _require_mapping(value, str(path), AssetValidationError), raw


def _deep_canonical_copy(value: Any) -> Any:
    return json.loads(canonical_json_bytes(value).decode("utf-8"))


def _validate_literal_phrases(
    phrases: Any,
    concept_normalized: str,
    where: str,
    *,
    allow_empty: bool,
) -> list[str]:
    items = _require_string_list(
        phrases,
        where,
        InputContractError,
        allow_empty=allow_empty,
    )
    for index, phrase in enumerate(items):
        normalized = _normalize_text(phrase)
        if not normalized or normalized not in concept_normalized:
            raise InputContractError(
                f"{where}[{index}] is not a normalized literal substring of concept"
            )
    return items


def _validate_fact(
    value: Any,
    concept_normalized: str,
    where: str,
) -> Mapping[str, Any]:
    fact = _require_mapping(value, where, InputContractError)
    _require_exact_keys(fact, {"id", "request_phrases"}, where, InputContractError)
    _require_nonempty_string(fact["id"], f"{where}.id", InputContractError)
    _validate_literal_phrases(
        fact["request_phrases"],
        concept_normalized,
        f"{where}.request_phrases",
        allow_empty=False,
    )
    return fact


def _validate_contract_semantic_anchor_groups(
    value: Any,
    phrases: Sequence[str],
    *,
    fixed: bool,
    where: str,
    assets: UniversalSceneAssets,
) -> list[Mapping[str, Any]]:
    """Validate typed value authority against only its own literal spans."""

    groups = _require_list(value, where, InputContractError)
    if not fixed:
        if groups:
            raise InputContractError(f"{where} must be empty outside a fixed record")
        return []
    if not groups or len(groups) > 4:
        raise InputContractError(f"{where} must contain 1..4 typed semantic anchors")
    result: list[Mapping[str, Any]] = []
    signatures: set[tuple[tuple[str, ...], str]] = set()
    for index, raw_group in enumerate(groups):
        group_where = f"{where}[{index}]"
        group = _require_mapping(raw_group, group_where, InputContractError)
        _require_exact_keys(
            group,
            {"alternatives", "required_polarity"},
            group_where,
            InputContractError,
        )
        alternatives = _require_string_list(
            group["alternatives"],
            f"{group_where}.alternatives",
            InputContractError,
            allow_empty=False,
        )
        normalized_alternatives = tuple(_normalize_text(item) for item in alternatives)
        if len(normalized_alternatives) != len(set(normalized_alternatives)):
            raise InputContractError(f"{group_where}.alternatives contains duplicates")
        if any(
            not any(
                _normalize_text(alternative) in _normalize_text(str(phrase))
                for phrase in phrases
            )
            for alternative in alternatives
        ):
            raise InputContractError(
                f"{group_where}.alternatives must be literal substrings of this record"
            )
        polarity = group["required_polarity"]
        if polarity not in {"affirmative", "negated"}:
            raise InputContractError(
                f"{group_where}.required_polarity is outside the closed enum"
            )
        signature = (normalized_alternatives, str(polarity))
        if signature in signatures:
            raise InputContractError(f"{where} contains duplicate semantic anchors")
        signatures.add(signature)
        result.append(group)
    if not _contract_semantic_anchor_groups_match(result, phrases, assets):
        raise InputContractError(
            f"{where} must authenticate every group inside this record's request phrases"
        )
    return result


def _quantity_profile_matches_phrase(profile: Mapping[str, Any], phrase: str) -> bool:
    return any(
        _literal_catalog_alias_match(str(alias), phrase)
        for record in profile["literal_aliases"]
        for alias in record["values"]
    )


def _validate_literal_quantities(
    contract: Mapping[str, Any],
    concept: str,
    assets: UniversalSceneAssets,
) -> None:
    """Bind reviewed person-cardinality literals to entity quantities."""

    profiles = assets.semantic_bindings["literal_quantity_bindings"]
    bound_phrases: list[str] = []
    entities = contract["identity_core"]["entities"]
    for entity_index, entity in enumerate(entities):
        entity_matches: list[Mapping[str, Any]] = []
        for fact in entity["feature_facts"]:
            for phrase in fact["request_phrases"]:
                bound_phrases.append(str(phrase))
                matches = [
                    profile
                    for profile in profiles
                    if _quantity_profile_matches_phrase(profile, str(phrase))
                ]
                if len(matches) > 1:
                    raise InputContractError(
                        f"identity_core.entities[{entity_index}] has an ambiguous reviewed quantity phrase"
                    )
                entity_matches.extend(matches)
        if entity_matches and int(entity["quantity"]) != max(
            int(profile["quantity"]) for profile in entity_matches
        ):
            raise InputContractError(
                f"identity_core.entities[{entity_index}].quantity contradicts its highest literal-bound total"
            )
    total_quantity = sum(int(entity["quantity"]) for entity in entities)
    for fact in contract["identity_core"]["scene_facts"]:
        for phrase in fact["request_phrases"]:
            bound_phrases.append(str(phrase))
            matches = [
                profile
                for profile in profiles
                if _quantity_profile_matches_phrase(profile, str(phrase))
            ]
            if len(matches) > 1:
                raise InputContractError("identity_core.scene_facts has an ambiguous reviewed quantity phrase")
            if matches and total_quantity != int(matches[0]["quantity"]):
                raise InputContractError(
                    "identity entity quantities contradict the literal-bound total subject quantity"
                )
    raw_matches = [
        profile
        for profile in profiles
        if _quantity_profile_matches_phrase(profile, concept)
    ]
    for profile in raw_matches:
        if not any(_quantity_profile_matches_phrase(profile, phrase) for phrase in bound_phrases):
            raise InputContractError(
                "a reviewed explicit subject quantity in the request is not represented by an identity fact"
            )


def validate_scene_contract(
    concept: str,
    scene_contract: Mapping[str, Any],
    *,
    assets: UniversalSceneAssets | None = None,
) -> ValidatedSceneContract:
    """Validate hash, exact shape, literal claims, capabilities, and closure.

    The returned value is a canonical deep copy.  Callers cannot mutate their
    original mapping after validation and affect a subsequent selection.
    """

    if not isinstance(concept, str) or not concept.strip():
        raise InputContractError("concept must be a non-empty string")
    if assets is None:
        raise InputContractError(
            "validated universal semantic-binding assets are required for a scene contract"
        )
    contract_in = _require_mapping(scene_contract, "scene_contract", InputContractError)
    contract = _deep_canonical_copy(contract_in)
    _require_exact_keys(
        contract,
        {
            "schema",
            "request_text_sha256",
            "identity_core",
            "participant_bindings",
            "slot_states",
            "event_roles",
            "context_profile",
        },
        "scene_contract",
        InputContractError,
    )
    if contract["schema"] != SCENE_CONTRACT_SCHEMA:
        raise InputContractError(f"scene_contract.schema must be {SCENE_CONTRACT_SCHEMA}")
    request_hash = hashlib.sha256(concept.encode("utf-8")).hexdigest()
    if contract["request_text_sha256"] != request_hash:
        raise InputContractError("scene_contract.request_text_sha256 does not match concept bytes")
    concept_normalized = _normalize_text(concept)

    identity = _require_mapping(contract["identity_core"], "identity_core", InputContractError)
    _require_exact_keys(
        identity,
        {"entities", "scene_facts", "forbidden_facts"},
        "identity_core",
        InputContractError,
    )
    entities = _require_list(identity["entities"], "identity_core.entities", InputContractError)
    if not entities:
        raise InputContractError("identity_core.entities must contain at least one entity")
    entity_by_id: dict[str, Mapping[str, Any]] = {}
    capability_capacities: list[Mapping[str, Any]] = []
    fact_ids: set[str] = set()

    for index, raw_entity in enumerate(entities):
        where = f"identity_core.entities[{index}]"
        entity = _require_mapping(raw_entity, where, InputContractError)
        _require_exact_keys(
            entity,
            {
                "entity_id",
                "quantity",
                "embodiment_profile_id",
                "capability_projection_mode",
                "feature_facts",
                "capabilities",
            },
            where,
            InputContractError,
        )
        entity_id = _require_nonempty_string(entity["entity_id"], f"{where}.entity_id", InputContractError)
        if entity_id in entity_by_id:
            raise InputContractError(f"duplicate entity_id: {entity_id}")
        _require_int_range(entity["quantity"], 1, 64, f"{where}.quantity", InputContractError)
        profile_id = _require_nonempty_string(
            entity["embodiment_profile_id"],
            f"{where}.embodiment_profile_id",
            InputContractError,
        )
        if not profile_id.startswith("custom_") and profile_id not in assets.embodiment_by_id:
            raise InputContractError(f"unknown embodiment profile: {profile_id}")
        projection_mode = entity["capability_projection_mode"]
        if projection_mode not in {"declared_subset", "catalog_exact"}:
            raise InputContractError(
                f"{where}.capability_projection_mode is outside the closed enum"
            )
        if profile_id.startswith("custom_") and projection_mode != "declared_subset":
            raise InputContractError(
                f"{where} custom embodiment profiles must use declared_subset"
            )
        features = _require_list(entity["feature_facts"], f"{where}.feature_facts", InputContractError)
        local_feature_ids: set[str] = set()
        local_features_by_id: dict[str, Mapping[str, Any]] = {}
        for fact_index, raw_fact in enumerate(features):
            fact = _validate_fact(raw_fact, concept_normalized, f"{where}.feature_facts[{fact_index}]")
            fact_id = str(fact["id"])
            if fact_id in fact_ids:
                raise InputContractError(f"duplicate identity fact id: {fact_id}")
            fact_ids.add(fact_id)
            local_feature_ids.add(fact_id)
            local_features_by_id[fact_id] = fact

        capabilities = _require_list(entity["capabilities"], f"{where}.capabilities", InputContractError)
        local_capability_ids: set[str] = set()
        for capability_index, raw_capability in enumerate(capabilities):
            cap_where = f"{where}.capabilities[{capability_index}]"
            capability = _require_mapping(raw_capability, cap_where, InputContractError)
            _require_exact_keys(
                capability,
                {"id", "capacity", "state", "source", "source_fact_id"},
                cap_where,
                InputContractError,
            )
            capability_id = _require_nonempty_string(
                capability["id"], f"{cap_where}.id", InputContractError
            )
            if capability_id in local_capability_ids:
                raise InputContractError(f"duplicate capability for {entity_id}: {capability_id}")
            local_capability_ids.add(capability_id)
            capacity = _require_int_range(
                capability["capacity"], 0, 64, f"{cap_where}.capacity", InputContractError
            )
            state = capability["state"]
            if state not in {"available", "unavailable"}:
                raise InputContractError(f"{cap_where}.state must be available|unavailable")
            if (state == "unavailable") != (capacity == 0):
                raise InputContractError(
                    f"{cap_where} unavailable must have capacity 0 and available must be positive"
                )
            source = capability["source"]
            if source not in {"explicit", "embodiment_profile"}:
                raise InputContractError(f"{cap_where}.source must be explicit|embodiment_profile")
            source_fact_id = _require_nonempty_string(
                capability["source_fact_id"], f"{cap_where}.source_fact_id", InputContractError
            )
            if source == "explicit" and source_fact_id not in local_feature_ids:
                raise InputContractError(
                    f"{cap_where}.source_fact_id must reference this entity's literal feature fact"
                )
            profiles_for_capability = assets.capability_assertions_by_id.get(
                capability_id,
                (),
            )
            unavailable_profiles = [
                profile
                for profile in profiles_for_capability
                if profile["assertion"] == "unavailable"
            ]
            available_profiles = [
                profile
                for profile in profiles_for_capability
                if profile["assertion"] == "available"
            ]
            every_feature_phrase = [
                str(phrase)
                for feature in local_features_by_id.values()
                for phrase in feature["request_phrases"]
            ]
            contradictory_absence = any(
                _capability_profile_literal_matches(profile, every_feature_phrase, assets)
                for profile in unavailable_profiles
            )
            contradictory_presence = any(
                _capability_profile_literal_matches(profile, every_feature_phrase, assets)
                for profile in available_profiles
            )
            if state == "available" and contradictory_absence:
                raise InputContractError(
                    f"{cap_where} positive capacity contradicts a reviewed literal absence assertion"
                )
            if state == "unavailable" and contradictory_presence:
                raise InputContractError(
                    f"{cap_where} unavailable capacity contradicts a reviewed literal positive assertion"
                )
            if source == "explicit":
                if state == "available":
                    source_phrases = [
                        str(phrase)
                        for phrase in local_features_by_id[source_fact_id]["request_phrases"]
                    ]
                    matched_profiles = [
                        profile
                        for profile in available_profiles
                        if int(profile["minimum_capacity"]) <= capacity <= int(profile["maximum_capacity"])
                        and _capability_profile_literal_matches(profile, source_phrases, assets)
                    ]
                    if not matched_profiles:
                        raise InputContractError(
                            f"{cap_where} positive explicit capability lacks a reviewed literal-bound assertion profile"
                        )
                # An explicit unavailable/0 assertion is a conservative denial
                # and may remain opaque.  It never authorizes a positive resource.
            if source == "embodiment_profile":
                if source_fact_id != profile_id:
                    raise InputContractError(
                        f"{cap_where}.source_fact_id must equal embodiment_profile_id"
                    )
                if assets is None:
                    raise InputContractError(
                        "assets are required to validate embodiment-profile-derived capabilities"
                    )
                profile = assets.embodiment_by_id.get(profile_id)
                if profile is None:
                    raise InputContractError(f"unknown embodiment profile: {profile_id}")
                profile_capacities = _profile_capacities(profile)
                declared = profile_capacities.get(capability_id)
                if declared is None:
                    raise InputContractError(
                        f"profile {profile_id} does not declare capability {capability_id}"
                    )
                if declared != capacity:
                    raise InputContractError(
                        f"profile capability mismatch for {profile_id}:{capability_id}"
                    )
            capability_capacities.append(
                {
                    "entity_id": entity_id,
                    "resource_kind": capability_id,
                    "capacity": capacity,
                    "state": state,
                    "source": source,
                    "source_fact_id": source_fact_id,
                }
            )
        embodiment_profile = assets.embodiment_by_id.get(profile_id)
        if projection_mode == "catalog_exact":
            if embodiment_profile is None:
                raise InputContractError(
                    f"{where} catalog_exact requires a known embodiment profile"
                )
            expected_capabilities = [
                {
                    "id": str(item["id"]),
                    "capacity": int(item["capacity"]),
                    "state": (
                        "unavailable" if int(item["capacity"]) == 0 else "available"
                    ),
                    "source": "embodiment_profile",
                    "source_fact_id": profile_id,
                }
                for item in embodiment_profile["capability_capacities"]
            ]
            if capabilities != expected_capabilities:
                raise InputContractError(
                    f"{where}.capabilities must exactly project catalog_exact profile {profile_id}"
                )
        entity_by_id[entity_id] = entity

    participant_bindings = _require_list(
        contract["participant_bindings"],
        "participant_bindings",
        InputContractError,
    )
    if len(participant_bindings) != len(EVENT_ROLE_IDS):
        raise InputContractError(
            "participant_bindings must contain exactly one ordered record per event role"
        )
    participant_by_role: dict[str, Mapping[str, Any]] = {}
    for index, (expected_role_id, raw_binding) in enumerate(
        zip(EVENT_ROLE_IDS, participant_bindings)
    ):
        where = f"participant_bindings[{index}]"
        binding = _require_mapping(raw_binding, where, InputContractError)
        _require_exact_keys(
            binding,
            {"role_id", "entity_ids", "primary_entity_id"},
            where,
            InputContractError,
        )
        if binding["role_id"] != expected_role_id:
            raise InputContractError(
                "participant_bindings must follow the closed EVENT_ROLE_IDS order"
            )
        entity_ids = _require_string_list(
            binding["entity_ids"],
            f"{where}.entity_ids",
            InputContractError,
        )
        if entity_ids != sorted(set(entity_ids)):
            raise InputContractError(f"{where}.entity_ids must be sorted and unique")
        if set(entity_ids) - set(entity_by_id):
            raise InputContractError(f"{where}.entity_ids contains an unknown identity entity")
        primary = binding["primary_entity_id"]
        if not entity_ids:
            if primary is not None:
                raise InputContractError(f"{where}.primary_entity_id must be null for an empty binding")
        elif primary not in entity_ids:
            raise InputContractError(f"{where}.primary_entity_id must be a bound entity")
        if expected_role_id == "actor" and not entity_ids:
            raise InputContractError("participant_bindings.actor must bind at least one identity entity")
        participant_by_role[expected_role_id] = binding

    for list_name in ("scene_facts", "forbidden_facts"):
        facts = _require_list(identity[list_name], f"identity_core.{list_name}", InputContractError)
        for index, raw_fact in enumerate(facts):
            fact = _validate_fact(raw_fact, concept_normalized, f"identity_core.{list_name}[{index}]")
            fact_id = str(fact["id"])
            if fact_id in fact_ids:
                raise InputContractError(f"duplicate identity fact id: {fact_id}")
            fact_ids.add(fact_id)

    asserted_identity_facts = [
        fact
        for entity in contract["identity_core"]["entities"]
        for fact in entity["feature_facts"]
    ] + list(contract["identity_core"]["scene_facts"])
    for fact in asserted_identity_facts:
        for phrase in fact["request_phrases"]:
            for profile in assets.semantic_bindings["identity_literal_profiles"]:
                aliases = [
                    str(alias)
                    for record in profile["literal_aliases"]
                    for alias in record["values"]
                ]
                if "negated" in _literal_alias_occurrence_polarities(
                    str(phrase), aliases, assets
                ):
                    raise InputContractError(
                        "asserted identity facts may not contain a negated reviewed identity occurrence"
                    )

    _validate_literal_quantities(contract, concept, assets)

    slot_states = _require_list(contract["slot_states"], "slot_states", InputContractError)
    if [item.get("slot_id") if isinstance(item, Mapping) else None for item in slot_states] != list(SCENE_SLOT_IDS):
        raise InputContractError(f"slot_states must contain the closed order {list(SCENE_SLOT_IDS)}")
    slot_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_slot in enumerate(slot_states):
        where = f"slot_states[{index}]"
        slot = _require_mapping(raw_slot, where, InputContractError)
        _require_exact_keys(
            slot,
            {
                "slot_id",
                "state",
                "value_ids",
                "request_phrases",
                "value_phrase_bindings",
            },
            where,
            InputContractError,
        )
        state = slot["state"]
        if state not in {"fixed", "closed", "open"}:
            raise InputContractError(f"{where}.state must be fixed|closed|open")
        values = _require_string_list(slot["value_ids"], f"{where}.value_ids", InputContractError)
        phrases = _validate_literal_phrases(
            slot["request_phrases"],
            concept_normalized,
            f"{where}.request_phrases",
            allow_empty=state == "open",
        )
        if state == "fixed" and (not values or not phrases):
            raise InputContractError(f"{where} fixed state requires literal-bound values")
        if state == "closed" and (values or not phrases):
            raise InputContractError(f"{where} closed state requires a negative literal and no values")
        if state == "open" and (values or phrases):
            raise InputContractError(f"{where} open state must not contain inferred values or phrases")
        raw_value_bindings = _require_list(
            slot["value_phrase_bindings"],
            f"{where}.value_phrase_bindings",
            InputContractError,
        )
        value_bindings: list[Mapping[str, Any]] = []
        for binding_index, raw_binding in enumerate(raw_value_bindings):
            binding_where = f"{where}.value_phrase_bindings[{binding_index}]"
            binding = _require_mapping(raw_binding, binding_where, InputContractError)
            _require_exact_keys(
                binding,
                {"value_id", "request_phrases", "semantic_anchor_groups"},
                binding_where,
                InputContractError,
            )
            _require_nonempty_string(
                binding["value_id"],
                f"{binding_where}.value_id",
                InputContractError,
            )
            binding_phrases = _validate_literal_phrases(
                binding["request_phrases"],
                concept_normalized,
                f"{binding_where}.request_phrases",
                allow_empty=False,
            )
            semantic_anchor_groups = _validate_contract_semantic_anchor_groups(
                binding["semantic_anchor_groups"],
                binding_phrases,
                fixed=state == "fixed",
                where=f"{binding_where}.semantic_anchor_groups",
                assets=assets,
            )
            value_bindings.append(
                {
                    "value_id": str(binding["value_id"]),
                    "request_phrases": binding_phrases,
                    "semantic_anchor_groups": semantic_anchor_groups,
                }
            )
        if state == "fixed":
            if [item["value_id"] for item in value_bindings] != values:
                raise InputContractError(
                    f"{where}.value_phrase_bindings must exactly follow value_ids order"
                )
            flattened_binding_phrases = [
                phrase
                for item in value_bindings
                for phrase in item["request_phrases"]
            ]
            if flattened_binding_phrases != phrases:
                raise InputContractError(
                    f"{where}.value_phrase_bindings must partition request_phrases in exact order"
                )
            if len(flattened_binding_phrases) != len(
                {_normalize_text(phrase) for phrase in flattened_binding_phrases}
            ):
                raise InputContractError(
                    f"{where}.value_phrase_bindings may not reuse a literal phrase across values"
                )
            anchor_owner_by_text: dict[str, str] = {}
            for item in value_bindings:
                for group in item["semantic_anchor_groups"]:
                    for alternative in group["alternatives"]:
                        normalized_anchor = _normalize_text(str(alternative))
                        prior_owner = anchor_owner_by_text.get(normalized_anchor)
                        if prior_owner is not None and prior_owner != item["value_id"]:
                            raise InputContractError(
                                f"{where}.value_phrase_bindings may not reuse a semantic anchor across values"
                            )
                        anchor_owner_by_text[normalized_anchor] = str(item["value_id"])
        elif value_bindings:
            raise InputContractError(
                f"{where}.value_phrase_bindings must be empty for {state} state"
            )
        if state == "closed" and any(
            not _phrase_has_closed_polarity(
                phrase,
                target_kind="slot",
                target_id=str(slot["slot_id"]),
                assets=assets,
            )
            for phrase in phrases
        ):
            raise InputContractError(f"{where} closed state lacks a scoped reviewed negative literal")
        slot_by_id[str(slot["slot_id"])] = slot

    event_roles = _require_list(contract["event_roles"], "event_roles", InputContractError)
    if [item.get("role_id") if isinstance(item, Mapping) else None for item in event_roles] != list(EVENT_ROLE_IDS):
        raise InputContractError(f"event_roles must contain the closed order {list(EVENT_ROLE_IDS)}")
    role_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_role in enumerate(event_roles):
        where = f"event_roles[{index}]"
        role = _require_mapping(raw_role, where, InputContractError)
        _require_exact_keys(
            role,
            {"role_id", "state", "value_id", "request_phrases", "semantic_anchor_groups"},
            where,
            InputContractError,
        )
        state = role["state"]
        if state not in {"fixed", "closed", "open"}:
            raise InputContractError(f"{where}.state must be fixed|closed|open")
        value_id = role["value_id"]
        phrases = _validate_literal_phrases(
            role["request_phrases"],
            concept_normalized,
            f"{where}.request_phrases",
            allow_empty=state == "open",
        )
        if state == "fixed":
            _require_nonempty_string(value_id, f"{where}.value_id", InputContractError)
            if not phrases:
                raise InputContractError(f"{where} fixed role requires literal evidence")
        elif state == "closed":
            if value_id is not None or not phrases:
                raise InputContractError(f"{where} closed role requires negative literal and null value")
        elif value_id is not None or phrases:
            raise InputContractError(f"{where} open role must remain null and unbound")
        _validate_contract_semantic_anchor_groups(
            role["semantic_anchor_groups"],
            phrases,
            fixed=state == "fixed",
            where=f"{where}.semantic_anchor_groups",
            assets=assets,
        )
        if state == "closed" and any(
            not _phrase_has_closed_polarity(
                phrase,
                target_kind="event_role",
                target_id=str(role["role_id"]),
                assets=assets,
            )
            for phrase in phrases
        ):
            raise InputContractError(f"{where} closed role lacks a scoped reviewed negative literal")
        role_by_id[str(role["role_id"])] = role

    for role_id in EVENT_ROLE_IDS:
        role = role_by_id[role_id]
        participant = participant_by_role[role_id]
        if role["state"] == "closed" and participant["entity_ids"]:
            raise InputContractError(
                f"participant_bindings.{role_id} cannot enter a closed event role"
            )
        if participant["entity_ids"] and role["state"] != "fixed":
            raise InputContractError(
                f"participant_bindings.{role_id} requires a fixed event role"
            )

    semantic_values = (
        list(slot_by_id["prop"]["value_ids"])
        if slot_by_id["prop"]["state"] == "fixed"
        else []
    )
    fixed_prop_phrases = (
        list(slot_by_id["prop"]["request_phrases"])
        if slot_by_id["prop"]["state"] == "fixed"
        else []
    )
    for role_id in ("target", "instrument"):
        role = role_by_id[role_id]
        role_value = role["value_id"]
        if role["state"] == "fixed" and isinstance(role_value, str):
            semantic_values.append(role_value)
            fixed_prop_phrases.extend(role["request_phrases"])

    positive_identity_phrases = [
        str(phrase)
        for entity in contract["identity_core"]["entities"]
        for fact in entity["feature_facts"]
        for phrase in fact["request_phrases"]
    ] + [
        str(phrase)
        for fact in contract["identity_core"]["scene_facts"]
        for phrase in fact["request_phrases"]
    ]
    forbidden_identity_phrases = [
        str(phrase)
        for fact in contract["identity_core"]["forbidden_facts"]
        for phrase in fact["request_phrases"]
    ]
    closed_binding_phrases = [
        str(phrase)
        for slot in contract["slot_states"]
        if slot["state"] == "closed"
        for phrase in slot["request_phrases"]
    ] + [
        str(phrase)
        for role in contract["event_roles"]
        if role["state"] == "closed"
        for phrase in role["request_phrases"]
    ]
    positive_prop_phrases = positive_identity_phrases + list(fixed_prop_phrases)
    all_bound_phrases = [
        *positive_identity_phrases,
        *forbidden_identity_phrases,
        *(
            str(phrase)
            for slot in contract["slot_states"]
            for phrase in slot["request_phrases"]
        ),
        *(
            str(phrase)
            for role in contract["event_roles"]
            for phrase in role["request_phrases"]
        ),
    ]

    def literal_prop_polarities(
        phrases: Sequence[str],
        *,
        allow_postposed_logical: bool,
    ) -> dict[str, set[str]]:
        result: dict[str, set[str]] = {}
        for prop_id, prop in assets.prop_by_id.items():
            aliases = [
                str(alias)
                for record in prop["aliases"]
                for alias in record["values"]
            ]
            for phrase in phrases:
                polarities = _literal_alias_occurrence_polarities(
                    str(phrase),
                    aliases,
                    assets,
                    allow_postposed_logical=allow_postposed_logical,
                )
                if polarities:
                    result.setdefault(str(prop_id), set()).update(polarities)
        return result

    # The raw request can place a negated action immediately after a positive
    # prop noun ("machine gun, without firing it").  Raw coverage therefore
    # uses only preceding logical scope; the literal-bound slot/role spans are
    # narrower and may safely authenticate postposed noun absence such as
    # "no apple is present".
    raw_prop_polarities = literal_prop_polarities(
        [concept], allow_postposed_logical=False
    )
    bound_prop_polarities = literal_prop_polarities(
        all_bound_phrases, allow_postposed_logical=True
    )
    fixed_prop_polarities = literal_prop_polarities(
        fixed_prop_phrases, allow_postposed_logical=True
    )
    raw_literal_props = set(raw_prop_polarities)
    positive_literal_props = {
        prop_id
        for prop_id, polarities in bound_prop_polarities.items()
        if "affirmative" in polarities
    }
    negative_literal_props = {
        prop_id
        for prop_id, polarities in bound_prop_polarities.items()
        if polarities == {"negated"}
    }
    unclassified_literal_props = raw_literal_props - set(bound_prop_polarities)
    if unclassified_literal_props:
        raise InputContractError(
            "known catalog prop mentions must be classified by a positive fixed binding or an explicit negative binding: "
            f"unclassified={sorted(unclassified_literal_props)}"
        )
    raw_affirmative_props = {
        prop_id
        for prop_id, polarities in raw_prop_polarities.items()
        if "affirmative" in polarities
    }
    missing_affirmative_projection = raw_affirmative_props - positive_literal_props
    if missing_affirmative_projection:
        raise InputContractError(
            "affirmative catalog prop occurrences must remain affirmative in a literal-bound fact/slot/role: "
            f"missing={sorted(missing_affirmative_projection)}"
        )
    raw_negative_only_props = {
        prop_id
        for prop_id, polarities in raw_prop_polarities.items()
        if polarities == {"negated"}
    }
    missing_negative_projection = raw_negative_only_props - negative_literal_props
    if missing_negative_projection:
        raise InputContractError(
            "negated-only catalog prop occurrences require an exact negative literal binding: "
            f"missing={sorted(missing_negative_projection)}"
        )

    matched_known_props = _semantic_prop_ids_from_values(semantic_values, assets)
    matched_distinct_senses: set[str] = set()
    for prop_id, profiles_for_prop in assets.prop_sense_by_catalog_id.items():
        for profile in profiles_for_prop:
            if not _distinct_prop_sense_matches(
                profile,
                positive_prop_phrases,
                semantic_values,
            ):
                continue
            matched_distinct_senses.add(str(prop_id))
            if profile["activation_target"] is not None:
                matched_known_props.add(str(profile["activation_target"]))

    for prop_id in sorted(matched_known_props):
        aliases = [
            str(alias)
            for record in assets.prop_by_id[prop_id]["aliases"]
            for alias in record["values"]
        ]
        if fixed_prop_polarities.get(prop_id) != {"affirmative"}:
            raise InputContractError(
                f"fixed semantic prop {prop_id} requires affirmative-only literal catalog occurrences"
            )
    invalid_positive_props = positive_literal_props - matched_known_props - matched_distinct_senses
    if invalid_positive_props:
        raise InputContractError(
            "positive catalog prop literals must project to fixed semantic prop values or a reviewed distinct sense: "
            f"literal={sorted(positive_literal_props)}, semantic={sorted(matched_known_props)}, "
            f"unmatched={sorted(invalid_positive_props)}"
        )

    context = _require_mapping(contract["context_profile"], "context_profile", InputContractError)
    _require_exact_keys(
        context,
        {"theme_tags", "era_technology", "tone", "violence", "social", "scale"},
        "context_profile",
        InputContractError,
    )
    _require_string_list(context["theme_tags"], "context_profile.theme_tags", InputContractError)
    _require_nonempty_string(context["era_technology"], "context_profile.era_technology", InputContractError)
    _require_nonempty_string(context["tone"], "context_profile.tone", InputContractError)
    if context["violence"] not in {"closed", "nonviolent", "contextual", "active", "unknown"}:
        raise InputContractError("context_profile.violence is outside the closed enum")
    if context["social"] not in {"solo", "dyad", "ensemble", "unknown"}:
        raise InputContractError("context_profile.social is outside the closed enum")
    if context["scale"] not in {"intimate", "room", "site", "world", "unknown"}:
        raise InputContractError("context_profile.scale is outside the closed enum")
    entity_quantity = sum(
        int(entity["quantity"])
        for entity in contract["identity_core"]["entities"]
    )
    fixed_recipient = role_by_id["recipient"]["state"] == "fixed"
    social_value = str(context["social"])
    social_is_structurally_bound = (
        social_value == "unknown"
        or (social_value == "solo" and entity_quantity == 1 and not fixed_recipient)
        or (
            social_value == "dyad"
            and (entity_quantity == 2 or (entity_quantity == 1 and fixed_recipient))
        )
        or (social_value == "ensemble" and entity_quantity >= 3)
    )
    if not social_is_structurally_bound:
        raise InputContractError(
            "context_profile.social contradicts typed entity cardinality/recipient structure"
        )
    for profile in assets.semantic_bindings["context_literal_profiles"]:
        field = str(profile["field"])
        if str(context[field]) != str(profile["value"]):
            continue
        if not _context_literal_profile_matches(profile, concept, assets):
            raise InputContractError(
                f"context_profile.{field}={profile['value']} lacks reviewed literal evidence"
            )
    if "prop_decommissioned_machine_gun" in matched_known_props:
        if context["era_technology"] != "decommissioned_firearm":
            raise InputContractError(
                "decommissioned machine-gun prop requires decommissioned_firearm context"
            )
        if context["violence"] not in {"closed", "nonviolent"}:
            raise InputContractError(
                "decommissioned machine-gun prop requires a closed/nonviolent context"
            )
        target_role = role_by_id["target"]
        if target_role["state"] == "open":
            raise InputContractError(
                "decommissioned machine-gun prop requires a fixed weapon-state target or explicit-none target"
            )
        if target_role["state"] == "fixed" and assets is not None:
            target_props = _semantic_prop_ids_from_values(
                [str(target_role["value_id"])],
                assets,
            )
            if "prop_decommissioned_machine_gun" not in target_props:
                raise InputContractError(
                    "decommissioned machine-gun target must bind the weapon itself"
                )

    contract_hash = canonical_sha256(contract)
    return ValidatedSceneContract(
        contract=MappingProxyType(contract),
        request_text=concept,
        sha256=contract_hash,
        request_sha256=request_hash,
        slot_by_id=MappingProxyType(slot_by_id),
        role_by_id=MappingProxyType(role_by_id),
        participant_by_role=MappingProxyType(participant_by_role),
        entity_by_id=MappingProxyType(entity_by_id),
        capability_capacities=tuple(MappingProxyType(dict(item)) for item in capability_capacities),
    )


def _profile_capacities(profile: Mapping[str, Any]) -> dict[str, int]:
    raw = profile.get("capability_capacities", {})
    if isinstance(raw, Mapping):
        return {str(key): int(value) for key, value in raw.items()}
    result: dict[str, int] = {}
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, Mapping) and isinstance(item.get("id"), str):
                result[item["id"]] = int(item.get("capacity", 0))
    return result


def _validate_vector(
    value: Any,
    axes: Sequence[str],
    where: str,
    error_type: type[Exception] = AssetValidationError,
) -> dict[str, int]:
    vector = _require_mapping(value, where, error_type)
    _require_exact_keys(vector, axes, where, error_type)
    return {
        axis: _require_int_range(vector[axis], 0, 3, f"{where}.{axis}", error_type)
        for axis in axes
    }


def _distance_band(vector: Mapping[str, int]) -> str:
    values = [int(vector[axis]) for axis in DISTANCE_AXIS_IDS]
    if max(values) == 3 or sum(values) >= 10:
        return "far"
    if max(values) == 2 or sum(values) >= 4:
        return "middle"
    return "near"


def _creativity_target(creativity: float) -> str:
    if creativity < 0.25:
        return "near"
    if creativity < 0.75:
        return "middle"
    return "far"


def _theme_displacement_band(value: int) -> str:
    if value == 3:
        return "far"
    if value == 2:
        return "middle"
    return "near"


def _max_vector(vectors: Iterable[Mapping[str, int]], axes: Sequence[str]) -> dict[str, int]:
    result = {axis: 0 for axis in axes}
    for vector in vectors:
        for axis in axes:
            result[axis] = max(result[axis], int(vector[axis]))
    return result


def _validate_predicate(value: Any, where: str) -> tuple[str, str, str]:
    item = _require_list(value, where, AssetValidationError)
    if len(item) != 3 or any(not isinstance(part, str) or not part for part in item):
        raise AssetValidationError(f"{where} must be a three-string predicate")
    if item[0] not in SUPPORTED_PREDICATE_KINDS:
        raise AssetValidationError(f"{where} has unsupported predicate kind {item[0]!r}")
    return item[0], item[1], item[2]


def _validate_predicate_list(value: Any, where: str) -> list[tuple[str, str, str]]:
    items = _require_list(value, where, AssetValidationError)
    return [_validate_predicate(item, f"{where}[{index}]") for index, item in enumerate(items)]


def _validate_predicate_groups(value: Any, where: str) -> list[list[tuple[str, str, str]]]:
    groups = _require_list(value, where, AssetValidationError)
    result: list[list[tuple[str, str, str]]] = []
    for index, raw_group in enumerate(groups):
        group = _validate_predicate_list(raw_group, f"{where}[{index}]")
        if not group:
            raise AssetValidationError(f"{where}[{index}] must not be empty")
        result.append(group)
    return result


def _validate_parameters(value: Any, where: str) -> None:
    parameters = _require_mapping(value, where, AssetValidationError)
    for parameter_id, raw_values in parameters.items():
        _require_nonempty_string(parameter_id, f"{where} key", AssetValidationError)
        _require_string_list(
            raw_values,
            f"{where}.{parameter_id}",
            AssetValidationError,
            allow_empty=False,
        )


def _validate_visual_contract(
    value: Any,
    where: str,
    *,
    predicate_kind_ids: set[str],
    resource_kind_ids: set[str],
) -> None:
    contract = _require_mapping(value, where, AssetValidationError)
    _require_exact_keys(
        contract,
        {
            "bindings",
            "requires_all",
            "requires_any",
            "forbids_any",
            "provides",
            "resource_claims",
            "distance_profile",
            "load_profile",
            "bridge_types",
            "salience",
            "render_risk",
            "pixel_evidence",
        },
        where,
        AssetValidationError,
    )
    bindings = _require_list(contract["bindings"], f"{where}.bindings", AssetValidationError)
    seen_bindings: set[str] = set()
    for index, raw_binding in enumerate(bindings):
        binding = _require_list(raw_binding, f"{where}.bindings[{index}]", AssetValidationError)
        if (
            len(binding) != 2
            or binding[0] not in EVENT_ROLE_IDS
            or binding[1] not in {"required", "optional", "event_spine"}
        ):
            raise AssetValidationError(
                f"{where}.bindings[{index}] must be [event_role, required|optional|event_spine]"
            )
        if binding[0] in seen_bindings:
            raise AssetValidationError(f"{where}.bindings repeats role {binding[0]}")
        seen_bindings.add(binding[0])

    predicates = _validate_predicate_list(contract["requires_all"], f"{where}.requires_all")
    predicates += _validate_predicate_list(contract["forbids_any"], f"{where}.forbids_any")
    predicates += _validate_predicate_list(contract["provides"], f"{where}.provides")
    for group in _validate_predicate_groups(contract["requires_any"], f"{where}.requires_any"):
        predicates += group
    undeclared = {item[0] for item in predicates} - predicate_kind_ids
    if undeclared:
        raise AssetValidationError(f"{where} uses undeclared predicate kinds: {sorted(undeclared)}")

    claims = _require_list(contract["resource_claims"], f"{where}.resource_claims", AssetValidationError)
    for index, raw_claim in enumerate(claims):
        claim = _require_list(raw_claim, f"{where}.resource_claims[{index}]", AssetValidationError)
        if (
            len(claim) != 4
            or claim[0] not in resource_kind_ids
            or claim[1] not in {*EVENT_ROLE_IDS, "scene"}
            or isinstance(claim[2], bool)
            or not isinstance(claim[2], int)
            or claim[2] <= 0
            or claim[3] not in {"exclusive", "shared"}
        ):
            raise AssetValidationError(
                f"{where}.resource_claims[{index}] has an invalid typed claim"
            )

    distance = _require_mapping(contract["distance_profile"], f"{where}.distance_profile", AssetValidationError)
    _require_exact_keys(distance, {"base", "adjustments"}, f"{where}.distance_profile", AssetValidationError)
    _validate_vector(distance["base"], DISTANCE_AXIS_IDS, f"{where}.distance_profile.base")
    adjustments = _require_list(distance["adjustments"], f"{where}.distance_profile.adjustments", AssetValidationError)
    for index, adjustment in enumerate(adjustments):
        item = _require_mapping(adjustment, f"{where}.distance_profile.adjustments[{index}]", AssetValidationError)
        _require_exact_keys(item, {"when_all", "operation"}, f"{where}.distance_profile.adjustments[{index}]", AssetValidationError)
        _validate_predicate_list(item["when_all"], f"{where}.distance_profile.adjustments[{index}].when_all")
        if item["operation"] != "compare_each_axis_ordinal_0_3":
            raise AssetValidationError(f"{where} adjustment operation is not closed")

    _validate_vector(contract["load_profile"], LOAD_AXIS_IDS, f"{where}.load_profile")
    bridge_types = _require_string_list(contract["bridge_types"], f"{where}.bridge_types", AssetValidationError)
    if set(bridge_types) - KNOWN_BRIDGE_TYPES:
        raise AssetValidationError(f"{where}.bridge_types contains an unknown type")

    salience = _require_mapping(contract["salience"], f"{where}.salience", AssetValidationError)
    _require_exact_keys(salience, {"role", "displacement_cap"}, f"{where}.salience", AssetValidationError)
    if salience["role"] not in {"support", "primary", "secondary"}:
        raise AssetValidationError(f"{where}.salience.role is outside the closed enum")
    _require_int_range(salience["displacement_cap"], 0, 3, f"{where}.salience.displacement_cap", AssetValidationError)

    render_risk = _require_mapping(contract["render_risk"], f"{where}.render_risk", AssetValidationError)
    _require_exact_keys(render_risk, {"band", "tags"}, f"{where}.render_risk", AssetValidationError)
    if render_risk["band"] not in {"low", "medium", "high"}:
        raise AssetValidationError(f"{where}.render_risk.band is outside the closed enum")
    _require_string_list(render_risk["tags"], f"{where}.render_risk.tags", AssetValidationError)

    evidence = _require_list(contract["pixel_evidence"], f"{where}.pixel_evidence", AssetValidationError)
    if not evidence:
        raise AssetValidationError(f"{where}.pixel_evidence must not be empty for a visual atom")
    evidence_ids: set[str] = set()
    for index, raw_evidence in enumerate(evidence):
        item_where = f"{where}.pixel_evidence[{index}]"
        item = _require_mapping(raw_evidence, item_where, AssetValidationError)
        _require_exact_keys(item, {"id", "kind", "definition", "minimum_scale_ids"}, item_where, AssetValidationError)
        evidence_id = _require_nonempty_string(item["id"], f"{item_where}.id", AssetValidationError)
        if evidence_id in evidence_ids:
            raise AssetValidationError(f"duplicate pixel evidence id in {where}: {evidence_id}")
        evidence_ids.add(evidence_id)
        if item["kind"] not in {"contact", "orientation", "state_boundary", "support", "path", "residue", "display"}:
            raise AssetValidationError(f"{item_where}.kind is outside the closed enum")
        _require_nonempty_string(item["definition"], f"{item_where}.definition", AssetValidationError)
        scales = _require_string_list(
            item["minimum_scale_ids"],
            f"{item_where}.minimum_scale_ids",
            AssetValidationError,
            allow_empty=False,
        )
        if set(scales) - {"native", "thumbnail_320px", "thumbnail_640px"}:
            raise AssetValidationError(f"{item_where} has an unknown review scale")


def _validate_nonvisual_contract(value: Any, role: str, where: str) -> None:
    contract = _require_mapping(value, where, AssetValidationError)
    if role == "router":
        _require_exact_keys(
            contract,
            {"stage", "opens_facets", "requires_all", "forbids_any", "deterministic_order"},
            where,
            AssetValidationError,
        )
        _require_nonempty_string(contract["stage"], f"{where}.stage", AssetValidationError)
        facets = _require_string_list(contract["opens_facets"], f"{where}.opens_facets", AssetValidationError)
        if set(facets) - set(FACET_IDS):
            raise AssetValidationError(f"{where}.opens_facets contains an unknown facet")
        _validate_predicate_list(contract["requires_all"], f"{where}.requires_all")
        _validate_predicate_list(contract["forbids_any"], f"{where}.forbids_any")
        if contract["deterministic_order"] != "candidate_id_ascending":
            raise AssetValidationError(f"{where}.deterministic_order has drifted")
    elif role == "guard":
        _require_exact_keys(
            contract,
            {"stage", "violation_code", "when_all", "require_all", "outcome"},
            where,
            AssetValidationError,
        )
        _require_nonempty_string(contract["stage"], f"{where}.stage", AssetValidationError)
        _require_nonempty_string(contract["violation_code"], f"{where}.violation_code", AssetValidationError)
        _validate_predicate_list(contract["when_all"], f"{where}.when_all")
        _validate_predicate_list(contract["require_all"], f"{where}.require_all")
        if contract["outcome"] not in {"block", "repair", "requires_bridge"}:
            raise AssetValidationError(f"{where}.outcome is outside the closed enum")
    elif role == "metric":
        _require_exact_keys(
            contract,
            {"stage", "value_type", "input_ids", "output_axis"},
            where,
            AssetValidationError,
        )
        _require_nonempty_string(contract["stage"], f"{where}.stage", AssetValidationError)
        if contract["value_type"] not in {"ordinal_0_3", "count", "boolean", "band"}:
            raise AssetValidationError(f"{where}.value_type is outside the closed enum")
        _require_string_list(contract["input_ids"], f"{where}.input_ids", AssetValidationError)
        _require_nonempty_string(contract["output_axis"], f"{where}.output_axis", AssetValidationError)
    else:
        raise AssetValidationError(f"unsupported nonvisual role: {role}")


def _validate_prop_concept(value: Any, where: str) -> None:
    prop = _require_mapping(value, where, AssetValidationError)
    _require_exact_keys(
        prop,
        {
            "id",
            "aliases",
            "hypernym_ids",
            "part_ids",
            "material_ids",
            "affordance_candidate_ids",
            "state_ids",
            "base_distance_profile",
            "base_load_profile",
            "risk_tags",
            "provenance_record_ids",
        },
        where,
        AssetValidationError,
    )
    _require_nonempty_string(prop["id"], f"{where}.id", AssetValidationError)
    aliases = _require_list(prop["aliases"], f"{where}.aliases", AssetValidationError)
    if not aliases:
        raise AssetValidationError(f"{where}.aliases must not be empty")
    seen_locales: set[str] = set()
    for index, raw_alias in enumerate(aliases):
        alias_where = f"{where}.aliases[{index}]"
        alias = _require_mapping(raw_alias, alias_where, AssetValidationError)
        _require_exact_keys(alias, {"locale", "values"}, alias_where, AssetValidationError)
        if alias["locale"] not in {"ko", "en", "ja", "zh"} or alias["locale"] in seen_locales:
            raise AssetValidationError(f"{alias_where}.locale is unknown or duplicated")
        seen_locales.add(alias["locale"])
        _require_string_list(alias["values"], f"{alias_where}.values", AssetValidationError, allow_empty=False)
    for key in (
        "hypernym_ids",
        "part_ids",
        "material_ids",
        "affordance_candidate_ids",
        "state_ids",
        "risk_tags",
        "provenance_record_ids",
    ):
        _require_string_list(prop[key], f"{where}.{key}", AssetValidationError)
    _validate_vector(prop["base_distance_profile"], DISTANCE_AXIS_IDS, f"{where}.base_distance_profile")
    _validate_vector(prop["base_load_profile"], LOAD_AXIS_IDS, f"{where}.base_load_profile")


def _validate_embodiment_profile(value: Any, where: str) -> None:
    profile = _require_mapping(value, where, AssetValidationError)
    _require_exact_keys(
        profile,
        {"id", "capability_capacities", "unavailable_channels", "support_types", "provenance_record_ids"},
        where,
        AssetValidationError,
    )
    _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
    capacities = _require_list(profile["capability_capacities"], f"{where}.capability_capacities", AssetValidationError)
    seen_capabilities: set[str] = set()
    for index, raw_capacity in enumerate(capacities):
        capacity_where = f"{where}.capability_capacities[{index}]"
        item = _require_mapping(raw_capacity, capacity_where, AssetValidationError)
        _require_exact_keys(item, {"id", "capacity"}, capacity_where, AssetValidationError)
        capability_id = _require_nonempty_string(item["id"], f"{capacity_where}.id", AssetValidationError)
        if capability_id in seen_capabilities:
            raise AssetValidationError(f"duplicate profile capability {capability_id}")
        seen_capabilities.add(capability_id)
        _require_int_range(item["capacity"], 0, 64, f"{capacity_where}.capacity", AssetValidationError)
    _require_string_list(profile["unavailable_channels"], f"{where}.unavailable_channels", AssetValidationError)
    _require_string_list(profile["support_types"], f"{where}.support_types", AssetValidationError)
    _require_string_list(profile["provenance_record_ids"], f"{where}.provenance_record_ids", AssetValidationError, allow_empty=False)


def _validate_locale_alias_records(value: Any, where: str) -> list[Mapping[str, Any]]:
    records = _require_list(value, where, AssetValidationError)
    if not records:
        raise AssetValidationError(f"{where} must not be empty")
    seen_locales: set[str] = set()
    result: list[Mapping[str, Any]] = []
    for index, raw_record in enumerate(records):
        record_where = f"{where}[{index}]"
        record = _require_mapping(raw_record, record_where, AssetValidationError)
        _require_exact_keys(record, {"locale", "values"}, record_where, AssetValidationError)
        locale = record["locale"]
        if locale not in {"ko", "en", "ja", "zh"} or locale in seen_locales:
            raise AssetValidationError(f"{record_where}.locale is unknown or duplicated")
        seen_locales.add(str(locale))
        _require_string_list(
            record["values"],
            f"{record_where}.values",
            AssetValidationError,
            allow_empty=False,
        )
        result.append(record)
    return result


def _validate_lexeme_groups(
    value: Any,
    where: str,
    *,
    maximum_groups: int,
) -> list[list[str]]:
    groups = _require_list(value, where, AssetValidationError)
    if not groups or len(groups) > maximum_groups:
        raise AssetValidationError(f"{where} must contain 1..{maximum_groups} AND-groups")
    normalized_groups: list[list[str]] = []
    for index, raw_group in enumerate(groups):
        group = _require_string_list(
            raw_group,
            f"{where}[{index}]",
            AssetValidationError,
            allow_empty=False,
        )
        normalized = [_normalize_text(item) for item in group]
        if len(normalized) != len(set(normalized)):
            raise AssetValidationError(f"{where}[{index}] has normalized duplicate alternatives")
        normalized_groups.append(group)
    if len({tuple(_normalize_text(item) for item in group) for group in normalized_groups}) != len(normalized_groups):
        raise AssetValidationError(f"{where} has duplicate normalized groups")
    return normalized_groups


def _validate_polarized_literal_groups(
    value: Any,
    where: str,
    *,
    maximum_groups: int,
    allow_empty: bool = False,
) -> list[Mapping[str, Any]]:
    """Validate data-owned AND-groups with an explicit occurrence polarity."""

    groups = _require_list(value, where, AssetValidationError)
    if (not allow_empty and not groups) or len(groups) > maximum_groups:
        lower = 0 if allow_empty else 1
        raise AssetValidationError(
            f"{where} must contain {lower}..{maximum_groups} polarized AND-groups"
        )
    normalized_groups: set[tuple[tuple[str, ...], str]] = set()
    result: list[Mapping[str, Any]] = []
    for index, raw_group in enumerate(groups):
        group_where = f"{where}[{index}]"
        group = _require_mapping(raw_group, group_where, AssetValidationError)
        _require_exact_keys(
            group,
            {"alternatives", "required_polarity"},
            group_where,
            AssetValidationError,
        )
        alternatives = _require_string_list(
            group["alternatives"],
            f"{group_where}.alternatives",
            AssetValidationError,
            allow_empty=False,
        )
        normalized = tuple(_normalize_text(item) for item in alternatives)
        if len(normalized) != len(set(normalized)):
            raise AssetValidationError(f"{group_where}.alternatives has normalized duplicates")
        polarity = group["required_polarity"]
        if polarity not in {"affirmative", "negated"}:
            raise AssetValidationError(f"{group_where}.required_polarity is outside the closed enum")
        signature = (normalized, str(polarity))
        if signature in normalized_groups:
            raise AssetValidationError(f"{where} contains a duplicate polarized group")
        normalized_groups.add(signature)
        result.append(group)
    return result


def _is_normalized_english_lexeme(value: str) -> bool:
    return (
        bool(value)
        and value == _normalize_text(value)
        and value.isascii()
        and all(character.isalnum() or character == " " for character in value)
    )


def _validate_semantic_bindings_asset(
    asset: Mapping[str, Any],
    *,
    candidate_by_id: Mapping[str, Mapping[str, Any]],
    candidate_asset: Mapping[str, Any],
    prop_by_id: Mapping[str, Mapping[str, Any]],
    compatibility: Mapping[str, Any],
) -> tuple[
    dict[str, tuple[Mapping[str, Any], ...]],
    dict[str, tuple[Mapping[str, Any], ...]],
    dict[str, Mapping[str, Any]],
    dict[str, Mapping[str, Any]],
]:
    _require_exact_keys(
        asset,
        {
            "schema",
            "reviewed_at",
            "normalization",
            "prop_literal_sense_bindings",
            "explicit_capability_assertion_profiles",
            "literal_polarity_contract",
            "literal_quantity_bindings",
            "identity_literal_profiles",
            "context_literal_profiles",
            "literal_visual_realization_profiles",
            "visual_carrier_profiles",
            "resource_carrier_profiles",
            "semantic_effect_registry",
            "guard_execution_profiles",
            "contract_effect_profiles",
            "counts",
        },
        "semantic_bindings",
        AssetValidationError,
    )
    if asset["schema"] != SEMANTIC_BINDINGS_SCHEMA:
        raise AssetValidationError(f"semantic_bindings.schema must be {SEMANTIC_BINDINGS_SCHEMA}")
    _require_nonempty_string(asset["reviewed_at"], "semantic_bindings.reviewed_at", AssetValidationError)
    if asset["normalization"] != NORMALIZATION_ID:
        raise AssetValidationError(f"semantic_bindings.normalization must be {NORMALIZATION_ID}")

    prop_senses = _require_list(
        asset["prop_literal_sense_bindings"],
        "semantic_bindings.prop_literal_sense_bindings",
        AssetValidationError,
    )
    prop_sense_by_catalog_id_mut: dict[str, list[Mapping[str, Any]]] = {}
    prop_sense_ids: set[str] = set()
    for index, raw_profile in enumerate(prop_senses):
        where = f"semantic_bindings.prop_literal_sense_bindings[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(
            profile,
            {"id", "catalog_prop_id", "literal_aliases", "accepted_semantic_tokens", "activation_target"},
            where,
            AssetValidationError,
        )
        profile_id = _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
        if profile_id in prop_sense_ids:
            raise AssetValidationError(f"duplicate prop literal sense binding: {profile_id}")
        prop_sense_ids.add(profile_id)
        catalog_prop_id = _require_nonempty_string(
            profile["catalog_prop_id"], f"{where}.catalog_prop_id", AssetValidationError
        )
        if catalog_prop_id not in prop_by_id:
            raise AssetValidationError(f"{where}.catalog_prop_id is unknown")
        if "sense_disambiguation_required" not in prop_by_id[catalog_prop_id]["risk_tags"]:
            raise AssetValidationError(f"{where} may only refine a catalog prop that requires sense disambiguation")
        _validate_locale_alias_records(profile["literal_aliases"], f"{where}.literal_aliases")
        semantic_tokens = _require_string_list(
            profile["accepted_semantic_tokens"],
            f"{where}.accepted_semantic_tokens",
            AssetValidationError,
            allow_empty=False,
        )
        if any(len(_semantic_tokens(token)) != 1 for token in semantic_tokens):
            raise AssetValidationError(f"{where}.accepted_semantic_tokens must be closed single semantic tokens")
        activation_target = profile["activation_target"]
        if activation_target is not None and activation_target not in prop_by_id:
            raise AssetValidationError(f"{where}.activation_target is unknown")
        prop_sense_by_catalog_id_mut.setdefault(catalog_prop_id, []).append(profile)

    capability_profiles = _require_list(
        asset["explicit_capability_assertion_profiles"],
        "semantic_bindings.explicit_capability_assertion_profiles",
        AssetValidationError,
    )
    capability_by_id_mut: dict[str, list[Mapping[str, Any]]] = {}
    capability_profile_ids: set[str] = set()
    for index, raw_profile in enumerate(capability_profiles):
        where = f"semantic_bindings.explicit_capability_assertion_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(
            profile,
            {"id", "capability_id", "assertion", "minimum_capacity", "maximum_capacity", "required_literal_groups"},
            where,
            AssetValidationError,
        )
        profile_id = _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
        if profile_id in capability_profile_ids:
            raise AssetValidationError(f"duplicate capability assertion profile: {profile_id}")
        capability_profile_ids.add(profile_id)
        capability_id = _require_nonempty_string(
            profile["capability_id"], f"{where}.capability_id", AssetValidationError
        )
        if capability_id not in ENTITY_RESOURCE_KINDS:
            raise AssetValidationError(f"{where}.capability_id is outside the entity resource enum")
        if profile["assertion"] not in {"available", "unavailable"}:
            raise AssetValidationError(f"{where}.assertion is outside the closed enum")
        minimum = _require_int_range(
            profile["minimum_capacity"], 0, 64, f"{where}.minimum_capacity", AssetValidationError
        )
        maximum = _require_int_range(
            profile["maximum_capacity"], 0, 64, f"{where}.maximum_capacity", AssetValidationError
        )
        if minimum > maximum:
            raise AssetValidationError(f"{where} capacity range is inverted")
        if profile["assertion"] == "unavailable" and (minimum != 0 or maximum != 0):
            raise AssetValidationError(f"{where} unavailable assertion must be exactly capacity 0")
        if profile["assertion"] == "available" and minimum < 1:
            raise AssetValidationError(f"{where} available assertion must require positive capacity")
        _validate_lexeme_groups(
            profile["required_literal_groups"],
            f"{where}.required_literal_groups",
            maximum_groups=4,
        )
        capability_by_id_mut.setdefault(capability_id, []).append(profile)

    polarity = _require_mapping(
        asset["literal_polarity_contract"],
        "semantic_bindings.literal_polarity_contract",
        AssetValidationError,
    )
    _require_exact_keys(
        polarity,
        {"negative_markers", "target_profiles"},
        "semantic_bindings.literal_polarity_contract",
        AssetValidationError,
    )
    negative_records = _require_list(
        polarity["negative_markers"],
        "semantic_bindings.literal_polarity_contract.negative_markers",
        AssetValidationError,
    )
    negative_locales: set[str] = set()
    for index, raw_record in enumerate(negative_records):
        where = f"semantic_bindings.literal_polarity_contract.negative_markers[{index}]"
        record = _require_mapping(raw_record, where, AssetValidationError)
        _require_exact_keys(
            record,
            {
                "locale",
                "logical_values",
                "target_absence_values",
                "target_substitution_values",
                "affirmative_conflict_values",
            },
            where,
            AssetValidationError,
        )
        locale = record["locale"]
        if locale not in {"ko", "en", "ja", "zh"} or locale in negative_locales:
            raise AssetValidationError(f"{where}.locale is unknown or duplicated")
        negative_locales.add(str(locale))
        for field in (
            "logical_values",
            "target_absence_values",
            "affirmative_conflict_values",
        ):
            _require_string_list(
                record[field],
                f"{where}.{field}",
                AssetValidationError,
                allow_empty=False,
            )
        substitution_records = _require_list(
            record["target_substitution_values"],
            f"{where}.target_substitution_values",
            AssetValidationError,
        )
        if not substitution_records:
            raise AssetValidationError(
                f"{where}.target_substitution_values must not be empty"
            )
        substitution_values: set[str] = set()
        for substitution_index, raw_substitution in enumerate(substitution_records):
            substitution_where = (
                f"{where}.target_substitution_values[{substitution_index}]"
            )
            substitution = _require_mapping(
                raw_substitution,
                substitution_where,
                AssetValidationError,
            )
            _require_exact_keys(
                substitution,
                {"value", "marker_position_relative_to_negated_target"},
                substitution_where,
                AssetValidationError,
            )
            substitution_value = _require_nonempty_string(
                substitution["value"],
                f"{substitution_where}.value",
                AssetValidationError,
            )
            if substitution_value in substitution_values:
                raise AssetValidationError(
                    f"{where}.target_substitution_values must not contain duplicate values"
                )
            substitution_values.add(substitution_value)
            marker_position = _require_nonempty_string(
                substitution["marker_position_relative_to_negated_target"],
                f"{substitution_where}.marker_position_relative_to_negated_target",
                AssetValidationError,
            )
            if marker_position not in {"before", "after"}:
                raise AssetValidationError(
                    f"{substitution_where}.marker_position_relative_to_negated_target "
                    "is outside the closed enum"
                )
    if negative_locales != {"ko", "en", "ja", "zh"}:
        raise AssetValidationError("literal polarity negative markers must cover ko/en/ja/zh")
    target_profiles = _require_list(
        polarity["target_profiles"],
        "semantic_bindings.literal_polarity_contract.target_profiles",
        AssetValidationError,
    )
    target_keys: set[tuple[str, str]] = set()
    for index, raw_profile in enumerate(target_profiles):
        where = f"semantic_bindings.literal_polarity_contract.target_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(profile, {"target_kind", "target_id", "literal_alternatives"}, where, AssetValidationError)
        target_kind = profile["target_kind"]
        target_id = profile["target_id"]
        if target_kind == "slot":
            allowed_ids = set(SCENE_SLOT_IDS)
        elif target_kind == "event_role":
            allowed_ids = set(EVENT_ROLE_IDS)
        else:
            raise AssetValidationError(f"{where}.target_kind is outside the closed enum")
        if target_id not in allowed_ids:
            raise AssetValidationError(f"{where}.target_id is unknown for {target_kind}")
        key = (str(target_kind), str(target_id))
        if key in target_keys:
            raise AssetValidationError(f"duplicate literal polarity target: {key}")
        target_keys.add(key)
        _require_string_list(
            profile["literal_alternatives"],
            f"{where}.literal_alternatives",
            AssetValidationError,
            allow_empty=False,
        )
    expected_targets = {
        *(("slot", slot_id) for slot_id in SCENE_SLOT_IDS),
        *(("event_role", role_id) for role_id in EVENT_ROLE_IDS),
    }
    if target_keys != expected_targets:
        raise AssetValidationError("literal polarity target profiles must exactly cover all slots and event roles")

    quantity_bindings = _require_list(
        asset["literal_quantity_bindings"],
        "semantic_bindings.literal_quantity_bindings",
        AssetValidationError,
    )
    quantity_values: set[int] = set()
    for index, raw_profile in enumerate(quantity_bindings):
        where = f"semantic_bindings.literal_quantity_bindings[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(profile, {"id", "quantity", "literal_aliases"}, where, AssetValidationError)
        _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
        quantity = _require_int_range(profile["quantity"], 1, 64, f"{where}.quantity", AssetValidationError)
        if quantity in quantity_values:
            raise AssetValidationError(f"duplicate literal quantity binding: {quantity}")
        quantity_values.add(quantity)
        alias_records = _validate_locale_alias_records(
            profile["literal_aliases"], f"{where}.literal_aliases"
        )
        if {record["locale"] for record in alias_records} != {"ko", "en", "ja", "zh"}:
            raise AssetValidationError(f"{where} must cover ko/en/ja/zh")
    if not {1, 2, 3, 4} <= quantity_values:
        raise AssetValidationError("literal quantity bindings must cover at least 1,2,3,4")

    identity_profiles = _require_list(
        asset["identity_literal_profiles"],
        "semantic_bindings.identity_literal_profiles",
        AssetValidationError,
    )
    identity_profile_ids: set[str] = set()
    for index, raw_profile in enumerate(identity_profiles):
        where = f"semantic_bindings.identity_literal_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(profile, {"id", "literal_aliases", "required_lexeme_groups"}, where, AssetValidationError)
        profile_id = _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
        if profile_id in identity_profile_ids:
            raise AssetValidationError(f"duplicate identity literal profile: {profile_id}")
        identity_profile_ids.add(profile_id)
        _validate_locale_alias_records(profile["literal_aliases"], f"{where}.literal_aliases")
        _validate_lexeme_groups(
            profile["required_lexeme_groups"],
            f"{where}.required_lexeme_groups",
            maximum_groups=3,
        )

    context_literal_profiles = _require_list(
        asset["context_literal_profiles"],
        "semantic_bindings.context_literal_profiles",
        AssetValidationError,
    )
    context_literal_keys: set[tuple[str, str]] = set()
    allowed_context_literal_fields = {"era_technology", "tone", "violence", "scale"}
    for index, raw_profile in enumerate(context_literal_profiles):
        where = f"semantic_bindings.context_literal_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(
            profile,
            {"id", "field", "value", "required_literal_groups", "polarity"},
            where,
            AssetValidationError,
        )
        _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
        field = _require_nonempty_string(profile["field"], f"{where}.field", AssetValidationError)
        value = _require_nonempty_string(profile["value"], f"{where}.value", AssetValidationError)
        key = (field, value)
        if field not in allowed_context_literal_fields or key in context_literal_keys:
            raise AssetValidationError(f"{where} is unknown or duplicated")
        context_literal_keys.add(key)
        _validate_lexeme_groups(
            profile["required_literal_groups"],
            f"{where}.required_literal_groups",
            maximum_groups=3,
        )
        if profile["polarity"] not in {"affirmative", "negated"}:
            raise AssetValidationError(f"{where}.polarity is outside the closed enum")
    expected_context_literal_keys = {
        ("era_technology", "decommissioned_firearm"),
        ("era_technology", "industrial"),
        ("tone", "investigative"),
        ("tone", "quiet_everyday"),
        ("violence", "active"),
        ("violence", "closed"),
        ("violence", "nonviolent"),
    }
    if context_literal_keys != expected_context_literal_keys:
        raise AssetValidationError(
            "context literal profiles must exactly cover executable non-default context values"
        )

    literal_realization_profiles = _require_list(
        asset["literal_visual_realization_profiles"],
        "semantic_bindings.literal_visual_realization_profiles",
        AssetValidationError,
    )
    literal_realization_ids: set[str] = set()
    literal_realization_candidates: set[str] = set()
    literal_realization_ranks: set[int] = set()
    for index, raw_profile in enumerate(literal_realization_profiles):
        where = f"semantic_bindings.literal_visual_realization_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(
            profile,
            {
                "id",
                "source_slot_id",
                "mechanism_class_id",
                "realized_facet",
                "candidate_group",
                "participant_roles",
                "quantifier",
                "enforcement",
                "literal_scope",
                "required_literal_groups",
                "owned_pixel_kinds",
                "owned_resource_kinds",
                "selection_rank",
            },
            where,
            AssetValidationError,
        )
        profile_id = _require_nonempty_string(
            profile["id"], f"{where}.id", AssetValidationError
        )
        if profile_id in literal_realization_ids:
            raise AssetValidationError(f"duplicate literal visual realization profile: {profile_id}")
        literal_realization_ids.add(profile_id)
        source_slot_id = _require_nonempty_string(
            profile["source_slot_id"], f"{where}.source_slot_id", AssetValidationError
        )
        if source_slot_id not in SCENE_SLOT_IDS:
            raise AssetValidationError(f"{where}.source_slot_id is outside the closed slot enum")
        mechanism_class_id = _require_nonempty_string(
            profile["mechanism_class_id"], f"{where}.mechanism_class_id", AssetValidationError
        )
        if mechanism_class_id not in LITERAL_REALIZATION_MECHANISM_IDS:
            raise AssetValidationError(f"{where}.mechanism_class_id is outside the closed enum")
        realized_facet = _require_nonempty_string(
            profile["realized_facet"], f"{where}.realized_facet", AssetValidationError
        )
        if realized_facet not in LITERAL_REALIZATION_FACETS_BY_SLOT[source_slot_id]:
            raise AssetValidationError(
                f"{where}.realized_facet is incompatible with its reviewed source slot"
            )
        candidate_group = _require_string_list(
            profile["candidate_group"], f"{where}.candidate_group", AssetValidationError,
            allow_empty=False,
        )
        if candidate_group != sorted(set(candidate_group)):
            raise AssetValidationError(f"{where}.candidate_group must be sorted and unique")
        candidates_in_group: list[Mapping[str, Any]] = []
        for candidate_id in candidate_group:
            candidate = candidate_by_id.get(candidate_id)
            if candidate is None or candidate["role"] != "visual_atom":
                raise AssetValidationError(f"{where}.candidate_group contains a nonvisual candidate")
            if candidate["facet"] != realized_facet:
                raise AssetValidationError(f"{where}.candidate_group contains a wrong-facet candidate")
            if candidate_id in literal_realization_candidates:
                raise AssetValidationError(
                    f"{where}.candidate_group repeats an ambiguous candidate binding"
                )
            literal_realization_candidates.add(candidate_id)
            candidates_in_group.append(candidate)
        participant_roles = _require_list(
            profile["participant_roles"],
            f"{where}.participant_roles",
            AssetValidationError,
        )
        if not participant_roles:
            raise AssetValidationError(f"{where}.participant_roles must not be empty")
        seen_participant_roles: set[str] = set()
        participant_role_ids: list[str] = []
        for participant_index, raw_participant in enumerate(participant_roles):
            participant_where = f"{where}.participant_roles[{participant_index}]"
            participant = _require_mapping(
                raw_participant, participant_where, AssetValidationError
            )
            _require_exact_keys(
                participant,
                {"role_id", "entity_quantifier"},
                participant_where,
                AssetValidationError,
            )
            role_id = participant["role_id"]
            if role_id not in EVENT_ROLE_IDS or role_id in seen_participant_roles:
                raise AssetValidationError(
                    f"{participant_where}.role_id is unknown or duplicated"
                )
            seen_participant_roles.add(str(role_id))
            participant_role_ids.append(str(role_id))
            if participant["entity_quantifier"] not in {"primary", "all"}:
                raise AssetValidationError(
                    f"{participant_where}.entity_quantifier is outside the closed enum"
                )
        if participant_role_ids != sorted(
            participant_role_ids,
            key=lambda role_id: EVENT_ROLE_IDS.index(role_id),
        ):
            raise AssetValidationError(
                f"{where}.participant_roles must preserve EVENT_ROLE_IDS order"
            )
        if profile["quantifier"] not in {"any", "all"}:
            raise AssetValidationError(f"{where}.quantifier is outside the closed enum")
        if profile["enforcement"] not in {"selected", "eligible"}:
            raise AssetValidationError(f"{where}.enforcement is outside the closed enum")
        scope = profile["literal_scope"]
        if scope not in LITERAL_REALIZATION_SCOPE_IDS:
            raise AssetValidationError(f"{where}.literal_scope is outside the closed enum")
        raw_groups = _require_list(
            profile["required_literal_groups"],
            f"{where}.required_literal_groups",
            AssetValidationError,
        )
        if scope == "fixed_value_bindings":
            if raw_groups:
                _validate_polarized_literal_groups(
                    raw_groups,
                    f"{where}.required_literal_groups",
                    maximum_groups=3,
                )
            else:
                expected_group = NEUTRAL_FIXED_VALUE_PROJECTION_GROUPS.get(mechanism_class_id)
                if expected_group is None or tuple(candidate_group) != expected_group:
                    raise AssetValidationError(
                        f"{where} empty binding scope may only authorize a closed neutral projection"
                    )
                if source_slot_id not in {"action", "prop"} or realized_facet != source_slot_id:
                    raise AssetValidationError(
                        f"{where} empty binding scope may only realize its identical source facet"
                    )
        else:
            _validate_polarized_literal_groups(
                raw_groups,
                f"{where}.required_literal_groups",
                maximum_groups=3,
            )
        owned_pixel_kinds = _require_string_list(
            profile["owned_pixel_kinds"],
            f"{where}.owned_pixel_kinds",
            AssetValidationError,
        )
        if owned_pixel_kinds != sorted(set(owned_pixel_kinds)) or set(owned_pixel_kinds) - set(PIXEL_EVIDENCE_KIND_IDS):
            raise AssetValidationError(f"{where}.owned_pixel_kinds is unsorted, duplicated, or unknown")
        owned_resource_kinds = _require_string_list(
            profile["owned_resource_kinds"],
            f"{where}.owned_resource_kinds",
            AssetValidationError,
        )
        if owned_resource_kinds != sorted(set(owned_resource_kinds)) or set(owned_resource_kinds) - set(compatibility["resource_kind_ids"]):
            raise AssetValidationError(f"{where}.owned_resource_kinds is unsorted, duplicated, or unknown")
        candidate_pixel_sets = [
            {str(item["kind"]) for item in candidate["runtime_contract"]["pixel_evidence"]}
            for candidate in candidates_in_group
        ]
        candidate_resource_sets = [
            {str(item[0]) for item in candidate["runtime_contract"]["resource_claims"]}
            for candidate in candidates_in_group
        ]
        if profile["quantifier"] == "any":
            pixel_ownership_ok = all(
                set(owned_pixel_kinds) <= kinds for kinds in candidate_pixel_sets
            )
            resource_ownership_ok = all(
                set(owned_resource_kinds) <= kinds for kinds in candidate_resource_sets
            )
        else:
            pixel_ownership_ok = set(owned_pixel_kinds) <= set().union(*candidate_pixel_sets)
            resource_ownership_ok = set(owned_resource_kinds) <= set().union(*candidate_resource_sets)
        if not pixel_ownership_ok:
            raise AssetValidationError(
                f"{where}.owned_pixel_kinds lack exact candidate-group ownership"
            )
        if not resource_ownership_ok:
            raise AssetValidationError(
                f"{where}.owned_resource_kinds lack exact candidate-group ownership"
            )
        rank = _require_int_range(
            profile["selection_rank"], 0, 999, f"{where}.selection_rank", AssetValidationError
        )
        if rank in literal_realization_ranks:
            raise AssetValidationError(f"duplicate literal realization selection rank: {rank}")
        literal_realization_ranks.add(rank)

    visual_profiles = _require_list(
        asset["visual_carrier_profiles"],
        "semantic_bindings.visual_carrier_profiles",
        AssetValidationError,
    )
    visual_by_id: dict[str, Mapping[str, Any]] = {}
    forbidden_internal_terms = {
        "affordance", "manipulator", "attention channel", "prop slot", "core salience",
        "candidate id", "resource kind", "bridge type",
    }
    for index, raw_profile in enumerate(visual_profiles):
        where = f"semantic_bindings.visual_carrier_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(profile, {"candidate_id", "required_lexeme_groups"}, where, AssetValidationError)
        candidate_id = _require_nonempty_string(profile["candidate_id"], f"{where}.candidate_id", AssetValidationError)
        candidate = candidate_by_id.get(candidate_id)
        if candidate is None or candidate["role"] != "visual_atom" or candidate_id in visual_by_id:
            raise AssetValidationError(f"{where}.candidate_id is unknown, nonvisual, or duplicated")
        groups = _validate_lexeme_groups(
            profile["required_lexeme_groups"],
            f"{where}.required_lexeme_groups",
            maximum_groups=2,
        )
        if any(
            internal in _normalize_text(alternative)
            for group in groups
            for alternative in group
            for internal in forbidden_internal_terms
        ):
            raise AssetValidationError(f"{where} exposes internal runtime jargon")
        if any(
            not _is_normalized_english_lexeme(str(alternative))
            for group in groups
            for alternative in group
        ):
            raise AssetValidationError(
                f"{where} alternatives must be normalized lower-case English lexemes"
            )
        visual_by_id[candidate_id] = profile
    expected_visual_ids = {
        candidate_id
        for candidate_id, candidate in candidate_by_id.items()
        if candidate["role"] == "visual_atom"
    }
    if set(visual_by_id) != expected_visual_ids:
        raise AssetValidationError("visual carrier profiles must exactly cover executable visual candidates")

    resource_profiles = _require_list(
        asset["resource_carrier_profiles"],
        "semantic_bindings.resource_carrier_profiles",
        AssetValidationError,
    )
    resource_by_kind: dict[str, Mapping[str, Any]] = {}
    for index, raw_profile in enumerate(resource_profiles):
        where = f"semantic_bindings.resource_carrier_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(profile, {"resource_kind", "required_lexeme_groups"}, where, AssetValidationError)
        kind = _require_nonempty_string(profile["resource_kind"], f"{where}.resource_kind", AssetValidationError)
        if kind in resource_by_kind:
            raise AssetValidationError(f"duplicate resource carrier profile: {kind}")
        groups = _validate_lexeme_groups(
            profile["required_lexeme_groups"],
            f"{where}.required_lexeme_groups",
            maximum_groups=1,
        )
        if any(
            not _is_normalized_english_lexeme(str(alternative))
            or any(internal in _normalize_text(str(alternative)) for internal in forbidden_internal_terms)
            for group in groups
            for alternative in group
        ):
            raise AssetValidationError(
                f"{where} must use normalized neutral visual terms without internal runtime jargon"
            )
        resource_by_kind[kind] = profile
    resource_kinds = set(compatibility["resource_kind_ids"])
    if set(resource_by_kind) != resource_kinds:
        raise AssetValidationError("resource carrier profiles must exactly cover compatibility resource kinds")

    contract_effect_profiles = _require_list(
        asset["contract_effect_profiles"],
        "semantic_bindings.contract_effect_profiles",
        AssetValidationError,
    )
    contract_effect_by_id: dict[str, Mapping[str, Any]] = {}
    contract_effect_ids: set[str] = set()
    valid_source_ids = {
        "request": {"concept"},
        "identity_fact": {"feature_fact", "scene_fact", "forbidden_fact"},
        "slot": set(SCENE_SLOT_IDS),
        "event_role": set(EVENT_ROLE_IDS),
        "context": set(CONTEXT_FIELD_IDS),
    }
    for index, raw_profile in enumerate(contract_effect_profiles):
        where = f"semantic_bindings.contract_effect_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(
            profile,
            {
                "id",
                "effect_id",
                "source_targets",
                "semantic_value_ids",
                "literal_aliases",
                "required_literal_groups",
                "polarity",
                "subject_binding",
            },
            where,
            AssetValidationError,
        )
        profile_id = _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
        if profile_id in contract_effect_by_id:
            raise AssetValidationError(f"duplicate contract effect profile: {profile_id}")
        effect_id = _require_nonempty_string(
            profile["effect_id"], f"{where}.effect_id", AssetValidationError
        )
        if effect_id not in SEMANTIC_EFFECT_IDS or effect_id in contract_effect_ids:
            raise AssetValidationError(f"{where}.effect_id is unknown or duplicated")
        contract_effect_ids.add(effect_id)
        targets = _require_list(profile["source_targets"], f"{where}.source_targets", AssetValidationError)
        if not targets:
            raise AssetValidationError(f"{where}.source_targets must not be empty")
        seen_targets: set[tuple[str, str]] = set()
        for target_index, raw_target in enumerate(targets):
            target_where = f"{where}.source_targets[{target_index}]"
            target = _require_mapping(raw_target, target_where, AssetValidationError)
            _require_exact_keys(target, {"source_kind", "source_id"}, target_where, AssetValidationError)
            source_kind = target["source_kind"]
            source_id = target["source_id"]
            if (
                source_kind not in CONTRACT_EFFECT_SOURCE_KIND_IDS
                or source_id not in valid_source_ids[source_kind]
                or (source_kind, source_id) in seen_targets
            ):
                raise AssetValidationError(f"{target_where} is unknown or duplicated")
            seen_targets.add((str(source_kind), str(source_id)))
        semantic_values = _require_string_list(
            profile["semantic_value_ids"],
            f"{where}.semantic_value_ids",
            AssetValidationError,
            allow_empty=False,
        )
        if any(not _semantic_tokens(value) for value in semantic_values):
            raise AssetValidationError(f"{where}.semantic_value_ids contains an empty semantic value")
        alias_records = _validate_locale_alias_records(
            profile["literal_aliases"], f"{where}.literal_aliases"
        )
        if {record["locale"] for record in alias_records} != {"ko", "en", "ja", "zh"}:
            raise AssetValidationError(f"{where}.literal_aliases must cover ko/en/ja/zh")
        _validate_lexeme_groups(
            profile["required_literal_groups"],
            f"{where}.required_literal_groups",
            maximum_groups=3,
        )
        if profile["polarity"] != "affirmative":
            raise AssetValidationError(f"{where}.polarity must be affirmative")
        if profile["subject_binding"] not in CONTRACT_EFFECT_SUBJECT_BINDINGS:
            raise AssetValidationError(f"{where}.subject_binding is outside the closed enum")
        contract_effect_by_id[profile_id] = profile
    if contract_effect_ids != set(SEMANTIC_EFFECT_IDS):
        raise AssetValidationError("contract effect profiles must exactly cover the closed effect enum")

    effect_registry = _require_mapping(
        asset["semantic_effect_registry"],
        "semantic_bindings.semantic_effect_registry",
        AssetValidationError,
    )
    _require_exact_keys(
        effect_registry,
        {"schema", "effect_ids", "source_kind_ids", "profiles", "counts"},
        "semantic_bindings.semantic_effect_registry",
        AssetValidationError,
    )
    if effect_registry["schema"] != SEMANTIC_EFFECT_REGISTRY_SCHEMA:
        raise AssetValidationError("semantic effect registry schema has drifted")
    if effect_registry["effect_ids"] != list(SEMANTIC_EFFECT_IDS):
        raise AssetValidationError("semantic effect IDs must equal the closed sorted enum")
    if effect_registry["source_kind_ids"] != list(SEMANTIC_EFFECT_SOURCE_KIND_IDS):
        raise AssetValidationError("semantic effect source kinds have drifted")
    expected_effect_sources = {
        "visual_candidate": {
            candidate_id
            for candidate_id, candidate in candidate_by_id.items()
            if candidate["role"] == "visual_atom"
        },
        "proposal_profile": {
            str(profile["id"])
            for profile in candidate_asset["proposal_profiles"]
        },
        "context_profile": {
            str(profile["id"])
            for profile in candidate_asset["context_distance_profiles"]
        },
        "bridge_type": set(compatibility["bridge_policy"]["bridge_type_ids"]),
        "resource_kind": set(compatibility["resource_kind_ids"]),
    }
    effect_profiles = _require_list(
        effect_registry["profiles"],
        "semantic_bindings.semantic_effect_registry.profiles",
        AssetValidationError,
    )
    seen_effect_sources: dict[str, set[str]] = {
        kind: set() for kind in SEMANTIC_EFFECT_SOURCE_KIND_IDS
    }
    for index, raw_profile in enumerate(effect_profiles):
        where = f"semantic_bindings.semantic_effect_registry.profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(
            profile,
            {"source_kind", "source_id", "effect_ids"},
            where,
            AssetValidationError,
        )
        source_kind = profile["source_kind"]
        if source_kind not in seen_effect_sources:
            raise AssetValidationError(f"{where}.source_kind is outside the closed enum")
        source_id = _require_nonempty_string(
            profile["source_id"], f"{where}.source_id", AssetValidationError
        )
        if source_id in seen_effect_sources[source_kind]:
            raise AssetValidationError(f"duplicate semantic effect source: {source_kind}:{source_id}")
        seen_effect_sources[source_kind].add(source_id)
        effects = _require_string_list(
            profile["effect_ids"],
            f"{where}.effect_ids",
            AssetValidationError,
        )
        if effects != sorted(set(effects)) or set(effects) - set(SEMANTIC_EFFECT_IDS):
            raise AssetValidationError(f"{where}.effect_ids is unsorted, duplicated, or unknown")
        if effects:
            raise AssetValidationError(
                f"{where}.effect_ids must be empty for the independently reviewed safe v1 source catalog"
            )
    if seen_effect_sources != expected_effect_sources:
        raise AssetValidationError("semantic effect profiles must exactly cover every selectable source")

    def source_semantic_strings(source_kind: str, source_id: str) -> list[str]:
        if source_kind == "visual_candidate":
            candidate = candidate_by_id[source_id]
            runtime = candidate["runtime_contract"]
            return [
                source_id,
                str(candidate["definition"]),
                *(
                    str(value)
                    for alias_record in candidate["aliases"]
                    for value in alias_record["values"]
                ),
                *(str(value) for value in runtime.get("parameters", {}).values()),
                *("::".join(str(part) for part in predicate) for predicate in runtime.get("provides", [])),
            ]
        if source_kind == "proposal_profile":
            profile = next(
                item for item in candidate_asset["proposal_profiles"] if str(item["id"]) == source_id
            )
            return [
                source_id,
                str(profile["value_id"]),
                str(profile["prompt_phrase_en"]),
                *(
                    str(alternative)
                    for group in profile["carrier_lexeme_groups"]
                    for alternative in group
                ),
                *(str(value) for value in profile["event_roles"].values() if value is not None),
            ]
        if source_kind == "context_profile":
            profile = next(
                item for item in candidate_asset["context_distance_profiles"] if str(item["id"]) == source_id
            )
            return [
                source_id,
                *("::".join(str(part) for part in predicate) for predicate in profile["requires_all"]),
                *(
                    "::".join(str(part) for part in predicate)
                    for group in profile["requires_any"]
                    for predicate in group
                ),
            ]
        if source_kind == "bridge_type":
            return [source_id]
        if source_kind == "resource_kind":
            profile = resource_by_kind[source_id]
            return [
                source_id,
                *(str(value) for group in profile["required_lexeme_groups"] for value in group),
            ]
        raise AssetValidationError(f"unknown semantic-effect source kind: {source_kind}")

    def derived_source_effects(source_kind: str, source_id: str) -> set[str]:
        strings = source_semantic_strings(source_kind, source_id)
        result: set[str] = set()
        for profile in contract_effect_profiles:
            semantic_values = {
                _normalize_text(value) for value in profile["semantic_value_ids"]
            }
            aliases = [
                str(value)
                for alias_record in profile["literal_aliases"]
                for value in alias_record["values"]
            ]
            for text in strings:
                normalized = _normalize_text(text)
                tokens = _semantic_tokens(text)
                semantic_match = any(
                    normalized == semantic_value
                    or _contains_token_subsequence(tokens, _semantic_tokens(semantic_value))
                    for semantic_value in semantic_values
                )
                literal_match = any(_literal_catalog_alias_match(alias, text) for alias in aliases)
                compositional_match = _required_literal_groups_match(
                    profile["required_literal_groups"], [text]
                )
                if semantic_match or literal_match or compositional_match:
                    result.add(str(profile["effect_id"]))
                    break
        return result

    for source_kind, source_ids in expected_effect_sources.items():
        for source_id in source_ids:
            derived = derived_source_effects(source_kind, source_id)
            declared = set(
                next(
                    profile["effect_ids"]
                    for profile in effect_profiles
                    if profile["source_kind"] == source_kind and profile["source_id"] == source_id
                )
            )
            if declared != derived:
                raise AssetValidationError(
                    f"semantic effect profile disagrees with independently derived source semantics: "
                    f"{source_kind}:{source_id} expected={sorted(derived)} actual={sorted(declared)}"
                )
    effect_counts = _require_mapping(
        effect_registry["counts"],
        "semantic_bindings.semantic_effect_registry.counts",
        AssetValidationError,
    )
    expected_effect_counts = {
        kind: len(expected_effect_sources[kind])
        for kind in SEMANTIC_EFFECT_SOURCE_KIND_IDS
    }
    expected_effect_counts["total"] = sum(expected_effect_counts.values())
    if dict(effect_counts) != expected_effect_counts:
        raise AssetValidationError("semantic effect registry counts have drifted")

    guard_profiles = _require_list(
        asset["guard_execution_profiles"],
        "semantic_bindings.guard_execution_profiles",
        AssetValidationError,
    )
    expected_guard_ids = {
        candidate_id
        for candidate_id, candidate in candidate_by_id.items()
        if candidate["role"] == "guard"
    }
    guard_profile_map: dict[str, str] = {}
    for index, raw_profile in enumerate(guard_profiles):
        where = f"semantic_bindings.guard_execution_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(profile, {"guard_id", "predicate_id"}, where, AssetValidationError)
        guard_id = _require_nonempty_string(
            profile["guard_id"], f"{where}.guard_id", AssetValidationError
        )
        predicate_id = _require_nonempty_string(
            profile["predicate_id"], f"{where}.predicate_id", AssetValidationError
        )
        if guard_id in guard_profile_map:
            raise AssetValidationError(f"duplicate guard execution profile: {guard_id}")
        guard_profile_map[guard_id] = predicate_id
    if set(guard_profile_map) != expected_guard_ids:
        raise AssetValidationError("guard execution profiles must exactly cover executable guard candidates")
    if guard_profile_map != dict(GUARD_EXECUTION_PREDICATE_BY_ID):
        raise AssetValidationError("guard execution predicates drifted from the closed non-tautological evaluator")

    counts = _require_mapping(asset["counts"], "semantic_bindings.counts", AssetValidationError)
    expected_counts = {
        "prop_literal_sense_bindings": len(prop_senses),
        "explicit_capability_assertion_profiles": len(capability_profiles),
        "literal_polarity_targets": len(target_profiles),
        "literal_quantity_bindings": len(quantity_bindings),
        "identity_literal_profiles": len(identity_profiles),
        "context_literal_profiles": len(context_literal_profiles),
        "literal_visual_realization_profiles": len(literal_realization_profiles),
        "visual_carrier_profiles": len(visual_profiles),
        "resource_carrier_profiles": len(resource_profiles),
        "semantic_effect_profiles": len(effect_profiles),
        "guard_execution_profiles": len(guard_profiles),
        "contract_effect_profiles": len(contract_effect_profiles),
    }
    if dict(counts) != expected_counts:
        raise AssetValidationError(f"semantic bindings counts mismatch: expected={expected_counts}, actual={dict(counts)}")

    return (
        {key: tuple(value) for key, value in prop_sense_by_catalog_id_mut.items()},
        {key: tuple(value) for key, value in capability_by_id_mut.items()},
        visual_by_id,
        resource_by_kind,
    )


def _validate_candidate_asset(
    asset: Mapping[str, Any],
    compatibility: Mapping[str, Any],
    manifest: Mapping[str, Any] | None,
) -> tuple[
    dict[str, Mapping[str, Any]],
    dict[str, Mapping[str, Any]],
    dict[str, Mapping[str, Any]],
]:
    _require_exact_keys(
        asset,
        {
            "schema",
            "reviewed_at",
            "normalization",
            "candidate_role_ids",
            "facet_ids",
            "distance_axis_ids",
            "load_axis_ids",
            "research_packets",
            "research_manifest_sha256",
            "semantic_bindings_asset_sha256",
            "selection_contract",
            "no_prop_path",
            "nonhuman_path",
            "context_distance_profiles",
            "proposal_profiles",
            "topic_contributions",
            "candidates",
            "prop_concepts",
            "embodiment_profiles",
            "counts",
        },
        "candidate_asset",
        AssetValidationError,
    )
    if asset["schema"] != CANDIDATE_SCHEMA:
        raise AssetValidationError(f"candidate_asset.schema must be {CANDIDATE_SCHEMA}")
    _require_nonempty_string(asset["reviewed_at"], "candidate_asset.reviewed_at", AssetValidationError)
    if asset["normalization"] != NORMALIZATION_ID:
        raise AssetValidationError(f"candidate_asset.normalization must be {NORMALIZATION_ID}")
    if asset["candidate_role_ids"] != list(CANDIDATE_ROLE_IDS):
        raise AssetValidationError("candidate_asset.candidate_role_ids has drifted")
    if asset["facet_ids"] != list(FACET_IDS):
        raise AssetValidationError("candidate_asset.facet_ids has drifted")
    if asset["distance_axis_ids"] != list(DISTANCE_AXIS_IDS):
        raise AssetValidationError("candidate_asset.distance_axis_ids has drifted")
    if asset["load_axis_ids"] != list(LOAD_AXIS_IDS):
        raise AssetValidationError("candidate_asset.load_axis_ids has drifted")
    if not _is_sha256(asset["semantic_bindings_asset_sha256"]):
        raise AssetValidationError("candidate_asset.semantic_bindings_asset_sha256 is invalid")

    predicate_kinds = set(_require_string_list(
        compatibility["predicate_kind_ids"],
        "compatibility.predicate_kind_ids",
        AssetValidationError,
        allow_empty=False,
    ))
    if predicate_kinds - SUPPORTED_PREDICATE_KINDS:
        raise AssetValidationError(
            f"compatibility declares unsupported predicate kinds: {sorted(predicate_kinds - SUPPORTED_PREDICATE_KINDS)}"
        )
    resource_kinds = set(_require_string_list(
        compatibility["resource_kind_ids"],
        "compatibility.resource_kind_ids",
        AssetValidationError,
        allow_empty=False,
    ))
    operational_bridge_types = set(
        _require_string_list(
            compatibility["bridge_policy"]["bridge_type_ids"],
            "compatibility.bridge_policy.bridge_type_ids",
            AssetValidationError,
            allow_empty=False,
        )
    )

    research_packets = _require_list(asset["research_packets"], "candidate_asset.research_packets", AssetValidationError)
    if manifest is not None:
        manifest_shards = _require_list(manifest.get("shards"), "research_manifest.shards", AssetValidationError)
        expected_packet_pairs = {
            (item.get("sha256"), item.get("record_count"))
            for item in manifest_shards
            if isinstance(item, Mapping)
        }
        actual_packet_pairs: set[tuple[Any, Any]] = set()
        for index, raw_packet in enumerate(research_packets):
            where = f"candidate_asset.research_packets[{index}]"
            packet = _require_mapping(raw_packet, where, AssetValidationError)
            _require_exact_keys(packet, {"path", "sha256", "record_count", "topic_ids"}, where, AssetValidationError)
            _require_nonempty_string(packet["path"], f"{where}.path", AssetValidationError)
            if not _is_sha256(packet["sha256"]):
                raise AssetValidationError(f"{where}.sha256 is invalid")
            _require_int_range(packet["record_count"], 1, 100000, f"{where}.record_count", AssetValidationError)
            _require_string_list(packet["topic_ids"], f"{where}.topic_ids", AssetValidationError, allow_empty=False)
            actual_packet_pairs.add((packet["sha256"], packet["record_count"]))
        if actual_packet_pairs != expected_packet_pairs or len(actual_packet_pairs) != len(research_packets):
            raise AssetValidationError("candidate_asset.research_packets do not exactly match manifest shard hashes/counts")

    if not _is_sha256(asset["research_manifest_sha256"]):
        raise AssetValidationError("candidate_asset.research_manifest_sha256 is invalid")
    selection_contract = _require_mapping(asset["selection_contract"], "candidate_asset.selection_contract", AssetValidationError)
    _require_exact_keys(
        selection_contract,
        {
            "research_candidates_are_not_prompt_tags",
            "research_topic_ids_are_provenance_only",
            "visual_atoms_require_event_spine_binding",
            "router_guard_metric_prompt_emission",
            "creator_or_work_name_tokens",
            "unknown_fixed_props",
        },
        "candidate_asset.selection_contract",
        AssetValidationError,
    )
    if (
        selection_contract["research_candidates_are_not_prompt_tags"] is not True
        or selection_contract["research_topic_ids_are_provenance_only"] is not True
        or selection_contract["visual_atoms_require_event_spine_binding"] is not True
        or selection_contract["router_guard_metric_prompt_emission"] != "forbidden"
        or selection_contract["creator_or_work_name_tokens"] != "forbidden"
        or selection_contract["unknown_fixed_props"] != "preserve_as_opaque_and_do_not_invent_affordances"
    ):
        raise AssetValidationError("candidate_asset.selection_contract weakens a universal boundary")

    no_prop_path = _require_mapping(asset["no_prop_path"], "candidate_asset.no_prop_path", AssetValidationError)
    _require_exact_keys(
        no_prop_path,
        {"activation_predicate", "blocked_facets", "closed_event_roles", "allowed_realization_candidate_ids", "required_result_path"},
        "candidate_asset.no_prop_path",
        AssetValidationError,
    )
    _validate_predicate(no_prop_path["activation_predicate"], "candidate_asset.no_prop_path.activation_predicate")
    if set(_require_string_list(no_prop_path["blocked_facets"], "candidate_asset.no_prop_path.blocked_facets", AssetValidationError)) != {"prop", "prop_state"}:
        raise AssetValidationError("candidate_asset.no_prop_path.blocked_facets has drifted")
    _require_string_list(no_prop_path["closed_event_roles"], "candidate_asset.no_prop_path.closed_event_roles", AssetValidationError)
    _require_string_list(no_prop_path["allowed_realization_candidate_ids"], "candidate_asset.no_prop_path.allowed_realization_candidate_ids", AssetValidationError)
    _require_nonempty_string(no_prop_path["required_result_path"], "candidate_asset.no_prop_path.required_result_path", AssetValidationError)

    nonhuman_path = _require_mapping(asset["nonhuman_path"], "candidate_asset.nonhuman_path", AssetValidationError)
    _require_exact_keys(
        nonhuman_path,
        {"capability_router_candidate_id", "substitution_router_candidate_id", "human_channel_fabrication", "available_channel_candidate_ids"},
        "candidate_asset.nonhuman_path",
        AssetValidationError,
    )
    if nonhuman_path["human_channel_fabrication"] != "forbidden":
        raise AssetValidationError("candidate_asset.nonhuman_path permits fabricated human channels")
    for key in ("capability_router_candidate_id", "substitution_router_candidate_id"):
        _require_nonempty_string(nonhuman_path[key], f"candidate_asset.nonhuman_path.{key}", AssetValidationError)
    _require_string_list(nonhuman_path["available_channel_candidate_ids"], "candidate_asset.nonhuman_path.available_channel_candidate_ids", AssetValidationError)

    topic_contributions = _require_mapping(asset["topic_contributions"], "candidate_asset.topic_contributions", AssetValidationError)
    for topic_id, raw_ids in topic_contributions.items():
        _require_nonempty_string(topic_id, "candidate_asset.topic_contributions key", AssetValidationError)
        _require_string_list(raw_ids, f"candidate_asset.topic_contributions.{topic_id}", AssetValidationError, allow_empty=False)

    candidates = _require_list(asset["candidates"], "candidate_asset.candidates", AssetValidationError)
    if not candidates:
        raise AssetValidationError("candidate_asset.candidates must not be empty")
    candidate_by_id: dict[str, Mapping[str, Any]] = {}
    role_counts = {role: 0 for role in CANDIDATE_ROLE_IDS}
    topic_ids: set[str] = set()
    for index, raw_candidate in enumerate(candidates):
        where = f"candidate_asset.candidates[{index}]"
        candidate = _require_mapping(raw_candidate, where, AssetValidationError)
        _require_exact_keys(
            candidate,
            {
                "id",
                "role",
                "facet",
                "layer",
                "definition",
                "research_topic_ids",
                "provenance_record_ids",
                "direct_source_record_ids",
                "aliases",
                "triggers",
                "bindings",
                "parameters",
                "preconditions",
                "postconditions",
                "capabilities",
                "resource_claims",
                "semantic_distance",
                "semantic_load",
                "salience",
                "render_risk",
                "pixel_evidence",
                "runtime_contract",
                "annotation_provenance",
            },
            where,
            AssetValidationError,
        )
        candidate_id = _require_nonempty_string(candidate["id"], f"{where}.id", AssetValidationError)
        if candidate_id in candidate_by_id:
            raise AssetValidationError(f"duplicate candidate id: {candidate_id}")
        if any(key in candidate for key in ("topic_id", "route_id", "bundle_id", "route_ids", "bundle_ids")):
            raise AssetValidationError(f"universal candidate owns a forbidden route/topic field: {candidate_id}")
        role = candidate["role"]
        if role not in CANDIDATE_ROLE_IDS:
            raise AssetValidationError(f"{where}.role is outside the closed enum")
        facet = candidate["facet"]
        if facet not in FACET_IDS:
            raise AssetValidationError(f"{where}.facet is outside the closed enum")
        _require_nonempty_string(candidate["layer"], f"{where}.layer", AssetValidationError)
        _require_nonempty_string(candidate["definition"], f"{where}.definition", AssetValidationError)
        research_topics = _require_string_list(
            candidate["research_topic_ids"],
            f"{where}.research_topic_ids",
            AssetValidationError,
            allow_empty=False,
        )
        topic_ids.update(research_topics)
        _require_string_list(
            candidate["provenance_record_ids"],
            f"{where}.provenance_record_ids",
            AssetValidationError,
            allow_empty=False,
        )
        _require_string_list(candidate["direct_source_record_ids"], f"{where}.direct_source_record_ids", AssetValidationError)
        aliases = _require_list(candidate["aliases"], f"{where}.aliases", AssetValidationError)
        for alias_index, raw_alias in enumerate(aliases):
            alias_where = f"{where}.aliases[{alias_index}]"
            alias = _require_mapping(raw_alias, alias_where, AssetValidationError)
            _require_exact_keys(alias, {"locale", "values"}, alias_where, AssetValidationError)
            if alias["locale"] not in {"ko", "en", "ja", "zh"}:
                raise AssetValidationError(f"{alias_where}.locale is outside the closed enum")
            _require_string_list(alias["values"], f"{alias_where}.values", AssetValidationError, allow_empty=False)
        _validate_predicate_list(candidate["triggers"], f"{where}.triggers")
        bindings = _require_list(candidate["bindings"], f"{where}.bindings", AssetValidationError)
        for binding_index, raw_binding in enumerate(bindings):
            binding = _require_list(raw_binding, f"{where}.bindings[{binding_index}]", AssetValidationError)
            if len(binding) != 2 or binding[0] not in EVENT_ROLE_IDS or binding[1] not in {"required", "optional", "event_spine"}:
                raise AssetValidationError(f"{where}.bindings[{binding_index}] is invalid")
        _validate_parameters(candidate["parameters"], f"{where}.parameters")
        preconditions = _require_mapping(candidate["preconditions"], f"{where}.preconditions", AssetValidationError)
        _require_exact_keys(preconditions, {"requires_all", "requires_any", "forbids_any"}, f"{where}.preconditions", AssetValidationError)
        _validate_predicate_list(preconditions["requires_all"], f"{where}.preconditions.requires_all")
        _validate_predicate_groups(preconditions["requires_any"], f"{where}.preconditions.requires_any")
        _validate_predicate_list(preconditions["forbids_any"], f"{where}.preconditions.forbids_any")
        _validate_predicate_list(candidate["postconditions"], f"{where}.postconditions")
        capabilities = _require_mapping(candidate["capabilities"], f"{where}.capabilities", AssetValidationError)
        _require_exact_keys(capabilities, {"requires_all", "requires_any"}, f"{where}.capabilities", AssetValidationError)
        _validate_predicate_list(capabilities["requires_all"], f"{where}.capabilities.requires_all")
        _validate_predicate_groups(capabilities["requires_any"], f"{where}.capabilities.requires_any")
        common_claims = _require_list(candidate["resource_claims"], f"{where}.resource_claims", AssetValidationError)
        for claim_index, raw_claim in enumerate(common_claims):
            claim = _require_list(raw_claim, f"{where}.resource_claims[{claim_index}]", AssetValidationError)
            if len(claim) != 4 or claim[0] not in resource_kinds or claim[1] not in {*EVENT_ROLE_IDS, "scene"} or isinstance(claim[2], bool) or not isinstance(claim[2], int) or claim[2] <= 0 or claim[3] not in {"exclusive", "shared"}:
                raise AssetValidationError(f"{where}.resource_claims[{claim_index}] is invalid")
        semantic_distance = _require_mapping(candidate["semantic_distance"], f"{where}.semantic_distance", AssetValidationError)
        _require_exact_keys(semantic_distance, {"base", "adjustments"}, f"{where}.semantic_distance", AssetValidationError)
        _validate_vector(semantic_distance["base"], DISTANCE_AXIS_IDS, f"{where}.semantic_distance.base")
        _require_list(semantic_distance["adjustments"], f"{where}.semantic_distance.adjustments", AssetValidationError)
        _validate_vector(candidate["semantic_load"], LOAD_AXIS_IDS, f"{where}.semantic_load")
        common_salience = _require_mapping(candidate["salience"], f"{where}.salience", AssetValidationError)
        _require_exact_keys(common_salience, {"role", "displacement_cap"}, f"{where}.salience", AssetValidationError)
        if common_salience["role"] not in {"support", "nonvisual", "primary", "secondary"}:
            raise AssetValidationError(f"{where}.salience.role is invalid")
        _require_int_range(common_salience["displacement_cap"], 0, 3, f"{where}.salience.displacement_cap", AssetValidationError)
        common_risk = _require_mapping(candidate["render_risk"], f"{where}.render_risk", AssetValidationError)
        _require_exact_keys(common_risk, {"band", "tags"}, f"{where}.render_risk", AssetValidationError)
        if common_risk["band"] not in {"none", "low", "medium", "high"}:
            raise AssetValidationError(f"{where}.render_risk.band is invalid")
        _require_string_list(common_risk["tags"], f"{where}.render_risk.tags", AssetValidationError)
        common_evidence = _require_list(candidate["pixel_evidence"], f"{where}.pixel_evidence", AssetValidationError)
        annotation = _require_mapping(candidate["annotation_provenance"], f"{where}.annotation_provenance", AssetValidationError)
        _require_exact_keys(annotation, {"definition", "pixel_evidence", "runtime_fields"}, f"{where}.annotation_provenance", AssetValidationError)
        if annotation["runtime_fields"] != "design_inference":
            raise AssetValidationError(f"{where}.annotation_provenance.runtime_fields overclaims support")
        if role == "visual_atom":
            _validate_visual_contract(
                candidate["runtime_contract"],
                f"{where}.runtime_contract",
                predicate_kind_ids=predicate_kinds,
                resource_kind_ids=resource_kinds,
            )
            runtime = candidate["runtime_contract"]
            if set(runtime["bridge_types"]) - operational_bridge_types:
                raise AssetValidationError(
                    f"{where}.runtime_contract.bridge_types is outside the operational closed seven"
                )
            duplicate_pairs = (
                ("bindings", "bindings"),
                ("resource_claims", "resource_claims"),
                ("semantic_distance", "distance_profile"),
                ("semantic_load", "load_profile"),
                ("salience", "salience"),
                ("render_risk", "render_risk"),
                ("pixel_evidence", "pixel_evidence"),
            )
            for common_key, runtime_key in duplicate_pairs:
                if candidate[common_key] != runtime[runtime_key]:
                    raise AssetValidationError(f"{where} duplicate runtime field drift: {common_key}")
            if candidate["preconditions"]["requires_all"] != runtime["requires_all"] or candidate["preconditions"]["requires_any"] != runtime["requires_any"] or candidate["preconditions"]["forbids_any"] != runtime["forbids_any"] or candidate["postconditions"] != runtime["provides"]:
                raise AssetValidationError(f"{where} duplicated predicate contract drift")
            if not common_evidence:
                raise AssetValidationError(f"{where} visual atom lacks pixel evidence")
        else:
            _validate_nonvisual_contract(candidate["runtime_contract"], role, f"{where}.runtime_contract")
            if common_evidence:
                raise AssetValidationError(f"{where} nonvisual candidate exposes pixel evidence")
        role_counts[role] += 1
        candidate_by_id[candidate_id] = candidate

    all_pixel_ids = {
        evidence["id"]
        for candidate in candidates
        for evidence in candidate["pixel_evidence"]
    }
    context_profiles = _require_list(
        asset["context_distance_profiles"],
        "candidate_asset.context_distance_profiles",
        AssetValidationError,
    )
    context_profile_ids: set[str] = set()
    for index, raw_profile in enumerate(context_profiles):
        where = f"candidate_asset.context_distance_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(
            profile,
            {
                "id",
                "candidate_ids",
                "carrier_candidate_id",
                "requires_all",
                "requires_any",
                "forbids_any",
                "distance_profile",
                "load_profile",
                "bridge_types",
                "pixel_evidence_ids",
                "policy_mode",
            },
            where,
            AssetValidationError,
        )
        profile_id = _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
        if profile_id in context_profile_ids:
            raise AssetValidationError(f"duplicate context distance profile: {profile_id}")
        context_profile_ids.add(profile_id)
        candidate_ids = _require_string_list(
            profile["candidate_ids"],
            f"{where}.candidate_ids",
            AssetValidationError,
            allow_empty=False,
        )
        if set(candidate_ids) - set(candidate_by_id):
            raise AssetValidationError(f"{where} references an unknown candidate")
        if any(candidate_by_id[candidate_id]["role"] != "visual_atom" for candidate_id in candidate_ids):
            raise AssetValidationError(f"{where} may reference visual atoms only")
        carrier_candidate_id = _require_nonempty_string(
            profile["carrier_candidate_id"],
            f"{where}.carrier_candidate_id",
            AssetValidationError,
        )
        if carrier_candidate_id not in candidate_ids:
            raise AssetValidationError(f"{where}.carrier_candidate_id must be in candidate_ids")
        if carrier_candidate_id == "usl_core_identity_anchor":
            raise AssetValidationError(f"{where}.carrier_candidate_id may not be the preservation-only core anchor")
        if candidate_by_id[carrier_candidate_id]["facet"] != "bridge":
            raise AssetValidationError(
                f"{where}.carrier_candidate_id must be a reviewed bridge-facet carrier"
            )
        predicates = _validate_predicate_list(profile["requires_all"], f"{where}.requires_all")
        predicate_groups = _validate_predicate_groups(profile["requires_any"], f"{where}.requires_any")
        predicates += [predicate for group in predicate_groups for predicate in group]
        predicates += _validate_predicate_list(profile["forbids_any"], f"{where}.forbids_any")
        if {predicate[0] for predicate in predicates} - predicate_kinds:
            raise AssetValidationError(f"{where} uses a predicate kind outside compatibility")
        if any(predicate[0] == "context" and predicate[1] == "creativity" for predicate in predicates):
            raise AssetValidationError(f"{where} must not make eligibility creativity-dependent")
        if any("holdout" in part.casefold() or "case_id" in part.casefold() for predicate in predicates for part in predicate):
            raise AssetValidationError(f"{where} contains a holdout-specific predicate")
        distance_vector = _validate_vector(
            profile["distance_profile"],
            DISTANCE_AXIS_IDS,
            f"{where}.distance_profile",
        )
        _validate_vector(profile["load_profile"], LOAD_AXIS_IDS, f"{where}.load_profile")
        bridge_types = _require_string_list(
            profile["bridge_types"],
            f"{where}.bridge_types",
            AssetValidationError,
            allow_empty=False,
        )
        if set(bridge_types) - operational_bridge_types:
            raise AssetValidationError(f"{where}.bridge_types has an unknown operational type")
        evidence_ids = _require_string_list(
            profile["pixel_evidence_ids"],
            f"{where}.pixel_evidence_ids",
            AssetValidationError,
            allow_empty=False,
        )
        if set(evidence_ids) - all_pixel_ids:
            raise AssetValidationError(f"{where}.pixel_evidence_ids references unknown evidence")
        owned_evidence_ids = {
            evidence["id"]
            for candidate_id in candidate_ids
            for evidence in candidate_by_id[candidate_id]["pixel_evidence"]
        }
        if set(evidence_ids) - owned_evidence_ids:
            raise AssetValidationError(f"{where}.pixel_evidence_ids must belong to candidate_ids")
        carrier_evidence_ids = {
            evidence["id"]
            for evidence in candidate_by_id[carrier_candidate_id]["pixel_evidence"]
        }
        if not set(evidence_ids) & carrier_evidence_ids:
            raise AssetValidationError(f"{where} lacks pixel evidence owned by carrier_candidate_id")
        if profile["policy_mode"] not in {"ordinary", "safe_tool", "explicit_weapon_only"}:
            raise AssetValidationError(f"{where}.policy_mode is invalid")
        band = _distance_band(distance_vector)
        if band == "near" and not set(bridge_types) & set(ENTRY_BRIDGE_TYPES):
            raise AssetValidationError(f"{where} near profile lacks an entry bridge")
        if band == "middle" and not (
            set(bridge_types) & set(ENTRY_BRIDGE_TYPES)
            and set(bridge_types) & set(EXIT_BRIDGE_TYPES)
        ):
            raise AssetValidationError(f"{where} middle profile lacks entry+exit bridges")
        if band == "far" and not (
            set(bridge_types) & set(ENTRY_BRIDGE_TYPES)
            and set(bridge_types) & set(MEDIATION_BRIDGE_TYPES)
            and set(bridge_types) & set(EXIT_BRIDGE_TYPES)
        ):
            raise AssetValidationError(f"{where} far profile lacks entry+mediation+exit bridges")
        if (
            "usl_core_identity_anchor" not in candidate_ids
            or "pixel::usl_core_identity_anchor" not in evidence_ids
        ):
            raise AssetValidationError(f"{where} lacks the separate visible core identity anchor")

    context_carrier_ids = {
        str(profile["carrier_candidate_id"]) for profile in context_profiles
    }
    if context_carrier_ids != set(CONTEXT_PROFILE_CARRIER_CANDIDATE_IDS):
        raise AssetValidationError(
            "context profiles must use the exact reviewed bridge-carrier inventory"
        )

    proposal_prop_concept_ids: set[str] = set()
    for index, raw_prop in enumerate(
        _require_list(
            asset["prop_concepts"],
            "candidate_asset.prop_concepts",
            AssetValidationError,
        )
    ):
        where = f"candidate_asset.prop_concepts[{index}]"
        prop = _require_mapping(raw_prop, where, AssetValidationError)
        prop_id = _require_nonempty_string(
            prop.get("id"), f"{where}.id", AssetValidationError
        )
        if prop_id in proposal_prop_concept_ids:
            raise AssetValidationError(f"duplicate prop concept id: {prop_id}")
        proposal_prop_concept_ids.add(prop_id)

    proposal_profiles = _require_list(asset["proposal_profiles"], "candidate_asset.proposal_profiles", AssetValidationError)
    proposal_ids: set[str] = set()
    proposal_family_ids: set[str] = set()
    proposal_signatures: set[str] = set()
    proposal_bands: list[str] = []
    proposal_values_by_band: dict[str, list[str]] = {"near": [], "middle": [], "far": []}
    proposal_sort_loads_by_band: dict[str, set[tuple[int, int]]] = {"near": set(), "middle": set(), "far": set()}
    for index, raw_profile in enumerate(proposal_profiles):
        where = f"candidate_asset.proposal_profiles[{index}]"
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        _require_exact_keys(
            profile,
            {"id", "semantic_family_id", "semantic_family_payload", "semantic_family_signature", "candidate_ids", "slot_id", "eligible_slot_states", "value_id", "prompt_phrase_en", "carrier_lexeme_groups", "requires_all", "forbids_any", "event_roles", "distance_profile", "load_profile", "bridge_types", "pixel_evidence_ids", "remote_or_high_load", "policy_mode"},
            where,
            AssetValidationError,
        )
        profile_id = _require_nonempty_string(profile["id"], f"{where}.id", AssetValidationError)
        if profile_id in proposal_ids:
            raise AssetValidationError(f"duplicate proposal profile: {profile_id}")
        proposal_ids.add(profile_id)
        family_id = _require_nonempty_string(
            profile["semantic_family_id"], f"{where}.semantic_family_id", AssetValidationError
        )
        if family_id in proposal_family_ids:
            raise AssetValidationError(f"duplicate proposal semantic family: {family_id}")
        proposal_family_ids.add(family_id)
        signature = profile["semantic_family_signature"]
        if not _is_sha256(signature) or signature in proposal_signatures:
            raise AssetValidationError(f"{where}.semantic_family_signature is invalid or duplicated")
        proposal_signatures.add(str(signature))
        candidate_ids = _require_string_list(profile["candidate_ids"], f"{where}.candidate_ids", AssetValidationError, allow_empty=False)
        if set(candidate_ids) - set(candidate_by_id):
            raise AssetValidationError(f"{where} references an unknown candidate")
        if any(candidate_by_id[candidate_id]["role"] != "visual_atom" for candidate_id in candidate_ids):
            raise AssetValidationError(f"{where} may reference visual atoms only")
        primary_candidate = candidate_by_id[candidate_ids[0]]
        if primary_candidate["facet"] != "prop" or candidate_ids[0] == "usl_core_identity_anchor":
            raise AssetValidationError(f"{where} must place a genuine prop connector candidate first")
        if profile["slot_id"] != "prop":
            raise AssetValidationError(f"{where}.slot_id must be prop")
        eligible_states = _require_string_list(profile["eligible_slot_states"], f"{where}.eligible_slot_states", AssetValidationError, allow_empty=False)
        if set(eligible_states) - {"fixed", "open"}:
            raise AssetValidationError(f"{where}.eligible_slot_states contains an invalid state")
        value_id = _require_nonempty_string(
            profile["value_id"], f"{where}.value_id", AssetValidationError
        )
        if value_id not in proposal_prop_concept_ids:
            raise AssetValidationError(
                f"{where}.value_id must exactly reference a reviewed prop concept"
            )
        _require_nonempty_string(profile["prompt_phrase_en"], f"{where}.prompt_phrase_en", AssetValidationError)
        proposal_carrier_groups = _validate_lexeme_groups(
            profile["carrier_lexeme_groups"],
            f"{where}.carrier_lexeme_groups",
            maximum_groups=2,
        )
        if any(
            not _is_normalized_english_lexeme(str(alternative))
            for group in proposal_carrier_groups
            for alternative in group
        ):
            raise AssetValidationError(
                f"{where}.carrier_lexeme_groups must use normalized natural English lexemes"
            )
        _validate_predicate_list(profile["requires_all"], f"{where}.requires_all")
        _validate_predicate_list(profile["forbids_any"], f"{where}.forbids_any")
        roles = _require_mapping(profile["event_roles"], f"{where}.event_roles", AssetValidationError)
        _require_exact_keys(roles, EVENT_ROLE_IDS, f"{where}.event_roles", AssetValidationError)
        for role_id, value_id in roles.items():
            if value_id is not None:
                _require_nonempty_string(value_id, f"{where}.event_roles.{role_id}", AssetValidationError)
        distance_vector = _validate_vector(profile["distance_profile"], DISTANCE_AXIS_IDS, f"{where}.distance_profile")
        _validate_vector(profile["load_profile"], LOAD_AXIS_IDS, f"{where}.load_profile")
        bridge_types = _require_string_list(profile["bridge_types"], f"{where}.bridge_types", AssetValidationError, allow_empty=False)
        if set(bridge_types) - set(ENTRY_BRIDGE_TYPES + MEDIATION_BRIDGE_TYPES + EXIT_BRIDGE_TYPES):
            raise AssetValidationError(f"{where}.bridge_types has an unknown type")
        evidence_ids = _require_string_list(profile["pixel_evidence_ids"], f"{where}.pixel_evidence_ids", AssetValidationError, allow_empty=False)
        if set(evidence_ids) - all_pixel_ids:
            raise AssetValidationError(f"{where}.pixel_evidence_ids references unknown evidence")
        candidate_pixel_ids = {
            evidence["id"]
            for candidate_id in candidate_ids
            for evidence in candidate_by_id[candidate_id]["pixel_evidence"]
        }
        if set(evidence_ids) - candidate_pixel_ids:
            raise AssetValidationError(f"{where}.pixel_evidence_ids must belong to candidate_ids")
        primary_pixel_ids = {
            evidence["id"] for evidence in primary_candidate["pixel_evidence"]
        }
        if not set(evidence_ids) & primary_pixel_ids:
            raise AssetValidationError(f"{where} lacks pixel evidence owned by its connector candidate")
        if not isinstance(profile["remote_or_high_load"], bool):
            raise AssetValidationError(f"{where}.remote_or_high_load must be boolean")
        if profile["policy_mode"] not in {"ordinary", "safe_tool", "explicit_weapon_only"}:
            raise AssetValidationError(f"{where}.policy_mode is invalid")
        if profile["policy_mode"] == "explicit_weapon_only" and "open" in eligible_states:
            raise AssetValidationError(f"{where} cannot make a weapon an open-slot default")
        band = _distance_band(distance_vector)
        proposal_bands.append(band)
        proposal_values_by_band[band].append(str(profile["value_id"]))
        proposal_sort_loads_by_band[band].add(
            (
                int(profile["load_profile"]["physical"]),
                int(profile["load_profile"]["theme_displacement"]),
            )
        )
        if band == "near":
            if not set(bridge_types) & set(ENTRY_BRIDGE_TYPES):
                raise AssetValidationError(f"{where} near proposal lacks a direct entry bridge")
        elif band == "middle":
            if not (set(bridge_types) & set(ENTRY_BRIDGE_TYPES) and set(bridge_types) & set(EXIT_BRIDGE_TYPES) and len(set(bridge_types)) >= 2):
                raise AssetValidationError(f"{where} middle proposal lacks entry+exit bridges")
        else:
            if not (set(bridge_types) & set(ENTRY_BRIDGE_TYPES) and set(bridge_types) & set(MEDIATION_BRIDGE_TYPES) and set(bridge_types) & set(EXIT_BRIDGE_TYPES) and len(set(bridge_types)) >= 3):
                raise AssetValidationError(f"{where} far proposal lacks entry+mediation+exit bridges")
            if "usl_core_identity_anchor" not in candidate_ids:
                raise AssetValidationError(f"{where} far proposal lacks the visible core identity anchor")
        if profile["remote_or_high_load"] != (band == "far" or max(profile["load_profile"].values()) == 3):
            raise AssetValidationError(f"{where}.remote_or_high_load disagrees with typed profiles")
        computed_payload = _proposal_semantic_family_payload(profile, candidate_by_id)
        stored_payload = _require_mapping(
            profile["semantic_family_payload"],
            f"{where}.semantic_family_payload",
            AssetValidationError,
        )
        if dict(stored_payload) != computed_payload:
            raise AssetValidationError(
                f"{where}.semantic_family_payload disagrees with normalized slot/prop/event/resource semantics"
            )
        computed_signature = canonical_sha256(computed_payload)
        if signature != computed_signature:
            raise AssetValidationError(
                f"{where}.semantic_family_signature disagrees with semantic_family_payload"
            )
    if len(proposal_profiles) < 12 or any(proposal_bands.count(band) < 4 for band in ("near", "middle", "far")):
        raise AssetValidationError("proposal_profiles must provide at least four semantic families per distance band")
    for band in ("near", "middle", "far"):
        values = proposal_values_by_band[band]
        if max(values.count(value) for value in set(values)) * 2 > len(values):
            raise AssetValidationError(f"proposal_profiles {band} band exceeds the 50% prop/value-family cap")
        if len(proposal_sort_loads_by_band[band]) != 1:
            raise AssetValidationError(
                f"proposal_profiles {band} band must keep physical/theme-displacement sort keys tied for seed diversity"
            )

    props = _require_list(asset["prop_concepts"], "candidate_asset.prop_concepts", AssetValidationError)
    prop_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_prop in enumerate(props):
        where = f"candidate_asset.prop_concepts[{index}]"
        _validate_prop_concept(raw_prop, where)
        prop = _require_mapping(raw_prop, where, AssetValidationError)
        prop_id = str(prop["id"])
        if prop_id in prop_by_id:
            raise AssetValidationError(f"duplicate prop concept id: {prop_id}")
        unknown_affordances = set(prop["affordance_candidate_ids"]) - set(candidate_by_id)
        if unknown_affordances:
            raise AssetValidationError(f"prop {prop_id} references unknown candidates: {sorted(unknown_affordances)}")
        prop_by_id[prop_id] = prop

    profiles = _require_list(asset["embodiment_profiles"], "candidate_asset.embodiment_profiles", AssetValidationError)
    embodiment_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_profile in enumerate(profiles):
        where = f"candidate_asset.embodiment_profiles[{index}]"
        _validate_embodiment_profile(raw_profile, where)
        profile = _require_mapping(raw_profile, where, AssetValidationError)
        profile_id = str(profile["id"])
        if profile_id in embodiment_by_id:
            raise AssetValidationError(f"duplicate embodiment profile id: {profile_id}")
        embodiment_by_id[profile_id] = profile

    counts = _require_mapping(asset["counts"], "candidate_asset.counts", AssetValidationError)
    _require_exact_keys(
        counts,
        {
            "research_records",
            "research_topics",
            "research_sources",
            "research_candidates",
            "executable_candidates",
            "executable_by_role",
            "pixel_evidence_records",
            "prop_concepts",
            "embodiment_profiles",
            "proposal_profiles",
            "context_distance_profiles",
        },
        "candidate_asset.counts",
        AssetValidationError,
    )
    executable_by_role = _require_mapping(counts["executable_by_role"], "candidate_asset.counts.executable_by_role", AssetValidationError)
    if dict(executable_by_role) != role_counts:
        raise AssetValidationError(f"candidate role counts mismatch: expected={role_counts}, actual={dict(executable_by_role)}")
    expected_simple_counts = {
        "executable_candidates": len(candidates),
        "pixel_evidence_records": sum(len(item["pixel_evidence"]) for item in candidates),
        "prop_concepts": len(props),
        "embodiment_profiles": len(profiles),
        "proposal_profiles": len(proposal_profiles),
        "context_distance_profiles": len(context_profiles),
        "research_topics": len(topic_ids),
    }
    for key, expected in expected_simple_counts.items():
        if counts[key] != expected:
            raise AssetValidationError(f"candidate_asset.counts.{key} mismatch: expected={expected}, actual={counts[key]}")
    contribution_ids = {candidate_id for raw_ids in topic_contributions.values() for candidate_id in raw_ids}
    if set(topic_contributions) != topic_ids:
        raise AssetValidationError("candidate_asset.topic_contributions keys must equal active research topics")
    if contribution_ids - set(candidate_by_id):
        raise AssetValidationError(f"topic_contributions references unknown candidates: {sorted(contribution_ids-set(candidate_by_id))}")
    for key in ("capability_router_candidate_id", "substitution_router_candidate_id"):
        if nonhuman_path[key] not in candidate_by_id:
            raise AssetValidationError(f"nonhuman_path references unknown candidate: {nonhuman_path[key]}")
    if set(nonhuman_path["available_channel_candidate_ids"]) - set(candidate_by_id):
        raise AssetValidationError("nonhuman_path references unknown channel candidates")
    if set(no_prop_path["allowed_realization_candidate_ids"]) - set(candidate_by_id):
        raise AssetValidationError("no_prop_path references unknown realization candidates")
    if manifest is not None:
        manifest_topics = set(_require_string_list(manifest.get("topic_ids"), "research_manifest.topic_ids", AssetValidationError))
        if topic_ids != manifest_topics:
            raise AssetValidationError(
                f"executable catalog must actively cover all research topics; missing={sorted(manifest_topics-topic_ids)}, extra={sorted(topic_ids-manifest_topics)}"
            )
        totals = _require_mapping(manifest.get("totals"), "research_manifest.totals", AssetValidationError)
        research_expected = {
            "research_records": totals.get("record_count"),
            "research_topics": totals.get("topic_count"),
            "research_sources": totals.get("independent_source_count"),
            "research_candidates": totals.get("candidate_count"),
        }
        for key, expected in research_expected.items():
            if counts[key] != expected:
                raise AssetValidationError(f"candidate_asset.counts.{key} does not match research manifest")
    return candidate_by_id, prop_by_id, embodiment_by_id


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            yield str(key)
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def _validate_compatibility_asset(asset: Mapping[str, Any]) -> None:
    _require_exact_keys(
        asset,
        {
            "schema",
            "reviewed_at",
            "candidate_asset_sha256",
            "semantic_bindings_asset_sha256",
            "predicate_contract",
            "predicate_kind_ids",
            "resource_kind_ids",
            "slot_ids",
            "slot_state_contract",
            "facet_resolution_order",
            "event_spine_contract",
            "event_spine_templates",
            "solver",
            "budgets",
            "resource_policy",
            "distance_policy",
            "bridge_policy",
            "decision_outcomes",
            "decision_reason_code_ids",
            "universal_rules",
            "guard_candidate_ids",
            "router_candidate_ids",
            "metric_candidate_ids",
            "exception_rules",
            "counts",
        },
        "compatibility_asset",
        AssetValidationError,
    )
    if asset["schema"] != COMPATIBILITY_SCHEMA:
        raise AssetValidationError(f"compatibility_asset.schema must be {COMPATIBILITY_SCHEMA}")
    _require_nonempty_string(asset["reviewed_at"], "compatibility_asset.reviewed_at", AssetValidationError)
    if not _is_sha256(asset["candidate_asset_sha256"]):
        raise AssetValidationError("compatibility_asset.candidate_asset_sha256 is invalid")
    if not _is_sha256(asset["semantic_bindings_asset_sha256"]):
        raise AssetValidationError("compatibility_asset.semantic_bindings_asset_sha256 is invalid")
    forbidden_matrix_keys = {"pair_matrix", "compatibility_matrix", "all_pairs", "pairwise_edges"}
    present_forbidden = set(_walk_keys(asset)) & forbidden_matrix_keys
    if present_forbidden:
        raise AssetValidationError(f"compatibility asset contains forbidden all-pairs fields: {sorted(present_forbidden)}")

    predicate_contract = _require_mapping(asset["predicate_contract"], "compatibility.predicate_contract", AssetValidationError)
    _require_exact_keys(predicate_contract, {"shape", "negation_location", "arbitrary_expression_evaluation"}, "compatibility.predicate_contract", AssetValidationError)
    if predicate_contract["shape"] != ["kind", "subject", "value"] or predicate_contract["negation_location"] != "forbids_any_only" or predicate_contract["arbitrary_expression_evaluation"] != "forbidden":
        raise AssetValidationError("compatibility predicate contract has drifted")
    predicate_kinds = _require_string_list(asset["predicate_kind_ids"], "compatibility.predicate_kind_ids", AssetValidationError, allow_empty=False)
    if set(predicate_kinds) != SUPPORTED_PREDICATE_KINDS:
        raise AssetValidationError("compatibility predicate kinds must equal the runtime closed enum")
    resource_kinds = _require_string_list(asset["resource_kind_ids"], "compatibility.resource_kind_ids", AssetValidationError, allow_empty=False)
    required_resources = {
        "manipulator", "attention_channel", "head_orientation", "support_contact", "mouth", "appendage", "locomotor_contact",
        "focal_primary", "focal_secondary", "foreground_salience", "event_peak", "prop_slot",
    }
    if not required_resources <= set(resource_kinds) or set(resource_kinds) - (ENTITY_RESOURCE_KINDS | SCENE_RESOURCE_KINDS):
        raise AssetValidationError("compatibility resource kinds are missing required resources or contain an unknown kind")
    expected_solver_slots = [facet for facet in FACET_IDS if facet not in {"bridge", "salience"}]
    if asset["slot_ids"] != expected_solver_slots:
        raise AssetValidationError("compatibility slot_ids have drifted")

    slot_contract = _require_mapping(asset["slot_state_contract"], "compatibility.slot_state_contract", AssetValidationError)
    _require_exact_keys(slot_contract, {"enum", "fixed", "closed", "open", "precedence"}, "compatibility.slot_state_contract", AssetValidationError)
    if slot_contract["enum"] != ["fixed", "closed", "open"] or slot_contract["precedence"] != ["fixed", "closed", "open"]:
        raise AssetValidationError("compatibility slot-state enum or precedence has drifted")
    for state in ("fixed", "closed", "open"):
        _require_nonempty_string(slot_contract[state], f"compatibility.slot_state_contract.{state}", AssetValidationError)
    if asset["facet_resolution_order"] != [
        "action", "phase", "relation", "contact", "pose", "attention", "expression", "perceived_affect", "gesture", "prop", "prop_state", "environment", "consequence", "bridge", "salience"
    ]:
        raise AssetValidationError("compatibility facet resolution order has drifted")

    spine = _require_mapping(asset["event_spine_contract"], "compatibility.event_spine_contract", AssetValidationError)
    _require_exact_keys(spine, {"root_count", "required_role_ids", "optional_role_ids", "phase_count", "second_independent_premise", "orphan_atom"}, "compatibility.event_spine_contract", AssetValidationError)
    if spine["root_count"] != 1 or spine["phase_count"] != 1 or spine["required_role_ids"] != ["actor", "action"] or spine["second_independent_premise"] != "block" or spine["orphan_atom"] != "block":
        raise AssetValidationError("compatibility one-event contract has weakened")
    optional_roles = _require_string_list(spine["optional_role_ids"], "compatibility.event_spine_contract.optional_role_ids", AssetValidationError)
    if set(optional_roles) != {"target", "instrument", "recipient", "result", "location"}:
        raise AssetValidationError("compatibility optional event roles have drifted")
    templates = _require_list(asset["event_spine_templates"], "compatibility.event_spine_templates", AssetValidationError)
    template_ids: set[str] = set()
    for index, raw_template in enumerate(templates):
        where = f"compatibility.event_spine_templates[{index}]"
        template = _require_mapping(raw_template, where, AssetValidationError)
        _require_exact_keys(template, {"id", "required_roles", "optional_roles", "forbidden_roles"}, where, AssetValidationError)
        template_id = _require_nonempty_string(template["id"], f"{where}.id", AssetValidationError)
        if template_id in template_ids:
            raise AssetValidationError(f"duplicate event template: {template_id}")
        template_ids.add(template_id)
        for key in ("required_roles", "optional_roles", "forbidden_roles"):
            roles = _require_string_list(template[key], f"{where}.{key}", AssetValidationError)
            if set(roles) - set(EVENT_ROLE_IDS):
                raise AssetValidationError(f"{where}.{key} contains an unknown role")

    solver = _require_mapping(asset["solver"], "compatibility.solver", AssetValidationError)
    _require_exact_keys(
        solver,
        {"selection_mode", "beam_width", "max_candidates_per_facet_before_beam", "catalog_order", "ranking_order", "seed_is_final_tiebreak_only"},
        "compatibility.solver",
        AssetValidationError,
    )
    if solver["selection_mode"] != "predicate_beam_v1" or solver["beam_width"] != 8 or solver["max_candidates_per_facet_before_beam"] != 3 or solver["catalog_order"] != "candidate_id_ascending" or solver["seed_is_final_tiebreak_only"] is not True:
        raise AssetValidationError("compatibility solver policy has drifted")
    ranking = _require_string_list(solver["ranking_order"], "compatibility.solver.ranking_order", AssetValidationError, allow_empty=False)
    if ranking[-1] != "seed_digest" or "hard_gate_pass" not in ranking:
        raise AssetValidationError("compatibility ranking must keep seed as final tie-break")

    budgets = _require_mapping(asset["budgets"], "compatibility.budgets", AssetValidationError)
    expected_budgets = {
        "event_spines": 1,
        "primary_actions": 1,
        "phases": 1,
        "pose_support_solutions": 1,
        "display_bundles": 1,
        "display_primitives_per_bundle": 2,
        "perceived_affect_hypotheses": 1,
        "gestures": 1,
        "optional_props": 1,
        "relation_topologies": 1,
        "primary_environment_roles": 1,
        "remote_or_high_load_optional_premises": 1,
        "second_independent_premises": 0,
        "orphan_atoms": 0,
    }
    if dict(budgets) != expected_budgets:
        raise AssetValidationError("compatibility fixed budgets have drifted")

    resource_policy = _require_mapping(asset["resource_policy"], "compatibility.resource_policy", AssetValidationError)
    _require_exact_keys(resource_policy, {"scope", "capacity_check", "same_phase_double_booking", "shared_attention_exception", "repair_order"}, "compatibility.resource_policy", AssetValidationError)
    if resource_policy["scope"] != "entity_or_scene" or resource_policy["capacity_check"] != "sum_exclusive_claims_lte_capacity" or resource_policy["same_phase_double_booking"] != "block":
        raise AssetValidationError("compatibility resource policy has weakened")
    _require_string_list(resource_policy["repair_order"], "compatibility.resource_policy.repair_order", AssetValidationError)

    distance = _require_mapping(asset["distance_policy"], "compatibility.distance_policy", AssetValidationError)
    _require_exact_keys(distance, {"axis_ids", "value_type", "band_rules", "creativity_bands", "creativity_changes", "creativity_never_changes"}, "compatibility.distance_policy", AssetValidationError)
    if distance["axis_ids"] != list(DISTANCE_AXIS_IDS) or distance["value_type"] != "ordinal_0_3":
        raise AssetValidationError("compatibility distance axes have drifted")
    rules = _require_list(distance["band_rules"], "compatibility.distance_policy.band_rules", AssetValidationError)
    if [rule.get("band") if isinstance(rule, Mapping) else None for rule in rules] != ["far", "middle", "near"]:
        raise AssetValidationError("compatibility distance band rule order has drifted")
    creativity_bands = _require_list(distance["creativity_bands"], "compatibility.distance_policy.creativity_bands", AssetValidationError)
    expected_ranges = {
        "low": (0.0, True, 0.25, False, "near"),
        "middle": (0.25, True, 0.75, False, "middle"),
        "high": (0.75, True, 1.0, True, "far"),
    }
    for index, raw_band in enumerate(creativity_bands):
        where = f"compatibility.distance_policy.creativity_bands[{index}]"
        band = _require_mapping(raw_band, where, AssetValidationError)
        _require_exact_keys(band, {"id", "lower", "lower_inclusive", "upper", "upper_inclusive", "target_band", "eligible_distance_weights"}, where, AssetValidationError)
        expected = expected_ranges.get(band["id"])
        actual = (band["lower"], band["lower_inclusive"], band["upper"], band["upper_inclusive"], band["target_band"])
        if expected is None or actual != expected:
            raise AssetValidationError(f"{where} does not implement exact creativity thresholds")
        weights = _require_mapping(band["eligible_distance_weights"], f"{where}.eligible_distance_weights", AssetValidationError)
        _require_exact_keys(weights, {"near", "middle", "far"}, f"{where}.eligible_distance_weights", AssetValidationError)
        if band["id"] == "low" and not (weights["near"] > weights["middle"] > weights["far"] > 0):
            raise AssetValidationError("low creativity must rank near first without changing eligibility")
        if band["id"] == "middle" and not (weights["middle"] > weights["near"] > 0 and weights["far"] > 0):
            raise AssetValidationError("middle creativity must rank middle first without excluding far")
        if band["id"] == "high" and not (weights["far"] > weights["middle"] > weights["near"] > 0):
            raise AssetValidationError("high creativity must prefer far")
    if [item.get("id") for item in creativity_bands if isinstance(item, Mapping)] != ["low", "middle", "high"]:
        raise AssetValidationError("creativity bands must remain in low/middle/high order")
    if distance["creativity_changes"] != ["eligible_distance_band_weight"]:
        raise AssetValidationError("creativity may change only distance-band weighting")
    never_changes = set(_require_string_list(distance["creativity_never_changes"], "compatibility.distance_policy.creativity_never_changes", AssetValidationError))
    if not {"identity", "fixed_or_closed_slots", "feasibility", "resource_capacity", "policy", "candidate_count", "event_spine_count"} <= never_changes:
        raise AssetValidationError("creativity hard-gate invariants are incomplete")

    bridge = _require_mapping(asset["bridge_policy"], "compatibility.bridge_policy", AssetValidationError)
    _require_exact_keys(
        bridge,
        {"bridge_type_ids", "category_members", "near_minimum", "near_direct_event_edge_required", "middle_minimum", "middle_required_categories", "far_minimum", "far_required_categories", "far_visible_core_identity_anchor_required", "bridge_requires_pixel_evidence", "explanation_only_bridge"},
        "compatibility.bridge_policy",
        AssetValidationError,
    )
    if set(bridge["bridge_type_ids"]) != set(ENTRY_BRIDGE_TYPES + MEDIATION_BRIDGE_TYPES + EXIT_BRIDGE_TYPES) or len(bridge["bridge_type_ids"]) != 7:
        raise AssetValidationError("compatibility bridge type enum has drifted")
    if set(bridge["bridge_type_ids"]) != set(_BRIDGE_NATURAL_LEXEME_GROUPS):
        raise AssetValidationError(
            "compatibility bridge types must exactly match the closed natural carrier mapping"
        )
    categories = _require_mapping(bridge["category_members"], "compatibility.bridge_policy.category_members", AssetValidationError)
    expected_categories = {"entry": list(ENTRY_BRIDGE_TYPES), "mediation": list(MEDIATION_BRIDGE_TYPES), "exit": list(EXIT_BRIDGE_TYPES)}
    if dict(categories) != expected_categories:
        raise AssetValidationError("compatibility bridge categories have drifted")
    if bridge["near_minimum"] != 1 or bridge["near_direct_event_edge_required"] is not True or bridge["middle_minimum"] != 2 or bridge["middle_required_categories"] != ["entry", "exit"] or bridge["far_minimum"] != 3 or bridge["far_required_categories"] != ["entry", "mediation", "exit"] or bridge["far_visible_core_identity_anchor_required"] is not True or bridge["bridge_requires_pixel_evidence"] is not True or bridge["explanation_only_bridge"] != "block":
        raise AssetValidationError("compatibility bridge policy has weakened")

    decisions = _require_mapping(asset["decision_outcomes"], "compatibility.decision_outcomes", AssetValidationError)
    _require_exact_keys(decisions, {"allow", "allow_with_bridge", "repair", "block", "order"}, "compatibility.decision_outcomes", AssetValidationError)
    if decisions["order"] != ["block", "repair", "allow_with_bridge", "allow"]:
        raise AssetValidationError("compatibility decision precedence has drifted")
    for key in ("allow", "allow_with_bridge", "repair", "block"):
        _require_nonempty_string(decisions[key], f"compatibility.decision_outcomes.{key}", AssetValidationError)

    decision_reason_code_ids = _require_string_list(
        asset["decision_reason_code_ids"],
        "compatibility.decision_reason_code_ids",
        AssetValidationError,
        allow_empty=False,
    )
    if decision_reason_code_ids != list(DECISION_REASON_CODE_IDS):
        raise AssetValidationError(
            "compatibility.decision_reason_code_ids must equal the frozen runtime registry"
        )

    universal_rules = _require_list(asset["universal_rules"], "compatibility.universal_rules", AssetValidationError)
    rule_ids: set[str] = set()
    for index, raw_rule in enumerate(universal_rules):
        where = f"compatibility.universal_rules[{index}]"
        rule = _require_mapping(raw_rule, where, AssetValidationError)
        _require_exact_keys(
            rule,
            {"id", "when_all", "outcome", "reason_code", "candidate_scope"},
            where,
            AssetValidationError,
        )
        rule_id = _require_nonempty_string(rule["id"], f"{where}.id", AssetValidationError)
        if rule_id in rule_ids:
            raise AssetValidationError(f"duplicate universal rule: {rule_id}")
        rule_ids.add(rule_id)
        _validate_predicate_list(rule["when_all"], f"{where}.when_all")
        if rule["outcome"] not in {"allow", "allow_with_bridge", "repair", "block"}:
            raise AssetValidationError(f"{where}.outcome is invalid")
        if rule["outcome"] == "allow":
            raise AssetValidationError(f"{where}.outcome may not be allow in v1")
        reason_code = _require_nonempty_string(
            rule["reason_code"], f"{where}.reason_code", AssetValidationError
        )
        if reason_code not in decision_reason_code_ids:
            raise AssetValidationError(f"{where}.reason_code is not registered")
        if UNIVERSAL_RULE_REASON_CODE_BY_ID.get(rule_id) != reason_code:
            raise AssetValidationError(f"{where}.reason_code disagrees with the frozen rule mapping")
        _require_nonempty_string(rule["candidate_scope"], f"{where}.candidate_scope", AssetValidationError)
    if rule_ids != set(UNIVERSAL_RULE_REASON_CODE_BY_ID):
        raise AssetValidationError("compatibility universal-rule inventory has drifted")

    for key in ("guard_candidate_ids", "router_candidate_ids", "metric_candidate_ids"):
        _require_string_list(asset[key], f"compatibility.{key}", AssetValidationError)
    exceptions = _require_list(asset["exception_rules"], "compatibility.exception_rules", AssetValidationError)
    exception_ids: set[str] = set()
    seen_candidate_sets: set[tuple[str, ...]] = set()
    for index, raw_exception in enumerate(exceptions):
        where = f"compatibility.exception_rules[{index}]"
        item = _require_mapping(raw_exception, where, AssetValidationError)
        _require_exact_keys(item, {"id", "candidate_ids", "when_all", "outcome", "reason", "provenance_record_ids"}, where, AssetValidationError)
        item_id = _require_nonempty_string(item["id"], f"{where}.id", AssetValidationError)
        if item_id in exception_ids:
            raise AssetValidationError(f"duplicate exception id: {item_id}")
        exception_ids.add(item_id)
        candidate_tuple = tuple(sorted(_require_string_list(item["candidate_ids"], f"{where}.candidate_ids", AssetValidationError, allow_empty=False)))
        if candidate_tuple in seen_candidate_sets:
            raise AssetValidationError("duplicate or reverse-duplicate sparse exception")
        seen_candidate_sets.add(candidate_tuple)
        _validate_predicate_list(item["when_all"], f"{where}.when_all")
        if item["outcome"] not in {"allow", "allow_with_bridge", "repair", "block"}:
            raise AssetValidationError(f"{where}.outcome is invalid")
        _require_nonempty_string(item["reason"], f"{where}.reason", AssetValidationError)
        _require_string_list(item["provenance_record_ids"], f"{where}.provenance_record_ids", AssetValidationError, allow_empty=False)
    counts = _require_mapping(asset["counts"], "compatibility.counts", AssetValidationError)
    expected_counts = {
        "guard_candidates": len(asset["guard_candidate_ids"]),
        "router_candidates": len(asset["router_candidate_ids"]),
        "metric_candidates": len(asset["metric_candidate_ids"]),
        "exception_rules": len(exceptions),
        "pairwise_candidate_edges": 0,
    }
    if dict(counts) != expected_counts:
        raise AssetValidationError(f"compatibility counts mismatch: expected={expected_counts}, actual={dict(counts)}")


def validate_universal_scene_assets(
    candidate_asset: Mapping[str, Any],
    compatibility_asset: Mapping[str, Any],
    *,
    semantic_bindings_asset: Mapping[str, Any] | None = None,
    candidate_path: str | Path | None = None,
    compatibility_path: str | Path | None = None,
    semantic_bindings_path: str | Path | None = None,
    research_manifest: Mapping[str, Any] | None = None,
    research_manifest_path: str | Path | None = None,
) -> UniversalSceneAssets:
    """Validate already decoded assets and return an immutable runtime view."""

    candidate_copy = _deep_canonical_copy(_require_mapping(candidate_asset, "candidate_asset", AssetValidationError))
    compatibility_copy = _deep_canonical_copy(_require_mapping(compatibility_asset, "compatibility_asset", AssetValidationError))
    if semantic_bindings_asset is None:
        if candidate_path is None:
            raise AssetValidationError("semantic_bindings_asset is required for in-memory validation")
        derived_semantic_path = Path(candidate_path).resolve().parent / SEMANTIC_BINDINGS_FILENAME
        semantic_bindings_asset, _ = _load_json_object(derived_semantic_path)
        if semantic_bindings_path is None:
            semantic_bindings_path = derived_semantic_path
    semantic_copy = _deep_canonical_copy(
        _require_mapping(semantic_bindings_asset, "semantic_bindings_asset", AssetValidationError)
    )
    manifest_copy = None if research_manifest is None else _deep_canonical_copy(
        _require_mapping(research_manifest, "research_manifest", AssetValidationError)
    )
    _validate_compatibility_asset(compatibility_copy)
    candidate_by_id, prop_by_id, embodiment_by_id = _validate_candidate_asset(
        candidate_copy, compatibility_copy, manifest_copy
    )
    (
        prop_sense_by_catalog_id,
        capability_assertions_by_id,
        visual_carrier_by_candidate_id,
        resource_carrier_by_kind,
    ) = _validate_semantic_bindings_asset(
        semantic_copy,
        candidate_by_id=candidate_by_id,
        candidate_asset=candidate_copy,
        prop_by_id=prop_by_id,
        compatibility=compatibility_copy,
    )

    candidate_raw = Path(candidate_path).read_bytes() if candidate_path is not None else canonical_json_bytes(candidate_copy)
    compatibility_raw = Path(compatibility_path).read_bytes() if compatibility_path is not None else canonical_json_bytes(compatibility_copy)
    semantic_raw = Path(semantic_bindings_path).read_bytes() if semantic_bindings_path is not None else canonical_json_bytes(semantic_copy)
    candidate_hash = _raw_sha256(candidate_raw)
    compatibility_hash = _raw_sha256(compatibility_raw)
    semantic_hash = _raw_sha256(semantic_raw)
    if candidate_path is not None and compatibility_copy["candidate_asset_sha256"] != candidate_hash:
        raise AssetValidationError("compatibility candidate_asset_sha256 does not match raw candidate bytes")
    if candidate_copy["semantic_bindings_asset_sha256"] != semantic_hash:
        raise AssetValidationError("candidate semantic_bindings_asset_sha256 does not match raw semantic-binding bytes")
    if compatibility_copy["semantic_bindings_asset_sha256"] != semantic_hash:
        raise AssetValidationError("compatibility semantic_bindings_asset_sha256 does not match raw semantic-binding bytes")
    if research_manifest_path is not None:
        manifest_raw = Path(research_manifest_path).read_bytes()
        manifest_hash = _raw_sha256(manifest_raw)
    elif manifest_copy is not None:
        manifest_hash = canonical_sha256(manifest_copy)
    else:
        manifest_hash = candidate_copy["research_manifest_sha256"]
    if candidate_copy["research_manifest_sha256"] != manifest_hash:
        raise AssetValidationError("candidate research_manifest_sha256 does not match manifest bytes")

    role_expectations = {
        "guard_candidate_ids": "guard",
        "router_candidate_ids": "router",
        "metric_candidate_ids": "metric",
    }
    for key, role in role_expectations.items():
        expected_ids = sorted(candidate_id for candidate_id, item in candidate_by_id.items() if item["role"] == role)
        if compatibility_copy[key] != expected_ids:
            raise AssetValidationError(f"compatibility.{key} does not exactly reference catalog {role}s")
    referenced_exception_ids = {
        candidate_id
        for item in compatibility_copy["exception_rules"]
        for candidate_id in item["candidate_ids"]
    }
    if referenced_exception_ids - set(candidate_by_id):
        raise AssetValidationError("compatibility exception references an unknown candidate")

    asset_dir: Path | None = None
    if candidate_path is not None:
        asset_dir = Path(candidate_path).resolve().parent
    hashes = MappingProxyType(
        {
            "universal_candidates_sha256": candidate_hash,
            "universal_compatibility_sha256": compatibility_hash,
            "universal_semantic_bindings_sha256": semantic_hash,
            "universal_research_manifest_sha256": manifest_hash,
        }
    )
    return UniversalSceneAssets(
        asset_dir=asset_dir,
        candidates=MappingProxyType(candidate_copy),
        compatibility=MappingProxyType(compatibility_copy),
        semantic_bindings=MappingProxyType(semantic_copy),
        candidate_by_id=MappingProxyType(candidate_by_id),
        proposal_by_id=MappingProxyType(
            {
                str(profile["id"]): profile
                for profile in candidate_copy["proposal_profiles"]
            }
        ),
        prop_by_id=MappingProxyType(prop_by_id),
        embodiment_by_id=MappingProxyType(embodiment_by_id),
        prop_sense_by_catalog_id=MappingProxyType(prop_sense_by_catalog_id),
        capability_assertions_by_id=MappingProxyType(capability_assertions_by_id),
        visual_carrier_by_candidate_id=MappingProxyType(visual_carrier_by_candidate_id),
        resource_carrier_by_kind=MappingProxyType(resource_carrier_by_kind),
        asset_hashes=hashes,
    )


def load_universal_scene_assets(asset_dir: str | Path | None = None) -> UniversalSceneAssets:
    """Load and strictly validate the four raw-byte-bound universal assets."""

    base = (
        Path(asset_dir).expanduser().resolve()
        if asset_dir is not None
        else (Path(__file__).resolve().parent.parent / "assets")
    )
    candidate_path = base / CANDIDATE_FILENAME
    compatibility_path = base / COMPATIBILITY_FILENAME
    semantic_path = base / SEMANTIC_BINDINGS_FILENAME
    manifest_path = base / RESEARCH_MANIFEST_FILENAME
    candidate, _ = _load_json_object(candidate_path)
    compatibility, _ = _load_json_object(compatibility_path)
    semantic_bindings, _ = _load_json_object(semantic_path)
    manifest, _ = _load_json_object(manifest_path)
    return validate_universal_scene_assets(
        candidate,
        compatibility,
        semantic_bindings_asset=semantic_bindings,
        candidate_path=candidate_path,
        compatibility_path=compatibility_path,
        semantic_bindings_path=semantic_path,
        research_manifest=manifest,
        research_manifest_path=manifest_path,
    )


def _derived_facet_state(
    facet: str,
    validated: ValidatedSceneContract,
) -> str:
    slots = validated.slot_by_id
    roles = validated.role_by_id
    if facet == "expression":
        return str(slots["expression"]["state"])
    if facet == "perceived_affect":
        return "closed" if slots["expression"]["state"] == "closed" else "open"
    if facet == "attention":
        channel_ids = {
            "attention_channel", "head_orientation", "body_orientation", "body_contour_display",
            "internal_luminance_display", "light_emission", "surface_signal", "mobile_ear_pair",
            "wing_axis_pair", "tail_axis", "mechanical_state_displacement",
        }
        relevant = [
            item for item in validated.capability_capacities
            if item["entity_id"] == _actor_entity_id(validated) and item["resource_kind"] in channel_ids
        ]
        if relevant and all(item["state"] == "unavailable" for item in relevant):
            return "closed"
        return "open"
    if facet == "pose":
        return str(slots["pose"]["state"])
    if facet == "gesture":
        return "closed" if slots["pose"]["state"] == "closed" else "open"
    if facet == "action":
        return str(slots["action"]["state"])
    if facet == "phase":
        role_state = str(roles["phase"]["state"])
        if role_state != "open":
            return role_state
        return "closed" if slots["action"]["state"] == "closed" else "open"
    if facet == "relation":
        return str(slots["relation"]["state"])
    if facet == "contact":
        return "closed" if slots["relation"]["state"] == "closed" else "open"
    if facet == "prop":
        return str(slots["prop"]["state"])
    if facet == "prop_state":
        return "closed" if slots["prop"]["state"] == "closed" else "open"
    if facet == "environment":
        return str(slots["environment"]["state"])
    if facet == "consequence":
        if slots["action"]["state"] == "closed" and roles["result"]["state"] != "fixed":
            return "closed"
        return "open"
    if facet in {"bridge", "salience"}:
        return "open"
    raise SelectionError(f"unknown facet state requested: {facet}")


def _available_capabilities(validated: ValidatedSceneContract, entity_id: str) -> dict[str, int]:
    return {
        str(item["resource_kind"]): int(item["capacity"])
        for item in validated.capability_capacities
        if item["entity_id"] == entity_id and item["state"] == "available"
    }


def _actor_entity_id(validated: ValidatedSceneContract) -> str:
    primary = validated.participant_by_role["actor"]["primary_entity_id"]
    if primary is None:
        raise SelectionError("scene contract lacks a primary actor participant")
    return str(primary)


def _actor_role_value(validated: ValidatedSceneContract) -> str:
    actor = validated.role_by_id["actor"]
    if actor["state"] == "fixed":
        return str(actor["value_id"])
    return _actor_entity_id(validated)


def _scene_location_value(validated: ValidatedSceneContract) -> str | None:
    location = validated.role_by_id["location"]
    if location["state"] == "fixed":
        return str(location["value_id"])
    environment = validated.slot_by_id["environment"]
    if environment["state"] == "fixed" and environment["value_ids"]:
        return str(environment["value_ids"][0])
    return None


def _aliases_for_prop(prop: Mapping[str, Any]) -> list[str]:
    return [
        value
        for locale_record in prop["aliases"]
        for value in locale_record["values"]
    ]


def _matched_prop_ids(
    concept: str,
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> set[str]:
    if validated.slot_by_id["prop"]["state"] != "fixed":
        return set()
    # Match the semantic IDs that the literal-bound contract already fixed.
    # Looking at raw aliases alone would collapse distinct senses such as a
    # small wooden mallet into the heavier generic hammer profile.
    haystack_parts: list[str] = list(validated.slot_by_id["prop"]["value_ids"])
    for role_id in ("target", "instrument"):
        value = validated.role_by_id[role_id]["value_id"]
        if isinstance(value, str):
            haystack_parts.append(value)
    # The request bytes are deliberately not searched here.  A prop becomes a
    # catalog prop only through a semantic value already fixed by the literal-
    # bound contract.  Token subsequence matching lets ``small_hammer`` map to
    # hammer without collapsing ``small_wooden_mallet`` into that concept.
    result = _semantic_prop_ids_from_values(haystack_parts, assets)
    literal_phrases = list(validated.slot_by_id["prop"]["request_phrases"])
    for role_id in ("target", "instrument"):
        role = validated.role_by_id[role_id]
        if role["state"] == "fixed":
            literal_phrases.extend(role["request_phrases"])
    for profiles in assets.prop_sense_by_catalog_id.values():
        for profile in profiles:
            if (
                profile["activation_target"] is not None
                and _distinct_prop_sense_matches(profile, literal_phrases, haystack_parts)
            ):
                result.add(str(profile["activation_target"]))
    del concept
    return result


def _initial_roles(validated: ValidatedSceneContract) -> dict[str, dict[str, Any]]:
    roles: dict[str, dict[str, Any]] = {}
    for role_id in EVENT_ROLE_IDS:
        role = validated.role_by_id[role_id]
        if role["state"] == "fixed":
            roles[role_id] = {
                "role_id": role_id,
                "value_id": str(role["value_id"]),
                "source": "user_fixed",
                "source_id": role_id,
            }
    if "actor" not in roles:
        roles["actor"] = {
            "role_id": "actor",
            "value_id": _actor_role_value(validated),
            "source": "runtime_selected",
            "source_id": f"identity_entity:{_actor_entity_id(validated)}",
        }
    return roles


def _predicate_truth(
    predicate: Sequence[str],
    *,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    selected_candidate_ids: set[str],
    provided_predicates: set[tuple[str, str, str]],
    assets: UniversalSceneAssets,
) -> bool:
    kind, subject, value = predicate
    if kind == "slot":
        try:
            state = _derived_facet_state(subject, validated)
        except SelectionError:
            return False
        return state == value or (value == "open_or_fixed" and state in {"open", "fixed"})
    if kind == "event_role":
        if value in {"contract_fixed", "contract_open", "contract_closed"}:
            expected_state = value.removeprefix("contract_")
            return validated.role_by_id.get(subject, {}).get("state") == expected_state
        if value == "present":
            return subject in roles and bool(roles[subject].get("value_id"))
        if value == "explicit_none":
            return validated.role_by_id.get(subject, {}).get("state") == "closed"
        return subject in roles and roles[subject].get("value_id") == value
    if kind == "capability":
        if subject != "actor":
            return False
        capacities = _available_capabilities(validated, _actor_entity_id(validated))
        if value == "manipulator_or_equivalent":
            equivalents = {
                "manipulator", "mouth", "appendage", "wing_appendage", "tail_axis",
                "body_orientation", "support_contact", "external_anchor",
            }
            return any(capacities.get(item, 0) > 0 for item in equivalents)
        if value == "nonhuman_display_channel":
            channels = {
                "appendage", "wing_appendage", "body_orientation", "body_contour_display",
                "surface_signal", "light_emission", "internal_luminance_display", "mobile_ear_pair",
                "wing_axis_pair", "tail_axis", "mechanical_state_displacement",
            }
            return any(capacities.get(item, 0) > 0 for item in channels)
        if value == "manipulator_capacity_gte_4":
            return capacities.get("manipulator", 0) >= 4
        if value.endswith("_unavailable"):
            capability_id = value.removesuffix("_unavailable")
            return any(
                item["resource_kind"] == capability_id
                and item["state"] == "unavailable"
                and int(item["capacity"]) == 0
                for item in validated.capability_capacities
                if item["entity_id"] == _actor_entity_id(validated)
            )
        return capacities.get(value, 0) > 0
    if kind == "normalized_prop_concept":
        return value in matched_prop_ids
    if kind == "context":
        context = validated.contract["context_profile"]
        if subject == "identity_core":
            return value == "available"
        if subject == "social" and value == "dyad_or_ensemble":
            return context["social"] in {"dyad", "ensemble"}
        if subject in {"era_technology", "tone", "violence", "scale"}:
            if context.get(subject) != value:
                return False
            profile = next(
                (
                    profile
                    for profile in assets.semantic_bindings["context_literal_profiles"]
                    if profile["field"] == subject and profile["value"] == value
                ),
                None,
            )
            return profile is not None and _context_literal_profile_matches(
                profile, validated.request_text, assets
            )
        if subject == "tool_state" and value == "safe_inactive":
            violence_value = str(context["violence"])
            profile = next(
                (
                    profile
                    for profile in assets.semantic_bindings["context_literal_profiles"]
                    if profile["field"] == "violence"
                    and profile["value"] == violence_value
                ),
                None,
            )
            return (
                violence_value in {"closed", "nonviolent"}
                and profile is not None
                and _context_literal_profile_matches(
                    profile, validated.request_text, assets
                )
            )
        if subject == "weapon_state" and value == "decommissioned_or_other_policy_eligible":
            era_profile = next(
                (
                    profile
                    for profile in assets.semantic_bindings["context_literal_profiles"]
                    if profile["field"] == "era_technology"
                    and profile["value"] == "decommissioned_firearm"
                ),
                None,
            )
            return (
                "prop_decommissioned_machine_gun" in matched_prop_ids
                and context["violence"] != "active"
                and context["era_technology"] == "decommissioned_firearm"
                and era_profile is not None
                and _context_literal_profile_matches(
                    era_profile, validated.request_text, assets
                )
            )
        return context.get(subject) == value
    if kind == "policy":
        # Local default metadata only.  A downstream generation platform stays
        # authoritative and may refuse; the unchanged-prompt retry contract is
        # applied by the generation layer, not asserted here as clearance.
        return subject == "local_default_metadata" and value == "automatic_pass"
    if kind == "cardinality" and subject == "actors" and value == "at_least_2":
        return sum(int(entity["quantity"]) for entity in validated.contract["identity_core"]["entities"]) >= 2
    if kind == "candidate":
        if subject == "selected" and value == "true":
            return bool(selected_candidate_ids)
        return subject in selected_candidate_ids and value == "selected"
    if kind == "facet_evidence":
        return (kind, subject, value) in provided_predicates
    if kind == "guard_contract":
        return value == "satisfied" and subject in assets.compatibility["guard_candidate_ids"]
    if kind == "resource_available":
        return value != "false"
    if kind == "visible_evidence":
        return value == "present"
    if kind == "bridge":
        return any(item[0] == kind and item[1] == subject and item[2] == value for item in provided_predicates)
    if kind == "rule":
        return (kind, subject, value) in provided_predicates
    if kind == "candidate_tag":
        return False
    if kind in {"axis_max", "axis_sum"}:
        return False
    return False


def _predicate_set_passes(
    requires_all: Sequence[Sequence[str]],
    requires_any: Sequence[Sequence[Sequence[str]]],
    forbids_any: Sequence[Sequence[str]],
    **context: Any,
) -> bool:
    if not all(_predicate_truth(item, **context) for item in requires_all):
        return False
    if any(not any(_predicate_truth(item, **context) for item in group) for group in requires_any):
        return False
    if any(_predicate_truth(item, **context) for item in forbids_any):
        return False
    return True


def _proposal_eligibility_decision(
    profile: Mapping[str, Any],
    *,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
    mandatory_candidate_ids: set[str] | None = None,
) -> tuple[bool, str]:
    if not (
        _derived_facet_state("prop", validated) == "open"
        and _derived_facet_state("action", validated) == "open"
    ):
        return False, "proposal_path_not_open"
    if _derived_facet_state(str(profile["slot_id"]), validated) not in profile["eligible_slot_states"]:
        return False, "slot_state_ineligible"
    context = {
        "validated": validated,
        "roles": roles,
        "matched_prop_ids": matched_prop_ids,
        "selected_candidate_ids": set(),
        "provided_predicates": set(),
        "assets": assets,
    }
    if not all(_predicate_truth(item, **context) for item in profile["requires_all"]):
        return False, "requires_all_unsatisfied"
    if any(_predicate_truth(item, **context) for item in profile["forbids_any"]):
        return False, "forbidden_predicate_satisfied"
    if (
        mandatory_candidate_ids is not None
        and str(profile["candidate_ids"][0]) in mandatory_candidate_ids
    ):
        return False, "precondition_unsatisfied"
    if profile["policy_mode"] == "explicit_weapon_only":
        return False, "policy_explicit_only"
    if profile["policy_mode"] == "safe_tool" and validated.contract["context_profile"]["violence"] == "active":
        return False, "policy_active_violence"

    resolved_proposals: dict[str, str | None] = {}
    for role_id, proposed in profile["event_roles"].items():
        if proposed is None:
            continue
        resolved: str | None = str(proposed)
        if proposed == "$identity_actor":
            resolved = _actor_role_value(validated)
        elif proposed == "$scene_location":
            resolved = _scene_location_value(validated)
        if resolved is None:
            continue
        resolved_proposals[str(role_id)] = resolved
    if any(
        (existing := roles.get(role_id)) is not None
        and existing["source"] == "user_fixed"
        and existing["value_id"] != proposed
        for role_id, proposed in resolved_proposals.items()
    ):
        return False, "fixed_role_conflict"
    if any(
        validated.role_by_id[role_id]["state"] == "closed"
        for role_id in resolved_proposals
    ):
        return False, "closed_role_conflict"
    return True, "eligible"


def _proposal_is_eligible(
    profile: Mapping[str, Any],
    *,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
) -> bool:
    eligible, _ = _proposal_eligibility_decision(
        profile,
        validated=validated,
        roles=roles,
        matched_prop_ids=matched_prop_ids,
        assets=assets,
        mandatory_candidate_ids=None,
    )
    return eligible


def _apply_proposal_roles(
    profile: Mapping[str, Any],
    roles: dict[str, dict[str, Any]],
    validated: ValidatedSceneContract,
) -> None:
    for role_id in EVENT_ROLE_IDS:
        proposed = profile["event_roles"][role_id]
        if proposed is None:
            continue
        if proposed == "$identity_actor":
            proposed = _actor_role_value(validated)
        elif proposed == "$scene_location":
            proposed = _scene_location_value(validated)
            if proposed is None:
                continue
        if role_id in roles:
            if roles[role_id]["source"] == "user_fixed" and roles[role_id]["value_id"] != proposed:
                raise SelectionError(f"proposal {profile['id']} conflicts with fixed event role {role_id}")
            continue
        if validated.role_by_id[role_id]["state"] == "closed":
            raise SelectionError(f"proposal {profile['id']} enters closed event role {role_id}")
        roles[role_id] = {
            "role_id": role_id,
            "value_id": proposed,
            "source": "runtime_selected",
            "source_id": f"proposal:{profile['id']}",
        }


def _candidate_is_eligible(
    candidate: Mapping[str, Any],
    *,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    selected_candidate_ids: set[str],
    provided_predicates: set[tuple[str, str, str]],
    assets: UniversalSceneAssets,
) -> tuple[bool, str]:
    if candidate["role"] != "visual_atom":
        return False, "nonvisual_candidate"
    facet = str(candidate["facet"])
    state = _derived_facet_state(facet, validated)
    realization_profiles = _matching_literal_visual_realization_profiles(
        candidate, validated, assets
    )
    if state == "closed":
        return False, f"closed_facet:{facet}"
    if (
        facet == "perceived_affect"
        and validated.slot_by_id["expression"]["state"] == "fixed"
        and not realization_profiles
    ):
        return False, "fixed_facet:perceived_affect"
    if state == "fixed":
        catalog_prop_owner_ids = {
            str(prop_id)
            for prop_id, prop in assets.prop_by_id.items()
            if candidate["id"] in prop["affordance_candidate_ids"]
        }
        fixed_prop_match = facet == "prop" and (
            bool(catalog_prop_owner_ids & matched_prop_ids)
            or not catalog_prop_owner_ids
        )
        if not fixed_prop_match and not realization_profiles:
            return False, f"fixed_facet:{facet}"
    predicate_roles = roles
    if (
        facet == "phase"
        and "phase" not in roles
        and validated.role_by_id["phase"]["state"] == "open"
        and ["phase", "required"] in candidate["runtime_contract"]["bindings"]
    ):
        # An open phase role is resolved by the selected phase carrier itself.
        # Evaluate that carrier against a candidate-scoped provisional role;
        # fixed and closed phase roles never enter this self-provision path.
        predicate_roles = {
            **roles,
            "phase": {
                "role_id": "phase",
                "value_id": str(candidate["id"]),
                "source": "runtime_selected",
                "source_id": f"candidate:{candidate['id']}",
            },
        }
    context = {
        "validated": validated,
        "roles": predicate_roles,
        "matched_prop_ids": matched_prop_ids,
        "selected_candidate_ids": selected_candidate_ids,
        "provided_predicates": provided_predicates,
        "assets": assets,
    }
    unsatisfied_triggers = [
        item for item in candidate["triggers"] if not _predicate_truth(item, **context)
    ]
    if unsatisfied_triggers and not (
        realization_profiles
        and all(
            item[0] == "slot" and item[2] in {"open", "open_or_fixed"}
            for item in unsatisfied_triggers
        )
    ):
        return False, "trigger_unsatisfied"
    pre = candidate["preconditions"]
    if not _predicate_set_passes(
        pre["requires_all"], pre["requires_any"], pre["forbids_any"], **context
    ):
        return False, "precondition_unsatisfied"
    capabilities = candidate["capabilities"]
    if not _predicate_set_passes(
        capabilities["requires_all"], capabilities["requires_any"], [], **context
    ):
        return False, "capability_unsatisfied"
    return True, "eligible"


def _candidate_parameters(candidate: Mapping[str, Any]) -> dict[str, str]:
    return {
        str(parameter_id): sorted(str(value) for value in values)[0]
        for parameter_id, values in sorted(candidate["parameters"].items())
    }


def _entry_parameters_for_candidate(
    candidate: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> dict[str, Any]:
    profiles = _matching_literal_visual_realization_profiles(
        candidate, validated, assets
    )
    if profiles:
        return _literal_realization_parameters(profiles[0], validated, assets)
    return _candidate_parameters(candidate)


def _candidate_rank(
    candidate: Mapping[str, Any],
    *,
    target_band: str,
    prior_exposure_ids: set[str],
    digest_prefix: str,
) -> tuple[Any, ...]:
    band_index = {"near": 0, "middle": 1, "far": 2}
    vector = candidate["runtime_contract"]["distance_profile"]["base"]
    band = _distance_band(vector)
    load = candidate["runtime_contract"]["load_profile"]
    digest = hashlib.sha256(f"{digest_prefix}|{candidate['id']}".encode("utf-8")).hexdigest()
    return (
        abs(band_index[band] - band_index[target_band]),
        len(candidate["runtime_contract"]["bridge_types"]),
        int(load["theme_displacement"]),
        max(0, int(load["visual_salience"]) - int(candidate["runtime_contract"]["salience"]["displacement_cap"])),
        int(load["physical"]),
        1 if candidate["id"] in prior_exposure_ids else 0,
        digest,
        str(candidate["id"]),
    )


def _resource_capacities(validated: ValidatedSceneContract) -> dict[tuple[str, str], int]:
    result = {
        (str(item["entity_id"]), str(item["resource_kind"])): int(item["capacity"])
        for item in validated.capability_capacities
        if item["state"] == "available"
    }
    for kind in SCENE_RESOURCE_KINDS:
        result[("scene", kind)] = 1
    return result


def _resolved_claim_tuples(
    claim: Sequence[Any],
    validated: ValidatedSceneContract,
    resolved_owner_refs: Sequence[Mapping[str, Any]] = (),
) -> tuple[tuple[str, str, int, str], ...]:
    kind, owner_scope, amount, mode = claim
    if owner_scope == "scene":
        owner_ids = ["scene"]
    else:
        profile_owner_ids = [
            str(item["entity_id"])
            for item in resolved_owner_refs
            if item["role_id"] == owner_scope
        ]
        if profile_owner_ids:
            owner_ids = profile_owner_ids
        else:
            participant = validated.participant_by_role.get(str(owner_scope))
            if participant is not None and participant["primary_entity_id"] is not None:
                owner_ids = [str(participant["primary_entity_id"])]
            else:
                # A semantic role without an identity participant remains a
                # typed role node; it is never reassigned to the first entity.
                owner_ids = [str(owner_scope)]
    return tuple(
        (str(kind), owner_id, int(amount), str(mode))
        for owner_id in owner_ids
    )


def _claims_fit(
    selected: Sequence[Mapping[str, Any]],
    validated: ValidatedSceneContract,
) -> bool:
    capacities = _resource_capacities(validated)
    exclusive: dict[tuple[str, str], int] = {}
    shared: dict[tuple[str, str], int] = {}
    for entry in selected:
        candidate = entry["candidate"]
        owner_refs = entry.get("parameters", {}).get("resolved_owner_refs", [])
        for raw_claim in candidate["runtime_contract"]["resource_claims"]:
            for kind, owner_id, amount, mode in _resolved_claim_tuples(
                raw_claim, validated, owner_refs
            ):
                key = (owner_id, kind)
                if key not in capacities:
                    return False
                if mode == "exclusive":
                    exclusive[key] = exclusive.get(key, 0) + amount
                else:
                    # Shared claims consume the maximum per exact participant.
                    shared[key] = max(shared.get(key, 0), amount)
    for key in set(exclusive) | set(shared):
        if exclusive.get(key, 0) + shared.get(key, 0) > capacities.get(key, 0):
            return False
    return True


def _select_catalog_atoms(
    *,
    validated: ValidatedSceneContract,
    roles: dict[str, dict[str, Any]],
    eligibility_roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
    target_band: str,
    seed: int,
    topic_id: str,
    format_id: str,
    prior_exposure_ids: set[str],
    proposal: Mapping[str, Any] | None,
) -> tuple[
    list[dict[str, Any]],
    dict[str, int],
    dict[str, int],
    dict[str, list[str]],
    list[dict[str, str]],
]:
    selected: list[dict[str, Any]] = []
    selected_ids: set[str] = set()
    provided: set[tuple[str, str, str]] = set()
    rejection_counts: dict[str, int] = {}
    eligible_counts: dict[str, int] = {facet: 0 for facet in FACET_IDS}
    eligible_candidate_ids_by_facet: dict[str, list[str]] = {
        facet: [] for facet in FACET_IDS
    }
    candidate_rejections: list[dict[str, str]] = []
    digest_prefix = "|".join(
        [
            assets.asset_hashes["universal_candidates_sha256"],
            validated.request_sha256,
            validated.sha256,
            topic_id,
            format_id,
            target_band,
            str(seed),
        ]
    )

    # Mandatory literal groups are reserved before the common candidate pool
    # or optional proposal is materialized.  Resource claims, provided
    # predicates, facet occupancy, and all later solver choices therefore see
    # the same creativity-invariant contract-owned initial selection.
    selected = _reserve_literal_visual_realization_requirements(
        selected,
        validated=validated,
        roles=roles,
        matched_prop_ids=matched_prop_ids,
        assets=assets,
    )
    if proposal is not None:
        primary_id = str(proposal["candidate_ids"][0])
        if any(str(entry["candidate"]["id"]) == primary_id for entry in selected):
            raise SelectionError(
                f"proposal {proposal['id']} duplicates a mandatory literal realization"
            )
        primary = assets.candidate_by_id[primary_id]
        proposal_entry = {
            "candidate": primary,
            "proposal": proposal,
            "distance_vector": dict(proposal["distance_profile"]),
            "load_vector": dict(proposal["load_profile"]),
            "parameters": {
                "proposal_id": str(proposal["id"]),
                "value_id": str(proposal["value_id"]),
                "prompt_phrase_en": str(proposal["prompt_phrase_en"]),
            },
        }
        if not _claims_fit([*selected, proposal_entry], validated):
            raise SelectionError(
                f"proposal {proposal['id']} conflicts with mandatory resource ownership"
            )
        # Proposal remains the stable first atom for source-role resolution;
        # its insertion occurs only after mandatory feasibility is proven.
        selected.insert(0, proposal_entry)
    selected_ids = {str(entry["candidate"]["id"]) for entry in selected}
    provided = {
        tuple(predicate)
        for entry in selected
        for predicate in entry["candidate"]["postconditions"]
    }

    # The authenticated eligibility partition is a hard-gate projection, not
    # a record of the creativity-selected proposal.  Only contract-owned
    # literal requirements may seed it; optional proposal roles/candidates
    # must not change eligible IDs or rejection reasons across seeds/bands.
    eligibility_entries = [
        entry
        for entry in selected
        if "literal_realization_profile_id" in entry.get("parameters", {})
    ]
    eligibility_selected_ids = {
        str(entry["candidate"]["id"]) for entry in eligibility_entries
    }
    eligibility_provided = {
        tuple(predicate)
        for entry in eligibility_entries
        for predicate in entry["candidate"]["postconditions"]
    }

    pools: dict[str, list[Mapping[str, Any]]] = {facet: [] for facet in FACET_IDS}
    for candidate_id in sorted(assets.candidate_by_id):
        candidate = assets.candidate_by_id[candidate_id]
        eligible, reason = _candidate_is_eligible(
            candidate,
            validated=validated,
            roles=eligibility_roles,
            matched_prop_ids=matched_prop_ids,
            selected_candidate_ids=eligibility_selected_ids,
            provided_predicates=eligibility_provided,
            assets=assets,
        )
        facet = str(candidate["facet"])
        if eligible:
            eligible_counts[facet] += 1
            pools[facet].append(candidate)
            eligible_candidate_ids_by_facet[facet].append(str(candidate_id))
        else:
            rejection_counts[reason] = rejection_counts.get(reason, 0) + 1
            if candidate["role"] == "visual_atom":
                candidate_rejections.append(
                    {"candidate_id": str(candidate_id), "reason_code": str(reason)}
                )

    display_selected = sum(
        str(entry["candidate"]["facet"]) in {"attention", "expression"}
        for entry in selected
    )
    resolution_order = assets.compatibility["facet_resolution_order"]
    for facet in resolution_order:
        if facet in {"bridge", "salience"}:
            continue
        facet_state = _derived_facet_state(facet, validated)
        if proposal is not None and facet in {"action", "phase"} and facet_state == "open":
            continue
        if facet_state not in {"open", "fixed"}:
            continue
        if any(
            str(entry["candidate"]["facet"]) == facet
            and "literal_realization_profile_id" in entry.get("parameters", {})
            for entry in selected
        ):
            continue
        if facet == "prop" and facet_state == "open":
            continue
        should_select = facet_state == "fixed"
        if facet_state == "fixed":
            pass
        elif facet == "action":
            should_select = "action" not in roles
        elif facet == "phase":
            should_select = "phase" not in roles
        elif facet == "pose":
            should_select = True
        elif facet in {"attention", "expression"}:
            should_select = display_selected < 2
        elif facet == "perceived_affect":
            should_select = display_selected > 0
        elif facet == "gesture":
            should_select = any(role_id in roles for role_id in ("target", "recipient"))
        elif facet in {"relation", "contact"}:
            should_select = validated.contract["context_profile"]["social"] in {"dyad", "ensemble"} or "recipient" in roles
        elif facet == "prop_state":
            should_select = proposal is not None or bool(matched_prop_ids)
        elif facet == "environment":
            should_select = validated.slot_by_id["environment"]["state"] == "open"
        elif facet == "consequence":
            should_select = "result" in roles
        if not should_select or not pools[facet]:
            continue
        candidates = sorted(pools[facet], key=lambda item: str(item["id"]))
        candidates = [
            candidate
            for candidate in candidates
            if str(candidate["id"]) not in selected_ids
        ]
        if facet_state == "fixed" and facet == "prop":
            fixed_prop_candidate_ids = {
                candidate_id
                for prop_id in matched_prop_ids
                for candidate_id in assets.prop_by_id[prop_id]["affordance_candidate_ids"]
            }
            candidates = [
                candidate
                for candidate in candidates
                if candidate["id"] in fixed_prop_candidate_ids
            ]
        candidates = candidates[: int(assets.compatibility["solver"]["max_candidates_per_facet_before_beam"])]
        candidates.sort(
            key=lambda item: _candidate_rank(
                item,
                target_band=target_band,
                prior_exposure_ids=prior_exposure_ids,
                digest_prefix=digest_prefix,
            )
        )
        chosen: Mapping[str, Any] | None = None
        for candidate in candidates:
            currently_eligible, _ = _candidate_is_eligible(
                candidate,
                validated=validated,
                roles=roles,
                matched_prop_ids=matched_prop_ids,
                selected_candidate_ids=selected_ids,
                provided_predicates=provided,
                assets=assets,
            )
            if not currently_eligible:
                continue
            trial = selected + [
                {
                    "candidate": candidate,
                    "proposal": None,
                    "distance_vector": dict(candidate["runtime_contract"]["distance_profile"]["base"]),
                    "load_vector": dict(candidate["runtime_contract"]["load_profile"]),
                    "parameters": _entry_parameters_for_candidate(
                        candidate, validated, assets
                    ),
                }
            ]
            if _claims_fit(trial, validated):
                chosen = candidate
                selected = trial
                break
            rejection_counts["resource_capacity"] = rejection_counts.get("resource_capacity", 0) + 1
        if chosen is None:
            continue
        selected_ids.add(str(chosen["id"]))
        for predicate in chosen["postconditions"]:
            provided.add(tuple(predicate))
        if facet in {"attention", "expression"}:
            display_selected += 1
        if facet == "action" and "action" not in roles:
            roles["action"] = {
                "role_id": "action",
                "value_id": str(chosen["id"]),
                "source": "runtime_selected",
                "source_id": f"candidate:{chosen['id']}",
            }
        if facet == "phase" and "phase" not in roles:
            roles["phase"] = {
                "role_id": "phase",
                "value_id": str(chosen["id"]),
                "source": "runtime_selected",
                "source_id": f"candidate:{chosen['id']}",
            }

    if "action" not in roles:
        raise SelectionError("open action slot has no eligible action atom or proposal")
    if "phase" not in roles:
        raise SelectionError("event spine requires exactly one eligible phase")

    anchor = assets.candidate_by_id.get("usl_core_identity_anchor")
    if anchor is not None and all(entry["candidate"]["id"] != anchor["id"] for entry in selected):
        selected.append(
            {
                "candidate": anchor,
                "proposal": None,
                "distance_vector": dict(anchor["runtime_contract"]["distance_profile"]["base"]),
                "load_vector": dict(anchor["runtime_contract"]["load_profile"]),
                "parameters": _candidate_parameters(anchor),
            }
        )
    if not _claims_fit(selected, validated):
        raise SelectionError("selected universal atoms exceed a capability/resource capacity")
    _assert_literal_realization_selection_budgets(selected, validated)
    return (
        selected,
        eligible_counts,
        rejection_counts,
        {
            facet: sorted(candidate_ids)
            for facet, candidate_ids in eligible_candidate_ids_by_facet.items()
        },
        sorted(candidate_rejections, key=lambda item: item["candidate_id"]),
    )


def _assert_literal_realization_selection_budgets(
    entries: Sequence[Mapping[str, Any]],
    validated: ValidatedSceneContract,
) -> None:
    literal_entries = [
        entry
        for entry in entries
        if "literal_realization_profile_id" in entry.get("parameters", {})
    ]
    if len(literal_entries) > MAX_LITERAL_REALIZATION_ATOMS_TOTAL:
        raise SelectionError("literal realization scene budget exceeded")
    if len(entries) > MAX_SELECTED_VISUAL_ATOMS_TOTAL:
        raise SelectionError("selected visual atom budget exceeded")
    resolved_claim_count = sum(
        len(
            _resolved_claim_tuples(
                raw_claim,
                validated,
                entry.get("parameters", {}).get("resolved_owner_refs", []),
            )
        )
        for entry in entries
        for raw_claim in entry["candidate"]["runtime_contract"]["resource_claims"]
    )
    if resolved_claim_count > MAX_SELECTED_RESOURCE_CLAIMS_TOTAL:
        raise SelectionError("selected resource claim budget exceeded")
    literal_facets = {str(entry["candidate"]["facet"]) for entry in literal_entries}
    for facet in literal_facets:
        facet_count = sum(
            str(entry["candidate"]["facet"]) == facet for entry in entries
        )
        if facet_count > MAX_LITERAL_REALIZATION_ATOMS_PER_FACET:
            raise SelectionError(
                f"literal realization facet budget exceeded for {facet}"
            )


def _reserve_literal_visual_realization_requirements(
    selected: list[dict[str, Any]],
    *,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
) -> list[dict[str, Any]]:
    """Solve matched typed realization groups without replacing fixed roles.

    ``eligible`` groups only prove that the common hard-gate pool contains the
    reviewed candidate alternatives.  ``selected`` groups are mandatory:
    ``any`` chooses exactly one feasible candidate and ``all`` materializes the
    complete group.  The closed per-facet/scene budget raises rather than
    truncating, so data drift cannot silently drop a required mechanism.
    """

    result = list(selected)
    selected_ids = {str(entry["candidate"]["id"]) for entry in result}
    provided = {
        tuple(predicate)
        for entry in result
        for predicate in entry["candidate"]["postconditions"]
    }
    profiles = sorted(
        assets.semantic_bindings["literal_visual_realization_profiles"],
        key=lambda item: (int(item["selection_rank"]), str(item["id"])),
    )

    def eligible_candidate(candidate: Mapping[str, Any]) -> tuple[bool, str]:
        return _candidate_is_eligible(
            candidate,
            validated=validated,
            roles=roles,
            matched_prop_ids=matched_prop_ids,
            selected_candidate_ids=selected_ids,
            provided_predicates=provided,
            assets=assets,
        )

    for profile in profiles:
        if not _literal_visual_realization_profile_matches(profile, validated, assets):
            continue
        candidates = [
            assets.candidate_by_id[str(candidate_id)]
            for candidate_id in profile["candidate_group"]
        ]
        eligible = [
            candidate
            for candidate in candidates
            if eligible_candidate(candidate)[0]
        ]
        if profile["quantifier"] == "all":
            eligibility_passes = len(eligible) == len(candidates)
        else:
            eligibility_passes = bool(eligible)
        if not eligibility_passes:
            reasons = {
                str(candidate["id"]): eligible_candidate(candidate)[1]
                for candidate in candidates
            }
            raise SelectionError(
                f"literal realization group {profile['id']} has no complete eligible proof: {reasons}"
            )
        if profile["enforcement"] == "eligible":
            continue
        existing = [
            entry
            for entry in result
            if str(entry["candidate"]["id"]) in set(profile["candidate_group"])
        ]
        if profile["quantifier"] == "any" and len(existing) > 1:
            raise SelectionError(
                f"literal realization group {profile['id']} selected more than one alternative"
            )
        required_candidates = (
            candidates
            if profile["quantifier"] == "all"
            else ([] if existing else eligible[:1])
        )
        for entry in existing:
            if entry.get("proposal") is not None:
                raise SelectionError(
                    f"proposal atom cannot impersonate literal realization {profile['id']}"
                )
            entry["parameters"] = _literal_realization_parameters(profile, validated, assets)
        for candidate in required_candidates:
            if any(
                str(entry["candidate"]["id"]) == str(candidate["id"])
                for entry in result
            ):
                continue
            entry = {
                "candidate": candidate,
                "proposal": None,
                "distance_vector": dict(
                    candidate["runtime_contract"]["distance_profile"]["base"]
                ),
                "load_vector": dict(candidate["runtime_contract"]["load_profile"]),
                "parameters": _literal_realization_parameters(profile, validated, assets),
            }
            if not _claims_fit([*result, entry], validated):
                raise SelectionError(
                    f"literal realization {profile['id']} exceeds a resource capacity"
                )
            result.append(entry)
            selected_ids.add(str(candidate["id"]))
            provided.update(tuple(predicate) for predicate in candidate["postconditions"])
        selected_for_group = [
            entry
            for entry in result
            if str(entry["candidate"]["id"]) in set(profile["candidate_group"])
        ]
        expected_count = len(candidates) if profile["quantifier"] == "all" else 1
        if len(selected_for_group) != expected_count:
            raise SelectionError(
                f"literal realization group {profile['id']} failed its exact selection quantifier"
            )
        _assert_literal_realization_selection_budgets(result, validated)
    return result


def _inject_context_profile_carriers(
    selected: list[dict[str, Any]],
    *,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
) -> list[dict[str, Any]]:
    """Materialize every eligible context overlay on its reviewed atom.

    A profile may never borrow the zero-distance core anchor as a semantic
    carrier.  Eligibility is creativity-invariant and the selected carrier is
    a real visual atom whose evidence remains separately reviewable.
    """

    result = list(selected)
    selected_ids = {str(entry["candidate"]["id"]) for entry in result}
    provided = {
        tuple(predicate)
        for entry in result
        for predicate in entry["candidate"]["postconditions"]
    }
    for profile in sorted(
        assets.candidates["context_distance_profiles"],
        key=lambda item: str(item["id"]),
    ):
        context = {
            "validated": validated,
            "roles": {
                role_id: role
                for role_id, role in roles.items()
                if role.get("value_id") is not None
            },
            "matched_prop_ids": matched_prop_ids,
            "selected_candidate_ids": selected_ids,
            "provided_predicates": provided,
            "assets": assets,
        }
        if not _predicate_set_passes(
            profile["requires_all"],
            profile["requires_any"],
            profile["forbids_any"],
            **context,
        ):
            continue
        policy_mode = profile["policy_mode"]
        if policy_mode == "safe_tool" and validated.contract["context_profile"]["violence"] == "active":
            continue
        if policy_mode == "explicit_weapon_only" and "prop_decommissioned_machine_gun" not in matched_prop_ids:
            continue
        carrier_id = str(profile["carrier_candidate_id"])
        if carrier_id in selected_ids:
            continue
        carrier = assets.candidate_by_id[carrier_id]
        eligible, reason = _candidate_is_eligible(
            carrier,
            validated=validated,
            roles=dict(roles),
            matched_prop_ids=matched_prop_ids,
            selected_candidate_ids=selected_ids,
            provided_predicates=provided,
            assets=assets,
        )
        if not eligible:
            raise SelectionError(
                f"eligible context profile {profile['id']} has ineligible carrier {carrier_id}: {reason}"
            )
        trial = result + [
            {
                "candidate": carrier,
                "proposal": None,
                "distance_vector": dict(carrier["runtime_contract"]["distance_profile"]["base"]),
                "load_vector": dict(carrier["runtime_contract"]["load_profile"]),
                "parameters": _candidate_parameters(carrier),
            }
        ]
        trial_context_carrier_ids = {
            str(entry["candidate"]["id"])
            for entry in trial
            if str(entry["candidate"]["id"])
            in CONTEXT_PROFILE_CARRIER_CANDIDATE_IDS
        }
        if len(trial_context_carrier_ids) > MAX_CONTEXT_PROFILE_CARRIERS:
            raise SelectionError("context profile carrier budget exceeded")
        _assert_literal_realization_selection_budgets(trial, validated)
        if not _claims_fit(trial, validated):
            raise SelectionError(
                f"eligible context profile {profile['id']} carrier exceeds a resource capacity"
            )
        result = trial
        selected_ids.add(carrier_id)
        provided.update(tuple(predicate) for predicate in carrier["postconditions"])
    return result


_BRIDGE_CANDIDATE_BY_TYPE = {
    "affordance": "usc_cbg_affordance_bridge_atom",
    "motivation": "usc_cbg_motivation_bridge_atom",
    "identity_contrast": "usc_cbg_identity_contrast_bridge_atom",
    "mechanics": "usc_cbg_mechanics_bridge_atom",
    "state_change": "usc_cbg_state_change_bridge_atom",
    "consequence": "usc_cbg_consequence_bridge_atom",
}


def _choose_bridge_types(band: str, available: Sequence[str]) -> list[str]:
    """Return every supported bridge in closed semantic/category order.

    Band minima are additive topology requirements, not a reason to discard
    other researched bridge obligations owned by the selected premise.
    """

    available_set = set(available)
    ordered = [
        item
        for item in (*ENTRY_BRIDGE_TYPES, *MEDIATION_BRIDGE_TYPES, *EXIT_BRIDGE_TYPES)
        if item in available_set
    ]
    entry = next((item for item in ENTRY_BRIDGE_TYPES if item in available_set), "affordance")
    if entry not in ordered:
        ordered.insert(0, entry)
    if band in {"middle", "far"} and not set(ordered) & set(EXIT_BRIDGE_TYPES):
        ordered.append("consequence")
    if band == "far" and not set(ordered) & set(MEDIATION_BRIDGE_TYPES):
        first_exit = next(
            (index for index, item in enumerate(ordered) if item in EXIT_BRIDGE_TYPES),
            len(ordered),
        )
        ordered.insert(first_exit, "mechanics")
    return ordered


def _bridge_source_candidate(
    bridge_type: str,
    assets: UniversalSceneAssets,
    fallback_candidate: Mapping[str, Any],
) -> Mapping[str, Any]:
    candidate_id = _BRIDGE_CANDIDATE_BY_TYPE.get(bridge_type)
    if candidate_id is not None and candidate_id in assets.candidate_by_id:
        return assets.candidate_by_id[candidate_id]
    if bridge_type in fallback_candidate["runtime_contract"]["bridge_types"]:
        return fallback_candidate
    raise SelectionError(f"no pixel-grounded bridge candidate for type {bridge_type}")


def _ensure_runtime_role(
    roles: dict[str, dict[str, Any]],
    validated: ValidatedSceneContract,
    role_id: str,
    value_id: str,
    source_id: str,
) -> str:
    if role_id in roles:
        return str(roles[role_id]["value_id"])
    if validated.role_by_id[role_id]["state"] == "closed":
        raise SelectionError(f"bridge requires closed event role {role_id}")
    roles[role_id] = {
        "role_id": role_id,
        "value_id": value_id,
        "source": "runtime_selected",
        "source_id": source_id,
    }
    return value_id


def _scene_capability_records(validated: ValidatedSceneContract) -> list[dict[str, Any]]:
    records = [dict(item) for item in validated.capability_capacities]
    for kind in sorted(SCENE_RESOURCE_KINDS):
        records.append(
            {
                "entity_id": "scene",
                "resource_kind": kind,
                "capacity": 1,
                "state": "available",
                "source": "compatibility_budget",
                "source_fact_id": f"compatibility:{kind}",
            }
        )
    return records


def _fixed_prop_vectors(
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
) -> tuple[list[Mapping[str, int]], list[Mapping[str, int]]]:
    return (
        [assets.prop_by_id[prop_id]["base_distance_profile"] for prop_id in sorted(matched_prop_ids)],
        [assets.prop_by_id[prop_id]["base_load_profile"] for prop_id in sorted(matched_prop_ids)],
    )


_CARRIER_NOISE_TOKENS = {
    "a",
    "action",
    "actor",
    "an",
    "and",
    "are",
    "as",
    "at",
    "atom",
    "be",
    "been",
    "being",
    "both",
    "bridge",
    "by",
    "candidate",
    "cbg",
    "context",
    "detail",
    "dpa",
    "ecs",
    "evidence",
    "event",
    "explicit",
    "facet",
    "fixed",
    "frames",
    "gha",
    "global",
    "id",
    "ofm",
    "of",
    "or",
    "predicate",
    "profile",
    "prop",
    "resource",
    "role",
    "scene",
    "sdc",
    "sptg",
    "state",
    "temporal",
    "the",
    "to",
    "uao",
    "ubp",
    "ugf",
    "use",
    "used",
    "uses",
    "using",
    "usc",
    "ush",
    "usl",
    "visible",
    "visual",
    "with",
    "for",
    "from",
    "has",
    "have",
    "in",
    "into",
    "is",
    "it",
    "its",
    "on",
    "onto",
    "remain",
    "remains",
    "that",
    "their",
    "this",
    "through",
    "under",
    "while",
}

_CARRIER_FALLBACK_SEMANTICS = {
    "actor": "character",
    "action": "motion",
    "target": "focus object",
    "instrument": "tool",
    "recipient": "receiver",
    "result": "outcome",
    "location": "setting",
    "phase": "timing",
    "identity detail": "identity feature",
    "scene evidence": "scene fact",
    "causal bridge": "causal link",
    "resource use": "capacity",
}

_BRIDGE_NATURAL_LEXEME_GROUPS: Mapping[str, tuple[tuple[str, ...], ...]] = MappingProxyType(
    {
        "affordance": (("enables", "allows", "makes possible"),),
        "motivation": (("because of", "drawn by", "responding to"),),
        "mechanics": (("through weight", "through tension", "through balance", "through pressure"),),
        "ownership": (("shared", "handed over", "passed between"),),
        "state_change": (("changes", "shifts", "moves into"),),
        "consequence": (("leaves", "results in", "ends with"),),
        "identity_contrast": (("contrasts with", "set against", "counterpoints"),),
    }
)

_RESOURCE_NATURAL_LEXEME_GROUPS: Mapping[str, tuple[tuple[str, ...], ...]] = MappingProxyType(
    {
        "manipulator": (("hand", "claw", "tendril", "gripper"),),
        "attention_channel": (("gaze", "glance", "focus"),),
        "head_orientation": (("turned head", "tilted head", "facing direction"),),
        "facial_display": (("brow movement", "mouth shape", "eyelid change", "facial expression"),),
        "support_contact": (("brace", "foot", "base", "support"),),
        "mouth": (("mouth", "lips", "jaw", "beak"),),
        "appendage": (("limb", "tail", "tendril", "wing"),),
        "wing_appendage": (("wing", "feathered limb"),),
        "locomotor_contact": (("foot", "paw", "hoof", "wheel"),),
        "body_orientation": (("body turn", "shoulder angle", "torso direction"),),
        "body_contour_display": (("silhouette", "body outline", "contour"),),
        "surface_signal": (("marking", "surface pattern", "color change"),),
        "light_emission": (("glow", "cast light", "radiance"),),
        "internal_luminance_display": (("inner glow", "light beneath skin", "translucent light"),),
        "mobile_ear_pair": (("ear tilt", "turned ears", "ear angle"),),
        "wing_axis_pair": (("wing angle", "spread wings", "folded wings"),),
        "tail_axis": (("tail curve", "tail angle", "tail sweep"),),
        "mechanical_state_displacement": (("hinge shift", "lever motion", "gear turn", "panel movement"),),
        "external_anchor": (("rope", "hook", "rail", "fixed point"),),
        "focal_primary": (("main figure", "central focus", "foreground subject"),),
        "focal_secondary": (("supporting figure", "secondary detail", "background focus"),),
        "foreground_salience": (("foreground detail", "nearest object", "front layer"),),
        "event_peak": (("impact moment", "turning point", "peak action"),),
        "prop_slot": (("object", "item", "tool"),),
    }
)

_ABSENCE_TARGET_NATURAL_LEXEME_GROUPS: Mapping[str, tuple[tuple[str, ...], ...]] = MappingProxyType(
    {
        "manipulator": (("human hand", "grasping hand"),),
        "attention_channel": (("visible attention cue",),),
        "head_orientation": (("visible head turn",),),
        "facial_display": (("visible facial expression",),),
        "support_contact": (("supporting contact",),),
        "mouth": (("mouth",),),
        "appendage": (("limb",),),
        "wing_appendage": (("wing",),),
        "locomotor_contact": (("ground contacting limb",),),
        "body_orientation": (("visible body direction",),),
        "body_contour_display": (("visible body outline",),),
        "surface_signal": (("visible surface marking",),),
        "light_emission": (("emitted light",),),
        "internal_luminance_display": (("inner glow",),),
        "mobile_ear_pair": (("movable ears",),),
        "wing_axis_pair": (("visible wing angle",),),
        "tail_axis": (("visible tail",),),
        "mechanical_state_displacement": (("moving mechanical part",),),
        "external_anchor": (("fixed external attachment",),),
    }
)

_PIXEL_KIND_NATURAL_LEXEME_GROUPS: Mapping[str, tuple[tuple[str, ...], ...]] = MappingProxyType(
    {
        "path": (("path", "line", "alignment", "trajectory"),),
        "contact": (("contact", "touch", "grip", "overlap"),),
        "display": (("facial cue", "body cue", "gaze direction", "visible marking"),),
        "residue": (("dust", "droplet", "fragment", "trace"),),
        "state_boundary": (("before and after", "visible change", "changed position"),),
    }
)

_ATOM_DEFINITION_NOISE_TOKENS = _CARRIER_NOISE_TOKENS | {
    "access",
    "active",
    "affordance",
    "anchor",
    "assign",
    "attributable",
    "back",
    "bearing",
    "bounded",
    "candidate",
    "capacity",
    "channel",
    "clear",
    "coherent",
    "combine",
    "compatible",
    "connects",
    "consequence",
    "control",
    "contract",
    "core",
    "crop",
    "declared",
    "delivery",
    "depicted",
    "direct",
    "displacement",
    "distinct",
    "each",
    "effector",
    "enabling",
    "engineering",
    "every",
    "families",
    "first",
    "fixed",
    "frame",
    "generic",
    "identifies",
    "identity",
    "inspection",
    "instrument",
    "intentionally",
    "internal",
    "least",
    "load",
    "manipulators",
    "manipulator",
    "meaningful",
    "mechanically",
    "mechanics",
    "mechanism",
    "minimum",
    "named",
    "native",
    "one",
    "object",
    "ontology",
    "optional",
    "ownership",
    "pixel",
    "plausible",
    "predicate",
    "premise",
    "profile",
    "readable",
    "reads",
    "region",
    "rendered",
    "rendering",
    "relation",
    "response",
    "runtime",
    "salience",
    "scale",
    "selected",
    "semantic",
    "show",
    "shown",
    "shows",
    "signature",
    "source",
    "specified",
    "specify",
    "second",
    "size",
    "state",
    "subject",
    "such",
    "target",
    "three",
    "thumbnail",
    "topology",
    "two",
    "unambiguous",
    "uniform",
    "vector",
    "vectors",
    "visibly",
    "against",
    "continuous",
    "differs",
    "exits",
    "identifiable",
    "localized",
    "meets",
    "more",
    "points",
    "reaches",
    "regions",
    "separate",
    "terminates",
}


def _carrier_words(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    ascii_words = "".join(
        character if character.isascii() and character.isalnum() else " "
        for character in normalized
    ).split()
    return [
        word
        for word in ascii_words
        if not word.isdigit() and word not in _CARRIER_NOISE_TOKENS
    ]


def _carrier_lexeme_group(
    *semantic_values: str,
    fallback: str,
) -> list[list[str]]:
    groups: list[list[str]] = []
    for semantic_value in semantic_values:
        anchors: list[str] = []
        for word in _carrier_words(semantic_value):
            if word not in anchors:
                anchors.append(word)
        if anchors:
            group = [" ".join(anchors)]
            if group not in groups:
                groups.append(group)
    if not groups:
        fallback_semantics = _CARRIER_FALLBACK_SEMANTICS.get(fallback, fallback)
        fallback_words = _carrier_words(fallback_semantics)
        if fallback_words:
            groups.append([" ".join(dict.fromkeys(fallback_words))])
    if not groups:
        # Closed metadata should always provide a semantic token.  Keep the
        # carrier fail-closed if a future enum consists entirely of connector
        # words instead of silently weakening it to generic "visible evidence".
        raise SelectionError("composition carrier has no substantive English semantic anchor")
    return groups[:2]


def _closed_natural_groups(
    mapping: Mapping[str, tuple[tuple[str, ...], ...]],
    key: str,
    *,
    kind: str,
) -> list[list[str]]:
    groups = mapping.get(key)
    if groups is None:
        raise SelectionError(f"{kind} {key!r} lacks a closed natural-language carrier mapping")
    return [list(group) for group in groups]


def _positive_visual_definition_prefix(value: str) -> str:
    """Discard contrastive negative tails before extracting visible anchors."""

    normalized = unicodedata.normalize("NFKC", value).casefold()
    cut = len(normalized)
    for marker in (
        " rather than ",
        " instead of ",
        " without ",
        " but not ",
        " with no ",
        " from generic ",
    ):
        position = normalized.find(marker)
        if position >= 0:
            cut = min(cut, position)
    return normalized[:cut]


def _atom_visual_carrier_groups(
    atom: Mapping[str, Any],
    assets: UniversalSceneAssets,
) -> list[list[str]]:
    """Load reviewed visual semantics; never infer them from prose or IDs."""

    parameters = atom["parameters"]
    if isinstance(parameters, Mapping) and "proposal_id" in parameters:
        proposal_id = str(parameters["proposal_id"])
        proposal = assets.proposal_by_id.get(proposal_id)
        if proposal is None:
            raise SelectionError(f"selected proposal {proposal_id!r} lacks an asset record")
        return [list(group) for group in proposal["carrier_lexeme_groups"]]

    candidate_id = str(atom["candidate_id"])
    profile = assets.visual_carrier_by_candidate_id.get(candidate_id)
    if profile is None:
        raise SelectionError(f"selected atom {candidate_id!r} lacks an asset-owned visual carrier")
    return [list(group) for group in profile["required_lexeme_groups"]]


def _collapsed_context_group(groups: Sequence[Sequence[str]]) -> list[str] | None:
    terms: list[str] = []
    for group in groups:
        if not group:
            continue
        for word in str(group[0]).split():
            if word not in terms:
                terms.append(word)
    return [" ".join(terms)] if terms else None


def _build_composition_carriers(
    *,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    atoms: Sequence[Mapping[str, Any]],
    bridges: Sequence[Mapping[str, Any]],
    resource_claims: Sequence[Mapping[str, Any]],
    assets: UniversalSceneAssets,
) -> dict[str, Any]:
    identity_items: list[dict[str, Any]] = []
    for entity in validated.contract["identity_core"]["entities"]:
        for fact in entity["feature_facts"]:
            fact_id = str(fact["id"])
            unavailable_capabilities = [
                capability
                for capability in entity["capabilities"]
                if capability["source"] == "explicit"
                and capability["state"] == "unavailable"
                and capability["capacity"] == 0
                and capability["source_fact_id"] == fact_id
            ]
            asserted_absence = bool(unavailable_capabilities)
            fact_groups: list[list[str]] = []
            if asserted_absence:
                for capability in unavailable_capabilities:
                    resource_profile = assets.resource_carrier_by_kind.get(str(capability["id"]))
                    if resource_profile is None:
                        raise SelectionError(
                            f"unavailable capability {capability['id']!r} lacks a semantic carrier"
                        )
                    for group in resource_profile["required_lexeme_groups"]:
                        if group not in fact_groups:
                            fact_groups.append(list(group))
            else:
                fact_groups = _literal_identity_carrier_groups(
                    [str(phrase) for phrase in fact["request_phrases"]],
                    assets,
                )
            identity_items.append(
                {
                    "fact_id": fact_id,
                    "polarity": (
                        "asserted_absence"
                        if asserted_absence
                        else "asserted_presence"
                    ),
                    "required_lexeme_groups": fact_groups,
                }
            )
    for fact_kind in ("scene_facts", "forbidden_facts"):
        for fact in validated.contract["identity_core"][fact_kind]:
            identity_items.append(
                {
                    "fact_id": str(fact["id"]),
                    "polarity": (
                        "forbidden"
                        if fact_kind == "forbidden_facts"
                        else "asserted_presence"
                    ),
                    "required_lexeme_groups": _literal_identity_carrier_groups(
                        [str(phrase) for phrase in fact["request_phrases"]],
                        assets,
                    ),
                }
            )

    fixed_slot_items = [
        {
            "slot_id": str(slot["slot_id"]),
            "value_id": str(binding["value_id"]),
            "required_lexeme_groups": _literal_value_carrier_groups(
                [str(phrase) for phrase in binding["request_phrases"]],
                [str(binding["value_id"])],
                assets,
            ),
        }
        for slot in validated.contract["slot_states"]
        if slot["state"] == "fixed"
        for binding in slot["value_phrase_bindings"]
    ]
    role_items = [
        {
            "role_id": role_id,
            "value_id": str(roles[role_id]["value_id"]),
            "required_lexeme_groups": (
                _literal_value_carrier_groups(
                    [
                        str(phrase)
                        for phrase in validated.role_by_id[role_id]["request_phrases"]
                    ],
                    [str(roles[role_id]["value_id"])],
                    assets,
                )
                if roles[role_id]["source"] == "user_fixed"
                else _carrier_lexeme_group(
                    str(roles[role_id]["value_id"]), fallback=role_id
                )
            ),
        }
        for role_id in EVENT_ROLE_IDS
        if role_id in roles and roles[role_id].get("value_id") is not None
    ]
    atom_items: list[dict[str, Any]] = []
    atom_groups_by_instance: dict[str, list[list[str]]] = {}
    for atom in atoms:
        groups = _atom_visual_carrier_groups(atom, assets)
        instance_id = str(atom["instance_id"])
        atom_groups_by_instance[instance_id] = groups
        atom_items.append(
            {
                "instance_id": instance_id,
                "candidate_id": str(atom["candidate_id"]),
                "required_lexeme_groups": groups,
            }
        )
    bridge_items: list[dict[str, Any]] = []
    for bridge in bridges:
        bridge_groups = _closed_natural_groups(
            _BRIDGE_NATURAL_LEXEME_GROUPS,
            str(bridge["bridge_type"]),
            kind="bridge type",
        )
        contextual_groups = next(
            (
                groups
                for instance_id, groups in atom_groups_by_instance.items()
                if instance_id in str(bridge["bridge_id"])
                or instance_id in {str(bridge["from_node_id"]), str(bridge["to_node_id"])}
            ),
            None,
        )
        if contextual_groups is None:
            bridge_id = str(bridge["bridge_id"])
            fixed_prop_marker = "_fixed_prop_"
            fixed_prop_context = (
                bridge_id.split(fixed_prop_marker, 1)[1]
                if fixed_prop_marker in bridge_id
                else None
            )
            endpoint_groups = (
                [
                    [
                        str(alias)
                        for record in assets.prop_by_id[fixed_prop_context]["aliases"]
                        if record["locale"] == "en"
                        for alias in record["values"]
                    ]
                ]
                if fixed_prop_context is not None
                and fixed_prop_context in assets.prop_by_id
                else _carrier_lexeme_group(
                    str(bridge["from_node_id"]),
                    str(bridge["to_node_id"]),
                    fallback="causal link",
                )
            )
            contextual_groups = endpoint_groups
        collapsed_context = _collapsed_context_group(contextual_groups)
        if collapsed_context is not None and collapsed_context not in bridge_groups:
            bridge_groups.append(collapsed_context)
        bridge_items.append(
            {
                "bridge_id": str(bridge["bridge_id"]),
                "bridge_type": str(bridge["bridge_type"]),
                "required_lexeme_groups": bridge_groups,
            }
        )
    resource_items: list[dict[str, Any]] = []
    for claim in resource_claims:
        if claim["evidence_required"] is not True:
            continue
        resource_profile = assets.resource_carrier_by_kind.get(str(claim["resource_kind"]))
        if resource_profile is None:
            raise SelectionError(
                f"resource kind {claim['resource_kind']!r} lacks an asset-owned natural carrier"
            )
        resource_groups = [
            list(group) for group in resource_profile["required_lexeme_groups"]
        ]
        claimant_context = atom_groups_by_instance.get(str(claim["claimant_id"]))
        collapsed_context = (
            _collapsed_context_group(claimant_context)
            if claimant_context is not None
            else None
        )
        if collapsed_context is not None and collapsed_context not in resource_groups:
            resource_groups.append(collapsed_context)
        resource_items.append(
            {
                "claim_id": str(claim["claim_id"]),
                "resource_kind": str(claim["resource_kind"]),
                "required_lexeme_groups": resource_groups,
            }
        )
    return {
        "schema": COMPOSITION_CARRIERS_SCHEMA,
        "identity_core": identity_items,
        "fixed_slots": fixed_slot_items,
        "event_roles": role_items,
        "atoms": atom_items,
        "bridges": bridge_items,
        "resources": resource_items,
    }


def _semantic_effect_profiles_by_source(
    assets: UniversalSceneAssets,
) -> dict[tuple[str, str], tuple[str, ...]]:
    registry = _require_mapping(
        assets.semantic_bindings["semantic_effect_registry"],
        "semantic_bindings.semantic_effect_registry",
        SelectionError,
    )
    result: dict[tuple[str, str], tuple[str, ...]] = {}
    for raw_profile in _require_list(
        registry["profiles"],
        "semantic_bindings.semantic_effect_registry.profiles",
        SelectionError,
    ):
        profile = _require_mapping(
            raw_profile,
            "semantic_bindings.semantic_effect_registry.profile",
            SelectionError,
        )
        key = (str(profile["source_kind"]), str(profile["source_id"]))
        if key in result:
            raise SelectionError(f"duplicate semantic effect source at runtime: {key}")
        result[key] = tuple(str(item) for item in profile["effect_ids"])
    return result


def _guard_source_contract(candidate: Mapping[str, Any]) -> dict[str, Any]:
    runtime = _require_mapping(
        candidate["runtime_contract"],
        f"guard {candidate['id']}.runtime_contract",
        SelectionError,
    )
    return {
        "guard_id": str(candidate["id"]),
        "role": str(candidate["role"]),
        "research_topic_ids": list(candidate["research_topic_ids"]),
        "provenance_record_ids": list(candidate["provenance_record_ids"]),
        "stage": str(runtime["stage"]),
        "violation_code": str(runtime["violation_code"]),
        "outcome": str(runtime["outcome"]),
    }


def _guard_predicate_result(
    predicate_id: str,
    *,
    selection: Mapping[str, Any],
    assets: UniversalSceneAssets,
    validated: ValidatedSceneContract,
    matched_prop_ids: set[str],
    observed_effect_ids: set[str],
    effect_occurrences: Sequence[Mapping[str, Any]],
) -> tuple[bool, list[str]]:
    event = _require_mapping(selection["selected_event"], "selected_event", SelectionError)
    roles = {
        str(item["role_id"]): item
        for item in _require_list(event["roles"], "selected_event.roles", SelectionError)
    }
    atoms = _require_list(selection["atoms"], "atoms", SelectionError)
    bridges = _require_list(selection["bridges"], "bridges", SelectionError)
    claims = _require_list(selection["resource_claims"], "resource_claims", SelectionError)
    pixels = _require_mapping(
        selection["pixel_evidence_contract"],
        "pixel_evidence_contract",
        SelectionError,
    )
    pixel_items = {
        str(item["item_id"]): item
        for item in _require_list(pixels["items"], "pixel_evidence_contract.items", SelectionError)
    }
    edges = {
        str(item["edge_id"]): item
        for item in _require_list(event["spine_edges"], "selected_event.spine_edges", SelectionError)
    }
    atom_by_id = {str(atom["instance_id"]): atom for atom in atoms}
    candidate_by_atom = {
        str(atom["instance_id"]): assets.candidate_by_id[str(atom["candidate_id"])]
        for atom in atoms
    }
    facet_atoms: dict[str, list[Mapping[str, Any]]] = {}
    for atom in atoms:
        facet_atoms.setdefault(str(atom["facet"]), []).append(atom)
    capacities = _resource_capacities(validated)
    claim_usage: dict[tuple[str, str], tuple[int, int]] = {}
    for claim in claims:
        key = (str(claim["owner_id"]), str(claim["resource_kind"]))
        exclusive, shared = claim_usage.get(key, (0, 0))
        if claim["mode"] == "exclusive":
            exclusive += int(claim["amount"])
        else:
            shared = max(shared, int(claim["amount"]))
        claim_usage[key] = (exclusive, shared)
    capacity_pass = all(
        key in capacities and exclusive + shared <= capacities[key]
        for key, (exclusive, shared) in claim_usage.items()
    )
    atom_edges_pass = all(
        len(atom["event_edge_ids"]) == 1
        and atom["event_edge_ids"][0] in edges
        and edges[atom["event_edge_ids"][0]]["from_node_id"] == "event_01"
        and edges[atom["event_edge_ids"][0]]["to_node_id"] == atom["instance_id"]
        and edges[atom["event_edge_ids"][0]]["relation_id"] == f"realizes:{atom['facet']}"
        for atom in atoms
    )
    bridge_edges_pass = all(
        len(bridge["event_edge_ids"]) == 1
        and bridge["event_edge_ids"][0] in edges
        and edges[bridge["event_edge_ids"][0]]["from_node_id"] == bridge["from_node_id"]
        and edges[bridge["event_edge_ids"][0]]["to_node_id"] == bridge["to_node_id"]
        and edges[bridge["event_edge_ids"][0]]["relation_id"] == f"bridge:{bridge['bridge_type']}"
        for bridge in bridges
    )
    atom_pixels_pass = all(
        atom["pixel_evidence_ids"]
        and all(
            pixel_id in pixel_items
            and pixel_items[pixel_id]["source_kind"] == "atom"
            and pixel_items[pixel_id]["source_id"] == atom["instance_id"]
            for pixel_id in atom["pixel_evidence_ids"]
        )
        for atom in atoms
    )
    bridge_pixels_pass = all(
        bridge["pixel_evidence_ids"]
        and all(
            pixel_id in pixel_items
            and pixel_items[pixel_id]["source_kind"] == "bridge"
            and pixel_items[pixel_id]["source_id"] == bridge["bridge_id"]
            for pixel_id in bridge["pixel_evidence_ids"]
        )
        for bridge in bridges
    )
    blocked_narrative_effects = {
        "combat_opponent_assignment",
        "combat_target_assignment",
        "navigation_instrument_use",
        "romantic_contact",
        "scene_promise_hijack",
    }
    relevant_ids = sorted(
        {
            *(str(atom["instance_id"]) for atom in atoms),
            *(str(bridge["bridge_id"]) for bridge in bridges),
            *(str(claim["claim_id"]) for claim in claims),
        }
    )

    if predicate_id == "single_phase_present":
        phase = roles.get("phase", {}).get("value_id")
        passed = bool(phase) and event["phase_id"] == phase and all(
            claim["phase_id"] == phase for claim in claims
        )
        return passed, [str(phase)] if phase else []
    if predicate_id == "dynamic_action_present":
        action = roles.get("action", {}).get("value_id")
        action_atoms = [
            atom for facet in ("action", "phase", "contact") for atom in facet_atoms.get(facet, [])
        ]
        dynamic_bindings = [
            *(str(atom["instance_id"]) for atom in action_atoms),
            *(str(bridge["bridge_id"]) for bridge in bridges),
        ]
        return bool(action) and bool(dynamic_bindings), [str(action), *dynamic_bindings]
    if predicate_id == "display_cues_contextualized":
        display_atoms = facet_atoms.get("perceived_affect", [])
        return all(atom["bindings"] and atom["pixel_evidence_ids"] for atom in display_atoms), [
            str(atom["instance_id"]) for atom in display_atoms
        ]
    if predicate_id in {
        "display_inner_state_not_claimed",
        "attention_intention_not_claimed",
        "nonhuman_inner_state_not_claimed",
        "facial_motion_inner_state_not_claimed",
        "gesture_cultural_emblem_absent",
    }:
        return not bool(observed_effect_ids & blocked_narrative_effects), relevant_ids
    if predicate_id == "event_roles_coherent":
        nonnull_roles = {role_id for role_id, role in roles.items() if role["value_id"] is not None}
        role_edge_ids = {
            str(edge["relation_id"]).split(":", 1)[1]
            for edge in edges.values()
            if str(edge["relation_id"]).startswith("has_role:")
        }
        passed = {"actor", "action", "phase"} <= nonnull_roles and role_edge_ids == nonnull_roles
        return passed, sorted(nonnull_roles)
    if predicate_id == "nonhuman_channel_context_bound":
        nxc_atoms = [
            atom
            for atom_id, atom in atom_by_id.items()
            if any(
                topic == "nonhuman_expression_channels"
                for topic in candidate_by_atom[atom_id]["research_topic_ids"]
            )
        ]
        return all(atom["bindings"] and atom["pixel_evidence_ids"] for atom in nxc_atoms), [
            str(atom["instance_id"]) for atom in nxc_atoms
        ]
    if predicate_id == "weapon_event_safe":
        if "active_weapon_discharge" in observed_effect_ids:
            return False, ["active_weapon_discharge"]
        weapon_present = "prop_decommissioned_machine_gun" in matched_prop_ids
        if not weapon_present:
            return True, ["no_reviewed_weapon_present"]
        context = validated.contract["context_profile"]
        passed = (
            context["violence"] != "active"
            and roles.get("target", {}).get("value_id") is not None
            and "active_weapon_discharge" not in observed_effect_ids
        )
        return passed, ["prop_decommissioned_machine_gun", "target"]
    if predicate_id in {
        "resource_capacity_within_declared",
        "contact_resource_within_capacity",
        "resource_claims_within_capability",
    }:
        capability_bindings = [
            ":".join(
                [
                    str(record["entity_id"]),
                    "capability",
                    str(record["resource_kind"]),
                    canonical_sha256(record),
                ]
            )
            for record in _scene_capability_records(validated)
        ]
        attachment_capabilities = {
            "human_face_attachment": "facial_display",
            "human_hand_attachment": "manipulator",
            "human_limb_attachment": "appendage",
        }
        attachment_pass = True
        attachment_bindings: list[str] = []
        for occurrence in effect_occurrences:
            effect_id = str(occurrence["effect_id"])
            capability_id = attachment_capabilities.get(effect_id)
            if capability_id is None:
                continue
            subject_ref = occurrence["subject_ref"]
            if subject_ref is None or subject_ref not in validated.entity_by_id:
                attachment_pass = False
                attachment_bindings.append(f"unresolved:{effect_id}")
                continue
            subject_capacities = _available_capabilities(validated, str(subject_ref))
            attachment_pass = attachment_pass and subject_capacities.get(capability_id, 0) > 0
            attachment_bindings.append(f"{subject_ref}:{capability_id}")
        bindings = [
            *(str(claim["claim_id"]) for claim in claims),
            *capability_bindings,
            *attachment_bindings,
        ] or ["no_resource_claim_or_attachment_effect"]
        return capacity_pass and attachment_pass, bindings
    if predicate_id == "narrative_effects_absent":
        bindings = sorted(observed_effect_ids) or ["no_blocked_narrative_effect_observed"]
        return not bool(observed_effect_ids & blocked_narrative_effects), bindings
    if predicate_id == "weapon_role_target_safe":
        weapon_present = "prop_decommissioned_machine_gun" in matched_prop_ids
        passed = (
            not weapon_present
            or (
                roles.get("target", {}).get("value_id") is not None
                and not bool(
                    observed_effect_ids
                    & {"combat_opponent_assignment", "combat_target_assignment"}
                )
            )
        )
        return passed, ["target"] if weapon_present else ["no_reviewed_weapon_present"]
    if predicate_id == "gesture_context_bound":
        gesture_atoms = facet_atoms.get("gesture", [])
        return all(atom["bindings"] and atom["pixel_evidence_ids"] for atom in gesture_atoms), [
            str(atom["instance_id"]) for atom in gesture_atoms
        ]
    if predicate_id == "bridge_path_connected":
        return bool(bridges) and bridge_edges_pass, [str(bridge["bridge_id"]) for bridge in bridges]
    if predicate_id == "bridge_pixel_grounded":
        return bool(bridges) and bridge_pixels_pass, [str(bridge["bridge_id"]) for bridge in bridges]
    if predicate_id == "contact_pixel_grounded":
        contact_atoms = facet_atoms.get("contact", [])
        passed = all(
            any(
                pixel_items[pixel_id]["kind"] in {"contact", "support"}
                for pixel_id in atom["pixel_evidence_ids"]
            )
            for atom in contact_atoms
        )
        return passed, [str(atom["instance_id"]) for atom in contact_atoms]
    if predicate_id == "consequence_review_scale_declared":
        consequence_ids = set(pixels["consequence_item_ids"])
        passed = bool(consequence_ids) and all(
            item_id in pixel_items and bool(pixel_items[item_id]["minimum_scale_ids"])
            for item_id in consequence_ids
        )
        return passed, sorted(str(item) for item in consequence_ids)
    if predicate_id == "atom_event_edges_connected":
        return atom_edges_pass, [str(atom["instance_id"]) for atom in atoms]
    if predicate_id == "prop_literal_sense_bound":
        selected_prop_sources = {
            *(str(atom["candidate_id"]) for atom in atoms),
            *(str(bridge["candidate_id"]) for bridge in bridges),
        }
        fixed_prop_atoms = {
            candidate_id
            for candidate_id in selected_prop_sources
            if any(
                candidate_id in assets.prop_by_id[prop_id]["affordance_candidate_ids"]
                for prop_id in matched_prop_ids
            )
        }
        fixed_prop_atoms.update(
            str(candidate_id)
            for prop_id in matched_prop_ids
            for candidate_id in assets.prop_by_id[prop_id]["affordance_candidate_ids"][:1]
        )
        passed = all(
            any(candidate_id in fixed_prop_atoms for candidate_id in assets.prop_by_id[prop_id]["affordance_candidate_ids"])
            for prop_id in matched_prop_ids
        )
        bindings = sorted({*matched_prop_ids, *fixed_prop_atoms}) or [
            "no_reviewed_catalog_prop_present"
        ]
        return passed, bindings
    if predicate_id == "relation_event_edges_connected":
        relation_atoms = facet_atoms.get("relation", [])
        passed = all(
            len(atom["event_edge_ids"]) == 1 and atom["event_edge_ids"][0] in edges
            for atom in relation_atoms
        )
        bindings = [str(atom["instance_id"]) for atom in relation_atoms] or [
            "no_selected_relation_atom"
        ]
        return passed, bindings
    if predicate_id == "creativity_invariant_pool_traced":
        trace = selection["selection_trace"]
        invariant = selection["creativity_invariant_trace"]
        profiles = [row["record_id"] for row in invariant["eligible_proposals"]]
        rejected = [
            {
                "proposal_id": row["record_id"],
                "reason_code": row["reason_codes"][0],
            }
            for row in invariant["rejected_proposals"]
        ]
        candidate_ids = [
            candidate_id
            for facet in FACET_IDS
            for candidate_id in trace["eligible_candidate_ids_by_facet"][facet]
        ]
        candidate_rejections = [
            {
                "candidate_id": row["record_id"],
                "reason_code": (
                    f"closed_facet:{assets.candidate_by_id[row['record_id']]['facet']}"
                    if row["reason_codes"] == ["closed_facet"]
                    else f"fixed_facet:{assets.candidate_by_id[row['record_id']]['facet']}"
                    if row["reason_codes"] == ["fixed_facet_conflict"]
                    else row["reason_codes"][0]
                ),
            }
            for row in invariant["rejected_candidates"]
        ]
        passed = (
            invariant["complete_trace"] is True
            and invariant["trace_sha256"] == _trace_self_hash(invariant)
            and trace["eligible_proposal_profile_ids"] == profiles
            and trace["proposal_rejections"] == rejected
            and sorted(candidate_ids) == invariant["eligible_candidate_ids"]
            and trace["candidate_rejections"] == candidate_rejections
        )
        return passed, [invariant["trace_sha256"], *profiles]
    if predicate_id == "remote_budget_within_global":
        distance = selection["semantic_distance_trace"]
        passed = (
            distance["max_optional_remote_count"] == GLOBAL_OPTIONAL_REMOTE_MAX
            and distance["optional_remote_count"] <= 1
            and (
                distance["fixed_remote_count"] == 0
                or distance["optional_remote_count"] == 0
            )
        )
        bindings = list(distance["remote_atom_ids"])
        bindings.extend(
            [
                f"fixed_remote_count:{distance['fixed_remote_count']}",
                f"optional_remote_count:{distance['optional_remote_count']}",
                f"max_optional_remote_count:{distance['max_optional_remote_count']}",
            ]
        )
        return passed, bindings
    if predicate_id == "remote_premise_has_visible_bridge":
        remote_ids = set(selection["semantic_distance_trace"]["remote_atom_ids"])
        bridged_remote_ids = {
            atom_id
            for atom_id in remote_ids
            if any(
                atom_id in {str(bridge["from_node_id"]), str(bridge["to_node_id"])}
                for bridge in bridges
            )
        }
        return bridged_remote_ids == remote_ids and bridge_pixels_pass, sorted(remote_ids)
    if predicate_id == "identity_core_preserved":
        entities = validated.contract["identity_core"]["entities"]
        selected_candidates = {str(atom["candidate_id"]) for atom in atoms}
        return bool(entities) and "usl_core_identity_anchor" in selected_candidates, [
            str(entity["entity_id"]) for entity in entities
        ]
    if predicate_id == "physical_relation_grounded":
        physical_atoms = [
            atom for facet in ("contact", "relation") for atom in facet_atoms.get(facet, [])
        ]
        return all(atom["event_edge_ids"] and atom["pixel_evidence_ids"] for atom in physical_atoms), [
            str(atom["instance_id"]) for atom in physical_atoms
        ]
    if predicate_id == "history_claim_pixel_grounded":
        history_atoms = facet_atoms.get("prop_state", [])
        return all(atom["event_edge_ids"] and atom["pixel_evidence_ids"] for atom in history_atoms), [
            str(atom["instance_id"]) for atom in history_atoms
        ]
    if predicate_id == "local_policy_authority_separated":
        allowed_policy = ("policy", "local_default_metadata", "automatic_pass")
        selected_candidate_ids = {str(atom["candidate_id"]) for atom in atoms}
        selected_proposal_ids = {
            str(atom["parameters"]["proposal_id"])
            for atom in atoms
            if "proposal_id" in atom["parameters"]
        }
        proposal_profiles = [
            profile
            for profile in assets.candidates["proposal_profiles"]
            if str(profile["id"]) in selected_proposal_ids
        ]
        context_profiles = [
            profile
            for profile in assets.candidates["context_distance_profiles"]
            if set(str(value) for value in profile["candidate_ids"]) <= selected_candidate_ids
        ]
        policy_predicates = {
            tuple(predicate)
            for atom in atoms
            for predicate in assets.candidate_by_id[str(atom["candidate_id"])]["runtime_contract"]["requires_all"]
            if predicate[0] == "policy"
        }
        policy_predicates.update(
            tuple(predicate)
            for profile in [*proposal_profiles, *context_profiles]
            for predicate in profile["requires_all"]
            if predicate[0] == "policy"
        )
        policy_modes = {
            str(profile["policy_mode"])
            for profile in [*proposal_profiles, *context_profiles]
        }
        passed = (
            (not policy_predicates or policy_predicates == {allowed_policy})
            and policy_modes <= {"ordinary", "safe_tool", "explicit_weapon_only"}
        )
        return passed, sorted(
            "::".join(item) for item in policy_predicates
        ) + sorted(f"policy_mode:{mode}" for mode in policy_modes)
    if predicate_id == "theme_load_within_limit":
        maximum = max((int(atom["load_vector"]["theme_displacement"]) for atom in atoms), default=0)
        fixed_theme_cap = max(
            (
                int(assets.prop_by_id[prop_id]["base_load_profile"]["theme_displacement"])
                for prop_id in matched_prop_ids
            ),
            default=0,
        )
        allowed_maximum = max(2, fixed_theme_cap)
        return maximum <= allowed_maximum, [
            f"theme_displacement:{maximum}",
            f"allowed_theme_displacement:{allowed_maximum}",
        ]
    raise SelectionError(f"guard execution predicate is not implemented: {predicate_id}")


def _contract_effect_term_surface_values(
    clause: str,
    terms: Sequence[str],
) -> tuple[str, ...]:
    """Return reviewed effect terms as they occur, including inflections.

    Catalog aliases keep their stricter exact-token matcher.  Contract-effect
    composition is separately protected by same-clause AND groups, so ordinary
    English verb inflections and CJK grammatical suffixes may be recognized
    without promoting those rules into prop or identity resolution.
    """

    normalized_clause = _normalize_text(clause)
    surfaces: list[str] = []
    for raw_term in terms:
        term = _normalize_text(str(raw_term))
        if not term:
            continue
        if term.isascii():
            tokens = _ascii_alnum_tokens(term)
            if not tokens:
                continue
            final = tokens[-1]
            final_forms = {final}
            if len(final) >= 3 and final.isalpha():
                final_forms.update(
                    {
                        f"{final}s",
                        f"{final}es",
                        f"{final}ed",
                        f"{final}d",
                        f"{final}ing",
                    }
                )
                if final.endswith("e") and len(final) > 3:
                    final_forms.add(f"{final[:-1]}ing")
                if final.endswith("y") and len(final) > 3:
                    final_forms.update({f"{final[:-1]}ies", f"{final[:-1]}ied"})
            prefix = r"\s+".join(re.escape(token) for token in tokens[:-1])
            if prefix:
                prefix += r"\s+"
            pattern = (
                r"(?<![a-z0-9])"
                + prefix
                + r"(?:"
                + "|".join(
                    re.escape(value)
                    for value in sorted(final_forms, key=lambda value: (-len(value), value))
                )
                + r")(?![a-z0-9])"
            )
            for match in re.finditer(pattern, normalized_clause):
                surface = match.group(0)
                if surface not in surfaces:
                    surfaces.append(surface)
        else:
            for start, end in _normalized_substring_spans(term, normalized_clause):
                surface = normalized_clause[start:end]
                if surface not in surfaces:
                    surfaces.append(surface)
    return tuple(surfaces)


_CONTRACT_EFFECT_HARD_CLAUSE_PATTERN = re.compile(
    r"[.!?;:。！？；：\r\n]+|\s*[\u2012-\u2015]\s*|"
    r"\b(?:but|however|yet|whereas|while|then|even\s+though|although)\b|"
    r"(?:하지만|그러나|반면|그런데|그\s*뒤|그\s*후|"
    r"しかし|ただし|一方|その後|"
    r"但是|然而|不过|但)"
)
_CONTRACT_EFFECT_SOFT_COORDINATOR_PATTERN = re.compile(
    r"\band\b|(?:그리고|하고|そして|并且|然后)"
)
_CONTRACT_EFFECT_EN_INDEPENDENT_SUBJECT_PATTERN = re.compile(
    r"^(?:a|an|the|this|that|these|those|another|it|he|she|they|we|i|you)\b"
)


def _contract_effect_assertion_clauses(
    value: str,
    assets: UniversalSceneAssets,
) -> tuple[tuple[str, bool], ...]:
    """Return effect clauses plus inherited negative-directive scope.

    Sentence punctuation, em dashes, and contrastive coordinators always reset
    assertion scope.  A plain additive coordinator keeps a negative directive
    on same-subject conjuncts (``do not X and Y``).  English resets that carry
    only when the right side starts an explicit determiner/pronoun subject;
    this preserves ``... and the weapon fires`` as an affirmative
    reassertion.  KO/JA/ZH pro-drop coordination remains conservative unless a
    hard contrast boundary starts the new assertion.
    """

    raw = unicodedata.normalize("NFKC", str(value)).casefold()
    result: list[tuple[str, bool]] = []
    for hard_part in _CONTRACT_EFFECT_HARD_CLAUSE_PATTERN.split(raw):
        if not hard_part.strip():
            continue
        soft_parts = _CONTRACT_EFFECT_SOFT_COORDINATOR_PATTERN.split(hard_part)
        inherited_negative = False
        for part_index, raw_part in enumerate(soft_parts):
            clause = _normalize_text(raw_part)
            if not clause:
                continue
            explicit_subject_reset = bool(
                part_index > 0
                and _CONTRACT_EFFECT_EN_INDEPENDENT_SUBJECT_PATTERN.match(clause)
            )
            force_negated = (
                part_index > 0
                and inherited_negative
                and not explicit_subject_reset
            )
            result.append((clause, force_negated))
            own_negative = _contract_effect_clause_has_global_negative(
                clause,
                assets,
            )
            inherited_negative = own_negative or (
                force_negated and not explicit_subject_reset
            )
    return tuple(result)


def _contract_effect_group_polarities(
    clause: str,
    group: Sequence[str],
    assets: UniversalSceneAssets,
) -> set[str]:
    surfaces = _contract_effect_term_surface_values(
        clause, [str(value) for value in group]
    )
    return {
        polarity
        for surface in surfaces
        for polarity in _literal_alias_occurrence_polarities(
            clause,
            [surface],
            assets,
            include_target_absence=True,
            include_target_substitution=True,
            allow_korean_postposed_copular=True,
            allow_authenticated_nonascii_substrings=True,
            allow_reviewed_nonascii_marker_affixes=True,
        )
    }


def _contract_effect_clause_has_global_negative(
    clause: str,
    assets: UniversalSceneAssets,
) -> bool:
    normalized = _normalize_text(clause).replace("not only", "")
    directional_spans = {
        span
        for record in assets.semantic_bindings["literal_polarity_contract"]["negative_markers"]
        for marker in record["target_substitution_values"]
        for span in _normalized_substring_spans(str(marker["value"]), normalized)
    }
    for record in assets.semantic_bindings["literal_polarity_contract"]["negative_markers"]:
        for field in (
            "logical_values",
            "target_absence_values",
            "affirmative_conflict_values",
        ):
            for raw_marker in record[field]:
                marker = str(raw_marker)
                spans = (
                    _normalized_alias_spans(marker, normalized)
                    if marker.isascii()
                    else _normalized_substring_spans(marker, normalized)
                )
                if any(
                    not any(
                        directional_start <= start and end <= directional_end
                        for directional_start, directional_end in directional_spans
                    )
                    for start, end in spans
                ):
                    return True
    return False


def _contract_effect_profile_direct_polarities(
    profile: Mapping[str, Any],
    phrases: Sequence[str],
    assets: UniversalSceneAssets,
) -> set[str]:
    aliases = [
        str(value)
        for record in profile["literal_aliases"]
        for value in record["values"]
    ]
    result: set[str] = set()
    for phrase in phrases:
        for clause, inherited_negative in _contract_effect_assertion_clauses(
            str(phrase),
            assets,
        ):
            surfaces = _contract_effect_term_surface_values(clause, aliases)
            if not surfaces:
                continue
            polarities = {
                polarity
                for surface in surfaces
                for polarity in _literal_alias_occurrence_polarities(
                    clause,
                    [surface],
                    assets,
                    include_target_absence=True,
                    include_target_substitution=True,
                    allow_korean_postposed_copular=True,
                    allow_authenticated_nonascii_substrings=True,
                    allow_reviewed_nonascii_marker_affixes=True,
                )
            }
            if inherited_negative or _contract_effect_clause_has_global_negative(
                clause,
                assets,
            ):
                result.add("negated")
            else:
                result.update(polarities)
    return result


def _contract_effect_profile_compositional_polarities(
    profile: Mapping[str, Any],
    phrases: Sequence[str],
    assets: UniversalSceneAssets,
) -> set[str]:
    result: set[str] = set()
    groups = list(profile["required_literal_groups"])
    for phrase in phrases:
        for clause, inherited_negative in _contract_effect_assertion_clauses(
            str(phrase),
            assets,
        ):
            group_polarities = [
                _contract_effect_group_polarities(clause, group, assets)
                for group in groups
            ]
            if not group_polarities or any(not polarities for polarities in group_polarities):
                continue
            # The action/growth/assignment group is last by asset contract.
            # Its local polarity governs the matched compositional clause;
            # earlier descriptive groups may be farther from a postposed
            # marker, but cannot turn a directly negated action positive.
            if inherited_negative or "negated" in group_polarities[-1]:
                result.add("negated")
            elif "affirmative" in group_polarities[-1]:
                result.add("affirmative")
    return result


def _contract_effect_projection_records(
    *,
    request_text: str,
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> list[dict[str, Any]]:
    profiles = list(assets.semantic_bindings["contract_effect_profiles"])
    actor_entity_id = _actor_entity_id(validated)
    roles = validated.role_by_id
    occurrences: list[dict[str, Any]] = [
        {
            "source_kind": "request",
            "source_id": "concept",
            "instance_kind": "context_value",
            "instance_id": "request::concept",
            "phrases": [request_text],
            "semantic_value_ids": [],
            "source_entity_id": actor_entity_id,
            "assertion": "positive",
        }
    ]
    identity = validated.contract["identity_core"]
    for entity in identity["entities"]:
        entity_id = str(entity["entity_id"])
        for fact in entity["feature_facts"]:
            occurrences.append(
                {
                    "source_kind": "identity_fact",
                    "source_id": "feature_fact",
                    "instance_kind": "identity_fact",
                    "instance_id": f"feature_fact::{entity_id}::{fact['id']}",
                    "phrases": list(fact["request_phrases"]),
                    "semantic_value_ids": [str(fact["id"])],
                    "source_entity_id": entity_id,
                    "assertion": "positive",
                }
            )
    for list_name, source_id, assertion in (
        ("scene_facts", "scene_fact", "positive"),
        ("forbidden_facts", "forbidden_fact", "forbidden"),
    ):
        for fact in identity[list_name]:
            occurrences.append(
                {
                    "source_kind": "identity_fact",
                    "source_id": source_id,
                    "instance_kind": "identity_fact",
                    "instance_id": f"{source_id}::{fact['id']}",
                    "phrases": list(fact["request_phrases"]),
                    "semantic_value_ids": [str(fact["id"])],
                    "source_entity_id": actor_entity_id,
                    "assertion": assertion,
                }
            )
    for slot in validated.contract["slot_states"]:
        occurrences.append(
            {
                "source_kind": "slot",
                "source_id": str(slot["slot_id"]),
                "instance_kind": "slot_state",
                "instance_id": f"slot_state::{slot['slot_id']}",
                "phrases": list(slot["request_phrases"]),
                "semantic_value_ids": [str(value) for value in slot["value_ids"]],
                "source_entity_id": actor_entity_id,
                "assertion": "negative" if slot["state"] == "closed" else "positive",
            }
        )
    for role in validated.contract["event_roles"]:
        semantic_values = [] if role["value_id"] is None else [str(role["value_id"])]
        occurrences.append(
            {
                "source_kind": "event_role",
                "source_id": str(role["role_id"]),
                "instance_kind": "event_role",
                "instance_id": f"event_role::{role['role_id']}",
                "phrases": list(role["request_phrases"]),
                "semantic_value_ids": semantic_values,
                "source_entity_id": actor_entity_id,
                "assertion": "negative" if role["state"] == "closed" else "positive",
            }
        )
    for field in CONTEXT_FIELD_IDS:
        raw_context_value = validated.contract["context_profile"][field]
        semantic_values = (
            [str(value) for value in raw_context_value]
            if isinstance(raw_context_value, list)
            else [str(raw_context_value)]
        )
        occurrences.append(
            {
                "source_kind": "context",
                "source_id": field,
                "instance_kind": "context_value",
                "instance_id": f"context_value::{field}",
                "phrases": [request_text],
                "semantic_value_ids": semantic_values,
                "source_entity_id": actor_entity_id,
                "assertion": "positive",
            }
        )

    def subject_for(profile: Mapping[str, Any], occurrence: Mapping[str, Any]) -> str | None:
        binding = str(profile["subject_binding"])
        if binding == "scene":
            return None
        if binding == "source_entity":
            return str(occurrence["source_entity_id"])
        if binding in {"target", "recipient"}:
            participant = validated.participant_by_role[binding]
            if participant["primary_entity_id"] is not None:
                return str(participant["primary_entity_id"])
            return binding
        return actor_entity_id

    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for occurrence in occurrences:
        if occurrence["assertion"] == "forbidden":
            continue
        target_key = (str(occurrence["source_kind"]), str(occurrence["source_id"]))
        for profile in profiles:
            targets = {
                (str(target["source_kind"]), str(target["source_id"]))
                for target in profile["source_targets"]
            }
            if target_key not in targets:
                continue
            polarities = _contract_effect_profile_direct_polarities(
                profile, occurrence["phrases"], assets
            )
            semantic_match = bool(
                set(str(value) for value in occurrence["semantic_value_ids"])
                & set(str(value) for value in profile["semantic_value_ids"])
            )
            literal_match = "affirmative" in polarities
            compositional_polarities = _contract_effect_profile_compositional_polarities(
                profile, occurrence["phrases"], assets
            )
            compositional_match = "affirmative" in compositional_polarities
            semantic_match_is_affirmative = (
                semantic_match
                and "negated" not in polarities
                and "negated" not in compositional_polarities
            )
            if (
                not literal_match
                and not compositional_match
                and not semantic_match_is_affirmative
            ):
                continue
            group_key = (str(occurrence["instance_kind"]), str(occurrence["instance_id"]))
            item = grouped.setdefault(
                group_key,
                {
                    "instance_kind": str(occurrence["instance_kind"]),
                    "instance_id": str(occurrence["instance_id"]),
                    "scope": "contract_projection",
                    "source_profile_refs": [],
                    "contract_effect_profile_ids": [],
                    "effect_occurrences": [],
                    "load_vector": {axis: 0 for axis in LOAD_AXIS_IDS},
                },
            )
            profile_id = str(profile["id"])
            effect = {
                "effect_id": str(profile["effect_id"]),
                "source_profile_id": profile_id,
                "subject_ref": subject_for(profile, occurrence),
            }
            if profile_id not in item["contract_effect_profile_ids"]:
                item["contract_effect_profile_ids"].append(profile_id)
            if effect not in item["effect_occurrences"]:
                item["effect_occurrences"].append(effect)
    result = list(grouped.values())
    for item in result:
        item["contract_effect_profile_ids"].sort()
        item["effect_occurrences"].sort(
            key=lambda value: (
                str(value["effect_id"]),
                str(value["source_profile_id"]),
                "" if value["subject_ref"] is None else str(value["subject_ref"]),
            )
        )
    return sorted(result, key=lambda item: (item["instance_kind"], item["instance_id"]))


def _utf8_sorted(values: Iterable[str]) -> list[str]:
    return sorted(set(str(value) for value in values), key=lambda value: value.encode("utf-8"))


def _owner_scope_hash(owner_scope: str, validated: ValidatedSceneContract) -> str:
    return canonical_sha256(
        {
            "schema": "illustration-universal-scene-capacity-owner/v1",
            "scene_contract_sha256": validated.sha256,
            "owner_scope": str(owner_scope),
        }
    )


def _trace_self_hash(trace: Mapping[str, Any]) -> str:
    return canonical_sha256(
        {key: value for key, value in trace.items() if key != "trace_sha256"}
    )


def _mandatory_literal_reservations(
    *,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
) -> list[dict[str, Any]]:
    return _reserve_literal_visual_realization_requirements(
        [],
        validated=validated,
        roles=roles,
        matched_prop_ids=matched_prop_ids,
        assets=assets,
    )


def _preselection_trial(
    *,
    record_id: str,
    mandatory_entries: Sequence[Mapping[str, Any]],
    tested_entry: Mapping[str, Any] | None,
    tested_source_kind: str | None,
    tested_source_id: str | None,
    validated: ValidatedSceneContract,
) -> dict[str, Any]:
    canonical_mandatory = sorted(
        mandatory_entries,
        key=lambda entry: (
            str(entry["candidate"]["id"]),
            tuple(
                _utf8_sorted(
                    [str(entry.get("parameters", {}).get("literal_realization_profile_id"))]
                    if entry.get("parameters", {}).get("literal_realization_profile_id")
                    else []
                )
            ),
            canonical_sha256(entry.get("parameters", {})),
        ),
    )
    trial_entries: list[tuple[str, str, Mapping[str, Any]]] = [
        ("mandatory_literal", str(entry["candidate"]["id"]), entry)
        for entry in canonical_mandatory
    ]
    if tested_entry is not None and not any(
        str(entry["candidate"]["id"])
        == str(tested_entry["candidate"]["id"])
        for entry in canonical_mandatory
    ):
        if tested_source_kind is None or tested_source_id is None:
            raise SelectionError("tested preselection entry lacks a typed source")
        trial_entries.append((tested_source_kind, tested_source_id, tested_entry))

    entry_rows: list[dict[str, Any]] = []
    resolved_claim_rows: list[dict[str, Any]] = []
    for entry_ordinal, (source_kind, source_id, entry) in enumerate(trial_entries):
        parameters = entry.get("parameters", {})
        profile_id = parameters.get("literal_realization_profile_id")
        entry_rows.append(
            {
                "entry_ordinal": entry_ordinal,
                "source_kind": source_kind,
                "source_id": source_id,
                "candidate_id": str(entry["candidate"]["id"]),
                "literal_realization_profile_ids": (
                    [str(profile_id)] if profile_id is not None else []
                ),
                "parameters_sha256": canonical_sha256(parameters),
            }
        )
        owner_refs = parameters.get("resolved_owner_refs", [])
        for raw_claim_ordinal, raw_claim in enumerate(
            entry["candidate"]["runtime_contract"]["resource_claims"]
        ):
            resolved_claims = sorted(
                _resolved_claim_tuples(raw_claim, validated, owner_refs),
                key=lambda item: str(item[1]).encode("utf-8"),
            )
            for resolved_owner_ordinal, (kind, owner_id, amount, mode) in enumerate(
                resolved_claims
            ):
                resolved_claim_rows.append(
                    {
                        "entry_ordinal": entry_ordinal,
                        "raw_claim_ordinal": raw_claim_ordinal,
                        "resolved_owner_ordinal": resolved_owner_ordinal,
                        "owner_scope_hash": _owner_scope_hash(owner_id, validated),
                        "resource_kind": str(kind),
                        "amount": int(amount),
                        "mode": str(mode),
                    }
                )

    literal_facets = {
        str(entry["candidate"]["facet"])
        for entry in canonical_mandatory
        if entry.get("parameters", {}).get("literal_realization_profile_id") is not None
    }
    literal_facet_counts = [
        {
            "facet_id": facet_id,
            "count": sum(
                str(entry[2]["candidate"]["facet"]) == facet_id
                for entry in trial_entries
            ),
        }
        for facet_id in _utf8_sorted(literal_facets)
    ]
    return {
        "schema": PRESELECTION_TRIAL_SCHEMA,
        "record_id": record_id,
        "entries": entry_rows,
        "resolved_claims": resolved_claim_rows,
        "literal_facet_counts": literal_facet_counts,
        "literal_total": sum(
            entry.get("parameters", {}).get("literal_realization_profile_id")
            is not None
            for entry in canonical_mandatory
        ),
    }


def _resource_capacity_rows(
    validated: ValidatedSceneContract,
) -> list[dict[str, Any]]:
    capacities = _resource_capacities(validated)
    owner_scopes: list[tuple[str, tuple[str, ...]]] = [
        ("scene", tuple(sorted(SCENE_RESOURCE_KINDS)))
    ]
    owner_scopes.extend(
        (str(entity_id), tuple(sorted(ENTITY_RESOURCE_KINDS)))
        for entity_id in sorted(validated.entity_by_id)
    )
    owner_scopes.extend(
        (role_id, tuple(sorted(ENTITY_RESOURCE_KINDS)))
        for role_id in EVENT_ROLE_IDS
        if validated.participant_by_role[role_id]["primary_entity_id"] is None
    )
    rows = [
        {
            "owner_scope_hash": _owner_scope_hash(owner_scope, validated),
            "resource_kind": resource_kind,
            "capacity": int(capacities.get((owner_scope, resource_kind), 0)),
            "state": (
                "available"
                if int(capacities.get((owner_scope, resource_kind), 0)) > 0
                else "unavailable"
            ),
        }
        for owner_scope, resource_kinds in owner_scopes
        for resource_kind in resource_kinds
    ]
    rows.sort(key=lambda row: (row["owner_scope_hash"], row["resource_kind"]))
    return rows


def _trial_resource_checks(
    trial: Mapping[str, Any],
    capacity_by_hash_kind: Mapping[tuple[str, str], int],
) -> list[dict[str, Any]]:
    exclusive: dict[tuple[str, str], int] = {}
    shared: dict[tuple[str, str], int] = {}
    for claim in trial["resolved_claims"]:
        key = (str(claim["owner_scope_hash"]), str(claim["resource_kind"]))
        if claim["mode"] == "exclusive":
            exclusive[key] = exclusive.get(key, 0) + int(claim["amount"])
        else:
            shared[key] = max(shared.get(key, 0), int(claim["amount"]))
    return [
        {
            "owner_scope_hash": owner_scope_hash,
            "resource_kind": resource_kind,
            "exclusive_required": exclusive.get((owner_scope_hash, resource_kind), 0),
            "shared_required": shared.get((owner_scope_hash, resource_kind), 0),
            "capacity": int(
                capacity_by_hash_kind.get((owner_scope_hash, resource_kind), 0)
            ),
            "fits": (
                exclusive.get((owner_scope_hash, resource_kind), 0)
                + shared.get((owner_scope_hash, resource_kind), 0)
                <= int(capacity_by_hash_kind.get((owner_scope_hash, resource_kind), 0))
            ),
        }
        for owner_scope_hash, resource_kind in sorted(set(exclusive) | set(shared))
    ]


def _cardinality_limit_rows(assets: UniversalSceneAssets) -> list[dict[str, Any]]:
    compatibility_scope = {
        "display_bundles": ("bundle", "display"),
        "display_primitives_per_bundle": ("bundle", "display"),
        "event_spines": ("scene", "event_graph"),
        "gestures": ("facet", "gesture"),
        "optional_props": ("facet", "prop"),
        "orphan_atoms": ("scene", "event_graph"),
        "perceived_affect_hypotheses": ("facet", "perceived_affect"),
        "phases": ("facet", "phase"),
        "pose_support_solutions": ("facet", "pose"),
        "primary_actions": ("facet", "action"),
        "primary_environment_roles": ("facet", "environment"),
        "relation_topologies": ("facet", "relation"),
        "remote_or_high_load_optional_premises": ("global", "optional_remote"),
        "second_independent_premises": ("global", "independent_premise"),
    }
    rows = [
        {
            "record_id": f"compatibility_budget__{metric_id}",
            "source_kind": "compatibility_budget",
            "metric_id": metric_id,
            "evaluation_stage": "postselection_scene",
            "scope_kind": compatibility_scope[metric_id][0],
            "scope_id": compatibility_scope[metric_id][1],
            "minimum": 0,
            "maximum": int(maximum),
        }
        for metric_id, maximum in assets.compatibility["budgets"].items()
    ]
    runtime_limits = (
        ("context_profile_carriers", "postselection_scene", "global", "context_carrier", MAX_CONTEXT_PROFILE_CARRIERS),
        ("global_optional_remote", "postselection_scene", "global", "optional_remote", GLOBAL_OPTIONAL_REMOTE_MAX),
        ("literal_realization_atoms_per_facet", "preselection_reservation", "each_facet", None, MAX_LITERAL_REALIZATION_ATOMS_PER_FACET),
        ("literal_realization_atoms_total", "preselection_reservation", "global", "literal_realization", MAX_LITERAL_REALIZATION_ATOMS_TOTAL),
        ("selected_resource_claims_total", "postselection_scene", "global", "resource_claim", MAX_SELECTED_RESOURCE_CLAIMS_TOTAL),
        ("selected_visual_atoms_total", "postselection_scene", "global", "visual_atom", MAX_SELECTED_VISUAL_ATOMS_TOTAL),
    )
    rows.extend(
        {
            "record_id": f"runtime_limit__{metric_id}",
            "source_kind": "runtime_limit",
            "metric_id": metric_id,
            "evaluation_stage": stage,
            "scope_kind": scope_kind,
            "scope_id": scope_id,
            "minimum": 0,
            "maximum": maximum,
        }
        for metric_id, stage, scope_kind, scope_id, maximum in runtime_limits
    )
    return sorted(rows, key=lambda row: row["record_id"].encode("utf-8"))


def _matched_prop_sense_occurrence_hashes(
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> list[str]:
    sources: list[tuple[str, str]] = []
    prop_index = next(
        index
        for index, slot in enumerate(validated.contract["slot_states"])
        if slot["slot_id"] == "prop"
    )
    prop_slot = validated.slot_by_id["prop"]
    if prop_slot["state"] == "fixed":
        sources.extend(
            (f"/slot_states/{prop_index}/request_phrases/{index}", str(phrase))
            for index, phrase in enumerate(prop_slot["request_phrases"])
        )
    for role_id in ("target", "instrument"):
        role = validated.role_by_id[role_id]
        if role["state"] != "fixed":
            continue
        role_index = EVENT_ROLE_IDS.index(role_id)
        sources.extend(
            (f"/event_roles/{role_index}/request_phrases/{index}", str(phrase))
            for index, phrase in enumerate(role["request_phrases"])
        )
    semantic_values = _utf8_sorted(
        [
            *(_normalize_text(str(value)) for value in prop_slot["value_ids"]),
            *(
                _normalize_text(str(validated.role_by_id[role_id]["value_id"]))
                for role_id in ("target", "instrument")
                if validated.role_by_id[role_id]["state"] == "fixed"
            ),
        ]
    )
    phrases = [phrase for _, phrase in sources]
    result: list[str] = []
    for profiles in assets.prop_sense_by_catalog_id.values():
        for profile in profiles:
            if not _distinct_prop_sense_matches(profile, phrases, semantic_values):
                continue
            canonical_prop_id = str(
                profile["activation_target"] or profile["catalog_prop_id"]
            )
            for source_pointer, phrase in sources:
                normalized_phrase = _normalize_text(phrase)
                for record in profile["literal_aliases"]:
                    for raw_alias in record["values"]:
                        alias = str(raw_alias)
                        spans = list(_normalized_alias_spans(alias, normalized_phrase))
                        polarities = list(
                            _literal_alias_occurrence_polarities(
                                normalized_phrase,
                                [alias],
                                assets,
                                include_target_absence=True,
                                include_target_substitution=True,
                            )
                        )
                        if len(spans) != len(polarities):
                            raise SelectionError("prop-sense occurrence polarity did not preserve spans")
                        for (start, end), polarity in zip(spans, polarities):
                            result.append(
                                canonical_sha256(
                                    {
                                        "schema": "illustration-universal-scene-prop-sense-occurrence/v1",
                                        "source_pointer": source_pointer,
                                        "normalized_source_text_sha256": hashlib.sha256(
                                            normalized_phrase.encode("utf-8")
                                        ).hexdigest(),
                                        "binding_profile_id": str(profile["id"]),
                                        "canonical_prop_id": canonical_prop_id,
                                        "matched_alias_sha256": hashlib.sha256(
                                            _normalize_text(alias).encode("utf-8")
                                        ).hexdigest(),
                                        "semantic_values_sha256": canonical_sha256(semantic_values),
                                        "occurrence_start": start,
                                        "occurrence_end": end,
                                        "polarity": polarity,
                                    }
                                )
                            )
    return _utf8_sorted(result)


def _policy_source_contract_rows(assets: UniversalSceneAssets) -> list[dict[str, Any]]:
    sources: list[tuple[str, str, str, str, str | None, str | None, Mapping[str, Any]]] = []
    sources.extend(
        (
            f"proposal_policy__{profile['id']}",
            "proposal_policy",
            str(profile["id"]),
            "contract_input",
            str(profile["policy_mode"]),
            None,
            profile,
        )
        for profile in assets.candidates["proposal_profiles"]
    )
    sources.extend(
        (
            f"context_policy__{profile['id']}",
            "context_policy",
            str(profile["id"]),
            "contract_input",
            str(profile["policy_mode"]),
            None,
            profile,
        )
        for profile in assets.candidates["context_distance_profiles"]
    )
    sources.extend(
        (
            f"universal_rule__{rule['id']}",
            "universal_rule",
            str(rule["id"]),
            "postselection",
            None,
            str(rule["outcome"]),
            rule,
        )
        for rule in assets.compatibility["universal_rules"]
    )
    rows: list[dict[str, Any]] = []
    for record_id, source_kind, source_id, stage, mode, outcome, source_record in sources:
        source_payload = {
            "schema": "illustration-universal-scene-policy-source-contract/v1",
            "record_id": record_id,
            "source_kind": source_kind,
            "source_id": source_id,
            "evaluation_stage": stage,
            "policy_mode": mode,
            "declared_outcome": outcome,
            "source_record": source_record,
        }
        rows.append(
            {
                "record_id": record_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "evaluation_stage": stage,
                "policy_mode": mode,
                "declared_outcome": outcome,
                "source_contract_sha256": canonical_sha256(source_payload),
            }
        )
    return sorted(rows, key=lambda row: row["record_id"].encode("utf-8"))


def _preselection_policy_decision_rows(
    *,
    validated: ValidatedSceneContract,
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_kind, profiles in (
        ("proposal", assets.candidates["proposal_profiles"]),
        ("context", assets.candidates["context_distance_profiles"]),
    ):
        for profile in profiles:
            mode = str(profile["policy_mode"])
            if mode == "ordinary":
                applicable, outcome, reasons = True, "pass", ["policy_pass"]
            elif mode == "safe_tool":
                applicable = True
                if validated.contract["context_profile"]["violence"] == "active":
                    outcome, reasons = "reject", ["policy_active_violence"]
                else:
                    outcome, reasons = "pass", ["policy_pass"]
            elif source_kind == "proposal":
                applicable, outcome, reasons = True, "reject", ["policy_explicit_only"]
            elif "prop_decommissioned_machine_gun" in matched_prop_ids:
                applicable, outcome, reasons = True, "pass", ["policy_pass"]
            else:
                applicable, outcome, reasons = False, "not_applicable", ["policy_not_applicable"]
            rows.append(
                {
                    "record_id": f"{source_kind}_policy__{profile['id']}",
                    "applicable": applicable,
                    "outcome": outcome,
                    "reason_codes": reasons,
                }
            )
    return sorted(rows, key=lambda row: row["record_id"].encode("utf-8"))


def _guard_source_contract_rows(assets: UniversalSceneAssets) -> list[dict[str, Any]]:
    guard_profile_by_id = {
        str(profile["guard_id"]): str(profile["predicate_id"])
        for profile in assets.semantic_bindings["guard_execution_profiles"]
    }
    rows: list[dict[str, Any]] = []
    for guard_id in _utf8_sorted(assets.compatibility["guard_candidate_ids"]):
        candidate = assets.candidate_by_id[guard_id]
        runtime = candidate["runtime_contract"]
        row_without_hash = {
            "record_id": guard_id,
            "source_candidate_id": guard_id,
            "predicate_id": guard_profile_by_id[guard_id],
            "role": "guard",
            "evaluation_stage": "postselection_conditional",
            "research_topic_ids": _utf8_sorted(candidate["research_topic_ids"]),
            "provenance_record_ids": _utf8_sorted(candidate["provenance_record_ids"]),
            "stage": str(runtime["stage"]),
            "violation_code": str(runtime["violation_code"]),
            "when_all": _deep_canonical_copy(runtime["when_all"]),
            "require_all": _deep_canonical_copy(runtime["require_all"]),
            "declared_outcome": str(runtime["outcome"]),
        }
        rows.append(
            {
                "record_id": row_without_hash["record_id"],
                "source_candidate_id": row_without_hash["source_candidate_id"],
                "predicate_id": row_without_hash["predicate_id"],
                "source_contract_sha256": canonical_sha256(row_without_hash),
                **{
                    key: value
                    for key, value in row_without_hash.items()
                    if key not in {"record_id", "source_candidate_id", "predicate_id"}
                },
            }
        )
    return rows


def _build_creativity_invariant_trace(
    *,
    validated: ValidatedSceneContract,
    eligibility_roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    mandatory_entries = _mandatory_literal_reservations(
        validated=validated,
        roles=eligibility_roles,
        matched_prop_ids=matched_prop_ids,
        assets=assets,
    )
    mandatory_candidate_ids = {
        str(entry["candidate"]["id"]) for entry in mandatory_entries
    }
    mandatory_profile_ids = _utf8_sorted(
        str(entry["parameters"]["literal_realization_profile_id"])
        for entry in mandatory_entries
        if entry.get("parameters", {}).get("literal_realization_profile_id")
    )
    profile_by_id = {
        str(profile["id"]): profile
        for profile in assets.semantic_bindings["literal_visual_realization_profiles"]
    }
    mandatory_source_sha = canonical_sha256(
        [profile_by_id[profile_id] for profile_id in mandatory_profile_ids]
    )
    base_trial = _preselection_trial(
        record_id="mandatory_literal__base",
        mandatory_entries=mandatory_entries,
        tested_entry=None,
        tested_source_kind=None,
        tested_source_id=None,
        validated=validated,
    )

    proposal_decisions = [
        (
            profile,
            *_proposal_eligibility_decision(
                profile,
                validated=validated,
                roles=eligibility_roles,
                matched_prop_ids=matched_prop_ids,
                assets=assets,
                mandatory_candidate_ids=mandatory_candidate_ids,
            ),
        )
        for profile in assets.candidates["proposal_profiles"]
    ]
    eligible_proposals = [
        {
            "record_id": str(profile["id"]),
            "semantic_signature": canonical_sha256(
                _proposal_semantic_family_payload(profile, assets.candidate_by_id)
            ),
            "distance_band": _distance_band(profile["distance_profile"]),
        }
        for profile, eligible, _reason in proposal_decisions
        if eligible
    ]
    eligible_proposals.sort(key=lambda row: row["record_id"].encode("utf-8"))
    rejected_proposals = [
        {
            "record_id": str(profile["id"]),
            "outcome": "rejected",
            "reason_codes": [str(reason)],
        }
        for profile, eligible, reason in proposal_decisions
        if not eligible
    ]
    rejected_proposals.sort(key=lambda row: row["record_id"].encode("utf-8"))

    selected_ids = set(mandatory_candidate_ids)
    provided = {
        tuple(predicate)
        for entry in mandatory_entries
        for predicate in entry["candidate"]["postconditions"]
    }
    eligible_candidate_ids: list[str] = []
    rejected_candidates: list[dict[str, Any]] = []
    reason_map = {
        "trigger_unsatisfied": "trigger_unsatisfied",
        "precondition_unsatisfied": "precondition_unsatisfied",
        "capability_unsatisfied": "capability_unsatisfied",
    }
    visual_candidates = [
        candidate
        for candidate in assets.candidate_by_id.values()
        if candidate["role"] == "visual_atom"
    ]
    visual_candidates.sort(key=lambda candidate: str(candidate["id"]).encode("utf-8"))
    for candidate in visual_candidates:
        eligible, raw_reason = _candidate_is_eligible(
            candidate,
            validated=validated,
            roles=eligibility_roles,
            matched_prop_ids=matched_prop_ids,
            selected_candidate_ids=selected_ids,
            provided_predicates=provided,
            assets=assets,
        )
        candidate_id = str(candidate["id"])
        if eligible:
            eligible_candidate_ids.append(candidate_id)
            continue
        if raw_reason.startswith("closed_facet:"):
            reason = "closed_facet"
        elif raw_reason.startswith("fixed_facet:"):
            reason = "fixed_facet_conflict"
        else:
            reason = reason_map.get(raw_reason)
        if reason is None:
            raise SelectionError(
                f"visual candidate {candidate_id} has an untraceable rejection: {raw_reason}"
            )
        rejected_candidates.append(
            {"record_id": candidate_id, "outcome": "rejected", "reason_codes": [reason]}
        )

    capacity_rows = _resource_capacity_rows(validated)
    capacity_by_hash_kind = {
        (str(row["owner_scope_hash"]), str(row["resource_kind"])): int(row["capacity"])
        for row in capacity_rows
    }
    trials: dict[str, tuple[str, str | None, str, Mapping[str, Any]]] = {
        "mandatory_literal__base": (
            "mandatory_literal",
            None,
            mandatory_source_sha,
            base_trial,
        )
    }
    for profile in assets.candidates["proposal_profiles"]:
        primary = assets.candidate_by_id[str(profile["candidate_ids"][0])]
        entry = {
            "candidate": primary,
            "proposal": profile,
            "parameters": {
                "proposal_id": str(profile["id"]),
                "value_id": str(profile["value_id"]),
                "prompt_phrase_en": str(profile["prompt_phrase_en"]),
            },
        }
        record_id = f"proposal__{profile['id']}"
        trials[record_id] = (
            "proposal",
            str(profile["id"]),
            canonical_sha256(profile),
            _preselection_trial(
                record_id=record_id,
                mandatory_entries=mandatory_entries,
                tested_entry=entry,
                tested_source_kind="proposal",
                tested_source_id=str(profile["id"]),
                validated=validated,
            ),
        )
    for candidate in visual_candidates:
        candidate_id = str(candidate["id"])
        entry = {
            "candidate": candidate,
            "proposal": None,
            "parameters": _entry_parameters_for_candidate(candidate, validated, assets),
        }
        record_id = f"candidate__{candidate_id}"
        trials[record_id] = (
            "visual_candidate",
            candidate_id,
            canonical_sha256(candidate),
            _preselection_trial(
                record_id=record_id,
                mandatory_entries=mandatory_entries,
                tested_entry=entry,
                tested_source_kind="visual_candidate",
                tested_source_id=candidate_id,
                validated=validated,
            ),
        )

    resource_feasibility: list[dict[str, Any]] = []
    for record_id in sorted(trials, key=lambda value: value.encode("utf-8")):
        source_kind, source_id, source_record_sha, trial = trials[record_id]
        checks = _trial_resource_checks(trial, capacity_by_hash_kind)
        fits = all(bool(check["fits"]) for check in checks)
        resource_feasibility.append(
            {
                "record_id": record_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "source_record_sha256": source_record_sha,
                "trial_sha256": canonical_sha256(trial),
                "checks": checks,
                "outcome": "eligible" if fits else "rejected",
                "reason_codes": ["resource_feasible" if fits else "resource_capacity"],
            }
        )

    cardinality_limits = _cardinality_limit_rows(assets)
    preselection_limits = [
        row
        for row in cardinality_limits
        if row["evaluation_stage"] == "preselection_reservation"
    ]
    cardinality_feasibility: list[dict[str, Any]] = []
    for record_id in sorted(trials, key=lambda value: value.encode("utf-8")):
        source_kind, source_id, source_record_sha, trial = trials[record_id]
        facet_count_by_id = {
            str(row["facet_id"]): int(row["count"])
            for row in trial["literal_facet_counts"]
        }
        results = []
        for limit in preselection_limits:
            if limit["metric_id"] == "literal_realization_atoms_total":
                fits = int(trial["literal_total"]) <= int(limit["maximum"])
            else:
                fits = all(
                    count <= int(limit["maximum"])
                    for count in facet_count_by_id.values()
                )
            results.append({"limit_id": str(limit["record_id"]), "fits": fits})
        fits = all(bool(item["fits"]) for item in results)
        cardinality_feasibility.append(
            {
                "record_id": record_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "source_record_sha256": source_record_sha,
                "trial_sha256": canonical_sha256(trial),
                "limit_results": results,
                "outcome": "eligible" if fits else "rejected",
                "reason_codes": ["cardinality_feasible" if fits else "cardinality_limit"],
            }
        )
    if next(row for row in resource_feasibility if row["record_id"] == "mandatory_literal__base")["outcome"] != "eligible":
        raise SelectionError("mandatory literal resource reservation is infeasible")
    if next(row for row in cardinality_feasibility if row["record_id"] == "mandatory_literal__base")["outcome"] != "eligible":
        raise SelectionError("mandatory literal cardinality reservation is infeasible")

    policy_sources = _policy_source_contract_rows(assets)
    policy_decisions = _preselection_policy_decision_rows(
        validated=validated,
        matched_prop_ids=matched_prop_ids,
        assets=assets,
    )
    guard_sources = _guard_source_contract_rows(assets)
    inventory = {
        "proposal_profile_ids": _utf8_sorted(
            str(profile["id"]) for profile in assets.candidates["proposal_profiles"]
        ),
        "visual_candidate_ids": _utf8_sorted(
            str(candidate["id"]) for candidate in visual_candidates
        ),
        "guard_candidate_ids": _utf8_sorted(assets.compatibility["guard_candidate_ids"]),
        "policy_source_record_ids": [row["record_id"] for row in policy_sources],
        "preselection_policy_decision_ids": [row["record_id"] for row in policy_decisions],
        "resource_feasibility_record_ids": [row["record_id"] for row in resource_feasibility],
        "cardinality_limit_ids": [row["record_id"] for row in cardinality_limits],
        "cardinality_feasibility_record_ids": [row["record_id"] for row in cardinality_feasibility],
    }
    trace: dict[str, Any] = {
        "schema": CREATIVITY_INVARIANT_TRACE_SCHEMA,
        "request_sha256": validated.request_sha256,
        "scene_contract_sha256": validated.sha256,
        "asset_hashes": dict(assets.asset_hashes),
        "reason_code_registry": list(DECISION_REASON_CODE_IDS),
        "inventory": inventory,
        "eligible_proposals": eligible_proposals,
        "rejected_proposals": rejected_proposals,
        "eligible_candidate_ids": eligible_candidate_ids,
        "rejected_candidates": rejected_candidates,
        "matched_prop_sense_hashes": _matched_prop_sense_occurrence_hashes(validated, assets),
        "policy_source_contracts": policy_sources,
        "preselection_policy_decisions": policy_decisions,
        "resource_capacities": capacity_rows,
        "resource_feasibility": resource_feasibility,
        "cardinality_limits": cardinality_limits,
        "cardinality_feasibility": cardinality_feasibility,
        "guard_source_contracts": guard_sources,
        "guard_source_contracts_sha256": canonical_sha256(guard_sources),
        "complete_trace": True,
    }
    trace["trace_sha256"] = _trace_self_hash(trace)
    return trace, mandatory_entries


def _revalidate_creativity_invariant_trace(
    stored_trace: Mapping[str, Any],
    *,
    validated: ValidatedSceneContract,
    eligibility_roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    expected, mandatory_entries = _build_creativity_invariant_trace(
        validated=validated,
        eligibility_roles=eligibility_roles,
        matched_prop_ids=matched_prop_ids,
        assets=assets,
    )
    if dict(stored_trace) != expected:
        raise SelectionError(
            "selection creativity-invariant trace does not independently reproduce"
        )
    return expected, mandatory_entries


def _selected_candidate_roster_projection(
    *,
    selection: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
    context_overlay_pairs: Sequence[tuple[str, str]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    context_profiles_by_instance: dict[str, set[str]] = {}
    for profile_id, instance_id in context_overlay_pairs:
        context_profiles_by_instance.setdefault(str(instance_id), set()).add(
            str(profile_id)
        )
    rows: list[dict[str, Any]] = []
    for selection_ordinal, atom in enumerate(selection["atoms"]):
        instance_id = str(atom["instance_id"])
        candidate_id = str(atom["candidate_id"])
        facet_id = str(atom["facet"])
        parameters = atom["parameters"]
        proposal_id = parameters.get("proposal_id")
        proposal_primary = bool(
            proposal_id is not None
            and str(assets.proposal_by_id[str(proposal_id)]["candidate_ids"][0])
            == candidate_id
        )
        literal_profile_id = parameters.get("literal_realization_profile_id")
        mandatory_literal = literal_profile_id is not None
        source_slot_id = parameters.get("source_slot_id")
        fixed_realization = (
            _derived_facet_state(facet_id, validated) == "fixed"
            or (
                source_slot_id in SCENE_SLOT_IDS
                and validated.slot_by_id[str(source_slot_id)]["state"] == "fixed"
            )
        )
        core_anchor = candidate_id == "usl_core_identity_anchor"
        context_profile_ids = _utf8_sorted(
            context_profiles_by_instance.get(instance_id, set())
        )
        context_carrier = bool(context_profile_ids)
        authority_refs: list[dict[str, str]] = []
        if mandatory_literal:
            authority_refs.append(
                {
                    "kind": "literal_realization_profile",
                    "source_id": str(literal_profile_id),
                }
            )
        if fixed_realization:
            if source_slot_id in SCENE_SLOT_IDS:
                authority_refs.append(
                    {"kind": "fixed_slot", "source_id": str(source_slot_id)}
                )
            elif facet_id in SCENE_SLOT_IDS:
                authority_refs.append(
                    {"kind": "fixed_slot", "source_id": facet_id}
                )
            elif facet_id == "phase" and validated.role_by_id["phase"]["state"] == "fixed":
                authority_refs.append({"kind": "fixed_role", "source_id": "phase"})
        if core_anchor:
            authority_refs.append(
                {
                    "kind": "core_anchor_candidate",
                    "source_id": "usl_core_identity_anchor",
                }
            )
        authority_refs.extend(
            {"kind": "context_profile", "source_id": profile_id}
            for profile_id in context_profile_ids
        )
        if proposal_primary:
            authority_refs.append(
                {"kind": "proposal_profile", "source_id": str(proposal_id)}
            )
        authority_refs = sorted(
            {
                (item["kind"], item["source_id"]): item
                for item in authority_refs
            }.values(),
            key=lambda item: (item["kind"].encode("utf-8"), item["source_id"].encode("utf-8")),
        )
        rows.append(
            {
                "selection_ordinal": selection_ordinal,
                "instance_id": instance_id,
                "candidate_id": candidate_id,
                "facet_id": facet_id,
                "proposal_primary": proposal_primary,
                "protection_flags": {
                    "mandatory_literal": mandatory_literal,
                    "fixed_realization": fixed_realization,
                    "core_anchor": core_anchor,
                    "context_carrier": context_carrier,
                },
                "authority_refs": authority_refs,
            }
        )
    if len({row["instance_id"] for row in rows}) != len(rows):
        raise SelectionError("selected candidate roster has duplicate instance IDs")
    payload = {
        "schema": "illustration-universal-scene-selected-candidate-roster/v1",
        "rows": rows,
    }
    return payload, rows


def _candidate_roster_subprojections(
    roster_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    protected_counts: dict[tuple[Any, ...], int] = {}
    proposal_counts: dict[str, int] = {}
    optional_rows: list[dict[str, Any]] = []
    for row in roster_rows:
        flags = row["protection_flags"]
        protected = any(bool(value) for value in flags.values())
        if protected:
            key = (
                str(row["candidate_id"]),
                bool(flags["mandatory_literal"]),
                bool(flags["fixed_realization"]),
                bool(flags["core_anchor"]),
                bool(flags["context_carrier"]),
            )
            protected_counts[key] = protected_counts.get(key, 0) + 1
        elif row["proposal_primary"]:
            candidate_id = str(row["candidate_id"])
            proposal_counts[candidate_id] = proposal_counts.get(candidate_id, 0) + 1
        else:
            optional_rows.append(
                {
                    "selection_ordinal": int(row["selection_ordinal"]),
                    "instance_id": str(row["instance_id"]),
                    "candidate_id": str(row["candidate_id"]),
                    "facet_id": str(row["facet_id"]),
                }
            )
    protected_rows = [
        {
            "candidate_id": key[0],
            "mandatory_literal": key[1],
            "fixed_realization": key[2],
            "core_anchor": key[3],
            "context_carrier": key[4],
            "occurrence_count": count,
        }
        for key, count in sorted(protected_counts.items())
    ]
    proposal_rows = [
        {"candidate_id": candidate_id, "occurrence_count": occurrence_count}
        for candidate_id, occurrence_count in sorted(proposal_counts.items())
    ]
    return (
        {
            "schema": "illustration-universal-scene-protected-candidate-roster/v1",
            "rows": protected_rows,
        },
        {
            "schema": "illustration-universal-scene-proposal-primary-roster/v1",
            "rows": proposal_rows,
        },
        {
            "schema": "illustration-universal-scene-optional-candidate-roster/v1",
            "rows": optional_rows,
        },
    )


def _fixed_contract_projection(validated: ValidatedSceneContract) -> dict[str, Any]:
    return {
        "schema": "illustration-universal-scene-fixed-contract/v1",
        "identity_core": _deep_canonical_copy(validated.contract["identity_core"]),
        "participant_bindings": _deep_canonical_copy(validated.contract["participant_bindings"]),
        "slot_states": _deep_canonical_copy(validated.contract["slot_states"]),
        "event_roles": _deep_canonical_copy(validated.contract["event_roles"]),
        "context_profile": _deep_canonical_copy(validated.contract["context_profile"]),
    }


def _resolved_proposal_event_role_value(
    profile: Mapping[str, Any],
    role_id: str,
    validated: ValidatedSceneContract,
) -> str | None:
    raw_value = profile["event_roles"][role_id]
    if raw_value is None:
        return None
    if raw_value == "$identity_actor":
        return _actor_role_value(validated)
    if raw_value == "$scene_location":
        return _scene_location_value(validated)
    return str(raw_value)


def _serialized_atom_role_binding_matches(
    atom: Mapping[str, Any],
    candidate: Mapping[str, Any],
    role_id: str,
    value_id: str,
) -> bool:
    authored = [
        str(requirement)
        for binding_role_id, requirement in candidate["runtime_contract"]["bindings"]
        if binding_role_id == role_id
    ]
    serialized = [
        binding
        for binding in atom["bindings"]
        if str(binding["role_id"]) == role_id
    ]
    if len(authored) != 1 or len(serialized) != 1:
        return False
    expected_requirement = "required" if authored[0] == "event_spine" else authored[0]
    return (
        str(serialized[0]["node_id"]) == value_id
        and str(serialized[0]["requirement"]) == expected_requirement
    )


def _serialized_bridge_role_binding_matches(
    bridge: Mapping[str, Any],
    role_id: str,
    value_id: str,
    *,
    selection: Mapping[str, Any],
    assets: UniversalSceneAssets,
) -> bool:
    bridge_type = str(bridge["bridge_type"])
    candidate = assets.candidate_by_id.get(str(bridge["candidate_id"]))
    if (
        candidate is None
        or bridge_type not in candidate["runtime_contract"]["bridge_types"]
    ):
        return False
    edge_by_id = {
        str(edge["edge_id"]): edge
        for edge in selection["selected_event"]["spine_edges"]
    }
    event_edge_ids = [str(edge_id) for edge_id in bridge["event_edge_ids"]]
    if not event_edge_ids or len(event_edge_ids) != len(set(event_edge_ids)):
        return False
    if any(
        edge_id not in edge_by_id
        or edge_by_id[edge_id] != {
            "edge_id": edge_id,
            "from_node_id": str(bridge["from_node_id"]),
            "relation_id": f"bridge:{bridge_type}",
            "to_node_id": str(bridge["to_node_id"]),
        }
        for edge_id in event_edge_ids
    ):
        return False
    if role_id == "target":
        return (
            bridge_type in MEDIATION_BRIDGE_TYPES
            and str(bridge["to_node_id"]) == value_id
        ) or (
            bridge_type in EXIT_BRIDGE_TYPES
            and str(bridge["from_node_id"]) == value_id
        )
    if role_id == "result":
        return (
            bridge_type in EXIT_BRIDGE_TYPES
            and str(bridge["to_node_id"]) == value_id
        )
    return False


def _runtime_selected_role_authority(
    role: Mapping[str, Any],
    *,
    selection: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> tuple[str, str | None, str | None]:
    role_id = str(role["role_id"])
    value_id = role["value_id"]
    source_id = str(role["source_id"])
    atom_by_id = {
        str(atom["instance_id"]): atom for atom in selection["atoms"]
    }
    bridge_by_id = {
        str(bridge["bridge_id"]): bridge for bridge in selection["bridges"]
    }
    selected_proposal_atoms = [
        atom for atom in selection["atoms"] if "proposal_id" in atom["parameters"]
    ]

    if role_id == "actor":
        expected_source_id = f"identity_entity:{_actor_entity_id(validated)}"
        if source_id != expected_source_id or value_id != _actor_role_value(validated):
            raise SelectionError("runtime-selected actor lacks its exact identity anchor")
        return "identity_anchor", _actor_entity_id(validated), canonical_sha256(
            {
                "participant": validated.participant_by_role["actor"],
                "entity": validated.entity_by_id[_actor_entity_id(validated)],
            }
        )

    source_atom = atom_by_id.get(source_id)
    proposal_authorities = [
        (atom, assets.proposal_by_id[str(atom["parameters"]["proposal_id"])])
        for atom in selected_proposal_atoms
        if _resolved_proposal_event_role_value(
            assets.proposal_by_id[str(atom["parameters"]["proposal_id"])],
            role_id,
            validated,
        )
        == value_id
    ]
    if proposal_authorities and (
        len(proposal_authorities) != 1 or proposal_authorities[0][0] is not source_atom
    ):
        raise SelectionError(
            f"runtime-selected role {role_id} was swapped away from its exact proposal event-frame source"
        )
    if source_atom is not None and "proposal_id" in source_atom["parameters"]:
        proposal_id = str(source_atom["parameters"]["proposal_id"])
        profile = assets.proposal_by_id.get(proposal_id)
        proposal_atoms = [
            atom
            for atom in selection["atoms"]
            if str(atom["parameters"].get("proposal_id", "")) == proposal_id
        ]
        if (
            profile is None
            or len(proposal_atoms) != 1
            or proposal_atoms[0] is not source_atom
            or str(source_atom["candidate_id"]) != str(profile["candidate_ids"][0])
            or _resolved_proposal_event_role_value(profile, role_id, validated)
            != value_id
        ):
            raise SelectionError(
                f"runtime-selected role {role_id} does not resolve from its exact proposal event frame"
            )
        return "proposal_event_frame", proposal_id, canonical_sha256(profile)

    if value_id is None:
        return "none", None, None

    value_id_string = str(value_id)
    if source_atom is not None:
        candidate_id = str(source_atom["candidate_id"])
        candidate = assets.candidate_by_id.get(candidate_id)
        if (
            candidate is None
            or (
                role_id in {"action", "phase"}
                and candidate_id != value_id_string
            )
            or not _serialized_atom_role_binding_matches(
                source_atom, candidate, role_id, value_id_string
            )
        ):
            raise SelectionError(
                f"runtime-selected role {role_id} source atom does not declare and serialize its exact role/value binding"
            )
        return "selected_candidate_binding", candidate_id, canonical_sha256(candidate)

    source_bridge = bridge_by_id.get(source_id)
    if source_bridge is not None:
        if not _serialized_bridge_role_binding_matches(
            source_bridge,
            role_id,
            value_id_string,
            selection=selection,
            assets=assets,
        ):
            raise SelectionError(
                f"runtime-selected role {role_id} source bridge does not own its exact typed endpoint"
            )
        matching_bridges = [
            bridge
            for bridge in selection["bridges"]
            if _serialized_bridge_role_binding_matches(
                bridge,
                role_id,
                value_id_string,
                selection=selection,
                assets=assets,
            )
        ]
        if (
            not matching_bridges
            or str(matching_bridges[0]["bridge_id"]) != source_id
        ):
            raise SelectionError(
                f"runtime-selected role {role_id} does not cite the canonical exact typed bridge endpoint"
            )
        return (
            "bridge_binding",
            source_id,
            canonical_sha256(
                assets.candidate_by_id[str(source_bridge["candidate_id"])]
            ),
        )

    if source_id.startswith("identity_entity:"):
        raise SelectionError(
            f"runtime-selected role {role_id} cannot borrow an identity anchor"
        )
    raise SelectionError(f"runtime-selected role {role_id} lacks an exact selected source")


def _rebind_bridge_owned_runtime_roles(
    roles: dict[str, dict[str, Any]],
    *,
    validated: ValidatedSceneContract,
    atoms: Sequence[Mapping[str, Any]],
    bridges: Sequence[Mapping[str, Any]],
    spine_edges: Sequence[Mapping[str, Any]],
    assets: UniversalSceneAssets,
) -> None:
    atom_by_id = {str(atom["instance_id"]): atom for atom in atoms}
    for role_id in ("target", "result"):
        role = roles.get(role_id)
        if (
            role is None
            or role["source"] != "runtime_selected"
            or role["value_id"] is None
        ):
            continue
        source_atom = atom_by_id.get(str(role["source_id"]))
        if source_atom is not None:
            proposal_id = source_atom["parameters"].get("proposal_id")
            if proposal_id is not None:
                profile = assets.proposal_by_id[str(proposal_id)]
                if _resolved_proposal_event_role_value(
                    profile, role_id, validated
                ) == role["value_id"]:
                    continue
            candidate = assets.candidate_by_id[str(source_atom["candidate_id"])]
            if any(
                binding_role_id == role_id
                for binding_role_id, _ in candidate["runtime_contract"]["bindings"]
            ):
                continue
        matching_bridges = [
            bridge
            for bridge in bridges
            if _serialized_bridge_role_binding_matches(
                bridge,
                role_id,
                str(role["value_id"]),
                selection={
                    "selected_event": {"spine_edges": spine_edges},
                    "atoms": atoms,
                    "bridges": bridges,
                },
                assets=assets,
            )
        ]
        if matching_bridges:
            role["source_id"] = str(matching_bridges[0]["bridge_id"])


def _role_projection_payloads(
    *,
    selection: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime_roles = {
        str(role["role_id"]): role for role in selection["selected_event"]["roles"]
    }
    contract_rows = [
        {
            "role_id": role_id,
            "state": str(validated.role_by_id[role_id]["state"]),
            "contract_value_id": (
                str(validated.role_by_id[role_id]["value_id"])
                if validated.role_by_id[role_id]["state"] == "fixed"
                else None
            ),
        }
        for role_id in EVENT_ROLE_IDS
    ]
    protected_rows: list[dict[str, Any]] = []
    for role_id in EVENT_ROLE_IDS:
        contract_role = validated.role_by_id[role_id]
        state = str(contract_role["state"])
        if state not in {"fixed", "closed"} and role_id not in {"actor", "location"}:
            continue
        runtime_value = runtime_roles[role_id]["value_id"]
        if state == "fixed":
            authority_kind = "contract_fixed"
            authority_source = contract_role
        elif state == "closed":
            authority_kind = "contract_closed"
            authority_source = contract_role
        elif role_id == "actor":
            authority_kind = "identity_anchor"
            authority_source = {
                "participant": validated.participant_by_role["actor"],
                "entity": validated.entity_by_id[_actor_entity_id(validated)],
            }
        else:
            authority_kind = "location_anchor"
            authority_source = {
                "participant": validated.participant_by_role["location"],
                "environment_slot": validated.slot_by_id["environment"],
            }
        protected_rows.append(
            {
                "role_id": role_id,
                "contract_state": state,
                "runtime_value_id": runtime_value,
                "authority_kind": authority_kind,
                "authority_source_sha256": canonical_sha256(authority_source),
            }
        )

    proposal_atom = next(
        (atom for atom in selection["atoms"] if "proposal_id" in atom["parameters"]),
        None,
    )
    proposal_profile = (
        assets.proposal_by_id[str(proposal_atom["parameters"]["proposal_id"])]
        if proposal_atom is not None
        else None
    )
    open_rows: list[dict[str, Any]] = []
    for role_id in ("action", "target", "instrument", "recipient", "result", "phase"):
        if validated.role_by_id[role_id]["state"] != "open":
            continue
        role = runtime_roles[role_id]
        value_id = role["value_id"]
        source_id = str(role["source_id"])
        authority_kind = "none"
        authority_record_id: str | None = None
        authority_source_sha256: str | None = None
        if (
            value_id is None
            and proposal_profile is not None
            and proposal_profile["event_roles"][role_id] is None
        ):
            authority_kind = "proposal_event_frame"
            authority_record_id = str(proposal_profile["id"])
            authority_source_sha256 = canonical_sha256(proposal_profile)
        elif value_id is not None:
            (
                authority_kind,
                authority_record_id,
                authority_source_sha256,
            ) = _runtime_selected_role_authority(
                role,
                selection=selection,
                validated=validated,
                assets=assets,
            )
        open_rows.append(
            {
                "role_id": role_id,
                "runtime_value_id": value_id,
                "authority_kind": authority_kind,
                "authority_record_id": authority_record_id,
                "authority_source_sha256": authority_source_sha256,
            }
        )
    open_rows.sort(key=lambda row: row["role_id"].encode("utf-8"))
    return (
        {"schema": "illustration-universal-scene-contract-roles/v1", "rows": contract_rows},
        {"schema": "illustration-universal-scene-protected-final-roles/v1", "rows": protected_rows},
        {"schema": "illustration-universal-scene-runtime-open-roles/v1", "rows": open_rows},
    )


def _protected_scene_facts_projection(
    *, selection: Mapping[str, Any], validated: ValidatedSceneContract
) -> dict[str, Any]:
    return {
        "schema": "illustration-universal-scene-protected-scene-facts/v1",
        "identity_entities": [
            {
                "entity_id": str(entity["entity_id"]),
                "quantity": int(entity["quantity"]),
                "embodiment_profile_id": str(entity["embodiment_profile_id"]),
            }
            for entity in sorted(
                validated.contract["identity_core"]["entities"],
                key=lambda item: str(item["entity_id"]).encode("utf-8"),
            )
        ],
        "identity_feature_fact_ids": [
            {
                "entity_id": str(entity["entity_id"]),
                "fact_ids": _utf8_sorted(fact["id"] for fact in entity["feature_facts"]),
            }
            for entity in sorted(
                validated.contract["identity_core"]["entities"],
                key=lambda item: str(item["entity_id"]).encode("utf-8"),
            )
        ],
        "participant_bindings": _deep_canonical_copy(
            validated.contract["participant_bindings"]
        ),
        "capability_capacities": [
            {
                "entity_id": str(record["entity_id"]),
                "resource_kind": str(record["resource_kind"]),
                "capacity": int(record["capacity"]),
                "state": str(record["state"]),
            }
            for record in sorted(
                validated.capability_capacities,
                key=lambda item: (
                    str(item["entity_id"]).encode("utf-8"),
                    str(item["resource_kind"]).encode("utf-8"),
                ),
            )
        ],
        "asserted_scene_fact_ids": _utf8_sorted(
            fact["id"] for fact in validated.contract["identity_core"]["scene_facts"]
        ),
        "forbidden_fact_results": [
            {"fact_id": str(fact["id"]), "selected_truth": False}
            for fact in sorted(
                validated.contract["identity_core"]["forbidden_facts"],
                key=lambda item: str(item["id"]).encode("utf-8"),
            )
        ],
    }


def _final_resource_projection(
    selection: Mapping[str, Any], validated: ValidatedSceneContract
) -> tuple[list[dict[str, Any]], bool]:
    capacities = _resource_capacities(validated)
    exclusive: dict[tuple[str, str], int] = {}
    shared: dict[tuple[str, str], int] = {}
    for claim in selection["resource_claims"]:
        key = (str(claim["owner_id"]), str(claim["resource_kind"]))
        if claim["mode"] == "exclusive":
            exclusive[key] = exclusive.get(key, 0) + int(claim["amount"])
        else:
            shared[key] = max(shared.get(key, 0), int(claim["amount"]))
    rows = [
        {
            "owner_scope_hash": _owner_scope_hash(owner_id, validated),
            "resource_kind": resource_kind,
            "exclusive_required": exclusive.get((owner_id, resource_kind), 0),
            "shared_required": shared.get((owner_id, resource_kind), 0),
        }
        for owner_id, resource_kind in set(exclusive) | set(shared)
    ]
    rows.sort(key=lambda row: (row["owner_scope_hash"], row["resource_kind"]))
    fits = all(
        exclusive.get(key, 0) + shared.get(key, 0) <= capacities.get(key, 0)
        for key in set(exclusive) | set(shared)
    )
    return rows, fits


def _pixel_and_bridge_projections(
    *,
    selection: Mapping[str, Any],
    roster_rows: Sequence[Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: UniversalSceneAssets,
    validated: ValidatedSceneContract,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], bool]:
    roster_by_instance = {str(row["instance_id"]): row for row in roster_rows}
    atom_ids = set(roster_by_instance)
    bridge_ids = {str(bridge["bridge_id"]) for bridge in selection["bridges"]}
    scale_order = ("native", "thumbnail_320px", "thumbnail_640px")
    pixel_rows: list[dict[str, Any]] = []
    item_ids: set[str] = set()
    for item in selection["pixel_evidence_contract"]["items"]:
        item_id = str(item["item_id"])
        if item_id in item_ids:
            raise SelectionError(f"duplicate pixel evidence item ID: {item_id}")
        item_ids.add(item_id)
        source_kind = str(item["source_kind"])
        source_id = str(item["source_id"])
        if source_kind == "atom" and source_id in atom_ids:
            owner_kind, owner_id = "candidate_atom", source_id
        elif source_kind == "bridge" and source_id in bridge_ids:
            owner_kind, owner_id = "bridge", source_id
        else:
            owner_kind, owner_id = "protected_scene", source_id
        scales = list(item["minimum_scale_ids"])
        if (
            not scales
            or len(scales) != len(set(scales))
            or any(scale not in scale_order for scale in scales)
            or scales != [scale for scale in scale_order if scale in scales]
            or item["status"] != "future_review_required"
            or item["kind"] not in PIXEL_EVIDENCE_KIND_IDS
        ):
            raise SelectionError(f"pixel evidence row has an invalid closed field: {item_id}")
        pixel_rows.append(
            {
                "owner_kind": owner_kind,
                "owner_id": owner_id,
                "item_id": item_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "kind": str(item["kind"]),
                "minimum_scale_ids": scales,
                "status": "future_review_required",
            }
        )
    pixel_rows.sort(
        key=lambda row: tuple(
            str(row[key]).encode("utf-8")
            for key in ("owner_kind", "owner_id", "item_id", "source_kind", "source_id", "kind")
        )
    )

    protected_atom_ids = {
        str(row["instance_id"])
        for row in roster_rows
        if any(bool(value) for value in row["protection_flags"].values())
    }
    bridge_rows: list[dict[str, Any]] = []
    protected_bridge_ids: set[str] = set()
    for bridge in sorted(selection["bridges"], key=lambda item: str(item["bridge_id"]).encode("utf-8")):
        bridge_id = str(bridge["bridge_id"])
        bridge_type = str(bridge["bridge_type"])
        prefix = f"bridge_{bridge_type}_"
        suffix = bridge_id.removeprefix(prefix)
        occurrence_text, separator, owner_label = suffix.partition("_")
        if not separator or not occurrence_text.isdigit() or int(occurrence_text) <= 0:
            raise SelectionError(f"bridge ID lacks owner-local occurrence: {bridge_id}")
        owner_atom = next(
            (
                atom_id
                for atom_id in sorted(atom_ids, key=len, reverse=True)
                if owner_label == atom_id
            ),
            None,
        )
        if owner_atom is not None:
            roster = roster_by_instance[owner_atom]
            premise_owner = {
                "owner_kind": "candidate_atom",
                "owner_id": owner_atom,
                "source_id": str(roster["candidate_id"]),
                "source_record_sha256": canonical_sha256(
                    assets.candidate_by_id[str(roster["candidate_id"])]
                ),
                "proposal_primary": bool(roster["proposal_primary"]),
                "protection_flags": _deep_canonical_copy(roster["protection_flags"]),
            }
            if owner_atom in protected_atom_ids:
                protected_bridge_ids.add(bridge_id)
        elif owner_label.startswith("fixed_"):
            prop_id = owner_label.removeprefix("fixed_")
            if prop_id not in matched_prop_ids:
                raise SelectionError(f"bridge fixed-prop owner is unauthenticated: {bridge_id}")
            premise_owner = {
                "owner_kind": "fixed_prop",
                "owner_id": f"fixed_prop:{prop_id}",
                "source_id": prop_id,
                "source_record_sha256": canonical_sha256(assets.prop_by_id[prop_id]),
                "proposal_primary": False,
                "protection_flags": {
                    "mandatory_literal": False,
                    "fixed_realization": True,
                    "core_anchor": False,
                    "context_carrier": False,
                },
            }
            protected_bridge_ids.add(bridge_id)
        else:
            raise SelectionError(f"bridge lacks an authenticated premise owner: {bridge_id}")
        owned_pixels = [
            row
            for row in pixel_rows
            if row["owner_kind"] == "bridge" and row["owner_id"] == bridge_id
        ]
        owned_pixel_payload = {
            "schema": "illustration-universal-scene-owner-pixel-evidence/v1",
            "owner_kind": "bridge",
            "owner_id": bridge_id,
            "rows": [
                {
                    key: row[key]
                    for key in (
                        "item_id",
                        "source_kind",
                        "source_id",
                        "kind",
                        "minimum_scale_ids",
                        "status",
                    )
                }
                for row in sorted(
                    owned_pixels,
                    key=lambda item: tuple(
                        str(item[key]).encode("utf-8")
                        for key in ("item_id", "source_kind", "source_id", "kind")
                    ),
                )
            ],
        }
        bridge_rows.append(
            {
                "bridge_id": bridge_id,
                "bridge_type": bridge_type,
                "owner_local_occurrence": int(occurrence_text),
                "candidate_id": str(bridge["candidate_id"]),
                "bridge_source_record_sha256": canonical_sha256(
                    assets.candidate_by_id[str(bridge["candidate_id"])]
                ),
                "premise_owner": premise_owner,
                "from_node_id": str(bridge["from_node_id"]),
                "to_node_id": str(bridge["to_node_id"]),
                "event_edge_ids": _utf8_sorted(bridge["event_edge_ids"]),
                "pixel_evidence_ids": _utf8_sorted(bridge["pixel_evidence_ids"]),
                "pixel_owner_projection_sha256": canonical_sha256(owned_pixel_payload),
            }
        )
    protected_pixel_rows = [
        row
        for row in pixel_rows
        if (
            row["owner_kind"] == "protected_scene"
            and (
                row["source_kind"] in {"core_anchor", "event"}
                or (
                    row["source_kind"] == "consequence"
                    and validated.role_by_id["result"]["state"] in {"fixed", "closed"}
                )
            )
        )
        or (row["owner_kind"] == "candidate_atom" and row["owner_id"] in protected_atom_ids)
        or (row["owner_kind"] == "bridge" and row["owner_id"] in protected_bridge_ids)
    ]
    return pixel_rows, bridge_rows, protected_pixel_rows, True


def _postselection_guard_executions(
    *,
    hard_gate_snapshot: Mapping[str, Any],
    invariant_trace: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], bool]:
    source_by_id = {
        str(row["record_id"]): row
        for row in invariant_trace["guard_source_contracts"]
    }
    executions: list[dict[str, Any]] = []
    for old in sorted(
        hard_gate_snapshot["guard_executions"],
        key=lambda row: str(row["guard_id"]).encode("utf-8"),
    ):
        guard_id = str(old["guard_id"])
        source = source_by_id[guard_id]
        applicable = bool(old["applicable"])
        if applicable:
            predicate_result = old["predicate_results"][0]
            passed: bool | None = bool(predicate_result["passed"])
            evidence = {
                "schema": "illustration-universal-scene-guard-predicate-evidence/v1",
                "predicate_id": str(source["predicate_id"]),
                "passed": passed,
                "binding_ids": _utf8_sorted(predicate_result["binding_ids"]),
            }
            outcome = "pass" if passed else "block"
            reasons = [
                "all_guard_predicates_passed" if passed else "guard_predicate_failed"
            ]
        else:
            passed = None
            evidence = []
            outcome = "not_applicable"
            reasons = ["guard_not_applicable"]
        executions.append(
            {
                "guard_id": guard_id,
                "predicate_id": str(source["predicate_id"]),
                "source_contract_sha256": str(source["source_contract_sha256"]),
                "applicable": applicable,
                "predicate_passed": passed,
                "predicate_evidence_sha256": canonical_sha256(evidence),
                "outcome": outcome,
                "reason_codes": reasons,
            }
        )
    hard_gate_pass = (
        len(executions) == len(source_by_id) == 32
        and {row["guard_id"] for row in executions} == set(source_by_id)
        and any(bool(row["applicable"]) for row in executions)
        and all(row["outcome"] != "block" for row in executions)
    )
    return executions, hard_gate_pass


def _selected_policy_decisions(
    *,
    selection: Mapping[str, Any],
    context_overlay_pairs: Sequence[tuple[str, str]],
    invariant_trace: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    decision_by_id = {
        str(row["record_id"]): row
        for row in invariant_trace["preselection_policy_decisions"]
    }
    selected_ids = {
        f"proposal_policy__{atom['parameters']['proposal_id']}"
        for atom in selection["atoms"]
        if "proposal_id" in atom["parameters"]
    }
    selected_ids.update(
        f"context_policy__{profile_id}" for profile_id, _instance_id in context_overlay_pairs
    )
    return [decision_by_id[record_id] for record_id in _utf8_sorted(selected_ids)]


def _universal_rule_execution_rows(
    *,
    selection: Mapping[str, Any],
    validated: ValidatedSceneContract,
    invariant_trace: Mapping[str, Any],
    selected_policy_decisions: Sequence[Mapping[str, Any]],
    final_resource_pass: bool,
    universal_rules: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], bool]:
    policy_source_by_id = {
        str(row["record_id"]): row
        for row in invariant_trace["policy_source_contracts"]
    }
    atom_facets = [str(atom["facet"]) for atom in selection["atoms"]]
    bridge_types = [str(bridge["bridge_type"]) for bridge in selection["bridges"]]
    bridge_pixel_pass = all(bool(bridge["pixel_evidence_ids"]) for bridge in selection["bridges"])
    selected_band = str(selection["semantic_distance_trace"]["selected_band"])
    if selected_band == "middle":
        visible_bridge_violation = not (
            len(set(bridge_types)) >= 2
            and bool(set(bridge_types) & set(ENTRY_BRIDGE_TYPES))
            and bool(set(bridge_types) & set(EXIT_BRIDGE_TYPES))
            and bridge_pixel_pass
        )
    elif selected_band == "far":
        visible_bridge_violation = not (
            len(set(bridge_types)) >= 3
            and bool(set(bridge_types) & set(ENTRY_BRIDGE_TYPES))
            and bool(set(bridge_types) & set(MEDIATION_BRIDGE_TYPES))
            and bool(set(bridge_types) & set(EXIT_BRIDGE_TYPES))
            and bridge_pixel_pass
        )
    else:
        visible_bridge_violation = False
    violations = {
        "rule_fixed_identity_precedence": False,
        "rule_closed_prop": (
            validated.slot_by_id["prop"]["state"] == "closed"
            and any(facet in {"prop", "prop_state"} for facet in atom_facets)
        ),
        "rule_exactly_one_event": selection.get("selected_event") is None,
        "rule_resource_capacity": not final_resource_pass,
        "rule_visible_middle_far_bridge": visible_bridge_violation,
        "rule_remote_budget": int(selection["semantic_distance_trace"]["optional_remote_count"]) > 1,
        "rule_policy_independent_of_creativity": any(
            row["outcome"] != "pass" for row in selected_policy_decisions
        ),
    }
    rows: list[dict[str, Any]] = []
    for rule in sorted(
        universal_rules,
        key=lambda item: str(item["id"]).encode("utf-8"),
    ):
        rule_id = str(rule["id"])
        violated = bool(violations[rule_id])
        source = policy_source_by_id[f"universal_rule__{rule_id}"]
        rows.append(
            {
                "rule_id": rule_id,
                "source_contract_sha256": str(source["source_contract_sha256"]),
                "violated": violated,
                "outcome": "block" if violated else "pass",
                "reason_codes": [
                    str(rule["reason_code"]) if violated else "rule_satisfied"
                ],
            }
        )
    return rows, all(row["outcome"] == "pass" for row in rows)


def _postselection_cardinality_rows(
    *,
    selection: Mapping[str, Any],
    roster_rows: Sequence[Mapping[str, Any]],
    invariant_trace: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], bool, str]:
    atoms = list(selection["atoms"])
    runtime_roles = {
        str(role["role_id"]): role for role in selection["selected_event"]["roles"]
    }
    edge_by_id = {
        str(edge["edge_id"]): edge for edge in selection["selected_event"]["spine_edges"]
    }
    event_root_count = 1 if selection.get("selected_event") is not None else 0
    optional_prop_count = sum(
        row["facet_id"] == "prop"
        and not bool(row["protection_flags"]["mandatory_literal"])
        and not bool(row["proposal_primary"])
        for row in roster_rows
    )
    orphan_count = sum(
        not (
            len(atom["event_edge_ids"]) == 1
            and atom["event_edge_ids"][0] in edge_by_id
            and edge_by_id[atom["event_edge_ids"][0]]["from_node_id"] == "event_01"
            and edge_by_id[atom["event_edge_ids"][0]]["to_node_id"] == atom["instance_id"]
            and edge_by_id[atom["event_edge_ids"][0]]["relation_id"]
            == f"realizes:{atom['facet']}"
        )
        for atom in atoms
    )
    optional_remote = int(selection["semantic_distance_trace"]["optional_remote_count"])
    observed = {
        "display_bundles": int(any(atom["facet"] in {"expression", "perceived_affect"} for atom in atoms)),
        "display_primitives_per_bundle": sum(atom["facet"] in {"expression", "perceived_affect"} for atom in atoms),
        "event_spines": event_root_count,
        "gestures": sum(atom["facet"] == "gesture" for atom in atoms),
        "optional_props": optional_prop_count,
        "orphan_atoms": orphan_count,
        "perceived_affect_hypotheses": sum(atom["facet"] == "perceived_affect" for atom in atoms),
        "phases": len({selection["selected_event"]["phase_id"]}) if selection["selected_event"]["phase_id"] is not None else 0,
        "pose_support_solutions": sum(atom["facet"] == "pose" for atom in atoms),
        "primary_actions": int(runtime_roles["action"]["value_id"] is not None),
        "primary_environment_roles": int(runtime_roles["location"]["value_id"] is not None),
        "relation_topologies": sum(atom["facet"] == "relation" for atom in atoms),
        "remote_or_high_load_optional_premises": optional_remote,
        "second_independent_premises": max(0, event_root_count - 1),
        "context_profile_carriers": sum(
            str(atom["candidate_id"]) in CONTEXT_PROFILE_CARRIER_CANDIDATE_IDS
            for atom in atoms
        ),
        "global_optional_remote": optional_remote,
        "selected_resource_claims_total": len(selection["resource_claims"]),
        "selected_visual_atoms_total": len(atoms),
    }
    limits = [
        row
        for row in invariant_trace["cardinality_limits"]
        if row["evaluation_stage"] == "postselection_scene"
    ]
    rows = [
        {
            "limit_id": str(limit["record_id"]),
            "observed": int(observed[str(limit["metric_id"])]),
            "minimum": int(limit["minimum"]),
            "maximum": int(limit["maximum"]),
            "fits": int(limit["minimum"])
            <= int(observed[str(limit["metric_id"])])
            <= int(limit["maximum"]),
        }
        for limit in limits
    ]
    invariant_rows = _deep_canonical_copy(rows)
    remote_limit_ids = {
        "compatibility_budget__remote_or_high_load_optional_premises",
        "runtime_limit__global_optional_remote",
    }
    for row in invariant_rows:
        if row["limit_id"] in remote_limit_ids:
            row["observed"] = None
    return rows, all(row["fits"] for row in rows), canonical_sha256(invariant_rows)


def _build_postselection_run_trace(
    *,
    selection: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
    matched_prop_ids: set[str],
    context_overlay_pairs: Sequence[tuple[str, str]],
) -> dict[str, Any]:
    invariant_trace = selection["creativity_invariant_trace"]
    roster_payload, roster_rows = _selected_candidate_roster_projection(
        selection=selection,
        validated=validated,
        assets=assets,
        context_overlay_pairs=context_overlay_pairs,
    )
    protected_roster, proposal_roster, optional_roster = (
        _candidate_roster_subprojections(roster_rows)
    )
    contract_roles, protected_roles, runtime_open_roles = _role_projection_payloads(
        selection=selection, validated=validated, assets=assets
    )
    protected_scene_facts = _protected_scene_facts_projection(
        selection=selection, validated=validated
    )
    resource_footprint, resource_pass = _final_resource_projection(
        selection, validated
    )
    pixel_rows, bridge_rows, protected_pixel_rows, pixel_pass = (
        _pixel_and_bridge_projections(
            selection=selection,
            roster_rows=roster_rows,
            matched_prop_ids=matched_prop_ids,
            assets=assets,
            validated=validated,
        )
    )
    active_context_ids = _utf8_sorted(profile_id for profile_id, _ in context_overlay_pairs)
    active_context_payload = {
        "schema": "illustration-universal-scene-active-context-profiles/v1",
        "profile_ids": active_context_ids,
    }
    facet_multiset = [
        {
            "facet_id": facet_id,
            "count": sum(str(atom["facet"]) == facet_id for atom in selection["atoms"]),
        }
        for facet_id in _utf8_sorted(FACET_IDS)
    ]
    semantic_distance = {
        "selected_candidate_distance_vectors": [
            {
                "selection_ordinal": index,
                "instance_id": str(atom["instance_id"]),
                "candidate_id": str(atom["candidate_id"]),
                "vector": _deep_canonical_copy(atom["distance_vector"]),
            }
            for index, atom in enumerate(selection["atoms"])
        ],
        "aggregate_distance_vector": _deep_canonical_copy(
            selection["semantic_distance_trace"]["vector"]
        ),
        "selected_distance_band": str(selection["semantic_distance_trace"]["selected_band"]),
        "fixed_remote_count": int(selection["semantic_distance_trace"]["fixed_remote_count"]),
        "global_optional_remote_max": GLOBAL_OPTIONAL_REMOTE_MAX,
    }
    remote_instance_ids = set(selection["semantic_distance_trace"]["remote_atom_ids"])
    optional_remote_projection = {
        "remote_candidate_ids": _utf8_sorted(
            atom["candidate_id"]
            for atom in selection["atoms"]
            if atom["instance_id"] in remote_instance_ids
        ),
        "optional_remote_count": int(selection["semantic_distance_trace"]["optional_remote_count"]),
    }
    pixel_kind_counts = [
        {"kind": kind, "count": sum(row["kind"] == kind for row in pixel_rows)}
        for kind in _utf8_sorted(PIXEL_EVIDENCE_KIND_IDS)
    ]
    pixel_kind_payload = {
        "schema": "illustration-universal-scene-pixel-kind-multiset/v1",
        "rows": pixel_kind_counts,
    }
    pixel_chain_payload = {
        "schema": "illustration-universal-scene-pixel-evidence-chain/v1",
        "rows": pixel_rows,
    }
    protected_pixel_payload = {
        "schema": "illustration-universal-scene-protected-pixel-evidence/v1",
        "rows": protected_pixel_rows,
    }
    proposal_atoms = [
        atom for atom in selection["atoms"] if "proposal_id" in atom["parameters"]
    ]
    if len(proposal_atoms) > 1:
        raise SelectionError("postselection trace found multiple proposal primaries")
    selected_profile = (
        assets.proposal_by_id[str(proposal_atoms[0]["parameters"]["proposal_id"])]
        if proposal_atoms
        else None
    )
    selected_projection = {
        "fixed_contract_projection_sha256": canonical_sha256(_fixed_contract_projection(validated)),
        "contract_role_projection_sha256": canonical_sha256(contract_roles),
        "protected_final_role_projection_sha256": canonical_sha256(protected_roles),
        "protected_scene_facts_sha256": canonical_sha256(protected_scene_facts),
        "runtime_open_role_projection_sha256": canonical_sha256(runtime_open_roles),
        "selected_semantic_family_signature": (
            str(selected_profile["semantic_family_signature"]) if selected_profile else None
        ),
        "selected_proposal_profile_sha256": (
            hashlib.sha256(str(selected_profile["id"]).encode("utf-8")).hexdigest()
            if selected_profile
            else None
        ),
        "selected_candidate_roster_sha256": canonical_sha256(roster_payload),
        "protected_candidate_roster_sha256": canonical_sha256(protected_roster),
        "proposal_primary_roster_sha256": canonical_sha256(proposal_roster),
        "optional_candidate_roster_sha256": canonical_sha256(optional_roster),
        "active_context_profile_ids_sha256": canonical_sha256(active_context_payload),
        "selected_atom_count": len(selection["atoms"]),
        "selected_facet_multiset": facet_multiset,
        "aggregate_resource_footprint": resource_footprint,
        "resource_claim_count": len(selection["resource_claims"]),
        "mandatory_literal_atom_count": sum(
            bool(row["protection_flags"]["mandatory_literal"]) for row in roster_rows
        ),
        "context_profile_carrier_count": sum(
            str(atom["candidate_id"]) in CONTEXT_PROFILE_CARRIER_CANDIDATE_IDS
            for atom in selection["atoms"]
        ),
        "fixed_remote_count": int(selection["semantic_distance_trace"]["fixed_remote_count"]),
        "optional_remote_count": int(selection["semantic_distance_trace"]["optional_remote_count"]),
        "global_optional_remote_max": GLOBAL_OPTIONAL_REMOTE_MAX,
        "semantic_distance_sha256": canonical_sha256(semantic_distance),
        "optional_remote_projection_sha256": canonical_sha256(optional_remote_projection),
        "bridge_topology_sha256": canonical_sha256(bridge_rows),
        "pixel_evidence_chain_sha256": canonical_sha256(pixel_chain_payload),
        "pixel_evidence_count": len(pixel_rows),
        "pixel_kind_multiset_sha256": canonical_sha256(pixel_kind_payload),
        "protected_pixel_evidence_sha256": canonical_sha256(protected_pixel_payload),
        "pixel_evidence_contract_pass": pixel_pass,
    }
    guard_executions, hard_gate_pass = _postselection_guard_executions(
        hard_gate_snapshot=selection["hard_gate_snapshot"],
        invariant_trace=invariant_trace,
    )
    selected_policy_decisions = _selected_policy_decisions(
        selection=selection,
        context_overlay_pairs=context_overlay_pairs,
        invariant_trace=invariant_trace,
    )
    universal_rules, universal_rules_pass = _universal_rule_execution_rows(
        selection=selection,
        validated=validated,
        invariant_trace=invariant_trace,
        selected_policy_decisions=selected_policy_decisions,
        final_resource_pass=resource_pass,
        universal_rules=assets.compatibility["universal_rules"],
    )
    cardinality_rows, cardinality_pass, cardinality_invariant_sha = (
        _postselection_cardinality_rows(
            selection=selection,
            roster_rows=roster_rows,
            invariant_trace=invariant_trace,
        )
    )
    selected_policy_pass = all(row["outcome"] == "pass" for row in selected_policy_decisions)
    policy_gate_pass = selected_policy_pass and universal_rules_pass
    trace: dict[str, Any] = {
        "schema": POSTSELECTION_RUN_TRACE_SCHEMA,
        "invariant_trace_sha256": str(invariant_trace["trace_sha256"]),
        "guard_source_contracts_sha256": str(invariant_trace["guard_source_contracts_sha256"]),
        "selected_projection": selected_projection,
        "guard_executions": guard_executions,
        "guard_executions_sha256": canonical_sha256(guard_executions),
        "hard_gate_pass": hard_gate_pass,
        "universal_rule_executions": universal_rules,
        "universal_rule_executions_sha256": canonical_sha256(universal_rules),
        "postselection_cardinality_decisions": cardinality_rows,
        "postselection_cardinality_decisions_sha256": canonical_sha256(cardinality_rows),
        "postselection_cardinality_invariant_sha256": cardinality_invariant_sha,
        "postselection_resource_pass": resource_pass,
        "policy_gate_pass": policy_gate_pass,
        "cardinality_gate_pass": cardinality_pass,
        "complete_trace": True,
    }
    trace["trace_sha256"] = _trace_self_hash(trace)
    if not (
        hard_gate_pass
        and resource_pass
        and policy_gate_pass
        and cardinality_pass
        and pixel_pass
    ):
        raise SelectionError("postselection trace rejected the selected scene")
    return trace


def _revalidate_postselection_run_trace(
    stored_trace: Mapping[str, Any],
    *,
    selection: Mapping[str, Any],
    validated: ValidatedSceneContract,
    assets: UniversalSceneAssets,
    matched_prop_ids: set[str],
    context_overlay_pairs: Sequence[tuple[str, str]],
) -> dict[str, Any]:
    expected = _build_postselection_run_trace(
        selection=selection,
        validated=validated,
        assets=assets,
        matched_prop_ids=matched_prop_ids,
        context_overlay_pairs=context_overlay_pairs,
    )
    if dict(stored_trace) != expected:
        raise SelectionError(
            "selection postselection-run trace does not independently reproduce"
        )
    return expected


def _guard_predicate_applicable(
    predicate_id: str,
    *,
    selection: Mapping[str, Any],
    assets: UniversalSceneAssets,
    matched_prop_ids: set[str],
    observed_effect_ids: set[str],
) -> bool:
    atoms = list(selection["atoms"])
    facets = {str(atom["facet"]) for atom in atoms}
    topic_ids = {
        str(topic_id)
        for atom in atoms
        for topic_id in assets.candidate_by_id[str(atom["candidate_id"])]["research_topic_ids"]
    }
    compiled_required_predicates = {
        "display_inner_state_not_claimed",
        "event_roles_coherent",
        "weapon_event_safe",
        "resource_capacity_within_declared",
        "narrative_effects_absent",
        "weapon_role_target_safe",
        "prop_literal_sense_bound",
        "relation_event_edges_connected",
        "theme_load_within_limit",
    }
    if predicate_id in compiled_required_predicates:
        return True
    if predicate_id in {
        "display_cues_contextualized",
        "display_inner_state_not_claimed",
    }:
        return "perceived_affect" in facets
    if predicate_id == "attention_intention_not_claimed":
        return "attention" in facets
    if predicate_id in {
        "nonhuman_channel_context_bound",
        "nonhuman_inner_state_not_claimed",
    }:
        return "nonhuman_expression_channels" in topic_ids
    if predicate_id == "facial_motion_inner_state_not_claimed":
        return "observable_facial_motion" in topic_ids
    if predicate_id in {"weapon_event_safe", "weapon_role_target_safe"}:
        return (
            "prop_decommissioned_machine_gun" in matched_prop_ids
            or bool(
                observed_effect_ids
                & {
                    "active_weapon_discharge",
                    "combat_opponent_assignment",
                    "combat_target_assignment",
                }
            )
        )
    if predicate_id == "narrative_effects_absent":
        return bool(
            observed_effect_ids
            & {
                "combat_opponent_assignment",
                "combat_target_assignment",
                "navigation_instrument_use",
                "romantic_contact",
                "scene_promise_hijack",
            }
        ) or bool(facets & {"prop", "relation", "action"})
    if predicate_id in {"gesture_context_bound", "gesture_cultural_emblem_absent"}:
        return "gesture" in facets
    if predicate_id in {"contact_pixel_grounded", "contact_resource_within_capacity"}:
        return "contact" in facets
    if predicate_id == "relation_event_edges_connected":
        return "relation" in facets
    if predicate_id == "remote_premise_has_visible_bridge":
        return bool(selection["semantic_distance_trace"]["remote_atom_ids"])
    if predicate_id == "physical_relation_grounded":
        return bool(facets & {"contact", "relation"})
    if predicate_id == "history_claim_pixel_grounded":
        return "prop_state" in facets
    if predicate_id == "prop_literal_sense_bound":
        return bool(matched_prop_ids)
    if predicate_id == "local_policy_authority_separated":
        return any("proposal_id" in atom["parameters"] for atom in atoms) or any(
            any(predicate[0] == "policy" for predicate in assets.candidate_by_id[str(atom["candidate_id"])]["runtime_contract"]["requires_all"])
            for atom in atoms
        )
    return True


def _build_hard_gate_snapshot(
    *,
    request_text: str,
    selection: Mapping[str, Any],
    assets: UniversalSceneAssets,
    validated: ValidatedSceneContract,
    matched_prop_ids: set[str],
    context_overlay_pairs: Sequence[tuple[str, str]],
) -> dict[str, Any]:
    registry = _require_mapping(
        assets.semantic_bindings["semantic_effect_registry"],
        "semantic_bindings.semantic_effect_registry",
        SelectionError,
    )
    effect_profiles = _semantic_effect_profiles_by_source(assets)
    source_kind_order = {
        kind: index for index, kind in enumerate(SEMANTIC_EFFECT_SOURCE_KIND_IDS)
    }

    def source_ref(source_kind: str, source_id: str) -> dict[str, str]:
        if (source_kind, source_id) not in effect_profiles:
            raise SelectionError(f"selected source lacks semantic effect registry coverage: {source_kind}:{source_id}")
        return {"source_kind": source_kind, "source_id": source_id}

    def ordered_refs(refs: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
        unique = {
            (str(ref["source_kind"]), str(ref["source_id"]))
            for ref in refs
        }
        return [
            {"source_kind": kind, "source_id": source_id}
            for kind, source_id in sorted(
                unique,
                key=lambda item: (source_kind_order[item[0]], item[1]),
            )
        ]

    def resolved_effects(
        refs: Sequence[Mapping[str, str]],
        *,
        subject_ref: str | None,
    ) -> list[dict[str, Any]]:
        effects = sorted(
            {
                effect_id
                for ref in refs
                for effect_id in effect_profiles[(str(ref["source_kind"]), str(ref["source_id"]))]
            }
        )
        return [
            {
                "effect_id": effect_id,
                "source_profile_id": "semantic_effect_registry",
                "subject_ref": subject_ref,
            }
            for effect_id in effects
        ]

    zero_load = {axis: 0 for axis in LOAD_AXIS_IDS}
    atoms = list(selection["atoms"])
    atom_by_id = {str(atom["instance_id"]): atom for atom in atoms}
    selected_refs: list[dict[str, Any]] = []
    actor_entity_id = _actor_entity_id(validated)
    roles = list(selection["selected_event"]["roles"])
    bridges = list(selection["bridges"])
    bridge_by_source_suffix = sorted(
        bridges,
        key=lambda item: str(item["bridge_id"]),
    )

    for role in roles:
        value_id = role["value_id"]
        if value_id is None:
            continue
        refs: list[dict[str, str]] = []
        scope = "contract_projection"
        if role["source"] == "runtime_selected" and str(role["source_id"]) in atom_by_id:
            source_atom = atom_by_id[str(role["source_id"])]
            refs.append(source_ref("visual_candidate", str(source_atom["candidate_id"])))
            scope = "runtime_addition"
        elif role["source"] == "runtime_selected" and not str(role["source_id"]).startswith("identity_entity:"):
            source_bridge = next(
                (
                    bridge
                    for bridge in bridge_by_source_suffix
                    if str(bridge["bridge_id"]).endswith(str(role["source_id"]))
                ),
                None,
            )
            if source_bridge is None:
                raise SelectionError(f"runtime-selected role lacks a typed source: {role['role_id']}")
            refs.extend(
                [
                    source_ref("visual_candidate", str(source_bridge["candidate_id"])),
                    source_ref("bridge_type", str(source_bridge["bridge_type"])),
                ]
            )
            scope = "runtime_addition"
        refs = ordered_refs(refs)
        selected_refs.append(
            {
                "instance_kind": "event_role",
                "instance_id": str(role["role_id"]),
                "scope": scope,
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(
                    refs,
                    subject_ref=actor_entity_id if role["role_id"] == "actor" else None,
                ),
                "load_vector": dict(zero_load),
            }
        )

    for prop_id in sorted(matched_prop_ids):
        prop = assets.prop_by_id[prop_id]
        source_candidate_id = next(
            (
                str(candidate_id)
                for candidate_id in prop["affordance_candidate_ids"]
                if candidate_id in assets.candidate_by_id
                and assets.candidate_by_id[candidate_id]["role"] == "visual_atom"
            ),
            None,
        )
        if source_candidate_id is None:
            raise SelectionError(f"fixed catalog prop lacks a reviewed visual source: {prop_id}")
        refs = ordered_refs([source_ref("visual_candidate", source_candidate_id)])
        selected_refs.append(
            {
                "instance_kind": "fixed_prop",
                "instance_id": prop_id,
                "scope": "contract_projection",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, subject_ref=actor_entity_id),
                "load_vector": dict(prop["base_load_profile"]),
            }
        )

    for atom in atoms:
        refs = ordered_refs(
            [source_ref("visual_candidate", str(atom["candidate_id"]))]
        )
        selected_refs.append(
            {
                "instance_kind": "atom",
                "instance_id": str(atom["instance_id"]),
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, subject_ref=actor_entity_id),
                "load_vector": dict(atom["load_vector"]),
            }
        )

    for bridge in bridges:
        refs = ordered_refs(
            [
                source_ref("visual_candidate", str(bridge["candidate_id"])),
                source_ref("bridge_type", str(bridge["bridge_type"])),
            ]
        )
        candidate_load = assets.candidate_by_id[str(bridge["candidate_id"])]["runtime_contract"]["load_profile"]
        selected_refs.append(
            {
                "instance_kind": "bridge",
                "instance_id": str(bridge["bridge_id"]),
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, subject_ref=actor_entity_id),
                "load_vector": dict(candidate_load),
            }
        )

    for claim in selection["resource_claims"]:
        claimant = atom_by_id.get(str(claim["claimant_id"]))
        if claimant is None:
            raise SelectionError(f"resource claim lacks selected claimant atom: {claim['claim_id']}")
        refs = ordered_refs(
            [
                source_ref("resource_kind", str(claim["resource_kind"])),
                source_ref("visual_candidate", str(claimant["candidate_id"])),
            ]
        )
        subject_ref = None if claim["owner_id"] == "scene" else str(claim["owner_id"])
        selected_refs.append(
            {
                "instance_kind": "resource_claim",
                "instance_id": str(claim["claim_id"]),
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, subject_ref=subject_ref),
                "load_vector": dict(claimant["load_vector"]),
            }
        )

    proposal_atoms = [atom for atom in atoms if "proposal_id" in atom["parameters"]]
    if len(proposal_atoms) > 1:
        raise SelectionError("hard-gate snapshot found multiple selected proposal atoms")
    for atom in proposal_atoms:
        proposal_id = str(atom["parameters"]["proposal_id"])
        refs = ordered_refs([source_ref("proposal_profile", proposal_id)])
        profile = next(
            profile
            for profile in assets.candidates["proposal_profiles"]
            if str(profile["id"]) == proposal_id
        )
        selected_refs.append(
            {
                "instance_kind": "proposal",
                "instance_id": proposal_id,
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, subject_ref=actor_entity_id),
                "load_vector": dict(profile["load_profile"]),
            }
        )

    context_by_id = {
        str(profile["id"]): profile
        for profile in assets.candidates["context_distance_profiles"]
    }
    for profile_id, carrier_instance_id in sorted(context_overlay_pairs):
        profile = context_by_id.get(profile_id)
        if profile is None or carrier_instance_id not in atom_by_id:
            raise SelectionError(f"context overlay lacks typed profile/carrier: {profile_id}")
        refs = ordered_refs([source_ref("context_profile", profile_id)])
        selected_refs.append(
            {
                "instance_kind": "context_overlay",
                "instance_id": f"{profile_id}::{carrier_instance_id}",
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, subject_ref=actor_entity_id),
                "load_vector": dict(profile["load_profile"]),
            }
        )

    selected_refs.extend(
        _contract_effect_projection_records(
            request_text=request_text,
            validated=validated,
            assets=assets,
        )
    )

    observed_effect_ids = sorted(
        {
            str(occurrence["effect_id"])
            for item in selected_refs
            for occurrence in item["effect_occurrences"]
        }
    )
    semantic_load_max = _max_vector(
        [item["load_vector"] for item in selected_refs],
        LOAD_AXIS_IDS,
    )
    guard_profiles = {
        str(profile["guard_id"]): str(profile["predicate_id"])
        for profile in assets.semantic_bindings["guard_execution_profiles"]
    }
    guard_executions: list[dict[str, Any]] = []
    for guard_id in sorted(guard_profiles):
        candidate = assets.candidate_by_id[guard_id]
        predicate_id = guard_profiles[guard_id]
        observed_effect_set = set(observed_effect_ids)
        applicable = _guard_predicate_applicable(
            predicate_id,
            selection=selection,
            assets=assets,
            matched_prop_ids=matched_prop_ids,
            observed_effect_ids=observed_effect_set,
        )
        effect_occurrences = [
            occurrence
            for item in selected_refs
            for occurrence in item["effect_occurrences"]
        ]
        if applicable:
            passed, binding_ids = _guard_predicate_result(
                predicate_id,
                selection=selection,
                assets=assets,
                validated=validated,
                matched_prop_ids=matched_prop_ids,
                observed_effect_ids=observed_effect_set,
                effect_occurrences=effect_occurrences,
            )
            predicate_results = [
                {
                    "predicate_id": predicate_id,
                    "passed": passed,
                    "binding_ids": sorted(set(binding_ids)),
                }
            ]
            outcome = "pass" if passed else "block"
            reason_codes = [
                "all_guard_predicates_passed" if passed else "guard_predicate_failed"
            ]
        else:
            predicate_results = []
            outcome = "not_applicable"
            reason_codes = ["guard_not_applicable"]
        source_contract = _guard_source_contract(candidate)
        runtime_contract = candidate["runtime_contract"]
        guard_executions.append(
            {
                "guard_id": guard_id,
                "source_candidate_id": guard_id,
                "source_contract_sha256": canonical_sha256(source_contract),
                "stage": str(runtime_contract["stage"]),
                "violation_code": str(runtime_contract["violation_code"]),
                "applicable": applicable,
                "predicate_results": predicate_results,
                "outcome": outcome,
                "reason_codes": reason_codes,
            }
        )
    hard_gate_pass = all(item["outcome"] != "block" for item in guard_executions)
    snapshot: dict[str, Any] = {
        "schema": HARD_GATE_SNAPSHOT_SCHEMA,
        "asset_hashes": dict(assets.asset_hashes),
        "semantic_effect_registry_sha256": canonical_sha256(registry),
        "source_coverage": dict(registry["counts"]),
        "selected_source_refs": selected_refs,
        "observed_effect_ids": observed_effect_ids,
        "semantic_load_max": semantic_load_max,
        "guard_executions": guard_executions,
        "hard_gate_pass": hard_gate_pass,
    }
    snapshot["snapshot_sha256"] = canonical_sha256(snapshot)
    if not hard_gate_pass:
        blocked = [item["guard_id"] for item in guard_executions if item["outcome"] == "block"]
        raise SelectionError(f"hard gate blocked the selection: {blocked}")
    return snapshot


def build_universal_scene_selection(
    *,
    concept: str,
    scene_contract: Mapping[str, Any],
    topic_id: str,
    format_id: str,
    creativity: float = 0.5,
    seed: int = 0,
    asset_dir: str | Path | None = None,
    assets: UniversalSceneAssets | None = None,
    prior_exposure_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Build one deterministic connected universal event selection.

    Creativity changes only target distance ranking and bridge expression.
    The eligible pool, global one-remote budget, literals, capabilities,
    policies, resources, and predicate results stay invariant.
    """

    _require_nonempty_string(topic_id, "topic_id", InputContractError)
    _require_nonempty_string(format_id, "format_id", InputContractError)
    creativity_value = _require_number_range(creativity, 0.0, 1.0, "creativity", InputContractError)
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise InputContractError("seed must be an integer")
    exposure_list = _require_string_list(
        list(prior_exposure_ids),
        "prior_exposure_ids",
        InputContractError,
    )
    if assets is not None and asset_dir is not None:
        raise InputContractError("pass assets or asset_dir, not both")
    runtime_assets = assets if assets is not None else load_universal_scene_assets(asset_dir)
    known_exposure_ids = {
        candidate_id
        for candidate_id, candidate in runtime_assets.candidate_by_id.items()
        if candidate["role"] == "visual_atom"
    }
    unknown_exposure_ids = set(exposure_list) - known_exposure_ids
    if unknown_exposure_ids:
        raise InputContractError(
            f"prior_exposure_ids contains unknown visual candidate IDs: {sorted(unknown_exposure_ids)}"
        )
    exposure_ids = set(exposure_list)
    validated = validate_scene_contract(concept, scene_contract, assets=runtime_assets)
    target_band = _creativity_target(creativity_value)
    max_optional_remote = GLOBAL_OPTIONAL_REMOTE_MAX
    roles = _initial_roles(validated)
    eligibility_roles = _deep_canonical_copy(roles)
    matched_props = _matched_prop_ids(concept, validated, runtime_assets)
    creativity_invariant_trace, mandatory_literal_entries = (
        _build_creativity_invariant_trace(
            validated=validated,
            eligibility_roles=eligibility_roles,
            matched_prop_ids=matched_props,
            assets=runtime_assets,
        )
    )
    mandatory_literal_candidate_ids = {
        str(entry["candidate"]["id"]) for entry in mandatory_literal_entries
    }

    proposal: Mapping[str, Any] | None = None
    proposal_fallback_reason: str | None = None
    all_proposal_profiles = list(runtime_assets.candidates["proposal_profiles"])
    proposal_decisions = [
        (
            profile,
            *_proposal_eligibility_decision(
                profile,
                validated=validated,
                roles=eligibility_roles,
                matched_prop_ids=matched_props,
                assets=runtime_assets,
                mandatory_candidate_ids=mandatory_literal_candidate_ids,
            ),
        )
        for profile in all_proposal_profiles
    ]
    eligible_profiles = [
        profile for profile, eligible, _ in proposal_decisions if eligible
    ]
    resource_eligible_proposal_ids = {
        str(row["source_id"])
        for row in creativity_invariant_trace["resource_feasibility"]
        if row["source_kind"] == "proposal" and row["outcome"] == "eligible"
    }
    cardinality_eligible_proposal_ids = {
        str(row["source_id"])
        for row in creativity_invariant_trace["cardinality_feasibility"]
        if row["source_kind"] == "proposal" and row["outcome"] == "eligible"
    }
    rankable_profiles = [
        profile
        for profile in eligible_profiles
        if str(profile["id"]) in resource_eligible_proposal_ids
        and str(profile["id"]) in cardinality_eligible_proposal_ids
    ]
    proposal_rejections = sorted(
        (
            {
                "proposal_id": str(profile["id"]),
                "reason_code": str(reason_code),
            }
            for profile, eligible, reason_code in proposal_decisions
            if not eligible
        ),
        key=lambda item: item["proposal_id"].encode("utf-8"),
    )
    if rankable_profiles:
        target_index = {"near": 0, "middle": 1, "far": 2}[target_band]
        # Creativity ranks one invariant hard-eligible pool; it never removes a
        # semantic family or changes policy/resource eligibility.
        ranked_profiles = list(rankable_profiles)
        prefix = "|".join(
            [
                runtime_assets.asset_hashes["universal_candidates_sha256"],
                validated.request_sha256,
                validated.sha256,
                topic_id,
                format_id,
                str(creativity_value),
                str(seed),
            ]
        )
        ranked_profiles.sort(
            key=lambda profile: (
                abs({"near": 0, "middle": 1, "far": 2}[_distance_band(profile["distance_profile"])] - target_index),
                int(profile["load_profile"]["theme_displacement"]),
                int(profile["load_profile"]["physical"]),
                hashlib.sha256(f"{prefix}|{profile['id']}".encode("utf-8")).hexdigest(),
                str(profile["id"]),
            )
        )
        proposal = ranked_profiles[0]
        if (
            str(proposal["id"]) not in resource_eligible_proposal_ids
            or str(proposal["id"]) not in cardinality_eligible_proposal_ids
        ):
            raise SelectionError("selected proposal is absent from the invariant feasible intersection")
        _apply_proposal_roles(proposal, roles, validated)
        proposal_band = _distance_band(proposal["distance_profile"])
        if proposal_band != target_band:
            proposal_fallback_reason = f"no_coherent_{target_band}_proposal_fell_back_to_{proposal_band}"

    (
        selected_entries,
        eligible_counts,
        rejection_counts,
        eligible_candidate_ids_by_facet,
        candidate_rejections,
    ) = _select_catalog_atoms(
        validated=validated,
        roles=roles,
        eligibility_roles=eligibility_roles,
        matched_prop_ids=matched_props,
        assets=runtime_assets,
        target_band=target_band,
        seed=seed,
        topic_id=topic_id,
        format_id=format_id,
        prior_exposure_ids=exposure_ids,
        proposal=proposal,
    )
    selected_entries = _inject_context_profile_carriers(
        selected_entries,
        validated=validated,
        roles=roles,
        matched_prop_ids=matched_props,
        assets=runtime_assets,
    )
    _assert_literal_realization_selection_budgets(selected_entries, validated)
    if not _claims_fit(selected_entries, validated):
        raise SelectionError(
            "context carrier completion exceeds a capability/resource capacity"
        )

    # Assign stable instance IDs before binding roles, resources, and evidence.
    instance_entries: list[tuple[str, Mapping[str, Any]]] = []
    for index, entry in enumerate(selected_entries, start=1):
        instance_entries.append((f"atom_{index:02d}_{entry['candidate']['id']}", entry))
    if (
        len(instance_entries) != len(selected_entries)
        or len({instance_id for instance_id, _ in instance_entries}) != len(instance_entries)
    ):
        raise SelectionError("selected entries did not receive one unique atom instance each")
    profile_overlays = _selection_context_profile_overlays(
        assets=runtime_assets,
        validated=validated,
        roles=roles,
        matched_prop_ids=matched_props,
        atoms=[
            {
                "instance_id": instance_id,
                "candidate_id": str(entry["candidate"]["id"]),
            }
            for instance_id, entry in instance_entries
        ],
        provided_predicates={
            tuple(predicate)
            for _, entry in instance_entries
            for predicate in entry["candidate"]["postconditions"]
        },
    )
    for instance_id, entry in instance_entries:
        overlay = profile_overlays.get(instance_id)
        if overlay is None:
            entry["context_bridge_types"] = []
            continue
        entry["distance_vector"] = _max_vector(
            [entry["distance_vector"], overlay["distance_profile"]],
            DISTANCE_AXIS_IDS,
        )
        entry["load_vector"] = _max_vector(
            [entry["load_vector"], overlay["load_profile"]],
            LOAD_AXIS_IDS,
        )
        entry["context_bridge_types"] = list(overlay["bridge_types"])
    for role in roles.values():
        source_id = str(role["source_id"])
        if source_id.startswith("proposal:") and proposal is not None:
            role["source_id"] = instance_entries[0][0]
        elif source_id.startswith("candidate:"):
            candidate_id = source_id.split(":", 1)[1]
            match = next((instance_id for instance_id, entry in instance_entries if entry["candidate"]["id"] == candidate_id), None)
            if match is not None:
                role["source_id"] = match

    edges: list[dict[str, str]] = []
    for role_id in EVENT_ROLE_IDS:
        if role_id in roles:
            edges.append(
                {
                    "edge_id": f"edge_role_{len(edges)+1:02d}_{role_id}",
                    "from_node_id": "event_01",
                    "relation_id": f"has_role:{role_id}",
                    "to_node_id": str(roles[role_id]["value_id"]),
                }
            )

    atoms: list[dict[str, Any]] = []
    resource_claims: list[dict[str, Any]] = []
    pixel_items: list[dict[str, Any]] = []
    core_item_ids: list[str] = []
    event_item_ids: list[str] = []
    contact_item_ids: list[str] = []
    consequence_item_ids: list[str] = []

    actor_entity = validated.entity_by_id[_actor_entity_id(validated)]
    if not actor_entity["feature_facts"]:
        raise SelectionError(
            "primary actor participant lacks a literal identity feature for core pixel evidence"
        )
    first_fact = actor_entity["feature_facts"][0]
    core_item_id = f"pixel_core_{first_fact['id']}"
    pixel_items.append(
        {
            "item_id": core_item_id,
            "source_kind": "core_anchor",
            "source_id": str(first_fact["id"]),
            "kind": "display",
            "minimum_scale_ids": ["native", "thumbnail_320px"],
            "status": "future_review_required",
        }
    )
    core_item_ids.append(core_item_id)
    event_item_id = "pixel_event_actor_action"
    pixel_items.append(
        {
            "item_id": event_item_id,
            "source_kind": "event",
            "source_id": "event_01",
            "kind": "path",
            "minimum_scale_ids": ["native", "thumbnail_320px"],
            "status": "future_review_required",
        }
    )
    event_item_ids.append(event_item_id)

    for instance_id, entry in instance_entries:
        candidate = entry["candidate"]
        atom_edge_id = f"edge_atom_{len(edges)+1:02d}"
        edges.append(
            {
                "edge_id": atom_edge_id,
                "from_node_id": "event_01",
                "relation_id": f"realizes:{candidate['facet']}",
                "to_node_id": instance_id,
            }
        )
        bindings: list[dict[str, str]] = []
        for role_id, requirement in candidate["runtime_contract"]["bindings"]:
            if role_id not in roles:
                if requirement == "required":
                    raise SelectionError(f"selected atom {candidate['id']} lacks required role {role_id}")
                continue
            bindings.append(
                {
                    "role_id": role_id,
                    "node_id": str(roles[role_id]["value_id"]),
                    "requirement": "required" if requirement == "event_spine" else requirement,
                }
            )
        claim_ids: list[str] = []
        for raw_claim in candidate["runtime_contract"]["resource_claims"]:
            for kind, owner_id, amount, mode in _resolved_claim_tuples(
                raw_claim,
                validated,
                entry.get("parameters", {}).get("resolved_owner_refs", []),
            ):
                claim_id = f"claim_{len(resource_claims)+1:02d}_{kind}"
                resource_claims.append(
                    {
                        "claim_id": claim_id,
                        "resource_kind": kind,
                        "owner_id": owner_id,
                        "amount": amount,
                        "mode": mode,
                        "claimant_id": instance_id,
                        "phase_id": str(roles["phase"]["value_id"]),
                        "evidence_required": True,
                    }
                )
                claim_ids.append(claim_id)
        atom_pixel_ids: list[str] = []
        for evidence in candidate["runtime_contract"]["pixel_evidence"]:
            item_id = f"pixel_atom_{instance_id}_{evidence['id'].replace('::', '_')}"
            pixel_items.append(
                {
                    "item_id": item_id,
                    "source_kind": "atom",
                    "source_id": instance_id,
                    "kind": evidence["kind"],
                    "minimum_scale_ids": list(evidence["minimum_scale_ids"]),
                    "status": "future_review_required",
                }
            )
            atom_pixel_ids.append(item_id)
            if evidence["kind"] in {"contact", "support"}:
                contact_item_ids.append(item_id)
            if candidate["facet"] == "consequence" or evidence["kind"] in {"state_boundary", "residue"}:
                consequence_item_ids.append(item_id)
        atom_band = _distance_band(entry["distance_vector"])
        atoms.append(
            {
                "instance_id": instance_id,
                "candidate_id": str(candidate["id"]),
                "facet": str(candidate["facet"]),
                "parameters": dict(entry["parameters"]),
                "bindings": bindings,
                "event_edge_ids": [atom_edge_id],
                "resource_claim_ids": claim_ids,
                "pixel_evidence_ids": atom_pixel_ids,
                "distance_vector": dict(entry["distance_vector"]),
                "distance_band": atom_band,
                "load_vector": dict(entry["load_vector"]),
            }
        )

    if "result" in roles:
        consequence_item_id = "pixel_event_consequence"
        pixel_items.append(
            {
                "item_id": consequence_item_id,
                "source_kind": "consequence",
                "source_id": str(roles["result"]["value_id"]),
                "kind": "state_boundary",
                "minimum_scale_ids": ["native"],
                "status": "future_review_required",
            }
        )
        consequence_item_ids.append(consequence_item_id)

    bridges: list[dict[str, Any]] = []
    bridge_ids: set[str] = set()
    edge_ids: set[str] = {
        str(edge["edge_id"])
        for edge in edges
    }
    pixel_item_ids: set[str] = {
        str(item["item_id"])
        for item in pixel_items
    }
    bridge_occurrences_by_owner_type: dict[tuple[str, str], int] = {}

    def add_bridge_path(
        *,
        premise_node: str,
        band: str,
        available_types: Sequence[str],
        fallback_candidate: Mapping[str, Any],
        source_label: str,
    ) -> None:
        bridge_types = _choose_bridge_types(band, available_types)
        actor_node = str(roles["actor"]["value_id"])
        needs_target = bool(set(bridge_types) & set(MEDIATION_BRIDGE_TYPES)) or (
            band == "far" and bool(set(bridge_types) & set(EXIT_BRIDGE_TYPES))
        )
        needs_result = bool(set(bridge_types) & set(EXIT_BRIDGE_TYPES))
        target_node = (
            _ensure_runtime_role(
                roles,
                validated,
                "target",
                f"visible_target:{source_label}",
                source_label,
            )
            if needs_target
            else None
        )
        result_node = (
            _ensure_runtime_role(
                roles,
                validated,
                "result",
                f"visible_consequence:{source_label}",
                source_label,
            )
            if needs_result
            else None
        )
        for bridge_type in bridge_types:
            if bridge_type in ENTRY_BRIDGE_TYPES:
                from_node, to_node = (
                    ("event_01", premise_node)
                    if band == "near"
                    else (actor_node, premise_node)
                )
            elif bridge_type in MEDIATION_BRIDGE_TYPES:
                if target_node is None:
                    raise SelectionError("mediation bridge lacks a typed target endpoint")
                from_node, to_node = premise_node, target_node
            elif bridge_type in EXIT_BRIDGE_TYPES:
                if result_node is None or (band == "far" and target_node is None):
                    raise SelectionError("exit bridge lacks its typed result/target endpoint")
                from_node, to_node = (
                    (target_node, result_node)
                    if band == "far"
                    else (premise_node, result_node)
                )
            else:
                raise SelectionError(f"bridge type is outside the operational closed seven: {bridge_type}")
            source_candidate = _bridge_source_candidate(bridge_type, runtime_assets, fallback_candidate)
            owner_type = (source_label, bridge_type)
            owner_occurrence = bridge_occurrences_by_owner_type.get(owner_type, 0) + 1
            bridge_occurrences_by_owner_type[owner_type] = owner_occurrence
            bridge_id = (
                f"bridge_{bridge_type}_{owner_occurrence:02d}_{source_label}"
            )
            edge_id = f"edge_{bridge_id}"
            if bridge_id in bridge_ids:
                raise SelectionError(f"bridge id collision: {bridge_id}")
            if edge_id in edge_ids:
                raise SelectionError(f"bridge edge id collision: {edge_id}")
            bridge_ids.add(bridge_id)
            edge_ids.add(edge_id)
            edges.append(
                {
                    "edge_id": edge_id,
                    "from_node_id": from_node,
                    "relation_id": f"bridge:{bridge_type}",
                    "to_node_id": to_node,
                }
            )
            bridge_pixel_ids: list[str] = []
            for evidence in source_candidate["runtime_contract"]["pixel_evidence"]:
                item_id = f"pixel_bridge_{bridge_id}_{evidence['id'].replace('::', '_')}"
                if item_id in pixel_item_ids:
                    raise SelectionError(f"bridge pixel item id collision: {item_id}")
                pixel_item_ids.add(item_id)
                pixel_items.append(
                    {
                        "item_id": item_id,
                        "source_kind": "bridge",
                        "source_id": bridge_id,
                        "kind": evidence["kind"],
                        "minimum_scale_ids": list(evidence["minimum_scale_ids"]),
                        "status": "future_review_required",
                    }
                )
                bridge_pixel_ids.append(item_id)
            if not bridge_pixel_ids:
                raise SelectionError(f"bridge {bridge_id} lacks future pixel evidence")
            bridges.append(
                {
                    "bridge_id": bridge_id,
                    "bridge_type": bridge_type,
                    "candidate_id": str(source_candidate["id"]),
                    "from_node_id": from_node,
                    "to_node_id": to_node,
                    "event_edge_ids": [edge_id],
                    "pixel_evidence_ids": bridge_pixel_ids,
                }
            )

    for atom, (_, entry) in zip(atoms, instance_entries):
        available_bridge_types = list(
            entry["proposal"]["bridge_types"]
            if entry["proposal"] is not None
            else entry["candidate"]["runtime_contract"]["bridge_types"]
        )
        for bridge_type in entry.get("context_bridge_types", []):
            if bridge_type not in available_bridge_types:
                available_bridge_types.append(bridge_type)
        add_bridge_path(
            premise_node=atom["instance_id"],
            band=atom["distance_band"],
            available_types=available_bridge_types,
            fallback_candidate=entry["candidate"],
            source_label=atom["instance_id"],
        )

    fixed_distance_vectors, fixed_load_vectors = _fixed_prop_vectors(matched_props, runtime_assets)
    fixed_remote_props = [
        prop_id
        for prop_id in sorted(matched_props)
        if _distance_band(runtime_assets.prop_by_id[prop_id]["base_distance_profile"]) == "far"
    ]
    for prop_id in sorted(matched_props):
        prop = runtime_assets.prop_by_id[prop_id]
        prop_band = _distance_band(prop["base_distance_profile"])
        fallback_id = next(
            (
                candidate_id
                for candidate_id in prop["affordance_candidate_ids"]
                if candidate_id in runtime_assets.candidate_by_id
                and runtime_assets.candidate_by_id[candidate_id]["role"] == "visual_atom"
            ),
            None,
        )
        if fallback_id is None:
            raise SelectionError(f"fixed prop {prop_id} lacks a visual affordance candidate")
        premise_node = next(
            (
                str(roles[role_id]["value_id"])
                for role_id in ("instrument", "target")
                if role_id in roles and (
                    prop_id in _normalize_text(str(roles[role_id]["value_id"]))
                    or any(_normalize_text(alias) in _normalize_text(concept) for alias in _aliases_for_prop(prop))
                )
            ),
            f"fixed_prop:{prop_id}",
        )
        add_bridge_path(
            premise_node=premise_node,
            band=prop_band,
            available_types=runtime_assets.candidate_by_id[fallback_id]["runtime_contract"]["bridge_types"],
            fallback_candidate=runtime_assets.candidate_by_id[fallback_id],
            source_label=f"fixed_{prop_id}",
        )

    _rebind_bridge_owned_runtime_roles(
        roles,
        validated=validated,
        atoms=atoms,
        bridges=bridges,
        spine_edges=edges,
        assets=runtime_assets,
    )

    if "result" in roles and not consequence_item_ids:
        consequence_item_id = "pixel_event_consequence_late"
        pixel_items.append(
            {
                "item_id": consequence_item_id,
                "source_kind": "consequence",
                "source_id": str(roles["result"]["value_id"]),
                "kind": "state_boundary",
                "minimum_scale_ids": ["native"],
                "status": "future_review_required",
            }
        )
        consequence_item_ids.append(consequence_item_id)

    # Role creation by bridge paths happened after the first role-edge pass.
    existing_role_edges = {
        edge["relation_id"].split(":", 1)[1]
        for edge in edges
        if edge["relation_id"].startswith("has_role:")
    }
    for role_id in EVENT_ROLE_IDS:
        if role_id in roles and role_id not in existing_role_edges:
            edges.insert(
                len(existing_role_edges),
                {
                    "edge_id": f"edge_role_late_{role_id}",
                    "from_node_id": "event_01",
                    "relation_id": f"has_role:{role_id}",
                    "to_node_id": str(roles[role_id]["value_id"]),
                },
            )
            existing_role_edges.add(role_id)

    # Bridge completion may add a typed result/location after atom instances
    # were first emitted.  Re-project every optional/required atom role from
    # the final event spine so the public replay sees one canonical binding
    # view rather than selection-time partial state.
    for atom in atoms:
        candidate = runtime_assets.candidate_by_id[str(atom["candidate_id"])]
        final_bindings: list[dict[str, str]] = []
        for role_id, requirement in candidate["runtime_contract"]["bindings"]:
            if role_id not in roles:
                if requirement == "required":
                    raise SelectionError(
                        f"selected atom {candidate['id']} lacks final required role {role_id}"
                    )
                continue
            final_bindings.append(
                {
                    "role_id": role_id,
                    "node_id": str(roles[role_id]["value_id"]),
                    "requirement": (
                        "required" if requirement == "event_spine" else requirement
                    ),
                }
            )
        atom["bindings"] = final_bindings

    aggregate_distance = _max_vector(
        [*fixed_distance_vectors, *(atom["distance_vector"] for atom in atoms)],
        DISTANCE_AXIS_IDS,
    )
    selected_band = _distance_band(aggregate_distance)
    remote_atom_ids = [atom["instance_id"] for atom in atoms if atom["distance_band"] == "far"]
    proposal_remote = bool(proposal is not None and proposal["remote_or_high_load"])
    optional_remote_count = max(len(remote_atom_ids), 1 if proposal_remote else 0)
    fixed_remote_count = len(fixed_remote_props)
    if fixed_remote_count and optional_remote_count:
        raise SelectionError("optional remote premise competes with preserved fixed remote premises")
    if optional_remote_count > max_optional_remote:
        raise SelectionError("global optional remote-premise budget exceeded")
    fallback_reason = proposal_fallback_reason
    if selected_band != target_band and fallback_reason is None:
        if fixed_remote_count and {"near": 0, "middle": 1, "far": 2}[selected_band] > {"near": 0, "middle": 1, "far": 2}[target_band]:
            fallback_reason = "user_fixed_remote_preserved"
        else:
            fallback_reason = f"no_coherent_{target_band}_bundle_selected_{selected_band}"

    all_scales = sorted(
        {scale for item in pixel_items for scale in item["minimum_scale_ids"]},
        key=lambda item: (item != "native", item),
    )
    selected_ids_for_digest = [atom["candidate_id"] for atom in atoms] + [bridge["candidate_id"] for bridge in bridges]
    tie_break_digest = hashlib.sha256(
        canonical_json_bytes(
            {
                "asset_hashes": dict(runtime_assets.asset_hashes),
                "request_sha256": validated.request_sha256,
                "scene_contract_sha256": validated.sha256,
                "topic_id": topic_id,
                "format_id": format_id,
                "creativity": creativity_value,
                "seed": seed,
                "prior_exposure_ids": exposure_list,
                "selected_ids": selected_ids_for_digest,
            }
        )
    ).hexdigest()
    result = {
        "schema": SELECTION_SCHEMA,
        "scene_contract": _deep_canonical_copy(dict(validated.contract)),
        "composition_carriers": _build_composition_carriers(
            validated=validated,
            roles=roles,
            atoms=atoms,
            bridges=bridges,
            resource_claims=resource_claims,
            assets=runtime_assets,
        ),
        "identity_core": {
            "entities": _deep_canonical_copy(validated.contract["identity_core"]["entities"]),
            "scene_facts": _deep_canonical_copy(validated.contract["identity_core"]["scene_facts"]),
            "forbidden_facts": _deep_canonical_copy(validated.contract["identity_core"]["forbidden_facts"]),
            "capability_capacities": _scene_capability_records(validated),
        },
        "slot_states": _deep_canonical_copy(validated.contract["slot_states"]),
        "context_profile": _deep_canonical_copy(validated.contract["context_profile"]),
        "selected_event": {
            "event_id": "event_01",
            "phase_id": str(roles["phase"]["value_id"]),
            "roles": [
                dict(roles[role_id])
                if role_id in roles
                else {
                    "role_id": role_id,
                    "value_id": None,
                    "source": "user_fixed" if validated.role_by_id[role_id]["state"] == "closed" else "runtime_selected",
                    "source_id": role_id,
                }
                for role_id in EVENT_ROLE_IDS
            ],
            "spine_edges": edges,
        },
        "atoms": atoms,
        "bridges": bridges,
        "resource_claims": resource_claims,
        "semantic_distance_trace": {
            "policy_id": "typed_ordinal_distance_v1",
            "creativity": creativity_value,
            "target_band": target_band,
            "selected_band": selected_band,
            "vector": aggregate_distance,
            "fixed_remote_count": fixed_remote_count,
            "optional_remote_count": optional_remote_count,
            "max_optional_remote_count": max_optional_remote,
            "remote_atom_ids": remote_atom_ids,
            "fallback_reason": fallback_reason,
            "theme_displacement_band": _theme_displacement_band(aggregate_distance["theme"]),
        },
        "pixel_evidence_contract": {
            "required_scale_ids": all_scales,
            "items": pixel_items,
            "core_anchor_item_ids": core_item_ids,
            "event_item_ids": event_item_ids,
            "contact_item_ids": sorted(set(contact_item_ids)),
            "consequence_item_ids": sorted(set(consequence_item_ids)),
        },
        "selection_trace": {
            "selection_mode": "predicate_beam_v1",
            "seed": seed,
            "scene_contract_sha256": validated.sha256,
            "eligible_count_by_facet": eligible_counts,
            "eligible_candidate_ids_by_facet": eligible_candidate_ids_by_facet,
            "candidate_rejections": candidate_rejections,
            "rejection_count_by_code": {
                reason_code: sum(
                    item["reason_code"] == reason_code
                    for item in candidate_rejections
                )
                for reason_code in sorted(
                    {item["reason_code"] for item in candidate_rejections}
                )
            },
            "eligible_proposal_family_ids": sorted(
                str(profile["semantic_family_id"]) for profile in eligible_profiles
            ),
            "eligible_proposal_profile_ids": sorted(
                str(profile["id"]) for profile in eligible_profiles
            ),
            "proposal_rejections": proposal_rejections,
            "eligible_proposal_count_by_band": {
                band: sum(
                    _distance_band(profile["distance_profile"]) == band
                    for profile in eligible_profiles
                )
                for band in ("near", "middle", "far")
            },
            "proposal_rejection_count_by_code": {
                reason_code: sum(
                    item["reason_code"] == reason_code
                    for item in proposal_rejections
                )
                for reason_code in PROPOSAL_REJECTION_REASON_IDS
                if any(
                    item["reason_code"] == reason_code
                    for item in proposal_rejections
                )
            },
            "beam_width": int(runtime_assets.compatibility["solver"]["beam_width"]),
            "tie_break_digest": tie_break_digest,
        },
        "creativity_invariant_trace": creativity_invariant_trace,
    }
    context_overlay_pairs = [
        (profile_id, instance_id)
        for instance_id, overlay in profile_overlays.items()
        for profile_id in overlay["profile_ids"]
    ]
    hard_gate_snapshot = _build_hard_gate_snapshot(
        request_text=concept,
        selection=result,
        assets=runtime_assets,
        validated=validated,
        matched_prop_ids=matched_props,
        context_overlay_pairs=context_overlay_pairs,
    )
    result["hard_gate_snapshot"] = hard_gate_snapshot
    result["selection_trace"]["hard_gate_snapshot_sha256"] = hard_gate_snapshot[
        "snapshot_sha256"
    ]
    result["postselection_run_trace"] = _build_postselection_run_trace(
        selection=result,
        validated=validated,
        assets=runtime_assets,
        matched_prop_ids=matched_props,
        context_overlay_pairs=context_overlay_pairs,
    )
    return _deep_canonical_copy(result)


def _selection_contract_view(
    selection: Mapping[str, Any],
    request_text: str,
    assets: UniversalSceneAssets,
) -> tuple[ValidatedSceneContract, dict[str, Mapping[str, Any]]]:
    """Validate the embedded contract and every retained scene projection."""

    embedded = _require_mapping(selection["scene_contract"], "selection.scene_contract", SelectionError)
    validated = validate_scene_contract(request_text, embedded, assets=assets)
    identity = _require_mapping(selection["identity_core"], "selection.identity_core", SelectionError)
    _require_exact_keys(
        identity,
        {"entities", "scene_facts", "forbidden_facts", "capability_capacities"},
        "selection.identity_core",
        SelectionError,
    )
    expected_identity = {
        "entities": _deep_canonical_copy(validated.contract["identity_core"]["entities"]),
        "scene_facts": _deep_canonical_copy(validated.contract["identity_core"]["scene_facts"]),
        "forbidden_facts": _deep_canonical_copy(validated.contract["identity_core"]["forbidden_facts"]),
        "capability_capacities": _scene_capability_records(validated),
    }
    if identity != expected_identity:
        raise SelectionError("selection identity_core is not the exact embedded-contract projection")
    if selection["slot_states"] != validated.contract["slot_states"]:
        raise SelectionError("selection slot_states are not the exact embedded-contract projection")
    if selection["context_profile"] != validated.contract["context_profile"]:
        raise SelectionError("selection context_profile is not the exact embedded-contract projection")

    event = _require_mapping(selection["selected_event"], "selection.selected_event", SelectionError)
    _require_exact_keys(
        event,
        {"event_id", "phase_id", "roles", "spine_edges"},
        "selection.selected_event",
        SelectionError,
    )
    if event["event_id"] != "event_01":
        raise SelectionError("selection must retain exactly event_01")
    raw_roles = _require_list(event["roles"], "selection.selected_event.roles", SelectionError)
    if [item.get("role_id") if isinstance(item, Mapping) else None for item in raw_roles] != list(EVENT_ROLE_IDS):
        raise SelectionError("selection.selected_event.roles must contain the exact closed role order")
    role_outputs: dict[str, Mapping[str, Any]] = {}
    for index, raw_role in enumerate(raw_roles):
        where = f"selection.selected_event.roles[{index}]"
        role = _require_mapping(raw_role, where, SelectionError)
        _require_exact_keys(role, {"role_id", "value_id", "source", "source_id"}, where, SelectionError)
        role_id = str(role["role_id"])
        if role["source"] not in {"user_fixed", "runtime_selected"}:
            raise SelectionError(f"{where}.source is outside the closed enum")
        source_id = _require_nonempty_string(role["source_id"], f"{where}.source_id", SelectionError)
        value_id = role["value_id"]
        if value_id is not None:
            _require_nonempty_string(value_id, f"{where}.value_id", SelectionError)
        contract_role = validated.role_by_id[role_id]
        if contract_role["state"] == "fixed":
            if role["source"] != "user_fixed" or source_id != role_id or value_id != contract_role["value_id"]:
                raise SelectionError(f"{where} does not preserve the embedded fixed role")
        elif contract_role["state"] == "closed":
            if role["source"] != "user_fixed" or source_id != role_id or value_id is not None:
                raise SelectionError(f"{where} enters an embedded closed role")
        elif role["source"] != "runtime_selected":
            raise SelectionError(f"{where} turns an open role into a user-fixed claim")
        role_outputs[role_id] = role
    if role_outputs["actor"]["value_id"] is None:
        raise SelectionError("event actor must be present")
    if role_outputs["phase"]["value_id"] is None or event["phase_id"] != role_outputs["phase"]["value_id"]:
        raise SelectionError("event phase_id must exactly match the non-null phase role")
    for role_id in EVENT_ROLE_IDS:
        role = role_outputs[role_id]
        if (
            validated.role_by_id[role_id]["state"] == "open"
            and role["source"] == "runtime_selected"
            and role["value_id"] is not None
        ):
            _runtime_selected_role_authority(
                role,
                selection=selection,
                validated=validated,
                assets=assets,
            )

    trace = _require_mapping(selection["selection_trace"], "selection.selection_trace", SelectionError)
    scene_hash = trace.get("scene_contract_sha256")
    if scene_hash != validated.sha256:
        raise SelectionError("selection trace does not hash the embedded canonical scene contract")
    return validated, role_outputs


def _selection_context_profile_overlays(
    *,
    assets: UniversalSceneAssets,
    validated: ValidatedSceneContract,
    roles: Mapping[str, Mapping[str, Any]],
    matched_prop_ids: set[str],
    atoms: Sequence[Mapping[str, Any]],
    provided_predicates: set[tuple[str, str, str]],
) -> dict[str, dict[str, Any]]:
    """Recompute creativity-invariant typed context overlays."""

    profiles = assets.candidates.get("context_distance_profiles", [])
    if not isinstance(profiles, list):
        raise SelectionError("validated context_distance_profiles is not an array")
    instances_by_candidate: dict[str, list[str]] = {}
    for atom in atoms:
        instances_by_candidate.setdefault(str(atom["candidate_id"]), []).append(str(atom["instance_id"]))
    selected_ids = set(instances_by_candidate)
    overlays: dict[str, dict[str, Any]] = {}
    context = {
        "validated": validated,
        "roles": {role_id: role for role_id, role in roles.items() if role.get("value_id") is not None},
        "matched_prop_ids": matched_prop_ids,
        "selected_candidate_ids": selected_ids,
        "provided_predicates": provided_predicates,
        "assets": assets,
    }
    for profile in sorted(profiles, key=lambda item: str(item["id"])):
        candidate_ids = [str(item) for item in profile["candidate_ids"]]
        if not candidate_ids or not set(candidate_ids) <= selected_ids:
            continue
        if not _predicate_set_passes(
            profile["requires_all"],
            profile["requires_any"],
            profile["forbids_any"],
            **context,
        ):
            continue
        policy_mode = profile["policy_mode"]
        if policy_mode == "safe_tool" and validated.contract["context_profile"]["violence"] == "active":
            continue
        if policy_mode == "explicit_weapon_only" and "prop_decommissioned_machine_gun" not in matched_prop_ids:
            continue
        carrier_candidate_id = str(profile["carrier_candidate_id"])
        if carrier_candidate_id not in instances_by_candidate:
            # Strict asset validation guarantees membership; selection still
            # fails closed if an untrusted/mutated profile view drifts.
            raise SelectionError(
                f"context distance profile {profile['id']} lacks its selected carrier candidate"
            )
        carrier_instance_id = sorted(instances_by_candidate[carrier_candidate_id])[0]
        overlay = overlays.setdefault(
            carrier_instance_id,
            {
                "distance_profile": {axis: 0 for axis in DISTANCE_AXIS_IDS},
                "load_profile": {axis: 0 for axis in LOAD_AXIS_IDS},
                "bridge_types": [],
                "profile_ids": [],
            },
        )
        overlay["distance_profile"] = _max_vector(
            [overlay["distance_profile"], profile["distance_profile"]],
            DISTANCE_AXIS_IDS,
        )
        overlay["load_profile"] = _max_vector(
            [overlay["load_profile"], profile["load_profile"]],
            LOAD_AXIS_IDS,
        )
        for bridge_type in profile["bridge_types"]:
            if bridge_type not in overlay["bridge_types"]:
                overlay["bridge_types"].append(bridge_type)
        overlay["profile_ids"].append(str(profile["id"]))
    return overlays


def _validate_universal_scene_selection_impl(
    selection: Mapping[str, Any],
    request_text: str,
    assets: UniversalSceneAssets,
    *,
    topic_id: str | None = None,
    format_id: str | None = None,
    creativity: float | None = None,
    seed: int | None = None,
    prior_exposure_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Independently re-evaluate an untrusted v3 scene against frozen assets.

    This boundary deliberately does not accept a trusted eligibility trace.
    Candidate predicates, fixed/closed slots, capability/resource claims,
    semantic profiles, bridge edges, and pixel-evidence ownership are derived
    again from the raw-byte-bound asset view.
    """

    if not isinstance(request_text, str) or not request_text.strip():
        raise InputContractError("request_text must be a non-empty string")
    if not isinstance(assets, UniversalSceneAssets):
        raise AssetValidationError("assets must be a validated UniversalSceneAssets instance")
    if topic_id is None or format_id is None or creativity is None or seed is None:
        raise SelectionError(
            "canonical replay requires topic_id, format_id, creativity, seed, and prior_exposure_ids"
        )
    _require_nonempty_string(topic_id, "topic_id", SelectionError)
    _require_nonempty_string(format_id, "format_id", SelectionError)
    creativity_value = _require_number_range(
        creativity, 0.0, 1.0, "creativity", SelectionError
    )
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise SelectionError("seed must be an integer")
    exposure_ids = _require_string_list(
        list(prior_exposure_ids),
        "prior_exposure_ids",
        SelectionError,
    )
    try:
        scene = _deep_canonical_copy(_require_mapping(selection, "selection", SelectionError))
    except UniversalSceneRuntimeError:
        raise
    except (TypeError, ValueError, OverflowError) as exc:
        raise SelectionError(f"selection is not canonical JSON: {exc}") from exc
    _require_exact_keys(
        scene,
        {
            "schema",
            "scene_contract",
            "composition_carriers",
            "identity_core",
            "slot_states",
            "context_profile",
            "selected_event",
            "atoms",
            "bridges",
            "resource_claims",
            "semantic_distance_trace",
            "pixel_evidence_contract",
            "hard_gate_snapshot",
            "selection_trace",
            "creativity_invariant_trace",
            "postselection_run_trace",
        },
        "selection",
        SelectionError,
    )
    if scene["schema"] != SELECTION_SCHEMA:
        raise SelectionError(f"selection.schema must be {SELECTION_SCHEMA}")
    validated, role_outputs = _selection_contract_view(scene, request_text, assets)
    roles = {
        role_id: role
        for role_id, role in role_outputs.items()
        if role["value_id"] is not None
    }
    matched_props = _matched_prop_ids(request_text, validated, assets)
    expected_invariant_trace, replay_mandatory_entries = (
        _revalidate_creativity_invariant_trace(
            scene["creativity_invariant_trace"],
            validated=validated,
            eligibility_roles=_initial_roles(validated),
            matched_prop_ids=matched_props,
            assets=assets,
        )
    )
    replay_mandatory_candidate_ids = {
        str(entry["candidate"]["id"]) for entry in replay_mandatory_entries
    }

    event = scene["selected_event"]
    raw_edges = _require_list(event["spine_edges"], "selection.selected_event.spine_edges", SelectionError)
    edge_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_edge in enumerate(raw_edges):
        where = f"selection.selected_event.spine_edges[{index}]"
        edge = _require_mapping(raw_edge, where, SelectionError)
        _require_exact_keys(edge, {"edge_id", "from_node_id", "relation_id", "to_node_id"}, where, SelectionError)
        edge_id = _require_nonempty_string(edge["edge_id"], f"{where}.edge_id", SelectionError)
        if edge_id in edge_by_id:
            raise SelectionError(f"duplicate event edge: {edge_id}")
        for field in ("from_node_id", "relation_id", "to_node_id"):
            _require_nonempty_string(edge[field], f"{where}.{field}", SelectionError)
        edge_by_id[edge_id] = edge
    for role_id, role in role_outputs.items():
        role_edges = [
            edge for edge in raw_edges
            if edge["relation_id"] == f"has_role:{role_id}"
        ]
        if role["value_id"] is None:
            if role_edges:
                raise SelectionError(f"null event role {role_id} has a spine edge")
        elif len(role_edges) != 1 or role_edges[0]["from_node_id"] != "event_01" or role_edges[0]["to_node_id"] != role["value_id"]:
            raise SelectionError(f"event role {role_id} lacks its exact role edge")

    raw_atoms = _require_list(scene["atoms"], "selection.atoms", SelectionError)
    if not raw_atoms:
        raise SelectionError("selection.atoms must not be empty")
    atom_by_id: dict[str, Mapping[str, Any]] = {}
    selected_candidate_ids: set[str] = set()
    provided_predicates: set[tuple[str, str, str]] = set()
    proposal_by_id = {
        str(profile["id"]): profile
        for profile in assets.candidates["proposal_profiles"]
    }
    literal_realization_by_id = {
        str(profile["id"]): profile
        for profile in assets.semantic_bindings["literal_visual_realization_profiles"]
    }
    atom_profiles: dict[str, dict[str, Any]] = {}
    literal_realization_atom_ids: dict[str, list[str]] = {}
    proposal_atom_ids: set[str] = set()
    for index, raw_atom in enumerate(raw_atoms):
        where = f"selection.atoms[{index}]"
        atom = _require_mapping(raw_atom, where, SelectionError)
        _require_exact_keys(
            atom,
            {"instance_id", "candidate_id", "facet", "parameters", "bindings", "event_edge_ids", "resource_claim_ids", "pixel_evidence_ids", "distance_vector", "distance_band", "load_vector"},
            where,
            SelectionError,
        )
        instance_id = _require_nonempty_string(atom["instance_id"], f"{where}.instance_id", SelectionError)
        if instance_id in atom_by_id:
            raise SelectionError(f"duplicate atom instance_id: {instance_id}")
        candidate_id = _require_nonempty_string(atom["candidate_id"], f"{where}.candidate_id", SelectionError)
        candidate = assets.candidate_by_id.get(candidate_id)
        if candidate is None or candidate["role"] != "visual_atom":
            raise SelectionError(f"atom {instance_id} references a non-visual or unknown candidate")
        if atom["facet"] != candidate["facet"]:
            raise SelectionError(f"atom {instance_id} facet disagrees with candidate")
        parameters = _require_mapping(atom["parameters"], f"{where}.parameters", SelectionError)
        proposal = None
        if "proposal_id" in parameters:
            _require_exact_keys(parameters, {"proposal_id", "value_id", "prompt_phrase_en"}, f"{where}.parameters", SelectionError)
            proposal = proposal_by_id.get(str(parameters["proposal_id"]))
            if proposal is None or candidate_id not in proposal["candidate_ids"]:
                raise SelectionError(f"atom {instance_id} has an unknown proposal binding")
            if parameters["value_id"] != proposal["value_id"] or parameters["prompt_phrase_en"] != proposal["prompt_phrase_en"]:
                raise SelectionError(f"atom {instance_id} proposal parameters drifted")
            if not _proposal_is_eligible(
                proposal,
                validated=validated,
                roles=roles,
                matched_prop_ids=matched_props,
                assets=assets,
            ):
                raise SelectionError(f"atom {instance_id} proposal is ineligible")
            proposal_atom_ids.add(instance_id)
            base_distance = dict(proposal["distance_profile"])
            base_load = dict(proposal["load_profile"])
            bridge_types = list(proposal["bridge_types"])
        elif "literal_realization_profile_id" in parameters:
            _require_exact_keys(
                parameters,
                {
                    "literal_realization_profile_id",
                    "mechanism_class_id",
                    "source_slot_id",
                    "resolved_owner_refs",
                    "value_phrase_bindings",
                    "request_text_sha256",
                },
                f"{where}.parameters",
                SelectionError,
            )
            profile = literal_realization_by_id.get(
                str(parameters["literal_realization_profile_id"])
            )
            if profile is None or candidate_id not in profile["candidate_group"]:
                raise SelectionError(
                    f"atom {instance_id} has an unknown literal realization binding"
                )
            if parameters != _literal_realization_parameters(profile, validated, assets):
                raise SelectionError(
                    f"atom {instance_id} literal realization parameters drifted"
                )
            if not any(
                item["id"] == profile["id"]
                for item in _matching_literal_visual_realization_profiles(
                    candidate, validated, assets
                )
            ):
                raise SelectionError(
                    f"atom {instance_id} literal realization no longer matches"
                )
            literal_realization_atom_ids.setdefault(str(profile["id"]), []).append(
                instance_id
            )
            base_distance = dict(candidate["runtime_contract"]["distance_profile"]["base"])
            base_load = dict(candidate["runtime_contract"]["load_profile"])
            bridge_types = list(candidate["runtime_contract"]["bridge_types"])
        else:
            if dict(parameters) != _candidate_parameters(candidate):
                raise SelectionError(f"atom {instance_id} parameters disagree with candidate")
            base_distance = dict(candidate["runtime_contract"]["distance_profile"]["base"])
            base_load = dict(candidate["runtime_contract"]["load_profile"])
            bridge_types = list(candidate["runtime_contract"]["bridge_types"])
        atom_profiles[instance_id] = {
            "candidate": candidate,
            "proposal": proposal,
            "distance": base_distance,
            "load": base_load,
            "bridge_types": bridge_types,
        }
        atom_by_id[instance_id] = atom
        selected_candidate_ids.add(candidate_id)
        provided_predicates.update(tuple(item) for item in candidate["postconditions"])
    if len(proposal_atom_ids) > 1:
        raise SelectionError("selection contains more than one proposal atom")
    literal_atom_total = sum(len(values) for values in literal_realization_atom_ids.values())
    if literal_atom_total > MAX_LITERAL_REALIZATION_ATOMS_TOTAL:
        raise SelectionError("selection exceeds the literal realization scene budget")
    literal_facet_counts: dict[str, int] = {}
    for profile_id, instance_ids in literal_realization_atom_ids.items():
        profile = literal_realization_by_id[profile_id]
        for instance_id in instance_ids:
            facet = str(atom_by_id[instance_id]["facet"])
            literal_facet_counts[facet] = literal_facet_counts.get(facet, 0) + 1
        if not _literal_visual_realization_profile_matches(profile, validated, assets):
            raise SelectionError(f"literal realization profile {profile_id} is not request-bound")
    if any(
        count > MAX_LITERAL_REALIZATION_ATOMS_PER_FACET
        for count in literal_facet_counts.values()
    ):
        raise SelectionError("selection exceeds a literal realization facet budget")
    for profile in assets.semantic_bindings["literal_visual_realization_profiles"]:
        if not _literal_visual_realization_profile_matches(profile, validated, assets):
            continue
        selected_count = len(literal_realization_atom_ids.get(str(profile["id"]), []))
        if profile["enforcement"] == "selected":
            expected_count = len(profile["candidate_group"]) if profile["quantifier"] == "all" else 1
            if selected_count != expected_count:
                raise SelectionError(
                    f"literal realization profile {profile['id']} violates its selection quantifier"
                )

    overlays = _selection_context_profile_overlays(
        assets=assets,
        validated=validated,
        roles=role_outputs,
        matched_prop_ids=matched_props,
        atoms=raw_atoms,
        provided_predicates=provided_predicates,
    )
    for instance_id, overlay in overlays.items():
        profile = atom_profiles[instance_id]
        profile["distance"] = _max_vector([profile["distance"], overlay["distance_profile"]], DISTANCE_AXIS_IDS)
        profile["load"] = _max_vector([profile["load"], overlay["load_profile"]], LOAD_AXIS_IDS)
        for bridge_type in overlay["bridge_types"]:
            if bridge_type not in profile["bridge_types"]:
                profile["bridge_types"].append(bridge_type)

    expected_claims: list[dict[str, Any]] = []
    pixel_contract = _require_mapping(scene["pixel_evidence_contract"], "selection.pixel_evidence_contract", SelectionError)
    _require_exact_keys(pixel_contract, {"required_scale_ids", "items", "core_anchor_item_ids", "event_item_ids", "contact_item_ids", "consequence_item_ids"}, "selection.pixel_evidence_contract", SelectionError)
    pixel_items = _require_list(pixel_contract["items"], "selection.pixel_evidence_contract.items", SelectionError)
    pixel_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_item in enumerate(pixel_items):
        where = f"selection.pixel_evidence_contract.items[{index}]"
        item = _require_mapping(raw_item, where, SelectionError)
        _require_exact_keys(item, {"item_id", "source_kind", "source_id", "kind", "minimum_scale_ids", "status"}, where, SelectionError)
        item_id = _require_nonempty_string(item["item_id"], f"{where}.item_id", SelectionError)
        if item_id in pixel_by_id:
            raise SelectionError(f"duplicate pixel evidence item: {item_id}")
        if item["status"] != "future_review_required":
            raise SelectionError(f"pixel evidence {item_id} claims an unperformed review")
        pixel_by_id[item_id] = item

    claim_counter = 0
    for instance_id, atom in atom_by_id.items():
        profile = atom_profiles[instance_id]
        candidate = profile["candidate"]
        if instance_id not in proposal_atom_ids:
            eligible, reason = _candidate_is_eligible(
                candidate,
                validated=validated,
                roles=roles,
                matched_prop_ids=matched_props,
                selected_candidate_ids=selected_candidate_ids,
                provided_predicates=provided_predicates,
                assets=assets,
            )
            if not eligible:
                raise SelectionError(f"atom {instance_id} is ineligible: {reason}")
        expected_distance = profile["distance"]
        expected_load = profile["load"]
        if atom["distance_vector"] != expected_distance or atom["distance_band"] != _distance_band(expected_distance):
            raise SelectionError(f"atom {instance_id} semantic distance drifted")
        if atom["load_vector"] != expected_load:
            raise SelectionError(f"atom {instance_id} semantic load drifted")
        expected_bindings: list[dict[str, str]] = []
        for role_id, requirement in candidate["runtime_contract"]["bindings"]:
            if role_id not in roles:
                if requirement == "required":
                    raise SelectionError(f"atom {instance_id} lacks required role {role_id}")
                continue
            expected_bindings.append(
                {
                    "role_id": role_id,
                    "node_id": str(roles[role_id]["value_id"]),
                    "requirement": "required" if requirement == "event_spine" else requirement,
                }
            )
        if atom["bindings"] != expected_bindings:
            raise SelectionError(f"atom {instance_id} event-role bindings drifted")
        atom_edge_ids = _require_string_list(atom["event_edge_ids"], f"atom {instance_id}.event_edge_ids", SelectionError, allow_empty=False)
        if len(atom_edge_ids) != 1:
            raise SelectionError(f"atom {instance_id} must bind one direct event edge")
        atom_edge = edge_by_id.get(atom_edge_ids[0])
        if atom_edge is None or atom_edge["from_node_id"] != "event_01" or atom_edge["to_node_id"] != instance_id or atom_edge["relation_id"] != f"realizes:{candidate['facet']}":
            raise SelectionError(f"atom {instance_id} direct event edge drifted")
        expected_atom_pixel_ids: list[str] = []
        for evidence in candidate["runtime_contract"]["pixel_evidence"]:
            item_id = f"pixel_atom_{instance_id}_{evidence['id'].replace('::', '_')}"
            expected_atom_pixel_ids.append(item_id)
            item = pixel_by_id.get(item_id)
            if item is None or item["source_kind"] != "atom" or item["source_id"] != instance_id or item["kind"] != evidence["kind"] or item["minimum_scale_ids"] != evidence["minimum_scale_ids"]:
                raise SelectionError(f"atom {instance_id} pixel evidence drifted")
        if atom["pixel_evidence_ids"] != expected_atom_pixel_ids:
            raise SelectionError(f"atom {instance_id} pixel-evidence references drifted")
        expected_atom_claim_ids: list[str] = []
        for raw_claim in candidate["runtime_contract"]["resource_claims"]:
            for kind, owner_id, amount, mode in _resolved_claim_tuples(
                raw_claim,
                validated,
                atom["parameters"].get("resolved_owner_refs", []),
            ):
                claim_counter += 1
                claim_id = f"claim_{claim_counter:02d}_{kind}"
                expected_atom_claim_ids.append(claim_id)
                expected_claims.append(
                    {
                        "claim_id": claim_id,
                        "resource_kind": kind,
                        "owner_id": owner_id,
                        "amount": amount,
                        "mode": mode,
                        "claimant_id": instance_id,
                        "phase_id": str(event["phase_id"]),
                        "evidence_required": True,
                    }
                )
        if atom["resource_claim_ids"] != expected_atom_claim_ids:
            raise SelectionError(f"atom {instance_id} resource-claim references drifted")

    if scene["resource_claims"] != expected_claims:
        raise SelectionError("selection resource claims do not reproduce candidate contracts")
    capacities = _resource_capacities(validated)
    exclusive: dict[tuple[str, str], int] = {}
    shared: dict[tuple[str, str], int] = {}
    for claim in expected_claims:
        key = (claim["owner_id"], claim["resource_kind"])
        if key not in capacities:
            raise SelectionError(f"resource claim has no declared capacity: {key}")
        if claim["mode"] == "exclusive":
            exclusive[key] = exclusive.get(key, 0) + int(claim["amount"])
        else:
            shared[key] = max(shared.get(key, 0), int(claim["amount"]))
    for key in set(exclusive) | set(shared):
        if exclusive.get(key, 0) + shared.get(key, 0) > capacities[key]:
            raise SelectionError(f"resource capacity exceeded: {key}")

    raw_bridges = _require_list(scene["bridges"], "selection.bridges", SelectionError)
    bridge_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_bridge in enumerate(raw_bridges):
        where = f"selection.bridges[{index}]"
        bridge = _require_mapping(raw_bridge, where, SelectionError)
        _require_exact_keys(bridge, {"bridge_id", "bridge_type", "candidate_id", "from_node_id", "to_node_id", "event_edge_ids", "pixel_evidence_ids"}, where, SelectionError)
        bridge_id = _require_nonempty_string(bridge["bridge_id"], f"{where}.bridge_id", SelectionError)
        if bridge_id in bridge_by_id or bridge["bridge_type"] not in set(ENTRY_BRIDGE_TYPES + MEDIATION_BRIDGE_TYPES + EXIT_BRIDGE_TYPES):
            raise SelectionError(f"duplicate or untyped bridge: {bridge_id}")
        candidate = assets.candidate_by_id.get(str(bridge["candidate_id"]))
        if candidate is None or candidate["role"] != "visual_atom":
            raise SelectionError(f"bridge {bridge_id} references a non-visual candidate")
        edge_ids = _require_string_list(bridge["event_edge_ids"], f"{where}.event_edge_ids", SelectionError, allow_empty=False)
        if len(edge_ids) != 1:
            raise SelectionError(f"bridge {bridge_id} must own exactly one edge")
        edge = edge_by_id.get(edge_ids[0])
        if edge is None or edge["from_node_id"] != bridge["from_node_id"] or edge["to_node_id"] != bridge["to_node_id"] or edge["relation_id"] != f"bridge:{bridge['bridge_type']}":
            raise SelectionError(f"bridge {bridge_id} edge binding drifted")
        expected_pixel_ids: list[str] = []
        for evidence in candidate["runtime_contract"]["pixel_evidence"]:
            item_id = f"pixel_bridge_{bridge_id}_{evidence['id'].replace('::', '_')}"
            expected_pixel_ids.append(item_id)
            item = pixel_by_id.get(item_id)
            if item is None or item["source_kind"] != "bridge" or item["source_id"] != bridge_id or item["kind"] != evidence["kind"] or item["minimum_scale_ids"] != evidence["minimum_scale_ids"]:
                raise SelectionError(f"bridge {bridge_id} pixel evidence drifted")
        if bridge["pixel_evidence_ids"] != expected_pixel_ids:
            raise SelectionError(f"bridge {bridge_id} pixel-evidence references drifted")
        bridge_by_id[bridge_id] = bridge

    for instance_id, atom in atom_by_id.items():
        expected_types = _choose_bridge_types(atom["distance_band"], atom_profiles[instance_id]["bridge_types"])
        actual = [bridge for bridge in raw_bridges if str(bridge["bridge_id"]).endswith(f"_{instance_id}")]
        if [bridge["bridge_type"] for bridge in actual] != expected_types:
            raise SelectionError(f"atom {instance_id} bridge path does not satisfy its distance band")
    fixed_distance_vectors, _ = _fixed_prop_vectors(matched_props, assets)
    fixed_remote_count = sum(
        1 for vector in fixed_distance_vectors if _distance_band(vector) == "far"
    )

    distance = _require_mapping(scene["semantic_distance_trace"], "selection.semantic_distance_trace", SelectionError)
    _require_exact_keys(distance, {"policy_id", "creativity", "target_band", "selected_band", "vector", "fixed_remote_count", "optional_remote_count", "max_optional_remote_count", "remote_atom_ids", "fallback_reason", "theme_displacement_band"}, "selection.semantic_distance_trace", SelectionError)
    if distance["policy_id"] != "typed_ordinal_distance_v1":
        raise SelectionError("semantic distance policy_id drifted")
    creativity = _require_number_range(distance["creativity"], 0.0, 1.0, "semantic_distance_trace.creativity", SelectionError)
    target_band = _creativity_target(creativity)
    max_optional = GLOBAL_OPTIONAL_REMOTE_MAX
    aggregate = _max_vector([*fixed_distance_vectors, *(atom["distance_vector"] for atom in raw_atoms)], DISTANCE_AXIS_IDS)
    remote_atom_ids = [atom["instance_id"] for atom in raw_atoms if atom["distance_band"] == "far"]
    proposal_remote = any(
        atom_profiles[instance_id]["proposal"] is not None
        and atom_profiles[instance_id]["proposal"]["remote_or_high_load"]
        for instance_id in atom_profiles
    )
    optional_remote = max(len(remote_atom_ids), 1 if proposal_remote else 0)
    if distance["target_band"] != target_band or distance["max_optional_remote_count"] != max_optional:
        raise SelectionError("creativity changed a hard gate or target contract")
    if distance["vector"] != aggregate or distance["selected_band"] != _distance_band(aggregate):
        raise SelectionError("aggregate semantic distance trace drifted")
    if distance["fixed_remote_count"] != fixed_remote_count or distance["optional_remote_count"] != optional_remote or distance["remote_atom_ids"] != remote_atom_ids:
        raise SelectionError("remote-premise accounting drifted")
    if (fixed_remote_count and optional_remote) or optional_remote > max_optional:
        raise SelectionError("remote-premise budget exceeded")
    if distance["theme_displacement_band"] != _theme_displacement_band(aggregate["theme"]):
        raise SelectionError("theme displacement trace drifted")

    required_scales = sorted(
        {scale for item in pixel_items for scale in item["minimum_scale_ids"]},
        key=lambda item: (item != "native", item),
    )
    if pixel_contract["required_scale_ids"] != required_scales:
        raise SelectionError("pixel evidence required scales drifted")
    referenced_pixel_ids = {
        *pixel_contract["core_anchor_item_ids"],
        *pixel_contract["event_item_ids"],
        *pixel_contract["contact_item_ids"],
        *pixel_contract["consequence_item_ids"],
        *(item_id for atom in raw_atoms for item_id in atom["pixel_evidence_ids"]),
        *(item_id for bridge in raw_bridges for item_id in bridge["pixel_evidence_ids"]),
    }
    if set(pixel_by_id) != referenced_pixel_ids:
        raise SelectionError("pixel evidence contains an orphan or missing item")
    if not pixel_contract["core_anchor_item_ids"] or not pixel_contract["event_item_ids"]:
        raise SelectionError("core/event pixel evidence is missing")
    if roles.get("result") is not None and not pixel_contract["consequence_item_ids"]:
        raise SelectionError("event consequence lacks a pixel-evidence obligation")

    replay_context_overlay_pairs = [
        (profile_id, instance_id)
        for instance_id, overlay in overlays.items()
        for profile_id in overlay["profile_ids"]
    ]
    expected_hard_gate_snapshot = _build_hard_gate_snapshot(
        request_text=request_text,
        selection=scene,
        assets=assets,
        validated=validated,
        matched_prop_ids=matched_props,
        context_overlay_pairs=replay_context_overlay_pairs,
    )
    if scene["hard_gate_snapshot"] != expected_hard_gate_snapshot:
        raise SelectionError("selection hard-gate snapshot does not independently reproduce")
    expected_postselection_trace = _revalidate_postselection_run_trace(
        scene["postselection_run_trace"],
        selection=scene,
        validated=validated,
        assets=assets,
        matched_prop_ids=matched_props,
        context_overlay_pairs=replay_context_overlay_pairs,
    )

    trace = _require_mapping(scene["selection_trace"], "selection.selection_trace", SelectionError)
    _require_exact_keys(trace, {"selection_mode", "seed", "scene_contract_sha256", "eligible_count_by_facet", "eligible_candidate_ids_by_facet", "candidate_rejections", "rejection_count_by_code", "eligible_proposal_family_ids", "eligible_proposal_profile_ids", "proposal_rejections", "eligible_proposal_count_by_band", "proposal_rejection_count_by_code", "beam_width", "tie_break_digest", "hard_gate_snapshot_sha256"}, "selection.selection_trace", SelectionError)
    if trace["selection_mode"] != "predicate_beam_v1" or trace["beam_width"] != int(assets.compatibility["solver"]["beam_width"]):
        raise SelectionError("selection solver trace drifted")
    if (
        isinstance(trace["seed"], bool)
        or not isinstance(trace["seed"], int)
        or not _is_sha256(trace["tie_break_digest"])
        or trace["hard_gate_snapshot_sha256"] != expected_hard_gate_snapshot["snapshot_sha256"]
    ):
        raise SelectionError("selection trace seed or digest is invalid")
    eligible_family_ids = _require_string_list(
        trace["eligible_proposal_family_ids"],
        "selection.selection_trace.eligible_proposal_family_ids",
        SelectionError,
    )
    if eligible_family_ids != sorted(set(eligible_family_ids)):
        raise SelectionError(
            "selection trace eligible proposal family IDs must be sorted and unique"
        )
    eligible_proposal_profile_ids = _require_string_list(
        trace["eligible_proposal_profile_ids"],
        "selection.selection_trace.eligible_proposal_profile_ids",
        SelectionError,
    )
    if eligible_proposal_profile_ids != sorted(set(eligible_proposal_profile_ids)):
        raise SelectionError(
            "selection trace eligible proposal profile IDs must be sorted and unique"
        )
    proposal_catalog_by_id = {
        str(profile["id"]): profile
        for profile in assets.candidates["proposal_profiles"]
    }
    if set(eligible_proposal_profile_ids) - set(proposal_catalog_by_id):
        raise SelectionError(
            "selection trace contains an unknown eligible proposal profile"
        )
    raw_proposal_rejections = _require_list(
        trace["proposal_rejections"],
        "selection.selection_trace.proposal_rejections",
        SelectionError,
    )
    proposal_rejections: list[dict[str, str]] = []
    for index, raw_rejection in enumerate(raw_proposal_rejections):
        where = f"selection.selection_trace.proposal_rejections[{index}]"
        rejection = _require_mapping(raw_rejection, where, SelectionError)
        _require_exact_keys(
            rejection,
            {"proposal_id", "reason_code"},
            where,
            SelectionError,
        )
        proposal_id = _require_nonempty_string(
            rejection["proposal_id"], f"{where}.proposal_id", SelectionError
        )
        reason_code = _require_nonempty_string(
            rejection["reason_code"], f"{where}.reason_code", SelectionError
        )
        if proposal_id not in proposal_catalog_by_id:
            raise SelectionError(
                "selection trace rejects an unknown proposal profile"
            )
        if reason_code not in PROPOSAL_REJECTION_REASON_IDS:
            raise SelectionError(
                "selection trace proposal rejection reason is outside the closed enum"
            )
        proposal_rejections.append(
            {"proposal_id": proposal_id, "reason_code": reason_code}
        )
    if proposal_rejections != sorted(
        proposal_rejections,
        key=lambda item: item["proposal_id"].encode("utf-8"),
    ) or len({item["proposal_id"] for item in proposal_rejections}) != len(
        proposal_rejections
    ):
        raise SelectionError(
            "selection trace proposal rejections must be byte-sorted and unique"
        )
    rejected_proposal_ids = {
        item["proposal_id"] for item in proposal_rejections
    }
    if (
        set(eligible_proposal_profile_ids) & rejected_proposal_ids
        or set(eligible_proposal_profile_ids) | rejected_proposal_ids
        != set(proposal_catalog_by_id)
    ):
        raise SelectionError(
            "selection trace proposal decision partition is incomplete"
        )
    replay_proposal_roles = _initial_roles(validated)
    replay_eligible_proposal_ids: list[str] = []
    replay_proposal_rejections: list[dict[str, str]] = []
    for proposal_profile in assets.candidates["proposal_profiles"]:
        eligible, reason_code = _proposal_eligibility_decision(
            proposal_profile,
            validated=validated,
            roles=replay_proposal_roles,
            matched_prop_ids=matched_props,
            assets=assets,
            mandatory_candidate_ids=replay_mandatory_candidate_ids,
        )
        if eligible:
            replay_eligible_proposal_ids.append(str(proposal_profile["id"]))
        else:
            replay_proposal_rejections.append(
                {
                    "proposal_id": str(proposal_profile["id"]),
                    "reason_code": str(reason_code),
                }
            )
    replay_eligible_proposal_ids.sort()
    replay_proposal_rejections.sort(
        key=lambda item: item["proposal_id"].encode("utf-8")
    )
    if (
        eligible_proposal_profile_ids != replay_eligible_proposal_ids
        or proposal_rejections != replay_proposal_rejections
    ):
        raise SelectionError(
            "selection trace proposal decisions do not independently replay"
        )
    expected_family_ids = sorted(
        str(proposal_catalog_by_id[profile_id]["semantic_family_id"])
        for profile_id in eligible_proposal_profile_ids
    )
    if eligible_family_ids != expected_family_ids:
        raise SelectionError(
            "selection trace proposal families are not exact profile projections"
        )
    expected_proposal_band_counts = {
        band: sum(
            _distance_band(proposal_catalog_by_id[profile_id]["distance_profile"])
            == band
            for profile_id in eligible_proposal_profile_ids
        )
        for band in ("near", "middle", "far")
    }
    if trace["eligible_proposal_count_by_band"] != expected_proposal_band_counts:
        raise SelectionError(
            "selection trace proposal band counts are not exact projections"
        )
    expected_proposal_rejection_counts = {
        reason_code: sum(
            item["reason_code"] == reason_code for item in proposal_rejections
        )
        for reason_code in PROPOSAL_REJECTION_REASON_IDS
        if any(
            item["reason_code"] == reason_code for item in proposal_rejections
        )
    }
    if trace["proposal_rejection_count_by_code"] != expected_proposal_rejection_counts:
        raise SelectionError(
            "selection trace proposal rejection counts are not exact projections"
        )
    eligible_ids_by_facet = _require_mapping(
        trace["eligible_candidate_ids_by_facet"],
        "selection.selection_trace.eligible_candidate_ids_by_facet",
        SelectionError,
    )
    if set(eligible_ids_by_facet) != set(FACET_IDS):
        raise SelectionError("selection trace eligible candidate facets drifted")
    traced_eligible_ids: set[str] = set()
    for facet in FACET_IDS:
        candidate_ids = _require_string_list(
            eligible_ids_by_facet[facet],
            f"selection.selection_trace.eligible_candidate_ids_by_facet.{facet}",
            SelectionError,
        )
        if candidate_ids != sorted(set(candidate_ids)):
            raise SelectionError("selection trace eligible candidate IDs must be sorted and unique")
        if any(
            candidate_id not in assets.candidate_by_id
            or assets.candidate_by_id[candidate_id]["role"] != "visual_atom"
            or assets.candidate_by_id[candidate_id]["facet"] != facet
            for candidate_id in candidate_ids
        ):
            raise SelectionError("selection trace eligible candidate IDs disagree with the asset catalog")
        traced_eligible_ids.update(candidate_ids)
    raw_rejections = _require_list(
        trace["candidate_rejections"],
        "selection.selection_trace.candidate_rejections",
        SelectionError,
    )
    rejected_ids: list[str] = []
    for index, raw_rejection in enumerate(raw_rejections):
        where = f"selection.selection_trace.candidate_rejections[{index}]"
        rejection = _require_mapping(raw_rejection, where, SelectionError)
        _require_exact_keys(rejection, {"candidate_id", "reason_code"}, where, SelectionError)
        candidate_id = _require_nonempty_string(
            rejection["candidate_id"], f"{where}.candidate_id", SelectionError
        )
        _require_nonempty_string(
            rejection["reason_code"], f"{where}.reason_code", SelectionError
        )
        candidate = assets.candidate_by_id.get(candidate_id)
        if candidate is None or candidate["role"] != "visual_atom":
            raise SelectionError("selection trace rejected candidate is not a visual source")
        rejected_ids.append(candidate_id)
    if rejected_ids != sorted(set(rejected_ids)):
        raise SelectionError("selection trace rejected candidate IDs must be sorted and unique")
    all_visual_ids = {
        candidate_id
        for candidate_id, candidate in assets.candidate_by_id.items()
        if candidate["role"] == "visual_atom"
    }
    if traced_eligible_ids & set(rejected_ids) or traced_eligible_ids | set(rejected_ids) != all_visual_ids:
        raise SelectionError("selection trace candidate eligibility partition is incomplete")
    if trace["eligible_count_by_facet"] != {
        facet: len(eligible_ids_by_facet[facet]) for facet in FACET_IDS
    }:
        raise SelectionError("selection trace eligible facet counts are not exact projections")
    for field in ("eligible_count_by_facet", "rejection_count_by_code", "eligible_proposal_count_by_band", "proposal_rejection_count_by_code"):
        counts = _require_mapping(trace[field], f"selection.selection_trace.{field}", SelectionError)
        if any(not isinstance(key, str) or not key or isinstance(value, bool) or not isinstance(value, int) or value < 0 for key, value in counts.items()):
            raise SelectionError(f"selection trace {field} is invalid")
    replay = build_universal_scene_selection(
        concept=request_text,
        scene_contract=scene["scene_contract"],
        topic_id=topic_id,
        format_id=format_id,
        creativity=creativity_value,
        seed=seed,
        assets=assets,
        prior_exposure_ids=exposure_ids,
    )
    if replay != scene:
        raise SelectionError(
            "selection does not exactly reproduce the canonical predicate solver result"
        )
    return _deep_canonical_copy(scene)


def validate_universal_scene_selection(
    selection: Mapping[str, Any],
    request_text: str,
    assets: UniversalSceneAssets,
    *,
    topic_id: str | None = None,
    format_id: str | None = None,
    creativity: float | None = None,
    seed: int | None = None,
    prior_exposure_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Fail-closed public wrapper for independent canonical replay."""

    try:
        return _validate_universal_scene_selection_impl(
            selection,
            request_text,
            assets,
            topic_id=topic_id,
            format_id=format_id,
            creativity=creativity,
            seed=seed,
            prior_exposure_ids=prior_exposure_ids,
        )
    except UniversalSceneRuntimeError:
        raise
    except (KeyError, IndexError, TypeError, ValueError, OverflowError) as exc:
        raise SelectionError(
            f"selection cannot be independently revalidated: {type(exc).__name__}: {exc}"
        ) from exc


__all__ = (
    "SCENE_CONTRACT_SCHEMA",
    "CANDIDATE_SCHEMA",
    "COMPATIBILITY_SCHEMA",
    "SELECTION_SCHEMA",
    "COMPOSITION_CARRIERS_SCHEMA",
    "CANDIDATE_FILENAME",
    "COMPATIBILITY_FILENAME",
    "RESEARCH_MANIFEST_FILENAME",
    "UniversalSceneRuntimeError",
    "InputContractError",
    "AssetValidationError",
    "SelectionError",
    "UniversalSceneAssets",
    "ValidatedSceneContract",
    "canonical_json_bytes",
    "canonical_sha256",
    "validate_scene_contract",
    "validate_universal_scene_assets",
    "load_universal_scene_assets",
    "build_universal_scene_selection",
    "validate_universal_scene_selection",
)
