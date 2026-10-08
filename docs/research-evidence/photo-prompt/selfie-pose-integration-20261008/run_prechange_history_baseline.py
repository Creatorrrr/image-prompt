"""Reproduce historical failures using hash-verified prechange source bytes."""
import hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
W=Path(__file__).resolve().parents[4];P=Path('/Users/chasoik/Projects/image-prompt')
OUT=Path(__file__).resolve().parent;PRIMARY_OUT=P/OUT.relative_to(W)
original=json.loads((PRIMARY_OUT/'primary-application.json').read_text())
expected={r['path']:r['before_sha256']for r in original['copied']if r['before_sha256']is not None}
modules=sys.argv[1:]or['tests.test_photo_appearance_boundary_history']
with tempfile.TemporaryDirectory(prefix='selfie-prechange-baseline-')as tmp:
    root=Path(tmp).resolve();linked=0
    # Read-only shared payloads. Tests use their own temporary trees. Restored
    # live sources are first unlinked, so writes cannot affect the worktree.
    for dirname in ['skills','tests','docs']:
        for current,dirs,files in os.walk(W/dirname,followlinks=False):
            current=Path(current)
            dirs[:]=[d for d in dirs if not(current/d).is_symlink()and not(current/d).is_relative_to(OUT)]
            if current.is_relative_to(OUT):continue
            for name in files:
                source=current/name;rel=source.relative_to(W)
                if source.is_symlink()or rel.as_posix()in ['skills/photo-prompt-image-generator/assets/photo_prompt_selfie_pose_extension.json','skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_selfie_pose.json','tests/test_photo_selfie_pose_semantics.py']:continue
                target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);os.link(source,target);linked+=1
    restored=[]
    with zipfile.ZipFile(PRIMARY_OUT/'primary-owned-before.zip')as archive:
        for name in archive.namelist():
            if name not in expected:continue
            raw=archive.read(name);assert hashlib.sha256(raw).hexdigest()==expected[name]
            target=root/name;target.parent.mkdir(parents=True,exist_ok=True);target.unlink(missing_ok=True);target.write_bytes(raw)
            target.chmod((W/name).stat().st_mode&0o7777)
            restored.append({'path':name,'sha256':expected[name]})
    for module in modules:
        label=module.removeprefix('tests.');log=OUT/(label+'-prechange-baseline.log')
        assert not log.exists(),('Preserve previous baseline evidence',log)
        command=[str(P/'.venv/bin/python'),'-m','unittest',module,'-v']
        with log.open('w')as f:result=subprocess.run(command,cwd=root,stdout=f,stderr=subprocess.STDOUT)
        (OUT/(label+'-prechange-baseline-receipt.json')).write_text(json.dumps({'argv':command,'exit_code':result.returncode,'restored_hash_verified_prechange_sources':restored,'new_selfie_source_files_absent':True,'read_only_linked_payload_count':linked,'scope':'Identical historical test expectations and code, prechange live metadata recovered from exact original backup; no golden fixture or gate changed. Temporary baseline tree removed after the run.','log':str(log)},ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'module':module,'exit_code':result.returncode,'restored_sources':len(restored),'log':str(log)}),flush=True)
