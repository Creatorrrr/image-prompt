"""GC only ignored bytecode reproduced byte-for-byte from protected clean source."""
import argparse
import importlib.util
import marshal
import os
from pathlib import Path
import py_compile
import re
import shutil
import struct
import subprocess
import sys
import tempfile

from state import ROOT, EVIDENCE, read, write, sha

CACHES = ('skills/photo-prompt-image-generator/scripts/__pycache__',
          'skills/photo-prompt-image-generator/precore/__pycache__','tests/__pycache__')


def inventory():
    baseline = read(EVIDENCE/'BASELINE.json.gz')
    dirty = baseline['repositories'][str(ROOT)]['status']
    qualified = []; deferred = []
    with tempfile.TemporaryDirectory(prefix='photo-bytecode-proof-') as temp:
        for folder in CACHES:
            for p in sorted((ROOT/folder).glob('*.pyc')):
                source = p.parent.parent/(p.name.split('.')[0]+'.py')
                reason = None
                try:
                    if p.is_symlink() or p.stat().st_nlink!=1 or str(p) in baseline['files']:
                        raise ValueError('linked or protected bytecode')
                    if source.is_symlink() or not source.is_file() or str(source.relative_to(ROOT)) in dirty:
                        raise ValueError('source absent or original uncommitted work')
                    if str(source) not in baseline['files'] or sha(source)!=baseline['files'][str(source)]['sha256']:
                        raise ValueError('source not in unchanged original baseline')
                    raw = p.read_bytes()
                    if raw[:4]!=importlib.util.MAGIC_NUMBER:
                        raise ValueError('different interpreter; retain historical bytecode')
                    flags = struct.unpack('<I',raw[4:8])[0]
                    modes = {0:py_compile.PycInvalidationMode.TIMESTAMP,
                             1:py_compile.PycInvalidationMode.UNCHECKED_HASH,
                             3:py_compile.PycInvalidationMode.CHECKED_HASH}
                    if flags not in modes:raise ValueError('unknown bytecode header')
                    code = marshal.loads(raw[16:])  # Inspect metadata only; never execute cached code.
                    if not hasattr(code,'co_filename') or Path(code.co_filename).resolve()!=source.resolve():
                        raise ValueError('compiled source owner is uncertain')
                    opt = re.search(r'\.opt-([012])\.pyc$',p.name)
                    restored = Path(temp)/'regenerated.pyc'
                    py_compile.compile(str(source),cfile=str(restored),dfile=code.co_filename,doraise=True,
                                       optimize=int(opt.group(1)) if opt else 0,invalidation_mode=modes[flags])
                    if restored.read_bytes()!=raw:
                        raise ValueError('exact regeneration differs; preserve unknown historical bytes')
                    qualified.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':len(raw),
                                      'source':str(source.relative_to(ROOT)),'source_sha256':sha(source),
                                      'header_hex':raw[:16].hex(),'compiled_filename':code.co_filename,
                                      'optimization':int(opt.group(1)) if opt else 0,'invalidation_flags':flags,
                                      'interpreter':sys.version,'magic':importlib.util.MAGIC_NUMBER.hex(),
                                      'proof':'byte-for-byte py_compile regeneration; no cached execution'})
                except (ValueError,EOFError,TypeError,struct.error,py_compile.PyCompileError) as error:
                    reason = str(error)
                if reason:
                    deferred.append({'path':str(p.relative_to(ROOT)),'reason':reason})
    result = {'schema':'photo-bytecode-gc/v1','qualified':qualified,'deferred':deferred,
              'qualified_bytes':sum(r['bytes'] for r in qualified),'other_runtime_stores':'DEFER/PRESERVE'}
    write(EVIDENCE/'BYTECODE-GC.json',result)
    print('bytecode exact regeneration:',len(qualified),'eligible;',len(deferred),'deferred',flush=True)
    return result


def apply():
    if (EVIDENCE/'STAGE07.json').exists():
        raise ValueError('GC already complete')
    rows = inventory()['qualified']
    if not rows:
        write(EVIDENCE/'STAGE07.json',{'status':'PASS','removed_files':0,'all_uncertain_members_deferred':True})
        return
    paths = [str(ROOT/r['path']) for r in rows]
    opened = subprocess.run(['/usr/sbin/lsof','-n','-P','-F','n','--',*paths],capture_output=True,text=True,timeout=45)
    if opened.returncode not in (0,1) or any(v[1:] in paths for v in opened.stdout.splitlines() if v.startswith('n')):
        raise ValueError('open or uncertain bytecode; no files removed')
    env = dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    quarantine = Path(tempfile.mkdtemp(prefix='photo-cleanup-quarantine-',dir=ROOT/'.codex-artifacts'))
    write(EVIDENCE/'BYTECODE-QUARANTINE.json',{'state':'prepared','path':str(quarantine),
          'targets':[r['path'] for r in rows],'lsof_exit_code':opened.returncode})
    moved = []
    try:
        for row in rows:
            p = ROOT/row['path']
            if sha(p)!=row['sha256'] or sha(ROOT/row['source'])!=row['source_sha256'] or p.stat().st_nlink!=1:
                raise ValueError('GC source/target changed before rename')
            target = quarantine/row['path'];target.parent.mkdir(parents=True,exist_ok=True)
            p.rename(target);moved.append((p,target))
        for name,command in [
            ('GC-OPERATING.json',['python3','tools/photo_runtime_maintenance/checks.py','operating','--output',str(EVIDENCE/'GC-OPERATING.json')]),
            ('GC-INSTALLED.json',['python3','tools/photo_runtime_maintenance/installed_checks.py','--output',str(EVIDENCE/'GC-INSTALLED.json')]),
            ('GC-ARCHIVE.json',['python3','tools/photo_runtime_maintenance/checks.py','archive','--output',str(EVIDENCE/'GC-ARCHIVE.json')])]:
            subprocess.run(command,cwd=ROOT,env=env,check=True,timeout=240)
        subprocess.run(['python3','tools/photo_runtime_maintenance/state.py','verify','--allow-json',str(EVIDENCE/'ALLOWED-CHANGES.json'),
                        '--output',str(EVIDENCE/'VERIFY-07.json')],cwd=ROOT,env=env,check=True,timeout=180)
    except BaseException:
        for original,target in reversed(moved):
            if original.exists():
                raise RuntimeError('restore collision; quarantine retained: '+str(quarantine))
            target.rename(original)
        quarantine.rmdir() if not any(quarantine.iterdir()) else None
        raise
    if any(p.exists() for p,_ in moved):
        raise ValueError('bytecode regenerated concurrently; quarantine retained')
    shutil.rmtree(quarantine)
    write(EVIDENCE/'BYTECODE-QUARANTINE.json',{'state':'removed_after_validation','targets':[r['path'] for r in rows],
          'quarantine_absent':not quarantine.exists(),'lsof_exit_code':opened.returncode})
    write(EVIDENCE/'STAGE07.json',{'status':'PASS','removed_files':len(rows),'removed_logical_bytes':sum(r['bytes'] for r in rows),
          'exact_regeneration_proved':True,'isolated_absence_checks':['operating48','actual_installed_two_goals_native_receipt','archive450_orders_17_tests'],
          'quarantine_removed':True,'unknown_shards_and_stores_preserved':True,'CURRENT_writes':0,'Gemini_calls':0})
    print('GC PASS:',len(rows),'exactly regenerable files removed',flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--apply',action='store_true')
    a = p.parse_args();apply() if a.apply else inventory()
