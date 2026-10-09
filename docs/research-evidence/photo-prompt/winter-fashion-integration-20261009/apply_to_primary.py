"""Add only owned winter sources; rebuild current primary indexes with exact caches."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,zipfile,os

PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
WORK=Path('/Users/chasoik/.codex/worktrees/winter-fashion-integration-20261009/image-prompt')
SKILL=PRIMARY/'skills/photo-prompt-image-generator'
SCRIPTS=SKILL/'scripts'
OUT=PRIMARY/'docs/research-evidence/photo-prompt/winter-fashion-integration-20261009'
sys.path.insert(0,str(SCRIPTS))
from photo_runtime_sources import source_update
from prompt_generator import load_semantic_index_payload

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(name,args):
    with (OUT/name).open('w') as log:
        # Canonical builders own their own cooperative write context. Keep that
        # context in a separate staging store while the primary store remains
        # guarded by the outer multi-source revision until BOTH indexes validate.
        env={**os.environ,'PHOTO_RUNTIME_STORE':str(OUT/'build-runtime-store')}
        p=subprocess.run([str(PRIMARY/'.venv/bin/python'),*args],cwd=PRIMARY,env=env,stdout=log,stderr=subprocess.STDOUT)
    if p.returncode:raise RuntimeError(f'{name}: code {p.returncode}')

owned=['photo_prompt_winter_fashion_extension.json','photo_prompt_visual_obligations_winter_fashion.json']
before={p.name:digest(p) for p in (SKILL/'assets').glob('*.json') if 'index' not in p.name}
with zipfile.ZipFile(OUT/'PRIMARY-OWNED-BEFORE.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['photo_prompt_source_manifest.json','photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
        p=SKILL/'assets'/name;z.write(p,p.relative_to(PRIMARY))
with source_update(SKILL):
    for name in owned:
        target=SKILL/'assets'/name
        if target.exists() and digest(target)!=digest(WORK/'skills/photo-prompt-image-generator/assets'/name):
            raise RuntimeError('Winter source changed independently: '+name)
        shutil.copy2(WORK/'skills/photo-prompt-image-generator/assets'/name,target)
    manifest_path=SKILL/'assets/photo_prompt_source_manifest.json'
    manifest=json.loads(manifest_path.read_text())
    for name,kind in [(owned[0],'candidate'),(owned[1],'visual_profile')]:
        if not any(s['file']==name for s in manifest['sources']):
            manifest['sources'].append({'file':name,'kind':kind,'required':True,'load_order':1+max(s['load_order'] for s in manifest['sources'] if s['kind']==kind)})
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    run('primary-final-authoring.log',[str(OUT/'author_winter_data.py'),str(PRIMARY)])
    shutil.copy2(WORK/'tests/test_photo_winter_fashion_integration.py',PRIMARY/'tests/test_photo_winter_fashion_integration.py')
    # This cache is only a vector source. Canonical builders rederive every text,
    # document, dictionary/registry hash and statistics from CURRENT primary data.
    cached=load_semantic_index_payload(WORK/'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json')
    checkpoint=OUT/'primary-semantic-cache.partial'
    checkpoint.write_text(json.dumps(cached,ensure_ascii=False)+'\n')
    run('primary-semantic-build.log',['skills/photo-prompt-image-generator/scripts/build_semantic_index.py','--batch-size','1','--request-interval','0.1','--keep-stale-generations','--checkpoint',str(checkpoint),'--progress','--no-runtime-publication'])
    run('primary-visual-build.log',['skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py','--batch-size','1','--cache-index',str(WORK/'skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json'),'--no-runtime-publication'])
    run('primary-dictionary.log',['skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py','--no-runtime-publication'])
    run('primary-visual-check.log',['skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py','--check','--no-runtime-publication'])
after={p.name:digest(p) for p in (SKILL/'assets').glob('*.json') if 'index' not in p.name}
unexpected=[name for name,h in before.items() if name!='photo_prompt_source_manifest.json' and after.get(name)!=h]
result={'status':'PASS_current_primary_source_and_indexes_published','owned_sources':owned,'unchanged_prior_authored_files':len(before)-1,'unexpected_prior_authored_changes':unexpected,'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=PRIMARY).decode().strip()}
(OUT/'PRIMARY-APPLICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result))
if unexpected:raise RuntimeError('Concurrent authored source changes require review')
