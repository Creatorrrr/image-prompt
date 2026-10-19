"""Compare import-affected CLI help under independent code and no-network policy."""
from pathlib import Path
import hashlib
import subprocess
import sys

ROOT=Path('/Users/chasoik/Projects/image-prompt')
sys.path.insert(0,str(ROOT/'tools/photo_runtime_maintenance'))
import import_seventeen_cleanup as scope
from history_state import new

output=scope.E/'CLI-HELP.json'; assert not output.exists()
cases={}
for label in ('control','combined'):
    project=Path(scope.state.read(scope.E/'PRIVATE-PROJECTS.json')['projects'][label]); scripts=project/'skills/photo-prompt-image-generator/scripts'
    results={}
    for module in ['qualify_local_embeddings','install_photo_h_f2_runtime','audit_moe_render_review','validate_precore_feature_selection']:
        cmd=['/usr/bin/sandbox-exec','-p',scope.four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))',
            str(scope.SKILL/'.runtime/embedding-python/bin/python'),'-I','-B','-c',
            "import runpy,sys;sys.path.insert(0,sys.argv.pop(1));runpy.run_path(sys.argv.pop(1),run_name='__main__')",
            str(scripts),str(scripts/(module+'.py')),'--help']
        child=subprocess.run(cmd,env=scope.checks.environment(),capture_output=True,text=True,timeout=30)
        assert child.returncode==0 and 'usage:' in child.stdout.lower(),child.stderr
        stdout=child.stdout.replace(str(project.resolve()),'<project>').replace(str(project),'<project>')
        results[module]={'exit_code':child.returncode,'normalized_stdout_sha256':hashlib.sha256(stdout.encode()).hexdigest(),
            'stdout':child.stdout,'stderr':child.stderr}
    cases[label]=results
assert {m:r['normalized_stdout_sha256'] for m,r in cases['control'].items()}=={m:r['normalized_stdout_sha256'] for m,r in cases['combined'].items()}
new(output,{'status':'PASS','cases':cases,'normalized_help_output_equal':True,
    'scope':'--help only; no model inference, installation or API invocation','Gemini_calls':0,'CURRENT_writes':0})
print('4 CLI help outputs equal',flush=True)
