"""Apply only this task's reviewed authored delta to the fetched main tree."""
from pathlib import Path
import copy,hashlib,json,shutil,subprocess,sys
PRIMARY=Path('/Users/chasoik/Projects/image-prompt')
TARGET=Path('/Users/chasoik/.codex/worktrees/character-hair-main-merge/image-prompt')
OLD=PRIMARY/'docs/research-evidence/photo-prompt/character-hair-integration-20261008/before'
EVIDENCE=TARGET/'docs/research-evidence/photo-prompt/character-hair-main-merge-20261008'
ASSETS=Path('skills/photo-prompt-image-generator/assets')
sys.path.insert(0,str(TARGET/'skills/photo-prompt-image-generator/scripts'))
from photo_runtime_sources import source_update

def read(p):return json.loads(p.read_text())
def dump(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def merge(base,local,remote,path):
    if local==base:return copy.deepcopy(remote)
    if remote==base or remote==local:return copy.deepcopy(local)
    if all(isinstance(x,dict) for x in [base,local,remote]):
        result=copy.deepcopy(remote)
        for key in set(base)|set(local):
            if key not in local:
                assert remote.get(key)==base.get(key),('concurrent field deletion',path,key);result.pop(key,None)
            elif key not in base:
                assert key not in remote or remote[key]==local[key],('concurrent new field',path,key);result[key]=copy.deepcopy(local[key])
            else:result[key]=merge(base[key],local[key],remote.get(key),path+'.'+key)
        return result
    raise AssertionError(('Authored conflict needs explicit semantic resolution',path))

def main():
    names=['photo_prompt_tags.json','photo_prompt_visual_obligations.json'];deltas={}
    with source_update(TARGET/'skills/photo-prompt-image-generator'):
        for name in names:
            base=read(OLD/name);local=read(PRIMARY/ASSETS/name);remote=read(TARGET/ASSETS/name);initial=copy.deepcopy(remote)
            if 'slots' in base:
                original={(slot,x['id']):x for slot,rows in base['slots'].items() for x in rows};ours={(slot,x['id']):x for slot,rows in local['slots'].items() for x in rows};changes=[]
                for slot,rows in remote['slots'].items():
                    for i,row in enumerate(rows):
                        key=(slot,row['id'])
                        if key in original and ours[key]!=original[key]:rows[i]=merge(original[key],ours[key],row,name+'.'+str(key));changes.append(list(key))
                assert len(changes)==2
            else:
                original={x['id']:x for x in base['profiles']};ours={x['id']:x for x in local['profiles']};changes=[]
                for i,row in enumerate(remote['profiles']):
                    key=row['id']
                    if ours.get(key)!=original.get(key):remote['profiles'][i]=merge(original[key],ours[key],row,name+'.'+key);changes.append(key)
                assert set(changes)=={'wet_damp_clumped_hair_state','balayage_ribbon_color_placement'}
            dump(EVIDENCE/'pulled_before'/name,initial);dump(TARGET/ASSETS/name,remote);deltas[name]=changes
        manifest=read(TARGET/ASSETS/'photo_prompt_source_manifest.json');dump(EVIDENCE/'pulled_before/photo_prompt_source_manifest.json',manifest)
        for name,kind in [('photo_prompt_character_hair_extension.json','candidate'),('photo_prompt_visual_obligations_character_hair.json','visual_profile')]:
            assert not any(row['file']==name for row in manifest['sources'])
            manifest['sources'].append({'file':name,'kind':kind,'required':True,'load_order':max(row['load_order'] for row in manifest['sources'] if row['kind']==kind)+1})
        dump(TARGET/ASSETS/'photo_prompt_source_manifest.json',manifest)
        new=[str(ASSETS/name) for name in ['photo_prompt_character_hair_extension.json','photo_prompt_visual_obligations_character_hair.json']]+['tests/test_photo_character_hair_integration.py','docs/research-evidence/photo-prompt/extension-maintenance/character-hair-owned-relations-20261008.json','docs/research-evidence/photo-prompt/extension-maintenance/character-hair-owned-relations-20261008-v2.json']
        for name in new:
            target=TARGET/name;assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PRIMARY/name,target)
        # This test was clean in the recorded before snapshot.
        name='tests/test_photo_hair_visual_semantics.py';before=read(PRIMARY/'docs/research-evidence/photo-prompt/character-hair-integration-20261008/PRIMARY-BEFORE.json');expected=next(x['sha256'] for x in before['files'] if x['path']==name);assert sha(TARGET/name)==expected;shutil.copy2(PRIMARY/name,TARGET/name)
        name='tests/test_photo_scene_data_cleanup.py';text=(TARGET/name).read_text();needle='        filenames=tuple(name for name in generator.RESEARCH_EXTENSION_FILENAMES\n';assert text.count(needle)==1;text=text.replace(needle,'        # The hair overlay references SCA/appearance rows omitted from this\n        # historical inventory; omit that dependent overlay in this fixture too.\n'+needle)
        needle="                                        'photo_prompt_visual_grammar_extension.json',\n";assert text.count(needle)==1;text=text.replace(needle,needle+"                                        'photo_prompt_character_hair_extension.json',\n");(TARGET/name).write_text(text)
    for rel in ['docs/research-evidence/photo-prompt/character-hair-20261008','docs/research-evidence/photo-prompt/character-hair-integration-20261008','skills/photo-prompt-image-generator/data/runs/character-hair-integration-20261008']:
        for p in (PRIMARY/rel).rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts or p.suffix=='.pyc' or p.name.endswith('.LOCK') or p.name=='.LOCK':continue
            target=TARGET/p.relative_to(PRIMARY);assert not target.exists();target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    rel='docs/researches/2026-10-08-character-hair-visual-semantics.md';(TARGET/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PRIMARY/rel,TARGET/rel)
    report={'pulled_main':subprocess.check_output(['git','rev-parse','HEAD'],cwd=TARGET,text=True).strip(),'owned_record_changes':deltas,'new_sources':new,'manifest_appended':manifest['sources'][-2:],'prior_source_registrations_retained':True,'unrelated_primary_sources_imported':False,'native_evidence_retained_without_reinterpretation':True}
    dump(EVIDENCE/'AUTHORED-MERGE.json',report);print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
