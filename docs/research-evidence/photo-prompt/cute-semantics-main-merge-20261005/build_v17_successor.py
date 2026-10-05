"""Seal the real cute DATA successor; preserve V1-V16 and the frozen scene."""
import copy
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path.cwd()
HERE = ROOT / 'docs/research-evidence/photo-prompt/cute-semantics-main-merge-20261005'
ASSETS = ROOT / 'skills/subculture-illustration-image-generator/assets'
PHOTO = ROOT / 'skills/photo-prompt-image-generator'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
parent = json.loads((HERE / 'PARENT-HISTORY.json').read_text())
previous = ASSETS / 'photo_regression_baseline_v16.json'
previous_pack = ASSETS / 'photo_regression_baseline_v16_pack.json'
raw = (HERE / 'V17-PACK-CAPTURE.json').read_bytes()
pack = json.loads(raw)[0]
old = copy.deepcopy(json.loads(previous_pack.read_bytes())[0])
current = copy.deepcopy(pack)
deltas = []
for path in [('core_retrieval','canonical_sha256'),('core_retrieval','slot_corpus_sha256'),
             ('core_retrieval','slot_ownership_sha256'),('pack_id',),('provenance','tags_hash')]:
    left, right = old, current
    for key in path[:-1]:left,right=left[key],right[key]
    key=path[-1]
    assert left[key] != right[key]
    deltas.append(dict(path='/'+'/'.join(path),previous=left[key],current=right[key]))
    del left[key],right[key]
assert old == current
data_commit = subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
files = [p for p in PHOTO.rglob('*') if p.is_file() and '__pycache__' not in p.parts
         and '/photo_prompt_semantic_index_shards/' not in str(p)
         and p.suffix in {'.json','.py','.md'}]
index = json.loads((PHOTO/'assets/photo_prompt_semantic_index.json').read_text())
shards = {str((PHOTO/'assets'/r['path']).relative_to(ROOT)):sha(PHOTO/'assets'/r['path']) for r in index['shards']}
proof = dict(schema='photo-cute-equivalent-language-inventory-transition/v17',
    data_commit=data_commit,data_parent_commit=parent['parent_commit'],
    previous_manifest_sha256=sha(previous),previous_pack_sha256=sha(previous_pack),
    current_pack_sha256=hashlib.sha256(raw).hexdigest(),current_pack_id=pack['pack_id'],
    public_candidate_count=64,reviewed_binding_deltas=deltas,
    candidate_objects_order_and_all_other_pack_fields_equal=True,
    immutable_history=parent['immutable_history'],
    source_parent_archive=str((HERE/parent['archive']).relative_to(ROOT)),
    source_parent_archive_sha256=parent['archive_sha256'],
    source_files={str(p.relative_to(ROOT)):sha(p) for p in sorted(files)},
    source_inventory_after={p.name:sha(p) for p in sorted((PHOTO/'assets').glob('*.json'))},
    active_semantic_shards=shards,
    reviewed_authored_delta=dict(existing_candidate_targets=67,positive_candidate_paraphrases=134,
        new_narrow_candidates=15,new_visual_profiles=26,new_optional_bundles=26,
        existing_profiles_enriched=11),
    previous_validator_sha256=parent['archived_source_hashes']['skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py'],
    universal_v2_before_sha256=parent['archived_source_hashes']['skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json'])
proof_path=HERE/'V17-CUTE-DATA-PROOF.json'
proof_path.write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
baseline=json.loads(previous.read_text())
for key in ['authored_metadata_ownership_transition','metadata_only_transition','zero_pack_delta_transition','optional_inventory_transition']:
    baseline.pop(key,None)
baseline.update(schema='photo_regression_baseline/v17',status='current',
    historical_baseline=dict(path=previous.name,schema='photo_regression_baseline/v16',sha256=sha(previous)),
    change_scope='Reviewed equivalent-language and narrow-form DATA inventory; five frozen-pack bindings only.',
    purpose='Preserve the frozen scene, candidates/order, controls, negative and privacy while binding the merged cute DATA.',
    sha256=proof['current_pack_sha256'],pack_id=pack['pack_id'],
    cute_equivalent_language_inventory_transition=dict(data_commit=data_commit,data_parent_commit=parent['parent_commit'],
        evidence_sha256=sha(proof_path),source_files=proof['source_files']))
(ASSETS/'photo_regression_baseline_v17_pack.json').write_bytes(raw)
(ASSETS/'photo_regression_baseline_v17.json').write_text(json.dumps(baseline,ensure_ascii=False,indent=2)+'\n')
print('V17 proof SHA',sha(proof_path),'DATA',data_commit)
