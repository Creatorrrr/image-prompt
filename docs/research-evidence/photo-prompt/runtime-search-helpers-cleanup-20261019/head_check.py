"""Check the separately staged HEAD-derived variant, retaining baseline failures."""
import difflib
import re
from pathlib import Path
import shutil
import sys

ROOT=Path('/Users/chasoik/Projects/image-prompt')
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import search_helpers_cleanup as scope
from history_state import new

output=scope.E/'HEAD-COMPARISON.json'; assert not output.exists()
info=scope.state.read(scope.E/'PRIVATE-PROJECTS.json'); targets=scope.state.read(scope.E/'TARGETS.json')
tests=['tests.test_photo_bm25f_retrieval','tests.test_photo_contextual_source_effects',
    'tests.test_photo_workflow_precore','tests.test_photo_precore_feature_selection','tests.test_photo_retry_context']
results={}; line_maps={}
for label in ('control','combined'):
    project=Path(info['private_parent'])/('head-final-'+label); skill=scope.four_patch.copy_code(project)
    for part in ('scripts','precore'):
        for path in (skill/part).glob('*.py'):
            rel=str(path.relative_to(project)); original=scope.state.git(ROOT,'show',targets['base_head']+':'+rel)
            raw=scope.transform(original,path.stem) if label=='combined' and rel in scope.TARGETS else original
            if label=='combined' and rel in scope.TARGETS:
                assert scope.digest(raw)==targets['index'][rel]
                mapping={}
                for tag,i,j,k,l in difflib.SequenceMatcher(None,original.splitlines(),raw.splitlines(),autojunk=False).get_opcodes():
                    if tag=='equal': mapping.update({k+offset+1:i+offset+1 for offset in range(j-i)})
                line_maps[rel]=mapping
            path.write_bytes(raw)
    shutil.copytree(ROOT/'tests',project/'tests',ignore=shutil.ignore_patterns('__pycache__'))
    for rel in scope.state.git(ROOT,'ls-tree','-r','--name-only',targets['base_head'],'--','tests').decode().splitlines():
        path=project/rel; path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(scope.state.git(ROOT,'show',targets['base_head']+':'+rel))
    result=scope.worker(project,label=='combined',tests,scope.four_patch.policy()+
        '(deny file-read* (regex "/site-packages/torch(/|$)"))',180)
    assert result.get('tests')==43 and result.get('skipped')==0 and not result.get('errors'),result
    results[label]=result
    print('HEAD',label,'tests',result['tests'],'baseline failures',len(result['failures']),flush=True)

def normalize(detail):
    def frame(match):
        rel=match.group(1); line=int(match.group(2))
        if rel in line_maps:
            assert line in line_maps[rel], 'failure in changed code requires inspection'
            line=line_maps[rel][line]
        return 'File "<project>/'+rel+'", line '+str(line)
    return re.sub(r'File "<project>/([^"\n]+)", line (\d+)',frame,detail)

baseline=results['control']; candidate=results['combined']
normalized=[[name,normalize(detail)] for name,detail in candidate['failures']]
assert baseline['failures']==normalized and baseline['errors']==candidate['errors']
assert baseline['exit_code']==candidate['exit_code'] and len(baseline['failures'])==2
new(output,{'status':'PASS','qualification':'Differential only: 41 pass and the same 2 preexisting failures per arm',
    'baseline_test_status':'FAIL','cases':results,'tests_each':43,'preexisting_failures_each':2,
    'new_candidate_failures':0,'normalized_failure_details_equal':True,
    'normalization':'Project paths; candidate traceback line numbers mapped only through exactly equal source lines to HEAD',
    'candidate_failures_normalized':normalized,'equal_source_line_map_sha256':scope.digest(str(line_maps).encode()),
    'source_and_tracked_tests_from':targets['base_head'],'nonpython_inputs':'preserved working copies',
    'network_denied':True,'original_writes_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
