"""Reopen unaccepted noise rewrite; retain its actual canonical source property."""
import copy
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path.cwd(); R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode = True; sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as native
sys.path.insert(0, str(R)); import prepare_native_inputs as prep
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
assert Path(prep.reviews.native.__file__).resolve().is_relative_to(G)

def read(path): return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())
def save(path, value):
    with path.open('xb') as stream: stream.write(c.canonical_bytes(value) + b'\n')
def ref(path): return {'file': str(path.relative_to(ROOT)), 'file_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'sha256': c.digest(read(path))}

parent = R / 'native-inputs/root-mood-noise-source-plan-11'
current = read(parent / 'CURRENT-PROPOSAL.json.gz'); original = read(R / 'SOURCE.json.gz')
assert c.digest(current) == '987964e32ed8459c2edeb0a439f7779374accddf39b109193995d977388db637'
cid = 'cand_f1251d5df8735a3d83381e34a2d70b34'; after = copy.deepcopy(current['candidates'][cid])
after['effects'] = copy.deepcopy(original['candidates'][cid]['effects'])
assert after['effects']['properties'] == [{'dimension': 'style', 'property': 'rendering.noise', 'target': 'image_plane'}]
reason = 'Preserve the original actual style/rendering.noise effect and image_plane source address. Bind that source address explicitly to the actual existing image; source addresses are not requester owner IDs. Root previous unaccepted image.noise rewrite fails the independently tested original rendering.noise lock. Use a freshly manually certified same-canonical-fact grain_profile view without adding or renaming any effect. The literal ISO qualifier and independent image presence obligation remain.'
D = R / 'native-inputs/root-noise-canonical-source-plan-12'; D.mkdir(exist_ok=False)
old_batch = R / 'native_batches/root-03169-149-01/BATCH.json'
memo = {'schema': 'photo-root-native-semantic-reopen/v1', 'actor': '/root', 'candidate_id': cid,
        'prior_batch': ref(old_batch), 'decision': 'hold_prior_unaccepted_noise_source_and_proof_use_new_fresh_input',
        'observed_failure': 'check_mood_noise_root_04.py: full original_actual_noise_property_lock_denied observedTrue expectedFalse',
        'completed_checks_before_failure': 29, 'test_script_raw_sha256': hashlib.sha256((R / 'check_mood_noise_root_04.py').read_bytes()).hexdigest(),
        'reason': reason, 'whole_before_source': current['candidates'][cid], 'whole_proposed_after_source': after,
        'requirements': ['Fresh full source/proof/spec/ordinary quotes/actual owner maps and source P review.',
                         'Use original rendering.noise and image_plane as canonical facts/effect set; no image.noise shadow effect or permission alias invented.',
                         'Manual grain_profile view must retain exact canonical E mode/value/operation/P closure/target/receivers and independently bound complete source authority.',
                         'Test original exact rendering.noise and parent rendering locks, actual alias/ancestor/disjoint scope and full/compact own-binding gates.',
                         'Prior44 PASS is bounded and does not waive this added failed semantic regression. No automatic re-sign or status rewrite.'],
        'operating_changes': 0, 'Gemini_calls': 0}
save(D / 'ROOT-SEMANTIC-REOPEN.json', memo)
current['candidates'][cid] = after
approval = read(parent / 'SOURCE-APPROVAL.json'); selected = next(row for row in approval['changes'] if row['candidate_id'] == cid)
selected['after'] = after; selected['reason'] = reason
selected['delta'] = [{'pointer': '/' + key, 'before_exists': True, 'before': selected['before'][key], 'after_exists': True, 'after': after[key], 'reason': reason}
                     for key in selected['before'] if selected['before'][key] != after[key]]
selected['provenance'].append(ref(D / 'ROOT-SEMANTIC-REOPEN.json'))
approval['current_source_sha256'] = c.digest(current)
approval['reason'] += ' Reopen the unaccepted noise rewrite; retain original canonical property/target/effect. Research native same-fact view must be freshly authored, not re-signed.'
prep.approve_source(ROOT, original, current, approval); c.validate(current)
with (D / 'CURRENT-PROPOSAL.json.gz').open('xb') as stream: stream.write(gzip.compress(c.canonical_bytes(current), mtime=0))
save(D / 'SOURCE-APPROVAL.json', approval)
plan = read(parent / 'PLAN-03169.json'); plan['current_proposal'] = ref(D / 'CURRENT-PROPOSAL.json.gz'); plan['source_approval'] = ref(D / 'SOURCE-APPROVAL.json')
old_row = read(old_batch)['records'][0]
plan['required_revisions'] = {cid: {'prior_review': {'artifact': ref(old_batch), 'pointer': '/records/0', 'sha256': c.digest(old_row)},
                                   'memo_artifacts': [ref(D / 'ROOT-SEMANTIC-REOPEN.json')], 'reason': reason}}
plan['reason'] = reason; save(D / 'PLAN-03169.json', plan)
out, receipt = prep.write_inputs(ref(D / 'PLAN-03169.json'), 'root-03169-149-02', actor='/root', root=ROOT, here=R)
save(D / 'ROOT-PREPARATION-VERIFICATION.json', {'current_proposal': ref(D / 'CURRENT-PROPOSAL.json.gz'), 'source_approval': ref(D / 'SOURCE-APPROVAL.json'),
     'only_changed_from_parent': cid, 'total_original_source_changes': len(approval['changes']), 'prepared': str(out.relative_to(ROOT)),
     'original_noise_effects_exactly_restored': after['effects'] == original['candidates'][cid]['effects'],
     'native_proofs_created': 0, 'operating_changes': 0, 'Gemini_calls': 0})
print(json.dumps({'prepared': str(out), 'source_sha256': c.digest(current), 'original_canonical_effects_preserved': True, 'native_proofs_created': 0}))
