#!/usr/bin/env python3
"""Fail-closed audit for an agent-composed subculture illustration prompt.

The candidate pack is the complete trust boundary for legacy commands.  For
the additive v3 universal-scene contract the auditor also reloads the sibling
assets, verifies their raw-byte hashes, and asks the universal runtime to
re-evaluate the retained canonical selection.  It then verifies that every
visible evidence phrase claimed by the composed object is literally present
in ``prompt_en``.

Exit status:
    0: pack integrity and composed-prompt audit pass
    1: pack is sound, but the composed prompt fails one or more checks
    2: CLI/JSON error or candidate-pack integrity failure
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, Sequence


CONTRACT_VERSION = "subculture-illustration-candidate-pack/v1"
CONTRACT_VERSION_V2 = "subculture-illustration-candidate-pack/v2"
CONTRACT_VERSION_V3 = "subculture-illustration-candidate-pack/v3"
SUPPORTED_CONTRACT_VERSIONS = (CONTRACT_VERSION, CONTRACT_VERSION_V2, CONTRACT_VERSION_V3)

COMPOSED_PROMPT_SCHEMA_V2 = "subculture-illustration-composed-prompt/v2"
COMPOSED_PROMPT_SCHEMA_V3 = "subculture-illustration-composed-prompt/v3"
SCENE_CONTRACT_SCHEMA = "subculture-illustration-scene-contract/v2"
UNIVERSAL_SCENE_SCHEMA = "illustration-universal-scene-selection/v1"
UNIVERSAL_SCENE_EVIDENCE_SCHEMA = "illustration-universal-scene-evidence/v1"
UNIVERSAL_COMPOSITION_CARRIERS_SCHEMA = "illustration-universal-composition-carriers/v1"
SECOND_LOOK_PLAN_SCHEMA = "illustration-second-look-plan/v1"
SECOND_LOOK_PLAN_CONTRACT_KEYS = {
    "schema",
    "required",
    "required_roles",
    "carrier_kinds",
    "risk_flags",
    "forbidden_as_sole",
    "allowed_review_scale_ids",
    "fallback_must_reference_selected_consequence",
}
SECOND_LOOK_PLAN_KEYS = {
    "schema",
    "selected_proposal_id",
    "reveal_phrase",
    "review_scale_ids",
    "primary_carrier",
    "fallback_carrier",
}
SECOND_LOOK_CARRIER_KEYS = {
    "carrier_kind",
    "carrier_phrase",
    "protected_locus_phrase",
    "consequence_phrase",
    "risk_flags",
}
SECOND_LOOK_ROLES = ("primary_carrier", "fallback_carrier")
SECOND_LOOK_CARRIER_KINDS = (
    "surface_state",
    "material_boundary",
    "isolated_contour",
    "object_relation",
    "environmental_trace",
    "projected_form",
    "dedicated_panel",
)
SECOND_LOOK_RISK_FLAGS = (
    "compound_anatomy",
    "subscale_symbol_decode",
    "overlapping_multi_limb_projection",
)

# These patterns are intentionally scoped to the phrases explicitly linked to
# one second-look carrier.  They are a narrow under-declaration backstop, not a
# general semantic classifier over the full prompt.
SECOND_LOOK_LINKED_RISK_PATTERNS: dict[str, tuple[str, ...]] = {
    "compound_anatomy": (
        r"\b(?:clasped|clasping|interlocked|interlocking|interlaced|intertwined|entangled|overlapping|merged|clustered)\s+(?:human\s+)?(?:hands?|fingers?|arms?|limbs?)\b",
        r"\b(?:two|three|four|both|multiple|several|\d+)\s+(?:human\s+)?(?:hands?|fingers?|arms?|limbs?)\b[^.!?;]{0,64}\b(?:clasp(?:ed|ing|s)?|interlock(?:ed|ing|s)?|interlac(?:ed|ing)|intertwin(?:ed|ing)|entangl(?:ed|ing)|overlap(?:ped|ping|s)?|merg(?:ed|ing)|cluster(?:ed|ing|s)?)\b",
    ),
    "subscale_symbol_decode": (
        r"\b(?:tiny|minute|microscopic|micro[- ]?scale|sub[- ]?scale|hairline|pinhead[- ]sized|coin[- ]sized|fingernail[- ]sized)\b[^.!?;]{0,64}\b(?:text|letters?|lettering|words?|glyphs?|runes?|symbols?|inscriptions?|writing|characters?|marks?)\b",
        r"\b(?:text|letters?|lettering|words?|glyphs?|runes?|symbols?|inscriptions?|writing|characters?|marks?)\b[^.!?;]{0,64}\b(?:tiny|minute|microscopic|micro[- ]?scale|sub[- ]?scale|hairline|pinhead[- ]sized|coin[- ]sized|fingernail[- ]sized)\b",
    ),
    "overlapping_multi_limb_projection": (
        r"\b(?:overlapping|merged|intersecting|crossing|entangled|clustered)\s+multi[- ]limb(?:ed)?\s+(?:shadow|silhouette|projection|reflection)s?\b",
        r"\bmulti[- ]limb(?:ed)?\s+(?:shadow|silhouette|projection|reflection)s?\b",
        r"\b(?:two|three|four|multiple|several|\d+)\s+(?:overlapping|merged|intersecting|crossing|entangled|clustered)?\s*(?:arms?|hands?|limbs?)\s+(?:shadows?|silhouettes?|projections?|reflections?)\b",
        r"\b(?:shadows?|silhouettes?|projections?|reflections?)\b[^.!?;]{0,80}\b(?:two|three|four|multiple|several|\d+)\s+(?:arms?|hands?|limbs?)\b[^.!?;]{0,48}\b(?:overlap|merge|intersect|cross|entangle|cluster)(?:ed|ing|s)?\b",
        r"\b(?:overlapping|merged|intersecting|crossing|entangled|clustered)\b[^.!?;]{0,48}\b(?:shadows?|silhouettes?|projections?|reflections?)\s+(?:of|from)\s+(?:two|three|four|multiple|several|\d+)\s+(?:arms?|hands?|limbs?)\b",
        r"\b(?:overlapping|merged|intersecting|crossing|entangled|clustered)\b[^.!?;]{0,48}\b(?:two|three|four|multiple|several|\d+)\s+(?:arms?|hands?|limbs?)\b[^.!?;]{0,48}\b(?:shadows?|silhouettes?|projections?|reflections?)\b",
    ),
}

VARIANT_FAMILY: dict[str, str] = {
    "single_illustration": "single_frame",
    "key_art": "key_art",
    "ensemble_key_art": "key_art",
    "responsive_key_art": "key_art",
    "light_novel_cover": "cover",
    "collectible_card": "card",
    "vertical_scroll_sequence": "vertical_sequence",
    "character_design_board": "adaptation_board",
    "merch_adaptation_board": "adaptation_board",
    "campaign_art_board": "adaptation_board",
}

# These are prompt-evidence keys, not aspect-ratio aliases.  A pack may add
# stricter fields, but cannot remove these canonical variant requirements.
FORMAT_REQUIRED_FIELDS: dict[str, tuple[str, ...]] = {
    "single_illustration": (
        "decisive_instant_phrase",
        "visual_rest_or_omission_phrase",
    ),
    "key_art": (
        "project_pillar_phrase",
        "cast_world_stake_hierarchy_phrase",
        "repeatable_signature_phrase",
    ),
    "ensemble_key_art": (
        "project_pillar_phrase",
        "cast_world_stake_hierarchy_phrase",
        "repeatable_signature_phrase",
        "silhouette_separation_phrase",
        "directed_relations_phrase",
    ),
    "responsive_key_art": (
        "project_pillar_phrase",
        "cast_world_stake_hierarchy_phrase",
        "repeatable_signature_phrase",
        "square_safe_zone_phrase",
        "wide_safe_zone_phrase",
        "vertical_safe_zone_phrase",
        "core_action_preservation_phrase",
        "secondary_clue_preservation_phrase",
    ),
    "light_novel_cover": (
        "story_promise_phrase",
        "relation_or_conflict_hook_phrase",
        "title_safe_area_phrase",
        "trim_safe_core_phrase",
    ),
    "collectible_card": (
        "frame_safe_silhouette_phrase",
        "hand_action_target_phrase",
        "effect_causality_phrase",
        "rarity_as_scene_consequence_phrase",
    ),
    "vertical_scroll_sequence": (
        "beat_one_phrase",
        "beat_two_phrase",
        "gutter_duration_phrase",
        "delayed_reveal_phrase",
        "identity_invariant_phrase",
    ),
    "character_design_board": (
        "representation_one_phrase",
        "representation_two_phrase",
        "identity_invariant_phrase",
        "format_specific_simplification_phrase",
        "state_or_view_change_phrase",
    ),
    "merch_adaptation_board": (
        "representation_one_phrase",
        "representation_two_phrase",
        "identity_invariant_phrase",
        "format_specific_simplification_phrase",
        "functional_anchor_phrase",
        "small_scale_simplification_phrase",
    ),
    "campaign_art_board": (
        "representation_one_phrase",
        "representation_two_phrase",
        "identity_invariant_phrase",
        "format_specific_simplification_phrase",
        "shared_signature_phrase",
        "distinct_application_phrase",
    ),
}

AUTHORIAL_REQUIRED_FIELDS = (
    "focal_hierarchy_phrase",
    "controlled_omission_phrase",
    "edge_or_mark_rule_phrase",
    "repeated_material_or_motif_rule_phrase",
)

VIEWER_REQUIRED_FIELDS = (
    "first_glance_hook_phrase",
    "second_look_reveal_phrase",
    "affect_actor_phrase",
    "affect_action_phrase",
    "affect_target_phrase",
    "affect_consequence_phrase",
)

FORMAT_CONTRACT_KEY_GROUPS = (
    ("hierarchy_contract",),
    ("crop_contract",),
    ("sequence_contract", "sequential_contract"),
    ("scale_contract", "scale_preservation_contract"),
    ("text_space_contract", "text_safe_contract"),
)

ASPECT_ONLY_KEYS = {
    "aspect_ratio",
    "aspect_ratio_phrase",
    "ratio",
    "ratio_phrase",
    "dimensions",
    "dimensions_phrase",
}

OUTCOME_CLAIM_PATTERNS = (
    r"\bthe viewer (?:feels?|will feel|experiences?|will experience)\b",
    r"\b(?:evokes?|creates?|guarantees?) (?:empathy|attachment|engagement|immersion|virality)\b",
    r"\b(?:memorable|viral|irresistible) image\b",
    r"\bmakes? the viewer (?:feel|care|buy|share|return)\b",
)

POST_RENDER_CLAIM_PATTERNS = (
    r"\brendered pixels? (?:pass|passed|prove|proved|show|showed|verify|verified|survive|survived)\b",
    r"\b(?:the )?(?:final|generated|rendered) image (?:passes|passed|proves|proved|verifies|verified)\b",
    r"\b(?:passes|passed|verified by|approved by) (?:the )?(?:pixel|render|thumbnail|native[- ]scale) review\b",
    r"\b(?:pixel|rendered[- ]image) review\s*:\s*(?:pass|approved|verified)\b",
)

POST_RENDER_EVIDENCE_KEY_PATTERN = re.compile(
    r"(?:^|_)(?:rendered_pixel_review|post_render|pixel_review|render_review|"
    r"thumbnail_review|native_review|image_review|qualification_status)(?:_|$)",
    flags=re.IGNORECASE,
)

NON_COMPOSITION_EVIDENCE_KEYS = {
    "prompt_contract",
    "rendered_pixel_review",
}

NAMED_STYLE_PATTERNS = (
    r"\bin (?:the )?style of\b",
    r"\b(?:style|art|design) of (?-i:[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){0,3})\b",
    r"\bby (?:artist|illustrator|mangaka|character designer)\b",
    r"\b(?:copy|copies|replicate|replicates|imitate|imitates) (?:the )?(?:art|look|style|visual language) of\b",
    r"\b(?:Studio Ghibli|Pixar|Disney|MAPPA|ufotable|Kyoto Animation|Trigger|Madhouse|Gainax|Sunrise|Bones)(?:'s)? style\b",
)

# This is deliberately a narrow, high-confidence backstop.  The authoritative
# declaration remains reference_boundary; a local regex cannot enumerate all
# artists, studios, franchises, or protected designs.
PROTECTED_IP_PATTERNS = (
    r"\b(?:Pok[eé]mon|Pikachu|Naruto|One Piece|Genshin Impact|Honkai|Demon Slayer)\b",
    r"\b(?:Dragon Ball|Gundam|Evangelion|Hello Kitty|Sanrio|Totoro)\b",
    r"\b(?:Marvel|DC Comics|Disney|Mickey Mouse|Star Wars|Harry Potter)\b",
    r"\b(?:Super Mario|The Legend of Zelda|Sonic the Hedgehog|League of Legends|Overwatch)\b",
    r"[©™®]",
)

UNIVERSAL_INFERENCE_PATTERNS = (
    r"\b(?:universally|inherently|intrinsically|naturally|always)\b[^.!?]{0,70}\b(?:means?|symboli[sz]es?|represents?|denotes?|proves?)\b",
    r"\b(?:color|colour|red|blue|white|black|circle|square|triangle|shape)s?\b[^.!?]{0,45}\b(?:always|inherently|universally)\b",
    r"\ball (?:Korean|Japanese|Chinese|Asian|East Asian) (?:people|viewers|audiences|characters)\b",
    r"\b(?:Korean|Japanese|Chinese|Asian|East Asian) (?:people|viewers|audiences|characters) (?:are|always|naturally|inherently)\b",
    r"\b(?:national|racial|cultural) personality\b",
)

DECORATIVE_SOUP_PATTERNS = (
    r"\b(?:decorative|ornamental|random) (?:motif|motifs|symbol|symbols|icons?)\b",
    r"\b(?:motif|symbol|icon) (?:collage|soup|pile|stack)\b",
    r"\b(?:scatter|sprinkle|fill)\b[^.!?]{0,35}\b(?:motifs?|symbols?|icons?)\b",
)

FORMAT_FORBIDDEN_PATTERNS: dict[str, tuple[tuple[str, str], ...]] = {
    "light_novel_cover": (
        (r"\b(?:readable|legible|spelled[- ]out|generated) title(?: text| lettering)?\b", "generated readable title text"),
        (r"\b(?:write|render|print) the (?:exact )?title\b", "generated readable title text"),
    ),
    "collectible_card": (
        (r"\b(?:paid rarity|rarity badge|rarity stars?|gem frame|gacha UI|monetization cue|SSR badge|UR badge|five[- ]star badge)\b", "paid-rarity UI or monetization cue"),
    ),
    "vertical_scroll_sequence": (
        (r"\b(?:single|one) (?:poster|image) stretched (?:to|into) (?:9:16|vertical)\b", "stretched-poster substitution"),
    ),
    "character_design_board": (
        (r"\bidentical (?:asset|image|pose) (?:reused|repeated|copied)\b", "identical asset reuse"),
    ),
    "merch_adaptation_board": (
        (r"\bidentical (?:asset|image|pose) (?:reused|repeated|copied)\b", "identical asset reuse"),
    ),
    "campaign_art_board": (
        (r"\bidentical (?:asset|image|pose) (?:reused|repeated|copied)\b", "identical asset reuse"),
    ),
}

UNIVERSAL_SCENE_KEYS = {
    "schema",
    "scene_contract",
    "composition_carriers",
    "identity_core",
    "slot_states",
    "selected_event",
    "atoms",
    "bridges",
    "resource_claims",
    "semantic_distance_trace",
    "pixel_evidence_contract",
    "hard_gate_snapshot",
    "creativity_invariant_trace",
    "postselection_run_trace",
    "selection_trace",
    "context_profile",
}
UNIVERSAL_COMPOSITION_CARRIER_KEYS = {
    "schema",
    "identity_core",
    "fixed_slots",
    "event_roles",
    "atoms",
    "bridges",
    "resources",
}
UNIVERSAL_EMBEDDED_SCENE_CONTRACT_KEYS = {
    "schema",
    "request_text_sha256",
    "identity_core",
    "participant_bindings",
    "slot_states",
    "event_roles",
    "context_profile",
}
UNIVERSAL_PACK_KEYS = {
    "contract_version",
    "pack_id",
    "request_contract",
    "format_profile",
    "visual_grammar",
    "authorial_contract",
    "viewer_contract",
    "guard_contract",
    "composition_contract",
    "safety",
    "negative_en",
    "asset_hashes",
    "provenance",
    "universal_scene",
}
UNIVERSAL_REQUEST_CONTRACT_KEYS = {
    "request_text",
    "mandatory_intents",
    "route_id",
    "topic_id",
    "route_source",
    "format_source",
    "matched_rule_ids",
    "matched_format_alias",
    "creativity",
    "prior_exposure_ids",
    "scene_contract_schema",
    "scene_contract_sha256",
}
UNIVERSAL_COMPOSITION_CONTRACT_KEYS = {
    "composer",
    "required_chosen_candidate_ids",
    "negative_must_match_exactly",
    "evidence_values_must_be_literal_prompt_substrings",
    "final_prompt_composition_deferred",
    "composed_schema",
}
UNIVERSAL_ASSET_HASH_KEYS = {
    "topic_crosswalk_sha256",
    "format_profiles_sha256",
    "mechanism_graph_sha256",
    "research_manifest_sha256",
    "universal_candidates_sha256",
    "universal_compatibility_sha256",
    "universal_semantic_bindings_sha256",
    "universal_research_manifest_sha256",
}
UNIVERSAL_IDENTITY_CORE_KEYS = {
    "entities",
    "scene_facts",
    "forbidden_facts",
    "capability_capacities",
}
UNIVERSAL_SLOT_KEYS = {
    "slot_id",
    "state",
    "value_ids",
    "request_phrases",
    "value_phrase_bindings",
}
UNIVERSAL_VALUE_PHRASE_BINDING_KEYS = {
    "value_id",
    "request_phrases",
    "semantic_anchor_groups",
}
UNIVERSAL_SEMANTIC_ANCHOR_GROUP_KEYS = {"alternatives", "required_polarity"}
UNIVERSAL_PARTICIPANT_BINDING_KEYS = {
    "role_id",
    "entity_ids",
    "primary_entity_id",
}
UNIVERSAL_CONTRACT_EVENT_ROLE_KEYS = {
    "role_id",
    "state",
    "value_id",
    "request_phrases",
    "semantic_anchor_groups",
}
UNIVERSAL_EVENT_KEYS = {"event_id", "phase_id", "roles", "spine_edges"}
UNIVERSAL_ATOM_KEYS = {
    "instance_id",
    "candidate_id",
    "facet",
    "parameters",
    "bindings",
    "event_edge_ids",
    "resource_claim_ids",
    "pixel_evidence_ids",
    "distance_vector",
    "distance_band",
    "load_vector",
}
UNIVERSAL_BRIDGE_KEYS = {
    "bridge_id",
    "bridge_type",
    "candidate_id",
    "from_node_id",
    "to_node_id",
    "event_edge_ids",
    "pixel_evidence_ids",
}
UNIVERSAL_RESOURCE_CLAIM_KEYS = {
    "claim_id",
    "resource_kind",
    "owner_id",
    "amount",
    "mode",
    "claimant_id",
    "phase_id",
    "evidence_required",
}
UNIVERSAL_DISTANCE_TRACE_KEYS = {
    "policy_id",
    "creativity",
    "target_band",
    "selected_band",
    "vector",
    "fixed_remote_count",
    "optional_remote_count",
    "max_optional_remote_count",
    "remote_atom_ids",
    "fallback_reason",
    "theme_displacement_band",
}
UNIVERSAL_PIXEL_EVIDENCE_KEYS = {
    "required_scale_ids",
    "items",
    "core_anchor_item_ids",
    "event_item_ids",
    "contact_item_ids",
    "consequence_item_ids",
}
UNIVERSAL_SELECTION_TRACE_KEYS = {
    "selection_mode",
    "seed",
    "scene_contract_sha256",
    "eligible_count_by_facet",
    "eligible_candidate_ids_by_facet",
    "candidate_rejections",
    "rejection_count_by_code",
    "eligible_proposal_family_ids",
    "eligible_proposal_profile_ids",
    "proposal_rejections",
    "eligible_proposal_count_by_band",
    "proposal_rejection_count_by_code",
    "beam_width",
    "tie_break_digest",
    "hard_gate_snapshot_sha256",
}
UNIVERSAL_CANDIDATE_REJECTION_KEYS = {"candidate_id", "reason_code"}
UNIVERSAL_PROPOSAL_REJECTION_KEYS = {"proposal_id", "reason_code"}
UNIVERSAL_CREATIVITY_INVARIANT_SCHEMA = (
    "illustration-universal-scene-creativity-invariant-trace/v1"
)
UNIVERSAL_CREATIVITY_INVARIANT_KEYS = {
    "schema",
    "request_sha256",
    "scene_contract_sha256",
    "asset_hashes",
    "reason_code_registry",
    "inventory",
    "eligible_proposals",
    "rejected_proposals",
    "eligible_candidate_ids",
    "rejected_candidates",
    "matched_prop_sense_hashes",
    "policy_source_contracts",
    "preselection_policy_decisions",
    "resource_capacities",
    "resource_feasibility",
    "cardinality_limits",
    "cardinality_feasibility",
    "guard_source_contracts",
    "guard_source_contracts_sha256",
    "complete_trace",
    "trace_sha256",
}
UNIVERSAL_CREATIVITY_INVENTORY_KEYS = {
    "proposal_profile_ids",
    "visual_candidate_ids",
    "guard_candidate_ids",
    "policy_source_record_ids",
    "preselection_policy_decision_ids",
    "resource_feasibility_record_ids",
    "cardinality_limit_ids",
    "cardinality_feasibility_record_ids",
}
UNIVERSAL_INVARIANT_ELIGIBLE_PROPOSAL_KEYS = {
    "record_id",
    "semantic_signature",
    "distance_band",
}
UNIVERSAL_INVARIANT_REJECTED_SOURCE_KEYS = {
    "record_id",
    "outcome",
    "reason_codes",
}
UNIVERSAL_POLICY_SOURCE_CONTRACT_KEYS = {
    "record_id",
    "source_kind",
    "source_id",
    "evaluation_stage",
    "policy_mode",
    "declared_outcome",
    "source_contract_sha256",
}
UNIVERSAL_PRESELECTION_POLICY_DECISION_KEYS = {
    "record_id",
    "applicable",
    "outcome",
    "reason_codes",
}
UNIVERSAL_RESOURCE_CAPACITY_ROW_KEYS = {
    "owner_scope_hash",
    "resource_kind",
    "capacity",
    "state",
}
UNIVERSAL_PRESELECTION_FEASIBILITY_KEYS = {
    "record_id",
    "source_kind",
    "source_id",
    "source_record_sha256",
    "trial_sha256",
    "checks",
    "outcome",
    "reason_codes",
}
UNIVERSAL_RESOURCE_FEASIBILITY_CHECK_KEYS = {
    "owner_scope_hash",
    "resource_kind",
    "exclusive_required",
    "shared_required",
    "capacity",
    "fits",
}
UNIVERSAL_CARDINALITY_LIMIT_KEYS = {
    "record_id",
    "source_kind",
    "metric_id",
    "evaluation_stage",
    "scope_kind",
    "scope_id",
    "minimum",
    "maximum",
}
UNIVERSAL_CARDINALITY_FEASIBILITY_KEYS = {
    "record_id",
    "source_kind",
    "source_id",
    "source_record_sha256",
    "trial_sha256",
    "limit_results",
    "outcome",
    "reason_codes",
}
UNIVERSAL_CARDINALITY_LIMIT_RESULT_KEYS = {"limit_id", "fits"}
UNIVERSAL_GUARD_SOURCE_CONTRACT_KEYS = {
    "record_id",
    "source_candidate_id",
    "predicate_id",
    "source_contract_sha256",
    "role",
    "evaluation_stage",
    "research_topic_ids",
    "provenance_record_ids",
    "stage",
    "violation_code",
    "when_all",
    "require_all",
    "declared_outcome",
}
UNIVERSAL_POSTSELECTION_TRACE_SCHEMA = (
    "illustration-universal-scene-postselection-run-trace/v1"
)
UNIVERSAL_POSTSELECTION_TRACE_KEYS = {
    "schema",
    "invariant_trace_sha256",
    "guard_source_contracts_sha256",
    "selected_projection",
    "guard_executions",
    "guard_executions_sha256",
    "hard_gate_pass",
    "universal_rule_executions",
    "universal_rule_executions_sha256",
    "postselection_cardinality_decisions",
    "postselection_cardinality_decisions_sha256",
    "postselection_cardinality_invariant_sha256",
    "postselection_resource_pass",
    "policy_gate_pass",
    "cardinality_gate_pass",
    "complete_trace",
    "trace_sha256",
}
UNIVERSAL_POSTSELECTION_SELECTED_PROJECTION_KEYS = {
    "fixed_contract_projection_sha256",
    "contract_role_projection_sha256",
    "protected_final_role_projection_sha256",
    "protected_scene_facts_sha256",
    "runtime_open_role_projection_sha256",
    "selected_semantic_family_signature",
    "selected_proposal_profile_sha256",
    "selected_candidate_roster_sha256",
    "protected_candidate_roster_sha256",
    "proposal_primary_roster_sha256",
    "optional_candidate_roster_sha256",
    "active_context_profile_ids_sha256",
    "selected_atom_count",
    "selected_facet_multiset",
    "aggregate_resource_footprint",
    "resource_claim_count",
    "mandatory_literal_atom_count",
    "context_profile_carrier_count",
    "fixed_remote_count",
    "optional_remote_count",
    "global_optional_remote_max",
    "semantic_distance_sha256",
    "optional_remote_projection_sha256",
    "bridge_topology_sha256",
    "pixel_evidence_chain_sha256",
    "pixel_evidence_count",
    "pixel_kind_multiset_sha256",
    "protected_pixel_evidence_sha256",
    "pixel_evidence_contract_pass",
}
UNIVERSAL_POSTSELECTION_GUARD_EXECUTION_KEYS = {
    "guard_id",
    "predicate_id",
    "source_contract_sha256",
    "applicable",
    "predicate_passed",
    "predicate_evidence_sha256",
    "outcome",
    "reason_codes",
}
UNIVERSAL_RULE_EXECUTION_KEYS = {
    "rule_id",
    "source_contract_sha256",
    "violated",
    "outcome",
    "reason_codes",
}
UNIVERSAL_POSTSELECTION_CARDINALITY_KEYS = {
    "limit_id",
    "observed",
    "minimum",
    "maximum",
    "fits",
}
UNIVERSAL_PRESELECTION_TRIAL_SCHEMA = (
    "illustration-universal-scene-preselection-trial/v1"
)
UNIVERSAL_PRESELECTION_TRIAL_ENTRY_KEYS = {
    "entry_ordinal",
    "source_kind",
    "source_id",
    "candidate_id",
    "literal_realization_profile_ids",
    "parameters_sha256",
}
UNIVERSAL_PRESELECTION_TRIAL_CLAIM_KEYS = {
    "entry_ordinal",
    "raw_claim_ordinal",
    "resolved_owner_ordinal",
    "owner_scope_hash",
    "resource_kind",
    "amount",
    "mode",
}
UNIVERSAL_CARDINALITY_LIMIT_IDS = (
    "compatibility_budget__display_bundles",
    "compatibility_budget__display_primitives_per_bundle",
    "compatibility_budget__event_spines",
    "compatibility_budget__gestures",
    "compatibility_budget__optional_props",
    "compatibility_budget__orphan_atoms",
    "compatibility_budget__perceived_affect_hypotheses",
    "compatibility_budget__phases",
    "compatibility_budget__pose_support_solutions",
    "compatibility_budget__primary_actions",
    "compatibility_budget__primary_environment_roles",
    "compatibility_budget__relation_topologies",
    "compatibility_budget__remote_or_high_load_optional_premises",
    "compatibility_budget__second_independent_premises",
    "runtime_limit__context_profile_carriers",
    "runtime_limit__global_optional_remote",
    "runtime_limit__literal_realization_atoms_per_facet",
    "runtime_limit__literal_realization_atoms_total",
    "runtime_limit__selected_resource_claims_total",
    "runtime_limit__selected_visual_atoms_total",
)
UNIVERSAL_PRESELECTION_CARDINALITY_LIMIT_IDS = {
    "runtime_limit__literal_realization_atoms_per_facet",
    "runtime_limit__literal_realization_atoms_total",
}
UNIVERSAL_DECISION_REASON_CODE_IDS = (
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
UNIVERSAL_HARD_GATE_SCHEMA = "illustration-universal-hard-gate-snapshot/v1"
UNIVERSAL_HARD_GATE_KEYS = {
    "schema",
    "asset_hashes",
    "semantic_effect_registry_sha256",
    "source_coverage",
    "selected_source_refs",
    "observed_effect_ids",
    "semantic_load_max",
    "guard_executions",
    "hard_gate_pass",
    "snapshot_sha256",
}
UNIVERSAL_HARD_GATE_ASSET_HASH_KEYS = {
    "universal_candidates_sha256",
    "universal_compatibility_sha256",
    "universal_semantic_bindings_sha256",
    "universal_research_manifest_sha256",
}
UNIVERSAL_EFFECT_SOURCE_COUNTS = {
    "visual_candidate": 65,
    "proposal_profile": 12,
    "context_profile": 18,
    "bridge_type": 7,
    "resource_kind": 24,
    "total": 126,
}
UNIVERSAL_SELECTED_SOURCE_KEYS = {
    "instance_kind",
    "instance_id",
    "scope",
    "source_profile_refs",
    "contract_effect_profile_ids",
    "effect_occurrences",
    "load_vector",
}
UNIVERSAL_SELECTED_INSTANCE_KINDS = {
    "event_role",
    "fixed_prop",
    "atom",
    "bridge",
    "resource_claim",
    "proposal",
    "context_overlay",
    "identity_fact",
    "slot_state",
    "context_value",
}
UNIVERSAL_EFFECT_SOURCE_KINDS = {
    "visual_candidate",
    "proposal_profile",
    "context_profile",
    "bridge_type",
    "resource_kind",
}
UNIVERSAL_EFFECT_IDS = {
    "active_weapon_discharge",
    "combat_opponent_assignment",
    "combat_target_assignment",
    "human_face_attachment",
    "human_hand_attachment",
    "human_limb_attachment",
    "navigation_instrument_use",
    "romantic_contact",
    "scene_promise_hijack",
}
UNIVERSAL_CONTRACT_EFFECT_PROFILE_IDS = {
    f"contract_effect_{effect_id}" for effect_id in UNIVERSAL_EFFECT_IDS
}
UNIVERSAL_CONTRACT_EFFECT_PROFILE_KEYS = {
    "id",
    "effect_id",
    "source_targets",
    "semantic_value_ids",
    "literal_aliases",
    "required_literal_groups",
    "polarity",
    "subject_binding",
}
UNIVERSAL_CONTRACT_EFFECT_TARGET_KEYS = {"source_kind", "source_id"}
UNIVERSAL_CONTRACT_EFFECT_SOURCE_KINDS = {
    "request",
    "identity_fact",
    "slot",
    "event_role",
    "context",
}
UNIVERSAL_CONTRACT_EFFECT_SUBJECT_BINDINGS = {
    "source_entity",
    "actor",
    "target",
    "recipient",
    "scene",
}
UNIVERSAL_CONTEXT_LITERAL_PROFILE_KEYS = {
    "id",
    "field",
    "value",
    "required_literal_groups",
    "polarity",
}
UNIVERSAL_CONTEXT_LITERAL_KEYS = {
    ("era_technology", "decommissioned_firearm"),
    ("era_technology", "industrial"),
    ("tone", "investigative"),
    ("tone", "quiet_everyday"),
    ("violence", "active"),
    ("violence", "closed"),
    ("violence", "nonviolent"),
}
UNIVERSAL_LITERAL_REALIZATION_PROFILE_KEYS = {
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
}
UNIVERSAL_LITERAL_REALIZATION_PARTICIPANT_KEYS = {
    "role_id",
    "entity_quantifier",
}
UNIVERSAL_LITERAL_REALIZATION_PARAMETER_KEYS = {
    "literal_realization_profile_id",
    "mechanism_class_id",
    "source_slot_id",
    "resolved_owner_refs",
    "value_phrase_bindings",
    "request_text_sha256",
}
UNIVERSAL_LITERAL_REALIZATION_OWNER_KEYS = {"role_id", "entity_id"}
UNIVERSAL_LITERAL_REALIZATION_SCOPE_IDS = {
    "fixed_value_bindings",
    "slot_phrases",
    "request_text",
}
UNIVERSAL_LITERAL_REALIZATION_MAX_PER_FACET = 2
UNIVERSAL_LITERAL_REALIZATION_MAX_TOTAL = 10
UNIVERSAL_SELECTED_VISUAL_ATOM_MAX_TOTAL = 18
UNIVERSAL_SELECTED_RESOURCE_CLAIM_MAX_TOTAL = 32
UNIVERSAL_LITERAL_AUTHENTICATION_HARD_SEPARATORS = (
    ".", ";", ":", "!", "?", "。", "；", "：", "！", "？",
    " but ", " however ", " although ", " even though ",
    " 하지만 ", " 그러나 ", " 반면 ",
    " しかし ", " 一方 ", " 但 ", " 但是 ", " 然而 ",
)
UNIVERSAL_LITERAL_CLAUSE_SEPARATORS = (
    ".", ",", ";", ":", "!", "?", "。", "，", "；", "：", "！", "？",
    " — ", " – ", " but ", " and ", " then ", " while ", " however ",
    " whereas ", " and then ", " even though ", " although ",
    " 하지만 ", " 그러나 ", " 반면 ", " 동안 ", "하면서 ", "하고 ",
    " しかし ", " 一方 ", " ながら ", " 但 ", " 但是 ", " 然而 ", " 同时 ",
)
UNIVERSAL_LITERAL_GRAMMATICAL_SUFFIXES = (
    "을", "를", "이", "가", "은", "는", "과", "와", "의", "에",
    "에서", "에게", "으로", "로", "도", "만", "처럼", "보다", "랑",
    "이라고", "라고", "이며", "이나", "라도", "까지", "부터", "조차",
    "마저", "께서", "한테", "하고", "を", "が", "は", "の", "に",
    "で", "と", "も", "へ",
)
UNIVERSAL_SOURCE_REF_KEYS = {"source_kind", "source_id"}
UNIVERSAL_EFFECT_OCCURRENCE_KEYS = {
    "effect_id",
    "source_profile_id",
    "subject_ref",
}
UNIVERSAL_GUARD_EXECUTION_KEYS = {
    "guard_id",
    "source_candidate_id",
    "source_contract_sha256",
    "stage",
    "violation_code",
    "applicable",
    "predicate_results",
    "outcome",
    "reason_codes",
}
UNIVERSAL_GUARD_PREDICATE_KEYS = {
    "predicate_id",
    "passed",
    "binding_ids",
}
UNIVERSAL_GUARD_STAGES = {
    "action",
    "bridge",
    "consequence",
    "display",
    "event_spine",
    "hard_gate",
    "load",
    "normalize",
    "phase",
    "prop",
    "prop_state",
    "rank",
    "relation",
    "resource",
}
UNIVERSAL_REQUIRED_GUARD_IDS = {
    "dpa_inner_state_nonclaim_guard",
    "event_role_frames_role_assignment_guard",
    "uao_weapon_event_guard",
    "ubp_embodiment_capability_guard",
    "uer_narrative_inference_guard",
    "uer_weapon_role_target_guard",
    "usc_lexical_sense_ambiguity_guard",
    "usc_relation_relation_truth_guard",
    "usl_theme_hijack_guard",
}
UNIVERSAL_GUARD_EXECUTION_PREDICATES = {
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
UNIVERSAL_EVIDENCE_KEYS = {
    "schema",
    "scene_block_phrase",
    "identity_core_phrases",
    "fixed_slot_phrases",
    "event_role_phrases",
    "atom_phrases",
    "bridge_phrases",
    "resource_phrases",
    "salience_phrases",
    "consequence_phrase",
}
UNIVERSAL_SALIENCE_KEYS = {
    "primary_core_event_phrase",
    "secondary_discovery_phrase",
    "controlled_rest_phrase",
    "remote_carrier_phrase",
}
UNIVERSAL_DISTANCE_AXES = (
    "theme",
    "era_technology",
    "tone",
    "violence",
    "social",
    "scale",
    "salience_displacement",
)
UNIVERSAL_LOAD_AXES = (
    "physical",
    "occupancy",
    "affective_valence",
    "affective_arousal",
    "violence",
    "visual_salience",
    "scene_importance",
    "theme_displacement",
)
UNIVERSAL_PIXEL_EVIDENCE_KIND_IDS = (
    "contact",
    "orientation",
    "state_boundary",
    "support",
    "path",
    "residue",
    "display",
)
UNIVERSAL_ENTITY_RESOURCE_KINDS = {
    "manipulator",
    "attention_channel",
    "head_orientation",
    "facial_display",
    "support_contact",
    "mouth",
    "appendage",
    "wing_appendage",
    "locomotor_contact",
    "body_orientation",
    "body_contour_display",
    "surface_signal",
    "light_emission",
    "internal_luminance_display",
    "mobile_ear_pair",
    "wing_axis_pair",
    "tail_axis",
    "mechanical_state_displacement",
    "external_anchor",
}
UNIVERSAL_SCENE_RESOURCE_CAPACITIES = {
    "focal_primary": 1,
    "focal_secondary": 1,
    "foreground_salience": 1,
    "event_peak": 1,
    "prop_slot": 1,
}
UNIVERSAL_FIXED_PROP_ATOMS: dict[str, set[str]] = {
    "uao_global_prop_apple": {"apple", "one_apple", "prop_apple"},
    "uao_global_prop_hammer": {"hammer", "small_hammer", "prop_hammer"},
    "uao_global_prop_machine_gun": {
        "decommissioned_machine_gun",
        "unmarked_decommissioned_machine_gun",
        "prop_decommissioned_machine_gun",
    },
}
UNIVERSAL_FIXED_PROP_CONCEPT_BY_CANDIDATE = {
    "uao_global_prop_apple": "prop_apple",
    "uao_global_prop_hammer": "prop_hammer",
    "uao_global_prop_machine_gun": "prop_decommissioned_machine_gun",
}
UNIVERSAL_PROP_LITERAL_SENSE_DISAMBIGUATORS: dict[str, set[str]] = {
    "prop_hammer": {"mallet"},
}
UNIVERSAL_FIXED_PROP_DISTANCE_VECTORS: dict[str, dict[str, int]] = {
    "uao_global_prop_apple": {
        "theme": 0,
        "era_technology": 0,
        "tone": 0,
        "violence": 0,
        "social": 0,
        "scale": 0,
        "salience_displacement": 0,
    },
    "uao_global_prop_hammer": {
        "theme": 0,
        "era_technology": 1,
        "tone": 0,
        "violence": 1,
        "social": 0,
        "scale": 1,
        "salience_displacement": 1,
    },
    "uao_global_prop_machine_gun": {
        "theme": 2,
        "era_technology": 2,
        "tone": 2,
        "violence": 3,
        "social": 0,
        "scale": 1,
        "salience_displacement": 3,
    },
}
UNIVERSAL_SLOT_IDS = ("expression", "pose", "action", "relation", "prop", "environment")
UNIVERSAL_SLOT_STATES = ("fixed", "closed", "open")
UNIVERSAL_FACET_IDS = {
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
}
UNIVERSAL_ROLE_IDS = ("actor", "action", "target", "instrument", "recipient", "result", "location", "phase")
UNIVERSAL_BRIDGE_ENTRY_TYPES = {"affordance", "motivation", "identity_contrast"}
UNIVERSAL_BRIDGE_MEDIATION_TYPES = {"mechanics", "ownership"}
UNIVERSAL_BRIDGE_EXIT_TYPES = {"state_change", "consequence"}
UNIVERSAL_HEX_64 = re.compile(r"[0-9a-f]{64}")
UNIVERSAL_CARRIER_INTERNAL_TOKENS = {
    "atom",
    "candidate",
    "cbg",
    "dpa",
    "ecs",
    "facet",
    "gha",
    "global",
    "id",
    "ofm",
    "predicate",
    "profile",
    "sdc",
    "sptg",
    "uao",
    "ubp",
    "ugf",
    "usc",
    "ush",
    "usl",
}
UNIVERSAL_UNSUPPORTED_INFERENCE_PATTERNS: tuple[tuple[str, str], ...] = (
    (
        r"\b(?:smil(?:e|es|ing)|frown(?:s|ing)?|eyes?|brows?|eyelids?|lips?|mouth|face|expression|facial (?:appearance|motion|movement|expression))\b"
        r"[^.!?;:]{0,90}\b(?:proves?|confirms?|reveals?|means?|demonstrates?|establish(?:es|ed)?|certif(?:y|ies|ied)|verif(?:y|ies|ied)|indicat(?:e|es|ed)|signals?|signal(?:ed|ing)|impl(?:y|ies|ied)|tells?(?: us)?|told us|betrays?|betrayed|guarantees?|guaranteed|shows?(?: us)?(?: that)?|makes? it clear(?: that)?|lets? us know(?: that)?)\b"
        r"[^.!?;:]{0,90}\b(?:emotion|personality|diagnosis|culture|inner state|true (?:emotion|feeling|fear|state)|fearful|adult(?:hood)?|age(?![- ]worn\b)|feels?|is (?:sad|angry|happy|afraid|adult|young|old|introverted|extroverted))\b",
        "facial motion cannot establish inner emotion, personality, diagnosis, culture, or age as truth",
    ),
    (
        r"\b(?:gaze|eye contact|looks? at|looking at|proximity|stands? close|standing close)\b"
        r"[^.!?;:]{0,90}\b(?:proves?|confirms?|reveals?|means?|demonstrates?|establish(?:es|ed)?|certif(?:y|ies|ied)|verif(?:y|ies|ied)|indicat(?:e|es|ed)|signals?|signal(?:ed|ing)|impl(?:y|ies|ied)|tells?(?: us)?|told us|betrays?|betrayed|guarantees?|guaranteed|shows?(?: us)?(?: that)?|makes? it clear(?: that)?|lets? us know(?: that)?)\b"
        r"[^.!?;:]{0,90}\b(?:intent|romance|romantic|dominance|dominant|ownership|owns?|belongs?|loves?|wants?)\b",
        "gaze or proximity cannot establish intent, romance, dominance, or ownership as truth",
    ),
    (
        r"\b(?:weapon|gun|rifle|machine gun)\b[^.!?;:]{0,100}\b(?:allowed|safe|compliant|exempt|permitted|included|depicted safely)\b"
        r"[^.!?;:]{0,100}\b(?:creative|creativity|stylized|style|small|low[- ]salience|narrative|fictional)\b",
        "weapon boundaries cannot be bypassed through creativity, style, salience, or narrative role",
    ),
    (
        r"\b(?:emotion|personality|diagnosis|culture|adult(?:hood)?|age|fear|sadness|anger|happiness)\b"
        r"[^.!?;:]{0,90}\b(?:is|are|was|were)\s+(?:proven|confirmed|revealed|demonstrated|shown|certified|verified)\b"
        r"[^.!?;:]{0,90}\bby\b[^.!?;:]{0,50}\b(?:smil(?:e|es|ing)|frown(?:s|ing)?|eyes?|brows?|eyelids?|lips?|mouth|face|expression|facial (?:appearance|motion|movement|expression))\b",
        "facial motion cannot establish inner emotion, personality, diagnosis, culture, or age as truth",
    ),
    (
        r"\b(?:intent|romance|romantic intent|dominance|ownership|love|desire)\b"
        r"[^.!?;:]{0,90}\b(?:is|are|was|were)\s+(?:proven|confirmed|revealed|demonstrated|shown|established|certified|verified)\b"
        r"[^.!?;:]{0,90}\bby\b[^.!?;:]{0,50}\b(?:gaze|eye contact|proximity|standing close)\b",
        "gaze or proximity cannot establish intent, romance, dominance, or ownership as truth",
    ),
    (
        r"\b(?:because|since|as|due to|by virtue of)\b[^.!?;:]{0,100}\b(?:creative|creativity|stylized|style|small|low[- ]salience|narrative|fictional)\b"
        r"[^.!?;:]{0,100}\b(?:weapon|gun|rifle|machine gun)\b[^.!?;:]{0,50}\b(?:is|becomes?|remains?)\s+(?:allowed|safe|compliant|exempt|permitted|included|depicted safely)\b",
        "weapon boundaries cannot be bypassed through creativity, style, salience, or narrative role",
    ),
    (
        r"\b(?:creative|creativity|stylized|stylization|style|small|low[- ]salience|narrative|fictional)\b"
        r"[^.!?;:]{0,90}\b(?:renders?|makes?|qualif(?:y|ies|ied))\b[^.!?;:]{0,70}"
        r"\b(?:weapon|gun|rifle|machine gun)\b[^.!?;:]{0,50}\b(?:allowed|safe|compliant|exempt|permitted|included|depicted safely)\b",
        "weapon boundaries cannot be bypassed through creativity, style, salience, or narrative role",
    ),
    (
        r"\b(?:fictional|stylized|small|low[- ]salience)\s+(?:weapon|gun|rifle|machine gun)\b"
        r"[^.!?;:]{0,50}\b(?:is|are|becomes?|remains?)\s+(?:allowed|safe|compliant|exempt|permitted|included|depicted safely)\b",
        "weapon boundaries cannot be bypassed through creativity, style, salience, or narrative role",
    ),
    (
        r"\b(?:weapon|gun|rifle|machine gun)\b[^.!?;:]{0,70}"
        r"\b(?:creative|stylized|small|low[- ]salience|narrative|fictional)\b[^.!?;:]{0,40}"
        r"\b(?:therefore|thus|so|hence)?\s*(?:allowed|safe|compliant|exempt|permitted|included|depicted safely)\b",
        "weapon boundaries cannot be bypassed through creativity, style, salience, or narrative role",
    ),
    (
        r"\b(?:creative|creativity|stylization|style|small size|low[- ]salience|narrative role|fictional(?:ity)?)\b"
        r"[^.!?;:]{0,50}\b(?:excuses?|exempts?|permits?|allows?|justif(?:y|ies|ied))\b[^.!?;:]{0,50}"
        r"\b(?:weapon|gun|rifle|machine gun)\b",
        "weapon boundaries cannot be bypassed through creativity, style, salience, or narrative role",
    ),
    (
        r"\b(?:smil(?:e|es|ing)|frown(?:s|ing)?|eyes?|brows?|eyelids?|lips?|mouth|face|expression|facial (?:appearance|motion|movement|expression))\b"
        r"[^.!?;:]{0,50}\b(?:is|are|serves? as|acts? as)\s+(?:proof|evidence|confirmation|an? indicator|an? sign)\s+(?:of|that)\b"
        r"[^.!?;:]{0,70}\b(?:emotion|personality|diagnosis|culture|inner state|fear|fearful|adult(?:hood)?|age(?![- ]worn\b)|sadness|anger|happiness)\b",
        "facial motion cannot establish inner emotion, personality, diagnosis, culture, or age as truth",
    ),
    (
        r"\b(?:we|one|the viewer)\s+can\s+infer\b[^.!?;:]{0,80}"
        r"\b(?:emotion|personality|diagnosis|culture|inner state|fear|adult(?:hood)?|age|sadness|anger|happiness|is (?:adult|young|old))\b"
        r"[^.!?;:]{0,70}\bfrom\b[^.!?;:]{0,40}\b(?:smil(?:e|es|ing)|frown(?:s|ing)?|eyes?|brows?|eyelids?|lips?|mouth|face|expression|facial (?:appearance|motion|movement|expression))\b",
        "facial motion cannot establish inner emotion, personality, diagnosis, culture, or age as truth",
    ),
    (
        r"\bfrom\s+(?:(?:her|his|their|the)\s+)?(?:smil(?:e|es|ing)|frown(?:s|ing)?|eyes?|brows?|eyelids?|lips?|mouth|face|expression|facial (?:appearance|motion|movement|expression))\b"
        r"[^.!?;:]{0,70}\b(?:we|one|the viewer)\s+can\s+infer\b[^.!?;:]{0,80}"
        r"\b(?:emotion|personality|diagnosis|culture|inner state|fear|adult(?:hood)?|age|sadness|anger|happiness|is (?:adult|young|old))\b",
        "facial motion cannot establish inner emotion, personality, diagnosis, culture, or age as truth",
    ),
    (
        r"\b(?:smil(?:e|es|ing)|frown(?:s|ing)?|eyes?|brows?|eyelids?|lips?|mouth|face|expression|facial (?:appearance|motion|movement|expression))\b"
        r"[^.!?;:]{0,50}\b(?:identif(?:y|ies|ied)\s+\w+\s+as|reads? as)\b[^.!?;:]{0,50}"
        r"\b(?:fear|fearful|adult|young|old|introverted|extroverted|sad|angry|happy)\b",
        "facial motion cannot establish inner emotion, personality, diagnosis, culture, or age as truth",
    ),
    (
        r"\b(?:emotion|personality|diagnosis|culture|inner state|fear|adult(?:hood)?|age|sadness|anger|happiness)\b"
        r"[^.!?;:]{0,40}\b(?:is|are)\s+(?:evident|apparent)\s+from\b[^.!?;:]{0,50}"
        r"\b(?:smil(?:e|es|ing)|frown(?:s|ing)?|eyes?|brows?|eyelids?|lips?|mouth|face|expression|facial (?:appearance|motion|movement|expression))\b",
        "facial motion cannot establish inner emotion, personality, diagnosis, culture, or age as truth",
    ),
    (
        r"\b(?:she|he|they|the subject)\s+looks?\s+(?:adult|young|old|afraid|sad|angry|happy)\b"
        r"[^.!?;:]{0,35}\bbecause\b[^.!?;:]{0,45}\b(?:smil(?:e|es|ing)|frown(?:s|ing)?|eyes?|brows?|eyelids?|lips?|mouth|face|expression|facial (?:appearance|motion|movement|expression))\b",
        "facial motion cannot establish inner emotion, personality, diagnosis, culture, or age as truth",
    ),
    (
        r"\b(?:fictionality|imaginary nature|stylization|stylized nature|small size|low[- ]salience)\b"
        r"[^.!?;:]{0,55}(?:\bmakes?\s+(?:it|the\s+(?:weapon|gun|rifle|machine gun))\s+"
        r"(?:permissible|allowed|safe)\b|\b(?:legitimizes?|licenses?|permits?|allows?)\b"
        r"[^.!?;:]{0,40}\b(?:weapon|gun|rifle|machine gun|it)\b|"
        r"\b(?:renders?|qualif(?:y|ies|ied))\s+(?:the\s+)?(?:weapon|gun|rifle|machine gun|it)\s+"
        r"(?:as\s+)?(?:permissible|allowed|safe|permitted)\b)",
        "weapon boundaries cannot be bypassed through creativity, style, salience, or narrative role",
    ),
    (
        r"\b(?:weapon|gun|rifle|machine gun)\b[^.!?;:]{0,60}"
        r"\b(?:is|becomes?|may be|can be)\s+(?:harmless|safe|permitted|allowed|included|shown|depicted)\b"
        r"[^.!?;:]{0,45}\b(?:thanks to|on account of|because of|due to)\b[^.!?;:]{0,45}"
        r"\b(?:fictional(?:ity| nature)?|imaginary nature|stylized|stylization|small|low[- ]salience)\b",
        "weapon boundaries cannot be bypassed through creativity, style, salience, or narrative role",
    ),
)


class AuditInputError(ValueError):
    """Raised for CLI transport or JSON shape errors."""


def issue(check: str, reason: str, **details: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"check": check, "reason": reason}
    result.update(details)
    return result


def load_json_arg(raw: str) -> Any:
    """Load an inline JSON value or a UTF-8 JSON file."""

    value = str(raw or "").strip()
    if not value:
        raise AuditInputError("JSON argument must not be empty")
    if value.startswith("{") or value.startswith("["):
        return json.loads(value)
    return json.loads(Path(value).read_text(encoding="utf-8"))


def first_pack(payload: Any) -> dict[str, Any]:
    """Accept exactly one candidate pack, optionally wrapped in a list."""

    if isinstance(payload, list):
        if len(payload) != 1:
            raise AuditInputError("candidate pack list must contain exactly one pack")
        payload = payload[0]
    if not isinstance(payload, dict):
        raise AuditInputError("candidate pack must be a JSON object or a one-item list")
    return payload


def composed_object(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise AuditInputError("composed prompt must be a JSON object")
    return payload


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _audit_plain_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _audit_plain_json(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_audit_plain_json(item) for item in value]
    return value


def _audit_canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        canonical_json(_audit_plain_json(value)).encode("utf-8")
    ).hexdigest()


def _audit_utf8_sorted(values: Iterable[str]) -> list[str]:
    return sorted(
        {str(value) for value in values}, key=lambda value: value.encode("utf-8")
    )


def _audit_semantic_family_normalize(value: Any) -> str:
    normalized = unicodedata.normalize("NFKC", str(value)).casefold()
    normalized = re.sub(r"[_-]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _audit_proposal_semantic_family_payload(
    profile: Mapping[str, Any], candidate_by_id: Mapping[str, Any]
) -> dict[str, Any]:
    """Recompute the frozen semantic-family payload from complete raw sources."""

    normalized_roles: dict[str, str] = {}
    event_roles = (
        dict(profile.get("event_roles"))
        if isinstance(profile.get("event_roles"), Mapping)
        else {}
    )
    for role_id in UNIVERSAL_ROLE_IDS:
        raw_value = event_roles.get(role_id)
        if raw_value is None:
            normalized_roles[role_id] = "null"
            continue
        raw_normalized = unicodedata.normalize("NFKC", str(raw_value)).casefold()
        if raw_normalized in {"$identity_actor", "$actor"}:
            normalized_roles[role_id] = "$actor"
        elif raw_normalized in {"$scene_location", "$location"}:
            normalized_roles[role_id] = "$location"
        else:
            normalized_roles[role_id] = _audit_semantic_family_normalize(raw_value)

    reduced: dict[tuple[str, str, str], int] = {}
    for candidate_id in _string_list(profile.get("candidate_ids")) or []:
        candidate = (
            dict(candidate_by_id.get(candidate_id))
            if isinstance(candidate_by_id.get(candidate_id), Mapping)
            else {}
        )
        runtime_contract = (
            dict(candidate.get("runtime_contract"))
            if isinstance(candidate.get("runtime_contract"), Mapping)
            else {}
        )
        claims = runtime_contract.get("resource_claims")
        if not isinstance(claims, list):
            raise ValueError(f"proposal member {candidate_id} lacks typed resource claims")
        for raw_claim in claims:
            if (
                not isinstance(raw_claim, Sequence)
                or isinstance(raw_claim, (str, bytes))
                or len(raw_claim) != 4
            ):
                raise ValueError(f"proposal member {candidate_id} has malformed resource claim")
            resource_kind, raw_owner, raw_amount, mode = raw_claim
            if (
                not _is_nonempty_string(resource_kind)
                or not _is_nonempty_string(raw_owner)
                or not isinstance(raw_amount, int)
                or isinstance(raw_amount, bool)
                or raw_amount <= 0
                or mode not in {"exclusive", "shared"}
            ):
                raise ValueError(f"proposal member {candidate_id} has invalid resource claim")
            owner = str(raw_owner)
            if owner in {"actor", "scene"}:
                owner_scope = owner
            elif owner in UNIVERSAL_ROLE_IDS:
                owner_scope = f"role:{_audit_semantic_family_normalize(owner)}"
            else:
                raise ValueError(f"proposal member {candidate_id} has unknown claim owner {owner}")
            key = (
                owner_scope,
                _audit_semantic_family_normalize(resource_kind),
                str(mode),
            )
            amount = int(raw_amount)
            if mode == "exclusive":
                reduced[key] = reduced.get(key, 0) + amount
            else:
                reduced[key] = max(reduced.get(key, 0), amount)
    resource_footprint = [
        {
            "owner_scope": owner_scope,
            "resource_kind": resource_kind,
            "mode": mode,
            "amount": reduced[(owner_scope, resource_kind, mode)],
        }
        for owner_scope, resource_kind, mode in sorted(reduced)
    ]
    return {
        "schema": "subculture-illustration-semantic-family-key/v1",
        "slot": _audit_semantic_family_normalize(profile.get("slot_id")),
        "prop_concept": _audit_semantic_family_normalize(profile.get("value_id")),
        "event_frame": normalized_roles,
        "resource_footprint": resource_footprint,
    }


def computed_pack_id(pack: Mapping[str, Any]) -> str:
    """Return the canonical 16-hex pack ID with pack_id nulled."""

    hashable = dict(pack)
    hashable["pack_id"] = None
    return hashlib.sha256(canonical_json(hashable).encode("utf-8")).hexdigest()[:16]


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any) -> list[str] | None:
    if not isinstance(value, list):
        return None
    if any(not _is_nonempty_string(item) for item in value):
        return None
    return [str(item) for item in value]


def _mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _unique_string_list(value: Any) -> list[str] | None:
    items = _string_list(value)
    if items is None or len(items) != len(set(items)):
        return None
    return items


def _hex64(value: Any) -> bool:
    return isinstance(value, str) and UNIVERSAL_HEX_64.fullmatch(value) is not None


def _closed_int(value: Any, minimum: int, maximum: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and minimum <= value <= maximum


def _universal_distance_band(vector: Mapping[str, Any]) -> str | None:
    if set(vector) != set(UNIVERSAL_DISTANCE_AXES):
        return None
    values = [vector.get(axis) for axis in UNIVERSAL_DISTANCE_AXES]
    if any(not _closed_int(value, 0, 3) for value in values):
        return None
    numeric = [int(value) for value in values]
    if 3 in numeric or sum(numeric) >= 10:
        return "far"
    if 2 in numeric or sum(numeric) >= 4:
        return "middle"
    return "near"


def _creativity_band(value: Any) -> str | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    creativity = float(value)
    if not 0.0 <= creativity <= 1.0:
        return None
    if creativity < 0.25:
        return "near"
    if creativity < 0.75:
        return "middle"
    return "far"


def _literal_request_phrases(
    fact: Any,
    request_text: str,
    *,
    check: str,
    fact_kind: str,
) -> list[dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    if not isinstance(fact, dict):
        return [issue(check, f"{fact_kind} must be an object")]
    if set(fact) != {"id", "request_phrases"}:
        errors.append(
            issue(
                check,
                f"{fact_kind} must retain the exact literal-bound fact field set",
                missing=sorted({"id", "request_phrases"} - set(fact)),
                unexpected=sorted(set(fact) - {"id", "request_phrases"}),
            )
        )
    fact_id = fact.get("id")
    phrases = _unique_string_list(fact.get("request_phrases"))
    if not _is_nonempty_string(fact_id):
        errors.append(issue(check, f"{fact_kind} id must be a nonempty string"))
    if not phrases:
        errors.append(issue(check, f"{fact_kind} must retain nonempty literal request_phrases", fact_id=fact_id))
    else:
        normalized_request = _normalized_literal_text(request_text)
        missing = [
            phrase
            for phrase in phrases
            if _normalized_literal_text(phrase) not in normalized_request
        ]
        if missing:
            errors.append(
                issue(
                    check,
                    f"{fact_kind} request_phrases must be literal request_text substrings",
                    fact_id=fact_id,
                    missing=missing,
                )
            )
    return errors


def _pixel_item_ids(items: Any) -> tuple[list[str], list[dict[str, Any]]]:
    """Read compact pixel obligations without treating them as render results."""

    errors: list[dict[str, Any]] = []
    if not isinstance(items, list):
        return [], [issue("universal_pixel_evidence", "pixel_evidence_contract.items must be a list")]
    item_ids: list[str] = []
    for index, item in enumerate(items):
        if isinstance(item, str):
            item_id = item
        elif isinstance(item, dict):
            item_id = item.get("id") or item.get("item_id")
            for key, value in item.items():
                if POST_RENDER_EVIDENCE_KEY_PATTERN.search(str(key)):
                    errors.append(
                        issue(
                            "universal_pixel_evidence",
                            "pre-render pixel obligation cannot embed a post-render review field",
                            index=index,
                            field=key,
                        )
                    )
                if isinstance(value, str) and any(
                    re.search(pattern, value, flags=re.IGNORECASE) for pattern in POST_RENDER_CLAIM_PATTERNS
                ):
                    errors.append(
                        issue(
                            "universal_pixel_evidence",
                            "pre-render pixel obligation cannot claim that rendered pixels passed",
                            index=index,
                            field=key,
                        )
                    )
        else:
            item_id = None
        if not _is_nonempty_string(item_id):
            errors.append(issue("universal_pixel_evidence", "every pixel obligation must have a nonempty id", index=index))
        else:
            item_ids.append(str(item_id))
    if len(item_ids) != len(set(item_ids)):
        errors.append(issue("universal_pixel_evidence", "pixel obligation ids must be unique", ids=item_ids))
    return item_ids, errors


def _normalized_contract_phrase(value: Any) -> str:
    """Normalize only for equality checks; literal prompt coverage stays exact."""

    if not isinstance(value, str):
        return ""
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _normalized_literal_text(value: Any) -> str:
    """Mirror the v3 scene-contract NFKC/casefold/whitespace boundary."""

    return _normalized_contract_phrase(value)


def _is_cjk_lexical_character(character: str) -> bool:
    """Return whether one code point is an individual CJK lexical unit."""

    codepoint = ord(character)
    return any(
        lower <= codepoint <= upper
        for lower, upper in (
            (0x1100, 0x11FF),
            (0x3040, 0x30FF),
            (0x3100, 0x318F),
            (0x31A0, 0x31BF),
            (0x31F0, 0x31FF),
            (0x3400, 0x4DBF),
            (0x4E00, 0x9FFF),
            (0xAC00, 0xD7AF),
            (0xF900, 0xFAFF),
            (0x20000, 0x2FA1F),
        )
    )


def _universal_lexical_unit_count(value: str) -> int:
    """Count Unicode letter/number runs plus individual CJK characters."""

    normalized = unicodedata.normalize("NFKC", value)
    count = 0
    in_run = False
    for index, character in enumerate(normalized):
        if _is_cjk_lexical_character(character):
            if in_run:
                count += 1
                in_run = False
            count += 1
            continue
        category = unicodedata.category(character)
        if category.startswith(("L", "N")) or (in_run and category.startswith("M")):
            in_run = True
            continue
        if (
            in_run
            and character in {"-", "'", "’"}
            and index + 1 < len(normalized)
            and unicodedata.category(normalized[index + 1]).startswith(("L", "N"))
        ):
            continue
        if in_run:
            count += 1
            in_run = False
    return count + int(in_run)


def _exact_object_keys(
    value: Any,
    expected_keys: Iterable[str],
    *,
    check: str,
    object_name: str,
) -> list[dict[str, Any]]:
    if not isinstance(value, dict):
        return [issue(check, f"{object_name} must be an object")]
    expected = set(expected_keys)
    actual = set(value)
    if actual == expected:
        return []
    return [
        issue(
            check,
            f"{object_name} must have the exact v2 field set",
            missing=sorted(expected - actual),
            unexpected=sorted(actual - expected),
        )
    ]


def _semantic_anchor_group_shape_failures(
    value: Any,
    phrases: Sequence[str],
    *,
    fixed: bool,
    check: str,
    object_name: str,
) -> list[dict[str, Any]]:
    """Validate v2 typed semantic authority without trusting value IDs."""

    failures: list[dict[str, Any]] = []
    if not isinstance(value, list):
        return [issue(check, f"{object_name} must be a list")]
    if not fixed:
        if value:
            failures.append(
                issue(
                    check,
                    f"{object_name} must be empty outside a fixed record",
                    actual=value,
                )
            )
        return failures
    if not 1 <= len(value) <= 4:
        return [
            issue(
                check,
                f"{object_name} must contain one to four typed semantic anchors",
                actual=value,
            )
        ]
    normalized_phrases = [_normalized_literal_text(phrase) for phrase in phrases]
    signatures: set[tuple[tuple[str, ...], str]] = set()
    for index, raw_group in enumerate(value):
        failures.extend(
            _exact_object_keys(
                raw_group,
                UNIVERSAL_SEMANTIC_ANCHOR_GROUP_KEYS,
                check=check,
                object_name=f"{object_name}[{index}]",
            )
        )
        if not isinstance(raw_group, dict):
            continue
        alternatives = _unique_string_list(raw_group.get("alternatives"))
        polarity = raw_group.get("required_polarity")
        if not alternatives:
            failures.append(
                issue(
                    check,
                    "semantic anchor alternatives must be a nonempty unique string list",
                    object_name=object_name,
                    index=index,
                )
            )
            continue
        normalized_alternatives = tuple(
            _normalized_literal_text(alternative) for alternative in alternatives
        )
        if any(
            not any(alternative in phrase for phrase in normalized_phrases)
            for alternative in normalized_alternatives
        ):
            failures.append(
                issue(
                    check,
                    "semantic anchor alternatives must be literal substrings of their own authority phrases",
                    object_name=object_name,
                    index=index,
                    alternatives=alternatives,
                )
            )
        if polarity not in {"affirmative", "negated"}:
            failures.append(
                issue(
                    check,
                    "semantic anchor required_polarity is outside the closed enum",
                    object_name=object_name,
                    index=index,
                    actual=polarity,
                )
            )
            continue
        signature = (normalized_alternatives, str(polarity))
        if signature in signatures:
            failures.append(
                issue(
                    check,
                    "semantic anchor groups must be unique",
                    object_name=object_name,
                    index=index,
                )
            )
        signatures.add(signature)
    return failures


def _match_is_negated(text: str, start: int) -> bool:
    """Recognize a nearby plain-language exclusion, not full English scope."""

    prefix = text[max(0, start - 64) : start]
    local_clause = re.split(r"[.!?;,:]", prefix)[-1]
    return re.search(
        r"\b(?:no|not|cannot|can['’]t|without|avoid|exclude|never|forbid(?:den)?)\b",
        local_clause,
        flags=re.IGNORECASE,
    ) is not None


def _predicate_is_directly_negated(text: str, start: int) -> bool:
    """Bind negation to the predicate immediately following it."""

    prefix = text[max(0, start - 72) : start]
    local_clause = re.split(
        r"[.!?;,:]|\b(?:but|however|yet|although|whereas)\b",
        prefix,
        flags=re.IGNORECASE,
    )[-1]
    return re.search(
        r"(?:\b(?:do|does|did|can|could|should|would|will|must|may|might|"
        r"is|are|was|were|has|have|had)\s+not(?!\s+only\b)|"
        r"\b(?:cannot|can't|never|not(?!\s+only\b)|no))\s+"
        r"(?:(?:really|actually|directly)\s+)?$",
        local_clause,
        flags=re.IGNORECASE,
    ) is not None


def _nonnegated_matches(pattern: str, text: str) -> list[re.Match[str]]:
    return [
        match
        for match in re.finditer(pattern, text, flags=re.IGNORECASE)
        if not _match_is_negated(text, match.start())
    ]


def _excerpt_has_affirmative_forbidden_inference(excerpt: str) -> bool:
    """Reject a positive contrast tail even when another outcome is negated."""

    predicate_pattern = (
        r"\b(?:prove(?:s|d)?|confirm(?:s|ed)?|reveal(?:s|ed)?|mean(?:s|t)?|"
        r"demonstrate(?:s|d)?|show(?:s|ed)?|establish(?:es|ed)?|"
        r"certif(?:y|ies|ied)|verif(?:y|ies|ied)|indicat(?:e|es|ed)|"
        r"signal(?:s|ed|ing)?|impl(?:y|ies|ied)|tell(?:s|ing)?|told|"
        r"betray(?:s|ed|ing)?|guarantee(?:s|d|ing)?|makes? it clear|lets? us know)\b"
    )
    outcome_pattern = re.compile(
        r"\b(?:emotion|personality|diagnosis|culture|inner state|fearful|fear|"
        r"sadness|anger|happiness|adult(?:hood)?|age(?![- ]worn\b)|intent|romance|romantic|"
        r"dominance|ownership|love|desire|introverted|extroverted)\b",
        flags=re.IGNORECASE,
    )
    clauses = [
        clause.strip()
        for clause in re.split(
            r"[.!?;]+|\b(?:but|however|yet|although|whereas)\b",
            excerpt,
            flags=re.IGNORECASE,
        )
        if clause.strip()
    ]
    for clause in clauses:
        for predicate in re.finditer(predicate_pattern, clause, flags=re.IGNORECASE):
            if _predicate_is_directly_negated(clause, predicate.start()):
                continue
            following = clause[predicate.end() : predicate.end() + 120]
            for outcome in outcome_pattern.finditer(following):
                absolute_start = predicate.end() + outcome.start()
                predicate_to_outcome = clause[predicate.end() : absolute_start]
                if not _match_is_negated(
                    predicate_to_outcome, len(predicate_to_outcome)
                ):
                    return True
    passive_predicate_pattern = re.compile(
        r"\b(?:is|are|was|were)\s+(?:not\s+)?"
        r"(?:proven|confirmed|revealed|demonstrated|shown|established|certified|"
        r"verified|indicated|signaled|implied|betrayed|guaranteed)\b",
        flags=re.IGNORECASE,
    )
    for clause in clauses:
        for match in passive_predicate_pattern.finditer(clause):
            predicate = re.search(
                r"\b(?:proven|confirmed|revealed|demonstrated|shown|established|certified|verified|indicated|signaled|implied|betrayed|guaranteed)\b",
                match.group(0),
                flags=re.IGNORECASE,
            )
            if predicate is not None and not _predicate_is_directly_negated(
                clause,
                match.start() + predicate.start(),
            ):
                return True

    strong_relation_predicates = re.compile(
        r"\b(?:proof|evidence|confirmation|indicator|sign|infer|identif(?:y|ies|ied)|"
        r"reads?|evident|apparent|looks?|makes?|renders?|qualif(?:y|ies|ied)|"
        r"legitimizes?|licenses?|permits?|allows?|harmless|permissible)\b",
        flags=re.IGNORECASE,
    )
    excerpt_has_flagged_weapon_premise = re.search(
        r"\b(?:creative|creativity|stylized|stylization|style|small|low[- ]salience|narrative|fictional(?:ity)?)\b",
        excerpt,
        flags=re.IGNORECASE,
    ) is not None
    for clause in clauses:
        for relation in strong_relation_predicates.finditer(clause):
            if _predicate_is_directly_negated(clause, relation.start()):
                continue
            relation_text = relation.group(0).casefold()
            governed_outcome = False
            for outcome in outcome_pattern.finditer(clause):
                if outcome.end() <= relation.start() and not re.fullmatch(
                    r"(?:evident|apparent)", relation_text, flags=re.IGNORECASE
                ):
                    continue
                if outcome.start() >= relation.end():
                    relation_to_outcome = clause[relation.end() : outcome.start()]
                    if _match_is_negated(
                        relation_to_outcome, len(relation_to_outcome)
                    ):
                        continue
                governed_outcome = True
                break
            if governed_outcome:
                return True
            if (
                re.search(r"\b(?:weapon|gun|rifle|machine gun)\b", clause, flags=re.IGNORECASE)
                and excerpt_has_flagged_weapon_premise
                and re.fullmatch(
                    r"(?:makes?|renders?|qualif(?:y|ies|ied)|legitimizes?|licenses?|permits?|allows?|harmless|permissible)",
                    relation_text,
                    flags=re.IGNORECASE,
                )
            ):
                return True

    flagged_premise = (
        r"(?:creative|creativity|stylized|stylization|style|small|low[- ]salience|"
        r"narrative|fictional)"
    )
    weapon_cause_patterns = (
        rf"\b(?:because|due to|by virtue of)\s+(?:it\s+is\s+)?{flagged_premise}\b",
        rf"\b{flagged_premise}\b[^.!?;]{{0,70}}\b(?:renders?|makes?|qualif(?:y|ies|ied))\b",
    )
    for clause in clauses:
        for pattern in weapon_cause_patterns:
            for match in re.finditer(pattern, clause, flags=re.IGNORECASE):
                if _match_is_negated(clause, match.start()):
                    continue
                causal_predicate = re.search(
                    r"\b(?:renders?|makes?|qualif(?:y|ies|ied))\b",
                    match.group(0),
                    flags=re.IGNORECASE,
                )
                if causal_predicate is not None and _predicate_is_directly_negated(
                    clause,
                    match.start() + causal_predicate.start(),
                ):
                    continue
                return True
    return False


def _unsupported_inference_is_explicitly_negated(excerpt: str) -> bool:
    """Do not punish a prompt that explicitly rejects the forbidden claim."""

    if _excerpt_has_affirmative_forbidden_inference(excerpt):
        return False
    if re.search(
        r"\b(?:weapon|gun|rifle|machine gun)\b[^.!?;:]{0,80}",
        excerpt,
        flags=re.IGNORECASE,
    ) is not None:
        physical_safety_basis = re.search(
            r"\b(?:safe|permitted|allowed|compliant)\b[^.!?;:]{0,70}"
            r"\b(?:because|since|as|due to|by virtue of)\b[^.!?;:]{0,50}"
            r"\b(?:decommissioned|disabled|unloaded|locked|secured|inert)\b|"
            r"\b(?:because|since|as|due to|by virtue of)\b[^.!?;:]{0,50}"
            r"\b(?:decommissioned|disabled|unloaded|locked|secured|inert)\b[^.!?;:]{0,70}"
            r"\b(?:safe|permitted|allowed|compliant)\b",
            excerpt,
            flags=re.IGNORECASE,
        )
        if physical_safety_basis is not None:
            return True
    return any(
        re.search(pattern, excerpt, flags=re.IGNORECASE) is not None
        for pattern in (
            r"\b(?:do|does|did|can|could|should|would|will|must|may|might)\s+not\s+(?:prove|confirm|reveal|mean|demonstrate|show|establish|certify|verify|indicate|signal|imply|tell|betray|guarantee)\b",
            r"\b(?:cannot|can't|never)\s+(?:prove|confirm|reveal|mean|demonstrate|show|establish|certify|verify|indicate|signal|imply|tell|betray|guarantee)\b",
            r"\b(?:do|does|did|can|could|should|would|will|must|may|might)\s+not\s+(?:make it clear|let us know)\b",
            r"\b(?:cannot|can't|never)\s+(?:make it clear|let us know)\b",
            r"\b(?:cannot|can't|never)\s+(?:renders?|qualif(?:y|ies|ied)|establish(?:es|ed)?)\b",
            r"\bwithout\s+(?:proving|confirming|revealing|demonstrating|showing|establishing|certifying|verifying|indicating|signaling|implying|betraying|guaranteeing)\b",
            r"\b(?:is|are|was|were)\s+not\s+(?:proven|confirmed|revealed|demonstrated|shown|established|certified|verified|indicated|signaled|implied|betrayed|guaranteed)\b",
            r"\b(?:do|does|did|can|could|should|would|will|must|may|might)\s+not\s+"
            r"(?:make(?:s)?(?:\s+(?:it|the\s+(?:weapon|gun|rifle|machine gun)))?\s+"
            r"(?:permissible|allowed|safe)|legitimiz(?:e|es)|licens(?:e|es)|permit|allow)\b",
            r"\bnot\s+(?!only\b)(?:(?:an?|the|her|his|their|its)\s+)?(?:emotion|personality|diagnosis|culture|inner state|intent|romance|dominance|ownership|age)\b",
            r"\b(?:weapon|gun|rifle|machine gun)\b[^.!?]{0,40}\b(?:is|are|was|were)\s+not\s+(?:allowed|safe|compliant|exempt)\b",
            r"\bnot\s+because\s+(?:it\s+is\s+)?(?:creative|creativity|stylized|stylization|style|small|low[- ]salience|narrative|fictional)\b",
        )
    )


def text_contains_term(text: str, term: str) -> bool:
    """Case-insensitive term coverage with ASCII token boundaries."""

    needle = str(term or "").strip()
    if not needle:
        return False
    if needle.isascii() and re.search(r"[A-Za-z0-9]", needle):
        pattern = r"(?<![A-Za-z0-9])" + re.escape(needle) + r"(?![A-Za-z0-9])"
        return re.search(pattern, text, flags=re.IGNORECASE) is not None
    return needle.casefold() in text.casefold()


def _literal_catalog_alias_matches(alias: str, phrase: str) -> bool:
    """Mirror the v3 catalog alias boundary without importing runtime trust."""

    normalized_alias = _normalized_literal_text(alias)
    normalized_phrase = _normalized_literal_text(phrase)
    if not normalized_alias or not normalized_phrase:
        return False
    if normalized_alias.isascii():
        alias_tokens = re.findall(r"[a-z0-9]+", normalized_alias)
        phrase_tokens = re.findall(r"[a-z0-9]+", normalized_phrase)
        return bool(alias_tokens) and any(
            phrase_tokens[index : index + len(alias_tokens)] == alias_tokens
            for index in range(len(phrase_tokens) - len(alias_tokens) + 1)
        )
    start = 0
    while True:
        index = normalized_phrase.find(normalized_alias, start)
        if index < 0:
            return False
        before = normalized_phrase[index - 1 : index]
        after_index = index + len(normalized_alias)
        after = normalized_phrase[after_index:]
        before_ok = not before or before.isspace() or not before.isalnum()
        after_ok = (
            not after
            or after[0].isspace()
            or not after[0].isalnum()
            or any(
                after.startswith(suffix)
                for suffix in UNIVERSAL_LITERAL_GRAMMATICAL_SUFFIXES
            )
        )
        if before_ok and after_ok:
            return True
        start = index + 1


def _universal_literal_alias_spans(alias: str, phrase: str) -> tuple[tuple[int, int], ...]:
    """Return every normalized boundary-valid alias span for effect replay."""

    normalized_alias = _normalized_literal_text(alias)
    normalized_phrase = _normalized_literal_text(phrase)
    if not normalized_alias or not normalized_phrase:
        return ()
    if normalized_alias.isascii():
        if re.search(r"[a-z0-9]", normalized_alias):
            pattern = re.compile(
                r"(?<![a-z0-9])" + re.escape(normalized_alias) + r"(?![a-z0-9])"
            )
            return tuple(
                (match.start(), match.end())
                for match in pattern.finditer(normalized_phrase)
            )
        return tuple(
            (match.start(), match.end())
            for match in re.finditer(re.escape(normalized_alias), normalized_phrase)
        )
    result: list[tuple[int, int]] = []
    start = 0
    while True:
        index = normalized_phrase.find(normalized_alias, start)
        if index < 0:
            break
        end = index + len(normalized_alias)
        before = normalized_phrase[index - 1 : index]
        after = normalized_phrase[end:]
        before_ok = not before or before.isspace() or not before.isalnum()
        after_ok = (
            not after
            or after[0].isspace()
            or not after[0].isalnum()
            or any(
                after.startswith(suffix)
                for suffix in UNIVERSAL_LITERAL_GRAMMATICAL_SUFFIXES
            )
        )
        if before_ok and after_ok:
            result.append((index, end))
        start = index + 1
    return tuple(result)


def _universal_normalized_substring_spans(
    value: str, phrase: str
) -> tuple[tuple[int, int], ...]:
    """Return authenticated normalized substring spans without catalog promotion."""

    normalized_value = _normalized_literal_text(value)
    normalized_phrase = _normalized_literal_text(phrase)
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


def _universal_literal_effect_polarities(
    phrase: str,
    aliases: Sequence[str],
    semantic_bindings: Mapping[str, Any],
    *,
    include_target_absence: bool = False,
    include_target_substitution: bool = False,
    allow_postposed_logical: bool = True,
    allow_korean_postposed_copular: bool = True,
    allow_authenticated_nonascii_substrings: bool = False,
    allow_reviewed_nonascii_marker_affixes: bool = False,
    postposed_logical_barrier_aliases: Sequence[str] = (),
) -> tuple[str, ...]:
    """Independently classify every contract-effect alias occurrence."""

    normalized = _normalized_literal_text(phrase)
    marker_fields = ["logical_values"]
    if include_target_absence:
        marker_fields.append("target_absence_values")
    polarity_contract = _mapping(semantic_bindings.get("literal_polarity_contract"))
    marker_records = polarity_contract.get("negative_markers")
    marker_specs: list[tuple[str, str | None]] = [
        (str(marker), None)
        for record in (marker_records if isinstance(marker_records, list) else [])
        if isinstance(record, dict)
        for field in marker_fields
        for marker in (_string_list(record.get(field)) or [])
    ]
    if include_target_substitution:
        marker_specs.extend(
            (
                str(marker.get("value")),
                str(marker.get("marker_position_relative_to_negated_target")),
            )
            for record in (marker_records if isinstance(marker_records, list) else [])
            if isinstance(record, dict)
            for marker in (
                record.get("target_substitution_values")
                if isinstance(record.get("target_substitution_values"), list)
                else []
            )
            if isinstance(marker, dict)
            and _is_nonempty_string(marker.get("value"))
            and marker.get("marker_position_relative_to_negated_target")
            in {"before", "after"}
        )
    directional_marker_spans = {
        span
        for marker, marker_position in marker_specs
        if marker_position is not None
        for span in _universal_normalized_substring_spans(marker, normalized)
    }
    separator_spans: list[tuple[int, int]] = []
    for separator in UNIVERSAL_LITERAL_CLAUSE_SEPARATORS:
        normalized_separator = _normalized_literal_text(separator)
        if not normalized_separator:
            continue
        separator_spans.extend(_universal_normalized_substring_spans(normalized_separator, normalized))
    separator_spans.sort()

    def local_bounds(start: int, end: int) -> tuple[int, int]:
        left = max(
            (boundary_end for _, boundary_end in separator_spans if boundary_end <= start),
            default=0,
        )
        right = min(
            (boundary_start for boundary_start, _ in separator_spans if boundary_start >= end),
            default=len(normalized),
        )
        return left, right

    results: list[tuple[int, str]] = []
    for alias in aliases:
        alias_spans = set(_universal_literal_alias_spans(str(alias), normalized))
        if allow_authenticated_nonascii_substrings and not str(alias).isascii():
            alias_spans.update(
                _universal_normalized_substring_spans(str(alias), normalized)
            )
        alias_spans.update(
            (start, end)
            for start, end in _universal_normalized_substring_spans(
                str(alias), normalized
            )
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
            clause_barrier_spans = {
                span
                for barrier_alias in postposed_logical_barrier_aliases
                for span in (
                    _universal_normalized_substring_spans(
                        str(barrier_alias), clause
                    )
                    if not str(barrier_alias).isascii()
                    else _universal_literal_alias_spans(str(barrier_alias), clause)
                )
            }
            negated = False
            for marker, marker_position in marker_specs:
                marker_spans = list(
                    _universal_normalized_substring_spans(marker, clause)
                    if marker_position is not None
                    else _universal_literal_alias_spans(marker, clause)
                )
                if (
                    marker_position is None
                    and allow_reviewed_nonascii_marker_affixes
                    and not marker.isascii()
                ):
                    marker_spans.extend(
                        _universal_normalized_substring_spans(marker, clause)
                    )
                if marker_position is None and allow_korean_postposed_copular and marker == "아니":
                    marker_spans.extend(
                        _universal_literal_alias_spans("아니라", clause)
                    )
                for marker_start, marker_end in sorted(set(marker_spans)):
                    if marker_position is None and any(
                        directional_start <= marker_start
                        and marker_end <= directional_end
                        for directional_start, directional_end in directional_marker_spans
                    ):
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
                        continue
                    if marker_position == "before" and marker_end > alias_start:
                        continue
                    if marker_position == "after" and marker_start < alias_end:
                        continue
                    if marker_position is None and marker == "않" and marker_end <= alias_start:
                        # Reviewed Korean ``않`` is a postposed auxiliary.  It
                        # can negate the nearest preceding anchor (펴지 않고)
                        # but cannot leak forward into later handle/rib nouns.
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
                            close = len(re.findall(r"[a-z0-9]+", between)) <= 2
                        elif marker_position is not None:
                            close = len(between.replace(" ", "")) <= 2
                        else:
                            close = len(between.replace(" ", "")) <= 8
                        if close:
                            negated = True
                            break
                if negated:
                    break
            results.append((start, "negated" if negated else "affirmative"))
    return tuple(polarity for _, polarity in sorted(set(results)))


def _universal_literal_effect_clauses(phrase: str) -> tuple[str, ...]:
    """Split a literal span at the closed cross-language clause boundary."""

    clauses = [_normalized_literal_text(phrase)]
    for separator in UNIVERSAL_LITERAL_CLAUSE_SEPARATORS:
        normalized_separator = _normalized_literal_text(separator)
        if not normalized_separator:
            continue
        next_clauses: list[str] = []
        for clause in clauses:
            spans = _universal_literal_alias_spans(normalized_separator, clause)
            if not spans:
                next_clauses.append(clause)
                continue
            cursor = 0
            for start, end in spans:
                fragment = clause[cursor:start].strip()
                if fragment:
                    next_clauses.append(fragment)
                cursor = end
            fragment = clause[cursor:].strip()
            if fragment:
                next_clauses.append(fragment)
        clauses = next_clauses
    return tuple(clause for clause in clauses if clause)


_UNIVERSAL_CONTRACT_EFFECT_HARD_CLAUSE_PATTERN = re.compile(
    r"[.!?;:。！？；：\r\n]+|\s*[\u2012-\u2015]\s*|"
    r"\b(?:but|however|yet|whereas|while|then|even\s+though|although)\b|"
    r"(?:하지만|그러나|반면|그런데|그\s*뒤|그\s*후|"
    r"しかし|ただし|一方|その後|"
    r"但是|然而|不过|但)"
)
_UNIVERSAL_CONTRACT_EFFECT_SOFT_COORDINATOR_PATTERN = re.compile(
    r"\band\b|(?:그리고|하고|そして|并且|然后)"
)
_UNIVERSAL_CONTRACT_EFFECT_EN_INDEPENDENT_SUBJECT_PATTERN = re.compile(
    r"^(?:a|an|the|this|that|these|those|another|it|he|she|they|we|i|you)\b"
)


def _universal_contract_effect_clause_has_global_negative(
    clause: str,
    semantic_bindings: Mapping[str, Any],
) -> bool:
    """Detect one reviewed directive without borrowing directional roots."""

    normalized = _normalized_literal_text(clause).replace("not only", "")
    polarity_contract = _mapping(
        semantic_bindings.get("literal_polarity_contract")
    )
    marker_records = polarity_contract.get("negative_markers")
    records = [
        record
        for record in (
            marker_records if isinstance(marker_records, list) else []
        )
        if isinstance(record, Mapping)
    ]
    directional_spans = {
        span
        for record in records
        for marker in (
            record.get("target_substitution_values")
            if isinstance(record.get("target_substitution_values"), list)
            else []
        )
        if isinstance(marker, Mapping)
        and _is_nonempty_string(marker.get("value"))
        for span in _universal_normalized_substring_spans(
            str(marker["value"]), normalized
        )
    }
    for record in records:
        for field in (
            "logical_values",
            "target_absence_values",
            "affirmative_conflict_values",
        ):
            for raw_marker in _string_list(record.get(field)) or []:
                spans = (
                    _universal_literal_alias_spans(raw_marker, normalized)
                    if raw_marker.isascii()
                    else _universal_normalized_substring_spans(
                        raw_marker, normalized
                    )
                )
                if any(
                    not any(
                        directional_start <= start
                        and end <= directional_end
                        for directional_start, directional_end in directional_spans
                    )
                    for start, end in spans
                ):
                    return True
    return False


def _universal_contract_effect_assertion_clauses(
    value: str,
    semantic_bindings: Mapping[str, Any],
) -> tuple[tuple[str, bool], ...]:
    """Split effect assertions and carry only same-subject negative lists."""

    raw = unicodedata.normalize("NFKC", str(value)).casefold()
    result: list[tuple[str, bool]] = []
    for hard_part in _UNIVERSAL_CONTRACT_EFFECT_HARD_CLAUSE_PATTERN.split(raw):
        if not hard_part.strip():
            continue
        soft_parts = _UNIVERSAL_CONTRACT_EFFECT_SOFT_COORDINATOR_PATTERN.split(
            hard_part
        )
        inherited_negative = False
        for part_index, raw_part in enumerate(soft_parts):
            clause = _normalized_literal_text(raw_part)
            if not clause:
                continue
            explicit_subject_reset = bool(
                part_index > 0
                and _UNIVERSAL_CONTRACT_EFFECT_EN_INDEPENDENT_SUBJECT_PATTERN.match(
                    clause
                )
            )
            force_negated = (
                part_index > 0
                and inherited_negative
                and not explicit_subject_reset
            )
            result.append((clause, force_negated))
            own_negative = _universal_contract_effect_clause_has_global_negative(
                clause, semantic_bindings
            )
            inherited_negative = own_negative or (
                force_negated and not explicit_subject_reset
            )
    return tuple(result)


def _universal_required_literal_matching_clauses(
    groups: Sequence[Sequence[str]],
    phrase: str,
    semantic_bindings: Mapping[str, Any],
) -> tuple[tuple[str, bool], ...]:
    """Require every reviewed AND-group inside the same literal span."""

    if not groups:
        return ()
    return tuple(
        (clause, inherited_negative)
        for clause, inherited_negative in _universal_contract_effect_assertion_clauses(
            phrase, semantic_bindings
        )
        if all(
            bool(_universal_contract_effect_surface_aliases(group, clause))
            for group in groups
        )
    )


def _universal_contract_effect_ascii_inflections(value: str) -> set[str]:
    """Return a closed regular-English surface set for one reviewed verb."""

    if re.fullmatch(r"[a-z]+", value) is None:
        return {value}
    result = {value}
    if value.endswith("e"):
        result.update({f"{value}s", f"{value}d", f"{value[:-1]}ing"})
    elif value.endswith("y") and len(value) > 1:
        result.update(
            {
                f"{value[:-1]}ies",
                f"{value[:-1]}ied",
                f"{value}ing",
            }
        )
    elif value.endswith(("s", "sh", "ch", "x", "z")):
        result.update({f"{value}es", f"{value}ed", f"{value}ing"})
    else:
        result.update({f"{value}s", f"{value}ed", f"{value}ing"})
    return result


def _universal_contract_effect_surface_aliases(
    alternatives: Sequence[str],
    clause: str,
) -> tuple[str, ...]:
    """Resolve reviewed effect lexemes to exact occurrence-local surfaces."""

    normalized_clause = _normalized_literal_text(clause)
    clause_tokens = re.findall(r"[a-z0-9]+", normalized_clause)
    surfaces: set[str] = set()
    for raw_alternative in alternatives:
        alternative = _normalized_literal_text(str(raw_alternative))
        if not alternative:
            continue
        if not alternative.isascii():
            if alternative in normalized_clause:
                surfaces.add(alternative)
            continue
        alternative_tokens = re.findall(r"[a-z0-9]+", alternative)
        if len(alternative_tokens) != 1 or not alternative_tokens[0].isalpha():
            if _literal_catalog_alias_matches(alternative, normalized_clause):
                surfaces.add(alternative)
            continue
        inflections = _universal_contract_effect_ascii_inflections(
            alternative_tokens[0]
        )
        surfaces.update(token for token in clause_tokens if token in inflections)
    return tuple(sorted(surfaces))


def _audit_contract_effect_projection_failures(
    scene: Mapping[str, Any],
    request_text: str,
    semantic_bindings: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Replay all data-owned contract-effect profiles without runtime helpers."""

    failures: list[dict[str, Any]] = []
    raw_profiles = semantic_bindings.get("contract_effect_profiles")
    if not isinstance(raw_profiles, list):
        return [issue("universal_asset_binding", "semantic bindings must expose the closed nine contract effect profiles")]
    profile_by_id: dict[str, Mapping[str, Any]] = {}
    effect_ids: set[str] = set()
    for index, raw_profile in enumerate(raw_profiles):
        failures.extend(
            _exact_object_keys(
                raw_profile,
                UNIVERSAL_CONTRACT_EFFECT_PROFILE_KEYS,
                check="universal_asset_binding",
                object_name=f"contract_effect_profiles[{index}]",
            )
        )
        if not isinstance(raw_profile, dict):
            continue
        profile_id = raw_profile.get("id")
        effect_id = raw_profile.get("effect_id")
        if (
            profile_id not in UNIVERSAL_CONTRACT_EFFECT_PROFILE_IDS
            or effect_id not in UNIVERSAL_EFFECT_IDS
            or profile_id != f"contract_effect_{effect_id}"
            or profile_id in profile_by_id
            or effect_id in effect_ids
        ):
            failures.append(issue("universal_asset_binding", "contract effect profile id/effect binding is unknown or duplicated", profile_id=profile_id, effect_id=effect_id))
            continue
        profile_by_id[str(profile_id)] = raw_profile
        effect_ids.add(str(effect_id))
        targets = raw_profile.get("source_targets")
        target_keys: list[tuple[str, str]] = []
        if not isinstance(targets, list) or not targets:
            failures.append(issue("universal_asset_binding", "contract effect source_targets must be nonempty", profile_id=profile_id))
            targets = []
        for target_index, raw_target in enumerate(targets):
            failures.extend(
                _exact_object_keys(
                    raw_target,
                    UNIVERSAL_CONTRACT_EFFECT_TARGET_KEYS,
                    check="universal_asset_binding",
                    object_name=f"contract effect target {profile_id}[{target_index}]",
                )
            )
            if not isinstance(raw_target, dict):
                continue
            source_kind = raw_target.get("source_kind")
            source_id = raw_target.get("source_id")
            if source_kind not in UNIVERSAL_CONTRACT_EFFECT_SOURCE_KINDS or not _is_nonempty_string(source_id):
                failures.append(issue("universal_asset_binding", "contract effect target is outside the closed source kinds", profile_id=profile_id, source_kind=source_kind, source_id=source_id))
            else:
                target_keys.append((str(source_kind), str(source_id)))
        if len(target_keys) != len(set(target_keys)):
            failures.append(issue("universal_asset_binding", "contract effect targets must be unique", profile_id=profile_id, actual=[list(item) for item in target_keys]))
        semantic_values = _unique_string_list(raw_profile.get("semantic_value_ids"))
        groups = raw_profile.get("required_literal_groups")
        if not semantic_values or not isinstance(groups, list) or not 1 <= len(groups) <= 3:
            failures.append(issue("universal_asset_binding", "contract effect semantic ids and one-to-three literal AND-groups are required", profile_id=profile_id))
        elif any(not _unique_string_list(group) for group in groups):
            failures.append(issue("universal_asset_binding", "every contract effect literal group must be a nonempty unique alternative list", profile_id=profile_id))
        aliases = raw_profile.get("literal_aliases")
        locales: set[str] = set()
        if isinstance(aliases, list):
            for record in aliases:
                if isinstance(record, dict) and _is_nonempty_string(record.get("locale")) and _unique_string_list(record.get("values")):
                    locales.add(str(record["locale"]))
        if locales != {"ko", "en", "ja", "zh"}:
            failures.append(issue("universal_asset_binding", "contract effect literal aliases must cover ko/en/ja/zh", profile_id=profile_id, actual=sorted(locales)))
        if raw_profile.get("polarity") != "affirmative" or raw_profile.get("subject_binding") not in UNIVERSAL_CONTRACT_EFFECT_SUBJECT_BINDINGS:
            failures.append(issue("universal_asset_binding", "contract effect polarity/subject binding is outside the closed contract", profile_id=profile_id))
    if set(profile_by_id) != UNIVERSAL_CONTRACT_EFFECT_PROFILE_IDS or effect_ids != UNIVERSAL_EFFECT_IDS:
        failures.append(issue("universal_asset_binding", "contract effect profiles must exactly cover all nine blocked semantics", expected=sorted(UNIVERSAL_CONTRACT_EFFECT_PROFILE_IDS), actual=sorted(profile_by_id)))
    if failures:
        return failures

    contract = _mapping(scene.get("scene_contract"))
    identity = _mapping(contract.get("identity_core"))
    entities_value = identity.get("entities")
    entities = [
        entity
        for entity in (entities_value if isinstance(entities_value, list) else [])
        if isinstance(entity, dict)
    ]
    entity_ids = {
        str(entity.get("entity_id"))
        for entity in entities
        if _is_nonempty_string(entity.get("entity_id"))
    }
    role_records_value = contract.get("event_roles")
    role_records = [
        role
        for role in (
            role_records_value if isinstance(role_records_value, list) else []
        )
        if isinstance(role, dict)
    ]
    role_by_id = {
        str(role.get("role_id")): role
        for role in role_records
        if _is_nonempty_string(role.get("role_id"))
    }
    actor_value = _mapping(role_by_id.get("actor")).get("value_id")
    actor_participant_primary = _audit_participant_primary(scene, "actor")
    actor_entity_id = (
        str(actor_participant_primary)
        if _is_nonempty_string(actor_participant_primary)
        else (
            str(actor_value)
            if _is_nonempty_string(actor_value) and str(actor_value) in entity_ids
            else "actor"
        )
    )
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
    for entity in entities:
        entity_id = str(entity.get("entity_id"))
        for fact in (
            entity.get("feature_facts")
            if isinstance(entity.get("feature_facts"), list)
            else []
        ):
            if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                occurrences.append(
                    {
                        "source_kind": "identity_fact",
                        "source_id": "feature_fact",
                        "instance_kind": "identity_fact",
                        "instance_id": f"feature_fact::{entity_id}::{fact['id']}",
                        "phrases": list(_string_list(fact.get("request_phrases")) or []),
                        "semantic_value_ids": [str(fact["id"])],
                        "source_entity_id": entity_id,
                        "assertion": "positive",
                    }
                )
    for list_name, source_id, assertion in (
        ("scene_facts", "scene_fact", "positive"),
        ("forbidden_facts", "forbidden_fact", "forbidden"),
    ):
        for fact in (
            identity.get(list_name)
            if isinstance(identity.get(list_name), list)
            else []
        ):
            if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                occurrences.append(
                    {
                        "source_kind": "identity_fact",
                        "source_id": source_id,
                        "instance_kind": "identity_fact",
                        "instance_id": f"{source_id}::{fact['id']}",
                        "phrases": list(_string_list(fact.get("request_phrases")) or []),
                        "semantic_value_ids": [str(fact["id"])],
                        "source_entity_id": actor_entity_id,
                        "assertion": assertion,
                    }
                )
    for slot in (
        contract.get("slot_states")
        if isinstance(contract.get("slot_states"), list)
        else []
    ):
        if isinstance(slot, dict) and _is_nonempty_string(slot.get("slot_id")):
            occurrences.append(
                {
                    "source_kind": "slot",
                    "source_id": str(slot["slot_id"]),
                    "instance_kind": "slot_state",
                    "instance_id": f"slot_state::{slot['slot_id']}",
                    "phrases": list(_string_list(slot.get("request_phrases")) or []),
                    "semantic_value_ids": list(_string_list(slot.get("value_ids")) or []),
                    "source_entity_id": actor_entity_id,
                    "assertion": "negative" if slot.get("state") == "closed" else "positive",
                }
            )
    for role in role_records:
        role_id = str(role.get("role_id"))
        value_id = role.get("value_id")
        occurrences.append(
            {
                "source_kind": "event_role",
                "source_id": role_id,
                "instance_kind": "event_role",
                "instance_id": f"event_role::{role_id}",
                "phrases": list(_string_list(role.get("request_phrases")) or []),
                "semantic_value_ids": [str(value_id)] if _is_nonempty_string(value_id) else [],
                "source_entity_id": actor_entity_id,
                "assertion": "negative" if role.get("state") == "closed" else "positive",
            }
        )
    context = _mapping(contract.get("context_profile"))
    for field in ("theme_tags", "era_technology", "tone", "violence", "social", "scale"):
        raw_value = context.get(field)
        semantic_values = (
            [str(value) for value in raw_value]
            if isinstance(raw_value, list)
            else ([str(raw_value)] if raw_value is not None else [])
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

    def profile_aliases(profile: Mapping[str, Any]) -> list[str]:
        return [
            str(value)
            for record in profile.get("literal_aliases", [])
            if isinstance(record, dict)
            for value in (_string_list(record.get("values")) or [])
        ]

    def effect_subject(profile: Mapping[str, Any], occurrence: Mapping[str, Any]) -> str | None:
        binding = str(profile.get("subject_binding"))
        if binding == "scene":
            return None
        if binding == "source_entity":
            return str(occurrence.get("source_entity_id"))
        if binding in {"target", "recipient"}:
            participant_primary = _audit_participant_primary(scene, binding)
            if _is_nonempty_string(participant_primary):
                return str(participant_primary)
            role_value = _mapping(role_by_id.get(binding)).get("value_id")
            return str(role_value) if _is_nonempty_string(role_value) and str(role_value) in entity_ids else binding
        return actor_entity_id

    expected_effect_occurrences: set[tuple[str, str, str, str, str]] = set()
    for occurrence in occurrences:
        if occurrence["assertion"] == "forbidden":
            continue
        target_key = (str(occurrence["source_kind"]), str(occurrence["source_id"]))
        for profile_id, profile in profile_by_id.items():
            targets = {
                (str(target.get("source_kind")), str(target.get("source_id")))
                for target in profile.get("source_targets", [])
                if isinstance(target, dict)
            }
            if target_key not in targets:
                continue
            aliases = profile_aliases(profile)
            alias_polarities: set[str] = set()
            for phrase in occurrence["phrases"]:
                for clause, inherited_negative in (
                    _universal_contract_effect_assertion_clauses(
                        str(phrase), semantic_bindings
                    )
                ):
                    surfaces = _universal_contract_effect_surface_aliases(
                        aliases, clause
                    )
                    if not surfaces:
                        continue
                    polarities = set(
                        _universal_literal_effect_polarities(
                            clause,
                            surfaces,
                            semantic_bindings,
                            include_target_absence=True,
                            include_target_substitution=True,
                            allow_korean_postposed_copular=True,
                            allow_authenticated_nonascii_substrings=True,
                            allow_reviewed_nonascii_marker_affixes=True,
                        )
                    )
                    if (
                        inherited_negative
                        or _universal_contract_effect_clause_has_global_negative(
                            clause, semantic_bindings
                        )
                    ):
                        alias_polarities.add("negated")
                    else:
                        alias_polarities.update(polarities)
            literal_match = "affirmative" in alias_polarities
            groups = profile.get("required_literal_groups", [])
            compositional_polarities: set[str] = set()
            for phrase in occurrence["phrases"]:
                for clause, inherited_negative in (
                    _universal_required_literal_matching_clauses(
                        groups, str(phrase), semantic_bindings
                    )
                ):
                    clause_polarities = set(
                        _universal_literal_effect_polarities(
                            clause,
                            _universal_contract_effect_surface_aliases(
                                [str(value) for value in groups[-1]],
                                clause,
                            ),
                            semantic_bindings,
                            include_target_absence=True,
                            include_target_substitution=True,
                            allow_korean_postposed_copular=True,
                            allow_authenticated_nonascii_substrings=True,
                            allow_reviewed_nonascii_marker_affixes=True,
                        )
                    )
                    # Multiple reviewed alternatives can describe one local
                    # predicate ("not use as a navigation instrument").  A
                    # directly negated verb scopes that complete matched
                    # group; a later affirmative occurrence lives in its own
                    # clause and is still accumulated independently.
                    if inherited_negative or "negated" in clause_polarities:
                        compositional_polarities.add("negated")
                    elif "affirmative" in clause_polarities:
                        compositional_polarities.add("affirmative")
            compositional_match = "affirmative" in compositional_polarities
            semantic_match = bool(
                set(str(value) for value in occurrence["semantic_value_ids"])
                & set(_string_list(profile.get("semantic_value_ids")) or [])
            )
            if not literal_match and not compositional_match and not (
                semantic_match
                and "negated" not in alias_polarities
                and "negated" not in compositional_polarities
            ):
                continue
            subject = effect_subject(profile, occurrence)
            expected_effect_occurrences.add(
                (
                    str(occurrence["instance_kind"]),
                    str(occurrence["instance_id"]),
                    profile_id,
                    str(profile["effect_id"]),
                    "" if subject is None else str(subject),
                )
            )

    snapshot = _mapping(scene.get("hard_gate_snapshot"))
    actual_effect_occurrences: set[tuple[str, str, str, str, str]] = set()
    registry_effect_occurrences: list[dict[str, Any]] = []
    for item in (
        snapshot.get("selected_source_refs")
        if isinstance(snapshot.get("selected_source_refs"), list)
        else []
    ):
        if not isinstance(item, dict):
            continue
        for occurrence in (
            item.get("effect_occurrences")
            if isinstance(item.get("effect_occurrences"), list)
            else []
        ):
            if not isinstance(occurrence, dict):
                continue
            if occurrence.get("source_profile_id") == "semantic_effect_registry":
                registry_effect_occurrences.append(dict(occurrence))
                continue
            actual_effect_occurrences.add(
                (
                    str(item.get("instance_kind")),
                    str(item.get("instance_id")),
                    str(occurrence.get("source_profile_id")),
                    str(occurrence.get("effect_id")),
                    "" if occurrence.get("subject_ref") is None else str(occurrence.get("subject_ref")),
                )
            )
    if registry_effect_occurrences:
        failures.append(
            issue(
                "universal_hard_gate",
                "the frozen independently reviewed 126-source registry cannot inject blocked semantic effects",
                actual=registry_effect_occurrences,
            )
        )
    if actual_effect_occurrences != expected_effect_occurrences:
        failures.append(
            issue(
                "universal_hard_gate",
                "contract effect projection must exactly replay all data-owned multilingual semantic profiles",
                missing=[list(item) for item in sorted(expected_effect_occurrences - actual_effect_occurrences)],
                unexpected=[list(item) for item in sorted(actual_effect_occurrences - expected_effect_occurrences)],
            )
        )
    if expected_effect_occurrences:
        failures.append(
            issue(
                "universal_hard_gate",
                "blocked contract semantics cannot survive into a valid candidate pack",
                effects=sorted({item[3] for item in expected_effect_occurrences}),
                occurrences=[list(item) for item in sorted(expected_effect_occurrences)],
            )
        )
    return failures


def _audit_context_literal_profile_failures(
    scene: Mapping[str, Any],
    request_text: str,
    semantic_bindings: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Authenticate every executable non-default context value independently."""

    failures: list[dict[str, Any]] = []
    raw_profiles = semantic_bindings.get("context_literal_profiles")
    if not isinstance(raw_profiles, list):
        return [issue("universal_asset_binding", "semantic bindings must expose reviewed context literal profiles")]
    profile_by_key: dict[tuple[str, str], Mapping[str, Any]] = {}
    profile_ids: set[str] = set()
    for index, raw_profile in enumerate(raw_profiles):
        failures.extend(
            _exact_object_keys(
                raw_profile,
                UNIVERSAL_CONTEXT_LITERAL_PROFILE_KEYS,
                check="universal_asset_binding",
                object_name=f"context_literal_profiles[{index}]",
            )
        )
        if not isinstance(raw_profile, dict):
            continue
        profile_id = raw_profile.get("id")
        field = raw_profile.get("field")
        value = raw_profile.get("value")
        key = (str(field), str(value))
        groups = raw_profile.get("required_literal_groups")
        if (
            not _is_nonempty_string(profile_id)
            or profile_id in profile_ids
            or key not in UNIVERSAL_CONTEXT_LITERAL_KEYS
            or key in profile_by_key
            or not isinstance(groups, list)
            or not 1 <= len(groups) <= 3
            or any(not _unique_string_list(group) for group in groups)
            or raw_profile.get("polarity") not in {"affirmative", "negated"}
        ):
            failures.append(
                issue(
                    "universal_asset_binding",
                    "context literal profile is malformed, duplicated, or outside the closed executable values",
                    profile_id=profile_id,
                    field=field,
                    value=value,
                )
            )
            continue
        profile_ids.add(str(profile_id))
        profile_by_key[key] = raw_profile
    if set(profile_by_key) != UNIVERSAL_CONTEXT_LITERAL_KEYS:
        failures.append(
            issue(
                "universal_asset_binding",
                "context literal profiles must exactly cover the seven executable non-default context values",
                expected=[list(item) for item in sorted(UNIVERSAL_CONTEXT_LITERAL_KEYS)],
                actual=[list(item) for item in sorted(profile_by_key)],
            )
        )
    if failures:
        return failures

    def profile_matches(profile: Mapping[str, Any]) -> bool:
        expected_polarity = str(profile["polarity"])
        groups = profile["required_literal_groups"]
        normalized = _normalized_literal_text(request_text)
        # Commas and list conjunctions deliberately remain inside the scope so
        # one reviewed terminal directive can govern a literal list.  Sentence
        # and contrast boundaries cannot lend that directive to another claim.
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
        if expected_polarity == "affirmative":
            target_spans = sorted(
                {
                    span
                    for group in groups
                    for alternative in group
                    for span in _universal_literal_alias_spans(
                        str(alternative), normalized
                    )
                }
            )
            polarity_contract = _mapping(
                semantic_bindings.get("literal_polarity_contract")
            )
            marker_records = polarity_contract.get("negative_markers")
            directive_spans = sorted(
                {
                    span
                    for record in (
                        marker_records if isinstance(marker_records, list) else []
                    )
                    if isinstance(record, dict)
                    for alternative in (
                        _string_list(record.get("affirmative_conflict_values")) or []
                    )
                    for span in _universal_literal_alias_spans(
                        str(alternative), normalized
                    )
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
                        len(re.findall(r"[a-z0-9]+", between)) <= 16
                        if normalized[target_start:target_end].isascii()
                        else len(between.replace(" ", "")) <= 64
                    )
                    if not close_enough:
                        continue
                    if _universal_literal_effect_polarities(
                        between,
                        intervening_affirmative_terms,
                        semantic_bindings,
                        allow_postposed_logical=False,
                        allow_korean_postposed_copular=False,
                    ):
                        continue
                    return False
            for clause in _universal_literal_effect_clauses(request_text):
                if all(
                    (
                        polarities := _universal_literal_effect_polarities(
                            clause,
                            [str(alternative) for alternative in group],
                            semantic_bindings,
                            allow_postposed_logical=False,
                            allow_korean_postposed_copular=False,
                        )
                    )
                    and set(polarities) == {"affirmative"}
                    for group in groups
                ):
                    return True
            return False

        if len(groups) != 2:
            return False
        target_spans = sorted(
            {
                span
                for alternative in groups[0]
                for span in _universal_literal_alias_spans(str(alternative), normalized)
            }
        )
        directive_spans = sorted(
            {
                span
                for alternative in groups[1]
                for span in _universal_literal_alias_spans(str(alternative), normalized)
            }
        )
        if not target_spans or not directive_spans:
            return False

        affirmative_conflict_terms = (
            "include", "add", "show", "depict", "visible", "present",
            "넣어", "추가", "보여", "사용해", "사용한다",
            "追加", "表示", "描く", "包含", "添加", "展示",
        )
        absence_terms = (
            "omit", "remove", "exclude", "erase",
            "빼", "제외", "생략", "지워",
            "省く", "除外", "削除", "省略", "排除", "删除",
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
                    len(re.findall(
                        r"[a-z0-9]+",
                        normalized[min(target_end, end):max(target_start, start)],
                    )) <= 16
                    if normalized[target_start:target_end].isascii()
                    else len(
                        normalized[min(target_end, end):max(target_start, start)].replace(" ", "")
                    ) <= 64
                )
                for start, end in local_directives
            ):
                return False
            local_clause = normalized[left:right]
            conflict_polarities = _universal_literal_effect_polarities(
                local_clause,
                affirmative_conflict_terms,
                semantic_bindings,
            )
            if "affirmative" in conflict_polarities:
                return False
            absence_polarities = _universal_literal_effect_polarities(
                local_clause,
                absence_terms,
                semantic_bindings,
            )
            if "negated" in absence_polarities:
                return False
        return True

    context = _mapping(_mapping(scene.get("scene_contract")).get("context_profile"))
    for (field, value), profile in sorted(profile_by_key.items()):
        if str(context.get(field)) != value:
            continue
        if not profile_matches(profile):
            failures.append(
                issue(
                    "universal_scene_contract",
                    "executable context value lacks a contradiction-free reviewed literal assertion",
                    profile_id=profile.get("id"),
                    field=field,
                    value=value,
                    expected_polarity=profile.get("polarity"),
                )
            )
    return failures


def selected_runtime_nodes(pack: Mapping[str, Any]) -> list[dict[str, Any]]:
    grammar = _mapping(pack.get("visual_grammar"))
    return [node for node in grammar.get("runtime_nodes") or [] if isinstance(node, dict)]


def expected_chosen_candidate_ids(pack: Mapping[str, Any]) -> list[str]:
    """Compute the exact trace IDs exposed by a valid compact pack."""

    request = _mapping(pack.get("request_contract"))
    profile = _mapping(pack.get("format_profile"))
    route_id = str(request.get("route_id") or "")
    variant_id = str(profile.get("variant_id") or "")
    ids = [f"route:{route_id}", f"format:{variant_id}"]
    ids.extend(f"visual:{node.get('id')}" for node in selected_runtime_nodes(pack) if node.get("id"))
    if pack.get("contract_version") == CONTRACT_VERSION_V3:
        scene = _mapping(pack.get("universal_scene"))
        atoms = scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
        bridges = scene.get("bridges") if isinstance(scene.get("bridges"), list) else []
        ids.extend(
            f"universal:{atom.get('instance_id')}"
            for atom in atoms
            if isinstance(atom, dict) and _is_nonempty_string(atom.get("instance_id"))
        )
        ids.extend(
            f"universal:{bridge.get('bridge_id')}"
            for bridge in bridges
            if isinstance(bridge, dict) and _is_nonempty_string(bridge.get("bridge_id"))
        )
    return ids


def _profile_required_evidence_fields(profile: Mapping[str, Any]) -> list[str]:
    # Format assets also declare lifecycle evidence types such as
    # ``rendered_pixel_review``.  Those are qualification requirements, not
    # phrases that a pre-render prompt may truthfully claim.  Only the typed
    # composition-field list crosses into composed-prompt auditing.
    return _string_list(profile.get("required_format_evidence_fields")) or []


def _second_look_pack_contract_failures(
    pack: Mapping[str, Any],
    profile: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Validate the exact v2 pre-render second-look planning contract."""

    version = pack.get("contract_version")
    if version not in (CONTRACT_VERSION_V2, CONTRACT_VERSION_V3):
        return []

    errors: list[dict[str, Any]] = []
    composition = pack.get("composition_contract")
    if not isinstance(composition, dict):
        errors.append(issue("composition_contract", "composition_contract must be an object"))
    expected_schema = COMPOSED_PROMPT_SCHEMA_V3 if version == CONTRACT_VERSION_V3 else COMPOSED_PROMPT_SCHEMA_V2
    if isinstance(composition, dict) and composition.get("composed_schema") != expected_schema:
        errors.append(
            issue(
                "second_look_pack_contract",
                "composition_contract.composed_schema must select the version-bound composed-prompt schema",
                expected=expected_schema,
                actual=composition.get("composed_schema"),
            )
        )

    viewer = pack.get("viewer_contract")
    if not isinstance(viewer, dict):
        errors.append(issue("viewer_contract", "viewer_contract must be an object"))
        return errors
    plan_contract = viewer.get("second_look_plan_contract")
    errors.extend(
        _exact_object_keys(
            plan_contract,
            SECOND_LOOK_PLAN_CONTRACT_KEYS,
            check="second_look_pack_contract",
            object_name="viewer_contract.second_look_plan_contract",
        )
    )
    if not isinstance(plan_contract, dict):
        return errors

    expected_values: tuple[tuple[str, Any], ...] = (
        ("schema", SECOND_LOOK_PLAN_SCHEMA),
        ("required", True),
        ("required_roles", list(SECOND_LOOK_ROLES)),
        ("carrier_kinds", list(SECOND_LOOK_CARRIER_KINDS)),
        ("risk_flags", list(SECOND_LOOK_RISK_FLAGS)),
        ("forbidden_as_sole", list(SECOND_LOOK_RISK_FLAGS)),
        ("fallback_must_reference_selected_consequence", True),
    )
    for field, expected in expected_values:
        actual = plan_contract.get(field)
        # Identity is intentional for the boolean fields: integers must not
        # masquerade as JSON booleans.
        matches = actual is expected if isinstance(expected, bool) else actual == expected
        if not matches:
            errors.append(
                issue(
                    "second_look_pack_contract",
                    "second-look contract field does not match the closed v2 contract",
                    field=field,
                    expected=expected,
                    actual=actual,
                )
            )

    scale_contract = profile.get("scale_contract")
    expected_scales = (
        _string_list(scale_contract.get("inspection_scales"))
        if isinstance(scale_contract, dict)
        else None
    )
    if not expected_scales or len(expected_scales) != len(set(expected_scales)):
        errors.append(
            issue(
                "second_look_pack_contract",
                "format_profile.scale_contract.inspection_scales must be a nonempty unique string list",
                actual=scale_contract.get("inspection_scales") if isinstance(scale_contract, dict) else None,
            )
        )
    if plan_contract.get("allowed_review_scale_ids") != expected_scales:
        errors.append(
            issue(
                "second_look_pack_contract",
                "allowed_review_scale_ids must exactly copy the selected format inspection scales",
                expected=expected_scales,
                actual=plan_contract.get("allowed_review_scale_ids"),
            )
        )
    return errors


def _universal_hard_gate_failures(
    pack: Mapping[str, Any],
    scene: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Validate the authenticated all-guard semantic hard-gate snapshot."""

    failures: list[dict[str, Any]] = []
    snapshot_value = scene.get("hard_gate_snapshot")
    failures.extend(
        _exact_object_keys(
            snapshot_value,
            UNIVERSAL_HARD_GATE_KEYS,
            check="universal_hard_gate",
            object_name="universal_scene.hard_gate_snapshot",
        )
    )
    if not isinstance(snapshot_value, dict):
        return failures
    snapshot = snapshot_value
    if snapshot.get("schema") != UNIVERSAL_HARD_GATE_SCHEMA:
        failures.append(
            issue(
                "universal_hard_gate",
                "hard-gate snapshot schema is outside the closed v1 contract",
                expected=UNIVERSAL_HARD_GATE_SCHEMA,
                actual=snapshot.get("schema"),
            )
        )

    snapshot_asset_hashes = snapshot.get("asset_hashes")
    failures.extend(
        _exact_object_keys(
            snapshot_asset_hashes,
            UNIVERSAL_HARD_GATE_ASSET_HASH_KEYS,
            check="universal_hard_gate",
            object_name="hard_gate_snapshot.asset_hashes",
        )
    )
    pack_asset_hashes = _mapping(pack.get("asset_hashes"))
    if isinstance(snapshot_asset_hashes, dict):
        expected_snapshot_hashes = {
            key: pack_asset_hashes.get(key)
            for key in UNIVERSAL_HARD_GATE_ASSET_HASH_KEYS
        }
        if snapshot_asset_hashes != expected_snapshot_hashes:
            failures.append(
                issue(
                    "universal_hard_gate",
                    "hard-gate asset hashes must exactly copy the raw-byte-bound universal pack hashes",
                    expected=expected_snapshot_hashes,
                    actual=snapshot_asset_hashes,
                )
            )
        for field, value in snapshot_asset_hashes.items():
            if not _hex64(value):
                failures.append(
                    issue(
                        "universal_hard_gate",
                        "hard-gate asset hash is malformed",
                        field=field,
                        actual=value,
                    )
                )
    if not _hex64(snapshot.get("semantic_effect_registry_sha256")):
        failures.append(
            issue(
                "universal_hard_gate",
                "semantic effect registry digest must be 64 lowercase hexadecimal characters",
                actual=snapshot.get("semantic_effect_registry_sha256"),
            )
        )

    source_coverage = snapshot.get("source_coverage")
    if not isinstance(source_coverage, dict) or source_coverage != UNIVERSAL_EFFECT_SOURCE_COUNTS:
        failures.append(
            issue(
                "universal_hard_gate",
                "semantic effect source coverage must exactly cover the frozen 126-source registry",
                expected=UNIVERSAL_EFFECT_SOURCE_COUNTS,
                actual=source_coverage,
            )
        )

    identity = _mapping(scene.get("identity_core"))
    entity_ids = {
        str(entity.get("entity_id"))
        for entity in (
            identity.get("entities")
            if isinstance(identity.get("entities"), list)
            else []
        )
        if isinstance(entity, dict) and _is_nonempty_string(entity.get("entity_id"))
    }
    known_subject_refs = entity_ids | set(UNIVERSAL_ROLE_IDS)
    source_kind_order = {
        source_kind: index
        for index, source_kind in enumerate(
            ("visual_candidate", "proposal_profile", "context_profile", "bridge_type", "resource_kind")
        )
    }
    selected_value = snapshot.get("selected_source_refs")
    if not isinstance(selected_value, list) or not selected_value:
        failures.append(
            issue(
                "universal_hard_gate",
                "selected_source_refs must be a nonempty typed source projection",
                actual=selected_value,
            )
        )
        selected_value = []
    selected_keys: list[tuple[str, str]] = []
    selected_by_kind: dict[str, set[str]] = {}
    selected_item_by_key: dict[tuple[str, str], Mapping[str, Any]] = {}
    observed_from_records: set[str] = set()
    calculated_load_max = {axis: 0 for axis in UNIVERSAL_LOAD_AXES}
    for index, raw_item in enumerate(selected_value):
        failures.extend(
            _exact_object_keys(
                raw_item,
                UNIVERSAL_SELECTED_SOURCE_KEYS,
                check="universal_hard_gate",
                object_name=f"hard_gate_snapshot.selected_source_refs[{index}]",
            )
        )
        if not isinstance(raw_item, dict):
            continue
        instance_kind = raw_item.get("instance_kind")
        instance_id = raw_item.get("instance_id")
        if instance_kind not in UNIVERSAL_SELECTED_INSTANCE_KINDS or not _is_nonempty_string(instance_id):
            failures.append(
                issue(
                    "universal_hard_gate",
                    "selected source instance kind/id is outside the closed contract",
                    index=index,
                    instance_kind=instance_kind,
                    instance_id=instance_id,
                )
            )
            continue
        key = (str(instance_kind), str(instance_id))
        selected_keys.append(key)
        selected_by_kind.setdefault(str(instance_kind), set()).add(str(instance_id))
        selected_item_by_key.setdefault(key, raw_item)

        refs_value = raw_item.get("source_profile_refs")
        refs: list[dict[str, str]] = []
        if not isinstance(refs_value, list):
            failures.append(issue("universal_hard_gate", "source_profile_refs must be a list", instance_key=list(key)))
            refs_value = []
        ref_keys: list[tuple[str, str]] = []
        for ref_index, raw_ref in enumerate(refs_value):
            failures.extend(
                _exact_object_keys(
                    raw_ref,
                    UNIVERSAL_SOURCE_REF_KEYS,
                    check="universal_hard_gate",
                    object_name=f"selected source ref {key}[{ref_index}]",
                )
            )
            if not isinstance(raw_ref, dict):
                continue
            source_kind = raw_ref.get("source_kind")
            source_id = raw_ref.get("source_id")
            if source_kind not in UNIVERSAL_EFFECT_SOURCE_KINDS or not _is_nonempty_string(source_id):
                failures.append(
                    issue(
                        "universal_hard_gate",
                        "source profile reference is outside the closed registry kinds",
                        instance_key=list(key),
                        source_kind=source_kind,
                        source_id=source_id,
                    )
                )
                continue
            ref_keys.append((str(source_kind), str(source_id)))
            refs.append({"source_kind": str(source_kind), "source_id": str(source_id)})
        expected_ref_keys = sorted(
            set(ref_keys),
            key=lambda value: (source_kind_order[value[0]], value[1]),
        )
        if ref_keys != expected_ref_keys:
            failures.append(
                issue(
                    "universal_hard_gate",
                    "source profile references must be unique and canonically ordered",
                    instance_key=list(key),
                    expected=[list(item) for item in expected_ref_keys],
                    actual=[list(item) for item in ref_keys],
                )
            )

        contract_profile_ids = _unique_string_list(raw_item.get("contract_effect_profile_ids"))
        if (
            contract_profile_ids is None
            or contract_profile_ids != sorted(contract_profile_ids)
            or not set(contract_profile_ids).issubset(UNIVERSAL_CONTRACT_EFFECT_PROFILE_IDS)
        ):
            failures.append(
                issue(
                    "universal_hard_gate",
                    "contract effect profile ids must be a sorted unique subset of the closed nine",
                    instance_key=list(key),
                    actual=raw_item.get("contract_effect_profile_ids"),
                )
            )
            contract_profile_ids = []

        occurrences_value = raw_item.get("effect_occurrences")
        if not isinstance(occurrences_value, list):
            failures.append(issue("universal_hard_gate", "effect_occurrences must be a list", instance_key=list(key)))
            occurrences_value = []
        occurrence_keys: list[tuple[str, str, str]] = []
        occurrence_contract_profiles: set[str] = set()
        for occurrence_index, raw_occurrence in enumerate(occurrences_value):
            failures.extend(
                _exact_object_keys(
                    raw_occurrence,
                    UNIVERSAL_EFFECT_OCCURRENCE_KEYS,
                    check="universal_hard_gate",
                    object_name=f"selected effect occurrence {key}[{occurrence_index}]",
                )
            )
            if not isinstance(raw_occurrence, dict):
                continue
            effect_id = raw_occurrence.get("effect_id")
            source_profile_id = raw_occurrence.get("source_profile_id")
            subject_ref = raw_occurrence.get("subject_ref")
            if effect_id not in UNIVERSAL_EFFECT_IDS:
                failures.append(issue("universal_hard_gate", "effect occurrence id is outside the closed nine", instance_key=list(key), effect_id=effect_id))
                continue
            if subject_ref is not None and (
                not _is_nonempty_string(subject_ref) or str(subject_ref) not in known_subject_refs
            ):
                failures.append(
                    issue(
                        "universal_hard_gate",
                        "effect occurrence subject must bind a known identity entity or event role, with null reserved for scene scope",
                        instance_key=list(key),
                        subject_ref=subject_ref,
                    )
                )
            if source_profile_id == "semantic_effect_registry":
                if not refs:
                    failures.append(issue("universal_hard_gate", "registry effect occurrence requires a selected registry source", instance_key=list(key), effect_id=effect_id))
            elif source_profile_id in UNIVERSAL_CONTRACT_EFFECT_PROFILE_IDS:
                occurrence_contract_profiles.add(str(source_profile_id))
                if source_profile_id not in contract_profile_ids or source_profile_id != f"contract_effect_{effect_id}":
                    failures.append(
                        issue(
                            "universal_hard_gate",
                            "contract effect occurrence must bind its exact declared profile and effect",
                            instance_key=list(key),
                            source_profile_id=source_profile_id,
                            effect_id=effect_id,
                        )
                    )
            else:
                failures.append(issue("universal_hard_gate", "effect occurrence source profile is unknown", instance_key=list(key), source_profile_id=source_profile_id))
            observed_from_records.add(str(effect_id))
            occurrence_keys.append((str(effect_id), str(source_profile_id), "" if subject_ref is None else str(subject_ref)))
        if occurrence_keys != sorted(set(occurrence_keys)):
            failures.append(
                issue(
                    "universal_hard_gate",
                    "effect occurrences must be unique and canonically ordered",
                    instance_key=list(key),
                    actual=[list(item) for item in occurrence_keys],
                )
            )
        if occurrence_contract_profiles != set(contract_profile_ids):
            failures.append(
                issue(
                    "universal_hard_gate",
                    "contract effect profile ids must exactly equal occurrence provenance",
                    instance_key=list(key),
                    expected=sorted(occurrence_contract_profiles),
                    actual=contract_profile_ids,
                )
            )

        scope = raw_item.get("scope")
        is_effect_projection = (
            instance_kind in {"identity_fact", "slot_state", "context_value"}
            or (instance_kind == "event_role" and str(instance_id).startswith("event_role::"))
        )
        if is_effect_projection:
            if scope != "contract_projection" or refs or not contract_profile_ids or not occurrences_value:
                failures.append(issue("universal_hard_gate", "contract effect projection must have only data-owned effect profiles and occurrences", instance_key=list(key)))
        elif instance_kind == "fixed_prop":
            if scope != "contract_projection" or not refs or contract_profile_ids:
                failures.append(issue("universal_hard_gate", "fixed prop projection must cite one reviewed visual source without contract effects", instance_key=list(key)))
        elif instance_kind == "event_role":
            if scope not in {"contract_projection", "runtime_addition"}:
                failures.append(issue("universal_hard_gate", "event-role source scope is outside the closed enum", instance_key=list(key), actual=scope))
            if scope == "contract_projection" and refs:
                failures.append(issue("universal_hard_gate", "contract-projected event role cannot invent a runtime source", instance_key=list(key)))
            if scope == "runtime_addition" and not refs:
                failures.append(issue("universal_hard_gate", "runtime-selected event role requires a registry source", instance_key=list(key)))
            if contract_profile_ids:
                failures.append(issue("universal_hard_gate", "selected event role record cannot duplicate contract-effect projection provenance", instance_key=list(key)))
        elif scope != "runtime_addition" or not refs or contract_profile_ids:
            failures.append(issue("universal_hard_gate", "runtime-added source must cite registry profiles and cannot claim contract-effect provenance", instance_key=list(key), scope=scope))

        load_vector = raw_item.get("load_vector")
        if not isinstance(load_vector, dict) or set(load_vector) != set(UNIVERSAL_LOAD_AXES) or any(
            not _closed_int(load_vector.get(axis), 0, 3) for axis in UNIVERSAL_LOAD_AXES
        ):
            failures.append(issue("universal_hard_gate", "selected semantic load vector must cover the exact eight bounded axes", instance_key=list(key), actual=load_vector))
        else:
            if is_effect_projection and any(int(load_vector[axis]) != 0 for axis in UNIVERSAL_LOAD_AXES):
                failures.append(issue("universal_hard_gate", "contract effect projection cannot inject semantic load", instance_key=list(key), actual=load_vector))
            for axis in UNIVERSAL_LOAD_AXES:
                calculated_load_max[axis] = max(calculated_load_max[axis], int(load_vector[axis]))

    if len(selected_keys) != len(set(selected_keys)):
        failures.append(issue("universal_hard_gate", "selected hard-gate source instance keys must be unique", actual=[list(key) for key in selected_keys]))

    event_roles_value = _mapping(scene.get("selected_event")).get("roles")
    event_roles = event_roles_value if isinstance(event_roles_value, list) else []
    expected_role_ids = {
        str(role.get("role_id"))
        for role in event_roles
        if isinstance(role, dict) and role.get("value_id") is not None
    }
    actual_role_ids = {
        instance_id
        for instance_id in selected_by_kind.get("event_role", set())
        if not instance_id.startswith("event_role::")
    }
    if actual_role_ids != expected_role_ids:
        failures.append(issue("universal_hard_gate", "selected event-role sources must exactly cover every populated event role", expected=sorted(expected_role_ids), actual=sorted(actual_role_ids)))
    for instance_kind, scene_field, id_field in (
        ("atom", "atoms", "instance_id"),
        ("bridge", "bridges", "bridge_id"),
        ("resource_claim", "resource_claims", "claim_id"),
    ):
        expected_ids = {
            str(item.get(id_field))
            for item in (
                scene.get(scene_field)
                if isinstance(scene.get(scene_field), list)
                else []
            )
            if isinstance(item, dict) and _is_nonempty_string(item.get(id_field))
        }
        actual_ids = selected_by_kind.get(instance_kind, set())
        if actual_ids != expected_ids:
            failures.append(issue("universal_hard_gate", "selected source projection does not exactly cover its scene instances", instance_kind=instance_kind, expected=sorted(expected_ids), actual=sorted(actual_ids)))
    atom_by_id = {
        str(atom.get("instance_id")): atom
        for atom in (
            scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
        )
        if isinstance(atom, dict) and _is_nonempty_string(atom.get("instance_id"))
    }
    for instance_id, atom in atom_by_id.items():
        selected_atom = selected_item_by_key.get(("atom", instance_id))
        if isinstance(selected_atom, Mapping) and selected_atom.get("load_vector") != atom.get("load_vector"):
            failures.append(
                issue(
                    "universal_hard_gate",
                    "atom hard-gate load must exactly copy the selected canonical atom load",
                    instance_id=instance_id,
                    expected=atom.get("load_vector"),
                    actual=selected_atom.get("load_vector"),
                )
            )
    for claim in (
        scene.get("resource_claims")
        if isinstance(scene.get("resource_claims"), list)
        else []
    ):
        if not isinstance(claim, dict) or not _is_nonempty_string(claim.get("claim_id")):
            continue
        claimant = atom_by_id.get(str(claim.get("claimant_id")))
        selected_claim = selected_item_by_key.get(("resource_claim", str(claim["claim_id"])))
        expected_load = claimant.get("load_vector") if isinstance(claimant, Mapping) else None
        if isinstance(selected_claim, Mapping) and selected_claim.get("load_vector") != expected_load:
            failures.append(
                issue(
                    "universal_hard_gate",
                    "resource-claim hard-gate load must exactly copy its claimant atom load",
                    claim_id=claim.get("claim_id"),
                    claimant_id=claim.get("claimant_id"),
                    expected=expected_load,
                    actual=selected_claim.get("load_vector"),
                )
            )
    expected_proposal_ids = {
        str(atom.get("parameters", {}).get("proposal_id"))
        for atom in (
            scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
        )
        if isinstance(atom, dict)
        and isinstance(atom.get("parameters"), dict)
        and _is_nonempty_string(atom["parameters"].get("proposal_id"))
    }
    if selected_by_kind.get("proposal", set()) != expected_proposal_ids:
        failures.append(issue("universal_hard_gate", "proposal source projection must exactly cover selected proposal atoms", expected=sorted(expected_proposal_ids), actual=sorted(selected_by_kind.get("proposal", set()))))

    observed_effect_ids = _unique_string_list(snapshot.get("observed_effect_ids"))
    if observed_effect_ids is None or observed_effect_ids != sorted(observed_from_records):
        failures.append(
            issue(
                "universal_hard_gate",
                "observed_effect_ids must exactly equal the selected scoped occurrence union",
                expected=sorted(observed_from_records),
                actual=snapshot.get("observed_effect_ids"),
            )
        )
    semantic_load_max = snapshot.get("semantic_load_max")
    if semantic_load_max != calculated_load_max:
        failures.append(issue("universal_hard_gate", "semantic_load_max must be the component-wise selected-source maximum", expected=calculated_load_max, actual=semantic_load_max))

    guard_value = snapshot.get("guard_executions")
    if not isinstance(guard_value, list):
        failures.append(issue("universal_hard_gate", "guard_executions must be the complete 32-record execution list", actual=guard_value))
        guard_value = []
    guard_ids: list[str] = []
    guard_by_id: dict[str, Mapping[str, Any]] = {}
    for index, raw_guard in enumerate(guard_value):
        failures.extend(
            _exact_object_keys(
                raw_guard,
                UNIVERSAL_GUARD_EXECUTION_KEYS,
                check="universal_hard_gate",
                object_name=f"hard_gate_snapshot.guard_executions[{index}]",
            )
        )
        if not isinstance(raw_guard, dict):
            continue
        guard_id = raw_guard.get("guard_id")
        if guard_id not in UNIVERSAL_GUARD_EXECUTION_PREDICATES:
            failures.append(issue("universal_hard_gate", "guard execution id is outside the closed all-32 set", guard_id=guard_id))
            continue
        guard_id = str(guard_id)
        guard_ids.append(guard_id)
        guard_by_id[guard_id] = raw_guard
        if raw_guard.get("source_candidate_id") != guard_id:
            failures.append(issue("universal_hard_gate", "guard execution must bind its exact data-owned candidate", guard_id=guard_id, actual=raw_guard.get("source_candidate_id")))
        if not _hex64(raw_guard.get("source_contract_sha256")):
            failures.append(issue("universal_hard_gate", "guard source contract digest is malformed", guard_id=guard_id, actual=raw_guard.get("source_contract_sha256")))
        if raw_guard.get("stage") not in UNIVERSAL_GUARD_STAGES:
            failures.append(issue("universal_hard_gate", "guard stage is outside the closed enum", guard_id=guard_id, actual=raw_guard.get("stage")))
        if raw_guard.get("violation_code") != f"universal_guard::{guard_id}":
            failures.append(issue("universal_hard_gate", "guard violation code must bind its exact candidate id", guard_id=guard_id, actual=raw_guard.get("violation_code")))
        applicable = raw_guard.get("applicable")
        predicate_results = raw_guard.get("predicate_results")
        reason_codes = _unique_string_list(raw_guard.get("reason_codes"))
        if not isinstance(applicable, bool):
            failures.append(issue("universal_hard_gate", "guard applicability must be boolean", guard_id=guard_id, actual=applicable))
        elif applicable:
            valid_predicate = False
            if isinstance(predicate_results, list) and len(predicate_results) == 1:
                predicate = predicate_results[0]
                failures.extend(
                    _exact_object_keys(
                        predicate,
                        UNIVERSAL_GUARD_PREDICATE_KEYS,
                        check="universal_hard_gate",
                        object_name=f"guard predicate result {guard_id}",
                    )
                )
                if isinstance(predicate, dict):
                    binding_ids = _unique_string_list(predicate.get("binding_ids"))
                    valid_predicate = (
                        predicate.get("predicate_id") == UNIVERSAL_GUARD_EXECUTION_PREDICATES[guard_id]
                        and predicate.get("passed") is True
                        and bool(binding_ids)
                        and binding_ids == sorted(binding_ids)
                    )
            if not valid_predicate or raw_guard.get("outcome") != "pass" or reason_codes != ["all_guard_predicates_passed"]:
                failures.append(
                    issue(
                        "universal_hard_gate",
                        "applicable guard must expose one nonempty typed passing proof and pass outcome",
                        guard_id=guard_id,
                        predicate_results=predicate_results,
                        outcome=raw_guard.get("outcome"),
                        reason_codes=raw_guard.get("reason_codes"),
                    )
                )
        elif (
            predicate_results != []
            or raw_guard.get("outcome") != "not_applicable"
            or reason_codes != ["guard_not_applicable"]
        ):
            failures.append(
                issue(
                    "universal_hard_gate",
                    "nonapplicable guard must retain an explicit not-applicable result without predicate proof",
                    guard_id=guard_id,
                    predicate_results=predicate_results,
                    outcome=raw_guard.get("outcome"),
                    reason_codes=raw_guard.get("reason_codes"),
                )
            )
    expected_guard_ids = sorted(UNIVERSAL_GUARD_EXECUTION_PREDICATES)
    if guard_ids != expected_guard_ids:
        failures.append(
            issue(
                "universal_hard_gate",
                "guard executions must exactly cover all 32 data-owned guards in canonical order",
                expected=expected_guard_ids,
                actual=guard_ids,
            )
        )
    for guard_id in sorted(UNIVERSAL_REQUIRED_GUARD_IDS):
        guard = guard_by_id.get(guard_id)
        if not isinstance(guard, dict) or guard.get("applicable") is not True or guard.get("outcome") != "pass":
            failures.append(issue("universal_hard_gate", "compiled-required guard must be applicable and pass", guard_id=guard_id))
    if snapshot.get("hard_gate_pass") is not True:
        failures.append(issue("universal_hard_gate", "candidate pack cannot survive a blocked or non-boolean hard gate", actual=snapshot.get("hard_gate_pass")))

    snapshot_sha = snapshot.get("snapshot_sha256")
    hashable_snapshot = dict(snapshot)
    hashable_snapshot.pop("snapshot_sha256", None)
    expected_snapshot_sha = hashlib.sha256(
        canonical_json(hashable_snapshot).encode("utf-8")
    ).hexdigest()
    if snapshot_sha != expected_snapshot_sha:
        failures.append(issue("universal_hard_gate", "hard-gate snapshot digest does not match canonical content", expected=expected_snapshot_sha, actual=snapshot_sha))
    trace_snapshot_sha = _mapping(scene.get("selection_trace")).get("hard_gate_snapshot_sha256")
    if trace_snapshot_sha != snapshot_sha or not _hex64(trace_snapshot_sha):
        failures.append(issue("universal_hard_gate", "selection trace must bind the exact hard-gate snapshot digest", expected=snapshot_sha, actual=trace_snapshot_sha))
    return failures


def _audit_semantic_tokens(value: Any) -> tuple[str, ...]:
    return tuple(re.findall(r"[a-z0-9]+", _normalized_literal_text(value)))


def _audit_contains_token_subsequence(
    haystack: Sequence[str], needle: Sequence[str]
) -> bool:
    return bool(needle) and any(
        tuple(haystack[index : index + len(needle)]) == tuple(needle)
        for index in range(len(haystack) - len(needle) + 1)
    )


def _audit_participant_primary(
    scene: Mapping[str, Any], role_id: str
) -> str | None:
    contract = _mapping(scene.get("scene_contract"))
    for binding in (
        contract.get("participant_bindings")
        if isinstance(contract.get("participant_bindings"), list)
        else []
    ):
        if isinstance(binding, dict) and binding.get("role_id") == role_id:
            primary = binding.get("primary_entity_id")
            return str(primary) if _is_nonempty_string(primary) else None
    return None


def _audit_matched_catalog_prop_ids(
    scene: Mapping[str, Any], assets: Any
) -> set[str]:
    """Resolve catalog props from fixed semantic values, never request keywords."""

    contract = _mapping(scene.get("scene_contract"))
    slots = {
        str(slot.get("slot_id")): slot
        for slot in (
            contract.get("slot_states")
            if isinstance(contract.get("slot_states"), list)
            else []
        )
        if isinstance(slot, dict) and _is_nonempty_string(slot.get("slot_id"))
    }
    prop_slot = slots.get("prop")
    if not isinstance(prop_slot, dict) or prop_slot.get("state") != "fixed":
        return set()
    semantic_values = list(_string_list(prop_slot.get("value_ids")) or [])
    literal_phrases = list(_string_list(prop_slot.get("request_phrases")) or [])
    roles = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, dict) and _is_nonempty_string(role.get("role_id"))
    }
    for role_id in ("target", "instrument"):
        role = roles.get(role_id)
        if not isinstance(role, dict):
            continue
        if _is_nonempty_string(role.get("value_id")):
            semantic_values.append(str(role["value_id"]))
        if role.get("state") == "fixed":
            literal_phrases.extend(_string_list(role.get("request_phrases")) or [])

    value_tokens = [_audit_semantic_tokens(value) for value in semantic_values]
    prop_by_id = getattr(assets, "prop_by_id", {})
    result: set[str] = set()
    for prop_id, raw_prop in (
        prop_by_id.items() if isinstance(prop_by_id, Mapping) else []
    ):
        if not isinstance(raw_prop, Mapping):
            continue
        prop_tokens = list(_audit_semantic_tokens(prop_id))
        if prop_tokens[:1] == ["prop"]:
            prop_tokens = prop_tokens[1:]
        semantic_names = [tuple(prop_tokens)]
        semantic_names.extend(
            _audit_semantic_tokens(alias)
            for record in raw_prop.get("aliases", [])
            if isinstance(record, Mapping) and record.get("locale") == "en"
            for alias in (_string_list(record.get("values")) or [])
        )
        if any(
            _audit_contains_token_subsequence(tokens, semantic_name)
            for tokens in value_tokens
            for semantic_name in semantic_names
        ):
            result.add(str(prop_id))

    prop_senses = getattr(assets, "prop_sense_by_catalog_id", {})
    for profiles in (
        prop_senses.values() if isinstance(prop_senses, Mapping) else []
    ):
        for profile in profiles if isinstance(profiles, Sequence) else []:
            if not isinstance(profile, Mapping) or not _is_nonempty_string(
                profile.get("activation_target")
            ):
                continue
            aliases = [
                str(alias)
                for record in profile.get("literal_aliases", [])
                if isinstance(record, Mapping)
                for alias in (_string_list(record.get("values")) or [])
            ]
            literal_match = any(
                _literal_catalog_alias_matches(alias, phrase)
                for alias in aliases
                for phrase in literal_phrases
            )
            semantic_match = any(
                _audit_contains_token_subsequence(
                    value_tokens_item, _audit_semantic_tokens(token)
                )
                for token in (_string_list(profile.get("accepted_semantic_tokens")) or [])
                for value_tokens_item in value_tokens
            )
            if literal_match and semantic_match:
                result.add(str(profile["activation_target"]))
    return result


def _audit_derived_facet_state(
    facet: str,
    *,
    contract: Mapping[str, Any],
    actor_entity_id: str,
) -> str | None:
    slots = {
        str(slot.get("slot_id")): slot
        for slot in (
            contract.get("slot_states")
            if isinstance(contract.get("slot_states"), list)
            else []
        )
        if isinstance(slot, dict)
    }
    roles = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, dict)
    }
    if facet == "expression":
        return _mapping(slots.get("expression")).get("state")
    if facet == "perceived_affect":
        return "closed" if _mapping(slots.get("expression")).get("state") == "closed" else "open"
    if facet == "attention":
        channel_ids = {
            "attention_channel", "head_orientation", "body_orientation",
            "body_contour_display", "internal_luminance_display", "light_emission",
            "surface_signal", "mobile_ear_pair", "wing_axis_pair", "tail_axis",
            "mechanical_state_displacement",
        }
        identity = _mapping(contract.get("identity_core"))
        actor_entity = next(
            (
                entity
                for entity in identity.get("entities", [])
                if isinstance(entity, dict) and entity.get("entity_id") == actor_entity_id
            ),
            {},
        )
        relevant = [
            capability
            for capability in (
                actor_entity.get("capabilities")
                if isinstance(actor_entity, dict)
                and isinstance(actor_entity.get("capabilities"), list)
                else []
            )
            if isinstance(capability, dict) and capability.get("id") in channel_ids
        ]
        if relevant and all(item.get("state") == "unavailable" for item in relevant):
            return "closed"
        return "open"
    if facet == "pose":
        return _mapping(slots.get("pose")).get("state")
    if facet == "gesture":
        return "closed" if _mapping(slots.get("pose")).get("state") == "closed" else "open"
    if facet == "action":
        return _mapping(slots.get("action")).get("state")
    if facet == "phase":
        role_state = _mapping(roles.get("phase")).get("state")
        return role_state if role_state != "open" else (
            "closed" if _mapping(slots.get("action")).get("state") == "closed" else "open"
        )
    if facet == "relation":
        return _mapping(slots.get("relation")).get("state")
    if facet == "contact":
        return "closed" if _mapping(slots.get("relation")).get("state") == "closed" else "open"
    if facet == "prop":
        return _mapping(slots.get("prop")).get("state")
    if facet == "prop_state":
        return "closed" if _mapping(slots.get("prop")).get("state") == "closed" else "open"
    if facet == "environment":
        return _mapping(slots.get("environment")).get("state")
    if facet == "consequence":
        if (
            _mapping(slots.get("action")).get("state") == "closed"
            and _mapping(roles.get("result")).get("state") != "fixed"
        ):
            return "closed"
        return "open"
    return "open" if facet in {"bridge", "salience"} else None


def _audit_context_predicate_truth(
    predicate: Sequence[str],
    *,
    scene: Mapping[str, Any],
    assets: Any,
    matched_prop_ids: set[str],
    selected_candidate_ids: set[str],
    provided_predicates: set[tuple[str, str, str]],
) -> bool:
    if len(predicate) != 3:
        return False
    kind, subject, value = (str(item) for item in predicate)
    contract = _mapping(scene.get("scene_contract"))
    actor_entity_id = _audit_participant_primary(scene, "actor") or ""
    selected_roles = {
        str(role.get("role_id")): role
        for role in (
            _mapping(scene.get("selected_event")).get("roles")
            if isinstance(_mapping(scene.get("selected_event")).get("roles"), list)
            else []
        )
        if isinstance(role, dict)
    }
    contract_roles = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, dict)
    }
    if kind == "slot":
        state = _audit_derived_facet_state(
            subject, contract=contract, actor_entity_id=actor_entity_id
        )
        return state == value or (value == "open_or_fixed" and state in {"open", "fixed"})
    if kind == "event_role":
        if value in {"contract_fixed", "contract_open", "contract_closed"}:
            return _mapping(contract_roles.get(subject)).get("state") == value.removeprefix("contract_")
        if value == "present":
            return bool(_mapping(selected_roles.get(subject)).get("value_id"))
        if value == "explicit_none":
            return _mapping(contract_roles.get(subject)).get("state") == "closed"
        return _mapping(selected_roles.get(subject)).get("value_id") == value
    if kind == "capability":
        if subject != "actor":
            return False
        identity = _mapping(contract.get("identity_core"))
        actor_entity = next(
            (
                entity
                for entity in identity.get("entities", [])
                if isinstance(entity, dict) and entity.get("entity_id") == actor_entity_id
            ),
            {},
        )
        capabilities = [
            capability
            for capability in (
                actor_entity.get("capabilities")
                if isinstance(actor_entity, dict)
                and isinstance(actor_entity.get("capabilities"), list)
                else []
            )
            if isinstance(capability, dict)
        ]
        available = {
            str(capability.get("id")): int(capability.get("capacity", 0))
            for capability in capabilities
            if capability.get("state") == "available"
        }
        if value == "manipulator_or_equivalent":
            equivalents = {
                "manipulator", "mouth", "appendage", "wing_appendage", "tail_axis",
                "body_orientation", "support_contact", "external_anchor",
            }
            return any(available.get(item, 0) > 0 for item in equivalents)
        if value == "nonhuman_display_channel":
            channels = {
                "appendage", "wing_appendage", "body_orientation", "body_contour_display",
                "surface_signal", "light_emission", "internal_luminance_display",
                "mobile_ear_pair", "wing_axis_pair", "tail_axis",
                "mechanical_state_displacement",
            }
            return any(available.get(item, 0) > 0 for item in channels)
        if value == "manipulator_capacity_gte_4":
            return available.get("manipulator", 0) >= 4
        if value.endswith("_unavailable"):
            capability_id = value.removesuffix("_unavailable")
            return any(
                capability.get("id") == capability_id
                and capability.get("state") == "unavailable"
                and capability.get("capacity") == 0
                for capability in capabilities
            )
        return available.get(value, 0) > 0
    if kind == "normalized_prop_concept":
        return value in matched_prop_ids
    if kind == "context":
        context = _mapping(contract.get("context_profile"))
        if subject == "identity_core":
            return value == "available"
        if subject == "social" and value == "dyad_or_ensemble":
            return context.get("social") in {"dyad", "ensemble"}
        if subject == "tool_state" and value == "safe_inactive":
            return context.get("violence") in {"closed", "nonviolent"}
        if subject == "weapon_state" and value == "decommissioned_or_other_policy_eligible":
            return (
                "prop_decommissioned_machine_gun" in matched_prop_ids
                and context.get("violence") != "active"
                and context.get("era_technology") == "decommissioned_firearm"
            )
        return context.get(subject) == value
    if kind == "policy":
        return subject == "local_default_metadata" and value == "automatic_pass"
    if kind == "cardinality" and subject == "actors" and value == "at_least_2":
        return sum(
            int(entity.get("quantity", 0))
            for entity in _mapping(contract.get("identity_core")).get("entities", [])
            if isinstance(entity, dict)
        ) >= 2
    if kind == "candidate":
        return bool(selected_candidate_ids) if (subject, value) == ("selected", "true") else (
            subject in selected_candidate_ids and value == "selected"
        )
    if kind == "facet_evidence":
        return (kind, subject, value) in provided_predicates
    if kind == "guard_contract":
        compatibility = getattr(assets, "compatibility", {})
        return (
            value == "satisfied"
            and subject in (
                compatibility.get("guard_candidate_ids", [])
                if isinstance(compatibility, Mapping)
                else []
            )
        )
    if kind == "resource_available":
        return value != "false"
    if kind == "visible_evidence":
        return value == "present"
    if kind in {"bridge", "rule"}:
        return (kind, subject, value) in provided_predicates
    return False


def _audit_expected_context_overlay_pairs(
    scene: Mapping[str, Any], assets: Any, matched_prop_ids: set[str]
) -> list[tuple[str, str]]:
    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, dict)
    ]
    instances_by_candidate: dict[str, list[str]] = {}
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    provided_predicates: set[tuple[str, str, str]] = set()
    for atom in atoms:
        candidate_id = str(atom.get("candidate_id"))
        instances_by_candidate.setdefault(candidate_id, []).append(str(atom.get("instance_id")))
        candidate = candidate_by_id.get(candidate_id) if isinstance(candidate_by_id, Mapping) else None
        if isinstance(candidate, Mapping):
            provided_predicates.update(
                tuple(str(value) for value in predicate)
                for predicate in candidate.get("postconditions", [])
                if isinstance(predicate, Sequence) and len(predicate) == 3
            )
    selected_candidate_ids = set(instances_by_candidate)
    candidates = getattr(assets, "candidates", {})
    profiles = (
        candidates.get("context_distance_profiles", [])
        if isinstance(candidates, Mapping)
        else []
    )
    context = _mapping(scene.get("scene_contract")).get("context_profile")
    violence = _mapping(context).get("violence")
    pairs: list[tuple[str, str]] = []
    for profile in sorted(
        (item for item in profiles if isinstance(item, Mapping)),
        key=lambda item: str(item.get("id")),
    ):
        candidate_ids = [str(item) for item in profile.get("candidate_ids", [])]
        if not candidate_ids or not set(candidate_ids) <= selected_candidate_ids:
            continue
        truth = lambda predicate: _audit_context_predicate_truth(
            predicate,
            scene=scene,
            assets=assets,
            matched_prop_ids=matched_prop_ids,
            selected_candidate_ids=selected_candidate_ids,
            provided_predicates=provided_predicates,
        )
        if not all(truth(item) for item in profile.get("requires_all", [])):
            continue
        if any(
            not any(truth(item) for item in group)
            for group in profile.get("requires_any", [])
        ):
            continue
        if any(truth(item) for item in profile.get("forbids_any", [])):
            continue
        if profile.get("policy_mode") == "safe_tool" and violence == "active":
            continue
        if (
            profile.get("policy_mode") == "explicit_weapon_only"
            and "prop_decommissioned_machine_gun" not in matched_prop_ids
        ):
            continue
        carrier_id = str(profile.get("carrier_candidate_id"))
        carrier_instances = sorted(instances_by_candidate.get(carrier_id, []))
        if carrier_instances:
            pairs.append((str(profile.get("id")), carrier_instances[0]))
    return sorted(pairs)


def _audit_guard_predicate_applicable(
    predicate_id: str,
    *,
    scene: Mapping[str, Any],
    assets: Any,
    matched_prop_ids: set[str],
    observed_effect_ids: set[str],
) -> bool:
    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, dict)
    ]
    facets = {str(atom.get("facet")) for atom in atoms}
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    topic_ids = {
        str(topic_id)
        for atom in atoms
        for topic_id in (
            _mapping(candidate_by_id.get(str(atom.get("candidate_id")))).get(
                "research_topic_ids", []
            )
            if isinstance(candidate_by_id, Mapping)
            else []
        )
    }
    if predicate_id in {
        "display_inner_state_not_claimed",
        "event_roles_coherent",
        "weapon_event_safe",
        "resource_capacity_within_declared",
        "narrative_effects_absent",
        "weapon_role_target_safe",
        "prop_literal_sense_bound",
        "relation_event_edges_connected",
        "theme_load_within_limit",
    }:
        return True
    if predicate_id in {"display_cues_contextualized", "display_inner_state_not_claimed"}:
        return "perceived_affect" in facets
    if predicate_id == "attention_intention_not_claimed":
        return "attention" in facets
    if predicate_id in {"nonhuman_channel_context_bound", "nonhuman_inner_state_not_claimed"}:
        return "nonhuman_expression_channels" in topic_ids
    if predicate_id == "facial_motion_inner_state_not_claimed":
        return "observable_facial_motion" in topic_ids
    if predicate_id in {"weapon_event_safe", "weapon_role_target_safe"}:
        return "prop_decommissioned_machine_gun" in matched_prop_ids or bool(
            observed_effect_ids
            & {
                "active_weapon_discharge",
                "combat_opponent_assignment",
                "combat_target_assignment",
            }
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
        return bool(_mapping(scene.get("semantic_distance_trace")).get("remote_atom_ids"))
    if predicate_id == "physical_relation_grounded":
        return bool(facets & {"contact", "relation"})
    if predicate_id == "history_claim_pixel_grounded":
        return "prop_state" in facets
    if predicate_id == "prop_literal_sense_bound":
        return bool(matched_prop_ids)
    if predicate_id == "local_policy_authority_separated":
        return any(
            isinstance(atom.get("parameters"), dict)
            and "proposal_id" in atom["parameters"]
            for atom in atoms
        ) or any(
            any(
                isinstance(predicate, Sequence)
                and len(predicate) == 3
                and predicate[0] == "policy"
                for predicate in _mapping(
                    candidate_by_id.get(str(atom.get("candidate_id")))
                ).get("runtime_contract", {}).get("requires_all", [])
            )
            for atom in atoms
        )
    return True


def _audit_guard_predicate_result(
    predicate_id: str,
    *,
    scene: Mapping[str, Any],
    assets: Any,
    matched_prop_ids: set[str],
    observed_effect_ids: set[str],
    effect_occurrences: Sequence[Mapping[str, Any]],
) -> tuple[bool, list[str]]:
    event = _mapping(scene.get("selected_event"))
    roles = {
        str(item.get("role_id")): item
        for item in (event.get("roles") if isinstance(event.get("roles"), list) else [])
        if isinstance(item, dict)
    }
    atoms = [item for item in scene.get("atoms", []) if isinstance(item, dict)]
    bridges = [item for item in scene.get("bridges", []) if isinstance(item, dict)]
    claims = [item for item in scene.get("resource_claims", []) if isinstance(item, dict)]
    pixels = _mapping(scene.get("pixel_evidence_contract"))
    pixel_items = {
        str(item.get("item_id")): item
        for item in (pixels.get("items") if isinstance(pixels.get("items"), list) else [])
        if isinstance(item, dict)
    }
    edges = {
        str(item.get("edge_id")): item
        for item in (event.get("spine_edges") if isinstance(event.get("spine_edges"), list) else [])
        if isinstance(item, dict)
    }
    atom_by_id = {str(atom.get("instance_id")): atom for atom in atoms}
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    candidate_by_atom = {
        str(atom.get("instance_id")): _mapping(
            candidate_by_id.get(str(atom.get("candidate_id")))
            if isinstance(candidate_by_id, Mapping)
            else None
        )
        for atom in atoms
    }
    facet_atoms: dict[str, list[Mapping[str, Any]]] = {}
    for atom in atoms:
        facet_atoms.setdefault(str(atom.get("facet")), []).append(atom)

    contract = _mapping(scene.get("scene_contract"))
    identity = _mapping(contract.get("identity_core"))
    capacities: dict[tuple[str, str], int] = {
        (str(entity.get("entity_id")), str(capability.get("id"))): int(capability.get("capacity", 0))
        for entity in (
            identity.get("entities") if isinstance(identity.get("entities"), list) else []
        )
        if isinstance(entity, dict)
        for capability in (
            entity.get("capabilities") if isinstance(entity.get("capabilities"), list) else []
        )
        if isinstance(capability, dict)
    }
    capacities.update(
        {("scene", kind): amount for kind, amount in UNIVERSAL_SCENE_RESOURCE_CAPACITIES.items()}
    )
    claim_usage: dict[tuple[str, str], tuple[int, int]] = {}
    for claim in claims:
        key = (str(claim.get("owner_id")), str(claim.get("resource_kind")))
        exclusive, shared = claim_usage.get(key, (0, 0))
        if claim.get("mode") == "exclusive":
            exclusive += int(claim.get("amount", 0))
        else:
            shared = max(shared, int(claim.get("amount", 0)))
        claim_usage[key] = (exclusive, shared)
    capacity_pass = all(
        key in capacities and exclusive + shared <= capacities[key]
        for key, (exclusive, shared) in claim_usage.items()
    )
    atom_edges_pass = all(
        isinstance(atom.get("event_edge_ids"), list)
        and len(atom["event_edge_ids"]) == 1
        and atom["event_edge_ids"][0] in edges
        and edges[atom["event_edge_ids"][0]].get("from_node_id") == "event_01"
        and edges[atom["event_edge_ids"][0]].get("to_node_id") == atom.get("instance_id")
        and edges[atom["event_edge_ids"][0]].get("relation_id") == f"realizes:{atom.get('facet')}"
        for atom in atoms
    )
    bridge_edges_pass = all(
        isinstance(bridge.get("event_edge_ids"), list)
        and len(bridge["event_edge_ids"]) == 1
        and bridge["event_edge_ids"][0] in edges
        and edges[bridge["event_edge_ids"][0]].get("from_node_id") == bridge.get("from_node_id")
        and edges[bridge["event_edge_ids"][0]].get("to_node_id") == bridge.get("to_node_id")
        and edges[bridge["event_edge_ids"][0]].get("relation_id") == f"bridge:{bridge.get('bridge_type')}"
        for bridge in bridges
    )
    bridge_pixels_pass = all(
        bool(bridge.get("pixel_evidence_ids"))
        and all(
            pixel_id in pixel_items
            and pixel_items[pixel_id].get("source_kind") == "bridge"
            and pixel_items[pixel_id].get("source_id") == bridge.get("bridge_id")
            for pixel_id in bridge.get("pixel_evidence_ids", [])
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
            *(str(atom.get("instance_id")) for atom in atoms),
            *(str(bridge.get("bridge_id")) for bridge in bridges),
            *(str(claim.get("claim_id")) for claim in claims),
        }
    )

    if predicate_id == "single_phase_present":
        phase = _mapping(roles.get("phase")).get("value_id")
        passed = bool(phase) and event.get("phase_id") == phase and all(
            claim.get("phase_id") == phase for claim in claims
        )
        return passed, [str(phase)] if phase else []
    if predicate_id == "dynamic_action_present":
        action = _mapping(roles.get("action")).get("value_id")
        action_atoms = [
            atom
            for facet in ("action", "phase", "contact")
            for atom in facet_atoms.get(facet, [])
        ]
        dynamic_bindings = [
            *(str(atom.get("instance_id")) for atom in action_atoms),
            *(str(bridge.get("bridge_id")) for bridge in bridges),
        ]
        return bool(action) and bool(dynamic_bindings), [str(action), *dynamic_bindings]
    if predicate_id == "display_cues_contextualized":
        display_atoms = facet_atoms.get("perceived_affect", [])
        return all(atom.get("bindings") and atom.get("pixel_evidence_ids") for atom in display_atoms), [
            str(atom.get("instance_id")) for atom in display_atoms
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
        nonnull_roles = {
            role_id for role_id, role in roles.items() if role.get("value_id") is not None
        }
        role_edge_ids = {
            str(edge.get("relation_id")).split(":", 1)[1]
            for edge in edges.values()
            if str(edge.get("relation_id")).startswith("has_role:")
        }
        return {"actor", "action", "phase"} <= nonnull_roles and role_edge_ids == nonnull_roles, sorted(nonnull_roles)
    if predicate_id == "nonhuman_channel_context_bound":
        nxc_atoms = [
            atom
            for atom_id, atom in atom_by_id.items()
            if "nonhuman_expression_channels" in candidate_by_atom[atom_id].get("research_topic_ids", [])
        ]
        return all(atom.get("bindings") and atom.get("pixel_evidence_ids") for atom in nxc_atoms), [
            str(atom.get("instance_id")) for atom in nxc_atoms
        ]
    if predicate_id == "weapon_event_safe":
        weapon_present = "prop_decommissioned_machine_gun" in matched_prop_ids
        if not weapon_present:
            return True, ["no_reviewed_weapon_present"]
        context = _mapping(contract.get("context_profile"))
        passed = (
            context.get("violence") != "active"
            and _mapping(roles.get("target")).get("value_id") is not None
            and "active_weapon_discharge" not in observed_effect_ids
        )
        return passed, ["prop_decommissioned_machine_gun", "target"]
    if predicate_id in {
        "resource_capacity_within_declared",
        "contact_resource_within_capacity",
        "resource_claims_within_capability",
    }:
        capability_records = [
            {
                "entity_id": str(entity.get("entity_id")),
                "resource_kind": str(capability.get("id")),
                "capacity": capability.get("capacity"),
                "state": capability.get("state"),
                "source": capability.get("source"),
                "source_fact_id": capability.get("source_fact_id"),
            }
            for entity in (
                identity.get("entities")
                if isinstance(identity.get("entities"), list)
                else []
            )
            if isinstance(entity, Mapping)
            for capability in (
                entity.get("capabilities")
                if isinstance(entity.get("capabilities"), list)
                else []
            )
            if isinstance(capability, Mapping)
        ]
        capability_records.extend(
            {
                "entity_id": "scene",
                "resource_kind": resource_kind,
                "capacity": capacity,
                "state": "available",
                "source": "compatibility_budget",
                "source_fact_id": f"compatibility:{resource_kind}",
            }
            for resource_kind, capacity in sorted(
                UNIVERSAL_SCENE_RESOURCE_CAPACITIES.items()
            )
        )
        capability_bindings = [
            ":".join(
                (
                    str(record["entity_id"]),
                    "capability",
                    str(record["resource_kind"]),
                    hashlib.sha256(
                        canonical_json(record).encode("utf-8")
                    ).hexdigest(),
                )
            )
            for record in capability_records
        ]
        attachment_capabilities = {
            "human_face_attachment": "facial_display",
            "human_hand_attachment": "manipulator",
            "human_limb_attachment": "appendage",
        }
        attachment_pass = True
        attachment_bindings: list[str] = []
        entity_ids = {
            str(entity.get("entity_id"))
            for entity in identity.get("entities", [])
            if isinstance(entity, dict)
        }
        for occurrence in effect_occurrences:
            effect_id = str(occurrence.get("effect_id"))
            capability_id = attachment_capabilities.get(effect_id)
            if capability_id is None:
                continue
            subject_ref = occurrence.get("subject_ref")
            if subject_ref is None or str(subject_ref) not in entity_ids:
                attachment_pass = False
                attachment_bindings.append(f"unresolved:{effect_id}")
                continue
            attachment_pass = attachment_pass and capacities.get(
                (str(subject_ref), capability_id), 0
            ) > 0
            attachment_bindings.append(f"{subject_ref}:{capability_id}")
        bindings = [
            *(str(claim.get("claim_id")) for claim in claims),
            *capability_bindings,
            *attachment_bindings,
        ] or ["no_resource_claim_or_attachment_effect"]
        return capacity_pass and attachment_pass, bindings
    if predicate_id == "narrative_effects_absent":
        bindings = sorted(observed_effect_ids) or ["no_blocked_narrative_effect_observed"]
        return not bool(observed_effect_ids & blocked_narrative_effects), bindings
    if predicate_id == "weapon_role_target_safe":
        weapon_present = "prop_decommissioned_machine_gun" in matched_prop_ids
        passed = not weapon_present or (
            _mapping(roles.get("target")).get("value_id") is not None
            and not bool(
                observed_effect_ids
                & {"combat_opponent_assignment", "combat_target_assignment"}
            )
        )
        return passed, ["target"] if weapon_present else ["no_reviewed_weapon_present"]
    if predicate_id == "gesture_context_bound":
        gesture_atoms = facet_atoms.get("gesture", [])
        return all(atom.get("bindings") and atom.get("pixel_evidence_ids") for atom in gesture_atoms), [
            str(atom.get("instance_id")) for atom in gesture_atoms
        ]
    if predicate_id == "bridge_path_connected":
        return bool(bridges) and bridge_edges_pass, [str(bridge.get("bridge_id")) for bridge in bridges]
    if predicate_id == "bridge_pixel_grounded":
        return bool(bridges) and bridge_pixels_pass, [str(bridge.get("bridge_id")) for bridge in bridges]
    if predicate_id == "contact_pixel_grounded":
        contact_atoms = facet_atoms.get("contact", [])
        passed = all(
            any(
                pixel_items.get(pixel_id, {}).get("kind") in {"contact", "support"}
                for pixel_id in atom.get("pixel_evidence_ids", [])
            )
            for atom in contact_atoms
        )
        return passed, [str(atom.get("instance_id")) for atom in contact_atoms]
    if predicate_id == "consequence_review_scale_declared":
        consequence_ids = set(pixels.get("consequence_item_ids", []))
        passed = bool(consequence_ids) and all(
            item_id in pixel_items and bool(pixel_items[item_id].get("minimum_scale_ids"))
            for item_id in consequence_ids
        )
        return passed, sorted(str(item) for item in consequence_ids)
    if predicate_id == "atom_event_edges_connected":
        return atom_edges_pass, [str(atom.get("instance_id")) for atom in atoms]
    if predicate_id == "prop_literal_sense_bound":
        selected_sources = {
            *(str(atom.get("candidate_id")) for atom in atoms),
            *(str(bridge.get("candidate_id")) for bridge in bridges),
        }
        prop_by_id = getattr(assets, "prop_by_id", {})
        fixed_prop_atoms = {
            candidate_id
            for candidate_id in selected_sources
            if any(
                candidate_id
                in _mapping(prop_by_id.get(prop_id)).get(
                    "affordance_candidate_ids", []
                )
                for prop_id in matched_prop_ids
            )
        }
        fixed_prop_atoms.update(
            str(candidate_id)
            for prop_id in matched_prop_ids
            for candidate_id in _mapping(prop_by_id.get(prop_id)).get(
                "affordance_candidate_ids", []
            )[:1]
        )
        passed = all(
            any(
                str(candidate_id) in fixed_prop_atoms
                for candidate_id in _mapping(prop_by_id.get(prop_id)).get(
                    "affordance_candidate_ids", []
                )
            )
            for prop_id in matched_prop_ids
        )
        return passed, sorted({*matched_prop_ids, *fixed_prop_atoms}) or [
            "no_reviewed_catalog_prop_present"
        ]
    if predicate_id == "relation_event_edges_connected":
        relation_atoms = facet_atoms.get("relation", [])
        passed = all(
            isinstance(atom.get("event_edge_ids"), list)
            and len(atom["event_edge_ids"]) == 1
            and atom["event_edge_ids"][0] in edges
            for atom in relation_atoms
        )
        return passed, [str(atom.get("instance_id")) for atom in relation_atoms] or [
            "no_selected_relation_atom"
        ]
    if predicate_id == "creativity_invariant_pool_traced":
        trace = _mapping(scene.get("selection_trace"))
        invariant = _mapping(scene.get("creativity_invariant_trace"))
        profiles = [
            str(row.get("record_id"))
            for row in invariant.get("eligible_proposals", [])
            if isinstance(row, Mapping)
        ]
        rejected = [
            {
                "proposal_id": str(row.get("record_id")),
                "reason_code": str((_string_list(row.get("reason_codes")) or [""])[0]),
            }
            for row in invariant.get("rejected_proposals", [])
            if isinstance(row, Mapping)
        ]
        candidate_ids = [
            str(candidate_id)
            for candidate_ids_for_facet in _mapping(
                trace.get("eligible_candidate_ids_by_facet")
            ).values()
            for candidate_id in (
                candidate_ids_for_facet
                if isinstance(candidate_ids_for_facet, list)
                else []
            )
        ]
        candidate_by_id = getattr(assets, "candidate_by_id", {})
        candidate_rejections = []
        for row in invariant.get("rejected_candidates", []):
            if not isinstance(row, Mapping):
                continue
            record_id = str(row.get("record_id"))
            reason_codes = _string_list(row.get("reason_codes")) or [""]
            reason = reason_codes[0]
            candidate = (
                candidate_by_id.get(record_id)
                if isinstance(candidate_by_id, Mapping)
                else None
            )
            facet = str(candidate.get("facet")) if isinstance(candidate, Mapping) else ""
            if reason == "closed_facet":
                reason = f"closed_facet:{facet}"
            elif reason == "fixed_facet_conflict":
                reason = f"fixed_facet:{facet}"
            candidate_rejections.append(
                {"candidate_id": record_id, "reason_code": reason}
            )
        passed = (
            invariant.get("complete_trace") is True
            and invariant.get("trace_sha256")
            == _audit_canonical_sha256(
                {
                    key: value
                    for key, value in invariant.items()
                    if key != "trace_sha256"
                }
            )
            and trace.get("eligible_proposal_profile_ids") == profiles
            and trace.get("proposal_rejections") == rejected
            and sorted(candidate_ids) == invariant.get("eligible_candidate_ids")
            and trace.get("candidate_rejections") == candidate_rejections
        )
        return passed, [str(invariant.get("trace_sha256")), *profiles]
    if predicate_id == "remote_budget_within_global":
        distance = _mapping(scene.get("semantic_distance_trace"))
        passed = (
            distance.get("max_optional_remote_count") == 1
            and int(distance.get("optional_remote_count", 0)) <= 1
            and (
                int(distance.get("fixed_remote_count", 0)) == 0
                or int(distance.get("optional_remote_count", 0)) == 0
            )
        )
        bindings = list(distance.get("remote_atom_ids", []))
        bindings.extend(
            [
                f"fixed_remote_count:{distance.get('fixed_remote_count')}",
                f"optional_remote_count:{distance.get('optional_remote_count')}",
                f"max_optional_remote_count:{distance.get('max_optional_remote_count')}",
            ]
        )
        return passed, bindings
    if predicate_id == "remote_premise_has_visible_bridge":
        remote_ids = set(_mapping(scene.get("semantic_distance_trace")).get("remote_atom_ids", []))
        bridged = {
            atom_id
            for atom_id in remote_ids
            if any(
                atom_id in {str(bridge.get("from_node_id")), str(bridge.get("to_node_id"))}
                for bridge in bridges
            )
        }
        return bridged == remote_ids and bridge_pixels_pass, sorted(str(item) for item in remote_ids)
    if predicate_id == "identity_core_preserved":
        entities = identity.get("entities") if isinstance(identity.get("entities"), list) else []
        selected_candidates = {str(atom.get("candidate_id")) for atom in atoms}
        return bool(entities) and "usl_core_identity_anchor" in selected_candidates, [
            str(entity.get("entity_id")) for entity in entities if isinstance(entity, dict)
        ]
    if predicate_id == "physical_relation_grounded":
        physical_atoms = [
            atom
            for facet in ("contact", "relation")
            for atom in facet_atoms.get(facet, [])
        ]
        return all(atom.get("event_edge_ids") and atom.get("pixel_evidence_ids") for atom in physical_atoms), [
            str(atom.get("instance_id")) for atom in physical_atoms
        ]
    if predicate_id == "history_claim_pixel_grounded":
        history_atoms = facet_atoms.get("prop_state", [])
        return all(atom.get("event_edge_ids") and atom.get("pixel_evidence_ids") for atom in history_atoms), [
            str(atom.get("instance_id")) for atom in history_atoms
        ]
    if predicate_id == "local_policy_authority_separated":
        allowed_policy = ("policy", "local_default_metadata", "automatic_pass")
        selected_candidate_ids = {str(atom.get("candidate_id")) for atom in atoms}
        selected_proposal_ids = {
            str(_mapping(atom.get("parameters")).get("proposal_id"))
            for atom in atoms
            if _is_nonempty_string(_mapping(atom.get("parameters")).get("proposal_id"))
        }
        candidates = getattr(assets, "candidates", {})
        proposal_profiles = [
            profile
            for profile in (
                candidates.get("proposal_profiles", [])
                if isinstance(candidates, Mapping)
                else []
            )
            if isinstance(profile, Mapping) and str(profile.get("id")) in selected_proposal_ids
        ]
        context_profiles = [
            profile
            for profile in (
                candidates.get("context_distance_profiles", [])
                if isinstance(candidates, Mapping)
                else []
            )
            if isinstance(profile, Mapping)
            and set(str(value) for value in profile.get("candidate_ids", [])) <= selected_candidate_ids
        ]
        policy_predicates = {
            tuple(str(value) for value in predicate)
            for atom in atoms
            for predicate in _mapping(
                _mapping(candidate_by_id.get(str(atom.get("candidate_id")))).get(
                    "runtime_contract"
                )
            ).get("requires_all", [])
            if isinstance(predicate, Sequence) and len(predicate) == 3 and predicate[0] == "policy"
        }
        policy_predicates.update(
            tuple(str(value) for value in predicate)
            for profile in [*proposal_profiles, *context_profiles]
            for predicate in profile.get("requires_all", [])
            if isinstance(predicate, Sequence) and len(predicate) == 3 and predicate[0] == "policy"
        )
        policy_modes = {
            str(profile.get("policy_mode")) for profile in [*proposal_profiles, *context_profiles]
        }
        passed = (
            (not policy_predicates or policy_predicates == {allowed_policy})
            and policy_modes <= {"ordinary", "safe_tool", "explicit_weapon_only"}
        )
        return passed, sorted("::".join(item) for item in policy_predicates) + sorted(
            f"policy_mode:{mode}" for mode in policy_modes
        )
    if predicate_id == "theme_load_within_limit":
        maximum = max(
            (int(_mapping(atom.get("load_vector")).get("theme_displacement", 0)) for atom in atoms),
            default=0,
        )
        prop_by_id = getattr(assets, "prop_by_id", {})
        fixed_theme_cap = max(
            (
                int(
                    _mapping(
                        _mapping(prop_by_id.get(prop_id)).get("base_load_profile")
                    ).get("theme_displacement", 0)
                )
                for prop_id in matched_prop_ids
            ),
            default=0,
        )
        allowed_maximum = max(2, fixed_theme_cap)
        return maximum <= allowed_maximum, [
            f"theme_displacement:{maximum}",
            f"allowed_theme_displacement:{allowed_maximum}",
        ]
    raise ValueError(f"unimplemented independent guard predicate: {predicate_id}")


def _audit_expected_hard_gate_snapshot(
    scene: Mapping[str, Any],
    assets: Any,
    semantic_bindings: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Rebuild every selected source and all 32 guard proofs from raw assets."""

    failures: list[dict[str, Any]] = []
    registry = _mapping(semantic_bindings.get("semantic_effect_registry"))
    raw_profiles = registry.get("profiles")
    effect_profiles: dict[tuple[str, str], tuple[str, ...]] = {}
    for profile in raw_profiles if isinstance(raw_profiles, list) else []:
        if not isinstance(profile, Mapping):
            continue
        source_key = (str(profile.get("source_kind")), str(profile.get("source_id")))
        effect_profiles[source_key] = tuple(
            str(effect_id) for effect_id in profile.get("effect_ids", [])
        )
    source_kind_order = {
        kind: index
        for index, kind in enumerate(
            (
                "visual_candidate",
                "proposal_profile",
                "context_profile",
                "bridge_type",
                "resource_kind",
            )
        )
    }

    def ordered_refs(*refs: tuple[str, str]) -> list[dict[str, str]]:
        unique = sorted(
            set(refs),
            key=lambda item: (source_kind_order.get(item[0], 10**6), item[1]),
        )
        for source_key in unique:
            if source_key not in effect_profiles:
                failures.append(
                    issue(
                        "universal_asset_binding",
                        "selected source lacks raw semantic-registry coverage",
                        source_kind=source_key[0],
                        source_id=source_key[1],
                    )
                )
        return [
            {"source_kind": source_kind, "source_id": source_id}
            for source_kind, source_id in unique
        ]

    def resolved_effects(
        refs: Sequence[Mapping[str, str]], subject_ref: str | None
    ) -> list[dict[str, Any]]:
        effects = sorted(
            {
                effect_id
                for ref in refs
                for effect_id in effect_profiles.get(
                    (str(ref["source_kind"]), str(ref["source_id"])), ()
                )
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

    zero_load = {axis: 0 for axis in UNIVERSAL_LOAD_AXES}
    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, dict)
    ]
    atom_by_id = {str(atom.get("instance_id")): atom for atom in atoms}
    bridges = [
        bridge
        for bridge in (
            scene.get("bridges") if isinstance(scene.get("bridges"), list) else []
        )
        if isinstance(bridge, dict)
    ]
    claims = [
        claim
        for claim in (
            scene.get("resource_claims")
            if isinstance(scene.get("resource_claims"), list)
            else []
        )
        if isinstance(claim, dict)
    ]
    actor_entity_id = _audit_participant_primary(scene, "actor") or ""
    if not actor_entity_id:
        failures.append(
            issue(
                "universal_scene_contract",
                "hard-gate replay requires the typed actor participant primary",
            )
        )
    selected_refs: list[dict[str, Any]] = []
    event = _mapping(scene.get("selected_event"))
    roles = [
        role
        for role in (event.get("roles") if isinstance(event.get("roles"), list) else [])
        if isinstance(role, dict)
    ]
    sorted_bridges = sorted(bridges, key=lambda item: str(item.get("bridge_id")))
    for role in roles:
        if role.get("value_id") is None:
            continue
        refs: list[dict[str, str]] = []
        scope = "contract_projection"
        source_id = str(role.get("source_id"))
        if role.get("source") == "runtime_selected" and source_id in atom_by_id:
            refs = ordered_refs(
                ("visual_candidate", str(atom_by_id[source_id].get("candidate_id")))
            )
            scope = "runtime_addition"
        elif role.get("source") == "runtime_selected" and not source_id.startswith(
            "identity_entity:"
        ):
            source_bridge = next(
                (
                    bridge
                    for bridge in sorted_bridges
                    if str(bridge.get("bridge_id")).endswith(source_id)
                ),
                None,
            )
            if source_bridge is None:
                failures.append(
                    issue(
                        "universal_hard_gate",
                        "runtime-selected role lacks its exact atom or bridge source",
                        role_id=role.get("role_id"),
                        source_id=source_id,
                    )
                )
            else:
                refs = ordered_refs(
                    ("visual_candidate", str(source_bridge.get("candidate_id"))),
                    ("bridge_type", str(source_bridge.get("bridge_type"))),
                )
                scope = "runtime_addition"
        selected_refs.append(
            {
                "instance_kind": "event_role",
                "instance_id": str(role.get("role_id")),
                "scope": scope,
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(
                    refs,
                    actor_entity_id if role.get("role_id") == "actor" else None,
                ),
                "load_vector": dict(zero_load),
            }
        )

    matched_prop_ids = _audit_matched_catalog_prop_ids(scene, assets)
    prop_by_id = getattr(assets, "prop_by_id", {})
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    for prop_id in sorted(matched_prop_ids):
        prop = _mapping(prop_by_id.get(prop_id) if isinstance(prop_by_id, Mapping) else None)
        source_candidate_id = next(
            (
                str(candidate_id)
                for candidate_id in prop.get("affordance_candidate_ids", [])
                if _mapping(
                    candidate_by_id.get(str(candidate_id))
                    if isinstance(candidate_by_id, Mapping)
                    else None
                ).get("role")
                == "visual_atom"
            ),
            None,
        )
        if source_candidate_id is None:
            failures.append(
                issue(
                    "universal_hard_gate",
                    "fixed catalog prop lacks a reviewed visual source",
                    prop_id=prop_id,
                )
            )
            continue
        refs = ordered_refs(("visual_candidate", source_candidate_id))
        selected_refs.append(
            {
                "instance_kind": "fixed_prop",
                "instance_id": prop_id,
                "scope": "contract_projection",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, actor_entity_id),
                "load_vector": dict(_mapping(prop.get("base_load_profile"))),
            }
        )

    for atom in atoms:
        refs = ordered_refs(("visual_candidate", str(atom.get("candidate_id"))))
        selected_refs.append(
            {
                "instance_kind": "atom",
                "instance_id": str(atom.get("instance_id")),
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, actor_entity_id),
                "load_vector": dict(_mapping(atom.get("load_vector"))),
            }
        )
    for bridge in bridges:
        refs = ordered_refs(
            ("visual_candidate", str(bridge.get("candidate_id"))),
            ("bridge_type", str(bridge.get("bridge_type"))),
        )
        candidate = _mapping(
            candidate_by_id.get(str(bridge.get("candidate_id")))
            if isinstance(candidate_by_id, Mapping)
            else None
        )
        selected_refs.append(
            {
                "instance_kind": "bridge",
                "instance_id": str(bridge.get("bridge_id")),
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, actor_entity_id),
                "load_vector": dict(
                    _mapping(_mapping(candidate.get("runtime_contract")).get("load_profile"))
                ),
            }
        )
    for claim in claims:
        claimant = atom_by_id.get(str(claim.get("claimant_id")))
        if claimant is None:
            failures.append(
                issue(
                    "universal_hard_gate",
                    "resource claim lacks its exact selected claimant atom",
                    claim_id=claim.get("claim_id"),
                    claimant_id=claim.get("claimant_id"),
                )
            )
            continue
        refs = ordered_refs(
            ("visual_candidate", str(claimant.get("candidate_id"))),
            ("resource_kind", str(claim.get("resource_kind"))),
        )
        subject_ref = None if claim.get("owner_id") == "scene" else str(claim.get("owner_id"))
        selected_refs.append(
            {
                "instance_kind": "resource_claim",
                "instance_id": str(claim.get("claim_id")),
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, subject_ref),
                "load_vector": dict(_mapping(claimant.get("load_vector"))),
            }
        )

    proposal_atoms = [
        atom
        for atom in atoms
        if _is_nonempty_string(_mapping(atom.get("parameters")).get("proposal_id"))
    ]
    if len(proposal_atoms) > 1:
        failures.append(
            issue(
                "universal_hard_gate",
                "hard-gate replay found multiple selected proposal atoms",
            )
        )
    candidates = getattr(assets, "candidates", {})
    proposal_by_id = {
        str(profile.get("id")): profile
        for profile in (
            candidates.get("proposal_profiles", [])
            if isinstance(candidates, Mapping)
            else []
        )
        if isinstance(profile, Mapping)
    }
    for atom in proposal_atoms:
        proposal_id = str(_mapping(atom.get("parameters")).get("proposal_id"))
        profile = _mapping(proposal_by_id.get(proposal_id))
        refs = ordered_refs(("proposal_profile", proposal_id))
        selected_refs.append(
            {
                "instance_kind": "proposal",
                "instance_id": proposal_id,
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, actor_entity_id),
                "load_vector": dict(_mapping(profile.get("load_profile"))),
            }
        )

    context_by_id = {
        str(profile.get("id")): profile
        for profile in (
            candidates.get("context_distance_profiles", [])
            if isinstance(candidates, Mapping)
            else []
        )
        if isinstance(profile, Mapping)
    }
    for profile_id, carrier_instance_id in _audit_expected_context_overlay_pairs(
        scene, assets, matched_prop_ids
    ):
        profile = _mapping(context_by_id.get(profile_id))
        refs = ordered_refs(("context_profile", profile_id))
        selected_refs.append(
            {
                "instance_kind": "context_overlay",
                "instance_id": f"{profile_id}::{carrier_instance_id}",
                "scope": "runtime_addition",
                "source_profile_refs": refs,
                "contract_effect_profile_ids": [],
                "effect_occurrences": resolved_effects(refs, actor_entity_id),
                "load_vector": dict(_mapping(profile.get("load_profile"))),
            }
        )

    observed_effect_ids = sorted(
        {
            str(occurrence["effect_id"])
            for item in selected_refs
            for occurrence in item["effect_occurrences"]
        }
    )
    semantic_load_max = {
        axis: max(
            (int(_mapping(item.get("load_vector")).get(axis, 0)) for item in selected_refs),
            default=0,
        )
        for axis in UNIVERSAL_LOAD_AXES
    }
    raw_guard_profiles = semantic_bindings.get("guard_execution_profiles")
    guard_profile_map = {
        str(profile.get("guard_id")): str(profile.get("predicate_id"))
        for profile in (
            raw_guard_profiles if isinstance(raw_guard_profiles, list) else []
        )
        if isinstance(profile, Mapping)
    }
    effect_occurrences = [
        occurrence
        for item in selected_refs
        for occurrence in item["effect_occurrences"]
    ]
    guard_executions: list[dict[str, Any]] = []
    observed_effect_set = set(observed_effect_ids)
    for guard_id in sorted(guard_profile_map):
        candidate = _mapping(
            candidate_by_id.get(guard_id)
            if isinstance(candidate_by_id, Mapping)
            else None
        )
        predicate_id = guard_profile_map[guard_id]
        applicable = _audit_guard_predicate_applicable(
            predicate_id,
            scene=scene,
            assets=assets,
            matched_prop_ids=matched_prop_ids,
            observed_effect_ids=observed_effect_set,
        )
        if applicable:
            passed, bindings = _audit_guard_predicate_result(
                predicate_id,
                scene=scene,
                assets=assets,
                matched_prop_ids=matched_prop_ids,
                observed_effect_ids=observed_effect_set,
                effect_occurrences=effect_occurrences,
            )
            predicate_results = [
                {
                    "predicate_id": predicate_id,
                    "passed": passed,
                    "binding_ids": sorted(set(bindings)),
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
        runtime_contract = _mapping(candidate.get("runtime_contract"))
        source_contract = {
            "guard_id": str(candidate.get("id")),
            "role": str(candidate.get("role")),
            "research_topic_ids": list(candidate.get("research_topic_ids", [])),
            "provenance_record_ids": list(candidate.get("provenance_record_ids", [])),
            "stage": str(runtime_contract.get("stage")),
            "violation_code": str(runtime_contract.get("violation_code")),
            "outcome": str(runtime_contract.get("outcome")),
        }
        guard_executions.append(
            {
                "guard_id": guard_id,
                "source_candidate_id": guard_id,
                "source_contract_sha256": hashlib.sha256(
                    canonical_json(source_contract).encode("utf-8")
                ).hexdigest(),
                "stage": str(runtime_contract.get("stage")),
                "violation_code": str(runtime_contract.get("violation_code")),
                "applicable": applicable,
                "predicate_results": predicate_results,
                "outcome": outcome,
                "reason_codes": reason_codes,
            }
        )
    expected: dict[str, Any] = {
        "schema": UNIVERSAL_HARD_GATE_SCHEMA,
        "asset_hashes": dict(getattr(assets, "asset_hashes", {})),
        "semantic_effect_registry_sha256": hashlib.sha256(
            canonical_json(registry).encode("utf-8")
        ).hexdigest(),
        "source_coverage": dict(_mapping(registry.get("counts"))),
        "selected_source_refs": selected_refs,
        "observed_effect_ids": observed_effect_ids,
        "semantic_load_max": semantic_load_max,
        "guard_executions": guard_executions,
        "hard_gate_pass": all(
            record["outcome"] != "block" for record in guard_executions
        ),
    }
    expected["snapshot_sha256"] = hashlib.sha256(
        canonical_json(expected).encode("utf-8")
    ).hexdigest()
    return expected, failures


def _audit_embodiment_projection_failures(
    scene: Mapping[str, Any], assets: Any
) -> list[dict[str, Any]]:
    """Apply the entity-owned catalog_exact/declared_subset capability rule."""

    failures: list[dict[str, Any]] = []
    contract = _mapping(scene.get("scene_contract"))
    identity = _mapping(contract.get("identity_core"))
    embodiment_by_id = getattr(assets, "embodiment_by_id", {})
    for entity in (
        identity.get("entities") if isinstance(identity.get("entities"), list) else []
    ):
        if not isinstance(entity, dict):
            continue
        entity_id = str(entity.get("entity_id"))
        profile_id = str(entity.get("embodiment_profile_id"))
        projection_mode = entity.get("capability_projection_mode")
        profile = (
            embodiment_by_id.get(profile_id)
            if isinstance(embodiment_by_id, Mapping)
            else None
        )
        actual_records = {
            str(capability.get("id")): {
                "id": str(capability.get("id")),
                "capacity": capability.get("capacity"),
                "state": capability.get("state"),
                "source": capability.get("source"),
                "source_fact_id": capability.get("source_fact_id"),
            }
            for capability in (
                entity.get("capabilities")
                if isinstance(entity.get("capabilities"), list)
                else []
            )
            if isinstance(capability, dict) and _is_nonempty_string(capability.get("id"))
        }
        if profile_id.startswith("custom_"):
            if profile is not None or projection_mode != "declared_subset":
                failures.append(
                    issue(
                        "universal_resource_capacity",
                        "custom embodiment must remain an inert declared_subset profile",
                        entity_id=entity_id,
                        profile_id=profile_id,
                        projection_mode=projection_mode,
                    )
                )
            profile_derived = sorted(
                capability_id
                for capability_id, record in actual_records.items()
                if record["source"] == "embodiment_profile"
            )
            if profile_derived:
                failures.append(
                    issue(
                        "universal_resource_capacity",
                        "custom embodiment cannot invent catalog-derived capabilities",
                        entity_id=entity_id,
                        capability_ids=profile_derived,
                    )
                )
            continue
        if not isinstance(profile, Mapping):
            failures.append(
                issue(
                    "universal_asset_binding",
                    "known embodiment profile is absent from the raw candidate asset",
                    entity_id=entity_id,
                    profile_id=profile_id,
                )
            )
            continue
        expected_records = {
            str(capability.get("id")): {
                "id": str(capability.get("id")),
                "capacity": int(capability.get("capacity", 0)),
                "state": (
                    "unavailable" if int(capability.get("capacity", 0)) == 0 else "available"
                ),
                "source": "embodiment_profile",
                "source_fact_id": profile_id,
            }
            for capability in profile.get("capability_capacities", [])
            if isinstance(capability, Mapping) and _is_nonempty_string(capability.get("id"))
        }
        if projection_mode == "catalog_exact":
            if actual_records != expected_records:
                failures.append(
                    issue(
                        "universal_resource_capacity",
                        "catalog_exact embodiment must project its full capability catalog exactly",
                        entity_id=entity_id,
                        profile_id=profile_id,
                        expected=expected_records,
                        actual=actual_records,
                    )
                )
            continue
        if projection_mode != "declared_subset":
            continue
        for capability_id, record in actual_records.items():
            if record["source"] != "embodiment_profile":
                continue
            expected = expected_records.get(capability_id)
            if record != expected:
                failures.append(
                    issue(
                        "universal_resource_capacity",
                        "declared_subset catalog-derived capability must exactly match its profile record",
                        entity_id=entity_id,
                        profile_id=profile_id,
                        capability_id=capability_id,
                        expected=expected,
                        actual=record,
                    )
                )
    return failures


def _audit_quiet_context_zero_theme_failures(
    assets: Any,
) -> list[dict[str, Any]]:
    """Keep the reviewed quiet-context carrier inert on every load axis."""

    candidates = getattr(assets, "candidates", {})
    raw_profiles = (
        candidates.get("context_distance_profiles", [])
        if isinstance(candidates, Mapping)
        else []
    )
    matching_profiles = [
        profile
        for profile in raw_profiles
        if isinstance(profile, Mapping)
        and profile.get("id") == "context_quiet_theme_guard_middle"
    ]
    expected_carrier_id = "usc_cbg_affordance_bridge_atom"
    if len(matching_profiles) != 1:
        return [
            issue(
                "universal_asset_binding",
                "the reviewed quiet-context profile must exist exactly once",
                profile_id="context_quiet_theme_guard_middle",
                profile_count=len(matching_profiles),
            )
        ]
    profile = matching_profiles[0]
    profile_load = _mapping(profile.get("load_profile"))
    profile_distance = _mapping(profile.get("distance_profile"))
    candidate_ids = _string_list(profile.get("candidate_ids")) or []
    carrier_id = profile.get("carrier_candidate_id")
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    carrier = _mapping(
        candidate_by_id.get(expected_carrier_id)
        if isinstance(candidate_by_id, Mapping)
        else None
    )
    carrier_runtime = _mapping(carrier.get("runtime_contract"))
    carrier_load = _mapping(carrier_runtime.get("load_profile"))
    carrier_distance = _mapping(
        _mapping(carrier_runtime.get("distance_profile")).get("base")
    )
    zero_load = {axis: 0 for axis in UNIVERSAL_LOAD_AXES}
    if (
        carrier_id != expected_carrier_id
        or expected_carrier_id not in candidate_ids
        or profile_distance.get("theme") != 0
        or profile_load.get("theme_displacement") != 0
        or carrier.get("role") != "visual_atom"
        or carrier_distance.get("theme") != 0
        or carrier_load != zero_load
    ):
        return [
            issue(
                "universal_asset_binding",
                "quiet-context theme evidence must use its reviewed zero-load carrier",
                profile_id="context_quiet_theme_guard_middle",
                expected_carrier_id=expected_carrier_id,
                actual_carrier_id=carrier_id,
                profile_theme_distance=profile_distance.get("theme"),
                profile_theme_load=profile_load.get("theme_displacement"),
                carrier_theme_distance=carrier_distance.get("theme"),
                carrier_load=carrier_load,
            )
        ]
    return []


def _audit_phase_projection_failures(
    scene: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Bind the one event phase to its role, carrier, and every claim."""

    failures: list[dict[str, Any]] = []
    contract = _mapping(scene.get("scene_contract"))
    contract_phase = next(
        (
            role
            for role in (
                contract.get("event_roles")
                if isinstance(contract.get("event_roles"), list)
                else []
            )
            if isinstance(role, Mapping) and role.get("role_id") == "phase"
        ),
        {},
    )
    event = _mapping(scene.get("selected_event"))
    phase_roles = [
        role
        for role in (event.get("roles") if isinstance(event.get("roles"), list) else [])
        if isinstance(role, Mapping) and role.get("role_id") == "phase"
    ]
    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, Mapping)
    ]
    phase_atoms = [atom for atom in atoms if atom.get("facet") == "phase"]
    if len(phase_roles) != 1 or len(phase_atoms) > 1:
        failures.append(
            issue(
                "universal_event_spine",
                "the event must expose one phase role and at most one typed phase atom",
                phase_role_count=len(phase_roles),
                phase_atom_ids=[atom.get("instance_id") for atom in phase_atoms],
            )
        )
        return failures
    phase_role = phase_roles[0]
    phase_value = phase_role.get("value_id")
    if (
        not _is_nonempty_string(phase_value)
        or event.get("phase_id") != phase_value
    ):
        failures.append(
            issue(
                "universal_event_spine",
                "selected event phase must exactly equal the typed phase-role value",
                event_phase_id=event.get("phase_id"),
                role_phase_value=phase_value,
            )
        )
    wrong_claim_ids = [
        str(claim.get("claim_id"))
        for claim in (
            scene.get("resource_claims")
            if isinstance(scene.get("resource_claims"), list)
            else []
        )
        if isinstance(claim, Mapping) and claim.get("phase_id") != phase_value
    ]
    wrong_binding_atoms = [
        str(atom.get("instance_id"))
        for atom in atoms
        if any(
            isinstance(binding, Mapping)
            and binding.get("role_id") == "phase"
            and binding.get("node_id") != phase_value
            for binding in (
                atom.get("bindings") if isinstance(atom.get("bindings"), list) else []
            )
        )
    ]
    if wrong_claim_ids or wrong_binding_atoms:
        failures.append(
            issue(
                "universal_event_spine",
                "every claim and phase binding must use the one selected phase value",
                phase_value=phase_value,
                wrong_claim_ids=wrong_claim_ids,
                wrong_binding_atom_ids=wrong_binding_atoms,
            )
        )
    source_atom = next(
        (
            atom
            for atom in atoms
            if atom.get("instance_id") == phase_role.get("source_id")
        ),
        None,
    )
    proposal_source = bool(
        isinstance(source_atom, Mapping)
        and _is_nonempty_string(_mapping(source_atom.get("parameters")).get("proposal_id"))
    )
    if (
        contract_phase.get("state") == "open"
        and phase_role.get("source") == "runtime_selected"
        and not proposal_source
    ):
        if (
            len(phase_atoms) != 1
            or source_atom is not phase_atoms[0]
            or source_atom.get("candidate_id") != phase_value
            or not any(
                isinstance(binding, Mapping)
                and binding.get("role_id") == "phase"
                and binding.get("requirement") == "required"
                and binding.get("node_id") == phase_value
                for binding in source_atom.get("bindings", [])
            )
        ):
            failures.append(
                issue(
                    "universal_event_spine",
                    "an open non-proposal phase must materialize exactly one self-provisioning phase atom",
                    phase_value=phase_value,
                    phase_source_id=phase_role.get("source_id"),
                    phase_atom_ids=[atom.get("instance_id") for atom in phase_atoms],
                    phase_candidate_ids=[atom.get("candidate_id") for atom in phase_atoms],
                )
            )
    return failures


def _audit_fixed_prop_candidate_boundary_failures(
    scene: Mapping[str, Any],
    assets: Any,
) -> list[dict[str, Any]]:
    """Separate fixed-prop eligibility from fixed-prop materialization."""

    contract = _mapping(scene.get("scene_contract"))
    prop_slot = next(
        (
            slot
            for slot in (
                contract.get("slot_states")
                if isinstance(contract.get("slot_states"), list)
                else []
            )
            if isinstance(slot, Mapping) and slot.get("slot_id") == "prop"
        ),
        {},
    )
    if prop_slot.get("state") != "fixed":
        return []
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    prop_by_id = getattr(assets, "prop_by_id", {})
    matched_prop_ids = _audit_matched_catalog_prop_ids(scene, assets)

    def catalog_owner_ids(candidate_id: str) -> set[str]:
        return {
            str(prop_id)
            for prop_id, prop in (
                prop_by_id.items() if isinstance(prop_by_id, Mapping) else []
            )
            if candidate_id
            in (_string_list(_mapping(prop).get("affordance_candidate_ids")) or [])
        }

    trace = _mapping(scene.get("selection_trace"))
    eligible_by_facet = _mapping(trace.get("eligible_candidate_ids_by_facet"))
    wrong_eligible: list[dict[str, Any]] = []
    for candidate_id in _string_list(eligible_by_facet.get("prop")) or []:
        candidate = _mapping(
            candidate_by_id.get(candidate_id)
            if isinstance(candidate_by_id, Mapping)
            else None
        )
        if candidate.get("role") != "visual_atom" or candidate.get("facet") != "prop":
            continue
        owners = catalog_owner_ids(candidate_id)
        if owners and not (owners & matched_prop_ids):
            wrong_eligible.append(
                {
                    "candidate_id": candidate_id,
                    "catalog_owner_ids": sorted(owners),
                }
            )
    wrong_selected: list[dict[str, Any]] = []
    for atom in (
        scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
    ):
        if not isinstance(atom, Mapping) or atom.get("facet") != "prop":
            continue
        candidate_id = str(atom.get("candidate_id"))
        owners = catalog_owner_ids(candidate_id)
        parameters = _mapping(atom.get("parameters"))
        if owners:
            invalid = not bool(owners & matched_prop_ids)
        else:
            # The common fixed-facet selector may materialize only a reviewed
            # catalog affordance.  An opaque/generic prop can enter the scene
            # solely through an exact active literal-realization profile.
            invalid = not _is_nonempty_string(
                parameters.get("literal_realization_profile_id")
            )
        if invalid:
            wrong_selected.append(
                {
                    "instance_id": atom.get("instance_id"),
                    "candidate_id": candidate_id,
                    "catalog_owner_ids": sorted(owners),
                    "literal_realization_profile_id": parameters.get(
                        "literal_realization_profile_id"
                    ),
                }
            )
    if not wrong_eligible and not wrong_selected:
        return []
    return [
        issue(
            "universal_candidate_eligibility",
            "fixed prop candidates must be catalog-compatible or catalog-neutral, while catalog-neutral selection requires exact literal authority",
            matched_prop_ids=sorted(matched_prop_ids),
            wrong_eligible=wrong_eligible,
            wrong_selected=wrong_selected,
        )
    ]


def _audit_semantic_anchor_authority_failures(
    scene: Mapping[str, Any], semantic_bindings: Mapping[str, Any]
) -> list[dict[str, Any]]:
    """Replay fixed value authority with data-owned directional polarity."""

    failures: list[dict[str, Any]] = []
    contract = _mapping(scene.get("scene_contract"))

    def record_matches(
        groups: Sequence[Mapping[str, Any]], phrases: Sequence[str]
    ) -> bool:
        for group_index, group in enumerate(groups):
            peer_aliases = [
                str(alternative)
                for peer_index, peer_group in enumerate(groups)
                if peer_index != group_index
                for alternative in (
                    _string_list(peer_group.get("alternatives")) or []
                )
            ]
            group_matches = False
            for phrase in phrases:
                polarities = _universal_literal_effect_polarities(
                    str(phrase),
                    _string_list(group.get("alternatives")) or [],
                    semantic_bindings,
                    include_target_absence=False,
                    include_target_substitution=True,
                    allow_postposed_logical=True,
                    allow_korean_postposed_copular=False,
                    allow_authenticated_nonascii_substrings=True,
                    allow_reviewed_nonascii_marker_affixes=True,
                    postposed_logical_barrier_aliases=peer_aliases,
                )
                if polarities and set(polarities) == {
                    str(group.get("required_polarity"))
                }:
                    group_matches = True
                    break
            if not group_matches:
                return False
        return True

    for slot in (
        contract.get("slot_states")
        if isinstance(contract.get("slot_states"), list)
        else []
    ):
        if not isinstance(slot, dict) or slot.get("state") != "fixed":
            continue
        for binding in (
            slot.get("value_phrase_bindings")
            if isinstance(slot.get("value_phrase_bindings"), list)
            else []
        ):
            if not isinstance(binding, dict):
                continue
            groups = [
                group
                for group in (
                    binding.get("semantic_anchor_groups")
                    if isinstance(binding.get("semantic_anchor_groups"), list)
                    else []
                )
                if isinstance(group, Mapping)
            ]
            phrases = _string_list(binding.get("request_phrases")) or []
            if groups and record_matches(groups, phrases):
                continue
            details = {
                "slot_id": slot.get("slot_id"),
                "value_id": binding.get("value_id"),
            }
            failures.extend(
                [
                    issue(
                        "universal_scene_contract",
                        "each fixed value semantic anchor must have its exact reviewed polarity in one of that value binding's own literal spans",
                        **details,
                    ),
                    issue(
                        "universal_slot_state",
                        "each fixed value semantic anchor must have its exact reviewed polarity in one of that value binding's own literal spans",
                        **details,
                    ),
                ]
            )
    for role in (
        contract.get("event_roles")
        if isinstance(contract.get("event_roles"), list)
        else []
    ):
        if not isinstance(role, dict) or role.get("state") != "fixed":
            continue
        groups = [
            group
            for group in (
                role.get("semantic_anchor_groups")
                if isinstance(role.get("semantic_anchor_groups"), list)
                else []
            )
            if isinstance(group, Mapping)
        ]
        phrases = _string_list(role.get("request_phrases")) or []
        if groups and record_matches(groups, phrases):
            continue
        failures.extend(
            [
                issue(
                    "universal_scene_contract",
                    "each fixed event-role semantic anchor must have its exact reviewed polarity in one of that role's own literal spans",
                    role_id=role.get("role_id"),
                    value_id=role.get("value_id"),
                ),
                issue(
                    "universal_event_spine",
                    "each fixed event-role semantic anchor must have its exact reviewed polarity in one of that role's own literal spans",
                    role_id=role.get("role_id"),
                    value_id=role.get("value_id"),
                ),
            ]
        )
    return failures


def _audit_literal_visual_realization_failures(
    scene: Mapping[str, Any],
    request_text: str,
    assets: Any,
    semantic_bindings: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Independently bind mandatory literal mechanisms to exact owned output.

    The public runtime replay remains a useful sibling check, but it is not the
    authority here.  This path derives profile activation, participant owners,
    selected/eligible quantifiers, atom parameters, pixels, and resource claims
    from the raw assets plus the embedded v2 contract.
    """

    failures: list[dict[str, Any]] = []
    raw_profiles = semantic_bindings.get("literal_visual_realization_profiles")
    if not isinstance(raw_profiles, list):
        return [
            issue(
                "universal_asset_binding",
                "semantic bindings must expose typed literal visual realization profiles",
            )
        ]
    contract = _mapping(scene.get("scene_contract"))
    slot_by_id = {
        str(slot.get("slot_id")): slot
        for slot in (
            contract.get("slot_states")
            if isinstance(contract.get("slot_states"), list)
            else []
        )
        if isinstance(slot, dict) and _is_nonempty_string(slot.get("slot_id"))
    }
    role_by_id = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, dict) and _is_nonempty_string(role.get("role_id"))
    }
    participant_by_role = {
        str(binding.get("role_id")): binding
        for binding in (
            contract.get("participant_bindings")
            if isinstance(contract.get("participant_bindings"), list)
            else []
        )
        if isinstance(binding, dict) and _is_nonempty_string(binding.get("role_id"))
    }
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    prop_by_id = getattr(assets, "prop_by_id", {})
    matched_prop_ids = _audit_matched_catalog_prop_ids(scene, assets)

    def hard_literal_clauses(value: str) -> tuple[str, ...]:
        normalized = _normalized_literal_text(value)
        for separator in UNIVERSAL_LITERAL_AUTHENTICATION_HARD_SEPARATORS:
            normalized = normalized.replace(
                _normalized_literal_text(separator), "\n"
            )
        return tuple(part.strip() for part in normalized.splitlines() if part.strip())

    def groups_match(
        groups: Sequence[Mapping[str, Any]], phrases: Sequence[str]
    ) -> bool:
        if not groups:
            return False
        for phrase in phrases:
            # Realization groups are one visual predicate.  A second sentence
            # or hard contrast cannot donate the missing mechanism lexeme to
            # the first, even when both happen to live in one stored phrase.
            clauses = hard_literal_clauses(str(phrase))
            if not clauses:
                continue
            for clause in clauses:
                all_groups_match = True
                for group_index, group in enumerate(groups):
                    alternatives = _string_list(group.get("alternatives")) or []
                    peer_aliases = [
                        str(alternative)
                        for peer_index, peer in enumerate(groups)
                        if peer_index != group_index
                        for alternative in (_string_list(peer.get("alternatives")) or [])
                    ]
                    polarities = _universal_literal_effect_polarities(
                        clause,
                        alternatives,
                        semantic_bindings,
                        include_target_absence=False,
                        include_target_substitution=True,
                        allow_postposed_logical=True,
                        allow_korean_postposed_copular=False,
                        allow_authenticated_nonascii_substrings=True,
                        allow_reviewed_nonascii_marker_affixes=True,
                        postposed_logical_barrier_aliases=peer_aliases,
                    )
                    if not polarities or set(polarities) != {
                        str(group.get("required_polarity"))
                    }:
                        all_groups_match = False
                        break
                if all_groups_match:
                    return True
        return False

    def resolved_owner_refs(profile: Mapping[str, Any]) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for participant in profile.get("participant_roles", []):
            if not isinstance(participant, Mapping):
                continue
            role_id = str(participant.get("role_id"))
            binding = participant_by_role.get(role_id, {})
            entity_ids = _string_list(binding.get("entity_ids")) or []
            if participant.get("entity_quantifier") == "primary":
                primary = binding.get("primary_entity_id")
                entity_ids = [str(primary)] if _is_nonempty_string(primary) else []
            result.extend(
                {"role_id": role_id, "entity_id": str(entity_id)}
                for entity_id in entity_ids
            )
        return result

    def value_bindings(profile: Mapping[str, Any]) -> list[Mapping[str, Any]]:
        slot_id = str(profile.get("source_slot_id"))
        slot = slot_by_id.get(slot_id)
        if not isinstance(slot, dict) or slot.get("state") != "fixed":
            return []
        for participant in profile.get("participant_roles", []):
            if not isinstance(participant, Mapping):
                return []
            binding = participant_by_role.get(str(participant.get("role_id")))
            if not isinstance(binding, dict) or not (
                _string_list(binding.get("entity_ids")) or []
            ):
                return []
            if (
                participant.get("entity_quantifier") == "primary"
                and not _is_nonempty_string(binding.get("primary_entity_id"))
            ):
                return []
        bindings = [
            binding
            for binding in (
                slot.get("value_phrase_bindings")
                if isinstance(slot.get("value_phrase_bindings"), list)
                else []
            )
            if isinstance(binding, Mapping)
        ]
        groups = [
            group
            for group in (
                profile.get("required_literal_groups")
                if isinstance(profile.get("required_literal_groups"), list)
                else []
            )
            if isinstance(group, Mapping)
        ]
        # No executable catch-all is accepted.  A literal realization must own
        # at least one reviewed polarized group in the raw semantic asset.
        if not groups:
            return []
        scope = profile.get("literal_scope")
        if scope == "fixed_value_bindings":
            if profile.get("mechanism_class_id") == "prop_contact_region":
                if any(
                    str(value_id) in prop_by_id
                    for value_id in (_string_list(slot.get("value_ids")) or [])
                ):
                    return []
                slot_phrases = {
                    _normalized_literal_text(str(phrase))
                    for binding in bindings
                    for phrase in (_string_list(binding.get("request_phrases")) or [])
                }
                role_phrases = {
                    _normalized_literal_text(str(phrase))
                    for role_id in ("target", "instrument")
                    for role in (role_by_id.get(role_id),)
                    if isinstance(role, dict) and role.get("state") == "fixed"
                    for phrase in (_string_list(role.get("request_phrases")) or [])
                }
                if not slot_phrases.intersection(role_phrases):
                    return []
            return [
                binding
                for binding in bindings
                if groups_match(
                    groups, _string_list(binding.get("request_phrases")) or []
                )
            ]
        if scope == "slot_phrases":
            if not groups_match(
                groups, _string_list(slot.get("request_phrases")) or []
            ):
                return []
            matched = [
                binding
                for binding in bindings
                if groups_match(
                    groups, _string_list(binding.get("request_phrases")) or []
                )
            ]
            return matched or bindings
        if scope == "request_text" and groups_match(
            groups, hard_literal_clauses(request_text)
        ):
            return bindings
        return []

    profile_by_id: dict[str, Mapping[str, Any]] = {}
    candidate_profile_ids: dict[str, list[str]] = {}
    seen_ranks: set[int] = set()
    seen_candidate_ids: set[str] = set()
    for index, profile in enumerate(raw_profiles):
        profile_name = f"literal_visual_realization_profiles[{index}]"
        failures.extend(
            _exact_object_keys(
                profile,
                UNIVERSAL_LITERAL_REALIZATION_PROFILE_KEYS,
                check="universal_asset_binding",
                object_name=profile_name,
            )
        )
        if not isinstance(profile, Mapping):
            continue
        profile_id = profile.get("id")
        candidate_group = _string_list(profile.get("candidate_group"))
        groups = profile.get("required_literal_groups")
        participant_roles = profile.get("participant_roles")
        owned_pixel_kinds = _string_list(profile.get("owned_pixel_kinds"))
        owned_resource_kinds = _string_list(profile.get("owned_resource_kinds"))
        rank = profile.get("selection_rank")
        invalid = False
        if not _is_nonempty_string(profile_id) or str(profile_id) in profile_by_id:
            invalid = True
        if (
            candidate_group is None
            or not candidate_group
            or candidate_group != sorted(set(candidate_group))
        ):
            invalid = True
        if (
            not isinstance(rank, int)
            or isinstance(rank, bool)
            or rank < 0
            or rank > 999
            or rank in seen_ranks
        ):
            invalid = True
        if profile.get("source_slot_id") not in slot_by_id:
            invalid = True
        if profile.get("literal_scope") not in UNIVERSAL_LITERAL_REALIZATION_SCOPE_IDS:
            invalid = True
        if profile.get("quantifier") not in {"any", "all"}:
            invalid = True
        if profile.get("enforcement") not in {"selected", "eligible"}:
            invalid = True
        if not isinstance(groups, list) or not groups or len(groups) > 3:
            invalid = True
        else:
            normalized_group_signatures: set[tuple[tuple[str, ...], str]] = set()
            for group in groups:
                if not isinstance(group, Mapping) or set(group) != UNIVERSAL_SEMANTIC_ANCHOR_GROUP_KEYS:
                    invalid = True
                    continue
                alternatives = _string_list(group.get("alternatives"))
                normalized_alternatives = tuple(
                    _normalized_literal_text(alternative)
                    for alternative in (alternatives or [])
                )
                signature = (
                    normalized_alternatives,
                    str(group.get("required_polarity")),
                )
                if (
                    alternatives is None
                    or not alternatives
                    or len(normalized_alternatives)
                    != len(set(normalized_alternatives))
                    or group.get("required_polarity") not in {"affirmative", "negated"}
                    or signature in normalized_group_signatures
                ):
                    invalid = True
                normalized_group_signatures.add(signature)
        if not isinstance(participant_roles, list) or not participant_roles:
            invalid = True
        else:
            participant_role_ids: list[str] = []
            for participant in participant_roles:
                if not isinstance(participant, Mapping) or set(participant) != UNIVERSAL_LITERAL_REALIZATION_PARTICIPANT_KEYS:
                    invalid = True
                    continue
                role_id = str(participant.get("role_id"))
                participant_role_ids.append(role_id)
                if (
                    role_id not in UNIVERSAL_ROLE_IDS
                    or participant.get("entity_quantifier") not in {"primary", "all"}
                ):
                    invalid = True
            if (
                len(participant_role_ids) != len(set(participant_role_ids))
                or participant_role_ids
                != sorted(
                    participant_role_ids,
                    key=lambda role_id: UNIVERSAL_ROLE_IDS.index(role_id)
                    if role_id in UNIVERSAL_ROLE_IDS
                    else len(UNIVERSAL_ROLE_IDS),
                )
            ):
                invalid = True
        if (
            owned_pixel_kinds is None
            or owned_pixel_kinds != sorted(set(owned_pixel_kinds))
            or owned_resource_kinds is None
            or owned_resource_kinds != sorted(set(owned_resource_kinds))
        ):
            invalid = True
        candidate_pixel_sets: list[set[str]] = []
        candidate_resource_sets: list[set[str]] = []
        participant_role_set = {
            str(participant.get("role_id"))
            for participant in (
                participant_roles if isinstance(participant_roles, list) else []
            )
            if isinstance(participant, Mapping)
        }
        for candidate_id in candidate_group or []:
            candidate = (
                candidate_by_id.get(candidate_id)
                if isinstance(candidate_by_id, Mapping)
                else None
            )
            if (
                not isinstance(candidate, Mapping)
                or candidate.get("role") != "visual_atom"
                or candidate.get("facet") != profile.get("realized_facet")
                or candidate_id in seen_candidate_ids
            ):
                invalid = True
                continue
            seen_candidate_ids.add(candidate_id)
            runtime_contract = candidate.get("runtime_contract")
            runtime_contract = runtime_contract if isinstance(runtime_contract, Mapping) else {}
            candidate_binding_roles = {
                str(binding[0])
                for binding in runtime_contract.get("bindings", [])
                if isinstance(binding, Sequence)
                and not isinstance(binding, (str, bytes))
                and len(binding) == 2
            }
            if not participant_role_set <= candidate_binding_roles:
                invalid = True
            candidate_pixel_sets.append(
                {
                    str(item.get("kind"))
                    for item in runtime_contract.get("pixel_evidence", [])
                    if isinstance(item, Mapping)
                }
            )
            candidate_resource_sets.append(
                {
                    str(item[0])
                    for item in runtime_contract.get("resource_claims", [])
                    if isinstance(item, Sequence)
                    and not isinstance(item, (str, bytes))
                    and len(item) == 4
                }
            )
            candidate_profile_ids.setdefault(candidate_id, []).append(str(profile_id))
        if candidate_pixel_sets and owned_pixel_kinds is not None:
            owned = set(owned_pixel_kinds)
            if profile.get("quantifier") == "any":
                invalid = invalid or not all(owned <= kinds for kinds in candidate_pixel_sets)
            else:
                invalid = invalid or not owned <= set().union(*candidate_pixel_sets)
        if candidate_resource_sets and owned_resource_kinds is not None:
            owned = set(owned_resource_kinds)
            if profile.get("quantifier") == "any":
                invalid = invalid or not all(owned <= kinds for kinds in candidate_resource_sets)
            else:
                invalid = invalid or not owned <= set().union(*candidate_resource_sets)
        if invalid:
            failures.append(
                issue(
                    "universal_asset_binding",
                    "literal visual realization profile is not a closed unambiguous owned mapping",
                    profile_id=profile_id,
                    profile_index=index,
                )
            )
            continue
        profile_by_id[str(profile_id)] = profile
        seen_ranks.add(int(rank))

    ambiguous_candidates = {
        candidate_id: profile_ids
        for candidate_id, profile_ids in candidate_profile_ids.items()
        if len(profile_ids) != 1
    }
    if ambiguous_candidates:
        failures.append(
            issue(
                "universal_asset_binding",
                "literal realization candidates cannot use ambiguous last-match profile authority",
                candidates=ambiguous_candidates,
            )
        )
    if failures:
        return failures

    matched_bindings: dict[str, list[Mapping[str, Any]]] = {
        profile_id: bindings
        for profile_id, profile in profile_by_id.items()
        for bindings in (value_bindings(profile),)
        if bindings
    }
    matched_profile_by_candidate = {
        candidate_id: profile_id
        for profile_id, profile in matched_bindings.items()
        for candidate_id in (_string_list(profile_by_id[profile_id].get("candidate_group")) or [])
    }

    selected_event = _mapping(scene.get("selected_event"))
    selected_role_by_id = {
        str(role.get("role_id")): role
        for role in (
            selected_event.get("roles")
            if isinstance(selected_event.get("roles"), list)
            else []
        )
        if isinstance(role, Mapping) and _is_nonempty_string(role.get("role_id"))
    }
    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, dict)
    ]
    atom_by_candidate: dict[str, list[Mapping[str, Any]]] = {}
    for atom in atoms:
        atom_by_candidate.setdefault(str(atom.get("candidate_id")), []).append(atom)
    selected_ids: set[str] = set()
    provided_predicates: set[tuple[str, str, str]] = set()

    def predicate_truth(predicate: Sequence[str]) -> bool:
        return _audit_context_predicate_truth(
            predicate,
            scene=scene,
            assets=assets,
            matched_prop_ids=matched_prop_ids,
            selected_candidate_ids=selected_ids,
            provided_predicates=provided_predicates,
        )

    def candidate_eligible(candidate: Mapping[str, Any]) -> bool:
        if candidate.get("role") != "visual_atom":
            return False
        candidate_id = str(candidate.get("id"))
        facet = str(candidate.get("facet"))
        state = _audit_derived_facet_state(
            facet,
            contract=contract,
            actor_entity_id=_audit_participant_primary(scene, "actor") or "",
        )
        has_profile = candidate_id in matched_profile_by_candidate
        if state == "closed":
            return False
        if (
            facet == "perceived_affect"
            and _mapping(slot_by_id.get("expression")).get("state") == "fixed"
            and not has_profile
        ):
            return False
        if state == "fixed":
            fixed_prop_match = facet == "prop" and any(
                candidate_id
                in (
                    _string_list(_mapping(prop_by_id.get(prop_id)).get("affordance_candidate_ids"))
                    or []
                )
                for prop_id in matched_prop_ids
            )
            if not fixed_prop_match and not has_profile:
                return False
        triggers = [
            trigger
            for trigger in candidate.get("triggers", [])
            if isinstance(trigger, Sequence) and not isinstance(trigger, (str, bytes))
        ]
        unsatisfied = [trigger for trigger in triggers if not predicate_truth(trigger)]
        if unsatisfied and not (
            has_profile
            and all(
                len(trigger) == 3
                and trigger[0] == "slot"
                and trigger[2] in {"open", "open_or_fixed"}
                for trigger in unsatisfied
            )
        ):
            return False
        preconditions = candidate.get("preconditions")
        preconditions = preconditions if isinstance(preconditions, Mapping) else {}
        capabilities = candidate.get("capabilities")
        capabilities = capabilities if isinstance(capabilities, Mapping) else {}

        def predicate_set_passes(
            requires_all: Any, requires_any: Any, forbids_any: Any
        ) -> bool:
            all_items = requires_all if isinstance(requires_all, Sequence) else []
            any_groups = requires_any if isinstance(requires_any, Sequence) else []
            forbid_items = forbids_any if isinstance(forbids_any, Sequence) else []
            return (
                all(predicate_truth(item) for item in all_items)
                and all(
                    isinstance(group, Sequence)
                    and not isinstance(group, (str, bytes))
                    and any(predicate_truth(item) for item in group)
                    for group in any_groups
                )
                and not any(predicate_truth(item) for item in forbid_items)
            )

        return predicate_set_passes(
            preconditions.get("requires_all", []),
            preconditions.get("requires_any", []),
            preconditions.get("forbids_any", []),
        ) and predicate_set_passes(
            capabilities.get("requires_all", []),
            capabilities.get("requires_any", []),
            [],
        )

    expected_selected_candidates: dict[str, list[str]] = {}
    trace = _mapping(scene.get("selection_trace"))
    eligible_ids_by_facet = _mapping(trace.get("eligible_candidate_ids_by_facet"))
    for profile_id in sorted(
        matched_bindings,
        key=lambda item: (int(profile_by_id[item]["selection_rank"]), item),
    ):
        profile = profile_by_id[profile_id]
        candidate_ids = _string_list(profile.get("candidate_group")) or []
        eligible_ids = [
            candidate_id
            for candidate_id in candidate_ids
            if isinstance(candidate_by_id.get(candidate_id), Mapping)
            and candidate_eligible(candidate_by_id[candidate_id])
        ]
        eligibility_passes = (
            len(eligible_ids) == len(candidate_ids)
            if profile.get("quantifier") == "all"
            else bool(eligible_ids)
        )
        trace_eligible_ids = set(
            _string_list(eligible_ids_by_facet.get(str(profile.get("realized_facet"))))
            or []
        )
        trace_passes = (
            set(candidate_ids) <= trace_eligible_ids
            if profile.get("quantifier") == "all"
            else bool(set(candidate_ids) & trace_eligible_ids)
        )
        if not eligibility_passes or not trace_passes:
            failures.append(
                issue(
                    "universal_candidate_eligibility",
                    "matched literal realization group lacks its exact independently eligible candidate proof",
                    profile_id=profile_id,
                    eligible_candidate_ids=eligible_ids,
                    candidate_group=candidate_ids,
                )
            )
            continue
        selected_for_profile = (
            candidate_ids
            if profile.get("quantifier") == "all"
            else eligible_ids[:1]
        )
        if profile.get("enforcement") == "selected":
            expected_selected_candidates[profile_id] = selected_for_profile
            for candidate_id in selected_for_profile:
                selected_ids.add(candidate_id)
                candidate = candidate_by_id[candidate_id]
                provided_predicates.update(
                    tuple(str(value) for value in predicate)
                    for predicate in candidate.get("postconditions", [])
                    if isinstance(predicate, Sequence)
                    and not isinstance(predicate, (str, bytes))
                    and len(predicate) == 3
                )

    request_sha256 = hashlib.sha256(request_text.encode("utf-8")).hexdigest()
    actual_literal_atoms_by_profile: dict[str, list[Mapping[str, Any]]] = {}
    literal_atom_ids: set[str] = set()
    for atom in atoms:
        candidate_id = str(atom.get("candidate_id"))
        parameters = atom.get("parameters")
        parameters = parameters if isinstance(parameters, dict) else {}
        actual_profile_id = parameters.get("literal_realization_profile_id")
        expected_profile_id = matched_profile_by_candidate.get(candidate_id)
        if actual_profile_id is None and expected_profile_id is None:
            continue
        if actual_profile_id != expected_profile_id or expected_profile_id not in matched_bindings:
            failures.append(
                issue(
                    "universal_candidate_eligibility",
                    "selected literal candidate must bind its one exact active realization profile",
                    instance_id=atom.get("instance_id"),
                    candidate_id=candidate_id,
                    expected_profile_id=expected_profile_id,
                    actual_profile_id=actual_profile_id,
                )
            )
            continue
        profile = profile_by_id[expected_profile_id]
        expected_parameters = {
            "literal_realization_profile_id": expected_profile_id,
            "mechanism_class_id": str(profile.get("mechanism_class_id")),
            "source_slot_id": str(profile.get("source_slot_id")),
            "resolved_owner_refs": resolved_owner_refs(profile),
            "value_phrase_bindings": list(matched_bindings[expected_profile_id]),
            "request_text_sha256": request_sha256,
        }
        if set(parameters) != UNIVERSAL_LITERAL_REALIZATION_PARAMETER_KEYS or parameters != expected_parameters:
            failures.append(
                issue(
                    "universal_candidate_eligibility",
                    "literal realization atom parameters must exactly reproduce profile, owner, value, and request authority",
                    instance_id=atom.get("instance_id"),
                    profile_id=expected_profile_id,
                    expected=expected_parameters,
                    actual=parameters,
                )
            )
        actual_literal_atoms_by_profile.setdefault(expected_profile_id, []).append(atom)
        literal_atom_ids.add(str(atom.get("instance_id")))

    for profile_id, expected_candidate_ids in expected_selected_candidates.items():
        actual_atoms = actual_literal_atoms_by_profile.get(profile_id, [])
        actual_candidate_ids = [str(atom.get("candidate_id")) for atom in actual_atoms]
        if actual_candidate_ids != expected_candidate_ids:
            failures.append(
                issue(
                    "universal_candidate_eligibility",
                    "selected literal realization must satisfy its exact any/all candidate quantifier",
                    profile_id=profile_id,
                    expected_candidate_ids=expected_candidate_ids,
                    actual_candidate_ids=actual_candidate_ids,
                )
            )
    unexpected_profiles = sorted(
        set(actual_literal_atoms_by_profile) - set(matched_bindings)
    )
    if unexpected_profiles:
        failures.append(
            issue(
                "universal_candidate_eligibility",
                "unmatched literal realization profiles cannot be injected after selection",
                profile_ids=unexpected_profiles,
            )
        )

    resources = [
        claim
        for claim in (
            scene.get("resource_claims")
            if isinstance(scene.get("resource_claims"), list)
            else []
        )
        if isinstance(claim, dict)
    ]
    claim_by_id = {
        str(claim.get("claim_id")): claim
        for claim in resources
        if _is_nonempty_string(claim.get("claim_id"))
    }
    pixel_contract = _mapping(scene.get("pixel_evidence_contract"))
    pixel_by_id = {
        str(item.get("item_id")): item
        for item in (
            pixel_contract.get("items")
            if isinstance(pixel_contract.get("items"), list)
            else []
        )
        if isinstance(item, dict) and _is_nonempty_string(item.get("item_id"))
    }

    def expected_claim_rows(
        atom: Mapping[str, Any], candidate: Mapping[str, Any]
    ) -> list[tuple[str, str, int, str, str]]:
        parameters = atom.get("parameters")
        parameters = parameters if isinstance(parameters, dict) else {}
        owner_refs = parameters.get("resolved_owner_refs")
        owner_refs = owner_refs if isinstance(owner_refs, list) else []
        rows: list[tuple[str, str, int, str, str]] = []
        runtime_contract = candidate.get("runtime_contract")
        runtime_contract = runtime_contract if isinstance(runtime_contract, Mapping) else {}
        for raw_claim in runtime_contract.get("resource_claims", []):
            if (
                not isinstance(raw_claim, Sequence)
                or isinstance(raw_claim, (str, bytes))
                or len(raw_claim) != 4
            ):
                continue
            kind, owner_scope, amount, mode = raw_claim
            if owner_scope == "scene":
                owner_ids = ["scene"]
            else:
                owner_ids = [
                    str(ref.get("entity_id"))
                    for ref in owner_refs
                    if isinstance(ref, dict) and ref.get("role_id") == owner_scope
                ]
                if not owner_ids:
                    participant = participant_by_role.get(str(owner_scope), {})
                    primary = participant.get("primary_entity_id")
                    owner_ids = [
                        str(primary)
                        if _is_nonempty_string(primary)
                        else str(owner_scope)
                    ]
            rows.extend(
                (
                    str(kind),
                    owner_id,
                    int(amount),
                    str(mode),
                    str(atom.get("instance_id")),
                )
                for owner_id in owner_ids
            )
        return rows

    for profile_id, profile_atoms in actual_literal_atoms_by_profile.items():
        profile = profile_by_id[profile_id]
        actual_profile_pixel_kinds: set[str] = set()
        actual_profile_resource_kinds: set[str] = set()
        for atom in profile_atoms:
            instance_id = str(atom.get("instance_id"))
            candidate = candidate_by_id.get(str(atom.get("candidate_id")))
            if not isinstance(candidate, Mapping):
                continue
            runtime_contract = candidate.get("runtime_contract")
            runtime_contract = runtime_contract if isinstance(runtime_contract, Mapping) else {}
            expected_bindings: list[dict[str, str]] = []
            missing_required_roles: list[str] = []
            for raw_binding in runtime_contract.get("bindings", []):
                if (
                    not isinstance(raw_binding, Sequence)
                    or isinstance(raw_binding, (str, bytes))
                    or len(raw_binding) != 2
                ):
                    continue
                role_id, requirement = (str(raw_binding[0]), str(raw_binding[1]))
                selected_role = selected_role_by_id.get(role_id)
                if selected_role is None or not _is_nonempty_string(
                    selected_role.get("value_id")
                ):
                    if requirement in {"required", "event_spine"}:
                        missing_required_roles.append(role_id)
                    continue
                expected_bindings.append(
                    {
                        "role_id": role_id,
                        "node_id": str(selected_role["value_id"]),
                        "requirement": (
                            "required"
                            if requirement == "event_spine"
                            else requirement
                        ),
                    }
                )
            if missing_required_roles or atom.get("bindings") != expected_bindings:
                failures.append(
                    issue(
                        "universal_event_spine",
                        "literal realization atom bindings must exactly join its reviewed candidate to the final event roles",
                        profile_id=profile_id,
                        instance_id=instance_id,
                        missing_required_role_ids=missing_required_roles,
                        expected=expected_bindings,
                        actual=atom.get("bindings"),
                    )
                )
            expected_pixel_ids: list[str] = []
            for evidence in runtime_contract.get("pixel_evidence", []):
                if not isinstance(evidence, Mapping):
                    continue
                item_id = (
                    f"pixel_atom_{instance_id}_"
                    f"{str(evidence.get('id')).replace('::', '_')}"
                )
                expected_pixel_ids.append(item_id)
                expected_item = {
                    "item_id": item_id,
                    "source_kind": "atom",
                    "source_id": instance_id,
                    "kind": str(evidence.get("kind")),
                    "minimum_scale_ids": list(evidence.get("minimum_scale_ids", [])),
                    "status": "future_review_required",
                }
                actual_item = pixel_by_id.get(item_id)
                if actual_item != expected_item:
                    failures.append(
                        issue(
                            "universal_pixel_evidence",
                            "literal realization pixel proof must be owned by its exact selected candidate instance",
                            profile_id=profile_id,
                            instance_id=instance_id,
                            item_id=item_id,
                            expected=expected_item,
                            actual=actual_item,
                        )
                    )
                actual_profile_pixel_kinds.add(str(evidence.get("kind")))
            if atom.get("pixel_evidence_ids") != expected_pixel_ids:
                failures.append(
                    issue(
                        "universal_pixel_evidence",
                        "literal realization atom must expose exactly its own candidate pixel obligations",
                        profile_id=profile_id,
                        instance_id=instance_id,
                        expected=expected_pixel_ids,
                        actual=atom.get("pixel_evidence_ids"),
                    )
                )
            expected_rows = expected_claim_rows(atom, candidate)
            actual_rows = [
                (
                    str(claim.get("resource_kind")),
                    str(claim.get("owner_id")),
                    int(claim.get("amount", 0)),
                    str(claim.get("mode")),
                    str(claim.get("claimant_id")),
                )
                for claim_id in (_string_list(atom.get("resource_claim_ids")) or [])
                for claim in (claim_by_id.get(claim_id),)
                if isinstance(claim, dict)
            ]
            if actual_rows != expected_rows:
                failures.append(
                    issue(
                        "universal_resource_capacity",
                        "literal realization claims must bind exact candidate kinds to exact resolved participant owners",
                        profile_id=profile_id,
                        instance_id=instance_id,
                        expected=expected_rows,
                        actual=actual_rows,
                    )
                )
            actual_profile_resource_kinds.update(row[0] for row in actual_rows)
        if not set(_string_list(profile.get("owned_pixel_kinds")) or []) <= actual_profile_pixel_kinds:
            failures.append(
                issue(
                    "universal_pixel_evidence",
                    "literal realization owned pixel kinds must be supplied by its exact selected profile atoms",
                    profile_id=profile_id,
                    expected=profile.get("owned_pixel_kinds"),
                    actual=sorted(actual_profile_pixel_kinds),
                )
            )
        if not set(_string_list(profile.get("owned_resource_kinds")) or []) <= actual_profile_resource_kinds:
            failures.append(
                issue(
                    "universal_resource_capacity",
                    "literal realization owned resources must be claimed by its exact selected profile atoms and participants",
                    profile_id=profile_id,
                    expected=profile.get("owned_resource_kinds"),
                    actual=sorted(actual_profile_resource_kinds),
                )
            )

    if len(atoms) > UNIVERSAL_SELECTED_VISUAL_ATOM_MAX_TOTAL:
        failures.append(
            issue(
                "universal_candidate_eligibility",
                "selected atom count exceeds the pre-reserved literal-aware scene budget",
                maximum=UNIVERSAL_SELECTED_VISUAL_ATOM_MAX_TOTAL,
                actual=len(atoms),
            )
        )
    if len(literal_atom_ids) > UNIVERSAL_LITERAL_REALIZATION_MAX_TOTAL:
        failures.append(
            issue(
                "universal_candidate_eligibility",
                "literal realization atom count exceeds the closed scene budget",
                maximum=UNIVERSAL_LITERAL_REALIZATION_MAX_TOTAL,
                actual=len(literal_atom_ids),
            )
        )
    literal_facets = {
        str(atom.get("facet"))
        for atom in atoms
        if str(atom.get("instance_id")) in literal_atom_ids
    }
    for facet in literal_facets:
        facet_count = sum(atom.get("facet") == facet for atom in atoms)
        if facet_count > UNIVERSAL_LITERAL_REALIZATION_MAX_PER_FACET:
            failures.append(
                issue(
                    "universal_candidate_eligibility",
                    "literal realization pre-reservation exceeds the closed per-facet budget",
                    facet=facet,
                    maximum=UNIVERSAL_LITERAL_REALIZATION_MAX_PER_FACET,
                    actual=facet_count,
                )
            )
    if len(resources) > UNIVERSAL_SELECTED_RESOURCE_CLAIM_MAX_TOTAL:
        failures.append(
            issue(
                "universal_resource_capacity",
                "selected resource claims exceed the literal-aware scene budget",
                maximum=UNIVERSAL_SELECTED_RESOURCE_CLAIM_MAX_TOTAL,
                actual=len(resources),
            )
        )
    return failures


def _audit_proposal_trace_failures(
    scene: Mapping[str, Any], assets: Any
) -> list[dict[str, Any]]:
    """Recompute the complete creativity-invariant proposal partition."""

    raw_candidates = getattr(assets, "candidates", {})
    raw_profiles = (
        raw_candidates.get("proposal_profiles")
        if isinstance(raw_candidates, Mapping)
        else None
    )
    if not isinstance(raw_profiles, list) or len(raw_profiles) != 12:
        return [
            issue(
                "universal_asset_binding",
                "candidate asset must expose the closed twelve-profile proposal catalog",
                actual_count=len(raw_profiles) if isinstance(raw_profiles, list) else None,
            )
        ]
    contract = _mapping(scene.get("scene_contract"))
    slots = {
        str(slot.get("slot_id")): slot
        for slot in (
            contract.get("slot_states")
            if isinstance(contract.get("slot_states"), list)
            else []
        )
        if isinstance(slot, dict) and _is_nonempty_string(slot.get("slot_id"))
    }
    contract_roles = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, dict) and _is_nonempty_string(role.get("role_id"))
    }
    actor_primary = _audit_participant_primary(scene, "actor")
    actor_contract_role = _mapping(contract_roles.get("actor"))
    actor_value = (
        str(actor_contract_role.get("value_id"))
        if actor_contract_role.get("state") == "fixed"
        and _is_nonempty_string(actor_contract_role.get("value_id"))
        else actor_primary
    )
    initial_roles: dict[str, dict[str, Any]] = {}
    for role_id in UNIVERSAL_ROLE_IDS:
        role = _mapping(contract_roles.get(role_id))
        if role.get("state") == "fixed" and _is_nonempty_string(role.get("value_id")):
            initial_roles[role_id] = {
                "role_id": role_id,
                "value_id": str(role["value_id"]),
                "source": "user_fixed",
                "source_id": role_id,
            }
    if "actor" not in initial_roles and _is_nonempty_string(actor_value):
        initial_roles["actor"] = {
            "role_id": "actor",
            "value_id": str(actor_value),
            "source": "runtime_selected",
            "source_id": f"identity_entity:{actor_primary}",
        }
    matched_prop_ids = _audit_matched_catalog_prop_ids(scene, assets)

    def predicate_truth(predicate: Any) -> bool:
        if (
            not isinstance(predicate, Sequence)
            or isinstance(predicate, (str, bytes))
            or len(predicate) != 3
        ):
            return False
        kind, subject, value = (str(item) for item in predicate)
        if kind == "slot":
            state = _audit_derived_facet_state(
                subject,
                contract=contract,
                actor_entity_id=actor_primary or "",
            )
            return state == value or (
                value == "open_or_fixed" and state in {"open", "fixed"}
            )
        if kind == "event_role":
            if value in {"contract_fixed", "contract_open", "contract_closed"}:
                return _mapping(contract_roles.get(subject)).get("state") == value.removeprefix("contract_")
            if value == "present":
                return bool(_mapping(initial_roles.get(subject)).get("value_id"))
            if value == "explicit_none":
                return _mapping(contract_roles.get(subject)).get("state") == "closed"
            return _mapping(initial_roles.get(subject)).get("value_id") == value
        if kind == "capability" and subject == "actor":
            identity = _mapping(contract.get("identity_core"))
            actor = next(
                (
                    entity
                    for entity in identity.get("entities", [])
                    if isinstance(entity, dict)
                    and entity.get("entity_id") == actor_primary
                ),
                {},
            )
            available = {
                str(capability.get("id")): int(capability.get("capacity", 0))
                for capability in (
                    actor.get("capabilities")
                    if isinstance(actor, dict)
                    and isinstance(actor.get("capabilities"), list)
                    else []
                )
                if isinstance(capability, dict)
                and capability.get("state") == "available"
            }
            if value == "manipulator_or_equivalent":
                return any(
                    available.get(capability_id, 0) > 0
                    for capability_id in {
                        "manipulator", "mouth", "appendage", "wing_appendage",
                        "tail_axis", "body_orientation", "support_contact",
                        "external_anchor",
                    }
                )
            return available.get(value, 0) > 0
        if kind == "normalized_prop_concept":
            return value in matched_prop_ids
        if kind == "context":
            context = _mapping(contract.get("context_profile"))
            if subject == "identity_core":
                return value == "available"
            if subject == "social" and value == "dyad_or_ensemble":
                return context.get("social") in {"dyad", "ensemble"}
            if subject == "tool_state" and value == "safe_inactive":
                return context.get("violence") in {"closed", "nonviolent"}
            return context.get(subject) == value
        if kind == "policy":
            return subject == "local_default_metadata" and value == "automatic_pass"
        if kind == "cardinality" and subject == "actors" and value == "at_least_2":
            return sum(
                int(entity.get("quantity", 0))
                for entity in _mapping(contract.get("identity_core")).get("entities", [])
                if isinstance(entity, dict)
            ) >= 2
        return False

    def decision(profile: Mapping[str, Any]) -> tuple[bool, str]:
        prop_state = _audit_derived_facet_state(
            "prop", contract=contract, actor_entity_id=actor_primary or ""
        )
        action_state = _audit_derived_facet_state(
            "action", contract=contract, actor_entity_id=actor_primary or ""
        )
        if not (prop_state == "open" and action_state == "open"):
            return False, "proposal_path_not_open"
        slot_state = _audit_derived_facet_state(
            str(profile.get("slot_id")),
            contract=contract,
            actor_entity_id=actor_primary or "",
        )
        if slot_state not in (_string_list(profile.get("eligible_slot_states")) or []):
            return False, "slot_state_ineligible"
        if not all(predicate_truth(item) for item in profile.get("requires_all", [])):
            return False, "requires_all_unsatisfied"
        if any(predicate_truth(item) for item in profile.get("forbids_any", [])):
            return False, "forbidden_predicate_satisfied"
        if profile.get("policy_mode") == "explicit_weapon_only":
            return False, "policy_explicit_only"
        if (
            profile.get("policy_mode") == "safe_tool"
            and _mapping(contract.get("context_profile")).get("violence") == "active"
        ):
            return False, "policy_active_violence"
        resolved: dict[str, str] = {}
        event_roles = profile.get("event_roles")
        event_roles = event_roles if isinstance(event_roles, Mapping) else {}
        for role_id, proposed in event_roles.items():
            if proposed is None:
                continue
            value = str(proposed)
            if proposed == "$identity_actor":
                value = str(actor_value) if _is_nonempty_string(actor_value) else ""
            elif proposed == "$scene_location":
                location = _mapping(contract_roles.get("location"))
                if location.get("state") == "fixed" and _is_nonempty_string(location.get("value_id")):
                    value = str(location["value_id"])
                else:
                    environment = _mapping(slots.get("environment"))
                    environment_values = _string_list(environment.get("value_ids")) or []
                    value = environment_values[0] if environment.get("state") == "fixed" and environment_values else ""
            if value:
                resolved[str(role_id)] = value
        if any(
            isinstance(existing := initial_roles.get(role_id), dict)
            and existing.get("source") == "user_fixed"
            and existing.get("value_id") != proposed
            for role_id, proposed in resolved.items()
        ):
            return False, "fixed_role_conflict"
        if any(
            _mapping(contract_roles.get(role_id)).get("state") == "closed"
            for role_id in resolved
        ):
            return False, "closed_role_conflict"
        return True, "eligible"

    profile_by_id: dict[str, Mapping[str, Any]] = {}
    expected_eligible_ids: list[str] = []
    expected_rejections: list[dict[str, str]] = []
    for profile in raw_profiles:
        if not isinstance(profile, Mapping) or not _is_nonempty_string(profile.get("id")):
            return [
                issue(
                    "universal_asset_binding",
                    "proposal catalog contains an untyped profile",
                )
            ]
        profile_id = str(profile["id"])
        if profile_id in profile_by_id:
            return [
                issue(
                    "universal_asset_binding",
                    "proposal profile IDs must be unique",
                    proposal_id=profile_id,
                )
            ]
        profile_by_id[profile_id] = profile
        eligible, reason = decision(profile)
        if eligible:
            expected_eligible_ids.append(profile_id)
        else:
            expected_rejections.append(
                {"proposal_id": profile_id, "reason_code": reason}
            )
    expected_eligible_ids.sort()
    expected_rejections.sort(key=lambda item: item["proposal_id"].encode("utf-8"))
    expected_family_ids = sorted(
        str(profile_by_id[profile_id].get("semantic_family_id"))
        for profile_id in expected_eligible_ids
    )
    expected_band_counts = {
        band: sum(
            _universal_distance_band(
                profile_by_id[profile_id].get("distance_profile", {})
            )
            == band
            for profile_id in expected_eligible_ids
        )
        for band in ("near", "middle", "far")
    }
    reason_ids = (
        "proposal_path_not_open",
        "slot_state_ineligible",
        "requires_all_unsatisfied",
        "forbidden_predicate_satisfied",
        "policy_explicit_only",
        "policy_active_violence",
        "fixed_role_conflict",
        "closed_role_conflict",
    )
    expected_rejection_counts = {
        reason: sum(item["reason_code"] == reason for item in expected_rejections)
        for reason in reason_ids
        if any(item["reason_code"] == reason for item in expected_rejections)
    }
    trace = _mapping(scene.get("selection_trace"))
    expected_fields = {
        "eligible_proposal_profile_ids": expected_eligible_ids,
        "proposal_rejections": expected_rejections,
        "eligible_proposal_family_ids": expected_family_ids,
        "eligible_proposal_count_by_band": expected_band_counts,
        "proposal_rejection_count_by_code": expected_rejection_counts,
    }
    actual_fields = {key: trace.get(key) for key in expected_fields}
    if actual_fields != expected_fields:
        return [
            issue(
                "universal_candidate_eligibility",
                "proposal trace must exactly equal the raw-profile first-failure decision partition and projections",
                mismatched_fields=sorted(
                    key for key in expected_fields if actual_fields[key] != expected_fields[key]
                ),
                expected=expected_fields,
                actual=actual_fields,
            )
        ]
    return []


def _audit_initial_event_roles(scene: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    contract = _mapping(scene.get("scene_contract"))
    roles: dict[str, dict[str, Any]] = {}
    for role in (
        contract.get("event_roles")
        if isinstance(contract.get("event_roles"), list)
        else []
    ):
        if not isinstance(role, Mapping) or role.get("state") != "fixed":
            continue
        role_id = str(role.get("role_id"))
        roles[role_id] = {
            "role_id": role_id,
            "value_id": str(role.get("value_id")),
            "source": "user_fixed",
            "source_id": role_id,
        }
    if "actor" not in roles:
        actor_id = _audit_participant_primary(scene, "actor")
        if actor_id is not None:
            roles["actor"] = {
                "role_id": "actor",
                "value_id": actor_id,
                "source": "runtime_selected",
                "source_id": f"identity_entity:{actor_id}",
            }
    return roles


def _audit_proposal_invariant_partition(
    scene: Mapping[str, Any], assets: Any
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Derive the proposal pool before creativity, seed, rank, or feasibility."""

    raw_candidates = getattr(assets, "candidates", {})
    raw_profiles = (
        raw_candidates.get("proposal_profiles", [])
        if isinstance(raw_candidates, Mapping)
        else []
    )
    if not isinstance(raw_profiles, Sequence) or isinstance(
        raw_profiles, (str, bytes)
    ):
        raise ValueError("proposal catalog is not a typed sequence")
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    contract = _mapping(scene.get("scene_contract"))
    contract_roles = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, Mapping) and _is_nonempty_string(role.get("role_id"))
    }
    slots = {
        str(slot.get("slot_id")): slot
        for slot in (
            contract.get("slot_states")
            if isinstance(contract.get("slot_states"), list)
            else []
        )
        if isinstance(slot, Mapping) and _is_nonempty_string(slot.get("slot_id"))
    }
    actor_primary = _audit_participant_primary(scene, "actor")
    initial_roles = _audit_initial_event_roles(scene)
    actor_value = _mapping(initial_roles.get("actor")).get("value_id")
    matched_prop_ids = _audit_matched_catalog_prop_ids(scene, assets)
    mandatory_candidate_ids = {
        str(atom.get("candidate_id"))
        for atom in (
            scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
        )
        if isinstance(atom, Mapping)
        and _is_nonempty_string(
            _mapping(atom.get("parameters")).get("literal_realization_profile_id")
        )
    }

    def predicate_truth(predicate: Any) -> bool:
        if (
            not isinstance(predicate, Sequence)
            or isinstance(predicate, (str, bytes))
            or len(predicate) != 3
        ):
            return False
        kind, subject, value = (str(item) for item in predicate)
        if kind == "slot":
            state = _audit_derived_facet_state(
                subject,
                contract=contract,
                actor_entity_id=actor_primary or "",
            )
            return state == value or (
                value == "open_or_fixed" and state in {"open", "fixed"}
            )
        if kind == "event_role":
            contract_role = _mapping(contract_roles.get(subject))
            if value in {"contract_fixed", "contract_open", "contract_closed"}:
                return contract_role.get("state") == value.removeprefix("contract_")
            if value == "present":
                return bool(_mapping(initial_roles.get(subject)).get("value_id"))
            if value == "explicit_none":
                return contract_role.get("state") == "closed"
            return _mapping(initial_roles.get(subject)).get("value_id") == value
        if kind == "capability" and subject == "actor":
            actor = next(
                (
                    entity
                    for entity in _mapping(contract.get("identity_core")).get(
                        "entities", []
                    )
                    if isinstance(entity, Mapping)
                    and entity.get("entity_id") == actor_primary
                ),
                {},
            )
            available = {
                str(capability.get("id")): int(capability.get("capacity", 0))
                for capability in (
                    actor.get("capabilities", [])
                    if isinstance(actor, Mapping)
                    and isinstance(actor.get("capabilities"), list)
                    else []
                )
                if isinstance(capability, Mapping)
                and capability.get("state") == "available"
            }
            if value == "manipulator_or_equivalent":
                return any(
                    available.get(capability_id, 0) > 0
                    for capability_id in {
                        "manipulator",
                        "mouth",
                        "appendage",
                        "wing_appendage",
                        "tail_axis",
                        "body_orientation",
                        "support_contact",
                        "external_anchor",
                    }
                )
            return available.get(value, 0) > 0
        if kind == "normalized_prop_concept":
            return value in matched_prop_ids
        if kind == "context":
            context = _mapping(contract.get("context_profile"))
            if subject == "identity_core":
                return value == "available"
            if subject == "social" and value == "dyad_or_ensemble":
                return context.get("social") in {"dyad", "ensemble"}
            if subject == "tool_state" and value == "safe_inactive":
                return context.get("violence") in {"closed", "nonviolent"}
            return context.get(subject) == value
        if kind == "policy":
            return subject == "local_default_metadata" and value == "automatic_pass"
        if kind == "cardinality" and subject == "actors" and value == "at_least_2":
            return (
                sum(
                    int(entity.get("quantity", 0))
                    for entity in _mapping(contract.get("identity_core")).get(
                        "entities", []
                    )
                    if isinstance(entity, Mapping)
                )
                >= 2
            )
        return False

    def proposal_decision(profile: Mapping[str, Any]) -> tuple[bool, str]:
        if not (
            _audit_derived_facet_state(
                "prop", contract=contract, actor_entity_id=actor_primary or ""
            )
            == "open"
            and _audit_derived_facet_state(
                "action", contract=contract, actor_entity_id=actor_primary or ""
            )
            == "open"
        ):
            return False, "proposal_path_not_open"
        slot_state = _audit_derived_facet_state(
            str(profile.get("slot_id")),
            contract=contract,
            actor_entity_id=actor_primary or "",
        )
        if slot_state not in (_string_list(profile.get("eligible_slot_states")) or []):
            return False, "slot_state_ineligible"
        if not all(predicate_truth(item) for item in profile.get("requires_all", [])):
            return False, "requires_all_unsatisfied"
        if any(predicate_truth(item) for item in profile.get("forbids_any", [])):
            return False, "forbidden_predicate_satisfied"
        candidate_ids = _string_list(profile.get("candidate_ids")) or []
        if candidate_ids and candidate_ids[0] in mandatory_candidate_ids:
            return False, "precondition_unsatisfied"
        if profile.get("policy_mode") == "explicit_weapon_only":
            return False, "policy_explicit_only"
        if (
            profile.get("policy_mode") == "safe_tool"
            and _mapping(contract.get("context_profile")).get("violence") == "active"
        ):
            return False, "policy_active_violence"
        resolved: dict[str, str] = {}
        event_roles = (
            profile.get("event_roles")
            if isinstance(profile.get("event_roles"), Mapping)
            else {}
        )
        for role_id, proposed in event_roles.items():
            if proposed is None:
                continue
            resolved_value = str(proposed)
            if proposed == "$identity_actor":
                resolved_value = str(actor_value) if _is_nonempty_string(actor_value) else ""
            elif proposed == "$scene_location":
                location = _mapping(contract_roles.get("location"))
                if location.get("state") == "fixed" and _is_nonempty_string(
                    location.get("value_id")
                ):
                    resolved_value = str(location.get("value_id"))
                else:
                    environment = _mapping(slots.get("environment"))
                    values = _string_list(environment.get("value_ids")) or []
                    resolved_value = (
                        values[0]
                        if environment.get("state") == "fixed" and values
                        else ""
                    )
            if resolved_value:
                resolved[str(role_id)] = resolved_value
        if any(
            _mapping(initial_roles.get(role_id)).get("source") == "user_fixed"
            and _mapping(initial_roles.get(role_id)).get("value_id") != proposed
            for role_id, proposed in resolved.items()
        ):
            return False, "fixed_role_conflict"
        if any(
            _mapping(contract_roles.get(role_id)).get("state") == "closed"
            for role_id in resolved
        ):
            return False, "closed_role_conflict"
        return True, "eligible"

    eligible_rows: list[dict[str, Any]] = []
    rejected_rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for raw_profile in raw_profiles:
        if not isinstance(raw_profile, Mapping) or not _is_nonempty_string(
            raw_profile.get("id")
        ):
            raise ValueError("proposal catalog contains an untyped profile")
        profile = dict(raw_profile)
        profile_id = str(profile.get("id"))
        if profile_id in seen_ids:
            raise ValueError(f"duplicate proposal profile {profile_id}")
        seen_ids.add(profile_id)
        expected_payload = _audit_proposal_semantic_family_payload(
            profile, candidate_by_id
        )
        expected_signature = _audit_canonical_sha256(expected_payload)
        if profile.get("semantic_family_payload") != expected_payload:
            raise ValueError(
                f"proposal {profile_id} semantic family payload is not source-derived"
            )
        if profile.get("semantic_family_signature") != expected_signature:
            raise ValueError(
                f"proposal {profile_id} semantic family signature is not canonical"
            )
        eligible, reason = proposal_decision(profile)
        if eligible:
            eligible_rows.append(
                {
                    "record_id": profile_id,
                    "semantic_signature": expected_signature,
                    "distance_band": _universal_distance_band(
                        profile.get("distance_profile", {})
                    ),
                }
            )
        else:
            rejected_rows.append(
                {
                    "record_id": profile_id,
                    "outcome": "rejected",
                    "reason_codes": [reason],
                }
            )
    eligible_rows.sort(key=lambda row: str(row["record_id"]).encode("utf-8"))
    rejected_rows.sort(key=lambda row: str(row["record_id"]).encode("utf-8"))
    return eligible_rows, rejected_rows


def _audit_candidate_invariant_partition(
    scene: Mapping[str, Any], assets: Any
) -> tuple[list[str], list[dict[str, Any]]]:
    """Recompute the visual pool without proposal, creativity, seed, or rank state."""

    contract = _mapping(scene.get("scene_contract"))
    contract_roles = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, Mapping)
    }
    initial_roles = _audit_initial_event_roles(scene)
    actor_entity_id = _audit_participant_primary(scene, "actor") or ""
    matched_prop_ids = _audit_matched_catalog_prop_ids(scene, assets)
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    prop_by_id = getattr(assets, "prop_by_id", {})
    atoms = [
        atom
        for atom in (
            scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
        )
        if isinstance(atom, Mapping)
    ]
    mandatory_candidate_ids = {
        str(atom.get("candidate_id"))
        for atom in atoms
        if _is_nonempty_string(
            _mapping(atom.get("parameters")).get("literal_realization_profile_id")
        )
    }
    provided_predicates = {
        tuple(str(value) for value in predicate)
        for candidate_id in mandatory_candidate_ids
        for candidate in (
            _mapping(
                candidate_by_id.get(candidate_id)
                if isinstance(candidate_by_id, Mapping)
                else None
            ),
        )
        for predicate in candidate.get("postconditions", [])
        if isinstance(predicate, Sequence)
        and not isinstance(predicate, (str, bytes))
        and len(predicate) == 3
    }

    catalog_owners: dict[str, set[str]] = {}
    for prop_id, prop in (
        prop_by_id.items() if isinstance(prop_by_id, Mapping) else []
    ):
        for candidate_id in _string_list(_mapping(prop).get("affordance_candidate_ids")) or []:
            catalog_owners.setdefault(candidate_id, set()).add(str(prop_id))

    def predicate_truth(
        predicate: Sequence[str], roles: Mapping[str, Mapping[str, Any]]
    ) -> bool:
        if len(predicate) != 3:
            return False
        kind, subject, value = (str(item) for item in predicate)
        if kind == "event_role":
            contract_role = _mapping(contract_roles.get(subject))
            if value in {"contract_fixed", "contract_open", "contract_closed"}:
                return contract_role.get("state") == value.removeprefix("contract_")
            if value == "present":
                return bool(_mapping(roles.get(subject)).get("value_id"))
            if value == "explicit_none":
                return contract_role.get("state") == "closed"
            return _mapping(roles.get(subject)).get("value_id") == value
        if kind == "candidate":
            if (subject, value) == ("selected", "true"):
                return bool(mandatory_candidate_ids)
            return subject in mandatory_candidate_ids and value == "selected"
        if kind == "facet_evidence":
            return (kind, subject, value) in provided_predicates
        if kind == "candidate_tag" or kind in {"axis_max", "axis_sum"}:
            return False
        return _audit_context_predicate_truth(
            predicate,
            scene=scene,
            assets=assets,
            matched_prop_ids=matched_prop_ids,
            selected_candidate_ids=mandatory_candidate_ids,
            provided_predicates=provided_predicates,
        )

    def predicate_set_passes(
        requires_all: Any,
        requires_any: Any,
        forbids_any: Any,
        roles: Mapping[str, Mapping[str, Any]],
    ) -> bool:
        all_items = requires_all if isinstance(requires_all, Sequence) else []
        any_groups = requires_any if isinstance(requires_any, Sequence) else []
        forbidden = forbids_any if isinstance(forbids_any, Sequence) else []
        return (
            all(predicate_truth(item, roles) for item in all_items)
            and all(
                isinstance(group, Sequence)
                and not isinstance(group, (str, bytes))
                and any(predicate_truth(item, roles) for item in group)
                for group in any_groups
            )
            and not any(predicate_truth(item, roles) for item in forbidden)
        )

    eligible_ids: list[str] = []
    rejected: list[dict[str, Any]] = []
    for candidate_id in _audit_utf8_sorted(
        candidate_id
        for candidate_id, candidate in (
            candidate_by_id.items() if isinstance(candidate_by_id, Mapping) else []
        )
        if isinstance(candidate, Mapping) and candidate.get("role") == "visual_atom"
    ):
        candidate = _mapping(candidate_by_id.get(candidate_id))
        facet = str(candidate.get("facet"))
        state = _audit_derived_facet_state(
            facet, contract=contract, actor_entity_id=actor_entity_id
        )
        has_literal_authority = candidate_id in mandatory_candidate_ids
        reason: str | None = None
        if state == "closed":
            reason = "closed_facet"
        elif (
            facet == "perceived_affect"
            and _mapping(
                next(
                    (
                        slot
                        for slot in contract.get("slot_states", [])
                        if isinstance(slot, Mapping)
                        and slot.get("slot_id") == "expression"
                    ),
                    {},
                )
            ).get("state")
            == "fixed"
            and not has_literal_authority
        ):
            reason = "fixed_facet_conflict"
        elif state == "fixed":
            owner_ids = catalog_owners.get(candidate_id, set())
            fixed_prop_match = facet == "prop" and (
                bool(owner_ids & matched_prop_ids) or not owner_ids
            )
            if not fixed_prop_match and not has_literal_authority:
                reason = "fixed_facet_conflict"

        predicate_roles = initial_roles
        runtime_contract = _mapping(candidate.get("runtime_contract"))
        raw_bindings = runtime_contract.get("bindings")
        if (
            reason is None
            and facet == "phase"
            and "phase" not in initial_roles
            and _mapping(contract_roles.get("phase")).get("state") == "open"
            and ["phase", "required"]
            in (raw_bindings if isinstance(raw_bindings, list) else [])
        ):
            predicate_roles = {
                **initial_roles,
                "phase": {
                    "role_id": "phase",
                    "value_id": candidate_id,
                    "source": "runtime_selected",
                    "source_id": f"candidate:{candidate_id}",
                },
            }
        if reason is None:
            unsatisfied = [
                item
                for item in candidate.get("triggers", [])
                if not predicate_truth(item, predicate_roles)
            ]
            if unsatisfied and not (
                has_literal_authority
                and all(
                    isinstance(item, Sequence)
                    and len(item) == 3
                    and item[0] == "slot"
                    and item[2] in {"open", "open_or_fixed"}
                    for item in unsatisfied
                )
            ):
                reason = "trigger_unsatisfied"
        if reason is None:
            preconditions = _mapping(candidate.get("preconditions"))
            if not predicate_set_passes(
                preconditions.get("requires_all", []),
                preconditions.get("requires_any", []),
                preconditions.get("forbids_any", []),
                predicate_roles,
            ):
                reason = "precondition_unsatisfied"
        if reason is None:
            capabilities = _mapping(candidate.get("capabilities"))
            if not predicate_set_passes(
                capabilities.get("requires_all", []),
                capabilities.get("requires_any", []),
                [],
                predicate_roles,
            ):
                reason = "capability_unsatisfied"
        if reason is None:
            eligible_ids.append(candidate_id)
        else:
            rejected.append(
                {
                    "record_id": candidate_id,
                    "outcome": "rejected",
                    "reason_codes": [reason],
                }
            )
    return eligible_ids, rejected


def _audit_owner_scope_hash(scene_contract_sha256: str, owner_scope: str) -> str:
    return _audit_canonical_sha256(
        {
            "schema": "illustration-universal-scene-capacity-owner/v1",
            "scene_contract_sha256": scene_contract_sha256,
            "owner_scope": owner_scope,
        }
    )


def _audit_resource_capacity_projection(
    scene: Mapping[str, Any], scene_contract_sha256: str
) -> tuple[list[dict[str, Any]], dict[tuple[str, str], int]]:
    contract = _mapping(scene.get("scene_contract"))
    identity = _mapping(contract.get("identity_core"))
    owners: dict[str, dict[str, int]] = {}
    for entity in (
        identity.get("entities")
        if isinstance(identity.get("entities"), list)
        else []
    ):
        if not isinstance(entity, Mapping) or not _is_nonempty_string(
            entity.get("entity_id")
        ):
            continue
        entity_id = str(entity.get("entity_id"))
        owners[entity_id] = {
            str(capability.get("id")): int(capability.get("capacity", 0))
            for capability in (
                entity.get("capabilities")
                if isinstance(entity.get("capabilities"), list)
                else []
            )
            if isinstance(capability, Mapping)
            and str(capability.get("id")) in UNIVERSAL_ENTITY_RESOURCE_KINDS
            and isinstance(capability.get("capacity"), int)
            and not isinstance(capability.get("capacity"), bool)
        }
    for binding in (
        contract.get("participant_bindings")
        if isinstance(contract.get("participant_bindings"), list)
        else []
    ):
        if (
            isinstance(binding, Mapping)
            and _is_nonempty_string(binding.get("role_id"))
            and binding.get("primary_entity_id") is None
        ):
            owners.setdefault(str(binding.get("role_id")), {})

    rows: list[dict[str, Any]] = []
    capacity_by_owner_kind: dict[tuple[str, str], int] = {}
    for owner_scope, declared in owners.items():
        owner_hash = _audit_owner_scope_hash(scene_contract_sha256, owner_scope)
        for resource_kind in _audit_utf8_sorted(UNIVERSAL_ENTITY_RESOURCE_KINDS):
            capacity = int(declared.get(resource_kind, 0))
            capacity_by_owner_kind[(owner_scope, resource_kind)] = capacity
            rows.append(
                {
                    "owner_scope_hash": owner_hash,
                    "resource_kind": resource_kind,
                    "capacity": capacity,
                    "state": "unavailable" if capacity == 0 else "available",
                }
            )
    scene_owner_hash = _audit_owner_scope_hash(scene_contract_sha256, "scene")
    for resource_kind in _audit_utf8_sorted(UNIVERSAL_SCENE_RESOURCE_CAPACITIES):
        capacity = int(UNIVERSAL_SCENE_RESOURCE_CAPACITIES[resource_kind])
        capacity_by_owner_kind[("scene", resource_kind)] = capacity
        rows.append(
            {
                "owner_scope_hash": scene_owner_hash,
                "resource_kind": resource_kind,
                "capacity": capacity,
                "state": "available",
            }
        )
    rows.sort(
        key=lambda row: (
            str(row["owner_scope_hash"]).encode("utf-8"),
            str(row["resource_kind"]).encode("utf-8"),
        )
    )
    return rows, capacity_by_owner_kind


def _audit_candidate_default_parameters(candidate: Mapping[str, Any]) -> dict[str, str]:
    raw_parameters = candidate.get("parameters")
    raw_parameters = raw_parameters if isinstance(raw_parameters, Mapping) else {}
    result: dict[str, str] = {}
    for parameter_id, values in sorted(raw_parameters.items()):
        alternatives = _string_list(values) or []
        if alternatives:
            result[str(parameter_id)] = _audit_utf8_sorted(alternatives)[0]
    return result


def _audit_resolved_trial_claims(
    entries: Sequence[Mapping[str, Any]],
    *,
    scene: Mapping[str, Any],
    scene_contract_sha256: str,
) -> list[dict[str, Any]]:
    contract = _mapping(scene.get("scene_contract"))
    participant_by_role = {
        str(binding.get("role_id")): binding
        for binding in (
            contract.get("participant_bindings")
            if isinstance(contract.get("participant_bindings"), list)
            else []
        )
        if isinstance(binding, Mapping)
    }
    rows: list[dict[str, Any]] = []
    for entry in entries:
        candidate = entry.get("candidate")
        candidate = candidate if isinstance(candidate, Mapping) else {}
        parameters = entry.get("parameters")
        parameters = parameters if isinstance(parameters, Mapping) else {}
        owner_refs = (
            parameters.get("resolved_owner_refs")
            if isinstance(parameters.get("resolved_owner_refs"), list)
            else []
        )
        runtime_contract = candidate.get("runtime_contract")
        runtime_contract = (
            runtime_contract if isinstance(runtime_contract, Mapping) else {}
        )
        for raw_claim_ordinal, raw_claim in enumerate(
            runtime_contract.get("resource_claims", [])
        ):
            if (
                not isinstance(raw_claim, Sequence)
                or isinstance(raw_claim, (str, bytes))
                or len(raw_claim) != 4
            ):
                raise ValueError("preselection trial contains malformed resource claim")
            resource_kind, owner_scope, amount, mode = raw_claim
            if owner_scope == "scene":
                owner_ids = ["scene"]
            else:
                owner_ids = _audit_utf8_sorted(
                    str(ref.get("entity_id"))
                    for ref in owner_refs
                    if isinstance(ref, Mapping)
                    and ref.get("role_id") == owner_scope
                    and _is_nonempty_string(ref.get("entity_id"))
                )
                if not owner_ids:
                    participant = _mapping(participant_by_role.get(str(owner_scope)))
                    primary = participant.get("primary_entity_id")
                    owner_ids = [
                        str(primary)
                        if _is_nonempty_string(primary)
                        else str(owner_scope)
                    ]
            for resolved_owner_ordinal, owner_id in enumerate(owner_ids):
                rows.append(
                    {
                        "entry_ordinal": int(entry["entry_ordinal"]),
                        "raw_claim_ordinal": raw_claim_ordinal,
                        "resolved_owner_ordinal": resolved_owner_ordinal,
                        "owner_scope_hash": _audit_owner_scope_hash(
                            scene_contract_sha256, owner_id
                        ),
                        "resource_kind": str(resource_kind),
                        "amount": int(amount),
                        "mode": str(mode),
                    }
                )
    rows.sort(
        key=lambda row: (
            int(row["entry_ordinal"]),
            int(row["raw_claim_ordinal"]),
            int(row["resolved_owner_ordinal"]),
        )
    )
    return rows


def _audit_preselection_trial(
    record_id: str,
    source_kind: str,
    source_id: str | None,
    *,
    scene: Mapping[str, Any],
    assets: Any,
    semantic_bindings: Mapping[str, Any],
    scene_contract_sha256: str,
) -> tuple[dict[str, Any], Any]:
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    atoms = [
        atom
        for atom in (
            scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
        )
        if isinstance(atom, Mapping)
        and _is_nonempty_string(
            _mapping(atom.get("parameters")).get("literal_realization_profile_id")
        )
    ]
    mandatory_internal: list[dict[str, Any]] = []
    active_profile_ids: set[str] = set()
    for atom in atoms:
        parameters = _mapping(atom.get("parameters"))
        profile_id = str(parameters.get("literal_realization_profile_id"))
        active_profile_ids.add(profile_id)
        candidate_id = str(atom.get("candidate_id"))
        candidate = (
            candidate_by_id.get(candidate_id)
            if isinstance(candidate_by_id, Mapping)
            else None
        )
        if not isinstance(candidate, Mapping):
            raise ValueError(f"mandatory literal candidate {candidate_id} is absent")
        mandatory_internal.append(
            {
                "source_kind": "mandatory_literal",
                "source_id": candidate_id,
                "candidate_id": candidate_id,
                "literal_realization_profile_ids": [profile_id],
                "parameters": _audit_plain_json(parameters),
                "candidate": candidate,
            }
        )
    mandatory_internal.sort(
        key=lambda entry: (
            str(entry["candidate_id"]).encode("utf-8"),
            tuple(entry["literal_realization_profile_ids"]),
            _audit_canonical_sha256(entry["parameters"]),
        )
    )
    internal_entries = list(mandatory_internal)
    source_record: Any
    if source_kind == "mandatory_literal":
        profile_by_id = {
            str(profile.get("id")): profile
            for profile in semantic_bindings.get(
                "literal_visual_realization_profiles", []
            )
            if isinstance(profile, Mapping)
        }
        source_record = [
            _audit_plain_json(profile_by_id[profile_id])
            for profile_id in _audit_utf8_sorted(active_profile_ids)
        ]
    elif source_kind == "proposal":
        raw_candidates = getattr(assets, "candidates", {})
        profiles = (
            raw_candidates.get("proposal_profiles", [])
            if isinstance(raw_candidates, Mapping)
            else []
        )
        profile = next(
            (
                item
                for item in profiles
                if isinstance(item, Mapping) and item.get("id") == source_id
            ),
            None,
        )
        if not isinstance(profile, Mapping):
            raise ValueError(f"unknown proposal trial source {source_id}")
        source_record = _audit_plain_json(profile)
        candidate_id = str((_string_list(profile.get("candidate_ids")) or [""])[0])
        if candidate_id not in {entry["candidate_id"] for entry in internal_entries}:
            candidate = candidate_by_id.get(candidate_id)
            if not isinstance(candidate, Mapping):
                raise ValueError(f"proposal primary candidate {candidate_id} is absent")
            internal_entries.append(
                {
                    "source_kind": "proposal",
                    "source_id": str(source_id),
                    "candidate_id": candidate_id,
                    "literal_realization_profile_ids": [],
                    "parameters": {
                        "proposal_id": str(profile.get("id")),
                        "value_id": str(profile.get("value_id")),
                        "prompt_phrase_en": str(profile.get("prompt_phrase_en")),
                    },
                    "candidate": candidate,
                }
            )
    elif source_kind == "visual_candidate":
        candidate = candidate_by_id.get(str(source_id))
        if not isinstance(candidate, Mapping):
            raise ValueError(f"unknown visual trial source {source_id}")
        source_record = _audit_plain_json(candidate)
        candidate_id = str(source_id)
        if candidate_id not in {entry["candidate_id"] for entry in internal_entries}:
            internal_entries.append(
                {
                    "source_kind": "visual_candidate",
                    "source_id": candidate_id,
                    "candidate_id": candidate_id,
                    "literal_realization_profile_ids": [],
                    "parameters": _audit_candidate_default_parameters(candidate),
                    "candidate": candidate,
                }
            )
    else:
        raise ValueError(f"unknown preselection source kind {source_kind}")

    entries: list[dict[str, Any]] = []
    for ordinal, internal in enumerate(internal_entries):
        internal["entry_ordinal"] = ordinal
        entries.append(
            {
                "entry_ordinal": ordinal,
                "source_kind": str(internal["source_kind"]),
                "source_id": str(internal["source_id"]),
                "candidate_id": str(internal["candidate_id"]),
                "literal_realization_profile_ids": list(
                    internal["literal_realization_profile_ids"]
                ),
                "parameters_sha256": _audit_canonical_sha256(
                    internal["parameters"]
                ),
            }
        )
    claims = _audit_resolved_trial_claims(
        internal_entries,
        scene=scene,
        scene_contract_sha256=scene_contract_sha256,
    )
    literal_facets = {
        str(entry["candidate"].get("facet")) for entry in mandatory_internal
    }
    facet_counts = [
        {
            "facet_id": facet,
            "count": sum(
                str(entry["candidate"].get("facet")) == facet
                for entry in internal_entries
            ),
        }
        for facet in _audit_utf8_sorted(literal_facets)
    ]
    trial = {
        "schema": UNIVERSAL_PRESELECTION_TRIAL_SCHEMA,
        "record_id": record_id,
        "entries": entries,
        "resolved_claims": claims,
        "literal_facet_counts": facet_counts,
        "literal_total": len(mandatory_internal),
    }
    return trial, source_record


def _audit_cardinality_limit_projection(
    compatibility: Mapping[str, Any],
) -> list[dict[str, Any]]:
    facet_scope = {
        "primary_actions": "action",
        "phases": "phase",
        "pose_support_solutions": "pose",
        "perceived_affect_hypotheses": "perceived_affect",
        "gestures": "gesture",
        "optional_props": "prop",
        "relation_topologies": "relation",
        "primary_environment_roles": "environment",
    }
    rows: list[dict[str, Any]] = []
    budgets = compatibility.get("budgets")
    budgets = budgets if isinstance(budgets, Mapping) else {}
    for metric_id, maximum in budgets.items():
        if metric_id in facet_scope:
            scope_kind, scope_id = "facet", facet_scope[str(metric_id)]
        elif metric_id in {"display_bundles", "display_primitives_per_bundle"}:
            scope_kind, scope_id = "bundle", "display"
        elif metric_id in {
            "remote_or_high_load_optional_premises",
            "second_independent_premises",
        }:
            scope_kind = "global"
            scope_id = (
                "optional_remote"
                if metric_id == "remote_or_high_load_optional_premises"
                else "independent_premise"
            )
        else:
            scope_kind, scope_id = "scene", "event_graph"
        rows.append(
            {
                "record_id": f"compatibility_budget__{metric_id}",
                "source_kind": "compatibility_budget",
                "metric_id": str(metric_id),
                "evaluation_stage": "postselection_scene",
                "scope_kind": scope_kind,
                "scope_id": scope_id,
                "minimum": 0,
                "maximum": int(maximum),
            }
        )
    runtime_limits = (
        ("context_profile_carriers", "postselection_scene", "global", "context_carrier", 6),
        ("global_optional_remote", "postselection_scene", "global", "optional_remote", 1),
        ("literal_realization_atoms_per_facet", "preselection_reservation", "each_facet", None, UNIVERSAL_LITERAL_REALIZATION_MAX_PER_FACET),
        ("literal_realization_atoms_total", "preselection_reservation", "global", "literal_realization", UNIVERSAL_LITERAL_REALIZATION_MAX_TOTAL),
        ("selected_resource_claims_total", "postselection_scene", "global", "resource_claim", UNIVERSAL_SELECTED_RESOURCE_CLAIM_MAX_TOTAL),
        ("selected_visual_atoms_total", "postselection_scene", "global", "visual_atom", UNIVERSAL_SELECTED_VISUAL_ATOM_MAX_TOTAL),
    )
    for metric_id, stage, scope_kind, scope_id, maximum in runtime_limits:
        rows.append(
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
        )
    rows.sort(key=lambda row: str(row["record_id"]).encode("utf-8"))
    return rows


def _audit_policy_gate_projection(
    scene: Mapping[str, Any], assets: Any, matched_prop_ids: set[str]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    raw_candidates = getattr(assets, "candidates", {})
    compatibility = getattr(assets, "compatibility", {})
    proposal_profiles = (
        raw_candidates.get("proposal_profiles", [])
        if isinstance(raw_candidates, Mapping)
        else []
    )
    context_profiles = (
        raw_candidates.get("context_distance_profiles", [])
        if isinstance(raw_candidates, Mapping)
        else []
    )
    universal_rules = (
        compatibility.get("universal_rules", [])
        if isinstance(compatibility, Mapping)
        else []
    )
    violence = _mapping(_mapping(scene.get("scene_contract")).get("context_profile")).get(
        "violence"
    )
    source_contracts: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    for source_kind, prefix, profiles in (
        ("proposal_policy", "proposal_policy__", proposal_profiles),
        ("context_policy", "context_policy__", context_profiles),
    ):
        for profile in profiles:
            if not isinstance(profile, Mapping):
                continue
            source_id = str(profile.get("id"))
            record_id = f"{prefix}{source_id}"
            policy_mode = str(profile.get("policy_mode"))
            source_payload = {
                "schema": "illustration-universal-scene-policy-source-contract/v1",
                "record_id": record_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "evaluation_stage": "contract_input",
                "policy_mode": policy_mode,
                "declared_outcome": None,
                "source_record": _audit_plain_json(profile),
            }
            source_contracts.append(
                {
                    "record_id": record_id,
                    "source_kind": source_kind,
                    "source_id": source_id,
                    "evaluation_stage": "contract_input",
                    "policy_mode": policy_mode,
                    "declared_outcome": None,
                    "source_contract_sha256": _audit_canonical_sha256(
                        source_payload
                    ),
                }
            )
            if policy_mode == "ordinary":
                applicable, outcome, reasons = True, "pass", ["policy_pass"]
            elif policy_mode == "safe_tool":
                applicable = True
                if violence == "active":
                    outcome, reasons = "reject", ["policy_active_violence"]
                else:
                    outcome, reasons = "pass", ["policy_pass"]
            elif source_kind == "proposal_policy":
                applicable, outcome, reasons = (
                    True,
                    "reject",
                    ["policy_explicit_only"],
                )
            elif "prop_decommissioned_machine_gun" in matched_prop_ids:
                applicable, outcome, reasons = True, "pass", ["policy_pass"]
            else:
                applicable, outcome, reasons = (
                    False,
                    "not_applicable",
                    ["policy_not_applicable"],
                )
            decisions.append(
                {
                    "record_id": record_id,
                    "applicable": applicable,
                    "outcome": outcome,
                    "reason_codes": reasons,
                }
            )
    for rule in universal_rules:
        if not isinstance(rule, Mapping):
            continue
        source_id = str(rule.get("id"))
        record_id = f"universal_rule__{source_id}"
        declared_outcome = str(rule.get("outcome"))
        source_payload = {
            "schema": "illustration-universal-scene-policy-source-contract/v1",
            "record_id": record_id,
            "source_kind": "universal_rule",
            "source_id": source_id,
            "evaluation_stage": "postselection",
            "policy_mode": None,
            "declared_outcome": declared_outcome,
            "source_record": _audit_plain_json(rule),
        }
        source_contracts.append(
            {
                "record_id": record_id,
                "source_kind": "universal_rule",
                "source_id": source_id,
                "evaluation_stage": "postselection",
                "policy_mode": None,
                "declared_outcome": declared_outcome,
                "source_contract_sha256": _audit_canonical_sha256(source_payload),
            }
        )
    source_contracts.sort(key=lambda row: str(row["record_id"]).encode("utf-8"))
    decisions.sort(key=lambda row: str(row["record_id"]).encode("utf-8"))
    return source_contracts, decisions


def _audit_guard_source_contract_projection(
    assets: Any, semantic_bindings: Mapping[str, Any]
) -> list[dict[str, Any]]:
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    guard_profiles = semantic_bindings.get("guard_execution_profiles")
    predicate_by_guard = {
        str(profile.get("guard_id")): str(profile.get("predicate_id"))
        for profile in (guard_profiles if isinstance(guard_profiles, list) else [])
        if isinstance(profile, Mapping)
    }
    rows: list[dict[str, Any]] = []
    for guard_id in _audit_utf8_sorted(predicate_by_guard):
        candidate = (
            candidate_by_id.get(guard_id)
            if isinstance(candidate_by_id, Mapping)
            else None
        )
        if not isinstance(candidate, Mapping):
            raise ValueError(f"guard source {guard_id} is absent")
        runtime_contract = candidate.get("runtime_contract")
        runtime_contract = (
            runtime_contract if isinstance(runtime_contract, Mapping) else {}
        )
        source_payload = {
            "record_id": guard_id,
            "source_candidate_id": guard_id,
            "predicate_id": predicate_by_guard[guard_id],
            "role": str(candidate.get("role")),
            "evaluation_stage": "postselection_conditional",
            "research_topic_ids": _audit_utf8_sorted(
                _string_list(candidate.get("research_topic_ids")) or []
            ),
            "provenance_record_ids": _audit_utf8_sorted(
                _string_list(candidate.get("provenance_record_ids")) or []
            ),
            "stage": str(runtime_contract.get("stage")),
            "violation_code": str(runtime_contract.get("violation_code")),
            "when_all": _audit_plain_json(runtime_contract.get("when_all", [])),
            "require_all": _audit_plain_json(
                runtime_contract.get("require_all", [])
            ),
            "declared_outcome": str(runtime_contract.get("outcome")),
        }
        rows.append(
            {
                **source_payload,
                "source_contract_sha256": _audit_canonical_sha256(
                    source_payload
                ),
            }
        )
    return rows


def _audit_preselection_feasibility_projection(
    scene: Mapping[str, Any],
    assets: Any,
    semantic_bindings: Mapping[str, Any],
    scene_contract_sha256: str,
    capacity_rows: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    raw_candidates = getattr(assets, "candidates", {})
    proposal_profiles = (
        raw_candidates.get("proposal_profiles", [])
        if isinstance(raw_candidates, Mapping)
        else []
    )
    record_specs: list[tuple[str, str, str | None]] = [
        ("mandatory_literal__base", "mandatory_literal", None)
    ]
    record_specs.extend(
        (f"proposal__{profile.get('id')}", "proposal", str(profile.get("id")))
        for profile in proposal_profiles
        if isinstance(profile, Mapping)
    )
    record_specs.extend(
        (f"candidate__{candidate_id}", "visual_candidate", str(candidate_id))
        for candidate_id, candidate in (
            candidate_by_id.items() if isinstance(candidate_by_id, Mapping) else []
        )
        if isinstance(candidate, Mapping) and candidate.get("role") == "visual_atom"
    )
    record_specs.sort(key=lambda item: item[0].encode("utf-8"))
    capacities_by_hash_kind = {
        (str(row.get("owner_scope_hash")), str(row.get("resource_kind"))): int(
            row.get("capacity", 0)
        )
        for row in capacity_rows
    }
    resource_rows: list[dict[str, Any]] = []
    cardinality_rows: list[dict[str, Any]] = []
    for record_id, source_kind, source_id in record_specs:
        trial, source_record = _audit_preselection_trial(
            record_id,
            source_kind,
            source_id,
            scene=scene,
            assets=assets,
            semantic_bindings=semantic_bindings,
            scene_contract_sha256=scene_contract_sha256,
        )
        aggregates: dict[tuple[str, str], tuple[int, int]] = {}
        for claim in trial["resolved_claims"]:
            key = (str(claim["owner_scope_hash"]), str(claim["resource_kind"]))
            exclusive, shared = aggregates.get(key, (0, 0))
            if claim["mode"] == "exclusive":
                exclusive += int(claim["amount"])
            else:
                shared = max(shared, int(claim["amount"]))
            aggregates[key] = (exclusive, shared)
        checks: list[dict[str, Any]] = []
        for owner_hash, resource_kind in sorted(aggregates):
            exclusive, shared = aggregates[(owner_hash, resource_kind)]
            capacity = capacities_by_hash_kind.get((owner_hash, resource_kind), 0)
            checks.append(
                {
                    "owner_scope_hash": owner_hash,
                    "resource_kind": resource_kind,
                    "exclusive_required": exclusive,
                    "shared_required": shared,
                    "capacity": capacity,
                    "fits": exclusive + shared <= capacity,
                }
            )
        resource_pass = all(check["fits"] for check in checks)
        shared_fields = {
            "record_id": record_id,
            "source_kind": source_kind,
            "source_id": source_id,
            "source_record_sha256": _audit_canonical_sha256(source_record),
            "trial_sha256": _audit_canonical_sha256(trial),
        }
        resource_rows.append(
            {
                **shared_fields,
                "checks": checks,
                "outcome": "eligible" if resource_pass else "rejected",
                "reason_codes": [
                    "resource_feasible" if resource_pass else "resource_capacity"
                ],
            }
        )
        per_facet_pass = all(
            int(row["count"]) <= UNIVERSAL_LITERAL_REALIZATION_MAX_PER_FACET
            for row in trial["literal_facet_counts"]
        )
        total_pass = (
            int(trial["literal_total"]) <= UNIVERSAL_LITERAL_REALIZATION_MAX_TOTAL
        )
        limit_results = [
            {
                "limit_id": "runtime_limit__literal_realization_atoms_per_facet",
                "fits": per_facet_pass,
            },
            {
                "limit_id": "runtime_limit__literal_realization_atoms_total",
                "fits": total_pass,
            },
        ]
        cardinality_pass = per_facet_pass and total_pass
        cardinality_rows.append(
            {
                **shared_fields,
                "limit_results": limit_results,
                "outcome": "eligible" if cardinality_pass else "rejected",
                "reason_codes": [
                    "cardinality_feasible"
                    if cardinality_pass
                    else "cardinality_limit"
                ],
            }
        )
    return resource_rows, cardinality_rows


def _audit_matched_prop_sense_occurrence_hashes(
    scene: Mapping[str, Any],
    assets: Any,
    semantic_bindings: Mapping[str, Any],
) -> list[str]:
    contract = _mapping(scene.get("scene_contract"))
    slots = (
        contract.get("slot_states")
        if isinstance(contract.get("slot_states"), list)
        else []
    )
    prop_index = next(
        (
            index
            for index, slot in enumerate(slots)
            if isinstance(slot, Mapping) and slot.get("slot_id") == "prop"
        ),
        None,
    )
    if prop_index is None:
        return []
    prop_slot = slots[prop_index]
    sources: list[tuple[str, str]] = []
    if prop_slot.get("state") == "fixed":
        sources.extend(
            (
                f"/slot_states/{prop_index}/request_phrases/{phrase_index}",
                str(phrase),
            )
            for phrase_index, phrase in enumerate(
                _string_list(prop_slot.get("request_phrases")) or []
            )
        )
    roles = (
        contract.get("event_roles")
        if isinstance(contract.get("event_roles"), list)
        else []
    )
    role_by_id = {
        str(role.get("role_id")): role
        for role in roles
        if isinstance(role, Mapping)
    }
    for role_id in ("target", "instrument"):
        role = _mapping(role_by_id.get(role_id))
        if role.get("state") != "fixed":
            continue
        role_index = UNIVERSAL_ROLE_IDS.index(role_id)
        sources.extend(
            (
                f"/event_roles/{role_index}/request_phrases/{phrase_index}",
                str(phrase),
            )
            for phrase_index, phrase in enumerate(
                _string_list(role.get("request_phrases")) or []
            )
        )
    semantic_values = _audit_utf8_sorted(
        {
            *(
                _normalized_literal_text(value)
                for value in (_string_list(prop_slot.get("value_ids")) or [])
            ),
            *(
                _normalized_literal_text(role_by_id[role_id].get("value_id"))
                for role_id in ("target", "instrument")
                if isinstance(role_by_id.get(role_id), Mapping)
                and role_by_id[role_id].get("state") == "fixed"
            ),
        }
    )
    phrases = [phrase for _, phrase in sources]
    prop_senses = getattr(assets, "prop_sense_by_catalog_id", {})
    result: list[str] = []
    for profiles in (
        prop_senses.values() if isinstance(prop_senses, Mapping) else []
    ):
        for profile in profiles if isinstance(profiles, Sequence) else []:
            if not isinstance(profile, Mapping):
                continue
            aliases = [
                str(alias)
                for record in profile.get("literal_aliases", [])
                if isinstance(record, Mapping)
                for alias in (_string_list(record.get("values")) or [])
            ]
            literal_match = any(
                _literal_catalog_alias_matches(alias, phrase)
                for alias in aliases
                for phrase in phrases
            )
            semantic_match = any(
                _audit_contains_token_subsequence(
                    _audit_semantic_tokens(value), _audit_semantic_tokens(token)
                )
                for token in (
                    _string_list(profile.get("accepted_semantic_tokens")) or []
                )
                for value in semantic_values
            )
            if not (literal_match and semantic_match):
                continue
            canonical_prop_id = str(
                profile.get("activation_target") or profile.get("catalog_prop_id")
            )
            for source_pointer, phrase in sources:
                normalized_phrase = _normalized_literal_text(phrase)
                for alias in aliases:
                    spans = list(
                        _universal_literal_alias_spans(alias, normalized_phrase)
                    )
                    polarities = list(
                        _universal_literal_effect_polarities(
                            normalized_phrase,
                            [alias],
                            semantic_bindings,
                            include_target_absence=True,
                            include_target_substitution=True,
                            allow_korean_postposed_copular=False,
                        )
                    )
                    if len(spans) != len(polarities):
                        raise ValueError(
                            "prop-sense occurrence polarity did not preserve spans"
                        )
                    for (start, end), polarity in zip(spans, polarities):
                        result.append(
                            _audit_canonical_sha256(
                                {
                                    "schema": "illustration-universal-scene-prop-sense-occurrence/v1",
                                    "source_pointer": source_pointer,
                                    "normalized_source_text_sha256": hashlib.sha256(
                                        normalized_phrase.encode("utf-8")
                                    ).hexdigest(),
                                    "binding_profile_id": str(profile.get("id")),
                                    "canonical_prop_id": canonical_prop_id,
                                    "matched_alias_sha256": hashlib.sha256(
                                        _normalized_literal_text(alias).encode("utf-8")
                                    ).hexdigest(),
                                    "semantic_values_sha256": _audit_canonical_sha256(
                                        semantic_values
                                    ),
                                    "occurrence_start": start,
                                    "occurrence_end": end,
                                    "polarity": polarity,
                                }
                            )
                        )
    return _audit_utf8_sorted(result)


def _audit_expected_creativity_invariant_trace(
    scene: Mapping[str, Any],
    request_text: str,
    assets: Any,
    semantic_bindings: Mapping[str, Any],
) -> dict[str, Any]:
    """Recompute the frozen, selection-independent trace from primary inputs."""

    contract = _mapping(scene.get("scene_contract"))
    scene_contract_sha256 = _audit_canonical_sha256(contract)
    compatibility = getattr(assets, "compatibility", {})
    if not isinstance(compatibility, Mapping):
        raise ValueError("compatibility asset is unavailable")
    raw_reason_ids = compatibility.get("decision_reason_code_ids")
    actual_reason_ids = list(raw_reason_ids) if isinstance(raw_reason_ids, list) else None
    if actual_reason_ids != list(UNIVERSAL_DECISION_REASON_CODE_IDS):
        raise ValueError("decision reason registry differs from the frozen order")

    eligible_proposals, rejected_proposals = _audit_proposal_invariant_partition(
        scene, assets
    )
    eligible_candidate_ids, rejected_candidates = (
        _audit_candidate_invariant_partition(scene, assets)
    )
    capacity_rows, _capacity_by_owner_kind = _audit_resource_capacity_projection(
        scene, scene_contract_sha256
    )
    resource_feasibility, cardinality_feasibility = (
        _audit_preselection_feasibility_projection(
            scene,
            assets,
            semantic_bindings,
            scene_contract_sha256,
            capacity_rows,
        )
    )
    cardinality_limits = _audit_cardinality_limit_projection(compatibility)
    if [row["record_id"] for row in cardinality_limits] != list(
        UNIVERSAL_CARDINALITY_LIMIT_IDS
    ):
        raise ValueError("cardinality limit inventory or UTF-8 order has drifted")
    matched_prop_ids = _audit_matched_catalog_prop_ids(scene, assets)
    policy_sources, policy_decisions = _audit_policy_gate_projection(
        scene, assets, matched_prop_ids
    )
    guard_sources = _audit_guard_source_contract_projection(
        assets, semantic_bindings
    )
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    raw_candidates = getattr(assets, "candidates", {})
    proposal_profiles = (
        raw_candidates.get("proposal_profiles", [])
        if isinstance(raw_candidates, Mapping)
        else []
    )
    visual_candidate_ids = _audit_utf8_sorted(
        str(candidate_id)
        for candidate_id, candidate in (
            candidate_by_id.items() if isinstance(candidate_by_id, Mapping) else []
        )
        if isinstance(candidate, Mapping) and candidate.get("role") == "visual_atom"
    )
    inventory = {
        "proposal_profile_ids": _audit_utf8_sorted(
            str(profile.get("id"))
            for profile in proposal_profiles
            if isinstance(profile, Mapping)
        ),
        "visual_candidate_ids": visual_candidate_ids,
        "guard_candidate_ids": _audit_utf8_sorted(
            _string_list(compatibility.get("guard_candidate_ids")) or []
        ),
        "policy_source_record_ids": _audit_utf8_sorted(
            str(row["record_id"]) for row in policy_sources
        ),
        "preselection_policy_decision_ids": _audit_utf8_sorted(
            str(row["record_id"]) for row in policy_decisions
        ),
        "resource_feasibility_record_ids": _audit_utf8_sorted(
            str(row["record_id"]) for row in resource_feasibility
        ),
        "cardinality_limit_ids": _audit_utf8_sorted(
            str(row["record_id"]) for row in cardinality_limits
        ),
        "cardinality_feasibility_record_ids": _audit_utf8_sorted(
            str(row["record_id"]) for row in cardinality_feasibility
        ),
    }
    asset_hashes = getattr(assets, "asset_hashes", {})
    if not isinstance(asset_hashes, Mapping):
        raise ValueError("validated asset hash inventory is unavailable")
    trace: dict[str, Any] = {
        "schema": UNIVERSAL_CREATIVITY_INVARIANT_SCHEMA,
        "request_sha256": hashlib.sha256(request_text.encode("utf-8")).hexdigest(),
        "scene_contract_sha256": scene_contract_sha256,
        "asset_hashes": _audit_plain_json(asset_hashes),
        "reason_code_registry": list(UNIVERSAL_DECISION_REASON_CODE_IDS),
        "inventory": inventory,
        "eligible_proposals": eligible_proposals,
        "rejected_proposals": rejected_proposals,
        "eligible_candidate_ids": eligible_candidate_ids,
        "rejected_candidates": rejected_candidates,
        "matched_prop_sense_hashes": _audit_matched_prop_sense_occurrence_hashes(
            scene, assets, semantic_bindings
        ),
        "policy_source_contracts": policy_sources,
        "preselection_policy_decisions": policy_decisions,
        "resource_capacities": capacity_rows,
        "resource_feasibility": resource_feasibility,
        "cardinality_limits": cardinality_limits,
        "cardinality_feasibility": cardinality_feasibility,
        "guard_source_contracts": guard_sources,
        "guard_source_contracts_sha256": _audit_canonical_sha256(guard_sources),
        "complete_trace": True,
    }
    trace["trace_sha256"] = _audit_canonical_sha256(trace)
    return trace


def _audit_creativity_invariant_trace_failures(
    scene: Mapping[str, Any],
    request_text: str,
    assets: Any,
    semantic_bindings: Mapping[str, Any],
) -> list[dict[str, Any]]:
    try:
        expected = _audit_expected_creativity_invariant_trace(
            scene, request_text, assets, semantic_bindings
        )
    except (KeyError, TypeError, ValueError) as exc:
        return [
            issue(
                "universal_creativity_invariant",
                "independent creativity-invariant replay could not derive the complete frozen trace",
                error=str(exc),
            )
        ]
    actual_value = scene.get("creativity_invariant_trace")
    actual = _mapping(actual_value)
    failures: list[dict[str, Any]] = []
    if not isinstance(actual_value, dict) or set(actual) != UNIVERSAL_CREATIVITY_INVARIANT_KEYS:
        failures.append(
            issue(
                "universal_creativity_invariant",
                "creativity-invariant trace must expose the exact frozen field set",
                expected=sorted(UNIVERSAL_CREATIVITY_INVARIANT_KEYS),
                actual=sorted(actual) if isinstance(actual_value, dict) else actual_value,
            )
        )
    if actual != expected:
        failures.append(
            issue(
                "universal_creativity_invariant",
                "creativity-invariant trace must exactly equal independent raw-asset and embedded-contract replay",
                mismatched_fields=sorted(
                    key
                    for key in UNIVERSAL_CREATIVITY_INVARIANT_KEYS
                    if actual.get(key) != expected.get(key)
                ),
                expected_trace_sha256=expected.get("trace_sha256"),
                actual_trace_sha256=actual.get("trace_sha256"),
            )
        )
    return failures


def _audit_selected_candidate_roster_projection(
    scene: Mapping[str, Any],
    assets: Any,
    context_overlay_pairs: Sequence[tuple[str, str]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    context_profiles_by_instance: dict[str, set[str]] = {}
    for profile_id, instance_id in context_overlay_pairs:
        context_profiles_by_instance.setdefault(str(instance_id), set()).add(
            str(profile_id)
        )
    contract = _mapping(scene.get("scene_contract"))
    role_by_id = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, Mapping)
    }
    actor_entity_id = _audit_participant_primary(scene, "actor") or ""
    proposal_by_id = getattr(assets, "proposal_by_id", {})
    rows: list[dict[str, Any]] = []
    for selection_ordinal, atom in enumerate(
        scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
    ):
        if not isinstance(atom, Mapping):
            raise ValueError("selected candidate roster contains an untyped atom")
        instance_id = str(atom.get("instance_id"))
        candidate_id = str(atom.get("candidate_id"))
        facet_id = str(atom.get("facet"))
        parameters = _mapping(atom.get("parameters"))
        proposal_id = parameters.get("proposal_id")
        proposal = (
            proposal_by_id.get(str(proposal_id))
            if proposal_id is not None and isinstance(proposal_by_id, Mapping)
            else None
        )
        proposal_ids = (
            _string_list(proposal.get("candidate_ids"))
            if isinstance(proposal, Mapping)
            else None
        ) or []
        proposal_primary = bool(
            proposal_id is not None
            and proposal_ids
            and proposal_ids[0] == candidate_id
        )
        literal_profile_id = parameters.get("literal_realization_profile_id")
        mandatory_literal = literal_profile_id is not None
        source_slot_id = parameters.get("source_slot_id")
        contract_slots = {
            str(slot.get("slot_id")): slot
            for slot in contract.get("slot_states", [])
            if isinstance(slot, Mapping)
        }
        fixed_realization = (
            _audit_derived_facet_state(
                facet_id,
                contract=contract,
                actor_entity_id=actor_entity_id,
            )
            == "fixed"
            or (
                source_slot_id in UNIVERSAL_SLOT_IDS
                and _mapping(contract_slots.get(str(source_slot_id))).get("state")
                == "fixed"
            )
        )
        core_anchor = candidate_id == "usl_core_identity_anchor"
        context_profile_ids = _audit_utf8_sorted(
            context_profiles_by_instance.get(instance_id, set())
        )
        authority_refs: list[dict[str, str]] = []
        if mandatory_literal:
            authority_refs.append(
                {
                    "kind": "literal_realization_profile",
                    "source_id": str(literal_profile_id),
                }
            )
        if fixed_realization:
            if source_slot_id in UNIVERSAL_SLOT_IDS:
                authority_refs.append(
                    {"kind": "fixed_slot", "source_id": str(source_slot_id)}
                )
            elif facet_id in UNIVERSAL_SLOT_IDS:
                authority_refs.append(
                    {"kind": "fixed_slot", "source_id": facet_id}
                )
            elif (
                facet_id == "phase"
                and _mapping(role_by_id.get("phase")).get("state") == "fixed"
            ):
                authority_refs.append(
                    {"kind": "fixed_role", "source_id": "phase"}
                )
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
                (str(item["kind"]), str(item["source_id"])): item
                for item in authority_refs
            }.values(),
            key=lambda item: (
                str(item["kind"]).encode("utf-8"),
                str(item["source_id"]).encode("utf-8"),
            ),
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
                    "context_carrier": bool(context_profile_ids),
                },
                "authority_refs": authority_refs,
            }
        )
    if len({row["instance_id"] for row in rows}) != len(rows):
        raise ValueError("selected candidate roster has duplicate instance IDs")
    return {
        "schema": "illustration-universal-scene-selected-candidate-roster/v1",
        "rows": rows,
    }, rows


def _audit_candidate_roster_subprojections(
    roster_rows: Sequence[Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    protected_counts: dict[tuple[Any, ...], int] = {}
    proposal_counts: dict[str, int] = {}
    optional_rows: list[dict[str, Any]] = []
    for row in roster_rows:
        flags = _mapping(row.get("protection_flags"))
        protected = any(bool(value) for value in flags.values())
        if protected:
            key = (
                str(row.get("candidate_id")),
                bool(flags.get("mandatory_literal")),
                bool(flags.get("fixed_realization")),
                bool(flags.get("core_anchor")),
                bool(flags.get("context_carrier")),
            )
            protected_counts[key] = protected_counts.get(key, 0) + 1
        elif row.get("proposal_primary") is True:
            candidate_id = str(row.get("candidate_id"))
            proposal_counts[candidate_id] = proposal_counts.get(candidate_id, 0) + 1
        else:
            optional_rows.append(
                {
                    "selection_ordinal": int(row.get("selection_ordinal", 0)),
                    "instance_id": str(row.get("instance_id")),
                    "candidate_id": str(row.get("candidate_id")),
                    "facet_id": str(row.get("facet_id")),
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


def _audit_fixed_contract_projection(scene: Mapping[str, Any]) -> dict[str, Any]:
    contract = _mapping(scene.get("scene_contract"))
    return {
        "schema": "illustration-universal-scene-fixed-contract/v1",
        "identity_core": _audit_plain_json(contract.get("identity_core")),
        "participant_bindings": _audit_plain_json(
            contract.get("participant_bindings")
        ),
        "slot_states": _audit_plain_json(contract.get("slot_states")),
        "event_roles": _audit_plain_json(contract.get("event_roles")),
        "context_profile": _audit_plain_json(contract.get("context_profile")),
    }


def _audit_resolved_proposal_role_value(
    profile: Mapping[str, Any],
    role_id: str,
    scene: Mapping[str, Any],
) -> str | None:
    """Resolve one raw proposal role without trusting serialized role output."""

    event_roles = _mapping(profile.get("event_roles"))
    raw_value = event_roles.get(role_id)
    if raw_value is None:
        return None
    contract = _mapping(scene.get("scene_contract"))
    contract_roles = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, Mapping)
    }
    if raw_value == "$identity_actor":
        actor = _mapping(contract_roles.get("actor"))
        if actor.get("state") == "fixed" and _is_nonempty_string(
            actor.get("value_id")
        ):
            return str(actor["value_id"])
        return _audit_participant_primary(scene, "actor")
    if raw_value == "$scene_location":
        location = _mapping(contract_roles.get("location"))
        if location.get("state") == "fixed" and _is_nonempty_string(
            location.get("value_id")
        ):
            return str(location["value_id"])
        environment = next(
            (
                slot
                for slot in (
                    contract.get("slot_states")
                    if isinstance(contract.get("slot_states"), list)
                    else []
                )
                if isinstance(slot, Mapping)
                and slot.get("slot_id") == "environment"
            ),
            {},
        )
        values = _string_list(_mapping(environment).get("value_ids")) or []
        return (
            str(values[0])
            if _mapping(environment).get("state") == "fixed" and values
            else None
        )
    return str(raw_value)


def _audit_atom_role_binding_matches(
    atom: Mapping[str, Any],
    candidate: Mapping[str, Any],
    role_id: str,
    value_id: str,
) -> bool:
    """Require one raw candidate binding and one equal serialized binding."""

    runtime_contract = _mapping(candidate.get("runtime_contract"))
    authored = [
        str(binding[1])
        for binding in (
            runtime_contract.get("bindings")
            if isinstance(runtime_contract.get("bindings"), list)
            else []
        )
        if isinstance(binding, Sequence)
        and not isinstance(binding, (str, bytes))
        and len(binding) == 2
        and str(binding[0]) == role_id
    ]
    serialized = [
        binding
        for binding in (
            atom.get("bindings") if isinstance(atom.get("bindings"), list) else []
        )
        if isinstance(binding, Mapping) and str(binding.get("role_id")) == role_id
    ]
    if len(authored) != 1 or len(serialized) != 1:
        return False
    expected_requirement = (
        "required" if authored[0] == "event_spine" else authored[0]
    )
    return (
        str(serialized[0].get("node_id")) == value_id
        and str(serialized[0].get("requirement")) == expected_requirement
    )


def _audit_bridge_role_binding_matches(
    bridge: Mapping[str, Any],
    role_id: str,
    value_id: str,
    *,
    scene: Mapping[str, Any],
    assets: Any,
) -> bool:
    """Authenticate a bridge role against its raw type, exact edge, and endpoint."""

    bridge_type = str(bridge.get("bridge_type"))
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    candidate = (
        candidate_by_id.get(str(bridge.get("candidate_id")))
        if isinstance(candidate_by_id, Mapping)
        else None
    )
    runtime_contract = _mapping(
        candidate.get("runtime_contract") if isinstance(candidate, Mapping) else None
    )
    if (
        not isinstance(candidate, Mapping)
        or bridge_type
        not in (_string_list(runtime_contract.get("bridge_types")) or [])
    ):
        return False
    event = _mapping(scene.get("selected_event"))
    edge_by_id = {
        str(edge.get("edge_id")): edge
        for edge in (
            event.get("spine_edges")
            if isinstance(event.get("spine_edges"), list)
            else []
        )
        if isinstance(edge, Mapping) and _is_nonempty_string(edge.get("edge_id"))
    }
    event_edge_ids = _string_list(bridge.get("event_edge_ids")) or []
    if not event_edge_ids or len(event_edge_ids) != len(set(event_edge_ids)):
        return False
    expected_edge = {
        "from_node_id": str(bridge.get("from_node_id")),
        "relation_id": f"bridge:{bridge_type}",
        "to_node_id": str(bridge.get("to_node_id")),
    }
    for edge_id in event_edge_ids:
        edge = _mapping(edge_by_id.get(edge_id))
        if (
            edge.get("edge_id") != edge_id
            or any(edge.get(key) != value for key, value in expected_edge.items())
        ):
            return False
    if role_id == "target":
        return (
            bridge_type in UNIVERSAL_BRIDGE_MEDIATION_TYPES
            and str(bridge.get("to_node_id")) == value_id
        ) or (
            bridge_type in UNIVERSAL_BRIDGE_EXIT_TYPES
            and str(bridge.get("from_node_id")) == value_id
        )
    if role_id == "result":
        return (
            bridge_type in UNIVERSAL_BRIDGE_EXIT_TYPES
            and str(bridge.get("to_node_id")) == value_id
        )
    return False


def _audit_runtime_selected_role_authority(
    role: Mapping[str, Any],
    *,
    scene: Mapping[str, Any],
    assets: Any,
) -> tuple[str, str | None, str | None]:
    """Independently bind one runtime role to its exact selected authority."""

    role_id = str(role.get("role_id"))
    value_id = role.get("value_id")
    source_id = str(role.get("source_id"))
    atoms = [
        atom
        for atom in (
            scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
        )
        if isinstance(atom, Mapping)
    ]
    bridges = [
        bridge
        for bridge in (
            scene.get("bridges") if isinstance(scene.get("bridges"), list) else []
        )
        if isinstance(bridge, Mapping)
    ]
    atom_by_id = {str(atom.get("instance_id")): atom for atom in atoms}
    bridge_by_id = {str(bridge.get("bridge_id")): bridge for bridge in bridges}
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    proposal_by_id = getattr(assets, "proposal_by_id", {})

    if role_id in {"actor", "location"} and source_id.startswith(
        "identity_entity:"
    ):
        entity_id = source_id.removeprefix("identity_entity:")
        expected_entity = _audit_participant_primary(scene, role_id)
        if entity_id != expected_entity or value_id != expected_entity:
            raise ValueError(
                f"runtime-selected {role_id} lacks its exact participant identity anchor"
            )
        contract = _mapping(scene.get("scene_contract"))
        participant = next(
            (
                binding
                for binding in (
                    contract.get("participant_bindings")
                    if isinstance(contract.get("participant_bindings"), list)
                    else []
                )
                if isinstance(binding, Mapping)
                and binding.get("role_id") == role_id
            ),
            {},
        )
        entity = next(
            (
                item
                for item in _mapping(contract.get("identity_core")).get(
                    "entities", []
                )
                if isinstance(item, Mapping) and item.get("entity_id") == entity_id
            ),
            {},
        )
        return (
            "identity_anchor",
            entity_id,
            _audit_canonical_sha256(
                {"participant": _audit_plain_json(participant), "entity": _audit_plain_json(entity)}
            ),
        )
    if source_id.startswith("identity_entity:"):
        raise ValueError(
            f"runtime-selected role {role_id} cannot borrow an identity anchor"
        )

    source_atom = atom_by_id.get(source_id)
    selected_proposal_atoms = [
        atom
        for atom in atoms
        if _is_nonempty_string(_mapping(atom.get("parameters")).get("proposal_id"))
    ]
    proposal_authorities: list[tuple[Mapping[str, Any], Mapping[str, Any]]] = []
    for atom in selected_proposal_atoms:
        proposal_id = str(_mapping(atom.get("parameters")).get("proposal_id"))
        profile = (
            proposal_by_id.get(proposal_id)
            if isinstance(proposal_by_id, Mapping)
            else None
        )
        if isinstance(profile, Mapping) and _audit_resolved_proposal_role_value(
            profile, role_id, scene
        ) == value_id:
            proposal_authorities.append((atom, profile))
    if proposal_authorities and (
        len(proposal_authorities) != 1
        or proposal_authorities[0][0] is not source_atom
    ):
        raise ValueError(
            f"runtime-selected role {role_id} was swapped away from its exact proposal source"
        )
    if source_atom is not None and _is_nonempty_string(
        _mapping(source_atom.get("parameters")).get("proposal_id")
    ):
        proposal_id = str(_mapping(source_atom.get("parameters")).get("proposal_id"))
        profile = (
            proposal_by_id.get(proposal_id)
            if isinstance(proposal_by_id, Mapping)
            else None
        )
        same_profile_atoms = [
            atom
            for atom in selected_proposal_atoms
            if str(_mapping(atom.get("parameters")).get("proposal_id")) == proposal_id
        ]
        candidate_ids = (
            _string_list(profile.get("candidate_ids"))
            if isinstance(profile, Mapping)
            else None
        ) or []
        if (
            not isinstance(profile, Mapping)
            or len(same_profile_atoms) != 1
            or same_profile_atoms[0] is not source_atom
            or not candidate_ids
            or str(source_atom.get("candidate_id")) != candidate_ids[0]
            or _audit_resolved_proposal_role_value(profile, role_id, scene)
            != value_id
        ):
            raise ValueError(
                f"runtime-selected role {role_id} does not resolve from its exact proposal event frame"
            )
        return (
            "proposal_event_frame",
            proposal_id,
            _audit_canonical_sha256(profile),
        )

    if value_id is None:
        return "none", None, None
    value_text = str(value_id)
    if source_atom is not None:
        candidate_id = str(source_atom.get("candidate_id"))
        candidate = (
            candidate_by_id.get(candidate_id)
            if isinstance(candidate_by_id, Mapping)
            else None
        )
        if (
            not isinstance(candidate, Mapping)
            or (role_id in {"action", "phase"} and candidate_id != value_text)
            or not _audit_atom_role_binding_matches(
                source_atom, candidate, role_id, value_text
            )
        ):
            raise ValueError(
                f"runtime-selected role {role_id} source atom lacks its exact authored and serialized binding"
            )
        return (
            "selected_candidate_binding",
            candidate_id,
            _audit_canonical_sha256(candidate),
        )

    source_bridge = bridge_by_id.get(source_id)
    if source_bridge is not None:
        matching_bridges = [
            bridge
            for bridge in bridges
            if _audit_bridge_role_binding_matches(
                bridge, role_id, value_text, scene=scene, assets=assets
            )
        ]
        if (
            not matching_bridges
            or str(matching_bridges[0].get("bridge_id")) != source_id
        ):
            raise ValueError(
                f"runtime-selected role {role_id} does not cite the canonical exact typed bridge endpoint"
            )
        candidate_id = str(source_bridge.get("candidate_id"))
        candidate = (
            candidate_by_id.get(candidate_id)
            if isinstance(candidate_by_id, Mapping)
            else None
        )
        if not isinstance(candidate, Mapping):
            raise ValueError(
                f"runtime-selected role {role_id} bridge source candidate is absent"
            )
        return "bridge_binding", source_id, _audit_canonical_sha256(candidate)

    raise ValueError(
        f"runtime-selected role {role_id} lacks an exact selected authority source"
    )


def _audit_runtime_selected_role_source_failures(
    scene: Mapping[str, Any], assets: Any
) -> list[dict[str, Any]]:
    """Reject role/source swaps before trusting either trace or runtime replay."""

    contract = _mapping(scene.get("scene_contract"))
    contract_roles = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, Mapping)
    }
    runtime_roles = {
        str(role.get("role_id")): role
        for role in _mapping(scene.get("selected_event")).get("roles", [])
        if isinstance(role, Mapping)
    }
    failures: list[dict[str, Any]] = []
    for role_id in UNIVERSAL_ROLE_IDS:
        contract_role = _mapping(contract_roles.get(role_id))
        runtime_role = _mapping(runtime_roles.get(role_id))
        if (
            contract_role.get("state") != "open"
            or runtime_role.get("value_id") is None
        ):
            continue
        if runtime_role.get("source") != "runtime_selected":
            failures.append(
                issue(
                    "universal_event_spine",
                    "nonnull open role must remain runtime-selected",
                    role_id=role_id,
                    actual=runtime_role,
                )
            )
            continue
        try:
            _audit_runtime_selected_role_authority(
                runtime_role, scene=scene, assets=assets
            )
        except (KeyError, TypeError, ValueError) as exc:
            failures.append(
                issue(
                    "universal_event_spine",
                    "nonnull open runtime role must cite the exact authority that declares its role and value",
                    role_id=role_id,
                    source_id=runtime_role.get("source_id"),
                    value_id=runtime_role.get("value_id"),
                    error=str(exc),
                )
            )
    return failures


def _audit_role_projection_payloads(
    scene: Mapping[str, Any], assets: Any
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract = _mapping(scene.get("scene_contract"))
    contract_role_by_id = {
        str(role.get("role_id")): role
        for role in (
            contract.get("event_roles")
            if isinstance(contract.get("event_roles"), list)
            else []
        )
        if isinstance(role, Mapping)
    }
    participant_by_role = {
        str(binding.get("role_id")): binding
        for binding in (
            contract.get("participant_bindings")
            if isinstance(contract.get("participant_bindings"), list)
            else []
        )
        if isinstance(binding, Mapping)
    }
    entity_by_id = {
        str(entity.get("entity_id")): entity
        for entity in _mapping(contract.get("identity_core")).get("entities", [])
        if isinstance(entity, Mapping)
    }
    slot_by_id = {
        str(slot.get("slot_id")): slot
        for slot in (
            contract.get("slot_states")
            if isinstance(contract.get("slot_states"), list)
            else []
        )
        if isinstance(slot, Mapping)
    }
    runtime_roles = {
        str(role.get("role_id")): role
        for role in _mapping(scene.get("selected_event")).get("roles", [])
        if isinstance(role, Mapping)
    }
    contract_rows = [
        {
            "role_id": role_id,
            "state": str(_mapping(contract_role_by_id.get(role_id)).get("state")),
            "contract_value_id": (
                str(_mapping(contract_role_by_id.get(role_id)).get("value_id"))
                if _mapping(contract_role_by_id.get(role_id)).get("state") == "fixed"
                else None
            ),
        }
        for role_id in UNIVERSAL_ROLE_IDS
    ]
    protected_rows: list[dict[str, Any]] = []
    for role_id in UNIVERSAL_ROLE_IDS:
        contract_role = _mapping(contract_role_by_id.get(role_id))
        state = str(contract_role.get("state"))
        if state not in {"fixed", "closed"} and role_id not in {"actor", "location"}:
            continue
        runtime_value = _mapping(runtime_roles.get(role_id)).get("value_id")
        if state == "fixed":
            authority_kind = "contract_fixed"
            authority_source: Any = contract_role
        elif state == "closed":
            authority_kind = "contract_closed"
            authority_source = contract_role
        elif role_id == "actor":
            authority_kind = "identity_anchor"
            participant = _mapping(participant_by_role.get("actor"))
            actor_id = str(participant.get("primary_entity_id"))
            authority_source = {
                "participant": participant,
                "entity": _mapping(entity_by_id.get(actor_id)),
            }
        else:
            authority_kind = "location_anchor"
            authority_source = {
                "participant": _mapping(participant_by_role.get("location")),
                "environment_slot": _mapping(slot_by_id.get("environment")),
            }
        protected_rows.append(
            {
                "role_id": role_id,
                "contract_state": state,
                "runtime_value_id": runtime_value,
                "authority_kind": authority_kind,
                "authority_source_sha256": _audit_canonical_sha256(authority_source),
            }
        )

    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, Mapping)
    ]
    proposal_atoms = [
        atom for atom in atoms if "proposal_id" in _mapping(atom.get("parameters"))
    ]
    if len(proposal_atoms) > 1:
        raise ValueError("multiple proposal primaries are selected")
    proposal_by_id = getattr(assets, "proposal_by_id", {})
    proposal_profile = (
        proposal_by_id.get(
            str(_mapping(proposal_atoms[0].get("parameters")).get("proposal_id"))
        )
        if proposal_atoms and isinstance(proposal_by_id, Mapping)
        else None
    )
    open_rows: list[dict[str, Any]] = []
    for role_id in ("action", "target", "instrument", "recipient", "result", "phase"):
        if _mapping(contract_role_by_id.get(role_id)).get("state") != "open":
            continue
        role = _mapping(runtime_roles.get(role_id))
        value_id = role.get("value_id")
        authority_kind = "none"
        authority_record_id: str | None = None
        authority_source_sha256: str | None = None
        proposal_roles = (
            proposal_profile.get("event_roles")
            if isinstance(proposal_profile, Mapping)
            and isinstance(proposal_profile.get("event_roles"), Mapping)
            else {}
        )
        if value_id is None and proposal_profile is not None and proposal_roles.get(role_id) is None:
            authority_kind = "proposal_event_frame"
            authority_record_id = str(proposal_profile.get("id"))
            authority_source_sha256 = _audit_canonical_sha256(proposal_profile)
        elif value_id is not None:
            (
                authority_kind,
                authority_record_id,
                authority_source_sha256,
            ) = _audit_runtime_selected_role_authority(
                role, scene=scene, assets=assets
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
    open_rows.sort(key=lambda row: str(row["role_id"]).encode("utf-8"))
    return (
        {
            "schema": "illustration-universal-scene-contract-roles/v1",
            "rows": contract_rows,
        },
        {
            "schema": "illustration-universal-scene-protected-final-roles/v1",
            "rows": protected_rows,
        },
        {
            "schema": "illustration-universal-scene-runtime-open-roles/v1",
            "rows": open_rows,
        },
    )


def _audit_protected_scene_facts_projection(
    scene: Mapping[str, Any],
) -> dict[str, Any]:
    contract = _mapping(scene.get("scene_contract"))
    identity = _mapping(contract.get("identity_core"))
    entities = [
        entity
        for entity in (
            identity.get("entities") if isinstance(identity.get("entities"), list) else []
        )
        if isinstance(entity, Mapping)
    ]
    capacity_records = [
        record
        for record in _mapping(scene.get("identity_core")).get(
            "capability_capacities", []
        )
        if isinstance(record, Mapping)
        and record.get("entity_id") != "scene"
    ]
    return {
        "schema": "illustration-universal-scene-protected-scene-facts/v1",
        "identity_entities": [
            {
                "entity_id": str(entity.get("entity_id")),
                "quantity": int(entity.get("quantity", 0)),
                "embodiment_profile_id": str(entity.get("embodiment_profile_id")),
            }
            for entity in sorted(
                entities, key=lambda item: str(item.get("entity_id")).encode("utf-8")
            )
        ],
        "identity_feature_fact_ids": [
            {
                "entity_id": str(entity.get("entity_id")),
                "fact_ids": _audit_utf8_sorted(
                    str(fact.get("id"))
                    for fact in entity.get("feature_facts", [])
                    if isinstance(fact, Mapping)
                ),
            }
            for entity in sorted(
                entities, key=lambda item: str(item.get("entity_id")).encode("utf-8")
            )
        ],
        "participant_bindings": _audit_plain_json(
            contract.get("participant_bindings")
        ),
        "capability_capacities": [
            {
                "entity_id": str(record.get("entity_id")),
                "resource_kind": str(record.get("resource_kind")),
                "capacity": int(record.get("capacity", 0)),
                "state": str(record.get("state")),
            }
            for record in sorted(
                capacity_records,
                key=lambda item: (
                    str(item.get("entity_id")).encode("utf-8"),
                    str(item.get("resource_kind")).encode("utf-8"),
                ),
            )
        ],
        "asserted_scene_fact_ids": _audit_utf8_sorted(
            str(fact.get("id"))
            for fact in identity.get("scene_facts", [])
            if isinstance(fact, Mapping)
        ),
        "forbidden_fact_results": [
            {"fact_id": str(fact.get("id")), "selected_truth": False}
            for fact in sorted(
                (
                    fact
                    for fact in identity.get("forbidden_facts", [])
                    if isinstance(fact, Mapping)
                ),
                key=lambda item: str(item.get("id")).encode("utf-8"),
            )
        ],
    }


def _audit_final_resource_projection(
    scene: Mapping[str, Any], scene_contract_sha256: str
) -> tuple[list[dict[str, Any]], bool]:
    _capacity_rows, capacities = _audit_resource_capacity_projection(
        scene, scene_contract_sha256
    )
    exclusive: dict[tuple[str, str], int] = {}
    shared: dict[tuple[str, str], int] = {}
    for claim in (
        scene.get("resource_claims")
        if isinstance(scene.get("resource_claims"), list)
        else []
    ):
        if not isinstance(claim, Mapping):
            raise ValueError("postselection resource claim is untyped")
        key = (str(claim.get("owner_id")), str(claim.get("resource_kind")))
        if claim.get("mode") == "exclusive":
            exclusive[key] = exclusive.get(key, 0) + int(claim.get("amount", 0))
        else:
            shared[key] = max(shared.get(key, 0), int(claim.get("amount", 0)))
    keys = set(exclusive) | set(shared)
    rows = [
        {
            "owner_scope_hash": _audit_owner_scope_hash(
                scene_contract_sha256, owner_id
            ),
            "resource_kind": resource_kind,
            "exclusive_required": exclusive.get((owner_id, resource_kind), 0),
            "shared_required": shared.get((owner_id, resource_kind), 0),
        }
        for owner_id, resource_kind in keys
    ]
    rows.sort(key=lambda row: (row["owner_scope_hash"], row["resource_kind"]))
    return rows, all(
        exclusive.get(key, 0) + shared.get(key, 0) <= capacities.get(key, 0)
        for key in keys
    )


def _audit_pixel_and_bridge_projections(
    scene: Mapping[str, Any],
    roster_rows: Sequence[Mapping[str, Any]],
    matched_prop_ids: set[str],
    assets: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], bool]:
    roster_by_instance = {
        str(row.get("instance_id")): row for row in roster_rows
    }
    atom_ids = set(roster_by_instance)
    bridges = [
        bridge
        for bridge in (
            scene.get("bridges") if isinstance(scene.get("bridges"), list) else []
        )
        if isinstance(bridge, Mapping)
    ]
    bridge_ids = {str(bridge.get("bridge_id")) for bridge in bridges}
    pixel = _mapping(scene.get("pixel_evidence_contract"))
    scale_order = ("native", "thumbnail_320px", "thumbnail_640px")
    pixel_rows: list[dict[str, Any]] = []
    item_ids: set[str] = set()
    for item in pixel.get("items", []) if isinstance(pixel.get("items"), list) else []:
        if not isinstance(item, Mapping):
            raise ValueError("pixel evidence projection contains an untyped row")
        item_id = str(item.get("item_id"))
        if item_id in item_ids:
            raise ValueError(f"duplicate pixel evidence item ID: {item_id}")
        item_ids.add(item_id)
        source_kind = str(item.get("source_kind"))
        source_id = str(item.get("source_id"))
        if source_kind == "atom" and source_id in atom_ids:
            owner_kind, owner_id = "candidate_atom", source_id
        elif source_kind == "bridge" and source_id in bridge_ids:
            owner_kind, owner_id = "bridge", source_id
        else:
            owner_kind, owner_id = "protected_scene", source_id
        scales = list(item.get("minimum_scale_ids", []))
        if (
            not scales
            or len(scales) != len(set(scales))
            or any(scale not in scale_order for scale in scales)
            or scales != [scale for scale in scale_order if scale in scales]
            or item.get("status") != "future_review_required"
            or item.get("kind") not in UNIVERSAL_PIXEL_EVIDENCE_KIND_IDS
        ):
            raise ValueError(f"pixel evidence row has an invalid closed field: {item_id}")
        pixel_rows.append(
            {
                "owner_kind": owner_kind,
                "owner_id": owner_id,
                "item_id": item_id,
                "source_kind": source_kind,
                "source_id": source_id,
                "kind": str(item.get("kind")),
                "minimum_scale_ids": scales,
                "status": "future_review_required",
            }
        )
    pixel_rows.sort(
        key=lambda row: tuple(
            str(row[key]).encode("utf-8")
            for key in (
                "owner_kind",
                "owner_id",
                "item_id",
                "source_kind",
                "source_id",
                "kind",
            )
        )
    )
    protected_atom_ids = {
        str(row.get("instance_id"))
        for row in roster_rows
        if any(bool(value) for value in _mapping(row.get("protection_flags")).values())
    }
    candidate_by_id = getattr(assets, "candidate_by_id", {})
    prop_by_id = getattr(assets, "prop_by_id", {})
    bridge_rows: list[dict[str, Any]] = []
    protected_bridge_ids: set[str] = set()
    for bridge in sorted(
        bridges, key=lambda item: str(item.get("bridge_id")).encode("utf-8")
    ):
        bridge_id = str(bridge.get("bridge_id"))
        bridge_type = str(bridge.get("bridge_type"))
        suffix = bridge_id.removeprefix(f"bridge_{bridge_type}_")
        occurrence_text, separator, owner_label = suffix.partition("_")
        if not separator or not occurrence_text.isdigit() or int(occurrence_text) <= 0:
            raise ValueError(f"bridge ID lacks owner-local occurrence: {bridge_id}")
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
            candidate_id = str(roster.get("candidate_id"))
            premise_owner = {
                "owner_kind": "candidate_atom",
                "owner_id": owner_atom,
                "source_id": candidate_id,
                "source_record_sha256": _audit_canonical_sha256(
                    candidate_by_id[candidate_id]
                ),
                "proposal_primary": bool(roster.get("proposal_primary")),
                "protection_flags": _audit_plain_json(
                    roster.get("protection_flags")
                ),
            }
            if owner_atom in protected_atom_ids:
                protected_bridge_ids.add(bridge_id)
        elif owner_label.startswith("fixed_"):
            prop_id = owner_label.removeprefix("fixed_")
            if prop_id not in matched_prop_ids:
                raise ValueError(
                    f"bridge fixed-prop owner is unauthenticated: {bridge_id}"
                )
            premise_owner = {
                "owner_kind": "fixed_prop",
                "owner_id": f"fixed_prop:{prop_id}",
                "source_id": prop_id,
                "source_record_sha256": _audit_canonical_sha256(
                    prop_by_id[prop_id]
                ),
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
            raise ValueError(f"bridge lacks an authenticated premise owner: {bridge_id}")
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
        bridge_candidate_id = str(bridge.get("candidate_id"))
        bridge_rows.append(
            {
                "bridge_id": bridge_id,
                "bridge_type": bridge_type,
                "owner_local_occurrence": int(occurrence_text),
                "candidate_id": bridge_candidate_id,
                "bridge_source_record_sha256": _audit_canonical_sha256(
                    candidate_by_id[bridge_candidate_id]
                ),
                "premise_owner": premise_owner,
                "from_node_id": str(bridge.get("from_node_id")),
                "to_node_id": str(bridge.get("to_node_id")),
                "event_edge_ids": _audit_utf8_sorted(
                    _string_list(bridge.get("event_edge_ids")) or []
                ),
                "pixel_evidence_ids": _audit_utf8_sorted(
                    _string_list(bridge.get("pixel_evidence_ids")) or []
                ),
                "pixel_owner_projection_sha256": _audit_canonical_sha256(
                    owned_pixel_payload
                ),
            }
        )
    contract_roles = {
        str(role.get("role_id")): role
        for role in _mapping(scene.get("scene_contract")).get("event_roles", [])
        if isinstance(role, Mapping)
    }
    protected_result = _mapping(contract_roles.get("result")).get("state") in {
        "fixed",
        "closed",
    }
    protected_pixel_rows = [
        row
        for row in pixel_rows
        if (
            row["owner_kind"] == "protected_scene"
            and (
                row["source_kind"] in {"core_anchor", "event"}
                or (row["source_kind"] == "consequence" and protected_result)
            )
        )
        or (
            row["owner_kind"] == "candidate_atom"
            and row["owner_id"] in protected_atom_ids
        )
        or (
            row["owner_kind"] == "bridge"
            and row["owner_id"] in protected_bridge_ids
        )
    ]
    return pixel_rows, bridge_rows, protected_pixel_rows, True


def _audit_postselection_guard_executions(
    hard_gate_snapshot: Mapping[str, Any],
    invariant_trace: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], bool]:
    source_by_id = {
        str(row.get("record_id")): row
        for row in invariant_trace.get("guard_source_contracts", [])
        if isinstance(row, Mapping)
    }
    executions: list[dict[str, Any]] = []
    old_rows = hard_gate_snapshot.get("guard_executions")
    for old in sorted(
        (row for row in old_rows if isinstance(row, Mapping))
        if isinstance(old_rows, list)
        else [],
        key=lambda row: str(row.get("guard_id")).encode("utf-8"),
    ):
        guard_id = str(old.get("guard_id"))
        source = _mapping(source_by_id.get(guard_id))
        if not source:
            raise ValueError(f"postselection guard lacks source contract: {guard_id}")
        applicable = bool(old.get("applicable"))
        if applicable:
            predicate_results = old.get("predicate_results")
            if not isinstance(predicate_results, list) or len(predicate_results) != 1:
                raise ValueError(f"applicable guard lacks one predicate proof: {guard_id}")
            predicate_result = _mapping(predicate_results[0])
            passed: bool | None = bool(predicate_result.get("passed"))
            evidence: Any = {
                "schema": "illustration-universal-scene-guard-predicate-evidence/v1",
                "predicate_id": str(source.get("predicate_id")),
                "passed": passed,
                "binding_ids": _audit_utf8_sorted(
                    _string_list(predicate_result.get("binding_ids")) or []
                ),
            }
            outcome = "pass" if passed else "block"
            reason_codes = [
                "all_guard_predicates_passed" if passed else "guard_predicate_failed"
            ]
        else:
            passed = None
            evidence = []
            outcome = "not_applicable"
            reason_codes = ["guard_not_applicable"]
        executions.append(
            {
                "guard_id": guard_id,
                "predicate_id": str(source.get("predicate_id")),
                "source_contract_sha256": str(source.get("source_contract_sha256")),
                "applicable": applicable,
                "predicate_passed": passed,
                "predicate_evidence_sha256": _audit_canonical_sha256(evidence),
                "outcome": outcome,
                "reason_codes": reason_codes,
            }
        )
    hard_gate_pass = (
        len(executions) == len(source_by_id) == 32
        and {row["guard_id"] for row in executions} == set(source_by_id)
        and any(bool(row["applicable"]) for row in executions)
        and all(row["outcome"] != "block" for row in executions)
    )
    return executions, hard_gate_pass


def _audit_selected_policy_decisions(
    scene: Mapping[str, Any],
    context_overlay_pairs: Sequence[tuple[str, str]],
    invariant_trace: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    decision_by_id = {
        str(row.get("record_id")): row
        for row in invariant_trace.get("preselection_policy_decisions", [])
        if isinstance(row, Mapping)
    }
    selected_ids = {
        f"proposal_policy__{_mapping(atom.get('parameters')).get('proposal_id')}"
        for atom in (
            scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
        )
        if isinstance(atom, Mapping)
        and "proposal_id" in _mapping(atom.get("parameters"))
    }
    selected_ids.update(
        f"context_policy__{profile_id}"
        for profile_id, _instance_id in context_overlay_pairs
    )
    missing = _audit_utf8_sorted(set(selected_ids) - set(decision_by_id))
    if missing:
        raise ValueError(f"selected policy decision source is absent: {missing}")
    return [decision_by_id[record_id] for record_id in _audit_utf8_sorted(selected_ids)]


def _audit_universal_rule_execution_rows(
    scene: Mapping[str, Any],
    invariant_trace: Mapping[str, Any],
    selected_policy_decisions: Sequence[Mapping[str, Any]],
    final_resource_pass: bool,
    universal_rules: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], bool]:
    policy_source_by_id = {
        str(row.get("record_id")): row
        for row in invariant_trace.get("policy_source_contracts", [])
        if isinstance(row, Mapping)
    }
    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, Mapping)
    ]
    bridges = [
        bridge
        for bridge in (
            scene.get("bridges") if isinstance(scene.get("bridges"), list) else []
        )
        if isinstance(bridge, Mapping)
    ]
    atom_facets = [str(atom.get("facet")) for atom in atoms]
    bridge_types = [str(bridge.get("bridge_type")) for bridge in bridges]
    bridge_pixel_pass = all(
        bool(_string_list(bridge.get("pixel_evidence_ids"))) for bridge in bridges
    )
    selected_band = str(
        _mapping(scene.get("semantic_distance_trace")).get("selected_band")
    )
    if selected_band == "middle":
        visible_bridge_violation = not (
            len(set(bridge_types)) >= 2
            and bool(set(bridge_types) & UNIVERSAL_BRIDGE_ENTRY_TYPES)
            and bool(set(bridge_types) & UNIVERSAL_BRIDGE_EXIT_TYPES)
            and bridge_pixel_pass
        )
    elif selected_band == "far":
        visible_bridge_violation = not (
            len(set(bridge_types)) >= 3
            and bool(set(bridge_types) & UNIVERSAL_BRIDGE_ENTRY_TYPES)
            and bool(set(bridge_types) & UNIVERSAL_BRIDGE_MEDIATION_TYPES)
            and bool(set(bridge_types) & UNIVERSAL_BRIDGE_EXIT_TYPES)
            and bridge_pixel_pass
        )
    else:
        visible_bridge_violation = False
    contract = _mapping(scene.get("scene_contract"))
    prop_slot = next(
        (
            slot
            for slot in contract.get("slot_states", [])
            if isinstance(slot, Mapping) and slot.get("slot_id") == "prop"
        ),
        {},
    )
    distance = _mapping(scene.get("semantic_distance_trace"))
    violations = {
        "rule_fixed_identity_precedence": False,
        "rule_closed_prop": (
            _mapping(prop_slot).get("state") == "closed"
            and any(facet in {"prop", "prop_state"} for facet in atom_facets)
        ),
        "rule_exactly_one_event": scene.get("selected_event") is None,
        "rule_resource_capacity": not final_resource_pass,
        "rule_visible_middle_far_bridge": visible_bridge_violation,
        "rule_remote_budget": int(distance.get("optional_remote_count", 0)) > 1,
        "rule_policy_independent_of_creativity": any(
            row.get("outcome") != "pass" for row in selected_policy_decisions
        ),
    }
    rows: list[dict[str, Any]] = []
    for rule in sorted(
        (row for row in universal_rules if isinstance(row, Mapping)),
        key=lambda row: str(row.get("id")).encode("utf-8"),
    ):
        rule_id = str(rule.get("id"))
        if rule_id not in violations:
            raise ValueError(f"unimplemented universal rule: {rule_id}")
        violated = bool(violations[rule_id])
        source = _mapping(policy_source_by_id.get(f"universal_rule__{rule_id}"))
        rows.append(
            {
                "rule_id": rule_id,
                "source_contract_sha256": str(source.get("source_contract_sha256")),
                "violated": violated,
                "outcome": "block" if violated else "pass",
                "reason_codes": [
                    str(rule.get("reason_code")) if violated else "rule_satisfied"
                ],
            }
        )
    return rows, all(row["outcome"] == "pass" for row in rows)


def _audit_postselection_cardinality_rows(
    scene: Mapping[str, Any],
    roster_rows: Sequence[Mapping[str, Any]],
    invariant_trace: Mapping[str, Any],
    context_carrier_candidate_ids: set[str],
) -> tuple[list[dict[str, Any]], bool, str]:
    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, Mapping)
    ]
    event = _mapping(scene.get("selected_event"))
    runtime_roles = {
        str(role.get("role_id")): role
        for role in event.get("roles", [])
        if isinstance(role, Mapping)
    }
    edge_by_id = {
        str(edge.get("edge_id")): edge
        for edge in event.get("spine_edges", [])
        if isinstance(edge, Mapping)
    }
    event_root_count = 1 if scene.get("selected_event") is not None else 0
    optional_prop_count = sum(
        row.get("facet_id") == "prop"
        and not bool(_mapping(row.get("protection_flags")).get("mandatory_literal"))
        and not bool(row.get("proposal_primary"))
        for row in roster_rows
    )
    orphan_count = sum(
        not (
            len(_string_list(atom.get("event_edge_ids")) or []) == 1
            and str((_string_list(atom.get("event_edge_ids")) or [""])[0]) in edge_by_id
            and _mapping(
                edge_by_id.get(str((_string_list(atom.get("event_edge_ids")) or [""])[0]))
            ).get("from_node_id")
            == "event_01"
            and _mapping(
                edge_by_id.get(str((_string_list(atom.get("event_edge_ids")) or [""])[0]))
            ).get("to_node_id")
            == atom.get("instance_id")
        )
        for atom in atoms
    )
    distance = _mapping(scene.get("semantic_distance_trace"))
    optional_remote = int(distance.get("optional_remote_count", 0))
    observed = {
        "display_bundles": int(
            any(atom.get("facet") in {"expression", "perceived_affect"} for atom in atoms)
        ),
        "display_primitives_per_bundle": sum(
            atom.get("facet") in {"expression", "perceived_affect"} for atom in atoms
        ),
        "event_spines": event_root_count,
        "gestures": sum(atom.get("facet") == "gesture" for atom in atoms),
        "optional_props": optional_prop_count,
        "orphan_atoms": orphan_count,
        "perceived_affect_hypotheses": sum(
            atom.get("facet") == "perceived_affect" for atom in atoms
        ),
        "phases": len({event.get("phase_id")}) if event.get("phase_id") is not None else 0,
        "pose_support_solutions": sum(atom.get("facet") == "pose" for atom in atoms),
        "primary_actions": int(_mapping(runtime_roles.get("action")).get("value_id") is not None),
        "primary_environment_roles": int(
            _mapping(runtime_roles.get("location")).get("value_id") is not None
        ),
        "relation_topologies": sum(atom.get("facet") == "relation" for atom in atoms),
        "remote_or_high_load_optional_premises": optional_remote,
        "second_independent_premises": max(0, event_root_count - 1),
        "context_profile_carriers": sum(
            str(atom.get("candidate_id")) in context_carrier_candidate_ids
            for atom in atoms
        ),
        "global_optional_remote": optional_remote,
        "selected_resource_claims_total": len(
            scene.get("resource_claims")
            if isinstance(scene.get("resource_claims"), list)
            else []
        ),
        "selected_visual_atoms_total": len(atoms),
    }
    limits = [
        row
        for row in invariant_trace.get("cardinality_limits", [])
        if isinstance(row, Mapping)
        and row.get("evaluation_stage") == "postselection_scene"
    ]
    rows = [
        {
            "limit_id": str(limit.get("record_id")),
            "observed": int(observed[str(limit.get("metric_id"))]),
            "minimum": int(limit.get("minimum", 0)),
            "maximum": int(limit.get("maximum", 0)),
            "fits": int(limit.get("minimum", 0))
            <= int(observed[str(limit.get("metric_id"))])
            <= int(limit.get("maximum", 0)),
        }
        for limit in limits
    ]
    invariant_rows = _audit_plain_json(rows)
    for row in invariant_rows:
        if row["limit_id"] in {
            "compatibility_budget__remote_or_high_load_optional_premises",
            "runtime_limit__global_optional_remote",
        }:
            row["observed"] = None
    return rows, all(row["fits"] for row in rows), _audit_canonical_sha256(
        invariant_rows
    )


def _audit_expected_postselection_run_trace(
    scene: Mapping[str, Any],
    assets: Any,
    semantic_bindings: Mapping[str, Any],
) -> dict[str, Any]:
    invariant_trace = _mapping(scene.get("creativity_invariant_trace"))
    if not invariant_trace:
        raise ValueError("postselection replay lacks the invariant trace")
    matched_prop_ids = _audit_matched_catalog_prop_ids(scene, assets)
    context_overlay_pairs = _audit_expected_context_overlay_pairs(
        scene, assets, matched_prop_ids
    )
    roster_payload, roster_rows = _audit_selected_candidate_roster_projection(
        scene, assets, context_overlay_pairs
    )
    protected_roster, proposal_roster, optional_roster = (
        _audit_candidate_roster_subprojections(roster_rows)
    )
    contract_roles, protected_roles, runtime_open_roles = (
        _audit_role_projection_payloads(scene, assets)
    )
    protected_scene_facts = _audit_protected_scene_facts_projection(scene)
    scene_contract_sha256 = _audit_canonical_sha256(
        _mapping(scene.get("scene_contract"))
    )
    resource_footprint, resource_pass = _audit_final_resource_projection(
        scene, scene_contract_sha256
    )
    pixel_rows, bridge_rows, protected_pixel_rows, pixel_pass = (
        _audit_pixel_and_bridge_projections(
            scene, roster_rows, matched_prop_ids, assets
        )
    )
    active_context_ids = _audit_utf8_sorted(
        profile_id for profile_id, _instance_id in context_overlay_pairs
    )
    active_context_payload = {
        "schema": "illustration-universal-scene-active-context-profiles/v1",
        "profile_ids": active_context_ids,
    }
    atoms = [
        atom
        for atom in (scene.get("atoms") if isinstance(scene.get("atoms"), list) else [])
        if isinstance(atom, Mapping)
    ]
    facet_multiset = [
        {
            "facet_id": facet_id,
            "count": sum(str(atom.get("facet")) == facet_id for atom in atoms),
        }
        for facet_id in _audit_utf8_sorted(UNIVERSAL_FACET_IDS)
    ]
    distance = _mapping(scene.get("semantic_distance_trace"))
    semantic_distance = {
        "selected_candidate_distance_vectors": [
            {
                "selection_ordinal": index,
                "instance_id": str(atom.get("instance_id")),
                "candidate_id": str(atom.get("candidate_id")),
                "vector": _audit_plain_json(atom.get("distance_vector")),
            }
            for index, atom in enumerate(atoms)
        ],
        "aggregate_distance_vector": _audit_plain_json(distance.get("vector")),
        "selected_distance_band": str(distance.get("selected_band")),
        "fixed_remote_count": int(distance.get("fixed_remote_count", 0)),
        "global_optional_remote_max": 1,
    }
    remote_instance_ids = set(_string_list(distance.get("remote_atom_ids")) or [])
    optional_remote_projection = {
        "remote_candidate_ids": _audit_utf8_sorted(
            str(atom.get("candidate_id"))
            for atom in atoms
            if atom.get("instance_id") in remote_instance_ids
        ),
        "optional_remote_count": int(distance.get("optional_remote_count", 0)),
    }
    pixel_kind_payload = {
        "schema": "illustration-universal-scene-pixel-kind-multiset/v1",
        "rows": [
            {
                "kind": kind,
                "count": sum(row["kind"] == kind for row in pixel_rows),
            }
            for kind in _audit_utf8_sorted(UNIVERSAL_PIXEL_EVIDENCE_KIND_IDS)
        ],
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
        atom for atom in atoms if "proposal_id" in _mapping(atom.get("parameters"))
    ]
    if len(proposal_atoms) > 1:
        raise ValueError("postselection trace found multiple proposal primaries")
    proposal_by_id = getattr(assets, "proposal_by_id", {})
    selected_profile = (
        proposal_by_id.get(
            str(_mapping(proposal_atoms[0].get("parameters")).get("proposal_id"))
        )
        if proposal_atoms and isinstance(proposal_by_id, Mapping)
        else None
    )
    raw_candidates = getattr(assets, "candidates", {})
    context_profiles = (
        raw_candidates.get("context_distance_profiles", [])
        if isinstance(raw_candidates, Mapping)
        else []
    )
    context_carrier_candidate_ids = {
        str(profile.get("carrier_candidate_id"))
        for profile in context_profiles
        if isinstance(profile, Mapping)
    }
    selected_projection = {
        "fixed_contract_projection_sha256": _audit_canonical_sha256(
            _audit_fixed_contract_projection(scene)
        ),
        "contract_role_projection_sha256": _audit_canonical_sha256(contract_roles),
        "protected_final_role_projection_sha256": _audit_canonical_sha256(
            protected_roles
        ),
        "protected_scene_facts_sha256": _audit_canonical_sha256(
            protected_scene_facts
        ),
        "runtime_open_role_projection_sha256": _audit_canonical_sha256(
            runtime_open_roles
        ),
        "selected_semantic_family_signature": (
            str(selected_profile.get("semantic_family_signature"))
            if isinstance(selected_profile, Mapping)
            else None
        ),
        "selected_proposal_profile_sha256": (
            hashlib.sha256(str(selected_profile.get("id")).encode("utf-8")).hexdigest()
            if isinstance(selected_profile, Mapping)
            else None
        ),
        "selected_candidate_roster_sha256": _audit_canonical_sha256(roster_payload),
        "protected_candidate_roster_sha256": _audit_canonical_sha256(
            protected_roster
        ),
        "proposal_primary_roster_sha256": _audit_canonical_sha256(proposal_roster),
        "optional_candidate_roster_sha256": _audit_canonical_sha256(optional_roster),
        "active_context_profile_ids_sha256": _audit_canonical_sha256(
            active_context_payload
        ),
        "selected_atom_count": len(atoms),
        "selected_facet_multiset": facet_multiset,
        "aggregate_resource_footprint": resource_footprint,
        "resource_claim_count": len(
            scene.get("resource_claims")
            if isinstance(scene.get("resource_claims"), list)
            else []
        ),
        "mandatory_literal_atom_count": sum(
            bool(_mapping(row.get("protection_flags")).get("mandatory_literal"))
            for row in roster_rows
        ),
        "context_profile_carrier_count": sum(
            str(atom.get("candidate_id")) in context_carrier_candidate_ids
            for atom in atoms
        ),
        "fixed_remote_count": int(distance.get("fixed_remote_count", 0)),
        "optional_remote_count": int(distance.get("optional_remote_count", 0)),
        "global_optional_remote_max": 1,
        "semantic_distance_sha256": _audit_canonical_sha256(semantic_distance),
        "optional_remote_projection_sha256": _audit_canonical_sha256(
            optional_remote_projection
        ),
        "bridge_topology_sha256": _audit_canonical_sha256(bridge_rows),
        "pixel_evidence_chain_sha256": _audit_canonical_sha256(pixel_chain_payload),
        "pixel_evidence_count": len(pixel_rows),
        "pixel_kind_multiset_sha256": _audit_canonical_sha256(pixel_kind_payload),
        "protected_pixel_evidence_sha256": _audit_canonical_sha256(
            protected_pixel_payload
        ),
        "pixel_evidence_contract_pass": pixel_pass,
    }
    expected_hard_gate, hard_gate_failures = _audit_expected_hard_gate_snapshot(
        scene, assets, semantic_bindings
    )
    if hard_gate_failures:
        raise ValueError(
            f"postselection replay found {len(hard_gate_failures)} hard-gate source failures"
        )
    guard_executions, hard_gate_pass = _audit_postselection_guard_executions(
        expected_hard_gate, invariant_trace
    )
    selected_policy_decisions = _audit_selected_policy_decisions(
        scene, context_overlay_pairs, invariant_trace
    )
    compatibility = getattr(assets, "compatibility", {})
    universal_rules_source = (
        compatibility.get("universal_rules", [])
        if isinstance(compatibility, Mapping)
        else []
    )
    universal_rules, universal_rules_pass = _audit_universal_rule_execution_rows(
        scene,
        invariant_trace,
        selected_policy_decisions,
        resource_pass,
        universal_rules_source,
    )
    cardinality_rows, cardinality_pass, cardinality_invariant_sha = (
        _audit_postselection_cardinality_rows(
            scene,
            roster_rows,
            invariant_trace,
            context_carrier_candidate_ids,
        )
    )
    policy_gate_pass = (
        all(row.get("outcome") == "pass" for row in selected_policy_decisions)
        and universal_rules_pass
    )
    trace: dict[str, Any] = {
        "schema": UNIVERSAL_POSTSELECTION_TRACE_SCHEMA,
        "invariant_trace_sha256": str(invariant_trace.get("trace_sha256")),
        "guard_source_contracts_sha256": str(
            invariant_trace.get("guard_source_contracts_sha256")
        ),
        "selected_projection": selected_projection,
        "guard_executions": guard_executions,
        "guard_executions_sha256": _audit_canonical_sha256(guard_executions),
        "hard_gate_pass": hard_gate_pass,
        "universal_rule_executions": universal_rules,
        "universal_rule_executions_sha256": _audit_canonical_sha256(universal_rules),
        "postselection_cardinality_decisions": cardinality_rows,
        "postselection_cardinality_decisions_sha256": _audit_canonical_sha256(
            cardinality_rows
        ),
        "postselection_cardinality_invariant_sha256": cardinality_invariant_sha,
        "postselection_resource_pass": resource_pass,
        "policy_gate_pass": policy_gate_pass,
        "cardinality_gate_pass": cardinality_pass,
        "complete_trace": True,
    }
    trace["trace_sha256"] = _audit_canonical_sha256(trace)
    return trace


def _audit_postselection_run_trace_failures(
    scene: Mapping[str, Any],
    assets: Any,
    semantic_bindings: Mapping[str, Any],
) -> list[dict[str, Any]]:
    try:
        expected = _audit_expected_postselection_run_trace(
            scene, assets, semantic_bindings
        )
    except (KeyError, TypeError, ValueError) as exc:
        return [
            issue(
                "universal_postselection_trace",
                "independent postselection replay could not derive the complete frozen trace",
                error=str(exc),
            )
        ]
    actual = _mapping(scene.get("postselection_run_trace"))
    if actual == expected:
        return []
    return [
        issue(
            "universal_postselection_trace",
            "postselection trace must exactly equal independent raw-asset and selected-scene replay",
            mismatched_fields=sorted(
                key
                for key in UNIVERSAL_POSTSELECTION_TRACE_KEYS
                if actual.get(key) != expected.get(key)
            ),
            expected_trace_sha256=expected.get("trace_sha256"),
            actual_trace_sha256=actual.get("trace_sha256"),
        )
    ]


def _audit_frozen_trace_shape_failures(
    scene: Mapping[str, Any], request_text: str, scene_contract_sha256: Any
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    invariant_value = scene.get("creativity_invariant_trace")
    failures.extend(
        _exact_object_keys(
            invariant_value,
            UNIVERSAL_CREATIVITY_INVARIANT_KEYS,
            check="universal_creativity_invariant",
            object_name="universal_scene.creativity_invariant_trace",
        )
    )
    invariant = _mapping(invariant_value)
    if invariant:
        if invariant.get("schema") != UNIVERSAL_CREATIVITY_INVARIANT_SCHEMA:
            failures.append(
                issue(
                    "universal_creativity_invariant",
                    "creativity-invariant trace schema is outside the frozen contract",
                    expected=UNIVERSAL_CREATIVITY_INVARIANT_SCHEMA,
                    actual=invariant.get("schema"),
                )
            )
        expected_request_sha = hashlib.sha256(request_text.encode("utf-8")).hexdigest()
        if invariant.get("request_sha256") != expected_request_sha:
            failures.append(
                issue(
                    "universal_creativity_invariant",
                    "invariant request hash must bind the exact request bytes",
                    expected=expected_request_sha,
                    actual=invariant.get("request_sha256"),
                )
            )
        if invariant.get("scene_contract_sha256") != scene_contract_sha256:
            failures.append(
                issue(
                    "universal_creativity_invariant",
                    "invariant trace must bind the embedded scene contract",
                    expected=scene_contract_sha256,
                    actual=invariant.get("scene_contract_sha256"),
                )
            )
        failures.extend(
            _exact_object_keys(
                invariant.get("asset_hashes"),
                UNIVERSAL_HARD_GATE_ASSET_HASH_KEYS,
                check="universal_creativity_invariant",
                object_name="creativity_invariant_trace.asset_hashes",
            )
        )
        failures.extend(
            _exact_object_keys(
                invariant.get("inventory"),
                UNIVERSAL_CREATIVITY_INVENTORY_KEYS,
                check="universal_creativity_invariant",
                object_name="creativity_invariant_trace.inventory",
            )
        )
        inventory = _mapping(invariant.get("inventory"))
        for field in UNIVERSAL_CREATIVITY_INVENTORY_KEYS:
            values = _unique_string_list(inventory.get(field))
            if values is None or values != _audit_utf8_sorted(values):
                failures.append(
                    issue(
                        "universal_creativity_invariant",
                        "invariant scalar inventory arrays must be UTF-8-byte-sorted and unique",
                        field=field,
                        actual=inventory.get(field),
                    )
                )
        scalar_arrays = (
            "reason_code_registry",
            "eligible_candidate_ids",
            "matched_prop_sense_hashes",
        )
        for field in scalar_arrays:
            values = _unique_string_list(invariant.get(field))
            if values is None or values != _audit_utf8_sorted(values):
                failures.append(
                    issue(
                        "universal_creativity_invariant",
                        "invariant scalar arrays must be UTF-8-byte-sorted and unique",
                        field=field,
                        actual=invariant.get(field),
                    )
                )
        for field, keys in (
            ("eligible_proposals", UNIVERSAL_INVARIANT_ELIGIBLE_PROPOSAL_KEYS),
            ("rejected_proposals", UNIVERSAL_INVARIANT_REJECTED_SOURCE_KEYS),
            ("rejected_candidates", UNIVERSAL_INVARIANT_REJECTED_SOURCE_KEYS),
            ("policy_source_contracts", UNIVERSAL_POLICY_SOURCE_CONTRACT_KEYS),
            (
                "preselection_policy_decisions",
                UNIVERSAL_PRESELECTION_POLICY_DECISION_KEYS,
            ),
            ("resource_capacities", UNIVERSAL_RESOURCE_CAPACITY_ROW_KEYS),
            ("resource_feasibility", UNIVERSAL_PRESELECTION_FEASIBILITY_KEYS),
            ("cardinality_limits", UNIVERSAL_CARDINALITY_LIMIT_KEYS),
            (
                "cardinality_feasibility",
                UNIVERSAL_CARDINALITY_FEASIBILITY_KEYS,
            ),
            ("guard_source_contracts", UNIVERSAL_GUARD_SOURCE_CONTRACT_KEYS),
        ):
            rows = invariant.get(field)
            if not isinstance(rows, list):
                failures.append(
                    issue(
                        "universal_creativity_invariant",
                        "invariant trace record inventory must be a typed list",
                        field=field,
                        actual=rows,
                    )
                )
                continue
            for index, row in enumerate(rows):
                failures.extend(
                    _exact_object_keys(
                        row,
                        keys,
                        check="universal_creativity_invariant",
                        object_name=f"creativity_invariant_trace.{field}[{index}]",
                    )
                )
        if invariant.get("complete_trace") is not True:
            failures.append(
                issue(
                    "universal_creativity_invariant",
                    "creativity-invariant trace must be marked complete",
                )
            )
        expected_trace_sha = _audit_canonical_sha256(
            {key: value for key, value in invariant.items() if key != "trace_sha256"}
        )
        if invariant.get("trace_sha256") != expected_trace_sha:
            failures.append(
                issue(
                    "universal_creativity_invariant",
                    "creativity-invariant self hash is not canonical",
                    expected=expected_trace_sha,
                    actual=invariant.get("trace_sha256"),
                )
            )

    postselection_value = scene.get("postselection_run_trace")
    failures.extend(
        _exact_object_keys(
            postselection_value,
            UNIVERSAL_POSTSELECTION_TRACE_KEYS,
            check="universal_postselection_trace",
            object_name="universal_scene.postselection_run_trace",
        )
    )
    postselection = _mapping(postselection_value)
    if postselection:
        if postselection.get("schema") != UNIVERSAL_POSTSELECTION_TRACE_SCHEMA:
            failures.append(
                issue(
                    "universal_postselection_trace",
                    "postselection trace schema is outside the frozen contract",
                    expected=UNIVERSAL_POSTSELECTION_TRACE_SCHEMA,
                    actual=postselection.get("schema"),
                )
            )
        if postselection.get("invariant_trace_sha256") != invariant.get(
            "trace_sha256"
        ):
            failures.append(
                issue(
                    "universal_postselection_trace",
                    "postselection trace must bind the exact invariant trace",
                    expected=invariant.get("trace_sha256"),
                    actual=postselection.get("invariant_trace_sha256"),
                )
            )
        failures.extend(
            _exact_object_keys(
                postselection.get("selected_projection"),
                UNIVERSAL_POSTSELECTION_SELECTED_PROJECTION_KEYS,
                check="universal_postselection_trace",
                object_name="postselection_run_trace.selected_projection",
            )
        )
        for field, keys in (
            ("guard_executions", UNIVERSAL_POSTSELECTION_GUARD_EXECUTION_KEYS),
            ("universal_rule_executions", UNIVERSAL_RULE_EXECUTION_KEYS),
            (
                "postselection_cardinality_decisions",
                UNIVERSAL_POSTSELECTION_CARDINALITY_KEYS,
            ),
        ):
            rows = postselection.get(field)
            if not isinstance(rows, list):
                failures.append(
                    issue(
                        "universal_postselection_trace",
                        "postselection execution inventory must be a typed list",
                        field=field,
                        actual=rows,
                    )
                )
                continue
            for index, row in enumerate(rows):
                failures.extend(
                    _exact_object_keys(
                        row,
                        keys,
                        check="universal_postselection_trace",
                        object_name=f"postselection_run_trace.{field}[{index}]",
                    )
                )
        for rows_field, digest_field in (
            ("guard_executions", "guard_executions_sha256"),
            ("universal_rule_executions", "universal_rule_executions_sha256"),
            (
                "postselection_cardinality_decisions",
                "postselection_cardinality_decisions_sha256",
            ),
        ):
            rows = postselection.get(rows_field)
            if isinstance(rows, list) and postselection.get(
                digest_field
            ) != _audit_canonical_sha256(rows):
                failures.append(
                    issue(
                        "universal_postselection_trace",
                        "postselection execution digest must bind its exact rows",
                        field=digest_field,
                    )
                )
        if postselection.get("complete_trace") is not True:
            failures.append(
                issue(
                    "universal_postselection_trace",
                    "postselection trace must be marked complete",
                )
            )
        expected_trace_sha = _audit_canonical_sha256(
            {
                key: value
                for key, value in postselection.items()
                if key != "trace_sha256"
            }
        )
        if postselection.get("trace_sha256") != expected_trace_sha:
            failures.append(
                issue(
                    "universal_postselection_trace",
                    "postselection self hash is not canonical",
                    expected=expected_trace_sha,
                    actual=postselection.get("trace_sha256"),
                )
            )
    return failures


def _audit_exact_hard_gate_replay_failures(
    scene: Mapping[str, Any],
    assets: Any,
    semantic_bindings: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Compare the untrusted snapshot to an asset/contract-derived snapshot."""

    try:
        expected, failures = _audit_expected_hard_gate_snapshot(
            scene, assets, semantic_bindings
        )
    except (KeyError, TypeError, ValueError) as exc:
        return [
            issue(
                "universal_hard_gate",
                "independent hard-gate replay could not derive a complete typed snapshot",
                error=str(exc),
            )
        ]
    actual = _mapping(scene.get("hard_gate_snapshot"))
    if actual != expected:
        failures.append(
            issue(
                "universal_hard_gate",
                "hard-gate snapshot must exactly equal independent raw-asset and embedded-contract replay",
                mismatched_fields=sorted(
                    key
                    for key in UNIVERSAL_HARD_GATE_KEYS
                    if actual.get(key) != expected.get(key)
                ),
                expected_snapshot_sha256=expected.get("snapshot_sha256"),
                actual_snapshot_sha256=actual.get("snapshot_sha256"),
            )
        )
    return failures


def _runtime_universal_revalidation_failures(
    pack: Mapping[str, Any],
    scene: Mapping[str, Any],
    request_text: str,
) -> list[dict[str, Any]]:
    """Re-evaluate v3 selection against raw-byte-bound sibling assets."""

    script_dir = str(Path(__file__).resolve().parent)
    inserted_path = script_dir not in sys.path
    if inserted_path:
        sys.path.insert(0, script_dir)
    try:
        import universal_scene_runtime as universal_runtime
    except (ImportError, OSError, SyntaxError) as exc:
        return [issue("universal_asset_binding", "universal runtime revalidation is unavailable", error=str(exc))]
    finally:
        if inserted_path and sys.path and sys.path[0] == script_dir:
            sys.path.pop(0)
    try:
        assets = universal_runtime.load_universal_scene_assets()
        pack_hashes = _mapping(pack.get("asset_hashes"))
        expected_hashes = dict(assets.asset_hashes)
        actual_hashes = {key: pack_hashes.get(key) for key in expected_hashes}
        if actual_hashes != expected_hashes:
            return [
                issue(
                    "universal_asset_binding",
                    "pack universal hashes do not match validated sibling asset bytes",
                    expected=expected_hashes,
                    actual=actual_hashes,
                )
            ]
        snapshot = _mapping(scene.get("hard_gate_snapshot"))
        snapshot_hashes = _mapping(snapshot.get("asset_hashes"))
        if snapshot_hashes != expected_hashes:
            return [
                issue(
                    "universal_asset_binding",
                    "hard-gate snapshot hashes do not match validated sibling asset bytes",
                    expected=expected_hashes,
                    actual=snapshot_hashes,
                )
            ]
        raw_semantic_bindings = getattr(assets, "semantic_bindings", {})
        semantic_bindings = (
            dict(raw_semantic_bindings)
            if isinstance(raw_semantic_bindings, Mapping)
            else {}
        )
        quiet_context_failures = _audit_quiet_context_zero_theme_failures(assets)
        if quiet_context_failures:
            return quiet_context_failures
        contract_effect_failures = _audit_contract_effect_projection_failures(
            scene,
            request_text,
            semantic_bindings,
        )
        if contract_effect_failures:
            return contract_effect_failures
        context_literal_failures = _audit_context_literal_profile_failures(
            scene,
            request_text,
            semantic_bindings,
        )
        if context_literal_failures:
            return context_literal_failures
        semantic_anchor_failures = _audit_semantic_anchor_authority_failures(
            scene,
            semantic_bindings,
        )
        if semantic_anchor_failures:
            return semantic_anchor_failures
        embodiment_projection_failures = _audit_embodiment_projection_failures(
            scene,
            assets,
        )
        if embodiment_projection_failures:
            return embodiment_projection_failures
        phase_projection_failures = _audit_phase_projection_failures(scene)
        if phase_projection_failures:
            return phase_projection_failures
        proposal_trace_failures = _audit_proposal_trace_failures(scene, assets)
        if proposal_trace_failures:
            return proposal_trace_failures
        fixed_prop_candidate_failures = _audit_fixed_prop_candidate_boundary_failures(
            scene,
            assets,
        )
        if fixed_prop_candidate_failures:
            return fixed_prop_candidate_failures
        literal_realization_failures = _audit_literal_visual_realization_failures(
            scene,
            request_text,
            assets,
            semantic_bindings,
        )
        if literal_realization_failures:
            return literal_realization_failures
        role_source_failures = _audit_runtime_selected_role_source_failures(
            scene,
            assets,
        )
        if role_source_failures:
            return role_source_failures
        invariant_trace_failures = _audit_creativity_invariant_trace_failures(
            scene,
            request_text,
            assets,
            semantic_bindings,
        )
        if invariant_trace_failures:
            return invariant_trace_failures
        exact_hard_gate_failures = _audit_exact_hard_gate_replay_failures(
            scene,
            assets,
            semantic_bindings,
        )
        if exact_hard_gate_failures:
            return exact_hard_gate_failures
        postselection_trace_failures = _audit_postselection_run_trace_failures(
            scene,
            assets,
            semantic_bindings,
        )
        if postselection_trace_failures:
            return postselection_trace_failures
        effect_registry = _mapping(semantic_bindings.get("semantic_effect_registry"))
        expected_registry_sha = hashlib.sha256(
            canonical_json(effect_registry).encode("utf-8")
        ).hexdigest()
        if snapshot.get("semantic_effect_registry_sha256") != expected_registry_sha:
            return [
                issue(
                    "universal_asset_binding",
                    "hard-gate semantic registry digest does not match the validated data-owned registry",
                    expected=expected_registry_sha,
                    actual=snapshot.get("semantic_effect_registry_sha256"),
                )
            ]
        if snapshot.get("source_coverage") != effect_registry.get("counts"):
            return [
                issue(
                    "universal_asset_binding",
                    "hard-gate source coverage does not match the validated semantic registry",
                    expected=effect_registry.get("counts"),
                    actual=snapshot.get("source_coverage"),
                )
            ]
        registry_profiles = effect_registry.get("profiles")
        registry_source_keys: set[tuple[str, str]] = set()
        for profile in (
            registry_profiles if isinstance(registry_profiles, list) else []
        ):
            if not isinstance(profile, dict):
                continue
            source_key = (str(profile.get("source_kind")), str(profile.get("source_id")))
            registry_source_keys.add(source_key)
            if profile.get("effect_ids") != []:
                return [
                    issue(
                        "universal_asset_binding",
                        "the independently reviewed v1 selectable-source registry must remain effect-empty",
                        source_kind=source_key[0],
                        source_id=source_key[1],
                        actual=profile.get("effect_ids"),
                    )
                ]
        selected_registry_source_keys = {
            (str(ref.get("source_kind")), str(ref.get("source_id")))
            for item in (
                snapshot.get("selected_source_refs")
                if isinstance(snapshot.get("selected_source_refs"), list)
                else []
            )
            if isinstance(item, dict)
            for ref in (
                item.get("source_profile_refs")
                if isinstance(item.get("source_profile_refs"), list)
                else []
            )
            if isinstance(ref, dict)
        }
        unknown_selected_sources = sorted(
            selected_registry_source_keys - registry_source_keys
        )
        if unknown_selected_sources:
            return [
                issue(
                    "universal_asset_binding",
                    "hard-gate selected source is absent from the validated semantic registry",
                    unknown=[list(item) for item in unknown_selected_sources],
                )
            ]
        selection_trace = _mapping(scene.get("selection_trace"))
        eligible_ids_by_facet = _mapping(
            selection_trace.get("eligible_candidate_ids_by_facet")
        )
        traced_eligible_ids: set[str] = set()
        invalid_eligible_ids: list[tuple[str, str]] = []
        for facet in sorted(UNIVERSAL_FACET_IDS):
            for candidate_id in (
                eligible_ids_by_facet.get(facet)
                if isinstance(eligible_ids_by_facet.get(facet), list)
                else []
            ):
                candidate = assets.candidate_by_id.get(str(candidate_id))
                if (
                    not isinstance(candidate, Mapping)
                    or candidate.get("role") != "visual_atom"
                    or candidate.get("facet") != facet
                ):
                    invalid_eligible_ids.append((facet, str(candidate_id)))
                traced_eligible_ids.add(str(candidate_id))
        rejected_candidate_ids = {
            str(rejection.get("candidate_id"))
            for rejection in (
                selection_trace.get("candidate_rejections")
                if isinstance(selection_trace.get("candidate_rejections"), list)
                else []
            )
            if isinstance(rejection, dict)
            and _is_nonempty_string(rejection.get("candidate_id"))
        }
        invalid_rejected_ids = sorted(
            candidate_id
            for candidate_id in rejected_candidate_ids
            if not isinstance(assets.candidate_by_id.get(candidate_id), Mapping)
            or assets.candidate_by_id[candidate_id].get("role") != "visual_atom"
        )
        all_visual_ids = {
            str(candidate_id)
            for candidate_id, candidate in assets.candidate_by_id.items()
            if isinstance(candidate, Mapping) and candidate.get("role") == "visual_atom"
        }
        if (
            invalid_eligible_ids
            or invalid_rejected_ids
            or traced_eligible_ids & rejected_candidate_ids
            or traced_eligible_ids | rejected_candidate_ids != all_visual_ids
        ):
            return [
                issue(
                    "universal_asset_binding",
                    "selection trace must exactly partition every validated visual candidate by typed facet eligibility",
                    invalid_eligible=[list(item) for item in invalid_eligible_ids],
                    invalid_rejected=invalid_rejected_ids,
                    missing=sorted(all_visual_ids - traced_eligible_ids - rejected_candidate_ids),
                    overlap=sorted(traced_eligible_ids & rejected_candidate_ids),
                    extra=sorted((traced_eligible_ids | rejected_candidate_ids) - all_visual_ids),
                )
            ]
        raw_guard_profiles = semantic_bindings.get("guard_execution_profiles")
        guard_profile_map = {
            str(profile.get("guard_id")): str(profile.get("predicate_id"))
            for profile in (
                raw_guard_profiles if isinstance(raw_guard_profiles, list) else []
            )
            if isinstance(profile, dict)
        }
        if guard_profile_map != UNIVERSAL_GUARD_EXECUTION_PREDICATES:
            return [
                issue(
                    "universal_asset_binding",
                    "data-owned guard execution profiles do not match the closed all-32 evaluator",
                    expected=UNIVERSAL_GUARD_EXECUTION_PREDICATES,
                    actual=guard_profile_map,
                )
            ]
        hard_gate_guard_by_id = {
            str(record.get("guard_id")): record
            for record in (
                snapshot.get("guard_executions")
                if isinstance(snapshot.get("guard_executions"), list)
                else []
            )
            if isinstance(record, dict)
            and _is_nonempty_string(record.get("guard_id"))
        }
        for guard_id in sorted(UNIVERSAL_GUARD_EXECUTION_PREDICATES):
            candidate = assets.candidate_by_id.get(guard_id)
            record = hard_gate_guard_by_id.get(guard_id)
            if not isinstance(candidate, Mapping) or not isinstance(record, Mapping):
                return [
                    issue(
                        "universal_asset_binding",
                        "hard-gate guard is missing its validated data-owned candidate",
                        guard_id=guard_id,
                    )
                ]
            raw_runtime_contract = candidate.get("runtime_contract")
            runtime_contract = (
                dict(raw_runtime_contract)
                if isinstance(raw_runtime_contract, Mapping)
                else {}
            )
            source_contract = {
                "guard_id": str(candidate.get("id")),
                "role": str(candidate.get("role")),
                "research_topic_ids": list(candidate.get("research_topic_ids", [])),
                "provenance_record_ids": list(candidate.get("provenance_record_ids", [])),
                "stage": str(runtime_contract.get("stage")),
                "violation_code": str(runtime_contract.get("violation_code")),
                "outcome": str(runtime_contract.get("outcome")),
            }
            expected_guard_sha = hashlib.sha256(
                canonical_json(source_contract).encode("utf-8")
            ).hexdigest()
            if (
                record.get("source_contract_sha256") != expected_guard_sha
                or record.get("stage") != runtime_contract.get("stage")
                or record.get("violation_code") != runtime_contract.get("violation_code")
            ):
                return [
                    issue(
                        "universal_asset_binding",
                        "hard-gate guard execution does not bind its exact validated source contract",
                        guard_id=guard_id,
                        expected_sha256=expected_guard_sha,
                        actual_sha256=record.get("source_contract_sha256"),
                    )
                ]
        slot_records = scene.get("slot_states") if isinstance(scene.get("slot_states"), list) else []
        fixed_prop_slot = next(
            (
                slot
                for slot in slot_records
                if isinstance(slot, dict)
                and slot.get("slot_id") == "prop"
                and slot.get("state") == "fixed"
            ),
            None,
        )
        if isinstance(fixed_prop_slot, dict):
            semantic_values = set(_string_list(fixed_prop_slot.get("value_ids")) or [])
            literal_phrases = list(_string_list(fixed_prop_slot.get("request_phrases")) or [])
            embedded_roles = _mapping(scene.get("scene_contract")).get("event_roles")
            for role in embedded_roles if isinstance(embedded_roles, list) else []:
                if (
                    isinstance(role, dict)
                    and role.get("role_id") in {"target", "instrument"}
                    and role.get("state") == "fixed"
                    and _is_nonempty_string(role.get("value_id"))
                ):
                    semantic_values.add(str(role["value_id"]))
                    literal_phrases.extend(_string_list(role.get("request_phrases")) or [])
            normalized_prop_evidence = " ".join(
                _normalized_literal_text(phrase)
                for phrase in literal_phrases
            )
            for candidate_id, semantic_ids in UNIVERSAL_FIXED_PROP_ATOMS.items():
                concept_id = UNIVERSAL_FIXED_PROP_CONCEPT_BY_CANDIDATE[candidate_id]
                prop_concept = assets.prop_by_id.get(concept_id)
                aliases = {
                    _normalized_literal_text(alias)
                    for alias_group in (
                        prop_concept.get("aliases", [])
                        if isinstance(prop_concept, Mapping)
                        else []
                    )
                    if isinstance(alias_group, Mapping)
                    for alias in (_string_list(alias_group.get("values")) or [])
                }
                literal_alias_matched = any(
                    alias and _literal_catalog_alias_matches(alias, normalized_prop_evidence)
                    for alias in aliases
                )
                semantic_id_matched = bool(semantic_values.intersection(semantic_ids))
                semantic_tokens = {
                    token
                    for value_id in semantic_values
                    for token in re.split(
                        r"[_\-/.:\s]+",
                        _normalized_literal_text(value_id),
                    )
                    if token
                }
                distinct_sense_bound = any(
                    token == stem or (len(stem) >= 3 and token.startswith(stem))
                    for stem in UNIVERSAL_PROP_LITERAL_SENSE_DISAMBIGUATORS.get(concept_id, set())
                    for token in semantic_tokens
                )
                if (
                    literal_alias_matched
                    and not semantic_id_matched
                    and not distinct_sense_bound
                ):
                    details = {
                        "candidate_id": candidate_id,
                        "concept_id": concept_id,
                        "fixed_values": sorted(semantic_values),
                    }
                    return [
                        issue(
                            "universal_scene_contract",
                            "literal known-prop slot evidence must not be under-declared by an unrelated semantic value id",
                            **details,
                        ),
                        issue(
                            "universal_slot_state",
                            "literal known-prop slot evidence must not be under-declared by an unrelated semantic value id",
                            **details,
                        ),
                    ]
                if semantic_id_matched and not literal_alias_matched:
                    details = {
                        "candidate_id": candidate_id,
                        "concept_id": concept_id,
                        "fixed_values": sorted(semantic_values),
                    }
                    return [
                        issue(
                            "universal_scene_contract",
                            "known fixed prop semantic id is not bound to a literal catalog alias in its slot evidence",
                            **details,
                        ),
                        issue(
                            "universal_slot_state",
                            "known fixed prop semantic id is not bound to a literal catalog alias in its slot evidence",
                            **details,
                        ),
                    ]
        request = _mapping(pack.get("request_contract"))
        exposure_ids = _string_list(request.get("prior_exposure_ids")) or []
        unknown_exposure_ids = sorted(
            set(exposure_ids) - set(assets.candidate_by_id)
        )
        if unknown_exposure_ids:
            return [
                issue(
                    "universal_candidate_eligibility",
                    "prior_exposure_ids contains unknown universal candidate ids",
                    unknown=unknown_exposure_ids,
                )
            ]
        validator = getattr(universal_runtime, "validate_universal_scene_selection", None)
        if not callable(validator):
            return [issue("universal_candidate_eligibility", "universal runtime selection revalidator is unavailable")]
        profile = _mapping(pack.get("format_profile"))
        provenance = _mapping(pack.get("provenance"))
        validated = validator(
            scene,
            request_text,
            assets,
            topic_id=request.get("topic_id"),
            format_id=profile.get("variant_id"),
            creativity=request.get("creativity"),
            seed=provenance.get("seed"),
            prior_exposure_ids=request.get("prior_exposure_ids"),
        )
        if canonical_json(validated) != canonical_json(scene):
            return [issue("universal_candidate_eligibility", "runtime revalidation did not reproduce the canonical universal selection")]
    except universal_runtime.UniversalSceneRuntimeError as exc:
        if isinstance(exc, universal_runtime.InputContractError):
            check = "universal_scene_contract"
        elif isinstance(exc, universal_runtime.AssetValidationError):
            check = "universal_asset_binding"
        else:
            check = "universal_candidate_eligibility"
        return [
            issue(
                check,
                "universal selection fails independent asset/runtime-contract revalidation",
                error_type=type(exc).__name__,
                error=str(exc),
            )
        ]
    except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        return [issue("universal_asset_binding", "universal asset revalidation failed closed", error_type=type(exc).__name__, error=str(exc))]
    return []


def _universal_composition_carrier_contract(
    scene: Mapping[str, Any],
) -> tuple[
    dict[str, dict[Any, list[list[str]]]],
    dict[str, str],
    list[dict[str, Any]],
]:
    """Validate and index the authenticated semantic carriers for v3 prose."""

    failures: list[dict[str, Any]] = []
    indexed: dict[str, dict[Any, list[list[str]]]] = {
        section: {}
        for section in (
            "identity_core",
            "fixed_slots",
            "event_roles",
            "atoms",
            "bridges",
            "resources",
        )
    }
    identity_polarity: dict[str, str] = {}
    carriers = scene.get("composition_carriers")
    failures.extend(
        _exact_object_keys(
            carriers,
            UNIVERSAL_COMPOSITION_CARRIER_KEYS,
            check="universal_composition_carriers",
            object_name="universal_scene.composition_carriers",
        )
    )
    if not isinstance(carriers, dict):
        return indexed, identity_polarity, failures
    if carriers.get("schema") != UNIVERSAL_COMPOSITION_CARRIERS_SCHEMA:
        failures.append(
            issue(
                "universal_composition_carriers",
                "composition carriers schema is outside the closed contract",
                expected=UNIVERSAL_COMPOSITION_CARRIERS_SCHEMA,
                actual=carriers.get("schema"),
            )
        )

    identity = _mapping(scene.get("identity_core"))
    expected_identity: dict[str, dict[str, str]] = {}
    for entity in identity.get("entities") if isinstance(identity.get("entities"), list) else []:
        if not isinstance(entity, dict):
            continue
        asserted_absence_fact_ids = {
            str(capability["source_fact_id"])
            for capability in (
                entity.get("capabilities")
                if isinstance(entity.get("capabilities"), list)
                else []
            )
            if isinstance(capability, dict)
            and capability.get("source") == "explicit"
            and capability.get("state") == "unavailable"
            and capability.get("capacity") == 0
            and _is_nonempty_string(capability.get("source_fact_id"))
        }
        for fact in entity.get("feature_facts") if isinstance(entity.get("feature_facts"), list) else []:
            if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                fact_id = str(fact["id"])
                expected_identity[str(fact["id"])] = {
                    "fact_id": fact_id,
                    "polarity": (
                        "asserted_absence"
                        if fact_id in asserted_absence_fact_ids
                        else "asserted_presence"
                    ),
                }
    for fact_kind, polarity in (("scene_facts", "asserted_presence"), ("forbidden_facts", "forbidden")):
        for fact in identity.get(fact_kind) if isinstance(identity.get(fact_kind), list) else []:
            if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                expected_identity[str(fact["id"])] = {
                    "fact_id": str(fact["id"]),
                    "polarity": polarity,
                }

    expected_fixed: dict[tuple[str, str], dict[str, str]] = {}
    slot_states = scene.get("slot_states") if isinstance(scene.get("slot_states"), list) else []
    for slot in slot_states:
        if not isinstance(slot, dict) or slot.get("state") != "fixed" or not _is_nonempty_string(slot.get("slot_id")):
            continue
        for value_id in _string_list(slot.get("value_ids")) or []:
            pair = (str(slot["slot_id"]), value_id)
            expected_fixed[pair] = {"slot_id": pair[0], "value_id": pair[1]}

    event = _mapping(scene.get("selected_event"))
    expected_roles: dict[str, dict[str, str]] = {}
    for role in event.get("roles") if isinstance(event.get("roles"), list) else []:
        if (
            isinstance(role, dict)
            and _is_nonempty_string(role.get("role_id"))
            and _is_nonempty_string(role.get("value_id"))
        ):
            role_id = str(role["role_id"])
            expected_roles[role_id] = {
                "role_id": role_id,
                "value_id": str(role["value_id"]),
            }

    expected_atoms: dict[str, dict[str, str]] = {}
    for atom in scene.get("atoms") if isinstance(scene.get("atoms"), list) else []:
        if (
            isinstance(atom, dict)
            and _is_nonempty_string(atom.get("instance_id"))
            and _is_nonempty_string(atom.get("candidate_id"))
        ):
            instance_id = str(atom["instance_id"])
            expected_atoms[instance_id] = {
                "instance_id": instance_id,
                "candidate_id": str(atom["candidate_id"]),
            }

    expected_bridges: dict[str, dict[str, str]] = {}
    for bridge in scene.get("bridges") if isinstance(scene.get("bridges"), list) else []:
        if (
            isinstance(bridge, dict)
            and _is_nonempty_string(bridge.get("bridge_id"))
            and _is_nonempty_string(bridge.get("bridge_type"))
        ):
            bridge_id = str(bridge["bridge_id"])
            expected_bridges[bridge_id] = {
                "bridge_id": bridge_id,
                "bridge_type": str(bridge["bridge_type"]),
            }

    expected_resources: dict[str, dict[str, str]] = {}
    claims = scene.get("resource_claims") if isinstance(scene.get("resource_claims"), list) else []
    for claim in claims:
        if (
            isinstance(claim, dict)
            and claim.get("evidence_required") is True
            and _is_nonempty_string(claim.get("claim_id"))
            and _is_nonempty_string(claim.get("resource_kind"))
        ):
            claim_id = str(claim["claim_id"])
            expected_resources[claim_id] = {
                "claim_id": claim_id,
                "resource_kind": str(claim["resource_kind"]),
            }

    literal_sources: dict[str, dict[Any, set[str]]] = {
        section: {}
        for section in ("identity_core", "fixed_slots", "event_roles")
    }
    for entity in identity.get("entities") if isinstance(identity.get("entities"), list) else []:
        if not isinstance(entity, dict):
            continue
        for fact in entity.get("feature_facts") if isinstance(entity.get("feature_facts"), list) else []:
            if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                literal_sources["identity_core"][str(fact["id"])] = {
                    _normalized_literal_text(phrase)
                    for phrase in (_string_list(fact.get("request_phrases")) or [])
                }
    for fact_kind in ("scene_facts", "forbidden_facts"):
        for fact in identity.get(fact_kind) if isinstance(identity.get(fact_kind), list) else []:
            if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                literal_sources["identity_core"][str(fact["id"])] = {
                    _normalized_literal_text(phrase)
                    for phrase in (_string_list(fact.get("request_phrases")) or [])
                }
    for slot in slot_states:
        if not isinstance(slot, dict) or slot.get("state") != "fixed" or not _is_nonempty_string(slot.get("slot_id")):
            continue
        for binding in slot.get("value_phrase_bindings") if isinstance(slot.get("value_phrase_bindings"), list) else []:
            if not isinstance(binding, dict) or not _is_nonempty_string(binding.get("value_id")):
                continue
            literal_sources["fixed_slots"][(str(slot["slot_id"]), str(binding["value_id"]))] = {
                _normalized_literal_text(phrase)
                for phrase in (_string_list(binding.get("request_phrases")) or [])
            }
    embedded_contract = _mapping(scene.get("scene_contract"))
    for role in embedded_contract.get("event_roles") if isinstance(embedded_contract.get("event_roles"), list) else []:
        if (
            isinstance(role, dict)
            and role.get("state") == "fixed"
            and _is_nonempty_string(role.get("role_id"))
        ):
            literal_sources["event_roles"][str(role["role_id"])] = {
                _normalized_literal_text(phrase)
                for phrase in (_string_list(role.get("request_phrases")) or [])
            }

    section_contracts: tuple[
        tuple[str, str, dict[Any, dict[str, str]], set[str]], ...
    ] = (
        ("identity_core", "fact_id", expected_identity, {"fact_id", "polarity", "required_lexeme_groups"}),
        ("fixed_slots", "slot_id", expected_fixed, {"slot_id", "value_id", "required_lexeme_groups"}),
        ("event_roles", "role_id", expected_roles, {"role_id", "value_id", "required_lexeme_groups"}),
        ("atoms", "instance_id", expected_atoms, {"instance_id", "candidate_id", "required_lexeme_groups"}),
        ("bridges", "bridge_id", expected_bridges, {"bridge_id", "bridge_type", "required_lexeme_groups"}),
        ("resources", "claim_id", expected_resources, {"claim_id", "resource_kind", "required_lexeme_groups"}),
    )
    for section, id_key, expected, exact_keys in section_contracts:
        records = carriers.get(section)
        if not isinstance(records, list):
            failures.append(
                issue(
                    "universal_composition_carriers",
                    "composition carrier section must be a list",
                    section=section,
                )
            )
            continue
        actual_metadata: dict[Any, dict[str, str]] = {}
        for index, record in enumerate(records):
            if not isinstance(record, dict) or set(record) != exact_keys:
                failures.append(
                    issue(
                        "universal_composition_carriers",
                        "composition carrier item must have its exact closed field set",
                        section=section,
                        index=index,
                    )
                )
                continue
            if section == "fixed_slots":
                slot_id = record.get("slot_id")
                value_id = record.get("value_id")
                record_key: Any = (
                    str(slot_id) if _is_nonempty_string(slot_id) else "",
                    str(value_id) if _is_nonempty_string(value_id) else "",
                )
                metadata_keys = ("slot_id", "value_id")
            else:
                raw_key = record.get(id_key)
                record_key = str(raw_key) if _is_nonempty_string(raw_key) else ""
                metadata_keys = tuple(key for key in exact_keys if key != "required_lexeme_groups")
            if not record_key or (isinstance(record_key, tuple) and not all(record_key)):
                failures.append(
                    issue(
                        "universal_composition_carriers",
                        "composition carrier identifier fields must be nonempty strings",
                        section=section,
                        index=index,
                    )
                )
                continue
            if record_key in indexed[section]:
                failures.append(
                    issue(
                        "universal_composition_carriers",
                        "composition carrier identifiers must be unique",
                        section=section,
                        record_id=list(record_key) if isinstance(record_key, tuple) else record_key,
                    )
                )
            raw_groups = record.get("required_lexeme_groups")
            valid_groups: list[list[str]] = []
            maximum_groups = 3 if section == "identity_core" else 2
            if not isinstance(raw_groups, list) or not 1 <= len(raw_groups) <= maximum_groups:
                failures.append(
                    issue(
                        "universal_composition_carriers",
                        "required_lexeme_groups exceeds the section-specific compact anchor bound",
                        section=section,
                        record_id=list(record_key) if isinstance(record_key, tuple) else record_key,
                        maximum_groups=maximum_groups,
                    )
                )
            else:
                seen_groups: set[tuple[str, ...]] = set()
                for group_index, raw_group in enumerate(raw_groups):
                    alternatives = _string_list(raw_group)
                    normalized_alternatives = [
                        _normalized_literal_text(alternative)
                        for alternative in (alternatives or [])
                    ]
                    group_signature = tuple(normalized_alternatives)
                    authenticated_literals = literal_sources.get(section, {}).get(record_key, set())

                    def valid_alternative(alternative: str, normalized: str) -> bool:
                        internal_tokens = set(re.findall(r"[a-z0-9]+", normalized)).intersection(
                            UNIVERSAL_CARRIER_INTERNAL_TOKENS
                        )
                        reviewed_english = (
                            alternative == normalized
                            and re.fullmatch(r"[a-z0-9]+(?: [a-z0-9]+)*", alternative) is not None
                            and not internal_tokens
                        )
                        unmistakable_namespace = re.search(
                            r"(?:^|\b)(?:cbg|dpa|ecs|gha|ofm|sdc|sptg|uao|ubp|ugf|usc|ush|usl)[_:/-]|"
                            r"\b(?:candidate|resource|bridge|instance|slot|role)[_ -]?id\b",
                            normalized,
                        ) is not None
                        literal_fallback = (
                            normalized in authenticated_literals
                            and 1 <= len(normalized) <= 240
                            and any(character.isalnum() for character in normalized)
                            and not unmistakable_namespace
                            and not any(
                                unicodedata.category(character) in {"Cc", "Cf", "Cs"}
                                for character in alternative
                            )
                        )
                        return reviewed_english or literal_fallback

                    valid_group = (
                        alternatives is not None
                        and bool(alternatives)
                        and len(normalized_alternatives) == len(set(normalized_alternatives))
                        and all(
                            valid_alternative(alternative, normalized)
                            for alternative, normalized in zip(alternatives, normalized_alternatives)
                        )
                        and group_signature not in seen_groups
                    )
                    if not valid_group:
                        failures.append(
                            issue(
                                "universal_composition_carriers",
                                "every lexeme group must be a unique normalized reviewed-English list or an exact literal-bound fallback, never an internal namespace token",
                                section=section,
                                record_id=list(record_key) if isinstance(record_key, tuple) else record_key,
                                group_index=group_index,
                            )
                        )
                        continue
                    seen_groups.add(group_signature)
                    valid_groups.append(normalized_alternatives)
            indexed[section][record_key] = valid_groups
            actual_metadata[record_key] = {
                key: str(record[key]) if _is_nonempty_string(record.get(key)) else ""
                for key in metadata_keys
            }
            if section == "identity_core" and isinstance(record_key, str):
                polarity = record.get("polarity")
                if polarity not in ("asserted_presence", "asserted_absence", "forbidden"):
                    failures.append(
                        issue(
                            "universal_composition_carriers",
                            "identity carrier polarity is outside the closed enum",
                            fact_id=record_key,
                            actual=polarity,
                        )
                    )
                elif isinstance(polarity, str):
                    identity_polarity[record_key] = polarity
        if actual_metadata != expected:
            failures.append(
                issue(
                    "universal_composition_carriers",
                    "composition carrier section must exactly cover and bind its canonical scene records",
                    section=section,
                    expected=[list(key) if isinstance(key, tuple) else key for key in expected],
                    actual=[list(key) if isinstance(key, tuple) else key for key in actual_metadata],
                )
            )
    return indexed, identity_polarity, failures


def validate_universal_scene_integrity(pack: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Validate the additive v3 scene proof and sibling asset bindings.

    The generator validates the complete scene contract before pack assembly.
    The pack retains its hash plus the canonical identity, slot and context
    projection.  The auditor cross-binds those copies, then reloads the frozen
    sibling assets and re-evaluates the selected catalog contracts.
    """

    if pack.get("contract_version") != CONTRACT_VERSION_V3:
        return []

    errors: list[dict[str, Any]] = []
    errors.extend(
        _exact_object_keys(
            pack,
            UNIVERSAL_PACK_KEYS,
            check="universal_scene_contract",
            object_name="v3 candidate pack",
        )
    )
    request = _mapping(pack.get("request_contract"))
    errors.extend(
        _exact_object_keys(
            pack.get("request_contract"),
            UNIVERSAL_REQUEST_CONTRACT_KEYS,
            check="universal_scene_contract",
            object_name="v3 request_contract",
        )
    )
    request_text = request.get("request_text") if _is_nonempty_string(request.get("request_text")) else ""
    prior_exposure_ids = _unique_string_list(request.get("prior_exposure_ids"))
    if prior_exposure_ids is None:
        errors.append(
            issue(
                "universal_scene_contract",
                "prior_exposure_ids must be an ordered unique string list",
                actual=request.get("prior_exposure_ids"),
            )
        )
        prior_exposure_ids = []
    scene_contract_sha = request.get("scene_contract_sha256")
    if request.get("scene_contract_schema") != SCENE_CONTRACT_SCHEMA:
        errors.append(
            issue(
                "universal_scene_contract",
                "request_contract must bind the closed scene-contract schema",
                expected=SCENE_CONTRACT_SCHEMA,
                actual=request.get("scene_contract_schema"),
            )
        )
    if not _hex64(scene_contract_sha):
        errors.append(issue("universal_scene_contract", "scene_contract_sha256 must be 64 lowercase hexadecimal characters"))

    composition = pack.get("composition_contract")
    errors.extend(
        _exact_object_keys(
            composition,
            UNIVERSAL_COMPOSITION_CONTRACT_KEYS,
            check="universal_scene_contract",
            object_name="v3 composition_contract",
        )
    )
    if isinstance(composition, dict) and composition.get("composed_schema") != COMPOSED_PROMPT_SCHEMA_V3:
        errors.append(issue("universal_scene_contract", "v3 composition contract must select the v3 composed schema"))
    asset_hashes_value = pack.get("asset_hashes")
    errors.extend(
        _exact_object_keys(
            asset_hashes_value,
            UNIVERSAL_ASSET_HASH_KEYS,
            check="universal_asset_binding",
            object_name="v3 asset_hashes",
        )
    )
    provenance = pack.get("provenance")
    if not isinstance(provenance, dict):
        errors.append(issue("universal_scene_contract", "v3 provenance must be an object"))
        provenance = {}
    elif provenance.get("generator_version") != "subculture-illustration-generator/v3":
        errors.append(issue("universal_scene_contract", "v3 pack must bind the v3 generator", actual=provenance.get("generator_version")))

    scene = pack.get("universal_scene")
    errors.extend(
        _exact_object_keys(
            scene,
            UNIVERSAL_SCENE_KEYS,
            check="universal_scene_contract",
            object_name="universal_scene",
        )
    )
    if not isinstance(scene, dict):
        return errors
    if scene.get("schema") != UNIVERSAL_SCENE_SCHEMA:
        errors.append(
            issue(
                "universal_scene_contract",
                "universal_scene schema is not the closed v1 selection schema",
                expected=UNIVERSAL_SCENE_SCHEMA,
                actual=scene.get("schema"),
            )
        )
    embedded_contract = scene.get("scene_contract")
    errors.extend(
        _exact_object_keys(
            embedded_contract,
            UNIVERSAL_EMBEDDED_SCENE_CONTRACT_KEYS,
            check="universal_scene_contract",
            object_name="universal_scene.scene_contract",
        )
    )
    embedded_contract_sha: str | None = None
    if isinstance(embedded_contract, dict):
        if embedded_contract.get("schema") != SCENE_CONTRACT_SCHEMA:
            errors.append(
                issue(
                    "universal_scene_contract",
                    "embedded scene contract schema is outside the closed contract",
                    expected=SCENE_CONTRACT_SCHEMA,
                    actual=embedded_contract.get("schema"),
                )
            )
        expected_request_sha = hashlib.sha256(request_text.encode("utf-8")).hexdigest()
        if embedded_contract.get("request_text_sha256") != expected_request_sha:
            errors.append(
                issue(
                    "universal_scene_contract",
                    "embedded scene contract request hash does not match exact request_text bytes",
                    expected=expected_request_sha,
                    actual=embedded_contract.get("request_text_sha256"),
                )
            )
        embedded_contract_sha = hashlib.sha256(
            canonical_json(embedded_contract).encode("utf-8")
        ).hexdigest()
        if embedded_contract_sha != scene_contract_sha:
            errors.append(
                issue(
                    "universal_scene_contract",
                    "request_contract scene hash must recompute from the embedded canonical contract",
                    expected=embedded_contract_sha,
                    actual=scene_contract_sha,
                )
            )
    context_profile = scene.get("context_profile")
    errors.extend(
        _exact_object_keys(
            context_profile,
            {"theme_tags", "era_technology", "tone", "violence", "social", "scale"},
            check="universal_scene_contract",
            object_name="universal_scene.context_profile",
        )
    )
    if isinstance(context_profile, dict):
        if _unique_string_list(context_profile.get("theme_tags")) is None:
            errors.append(issue("universal_scene_contract", "context_profile.theme_tags must be a unique string list"))
        for field in ("era_technology", "tone"):
            if not _is_nonempty_string(context_profile.get(field)):
                errors.append(issue("universal_scene_contract", "context profile field must be a nonempty closed value", field=field))
        for field, allowed in (
            ("violence", {"closed", "nonviolent", "contextual", "active", "unknown"}),
            ("social", {"solo", "dyad", "ensemble", "unknown"}),
            ("scale", {"intimate", "room", "site", "world", "unknown"}),
        ):
            if context_profile.get(field) not in allowed:
                errors.append(issue("universal_scene_contract", "context profile field is outside the closed enum", field=field, actual=context_profile.get(field), allowed=sorted(allowed)))
        embedded_context = _mapping(embedded_contract).get("context_profile")
        if context_profile != embedded_context:
            errors.append(
                issue(
                    "universal_scene_contract",
                    "context_profile must exactly copy the embedded scene contract",
                    expected=embedded_context,
                    actual=context_profile,
                )
            )

    errors.extend(
        _audit_frozen_trace_shape_failures(
            scene,
            request_text,
            scene_contract_sha,
        )
    )

    selection = scene.get("selection_trace")
    errors.extend(
        _exact_object_keys(
            selection,
            UNIVERSAL_SELECTION_TRACE_KEYS,
            check="universal_scene_contract",
            object_name="universal_scene.selection_trace",
        )
    )
    if isinstance(selection, dict):
        if selection.get("scene_contract_sha256") != scene_contract_sha:
            errors.append(
                issue(
                    "universal_scene_contract",
                    "selection trace and request contract must bind the same scene-contract hash",
                    request_hash=scene_contract_sha,
                    trace_hash=selection.get("scene_contract_sha256"),
                )
            )
        if selection.get("seed") != provenance.get("seed"):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "universal selection seed must exactly copy the legacy authorial selection seed",
                    expected=provenance.get("seed"),
                    actual=selection.get("seed"),
                )
            )
        if selection.get("selection_mode") != "predicate_beam_v1":
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "universal selection must use the closed predicate beam solver",
                    actual=selection.get("selection_mode"),
                )
            )
        if selection.get("beam_width") != 8:
            errors.append(issue("universal_candidate_eligibility", "beam_width must equal the frozen compatibility value eight", actual=selection.get("beam_width")))
        if not _hex64(selection.get("tie_break_digest")):
            errors.append(issue("universal_candidate_eligibility", "tie_break_digest must be 64 lowercase hexadecimal characters"))
        proposal_family_ids = _unique_string_list(
            selection.get("eligible_proposal_family_ids")
        )
        if proposal_family_ids is None or proposal_family_ids != sorted(proposal_family_ids):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "eligible_proposal_family_ids must be a sorted unique string list",
                    actual=selection.get("eligible_proposal_family_ids"),
                )
            )
        proposal_profile_ids = _unique_string_list(
            selection.get("eligible_proposal_profile_ids")
        )
        if proposal_profile_ids is None or proposal_profile_ids != sorted(proposal_profile_ids):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "eligible_proposal_profile_ids must be a sorted unique string list",
                    actual=selection.get("eligible_proposal_profile_ids"),
                )
            )
        raw_proposal_rejections = selection.get("proposal_rejections")
        proposal_rejection_ids: list[str] = []
        proposal_rejection_reason_counts: dict[str, int] = {}
        proposal_reason_ids = {
            "proposal_path_not_open",
            "slot_state_ineligible",
            "requires_all_unsatisfied",
            "forbidden_predicate_satisfied",
            "policy_explicit_only",
            "policy_active_violence",
            "fixed_role_conflict",
            "closed_role_conflict",
        }
        if not isinstance(raw_proposal_rejections, list):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "proposal_rejections must be a typed list",
                    actual=raw_proposal_rejections,
                )
            )
        else:
            for index, rejection in enumerate(raw_proposal_rejections):
                errors.extend(
                    _exact_object_keys(
                        rejection,
                        UNIVERSAL_PROPOSAL_REJECTION_KEYS,
                        check="universal_candidate_eligibility",
                        object_name=f"proposal_rejections[{index}]",
                    )
                )
                if not isinstance(rejection, dict):
                    continue
                proposal_id = rejection.get("proposal_id")
                reason_code = rejection.get("reason_code")
                if (
                    not _is_nonempty_string(proposal_id)
                    or reason_code not in proposal_reason_ids
                ):
                    errors.append(
                        issue(
                            "universal_candidate_eligibility",
                            "proposal rejection requires a known closed reason and nonempty profile id",
                            index=index,
                            actual=rejection,
                        )
                    )
                    continue
                proposal_rejection_ids.append(str(proposal_id))
                proposal_rejection_reason_counts[str(reason_code)] = (
                    proposal_rejection_reason_counts.get(str(reason_code), 0) + 1
                )
            expected_order = sorted(
                proposal_rejection_ids, key=lambda value: value.encode("utf-8")
            )
            if (
                proposal_rejection_ids != expected_order
                or len(proposal_rejection_ids) != len(set(proposal_rejection_ids))
            ):
                errors.append(
                    issue(
                        "universal_candidate_eligibility",
                        "proposal rejections must be UTF-8-byte-sorted and unique",
                        actual=proposal_rejection_ids,
                    )
                )
        if proposal_profile_ids is not None:
            overlap = sorted(set(proposal_profile_ids) & set(proposal_rejection_ids))
            if overlap:
                errors.append(
                    issue(
                        "universal_candidate_eligibility",
                        "proposal profiles cannot be both eligible and rejected",
                        proposal_ids=overlap,
                    )
                )
        eligible_ids_by_facet = selection.get("eligible_candidate_ids_by_facet")
        traced_eligible_ids: set[str] = set()
        traced_facet_lengths: dict[str, int] = {}
        if not isinstance(eligible_ids_by_facet, dict) or set(eligible_ids_by_facet) != UNIVERSAL_FACET_IDS:
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "eligible candidate trace must cover the closed fifteen facets exactly",
                    expected=sorted(UNIVERSAL_FACET_IDS),
                    actual=(
                        sorted(eligible_ids_by_facet)
                        if isinstance(eligible_ids_by_facet, dict)
                        else eligible_ids_by_facet
                    ),
                )
            )
        else:
            for facet in sorted(UNIVERSAL_FACET_IDS):
                candidate_ids = _unique_string_list(eligible_ids_by_facet.get(facet))
                if candidate_ids is None or candidate_ids != sorted(candidate_ids):
                    errors.append(
                        issue(
                            "universal_candidate_eligibility",
                            "eligible candidate IDs must be sorted and unique within each facet",
                            facet=facet,
                            actual=eligible_ids_by_facet.get(facet),
                        )
                    )
                    continue
                duplicate_ids = sorted(set(candidate_ids) & traced_eligible_ids)
                if duplicate_ids:
                    errors.append(
                        issue(
                            "universal_candidate_eligibility",
                            "one visual candidate cannot be eligible in multiple facets",
                            facet=facet,
                            duplicate_ids=duplicate_ids,
                        )
                    )
                traced_eligible_ids.update(candidate_ids)
                traced_facet_lengths[facet] = len(candidate_ids)

        raw_candidate_rejections = selection.get("candidate_rejections")
        rejected_candidate_ids: list[str] = []
        rejected_reason_counts: dict[str, int] = {}
        if not isinstance(raw_candidate_rejections, list):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "candidate_rejections must be a typed list",
                    actual=raw_candidate_rejections,
                )
            )
        else:
            for index, rejection in enumerate(raw_candidate_rejections):
                errors.extend(
                    _exact_object_keys(
                        rejection,
                        UNIVERSAL_CANDIDATE_REJECTION_KEYS,
                        check="universal_candidate_eligibility",
                        object_name=f"candidate_rejections[{index}]",
                    )
                )
                if not isinstance(rejection, dict):
                    continue
                candidate_id = rejection.get("candidate_id")
                reason_code = rejection.get("reason_code")
                if not _is_nonempty_string(candidate_id) or not _is_nonempty_string(reason_code):
                    errors.append(
                        issue(
                            "universal_candidate_eligibility",
                            "candidate rejection requires a nonempty candidate id and reason code",
                            index=index,
                            actual=rejection,
                        )
                    )
                    continue
                rejected_candidate_ids.append(str(candidate_id))
                rejected_reason_counts[str(reason_code)] = rejected_reason_counts.get(str(reason_code), 0) + 1
            if rejected_candidate_ids != sorted(set(rejected_candidate_ids)):
                errors.append(
                    issue(
                        "universal_candidate_eligibility",
                        "rejected visual candidate IDs must be sorted and unique",
                        actual=rejected_candidate_ids,
                    )
                )
            overlap = sorted(traced_eligible_ids & set(rejected_candidate_ids))
            if overlap:
                errors.append(
                    issue(
                        "universal_candidate_eligibility",
                        "a visual candidate cannot be both eligible and rejected",
                        candidate_ids=overlap,
                    )
                )
        for field in (
            "eligible_count_by_facet",
            "rejection_count_by_code",
            "eligible_proposal_count_by_band",
            "proposal_rejection_count_by_code",
        ):
            counts = selection.get(field)
            if not isinstance(counts, dict) or any(
                not _is_nonempty_string(key) or not _closed_int(value, 0, 10**9)
                for key, value in (counts.items() if isinstance(counts, dict) else [])
            ):
                errors.append(issue("universal_candidate_eligibility", f"{field} must be a nonnegative integer mapping"))
        eligible_counts = selection.get("eligible_count_by_facet")
        if isinstance(eligible_counts, dict) and set(eligible_counts) != UNIVERSAL_FACET_IDS:
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "eligible facet counts must cover the closed fifteen facets exactly",
                    expected=sorted(UNIVERSAL_FACET_IDS),
                    actual=sorted(eligible_counts),
                )
            )
        elif (
            isinstance(eligible_counts, dict)
            and traced_facet_lengths
            and eligible_counts != traced_facet_lengths
        ):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "eligible facet counts must exactly project the retained candidate ID lists",
                    expected=traced_facet_lengths,
                    actual=eligible_counts,
                )
            )
        rejection_counts = selection.get("rejection_count_by_code")
        if isinstance(rejection_counts, dict):
            undercounted = {
                reason: count
                for reason, count in rejected_reason_counts.items()
                if not _closed_int(rejection_counts.get(reason), count, 10**9)
            }
            if undercounted:
                errors.append(
                    issue(
                        "universal_candidate_eligibility",
                        "aggregate rejection counts cannot undercount retained visual-candidate decisions",
                        minimum_by_code=undercounted,
                        actual=rejection_counts,
                    )
                )
        proposal_band_counts = selection.get("eligible_proposal_count_by_band")
        if isinstance(proposal_band_counts, dict) and set(proposal_band_counts) != {
            "near",
            "middle",
            "far",
        }:
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "eligible proposal counts must cover the closed distance bands exactly",
                    actual=sorted(proposal_band_counts),
                )
            )
        elif (
            isinstance(proposal_band_counts, dict)
            and proposal_profile_ids is not None
            and all(_closed_int(value, 0, 10**9) for value in proposal_band_counts.values())
            and sum(proposal_band_counts.values()) != len(proposal_profile_ids)
        ):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "eligible proposal band counts must exactly project eligible profile IDs",
                    expected=len(proposal_profile_ids),
                    actual=sum(proposal_band_counts.values()),
                )
            )
        if (
            proposal_profile_ids is not None
            and proposal_family_ids is not None
            and len(proposal_profile_ids) != len(proposal_family_ids)
        ):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "eligible proposal family and profile projections must have equal cardinality",
                    profile_count=len(proposal_profile_ids),
                    family_count=len(proposal_family_ids),
                )
            )
        proposal_rejection_counts = selection.get("proposal_rejection_count_by_code")
        if (
            isinstance(proposal_rejection_counts, dict)
            and proposal_rejection_counts != proposal_rejection_reason_counts
        ):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "proposal rejection counts must exactly project retained first-failure rows",
                    expected=proposal_rejection_reason_counts,
                    actual=proposal_rejection_counts,
                )
            )

    identity = scene.get("identity_core")
    errors.extend(
        _exact_object_keys(
            identity,
            UNIVERSAL_IDENTITY_CORE_KEYS,
            check="universal_identity_core",
            object_name="universal_scene.identity_core",
        )
    )
    if isinstance(identity, dict) and isinstance(embedded_contract, dict):
        embedded_identity = _mapping(embedded_contract.get("identity_core"))
        for field in ("entities", "scene_facts", "forbidden_facts"):
            if identity.get(field) != embedded_identity.get(field):
                errors.append(
                    issue(
                        "universal_identity_core",
                        "identity projection must exactly copy the embedded scene contract",
                        field=field,
                        expected=embedded_identity.get(field),
                        actual=identity.get(field),
                    )
                )
    identity_fact_ids: list[str] = []
    capacity_by_owner_kind: dict[tuple[str, str], int] = {}
    entity_capacity_by_owner_kind: dict[tuple[str, str], int] = {}
    entity_capacity_record_by_owner_kind: dict[tuple[str, str], dict[str, Any]] = {}
    flattened_capacity_record_by_owner_kind: dict[tuple[str, str], dict[str, Any]] = {}
    entity_ids: list[str] = []
    if isinstance(identity, dict):
        entities = identity.get("entities")
        if not isinstance(entities, list) or not entities:
            errors.append(issue("universal_identity_core", "identity_core.entities must be a nonempty list"))
            entities = []
        for entity in entities:
            if not isinstance(entity, dict) or set(entity) != {
                "entity_id",
                "quantity",
                "embodiment_profile_id",
                "capability_projection_mode",
                "feature_facts",
                "capabilities",
            }:
                errors.append(issue("universal_identity_core", "every entity must have the exact scene-contract field set"))
                continue
            entity_id = entity.get("entity_id")
            if not _is_nonempty_string(entity_id):
                errors.append(issue("universal_identity_core", "entity_id must be a nonempty string"))
                continue
            entity_ids.append(str(entity_id))
            if not _closed_int(entity.get("quantity"), 1, 64):
                errors.append(issue("universal_identity_core", "entity quantity must be a positive bounded integer", entity_id=entity_id))
            if not _is_nonempty_string(entity.get("embodiment_profile_id")):
                errors.append(issue("universal_identity_core", "embodiment_profile_id must remain visible", entity_id=entity_id))
            projection_mode = entity.get("capability_projection_mode")
            if projection_mode not in {"catalog_exact", "declared_subset"}:
                errors.append(
                    issue(
                        "universal_resource_capacity",
                        "capability_projection_mode is outside the closed enum",
                        entity_id=entity_id,
                        actual=projection_mode,
                    )
                )
            elif str(entity.get("embodiment_profile_id", "")).startswith("custom_") and projection_mode != "declared_subset":
                errors.append(
                    issue(
                        "universal_resource_capacity",
                        "custom embodiment profiles must use declared_subset capability projection",
                        entity_id=entity_id,
                        actual=projection_mode,
                    )
                )
            feature_facts = entity.get("feature_facts")
            if not isinstance(feature_facts, list):
                errors.append(issue("universal_identity_core", "feature_facts must be a list", entity_id=entity_id))
                feature_facts = []
            for fact in feature_facts:
                errors.extend(
                    _literal_request_phrases(
                        fact,
                        request_text,
                        check="universal_identity_core",
                        fact_kind="identity feature fact",
                    )
                )
                if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                    identity_fact_ids.append(str(fact["id"]))
            entity_feature_ids = {
                str(fact["id"])
                for fact in feature_facts
                if isinstance(fact, dict) and _is_nonempty_string(fact.get("id"))
            }
            capabilities = entity.get("capabilities")
            if not isinstance(capabilities, list):
                errors.append(issue("universal_resource_capacity", "entity capabilities must be a list", entity_id=entity_id))
                capabilities = []
            for capability in capabilities:
                if not isinstance(capability, dict) or set(capability) != {
                    "id",
                    "capacity",
                    "state",
                    "source",
                    "source_fact_id",
                }:
                    errors.append(issue("universal_resource_capacity", "capability must have the exact scene-contract field set", entity_id=entity_id))
                    continue
                if not _is_nonempty_string(capability.get("id")) or not _closed_int(capability.get("capacity"), 0, 64):
                    errors.append(issue("universal_resource_capacity", "capability id/capacity is invalid", entity_id=entity_id))
                elif capability.get("id") not in UNIVERSAL_ENTITY_RESOURCE_KINDS:
                    errors.append(issue("universal_resource_capacity", "entity capability kind is outside the closed compatibility enum", entity_id=entity_id, resource_kind=capability.get("id")))
                if capability.get("state") not in ("available", "unavailable"):
                    errors.append(issue("universal_resource_capacity", "capability state is outside the closed enum", entity_id=entity_id))
                elif (capability.get("state") == "unavailable") != (capability.get("capacity") == 0):
                    errors.append(issue("universal_resource_capacity", "unavailable capability must have zero capacity and available capability must be positive", entity_id=entity_id, capability_id=capability.get("id")))
                if not _is_nonempty_string(capability.get("source")) or not _is_nonempty_string(capability.get("source_fact_id")):
                    errors.append(issue("universal_resource_capacity", "capability provenance must remain visible", entity_id=entity_id, capability_id=capability.get("id")))
                if _is_nonempty_string(capability.get("id")) and _closed_int(capability.get("capacity"), 0, 64):
                    capability_key = (str(entity_id), str(capability["id"]))
                    if capability_key in entity_capacity_by_owner_kind:
                        errors.append(issue("universal_resource_capacity", "entity capability ids must be unique", entity_id=entity_id, resource_kind=capability.get("id")))
                    entity_capacity_by_owner_kind[capability_key] = (
                        int(capability["capacity"]) if capability.get("state") == "available" else 0
                    )
                    entity_capacity_record_by_owner_kind[capability_key] = {
                        "capacity": capability.get("capacity"),
                        "state": capability.get("state"),
                        "source": capability.get("source"),
                        "source_fact_id": capability.get("source_fact_id"),
                    }
                source = capability.get("source")
                source_fact_id = capability.get("source_fact_id")
                if source not in ("explicit", "embodiment_profile"):
                    errors.append(issue("universal_resource_capacity", "capability source is outside the closed enum", entity_id=entity_id, capability_id=capability.get("id"), actual=source))
                elif source == "embodiment_profile" and source_fact_id != entity.get("embodiment_profile_id"):
                    errors.append(issue("universal_resource_capacity", "profile-derived capability must cite the frozen embodiment profile", entity_id=entity_id, capability_id=capability.get("id"), expected=entity.get("embodiment_profile_id"), actual=source_fact_id))
                elif source == "explicit" and source_fact_id not in entity_feature_ids:
                    errors.append(issue("universal_resource_capacity", "explicit capability must cite a literal-bound feature fact", entity_id=entity_id, capability_id=capability.get("id"), source_fact_id=source_fact_id))

        for collection_name in ("scene_facts", "forbidden_facts"):
            facts = identity.get(collection_name)
            if not isinstance(facts, list):
                errors.append(issue("universal_identity_core", f"identity_core.{collection_name} must be a list"))
                continue
            for fact in facts:
                errors.extend(
                    _literal_request_phrases(
                        fact,
                        request_text,
                        check="universal_identity_core",
                        fact_kind=collection_name[:-1].replace("_", " "),
                    )
                )
                if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                    identity_fact_ids.append(str(fact["id"]))

        capacities = identity.get("capability_capacities")
        if not isinstance(capacities, list):
            errors.append(issue("universal_resource_capacity", "capability_capacities must be a list"))
            capacities = []
        for capacity in capacities:
            expected_capacity_keys = {"entity_id", "resource_kind", "capacity", "state", "source", "source_fact_id"}
            if not isinstance(capacity, dict) or set(capacity) != expected_capacity_keys:
                errors.append(issue("universal_resource_capacity", "capability capacity must have the exact field set"))
                continue
            owner_id = capacity.get("entity_id")
            resource_kind = capacity.get("resource_kind")
            amount = capacity.get("capacity")
            if not _is_nonempty_string(owner_id) or not _is_nonempty_string(resource_kind) or not _closed_int(amount, 0, 64):
                errors.append(issue("universal_resource_capacity", "capability capacity owner, kind, or amount is invalid"))
                continue
            key = (str(owner_id), str(resource_kind))
            if key in capacity_by_owner_kind:
                errors.append(issue("universal_resource_capacity", "capability capacity keys must be unique", owner_id=owner_id, resource_kind=resource_kind))
            capacity_by_owner_kind[key] = int(amount) if capacity.get("state") == "available" else 0
            flattened_capacity_record_by_owner_kind[key] = {
                "capacity": capacity.get("capacity"),
                "state": capacity.get("state"),
                "source": capacity.get("source"),
                "source_fact_id": capacity.get("source_fact_id"),
            }
            if capacity.get("state") not in ("available", "unavailable"):
                errors.append(issue("universal_resource_capacity", "capability capacity state is outside the closed enum", owner_id=owner_id, resource_kind=resource_kind))
            elif (capacity.get("state") == "unavailable") != (amount == 0):
                errors.append(issue("universal_resource_capacity", "flattened unavailable capacity must be zero and available capacity positive", owner_id=owner_id, resource_kind=resource_kind))
            if not _is_nonempty_string(capacity.get("source")) or not _is_nonempty_string(capacity.get("source_fact_id")):
                errors.append(issue("universal_resource_capacity", "capability capacity provenance must remain visible", owner_id=owner_id, resource_kind=resource_kind))

            if owner_id == "scene":
                expected_scene_capacity = UNIVERSAL_SCENE_RESOURCE_CAPACITIES.get(str(resource_kind))
                if expected_scene_capacity is None:
                    errors.append(issue("universal_resource_capacity", "scene resource kind is outside the frozen budget enum", resource_kind=resource_kind))
                elif capacity.get("state") != "available" or amount != expected_scene_capacity:
                    errors.append(issue("universal_resource_capacity", "scene resource capacity must equal its frozen compatibility budget", resource_kind=resource_kind, expected=expected_scene_capacity, actual=amount, state=capacity.get("state")))
                if capacity.get("source") != "compatibility_budget" or capacity.get("source_fact_id") != f"compatibility:{resource_kind}":
                    errors.append(issue("universal_resource_capacity", "scene resource capacity must cite its frozen compatibility budget", resource_kind=resource_kind, source=capacity.get("source"), source_fact_id=capacity.get("source_fact_id")))
            elif owner_id not in entity_ids:
                errors.append(issue("universal_resource_capacity", "capability capacity owner must be an identity entity or scene", owner_id=owner_id))

        flattened_entity_records = {
            key: value
            for key, value in flattened_capacity_record_by_owner_kind.items()
            if key[0] in set(entity_ids)
        }
        if flattened_entity_records != entity_capacity_record_by_owner_kind:
            errors.append(
                issue(
                    "universal_resource_capacity",
                    "flattened entity capacities must exactly preserve capability value, state, and provenance",
                    expected={f"{owner}:{kind}": value for (owner, kind), value in sorted(entity_capacity_record_by_owner_kind.items())},
                    actual={f"{owner}:{kind}": value for (owner, kind), value in sorted(flattened_entity_records.items())},
                )
            )

    if len(entity_ids) != len(set(entity_ids)):
        errors.append(issue("universal_identity_core", "identity entity ids must be unique", ids=entity_ids))
    if len(identity_fact_ids) != len(set(identity_fact_ids)):
        errors.append(issue("universal_identity_core", "identity fact ids must be unique", ids=identity_fact_ids))

    participant_bindings = (
        embedded_contract.get("participant_bindings")
        if isinstance(embedded_contract, dict)
        else None
    )
    if not isinstance(participant_bindings, list):
        errors.append(
            issue(
                "universal_scene_contract",
                "embedded participant_bindings must be the ordered eight-role projection",
            )
        )
        participant_bindings = []
    participant_role_ids: list[str] = []
    known_entity_ids = set(entity_ids)
    for index, raw_binding in enumerate(participant_bindings):
        errors.extend(
            _exact_object_keys(
                raw_binding,
                UNIVERSAL_PARTICIPANT_BINDING_KEYS,
                check="universal_scene_contract",
                object_name=f"participant_bindings[{index}]",
            )
        )
        if not isinstance(raw_binding, dict):
            continue
        role_id = raw_binding.get("role_id")
        binding_entity_ids = _unique_string_list(raw_binding.get("entity_ids"))
        primary_entity_id = raw_binding.get("primary_entity_id")
        if role_id not in UNIVERSAL_ROLE_IDS:
            errors.append(
                issue(
                    "universal_scene_contract",
                    "participant binding role is outside the closed eight-role set",
                    index=index,
                    actual=role_id,
                )
            )
            continue
        participant_role_ids.append(str(role_id))
        if binding_entity_ids is None or binding_entity_ids != sorted(binding_entity_ids):
            errors.append(
                issue(
                    "universal_scene_contract",
                    "participant entity_ids must be a sorted unique string list",
                    role_id=role_id,
                    actual=raw_binding.get("entity_ids"),
                )
            )
            binding_entity_ids = []
        unknown_participants = sorted(set(binding_entity_ids) - known_entity_ids)
        if unknown_participants:
            errors.append(
                issue(
                    "universal_scene_contract",
                    "participant binding references an unknown identity entity",
                    role_id=role_id,
                    unknown=unknown_participants,
                )
            )
        if primary_entity_id is not None and (
            not _is_nonempty_string(primary_entity_id)
            or str(primary_entity_id) not in set(binding_entity_ids)
        ):
            errors.append(
                issue(
                    "universal_scene_contract",
                    "participant primary_entity_id must be null or one of its bound entities",
                    role_id=role_id,
                    actual=primary_entity_id,
                )
            )
        if role_id == "actor" and (
            not binding_entity_ids or not _is_nonempty_string(primary_entity_id)
        ):
            errors.append(
                issue(
                    "universal_scene_contract",
                    "actor participant binding requires a nonempty entity set and primary entity",
                    actual=raw_binding,
                )
            )
    if participant_role_ids != list(UNIVERSAL_ROLE_IDS):
        errors.append(
            issue(
                "universal_scene_contract",
                "participant_bindings must exactly follow the closed event-role order",
                expected=list(UNIVERSAL_ROLE_IDS),
                actual=participant_role_ids,
            )
        )

    slot_states = scene.get("slot_states")
    slot_by_id: dict[str, dict[str, Any]] = {}
    if not isinstance(slot_states, list):
        errors.append(issue("universal_slot_state", "slot_states must be a list"))
        slot_states = []
    for slot in slot_states:
        if not isinstance(slot, dict) or set(slot) != UNIVERSAL_SLOT_KEYS:
            errors.append(issue("universal_slot_state", "every slot state must have the exact scene-contract field set"))
            continue
        slot_id = slot.get("slot_id")
        state = slot.get("state")
        values = _unique_string_list(slot.get("value_ids"))
        phrases = _unique_string_list(slot.get("request_phrases"))
        raw_bindings = slot.get("value_phrase_bindings")
        value_bindings: list[dict[str, Any]] = []
        bindings_valid = isinstance(raw_bindings, list)
        if bindings_valid:
            for binding in raw_bindings:
                if not isinstance(binding, dict) or set(binding) != UNIVERSAL_VALUE_PHRASE_BINDING_KEYS:
                    bindings_valid = False
                    continue
                binding_value = binding.get("value_id")
                binding_phrases = _unique_string_list(binding.get("request_phrases"))
                if not _is_nonempty_string(binding_value) or not binding_phrases:
                    bindings_valid = False
                    continue
                anchor_failures = _semantic_anchor_group_shape_failures(
                    binding.get("semantic_anchor_groups"),
                    binding_phrases,
                    fixed=state == "fixed",
                    check="universal_slot_state",
                    object_name=(
                        f"slot {slot_id} value binding {binding_value} semantic_anchor_groups"
                    ),
                )
                if anchor_failures:
                    bindings_valid = False
                    errors.extend(anchor_failures)
                value_bindings.append(
                    {
                        "value_id": str(binding_value),
                        "request_phrases": binding_phrases,
                        "semantic_anchor_groups": binding.get("semantic_anchor_groups"),
                    }
                )
        if not bindings_valid:
            errors.append(
                issue(
                    "universal_slot_state",
                    "value_phrase_bindings must be exact value-to-nonempty-literal records",
                    slot_id=slot_id,
                )
            )
        if slot_id not in UNIVERSAL_SLOT_IDS:
            errors.append(issue("universal_slot_state", "slot_id is outside the closed enum", actual=slot_id))
            continue
        if slot_id in slot_by_id:
            errors.append(issue("universal_slot_state", "slot ids must be unique", slot_id=slot_id))
        slot_by_id[str(slot_id)] = slot
        if state not in UNIVERSAL_SLOT_STATES:
            errors.append(issue("universal_slot_state", "slot state is outside the closed enum", slot_id=slot_id, actual=state))
            continue
        if values is None or phrases is None:
            errors.append(issue("universal_slot_state", "slot values and request phrases must be unique string lists", slot_id=slot_id))
            continue
        if state == "open" and (values or phrases):
            errors.append(issue("universal_slot_state", "open slots cannot carry inferred fixed values or phrases", slot_id=slot_id))
        if state in ("fixed", "closed") and not phrases:
            errors.append(issue("universal_slot_state", "fixed and closed slots require literal request evidence", slot_id=slot_id))
        if state == "fixed" and not values:
            errors.append(issue("universal_slot_state", "fixed slots require at least one fixed value", slot_id=slot_id))
        if state == "closed" and values:
            errors.append(issue("universal_slot_state", "closed slots cannot contain selected values", slot_id=slot_id))
        if state == "fixed" and values is not None and phrases is not None and bindings_valid:
            binding_value_ids = [binding["value_id"] for binding in value_bindings]
            flattened_binding_phrases = [
                phrase
                for binding in value_bindings
                for phrase in binding["request_phrases"]
            ]
            if binding_value_ids != values:
                errors.append(
                    issue(
                        "universal_slot_state",
                        "fixed value_phrase_bindings must exactly follow value_ids order",
                        slot_id=slot_id,
                        expected=values,
                        actual=binding_value_ids,
                    )
                )
            if flattened_binding_phrases != phrases:
                errors.append(
                    issue(
                        "universal_slot_state",
                        "fixed value_phrase_bindings must partition request_phrases in exact order",
                        slot_id=slot_id,
                        expected=phrases,
                        actual=flattened_binding_phrases,
                    )
                )
            normalized_binding_phrases = [
                _normalized_literal_text(phrase)
                for phrase in flattened_binding_phrases
            ]
            if len(normalized_binding_phrases) != len(set(normalized_binding_phrases)):
                errors.append(
                    issue(
                        "universal_slot_state",
                        "fixed literal phrases may not be reused across value bindings",
                        slot_id=slot_id,
                    )
                )
            anchor_owner_by_text: dict[str, str] = {}
            for binding in value_bindings:
                for group in (
                    binding.get("semantic_anchor_groups")
                    if isinstance(binding.get("semantic_anchor_groups"), list)
                    else []
                ):
                    if not isinstance(group, dict):
                        continue
                    for alternative in _string_list(group.get("alternatives")) or []:
                        normalized_anchor = _normalized_literal_text(alternative)
                        prior_owner = anchor_owner_by_text.get(normalized_anchor)
                        if prior_owner is not None and prior_owner != binding["value_id"]:
                            errors.append(
                                issue(
                                    "universal_slot_state",
                                    "one semantic anchor cannot authorize multiple fixed values",
                                    slot_id=slot_id,
                                    alternative=alternative,
                                    prior_value_id=prior_owner,
                                    value_id=binding["value_id"],
                                )
                            )
                        anchor_owner_by_text[normalized_anchor] = binding["value_id"]
        elif state in {"open", "closed"} and value_bindings:
            errors.append(
                issue(
                    "universal_slot_state",
                    "open and closed slots cannot contain value_phrase_bindings",
                    slot_id=slot_id,
                )
            )
        normalized_request = _normalized_literal_text(request_text)
        missing_phrases = [
            phrase
            for phrase in phrases
            if _normalized_literal_text(phrase) not in normalized_request
        ]
        if missing_phrases:
            errors.append(issue("universal_slot_state", "slot request phrases must be literal request_text substrings", slot_id=slot_id, missing=missing_phrases))
    if set(slot_by_id) != set(UNIVERSAL_SLOT_IDS):
        errors.append(
            issue(
                "universal_slot_state",
                "slot_states must contain the exact six universal slots",
                missing=sorted(set(UNIVERSAL_SLOT_IDS) - set(slot_by_id)),
                extra=sorted(set(slot_by_id) - set(UNIVERSAL_SLOT_IDS)),
            )
        )
    if isinstance(embedded_contract, dict) and slot_states != embedded_contract.get("slot_states"):
        errors.append(
            issue(
                "universal_slot_state",
                "slot_states must exactly copy the embedded scene contract",
                expected=embedded_contract.get("slot_states"),
                actual=slot_states,
            )
        )

    selected_event = scene.get("selected_event")
    errors.extend(
        _exact_object_keys(
            selected_event,
            UNIVERSAL_EVENT_KEYS,
            check="universal_event_spine",
            object_name="universal_scene.selected_event",
        )
    )
    event_id = ""
    phase_id: Any = None
    event_edge_ids: set[str] = set()
    event_edge_endpoints: dict[str, tuple[str, str]] = {}
    event_edge_records: dict[str, dict[str, Any]] = {}
    role_by_id: dict[str, dict[str, Any]] = {}
    graph: dict[str, set[str]] = {}
    if isinstance(selected_event, dict):
        event_id = str(selected_event.get("event_id") or "")
        phase_id = selected_event.get("phase_id")
        if event_id != "event_01":
            errors.append(issue("universal_event_spine", "v3 must instantiate exactly the canonical event_01 root", actual=event_id))
        if not _is_nonempty_string(phase_id):
            errors.append(issue("universal_event_spine", "selected event must have exactly one nonempty phase_id"))
        roles = selected_event.get("roles")
        if not isinstance(roles, list):
            errors.append(issue("universal_event_spine", "selected_event.roles must be a list"))
            roles = []
        for role in roles:
            if not isinstance(role, dict) or set(role) != {"role_id", "value_id", "source", "source_id"}:
                errors.append(issue("universal_event_spine", "every event role must have the exact field set"))
                continue
            role_id = role.get("role_id")
            if role_id not in UNIVERSAL_ROLE_IDS:
                errors.append(issue("universal_event_spine", "event role is outside the closed enum", actual=role_id))
                continue
            if role_id in role_by_id:
                errors.append(issue("universal_event_spine", "event role ids must be unique", role_id=role_id))
            role_by_id[str(role_id)] = role
            if role.get("source") not in ("user_fixed", "runtime_selected") or not _is_nonempty_string(role.get("source_id")):
                errors.append(issue("universal_event_spine", "event role source must be typed and bound", role_id=role_id))
            if role_id in ("actor", "action") and not _is_nonempty_string(role.get("value_id")):
                errors.append(issue("universal_event_spine", "actor and action roles must be populated", role_id=role_id))
        if set(role_by_id) != set(UNIVERSAL_ROLE_IDS):
            errors.append(
                issue(
                    "universal_event_spine",
                    "selected event must expose the exact eight role records",
                    missing=sorted(set(UNIVERSAL_ROLE_IDS) - set(role_by_id)),
                    extra=sorted(set(role_by_id) - set(UNIVERSAL_ROLE_IDS)),
                )
            )
        embedded_roles = (
            embedded_contract.get("event_roles")
            if isinstance(embedded_contract, dict)
            and isinstance(embedded_contract.get("event_roles"), list)
            else []
        )
        for index, contract_role in enumerate(embedded_roles):
            errors.extend(
                _exact_object_keys(
                    contract_role,
                    UNIVERSAL_CONTRACT_EVENT_ROLE_KEYS,
                    check="universal_event_spine",
                    object_name=f"embedded event_roles[{index}]",
                )
            )
            if not isinstance(contract_role, dict):
                continue
            contract_state = contract_role.get("state")
            contract_phrases = _unique_string_list(
                contract_role.get("request_phrases")
            )
            if contract_state not in UNIVERSAL_SLOT_STATES or contract_phrases is None:
                errors.append(
                    issue(
                        "universal_event_spine",
                        "embedded event role state or literal phrase list is malformed",
                        index=index,
                    )
                )
                continue
            errors.extend(
                _semantic_anchor_group_shape_failures(
                    contract_role.get("semantic_anchor_groups"),
                    contract_phrases,
                    fixed=contract_state == "fixed",
                    check="universal_event_spine",
                    object_name=(
                        f"embedded event role {contract_role.get('role_id')} semantic_anchor_groups"
                    ),
                )
            )
        embedded_role_by_id = {
            str(role.get("role_id")): role
            for role in embedded_roles
            if isinstance(role, dict) and _is_nonempty_string(role.get("role_id"))
        }
        if set(embedded_role_by_id) != set(UNIVERSAL_ROLE_IDS):
            errors.append(
                issue(
                    "universal_event_spine",
                    "embedded scene contract must expose the exact eight event roles",
                    missing=sorted(set(UNIVERSAL_ROLE_IDS) - set(embedded_role_by_id)),
                    extra=sorted(set(embedded_role_by_id) - set(UNIVERSAL_ROLE_IDS)),
                )
            )
        for role_id, contract_role in embedded_role_by_id.items():
            selected_role = role_by_id.get(role_id)
            if selected_role is None:
                continue
            state = contract_role.get("state")
            fixed_value = contract_role.get("value_id")
            if state == "fixed" and (
                selected_role.get("value_id") != fixed_value
                or selected_role.get("source") != "user_fixed"
                or selected_role.get("source_id") != role_id
            ):
                errors.append(
                    issue(
                        "universal_event_spine",
                        "fixed event role must exactly preserve the embedded scene contract",
                        role_id=role_id,
                        expected_value=fixed_value,
                        actual=selected_role,
                    )
                )
            elif state == "closed" and (
                selected_role.get("value_id") is not None
                or selected_role.get("source") != "user_fixed"
                or selected_role.get("source_id") != role_id
            ):
                errors.append(
                    issue(
                        "universal_event_spine",
                        "closed event role must remain an empty user-fixed record",
                        role_id=role_id,
                        actual=selected_role,
                    )
                )
            elif state == "open" and selected_role.get("source") != "runtime_selected":
                errors.append(
                    issue(
                        "universal_event_spine",
                        "open event role must remain runtime-selected without user-fixed provenance",
                        role_id=role_id,
                        actual=selected_role,
                    )
                )
        prop_slot_record = slot_by_id.get("prop")
        if prop_slot_record is not None and prop_slot_record.get("state") == "closed":
            instrument_role = role_by_id.get("instrument") or {}
            if instrument_role.get("value_id") is not None:
                errors.append(
                    issue(
                        "universal_slot_state",
                        "a closed prop slot requires an empty instrument role",
                        actual=instrument_role.get("value_id"),
                    )
                )
        phase_role_record = role_by_id.get("phase") or {}
        if _is_nonempty_string(phase_id) and phase_role_record.get("value_id") != phase_id:
            errors.append(
                issue(
                    "universal_event_spine",
                    "selected event phase_id must exactly equal the populated phase role value",
                    expected=phase_id,
                    actual=phase_role_record.get("value_id"),
                )
            )
        if _is_nonempty_string(_mapping(role_by_id.get("instrument")).get("value_id")) and not _is_nonempty_string(_mapping(role_by_id.get("target")).get("value_id")):
            errors.append(issue("universal_event_spine", "an instrument role requires a populated affected target"))
        if _is_nonempty_string(_mapping(role_by_id.get("recipient")).get("value_id")) and not _is_nonempty_string(_mapping(role_by_id.get("target")).get("value_id")):
            errors.append(issue("universal_event_spine", "a recipient/handoff role requires a populated directed target"))
        edges = selected_event.get("spine_edges")
        if not isinstance(edges, list) or not edges:
            errors.append(issue("universal_event_spine", "selected event must expose a nonempty connected spine"))
            edges = []
        for edge in edges:
            if not isinstance(edge, dict) or set(edge) != {"edge_id", "from_node_id", "relation_id", "to_node_id"}:
                errors.append(issue("universal_event_spine", "every spine edge must have the exact field set"))
                continue
            edge_id = edge.get("edge_id")
            from_node = edge.get("from_node_id")
            to_node = edge.get("to_node_id")
            if not all(_is_nonempty_string(value) for value in (edge_id, from_node, edge.get("relation_id"), to_node)):
                errors.append(issue("universal_event_spine", "spine edge fields must be nonempty strings"))
                continue
            if edge_id in event_edge_ids:
                errors.append(issue("universal_event_spine", "spine edge ids must be unique", edge_id=edge_id))
            event_edge_ids.add(str(edge_id))
            event_edge_endpoints[str(edge_id)] = (str(from_node), str(to_node))
            event_edge_records[str(edge_id)] = edge
            graph.setdefault(str(from_node), set()).add(str(to_node))
            graph.setdefault(str(to_node), set()).add(str(from_node))
            for node in (str(from_node), str(to_node)):
                if re.fullmatch(r"event_[0-9]+", node) and node != event_id:
                    errors.append(issue("universal_event_spine", "a second event root is forbidden", event_id=node))

    fixed_prop_profiles: list[dict[str, Any]] = []
    fixed_prop_slot = _mapping(slot_by_id.get("prop"))
    fixed_prop_values = set(_string_list(fixed_prop_slot.get("value_ids")) or [])
    if fixed_prop_slot.get("state") == "fixed":
        for candidate_id, aliases in UNIVERSAL_FIXED_PROP_ATOMS.items():
            matched_values = sorted(aliases & fixed_prop_values)
            if not matched_values:
                continue
            preserved_role_nodes = [
                str(role_by_id[role_id]["value_id"])
                for role_id in ("target", "instrument")
                if role_id in role_by_id
                and role_by_id[role_id].get("value_id") in aliases
            ]
            fixed_prop_profiles.append(
                {
                    "candidate_id": candidate_id,
                    "matched_values": matched_values,
                    "role_nodes": preserved_role_nodes,
                    "distance_vector": UNIVERSAL_FIXED_PROP_DISTANCE_VECTORS[candidate_id],
                }
            )

    atoms_raw = scene.get("atoms")
    atoms = atoms_raw if isinstance(atoms_raw, list) else []
    if not isinstance(atoms_raw, list) or not atoms:
        errors.append(issue("universal_candidate_eligibility", "universal_scene.atoms must be a nonempty list"))
    atom_by_id: dict[str, dict[str, Any]] = {}
    fixed_prop_atom_ids: set[str] = set()
    all_atom_pixel_ids: set[str] = set()
    all_atom_claim_ids: set[str] = set()
    derived_closed_facets: set[str] = set()
    expression_state = _mapping(slot_by_id.get("expression")).get("state")
    pose_state = _mapping(slot_by_id.get("pose")).get("state")
    action_state = _mapping(slot_by_id.get("action")).get("state")
    relation_state = _mapping(slot_by_id.get("relation")).get("state")
    prop_state = _mapping(slot_by_id.get("prop")).get("state")
    if expression_state != "open":
        derived_closed_facets.add("perceived_affect")
    if pose_state == "closed":
        derived_closed_facets.add("gesture")
    result_role_for_state = role_by_id.get("result")
    result_is_fixed = (
        isinstance(result_role_for_state, dict)
        and result_role_for_state.get("source") == "user_fixed"
        and _is_nonempty_string(result_role_for_state.get("value_id"))
    )
    if action_state == "closed":
        derived_closed_facets.add("phase")
        if not result_is_fixed:
            derived_closed_facets.add("consequence")
    if relation_state == "closed":
        derived_closed_facets.add("contact")
    if prop_state == "closed":
        derived_closed_facets.add("prop_state")
    attention_kinds = ("attention_channel", "head_orientation", "body_orientation")
    declared_attention = [
        capacity
        for (owner, kind), capacity in capacity_by_owner_kind.items()
        if kind in attention_kinds
    ]
    if declared_attention and max(declared_attention) == 0:
        derived_closed_facets.add("attention")
    phase_role = role_by_id.get("phase")
    if isinstance(phase_role, dict) and phase_role.get("source") == "user_fixed":
        derived_closed_facets.add("phase")
    for atom in atoms:
        errors.extend(
            _exact_object_keys(
                atom,
                UNIVERSAL_ATOM_KEYS,
                check="universal_candidate_eligibility",
                object_name="universal atom",
            )
        )
        if not isinstance(atom, dict):
            continue
        instance_id = atom.get("instance_id")
        candidate_id = atom.get("candidate_id")
        facet = atom.get("facet")
        is_literal_realization = (
            isinstance(atom.get("parameters"), dict)
            and _is_nonempty_string(
                atom["parameters"].get("literal_realization_profile_id")
            )
        )
        if not _is_nonempty_string(instance_id) or not _is_nonempty_string(candidate_id):
            errors.append(issue("universal_candidate_eligibility", "atom instance_id and candidate_id must be nonempty strings"))
            continue
        if instance_id in atom_by_id:
            errors.append(issue("universal_candidate_eligibility", "atom instance ids must be unique", instance_id=instance_id))
        atom_by_id[str(instance_id)] = atom
        if facet not in UNIVERSAL_FACET_IDS:
            errors.append(issue("universal_candidate_eligibility", "atom facet is outside the closed enum", instance_id=instance_id, facet=facet))
        slot = slot_by_id.get(str(facet))
        fixed_prop_values = set(_string_list(_mapping(slot_by_id.get("prop")).get("value_ids")) or [])
        is_preserved_fixed_prop = (
            facet == "prop"
            and _mapping(slot_by_id.get("prop")).get("state") == "fixed"
            and bool(UNIVERSAL_FIXED_PROP_ATOMS.get(str(candidate_id), set()) & fixed_prop_values)
        )
        if is_preserved_fixed_prop:
            fixed_prop_atom_ids.add(str(instance_id))
        if (
            slot is not None
            and slot.get("state") in ("fixed", "closed")
            and not is_preserved_fixed_prop
            and not is_literal_realization
        ):
            errors.append(
                issue(
                    "universal_slot_state",
                    "runtime atoms cannot add to or replace a user-fixed/closed slot",
                    slot_id=facet,
                    state=slot.get("state"),
                    instance_id=instance_id,
                )
            )
        if facet in derived_closed_facets and not is_literal_realization:
            errors.append(
                issue(
                    "universal_slot_state",
                    "selected atom violates a derived fixed/closed facet state",
                    facet=facet,
                    instance_id=instance_id,
                )
            )
        bindings = atom.get("bindings")
        if not isinstance(bindings, list) or not bindings:
            errors.append(issue("universal_candidate_eligibility", "selected atom must retain at least one typed event binding", instance_id=instance_id))
        else:
            for binding in bindings:
                if not isinstance(binding, dict) or set(binding) != {"role_id", "node_id", "requirement"}:
                    errors.append(issue("universal_candidate_eligibility", "atom binding must have the exact field set", instance_id=instance_id))
                    continue
                if binding.get("role_id") not in UNIVERSAL_ROLE_IDS or binding.get("requirement") not in ("required", "optional") or not _is_nonempty_string(binding.get("node_id")):
                    errors.append(issue("universal_candidate_eligibility", "atom binding is outside the closed role/requirement contract", instance_id=instance_id))
                    continue
                bound_role = role_by_id.get(str(binding.get("role_id")))
                expected_node = bound_role.get("value_id") if isinstance(bound_role, dict) else None
                if binding.get("node_id") != expected_node:
                    errors.append(
                        issue(
                            "universal_event_spine",
                            "atom binding node must exactly equal the selected event-role value",
                            instance_id=instance_id,
                            role_id=binding.get("role_id"),
                            expected=expected_node,
                            actual=binding.get("node_id"),
                        )
                    )
        edge_ids = _unique_string_list(atom.get("event_edge_ids"))
        if not edge_ids:
            errors.append(issue("universal_event_spine", "every selected atom must connect to the event spine", instance_id=instance_id))
        elif len(edge_ids) != 1:
            errors.append(issue("universal_event_spine", "each atom must own exactly one direct realization edge", instance_id=instance_id, event_edge_ids=edge_ids))
        elif not set(edge_ids).issubset(event_edge_ids):
            errors.append(issue("universal_event_spine", "atom references an unknown event edge", instance_id=instance_id, unknown=sorted(set(edge_ids) - event_edge_ids)))
        elif not any(str(instance_id) in event_edge_endpoints.get(edge_id, ()) for edge_id in edge_ids):
            errors.append(issue("universal_event_spine", "atom event_edge_ids do not attach the atom instance to the spine", instance_id=instance_id, event_edge_ids=edge_ids))
        elif not any(
            event_edge_endpoints.get(edge_id) == (event_id, str(instance_id))
            and event_edge_records.get(edge_id, {}).get("relation_id") == f"realizes:{facet}"
            for edge_id in edge_ids
        ):
            errors.append(issue("universal_event_spine", "atom must retain its direct typed event-to-instance realization edge", instance_id=instance_id, facet=facet, event_edge_ids=edge_ids))
        claim_ids = _unique_string_list(atom.get("resource_claim_ids"))
        if claim_ids is None:
            errors.append(issue("universal_resource_capacity", "atom resource_claim_ids must be a unique string list", instance_id=instance_id))
        else:
            all_atom_claim_ids.update(claim_ids)
        pixel_ids = _unique_string_list(atom.get("pixel_evidence_ids"))
        if not pixel_ids:
            errors.append(issue("universal_pixel_evidence", "every selected visual atom must expose a future pixel obligation", instance_id=instance_id))
        else:
            all_atom_pixel_ids.update(pixel_ids)
        vector = atom.get("distance_vector")
        band = _universal_distance_band(vector) if isinstance(vector, dict) else None
        if band is None or atom.get("distance_band") != band:
            errors.append(issue("universal_semantic_distance", "atom distance vector must recompute to its recorded band", instance_id=instance_id, expected=band, actual=atom.get("distance_band")))
        load = atom.get("load_vector")
        if not isinstance(load, dict) or set(load) != set(UNIVERSAL_LOAD_AXES) or any(not _closed_int(load.get(axis), 0, 3) for axis in UNIVERSAL_LOAD_AXES):
            errors.append(issue("universal_candidate_eligibility", "atom load_vector must contain the exact eight ordinal axes", instance_id=instance_id))
    eligible_counts = selection.get("eligible_count_by_facet") if isinstance(selection, dict) else None
    if isinstance(eligible_counts, dict):
        for instance_id, atom in atom_by_id.items():
            facet = atom.get("facet")
            if not _closed_int(eligible_counts.get(facet), 1, 10**9):
                errors.append(
                    issue(
                        "universal_candidate_eligibility",
                        "selected atom facet has no visible eligible candidate count",
                        instance_id=instance_id,
                        facet=facet,
                        eligible_count=eligible_counts.get(facet),
                    )
                )
    for role_id, role in role_by_id.items():
        if role.get("source") == "user_fixed" and role.get("source_id") != role_id:
            errors.append(
                issue(
                    "universal_slot_state",
                    "user-fixed event role must retain its contract role id as source_id",
                    role_id=role_id,
                    actual=role.get("source_id"),
                )
            )
    selected_proposal_ids = {
        str(atom["parameters"]["proposal_id"])
        for atom in atom_by_id.values()
        if isinstance(atom.get("parameters"), dict)
        and _is_nonempty_string(atom["parameters"].get("proposal_id"))
    }
    if len(selected_proposal_ids) > 1:
        errors.append(
            issue(
                "universal_candidate_budget",
                "one event may select at most one optional proposal premise",
                proposal_ids=sorted(selected_proposal_ids),
            )
        )

    bridges_raw = scene.get("bridges")
    bridges = bridges_raw if isinstance(bridges_raw, list) else []
    if not isinstance(bridges_raw, list):
        errors.append(issue("universal_bridge_contract", "universal_scene.bridges must be a list"))
    bridge_by_id: dict[str, dict[str, Any]] = {}
    all_bridge_pixel_ids: set[str] = set()
    for bridge in bridges:
        errors.extend(
            _exact_object_keys(
                bridge,
                UNIVERSAL_BRIDGE_KEYS,
                check="universal_bridge_contract",
                object_name="universal bridge",
            )
        )
        if not isinstance(bridge, dict):
            continue
        bridge_id = bridge.get("bridge_id")
        if not _is_nonempty_string(bridge_id) or not _is_nonempty_string(bridge.get("candidate_id")):
            errors.append(issue("universal_bridge_contract", "bridge_id and candidate_id must be nonempty strings"))
            continue
        if bridge_id in bridge_by_id:
            errors.append(issue("universal_bridge_contract", "bridge ids must be unique", bridge_id=bridge_id))
        bridge_by_id[str(bridge_id)] = bridge
        if not _is_nonempty_string(bridge.get("bridge_type")) or not _is_nonempty_string(bridge.get("from_node_id")) or not _is_nonempty_string(bridge.get("to_node_id")):
            errors.append(issue("universal_bridge_contract", "bridge endpoints and type must be nonempty strings", bridge_id=bridge_id))
        edge_ids = _unique_string_list(bridge.get("event_edge_ids"))
        if not edge_ids:
            errors.append(issue("universal_event_spine", "every selected bridge must connect to the event spine", bridge_id=bridge_id))
        elif len(edge_ids) != 1:
            errors.append(issue("universal_event_spine", "each bridge must own exactly one directed bridge edge", bridge_id=bridge_id, event_edge_ids=edge_ids))
        elif not set(edge_ids).issubset(event_edge_ids):
            errors.append(issue("universal_event_spine", "bridge references an unknown event edge", bridge_id=bridge_id, unknown=sorted(set(edge_ids) - event_edge_ids)))
        elif not any(
            event_edge_endpoints.get(edge_id) == (str(bridge.get("from_node_id")), str(bridge.get("to_node_id")))
            for edge_id in edge_ids
        ):
            errors.append(issue("universal_event_spine", "bridge event_edge_ids do not bind its directed endpoints", bridge_id=bridge_id, event_edge_ids=edge_ids))
        elif not any(
            event_edge_records.get(edge_id, {}).get("relation_id") == f"bridge:{bridge.get('bridge_type')}"
            for edge_id in edge_ids
        ):
            errors.append(issue("universal_event_spine", "bridge edge relation must exactly bind its closed bridge type", bridge_id=bridge_id, bridge_type=bridge.get("bridge_type")))
        pixel_ids = _unique_string_list(bridge.get("pixel_evidence_ids"))
        if not pixel_ids:
            errors.append(issue("universal_pixel_evidence", "every selected bridge must expose a future pixel obligation", bridge_id=bridge_id))
        else:
            all_bridge_pixel_ids.update(pixel_ids)

    for role_id, role in role_by_id.items():
        source_id = role.get("source_id")
        if (
            role.get("source") == "runtime_selected"
            and _is_nonempty_string(role.get("value_id"))
            and source_id not in atom_by_id
            and source_id not in bridge_by_id
            and not (
                role_id in {"actor", "location"}
                and _is_nonempty_string(source_id)
                and str(source_id).startswith("identity_entity:")
            )
        ):
            errors.append(
                issue(
                    "universal_candidate_eligibility",
                    "nonnull runtime-selected event role must cite a selected atom, bridge, or scoped identity source",
                    role_id=role_id,
                    source_id=source_id,
                )
            )

    allowed_relation_ids = {
        *(f"has_role:{role_id}" for role_id in UNIVERSAL_ROLE_IDS),
        *(f"realizes:{facet}" for facet in UNIVERSAL_FACET_IDS),
        *(f"bridge:{bridge_type}" for bridge_type in (UNIVERSAL_BRIDGE_ENTRY_TYPES | UNIVERSAL_BRIDGE_MEDIATION_TYPES | UNIVERSAL_BRIDGE_EXIT_TYPES)),
    }
    for edge_id, edge in event_edge_records.items():
        if edge.get("relation_id") not in allowed_relation_ids:
            errors.append(issue("universal_event_spine", "spine relation is outside the closed role/atom/bridge enum", edge_id=edge_id, relation_id=edge.get("relation_id")))
    for role_id, role in role_by_id.items():
        role_value = role.get("value_id")
        matching_edges = [
            edge
            for edge in event_edge_records.values()
            if edge.get("relation_id") == f"has_role:{role_id}"
        ]
        if not _is_nonempty_string(role_value):
            if matching_edges:
                errors.append(issue("universal_event_spine", "empty event role cannot retain a role edge", role_id=role_id, edge_count=len(matching_edges)))
            continue
        expected_endpoints = (event_id, str(role_value))
        if len(matching_edges) != 1 or (
            str(matching_edges[0].get("from_node_id")),
            str(matching_edges[0].get("to_node_id")),
        ) != expected_endpoints:
            errors.append(
                issue(
                    "universal_event_spine",
                    "populated event role requires exactly one directed event-root role edge",
                    role_id=role_id,
                    value_id=role_value,
                    expected_endpoints=expected_endpoints,
                    actual_edges=matching_edges,
                )
            )

    owned_edge_ids: set[str] = set()
    edge_owner_counts: dict[str, int] = {}
    for role_id in UNIVERSAL_ROLE_IDS:
        for edge_id, edge in event_edge_records.items():
            if edge.get("relation_id") == f"has_role:{role_id}":
                owned_edge_ids.add(edge_id)
                edge_owner_counts[edge_id] = edge_owner_counts.get(edge_id, 0) + 1
    for atom in atom_by_id.values():
        for edge_id in _string_list(atom.get("event_edge_ids")) or []:
            owned_edge_ids.add(edge_id)
            edge_owner_counts[edge_id] = edge_owner_counts.get(edge_id, 0) + 1
    for bridge in bridge_by_id.values():
        for edge_id in _string_list(bridge.get("event_edge_ids")) or []:
            owned_edge_ids.add(edge_id)
            edge_owner_counts[edge_id] = edge_owner_counts.get(edge_id, 0) + 1
    if owned_edge_ids != event_edge_ids:
        errors.append(
            issue(
                "universal_event_spine",
                "every spine edge must be owned by exactly one role, atom, or bridge record",
                unowned=sorted(event_edge_ids - owned_edge_ids),
                unknown_owned=sorted(owned_edge_ids - event_edge_ids),
            )
        )
    multiply_owned = {
        edge_id: count
        for edge_id, count in edge_owner_counts.items()
        if count != 1
    }
    if multiply_owned:
        errors.append(
            issue(
                "universal_event_spine",
                "each spine edge must have exactly one typed owner",
                ownership_counts=multiply_owned,
            )
        )

    resources_raw = scene.get("resource_claims")
    resources = resources_raw if isinstance(resources_raw, list) else []
    if not isinstance(resources_raw, list):
        errors.append(issue("universal_resource_capacity", "resource_claims must be a list"))
    resource_by_id: dict[str, dict[str, Any]] = {}
    exclusive_usage: dict[tuple[str, str], int] = {}
    shared_usage: dict[tuple[str, str], int] = {}
    for claim in resources:
        errors.extend(
            _exact_object_keys(
                claim,
                UNIVERSAL_RESOURCE_CLAIM_KEYS,
                check="universal_resource_capacity",
                object_name="universal resource claim",
            )
        )
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("claim_id")
        owner_id = claim.get("owner_id")
        resource_kind = claim.get("resource_kind")
        claimant_id = claim.get("claimant_id")
        if not all(_is_nonempty_string(value) for value in (claim_id, owner_id, resource_kind, claimant_id)):
            errors.append(issue("universal_resource_capacity", "resource claim identifiers must be nonempty strings"))
            continue
        if claim_id in resource_by_id:
            errors.append(issue("universal_resource_capacity", "resource claim ids must be unique", claim_id=claim_id))
        resource_by_id[str(claim_id)] = claim
        if not _closed_int(claim.get("amount"), 1, 64) or claim.get("mode") not in ("exclusive", "shared"):
            errors.append(issue("universal_resource_capacity", "resource amount/mode is outside the closed contract", claim_id=claim_id))
            continue
        if claim.get("phase_id") != phase_id:
            errors.append(issue("universal_resource_capacity", "resource claim phase must equal the single event phase", claim_id=claim_id, expected=phase_id, actual=claim.get("phase_id")))
        if not isinstance(claim.get("evidence_required"), bool):
            errors.append(issue("universal_resource_capacity", "evidence_required must be boolean", claim_id=claim_id))
        key = (str(owner_id), str(resource_kind))
        if claim.get("mode") == "exclusive":
            exclusive_usage[key] = exclusive_usage.get(key, 0) + int(claim["amount"])
        else:
            # The one-event spine has one resolved target.  Shared claims are
            # same-target observations and consume the maximum shared amount,
            # while exclusive claims remain additive.
            shared_usage[key] = max(shared_usage.get(key, 0), int(claim["amount"]))
        if claimant_id not in atom_by_id:
            errors.append(issue("universal_resource_capacity", "resource claimant must be a selected atom", claim_id=claim_id, claimant_id=claimant_id))
    if set(resource_by_id) != all_atom_claim_ids:
        errors.append(
            issue(
                "universal_resource_capacity",
                "atom resource_claim_ids must exactly expose all selected resource claims",
                missing=sorted(set(resource_by_id) - all_atom_claim_ids),
                extra=sorted(all_atom_claim_ids - set(resource_by_id)),
            )
        )
    for instance_id, atom in atom_by_id.items():
        declared = set(_string_list(atom.get("resource_claim_ids")) or [])
        owned = {
            claim_id
            for claim_id, claim in resource_by_id.items()
            if claim.get("claimant_id") == instance_id
        }
        if declared != owned:
            errors.append(
                issue(
                    "universal_resource_capacity",
                    "each atom must exactly bind only its own resource claims",
                    instance_id=instance_id,
                    missing=sorted(owned - declared),
                    foreign_or_extra=sorted(declared - owned),
                )
            )
    for key in set(exclusive_usage) | set(shared_usage):
        amount = exclusive_usage.get(key, 0) + shared_usage.get(key, 0)
        capacity = capacity_by_owner_kind.get(key)
        if capacity is None:
            errors.append(issue("universal_resource_capacity", "resource claim has no visible capability capacity", owner_id=key[0], resource_kind=key[1]))
        elif amount > capacity:
            errors.append(issue("universal_resource_capacity", "resource claims exceed visible capability capacity", owner_id=key[0], resource_kind=key[1], used=amount, capacity=capacity))

    distance = scene.get("semantic_distance_trace")
    errors.extend(
        _exact_object_keys(
            distance,
            UNIVERSAL_DISTANCE_TRACE_KEYS,
            check="universal_semantic_distance",
            object_name="universal_scene.semantic_distance_trace",
        )
    )
    selected_band: Any = None
    target_band: Any = None
    remote_atom_ids: list[str] = []
    if isinstance(distance, dict):
        recorded_creativity = distance.get("creativity")
        request_creativity = request.get("creativity")
        target_band = _creativity_band(recorded_creativity)
        selected_band = _universal_distance_band(distance.get("vector")) if isinstance(distance.get("vector"), dict) else None
        if distance.get("policy_id") != "typed_ordinal_distance_v1":
            errors.append(issue("universal_semantic_distance", "distance policy_id must equal the frozen typed ordinal policy", actual=distance.get("policy_id")))
        if recorded_creativity != request_creativity:
            errors.append(issue("universal_semantic_distance", "distance trace creativity must exactly copy request creativity", expected=request_creativity, actual=recorded_creativity))
        if target_band is None or distance.get("target_band") != target_band:
            errors.append(issue("universal_semantic_distance", "target band must recompute from numeric creativity", expected=target_band, actual=distance.get("target_band")))
        if selected_band is None or distance.get("selected_band") != selected_band:
            errors.append(issue("universal_semantic_distance", "selected band must recompute from the seven-axis trace vector", expected=selected_band, actual=distance.get("selected_band")))
        expected_vector = {
            axis: max(
                [
                    int(atom["distance_vector"][axis])
                    for atom in atom_by_id.values()
                    if isinstance(atom.get("distance_vector"), dict)
                    and _closed_int(atom["distance_vector"].get(axis), 0, 3)
                ]
                + [
                    int(profile["distance_vector"][axis])
                    for profile in fixed_prop_profiles
                ],
                default=0,
            )
            for axis in UNIVERSAL_DISTANCE_AXES
        }
        if distance.get("vector") != expected_vector:
            errors.append(
                issue(
                    "universal_semantic_distance",
                    "trace vector must be the component-wise maximum of selected atom vectors, including preserved catalog props",
                    expected=expected_vector,
                    actual=distance.get("vector"),
                )
            )
        theme_value = expected_vector["theme"]
        expected_theme_band = "far" if theme_value == 3 else ("middle" if theme_value == 2 else "near")
        if distance.get("theme_displacement_band") != expected_theme_band:
            errors.append(
                issue(
                    "universal_semantic_distance",
                    "theme_displacement_band must recompute from the theme axis",
                    expected=expected_theme_band,
                    actual=distance.get("theme_displacement_band"),
                )
            )
        band_rank = {"near": 0, "middle": 1, "far": 2}
        fixed_bands = [
            _universal_distance_band(profile["distance_vector"])
            for profile in fixed_prop_profiles
        ]
        fixed_preservation_exceeds_target = (
            target_band in band_rank
            and selected_band in band_rank
            and any(
                fixed_band in band_rank
                and band_rank[fixed_band] > band_rank[target_band]
                for fixed_band in fixed_bands
            )
            and distance.get("optional_remote_count") == 0
        )
        coherent_bundle_fallback = (
            target_band in band_rank
            and selected_band in band_rank
            and distance.get("fallback_reason")
            == f"no_coherent_{target_band}_bundle_selected_{selected_band}"
        )
        allowed_by_target = {"near": {"near"}, "middle": {"near", "middle"}, "far": {"near", "middle", "far"}}
        if (
            target_band in allowed_by_target
            and selected_band not in allowed_by_target[target_band]
            and not fixed_preservation_exceeds_target
            and not coherent_bundle_fallback
        ):
            errors.append(issue("universal_semantic_distance", "selected distance exceeds the creativity target gate", target_band=target_band, selected_band=selected_band))
        maximum = 1
        if distance.get("max_optional_remote_count") != maximum:
            errors.append(issue("universal_semantic_distance", "the global optional remote budget must equal one", expected=maximum, actual=distance.get("max_optional_remote_count")))
        fixed_count = distance.get("fixed_remote_count")
        optional_count = distance.get("optional_remote_count")
        if not _closed_int(fixed_count, 0, 64) or not _closed_int(optional_count, 0, 1):
            errors.append(issue("universal_semantic_distance", "remote counts must be nonnegative integers and optional count at most one"))
        elif optional_count > maximum:
            errors.append(issue("universal_semantic_distance", "optional remote premise exceeds the creativity-band budget", optional_remote_count=optional_count, maximum=maximum))
        remote_atom_ids = _unique_string_list(distance.get("remote_atom_ids")) or []
        if _unique_string_list(distance.get("remote_atom_ids")) is None or not set(remote_atom_ids).issubset(atom_by_id):
            errors.append(issue("universal_semantic_distance", "remote_atom_ids must be a unique selected-atom list", unknown=sorted(set(remote_atom_ids) - set(atom_by_id))))
        far_atom_ids = {
            instance_id
            for instance_id, atom in atom_by_id.items()
            if atom.get("distance_band") == "far"
        }
        expected_remote_ids = far_atom_ids
        minimum_fixed_count = sum(
            _universal_distance_band(profile["distance_vector"]) == "far"
            for profile in fixed_prop_profiles
        )
        if set(remote_atom_ids) != expected_remote_ids:
            errors.append(
                issue(
                    "universal_semantic_distance",
                    "remote_atom_ids must exactly list every far selected atom",
                    expected=sorted(expected_remote_ids),
                    actual=remote_atom_ids,
                )
            )
        if _closed_int(fixed_count, 0, 64) and fixed_count != minimum_fixed_count:
            errors.append(
                issue(
                    "universal_semantic_distance",
                    "fixed_remote_count must exactly count user-fixed far catalog props",
                    expected=minimum_fixed_count,
                    actual=fixed_count,
                )
            )
        proposal_high_load = any(
            isinstance(atom.get("parameters"), dict)
            and _is_nonempty_string(atom["parameters"].get("proposal_id"))
            and isinstance(atom.get("load_vector"), dict)
            and max(
                (
                    value
                    for value in atom["load_vector"].values()
                    if _closed_int(value, 0, 3)
                ),
                default=0,
            )
            == 3
            for atom in atom_by_id.values()
        )
        expected_optional_count = 1 if far_atom_ids or proposal_high_load else 0
        if _closed_int(optional_count, 0, 1) and optional_count != expected_optional_count:
            errors.append(
                issue(
                    "universal_semantic_distance",
                    "optional_remote_count must exactly count the selected far or high-load optional augmentation",
                    expected=expected_optional_count,
                    actual=optional_count,
                )
            )
        if (
            _closed_int(fixed_count, 0, 64)
            and _closed_int(optional_count, 0, 1)
            and fixed_count + optional_count > 1
        ):
            errors.append(
                issue(
                    "universal_semantic_distance",
                    "fixed plus optional remote/high-load premises exceed the one-premise budget",
                    fixed_remote_count=fixed_count,
                    optional_remote_count=optional_count,
                )
            )
        fallback = distance.get("fallback_reason")
        if selected_band == target_band and fallback is not None:
            errors.append(issue("universal_semantic_distance", "fallback_reason must be null when the target band was selected", actual=fallback))
        if selected_band != target_band and not _is_nonempty_string(fallback):
            errors.append(issue("universal_semantic_distance", "band mismatch must retain a concrete fallback reason", target_band=target_band, selected_band=selected_band))
        if fixed_preservation_exceeds_target and minimum_fixed_count > 0 and fallback != "user_fixed_remote_preserved":
            errors.append(
                issue(
                    "universal_semantic_distance",
                    "fixed far-prop target override must retain its typed preservation reason",
                    expected="user_fixed_remote_preserved",
                    actual=fallback,
                )
            )

    pixel = scene.get("pixel_evidence_contract")
    errors.extend(
        _exact_object_keys(
            pixel,
            UNIVERSAL_PIXEL_EVIDENCE_KEYS,
            check="universal_pixel_evidence",
            object_name="universal_scene.pixel_evidence_contract",
        )
    )
    pixel_ids: list[str] = []
    pixel_item_by_id: dict[str, dict[str, Any]] = {}
    core_anchor_ids: list[str] = []
    pixel_category_ids: dict[str, list[str]] = {}
    if isinstance(pixel, dict):
        scales = _unique_string_list(pixel.get("required_scale_ids"))
        if not scales or not {"native", "thumbnail_320px"}.issubset(scales):
            errors.append(issue("universal_pixel_evidence", "required scales must include native and thumbnail_320px", actual=pixel.get("required_scale_ids")))
        items = pixel.get("items")
        pixel_ids, item_errors = _pixel_item_ids(items)
        errors.extend(item_errors)
        if isinstance(items, list):
            for item in items:
                if not isinstance(item, dict):
                    errors.append(issue("universal_pixel_evidence", "pixel items must be typed obligation objects, not bare prompt claims"))
                    continue
                expected_item_keys = {"item_id", "source_kind", "source_id", "kind", "minimum_scale_ids", "status"}
                if set(item) != expected_item_keys:
                    errors.append(issue("universal_pixel_evidence", "pixel obligation must have the exact future-review field set", item_id=item.get("item_id")))
                if _is_nonempty_string(item.get("item_id")):
                    pixel_item_by_id[str(item["item_id"])] = item
                if item.get("source_kind") not in ("core_anchor", "event", "atom", "bridge", "consequence"):
                    errors.append(issue("universal_pixel_evidence", "pixel source_kind is outside the closed enum", item_id=item.get("item_id"), actual=item.get("source_kind")))
                if not _is_nonempty_string(item.get("source_id")) or not _is_nonempty_string(item.get("kind")):
                    errors.append(issue("universal_pixel_evidence", "pixel obligation source and kind must be nonempty", item_id=item.get("item_id")))
                if not _unique_string_list(item.get("minimum_scale_ids")):
                    errors.append(issue("universal_pixel_evidence", "pixel obligation minimum_scale_ids must be a nonempty unique string list", item_id=item.get("item_id")))
                if item.get("status") != "future_review_required":
                    errors.append(issue("universal_pixel_evidence", "pre-render pixel evidence must remain a future review obligation", item_id=item.get("item_id"), actual=item.get("status")))
        if scales:
            scale_set = set(scales)
            item_scale_union: set[str] = set()
            for item in pixel_item_by_id.values():
                item_scales = set(_string_list(item.get("minimum_scale_ids")) or [])
                item_scale_union.update(item_scales)
                if not item_scales.issubset(scale_set):
                    errors.append(
                        issue(
                            "universal_pixel_evidence",
                            "pixel item minimum scales must be a subset of required_scale_ids",
                            item_id=item.get("item_id"),
                            unknown=sorted(item_scales - scale_set),
                        )
                    )
            if item_scale_union != scale_set:
                errors.append(
                    issue(
                        "universal_pixel_evidence",
                        "required_scale_ids must exactly equal the selected item-scale union",
                        expected=sorted(item_scale_union),
                        actual=scales,
                    )
                )
        pixel_id_set = set(pixel_ids)
        for field in ("core_anchor_item_ids", "event_item_ids", "contact_item_ids", "consequence_item_ids"):
            ids = _unique_string_list(pixel.get(field))
            if ids is None or not set(ids).issubset(pixel_id_set):
                errors.append(issue("universal_pixel_evidence", f"{field} must be a unique subset of pixel obligation ids", unknown=sorted(set(ids or []) - pixel_id_set)))
            pixel_category_ids[field] = ids or []
            if field == "core_anchor_item_ids":
                core_anchor_ids = ids or []
        if not pixel_category_ids.get("core_anchor_item_ids"):
            errors.append(issue("universal_pixel_evidence", "every scene requires a future core-identity anchor review obligation"))
        if not pixel_category_ids.get("event_item_ids"):
            errors.append(issue("universal_pixel_evidence", "every scene requires a future actor-action event review obligation"))
        if any(atom.get("facet") == "contact" for atom in atom_by_id.values()) and not pixel_category_ids.get("contact_item_ids"):
            errors.append(issue("universal_pixel_evidence", "selected contact atom requires a future contact review obligation"))
        if _is_nonempty_string(_mapping(role_by_id.get("result")).get("value_id")) and not pixel_category_ids.get("consequence_item_ids"):
            errors.append(issue("universal_pixel_evidence", "populated result role requires a future consequence review obligation"))
        for field, expected_source_kinds in (
            ("core_anchor_item_ids", {"core_anchor"}),
            ("event_item_ids", {"event"}),
            # A consequence category may point either to a dedicated event
            # consequence obligation or to a selected atom whose visible
            # residue/state is the consequence.  Ownership remains exact
            # below through source_id and the atom's declared evidence IDs.
            ("consequence_item_ids", {"atom", "consequence"}),
        ):
            for item_id in pixel_category_ids.get(field, []):
                item = pixel_item_by_id.get(item_id)
                if item is not None and item.get("source_kind") not in expected_source_kinds:
                    errors.append(issue("universal_pixel_evidence", "pixel category item has the wrong typed source kind", field=field, item_id=item_id, expected=sorted(expected_source_kinds), actual=item.get("source_kind")))
        result_value = _mapping(role_by_id.get("result")).get("value_id")
        for item_id in pixel_category_ids.get("core_anchor_item_ids", []):
            item = pixel_item_by_id.get(item_id)
            if item is not None and (
                item.get("kind") != "display"
                or item.get("source_id") not in set(identity_fact_ids)
            ):
                errors.append(
                    issue(
                        "universal_pixel_evidence",
                        "core-anchor item must bind a literal identity fact and display evidence",
                        item_id=item_id,
                        source_id=item.get("source_id"),
                        kind=item.get("kind"),
                    )
                )
        for item_id in pixel_category_ids.get("event_item_ids", []):
            item = pixel_item_by_id.get(item_id)
            if item is not None and (
                item.get("source_id") != event_id
                or item.get("kind") != "path"
            ):
                errors.append(
                    issue(
                        "universal_pixel_evidence",
                        "event item must bind the single event root and path evidence",
                        item_id=item_id,
                        expected_source_id=event_id,
                        actual_source_id=item.get("source_id"),
                        kind=item.get("kind"),
                    )
                )
        for item_id in pixel_category_ids.get("contact_item_ids", []):
            item = pixel_item_by_id.get(item_id)
            source_atom = atom_by_id.get(str(item.get("source_id"))) if item is not None else None
            if item is not None and (
                item.get("source_kind") != "atom"
                or source_atom is None
                or item.get("kind") not in {"contact", "support"}
                or item_id not in (_string_list(source_atom.get("pixel_evidence_ids")) or [])
            ):
                errors.append(
                    issue(
                        "universal_pixel_evidence",
                        "contact category must bind contact evidence owned by one selected atom",
                        item_id=item_id,
                        source_kind=item.get("source_kind"),
                        source_id=item.get("source_id"),
                        kind=item.get("kind"),
                    )
                )
        for item_id in pixel_category_ids.get("consequence_item_ids", []):
            item = pixel_item_by_id.get(item_id)
            if item is None:
                continue
            source_kind = item.get("source_kind")
            if source_kind == "consequence":
                valid_consequence = (
                    _is_nonempty_string(result_value)
                    and item.get("source_id") == result_value
                    and item.get("kind") == "state_boundary"
                )
            else:
                source_atom = atom_by_id.get(str(item.get("source_id")))
                valid_consequence = (
                    source_kind == "atom"
                    and source_atom is not None
                    and (
                        source_atom.get("facet") in {"consequence", "prop_state"}
                        or item.get("kind") in {"residue", "state_boundary"}
                    )
                    and item.get("kind") in {"residue", "state_boundary"}
                    and item_id in (_string_list(source_atom.get("pixel_evidence_ids")) or [])
                )
            if not valid_consequence:
                errors.append(
                    issue(
                        "universal_pixel_evidence",
                        "consequence category must bind the event result or owned consequence/state residue",
                        item_id=item_id,
                        source_kind=source_kind,
                        source_id=item.get("source_id"),
                        kind=item.get("kind"),
                    )
                )
        referenced_pixel_ids = all_atom_pixel_ids | all_bridge_pixel_ids
        if not referenced_pixel_ids.issubset(pixel_id_set):
            errors.append(issue("universal_pixel_evidence", "atoms or bridges reference unknown pixel obligations", unknown=sorted(referenced_pixel_ids - pixel_id_set)))
        if not set(pixel_ids).issubset(referenced_pixel_ids | set(core_anchor_ids) | set(pixel.get("event_item_ids") or []) | set(pixel.get("consequence_item_ids") or [])):
            errors.append(issue("universal_pixel_evidence", "pixel obligations must be owned by an atom, bridge, core anchor, event, or consequence", orphan=sorted(set(pixel_ids) - referenced_pixel_ids - set(core_anchor_ids) - set(pixel.get("event_item_ids") or []) - set(pixel.get("consequence_item_ids") or []))))
        for instance_id, atom in atom_by_id.items():
            for item_id in _string_list(atom.get("pixel_evidence_ids")) or []:
                item = pixel_item_by_id.get(item_id)
                expected_source_kinds = {"atom"}
                if atom.get("facet") == "consequence":
                    expected_source_kinds.add("consequence")
                if item is not None and (
                    item.get("source_kind") not in expected_source_kinds
                    or item.get("source_id") != instance_id
                ):
                    errors.append(
                        issue(
                            "universal_pixel_evidence",
                            "atom pixel evidence must be owned by that exact atom instance",
                            instance_id=instance_id,
                            item_id=item_id,
                            expected_source_kinds=sorted(expected_source_kinds),
                            actual_source_kind=item.get("source_kind"),
                            actual_source_id=item.get("source_id"),
                        )
                    )
        for bridge_id, bridge in bridge_by_id.items():
            for item_id in _string_list(bridge.get("pixel_evidence_ids")) or []:
                item = pixel_item_by_id.get(item_id)
                if item is not None and (item.get("source_kind"), item.get("source_id")) != ("bridge", bridge_id):
                    errors.append(
                        issue(
                            "universal_pixel_evidence",
                            "bridge pixel evidence must be owned by that exact bridge instance",
                            bridge_id=bridge_id,
                            item_id=item_id,
                            actual_source_kind=item.get("source_kind"),
                            actual_source_id=item.get("source_id"),
                        )
                    )

    bridge_types = {str(bridge.get("bridge_type")) for bridge in bridges if isinstance(bridge, dict)}
    closed_bridge_types = UNIVERSAL_BRIDGE_ENTRY_TYPES | UNIVERSAL_BRIDGE_MEDIATION_TYPES | UNIVERSAL_BRIDGE_EXIT_TYPES
    unknown_bridge_types = sorted(bridge_types - closed_bridge_types)
    if unknown_bridge_types:
        errors.append(issue("universal_bridge_contract", "bridge type is outside the closed compatibility enum", unknown=unknown_bridge_types))
    if selected_band == "near" and len(bridge_types) < 1:
        errors.append(issue("universal_bridge_contract", "near distance requires at least one direct typed bridge", actual=sorted(bridge_types)))
    if selected_band == "middle":
        missing_classes: list[str] = []
        if not bridge_types & UNIVERSAL_BRIDGE_ENTRY_TYPES:
            missing_classes.append("entry")
        if not bridge_types & UNIVERSAL_BRIDGE_EXIT_TYPES:
            missing_classes.append("exit")
        if len(bridge_types) < 2 or missing_classes:
            errors.append(
                issue(
                    "universal_bridge_contract",
                    "middle distance requires distinct entry and exit bridge classes",
                    missing=missing_classes,
                    actual=sorted(bridge_types),
                )
            )
    if selected_band == "far":
        missing_classes: list[str] = []
        if not bridge_types & UNIVERSAL_BRIDGE_ENTRY_TYPES:
            missing_classes.append("entry")
        if not bridge_types & UNIVERSAL_BRIDGE_MEDIATION_TYPES:
            missing_classes.append("mediation")
        if not bridge_types & UNIVERSAL_BRIDGE_EXIT_TYPES:
            missing_classes.append("exit")
        if missing_classes:
            errors.append(issue("universal_bridge_contract", "far distance requires entry, mediation, and exit bridge classes", missing=missing_classes, actual=sorted(bridge_types)))
        if not core_anchor_ids:
            errors.append(issue("universal_bridge_contract", "far distance requires a separate visible core identity anchor"))

    bridge_adjacency: dict[str, list[tuple[str, str]]] = {}
    for bridge in bridges:
        if not isinstance(bridge, dict):
            continue
        left = bridge.get("from_node_id")
        right = bridge.get("to_node_id")
        bridge_type = bridge.get("bridge_type")
        if not all(_is_nonempty_string(value) for value in (left, right, bridge_type)):
            continue
        bridge_adjacency.setdefault(str(left), []).append((str(right), str(bridge_type)))

    def bridge_path_satisfies(
        start_node: str,
        end_node: str,
        required_node: str,
        required_categories: tuple[set[str], ...],
        minimum_types: int,
    ) -> bool:
        if not start_node or not end_node or start_node not in bridge_adjacency:
            return False
        pending_paths: list[tuple[str, frozenset[str], frozenset[str]]] = [
            (start_node, frozenset({start_node}), frozenset())
        ]
        visited_states: set[tuple[str, frozenset[str], frozenset[str]]] = set()
        while pending_paths:
            node, visited_nodes, used_types = pending_paths.pop()
            state = (node, visited_nodes, used_types)
            if state in visited_states:
                continue
            visited_states.add(state)
            if node == end_node:
                if (
                    required_node in visited_nodes
                    and len(used_types) >= minimum_types
                    and all(used_types & category for category in required_categories)
                ):
                    return True
            for neighbor, bridge_type in bridge_adjacency.get(node, []):
                next_types = used_types | {bridge_type}
                if neighbor == node and next_types != used_types:
                    pending_paths.append((node, visited_nodes, next_types))
                    continue
                if neighbor in visited_nodes:
                    continue
                pending_paths.append(
                    (
                        neighbor,
                        visited_nodes | {neighbor},
                        next_types,
                    )
                )
        return False

    for instance_id, atom in atom_by_id.items():
        band = atom.get("distance_band")
        actor_path_node = str(_mapping(role_by_id.get("actor")).get("value_id") or "")
        if instance_id in fixed_prop_atom_ids:
            fixed_values = set(_string_list(_mapping(slot_by_id.get("prop")).get("value_ids")) or [])
            preserved_role = next(
                (
                    role_by_id[role_id]
                    for role_id in ("target", "instrument")
                    if role_by_id.get(role_id, {}).get("value_id") in fixed_values
                ),
                {},
            )
            path_end = str(preserved_role.get("value_id") or "")
        else:
            path_end = str(_mapping(role_by_id.get("result")).get("value_id") or "")
        if (
            band == "middle"
            and instance_id not in fixed_prop_atom_ids
            and not bridge_path_satisfies(
            actor_path_node,
            path_end,
            instance_id,
            (UNIVERSAL_BRIDGE_ENTRY_TYPES, UNIVERSAL_BRIDGE_EXIT_TYPES),
            2,
            )
        ):
            errors.append(
                issue(
                    "universal_bridge_contract",
                    "each middle atom requires its own event path with entry and exit bridge classes",
                    instance_id=instance_id,
                    path_start=actor_path_node,
                    path_end=path_end,
                )
            )
        if (
            band == "far"
            and instance_id not in fixed_prop_atom_ids
            and not bridge_path_satisfies(
            actor_path_node,
            path_end,
            instance_id,
            (
                UNIVERSAL_BRIDGE_ENTRY_TYPES,
                UNIVERSAL_BRIDGE_MEDIATION_TYPES,
                UNIVERSAL_BRIDGE_EXIT_TYPES,
            ),
            3,
            )
        ):
            errors.append(
                issue(
                    "universal_bridge_contract",
                    "each far atom or fixed prop requires its own event path with entry, mediation, and exit bridge classes",
                    instance_id=instance_id,
                    path_start=actor_path_node,
                    path_end=path_end,
                )
            )

    actor_path_node = str(_mapping(role_by_id.get("actor")).get("value_id") or "")
    result_path_node = str(_mapping(role_by_id.get("result")).get("value_id") or "")
    for profile in fixed_prop_profiles:
        profile_band = _universal_distance_band(profile["distance_vector"])
        if profile_band not in ("middle", "far"):
            continue
        role_nodes = profile.get("role_nodes") or []
        if len(role_nodes) != 1:
            errors.append(
                issue(
                    "universal_slot_state",
                    "a known fixed catalog prop must retain one exact target or instrument role binding",
                    candidate_id=profile.get("candidate_id"),
                    matched_values=profile.get("matched_values"),
                    role_nodes=role_nodes,
                )
            )
            continue
        categories = (
            (UNIVERSAL_BRIDGE_ENTRY_TYPES, UNIVERSAL_BRIDGE_EXIT_TYPES)
            if profile_band == "middle"
            else (
                UNIVERSAL_BRIDGE_ENTRY_TYPES,
                UNIVERSAL_BRIDGE_MEDIATION_TYPES,
                UNIVERSAL_BRIDGE_EXIT_TYPES,
            )
        )
        if not bridge_path_satisfies(
            actor_path_node,
            result_path_node,
            role_nodes[0],
            categories,
            len(categories),
        ):
            errors.append(
                issue(
                    "universal_bridge_contract",
                    "a middle/far fixed catalog prop requires its own serial event bridge path",
                    candidate_id=profile.get("candidate_id"),
                    prop_node=role_nodes[0],
                    distance_band=profile_band,
                    path_start=actor_path_node,
                    path_end=result_path_node,
                )
            )

    if event_id:
        visited: set[str] = set()
        pending = [event_id]
        while pending:
            node = pending.pop()
            if node in visited:
                continue
            visited.add(node)
            pending.extend(sorted(graph.get(node, set()) - visited))
        graph_nodes = set(graph)
        if graph_nodes and not graph_nodes.issubset(visited):
            errors.append(issue("universal_event_spine", "selected event spine is disconnected", disconnected=sorted(graph_nodes - visited)))

    _, _, carrier_errors = _universal_composition_carrier_contract(scene)
    errors.extend(carrier_errors)
    errors.extend(_universal_hard_gate_failures(pack, scene))

    asset_hashes = _mapping(pack.get("asset_hashes"))
    for field in (
        "universal_candidates_sha256",
        "universal_compatibility_sha256",
        "universal_semantic_bindings_sha256",
        "universal_research_manifest_sha256",
    ):
        if not _hex64(asset_hashes.get(field)):
            errors.append(issue("universal_asset_binding", "v3 universal asset hash is missing or malformed", field=field, actual=asset_hashes.get(field)))
    errors.extend(_runtime_universal_revalidation_failures(pack, scene, request_text))
    return errors


def validate_pack_integrity(pack: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Validate the complete compact graph and format proof embedded in a pack."""

    errors: list[dict[str, Any]] = []
    pack_id = pack.get("pack_id")
    expected_id = computed_pack_id(pack)
    if not isinstance(pack_id, str) or not re.fullmatch(r"[0-9a-f]{16}", pack_id):
        errors.append(issue("pack_integrity", "pack_id must be 16 lowercase hexadecimal characters", actual=pack_id))
    if pack_id != expected_id:
        errors.append(issue("pack_integrity", "candidate pack content does not match canonical pack_id", expected=expected_id, actual=pack_id))

    if pack.get("contract_version") not in SUPPORTED_CONTRACT_VERSIONS:
        errors.append(
            issue(
                "pack_contract",
                "unsupported or missing candidate-pack contract_version",
                expected=list(SUPPORTED_CONTRACT_VERSIONS),
                actual=pack.get("contract_version"),
            )
        )
    elif pack.get("contract_version") in (CONTRACT_VERSION, CONTRACT_VERSION_V2):
        legacy_v3_leaks: list[str] = []
        if "universal_scene" in pack:
            legacy_v3_leaks.append("universal_scene")
        request_value = pack.get("request_contract")
        if isinstance(request_value, dict):
            legacy_v3_leaks.extend(
                f"request_contract.{field}"
                for field in (
                    "scene_contract_schema",
                    "scene_contract_sha256",
                    "prior_exposure_ids",
                )
                if field in request_value
            )
        asset_hash_value = pack.get("asset_hashes")
        if isinstance(asset_hash_value, dict):
            legacy_v3_leaks.extend(
                f"asset_hashes.{field}"
                for field in (
                    "universal_candidates_sha256",
                    "universal_compatibility_sha256",
                    "universal_semantic_bindings_sha256",
                    "universal_research_manifest_sha256",
                )
                if field in asset_hash_value
            )
        if legacy_v3_leaks:
            errors.append(
                issue(
                    "pack_contract",
                    "legacy contract version cannot retain v3-only scene fields",
                    fields=legacy_v3_leaks,
                )
            )

    request = pack.get("request_contract")
    if not isinstance(request, dict):
        errors.append(issue("request_contract", "request_contract must be an object"))
        request = {}
    route_id = request.get("route_id")
    if not _is_nonempty_string(route_id):
        errors.append(issue("request_contract", "route_id must be a nonempty string"))

    if not _is_nonempty_string(pack.get("negative_en")):
        errors.append(issue("pack_contract", "negative_en must be a nonempty string"))

    profile = pack.get("format_profile")
    if not isinstance(profile, dict):
        errors.append(issue("format_contract", "format_profile must be an object"))
        profile = {}
    variant_id = profile.get("variant_id")
    family_id = profile.get("family_id")
    if variant_id not in VARIANT_FAMILY:
        errors.append(issue("format_contract", "unknown format variant", actual=variant_id, known=sorted(VARIANT_FAMILY)))
    elif family_id != VARIANT_FAMILY[variant_id]:
        errors.append(issue("format_contract", "format family does not match variant", variant_id=variant_id, expected=VARIANT_FAMILY[variant_id], actual=family_id))
    for aliases in FORMAT_CONTRACT_KEY_GROUPS:
        present = [key for key in aliases if isinstance(profile.get(key), dict)]
        if not present:
            errors.append(issue("format_contract", "compact format contract group must embed an object", accepted_fields=list(aliases)))
    embedded_format_fields = _profile_required_evidence_fields(profile)
    lifecycle_evidence_types = _string_list(profile.get("required_evidence_types"))
    if lifecycle_evidence_types is None:
        errors.append(issue("format_contract", "required_evidence_types must be a string list of lifecycle qualification types"))
        lifecycle_evidence_types = []
    if not embedded_format_fields:
        errors.append(issue("format_contract", "format profile must embed required non-ratio evidence fields"))
    elif all(field in ASPECT_ONLY_KEYS for field in embedded_format_fields):
        errors.append(issue("format_contract", "format profile substitutes aspect ratio for typed format behavior", fields=embedded_format_fields))
    elif variant_id in FORMAT_REQUIRED_FIELDS:
        missing_canonical = sorted(set(FORMAT_REQUIRED_FIELDS[variant_id]) - set(embedded_format_fields))
        if missing_canonical:
            errors.append(issue("format_contract", "embedded format requirements omit canonical typed evidence", missing=missing_canonical))
    leaked_lifecycle_fields = sorted(
        field
        for field in embedded_format_fields
        if field in set(lifecycle_evidence_types)
        or field in NON_COMPOSITION_EVIDENCE_KEYS
        or POST_RENDER_EVIDENCE_KEY_PATTERN.search(field)
    )
    if leaked_lifecycle_fields:
        errors.append(
            issue(
                "format_contract",
                "post-render or lifecycle qualification types cannot be required composed-prompt fields",
                fields=leaked_lifecycle_fields,
            )
        )

    grammar = pack.get("visual_grammar")
    if not isinstance(grammar, dict):
        errors.append(issue("visual_grammar", "visual_grammar must be an object"))
        grammar = {}
    if not _is_nonempty_string(grammar.get("topic_id")):
        errors.append(issue("visual_grammar", "visual_grammar.topic_id must be a nonempty string"))
    elif route_id and grammar.get("topic_id") != route_id:
        errors.append(issue("visual_grammar", "visual_grammar topic must match request route", route_id=route_id, topic_id=grammar.get("topic_id")))
    if not _is_nonempty_string(grammar.get("family_id")):
        errors.append(issue("visual_grammar", "visual_grammar.family_id must be a nonempty string"))
    raw_nodes = grammar.get("runtime_nodes")
    if not isinstance(raw_nodes, list) or any(not isinstance(node, dict) for node in raw_nodes):
        errors.append(issue("visual_grammar", "runtime_nodes must be a list of objects"))
        raw_nodes = []
    nodes = [node for node in raw_nodes if isinstance(node, dict)]
    if not 1 <= len(nodes) <= 3:
        errors.append(issue("visual_grammar", "runtime bundle must contain one to three nodes", count=len(nodes)))

    node_ids = [str(node.get("id") or "") for node in nodes]
    if any(not node_id for node_id in node_ids):
        errors.append(issue("visual_grammar", "every runtime node must have a nonempty id"))
    if len(node_ids) != len(set(node_ids)):
        errors.append(issue("visual_grammar", "runtime node ids must be unique", ids=node_ids))

    primary_ids: list[str] = []
    support_ids: list[str] = []
    available_evidence: set[str] = set()
    for node in nodes:
        node_id = str(node.get("id") or "")
        node_type = node.get("node_type")
        role = node.get("selected_role")
        if node_type != "visual_atom":
            errors.append(issue("typed_candidate_boundary", "selected runtime node is not a visual_atom", node_id=node_id, node_type=node_type))
        if role == "primary":
            primary_ids.append(node_id)
        elif role == "support":
            support_ids.append(node_id)
        else:
            errors.append(issue("visual_grammar", "runtime node selected_role must be primary or support", node_id=node_id, selected_role=role))
        if not _is_nonempty_string(node.get("definition")):
            errors.append(issue("visual_grammar", "runtime node must embed a nonempty definition", node_id=node_id))
        evidence_types = _string_list(node.get("observable_evidence_types"))
        if not evidence_types:
            errors.append(issue("visual_grammar", "runtime node must embed observable evidence types", node_id=node_id))
        else:
            available_evidence.update(evidence_types)
            phase_invalid = sorted(
                evidence_type
                for evidence_type in evidence_types
                if evidence_type in NON_COMPOSITION_EVIDENCE_KEYS
                or POST_RENDER_EVIDENCE_KEY_PATTERN.search(evidence_type)
            )
            if phase_invalid:
                errors.append(issue("visual_grammar", "visual atoms cannot expose post-render qualification evidence", node_id=node_id, evidence_types=phase_invalid))
        format_families = _string_list(node.get("format_family_ids"))
        if not format_families:
            errors.append(issue("visual_grammar", "runtime node must embed applicable format families", node_id=node_id))
        elif family_id not in format_families:
            errors.append(issue("visual_grammar", "runtime node is not applicable to the selected format family", node_id=node_id, family_id=family_id, allowed=format_families))

    if len(primary_ids) != 1:
        errors.append(issue("sparse_visual_bundle", "runtime bundle must have exactly one primary visual atom", primary_ids=primary_ids))
    if len(support_ids) > 2:
        errors.append(issue("sparse_visual_bundle", "runtime bundle may expose at most two support visual atoms", support_ids=support_ids))
    if grammar.get("primary_runtime_id") != (primary_ids[0] if len(primary_ids) == 1 else None):
        errors.append(issue("sparse_visual_bundle", "primary_runtime_id does not match the primary runtime node", declared=grammar.get("primary_runtime_id"), actual=primary_ids))
    declared_supports = _string_list(grammar.get("support_runtime_ids"))
    if declared_supports is None or set(declared_supports) != set(support_ids) or len(declared_supports) != len(support_ids):
        errors.append(issue("sparse_visual_bundle", "support_runtime_ids do not exactly match support runtime nodes", declared=grammar.get("support_runtime_ids"), actual=support_ids))
    max_support = grammar.get("max_support_cues")
    if isinstance(max_support, bool) or not isinstance(max_support, int) or not 0 <= max_support <= 2:
        errors.append(issue("sparse_visual_bundle", "max_support_cues must be an integer from zero to two", actual=max_support))
    elif len(support_ids) > max_support:
        errors.append(issue("sparse_visual_bundle", "selected support count exceeds max_support_cues", support_count=len(support_ids), max_support_cues=max_support))

    required_visual_evidence = _string_list(grammar.get("required_evidence_types"))
    if not required_visual_evidence:
        errors.append(issue("visual_grammar", "visual_grammar must embed required evidence types"))
    else:
        phase_invalid = sorted(
            evidence_type
            for evidence_type in required_visual_evidence
            if evidence_type in NON_COMPOSITION_EVIDENCE_KEYS
            or POST_RENDER_EVIDENCE_KEY_PATTERN.search(evidence_type)
        )
        if phase_invalid:
            errors.append(issue("visual_grammar", "post-render qualification cannot be required as pre-render visual evidence", evidence_types=phase_invalid))
        unavailable = sorted(set(required_visual_evidence) - available_evidence)
        if unavailable:
            errors.append(issue("visual_grammar", "required evidence is not supplied by the selected runtime nodes", unavailable=unavailable, available=sorted(available_evidence)))

    compatible_ids = _string_list(grammar.get("compatible_edge_ids"))
    if compatible_ids is None:
        errors.append(issue("compatibility_edge", "compatible_edge_ids must be a string list"))
        compatible_ids = []
    if len(nodes) > 1 and not compatible_ids:
        errors.append(issue("compatibility_edge", "multi-node bundle requires a declared compatibility edge"))

    edge = grammar.get("selected_edge")
    if not isinstance(edge, dict):
        errors.append(issue("compatibility_edge", "visual_grammar must embed selected_edge"))
    else:
        edge_id = edge.get("id")
        if not _is_nonempty_string(edge_id) or edge_id not in compatible_ids:
            errors.append(issue("compatibility_edge", "selected edge id is absent from compatible_edge_ids", edge_id=edge_id, compatible_edge_ids=compatible_ids))
        if edge.get("route_id") != route_id:
            errors.append(issue("compatibility_edge", "selected edge route does not match request route", expected=route_id, actual=edge.get("route_id")))
        edge_families = _string_list(edge.get("format_family_ids"))
        if not edge_families or family_id not in edge_families:
            errors.append(issue("compatibility_edge", "selected edge is not applicable to the format family", family_id=family_id, allowed=edge.get("format_family_ids")))
        if edge.get("primary_node_id") != grammar.get("primary_runtime_id"):
            errors.append(issue("compatibility_edge", "selected edge primary does not match visual_grammar", edge_primary=edge.get("primary_node_id"), grammar_primary=grammar.get("primary_runtime_id")))
        edge_supports = _string_list(edge.get("support_node_ids"))
        if edge_supports is None or set(edge_supports) != set(support_ids) or len(edge_supports) != len(support_ids):
            errors.append(issue("compatibility_edge", "selected edge supports do not exactly match runtime supports", edge_supports=edge.get("support_node_ids"), runtime_supports=support_ids))
        minimum = edge.get("minimum_supports")
        maximum = edge.get("maximum_supports")
        if isinstance(minimum, bool) or not isinstance(minimum, int) or isinstance(maximum, bool) or not isinstance(maximum, int) or not (0 <= minimum <= maximum <= 2):
            errors.append(issue("compatibility_edge", "selected edge support bounds must satisfy 0 <= minimum <= maximum <= 2", minimum=minimum, maximum=maximum))
        elif not minimum <= len(support_ids) <= maximum:
            errors.append(issue("compatibility_edge", "selected support count is outside selected edge bounds", support_count=len(support_ids), minimum=minimum, maximum=maximum))
        edge_evidence = _string_list(edge.get("required_evidence_types"))
        if not edge_evidence:
            errors.append(issue("compatibility_edge", "selected edge must embed required evidence types"))
        elif required_visual_evidence and not set(edge_evidence).issubset(set(required_visual_evidence)):
            errors.append(issue("compatibility_edge", "selected edge evidence is absent from visual_grammar requirements", edge_required=edge_evidence, grammar_required=required_visual_evidence))

    expected_ids = expected_chosen_candidate_ids(pack)
    composition_contract = pack.get("composition_contract")
    if not isinstance(composition_contract, dict):
        errors.append(issue("composition_contract", "composition_contract must be an object"))
    else:
        declared_ids = _string_list(composition_contract.get("required_chosen_candidate_ids"))
        if declared_ids is None or set(declared_ids) != set(expected_ids) or len(declared_ids) != len(expected_ids):
            errors.append(issue("composition_contract", "required_chosen_candidate_ids do not exactly match the compact pack selection", declared=composition_contract.get("required_chosen_candidate_ids"), expected=expected_ids))

    authorial_contract = pack.get("authorial_contract")
    if not isinstance(authorial_contract, dict):
        errors.append(issue("authorial_contract", "authorial_contract must be an object"))
    else:
        authorial_required = _string_list(authorial_contract.get("required_fields"))
        if authorial_required is None or not set(AUTHORIAL_REQUIRED_FIELDS).issubset(authorial_required):
            errors.append(issue("authorial_contract", "authorial_contract must embed all canonical authorial evidence fields", required=list(AUTHORIAL_REQUIRED_FIELDS), actual=authorial_contract.get("required_fields")))
        if not isinstance(authorial_contract.get("creative_development_required"), bool):
            errors.append(issue("authorial_contract", "creative_development_required must be boolean"))

    viewer_contract = pack.get("viewer_contract")
    if not isinstance(viewer_contract, dict):
        errors.append(issue("viewer_contract", "viewer_contract must be an object"))
    else:
        viewer_required = _string_list(viewer_contract.get("required_fields"))
        if viewer_required is None or not set(VIEWER_REQUIRED_FIELDS).issubset(viewer_required):
            errors.append(issue("viewer_contract", "viewer_contract must embed all canonical causal viewer fields", required=list(VIEWER_REQUIRED_FIELDS), actual=viewer_contract.get("required_fields")))

    safety = pack.get("safety")
    if not isinstance(safety, dict) or safety.get("status") != "pass" or safety.get("requires_user_approval") is True:
        errors.append(issue("safety_contract", "candidate pack safety must already be pass with no approval wait", safety=safety))

    guard = pack.get("guard_contract")
    if not isinstance(guard, dict):
        errors.append(issue("guard_contract", "guard_contract must be an object"))
    else:
        if _string_list(guard.get("guard_node_ids")) is None:
            errors.append(issue("guard_contract", "guard_node_ids must be a string list"))
        if _string_list(guard.get("router_node_ids")) is None:
            errors.append(issue("guard_contract", "router_node_ids must be a string list"))

    errors.extend(_second_look_pack_contract_failures(pack, profile))
    errors.extend(validate_universal_scene_integrity(pack))

    return errors


def _evidence_leaf_values(value: Any, path: str = "") -> Iterator[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            yield from _evidence_leaf_values(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _evidence_leaf_values(child, f"{path}[{index}]")
    else:
        yield path, value


def _phrase_is_literal(prompt_en: str, value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value in prompt_en


def audit_literal_evidence(
    prompt_en: str,
    section_name: str,
    section: Any,
    *,
    skipped_roots: Iterable[str] = (),
) -> list[dict[str, Any]]:
    """Require every visible-evidence scalar to be an exact prompt substring."""

    failures: list[dict[str, Any]] = []
    if not isinstance(section, dict):
        return [issue("evidence_shape", "evidence section must be an object", section=section_name)]
    skipped = set(skipped_roots)
    visible_section = {key: value for key, value in section.items() if key not in skipped}
    for path, value in _evidence_leaf_values(visible_section):
        full_path = f"{section_name}.{path}" if path else section_name
        if not isinstance(value, str):
            failures.append(issue("literal_evidence", "visible evidence leaf must be a string", field=full_path, actual_type=type(value).__name__))
        elif not value.strip():
            failures.append(issue("literal_evidence", "visible evidence phrase must be nonempty", field=full_path))
        elif value not in prompt_en:
            failures.append(issue("literal_evidence", "evidence phrase is not an exact literal substring of prompt_en", field=full_path, phrase=value))
    return failures


def _required_phrase_failures(
    section_name: str,
    section: Mapping[str, Any],
    required_fields: Iterable[str],
    prompt_en: str,
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for field in dict.fromkeys(required_fields):
        value = section.get(field)
        if not _is_nonempty_string(value):
            failures.append(issue("required_evidence", "required evidence phrase is missing", section=section_name, field=field))
        elif value not in prompt_en:
            failures.append(issue("literal_evidence", "required evidence phrase is not an exact literal substring of prompt_en", section=section_name, field=field, phrase=value))
    return failures


def _authorial_concreteness_failures(authorial: Mapping[str, Any]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    generic_only = {
        "beautiful",
        "cinematic",
        "detailed",
        "high quality",
        "masterpiece",
        "anime style",
        "stylized",
        "atmospheric",
    }
    for field in AUTHORIAL_REQUIRED_FIELDS:
        value = authorial.get(field)
        if not _is_nonempty_string(value):
            continue
        normalized = " ".join(re.findall(r"[A-Za-z0-9]+", str(value).casefold()))
        word_count = len(normalized.split())
        if normalized in generic_only or word_count < 3:
            failures.append(issue("authorial_grammar", "authorial evidence must state a concrete decision, not a style adjective", field=field, phrase=value))
    return failures


def _strict_chosen_ids(raw: Any) -> tuple[list[str], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    if not isinstance(raw, list):
        return [], [issue("chosen_candidate_ids", "chosen_candidate_ids must be a list of strings")]
    ids: list[str] = []
    for index, value in enumerate(raw):
        if not _is_nonempty_string(value):
            failures.append(issue("chosen_candidate_ids", "candidate id must be a nonempty string", index=index, actual=value))
        else:
            ids.append(str(value))
    if len(ids) != len(set(ids)):
        failures.append(issue("chosen_candidate_ids", "chosen_candidate_ids must not contain duplicates", ids=ids))
    return ids, failures


def _mandatory_intent_failures(pack: Mapping[str, Any], composed: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    request = _mapping(pack.get("request_contract"))
    intents = request.get("mandatory_intents") or []
    if not isinstance(intents, list):
        return [issue("mandatory_intent", "request_contract.mandatory_intents must be a list")]
    assertions = composed.get("coverage_assertions", {})
    if not isinstance(assertions, dict):
        return [issue("coverage_assertions", "coverage_assertions must be an object when supplied")]
    known_keys: set[str] = set()
    visual_evidence = _mapping(composed.get("visual_evidence"))
    for intent in intents:
        evidence_key = ""
        if isinstance(intent, str):
            text = intent
            terms = [intent]
        elif isinstance(intent, dict):
            text = str(intent.get("text") or intent.get("id") or "")
            evidence_key = str(intent.get("evidence_key") or "")
            raw_terms = _string_list(intent.get("audit_terms"))
            terms = raw_terms or ([text] if text else [])
        else:
            failures.append(issue("mandatory_intent", "mandatory intent must be a string or object", actual=intent))
            continue
        if not text:
            failures.append(issue("mandatory_intent", "mandatory intent must have a nonempty identity"))
            continue
        known_keys.add(text)
        asserted = assertions.get(text)
        assertion_phrases = [asserted] if isinstance(asserted, str) else (_string_list(asserted) or [])
        for phrase in assertion_phrases:
            if phrase not in prompt_en:
                failures.append(issue("coverage_assertions", "asserted mandatory-intent phrase is not literal in prompt_en", intent=text, phrase=phrase))
        bound_evidence = visual_evidence.get(evidence_key) if evidence_key else None
        evidence_covers = _phrase_is_literal(prompt_en, bound_evidence)
        if evidence_key and not evidence_covers:
            failures.append(issue("mandatory_intent", "mandatory-intent evidence_key has no literal visual_evidence phrase", intent=text, evidence_key=evidence_key))
        accepted = [term for term in terms if isinstance(term, str) and text_contains_term(prompt_en, term)]
        if not accepted and not assertion_phrases and not evidence_covers:
            failures.append(issue("mandatory_intent", "mandatory visible intent is absent from prompt_en", intent=text, accepted_terms=terms))
    for key in assertions:
        if str(key) not in known_keys:
            failures.append(issue("coverage_assertions", "assertion key is not a mandatory intent", intent=key))
    return failures


def _reference_boundary_failures(composed: Mapping[str, Any], prompt_en: str, pack: Mapping[str, Any]) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    boundary = composed.get("reference_boundary")
    if not isinstance(boundary, dict):
        return [issue("reference_boundary", "reference_boundary must be an object")]
    if boundary.get("original_design") is not True:
        failures.append(issue("reference_boundary", "original_design must be true"))
    for key in ("named_style_references", "protected_ip_references"):
        value = boundary.get(key)
        if not isinstance(value, list):
            failures.append(issue("reference_boundary", f"{key} must be a list"))
        elif value:
            failures.append(issue("reference_boundary", f"{key} must be empty", references=value))

    for pattern in NAMED_STYLE_PATTERNS:
        match = re.search(pattern, prompt_en, flags=re.IGNORECASE)
        if match:
            failures.append(issue("named_style_reference", "prompt uses a named-artist/studio style proof", excerpt=match.group(0)))
    for pattern in PROTECTED_IP_PATTERNS:
        match = re.search(pattern, prompt_en, flags=re.IGNORECASE)
        if match:
            failures.append(issue("protected_ip_reference", "prompt contains a protected-IP or logo reference", excerpt=match.group(0)))

    guard = _mapping(pack.get("guard_contract"))
    for key in ("forbidden_prompt_terms", "named_style_terms", "protected_ip_terms"):
        terms = _string_list(guard.get(key)) or []
        for term in terms:
            if term.casefold() in prompt_en.casefold():
                failures.append(issue("guard_contract", "prompt contains a pack-declared forbidden reference", category=key, term=term))
    return failures


def _policy_language_failures(prompt_en: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for pattern in UNIVERSAL_INFERENCE_PATTERNS:
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            match = matches[0]
            failures.append(issue("universal_inference", "prompt makes a universal color, shape, or cultural inference", excerpt=match.group(0)))
    for pattern in OUTCOME_CLAIM_PATTERNS:
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            match = matches[0]
            failures.append(issue("viewer_outcome_claim", "viewer response claim is not visible evidence", excerpt=match.group(0)))
    return failures


def _phase_boundary_failures(
    pack: Mapping[str, Any],
    composed: Mapping[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    """Reject post-render qualification claims in a pre-render composition."""

    failures: list[dict[str, Any]] = []
    profile = _mapping(pack.get("format_profile"))
    lifecycle_types = set(_string_list(profile.get("required_evidence_types")) or [])
    composition_fields = set(_profile_required_evidence_fields(profile))
    lifecycle_only = lifecycle_types - composition_fields

    for section_name in (
        "visual_evidence",
        "authorial_grammar",
        "viewer_evidence",
        "format_evidence",
    ):
        section = composed.get(section_name)
        if not isinstance(section, dict):
            continue
        for path, _value in _evidence_leaf_values(section):
            segments = [segment for segment in re.split(r"[.\[\]]+", path) if segment]
            for segment in segments:
                if segment in lifecycle_only or POST_RENDER_EVIDENCE_KEY_PATTERN.search(segment):
                    failures.append(
                        issue(
                            "phase_boundary",
                            "post-render or lifecycle qualification field cannot be claimed by a pre-render composed prompt",
                            section=section_name,
                            field=path,
                            lifecycle_field=segment,
                        )
                    )
                    break

    for pattern in POST_RENDER_CLAIM_PATTERNS:
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            failures.append(
                issue(
                    "phase_boundary",
                    "prompt claims a completed pixel or render review before image generation",
                    excerpt=matches[0].group(0),
                )
            )
    return failures


def _photo_dominance_failures(pack: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    request = _mapping(pack.get("request_contract"))
    request_text = str(request.get("request_text") or "")
    hybrid_requested = request.get("hybrid_medium_requested") is True or bool(
        re.search(r"\b(?:hybrid medium|photo[- ]illustration|photographic illustration|mixed photo and illustration)\b", request_text, flags=re.IGNORECASE)
    )
    if hybrid_requested:
        return []

    categories: dict[str, list[str]] = {}
    patterns: dict[str, str] = {
        "photo_medium": r"\b(?:photorealistic|photo-realistic|photographic|photograph|photo shoot|photo portrait)\b",
        "camera_body": r"\b(?:DSLR camera|mirrorless camera|shot on|captured (?:on|with)|(?:Leica|Canon|Nikon|Hasselblad)(?:\s+camera)?)\b",
        "lens_formula": r"\b(?:bokeh|depth of field|focal length|\d{2,3}\s*mm(?:\s+lens)?|telephoto lens|wide[- ]angle lens|macro lens)\b",
        "exposure_formula": r"\b(?:ISO\s*\d+|f\s*/\s*\d|shutter speed|aperture)\b",
    }
    for category, pattern in patterns.items():
        hits = [match.group(0) for match in re.finditer(pattern, prompt_en, flags=re.IGNORECASE)]
        if hits:
            categories[category] = hits
    begins_as_photo = re.search(r"^\s*(?:a |an )?(?:photorealistic |photographic )?(?:photo|photograph)\b", prompt_en, flags=re.IGNORECASE)
    equipment_formula = "exposure_formula" in categories or (
        "camera_body" in categories and "lens_formula" in categories
    )
    illustration_present = bool(re.search(r"\b(?:illustration|drawn|painted|inked|linework|cel[- ]shaded|artwork)\b", prompt_en, flags=re.IGNORECASE))
    if begins_as_photo or equipment_formula or (len(categories) >= 2 and not illustration_present):
        return [issue("photographic_dominance", "camera, lens, or photoreal capture formula dominates an illustration prompt without an explicit hybrid-medium request", categories=categories)]
    return []


def _motif_failures(pack: Mapping[str, Any], composed: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    authorial = _mapping(composed.get("authorial_grammar"))
    visual = _mapping(composed.get("visual_evidence"))
    motif_values: list[str] = []
    state_values: list[str] = []
    for section in (authorial, visual):
        for key, value in section.items():
            lowered = str(key).lower()
            values = [value] if isinstance(value, str) else (_string_list(value) or [])
            if "motif_family" in lowered:
                motif_values.extend(values)
            if "motif" in lowered and ("state" in lowered or "placement" in lowered):
                state_values.extend(values)
    unique_motifs = list(dict.fromkeys(motif_values))
    if len(unique_motifs) > 1:
        failures.append(issue("motif_budget", "at most one motif family may be claimed", motif_families=unique_motifs))
    for pattern in DECORATIVE_SOUP_PATTERNS:
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            match = matches[0]
            failures.append(issue("decorative_motif_soup", "decorative motif accumulation is not a causal visual metaphor", excerpt=match.group(0)))

    # A declared list of three or more comma-separated symbols is also a
    # high-confidence soup signal, regardless of whether it uses the word art.
    for match in re.finditer(r"\b(?:motifs?|symbols?|icons?)\s+(?:of|:)\s+([^.!?]{1,140})", prompt_en, flags=re.IGNORECASE):
        items = [part.strip() for part in re.split(r",|\band\b|&", match.group(1), flags=re.IGNORECASE) if part.strip()]
        if len(items) >= 3:
            failures.append(issue("decorative_motif_soup", "prompt stacks three or more motif subjects without a single-family state rule", excerpt=match.group(0), item_count=len(items)))

    route_id = str(_mapping(pack.get("request_contract")).get("route_id") or "")
    if route_id == "recurring_motif_visual_metaphor":
        if len(unique_motifs) != 1:
            failures.append(issue("motif_budget", "recurring-motif route requires exactly one literal motif-family phrase", motif_families=unique_motifs))
        if len(set(state_values)) < 2:
            failures.append(issue("motif_state_change", "recurring-motif route requires two distinct literal states or placements tied to the event", states=state_values))
    return failures


def _format_failures(pack: Mapping[str, Any], composed: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    profile = _mapping(pack.get("format_profile"))
    variant = str(profile.get("variant_id") or "")
    evidence = composed.get("format_evidence")
    if not isinstance(evidence, dict):
        return [issue("format_evidence", "format_evidence must be an object")]
    required = list(FORMAT_REQUIRED_FIELDS.get(variant, ()))
    required.extend(_profile_required_evidence_fields(profile))
    failures.extend(_required_phrase_failures("format_evidence", evidence, required, prompt_en))
    non_ratio_keys = [key for key, value in evidence.items() if key not in ASPECT_ONLY_KEYS and _is_nonempty_string(value)]
    if not non_ratio_keys:
        failures.append(issue("aspect_only_format", "format evidence contains only an aspect ratio or no typed behavior", keys=sorted(evidence)))
    for pattern, label in FORMAT_FORBIDDEN_PATTERNS.get(variant, ()):
        matches = _nonnegated_matches(pattern, prompt_en)
        if matches:
            match = matches[0]
            failures.append(issue("format_substitution", f"{variant} contains forbidden {label}", excerpt=match.group(0)))
    return failures


def _creative_development_failures(pack: Mapping[str, Any], composed: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    contract = _mapping(pack.get("authorial_contract"))
    if contract.get("creative_development_required") is not True:
        return []
    failures: list[dict[str, Any]] = []
    authorial = _mapping(composed.get("authorial_grammar"))
    development = authorial.get("creative_development")
    if not isinstance(development, dict):
        return [issue("creative_development", "high-creativity pack requires authorial_grammar.creative_development")]
    rejected = _string_list(development.get("rejected_ordinary_answers"))
    if not rejected or len(set(rejected)) < 3:
        failures.append(issue("creative_development", "at least three distinct ordinary first answers must be rejected", answers=development.get("rejected_ordinary_answers")))
    proposals = development.get("proposals")
    if not isinstance(proposals, list) or len(proposals) < 4 or any(not isinstance(item, dict) for item in proposals):
        failures.append(issue("creative_development", "at least four structured proposals are required"))
        proposals = []
    proposal_ids: list[str] = []
    operator_ids: list[str] = []
    selected_flags: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for proposal in proposals:
        proposal_id = str(proposal.get("id") or "")
        operator_id = str(proposal.get("operator_id") or "")
        if not proposal_id or proposal_id in by_id:
            failures.append(issue("creative_development", "proposal ids must be nonempty and unique", proposal_id=proposal_id))
        else:
            by_id[proposal_id] = proposal
        proposal_ids.append(proposal_id)
        operator_ids.append(operator_id)
        if proposal.get("selected") is True:
            selected_flags.append(proposal_id)
        for field in ("familiar_anchor_phrase", "changed_rule_phrase", "aboutness", "signature_phrase"):
            if not _is_nonempty_string(proposal.get(field)):
                failures.append(issue("creative_development", "proposal field must be a nonempty scalar", proposal_id=proposal_id, field=field))
        consequences = _string_list(proposal.get("visible_consequence_phrases"))
        if not consequences or len(set(consequences)) < 2:
            failures.append(issue("creative_development", "proposal needs at least two distinct visible consequences", proposal_id=proposal_id))
    if len(set(operator_ids)) < min(4, len(proposals)):
        failures.append(issue("creative_development", "the first four proposals must use distinct operator IDs", operator_ids=operator_ids))
    selected_id = development.get("selected_proposal_id")
    if selected_flags and (len(selected_flags) != 1 or selected_id != selected_flags[0]):
        failures.append(issue("creative_development", "exactly one selected proposal must agree with selected_proposal_id", selected_flags=selected_flags, selected_proposal_id=selected_id))
    if not _is_nonempty_string(selected_id) or selected_id not in by_id:
        failures.append(issue("creative_development", "selected_proposal_id must name exactly one proposal", selected_proposal_id=selected_id))
        return failures
    selected = by_id[str(selected_id)]
    reveal_phrase = selected.get("first_second_reveal_phrase") or selected.get("reveal_phrase")
    if not _is_nonempty_string(reveal_phrase):
        failures.append(issue("creative_development", "selected proposal needs one first-to-second-look reveal phrase", selected_proposal_id=selected_id))
    selected_phrases = [
        selected.get("familiar_anchor_phrase"),
        selected.get("changed_rule_phrase"),
        reveal_phrase,
        selected.get("signature_phrase"),
        *(_string_list(selected.get("visible_consequence_phrases")) or []),
    ]
    for phrase in selected_phrases:
        if _is_nonempty_string(phrase) and phrase not in prompt_en:
            failures.append(issue("creative_development", "selected proposal evidence is not literal in prompt_en", selected_proposal_id=selected_id, phrase=phrase))
    for proposal_id, proposal in by_id.items():
        if proposal_id == selected_id:
            continue
        signature = proposal.get("signature_phrase")
        if _is_nonempty_string(signature) and signature in prompt_en:
            failures.append(issue("creative_development", "unselected proposal signature leaked into prompt_en", proposal_id=proposal_id, signature=signature))
    return failures


def _carrier_risk_failures(
    role: str,
    carrier: Mapping[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    raw_flags = carrier.get("risk_flags")
    flags = _string_list(raw_flags)
    if flags is None:
        failures.append(
            issue(
                "second_look_risk_flags",
                "carrier risk_flags must be a list of nonempty strings",
                role=role,
                actual=raw_flags,
            )
        )
        flags = []
    if len(flags) != len(set(flags)):
        failures.append(
            issue(
                "second_look_risk_flags",
                "carrier risk_flags must be unique",
                role=role,
                actual=flags,
            )
        )
    unknown = sorted(set(flags) - set(SECOND_LOOK_RISK_FLAGS))
    if unknown:
        failures.append(
            issue(
                "second_look_risk_flags",
                "carrier declares a risk flag outside the closed v2 enum",
                role=role,
                unknown=unknown,
                allowed=list(SECOND_LOOK_RISK_FLAGS),
            )
        )

    linked_text = ". ".join(
        str(carrier.get(field) or "")
        for field in ("carrier_phrase", "protected_locus_phrase", "consequence_phrase")
    )
    for risk_flag, patterns in SECOND_LOOK_LINKED_RISK_PATTERNS.items():
        if risk_flag in flags:
            continue
        match = next(
            (
                found
                for pattern in patterns
                if (found := re.search(pattern, linked_text, flags=re.IGNORECASE)) is not None
            ),
            None,
        )
        if match is not None:
            failures.append(
                issue(
                    "second_look_risk_backstop",
                    "linked carrier phrases contain a narrowly recognized risk that was not declared",
                    role=role,
                    risk_flag=risk_flag,
                    excerpt=match.group(0),
                )
            )
    return flags, failures


def _second_look_plan_failures(
    pack: Mapping[str, Any],
    composed: Mapping[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    """Audit the v2 plan contract as pre-render evidence in v2 and v3."""

    version = pack.get("contract_version")
    if version not in (CONTRACT_VERSION_V2, CONTRACT_VERSION_V3):
        return []

    failures: list[dict[str, Any]] = []
    expected_schema = COMPOSED_PROMPT_SCHEMA_V3 if version == CONTRACT_VERSION_V3 else COMPOSED_PROMPT_SCHEMA_V2
    if composed.get("schema") != expected_schema:
        failures.append(
            issue(
                "second_look_plan",
                "candidate pack requires its version-bound composed-prompt schema",
                expected=expected_schema,
                actual=composed.get("schema"),
            )
        )

    plan = composed.get("second_look_plan")
    failures.extend(
        _exact_object_keys(
            plan,
            SECOND_LOOK_PLAN_KEYS,
            check="second_look_plan",
            object_name="second_look_plan",
        )
    )
    if not isinstance(plan, dict):
        return failures
    if plan.get("schema") != SECOND_LOOK_PLAN_SCHEMA:
        failures.append(
            issue(
                "second_look_plan",
                "second_look_plan schema does not match the pack contract",
                expected=SECOND_LOOK_PLAN_SCHEMA,
                actual=plan.get("schema"),
            )
        )

    reveal_phrase = plan.get("reveal_phrase")
    if not _is_nonempty_string(reveal_phrase):
        failures.append(issue("second_look_plan", "reveal_phrase must be a nonempty string"))
    elif reveal_phrase not in prompt_en:
        failures.append(
            issue(
                "literal_evidence",
                "second-look reveal is not an exact literal substring of prompt_en",
                field="second_look_plan.reveal_phrase",
                phrase=reveal_phrase,
            )
        )
    viewer_reveal = _mapping(composed.get("viewer_evidence")).get("second_look_reveal_phrase")
    if reveal_phrase != viewer_reveal:
        failures.append(
            issue(
                "second_look_plan",
                "second-look plan reveal must exactly match viewer_evidence.second_look_reveal_phrase",
                expected=viewer_reveal,
                actual=reveal_phrase,
            )
        )

    review_scales = _string_list(plan.get("review_scale_ids"))
    if not review_scales:
        failures.append(
            issue(
                "second_look_review_scales",
                "review_scale_ids must be a nonempty string list",
                actual=plan.get("review_scale_ids"),
            )
        )
        review_scales = []
    elif len(review_scales) != len(set(review_scales)):
        failures.append(
            issue(
                "second_look_review_scales",
                "review_scale_ids must not contain duplicates",
                actual=review_scales,
            )
        )
    plan_contract = _mapping(_mapping(pack.get("viewer_contract")).get("second_look_plan_contract"))
    allowed_scales = _string_list(plan_contract.get("allowed_review_scale_ids")) or []
    unknown_scales = sorted(set(review_scales) - set(allowed_scales))
    if unknown_scales:
        failures.append(
            issue(
                "second_look_review_scales",
                "review_scale_ids must be a subset of the pack-declared inspection scales",
                unknown=unknown_scales,
                allowed=allowed_scales,
            )
        )

    carriers: dict[str, dict[str, Any]] = {}
    declared_risks: dict[str, list[str]] = {}
    for role in SECOND_LOOK_ROLES:
        carrier = plan.get(role)
        failures.extend(
            _exact_object_keys(
                carrier,
                SECOND_LOOK_CARRIER_KEYS,
                check="second_look_carrier",
                object_name=f"second_look_plan.{role}",
            )
        )
        if not isinstance(carrier, dict):
            continue
        carriers[role] = carrier
        carrier_kind = carrier.get("carrier_kind")
        if carrier_kind not in SECOND_LOOK_CARRIER_KINDS:
            failures.append(
                issue(
                    "second_look_carrier",
                    "carrier_kind is outside the closed v2 enum",
                    role=role,
                    actual=carrier_kind,
                    allowed=list(SECOND_LOOK_CARRIER_KINDS),
                )
            )
        for field in ("carrier_phrase", "protected_locus_phrase", "consequence_phrase"):
            phrase = carrier.get(field)
            if not _is_nonempty_string(phrase):
                failures.append(
                    issue(
                        "second_look_carrier",
                        "carrier phrase field must be a nonempty string",
                        role=role,
                        field=field,
                    )
                )
            elif phrase not in prompt_en:
                failures.append(
                    issue(
                        "literal_evidence",
                        "second-look carrier phrase is not an exact literal substring of prompt_en",
                        field=f"second_look_plan.{role}.{field}",
                        phrase=phrase,
                    )
                )
        flags, risk_failures = _carrier_risk_failures(role, carrier)
        declared_risks[role] = flags
        failures.extend(risk_failures)

    primary = carriers.get("primary_carrier")
    fallback = carriers.get("fallback_carrier")
    if primary is not None and fallback is not None:
        for field in ("carrier_phrase", "protected_locus_phrase", "consequence_phrase"):
            primary_value = _normalized_contract_phrase(primary.get(field))
            fallback_value = _normalized_contract_phrase(fallback.get(field))
            if primary_value and primary_value == fallback_value:
                failures.append(
                    issue(
                        "second_look_distinctness",
                        "primary and fallback carrier evidence must remain distinct after normalization",
                        field=field,
                        primary=primary.get(field),
                        fallback=fallback.get(field),
                    )
                )
        fallback_risks = declared_risks.get("fallback_carrier", [])
        if fallback_risks:
            failures.append(
                issue(
                    "second_look_fallback",
                    "fallback_carrier.risk_flags must be empty",
                    actual=fallback_risks,
                )
            )
        primary_risks = declared_risks.get("primary_carrier", [])
        if primary_risks and primary.get("carrier_kind") == fallback.get("carrier_kind"):
            failures.append(
                issue(
                    "second_look_fallback",
                    "a risky primary carrier requires a safe fallback of a different carrier kind",
                    primary_kind=primary.get("carrier_kind"),
                    fallback_kind=fallback.get("carrier_kind"),
                    primary_risk_flags=primary_risks,
                )
            )

    authorial_contract = _mapping(pack.get("authorial_contract"))
    creative_required = authorial_contract.get("creative_development_required") is True
    selected_id = plan.get("selected_proposal_id")
    primary_consequence = primary.get("consequence_phrase") if primary is not None else None
    fallback_consequence = fallback.get("consequence_phrase") if fallback is not None else None
    if (
        _is_nonempty_string(primary_consequence)
        and _is_nonempty_string(fallback_consequence)
        and _normalized_contract_phrase(primary_consequence)
        == _normalized_contract_phrase(fallback_consequence)
    ):
        # Keep this explicit proposal-level failure in addition to the carrier
        # pair failure: the two planned realizations must implement two actual
        # consequences, not two labels for one consequence.
        failures.append(
            issue(
                "second_look_proposal_binding",
                "primary and fallback must reference two distinct visible consequences",
                primary=primary_consequence,
                fallback=fallback_consequence,
            )
        )

    if not creative_required:
        if selected_id is not None:
            failures.append(
                issue(
                    "second_look_proposal_binding",
                    "selected_proposal_id must be null when creative development is not required",
                    actual=selected_id,
                )
            )
        return failures

    development = _mapping(_mapping(composed.get("authorial_grammar")).get("creative_development"))
    expected_selected_id = development.get("selected_proposal_id")
    if not _is_nonempty_string(selected_id) or selected_id != expected_selected_id:
        failures.append(
            issue(
                "second_look_proposal_binding",
                "second-look plan must name the creative-development selected proposal exactly",
                expected=expected_selected_id,
                actual=selected_id,
            )
        )
    proposals = development.get("proposals")
    selected_proposal = (
        next(
            (
                proposal
                for proposal in proposals
                if isinstance(proposal, dict) and proposal.get("id") == expected_selected_id
            ),
            None,
        )
        if isinstance(proposals, list)
        else None
    )
    if not isinstance(selected_proposal, dict):
        failures.append(
            issue(
                "second_look_proposal_binding",
                "selected proposal is unavailable for exact second-look binding",
                selected_proposal_id=expected_selected_id,
            )
        )
        return failures

    expected_reveal = selected_proposal.get("first_second_reveal_phrase") or selected_proposal.get("reveal_phrase")
    if reveal_phrase != expected_reveal:
        failures.append(
            issue(
                "second_look_proposal_binding",
                "second-look reveal must exactly match the selected proposal reveal",
                expected=expected_reveal,
                actual=reveal_phrase,
            )
        )
    proposal_consequences = _string_list(selected_proposal.get("visible_consequence_phrases")) or []
    for role, consequence in (
        ("primary_carrier", primary_consequence),
        ("fallback_carrier", fallback_consequence),
    ):
        if consequence not in proposal_consequences:
            failures.append(
                issue(
                    "second_look_proposal_binding",
                    "carrier consequence must exactly match a selected-proposal visible consequence",
                    role=role,
                    consequence=consequence,
                    selected_proposal_id=expected_selected_id,
                    allowed=proposal_consequences,
                )
            )
    return failures


def _universal_phrase_records(
    records: Any,
    *,
    id_key: str,
    expected_ids: set[str],
    section: str,
    scene_block: str,
    prompt_en: str,
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    failures: list[dict[str, Any]] = []
    phrases: dict[str, str] = {}
    if not isinstance(records, list):
        return {}, [issue("universal_composition_evidence", f"{section} must be a list")]
    for record in records:
        if not isinstance(record, dict) or set(record) != {id_key, "phrase"}:
            failures.append(
                issue(
                    "universal_composition_evidence",
                    f"every {section} item must have the exact id/phrase field set",
                )
            )
            continue
        record_id = record.get(id_key)
        phrase = record.get("phrase")
        if not _is_nonempty_string(record_id) or not _is_nonempty_string(phrase):
            failures.append(issue("universal_composition_evidence", f"{section} ids and phrases must be nonempty strings"))
            continue
        record_id = str(record_id)
        phrase = str(phrase)
        if record_id in phrases:
            failures.append(issue("universal_composition_evidence", f"{section} ids must be unique", record_id=record_id))
        phrases[record_id] = phrase
        if phrase not in scene_block or phrase not in prompt_en:
            failures.append(
                issue(
                    "universal_composition_evidence",
                    "universal evidence phrases must be literal substrings of both scene_block_phrase and prompt_en",
                    section=section,
                    record_id=record_id,
                    phrase=phrase,
                )
            )
        if any(re.search(pattern, phrase, flags=re.IGNORECASE) for pattern in POST_RENDER_CLAIM_PATTERNS):
            failures.append(
                issue(
                    "universal_pixel_evidence",
                    "pre-render composition evidence cannot claim a rendered-pixel pass",
                    section=section,
                    record_id=record_id,
                )
            )
    actual_ids = set(phrases)
    if actual_ids != expected_ids:
        failures.append(
            issue(
                "universal_composition_evidence",
                f"{section} must exactly cover its selected pack records",
                missing=sorted(expected_ids - actual_ids),
                extra=sorted(actual_ids - expected_ids),
            )
        )
    return phrases, failures


def _universal_carrier_phrase_failures(
    *,
    section: str,
    phrases: Mapping[Any, str],
    carrier_groups: Mapping[Any, list[list[str]]],
) -> list[dict[str, Any]]:
    """Require each linked phrase to carry every authenticated lexeme group."""

    failures: list[dict[str, Any]] = []
    for record_id, groups in carrier_groups.items():
        phrase = phrases.get(record_id)
        if not _is_nonempty_string(phrase):
            continue
        normalized_phrase = _normalized_literal_text(phrase)
        missing_groups = [
            alternatives
            for alternatives in groups
            if not any(
                text_contains_term(normalized_phrase, alternative)
                for alternative in alternatives
            )
        ]
        if missing_groups:
            failures.append(
                issue(
                    "universal_composition_semantics",
                    "linked composition evidence phrase does not express every authenticated semantic carrier group",
                    section=section,
                    record_id=list(record_id) if isinstance(record_id, tuple) else record_id,
                    phrase=phrase,
                    missing_lexeme_groups=missing_groups,
                )
            )
        elif not _carrier_matching_clauses(str(phrase), groups):
            failures.append(
                issue(
                    "universal_composition_semantics",
                    "all authenticated semantic carrier groups must co-occur within one compact clause",
                    section=section,
                    record_id=list(record_id) if isinstance(record_id, tuple) else record_id,
                    phrase=phrase,
                )
            )
    return failures


def _carrier_matching_clauses(
    phrase: str,
    groups: Sequence[Sequence[str]],
) -> list[str]:
    base_clauses = [
        clause.strip()
        for clause in re.split(
            r"[.!?;:]+|[—–]+|\b(?:but|however|yet|although|whereas|while|then|even though)\b",
            _normalized_literal_text(phrase),
        )
        if clause.strip()
    ]

    def matching_spans(clause: str, alternatives: Sequence[str]) -> list[tuple[int, int]]:
        spans: list[tuple[int, int]] = []
        for alternative in alternatives:
            pattern = (
                r"(?<![a-z0-9])" + re.escape(alternative) + r"(?![a-z0-9])"
                if alternative.isascii()
                else re.escape(alternative)
            )
            spans.extend(match.span() for match in re.finditer(pattern, clause))
        return sorted(set(spans))

    windows: list[str] = []
    for clause in base_clauses:
        spans_by_group = [matching_spans(clause, alternatives) for alternatives in groups]
        if not spans_by_group or any(not spans for spans in spans_by_group):
            continue
        pivot_spans = max(spans_by_group, key=len)
        if len(pivot_spans) == 1:
            windows.append(clause)
            continue

        def split_boundary(left: tuple[int, int], right: tuple[int, int]) -> int:
            between = clause[left[1] : right[0]]
            connector = re.search(
                r"[—–;:]|,\s*(?:(?:then|while)\b)?|"
                r"\b(?:and|but|however|yet|although|whereas|while|then|even though)\b",
                between,
            )
            if connector is not None:
                return left[1] + connector.start()
            midpoint = (left[1] + right[0]) // 2
            whitespace_positions = [
                left[1] + match.start()
                for match in re.finditer(r"\s+", between)
            ]
            return min(whitespace_positions, key=lambda value: abs(value - midpoint)) if whitespace_positions else midpoint

        boundaries = [0]
        boundaries.extend(
            split_boundary(left, right)
            for left, right in zip(pivot_spans, pivot_spans[1:])
        )
        boundaries.append(len(clause))
        repeated_windows = [
            clause[start:end].strip(" ,-")
            for start, end in zip(boundaries, boundaries[1:])
            if clause[start:end].strip(" ,-")
        ]
        matching_windows = [
            window
            for window in repeated_windows
            if all(
                any(text_contains_term(window, alternative) for alternative in alternatives)
                for alternatives in groups
            )
        ]
        windows.extend(matching_windows or [clause])
    return windows


def _carrier_anchor_clause(
    phrase: str,
    groups: Sequence[Sequence[str]],
) -> tuple[str, int, int, set[str]] | None:
    normalized = _normalized_literal_text(phrase)
    anchor_spans: list[tuple[int, int]] = []
    matched_anchors: set[str] = set()
    for alternatives in groups:
        matches: list[tuple[int, int, str]] = []
        for alternative in alternatives:
            if not alternative:
                continue
            pattern = (
                r"(?<![a-z0-9])" + re.escape(alternative) + r"(?![a-z0-9])"
                if alternative.isascii()
                else re.escape(alternative)
            )
            match = re.search(pattern, normalized)
            if match is not None:
                matches.append((*match.span(), alternative))
        if not matches:
            return None
        selected = min(matches)
        anchor_spans.append((selected[0], selected[1]))
        matched_anchors.add(selected[2])
    first_anchor = min(start for start, _ in anchor_spans)
    last_anchor = max(end for _, end in anchor_spans)
    clause_start_match = list(re.finditer(r"[.!?;]", normalized[:first_anchor]))
    clause_start = clause_start_match[-1].end() if clause_start_match else 0
    clause_end_match = re.search(r"[.!?;]", normalized[max(end for _, end in anchor_spans) :])
    clause_end = (
        max(end for _, end in anchor_spans) + clause_end_match.start()
        if clause_end_match is not None
        else len(normalized)
    )
    clause = normalized[clause_start:clause_end]
    return (
        clause,
        first_anchor - clause_start,
        last_anchor - clause_start,
        matched_anchors,
    )


def _carrier_negation_scope(
    phrase: str,
    groups: Sequence[Sequence[str]],
) -> tuple[bool, bool]:
    """Return ``(negative, absence_negative)`` for authenticated anchors."""

    scope = _carrier_anchor_clause(phrase, groups)
    if scope is None:
        return False, False
    clause, first_anchor, last_anchor, matched_anchors = scope
    anchor_pattern = "|".join(
        sorted((re.escape(anchor) for anchor in matched_anchors), key=len, reverse=True)
    )
    direct_before_anchor = re.search(
        rf"\b(?:no|not(?!\s+only\b))\s+"
        rf"(?:(?:a|an|the|one|any|all|single|multiple|repeated)\s+)*"
        rf"(?:{anchor_pattern})\b",
        clause,
    )
    if direct_before_anchor is not None and direct_before_anchor.start() <= last_anchor:
        before_direct = clause[: direct_before_anchor.start()]
        after_direct = clause[direct_before_anchor.end() :]
        negates_the_negative = bool(
            re.search(r"\bnot\s*$", before_direct)
            or re.search(
                r"\b(?:it\s+is|it's|that\s+is)\s+not\s+(?:really\s+)?true\s+that"
                r"(?:\s+there\s+(?:is|are))?\s*$",
                before_direct,
            )
        )
        affirmed_exception = bool(
            re.search(
                rf"\bexcept\s+(?:(?:a|an|the|one|any)\s+)?(?:{anchor_pattern})\b",
                after_direct,
            )
        )
        subject_scoped_exception = bool(
            re.match(
                r"\s*,?\s*except\s+(?:(?:on|for|by)\s+)?"
                r"(?:(?:a|an|the|this|that|one|any|each)\s+)?"
                r"(?:actor|character|subject|entity|person|owner|recipient|target|"
                r"participant|adult|child|human|creature|figure|them|him|her)\b",
                after_direct,
            )
        )
        if negates_the_negative or affirmed_exception or subject_scoped_exception:
            return False, False
        return True, True

    semantic_negative_target = (
        rf"(?:{anchor_pattern}|use|used|using|repeat|repeated|show|shown|include|"
        r"included|depict|depicted|connect|connected|occur|occurs|appears?|exist|exists?|"
        r"present|visible|available|provided)"
    )
    auxiliary_not = re.search(
        rf"\b(?:is|are|was|were|do|does|did|can|could|should|would|will|must|"
        rf"may|might|has|have|had)\s+not\s+(?!only\b)(?:\w+\s+){{0,2}}{semantic_negative_target}\b",
        clause,
    )
    if auxiliary_not is not None and auxiliary_not.start() <= last_anchor + 64:
        if re.search(
            r"\bnot\s+(?:omit|exclude|avoid|forbid)(?:s|ted|ting|d|den|ding)?\b",
            auxiliary_not.group(0),
        ):
            auxiliary_not = None
    if auxiliary_not is not None and auxiliary_not.start() <= last_anchor + 64:
        absence_targets = re.search(
            r"\b(?:present|visible|shown|included|depicted|connected|available|provided|"
            r"appear|appears|exist|exists|occur|occurs)\b",
            auxiliary_not.group(0),
        )
        return True, absence_targets is not None

    strong_negative = re.search(
        rf"\b(?:never|without|cannot|can't|lack(?:s|ed|ing)?|avoid(?:s|ed|ing)?|"
        rf"exclud(?:e|es|ed|ing)|omit(?:s|ted|ting)?|forbid(?:s|den|ding)?)\b"
        rf"\s+(?:\w+\s+){{0,2}}{semantic_negative_target}\b",
        clause,
    )
    if strong_negative is not None and strong_negative.start() <= last_anchor:
        affirmed_exception = re.search(
            rf"\bexcept\s+(?:(?:a|an|the|one|any)\s+)?(?:{anchor_pattern})\b",
            strong_negative.group(0),
        )
        negated_exclusion = re.search(
            r"(?:\bnever|\b(?:do|does|did|can|could|should|would|will|must|may|might)\s+not)\s*$",
            clause[: strong_negative.start()],
        )
        double_negative = re.match(
            r"never\s+(?:omit|exclude|avoid|forbid)(?:s|ted|ting|d|den|ding)?\b",
            strong_negative.group(0),
        )
        if (
            affirmed_exception is None
            and negated_exclusion is None
            and double_negative is None
            and first_anchor - 48 <= strong_negative.start() <= last_anchor
        ):
            return True, True

    explicit_negative_state = re.search(
        r"\b(?:(?:is|are|was|were|remains?|remained)\s+"
        r"(?:unused|prevented|prohibited|forbidden)|"
        r"(?:prevent|prohibit|forbid)(?:s|den|ding|ted|ting)?\s+"
        r"(?:the\s+)?(?:use|reuse|sharing))\b",
        clause,
    )
    if explicit_negative_state is not None and (
        first_anchor - 48 <= explicit_negative_state.start() <= last_anchor + 64
    ):
        return True, True

    tail_after_anchor = clause[last_anchor:]
    affirmed_by_negated_absence = re.search(
        r"\b(?:(?:cannot|can't|never|does not|doesn't|did not|didn't|will not|won't|"
        r"must not|should not)\s+(?:fail(?:s|ed|ing)?\s+to\s+(?:appear|exist|occur|show)|"
        r"disappear|vanish)(?:s|ed|ing)?|"
        r"(?:is|are|was|were)\s+not\s+(?:absent|missing|omitted|excluded|unavailable))\b",
        tail_after_anchor,
    )
    if affirmed_by_negated_absence is not None and affirmed_by_negated_absence.start() <= 64:
        return False, False

    absent_after_anchor = re.search(
        r"\b(?:(?:is|are|was|were|remain|remains|remained)\s+"
        r"(?:(?:fully|entirely|completely|visually)\s+)?"
        r"(?:absent|missing|omitted|excluded|unavailable|disconnected|forbidden|unused|prevented|"
        r"prohibited|hidden|concealed|obscured|invisible|unseen|occluded|cropped\s+out|off[- ]screen|"
        r"outside\s+(?:the\s+)?composition|out\s+of\s+(?:frame|view)|nowhere\s+visible)|"
        r"fail(?:s|ed|ing)?\s+to\s+(?:appear|exist|occur|show)|"
        r"(?:disappear|vanish)(?:s|ed|ing)?)\b",
        tail_after_anchor,
    )
    if absent_after_anchor is not None and absent_after_anchor.start() <= 64:
        return True, True
    return False, False


def _forbidden_carrier_has_scoped_negation(
    phrase: str,
    groups: Sequence[Sequence[str]],
) -> bool:
    return _carrier_negation_scope(phrase, groups)[0]


def _universal_forbidden_carrier_failures(
    *,
    identity_phrases: Mapping[str, str],
    identity_groups: Mapping[Any, list[list[str]]],
    identity_polarity: Mapping[str, str],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for fact_id, polarity in identity_polarity.items():
        if polarity != "forbidden":
            continue
        phrase = identity_phrases.get(fact_id)
        groups = identity_groups.get(fact_id, [])
        matching_clauses = (
            _carrier_matching_clauses(str(phrase), groups)
            if _is_nonempty_string(phrase) and groups
            else []
        )
        if matching_clauses and any(
            not _forbidden_carrier_has_scoped_negation(clause, groups)
            for clause in matching_clauses
        ):
            failures.append(
                issue(
                    "universal_composition_semantics",
                    "forbidden identity evidence must explicitly negate the authenticated fact within the same clause",
                    section="identity_core",
                    record_id=fact_id,
                    phrase=phrase,
                    polarity=polarity,
                )
            )
    return failures


def _universal_asserted_carrier_failures(
    *,
    phrase_sections: Mapping[str, Mapping[Any, str]],
    carrier_maps: Mapping[str, Mapping[Any, list[list[str]]]],
    identity_polarity: Mapping[str, str],
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for section, phrases in phrase_sections.items():
        groups_by_id = carrier_maps.get(section, {})
        for record_id, phrase in phrases.items():
            groups = groups_by_id.get(record_id, [])
            matching_clauses = _carrier_matching_clauses(phrase, groups) if groups else []
            scopes = [
                _carrier_negation_scope(clause, groups)
                for clause in matching_clauses
            ]
            if section == "identity_core":
                polarity = identity_polarity.get(str(record_id))
                if polarity == "forbidden":
                    continue
                if polarity == "asserted_absence":
                    if groups and matching_clauses and any(
                        not absence_negative
                        for _, absence_negative in scopes
                    ):
                        failures.append(
                            issue(
                                "universal_composition_semantics",
                                "asserted-absence identity evidence must explicitly express the authenticated absence within the same clause",
                                section=section,
                                record_id=record_id,
                                phrase=phrase,
                                polarity=polarity,
                            )
                        )
                    continue
                if polarity != "asserted_presence":
                    continue
            negates_realization = any(
                absence_negative
                or (section in {"atoms", "bridges", "resources"} and negative)
                for negative, absence_negative in scopes
            )
            if negates_realization:
                failures.append(
                    issue(
                        "universal_composition_semantics",
                        "asserted composition evidence must not negate the presence or realization of its authenticated semantic anchors",
                        section=section,
                        record_id=list(record_id) if isinstance(record_id, tuple) else record_id,
                        phrase=phrase,
                        polarity="asserted",
                    )
                )
            if groups and _carrier_is_substitution_or_representation_only(phrase, groups):
                failures.append(
                    issue(
                        "universal_composition_semantics",
                        "composition evidence must depict its authenticated value or realization, not only a replacement, label, diagram, or representation",
                        section=section,
                        record_id=list(record_id) if isinstance(record_id, tuple) else record_id,
                        phrase=phrase,
                        polarity="asserted",
                    )
                )
    return failures


def _carrier_is_substitution_or_representation_only(
    phrase: str,
    groups: Sequence[Sequence[str]],
) -> bool:
    """Reject high-confidence mention-only wording for semantic realizations."""

    anchors = {
        _normalized_literal_text(alternative)
        for alternatives in groups
        for alternative in alternatives
        if _is_nonempty_string(alternative)
    }
    if not anchors:
        return False
    anchor_pattern = "|".join(
        sorted((re.escape(anchor) for anchor in anchors), key=len, reverse=True)
    )
    normalized = _normalized_literal_text(phrase)
    replacement = re.search(
        rf"\b(?:replace(?:s|d|ment)?|replac(?:ed|ing)|substitut(?:e|es|ed|ing))\s+"
        rf"(?:(?:a|an|the|one)\s+)?(?:{anchor_pattern})\b(?!['’]s\b)|"
        rf"\b(?:{anchor_pattern})\b[^.!?;:]{{0,20}}\b(?:is|are|was|were)\s+replaced\s+by\b|"
        r"\b(?:takes?\s+the\s+place\s+of|stands?\s+in\s+for|appears?\s+instead\s+of)\s+"
        rf"(?:(?:a|an|the|one)\s+)?(?:{anchor_pattern})\b|"
        rf"\binstead\s+of\s+(?:(?:a|an|the|one)\s+)?(?:{anchor_pattern})\b|"
        rf"\b\w+(?:\s+\w+){{0,3}}\s+(?:doubles?\s+as|serves?\s+as|portrays?|"
        rf"represents?|stands?\s+for)\s+(?:(?:a|an|the|one)\s+)?(?:{anchor_pattern})\b",
        normalized,
    )
    if replacement is not None:
        return True
    representation_pattern = (
        rf"\b(?:{anchor_pattern})(?:[- ](?:shaped|like))\s+"
        r"(?:shadow|silhouette|outline|pattern|motif|symbol|drawing|image|print|reflection|"
        r"sculpture|model|hologram|cutout|sticker)\b|"
        rf"\b(?:{anchor_pattern})\b[^.!?;:]{{0,32}}\bappears?\s+only\s+as\s+"
        r"(?:(?:a|an|the)\s+)?(?:mural|drawing|caption|word|sign|print|image|reflection|"
        r"sculpture|model|hologram|cutout|sticker)\b|"
        r"\b(?:painted|printed|drawn|written)\s+(?:depiction|image|drawing|symbol|word|sign)\s+of\s+"
        rf"(?:(?:a|an|the)\s+)?(?:{anchor_pattern})\b|"
        r"\b(?:(?:a|an|the)\s+)?(?:drawing|mural|image|photograph|photo|picture|reflection|"
        r"shadow|silhouette|outline|sign|caption|print|depiction|sculpture|model|hologram|"
        r"cutout|sticker|diagram)\s+of\s+"
        rf"(?:(?:a|an|the)\s+)?(?:(?:actual|physical|visible)\s+)?(?:{anchor_pattern})\b|"
        rf"\b(?:{anchor_pattern})\b[^.!?;:]{{0,24}}\b(?:exists?|appears?)\s+only\s+as\s+"
        r"(?:(?:a|an|the)\s+)?(?:shadow|silhouette|outline|drawing|mural|image|photograph|"
        r"photo|picture|reflection|sign|caption|print|depiction|sculpture|model|hologram|"
        r"cutout|sticker|diagram)\b|"
        rf"\b(?:{anchor_pattern})\b[^.!?;:]{{0,24}}\b(?:is|are|was|were)\s+"
        r"(?:represented|suggested|depicted|written|printed|painted)\s+(?:by|on|as)\s+"
        r"(?:(?:a|an|the|its)\s+)?(?:shadow|silhouette|outline|drawing|mural|image|photograph|"
        r"photo|picture|reflection|label|sign|caption|print|depiction|sculpture|model|hologram|"
        r"cutout|sticker|diagram)\b|"
        rf"\b(?:the\s+)?(?:word|caption|label|diagram|sign)\b[^.!?;:]{{0,28}}\b"
        rf"(?:says?|reads?|labels?|shows?)?\s*(?:{anchor_pattern})\b"
    )
    representation_matches = list(re.finditer(representation_pattern, normalized))
    if not representation_matches:
        return False
    distinct_explicit_instance = next(
        (
            match
            for match in re.finditer(
                rf"\b(?:actual|physical)\s+(?:{anchor_pattern})\b",
                normalized,
            )
            if all(
                match.end() <= representation.start()
                or match.start() >= representation.end()
                for representation in representation_matches
            )
        ),
        None,
    )
    if distinct_explicit_instance is not None:
        return False
    positive_pattern = (
        rf"\b(?:actual|physical|visible)\s+(?:{anchor_pattern})\b[^.!?;:]{{0,36}}\b"
        r"(?:is|are|was|were)?\s*(?:held|carried|used|present|visible|resting|lying|standing|"
        r"occurring|performed|realized)\b|"
        rf"\b(?:{anchor_pattern})\b[^.!?;:]{{0,36}}\b"
        r"(?:is|are|was|were)?\s*(?:held|carried|used|resting|lying|standing|occurs?|"
        r"takes?\s+place|is\s+performed|is\s+(?:physically\s+)?realized)\b|"
        rf"\b(?:{anchor_pattern})\s+itself\b[^.!?;:]{{0,24}}\b(?:present|visible)\b"
    )
    representation_prefix = re.compile(
        r"(?:drawing|mural|image|photograph|photo|picture|reflection|shadow|silhouette|"
        r"outline|sign|caption|print|depiction|sculpture|model|hologram|cutout|sticker|"
        r"diagram)\s+of\s+(?:(?:a|an|the)\s+)?"
        r"(?:(?:actual|physical|visible)\s+)?$"
    )
    positive_realization = next(
        (
            match
            for match in re.finditer(positive_pattern, normalized)
            if representation_prefix.search(normalized[max(0, match.start() - 80) : match.start()]) is None
            and all(
                match.end() <= representation.start()
                or match.start() >= representation.end()
                for representation in representation_matches
            )
        ),
        None,
    )
    return positive_realization is None


def _universal_phrase_reuse_failures(
    phrase_sections: Mapping[str, Mapping[Any, str]],
    *,
    maximum_links: int = 8,
) -> list[dict[str, Any]]:
    links_by_phrase: dict[str, list[dict[str, Any]]] = {}
    for section, phrases in phrase_sections.items():
        for record_id, phrase in phrases.items():
            normalized = _normalized_literal_text(phrase)
            if not normalized:
                continue
            links_by_phrase.setdefault(normalized, []).append(
                {
                    "section": section,
                    "record_id": list(record_id) if isinstance(record_id, tuple) else record_id,
                }
            )
    return [
        issue(
            "universal_composition_semantics",
            "one exact evidence phrase is linked to too many distinct semantic records",
            phrase=phrase,
            linked_record_count=len(links),
            maximum_linked_records=maximum_links,
            links=links,
        )
        for phrase, links in links_by_phrase.items()
        if len(links) > maximum_links
    ]


def audit_universal_scene_evidence(
    pack: Mapping[str, Any],
    composed: Mapping[str, Any],
    prompt_en: str,
) -> list[dict[str, Any]]:
    """Audit additive v3 literal evidence; prompt prose alone is never proof."""

    if pack.get("contract_version") != CONTRACT_VERSION_V3:
        return []

    failures: list[dict[str, Any]] = []
    if composed.get("schema") != COMPOSED_PROMPT_SCHEMA_V3:
        failures.append(
            issue(
                "universal_composition_evidence",
                "v3 candidate pack requires the v3 composed-prompt schema",
                expected=COMPOSED_PROMPT_SCHEMA_V3,
                actual=composed.get("schema"),
            )
        )
    evidence = composed.get("universal_scene_evidence")
    failures.extend(
        _exact_object_keys(
            evidence,
            UNIVERSAL_EVIDENCE_KEYS,
            check="universal_composition_evidence",
            object_name="universal_scene_evidence",
        )
    )
    if not isinstance(evidence, dict):
        return failures
    if evidence.get("schema") != UNIVERSAL_SCENE_EVIDENCE_SCHEMA:
        failures.append(
            issue(
                "universal_composition_evidence",
                "universal_scene_evidence schema is outside the closed contract",
                expected=UNIVERSAL_SCENE_EVIDENCE_SCHEMA,
                actual=evidence.get("schema"),
            )
        )
    scene_block = evidence.get("scene_block_phrase")
    if not _is_nonempty_string(scene_block):
        failures.append(issue("universal_composition_evidence", "scene_block_phrase must be a nonempty string"))
        scene_block = ""
    else:
        scene_block = str(scene_block)
        if scene_block not in prompt_en:
            failures.append(issue("universal_composition_evidence", "scene_block_phrase must be one contiguous literal prompt_en substring"))
        lexical_unit_count = _universal_lexical_unit_count(scene_block)
        if lexical_unit_count > 150:
            failures.append(
                issue(
                    "universal_scene_word_budget",
                    "scene_block_phrase exceeds the hard 150 lexical-unit budget",
                    lexical_unit_count=lexical_unit_count,
                )
            )
        sentence_count = len(
            [
                part
                for part in re.split(r"(?:[.!?。！？]+|\r?\n+)", scene_block.strip())
                if part.strip()
            ]
        )
        if sentence_count > 8:
            failures.append(issue("universal_scene_word_budget", "scene_block_phrase exceeds the hard eight-sentence budget", sentence_count=sentence_count))
        if any(re.search(pattern, scene_block, flags=re.IGNORECASE) for pattern in POST_RENDER_CLAIM_PATTERNS):
            failures.append(issue("universal_pixel_evidence", "scene block cannot claim post-render pixel review or success"))
    for pattern, reason in UNIVERSAL_UNSUPPORTED_INFERENCE_PATTERNS:
        rejected_excerpt: str | None = None
        for candidate in re.finditer(pattern, prompt_en, flags=re.IGNORECASE):
            prefix = prompt_en[: candidate.start()]
            previous_boundaries = [match.end() for match in re.finditer(r"[.!?;:]", prefix)]
            clause_start = previous_boundaries[-1] if previous_boundaries else 0
            suffix_boundary = re.search(r"[.!?;:]", prompt_en[candidate.end() :])
            clause_end = (
                candidate.end() + suffix_boundary.start()
                if suffix_boundary is not None
                else len(prompt_en)
            )
            candidate_excerpt = prompt_en[clause_start:clause_end].strip()
            if not _unsupported_inference_is_explicitly_negated(candidate_excerpt):
                rejected_excerpt = candidate_excerpt
                break
        if rejected_excerpt is not None:
            failures.append(
                issue(
                    "universal_unsupported_inference",
                    reason,
                    excerpt=rejected_excerpt,
                )
            )

    scene = _mapping(pack.get("universal_scene"))
    carrier_maps, identity_polarity, _ = _universal_composition_carrier_contract(scene)
    identity = _mapping(scene.get("identity_core"))
    identity_ids: set[str] = set()
    entities = identity.get("entities") if isinstance(identity.get("entities"), list) else []
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        for fact in entity.get("feature_facts") or []:
            if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                identity_ids.add(str(fact["id"]))
    for collection_name in ("scene_facts", "forbidden_facts"):
        for fact in identity.get(collection_name) or []:
            if isinstance(fact, dict) and _is_nonempty_string(fact.get("id")):
                identity_ids.add(str(fact["id"]))

    selected_event = _mapping(scene.get("selected_event"))
    roles = selected_event.get("roles") if isinstance(selected_event.get("roles"), list) else []
    event_role_ids = {
        str(role["role_id"])
        for role in roles
        if isinstance(role, dict)
        and _is_nonempty_string(role.get("role_id"))
        and _is_nonempty_string(role.get("value_id"))
    }
    atoms = scene.get("atoms") if isinstance(scene.get("atoms"), list) else []
    atom_ids = {
        str(atom["instance_id"])
        for atom in atoms
        if isinstance(atom, dict) and _is_nonempty_string(atom.get("instance_id"))
    }
    bridges = scene.get("bridges") if isinstance(scene.get("bridges"), list) else []
    bridge_ids = {
        str(bridge["bridge_id"])
        for bridge in bridges
        if isinstance(bridge, dict) and _is_nonempty_string(bridge.get("bridge_id"))
    }
    resources = scene.get("resource_claims") if isinstance(scene.get("resource_claims"), list) else []
    resource_ids = {
        str(claim["claim_id"])
        for claim in resources
        if isinstance(claim, dict)
        and claim.get("evidence_required") is True
        and _is_nonempty_string(claim.get("claim_id"))
    }

    identity_phrases, record_failures = _universal_phrase_records(
        evidence.get("identity_core_phrases"),
        id_key="fact_id",
        expected_ids=identity_ids,
        section="identity_core_phrases",
        scene_block=scene_block,
        prompt_en=prompt_en,
    )
    failures.extend(record_failures)
    fixed_slot_pairs = {
        (str(slot.get("slot_id")), str(value_id))
        for slot in (scene.get("slot_states") if isinstance(scene.get("slot_states"), list) else [])
        if isinstance(slot, dict) and slot.get("state") == "fixed"
        for value_id in (_string_list(slot.get("value_ids")) or [])
    }
    fixed_slot_records = evidence.get("fixed_slot_phrases")
    actual_fixed_slot_pairs: set[tuple[str, str]] = set()
    fixed_slot_phrases: dict[tuple[str, str], str] = {}
    if not isinstance(fixed_slot_records, list):
        failures.append(issue("universal_composition_evidence", "fixed_slot_phrases must be a list"))
    else:
        for record in fixed_slot_records:
            if not isinstance(record, dict) or set(record) != {"slot_id", "value_id", "phrase"}:
                failures.append(issue("universal_composition_evidence", "every fixed_slot_phrases item must have exact slot_id/value_id/phrase fields"))
                continue
            slot_id = record.get("slot_id")
            value_id = record.get("value_id")
            phrase = record.get("phrase")
            if not all(_is_nonempty_string(value) for value in (slot_id, value_id, phrase)):
                failures.append(issue("universal_composition_evidence", "fixed slot ids, values, and phrases must be nonempty strings"))
                continue
            pair = (str(slot_id), str(value_id))
            if pair in actual_fixed_slot_pairs:
                failures.append(issue("universal_composition_evidence", "fixed slot evidence pairs must be unique", slot_id=slot_id, value_id=value_id))
            actual_fixed_slot_pairs.add(pair)
            fixed_slot_phrases[pair] = str(phrase)
            if str(phrase) not in scene_block or str(phrase) not in prompt_en:
                failures.append(
                    issue(
                        "universal_composition_evidence",
                        "fixed slot phrase must be a literal substring of both scene block and prompt",
                        slot_id=slot_id,
                        value_id=value_id,
                        phrase=phrase,
                    )
                )
    if actual_fixed_slot_pairs != fixed_slot_pairs:
        failures.append(
            issue(
                "universal_composition_evidence",
                "fixed_slot_phrases must exactly cover every fixed slot value",
                missing=[list(pair) for pair in sorted(fixed_slot_pairs - actual_fixed_slot_pairs)],
                extra=[list(pair) for pair in sorted(actual_fixed_slot_pairs - fixed_slot_pairs)],
            )
        )
    event_phrases, record_failures = _universal_phrase_records(
        evidence.get("event_role_phrases"),
        id_key="role_id",
        expected_ids=event_role_ids,
        section="event_role_phrases",
        scene_block=scene_block,
        prompt_en=prompt_en,
    )
    failures.extend(record_failures)
    atom_phrases, record_failures = _universal_phrase_records(
        evidence.get("atom_phrases"),
        id_key="instance_id",
        expected_ids=atom_ids,
        section="atom_phrases",
        scene_block=scene_block,
        prompt_en=prompt_en,
    )
    failures.extend(record_failures)
    bridge_phrases, record_failures = _universal_phrase_records(
        evidence.get("bridge_phrases"),
        id_key="bridge_id",
        expected_ids=bridge_ids,
        section="bridge_phrases",
        scene_block=scene_block,
        prompt_en=prompt_en,
    )
    failures.extend(record_failures)
    resource_phrases, record_failures = _universal_phrase_records(
        evidence.get("resource_phrases"),
        id_key="claim_id",
        expected_ids=resource_ids,
        section="resource_phrases",
        scene_block=scene_block,
        prompt_en=prompt_en,
    )
    failures.extend(record_failures)
    for section, phrases in (
        ("identity_core", identity_phrases),
        ("fixed_slots", fixed_slot_phrases),
        ("event_roles", event_phrases),
        ("atoms", atom_phrases),
        ("bridges", bridge_phrases),
        ("resources", resource_phrases),
    ):
        failures.extend(
            _universal_carrier_phrase_failures(
                section=section,
                phrases=phrases,
                carrier_groups=carrier_maps.get(section, {}),
            )
        )
    failures.extend(
        _universal_forbidden_carrier_failures(
            identity_phrases=identity_phrases,
            identity_groups=carrier_maps.get("identity_core", {}),
            identity_polarity=identity_polarity,
        )
    )
    phrase_sections: dict[str, Mapping[Any, str]] = {
        "identity_core": identity_phrases,
        "fixed_slots": fixed_slot_phrases,
        "event_roles": event_phrases,
        "atoms": atom_phrases,
        "bridges": bridge_phrases,
        "resources": resource_phrases,
    }
    failures.extend(
        _universal_asserted_carrier_failures(
            phrase_sections=phrase_sections,
            carrier_maps=carrier_maps,
            identity_polarity=identity_polarity,
        )
    )
    failures.extend(_universal_phrase_reuse_failures(phrase_sections))

    salience = evidence.get("salience_phrases")
    failures.extend(
        _exact_object_keys(
            salience,
            UNIVERSAL_SALIENCE_KEYS,
            check="universal_salience_budget",
            object_name="universal_scene_evidence.salience_phrases",
        )
    )
    if isinstance(salience, dict):
        for field in ("primary_core_event_phrase", "controlled_rest_phrase"):
            phrase = salience.get(field)
            if not _is_nonempty_string(phrase) or str(phrase) not in scene_block or str(phrase) not in prompt_en:
                failures.append(issue("universal_salience_budget", "required salience phrase must be literal scene-block evidence", field=field, phrase=phrase))
        for field in ("secondary_discovery_phrase", "remote_carrier_phrase"):
            phrase = salience.get(field)
            if phrase is not None and (not _is_nonempty_string(phrase) or str(phrase) not in scene_block or str(phrase) not in prompt_en):
                failures.append(issue("universal_salience_budget", "optional salience phrase must be null or literal scene-block evidence", field=field, phrase=phrase))
        distance_trace = _mapping(scene.get("semantic_distance_trace"))
        fixed_remote_count = distance_trace.get("fixed_remote_count")
        optional_remote_count = distance_trace.get("optional_remote_count")
        has_remote_premise = (
            isinstance(fixed_remote_count, int)
            and not isinstance(fixed_remote_count, bool)
            and isinstance(optional_remote_count, int)
            and not isinstance(optional_remote_count, bool)
            and fixed_remote_count + optional_remote_count > 0
        )
        if has_remote_premise and not _is_nonempty_string(salience.get("remote_carrier_phrase")):
            failures.append(issue("universal_salience_budget", "fixed or optional remote premise requires one literal remote carrier phrase"))
        if not has_remote_premise and salience.get("remote_carrier_phrase") is not None:
            failures.append(issue("universal_salience_budget", "remote carrier phrase must be null when no remote premise was selected"))

    pixel = _mapping(scene.get("pixel_evidence_contract"))
    result_role = next(
        (role for role in roles if isinstance(role, dict) and role.get("role_id") == "result"),
        {},
    )
    consequence_required = (
        _is_nonempty_string(result_role.get("value_id"))
        or bool(pixel.get("consequence_item_ids"))
        or any(isinstance(atom, dict) and atom.get("facet") == "consequence" for atom in atoms)
    )
    consequence_phrase = evidence.get("consequence_phrase")
    if consequence_required:
        if not _is_nonempty_string(consequence_phrase) or str(consequence_phrase) not in scene_block or str(consequence_phrase) not in prompt_en:
            failures.append(issue("universal_composition_evidence", "a claimed result requires literal scene-block consequence evidence", phrase=consequence_phrase))
    elif consequence_phrase is not None:
        failures.append(issue("universal_composition_evidence", "consequence_phrase must be null when the event claims no result", phrase=consequence_phrase))

    items = pixel.get("items") if isinstance(pixel.get("items"), list) else []
    for item in items:
        if not isinstance(item, dict):
            continue
        source_kind = item.get("source_kind")
        source_id = str(item.get("source_id") or "")
        if source_kind == "atom" and source_id not in atom_phrases:
            failures.append(issue("universal_pixel_evidence", "atom pixel obligation lacks exact atom phrase evidence", item_id=item.get("item_id"), source_id=source_id))
        elif source_kind == "bridge" and source_id not in bridge_phrases:
            failures.append(issue("universal_pixel_evidence", "bridge pixel obligation lacks exact bridge phrase evidence", item_id=item.get("item_id"), source_id=source_id))
        elif source_kind == "core_anchor" and not identity_phrases:
            failures.append(issue("universal_pixel_evidence", "core-anchor pixel obligation lacks identity phrase evidence", item_id=item.get("item_id")))
        elif source_kind == "event" and not event_phrases:
            failures.append(issue("universal_pixel_evidence", "event pixel obligation lacks event-role phrase evidence", item_id=item.get("item_id")))
        elif source_kind == "consequence" and not _is_nonempty_string(consequence_phrase):
            failures.append(issue("universal_pixel_evidence", "consequence pixel obligation lacks literal consequence evidence", item_id=item.get("item_id")))

    # Exact resource records are necessary even when a resource phrase shares
    # a sentence with an atom; prose alone cannot assert capacity eligibility.
    for claim_id in resource_ids:
        if claim_id not in resource_phrases:
            failures.append(issue("universal_resource_capacity", "evidence-required resource claim lacks a typed literal binding", claim_id=claim_id))
    return failures


def _prompt_word_warning(pack: Mapping[str, Any], prompt_en: str) -> list[dict[str, Any]]:
    profile = _mapping(pack.get("format_profile"))
    raw_range = profile.get("prompt_word_range")
    minimum: int | None = None
    maximum: int | None = None
    if isinstance(raw_range, list) and len(raw_range) == 2 and all(isinstance(item, int) and not isinstance(item, bool) for item in raw_range):
        minimum, maximum = raw_range
    elif isinstance(raw_range, dict):
        raw_min, raw_max = raw_range.get("minimum"), raw_range.get("maximum")
        if isinstance(raw_min, int) and not isinstance(raw_min, bool) and isinstance(raw_max, int) and not isinstance(raw_max, bool):
            minimum, maximum = raw_min, raw_max
    if minimum is None or maximum is None or minimum > maximum:
        return []
    count = len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", prompt_en))
    if not minimum <= count <= maximum:
        return [issue("prompt_word_range", "prompt word count is outside the format recommendation; this is advisory", word_count=count, minimum=minimum, maximum=maximum)]
    return []


def audit_composed_prompt(pack: dict[str, Any], composed: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic JSON-serializable audit result."""

    integrity_errors = validate_pack_integrity(pack)
    failures: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    required_fields = (
        "pack_id",
        "prompt_en",
        "negative_en",
        "chosen_candidate_ids",
        "composer",
        "visual_evidence",
        "authorial_grammar",
        "viewer_evidence",
        "format_evidence",
        "reference_boundary",
    )
    missing = [field for field in required_fields if field not in composed]
    if pack.get("contract_version") == CONTRACT_VERSION_V3:
        missing.extend(field for field in ("schema", "universal_scene_evidence") if field not in composed)
    if missing:
        failures.append(issue("output_contract", "composed object is missing required fields", fields=missing))

    prompt_en = composed.get("prompt_en")
    if not _is_nonempty_string(prompt_en):
        failures.append(issue("output_contract", "prompt_en must be a nonempty string"))
        prompt_en = ""
    else:
        prompt_en = str(prompt_en)
    if composed.get("composer") != "agent":
        failures.append(issue("output_contract", "composer must equal agent", actual=composed.get("composer")))
    if composed.get("pack_id") != pack.get("pack_id"):
        failures.append(issue("pack_id", "composed pack_id does not exactly match candidate pack", expected=pack.get("pack_id"), actual=composed.get("pack_id")))
    if composed.get("negative_en") != pack.get("negative_en"):
        failures.append(issue("negative_en", "negative_en is not byte-for-byte identical to candidate pack"))

    chosen_ids, chosen_failures = _strict_chosen_ids(composed.get("chosen_candidate_ids"))
    failures.extend(chosen_failures)
    expected_ids = expected_chosen_candidate_ids(pack)
    if set(chosen_ids) != set(expected_ids) or len(chosen_ids) != len(expected_ids):
        failures.append(issue("chosen_candidate_ids", "chosen_candidate_ids must be the exact route, format, and exposed visual-node set", expected=expected_ids, actual=chosen_ids, missing=sorted(set(expected_ids) - set(chosen_ids)), extra=sorted(set(chosen_ids) - set(expected_ids))))
    allowed_visual_ids = {candidate_id for candidate_id in expected_ids if candidate_id.startswith("visual:")}
    nonvisual_candidates = sorted(candidate_id for candidate_id in chosen_ids if candidate_id.startswith("visual:") and candidate_id not in allowed_visual_ids)
    if nonvisual_candidates:
        failures.append(issue("typed_candidate_boundary", "unexposed, router, guard, or other nonvisual candidate selected as visual proof", ids=nonvisual_candidates))

    visual_evidence = _mapping(composed.get("visual_evidence"))
    authorial = _mapping(composed.get("authorial_grammar"))
    viewer = _mapping(composed.get("viewer_evidence"))
    format_evidence = _mapping(composed.get("format_evidence"))
    failures.extend(audit_literal_evidence(prompt_en, "visual_evidence", composed.get("visual_evidence")))
    failures.extend(audit_literal_evidence(prompt_en, "authorial_grammar", composed.get("authorial_grammar"), skipped_roots=("creative_development",)))
    failures.extend(audit_literal_evidence(prompt_en, "viewer_evidence", composed.get("viewer_evidence")))
    failures.extend(audit_literal_evidence(prompt_en, "format_evidence", composed.get("format_evidence")))

    grammar = _mapping(pack.get("visual_grammar"))
    required_visual = _string_list(grammar.get("required_evidence_types")) or []
    failures.extend(_required_phrase_failures("visual_evidence", visual_evidence, required_visual, prompt_en))

    authorial_contract = _mapping(pack.get("authorial_contract"))
    authorial_fields = list(AUTHORIAL_REQUIRED_FIELDS)
    authorial_fields.extend(_string_list(authorial_contract.get("required_fields")) or [])
    failures.extend(_required_phrase_failures("authorial_grammar", authorial, authorial_fields, prompt_en))
    failures.extend(_authorial_concreteness_failures(authorial))

    viewer_contract = _mapping(pack.get("viewer_contract"))
    viewer_fields = list(VIEWER_REQUIRED_FIELDS)
    viewer_fields.extend(_string_list(viewer_contract.get("required_fields")) or [])
    if viewer_contract.get("reinspection_reward_required") is True:
        viewer_fields.append("reinspection_reward_phrase")
    failures.extend(_required_phrase_failures("viewer_evidence", viewer, viewer_fields, prompt_en))

    first = viewer.get("first_glance_hook_phrase")
    second = viewer.get("second_look_reveal_phrase")
    if _is_nonempty_string(first) and _is_nonempty_string(second):
        if first == second:
            failures.append(issue("first_second_look", "first-glance hook and second-look reveal must be different phrases"))
        elif prompt_en.find(str(first)) >= prompt_en.find(str(second)):
            failures.append(issue("first_second_look", "first-glance phrase must precede second-look phrase in prompt_en", first=first, second=second))
    causal_fields = ["affect_actor_phrase", "affect_action_phrase", "affect_target_phrase", "affect_consequence_phrase"]
    causal_values = [viewer.get(field) for field in causal_fields if _is_nonempty_string(viewer.get(field))]
    if len(causal_values) == len(causal_fields) and len(set(causal_values)) != len(causal_values):
        failures.append(issue("causal_viewer_evidence", "actor, directed action, target, and consequence must be distinct visible phrases", phrases=causal_values))

    failures.extend(_mandatory_intent_failures(pack, composed, prompt_en))
    failures.extend(_format_failures(pack, composed, prompt_en))
    failures.extend(_reference_boundary_failures(composed, prompt_en, pack))
    failures.extend(_policy_language_failures(prompt_en))
    failures.extend(_phase_boundary_failures(pack, composed, prompt_en))
    failures.extend(_photo_dominance_failures(pack, prompt_en))
    failures.extend(_motif_failures(pack, composed, prompt_en))
    failures.extend(_creative_development_failures(pack, composed, prompt_en))
    failures.extend(_second_look_plan_failures(pack, composed, prompt_en))
    failures.extend(audit_universal_scene_evidence(pack, composed, prompt_en))
    warnings.extend(_prompt_word_warning(pack, prompt_en))

    status = "error" if integrity_errors else ("fail" if failures else "pass")
    limits = [
        "A prompt audit cannot prove rendered pixel salience, historical originality, audience response, sales, or legal clearance.",
        "Named-style and protected-IP text detection is a narrow backstop; reference_boundary and platform policy remain authoritative.",
    ]
    if pack.get("contract_version") == CONTRACT_VERSION_V3:
        limits.append(
            "The v3 audit recomputes the embedded scene-contract hash and deterministically replays selection against local hash-bound assets; rendered pixels still require separate post-render review."
        )
    return {
        "status": status,
        "quality_status": "warn" if warnings else "pass",
        "pack_id": pack.get("pack_id"),
        "chosen_candidate_count": len(chosen_ids),
        "integrity_errors": integrity_errors,
        "failures": failures,
        "warnings": warnings,
        "limits": limits,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit one agent-composed illustration prompt against one compact candidate pack.")
    parser.add_argument("--pack", required=True, help="Candidate-pack JSON path or inline JSON.")
    parser.add_argument("--composed", required=True, help="Composed-prompt JSON path or inline JSON.")
    parser.add_argument("--output-file", help="Optional UTF-8 path for the same JSON result printed to stdout.")
    return parser.parse_args(argv)


def _transport_error_result(exc: Exception) -> dict[str, Any]:
    return {
        "status": "error",
        "quality_status": "not_run",
        "pack_id": None,
        "chosen_candidate_count": 0,
        "integrity_errors": [issue("input", str(exc))],
        "failures": [],
        "warnings": [],
        "limits": [],
    }


def main(argv: Sequence[str] | None = None) -> int:
    output_path: Path | None = None
    try:
        args = parse_args(argv)
        output_path = Path(args.output_file) if args.output_file else None
        pack = first_pack(load_json_arg(args.pack))
        composed = composed_object(load_json_arg(args.composed))
        result = audit_composed_prompt(pack, composed)
    except (AuditInputError, OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        result = _transport_error_result(exc)
        payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if output_path is not None:
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(payload, encoding="utf-8")
            except OSError:
                pass
        sys.stdout.write(payload)
        return 2

    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if output_path is not None:
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(payload, encoding="utf-8")
        except OSError as exc:
            error_result = _transport_error_result(exc)
            sys.stdout.write(json.dumps(error_result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            return 2
    sys.stdout.write(payload)
    if result["integrity_errors"]:
        return 2
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
