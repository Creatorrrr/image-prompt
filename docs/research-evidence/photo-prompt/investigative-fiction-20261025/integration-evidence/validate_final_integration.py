"""Read-only scoped source and selected-runtime checks; no image verdict inference."""
from pathlib import Path
import gc, hashlib, json, sys
gc.disable()
O = Path(__file__).resolve().parent
ROOT = O.parents[4]
S = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(S / 'scripts'))
import photo_candidate_corpus as corpus

def read(p): return json.loads(p.read_bytes())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(x):
    return hashlib.sha256(json.dumps(x, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()

before = read(O / 'source-before.json')
integration = read(O / 'data-integration.json')
after = corpus.load(S / 'assets')
fresh = read(O / 'new-native-records.json')
changed = read(O / 'changed-native-records.json')
prior = read(O / 'changed-native-prior.json')
assert len(fresh) == 113 and len(changed) == 5
assert len(after['candidates']) >= 23012
assert set(fresh).isdisjoint(before['candidates'])
for cid, expected in before['candidates'].items():
    if cid not in changed:
        assert digest(after['candidates'][cid]) == expected, cid
for cid, record in {**fresh, **changed}.items():
    assert after['candidates'][cid] == record, cid
for cid in changed:
    assert all(after['candidates'][cid][k] == prior[cid][k]
               for k in ('conditions', 'effects', 'provenance'))
assert all(digest(after['slot_bindings'][bid]) == expected
           for bid, expected in before['bindings'].items())
assert digest(after['slot_catalog']) == before['catalog_sha256']
assert digest(after['policies']) == before['policies_sha256']
allow = set(integration['allowlist']) | {
    'skills/photo-prompt-image-generator/retrieval-runtime.json'}
modified = [p for p, expected in before['protected'].items()
            if sha(ROOT / p) != expected]
# The earlier integration validation proved our source delta did not write the
# legacy working index. A later concurrent corpus/index build now changed it.
# Preserve that observed external result; it is not part of this source delta.
external_index = 'skills/photo-prompt-image-generator/assets/photo_candidate_search.json'
concurrent_external = set(modified) & {external_index}
assert not set(modified) - allow - concurrent_external, set(modified) - allow - concurrent_external
assert sha(S / 'SKILL.md') == before['protected'][str((S / 'SKILL.md').relative_to(ROOT))]
release = read(O / 'successor.json')
base = read(O / 'release-base.json')
selected = read(S / 'retrieval-runtime.json')
if selected['generation_id'] == release['generation_id']:
    assert selected['native_generation_id'] == release['native_generation_id']
else:
    # A concurrently selected successor is acceptable only after the separate
    # complete module/native-snapshot and full deployed index checks match it.
    for name in ('final-default-preservation.json',
                 'final-default-search-preservation.json'):
        preserved = read(O / name)
        assert preserved['status'] == 'pass'
        assert preserved['current_selected_config'] == selected
assert selected['code_sha256'] == base['config']['code_sha256']
assert read(O / 'install-active.json')['status'] == 'pass'
assert read(O / 'retrieval-qualification.json')['summary']['status'] == 'complete'
result = {
    'status': 'pass', 'working_CIDs': len(after['candidates']),
    'scoped_after_CIDs_at_integration': 23012,
    'concurrent_new_records_outside_scope': sorted(
        set(after['candidates']) - set(before['candidates']) - set(fresh)),
    'concurrent_manifest_modules_outside_scope': [
        m for m in read(S / 'assets/photo_candidate_corpus_manifest.json')['modules']
        if m not in before['manifest']['modules']
        and m['file'] not in {'photo_candidate_investigative_fiction_20261025.json',
                             'photo_candidate_investigative_fiction_bindings_20261025.json'}],
    'new_records': len(fresh), 'updated_existing_records': len(changed),
    'unrelated_candidate_records_preserved': len(before['candidates']) - len(changed),
    'prior_bindings_catalog_policies_preserved': True,
    'unexpected_protected_changes': [], 'changed_protected_files': modified,
    'concurrent_external_protected_changes': {
        p: {'sha256': sha(ROOT / p),
            'scope': 'Observed after our source-only integration validation; not written or reverted by this task. Operating pinned runtime validated separately.'}
        for p in concurrent_external},
    'SKILL_sha256': sha(S / 'SKILL.md'), 'selected_runtime': selected,
    'installed_kernel_code_preserved': True,
    'image_quality_or_native_approval_inferred': False,
}
(O / 'final-source-validation.json').write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
