"""Author a reviewed V35 DATA successor without modifying V1-V34 evidence."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
PHOTO='skills/photo-prompt-image-generator/assets/'
ILL=ROOT/'skills/subculture-illustration-image-generator/assets'
OLD=ROOT/'docs/research-evidence/photo-prompt/data-quality-links-main-merge-20261007/history/V34-DATA-SCOPE-PROOF.json'
ADDED={PHOTO+'photo_prompt_ethereal_gothic_scene_extension.json',PHOTO+'photo_prompt_visual_obligations_ethereal_gothic_scene.json'}
CHANGED={PHOTO+'photo_prompt_source_manifest.json',PHOTO+'photo_prompt_semantic_index.json',PHOTO+'photo_prompt_visual_profile_index.json'}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def entries(manifest):
    result={}
    for row in manifest['shards']:
        p=ROOT/PHOTO/row['path'];assert sha(p)==row['sha256'];part=json.loads(p.read_text())['entries'];assert not set(part)&set(result);result.update(part)
    assert set(result)==set(manifest['entry_order']);return result

def main():
    parent_path=HERE/'V34-PARENT-SOURCE.json';parent=json.loads(parent_path.read_text());records={r['path']:r for r in parent['members']}
    previous_proof=json.loads(OLD.read_text());old_baseline=json.loads((ILL/'photo_regression_baseline_v34.json').read_text())
    previous=json.loads((ILL/'photo_regression_baseline_v34_pack.json').read_text());current_path=HERE/'CURRENT-BOUNDARY-PACK.json';current=json.loads(current_path.read_text());receipt_path=HERE/'CURRENT-BOUNDARY-RECEIPT.json';receipt=json.loads(receipt_path.read_text())
    pointers=['/0/core_retrieval/canonical_sha256','/0/core_retrieval/slot_corpus_sha256','/0/core_retrieval/slot_ownership_sha256','/0/creative_augmentation/hard_eligible_pool_sha256','/0/pack_id','/0/provenance/tags_hash','/0/slots/light_shape/candidates/1']
    def get(v,pointer):
        for part in pointer.split('/')[1:]:v=v[int(part)] if isinstance(v,list) else v[part]
        return v
    changes=[dict(operation='replace',pointer=p,before=get(previous,p),after=get(current,p)) for p in pointers]
    expected=json.loads(json.dumps(previous))
    for row in changes:
        parts=row['pointer'].split('/')[1:];v=expected
        for part in parts[:-1]:v=v[int(part)] if isinstance(v,list) else v[part]
        k=int(parts[-1]) if isinstance(v,list) else parts[-1];assert v[k]==row['before'];v[k]=row['after']
    assert expected==current,'Unreviewed pack difference'
    assert changes[-1]['before']['entry_id']=='monitor_rectangle_glow' and changes[-1]['after']['entry_id']=='sparkling_water_reflection_highlights'
    active={};index_proof={}
    allowed_changed={'slot:hair_style:low_bun_hair','slot:color:cr_candidate_cool_subject','slot:color:cr_candidate_dark_on_dark','slot:quality:pe_neutral_diffusion','slot:color:cr_candidate_low_chroma'}
    for filename in ['photo_prompt_semantic_index.json','photo_prompt_visual_profile_index.json']:
        name=PHOTO+filename;old=json.loads((ROOT/records[name]['source_path']).read_text());new=json.loads((ROOT/name).read_text());a,b=entries(old),entries(new)
        assert set(a)<=set(b),'Prior index identities removed'
        for field in ['provider','embedding_model','embedding_dimensions']:assert old[field]==new[field]
        same=0;changed=[]
        for key,row in a.items():
            if row.get('text')==b[key].get('text'):
                assert row==b[key],('Changed compatible vector',key);same+=1
            else:changed.append(key)
        if filename=='photo_prompt_semantic_index.json':assert set(changed)<=allowed_changed,(filename,changed)
        else:assert not changed
        index_proof[filename]=dict(before_entries=len(a),after_entries=len(b),exact_reused_entries=same,reviewed_changed_text_ids=changed,added_ids=sorted(set(b)-set(a)))
        for row in new['shards']:active[PHOTO+row['path']]=row['sha256']
    save(HERE/'INDEX-VECTOR-PRESERVATION.json',index_proof)
    source_after={name:sha(ROOT/name) for name in sorted(set(previous_proof['source_files_after'])|ADDED)}
    assert all(source_after[n]==s for n,s in previous_proof['source_files_after'].items() if n not in CHANGED)
    inventory={p.name:sha(p) for p in sorted((ROOT/PHOTO).glob('*.json'))}
    assert set(inventory)==set(previous_proof['source_inventory_after'])|{Path(n).name for n in ADDED}
    proof=dict(schema='photo-ethereal-data-transition/v35',parent_manifest=parent_path.relative_to(ROOT).as_posix(),parent_manifest_sha256=sha(parent_path),previous_qualified_commit=parent['source_pin'],previous_qualified_tree=parent['source_tree'],parent_member_count=parent['member_count'],previous_proof=OLD.relative_to(ROOT).as_posix(),previous_proof_sha256=sha(OLD),previous_manifest_sha256=sha(ILL/'photo_regression_baseline_v34.json'),previous_pack_sha256=sha(ILL/'photo_regression_baseline_v34_pack.json'),current_pack_sha256=sha(current_path),current_pack_id=current[0]['pack_id'],reviewed_pack_delta=changes,allowed_pack_delta_pointers=pointers,optional_candidate_change=dict(slot='light_shape',position=1,before_entry_id='monitor_rectangle_glow',after_entry_id='sparkling_water_reflection_highlights',reason='Global BM25F corpus statistics change after the reviewed additive DATA extension; both advisory candidates already existed upstream. No candidate adoption or hard duty was changed.'),added_source_paths=sorted(ADDED),changed_source_paths=sorted(CHANGED),source_files_after=source_after,source_inventory_before=previous_proof['source_inventory_after'],source_inventory_after=inventory,active_shards_after=active,retained_shards_before=previous_proof['active_shards_after'],frozen_inputs=old_baseline['frozen_inputs'],preserved_public_candidate_count=64,authored_counts=dict(candidates=60,profiles=41,optional_bundles=68,existing_context_enrichments=5),evidence_files={p.relative_to(ROOT).as_posix():sha(p) for p in [current_path,receipt_path,HERE/'INDEX-VECTOR-PRESERVATION.json',ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/ethereal-gothic-20261007-v1.json',ROOT/'docs/research-evidence/photo-prompt/extension-maintenance/ethereal-gothic-20261007-v2.json']},generation_id=receipt['generation_id'],source_fingerprint=receipt['source_fingerprint'],algorithm_sha256=receipt['algorithm_sha256'],previous_validator_sha256=records['skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py']['sha256'],previous_universal_descriptor_sha256=records['skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json']['sha256'],boundary='Authored DATA and exact current pack qualification; V1-V34 and original V34 tests replay from authenticated committed bytes. Native image verdicts remain the original 1 PASS/2 FAIL, with user judgment pending.')
    proof_path=HERE/'V35-ETHEREAL-DATA-PROOF.json';save(proof_path,proof)
    baseline=dict(old_baseline);baseline.pop('data_scope_transition');baseline.update(schema='photo_regression_baseline/v35',created_at='2026-10-07',historical_baseline=dict(path='photo_regression_baseline_v34.json',schema='photo_regression_baseline/v34',sha256=proof['previous_manifest_sha256']),change_scope='Add 60 optional candidates, 41 visual profiles, 68 optional bundles and five additive existing-entry contexts; preserve committed main authored sources and all original V1-V34 qualification.',sha256=proof['current_pack_sha256'],pack_id=proof['current_pack_id'],purpose=proof['boundary'])
    baseline['command']=list(old_baseline['command']);baseline['command'][baseline['command'].index('--output-file')+1]='/tmp/subculture-illustration-photo-baseline-v35.json'
    baseline['ethereal_data_transition']=dict(evidence_path=proof_path.relative_to(ROOT).as_posix(),evidence_sha256=sha(proof_path),previous_qualified_commit=parent['source_pin'],parent_manifest_sha256=sha(parent_path))
    (ILL/'photo_regression_baseline_v35_pack.json').write_bytes(current_path.read_bytes());save(ILL/'photo_regression_baseline_v35.json',baseline)
    print(json.dumps(dict(proof_sha256=sha(proof_path),parent_manifest_sha256=sha(parent_path),reviewed_pack_delta=len(changes),indices=index_proof),ensure_ascii=False))

if __name__=='__main__':main()
