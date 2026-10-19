"""Fresh checks against the changed private source and the unchanged sealed runtime."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import tempfile

import checks
import four_patch
import four_state as scope
from history_state import new
import state


SOURCE_RUNNER = r'''
import os,sys,unittest,json,hashlib
from pathlib import Path
project=Path(sys.argv.pop(1)).resolve();os.chdir(project);sys.path.insert(0,str(project))
suite=unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:])
import bm25f_retrieval,photo_native_pack,photo_camera_evidence,photo_runtime_sources
modules={}
for m in (bm25f_retrieval,photo_native_pack,photo_camera_evidence,photo_runtime_sources):
 p=Path(m.__file__).resolve()
 if not p.is_relative_to(project):raise AssertionError('unchanged source fallback: '+str(p))
 modules[m.__name__]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
for m,name in [(bm25f_retrieval,'_normalized_lexicon'),(photo_native_pack,'resolve_rows'),
 (photo_camera_evidence,'legacy_camera_clauses'),(photo_runtime_sources,'publish_if_ready')]:
 if hasattr(m,name):raise AssertionError('tested source still contains '+name)
result=unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'status':'PASS' if result.wasSuccessful() and not result.skipped else 'FAIL',
 'tests':result.testsRun,'skipped':len(result.skipped),'loaded_changed_modules':modules}))
sys.exit(not result.wasSuccessful() or bool(result.skipped))
'''


def source(group, label='final'):
    output=scope.E/('SOURCE-'+group+'-'+label+'.json')
    if output.exists():raise FileExistsError('never overwrite check evidence')
    project=Path(state.read(scope.E/'PRIVATE-PROJECTS.json')['projects']['combined'])
    expected=state.read(scope.E/'PATCHES.json')['patches']['combined']['candidate_files']
    for path,sha in expected.items():
        if state.sha(project/path)!=sha:raise ValueError('private candidate drift')
    log=project/('source-'+group+'-'+label+'.log')
    new(scope.E/('SOURCE-'+group+'-'+label+'-progress.json'),{'private_log':str(log),
        'final_log':output.name,'scope':'temporary progress only; complete log retained in final evidence'})
    python=scope.SKILL/'.runtime/embedding-python/bin/python'
    env=checks.environment();env['PHOTO_RUNTIME_STORE']=str(project/'.test-runtime')
    policy=four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
    print(group,'private live log:',log,flush=True)
    with log.open('x') as stream:
        child=subprocess.Popen(['/usr/bin/sandbox-exec','-p',policy,str(python),'-I','-c',SOURCE_RUNNER,
            str(project),*checks.GROUPS[group]],cwd=project,env=env,stdout=subprocess.PIPE,
            stderr=stream,text=True,start_new_session=True)
        try:stdout,_=child.communicate(timeout=1200)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGTERM);stdout,_=child.communicate()
            new(output,{'status':'TIMEOUT','stdout':stdout,'stderr':log.read_text()})
            raise ValueError('source regression timeout')
    stderr=log.read_text()
    # Some existing native tests print their own records before the final runner summary.
    try:result=json.loads(stdout.splitlines()[-1])
    except ValueError:result={'status':'HARNESS_UNAVAILABLE'}
    result.update(group=group,exit_code=child.returncode,stdout=stdout,stderr=stderr,
        modules=checks.GROUPS[group],source='modified private working source',
        network_denied=True,live_production_source_reads_denied=True,
        original_writes_denied=True,torch_module_read_denied=True,Gemini_calls=0,CURRENT_writes=0)
    wanted=48 if group=='operating' else 70
    if child.returncode or result.get('tests')!=wanted or result.get('skipped')!=0:result['status']='FAIL'
    for row in result.get('loaded_changed_modules',{}).values():
        rel=str(Path(row['path']).relative_to(project.resolve()))
        if row['sha256']!=expected[rel]:result['status']='FAIL'
    new(output,result)
    print(group,result['status'],result.get('tests'),'tests',flush=True)
    if result['status']!='PASS':raise ValueError('modified-source '+group+' failed: '+stderr[-5000:])


def managed(kind):
    import managed_smoke
    output=scope.E/('MANAGED-'+kind+'.json')
    if output.exists():raise FileExistsError('managed evidence already exists')
    projects=state.read(scope.E/'PRIVATE-PROJECTS.json')['projects']
    original_root=managed_smoke.ROOT;original_profile=managed_smoke.profile
    managed_smoke.ROOT=Path(projects[kind])
    managed_smoke.profile=lambda:four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
    try:managed_smoke.main(output)
    finally:managed_smoke.ROOT=original_root;managed_smoke.profile=original_profile
    result=state.read(output)
    if result['status']!='PASS' or len(result['commands'])!=5:raise ValueError('managed H-F2 qualification failed')


def installed():
    import installed_checks
    output=scope.E/'INSTALLED.json'
    if output.exists():raise FileExistsError('installed evidence already exists')
    if not (state.EVIDENCE/'FIXTURE-PROTECTED.json.gz').exists():
        raise ValueError('original fixture protection must already exist; do not create old evidence')
    original_profile=installed_checks.profile
    installed_checks.profile=lambda:four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))'
    try:installed_checks.main(output)
    finally:installed_checks.profile=original_profile


def history(kind):
    import copy
    import hashlib
    import shutil
    import archive_experiments
    import bundles
    import installed_checks
    import logic_checks
    import native_replay
    output=scope.E/('HISTORY-'+kind+'.json')
    if output.exists():raise FileExistsError('historical evidence already exists')
    if kind=='frozen':
        result=native_replay.audit(installed_checks.FIXTURE)
        new(output,result)
        if result['status']!='PASS':raise ValueError('original frozen audit failed')
    elif kind=='archive':
        with tempfile.TemporaryDirectory(prefix='four-archive-') as tmp:
            restored=bundles.restore(archive_experiments.BUNDLE,state.read(archive_experiments.LOCK),Path(tmp)/'root')
            original_run=subprocess.run
            def closed_source_run(command,*args,**kwargs):
                if isinstance(command,(list,tuple)) and command and command[0]=='/usr/bin/sandbox-exec':
                    command=list(command);index=command.index('-p')+1
                    command[index]+='(deny file-read* '+ ' '.join('(subpath '+json.dumps(str(scope.SKILL/part))+')' for part in ('scripts','precore'))+')'
                return original_run(command,*args,**kwargs)
            subprocess.run=closed_source_run
            raw=Path(tmp)/'result.json'
            try:archive_experiments.replay(restored,raw)
            finally:subprocess.run=original_run
            new(output,{**state.read(raw),'original_working_source_reads_denied':True})
    elif kind=='negative':
        logic_checks.cli_negative(output)
    elif kind=='native-view':
        fixture=installed_checks.FIXTURE;original=state.read(fixture/'workflow.json')
        projects=state.read(scope.E/'PRIVATE-PROJECTS.json')['projects']
        with tempfile.TemporaryDirectory(prefix='four-native-view-') as tmp:
            run=Path(tmp)/'run';shutil.copytree(fixture,run,symlinks=True)
            def rewire(value):
                if isinstance(value,str):return value.replace(str(fixture),str(run))
                if isinstance(value,list):return [rewire(v) for v in value]
                if isinstance(value,dict):return {k:rewire(v) for k,v in value.items()}
                return value
            workflow=rewire(copy.deepcopy(original));workflow.pop('h_f2_binding',None)
            state.write(run/'workflow.json',workflow)
            results={}
            for label in ('control','combined'):
                entry=Path(projects[label])/'skills/photo-prompt-image-generator/scripts/photo_workflow.py'
                python=scope.SKILL/'.runtime/embedding-python/bin/python'
                process=subprocess.run(['/usr/bin/sandbox-exec','-p',four_patch.policy(),str(python),str(entry),
                    'view','--run',str(run)],env=checks.environment(),capture_output=True,text=True,timeout=90)
                results[label]={'exit_code':process.returncode,'stdout_sha256':hashlib.sha256(process.stdout.encode()).hexdigest(),
                    'stderr':process.stderr}
                if process.returncode:raise ValueError('derived native public view failed: '+process.stderr)
                value=json.loads(process.stdout)
                if value.get('contract_version')!='photo-composer-view/v4':raise ValueError('native view was not used')
            if results['control']['stdout_sha256']!=results['combined']['stdout_sha256']:
                raise ValueError('native public view changed')
            new(output,{'status':'PASS','cases':results,
                'fixture':'private derived native route using original issued native pack; not an additional historical original run',
                'exact_native_public_view_equal':True,'original_writes':0,'Gemini_calls':0,'CURRENT_writes':0})
    else:raise ValueError('unknown historical check')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=('operating','native','managed-control','managed-combined','installed','history-frozen','history-archive','history-negative','history-native-view'))
    parser.add_argument('--label',default='final')
    args=parser.parse_args()
    if args.kind in ('operating','native'):source(args.kind,args.label)
    elif args.kind.startswith('managed-'):managed(args.kind.removeprefix('managed-'))
    elif args.kind.startswith('history-'):history(args.kind.removeprefix('history-'))
    else:installed()
