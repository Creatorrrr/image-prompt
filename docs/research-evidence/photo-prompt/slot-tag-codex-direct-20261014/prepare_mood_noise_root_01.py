"""Two individually read literal source selections; no proof or native approval."""
import copy
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode = True
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(R))
import prepare_native_inputs as prep
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
assert Path(prep.reviews.native.__file__).resolve().is_relative_to(G)

def read(path):
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())

def save(path, value):
    with path.open('xb') as stream:
        stream.write(c.canonical_bytes(value) + b'\n')

def ref(path):
    return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'sha256': c.digest(read(path))}

parent = R / 'native-inputs/catalog149-source-pool-plan-09'
current = read(parent / 'CURRENT-PROPOSAL.json.gz')
original = read(R / 'SOURCE.json.gz')
assert c.digest(current) == '5ee63da71e477de1d52677fa768dd715eb6589c6f0f77ac213c11825b0c2fd44'
assert c.digest(original) == '125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
proposal_path = R / 'authored/native_09250_02250_03250.formal-feasibility-001.json'
assert hashlib.sha256(proposal_path.read_bytes()).hexdigest() == 'bdf1674d5a6b53f5ab3d225d89a98c571083a404a7b79c8ec45c25a335b153eb'
proposal = read(proposal_path)
selected = [row for row in proposal['records'] if row['ordinal'] in [3107, 3169]]
assert [row['ordinal'] for row in selected] == [3107, 3169]
D = R / 'native-inputs/root-mood-noise-source-plan-11'
D.mkdir(exist_ok=False)
reasons = {
    3107: 'Select the exact existing mood wording and precise scene atmosphere property. Emotional burnout/reset interpretation remains an actual mood effect; no clinical diagnosis, private emotion or performed reorganizing action is claimed. KO is only a partial restatement of the full EN/embedding value and must not independently certify every English qualifier.',
    3169: 'Select exact ISO3200 noise appearance and the existing image-plane application explanation. Rename only the coarse image-plane noise address to the exact image.noise carrier property; preserve style effect and literal ISO qualifier. No measured capture ISO, low-light scene, physical particles, sensor identity or film-stock claim.',
}
memo = {'schema': 'photo-root-two-literal-source-selection/v1', 'actor': '/root',
        'proposal': ref(proposal_path), 'selected_ordinals': [3107, 3169],
        'decisions': [{'ordinal': row['ordinal'], 'candidate_id': row['candidate_id'], 'reason': reasons[row['ordinal']]} for row in selected],
        'read_scope': 'Root read both complete original/current records, exact compiled5B rows, full proposed afters, own bindings, empty closures, frozen draft facts/units and mood/grain/film/material/color specs. This is two source choices for fresh review, not automatic acceptance of the five-row feasibility draft.',
        'requirements': ['Fresh source-local manual facts, owner maps, units, roles and full/compact consumer/lock checks on frozen50fd92.',
                         '3107 KO must use a bounded partial reference or its exact weaker own fact; preserve complete tired-but-reorganizing EN/embedding mood E.',
                         '3169 remains image noise appearance. No source body or literal ISO qualifier deletion; actual binding denies product/jewelry/food.',
                         '3179 green-cast is not selected in this change. Review actual protected local color and complete affected receiver/preservation scope before claiming complete native qualification.',
                         'No old proof/status re-sign, forced extra role or operating activation.'],
        'new_native_proofs': 0, 'operating_changes': 0, 'Gemini_calls': 0}
save(D / 'ROOT-SOURCE-SELECTION.json', memo)
approval = read(parent / 'SOURCE-APPROVAL.json')
for row in selected:
    cid = row['candidate_id']
    assert row['source_before'] == current['candidates'][cid] == original['candidates'][cid]
    after = copy.deepcopy(row['frozen_proposed_after'])
    assert after['conditions'] == row['source_before']['conditions'] and after['provenance'] == row['source_before']['provenance']
    current['candidates'][cid] = after
    delta = [{'pointer': '/' + key, 'before_exists': True, 'before': row['source_before'][key],
              'after_exists': True, 'after': after[key], 'reason': reasons[row['ordinal']]}
             for key in row['source_before'] if row['source_before'][key] != after[key]]
    approval['changes'].append({'candidate_id': cid, 'before': row['source_before'], 'after': after, 'delta': delta,
                                'reason': reasons[row['ordinal']], 'provenance': [ref(proposal_path), ref(D / 'ROOT-SOURCE-SELECTION.json')]})
approval['current_source_sha256'] = c.digest(current)
approval['reason'] += ' Add exactly two individually root-read mood/noise source-property corrections for fresh review. No third green-cast or1299 source choice, new proof or operating change.'
prep.approve_source(ROOT, original, current, approval)
c.validate(current)
with (D / 'CURRENT-PROPOSAL.json.gz').open('xb') as stream:
    stream.write(gzip.compress(c.canonical_bytes(current), mtime=0))
save(D / 'SOURCE-APPROVAL.json', approval)
order = read(R / 'ORDER.json')
compiled_path = R / 'decisions/review_02250_03250_03000_03250.json'
compiled = read(compiled_path)['decisions']
packet = R / 'packets/03000-250.json'
prepared = []
for row in selected:
    ordinal = row['ordinal']; cid = row['candidate_id']; loc = row['original_compiled_locator']
    old = compiled[loc['item'] - 1]
    assert old['candidate_id'] == cid and c.digest(old) == loc['row_sha256']
    assert hashlib.sha256(compiled_path.read_bytes()).hexdigest() == loc['file_raw_sha256']
    assert order[ordinal] == cid
    selection_path = D / f'ORIGINAL-SELECTION-{ordinal:05d}.json'
    selection = {'schema': prep.SELECTION, 'actor': '/root', 'original_source_sha256': c.digest(original),
                 'records': {cid: {'locator': {'file': str(compiled_path.relative_to(ROOT)), 'file_sha256': loc['file_raw_sha256'],
                                             'item': loc['item'], 'row_sha256': loc['row_sha256']},
                                   'packet': ref(packet), 'reason': 'Exact root-read original compiled row; old approval is historical only.'}},
                 'reason': 'One explicit original row and packet for fresh direct149V6 root review.'}
    save(selection_path, selection)
    plan = {'schema': prep.PLAN, 'actor': '/root', 'original_snapshot': ref(R / 'SOURCE.json.gz'),
            'current_proposal': ref(D / 'CURRENT-PROPOSAL.json.gz'), 'order': ref(R / 'ORDER.json'),
            'catalog_approval': ref(R / 'NATIVE-CATALOG-APPROVAL-149-V6.json'), 'source_approval': ref(D / 'SOURCE-APPROVAL.json'),
            'original_selection': ref(selection_path), 'required_revisions': {},
            'assignment': {'task_name': '/root', 'model': 'session_model_unspecified', 'reasoning_effort': 'session_effort_unspecified',
                           'start': ordinal, 'end': ordinal + 1, 'ids': [cid]},
            'reason': reasons[ordinal] + ' Root performs new direct review; preparation creates no read attestation or proof.'}
    plan_path = D / f'PLAN-{ordinal:05d}.json'
    save(plan_path, plan)
    out, receipt = prep.write_inputs(ref(plan_path), f'root-{ordinal:05d}-149-01', actor='/root', root=ROOT, here=R)
    prepared.append(str(out.relative_to(ROOT)))
report = {'schema': 'photo-root-two-source-preparation-verification/v1', 'actor': '/root',
          'current_proposal': ref(D / 'CURRENT-PROPOSAL.json.gz'), 'source_approval': ref(D / 'SOURCE-APPROVAL.json'),
          'changes_from_parent': [row['candidate_id'] for row in selected], 'total_authored_source_changes': len(approval['changes']),
          'catalog_equal_parent149': current['slot_catalog'] == read(parent / 'CURRENT-PROPOSAL.json.gz')['slot_catalog'],
          'bindings_equal_original': current['slot_bindings'] == original['slot_bindings'],
          'policies_equal_original': current['policies'] == original['policies'], 'prepared': prepared,
          'native_proofs_created': 0, 'operating_changes': 0, 'Gemini_calls': 0}
assert report['catalog_equal_parent149'] and report['bindings_equal_original'] and report['policies_equal_original']
save(D / 'ROOT-PREPARATION-VERIFICATION.json', report)
print(json.dumps({'prepared': prepared, 'source_corrections': 2, 'source_change_total': len(approval['changes']),
                  'current_source_sha256': c.digest(current), 'native_proofs_created': 0}))
