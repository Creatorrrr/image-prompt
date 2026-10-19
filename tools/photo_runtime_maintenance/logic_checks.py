"""Fresh outputs for existing checks; never rerun completed cleanup/GC commands."""
import argparse
import copy
import json
from pathlib import Path
import re
import subprocess
import tempfile

import archive_experiments
import bundles
import checks
import installed_checks
import logic_state as scope
import managed_smoke
import state


def cli_negative(output):
    original = state.read(installed_checks.FIXTURE/'workflow.json')
    receipt = state.read(original['artifacts']['runtime_receipt']['path'])
    manifest = state.read(Path(original['source_binding']['runtime_store'])/'generations'/receipt['generation_id']/'manifest.json')
    results = []
    with tempfile.TemporaryDirectory(prefix='replay-cli-negative-') as temp:
        temp = Path(temp)
        for kind,expected in [('missing_run','missing_or_symlink_file'),('receipt_tamper','receipt_checksum'),
                              ('missing_issued','missing_or_symlink_file'),('changed_generation','generation_checksum')]:
            run = temp/kind
            workflow = copy.deepcopy(original)
            if kind != 'missing_run':
                run.mkdir()
                if kind == 'receipt_tamper':
                    tampered = {**receipt,'algorithm_sha256':'changed'}
                    path = run/'receipt.json'
                    state.write(path,tampered)
                    workflow['artifacts']['runtime_receipt'] = {'path':str(path),'sha256':state.sha(path)}
                elif kind in {'missing_issued','changed_generation'}:
                    store = run/'store'
                    store.mkdir()
                    workflow['source_binding']['runtime_store'] = str(store)
                    if kind == 'changed_generation':
                        state.write(store/'receipts'/(receipt['request_id']+'.json'),receipt)
                        state.write(store/'generations'/receipt['generation_id']/'manifest.json',
                                    {**manifest,'algorithm_sha256':'changed'})
                state.write(run/'workflow.json',workflow)
            command = ['/usr/bin/sandbox-exec','-p',checks.profile(),__import__('sys').executable,
                '-B',str(scope.ROOT/'tools/photo_runtime_maintenance/native_replay.py'),'inspect','--run',str(run)]
            process = subprocess.run(command,env=checks.environment(),capture_output=True,text=True,timeout=30)
            result = json.loads(process.stdout)
            if process.returncode != 2 or result.get('status') != 'DEFER' or expected not in result.get('reason',''):
                raise ValueError('public negative path failed: '+kind+process.stdout+process.stderr)
            results.append({'case':kind,'exit_code':process.returncode,'result':result})
    scope.new(output,{'status':'PASS','cases':results,'network_denied':True,
        'original_run_modified':False,'Gemini_calls':0,'CURRENT_writes':0})


def run(kind, label):
    output = scope.E/(kind+'-'+label+'.json')
    if output.exists():
        raise FileExistsError('use a fresh evidence label')
    if kind in ('OPERATING','NATIVE'):
        checks.run(kind.lower(),output)
        result = state.read(output)
        expected = 48 if kind == 'OPERATING' else 70
        if result['test_count'] != expected or re.search(r'\bskipped[= ]',result['stderr']):
            raise ValueError('regression population or skip changed')
    elif kind == 'INSTALLED':
        installed_checks.main(output)
    elif kind == 'MANAGED':
        managed_smoke.main(output)
    elif kind == 'ARCHIVE':
        with tempfile.TemporaryDirectory(prefix='logic-archive-') as temp:
            restored = bundles.restore(archive_experiments.BUNDLE,state.read(archive_experiments.LOCK),Path(temp)/'root')
            archive_experiments.replay(restored,output)
    elif kind == 'CLI-NEGATIVE':
        cli_negative(output)
    elif kind == 'REPLAY-TESTS':
        command = ['/usr/bin/sandbox-exec','-p',checks.profile(),__import__('sys').executable,
            '-B','-m','unittest','discover','-s',str(scope.ROOT/'tools/photo_runtime_maintenance'),
            '-p','test_native_replay.py','-v']
        process = subprocess.run(command,env=checks.environment(),capture_output=True,text=True,timeout=60)
        count = sum(map(int,re.findall(r'Ran (\d+) tests?',process.stderr)))
        result = {'status':'PASS' if process.returncode == 0 and count == 15 else 'FAIL',
            'test_count':count,'exit_code':process.returncode,'stdout':process.stdout,'stderr':process.stderr,
            'network_denied':True,'model_calls':0,'Gemini_calls':0,'CURRENT_writes':0}
        scope.new(output,result)
    else:
        raise ValueError('unknown check')
    result = state.read(output)
    if result['status'] != 'PASS':
        raise ValueError(kind+' failed')
    print(kind,'PASS',flush=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=('OPERATING','NATIVE','INSTALLED','MANAGED','ARCHIVE','REPLAY-TESTS','CLI-NEGATIVE'))
    parser.add_argument('label')
    args = parser.parse_args()
    run(args.kind,args.label)
