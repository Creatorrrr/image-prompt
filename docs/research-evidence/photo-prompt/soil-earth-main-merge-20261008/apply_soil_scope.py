"""Apply only the qualified soil scope onto fetched main; preserve source identities."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

PRIMARY = Path('/Users/chasoik/Projects/image-prompt')
ROOT = Path.cwd()
SKILL = ROOT / 'skills/photo-prompt-image-generator'
OUT = ROOT / 'docs/research-evidence/photo-prompt/soil-earth-main-merge-20261008'
BEFORE = PRIMARY / OUT.relative_to(ROOT) / 'primary-scoped-before'
ORIGINAL = PRIMARY / 'docs/research-evidence/photo-prompt/soil-earth-semantics-20261008'
ARCHIVE = ROOT / ORIGINAL.relative_to(PRIMARY)
os.environ['PHOTO_RUNTIME_STORE'] = '/Users/chasoik/.cache/image-prompt/soil-earth-main-merge-20261008/runtime'
sys.path.insert(0, str(SKILL / 'scripts'))
from photo_runtime_sources import source_update

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read(path):
    return json.loads(Path(path).read_text())

def write(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

OUT.mkdir(parents=True, exist_ok=True)
assets = SKILL / 'assets'
manifest_path = assets / 'photo_prompt_source_manifest.json'
remote_manifest = read(manifest_path)
remote_sources = {row['file']: sha(assets / row['file']) for row in remote_manifest['sources'] if (assets / row['file']).is_file()}
water_path = assets / 'photo_prompt_visual_obligations_water_relations.json'
remote_water = read(water_path)
write(OUT / 'MAIN-MANIFEST-BEFORE.json', remote_manifest)
write(OUT / 'MAIN-WATER-BEFORE.json', remote_water)
original_water = read(ORIGINAL / 'integration/water-profiles.before.json')
local_water = read(BEFORE / water_path.relative_to(ROOT))
before_by_id = {p['id']: p for p in original_water['profiles']}
local_by_id = {p['id']: p for p in local_water['profiles']}
water_deltas = {}
for pid, before in before_by_id.items():
    after = local_by_id[pid]
    if before == after:
        continue
    old_phrases = before['semantics'].get('paraphrase_examples', [])
    new_phrases = after['semantics'].get('paraphrase_examples', [])
    assert new_phrases[:len(old_phrases)] == old_phrases
    restored = json.loads(json.dumps(after))
    restored['semantics']['paraphrase_examples'] = old_phrases
    assert restored == before, pid
    water_deltas[pid] = new_phrases[len(old_phrases):]
assert set(water_deltas) == {'water_rel_w002', 'water_rel_w069', 'water_rel_w070', 'water_rel_w077', 'water_rel_w120'}

copied_evidence = []
excluded = []
for directory, dirs, files in os.walk(ORIGINAL):
    if 'runtime-store' in dirs:
        excluded.append(str((Path(directory) / 'runtime-store').relative_to(PRIMARY)))
        dirs.remove('runtime-store')
    dirs[:] = [d for d in dirs if d != '__pycache__']
    for name in files:
        source = Path(directory) / name
        if source.is_symlink() or name.endswith('.LOCK'):
            excluded.append(str(source.relative_to(PRIMARY)))
            continue
        target = ARCHIVE / source.relative_to(ORIGINAL)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        assert sha(source) == sha(target)
        assert source.stat().st_mode & 0o777 == target.stat().st_mode & 0o777
        copied_evidence.append({'path': str(target.relative_to(ROOT)), 'sha256': sha(target), 'mode': oct(target.stat().st_mode & 0o777)})

new_names = ['photo_prompt_soil_earth_extension.json', 'photo_prompt_visual_obligations_soil_earth.json']
with source_update(SKILL):
    for name in new_names:
        source = BEFORE / 'skills/photo-prompt-image-generator/assets' / name
        shutil.copy2(source, assets / name)
        assert sha(source) == sha(assets / name)
    next_orders = {kind: max(row['load_order'] for row in remote_manifest['sources'] if row['kind'] == kind) + 1 for kind in ['candidate', 'visual_profile']}
    additions = []
    for name, kind in zip(new_names, ['candidate', 'visual_profile']):
        assert not any(row['file'] == name for row in remote_manifest['sources'])
        additions.append({'file': name, 'kind': kind, 'required': True, 'load_order': next_orders[kind]})
    remote_manifest['sources'].extend(additions)
    write(manifest_path, remote_manifest)
    remote_by_id = {p['id']: p for p in remote_water['profiles']}
    for pid, phrases in water_deltas.items():
        target_phrases = remote_by_id[pid]['semantics'].setdefault('paraphrase_examples', [])
        for phrase in phrases:
            if phrase not in target_phrases:
                target_phrases.append(phrase)
    write(water_path, remote_water)
    # This exact completed index is an input cache, not the merged final index.
    # The canonical builder will recompute text, BM25F and metadata for this main corpus.
    seed_path = BEFORE / 'skills/photo-prompt-image-generator/assets/photo_prompt_semantic_index.json'
    seed = read(seed_path)
    for shard in seed['shards']:
        relative = Path(shard['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        source = PRIMARY / 'skills/photo-prompt-image-generator/assets' / relative
        assert sha(source) == shard['sha256']
        target = assets / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    shutil.copy2(seed_path, assets / seed_path.name)

test_relative = Path('tests/test_photo_soil_earth_relations.py')
shutil.copy2(BEFORE / test_relative, ROOT / test_relative)
preserved = []
for name, before_sha in remote_sources.items():
    if name == water_path.name:
        continue
    assert sha(assets / name) == before_sha, name
    preserved.append({'file': name, 'sha256': before_sha})
old_water = read(OUT / 'MAIN-WATER-BEFORE.json')
old_by_id = {p['id']: p for p in old_water['profiles']}
new_by_id = {p['id']: p for p in read(water_path)['profiles']}
for pid, old in old_by_id.items():
    now = new_by_id[pid]
    if pid not in water_deltas:
        assert now == old
    else:
        old_phrases = old['semantics'].get('paraphrase_examples', [])
        assert now['semantics']['paraphrase_examples'][:len(old_phrases)] == old_phrases
        restored = json.loads(json.dumps(now))
        restored['semantics']['paraphrase_examples'] = old_phrases
        assert restored == old
assert read(manifest_path)['sources'][:-2] == read(OUT / 'MAIN-MANIFEST-BEFORE.json')['sources']
proof = {
    'main_base': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
    'new_soil_sources': {name: sha(assets / name) for name in new_names},
    'new_registration_rows': additions, 'main_rows_unchanged': True,
    'main_authored_sources_preserved': preserved, 'water_append_only_deltas': water_deltas,
    'water_other_fields_and_existing_phrases_preserved': True,
    'archive_files_copied_unchanged': copied_evidence, 'archive_excluded_retained_on_primary': excluded,
    'unrelated_primary_changes_imported': False,
    'index_cache_policy': 'Exact provider/model/dimensions and complete per-entry text only; canonical build required.',
    'native_evidence_scope': 'Original three runs remain immutable observations of their pinned generation; no reinterpretation against merged main.',
}
write(OUT / 'AUTHORED-PRESERVATION.json', proof)
print(json.dumps({'status': 'applied', 'main_sources_preserved': len(preserved), 'water_profiles_append_only': len(water_deltas), 'archived_files_unchanged': len(copied_evidence), 'new_registrations': additions}, ensure_ascii=False))
