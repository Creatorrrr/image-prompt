import datetime
import hashlib
import json
import os
import subprocess
from pathlib import Path

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

out = Path('output')
critic_bytes = (out / 'critic-root.json').read_bytes()
critic = json.loads(critic_bytes)
plan_bytes = (out / 'plan.review.json').read_bytes()
plan = json.loads(plan_bytes)
plan_canonical = json.dumps(plan, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
prompt_bytes = (out / 'prompt.review.txt').read_bytes()
bundle = json.loads((out / 'bundle.review.json').read_bytes())
assert critic['status'] == 'pass' and not critic['issues']
assert sha(Path('source.jpg').read_bytes()) == critic['source_sha256']
assert sha(plan_canonical) == critic['integrated_plan_sha256']
assert sha(prompt_bytes) == critic['prompt_sha256']
assert bundle['route']['route_fingerprint'] == critic['route_fingerprint']
bundle['coverage_review'] = critic
save(out / 'bundle.critic-passed.json', bundle)
save(out / 'critic-provenance.json', {
    'received_file': str((out / 'critic-root.json').resolve()),
    'raw_file_sha256': sha(critic_bytes),
    'applied_utc': now(),
    'reviewed_at': critic['reviewed_at'],
    'reviewer': critic['reviewer'],
    'independence_disclosure': critic['independence_disclosure'],
    'report_transformation': 'None; entire actual reviewer object assigned to coverage_review.'
})

checks = []
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
def check(label, args):
    start = now()
    result = subprocess.run(['python3', *args], text=True, capture_output=True, env=env)
    record = {'label': label, 'validator_snapshot': 'skill-v3', 'argv': ['python3', *args],
              'started_utc': start, 'ended_utc': now(), 'exit_code': result.returncode,
              'stdout': result.stdout, 'stderr': result.stderr}
    save(out / (label + '.json'), record)
    checks.append(record)
    if result.returncode:
        save(out / 'pre-render-validation.json', {'status': 'failed', 'checks': checks})
        raise SystemExit(label + ' failed: ' + result.stdout + result.stderr)

check('bundle-validation-critic-v3', ['skill-v3/tools/analysis_bundle.py', 'output/bundle.critic-passed.json'])
check('plan-validation-critic-v3', ['skill-v3/tools/salience_plan.py', 'output/plan.review.json', '--prompt', 'output/prompt.review.txt'])
check('prompt-lint-critic-v3', ['skill-v3/tools/prompt_lint.py', 'output/prompt.review.txt'])

for path in ['prompt.txt', 'plan.json', 'bundle.json']:
    assert not (out / path).exists(), path + ' already exists'
(out / 'prompt.txt').write_bytes(prompt_bytes)
(out / 'plan.json').write_bytes(plan_bytes)
bundle['execution']['prompt_frozen'] = True
save(out / 'bundle.json', bundle)
freeze_time = now()
check('bundle-validation-frozen-v3', ['skill-v3/tools/analysis_bundle.py', 'output/bundle.json'])
check('plan-validation-frozen-v3', ['skill-v3/tools/salience_plan.py', 'output/plan.json', '--prompt', 'output/prompt.txt'])
check('prompt-lint-frozen-v3', ['skill-v3/tools/prompt_lint.py', 'output/prompt.txt'])
save(out / 'prompt-freeze.json', {
    'frozen_utc': freeze_time, 'prompt_file': str((out / 'prompt.txt').resolve()),
    'prompt_sha256': sha(prompt_bytes), 'prompt_utf8_bytes': len(prompt_bytes),
    'prompt_characters': len(prompt_bytes.decode('utf-8')), 'prompt_words': len(prompt_bytes.decode('utf-8').split()),
    'plan_file_sha256': sha(plan_bytes), 'plan_canonical_sha256': sha(plan_canonical),
    'critic_file_sha256': sha(critic_bytes), 'source_sha256': critic['source_sha256'],
    'policy': 'Copy of exactly reviewed UTF-8 production text, no augmentation, no source conditioning.'
})
save(out / 'pre-render-validation.json', {'status': 'ok', 'checks': checks,
    'evidence_scope': 'Route, bundle, plan and literal/standalone structure only; not visual fidelity evidence.'})
save(out / 'generation-request.json', {'prompt': prompt_bytes.decode('utf-8')})
save(out / 'generation-attempt-log.json', {
    'prepared_utc': now(), 'status': 'prepared-not-yet-called',
    'tool': 'image_gen__imagegen', 'prompt_sha256': sha(prompt_bytes),
    'request_fields': ['prompt'], 'image_conditioning_fields': 'both omitted',
    'attempt_count': 0, 'transport_retry_count': 0, 'quality_retry_count': 0,
    'attempt_budget': 1, 'identical_byte_no_delivery_retry_budget': 1,
    'controls': {'exact_model': 'not-exposed/unsupported', 'size': 'not-exposed/unsupported', 'quality': 'not-exposed/unsupported'}
})
print(json.dumps({'status': 'ok', 'frozen_utc': freeze_time, 'prompt_sha256': sha(prompt_bytes), 'checks': len(checks)}))
