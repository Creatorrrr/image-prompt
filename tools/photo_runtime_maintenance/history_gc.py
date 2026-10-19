"""Quarantine frozen bytecodes in two batches; delete only after final qualification."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile

from deferred_gc import atomic, live_revision, rollback
from deferred_restore import publish_exclusive
import history_checks
import history_proof
import history_restore
from history_state import E, ROOT, new, targets, verify
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


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('batch',choices=['A','B']);a=p.parse_args()
    quarantine(a.batch)
