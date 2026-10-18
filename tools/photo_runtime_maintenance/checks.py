"""Explicit operating/native/archive checks; never discover archived experiments."""
import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess

from state import ROOT, EVIDENCE, write

GROUPS = {
    'operating': ['tests.test_photo_installed_h_f2','tests.test_photo_bm25f_retrieval',
                  'tests.test_photo_sharded_search','tests.test_photo_slot_oracle','tests.test_photo_local_embeddings'],
    'native': ['tests.test_photo_workflow_precore','tests.test_photo_precore_feature_selection',
               'tests.test_photo_native_permission_transport','tests.test_photo_native_member_scope_transport',
               'tests.test_photo_native_manual_role_view_transport','tests.test_photo_workflow_transport_bindings',
               'tests.test_photo_contextual_source_effects','tests.test_photo_workflow_runtime_bridge',
               'tests.test_photo_native_runtime_freshness'],
}


def environment():
    env = dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',
               HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
    for name in ['PYTHONPATH','GEMINI_API_KEY','GOOGLE_API_KEY','OPENAI_API_KEY','ANTHROPIC_API_KEY']:
        env.pop(name,None)
    return env


def profile():
    wt = '/Users/chasoik/.codex/worktrees/slot-search-relevance/image-prompt'
    return ('(version 1)(allow default)(deny network*)'
            '(deny file-read* (subpath '+json.dumps(wt)+'))'
            '(deny file-write* (subpath '+json.dumps(str(ROOT))+')'
            ' (subpath '+json.dumps(str(Path.home()/'.cache/image-prompt'))+'))')


def run(group,output):
    python = ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
    if group == 'archive':
        command = [str(python),str(ROOT/'tools/photo_runtime_maintenance/archive_experiments.py')]
        # Archive replay owns its own stronger sandbox and temporary restored tree.
    else:
        code = "import os,sys,unittest;root=sys.argv.pop(1);os.chdir(root);sys.path.insert(0,root);suite=unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:]);r=unittest.TextTestRunner().run(suite);sys.exit(not r.wasSuccessful())"
        command = ['/usr/bin/sandbox-exec','-p',profile(),str(python),'-I','-c',code,str(ROOT),*GROUPS[group]]
    child = subprocess.Popen(command,cwd=ROOT,env=environment(),stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,text=True,start_new_session=True)
    try:
        stdout,stderr = child.communicate(timeout=1200)
    except subprocess.TimeoutExpired:
        os.killpg(child.pid,signal.SIGTERM)
        stdout,stderr = child.communicate()
        write(output,{'status':'TIMEOUT','group':group,'stdout':stdout,'stderr':stderr,'limit_seconds':1200})
        raise ValueError('regression subprocess exceeded its resource ceiling')
    p = subprocess.CompletedProcess(command,child.returncode,stdout,stderr)
    count = re.findall(r'Ran (\d+) tests?',p.stderr+p.stdout)
    result = {'status':'PASS' if p.returncode==0 else 'FAIL','group':group,'modules':GROUPS.get(group,[]),
              'exit_code':p.returncode,'test_count':sum(map(int,count)),
              'stdout':p.stdout,'stderr':p.stderr,'network_denied':True,'Gemini_calls':0,'CURRENT_writes':0,
              'scope':'working-source runtime contracts; actual installed checks are separate'}
    write(output,result)
    print(group,result['status'],result['test_count'],'tests',flush=True)
    if p.returncode:
        print(p.stderr[-8000:])
        raise ValueError('regression check failed')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('group',choices=[*GROUPS,'archive'])
    p.add_argument('--output',type=Path,required=True)
    a = p.parse_args();run(a.group,a.output)
