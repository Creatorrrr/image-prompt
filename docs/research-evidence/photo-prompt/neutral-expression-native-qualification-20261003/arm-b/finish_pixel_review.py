"""Persist Arm B's agent-authored native-pixel observations, then bind gates.

This file records human/agent visual observations; it does not score pixels.
It writes only inside Arm B and never generates or edits an image.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('/Users/chasoik/Projects/image-prompt')
ARM = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / '.agents/skills/photo-prompt-image-generator/scripts'))
import audit_composed_prompt


def read(name):
    return json.loads((ARM / name).read_text(encoding='utf-8'))


def write(name, data):
    (ARM / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


pack = read('candidate_pack.json')
pack = pack[0] if isinstance(pack, list) else pack
composed = read('composed_prompt.json')
initial = read('pixel_test_review.json')
contract, errors = audit_composed_prompt.derive_effective_visual_obligation_contract(pack, composed)
embodiment_ids, embodiment_errors = audit_composed_prompt.photo_embodiment.render_gate_ids(pack, composed)
if errors or embodiment_errors:
    raise ValueError({'visual_contract': errors, 'embodiment_contract': embodiment_errors})

hard = {
    'vo_bm_long_limb_build_component_1': {
        'status': 'pass', 'review_scales': ['whole_frame', 'native'],
        'evidence': 'At whole-frame and original native views, the fitted top exposes an uninterrupted readable torso reference from shoulder region to pelvic garment boundary on the central actor. It remains comparable with the same actor\'s limb lengths rather than a separate object or shadow.'
    },
    'vo_bm_long_limb_build_component_2': {
        'status': 'pass', 'review_scales': ['whole_frame', 'native'],
        'evidence': 'At both whole-frame and native views, long upper/lower leg segments lead from hips through knees to visible ankles and shoes, and the near arm has a long shoulder-elbow-wrist path beside the shorter torso reference. The far upper arm is partly hidden, but the named length relation is established by the visible complete near arm and both legs; no concealed numerical length is inferred.'
    },
    'vo_bm_long_limb_build_component_3': {
        'status': 'pass', 'review_scales': ['whole_frame', 'native'],
        'evidence': 'At both whole-frame and native views, exposed upper-arm, forearm, thigh and lower-leg silhouettes show slender transverse volumes on the central actor. Clothing outlines provide context, but thinness is read on exposed limb contours, not from a garment fold or cast shadow.'
    },
    'vo_bm_long_limb_build_owner_state': {
        'status': 'pass', 'review_scales': ['whole_frame', 'native'],
        'evidence': 'At both scales the near shoulder-elbow-wrist chain and hip-knee-ankle chains stay connected to one central actor. The image in the segmented mirror reads as her coherent reflection; no second actor\'s limbs or detached contours supply the body relation.'
    },
    'embodiment_body_ownership': {
        'status': 'pass',
        'evidence': 'Both visible hands and both legs are continuously attributable to the central woman. The nearby mirror shows a corresponding back/side reflection rather than another actor supplying a limb.'
    },
    'embodiment_joint_chain_and_reach': {
        'status': 'pass',
        'evidence': 'The near arm bends from shoulder through elbow and wrist to the lower latch, while the farther hand reaches its brass wheel without an impossible crossing or stretched joint. These rendered targets are locally reachable; their incorrect height is judged separately under contact_and_space and B5.'
    },
    'embodiment_support_and_balance': {
        'status': 'pass',
        'evidence': 'Both low shoes visibly meet the concrete floor, and the standing figure is supported by her legs. No fingertip contact is rendered as bearing body weight; there is no floating sole or need for an absent support.'
    },
    'embodiment_contact_and_space': {
        'status': 'fail',
        'failure_type': 'intended_contact_geometry_and_component_mismatch',
        'evidence': 'The frozen geometry puts two low forward controls beside the hips, with separated waist-level hands and a flush bracket component. In the native image the brass wheel and hand are at chest level, both contacts lie toward the same lateral apparatus, and the newly placed component cannot be singled out. Distinct local contacts are coherent but the intended target heights and spatial staging did not survive rendering.'
    },
    'embodiment_visibility_and_projection': {
        'status': 'pass',
        'evidence': 'The native full frame contains the resolved face, both distinct hand-target contacts, torso, legs and both soles, allowing ownership, reach, support and the incorrect target heights to be assessed. The body is more oblique than the near-frontal authored view and the far upper arm is partly hidden; surface-definition adequacy is separately failed under B3.'
    }
}

required = contract['required_hard_gates'] + embodiment_ids
if set(hard) != set(required) or len(hard) != 9:
    raise ValueError('Review does not exactly cover the effective nine hard gates')

now = datetime.now(timezone.utc).isoformat()
review = {
    'schema_version': 'moe-render-review/v1',
    'contract_version': contract['contract_version'],
    'pack_id': pack['pack_id'],
    'reviewer': '/root/neutral_image_b',
    'reviewed_at_utc': now,
    'result_image': initial['result_image'],
    'result_sha256': initial['result_sha256'],
    'source_authorial_core_sha256': pack['authorial_core']['canonical_sha256'],
    'source_intent_lock_sha256': pack['authorial_core']['intent_lock']['canonical_sha256'],
    'source_embodiment_preflight_sha256': pack['embodiment_preflight']['canonical_sha256'],
    'effective_visual_contract_sha256': audit_composed_prompt.effective_visual_obligation_sha256(contract),
    'hard_gates': hard,
    'pixel_views': initial['views'],
    'partial_is_fail': True,
    'user_judgment': {
        'baseline_available': False,
        'genuinely_moe': 'pending',
        'better_than_baseline': 'not_applicable',
        'source': 'not_yet_received',
        'evidence': 'No direct requesting-user judgment has been received. The frozen baseline is a prompt, not a comparison image.'
    },
    'supplemental_observations': {
        'initial_gate_review': 'pixel_test_review.json',
        'whole_image': 'Face, blue top and repeated circular mirror facets create a coherent photograph. The figure, reference appearance and long narrow outline remain the main focus; this impression is independent of strict contact and muscle-definition failures.',
        'control_perception': 'The authored sensual_editorial=1 and fetish_fashion=0 read as a mild editorial gaze, parted lips and ordinary fitted work-bay clothing. This agent impression does not assert wearer desire or user acceptance.',
        'projection_deviation': 'The rendered body is more oblique than the near-frontal baseline. Far upper-arm surface is partly hidden; no hidden muscle contours are inferred.'
    }
}
write('render_review.json', review)

union = [
    {
        'gate_id': row['gate_id'], 'source': 'frozen_independent_synthetic_test',
        'status': row['status'], 'evidence': row['evidence'], 'evidence_ko': row['evidence_ko']
    }
    for row in initial['gates']
]
union.extend({
    'gate_id': gate_id,
    'source': 'adopted_profile' if gate_id.startswith('vo_') else 'embodiment_preflight',
    **hard[gate_id]
} for gate_id in required)


def count(rows):
    return {'total': len(rows), 'pass': sum(row['status'] == 'pass' for row in rows), 'fail': sum(row['status'] == 'fail' for row in rows)}


counts = {
    'initial': count(initial['gates']),
    'adopted_profile': count([hard[gate_id] for gate_id in contract['required_hard_gates']]),
    'embodiment': count([hard[gate_id] for gate_id in embodiment_ids]),
    'union': count(union)
}
ordinary = {
    'slot:silhouette_proportion:bm_wiry_definition': {
        'narrow_transverse_volumes': 'pass', 'localized_muscle_planes': 'fail',
        'localized_tendon_contours': 'fail', 'owner_relation': 'pass', 'overall_realization': 'fail',
        'coverage': ['B2_narrow_frame', 'B3_shallow_arm_definition', 'embodiment_body_ownership'],
        'boundary': 'Candidate adoption and literal prompt evidence do not establish rendered wiry muscle/tendon definition.'
    },
    'slot:silhouette_proportion:willowy_long_limb_proportion': {
        'torso_reference_length': 'pass', 'upper_lower_limb_lengths': 'pass',
        'slender_transverse_volumes': 'pass', 'owner_relation': 'pass', 'overall_realization': 'pass',
        'coverage': contract['required_hard_gates']
    }
}
combined = {
    'contract_version': 'agent-combined-native-pixel-review/v1', 'arm': 'B',
    'reviewer': '/root/neutral_image_b', 'reviewed_at_utc': now,
    'result_image': initial['result_image'], 'result_sha256': initial['result_sha256'],
    'counts': counts, 'all_required_gates_reviewed': True, 'missing_gate_ids': [],
    'strict_union': union, 'ordinary_candidate_realization': ordinary,
    'partial_is_fail': True, 'blocked_is_unscored': True, 'actual_image_call_count': 1,
    'generation_status': 'success', 'technical_qualified': False, 'user_acceptance': 'pending',
    'declined_optional_profile': {
        'profile_id': 'slender_linear_build',
        'reason': 'Existing owner_separation component terms and evidence-must-mention terms disagree; optional adoption was declined without inserting reporting prose.',
        'independent_initial_B2_result': 'pass', 'operating_data_edited_by_arm': False
    },
    'scope_boundary': 'One authored complex concept and one native image test keyword realization. There is no generation ablation or comparative baseline image, so this result cannot establish an isolated causal effect of the data update or universal generation reliability.'
}
write('combined_pixel_review.json', combined)
print(json.dumps({'counts': counts, 'failed_union_gate_ids': [row['gate_id'] for row in union if row['status'] == 'fail']}, ensure_ascii=False, indent=2))
