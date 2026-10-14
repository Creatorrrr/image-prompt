"""Serialize three individually authored source clarifications for new inputs.

No proof, role, mode, status or signature is created. The explicit replacements
below were selected by root after reading the complete sources and local facts.
"""
from __future__ import annotations
import copy
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


current = json.loads(gzip.decompress((HERE / 'native-inputs/root-00000-00020-plan-01/CURRENT-PROPOSAL.json.gz').read_bytes()))
original = json.loads(gzip.decompress((HERE / 'SOURCE.json.gz').read_bytes()))
assert digest(current) == 'f1a7b55527c677e3401a19aec37e57e36a0f07584c0464536bce8b9f141897be'
manual = [
    (1250, 'cand_253b99c26a365bf890f33cc533876ad0', {
        'ko': '차가움이 잠깐 풀리는 걸 들킨 표정',
        'application_contract': 'Apply only to the independently declared existing face bound to primary_face. Portray a fleeting expression of softening caught in the moment; no new observer or prior event is introduced.'},
     'The complete English original expressly states for a moment and caught. Clarify the Korean duration and application caught-expression cue from those existing positive clauses. Keep the cold-softening visible nuance and the restriction against a new observer/prior event. Do not attribute an uncited English qualifier to the old Korean/application quote.'),
    (1289, 'cand_e4785146de225d7991b84f405461a561', {
        'en': 'inside a campus café', 'ko': '캠퍼스 카페 내부',
        'application_contract': 'Select the interior of a campus café as the location for the independently declared scene bound to scene. Do not infer a specific institution, student identity or an off-campus neighborhood.'},
     'Both original phrase_en and phrase_ko expressly select the cafe interior. Align the shorter English/Korean labels and application with that existing whole-source inside meaning. No new room, institution, student or off-campus location is asserted. Each future fact must cite its own complete positive interior quote.'),
    (11128, 'cand_17f21e3dd66a5d1aa97b3b38efaab469', {
        'ko': '성인이 펜슬 스커트 차림으로 자연스럽게 서 있거나 걷는 전체 자세.'},
     'The common English, concept, relation and both actual Korean branch bodies already explicitly say natural. Add the omitted Korean adverb to the common translation. The future standing/walking common-Korean pose quote must itself include 자연스럽게; the old shortened quote cannot borrow that qualifier from another pointer or branch.')]
records = []
for ordinal, cid, replacements, reason in manual:
    before = copy.deepcopy(current['candidates'][cid])
    after = copy.deepcopy(before)
    delta = []
    for field, value in replacements.items():
        old = before['content'][field]
        assert old != value
        after['content'][field] = value
        delta.append({'pointer': '/content/' + field, 'before_exists': True,
                      'before': old, 'after_exists': True, 'after': value, 'reason': reason})
    bindings = {bid: value for bid, value in current['slot_bindings'].items() if value['candidate_id'] == cid}
    assert {key: value for key, value in before.items() if key != 'content'} == {key: value for key, value in after.items() if key != 'content'}
    records.append({'ordinal': ordinal, 'candidate_id': cid,
        'original_source': original['candidates'][cid], 'source_before': before,
        'source_after': after, 'source_before_sha256': digest(before),
        'source_after_sha256': digest(after), 'exact_delta': delta,
        'own_bindings_whole_unchanged': bindings, 'reason': reason,
        'selected_for_new_input_only': True, 'native_proof_or_status_approval': False})
out = {'schema': 'photo-root-quote-local-source-clarifications/v1', 'actor': '/root',
    'current_source_sha256': digest(current),
    'catalog_sha256': digest(current['slot_catalog']), 'records': records,
    'root_read_boundary': 'Complete original/current source and current proofs were read before these exact field decisions. The complete reconstructed after retains every other field exactly; local changed clauses were reread individually. This is source-input selection, not fresh full native approval.',
    'proof_quote_only_correction_without_source_change': {'ordinal': 1251,
        'fact_id': 'extentKo', 'new_quote': '얼굴을 꽉 채우는 뷰티 클로즈업',
        'reason': 'The existing complete Korean field already supports the face-filling tight crop. Source change is unnecessary; a new individually reviewed proof must use the full supporting quote.'},
    'operating_changes': 0, 'native_proofs_or_signatures': 0,
    'gemini_calls': 0, 'provider_network_or_embedding_calls': 0}
target = HERE / 'authored/root_quote_local_source_clarifications_v1.json'
with target.open('x') as stream:
    json.dump(out, stream, ensure_ascii=False, sort_keys=True, indent=2)
    stream.write('\n')
print(json.dumps({'file': str(target.relative_to(ROOT)), 'source_input_clarifications': len(records), 'sha256': digest(out), 'native_approvals': 0}))
