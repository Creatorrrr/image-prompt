"""Quarantine only frozen candidates; validate absence before deleting our quarantine."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import deferred_checks
from deferred_replay import replay
from deferred_restore import publish_exclusive
from deferred_state import E, ROOT, verify
import state


def atomic(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
    with tempfile.NamedTemporaryFile(prefix='.transaction-',dir=path.parent,delete=False) as stream:
        temporary=Path(stream.name);stream.write(raw);stream.flush();os.fsync(stream.fileno())
    os.replace(temporary,path)


def rollback(moved):
    collisions=[]
    for original,quarantined in reversed(moved):
        if original.exists() or original.is_symlink():collisions.append(str(original));continue
        try:publish_exclusive(quarantined,original)
        except OSError:collisions.append(str(original))
    return collisions


def live_revision():
    binding={'schema':'photo-native-runtime-namespace/v3','root':str(ROOT/'skills/photo-prompt-image-generator'),
             'mode':'local_current','remote':''}
    key=hashlib.sha256(json.dumps(binding,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    path=state.SHARED/'local'/key/'SOURCE.json'
    value=state.read(path) if path.exists() else None
    if value and value.get('editing'):raise ValueError('cooperative source maintenance is active')
    return value


def preflight(rows,folder=None):
    for row in rows:
        p=ROOT/row['path']
        if row['preflight']!='READY' or p.is_symlink() or state.stamp(p)!=row['before']:
            raise ValueError('target changed since freeze: '+row['path'])
        if p.stat().st_nlink!=1:raise ValueError('linked target: '+row['path'])
    if folder:
        base=ROOT/folder
        if base.is_symlink():raise ValueError('symlink shard directory')
        actual={str(p.relative_to(ROOT)) for p in base.rglob('*') if p.is_file() or p.is_symlink()}
        if actual!={r['path'] for r in rows}:raise ValueError('shard has unknown or missing members')
        command=['/usr/sbin/lsof','-n','-P','-F','n','+D',str(base)]
    else:
        command=['/usr/sbin/lsof','-n','-P','-F','n','--',*[str(ROOT/r['path']) for r in rows]]
    opened=subprocess.run(command,capture_output=True,text=True,timeout=45)
    if opened.returncode not in (0,1) or opened.stderr or any(s.startswith('n') for s in opened.stdout.splitlines()):
        raise ValueError('target is open or process inspection incomplete')
    return {'lsof_exit':opened.returncode,'opened_targets':0,'target_files':len(rows)}


def execute(phase,batch=None):
    checkpoint=E/('STAGE'+str(phase).zfill(2)+'.json')
    if checkpoint.exists():raise ValueError('stage already completed; never repeat removal')
    journal=E/('JOURNAL-'+str(phase).zfill(2)+'.json')
    if journal.exists() and Path(state.read(journal)['quarantine']).exists():
        raise ValueError('prior quarantine exists; inspect/recover before another attempt')
    frozen=state.read(E/'TARGETS.json.gz');previous=set(state.read(E/'REMOVED.json'));revision=live_revision()
    parent=ROOT/'.codex-artifacts';parent.mkdir(exist_ok=True)
    quarantine=Path(tempfile.mkdtemp(prefix='photo-deferred-quarantine-',dir=parent))
    moved=[];removed=[];deferred=[];opened=[]
    record={'state':'prepared','quarantine':str(quarantine),'moved':[],'phase':phase}
    atomic(journal,record)
    try:
        if batch is None:
            groups=[{'id':'bytecode','path':None}]
        else:
            groups=[r for r in frozen['shards'] if r['batch']==batch]
        for group in groups:
            group_rows=[r for r in frozen['targets'] if r['group']==group['id']]
            local=[]
            try:
                if batch is not None:
                    baseline=E/('REPLAY-baseline-'+group['id'][:12]+'.json')
                    if state.read(baseline)['status']!='PASS':raise ValueError('historical baseline did not pass')
                    refs=next(r for r in state.read(E/'REFERENCE-CLOSURE.json')['groups'] if r['id']==group['id'])
                    if refs['missing_references']:raise ValueError('historical references unresolved')
                opened.append({'group':group['id'],**preflight(group_rows,group['path'])})
                originals=[ROOT/group['path']] if group['path'] else [ROOT/r['path'] for r in group_rows]
                for original in originals:
                    target=quarantine/original.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
                    publish_exclusive(original,target);local.append((original,target));moved.append((original,target))
                    record['moved']=[{'original':str(a.relative_to(ROOT)),'quarantined':str(b.relative_to(quarantine))} for a,b in moved]
                    atomic(journal,record)
                removed.extend(r['path'] for r in group_rows)
                atomic(E/'REMOVED.json',sorted(previous|set(removed)))
                if batch is not None:replay(group['id'],'absent-'+str(phase),'git')
            except Exception as error:
                collisions=rollback(local)
                if collisions:raise RuntimeError('restore collision; quarantine retained: '+str(collisions)) from error
                localset=set(local);moved=[p for p in moved if p not in localset]
                rels={r['path'] for r in group_rows};removed=[p for p in removed if p not in rels]
                atomic(E/'REMOVED.json',sorted(previous|set(removed)))
                deferred.append({'group':group['id'],'reason':str(error)})
                record['moved']=[{'original':str(a.relative_to(ROOT)),'quarantined':str(b.relative_to(quarantine))} for a,b in moved]
                atomic(journal,record)
                print('DEFER:',group['id'],str(error),flush=True)
        record['state']='quarantined';atomic(journal,record)
        label='absent-'+str(phase)
        if removed:
            deferred_checks.suite(label,managed=batch is not None)
        if live_revision()!=revision:raise ValueError('source revision changed during cleanup')
        verify(E/('VERIFY-'+str(phase).zfill(2)+'.json'))
        expected={r['path']:r for r in frozen['targets'] if r['path'] in removed}
        actual={str(p.relative_to(quarantine)) for p in quarantine.rglob('*') if p.is_file() or p.is_symlink()}
        if actual!=set(expected):raise ValueError('quarantine has unowned or missing files')
        for rel,row in expected.items():
            p=quarantine/rel
            if p.is_symlink() or p.stat().st_nlink!=1 or state.sha(p)!=row['expected_sha256']:
                raise ValueError('quarantined member changed')
        record['state']='validated';atomic(journal,record)
        shutil.rmtree(quarantine)
    except BaseException as error:
        collisions=rollback(moved)
        if not collisions:atomic(E/'REMOVED.json',sorted(previous))
        record.update(state='restore_collision' if collisions else 'restored_after_failure',error=str(error),collisions=collisions)
        atomic(journal,record)
        state.write(checkpoint,{'status':'DEFER','reason':str(error),'restore_collisions':collisions,'removed_files':0,
            'quarantine_retained':str(quarantine),'Gemini_calls':0,'CURRENT_writes':0})
        print('stage',phase,'DEFER; no further removal',flush=True)
        return
    record.update(state='gc_done',quarantine_absent=not quarantine.exists());atomic(journal,record)
    state.write(checkpoint,{'status':'PASS' if not deferred else 'PASS_WITH_DEFERRED','removed_files':len(removed),
        'removed_logical_bytes':sum(r['before']['bytes'] for r in frozen['targets'] if r['path'] in removed),
        'deferred':deferred,'process_checks':opened,'quarantine_absent':not quarantine.exists(),
        'source_revision_unchanged':True,'absence_suite':label if removed else None,'Gemini_calls':0,'CURRENT_writes':0})
    print('stage',phase,'complete;',len(removed),'files removed;',len(deferred),'groups deferred',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('phase',type=int,choices=[4,5,6]);a=p.parse_args()
    execute(a.phase,None if a.phase==4 else a.phase-4)
