"""Quarantine only the frozen 65 pytest caches; exact removal follows all final gates."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
import subprocess
import tempfile

import checks
from deferred_gc import atomic, live_revision, rollback
from deferred_restore import publish_exclusive
import pytest_checks as history_checks
import pytest_proof as history_proof
import pytest_restore as history_restore
from pytest_state import E, ROOT, new, targets, verify
import state


def validate_quarantine(folder,rows):
    folder=Path(folder)
    if folder.is_symlink() or not folder.is_dir():raise ValueError('unsafe quarantine root')
    actual={str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file() or p.is_symlink()}
    if actual!={r['path'] for r in rows}:raise ValueError('quarantine has unknown or missing members')
    allowed=set(actual)
    for name in actual:allowed.update(str(p) for p in Path(name).parents if str(p)!='.')
    if {str(p.relative_to(folder)) for p in folder.rglob('*')}!=allowed:
        raise ValueError('quarantine contains an unowned directory')
    for row in rows:
        p=folder/row['path']
        if state.stamp(p)!=row['before']:raise ValueError('quarantined bytes, identity or mode changed')


def preflight(row):
    p=ROOT/row['path'];source=ROOT/row['analysis']['source']
    if row['preflight']!='READY' or state.stamp(p)!=row['before']:raise ValueError('cache changed')
    if p.is_symlink() or p.stat().st_nlink!=1:raise ValueError('cache is linked')
    if state.stamp(source)!=row['source_before']:raise ValueError('source ownership changed')


def quarantine(batch):
    phase=5 if batch=='A' else 6;checkpoint=E/('STAGE0'+str(phase)+'.json')
    journal=E/('JOURNAL-0'+str(phase)+'.json')
    if checkpoint.exists() or journal.exists():raise FileExistsError('batch already started; inspect journal instead of repeating')
    new(E/('BATCH-'+batch+'.LOCK'),{'batch':batch,'policy':'exclusive one-shot; never clear to repeat removal'})
    if state.read(E/'STAGE04.json')['status']!='PASS':raise ValueError('baseline not qualified')
    if batch=='B' and state.read(E/'STAGE05.json')['status'] not in ('PASS','PASS_WITH_DEFERRED'):
        raise ValueError('prior batch not qualified')
    history_restore.load_seal();eligible={r['path'] for r in history_proof.load_lock()['rows']}
    before_absent=set(state.read(E/'ABSENT.json'));revision=live_revision()
    selected=[r for r in targets() if r['batch']==batch and r['path'] in eligible]
    ready=[];deferred=[]
    for row in selected:
        try:preflight(row);ready.append(row)
        except Exception as error:deferred.append({'path':row['path'],'reason':str(error)})
    opened={'targets':len(ready),'exit_code':None}
    if ready:
        p=subprocess.run(['/usr/sbin/lsof','-n','-P','-F','n','--',*[str(ROOT/r['path']) for r in ready]],
            capture_output=True,text=True,timeout=45)
        opened.update(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
        if p.returncode not in (0,1) or p.stderr or any(line.startswith('n') for line in p.stdout.splitlines()):
            deferred.extend({'path':r['path'],'reason':'open file or inconclusive process inspection'} for r in ready)
            ready=[]
    parent=history_checks.QUARANTINE
    for p in (ROOT/'.codex-artifacts',parent):
        if p.is_symlink():raise ValueError('symlink quarantine ancestor')
    parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    folder=Path(tempfile.mkdtemp(prefix=batch+'-',dir=parent))
    moved=[];record={'state':'prepared','batch':batch,'phase':phase,'quarantine':str(folder),
        'planned_paths':[r['path'] for r in ready],'moved':[]}
    atomic(journal,record)
    try:
        for row in ready:
            preflight(row);original=ROOT/row['path'];destination=folder/row['path']
            destination.parent.mkdir(parents=True,exist_ok=True)
            publish_exclusive(original,destination);moved.append((original,destination))
            record['moved']=[str(a.relative_to(ROOT)) for a,b in moved]
            atomic(journal,record)
            atomic(E/'ABSENT.json',sorted(before_absent|set(record['moved'])))
        record['state']='quarantined';atomic(journal,record)
        validate_quarantine(folder,ready)
        if moved:history_checks.suite('absent-'+batch)
        if live_revision()!=revision:raise ValueError('source maintenance revision changed')
        verify(E/('VERIFY-0'+str(phase)+'.json'))
        validate_quarantine(folder,ready)
        record['state']='validated_quarantine';atomic(journal,record)
        new(checkpoint,{'status':'PASS' if not deferred else 'PASS_WITH_DEFERRED',
            'quarantined_files':len(moved),'quarantined_bytes':sum(r['before']['bytes'] for r in ready),
            'removed_files':0,'quarantine_retained':str(folder),'deferred':deferred,
            'process_check':opened,'suite':'SUITE-absent-'+batch+'.json' if moved else None,
            'source_revision_unchanged':True,'Gemini_calls':0,'CURRENT_writes':0})
        print('stage',phase,'PASS;',len(moved),'quarantined;',len(deferred),'deferred; deletion pending final checks',flush=True)
    except BaseException as error:
        collisions=rollback(moved)
        if not collisions:atomic(E/'ABSENT.json',sorted(before_absent))
        record.update(state='restore_collision' if collisions else 'restored_after_failure',
            error=str(error),collisions=collisions);atomic(journal,record)
        new(checkpoint,{'status':'DEFER','reason':str(error),'restore_collisions':collisions,
            'quarantine_retained':str(folder),'removed_files':0,'Gemini_calls':0,'CURRENT_writes':0})
        if not collisions:verify(E/('VERIFY-0'+str(phase)+'-rollback.json'))
        raise


def journals():
    frozen={r['path']:r for r in targets()};result=[]
    for phase in (5,6):
        record=state.read(E/('JOURNAL-0'+str(phase)+'.json'))
        if record['state']!='validated_quarantine':raise ValueError('batch not validated')
        rows=[frozen[p] for p in record['moved']]
        validate_quarantine(record['quarantine'],rows)
        result.append((phase,record,rows))
    return result


def offline_final():
    if (E/'OFFLINE-FINAL.json').exists():raise FileExistsError('offline proof already exists')
    journals();rows=history_proof.load_lock()['rows'];guards=history_checks.denials()
    with tempfile.TemporaryDirectory(prefix='pytest-final-recovery-') as temp:
        temp=Path(temp);zip_root=temp/'zip'
        p=subprocess.run(['/usr/bin/sandbox-exec','-p',checks.profile()+guards,sys.executable,'-B',
            str(Path(history_restore.__file__).resolve()),'restore',str(zip_root)],
            env=checks.environment(),capture_output=True,text=True,timeout=120)
        if p.returncode:raise ValueError('isolated raw-ZIP recovery failed: '+p.stderr[-2000:])
        git_root=history_proof.compile_rows(rows,temp/'git',read_denials=guards)
        for row in rows:
            for root in (zip_root,git_root):
                if state.sha(root/row['path'])!=row['sha256']:
                    raise ValueError('final exact recovery differs')
    origins=sorted({r['git_commit'] for r in rows});outside=[]
    for commit in origins:
        p=subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],capture_output=True)
        if p.returncode==1:outside.append(commit)
        elif p.returncode:raise ValueError('source ancestry check failed')
    new(E/'OFFLINE-FINAL.json',{'status':'PASS','files':len(rows),'original_cache_reads_denied':True,
        'quarantine_reads_denied':True,'ZIP_exact_files':len(rows),'Git_exact_files':len(rows),
        'source_commits':len(origins),'source_commits_on_other_preserved_refs':outside,
        'source_scope':'Git mode needs locked local objects; raw-byte ZIP recovery is independent of those refs and old compilers.',
        'network_denied':True,'Gemini_calls':0,'cache_code_executions':0,'CURRENT_writes':0})
    verify(E/'VERIFY-07-recovery.json')
    print('final offline recovery PASS: ZIP/Git',len(rows),'each; original/quarantine reads denied',flush=True)


def require_final_qualification():
    native=state.read(E/'NATIVE-final.json');offline=state.read(E/'OFFLINE-FINAL.json')
    if native['status']!='PASS' or native['test_count']!=70:
        raise ValueError('final native regression not qualified')
    if re.search(r'skipped=[1-9][0-9]*',native.get('stderr','')):
        raise ValueError('native skipped tests do not qualify final deletion')
    if offline['status']!='PASS' or offline['files']!=65:
        raise ValueError('final offline recovery not qualified')
    if state.read(E/'SUITE-absent-B.json')['status']!='PASS':raise ValueError('last absence suite not qualified')
    safety=state.read(E/'SAFETY-07-FINAL.json')
    if safety['status']!='PASS' or safety['tests']!=53 or safety['failures'] or safety['errors']:
        raise ValueError('final safety tests not qualified')
    independent=state.read(E/'ZIP-INDEPENDENT.json')
    if independent['status']!='PASS' or independent['files']!=65:
        raise ValueError('independent original-byte recovery not qualified')


def delete_verified(folder,rows,after_delete):
    """Only exact members and their known empty parent directories; no rmtree/glob deletion."""
    folder=Path(folder);validate_quarantine(folder,rows)
    directories=set()
    for row in rows:
        p=folder/row['path']
        if state.stamp(p)!=row['before']:raise ValueError('quarantine member changed before unlink')
        p.unlink();after_delete(row['path'])
        directories.update(parent for parent in p.parents if parent!=folder and parent.is_relative_to(folder))
    for directory in sorted(directories,key=lambda p:len(p.parts),reverse=True):directory.rmdir()
    folder.rmdir()


def finalize():
    if (E/'STAGE07.json').exists():raise FileExistsError('final cleanup already recorded')
    require_final_qualification()
    new(E/'FINALIZE.LOCK',{'policy':'exclusive one-shot; inspect journal on failure'})
    active=set(state.read(E/'ABSENT.json'));frozen=targets()
    groups=journals()
    planned={r['path'] for _,_,rows in groups for r in rows}
    if active!=planned or not active<={r['path'] for r in frozen}:raise ValueError('unexpected final target population')
    revision=live_revision();verify(E/'VERIFY-07-pre-delete.json')
    removed=[]
    try:
        for phase,record,rows in groups:
            record['state']='finalizing';atomic(E/('JOURNAL-0'+str(phase)+'.json'),record)
            def deleted(path):
                removed.append(path);atomic(E/'REMOVED.json',sorted(removed))
                record['deleted']=[p for p in removed if p in record['moved']]
                atomic(E/('JOURNAL-0'+str(phase)+'.json'),record)
            delete_verified(record['quarantine'],rows,deleted)
            record.update(state='gc_done',quarantine_absent=True)
            atomic(E/('JOURNAL-0'+str(phase)+'.json'),record)
        history_checks.QUARANTINE.rmdir()
        if live_revision()!=revision:raise ValueError('source revision changed')
        verify(E/'VERIFY-07.json')
        new(E/'STAGE07.json',{'status':'PASS','removed_files':len(removed),
            'removed_logical_bytes':sum(r['before']['bytes'] for r in frozen if r['path'] in removed),
            'native_tests':70,'offline_recovery_files_per_backend':65,
            'last_full_absence_suite':'SUITE-absent-B.json','quarantines_absent':True,
            'Gemini_calls':0,'new_embedding_calls':0,'CURRENT_writes':0})
        print('stage 7 PASS:',len(removed),'original bytecodes removed after all gates',flush=True)
    except BaseException as error:
        # Keep concurrent files. Restore our old bytes through verified private copies only.
        restored=[];collisions=[]
        with tempfile.TemporaryDirectory(prefix='pytest-final-rollback-') as temp:
            backup=history_restore.restore_zip(history_restore.ARCHIVE,history_restore.load_seal(),Path(temp)/'backup')
            for phase,record,rows in groups:
                for row in rows:
                    original=ROOT/row['path'];saved=Path(record['quarantine'])/row['path']
                    if original.exists() or original.is_symlink():collisions.append(row['path']);continue
                    source=saved if saved.exists() and state.stamp(saved)==row['before'] else backup/row['path']
                    try:publish_exclusive(source,original);restored.append(row['path'])
                    except OSError:collisions.append(row['path'])
        new(E/'STAGE07.json',{'status':'DEFER','reason':str(error),'deleted_before_failure':removed,
            'restored_original_bytes':restored,'restore_collisions_preserved':collisions,
            'scope':'ZIP-restored target inodes can differ; frozen non-target protection is not relaxed',
            'Gemini_calls':0,'CURRENT_writes':0})
        raise


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('batch',choices=['A','B','recovery','final']);a=p.parse_args()
    if a.batch=='recovery':offline_final()
    elif a.batch=='final':finalize()
    else:quarantine(a.batch)
