#!/usr/bin/env python3
"""Validate live illustration assets and their authenticated meaning contracts."""
from __future__ import annotations
import argparse
import copy
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence
from illustration_runtime import IllustrationRuntimeError, canonical_json_bytes, default_asset_dir, load_runtime_assets, normalize_text, validate_assets
RESEARCH_ROLE_VALUES = {'topic_matrix', 'independent_source'}
PROVENANCE_VALUES = {'source_supported', 'cross_source_synthesis', 'design_inference'}
CANDIDATE_ROLE_VALUES = {'visual_atom', 'router', 'guard'}
UNIVERSAL_RESEARCH_ROLE_VALUES = {'topic_matrix', 'independent_source'}
UNIVERSAL_CANDIDATE_ROLE_VALUES = {'visual_atom', 'router', 'guard', 'metric'}
UNIVERSAL_RESEARCH_SCHEMA = 'universal-scene-research/v1'
UNIVERSAL_RESEARCH_MANIFEST_SCHEMA = 'subculture_illustration_universal_scene_research_manifest/v1'
UNIVERSAL_EVENT_ROLE_IDS = ['actor', 'action', 'target', 'instrument', 'recipient', 'result', 'location', 'phase']
UNIVERSAL_CONTRACT_EFFECT_SUBJECT_BY_ID = {'active_weapon_discharge': 'actor', 'combat_opponent_assignment': 'recipient', 'combat_target_assignment': 'target', 'navigation_instrument_use': 'actor', 'romantic_contact': 'actor', 'scene_promise_hijack': 'scene', 'human_face_attachment': 'source_entity', 'human_hand_attachment': 'source_entity', 'human_limb_attachment': 'source_entity'}
UNIVERSAL_CONTRACT_EFFECT_TARGETS_BY_ID = {'active_weapon_discharge': [('request', 'concept'), ('slot', 'action'), ('event_role', 'action'), ('context', 'violence')], 'combat_opponent_assignment': [('request', 'concept'), ('slot', 'relation'), ('event_role', 'recipient'), ('event_role', 'target')], 'combat_target_assignment': [('request', 'concept'), ('slot', 'action'), ('slot', 'relation'), ('event_role', 'target')], 'navigation_instrument_use': [('request', 'concept'), ('slot', 'action'), ('slot', 'prop'), ('event_role', 'action'), ('event_role', 'instrument')], 'romantic_contact': [('request', 'concept'), ('slot', 'action'), ('slot', 'relation'), ('event_role', 'action'), ('event_role', 'recipient')], 'scene_promise_hijack': [('request', 'concept'), ('identity_fact', 'feature_fact'), ('identity_fact', 'scene_fact'), ('slot', 'relation'), ('event_role', 'result')], 'human_face_attachment': [('request', 'concept'), ('identity_fact', 'feature_fact'), ('identity_fact', 'scene_fact'), ('slot', 'expression')], 'human_hand_attachment': [('request', 'concept'), ('identity_fact', 'feature_fact'), ('identity_fact', 'scene_fact'), ('slot', 'pose'), ('slot', 'action')], 'human_limb_attachment': [('request', 'concept'), ('identity_fact', 'feature_fact'), ('identity_fact', 'scene_fact'), ('slot', 'pose')]}
UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS = ['affordance', 'motivation', 'identity_contrast', 'mechanics', 'ownership', 'state_change', 'consequence']
UNIVERSAL_DECISION_REASON_CODE_IDS = ['all_guard_predicates_passed', 'capability_unsatisfied', 'cardinality_feasible', 'cardinality_limit', 'closed_facet', 'closed_prop_slot', 'closed_role_conflict', 'event_spine_cardinality', 'fixed_facet_conflict', 'fixed_role_conflict', 'forbidden_predicate_satisfied', 'guard_not_applicable', 'guard_predicate_failed', 'identity_overwrite', 'policy_active_violence', 'policy_explicit_only', 'policy_not_applicable', 'policy_pass', 'policy_platform_blocked', 'precondition_unsatisfied', 'proposal_path_not_open', 'remote_budget_exceeded', 'requires_all_unsatisfied', 'resource_capacity', 'resource_feasible', 'rule_satisfied', 'slot_state_ineligible', 'trigger_unsatisfied', 'visible_bridge_required']
UNIVERSAL_RULE_REASON_CODES = {'rule_fixed_identity_precedence': 'identity_overwrite', 'rule_closed_prop': 'closed_prop_slot', 'rule_exactly_one_event': 'event_spine_cardinality', 'rule_resource_capacity': 'resource_capacity', 'rule_visible_middle_far_bridge': 'visible_bridge_required', 'rule_remote_budget': 'remote_budget_exceeded', 'rule_policy_independent_of_creativity': 'policy_platform_blocked'}
UNIVERSAL_V2_DERIVED_CANDIDATE_IDS = {'uao_global_prop_wooden_mallet', 'uao_safe_inactive_hazard_orientation', 'usc_contact_locomotor_surface_path', 'usc_contact_release_transition', 'usc_relation_actor_effect_recipient_chain', 'ush_functional_configuration_state', 'ush_layered_state_history', 'ush_material_identity_boundary'}
UNIVERSAL_V2_RESOURCE_KINDS = ['manipulator', 'attention_channel', 'head_orientation', 'facial_display', 'support_contact', 'mouth', 'appendage', 'wing_appendage', 'locomotor_contact', 'body_orientation', 'body_contour_display', 'surface_signal', 'light_emission', 'internal_luminance_display', 'mobile_ear_pair', 'wing_axis_pair', 'tail_axis', 'mechanical_state_displacement', 'external_anchor', 'focal_primary', 'focal_secondary', 'foreground_salience', 'event_peak', 'prop_slot']
UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS = ['active_weapon_discharge', 'combat_opponent_assignment', 'combat_target_assignment', 'navigation_instrument_use', 'romantic_contact', 'scene_promise_hijack', 'human_face_attachment', 'human_hand_attachment', 'human_limb_attachment']
UNIVERSAL_V2_LITERAL_REALIZATION_PROFILE_SPECS = [('lvr_safe_inactive_hazard_orientation', 'action', 'inactive_hazard_orientation', 'pose', ['uao_safe_inactive_hazard_orientation'], 'request_text', [(['firearm', 'gun', 'machine gun', 'weapon', '기관총', '무기', '총기'], 'affirmative'), (['carry sling', 'safety cover', 'secure', 'secured', '안전 덮개', '운반 끈'], 'affirmative'), (['discharge', 'fire', 'firing', 'shoot', '발사'], 'negated')], ['orientation', 'support'], ['support_contact'], 10), ('lvr_directed_attention_target', 'action', 'directed_attention', 'attention', ['gha_visible_target_line'], 'slot_phrases', [(['examine', 'inspect', 'look at', 'scrutinize', '바라보', '바라보다', '살피다', '살피며', '점검'], 'affirmative')], ['orientation'], ['attention_channel'], 20), ('lvr_ambiguous_restrained_display', 'expression', 'mixed_display', 'perceived_affect', ['dpa_mixed_display_cue_cluster'], 'slot_phrases', [(['ambiguous', 'either reading', '두 감정', '양가', '처럼도'], 'affirmative'), (['restrained', 'suppressed', '억제', '절제'], 'affirmative')], ['display'], [], 30), ('lvr_shared_attention_convergence', 'relation', 'shared_attention', 'attention', ['gha_joint_attention_convergence'], 'slot_phrases', [(['jointly inspect', 'look together', 'same target', 'shared attention', '같은 목표', '공유 주의', '동시에 바라보', '함께 조사'], 'affirmative')], ['orientation'], ['attention_channel'], 40), ('lvr_distributed_load_support', 'pose', 'visible_support_map', 'pose', ['ubp_support_contact_map'], 'slot_phrases', [(['heavy', 'load', 'weight', '무거운', '무게', '하중'], 'affirmative'), (['brace', 'distribute', 'support', '받치', '분산', '지지'], 'affirmative')], ['support'], ['support_contact'], 50), ('lvr_hazard_consequence', 'environment', 'material_leak_trace', 'consequence', ['usc_ecs_material_residue_atom'], 'slot_phrases', [(['hazard', 'leak', 'spill', '누출', '새는', '위험'], 'affirmative')], ['residue'], [], 60), ('lvr_protective_recipient_path', 'relation', 'directed_recipient_effect', 'relation', ['usc_relation_actor_effect_recipient_chain'], 'slot_phrases', [(['clear a path', 'protect', 'shield', '길을 만드', '길을 만들', '보호', '지키'], 'affirmative')], ['orientation', 'support'], ['focal_secondary'], 70), ('lvr_environment_consequence', 'action', 'environment_response', 'consequence', ['usc_ecs_environment_affordance_atom'], 'slot_phrases', [(['clear a path', 'displace', 'shield', 'windbreak', '길을 만들', '바람막이', '보호'], 'affirmative')], ['residue'], [], 80), ('lvr_release_recovery_phase', 'action', 'release_recovery_phase', 'phase', ['action_temporal_phases_release_recovery'], 'slot_phrases', [(['after placing', 'just after', 'release after', '내려놓은', '직후'], 'affirmative')], ['contact'], [], 90), ('lvr_insert_resistance_contact_commitment', 'action', 'contact_commitment_phase', 'phase', ['action_temporal_phases_contact_commitment'], 'slot_phrases', [(['insert', 'inserting', 'put in', '넣고', '삽입'], 'affirmative'), (['resistance', 'resistive', '저항'], 'affirmative')], ['path'], [], 95), ('lvr_release_contact_transition', 'action', 'release_recovery_phase', 'contact', ['usc_contact_release_transition'], 'request_text', [(['contact', 'junction', '접촉'], 'affirmative'), (['relax', 'release', 'separate', '분리', '풀리'], 'affirmative')], ['contact', 'state_boundary'], [], 100), ('lvr_shared_target_convergence', 'relation', 'shared_target_relation', 'relation', ['usc_relation_shared_target_convergence'], 'slot_phrases', [(['same object', 'same target', 'shared target', '같은 대상', '같은 목표', '공동 목표', '공유 주의'], 'affirmative')], ['orientation'], ['focal_secondary'], 110), ('lvr_wooden_mallet_prop', 'prop', 'typed_prop_identity', 'prop', ['uao_global_prop_wooden_mallet'], 'slot_phrases', [(['mallet', '木槌', '木锤', '나무망치', '말렛'], 'affirmative'), (['wood', 'wooden', '木製', '木质', '나무', '목제'], 'affirmative')], ['state_boundary'], ['prop_slot'], 120), ('lvr_visible_material_identity', 'prop', 'material_identity_boundary', 'prop_state', ['ush_material_identity_boundary'], 'slot_phrases', [(['fabric', 'glass', 'leather', 'metal', 'wood', '가죽', '금속', '나무', '목제', '유리', '천'], 'affirmative')], ['state_boundary'], [], 130), ('lvr_broken_closed_configuration', 'prop', 'functional_configuration_state', 'prop_state', ['ush_functional_configuration_state'], 'slot_phrases', [(['broken', 'damaged', '고장', '부러진', '파손'], 'affirmative'), (['open', 'unfold', '열', '펴', '펼'], 'negated')], ['state_boundary'], [], 140), ('lvr_layered_state_history', 'prop', 'layered_state_history', 'prop_state', ['ush_layered_state_history'], 'request_text', [(['abrasion', 'scuff', 'wear', 'worn', '닳', '마모'], 'affirmative'), (['patch', 'repair', 'stitch', '수선', '패치'], 'affirmative'), (['lubricant', 'oil', 'residue', '기름', '윤활유', '잔류'], 'affirmative')], ['residue', 'state_boundary'], [], 150), ('lvr_quiet_everyday_context', 'environment', 'context_anchor_relation', 'environment', ['usc_sptg_context_anchor_relation'], 'request_text', [(['calm', 'gentle', 'quiet', '잔잔', '조용'], 'affirmative'), (['daily', 'everyday', 'routine', '일상', '평범'], 'affirmative')], ['path'], [], 160), ('lvr_work_routine_action', 'action', 'action_observable_relation', 'action', ['event_role_frames_action_predicate'], 'slot_phrases', [(['arrange', 'organize', 'record', 'sort', '기록', '정리'], 'affirmative'), (['ledger', 'order book', 'register', '장부', '주문서'], 'affirmative')], ['path'], [], 170), ('lvr_locomotor_surface_contact', 'action', 'locomotor_surface_path', 'contact', ['usc_contact_locomotor_surface_path'], 'slot_phrases', [(['body traversal', 'pass through', 'traverse', 'walk through', '몸으로', '지나가', '통과'], 'affirmative'), (['ground', 'path', 'surface', '갈대밭', '길', '지면'], 'affirmative')], ['contact', 'support'], ['locomotor_contact'], 180)]
UNIVERSAL_DISTANCE_AXIS_IDS = ['theme', 'era_technology', 'tone', 'violence', 'social', 'scale', 'salience_displacement']
UNIVERSAL_LOAD_AXIS_IDS = ['physical', 'occupancy', 'affective_valence', 'affective_arousal', 'violence', 'visual_salience', 'scene_importance', 'theme_displacement']
UNIVERSAL_EFFECT_SOURCE_KIND_IDS = ['visual_candidate', 'proposal_profile', 'context_profile', 'bridge_type', 'resource_kind']
UNIVERSAL_RESEARCH_EXPECTED_TOTALS = {'record_count': 60, 'topic_count': 20, 'independent_source_count': 40, 'mechanism_count': 167, 'candidate_count': 220, 'pixel_evidence_count': 97, 'unique_source_url_count': 40, 'candidate_role_counts': {'visual_atom': 97, 'router': 38, 'guard': 52, 'metric': 33}, 'mechanism_provenance_counts': {'source_supported': 47, 'cross_source_synthesis': 10, 'design_inference': 110}}
GENERATION_RETRY_POLICY_SCHEMA = 'subculture-illustration-generation-retry-policy/v1'
GENERATION_RETRY_PHASES = ['primary_generation', 'fallback_repair_generation']
GENERATION_RETRY_OUTCOMES = {'tool_error', 'transport_error', 'server_error', 'rate_limit', 'timeout', 'empty_result', 'inaccessible_result', 'safety_refusal', 'policy_refusal', 'other_refusal'}
GENERATION_RETRY_PRESERVED_FIELDS = {'prompt_en', 'negative_en', 'pack_id', 'chosen_candidate_ids', 'seed', 'generation_parameters'}
RUNTIME_NAME_GUARDS = (re.compile('\\bin (?:the )?style of\\b', re.IGNORECASE), re.compile('\\bby (?:artist|illustrator|mangaka|studio)\\b', re.IGNORECASE), re.compile('\\b(?:Pok[eé]mon|Pikachu|Naruto|One Piece|Gundam|Evangelion|Genshin Impact|Honkai|Disney|Marvel|Sanrio)\\b', re.IGNORECASE))

class ValidationFailure(ValueError):
    """Raised when a versioned asset violates the frozen contract."""

def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)

def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))

def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        _require(isinstance(value, dict), f'{path.name}:{line_number} must be an object')
        rows.append(value)
    return rows

def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _strings(value: Any, label: str, *, minimum: int=0) -> list[str]:
    _require(isinstance(value, list), f'{label} must be a list')
    _require(all((isinstance(item, str) and item.strip() for item in value)), f'{label} must contain strings')
    _require(len(value) >= minimum, f'{label} must contain at least {minimum} values')
    return list(value)

def validate_generation_retry_policy(asset_dir: Path) -> dict[str, Any]:
    policy = _load_json(asset_dir / 'image_generation_retry_policy_v1.json')
    _require(isinstance(policy, dict), 'generation retry policy must be an object')
    _require(policy.get('schema') == GENERATION_RETRY_POLICY_SCHEMA, 'generation retry policy schema mismatch')
    _require(policy.get('retry_budget_scope') == 'per_generation_phase', 'generation retry budget must be per phase')
    _require(policy.get('phases') == GENERATION_RETRY_PHASES, 'generation retry phases mismatch')
    _require(policy.get('initial_calls_per_phase') == 1, 'generation phase must start with one call')
    _require(policy.get('max_unchanged_retries_after_initial') == 3, 'generation phase must allow exactly three unchanged retries')
    _require(policy.get('max_calls_per_phase') == 4, 'generation phase must allow four total calls')
    outcomes = _strings(policy.get('retryable_no_image_outcomes'), 'generation retry outcomes', minimum=1)
    _require(set(outcomes) == GENERATION_RETRY_OUTCOMES, 'generation retry outcomes mismatch')
    preserved = _strings(policy.get('preserve_exact_fields'), 'generation retry preserved fields', minimum=1)
    _require(set(preserved) == GENERATION_RETRY_PRESERVED_FIELDS, 'generation retry preserved fields mismatch')
    for field in ('stop_on_first_concrete_image', 'retry_does_not_consume_pixel_repair_slot', 'no_prompt_rewrite_between_retries', 'no_policy_evasion', 'higher_priority_platform_stop_applies'):
        _require(policy.get(field) is True, f'generation retry policy requires {field}=true')
    _require(policy.get('exhausted_status') == 'generation_failed_retries_exhausted', 'generation retry exhausted status mismatch')
    return {'schema': policy['schema'], 'max_unchanged_retries_after_initial': policy['max_unchanged_retries_after_initial'], 'max_calls_per_phase': policy['max_calls_per_phase'], 'includes_safety_refusal': 'safety_refusal' in outcomes, 'includes_policy_refusal': 'policy_refusal' in outcomes, 'status': 'pass'}

def validate_research(asset_dir: Path) -> dict[str, Any]:
    evidence_dir = asset_dir / 'research_evidence_illustration'
    manifest = _load_json(evidence_dir / 'manifest.json')
    _require(manifest.get('schema') == 'subculture_illustration_research_manifest_v1', 'research manifest schema mismatch')
    shards = manifest.get('shards')
    _require(isinstance(shards, list) and len(shards) == 6, 'research manifest must list six shards')
    rows: list[dict[str, Any]] = []
    shard_results: list[dict[str, Any]] = []
    for entry in shards:
        _require(isinstance(entry, dict), 'research shard entry must be an object')
        rel = entry.get('path')
        _require(isinstance(rel, str) and rel and (Path(rel).name == rel), 'research shard path must be one local filename')
        path = evidence_dir / rel
        _require(path.is_file(), f'missing research shard {rel}')
        digest = _sha256(path)
        _require(digest == entry.get('sha256'), f'research shard hash mismatch: {rel}')
        shard_rows = _load_jsonl(path)
        _require(len(shard_rows) == entry.get('record_count'), f'research shard row count mismatch: {rel}')
        rows.extend(shard_rows)
        shard_results.append({'path': rel, 'record_count': len(shard_rows), 'sha256': digest})
    _require(len(rows) == manifest.get('record_count') == 72, 'research record count must be 72')
    record_ids = [row.get('id') for row in rows]
    _require(all((isinstance(item, str) and item for item in record_ids)), 'research record id must be nonempty')
    _require(len(record_ids) == len(set(record_ids)), 'research record ids must be globally unique')
    live_record_ids = set(record_ids)
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        topic_id = row.get('topic_id')
        _require(isinstance(topic_id, str) and topic_id, 'research topic_id must be nonempty')
        _require(row.get('record_role') in RESEARCH_ROLE_VALUES, f'{topic_id} has invalid record_role')
        _require(row.get('status') == 'approved', f'{topic_id} research row is not approved')
        by_topic[topic_id].append(row)
    _require(len(by_topic) == manifest.get('topic_count') == 24, 'research topic count must be 24')
    all_candidate_ids: list[str] = []
    candidate_specs: dict[str, tuple[str, str, str]] = {}
    provenance_counts: Counter[str] = Counter()
    matrix_ids: dict[str, str] = {}
    for topic_id, topic_rows in by_topic.items():
        matrices = [row for row in topic_rows if row['record_role'] == 'topic_matrix']
        sources = [row for row in topic_rows if row['record_role'] == 'independent_source']
        _require(len(topic_rows) == 3 and len(matrices) == 1 and (len(sources) == 2), f'{topic_id} must have one matrix and two sources')
        _require(len({row.get('source_url') for row in topic_rows}) == 3, f'{topic_id} must have three distinct URLs')
        matrix = matrices[0]
        matrix_ids[topic_id] = matrix['id']
        source_ids = {row['id'] for row in sources}
        _require(set(matrix.get('synthesis_evidence_ids', [])) == source_ids, f'{topic_id} synthesis IDs mismatch')
        mechanisms = matrix.get('mechanisms')
        provenance = matrix.get('mechanism_provenance')
        _require(isinstance(mechanisms, list) and 6 <= len(mechanisms) <= 10, f'{topic_id} mechanism count/shape mismatch')
        _require(isinstance(provenance, list) and len(provenance) == len(mechanisms), f'{topic_id} provenance count mismatch')
        _require(all((isinstance(item, dict) and set(item) == {'id', 'statement'} for item in mechanisms)), f'{topic_id} mechanism shape mismatch')
        _require(all((isinstance(item, dict) and set(item) == {'mechanism_id', 'provenance', 'evidence_ids'} for item in provenance)), f'{topic_id} provenance shape mismatch')
        mechanism_ids = [item['id'] for item in mechanisms]
        _require(mechanism_ids == [item['mechanism_id'] for item in provenance], f'{topic_id} mechanism/provenance order mismatch')
        _require(len(mechanism_ids) == len(set(mechanism_ids)), f'{topic_id} duplicate mechanism IDs')
        for item in provenance:
            kind = item['provenance']
            provenance_counts[kind] += 1
            _require(kind in PROVENANCE_VALUES, f'{topic_id} invalid provenance kind {kind}')
            refs = _strings(item['evidence_ids'], f'{topic_id}.{item['mechanism_id']}.evidence_ids', minimum=1)
            _require(set(refs) <= live_record_ids, f'{topic_id} provenance has unknown record')
            if kind == 'cross_source_synthesis':
                _require(source_ids <= set(refs), f'{topic_id} cross-source mechanism lacks both sources')
        candidate_ids = _strings(matrix.get('candidate_ids'), f'{topic_id}.candidate_ids', minimum=1)
        definitions = matrix.get('candidate_definitions')
        roles = matrix.get('candidate_roles')
        _require(isinstance(definitions, dict) and set(definitions) == set(candidate_ids), f'{topic_id} candidate definitions mismatch')
        _require(isinstance(roles, dict) and set(roles) == set(candidate_ids), f'{topic_id} candidate roles mismatch')
        _require(set(roles.values()) <= CANDIDATE_ROLE_VALUES, f'{topic_id} invalid candidate role')
        evidence_ids = _strings(matrix.get('illustration_evidence'), f'{topic_id}.illustration_evidence', minimum=1)
        evidence_definitions = matrix.get('illustration_evidence_definitions')
        _require(isinstance(evidence_definitions, dict) and set(evidence_definitions) == set(evidence_ids), f'{topic_id} illustration evidence definitions mismatch')
        _require(set(evidence_ids) <= set(candidate_ids), f'{topic_id} illustration evidence is not a candidate subset')
        _require(all((roles[item] == 'visual_atom' for item in evidence_ids)), f'{topic_id} illustration evidence must be visual')
        for field in ('compatibility', 'conflicts', 'counterexamples', 'boundaries', 'format_implications', 'viewer_implications'):
            _strings(matrix.get(field), f'{topic_id}.{field}', minimum=4)
        all_candidate_ids.extend(candidate_ids)
        for candidate_id in candidate_ids:
            candidate_specs[candidate_id] = (definitions[candidate_id], roles[candidate_id], topic_id)
    _require(len(all_candidate_ids) == manifest.get('candidate_count') == 264, 'research candidate count must be 264')
    _require(len(all_candidate_ids) == len(set(all_candidate_ids)), 'research candidate IDs must be globally unique')
    expected_provenance = manifest.get('provenance_counts')
    _require(dict(provenance_counts) == expected_provenance, 'research provenance counts do not match manifest')
    _require(sum(provenance_counts.values()) == manifest.get('mechanism_count') == 192, 'research mechanism count must be 192')
    return {'record_count': len(rows), 'topic_count': len(by_topic), 'mechanism_count': sum(provenance_counts.values()), 'candidate_count': len(all_candidate_ids), 'candidate_ids': set(all_candidate_ids), 'candidate_specs': candidate_specs, 'matrix_ids': matrix_ids, 'topic_record_ids': {topic_id: {row['id'] for row in topic_rows} for topic_id, topic_rows in by_topic.items()}, 'provenance_counts': dict(sorted(provenance_counts.items())), 'shards': shard_results}

def validate_universal_scene_research(asset_dir: Path) -> dict[str, Any]:
    """Validate the independently audited 20-topic universal-scene corpus."""
    evidence_dir = asset_dir / 'research_evidence_universal_scene'
    manifest_path = evidence_dir / 'manifest.json'
    manifest = _load_json(manifest_path)
    _require(manifest.get('schema') == UNIVERSAL_RESEARCH_MANIFEST_SCHEMA, 'universal research manifest schema mismatch')
    _require(manifest.get('status') == 'approved', 'universal research manifest is not approved')
    _require(manifest.get('totals') == UNIVERSAL_RESEARCH_EXPECTED_TOTALS, 'universal research frozen totals mismatch')
    audit = manifest.get('independent_audit')
    _require(isinstance(audit, dict), 'universal research independent audit is missing')
    _require(audit.get('verdict') == 'pass' and audit.get('critical') == 0 and (audit.get('high') == 0) and (audit.get('medium') == 0), 'universal research independent audit is not clean')
    shards = manifest.get('shards')
    _require(isinstance(shards, list) and len(shards) == 6, 'universal research must list six shards')
    rows: list[dict[str, Any]] = []
    shard_results: list[dict[str, Any]] = []
    declared_topic_ids: list[str] = []
    for entry in shards:
        _require(isinstance(entry, dict), 'universal research shard entry must be an object')
        _require(set(entry) == {'path', 'sha256', 'record_count', 'topic_ids'}, 'universal research shard entry field mismatch')
        rel = entry.get('path')
        _require(isinstance(rel, str) and rel and (Path(rel).name == rel) and rel.endswith('.jsonl'), 'universal research shard path must be one local JSONL filename')
        path = evidence_dir / rel
        _require(path.is_file(), f'missing universal research shard {rel}')
        digest = _sha256(path)
        _require(digest == entry.get('sha256'), f'universal research shard hash mismatch: {rel}')
        shard_rows = _load_jsonl(path)
        _require(len(shard_rows) == entry.get('record_count'), f'universal research shard row count mismatch: {rel}')
        shard_topics = _strings(entry.get('topic_ids'), f'{rel}.topic_ids', minimum=1)
        _require({str(row.get('topic_id')) for row in shard_rows} == set(shard_topics), f'universal research shard topic coverage mismatch: {rel}')
        rows.extend(shard_rows)
        declared_topic_ids.extend(shard_topics)
        shard_results.append({'path': rel, 'record_count': len(shard_rows), 'sha256': digest})
    _require(len(rows) == 60, 'universal research record count must be 60')
    _require(len(declared_topic_ids) == len(set(declared_topic_ids)) == 20, 'universal research shard topics must partition 20 topics')
    _require(manifest.get('topic_ids') == declared_topic_ids, 'universal research manifest topic order must match shard order')
    matrix_keys = {'schema', 'record_id', 'topic_id', 'record_role', 'reviewed_at', 'status', 'synthesis_evidence_ids', 'research_questions', 'mechanisms', 'mechanism_provenance', 'candidate_ids', 'candidate_definitions', 'candidate_roles', 'pixel_evidence_ids', 'pixel_evidence_definitions', 'compatibility', 'conflicts', 'counterexamples', 'boundaries', 'domain_limits', 'embodiment_limits', 'cultural_limits', 'source_biases', 'runtime_implications', 'evaluation_implications'}
    source_keys = {'schema', 'record_id', 'topic_id', 'record_role', 'reviewed_at', 'status', 'source_url', 'title', 'source_type', 'authority', 'abstracted_dimensions', 'supported_candidate_ids', 'limitations'}
    record_ids = [row.get('record_id') for row in rows]
    _require(all((isinstance(value, str) and value for value in record_ids)) and len(record_ids) == len(set(record_ids)), 'universal research record IDs must be globally unique strings')
    all_record_ids = set(record_ids)
    by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        _require(row.get('schema') == UNIVERSAL_RESEARCH_SCHEMA, 'universal research row schema mismatch')
        _require(row.get('reviewed_at') == '2026-08-10', 'universal research review date drift')
        _require(row.get('status') == 'approved', 'universal research row is not approved')
        _require(row.get('record_role') in UNIVERSAL_RESEARCH_ROLE_VALUES, 'universal research row role mismatch')
        topic_id = row.get('topic_id')
        _require(isinstance(topic_id, str) and topic_id, 'universal research topic ID missing')
        by_topic[topic_id].append(row)
        expected_keys = matrix_keys if row['record_role'] == 'topic_matrix' else source_keys
        _require(set(row) == expected_keys, f'universal research row field mismatch: {row['record_id']}')
    _require(set(by_topic) == set(declared_topic_ids), 'universal research topic coverage mismatch')
    candidate_ids: list[str] = []
    pixel_evidence_ids: list[str] = []
    mechanism_ids: list[str] = []
    source_urls: list[str] = []
    role_counts: Counter[str] = Counter()
    provenance_counts: Counter[str] = Counter()
    candidate_specs: dict[str, dict[str, Any]] = {}
    topic_record_ids: dict[str, set[str]] = {}
    for topic_id, topic_rows in by_topic.items():
        matrices = [row for row in topic_rows if row['record_role'] == 'topic_matrix']
        sources = [row for row in topic_rows if row['record_role'] == 'independent_source']
        _require(len(topic_rows) == 3 and len(matrices) == 1 and (len(sources) == 2), f'{topic_id} must contain one matrix and two independent sources')
        matrix = matrices[0]
        source_ids = {row['record_id'] for row in sources}
        topic_record_ids[topic_id] = source_ids | {matrix['record_id']}
        _require(set(matrix.get('synthesis_evidence_ids', [])) == source_ids, f'{topic_id} synthesis must reference exactly its two independent sources')
        for source in sources:
            url = source.get('source_url')
            _require(isinstance(url, str) and url.startswith('https://'), f'{topic_id} source URL invalid')
            source_urls.append(url)
            _strings(source.get('abstracted_dimensions'), f'{source['record_id']}.abstracted_dimensions', minimum=2)
            _strings(source.get('limitations'), f'{source['record_id']}.limitations', minimum=2)
            _require(source.get('supported_candidate_ids') == [], f'{source['record_id']} must not overclaim direct runtime-candidate support')
        mechanisms = matrix.get('mechanisms')
        provenance = matrix.get('mechanism_provenance')
        _require(isinstance(mechanisms, list) and mechanisms, f'{topic_id} mechanisms missing')
        _require(isinstance(provenance, list) and len(provenance) == len(mechanisms), f'{topic_id} mechanism provenance mismatch')
        local_mechanism_ids: list[str] = []
        for mechanism in mechanisms:
            _require(isinstance(mechanism, dict) and set(mechanism) == {'id', 'statement'} and isinstance(mechanism.get('id'), str) and isinstance(mechanism.get('statement'), str) and mechanism['statement'].strip(), f'{topic_id} mechanism shape mismatch')
            local_mechanism_ids.append(mechanism['id'])
        _require(local_mechanism_ids == [item.get('mechanism_id') for item in provenance], f'{topic_id} mechanism/provenance order mismatch')
        for item in provenance:
            _require(isinstance(item, dict) and set(item) == {'mechanism_id', 'provenance', 'evidence_ids'}, f'{topic_id} mechanism provenance shape mismatch')
            kind = item.get('provenance')
            _require(kind in PROVENANCE_VALUES, f'{topic_id} invalid mechanism provenance')
            refs = _strings(item.get('evidence_ids'), f'{item['mechanism_id']}.evidence_ids', minimum=1)
            _require(set(refs) <= all_record_ids, f'{item['mechanism_id']} has unknown evidence')
            _require(set(refs) <= source_ids, f'{item['mechanism_id']} has cross-topic or matrix evidence')
            if kind == 'cross_source_synthesis':
                _require(set(refs) == source_ids, f'{item['mechanism_id']} lacks both sources')
            if kind == 'source_supported':
                _require(len(refs) == 1, f'{item['mechanism_id']} source support must be singular')
            provenance_counts[kind] += 1
        mechanism_ids.extend(local_mechanism_ids)
        local_candidate_ids = _strings(matrix.get('candidate_ids'), f'{topic_id}.candidate_ids', minimum=1)
        definitions = matrix.get('candidate_definitions')
        roles = matrix.get('candidate_roles')
        _require(isinstance(definitions, dict) and set(definitions) == set(local_candidate_ids), f'{topic_id} candidate definitions mismatch')
        _require(isinstance(roles, dict) and set(roles) == set(local_candidate_ids), f'{topic_id} candidate roles mismatch')
        _require(set(roles.values()) <= UNIVERSAL_CANDIDATE_ROLE_VALUES, f'{topic_id} candidate role is outside the closed enum')
        local_pixel_ids = _strings(matrix.get('pixel_evidence_ids'), f'{topic_id}.pixel_evidence_ids', minimum=0)
        pixel_definitions = matrix.get('pixel_evidence_definitions')
        _require(isinstance(pixel_definitions, dict) and set(pixel_definitions) == set(local_pixel_ids), f'{topic_id} pixel evidence definitions mismatch')
        _require(set(local_pixel_ids) <= set(local_candidate_ids) and all((roles[value] == 'visual_atom' for value in local_pixel_ids)), f'{topic_id} pixel evidence must be a visual-candidate subset')
        for field, minimum in {'research_questions': 3, 'compatibility': 4, 'conflicts': 4, 'counterexamples': 4, 'boundaries': 4, 'domain_limits': 3, 'embodiment_limits': 3, 'cultural_limits': 3, 'source_biases': 3, 'runtime_implications': 4, 'evaluation_implications': 4}.items():
            _strings(matrix.get(field), f'{topic_id}.{field}', minimum=minimum)
        for candidate_id in local_candidate_ids:
            definition = definitions[candidate_id]
            _require(isinstance(definition, str) and definition.strip(), f'{candidate_id} definition missing')
            role_counts[roles[candidate_id]] += 1
            candidate_specs[candidate_id] = {'definition': definition, 'role': roles[candidate_id], 'topic_id': topic_id, 'matrix_id': matrix['record_id'], 'record_ids': topic_record_ids[topic_id], 'has_pixel_evidence': candidate_id in set(local_pixel_ids)}
        candidate_ids.extend(local_candidate_ids)
        pixel_evidence_ids.extend(local_pixel_ids)
    _require(len(source_urls) == len(set(source_urls)) == 40, 'universal research source URLs must be 40/40 unique')
    _require(len(mechanism_ids) == len(set(mechanism_ids)) == 167, 'universal research mechanism IDs must be 167 unique values')
    _require(len(candidate_ids) == len(set(candidate_ids)) == 220, 'universal research candidate IDs must be 220 unique values')
    _require(len(pixel_evidence_ids) == len(set(pixel_evidence_ids)) == 97, 'universal research pixel IDs must be 97 unique values')
    _require(dict(role_counts) == UNIVERSAL_RESEARCH_EXPECTED_TOTALS['candidate_role_counts'], 'universal research candidate role counts mismatch')
    _require(dict(provenance_counts) == UNIVERSAL_RESEARCH_EXPECTED_TOTALS['mechanism_provenance_counts'], 'universal research provenance counts mismatch')
    return {'manifest_sha256': _sha256(manifest_path), 'record_count': len(rows), 'topic_count': len(by_topic), 'independent_source_count': len(source_urls), 'mechanism_count': len(mechanism_ids), 'candidate_count': len(candidate_ids), 'pixel_evidence_count': len(pixel_evidence_ids), 'candidate_role_counts': dict(sorted(role_counts.items())), 'mechanism_provenance_counts': dict(sorted(provenance_counts.items())), 'candidate_specs': candidate_specs, 'record_ids': all_record_ids, 'topic_ids': set(by_topic), 'topic_record_ids': topic_record_ids, 'shards': shard_results}

def _predicate_groups(value: Any, label: str, allowed_kinds: set[str]) -> list[list[str]]:
    """Validate flat predicates plus requires-any disjunction groups."""
    _require(isinstance(value, list), f'{label} must be a predicate list')
    predicates: list[list[str]] = []
    for index, item in enumerate(value):
        group = item if isinstance(item, list) else None
        _require(group is not None, f'{label}[{index}] must be an array')
        if len(group) == 3 and all((isinstance(part, str) and part for part in group)):
            candidates = [group]
        else:
            _require(group, f'{label}[{index}] predicate disjunction must not be empty')
            candidates = group
        for predicate in candidates:
            _require(isinstance(predicate, list) and len(predicate) == 3 and all((isinstance(part, str) and part for part in predicate)), f'{label}[{index}] predicate must be a three-string tuple')
            _require(predicate[0] in allowed_kinds, f'{label} has unknown predicate kind: {predicate[0]}')
            predicates.append(predicate)
    return predicates

def _zero_vector(value: Any, axes: list[str], label: str, *, maximum: int=3) -> dict[str, int]:
    _require(isinstance(value, dict) and list(value) == axes, f'{label} axis order mismatch')
    for axis in axes:
        item = value[axis]
        _require(isinstance(item, int) and (not isinstance(item, bool)) and (0 <= item <= maximum), f'{label}.{axis} must be an integer in 0..{maximum}')
    return value

def _universal_distance_band(vector: Mapping[str, int]) -> str:
    """Recompute the frozen ordinal band without trusting a data label."""
    maximum = max(vector.values())
    total = sum(vector.values())
    if maximum == 3 or total >= 10:
        return 'far'
    if maximum == 2 or total >= 4:
        return 'middle'
    return 'near'

def _normalize_universal_semantic_family_value(value: Any) -> str:
    """Normalize one data-owned semantic-family ontology value."""
    if value is None:
        return 'null'
    _require(isinstance(value, str), 'universal semantic-family values must be strings or null')
    normalized = unicodedata.normalize('NFKC', value).casefold()
    normalized = re.sub('[_-]', ' ', normalized)
    normalized = ' '.join(normalized.split())
    if normalized in {'$identity actor', '$actor'}:
        return '$actor'
    if normalized in {'$scene location', '$location'}:
        return '$location'
    return normalized

def _universal_semantic_family_payload(profile: Mapping[str, Any], candidate_by_id: Mapping[str, Mapping[str, Any]], prop_concept_ids: set[str]) -> dict[str, Any]:
    """Independently recompute the frozen ID-independent proposal family."""
    value_id = profile.get('value_id')
    _require(isinstance(value_id, str) and value_id in prop_concept_ids, 'universal proposal semantic family references an unknown prop concept')
    reduced: dict[tuple[str, str, str], int] = {}
    for candidate_id in profile['candidate_ids']:
        candidate = candidate_by_id[str(candidate_id)]
        for claim in candidate['runtime_contract']['resource_claims']:
            _require(isinstance(claim, list) and len(claim) == 4, f'{candidate_id} semantic-family resource claim must be a raw four-item tuple')
            resource_kind, owner_scope, amount, mode = claim
            _require(isinstance(resource_kind, str) and resource_kind and isinstance(owner_scope, str) and owner_scope and isinstance(amount, int) and (not isinstance(amount, bool)) and (amount > 0) and (mode in {'exclusive', 'shared'}), f'{candidate_id} semantic-family resource claim is invalid')
            if owner_scope in {'actor', 'scene'}:
                normalized_owner = owner_scope
            else:
                _require(owner_scope in UNIVERSAL_EVENT_ROLE_IDS, f'{candidate_id} semantic-family owner is outside the closed role domain')
                normalized_owner = f'role:{_normalize_universal_semantic_family_value(owner_scope)}'
            key = (normalized_owner, _normalize_universal_semantic_family_value(resource_kind), str(mode))
            if mode == 'exclusive':
                reduced[key] = reduced.get(key, 0) + amount
            else:
                reduced[key] = max(reduced.get(key, 0), amount)
    event_roles = profile['event_roles']
    return {'schema': 'subculture-illustration-semantic-family-key/v1', 'slot': _normalize_universal_semantic_family_value(profile['slot_id']), 'prop_concept': _normalize_universal_semantic_family_value(value_id), 'event_frame': {role_id: _normalize_universal_semantic_family_value(event_roles[role_id]) for role_id in UNIVERSAL_EVENT_ROLE_IDS}, 'resource_footprint': [{'owner_scope': owner_scope, 'resource_kind': resource_kind, 'mode': mode, 'amount': amount} for (owner_scope, resource_kind, mode), amount in sorted(reduced.items())]}

def _forbidden_pair_structures(value: Any, path: str='') -> list[str]:
    forbidden: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f'{path}.{key}' if path else str(key)
            normalized = str(key).casefold().replace('-', '_')
            if normalized in {'pair_matrix', 'compatibility_matrix', 'all_pairs', 'all_pairs_scan', 'pairwise_edges', 'candidate_pairs'}:
                forbidden.append(child_path)
            forbidden.extend(_forbidden_pair_structures(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            forbidden.extend(_forbidden_pair_structures(child, f'{path}[{index}]'))
    return forbidden

def _normalized_effect_text(value: Any) -> str:
    normalized = unicodedata.normalize('NFKC', str(value)).casefold()
    normalized = re.sub('[_/.-]+', ' ', normalized)
    return re.sub('\\s+', ' ', normalized).strip()

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
    raw = unicodedata.normalize('NFKC', str(value)).casefold()
    hard_clauses = re.split('[.!?;:。！？；：\\r\\n]+|\\s*[\\u2012-\\u2015]\\s*|\\b(?:and\\s+then|but|however|yet|whereas|while|then|even\\s+though|although)\\b|(?:하지만|그러나|반면|그런데|그\\s*뒤|그\\s*후|しかし|ただし|一方|その後|但是|然而|不过|但)', raw)
    soft_separator = re.compile('\\band\\b|그리고|하고|そして|并且|然后')
    independent_english_subject = re.compile('^(?:a|an|the|this|that|these|those|another|it|he|she|they|we|i|you)\\b')
    result: list[str] = []
    for hard_clause in hard_clauses:
        cursor = 0
        force_negative = False
        for separator in soft_separator.finditer(hard_clause):
            raw_clause = hard_clause[cursor:separator.start()]
            clause = _normalized_effect_text(raw_clause)
            if clause:
                if force_negative and (not _effect_clause_is_negative(clause)):
                    clause = f'do not {clause}'
                result.append(clause)
                force_negative = _effect_clause_is_negative(clause)
            rhs = _normalized_effect_text(hard_clause[separator.end():])
            if separator.group(0) == 'and' and independent_english_subject.match(rhs):
                force_negative = False
            cursor = separator.end()
        raw_clause = hard_clause[cursor:]
        clause = _normalized_effect_text(raw_clause)
        if clause:
            if force_negative and (not _effect_clause_is_negative(clause)):
                clause = f'do not {clause}'
            result.append(clause)
    return result

def _effect_text_match_spans(text: str, term: str) -> list[tuple[int, int]]:
    normalized_term = _normalized_effect_text(term)
    if not normalized_term:
        return []
    if normalized_term.isascii():
        suffix = '(?:s|es|ed|d|ing)?' if re.fullmatch('[a-z]+', normalized_term) and len(normalized_term) >= 4 else ''
        return [match.span() for match in re.finditer('(?<![a-z0-9])' + re.escape(normalized_term) + suffix + '(?![a-z0-9])', text)]
    return [(match.start(), match.end()) for match in re.finditer(re.escape(normalized_term), text)]

def _effect_match_substitution_side(clause: str, start: int, end: int) -> str | None:
    """Return a positive substitution segment, or ``None`` when rejected.

    Substitution markers are directional.  Treating the whole clause as
    negative made the Chinese ``A, rather than B`` form hide a positive A,
    while splitting at the marker made Korean/Japanese rejected alternatives
    look positive.  Segment labels also stop compositional lexeme groups from
    borrowing one half from each side of ``A 아니라 B``.
    """
    for marker in re.finditer('아니라|대신', clause):
        intervening = clause[end:marker.start()].strip(' ,')
        if end <= marker.start() and ' ' not in intervening:
            return None
        if end <= marker.start():
            return f'pre:{marker.start()}'
        if start >= marker.end():
            return f'post:{marker.start()}'
    for marker in re.finditer('(?:の)?ではなく|ではない|(?:の)?代わり(?:に)?', clause):
        if end <= marker.start():
            return None
        if start >= marker.end():
            return f'post:{marker.start()}'
    for marker in re.finditer('(?<!而)不是', clause):
        positive_turn = re.search('而是', clause[marker.end():])
        negative_end = marker.end() + positive_turn.start() if positive_turn is not None else len(clause)
        if start >= marker.end() and end <= negative_end:
            return None
        if positive_turn is not None and start >= negative_end + len('而是'):
            return f'post:{marker.start()}'
    for marker in re.finditer('而不是', clause):
        if start >= marker.end():
            return None
        if end <= marker.start():
            return f'pre:{marker.start()}'
    for marker in re.finditer('\\b(?:instead\\s+of|rather\\s+than)\\b', clause):
        negative_end = len(clause)
        if not clause[:marker.start()].strip():
            comma = clause.find(',', marker.end())
            if comma >= 0:
                negative_end = comma
        if start >= marker.end() and end <= negative_end:
            return None
        if end <= marker.start():
            return f'pre:{marker.start()}'
        if start >= negative_end and negative_end != len(clause):
            return f'post:{marker.start()}'
    return 'main'

def _effect_clause_is_negative(clause: str) -> bool:
    without_not_only = re.sub('\\bnot\\s+only\\b', '', clause)
    return re.search("\\b(?:no|never|without|cannot|can't|do\\s+not|does\\s+not|don't|doesn't|must\\s+not|should\\s+not|forbid(?:den)?|exclude(?:d)?|omit(?:ted)?)\\b|(?:않|아닌|없|금지|하지\\s*마|지\\s*마|말아|ない|禁止|不要|不(?:要|添加|装|长)|無|无)", without_not_only) is not None

def _effect_clause_positive_term_sides(clause: str, terms: Iterable[Any]) -> set[str]:
    if _effect_clause_is_negative(clause):
        return set()
    return {side for term in terms for start, end in _effect_text_match_spans(clause, str(term)) if (side := _effect_match_substitution_side(clause, start, end)) is not None}

def _effect_clause_has_positive_term(clause: str, terms: Iterable[Any]) -> bool:
    return bool(_effect_clause_positive_term_sides(clause, terms))

def _classify_universal_contract_effects(texts: Iterable[Any], contract_effect_profiles: Iterable[Mapping[str, Any]]) -> set[str]:
    """Classify positive blocked semantics from values, aliases, or term groups."""
    clauses = [clause for value in texts for clause in _effect_text_clauses(value)]
    effects: set[str] = set()
    for profile in contract_effect_profiles:
        effect_id = str(profile['effect_id'])
        semantic_values = [str(value) for value in profile['semantic_value_ids']]
        aliases = [str(value) for record in profile['literal_aliases'] for value in record['values']]
        groups = profile['required_literal_groups']
        for clause in clauses:
            semantic_match = _effect_clause_has_positive_term(clause, semantic_values)
            alias_match = _effect_clause_has_positive_term(clause, aliases)
            group_sides = [_effect_clause_positive_term_sides(clause, group) for group in groups]
            compositional_match = bool(group_sides) and bool(set.intersection(*group_sides))
            if semantic_match or alias_match or compositional_match:
                effects.add(effect_id)
                break
    return effects

def _validate_contract_effect_profiles(semantic_asset: Mapping[str, Any]) -> list[dict[str, Any]]:
    profiles = semantic_asset.get('contract_effect_profiles')
    _require(isinstance(profiles, list) and len(profiles) == 9, 'universal contract effect profile inventory mismatch')
    by_effect: dict[str, dict[str, Any]] = {}
    for profile in profiles:
        _require(isinstance(profile, dict) and set(profile) == {'id', 'effect_id', 'source_targets', 'semantic_value_ids', 'literal_aliases', 'required_literal_groups', 'polarity', 'subject_binding'}, 'universal contract effect profile shape mismatch')
        effect_id = profile.get('effect_id')
        _require(isinstance(effect_id, str) and effect_id in UNIVERSAL_CONTRACT_EFFECT_SUBJECT_BY_ID and (effect_id not in by_effect) and (profile.get('id') == f'contract_effect_{effect_id}') and (profile.get('polarity') == 'affirmative') and (profile.get('subject_binding') == UNIVERSAL_CONTRACT_EFFECT_SUBJECT_BY_ID[effect_id]), 'universal contract effect ID/polarity/subject binding drift')
        targets = profile.get('source_targets')
        _require(isinstance(targets, list) and [(target.get('source_kind'), target.get('source_id')) for target in targets if isinstance(target, dict) and set(target) == {'source_kind', 'source_id'}] == UNIVERSAL_CONTRACT_EFFECT_TARGETS_BY_ID[effect_id], f'universal contract effect source targets drift: {effect_id}')
        _strings(profile.get('semantic_value_ids'), f'contract_effect.{effect_id}.semantic_value_ids', minimum=1)
        aliases = profile.get('literal_aliases')
        _require(isinstance(aliases, list) and [record.get('locale') for record in aliases if isinstance(record, dict)] == ['ko', 'en', 'ja', 'zh'], f'universal contract effect locale coverage drift: {effect_id}')
        for record in aliases:
            _require(isinstance(record, dict) and set(record) == {'locale', 'values'}, f'universal contract effect alias shape drift: {effect_id}')
            _strings(record.get('values'), f'contract_effect.{effect_id}.{record['locale']}', minimum=1)
        groups = profile.get('required_literal_groups')
        _require(isinstance(groups, list) and len(groups) in {2, 3} and all((isinstance(group, list) and len(group) >= 2 and all((isinstance(value, str) and value.strip() for value in group)) for group in groups)), f'universal contract effect compositional groups drift: {effect_id}')
        if effect_id.startswith('human_'):
            _require(len(groups) == 3 and any((value in groups[0] for value in ('human', '사람', '人間', '人类'))) and any((value in groups[2] for value in ('attach', 'add', 'sprout', 'grow', '붙', '추가', '添加', '长出'))), f'universal human-attachment compositional guard weakened: {effect_id}')
        by_effect[effect_id] = profile
    _require(set(by_effect) == set(UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS), 'universal contract effects do not exactly cover the blocked semantic enum')
    return profiles

def _validate_universal_composition_literal_carriers(semantic_asset: Mapping[str, Any], target_inventory: Mapping[str, Mapping[str, Any]]) -> dict[str, int]:
    """Prove explicit English carriers exactly cover the canonical target set."""
    profile_set = semantic_asset.get('composition_literal_carrier_profiles')
    _require(isinstance(profile_set, Mapping) and list(profile_set) == ['identity_core', 'fixed_slots', 'event_roles'], 'universal composition literal-carrier section mismatch')
    section_fields = {'identity_core': ['fact_id', 'polarity', 'required_lexeme_groups'], 'fixed_slots': ['slot_id', 'value_id', 'required_lexeme_groups'], 'event_roles': ['role_id', 'value_id', 'required_lexeme_groups']}
    key_fields = {'identity_core': ('fact_id', 'polarity'), 'fixed_slots': ('slot_id', 'value_id'), 'event_roles': ('role_id', 'value_id')}
    internal_tokens = {'atom', 'candidate', 'cbg', 'dpa', 'ecs', 'facet', 'gha', 'global', 'id', 'ofm', 'predicate', 'profile', 'sdc', 'sptg', 'uao', 'ubp', 'ugf', 'usc', 'ush', 'usl'}
    actual: dict[str, set[tuple[str, ...]]] = {section: set() for section in section_fields}
    for section, fields in section_fields.items():
        records = profile_set.get(section) if isinstance(profile_set, Mapping) else None
        _require(isinstance(records, list) and records, f'universal composition carrier {section} must be a nonempty list')
        for index, profile in enumerate(records):
            _require(isinstance(profile, Mapping) and list(profile) == fields, f'universal composition carrier shape/order drift: {section}[{index}]')
            key = tuple((str(profile.get(field, '')) for field in key_fields[section]))
            _require(all(key) and key not in actual[section], f'universal composition carrier key is empty or duplicated: {section}/{key}')
            if section == 'identity_core':
                _require(key[1] in {'asserted_presence', 'forbidden'}, f'universal composition carrier polarity drift: {key}')
            groups = profile.get('required_lexeme_groups')
            _require(isinstance(groups, list) and 1 <= len(groups) <= (3 if section == 'identity_core' else 2), f'universal composition carrier group bound drift: {section}/{key}')
            seen_groups: set[tuple[str, ...]] = set()
            for group in groups:
                normalized_group = tuple((str(item) for item in group)) if isinstance(group, list) else ()
                _require(bool(normalized_group) and normalized_group not in seen_groups and (len(normalized_group) == len(set(normalized_group))) and all((re.fullmatch('[a-z0-9]+(?: [a-z0-9]+)*', alternative) is not None and alternative == normalize_text(alternative) and (not set(alternative.split()) & internal_tokens) for alternative in normalized_group)), f'universal composition carrier must be normalized reviewed English: {section}/{key}')
                seen_groups.add(normalized_group)
            actual[section].add(key)
    expected: dict[str, set[tuple[str, ...]]] = {section: set() for section in section_fields}
    _require(target_inventory.get('schema') == 'subculture-illustration-composition-targets/v1', 'invalid composition target inventory schema')
    targets = target_inventory.get('targets')
    _require(isinstance(targets, Mapping) and list(targets) == list(key_fields), 'invalid composition target sections')
    for section, fields in key_fields.items():
        rows = targets[section]
        _require(isinstance(rows, list) and bool(rows), f'empty composition targets: {section}')
        for row in rows:
            _require(isinstance(row, Mapping) and tuple(row) == fields, f'invalid composition target keys: {section}')
            pair = tuple((row[field] for field in fields))
            _require(all((isinstance(value, str) and bool(value) for value in pair)), f'invalid composition target values: {section}')
            _require(pair not in expected[section], f'duplicate composition target: {section}/{pair}')
            expected[section].add(pair)
    _require(actual == expected, 'universal composition carriers do not exactly cover canonical semantic targets')
    total = sum((len(values) for values in actual.values()))
    _require(semantic_asset.get('counts', {}).get('composition_literal_carrier_profiles') == total, 'universal composition carrier count drift')
    return {'identity_core': len(actual['identity_core']), 'fixed_slots': len(actual['fixed_slots']), 'event_roles': len(actual['event_roles']), 'total': total}

def _validate_universal_literal_realization_profiles(semantic_asset: Mapping[str, Any], candidate_by_id: Mapping[str, Mapping[str, Any]], resource_kind_ids: Sequence[str]) -> dict[str, Any]:
    """Validate the reviewed, case-independent literal realization table."""
    expected_top_keys = ['schema', 'reviewed_at', 'normalization', 'prop_literal_sense_bindings', 'explicit_capability_assertion_profiles', 'literal_polarity_contract', 'literal_quantity_bindings', 'identity_literal_profiles', 'composition_literal_carrier_profiles', 'context_literal_profiles', 'literal_visual_realization_profiles', 'visual_carrier_profiles', 'resource_carrier_profiles', 'semantic_effect_registry', 'guard_execution_profiles', 'contract_effect_profiles', 'counts']
    _require(isinstance(semantic_asset, Mapping) and list(semantic_asset) == expected_top_keys and (semantic_asset.get('schema') == 'subculture-illustration-universal-semantic-bindings/v1'), 'universal semantic-binding top-level contract mismatch')
    _require(semantic_asset.get('prop_literal_sense_bindings') == [{'id': 'prop_sense_wooden_mallet_not_generic_hammer', 'catalog_prop_id': 'prop_hammer', 'literal_aliases': [{'locale': 'ko', 'values': ['나무 망치', '나무망치', '목재 망치']}, {'locale': 'en', 'values': ['wooden mallet', 'small wooden mallet', 'mallet']}, {'locale': 'ja', 'values': ['木槌', '木製の槌']}, {'locale': 'zh', 'values': ['木槌', '木锤', '木錘']}], 'accepted_semantic_tokens': ['mallet'], 'activation_target': 'prop_wooden_mallet'}], 'universal wooden-mallet literal sense binding drift')
    expected_profiles: list[dict[str, Any]] = []
    actor_primary = [{'role_id': 'actor', 'entity_quantifier': 'primary'}]
    participant_overrides = {'lvr_shared_attention_convergence': [{'role_id': 'actor', 'entity_quantifier': 'all'}], 'lvr_protective_recipient_path': [{'role_id': 'actor', 'entity_quantifier': 'primary'}, {'role_id': 'recipient', 'entity_quantifier': 'all'}], 'lvr_shared_target_convergence': [{'role_id': 'actor', 'entity_quantifier': 'all'}]}
    for profile_id, source_slot_id, mechanism_class_id, realized_facet, candidate_group, literal_scope, required_literal_groups, owned_pixel_kinds, owned_resource_kinds, selection_rank in UNIVERSAL_V2_LITERAL_REALIZATION_PROFILE_SPECS:
        expected_profiles.append({'id': profile_id, 'source_slot_id': source_slot_id, 'mechanism_class_id': mechanism_class_id, 'realized_facet': realized_facet, 'candidate_group': candidate_group, 'participant_roles': copy.deepcopy(participant_overrides.get(profile_id, actor_primary)), 'quantifier': 'all', 'enforcement': 'selected', 'literal_scope': literal_scope, 'required_literal_groups': [{'alternatives': alternatives, 'required_polarity': required_polarity} for alternatives, required_polarity in required_literal_groups], 'owned_pixel_kinds': owned_pixel_kinds, 'owned_resource_kinds': owned_resource_kinds, 'selection_rank': selection_rank})
    profiles = semantic_asset.get('literal_visual_realization_profiles')
    _require(profiles == expected_profiles, 'universal literal visual realization profiles drift from the reviewed 19-profile table')
    profile_keys = ['id', 'source_slot_id', 'mechanism_class_id', 'realized_facet', 'candidate_group', 'participant_roles', 'quantifier', 'enforcement', 'literal_scope', 'required_literal_groups', 'owned_pixel_kinds', 'owned_resource_kinds', 'selection_rank']
    candidate_owners: set[str] = set()
    resource_kind_set = set(resource_kind_ids)
    for profile in profiles:
        _require(list(profile) == profile_keys and profile['candidate_group'] == sorted(set(profile['candidate_group'])) and profile['required_literal_groups'] and (profile['owned_pixel_kinds'] == sorted(set(profile['owned_pixel_kinds']))) and (profile['owned_resource_kinds'] == sorted(set(profile['owned_resource_kinds']))) and (set(profile['owned_resource_kinds']) <= resource_kind_set), f'literal realization profile closure/order drift: {profile['id']}')
        participant_role_ids = [str(item['role_id']) for item in profile['participant_roles']]
        _require(all((list(item) == ['role_id', 'entity_quantifier'] and item['role_id'] in UNIVERSAL_EVENT_ROLE_IDS and (item['entity_quantifier'] in {'primary', 'all'}) for item in profile['participant_roles'])) and len(participant_role_ids) == len(set(participant_role_ids)) and (participant_role_ids == [role_id for role_id in UNIVERSAL_EVENT_ROLE_IDS if role_id in participant_role_ids]), f'literal realization participant binding drift: {profile['id']}')
        for group in profile['required_literal_groups']:
            _require(list(group) == ['alternatives', 'required_polarity'] and group['alternatives'] and (group['alternatives'] == sorted(set(group['alternatives']))) and all((isinstance(value, str) and value.strip() and ('_' not in value) for value in group['alternatives'])) and (group['required_polarity'] in {'affirmative', 'negated'}), f'literal realization required group drift: {profile['id']}')
        for candidate_id in profile['candidate_group']:
            candidate = candidate_by_id.get(candidate_id)
            _require(candidate is not None and candidate.get('role') == 'visual_atom' and (candidate.get('facet') == profile['realized_facet']) and (candidate_id not in candidate_owners), f'literal realization candidate owner/facet drift: {candidate_id}')
            candidate_owners.add(candidate_id)
            pixel_kinds = {str(item['kind']) for item in candidate['runtime_contract']['pixel_evidence']}
            resource_kinds = {str(item[0]) for item in candidate['runtime_contract']['resource_claims']}
            _require(set(profile['owned_pixel_kinds']) <= pixel_kinds and set(profile['owned_resource_kinds']) <= resource_kinds, f'literal realization candidate material ownership drift: {candidate_id}')
    counts = semantic_asset.get('counts')
    _require(isinstance(counts, Mapping) and counts.get('literal_visual_realization_profiles') == 19, 'universal literal realization profile count drift')
    return {'profile_count': len(profiles), 'candidate_owner_count': len(candidate_owners)}

def _validate_universal_quiet_theme_source_contract(profile: Mapping[str, Any], candidate_by_id: Mapping[str, Mapping[str, Any]]) -> None:
    """Pin the reviewed quiet-theme source to a zero displacement outcome."""
    _require(profile.get('id') == 'context_quiet_theme_guard_middle' and profile.get('distance_profile', {}).get('theme') == 0 and (profile.get('load_profile', {}).get('theme_displacement') == 0), 'quiet-theme source must have zero theme distance and displacement load')
    carrier_ids = profile.get('candidate_ids')
    _require(isinstance(carrier_ids, list) and carrier_ids and all((candidate_id in candidate_by_id and candidate_by_id[candidate_id]['runtime_contract']['load_profile']['theme_displacement'] == 0 for candidate_id in carrier_ids)), 'quiet-theme source carriers must preserve zero theme displacement')

def _validate_universal_fixed_prop_eligibility_source_contract(candidate_by_id: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Pin the sole generic visual carrier eligible for open or fixed props."""
    predicate = ['slot', 'prop', 'open_or_fixed']
    eligible_ids = sorted((candidate_id for candidate_id, candidate in candidate_by_id.items() if predicate in candidate.get('triggers', [])))
    _require(eligible_ids == ['uer_role_bearing_contact'], 'fixed-prop eligibility must use only the reviewed generic role-bearing carrier')
    carrier = candidate_by_id['uer_role_bearing_contact']
    runtime = carrier['runtime_contract']
    _require(carrier.get('role') == 'visual_atom' and carrier.get('facet') == 'prop' and (carrier.get('parameters') == {}) and (carrier.get('triggers') == [predicate]) and (runtime.get('requires_all') == [['event_role', 'actor', 'present'], ['capability', 'actor', 'manipulator_or_equivalent']]) and (['slot', 'prop', 'closed'] in runtime.get('forbids_any', [])) and (runtime.get('resource_claims') == [['manipulator', 'actor', 1, 'exclusive'], ['prop_slot', 'scene', 1, 'exclusive']]), 'fixed-prop generic carrier source contract drift')
    return {'candidate_ids': eligible_ids, 'selection_required': False}

def _validate_universal_semantic_effect_policy(candidate_asset: Mapping[str, Any], compatibility: Mapping[str, Any], semantic_asset: Mapping[str, Any]) -> dict[str, Any]:
    """Independently bind the safe v1 source catalog to an empty effect policy."""
    contract_effect_profiles = _validate_contract_effect_profiles(semantic_asset)
    registry = semantic_asset.get('semantic_effect_registry')
    _require(isinstance(registry, dict) and list(registry) == ['schema', 'effect_ids', 'source_kind_ids', 'profiles', 'counts'] and (registry.get('schema') == 'illustration-universal-semantic-effect-registry/v1'), 'universal semantic effect registry contract mismatch')
    _require(registry.get('effect_ids') == sorted(UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS) and registry.get('source_kind_ids') == UNIVERSAL_EFFECT_SOURCE_KIND_IDS, 'universal semantic effect registry closed enums drift')
    candidates = candidate_asset.get('candidates')
    proposals = candidate_asset.get('proposal_profiles')
    contexts = candidate_asset.get('context_distance_profiles')
    bridge_policy = compatibility.get('bridge_policy')
    _require(isinstance(candidates, list) and isinstance(proposals, list) and isinstance(contexts, list) and isinstance(bridge_policy, dict), 'universal effect registry source catalogs are missing')
    expected_by_kind = {'visual_candidate': sorted((str(candidate['id']) for candidate in candidates if isinstance(candidate, dict) and candidate.get('role') == 'visual_atom')), 'proposal_profile': sorted((str(profile['id']) for profile in proposals if isinstance(profile, dict))), 'context_profile': sorted((str(profile['id']) for profile in contexts if isinstance(profile, dict))), 'bridge_type': sorted(_strings(bridge_policy.get('bridge_type_ids'), 'universal effect bridge sources', minimum=1)), 'resource_kind': sorted(_strings(compatibility.get('resource_kind_ids'), 'universal effect resource sources', minimum=1))}
    resource_carriers = semantic_asset.get('resource_carrier_profiles')
    _require(isinstance(resource_carriers, list), 'universal resource carrier profiles are missing')
    resource_carrier_by_kind = {str(profile.get('resource_kind')): profile for profile in resource_carriers if isinstance(profile, dict)}

    def flattened_strings(value: Any) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, Mapping):
            return [text for key, child in value.items() for text in [str(key), *flattened_strings(child)]]
        if isinstance(value, list):
            return [text for child in value for text in flattened_strings(child)]
        return [] if value is None else [str(value)]
    candidate_by_id = {str(candidate['id']): candidate for candidate in candidates if isinstance(candidate, dict) and isinstance(candidate.get('id'), str)}
    proposal_by_id = {str(profile['id']): profile for profile in proposals if isinstance(profile, dict) and isinstance(profile.get('id'), str)}
    context_by_id = {str(profile['id']): profile for profile in contexts if isinstance(profile, dict) and isinstance(profile.get('id'), str)}

    def source_semantic_texts(source_kind: str, source_id: str) -> list[str]:
        if source_kind == 'visual_candidate':
            source = candidate_by_id[source_id]
            return flattened_strings({'definition': source.get('definition'), 'aliases': source.get('aliases'), 'parameters': source.get('parameters'), 'bindings': source.get('bindings'), 'triggers': source.get('triggers'), 'postconditions': source.get('postconditions')})
        if source_kind == 'proposal_profile':
            source = proposal_by_id[source_id]
            return flattened_strings({'value_id': source.get('value_id'), 'prompt_phrase_en': source.get('prompt_phrase_en'), 'event_roles': source.get('event_roles')})
        if source_kind == 'context_profile':
            source = context_by_id[source_id]
            return flattened_strings({'requires_all': source.get('requires_all'), 'requires_any': source.get('requires_any'), 'forbids_any': source.get('forbids_any')})
        if source_kind == 'bridge_type':
            return [source_id]
        if source_kind == 'resource_kind':
            return flattened_strings(resource_carrier_by_kind[source_id])
        raise ValidationFailure(f'unknown universal effect source kind: {source_kind}')
    independently_derived_effects: dict[tuple[str, str], set[str]] = {}
    for kind in UNIVERSAL_EFFECT_SOURCE_KIND_IDS:
        for source_id in expected_by_kind[kind]:
            derived = _classify_universal_contract_effects(source_semantic_texts(kind, source_id), contract_effect_profiles)
            _require(not derived, f'universal safe source meaning activates a blocked semantic effect: {kind}:{source_id}:{sorted(derived)}')
            independently_derived_effects[kind, source_id] = derived
    expected_profiles = [{'source_kind': kind, 'source_id': source_id, 'effect_ids': sorted(independently_derived_effects[kind, source_id])} for kind in UNIVERSAL_EFFECT_SOURCE_KIND_IDS for source_id in expected_by_kind[kind]]
    _require(registry.get('profiles') == expected_profiles, 'universal semantic effect profiles must exactly equal the independently compiled empty safe catalog')
    expected_counts = {kind: len(expected_by_kind[kind]) for kind in UNIVERSAL_EFFECT_SOURCE_KIND_IDS}
    expected_counts['total'] = sum(expected_counts.values())
    _require(registry.get('counts') == expected_counts, 'universal semantic effect registry counts drift')
    return {'schema': registry['schema'], 'profile_count': expected_counts['total'], 'effect_id_count': len(UNIVERSAL_V2_BLOCKED_SEMANTIC_IDS), 'nonempty_effect_profile_count': 0, 'registry_sha256': hashlib.sha256(canonical_json_bytes(registry)).hexdigest()}

def _validate_universal_trace_source_authorities(candidate_asset: Mapping[str, Any], compatibility: Mapping[str, Any], semantic_asset: Mapping[str, Any], candidate_by_id: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """Independently freeze the raw authorities consumed by trace replay."""
    expected_budgets = {'event_spines': 1, 'primary_actions': 1, 'phases': 1, 'pose_support_solutions': 1, 'display_bundles': 1, 'display_primitives_per_bundle': 2, 'perceived_affect_hypotheses': 1, 'gestures': 1, 'optional_props': 1, 'relation_topologies': 1, 'primary_environment_roles': 1, 'remote_or_high_load_optional_premises': 1, 'second_independent_premises': 0, 'orphan_atoms': 0}
    _require(compatibility.get('budgets') == expected_budgets, 'universal trace compatibility budget authority drift')
    _require(compatibility.get('resource_policy') == {'scope': 'entity_or_scene', 'capacity_check': 'sum_exclusive_claims_lte_capacity', 'same_phase_double_booking': 'block', 'shared_attention_exception': 'only_same_visible_target', 'repair_order': ['release_phase', 'environment_support', 'mount_or_sling', 'alternate_capable_effector', 'drop_optional_candidate']}, 'universal trace resource-policy authority drift')
    _require(compatibility.get('decision_reason_code_ids') == UNIVERSAL_DECISION_REASON_CODE_IDS, 'universal trace reason-code authority drift')
    distance_policy = compatibility.get('distance_policy')
    creativity_bands = distance_policy.get('creativity_bands') if isinstance(distance_policy, Mapping) else None
    _require(isinstance(creativity_bands, list) and all((isinstance(band, Mapping) and 'max_optional_remote' not in band for band in creativity_bands)) and ('max_remote_or_high_load_optional_premises' not in distance_policy), 'universal trace source cannot encode creativity-band remote ceilings')
    proposals = candidate_asset.get('proposal_profiles')
    contexts = candidate_asset.get('context_distance_profiles')
    rules = compatibility.get('universal_rules')
    _require(isinstance(proposals, list) and len(proposals) == 12 and isinstance(contexts, list) and (len(contexts) == 18) and isinstance(rules, list) and (len(rules) == 7), 'universal trace policy-source inventory drift')
    policy_source_rows: list[dict[str, Any]] = []
    for prefix, source_kind, stage, rows in (('proposal_policy', 'proposal_policy', 'contract_input', proposals), ('context_policy', 'context_policy', 'contract_input', contexts), ('universal_rule', 'universal_rule', 'postselection', rules)):
        for source in rows:
            _require(isinstance(source, Mapping) and isinstance(source.get('id'), str) and bool(source['id']), 'universal trace policy source lacks a stable ID')
            record_id = f'{prefix}__{source['id']}'
            policy_mode = None if source_kind == 'universal_rule' else source.get('policy_mode')
            declared_outcome = source.get('outcome') if source_kind == 'universal_rule' else None
            _require(source_kind == 'universal_rule' and policy_mode is None and (declared_outcome in {'block', 'repair', 'allow_with_bridge'}) or (source_kind != 'universal_rule' and policy_mode in {'ordinary', 'safe_tool', 'explicit_weapon_only'} and (declared_outcome is None)), f'universal trace policy source domain drift: {record_id}')
            payload = {'schema': 'illustration-universal-scene-policy-source-contract/v1', 'record_id': record_id, 'source_kind': source_kind, 'source_id': source['id'], 'evaluation_stage': stage, 'policy_mode': policy_mode, 'declared_outcome': declared_outcome, 'source_record': copy.deepcopy(source)}
            policy_source_rows.append({'record_id': record_id, 'source_kind': source_kind, 'source_id': source['id'], 'evaluation_stage': stage, 'policy_mode': policy_mode, 'declared_outcome': declared_outcome, 'source_contract_sha256': hashlib.sha256(canonical_json_bytes(payload)).hexdigest()})
    policy_source_rows.sort(key=lambda row: row['record_id'].encode('utf-8'))
    _require(len(policy_source_rows) == len({row['record_id'] for row in policy_source_rows}) == 37, 'universal trace policy-source IDs are incomplete or duplicated')
    guard_profiles = semantic_asset.get('guard_execution_profiles')
    guard_ids = compatibility.get('guard_candidate_ids')
    _require(isinstance(guard_profiles, list) and len(guard_profiles) == 32 and isinstance(guard_ids, list) and (guard_ids == sorted(set(guard_ids))) and ([profile.get('guard_id') for profile in guard_profiles] == guard_ids), 'universal trace guard-source inventory/order drift')
    guard_source_rows: list[dict[str, Any]] = []
    predicate_ids: list[str] = []
    for profile in guard_profiles:
        _require(isinstance(profile, dict) and list(profile) == ['guard_id', 'predicate_id'] and isinstance(profile['predicate_id'], str) and bool(profile['predicate_id']), 'universal trace guard execution profile shape drift')
        guard_id = profile['guard_id']
        predicate_ids.append(profile['predicate_id'])
        candidate = candidate_by_id.get(guard_id)
        _require(isinstance(candidate, Mapping) and candidate.get('role') == 'guard', f'universal trace guard source candidate drift: {guard_id}')
        runtime_contract = candidate.get('runtime_contract')
        _require(isinstance(runtime_contract, Mapping) and set(runtime_contract) == {'stage', 'violation_code', 'when_all', 'require_all', 'outcome'} and (runtime_contract.get('outcome') in {'block', 'repair', 'requires_bridge'}), f'universal trace guard runtime source drift: {guard_id}')
        raw_topics = list(candidate['research_topic_ids'])
        raw_provenance = list(candidate['provenance_record_ids'])
        _require(len(raw_topics) == len(set(raw_topics)) and len(raw_provenance) == len(set(raw_provenance)), f'universal trace guard provenance duplicates: {guard_id}')
        topics = sorted(raw_topics, key=lambda value: value.encode('utf-8'))
        provenance = sorted(raw_provenance, key=lambda value: value.encode('utf-8'))
        source = {'record_id': guard_id, 'source_candidate_id': guard_id, 'predicate_id': profile['predicate_id'], 'role': 'guard', 'evaluation_stage': 'postselection_conditional', 'research_topic_ids': topics, 'provenance_record_ids': provenance, 'stage': runtime_contract['stage'], 'violation_code': runtime_contract['violation_code'], 'when_all': copy.deepcopy(runtime_contract['when_all']), 'require_all': copy.deepcopy(runtime_contract['require_all']), 'declared_outcome': runtime_contract['outcome']}
        guard_source_rows.append({'record_id': guard_id, 'source_candidate_id': guard_id, 'predicate_id': profile['predicate_id'], 'source_contract_sha256': hashlib.sha256(canonical_json_bytes(source)).hexdigest(), **{key: value for key, value in source.items() if key not in {'record_id', 'source_candidate_id', 'predicate_id'}}})
    _require(len(predicate_ids) == len(set(predicate_ids)) == 32, 'universal trace guard predicate inventory is not one-to-one')
    compatibility_budget_scopes = {'display_bundles': ('bundle', 'display'), 'display_primitives_per_bundle': ('bundle', 'display'), 'event_spines': ('scene', 'event_graph'), 'gestures': ('facet', 'gesture'), 'optional_props': ('facet', 'prop'), 'orphan_atoms': ('scene', 'event_graph'), 'perceived_affect_hypotheses': ('facet', 'perceived_affect'), 'phases': ('facet', 'phase'), 'pose_support_solutions': ('facet', 'pose'), 'primary_actions': ('facet', 'action'), 'primary_environment_roles': ('facet', 'environment'), 'relation_topologies': ('facet', 'relation'), 'remote_or_high_load_optional_premises': ('global', 'optional_remote'), 'second_independent_premises': ('global', 'independent_premise')}
    _require(set(compatibility_budget_scopes) == set(expected_budgets), 'universal trace compatibility-budget scope inventory drift')
    cardinality_limits = [{'record_id': f'compatibility_budget__{metric_id}', 'source_kind': 'compatibility_budget', 'metric_id': metric_id, 'evaluation_stage': 'postselection_scene', 'scope_kind': compatibility_budget_scopes[metric_id][0], 'scope_id': compatibility_budget_scopes[metric_id][1], 'minimum': 0, 'maximum': maximum} for metric_id, maximum in expected_budgets.items()]
    runtime_limits = {'context_profile_carriers': ('postselection_scene', 'global', 'context_carrier', 6), 'global_optional_remote': ('postselection_scene', 'global', 'optional_remote', 1), 'literal_realization_atoms_per_facet': ('preselection_reservation', 'each_facet', None, 2), 'literal_realization_atoms_total': ('preselection_reservation', 'global', 'literal_realization', 10), 'selected_resource_claims_total': ('postselection_scene', 'global', 'resource_claim', 32), 'selected_visual_atoms_total': ('postselection_scene', 'global', 'visual_atom', 18)}
    cardinality_limits.extend(({'record_id': f'runtime_limit__{metric_id}', 'source_kind': 'runtime_limit', 'metric_id': metric_id, 'evaluation_stage': specification[0], 'scope_kind': specification[1], 'scope_id': specification[2], 'minimum': 0, 'maximum': specification[3]} for metric_id, specification in runtime_limits.items()))
    cardinality_limits.sort(key=lambda row: row['record_id'].encode('utf-8'))
    cardinality_ids = [row['record_id'] for row in cardinality_limits]
    _require(cardinality_ids == sorted(set(cardinality_ids), key=lambda value: value.encode('utf-8')) and len(cardinality_ids) == 20, 'universal trace cardinality-limit inventory drift')
    return {'policy_source_contract_count': len(policy_source_rows), 'policy_source_contracts_sha256': hashlib.sha256(canonical_json_bytes(policy_source_rows)).hexdigest(), 'guard_source_contract_count': len(guard_source_rows), 'guard_source_contracts_sha256': hashlib.sha256(canonical_json_bytes(guard_source_rows)).hexdigest(), 'cardinality_limit_count': len(cardinality_ids), 'cardinality_limits_sha256': hashlib.sha256(canonical_json_bytes(cardinality_limits)).hexdigest(), 'cardinality_limit_ids_sha256': hashlib.sha256(canonical_json_bytes(cardinality_ids)).hexdigest()}

def validate_universal_scene_runtime_assets(asset_dir: Path, research: Mapping[str, Any]) -> dict[str, Any]:
    """Validate executable universal candidates, predicates, and cross-file refs."""
    candidate_path = asset_dir / 'illustration_universal_scene_candidates_v1.json'
    compatibility_path = asset_dir / 'illustration_universal_compatibility_graph_v1.json'
    semantic_path = asset_dir / 'illustration_universal_semantic_bindings_v1.json'
    _require(candidate_path.is_file(), 'missing universal scene candidate asset')
    _require(compatibility_path.is_file(), 'missing universal compatibility asset')
    _require(semantic_path.is_file(), 'missing universal semantic-binding asset')
    _require(candidate_path.stat().st_size <= 512 * 1024, 'universal candidate asset exceeds the 512 KiB unsharded limit')
    candidate_asset = _load_json(candidate_path)
    compatibility = _load_json(compatibility_path)
    semantic_asset = _load_json(semantic_path)
    semantic_effect_policy = _validate_universal_semantic_effect_policy(candidate_asset, compatibility, semantic_asset)
    candidate_top_keys = {'schema', 'reviewed_at', 'normalization', 'candidate_role_ids', 'facet_ids', 'distance_axis_ids', 'load_axis_ids', 'research_packets', 'research_manifest_sha256', 'selection_contract', 'no_prop_path', 'nonhuman_path', 'context_distance_profiles', 'proposal_profiles', 'topic_contributions', 'candidates', 'prop_concepts', 'embodiment_profiles', 'counts', 'semantic_bindings_asset_sha256'}
    _require(isinstance(candidate_asset, dict) and set(candidate_asset) == candidate_top_keys, 'universal candidate top-level fields mismatch')
    _require(candidate_asset.get('schema') == 'subculture-illustration-universal-scene-candidates/v1', 'universal candidate schema mismatch')
    _require(candidate_asset.get('reviewed_at') == '2026-08-10', 'universal candidate review date drift')
    _require(candidate_asset.get('normalization') == 'NFKC+casefold+whitespace-collapse', 'universal candidate normalization drift')
    _require(candidate_asset.get('candidate_role_ids') == ['visual_atom', 'router', 'guard', 'metric'], 'universal candidate role order mismatch')
    facet_ids = _strings(candidate_asset.get('facet_ids'), 'universal facet IDs', minimum=1)
    _require(candidate_asset.get('distance_axis_ids') == UNIVERSAL_DISTANCE_AXIS_IDS, 'universal distance axes mismatch')
    _require(candidate_asset.get('load_axis_ids') == UNIVERSAL_LOAD_AXIS_IDS, 'universal load axes mismatch')
    _require(candidate_asset.get('research_manifest_sha256') == research['manifest_sha256'], 'universal candidate research-manifest hash mismatch')
    research_packets = candidate_asset.get('research_packets')
    _require(isinstance(research_packets, list) and len(research_packets) == 6, 'universal candidate research packet list mismatch')
    expected_packet_core = [{'path': shard['path'], 'sha256': shard['sha256'], 'record_count': shard['record_count']} for shard in research['shards']]
    _require([{key: packet.get(key) for key in ('path', 'sha256', 'record_count')} for packet in research_packets if isinstance(packet, dict)] == expected_packet_core, 'universal candidate research packets do not exactly match the manifest shards')
    _require(all((isinstance(packet, dict) and set(packet) == {'path', 'sha256', 'record_count', 'topic_ids'} for packet in research_packets)) and len([topic for packet in research_packets for topic in packet['topic_ids']]) == 20 and (set((topic for packet in research_packets for topic in packet['topic_ids'])) == set(candidate_asset.get('topic_contributions', {}))), 'universal candidate research packet topic partition mismatch')
    selection_contract = candidate_asset.get('selection_contract')
    _require(isinstance(selection_contract, dict), 'universal candidate selection contract missing')
    for field in ('research_candidates_are_not_prompt_tags', 'research_topic_ids_are_provenance_only', 'visual_atoms_require_event_spine_binding'):
        _require(selection_contract.get(field) is True, f'universal selection contract requires {field}=true')
    _require(selection_contract.get('router_guard_metric_prompt_emission') == 'forbidden', 'nonvisual prompt emission must be forbidden')
    _require(selection_contract.get('unknown_fixed_props') == 'preserve_as_opaque_and_do_not_invent_affordances', 'unknown fixed-prop boundary drift')
    candidates = candidate_asset.get('candidates')
    _require(isinstance(candidates, list) and candidates, 'universal executable candidates missing')
    candidate_ids = [item.get('id') for item in candidates if isinstance(item, dict)]
    _require(len(candidate_ids) == len(candidates) == len(set(candidate_ids)), 'universal executable candidate IDs must be unique')
    _require(candidate_ids == sorted(candidate_ids), 'universal executable candidates must use canonical ID order')
    candidate_by_id = {item['id']: item for item in candidates}
    common_keys = {'id', 'role', 'facet', 'layer', 'definition', 'research_topic_ids', 'provenance_record_ids', 'direct_source_record_ids', 'aliases', 'triggers', 'bindings', 'parameters', 'preconditions', 'postconditions', 'capabilities', 'resource_claims', 'semantic_distance', 'semantic_load', 'salience', 'render_risk', 'pixel_evidence', 'runtime_contract', 'annotation_provenance'}
    role_counts: Counter[str] = Counter()
    pixel_ids: list[str] = []
    topic_contributors: dict[str, set[str]] = defaultdict(set)
    graph_predicate_kinds = set(_strings(compatibility.get('predicate_kind_ids'), 'universal predicate kinds', minimum=1))
    graph_resource_kind_values = _strings(compatibility.get('resource_kind_ids'), 'universal resource kinds', minimum=1)
    _require(graph_resource_kind_values == UNIVERSAL_V2_RESOURCE_KINDS and len(graph_resource_kind_values) == len(set(graph_resource_kind_values)) == 24, 'universal compatibility resource kinds must exactly equal the unique closed 24-kind domain')
    graph_resource_kinds = set(graph_resource_kind_values)
    composition_targets = _load_json(asset_dir / 'universal_composition_targets_v1.json')
    composition_literal_carrier_policy = _validate_universal_composition_literal_carriers(semantic_asset, composition_targets)
    literal_realization_policy = _validate_universal_literal_realization_profiles(semantic_asset, candidate_by_id, graph_resource_kind_values)
    for candidate in candidates:
        _require(isinstance(candidate, dict) and set(candidate) == common_keys, f'universal candidate field mismatch: {(candidate.get('id') if isinstance(candidate, dict) else '<invalid>')}')
        candidate_id = candidate['id']
        _require(not {'topic_id', 'route_id', 'bundle_id'} & set(candidate), f'{candidate_id} owns a route/topic/bundle')
        role = candidate.get('role')
        spec = research['candidate_specs'].get(candidate_id)
        if isinstance(spec, dict):
            _require(role == spec['role'] and role in UNIVERSAL_CANDIDATE_ROLE_VALUES, f'{candidate_id} research role mismatch')
            _require(candidate.get('definition') == spec['definition'], f'{candidate_id} research definition drift')
        else:
            _require(candidate_id in UNIVERSAL_V2_DERIVED_CANDIDATE_IDS and role == 'visual_atom' and (candidate.get('annotation_provenance') == {'definition': 'design_inference_from_reviewed_research', 'pixel_evidence': 'design_inference_from_reviewed_research', 'runtime_fields': 'design_inference'}) and isinstance(candidate.get('definition'), str) and bool(candidate['definition'].strip()), f'{candidate_id} is not an approved research-derived candidate')
        _require(candidate.get('facet') in facet_ids, f'{candidate_id} facet mismatch')
        topics = _strings(candidate.get('research_topic_ids'), f'{candidate_id}.research_topic_ids', minimum=1)
        if isinstance(spec, dict):
            _require(set(topics) == {spec['topic_id']}, f'{candidate_id} research topic mismatch')
        else:
            _require(set(topics) <= set(research['topic_ids']), f'{candidate_id} derived topic reference mismatch')
        provenance = _strings(candidate.get('provenance_record_ids'), f'{candidate_id}.provenance_record_ids', minimum=1)
        _require(set(provenance) <= (spec['record_ids'] if isinstance(spec, dict) else set(research['record_ids'])), f'{candidate_id} has unreviewed provenance')
        _require(candidate.get('direct_source_record_ids') == [], f'{candidate_id} overclaims direct source validation')
        aliases = candidate.get('aliases')
        _require(isinstance(aliases, list), f'{candidate_id}.aliases must be a list')
        for alias in aliases:
            if isinstance(alias, str):
                _require(alias.strip(), f'{candidate_id} has an empty alias')
            else:
                _require(isinstance(alias, dict) and set(alias) == {'locale', 'values'} and (alias.get('locale') in {'en', 'ko', 'ja', 'zh'}), f'{candidate_id} localized alias shape mismatch')
                _strings(alias.get('values'), f'{candidate_id}.{alias['locale']}.aliases', minimum=1)
        parameters = candidate.get('parameters')
        _require(isinstance(parameters, dict), f'{candidate_id}.parameters must be an object')
        for parameter, values in parameters.items():
            _require(isinstance(parameter, str) and parameter and isinstance(values, list), f'{candidate_id} parameter enum mismatch')
        preconditions = candidate.get('preconditions')
        capabilities = candidate.get('capabilities')
        _require(isinstance(preconditions, dict) and set(preconditions) == {'requires_all', 'requires_any', 'forbids_any'}, f'{candidate_id} preconditions shape mismatch')
        _require(isinstance(capabilities, dict) and set(capabilities) == {'requires_all', 'requires_any'}, f'{candidate_id} capabilities shape mismatch')
        for field in ('triggers', 'postconditions'):
            _predicate_groups(candidate.get(field), f'{candidate_id}.{field}', graph_predicate_kinds)
        for field in ('requires_all', 'requires_any', 'forbids_any'):
            _predicate_groups(preconditions[field], f'{candidate_id}.preconditions.{field}', graph_predicate_kinds)
        for field in ('requires_all', 'requires_any'):
            _predicate_groups(capabilities[field], f'{candidate_id}.capabilities.{field}', graph_predicate_kinds)
        bindings = candidate.get('bindings')
        _require(isinstance(bindings, list), f'{candidate_id}.bindings must be a list')
        for binding in bindings:
            _require(isinstance(binding, list) and len(binding) == 2 and all((isinstance(value, str) and value for value in binding)), f'{candidate_id} binding shape mismatch')
        resource_claims = candidate.get('resource_claims')
        _require(isinstance(resource_claims, list), f'{candidate_id}.resource_claims must be a list')
        for claim in resource_claims:
            _require(isinstance(claim, list) and len(claim) == 4 and (claim[0] in graph_resource_kinds) and isinstance(claim[1], str) and isinstance(claim[2], int) and (not isinstance(claim[2], bool)) and (claim[2] >= 1) and (claim[3] in {'exclusive', 'shared'}), f'{candidate_id} resource claim mismatch')
        semantic_distance = candidate.get('semantic_distance')
        _require(isinstance(semantic_distance, dict) and set(semantic_distance) == {'base', 'adjustments'}, f'{candidate_id} distance shape mismatch')
        _zero_vector(semantic_distance['base'], UNIVERSAL_DISTANCE_AXIS_IDS, f'{candidate_id}.semantic_distance.base')
        _zero_vector(candidate.get('semantic_load'), UNIVERSAL_LOAD_AXIS_IDS, f'{candidate_id}.semantic_load')
        _require(isinstance(candidate.get('salience'), dict) and set(candidate['salience']) == {'role', 'displacement_cap'}, f'{candidate_id} salience shape mismatch')
        _require(isinstance(candidate.get('render_risk'), dict) and set(candidate['render_risk']) == {'band', 'tags'}, f'{candidate_id} render-risk shape mismatch')
        pixel_evidence = candidate.get('pixel_evidence')
        _require(isinstance(pixel_evidence, list), f'{candidate_id}.pixel_evidence must be a list')
        runtime_contract = candidate.get('runtime_contract')
        _require(isinstance(runtime_contract, dict), f'{candidate_id}.runtime_contract missing')
        if role == 'visual_atom':
            _require(pixel_evidence, f'{candidate_id} visual atom has no pixel obligation')
            expected_runtime_keys = {'bindings', 'requires_all', 'requires_any', 'forbids_any', 'provides', 'resource_claims', 'distance_profile', 'load_profile', 'bridge_types', 'salience', 'render_risk', 'pixel_evidence'}
            _require(set(runtime_contract) == expected_runtime_keys, f'{candidate_id} visual runtime contract mismatch')
            _require(runtime_contract['bindings'] == bindings, f'{candidate_id} runtime bindings drift')
            _require(runtime_contract['requires_all'] == preconditions['requires_all'], f'{candidate_id} runtime requires_all drift')
            _require(runtime_contract['requires_any'] == preconditions['requires_any'], f'{candidate_id} runtime requires_any drift')
            _require(runtime_contract['forbids_any'] == preconditions['forbids_any'], f'{candidate_id} runtime forbids_any drift')
            _require(runtime_contract['provides'] == candidate['postconditions'], f'{candidate_id} runtime provides drift')
            _require(runtime_contract['resource_claims'] == resource_claims, f'{candidate_id} runtime resource claims drift')
            _require(runtime_contract['distance_profile'] == semantic_distance, f'{candidate_id} runtime distance drift')
            _require(runtime_contract['load_profile'] == candidate['semantic_load'], f'{candidate_id} runtime load drift')
            _require(runtime_contract['pixel_evidence'] == pixel_evidence, f'{candidate_id} runtime pixel evidence drift')
            runtime_bridge_types = _strings(runtime_contract['bridge_types'], f'{candidate_id}.runtime_contract.bridge_types')
            _require(len(runtime_bridge_types) == len(set(runtime_bridge_types)) and set(runtime_bridge_types) <= set(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS), f'{candidate_id} runtime bridge types escape the closed seven-type enum')
            for field in ('requires_all', 'requires_any', 'forbids_any', 'provides'):
                _predicate_groups(runtime_contract[field], f'{candidate_id}.runtime_contract.{field}', graph_predicate_kinds)
            for index, adjustment in enumerate(runtime_contract['distance_profile']['adjustments']):
                _require(isinstance(adjustment, dict) and set(adjustment) == {'when_all', 'operation'}, f'{candidate_id} distance adjustment shape mismatch')
                _predicate_groups(adjustment['when_all'], f'{candidate_id}.distance_adjustment[{index}]', graph_predicate_kinds)
        elif role == 'router':
            _require(pixel_evidence == [] and resource_claims == [], f'{candidate_id} nonvisual router exposes visual evidence/resources')
            _require(set(runtime_contract) == {'stage', 'opens_facets', 'requires_all', 'forbids_any', 'deterministic_order'}, f'{candidate_id} router runtime contract mismatch')
            _require(set(_strings(runtime_contract['opens_facets'], f'{candidate_id}.opens_facets', minimum=1)) <= set(facet_ids), f'{candidate_id} opens unknown facet')
            for field in ('requires_all', 'forbids_any'):
                _predicate_groups(runtime_contract[field], f'{candidate_id}.runtime_contract.{field}', graph_predicate_kinds)
        elif role == 'guard':
            _require(pixel_evidence == [] and resource_claims == [], f'{candidate_id} nonvisual guard exposes visual evidence/resources')
            _require(set(runtime_contract) == {'stage', 'violation_code', 'when_all', 'require_all', 'outcome'}, f'{candidate_id} guard runtime contract mismatch')
            _require(runtime_contract.get('outcome') in {'block', 'repair', 'requires_bridge'}, f'{candidate_id} guard outcome mismatch')
            for field in ('when_all', 'require_all'):
                _predicate_groups(runtime_contract[field], f'{candidate_id}.runtime_contract.{field}', graph_predicate_kinds)
        else:
            _require(pixel_evidence == [] and resource_claims == [], f'{candidate_id} nonvisual metric exposes visual evidence/resources')
            _require(set(runtime_contract) == {'stage', 'value_type', 'input_ids', 'output_axis'}, f'{candidate_id} metric runtime contract mismatch')
            _require(runtime_contract.get('value_type') in {'ordinal_0_3', 'count', 'boolean', 'band'}, f'{candidate_id} metric type mismatch')
            _strings(runtime_contract.get('input_ids'), f'{candidate_id}.input_ids', minimum=1)
        for pixel in pixel_evidence:
            _require(isinstance(pixel, dict) and set(pixel) == {'id', 'kind', 'definition', 'minimum_scale_ids'} and isinstance(pixel.get('id'), str) and isinstance(pixel.get('definition'), str) and pixel['definition'].strip(), f'{candidate_id} pixel evidence shape mismatch')
            _require(pixel.get('kind') in {'contact', 'orientation', 'state_boundary', 'support', 'path', 'residue', 'display'}, f'{candidate_id} pixel evidence kind mismatch')
            _require(set(_strings(pixel.get('minimum_scale_ids'), f'{candidate_id}.{pixel['id']}.minimum_scale_ids', minimum=1)) <= {'native', 'thumbnail_320px'}, f'{candidate_id} pixel scale mismatch')
            pixel_ids.append(pixel['id'])
        role_counts[role] += 1
        for topic_id in topics:
            topic_contributors[topic_id].add(candidate_id)
    _require({candidate_id for candidate_id in candidate_ids if candidate_id not in research['candidate_specs']} == UNIVERSAL_V2_DERIVED_CANDIDATE_IDS, 'universal research-derived candidate inventory drift')
    _require(len(pixel_ids) == len(set(pixel_ids)), 'universal executable pixel evidence IDs must be unique')
    _require(len(candidates) == 127 and dict(role_counts) == {'visual_atom': 65, 'router': 21, 'guard': 32, 'metric': 9} and (len(pixel_ids) == 76), 'universal executable candidate/role/pixel inventory drift')
    fixed_prop_eligibility_policy = _validate_universal_fixed_prop_eligibility_source_contract(candidate_by_id)
    pixel_owner_by_id = {pixel['id']: candidate['id'] for candidate in candidates for pixel in candidate['pixel_evidence']}
    proposal_profiles = candidate_asset.get('proposal_profiles')
    _require(isinstance(proposal_profiles, list) and len(proposal_profiles) == 12, 'universal proposal-profile inventory mismatch')
    proposal_keys = {'id', 'semantic_family_id', 'semantic_family_payload', 'semantic_family_signature', 'candidate_ids', 'slot_id', 'eligible_slot_states', 'value_id', 'prompt_phrase_en', 'carrier_lexeme_groups', 'requires_all', 'forbids_any', 'event_roles', 'distance_profile', 'load_profile', 'bridge_types', 'pixel_evidence_ids', 'remote_or_high_load', 'policy_mode'}
    compatibility_bridge_policy = compatibility.get('bridge_policy')
    _require(isinstance(compatibility_bridge_policy, dict), 'universal compatibility bridge policy missing')
    allowed_bridge_types = set(_strings(compatibility_bridge_policy.get('bridge_type_ids'), 'universal bridge types', minimum=1))
    bridge_categories = compatibility_bridge_policy.get('category_members')
    _require(isinstance(bridge_categories, dict) and set(bridge_categories) == {'entry', 'mediation', 'exit'}, 'universal bridge categories mismatch')
    category_members = {category: set(_strings(values, f'universal bridge category {category}', minimum=1)) for category, values in bridge_categories.items()}
    proposal_ids: set[str] = set()
    semantic_family_ids: set[str] = set()
    semantic_family_signatures: set[str] = set()
    proposal_band_counts: Counter[str] = Counter()
    raw_prop_concepts = candidate_asset.get('prop_concepts')
    _require(isinstance(raw_prop_concepts, list), 'universal prop catalog must be an array')
    proposal_prop_concept_ids = {str(prop['id']) for prop in raw_prop_concepts if isinstance(prop, dict) and isinstance(prop.get('id'), str)}
    for profile in proposal_profiles:
        profile_id = profile.get('id') if isinstance(profile, dict) else '<invalid>'
        _require(isinstance(profile, dict) and set(profile) == proposal_keys, f'universal proposal profile shape mismatch: {profile_id}')
        family_id = profile.get('semantic_family_id')
        family_signature = profile.get('semantic_family_signature')
        _require(isinstance(profile_id, str) and profile_id and (profile_id not in proposal_ids) and isinstance(family_id, str) and family_id and (family_id not in semantic_family_ids) and isinstance(family_signature, str) and (re.fullmatch('[0-9a-f]{64}', family_signature) is not None) and (family_signature not in semantic_family_signatures), 'universal proposal semantic family IDs/signatures must be unique')
        proposal_ids.add(profile_id)
        semantic_family_ids.add(family_id)
        semantic_family_signatures.add(family_signature)
        _require(profile.get('slot_id') == 'prop' and profile.get('eligible_slot_states') == ['open'], f'{profile_id} must remain an open-prop proposal')
        value_id = profile.get('value_id')
        expected_policy = {'prop_apple': 'ordinary', 'prop_hammer': 'safe_tool'}.get(value_id)
        _require(expected_policy is not None, f'{profile_id} open proposal uses an unreviewed prop')
        _require(profile.get('policy_mode') == expected_policy, f'{profile_id} value/policy contract drift')
        prompt_phrase = profile.get('prompt_phrase_en')
        _require(isinstance(prompt_phrase, str) and prompt_phrase.strip() == prompt_phrase and (1 <= len(prompt_phrase.split()) <= 80), f'{profile_id} prompt phrase mismatch')
        carrier_groups = profile.get('carrier_lexeme_groups')
        _require(isinstance(carrier_groups, list) and 1 <= len(carrier_groups) <= 2 and all((isinstance(group, list) and group and (len(group) == len(set(group))) and all((isinstance(alternative, str) and alternative == ' '.join(alternative.casefold().split()) and (re.fullmatch('[a-z0-9 ]+', alternative) is not None) for alternative in group)) for group in carrier_groups)), f'{profile_id} carrier lexeme groups are not closed natural English')
        requires_all = _predicate_groups(profile.get('requires_all'), f'{profile_id}.requires_all', graph_predicate_kinds)
        forbids_any = _predicate_groups(profile.get('forbids_any'), f'{profile_id}.forbids_any', graph_predicate_kinds)
        eligibility_tokens = {token.casefold().replace('-', '_') for predicate in requires_all + forbids_any for token in predicate}
        _require(not any((marker in token for token in eligibility_tokens for marker in ('creativ', 'seed', 'target_band', 'selected_band', 'semantic_distance'))), f'{profile_id} eligibility improperly depends on creativity or tie-break state')
        proposal_candidate_ids = _strings(profile.get('candidate_ids'), f'{profile_id}.candidate_ids', minimum=1)
        _require(len(proposal_candidate_ids) == len(set(proposal_candidate_ids)) and set(proposal_candidate_ids) <= set(candidate_ids) and all((candidate_by_id[candidate_id]['role'] == 'visual_atom' for candidate_id in proposal_candidate_ids)), f'{profile_id} candidate refs must be unique visual atoms')
        proposal_pixel_ids = _strings(profile.get('pixel_evidence_ids'), f'{profile_id}.pixel_evidence_ids', minimum=1)
        expected_pixel_ids = [pixel['id'] for candidate_id in proposal_candidate_ids for pixel in candidate_by_id[candidate_id]['pixel_evidence']]
        _require(proposal_pixel_ids == expected_pixel_ids and all((pixel_owner_by_id[pixel_id] in proposal_candidate_ids for pixel_id in proposal_pixel_ids)), f'{profile_id} pixel-evidence refs do not exactly cover its atoms')
        event_roles = profile.get('event_roles')
        _require(isinstance(event_roles, dict) and list(event_roles) == UNIVERSAL_EVENT_ROLE_IDS and all((value is None or (isinstance(value, str) and value) for value in event_roles.values())) and (event_roles['actor'] == '$identity_actor') and (event_roles['location'] == '$scene_location') and all((isinstance(event_roles[role_id], str) and event_roles[role_id] for role_id in ('action', 'target', 'result', 'phase'))), f'{profile_id} must provide the exact eight-role event frame')
        _require(_normalize_universal_semantic_family_value(profile['slot_id']) != 'null' and _normalize_universal_semantic_family_value(value_id) != 'null' and all((role_value is None or _normalize_universal_semantic_family_value(role_value) != 'null' for role_value in event_roles.values())), f'{profile_id} collides with the reserved null semantic-family sentinel')
        distance_vector = _zero_vector(profile.get('distance_profile'), UNIVERSAL_DISTANCE_AXIS_IDS, f'{profile_id}.distance_profile')
        _zero_vector(profile.get('load_profile'), UNIVERSAL_LOAD_AXIS_IDS, f'{profile_id}.load_profile')
        expected_band = _universal_distance_band(distance_vector)
        proposal_band_counts[expected_band] += 1
        _require(profile.get('remote_or_high_load') is (expected_band == 'far'), f'{profile_id} remote/high-load declaration disagrees with its recomputed band')
        family_payload = _universal_semantic_family_payload(profile, candidate_by_id, proposal_prop_concept_ids)
        _require(profile.get('semantic_family_payload') == family_payload and family_signature == hashlib.sha256(canonical_json_bytes(family_payload)).hexdigest(), f'{profile_id} semantic family signature is not independently reproducible')
        if profile_id == 'proposal_open_near_apple_inspection':
            _require(family_signature == '89805a24fc91b414199c257ca9c1420aae18868f0faf1f2960bfcdf31cb8cc0d', 'universal canonical apple semantic family positive control drift')
        profile_bridge_types = _strings(profile.get('bridge_types'), f'{profile_id}.bridge_types', minimum=1)
        _require(len(profile_bridge_types) == len(set(profile_bridge_types)) and set(profile_bridge_types) <= allowed_bridge_types, f'{profile_id} bridge types are invalid or duplicated')
        bridge_candidate_types = {bridge_type for candidate_id in proposal_candidate_ids if candidate_by_id[candidate_id]['facet'] == 'bridge' for bridge_type in candidate_by_id[candidate_id]['runtime_contract']['bridge_types']}
        _require(set(profile_bridge_types) == bridge_candidate_types, f'{profile_id} bridge list does not match its bridge atoms')
        required_categories = {'near': ('entry',), 'middle': ('entry', 'exit'), 'far': ('entry', 'mediation', 'exit')}[expected_band]
        _require(all((set(profile_bridge_types) & category_members[category] for category in required_categories)), f'{profile_id} lacks required {expected_band} bridge categories')
        if expected_band == 'far':
            _require('usl_core_identity_anchor' in proposal_candidate_ids, f'{profile_id} far proposal lacks a visible core identity anchor')
    _require(proposal_band_counts == Counter({'near': 4, 'middle': 4, 'far': 4}), 'universal proposals must retain four distinct semantic families per distance band')
    context_profiles = candidate_asset.get('context_distance_profiles')
    _require(isinstance(context_profiles, list) and len(context_profiles) == 18 and (len({profile.get('id') for profile in context_profiles if isinstance(profile, dict)}) == 18), 'universal context-distance profile inventory/order drift')
    _require(sum((isinstance(profile, Mapping) and profile.get('id') == 'context_quiet_theme_guard_middle' for profile in context_profiles)) == 1, 'universal quiet-theme source profile must exist exactly once')
    context_profile_keys = {'id', 'carrier_candidate_id', 'candidate_ids', 'requires_all', 'requires_any', 'forbids_any', 'distance_profile', 'load_profile', 'bridge_types', 'pixel_evidence_ids', 'policy_mode'}
    context_band_counts: Counter[str] = Counter()
    for profile in context_profiles:
        profile_id = profile.get('id') if isinstance(profile, dict) else '<invalid>'
        _require(isinstance(profile, dict) and set(profile) == context_profile_keys, f'universal context-distance profile shape mismatch: {profile_id}')
        _require(profile.get('policy_mode') in {'ordinary', 'safe_tool', 'explicit_weapon_only'}, f'{profile_id} context policy mode mismatch')
        predicates: list[list[str]] = []
        for field in ('requires_all', 'requires_any', 'forbids_any'):
            predicates.extend(_predicate_groups(profile.get(field), f'{profile_id}.{field}', graph_predicate_kinds))
        eligibility_tokens = {token.casefold().replace('-', '_') for predicate in predicates for token in predicate}
        _require(not any((marker in token for token in eligibility_tokens for marker in ('creativ', 'seed', 'target_band', 'selected_band', 'semantic_distance', 'case_id', 'request_text', 'request_phrase', 'regex'))) and (not re.search('universal_scene_[0-9]+', json.dumps(profile, ensure_ascii=False).casefold())), f'{profile_id} eligibility depends on creativity, seed, or a frozen holdout literal')
        carrier_ids = _strings(profile.get('candidate_ids'), f'{profile_id}.candidate_ids', minimum=1)
        _require(len(carrier_ids) == len(set(carrier_ids)) and set(carrier_ids) <= set(candidate_ids) and all((candidate_by_id[candidate_id]['role'] == 'visual_atom' for candidate_id in carrier_ids)), f'{profile_id} carriers must be unique visual candidates')
        _require(profile.get('carrier_candidate_id') in carrier_ids and profile.get('carrier_candidate_id') != 'usl_core_identity_anchor', f'{profile_id} must name one selected non-core overlay carrier')
        context_pixel_ids = _strings(profile.get('pixel_evidence_ids'), f'{profile_id}.pixel_evidence_ids', minimum=1)
        expected_context_pixel_ids = [pixel['id'] for candidate_id in carrier_ids for pixel in candidate_by_id[candidate_id]['pixel_evidence']]
        _require(context_pixel_ids == expected_context_pixel_ids and all((pixel_owner_by_id[pixel_id] in carrier_ids for pixel_id in context_pixel_ids)), f'{profile_id} pixel evidence does not exactly cover its carriers')
        distance_vector = _zero_vector(profile.get('distance_profile'), UNIVERSAL_DISTANCE_AXIS_IDS, f'{profile_id}.distance_profile')
        _zero_vector(profile.get('load_profile'), UNIVERSAL_LOAD_AXIS_IDS, f'{profile_id}.load_profile')
        if profile_id == 'context_quiet_theme_guard_middle':
            _validate_universal_quiet_theme_source_contract(profile, candidate_by_id)
        band = _universal_distance_band(distance_vector)
        context_band_counts[band] += 1
        profile_bridge_types = _strings(profile.get('bridge_types'), f'{profile_id}.bridge_types', minimum=1)
        minimum_bridge_count = {'near': compatibility_bridge_policy.get('near_minimum'), 'middle': compatibility_bridge_policy.get('middle_minimum'), 'far': compatibility_bridge_policy.get('far_minimum')}[band]
        _require(isinstance(minimum_bridge_count, int) and len(profile_bridge_types) >= minimum_bridge_count and (len(profile_bridge_types) == len(set(profile_bridge_types))) and (set(profile_bridge_types) <= allowed_bridge_types), f'{profile_id} bridge count/types do not satisfy its recomputed band')
        required_categories = {'near': ('entry',), 'middle': ('entry', 'exit'), 'far': ('entry', 'mediation', 'exit')}[band]
        _require(all((set(profile_bridge_types) & category_members[category] for category in required_categories)), f'{profile_id} lacks required {band} bridge categories')
        if band == 'far':
            _require('usl_core_identity_anchor' in carrier_ids, f'{profile_id} far context profile lacks the global core anchor')
    _require(context_band_counts == Counter({'near': 7, 'middle': 9, 'far': 2}), 'universal context-distance near/middle/far inventory drift')
    contributions = candidate_asset.get('topic_contributions')
    _require(isinstance(contributions, dict) and set(contributions) == set(research['topic_ids']), 'universal topic contributions must cover all 20 topics')
    for topic_id, ids in contributions.items():
        values = _strings(ids, f'topic_contributions.{topic_id}', minimum=1)
        _require(set(values) <= set(candidate_ids), f'{topic_id} contribution references unknown candidate')
        _require(all((topic_id in candidate_by_id[value]['research_topic_ids'] for value in values)), f'{topic_id} contribution has cross-topic candidate')
        _require(set(values) == topic_contributors[topic_id], f'{topic_id} contribution list is incomplete')
    no_prop = candidate_asset.get('no_prop_path')
    _require(isinstance(no_prop, dict), 'universal no-prop path missing')
    _require(no_prop.get('activation_predicate') == ['slot', 'prop', 'closed'], 'universal no-prop activation drift')
    _require(set(_strings(no_prop.get('blocked_facets'), 'no_prop_path.blocked_facets', minimum=2)) == {'prop', 'prop_state'}, 'universal no-prop blocked facets mismatch')
    _require(set(_strings(no_prop.get('closed_event_roles'), 'no_prop_path.closed_event_roles', minimum=1)) == {'instrument'}, 'universal no-prop event role mismatch')
    _require(set(_strings(no_prop.get('allowed_realization_candidate_ids'), 'no_prop_path.allowed_realization_candidate_ids', minimum=1)) <= set(candidate_ids), 'universal no-prop path has unknown candidate')
    nonhuman = candidate_asset.get('nonhuman_path')
    _require(isinstance(nonhuman, dict) and nonhuman.get('human_channel_fabrication') == 'forbidden', 'universal nonhuman boundary mismatch')
    for field in ('capability_router_candidate_id', 'substitution_router_candidate_id'):
        _require(nonhuman.get(field) in candidate_by_id and candidate_by_id[nonhuman[field]]['role'] == 'router', f'universal nonhuman {field} mismatch')
    _require(set(_strings(nonhuman.get('available_channel_candidate_ids'), 'nonhuman_path.available_channel_candidate_ids', minimum=1)) <= set(candidate_ids), 'universal nonhuman channel candidate mismatch')
    props = candidate_asset.get('prop_concepts')
    _require(isinstance(props, list) and len(props) == 4, 'universal prop catalog must contain four concepts')
    prop_ids = [prop.get('id') for prop in props if isinstance(prop, dict)]
    _require(prop_ids == ['prop_apple', 'prop_wooden_mallet', 'prop_hammer', 'prop_decommissioned_machine_gun'], 'universal prop catalog order/IDs mismatch')
    previous_load: tuple[int, int, int] | None = None
    for prop in props:
        _require(set(prop) == {'id', 'aliases', 'hypernym_ids', 'part_ids', 'material_ids', 'affordance_candidate_ids', 'state_ids', 'base_distance_profile', 'base_load_profile', 'risk_tags', 'provenance_record_ids'}, f'{prop.get('id')} prop shape mismatch')
        aliases = prop.get('aliases')
        _require(isinstance(aliases, list) and [item.get('locale') for item in aliases if isinstance(item, dict)] == ['en', 'ko', 'ja', 'zh'], f'{prop['id']} locale aliases mismatch')
        for alias in aliases:
            _require(isinstance(alias, dict) and set(alias) == {'locale', 'values'}, f'{prop['id']} alias shape mismatch')
            _strings(alias.get('values'), f'{prop['id']}.{alias['locale']}.aliases', minimum=1)
        _require(set(_strings(prop.get('affordance_candidate_ids'), f'{prop['id']}.affordance_candidate_ids', minimum=1)) <= set(candidate_ids), f'{prop['id']} affordance reference mismatch')
        _require(set(_strings(prop.get('state_ids'), f'{prop['id']}.state_ids', minimum=1)) <= set(candidate_ids), f'{prop['id']} state reference mismatch')
        _require(set(_strings(prop.get('provenance_record_ids'), f'{prop['id']}.provenance_record_ids', minimum=1)) <= research['record_ids'], f'{prop['id']} provenance reference mismatch')
        _zero_vector(prop.get('base_distance_profile'), UNIVERSAL_DISTANCE_AXIS_IDS, f'{prop['id']}.base_distance_profile')
        load = _zero_vector(prop.get('base_load_profile'), UNIVERSAL_LOAD_AXIS_IDS, f'{prop['id']}.base_load_profile')
        current_load = (load['physical'], load['violence'], load['visual_salience'])
        if previous_load is not None:
            _require(sum(current_load) > sum(previous_load), 'apple/mallet/hammer/machine-gun aggregate load must strictly increase')
        previous_load = current_load
    machine_gun = props[-1]
    machine_gun_candidate_ids = {*machine_gun['affordance_candidate_ids'], *machine_gun['state_ids'], 'uao_global_prop_decommissioned_machine_gun'}
    for profile in proposal_profiles:
        serialized_profile = json.dumps(profile, ensure_ascii=False).casefold()
        _require(not set(profile['candidate_ids']) & machine_gun_candidate_ids and 'machine_gun' not in serialized_profile and ('machine gun' not in serialized_profile), f'{profile['id']} must not activate a weapon through an open-slot proposal')
    embodiments = candidate_asset.get('embodiment_profiles')
    _require(isinstance(embodiments, list) and embodiments, 'universal embodiment profiles missing')
    embodiment_by_id: dict[str, dict[str, int]] = {}
    for profile in embodiments:
        _require(isinstance(profile, dict) and set(profile) == {'id', 'capability_capacities', 'unavailable_channels', 'support_types', 'provenance_record_ids'}, 'universal embodiment profile shape mismatch')
        profile_id = profile.get('id')
        _require(isinstance(profile_id, str) and profile_id and (profile_id not in embodiment_by_id), 'universal embodiment profile ID mismatch')
        capacities: dict[str, int] = {}
        raw_capacities = profile.get('capability_capacities')
        _require(isinstance(raw_capacities, list), f'{profile_id} capability capacities invalid')
        for capacity in raw_capacities:
            _require(isinstance(capacity, dict) and set(capacity) == {'id', 'capacity'} and isinstance(capacity.get('id'), str) and isinstance(capacity.get('capacity'), int) and (not isinstance(capacity['capacity'], bool)) and (capacity['capacity'] >= 0), f'{profile_id} capability capacity mismatch')
            _require(capacity['id'] not in capacities, f'{profile_id} duplicate capability')
            capacities[capacity['id']] = capacity['capacity']
        _strings(profile.get('unavailable_channels'), f'{profile_id}.unavailable_channels', minimum=0)
        _strings(profile.get('support_types'), f'{profile_id}.support_types', minimum=0)
        _require(set(_strings(profile.get('provenance_record_ids'), f'{profile_id}.provenance_record_ids', minimum=1)) <= research['record_ids'], f'{profile_id} embodiment provenance mismatch')
        embodiment_by_id[profile_id] = capacities
    counts = candidate_asset.get('counts')
    _require(isinstance(counts, dict), 'universal candidate counts missing')
    _require(counts.get('research_records') == 60 and counts.get('research_topics') == 20 and (counts.get('research_sources') == 40) and (counts.get('research_candidates') == 220), 'universal candidate research counts drift')
    _require(counts.get('executable_candidates') == len(candidates), 'universal executable candidate count mismatch')
    _require(counts.get('executable_by_role') == dict(role_counts), 'universal executable role counts mismatch')
    _require(counts.get('pixel_evidence_records') == len(pixel_ids), 'universal executable pixel count mismatch')
    _require(counts.get('prop_concepts') == len(props), 'universal prop count mismatch')
    _require(counts.get('embodiment_profiles') == len(embodiments), 'universal embodiment count mismatch')
    _require(counts.get('proposal_profiles') == len(proposal_profiles) == 12, 'universal proposal-profile count mismatch')
    _require(counts.get('context_distance_profiles') == len(context_profiles) == 18, 'universal context-distance profile count mismatch')
    compatibility_top_keys = {'schema', 'reviewed_at', 'candidate_asset_sha256', 'predicate_contract', 'predicate_kind_ids', 'resource_kind_ids', 'slot_ids', 'slot_state_contract', 'facet_resolution_order', 'event_spine_contract', 'event_spine_templates', 'solver', 'budgets', 'resource_policy', 'distance_policy', 'bridge_policy', 'decision_outcomes', 'decision_reason_code_ids', 'universal_rules', 'guard_candidate_ids', 'router_candidate_ids', 'metric_candidate_ids', 'exception_rules', 'counts', 'semantic_bindings_asset_sha256'}
    _require(isinstance(compatibility, dict) and set(compatibility) == compatibility_top_keys, 'universal compatibility top-level fields mismatch')
    _require(compatibility.get('schema') == 'subculture-illustration-universal-compatibility/v1', 'universal compatibility schema mismatch')
    _require(compatibility.get('candidate_asset_sha256') == _sha256(candidate_path), 'universal compatibility candidate hash mismatch')
    semantic_sha256 = _sha256(semantic_path)
    _require(candidate_asset.get('semantic_bindings_asset_sha256') == semantic_sha256 and compatibility.get('semantic_bindings_asset_sha256') == semantic_sha256, 'universal semantic-binding raw hash mismatch')
    _require(not _forbidden_pair_structures(compatibility), f'universal compatibility contains forbidden pair structures: {_forbidden_pair_structures(compatibility)}')
    decision_reason_code_ids = _strings(compatibility.get('decision_reason_code_ids'), 'universal decision reason-code registry', minimum=len(UNIVERSAL_DECISION_REASON_CODE_IDS))
    _require(decision_reason_code_ids == UNIVERSAL_DECISION_REASON_CODE_IDS and decision_reason_code_ids == sorted(set(decision_reason_code_ids)), 'universal decision reason-code registry must equal the frozen 29-code domain')
    _require(compatibility.get('slot_state_contract', {}).get('enum') == ['fixed', 'closed', 'open'], 'universal slot state enum mismatch')
    event_contract = compatibility.get('event_spine_contract')
    _require(isinstance(event_contract, dict) and event_contract.get('root_count') == 1 and (event_contract.get('phase_count') == 1) and (event_contract.get('second_independent_premise') == 'block') and (event_contract.get('orphan_atom') == 'block'), 'universal one-event-spine contract mismatch')
    budgets = compatibility.get('budgets')
    _require(isinstance(budgets, dict) and budgets.get('event_spines') == 1 and (budgets.get('primary_actions') == 1) and (budgets.get('phases') == 1) and (budgets.get('optional_props') == 1) and (budgets.get('remote_or_high_load_optional_premises') == 1) and (budgets.get('second_independent_premises') == 0) and (budgets.get('orphan_atoms') == 0), 'universal fixed budgets mismatch')
    solver = compatibility.get('solver')
    _require(isinstance(solver, dict) and solver.get('selection_mode') == 'predicate_beam_v1' and (solver.get('beam_width') == 8) and (solver.get('max_candidates_per_facet_before_beam') == 3) and (solver.get('seed_is_final_tiebreak_only') is True), 'universal solver contract mismatch')
    distance_policy = compatibility.get('distance_policy')
    _require(isinstance(distance_policy, dict) and distance_policy.get('axis_ids') == UNIVERSAL_DISTANCE_AXIS_IDS and (distance_policy.get('value_type') == 'ordinal_0_3'), 'universal distance policy mismatch')
    creativity_bands = distance_policy.get('creativity_bands')
    _require(isinstance(creativity_bands, list) and [band.get('id') for band in creativity_bands if isinstance(band, dict)] == ['low', 'middle', 'high'], 'universal creativity-band IDs mismatch')
    _require([(band.get('lower'), band.get('lower_inclusive'), band.get('upper'), band.get('upper_inclusive'), band.get('target_band')) for band in creativity_bands] == [(0.0, True, 0.25, False, 'near'), (0.25, True, 0.75, False, 'middle'), (0.75, True, 1.0, True, 'far')], 'universal creativity boundaries must be [0,.25), [.25,.75), [.75,1]')
    _require(set(distance_policy.get('creativity_changes', [])) == {'eligible_distance_band_weight'}, 'creativity may change only the distance distribution')
    _require({'identity', 'fixed_or_closed_slots', 'feasibility', 'resource_capacity', 'policy', 'culture_scope', 'candidate_count', 'event_spine_count'} <= set(distance_policy.get('creativity_never_changes', [])), 'creativity hard-gate invariants incomplete')
    bridge_policy = compatibility.get('bridge_policy')
    _require(isinstance(bridge_policy, dict), 'universal bridge policy missing')
    _require(bridge_policy.get('middle_minimum') >= 2 and bridge_policy.get('far_minimum') >= 3, 'middle/far bridge minimum was weakened')
    bridge_types = set(_strings(bridge_policy.get('bridge_type_ids'), 'universal bridge types', minimum=1))
    _require(bridge_types == set(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS) and len(bridge_policy['bridge_type_ids']) == len(UNIVERSAL_RUNTIME_BRIDGE_TYPE_IDS), 'universal compatibility bridge enum must be exactly the closed seven types')
    _require({'affordance', 'motivation', 'identity_contrast'} <= bridge_types, 'universal entry bridge types missing')
    _require({'mechanics', 'ownership'} <= bridge_types, 'universal mediation bridge types missing')
    _require({'state_change', 'consequence'} <= bridge_types, 'universal exit bridge types missing')
    _require(bridge_policy.get('bridge_requires_pixel_evidence') is True and bridge_policy.get('explanation_only_bridge') == 'block', 'universal bridge evidence boundary mismatch')
    universal_rules = compatibility.get('universal_rules')
    _require(isinstance(universal_rules, list) and len(universal_rules) == len(UNIVERSAL_RULE_REASON_CODES), 'universal-rule inventory mismatch')
    universal_rule_ids: list[str] = []
    for rule in universal_rules:
        rule_id = rule.get('id') if isinstance(rule, dict) else '<invalid>'
        _require(isinstance(rule, dict) and set(rule) == {'id', 'when_all', 'outcome', 'reason_code', 'candidate_scope'} and isinstance(rule_id, str) and (rule_id in UNIVERSAL_RULE_REASON_CODES) and (rule_id not in universal_rule_ids), f'universal-rule source shape/ID mismatch: {rule_id}')
        universal_rule_ids.append(rule_id)
        _predicate_groups(rule['when_all'], f'universal rule {rule_id}.when_all', graph_predicate_kinds)
        _require(rule['outcome'] in {'block', 'repair', 'allow_with_bridge'} and rule['reason_code'] == UNIVERSAL_RULE_REASON_CODES[rule_id] and (rule['reason_code'] in decision_reason_code_ids) and isinstance(rule['candidate_scope'], str) and bool(rule['candidate_scope']), f'universal-rule source contract drift: {rule_id}')
    _require(set(universal_rule_ids) == set(UNIVERSAL_RULE_REASON_CODES), 'universal-rule source inventory is incomplete')
    for role, field in (('guard', 'guard_candidate_ids'), ('router', 'router_candidate_ids'), ('metric', 'metric_candidate_ids')):
        ids = _strings(compatibility.get(field), f'compatibility.{field}', minimum=1)
        _require(ids == sorted((candidate_id for candidate_id, candidate in candidate_by_id.items() if candidate['role'] == role)), f'compatibility.{field} mismatch')
    exceptions = compatibility.get('exception_rules')
    _require(isinstance(exceptions, list), 'universal exception rules must be a list')
    exception_ids: set[str] = set()
    for exception in exceptions:
        _require(isinstance(exception, dict) and set(exception) == {'id', 'candidate_ids', 'when_all', 'outcome', 'reason', 'provenance_record_ids'}, 'universal exception rule shape mismatch')
        _require(exception.get('id') not in exception_ids, 'duplicate universal exception ID')
        exception_ids.add(exception['id'])
        _require(set(_strings(exception.get('candidate_ids'), f'{exception['id']}.candidate_ids', minimum=1)) <= set(candidate_ids), f'{exception['id']} candidate ref mismatch')
        _predicate_groups(exception.get('when_all'), f'{exception['id']}.when_all', graph_predicate_kinds)
        _require(set(_strings(exception.get('provenance_record_ids'), f'{exception['id']}.provenance_record_ids', minimum=1)) <= research['record_ids'], f'{exception['id']} provenance ref mismatch')
    compatibility_counts = compatibility.get('counts')
    _require(isinstance(compatibility_counts, dict), 'universal compatibility counts missing')
    _require(compatibility_counts.get('guard_candidates') == role_counts['guard'] and compatibility_counts.get('router_candidates') == role_counts['router'] and (compatibility_counts.get('metric_candidates') == role_counts['metric']) and (compatibility_counts.get('exception_rules') == len(exceptions)) and (compatibility_counts.get('pairwise_candidate_edges') == 0), 'universal compatibility counts mismatch')
    trace_source_authorities = _validate_universal_trace_source_authorities(candidate_asset, compatibility, semantic_asset, candidate_by_id)
    try:
        from universal_scene_runtime import validate_universal_scene_assets as runtime_validate_universal_assets
        runtime_assets = runtime_validate_universal_assets(candidate_asset, compatibility, semantic_bindings_asset=semantic_asset, candidate_path=candidate_path, compatibility_path=compatibility_path, semantic_bindings_path=semantic_path, research_manifest=_load_json(asset_dir / 'research_evidence_universal_scene' / 'manifest.json'), research_manifest_path=asset_dir / 'research_evidence_universal_scene' / 'manifest.json')
    except Exception as exc:
        raise ValidationFailure(f'universal runtime rejected its assets: {exc}') from exc
    return {'status': 'pass', 'candidate_sha256': _sha256(candidate_path), 'compatibility_sha256': _sha256(compatibility_path), 'semantic_bindings_sha256': semantic_sha256, 'candidate_count': len(candidates), 'role_counts': dict(sorted(role_counts.items())), 'pixel_evidence_count': len(pixel_ids), 'prop_count': len(props), 'embodiment_profile_count': len(embodiments), 'proposal_profile_count': len(proposal_profiles), 'context_distance_profile_count': len(context_profiles), 'composition_literal_carrier_policy': composition_literal_carrier_policy, 'literal_realization_policy': literal_realization_policy, 'fixed_prop_eligibility_policy': fixed_prop_eligibility_policy, 'semantic_effect_policy': semantic_effect_policy, 'trace_source_authorities': trace_source_authorities, 'topic_count': len(contributions), 'runtime_candidate_count': len(runtime_assets.candidate_by_id)}

def _runtime_texts(graph: Mapping[str, Any]) -> Iterable[tuple[str, str]]:
    for node in graph.get('runtime_nodes', []):
        if isinstance(node, dict):
            yield (str(node.get('id') or ''), str(node.get('definition') or ''))

def validate_all(asset_dir=None):
    root = Path(asset_dir).expanduser().resolve() if asset_dir else default_asset_dir()
    research = validate_research(root)
    universal_research = validate_universal_scene_research(root)
    universal_runtime = validate_universal_scene_runtime_assets(root, universal_research)
    assets = load_runtime_assets(root)
    runtime = validate_assets(root)
    _require(set(assets.nodes_by_id) == research['candidate_ids'], 'runtime node IDs must exactly equal research candidate IDs')
    route_alias_owner: dict[str, str] = {}
    for route_id, route in assets.routes_by_id.items():
        for phrases in route['aliases'].values():
            for phrase in phrases:
                normalized = normalize_text(phrase)
                owner = route_alias_owner.setdefault(normalized, route_id)
                _require(owner == route_id, f'normalized route alias collision: {phrase!r} -> {owner}, {route_id}')
    format_alias_owner: dict[str, str] = {}
    for variant_id, variant in assets.variants_by_id.items():
        for phrases in variant['aliases'].values():
            for phrase in phrases:
                normalized = normalize_text(phrase)
                owner = format_alias_owner.setdefault(normalized, variant_id)
                _require(owner == variant_id, f'normalized format alias collision: {phrase!r} -> {owner}, {variant_id}')
    for topic_id, route in assets.routes_by_id.items():
        _require(route['matrix_id'] == research['matrix_ids'][topic_id], f'route {topic_id} matrix provenance mismatch')
    for node_id, node in assets.nodes_by_id.items():
        definition, role, topic_id = research['candidate_specs'][node_id]
        _require(node['definition'] == definition, f'runtime definition drift: {node_id}')
        _require(node['role'] == role and node['topic_id'] == topic_id, f'runtime role/topic drift: {node_id}')
        provenance = node['provenance']
        _require(provenance['matrix_id'] == research['matrix_ids'][topic_id], f'runtime matrix ref drift: {node_id}')
        _require(set(provenance['evidence_record_ids']) <= research['topic_record_ids'][topic_id], f'runtime cross-topic evidence ref: {node_id}')
    for node_id, text in _runtime_texts(assets.graph):
        for pattern in RUNTIME_NAME_GUARDS:
            _require(not pattern.search(text), f'runtime definition contains protected/named-style text: {node_id}')
    generation_retry_policy = validate_generation_retry_policy(root)
    from moe_element_runtime import load_moe_element_assets, load_moe_grammar_assets
    moe_legacy = load_moe_element_assets(root)
    moe = load_moe_grammar_assets(root, legacy_assets=moe_legacy)
    for key in ('candidate_ids', 'candidate_specs', 'matrix_ids', 'topic_record_ids'):
        research.pop(key, None)
    for key in ('candidate_specs', 'record_ids', 'topic_ids', 'topic_record_ids'):
        universal_research.pop(key, None)
    return {'status': 'pass', 'scope': 'current asset integrity; no stored render or holdout qualification', 'research': research, 'universal_research': universal_research, 'universal_runtime': universal_runtime, 'runtime': runtime, 'generation_retry_policy': generation_retry_policy, 'moe': {'grammar_version': moe.version, 'elements': len(moe.elements_by_id)}}

def parse_args():
    parser = argparse.ArgumentParser(description='Validate current illustration assets and authenticated source contracts.')
    parser.add_argument('--asset-dir', help='override the sibling skill asset directory')
    return parser.parse_args()

def main():
    from moe_element_runtime import MoeElementError
    args = parse_args()
    try:
        result = validate_all(args.asset_dir)
    except (IllustrationRuntimeError, ValidationFailure, MoeElementError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'fail', 'error': str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
