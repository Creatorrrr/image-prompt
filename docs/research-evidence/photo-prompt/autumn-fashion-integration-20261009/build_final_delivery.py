"""Assemble exact native evidence without rewriting frozen arm artifacts."""
from pathlib import Path
import collections
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
E = Path(__file__).resolve().parent
RUN = ROOT / 'skills/photo-prompt-image-generator/data/runs/autumn-fashion-integration-20261009'
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
REFERENCE = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
ARMS = ['arm_1', 'arm_2_redraw', 'arm_3']

def read(path):
    return json.loads(Path(path).read_text())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def rel(path):
    return str(Path(path).relative_to(ROOT))

def main():
    cases = []
    reports = [read(RUN / arm / 'final_report.json') for arm in ARMS]
    concepts = ['비 온 뒤 천문대에서 젖은 난간 위의 별지도를 보호하는 순간',
                '직물 공방에서 셔틀을 날실 사이로 통과시키고 실 고리를 조절하는 순간',
                '옥상 소극장 리허설에서 바람에 풀린 무대 천을 금속 고리에 모으는 순간']
    seeds = [2026100901, 202610090202, 2026100903]
    gates = [(8, 8, []), (8, 6, ['embodiment_contact_and_space', 'embodiment_visibility_and_projection']),
             (9, 6, ['vo_pr_fabric_tension_fold_attachment_2', 'embodiment_contact_and_space', 'embodiment_visibility_and_projection'])]
    selected = [['slot:wardrobe_style:autumn_afr006_v1_candidate'], [], ['slot:garment_detail:autumn_afr027_v1_candidate']]
    old_profiles = [['vg_face_hands_place_readability_profile'], ['vg_face_hands_place_readability_profile'], ['pr_fabric_tension_fold_attachment']]
    relation_status = ['pass', 'not_selected', 'fail']
    clothing = [(4, 5), (4, 5), (3, 4)]
    notes = [
        '열린 올리브 셸의 두 앞판 사이로 같은 착용자의 크림색 플리스 칼라가 보인다. 부츠의 완전한 리본 매듭 끝점과 느슨한 종이를 보호하는 전체 행동은 부족하다.',
        '코듀로이 겉옷, 니트와 셔츠의 레이어, 커프스, 로퍼는 보인다. 반대 손은 베틀 프레임 위에 놓여 있고 요구한 실 고리 접촉과 셔틀의 통과가 확인되지 않는다. 바지 앞주름 두 개도 확인할 수 없다.',
        '트위드 같은 표면, 리브 칼라와 커프스, 체크 스커트와 부츠가 보인다. 봉제선에서 시작하는 주름과 천이 고리 안을 통과하는 경로가 모호하다. 카디건 하단과 스커트 허리밴드의 만나는 지점은 가려졌다.'
    ]
    originals = [reports[0]['result']['tool_returned_path'],
        '/Users/chasoik/.codex/generated_images/01a11d00-de7f-7263-9a63-0f3526e1c54f/exec-dacf9a74-8f5b-4210-8d0c-236bb0a97462.png',
        reports[2]['native_execution']['original_tool_local_path']]
    skill_hash = sha(ROOT / 'skills/photo-prompt-image-generator/SKILL.md')
    for i, arm in enumerate(ARMS):
        parent = RUN / arm
        manifest = read(parent / 'run_manifest.json')
        ledger = [json.loads(v) for v in (parent / 'image_runs.ndjson').read_text().splitlines() if v.strip()]
        assert len(ledger) == 1 and manifest['image_call_count'] == 1
        assert manifest['contract_version'] == 'photo-independent-run-manifest/v2'
        assert manifest['skill_sha256'] == skill_hash
        assert manifest['reference_sha256'] == [sha(REFERENCE)]
        assert manifest['cross_arm_inputs_used'] is False
        assert set(ledger[0]['chosen_candidate_ids']) == set(selected[i])
        assert manifest['chosen_visual_concept_ids'] == ['visual-concept:' + v for v in old_profiles[i]]
        receipts = list(parent.glob('revisions/*/runtime_receipt.json'))
        assert receipts
        assert all(read(v)['generation_id'] == '19523d77b4b4b00ec7eb9ef36833ac8e80c50a0631bfc03babd711b24078d838' for v in receipts)
        assert all(read(v)['source_fingerprint'] == 'b7d450b6529925a0e03786f168c919abd9833a5747e2dd6c97af80747e0bacc6' for v in receipts)
        native_paths = list(parent.glob('revisions/*/native_plan.json'))
        assert len(native_paths) == 1
        native = read(native_paths[0]); payload = native['payload']
        assert payload['referenced_image_paths'] == [str(REFERENCE)]
        assert payload['transparent_background'] is False
        image = E / 'images' / f'arm_{i+1}-attempt_1.png'
        prompt = E / 'prompts' / f'arm_{i+1}-native.en.txt'
        assert payload['prompt'] == prompt.read_text()
        assert sha(image) == sha(originals[i]) == manifest['image_hashes'][0]['sha256']
        total, passed, failed = gates[i]
        case = {'arm_id': arm, 'concept': concepts[i], 'random_seed': seeds[i],
            'authorial_core_sha256': manifest['authorial_core_sha256'],
            'intent_lock_sha256': manifest['intent_lock_sha256'],
            'skill_sha256': skill_hash, 'reference_sha256': sha(REFERENCE),
            'source_generation': '19523d77b4b4b00ec7eb9ef36833ac8e80c50a0631bfc03babd711b24078d838',
            'source_fingerprint': 'b7d450b6529925a0e03786f168c919abd9833a5747e2dd6c97af80747e0bacc6',
            'image_path': rel(image), 'image_sha256': sha(image), 'original_tool_path': originals[i],
            'native_prompt_path': rel(prompt), 'native_prompt_sha256': sha(prompt),
            'report_path': rel(parent / 'final_report.json'), 'report_sha256': sha(parent / 'final_report.json'),
            'ledger_path': rel(parent / 'image_runs.ndjson'), 'ledger_sha256': sha(parent / 'image_runs.ndjson'),
            'manifest_path': rel(parent / 'run_manifest.json'), 'manifest_sha256': sha(parent / 'run_manifest.json'),
            'actual_image_calls': 1, 'additional_image_calls': 0, 'observed_image_model': 'unknown',
            'prompt_audit': 'pass', 'runtime_audit': 'pass', 'review_record_valid': True,
            'required_hard_gates': total, 'passed_hard_gates': passed, 'failed_hard_gate_ids': failed,
            'strict_technical_qualification': 'pass' if passed == total else 'fail',
            'new_candidate_ids_selected': selected[i], 'new_visual_profiles_exposed': [],
            'new_visual_profiles_selected': [], 'existing_visual_profiles_selected': old_profiles[i],
            'selected_new_relation_pixel_status': relation_status[i],
            'supplemental_clothing_goals': {'pass': clothing[i][0], 'total': clothing[i][1]},
            'full_authored_scene_qualified': False, 'root_native_review': notes[i],
            'root_review_scale': 'original_native_image', 'retrieval': 'core_bm25f',
            'successful_live_embedding_query_observed': False, 'user_judgment': 'not_yet_received',
            'representative_eligible': False, 'partial_or_unobservable_is_fail': True}
        cases.append(case)
    assert len({v['authorial_core_sha256'] for v in cases}) == 3
    assert len({v['image_sha256'] for v in cases}) == 3
    assert len({read(RUN / arm / 'run_manifest.json')['ledger_run_id'] for arm in ARMS}) == 3
    fixture = ROOT / 'tests/fixtures/photo_prompt/autumn_fashion_three_arm_pixel_cases_v1.jsonl'
    fixture.write_text(''.join(json.dumps(c, ensure_ascii=False) + '\n' for c in cases))
    before = read(E / 'PRIMARY-FINAL-PRESERVATION.json')
    assert not before['changed_since_initial']
    assert all(v['matches_independent_worktree'] for v in before['owned_files'])
    delivery_observation = read(E / 'PRIMARY-DELIVERY-CONCURRENCY.json')
    assert all(v['same_as_verified_owned'] for v in delivery_observation['autumn_owned_files'])
    final_test_log = (E / 'PRIMARY-DELIVERY-AUTUMN-TESTS.log').read_text()
    assert 'Ran 13 tests' in final_test_log and final_test_log.rstrip().endswith('OK')
    mapping = read(E / 'term-runtime-map.json')
    assert mapping['count'] == len(mapping['terms']) == 347
    authored = read(ASSETS / 'photo_prompt_autumn_fashion_extension.json')
    profiles = read(ASSETS / 'photo_prompt_visual_obligations_autumn_fashion.json')['profiles']
    assert sum(len(v) for v in authored['slots'].values()) == len(profiles) == 112
    result = {'schema': 'autumn-integration-native-test-results/v1',
        'observed_at': datetime.datetime.now(datetime.UTC).isoformat(),
        'task_status': 'requested_integration_and_three_native_tests_completed',
        'native_outcome': 'partial_realization_no_new_profile_pixel_qualified',
        'data': {'term_map_count': 347, 'research_cards': 113, 'sources': 42,
            'new_candidates': 112, 'new_profiles': 112, 'existing_contracts_reused': 17,
            'new_candidate_slots': {k: len(v) for k,v in authored['slots'].items()},
            'authored_native_gates': sum(len(v['authored_components']['components']) for v in profiles),
            'nonpixel_specification_cards': ['AFR068', 'AFR092', 'AFR113'],
            'candidate_source_sha256': sha(ASSETS / 'photo_prompt_autumn_fashion_extension.json'),
            'profile_source_sha256': sha(ASSETS / 'photo_prompt_visual_obligations_autumn_fashion.json')},
        'skill_sha256': skill_hash, 'reference_sha256': sha(REFERENCE),
        'actual_native_call_count': 3, 'additional_native_calls': 0,
        'new_profiles_exposed_in_actual_cases': 0, 'new_profiles_pixel_qualified': 0,
        'selected_new_candidates': 2, 'selected_new_relations_pixel_pass': 1,
        'verification': {'focused_regression_tests_passed': 83, 'primary_autumn_tests_passed': 13,
            'primary_dictionary_validation': 'pass', 'primary_runtime_snapshot': read(E / 'PRIMARY-DELIVERY-RUNTIME.log'),
            'full_suite': read(E / 'FULL-SUITE-CLASSIFICATION.json'),
            'full_suite_tested_source_generation': '19523d77b4b4b00ec7eb9ef36833ac8e80c50a0631bfc03babd711b24078d838',
            'latest_primary_autumn_test_log': 'PRIMARY-DELIVERY-AUTUMN-TESTS.log',
            'corrected_import_tests_passed': 125, 'restored_existing_artifact_tests_passed': 4,
            'full_suite_pass': False},
        'preservation': {'initial_dirty_authored_files_byte_preserved_at_application_and_earlier_final_check': True,
            'initial_dirty_authored_files_identical_at_latest_delivery_observation': not delivery_observation['changed_since_previous_verified_snapshot'],
            'subsequent_concurrent_source_changes_preserved': delivery_observation['changed_since_previous_verified_snapshot'],
            'autumn_owned_files_remain_identical_to_tested_source': True,
            'original_source_manifest_rows_preserved': True, 'concurrent_season_sources_preserved': True,
            'control_or_generator_source_modified': False, 'commit_push_pr': 'not_requested'},
        'independence': {'three_original_agents': True, 'source_envelopes_frozen_before_delegation': True,
            'original_request_bytes_unchanged': True, 'cross_arm_creative_inputs': False,
            'second_original_observatory_core_discarded_before_retrieval_or_generation': True,
            'second_arm_neutral_diversity_filter_and_redraw_disclosed': True,
            'parent_neutral_wire_help_disclosed': True},
        'retry': {'additional_calls': 0, 'all_preparations_preserved': True,
            'reason': 'Closed retry context did not retain optional wardrobe/place prose needed to preserve the original cases. Unsupported restoration or unchanged reroll was not invoked.',
            'skill_rule_path': 'skills/photo-prompt-image-generator/SKILL.md', 'skill_rule_line': 38},
        'cases': cases, 'user_judgment': 'not_yet_received', 'representative_eligible': False}
    (E / 'FINAL-RESULTS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    (E / 'ROOT-NATIVE-REVIEW.json').write_text(json.dumps({'reviewer':'root','cases':cases,
        'boundary':'Direct inspection of each original image and saved native-scale output. The root review is separate from record validation and does not assert user acceptance.'}, ensure_ascii=False, indent=2)+'\n')
    (E / 'DELIVERY-VALIDATION.json').write_text(json.dumps({'status':'pass','cases':3,
        'reference_attached_each_case':True,'native_prompts_exact':True,'original_and_copied_image_hashes_equal':True,
        'distinct_frozen_core_hashes':True,'same_skill_hash':True,'actual_image_calls':3,
        'all_required_work_performed':True,'all_images_qualified':False,'new_profile_pixel_coverage':0},indent=2)+'\n')
    print(json.dumps({'delivery_validation':'pass','cases':3,'actual_image_calls':3,
        'new_profile_pixel_qualified':0,'strict_case_pass_count':1}))

if __name__ == '__main__':
    main()
