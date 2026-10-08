import datetime
import hashlib
import json
import pathlib
import struct


ARM = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path('/Users/chasoik/.codex/worktrees/selfie-pose-integration/image-prompt')
SKILL = ROOT / 'skills/photo-prompt-image-generator'


def load(name):
    return json.loads((ARM / name).read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(name, value):
    (ARM / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def link(name, label=None):
    return f'[{label or name}]({ARM / name})'


metadata = load('native-result-metadata.json')
manifest = load('run_manifest.json')
runtime = load('exact-runtime-request-v2.json')
receipt = load('exact-runtime-receipt-v2.json')
composed = load('composed-input-v2.json')
pixel = load('pixel-observations-v2.json')
review = load('visual-review-v2.json')
audit = load('review-audit-output-v2.json')
replay = load('phase1-v2-replay.json')
phase1 = load('phase1-freeze-summary.json')
contribution = load('data-contribution-v2.json')
artist = load('artist-notes-v2.json')
random = load('random-concept-selection.json')
compose_audit = load('compose-audit-output-v2.json')
generic = load('generic-repair-review-applicability.json')
ledger = [json.loads(x) for x in (ARM / 'image_runs.ndjson').read_text().splitlines() if x.strip()]
review_audit_path = 'run_v2/revisions/3c73938f05684afb9102dc5335a84ab0/review_audit.json'
runtime_audit_path = 'run_v2/revisions/4859398eba794c6b907a7a7ca6e46a6d/runtime_audit.json'
visual_audit = load(review_audit_path)['visual']
render_audit = load(runtime_audit_path)
image_path = ARM / 'generated-native-attempt-1.png'
image_bytes = image_path.read_bytes()
dimensions = list(struct.unpack('>II', image_bytes[16:24]))
runtime_bytes = (ARM / 'exact-runtime-prompt-v2.txt').read_bytes()
final_bytes = (ARM / 'final-prompt-v2.txt').read_bytes()
composed_bytes = composed['prompt_en'].encode()
ref = runtime['references'][0]
ref_hash = digest(pathlib.Path(ref['path']).read_bytes())

checks = {
    'native_image_hash': digest(image_bytes) == metadata['image_sha256'] == pixel['image_sha256'] == review['result_sha256'] == manifest['image_hashes'][0]['sha256'],
    'native_original_byte_identical': image_bytes == pathlib.Path(metadata['returned_local_path']).read_bytes(),
    'native_png_dimensions': dimensions == [1237, 1272] == metadata['native_dimensions'] == pixel['full_native_view_payload_dimensions'],
    'exact_runtime_text_equals_request': runtime_bytes.decode() == runtime['runtime_prompt_en'],
    'runtime_hash_equals_manifest_and_ledger': digest(runtime_bytes) == manifest['runtime_prompt_sha256'] == ledger[0]['runtime_prompt_sha256'],
    'final_prompt_equals_compose_plus_storage_newline': final_bytes == composed_bytes + b'\n',
    'exact_pack_negative_preserved': runtime['runtime_negative_en'] == composed['negative_en'] == ledger[0]['negative_en'],
    'new_candidate_literal_in_exact_runtime': contribution['literal_new_source_evidence']['prompt_evidence'] in runtime['runtime_prompt_en'],
    'reference_hash_unchanged': ref_hash == ref['sha256'] == manifest['reference_sha256'][0] == ledger[0]['reference_sha256'][0],
    'one_actual_call_one_ledger_row': len(ledger) == 1 and metadata['actual_image_call_count'] == ledger[0]['image_call_count'] == manifest['image_call_count'] == 1 and ledger[0]['attempt'] == 1,
    'original_run_zero_actual_calls': replay['original_run_actual_native_calls'] == 0 and replay['original_native_payload_will_not_be_called'],
    'core_unchanged': replay['same_core_controls_envelope_intent_contracts']['core'] == receipt['bindings']['authorial_core_sha256'] == manifest['authorial_core_sha256'] == ledger[0]['authorial_core_sha256'],
    'source_generation_v2': receipt['generation_id'] == '8d793f025f759eb7f782d0a194f9dd7f0781370aaff2bbea331146e940c3ab2f' and receipt['source_fingerprint'] == 'fe7ac255143e52fe70b9c64cc7bd02961d176b0258f35a1769aeff6b562a825c',
    'exact_authoritative_nine_gate_set': set(review['hard_gates']) == set(pixel['strict_gate_ids']) == set(visual_audit['required_hard_gates']) and len(review['hard_gates']) == 9,
    'nine_recorded_passes': all(v['status'] == 'pass' for v in review['hard_gates'].values()) and all(v['status'] == 'PASS' for v in pixel['hard_gate_observations']),
    'review_valid_technical_pass': audit['record_valid'] and audit['technical_qualification'] == 'pass' and visual_audit['schema_failures'] == [] and visual_audit['failed_hard_gates'] == [],
    'user_acceptance_pending': audit['user_judgment']['source'] == 'not_yet_received' and audit['user_judgment']['genuinely_moe'] == 'pending' and not visual_audit['representative_eligible'],
    'no_new_hard_gates': pixel['new_hard_gates_added'] is False,
}
initial_checks = dict(checks)
initial_checks.pop('final_prompt_equals_compose_plus_storage_newline')
initial_checks['final_prompt_equals_compose'] = False
save('final-delivery-verification-initial.json', {
    'schema_version': 'photo-final-delivery-verification/v1',
    'status': 'FAIL',
    'checks': initial_checks,
    'explanation': 'The initial verifier assumed the display prompt file had no storage newline. The file has exactly one terminal storage newline beyond the 3234-byte composed prompt; the 3793-byte audited runtime prompt/request are unchanged and byte-exact. No image, prompt content, gate or audit record was edited.',
    'final_file_bytes': len(final_bytes),
    'composed_prompt_bytes': len(composed_bytes),
})
if not all(checks.values()):
    raise RuntimeError(json.dumps(checks, ensure_ascii=False))

verification = {
    'schema_version': 'photo-final-delivery-verification/v1',
    'status': 'PASS',
    'verified_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'checks': checks,
    'native_image_path': str(image_path),
    'native_image_sha256': digest(image_bytes),
    'native_dimensions': dimensions,
    'runtime_prompt_sha256': digest(runtime_bytes),
    'runtime_prompt_byte_count': len(runtime_bytes),
    'final_prompt_sha256': digest(final_bytes),
    'final_prompt_byte_count': len(final_bytes),
    'composed_prompt_sha256': digest(composed_bytes),
    'display_prompt_storage_newline': True,
    'reference_sha256': ref_hash,
    'ledger_row_count': len(ledger),
    'actual_call_count': 1,
    'boundary': 'File/hash/record consistency checks supplement directly inspected native/thumbnail pixels. They do not infer visual truth, actual camera metadata or requesting-user acceptance.',
}
save('final-delivery-verification.json', verification)

artifacts = {
    'report': str(ARM / 'report.md'),
    'qualification': str(ARM / 'qualification.json'),
    'image': str(image_path),
    'returned_original_image': metadata['returned_local_path'],
    'thumbnail': pixel['thumbnail_path'],
    'final_prompt': str(ARM / 'final-prompt-v2.txt'),
    'composed_input': str(ARM / 'composed-input-v2.json'),
    'exact_runtime_prompt': str(ARM / 'exact-runtime-prompt-v2.txt'),
    'exact_runtime_request': str(ARM / 'exact-runtime-request-v2.json'),
    'runtime_receipt': str(ARM / 'exact-runtime-receipt-v2.json'),
    'compose_audit': str(ARM / 'compose-audit-output-v2.json'),
    'image_render_request_audit': str(ARM / runtime_audit_path),
    'authoritative_gate_shape': pixel['authoritative_gate_source'],
    'visual_review': str(ARM / 'visual-review-v2.json'),
    'moe_visual_review_audit': str(ARM / review_audit_path),
    'pixel_observations': str(ARM / 'pixel-observations-v2.json'),
    'artist_notes': str(ARM / 'artist-notes-v2.json'),
    'new_data_contribution': str(ARM / 'data-contribution-v2.json'),
    'source_id_catalog': str(ARM / 'new-source-id-catalog-v2.json'),
    'random_selection': str(ARM / 'random-concept-selection.json'),
    'precore_read_manifest': str(ARM / 'precore-explicit-read-manifest.json'),
    'core_freeze_summary': str(ARM / 'phase1-freeze-summary.json'),
    'unchanged_core_replay': str(ARM / 'phase1-v2-replay.json'),
    'ledger': str(ARM / 'image_runs.ndjson'),
    'independent_run_manifest': str(ARM / 'run_manifest.json'),
    'manifest_provenance': str(ARM / 'manifest-provenance.json'),
    'delivery_verification': str(ARM / 'final-delivery-verification.json'),
    'generic_repair_audit_applicability': str(ARM / 'generic-repair-review-applicability.json'),
}

qualification = {
    'schema_version': 'photo-independent-arm-qualification/v1',
    'arm_id': 'ultrawide',
    'written_at': verification['verified_at'],
    'result': {
        'technical_status': 'PASS',
        'official_strict_pixel_status': 'PASS',
        'official_strict_pixel_pass_count': 9,
        'official_strict_pixel_gate_count': 9,
        'new_data_pixel_correspondence': 'PARTIAL',
        'new_data_source_and_literal_status': 'PASS',
        'user_acceptance': 'PENDING',
        'qualification_status': visual_audit['qualification_status'],
        'representative_eligible': visual_audit['representative_eligible'],
        'repair_performed': False,
        'actual_image_call_count': 1,
        'summary_ko': '회전목마 수선 중 부러진 붉은 목재를 내보이는 직접 셀카. 공식 9개 조건은 모두 PASS이고 새 sf_071의 촬영 팔·얼굴 지향은 보인다. 실제 렌즈 높이·기기 접촉·렌즈 종류는 프레임 밖이므로 새 데이터의 전체 픽셀 대응은 PARTIAL, 사용자 수용은 미확인이다.',
    },
    'independence': {
        'random_seed': random['seed'],
        'random_algorithm': random['random_algorithm'],
        'draw_index': random['draw_index'],
        'selected_concept_id': random['selected_id'],
        'alternatives': random['alternatives'],
        'candidate_data_access_before_selection': False,
        'concept_before_camera': True,
        'cross_arm_inputs_used': False,
        'subagents_created_by_this_arm': 0,
    },
    'request_and_frozen_core': {
        'request_sha256': 'e01d0ad2bb1da5978db473bef7ce3e0212453e8f35839532c8ba05a27dbc7fff',
        'request_envelope_input_file_sha256': '862622c30ddaab8518b5b3b704d41ad32aede7b375040c7b2c1c23f6a4d9c7ce',
        'contracts': replay['same_core_controls_envelope_intent_contracts'],
        'same_original_request_bytes': True,
        'same_precore_author_inputs': True,
        'frozen_core_unchanged': True,
        'active_span_ids': ['complex_topic', 'image_reference'],
        'preserved_anchor_ids': composed['authorial_core_binding']['preserved_anchor_ids'],
        'active_coverage': composed['coverage_assertions'],
        'feature_selection': phase1['selection_audit'],
        'camera_assertion': {'capture_owner': 'unprescribed', 'direction_requirement': 'open', 'height_requirement': 'open', 'polarity': 'advisory'},
        'capture_authorial_choice': 'direct handheld ultra-wide selfie; actor-right capture arm/actor-left display hand in the final prompt',
        'open_dimension_refinements': composed['authorial_core_binding']['authorial_decisions'],
        'controls': {'sensual': 1, 'fetish': 0, 'surreal': 0, 'creativity': 1, 'emphasis': 'sensual_led', 'reference_edit_mode': 'off', 'viewer_enabled': False, 'trend_mode': 'off'},
        'control_application': random['control_application'],
        'authoring_brief_actual_review': True,
    },
    'reference': {
        'path': ref['path'],
        'sha256': ref_hash,
        'directly_viewed_before_authoring_and_generation': True,
        'usage_scope': 'visible face and short dark bob/wispy fringe only',
        'actual_identity_age_or_biography_inferred': False,
        'sent_as': 'referenced_image_paths',
    },
    'source_and_adoption': contribution,
    'original_run_coverage_gap': {
        'run_path': str(ARM / 'run'),
        'generation_id': '4561ae291c9a5626888dc0b05c295ebbe0a4416d40b7099b3c7d3e7216376ccf',
        'source_fingerprint': '333f41dd7bbc9c404ce9ac774824d4480dfd6f8d02f344538b15ea57f950196c',
        'pack_id': '91f07c256e8c73d3',
        'capture_context_slot_exposed': False,
        'new_exposed_candidate_ids': ['slot:lighting:sf_173_base'],
        'actual_image_call_count': 0,
        'started_marker_was_reservation_only': True,
        'old_payload_not_invoked': True,
        'gap_evidence_path': str(ARM / 'data-contribution.json'),
        'hold_evidence_path': str(ARM / 'generation-hold.json'),
        'v2_replay_preserves_original_run': True,
    },
    'runtime': {
        'run_path': str(ARM / 'run_v2'),
        'runtime_store': str(ROOT / 'docs/research-evidence/photo-prompt/selfie-pose-integration-20261008/runtime-store'),
        'generation_id': receipt['generation_id'],
        'source_fingerprint': receipt['source_fingerprint'],
        'pack_id': manifest['pack_id'],
        'pack_version': manifest['candidate_pack_version'],
        'pack_sha256': receipt['pack_sha256'],
        'canonical_runtime_receipt_sha256': receipt['canonical_sha256'],
        'skill_sha256_at_freeze': manifest['skill_sha256'],
        'runtime_prompt_sha256': digest(runtime_bytes),
        'runtime_prompt_byte_count': len(runtime_bytes),
        'composed_prompt_sha256': digest(composed_bytes),
        'composed_prompt_byte_count': len(composed_bytes),
        'final_prompt_file_byte_count': len(final_bytes),
        'final_prompt_file_has_one_storage_newline': True,
        'negative_preserved_exactly': True,
        'image_render_request_audit': render_audit,
        'compose_audit': compose_audit,
        'transparent_background': False,
        'receipt': receipt,
    },
    'generation': {
        **metadata,
        'operation_id': load('native-observation-v2.json')['operation_id'],
        'ledger_run_id': manifest['ledger_run_id'],
        'ledger_row_count': 1,
        'tool_fallback_used': False,
        'repair_call_count': 0,
        'moderation_block_observed': False,
        'native_save_success_is_not_user_acceptance': True,
    },
    'official_pixel_review': {
        'authoritative_gate_shape': pixel['authoritative_gate_source'],
        'contract_sha256': manifest['effective_visual_contract_sha256'],
        'hard_gates_added': False,
        'required_gate_ids': pixel['strict_gate_ids'],
        'native_dimensions': dimensions,
        'native_directly_inspected': True,
        'full_native_view_payload_dimensions': pixel['full_native_view_payload_dimensions'],
        'full_native_view_no_scale_reduction': True,
        'thumbnail_directly_inspected': True,
        'thumbnail_dimensions': pixel['thumbnail_dimensions'],
        'bbox_coordinates': pixel['bbox_coordinates'],
        'hard_gate_observations': pixel['hard_gate_observations'],
        'managed_audit': visual_audit,
        'audit_boundary': 'The auditor validates the recorded evidence schema/gate status, not visual truth. Gate observations are based on this arm directly reading the full native image and thumbnail.',
    },
    'independent_topic_pixel_review': artist['independent_topic_observations'],
    'artist_notes': artist,
    'user_judgment': audit['user_judgment'],
    'audit_corrections_and_applicability': {
        'original_compose_schema_fix': 'Fetish-zero baseline brief added to required bookkeeping; prompt and frozen core unchanged.',
        'visual_review_initial_wire_rejection': 'JSON null user-judgment fields were rejected; changed to pending/not_applicable enum strings. Pixel evidence and all nine statuses were unchanged.',
        'visual_review_wire_correction_path': str(ARM / 'review-wire-correction.json'),
        'generic_render_repair_review': generic,
        'generic_auditor_rejection_output_path': str(ARM / 'image-render-review-audit-output-v2.json'),
        'final_verifier_initial_mismatch': 'Display prompt contains one terminal storage newline; corrected verifier checks this exact storage format without changing any authored/runtime bytes.',
        'final_verifier_initial_evidence_path': str(ARM / 'final-delivery-verification-initial.json'),
    },
    'final_delivery_verification': verification,
    'artifacts': artifacts,
}
save('qualification.json', qualification)

gate_labels = {
    'vo_pc_pc16_owner_relation_1': ('주체 손의 전방 제시', '우측 제시 손·소매의 연결과 좌측 촬영 팔이 구분된다.'),
    'vo_pc_pc16_owner_relation_2': ('손과 물체 접촉', '붉은 목재와 엄지·반대쪽 굽힌 손가락의 접촉 경계가 보인다.'),
    'vo_pc_pc16_owner_relation_3': ('가까운 손·물체의 깊이', '전경의 큰 손·목재, 얼굴, 뒤 작업대·말의 층이 나뉜다.'),
    'vo_pc_pc16_owner_relation_4': ('표정 영역 가림 없음', '목재와 그립은 얼굴 우하단에 있고 두 눈과 작은 미소가 읽힌다.'),
    'embodiment_body_ownership': ('신체 소유', '각 팔은 같은 인물의 서로 다른 어깨·소매에서 이어진다.'),
    'embodiment_joint_chain_and_reach': ('관절 연쇄·도달', '한 팔의 전방 확장과 반대 팔의 굽힌 제시 자세가 공존한다.'),
    'embodiment_support_and_balance': ('지지·균형', '허리까지의 직립 자세가 자연스럽고 큰 목마는 작업대 쪽에 놓인다.'),
    'embodiment_contact_and_space': ('접촉·공간', '손가락이 목재의 칠한 몸통을 잡고 부러진 끝·표정은 분리된다.'),
    'embodiment_visibility_and_projection': ('가시성·투영', '촬영 팔, 그립, 얼굴, 뒤 수선 공간의 전후 관계가 함께 보인다.'),
}
table_rows = []
for gate in pixel['hard_gate_observations']:
    title, evidence = gate_labels[gate['gate_id']]
    regions = '; '.join(f"{r['region_id']} {r['bbox_xyxy']}" for r in gate['native_regions'])
    scales = 'native + thumbnail' if gate['required_review_scale'] == 'both' else 'native'
    table_rows.append(f"| `{gate['gate_id']}` ({title}) | PASS | {scales} | {regions} | {evidence} |")

report = f'''직접 셀카 arm B는 **기술 감사 PASS, 공식 픽셀 조건 9/9 PASS, 새 데이터의 전체 픽셀 대응 PARTIAL, 사용자 수용 PENDING**이다. 최초 native 이미지 1회가 정상 반환되었고 추가 생성이나 API 전환은 하지 않았다. 새 후보의 촬영 팔·얼굴 지향은 보이지만 실제 기기와 렌즈 높이는 프레임 밖에 있어 확인할 수 없다.

![회전목마 수선 중 직접 셀카]({image_path})

독립 seed `35437455`로 일반지식에서 만든 네 대안 중 `carousel_repair`를 추첨했다. 푸른 저녁의 회전목마 수선 공간에서 부러진 붉은 목재를 가까이 보여주고, 뒤의 붉은 갈기와 금속 이음새·목재 가루·사포·전구를 연결했다. 작은 미소의 이유가 수선 상황에서 읽히도록 의미를 먼저 정했다. 직접 손에 든 초광각 셀카는 에이전트의 촬영 선택이다. 사용자가 카메라 방식·높이를 잠근 것으로 취급하지 않았다. {link('random-concept-selection.json', '추첨 기록')}

참조 이미지를 직접 보고 얼굴과 짧은 어두운 단발·성긴 앞머리만 활용했다. 실제 신원·나이·이력을 추정하지 않았다. 원래 JPEG path를 native `referenced_image_paths`에 넣었고 SHA-256 `{ref_hash}`가 요청·런타임·ledger에서 같다. 저장된 컨트롤 sensual=1, fetish=0, surreal=0, creativity=1 및 실제 authoring brief를 적용했다.

후보 접근 전에 neutral feature 9개, baseline, camera assertion, 두 active spans(`complex_topic`, `image_reference`), core/selection/embodiment review를 동결했다. camera assertion의 capture owner는 `unprescribed`, 방향·높이는 `open`이었다. V2에도 원문과 네 계약 hash가 같다. 초기 손 좌우 표기는 이후 open pose에서 actor-right 촬영/actor-left 제시로 정돈했고, 새 후보의 근사 eye-line 높이는 open camera에서 채택했다. 핵심 사건·참조·의미는 바뀌지 않았다. {link('phase1-v2-replay.json', '동결 재사용 증거')}

| 동결 계약 | SHA-256 |
|---|---|
| core | `{replay['same_core_controls_envelope_intent_contracts']['core']}` |
| intent lock | `{replay['same_core_controls_envelope_intent_contracts']['intent_lock']}` |
| envelope | `{replay['same_core_controls_envelope_intent_contracts']['envelope']}` |
| controls | `{replay['same_core_controls_envelope_intent_contracts']['controls']}` |

원래 run의 pack `91f07c256e8c73d3`에는 capture_context 슬롯이 없었고 새 조명 후보 `sf_173_base`만 노출됐다. 보류된 reserved/started payload는 호출하지 않았으며 원래 run의 실제 생성은 0회다. 원래 run·pack·감사를 보존했다. V2의 capture_mode 경로에서 같은 동결 core로 재조회한 결과는 다음과 같다. {link('data-contribution.json', '원래 coverage gap')}, {link('data-contribution-v2.json', 'V2 기여 기록')}

| 층위 | 실제 결과 |
|---|---|
| runtime generation | `{receipt['generation_id']}` |
| source fingerprint | `{receipt['source_fingerprint']}` |
| V2 pack | `b889a5e9d99b64f2` / v6 |
| 새 후보 노출 | `slot:capture_mode:sf_071_base`, `slot:lighting:sf_173_base` |
| 새 후보 채택 | `slot:capture_mode:sf_071_base` |
| 새 profile 노출·채택 | 없음 |
| 기존 데이터 채택 | `visual-concept:pc_pc16_owner_relation`의 전체 4개 구성 요소 |

새 `sf_071` literal은 “{contribution['literal_new_source_evidence']['prompt_evidence']}”이다. 근사 눈높이, 촬영 팔의 주체 소유, 얼굴의 렌즈 지향을 명시한다. 기존 `pc_pc16`은 제시 손의 소유·목재 접촉·가까운 깊이·표정 가림 없음에 기여한다. 회전목마·수선 사건·재료 연결·초광각 선택은 후보 접근 전의 기본 저작에서 왔다. 기존 `pc_*`를 이번 새 데이터로 계산하지 않았다.

{link('final-prompt-v2.txt', '최종 프롬프트')}는 composed prompt 3234바이트에 저장용 마지막 newline 1바이트를 가진다. 실제 도구에 보낸 원문은 {link('exact-runtime-prompt-v2.txt', 'exact runtime prompt')} 3793바이트이며 SHA-256 `{digest(runtime_bytes)}`이다. pack negative가 정확히 포함되었고 {link('exact-runtime-request-v2.json', '런타임 요청')}·{link('exact-runtime-receipt-v2.json', '불변 runtime receipt')}·native plan의 바인딩을 검사했다. 구성 감사는 PASS이고 candidate coverage 밖의 4개 사용자 의미를 자유 서술/assertion으로 보존했다는 quality warnings는 유지했다.

실제 native 호출은 `{metadata['actual_invocation_started_at']}`–`{metadata['actual_invocation_ended_at']}`의 1회다. 이미지 원본은 **1237×1272 PNG**, SHA-256 `{digest(image_bytes)}`이며 반환 원본과 arm 복사본이 byte-identical이다. 실제 모델명은 도구 결과에 없어 `null`로 기록했다. {link('generated-native-attempt-1.png', '원본 이미지')}, {link('native-result-metadata.json', '반환·보존 기록')}, {link('image_runs.ndjson', '단일 ledger row')}, {link('run_manifest.json', '독립 manifest')}

아래는 생성 전 이미 고정된 4개 기존 visual gates와 5개 embodiment gates만 판정한 결과다. 전체 native pixels와 311×320 thumbnail을 직접 읽었다. 좌표는 원본의 좌상단 원점 `(x0,y0,x1,y1)` 근사 영역이며 관절 각도·물리 거리 측정값은 아니다. 상세 원본 증거와 각 한계는 {link('pixel-observations-v2.json', '픽셀 관찰 기록')}에 있다.

| 공식 gate | 판정 | 확인 scale | 원본 위치 | 실제 픽셀 증거 |
|---|---|---|---|---|
{chr(10).join(table_rows)}

발·촬영 손·기기 본체는 crop 밖이다. 보이는 직립 몸통과 팔 연쇄는 모순 없이 읽히며, 공식 게이트의 가시성·소유·도달·그립은 관찰 가능하다. 이 판정으로 실제 발바닥 접촉이나 프레임 밖의 기기 접촉을 확인했다고 주장하지 않는다. {link('visual-review-v2.json', '공식 visual review')}와 {link(review_audit_path, 'managed moe/visual review audit')}는 schema failures·failed gates가 각각 빈 배열이고 `visual_technical_qualified_user_judgment_pending`이다. 감사 도구는 기록의 유효성을 검사하며 픽셀 판정은 이 arm의 직접 관찰에 따른다.

새 데이터에 대한 독립 주제 관찰은 공식 9개 gate와 별도다. 새 hard gate를 추가하지 않았다.

| 독립 주제 관찰 | 상태 | 근거·한계 |
|---|---|---|
| `sf_071` source/literal/런타임 연결 | PASS | 실제 노출→채택→exact runtime 문구가 연결됨 |
| 촬영 팔의 전방 투영 | PASS | native `[0,548,497,1272]`의 팔이 화면 밖 촬영 위치로 이어짐 |
| 얼굴·시선의 렌즈 방향 | PASS | native 얼굴 `[355,250,800,648]`, 눈 `[465,340,738,416]`이 관찰자 방향으로 향함 |
| 근사 eye-line의 시각 일치성 | PARTIAL | 대화하는 듯한 높이는 자연스럽지만 active lens 자체는 보이지 않음 |
| 실제 렌즈 높이·촬영 손/기기 접촉 | UNOBSERVABLE | 카메라와 촬영 손이 프레임 밖 |
| 초광각 의도의 투영 | 부분 지지 | 전경 손·팔 확대와 후경 작업 공간은 보임; 실제 렌즈 종류는 UNOBSERVABLE |
| `0.5` 기기 배율 | 미선택 / UNOBSERVABLE | 입력으로 채택하지 않았고 raster에서 측정값으로 주장하지 않음 |
| 새 데이터 전체 픽셀 대응 | PARTIAL | 보이는 팔·얼굴 방향과 물리 카메라 사실의 증명 범위가 다름 |

독립 artist notes에서는 얼굴→큰 전경 그립→목마의 계층과 붉은 칠의 재료 연결이 장점이다. 이미지의 작은 미소와 수선 공간은 휴식 중 셀카로 읽힌다. 목마가 선택한 actor-right 대신 actor-left 뒤에 놓였고 이음새는 임시 clamp보다 금속 bridge plate/brace처럼 보인다. 이것은 open 저작 세부의 작은 차이이며 공식 gate 실패가 아니다. 실제 수선 전후 역사와 피로감은 픽셀만으로 확정되지 않는다. {link('artist-notes-v2.json', '이미지 기반 artist notes')}

최초 visual-review wire의 사용자 판단 null은 enum 검증에서 거절되어 `pending`/`not_applicable`로 바로잡았다. 이미지·증거·9개 판정은 바꾸지 않았다. 최초 generation에는 render_repair contract가 없어 generic repair review는 **NOT_APPLICABLE**이다. 해당 auditor의 탐색 호출은 lineage target 부족으로 거절됐으며 그 실패 기록을 PASS로 바꾸지 않았다. 실제 image-render-request 감사와 적용 가능한 moe/visual/embodiment 감사는 PASS다. {link('review-wire-correction.json', 'wire 수정 기록')}, {link('generic-repair-review-applicability.json', 'generic 감사 적용 범위')}

마지막 18개 파일·hash·gate-set·단일 호출·source 바인딩 검사는 PASS다. display prompt의 저장 newline에 대한 초기 검증 가정만 수정했고 런타임 문구를 바꾸지 않았다. 사용자 직접 판단은 아직 없으며 `representative_eligible=false`로 유지한다. 기술/픽셀/사용자 수용을 구분한 기계 판독 결과는 {link('qualification.json', 'qualification.json')}, 최종 일관성 증거는 {link('final-delivery-verification.json', 'delivery verification')}에 있다.
'''
(ARM / 'report.md').write_text(report)
print(json.dumps({'report': str(ARM / 'report.md'), 'qualification': str(ARM / 'qualification.json'), 'verification_check_count': len(checks), 'technical': qualification['result']['technical_status'], 'official_pixel': qualification['result']['official_strict_pixel_status'], 'new_topic_pixel': qualification['result']['new_data_pixel_correspondence'], 'user_acceptance': qualification['result']['user_acceptance']}, ensure_ascii=False))
