"""Audit metadata-only vectors, publish final sources, and sync owned worktree paths."""
from pathlib import Path
import gc,hashlib,json,shutil,sys,subprocess
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
SKILL=ROOT/'skills/photo-prompt-image-generator';A=SKILL/'assets'
WT=Path('/Users/chasoik/.codex/worktrees/character-hair-integration/image-prompt')
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg
from photo_runtime_sources import SnapshotPublisher,source_update

def dump(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    review=json.loads((HERE/'PROPERTY-PATH-REVIEW.json').read_text());assert review.get('status')=='applied'
    audits={}
    for kind,name,loader in [('candidate','photo_prompt_semantic_index.json',pg.load_semantic_index_payload),('profile','photo_prompt_visual_profile_index.json',pg.load_visual_profile_index_payload)]:
        old=json.loads((HERE/'before_metadata_fix'/name).read_text());new=loader(A/name)
        for field in ['provider','embedding_model','embedding_dimensions','semantic_text_recipe']:assert old[field]==new[field]
        old_rows={}
        for row in old['shards']:
            path=A/row['path'];assert sha(path)==row['sha256'];old_rows.update(json.loads(path.read_text())['entries'])
        assert set(old_rows)==set(new['entries'])
        for key,row in new['entries'].items():
            assert old_rows[key]['text']==row['text'],(kind,key,'positive text changed')
            assert old_rows[key]['vector']==row['vector'],(kind,key,'vector changed')
        audits[kind]={'entries':len(old_rows),'all_positive_texts_identical':True,'all_vectors_identical':True,'no_new_embedding_requests':True,'same_provider_model_dimensions_recipe':True}
        del old_rows,new;gc.collect()
    if '--audit-only' in sys.argv:
        dump(HERE/'FINAL-METADATA-INDEX-AUDIT.json',audits)
        print(json.dumps({'index_audit':audits,'runtime_mutation':False}));return
    original=json.loads((HERE/'RUNTIME-PUBLICATION.json').read_text())
    dump(HERE/'NATIVE-TEST-RUNTIME-PUBLICATION.json',original)
    store=Path(original['test_store'])
    pointer=SnapshotPublisher(SKILL).publish();test=SnapshotPublisher(SKILL,store).publish()
    final={'default':pointer,'test_store':str(store),'test_runtime':test,'native_test_generation':original['test_runtime']['generation_id'],'final_change':'14 supplemental-cut effect declarations normalized; every positive prototype and vector remains identical.'}
    dump(HERE/'RUNTIME-PUBLICATION.json',final);dump(HERE/'FINAL-METADATA-INDEX-AUDIT.json',audits)
    initial=json.loads((HERE/'PRIMARY-APPLICATION.json').read_text());owned=set(initial['owned_changed_existing_paths'])|{'tests/test_photo_scene_data_cleanup.py'}
    paths=owned|set(initial['owned_new_paths'])|{'docs/research-evidence/photo-prompt/extension-maintenance/character-hair-owned-relations-20261008-v2.json'}
    for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
        for row in json.loads((A/name).read_text())['shards']:
            paths.add('skills/photo-prompt-image-generator/assets/'+row['path'])
    with source_update(WT/'skills/photo-prompt-image-generator'):
        for name in sorted(paths):
            target=WT/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,target)
    before=json.loads((HERE/'PRIMARY-BEFORE.json').read_text());preserved=[];drift=[]
    for row in before['files']:
        if row['path'] in owned:continue
        p=ROOT/row['path']
        if p.exists() and sha(p)==row['sha256'] and (p.stat().st_mode&0o7777)==row['mode']:preserved.append(row['path'])
        else:drift.append(row['path'])
    assert not drift,drift
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head==before['primary_head']
    preservation={'snapshot_files':len(before['files']),'owned_changed_existing_paths':sorted(owned),'unrelated_files_preserved_byte_and_mode':len(preserved),'unrelated_drift':drift,'head_unchanged':head,'git_publication':'not_requested','final_owned_file_sha256':{name:sha(ROOT/name) for name in sorted(paths)}}
    dump(HERE/'FINAL-PRESERVATION.json',preservation)
    print(json.dumps({'final_generation':test['generation_id'],'native_test_generation':final['native_test_generation'],'index_audit':audits,'unrelated_files_preserved':len(preserved),'owned_paths_synced_to_worktree':len(paths)}))
if __name__=='__main__':main()
