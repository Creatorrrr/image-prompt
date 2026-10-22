"""Refresh raw maintenance index in isolation; adopt only if source is unchanged."""
from pathlib import Path
import sys, json, shutil, hashlib, gc, os, time
gc.disable()
O=Path(__file__).resolve().parent
ROOT=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator')
STAGE=O/'working-index-skill'
sys.path.insert(0,str(ROOT/'scripts'))
import photo_candidate_corpus as c, photo_search_layout as layout
from photo_local_embedding import space
from photo_runtime_sources import source_update
from build_shared_candidate_index import build

def read(p): return json.loads(p.read_bytes())
def write(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()

def main():
    initial=c.load(ROOT/'assets'); source_hash=c.digest(initial)
    active=read(ROOT/'assets'/layout.MANIFEST)
    write(O/'working-index-start.json',{'source_sha256':source_hash,'old_layout_id':active['layout_id'],'candidates':len(initial['candidates']),'bindings':len(initial['slot_bindings'])})
    STAGE.mkdir(exist_ok=True); (STAGE/'assets').mkdir(exist_ok=True)
    for p in (ROOT/'assets').iterdir():
        if p.is_file(): shutil.copyfile(p,STAGE/'assets'/p.name)
    active_dir=Path(active['metadata']['path']).parent
    assert len(active_dir.parts)==2 and active_dir.parts[0]=='photo_candidate_search_shards'
    shutil.copytree(ROOT/'assets'/active_dir,STAGE/'assets'/active_dir,dirs_exist_ok=True)
    for directory in ['scripts','precore']:
        (STAGE/directory).mkdir(exist_ok=True)
        for p in (ROOT/directory).glob('*.py'): shutil.copyfile(p,STAGE/directory/p.name)
    for name in ['embedding-runtime.lock.json','defaults.json']:
        if (ROOT/name).exists(): shutil.copyfile(ROOT/name,STAGE/name)
    if not (STAGE/'.runtime').exists(): (STAGE/'.runtime').symlink_to(ROOT/'.runtime',target_is_directory=True)
    assert c.digest(c.load(STAGE/'assets'))==source_hash
    with source_update(STAGE): result=build(STAGE/'assets',O/'working-index-cache',space=space())
    write(O/'working-index-build.json',result)
    candidate=read(STAGE/'assets'/layout.MANIFEST)
    with source_update(ROOT):
        assert c.digest(c.load(ROOT/'assets'))==source_hash,'Concurrent source advanced; do not adopt stale index'
        if read(ROOT/'assets'/layout.MANIFEST)['corpus_sha256']==source_hash:
            write(O/'working-index-adoption.json',{'status':'already_refreshed_by_another_writer','source_sha256':source_hash})
            return
        new_dir=Path(candidate['metadata']['path']).parent
        assert len(new_dir.parts)==2 and new_dir.parts[0]=='photo_candidate_search_shards'
        target=ROOT/'assets'/new_dir
        assert not target.exists(),'Unexpected existing namespace; inspect before resuming'
        shutil.copytree(STAGE/'assets'/new_dir,target)
        verification=layout.verify(ROOT/'assets',c.load(ROOT/'assets'),candidate)
        temporary=ROOT/'assets'/'photo_candidate_search.atompunk.partial'
        temporary.write_bytes((STAGE/'assets'/layout.MANIFEST).read_bytes())
        assert c.digest(c.load(ROOT/'assets'))==source_hash
        os.replace(temporary,ROOT/'assets'/layout.MANIFEST)
        write(O/'working-index-adoption.json',{'status':'pass','source_sha256':source_hash,'layout_id':candidate['layout_id'],'verification':verification,'authored_source_changed':False,'installed_release_changed':False,'CURRENT_writes':0})
if __name__=='__main__': main()
