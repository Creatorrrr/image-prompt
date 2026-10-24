"""Replay arm A's pre-candidate authored inputs in a disposable neutral run."""
from pathlib import Path
import copy
import json
import subprocess
import sys
import tempfile

R = Path(__file__).resolve().parents[5]
O = Path(__file__).resolve().parent
S = R / 'skills/photo-prompt-image-generator'
A = R / 'generated/photo-runs/campus-query-core-20261024-a'
state = json.loads((A / 'workflow.json').read_text())
seed = json.loads(Path(state['artifacts']['creative_controls']['path']).read_text())['seed']
results = []
with tempfile.TemporaryDirectory(prefix='freeze-contract-', dir=O) as tmp:
    tmp = Path(tmp)
    run = tmp / 'run'
    def call(args):
        result = subprocess.run([sys.executable, str(S / 'precore/prepare_photo_run.py'), *args],
                                capture_output=True, text=True)
        return dict(exit_code=result.returncode, stdout=result.stdout.strip(), stderr=result.stderr.strip())
    p = O / 'inputs'
    result = call(['init', '--run', str(run), '--request', str(p/'request.txt'), '--spans', str(p/'spans.json'),
                   '--request-id', 'campus-query-core-20261024-a', '--topic-context', str(p/'topic-context.json'),
                   '--query-scope', str(p/'query-scope.json'), '--input-inventory', str(p/'input-inventory.json'), '--mode', 'image'])
    assert result['exit_code'] == 0, result
    result = call(['controls', '--run', str(run), '--context', str(A/'creative_context.json'), '--seed', str(seed)])
    assert result['exit_code'] == 0, result
    core = json.loads((A/'core.authored.json').read_text())
    selection = json.loads((A/'precore_feature_selection.authored.json').read_text())
    no_review = copy.deepcopy(selection)
    no_review.pop('ownership_review')
    (tmp/'core.json').write_text(json.dumps(core))
    (tmp/'selection.json').write_text(json.dumps(no_review))
    args = ['freeze', '--run', str(run), '--core', str(tmp/'core.json'), '--selection', str(tmp/'selection.json'),
            '--review', str(A/'embodiment_review.authored.json')]
    result = call(args)
    assert result['exit_code'] != 0 and 'requester_ownership_review_required' in result['stdout']+result['stderr'], result
    results.append(dict(case='new freeze without ownership review rejected', **result))
    for row in core['intent_lock']['semantic_anchors']:
        if row['anchor_id'] == 'core_event':
            row['prompt_evidence'] = 'university cafeteria table'
    for row in selection['ownership_review']['anchors']:
        if row['anchor_id'] == 'core_event':
            row['prompt_evidence'] = 'university cafeteria table'
    (tmp/'core.json').write_text(json.dumps(core))
    (tmp/'selection.json').write_text(json.dumps(selection))
    result = call(args)
    assert result['exit_code'] != 0 and 'authorial detail is locked' in result['stdout']+result['stderr'], result
    results.append(dict(case='atomic author staging inside longer mandatory phrase rejected by real freeze', **result))
    (tmp/'core.json').write_bytes((A/'core.authored.json').read_bytes())
    (tmp/'selection.json').write_bytes((A/'precore_feature_selection.authored.json').read_bytes())
    result = call(args)
    assert result['exit_code'] == 0, result
    results.append(dict(case='same independent baseline with narrow requester anchors freezes', **result))
(O/'REAL-FREEZE-REGRESSION.json').write_text(json.dumps(dict(image_calls=0, cases=results), indent=2))
print(json.dumps(results, indent=2))
