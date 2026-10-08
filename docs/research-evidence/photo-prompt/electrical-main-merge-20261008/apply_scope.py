"""Apply only the electrical authored sources and frozen evidence to pulled main."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
SKILL = Path('skills/photo-prompt-image-generator')
EVIDENCE = Path('docs/research-evidence/photo-prompt/electrical-semantics-20261008')
MERGE = Path('docs/research-evidence/photo-prompt/electrical-main-merge-20261008')
OWNED = [SKILL/'assets/photo_prompt_electrical_relations_extension.json',
         SKILL/'assets/photo_prompt_visual_obligations_electrical_relations.json',
         Path('tests/test_photo_electrical_relations.py')]


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def git(root, *args): return subprocess.check_output(['git',*args],cwd=root)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--target',type=Path,required=True);args=parser.parse_args()
    target=args.target.resolve();assert target!=PRIMARY
    assert not git(target,'status','--porcelain').strip()
    base=git(target,'rev-parse','HEAD').decode().strip()
    sys.path.insert(0,str(target/SKILL/'scripts'))
    from photo_runtime_sources import source_update
    manifest=target/SKILL/'assets/photo_prompt_source_manifest.json'
    original=json.loads(manifest.read_text())
    primary=json.loads((PRIMARY/SKILL/'assets/photo_prompt_source_manifest.json').read_text())
    intended={p.name for p in OWNED[:2]}
    additions=[dict(row) for row in primary['sources'] if row['file'] in intended]
    assert len(additions)==2
    old_rows=list(original['sources']);merged=list(old_rows)
    for row in additions:
        assert not any(x['file']==row['file'] for x in merged),row['file']
        row['load_order']=max(x['load_order'] for x in merged if x['kind']==row['kind'])+1
        merged.append(row)
    protected={}
    for raw in git(target,'ls-files','-z',(SKILL/'assets').as_posix()).split(b'\0'):
        if not raw:continue
        name=raw.decode()
        if name.endswith(('photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json','photo_prompt_source_manifest.json')):continue
        p=target/name
        if p.is_file():protected[name]=sha(p)
    with source_update(target/SKILL):
        for relative in OWNED:
            src=PRIMARY/relative;dst=target/relative
            assert src.is_file() and not dst.exists(),relative
            dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
        manifest.write_text(json.dumps({**original,'sources':merged},ensure_ascii=False,indent=2)+'\n')
    evidence=[]
    for src in sorted((PRIMARY/EVIDENCE).rglob('*')):
        if not src.is_file():continue
        relative=src.relative_to(PRIMARY);dst=target/relative
        assert not dst.exists(),relative
        dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
        evidence.append({'path':str(relative),'sha256':sha(src),'bytes':src.stat().st_size})
    output=target/MERGE;output.mkdir(parents=True,exist_ok=True)
    shutil.copy2(Path(__file__),output/'apply_scope.py')
    proof={'pulled_main':base,'owned_authored_files':[{ 'path':str(p),'sha256':sha(PRIMARY/p)} for p in OWNED],
           'registered_additions':additions,'all_main_manifest_rows_preserved_exactly':merged[:len(old_rows)]==old_rows,
           'main_assets_before':protected,'frozen_evidence_files':evidence,
           'unrelated_primary_authored_changes_included':False,'native_regenerated_during_merge':False}
    (output/'AUTHORED-SCOPE.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'pulled_main':base,'new_authored_sources':2,'registered_additions':additions,
                      'protected_main_assets':len(protected),'frozen_evidence_files':len(evidence)},ensure_ascii=False))


if __name__=='__main__':main()
