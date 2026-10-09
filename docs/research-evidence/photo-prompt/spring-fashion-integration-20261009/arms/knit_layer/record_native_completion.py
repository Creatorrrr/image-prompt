"""Record the single observed native call; never invoke an image generator."""
from pathlib import Path
import json
import os
import subprocess

ARM = Path(__file__).resolve().parent
RUN = ARM / 'run'
WT = Path('/Users/chasoik/.codex/worktrees/spring-fashion-integration-20261009/image-prompt')
PY = '/Users/chasoik/Projects/image-prompt/.venv/bin/python'
SCRIPTS = WT / 'skills/photo-prompt-image-generator/scripts'
ENV = dict(os.environ, PHOTO_RUNTIME_STORE='/Users/chasoik/.cache/image-prompt/photo-runtime-spring-fashion-20261009')

def execute(argv, destination):
    proc = subprocess.run([PY, *map(str, argv)], cwd=WT, env=ENV, text=True, capture_output=True)
    destination.write_text(proc.stdout + proc.stderr)
    if proc.returncode:
        raise RuntimeError(f'{destination.name}: exit {proc.returncode}; original native result preserved')
    return json.loads(proc.stdout)

initial = json.loads((RUN/'workflow.json').read_text())
initial_op = next(o for o in initial['operations'] if o['operation_id'] == '7390e5e48c564d6885d7c25676f4cffd')
if initial_op['status'] == 'complete':
    managed = {'ledger_run_id': initial_op['last_event']['ledger_run_id']}
else:
    managed = execute([SCRIPTS/'photo_workflow.py', 'native-result', '--run', RUN,
                       '--ledger', RUN/'native_image_runs.ndjson', '--result', ARM/'native-tool-observation.json'],
                      ARM/'native-result.stdout.json')
state = json.loads((RUN/'workflow.json').read_text())
composed = json.loads(Path(state['artifacts']['composed']['path']).read_text())
op = next(o for o in state['operations'] if o['operation_id'] == '7390e5e48c564d6885d7c25676f4cffd')
flags = list(op['record_args'])
flags[flags.index('--ledger')+1] = str(ARM/'image_runs.ndjson')
flags += ['--concept', '봄 패션 용어 조사', '--arm-id', 'knit_layer', '--worktree-id', str(WT),
          '--skill-sha256', '9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b',
          '--source-ref', state['source_binding']['generation_id'] + ':' + state['source_binding']['source_fingerprint'],
          '--candidate-pack-version', 'v6', '--independent-no-cross-arm-inputs', '--manifest', str(ARM/'run_manifest.json')]
if composed.get('augmentation_brief') is not None:
    flags += ['--augmentation-brief-json', json.dumps(composed['augmentation_brief'], ensure_ascii=False)]
(ARM/'independent-recorder-args.json').write_text(json.dumps(flags, ensure_ascii=False, indent=2)+'\n')
independent = execute([SCRIPTS/'record_image_run.py', *flags], ARM/'independent-recorder.stdout.json')
assert managed['ledger_run_id'] == independent['run_id']
print(json.dumps({'status': 'recorded', 'ledger_run_id': independent['run_id'],
                  'ledger': str(ARM/'image_runs.ndjson'), 'manifest': str(ARM/'run_manifest.json'),
                  'actual_image_call_count': 1}, ensure_ascii=False))
