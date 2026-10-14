"""Restore five positive record kinds and freeze an explicit sparse rereview.

Research preparation only. The strict contiguous preparation helper is unchanged.
No positive fact, tag, proof, read attestation or operating source is authored.
"""
import copy
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode = True
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0, str(R))
import prepare_native_inputs as prep
nr = prep.reviews
sys.path[:0] = [str(G / 'scripts'), str(G / 'precore')]


def read(p):
    raw = p.read_bytes()
    return json.loads(gzip.decompress(raw) if p.suffix == '.gz' else raw)


def save(p, v):
    with p.open('xb') as f:
        f.write(c.canonical_bytes(v) + b'\n')


def ref(p):
    return dict(file=str(p.relative_to(ROOT)), file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(), sha256=c.digest(read(p)))


REASONS = {
    12027: 'Retaining a ranked original feature across actual standard and SD counterparts is a conditional positive preservation requirement. Unfilled feature and counterpart parameters do not make the requirement merely diagnostic. No particular feature, scale, morphology or real-person identity is selected by this kind restoration.',
    12038: 'The whole definition positively specifies a generic nonhuman character with separately controlled approachability and mild unease. The router metadata and absence of a named species do not cancel that subject requirement. No anatomy, species, exact expression, mental state or particular silhouette is introduced.',
    12049: 'Two coordinated body channels supporting one response are a parameterized positive coordination requirement. Missing concrete channels do not justify deleting the requirement. Exact channels, connected carriers, values and mutation versus preservation must still be independently authored; no pose or action is invented here.',
    12051: 'The typed OR among goal, value, object, posture and practical behavior supplies a same-character continuity requirement. An unfilled choice is not absence of positive meaning. Preserve the OR and continuity function; no arbitrary branch, private goal, physical object or behavior is chosen here.',
    12093: 'The source explicitly requires visible backstage separation. It does not prescribe a literal divider, but rejecting a divider cannot erase the positive separation requirement. Retain all face, name, location and private-life exposure limits without introducing a screen, performer, face or identifying information.',
}


def main():
    index_path = R / 'authored/native_diag70_05250_locator-index-v1.json'
    alt_path = R / 'authored/native_diag70_05250_hold5.alternatives-v1.json'
    assert hashlib.sha256(index_path.read_bytes()).hexdigest() == '08ed75a840f7e9d105c65f2e374a2c393e104e31b57a86598effb119f29ab88f'
    assert hashlib.sha256(alt_path.read_bytes()).hexdigest() == '7cb0ffa6fdef40b754361fa5a39f61030edabd452aeda40200c4f4cf00b53558'
    index = read(index_path)
    alternatives = {x['ordinal']: x for x in read(alt_path)['rows']}
    assert set(alternatives) == set(REASONS)
    parent = R / 'native-inputs/root-lower-lashes-source-plan-16-R02'
    current = read(parent / 'CURRENT-PROPOSAL.json.gz')
    assert c.digest(current) == '60bc1ace6319f7970732e50a470da9131ca9ab4c394781de79df03e5025c83ca'
    original = read(R / 'SOURCE.json.gz')
    parent_snapshot = copy.deepcopy(current)
    plan = read(parent / 'PLAN.json')
    order = nr.artifact(ROOT, plan['order'])
    catalog = nr.artifact(ROOT, plan['catalog_approval'])
    nr.verify_catalog(original['slot_catalog'], current['slot_catalog'], catalog['review'], ROOT)
    approval = read(parent / 'SOURCE-APPROVAL.json')
    D = R / 'native-inputs/root-diagnostic-kind-source-plan-18'
    D.mkdir(exist_ok=False)
    selected = []
    for ordinal, reason in REASONS.items():
        row = alternatives[ordinal]
        cid = order[ordinal]
        before = copy.deepcopy(current['candidates'][cid])
        assert row['candidate_id'] == cid and before == row['original_whole'] == row['current66_whole'] == original['candidates'][cid]
        assert before['record_kind'] == 'diagnostic'
        after = copy.deepcopy(before)
        after['record_kind'] = 'visual_option'
        current['candidates'][cid] = after
        selected.append(dict(ordinal=ordinal, candidate_id=cid, before=before, after=after, reason=reason,
                             decision='restore_positive_kind_only_pending_complete_native_contract',
                             positive_semantic_obligations=row['minimal_alternatives'][1]['positive_obligations'],
                             semantic_context=row['origin_whole'],
                             complete_positive_contract_selected=False, native_proof=None))
    memo = dict(schema='photo-root-diagnostic-kind-restoration/v1', actor='/root', parent_source=ref(parent / 'CURRENT-PROPOSAL.json.gz'),
                original_source=ref(R / 'SOURCE.json.gz'), catalog=ref(R / 'CATALOG-FINAL-149-V6.json'),
                independent_worker_review=ref(index_path), alternatives=ref(alt_path), selected=selected,
                root_read_scope='All70 complete original/current record bodies, plus all5 complete exact origin/5B/family/compatibility/neighbor-example contexts were directly read. Root does not claim a new reading of all70 historical5B/parent profiles; that fuller reading is separately attributed to the worker.',
                reason='Restore positive requirements incorrectly treated as diagnostic because parameters were unfilled. Preserve whole definitions, IDs, conditions, effects, provenance and all other fields. This only corrects record kinds in a research snapshot; complete positive contracts and facts remain pending.',
                unselected_alternative='A_check_only_interpretation would narrow the positive source to a check and is not selected.',
                diagnostic65_decision='Fresh individual native semantic review required; neither current kind nor empty effects is sufficient approval.',
                native_approvals=0, native_proofs_created=0, operating_changes=0, Gemini_calls=0)
    save(D / 'ROOT-SOURCE-SELECTION.json', memo)
    for row in selected:
        approval['changes'].append(dict(candidate_id=row['candidate_id'], before=row['before'], after=row['after'],
            delta=[dict(pointer='/record_kind', before_exists=True, before='diagnostic', after_exists=True, after='visual_option', reason=row['reason'])],
            reason=row['reason'], provenance=[ref(alt_path), ref(index_path), ref(D / 'ROOT-SOURCE-SELECTION.json')]))
    approval['current_source_sha256'] = c.digest(current)
    approval['reason'] += ' Root restores five positive record kinds without selecting positive contracts or native facts.'
    prep.approve_source(ROOT, original, current, approval)
    c.validate(current)
    assert len(approval['changes']) == 71
    changed = {cid for cid in current['candidates'] if current['candidates'][cid] != parent_snapshot['candidates'][cid]}
    assert changed == {x['candidate_id'] for x in selected}
    for cid in changed:
        a = copy.deepcopy(current['candidates'][cid]); b = copy.deepcopy(parent_snapshot['candidates'][cid])
        a.pop('record_kind'); b.pop('record_kind'); assert a == b
    assert all(current[k] == parent_snapshot[k] for k in ('slot_catalog', 'slot_bindings', 'policies'))
    with (D / 'CURRENT-PROPOSAL.json.gz').open('xb') as f:
        f.write(gzip.compress(c.canonical_bytes(current), mtime=0))
    save(D / 'SOURCE-APPROVAL.json', approval)
    rows = index['rows']; ids = [r['candidate_id'] for r in rows]; ordinals = [r['ordinal'] for r in rows]
    assert len(ids) == len(set(ids)) == 70 and [order[o] for o in ordinals] == ids
    assert {cid for cid, r in original['candidates'].items() if r['record_kind'] == 'diagnostic'} == set(ids)
    cache = {}; historical = {}; required = {}
    for row in rows:
        cid = row['candidate_id']; loc = row['original_compiled_locator']
        packet_ref = {k:row['original_packet'][k] for k in ('file', 'file_sha256', 'sha256')}
        historical[cid] = nr.compiled_review(ROOT, R, loc, original, cid, packet_ref, c.digest(original), c.digest(original['slot_catalog']), cache)
        assert not n.referenced_records(current['candidates'][cid], current)
        assert not {bid:b for bid,b in current['slot_bindings'].items() if b['candidate_id'] == cid}
        required[cid] = dict(prior_review=dict(artifact=ref(ROOT / loc['file']), pointer='/decisions/' + str(loc['item']-1), sha256=loc['row_sha256']),
                             memo_artifacts=[ref(index_path), ref(D / 'ROOT-SOURCE-SELECTION.json')],
                             reason='Fresh sparse review of whole source, exact5B, actual origin/parent purpose and149 full role boundaries. Five restored positive kinds remain pending until complete contracts; other65 are not approved from kind alone.')
    nr_fields = dict(schema=nr.INPUT, actor='/root', ids=ids, original_snapshot=ref(R / 'SOURCE.json.gz'), current_snapshot=ref(D / 'CURRENT-PROPOSAL.json.gz'), order=plan['order'],
        catalog_review=catalog['review'], original_decisions={r['candidate_id']:r['original_compiled_locator'] for r in rows},
        original_packets={r['candidate_id']:{k:r['original_packet'][k] for k in ('file','file_sha256','sha256')} for r in rows}, required_revisions=required)
    out = R / 'native-inputs/prepared/review05250-diagnostic70-149-01'; out.mkdir(exist_ok=False)
    save(out / 'INPUT.json', nr_fields)
    assignment = dict(schema=nr.ASSIGNMENT, actor='/root', task_name='/root/review_05250_06250', model='gpt-6.1-sol', reasoning_effort='high', ids=ids, ordinals=ordinals, input=ref(out / 'INPUT.json'))
    nr.validate_assignment_identity(assignment); prep.required_revisions(ROOT, required, ids)
    save(out / 'ASSIGNMENT.json', assignment)
    packet = dict(schema=prep.PACKET, preparation_plan=ref(D / 'ROOT-SOURCE-SELECTION.json'), assignment_sha256=c.digest(assignment), input_sha256=c.digest(nr_fields), prepared_count=70, actual_read_count=0,
                  ids=ids, ordinals=ordinals, original_records={cid:original['candidates'][cid] for cid in ids}, current_records={cid:current['candidates'][cid] for cid in ids},
                  references={cid:{} for cid in ids}, reference_bindings={cid:{} for cid in ids}, historical_compiled_rows=historical,
                  historical_statuses={cid:r['status'] for cid,r in historical.items()}, original_compiled_artifacts={cid:loc['file']+'#item='+str(loc['item']) for cid,loc in nr_fields['original_decisions'].items()})
    save(out / 'PREPARED-PACKET.json', packet)
    receipt = dict(schema='photo-root-explicit-sparse-native-preparation/v1', source=ref(D / 'CURRENT-PROPOSAL.json.gz'), source_approval=ref(D / 'SOURCE-APPROVAL.json'),
                   source_changes_total=71, original_diagnostic_count=70, research_current_kind_counts=dict(Counter(x['record_kind'] for x in current['candidates'].values())),
                   assignment=ref(out / 'ASSIGNMENT.json'), input=ref(out / 'INPUT.json'), packet=ref(out / 'PREPARED-PACKET.json'),
                   sparse_ordinals_explicit=True, contiguous_helper_modified=False, locator_checks=70, required_closure_empty_checks=70, own_bindings_empty_checks=70,
                   prepared_count=70, actual_read_count=0, native_proofs_created=0, operating_changes=0, Gemini_calls=0)
    save(out / 'PREPARATION.json', receipt)
    save(D / 'ROOT-PREPARATION-VERIFICATION.json', receipt)
    print(json.dumps(dict(source_sha256=c.digest(current), prepared=str(out.relative_to(ROOT)), kind_counts=receipt['research_current_kind_counts'], source_changes_total=71, native_approvals=0)))


if __name__ == '__main__':
    main()
