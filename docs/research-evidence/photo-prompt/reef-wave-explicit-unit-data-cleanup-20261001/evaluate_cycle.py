#!/usr/bin/env python3
"""Frozen three-state, 30-query DATA evaluator.

Default is a zero-call, zero-runtime-write plan. --execute requires the approved
source edit, allows only the one missing exact document input, and writes the
proposal index and 180 evidence rows. --replay makes no API or file writes and
checks the complete saved results plus current physical index. No auto-accept.
"""
import argparse
import copy
import datetime as dt
import fcntl
import json
import math
import os
import urllib.error
import urllib.request
from cycle_common import (
    A, E, R, REEF, STATES, g, git, guard_window, load_baseline_index,
    load_freeze, load_reused_cache, objsha, raw_proposal, read_json, require,
    sha, states_from_freeze, validate_vector, write_json,
)
import build_semantic_index as builder
from bm25f_retrieval import rank_bm25f


def cosine(left, right):
    return sum(a*b for a, b in zip(left, right)) / math.sqrt(sum(a*a for a in left) * sum(b*b for b in right))


def call_one_document(frozen, work, cache, attempts, extra_stop):
    """One request, durable pre-send attempt record, no retries or secret output."""
    h = sha(work['text'].encode())
    require(h == frozen['fresh_document']['sha256'], 'Unapproved API input')
    require(work['kind'] == 'document' and work['key'] == REEF, 'Only the exact reef document is authorized for this runner')
    require(not any(a['sha256'] == h for a in attempts), 'Prior attempt requires explicit review; this runner cannot retry it')
    require(all(a['status'] == 'completed' for a in attempts), 'Prior failed or uncertain attempt requires review; refuse new call')
    require(len(attempts) < frozen['maximum_paid_attempts'], 'Attempt cap reached')
    require(len(work['text'].encode()) <= frozen['token_limit_per_input'], 'Input exceeds conservative byte/token cap')
    budget = guard_window(frozen, extra_stop, prospective_attempts=len(attempts) + 1)
    env_path = R / '.env'
    if env_path.exists():
        require(git('check-ignore', '--', '.env').decode().strip() == '.env', 'Project credential file must be ignored')
    # Deliberately deferred until --execute, after all frozen-input guards.
    builder.load_project_env()
    key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    require(bool(key), 'API configuration absent; no request sent')
    record = {
        'number': len(attempts) + 1, 'kind': work['kind'], 'key': work['key'],
        'sha256': h, 'input_utf8_bytes': len(work['text'].encode()),
        'status': 'attempt_started', 'utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'per_attempt_upper_usd': frozen['per_attempt_upper_usd'], 'budget_guard': budget,
    }
    attempts.append(record)
    write_json(E / 'api-attempts.json', attempts)  # fsync before sending anything
    request = urllib.request.Request(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent',
        data=json.dumps({'model': 'models/gemini-embedding-2', 'content': {'parts': [{'text': work['text']}]}, 'outputDimensionality': 768}).encode(),
        headers={'Content-Type': 'application/json', 'x-goog-api-key': key}, method='POST',
    )
    try:
        # Default urllib has no retry loop. Redirects are rejected so credentials
        # and text cannot be forwarded to an unapproved endpoint.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        with urllib.request.build_opener(NoRedirect).open(request, timeout=45) as response:
            response_data = json.load(response)
        original_vector = response_data['embedding']['values']
        validate_vector({'model': g.SEMANTIC_MODEL_ID, 'dimensions': 768, 'text': work['text'], 'vector': original_vector}, work['text'])
        vector = g.round_embedding_vector(original_vector, 768)
        result = {'text': work['text'], 'vector': vector, 'model': g.SEMANTIC_MODEL_ID, 'dimensions': 768}
        validate_vector(result, work['text'])
    except urllib.error.HTTPError as error:
        record.update(status='failed_http_no_retry', http_status=error.code)
        write_json(E / 'api-attempts.json', attempts)
        raise SystemExit('Embedding HTTP failure recorded; response suppressed; no retry')
    except Exception as error:
        record.update(status='failed_or_uncertain_no_retry', error_class=type(error).__name__)
        write_json(E / 'api-attempts.json', attempts)
        raise SystemExit('Embedding failure recorded; details suppressed; no retry')
    # A crash after this cache write but before completion stays uncertain and
    # cannot trigger another paid call without an explicit reviewed recovery.
    new_cache = read_json(E / 'new-vector-cache.json') if (E / 'new-vector-cache.json').exists() else {}
    new_cache[h] = result
    write_json(E / 'new-vector-cache.json', new_cache)
    record.update(status='completed', vector_sha256=objsha(vector), completed_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    write_json(E / 'api-attempts.json', attempts)
    cache[h] = result
    print('Completed one exact reef document embedding; no retry', flush=True)


def make_index(data, old, cache):
    bm = g.build_semantic_bm25f_payload(data)
    entries = {}
    changed = []
    for key, kind, row, slot in g.iter_semantic_entries(data):
        text = g.semantic_text_for_entry(row, slot, kind=kind)
        if old['entries'][key]['text'] == text:
            vector = old['entries'][key]['vector']
        else:
            h = sha(text.encode())
            validate_vector(cache[h], text)
            vector = cache[h]['vector']
            changed.append(key)
        entries[key] = {'kind': kind, 'slot': slot, 'id': row['id'], 'text': text, 'vector': vector, 'bm25f_document': bm['documents'][key]}
    index = {
        'provider': g.SEMANTIC_PROVIDER, 'dictionary_hash': g.dictionary_hash(data),
        'semantic_text_recipe': g.SEMANTIC_TEXT_RECIPE_VERSION,
        'embedding_model': g.SEMANTIC_MODEL_ID, 'embedding_dimensions': 768,
        'bm25f': {key: value for key, value in bm.items() if key != 'documents'}, 'entries': entries,
    }
    g.validate_semantic_index_metadata(index, data)
    require(g.semantic_bm25f_payload_from_index(index) == bm, 'State BM25F differs from complete derivation')
    require(set(entries) == set(old['entries']), 'State full-index coverage changed')
    require(set(changed) <= {REEF}, 'Unexpected document changed')
    unchanged = [key for key in entries if key not in changed]
    require(all(entries[key]['vector'] == old['entries'][key]['vector'] for key in unchanged), 'An unchanged document vector changed')
    return index, {
        'dictionary_hash': index['dictionary_hash'], 'document_count': len(entries),
        'changed_documents': changed, 'reused_document_vectors': len(unchanged),
        'changed_document_vectors': len(changed), 'bm25f_sha256': objsha(bm),
        'complete_entries_sha256': objsha(entries), 'entry_order_sha256': objsha(list(entries)),
        'all_document_texts_match_current_recipe': True,
        'all_vectors_finite_nonzero_768_dimensions': True,
        'full_bm25f_regenerated_and_equal': True,
    }


def evaluate(frozen, states, indexes, cache):
    rows = []
    for label in STATES:
        index, data = indexes[label], states[label]
        bm = g.semantic_bm25f_payload_from_index(index)
        for q in frozen['queries']:
            allowed = ['slot:' + q['slot'] + ':' + row['id'] for row in data['slots'][q['slot']]]
            vector = cache[q['query_sha256']]['vector']
            dense = [{'id': key, 'score': round(cosine(vector, index['entries'][key]['vector']), 12)} for key in allowed]
            dense.sort(key=lambda value: (-value['score'], value['id']))
            lexical = rank_bm25f(bm, {'query': q['query']}, allowed_ids=allowed, limit=len(allowed))
            for method, ranked, id_key in [('dense', dense, 'id'), ('lexical', lexical, 'document_id')]:
                def exposure(target):
                    for rank, result in enumerate(ranked, 1):
                        if result[id_key] == target:
                            return {'id': target, 'rank': rank, 'score': result['score'], 'in_top5': rank <= 5, 'in_top12': rank <= 12}
                    return {'id': target, 'rank': None, 'score': None, 'in_top5': False, 'in_top12': False}
                rows.append({
                    'state': label, 'method': method, 'query_id': q['id'], 'query': q['query'],
                    'query_sha256': q['query_sha256'], 'kind': q['kind'], 'slot': q['slot'],
                    'source_file': q['source_file'], 'source_sha256': q['source_sha256'],
                    'corpus_size': len(allowed), 'returned_hits': len(ranked),
                    'primary_target': exposure(q['target']), 'secondary_reef': exposure(REEF),
                    'top12': ranked[:12],
                })
    require(len(rows) == len(STATES) * len(frozen['queries']) * 2 == 180, 'Incomplete result matrix')
    require(len({(r['state'], r['method'], r['query_id']) for r in rows}) == 180, 'Duplicate result rows')
    return rows


def exposure_report(rows):
    lookup = {(r['state'], r['method'], r['query_id']): r for r in rows}
    comparisons = []
    for before in (r for r in rows if r['state'] == 'baseline'):
        key = before['method'], before['query_id']
        results = {label: lookup[(label, *key)] for label in STATES}
        comparisons.append({
            'method': key[0], 'query_id': key[1], 'kind': before['kind'],
            'primary_target': {label: row['primary_target'] for label, row in results.items()},
            'secondary_reef': {label: row['secondary_reef'] for label, row in results.items()},
            'top12_ids': {label: [hit['id' if key[0] == 'dense' else 'document_id'] for hit in row['top12']] for label, row in results.items()},
            'requires_independent_tradeoff_review': True,
        })
    return {
        'status': 'measured_only_not_an_acceptance_decision',
        'comparisons': comparisons,
        'acceptance_warning': 'Review every primary/secondary rank, score and top12 transition against the concrete full corrected-process unit benefit. Primary rank1 is not sufficient. Preserve old aquarium/intertidal/dune/cafe harms and all newly measured collateral exposure; do not hide unchanged-rank score increases.',
        'limits': '30 reused inspectable diagnostics, not a blind benchmark. Full-unit controlled serialization is distinct from natural retrieval, eligibility, adoption, final composed prompt and rendered images. Direction queries do not establish relation reasoning; ebb queries have no low-rank requirement.',
    }


def run(args):
    frozen = load_freeze()
    states = states_from_freeze(frozen)
    cache = load_reused_cache(frozen)
    old, shard_checks = load_baseline_index(frozen, states['baseline'])
    current = g.load_json(A / 'photo_prompt_tags.json')
    require(current in [states['baseline'], states['fresh_explicit_unit']], 'Current merged data exceeds the frozen source proposal')
    source = R / frozen['source_file']
    require(source.read_bytes() in [(E / 'baseline-raw-extension.json').read_bytes(), raw_proposal(frozen)], 'Current raw source exceeds minimal frozen edit')
    new_path = E / 'new-vector-cache.json'
    if new_path.exists():
        new_cache = read_json(new_path)
        require(set(new_cache) <= {frozen['fresh_document']['sha256']}, 'Unexpected new-cache input')
        for h, record in new_cache.items():
            validate_vector(record, frozen['fresh_document']['text'])
            require(h == sha(record['text'].encode()), 'New-cache exact text mismatch')
        cache.update(new_cache)
    attempts = read_json(E / 'api-attempts.json') if (E / 'api-attempts.json').exists() else []
    require(len(attempts) <= frozen['maximum_paid_attempts'], 'Saved attempts exceed cap')
    require(all(a['sha256'] == frozen['fresh_document']['sha256'] for a in attempts), 'Unexpected attempted input')
    require([a['number'] for a in attempts] == list(range(1, len(attempts) + 1)), 'Attempt numbering mismatch')
    if new_path.exists():
        for h, record in read_json(new_path).items():
            completed = [a for a in attempts if a['sha256'] == h and a['status'] == 'completed']
            require(len(completed) == 1 and completed[0]['vector_sha256'] == objsha(record['vector']), 'Fresh cache lacks one matching completed attempt; review recovery before proceeding')
    fresh = {'kind': 'document', 'key': REEF, 'text': frozen['fresh_document']['text']}
    work = [fresh] + [{'kind': 'query', 'key': q['id'], 'text': q['query']} for q in frozen['queries']]
    pending = [item for item in work if sha(item['text'].encode()) not in cache]
    require(all(item == fresh for item in pending), 'A reused query cache is missing; paid fallback forbidden')
    require(len(work) == 31 and len(pending) <= 1, 'Logical or paid workload expanded')
    plan = {
        'status': 'plan_only', 'model': g.SEMANTIC_MODEL_ID, 'dimensions': 768,
        'frozen_sha256': sha((E / 'frozen-inventory-queries.json').read_bytes()),
        'logical_new_proposal_texts': len(work), 'frozen_queries': len(frozen['queries']),
        'reused_query_vectors': len(frozen['queries']), 'new_proposal_documents': 1,
        'cached_old_comparator_documents': 1, 'pending_texts': len(pending),
        'pending_input_utf8_bytes': sum(len(item['text'].encode()) for item in pending),
        'maximum_calls': frozen['maximum_paid_attempts'], 'automatic_retries': 0,
        'nominal_upper_usd': len(pending) * frozen['per_attempt_upper_usd'],
        'additional_conservative_upper_usd': frozen['maximum_additional_cost_usd'],
        'previous_tracked_cost_upper_usd': frozen['previous_tracked_cost_upper_usd'],
        'project_budget_usd': frozen['project_budget_usd'], 'deadline_utc': frozen['deadline_utc'],
        'planned_result_rows': 180, 'states': list(STATES),
        'price_usd_per_million_tokens': 0.20, 'token_limit_per_input': frozen['token_limit_per_input'],
        'price_source': 'https://ai.google.dev/gemini-api/docs/pricing',
        'token_limit_source': 'https://ai.google.dev/gemini-api/docs/embeddings',
        'budget_limit_note': 'Tracked cleanup attempt upper bounds; unrelated account work is not reconciled with billing.',
    }
    if not args.execute and not args.replay:
        validation = {'status': 'zero_call_plan_validation', 'baseline_document_count': len(old['entries']), 'baseline_shards': shard_checks, 'baseline_exact_text_vector_bm25f_validation': True, 'reused_cache_records': len(cache), 'cached_comparator_and_all_30_queries_verified': True, 'new_proposal_document_sha256': frozen['fresh_document']['sha256'], 'pending_fresh_document': bool(pending), 'source_runtime_written': False}
        write_json(E / 'api-workload.json', plan)
        write_json(E / 'plan-validation.json', validation)
        print(json.dumps(plan, indent=2))
        return
    require(current == states['fresh_explicit_unit'] and source.read_bytes() == raw_proposal(frozen), 'Apply approved fresh source before execute/replay')
    require(all(a['status'] == 'completed' for a in attempts), 'Prior uncertain/failed attempt must be reviewed before execute/replay')
    if args.replay:
        require(not pending, 'Replay has no exact fresh vector; no API fallback')
    elif pending:
        call_one_document(frozen, fresh, cache, attempts, args.stop_file)
    indexes, validation = {}, {}
    for label in STATES:
        indexes[label], validation[label] = make_index(states[label], old, cache)
    expected_changes = {'baseline': 0, 'old_corrected_labels': 1, 'fresh_explicit_unit': 1}
    for label, count in expected_changes.items():
        require(validation[label]['changed_document_vectors'] == count, 'Wrong state changed-document count')
        require(validation[label]['reused_document_vectors'] == frozen['baseline_document_count'] - count, 'Wrong reused count')
    rows = evaluate(frozen, states, indexes, cache)
    report = exposure_report(rows)
    if args.execute:
        guard_window(frozen, args.stop_file)
        builder.write_sharded_payload(A / 'photo_prompt_semantic_index.json', indexes['fresh_explicit_unit'], keep_stale_generations=True)
    actual = g.load_semantic_index(A / 'photo_prompt_semantic_index.json', states['fresh_explicit_unit'])
    require(actual['entries'] == indexes['fresh_explicit_unit']['entries'], 'Current physical index differs from complete expected index')
    require(actual['bm25f'] == indexes['fresh_explicit_unit']['bm25f'], 'Current physical BM25F differs')
    validation['physical_index'] = {'manifest_sha256': sha((A / 'photo_prompt_semantic_index.json').read_bytes()), 'all_shards_verified_by_production_loader': True, 'all_entries_equal': True, 'full_bm25f_equal': True}
    validation['baseline_shards'] = [{k: v for k, v in entry.items() if k != 'source'} for entry in shard_checks]
    for name, value in [('ranking-results.json', rows), ('collateral-exposure-comparison.json', report), ('validation.json', validation)]:
        if args.replay:
            require(read_json(E / name) == value, 'Saved replay mismatch: ' + name)
        else:
            write_json(E / name, value)
    if args.execute:
        plan.update(status='measured_pending_independent_acceptance', pending_texts=0, calls_attempted=len(attempts), calls_completed=sum(a['status'] == 'completed' for a in attempts), actual_attempt_upper_usd=len(attempts)*frozen['per_attempt_upper_usd'], cumulative_tracked_upper_usd=frozen['previous_tracked_cost_upper_usd']+len(attempts)*frozen['per_attempt_upper_usd'])
        write_json(E / 'api-workload.json', plan)
    print(('Reproduced' if args.replay else 'Saved') + ' 180 query/method/state rows and exact complete index/BM25F validation; acceptance remains separate')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--execute', action='store_true')
    mode.add_argument('--replay', action='store_true')
    parser.add_argument('--stop-file', type=__import__('pathlib').Path)
    args = parser.parse_args()
    if args.execute:
        with (E / '.evaluation.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            run(args)
    else:
        run(args)


if __name__ == '__main__':
    main()
