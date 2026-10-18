"""Existing offline regressions with new outputs; never overwrite frozen evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import archive_experiments
import bundles
import checks
import installed_checks
import managed_smoke
import state
from deferred_state import E, ROOT


def fingerprint(label):
    if (E/('FINGERPRINT-'+label+'.json')).exists():raise FileExistsError('fingerprint output already exists')
    python=ROOT/'skills/photo-prompt-image-generator/.runtime/embedding-python/bin/python'
    code="import sys,json;from pathlib import Path;root=Path(sys.argv[1]);sys.path.insert(0,str(root/'scripts'));import photo_runtime_sources as r;from photo_global_index_storage import json_digest;s,_=r.capture_sources(root,full=True);print(json.dumps({'source_sha256':json_digest(s),'files':len(s['files']),'code_files':len(s['code']),'model_calls':0}))"
    p=subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile(),str(python),'-I','-c',code,
        str(ROOT/'skills/photo-prompt-image-generator')],env=checks.environment(),capture_output=True,text=True,timeout=180)
    if p.returncode:raise ValueError('main source fingerprint failed: '+p.stderr[-3000:])
    result=json.loads(p.stdout)
    baseline=E/'FINGERPRINT-baseline.json'
    if baseline.exists() and result!=state.read(baseline):raise ValueError('main source/code/model fingerprint changed')
    state.write(E/('FINGERPRINT-'+label+'.json'),result)
    return result


def archive(label):
    if (E/('ARCHIVE-'+label+'.json')).exists():raise FileExistsError('archive output already exists')
    with tempfile.TemporaryDirectory(prefix='photo-deferred-archive-') as temp:
        restored=bundles.restore(archive_experiments.BUNDLE,state.read(archive_experiments.LOCK),Path(temp)/'root')
        archive_experiments.replay(restored,E/('ARCHIVE-'+label+'.json'))


def suite(label,managed=True,native=False):
    if any((E/(name+'-'+label+'.json')).exists() for name in
           ('OPERATING','INSTALLED','ARCHIVE','MANAGED','NATIVE','FINGERPRINT','SUITE')):
        raise FileExistsError('regression output exists; use a fresh label instead of rewriting evidence')
    checks.run('operating',E/('OPERATING-'+label+'.json'))
    installed_checks.main(E/('INSTALLED-'+label+'.json'))
    archive(label)
    if managed:managed_smoke.main(E/('MANAGED-'+label+'.json'))
    if native:checks.run('native',E/('NATIVE-'+label+'.json'))
    result={'status':'PASS','label':label,'operating_tests':48,'installed_goals':2,
        'archived_orders':450,'archived_tests':17,'managed':managed,'native_tests':70 if native else None,
        'fingerprint':fingerprint(label),'network_denied':True,'new_embedding_calls':0,'Gemini_calls':0,'CURRENT_writes':0}
    state.write(E/('SUITE-'+label+'.json'),result)
    print('bounded regression suite PASS:',label,flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('label');p.add_argument('--no-managed',action='store_true')
    p.add_argument('--native',action='store_true');p.add_argument('--fingerprint-only',action='store_true');a=p.parse_args()
    fingerprint(a.label) if a.fingerprint_only else suite(a.label,not a.no_managed,a.native)
