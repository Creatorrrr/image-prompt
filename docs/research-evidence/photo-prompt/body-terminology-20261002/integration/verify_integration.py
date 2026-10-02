"""Receipt the live corpus, generated indexes and preserved legacy contracts."""
import hashlib
import copy
import json
from pathlib import Path
import subprocess
import sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[4]
ASSETS=ROOT/'skills/photo-prompt-image-generator/assets'
sys.path.insert(0,str(ASSETS.parent/'scripts'))
import prompt_generator as pg

baseline=json.loads((OUT/'BASELINE.json').read_text())
manifest=json.loads((OUT/'INTEGRATION-MANIFEST.json').read_text())
registry=pg.load_visual_obligation_registry(ASSETS/'photo_prompt_visual_obligations.json')
data=pg.load_json(ASSETS/'photo_prompt_tags.json')
profiles={p['id']:p for p in registry['profiles']}
candidates={slot:{e['id']:e for e in entries} for slot,entries in data['slots'].items()}
assert set(baseline['profile_ids'])<=set(profiles)
assert all(set(ids)<=set(candidates[slot]) for slot,ids in baseline['candidate_ids'].items())

def old_document(name):
    path=ASSETS/name
    rel=str(path.relative_to(ROOT))
    return json.loads(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT,text=True))

old_docs={name:old_document(name) for name in manifest['changed_existing_assets']}
preserved=[]
unchanged_profiles=[]
for row in manifest['crosswalk']:
    if row['profile_action']=='new_independent_axis': continue
    original=next(p for p in old_docs[row['profile_source']]['profiles'] if p['id']==row['profile_id'])
    authored=json.loads((ASSETS/row['profile_source']).read_text())
    live=next(p for p in authored['profiles'] if p['id']==row['profile_id'])
    old_contract=copy.deepcopy(original)
    live_contract=copy.deepcopy(live)
    for container,field in [('semantics','paraphrase_examples'),('concept_candidate','concept_terms')]:
        old_values=old_contract[container].pop(field)
        live_values=live_contract[container].pop(field)
        assert live_values[:len(old_values)]==old_values,(row['profile_id'],field)
    assert live_contract==old_contract,(row['profile_id'],'authored contract changed')
    if live == original:
        unchanged_profiles.append(row['profile_id'])
    preserved.append(row['profile_id'])

assert set(unchanged_profiles)=={'inner_thigh_negative_space','pfe_cleavage',
    'pfe_midriff','pfe_lateral_chest','pfe_lower_chest'}

visual_index=pg.load_visual_profile_index(ASSETS/'photo_prompt_visual_profile_index.json',registry)
semantic_index=pg.load_semantic_index_payload(ASSETS/'photo_prompt_semantic_index.json')
pg.validate_semantic_index_metadata(semantic_index,data)
assert len(profiles)==1496
assert sum(map(len,candidates.values()))==9664
assert len(semantic_index['entries'])==9700
assert set(semantic_index['entries'])=={key for key,_,_,_ in pg.iter_semantic_entries(data)}

source_paths=[ASSETS/'photo_prompt_tags.json',ASSETS/'photo_prompt_visual_obligations.json',
    *[ASSETS/name for name in pg.RESEARCH_EXTENSION_FILENAMES],
    *[ASSETS/name for name in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES],
    ASSETS.parent/'scripts/prompt_generator.py',ASSETS.parent/'references/retrieval-contract.md']
sources=[dict(path=str(path.relative_to(ROOT)),bytes=path.stat().st_size,
    sha256=hashlib.sha256(path.read_bytes()).hexdigest()) for path in source_paths]
receipt=dict(schema_version='body-morphology-live-integration-receipt/v1',status='PASS',
    baseline_profiles=baseline['registry_profiles'],current_profiles=len(profiles),
    baseline_candidates=baseline['candidate_entries'],current_candidates=sum(map(len,candidates.values())),
    slot_count=len(candidates),semantic_index_entries=len(semantic_index['entries']),
    preserved_baseline_ids=True,preserved_enriched_profile_contracts=preserved,
    exactly_reused_profile_contracts=unchanged_profiles,
    integrated_planned_axes=91,supplemental_axes=['skin_piloerection'],
    new_profiles=77,enriched_profiles=10,reused_unchanged_profiles=5,
    new_candidates=74,enriched_candidates=18,structured_base_enrichments=13,
    equivalent_context_overlays=5,
    supplemental_paraphrase_families=12,
    visual_registry_sha256=visual_index['registry_sha256'],
    dictionary_hash=semantic_index['dictionary_hash'],
    vector_space=dict(provider=semantic_index.get('provider'),model=semantic_index.get('embedding_model'),
                      dimensions=semantic_index.get('embedding_dimensions')),
    sources=sources,
    boundary='This receipt validates source, metadata and preserved contracts; image quality and user acceptance are separate.')
(OUT/'LIVE-INTEGRATION-RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in {'sources','preserved_enriched_profile_contracts'}},ensure_ascii=False))
