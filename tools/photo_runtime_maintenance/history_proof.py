"""Trace bounded cache consumers and recompile locked historical Git source offline."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import py_compile
import re
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parent))
import bundles
import checks
from deferred_restore import publish_exclusive
from history_state import E, ROOT, new, targets
import state

BINARIES = {'cb0d0d0a':Path('/opt/homebrew/bin/python3.12'),
            '2b0e0d0a':Path('/opt/homebrew/bin/python3.14')}


def git(*args,read_denials=''):
    return subprocess.check_output(['/usr/bin/sandbox-exec','-p',
        checks.profile()+read_denials,'git','--no-lazy-fetch','-C',str(ROOT),*args],
        env=dict(os.environ,GIT_NO_LAZY_FETCH='1'),timeout=120)


def scan_references():
    baseline=state.read(E/'BASELINE.json.gz');rows=targets()
    literals=re.compile('|'.join(re.escape(Path(r['path']).name) for r in rows))
    generic=re.compile(r'SourcelessFileLoader|cache_from_source|marshal\.loads|marshal\.load\(|\.pyc')
    hits=[];direct=[];files=0;metadata=0;archive_members=0
    reviewed = {'verify_five_case_artifacts.py','merge_authored_hair.py','reproduce.py',
        'verify_final_tool.py','finalize_evidence.py','test_photo_visual_profile_shards.py',
        'prepare_publication.py','bytecode_regeneration_probe.py','verify_history_bytecodes.py',
        'write_report.py','bytecode_gc.py','deferred_restore.py','classify.py'}
    for name,stamp in baseline['files'].items():
        p=Path(name)
        if stamp.get('kind')!='file':continue
        is_python=p.suffix=='.py'
        is_metadata=p.name in ('manifest.json','CURRENT.json','workflow.json')
        if not (is_python or is_metadata):continue
        text=p.read_text(errors='replace')
        if is_python:
            files+=1
            for number,line in enumerate(text.splitlines(),1):
                if generic.search(line):
                    category='inspection_or_copy_filter' if p.name in reviewed else 'UNRESOLVED'
                    hits.append({'file':name,'line':number,'text':line.strip(),'classification':category})
        else:metadata+=1
        for match in literals.finditer(text):
            direct.append({'file':name,'cache_name':match.group(),'kind':'source' if is_python else 'runtime_metadata'})
    archive_root=ROOT/'docs/research-archives/photo-prompt'
    for name,lock_name in [('h-f2-operating-source.zip','SOURCE-LOCK.json'),
                           ('source-review-and-lane-experiments.zip','EXPERIMENT-LOCK.json')]:
        seal=state.read(archive_root/lock_name)
        with bundles.joined_archive(archive_root/name,seal) as archive:
            if state.sha(archive)!=seal['archive_sha256']:raise ValueError('source archive changed')
            with zipfile.ZipFile(archive) as z:
                for member in z.infolist():
                    archive_members+=1
                    if member.filename.endswith('.pyc'):raise ValueError('opaque bytecode member in replay archive')
                    if not member.filename.endswith('.py'):continue
                    raw=z.read(member)
                    if hashlib.sha256(raw).hexdigest()!=seal['files'][member.filename]['sha256']:
                        raise ValueError('archive source member changed')
                    for match in literals.finditer(raw.decode(errors='replace')):
                        direct.append({'file':name+':'+member.filename,'cache_name':match.group(),'kind':'archived_source'})
                    for number,line in enumerate(raw.decode(errors='replace').splitlines(),1):
                        if generic.search(line):
                            hits.append({'file':name+':'+member.filename,'line':number,'text':line.strip(),
                                'classification':'UNRESOLVED_ARCHIVE_CACHE_CONSUMER'})
    # Known diagnostics inspect or exclude caches; they do not execute sourceless inputs.
    unresolved=[r for r in hits if r['classification'].startswith('UNRESOLVED')]
    result={'python_files':files,'runtime_metadata_files':metadata,'archive_members':archive_members,
        'cache_aware_lines':hits,'direct_cache_references':direct,'unresolved_consumers':unresolved,
        'scope':'known protected source, sealed code and two verified source archives; no all-history CLI claim',
        'ordinary_import_rule':'PEP 3147 __pycache__ alone is not an ordinary source-less module',
        'old_run_bindings':len(state.read(state.EVIDENCE/'RUN-BINDINGS.json.gz')['rows']),
        'old_unresolved_runs_preserved':41}
    new(E/'REFERENCE-CLOSURE.json',result)
    return result


def compile_child(specification,destination):
    for row in state.read(specification):
        source=Path(row['source']);raw=source.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=row['source_sha256']:raise ValueError('source changed')
        header=bytes.fromhex(row['header_hex'])
        if header[:4]!=importlib.util.MAGIC_NUMBER or header[4:8]!=b'\0'*4:
            raise ValueError('interpreter or invalidation mode differs')
        with tempfile.TemporaryDirectory(prefix='history-source-') as temp:
            copy=Path(temp)/'source.py';copy.write_bytes(raw)
            stamp=int.from_bytes(header[8:12],'little');os.utime(copy,(stamp,stamp))
            target=Path(destination)/row['path'];target.parent.mkdir(parents=True,exist_ok=True)
            py_compile.compile(str(copy),cfile=str(target),dfile=row['compiled_filename'],
                doraise=True,optimize=row['optimization'],invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP)
        if state.sha(target)!=row['sha256'] or target.stat().st_size!=row['bytes']:
            raise ValueError('whole cache bytes differ: '+row['path'])
        target.chmod(row['mode'])


def compile_rows(rows,destination,read_denials=''):
    destination=Path(destination)
    if destination.exists() or destination.is_symlink():raise FileExistsError('recovery destination exists')
    names=[r['path'] for r in rows]
    if not names or len(names)!=len(set(names)):raise ValueError('empty or duplicate recovery names')
    for row in rows:
        bundles.safe_name(row['path'])
        if not re.fullmatch('[0-9a-f]{40}',row['git_blob']):raise ValueError('invalid Git object identity')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.history-compile-',dir=destination.parent) as temp:
        temp=Path(temp);staged=temp/'root';staged.mkdir();groups={};sources={}
        for row in rows:
            oid=row['git_blob']
            if oid not in sources:
                raw=git('cat-file','blob',oid,read_denials=read_denials)
                if hashlib.sha256(raw).hexdigest()!=row['source_sha256']:raise ValueError('source blob differs')
                source=temp/(oid+'.py');source.write_bytes(raw);sources[oid]=source
            spec={**row,'source':str(sources[oid])}
            groups.setdefault(row['header_hex'][:8],[]).append(spec)
        for magic,spec in groups.items():
            binary=BINARIES[magic];expected=spec[0].get('interpreter_sha256')
            if expected and state.sha(binary.resolve())!=expected:raise ValueError('recovery interpreter changed')
            path=temp/(magic+'.json');state.write(path,spec)
            launch="import sys,runpy;from pathlib import Path;p=sys.argv.pop(1);sys.path.insert(0,str(Path(p).parent));runpy.run_path(p,run_name='__main__')"
            subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile()+read_denials,str(binary),'-I','-c',launch,
                str(Path(__file__).resolve()),'compile-child',str(path),str(staged)],
                env=checks.environment(),check=True,timeout=120)
        publish_exclusive(staged,destination)
    return destination


def prove():
    if (E/'STAGE02.json').exists():raise FileExistsError('stage 2 already sealed')
    refs=scan_references();rows=targets();paths=sorted({r['analysis']['source'] for r in rows})
    raw=git('-c','core.quotePath=false','log','--all','--format=COMMIT:%H','--raw','--no-abbrev','--no-renames','--',*paths).decode()
    commits={};commit=None
    for line in raw.splitlines():
        if line.startswith('COMMIT:'):commit=line[7:]
        elif line.startswith(':'):
            fields,path=line.split('\t',1);blob=fields.split()[3]
            if blob.strip('0'):commits.setdefault((path,blob),commit)
    recovery=[];deferred=[]
    for target in rows:
        row=target['analysis'];reason=None
        if target['preflight']!='READY' or state.stamp(ROOT/target['path'])!=target['before']:reason='changed target'
        if refs['unresolved_consumers']:reason='unresolved generic cache consumer; preserve until reviewed'
        if any(r['cache_name']==Path(target['path']).name for r in refs['direct_cache_references']):
            reason='direct source/runtime cache reference requires review'
        match=row['matches'][0];commit=commits.get((row['source'],match['git_blob']))
        if not commit:reason='source commit unavailable'
        if reason:deferred.append({'path':target['path'],'reason':reason});continue
        if git('rev-parse',commit+':'+row['source']).decode().strip()!=match['git_blob']:
            raise ValueError('commit/tree/blob relationship differs')
        binary=BINARIES[row['magic']]
        opt=re.search(r'\.opt-([012])\.pyc$',row['path'])
        recovery.append({'path':target['path'],'batch':target['batch'],'sha256':row['sha256'],
            'bytes':row['bytes'],'mode':target['before']['mode'],'git_commit':commit,
            'git_blob':match['git_blob'],'source_path':row['source'],'source_sha256':match['source_sha256'],
            'header_hex':row['header_hex'],'compiled_filename':row['compiled_filename'],
            'optimization':int(opt.group(1)) if opt else 0,'interpreter':str(binary),
            'interpreter_sha256':state.sha(binary.resolve())})
    if recovery:
        with tempfile.TemporaryDirectory(prefix='history-proof-') as temp:
            restored=compile_rows(recovery,Path(temp)/'compiled')
            if any(state.sha(restored/r['path'])!=r['sha256'] for r in recovery):raise ValueError('regeneration differs')
    new(E/'RESTORE-LOCK.json.gz',{'schema':'photo-history-bytecode-restore/v1','rows':recovery,'deferred':deferred})
    new(E/'STAGE02.json',{'status':'PASS' if not deferred else 'PASS_WITH_DEFERRED',
        'eligible':len(recovery),'deferred':deferred,'whole_bytes_recompiled':len(recovery),
        'lock_sha256':state.sha(E/'RESTORE-LOCK.json.gz'),'references':{k:refs[k] for k in
            ('python_files','runtime_metadata_files','archive_members')},'cache_code_executions':0,
        'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 2:',len(recovery),'exactly recompiled;',len(deferred),'deferred',flush=True)


def load_lock():
    final=E/'STAGE02-FINAL.json'
    checkpoint=state.read(final if final.exists() else E/'STAGE02.json')
    path=E/('RESTORE-LOCK-v2.json.gz' if final.exists() else 'RESTORE-LOCK.json.gz')
    if state.sha(path)!=checkpoint['lock_sha256']:raise ValueError('sealed source recovery lock changed')
    return state.read(path)


def refine_parent_commits():
    """A deletion's parent can bind an old blob omitted by simplified log output."""
    if (E/'STAGE02-FINAL.json').exists():raise FileExistsError('source refinement already sealed')
    original=load_lock();pending=original['deferred']
    if any(r['reason']!='source commit unavailable' for r in pending):
        raise ValueError('do not reinterpret unresolved references as source provenance')
    by_path={r['path']:r for r in targets()};paths=[by_path[r['path']]['analysis']['source'] for r in pending]
    raw=git('-c','core.quotePath=false','log','--all','--format=COMMIT:%H','--raw','--no-abbrev','--no-renames','--',*paths).decode()
    parents={};commit=None
    for line in raw.splitlines():
        if line.startswith('COMMIT:'):commit=line[7:]
        elif line.startswith(':'):
            fields,path=line.split('\t',1);old=fields.split()[2]
            if old.strip('0'):parents.setdefault((path,old),[]).append(commit)
    added=[];remaining=[]
    for item in pending:
        target=by_path[item['path']];row=target['analysis'];match=row['matches'][0];found=None
        for change in parents.get((row['source'],match['git_blob']),[]):
            for parent in git('rev-list','--parents','-n','1',change).decode().split()[1:]:
                try:blob=git('rev-parse',parent+':'+row['source']).decode().strip()
                except subprocess.CalledProcessError:continue
                if blob==match['git_blob']:found=parent;break
            if found:break
        if not found:remaining.append(item);continue
        if state.stamp(ROOT/item['path'])!=target['before']:raise ValueError('cache changed during provenance refinement')
        binary=BINARIES[row['magic']]
        added.append({'path':target['path'],'batch':target['batch'],'sha256':row['sha256'],
            'bytes':row['bytes'],'mode':target['before']['mode'],'git_commit':found,
            'git_blob':match['git_blob'],'source_path':row['source'],'source_sha256':match['source_sha256'],
            'header_hex':row['header_hex'],'compiled_filename':row['compiled_filename'],
            'optimization':0,'interpreter':str(binary),'interpreter_sha256':state.sha(binary.resolve())})
    if added:
        with tempfile.TemporaryDirectory(prefix='history-parent-proof-') as temp:
            compile_rows(added,Path(temp)/'compiled')
    rows=sorted(original['rows']+added,key=lambda r:r['path'])
    new(E/'RESTORE-LOCK-v2.json.gz',{'schema':'photo-history-bytecode-restore/v1','rows':rows,'deferred':remaining})
    new(E/'STAGE02-FINAL.json',{'status':'PASS' if not remaining else 'PASS_WITH_DEFERRED',
        'eligible':len(rows),'deferred':remaining,'whole_bytes_recompiled':len(rows),
        'additional_parent_tree_bindings':len(added),'prior_evidence_preserved':'STAGE02.json',
        'lock_sha256':state.sha(E/'RESTORE-LOCK-v2.json.gz'),'Gemini_calls':0,'CURRENT_writes':0})
    print('stage 2 final:',len(rows),'exact caches;',len(added),'parent-tree bindings;',len(remaining),'deferred',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('command',choices=['prove','refine','restore','compile-child'])
    p.add_argument('specification',nargs='?');p.add_argument('destination',nargs='?');a=p.parse_args()
    if a.command=='prove':prove()
    elif a.command=='refine':refine_parent_commits()
    elif a.command=='restore':compile_rows(load_lock()['rows'],Path(a.specification))
    else:compile_child(a.specification,a.destination)
