"""Bind final qualification to preserved native originals and canonical reviews.

This validates evidence records. Pixel judgments remain authored by each arm and
independently inspected by the coordinator; this script does not infer pixels.
"""
import hashlib
import json
import pathlib
import struct

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
GENERATION = "f492f8a428edcf489d7fd9b0c2f2525b2dc7ac1c180446cf20f6eb5af7a19870"
FINGERPRINT = "614b5e4fb66959c7304e45bfbb1de601f6cbd892dd908812e2e7492f7ecf843b"
SKILL = "4bff09cfe16ef93183c2130d27143045f02da3114410b61e9b3a0369ea4f2455"
REFERENCE = "048adbd3e4343a3725fec6aa0455aa1f367878560bc15d4493a18fde1ce8604c"
EXPECTED_COUNTS = {"a": 11, "b": 6, "c": 13}


def read(path):
    return json.loads(pathlib.Path(path).read_text())


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def arm_result(arm):
    base = HERE / "arms" / arm
    summary_path = base / "result_summary.json"
    assert summary_path.exists(), f"{arm}: final arm summary is pending"
    rows = [json.loads(line) for line in (base / "image_runs.ndjson").read_text().splitlines() if line.strip()]
    assert len({row['run_id'] for row in rows}) == len(rows), f"{arm}: duplicate ledger rows"
    assert 1 <= len(rows) <= 2, f"{arm}: actual native call scope"
    assert [row['image_call_count'] for row in rows] == list(range(1, len(rows) + 1))
    for row in rows:
        assert row['generation_environment'] == 'native_imagegen'
        assert row['tool'] == 'image_gen'
        assert row['skill_sha256'] == SKILL
        assert GENERATION in row['source_ref']
        assert row['reference_sha256'] == [REFERENCE]
        assert row['cross_arm_inputs_used'] is False
        assert row['candidate_pack_version'] == 'v6'
        for image in row['image_hashes']:
            assert sha(image['path']) == image['sha256']
    final = rows[-1]
    run = pathlib.Path(final['native_render_plan_json']).parents[2]
    workflow = read(run / 'workflow.json')
    assert workflow['phase'] == 'review_record_validated', f"{arm}: canonical final review is pending"
    assert workflow['source_binding']['generation_id'] == GENERATION
    assert workflow['source_binding']['source_fingerprint'] == FINGERPRINT
    artifacts = workflow['artifacts']
    for binding in artifacts.values():
        assert sha(binding['path']) == binding['sha256'], f"{arm}: artifact binding mismatch"
    manifest = read(base / 'run_manifest.json')
    assert manifest['contract_version'] == 'photo-independent-run-manifest/v2'
    assert manifest['ledger_run_id'] == final['run_id']
    assert manifest['image_call_count'] == len(rows)
    assert manifest['cross_arm_inputs_used'] is False
    assert manifest['skill_sha256'] == SKILL
    assert manifest['reference_sha256'] == [REFERENCE]
    assert GENERATION in manifest['source_ref']
    assert manifest['image_hashes'] == final['image_hashes']
    plan = read(artifacts['native_plan']['path'])
    request = read(artifacts['render_request']['path'])
    assert len(plan['references']) == len(request['references']) == 1
    assert plan['references'][0]['sha256'] == request['references'][0]['sha256'] == REFERENCE
    reference_role = request['references'][0]['role']
    assert plan['references'][0]['role'] == reference_role
    assert reference_role in {'visible_face_and_hair_guidance', 'visible_face_hair_guidance'}
    assert plan['payload']['prompt'] == request['runtime_prompt_en']
    assert plan['payload']['referenced_image_paths'] == request['referenced_image_paths']
    assert sha(request['referenced_image_paths'][0]) == REFERENCE
    assert read(artifacts['composed_audit']['path'])['status'] == 'pass'
    assert read(artifacts['runtime_audit']['path'])['status'] == 'pass'
    review = read(artifacts['visual_review']['path'])
    audit = read(artifacts['review_audit']['path'])
    assert audit['visual']['schema_failures'] == []
    assert set(review['hard_gates']) == set(audit['visual']['required_hard_gates'])
    gates = dict(review['hard_gates'])
    if 'generic_review' in artifacts:
        generic = read(artifacts['generic_review']['path'])
        assert audit['generic']['status'] == 'pass' and audit['generic']['failures'] == []
        assert len(generic['gates']) == 4
        for gate in generic['gates']:
            assert gate['gate_id'] not in gates
            gates[gate['gate_id']] = gate
    assert len(gates) == EXPECTED_COUNTS[arm]
    image = pathlib.Path(review['result_image'])
    image_sha = sha(image)
    assert image_sha == review['result_sha256']
    assert {'path': str(image), 'sha256': image_sha} in final['image_hashes']
    assert all(gate['status'] in {'pass', 'fail'} for gate in gates.values())
    failed = [gate_id for gate_id, gate in gates.items() if gate['status'] != 'pass']
    technical = not failed
    assert audit['visual']['technical_qualified'] == all(gate['status'] == 'pass' for gate in review['hard_gates'].values())
    if 'generic' in audit:
        assert audit['generic']['technical_qualified'] == all(gate['status'] == 'pass' for gate in generic['gates'])
    png = image.read_bytes()
    assert png[:8] == b'\x89PNG\r\n\x1a\n'
    dimensions = list(struct.unpack('>II', png[16:24]))
    return {
        'arm_id': arm, 'actual_native_calls': len(rows), 'ledger_run_id': final['run_id'],
        'all_ledger_run_ids': [row['run_id'] for row in rows], 'final_run': str(run),
        'image': str(image), 'image_sha256': image_sha, 'dimensions': dimensions,
        'observed_native_model': None, 'pack_id': final['pack_id'],
        'source_generation': GENERATION, 'source_fingerprint': FINGERPRINT,
        'skill_sha256': SKILL, 'reference_sha256': REFERENCE, 'reference_role': reference_role,
        'record_valid': True, 'all_required_gate_union_pass': technical,
        'passed': len(gates) - len(failed), 'failed': len(failed), 'gate_count': len(gates),
        'failed_gate_ids': failed, 'hard_gate_results': gates,
        'user_acceptance': 'pending',
        'adopted_candidate_ids': final['chosen_candidate_ids'],
        'adopted_visual_concept_ids': final['chosen_visual_concept_ids'],
        'bound_artifacts': artifacts,
        'arm_summary': {'path': str(summary_path), 'sha256': sha(summary_path)},
        'arm_report': {'path': str(base / 'REPORT.md'), 'sha256': sha(base / 'REPORT.md')},
        'ledger': {'path': str(base / 'image_runs.ndjson'), 'sha256': sha(base / 'image_runs.ndjson')},
        'manifest': {'path': str(base / 'run_manifest.json'), 'sha256': sha(base / 'run_manifest.json')},
        'boundary': 'Exact required gate union only; complete adopted relations and additional scene deviations are preserved in the arm report. Record validity does not promote pixel failures or user acceptance.'
    }


if __name__ == '__main__':
    results = [arm_result(arm) for arm in ['a', 'b', 'c']]
    output = {
        'schema_version': 'wardrobe-refinement-final-native-qualification/v1',
        'evidence_record_status': 'PASS',
        'all_three_cases_required_pass': all(result['all_required_gate_union_pass'] for result in results),
        'all_required_pass_cases': sum(result['all_required_gate_union_pass'] for result in results),
        'total_cases': 3, 'actual_new_native_calls': sum(result['actual_native_calls'] for result in results),
        'actual_new_saved_originals': sum(result['actual_native_calls'] for result in results),
        'api_image_calls': 0, 'user_acceptance': 'pending', 'arms': results,
        'boundary': 'Native saved originals and exact canonical reviews. Preflight/source recovery and local crop operations are zero extra image calls. Counts are cumulative per arm, never a sum of cumulative ledger fields. Three cases do not establish causal effectiveness or success for all 148 profiles.'
    }
    (HERE / 'NATIVE-QUALIFICATION-LEDGER.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key: value for key, value in output.items() if key != 'arms'}, ensure_ascii=False))
