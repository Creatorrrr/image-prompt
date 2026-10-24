"""Read-only retention comparison; does not select or mutate any runtime."""
from pathlib import Path
import json, hashlib, gzip, datetime

R = Path('/Users/chasoik/Projects/image-prompt')
O = Path(__file__).resolve().parent
store = Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed'
selected = json.loads((R/'skills/photo-prompt-image-generator/retrieval-runtime.json').read_text())
published = json.loads((O/'publication/code-successor.json').read_text())
native = store/'generations'/selected['native_generation_id']
publication = store/'generations'/published['native_generation_id']
result = {
    'status': 'pass',
    'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'selected_generation': selected['generation_id'],
    'selected_native_generation': selected['native_generation_id'],
    'our_publication_generation': published['generation_id'],
    'default_advanced_concurrently': selected['generation_id'] != published['generation_id'],
    'topic_assets': {},
}
for name in ['photo_candidate_romcom_20261024.json', 'photo_candidate_romcom_bindings_20261024.json']:
    current = native/'assets'/name
    assert current.read_bytes() == (publication/'assets'/name).read_bytes(), name
    result['topic_assets'][name] = {'same_as_publication': True, 'sha256': hashlib.sha256(current.read_bytes()).hexdigest()}
current_manifest = json.loads((native/'manifest.json').read_text())
published_manifest = json.loads((publication/'manifest.json').read_text())
same_code = current_manifest['source']['code'] == published_manifest['source']['code']
result['runtime_code_exactly_same'] = same_code
result['runtime_code_changed_concurrently'] = not same_code
result['test_transactions_remain_bound_to_original_test_release'] = True
records = json.loads((native/'assets/photo_candidate_romcom_20261024.json').read_text())['candidates']
positive = {cid for cid, record in records.items() if record['record_kind'] != 'diagnostic'}
diagnostics = set(records)-positive
index = json.loads(gzip.decompress((store/'h-f2-generations'/selected['generation_id']/'indexed-documents.json.gz').read_bytes()))
ids = {row['cid'] for row in index}
assert positive <= ids and diagnostics.isdisjoint(ids)
semantics = R/'skills/photo-prompt-image-generator/assets/photo_romcom_semantics_20261024.json'
assert semantics.read_bytes() == (O/'publication/successor-skill/assets'/semantics.name).read_bytes()
result['authored_semantics'] = {'sha256': hashlib.sha256(semantics.read_bytes()).hexdigest(), 'same_as_publication_source': True, 'native_manifest_member': False}
skill = R/'skills/photo-prompt-image-generator/SKILL.md'
used_skill = O/'SKILL-used.md'
skill_sha = hashlib.sha256(skill.read_bytes()).hexdigest()
used_sha = hashlib.sha256(used_skill.read_bytes()).hexdigest()
assert used_sha == '83b3239eda5b5e26b1c51dad268258eb21a24f3dbca3b814517eb89169390cb8'
required_starts = ('For a scene whose meaning depends on a small discrepancy,', 'Give each consequential contact an observable target')
for prefix in required_starts:
    paragraph = next(line for line in used_skill.read_text().splitlines() if line.startswith(prefix))
    assert paragraph in skill.read_text(), prefix
result.update(romcom_records=len(records), positive_indexed=len(positive), diagnostics_excluded=len(diagnostics), bindings=len(json.loads((native/'assets/photo_candidate_romcom_bindings_20261024.json').read_text())['slot_bindings']), image_test_skill_sha256=used_sha, current_skill_sha256=skill_sha, current_skill_changed_concurrently=skill_sha != used_sha, our_skill_guidance_paragraphs_retained=True)
(O/'selected-default-retention-verification.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
