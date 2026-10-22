"""Verify byte bindings and summarize the three already completed invocations."""
from pathlib import Path
import hashlib
import json
from collect_evidence import RUNS, OUT


def read(path):
    return json.loads(path.read_bytes())


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    retrieval = read(OUT / 'ACTUAL-RETRIEVAL.json')['cases']
    cases = []
    for item in retrieval:
        arm = item['arm']
        run = RUNS[arm]
        state = read(run / 'workflow.json')
        ledger = run / ('ledger-corrected.ndjson' if arm == 'encounter' else 'image_runs.ndjson')
        rows = [json.loads(line) for line in ledger.read_text().splitlines() if line.strip()]
        assert len(rows) == 1
        row = rows[0]
        image = OUT / 'images' / (arm + '.png')
        review = read(OUT / ('ROOT-REVIEW-' + arm + '.json'))
        assert sha(image.read_bytes()) == review['image_sha256'] == row['image_hashes'][0]['sha256']
        assert row['status'] == 'success' and row['image_call_count'] == 1
        assert state['phase'] == 'review_record_validated'
        native = row['prompt_en'].encode()
        authored = (run / 'final-prompt.txt').read_bytes()
        assert sha(native) == row['runtime_prompt_sha256']
        assert authored in (native, native + b'\n')
        assert row['reference_sha256'] == ['06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7']
        target = OUT / 'arms' / arm / 'native-prompt.txt'
        target.write_bytes(native)
        cases.append({
            **item, 'actual_image_calls': 1, 'returned_images': 1, 'retries': 0,
            'new_12_prompt_contribution_count': int(arm == 'science'),
            'new_12_full_pixel_pass_count': 0,
            'tool': 'image_gen.imagegen', 'observed_model': None,
            'image': str(image.relative_to(OUT)), 'image_sha256': review['image_sha256'],
            'prompt': str(target.relative_to(OUT)), 'runtime_prompt_sha256': sha(native),
            'authored_prompt_file': 'arms/' + arm + '/final-prompt.txt',
            'authored_prompt_file_sha256': sha(authored),
            'file_difference': 'one trailing newline' if authored != native else 'none',
            'authoritative_ledger': 'arms/' + arm + '/' + ledger.name,
            'authoritative_ledger_run_id': row['run_id'],
            'actual_operation': row['workflow_operation_id'],
            'reference_sha256': row['reference_sha256'][0],
            'review_record_valid': True, 'technical_qualification': 'fail',
            'user_judgment': 'pending', 'native_approval_granted': False,
            'independent_root_review': 'ROOT-REVIEW-' + arm + '.json',
        })
    assert len({case['actual_operation'] for case in cases}) == 3
    result = {
        'schema': 'lovecraftian-reinforcement-results/v1',
        'status': 'completed_with_partial_pixel_realization',
        'new_semantic_cards': 12, 'new_candidates': 12, 'new_bindings': 41,
        'regression_tests_passed': 94, 'independent_arms': 3,
        'actual_image_calls': 3, 'returned_images': 3, 'retries': 0,
        'new_candidates_issued': sum(len(case['new_12_exposed']) for case in cases),
        'new_candidates_with_prompt_contribution': 1,
        'new_candidates_with_full_pixel_pass': 0, 'whole_cases_technical_pass': 0,
        'default_activation_by_this_work': False, 'user_acceptance': 'pending',
        'final_default_config_drift': read(OUT / 'PRESERVATION.json')['final_observed_config'],
        'limits': [
            'No matched baseline images or replicated seeds; causal quality gain not measured.',
            'Added12, original84 and preexisting cross-family sources are distinct sets.',
            'Source inspiration does not grant typed native approval.',
            'Superseded metadata records do not represent extra image calls.',
        ],
        'cases': cases,
    }
    (OUT / 'RESULTS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    copies = read(OUT / 'EVIDENCE-COPIES.json')['byte_exact_copies']
    for item in copies:
        assert sha((OUT / item['copy']).read_bytes()) == item['sha256']
    print(json.dumps({'status': 'pass', 'verified_evidence_copies': len(copies),
                      'native_prompt_bindings': 3, 'image_bindings': 3,
                      'actual_image_calls': 3, 'whole_case_pass': 0}))


if __name__ == '__main__':
    main()
