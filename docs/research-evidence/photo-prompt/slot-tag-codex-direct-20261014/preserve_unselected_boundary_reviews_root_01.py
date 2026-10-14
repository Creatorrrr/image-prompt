"""Preserve exact unselected proposals and their real proof boundaries."""
import ast
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
names = [
    'authored/native_1299_hands_exchange_application_proposal_01.json',
    'authored/native_1299_hands_exchange_application_proposal_01.literal.py',
    'authored/native_1299_hands_exchange_application_proposal_02.json',
    'authored/native_1299_hands_exchange_application_proposal_02.literal.py',
    'authored/native_1299_hands_exchange_application_proposal_03.json',
    'authored/native_1299_hands_exchange_application_proposal_03.py',
    'worker-notes/native-1299-hands-exchange-application-review-20261015-01.json',
    'worker-notes/native-1299-hands-exchange-application-review-20261015-01.md',
    'worker-notes/native-1299-hands-exchange-application-shape-20261015-01.py',
    'worker-notes/native-1299-hands-exchange-application-shape-20261015-01.log',
    'worker-notes/native-1299-hands-exchange-application-shape-20261015-02.py',
    'worker-notes/native-1299-hands-exchange-application-shape-20261015-02.log',
    'worker-notes/native-1299-hands-exchange-application-shape-20261015-02.json',
    'authored/native_12250_catalog_footwear_sock_9428_proposal_20261015.json',
    'authored/native_12250_catalog_footwear_sock_9428_proposal_20261015.py',
    'worker-notes/native_12250_catalog_footwear_sock_9428_proposal_20261015.json',
    'check_1299_scope_proposal_root_03.py',
    'ROOT-1299-SCOPE-PROPOSAL-SHAPE-03.json',
    'ROOT-1299-SCOPE-PROPOSAL-SHAPE-03-FAILED-ATTEMPT-01.json',
    Path(__file__).name,
]
pins = {}
for name in names:
    path = HERE / name
    raw = path.read_bytes()
    if path.suffix == '.json': json.loads(raw)
    if path.suffix == '.py': ast.parse(raw)
    pins[str(path.relative_to(ROOT))] = hashlib.sha256(raw).hexdigest()
assert pins[str((HERE / names[2]).relative_to(ROOT))] == '8276595d82f95a0b9e656daa0e3374181729b3c8d1bda55f24d501b55d1080f0'
assert pins[str((HERE / names[4]).relative_to(ROOT))] == '7cadf761e6618b75b66341ce4fa9365687a4eecb92839bc26b53bb36726710e6'
assert pins[str((HERE / names[13]).relative_to(ROOT))] == 'fe7a469e2c46ad4e52e79c9d00cf9c91d657a0e6cf6af0926e9b594aa8b3483e'
catalog = json.loads((HERE / 'CATALOG-FINAL-149-V6.json').read_bytes())
footwear = json.loads((HERE / names[13]).read_bytes())
assert footwear['exact_before'] == catalog['footwear']
assert footwear['slot_count_before'] == footwear['slot_count_if_adopted'] == 149
assert json.loads((HERE / names[17]).read_bytes())['checks_passed'] == 7
report = {
    'schema': 'photo-root-unselected-boundary-review-preservation/v1', 'actor': '/root', 'files': pins,
    'candidate1299': {
        'decision': 'pending_no_source_choice_selected',
        'root_read_boundary': 'Whole original/current1299, actual binding and old49th pending row; whole proposed after02 and03, all02 P/E intents and03 owner map; actual permission/owner-scope code and12 named149 fullspecs. No root claim to read all01 alternatives or all19 worker specs.',
        'meaning': 'An item handoff is a deliberate narrower application of ambiguous exchange. Proposal03 changes EN/KO to disclose that choice and adds an independent complete framing receiver inventory. Existing member provenance checks do not prove semantic completeness.',
        'checks': 'Worker6 shape checks for01/02; root7 frozen50fd92 shape checks for03. No actual source proof, admission, complete receiver/lock or runtime qualification.',
        'next': 'Fresh direct source/proposal review and actual independently grounded framing union tests before root source selection and new prepared input. Old first50 pending status remains unchanged.',
    },
    'footwear9428': {
        'decision': 'do_not_adopt_sock_family_extension_now_keep149V6',
        'root_read_boundary': 'Complete before/after footwear plus current garment_detail, wardrobe_style, wearable_accessory, garment_state and garment_fit fullspecs;9428/9463 positive source content and complete old5B rows. Repeated original/current/5Bafter/binding copies compared exactly; closure empty. Other worker10 fullspec reading is delegated provenance.',
        'meaning': 'The actual sock upper edge and same-knee relationship can use garment_detail. Combining socks with shoes but excluding other declared hosiery needs a consolidated garment-kind boundary decision. Neither a shoe nor footwear.type is invented from a sock hem.',
        'next': 'Preserve actual9428/9502 garment kind and local structure; collect garment-type scope alternatives after bulk review. No mandatory second tag or automatic old5B role import.',
    },
    'root_source_changes_accepted': 0, 'native_proofs_created': 0, 'catalog_changes': 0,
    'operating_changes': 0, 'Gemini_calls': 0, 'proof_boundary': 'Preservation and schema/hash checks confer no candidate semantic or native approval.',
}
output = HERE / 'ROOT-UNSELECTED-BOUNDARY-REVIEWS-01.json'
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=ROOT).strip()
with output.open('x') as stream:
    json.dump(report, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
paths = sorted(set(pins) | {str(output.relative_to(ROOT))})
subprocess.run(['git', 'add', '--', *paths], cwd=ROOT, check=True)
subprocess.run(['git', 'diff', '--cached', '--check'], cwd=ROOT, check=True)
for name in paths:
    assert subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT) == (ROOT / name).read_bytes(), name
print(json.dumps({'preserved_files': len(paths), 'source_choices_accepted': 0, 'native_proofs_created': 0}))
