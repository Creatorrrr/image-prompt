"""Normalize supplemental cut property paths, preserving positive text and history."""
from pathlib import Path
import copy,hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
SKILL=ROOT/'skills/photo-prompt-image-generator';A=SKILL/'assets'
sys.path.insert(0,str(SKILL/'scripts'))
import photo_candidate_semantics as cs
import prompt_generator as pg
from photo_runtime_sources import source_update
from visual_profile_contracts import compile_visual_profile

def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def main():
    candidate_path=A/'photo_prompt_character_hair_extension.json';profile_path=A/'photo_prompt_visual_obligations_character_hair.json'
    source=json.loads(candidate_path.read_text());visual=json.loads(profile_path.read_text());old=copy.deepcopy(source);old_visual=copy.deepcopy(visual)
    changes=[]
    owned_rows=[(e['id'],e) for rows in source['slots'].values() for e in rows]+[(p['id'],p['concept_candidate']) for p in visual['profiles']]
    for owner_id,row in owned_rows:
        for effect in row['affected_properties']:
            path=effect['property']
            if path.startswith('hair.style.supp-'):
                effect['property']=path.replace('hair.style.supp-','hair.style.',1).replace('-','_')
                changes.append({'id':owner_id,'before':path,'after':effect['property']})
            assert re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)*',effect['property'])
    # Effects and provenance are metadata, not retrieval prototypes. Prove that
    # these normalized paths cannot quietly rewrite a positive description.
    for slot,rows in source['slots'].items():
        for before,after in zip(old['slots'][slot],rows):assert pg.semantic_text_for_entry(before,slot)==pg.semantic_text_for_entry(after,slot)
    for before,after in zip(old_visual['profiles'],visual['profiles']):
        assert pg.visual_profile_semantic_text(compile_visual_profile(before))==pg.visual_profile_semantic_text(compile_visual_profile(after))
    report={'changed_effect_declarations':len(changes),'changes':changes,'all_positive_candidate_and_profile_texts_identical':True,
            'native_test_generation':'0a3b19f34fb2ef66f6406cbf4f38c9aac196ebc515b8bb918aa2d1c16fc40000',
            'reason':'Supplemental-cut prefix stripping produced a hyphenated property segment. Normalize it to a canonical dotted path; the conservative hair.style parent effect and all rendered meaning remain unchanged.'}
    dump(HERE/'PROPERTY-PATH-REVIEW.json',report)
    if '--apply' not in sys.argv:print(json.dumps({k:v for k,v in report.items() if k!='changes'}));return
    assert changes and old['maintenance_ref']['record_id']=='character-hair-owned-relations-20261008'
    record_path=ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/character-hair-owned-relations-20261008-v2.json'
    assert not record_path.exists()
    predecessor=old['maintenance_ref'];original_record=json.loads((record_path.parent/(predecessor['record_id']+'.json')).read_text())
    assert cs.digest(original_record)==predecessor['sha256']
    record={'contract_version':'photo-extension-maintenance-record/v1','record_id':record_path.stem,
            'authored_source_sha256':cs.digest({k:v for k,v in source.items() if k!='maintenance_ref'}),
            'maintenance_only':{'source_revision':{'predecessor_ref':predecessor,
                'research':'docs/research-evidence/photo-prompt/character-hair-20261008',
                'mapping':'docs/research-evidence/photo-prompt/character-hair-integration-20261008/INTEGRATION-MAP.json',
                'metadata_review':'docs/research-evidence/photo-prompt/character-hair-integration-20261008/PROPERTY-PATH-REVIEW.json',
                'phase':'authored_with_partial_native_evidence_not_dataset_wide_qualification'}}}
    source['maintenance_ref']={'contract_version':'photo-extension-maintenance-ref/v1','record_id':record['record_id'],'sha256':cs.digest(record)}
    dump(HERE/'before_metadata_fix/photo_prompt_character_hair_extension.json',old)
    dump(HERE/'before_metadata_fix/photo_prompt_visual_obligations_character_hair.json',old_visual)
    with source_update(SKILL):dump(record_path,record);dump(candidate_path,source);dump(profile_path,visual)
    report.update({'status':'applied','successor_record':str(record_path.relative_to(ROOT)),
                   'candidate_source_sha256':hashlib.sha256(candidate_path.read_bytes()).hexdigest(),
                   'profile_source_sha256':hashlib.sha256(profile_path.read_bytes()).hexdigest()})
    dump(HERE/'PROPERTY-PATH-REVIEW.json',report);print(json.dumps({k:v for k,v in report.items() if k!='changes'}))

if __name__=='__main__':main()
