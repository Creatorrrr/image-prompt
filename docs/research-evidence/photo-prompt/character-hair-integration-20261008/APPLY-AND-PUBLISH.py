"""Transplant reviewed owned paths only, retaining all prior shard generations."""
from pathlib import Path
import hashlib,json,shutil,sys

WORKTREE=Path(__file__).resolve().parents[4]
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
HERE=PRIMARY/'docs/research-evidence/photo-prompt/character-hair-integration-20261008'
SKILL=PRIMARY/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
from photo_runtime_sources import source_update,SnapshotPublisher

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def main():
    before=json.loads((HERE/'PRIMARY-BEFORE.json').read_text())
    old={row['path']:row['sha256'] for row in before['files']}
    owned_existing=[f'skills/photo-prompt-image-generator/assets/{n}' for n in [
        'photo_prompt_tags.json','photo_prompt_visual_obligations.json','photo_prompt_source_manifest.json',
        'photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']]
    owned_existing+=['tests/test_photo_hair_visual_semantics.py']
    for name in owned_existing:
        assert sha(PRIMARY/name)==old[name],f'Concurrent edit requires a reviewed merge: {name}'
    # The derived corpus must include the same full set of concurrent sources.
    drift=[name for name,expected in old.items() if sha(PRIMARY/name)!=expected]
    assert not drift,('Primary snapshot drift; rebuild the combined corpus before transplant',drift)
    new=[f'skills/photo-prompt-image-generator/assets/{n}' for n in [
        'photo_prompt_character_hair_extension.json','photo_prompt_visual_obligations_character_hair.json']]
    new+=['tests/test_photo_character_hair_integration.py',
          'docs/research-evidence/photo-prompt/extension-maintenance/character-hair-owned-relations-20261008.json']
    for name in new:assert not (PRIMARY/name).exists(),f'Unexpected new-path owner: {name}'
    shards=[]
    for filename in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
        manifest=json.loads((WORKTREE/'skills/photo-prompt-image-generator/assets'/filename).read_text())
        for row in manifest['shards']:
            name='skills/photo-prompt-image-generator/assets/'+row['path']
            assert sha(WORKTREE/name)==row['sha256']
            if (PRIMARY/name).exists():assert sha(PRIMARY/name)==row['sha256'],'Content-addressed shard collision'
            shards.append(name)
    paths=owned_existing+new+shards
    with source_update(SKILL):
        for name in paths:
            target=PRIMARY/name;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(WORKTREE/name,target)
    # Research/test results are outside the runtime authority.
    source_evidence=WORKTREE/'docs/research-evidence/photo-prompt/character-hair-integration-20261008'
    for path in source_evidence.rglob('*'):
        if not path.is_file() or '__pycache__' in path.parts:continue
        target=HERE/path.relative_to(source_evidence);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,target)
    preserved=[name for name,expected in old.items() if name not in owned_existing and sha(PRIMARY/name)==expected]
    report={'owned_changed_existing_paths':owned_existing,'owned_new_paths':new,'new_index_shards':shards,
            'unrelated_snapshot_files_preserved':len(preserved),'unrelated_changes':[],
            'applied_sha256':{name:sha(PRIMARY/name) for name in paths},'git_publication':'not_requested'}
    assert len(preserved)==len(old)-len(owned_existing)
    dump(HERE/'PRIMARY-APPLICATION.json',report)
    pointer=SnapshotPublisher(SKILL).publish()
    store=Path.home()/'.cache/image-prompt/character-hair-integration-20261008/runtime'
    isolated=SnapshotPublisher(SKILL,store).publish()
    dump(HERE/'RUNTIME-PUBLICATION.json',{'default':pointer,'test_store':str(store),'test_runtime':isolated})
    print(json.dumps({'copied':len(paths),'preserved':len(preserved),'generation_id':isolated['generation_id'],'test_store':str(store)}))

if __name__=='__main__':main()
