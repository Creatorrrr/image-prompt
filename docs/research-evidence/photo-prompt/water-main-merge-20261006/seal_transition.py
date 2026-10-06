"""Seal the reviewed V30 boundary without relabeling immutable V1-V29."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
PHOTO = Path('skills/photo-prompt-image-generator')
ILL = Path('skills/subculture-illustration-image-generator')
PARENT = 'c5588d4fc791e9ed391822a96c40573004322256'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    original = json.loads((ROOT / 'docs/research-evidence/photo-prompt/retrieval-runtime-freshness-20261006/V28-PARENT-SOURCE.json').read_bytes())
    previous = json.loads((ROOT / 'docs/research-evidence/photo-prompt/retrieval-runtime-freshness-20261006/V29-RUNTIME-PROOF.json').read_bytes())
    paths = {row['path'] for row in original['members']}
    paths.update(row['source_path'] for row in original['members'])
    paths.update(previous['source_files_after'])
    paths.update(previous['active_shards_after'])
    paths.update(str(p.relative_to(ROOT)) for p in (ROOT / ILL / 'assets').glob('photo_regression_baseline_v*.json') if '_v30' not in p.name)
    paths.update([
        'docs/research-evidence/photo-prompt/retrieval-runtime-freshness-20261006/V29-RUNTIME-PROOF.json',
        'docs/research-evidence/photo-prompt/retrieval-runtime-freshness-20261006/V28-PARENT-SOURCE.json',
        'tests/photo_prompt_fixtures.py',
    ])
    tree = subprocess.check_output(['git','ls-tree','-r','-z',PARENT],cwd=ROOT)
    objects = {}
    for row in tree.split(b'\0'):
        if not row: continue
        metadata, name = row.split(b'\t',1)
        mode, kind, blob = metadata.decode().split()
        objects[name.decode()] = (mode, blob)
    missing = sorted(paths - objects.keys())
    if missing: raise RuntimeError(f'Parent dependencies are not in pinned Git tree: {missing}')
    members = []
    proc = subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    try:
        for name in sorted(paths):
            mode, blob = objects[name]
            proc.stdin.write((blob+'\n').encode());proc.stdin.flush()
            header=proc.stdout.readline().decode().strip().split()
            assert header[0]==blob and header[1]=='blob'
            raw=proc.stdout.read(int(header[2]));assert proc.stdout.read(1)==b'\n'
            current=ROOT/name
            archived=HERE/'v29-parent-source-files'/name
            source_path=name
            must_archive = name in {
                'tests/photo_prompt_fixtures.py',
                str(ILL/'scripts/validate_illustration_assets.py'),
                str(ILL/'assets/universal_scene_baseline_v2.json'),
            }
            if must_archive or not current.is_file() or current.read_bytes()!=raw:
                archived.parent.mkdir(parents=True,exist_ok=True)
                if archived.exists():assert archived.read_bytes()==raw
                else:archived.write_bytes(raw)
                archived.chmod(int(mode[-3:],8))
                source_path=str(archived.relative_to(ROOT))
            members.append({'path':name,'source_path':source_path,'sha256':digest(raw),
                            'git_blob':blob,'bytes':len(raw),'mode':mode})
    finally:
        proc.stdin.close();proc.wait()
    parent_manifest={'schema':'photo-v29-parent-source-manifest/v1','source_pin':PARENT,
        'source_tree':subprocess.check_output(['git','rev-parse',PARENT+'^{tree}'],cwd=ROOT,text=True).strip(),
        'member_count':len(members),'total_member_bytes':sum(row['bytes'] for row in members),'members':members}
    parent_path=HERE/'V29-PARENT-SOURCE.json';save(parent_path,parent_manifest)
    assets=ROOT/PHOTO/'assets'
    source_files={}
    for p in sorted((ROOT/PHOTO).rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix in ('.json','.py','.md') and '_index_shards' not in str(p.parent):
            source_files[str(p.relative_to(ROOT))]=digest(p.read_bytes())
    inventory={p.name:digest(p.read_bytes()) for p in sorted(assets.glob('*.json'))}
    active={}
    for name in ('photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json'):
        for row in json.loads((assets/name).read_bytes())['shards']:
            p=assets/row['path'];assert digest(p.read_bytes())==row['sha256']
            active[str(p.relative_to(ROOT))]=row['sha256']
    illustration_assets=ROOT/ILL/'assets'
    old_raw=(illustration_assets/'photo_regression_baseline_v29_pack.json').read_bytes()
    raw=(ROOT/'.codex-artifacts/water-main-current-pack.json').read_bytes()
    old,new=json.loads(old_raw)[0],json.loads(raw)[0]
    delta=json.loads((HERE/'PACK-DELTA.json').read_bytes())
    unchanged=('authorial_core','creative_controls','embodiment_preflight','authorial_composition','negative_en')
    assert all(old[k]==new[k] for k in unchanged)
    assert all(old['slots'][k]['candidates']==new['slots'][k]['candidates'] for k in old['slots'] if k!='texture')
    assert old['slots']['texture']['candidates'][0]==new['slots']['texture']['candidates'][0]
    assert [x['id'] for x in old['slots']['texture']['candidates']]==['slot:texture:porcelain_hairline_crack','slot:texture:steam_haze']
    assert [x['id'] for x in new['slots']['texture']['candidates']]==['slot:texture:porcelain_hairline_crack','slot:texture:water_w026']
    assert old['adult_appeal']['composition_requirements']['adult_subject_phrase_required'] is True
    assert new['adult_appeal']['composition_requirements']['adult_subject_phrase_required'] is False
    water_names=['photo_prompt_water_relations_extension.json','photo_prompt_visual_obligations_water_relations.json']
    proof={'schema':'photo-water-main-transition/v30','previous_qualified_commit':PARENT,
        'previous_qualified_tree':parent_manifest['source_tree'],
        'parent_manifest':str(parent_path.relative_to(ROOT)),'parent_manifest_sha256':digest(parent_path.read_bytes()),
        'parent_member_count':len(members),'previous_manifest_sha256':digest((illustration_assets/'photo_regression_baseline_v29.json').read_bytes()),
        'previous_validator_sha256':next(row['sha256'] for row in members if row['path']==str(ILL/'scripts/validate_illustration_assets.py')),
        'previous_universal_descriptor_sha256':next(row['sha256'] for row in members if row['path']==str(ILL/'assets/universal_scene_baseline_v2.json')),
        'previous_pack_sha256':digest(old_raw),'previous_pack_id':old['pack_id'],
        'current_pack_sha256':digest(raw),'current_pack_id':new['pack_id'],
        'reviewed_pack_delta':delta['differences'],
        'preserved_contract_keys':list(unchanged),'unchanged_candidate_policy':'Every candidate object and ordering is exact except the reviewed second optional texture candidate: steam haze -> linked surface foam. The frozen core, controls, body review, budget and negative remain exact.',
        'local_commits_preserved':['270c491d','199670d3'],
        'water_source_sha256':{name:inventory[name] for name in water_names},
        'water_candidates':117,'water_profiles':117,'water_component_gates':351,
        'source_files_after':source_files,'source_inventory_after':inventory,'active_shards_after':active,
        'frozen_inputs':json.loads((illustration_assets/'photo_regression_baseline_v29.json').read_bytes())['frozen_inputs'],
        'native_image_calls_during_merge':0,'historical_water_render_generation':'ca8d80bf02fe00c9e49c1c59607cf0d859f5ca6f96818f50561ffa488d145327',
        'proof_boundary':'Current boundary and source integrity qualification; original water pixel results remain bound to their original generation, without claiming a rerender after merge.'}
    proof_path=HERE/'V30-WATER-MAIN-PROOF.json';save(proof_path,proof)
    baseline=json.loads((illustration_assets/'photo_regression_baseline_v29.json').read_bytes())
    baseline.update(schema='photo_regression_baseline/v30',historical_baseline={
        'path':'photo_regression_baseline_v29.json','schema':'photo_regression_baseline/v29','sha256':proof['previous_manifest_sha256']},
        change_scope='Add water relation data and preserve both main histories, including contextual adult wording; retain V1-V29 source and pack bytes.',
        sha256=proof['current_pack_sha256'],pack_id=new['pack_id'],
        purpose='Qualify declared water DATA and merged local policy changes without relabeling historical image or user acceptance evidence.')
    baseline['command'][-1]='/tmp/subculture-illustration-photo-baseline-v30.json'
    baseline.pop('runtime_freshness_transition')
    baseline['water_main_transition']={'evidence_path':str(proof_path.relative_to(ROOT)),
        'evidence_sha256':digest(proof_path.read_bytes()),'previous_qualified_commit':PARENT,
        'parent_manifest_sha256':proof['parent_manifest_sha256']}
    save(illustration_assets/'photo_regression_baseline_v30.json',baseline)
    (illustration_assets/'photo_regression_baseline_v30_pack.json').write_bytes(raw)
    print(json.dumps({'proof_sha256':digest(proof_path.read_bytes()),'parent_sha256':proof['parent_manifest_sha256'],
        'parent_members':len(members),'pack_delta_count':delta['count'],'water_sources':proof['water_source_sha256']}))


if __name__=='__main__':main()
