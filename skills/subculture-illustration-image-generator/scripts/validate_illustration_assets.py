#!/usr/bin/env python3
"""Validate research, typed runtime assets, and frozen illustration holdouts."""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

from illustration_runtime import (
    IllustrationRuntimeError,
    LEGACY_CONTRACT_VERSION,
    build_candidate_pack,
    canonical_json_bytes,
    default_asset_dir,
    load_runtime_assets,
    normalize_text,
    validate_assets,
)
from illustration_audit import audit_composed_prompt


RESEARCH_ROLE_VALUES = {"topic_matrix", "independent_source"}
PROVENANCE_VALUES = {"source_supported", "cross_source_synthesis", "design_inference"}
CANDIDATE_ROLE_VALUES = {"visual_atom", "router", "guard"}
UNIVERSAL_RESEARCH_ROLE_VALUES = {"topic_matrix", "independent_source"}
UNIVERSAL_CANDIDATE_ROLE_VALUES = {"visual_atom", "router", "guard", "metric"}
UNIVERSAL_RESEARCH_SCHEMA = "universal-scene-research/v1"
UNIVERSAL_RESEARCH_MANIFEST_SCHEMA = (
    "subculture_illustration_universal_scene_research_manifest/v1"
)
UNIVERSAL_SCENE_HOLDOUT_SCHEMA = "subculture_illustration_universal_scene_holdout/v1"
UNIVERSAL_SCENE_CONTRACT_HOLDOUT_SCHEMA = (
    "subculture_illustration_scene_contract_holdout/v1"
)
UNIVERSAL_SCENE_CONTRACT_SCHEMA = "subculture-illustration-scene-contract/v1"
UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SCHEMA = (
    "subculture_illustration_scene_contract_holdout/v2"
)
UNIVERSAL_V2_SCENE_CONTRACT_SCHEMA = "subculture-illustration-scene-contract/v2"
UNIVERSAL_RENDER_HOLDOUT_SCHEMA = "subculture_illustration_universal_render_holdout/v1"
UNIVERSAL_V2_CURRENT_HOLDOUT_SCHEMA = (
    "subculture_illustration_universal_scene_current_holdout/v2"
)
UNIVERSAL_V2_EXPECTATION_CROSSWALK_SCHEMA = (
    "subculture_illustration_universal_scene_expectation_crosswalk/v2"
)
UNIVERSAL_V2_CURRENT_MANIFEST_SCHEMA = (
    "subculture_illustration_universal_scene_current_holdout_manifest/v2"
)
UNIVERSAL_V2_BASELINE_SCHEMA = "subculture_illustration_universal_scene_baseline/v2"
UNIVERSAL_V1_PROMPT_HOLDOUT_SHA256 = (
    "109b4fab562e75d20d5a79daf0d2027890bc44366e380e21f2aa6ce9b356aaee"
)
UNIVERSAL_V1_SCENE_CONTRACT_HOLDOUT_SHA256 = (
    "c5f1a4fabfb029cfe8b5eb0c21d1208f2ab617cfdfd0e9034373196c4bc6d341"
)
UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SHA256 = (
    "6492bbe76aa7dd410636e0dcb0e565ce0906dcb913e7901fb7a8a502099958e6"
)
UNIVERSAL_V2_CURRENT_HOLDOUT_SHA256 = (
    "725c8eced155d4ec8b022fe7dd7a162f96b69c866c9f6c889dcb83b59ee359a5"
)
UNIVERSAL_V2_EXPECTATION_CROSSWALK_SHA256 = (
    "15c055462281b09a99531f97732ca43a6cd0fd6315f62d9f9fab62223ae22ff1"
)
UNIVERSAL_V2_CURRENT_MANIFEST_SHA256 = (
    "be6baf40ddfb449c52299f1b448703db474eefd9dcc5da6c27bd092bec964660"
)
UNIVERSAL_V1_BASELINE_SHA256 = (
    "cf072f22116614aa6dedb8f5f3b91e47ef889f44ce6119566c29c30562ebc294"
)
HISTORICAL_CONTRACT_VERSION_V2 = "subculture-illustration-candidate-pack/v2"
UNIVERSAL_CONTRACT_VERSION_V3 = "subculture-illustration-candidate-pack/v3"
UNIVERSAL_SLOT_IDS = ["expression", "pose", "action", "relation", "prop", "environment"]
UNIVERSAL_EVENT_ROLE_IDS = [
    "actor",
    "action",
    "target",
    "instrument",
    "recipient",
    "result",
    "location",
    "phase",
]
UNIVERSAL_CONTRACT_EFFECT_SUBJECT_BY_ID = {
    "active_weapon_discharge": "actor",
    "combat_opponent_assignment": "recipient",
    "combat_target_assignment": "target",
    "navigation_instrument_use": "actor",
    "romantic_contact": "actor",
    "scene_promise_hijack": "scene",
    "human_face_attachment": "source_entity",
    "human_hand_attachment": "source_entity",
    "human_limb_attachment": "source_entity",
}
UNIVERSAL_CONTRACT_EFFECT_TARGETS_BY_ID = {
    "active_weapon_discharge": [
        ("request", "concept"),
        ("slot", "action"),
        ("event_role", "action"),
        ("context", "violence"),
    ],
    "combat_opponent_assignment": [
        ("request", "concept"),
        ("slot", "relation"),
        ("event_role", "recipient"),
        ("event_role", "target"),
    ],
    "combat_target_assignment": [
        ("request", "concept"),
        ("slot", "action"),
        ("slot", "relation"),
        ("event_role", "target"),
    ],
    "navigation_instrument_use": [
        ("request", "concept"),
        ("slot", "action"),
        ("slot", "prop"),
        ("event_role", "action"),
        ("event_role", "instrument"),
    ],
    "romantic_contact": [
        ("request", "concept"),
        ("slot", "action"),
        ("slot", "relation"),
        ("event_role", "action"),
        ("event_role", "recipient"),
    ],
    "scene_promise_hijack": [
        ("request", "concept"),
        ("identity_fact", "feature_fact"),
        ("identity_fact", "scene_fact"),
        ("slot", "relation"),
        ("event_role", "result"),
    ],
    "human_face_attachment": [
        ("request", "concept"),
        ("identity_fact", "feature_fact"),
        ("identity_fact", "scene_fact"),
        ("slot", "expression"),
    ],
    "human_hand_attachment": [
        ("request", "concept"),
        ("identity_fact", "feature_fact"),
        ("identity_fact", "scene_fact"),
        ("slot", "pose"),
        ("slot", "action"),
    ],
    "human_limb_attachment": [
        ("request", "concept"),
        ("identity_fact", "feature_fact"),
        ("identity_fact", "scene_fact"),
        ("slot", "pose"),
    ],
}
UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS = [
    "affordance",
    "motivation",
    "identity_contrast",
    "mechanics",
    "ownership",
    "state_change",
    "consequence",
]
UNIVERSAL_DECISION_REASON_CODE_IDS = [
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
]
UNIVERSAL_RULE_REASON_CODES = {
    "rule_fixed_identity_precedence": "identity_overwrite",
    "rule_closed_prop": "closed_prop_slot",
    "rule_exactly_one_event": "event_spine_cardinality",
    "rule_resource_capacity": "resource_capacity",
    "rule_visible_middle_far_bridge": "visible_bridge_required",
    "rule_remote_budget": "remote_budget_exceeded",
    "rule_policy_independent_of_creativity": "policy_platform_blocked",
}
UNIVERSAL_V2_TARGET_KIND_IDS = [
    "slot",
    "event_role",
    "atom_facet",
    "visual_candidate",
    "resource_kind",
    "runtime_bridge_type",
    "pixel_evidence_kind",
    "guard_contract",
    "blocked_semantic",
    "context_profile_field",
    "semantic_load_axis",
    "embodiment_profile",
]
UNIVERSAL_V2_VISUAL_CANDIDATE_IDS = [
    "action_temporal_phases_release_recovery",
    "dpa_mixed_display_cue_cluster",
    "event_role_frames_action_predicate",
    "event_role_frames_shared_object_handoff",
    "gha_joint_attention_convergence",
    "gha_visible_target_line",
    "uao_global_prop_wooden_mallet",
    "uao_safe_inactive_hazard_orientation",
    "ubp_support_contact_map",
    "ugf_target_anchor_atom",
    "usc_contact_locomotor_surface_path",
    "usc_contact_release_transition",
    "usc_ecs_displacement_damage_repair_atom",
    "usc_ecs_environment_affordance_atom",
    "usc_ecs_material_residue_atom",
    "usc_ecs_witness_or_system_response_atom",
    "usc_relation_actor_effect_recipient_chain",
    "usc_relation_shared_target_convergence",
    "usc_sptg_context_anchor_relation",
    "ush_functional_configuration_state",
    "ush_layered_state_history",
    "ush_material_identity_boundary",
]
UNIVERSAL_V2_DERIVED_CANDIDATE_IDS = {
    "uao_global_prop_wooden_mallet",
    "uao_safe_inactive_hazard_orientation",
    "usc_contact_locomotor_surface_path",
    "usc_contact_release_transition",
    "usc_relation_actor_effect_recipient_chain",
    "ush_functional_configuration_state",
    "ush_layered_state_history",
    "ush_material_identity_boundary",
}
UNIVERSAL_V2_ATOM_FACETS = [
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
]
UNIVERSAL_V2_RESOURCE_KINDS = [
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
    "focal_primary",
    "focal_secondary",
    "foreground_salience",
    "event_peak",
    "prop_slot",
]
UNIVERSAL_V2_PIXEL_EVIDENCE_KINDS = [
    "contact",
    "orientation",
    "state_boundary",
    "support",
    "path",
    "residue",
    "display",
]
UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS = [
    "active_weapon_discharge",
    "combat_opponent_assignment",
    "combat_target_assignment",
    "navigation_instrument_use",
    "romantic_contact",
    "scene_promise_hijack",
    "human_face_attachment",
    "human_hand_attachment",
    "human_limb_attachment",
]
UNIVERSAL_V2_CONTEXT_PROFILE_FIELD_IDS = [
    "theme_tags",
    "era_technology",
    "tone",
    "violence",
    "social",
    "scale",
]
UNIVERSAL_V2_SEMANTIC_LOAD_AXIS_IDS = [
    "physical",
    "occupancy",
    "affective_valence",
    "affective_arousal",
    "violence",
    "visual_salience",
    "scene_importance",
    "theme_displacement",
]
UNIVERSAL_V2_REVISION = {
    "kind": "post_contract_qualification_revision",
    "revised_at": "2026-08-10",
    "frozen_before_implementation": False,
    "runtime_outputs_used": False,
}
UNIVERSAL_V2_CONTRACT_REVISION_BASE = {
    "kind": "post_contract_qualification_revision",
    "revised_at": "2026-08-10",
    "frozen_before_implementation": False,
    "runtime_outputs_used": False,
}
UNIVERSAL_V2_C16_EMBODIMENT_PROFILE_ID = (
    "four_armed_adult_equivalent_mechanical_humanoid"
)
UNIVERSAL_V2_C16_PROFILE_CAPACITIES = [
    ("manipulator", 4),
    ("attention_channel", 1),
    ("head_orientation", 1),
    ("support_contact", 2),
    ("mechanical_state_displacement", 2),
]
UNIVERSAL_V2_CUSTOM_EMBODIMENT_CORRECTIONS = {
    "universal_scene_04_explicit_apple": (
        1,
        "recipient_01",
        "unknown_guest_embodiment",
        "custom_unknown_guest_embodiment",
    ),
    "universal_scene_08_ambiguous_display_affect": (
        1,
        "recipient_01",
        "unspecified_handoff_recipient",
        "custom_unspecified_handoff_recipient",
    ),
    "universal_scene_09_shared_attention": (
        1,
        "actor_02",
        "winged_nonhuman_unspecified_life_stage",
        "custom_winged_nonhuman_unspecified_life_stage",
    ),
    "universal_scene_11_gesture_function": (
        1,
        "recipient_01",
        "unspecified_colleague",
        "custom_unspecified_colleague",
    ),
    "universal_scene_12_nonhuman_display": (
        0,
        "actor_01",
        "faceless_limbless_adult_cloud_nonhuman",
        "custom_faceless_limbless_adult_cloud_nonhuman",
    ),
}
UNIVERSAL_V2_HISTORICAL_FIXED_ROLE_NONAUTHORITIES = [
    (
        "universal_scene_04_explicit_apple",
        "instrument",
        "small_kitchen_knife",
        "/expected_event_frame/fixed_roles/instrument",
    ),
    (
        "universal_scene_05_explicit_hammer",
        "result",
        "mount_partially_reseated",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_06_explicit_machine_gun",
        "instrument",
        "gloved_hands",
        "/expected_event_frame/fixed_roles/instrument",
    ),
    (
        "universal_scene_06_explicit_machine_gun",
        "result",
        "safe_transport_readiness_assessed",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_07_fixed_facial_motion",
        "result",
        "fault_noticed",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_08_ambiguous_display_affect",
        "result",
        "message_handoff_pending",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_09_shared_attention",
        "result",
        "shared_hypothesis_and_next_move",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_10_pose_support",
        "instrument",
        "rope_and_body_weight",
        "/expected_event_frame/fixed_roles/instrument",
    ),
    (
        "universal_scene_10_pose_support",
        "result",
        "crate_moves_while_beam_flexes",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_11_gesture_function",
        "result",
        "colleague_halts_before_hazard",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_12_nonhuman_display",
        "result",
        "reduced_wind_on_climber",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_17_relation_topology",
        "recipient",
        "axis_holder",
        "/expected_event_frame/fixed_roles/recipient",
    ),
    (
        "universal_scene_18_prop_lexical_normalization",
        "result",
        "root_fragments_in_mortar",
        "/expected_event_frame/fixed_roles/result",
    ),
    (
        "universal_scene_22_theme_hijack_guard",
        "result",
        "orders_sorted",
        "/expected_event_frame/fixed_roles/result",
    ),
]
UNIVERSAL_V2_SEMANTIC_ANCHOR_EXCEPTIONS = {
    (
        "universal_scene_11_gesture_function",
        "event_role",
        "actor",
        "actor_01",
    ): [("성인 방역 기술자", "affirmative")],
    (
        "universal_scene_14_event_roles",
        "slot",
        "prop",
        "broken_lever_as_evidence",
    ): [
        ("부러진 레버", "affirmative"),
        ("증거물", "affirmative"),
        ("도구", "negated"),
    ],
    (
        "universal_scene_14_event_roles",
        "event_role",
        "target",
        "broken_lever_as_evidence",
    ): [
        ("부러진 레버", "affirmative"),
        ("증거물", "affirmative"),
        ("도구", "negated"),
    ],
    (
        "universal_scene_16_contact_resource",
        "event_role",
        "result",
        "nonconflicting_hand_contact_and_load",
    ): [
        ("각 손의 접촉", "affirmative"),
        ("하중", "affirmative"),
        ("충돌", "negated"),
    ],
    (
        "universal_scene_19_affordance_repurpose",
        "slot",
        "prop",
        "closed_broken_umbrella",
    ): [("고장 난 우산", "affirmative"), ("펴지", "negated")],
    (
        "universal_scene_19_affordance_repurpose",
        "event_role",
        "instrument",
        "closed_broken_umbrella_handle_and_ribs",
    ): [
        ("고장 난 우산", "affirmative"),
        ("펴지", "negated"),
        ("손잡이", "affirmative"),
        ("갈비살", "affirmative"),
    ],
    (
        "universal_scene_21_prop_narrative_role",
        "slot",
        "action",
        "jointly_investigate_broken_compass",
    ): [
        ("깨진 나침반", "affirmative"),
        ("함께 조사", "affirmative"),
        ("증거", "affirmative"),
        ("도구", "negated"),
    ],
    (
        "universal_scene_21_prop_narrative_role",
        "slot",
        "prop",
        "broken_compass_as_evidence",
    ): [
        ("깨진 나침반", "affirmative"),
        ("증거", "affirmative"),
        ("도구", "negated"),
    ],
    (
        "universal_scene_21_prop_narrative_role",
        "event_role",
        "target",
        "broken_compass_as_route_tampering_evidence",
    ): [
        ("깨진 나침반", "affirmative"),
        ("증거", "affirmative"),
        ("도구", "negated"),
    ],
}
UNIVERSAL_V2_MULTI_VALUE_PHRASE_BINDINGS = {
    ("universal_scene_13_atomic_action", "environment"): [
        ("stopped_subway_door", ["멈춘 자동문"]),
        ("door_gap", ["자동문 틈"]),
    ],
    ("universal_scene_14_event_roles", "prop"): [
        ("broken_lever_as_evidence", ["부러진 레버를 도구가 아니라 증거물로"]),
        ("cloth_wrap", ["천에 싸서"]),
    ],
    ("universal_scene_14_event_roles", "environment"): [
        ("sluice_lever_mount", ["빈 레버 자리"]),
        ("leak_onset", ["물이 새기 시작하는"]),
    ],
    ("universal_scene_15_action_phase", "prop"): [
        ("long_tongs", ["긴 집게"]),
        ("hot_glass_drop", ["뜨거운 유리 방울"]),
        ("support_block", ["받침"]),
    ],
    ("universal_scene_16_contact_resource", "prop"): [
        ("heavy_power_cell", ["무거운 동력 셀"]),
        ("locking_pin", ["잠금핀"]),
        ("guardrail", ["난간"]),
    ],
    ("universal_scene_17_relation_topology", "relation"): [
        (
            "three_member_task_topology",
            ["성인 세 명의 폭풍 관측팀", "관계 중심 키 아트"],
        ),
        ("shared_weather_vane_target", ["같은 목표를 보며"]),
    ],
    ("universal_scene_17_relation_topology", "prop"): [
        ("folding_weather_vane", ["하나의 접이식 풍향계"]),
        ("locking_pin", ["고정핀"]),
    ],
    ("universal_scene_18_prop_lexical_normalization", "prop"): [
        ("small_wooden_mallet", ["낡은 나무망치", "작은 목제 말렛"]),
        ("dried_roots", ["말린 뿌리"]),
    ],
}
UNIVERSAL_V2_COMPILED_OBLIGATION_SCHEMA = (
    "subculture_illustration_universal_scene_compiled_obligation_contract/v1"
)
UNIVERSAL_V2_VISUAL_CANDIDATE_TARGETS_BY_MAPPING = {
    "legacy_event.gesture": (["ugf_target_anchor_atom"], "all", "eligible"),
    "legacy_event.gesture_details": (["ugf_target_anchor_atom"], "all", "eligible"),
    "legacy_bridge.appraisal_ambiguity": (
        ["dpa_mixed_display_cue_cluster"],
        "all",
        "required",
    ),
    "legacy_bridge.attention_target": (["gha_visible_target_line"], "all", "required"),
    "legacy_bridge.body_environment_contact": (
        ["usc_contact_locomotor_surface_path"],
        "all",
        "required",
    ),
    "legacy_bridge.contact_transition": (
        [
            "action_temporal_phases_release_recovery",
            "usc_contact_release_transition",
        ],
        "all",
        "required",
    ),
    "legacy_bridge.environment_consequence": (
        [
            "usc_ecs_displacement_damage_repair_atom",
            "usc_ecs_environment_affordance_atom",
            "usc_ecs_material_residue_atom",
            "usc_ecs_witness_or_system_response_atom",
        ],
        "any",
        "required",
    ),
    "legacy_bridge.hazard_consequence": (
        [
            "usc_ecs_displacement_damage_repair_atom",
            "usc_ecs_material_residue_atom",
            "usc_ecs_witness_or_system_response_atom",
        ],
        "any",
        "required",
    ),
    "legacy_bridge.lexical_normalization": (
        ["uao_global_prop_wooden_mallet"],
        "all",
        "required",
    ),
    "legacy_bridge.load": (["ubp_support_contact_map"], "all", "required"),
    "legacy_bridge.material": (["ush_material_identity_boundary"], "all", "required"),
    "legacy_bridge.protective_relation": (
        ["usc_relation_actor_effect_recipient_chain"],
        "all",
        "required",
    ),
    "legacy_bridge.risk_posture": (
        ["uao_safe_inactive_hazard_orientation"],
        "all",
        "required",
    ),
    "legacy_bridge.shared_attention": (
        ["gha_joint_attention_convergence"],
        "all",
        "required",
    ),
    "legacy_bridge.shared_target": (
        ["usc_relation_shared_target_convergence"],
        "all",
        "required",
    ),
    "legacy_bridge.state": (["ush_functional_configuration_state"], "all", "required"),
    "legacy_bridge.state_history": (["ush_layered_state_history"], "all", "required"),
    "legacy_bridge.temporal_phase": (
        ["action_temporal_phases_release_recovery"],
        "all",
        "required",
    ),
    "legacy_bridge.tone": (["usc_sptg_context_anchor_relation"], "all", "required"),
    "legacy_bridge.work_routine": (
        ["event_role_frames_action_predicate"],
        "all",
        "required",
    ),
}
UNIVERSAL_V2_LITERAL_REALIZATION_PROFILE_SPECS = [
    (
        "lvr_safe_inactive_hazard_orientation",
        "action",
        "inactive_hazard_orientation",
        "pose",
        ["uao_safe_inactive_hazard_orientation"],
        "request_text",
        [
            (
                ["firearm", "gun", "machine gun", "weapon", "기관총", "무기", "총기"],
                "affirmative",
            ),
            (
                [
                    "carry sling",
                    "safety cover",
                    "secure",
                    "secured",
                    "안전 덮개",
                    "운반 끈",
                ],
                "affirmative",
            ),
            (["discharge", "fire", "firing", "shoot", "발사"], "negated"),
        ],
        ["orientation", "support"],
        ["support_contact"],
        10,
    ),
    (
        "lvr_directed_attention_target",
        "action",
        "directed_attention",
        "attention",
        ["gha_visible_target_line"],
        "slot_phrases",
        [
            (
                [
                    "examine",
                    "inspect",
                    "look at",
                    "scrutinize",
                    "바라보",
                    "바라보다",
                    "살피다",
                    "살피며",
                    "점검",
                ],
                "affirmative",
            )
        ],
        ["orientation"],
        ["attention_channel"],
        20,
    ),
    (
        "lvr_ambiguous_restrained_display",
        "expression",
        "mixed_display",
        "perceived_affect",
        ["dpa_mixed_display_cue_cluster"],
        "slot_phrases",
        [
            (
                ["ambiguous", "either reading", "두 감정", "양가", "처럼도"],
                "affirmative",
            ),
            (["restrained", "suppressed", "억제", "절제"], "affirmative"),
        ],
        ["display"],
        [],
        30,
    ),
    (
        "lvr_shared_attention_convergence",
        "relation",
        "shared_attention",
        "attention",
        ["gha_joint_attention_convergence"],
        "slot_phrases",
        [
            (
                [
                    "jointly inspect",
                    "look together",
                    "same target",
                    "shared attention",
                    "같은 목표",
                    "공유 주의",
                    "동시에 바라보",
                    "함께 조사",
                ],
                "affirmative",
            )
        ],
        ["orientation"],
        ["attention_channel"],
        40,
    ),
    (
        "lvr_distributed_load_support",
        "pose",
        "visible_support_map",
        "pose",
        ["ubp_support_contact_map"],
        "slot_phrases",
        [
            (["heavy", "load", "weight", "무거운", "무게", "하중"], "affirmative"),
            (["brace", "distribute", "support", "받치", "분산", "지지"], "affirmative"),
        ],
        ["support"],
        ["support_contact"],
        50,
    ),
    (
        "lvr_hazard_consequence",
        "environment",
        "material_leak_trace",
        "consequence",
        ["usc_ecs_material_residue_atom"],
        "slot_phrases",
        [(["hazard", "leak", "spill", "누출", "새는", "위험"], "affirmative")],
        ["residue"],
        [],
        60,
    ),
    (
        "lvr_protective_recipient_path",
        "relation",
        "directed_recipient_effect",
        "relation",
        ["usc_relation_actor_effect_recipient_chain"],
        "slot_phrases",
        [
            (
                [
                    "clear a path",
                    "protect",
                    "shield",
                    "길을 만드",
                    "길을 만들",
                    "보호",
                    "지키",
                ],
                "affirmative",
            )
        ],
        ["orientation", "support"],
        ["focal_secondary"],
        70,
    ),
    (
        "lvr_environment_consequence",
        "action",
        "environment_response",
        "consequence",
        ["usc_ecs_environment_affordance_atom"],
        "slot_phrases",
        [
            (
                [
                    "clear a path",
                    "displace",
                    "shield",
                    "windbreak",
                    "길을 만들",
                    "바람막이",
                    "보호",
                ],
                "affirmative",
            )
        ],
        ["residue"],
        [],
        80,
    ),
    (
        "lvr_release_recovery_phase",
        "action",
        "release_recovery_phase",
        "phase",
        ["action_temporal_phases_release_recovery"],
        "slot_phrases",
        [
            (
                ["after placing", "just after", "release after", "내려놓은", "직후"],
                "affirmative",
            )
        ],
        ["contact"],
        [],
        90,
    ),
    (
        "lvr_insert_resistance_contact_commitment",
        "action",
        "contact_commitment_phase",
        "phase",
        ["action_temporal_phases_contact_commitment"],
        "slot_phrases",
        [
            (["insert", "inserting", "put in", "넣고", "삽입"], "affirmative"),
            (["resistance", "resistive", "저항"], "affirmative"),
        ],
        ["path"],
        [],
        95,
    ),
    (
        "lvr_release_contact_transition",
        "action",
        "release_recovery_phase",
        "contact",
        ["usc_contact_release_transition"],
        "request_text",
        [
            (["contact", "junction", "접촉"], "affirmative"),
            (["relax", "release", "separate", "분리", "풀리"], "affirmative"),
        ],
        ["contact", "state_boundary"],
        [],
        100,
    ),
    (
        "lvr_shared_target_convergence",
        "relation",
        "shared_target_relation",
        "relation",
        ["usc_relation_shared_target_convergence"],
        "slot_phrases",
        [
            (
                [
                    "same object",
                    "same target",
                    "shared target",
                    "같은 대상",
                    "같은 목표",
                    "공동 목표",
                    "공유 주의",
                ],
                "affirmative",
            )
        ],
        ["orientation"],
        ["focal_secondary"],
        110,
    ),
    (
        "lvr_wooden_mallet_prop",
        "prop",
        "typed_prop_identity",
        "prop",
        ["uao_global_prop_wooden_mallet"],
        "slot_phrases",
        [
            (["mallet", "木槌", "木锤", "나무망치", "말렛"], "affirmative"),
            (["wood", "wooden", "木製", "木质", "나무", "목제"], "affirmative"),
        ],
        ["state_boundary"],
        ["prop_slot"],
        120,
    ),
    (
        "lvr_visible_material_identity",
        "prop",
        "material_identity_boundary",
        "prop_state",
        ["ush_material_identity_boundary"],
        "slot_phrases",
        [
            (
                [
                    "fabric",
                    "glass",
                    "leather",
                    "metal",
                    "wood",
                    "가죽",
                    "금속",
                    "나무",
                    "목제",
                    "유리",
                    "천",
                ],
                "affirmative",
            )
        ],
        ["state_boundary"],
        [],
        130,
    ),
    (
        "lvr_broken_closed_configuration",
        "prop",
        "functional_configuration_state",
        "prop_state",
        ["ush_functional_configuration_state"],
        "slot_phrases",
        [
            (["broken", "damaged", "고장", "부러진", "파손"], "affirmative"),
            (["open", "unfold", "열", "펴", "펼"], "negated"),
        ],
        ["state_boundary"],
        [],
        140,
    ),
    (
        "lvr_layered_state_history",
        "prop",
        "layered_state_history",
        "prop_state",
        ["ush_layered_state_history"],
        "request_text",
        [
            (["abrasion", "scuff", "wear", "worn", "닳", "마모"], "affirmative"),
            (["patch", "repair", "stitch", "수선", "패치"], "affirmative"),
            (["lubricant", "oil", "residue", "기름", "윤활유", "잔류"], "affirmative"),
        ],
        ["residue", "state_boundary"],
        [],
        150,
    ),
    (
        "lvr_quiet_everyday_context",
        "environment",
        "context_anchor_relation",
        "environment",
        ["usc_sptg_context_anchor_relation"],
        "request_text",
        [
            (["calm", "gentle", "quiet", "잔잔", "조용"], "affirmative"),
            (["daily", "everyday", "routine", "일상", "평범"], "affirmative"),
        ],
        ["path"],
        [],
        160,
    ),
    (
        "lvr_work_routine_action",
        "action",
        "action_observable_relation",
        "action",
        ["event_role_frames_action_predicate"],
        "slot_phrases",
        [
            (["arrange", "organize", "record", "sort", "기록", "정리"], "affirmative"),
            (["ledger", "order book", "register", "장부", "주문서"], "affirmative"),
        ],
        ["path"],
        [],
        170,
    ),
    (
        "lvr_locomotor_surface_contact",
        "action",
        "locomotor_surface_path",
        "contact",
        ["usc_contact_locomotor_surface_path"],
        "slot_phrases",
        [
            (
                [
                    "body traversal",
                    "pass through",
                    "traverse",
                    "walk through",
                    "몸으로",
                    "지나가",
                    "통과",
                ],
                "affirmative",
            ),
            (["ground", "path", "surface", "갈대밭", "길", "지면"], "affirmative"),
        ],
        ["contact", "support"],
        ["locomotor_contact"],
        180,
    ),
]
UNIVERSAL_V2_EVALUATOR_IDS = {
    ("slot", "canonical_projection"): "canonical_slot_projection_v1",
    ("slot", "eligible"): "eligible_slot_v1",
    ("slot", "absent"): "absent_slot_materialization_v1",
    ("slot", "required"): "required_slot_materialization_v1",
    ("event_role", "canonical_projection"): "canonical_event_role_projection_v1",
    ("event_role", "eligible"): "eligible_event_role_v1",
    ("event_role", "absent"): "absent_event_role_v1",
    ("event_role", "required"): "required_event_role_v1",
    (
        "context_profile_field",
        "canonical_projection",
    ): "canonical_context_profile_projection_v1",
    (
        "embodiment_profile",
        "canonical_projection",
    ): "canonical_embodiment_profile_projection_v1",
    ("atom_facet", "eligible"): "eligible_atom_facet_v1",
    ("atom_facet", "absent"): "absent_atom_facet_v1",
    ("atom_facet", "required"): "required_atom_facet_v1",
    ("visual_candidate", "eligible"): "eligible_visual_candidate_v1",
    ("visual_candidate", "required"): "required_visual_candidate_v1",
    ("resource_kind", "eligible"): "eligible_resource_kind_v1",
    ("resource_kind", "absent"): "absent_resource_kind_v1",
    ("resource_kind", "required"): "required_resource_kind_v1",
    ("runtime_bridge_type", "eligible"): "eligible_runtime_bridge_type_v1",
    ("runtime_bridge_type", "required"): "required_runtime_bridge_type_v1",
    ("pixel_evidence_kind", "eligible"): "eligible_pixel_evidence_kind_v1",
    ("pixel_evidence_kind", "required"): "required_pixel_evidence_kind_v1",
    ("guard_contract", "required"): "required_guard_binding_v1",
    ("blocked_semantic", "absent"): "absent_blocked_semantic_v1",
    ("semantic_load_axis", "absent"): "zero_semantic_load_axis_v1",
}
UNIVERSAL_DISTANCE_AXIS_IDS = [
    "theme",
    "era_technology",
    "tone",
    "violence",
    "social",
    "scale",
    "salience_displacement",
]
UNIVERSAL_LOAD_AXIS_IDS = [
    "physical",
    "occupancy",
    "affective_valence",
    "affective_arousal",
    "violence",
    "visual_salience",
    "scene_importance",
    "theme_displacement",
]
UNIVERSAL_EFFECT_SOURCE_KIND_IDS = [
    "visual_candidate",
    "proposal_profile",
    "context_profile",
    "bridge_type",
    "resource_kind",
]
UNIVERSAL_RESEARCH_EXPECTED_TOTALS = {
    "record_count": 60,
    "topic_count": 20,
    "independent_source_count": 40,
    "mechanism_count": 167,
    "candidate_count": 220,
    "pixel_evidence_count": 97,
    "unique_source_url_count": 40,
    "candidate_role_counts": {
        "visual_atom": 97,
        "router": 38,
        "guard": 52,
        "metric": 33,
    },
    "mechanism_provenance_counts": {
        "source_supported": 47,
        "cross_source_synthesis": 10,
        "design_inference": 110,
    },
}
GENERATION_RETRY_POLICY_SCHEMA = "subculture-illustration-generation-retry-policy/v1"
GENERATION_RETRY_PHASES = ["primary_generation", "fallback_repair_generation"]
GENERATION_RETRY_OUTCOMES = {
    "tool_error",
    "transport_error",
    "server_error",
    "rate_limit",
    "timeout",
    "empty_result",
    "inaccessible_result",
    "safety_refusal",
    "policy_refusal",
    "other_refusal",
}
GENERATION_RETRY_PRESERVED_FIELDS = {
    "prompt_en",
    "negative_en",
    "pack_id",
    "chosen_candidate_ids",
    "seed",
    "generation_parameters",
}
LEGACY_PROMPT_QUALIFICATION_RUNTIME_SHA256 = (
    "0b44e7ea63517a963d26e1b897d1561c724013eb4ce7b5d9f31a1b9310994e57"
)
LEGACY_PROMPT_QUALIFICATION_AUDIT_SHA256 = (
    "c1a4d21b6476d4b7acaeab189780c409b863ba650505737599ee534d5e79d159"
)
V2_PROMPT_QUALIFICATION_RUNTIME_SHA256 = (
    "b51034902366418f9a406523d258fd97f6c98f24e79c61b9691c6cced5194a79"
)
V2_PROMPT_QUALIFICATION_AUDIT_SHA256 = (
    "e69b5ddda10e5f647ec5ea7de6c6dc8b71a294f93f11b0a2dd1f9118af6485b6"
)
PRE_UNIVERSAL_GENERATOR_CLI_SHA256 = (
    "48d58077379964fdcf2b018a4c6b8914b1eeca3f9984489bee0e5bd9e2cab5c5"
)
PRE_UNIVERSAL_AUDIT_CLI_SHA256 = (
    "a5b1a6a3658ed6e28fe1b2a47ec0a793ec3833962dbc6ae0091c2a5d6e27cb97"
)
RUNTIME_NAME_GUARDS = (
    re.compile(r"\bin (?:the )?style of\b", re.IGNORECASE),
    re.compile(r"\bby (?:artist|illustrator|mangaka|studio)\b", re.IGNORECASE),
    re.compile(
        r"\b(?:Pok[eé]mon|Pikachu|Naruto|One Piece|Gundam|Evangelion|Genshin Impact|Honkai|Disney|Marvel|Sanrio)\b",
        re.IGNORECASE,
    ),
)

CASE01_V2_SECOND_LOOK_PLAN = {
    "schema": "illustration-second-look-plan/v1",
    "selected_proposal_id": "render01_proposal_d",
    "reveal_phrase": (
        "Second look: the brass threshold and receiving mat already register the coat's "
        "arrival before the real handoff is complete."
    ),
    "review_scale_ids": ["native"],
    "primary_carrier": {
        "carrier_kind": "material_boundary",
        "carrier_phrase": "one broad pale seam",
        "protected_locus_phrase": (
            "the clear brass threshold strip beneath the closing doorway"
        ),
        "consequence_phrase": (
            "The pale luminous seam crosses the brass threshold before the real handoff "
            "is complete"
        ),
        "risk_flags": [],
    },
    "fallback_carrier": {
        "carrier_kind": "surface_state",
        "carrier_phrase": "one broad dry coat-length patch",
        "protected_locus_phrase": "the unoccupied receiving mat below the doorway",
        "consequence_phrase": (
            "Rain beads stop at a broad dry coat-length boundary on the unoccupied "
            "receiving mat"
        ),
        "risk_flags": [],
    },
}

CASE01_V3_SECOND_LOOK_PLAN = {
    "schema": "illustration-second-look-plan/v1",
    "selected_proposal_id": "render01_proposal_d",
    "reveal_phrase": (
        "Second look: the untouched closing bell is already swinging while the "
        "repaired coat and recipient hand remain separated."
    ),
    "review_scale_ids": ["native", "thumbnail_320px"],
    "primary_carrier": {
        "carrier_kind": "object_relation",
        "carrier_phrase": (
            "one large isolated brass closing bell already leaning on a taut crimson "
            "thread"
        ),
        "protected_locus_phrase": (
            "the clear black doorway above the untouched recipient hand"
        ),
        "consequence_phrase": (
            "The isolated brass closing bell leans and its displaced clapper swings "
            "while the repaired coat and recipient hand remain separated"
        ),
        "risk_flags": [],
    },
    "fallback_carrier": {
        "carrier_kind": "surface_state",
        "carrier_phrase": "one broad irregular dry coat-length patch",
        "protected_locus_phrase": (
            "the plain seamless dark receiving slab below the doorway"
        ),
        "consequence_phrase": (
            "Rain beads stop around one broad irregular dry coat-length patch that "
            "crosses the continuous grain of the plain dark receiving slab."
        ),
        "risk_flags": [],
    },
}


class ValidationFailure(ValueError):
    """Raised when a versioned asset violates the frozen contract."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line.strip():
            continue
        value = json.loads(line)
        _require(
            isinstance(value, dict), f"{path.name}:{line_number} must be an object"
        )
        rows.append(value)
    return rows


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _strings(value: Any, label: str, *, minimum: int = 0) -> list[str]:
    _require(isinstance(value, list), f"{label} must be a list")
    _require(
        all(isinstance(item, str) and item.strip() for item in value),
        f"{label} must contain strings",
    )
    _require(len(value) >= minimum, f"{label} must contain at least {minimum} values")
    return list(value)


def validate_generation_retry_policy(asset_dir: Path) -> dict[str, Any]:
    policy = _load_json(asset_dir / "image_generation_retry_policy_v1.json")
    _require(isinstance(policy, dict), "generation retry policy must be an object")
    _require(
        policy.get("schema") == GENERATION_RETRY_POLICY_SCHEMA,
        "generation retry policy schema mismatch",
    )
    _require(
        policy.get("retry_budget_scope") == "per_generation_phase",
        "generation retry budget must be per phase",
    )
    _require(
        policy.get("phases") == GENERATION_RETRY_PHASES,
        "generation retry phases mismatch",
    )
    _require(
        policy.get("initial_calls_per_phase") == 1,
        "generation phase must start with one call",
    )
    _require(
        policy.get("max_unchanged_retries_after_initial") == 3,
        "generation phase must allow exactly three unchanged retries",
    )
    _require(
        policy.get("max_calls_per_phase") == 4,
        "generation phase must allow four total calls",
    )
    outcomes = _strings(
        policy.get("retryable_no_image_outcomes"),
        "generation retry outcomes",
        minimum=1,
    )
    _require(
        set(outcomes) == GENERATION_RETRY_OUTCOMES, "generation retry outcomes mismatch"
    )
    preserved = _strings(
        policy.get("preserve_exact_fields"),
        "generation retry preserved fields",
        minimum=1,
    )
    _require(
        set(preserved) == GENERATION_RETRY_PRESERVED_FIELDS,
        "generation retry preserved fields mismatch",
    )
    for field in (
        "stop_on_first_concrete_image",
        "retry_does_not_consume_pixel_repair_slot",
        "no_prompt_rewrite_between_retries",
        "no_policy_evasion",
        "higher_priority_platform_stop_applies",
    ):
        _require(
            policy.get(field) is True, f"generation retry policy requires {field}=true"
        )
    _require(
        policy.get("exhausted_status") == "generation_failed_retries_exhausted",
        "generation retry exhausted status mismatch",
    )
    return {
        "schema": policy["schema"],
        "max_unchanged_retries_after_initial": policy[
            "max_unchanged_retries_after_initial"
        ],
        "max_calls_per_phase": policy["max_calls_per_phase"],
        "includes_safety_refusal": "safety_refusal" in outcomes,
        "includes_policy_refusal": "policy_refusal" in outcomes,
        "status": "pass",
    }


def validate_research(asset_dir: Path) -> dict[str, Any]:
    evidence_dir = asset_dir / "research_evidence_illustration"
    manifest = _load_json(evidence_dir / "manifest.json")
    _require(
        manifest.get("schema") == "subculture_illustration_research_manifest_v1",
        "research manifest schema mismatch",
    )
    shards = manifest.get("shards")
    _require(
        isinstance(shards, list) and len(shards) == 6,
        "research manifest must list six shards",
    )

    rows: list[dict[str, Any]] = []
    shard_results: list[dict[str, Any]] = []
    for entry in shards:
        _require(isinstance(entry, dict), "research shard entry must be an object")
        rel = entry.get("path")
        _require(
            isinstance(rel, str) and rel and Path(rel).name == rel,
            "research shard path must be one local filename",
        )
        path = evidence_dir / rel
        _require(path.is_file(), f"missing research shard {rel}")
        digest = _sha256(path)
        _require(digest == entry.get("sha256"), f"research shard hash mismatch: {rel}")
        shard_rows = _load_jsonl(path)
        _require(
            len(shard_rows) == entry.get("record_count"),
            f"research shard row count mismatch: {rel}",
        )
        rows.extend(shard_rows)
        shard_results.append(
            {"path": rel, "record_count": len(shard_rows), "sha256": digest}
        )

    _require(
        len(rows) == manifest.get("record_count") == 72,
        "research record count must be 72",
    )
    record_ids = [row.get("id") for row in rows]
    _require(
        all(isinstance(item, str) and item for item in record_ids),
        "research record id must be nonempty",
    )
    _require(
        len(record_ids) == len(set(record_ids)),
        "research record ids must be globally unique",
    )
    live_record_ids = set(record_ids)

    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        topic_id = row.get("topic_id")
        _require(
            isinstance(topic_id, str) and topic_id, "research topic_id must be nonempty"
        )
        _require(
            row.get("record_role") in RESEARCH_ROLE_VALUES,
            f"{topic_id} has invalid record_role",
        )
        _require(
            row.get("status") == "approved", f"{topic_id} research row is not approved"
        )
        by_topic[topic_id].append(row)
    _require(
        len(by_topic) == manifest.get("topic_count") == 24,
        "research topic count must be 24",
    )

    all_candidate_ids: list[str] = []
    candidate_specs: dict[str, tuple[str, str, str]] = {}
    provenance_counts: Counter[str] = Counter()
    matrix_ids: dict[str, str] = {}
    for topic_id, topic_rows in by_topic.items():
        matrices = [row for row in topic_rows if row["record_role"] == "topic_matrix"]
        sources = [
            row for row in topic_rows if row["record_role"] == "independent_source"
        ]
        _require(
            len(topic_rows) == 3 and len(matrices) == 1 and len(sources) == 2,
            f"{topic_id} must have one matrix and two sources",
        )
        _require(
            len({row.get("source_url") for row in topic_rows}) == 3,
            f"{topic_id} must have three distinct URLs",
        )
        matrix = matrices[0]
        matrix_ids[topic_id] = matrix["id"]
        source_ids = {row["id"] for row in sources}
        _require(
            set(matrix.get("synthesis_evidence_ids", [])) == source_ids,
            f"{topic_id} synthesis IDs mismatch",
        )

        mechanisms = matrix.get("mechanisms")
        provenance = matrix.get("mechanism_provenance")
        _require(
            isinstance(mechanisms, list) and 6 <= len(mechanisms) <= 10,
            f"{topic_id} mechanism count/shape mismatch",
        )
        _require(
            isinstance(provenance, list) and len(provenance) == len(mechanisms),
            f"{topic_id} provenance count mismatch",
        )
        _require(
            all(
                isinstance(item, dict) and set(item) == {"id", "statement"}
                for item in mechanisms
            ),
            f"{topic_id} mechanism shape mismatch",
        )
        _require(
            all(
                isinstance(item, dict)
                and set(item) == {"mechanism_id", "provenance", "evidence_ids"}
                for item in provenance
            ),
            f"{topic_id} provenance shape mismatch",
        )
        mechanism_ids = [item["id"] for item in mechanisms]
        _require(
            mechanism_ids == [item["mechanism_id"] for item in provenance],
            f"{topic_id} mechanism/provenance order mismatch",
        )
        _require(
            len(mechanism_ids) == len(set(mechanism_ids)),
            f"{topic_id} duplicate mechanism IDs",
        )
        for item in provenance:
            kind = item["provenance"]
            provenance_counts[kind] += 1
            _require(
                kind in PROVENANCE_VALUES, f"{topic_id} invalid provenance kind {kind}"
            )
            refs = _strings(
                item["evidence_ids"],
                f"{topic_id}.{item['mechanism_id']}.evidence_ids",
                minimum=1,
            )
            _require(
                set(refs) <= live_record_ids,
                f"{topic_id} provenance has unknown record",
            )
            if kind == "cross_source_synthesis":
                _require(
                    source_ids <= set(refs),
                    f"{topic_id} cross-source mechanism lacks both sources",
                )

        candidate_ids = _strings(
            matrix.get("candidate_ids"), f"{topic_id}.candidate_ids", minimum=1
        )
        definitions = matrix.get("candidate_definitions")
        roles = matrix.get("candidate_roles")
        _require(
            isinstance(definitions, dict) and set(definitions) == set(candidate_ids),
            f"{topic_id} candidate definitions mismatch",
        )
        _require(
            isinstance(roles, dict) and set(roles) == set(candidate_ids),
            f"{topic_id} candidate roles mismatch",
        )
        _require(
            set(roles.values()) <= CANDIDATE_ROLE_VALUES,
            f"{topic_id} invalid candidate role",
        )
        evidence_ids = _strings(
            matrix.get("illustration_evidence"),
            f"{topic_id}.illustration_evidence",
            minimum=1,
        )
        evidence_definitions = matrix.get("illustration_evidence_definitions")
        _require(
            isinstance(evidence_definitions, dict)
            and set(evidence_definitions) == set(evidence_ids),
            f"{topic_id} illustration evidence definitions mismatch",
        )
        _require(
            set(evidence_ids) <= set(candidate_ids),
            f"{topic_id} illustration evidence is not a candidate subset",
        )
        _require(
            all(roles[item] == "visual_atom" for item in evidence_ids),
            f"{topic_id} illustration evidence must be visual",
        )
        for field in (
            "compatibility",
            "conflicts",
            "counterexamples",
            "boundaries",
            "format_implications",
            "viewer_implications",
        ):
            _strings(matrix.get(field), f"{topic_id}.{field}", minimum=4)
        all_candidate_ids.extend(candidate_ids)
        for candidate_id in candidate_ids:
            candidate_specs[candidate_id] = (
                definitions[candidate_id],
                roles[candidate_id],
                topic_id,
            )

    _require(
        len(all_candidate_ids) == manifest.get("candidate_count") == 264,
        "research candidate count must be 264",
    )
    _require(
        len(all_candidate_ids) == len(set(all_candidate_ids)),
        "research candidate IDs must be globally unique",
    )
    expected_provenance = manifest.get("provenance_counts")
    _require(
        dict(provenance_counts) == expected_provenance,
        "research provenance counts do not match manifest",
    )
    _require(
        sum(provenance_counts.values()) == manifest.get("mechanism_count") == 192,
        "research mechanism count must be 192",
    )
    return {
        "record_count": len(rows),
        "topic_count": len(by_topic),
        "mechanism_count": sum(provenance_counts.values()),
        "candidate_count": len(all_candidate_ids),
        "candidate_ids": set(all_candidate_ids),
        "candidate_specs": candidate_specs,
        "matrix_ids": matrix_ids,
        "topic_record_ids": {
            topic_id: {row["id"] for row in topic_rows}
            for topic_id, topic_rows in by_topic.items()
        },
        "provenance_counts": dict(sorted(provenance_counts.items())),
        "shards": shard_results,
    }


def validate_universal_scene_research(asset_dir: Path) -> dict[str, Any]:
    """Validate the independently audited 20-topic universal-scene corpus."""

    evidence_dir = asset_dir / "research_evidence_universal_scene"
    manifest_path = evidence_dir / "manifest.json"
    manifest = _load_json(manifest_path)
    _require(
        manifest.get("schema") == UNIVERSAL_RESEARCH_MANIFEST_SCHEMA,
        "universal research manifest schema mismatch",
    )
    _require(
        manifest.get("status") == "approved",
        "universal research manifest is not approved",
    )
    _require(
        manifest.get("totals") == UNIVERSAL_RESEARCH_EXPECTED_TOTALS,
        "universal research frozen totals mismatch",
    )
    audit = manifest.get("independent_audit")
    _require(isinstance(audit, dict), "universal research independent audit is missing")
    _require(
        audit.get("verdict") == "pass"
        and audit.get("critical") == 0
        and audit.get("high") == 0
        and audit.get("medium") == 0,
        "universal research independent audit is not clean",
    )

    shards = manifest.get("shards")
    _require(
        isinstance(shards, list) and len(shards) == 6,
        "universal research must list six shards",
    )
    rows: list[dict[str, Any]] = []
    shard_results: list[dict[str, Any]] = []
    declared_topic_ids: list[str] = []
    for entry in shards:
        _require(
            isinstance(entry, dict), "universal research shard entry must be an object"
        )
        _require(
            set(entry) == {"path", "sha256", "record_count", "topic_ids"},
            "universal research shard entry field mismatch",
        )
        rel = entry.get("path")
        _require(
            isinstance(rel, str)
            and rel
            and Path(rel).name == rel
            and rel.endswith(".jsonl"),
            "universal research shard path must be one local JSONL filename",
        )
        path = evidence_dir / rel
        _require(path.is_file(), f"missing universal research shard {rel}")
        digest = _sha256(path)
        _require(
            digest == entry.get("sha256"),
            f"universal research shard hash mismatch: {rel}",
        )
        shard_rows = _load_jsonl(path)
        _require(
            len(shard_rows) == entry.get("record_count"),
            f"universal research shard row count mismatch: {rel}",
        )
        shard_topics = _strings(entry.get("topic_ids"), f"{rel}.topic_ids", minimum=1)
        _require(
            {str(row.get("topic_id")) for row in shard_rows} == set(shard_topics),
            f"universal research shard topic coverage mismatch: {rel}",
        )
        rows.extend(shard_rows)
        declared_topic_ids.extend(shard_topics)
        shard_results.append(
            {"path": rel, "record_count": len(shard_rows), "sha256": digest}
        )

    _require(len(rows) == 60, "universal research record count must be 60")
    _require(
        len(declared_topic_ids) == len(set(declared_topic_ids)) == 20,
        "universal research shard topics must partition 20 topics",
    )
    _require(
        manifest.get("topic_ids") == declared_topic_ids,
        "universal research manifest topic order must match shard order",
    )
    matrix_keys = {
        "schema",
        "record_id",
        "topic_id",
        "record_role",
        "reviewed_at",
        "status",
        "synthesis_evidence_ids",
        "research_questions",
        "mechanisms",
        "mechanism_provenance",
        "candidate_ids",
        "candidate_definitions",
        "candidate_roles",
        "pixel_evidence_ids",
        "pixel_evidence_definitions",
        "compatibility",
        "conflicts",
        "counterexamples",
        "boundaries",
        "domain_limits",
        "embodiment_limits",
        "cultural_limits",
        "source_biases",
        "runtime_implications",
        "evaluation_implications",
    }
    source_keys = {
        "schema",
        "record_id",
        "topic_id",
        "record_role",
        "reviewed_at",
        "status",
        "source_url",
        "title",
        "source_type",
        "authority",
        "abstracted_dimensions",
        "supported_candidate_ids",
        "limitations",
    }
    record_ids = [row.get("record_id") for row in rows]
    _require(
        all(isinstance(value, str) and value for value in record_ids)
        and len(record_ids) == len(set(record_ids)),
        "universal research record IDs must be globally unique strings",
    )
    all_record_ids = set(record_ids)
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        _require(
            row.get("schema") == UNIVERSAL_RESEARCH_SCHEMA,
            "universal research row schema mismatch",
        )
        _require(
            row.get("reviewed_at") == "2026-08-10",
            "universal research review date drift",
        )
        _require(
            row.get("status") == "approved", "universal research row is not approved"
        )
        _require(
            row.get("record_role") in UNIVERSAL_RESEARCH_ROLE_VALUES,
            "universal research row role mismatch",
        )
        topic_id = row.get("topic_id")
        _require(
            isinstance(topic_id, str) and topic_id,
            "universal research topic ID missing",
        )
        by_topic[topic_id].append(row)
        expected_keys = (
            matrix_keys if row["record_role"] == "topic_matrix" else source_keys
        )
        _require(
            set(row) == expected_keys,
            f"universal research row field mismatch: {row['record_id']}",
        )

    _require(
        set(by_topic) == set(declared_topic_ids),
        "universal research topic coverage mismatch",
    )
    candidate_ids: list[str] = []
    pixel_evidence_ids: list[str] = []
    mechanism_ids: list[str] = []
    source_urls: list[str] = []
    role_counts: Counter[str] = Counter()
    provenance_counts: Counter[str] = Counter()
    candidate_specs: dict[str, dict[str, Any]] = {}
    topic_record_ids: dict[str, set[str]] = {}
    for topic_id, topic_rows in by_topic.items():
        matrices = [row for row in topic_rows if row["record_role"] == "topic_matrix"]
        sources = [
            row for row in topic_rows if row["record_role"] == "independent_source"
        ]
        _require(
            len(topic_rows) == 3 and len(matrices) == 1 and len(sources) == 2,
            f"{topic_id} must contain one matrix and two independent sources",
        )
        matrix = matrices[0]
        source_ids = {row["record_id"] for row in sources}
        topic_record_ids[topic_id] = source_ids | {matrix["record_id"]}
        _require(
            set(matrix.get("synthesis_evidence_ids", [])) == source_ids,
            f"{topic_id} synthesis must reference exactly its two independent sources",
        )
        for source in sources:
            url = source.get("source_url")
            _require(
                isinstance(url, str) and url.startswith("https://"),
                f"{topic_id} source URL invalid",
            )
            source_urls.append(url)
            _strings(
                source.get("abstracted_dimensions"),
                f"{source['record_id']}.abstracted_dimensions",
                minimum=2,
            )
            _strings(
                source.get("limitations"),
                f"{source['record_id']}.limitations",
                minimum=2,
            )
            _require(
                source.get("supported_candidate_ids") == [],
                f"{source['record_id']} must not overclaim direct runtime-candidate support",
            )

        mechanisms = matrix.get("mechanisms")
        provenance = matrix.get("mechanism_provenance")
        _require(
            isinstance(mechanisms, list) and mechanisms,
            f"{topic_id} mechanisms missing",
        )
        _require(
            isinstance(provenance, list) and len(provenance) == len(mechanisms),
            f"{topic_id} mechanism provenance mismatch",
        )
        local_mechanism_ids: list[str] = []
        for mechanism in mechanisms:
            _require(
                isinstance(mechanism, dict)
                and set(mechanism) == {"id", "statement"}
                and isinstance(mechanism.get("id"), str)
                and isinstance(mechanism.get("statement"), str)
                and mechanism["statement"].strip(),
                f"{topic_id} mechanism shape mismatch",
            )
            local_mechanism_ids.append(mechanism["id"])
        _require(
            local_mechanism_ids == [item.get("mechanism_id") for item in provenance],
            f"{topic_id} mechanism/provenance order mismatch",
        )
        for item in provenance:
            _require(
                isinstance(item, dict)
                and set(item) == {"mechanism_id", "provenance", "evidence_ids"},
                f"{topic_id} mechanism provenance shape mismatch",
            )
            kind = item.get("provenance")
            _require(
                kind in PROVENANCE_VALUES, f"{topic_id} invalid mechanism provenance"
            )
            refs = _strings(
                item.get("evidence_ids"),
                f"{item['mechanism_id']}.evidence_ids",
                minimum=1,
            )
            _require(
                set(refs) <= all_record_ids,
                f"{item['mechanism_id']} has unknown evidence",
            )
            _require(
                set(refs) <= source_ids,
                f"{item['mechanism_id']} has cross-topic or matrix evidence",
            )
            if kind == "cross_source_synthesis":
                _require(
                    set(refs) == source_ids,
                    f"{item['mechanism_id']} lacks both sources",
                )
            if kind == "source_supported":
                _require(
                    len(refs) == 1,
                    f"{item['mechanism_id']} source support must be singular",
                )
            provenance_counts[kind] += 1
        mechanism_ids.extend(local_mechanism_ids)

        local_candidate_ids = _strings(
            matrix.get("candidate_ids"), f"{topic_id}.candidate_ids", minimum=1
        )
        definitions = matrix.get("candidate_definitions")
        roles = matrix.get("candidate_roles")
        _require(
            isinstance(definitions, dict)
            and set(definitions) == set(local_candidate_ids),
            f"{topic_id} candidate definitions mismatch",
        )
        _require(
            isinstance(roles, dict) and set(roles) == set(local_candidate_ids),
            f"{topic_id} candidate roles mismatch",
        )
        _require(
            set(roles.values()) <= UNIVERSAL_CANDIDATE_ROLE_VALUES,
            f"{topic_id} candidate role is outside the closed enum",
        )
        local_pixel_ids = _strings(
            matrix.get("pixel_evidence_ids"),
            f"{topic_id}.pixel_evidence_ids",
            minimum=0,
        )
        pixel_definitions = matrix.get("pixel_evidence_definitions")
        _require(
            isinstance(pixel_definitions, dict)
            and set(pixel_definitions) == set(local_pixel_ids),
            f"{topic_id} pixel evidence definitions mismatch",
        )
        _require(
            set(local_pixel_ids) <= set(local_candidate_ids)
            and all(roles[value] == "visual_atom" for value in local_pixel_ids),
            f"{topic_id} pixel evidence must be a visual-candidate subset",
        )
        for field, minimum in {
            "research_questions": 3,
            "compatibility": 4,
            "conflicts": 4,
            "counterexamples": 4,
            "boundaries": 4,
            "domain_limits": 3,
            "embodiment_limits": 3,
            "cultural_limits": 3,
            "source_biases": 3,
            "runtime_implications": 4,
            "evaluation_implications": 4,
        }.items():
            _strings(matrix.get(field), f"{topic_id}.{field}", minimum=minimum)
        for candidate_id in local_candidate_ids:
            definition = definitions[candidate_id]
            _require(
                isinstance(definition, str) and definition.strip(),
                f"{candidate_id} definition missing",
            )
            role_counts[roles[candidate_id]] += 1
            candidate_specs[candidate_id] = {
                "definition": definition,
                "role": roles[candidate_id],
                "topic_id": topic_id,
                "matrix_id": matrix["record_id"],
                "record_ids": topic_record_ids[topic_id],
                "has_pixel_evidence": candidate_id in set(local_pixel_ids),
            }
        candidate_ids.extend(local_candidate_ids)
        pixel_evidence_ids.extend(local_pixel_ids)

    _require(
        len(source_urls) == len(set(source_urls)) == 40,
        "universal research source URLs must be 40/40 unique",
    )
    _require(
        len(mechanism_ids) == len(set(mechanism_ids)) == 167,
        "universal research mechanism IDs must be 167 unique values",
    )
    _require(
        len(candidate_ids) == len(set(candidate_ids)) == 220,
        "universal research candidate IDs must be 220 unique values",
    )
    _require(
        len(pixel_evidence_ids) == len(set(pixel_evidence_ids)) == 97,
        "universal research pixel IDs must be 97 unique values",
    )
    _require(
        dict(role_counts)
        == UNIVERSAL_RESEARCH_EXPECTED_TOTALS["candidate_role_counts"],
        "universal research candidate role counts mismatch",
    )
    _require(
        dict(provenance_counts)
        == UNIVERSAL_RESEARCH_EXPECTED_TOTALS["mechanism_provenance_counts"],
        "universal research provenance counts mismatch",
    )
    return {
        "manifest_sha256": _sha256(manifest_path),
        "record_count": len(rows),
        "topic_count": len(by_topic),
        "independent_source_count": len(source_urls),
        "mechanism_count": len(mechanism_ids),
        "candidate_count": len(candidate_ids),
        "pixel_evidence_count": len(pixel_evidence_ids),
        "candidate_role_counts": dict(sorted(role_counts.items())),
        "mechanism_provenance_counts": dict(sorted(provenance_counts.items())),
        "candidate_specs": candidate_specs,
        "record_ids": all_record_ids,
        "topic_ids": set(by_topic),
        "topic_record_ids": topic_record_ids,
        "shards": shard_results,
    }


def _literal_phrases(
    value: Any, request: str, label: str, *, minimum: int = 0
) -> list[str]:
    phrases = _strings(value, label, minimum=minimum)
    normalized_request = unicodedata.normalize("NFKC", request)
    for phrase in phrases:
        _require(
            phrase in request
            and unicodedata.normalize("NFKC", phrase) in normalized_request,
            f"{label} contains a non-literal request phrase: {phrase!r}",
        )
    return phrases


def _universal_v2_projection_target(
    target_kind: str,
    target_id: str,
    target_values: list[str],
) -> list[dict[str, Any]]:
    return [
        {
            "target_kind": target_kind,
            "target_ids": [target_id],
            "target_values": list(target_values),
            "quantifier": "all",
            "enforcement": "canonical_projection",
        }
    ]


def _universal_v2_absence_target(
    target_kind: str,
    target_ids: list[str],
    *,
    target_values: list[str] | None = None,
) -> list[dict[str, Any]]:
    return [
        {
            "target_kind": target_kind,
            "target_ids": list(target_ids),
            "target_values": list(target_values or []),
            "quantifier": "all",
            "enforcement": "absent",
        }
    ]


def _universal_v2_contract_revision(case_id: str) -> dict[str, Any]:
    reason_id = (
        "literal_binding_schema_migration_and_resource_scope_and_custom_embodiment_scope_correction"
        if case_id == "universal_scene_12_nonhuman_display"
        else "literal_binding_schema_migration_and_custom_embodiment_scope_correction"
        if case_id in UNIVERSAL_V2_CUSTOM_EMBODIMENT_CORRECTIONS
        else {
            "universal_scene_15_action_phase": (
                "literal_binding_schema_migration_and_context_scope_correction"
            ),
            "universal_scene_16_contact_resource": (
                "literal_binding_schema_migration_and_embodiment_profile_scope_correction"
            ),
            "universal_scene_18_prop_lexical_normalization": (
                "literal_binding_schema_migration_and_context_scope_correction"
            ),
            "universal_scene_24_closed_no_prop_consequence": (
                "literal_binding_schema_migration_and_display_channel_scope_correction"
            ),
        }.get(case_id, "literal_binding_schema_migration")
    )
    return {**UNIVERSAL_V2_CONTRACT_REVISION_BASE, "reason_id": reason_id}


def _universal_v2_value_phrase_bindings(
    case_id: str,
    slot: Mapping[str, Any],
) -> tuple[list[str], list[dict[str, Any]]]:
    """Return the reviewed exact phrase partition for one current slot."""

    state = slot.get("state")
    value_ids = list(slot.get("value_ids", []))
    request_phrases = list(slot.get("request_phrases", []))
    if state != "fixed":
        return request_phrases, []
    reviewed = UNIVERSAL_V2_MULTI_VALUE_PHRASE_BINDINGS.get(
        (case_id, str(slot.get("slot_id")))
    )
    if reviewed is None:
        _require(
            len(value_ids) == 1,
            f"universal v2 fixed multi-value slot lacks reviewed bindings: {case_id}",
        )
        reviewed = [(value_ids[0], request_phrases)]
    if (case_id, slot.get("slot_id")) == (
        "universal_scene_17_relation_topology",
        "relation",
    ):
        request_phrases = [
            "성인 세 명의 폭풍 관측팀",
            "관계 중심 키 아트",
            "같은 목표를 보며",
        ]
    bindings = [
        {
            "value_id": value_id,
            "request_phrases": list(phrases),
            "semantic_anchor_groups": _universal_v2_semantic_anchor_groups(
                case_id=case_id,
                source_kind="slot",
                source_id=str(slot.get("slot_id")),
                value_id=value_id,
                request_phrases=phrases,
            ),
        }
        for value_id, phrases in reviewed
    ]
    _require(
        [binding["value_id"] for binding in bindings] == value_ids,
        f"universal v2 value binding order drift: {case_id}/{slot.get('slot_id')}",
    )
    flattened = [
        phrase for binding in bindings for phrase in binding["request_phrases"]
    ]
    _require(
        flattened == request_phrases
        and all(binding["request_phrases"] for binding in bindings)
        and len(flattened) == len(set(flattened)),
        f"universal v2 value binding phrase partition drift: {case_id}/{slot.get('slot_id')}",
    )
    return request_phrases, bindings


def _universal_v2_semantic_anchor_groups(
    *,
    case_id: str,
    source_kind: str,
    source_id: str,
    value_id: str,
    request_phrases: Sequence[str],
) -> list[dict[str, Any]]:
    """Return the reviewed directional literal anchors for one fixed value."""

    reviewed = UNIVERSAL_V2_SEMANTIC_ANCHOR_EXCEPTIONS.get(
        (case_id, source_kind, source_id, value_id)
    )
    if reviewed is None:
        reviewed = [(str(phrase), "affirmative") for phrase in request_phrases]
    groups = [
        {
            "alternatives": [alternative],
            "required_polarity": required_polarity,
        }
        for alternative, required_polarity in reviewed
    ]
    _require(
        groups
        and all(
            group["required_polarity"] in {"affirmative", "negated"}
            and group["alternatives"]
            and all(
                any(alternative in phrase for phrase in request_phrases)
                for alternative in group["alternatives"]
            )
            for group in groups
        ),
        f"universal v2 semantic anchors are not literal-bound: {case_id}/{source_kind}/{source_id}",
    )
    return groups


def _universal_v2_participant_bindings(
    case_id: str,
    entities: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Build the reviewed identity-entity projection for the eight event roles."""

    entity_ids = [str(entity["entity_id"]) for entity in entities]
    actor_ids = (
        ["actor_01", "actor_02"]
        if case_id
        in {
            "universal_scene_09_shared_attention",
            "universal_scene_21_prop_narrative_role",
        }
        else ["team_01"]
        if case_id == "universal_scene_17_relation_topology"
        else ["actor_01"]
    )
    fixed_recipient_cases = {
        "universal_scene_04_explicit_apple",
        "universal_scene_08_ambiguous_display_affect",
        "universal_scene_11_gesture_function",
        "universal_scene_12_nonhuman_display",
        "universal_scene_14_event_roles",
        "universal_scene_24_closed_no_prop_consequence",
    }
    recipient_ids = ["recipient_01"] if case_id in fixed_recipient_cases else []
    _require(
        set(actor_ids + recipient_ids) <= set(entity_ids),
        f"universal v2 participant source entity drift: {case_id}",
    )
    by_role = {
        "actor": actor_ids,
        "recipient": recipient_ids,
    }
    return [
        {
            "role_id": role_id,
            "entity_ids": list(by_role.get(role_id, [])),
            "primary_entity_id": (
                by_role[role_id][0] if by_role.get(role_id) else None
            ),
        }
        for role_id in UNIVERSAL_EVENT_ROLE_IDS
    ]


def _build_universal_v2_scene_contract(
    case_id: str,
    historical_contract: Mapping[str, Any],
) -> dict[str, Any]:
    """Migrate the immutable v1 literal contract without consulting runtime output."""

    contract = copy.deepcopy(dict(historical_contract))
    contract["schema"] = UNIVERSAL_V2_SCENE_CONTRACT_SCHEMA
    custom_correction = UNIVERSAL_V2_CUSTOM_EMBODIMENT_CORRECTIONS.get(case_id)
    if custom_correction is not None:
        entity_index, entity_id, historical_profile_id, current_profile_id = (
            custom_correction
        )
        entity = contract["identity_core"]["entities"][entity_index]
        _require(
            entity["entity_id"] == entity_id
            and entity["embodiment_profile_id"] == historical_profile_id,
            f"universal v2 custom embodiment source drift: {case_id}",
        )
        entity["embodiment_profile_id"] = current_profile_id
    if case_id == "universal_scene_16_contact_resource":
        entity = contract["identity_core"]["entities"][0]
        entity["embodiment_profile_id"] = UNIVERSAL_V2_C16_EMBODIMENT_PROFILE_ID
        entity["capabilities"] = [
            {
                "id": resource_kind,
                "capacity": capacity,
                "state": "unavailable" if capacity == 0 else "available",
                "source": "embodiment_profile",
                "source_fact_id": UNIVERSAL_V2_C16_EMBODIMENT_PROFILE_ID,
            }
            for resource_kind, capacity in UNIVERSAL_V2_C16_PROFILE_CAPACITIES
        ]
    migrated_entities: list[dict[str, Any]] = []
    for raw_entity in contract["identity_core"]["entities"]:
        entity = copy.deepcopy(raw_entity)
        migrated_entities.append(
            {
                "entity_id": entity["entity_id"],
                "quantity": entity["quantity"],
                "embodiment_profile_id": entity["embodiment_profile_id"],
                "capability_projection_mode": (
                    "catalog_exact"
                    if case_id == "universal_scene_16_contact_resource"
                    and entity["entity_id"] == "actor_01"
                    else "declared_subset"
                ),
                "feature_facts": entity["feature_facts"],
                "capabilities": entity["capabilities"],
            }
        )
    contract["identity_core"]["entities"] = migrated_entities
    migrated_slots: list[dict[str, Any]] = []
    for historical_slot in contract["slot_states"]:
        slot = copy.deepcopy(historical_slot)
        if (
            case_id == "universal_scene_12_nonhuman_display"
            and slot["slot_id"] == "prop"
        ):
            slot["state"] = "open"
            slot["value_ids"] = []
            slot["request_phrases"] = []
        if (
            case_id == "universal_scene_24_closed_no_prop_consequence"
            and slot["slot_id"] == "expression"
        ):
            slot["state"] = "fixed"
            slot["value_ids"] = ["body_direction_and_light_intensity_display"]
            slot["request_phrases"] = ["몸의 방향, 빛의 세기"]
        request_phrases, bindings = _universal_v2_value_phrase_bindings(case_id, slot)
        slot["request_phrases"] = request_phrases
        slot["value_phrase_bindings"] = bindings
        migrated_slots.append(slot)
    contract["slot_states"] = migrated_slots
    if case_id == "universal_scene_12_nonhuman_display":
        for role in contract["event_roles"]:
            if role["role_id"] == "instrument":
                role["state"] = "open"
                role["value_id"] = None
                role["request_phrases"] = []
    migrated_roles: list[dict[str, Any]] = []
    for raw_role in contract["event_roles"]:
        role = copy.deepcopy(raw_role)
        groups = (
            _universal_v2_semantic_anchor_groups(
                case_id=case_id,
                source_kind="event_role",
                source_id=str(role["role_id"]),
                value_id=str(role["value_id"]),
                request_phrases=role["request_phrases"],
            )
            if role["state"] == "fixed"
            else []
        )
        migrated_roles.append(
            {
                "role_id": role["role_id"],
                "state": role["state"],
                "value_id": role["value_id"],
                "request_phrases": role["request_phrases"],
                "semantic_anchor_groups": groups,
            }
        )
    contract["event_roles"] = migrated_roles
    if case_id in {
        "universal_scene_15_action_phase",
        "universal_scene_18_prop_lexical_normalization",
    }:
        contract["context_profile"]["scale"] = "unknown"
    return {
        "schema": contract["schema"],
        "request_text_sha256": contract["request_text_sha256"],
        "identity_core": contract["identity_core"],
        "participant_bindings": _universal_v2_participant_bindings(
            case_id,
            contract["identity_core"]["entities"],
        ),
        "slot_states": contract["slot_states"],
        "event_roles": contract["event_roles"],
        "context_profile": contract["context_profile"],
    }


def _expected_universal_v2_contract_wrapper(
    *,
    case_id: str,
    record_index: int,
    historical_raw_line: bytes,
    historical_wrapper: Mapping[str, Any],
    historical_path: Path,
) -> dict[str, Any]:
    historical_contract = historical_wrapper["scene_contract"]
    contract = _build_universal_v2_scene_contract(case_id, historical_contract)
    request_sha256 = historical_contract["request_text_sha256"]
    _require(
        contract["request_text_sha256"] == request_sha256,
        f"universal v2 request binding drift: {case_id}",
    )
    return {
        "schema": UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SCHEMA,
        "case_id": case_id,
        "revision": _universal_v2_contract_revision(case_id),
        "source_lineage": {
            "path": historical_path.name,
            "schema": UNIVERSAL_SCENE_CONTRACT_HOLDOUT_SCHEMA,
            "file_sha256": UNIVERSAL_V1_SCENE_CONTRACT_HOLDOUT_SHA256,
            "record_index": record_index + 1,
            "raw_record_sha256": hashlib.sha256(historical_raw_line).hexdigest(),
            "request_text_sha256": request_sha256,
        },
        "scene_contract": contract,
    }


def _universal_v2_ledger_entry(
    *,
    source_id: str = "legacy_prompt_record",
    source_pointer: str,
    legacy_kind: str,
    legacy_label: str,
    legacy_state: str | None,
    legacy_value: str | None,
    disposition: str,
    mapping_id: str | None,
    runtime_authority: bool = True,
    resolution: str | None = None,
    targets: list[dict[str, Any]],
) -> dict[str, Any]:
    if resolution is None:
        resolution = (
            "enforced_reviewed_crosswalk"
            if disposition == "reviewed_crosswalk"
            else "enforced_current_projection"
        )
    return {
        "source_id": source_id,
        "source_pointer": source_pointer,
        "legacy_kind": legacy_kind,
        "legacy_label": legacy_label,
        "legacy_state": legacy_state,
        "legacy_value": legacy_value,
        "disposition": disposition,
        "mapping_id": mapping_id,
        "runtime_authority": runtime_authority,
        "resolution": resolution,
        "targets": copy.deepcopy(targets),
    }


def _compile_universal_v2_obligations(
    ledger: list[dict[str, Any]],
    guard_source_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    obligations_by_target: dict[bytes, dict[str, Any]] = {}
    obligations: list[dict[str, Any]] = []
    for ledger_index, entry in enumerate(ledger):
        if entry.get("runtime_authority") is False:
            continue
        targets = entry.get("targets")
        _require(
            isinstance(targets, list), "universal v2 ledger targets must be a list"
        )
        for target_index, target in enumerate(targets):
            _require(
                isinstance(target, dict)
                and list(target)
                == [
                    "target_kind",
                    "target_ids",
                    "target_values",
                    "quantifier",
                    "enforcement",
                ],
                "universal v2 compiler target shape mismatch",
            )
            target_bytes = canonical_json_bytes(target)
            obligation = obligations_by_target.get(target_bytes)
            if obligation is None:
                evaluator_id = UNIVERSAL_V2_EVALUATOR_IDS.get(
                    (target["target_kind"], target["enforcement"])
                )
                _require(
                    evaluator_id is not None,
                    "universal v2 target has no closed evaluator binding",
                )
                obligation = {
                    "obligation_id": "uo2_" + hashlib.sha256(target_bytes).hexdigest(),
                    "target_kind": target["target_kind"],
                    "target_ids": copy.deepcopy(target["target_ids"]),
                    "target_values": copy.deepcopy(target["target_values"]),
                    "quantifier": target["quantifier"],
                    "enforcement": target["enforcement"],
                    "evaluator_id": evaluator_id,
                    "source_refs": [],
                }
                obligations_by_target[target_bytes] = obligation
                obligations.append(obligation)
            obligation["source_refs"].append(
                {
                    "ledger_entry_index": ledger_index,
                    "target_index": target_index,
                    "source_pointer": entry["source_pointer"],
                    "mapping_id": entry["mapping_id"],
                }
            )
    referenced_guard_ids = sorted(
        {
            target_id
            for obligation in obligations
            if obligation["target_kind"] == "guard_contract"
            for target_id in obligation["target_ids"]
        }
    )
    _require(
        set(referenced_guard_ids) <= set(guard_source_by_id),
        "universal v2 compiled guard target lacks a reviewed source contract",
    )
    return {
        "schema": UNIVERSAL_V2_COMPILED_OBLIGATION_SCHEMA,
        "derivation": "resolution_ledger_targets_first_occurrence_dedup_v1",
        "obligations": obligations,
        "guard_source_contracts": [
            copy.deepcopy(guard_source_by_id[guard_id])
            for guard_id in referenced_guard_ids
        ],
    }


def _validate_universal_v2_mapping_target(
    target: Any,
    *,
    canonical_domains: Mapping[str, Any],
    label: str,
) -> None:
    _require(
        isinstance(target, dict)
        and list(target)
        == [
            "target_kind",
            "target_ids",
            "target_values",
            "quantifier",
            "enforcement",
        ],
        f"{label} target shape mismatch",
    )
    kind = target.get("target_kind")
    _require(kind in UNIVERSAL_V2_TARGET_KIND_IDS, f"{label} target kind is not closed")
    domain_field = {
        "slot": "slot_ids",
        "event_role": "event_role_ids",
        "atom_facet": "atom_facets",
        "visual_candidate": "visual_candidate_ids",
        "resource_kind": "resource_kinds",
        "runtime_bridge_type": "runtime_bridge_type_ids",
        "pixel_evidence_kind": "pixel_evidence_kinds",
        "guard_contract": "guard_contract_ids",
        "blocked_semantic": "blocked_semantic_ids",
        "context_profile_field": "context_profile_field_ids",
        "semantic_load_axis": "semantic_load_axis_ids",
    }.get(kind)
    target_ids = _strings(target.get("target_ids"), f"{label}.target_ids", minimum=1)
    if domain_field is not None:
        _require(
            set(target_ids) <= set(canonical_domains[domain_field]),
            f"{label} target IDs escape the canonical domain",
        )
    target_values = target.get("target_values")
    _require(
        isinstance(target_values, list)
        and all(isinstance(value, str) and value for value in target_values),
        f"{label} target values invalid",
    )
    _require(target.get("quantifier") in {"any", "all"}, f"{label} quantifier invalid")
    _require(
        target.get("enforcement")
        in {"canonical_projection", "eligible", "absent", "required"},
        f"{label} enforcement invalid",
    )


def validate_universal_scene_current_oracle_v2(asset_dir: Path) -> dict[str, Any]:
    """Validate the post-contract oracle without consulting production output."""

    prompt_path = asset_dir / "universal_scene_prompt_holdout_v1.jsonl"
    historical_contract_path = asset_dir / "universal_scene_contract_holdout_v1.jsonl"
    current_contract_path = asset_dir / "universal_scene_contract_holdout_v2.jsonl"
    current_path = asset_dir / "universal_scene_current_holdout_v2.jsonl"
    crosswalk_path = asset_dir / "universal_scene_expectation_crosswalk_v2.json"
    manifest_path = asset_dir / "universal_scene_current_holdout_v2_manifest.json"
    baseline_v1_path = asset_dir / "universal_scene_baseline_v1.json"
    baseline_v2_path = asset_dir / "universal_scene_baseline_v2.json"
    validator_path = Path(__file__).resolve()

    frozen_hashes = {
        prompt_path: UNIVERSAL_V1_PROMPT_HOLDOUT_SHA256,
        historical_contract_path: UNIVERSAL_V1_SCENE_CONTRACT_HOLDOUT_SHA256,
        current_contract_path: UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SHA256,
        current_path: UNIVERSAL_V2_CURRENT_HOLDOUT_SHA256,
        crosswalk_path: UNIVERSAL_V2_EXPECTATION_CROSSWALK_SHA256,
        manifest_path: UNIVERSAL_V2_CURRENT_MANIFEST_SHA256,
        baseline_v1_path: UNIVERSAL_V1_BASELINE_SHA256,
    }
    for path, expected_digest in frozen_hashes.items():
        _require(path.is_file(), f"universal v2 oracle path missing: {path.name}")
        _require(
            _sha256(path) == expected_digest,
            f"universal v2 oracle frozen hash mismatch: {path.name}",
        )

    prompt_raw_lines = prompt_path.read_bytes().splitlines()
    historical_contract_raw_lines = historical_contract_path.read_bytes().splitlines()
    current_contract_raw_lines = current_contract_path.read_bytes().splitlines()
    prompt_rows = [json.loads(line) for line in prompt_raw_lines]
    historical_contract_wrappers = [
        json.loads(line) for line in historical_contract_raw_lines
    ]
    current_contract_wrappers = [
        json.loads(line) for line in current_contract_raw_lines
    ]
    _require(
        len(prompt_rows)
        == len(historical_contract_wrappers)
        == len(current_contract_wrappers)
        == 24,
        "universal v2 oracle source lineage must contain 24 tripled rows",
    )
    prompt_by_case = {
        row.get("case_id"): (index, row) for index, row in enumerate(prompt_rows)
    }
    historical_contract_by_case = {
        row.get("case_id"): (index, row)
        for index, row in enumerate(historical_contract_wrappers)
    }
    current_contract_by_case = {
        row.get("case_id"): (index, row)
        for index, row in enumerate(current_contract_wrappers)
    }
    _require(
        len(prompt_by_case)
        == len(historical_contract_by_case)
        == len(current_contract_by_case)
        == 24
        and set(prompt_by_case)
        == set(historical_contract_by_case)
        == set(current_contract_by_case),
        "universal v2 oracle source case coverage mismatch",
    )
    contract_v2_schema_migration_count = 0
    contract_v2_semantic_correction_count = 0
    contract_v2_phrase_order_normalization_count = 0
    for contract_index, wrapper in enumerate(current_contract_wrappers):
        case_id = wrapper.get("case_id")
        historical_index, historical_wrapper = historical_contract_by_case[case_id]
        _require(
            historical_index == contract_index,
            f"universal v2 contract source order drift: {case_id}",
        )
        expected_wrapper = _expected_universal_v2_contract_wrapper(
            case_id=case_id,
            record_index=historical_index,
            historical_raw_line=historical_contract_raw_lines[historical_index],
            historical_wrapper=historical_wrapper,
            historical_path=historical_contract_path,
        )
        _require(
            wrapper == expected_wrapper,
            f"universal v2 current scene-contract migration drift: {case_id}",
        )
        reason_id = wrapper["revision"]["reason_id"]
        if reason_id.startswith("literal_binding_schema_migration"):
            contract_v2_schema_migration_count += 1
        if reason_id != "literal_binding_schema_migration":
            contract_v2_semantic_correction_count += 1
        historical_slots = historical_wrapper["scene_contract"]["slot_states"]
        current_slots = wrapper["scene_contract"]["slot_states"]
        for historical_slot, current_slot in zip(historical_slots, current_slots):
            if (
                historical_slot["slot_id"] == current_slot["slot_id"]
                and historical_slot["state"] == current_slot["state"]
                and historical_slot["value_ids"] == current_slot["value_ids"]
                and historical_slot["request_phrases"]
                != current_slot["request_phrases"]
                and sorted(historical_slot["request_phrases"])
                == sorted(current_slot["request_phrases"])
            ):
                contract_v2_phrase_order_normalization_count += 1
        request_text = prompt_by_case[case_id][1]["request_ko"]
        _require(
            hashlib.sha256(request_text.encode("utf-8")).hexdigest()
            == wrapper["scene_contract"]["request_text_sha256"],
            f"universal v2 current contract request hash drift: {case_id}",
        )
        scene_contract = wrapper["scene_contract"]
        _require(
            list(scene_contract)
            == [
                "schema",
                "request_text_sha256",
                "identity_core",
                "participant_bindings",
                "slot_states",
                "event_roles",
                "context_profile",
            ],
            f"universal v2 current contract top-level order drift: {case_id}",
        )
        entities = scene_contract["identity_core"]["entities"]
        for entity in entities:
            _require(
                list(entity)
                == [
                    "entity_id",
                    "quantity",
                    "embodiment_profile_id",
                    "capability_projection_mode",
                    "feature_facts",
                    "capabilities",
                ]
                and entity["capability_projection_mode"]
                in {"declared_subset", "catalog_exact"},
                f"universal v2 entity projection shape drift: {case_id}",
            )
            if str(entity["embodiment_profile_id"]).startswith("custom_"):
                _require(
                    entity["capability_projection_mode"] == "declared_subset",
                    f"universal v2 custom entity cannot claim catalog_exact: {case_id}",
                )
        exact_entities = [
            entity
            for entity in entities
            if entity["capability_projection_mode"] == "catalog_exact"
        ]
        if case_id == "universal_scene_16_contact_resource":
            _require(
                len(exact_entities) == 1
                and exact_entities[0]["entity_id"] == "actor_01"
                and exact_entities[0]["embodiment_profile_id"]
                == UNIVERSAL_V2_C16_EMBODIMENT_PROFILE_ID
                and [
                    (item["id"], item["capacity"])
                    for item in exact_entities[0]["capabilities"]
                ]
                == UNIVERSAL_V2_C16_PROFILE_CAPACITIES
                and all(
                    item["state"]
                    == ("unavailable" if item["capacity"] == 0 else "available")
                    and item["source"] == "embodiment_profile"
                    and item["source_fact_id"] == UNIVERSAL_V2_C16_EMBODIMENT_PROFILE_ID
                    for item in exact_entities[0]["capabilities"]
                ),
                "universal v2 catalog_exact embodiment projection drift: case16",
            )
        else:
            _require(
                exact_entities == [],
                f"universal v2 unexpected catalog_exact entity: {case_id}",
            )

        participant_bindings = scene_contract["participant_bindings"]
        expected_participants = _universal_v2_participant_bindings(case_id, entities)
        _require(
            participant_bindings == expected_participants
            and all(
                list(binding) == ["role_id", "entity_ids", "primary_entity_id"]
                and binding["entity_ids"] == sorted(set(binding["entity_ids"]))
                and (
                    (not binding["entity_ids"] and binding["primary_entity_id"] is None)
                    or binding["primary_entity_id"] in binding["entity_ids"]
                )
                for binding in participant_bindings
            ),
            f"universal v2 participant projection drift: {case_id}",
        )
        role_state_by_id = {
            role["role_id"]: role["state"] for role in scene_contract["event_roles"]
        }
        _require(
            all(
                not binding["entity_ids"]
                for binding in participant_bindings
                if role_state_by_id[binding["role_id"]] == "closed"
            ),
            f"universal v2 closed role has identity participants: {case_id}",
        )

        for slot in scene_contract["slot_states"]:
            _require(
                list(slot)
                == [
                    "slot_id",
                    "state",
                    "value_ids",
                    "request_phrases",
                    "value_phrase_bindings",
                ],
                f"universal v2 current slot shape drift: {case_id}",
            )
            phrases = slot["request_phrases"]
            bindings = slot["value_phrase_bindings"]
            if slot["state"] == "fixed":
                _require(
                    [binding["value_id"] for binding in bindings] == slot["value_ids"]
                    and all(
                        list(binding)
                        == [
                            "value_id",
                            "request_phrases",
                            "semantic_anchor_groups",
                        ]
                        and binding["request_phrases"]
                        and binding["semantic_anchor_groups"]
                        and all(
                            list(group) == ["alternatives", "required_polarity"]
                            and group["required_polarity"] in {"affirmative", "negated"}
                            and isinstance(group["alternatives"], list)
                            and group["alternatives"]
                            and all(
                                isinstance(alternative, str)
                                and alternative
                                and any(
                                    alternative in phrase
                                    for phrase in binding["request_phrases"]
                                )
                                for alternative in group["alternatives"]
                            )
                            for group in binding["semantic_anchor_groups"]
                        )
                        for binding in bindings
                    )
                    and [
                        phrase
                        for binding in bindings
                        for phrase in binding["request_phrases"]
                    ]
                    == phrases
                    and len(phrases) == len(set(phrases)),
                    f"universal v2 current fixed-slot phrase partition drift: {case_id}",
                )
            else:
                _require(
                    bindings == [],
                    f"universal v2 open/closed slot has value bindings: {case_id}",
                )
            _literal_phrases(
                phrases,
                request_text,
                f"universal v2 slot phrases {case_id}/{slot['slot_id']}",
            )
        for role in scene_contract["event_roles"]:
            _require(
                list(role)
                == [
                    "role_id",
                    "state",
                    "value_id",
                    "request_phrases",
                    "semantic_anchor_groups",
                ],
                f"universal v2 current event-role shape drift: {case_id}",
            )
            groups = role["semantic_anchor_groups"]
            if role["state"] == "fixed":
                _require(
                    groups
                    and all(
                        list(group) == ["alternatives", "required_polarity"]
                        and group["required_polarity"] in {"affirmative", "negated"}
                        and isinstance(group["alternatives"], list)
                        and group["alternatives"]
                        and all(
                            isinstance(alternative, str)
                            and alternative
                            and any(
                                alternative in phrase
                                for phrase in role["request_phrases"]
                            )
                            for alternative in group["alternatives"]
                        )
                        for group in groups
                    ),
                    f"universal v2 fixed role semantic anchors drift: {case_id}/{role['role_id']}",
                )
            else:
                _require(
                    groups == [],
                    f"universal v2 non-fixed role has semantic anchors: {case_id}/{role['role_id']}",
                )
    _require(
        (
            contract_v2_schema_migration_count,
            contract_v2_semantic_correction_count,
            contract_v2_phrase_order_normalization_count,
        )
        == (24, 9, 1),
        "universal v2 derived migration/correction counts drift",
    )
    production_paths = [
        validator_path.with_name("illustration_runtime.py"),
        validator_path.with_name("universal_scene_runtime.py"),
        asset_dir / "illustration_universal_scene_candidates_v1.json",
        asset_dir / "illustration_universal_compatibility_graph_v1.json",
        asset_dir / "illustration_universal_semantic_bindings_v1.json",
    ]
    forbidden_holdout_markers = {
        prompt_path.name,
        historical_contract_path.name,
        current_contract_path.name,
        current_path.name,
        "universal_scene_expectation_crosswalk_v2.json",
    }
    frozen_case_ids = {str(row["case_id"]) for row in prompt_rows}
    frozen_request_texts = {str(row["request_ko"]) for row in prompt_rows}
    for production_path in production_paths:
        if not production_path.is_file():
            continue
        production_text = production_path.read_text(encoding="utf-8")
        _require(
            not any(marker in production_text for marker in forbidden_holdout_markers),
            f"production runtime/asset loads a current-oracle source: {production_path.name}",
        )
        _require(
            not any(case_id in production_text for case_id in frozen_case_ids),
            f"production runtime/asset branches on a frozen case ID: {production_path.name}",
        )
        _require(
            not any(request in production_text for request in frozen_request_texts),
            f"production runtime/asset embeds a frozen request: {production_path.name}",
        )

    crosswalk = _load_json(crosswalk_path)
    _require(
        isinstance(crosswalk, dict)
        and list(crosswalk)
        == [
            "schema",
            "canonical_domains",
            "band_policy",
            "guard_source_contracts",
            "legacy_event_label_mappings",
            "legacy_bridge_label_mappings",
            "invariants",
        ]
        and crosswalk.get("schema") == UNIVERSAL_V2_EXPECTATION_CROSSWALK_SCHEMA,
        "universal v2 crosswalk top-level contract mismatch",
    )
    canonical_domains = crosswalk.get("canonical_domains")
    _require(
        isinstance(canonical_domains, dict)
        and list(canonical_domains)
        == [
            "target_kind_ids",
            "slot_ids",
            "event_role_ids",
            "atom_facets",
            "visual_candidate_ids",
            "resource_kinds",
            "runtime_bridge_type_ids",
            "pixel_evidence_kinds",
            "guard_contract_ids",
            "blocked_semantic_ids",
            "context_profile_field_ids",
            "semantic_load_axis_ids",
        ],
        "universal v2 crosswalk canonical domains mismatch",
    )
    _require(
        canonical_domains.get("target_kind_ids") == UNIVERSAL_V2_TARGET_KIND_IDS
        and canonical_domains.get("slot_ids") == UNIVERSAL_SLOT_IDS
        and canonical_domains.get("event_role_ids") == UNIVERSAL_EVENT_ROLE_IDS
        and canonical_domains.get("atom_facets") == UNIVERSAL_V2_ATOM_FACETS
        and canonical_domains.get("visual_candidate_ids")
        == UNIVERSAL_V2_VISUAL_CANDIDATE_IDS
        and canonical_domains.get("resource_kinds") == UNIVERSAL_V2_RESOURCE_KINDS
        and canonical_domains.get("runtime_bridge_type_ids")
        == UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS
        and canonical_domains.get("pixel_evidence_kinds")
        == UNIVERSAL_V2_PIXEL_EVIDENCE_KINDS
        and canonical_domains.get("blocked_semantic_ids")
        == UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS
        and canonical_domains.get("context_profile_field_ids")
        == UNIVERSAL_V2_CONTEXT_PROFILE_FIELD_IDS
        and canonical_domains.get("semantic_load_axis_ids")
        == UNIVERSAL_V2_SEMANTIC_LOAD_AXIS_IDS,
        "universal v2 crosswalk canonical domain values drift",
    )
    guard_ids = _strings(
        canonical_domains.get("guard_contract_ids"),
        "universal v2 guard domain",
        minimum=32,
    )
    _require(
        len(guard_ids) == len(set(guard_ids)) == 32,
        "universal v2 guard domain must contain 32 unique IDs",
    )

    expected_band_policy = {
        "creativity_bands": [
            {
                "band": "near",
                "lower": 0,
                "lower_inclusive": True,
                "upper": 0.25,
                "upper_inclusive": False,
                "target_band": "near",
            },
            {
                "band": "middle",
                "lower": 0.25,
                "lower_inclusive": True,
                "upper": 0.75,
                "upper_inclusive": False,
                "target_band": "middle",
            },
            {
                "band": "far",
                "lower": 0.75,
                "lower_inclusive": True,
                "upper": 1,
                "upper_inclusive": True,
                "target_band": "far",
            },
        ],
        "global_max_optional_remote": 1,
        "category_members": {
            "entry": ["affordance", "motivation", "identity_contrast"],
            "mediation": ["mechanics", "ownership"],
            "exit": ["state_change", "consequence"],
        },
        "band_requirements": {
            "near": {
                "minimum_distinct_type_count": 1,
                "required_category_ids": ["entry"],
                "direct_event_edge_required": True,
                "visible_core_identity_anchor_required": False,
            },
            "middle": {
                "minimum_distinct_type_count": 2,
                "required_category_ids": ["entry", "exit"],
                "direct_event_edge_required": True,
                "visible_core_identity_anchor_required": False,
            },
            "far": {
                "minimum_distinct_type_count": 3,
                "required_category_ids": ["entry", "mediation", "exit"],
                "direct_event_edge_required": True,
                "visible_core_identity_anchor_required": True,
            },
        },
        "bridge_requires_pixel_evidence": True,
        "explanation_only_bridge": "block",
    }
    _require(
        crosswalk.get("band_policy") == expected_band_policy,
        "universal v2 crosswalk band policy drift",
    )
    expected_crosswalk_invariants = [
        "Legacy labels are preserved verbatim and every observed occurrence resolves through exactly one reviewed mapping.",
        "Runtime bridge targets use only the closed seven-type enum; band category and minimum requirements are additive.",
        "Mappings are global and contain no case ID, request text, seed, pack ID, selected candidate ID, or runtime output.",
        "Research and evidence obligations do not become literal user-fixed facts unless the canonical scene contract marks them fixed or closed.",
        "Guard targets are required mechanism bindings only and never satisfy material, absence, or semantic outcomes without a non-guard target.",
        "Every target occurrence is compiled source-only into a typed evaluator obligation; production assets are joined only by the separate runtime evaluator.",
        "Creativity bands rank target distance; one optional remote premise is globally eligible and is never rejected solely by creativity.",
    ]
    _require(
        crosswalk.get("invariants") == expected_crosswalk_invariants,
        "universal v2 crosswalk invariants drift",
    )
    serialized_crosswalk = json.dumps(crosswalk, ensure_ascii=False, sort_keys=True)
    _require(
        re.search(r"universal_scene_[0-9]+", serialized_crosswalk) is None,
        "universal v2 crosswalk contains a case-specific label",
    )

    legacy_event_occurrences: list[tuple[str, str]] = []
    legacy_bridge_occurrences: list[str] = []
    cases_with_noncanonical_bridge_labels: set[str] = set()
    closed_bridge_set = set(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS)
    for prompt in prompt_rows:
        frame = prompt["expected_event_frame"]
        for label in frame["fixed_roles"]:
            if label not in UNIVERSAL_EVENT_ROLE_IDS:
                legacy_event_occurrences.append((label, "fixed"))
        for state, field in (("open", "open_roles"), ("closed", "closed_roles")):
            for label in frame[field]:
                if label not in UNIVERSAL_EVENT_ROLE_IDS:
                    legacy_event_occurrences.append((label, state))
        for label in prompt["semantic_distance_expectation"]["required_bridge_types"]:
            legacy_bridge_occurrences.append(label)
            if label not in closed_bridge_set:
                cases_with_noncanonical_bridge_labels.add(prompt["case_id"])

    mapping_keys = [
        "mapping_id",
        "legacy_label",
        "legacy_kind",
        "allowed_legacy_states",
        "targets",
    ]
    guard_source_rows = crosswalk.get("guard_source_contracts")
    _require(
        isinstance(guard_source_rows, list) and len(guard_source_rows) == 9,
        "universal v2 crosswalk guard source inventory mismatch",
    )
    guard_source_keys = [
        "guard_id",
        "role",
        "research_topic_ids",
        "provenance_record_ids",
        "stage",
        "violation_code",
        "outcome",
    ]
    guard_source_ids = [
        row.get("guard_id") for row in guard_source_rows if isinstance(row, dict)
    ]
    _require(
        len(guard_source_ids) == len(guard_source_rows)
        and guard_source_ids == sorted(guard_source_ids)
        and len(set(guard_source_ids)) == 9,
        "universal v2 guard source IDs must be unique and bytewise sorted",
    )
    guard_source_by_id: dict[str, dict[str, Any]] = {}
    for guard_source in guard_source_rows:
        _require(
            isinstance(guard_source, dict) and list(guard_source) == guard_source_keys,
            "universal v2 guard source shape mismatch",
        )
        guard_id = guard_source.get("guard_id")
        _require(
            guard_source.get("role") == "guard"
            and guard_source.get("outcome") == "block"
            and guard_source.get("violation_code") == f"universal_guard::{guard_id}"
            and isinstance(guard_source.get("stage"), str)
            and guard_source["stage"],
            f"universal v2 guard source mechanism contract mismatch: {guard_id}",
        )
        _strings(
            guard_source.get("research_topic_ids"),
            f"universal v2 guard {guard_id} research topics",
            minimum=1,
        )
        _strings(
            guard_source.get("provenance_record_ids"),
            f"universal v2 guard {guard_id} provenance",
            minimum=1,
        )
        guard_source_by_id[str(guard_id)] = guard_source
    event_mapping_rows = crosswalk.get("legacy_event_label_mappings")
    bridge_mapping_rows = crosswalk.get("legacy_bridge_label_mappings")
    _require(
        isinstance(event_mapping_rows, list)
        and isinstance(bridge_mapping_rows, list)
        and len(event_mapping_rows) == 30
        and len(bridge_mapping_rows) == 35,
        "universal v2 crosswalk mapping counts mismatch",
    )
    event_mapping_by_label: dict[str, dict[str, Any]] = {}
    bridge_mapping_by_label: dict[str, dict[str, Any]] = {}
    for mapping_kind, rows, output in (
        ("event_label", event_mapping_rows, event_mapping_by_label),
        ("bridge_label", bridge_mapping_rows, bridge_mapping_by_label),
    ):
        labels = [row.get("legacy_label") for row in rows if isinstance(row, dict)]
        _require(
            len(labels) == len(rows)
            and labels == sorted(labels)
            and len(labels) == len(set(labels)),
            f"universal v2 {mapping_kind} mappings must be unique and bytewise sorted",
        )
        for mapping in rows:
            _require(
                isinstance(mapping, dict) and list(mapping) == mapping_keys,
                f"universal v2 {mapping_kind} mapping shape mismatch",
            )
            legacy_label = mapping.get("legacy_label")
            prefix = (
                "legacy_event" if mapping_kind == "event_label" else "legacy_bridge"
            )
            _require(
                isinstance(legacy_label, str)
                and legacy_label
                and mapping.get("mapping_id") == f"{prefix}.{legacy_label}"
                and mapping.get("legacy_kind") == mapping_kind,
                f"universal v2 {mapping_kind} mapping identity mismatch",
            )
            allowed_states = mapping.get("allowed_legacy_states")
            if mapping_kind == "event_label":
                _require(
                    allowed_states in (["open"], ["closed"]),
                    f"universal v2 event mapping state mismatch: {legacy_label}",
                )
            else:
                _require(
                    allowed_states == [],
                    f"universal v2 bridge mapping cannot declare a role state: {legacy_label}",
                )
            targets = mapping.get("targets")
            _require(
                isinstance(targets, list) and targets,
                f"universal v2 mapping targets missing: {legacy_label}",
            )
            non_guard_targets: list[dict[str, Any]] = []
            for target_index, target in enumerate(targets):
                _validate_universal_v2_mapping_target(
                    target,
                    canonical_domains=canonical_domains,
                    label=f"{mapping['mapping_id']}.targets[{target_index}]",
                )
                reviewed_nonhuman_display_value = (
                    legacy_label == "nonhuman_display_channel"
                    and target.get("target_kind") == "slot"
                    and target.get("target_ids") == ["expression"]
                    and target.get("target_values")
                    == ["body_direction_and_light_intensity_display"]
                    and target.get("enforcement") == "canonical_projection"
                )
                _require(
                    target.get("target_values") == []
                    or reviewed_nonhuman_display_value,
                    f"universal v2 reviewed mapping cannot assert literal values: {legacy_label}",
                )
                target_kind = target.get("target_kind")
                enforcement = target.get("enforcement")
                if target_kind == "guard_contract":
                    _require(
                        enforcement == "required",
                        f"universal v2 guard contract must always remain required: {legacy_label}",
                    )
                else:
                    non_guard_targets.append(target)
                if target_kind in {"blocked_semantic", "semantic_load_axis"}:
                    _require(
                        enforcement == "absent",
                        f"universal v2 blocked/load target must remain absent: {legacy_label}",
                    )
                if target_kind == "context_profile_field":
                    _require(
                        enforcement == "canonical_projection",
                        f"universal v2 context target must remain a canonical projection: {legacy_label}",
                    )
                if mapping_kind == "bridge_label":
                    if target_kind not in {
                        "guard_contract",
                        "context_profile_field",
                        "blocked_semantic",
                        "semantic_load_axis",
                    }:
                        _require(
                            enforcement == "required",
                            f"universal v2 bridge obligation was weakened: {legacy_label}",
                        )
                else:
                    if allowed_states == ["open"] and target_kind != "guard_contract":
                        if legacy_label == "nonhuman_display_channel":
                            _require(
                                (
                                    target_kind == "slot"
                                    and enforcement == "canonical_projection"
                                )
                                or (
                                    target_kind == "resource_kind"
                                    and enforcement == "eligible"
                                )
                                or (
                                    target_kind == "pixel_evidence_kind"
                                    and enforcement == "required"
                                ),
                                "universal v2 nonhuman display mapping enforcement drift",
                            )
                        else:
                            _require(
                                enforcement == "eligible",
                                f"universal v2 open-event mapping enforcement mismatch: {legacy_label}",
                            )
                    elif allowed_states == ["closed"] and target_kind not in {
                        "guard_contract",
                        "blocked_semantic",
                        "semantic_load_axis",
                    }:
                        if enforcement == "canonical_projection":
                            _require(
                                target_kind in {"slot", "event_role"},
                                f"universal v2 closed canonical auxiliary is not a slot/role: {legacy_label}",
                            )
                        else:
                            _require(
                                enforcement == "absent"
                                and target_kind
                                in {
                                    "slot",
                                    "event_role",
                                    "atom_facet",
                                    "resource_kind",
                                },
                                f"universal v2 closed-event mapping enforcement mismatch: {legacy_label}",
                            )
            _require(
                non_guard_targets,
                f"universal v2 mapping cannot use a guard as content evidence: {legacy_label}",
            )
            if mapping_kind == "event_label" and allowed_states == ["closed"]:
                _require(
                    any(
                        target["enforcement"] == "absent"
                        and target["target_kind"]
                        in {
                            "slot",
                            "event_role",
                            "atom_facet",
                            "resource_kind",
                            "blocked_semantic",
                            "semantic_load_axis",
                        }
                        for target in targets
                    ),
                    f"universal v2 closed mapping lacks a direct blocked outcome: {legacy_label}",
                )
            output[legacy_label] = mapping
    expected_nonhuman_display_targets = [
        {
            "target_kind": "slot",
            "target_ids": ["expression"],
            "target_values": ["body_direction_and_light_intensity_display"],
            "quantifier": "all",
            "enforcement": "canonical_projection",
        },
        {
            "target_kind": "resource_kind",
            "target_ids": [
                "body_orientation",
                "body_contour_display",
                "internal_luminance_display",
                "light_emission",
            ],
            "target_values": [],
            "quantifier": "any",
            "enforcement": "eligible",
        },
        {
            "target_kind": "pixel_evidence_kind",
            "target_ids": ["display", "orientation"],
            "target_values": [],
            "quantifier": "any",
            "enforcement": "required",
        },
    ]
    _require(
        event_mapping_by_label["nonhuman_display_channel"]["targets"]
        == expected_nonhuman_display_targets,
        "universal v2 nonhuman display targets drift",
    )
    _require(
        set(event_mapping_by_label)
        == {label for label, _state in legacy_event_occurrences},
        "universal v2 event-label crosswalk is not exhaustive and exact",
    )
    for label, state in legacy_event_occurrences:
        _require(
            state in event_mapping_by_label[label]["allowed_legacy_states"],
            f"universal v2 event occurrence is not allowed by its mapping: {label}",
        )
    _require(
        set(bridge_mapping_by_label) == set(legacy_bridge_occurrences),
        "universal v2 bridge-label crosswalk is not exhaustive and exact",
    )
    _require(
        bridge_mapping_by_label["event_role"]["targets"]
        == [
            {
                "target_kind": "guard_contract",
                "target_ids": ["event_role_frames_role_assignment_guard"],
                "target_values": [],
                "quantifier": "all",
                "enforcement": "required",
            },
            {
                "target_kind": "event_role",
                "target_ids": ["actor", "action", "target", "result"],
                "target_values": [],
                "quantifier": "all",
                "enforcement": "required",
            },
            {
                "target_kind": "pixel_evidence_kind",
                "target_ids": [
                    "contact",
                    "orientation",
                    "path",
                    "support",
                    "state_boundary",
                ],
                "target_values": [],
                "quantifier": "any",
                "enforcement": "required",
            },
        ],
        "universal v2 event-role mapping must require only the literal event spine",
    )
    _require(
        bridge_mapping_by_label["handoff"]["targets"]
        == [
            {
                "target_kind": "runtime_bridge_type",
                "target_ids": ["ownership"],
                "target_values": [],
                "quantifier": "all",
                "enforcement": "required",
            },
            {
                "target_kind": "event_role",
                "target_ids": ["action", "instrument"],
                "target_values": [],
                "quantifier": "all",
                "enforcement": "required",
            },
            {
                "target_kind": "pixel_evidence_kind",
                "target_ids": ["contact", "path"],
                "target_values": [],
                "quantifier": "any",
                "enforcement": "required",
            },
        ],
        "universal v2 handoff mapping lost its literal material evidence",
    )
    all_mapping_rows = [*event_mapping_rows, *bridge_mapping_rows]
    visual_targets_by_mapping: dict[str, list[dict[str, Any]]] = {
        str(mapping["mapping_id"]): [
            target
            for target in mapping["targets"]
            if target["target_kind"] == "visual_candidate"
        ]
        for mapping in all_mapping_rows
        if any(
            target["target_kind"] == "visual_candidate" for target in mapping["targets"]
        )
    }
    _require(
        set(visual_targets_by_mapping)
        == set(UNIVERSAL_V2_VISUAL_CANDIDATE_TARGETS_BY_MAPPING),
        "universal v2 visual-candidate mapping coverage drift",
    )
    for mapping_id, (
        target_ids,
        quantifier,
        enforcement,
    ) in UNIVERSAL_V2_VISUAL_CANDIDATE_TARGETS_BY_MAPPING.items():
        _require(
            visual_targets_by_mapping[mapping_id]
            == [
                {
                    "target_kind": "visual_candidate",
                    "target_ids": target_ids,
                    "target_values": [],
                    "quantifier": quantifier,
                    "enforcement": enforcement,
                }
            ],
            f"universal v2 visual-candidate target drift: {mapping_id}",
        )
    guard_targets = [
        target
        for mapping in all_mapping_rows
        for target in mapping["targets"]
        if target["target_kind"] == "guard_contract"
    ]
    _require(
        len(guard_targets) == 15
        and all(target["enforcement"] == "required" for target in guard_targets),
        "universal v2 guard targets must be 15 required enforcement records",
    )
    _require(
        {guard_id for target in guard_targets for guard_id in target["target_ids"]}
        == set(guard_source_by_id),
        "universal v2 guard target/source contract coverage mismatch",
    )
    closed_event_mappings = [
        mapping
        for mapping in event_mapping_rows
        if mapping["allowed_legacy_states"] == ["closed"]
    ]
    _require(
        len(closed_event_mappings) == 7,
        "universal v2 closed event mapping inventory drift",
    )
    expected_tone_targets = [
        {
            "target_kind": "context_profile_field",
            "target_ids": ["tone"],
            "target_values": [],
            "quantifier": "all",
            "enforcement": "canonical_projection",
        },
        {
            "target_kind": "blocked_semantic",
            "target_ids": ["scene_promise_hijack"],
            "target_values": [],
            "quantifier": "all",
            "enforcement": "absent",
        },
        {
            "target_kind": "semantic_load_axis",
            "target_ids": ["theme_displacement"],
            "target_values": [],
            "quantifier": "all",
            "enforcement": "absent",
        },
        {
            "target_kind": "atom_facet",
            "target_ids": ["environment", "salience"],
            "target_values": [],
            "quantifier": "any",
            "enforcement": "required",
        },
        {
            "target_kind": "visual_candidate",
            "target_ids": ["usc_sptg_context_anchor_relation"],
            "target_values": [],
            "quantifier": "all",
            "enforcement": "required",
        },
        {
            "target_kind": "pixel_evidence_kind",
            "target_ids": ["display", "path"],
            "target_values": [],
            "quantifier": "any",
            "enforcement": "required",
        },
        {
            "target_kind": "guard_contract",
            "target_ids": ["usl_theme_hijack_guard"],
            "target_values": [],
            "quantifier": "all",
            "enforcement": "required",
        },
    ]
    _require(
        bridge_mapping_by_label["tone"]["targets"] == expected_tone_targets,
        "universal v2 tone mapping lost context, load, material, pixel, or guard evidence",
    )

    current_raw_lines = current_path.read_bytes().splitlines()
    current_rows = [json.loads(line) for line in current_raw_lines]
    _require(
        len(current_rows) == 24, "universal v2 current holdout must contain 24 rows"
    )
    _require(
        [row.get("case_id") for row in current_rows]
        == [row.get("case_id") for row in prompt_rows],
        "universal v2 current holdout case order drift",
    )
    current_row_keys = [
        "schema",
        "case_id",
        "revision",
        "source_lineage",
        "legacy_prompt_record",
        "canonical_scene_contract",
        "canonical_projection",
        "resolution_ledger",
        "runtime_expectations",
    ]
    ledger_counts: Counter[str] = Counter()
    ledger_authority_counts: Counter[tuple[str, bool]] = Counter()
    projected_slot_count = 0
    projected_role_count = 0
    compiled_obligation_reference_count = 0
    compiled_obligation_per_row_unique_count_sum = 0
    compiled_global_ids: set[str] = set()
    observed_historical_fixed_role_nonauthorities: list[tuple[str, str, str, str]] = []
    for current_index, current in enumerate(current_rows):
        case_id = current.get("case_id")
        prompt_index, prompt = prompt_by_case[case_id]
        historical_contract_index, historical_wrapper = historical_contract_by_case[
            case_id
        ]
        contract_index, wrapper = current_contract_by_case[case_id]
        contract = wrapper["scene_contract"]
        _require(
            list(current) == current_row_keys
            and current.get("schema") == UNIVERSAL_V2_CURRENT_HOLDOUT_SCHEMA
            and current.get("revision") == UNIVERSAL_V2_REVISION,
            f"universal v2 current row shape/revision mismatch: {case_id}",
        )
        _require(
            prompt_index
            == historical_contract_index
            == contract_index
            == current_index,
            f"universal v2 source record index mismatch: {case_id}",
        )
        expected_lineage = {
            "prompt_holdout": {
                "path": prompt_path.name,
                "schema": UNIVERSAL_SCENE_HOLDOUT_SCHEMA,
                "file_sha256": UNIVERSAL_V1_PROMPT_HOLDOUT_SHA256,
                "record_index": prompt_index + 1,
                "raw_record_sha256": hashlib.sha256(
                    prompt_raw_lines[prompt_index]
                ).hexdigest(),
            },
            "historical_scene_contract_holdout": {
                "path": historical_contract_path.name,
                "schema": UNIVERSAL_SCENE_CONTRACT_HOLDOUT_SCHEMA,
                "file_sha256": UNIVERSAL_V1_SCENE_CONTRACT_HOLDOUT_SHA256,
                "record_index": historical_contract_index + 1,
                "raw_record_sha256": hashlib.sha256(
                    historical_contract_raw_lines[historical_contract_index]
                ).hexdigest(),
            },
            "current_scene_contract_holdout": {
                "path": current_contract_path.name,
                "schema": UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SCHEMA,
                "file_sha256": UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SHA256,
                "record_index": contract_index + 1,
                "raw_record_sha256": hashlib.sha256(
                    current_contract_raw_lines[contract_index]
                ).hexdigest(),
            },
        }
        _require(
            current.get("source_lineage") == expected_lineage,
            f"universal v2 source lineage mismatch: {case_id}",
        )
        _require(
            current.get("legacy_prompt_record") == prompt,
            f"universal v2 legacy prompt was relabeled or rewritten: {case_id}",
        )
        _require(
            current.get("canonical_scene_contract") == contract,
            f"universal v2 canonical scene contract drift: {case_id}",
        )
        expected_projection = {
            "scene_contract_sha256": hashlib.sha256(
                canonical_json_bytes(contract)
            ).hexdigest(),
            "slot_states": copy.deepcopy(contract["slot_states"]),
            "event_roles": copy.deepcopy(contract["event_roles"]),
        }
        _require(
            current.get("canonical_projection") == expected_projection,
            f"universal v2 six-slot/eight-role projection drift: {case_id}",
        )
        projected_slot_count += len(expected_projection["slot_states"])
        projected_role_count += len(expected_projection["event_roles"])
        slot_by_id = {slot["slot_id"]: slot for slot in contract["slot_states"]}
        role_by_id = {role["role_id"]: role for role in contract["event_roles"]}
        expected_ledger: list[dict[str, Any]] = []

        for slot_id, legacy_state in prompt["expected_slot_states"].items():
            canonical = slot_by_id[slot_id]
            if legacy_state == canonical["state"]:
                continue
            superseded_case12_prop = (
                case_id == "universal_scene_12_nonhuman_display" and slot_id == "prop"
            )
            expected_ledger.append(
                _universal_v2_ledger_entry(
                    source_pointer=f"/expected_slot_states/{slot_id}",
                    legacy_kind="slot_state",
                    legacy_label=slot_id,
                    legacy_state=legacy_state,
                    legacy_value=None,
                    disposition="literal_contract_authority",
                    mapping_id=None,
                    runtime_authority=not superseded_case12_prop,
                    resolution=(
                        "superseded_by_literal_scope_correction"
                        if superseded_case12_prop
                        else None
                    ),
                    targets=(
                        _universal_v2_absence_target("slot", ["prop"])
                        if superseded_case12_prop
                        else _universal_v2_projection_target(
                            "slot",
                            slot_id,
                            list(canonical["value_ids"])
                            if canonical["state"] == "fixed"
                            else [],
                        )
                    ),
                )
            )

        legacy_role_records: list[tuple[str, str, str | None, str]] = []
        for role_id, legacy_value in prompt["expected_event_frame"][
            "fixed_roles"
        ].items():
            legacy_role_records.append(
                (
                    role_id,
                    "fixed",
                    legacy_value,
                    f"/expected_event_frame/fixed_roles/{role_id}",
                )
            )
        for legacy_state, field in (("open", "open_roles"), ("closed", "closed_roles")):
            for item_index, role_id in enumerate(prompt["expected_event_frame"][field]):
                legacy_role_records.append(
                    (
                        role_id,
                        legacy_state,
                        None,
                        f"/expected_event_frame/{field}/{item_index}",
                    )
                )
        for role_id, legacy_state, legacy_value, source_pointer in legacy_role_records:
            if role_id not in role_by_id:
                mapping = event_mapping_by_label[role_id]
                superseded_case12_held_prop = (
                    case_id == "universal_scene_12_nonhuman_display"
                    and role_id == "held_prop"
                )
                expected_ledger.append(
                    _universal_v2_ledger_entry(
                        source_pointer=source_pointer,
                        legacy_kind="event_label",
                        legacy_label=role_id,
                        legacy_state=legacy_state,
                        legacy_value=legacy_value,
                        disposition="reviewed_crosswalk",
                        mapping_id=mapping["mapping_id"],
                        runtime_authority=not superseded_case12_held_prop,
                        resolution=(
                            "superseded_by_literal_scope_correction"
                            if superseded_case12_held_prop
                            else None
                        ),
                        targets=mapping["targets"],
                    )
                )
                continue
            canonical = role_by_id[role_id]
            canonical_values = (
                [canonical["value_id"]]
                if canonical["state"] == "fixed" and canonical["value_id"] is not None
                else []
            )
            if legacy_state != canonical["state"]:
                superseded_case12_instrument = (
                    case_id == "universal_scene_12_nonhuman_display"
                    and role_id == "instrument"
                )
                historical_fixed_role_nonauthority = (
                    case_id,
                    role_id,
                    legacy_value,
                    source_pointer,
                ) in UNIVERSAL_V2_HISTORICAL_FIXED_ROLE_NONAUTHORITIES
                expected_ledger.append(
                    _universal_v2_ledger_entry(
                        source_pointer=source_pointer,
                        legacy_kind="event_role_state",
                        legacy_label=role_id,
                        legacy_state=legacy_state,
                        legacy_value=legacy_value if legacy_state == "fixed" else None,
                        disposition=(
                            "historical_non_authoritative_expectation"
                            if historical_fixed_role_nonauthority
                            else "literal_contract_authority"
                        ),
                        mapping_id=None,
                        runtime_authority=not (
                            superseded_case12_instrument
                            or historical_fixed_role_nonauthority
                        ),
                        resolution=(
                            "superseded_by_literal_scope_correction"
                            if superseded_case12_instrument
                            else "historical_only_no_literal_role_binding"
                            if historical_fixed_role_nonauthority
                            else None
                        ),
                        targets=(
                            _universal_v2_absence_target("event_role", ["instrument"])
                            if superseded_case12_instrument
                            else _universal_v2_projection_target(
                                "event_role", role_id, canonical_values
                            )
                        ),
                    )
                )
            if (
                legacy_state == "fixed"
                and canonical["state"] == "fixed"
                and legacy_value != canonical["value_id"]
            ):
                expected_ledger.append(
                    _universal_v2_ledger_entry(
                        source_pointer=source_pointer,
                        legacy_kind="event_role_value",
                        legacy_label=role_id,
                        legacy_state="fixed",
                        legacy_value=legacy_value,
                        disposition="canonical_value_alias",
                        mapping_id=None,
                        targets=_universal_v2_projection_target(
                            "event_role", role_id, canonical_values
                        ),
                    )
                )

        mapped_research_ids: list[str] = []
        mapped_runtime_types: set[str] = set()
        for bridge_index, bridge_label in enumerate(
            prompt["semantic_distance_expectation"]["required_bridge_types"]
        ):
            mapping = bridge_mapping_by_label[bridge_label]
            if mapping["mapping_id"] not in mapped_research_ids:
                mapped_research_ids.append(mapping["mapping_id"])
            for target in mapping["targets"]:
                if target["target_kind"] == "runtime_bridge_type":
                    mapped_runtime_types.update(target["target_ids"])
            expected_ledger.append(
                _universal_v2_ledger_entry(
                    source_pointer=(
                        "/semantic_distance_expectation/"
                        f"required_bridge_types/{bridge_index}"
                    ),
                    legacy_kind="research_bridge_label",
                    legacy_label=bridge_label,
                    legacy_state=None,
                    legacy_value=None,
                    disposition="reviewed_crosswalk",
                    mapping_id=mapping["mapping_id"],
                    targets=mapping["targets"],
                )
            )
        custom_correction = UNIVERSAL_V2_CUSTOM_EMBODIMENT_CORRECTIONS.get(case_id)
        if custom_correction is not None:
            entity_index, entity_id, historical_profile_id, current_profile_id = (
                custom_correction
            )
            current_entity = contract["identity_core"]["entities"][entity_index]
            available_resources = [
                capability["id"]
                for capability in current_entity["capabilities"]
                if capability["state"] == "available"
            ]
            unavailable_resources = [
                capability["id"]
                for capability in current_entity["capabilities"]
                if capability["state"] == "unavailable"
            ]
            canonical_targets = _universal_v2_projection_target(
                "embodiment_profile", entity_id, [current_profile_id]
            )
            if available_resources:
                canonical_targets.append(
                    {
                        "target_kind": "resource_kind",
                        "target_ids": available_resources,
                        "target_values": [entity_id],
                        "quantifier": "all",
                        "enforcement": "eligible",
                    }
                )
            if unavailable_resources:
                canonical_targets.append(
                    {
                        "target_kind": "resource_kind",
                        "target_ids": unavailable_resources,
                        "target_values": [entity_id],
                        "quantifier": "all",
                        "enforcement": "absent",
                    }
                )
            expected_ledger.extend(
                [
                    _universal_v2_ledger_entry(
                        source_id="historical_scene_contract_record",
                        source_pointer=(
                            f"/scene_contract/identity_core/entities/{entity_index}"
                        ),
                        legacy_kind="scene_contract_custom_embodiment_scope",
                        legacy_label=entity_id,
                        legacy_state=None,
                        legacy_value=historical_profile_id,
                        disposition="superseded_contract_projection",
                        mapping_id=None,
                        runtime_authority=False,
                        resolution=(
                            "superseded_by_reviewed_custom_embodiment_scope_correction"
                        ),
                        targets=_universal_v2_projection_target(
                            "embodiment_profile",
                            entity_id,
                            [historical_profile_id],
                        ),
                    ),
                    _universal_v2_ledger_entry(
                        source_id="canonical_scene_contract",
                        source_pointer=f"/identity_core/entities/{entity_index}",
                        legacy_kind="scene_contract_custom_embodiment_scope",
                        legacy_label=entity_id,
                        legacy_state=None,
                        legacy_value=current_profile_id,
                        disposition="reviewed_custom_embodiment_scope_correction",
                        mapping_id=None,
                        runtime_authority=True,
                        resolution="enforced_reviewed_custom_embodiment_scope",
                        targets=canonical_targets,
                    ),
                ]
            )
        if case_id == "universal_scene_16_contact_resource":
            canonical_targets = _universal_v2_projection_target(
                "embodiment_profile",
                "actor_01",
                [UNIVERSAL_V2_C16_EMBODIMENT_PROFILE_ID],
            )
            canonical_targets.extend(
                [
                    {
                        "target_kind": "resource_kind",
                        "target_ids": [
                            resource_kind
                            for resource_kind, _capacity in (
                                UNIVERSAL_V2_C16_PROFILE_CAPACITIES
                            )
                        ],
                        "target_values": ["actor_01"],
                        "quantifier": "all",
                        "enforcement": "eligible",
                    },
                    {
                        "target_kind": "guard_contract",
                        "target_ids": ["ubp_embodiment_capability_guard"],
                        "target_values": ["actor_01"],
                        "quantifier": "all",
                        "enforcement": "required",
                    },
                ]
            )
            expected_ledger.extend(
                [
                    _universal_v2_ledger_entry(
                        source_id="historical_scene_contract_record",
                        source_pointer="/scene_contract/identity_core/entities/0",
                        legacy_kind="scene_contract_embodiment_resource_scope",
                        legacy_label="actor_01",
                        legacy_state=None,
                        legacy_value=("four_armed_adult_equivalent_mechanical_entity"),
                        disposition="superseded_contract_projection",
                        mapping_id=None,
                        runtime_authority=False,
                        resolution=(
                            "superseded_by_reviewed_embodiment_profile_scope_correction"
                        ),
                        targets=[
                            {
                                "target_kind": "resource_kind",
                                "target_ids": ["manipulator"],
                                "target_values": ["actor_01"],
                                "quantifier": "all",
                                "enforcement": "eligible",
                            }
                        ],
                    ),
                    _universal_v2_ledger_entry(
                        source_id="canonical_scene_contract",
                        source_pointer="/identity_core/entities/0",
                        legacy_kind="scene_contract_embodiment_resource_scope",
                        legacy_label="actor_01",
                        legacy_state=None,
                        legacy_value=UNIVERSAL_V2_C16_EMBODIMENT_PROFILE_ID,
                        disposition="reviewed_embodiment_profile_scope_correction",
                        mapping_id=None,
                        runtime_authority=True,
                        resolution="enforced_reviewed_embodiment_profile_scope",
                        targets=canonical_targets,
                    ),
                ]
            )
        if case_id == "universal_scene_12_nonhuman_display":
            expected_ledger.extend(
                [
                    _universal_v2_ledger_entry(
                        source_id="historical_scene_contract_record",
                        source_pointer="/scene_contract/slot_states/4",
                        legacy_kind="scene_contract_slot_state",
                        legacy_label="prop",
                        legacy_state="closed",
                        legacy_value=None,
                        disposition="superseded_contract_projection",
                        mapping_id=None,
                        runtime_authority=False,
                        resolution="superseded_by_literal_scope_correction",
                        targets=_universal_v2_absence_target("slot", ["prop"]),
                    ),
                    _universal_v2_ledger_entry(
                        source_id="historical_scene_contract_record",
                        source_pointer="/scene_contract/event_roles/3",
                        legacy_kind="scene_contract_event_role_state",
                        legacy_label="instrument",
                        legacy_state="closed",
                        legacy_value=None,
                        disposition="superseded_contract_projection",
                        mapping_id=None,
                        runtime_authority=False,
                        resolution="superseded_by_literal_scope_correction",
                        targets=_universal_v2_absence_target(
                            "event_role", ["instrument"]
                        ),
                    ),
                    _universal_v2_ledger_entry(
                        source_id="canonical_scene_contract",
                        source_pointer="/identity_core/entities/0/capabilities",
                        legacy_kind="scene_contract_resource_scope",
                        legacy_label="actor_01",
                        legacy_state=None,
                        legacy_value=None,
                        disposition="literal_resource_scope_correction",
                        mapping_id=None,
                        runtime_authority=True,
                        resolution="enforced_literal_resource_scope",
                        targets=[
                            {
                                "target_kind": "resource_kind",
                                "target_ids": [
                                    "facial_display",
                                    "manipulator",
                                    "appendage",
                                ],
                                "target_values": ["actor_01"],
                                "quantifier": "all",
                                "enforcement": "absent",
                            },
                            {
                                "target_kind": "blocked_semantic",
                                "target_ids": [
                                    "human_face_attachment",
                                    "human_hand_attachment",
                                    "human_limb_attachment",
                                ],
                                "target_values": ["actor_01"],
                                "quantifier": "all",
                                "enforcement": "absent",
                            },
                            {
                                "target_kind": "guard_contract",
                                "target_ids": ["ubp_embodiment_capability_guard"],
                                "target_values": ["actor_01"],
                                "quantifier": "all",
                                "enforcement": "required",
                            },
                        ],
                    ),
                ]
            )
        if case_id in {
            "universal_scene_15_action_phase",
            "universal_scene_18_prop_lexical_normalization",
        }:
            expected_ledger.extend(
                [
                    _universal_v2_ledger_entry(
                        source_id="historical_scene_contract_record",
                        source_pointer="/scene_contract/context_profile/scale",
                        legacy_kind="scene_contract_context_profile_value",
                        legacy_label="scale",
                        legacy_state=None,
                        legacy_value="intimate",
                        disposition="superseded_contract_projection",
                        mapping_id=None,
                        runtime_authority=False,
                        resolution="superseded_by_literal_context_scope_correction",
                        targets=_universal_v2_projection_target(
                            "context_profile_field", "scale", ["intimate"]
                        ),
                    ),
                    _universal_v2_ledger_entry(
                        source_id="canonical_scene_contract",
                        source_pointer="/context_profile/scale",
                        legacy_kind="scene_contract_context_scope",
                        legacy_label="scale",
                        legacy_state=None,
                        legacy_value="unknown",
                        disposition="literal_context_scope_correction",
                        mapping_id=None,
                        runtime_authority=True,
                        resolution="enforced_literal_context_scope",
                        targets=_universal_v2_projection_target(
                            "context_profile_field", "scale", ["unknown"]
                        ),
                    ),
                ]
            )
        if case_id == "universal_scene_24_closed_no_prop_consequence":
            display_targets = event_mapping_by_label["nonhuman_display_channel"][
                "targets"
            ]
            expected_ledger.extend(
                [
                    _universal_v2_ledger_entry(
                        source_id="historical_scene_contract_record",
                        source_pointer="/scene_contract/slot_states/0",
                        legacy_kind="scene_contract_slot_state",
                        legacy_label="expression",
                        legacy_state="closed",
                        legacy_value=None,
                        disposition="superseded_contract_projection",
                        mapping_id=None,
                        runtime_authority=False,
                        resolution="superseded_by_display_channel_scope_correction",
                        targets=_universal_v2_absence_target("slot", ["expression"]),
                    ),
                    _universal_v2_ledger_entry(
                        source_id="canonical_scene_contract",
                        source_pointer="/slot_states/0",
                        legacy_kind="scene_contract_display_scope",
                        legacy_label="expression",
                        legacy_state="fixed",
                        legacy_value="body_direction_and_light_intensity_display",
                        disposition="literal_display_channel_scope_correction",
                        mapping_id=None,
                        runtime_authority=True,
                        resolution="enforced_nonhuman_display_channel",
                        targets=display_targets,
                    ),
                ]
            )
        expected_ledger.sort(
            key=lambda item: (
                item["source_id"].encode("utf-8"),
                item["source_pointer"].encode("utf-8"),
                item["legacy_kind"].encode("utf-8"),
                item["legacy_label"].encode("utf-8"),
            )
        )
        _require(
            current.get("resolution_ledger") == expected_ledger,
            f"universal v2 resolution ledger drift: {case_id}",
        )
        historical_fixed_role_entries = [
            entry
            for entry in expected_ledger
            if entry["source_id"] == "legacy_prompt_record"
            and entry["legacy_kind"] == "event_role_state"
            and entry["legacy_state"] == "fixed"
            and entry["disposition"] == "historical_non_authoritative_expectation"
        ]
        for entry in historical_fixed_role_entries:
            canonical_role = role_by_id[entry["legacy_label"]]
            _require(
                entry["runtime_authority"] is False
                and entry["resolution"] == "historical_only_no_literal_role_binding"
                and canonical_role["state"] == "open"
                and canonical_role["value_id"] is None
                and entry["targets"]
                == _universal_v2_projection_target(
                    "event_role", entry["legacy_label"], []
                ),
                f"universal v2 historical fixed-role nonauthority drift: {case_id}",
            )
            observed_historical_fixed_role_nonauthorities.append(
                (
                    case_id,
                    entry["legacy_label"],
                    entry["legacy_value"],
                    entry["source_pointer"],
                )
            )
        for entry in expected_ledger:
            if (
                entry["source_id"] == "legacy_prompt_record"
                and entry["legacy_kind"] == "event_role_state"
                and entry["legacy_state"] == "fixed"
                and entry["runtime_authority"] is True
            ):
                canonical_role = role_by_id[entry["legacy_label"]]
                _require(
                    entry["disposition"] == "literal_contract_authority"
                    and canonical_role["state"] == "fixed"
                    and canonical_role["value_id"] is not None
                    and all(
                        target["target_kind"] == "event_role"
                        and target["enforcement"] == "canonical_projection"
                        and target["target_values"]
                        for target in entry["targets"]
                    ),
                    f"universal v2 authoritative fixed role lacks a nonnull literal projection: {case_id}",
                )
        ledger_counts.update(item["legacy_kind"] for item in expected_ledger)
        ledger_authority_counts.update(
            (item["legacy_kind"], bool(item["runtime_authority"]))
            for item in expected_ledger
        )
        expected_compiled_contract = _compile_universal_v2_obligations(
            expected_ledger,
            guard_source_by_id,
        )
        historical_ledger_indices = {
            ledger_index
            for ledger_index, entry in enumerate(expected_ledger)
            if entry["runtime_authority"] is False
        }
        _require(
            all(
                source_ref["ledger_entry_index"] not in historical_ledger_indices
                for obligation in expected_compiled_contract["obligations"]
                for source_ref in obligation["source_refs"]
            ),
            f"universal v2 historical ledger row compiled an obligation: {case_id}",
        )
        compiled_obligation_per_row_unique_count_sum += len(
            expected_compiled_contract["obligations"]
        )
        compiled_obligation_reference_count += sum(
            len(obligation["source_refs"])
            for obligation in expected_compiled_contract["obligations"]
        )
        compiled_global_ids.update(
            obligation["obligation_id"]
            for obligation in expected_compiled_contract["obligations"]
        )

        distance = prompt["semantic_distance_expectation"]
        band_requirement = expected_band_policy["band_requirements"][distance["band"]]
        required_type_ids = [
            bridge_type
            for bridge_type in UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS
            if bridge_type in mapped_runtime_types
        ]
        runtime_prop = copy.deepcopy(prompt["prop_expectation"])
        runtime_required_evidence = copy.deepcopy(prompt["required_pack_evidence"])
        runtime_forbidden_overwrite = copy.deepcopy(prompt["forbidden_overwrite"])
        if case_id == "universal_scene_12_nonhuman_display":
            runtime_prop = {
                "policy": "open",
                "load": "bounded_unknown",
                "named_prop": None,
            }
            runtime_required_evidence = [
                "nonhuman_display_only",
                "limbless_capability_match",
                "wind_response_visible",
                "nonhand_support_allowed",
            ]
            runtime_forbidden_overwrite = [
                "human_face",
                "human_hands",
                "biped_pose",
                "cute_mascot_anatomy",
            ]
        expected_runtime = {
            "semantic_distance": copy.deepcopy(distance),
            "prop": runtime_prop,
            "required_pack_evidence": runtime_required_evidence,
            "forbidden_overwrite": runtime_forbidden_overwrite,
            "runtime_bridge_contract": {
                "allowed_type_ids": list(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS),
                "category_members": copy.deepcopy(
                    expected_band_policy["category_members"]
                ),
                "minimum_distinct_type_count": max(
                    band_requirement["minimum_distinct_type_count"],
                    len(required_type_ids),
                ),
                "required_category_ids": copy.deepcopy(
                    band_requirement["required_category_ids"]
                ),
                "required_type_ids": required_type_ids,
                "mapped_research_obligation_ids": mapped_research_ids,
            },
            "compiled_obligation_contract": expected_compiled_contract,
        }
        _require(
            current.get("runtime_expectations") == expected_runtime,
            f"universal v2 runtime expectation drift: {case_id}",
        )

    _require(
        observed_historical_fixed_role_nonauthorities
        == UNIVERSAL_V2_HISTORICAL_FIXED_ROLE_NONAUTHORITIES,
        "universal v2 historical fixed-role nonauthority inventory drift",
    )
    expected_ledger_counts = {
        "slot_state": 18,
        "event_role_state": 31,
        "event_role_value": 44,
        "event_label": 34,
        "research_bridge_label": 81,
        "scene_contract_slot_state": 2,
        "scene_contract_event_role_state": 1,
        "scene_contract_resource_scope": 1,
        "scene_contract_context_profile_value": 2,
        "scene_contract_context_scope": 2,
        "scene_contract_display_scope": 1,
        "scene_contract_embodiment_resource_scope": 2,
        "scene_contract_custom_embodiment_scope": 10,
    }
    _require(
        dict(ledger_counts) == expected_ledger_counts,
        "universal v2 resolution ledger aggregate mismatch",
    )

    manifest = _load_json(manifest_path)
    _require(
        isinstance(manifest, dict)
        and list(manifest)
        == [
            "schema",
            "revision",
            "status",
            "source_lineage",
            "artifacts",
            "counts",
            "authoring_boundary",
            "limits",
        ]
        and manifest.get("schema") == UNIVERSAL_V2_CURRENT_MANIFEST_SCHEMA
        and manifest.get("revision") == UNIVERSAL_V2_REVISION
        and manifest.get("status") == "current",
        "universal v2 manifest top-level contract mismatch",
    )
    expected_source_lineage = {
        "prompt_holdout": {
            "path": prompt_path.name,
            "schema": UNIVERSAL_SCENE_HOLDOUT_SCHEMA,
            "record_count": 24,
            "sha256": UNIVERSAL_V1_PROMPT_HOLDOUT_SHA256,
        },
        "historical_scene_contract_holdout": {
            "path": historical_contract_path.name,
            "schema": UNIVERSAL_SCENE_CONTRACT_HOLDOUT_SCHEMA,
            "record_count": 24,
            "sha256": UNIVERSAL_V1_SCENE_CONTRACT_HOLDOUT_SHA256,
        },
        "current_scene_contract_holdout": {
            "path": current_contract_path.name,
            "schema": UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SCHEMA,
            "record_count": 24,
            "sha256": UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SHA256,
        },
    }
    expected_artifacts = {
        "current_holdout": {
            "path": current_path.name,
            "schema": UNIVERSAL_V2_CURRENT_HOLDOUT_SCHEMA,
            "record_count": 24,
            "sha256": UNIVERSAL_V2_CURRENT_HOLDOUT_SHA256,
        },
        "crosswalk": {
            "path": crosswalk_path.name,
            "schema": UNIVERSAL_V2_EXPECTATION_CROSSWALK_SCHEMA,
            "record_count": 65,
            "sha256": UNIVERSAL_V2_EXPECTATION_CROSSWALK_SHA256,
        },
    }
    expected_counts = {
        "case_count": 24,
        "projected_slot_count": 144,
        "projected_event_role_count": 192,
        "contract_v2_schema_migration_count": contract_v2_schema_migration_count,
        "contract_v2_semantic_correction_count": contract_v2_semantic_correction_count,
        "contract_v2_phrase_order_normalization_count": contract_v2_phrase_order_normalization_count,
        "historical_contract_context_value_correction_count": ledger_counts[
            "scene_contract_context_profile_value"
        ],
        "literal_context_scope_correction_count": ledger_counts[
            "scene_contract_context_scope"
        ],
        "literal_display_channel_scope_correction_count": ledger_counts[
            "scene_contract_display_scope"
        ],
        "historical_contract_embodiment_resource_scope_correction_count": (
            ledger_authority_counts[("scene_contract_embodiment_resource_scope", False)]
        ),
        "reviewed_embodiment_profile_scope_correction_count": (
            ledger_authority_counts[("scene_contract_embodiment_resource_scope", True)]
        ),
        "historical_contract_custom_embodiment_scope_correction_count": (
            ledger_authority_counts[("scene_contract_custom_embodiment_scope", False)]
        ),
        "reviewed_custom_embodiment_scope_correction_count": (
            ledger_authority_counts[("scene_contract_custom_embodiment_scope", True)]
        ),
        "historical_contract_slot_state_correction_count": ledger_counts[
            "scene_contract_slot_state"
        ],
        "historical_contract_event_role_state_correction_count": ledger_counts[
            "scene_contract_event_role_state"
        ],
        "literal_resource_scope_correction_count": ledger_counts[
            "scene_contract_resource_scope"
        ],
        "legacy_slot_state_conflict_count": ledger_counts["slot_state"],
        "legacy_role_state_conflict_count": ledger_counts["event_role_state"],
        "legacy_fixed_role_value_conflict_count": ledger_counts["event_role_value"],
        "legacy_noncanonical_event_label_occurrence_count": 34,
        "legacy_noncanonical_event_label_unique_count": 30,
        "legacy_bridge_obligation_count": 81,
        "legacy_noncanonical_bridge_occurrence_count": 39,
        "legacy_noncanonical_bridge_unique_count": 29,
        "cases_with_noncanonical_bridge_labels": 18,
        "resolution_ledger_entry_count": sum(ledger_counts.values()),
        "compiled_obligation_reference_count": compiled_obligation_reference_count,
        "compiled_obligation_per_row_unique_count_sum": compiled_obligation_per_row_unique_count_sum,
        "compiled_obligation_global_unique_count": len(compiled_global_ids),
        "guard_source_contract_count": 9,
    }
    _require(
        manifest.get("source_lineage") == expected_source_lineage
        and manifest.get("artifacts") == expected_artifacts
        and manifest.get("counts") == expected_counts,
        "universal v2 manifest lineage, artifacts, or counts drift",
    )
    _require(
        projected_slot_count == expected_counts["projected_slot_count"]
        and projected_role_count == expected_counts["projected_event_role_count"]
        and len(legacy_event_occurrences)
        == expected_counts["legacy_noncanonical_event_label_occurrence_count"]
        and len({label for label, _state in legacy_event_occurrences})
        == expected_counts["legacy_noncanonical_event_label_unique_count"]
        and len(legacy_bridge_occurrences)
        == expected_counts["legacy_bridge_obligation_count"]
        and sum(label not in closed_bridge_set for label in legacy_bridge_occurrences)
        == expected_counts["legacy_noncanonical_bridge_occurrence_count"]
        and len(set(legacy_bridge_occurrences) - closed_bridge_set)
        == expected_counts["legacy_noncanonical_bridge_unique_count"]
        and len(cases_with_noncanonical_bridge_labels)
        == expected_counts["cases_with_noncanonical_bridge_labels"]
        and compiled_obligation_reference_count
        == expected_counts["compiled_obligation_reference_count"]
        and compiled_obligation_per_row_unique_count_sum
        == expected_counts["compiled_obligation_per_row_unique_count_sum"]
        and len(compiled_global_ids)
        == expected_counts["compiled_obligation_global_unique_count"]
        and len(guard_source_rows) == expected_counts["guard_source_contract_count"],
        "universal v2 manifest computed count mismatch",
    )
    expected_authoring_boundary = {
        "allowed_input_paths": [
            prompt_path.name,
            historical_contract_path.name,
            current_contract_path.name,
            crosswalk_path.name,
        ],
        "forbidden_input_prefixes": [
            "prompt_qualification_v3/",
            "generated_images/",
            "runs/",
        ],
        "runtime_outputs_used": False,
    }
    expected_limits = {
        "prompt_only": "This oracle qualifies typed planning, literal binding, and runtime evidence obligations; it does not prove rendered pixel truth.",
        "post_contract_revision": "This is a post-contract qualification revision, not evidence frozen before implementation.",
        "runtime_independence": "The current oracle is authored only from immutable v1 prompt and scene-contract sources, the reviewed scene-contract v2 migrations and corrections, and the reviewed global crosswalk; it never reads candidate packs, runtime selections, qualification outputs, generated images, or run ledgers.",
        "runtime_evaluation_boundary": "Source-only compilation never loads production assets; a separate asset-backed evaluator may compare compiled expectations with runtime selections and guard definitions.",
        "population_claim": "Local qualification does not prove population-level preference, originality, commercial response, or legal clearance.",
    }
    _require(
        manifest.get("authoring_boundary") == expected_authoring_boundary
        and manifest.get("limits") == expected_limits,
        "universal v2 manifest authoring boundary or limits drift",
    )

    baseline = _load_json(baseline_v2_path)
    _require(
        isinstance(baseline, dict)
        and list(baseline)
        == [
            "schema",
            "created_at",
            "status",
            "historical_baseline",
            "source_lineage",
            "current_oracle",
            "compiled_obligations",
            "validator_contract",
            "invariants",
        ]
        and baseline.get("schema") == UNIVERSAL_V2_BASELINE_SCHEMA
        and baseline.get("created_at") == "2026-08-10"
        and baseline.get("status") == "current",
        "universal v2 baseline top-level contract mismatch",
    )
    _require(
        baseline.get("historical_baseline")
        == {
            "path": baseline_v1_path.name,
            "schema": "subculture_illustration_universal_scene_baseline/v1",
            "sha256": UNIVERSAL_V1_BASELINE_SHA256,
        },
        "universal v2 historical baseline binding drift",
    )
    expected_current_oracle = {
        "current_holdout": expected_artifacts["current_holdout"],
        "crosswalk": expected_artifacts["crosswalk"],
        "manifest": {
            "path": manifest_path.name,
            "schema": UNIVERSAL_V2_CURRENT_MANIFEST_SCHEMA,
            "record_count": 1,
            "sha256": UNIVERSAL_V2_CURRENT_MANIFEST_SHA256,
        },
    }
    module_constant_names = [
        "UNIVERSAL_V1_PROMPT_HOLDOUT_SHA256",
        "UNIVERSAL_V1_SCENE_CONTRACT_HOLDOUT_SHA256",
        "UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SHA256",
        "UNIVERSAL_V2_CURRENT_HOLDOUT_SHA256",
        "UNIVERSAL_V2_EXPECTATION_CROSSWALK_SHA256",
        "UNIVERSAL_V2_CURRENT_MANIFEST_SHA256",
    ]
    _require(
        baseline.get("source_lineage") == expected_source_lineage
        and baseline.get("current_oracle") == expected_current_oracle,
        "universal v2 baseline three-way lineage binding drift",
    )
    _require(
        baseline.get("compiled_obligations")
        == {
            "schema": UNIVERSAL_V2_COMPILED_OBLIGATION_SCHEMA,
            "case_count": 24,
            "obligation_reference_count": compiled_obligation_reference_count,
            "per_row_unique_obligation_count_sum": compiled_obligation_per_row_unique_count_sum,
            "global_unique_obligation_count": len(compiled_global_ids),
            "guard_source_contract_count": 9,
        },
        "universal v2 baseline compiled-obligation summary drift",
    )
    _require(
        baseline.get("validator_contract")
        == {
            "path": "../scripts/validate_illustration_assets.py",
            "sha256": _sha256(validator_path),
            "module_constant_names": module_constant_names,
        },
        "universal v2 baseline validator binding drift",
    )
    expected_baseline_invariants = [
        "The v1 prompt holdout, v1 scene-contract holdout, and v1 baseline remain byte-immutable historical evidence.",
        "All six slot records and all eight event-role records are exact projections of the canonical literal-bound scene contract.",
        "Every legacy noncanonical role or bridge label remains verbatim and has one reviewed global enforcement mapping.",
        "Every resolution-ledger target is compiled exactly once per occurrence into a typed evaluator obligation; deduplication preserves all source references.",
        "Guard targets are required mechanism bindings whose exact source and block outcome are independently joined to runtime assets; they never substitute for material semantic evidence.",
        "Runtime bridges use only the closed seven-type enum and never weaken the frozen near, middle, or far category minimums.",
        "Production runtime and candidate assets do not load holdout files or branch on case IDs or exact holdout request text.",
        "The current v2 oracle is a post-contract revision authored without runtime, pack, audit, qualification, or image output.",
        "Baseline and manifest hashes are descriptive records; validator constants and the independent test fixture provide the fail-closed anchor.",
        "Explicit legacy candidate-pack v1 and v2 replay remains byte-identical and is never relabeled as v3 evidence.",
    ]
    _require(
        baseline.get("invariants") == expected_baseline_invariants,
        "universal v2 baseline invariants drift",
    )
    return {
        "schema": UNIVERSAL_V2_CURRENT_HOLDOUT_SCHEMA,
        "case_count": len(current_rows),
        "projected_slot_count": projected_slot_count,
        "projected_event_role_count": projected_role_count,
        "resolution_ledger_entry_count": sum(ledger_counts.values()),
        "compiled_obligation_reference_count": compiled_obligation_reference_count,
        "compiled_obligation_per_row_unique_count_sum": compiled_obligation_per_row_unique_count_sum,
        "compiled_obligation_global_unique_count": len(compiled_global_ids),
        "guard_source_contract_count": len(guard_source_rows),
        "event_mapping_count": len(event_mapping_rows),
        "bridge_mapping_count": len(bridge_mapping_rows),
        "closed_runtime_bridge_type_count": len(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS),
        "prompt_holdout_sha256": UNIVERSAL_V1_PROMPT_HOLDOUT_SHA256,
        "scene_contract_holdout_sha256": UNIVERSAL_V1_SCENE_CONTRACT_HOLDOUT_SHA256,
        "current_scene_contract_holdout_sha256": UNIVERSAL_V2_SCENE_CONTRACT_HOLDOUT_SHA256,
        "current_holdout_sha256": UNIVERSAL_V2_CURRENT_HOLDOUT_SHA256,
        "crosswalk_sha256": UNIVERSAL_V2_EXPECTATION_CROSSWALK_SHA256,
        "manifest_sha256": UNIVERSAL_V2_CURRENT_MANIFEST_SHA256,
        "baseline_v1_sha256": UNIVERSAL_V1_BASELINE_SHA256,
        "baseline_v2_sha256": _sha256(baseline_v2_path),
        "validator_sha256": _sha256(validator_path),
    }


def _oracle_effect_occurrences(
    request_text: str,
    scene_contract: Mapping[str, Any],
    selected_roles: Mapping[str, Mapping[str, Any]],
    semantic_bindings: Mapping[str, Any],
) -> set[tuple[str, str, str | None]]:
    """Independently classify scoped positive contract effects.

    The runtime snapshot is evidence, not the authority for this replay.  This
    classifier starts from the literal-bound contract and the reviewed effect
    profiles so removing an occurrence and merely recomputing snapshot hashes
    cannot turn a dangerous positive assertion into an apparent absence.
    """

    profiles = _validate_contract_effect_profiles(semantic_bindings)
    identity = scene_contract["identity_core"]
    entities = identity["entities"]
    actor_id = str(entities[0]["entity_id"])
    entity_ids = {str(entity["entity_id"]) for entity in entities}
    slots = {str(item["slot_id"]): item for item in scene_contract["slot_states"]}
    roles = {str(item["role_id"]): item for item in scene_contract["event_roles"]}
    context = scene_contract["context_profile"]

    def values(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if value is None:
            return []
        return [str(value)]

    def target_texts(
        profile: Mapping[str, Any],
        *,
        omit_feature_facts: bool = False,
    ) -> list[str]:
        result: list[str] = []
        for target in profile["source_targets"]:
            kind = str(target["source_kind"])
            source_id = str(target["source_id"])
            if kind == "request" and source_id == "concept":
                result.append(request_text)
            elif kind == "slot" and source_id in slots:
                slot = slots[source_id]
                if slot["state"] == "fixed":
                    result.extend(str(item) for item in slot["value_ids"])
                    result.extend(str(item) for item in slot["request_phrases"])
            elif kind == "event_role" and source_id in roles:
                role = roles[source_id]
                if role["state"] == "fixed":
                    result.extend(values(role["value_id"]))
                    result.extend(str(item) for item in role["request_phrases"])
            elif kind == "context" and source_id in context:
                result.extend(values(context[source_id]))
            elif kind == "identity_fact" and source_id == "feature_fact":
                if not omit_feature_facts:
                    for entity in entities:
                        for fact in entity["feature_facts"]:
                            result.append(str(fact["id"]))
                            result.extend(str(item) for item in fact["request_phrases"])
            elif kind == "identity_fact" and source_id == "scene_fact":
                for fact in identity["scene_facts"]:
                    result.append(str(fact["id"]))
                    result.extend(str(item) for item in fact["request_phrases"])
        return result

    occurrences: set[tuple[str, str, str | None]] = set()
    for profile in profiles:
        effect_id = str(profile["effect_id"])
        profile_id = str(profile["id"])
        binding = str(profile["subject_binding"])
        if binding == "source_entity":
            for entity in entities:
                entity_texts = [
                    text
                    for fact in entity["feature_facts"]
                    for text in [str(fact["id"]), *map(str, fact["request_phrases"])]
                ]
                if effect_id in _classify_universal_contract_effects(
                    entity_texts,
                    [profile],
                ):
                    occurrences.add((effect_id, profile_id, str(entity["entity_id"])))
            remaining_texts = target_texts(profile, omit_feature_facts=True)
            if effect_id in _classify_universal_contract_effects(
                remaining_texts,
                [profile],
            ):
                occurrences.add((effect_id, profile_id, actor_id))
            continue
        texts = target_texts(profile)
        if effect_id not in _classify_universal_contract_effects(texts, [profile]):
            continue
        if binding == "scene":
            subject_ref: str | None = None
        elif binding in {"target", "recipient"}:
            selected = selected_roles[binding]["value_id"]
            subject_ref = (
                str(selected)
                if isinstance(selected, str) and selected in entity_ids
                else binding
            )
        else:
            subject_ref = actor_id
        occurrences.add((effect_id, profile_id, subject_ref))
    return occurrences


def evaluate_universal_scene_compiled_obligations(
    scene: Mapping[str, Any],
    oracle_row: Mapping[str, Any],
    assets: Any,
    *,
    research_record_ids: Iterable[str] | None = None,
    validate_selection_replay: bool = True,
) -> dict[str, Any]:
    """Execute every source-compiled v2 obligation against one v3 scene.

    The current oracle remains source-only.  This separate evaluator joins the
    compiled targets to a validated runtime asset view and reports every typed
    outcome.  It never rewrites an expectation to match a selected pack.
    """

    from universal_scene_runtime import (
        canonical_sha256 as universal_canonical_sha256,
        validate_scene_contract as runtime_validate_scene_contract,
        validate_universal_scene_selection,
    )

    _require(isinstance(scene, Mapping), "compiled obligation scene must be an object")
    _require(
        isinstance(oracle_row, Mapping),
        "compiled obligation oracle row must be an object",
    )
    prompt = oracle_row.get("legacy_prompt_record")
    canonical_contract = oracle_row.get("canonical_scene_contract")
    canonical_projection = oracle_row.get("canonical_projection")
    runtime_expectations = oracle_row.get("runtime_expectations")
    _require(
        isinstance(prompt, Mapping), "compiled obligation legacy prompt is missing"
    )
    _require(
        isinstance(canonical_contract, Mapping),
        "compiled obligation canonical contract is missing",
    )
    _require(
        isinstance(canonical_projection, Mapping),
        "compiled obligation canonical projection is missing",
    )
    _require(
        isinstance(runtime_expectations, Mapping),
        "compiled obligation runtime expectations are missing",
    )
    request_text = str(prompt["request_ko"])
    _require(
        scene.get("scene_contract") == canonical_contract,
        f"compiled obligation scene-contract drift: {oracle_row.get('case_id')}",
    )
    runtime_validate_scene_contract(
        request_text,
        canonical_contract,
        assets=assets,
    )
    if validate_selection_replay:
        try:
            replayed = validate_universal_scene_selection(
                scene,
                request_text,
                assets,
                topic_id=str(prompt["expected_topic_id"]),
                format_id=str(prompt["expected_format"]),
                creativity=float(prompt["creativity"]),
                seed=int(prompt["seed"]),
                prior_exposure_ids=(),
            )
        except Exception as exc:
            raise ValidationFailure(
                f"compiled obligation selection replay failed: {oracle_row.get('case_id')}: {exc}"
            ) from exc
        _require(
            replayed == scene,
            f"compiled obligation selection replay drift: {oracle_row.get('case_id')}",
        )

    slots = {str(item["slot_id"]): item for item in scene["slot_states"]}
    canonical_slots = {
        str(item["slot_id"]): item for item in canonical_projection["slot_states"]
    }
    selected_roles = {
        str(item["role_id"]): item for item in scene["selected_event"]["roles"]
    }
    canonical_roles = {
        str(item["role_id"]): item for item in canonical_projection["event_roles"]
    }
    selected_entities = {
        str(item["entity_id"]): item for item in scene["identity_core"]["entities"]
    }
    canonical_entities = {
        str(item["entity_id"]): item
        for item in canonical_contract["identity_core"]["entities"]
    }
    _require(
        set(slots) == set(UNIVERSAL_SLOT_IDS)
        and set(selected_roles) == set(UNIVERSAL_EVENT_ROLE_IDS),
        "compiled obligation scene projection is incomplete",
    )
    atoms = list(scene["atoms"])
    bridges = list(scene["bridges"])
    resource_claims = list(scene["resource_claims"])
    pixel_items = list(scene["pixel_evidence_contract"]["items"])
    pixel_by_item_id = {str(item["item_id"]): item for item in pixel_items}
    claim_by_id = {str(item["claim_id"]): item for item in resource_claims}
    selected_atom_facets = {str(item["facet"]) for item in atoms}
    slot_facets = {
        "expression": {"expression", "perceived_affect"},
        "pose": {"pose", "gesture"},
        "action": {"action", "phase", "consequence"},
        "relation": {"relation", "contact"},
        "prop": {"prop", "prop_state"},
        "environment": {"environment"},
    }

    trace = scene["selection_trace"]
    eligible_count_by_facet = trace["eligible_count_by_facet"]
    eligible_candidate_ids_by_facet = trace["eligible_candidate_ids_by_facet"]
    _require(
        isinstance(eligible_count_by_facet, Mapping)
        and isinstance(eligible_candidate_ids_by_facet, Mapping)
        and set(eligible_count_by_facet) == set(UNIVERSAL_V2_ATOM_FACETS)
        and set(eligible_candidate_ids_by_facet) == set(UNIVERSAL_V2_ATOM_FACETS)
        and all(
            isinstance(value, int) and not isinstance(value, bool) and value >= 0
            for value in eligible_count_by_facet.values()
        ),
        "compiled obligation eligible facet trace is invalid",
    )
    eligible_visual_ids: set[str] = set()
    eligible_atom_facets: set[str] = set()
    for facet in UNIVERSAL_V2_ATOM_FACETS:
        candidate_ids = eligible_candidate_ids_by_facet[facet]
        _require(
            isinstance(candidate_ids, list)
            and candidate_ids == sorted(set(candidate_ids))
            and eligible_count_by_facet[facet] == len(candidate_ids),
            f"compiled obligation eligible candidate trace drift: {facet}",
        )
        for candidate_id in candidate_ids:
            candidate = assets.candidate_by_id.get(candidate_id)
            _require(
                candidate is not None
                and candidate["role"] == "visual_atom"
                and candidate["facet"] == facet,
                f"compiled obligation eligible candidate catalog drift: {candidate_id}",
            )
            eligible_visual_ids.add(str(candidate_id))
        if candidate_ids:
            eligible_atom_facets.add(facet)
    candidate_rejections = trace["candidate_rejections"]
    _require(
        isinstance(candidate_rejections, list)
        and all(
            isinstance(item, Mapping)
            and list(item) == ["candidate_id", "reason_code"]
            and isinstance(item["candidate_id"], str)
            and item["candidate_id"]
            and isinstance(item["reason_code"], str)
            and item["reason_code"]
            for item in candidate_rejections
        ),
        "compiled obligation candidate rejection trace is invalid",
    )
    rejected_visual_ids = [str(item["candidate_id"]) for item in candidate_rejections]
    _require(
        rejected_visual_ids == sorted(set(rejected_visual_ids)),
        "compiled obligation rejected candidate IDs are not sorted and unique",
    )
    all_visual_ids = {
        str(candidate_id)
        for candidate_id, candidate in assets.candidate_by_id.items()
        if candidate["role"] == "visual_atom"
    }
    _require(
        not eligible_visual_ids.intersection(rejected_visual_ids)
        and eligible_visual_ids.union(rejected_visual_ids) == all_visual_ids,
        "compiled obligation eligible/rejected candidate partition is incomplete",
    )
    _require(
        dict(trace["rejection_count_by_code"])
        == dict(
            sorted(
                Counter(
                    str(item["reason_code"]) for item in candidate_rejections
                ).items()
            )
        ),
        "compiled obligation candidate rejection counts drift",
    )

    capability_records = scene["identity_core"]["capability_capacities"]
    eligible_resource_evidence: dict[str, list[str]] = defaultdict(list)
    for record in capability_records:
        if record["state"] == "available" and int(record["capacity"]) > 0:
            eligible_resource_evidence[str(record["resource_kind"])].append(
                f"{record['entity_id']}:{record['resource_kind']}"
            )
    for resource_kind in assets.compatibility["resource_kind_ids"]:
        if str(resource_kind) in {
            "focal_primary",
            "focal_secondary",
            "foreground_salience",
            "event_peak",
            "prop_slot",
        }:
            eligible_resource_evidence[str(resource_kind)].append(
                f"scene:{resource_kind}"
            )

    # Pixel and bridge eligibility joins only the exact trace-authenticated
    # candidate IDs.  A positive facet count never makes another same-facet
    # catalog record eligible by association.
    eligible_pixel_evidence: dict[str, list[str]] = defaultdict(list)
    eligible_bridge_evidence: dict[str, list[str]] = defaultdict(list)
    for candidate_id in sorted(eligible_visual_ids):
        candidate = assets.candidate_by_id[candidate_id]
        runtime = candidate["runtime_contract"]
        for pixel in runtime["pixel_evidence"]:
            eligible_pixel_evidence[str(pixel["kind"])].append(
                f"{candidate_id}:{pixel['id']}"
            )
        for bridge_type in runtime["bridge_types"]:
            eligible_bridge_evidence[str(bridge_type)].append(str(candidate_id))

    snapshot = scene["hard_gate_snapshot"]
    _require(
        isinstance(snapshot, Mapping),
        "compiled obligation hard-gate snapshot is missing",
    )
    snapshot_without_sha = dict(snapshot)
    snapshot_digest = snapshot_without_sha.pop("snapshot_sha256", None)
    _require(
        snapshot_digest == universal_canonical_sha256(snapshot_without_sha),
        "compiled obligation hard-gate snapshot digest drift",
    )
    _require(
        dict(snapshot["asset_hashes"]) == dict(assets.asset_hashes),
        "compiled obligation hard-gate asset binding drift",
    )
    registry = assets.semantic_bindings["semantic_effect_registry"]
    _require(
        snapshot["semantic_effect_registry_sha256"]
        == universal_canonical_sha256(registry),
        "compiled obligation semantic registry binding drift",
    )
    _require(
        dict(snapshot["source_coverage"]) == dict(registry["counts"]),
        "compiled obligation semantic source coverage drift",
    )
    registry_sources = {
        (str(item["source_kind"]), str(item["source_id"])): tuple(item["effect_ids"])
        for item in registry["profiles"]
    }
    _require(
        len(registry_sources) == int(registry["counts"]["total"]),
        "compiled obligation semantic registry source coverage is not exact",
    )
    selected_source_refs = list(snapshot["selected_source_refs"])
    seen_instances: set[tuple[str, str]] = set()
    actual_occurrences: set[tuple[str, str, str | None]] = set()
    effect_profile_ids: set[str] = set()
    load_max = {axis: 0 for axis in UNIVERSAL_LOAD_AXIS_IDS}
    source_kind_order = {
        value: index for index, value in enumerate(registry["source_kind_ids"])
    }
    for item in selected_source_refs:
        instance_key = (str(item["instance_kind"]), str(item["instance_id"]))
        _require(
            instance_key not in seen_instances,
            f"compiled obligation duplicate selected source instance: {instance_key}",
        )
        seen_instances.add(instance_key)
        refs = list(item["source_profile_refs"])
        expected_ref_order = sorted(
            refs,
            key=lambda ref: (
                source_kind_order.get(str(ref["source_kind"]), 10_000),
                str(ref["source_id"]),
            ),
        )
        _require(
            refs == expected_ref_order,
            "compiled obligation selected source order drift",
        )
        for ref in refs:
            key = (str(ref["source_kind"]), str(ref["source_id"]))
            _require(
                key in registry_sources,
                f"compiled obligation unknown semantic source: {key}",
            )
            _require(
                registry_sources[key] == (),
                f"compiled obligation safe source unexpectedly owns a blocked effect: {key}",
            )
        for profile_id in item["contract_effect_profile_ids"]:
            effect_profile_ids.add(str(profile_id))
        for occurrence in item["effect_occurrences"]:
            actual_occurrences.add(
                (
                    str(occurrence["effect_id"]),
                    str(occurrence["source_profile_id"]),
                    None
                    if occurrence["subject_ref"] is None
                    else str(occurrence["subject_ref"]),
                )
            )
        for axis in UNIVERSAL_LOAD_AXIS_IDS:
            load_max[axis] = max(load_max[axis], int(item["load_vector"][axis]))
    expected_occurrences = _oracle_effect_occurrences(
        request_text,
        canonical_contract,
        selected_roles,
        assets.semantic_bindings,
    )
    _require(
        actual_occurrences == expected_occurrences,
        "compiled obligation scoped semantic effect replay drift",
    )
    _require(
        effect_profile_ids == {item[1] for item in expected_occurrences},
        "compiled obligation contract effect profile binding drift",
    )
    _require(
        snapshot["observed_effect_ids"]
        == sorted({item[0] for item in expected_occurrences}),
        "compiled obligation observed semantic effect union drift",
    )
    _require(
        dict(snapshot["semantic_load_max"]) == load_max,
        "compiled obligation semantic load maximum drift",
    )

    contract = runtime_expectations["compiled_obligation_contract"]
    _require(
        contract["schema"] == UNIVERSAL_V2_COMPILED_OBLIGATION_SCHEMA,
        "compiled obligation contract schema drift",
    )
    obligations = list(contract["obligations"])
    visual_owner_specs_by_mapping: dict[str, dict[str, Any]] = {}
    for obligation in obligations:
        if obligation["target_kind"] != "visual_candidate":
            continue
        spec = {
            "candidate_ids": tuple(str(item) for item in obligation["target_ids"]),
            "quantifier": str(obligation["quantifier"]),
            "enforcement": str(obligation["enforcement"]),
        }
        for source_ref in obligation["source_refs"]:
            mapping_id = source_ref["mapping_id"]
            if not isinstance(mapping_id, str):
                continue
            prior = visual_owner_specs_by_mapping.setdefault(mapping_id, spec)
            _require(
                prior == spec,
                f"compiled obligation visual owner target drift: {mapping_id}",
            )
    guard_sources = {
        str(item["guard_id"]): item for item in contract["guard_source_contracts"]
    }
    guard_profiles = {
        str(item["guard_id"]): str(item["predicate_id"])
        for item in assets.semantic_bindings["guard_execution_profiles"]
    }
    guard_executions = list(snapshot["guard_executions"])
    _require(
        [str(item["guard_id"]) for item in guard_executions]
        == sorted(str(item) for item in assets.compatibility["guard_candidate_ids"]),
        "compiled obligation guard execution inventory/order drift",
    )
    execution_by_id = {str(item["guard_id"]): item for item in guard_executions}
    for guard_id, execution in execution_by_id.items():
        candidate = assets.candidate_by_id[guard_id]
        runtime = candidate["runtime_contract"]
        source_contract = {
            "guard_id": guard_id,
            "role": str(candidate["role"]),
            "research_topic_ids": list(candidate["research_topic_ids"]),
            "provenance_record_ids": list(candidate["provenance_record_ids"]),
            "stage": str(runtime["stage"]),
            "violation_code": str(runtime["violation_code"]),
            "outcome": str(runtime["outcome"]),
        }
        _require(
            execution["source_candidate_id"] == guard_id
            and execution["source_contract_sha256"]
            == universal_canonical_sha256(source_contract)
            and execution["stage"] == source_contract["stage"]
            and execution["violation_code"] == source_contract["violation_code"],
            f"compiled obligation guard source drift: {guard_id}",
        )
        predicate_results = list(execution["predicate_results"])
        if execution["applicable"] is True:
            _require(
                len(predicate_results) == 1
                and predicate_results[0]["predicate_id"] == guard_profiles[guard_id]
                and isinstance(predicate_results[0]["binding_ids"], list)
                and bool(predicate_results[0]["binding_ids"])
                and len(predicate_results[0]["binding_ids"])
                == len(set(predicate_results[0]["binding_ids"])),
                f"compiled obligation applicable guard has no typed proof: {guard_id}",
            )
            passed = predicate_results[0]["passed"] is True
            expected_outcome = "pass" if passed else "block"
            expected_reason = (
                "all_guard_predicates_passed" if passed else "guard_predicate_failed"
            )
            _require(
                execution["outcome"] == expected_outcome
                and execution["reason_codes"] == [expected_reason],
                f"compiled obligation guard result drift: {guard_id}",
            )
        else:
            _require(
                predicate_results == []
                and execution["outcome"] == "not_applicable"
                and execution["reason_codes"] == ["guard_not_applicable"],
                f"compiled obligation nonapplicable guard result drift: {guard_id}",
            )
    _require(
        snapshot["hard_gate_pass"]
        is all(item["outcome"] != "block" for item in guard_executions),
        "compiled obligation hard-gate aggregate drift",
    )

    if research_record_ids is None:
        _require(
            assets.asset_dir is not None,
            "compiled obligation evaluator requires research record IDs for in-memory assets",
        )
        manifest = _load_json(
            Path(assets.asset_dir)
            / "research_evidence_universal_scene"
            / "manifest.json"
        )
        resolved_research_ids = {
            str(record["record_id"])
            for shard in manifest["shards"]
            for record in _load_jsonl(
                Path(assets.asset_dir)
                / "research_evidence_universal_scene"
                / str(shard["path"])
            )
        }
    else:
        resolved_research_ids = {str(item) for item in research_record_ids}

    def owner_atoms(
        owner_specs: Mapping[str, Mapping[str, Any]],
        *,
        require_selected: bool,
    ) -> dict[str, list[Mapping[str, Any]]]:
        resolved: dict[str, list[Mapping[str, Any]]] = {}
        for mapping_id, spec in owner_specs.items():
            candidate_ids = set(spec["candidate_ids"])
            if require_selected or spec["enforcement"] == "required":
                records = [
                    item for item in atoms if item["candidate_id"] in candidate_ids
                ]
            else:
                records = [
                    {
                        "instance_id": f"eligible:{candidate_id}",
                        "candidate_id": candidate_id,
                    }
                    for candidate_id in sorted(candidate_ids & eligible_visual_ids)
                ]
            resolved[mapping_id] = records
        return resolved

    def evidence_for_target(
        evaluator_id: str,
        target_id: str,
        target_values: list[str],
        owner_specs: Mapping[str, Mapping[str, Any]],
    ) -> tuple[bool, list[str]]:
        if evaluator_id == "canonical_slot_projection_v1":
            passed = slots.get(target_id) == canonical_slots.get(target_id)
            if target_values:
                passed = passed and slots[target_id]["value_ids"] == target_values
            return passed, [f"slot:{target_id}:{slots[target_id]['state']}"]
        if evaluator_id == "eligible_slot_v1":
            record = canonical_slots[target_id]
            return record["state"] != "closed", [f"slot:{target_id}:{record['state']}"]
        if evaluator_id == "absent_slot_materialization_v1":
            record = canonical_slots[target_id]
            materialized = sorted(selected_atom_facets & slot_facets[target_id])
            return record["state"] == "closed" and not materialized, materialized
        if evaluator_id == "required_slot_materialization_v1":
            record = canonical_slots[target_id]
            materialized = sorted(selected_atom_facets & slot_facets[target_id])
            passed = record["state"] == "fixed" or bool(materialized)
            if target_values:
                passed = passed and record["value_ids"] == target_values
            return passed, materialized or [f"slot:{target_id}:{record['state']}"]
        if evaluator_id == "canonical_event_role_projection_v1":
            contract_role = next(
                item
                for item in canonical_contract["event_roles"]
                if item["role_id"] == target_id
            )
            selected = selected_roles[target_id]
            passed = contract_role == canonical_roles[target_id]
            if contract_role["state"] == "fixed":
                passed = passed and selected["value_id"] == contract_role["value_id"]
            if contract_role["state"] == "closed":
                passed = passed and selected["value_id"] is None
            if target_values:
                passed = passed and selected["value_id"] in target_values
            return passed, [
                f"role:{target_id}:{selected['value_id']}@{selected['source_id']}"
            ]
        if evaluator_id == "eligible_event_role_v1":
            return canonical_roles[target_id]["state"] != "closed", [
                f"role:{target_id}:{canonical_roles[target_id]['state']}"
            ]
        if evaluator_id == "absent_event_role_v1":
            selected = selected_roles[target_id]
            return (
                canonical_roles[target_id]["state"] == "closed"
                and selected["value_id"] is None,
                [f"role:{target_id}:{selected['value_id']}"],
            )
        if evaluator_id == "required_event_role_v1":
            selected = selected_roles.get(target_id)
            passed = selected is not None and selected["value_id"] is not None
            if target_values:
                passed = passed and selected["value_id"] in target_values
            if owner_specs:
                evidence: list[str] = []
                owner_passed = True
                for mapping_id, records in owner_atoms(
                    owner_specs,
                    require_selected=True,
                ).items():
                    local = [
                        f"{mapping_id}:{item['instance_id']}:{target_id}:{binding['node_id']}"
                        for item in records
                        for binding in item["bindings"]
                        if selected is not None
                        and selected["value_id"] is not None
                        and binding["role_id"] == target_id
                        and binding["requirement"] == "required"
                        and binding["node_id"] == selected["value_id"]
                    ]
                    owner_passed = owner_passed and bool(local)
                    evidence.extend(local)
                return passed and owner_passed, evidence
            return passed, [] if selected is None else [
                f"role:{target_id}:{selected['value_id']}@{selected['source_id']}"
            ]
        if evaluator_id == "canonical_context_profile_projection_v1":
            value = scene["context_profile"].get(target_id)
            expected = canonical_contract["context_profile"].get(target_id)
            passed = value == expected
            if target_values:
                passed = passed and value in target_values
            return passed, [f"context:{target_id}:{value}"]
        if evaluator_id == "canonical_embodiment_profile_projection_v1":
            selected = selected_entities.get(target_id)
            canonical = canonical_entities.get(target_id)
            passed = selected is not None and selected == canonical
            profile_id = None if selected is None else selected["embodiment_profile_id"]
            if target_values:
                passed = passed and profile_id in target_values
            return passed, [f"embodiment:{target_id}:{profile_id}"]
        if evaluator_id == "eligible_visual_candidate_v1":
            passed = target_id in eligible_visual_ids
            return passed, [f"eligible_candidate:{target_id}"] if passed else []
        if evaluator_id == "required_visual_candidate_v1":
            evidence = [
                f"{item['instance_id']}:{item['candidate_id']}"
                for item in atoms
                if item["candidate_id"] == target_id
            ]
            return bool(evidence), evidence
        if evaluator_id == "eligible_atom_facet_v1":
            if owner_specs:
                evidence: list[str] = []
                passed = True
                for mapping_id, records in owner_atoms(
                    owner_specs,
                    require_selected=False,
                ).items():
                    local = [
                        f"{mapping_id}:{item['candidate_id']}"
                        for item in records
                        if assets.candidate_by_id[item["candidate_id"]]["facet"]
                        == target_id
                    ]
                    passed = passed and bool(local)
                    evidence.extend(local)
                return passed, evidence
            return target_id in eligible_atom_facets, [
                f"eligible_count:{target_id}:{eligible_count_by_facet.get(target_id, 0)}"
            ]
        if evaluator_id == "absent_atom_facet_v1":
            evidence = [
                f"{item['instance_id']}:{item['candidate_id']}"
                for item in atoms
                if item["facet"] == target_id
            ]
            return not evidence, evidence
        if evaluator_id == "required_atom_facet_v1":
            if owner_specs:
                evidence = []
                passed = True
                for mapping_id, records in owner_atoms(
                    owner_specs,
                    require_selected=True,
                ).items():
                    local = [
                        f"{mapping_id}:{item['instance_id']}:{item['candidate_id']}"
                        for item in records
                        if item["facet"] == target_id
                    ]
                    passed = passed and bool(local)
                    evidence.extend(local)
                return passed, evidence
            evidence = [
                f"{item['instance_id']}:{item['candidate_id']}"
                for item in atoms
                if item["facet"] == target_id
            ]
            return bool(evidence), evidence
        if evaluator_id == "eligible_resource_kind_v1":
            if owner_specs:
                evidence = []
                capacity_evidence = list(eligible_resource_evidence.get(target_id, []))
                if target_values:
                    capacity_evidence = [
                        item
                        for item in capacity_evidence
                        if item.split(":", 1)[0] in target_values
                    ]
                passed = bool(capacity_evidence)
                evidence.extend(f"capacity:{item}" for item in capacity_evidence)
                for mapping_id, records in owner_atoms(
                    owner_specs,
                    require_selected=False,
                ).items():
                    local = [
                        f"{mapping_id}:{item['candidate_id']}:{target_id}"
                        for item in records
                        if any(
                            claim[0] == target_id
                            for claim in assets.candidate_by_id[item["candidate_id"]][
                                "runtime_contract"
                            ]["resource_claims"]
                        )
                    ]
                    passed = passed and bool(local)
                    evidence.extend(local)
                return passed, evidence
            evidence = eligible_resource_evidence.get(target_id, [])
            if target_values:
                evidence = [
                    item for item in evidence if item.split(":", 1)[0] in target_values
                ]
            return bool(evidence), list(evidence)
        if evaluator_id == "absent_resource_kind_v1":
            evidence = [
                f"{item['claim_id']}:{item['owner_id']}"
                for item in resource_claims
                if item["resource_kind"] == target_id
                and (not target_values or item["owner_id"] in target_values)
            ]
            return not evidence, evidence
        if evaluator_id == "required_resource_kind_v1":
            if owner_specs:
                evidence = []
                passed = True
                for mapping_id, records in owner_atoms(
                    owner_specs,
                    require_selected=True,
                ).items():
                    local = [
                        f"{mapping_id}:{claim_id}:{claim_by_id[claim_id]['owner_id']}"
                        for item in records
                        for claim_id in item["resource_claim_ids"]
                        if claim_id in claim_by_id
                        and claim_by_id[claim_id]["claimant_id"] == item["instance_id"]
                        and claim_by_id[claim_id]["resource_kind"] == target_id
                        and (
                            not target_values
                            or claim_by_id[claim_id]["owner_id"] in target_values
                        )
                    ]
                    passed = passed and bool(local)
                    evidence.extend(local)
                return passed, evidence
            evidence = [
                f"{item['claim_id']}:{item['owner_id']}"
                for item in resource_claims
                if item["resource_kind"] == target_id
                and (not target_values or item["owner_id"] in target_values)
            ]
            return bool(evidence), evidence
        if evaluator_id == "eligible_runtime_bridge_type_v1":
            evidence = eligible_bridge_evidence.get(target_id, [])
            return bool(evidence), list(evidence)
        if evaluator_id == "required_runtime_bridge_type_v1":
            if owner_specs:
                evidence = []
                passed = True
                for mapping_id, records in owner_atoms(
                    owner_specs,
                    require_selected=True,
                ).items():
                    local: list[str] = []
                    for owner_atom in records:
                        owner_candidate = assets.candidate_by_id[
                            str(owner_atom["candidate_id"])
                        ]
                        if (
                            target_id
                            not in owner_candidate["runtime_contract"]["bridge_types"]
                        ):
                            continue
                        instance_id = str(owner_atom["instance_id"])
                        for bridge in bridges:
                            if bridge[
                                "bridge_type"
                            ] != target_id or instance_id not in {
                                str(bridge["from_node_id"]),
                                str(bridge["to_node_id"]),
                            }:
                                continue
                            carrier = assets.candidate_by_id.get(
                                str(bridge["candidate_id"])
                            )
                            if (
                                carrier is None
                                or carrier["role"] != "visual_atom"
                                or target_id
                                not in carrier["runtime_contract"]["bridge_types"]
                            ):
                                continue
                            expected_pixel_ids: list[str] = []
                            pixels_match = True
                            for pixel in carrier["runtime_contract"]["pixel_evidence"]:
                                item_id = (
                                    f"pixel_bridge_{bridge['bridge_id']}_"
                                    f"{pixel['id'].replace('::', '_')}"
                                )
                                expected_pixel_ids.append(item_id)
                                item = pixel_by_item_id.get(item_id)
                                if (
                                    item is None
                                    or item["source_kind"] != "bridge"
                                    or item["source_id"] != bridge["bridge_id"]
                                    or item["kind"] != pixel["kind"]
                                    or item["minimum_scale_ids"]
                                    != pixel["minimum_scale_ids"]
                                ):
                                    pixels_match = False
                            if (
                                pixels_match
                                and bridge["pixel_evidence_ids"] == expected_pixel_ids
                            ):
                                local.append(
                                    f"{mapping_id}:{bridge['bridge_id']}:"
                                    f"{bridge['candidate_id']}:{instance_id}"
                                )
                    passed = passed and bool(local)
                    evidence.extend(local)
                return passed, evidence
            evidence = [
                str(item["bridge_id"])
                for item in bridges
                if item["bridge_type"] == target_id
            ]
            return bool(evidence), evidence
        if evaluator_id == "eligible_pixel_evidence_kind_v1":
            if owner_specs:
                evidence = []
                passed = True
                for mapping_id, records in owner_atoms(
                    owner_specs,
                    require_selected=False,
                ).items():
                    local = [
                        f"{mapping_id}:{item['candidate_id']}:{pixel['id']}"
                        for item in records
                        for pixel in assets.candidate_by_id[item["candidate_id"]][
                            "runtime_contract"
                        ]["pixel_evidence"]
                        if pixel["kind"] == target_id
                    ]
                    passed = passed and bool(local)
                    evidence.extend(local)
                return passed, evidence
            evidence = eligible_pixel_evidence.get(target_id, [])
            return bool(evidence), list(evidence)
        if evaluator_id == "required_pixel_evidence_kind_v1":
            if owner_specs:
                evidence = []
                passed = True
                for mapping_id, records in owner_atoms(
                    owner_specs,
                    require_selected=True,
                ).items():
                    local = [
                        f"{mapping_id}:{item['instance_id']}:{pixel_id}"
                        for item in records
                        for pixel_id in item["pixel_evidence_ids"]
                        if pixel_id in pixel_by_item_id
                        and pixel_by_item_id[pixel_id]["kind"] == target_id
                        and pixel_by_item_id[pixel_id]["source_kind"] == "atom"
                        and pixel_by_item_id[pixel_id]["source_id"]
                        == item["instance_id"]
                    ]
                    passed = passed and bool(local)
                    evidence.extend(local)
                return passed, evidence
            evidence = [
                str(item["item_id"])
                for item in pixel_items
                if item["kind"] == target_id
            ]
            return bool(evidence), evidence
        if evaluator_id == "required_guard_binding_v1":
            execution = execution_by_id.get(target_id)
            source = guard_sources.get(target_id)
            candidate = assets.candidate_by_id.get(target_id)
            passed = (
                execution is not None and source is not None and candidate is not None
            )
            if passed:
                runtime = candidate["runtime_contract"]
                actual_source = {
                    "guard_id": target_id,
                    "role": str(candidate["role"]),
                    "research_topic_ids": list(candidate["research_topic_ids"]),
                    "provenance_record_ids": list(candidate["provenance_record_ids"]),
                    "stage": str(runtime["stage"]),
                    "violation_code": str(runtime["violation_code"]),
                    "outcome": str(runtime["outcome"]),
                }
                passed = (
                    actual_source == source
                    and target_id in assets.compatibility["guard_candidate_ids"]
                    and set(source["provenance_record_ids"]) <= resolved_research_ids
                    and execution["applicable"] is True
                    and execution["outcome"] == "pass"
                    and bool(execution["predicate_results"])
                )
                if passed and target_values:
                    binding_ids = {
                        str(binding_id)
                        for predicate in execution["predicate_results"]
                        for binding_id in predicate["binding_ids"]
                    }
                    scoped_binding_ids = set(binding_ids)
                    for binding_id in binding_ids:
                        claim = claim_by_id.get(binding_id)
                        if claim is not None:
                            scoped_binding_ids.add(str(claim["owner_id"]))
                        prefix = binding_id.split(":", 1)[0]
                        if prefix in selected_entities:
                            scoped_binding_ids.add(prefix)
                    passed = set(target_values) <= scoped_binding_ids
            return passed, [] if execution is None else [
                f"guard:{target_id}:{execution['outcome']}:{execution['applicable']}"
            ]
        if evaluator_id == "absent_blocked_semantic_v1":
            evidence = [
                f"{effect_id}:{subject_ref}"
                for effect_id, _profile_id, subject_ref in actual_occurrences
                if effect_id == target_id
                and (not target_values or subject_ref in target_values)
            ]
            return not evidence, sorted(evidence)
        if evaluator_id == "zero_semantic_load_axis_v1":
            evidence = [
                f"{item['instance_kind']}:{item['instance_id']}:{item['load_vector'][target_id]}"
                for item in selected_source_refs
                if int(item["load_vector"][target_id]) != 0
            ]
            return load_max[target_id] == 0 and not evidence, evidence
        raise ValidationFailure(f"unsupported compiled evaluator: {evaluator_id}")

    results: list[dict[str, Any]] = []
    by_mapping: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for obligation in obligations:
        evaluator_id = str(obligation["evaluator_id"])
        target_values = [str(item) for item in obligation["target_values"]]
        obligation_mapping_ids = {
            str(source_ref["mapping_id"])
            for source_ref in obligation["source_refs"]
            if isinstance(source_ref["mapping_id"], str)
        }
        # A reviewed visual-candidate target owns its material atom, pixel,
        # resource, role-binding, and runtime-bridge siblings.  The latter two
        # require serialized graph identity, not a same-role or same-type
        # record elsewhere in the scene.
        owner_join_kinds = {
            "atom_facet",
            "event_role",
            "pixel_evidence_kind",
            "resource_kind",
            "runtime_bridge_type",
        }
        owner_specs = (
            {
                mapping_id: visual_owner_specs_by_mapping[mapping_id]
                for mapping_id in sorted(obligation_mapping_ids)
                if mapping_id in visual_owner_specs_by_mapping
            }
            if obligation["target_kind"] in owner_join_kinds
            else {}
        )
        target_results = []
        for target_id in obligation["target_ids"]:
            passed, evidence_ids = evidence_for_target(
                evaluator_id,
                str(target_id),
                target_values,
                owner_specs,
            )
            target_results.append(
                {
                    "target_id": str(target_id),
                    "passed": passed,
                    "evidence_ids": evidence_ids,
                }
            )
        passed = (
            all(item["passed"] for item in target_results)
            if obligation["quantifier"] == "all"
            else any(item["passed"] for item in target_results)
        )
        result = {
            "obligation_id": str(obligation["obligation_id"]),
            "evaluator_id": evaluator_id,
            "target_kind": str(obligation["target_kind"]),
            "enforcement": str(obligation["enforcement"]),
            "quantifier": str(obligation["quantifier"]),
            "passed": passed,
            "target_results": target_results,
            "source_refs": copy.deepcopy(obligation["source_refs"]),
        }
        results.append(result)
        for source_ref in obligation["source_refs"]:
            mapping_id = source_ref["mapping_id"]
            if isinstance(mapping_id, str):
                by_mapping[mapping_id].append(result)

    # A guard proves enforcement mechanics only.  It cannot mask a failed
    # material/absence obligation from the same reviewed legacy mapping.
    for result in results:
        if result["evaluator_id"] != "required_guard_binding_v1":
            continue
        mapping_ids = {
            source_ref["mapping_id"]
            for source_ref in result["source_refs"]
            if isinstance(source_ref["mapping_id"], str)
        }
        failed_material = sorted(
            {
                sibling["obligation_id"]
                for mapping_id in mapping_ids
                for sibling in by_mapping[mapping_id]
                if sibling["evaluator_id"] != "required_guard_binding_v1"
                and not sibling["passed"]
            }
        )
        if failed_material:
            result["passed"] = False
            result["target_results"].append(
                {
                    "target_id": "material_outcome_bindings",
                    "passed": False,
                    "evidence_ids": failed_material,
                }
            )

    failures = [item for item in results if not item["passed"]]
    evaluator_counts = Counter(item["evaluator_id"] for item in results)
    return {
        "schema": "subculture_illustration_universal_scene_obligation_evaluation/v1",
        "case_id": str(oracle_row["case_id"]),
        "status": "pass" if not failures else "fail",
        "obligation_count": len(results),
        "passed_count": len(results) - len(failures),
        "failed_count": len(failures),
        "evaluator_counts": dict(sorted(evaluator_counts.items())),
        "results": results,
        "failures": failures,
    }


def validate_universal_scene_holdouts(
    asset_dir: Path,
    research: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate the frozen prompt, semantic-contract, and render holdouts."""

    baseline = _load_json(asset_dir / "universal_scene_baseline_v1.json")
    _require(
        baseline.get("schema") == "subculture_illustration_universal_scene_baseline/v1",
        "universal scene baseline schema mismatch",
    )
    _require(
        baseline.get("baseline_ref") == "main@3185403d9e40",
        "universal scene baseline reference drift",
    )
    legacy_contracts = baseline.get("legacy_contracts")
    _require(
        isinstance(legacy_contracts, dict)
        and set(legacy_contracts)
        == {
            "candidate_pack_versions",
            "current_runtime_sha256",
            "current_audit_sha256",
            "generator_cli_sha256",
            "audit_cli_sha256",
        }
        and legacy_contracts.get("candidate_pack_versions")
        == [LEGACY_CONTRACT_VERSION, HISTORICAL_CONTRACT_VERSION_V2],
        "universal baseline legacy contract list drift",
    )
    frozen_legacy_hashes = {
        "current_runtime_sha256": V2_PROMPT_QUALIFICATION_RUNTIME_SHA256,
        "current_audit_sha256": V2_PROMPT_QUALIFICATION_AUDIT_SHA256,
        "generator_cli_sha256": PRE_UNIVERSAL_GENERATOR_CLI_SHA256,
        "audit_cli_sha256": PRE_UNIVERSAL_AUDIT_CLI_SHA256,
    }
    for field, expected_digest in frozen_legacy_hashes.items():
        _require(
            legacy_contracts.get(field) == expected_digest,
            f"universal baseline legacy hash drift: {field}",
        )
    v2_qualification_manifest = _load_json(
        asset_dir / "prompt_qualification_v2" / "manifest.json"
    )
    _require(
        v2_qualification_manifest.get("runtime_sha256")
        == V2_PROMPT_QUALIFICATION_RUNTIME_SHA256
        and v2_qualification_manifest.get("audit_sha256")
        == V2_PROMPT_QUALIFICATION_AUDIT_SHA256,
        "universal baseline v2 qualification hash binding drift",
    )
    for section_name in ("authorial_assets", "qualification_manifests"):
        section = baseline.get(section_name)
        _require(
            isinstance(section, dict) and section,
            f"universal baseline {section_name} missing",
        )
        for relative_path, expected_digest in section.items():
            path = asset_dir / relative_path
            _require(
                path.is_file(), f"universal baseline path missing: {relative_path}"
            )
            _require(
                _sha256(path) == expected_digest,
                f"immutable historical asset drift: {relative_path}",
            )
    prompt_path = asset_dir / "universal_scene_prompt_holdout_v1.jsonl"
    contract_path = asset_dir / "universal_scene_contract_holdout_v1.jsonl"
    render_path = asset_dir / "render_universal_scene_quality_holdout_v1.jsonl"
    frozen_paths = {
        prompt_path.name: prompt_path,
        contract_path.name: contract_path,
        render_path.name: render_path,
    }
    frozen_manifest = baseline.get("new_frozen_holdouts")
    _require(
        isinstance(frozen_manifest, dict), "universal frozen holdout manifest missing"
    )
    for filename, path in frozen_paths.items():
        entry = frozen_manifest.get(filename)
        _require(isinstance(entry, dict), f"universal baseline omits {filename}")
        _require(
            _sha256(path) == entry.get("sha256"),
            f"universal frozen holdout hash mismatch: {filename}",
        )

    prompt_rows = _load_jsonl(prompt_path)
    contract_rows = _load_jsonl(contract_path)
    render_rows = _load_jsonl(render_path)
    _require(
        len(prompt_rows) == frozen_manifest[prompt_path.name].get("record_count") == 24,
        "universal prompt holdout must contain 24 rows",
    )
    _require(
        len(contract_rows)
        == frozen_manifest[contract_path.name].get("record_count")
        == 24,
        "universal scene-contract holdout must contain 24 rows",
    )
    _require(
        len(render_rows) == frozen_manifest[render_path.name].get("record_count") == 6,
        "universal render holdout must contain six rows",
    )

    prompt_keys = {
        "schema",
        "case_id",
        "request_ko",
        "expected_topic_id",
        "expected_format",
        "seed",
        "creativity",
        "identity_core",
        "expected_slot_states",
        "expected_event_frame",
        "semantic_distance_expectation",
        "prop_expectation",
        "coverage_topic_ids",
        "required_pack_evidence",
        "forbidden_overwrite",
        "frozen_before_implementation",
    }
    prompt_by_case: dict[str, dict[str, Any]] = {}
    coverage_topics: set[str] = set()
    for row in prompt_rows:
        _require(
            set(row) == prompt_keys,
            f"universal prompt holdout field mismatch: {row.get('case_id')}",
        )
        _require(
            row.get("schema") == UNIVERSAL_SCENE_HOLDOUT_SCHEMA,
            "universal prompt holdout schema mismatch",
        )
        case_id = row.get("case_id")
        _require(
            isinstance(case_id, str) and case_id,
            "universal prompt holdout case ID missing",
        )
        _require(
            case_id not in prompt_by_case, f"duplicate universal prompt case: {case_id}"
        )
        _require(
            isinstance(row.get("request_ko"), str) and row["request_ko"],
            f"{case_id} request missing",
        )
        _require(
            isinstance(row.get("seed"), int) and not isinstance(row["seed"], bool),
            f"{case_id} seed invalid",
        )
        _require(
            isinstance(row.get("creativity"), (int, float))
            and not isinstance(row["creativity"], bool)
            and 0.0 <= float(row["creativity"]) <= 1.0,
            f"{case_id} creativity invalid",
        )
        _require(
            row.get("frozen_before_implementation") is True, f"{case_id} was not frozen"
        )
        slot_states = row.get("expected_slot_states")
        _require(
            isinstance(slot_states, dict)
            and list(slot_states) == UNIVERSAL_SLOT_IDS
            and set(slot_states.values()) <= {"fixed", "closed", "open"},
            f"{case_id} expected slot-state contract mismatch",
        )
        distance = row.get("semantic_distance_expectation")
        _require(
            isinstance(distance, dict)
            and set(distance)
            == {"band", "max_remote_candidates", "required_bridge_types"}
            and distance.get("band") in {"near", "middle", "far"}
            and distance.get("max_remote_candidates") in {0, 1},
            f"{case_id} semantic-distance expectation mismatch",
        )
        _strings(
            distance.get("required_bridge_types"),
            f"{case_id}.required_bridge_types",
            minimum=1,
        )
        prop = row.get("prop_expectation")
        _require(
            isinstance(prop, dict)
            and set(prop) == {"policy", "load", "named_prop"}
            and prop.get("policy") in {"optional_single", "required_exact", "forbidden"}
            and prop.get("load") in {"none", "low", "medium", "high"},
            f"{case_id} prop expectation mismatch",
        )
        for field in ("required_pack_evidence", "forbidden_overwrite"):
            _strings(row.get(field), f"{case_id}.{field}", minimum=1)
        topics = _strings(
            row.get("coverage_topic_ids"), f"{case_id}.coverage_topic_ids", minimum=1
        )
        coverage_topics.update(topics)
        prompt_by_case[case_id] = row
    if research is not None:
        _require(
            coverage_topics == set(research["topic_ids"]),
            "universal prompt holdout must cover all 20 research topics",
        )
    else:
        _require(
            len(coverage_topics) == 20, "universal prompt holdout must cover 20 topics"
        )

    same_core = prompt_rows[:3]
    _require(
        [row["case_id"] for row in same_core]
        == [
            "universal_scene_01_same_core_low",
            "universal_scene_02_same_core_mid",
            "universal_scene_03_same_core_high",
        ],
        "same-core creativity trio order drift",
    )
    for field in (
        "request_ko",
        "seed",
        "identity_core",
        "expected_topic_id",
        "expected_format",
    ):
        _require(
            len(
                {
                    json.dumps(row[field], ensure_ascii=False, sort_keys=True)
                    for row in same_core
                }
            )
            == 1,
            f"same-core creativity trio changed {field}",
        )
    _require(
        [float(row["creativity"]) for row in same_core] == [0.2, 0.5, 0.85],
        "same-core creativity values drift",
    )
    _require(
        [row["semantic_distance_expectation"]["band"] for row in same_core]
        == ["near", "middle", "far"],
        "same-core target distance bands drift",
    )
    named_props = {
        row["prop_expectation"]["named_prop"]
        for row in prompt_rows
        if row["prop_expectation"].get("named_prop")
    }
    _require(
        {"apple", "small_hammer", "decommissioned_machine_gun"} <= named_props,
        "universal holdout lacks apple, hammer, or decommissioned-machine-gun coverage",
    )

    _require(
        {row.get("case_id") for row in contract_rows} == set(prompt_by_case),
        "scene-contract holdout case coverage mismatch",
    )
    entity_ids_seen = 0
    fixed_literal_count = 0
    closed_literal_count = 0
    contract_by_case: dict[str, dict[str, Any]] = {}
    for wrapper in contract_rows:
        _require(
            set(wrapper) == {"schema", "case_id", "scene_contract"}
            and wrapper.get("schema") == UNIVERSAL_SCENE_CONTRACT_HOLDOUT_SCHEMA,
            f"scene-contract wrapper mismatch: {wrapper.get('case_id')}",
        )
        case_id = wrapper["case_id"]
        request = prompt_by_case[case_id]["request_ko"]
        contract = wrapper.get("scene_contract")
        _require(isinstance(contract, dict), f"{case_id} scene contract missing")
        _require(
            set(contract)
            == {
                "schema",
                "request_text_sha256",
                "identity_core",
                "slot_states",
                "event_roles",
                "context_profile",
            },
            f"{case_id} scene-contract top-level fields mismatch",
        )
        _require(
            contract.get("schema") == UNIVERSAL_SCENE_CONTRACT_SCHEMA,
            f"{case_id} scene-contract schema mismatch",
        )
        _require(
            contract.get("request_text_sha256")
            == hashlib.sha256(request.encode("utf-8")).hexdigest(),
            f"{case_id} request hash mismatch",
        )
        identity = contract.get("identity_core")
        _require(
            isinstance(identity, dict)
            and set(identity) == {"entities", "scene_facts", "forbidden_facts"},
            f"{case_id} identity-core shape mismatch",
        )
        entities = identity.get("entities")
        _require(
            isinstance(entities, list) and entities,
            f"{case_id} must declare an identity entity",
        )
        local_entity_ids: set[str] = set()
        for entity in entities:
            _require(
                isinstance(entity, dict)
                and set(entity)
                == {
                    "entity_id",
                    "quantity",
                    "embodiment_profile_id",
                    "feature_facts",
                    "capabilities",
                },
                f"{case_id} entity shape mismatch",
            )
            entity_id = entity.get("entity_id")
            _require(
                isinstance(entity_id, str)
                and entity_id
                and entity_id not in local_entity_ids,
                f"{case_id} entity ID mismatch",
            )
            local_entity_ids.add(entity_id)
            _require(
                isinstance(entity.get("quantity"), int)
                and not isinstance(entity["quantity"], bool)
                and entity["quantity"] >= 1,
                f"{case_id}.{entity_id} quantity invalid",
            )
            _require(
                isinstance(entity.get("embodiment_profile_id"), str)
                and entity["embodiment_profile_id"],
                f"{case_id}.{entity_id} embodiment missing",
            )
            facts = entity.get("feature_facts")
            capabilities = entity.get("capabilities")
            _require(
                isinstance(facts, list) and facts,
                f"{case_id}.{entity_id} feature facts missing",
            )
            _require(
                isinstance(capabilities, list),
                f"{case_id}.{entity_id} capabilities invalid",
            )
            fact_ids: set[str] = set()
            for fact in facts:
                _require(
                    isinstance(fact, dict) and set(fact) == {"id", "request_phrases"},
                    f"{case_id} feature fact shape mismatch",
                )
                _require(
                    isinstance(fact.get("id"), str) and fact["id"] not in fact_ids,
                    f"{case_id} feature fact ID mismatch",
                )
                fact_ids.add(fact["id"])
                _literal_phrases(
                    fact.get("request_phrases"),
                    request,
                    f"{case_id}.{fact['id']}",
                    minimum=1,
                )
            capability_ids: set[str] = set()
            for capability in capabilities:
                _require(
                    isinstance(capability, dict)
                    and set(capability)
                    == {"id", "capacity", "state", "source", "source_fact_id"},
                    f"{case_id} capability shape mismatch",
                )
                capability_id = capability.get("id")
                _require(
                    isinstance(capability_id, str)
                    and capability_id
                    and capability_id not in capability_ids,
                    f"{case_id} duplicate capability",
                )
                capability_ids.add(capability_id)
                _require(
                    isinstance(capability.get("capacity"), int)
                    and not isinstance(capability["capacity"], bool)
                    and capability["capacity"] >= 0,
                    f"{case_id}.{capability_id} capacity invalid",
                )
                _require(
                    capability.get("state") in {"available", "unavailable"},
                    f"{case_id}.{capability_id} state invalid",
                )
                _require(
                    capability.get("source") in {"explicit", "embodiment_profile"},
                    f"{case_id}.{capability_id} source invalid",
                )
                _require(
                    isinstance(capability.get("source_fact_id"), str)
                    and capability["source_fact_id"],
                    f"{case_id}.{capability_id} source fact missing",
                )
        entity_ids_seen += len(local_entity_ids)
        for group_name in ("scene_facts", "forbidden_facts"):
            facts = identity.get(group_name)
            _require(isinstance(facts, list), f"{case_id}.{group_name} must be a list")
            fact_ids: set[str] = set()
            for fact in facts:
                _require(
                    isinstance(fact, dict) and set(fact) == {"id", "request_phrases"},
                    f"{case_id}.{group_name} fact shape mismatch",
                )
                _require(
                    isinstance(fact.get("id"), str) and fact["id"] not in fact_ids,
                    f"{case_id}.{group_name} fact ID mismatch",
                )
                fact_ids.add(fact["id"])
                _literal_phrases(
                    fact.get("request_phrases"),
                    request,
                    f"{case_id}.{fact['id']}",
                    minimum=1,
                )

        slots = contract.get("slot_states")
        _require(
            isinstance(slots, list)
            and [slot.get("slot_id") for slot in slots] == UNIVERSAL_SLOT_IDS,
            f"{case_id} slot order mismatch",
        )
        for slot in slots:
            _require(
                set(slot) == {"slot_id", "state", "value_ids", "request_phrases"},
                f"{case_id}.{slot.get('slot_id')} slot shape mismatch",
            )
            state = slot.get("state")
            _require(
                state in {"fixed", "closed", "open"},
                f"{case_id}.{slot['slot_id']} state invalid",
            )
            values = slot.get("value_ids")
            _require(
                isinstance(values, list)
                and all(isinstance(value, str) and value for value in values),
                f"{case_id}.{slot['slot_id']} values invalid",
            )
            phrases = slot.get("request_phrases")
            if state == "open":
                _require(
                    values == [] and phrases == [],
                    f"{case_id}.{slot['slot_id']} open slot contains an inferred value",
                )
            elif state == "fixed":
                _require(values, f"{case_id}.{slot['slot_id']} fixed slot has no value")
                fixed_literal_count += len(
                    _literal_phrases(
                        phrases, request, f"{case_id}.{slot['slot_id']}", minimum=1
                    )
                )
            else:
                _require(
                    values == [],
                    f"{case_id}.{slot['slot_id']} closed slot contains a value",
                )
                closed_literal_count += len(
                    _literal_phrases(
                        phrases, request, f"{case_id}.{slot['slot_id']}", minimum=1
                    )
                )

        roles = contract.get("event_roles")
        _require(
            isinstance(roles, list)
            and [role.get("role_id") for role in roles] == UNIVERSAL_EVENT_ROLE_IDS,
            f"{case_id} event-role order mismatch",
        )
        for role in roles:
            _require(
                set(role) == {"role_id", "state", "value_id", "request_phrases"},
                f"{case_id}.{role.get('role_id')} role shape mismatch",
            )
            state = role.get("state")
            _require(
                state in {"fixed", "closed", "open"},
                f"{case_id}.{role['role_id']} state invalid",
            )
            if state == "open":
                _require(
                    role.get("value_id") is None and role.get("request_phrases") == [],
                    f"{case_id}.{role['role_id']} open role contains inference",
                )
            elif state == "fixed":
                _require(
                    isinstance(role.get("value_id"), str) and role["value_id"],
                    f"{case_id}.{role['role_id']} fixed role value missing",
                )
                fixed_literal_count += len(
                    _literal_phrases(
                        role.get("request_phrases"),
                        request,
                        f"{case_id}.{role['role_id']}",
                        minimum=1,
                    )
                )
            else:
                _require(
                    role.get("value_id") is None,
                    f"{case_id}.{role['role_id']} closed role contains a value",
                )
                closed_literal_count += len(
                    _literal_phrases(
                        role.get("request_phrases"),
                        request,
                        f"{case_id}.{role['role_id']}",
                        minimum=1,
                    )
                )

        context = contract.get("context_profile")
        _require(
            isinstance(context, dict)
            and set(context)
            == {"theme_tags", "era_technology", "tone", "violence", "social", "scale"},
            f"{case_id} context profile mismatch",
        )
        _require(
            isinstance(context.get("theme_tags"), list), f"{case_id} theme tags invalid"
        )
        _require(
            context.get("violence")
            in {"closed", "nonviolent", "contextual", "active", "unknown"},
            f"{case_id} violence context invalid",
        )
        _require(
            context.get("social") in {"solo", "dyad", "ensemble", "unknown"},
            f"{case_id} social context invalid",
        )
        _require(
            context.get("scale") in {"intimate", "room", "site", "world", "unknown"},
            f"{case_id} scale context invalid",
        )
        contract_by_case[case_id] = contract
    _require(
        contract_by_case[same_core[0]["case_id"]]
        == contract_by_case[same_core[1]["case_id"]]
        == contract_by_case[same_core[2]["case_id"]],
        "same-core creativity trio must use the exact same scene contract",
    )

    render_keys = {
        "schema",
        "case_id",
        "request_ko",
        "expected_topic_id",
        "format_profile",
        "seed",
        "creativity",
        "identity_core_focus",
        "event_focus",
        "expression_channel_focus",
        "contact_focus",
        "bridge_focus",
        "required_pixel_focus",
        "thumbnail_checks",
        "forbidden_pixel_convergence",
        "initial_generation_limit",
        "tool_failure_same_prompt_retry_limit",
        "pixel_repair_limit",
        "frozen_before_implementation",
    }
    render_case_ids: set[str] = set()
    for row in render_rows:
        _require(
            set(row) == render_keys
            and row.get("schema") == UNIVERSAL_RENDER_HOLDOUT_SCHEMA,
            f"universal render holdout shape mismatch: {row.get('case_id')}",
        )
        case_id = row.get("case_id")
        _require(
            isinstance(case_id, str) and case_id not in render_case_ids,
            "universal render case ID mismatch",
        )
        render_case_ids.add(case_id)
        _require(
            row.get("initial_generation_limit") == 1,
            f"{case_id} initial image limit drift",
        )
        _require(
            row.get("tool_failure_same_prompt_retry_limit") == 3,
            f"{case_id} same-prompt retry limit drift",
        )
        _require(
            row.get("pixel_repair_limit") == 1, f"{case_id} pixel repair limit drift"
        )
        _require(
            row.get("frozen_before_implementation") is True, f"{case_id} was not frozen"
        )
        for field in (
            "identity_core_focus",
            "expression_channel_focus",
            "contact_focus",
            "bridge_focus",
            "required_pixel_focus",
            "thumbnail_checks",
            "forbidden_pixel_convergence",
        ):
            _strings(row.get(field), f"{case_id}.{field}", minimum=1)
        event_focus = row.get("event_focus")
        _require(
            isinstance(event_focus, dict)
            and "actor" in event_focus
            and "action" in event_focus,
            f"{case_id} event focus incomplete",
        )
    current_oracle_v2 = validate_universal_scene_current_oracle_v2(asset_dir)
    return {
        "prompt_case_count": len(prompt_rows),
        "scene_contract_case_count": len(contract_rows),
        "render_case_count": len(render_rows),
        "covered_topic_count": len(coverage_topics),
        "identity_entity_count": entity_ids_seen,
        "fixed_literal_count": fixed_literal_count,
        "closed_literal_count": closed_literal_count,
        "prompt_holdout_sha256": _sha256(prompt_path),
        "scene_contract_holdout_sha256": _sha256(contract_path),
        "render_holdout_sha256": _sha256(render_path),
        "prompt_rows": prompt_rows,
        "scene_contracts_by_case": contract_by_case,
        "current_oracle_v2": current_oracle_v2,
    }


def _canonical_photo_pack_id(pack: Mapping[str, Any]) -> str:
    hashable = dict(pack)
    hashable["pack_id"] = None
    return hashlib.sha256(canonical_json_bytes(hashable)).hexdigest()[:16]


def _public_photo_candidate_count(pack: Mapping[str, Any]) -> int:
    presets = pack.get("presets")
    slots = pack.get("slots")
    _require(
        isinstance(presets, list) and isinstance(slots, dict),
        "photo baseline pack shape mismatch",
    )
    return len(presets) + sum(
        len(slot["candidates"])
        for slot in slots.values()
        if isinstance(slot, dict) and isinstance(slot.get("candidates"), list)
    )


def validate_photo_regression_baseline(asset_dir: Path) -> dict[str, Any]:
    """Validate immutable photo history plus the current sibling boundary."""

    historical_path = asset_dir / "photo_regression_baseline_v1.json"
    prior_path = asset_dir / "photo_regression_baseline_v2.json"
    baseline_path = asset_dir / "photo_regression_baseline_v3.json"
    universal_baseline = _load_json(asset_dir / "universal_scene_baseline_v1.json")
    photo_boundary = universal_baseline.get("photo_boundary")
    _require(
        isinstance(photo_boundary, dict), "universal baseline photo boundary missing"
    )
    _require(
        photo_boundary.get("baseline_asset") == historical_path.name
        and photo_boundary.get("baseline_asset_sha256") == _sha256(historical_path),
        "historical photo baseline asset hash drift",
    )
    historical = _load_json(historical_path)
    _require(
        historical.get("schema") == "photo_regression_baseline/v1"
        and historical.get("sha256")
        == photo_boundary.get("expected_candidate_pack_sha256")
        and historical.get("pack_id") == photo_boundary.get("expected_pack_id"),
        "historical photo baseline contract drift",
    )
    prior = _load_json(prior_path)
    _require(
        prior.get("schema") == "photo_regression_baseline/v2"
        and prior.get("historical_baseline")
        == {
            "path": historical_path.name,
            "schema": "photo_regression_baseline/v1",
            "sha256": _sha256(historical_path),
        },
        "prior photo baseline lineage mismatch",
    )
    baseline = _load_json(baseline_path)
    _require(
        baseline.get("schema") == "photo_regression_baseline/v3"
        and baseline.get("status") == "current"
        and baseline.get("historical_baseline")
        == {
            "path": prior_path.name,
            "schema": "photo_regression_baseline/v2",
            "sha256": _sha256(prior_path),
        },
        "current photo baseline lineage mismatch",
    )
    command = baseline.get("command")
    _require(
        isinstance(command, list) and all(isinstance(value, str) for value in command),
        "photo baseline command invalid",
    )
    _require(command.count("--output-file") == 1, "photo baseline output flag mismatch")
    _require(
        command.count("--candidate-pack-version") == 1
        and command[command.index("--candidate-pack-version") + 1] == "v4",
        "photo baseline candidate-pack version must be explicitly pinned to v4",
    )
    output_index = command.index("--output-file") + 1
    repo_root = Path(__file__).resolve().parents[3]
    with tempfile.TemporaryDirectory(prefix="illustration-photo-boundary-") as temp_dir:
        temporary_output = Path(temp_dir) / "photo-candidate-pack.json"
        actual_command = list(command)
        actual_command[output_index] = str(temporary_output)
        environment = os.environ.copy()
        environment["GEMINI_API_KEY"] = ""
        environment["GOOGLE_API_KEY"] = ""
        completed = subprocess.run(
            actual_command,
            cwd=repo_root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        _require(
            completed.returncode == 0,
            f"photo baseline command failed: {completed.stderr or completed.stdout}",
        )
        raw = temporary_output.read_bytes()
        payload = json.loads(raw)
    _require(
        isinstance(payload, list)
        and len(payload) == 1
        and isinstance(payload[0], dict),
        "photo baseline output shape mismatch",
    )
    pack = payload[0]
    provenance = pack.get("provenance")
    _require(
        isinstance(provenance, dict)
        and provenance.get("private_routing_exposed") is False,
        "photo baseline public provenance contract missing",
    )
    private_fields = baseline.get("private_fields_absent")
    _require(
        isinstance(private_fields, list)
        and private_fields
        and all(isinstance(field, str) and field for field in private_fields)
        and provenance.get("omitted_private_fields") == private_fields
        and not (set(private_fields) & set(provenance)),
        "photo baseline leaked or misdeclared private provenance",
    )
    digest = hashlib.sha256(raw).hexdigest()
    _require(
        digest == baseline.get("sha256"),
        "current photo baseline candidate-pack bytes drift",
    )
    _require(
        pack.get("pack_id")
        == _canonical_photo_pack_id(pack)
        == baseline.get("pack_id"),
        "current photo baseline pack ID drift",
    )
    _require(
        pack.get("contract_version") == baseline.get("contract_version"),
        "photo baseline contract version drift",
    )
    _require(
        _public_photo_candidate_count(pack) == baseline.get("public_candidate_count"),
        "photo baseline public candidate count drift",
    )
    _require(
        pack.get("negative_en") == baseline.get("negative_en"),
        "photo baseline negative prompt drift",
    )
    return {
        "status": "pass",
        "schema": baseline["schema"],
        "historical_sha256": _sha256(historical_path),
        "sha256": digest,
        "pack_id": pack["pack_id"],
    }


def _predicate_groups(
    value: Any, label: str, allowed_kinds: set[str]
) -> list[list[str]]:
    """Validate flat predicates plus requires-any disjunction groups."""

    _require(isinstance(value, list), f"{label} must be a predicate list")
    predicates: list[list[str]] = []
    for index, item in enumerate(value):
        group = item if isinstance(item, list) else None
        _require(group is not None, f"{label}[{index}] must be an array")
        if len(group) == 3 and all(isinstance(part, str) and part for part in group):
            candidates = [group]
        else:
            _require(group, f"{label}[{index}] predicate disjunction must not be empty")
            candidates = group
        for predicate in candidates:
            _require(
                isinstance(predicate, list)
                and len(predicate) == 3
                and all(isinstance(part, str) and part for part in predicate),
                f"{label}[{index}] predicate must be a three-string tuple",
            )
            _require(
                predicate[0] in allowed_kinds,
                f"{label} has unknown predicate kind: {predicate[0]}",
            )
            predicates.append(predicate)
    return predicates


def _zero_vector(
    value: Any, axes: list[str], label: str, *, maximum: int = 3
) -> dict[str, int]:
    _require(
        isinstance(value, dict) and list(value) == axes, f"{label} axis order mismatch"
    )
    for axis in axes:
        item = value[axis]
        _require(
            isinstance(item, int)
            and not isinstance(item, bool)
            and 0 <= item <= maximum,
            f"{label}.{axis} must be an integer in 0..{maximum}",
        )
    return value


def _universal_distance_band(vector: Mapping[str, int]) -> str:
    """Recompute the frozen ordinal band without trusting a data label."""

    maximum = max(vector.values())
    total = sum(vector.values())
    if maximum == 3 or total >= 10:
        return "far"
    if maximum == 2 or total >= 4:
        return "middle"
    return "near"


def _normalize_universal_semantic_family_value(value: Any) -> str:
    """Normalize one data-owned semantic-family ontology value."""

    if value is None:
        return "null"
    _require(
        isinstance(value, str),
        "universal semantic-family values must be strings or null",
    )
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = re.sub(r"[_-]", " ", normalized)
    normalized = " ".join(normalized.split())
    if normalized in {"$identity actor", "$actor"}:
        return "$actor"
    if normalized in {"$scene location", "$location"}:
        return "$location"
    return normalized


def _universal_semantic_family_payload(
    profile: Mapping[str, Any],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
    prop_concept_ids: set[str],
) -> dict[str, Any]:
    """Independently recompute the frozen ID-independent proposal family."""

    value_id = profile.get("value_id")
    _require(
        isinstance(value_id, str) and value_id in prop_concept_ids,
        "universal proposal semantic family references an unknown prop concept",
    )
    reduced: dict[tuple[str, str, str], int] = {}
    for candidate_id in profile["candidate_ids"]:
        candidate = candidate_by_id[str(candidate_id)]
        for claim in candidate["runtime_contract"]["resource_claims"]:
            _require(
                isinstance(claim, list) and len(claim) == 4,
                f"{candidate_id} semantic-family resource claim must be a raw four-item tuple",
            )
            resource_kind, owner_scope, amount, mode = claim
            _require(
                isinstance(resource_kind, str)
                and resource_kind
                and isinstance(owner_scope, str)
                and owner_scope
                and isinstance(amount, int)
                and not isinstance(amount, bool)
                and amount > 0
                and mode in {"exclusive", "shared"},
                f"{candidate_id} semantic-family resource claim is invalid",
            )
            if owner_scope in {"actor", "scene"}:
                normalized_owner = owner_scope
            else:
                _require(
                    owner_scope in UNIVERSAL_EVENT_ROLE_IDS,
                    f"{candidate_id} semantic-family owner is outside the closed role domain",
                )
                normalized_owner = (
                    f"role:{_normalize_universal_semantic_family_value(owner_scope)}"
                )
            key = (
                normalized_owner,
                _normalize_universal_semantic_family_value(resource_kind),
                str(mode),
            )
            if mode == "exclusive":
                reduced[key] = reduced.get(key, 0) + amount
            else:
                reduced[key] = max(reduced.get(key, 0), amount)
    event_roles = profile["event_roles"]
    return {
        "schema": "subculture-illustration-semantic-family-key/v1",
        "slot": _normalize_universal_semantic_family_value(profile["slot_id"]),
        "prop_concept": _normalize_universal_semantic_family_value(value_id),
        "event_frame": {
            role_id: _normalize_universal_semantic_family_value(event_roles[role_id])
            for role_id in UNIVERSAL_EVENT_ROLE_IDS
        },
        "resource_footprint": [
            {
                "owner_scope": owner_scope,
                "resource_kind": resource_kind,
                "mode": mode,
                "amount": amount,
            }
            for (owner_scope, resource_kind, mode), amount in sorted(reduced.items())
        ],
    }


def _forbidden_pair_structures(value: Any, path: str = "") -> list[str]:
    forbidden: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            normalized = str(key).casefold().replace("-", "_")
            if normalized in {
                "pair_matrix",
                "compatibility_matrix",
                "all_pairs",
                "all_pairs_scan",
                "pairwise_edges",
                "candidate_pairs",
            }:
                forbidden.append(child_path)
            forbidden.extend(_forbidden_pair_structures(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            forbidden.extend(_forbidden_pair_structures(child, f"{path}[{index}]"))
    return forbidden


def _normalized_effect_text(value: Any) -> str:
    normalized = unicodedata.normalize("NFKC", str(value)).casefold()
    normalized = re.sub(r"[_/.-]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _effect_text_clauses(value: Any) -> list[str]:
    """Segment raw text before lossy token normalization.

    Effect polarity is occurrence-local.  Normalizing ``.`` into whitespace
    before segmentation let an earlier negative occurrence suppress a later
    affirmative reassertion.  Hard sentence/contrast boundaries always reset
    scope.  Additive coordinators preserve a preceding negative scope unless
    the English right-hand side begins with a reviewed independent-subject
    witness; this keeps ``do not X and Y`` negative without hiding ``do not X
    and the scene includes X``.
    Directional substitution markers (``instead of``, ``대신``, ``ではなく``,
    ``而不是``) deliberately remain inside a clause for side-aware handling.
    """

    raw = unicodedata.normalize("NFKC", str(value)).casefold()
    hard_clauses = re.split(
        r"[.!?;:。！？；：\r\n]+|\s*[\u2012-\u2015]\s*|"
        r"\b(?:and\s+then|but|however|yet|whereas|while|then|"
        r"even\s+though|although)\b|"
        r"(?:하지만|그러나|반면|그런데|그\s*뒤|그\s*후|"
        r"しかし|ただし|一方|その後|"
        r"但是|然而|不过|但)",
        raw,
    )
    soft_separator = re.compile(r"\band\b|그리고|하고|そして|并且|然后")
    independent_english_subject = re.compile(
        r"^(?:a|an|the|this|that|these|those|another|it|he|she|they|we|i|you)\b"
    )
    result: list[str] = []
    for hard_clause in hard_clauses:
        cursor = 0
        force_negative = False
        for separator in soft_separator.finditer(hard_clause):
            raw_clause = hard_clause[cursor : separator.start()]
            clause = _normalized_effect_text(raw_clause)
            if clause:
                if force_negative and not _effect_clause_is_negative(clause):
                    clause = f"do not {clause}"
                result.append(clause)
                force_negative = _effect_clause_is_negative(clause)
            rhs = _normalized_effect_text(hard_clause[separator.end() :])
            if separator.group(0) == "and" and independent_english_subject.match(rhs):
                force_negative = False
            cursor = separator.end()
        raw_clause = hard_clause[cursor:]
        clause = _normalized_effect_text(raw_clause)
        if clause:
            if force_negative and not _effect_clause_is_negative(clause):
                clause = f"do not {clause}"
            result.append(clause)
    return result


def _effect_text_contains(text: str, term: str) -> bool:
    return bool(_effect_text_match_spans(text, term))


def _effect_text_match_spans(text: str, term: str) -> list[tuple[int, int]]:
    normalized_term = _normalized_effect_text(term)
    if not normalized_term:
        return []
    if normalized_term.isascii():
        suffix = (
            r"(?:s|es|ed|d|ing)?"
            if re.fullmatch(r"[a-z]+", normalized_term) and len(normalized_term) >= 4
            else ""
        )
        return [
            match.span()
            for match in re.finditer(
                r"(?<![a-z0-9])"
                + re.escape(normalized_term)
                + suffix
                + r"(?![a-z0-9])",
                text,
            )
        ]
    return [
        (match.start(), match.end())
        for match in re.finditer(re.escape(normalized_term), text)
    ]


def _effect_match_substitution_side(
    clause: str,
    start: int,
    end: int,
) -> str | None:
    """Return a positive substitution segment, or ``None`` when rejected.

    Substitution markers are directional.  Treating the whole clause as
    negative made the Chinese ``A, rather than B`` form hide a positive A,
    while splitting at the marker made Korean/Japanese rejected alternatives
    look positive.  Segment labels also stop compositional lexeme groups from
    borrowing one half from each side of ``A 아니라 B``.
    """

    # Korean postposed forms reject the immediately preceding alternative,
    # not every earlier assertion in the clause.  A second lexical token in
    # the intervening span (for example ``붙여 날개 대신``) closes the prior
    # positive assertion before the substituted-away noun.
    for marker in re.finditer(r"아니라|대신", clause):
        intervening = clause[end : marker.start()].strip(" ,")
        if end <= marker.start() and " " not in intervening:
            return None
        if end <= marker.start():
            return f"pre:{marker.start()}"
        if start >= marker.end():
            return f"post:{marker.start()}"

    # Japanese postposed forms reject the material before the marker.
    for marker in re.finditer(r"(?:の)?ではなく|ではない|(?:の)?代わり(?:に)?", clause):
        if end <= marker.start():
            return None
        if start >= marker.end():
            return f"post:{marker.start()}"

    # Chinese `A 而不是 B` rejects B, while `不是 A 而是 B` rejects A.
    for marker in re.finditer(r"(?<!而)不是", clause):
        positive_turn = re.search(r"而是", clause[marker.end() :])
        negative_end = (
            marker.end() + positive_turn.start()
            if positive_turn is not None
            else len(clause)
        )
        if start >= marker.end() and end <= negative_end:
            return None
        if positive_turn is not None and start >= negative_end + len("而是"):
            return f"post:{marker.start()}"
    for marker in re.finditer(r"而不是", clause):
        if start >= marker.end():
            return None
        if end <= marker.start():
            return f"pre:{marker.start()}"

    # English markers reject the following alternative.  A leading marker's
    # comma closes that rejected span so the replacement after it stays live.
    for marker in re.finditer(r"\b(?:instead\s+of|rather\s+than)\b", clause):
        negative_end = len(clause)
        if not clause[: marker.start()].strip():
            comma = clause.find(",", marker.end())
            if comma >= 0:
                negative_end = comma
        if start >= marker.end() and end <= negative_end:
            return None
        if end <= marker.start():
            return f"pre:{marker.start()}"
        if start >= negative_end and negative_end != len(clause):
            return f"post:{marker.start()}"
    return "main"


def _effect_clause_is_negative(clause: str) -> bool:
    without_not_only = re.sub(r"\bnot\s+only\b", "", clause)
    return (
        re.search(
            r"\b(?:no|never|without|cannot|can't|do\s+not|does\s+not|don't|doesn't|"
            r"must\s+not|should\s+not|forbid(?:den)?|exclude(?:d)?|omit(?:ted)?)\b|"
            r"(?:않|아닌|없|금지|하지\s*마|지\s*마|말아|ない|禁止|"
            r"不要|不(?:要|添加|装|长)|無|无)",
            without_not_only,
        )
        is not None
    )


def _effect_clause_positive_term_sides(
    clause: str,
    terms: Iterable[Any],
) -> set[str]:
    if _effect_clause_is_negative(clause):
        return set()
    return {
        side
        for term in terms
        for start, end in _effect_text_match_spans(clause, str(term))
        if (side := _effect_match_substitution_side(clause, start, end)) is not None
    }


def _effect_clause_has_positive_term(clause: str, terms: Iterable[Any]) -> bool:
    return bool(_effect_clause_positive_term_sides(clause, terms))


def _classify_universal_contract_effects(
    texts: Iterable[Any],
    contract_effect_profiles: Iterable[Mapping[str, Any]],
) -> set[str]:
    """Classify positive blocked semantics from values, aliases, or term groups."""

    clauses = [clause for value in texts for clause in _effect_text_clauses(value)]
    effects: set[str] = set()
    for profile in contract_effect_profiles:
        effect_id = str(profile["effect_id"])
        semantic_values = [str(value) for value in profile["semantic_value_ids"]]
        aliases = [
            str(value)
            for record in profile["literal_aliases"]
            for value in record["values"]
        ]
        groups = profile["required_literal_groups"]
        for clause in clauses:
            semantic_match = _effect_clause_has_positive_term(
                clause,
                semantic_values,
            )
            alias_match = _effect_clause_has_positive_term(clause, aliases)
            group_sides = [
                _effect_clause_positive_term_sides(clause, group) for group in groups
            ]
            compositional_match = bool(group_sides) and bool(
                set.intersection(*group_sides)
            )
            if semantic_match or alias_match or compositional_match:
                effects.add(effect_id)
                break
    return effects


def _validate_contract_effect_profiles(
    semantic_asset: Mapping[str, Any],
) -> list[dict[str, Any]]:
    profiles = semantic_asset.get("contract_effect_profiles")
    _require(
        isinstance(profiles, list) and len(profiles) == 9,
        "universal contract effect profile inventory mismatch",
    )
    by_effect: dict[str, dict[str, Any]] = {}
    for profile in profiles:
        _require(
            isinstance(profile, dict)
            and set(profile)
            == {
                "id",
                "effect_id",
                "source_targets",
                "semantic_value_ids",
                "literal_aliases",
                "required_literal_groups",
                "polarity",
                "subject_binding",
            },
            "universal contract effect profile shape mismatch",
        )
        effect_id = profile.get("effect_id")
        _require(
            isinstance(effect_id, str)
            and effect_id in UNIVERSAL_CONTRACT_EFFECT_SUBJECT_BY_ID
            and effect_id not in by_effect
            and profile.get("id") == f"contract_effect_{effect_id}"
            and profile.get("polarity") == "affirmative"
            and profile.get("subject_binding")
            == UNIVERSAL_CONTRACT_EFFECT_SUBJECT_BY_ID[effect_id],
            "universal contract effect ID/polarity/subject binding drift",
        )
        targets = profile.get("source_targets")
        _require(
            isinstance(targets, list)
            and [
                (target.get("source_kind"), target.get("source_id"))
                for target in targets
                if isinstance(target, dict)
                and set(target) == {"source_kind", "source_id"}
            ]
            == UNIVERSAL_CONTRACT_EFFECT_TARGETS_BY_ID[effect_id],
            f"universal contract effect source targets drift: {effect_id}",
        )
        _strings(
            profile.get("semantic_value_ids"),
            f"contract_effect.{effect_id}.semantic_value_ids",
            minimum=1,
        )
        aliases = profile.get("literal_aliases")
        _require(
            isinstance(aliases, list)
            and [record.get("locale") for record in aliases if isinstance(record, dict)]
            == ["ko", "en", "ja", "zh"],
            f"universal contract effect locale coverage drift: {effect_id}",
        )
        for record in aliases:
            _require(
                isinstance(record, dict) and set(record) == {"locale", "values"},
                f"universal contract effect alias shape drift: {effect_id}",
            )
            _strings(
                record.get("values"),
                f"contract_effect.{effect_id}.{record['locale']}",
                minimum=1,
            )
        groups = profile.get("required_literal_groups")
        _require(
            isinstance(groups, list)
            and len(groups) in {2, 3}
            and all(
                isinstance(group, list)
                and len(group) >= 2
                and all(isinstance(value, str) and value.strip() for value in group)
                for group in groups
            ),
            f"universal contract effect compositional groups drift: {effect_id}",
        )
        if effect_id.startswith("human_"):
            _require(
                len(groups) == 3
                and any(
                    value in groups[0] for value in ("human", "사람", "人間", "人类")
                )
                and any(
                    value in groups[2]
                    for value in (
                        "attach",
                        "add",
                        "sprout",
                        "grow",
                        "붙",
                        "추가",
                        "添加",
                        "长出",
                    )
                ),
                f"universal human-attachment compositional guard weakened: {effect_id}",
            )
        by_effect[effect_id] = profile
    _require(
        set(by_effect) == set(UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS),
        "universal contract effects do not exactly cover the blocked semantic enum",
    )
    return profiles


def _validate_universal_composition_literal_carriers(
    semantic_asset: Mapping[str, Any],
    contracts_by_case: Mapping[str, Mapping[str, Any]],
) -> dict[str, int]:
    """Prove explicit English carriers exactly cover the canonical target set."""

    profile_set = semantic_asset.get("composition_literal_carrier_profiles")
    _require(
        isinstance(profile_set, Mapping)
        and list(profile_set) == ["identity_core", "fixed_slots", "event_roles"],
        "universal composition literal-carrier section mismatch",
    )
    section_fields = {
        "identity_core": ["fact_id", "polarity", "required_lexeme_groups"],
        "fixed_slots": ["slot_id", "value_id", "required_lexeme_groups"],
        "event_roles": ["role_id", "value_id", "required_lexeme_groups"],
    }
    key_fields = {
        "identity_core": ("fact_id", "polarity"),
        "fixed_slots": ("slot_id", "value_id"),
        "event_roles": ("role_id", "value_id"),
    }
    internal_tokens = {
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
    actual: dict[str, set[tuple[str, ...]]] = {
        section: set() for section in section_fields
    }
    for section, fields in section_fields.items():
        records = profile_set.get(section) if isinstance(profile_set, Mapping) else None
        _require(
            isinstance(records, list) and records,
            f"universal composition carrier {section} must be a nonempty list",
        )
        for index, profile in enumerate(records):
            _require(
                isinstance(profile, Mapping) and list(profile) == fields,
                f"universal composition carrier shape/order drift: {section}[{index}]",
            )
            key = tuple(str(profile.get(field, "")) for field in key_fields[section])
            _require(
                all(key) and key not in actual[section],
                f"universal composition carrier key is empty or duplicated: {section}/{key}",
            )
            if section == "identity_core":
                _require(
                    key[1] in {"asserted_presence", "forbidden"},
                    f"universal composition carrier polarity drift: {key}",
                )
            groups = profile.get("required_lexeme_groups")
            _require(
                isinstance(groups, list)
                and 1 <= len(groups) <= (3 if section == "identity_core" else 2),
                f"universal composition carrier group bound drift: {section}/{key}",
            )
            seen_groups: set[tuple[str, ...]] = set()
            for group in groups:
                normalized_group = tuple(str(item) for item in group) if isinstance(group, list) else ()
                _require(
                    bool(normalized_group)
                    and normalized_group not in seen_groups
                    and len(normalized_group) == len(set(normalized_group))
                    and all(
                        re.fullmatch(r"[a-z0-9]+(?: [a-z0-9]+)*", alternative)
                        is not None
                        and alternative == normalize_text(alternative)
                        and not (set(alternative.split()) & internal_tokens)
                        for alternative in normalized_group
                    ),
                    f"universal composition carrier must be normalized reviewed English: {section}/{key}",
                )
                seen_groups.add(normalized_group)
            actual[section].add(key)

    expected: dict[str, set[tuple[str, ...]]] = {
        section: set() for section in section_fields
    }
    for contract in contracts_by_case.values():
        identity = contract["identity_core"]
        for entity in identity["entities"]:
            expected["identity_core"].update(
                (str(fact["id"]), "asserted_presence")
                for fact in entity["feature_facts"]
            )
        expected["identity_core"].update(
            (str(fact["id"]), "asserted_presence")
            for fact in identity["scene_facts"]
        )
        expected["identity_core"].update(
            (str(fact["id"]), "forbidden")
            for fact in identity["forbidden_facts"]
        )
        for slot in contract["slot_states"]:
            if slot["state"] == "fixed":
                expected["fixed_slots"].update(
                    (str(slot["slot_id"]), str(binding["value_id"]))
                    for binding in slot["value_phrase_bindings"]
                )
        expected["event_roles"].update(
            (str(role["role_id"]), str(role["value_id"]))
            for role in contract["event_roles"]
            if role["state"] == "fixed"
        )
    _require(
        actual == expected,
        "universal composition carriers do not exactly cover canonical semantic targets",
    )
    total = sum(len(values) for values in actual.values())
    _require(
        semantic_asset.get("counts", {}).get(
            "composition_literal_carrier_profiles"
        )
        == total,
        "universal composition carrier count drift",
    )
    return {
        "identity_core": len(actual["identity_core"]),
        "fixed_slots": len(actual["fixed_slots"]),
        "event_roles": len(actual["event_roles"]),
        "total": total,
    }


def _validate_universal_literal_realization_profiles(
    semantic_asset: Mapping[str, Any],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
    resource_kind_ids: Sequence[str],
) -> dict[str, Any]:
    """Validate the reviewed, case-independent literal realization table."""

    expected_top_keys = [
        "schema",
        "reviewed_at",
        "normalization",
        "prop_literal_sense_bindings",
        "explicit_capability_assertion_profiles",
        "literal_polarity_contract",
        "literal_quantity_bindings",
        "identity_literal_profiles",
        "composition_literal_carrier_profiles",
        "context_literal_profiles",
        "literal_visual_realization_profiles",
        "visual_carrier_profiles",
        "resource_carrier_profiles",
        "semantic_effect_registry",
        "guard_execution_profiles",
        "contract_effect_profiles",
        "counts",
    ]
    _require(
        isinstance(semantic_asset, Mapping)
        and list(semantic_asset) == expected_top_keys
        and semantic_asset.get("schema")
        == "subculture-illustration-universal-semantic-bindings/v1",
        "universal semantic-binding top-level contract mismatch",
    )
    _require(
        semantic_asset.get("prop_literal_sense_bindings")
        == [
            {
                "id": "prop_sense_wooden_mallet_not_generic_hammer",
                "catalog_prop_id": "prop_hammer",
                "literal_aliases": [
                    {
                        "locale": "ko",
                        "values": ["나무 망치", "나무망치", "목재 망치"],
                    },
                    {
                        "locale": "en",
                        "values": ["wooden mallet", "small wooden mallet", "mallet"],
                    },
                    {"locale": "ja", "values": ["木槌", "木製の槌"]},
                    {"locale": "zh", "values": ["木槌", "木锤", "木錘"]},
                ],
                "accepted_semantic_tokens": ["mallet"],
                "activation_target": "prop_wooden_mallet",
            }
        ],
        "universal wooden-mallet literal sense binding drift",
    )
    expected_profiles: list[dict[str, Any]] = []
    actor_primary = [{"role_id": "actor", "entity_quantifier": "primary"}]
    participant_overrides = {
        "lvr_shared_attention_convergence": [
            {"role_id": "actor", "entity_quantifier": "all"}
        ],
        "lvr_protective_recipient_path": [
            {"role_id": "actor", "entity_quantifier": "primary"},
            {"role_id": "recipient", "entity_quantifier": "all"},
        ],
        "lvr_shared_target_convergence": [
            {"role_id": "actor", "entity_quantifier": "all"}
        ],
    }
    for (
        profile_id,
        source_slot_id,
        mechanism_class_id,
        realized_facet,
        candidate_group,
        literal_scope,
        required_literal_groups,
        owned_pixel_kinds,
        owned_resource_kinds,
        selection_rank,
    ) in UNIVERSAL_V2_LITERAL_REALIZATION_PROFILE_SPECS:
        expected_profiles.append(
            {
                "id": profile_id,
                "source_slot_id": source_slot_id,
                "mechanism_class_id": mechanism_class_id,
                "realized_facet": realized_facet,
                "candidate_group": candidate_group,
                "participant_roles": copy.deepcopy(
                    participant_overrides.get(profile_id, actor_primary)
                ),
                "quantifier": "all",
                "enforcement": "selected",
                "literal_scope": literal_scope,
                "required_literal_groups": [
                    {
                        "alternatives": alternatives,
                        "required_polarity": required_polarity,
                    }
                    for alternatives, required_polarity in required_literal_groups
                ],
                "owned_pixel_kinds": owned_pixel_kinds,
                "owned_resource_kinds": owned_resource_kinds,
                "selection_rank": selection_rank,
            }
        )
    profiles = semantic_asset.get("literal_visual_realization_profiles")
    _require(
        profiles == expected_profiles,
        "universal literal visual realization profiles drift from the reviewed 19-profile table",
    )
    profile_keys = [
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
    ]
    candidate_owners: set[str] = set()
    resource_kind_set = set(resource_kind_ids)
    for profile in profiles:
        _require(
            list(profile) == profile_keys
            and profile["candidate_group"] == sorted(set(profile["candidate_group"]))
            and profile["required_literal_groups"]
            and profile["owned_pixel_kinds"]
            == sorted(set(profile["owned_pixel_kinds"]))
            and profile["owned_resource_kinds"]
            == sorted(set(profile["owned_resource_kinds"]))
            and set(profile["owned_resource_kinds"]) <= resource_kind_set,
            f"literal realization profile closure/order drift: {profile['id']}",
        )
        participant_role_ids = [
            str(item["role_id"]) for item in profile["participant_roles"]
        ]
        _require(
            all(
                list(item) == ["role_id", "entity_quantifier"]
                and item["role_id"] in UNIVERSAL_EVENT_ROLE_IDS
                and item["entity_quantifier"] in {"primary", "all"}
                for item in profile["participant_roles"]
            )
            and len(participant_role_ids) == len(set(participant_role_ids))
            and participant_role_ids
            == [
                role_id
                for role_id in UNIVERSAL_EVENT_ROLE_IDS
                if role_id in participant_role_ids
            ],
            f"literal realization participant binding drift: {profile['id']}",
        )
        for group in profile["required_literal_groups"]:
            _require(
                list(group) == ["alternatives", "required_polarity"]
                and group["alternatives"]
                and group["alternatives"] == sorted(set(group["alternatives"]))
                and all(
                    isinstance(value, str) and value.strip() and "_" not in value
                    for value in group["alternatives"]
                )
                and group["required_polarity"] in {"affirmative", "negated"},
                f"literal realization required group drift: {profile['id']}",
            )
        for candidate_id in profile["candidate_group"]:
            candidate = candidate_by_id.get(candidate_id)
            _require(
                candidate is not None
                and candidate.get("role") == "visual_atom"
                and candidate.get("facet") == profile["realized_facet"]
                and candidate_id not in candidate_owners,
                f"literal realization candidate owner/facet drift: {candidate_id}",
            )
            candidate_owners.add(candidate_id)
            pixel_kinds = {
                str(item["kind"])
                for item in candidate["runtime_contract"]["pixel_evidence"]
            }
            resource_kinds = {
                str(item[0])
                for item in candidate["runtime_contract"]["resource_claims"]
            }
            _require(
                set(profile["owned_pixel_kinds"]) <= pixel_kinds
                and set(profile["owned_resource_kinds"]) <= resource_kinds,
                f"literal realization candidate material ownership drift: {candidate_id}",
            )
    counts = semantic_asset.get("counts")
    _require(
        isinstance(counts, Mapping)
        and counts.get("literal_visual_realization_profiles") == 19,
        "universal literal realization profile count drift",
    )
    return {
        "profile_count": len(profiles),
        "candidate_owner_count": len(candidate_owners),
    }


def _validate_universal_visual_owner_mapping_realizability(
    crosswalk: Mapping[str, Any],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, int]:
    """Prove every reviewed visual-owner mapping can realize its siblings.

    This is deliberately asset-backed and is not part of source-only oracle
    compilation.  The crosswalk names case-independent semantic owners; the
    executable catalog must collectively expose every typed material edge that
    those owners are expected to ground.
    """

    mapping_rows = [
        *crosswalk.get("legacy_event_label_mappings", []),
        *crosswalk.get("legacy_bridge_label_mappings", []),
    ]
    _require(
        all(isinstance(mapping, Mapping) for mapping in mapping_rows),
        "universal visual-owner mapping table is missing",
    )
    checked_mapping_count = 0
    checked_sibling_target_count = 0
    material_kinds = {
        "atom_facet",
        "event_role",
        "pixel_evidence_kind",
        "resource_kind",
        "runtime_bridge_type",
    }

    for mapping in mapping_rows:
        targets = mapping.get("targets")
        _require(
            isinstance(targets, list),
            f"universal visual-owner targets are malformed: {mapping.get('mapping_id')}",
        )
        visual_targets = [
            target
            for target in targets
            if isinstance(target, Mapping)
            and target.get("target_kind") == "visual_candidate"
        ]
        if not visual_targets:
            continue
        mapping_id = str(mapping.get("mapping_id"))
        owner_ids = list(
            dict.fromkeys(
                str(candidate_id)
                for target in visual_targets
                for candidate_id in target.get("target_ids", [])
            )
        )
        owner_candidates = [
            candidate_by_id.get(candidate_id) for candidate_id in owner_ids
        ]
        _require(
            owner_ids
            and all(
                isinstance(candidate, Mapping)
                and candidate.get("role") == "visual_atom"
                for candidate in owner_candidates
            ),
            f"universal visual-owner mapping references a nonvisual or unknown candidate: {mapping_id}",
        )
        checked_mapping_count += 1

        def candidate_supports(
            candidate: Mapping[str, Any],
            target_kind: str,
            target_id: str,
            enforcement: str,
        ) -> bool:
            runtime = candidate["runtime_contract"]
            if target_kind == "atom_facet":
                return candidate["facet"] == target_id
            if target_kind == "event_role":
                return any(
                    binding[0] == target_id
                    and (enforcement != "required" or binding[1] == "required")
                    for binding in runtime["bindings"]
                )
            if target_kind == "pixel_evidence_kind":
                return any(
                    pixel["kind"] == target_id for pixel in runtime["pixel_evidence"]
                )
            if target_kind == "resource_kind":
                return any(
                    claim[0] == target_id for claim in runtime["resource_claims"]
                )
            if target_kind == "runtime_bridge_type":
                return target_id in runtime["bridge_types"]
            raise ValidationFailure(
                f"unsupported visual-owner sibling target kind: {target_kind}"
            )

        for target in targets:
            if not isinstance(target, Mapping):
                continue
            target_kind = str(target.get("target_kind"))
            if target_kind not in material_kinds:
                continue
            enforcement = str(target.get("enforcement"))
            if enforcement not in {"eligible", "required"}:
                continue
            target_ids = [str(target_id) for target_id in target.get("target_ids", [])]
            target_results = [
                any(
                    candidate_supports(
                        candidate,
                        target_kind,
                        target_id,
                        enforcement,
                    )
                    for candidate in owner_candidates
                    if isinstance(candidate, Mapping)
                )
                for target_id in target_ids
            ]
            realized = (
                all(target_results)
                if target.get("quantifier") == "all"
                else any(target_results)
            )
            _require(
                target_ids and realized,
                "universal visual-owner mapping has no collective executable "
                f"{target_kind} realization: {mapping_id}:{target_ids}",
            )
            checked_sibling_target_count += 1

    return {
        "mapping_count": checked_mapping_count,
        "sibling_target_count": checked_sibling_target_count,
    }


def _validate_universal_quiet_theme_source_contract(
    profile: Mapping[str, Any],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
) -> None:
    """Pin the reviewed quiet-theme source to a zero displacement outcome."""

    _require(
        profile.get("id") == "context_quiet_theme_guard_middle"
        and profile.get("distance_profile", {}).get("theme") == 0
        and profile.get("load_profile", {}).get("theme_displacement") == 0,
        "quiet-theme source must have zero theme distance and displacement load",
    )
    carrier_ids = profile.get("candidate_ids")
    _require(
        isinstance(carrier_ids, list)
        and carrier_ids
        and all(
            candidate_id in candidate_by_id
            and candidate_by_id[candidate_id]["runtime_contract"]["load_profile"][
                "theme_displacement"
            ]
            == 0
            for candidate_id in carrier_ids
        ),
        "quiet-theme source carriers must preserve zero theme displacement",
    )


def _validate_universal_fixed_prop_eligibility_source_contract(
    candidate_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Pin the sole generic visual carrier eligible for open or fixed props."""

    predicate = ["slot", "prop", "open_or_fixed"]
    eligible_ids = sorted(
        candidate_id
        for candidate_id, candidate in candidate_by_id.items()
        if predicate in candidate.get("triggers", [])
    )
    _require(
        eligible_ids == ["uer_role_bearing_contact"],
        "fixed-prop eligibility must use only the reviewed generic role-bearing carrier",
    )
    carrier = candidate_by_id["uer_role_bearing_contact"]
    runtime = carrier["runtime_contract"]
    _require(
        carrier.get("role") == "visual_atom"
        and carrier.get("facet") == "prop"
        and carrier.get("parameters") == {}
        and carrier.get("triggers") == [predicate]
        and runtime.get("requires_all")
        == [
            ["event_role", "actor", "present"],
            ["capability", "actor", "manipulator_or_equivalent"],
        ]
        and ["slot", "prop", "closed"] in runtime.get("forbids_any", [])
        and runtime.get("resource_claims")
        == [
            ["manipulator", "actor", 1, "exclusive"],
            ["prop_slot", "scene", 1, "exclusive"],
        ],
        "fixed-prop generic carrier source contract drift",
    )
    return {
        "candidate_ids": eligible_ids,
        "selection_required": False,
    }


def _validate_universal_semantic_effect_policy(
    candidate_asset: Mapping[str, Any],
    compatibility: Mapping[str, Any],
    semantic_asset: Mapping[str, Any],
) -> dict[str, Any]:
    """Independently bind the safe v1 source catalog to an empty effect policy."""

    contract_effect_profiles = _validate_contract_effect_profiles(semantic_asset)
    registry = semantic_asset.get("semantic_effect_registry")
    _require(
        isinstance(registry, dict)
        and list(registry)
        == ["schema", "effect_ids", "source_kind_ids", "profiles", "counts"]
        and registry.get("schema")
        == "illustration-universal-semantic-effect-registry/v1",
        "universal semantic effect registry contract mismatch",
    )
    _require(
        registry.get("effect_ids") == sorted(UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS)
        and registry.get("source_kind_ids") == UNIVERSAL_EFFECT_SOURCE_KIND_IDS,
        "universal semantic effect registry closed enums drift",
    )
    candidates = candidate_asset.get("candidates")
    proposals = candidate_asset.get("proposal_profiles")
    contexts = candidate_asset.get("context_distance_profiles")
    bridge_policy = compatibility.get("bridge_policy")
    _require(
        isinstance(candidates, list)
        and isinstance(proposals, list)
        and isinstance(contexts, list)
        and isinstance(bridge_policy, dict),
        "universal effect registry source catalogs are missing",
    )
    expected_by_kind = {
        "visual_candidate": sorted(
            str(candidate["id"])
            for candidate in candidates
            if isinstance(candidate, dict) and candidate.get("role") == "visual_atom"
        ),
        "proposal_profile": sorted(
            str(profile["id"]) for profile in proposals if isinstance(profile, dict)
        ),
        "context_profile": sorted(
            str(profile["id"]) for profile in contexts if isinstance(profile, dict)
        ),
        "bridge_type": sorted(
            _strings(
                bridge_policy.get("bridge_type_ids"),
                "universal effect bridge sources",
                minimum=1,
            )
        ),
        "resource_kind": sorted(
            _strings(
                compatibility.get("resource_kind_ids"),
                "universal effect resource sources",
                minimum=1,
            )
        ),
    }
    resource_carriers = semantic_asset.get("resource_carrier_profiles")
    _require(
        isinstance(resource_carriers, list),
        "universal resource carrier profiles are missing",
    )
    resource_carrier_by_kind = {
        str(profile.get("resource_kind")): profile
        for profile in resource_carriers
        if isinstance(profile, dict)
    }

    def flattened_strings(value: Any) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, Mapping):
            return [
                text
                for key, child in value.items()
                for text in [str(key), *flattened_strings(child)]
            ]
        if isinstance(value, list):
            return [text for child in value for text in flattened_strings(child)]
        return [] if value is None else [str(value)]

    candidate_by_id = {
        str(candidate["id"]): candidate
        for candidate in candidates
        if isinstance(candidate, dict) and isinstance(candidate.get("id"), str)
    }
    proposal_by_id = {
        str(profile["id"]): profile
        for profile in proposals
        if isinstance(profile, dict) and isinstance(profile.get("id"), str)
    }
    context_by_id = {
        str(profile["id"]): profile
        for profile in contexts
        if isinstance(profile, dict) and isinstance(profile.get("id"), str)
    }

    def source_semantic_texts(source_kind: str, source_id: str) -> list[str]:
        if source_kind == "visual_candidate":
            source = candidate_by_id[source_id]
            return flattened_strings(
                {
                    "definition": source.get("definition"),
                    "aliases": source.get("aliases"),
                    "parameters": source.get("parameters"),
                    "bindings": source.get("bindings"),
                    "triggers": source.get("triggers"),
                    "postconditions": source.get("postconditions"),
                }
            )
        if source_kind == "proposal_profile":
            source = proposal_by_id[source_id]
            return flattened_strings(
                {
                    "value_id": source.get("value_id"),
                    "prompt_phrase_en": source.get("prompt_phrase_en"),
                    "event_roles": source.get("event_roles"),
                }
            )
        if source_kind == "context_profile":
            source = context_by_id[source_id]
            return flattened_strings(
                {
                    "requires_all": source.get("requires_all"),
                    "requires_any": source.get("requires_any"),
                    "forbids_any": source.get("forbids_any"),
                }
            )
        if source_kind == "bridge_type":
            return [source_id]
        if source_kind == "resource_kind":
            return flattened_strings(resource_carrier_by_kind[source_id])
        raise ValidationFailure(f"unknown universal effect source kind: {source_kind}")

    independently_derived_effects: dict[tuple[str, str], set[str]] = {}
    for kind in UNIVERSAL_EFFECT_SOURCE_KIND_IDS:
        for source_id in expected_by_kind[kind]:
            derived = _classify_universal_contract_effects(
                source_semantic_texts(kind, source_id),
                contract_effect_profiles,
            )
            _require(
                not derived,
                "universal safe source meaning activates a blocked semantic effect: "
                f"{kind}:{source_id}:{sorted(derived)}",
            )
            independently_derived_effects[(kind, source_id)] = derived
    expected_profiles = [
        {
            "source_kind": kind,
            "source_id": source_id,
            "effect_ids": sorted(independently_derived_effects[(kind, source_id)]),
        }
        for kind in UNIVERSAL_EFFECT_SOURCE_KIND_IDS
        for source_id in expected_by_kind[kind]
    ]
    _require(
        registry.get("profiles") == expected_profiles,
        "universal semantic effect profiles must exactly equal the independently compiled empty safe catalog",
    )
    expected_counts = {
        kind: len(expected_by_kind[kind]) for kind in UNIVERSAL_EFFECT_SOURCE_KIND_IDS
    }
    expected_counts["total"] = sum(expected_counts.values())
    _require(
        registry.get("counts") == expected_counts,
        "universal semantic effect registry counts drift",
    )
    return {
        "schema": registry["schema"],
        "profile_count": expected_counts["total"],
        "effect_id_count": len(UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS),
        "nonempty_effect_profile_count": 0,
        "registry_sha256": hashlib.sha256(canonical_json_bytes(registry)).hexdigest(),
    }


def _validate_universal_trace_source_authorities(
    candidate_asset: Mapping[str, Any],
    compatibility: Mapping[str, Any],
    semantic_asset: Mapping[str, Any],
    candidate_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Independently freeze the raw authorities consumed by trace replay."""

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
    _require(
        compatibility.get("budgets") == expected_budgets,
        "universal trace compatibility budget authority drift",
    )
    _require(
        compatibility.get("resource_policy")
        == {
            "scope": "entity_or_scene",
            "capacity_check": "sum_exclusive_claims_lte_capacity",
            "same_phase_double_booking": "block",
            "shared_attention_exception": "only_same_visible_target",
            "repair_order": [
                "release_phase",
                "environment_support",
                "mount_or_sling",
                "alternate_capable_effector",
                "drop_optional_candidate",
            ],
        },
        "universal trace resource-policy authority drift",
    )
    _require(
        compatibility.get("decision_reason_code_ids")
        == UNIVERSAL_DECISION_REASON_CODE_IDS,
        "universal trace reason-code authority drift",
    )
    distance_policy = compatibility.get("distance_policy")
    creativity_bands = (
        distance_policy.get("creativity_bands")
        if isinstance(distance_policy, Mapping)
        else None
    )
    _require(
        isinstance(creativity_bands, list)
        and all(
            isinstance(band, Mapping) and "max_optional_remote" not in band
            for band in creativity_bands
        )
        and "max_remote_or_high_load_optional_premises" not in distance_policy,
        "universal trace source cannot encode creativity-band remote ceilings",
    )

    proposals = candidate_asset.get("proposal_profiles")
    contexts = candidate_asset.get("context_distance_profiles")
    rules = compatibility.get("universal_rules")
    _require(
        isinstance(proposals, list)
        and len(proposals) == 12
        and isinstance(contexts, list)
        and len(contexts) == 18
        and isinstance(rules, list)
        and len(rules) == 7,
        "universal trace policy-source inventory drift",
    )
    policy_source_rows: list[dict[str, Any]] = []
    for prefix, source_kind, stage, rows in (
        ("proposal_policy", "proposal_policy", "contract_input", proposals),
        ("context_policy", "context_policy", "contract_input", contexts),
        ("universal_rule", "universal_rule", "postselection", rules),
    ):
        for source in rows:
            _require(
                isinstance(source, Mapping)
                and isinstance(source.get("id"), str)
                and bool(source["id"]),
                "universal trace policy source lacks a stable ID",
            )
            record_id = f"{prefix}__{source['id']}"
            policy_mode = (
                None if source_kind == "universal_rule" else source.get("policy_mode")
            )
            declared_outcome = (
                source.get("outcome") if source_kind == "universal_rule" else None
            )
            _require(
                (
                    source_kind == "universal_rule"
                    and policy_mode is None
                    and declared_outcome in {"block", "repair", "allow_with_bridge"}
                )
                or (
                    source_kind != "universal_rule"
                    and policy_mode in {"ordinary", "safe_tool", "explicit_weapon_only"}
                    and declared_outcome is None
                ),
                f"universal trace policy source domain drift: {record_id}",
            )
            payload = {
                "schema": "illustration-universal-scene-policy-source-contract/v1",
                "record_id": record_id,
                "source_kind": source_kind,
                "source_id": source["id"],
                "evaluation_stage": stage,
                "policy_mode": policy_mode,
                "declared_outcome": declared_outcome,
                "source_record": copy.deepcopy(source),
            }
            policy_source_rows.append(
                {
                    "record_id": record_id,
                    "source_kind": source_kind,
                    "source_id": source["id"],
                    "evaluation_stage": stage,
                    "policy_mode": policy_mode,
                    "declared_outcome": declared_outcome,
                    "source_contract_sha256": hashlib.sha256(
                        canonical_json_bytes(payload)
                    ).hexdigest(),
                }
            )
    policy_source_rows.sort(key=lambda row: row["record_id"].encode("utf-8"))
    _require(
        len(policy_source_rows)
        == len({row["record_id"] for row in policy_source_rows})
        == 37,
        "universal trace policy-source IDs are incomplete or duplicated",
    )

    guard_profiles = semantic_asset.get("guard_execution_profiles")
    guard_ids = compatibility.get("guard_candidate_ids")
    _require(
        isinstance(guard_profiles, list)
        and len(guard_profiles) == 32
        and isinstance(guard_ids, list)
        and guard_ids == sorted(set(guard_ids))
        and [profile.get("guard_id") for profile in guard_profiles] == guard_ids,
        "universal trace guard-source inventory/order drift",
    )
    guard_source_rows: list[dict[str, Any]] = []
    predicate_ids: list[str] = []
    for profile in guard_profiles:
        _require(
            isinstance(profile, dict)
            and list(profile) == ["guard_id", "predicate_id"]
            and isinstance(profile["predicate_id"], str)
            and bool(profile["predicate_id"]),
            "universal trace guard execution profile shape drift",
        )
        guard_id = profile["guard_id"]
        predicate_ids.append(profile["predicate_id"])
        candidate = candidate_by_id.get(guard_id)
        _require(
            isinstance(candidate, Mapping) and candidate.get("role") == "guard",
            f"universal trace guard source candidate drift: {guard_id}",
        )
        runtime_contract = candidate.get("runtime_contract")
        _require(
            isinstance(runtime_contract, Mapping)
            and set(runtime_contract)
            == {"stage", "violation_code", "when_all", "require_all", "outcome"}
            and runtime_contract.get("outcome")
            in {"block", "repair", "requires_bridge"},
            f"universal trace guard runtime source drift: {guard_id}",
        )
        raw_topics = list(candidate["research_topic_ids"])
        raw_provenance = list(candidate["provenance_record_ids"])
        _require(
            len(raw_topics) == len(set(raw_topics))
            and len(raw_provenance) == len(set(raw_provenance)),
            f"universal trace guard provenance duplicates: {guard_id}",
        )
        topics = sorted(raw_topics, key=lambda value: value.encode("utf-8"))
        provenance = sorted(raw_provenance, key=lambda value: value.encode("utf-8"))
        source = {
            "record_id": guard_id,
            "source_candidate_id": guard_id,
            "predicate_id": profile["predicate_id"],
            "role": "guard",
            "evaluation_stage": "postselection_conditional",
            "research_topic_ids": topics,
            "provenance_record_ids": provenance,
            "stage": runtime_contract["stage"],
            "violation_code": runtime_contract["violation_code"],
            "when_all": copy.deepcopy(runtime_contract["when_all"]),
            "require_all": copy.deepcopy(runtime_contract["require_all"]),
            "declared_outcome": runtime_contract["outcome"],
        }
        guard_source_rows.append(
            {
                "record_id": guard_id,
                "source_candidate_id": guard_id,
                "predicate_id": profile["predicate_id"],
                "source_contract_sha256": hashlib.sha256(
                    canonical_json_bytes(source)
                ).hexdigest(),
                **{
                    key: value
                    for key, value in source.items()
                    if key not in {"record_id", "source_candidate_id", "predicate_id"}
                },
            }
        )
    _require(
        len(predicate_ids) == len(set(predicate_ids)) == 32,
        "universal trace guard predicate inventory is not one-to-one",
    )

    compatibility_budget_scopes = {
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
    _require(
        set(compatibility_budget_scopes) == set(expected_budgets),
        "universal trace compatibility-budget scope inventory drift",
    )
    cardinality_limits = [
        {
            "record_id": f"compatibility_budget__{metric_id}",
            "source_kind": "compatibility_budget",
            "metric_id": metric_id,
            "evaluation_stage": "postselection_scene",
            "scope_kind": compatibility_budget_scopes[metric_id][0],
            "scope_id": compatibility_budget_scopes[metric_id][1],
            "minimum": 0,
            "maximum": maximum,
        }
        for metric_id, maximum in expected_budgets.items()
    ]
    runtime_limits = {
        "context_profile_carriers": (
            "postselection_scene",
            "global",
            "context_carrier",
            6,
        ),
        "global_optional_remote": (
            "postselection_scene",
            "global",
            "optional_remote",
            1,
        ),
        "literal_realization_atoms_per_facet": (
            "preselection_reservation",
            "each_facet",
            None,
            2,
        ),
        "literal_realization_atoms_total": (
            "preselection_reservation",
            "global",
            "literal_realization",
            10,
        ),
        "selected_resource_claims_total": (
            "postselection_scene",
            "global",
            "resource_claim",
            32,
        ),
        "selected_visual_atoms_total": (
            "postselection_scene",
            "global",
            "visual_atom",
            18,
        ),
    }
    cardinality_limits.extend(
        {
            "record_id": f"runtime_limit__{metric_id}",
            "source_kind": "runtime_limit",
            "metric_id": metric_id,
            "evaluation_stage": specification[0],
            "scope_kind": specification[1],
            "scope_id": specification[2],
            "minimum": 0,
            "maximum": specification[3],
        }
        for metric_id, specification in runtime_limits.items()
    )
    cardinality_limits.sort(key=lambda row: row["record_id"].encode("utf-8"))
    cardinality_ids = [row["record_id"] for row in cardinality_limits]
    _require(
        cardinality_ids
        == sorted(set(cardinality_ids), key=lambda value: value.encode("utf-8"))
        and len(cardinality_ids) == 20,
        "universal trace cardinality-limit inventory drift",
    )
    return {
        "policy_source_contract_count": len(policy_source_rows),
        "policy_source_contracts_sha256": hashlib.sha256(
            canonical_json_bytes(policy_source_rows)
        ).hexdigest(),
        "guard_source_contract_count": len(guard_source_rows),
        "guard_source_contracts_sha256": hashlib.sha256(
            canonical_json_bytes(guard_source_rows)
        ).hexdigest(),
        "cardinality_limit_count": len(cardinality_ids),
        "cardinality_limits_sha256": hashlib.sha256(
            canonical_json_bytes(cardinality_limits)
        ).hexdigest(),
        "cardinality_limit_ids_sha256": hashlib.sha256(
            canonical_json_bytes(cardinality_ids)
        ).hexdigest(),
    }


def validate_universal_scene_runtime_assets(
    asset_dir: Path,
    research: Mapping[str, Any],
    holdouts: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate executable universal candidates, predicates, and cross-file refs."""

    candidate_path = asset_dir / "illustration_universal_scene_candidates_v1.json"
    compatibility_path = (
        asset_dir / "illustration_universal_compatibility_graph_v1.json"
    )
    semantic_path = asset_dir / "illustration_universal_semantic_bindings_v1.json"
    crosswalk_path = asset_dir / "universal_scene_expectation_crosswalk_v2.json"
    _require(candidate_path.is_file(), "missing universal scene candidate asset")
    _require(compatibility_path.is_file(), "missing universal compatibility asset")
    _require(semantic_path.is_file(), "missing universal semantic-binding asset")
    _require(
        candidate_path.stat().st_size <= 512 * 1024,
        "universal candidate asset exceeds the 512 KiB unsharded limit",
    )
    candidate_asset = _load_json(candidate_path)
    compatibility = _load_json(compatibility_path)
    semantic_asset = _load_json(semantic_path)
    expectation_crosswalk = _load_json(crosswalk_path)
    semantic_effect_policy = _validate_universal_semantic_effect_policy(
        candidate_asset,
        compatibility,
        semantic_asset,
    )

    candidate_top_keys = {
        "schema",
        "reviewed_at",
        "normalization",
        "candidate_role_ids",
        "facet_ids",
        "distance_axis_ids",
        "load_axis_ids",
        "research_packets",
        "research_manifest_sha256",
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
        "semantic_bindings_asset_sha256",
    }
    _require(
        isinstance(candidate_asset, dict)
        and set(candidate_asset) == candidate_top_keys,
        "universal candidate top-level fields mismatch",
    )
    _require(
        candidate_asset.get("schema")
        == "subculture-illustration-universal-scene-candidates/v1",
        "universal candidate schema mismatch",
    )
    _require(
        candidate_asset.get("reviewed_at") == "2026-08-10",
        "universal candidate review date drift",
    )
    _require(
        candidate_asset.get("normalization") == "NFKC+casefold+whitespace-collapse",
        "universal candidate normalization drift",
    )
    _require(
        candidate_asset.get("candidate_role_ids")
        == ["visual_atom", "router", "guard", "metric"],
        "universal candidate role order mismatch",
    )
    facet_ids = _strings(
        candidate_asset.get("facet_ids"), "universal facet IDs", minimum=1
    )
    _require(
        candidate_asset.get("distance_axis_ids") == UNIVERSAL_DISTANCE_AXIS_IDS,
        "universal distance axes mismatch",
    )
    _require(
        candidate_asset.get("load_axis_ids") == UNIVERSAL_LOAD_AXIS_IDS,
        "universal load axes mismatch",
    )
    _require(
        candidate_asset.get("research_manifest_sha256") == research["manifest_sha256"],
        "universal candidate research-manifest hash mismatch",
    )

    research_packets = candidate_asset.get("research_packets")
    _require(
        isinstance(research_packets, list) and len(research_packets) == 6,
        "universal candidate research packet list mismatch",
    )
    expected_packet_core = [
        {
            "path": shard["path"],
            "sha256": shard["sha256"],
            "record_count": shard["record_count"],
        }
        for shard in research["shards"]
    ]
    _require(
        [
            {key: packet.get(key) for key in ("path", "sha256", "record_count")}
            for packet in research_packets
            if isinstance(packet, dict)
        ]
        == expected_packet_core,
        "universal candidate research packets do not exactly match the manifest shards",
    )
    _require(
        all(
            isinstance(packet, dict)
            and set(packet) == {"path", "sha256", "record_count", "topic_ids"}
            for packet in research_packets
        )
        and len([topic for packet in research_packets for topic in packet["topic_ids"]])
        == 20
        and set(topic for packet in research_packets for topic in packet["topic_ids"])
        == set(candidate_asset.get("topic_contributions", {})),
        "universal candidate research packet topic partition mismatch",
    )
    selection_contract = candidate_asset.get("selection_contract")
    _require(
        isinstance(selection_contract, dict),
        "universal candidate selection contract missing",
    )
    for field in (
        "research_candidates_are_not_prompt_tags",
        "research_topic_ids_are_provenance_only",
        "visual_atoms_require_event_spine_binding",
    ):
        _require(
            selection_contract.get(field) is True,
            f"universal selection contract requires {field}=true",
        )
    _require(
        selection_contract.get("router_guard_metric_prompt_emission") == "forbidden",
        "nonvisual prompt emission must be forbidden",
    )
    _require(
        selection_contract.get("unknown_fixed_props")
        == "preserve_as_opaque_and_do_not_invent_affordances",
        "unknown fixed-prop boundary drift",
    )

    candidates = candidate_asset.get("candidates")
    _require(
        isinstance(candidates, list) and candidates,
        "universal executable candidates missing",
    )
    candidate_ids = [item.get("id") for item in candidates if isinstance(item, dict)]
    _require(
        len(candidate_ids) == len(candidates) == len(set(candidate_ids)),
        "universal executable candidate IDs must be unique",
    )
    _require(
        candidate_ids == sorted(candidate_ids),
        "universal executable candidates must use canonical ID order",
    )
    candidate_by_id = {item["id"]: item for item in candidates}
    common_keys = {
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
    }
    role_counts: Counter[str] = Counter()
    pixel_ids: list[str] = []
    topic_contributors: dict[str, set[str]] = defaultdict(set)
    graph_predicate_kinds = set(
        _strings(
            compatibility.get("predicate_kind_ids"),
            "universal predicate kinds",
            minimum=1,
        )
    )
    graph_resource_kind_values = _strings(
        compatibility.get("resource_kind_ids"),
        "universal resource kinds",
        minimum=1,
    )
    _require(
        graph_resource_kind_values == UNIVERSAL_V2_RESOURCE_KINDS
        and len(graph_resource_kind_values)
        == len(set(graph_resource_kind_values))
        == 24,
        "universal compatibility resource kinds must exactly equal the unique closed 24-kind domain",
    )
    graph_resource_kinds = set(graph_resource_kind_values)
    current_contracts_by_case = {
        str(row["case_id"]): row["canonical_scene_contract"]
        for row in _load_jsonl(
            asset_dir / "universal_scene_current_holdout_v2.jsonl"
        )
    }
    composition_literal_carrier_policy = (
        _validate_universal_composition_literal_carriers(
            semantic_asset,
            current_contracts_by_case,
        )
    )
    literal_realization_policy = _validate_universal_literal_realization_profiles(
        semantic_asset,
        candidate_by_id,
        graph_resource_kind_values,
    )
    for candidate in candidates:
        _require(
            isinstance(candidate, dict) and set(candidate) == common_keys,
            f"universal candidate field mismatch: {candidate.get('id') if isinstance(candidate, dict) else '<invalid>'}",
        )
        candidate_id = candidate["id"]
        _require(
            not ({"topic_id", "route_id", "bundle_id"} & set(candidate)),
            f"{candidate_id} owns a route/topic/bundle",
        )
        role = candidate.get("role")
        spec = research["candidate_specs"].get(candidate_id)
        if isinstance(spec, dict):
            _require(
                role == spec["role"] and role in UNIVERSAL_CANDIDATE_ROLE_VALUES,
                f"{candidate_id} research role mismatch",
            )
            _require(
                candidate.get("definition") == spec["definition"],
                f"{candidate_id} research definition drift",
            )
        else:
            _require(
                candidate_id in UNIVERSAL_V2_DERIVED_CANDIDATE_IDS
                and role == "visual_atom"
                and candidate.get("annotation_provenance")
                == {
                    "definition": "design_inference_from_reviewed_research",
                    "pixel_evidence": "design_inference_from_reviewed_research",
                    "runtime_fields": "design_inference",
                }
                and isinstance(candidate.get("definition"), str)
                and bool(candidate["definition"].strip()),
                f"{candidate_id} is not an approved research-derived candidate",
            )
        _require(candidate.get("facet") in facet_ids, f"{candidate_id} facet mismatch")
        topics = _strings(
            candidate.get("research_topic_ids"),
            f"{candidate_id}.research_topic_ids",
            minimum=1,
        )
        if isinstance(spec, dict):
            _require(
                set(topics) == {spec["topic_id"]},
                f"{candidate_id} research topic mismatch",
            )
        else:
            _require(
                set(topics) <= set(research["topic_ids"]),
                f"{candidate_id} derived topic reference mismatch",
            )
        provenance = _strings(
            candidate.get("provenance_record_ids"),
            f"{candidate_id}.provenance_record_ids",
            minimum=1,
        )
        _require(
            set(provenance)
            <= (
                spec["record_ids"]
                if isinstance(spec, dict)
                else set(research["record_ids"])
            ),
            f"{candidate_id} has unreviewed provenance",
        )
        _require(
            candidate.get("direct_source_record_ids") == [],
            f"{candidate_id} overclaims direct source validation",
        )
        aliases = candidate.get("aliases")
        _require(isinstance(aliases, list), f"{candidate_id}.aliases must be a list")
        for alias in aliases:
            if isinstance(alias, str):
                _require(alias.strip(), f"{candidate_id} has an empty alias")
            else:
                _require(
                    isinstance(alias, dict)
                    and set(alias) == {"locale", "values"}
                    and alias.get("locale") in {"en", "ko", "ja", "zh"},
                    f"{candidate_id} localized alias shape mismatch",
                )
                _strings(
                    alias.get("values"),
                    f"{candidate_id}.{alias['locale']}.aliases",
                    minimum=1,
                )
        parameters = candidate.get("parameters")
        _require(
            isinstance(parameters, dict), f"{candidate_id}.parameters must be an object"
        )
        for parameter, values in parameters.items():
            _require(
                isinstance(parameter, str) and parameter and isinstance(values, list),
                f"{candidate_id} parameter enum mismatch",
            )
        preconditions = candidate.get("preconditions")
        capabilities = candidate.get("capabilities")
        _require(
            isinstance(preconditions, dict)
            and set(preconditions) == {"requires_all", "requires_any", "forbids_any"},
            f"{candidate_id} preconditions shape mismatch",
        )
        _require(
            isinstance(capabilities, dict)
            and set(capabilities) == {"requires_all", "requires_any"},
            f"{candidate_id} capabilities shape mismatch",
        )
        for field in ("triggers", "postconditions"):
            _predicate_groups(
                candidate.get(field), f"{candidate_id}.{field}", graph_predicate_kinds
            )
        for field in ("requires_all", "requires_any", "forbids_any"):
            _predicate_groups(
                preconditions[field],
                f"{candidate_id}.preconditions.{field}",
                graph_predicate_kinds,
            )
        for field in ("requires_all", "requires_any"):
            _predicate_groups(
                capabilities[field],
                f"{candidate_id}.capabilities.{field}",
                graph_predicate_kinds,
            )
        bindings = candidate.get("bindings")
        _require(isinstance(bindings, list), f"{candidate_id}.bindings must be a list")
        for binding in bindings:
            _require(
                isinstance(binding, list)
                and len(binding) == 2
                and all(isinstance(value, str) and value for value in binding),
                f"{candidate_id} binding shape mismatch",
            )
        resource_claims = candidate.get("resource_claims")
        _require(
            isinstance(resource_claims, list),
            f"{candidate_id}.resource_claims must be a list",
        )
        for claim in resource_claims:
            _require(
                isinstance(claim, list)
                and len(claim) == 4
                and claim[0] in graph_resource_kinds
                and isinstance(claim[1], str)
                and isinstance(claim[2], int)
                and not isinstance(claim[2], bool)
                and claim[2] >= 1
                and claim[3] in {"exclusive", "shared"},
                f"{candidate_id} resource claim mismatch",
            )
        semantic_distance = candidate.get("semantic_distance")
        _require(
            isinstance(semantic_distance, dict)
            and set(semantic_distance) == {"base", "adjustments"},
            f"{candidate_id} distance shape mismatch",
        )
        _zero_vector(
            semantic_distance["base"],
            UNIVERSAL_DISTANCE_AXIS_IDS,
            f"{candidate_id}.semantic_distance.base",
        )
        _zero_vector(
            candidate.get("semantic_load"),
            UNIVERSAL_LOAD_AXIS_IDS,
            f"{candidate_id}.semantic_load",
        )
        _require(
            isinstance(candidate.get("salience"), dict)
            and set(candidate["salience"]) == {"role", "displacement_cap"},
            f"{candidate_id} salience shape mismatch",
        )
        _require(
            isinstance(candidate.get("render_risk"), dict)
            and set(candidate["render_risk"]) == {"band", "tags"},
            f"{candidate_id} render-risk shape mismatch",
        )
        pixel_evidence = candidate.get("pixel_evidence")
        _require(
            isinstance(pixel_evidence, list),
            f"{candidate_id}.pixel_evidence must be a list",
        )
        runtime_contract = candidate.get("runtime_contract")
        _require(
            isinstance(runtime_contract, dict),
            f"{candidate_id}.runtime_contract missing",
        )
        if role == "visual_atom":
            _require(
                pixel_evidence, f"{candidate_id} visual atom has no pixel obligation"
            )
            expected_runtime_keys = {
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
            }
            _require(
                set(runtime_contract) == expected_runtime_keys,
                f"{candidate_id} visual runtime contract mismatch",
            )
            _require(
                runtime_contract["bindings"] == bindings,
                f"{candidate_id} runtime bindings drift",
            )
            _require(
                runtime_contract["requires_all"] == preconditions["requires_all"],
                f"{candidate_id} runtime requires_all drift",
            )
            _require(
                runtime_contract["requires_any"] == preconditions["requires_any"],
                f"{candidate_id} runtime requires_any drift",
            )
            _require(
                runtime_contract["forbids_any"] == preconditions["forbids_any"],
                f"{candidate_id} runtime forbids_any drift",
            )
            _require(
                runtime_contract["provides"] == candidate["postconditions"],
                f"{candidate_id} runtime provides drift",
            )
            _require(
                runtime_contract["resource_claims"] == resource_claims,
                f"{candidate_id} runtime resource claims drift",
            )
            _require(
                runtime_contract["distance_profile"] == semantic_distance,
                f"{candidate_id} runtime distance drift",
            )
            _require(
                runtime_contract["load_profile"] == candidate["semantic_load"],
                f"{candidate_id} runtime load drift",
            )
            _require(
                runtime_contract["pixel_evidence"] == pixel_evidence,
                f"{candidate_id} runtime pixel evidence drift",
            )
            runtime_bridge_types = _strings(
                runtime_contract["bridge_types"],
                f"{candidate_id}.runtime_contract.bridge_types",
            )
            _require(
                len(runtime_bridge_types) == len(set(runtime_bridge_types))
                and set(runtime_bridge_types) <= set(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS),
                f"{candidate_id} runtime bridge types escape the closed seven-type enum",
            )
            for field in ("requires_all", "requires_any", "forbids_any", "provides"):
                _predicate_groups(
                    runtime_contract[field],
                    f"{candidate_id}.runtime_contract.{field}",
                    graph_predicate_kinds,
                )
            for index, adjustment in enumerate(
                runtime_contract["distance_profile"]["adjustments"]
            ):
                _require(
                    isinstance(adjustment, dict)
                    and set(adjustment) == {"when_all", "operation"},
                    f"{candidate_id} distance adjustment shape mismatch",
                )
                _predicate_groups(
                    adjustment["when_all"],
                    f"{candidate_id}.distance_adjustment[{index}]",
                    graph_predicate_kinds,
                )
        elif role == "router":
            _require(
                pixel_evidence == [] and resource_claims == [],
                f"{candidate_id} nonvisual router exposes visual evidence/resources",
            )
            _require(
                set(runtime_contract)
                == {
                    "stage",
                    "opens_facets",
                    "requires_all",
                    "forbids_any",
                    "deterministic_order",
                },
                f"{candidate_id} router runtime contract mismatch",
            )
            _require(
                set(
                    _strings(
                        runtime_contract["opens_facets"],
                        f"{candidate_id}.opens_facets",
                        minimum=1,
                    )
                )
                <= set(facet_ids),
                f"{candidate_id} opens unknown facet",
            )
            for field in ("requires_all", "forbids_any"):
                _predicate_groups(
                    runtime_contract[field],
                    f"{candidate_id}.runtime_contract.{field}",
                    graph_predicate_kinds,
                )
        elif role == "guard":
            _require(
                pixel_evidence == [] and resource_claims == [],
                f"{candidate_id} nonvisual guard exposes visual evidence/resources",
            )
            _require(
                set(runtime_contract)
                == {"stage", "violation_code", "when_all", "require_all", "outcome"},
                f"{candidate_id} guard runtime contract mismatch",
            )
            _require(
                runtime_contract.get("outcome")
                in {"block", "repair", "requires_bridge"},
                f"{candidate_id} guard outcome mismatch",
            )
            for field in ("when_all", "require_all"):
                _predicate_groups(
                    runtime_contract[field],
                    f"{candidate_id}.runtime_contract.{field}",
                    graph_predicate_kinds,
                )
        else:
            _require(
                pixel_evidence == [] and resource_claims == [],
                f"{candidate_id} nonvisual metric exposes visual evidence/resources",
            )
            _require(
                set(runtime_contract)
                == {"stage", "value_type", "input_ids", "output_axis"},
                f"{candidate_id} metric runtime contract mismatch",
            )
            _require(
                runtime_contract.get("value_type")
                in {"ordinal_0_3", "count", "boolean", "band"},
                f"{candidate_id} metric type mismatch",
            )
            _strings(
                runtime_contract.get("input_ids"),
                f"{candidate_id}.input_ids",
                minimum=1,
            )
        for pixel in pixel_evidence:
            _require(
                isinstance(pixel, dict)
                and set(pixel) == {"id", "kind", "definition", "minimum_scale_ids"}
                and isinstance(pixel.get("id"), str)
                and isinstance(pixel.get("definition"), str)
                and pixel["definition"].strip(),
                f"{candidate_id} pixel evidence shape mismatch",
            )
            _require(
                pixel.get("kind")
                in {
                    "contact",
                    "orientation",
                    "state_boundary",
                    "support",
                    "path",
                    "residue",
                    "display",
                },
                f"{candidate_id} pixel evidence kind mismatch",
            )
            _require(
                set(
                    _strings(
                        pixel.get("minimum_scale_ids"),
                        f"{candidate_id}.{pixel['id']}.minimum_scale_ids",
                        minimum=1,
                    )
                )
                <= {"native", "thumbnail_320px"},
                f"{candidate_id} pixel scale mismatch",
            )
            pixel_ids.append(pixel["id"])
        role_counts[role] += 1
        for topic_id in topics:
            topic_contributors[topic_id].add(candidate_id)

    _require(
        {
            candidate_id
            for candidate_id in candidate_ids
            if candidate_id not in research["candidate_specs"]
        }
        == UNIVERSAL_V2_DERIVED_CANDIDATE_IDS,
        "universal research-derived candidate inventory drift",
    )

    _require(
        len(pixel_ids) == len(set(pixel_ids)),
        "universal executable pixel evidence IDs must be unique",
    )
    _require(
        len(candidates) == 127
        and dict(role_counts)
        == {"visual_atom": 65, "router": 21, "guard": 32, "metric": 9}
        and len(pixel_ids) == 76,
        "universal executable candidate/role/pixel inventory drift",
    )
    visual_owner_mapping_policy = (
        _validate_universal_visual_owner_mapping_realizability(
            expectation_crosswalk,
            candidate_by_id,
        )
    )
    fixed_prop_eligibility_policy = (
        _validate_universal_fixed_prop_eligibility_source_contract(
            candidate_by_id,
        )
    )
    pixel_owner_by_id = {
        pixel["id"]: candidate["id"]
        for candidate in candidates
        for pixel in candidate["pixel_evidence"]
    }
    proposal_profiles = candidate_asset.get("proposal_profiles")
    _require(
        isinstance(proposal_profiles, list) and len(proposal_profiles) == 12,
        "universal proposal-profile inventory mismatch",
    )
    proposal_keys = {
        "id",
        "semantic_family_id",
        "semantic_family_payload",
        "semantic_family_signature",
        "candidate_ids",
        "slot_id",
        "eligible_slot_states",
        "value_id",
        "prompt_phrase_en",
        "carrier_lexeme_groups",
        "requires_all",
        "forbids_any",
        "event_roles",
        "distance_profile",
        "load_profile",
        "bridge_types",
        "pixel_evidence_ids",
        "remote_or_high_load",
        "policy_mode",
    }
    compatibility_bridge_policy = compatibility.get("bridge_policy")
    _require(
        isinstance(compatibility_bridge_policy, dict),
        "universal compatibility bridge policy missing",
    )
    allowed_bridge_types = set(
        _strings(
            compatibility_bridge_policy.get("bridge_type_ids"),
            "universal bridge types",
            minimum=1,
        )
    )
    bridge_categories = compatibility_bridge_policy.get("category_members")
    _require(
        isinstance(bridge_categories, dict)
        and set(bridge_categories) == {"entry", "mediation", "exit"},
        "universal bridge categories mismatch",
    )
    category_members = {
        category: set(
            _strings(values, f"universal bridge category {category}", minimum=1)
        )
        for category, values in bridge_categories.items()
    }
    proposal_ids: set[str] = set()
    semantic_family_ids: set[str] = set()
    semantic_family_signatures: set[str] = set()
    proposal_band_counts: Counter[str] = Counter()
    raw_prop_concepts = candidate_asset.get("prop_concepts")
    _require(
        isinstance(raw_prop_concepts, list),
        "universal prop catalog must be an array",
    )
    proposal_prop_concept_ids = {
        str(prop["id"])
        for prop in raw_prop_concepts
        if isinstance(prop, dict) and isinstance(prop.get("id"), str)
    }
    for profile in proposal_profiles:
        profile_id = profile.get("id") if isinstance(profile, dict) else "<invalid>"
        _require(
            isinstance(profile, dict) and set(profile) == proposal_keys,
            f"universal proposal profile shape mismatch: {profile_id}",
        )
        family_id = profile.get("semantic_family_id")
        family_signature = profile.get("semantic_family_signature")
        _require(
            isinstance(profile_id, str)
            and profile_id
            and profile_id not in proposal_ids
            and isinstance(family_id, str)
            and family_id
            and family_id not in semantic_family_ids
            and isinstance(family_signature, str)
            and re.fullmatch(r"[0-9a-f]{64}", family_signature) is not None
            and family_signature not in semantic_family_signatures,
            "universal proposal semantic family IDs/signatures must be unique",
        )
        proposal_ids.add(profile_id)
        semantic_family_ids.add(family_id)
        semantic_family_signatures.add(family_signature)
        _require(
            profile.get("slot_id") == "prop"
            and profile.get("eligible_slot_states") == ["open"],
            f"{profile_id} must remain an open-prop proposal",
        )
        value_id = profile.get("value_id")
        expected_policy = {
            "prop_apple": "ordinary",
            "prop_hammer": "safe_tool",
        }.get(value_id)
        _require(
            expected_policy is not None,
            f"{profile_id} open proposal uses an unreviewed prop",
        )
        _require(
            profile.get("policy_mode") == expected_policy,
            f"{profile_id} value/policy contract drift",
        )
        prompt_phrase = profile.get("prompt_phrase_en")
        _require(
            isinstance(prompt_phrase, str)
            and prompt_phrase.strip() == prompt_phrase
            and 1 <= len(prompt_phrase.split()) <= 80,
            f"{profile_id} prompt phrase mismatch",
        )
        carrier_groups = profile.get("carrier_lexeme_groups")
        _require(
            isinstance(carrier_groups, list)
            and 1 <= len(carrier_groups) <= 2
            and all(
                isinstance(group, list)
                and group
                and len(group) == len(set(group))
                and all(
                    isinstance(alternative, str)
                    and alternative == " ".join(alternative.casefold().split())
                    and re.fullmatch(r"[a-z0-9 ]+", alternative) is not None
                    for alternative in group
                )
                for group in carrier_groups
            ),
            f"{profile_id} carrier lexeme groups are not closed natural English",
        )
        requires_all = _predicate_groups(
            profile.get("requires_all"),
            f"{profile_id}.requires_all",
            graph_predicate_kinds,
        )
        forbids_any = _predicate_groups(
            profile.get("forbids_any"),
            f"{profile_id}.forbids_any",
            graph_predicate_kinds,
        )
        eligibility_tokens = {
            token.casefold().replace("-", "_")
            for predicate in requires_all + forbids_any
            for token in predicate
        }
        _require(
            not any(
                marker in token
                for token in eligibility_tokens
                for marker in (
                    "creativ",
                    "seed",
                    "target_band",
                    "selected_band",
                    "semantic_distance",
                )
            ),
            f"{profile_id} eligibility improperly depends on creativity or tie-break state",
        )
        proposal_candidate_ids = _strings(
            profile.get("candidate_ids"),
            f"{profile_id}.candidate_ids",
            minimum=1,
        )
        _require(
            len(proposal_candidate_ids) == len(set(proposal_candidate_ids))
            and set(proposal_candidate_ids) <= set(candidate_ids)
            and all(
                candidate_by_id[candidate_id]["role"] == "visual_atom"
                for candidate_id in proposal_candidate_ids
            ),
            f"{profile_id} candidate refs must be unique visual atoms",
        )
        proposal_pixel_ids = _strings(
            profile.get("pixel_evidence_ids"),
            f"{profile_id}.pixel_evidence_ids",
            minimum=1,
        )
        expected_pixel_ids = [
            pixel["id"]
            for candidate_id in proposal_candidate_ids
            for pixel in candidate_by_id[candidate_id]["pixel_evidence"]
        ]
        _require(
            proposal_pixel_ids == expected_pixel_ids
            and all(
                pixel_owner_by_id[pixel_id] in proposal_candidate_ids
                for pixel_id in proposal_pixel_ids
            ),
            f"{profile_id} pixel-evidence refs do not exactly cover its atoms",
        )
        event_roles = profile.get("event_roles")
        _require(
            isinstance(event_roles, dict)
            and list(event_roles) == UNIVERSAL_EVENT_ROLE_IDS
            and all(
                value is None or isinstance(value, str) and value
                for value in event_roles.values()
            )
            and event_roles["actor"] == "$identity_actor"
            and event_roles["location"] == "$scene_location"
            and all(
                isinstance(event_roles[role_id], str) and event_roles[role_id]
                for role_id in ("action", "target", "result", "phase")
            ),
            f"{profile_id} must provide the exact eight-role event frame",
        )
        _require(
            _normalize_universal_semantic_family_value(profile["slot_id"]) != "null"
            and _normalize_universal_semantic_family_value(value_id) != "null"
            and all(
                role_value is None
                or _normalize_universal_semantic_family_value(role_value) != "null"
                for role_value in event_roles.values()
            ),
            f"{profile_id} collides with the reserved null semantic-family sentinel",
        )
        distance_vector = _zero_vector(
            profile.get("distance_profile"),
            UNIVERSAL_DISTANCE_AXIS_IDS,
            f"{profile_id}.distance_profile",
        )
        _zero_vector(
            profile.get("load_profile"),
            UNIVERSAL_LOAD_AXIS_IDS,
            f"{profile_id}.load_profile",
        )
        expected_band = _universal_distance_band(distance_vector)
        proposal_band_counts[expected_band] += 1
        _require(
            profile.get("remote_or_high_load") is (expected_band == "far"),
            f"{profile_id} remote/high-load declaration disagrees with its recomputed band",
        )
        family_payload = _universal_semantic_family_payload(
            profile,
            candidate_by_id,
            proposal_prop_concept_ids,
        )
        _require(
            profile.get("semantic_family_payload") == family_payload
            and family_signature
            == hashlib.sha256(canonical_json_bytes(family_payload)).hexdigest(),
            f"{profile_id} semantic family signature is not independently reproducible",
        )
        if profile_id == "proposal_open_near_apple_inspection":
            _require(
                family_signature
                == "89805a24fc91b414199c257ca9c1420aae18868f0faf1f2960bfcdf31cb8cc0d",
                "universal canonical apple semantic family positive control drift",
            )
        profile_bridge_types = _strings(
            profile.get("bridge_types"),
            f"{profile_id}.bridge_types",
            minimum=1,
        )
        _require(
            len(profile_bridge_types) == len(set(profile_bridge_types))
            and set(profile_bridge_types) <= allowed_bridge_types,
            f"{profile_id} bridge types are invalid or duplicated",
        )
        bridge_candidate_types = {
            bridge_type
            for candidate_id in proposal_candidate_ids
            if candidate_by_id[candidate_id]["facet"] == "bridge"
            for bridge_type in candidate_by_id[candidate_id]["runtime_contract"][
                "bridge_types"
            ]
        }
        _require(
            set(profile_bridge_types) == bridge_candidate_types,
            f"{profile_id} bridge list does not match its bridge atoms",
        )
        required_categories = {
            "near": ("entry",),
            "middle": ("entry", "exit"),
            "far": ("entry", "mediation", "exit"),
        }[expected_band]
        _require(
            all(
                set(profile_bridge_types) & category_members[category]
                for category in required_categories
            ),
            f"{profile_id} lacks required {expected_band} bridge categories",
        )
        if expected_band == "far":
            _require(
                "usl_core_identity_anchor" in proposal_candidate_ids,
                f"{profile_id} far proposal lacks a visible core identity anchor",
            )
    _require(
        proposal_band_counts == Counter({"near": 4, "middle": 4, "far": 4}),
        "universal proposals must retain four distinct semantic families per distance band",
    )
    context_profiles = candidate_asset.get("context_distance_profiles")
    _require(
        isinstance(context_profiles, list)
        and len(context_profiles) == 18
        and len(
            {
                profile.get("id")
                for profile in context_profiles
                if isinstance(profile, dict)
            }
        )
        == 18,
        "universal context-distance profile inventory/order drift",
    )
    _require(
        sum(
            isinstance(profile, Mapping)
            and profile.get("id") == "context_quiet_theme_guard_middle"
            for profile in context_profiles
        )
        == 1,
        "universal quiet-theme source profile must exist exactly once",
    )
    context_profile_keys = {
        "id",
        "carrier_candidate_id",
        "candidate_ids",
        "requires_all",
        "requires_any",
        "forbids_any",
        "distance_profile",
        "load_profile",
        "bridge_types",
        "pixel_evidence_ids",
        "policy_mode",
    }
    context_band_counts: Counter[str] = Counter()
    for profile in context_profiles:
        profile_id = profile.get("id") if isinstance(profile, dict) else "<invalid>"
        _require(
            isinstance(profile, dict) and set(profile) == context_profile_keys,
            f"universal context-distance profile shape mismatch: {profile_id}",
        )
        _require(
            profile.get("policy_mode")
            in {"ordinary", "safe_tool", "explicit_weapon_only"},
            f"{profile_id} context policy mode mismatch",
        )
        predicates: list[list[str]] = []
        for field in ("requires_all", "requires_any", "forbids_any"):
            predicates.extend(
                _predicate_groups(
                    profile.get(field),
                    f"{profile_id}.{field}",
                    graph_predicate_kinds,
                )
            )
        eligibility_tokens = {
            token.casefold().replace("-", "_")
            for predicate in predicates
            for token in predicate
        }
        _require(
            not any(
                marker in token
                for token in eligibility_tokens
                for marker in (
                    "creativ",
                    "seed",
                    "target_band",
                    "selected_band",
                    "semantic_distance",
                    "case_id",
                    "request_text",
                    "request_phrase",
                    "regex",
                )
            )
            and not re.search(
                r"universal_scene_[0-9]+",
                json.dumps(profile, ensure_ascii=False).casefold(),
            ),
            f"{profile_id} eligibility depends on creativity, seed, or a frozen holdout literal",
        )
        carrier_ids = _strings(
            profile.get("candidate_ids"),
            f"{profile_id}.candidate_ids",
            minimum=1,
        )
        _require(
            len(carrier_ids) == len(set(carrier_ids))
            and set(carrier_ids) <= set(candidate_ids)
            and all(
                candidate_by_id[candidate_id]["role"] == "visual_atom"
                for candidate_id in carrier_ids
            ),
            f"{profile_id} carriers must be unique visual candidates",
        )
        _require(
            profile.get("carrier_candidate_id") in carrier_ids
            and profile.get("carrier_candidate_id") != "usl_core_identity_anchor",
            f"{profile_id} must name one selected non-core overlay carrier",
        )
        context_pixel_ids = _strings(
            profile.get("pixel_evidence_ids"),
            f"{profile_id}.pixel_evidence_ids",
            minimum=1,
        )
        expected_context_pixel_ids = [
            pixel["id"]
            for candidate_id in carrier_ids
            for pixel in candidate_by_id[candidate_id]["pixel_evidence"]
        ]
        _require(
            context_pixel_ids == expected_context_pixel_ids
            and all(
                pixel_owner_by_id[pixel_id] in carrier_ids
                for pixel_id in context_pixel_ids
            ),
            f"{profile_id} pixel evidence does not exactly cover its carriers",
        )
        distance_vector = _zero_vector(
            profile.get("distance_profile"),
            UNIVERSAL_DISTANCE_AXIS_IDS,
            f"{profile_id}.distance_profile",
        )
        _zero_vector(
            profile.get("load_profile"),
            UNIVERSAL_LOAD_AXIS_IDS,
            f"{profile_id}.load_profile",
        )
        if profile_id == "context_quiet_theme_guard_middle":
            _validate_universal_quiet_theme_source_contract(
                profile,
                candidate_by_id,
            )
        band = _universal_distance_band(distance_vector)
        context_band_counts[band] += 1
        profile_bridge_types = _strings(
            profile.get("bridge_types"),
            f"{profile_id}.bridge_types",
            minimum=1,
        )
        minimum_bridge_count = {
            "near": compatibility_bridge_policy.get("near_minimum"),
            "middle": compatibility_bridge_policy.get("middle_minimum"),
            "far": compatibility_bridge_policy.get("far_minimum"),
        }[band]
        _require(
            isinstance(minimum_bridge_count, int)
            and len(profile_bridge_types) >= minimum_bridge_count
            and len(profile_bridge_types) == len(set(profile_bridge_types))
            and set(profile_bridge_types) <= allowed_bridge_types,
            f"{profile_id} bridge count/types do not satisfy its recomputed band",
        )
        required_categories = {
            "near": ("entry",),
            "middle": ("entry", "exit"),
            "far": ("entry", "mediation", "exit"),
        }[band]
        _require(
            all(
                set(profile_bridge_types) & category_members[category]
                for category in required_categories
            ),
            f"{profile_id} lacks required {band} bridge categories",
        )
        if band == "far":
            _require(
                "usl_core_identity_anchor" in carrier_ids,
                f"{profile_id} far context profile lacks the global core anchor",
            )
    _require(
        context_band_counts == Counter({"near": 7, "middle": 9, "far": 2}),
        "universal context-distance near/middle/far inventory drift",
    )
    contributions = candidate_asset.get("topic_contributions")
    _require(
        isinstance(contributions, dict)
        and set(contributions) == set(research["topic_ids"]),
        "universal topic contributions must cover all 20 topics",
    )
    for topic_id, ids in contributions.items():
        values = _strings(ids, f"topic_contributions.{topic_id}", minimum=1)
        _require(
            set(values) <= set(candidate_ids),
            f"{topic_id} contribution references unknown candidate",
        )
        _require(
            all(
                topic_id in candidate_by_id[value]["research_topic_ids"]
                for value in values
            ),
            f"{topic_id} contribution has cross-topic candidate",
        )
        _require(
            set(values) == topic_contributors[topic_id],
            f"{topic_id} contribution list is incomplete",
        )

    no_prop = candidate_asset.get("no_prop_path")
    _require(isinstance(no_prop, dict), "universal no-prop path missing")
    _require(
        no_prop.get("activation_predicate") == ["slot", "prop", "closed"],
        "universal no-prop activation drift",
    )
    _require(
        set(
            _strings(
                no_prop.get("blocked_facets"), "no_prop_path.blocked_facets", minimum=2
            )
        )
        == {"prop", "prop_state"},
        "universal no-prop blocked facets mismatch",
    )
    _require(
        set(
            _strings(
                no_prop.get("closed_event_roles"),
                "no_prop_path.closed_event_roles",
                minimum=1,
            )
        )
        == {"instrument"},
        "universal no-prop event role mismatch",
    )
    _require(
        set(
            _strings(
                no_prop.get("allowed_realization_candidate_ids"),
                "no_prop_path.allowed_realization_candidate_ids",
                minimum=1,
            )
        )
        <= set(candidate_ids),
        "universal no-prop path has unknown candidate",
    )
    nonhuman = candidate_asset.get("nonhuman_path")
    _require(
        isinstance(nonhuman, dict)
        and nonhuman.get("human_channel_fabrication") == "forbidden",
        "universal nonhuman boundary mismatch",
    )
    for field in ("capability_router_candidate_id", "substitution_router_candidate_id"):
        _require(
            nonhuman.get(field) in candidate_by_id
            and candidate_by_id[nonhuman[field]]["role"] == "router",
            f"universal nonhuman {field} mismatch",
        )
    _require(
        set(
            _strings(
                nonhuman.get("available_channel_candidate_ids"),
                "nonhuman_path.available_channel_candidate_ids",
                minimum=1,
            )
        )
        <= set(candidate_ids),
        "universal nonhuman channel candidate mismatch",
    )

    props = candidate_asset.get("prop_concepts")
    _require(
        isinstance(props, list) and len(props) == 4,
        "universal prop catalog must contain four concepts",
    )
    prop_ids = [prop.get("id") for prop in props if isinstance(prop, dict)]
    _require(
        prop_ids
        == [
            "prop_apple",
            "prop_wooden_mallet",
            "prop_hammer",
            "prop_decommissioned_machine_gun",
        ],
        "universal prop catalog order/IDs mismatch",
    )
    previous_load: tuple[int, int, int] | None = None
    for prop in props:
        _require(
            set(prop)
            == {
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
            f"{prop.get('id')} prop shape mismatch",
        )
        aliases = prop.get("aliases")
        _require(
            isinstance(aliases, list)
            and [item.get("locale") for item in aliases if isinstance(item, dict)]
            == ["en", "ko", "ja", "zh"],
            f"{prop['id']} locale aliases mismatch",
        )
        for alias in aliases:
            _require(
                isinstance(alias, dict) and set(alias) == {"locale", "values"},
                f"{prop['id']} alias shape mismatch",
            )
            _strings(
                alias.get("values"),
                f"{prop['id']}.{alias['locale']}.aliases",
                minimum=1,
            )
        _require(
            set(
                _strings(
                    prop.get("affordance_candidate_ids"),
                    f"{prop['id']}.affordance_candidate_ids",
                    minimum=1,
                )
            )
            <= set(candidate_ids),
            f"{prop['id']} affordance reference mismatch",
        )
        _require(
            set(_strings(prop.get("state_ids"), f"{prop['id']}.state_ids", minimum=1))
            <= set(candidate_ids),
            f"{prop['id']} state reference mismatch",
        )
        _require(
            set(
                _strings(
                    prop.get("provenance_record_ids"),
                    f"{prop['id']}.provenance_record_ids",
                    minimum=1,
                )
            )
            <= research["record_ids"],
            f"{prop['id']} provenance reference mismatch",
        )
        _zero_vector(
            prop.get("base_distance_profile"),
            UNIVERSAL_DISTANCE_AXIS_IDS,
            f"{prop['id']}.base_distance_profile",
        )
        load = _zero_vector(
            prop.get("base_load_profile"),
            UNIVERSAL_LOAD_AXIS_IDS,
            f"{prop['id']}.base_load_profile",
        )
        current_load = (load["physical"], load["violence"], load["visual_salience"])
        if previous_load is not None:
            _require(
                sum(current_load) > sum(previous_load),
                "apple/mallet/hammer/machine-gun aggregate load must strictly increase",
            )
        previous_load = current_load
    machine_gun = props[-1]
    machine_gun_candidate_ids = {
        *machine_gun["affordance_candidate_ids"],
        *machine_gun["state_ids"],
        "uao_global_prop_decommissioned_machine_gun",
    }
    for profile in proposal_profiles:
        serialized_profile = json.dumps(profile, ensure_ascii=False).casefold()
        _require(
            not (set(profile["candidate_ids"]) & machine_gun_candidate_ids)
            and "machine_gun" not in serialized_profile
            and "machine gun" not in serialized_profile,
            f"{profile['id']} must not activate a weapon through an open-slot proposal",
        )

    embodiments = candidate_asset.get("embodiment_profiles")
    _require(
        isinstance(embodiments, list) and embodiments,
        "universal embodiment profiles missing",
    )
    embodiment_by_id: dict[str, dict[str, int]] = {}
    for profile in embodiments:
        _require(
            isinstance(profile, dict)
            and set(profile)
            == {
                "id",
                "capability_capacities",
                "unavailable_channels",
                "support_types",
                "provenance_record_ids",
            },
            "universal embodiment profile shape mismatch",
        )
        profile_id = profile.get("id")
        _require(
            isinstance(profile_id, str)
            and profile_id
            and profile_id not in embodiment_by_id,
            "universal embodiment profile ID mismatch",
        )
        capacities: dict[str, int] = {}
        raw_capacities = profile.get("capability_capacities")
        _require(
            isinstance(raw_capacities, list),
            f"{profile_id} capability capacities invalid",
        )
        for capacity in raw_capacities:
            _require(
                isinstance(capacity, dict)
                and set(capacity) == {"id", "capacity"}
                and isinstance(capacity.get("id"), str)
                and isinstance(capacity.get("capacity"), int)
                and not isinstance(capacity["capacity"], bool)
                and capacity["capacity"] >= 0,
                f"{profile_id} capability capacity mismatch",
            )
            _require(
                capacity["id"] not in capacities, f"{profile_id} duplicate capability"
            )
            capacities[capacity["id"]] = capacity["capacity"]
        _strings(
            profile.get("unavailable_channels"),
            f"{profile_id}.unavailable_channels",
            minimum=0,
        )
        _strings(profile.get("support_types"), f"{profile_id}.support_types", minimum=0)
        _require(
            set(
                _strings(
                    profile.get("provenance_record_ids"),
                    f"{profile_id}.provenance_record_ids",
                    minimum=1,
                )
            )
            <= research["record_ids"],
            f"{profile_id} embodiment provenance mismatch",
        )
        embodiment_by_id[profile_id] = capacities

    for case_id, contract in holdouts["scene_contracts_by_case"].items():
        for entity in contract["identity_core"]["entities"]:
            profile_id = entity["embodiment_profile_id"]
            for capability in entity["capabilities"]:
                if capability["source"] != "embodiment_profile":
                    continue
                _require(
                    profile_id in embodiment_by_id,
                    f"{case_id} references missing embodiment profile {profile_id}",
                )
                _require(
                    embodiment_by_id[profile_id].get(capability["id"])
                    == capability["capacity"],
                    f"{case_id} capability differs from profile {profile_id}:{capability['id']}",
                )

    counts = candidate_asset.get("counts")
    _require(isinstance(counts, dict), "universal candidate counts missing")
    _require(
        counts.get("research_records") == 60
        and counts.get("research_topics") == 20
        and counts.get("research_sources") == 40
        and counts.get("research_candidates") == 220,
        "universal candidate research counts drift",
    )
    _require(
        counts.get("executable_candidates") == len(candidates),
        "universal executable candidate count mismatch",
    )
    _require(
        counts.get("executable_by_role") == dict(role_counts),
        "universal executable role counts mismatch",
    )
    _require(
        counts.get("pixel_evidence_records") == len(pixel_ids),
        "universal executable pixel count mismatch",
    )
    _require(counts.get("prop_concepts") == len(props), "universal prop count mismatch")
    _require(
        counts.get("embodiment_profiles") == len(embodiments),
        "universal embodiment count mismatch",
    )
    _require(
        counts.get("proposal_profiles") == len(proposal_profiles) == 12,
        "universal proposal-profile count mismatch",
    )
    _require(
        counts.get("context_distance_profiles") == len(context_profiles) == 18,
        "universal context-distance profile count mismatch",
    )

    compatibility_top_keys = {
        "schema",
        "reviewed_at",
        "candidate_asset_sha256",
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
        "semantic_bindings_asset_sha256",
    }
    _require(
        isinstance(compatibility, dict)
        and set(compatibility) == compatibility_top_keys,
        "universal compatibility top-level fields mismatch",
    )
    _require(
        compatibility.get("schema")
        == "subculture-illustration-universal-compatibility/v1",
        "universal compatibility schema mismatch",
    )
    _require(
        compatibility.get("candidate_asset_sha256") == _sha256(candidate_path),
        "universal compatibility candidate hash mismatch",
    )
    semantic_sha256 = _sha256(semantic_path)
    _require(
        candidate_asset.get("semantic_bindings_asset_sha256") == semantic_sha256
        and compatibility.get("semantic_bindings_asset_sha256") == semantic_sha256,
        "universal semantic-binding raw hash mismatch",
    )
    _require(
        not _forbidden_pair_structures(compatibility),
        f"universal compatibility contains forbidden pair structures: {_forbidden_pair_structures(compatibility)}",
    )
    decision_reason_code_ids = _strings(
        compatibility.get("decision_reason_code_ids"),
        "universal decision reason-code registry",
        minimum=len(UNIVERSAL_DECISION_REASON_CODE_IDS),
    )
    _require(
        decision_reason_code_ids == UNIVERSAL_DECISION_REASON_CODE_IDS
        and decision_reason_code_ids == sorted(set(decision_reason_code_ids)),
        "universal decision reason-code registry must equal the frozen 29-code domain",
    )
    _require(
        compatibility.get("slot_state_contract", {}).get("enum")
        == ["fixed", "closed", "open"],
        "universal slot state enum mismatch",
    )
    event_contract = compatibility.get("event_spine_contract")
    _require(
        isinstance(event_contract, dict)
        and event_contract.get("root_count") == 1
        and event_contract.get("phase_count") == 1
        and event_contract.get("second_independent_premise") == "block"
        and event_contract.get("orphan_atom") == "block",
        "universal one-event-spine contract mismatch",
    )
    budgets = compatibility.get("budgets")
    _require(
        isinstance(budgets, dict)
        and budgets.get("event_spines") == 1
        and budgets.get("primary_actions") == 1
        and budgets.get("phases") == 1
        and budgets.get("optional_props") == 1
        and budgets.get("remote_or_high_load_optional_premises") == 1
        and budgets.get("second_independent_premises") == 0
        and budgets.get("orphan_atoms") == 0,
        "universal fixed budgets mismatch",
    )
    solver = compatibility.get("solver")
    _require(
        isinstance(solver, dict)
        and solver.get("selection_mode") == "predicate_beam_v1"
        and solver.get("beam_width") == 8
        and solver.get("max_candidates_per_facet_before_beam") == 3
        and solver.get("seed_is_final_tiebreak_only") is True,
        "universal solver contract mismatch",
    )
    distance_policy = compatibility.get("distance_policy")
    _require(
        isinstance(distance_policy, dict)
        and distance_policy.get("axis_ids") == UNIVERSAL_DISTANCE_AXIS_IDS
        and distance_policy.get("value_type") == "ordinal_0_3",
        "universal distance policy mismatch",
    )
    creativity_bands = distance_policy.get("creativity_bands")
    _require(
        isinstance(creativity_bands, list)
        and [band.get("id") for band in creativity_bands if isinstance(band, dict)]
        == ["low", "middle", "high"],
        "universal creativity-band IDs mismatch",
    )
    _require(
        [
            (
                band.get("lower"),
                band.get("lower_inclusive"),
                band.get("upper"),
                band.get("upper_inclusive"),
                band.get("target_band"),
            )
            for band in creativity_bands
        ]
        == [
            (0.0, True, 0.25, False, "near"),
            (0.25, True, 0.75, False, "middle"),
            (0.75, True, 1.0, True, "far"),
        ],
        "universal creativity boundaries must be [0,.25), [.25,.75), [.75,1]",
    )
    _require(
        set(distance_policy.get("creativity_changes", []))
        == {"eligible_distance_band_weight"},
        "creativity may change only the distance distribution",
    )
    _require(
        {
            "identity",
            "fixed_or_closed_slots",
            "feasibility",
            "resource_capacity",
            "policy",
            "culture_scope",
            "candidate_count",
            "event_spine_count",
        }
        <= set(distance_policy.get("creativity_never_changes", [])),
        "creativity hard-gate invariants incomplete",
    )
    bridge_policy = compatibility.get("bridge_policy")
    _require(isinstance(bridge_policy, dict), "universal bridge policy missing")
    _require(
        bridge_policy.get("middle_minimum") >= 2
        and bridge_policy.get("far_minimum") >= 3,
        "middle/far bridge minimum was weakened",
    )
    bridge_types = set(
        _strings(
            bridge_policy.get("bridge_type_ids"), "universal bridge types", minimum=1
        )
    )
    _require(
        bridge_types == set(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS)
        and len(bridge_policy["bridge_type_ids"])
        == len(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS),
        "universal compatibility bridge enum must be exactly the closed seven types",
    )
    _require(
        {"affordance", "motivation", "identity_contrast"} <= bridge_types,
        "universal entry bridge types missing",
    )
    _require(
        {"mechanics", "ownership"} <= bridge_types,
        "universal mediation bridge types missing",
    )
    _require(
        {"state_change", "consequence"} <= bridge_types,
        "universal exit bridge types missing",
    )
    _require(
        bridge_policy.get("bridge_requires_pixel_evidence") is True
        and bridge_policy.get("explanation_only_bridge") == "block",
        "universal bridge evidence boundary mismatch",
    )
    universal_rules = compatibility.get("universal_rules")
    _require(
        isinstance(universal_rules, list)
        and len(universal_rules) == len(UNIVERSAL_RULE_REASON_CODES),
        "universal-rule inventory mismatch",
    )
    universal_rule_ids: list[str] = []
    for rule in universal_rules:
        rule_id = rule.get("id") if isinstance(rule, dict) else "<invalid>"
        _require(
            isinstance(rule, dict)
            and set(rule)
            == {"id", "when_all", "outcome", "reason_code", "candidate_scope"}
            and isinstance(rule_id, str)
            and rule_id in UNIVERSAL_RULE_REASON_CODES
            and rule_id not in universal_rule_ids,
            f"universal-rule source shape/ID mismatch: {rule_id}",
        )
        universal_rule_ids.append(rule_id)
        _predicate_groups(
            rule["when_all"],
            f"universal rule {rule_id}.when_all",
            graph_predicate_kinds,
        )
        _require(
            rule["outcome"] in {"block", "repair", "allow_with_bridge"}
            and rule["reason_code"] == UNIVERSAL_RULE_REASON_CODES[rule_id]
            and rule["reason_code"] in decision_reason_code_ids
            and isinstance(rule["candidate_scope"], str)
            and bool(rule["candidate_scope"]),
            f"universal-rule source contract drift: {rule_id}",
        )
    _require(
        set(universal_rule_ids) == set(UNIVERSAL_RULE_REASON_CODES),
        "universal-rule source inventory is incomplete",
    )
    for role, field in (
        ("guard", "guard_candidate_ids"),
        ("router", "router_candidate_ids"),
        ("metric", "metric_candidate_ids"),
    ):
        ids = _strings(compatibility.get(field), f"compatibility.{field}", minimum=1)
        _require(
            ids
            == sorted(
                candidate_id
                for candidate_id, candidate in candidate_by_id.items()
                if candidate["role"] == role
            ),
            f"compatibility.{field} mismatch",
        )
    exceptions = compatibility.get("exception_rules")
    _require(isinstance(exceptions, list), "universal exception rules must be a list")
    exception_ids: set[str] = set()
    for exception in exceptions:
        _require(
            isinstance(exception, dict)
            and set(exception)
            == {
                "id",
                "candidate_ids",
                "when_all",
                "outcome",
                "reason",
                "provenance_record_ids",
            },
            "universal exception rule shape mismatch",
        )
        _require(
            exception.get("id") not in exception_ids, "duplicate universal exception ID"
        )
        exception_ids.add(exception["id"])
        _require(
            set(
                _strings(
                    exception.get("candidate_ids"),
                    f"{exception['id']}.candidate_ids",
                    minimum=1,
                )
            )
            <= set(candidate_ids),
            f"{exception['id']} candidate ref mismatch",
        )
        _predicate_groups(
            exception.get("when_all"),
            f"{exception['id']}.when_all",
            graph_predicate_kinds,
        )
        _require(
            set(
                _strings(
                    exception.get("provenance_record_ids"),
                    f"{exception['id']}.provenance_record_ids",
                    minimum=1,
                )
            )
            <= research["record_ids"],
            f"{exception['id']} provenance ref mismatch",
        )
    compatibility_counts = compatibility.get("counts")
    _require(
        isinstance(compatibility_counts, dict), "universal compatibility counts missing"
    )
    _require(
        compatibility_counts.get("guard_candidates") == role_counts["guard"]
        and compatibility_counts.get("router_candidates") == role_counts["router"]
        and compatibility_counts.get("metric_candidates") == role_counts["metric"]
        and compatibility_counts.get("exception_rules") == len(exceptions)
        and compatibility_counts.get("pairwise_candidate_edges") == 0,
        "universal compatibility counts mismatch",
    )
    trace_source_authorities = _validate_universal_trace_source_authorities(
        candidate_asset,
        compatibility,
        semantic_asset,
        candidate_by_id,
    )

    try:
        from universal_scene_runtime import (
            validate_universal_scene_assets as runtime_validate_universal_assets,
        )

        runtime_assets = runtime_validate_universal_assets(
            candidate_asset,
            compatibility,
            semantic_bindings_asset=semantic_asset,
            candidate_path=candidate_path,
            compatibility_path=compatibility_path,
            semantic_bindings_path=semantic_path,
            research_manifest=_load_json(
                asset_dir / "research_evidence_universal_scene" / "manifest.json"
            ),
            research_manifest_path=(
                asset_dir / "research_evidence_universal_scene" / "manifest.json"
            ),
        )
    except Exception as exc:
        raise ValidationFailure(
            f"universal runtime rejected its assets: {exc}"
        ) from exc
    return {
        "status": "pass",
        "candidate_sha256": _sha256(candidate_path),
        "compatibility_sha256": _sha256(compatibility_path),
        "semantic_bindings_sha256": semantic_sha256,
        "candidate_count": len(candidates),
        "role_counts": dict(sorted(role_counts.items())),
        "pixel_evidence_count": len(pixel_ids),
        "prop_count": len(props),
        "embodiment_profile_count": len(embodiments),
        "proposal_profile_count": len(proposal_profiles),
        "context_distance_profile_count": len(context_profiles),
        "composition_literal_carrier_policy": composition_literal_carrier_policy,
        "literal_realization_policy": literal_realization_policy,
        "visual_owner_mapping_policy": visual_owner_mapping_policy,
        "fixed_prop_eligibility_policy": fixed_prop_eligibility_policy,
        "semantic_effect_policy": semantic_effect_policy,
        "trace_source_authorities": trace_source_authorities,
        "topic_count": len(contributions),
        "runtime_candidate_count": len(runtime_assets.candidate_by_id),
    }


def _runtime_texts(graph: Mapping[str, Any]) -> Iterable[tuple[str, str]]:
    for node in graph.get("runtime_nodes", []):
        if isinstance(node, dict):
            yield str(node.get("id") or ""), str(node.get("definition") or "")


def validate_holdouts(asset_dir: Path, assets: Any) -> dict[str, Any]:
    prompt_rows = _load_jsonl(asset_dir / "illustration_prompt_holdout_v1.jsonl")
    _require(len(prompt_rows) == 24, "prompt holdout must contain 24 rows")
    resolved: list[dict[str, str]] = []
    for row in prompt_rows:
        pack = build_candidate_pack(
            row["request_ko"],
            seed=row["seed"],
            creativity=0.85,
            contract_version=HISTORICAL_CONTRACT_VERSION_V2,
            assets=assets,
        )
        actual_topic = pack["request_contract"]["topic_id"]
        actual_format = pack["format_profile"]["variant_id"]
        _require(
            actual_topic == row["topic_id"],
            f"holdout {row['case_id']} route mismatch: {actual_topic}",
        )
        _require(
            actual_format == row["expected_format"],
            f"holdout {row['case_id']} format mismatch: {actual_format}",
        )
        nodes = pack["visual_grammar"]["runtime_nodes"]
        _require(
            sum(node["selected_role"] == "primary" for node in nodes) == 1,
            f"holdout {row['case_id']} primary mismatch",
        )
        _require(
            len(nodes) <= 3
            and all(node["node_type"] == "visual_atom" for node in nodes),
            f"holdout {row['case_id']} sparse visual mismatch",
        )
        repeated = build_candidate_pack(
            row["request_ko"],
            seed=row["seed"],
            creativity=0.85,
            contract_version=HISTORICAL_CONTRACT_VERSION_V2,
            assets=assets,
        )
        _require(pack == repeated, f"holdout {row['case_id']} is not deterministic")
        resolved.append(
            {
                "case_id": row["case_id"],
                "topic_id": actual_topic,
                "variant_id": actual_format,
                "pack_id": pack["pack_id"],
            }
        )

    render_rows = _load_jsonl(
        asset_dir / "render_illustration_quality_holdout_v1.jsonl"
    )
    _require(len(render_rows) == 6, "render holdout must contain six rows")
    render_topics = [topic for row in render_rows for topic in row.get("topic_ids", [])]
    _require(
        len(render_topics) == 24 and len(set(render_topics)) == 24,
        "render holdout must cover 24 topics exactly once",
    )
    return {
        "prompt_case_count": len(prompt_rows),
        "render_case_count": len(render_rows),
        "resolved": resolved,
    }


def _validate_prompt_qualification(
    asset_dir: Path,
    assets: Any,
    *,
    directory_name: str,
    manifest_schema: str,
    contract_version: str | None,
    require_current_implementation_hashes: bool,
) -> dict[str, Any]:
    qualification_dir = asset_dir / directory_name
    manifest = _load_json(qualification_dir / "manifest.json")
    _require(
        manifest.get("schema") == manifest_schema,
        f"{directory_name} manifest schema mismatch",
    )
    if directory_name == "prompt_qualification_v1":
        _require(
            manifest.get("runtime_sha256")
            == LEGACY_PROMPT_QUALIFICATION_RUNTIME_SHA256,
            "legacy prompt qualification runtime identity drift",
        )
        _require(
            manifest.get("audit_sha256") == LEGACY_PROMPT_QUALIFICATION_AUDIT_SHA256,
            "legacy prompt qualification audit identity drift",
        )
    elif directory_name == "prompt_qualification_v2":
        _require(
            manifest.get("runtime_sha256") == V2_PROMPT_QUALIFICATION_RUNTIME_SHA256,
            "v2 prompt qualification runtime identity drift",
        )
        _require(
            manifest.get("audit_sha256") == V2_PROMPT_QUALIFICATION_AUDIT_SHA256,
            "v2 prompt qualification audit identity drift",
        )
    elif require_current_implementation_hashes:
        _require(
            _sha256(Path(__file__).with_name("illustration_runtime.py"))
            == manifest.get("runtime_sha256"),
            f"{directory_name} runtime hash drift",
        )
        _require(
            _sha256(Path(__file__).with_name("illustration_audit.py"))
            == manifest.get("audit_sha256"),
            f"{directory_name} audit hash drift",
        )
    shards = manifest.get("shards")
    _require(
        isinstance(shards, list) and len(shards) == 6,
        "prompt qualification must list six shards",
    )
    records: list[dict[str, Any]] = []
    for entry in shards:
        _require(
            isinstance(entry, dict),
            "prompt qualification shard entry must be an object",
        )
        path = qualification_dir / str(entry.get("path") or "")
        _require(
            path.is_file() and path.parent == qualification_dir,
            "invalid prompt qualification shard path",
        )
        _require(
            _sha256(path) == entry.get("sha256"),
            f"prompt qualification shard hash mismatch: {path.name}",
        )
        rows = _load_jsonl(path)
        _require(
            len(rows) == entry.get("record_count") == 4,
            f"prompt qualification shard count mismatch: {path.name}",
        )
        records.extend(rows)

    holdout_rows = _load_jsonl(asset_dir / "illustration_prompt_holdout_v1.jsonl")
    holdout_by_case = {row["case_id"]: row for row in holdout_rows}
    _require(
        len(records) == manifest.get("case_count") == 24,
        "prompt qualification case count must be 24",
    )
    case_ids = [record.get("case_id") for record in records]
    _require(
        len(case_ids) == len(set(case_ids)) and set(case_ids) == set(holdout_by_case),
        "prompt qualification case coverage mismatch",
    )
    pack_ids: list[str] = []
    prompt_hashes: list[str] = []
    word_counts: list[int] = []
    for record in records:
        case = holdout_by_case[record["case_id"]]
        expected_pack = build_candidate_pack(
            case["request_ko"],
            seed=case["seed"],
            creativity=0.85,
            contract_version=contract_version or HISTORICAL_CONTRACT_VERSION_V2,
            assets=assets,
        )
        pack = record.get("candidate_pack")
        composed = record.get("composed")
        stored_audit = record.get("audit")
        _require(
            isinstance(pack, dict) and pack == expected_pack,
            f"prompt qualification pack drift: {record['case_id']}",
        )
        _require(
            isinstance(composed, dict),
            f"prompt qualification composed shape: {record['case_id']}",
        )
        actual_audit = audit_composed_prompt(pack, composed)
        _require(
            actual_audit == stored_audit,
            f"prompt qualification audit drift: {record['case_id']}",
        )
        _require(
            actual_audit.get("status") == "pass"
            and actual_audit.get("quality_status") == "pass"
            and not actual_audit.get("integrity_errors")
            and not actual_audit.get("failures")
            and not actual_audit.get("warnings"),
            f"prompt qualification is not clean: {record['case_id']}",
        )
        prompt = composed["prompt_en"]
        pack_ids.append(pack["pack_id"])
        prompt_hashes.append(hashlib.sha256(prompt.encode("utf-8")).hexdigest())
        word_counts.append(
            len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", prompt))
        )
    _require(
        len(pack_ids) == len(set(pack_ids)),
        "prompt qualification pack IDs must be unique",
    )
    _require(
        len(prompt_hashes) == len(set(prompt_hashes)),
        "prompt qualification prompts must be unique",
    )
    expected_words = manifest.get("word_count")
    _require(
        expected_words
        == {
            "minimum": min(word_counts),
            "maximum": max(word_counts),
            "mean": round(sum(word_counts) / len(word_counts), 1),
        },
        "prompt qualification word-count summary mismatch",
    )
    return {
        "schema": manifest_schema,
        "case_count": len(records),
        "unique_pack_count": len(set(pack_ids)),
        "minimum_words": min(word_counts),
        "maximum_words": max(word_counts),
        "mean_words": round(sum(word_counts) / len(word_counts), 1),
    }


def validate_legacy_prompt_qualification(
    asset_dir: Path, assets: Any
) -> dict[str, Any]:
    """Verify immutable v1 prompt evidence against the explicit legacy path."""

    return _validate_prompt_qualification(
        asset_dir,
        assets,
        directory_name="prompt_qualification_v1",
        manifest_schema="subculture-illustration-prompt-qualification/v1",
        contract_version=LEGACY_CONTRACT_VERSION,
        require_current_implementation_hashes=False,
    )


def validate_prompt_qualification(asset_dir: Path, assets: Any) -> dict[str, Any]:
    """Verify immutable v2 evidence against the explicit historical path."""

    return _validate_prompt_qualification(
        asset_dir,
        assets,
        directory_name="prompt_qualification_v2",
        manifest_schema="subculture-illustration-prompt-qualification/v2",
        contract_version=HISTORICAL_CONTRACT_VERSION_V2,
        require_current_implementation_hashes=False,
    )


def validate_render_v2_preflight(
    asset_dir: Path,
    assets: Any,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    """Verify the separately authorized case-01 successor before any image call."""

    preflight_dir = asset_dir / "render_case01_v2_preflight"
    pack_path = preflight_dir / "candidate_pack.json"
    composed_path = preflight_dir / "composed_prompt.json"
    audit_path = preflight_dir / "audit.json"
    preflight_path = preflight_dir / "preflight.json"
    for path in (pack_path, composed_path, audit_path, preflight_path):
        _require(path.is_file(), f"missing render-v2 preflight artifact: {path.name}")
    _require(
        not any(path.suffix.lower() == ".png" for path in preflight_dir.iterdir()),
        "render-v2 preflight directory must not contain generated images",
    )

    pack = _load_json(pack_path)
    composed = _load_json(composed_path)
    stored_audit = _load_json(audit_path)
    preflight = _load_json(preflight_path)
    case_id = "illustration_render_01_single_narrative"
    _require(
        preflight.get("schema") == "subculture-illustration-render-preflight/v2",
        "render-v2 preflight schema mismatch",
    )
    _require(preflight.get("case_id") == case_id, "render-v2 preflight case mismatch")
    _require(
        preflight.get("status") == "ready_for_separately_authorized_generation"
        and preflight.get("qualification_phase") == "pre_render_only",
        "render-v2 preflight status mismatch",
    )
    _require(
        preflight.get("image_generated") is False
        and preflight.get("image_edited") is False
        and preflight.get("image_tool_invoked") is False,
        "render-v2 preflight must remain generation-free",
    )
    _require(
        preflight.get("approval_required_before_generation") is True
        and preflight.get("authorization_recorded_for_generation") is False,
        "render-v2 preflight must await separate user authority",
    )

    holdout_rows = _load_jsonl(
        asset_dir / "render_illustration_quality_holdout_v1.jsonl"
    )
    frozen = next((row for row in holdout_rows if row.get("case_id") == case_id), None)
    _require(isinstance(frozen, dict), "render-v2 preflight lacks its frozen holdout")
    review = _load_json(asset_dir / "render_illustration_quality_visual_review_v1.json")
    historical_case = next(
        (case for case in review.get("cases", []) if case.get("case_id") == case_id),
        None,
    )
    _require(
        isinstance(historical_case, dict), "render-v2 preflight lacks its v1 review"
    )
    _require(
        historical_case.get("qualification_status") == "fail_repair_exhausted"
        and historical_case.get("attempt_count") == 2
        and historical_case.get("repair_count") == 1
        and historical_case.get("final_image") is None,
        "render-v2 preflight may only succeed the preserved exhausted v1 failure",
    )

    expected_pack = build_candidate_pack(
        frozen["request_ko"],
        topic=historical_case["route_id"],
        format_id=historical_case["format_profile"],
        seed=historical_case["seed"],
        creativity=0.85,
        contract_version=HISTORICAL_CONTRACT_VERSION_V2,
        assets=assets,
    )
    _require(pack == expected_pack, "render-v2 preflight candidate pack drift")
    candidate_meta = preflight.get("candidate_pack")
    _require(
        isinstance(candidate_meta, dict),
        "render-v2 preflight candidate metadata missing",
    )
    _require(
        candidate_meta.get("exact_source") == "candidate_pack.json",
        "render-v2 candidate source must be local",
    )
    _require(
        candidate_meta.get("sha256") == _sha256(pack_path),
        "render-v2 candidate hash mismatch",
    )
    _require(
        candidate_meta.get("pack_id") == pack.get("pack_id"),
        "render-v2 pack ID mismatch",
    )
    _require(
        candidate_meta.get("contract_version") == pack.get("contract_version")
        and candidate_meta.get("seed") == historical_case["seed"]
        and candidate_meta.get("route_id") == historical_case["route_id"]
        and candidate_meta.get("format_profile") == historical_case["format_profile"]
        and candidate_meta.get("creativity") == 0.85
        and candidate_meta.get("safety_mode") == "automatic",
        "render-v2 candidate metadata drift",
    )

    _require(
        composed.get("pack_id") == pack.get("pack_id"),
        "render-v2 composed pack binding mismatch",
    )
    actual_audit = audit_composed_prompt(pack, composed)
    _require(actual_audit == stored_audit, "render-v2 preflight audit drift")
    _require(
        actual_audit.get("status") == "pass"
        and actual_audit.get("quality_status") == "pass"
        and not actual_audit.get("integrity_errors")
        and not actual_audit.get("failures")
        and not actual_audit.get("warnings"),
        "render-v2 preflight prompt audit is not clean",
    )
    prompt = composed.get("prompt_en")
    _require(
        isinstance(prompt, str) and prompt and not prompt.endswith("\n"),
        "render-v2 prompt shape mismatch",
    )
    prompt_bytes = prompt.encode("utf-8")
    prompt_meta = preflight.get("prompt")
    _require(
        isinstance(prompt_meta, dict), "render-v2 preflight prompt metadata missing"
    )
    _require(
        prompt_meta.get("exact_source") == "composed_prompt.json#prompt_en"
        and prompt_meta.get("composed_source") == "composed_prompt.json",
        "render-v2 prompt source must be local",
    )
    _require(
        prompt_meta.get("composed_file_sha256") == _sha256(composed_path),
        "render-v2 composed hash mismatch",
    )
    _require(
        prompt_meta.get("utf8_sha256") == hashlib.sha256(prompt_bytes).hexdigest(),
        "render-v2 prompt hash mismatch",
    )
    _require(
        prompt_meta.get("utf8_with_single_trailing_lf_sha256")
        == hashlib.sha256(prompt_bytes + b"\n").hexdigest(),
        "render-v2 prompt trailing-LF hash mismatch",
    )
    _require(
        prompt_meta.get("utf8_byte_count") == len(prompt_bytes),
        "render-v2 prompt byte count mismatch",
    )
    _require(
        prompt_meta.get("mutation_allowed_before_generation") is False,
        "render-v2 prompt must be frozen",
    )
    _require(
        prompt_meta.get("negative_en")
        == composed.get("negative_en")
        == pack.get("negative_en"),
        "render-v2 negative prompt binding mismatch",
    )

    audit_meta = preflight.get("audit")
    _require(isinstance(audit_meta, dict), "render-v2 preflight audit metadata missing")
    _require(
        audit_meta.get("exact_source") == "audit.json",
        "render-v2 audit source must be local",
    )
    _require(
        audit_meta.get("sha256") == _sha256(audit_path), "render-v2 audit hash mismatch"
    )
    _require(
        audit_meta.get("status") == actual_audit["status"]
        and audit_meta.get("quality_status") == actual_audit["quality_status"]
        and audit_meta.get("failure_count") == len(actual_audit["failures"])
        and audit_meta.get("warning_count") == len(actual_audit["warnings"])
        and audit_meta.get("integrity_error_count")
        == len(actual_audit["integrity_errors"]),
        "render-v2 audit metadata drift",
    )

    plan = composed.get("second_look_plan")
    _require(
        plan == CASE01_V2_SECOND_LOOK_PLAN, "render-v2 second-look repair plan drift"
    )
    execution = preflight.get("second_look_execution")
    _require(
        isinstance(execution, dict), "render-v2 second-look execution metadata missing"
    )
    _require(
        execution.get("plan_source") == "composed_prompt.json#second_look_plan"
        and execution.get("plan_canonical_json_sha256")
        == hashlib.sha256(canonical_json_bytes(plan)).hexdigest()
        and execution.get("selected_proposal_id") == plan["selected_proposal_id"]
        and execution.get("review_scale_ids") == plan["review_scale_ids"],
        "render-v2 second-look execution binding mismatch",
    )
    initial = execution.get("future_initial_attempt")
    repair = execution.get("future_bounded_repair_if_needed")
    _require(
        isinstance(initial, dict)
        and initial.get("attempted_role") == "primary_carrier"
        and initial.get("maximum_attempts") == 1
        and initial.get("carrier_kind") == plan["primary_carrier"]["carrier_kind"],
        "render-v2 initial attempt contract mismatch",
    )
    _require(
        isinstance(repair, dict)
        and repair.get("attempted_role") == "fallback_carrier"
        and repair.get("maximum_attempts") == 1
        and repair.get("carrier_kind") == plan["fallback_carrier"]["carrier_kind"]
        and repair.get("requires_initial_pixel_failure") is True
        and repair.get("must_switch_from_primary_carrier") is True
        and repair.get("repeat_primary_carrier_forbidden") is True,
        "render-v2 fallback repair contract mismatch",
    )
    normalized_prompt = normalize_text(prompt)
    for legacy_fragment in (
        "clasped hand",
        "hand shadow",
        "thread shadow",
        "projected hand",
    ):
        _require(
            legacy_fragment not in normalized_prompt,
            f"render-v2 prompt retains legacy fragile carrier: {legacy_fragment}",
        )

    historical = preflight.get("historical_v1_artifacts")
    _require(isinstance(historical, dict), "render-v2 historical-v1 metadata missing")
    expected_directory = str(Path(historical_case["result_path"]).parent)
    _require(
        historical.get("immutable") is True
        and historical.get("modified_during_preflight") is False
        and historical.get("directory") == expected_directory
        and historical.get("qualification_status") == "final_fail_repair_exhausted",
        "render-v2 historical-v1 preservation metadata drift",
    )
    historical_hashes = historical.get("hashes")
    _require(
        isinstance(historical_hashes, dict), "render-v2 historical-v1 hashes missing"
    )
    _require(
        historical_hashes.get("result.json") == historical_case["result_sha256"]
        and historical_hashes.get("initial.png")
        == historical_case["initial_image"]["sha256"]
        and historical_hashes.get("edit_candidate.png")
        == historical_case["repair_image"]["sha256"],
        "render-v2 historical-v1 review hashes drift",
    )
    if verify_local_images:
        local_repo_root = Path(__file__).resolve().parents[3]
        historical_dir = local_repo_root / expected_directory
        for filename, digest in historical_hashes.items():
            historical_path = historical_dir / filename
            _require(
                historical_path.is_file(), f"missing historical v1 artifact: {filename}"
            )
            _require(
                _sha256(historical_path) == digest,
                f"historical v1 artifact hash mismatch: {filename}",
            )
        _require(
            not (historical_dir / "final.png").exists(),
            "failed historical v1 case must remain without final.png",
        )

    return {
        "status": "historical_preflight_valid",
        "recorded_status": "ready_awaiting_user_approval",
        "case_id": case_id,
        "pack_id": pack["pack_id"],
        "prompt_sha256": prompt_meta["utf8_sha256"],
        "second_look_plan_sha256": execution["plan_canonical_json_sha256"],
        "initial_attempted_role": initial["attempted_role"],
        "repair_attempted_role": repair["attempted_role"],
        "image_generated": False,
        "historical_local_artifacts_verified": verify_local_images,
    }


def validate_render_v3_preflight(
    asset_dir: Path,
    assets: Any,
) -> dict[str, Any]:
    """Verify the authorized structural successor without rewriting v1/v2 history."""

    preflight_dir = asset_dir / "render_case01_v3_preflight"
    pack_path = preflight_dir / "candidate_pack.json"
    composed_path = preflight_dir / "composed_prompt.json"
    audit_path = preflight_dir / "audit.json"
    preflight_path = preflight_dir / "preflight.json"
    for path in (pack_path, composed_path, audit_path, preflight_path):
        _require(path.is_file(), f"missing render-v3 preflight artifact: {path.name}")
    _require(
        not any(path.suffix.lower() == ".png" for path in preflight_dir.iterdir()),
        "render-v3 preflight directory must not contain generated images",
    )

    pack = _load_json(pack_path)
    composed = _load_json(composed_path)
    stored_audit = _load_json(audit_path)
    preflight = _load_json(preflight_path)
    case_id = "illustration_render_01_single_narrative"
    _require(
        preflight.get("schema") == "subculture-illustration-render-preflight/v3",
        "render-v3 preflight schema mismatch",
    )
    _require(preflight.get("case_id") == case_id, "render-v3 preflight case mismatch")
    _require(
        preflight.get("status") == "authorized_ready_for_generation"
        and preflight.get("qualification_phase") == "pre_render_only",
        "render-v3 preflight status mismatch",
    )
    _require(
        preflight.get("image_generated") is False
        and preflight.get("image_edited") is False
        and preflight.get("image_tool_invoked") is False,
        "render-v3 preflight itself must remain generation-free",
    )
    _require(
        preflight.get("approval_required_before_generation") is True
        and preflight.get("authorization_recorded_for_generation") is True,
        "render-v3 preflight must record the explicit successor authority",
    )
    authorization = preflight.get("authorization")
    _require(
        isinstance(authorization, dict), "render-v3 authorization metadata missing"
    )
    _require(
        authorization.get("initial_generation_maximum") == 1
        and authorization.get("fallback_edit_maximum") == 1
        and authorization.get("batch_selection_forbidden") is True
        and authorization.get("full_regression_only_after_pixel_pass") is True,
        "render-v3 authorization boundary mismatch",
    )

    holdout_rows = _load_jsonl(
        asset_dir / "render_illustration_quality_holdout_v1.jsonl"
    )
    frozen = next((row for row in holdout_rows if row.get("case_id") == case_id), None)
    _require(isinstance(frozen, dict), "render-v3 preflight lacks its frozen holdout")
    historical_review = _load_json(
        asset_dir / "render_illustration_quality_visual_review_v1.json"
    )
    historical_case = next(
        (
            case
            for case in historical_review.get("cases", [])
            if case.get("case_id") == case_id
        ),
        None,
    )
    _require(
        isinstance(historical_case, dict), "render-v3 preflight lacks its v1 review"
    )
    v2_review = _load_json(asset_dir / "render_case01_v2_visual_review.json")
    _require(
        v2_review.get("qualification_status") == "fail_repair_exhausted"
        and v2_review.get("attempt_count") == 2
        and v2_review.get("repair_count") == 1
        and v2_review.get("final_image") is None,
        "render-v3 preflight must preserve the exhausted v2 failure",
    )

    expected_pack = build_candidate_pack(
        frozen["request_ko"],
        topic=historical_case["route_id"],
        format_id=historical_case["format_profile"],
        seed=historical_case["seed"],
        creativity=0.85,
        contract_version=HISTORICAL_CONTRACT_VERSION_V2,
        assets=assets,
    )
    _require(pack == expected_pack, "render-v3 preflight candidate pack drift")
    candidate_meta = preflight.get("candidate_pack")
    _require(isinstance(candidate_meta, dict), "render-v3 candidate metadata missing")
    _require(
        candidate_meta.get("exact_source") == "candidate_pack.json"
        and candidate_meta.get("sha256") == _sha256(pack_path)
        and candidate_meta.get("pack_id") == pack.get("pack_id")
        and candidate_meta.get("contract_version") == pack.get("contract_version")
        and candidate_meta.get("seed") == historical_case["seed"]
        and candidate_meta.get("route_id") == historical_case["route_id"]
        and candidate_meta.get("format_profile") == historical_case["format_profile"]
        and candidate_meta.get("creativity") == 0.85
        and candidate_meta.get("safety_mode") == "automatic",
        "render-v3 candidate metadata drift",
    )

    _require(
        composed.get("pack_id") == pack.get("pack_id"),
        "render-v3 composed pack binding mismatch",
    )
    actual_audit = audit_composed_prompt(pack, composed)
    _require(actual_audit == stored_audit, "render-v3 preflight audit drift")
    _require(
        actual_audit.get("status") == "pass"
        and actual_audit.get("quality_status") == "pass"
        and not actual_audit.get("integrity_errors")
        and not actual_audit.get("failures")
        and not actual_audit.get("warnings"),
        "render-v3 preflight prompt audit is not clean",
    )
    prompt = composed.get("prompt_en")
    _require(
        isinstance(prompt, str) and prompt and not prompt.endswith("\n"),
        "render-v3 prompt shape mismatch",
    )
    prompt_bytes = prompt.encode("utf-8")
    prompt_meta = preflight.get("prompt")
    _require(isinstance(prompt_meta, dict), "render-v3 prompt metadata missing")
    _require(
        prompt_meta.get("exact_source") == "composed_prompt.json#prompt_en"
        and prompt_meta.get("composed_source") == "composed_prompt.json"
        and prompt_meta.get("composed_file_sha256") == _sha256(composed_path)
        and prompt_meta.get("utf8_sha256") == hashlib.sha256(prompt_bytes).hexdigest()
        and prompt_meta.get("utf8_with_single_trailing_lf_sha256")
        == hashlib.sha256(prompt_bytes + b"\n").hexdigest()
        and prompt_meta.get("utf8_byte_count") == len(prompt_bytes)
        and prompt_meta.get("mutation_allowed_before_initial_generation") is False,
        "render-v3 prompt hash/freeze metadata drift",
    )
    _require(
        prompt_meta.get("negative_en")
        == composed.get("negative_en")
        == pack.get("negative_en"),
        "render-v3 negative prompt binding mismatch",
    )
    audit_meta = preflight.get("audit")
    _require(isinstance(audit_meta, dict), "render-v3 audit metadata missing")
    _require(
        audit_meta.get("exact_source") == "audit.json"
        and audit_meta.get("sha256") == _sha256(audit_path)
        and audit_meta.get("status") == actual_audit["status"]
        and audit_meta.get("quality_status") == actual_audit["quality_status"]
        and audit_meta.get("failure_count") == len(actual_audit["failures"])
        and audit_meta.get("warning_count") == len(actual_audit["warnings"])
        and audit_meta.get("integrity_error_count")
        == len(actual_audit["integrity_errors"]),
        "render-v3 audit metadata drift",
    )

    plan = composed.get("second_look_plan")
    _require(plan == CASE01_V3_SECOND_LOOK_PLAN, "render-v3 second-look plan drift")
    execution = preflight.get("second_look_execution")
    _require(
        isinstance(execution, dict), "render-v3 second-look execution metadata missing"
    )
    _require(
        execution.get("plan_source") == "composed_prompt.json#second_look_plan"
        and execution.get("plan_canonical_json_sha256")
        == hashlib.sha256(canonical_json_bytes(plan)).hexdigest()
        and execution.get("selected_proposal_id") == plan["selected_proposal_id"]
        and execution.get("review_scale_ids") == plan["review_scale_ids"],
        "render-v3 second-look execution binding mismatch",
    )
    initial = execution.get("future_initial_attempt")
    repair = execution.get("future_bounded_repair_if_needed")
    _require(
        isinstance(initial, dict)
        and initial.get("attempted_role") == "primary_carrier"
        and initial.get("maximum_attempts") == 1
        and initial.get("carrier_kind") == "object_relation",
        "render-v3 initial attempt contract mismatch",
    )
    _require(
        isinstance(repair, dict)
        and repair.get("attempted_role") == "fallback_carrier"
        and repair.get("maximum_attempts") == 1
        and repair.get("carrier_kind") == "surface_state"
        and repair.get("requires_initial_pixel_failure") is True
        and repair.get("must_switch_from_primary_carrier") is True
        and repair.get("repeat_primary_carrier_forbidden") is True,
        "render-v3 fallback repair contract mismatch",
    )
    normalized_prompt = normalize_text(prompt)
    for legacy_fragment in (
        "broad pale seam",
        "clear brass threshold strip",
        "unoccupied receiving mat",
        "broad dry coat-length boundary on the unoccupied receiving mat",
    ):
        _require(
            legacy_fragment not in normalized_prompt,
            f"render-v3 prompt retains failed v2 carrier: {legacy_fragment}",
        )
    for required_fragment in (
        "rigid ceiling chain",
        "bell body tilts",
        "clapper displaces",
        "no hand touches the bell",
        "no rug, mat, border, weave, tile, inlay",
        "continuous grain",
    ):
        _require(
            required_fragment in normalized_prompt,
            f"render-v3 prompt lacks structural carrier evidence: {required_fragment}",
        )

    historical = preflight.get("historical_artifacts")
    _require(
        isinstance(historical, list) and len(historical) == 2,
        "render-v3 historical metadata mismatch",
    )
    _require(
        [item.get("generation") for item in historical if isinstance(item, dict)]
        == ["v1", "v2"]
        and all(
            item.get("immutable") is True
            for item in historical
            if isinstance(item, dict)
        )
        and all(
            item.get("qualification_status") == "final_fail_repair_exhausted"
            for item in historical
            if isinstance(item, dict)
        ),
        "render-v3 must preserve both earlier exhausted outcomes",
    )

    return {
        "status": "authorized_preflight_valid",
        "recorded_status": "authorized_ready_for_generation",
        "case_id": case_id,
        "pack_id": pack["pack_id"],
        "prompt_sha256": prompt_meta["utf8_sha256"],
        "second_look_plan_sha256": execution["plan_canonical_json_sha256"],
        "initial_attempted_role": initial["attempted_role"],
        "repair_attempted_role": repair["attempted_role"],
        "image_generated_in_preflight": False,
    }


def _review_focus_map(value: Any, label: str) -> dict[str, str]:
    _require(isinstance(value, list) and value, f"{label} must be a nonempty list")
    result: dict[str, str] = {}
    for item in value:
        _require(isinstance(item, dict), f"{label} entries must be objects")
        focus = item.get("focus")
        outcome = item.get("outcome")
        _require(isinstance(focus, str) and focus, f"{label} focus must be nonempty")
        _require(
            isinstance(outcome, str) and outcome, f"{label} outcome must be nonempty"
        )
        _require(focus not in result, f"{label} contains duplicate focus {focus}")
        result[focus] = outcome
    return result


def _png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    _require(
        len(header) == 24
        and header[:8] == b"\x89PNG\r\n\x1a\n"
        and header[12:16] == b"IHDR",
        f"{path} is not a canonical PNG",
    )
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def validate_render_v2_qualification(
    asset_dir: Path,
    assets: Any,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    """Verify the bounded v2 successor without promoting either failed role."""

    review_path = asset_dir / "render_case01_v2_visual_review.json"
    review = _load_json(review_path)
    _require(
        review.get("schema_version")
        == "subculture-illustration-render-successor-review/v2",
        "render-v2 successor review schema mismatch",
    )
    case_id = "illustration_render_01_single_narrative"
    _require(review.get("case_id") == case_id, "render-v2 successor case mismatch")
    _require(
        review.get("relationship_to_v1")
        == "continues_the_preserved_v1_failure_with_a_distinct_v2_contract",
        "render-v2 successor must not relabel the v1 failure",
    )

    holdout_rows = _load_jsonl(
        asset_dir / "render_illustration_quality_holdout_v1.jsonl"
    )
    frozen = next((row for row in holdout_rows if row.get("case_id") == case_id), None)
    _require(isinstance(frozen, dict), "render-v2 successor lacks its frozen holdout")
    historical_review = _load_json(
        asset_dir / "render_illustration_quality_visual_review_v1.json"
    )
    historical_case = next(
        (
            case
            for case in historical_review.get("cases", [])
            if case.get("case_id") == case_id
        ),
        None,
    )
    _require(isinstance(historical_case, dict), "render-v2 successor lacks its v1 case")

    preflight_dir = asset_dir / "render_case01_v2_preflight"
    preflight_pack = _load_json(preflight_dir / "candidate_pack.json")
    preflight_composed = _load_json(preflight_dir / "composed_prompt.json")
    expected_pack = build_candidate_pack(
        frozen["request_ko"],
        topic=historical_case["route_id"],
        format_id=historical_case["format_profile"],
        seed=historical_case["seed"],
        creativity=0.85,
        contract_version=HISTORICAL_CONTRACT_VERSION_V2,
        assets=assets,
    )
    _require(preflight_pack == expected_pack, "render-v2 successor pack drift")
    preflight = review.get("preflight")
    _require(
        isinstance(preflight, dict), "render-v2 successor preflight metadata missing"
    )
    _require(
        preflight.get("directory") == "render_case01_v2_preflight"
        and preflight.get("pack_id") == preflight_pack["pack_id"]
        and preflight.get("prompt_sha256")
        == hashlib.sha256(preflight_composed["prompt_en"].encode("utf-8")).hexdigest()
        and preflight.get("second_look_plan_sha256")
        == hashlib.sha256(
            canonical_json_bytes(preflight_composed["second_look_plan"])
        ).hexdigest(),
        "render-v2 successor preflight binding mismatch",
    )

    _require(
        review.get("qualification_status") == "fail_repair_exhausted"
        and review.get("attempt_count") == 2
        and review.get("repair_count") == 1
        and review.get("final_image") is None,
        "render-v2 successor must preserve the exhausted failure",
    )
    initial = review.get("initial_image")
    repair = review.get("repair_image")
    _require(
        isinstance(initial, dict)
        and initial.get("attempted_role") == "primary_carrier"
        and initial.get("pixel_status") == "fail",
        "render-v2 primary attempt record mismatch",
    )
    _require(
        isinstance(repair, dict)
        and repair.get("attempted_role") == "fallback_carrier"
        and repair.get("pixel_status") == "fail",
        "render-v2 fallback attempt record mismatch",
    )

    focus = _review_focus_map(
        review.get("review_focus_results"), "render-v2.review_focus_results"
    )
    _require(
        set(frozen["required_pixel_focus"]) <= set(focus)
        and all(focus[item] == "pass" for item in frozen["required_pixel_focus"]),
        "render-v2 successor lost a frozen primary focus",
    )
    _require(
        focus.get("second_look_primary_carrier") == "fail"
        and focus.get("second_look_fallback_carrier") == "fail",
        "render-v2 successor must not promote a failed second-look carrier",
    )
    thumbnail = _review_focus_map(
        review.get("thumbnail_results"), "render-v2.thumbnail_results"
    )
    _require(
        set(thumbnail) == set(frozen["thumbnail_checks"])
        and set(thumbnail.values()) == {"pass"},
        "render-v2 successor thumbnail review mismatch",
    )
    forbidden = _review_focus_map(
        review.get("forbidden_convergence_results"),
        "render-v2.forbidden_convergence_results",
    )
    _require(
        set(forbidden) == set(frozen["forbidden_pixel_convergence"])
        and set(forbidden.values()) == {"absent"},
        "render-v2 successor forbidden-convergence mismatch",
    )

    second_look = review.get("second_look_pixel_review")
    _require(isinstance(second_look, dict), "render-v2 second-look review missing")
    expected_plan_sha = hashlib.sha256(
        canonical_json_bytes(preflight_composed["second_look_plan"])
    ).hexdigest()
    _require(
        second_look.get("plan_sha256") == expected_plan_sha
        and second_look.get("declared_review_scale_ids") == ["native"]
        and second_look.get("qualified_role") is None
        and second_look.get("qualification_status") == "fail_repair_exhausted",
        "render-v2 second-look summary mismatch",
    )
    attempts = second_look.get("attempts")
    _require(
        isinstance(attempts, list) and len(attempts) == 2,
        "render-v2 second-look attempts mismatch",
    )
    _require(
        [attempt.get("attempted_role") for attempt in attempts]
        == ["primary_carrier", "fallback_carrier"],
        "render-v2 second-look role order mismatch",
    )
    for attempt in attempts:
        scale_results = attempt.get("scale_results")
        _require(
            isinstance(scale_results, list)
            and len(scale_results) == 1
            and scale_results[0].get("scale_id") == "native"
            and scale_results[0].get("status") == "fail"
            and isinstance(scale_results[0].get("evidence"), str)
            and scale_results[0]["evidence"],
            "render-v2 second-look scale result mismatch",
        )

    aggregate = review.get("aggregate_with_preserved_v1_passes")
    _require(isinstance(aggregate, dict), "render-v2 aggregate missing")
    _require(
        aggregate
        == {
            "case_count": 6,
            "passed_case_count": 5,
            "failed_case_count": 1,
            "failure_case_ids": [case_id],
            "outcome": "partial",
        },
        "render-v2 aggregate must remain five pass and one fail",
    )
    suite = review.get("post_render_full_suite")
    _require(
        isinstance(suite, dict)
        and suite.get("authorized") is True
        and suite.get("condition") == "pixel_qualification_passes"
        and suite.get("condition_met") is False
        and suite.get("executed") is False,
        "render-v2 conditional full-suite record mismatch",
    )

    if verify_local_images:
        local_repo_root = Path(__file__).resolve().parents[3]
        result_rel = review.get("result_path")
        _require(
            isinstance(result_rel, str) and result_rel, "render-v2 result path missing"
        )
        result_path = local_repo_root / result_rel
        _require(result_path.is_file(), "render-v2 local result is missing")
        _require(
            _sha256(result_path) == review.get("result_sha256"),
            "render-v2 result hash mismatch",
        )
        result = _load_json(result_path)
        _require(
            result.get("schema") == "subculture-illustration-render-result/v2"
            and result.get("qualification_status") == "final_fail_repair_exhausted_v2"
            and result.get("attempt_count") == 2
            and result.get("repair_attempt_count") == 1
            and result.get("final_image") is None,
            "render-v2 local result status mismatch",
        )
        result_dir = result_path.parent
        local_pack = _load_json(result_dir / "candidate_pack.json")
        local_composed = _load_json(result_dir / "composed_prompt.json")
        local_audit = _load_json(result_dir / "audit.json")
        _require(local_pack == expected_pack, "render-v2 local pack drift")
        _require(
            local_composed == preflight_composed,
            "render-v2 local composed prompt drift",
        )
        _require(
            audit_composed_prompt(local_pack, local_composed) == local_audit,
            "render-v2 local audit drift",
        )
        _require(
            local_audit.get("status") == "pass"
            and local_audit.get("quality_status") == "pass"
            and not local_audit.get("integrity_errors")
            and not local_audit.get("failures")
            and not local_audit.get("warnings"),
            "render-v2 local audit is not clean",
        )
        _require(
            result.get("second_look_pixel_review") == second_look,
            "render-v2 result/review second-look mismatch",
        )
        _require(
            result.get("post_render_full_suite", {}).get("executed") is False,
            "render-v2 result must not claim the conditional suite ran",
        )
        for record in (initial, repair):
            image_path = local_repo_root / record["path"]
            _require(
                image_path.is_file(), f"render-v2 local image missing: {record['path']}"
            )
            _require(
                _sha256(image_path) == record["sha256"],
                f"render-v2 local image hash mismatch: {record['path']}",
            )
            expected_dimensions = tuple(
                int(value) for value in record["dimensions"].split("x", 1)
            )
            _require(
                _png_dimensions(image_path) == expected_dimensions,
                f"render-v2 local image dimensions mismatch: {record['path']}",
            )
        for view in result.get("review_views", []):
            _require(isinstance(view, dict), "render-v2 review view must be an object")
            view_path = result_dir / str(view.get("path") or "")
            _require(
                view_path.is_file(), f"render-v2 review view missing: {view_path.name}"
            )
            _require(
                _sha256(view_path) == view.get("sha256"),
                f"render-v2 review view hash mismatch: {view_path.name}",
            )
            _require(
                _png_dimensions(view_path) == (view.get("width"), view.get("height")),
                f"render-v2 review view dimensions mismatch: {view_path.name}",
            )
        for attempt_key in ("initial_attempt", "fallback_attempt"):
            attempt = result.get(attempt_key)
            _require(isinstance(attempt, dict), f"render-v2 {attempt_key} missing")
            native_path = Path(str(attempt.get("native_tool_path") or ""))
            _require(
                native_path.is_file(), f"render-v2 native source missing: {attempt_key}"
            )
            _require(
                _sha256(native_path) == attempt.get("sha256"),
                f"render-v2 native source hash mismatch: {attempt_key}",
            )
            blind_path = result_dir / str(attempt.get("blind_observations_path") or "")
            _require(
                blind_path.is_file(),
                f"render-v2 blind observations missing: {attempt_key}",
            )
            _require(
                _sha256(blind_path) == attempt.get("blind_observations_sha256"),
                f"render-v2 blind observation hash mismatch: {attempt_key}",
            )
        _require(
            not (result_dir / "final.png").exists(),
            "failed render-v2 case must not expose final.png",
        )

    return {
        "qualification_status": "partial",
        "case_id": case_id,
        "attempt_count": 2,
        "repair_count": 1,
        "qualified_role": None,
        "passed_case_count": 5,
        "failed_case_count": 1,
        "full_suite_executed": False,
        "local_artifacts_verified": verify_local_images,
    }


def validate_render_v3_qualification(
    asset_dir: Path,
    assets: Any,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    """Verify the one-attempt v3 pass while retaining both prior failures."""

    review_path = asset_dir / "render_case01_v3_visual_review.json"
    review = _load_json(review_path)
    _require(
        review.get("schema_version")
        == "subculture-illustration-render-successor-review/v3",
        "render-v3 successor review schema mismatch",
    )
    case_id = "illustration_render_01_single_narrative"
    _require(review.get("case_id") == case_id, "render-v3 successor case mismatch")
    _require(
        review.get("relationship_to_history")
        == "continues_preserved_v1_and_v2_failures_with_a_structurally_distinct_v3_plan",
        "render-v3 successor must preserve rather than relabel historical failures",
    )
    v2_review = _load_json(asset_dir / "render_case01_v2_visual_review.json")
    _require(
        v2_review.get("qualification_status") == "fail_repair_exhausted"
        and v2_review.get("attempt_count") == 2
        and v2_review.get("repair_count") == 1
        and v2_review.get("final_image") is None,
        "render-v3 successor cannot rewrite the v2 exhausted failure",
    )

    holdout_rows = _load_jsonl(
        asset_dir / "render_illustration_quality_holdout_v1.jsonl"
    )
    frozen = next((row for row in holdout_rows if row.get("case_id") == case_id), None)
    _require(isinstance(frozen, dict), "render-v3 successor lacks its frozen holdout")
    historical_review = _load_json(
        asset_dir / "render_illustration_quality_visual_review_v1.json"
    )
    historical_case = next(
        (
            case
            for case in historical_review.get("cases", [])
            if case.get("case_id") == case_id
        ),
        None,
    )
    _require(isinstance(historical_case, dict), "render-v3 successor lacks its v1 case")

    preflight_dir = asset_dir / "render_case01_v3_preflight"
    preflight_pack = _load_json(preflight_dir / "candidate_pack.json")
    preflight_composed = _load_json(preflight_dir / "composed_prompt.json")
    expected_pack = build_candidate_pack(
        frozen["request_ko"],
        topic=historical_case["route_id"],
        format_id=historical_case["format_profile"],
        seed=historical_case["seed"],
        creativity=0.85,
        contract_version=HISTORICAL_CONTRACT_VERSION_V2,
        assets=assets,
    )
    _require(preflight_pack == expected_pack, "render-v3 successor pack drift")
    preflight = review.get("preflight")
    _require(
        isinstance(preflight, dict), "render-v3 successor preflight metadata missing"
    )
    _require(
        preflight.get("directory") == "render_case01_v3_preflight"
        and preflight.get("pack_id") == preflight_pack["pack_id"]
        and preflight.get("prompt_sha256")
        == hashlib.sha256(preflight_composed["prompt_en"].encode("utf-8")).hexdigest()
        and preflight.get("second_look_plan_sha256")
        == hashlib.sha256(
            canonical_json_bytes(preflight_composed["second_look_plan"])
        ).hexdigest(),
        "render-v3 successor preflight binding mismatch",
    )

    _require(
        review.get("qualification_status") == "pass"
        and review.get("attempt_count") == 1
        and review.get("repair_count") == 0
        and review.get("repair_image") is None,
        "render-v3 successor must record one pristine primary pass and no repair",
    )
    initial = review.get("initial_image")
    final = review.get("final_image")
    _require(
        isinstance(initial, dict)
        and initial.get("attempted_role") == "primary_carrier"
        and initial.get("pixel_status") == "pass",
        "render-v3 primary attempt record mismatch",
    )
    _require(
        isinstance(final, dict)
        and final.get("byte_identical_to_initial") is True
        and final.get("sha256") == initial.get("sha256")
        and final.get("dimensions") == initial.get("dimensions"),
        "render-v3 final must be the byte-identical passing primary image",
    )

    focus = _review_focus_map(
        review.get("review_focus_results"), "render-v3.review_focus_results"
    )
    _require(
        set(frozen["required_pixel_focus"]) <= set(focus)
        and all(focus[item] == "pass" for item in frozen["required_pixel_focus"]),
        "render-v3 successor lost a frozen primary focus",
    )
    _require(
        focus.get("second_look_primary_carrier") == "pass"
        and focus.get("second_look_fallback_carrier") == "not_attempted",
        "render-v3 successor role qualification mismatch",
    )
    thumbnail = _review_focus_map(
        review.get("thumbnail_results"), "render-v3.thumbnail_results"
    )
    _require(
        set(thumbnail) == set(frozen["thumbnail_checks"])
        and set(thumbnail.values()) == {"pass"},
        "render-v3 successor thumbnail review mismatch",
    )
    forbidden = _review_focus_map(
        review.get("forbidden_convergence_results"),
        "render-v3.forbidden_convergence_results",
    )
    _require(
        set(forbidden) == set(frozen["forbidden_pixel_convergence"])
        and set(forbidden.values()) == {"absent"},
        "render-v3 successor forbidden-convergence mismatch",
    )

    second_look = review.get("second_look_pixel_review")
    _require(isinstance(second_look, dict), "render-v3 second-look review missing")
    expected_plan_sha = hashlib.sha256(
        canonical_json_bytes(preflight_composed["second_look_plan"])
    ).hexdigest()
    _require(
        second_look.get("plan_sha256") == expected_plan_sha
        and second_look.get("declared_review_scale_ids")
        == ["native", "thumbnail_320px"]
        and second_look.get("qualified_role") == "primary_carrier"
        and second_look.get("qualification_status") == "pass",
        "render-v3 second-look summary mismatch",
    )
    attempts = second_look.get("attempts")
    _require(
        isinstance(attempts, list)
        and len(attempts) == 1
        and attempts[0].get("attempted_role") == "primary_carrier",
        "render-v3 second-look attempt order mismatch",
    )
    scale_results = attempts[0].get("scale_results")
    _require(
        isinstance(scale_results, list)
        and [item.get("scale_id") for item in scale_results]
        == ["native", "thumbnail_320px"]
        and all(item.get("status") == "pass" for item in scale_results)
        and all(
            isinstance(item.get("evidence"), str) and item["evidence"]
            for item in scale_results
        ),
        "render-v3 second-look scale evidence mismatch",
    )

    aggregate = review.get("aggregate_with_preserved_v1_v2_evidence")
    _require(
        aggregate
        == {
            "case_count": 6,
            "passed_case_count": 6,
            "failed_case_count": 0,
            "failure_case_ids": [],
            "outcome": "pass",
        },
        "render-v3 aggregate must qualify all six cases",
    )
    suite = review.get("post_render_full_suite")
    _require(isinstance(suite, dict), "render-v3 full-suite record missing")
    _require(
        suite.get("authorized") is True
        and suite.get("condition") == "pixel_qualification_passes"
        and suite.get("condition_met") is True,
        "render-v3 conditional full-suite boundary mismatch",
    )
    suite_executed = suite.get("executed")
    _require(
        isinstance(suite_executed, bool),
        "render-v3 full-suite execution flag must be boolean",
    )
    if suite_executed:
        _require(
            suite.get("status") == "pass"
            and isinstance(suite.get("command"), str)
            and suite["command"]
            and isinstance(suite.get("test_count"), int)
            and suite["test_count"] > 0
            and suite.get("failure_count") == 0
            and suite.get("error_count") == 0,
            "render-v3 completed full-suite evidence mismatch",
        )
    else:
        _require(
            suite.get("status") == "pending",
            "render-v3 pending full-suite status mismatch",
        )

    if verify_local_images:
        local_repo_root = Path(__file__).resolve().parents[3]
        result_rel = review.get("result_path")
        _require(
            isinstance(result_rel, str) and result_rel, "render-v3 result path missing"
        )
        result_path = local_repo_root / result_rel
        _require(result_path.is_file(), "render-v3 local result is missing")
        _require(
            _sha256(result_path) == review.get("result_sha256"),
            "render-v3 result hash mismatch",
        )
        result = _load_json(result_path)
        _require(
            result.get("schema") == "subculture-illustration-render-result/v3"
            and result.get("qualification_status") == "pass_primary_carrier"
            and result.get("product_outcome") == "pass"
            and result.get("attempt_count") == 1
            and result.get("repair_attempt_count") == 0
            and result.get("fallback_attempt") is None,
            "render-v3 local result status mismatch",
        )
        result_dir = result_path.parent
        local_pack = _load_json(result_dir / "candidate_pack.json")
        local_composed = _load_json(result_dir / "composed_prompt.json")
        local_audit = _load_json(result_dir / "audit.json")
        local_preflight = _load_json(result_dir / "preflight.json")
        _require(local_pack == expected_pack, "render-v3 local pack drift")
        _require(
            local_composed == preflight_composed,
            "render-v3 local composed prompt drift",
        )
        _require(
            local_preflight == _load_json(preflight_dir / "preflight.json"),
            "render-v3 local preflight drift",
        )
        _require(
            audit_composed_prompt(local_pack, local_composed) == local_audit,
            "render-v3 local audit drift",
        )
        _require(
            result.get("second_look_pixel_review") == second_look,
            "render-v3 result/review second-look mismatch",
        )
        _require(
            result.get("post_render_full_suite") == suite,
            "render-v3 result/review full-suite record mismatch",
        )
        for record in (initial, final):
            image_path = local_repo_root / record["path"]
            _require(
                image_path.is_file(), f"render-v3 local image missing: {record['path']}"
            )
            _require(
                _sha256(image_path) == record["sha256"],
                f"render-v3 local image hash mismatch: {record['path']}",
            )
            expected_dimensions = tuple(
                int(value) for value in record["dimensions"].split("x", 1)
            )
            _require(
                _png_dimensions(image_path) == expected_dimensions,
                f"render-v3 local image dimensions mismatch: {record['path']}",
            )
        _require(
            (local_repo_root / initial["path"]).read_bytes()
            == (local_repo_root / final["path"]).read_bytes(),
            "render-v3 final differs from the passing primary image",
        )
        for view in result.get("review_views", []):
            _require(isinstance(view, dict), "render-v3 review view must be an object")
            view_path = result_dir / str(view.get("path") or "")
            _require(
                view_path.is_file(), f"render-v3 review view missing: {view_path.name}"
            )
            _require(
                _sha256(view_path) == view.get("sha256"),
                f"render-v3 review view hash mismatch: {view_path.name}",
            )
            _require(
                _png_dimensions(view_path) == (view.get("width"), view.get("height")),
                f"render-v3 review view dimensions mismatch: {view_path.name}",
            )
        attempt = result.get("initial_attempt")
        _require(isinstance(attempt, dict), "render-v3 initial attempt missing")
        native_path = Path(str(attempt.get("native_tool_path") or ""))
        _require(native_path.is_file(), "render-v3 native source missing")
        _require(
            _sha256(native_path) == attempt.get("sha256"),
            "render-v3 native source hash mismatch",
        )
        blind_path = result_dir / str(attempt.get("blind_observations_path") or "")
        _require(blind_path.is_file(), "render-v3 blind observations missing")
        _require(
            _sha256(blind_path) == attempt.get("blind_observations_sha256"),
            "render-v3 blind observation hash mismatch",
        )
        _require(
            not (result_dir / "edit_candidate.png").exists(),
            "passing render-v3 primary must not have a fallback edit",
        )

    return {
        "qualification_status": "pass",
        "case_id": case_id,
        "attempt_count": 1,
        "repair_count": 0,
        "qualified_role": "primary_carrier",
        "passed_case_count": 6,
        "failed_case_count": 0,
        "full_suite_executed": suite_executed,
        "local_artifacts_verified": verify_local_images,
    }


def validate_render_qualification(
    asset_dir: Path,
    assets: Any,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    review_path = asset_dir / "render_illustration_quality_visual_review_v1.json"
    review = _load_json(review_path)
    _require(
        review.get("schema_version") == "subculture-illustration-visual-review/v1",
        "render visual-review schema mismatch",
    )
    holdout_rows = _load_jsonl(
        asset_dir / "render_illustration_quality_holdout_v1.jsonl"
    )
    holdout_by_id = {row["case_id"]: row for row in holdout_rows}
    cases = review.get("cases")
    _require(
        isinstance(cases, list) and len(cases) == 6,
        "render visual review must contain six cases",
    )
    case_ids = [case.get("case_id") for case in cases if isinstance(case, dict)]
    _require(
        len(case_ids) == 6 and len(set(case_ids)) == 6,
        "render visual-review case IDs must be unique",
    )
    _require(
        set(case_ids) == set(holdout_by_id),
        "render visual-review holdout coverage mismatch",
    )

    passed = 0
    failed = 0
    local_repo_root = Path(__file__).resolve().parents[3]
    for case in cases:
        _require(isinstance(case, dict), "render visual-review case must be an object")
        case_id = case["case_id"]
        frozen = holdout_by_id[case_id]
        route_id = case.get("route_id")
        format_profile = case.get("format_profile")
        _require(
            route_id in frozen["topic_ids"],
            f"{case_id} primary route is outside frozen topic coverage",
        )
        _require(
            format_profile == frozen["format_profile"], f"{case_id} format mismatch"
        )
        seed = case.get("seed")
        _require(
            isinstance(seed, int) and not isinstance(seed, bool),
            f"{case_id} seed must be an integer",
        )
        expected_pack = build_candidate_pack(
            frozen["request_ko"],
            topic=route_id,
            format_id=format_profile,
            seed=seed,
            creativity=0.85,
            contract_version=LEGACY_CONTRACT_VERSION,
            assets=assets,
        )
        _require(
            expected_pack["pack_id"] == case.get("pack_id"), f"{case_id} pack ID drift"
        )

        required_focus = _review_focus_map(
            case.get("review_focus_results"), f"{case_id}.review_focus_results"
        )
        _require(
            set(frozen["required_pixel_focus"]) <= set(required_focus),
            f"{case_id} omits frozen required pixel focus",
        )
        _require(
            all(
                required_focus[item] == "pass"
                for item in frozen["required_pixel_focus"]
            ),
            f"{case_id} frozen required pixel focus is not fully passing",
        )
        thumbnail = _review_focus_map(
            case.get("thumbnail_results"), f"{case_id}.thumbnail_results"
        )
        _require(
            set(thumbnail) == set(frozen["thumbnail_checks"]),
            f"{case_id} thumbnail coverage mismatch",
        )
        _require(
            set(thumbnail.values()) == {"pass"},
            f"{case_id} thumbnail review is not passing",
        )
        forbidden = _review_focus_map(
            case.get("forbidden_convergence_results"),
            f"{case_id}.forbidden_convergence_results",
        )
        _require(
            set(forbidden) == set(frozen["forbidden_pixel_convergence"]),
            f"{case_id} forbidden-convergence coverage mismatch",
        )
        _require(
            set(forbidden.values()) == {"absent"},
            f"{case_id} has forbidden pixel convergence",
        )

        attempts = case.get("attempt_count")
        repairs = case.get("repair_count")
        _require(
            attempts in {1, 2} and repairs in {0, 1},
            f"{case_id} attempt budget shape mismatch",
        )
        _require(
            attempts == repairs + 1, f"{case_id} attempt and repair counts disagree"
        )
        _require(
            attempts <= frozen["initial_generation_limit"] + frozen["repair_limit"],
            f"{case_id} exceeded image budget",
        )
        status = case.get("qualification_status")
        is_pass = status in {"pass", "pass_after_single_bounded_edit"}
        failing_focus = [
            focus for focus, outcome in required_focus.items() if outcome == "fail"
        ]
        final_image = case.get("final_image")
        if is_pass:
            passed += 1
            _require(
                isinstance(final_image, dict),
                f"{case_id} passing case lacks final image",
            )
            _require(
                not failing_focus,
                f"{case_id} passing case contains failed review focus",
            )
        else:
            failed += 1
            _require(
                status == "fail_repair_exhausted",
                f"{case_id} has unknown qualification status",
            )
            _require(
                final_image is None,
                f"{case_id} failed case must not expose final image",
            )
            _require(
                repairs == frozen["repair_limit"] == 1,
                f"{case_id} failed before exhausting bounded repair",
            )
            _require(
                failing_focus,
                f"{case_id} failed case has no explicit failed review focus",
            )

        if verify_local_images:
            result_rel = case.get("result_path")
            _require(
                isinstance(result_rel, str) and result_rel,
                f"{case_id} result path missing",
            )
            result_file = local_repo_root / result_rel
            _require(result_file.is_file(), f"{case_id} local result is missing")
            _require(
                _sha256(result_file) == case.get("result_sha256"),
                f"{case_id} result hash mismatch",
            )
            case_dir = result_file.parent
            local_pack = _load_json(case_dir / "candidate_pack.json")
            composed = _load_json(case_dir / "composed_prompt.json")
            stored_audit = _load_json(case_dir / "audit.json")
            _require(
                local_pack == expected_pack, f"{case_id} local candidate pack drift"
            )
            _require(
                audit_composed_prompt(local_pack, composed) == stored_audit,
                f"{case_id} local prompt audit drift",
            )
            _require(
                stored_audit.get("status") == "pass"
                and stored_audit.get("quality_status") == "pass"
                and not stored_audit.get("integrity_errors")
                and not stored_audit.get("failures")
                and not stored_audit.get("warnings"),
                f"{case_id} local prompt audit is not clean",
            )
            image_records = [
                value
                for key, value in case.items()
                if key.endswith("_image") and isinstance(value, dict)
            ]
            for image_record in image_records:
                rel = image_record.get("path")
                _require(
                    isinstance(rel, str) and rel, f"{case_id} local image path missing"
                )
                image_file = local_repo_root / rel
                _require(
                    image_file.is_file(), f"{case_id} local image is missing: {rel}"
                )
                _require(
                    _sha256(image_file) == image_record.get("sha256"),
                    f"{case_id} local image hash mismatch: {rel}",
                )
                dimensions = image_record.get("dimensions")
                _require(
                    isinstance(dimensions, str) and "x" in dimensions,
                    f"{case_id} image dimensions missing",
                )
                expected_dimensions = tuple(
                    int(value) for value in dimensions.split("x", 1)
                )
                _require(
                    _png_dimensions(image_file) == expected_dimensions,
                    f"{case_id} image dimensions mismatch: {rel}",
                )

    cross_case = review.get("cross_case_review")
    _require(isinstance(cross_case, dict), "render cross-case review must be an object")
    _require(
        cross_case.get("case_count") == len(cases), "render cross-case count mismatch"
    )
    _require(
        cross_case.get("passed_case_count") == passed,
        "render passing-case count mismatch",
    )
    _require(
        cross_case.get("failed_case_count") == failed,
        "render failed-case count mismatch",
    )
    expected_outcome = "pass" if failed == 0 else "partial"
    _require(
        cross_case.get("outcome") == expected_outcome,
        "render cross-case outcome mismatch",
    )
    _require(
        set(cross_case.get("failure_case_ids", []))
        == {
            case["case_id"]
            for case in cases
            if case["qualification_status"] == "fail_repair_exhausted"
        },
        "render cross-case failure IDs mismatch",
    )
    return {
        "qualification_status": expected_outcome,
        "case_count": len(cases),
        "passed_case_count": passed,
        "failed_case_count": failed,
        "local_artifacts_verified": verify_local_images,
    }


def validate_all(
    asset_dir: str | Path | None = None,
    *,
    verify_local_images: bool = False,
) -> dict[str, Any]:
    root = Path(asset_dir).expanduser().resolve() if asset_dir else default_asset_dir()
    research = validate_research(root)
    universal_research = validate_universal_scene_research(root)
    universal_holdouts = validate_universal_scene_holdouts(root, universal_research)
    universal_runtime = validate_universal_scene_runtime_assets(
        root,
        universal_research,
        universal_holdouts,
    )
    photo_regression = validate_photo_regression_baseline(root)
    assets = load_runtime_assets(root)
    runtime = validate_assets(root)
    _require(
        set(assets.nodes_by_id) == research["candidate_ids"],
        "runtime node IDs must exactly equal research candidate IDs",
    )
    route_alias_owner: dict[str, str] = {}
    for route_id, route in assets.routes_by_id.items():
        for phrases in route["aliases"].values():
            for phrase in phrases:
                normalized = normalize_text(phrase)
                owner = route_alias_owner.setdefault(normalized, route_id)
                _require(
                    owner == route_id,
                    f"normalized route alias collision: {phrase!r} -> {owner}, {route_id}",
                )
    format_alias_owner: dict[str, str] = {}
    for variant_id, variant in assets.variants_by_id.items():
        for phrases in variant["aliases"].values():
            for phrase in phrases:
                normalized = normalize_text(phrase)
                owner = format_alias_owner.setdefault(normalized, variant_id)
                _require(
                    owner == variant_id,
                    f"normalized format alias collision: {phrase!r} -> {owner}, {variant_id}",
                )
    for topic_id, route in assets.routes_by_id.items():
        _require(
            route["matrix_id"] == research["matrix_ids"][topic_id],
            f"route {topic_id} matrix provenance mismatch",
        )
    for node_id, node in assets.nodes_by_id.items():
        definition, role, topic_id = research["candidate_specs"][node_id]
        _require(
            node["definition"] == definition, f"runtime definition drift: {node_id}"
        )
        _require(
            node["role"] == role and node["topic_id"] == topic_id,
            f"runtime role/topic drift: {node_id}",
        )
        provenance = node["provenance"]
        _require(
            provenance["matrix_id"] == research["matrix_ids"][topic_id],
            f"runtime matrix ref drift: {node_id}",
        )
        _require(
            set(provenance["evidence_record_ids"])
            <= research["topic_record_ids"][topic_id],
            f"runtime cross-topic evidence ref: {node_id}",
        )
    for node_id, text in _runtime_texts(assets.graph):
        for pattern in RUNTIME_NAME_GUARDS:
            _require(
                not pattern.search(text),
                f"runtime definition contains protected/named-style text: {node_id}",
            )
    holdouts = validate_holdouts(root, assets)
    legacy_prompt_qualification = validate_legacy_prompt_qualification(root, assets)
    prompt_qualification = validate_prompt_qualification(root, assets)
    render_v2_preflight = validate_render_v2_preflight(
        root,
        assets,
        verify_local_images=verify_local_images,
    )
    render_v3_preflight = validate_render_v3_preflight(root, assets)
    render_qualification = validate_render_qualification(
        root,
        assets,
        verify_local_images=verify_local_images,
    )
    render_v2_qualification = validate_render_v2_qualification(
        root,
        assets,
        verify_local_images=verify_local_images,
    )
    render_v3_qualification = validate_render_v3_qualification(
        root,
        assets,
        verify_local_images=verify_local_images,
    )
    generation_retry_policy = validate_generation_retry_policy(root)
    research.pop("candidate_ids")
    research.pop("candidate_specs")
    research.pop("matrix_ids")
    research.pop("topic_record_ids")
    for private_key in (
        "candidate_specs",
        "record_ids",
        "topic_ids",
        "topic_record_ids",
    ):
        universal_research.pop(private_key)
    universal_holdouts.pop("prompt_rows")
    universal_holdouts.pop("scene_contracts_by_case")
    return {
        "status": "pass",
        "product_qualification_status": render_v3_qualification["qualification_status"],
        "research": research,
        "universal_research": universal_research,
        "universal_holdouts": universal_holdouts,
        "universal_runtime": universal_runtime,
        "photo_regression": photo_regression,
        "runtime": runtime,
        "generation_retry_policy": generation_retry_policy,
        "holdouts": holdouts,
        "legacy_prompt_qualification": legacy_prompt_qualification,
        "prompt_qualification": prompt_qualification,
        "render_v2_preflight": render_v2_preflight,
        "render_v3_preflight": render_v3_preflight,
        "render_qualification": render_qualification,
        "render_v2_qualification": render_v2_qualification,
        "render_v3_qualification": render_v3_qualification,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the illustration research, runtime assets, and frozen holdouts."
    )
    parser.add_argument(
        "--asset-dir", help="override the sibling skill asset directory"
    )
    parser.add_argument(
        "--verify-local-images",
        action="store_true",
        help="also verify ignored local render/result files, PNG dimensions, hashes, packs, and audits",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = validate_all(
            args.asset_dir, verify_local_images=args.verify_local_images
        )
    except (
        IllustrationRuntimeError,
        ValidationFailure,
        OSError,
        UnicodeError,
        json.JSONDecodeError,
    ) as exc:
        result = {"status": "fail", "error": str(exc)}
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
