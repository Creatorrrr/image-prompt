"""Check the selected union against the actual image pin and latest parent."""
from pathlib import Path
import hashlib, json, sys, subprocess, datetime, collections
import gc
gc.disable()

O = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/Projects/image-prompt')
U = O/'union-current'
def read(p): return json.loads(Path(p).read_bytes())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p, x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

B = read(U/'before.json'); S = read(U/'successor.json'); I = read(U/'install-active.json')
assert I['status'] == 'pass' and I['generation_id'] == S['generation_id']
config_path = ROOT/'skills/photo-prompt-image-generator/retrieval-runtime.json'
active = read(config_path)
assert active['generation_id'] == S['generation_id'] and active['native_generation_id'] == S['native_generation_id']
store = Path(I['store']); current = store/'generations'/S['native_generation_id']
parent = Path(B['native'])
tested = store/'generations'/'eeaafc1952af220bd23823e72fcd1b1fadca8048f8ac334e08e7edbb25705d9a'
old_m = read(parent/'manifest.json'); new_m = read(current/'manifest.json'); test_m = read(tested/'manifest.json')
assert old_m['source']['code'] == new_m['source']['code'] == test_m['source']['code']
assert old_m['source']['environment'] == new_m['source']['environment'] == test_m['source']['environment'] == {'implementation':'cpython','python':[3,14,3],'unicode':'16.0.0'}
module = 'photo_candidate_court_palace_full_review_20261023.json'
binding = 'photo_candidate_court_palace_full_review_bindings_20261023.json'
new_files = {module,binding}
assert all(sha(current/'assets'/n) == sha(tested/'assets'/n) for n in new_files)
old_source = read(parent/'assets/photo_candidate_corpus_manifest.json')
new_source = read(current/'assets/photo_candidate_corpus_manifest.json')
assert new_source['modules'] == old_source['modules'] + [{'file':module,'kind':'candidates'},{'file':binding,'kind':'slot_bindings'}]
for entry in old_source['modules']:
    assert sha(parent/'assets'/entry['file']) == sha(current/'assets'/entry['file']), entry
sys.path.insert(0,str(current/'scripts'))
import photo_canonical_source as canonical
fresh = read(O/'new-native-records.json')
actual = read(current/'assets'/module)['candidates']
assert set(actual) == set(fresh) and len(actual) == 24
assert all(canonical.native_snapshot(actual[cid]) == r for cid,r in fresh.items())
raw_assets = ROOT/'skills/photo-prompt-image-generator/assets'
assert read(raw_assets/module)['candidates'] == fresh
assert sha(raw_assets/module) == read(O/'PREIMAGE-TEST-PLAN.json')['source_module_file_sha256']
raw_files = {x['file'] for x in read(raw_assets/'photo_candidate_corpus_manifest.json')['modules']}
assert new_files <= raw_files
raw_bindings = read(ROOT/'skills/photo-prompt-image-generator/assets'/binding)
actual_bindings = read(current/'assets'/binding)
assert raw_bindings['slot_bindings'] == actual_bindings['slot_bindings']
assert len(actual_bindings['slot_bindings']) == 35
preservation = read(U/'canonical-source-validation.json')
assert preservation['status'] == 'pass' and preservation['reviewed_source_updated_CIDs'] == 0
qualification = read(U/'retrieval-qualification.json')['summary']
assert qualification['status'] == 'pass' and qualification['target_at10'] == 36 and qualification['queries'] == 60
protected_drift = []
for rel, prior in B['protected_file_hashes'].items():
    if rel == 'skills/photo-prompt-image-generator/retrieval-runtime.json':
        continue  # The one intentional selection write was checked above.
    p = ROOT/rel
    if not p.is_file() or sha(p) != prior: protected_drift.append(dict(path=rel,before=prior,after=sha(p) if p.is_file() else None))
assert not protected_drift, protected_drift
head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head == B['HEAD']
status = subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=no'],cwd=ROOT,text=True)
summary = dict(schema='court-r2-final-union-verification/v1',status='pass',verified_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    active_config=active, parent_config=B['config'], image_test_h2_generation='265a75945bda1a1aea3b26ca88e13ab0dcb3139d22ae85197ed2d478ee3f2978',
    source_modules_byte_identical_to_image_test=True,new_native_snapshots_exact=24,new_bindings_exact=35,
    all_latest_parent_source_modules_byte_identical=True,existing_canonical_records_preserved=preservation['old_CIDs'],
    kernel_environment_and_code_equal_to_parent_and_image_test=True,protected_source_files_unchanged=len(B['protected_file_hashes'])-1,
    authorized_default_selection_write_verified=True,
    retrieval_qualification=qualification,HEAD=head,commit_push_pr=False,tracked_dirty_paths=len(status.splitlines()),
    dirty_status_counts=dict(collections.Counter(line[:2] for line in status.splitlines())),
    limits='Images were generated on the stated pinned release. This larger selected union preserves the exact tested sources but its whole-pool results and sampling are not claimed identical. Current state is a point-in-time observation; no unrelated changes were reset.')
write(O/'final-union-verification.json',summary)
print(json.dumps(summary,ensure_ascii=False))
