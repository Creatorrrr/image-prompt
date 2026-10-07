"""Preserve exact committed V34 replay inputs, including all sealed ancestors."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
PIN='f6b2f88fc9adeae0dfe59b78a7a0ecafc7b4c03a'
PRIOR=Path('docs/research-evidence/photo-prompt/data-quality-links-main-merge-20261007/history')
ILL='skills/subculture-illustration-image-generator/'
PHOTO='skills/photo-prompt-image-generator/'
MUTABLE={PHOTO+'assets/photo_prompt_source_manifest.json',PHOTO+'assets/photo_prompt_semantic_index.json',PHOTO+'assets/photo_prompt_visual_profile_index.json',ILL+'scripts/validate_illustration_assets.py',ILL+'assets/universal_scene_baseline_v2.json','tests/photo_prompt_fixtures.py','tests/test_photo_data_scope_v34_boundary_history.py','tests/test_photo_structure_maintenance.py','tests/test_photo_motion_artifact_owner_data_cleanup.py','tests/test_photo_data_scope_boundary_history.py','tests/test_photo_palette_boundary_history.py','tests/test_photo_robe_source_boundary_history.py','tests/test_photo_liminal_active_use_korean_data_cleanup.py'}

def sha(raw):return hashlib.sha256(raw).hexdigest()
def blob(raw):return hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)

def main():
    HERE.mkdir(parents=True,exist_ok=True)
    proof=json.loads((ROOT/PRIOR/'V34-DATA-SCOPE-PROOF.json').read_text())
    needed=set()
    for name in ['SOURCE-V32.json','SOURCE-LOCAL-V33.json','SOURCE-UPSTREAM-V33.json']:
        manifest=json.loads((ROOT/PRIOR/name).read_text());needed.add((PRIOR/name).as_posix())
        needed.update(r['path'] for r in manifest['members']);needed.update(r['source_path'] for r in manifest['members'])
    for group in ['source_files_after','active_shards_after','retained_shards_before','evidence_files','frozen_inputs']:needed.update(proof[group])
    needed.update([proof['upstream_proof'],(PRIOR/'V34-DATA-SCOPE-PROOF.json').as_posix(),'tests/photo_data_scope_history_v34.py','tests/test_photo_data_scope_v34_boundary_history.py','tests/photo_prompt_fixtures.py','tests/__init__.py',ILL+'assets/photo_regression_baseline_v34.json',ILL+'assets/photo_regression_baseline_v34_pack.json',ILL+'assets/universal_scene_baseline_v2.json'])
    tree_rows={}
    for item in git('ls-tree','-rz',PIN).split(b'\0'):
        if not item:continue
        info,name=item.split(b'\t',1);mode,kind,identity=info.decode().split();tree_rows[name.decode()]=(mode,kind,identity)
    rows=[]
    for name in sorted(needed):
        mode,kind,identity=tree_rows[name];assert kind=='blob' and mode in {'100644','100755'},('unsafe source',name)
        live=ROOT/name;raw=None
        if name not in MUTABLE and live.is_file() and not live.is_symlink():
            data=live.read_bytes()
            if blob(data)==identity and live.stat().st_mode&0o7777==int(mode[-3:],8):raw=data;backing=name
        if raw is None:
            raw=git('show',PIN+':'+name);assert blob(raw)==identity
            backing=(HERE/'parent-source-files'/name).relative_to(ROOT).as_posix();p=ROOT/backing;p.parent.mkdir(parents=True,exist_ok=True)
            if p.exists():assert p.read_bytes()==raw,'Refusing original snapshot replacement'
            else:p.write_bytes(raw);p.chmod(int(mode[-3:],8))
        rows.append(dict(path=name,source_path=backing,git_commit=PIN,git_path=name,git_blob=identity,mode=mode,bytes=len(raw),sha256=sha(raw)))
    manifest=dict(schema='photo-ethereal-parent-source/v1',stage='original-v34',source_pin=PIN,source_tree=git('show','-s','--format=%T',PIN).decode().strip(),environment=dict(implementation='cpython',python=[3,14,3],unicode='16.0.0'),member_count=len(rows),total_member_bytes=sum(r['bytes'] for r in rows),members=rows,purpose='Exact V34 current boundary and original assertions; all V1-V33 backing/proofs remain unchanged.')
    p=HERE/'V34-PARENT-SOURCE.json';p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'member_count':len(rows),'bytes':manifest['total_member_bytes'],'sha256':sha(p.read_bytes()),'source_tree':manifest['source_tree'],'new_backing_count':sum(r['source_path']!=r['path'] for r in rows)}))

if __name__=='__main__':main()
