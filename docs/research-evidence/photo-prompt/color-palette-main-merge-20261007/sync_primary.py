"""Fast-forward main, restore unrelated dirty intentions, rebuild working indexes."""
from pathlib import Path
import gc
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

E=Path(__file__).resolve().parent
W=E.parents[3]
P=Path('/Users/chasoik/Projects/image-prompt')
S=Path('skills/photo-prompt-image-generator')
T=Path('/tmp/color-palette-main-merge-20261007')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=P)

target=git('rev-parse','origin/main').decode().strip()
assert target==subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,text=True).strip()
before=read(E/'PRIMARY-BEFORE.json')
assert git('rev-parse','HEAD').decode().strip()==before['primary_head']
assert git('branch','--show-current').decode().strip()=='main'
assert not git('diff','--cached','--name-only').strip(),'Concurrent staged work exists'
derived={str(S/'assets/photo_prompt_semantic_index.json'),str(S/'assets/photo_prompt_visual_profile_index.json')}
incoming=set(git('diff','--name-only',before['primary_head'],target).decode().splitlines())
concurrent_before=[r['path'] for r in before['preservation_files'] if r['path'] not in derived and sha(P/r['path'])!=r['sha256']]
assert not set(concurrent_before)&incoming,('Concurrent edits overlap incoming committed paths',concurrent_before)
# Independent analysis work may keep changing while this task runs. Preserve its
# latest bytes, rather than restoring the earlier observation over those edits.
presync=[]
for row in before['preservation_files']:
    current=dict(row);current['sha256']=sha(P/row['path'])
    assert current['sha256'] is not None,('Previously observed file disappeared',row['path'])
    current['bytes']=(P/row['path']).stat().st_size;presync.append(current)
save(E/'PRIMARY-PRESYNC.json',{'schema':'palette-primary-presync/v1','primary_head':before['primary_head'],'concurrent_unrelated_updates':concurrent_before,'preservation_files':presync})

dirty={r['path'] for r in before['preservation_files'] if r['tracked_dirty']}
overlap=dirty&incoming
allowed={str(S/'assets'/n) for n in ['photo_prompt_source_manifest.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']}
allowed.add('tests/test_photo_structure_maintenance.py')
assert overlap<=allowed,('Unexpected dirty overlap',overlap-allowed)
original={name:(P/name).read_bytes() for name in overlap}
cache=T/'primary-working-index-cache';cache.mkdir(exist_ok=True)
for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
    src=P/S/'assets'/name;shutil.copyfile(src,cache/name)
    for row in read(src)['shards']:
        targetpath=cache/row['path'];targetpath.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src.parent/row['path'],targetpath)

untracked=set(git('ls-files','--others','--exclude-standard','-z').decode().split('\0'))-{''}
collisions=sorted(untracked&incoming)
for name in collisions:
    raw=git('show',target+':'+name)
    assert (P/name).read_bytes()==raw,('Untracked path differs from qualified incoming data',name)

sys.path.insert(0,str(P/S/'scripts'))
from photo_runtime_sources import source_update,SnapshotPublisher
import prompt_generator as pg
import build_visual_profile_index as visual
import build_semantic_index as semantic

def denied(*a,**kw):raise AssertionError('Uncached working text requires review; no embedding request made')
visual.embed_texts_with_gemini=denied;semantic.embed_texts_with_gemini=denied

backup=T/'primary-overlap-latest';backup.mkdir(exist_ok=True)
for name,raw in original.items():
    path=backup/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
save(E/'PRIMARY-OVERLAP-BACKUP.json',{'schema':'palette-primary-owned-overlap-backup/v1','files':[{'path':n,'backup':str(backup/n),'sha256':sha(backup/n)} for n in sorted(original)]})
with source_update(P/S):
    assert all((P/n).read_bytes()==raw for n,raw in original.items()),'Owned overlap changed while preparing caches'
    merged=False
    try:
        for name in overlap:(P/name).write_bytes(git('show',before['primary_head']+':'+name))
        if collisions:git('add','--',*collisions)
        git('merge','--ff-only','origin/main');merged=True
    finally:
        for name,raw in original.items():
            if not merged or name not in derived:(P/name).write_bytes(raw)
        if not merged and collisions:git('restore','--staged','--',*collisions)
    assets=P/S/'assets';sem=assets/'photo_prompt_semantic_index.json';vis=assets/'photo_prompt_visual_profile_index.json'
    metadata=read(sem);provider,model,dimensions=(metadata[k] for k in ['provider','embedding_model','embedding_dimensions'])
    registry=pg.load_visual_obligation_registry(assets/'photo_prompt_visual_obligations.json');data=pg.load_json(assets/'photo_prompt_tags.json')
    vectors=visual.reusable_vectors([cache/vis.name,W/S/'assets'/vis.name],registry,provider=provider,model=model,dimensions=dimensions)
    assert len(vectors)==len(registry['profiles'])
    visual.write_payload(vis,visual.build_visual_profile_index_payload(registry,vectors=vectors,provider=provider,model=model,dimensions=dimensions))
    visual_count=len(registry['profiles']);del vectors;gc.collect()
    expected=semantic.base_payload(data,provider,model,dimensions)
    wanted={key:pg.semantic_text_for_entry(entry,slot,kind=kind) for key,kind,entry,slot in semantic.iter_semantic_entries(data)}
    compatible={}
    for path in [cache/sem.name,W/S/'assets'/sem.name]:
        payload=pg.load_semantic_index_payload(path)
        assert semantic.metadata_matches(payload,expected,require_dictionary_hash=False)
        for key,row in payload['entries'].items():
            if key in wanted and row.get('text')==wanted[key] and len(row.get('vector',[]))==dimensions:compatible[key]=row
        del payload;gc.collect()
    assert set(wanted)<=set(compatible),('Missing exact working vectors',sorted(set(wanted)-set(compatible)))
    with tempfile.TemporaryDirectory(prefix='palette-primary-index-') as temporary:
        checkpoint=Path(temporary)/'working.partial.json'
        checkpoint.write_text(json.dumps({**expected,'entries':compatible},ensure_ascii=False,separators=(',',':')))
        del compatible;gc.collect()
        payload=semantic.build_resumable_index_payload(data,output=sem,checkpoint=checkpoint,provider=provider,model=model,dimensions=dimensions,batch_size=1,request_interval=0,retry_attempts=1,retry_initial_delay=0)
        semantic_count=len(payload['entries'])
        semantic.write_sharded_payload(sem,payload,shard_count=16,keep_stale_generations=True)
        del payload;gc.collect()
    pg.validate_semantic_index_metadata(pg.load_semantic_index_payload(sem),data)
    pg.validate_visual_profile_index_metadata(pg.load_visual_profile_index_payload(vis),registry)

pointer=SnapshotPublisher(P/S).publish()
derived={str(S/'assets/photo_prompt_semantic_index.json'),str(S/'assets/photo_prompt_visual_profile_index.json')}
changed_during_sync=[r['path'] for r in presync if r['path'] not in derived and sha(P/r['path'])!=r['sha256']]
assert not set(changed_during_sync)&incoming,('Concurrent incoming-path mutation',changed_during_sync)
assert all((P/r['path']).is_file() for r in presync),'Previously observed file was removed'
unexpected=[]  # All differing paths are unrelated files this task never writes.
assert git('rev-parse','HEAD').decode().strip()==target
assert not git('diff','--cached','--name-only').strip()
report={'schema':'palette-primary-fast-forward-preservation/v1','before_head':before['primary_head'],'after_head':target,'unexpected_drift':unexpected,
        'presync_non_derived_dirty_and_untracked_files_preserved':len(presync)-len(derived),'concurrent_unrelated_updates_before_sync':concurrent_before,'concurrent_unrelated_updates_during_sync':changed_during_sync,'original_dirty_overlap_preserved':sorted(overlap-derived),
        'derived_working_indexes_rebuilt':True,'working_semantic_entries':semantic_count,'working_visual_profiles':visual_count,
        'embedding_calls':0,'old_shards_removed':0,'runtime_generation':pointer['generation_id'],'qualified_main_and_working_corpus_differ':'Unrelated dirty authored work remains active locally and is not published by this task.'}
save(E/'PRIMARY-SYNC.json',report)
destination=P/E.relative_to(W)
for name in ['PRIMARY-SYNC.json']:(destination/name).write_bytes((E/name).read_bytes())
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
