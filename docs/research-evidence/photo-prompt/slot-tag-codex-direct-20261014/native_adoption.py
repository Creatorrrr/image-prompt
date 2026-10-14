"""Preview explicitly approved native adoption; never classify or activate.

All semantic content, facts, carriers, modes, effects, catalog edits and binding
conditions must be supplied by reviewed inputs. Only identity bookkeeping and
integrity checks are computed. Production CLI requires all 18,250 approvals.
"""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import re

import direct_review as review
import review_state
import photo_semantic_evidence as native

SCHEMA = 'photo-codex-native-adoption-manual/v1'
PRODUCTION_COUNT = 18250
BINDING_SPEC_FIELDS = frozenset({'role', 'semantic_role', 'conditions', 'weight'})


def exact(left, right):
    return review.c.canonical_bytes(left) == review.c.canonical_bytes(right)


def binding_id(cid, tag):
    return 'bind_' + review.c.digest({'candidate_id': cid, 'slot_id': tag})[:32]


def decision_digest(rows):
    return review.c.digest({row['candidate_id']: row for row in rows})


def references(value, path=''):
    """Exact candidate/binding reference leaves; no replacement policy is inferred."""
    found = {}
    if isinstance(value, str) and (review.c.ID.fullmatch(value) or review.c.BINDING_ID.fullmatch(value)):
        found[path] = value
    elif isinstance(value, dict):
        for key, child in value.items():
            escaped = str(key).replace('~', '~0').replace('/', '~1')
            found.update(references(child, path + '/' + escaped))
    elif isinstance(value, list):
        for n, child in enumerate(value):
            found.update(references(child, path + '/' + str(n)))
    return found


def require_fields(value, fields, label):
    if not isinstance(value, dict) or set(value) != set(fields):
        raise ValueError(label + ': exact fields required')


def reason(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('explicit manual review rationale required')


def validate_authored_inputs(data, rows):
    """Read-only counterpart of the ledger guards, without writing PROGRESS."""
    packets = {}
    for path in sorted((review.HERE / 'packets').glob('*.json')):
        packet = review.c.decode(path.read_bytes()); sha = review.c.digest(packet)
        if sha in packets:
            raise ValueError('duplicate full source packet')
        packets[sha] = packet
    cache, binding_cache, authored = {}, {}, {}
    source_sha, catalog_sha = review.c.digest(data), review.c.digest(data['slot_catalog'])
    for row in rows:
        review.validate_decision(row, data, provenance_cache=cache, binding_cache=binding_cache)
        location = row['authored_decision']
        path = review.run_path(location['file'], 'authored')
        if path not in authored:
            authored[path] = review.c.decode(path.read_bytes())
        item = review.authored_item(authored[path], location['item'])
        if location['sha256'] != review.c.digest(item) or any(not exact(row[k], v) for k, v in item.items()):
            raise ValueError('compiled approval differs from immutable authored decision')
        packet = packets.get(row['packet_sha256']); cid = row['candidate_id']
        if packet is None:
            raise ValueError('approval full source packet is missing or changed')
        if (cid not in packet['ids'] or not exact(packet['records'][cid], data['candidates'][cid])
                or not exact(packet['references'][cid], review.closure(data, cid))
                or packet['source_sha256'] != source_sha
                or packet['catalog_sha256'] != catalog_sha):
            raise ValueError('approval lacks exact full source packet binding')


def _manual_source_updates(proposed, source, by_id, updates):
    seen = set()
    for update in updates:
        require_fields(update, {'candidate_id', 'decision_sha256', 'before', 'after', 'reason'}, 'source update')
        cid = update['candidate_id']; reason(update['reason'])
        if cid in seen or cid not in by_id or update['decision_sha256'] != review.c.digest(by_id[cid]):
            raise ValueError('source update needs unique source-bound approval')
        seen.add(cid)
        current, after = proposed['candidates'][cid], update['after']
        if not exact(current, update['before']):
            raise ValueError('source update differs from exact before record')
        require_fields(after, current, 'native after record')
        if (after['id'] != cid or after['record_kind'] != by_id[cid]['recommended_kind']
                or not isinstance(after['provenance'], list)
                or after['provenance'][:len(source['candidates'][cid]['provenance'])] != source['candidates'][cid]['provenance']):
            raise ValueError('source identity/kind/original provenance must be preserved')
        if references(after) != references(current):
            raise ValueError('reference changes require separate exact reviewed reference updates')
        # Qualification is a separate explicit input, never an implicit source edit.
        if after['content'].get('role_evidence') != current['content'].get('role_evidence'):
            raise ValueError('source update cannot replace the separate manual native proof')
        proposed['candidates'][cid] = copy.deepcopy(after)


def _reference_updates(proposed, source, by_id, updates):
    seen = set()
    for update in updates:
        require_fields(update, {'candidate_id', 'source_record_sha256', 'decision_sha256',
            'pointer', 'before', 'after', 'reason'}, 'reference update')
        cid, path = update['candidate_id'], update['pointer']; reason(update['reason'])
        if (cid not in by_id or update['source_record_sha256'] != review.c.digest(source['candidates'][cid])
                or update['decision_sha256'] != review.c.digest(by_id[cid])
                or not isinstance(path, str) or not path.startswith('/content/')
                or (cid, path) in seen):
            raise ValueError('reference update requires unique exact source/decision binding')
        seen.add((cid, path))
        current = proposed['candidates'][cid]
        leaves = references(current)
        if (path not in leaves or leaves[path] != update['before']
                or not isinstance(update['after'], str)
                or not (review.c.ID.fullmatch(update['after']) or review.c.BINDING_ID.fullmatch(update['after']))
                or bool(review.c.ID.fullmatch(update['before'])) != bool(review.c.ID.fullmatch(update['after']))):
            raise ValueError('reference update must preserve an existing typed reference leaf')
        keys = [k.replace('~1', '/').replace('~0', '~') for k in path[1:].split('/')]
        parent = current
        for key in keys[:-1]:
            parent = parent[int(key)] if isinstance(parent, list) else parent[key]
        key = keys[-1]
        parent[int(key) if isinstance(parent, list) else key] = update['after']


def build_preview(source, baseline, order, rows, manual, *, actor, expected_count):
    """Pure operation. expected_count is explicit for small isolated fixtures.

    The production CLI always supplies PRODUCTION_COUNT and exposes no override.
    """
    if actor != '/root':
        raise ValueError('native adoption preview is root-only')
    if native.SCHEMA != 'photo-candidate-role-evidence/v3':
        raise ValueError('strict native v3 implementation required; no version fallback')
    if expected_count == PRODUCTION_COUNT:
        raise ValueError('full source production preview requires latest-native v2; historical v1 disabled')
    review.assert_source_snapshot(source, source, baseline, order)
    state = review_state.coverage(order, rows)
    if (type(expected_count) is not int or expected_count < 1
            or baseline['candidate_count'] != expected_count or len(source['candidates']) != expected_count
            or not state['source_review_approval_complete'] or state['pending_source_judgements']
            or state['unreviewed_source_records'] or set(state['all']) != set(source['candidates'])):
        raise ValueError('exact full source approval/count/ID closure required before native preview')
    validate_authored_inputs(source, rows)
    require_fields(manual, {'schema', 'actor', 'source_sha256', 'catalog_sha256', 'decisions_sha256',
        'records', 'catalog_updates', 'source_updates', 'reference_updates', 'binding_approvals'}, 'manual qualification')
    if (manual['schema'] != SCHEMA or manual['actor'] != '/root'
            or manual['source_sha256'] != review.c.digest(source)
            or manual['catalog_sha256'] != review.c.digest(source['slot_catalog'])
            or manual['decisions_sha256'] != decision_digest(rows)
            or not isinstance(manual['records'], dict)
            or set(manual['records']) != set(source['candidates'])
            or any(not isinstance(manual[k], list) for k in
                ('catalog_updates', 'source_updates', 'reference_updates', 'binding_approvals'))):
        raise ValueError('complete explicit manual qualification document/source/catalog/decision binding required')
    by_id = state['all']; proposed = copy.deepcopy(source)
    catalog_seen = set()
    for update in manual['catalog_updates']:
        require_fields(update, {'slot_id', 'before', 'after', 'reason'}, 'catalog update')
        tag = update['slot_id']; reason(update['reason'])
        if tag not in source['slot_catalog'] or tag in catalog_seen:
            raise ValueError('catalog add/remove/rename is unsupported without a new complete reviewed catalog')
        catalog_seen.add(tag)
        if (not exact(update['before'], proposed['slot_catalog'][tag])
                or not isinstance(update['after'], dict) or update['after'].get('id') != tag):
            raise ValueError('catalog update must preserve identity and exact before spec')
        proposed['slot_catalog'][tag] = copy.deepcopy(update['after'])
    for cid, row in by_id.items():
        proposed['candidates'][cid] = review.corrected_record(source['candidates'][cid], row['corrections'])
        proposed['candidates'][cid]['record_kind'] = row['recommended_kind']
    _manual_source_updates(proposed, source, by_id, manual['source_updates'])
    _reference_updates(proposed, source, by_id, manual['reference_updates'])
    final_catalog_sha = review.c.digest(proposed['slot_catalog'])
    old_pairs = {(b['candidate_id'], b['slot_id']): b for b in source['slot_bindings'].values()}
    if len(old_pairs) != len(source['slot_bindings']):
        raise ValueError('duplicate source candidate-slot binding/vote')
    bindings = {}
    for cid, row in sorted(by_id.items()):
        qualification = manual['records'][cid]
        require_fields(qualification, {'source_record_sha256', 'decision_sha256', 'meaning_sha256',
            'catalog_sha256', 'proof', 'bindings'}, 'per-CID manual qualification')
        record = proposed['candidates'][cid]; proof = qualification['proof']
        role_map = {role['slot_id']: role for role in row['roles']}
        if (qualification['source_record_sha256'] != review.c.digest(source['candidates'][cid])
                or qualification['decision_sha256'] != review.c.digest(row)
                or qualification['catalog_sha256'] != final_catalog_sha
                or qualification['meaning_sha256'] != native.meaning_sha256(record)
                or not isinstance(proof, dict) or proof.get('schema') != native.SCHEMA
                or proof.get('meaning_sha256') != qualification['meaning_sha256']
                or not isinstance(proof.get('roles'), dict) or set(proof['roles']) != set(role_map)
                or not isinstance(qualification['bindings'], dict) or set(qualification['bindings']) != set(role_map)):
            raise ValueError('exact reviewed role set/manual binding set/native v3 proof/meaning/catalog required')
        before_meaning = native.meaning_sha256(source['candidates'][cid])
        correction = proof.get('review', {}).get('source_correction')
        if before_meaning != qualification['meaning_sha256']:
            if (not isinstance(correction, dict) or correction.get('before_sha256') != before_meaning
                    or correction.get('after_sha256') != qualification['meaning_sha256']):
                raise ValueError('changed native source requires exact original/final meaning correction proof')
        elif correction is not None:
            raise ValueError('unchanged native meaning cannot claim a source correction')
        original_review = proof.get('review', {}).get('original_review', {})
        if (not isinstance(original_review, dict)
                or any(original_review.get(key) != value for key, value in {
                    'candidate_id': cid, 'source_record_sha256': row['source_record_sha256'],
                    'catalog_sha256': row['catalog_sha256'], 'decision_sha256': review.c.digest(row)}.items())
                or not (exact(original_review.get('artifact'), row['authored_decision'])
                        or original_review.get('artifact') == row['authored_decision']['file'])):
            raise ValueError('native proof must retain the exact original compiled approval provenance')
        if record['record_kind'] == 'diagnostic' and (role_map or proof.get('facts')):
            raise ValueError('diagnostic cannot acquire native positive roles/facts')
        if record['record_kind'] != 'diagnostic' and (not role_map or not proof.get('facts')):
            raise ValueError('positive candidate needs explicit owned native facts and roles')
        for tag, role in role_map.items():
            spec = proposed['slot_catalog'][tag]; supported = proof['roles'][tag]
            if (role['semantic_role'] != spec['semantic_role']
                    or supported.get('scope') != role['scope']
                    or set(supported.get('realization_ids', [])) != set(role['realization_ids'])
                    or supported.get('spec_sha256') != review.c.digest(spec)):
                raise ValueError('approved role spec/scope/actual realization set changed')
            binding_spec = qualification['bindings'][tag]
            require_fields(binding_spec, BINDING_SPEC_FIELDS, 'manual binding conditions')
            if binding_spec['semantic_role'] != spec['semantic_role']:
                raise ValueError('manual binding semantic role differs from reviewed spec')
            old = old_pairs.get((cid, tag)); bid = old['id'] if old else binding_id(cid, tag)
            if bid in bindings:
                raise ValueError('binding identity collision or duplicate vote')
            bindings[bid] = {'id': bid, 'candidate_id': cid, 'slot_id': tag, **copy.deepcopy(binding_spec)}
        # Direct facts remain exact source-supported; native carriers/modes/values
        # are supplied explicitly and validated below, never inferred here.
        fact_keys = ('realization_id', 'pointer', 'quote', 'dimension', 'target', 'property')
        native_facts = {tuple(f.get(k) for k in fact_keys) for f in proof.get('facts', [])}
        if any(tuple(f[k] for k in fact_keys) not in native_facts for f in row['facts']):
            raise ValueError('native proof lost an explicitly approved direct-source fact')
        record['content']['role_evidence'] = copy.deepcopy(proof)
    proposed['slot_bindings'] = dict(sorted(bindings.items()))
    changes = []
    for bid in sorted(set(source['slot_bindings']) | set(bindings)):
        before, after = source['slot_bindings'].get(bid), bindings.get(bid)
        if not exact(before, after):
            changes.append({'before': before, 'after': after})
    approvals = manual['binding_approvals']
    if len(approvals) != len(changes):
        raise ValueError('every binding add/remove/condition change needs exact explicit approval')
    normalized = []
    for approval in approvals:
        require_fields(approval, {'before', 'after', 'reason', 'candidate_id', 'decision_sha256'}, 'binding approval')
        reason(approval['reason']); cid = approval['candidate_id']
        if (cid not in by_id or approval['decision_sha256'] != review.c.digest(by_id[cid])
                or any(value is not None and value['candidate_id'] != cid for value in (approval['before'], approval['after']))):
            raise ValueError('binding approval is not bound to the exact candidate decision')
        normalized.append({'before': approval['before'], 'after': approval['after']})
    if sorted(map(review.c.digest, normalized)) != sorted(map(review.c.digest, changes)):
        raise ValueError('binding approval differs from exact before/after relation')
    # No dangling old binding gets a fallback slot, quiet drop or legacy adapter.
    for pointer, target in references(proposed).items():
        if review.c.BINDING_ID.fullmatch(target) and target not in bindings:
            raise ValueError('removed binding remains referenced; explicit reviewed reference update required: ' + pointer)
        if review.c.ID.fullmatch(target) and target not in proposed['candidates']:
            raise ValueError('dangling canonical candidate reference: ' + pointer)
    for cid, record in proposed['candidates'].items():
        if native.native_status(record) != 'qualified':
            raise ValueError('missing native v3 proof for candidate: ' + cid)
        native.validate(record, proposed['slot_catalog'], catalog_sha256=final_catalog_sha, corpus=proposed)
    review.c.validate(proposed)
    if set(proposed['candidates']) != set(source['candidates']):
        raise ValueError('candidate duplication/loss is forbidden')
    ledger = {'schema': 'photo-codex-native-adoption-preview/v1',
        'actor': '/root', 'expected_candidate_count': expected_count,
        'production_count_gate': expected_count == PRODUCTION_COUNT,
        'source_sha256': review.c.digest(source), 'next_corpus_sha256': review.c.digest(proposed),
        'catalog_sha256': final_catalog_sha, 'decisions_sha256': decision_digest(rows),
        'manual_qualification_sha256': review.c.digest(manual), 'binding_changes': changes,
        'catalog_changes': copy.deepcopy(manual['catalog_updates']),
        'reviewed_reference_updates': copy.deepcopy(manual['reference_updates']),
        'manual_binding_approvals': copy.deepcopy(manual['binding_approvals']),
        'candidate_changes': [{'candidate_id': cid, 'before_sha256': review.c.digest(source['candidates'][cid]),
            'after_sha256': review.c.digest(record), 'before': source['candidates'][cid], 'after': record}
            for cid, record in sorted(proposed['candidates'].items()) if not exact(record, source['candidates'][cid])],
        'native_changes_applied': False, 'runtime_activated': False, 'index_rebuilt': False,
        'stage06_complete': False, 'semantic_accuracy_certified': False,
        'root_all_worker_sources_read_claimed': False}
    return proposed, ledger


def write_preview(name, source, baseline, order, rows, manual, proposed, ledger):
    if ledger.get('production_count_gate') is not False:
        raise ValueError('historical v1 production writer disabled; use freshly verified latest-native v2')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}', name):
        raise ValueError('explicit new preview name required')
    if (ledger.get('actor') != '/root' or ledger.get('native_changes_applied') is not False
            or ledger.get('source_sha256') != review.c.digest(source)
            or ledger.get('next_corpus_sha256') != review.c.digest(proposed)
            or ledger.get('manual_qualification_sha256') != review.c.digest(manual)
            or ledger.get('decisions_sha256') != decision_digest(rows)):
        raise ValueError('preview output inputs differ from validated change ledger')
    output = (review.HERE / 'native-previews' / name).resolve()
    if not output.is_relative_to(review.HERE.resolve() / 'native-previews') or output.exists():
        raise ValueError('preview output must be new and inside the review run')
    output.mkdir(parents=True, exist_ok=False)
    documents = {'BEFORE-CORPUS.json': source, 'NEXT-CORPUS.json': proposed, 'CHANGE-LEDGER.json': ledger,
        'INPUT-BASELINE.json': baseline, 'INPUT-ORDER.json': order, 'INPUT-DECISIONS.json': rows,
        'INPUT-MANUAL-QUALIFICATION.json': manual}
    for filename, value in documents.items():
        with (output / filename).open('xb') as stream:
            stream.write(review.c.canonical_bytes(value) + b'\n')
    with (output / 'PREVIEW-COMPLETE.json').open('xb') as stream:
        stream.write(review.c.canonical_bytes({'complete': True, 'applied': False,
            'documents': {name: review.c.digest(value) for name, value in documents.items()}}) + b'\n')
    return output


SCHEMA_V2 = 'photo-codex-native-adoption-manual/v2'
MEMBER_CONTRACT = 'candidate-id-presentation-role/v1'
FULL_BINDING_FIELDS = frozenset({'id','candidate_id','slot_id','role','semantic_role','conditions','weight'})


def _exact_approvals(authored, expected, fields, label):
    if not isinstance(authored, list):
        raise ValueError(label + ': explicit complete approval list required')
    normalized = []
    for approval in authored:
        require_fields(approval, set(fields) | {'reason'}, label); reason(approval['reason'])
        normalized.append({key:approval[key] for key in fields})
    if sorted(map(review.c.digest, normalized)) != sorted(map(review.c.digest, expected)):
        raise ValueError(label + ': exact complete before/after approval mismatch')



def validate_preview_conditions(conditions, *, binding=False):
    """Reject policy fields the current consumer would silently ignore."""
    if binding:
        require_fields(conditions,{'subject_applicability'},'binding condition contract')
    else:
        review.c.validate_conditions(conditions,'native preview source')
    policy=conditions.get('subject_applicability',{})
    lists={'subject_categories','deny_subject_categories','allow_domains','deny_domains'}
    booleans={'allow_domains_override_subject_categories','require_domain_match'}
    if not isinstance(policy,dict) or not set(policy)<=lists|booleans:
        raise ValueError('unknown or unconsumed subject applicability schema')
    for key,value in policy.items():
        if key in booleans:
            if type(value) is not bool: raise ValueError('subject applicability flag must be explicit boolean')
        else: review.c.strings(value,'subject_applicability.'+key)

def verify_member_migrations(original,current,rows,authored):
    """Check exact manually classified former member guards; never migrate them."""
    if not isinstance(authored,list): raise ValueError('explicit member guard migration list required')
    required = {(cid,'/content/member_candidates/'+str(index)):(member,original['slot_bindings'].get(member['binding_id']))
        for cid,record in original['candidates'].items()
        for index,member in enumerate(record['content'].get('member_candidates',[])) if 'binding_id' in member}
    seen = set()
    for migration in authored:
        require_fields(migration,{'candidate_id','review_sha256','before_pointer','before_member','before_binding',
            'after_pointer','after_member','classification','condition_targets','reason'},'member guard migration')
        reason(migration['reason']); cid=migration['candidate_id']; key=(cid,migration['before_pointer'])
        if (key not in required or key in seen or migration['review_sha256'] != review.c.digest(rows[cid])
                or not exact(migration['before_member'],required[key][0])
                or required[key][1] is None or not exact(migration['before_binding'],required[key][1])):
            raise ValueError('member migration needs exact original member/full binding and accepted parent review')
        # The authored exact before binding identifies the old edge; this
        # checks an explicit migration, never creates a native CID fallback.
        old_cid=required[key][1]['candidate_id']
        if required[key][0].get('candidate_id',old_cid) != old_cid:
            raise ValueError('ambiguous original member CID/binding must be resolved explicitly first')
        seen.add(key); after=migration['after_member']; pointer=migration['after_pointer']
        if after is None:
            if pointer is not None or any(m.get('candidate_id')==old_cid
                    for m in current['candidates'][cid]['content'].get('member_candidates',[])):
                raise ValueError('removed member migration must match actual removed CID edge')
        else:
            if not isinstance(pointer,str) or not re.fullmatch(r'/content/member_candidates/(0|[1-9][0-9]*)',pointer):
                raise ValueError('explicit actual new member pointer required')
            index=int(pointer.rsplit('/',1)[1]); members=current['candidates'][cid]['content'].get('member_candidates',[])
            if (index>=len(members) or not exact(after,members[index]) or 'binding_id' in after
                    or after.get('candidate_id') != old_cid):
                raise ValueError('member migration cannot retarget identity or preserve old binding membership')
        classification=migration['classification']; targets=migration['condition_targets']
        if classification not in {'transferred_to_source_conditions','already_enforced_intrinsic','reviewed_nonessential'} or not isinstance(targets,list):
            raise ValueError('explicit authored guard classification required; no new unconsumed guard schema')
        if (classification=='reviewed_nonessential' and targets or classification!='reviewed_nonessential' and not targets):
            raise ValueError('guard classification requires explicit condition targets or reviewed nonessential reason')
        target_ids=set()
        for target in targets:
            require_fields(target,{'candidate_id','review_sha256','before','after','reason'},'member condition target'); reason(target['reason'])
            tid=target['candidate_id']
            if (tid not in rows or tid in target_ids or target['review_sha256']!=review.c.digest(rows[tid])
                    or not exact(target['before'],original['candidates'][tid]['conditions'])
                    or not exact(target['after'],current['candidates'][tid]['conditions'])
                    or classification=='transferred_to_source_conditions' and exact(target['before'],target['after'])
                    or classification=='already_enforced_intrinsic' and not exact(target['before'],target['after'])):
                raise ValueError('member condition migration target must bind exact reviewed source conditions')
            target_ids.add(tid)
    if seen!=set(required): raise ValueError('every former member binding guard needs explicit condition migration approval')


def build_preview_v2(latest_manifest_path, manual, *, actor, expected_count=PRODUCTION_COUNT, root=None, here=None):
    """Reverify accepted latest reviews and preview explicitly authored policies.

    Historical approval status/role sets never qualify the current source. No
    binding identity, applicability, empty condition, role or weight is inferred.
    expected_count is exposed only for isolated offline Python fixtures.
    """
    import native_reviews as reviews
    root = Path(root or review.ROOT).resolve(); here = Path(here or review.HERE).resolve()
    if actor != '/root': raise ValueError('native adoption preview is root-only')
    if native.SCHEMA != 'photo-candidate-role-evidence/v3':
        raise ValueError('strict native v3 implementation required; no version fallback')
    latest = reviews.verify_latest(latest_manifest_path, root=root, here=here, expected_count=expected_count)
    manifest = reviews.read_json(reviews.path_in(root,str(latest_manifest_path)))
    if review.c.digest(manifest) != latest['manifest_sha256']:
        raise ValueError('latest manifest changed during verification')
    original = reviews.artifact(root,manifest['original_snapshot'])
    current = reviews.artifact(root,manifest['current_snapshot'])
    require_fields(manual, {'schema','actor','latest_manifest_sha256','original_source_sha256',
        'current_source_sha256','catalog_sha256','member_contract','records','source_approvals',
        'reference_approvals','binding_approvals','policy_approval','member_guard_migrations'}, 'native v2 manual qualification')
    if (manual['schema'] != SCHEMA_V2 or manual['actor'] != '/root'
            or manual['member_contract'] != MEMBER_CONTRACT
            or any(manual[k] != latest[k] for k in ('original_source_sha256','current_source_sha256','catalog_sha256'))
            or manual['latest_manifest_sha256'] != latest['manifest_sha256']
            or not isinstance(manual['records'],dict) or set(manual['records']) != set(latest['records'])):
        raise ValueError('exact full latest current source/catalog/manual v2 contract required')
    if expected_count == PRODUCTION_COUNT and len(current['slot_catalog']) != 141:
        raise ValueError('production preview requires the fully reviewed current141 catalog')
    # Global policy semantics also require a separate exact root review. Their
    # fingerprint was already required to match every contributing native batch.
    policy = manual['policy_approval']
    if exact(original['policies'],current['policies']):
        if policy is not None: raise ValueError('unchanged policies cannot claim a policy change approval')
    else:
        require_fields(policy, {'before','after','reason'}, 'policy approval'); reason(policy['reason'])
        if not exact(policy['before'],original['policies']) or not exact(policy['after'],current['policies']):
            raise ValueError('exact whole policy before/after approval required')
    expected_sources, expected_references = [], []
    for cid,row in latest['records'].items():
        digest = review.c.digest(row); before,after = row['source_before'],row['source_after']
        validate_preview_conditions(after['conditions'])
        for branch in after['effects'].get('realizations',{}).get('branches',[]):
            validate_preview_conditions(branch['conditions'])
        if not exact(before,after):
            expected_sources.append(dict(candidate_id=cid,review_sha256=digest,before=before,after=after,delta=row['delta']))
        oldrefs,newrefs = references(before),references(after)
        for pointer in sorted(set(oldrefs)|set(newrefs)):
            if oldrefs.get(pointer) != newrefs.get(pointer):
                expected_references.append(dict(candidate_id=cid,review_sha256=digest,pointer=pointer,
                    before_exists=pointer in oldrefs,before=oldrefs.get(pointer),
                    after_exists=pointer in newrefs,after=newrefs.get(pointer)))
        # The finalized preview boundary consumes candidate identity and explicit
        # presentation roles. It cannot retain the interim old-binding guard.
        for member in after['content'].get('member_candidates',[]):
            if (not isinstance(member,dict) or 'binding_id' in member
                    or member.get('candidate_id') not in current['candidates']
                    or 'presentation_role' in member and member['presentation_role'] not in current['slot_catalog']):
                raise ValueError('final member contract requires explicit CID, any authored presentation role, and no binding_id')
    verify_member_migrations(original,current,latest['records'],manual['member_guard_migrations'])
    _exact_approvals(manual['source_approvals'],expected_sources,
        {'candidate_id','review_sha256','before','after','delta'},'source approval')
    _exact_approvals(manual['reference_approvals'],expected_references,
        {'candidate_id','review_sha256','pointer','before_exists','before','after_exists','after'},'reference approval')
    proposed = copy.deepcopy(current); bindings = {}
    for cid,row in latest['records'].items():
        qualification = manual['records'][cid]; proof = row['proof']
        require_fields(qualification, {'review_sha256','proof_sha256','bindings'}, 'native v2 candidate qualification')
        if (qualification['review_sha256'] != review.c.digest(row)
                or qualification['proof_sha256'] != review.c.digest(proof)
                or not isinstance(qualification['bindings'],dict)
                or set(qualification['bindings']) != set(proof['roles'])):
            raise ValueError('bindings must match every current native proof role and exact accepted proof')
        for tag,binding in qualification['bindings'].items():
            require_fields(binding,FULL_BINDING_FIELDS,'explicit full native binding')
            if (binding['candidate_id'] != cid or binding['slot_id'] != tag
                    or not isinstance(binding['id'],str) or not review.c.BINDING_ID.fullmatch(binding['id'])
                    or binding['id'] in bindings
                    or binding['semantic_role'] != current['slot_catalog'][tag]['semantic_role']):
                raise ValueError('explicit native binding identity/CID/current role spec mismatch')
            validate_preview_conditions(binding['conditions'],binding=True)
            bindings[binding['id']] = copy.deepcopy(binding)
        proposed['candidates'][cid]['content']['role_evidence'] = copy.deepcopy(proof)
    proposed['slot_bindings'] = dict(sorted(bindings.items()))
    changes = []
    for bid in sorted(set(original['slot_bindings'])|set(current['slot_bindings'])|set(bindings)):
        before,now,after = original['slot_bindings'].get(bid),current['slot_bindings'].get(bid),bindings.get(bid)
        if not exact(before,after) or not exact(now,after):
            # Preserve both original history and the exact current input. A
            # final value equal to history cannot silently undo a current edit.
            cids={value['candidate_id'] for value in (before,now,after) if value is not None}
            if len(cids)!=1 or not cids<=set(latest['records']):
                raise ValueError('binding identity cannot be retargeted to a different candidate')
            cid=next(iter(cids))
            changes.append(dict(candidate_id=cid,review_sha256=review.c.digest(latest['records'][cid]),
                before=before,current_before=now,after=after))
    _exact_approvals(manual['binding_approvals'],changes,
        {'candidate_id','review_sha256','before','current_before','after'},'binding approval')
    # Changing any still-consumed guard invalidates the authored native proof;
    # native.validate rechecks it against these final manually selected bindings.
    for pointer,target in references(proposed).items():
        if review.c.BINDING_ID.fullmatch(target) and target not in bindings:
            raise ValueError('removed binding remains referenced; explicit source/reference delta required: '+pointer)
        if review.c.ID.fullmatch(target) and target not in proposed['candidates']:
            raise ValueError('dangling candidate reference: '+pointer)
    for record in proposed['candidates'].values():
        if native.native_status(record) != 'qualified': raise ValueError('unqualified current native proof')
        native.validate(record,proposed['slot_catalog'],corpus=proposed)
    review.c.validate(proposed)
    ledger = dict(schema='photo-codex-native-adoption-preview/v2',actor='/root',expected_candidate_count=expected_count,
        production_count_gate=expected_count==PRODUCTION_COUNT,latest_manifest_sha256=latest['manifest_sha256'],
        original_source_sha256=review.c.digest(original),current_source_sha256=review.c.digest(current),
        next_corpus_sha256=review.c.digest(proposed),catalog_sha256=latest['catalog_sha256'],
        manual_qualification_sha256=review.c.digest(manual),member_contract=MEMBER_CONTRACT,
        original_compiled={cid:copy.deepcopy(row['original_compiled']) for cid,row in latest['records'].items()},
        accepted_reviews={cid:review.c.digest(row) for cid,row in latest['records'].items()},
        historical_batch_inputs=[dict(assignment_sha256=b['assignment_sha256'],input_sha256=b['input_sha256'],
            current_source_sha256=b['current_source_sha256']) for b in latest['batch_verifications']],
        source_approvals=copy.deepcopy(manual['source_approvals']),reference_approvals=copy.deepcopy(manual['reference_approvals']),
        binding_approvals=copy.deepcopy(manual['binding_approvals']),policy_approval=copy.deepcopy(policy),
        member_guard_migrations=copy.deepcopy(manual['member_guard_migrations']),
        member_guard_consumer_contract='explicit_source_conditions/v1',full_runtime_consumer_integration_verified=False,
        pending_count=0,operational_native_qualified_count=0,native_changes_applied=False,runtime_activated=False,index_rebuilt=False,
        stage06_complete=False,semantic_accuracy_certified=False,root_all_worker_sources_read_claimed=False)
    return proposed,ledger


def write_preview_v2(name, latest_manifest_path, manual, *, actor, expected_count=PRODUCTION_COUNT, root=None, here=None):
    """Reverify immediately, then create a new immutable research preview only."""
    import native_reviews as reviews
    root = Path(root or review.ROOT).resolve(); here = Path(here or review.HERE).resolve()
    if not isinstance(name,str) or not re.fullmatch(r'[a-z0-9][a-z0-9_-]{0,79}',name):
        raise ValueError('explicit new preview name required')
    output = (here/'native-previews'/name).resolve()
    if not output.is_relative_to(here/'native-previews') or output.exists():
        raise ValueError('preview output must be new and inside the review run')
    proposed,ledger = build_preview_v2(latest_manifest_path,manual,actor=actor,expected_count=expected_count,root=root,here=here)
    manifest = reviews.read_json(reviews.path_in(root,str(latest_manifest_path)))
    if review.c.digest(manifest) != ledger['latest_manifest_sha256']: raise ValueError('latest manifest changed before preview write')
    original=reviews.artifact(root,manifest['original_snapshot']); current=reviews.artifact(root,manifest['current_snapshot'])
    documents = {'ORIGINAL-CORPUS.json':original,'BEFORE-NATIVE-CORPUS.json':current,'NEXT-CORPUS.json':proposed,
        'CHANGE-LEDGER.json':ledger,'INPUT-LATEST-MANIFEST.json':manifest,'INPUT-MANUAL-QUALIFICATION.json':manual}
    output.mkdir(parents=True,exist_ok=False)
    for filename,value in documents.items():
        with (output/filename).open('xb') as stream: stream.write(review.c.canonical_bytes(value)+b'\n')
    with (output/'PREVIEW-COMPLETE.json').open('xb') as stream:
        stream.write(review.c.canonical_bytes(dict(complete=True,applied=False,
            documents={filename:review.c.digest(value) for filename,value in documents.items()}))+b'\n')
    return output,ledger


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--actor', required=True, choices=['/root'])
    parser.add_argument('--latest-manifest', required=True)
    parser.add_argument('--manual-qualification', required=True)
    parser.add_argument('--output-name', required=True)
    args = parser.parse_args()
    path = Path(args.manual_qualification).resolve()
    if not path.is_relative_to(review.HERE):
        raise ValueError('manual qualification document must be explicit and in this evidence run')
    manual = review.c.decode(path.read_bytes())
    if manual.get('schema') != SCHEMA_V2:
        raise ValueError('production preview CLI requires explicit latest-native v2; no historical approval fallback')
    output, ledger = write_preview_v2(args.output_name,args.latest_manifest,manual,actor=args.actor)
    print(json.dumps({'preview':str(output),'candidates':ledger['expected_candidate_count'],
                      'applied':False,'stage06_complete':False}))


if __name__ == '__main__': main()
