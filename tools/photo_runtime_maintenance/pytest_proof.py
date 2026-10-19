"""Pin source provenance and pytest toolchain; compile only private source copies."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import bundles
import checks
from deferred_restore import publish_exclusive
import history_proof
from pytest_state import E, ROOT, new, targets, load_baseline
import state

PYTHON=ROOT/'.venv/bin/python'
git=history_proof.git


def scan_references(refine=False):
    prior=state.read(ROOT/'docs/research-evidence/photo-prompt/runtime-cleanup-final-deferred-20261019/REFERENCE-CLOSURE.json')
    reviewed={(r['file'],r['line'],r['text']) for r in prior['generic_cache_lines']}
    names=re.compile('|'.join(re.escape(Path(r['path']).name) for r in targets()))
    generic=re.compile(r'SourcelessFileLoader|cache_from_source|marshal\.loads|marshal\.load\(|\.pyc')
    direct=[];unknown=[];hits=[];python_files=metadata=0
    for path,before in load_baseline()['files'].items():
        p=Path(path)
        if before.get('kind')!='file' or p.suffix!='.py' and p.name not in ('manifest.json','CURRENT.json','workflow.json'):continue
        text=p.read_text(errors='replace')
        if p.suffix=='.py':
            python_files+=1
            for n,line in enumerate(text.splitlines(),1):
                if generic.search(line):
                    known=(path,n,line.strip()) in reviewed
                    inspected=(refine and p==ROOT/'docs/research-evidence/photo-prompt/runtime-cleanup-final-deferred-20261019/probe_remaining_bytecodes.py'
                        and n==44 and state.sha(p)=='a3e143949a888cf48a681f73e6994ae9fc2ca2db3205bf01c74c197157fed593')
                    row={'file':path,'line':n,'text':line.strip(),'classification':'PRIVATE_COMPILE_OUTPUT_REVIEWED' if inspected else 'REUSED_INSPECTION_REVIEW' if known else 'UNRESOLVED'}
                    hits.append(row)
                    if not known and not inspected:unknown.append(row)
        else:metadata+=1
        for m in names.finditer(text):direct.append({'file':path,'cache':m.group()})
    # Archive contents and the complete protected source corpus must still be byte-identical.
    # Earlier scan verified all 563 members; verify archive seals afresh without extraction.
    import zipfile
    archive_root=ROOT/'docs/research-archives/photo-prompt';members=0
    for name,seal_name in [('h-f2-operating-source.zip','SOURCE-LOCK.json'),('source-review-and-lane-experiments.zip','EXPERIMENT-LOCK.json')]:
        seal=state.read(archive_root/seal_name)
        with bundles.joined_archive(archive_root/name,seal) as joined:
            if state.sha(joined)!=seal['archive_sha256']:raise ValueError('source archive changed')
            with zipfile.ZipFile(joined) as archive:
                for info in archive.infolist():
                    members+=1
                    if info.filename.endswith('.pyc'):unknown.append({'file':name+':'+info.filename})
                    if not info.filename.endswith('.py'):continue
                    raw=archive.read(info)
                    if hashlib.sha256(raw).hexdigest()!=seal['files'][info.filename]['sha256']:raise ValueError('archive member changed')
                    for m in names.finditer(raw.decode()):direct.append({'file':name+':'+info.filename,'cache':m.group()})
                    if generic.search(raw.decode()):unknown.append({'file':name+':'+info.filename})
    result={'python_files':python_files,'runtime_metadata_files':metadata,'archive_members':members,
        'direct_cache_references':direct,'unresolved_consumers':unknown,'generic_cache_lines':hits,
        'scope':'known protected sources and two sealed source archives; no all-history CLI claim',
        'unresolved_old_runs_preserved':41,'cache_code_executions':0}
    if refine:result['additional_review']='Probe line 44 creates a private source/output.pyc; line 45 compiles without executing; line 46 reads only that private output. Original cached code is never loaded/executed.'
    new(E/('REFERENCE-CLOSURE-FINAL.json' if refine else 'REFERENCE-CLOSURE.json'),result);return result


def capture_toolchain():
    code="""import sys,json,hashlib,sysconfig,importlib.util,importlib.metadata
from pathlib import Path
import pytest
from _pytest.assertion import rewrite
files=set()
for name in ('pytest','pluggy','packaging','iniconfig','pygments'):
 d=importlib.metadata.distribution(name)
 files.update(Path(d.locate_file(p)).resolve() for p in d.files or [] if str(p).endswith(('.py','.so','METADATA')))
files.update(Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m,'__file__',None) and str(m.__file__).endswith(('.py','.so')))
files.add(Path(sys.executable).resolve())
library=Path(sys.base_prefix)/'Python'
if library.is_file():files.add(library.resolve())
print(json.dumps({'python':sys.version,'magic':importlib.util.MAGIC_NUMBER.hex(),'pytest':pytest.__version__,'executable':sys.executable,'files':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}}))
"""
    p=subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile(),str(PYTHON),'-I','-c',code],
        env=checks.environment(),capture_output=True,text=True,check=True,timeout=60)
    result=json.loads(p.stdout)
    if result['pytest']!='9.0.3' or result['magic']!='2b0e0d0a':raise ValueError('matching toolchain unavailable')
    new(E/'TOOLCHAIN.json',result);return result


def check_toolchain(toolchain):
    for name,digest in toolchain['files'].items():
        if state.sha(name)!=digest:raise ValueError('pinned compiler/pytest dependency changed: '+name)


def compile_child(spec,destination):
    value=state.read(spec);check_toolchain(value['toolchain'])
    from _pytest.assertion.rewrite import _rewrite_test,_write_pyc_fp,_read_pyc
    for row in value['rows']:
        source=Path(row['private_source'])
        with tempfile.TemporaryDirectory(prefix='pytest-source-') as temp:
            copy=Path(temp)/'source.py';copy.write_bytes(source.read_bytes())
            stamp=int.from_bytes(bytes.fromhex(row['header_hex'])[8:12],'little')
            os.utime(copy,(stamp,stamp))
            class FrozenSource:
                def __fspath__(self):return str(copy)
                def __str__(self):return row['compiled_filename']
                def read_bytes(self):return copy.read_bytes()
            buffer=io.BytesIO()
            _write_pyc_fp(buffer,copy.stat(),_rewrite_test(FrozenSource(),None)[1])
            raw=buffer.getvalue()
            if hashlib.sha256(raw).hexdigest()!=row['sha256'] or len(raw)!=row['bytes']:raise ValueError('whole pytest cache differs')
            target=Path(destination)/row['path'];target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('xb') as stream:stream.write(raw)
            target.chmod(row['mode'])
            if _read_pyc(copy,target) is None:raise ValueError('pytest cannot read its regenerated cache')


def compile_rows(rows,destination,read_denials='',toolchain=None):
    destination=Path(destination)
    if destination.exists() or destination.is_symlink():raise FileExistsError('destination exists')
    names=[r['path'] for r in rows]
    if not rows or len(names)!=len(set(names)):raise ValueError('empty or duplicate recovery list')
    for row in rows:
        bundles.safe_name(row['path'])
        if not re.fullmatch('[0-9a-f]{40}',row['git_blob']):raise ValueError('invalid Git object')
    toolchain=toolchain or state.read(E/'TOOLCHAIN.json');check_toolchain(toolchain)
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.pytest-recompile-',dir=destination.parent) as temp:
        temp=Path(temp);staged=temp/'root';staged.mkdir();sources={};spec=[]
        for row in rows:
            oid=row['git_blob']
            if oid not in sources:
                raw=git('cat-file','blob',oid,read_denials=read_denials)
                if hashlib.sha256(raw).hexdigest()!=row['source_sha256']:raise ValueError('source blob differs')
                source=temp/(oid+'.py');source.write_bytes(raw);sources[oid]=source
            spec.append({**row,'private_source':str(sources[oid])})
        specification=temp/'spec.json';state.write(specification,{'rows':spec,'toolchain':toolchain})
        launch="import sys,runpy;from pathlib import Path;p=sys.argv.pop(1);sys.path.insert(0,str(Path(p).parent));runpy.run_path(p,run_name='__main__')"
        subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile()+read_denials,str(PYTHON),'-I','-c',launch,
            str(Path(__file__).resolve()),'child',str(specification),str(staged)],env=checks.environment(),check=True,timeout=120)
        publish_exclusive(staged,destination)
    return destination


def load_lock():
    final=(E/'STAGE02-FINAL.json').exists()
    checkpoint=state.read(E/('STAGE02-FINAL.json' if final else 'STAGE02.json'))
    path=E/('RESTORE-LOCK-v2.json.gz' if final else 'RESTORE-LOCK.json.gz')
    if state.sha(path)!=checkpoint['lock_sha256']:raise ValueError('recompile lock changed')
    if state.sha(E/'TOOLCHAIN.json')!=checkpoint['toolchain_sha256']:raise ValueError('toolchain seal changed')
    return state.read(path)


def prove(refine=False):
    checkpoint=E/('STAGE02-FINAL.json' if refine else 'STAGE02.json')
    if checkpoint.exists():raise FileExistsError('stage 2 already sealed')
    refs=scan_references(refine)
    toolchain=state.read(E/'TOOLCHAIN.json') if refine else capture_toolchain()
    check_toolchain(toolchain);rows=[];deferred=[]
    paths=sorted({r['analysis']['source'] for r in targets()})
    log=git('log','--all','--format=COMMIT:%H','--raw','--no-abbrev','--no-renames','--',*paths).decode()
    new_blobs={};old_blobs={};commit=None
    for line in log.splitlines():
        if line.startswith('COMMIT:'):commit=line[7:]
        elif line.startswith(':'):
            fields,path=line.split('\t',1);old,latest=fields.split()[2:4]
            if latest.strip('0'):new_blobs.setdefault((path,latest),commit)
            if old.strip('0'):old_blobs.setdefault((path,old),[]).append(commit)
    head=git('rev-parse','HEAD').decode().strip()
    for target in targets():
        row=target['analysis'];match=row['matches'][0];source=row['source'];reason=None
        if target['preflight']!='READY' or state.stamp(ROOT/target['path'])!=target['before']:reason='changed target'
        if refs['unresolved_consumers'] or refs['direct_cache_references']:reason='unresolved cache consumer'
        if match['origin']=='current':
            oid=git('rev-parse',head+':'+source).decode().strip();commit=head
        else:
            oid=match['git_blob'];commit=new_blobs.get((source,oid))
            if not commit:
                for change in old_blobs.get((source,oid),[]):
                    for parent in git('rev-list','--parents','-n','1',change).decode().split()[1:]:
                        try:found=git('rev-parse',parent+':'+source).decode().strip()
                        except subprocess.CalledProcessError:continue
                        if found==oid:commit=parent;break
                    if commit:break
        if not commit:reason='source commit unavailable'
        if reason:deferred.append({'path':target['path'],'reason':reason});continue
        if git('rev-parse',commit+':'+source).decode().strip()!=oid:raise ValueError('tree/blob binding differs')
        if hashlib.sha256(git('cat-file','blob',oid)).hexdigest()!=match['source_sha256']:raise ValueError('source differs')
        rows.append({'path':target['path'],'batch':target['batch'],'sha256':row['sha256'],'bytes':row['bytes'],
            'mode':target['before']['mode'],'git_commit':commit,'git_blob':oid,'source_path':source,
            'source_sha256':match['source_sha256'],'header_hex':row['header_hex'],'compiled_filename':row['compiled_filename']})
    if rows:
        with tempfile.TemporaryDirectory(prefix='pytest-proof-') as temp:compile_rows(rows,Path(temp)/'restored',toolchain=toolchain)
    lock_path=E/('RESTORE-LOCK-v2.json.gz' if refine else 'RESTORE-LOCK.json.gz')
    new(lock_path,{'schema':'photo-pytest-recompile/v1','rows':rows,'deferred':deferred})
    new(checkpoint,{'status':'PASS' if not deferred else 'PASS_WITH_DEFERRED','eligible':len(rows),
        'deferred':deferred,'whole_bytes_recompiled':len(rows),'pytest_reader_checks':len(rows),
        'lock_sha256':state.sha(lock_path),'toolchain_sha256':state.sha(E/'TOOLCHAIN.json'),
        'dependency_files':len(toolchain['files']),'cache_code_executions':0,'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 2 PASS;',len(rows),'exact pytest cache files;',len(deferred),'deferred',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('command',choices=['prove','refine','restore','child']);p.add_argument('spec',nargs='?');p.add_argument('destination',nargs='?');a=p.parse_args()
    if a.command in ('prove','refine'):prove(a.command=='refine')
    elif a.command=='restore':compile_rows(load_lock()['rows'],a.spec)
    else:compile_child(a.spec,a.destination)
