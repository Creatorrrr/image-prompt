import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess

ROOT = Path('/Users/chasoik/.codex/worktrees/color-palette-integration/image-prompt')
RUN = Path(__file__).resolve().parent

def read(name):
    return json.loads((RUN / name).read_text())

def write(name, value):
    (RUN / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

pack = read('candidate_pack.json')[0]
composed = read('composed_prompt.json')
saved = read('native_save_receipt.json')
attempt = read('native_attempt1.json')
receipt = read('runtime_receipt.json')
image_path = Path(saved['saved_image_path'])
pixels = image_path.read_bytes()
assert pixels[:8] == b'\x89PNG\r\n\x1a\n'
dimensions = list(struct.unpack('>II', pixels[16:24]))
assert hashlib.sha256(pixels).hexdigest() == saved['image_sha256']

hard_evidence = {
    'embodiment_body_ownership': 'Both forearms and hands visibly connect to the same woman. The screen-left hand belongs to her right forearm and the screen-right hand to her left forearm; neither is an isolated extra hand.',
    'embodiment_joint_chain_and_reach': 'Each elbow bends within the working space. Both wrists reach separate stern and bow underside areas, and visible sleeve-to-wrist chains remain coherent.',
    'embodiment_support_and_balance': 'The open wooden case lies flat on the level bench, and both palms currently support the boat above it. Her torso leans slightly over the bench in a plausible standing arrangement. Ordinary lower-body support is outside the crop and is not individually observed.',
    'embodiment_contact_and_space': 'The right palm cups the stern underside and the left fingers and palm support the bow underside. A narrow visible gap separates the hull from the fitted foam-lined case, preserving the transfer phase with coherent contact boundaries.',
    'embodiment_visibility_and_projection': 'The face, both support hands, full model and open carrying case coexist in the frame. The three-quarter view reveals the critical hull-to-cradle gap despite harmless finger and lower-body occlusion.',
}
write('moe_render_review.json', {
    'schema_version': 'moe-render-review/v1',
    'contract_version': 'photo-embodiment-preflight/v1',
    'pack_id': pack['pack_id'],
    'reviewer': 'agent_arm1_native_pixel_review',
    'result_image': str(image_path),
    'result_sha256': saved['image_sha256'],
    'hard_gates': {key: {'status': 'pass', 'evidence': value} for key, value in hard_evidence.items()},
    'user_judgment': {'baseline_available': False, 'genuinely_moe': 'pending', 'better_than_baseline': 'not_applicable', 'source': 'not_yet_received', 'evidence': ''},
    'supplemental_review_path': str(RUN / 'pixel_review.json'),
    'reviewed_scales': ['native', 'whole_frame'],
    'partial_is_fail': True,
})

evidence = {
    'material_owner_comparison': 'The apron is visibly fibrous and diffusely shaded; the matching aubergine hull has smooth elongated pale glints along its curved flank. The owners remain separately outlined.',
    'accent_and_neutral': 'The small ochre glazed cup sits in the lower-left bench corner. Much larger violet apron and hull areas dominate the selected colored carriers. Shirt and cabin remain pale ivory.',
    'pattern_surface_boundary': 'The violet and ivory mat has more than three alternating woven stripes that end at its cloth border. Apron, hull and cup have solid body pigments; thin brass boat detail is distinct incidental trim.',
    'local_reflectance': 'Apron fibers and folds are matte, hull glints are elongated, cup highlights are rounded and local, and steel tools remain silver. Skin and ivory cloth do not share a violet global wash.',
    'connected_event': 'Both hands contact separate boat underside regions above the waiting fitted case, making careful loading immediately readable. Tools, pad and detached label holder connect the working environment.',
}
test = read('test_case.json')
write('pixel_review.json', {
    'schema_version': 'synthetic-color-material-pixel-review/v1',
    'arm': 'arm1', 'attempt': 1,
    'image_path': str(image_path), 'image_sha256': saved['image_sha256'],
    'native_dimensions': dimensions, 'reviewed_scales': ['native', 'whole_frame'],
    'partial_is_fail': True,
    'predeclared_test_results': [{'id': row['id'], 'status': 'pass', 'evidence': evidence[row['id']], 'criteria': row['pixel_pass_criteria']} for row in test['expected_visible_relations']],
    'synthetic_relations_status': 'pass',
    'new_data_exposure_status': 'pass', 'new_data_selection_status': 'fail_coverage_gap',
    'new_data_pixel_attribution': 'not_applicable_no_new_candidate_or_profile_selected',
    'overall_image_review': {
        'main_impression': 'A calm craftsperson carefully transferring a violet boat model into an open fitted shipping case. Face and support hands lead into the glossy hull, then the receiving case and small ochre cup.',
        'action_environment_connection': 'Workshop shelves, model boats, hand tools, padded case and loading signage make the present packing action coherent. The hull-to-cradle gap supplies a readable next step.',
        'reason_to_care_supported_by_pixels': 'Deliberate two-handed handling and the protective case suggest care for a delicate crafted object.',
        'preceding_repair_limit': 'Tools and pads are compatible with repair, but no specific repaired damage is identifiable. Recently repaired remains authorial context.',
        'color_material_readability': 'Matte violet linen, glossy violet lacquer appearance, ochre glazed cup and ivory cotton remain separate. True wood substrate and chemical composition cannot be established beneath opaque lacquer.',
        'reference_appearance': 'Short dark bob, wispy fringe, visible face proportions and brown eyes are consistent with the supplied guide at this angle. This establishes no actual identity.',
        'qualitative_control_impression_before_label_comparison': 'Quiet, absorbed and approachable, with the task and shared workshop light carrying the appeal.',
        'control_comparison': 'Consistent with subtle supporting sensual direction; no added fetish or surreal treatment is foregrounded. This is an agent perception, not calibrated user preference.',
        'strengths': ['Clear support and receiving geometry', 'Two material responses under one violet pigment family', 'Localized stripes and distinct ochre accent'],
        'weaknesses': ['Generated lettering and brass railing are incidental additions', 'Specific prior repair is implied rather than demonstrated', 'No new candidate or profile was selected in this initial pack'],
    },
    'hard_gate_status': 'pass_5_embodiment_gates',
    'user_judgment': {'source': 'not_yet_received', 'status': 'pending'},
})
write('render_repair_review_applicability.json', {
    'audit': 'audit_image_render_review.py', 'applicability': 'not_applicable',
    'reason': 'The initial core has request_lineage=null and the pack has no render_repair. The generic repair-review auditor requires a v2 lineage repair target; no repair contract or rr_ gates are invented. Required initial embodiment and selected-visual review is recorded in moe_render_review.json.',
    'pack_id': pack['pack_id'], 'image_sha256': saved['image_sha256'],
})
write('preparation_issue.json', {
    'stage': 'post-render_review_metadata_preparation',
    'issue': 'System python3 did not contain optional Pillow library.',
    'resolution': 'Used standard-library PNG IHDR inspection for native dimensions; actual image was already reviewed using view_image.',
    'extra_image_calls': 0,
})

argv = [str(ROOT / '.venv/bin/python'), str(ROOT / 'skills/photo-prompt-image-generator/scripts/record_image_run.py'),
    '--ts', attempt['started_at'], '--concept', pack['authorial_core']['source_request'],
    '--prompt-en', composed['prompt_en'], '--negative-en', composed['negative_en'],
    '--seed', '607298438', '--attempt', '1', '--status', 'success', '--image-path', str(image_path),
    '--tool', 'image_gen.imagegen', '--generation-environment', 'codex_native', '--pack-id', pack['pack_id'],
    '--chosen-candidate-ids-json', json.dumps(composed['chosen_candidate_ids']),
    '--chosen-visual-concept-ids-json', json.dumps(composed['chosen_visual_concept_ids']),
    '--composer', 'agent', '--audit-status', 'pass', '--arm-id', 'arm1', '--worktree-id', str(ROOT),
    '--skill-sha256', hashlib.sha256((RUN / 'skill_snapshot.md').read_bytes()).hexdigest(),
    '--source-ref', 'runtime-generation:' + receipt['generation_id'] + ';source-fingerprint:' + receipt['source_fingerprint'],
    '--candidate-pack-version', 'v6', '--authorial-core-sha256', pack['authorial_core']['canonical_sha256'],
    '--intent-lock-sha256', pack['authorial_core']['intent_lock']['canonical_sha256'],
    '--reference-sha256', '048adbd3e4343a3725fec6aa0455aa1f367878560bc15d4493a18fde1ce8604c',
    '--image-call-count', '1', '--independent-no-cross-arm-inputs', '--manifest', str(RUN / 'run_manifest.json'),
    '--ledger', str(RUN / 'image_runs.ndjson')]
environment = dict(os.environ)
environment['PHOTO_RUNTIME_STORE'] = '/tmp/color-palette-runtime-20261006'
result = subprocess.run(argv, cwd=ROOT, env=environment, text=True, capture_output=True)
(RUN / 'record_attempt1_stdout.json').write_text(result.stdout)
(RUN / 'record_attempt1_stderr.txt').write_text(result.stderr)
if result.returncode:
    print(result.stdout, result.stderr)
    raise SystemExit(result.returncode)
for name in ['native_attempt1.json', 'moe_render_review.json', 'pixel_review.json', 'render_repair_review_applicability.json', 'run_manifest.json', 'image_runs.ndjson', 'record_attempt1_stdout.json', 'record_attempt1_stderr.txt']:
    shutil.copy2(RUN / name, RUN / 'initial-run' / name)
print(json.dumps({'recorder_exit_code': result.returncode, 'native_dimensions': dimensions, 'synthetic_test_status': 'pass', 'hard_gate_count': len(hard_evidence), 'repair_review': 'not_applicable'}))
