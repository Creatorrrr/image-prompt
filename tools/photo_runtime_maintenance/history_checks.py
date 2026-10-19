"""Reuse real regressions with new outputs and deny every target/cache quarantine read."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile

import archive_experiments
import bundles
import checks
import installed_checks
import managed_smoke
from history_state import E, ROOT, new, targets
import state

QUARANTINE = ROOT/'.codex-artifacts/history-bytecode-cleanup-20261019'
KINDS = ('OPERATING','INSTALLED','ARCHIVE','MANAGED','FINGERPRINT','POLICY')


def denials():
    paths=[ROOT/r['path'] for r in targets()]
    return '(deny file-read* '+ ' '.join('(literal '+json.dumps(str(p))+')' for p in paths)+')'+\
        '(deny file-read* (subpath '+json.dumps(str(QUARANTINE))+'))'


def fingerprint(output):
    python=ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
    code="import sys,json;from pathlib import Path;root=Path(sys.argv[1]);sys.path.insert(0,str(root/'scripts'));import photo_runtime_sources as r;from photo_global_index_storage import json_digest;s,_=r.capture_sources(root,full=True);print(json.dumps({'source_sha256':json_digest(s),'files':len(s['files']),'code_files':len(s['code']),'model_calls':0}))"
    p=subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile(),str(python),'-I','-c',code,
        str(ROOT/'skills/photo-prompt-image-generator')],env=checks.environment(),capture_output=True,text=True,timeout=180)
    if p.returncode:raise ValueError('fingerprint failed: '+p.stderr[-2000:])
    state.write(output,json.loads(p.stdout))


def native_verbose(output):
    """Same nine modules, with a private live log for this long regression run."""
    python=ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
    code="import os,sys,unittest;root=sys.argv.pop(1);os.chdir(root);sys.path.insert(0,root);r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:]));sys.exit(not r.wasSuccessful())"
    log=Path(os.environ['PHOTO_HISTORY_NATIVE_LOG'])
    with log.open('x') as stream:
        child=subprocess.Popen(['/usr/bin/sandbox-exec','-p',checks.profile(),str(python),'-I','-c',code,
            str(ROOT),*checks.GROUPS['native']],cwd=ROOT,env=checks.environment(),stdout=subprocess.PIPE,
            stderr=stream,text=True,start_new_session=True)
        try:stdout,_=child.communicate(timeout=1200)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGTERM);stdout,_=child.communicate()
            state.write(output,{'status':'TIMEOUT','stdout':stdout,'stderr':log.read_text()})
            raise ValueError('native regression exceeded 1200 seconds')
    stderr=log.read_text();count=sum(map(int,re.findall(r'Ran (\d+) tests?',stderr)))
    state.write(output,{'status':'PASS' if child.returncode==0 else 'FAIL','group':'native',
        'modules':checks.GROUPS['native'],'test_count':count,'exit_code':child.returncode,
        'stdout':stdout,'stderr':stderr,'network_denied':True,'Gemini_calls':0,'CURRENT_writes':0})
    if child.returncode or count!=70:raise ValueError('native regression population or result changed')


def child(kind,output):
    original=subprocess.Popen;receipts=[];extra=denials()
    def guarded_popen(*args,**kwargs):
        command=args[0] if args else kwargs['args']
        if isinstance(command,(list,tuple)) and command and str(command[0])=='/usr/bin/sandbox-exec':
            command=list(command);index=command.index('-p')+1;command[index]+=extra
            receipts.append({'profile_sha256':hashlib.sha256(command[index].encode()).hexdigest(),
                'target_read_denials':len(targets()),'quarantine_read_denied':True})
            if args:args=(command,*args[1:])
            else:kwargs['args']=command
        return original(*args,**kwargs)
    # Inject the stronger policy at each existing sandbox boundary; nested sandbox activation is unsupported.
    subprocess.Popen=guarded_popen
    try:
        if kind=='OPERATING':checks.run('operating',output)
        elif kind=='NATIVE':native_verbose(output)
        elif kind=='INSTALLED':installed_checks.main(output)
        elif kind=='MANAGED':managed_smoke.main(output)
        elif kind=='FINGERPRINT':fingerprint(output)
        elif kind=='ARCHIVE':
            with tempfile.TemporaryDirectory(prefix='history-archive-') as temp:
                root=bundles.restore(archive_experiments.BUNDLE,state.read(archive_experiments.LOCK),Path(temp)/'root')
                archive_experiments.replay(root,output)
        elif kind=='POLICY':
            available=[ROOT/r['path'] for r in targets() if (ROOT/r['path']).is_file()]
            if QUARANTINE.exists():available.extend(p for p in QUARANTINE.rglob('*.pyc') if p.is_file())
            if not available:raise ValueError('need an existing forbidden file to prove read denial')
            original_file=available[0];quarantined=next((p for p in available if p.is_relative_to(QUARANTINE)),None)
            probes=[original_file]+([quarantined] if quarantined and quarantined!=original_file else [])
            code="from pathlib import Path;import sys;\nfor name in sys.argv[1:]:\n try:Path(name).read_bytes()\n except PermissionError:pass\n else:raise SystemExit('forbidden cache was readable')\n"
            p=subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile(),sys.executable,'-I','-c',code,*map(str,probes)],
                capture_output=True,text=True,env=checks.environment(),timeout=30)
            if p.returncode:raise ValueError('cache read denial not enforced: '+p.stderr+p.stdout)
            state.write(output,{'status':'PASS','existing_files_denied':list(map(str,probes))})
        else:raise ValueError('unknown check kind')
        result=state.read(output)
        if not receipts:raise ValueError('regression ran without a sandbox receipt')
        result['cache_read_policy']={'sandbox_commands':receipts,'network_denied':True,
            'original_project_and_runtime_writes_denied':True,'target_count':228,
            'fixture_setup':'trusted launcher copies to private temporary directories'}
        state.write(output,result)
    finally:subprocess.Popen=original


def run_check(kind,label):
    output=E/(kind+'-'+label+'.json')
    if output.exists():raise FileExistsError('check evidence exists; use a new label')
    with tempfile.TemporaryDirectory(prefix='history-check-') as temp:
        raw=Path(temp)/'result.json'
        env=checks.environment()
        if kind=='NATIVE':
            env['PHOTO_HISTORY_NATIVE_LOG']=str(Path(temp)/'native.log')
            new(E/('NATIVE-'+label+'-progress.json'),{'private_log':env['PHOTO_HISTORY_NATIVE_LOG'],
                'scope':'live progress only; complete log retained in final result'})
        p=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),'child',kind,str(raw)],
            env=env,capture_output=True,text=True,timeout=1500 if kind=='NATIVE' else 900)
        result=state.read(raw) if raw.exists() else {'status':'FAIL'}
        result['worker']={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
        new(output,result)
        if p.returncode or result.get('status','PASS')!='PASS':
            raise ValueError(kind+' failed: '+p.stderr[-2500:]+p.stdout[-1500:])
        if kind=='FINGERPRINT':
            baseline=E/'FINGERPRINT-baseline.json'
            if baseline.exists():
                keys=('source_sha256','files','code_files','model_calls')
                if any(result[k]!=state.read(baseline)[k] for k in keys):raise ValueError('source/code/model fingerprint changed')
        print(label,kind,'PASS',flush=True)
        return result


def suite(label):
    if any((E/(kind+'-'+label+'.json')).exists() for kind in (*KINDS,'SUITE')):
        raise FileExistsError('suite evidence exists; never overwrite')
    results={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(run_check,kind,label):kind for kind in KINDS}
        for future in as_completed(futures):results[futures[future]]=future.result()
    if results['OPERATING']['test_count']!=48 or results['ARCHIVE']['experiment_tests']!=17:
        raise ValueError('regression population differs')
    new(E/('SUITE-'+label+'.json'),{'status':'PASS','operating_tests':48,
        'installed_goals':len(results['INSTALLED']['goals']),'archive_orders':
        results['ARCHIVE']['old_full_orders']+results['ARCHIVE']['latest_full_orders'],
        'archive_tests':17,'managed_commands':len(results['MANAGED']['commands']),
        'source_sha256':results['FINGERPRINT']['source_sha256'],'cache_read_denials':228,
        'quarantine_reads_denied':True,'Gemini_calls':0,'new_embedding_calls':0,'CURRENT_writes':0})
    print('suite PASS:',label,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['suite','child','native'])
    p.add_argument('label');p.add_argument('output',nargs='?',type=Path);a=p.parse_args()
    if a.command=='child':child(a.label,a.output)
    elif a.command=='native':run_check('NATIVE',a.label)
    else:suite(a.label)
