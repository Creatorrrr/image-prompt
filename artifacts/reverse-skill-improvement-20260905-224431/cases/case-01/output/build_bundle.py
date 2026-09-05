"""Persist actual lane/integration/critic evidence; never supply a synthetic review."""
import json, hashlib, argparse
from pathlib import Path


def read(name):
    return json.loads((Path('output') / name).read_text())


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument('--critic', required=True)
parser.add_argument('--frozen', action='store_true')
args = parser.parse_args()
review = json.loads(Path(args.critic).read_text())
plan = read('plan.json')
source = read('source-metadata.json')
decisions = read('integration-decisions.json')
request = read('execution-metadata.json')
plan_sha = canonical_sha(plan)
assert review['integrated_plan_sha256'] == plan_sha, 'Actual critic does not bind current plan'
bundle = {
    'schema_version': 'reverse-image-analysis-bundle/v2',
    'request': {'user_request': request['raw_request'], 'intent_mode': request['intent']},
    'source_artifact': {'sha256': source['sha256'], 'frame': 'x'.join(map(str, source['dimensions']))},
    'route': read('route.json'),
    'execution': {
        'mode': 'mixed',
        'prompt_frozen': args.frozen,
        'independence_claimed': False,
        'fresh_delegated_lanes': 1,
        'sequential_fallback_lanes': 4,
        'lane_waves': 1,
        'malformed_lane_retries': 0,
        'route_reroutes': 0,
        'failed_helper_spawns': 1,
        'fallback_reason': 'Actual helper spawn failed with agent thread limit reached; root authorized sequential fallback.',
        'critic_independence_disclosure': 'Root, independent of case integrator; shared reviewer across cases. Not claimed to be a newly empty context.',
    },
    'integrated_plan': {'payload': plan, 'sha256': plan_sha},
    'lane_reports': read('report-set.json'),
    'integration': {'status': 'complete', 'finding_dispositions': decisions['finding_dispositions'], 'obligation_dispositions': decisions['obligation_dispositions'], 'conflicts': decisions['conflicts']},
    'adjudications': [],
    'coverage_review': review,
}
if args.frozen:
    prompt_bytes = Path('output/prompt.txt').read_bytes()
    assert prompt_bytes == Path('output/prompt-draft.txt').read_bytes(), 'Frozen bytes differ from reviewed draft'
    prompt_sha = hashlib.sha256(prompt_bytes).hexdigest()
    reviewed_prompt_sha = review.get('reviewed_prompt_sha256') or review.get('prompt_sha256')
    assert reviewed_prompt_sha == prompt_sha, 'Actual critic does not bind current literal prompt'
    bundle['execution']['prompt_sha256'] = prompt_sha
Path('output/analysis-bundle.json').write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'bundle': 'output/analysis-bundle.json', 'plan_sha256': plan_sha, 'prompt_frozen': args.frozen, 'review_status': review['status']}))
