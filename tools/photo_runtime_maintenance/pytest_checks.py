"""Reuse bounded regressions with new evidence and 65 original/quarantine read denials."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import checks
import history_checks as shared
import pytest_proof
from pytest_state import E, ROOT, new, targets
import state

QUARANTINE=ROOT/'.codex-artifacts/pytest-bytecode-cleanup-20261019'
KINDS=(*shared.KINDS,'PYTEST')


def denials():
    return '(deny file-read* '+' '.join('(literal '+json.dumps(str(ROOT/r['path']))+')' for r in targets())+')'+\
        '(deny file-read* (subpath '+json.dumps(str(QUARANTINE))+'))'


def child(kind,output):
    if kind=='PYTEST':
        rows=pytest_proof.load_lock()['rows'];receipts=[];original=subprocess.Popen
        def audited(*args,**kwargs):
            command=args[0] if args else kwargs['args']
            if command[0]=='/usr/bin/sandbox-exec':
                profile=command[command.index('-p')+1]
                if denials() not in profile:raise ValueError('compiler lacks cache read denials')
                receipts.append(hashlib.sha256(profile.encode()).hexdigest())
            return original(*args,**kwargs)
        subprocess.Popen=audited
        try:
            with tempfile.TemporaryDirectory(prefix='pytest-cache-contract-') as temp:
                pytest_proof.compile_rows(rows,Path(temp)/'root',read_denials=denials())
        finally:subprocess.Popen=original
        if not receipts:raise ValueError('pytest contract ran without sandbox')
        state.write(output,{'status':'PASS','exact_writer_and_reader_checks':len(rows),
            'original_and_quarantine_reads_denied':True,'sandbox_profiles':receipts,
            'cache_code_executions':0,'Gemini_calls':0,'CURRENT_writes':0})
        return
    # Adapt only this private worker's module globals; shared code/evidence are never edited.
    shared.E=E;shared.QUARANTINE=QUARANTINE;shared.targets=targets;shared.denials=denials
    shared.child(kind,output)
    result=state.read(output)
    result['cache_read_policy']['target_count']=65
    state.write(output,result)


def run_check(kind,label):
    output=E/(kind+'-'+label+'.json')
    if output.exists():raise FileExistsError('use a new evidence label')
    with tempfile.TemporaryDirectory(prefix='pytest-cleanup-check-') as temp:
        raw=Path(temp)/'result.json';env=checks.environment()
        if kind=='NATIVE':
            env['PHOTO_HISTORY_NATIVE_LOG']=str(Path(temp)/'native.log')
            new(E/('NATIVE-'+label+'-progress.json'),{'private_log':env['PHOTO_HISTORY_NATIVE_LOG'],
                'scope':'live progress only; full log preserved in final JSON'})
        p=subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),'child',kind,str(raw)],
            env=env,capture_output=True,text=True,timeout=1500 if kind=='NATIVE' else 900)
        result=state.read(raw) if raw.exists() else {'status':'FAIL'}
        result['worker']={'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
        new(output,result)
        if p.returncode or result.get('status','PASS')!='PASS':raise ValueError(kind+' failed: '+p.stderr[-2500:])
        if kind=='FINGERPRINT' and (E/'FINGERPRINT-baseline.json').exists():
            before=state.read(E/'FINGERPRINT-baseline.json')
            if any(result[k]!=before[k] for k in ('source_sha256','files','code_files','model_calls')):
                raise ValueError('source/code/model fingerprint changed')
        print(label,kind,'PASS',flush=True);return result


def suite(label):
    if any((E/(kind+'-'+label+'.json')).exists() for kind in (*KINDS,'SUITE')):raise FileExistsError('suite already exists')
    result={}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures={pool.submit(run_check,kind,label):kind for kind in KINDS}
        for future in as_completed(futures):result[futures[future]]=future.result()
    if result['OPERATING']['test_count']!=48 or result['ARCHIVE']['experiment_tests']!=17:
        raise ValueError('regression population changed')
    new(E/('SUITE-'+label+'.json'),{'status':'PASS','operating_tests':48,
        'installed_goals':len(result['INSTALLED']['goals']),
        'archive_orders':result['ARCHIVE']['old_full_orders']+result['ARCHIVE']['latest_full_orders'],
        'archive_tests':17,'managed_commands':len(result['MANAGED']['commands']),
        'pytest_writer_reader_checks':result['PYTEST']['exact_writer_and_reader_checks'],
        'source_sha256':result['FINGERPRINT']['source_sha256'],'cache_read_denials':65,
        'quarantine_reads_denied':True,'Gemini_calls':0,'new_embedding_calls':0,'CURRENT_writes':0})
    print('suite PASS:',label,flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['suite','child','native']);p.add_argument('label');p.add_argument('output',nargs='?',type=Path);a=p.parse_args()
    if a.command=='child':child(a.label,a.output)
    elif a.command=='native':run_check('NATIVE',a.label)
    else:suite(a.label)
