"""Verify stored independent-arm provenance, without changing any arm artifact."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
REFERENCE = Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')

def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def text_sha(s): return hashlib.sha256(s.encode()).hexdigest()

raw = (HERE / 'RAW-REQUEST.txt').read_bytes()
raw_sha = hashlib.sha256(raw).hexdigest()
source_manifest = read(HERE / 'frozen-source-v1/SOURCE-MANIFEST.json')
source_checks = [{'path': row['path'], 'sha256_matches': sha(HERE / 'frozen-source-v1' / row['path']) == row['sha256']}
                 for row in source_manifest['files']]
assert all(row['sha256_matches'] for row in source_checks)

configurations = [
    ('arm-a', 'precore-freeze-manifest.json', 'composed_audit.json', 'runtime_audit.json', None),
    ('arm-b', 'precore_freeze.json', 'composed_audit.json', 'runtime_audit.json', 'native_args.json'),
    ('arm-c', 'precore-freeze-manifest.json', 'composed-audit.json', 'runtime-audit.json', 'native_call_arguments.json'),
]
results = []
for arm, freeze_name, compose_name, audit_name, native_name in configurations:
    root = HERE / arm
    envelope = read(root / 'request_envelope.json')
    freeze = read(root / freeze_name)
    pack = read(root / 'candidate_pack.json')
    pack = pack[0] if isinstance(pack, list) else pack
    runtime = read(root / 'runtime_request.json')
    native = read(root / native_name) if native_name else runtime['native_inputs']
    manifest = read(root / 'run_manifest.json')
    ledger = [json.loads(line) for line in (root / 'image_runs.ndjson').read_text().splitlines() if line]
    freeze_checks = [{'path': name, 'sha256_matches': sha(root / name) == expected}
                     for name, expected in freeze['files'].items()]
    image_checks = [{'path': row['path'], 'sha256_matches': sha(Path(row['path'])) == row['sha256']}
                    for row in manifest['image_hashes']]
    compose = read(root / compose_name)
    audit = read(root / audit_name)
    checks = {
        'shared_request_bytes': envelope['request_text'].encode() == raw,
        'request_hash': envelope['request_sha256'] == raw_sha,
        'active_span_exact_substrings': all(envelope['request_text'][row['start']:row['end']] == row['text'] for row in envelope['active_spans']),
        'frozen_precore_bytes': all(row['sha256_matches'] for row in freeze_checks),
        'baseline_text_hash': text_sha(pack['authorial_core']['baseline_prompt_en']) == freeze['baseline_prompt_sha256'],
        'native_prompt_exact_runtime_text': native['prompt'] == runtime['runtime_prompt_en'],
        'native_negative_suffix_bound': native['prompt'].endswith('\n\nAvoid: ' + runtime['runtime_negative_en']),
        'reference_original_path': native['referenced_image_paths'] == [str(REFERENCE)],
        'reference_original_bytes': all(row['sha256'] == sha(REFERENCE) and row['path'] == str(REFERENCE) for row in runtime['references']),
        'manifest_reference_hash': manifest['reference_sha256'] == [sha(REFERENCE)],
        'compose_pass_without_failures': compose['status'] == 'pass' and not compose['failures'],
        'runtime_pass_without_failures': audit['status'] == 'pass' and not audit['failures'],
        'image_bytes_preserved': all(row['sha256_matches'] for row in image_checks),
        'one_actual_native_attempt': len(ledger) == 1 and ledger[0]['image_call_count'] == 1 and manifest['image_call_count'] == 1,
        'native_tool_success': ledger[0]['tool'] == 'image_gen.imagegen' and ledger[0]['status'] == 'success',
        'no_cross_arm_inputs_declared': manifest['cross_arm_inputs_used'] is False,
        'qualification_v1_dictionary_bound': pack['provenance']['tags_hash'] == '32f7adada688cfc6298fa9fb2d9f1dc39227d2a8d234f1c26d4b979b9cf0e279',
        'core_manifest_bound': manifest['authorial_core_sha256'] == pack['authorial_core']['canonical_sha256'],
        'intent_lock_manifest_bound': manifest['intent_lock_sha256'] == pack['authorial_core']['intent_lock']['canonical_sha256'],
    }
    results.append({'arm': arm, 'checks': checks, 'freeze_file_checks': freeze_checks,
                    'image_checks': image_checks, 'selected_candidate_ids': ledger[0]['chosen_candidate_ids'],
                    'pack_id': pack['pack_id']})

payload = {'contract_version': 'qualification-evidence-verification/v1',
           'shared_request_sha256': raw_sha, 'reference_sha256': sha(REFERENCE),
           'frozen_runtime_file_count': len(source_checks), 'source_file_checks': source_checks,
           'arms': results, 'all_structural_checks_pass': all(all(row['checks'].values()) for row in results),
           'boundary': 'Hash and contract verification does not establish pixel correctness, native image-model identity, causal improvement, or requester acceptance.'}
(HERE / 'ARTIFACT-VERIFICATION.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'all_structural_checks_pass': payload['all_structural_checks_pass'],
                  'frozen_runtime_file_count': len(source_checks),
                  'failed_checks': {row['arm']: [key for key, value in row['checks'].items() if not value] for row in results}}, ensure_ascii=False))
assert payload['all_structural_checks_pass']
