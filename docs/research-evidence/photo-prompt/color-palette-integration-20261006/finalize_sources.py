"""Preserve generation-3 evidence and CAS-sync the last owned metadata revision."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

E=Path(__file__).resolve().parent
W=E.parents[3]
P=Path('/Users/chasoik/Projects/image-prompt')
S=Path('skills/photo-prompt-image-generator')
STORE=Path('/tmp/color-palette-runtime-20261006')
GEN3='9dbbf3161bcaac585c32a5f3e7d77890eb6cbdb4a917b863470577518c4d1e14'
FROZEN=STORE/'generations'/GEN3
PY=W/'.venv/bin/python'

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def digest(d):return hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

for name in ['RUNTIME-PUBLICATION-FINAL','PRIMARY-RUNTIME-PUBLICATION-FINAL']:
    for suffix in ['json','stdout','log']:
        src=E/(name+'.'+suffix)
        dst=E/(name+'-IMAGE-GENERATION-3.'+suffix)
        if src.is_file() and not dst.exists():shutil.copyfile(src,dst)

frozen_evidence=E/'image-generation-3-source'
frozen_evidence.mkdir(exist_ok=True)
for name in ['photo_prompt_palette_applications_extension.json','photo_prompt_visual_obligations_palette_applications.json']:
    shutil.copyfile(FROZEN/'assets'/name,frozen_evidence/name)
shutil.copyfile(FROZEN/'manifest.json',frozen_evidence/'runtime-manifest.json')

sys.path.insert(0,str(W/S/'scripts'))
import prompt_generator as pg
from photo_contracts import property_effects_allowed
from photo_runtime_sources import source_update

profiles_file='photo_prompt_visual_obligations_palette_applications.json'
oldp={p['id']:p for p in read(FROZEN/'assets'/profiles_file)['profiles']}
newp={p['id']:p for p in read(W/S/'assets'/profiles_file)['profiles']}
changed_profiles=[k for k in oldp if oldp[k]!=newp[k]]
assert set(changed_profiles)=={'pa_food_container_color_owners','pa_ordered_background_gradient'}
selected=['pa_bounded_metal_trim','pa_local_color_under_separate_lights']
assert all(oldp[k]==newp[k] for k in selected)
guards=[]
for pid,target in [('pa_food_container_color_owners','coffee_cup'),('pa_ordered_background_gradient','background_panel')]:
    lock={'contract_version':'photo-intent-lock/v2','semantic_anchors':[{'dimension':'color','target':target,'property':'surface.local_color'}]}
    op=oldp[pid]['concept_candidate'];np=newp[pid]['concept_candidate']
    before=property_effects_allowed(lock,op['affected_dimensions'],op['affected_properties'])
    after=property_effects_allowed(lock,np['affected_dimensions'],np['affected_properties'])
    assert before is True and after is False
    guards.append({'profile_id':pid,'actual_owner':target,'locked_property':'surface.local_color','before_allowed':before,'after_allowed':after})

index=read(E/'INDEX-REPORT.json')
for key,name,loader in [('semantic','photo_prompt_semantic_index.json',pg.load_semantic_index_payload),('visual','photo_prompt_visual_profile_index.json',pg.load_visual_profile_index_payload)]:
    old=loader(FROZEN/'assets'/name);new=loader(W/S/'assets'/name)
    assert set(old['entries'])==set(new['entries'])
    unchanged=sum(old['entries'][k]['text']==new['entries'][k]['text'] and old['entries'][k]['vector']==new['entries'][k]['vector'] for k in old['entries'])
    assert unchanged==len(new['entries'])
    assert len(new['entries'])==index[key]['current_entries']
    index[key]['manifest_sha256']=sha(W/S/'assets'/name)
    index[key]['last_metadata_revision_text_vector_preserved']=unchanged
    index[key]['comparison_generation_id']=GEN3
write(E/'INDEX-REPORT.json',index)

def publish(root,prefix,store=None):
    cmd=[str(PY),str(root/S/'scripts/publish_photo_runtime_snapshot.py')]
    if store is not None:cmd+=['--runtime-store',str(store)]
    with (E/(prefix+'.stdout')).open('w') as out,(E/(prefix+'.log')).open('w') as err:
        subprocess.run(cmd,cwd=root,stdout=out,stderr=err,check=True)
    raw=(E/(prefix+'.stdout')).read_text();decoder=json.JSONDecoder();offset=0;values=[]
    while offset<len(raw):
        while offset<len(raw) and raw[offset].isspace():offset+=1
        if offset==len(raw):break
        obj,offset=decoder.raw_decode(raw,offset);values.append(obj)
    pointer=next(d for d in reversed(values) if isinstance(d,dict) and d.get('generation_id'))
    write(E/(prefix+'.json'),pointer)
    print(json.dumps({'publication':prefix,'generation_id':pointer['generation_id']},ensure_ascii=False),flush=True)
    return pointer

worktree_pointer=publish(W,'RUNTIME-PUBLICATION-FINAL',STORE)
previous_sync=read(E/'SYNC-REPORT.json')
expected_owned={r['path']:r['sha256'] for r in previous_sync['copied']}
initial=read(E/'INPUT-SNAPSHOT.json')
initial_rows={r['path']:r['sha256'] for r in initial['files']}
for rel,expected in expected_owned.items():
    if sha(P/rel)!=expected:raise RuntimeError('Owned destination drift: '+rel)
for rel,expected in initial_rows.items():
    if rel not in expected_owned and sha(P/rel)!=expected:raise RuntimeError('Unrelated input drift: '+rel)

owned={Path(p) for p in expected_owned}
for name in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
    manifest=S/'assets'/name
    owned.add(manifest)
    owned.update(S/'assets'/row['path'] for row in read(W/manifest)['shards'])
for rel in owned:
    if str(rel) not in expected_owned and (P/rel).exists() and sha(P/rel)!=sha(W/rel):
        raise RuntimeError('New shard destination conflict: '+str(rel))

with source_update(P/S):
    for rel in sorted(owned):
        assert (W/rel).is_file(),str(rel)
        (P/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(W/rel,P/rel)

previous_sync['copied']=[{'path':str(rel),'sha256':sha(P/rel)} for rel in sorted(owned)]
previous_sync['last_revision']='Cup and background surface.local_color lock coverage; all selected rendered profile contracts unchanged.'
write(E/'SYNC-REPORT.json',previous_sync)
primary_pointer=publish(P,'PRIMARY-RUNTIME-PUBLICATION-FINAL')
assert primary_pointer['generation_id']==worktree_pointer['generation_id']

expected_all={**initial_rows,**{r['path']:r['sha256'] for r in previous_sync['copied']}}
drift=[p for p,expected in expected_all.items() if sha(P/p)!=expected]
assert not drift,drift
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip()
assert head=='6b0338ebe6ad3a9a5ee3c603fc742311ad921054'
skillsha=sha(P/S/'SKILL.md')
assert skillsha=='7dc4220b1dd784abe8ed7c93b84612d0472591c7753f0dcfda0c88da229ac857'
assert sha(P/'.agents/skills/photo-prompt-image-generator/SKILL.md')==skillsha
write(E/'FINAL-SOURCE-INTEGRITY.json',{'schema_version':'color-palette-final-source-integrity/v1','unexpected_drift':drift,'checked_files':len(expected_all),'upstream_head':head,'skill_sha256':skillsha,'old_shards_removed':0,'primary_and_worktree_generation_id':primary_pointer['generation_id']})
write(E/'FINAL-CARRIER-SCOPE-REPORT.json',{'schema_version':'color-palette-last-carrier-scope/v1','image_generation_id':GEN3,'final_active_generation_id':primary_pointer['generation_id'],'modified_unselected_profiles':changed_profiles,'selected_profile_contracts_unchanged':[{'profile_id':pid,'generation_3_contract_sha256':digest(oldp[pid]),'final_contract_sha256':digest(newp[pid]),'unchanged':True} for pid in selected],'guards':guards,'pixel_test_for_last_changed_profiles':False})
print(json.dumps({'sync_files':len(owned),'unexpected_drift':drift,'final_source_scope_checks':guards},ensure_ascii=False),flush=True)
