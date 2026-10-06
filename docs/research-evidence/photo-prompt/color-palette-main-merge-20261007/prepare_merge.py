"""Add only qualified palette sources to pulled main; archive exact V32 inputs."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess

W=Path(__file__).resolve().parents[4]
P=Path('/Users/chasoik/Projects/image-prompt')
Q=Path('/Users/chasoik/.codex/worktrees/color-palette-integration/image-prompt')
E=Path(__file__).resolve().parent
S=Path('skills/photo-prompt-image-generator')
I=Path('skills/subculture-illustration-image-generator')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=W)

pin=git('rev-parse','HEAD').decode().strip()
assert pin=='96e20422316276a4e0b5ed97f44152e4931e7504'
tree=git('rev-parse','HEAD^{tree}').decode().strip()
git('switch','-c','codex/palette-main-merge-20261007')

# Extend the already sealed V31 closure with the exact V32 source/evidence.
proof32=read(W/'docs/research-evidence/photo-prompt/robe-back-source-consistency-20261006/V32-ROBE-SOURCE-PROOF.json')
parent31=read(W/proof32['parent_manifest'])
closure={r['path'] for r in parent31['members']}
for key in ['source_files_after','active_shards_after','retained_shards_before','evidence_files','frozen_inputs']:
    closure.update(proof32[key])
closure.update([proof32['parent_manifest'],proof32['maintenance_successor']['path'],
                'docs/research-evidence/photo-prompt/robe-back-source-consistency-20261006/V32-ROBE-SOURCE-PROOF.json',
                str(I/'assets/photo_regression_baseline_v32.json'),str(I/'assets/photo_regression_baseline_v32_pack.json'),
                'tests/test_photo_robe_source_boundary_history.py'])
will_change={str(S/'assets'/n) for n in ['photo_prompt_source_manifest.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']}
will_change.update([str(I/'scripts/validate_illustration_assets.py'),str(I/'assets/universal_scene_baseline_v2.json'),
                    'tests/photo_prompt_fixtures.py','tests/test_photo_robe_source_boundary_history.py'])
records={}
for row in git('ls-tree','-r','-z','HEAD').split(b'\0'):
    if not row:continue
    meta,name=row.split(b'\t',1);mode,kind,blob=meta.decode().split();records[name.decode()]={'mode':mode,'blob':blob,'kind':kind}
members=[]
for name in sorted(closure):
    record=records[name]
    assert record['kind']=='blob' and record['mode'] in ['100644','100755'],name
    raw=(W/name).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==record['blob'],name
    source=name
    if name in will_change:
        source=str(E.relative_to(W)/'v32-parent-source-files'/name)
        target=W/source;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);target.chmod(int(record['mode'][-3:],8))
    members.append({'path':name,'source_path':source,'git_commit':pin,'git_path':name,'git_blob':record['blob'],
                    'mode':record['mode'],'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
parent={'schema':'photo-v32-parent-source-manifest/v1','source_pin':pin,'source_tree':tree,'member_count':len(members),
        'total_member_bytes':sum(r['bytes'] for r in members),'members':members}
save(E/'V32-PARENT-SOURCE.json',parent)
save(E/'REMOTE-V32-SOURCE-BOUNDARY.json',{'remote_main':pin,'source_tree':tree,'v32_proof_sha256':sha(W/'docs/research-evidence/photo-prompt/robe-back-source-consistency-20261006/V32-ROBE-SOURCE-PROOF.json'),'photo_source_files':proof32['source_files_after'],'source_inventory':proof32['source_inventory_after'],'active_shards':proof32['active_shards_after'],'frozen_inputs':proof32['frozen_inputs'],'historical_assets':{str(p.relative_to(W)):sha(p) for p in sorted((W/I/'assets').glob('photo_regression_baseline_v*.json'))}})

owned=[S/'assets/photo_prompt_palette_applications_extension.json',S/'assets/photo_prompt_visual_obligations_palette_applications.json',
       Path('tests/test_photo_palette_applications.py'),Path('docs/research-evidence/photo-prompt/extension-maintenance/photo_prompt_palette_applications_extension-20261006.json')]
for rel in owned:
    assert (P/rel).read_bytes()==(Q/rel).read_bytes(),str(rel)
    (W/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Q/rel,W/rel)
manifest_path=W/S/'assets/photo_prompt_source_manifest.json';manifest=read(manifest_path)
original_rows=json.loads(json.dumps(manifest['sources']))
for name,kind in [('photo_prompt_palette_applications_extension.json','candidate'),('photo_prompt_visual_obligations_palette_applications.json','visual_profile')]:
    assert not any(r['file']==name for r in manifest['sources'])
    order=max(r['load_order'] for r in manifest['sources'] if r['kind']==kind)+1
    manifest['sources'].append({'file':name,'kind':kind,'required':True,'load_order':order})
assert manifest['sources'][:-2]==original_rows
save(manifest_path,manifest)
test=W/'tests/test_photo_structure_maintenance.py';text=test.read_text()
needle='        self.assertEqual(list(sources.extension_files("candidate")), original["candidate"])'
added='        original["candidate"].append("photo_prompt_palette_applications_extension.json")\n        original["visual_profile"].append("photo_prompt_visual_obligations_palette_applications.json")\n        original["required_candidates"].append("photo_prompt_palette_applications_extension.json")\n'
assert text.count(needle)==1
test.write_text(text.replace(needle,added+needle))
for name in ['color-palette-integration-20261006','color-palette-semantics-20261006']:
    rel=Path('docs/research-evidence/photo-prompt')/name
    shutil.copytree(Q/rel,W/rel,dirs_exist_ok=True)
save(E/'MERGE-ADOPTION.json',{'strategy':'Qualified narrow palette sources appended to pulled main; original remote rows and all unrelated local work preserved.',
                          'source_main':pin,'qualified_worktree':str(Q),'new_candidates':37,'new_profiles':13,'optional_context_records':52,'held_claims':11,
                          'source_manifest_new_rows':manifest['sources'][-2:],'new_owned_files':[{ 'path':str(p),'sha256':sha(W/p)} for p in owned],
                          'unrelated_local_dirty_sources_published':False,'previous_native_images':'Archived unchanged; no new merged-tree rendering.'})
print(json.dumps({'parent_members':len(members),'parent_bytes':parent['total_member_bytes'],'parent_archive_copies':len(will_change),'owned_source_files':len(owned),'remote_main':pin},ensure_ascii=False),flush=True)
