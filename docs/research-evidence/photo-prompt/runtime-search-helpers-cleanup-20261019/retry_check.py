"""Reuse existing closed retry checks against the exact private candidate."""
from pathlib import Path
import sys

ROOT=Path('/Users/chasoik/Projects/image-prompt')
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import search_helpers_cleanup as scope
from history_state import new

output=scope.E/'RETRY.json';assert not output.exists()
project=Path(scope.state.read(scope.E/'PRIVATE-PROJECTS.json')['projects']['combined'])
result=scope.worker(project,True,['tests.test_photo_retry_context'],scope.four_patch.policy()+
    '(deny file-read* (regex "/site-packages/torch(/|$)"))',180)
assert result.get('status')=='PASS' and result.get('exit_code')==0 and result.get('tests')==8 and result.get('skipped')==0,result
for rel,sha in scope.state.read(scope.E/'TARGETS.json')['working'].items():
    assert result['loaded_modules'][Path(rel).stem]['sha256']==sha
new(output,{**result,'network_denied':True,'original_source_reads_denied':True,
    'original_writes_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
print('closed retry tests PASS:',result['tests'],flush=True)
