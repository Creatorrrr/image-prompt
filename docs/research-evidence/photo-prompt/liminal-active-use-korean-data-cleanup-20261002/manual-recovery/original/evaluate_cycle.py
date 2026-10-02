#!/usr/bin/env python3
"""Frozen two-state, 14-query Korean active-use evaluator. Default: zero-call plan only.

--execute requires the exact source proposal, sends only frozen missing inputs
under a durable no-retry log, then writes the proposal index and 56 result rows.
--replay is zero-call/read-only, reproducing all saved rows and physical index.
There is no automatic acceptance or post-measurement tuning.
"""
import argparse
import datetime as dt
import fcntl
import json
import math
import os
from pathlib import Path
import urllib.error
import urllib.request
from cycle_common import (
    A, E, R, W, TARGET, STATES, g, git, guard_window, load_baseline_index,
    load_freeze, load_reused_cache, objsha, raw_proposal, read_json, require,
    sha, states_from_freeze, validate_vector, write_json,
)
import build_semantic_index as builder
from bm25f_retrieval import rank_bm25f


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def cosine(left, right):
    return sum(a*b for a,b in zip(left,right)) / math.sqrt(sum(a*a for a in left) * sum(b*b for b in right))


def safe_transport_diagnostics(error):
    reason = getattr(error, 'reason', None)
    number = getattr(reason, 'errno', None)
    return {'error_class': type(error).__name__,
            'reason_type': type(reason).__name__ if reason is not None else None,
            'reason_errno': number if isinstance(number, int) and not isinstance(number, bool) else None}


def validate_attempts(frozen, attempts, new_cache):
    allowed = {item['sha256']:item for item in frozen['approved_inputs'] if item['sha256'] in frozen['pending_input_sha256']}
    require(len(attempts) <= frozen['maximum_paid_attempts'], 'Saved attempt count exceeds cap')
    require([a['number'] for a in attempts] == list(range(1,len(attempts)+1)), 'Attempt numbering mismatch')
    require(len({a['sha256'] for a in attempts}) == len(attempts), 'Duplicate attempt prohibited')
    for attempt in attempts:
        require(attempt['status'] in {'attempt_started','failed_http_no_retry','failed_or_uncertain_no_retry','completed'}, 'Unknown attempt status')
        require(not any(k.startswith('manual_') for k in attempt), 'New cycle forbids inherited manual retry metadata')
        require(attempt['sha256'] in allowed, 'Attempted an unfrozen or reused input')
        work = allowed[attempt['sha256']]
        require((attempt['kind'],attempt['key']) == (work['kind'],work['key']), 'Attempt identity mismatch')
        require(attempt['input_utf8_bytes'] == len(work['text'].encode()), 'Attempt input size mismatch')
        require(attempt['per_attempt_upper_usd'] == frozen['per_attempt_upper_usd'], 'Attempt cost mismatch')
    require(set(new_cache) <= set(allowed), 'New cache includes an unapproved input')
    for h,record in new_cache.items():
        validate_vector(record, allowed[h]['text'])
        require(h == sha(record['text'].encode()), 'New cache exact text mismatch')
        completed = [a for a in attempts if a['sha256'] == h and a['status'] == 'completed']
        require(len(completed) == 1 and completed[0]['vector_sha256'] == objsha(record['vector']), 'Fresh cache lacks one exact completed attempt; no retry')
    for attempt in attempts:
        if attempt['status'] == 'completed':
            require(attempt['sha256'] in new_cache, 'Completed attempt has no durable cache; do not retry')


def verify_execution_identity(frozen):
    require(git('rev-parse','HEAD').decode().strip() == frozen['baseline_commit'], 'HEAD changed before request')
    require((R / frozen['source_file']).read_bytes() == raw_proposal(frozen), 'Exact proposal source required before request')
    require(g.dictionary_hash(g.load_json(A / 'photo_prompt_tags.json')) == frozen['state_dictionary_hashes']['proposal'], 'Complete current dictionary changed before request')
    revision = frozen['maintenance_revision']
    require((R / revision['new_record_file']).read_bytes() == (E / revision['new_record_snapshot']).read_bytes(), 'Exact versioned maintenance record required before request')
    require(read_json(E / 'frozen-inventory-queries.json') == frozen, 'Loaded freeze changed before request')
    require(sha((E / 'frozen-inventory-queries.json').read_bytes()) == (E / 'frozen-sha256.txt').read_text().split()[0], 'Freeze changed before request')


def transient_project_credential():
    """Use only the existing ignored project .env; never populate environment."""
    path = R / '.env'
    require(path.is_file(), 'Existing project credential file absent; no request sent')
    require(git('check-ignore','--','.env').decode().strip() == '.env', 'Credential file must be ignored')
    found = {}
    for raw_line in path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        name,value = line.split('=',1)
        name = name.strip()
        if name in ('GEMINI_API_KEY','GOOGLE_API_KEY'):
            require(name not in found, 'Duplicate credential configuration; no request sent')
            found[name] = value.strip().strip('"').strip("'")
    key = found.get('GEMINI_API_KEY') or found.get('GOOGLE_API_KEY')
    require(bool(key), 'API configuration absent; no request sent')
    return key


def call_one_input(frozen, work, cache, attempts, extra_stop):
    """One approved missing input, durable pre-send log, no retry or redirect."""
    h = sha(work['text'].encode())
    require(work in frozen['approved_inputs'] and h == work['sha256'], 'Unapproved API input')
    require(h in frozen['pending_input_sha256'] and h not in cache, 'Only exact frozen missing inputs may be sent')
    require(not any(a['sha256'] == h for a in attempts), 'Prior attempt cannot be retried')
    require(all(a['status'] == 'completed' for a in attempts), 'Failed or uncertain attempt blocks further calls')
    require(len(attempts) < frozen['maximum_paid_attempts'], 'Attempt cap reached')
    require(len(work['text'].encode()) <= frozen['token_limit_per_input'], 'Conservative byte/token cap exceeded')
    budget = guard_window(frozen, extra_stop, charged_attempts=len(attempts), prospective_attempts=1)
    verify_execution_identity(frozen)
    # Credential loading occurs only after execute and exact-input guards.
    key = transient_project_credential()
    # Recheck STOP/deadline/ledger immediately before the durable attempt.
    budget = guard_window(frozen, extra_stop, charged_attempts=len(attempts), prospective_attempts=1)
    record = {'number':len(attempts)+1,'kind':work['kind'],'key':work['key'],'sha256':h,'input_utf8_bytes':len(work['text'].encode()),'status':'attempt_started','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'per_attempt_upper_usd':frozen['per_attempt_upper_usd'],'budget_guard':budget}
    attempts.append(record)
    write_json(E / 'api-attempts.json',attempts)
    request = urllib.request.Request(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent',
        data=json.dumps({'model':'models/gemini-embedding-2','content':{'parts':[{'text':work['text']}]},'outputDimensionality':768}).encode(),
        headers={'Content-Type':'application/json','x-goog-api-key':key},method='POST',
    )
    try:
        # urllib's single open has no application retry; any redirect fails closed.
        with urllib.request.build_opener(NoRedirect).open(request,timeout=45) as response:
            response_data = json.load(response)
        vector = response_data['embedding']['values']
        validate_vector({'model':g.SEMANTIC_MODEL_ID,'dimensions':768,'text':work['text'],'vector':vector},work['text'])
        vector = g.round_embedding_vector(vector,768)
        result = {'text':work['text'],'vector':vector,'model':g.SEMANTIC_MODEL_ID,'dimensions':768}
        validate_vector(result,work['text'])
    except urllib.error.HTTPError as error:
        record.update(status='failed_http_no_retry',**safe_transport_diagnostics(error))
        write_json(E / 'api-attempts.json',attempts)
        raise SystemExit('Embedding HTTP failure recorded; details suppressed; no retry')
    except Exception as error:
        record.update(status='failed_or_uncertain_no_retry',**safe_transport_diagnostics(error))
        write_json(E / 'api-attempts.json',attempts)
        raise SystemExit('Embedding failure recorded; details suppressed; no retry')
    new_path = E / 'new-vector-cache.json'
    new_cache = read_json(new_path) if new_path.exists() else {}
    new_cache[h] = result
    write_json(new_path,new_cache)
    record.update(status='completed',vector_sha256=objsha(vector),completed_utc=dt.datetime.now(dt.timezone.utc).isoformat())
    write_json(E / 'api-attempts.json',attempts)
    cache[h] = result
    print('Completed exact frozen ' + work['kind'] + ' input ' + work['key'] + '; no retry',flush=True)


def make_index(data, old, cache):
    bm = g.build_semantic_bm25f_payload(data)
    entries, changed = {}, []
    for key,kind,row,slot in g.iter_semantic_entries(data):
        text = g.semantic_text_for_entry(row,slot,kind=kind)
        if old['entries'][key]['text'] == text:
            vector = old['entries'][key]['vector']
        else:
            h = sha(text.encode())
            validate_vector(cache[h],text)
            vector = cache[h]['vector']
            changed.append(key)
        entries[key] = {'kind':kind,'slot':slot,'id':row['id'],'text':text,'vector':vector,'bm25f_document':bm['documents'][key]}
    index = {'provider':g.SEMANTIC_PROVIDER,'dictionary_hash':g.dictionary_hash(data),'semantic_text_recipe':g.SEMANTIC_TEXT_RECIPE_VERSION,'embedding_model':g.SEMANTIC_MODEL_ID,'embedding_dimensions':768,'bm25f':{key:value for key,value in bm.items() if key != 'documents'},'entries':entries}
    g.validate_semantic_index_metadata(index,data)
    require(g.semantic_bm25f_payload_from_index(index) == bm,'Complete BM25F derivation mismatch')
    require(set(entries) == set(old['entries']),'Full index coverage changed')
    require(set(changed) <= {TARGET},'Unexpected changed document')
    unchanged = [key for key in entries if key not in changed]
    require(all(entries[key]['vector'] == old['entries'][key]['vector'] for key in unchanged),'Unchanged document vector changed')
    return index, {'dictionary_hash':index['dictionary_hash'],'document_count':len(entries),'changed_documents':changed,'reused_document_vectors':len(unchanged),'changed_document_vectors':len(changed),'bm25f_sha256':objsha(bm),'complete_entries_sha256':objsha(entries),'entry_order_sha256':objsha(list(entries)),'all_document_texts_match_current_recipe':True,'all_vectors_finite_nonzero_768_dimensions':True,'full_bm25f_regenerated_and_equal':True}


def evaluate(frozen, states, indexes, cache):
    rows = []
    for label in STATES:
        index,data = indexes[label],states[label]
        bm = g.semantic_bm25f_payload_from_index(index)
        for q in frozen['queries']:
            allowed = ['slot:' + q['slot'] + ':' + row['id'] for row in data['slots'][q['slot']]]
            require(q['target'] in allowed and TARGET in allowed,'Query target is not an existing action')
            vector = cache[q['query_sha256']]['vector']
            dense = [{'id':key,'score':round(cosine(vector,index['entries'][key]['vector']),12)} for key in allowed]
            dense.sort(key=lambda value:(-value['score'],value['id']))
            lexical = rank_bm25f(bm,{'query':q['query']},allowed_ids=allowed,limit=len(allowed))
            for method,ranked,id_key in [('dense',dense,'id'),('lexical',lexical,'document_id')]:
                def exposure(target):
                    for rank,result in enumerate(ranked,1):
                        if result[id_key] == target:
                            return {'id':target,'rank':rank,'score':result['score'],'in_top5':rank <= 5,'in_top12':rank <= 12,'absent':False}
                    return {'id':target,'rank':None,'score':None,'in_top5':False,'in_top12':False,'absent':True}
                rows.append({'state':label,'method':method,'query_id':q['id'],'query':q['query'],'query_sha256':q['query_sha256'],'kind':q['kind'],'slot':q['slot'],'corpus_size':len(allowed),'returned_hits':len(ranked),'no_hits':not ranked,'primary_target':exposure(q['target']),'secondary_corrected_candidate':exposure(TARGET),'top12':ranked[:12],'full_ranking':ranked})
    require(len(rows) == len(STATES) * len(frozen['queries']) * 2 == 56,'Incomplete result matrix')
    require(len({(r['state'],r['method'],r['query_id']) for r in rows}) == 56,'Duplicate result rows')
    return rows


def exposure_report(rows):
    lookup = {(r['state'],r['method'],r['query_id']):r for r in rows}
    comparisons = []
    for before in (r for r in rows if r['state'] == 'baseline'):
        after = lookup[('proposal',before['method'],before['query_id'])]
        id_key = 'id' if before['method'] == 'dense' else 'document_id'
        mapped = {label:{hit[id_key]:{'rank':i,'score':hit['score']} for i,hit in enumerate(row['full_ranking'],1)} for label,row in [('baseline',before),('proposal',after)]}
        empty = {'rank':None,'score':None}
        changed = [{'id':key,'baseline':mapped['baseline'].get(key,empty),'proposal':mapped['proposal'].get(key,empty)} for key in sorted(set(mapped['baseline']) | set(mapped['proposal'])) if mapped['baseline'].get(key,empty) != mapped['proposal'].get(key,empty)]
        top = {label:[hit[id_key] for hit in row['top12']] for label,row in [('baseline',before),('proposal',after)]}
        comparisons.append({'method':before['method'],'query_id':before['query_id'],'kind':before['kind'],'query':before['query'],'primary_target':{'baseline':before['primary_target'],'proposal':after['primary_target']},'secondary_corrected_candidate':{'baseline':before['secondary_corrected_candidate'],'proposal':after['secondary_corrected_candidate']},'no_hits':{'baseline':before['no_hits'],'proposal':after['no_hits']},'returned_hits':{'baseline':before['returned_hits'],'proposal':after['returned_hits']},'top12_ids':top,'entered_top12':sorted(set(top['proposal'])-set(top['baseline'])),'left_top12':sorted(set(top['baseline'])-set(top['proposal'])),'all_changed_ranking_entries':changed,'changed_ranking_entry_count':len(changed),'requires_independent_tradeoff_review':True})
    return {'status':'measured_only_not_an_acceptance_decision','comparisons':comparisons,'no_hit_cases':[{'state':r['state'],'method':r['method'],'query_id':r['query_id'],'query':r['query']} for r in rows if r['no_hits']],'acceptance_warning':'Require elimination of the sourced Korean active-use contradiction and retained intended/coexistence behavior, with no unjustified near-miss or unrelated collateral loss. Review every primary/secondary rank, score, absence/no-hit case, full top12 transition and exhaustive ranking delta in both methods. Unchanged final English output cannot offset harmful retrieval. Do not tune source wording or probes after measurement.','limits':'Source-guided inspectable diagnostics, not a blind benchmark. Different ordinary waiting/transit scenes remain legitimate requests, never new exclusions. Optional retrieval is distinct from eligibility, adoption, composed prompt and rendered image. This is Korean active-use consistency repair, not a V6 semantic-loss fix.'}


def run(args):
    frozen = load_freeze()
    states = states_from_freeze(frozen)
    cache = load_reused_cache(frozen)
    old,shard_checks = load_baseline_index(frozen,states['baseline'])
    current = g.load_json(A / 'photo_prompt_tags.json')
    require(current in [states[label] for label in STATES],'Current merged data exceeds frozen scope')
    source = R / frozen['source_file']
    require(source.read_bytes() in [(E / 'baseline-raw-extension.json').read_bytes(),raw_proposal(frozen)],'Current raw source exceeds minimal proposal')
    for q in frozen['queries']:
        require(q['target'] in old['entries'] and old['entries'][q['target']]['slot'] == 'action','Frozen primary target identity/slot mismatch')
    new_cache = read_json(E / 'new-vector-cache.json') if (E / 'new-vector-cache.json').exists() else {}
    attempts = read_json(E / 'api-attempts.json') if (E / 'api-attempts.json').exists() else []
    validate_attempts(frozen,attempts,new_cache)
    cache.update(new_cache)
    pending = [item for item in frozen['approved_inputs'] if item['sha256'] not in cache]
    require(set(item['sha256'] for item in pending) <= set(frozen['pending_input_sha256']),'Pending workload expanded')
    live_budget = guard_window(frozen,args.stop_file,charged_attempts=len(attempts),prospective_attempts=len(pending)) if not args.replay else None
    plan = {'status':'plan_only','model':g.SEMANTIC_MODEL_ID,'dimensions':768,'frozen_sha256':sha((E / 'frozen-inventory-queries.json').read_bytes()),'logical_inputs':len(frozen['approved_inputs']),'frozen_queries':len(frozen['queries']),'reused_exact_input_vectors':len(frozen['reused_cache_provenance']),'reused_query_vectors':sum(q['query_sha256'] in frozen['reused_cache_provenance'] for q in frozen['queries']),'new_proposal_documents':1,'pending_texts':len(pending),'pending_inputs':[{'kind':x['kind'],'key':x['key'],'sha256':x['sha256'],'utf8_bytes':len(x['text'].encode())} for x in pending],'pending_input_utf8_bytes':sum(len(x['text'].encode()) for x in pending),'maximum_calls':frozen['maximum_paid_attempts'],'automatic_retries':0,'nominal_pending_upper_usd':len(pending)*frozen['per_attempt_upper_usd'],'additional_conservative_upper_usd':frozen['maximum_additional_cost_usd'],'previous_tracked_cost_upper_usd':frozen['previous_tracked_cost_upper_usd'],'maximum_cumulative_tracked_upper_usd':frozen['previous_tracked_cost_upper_usd']+frozen['maximum_additional_cost_usd'],'project_budget_usd':frozen['project_budget_usd'],'deadline_utc':frozen['deadline_utc'],'planned_result_rows':56,'states':list(STATES),'price_usd_per_million_tokens':frozen['price_usd_per_million_tokens'],'token_limit_per_input':frozen['token_limit_per_input'],'price_source':'https://ai.google.dev/gemini-api/docs/pricing','token_limit_source':'https://ai.google.dev/gemini-api/docs/embeddings','live_budget_guard':live_budget,'budget_limit_note':'Tracked cleanup attempt upper bounds; unrelated account work is not reconciled with billing.'}
    plan.update(already_attempted_calls=len(attempts),failed_or_uncertain_attempts_charged=sum(a['status'] != 'completed' for a in attempts),maximum_manual_recovery_allowance=1,manual_recovery_authorized=False)
    if not args.execute and not args.replay:
        write_json(E / 'api-workload.json',plan)
        write_json(E / 'plan-validation.json',{'status':'zero_call_plan_validation','baseline_document_count':len(old['entries']),'baseline_shards':shard_checks,'baseline_exact_text_vector_bm25f_validation':True,'reused_cache_records':len(cache),'all_primary_targets_exact_existing_action':True,'source_runtime_index_written':False,'query_retrieval_measurements':0})
        print(json.dumps(plan,indent=2))
        return
    require(current == states['proposal'] and source.read_bytes() == raw_proposal(frozen),'Apply exact source proposal before execute/replay')
    require(all(a['status'] == 'completed' for a in attempts),'Failed or uncertain attempt requires reviewed recovery; no automatic continuation')
    if args.replay:
        require(not pending,'Replay missing vector; API fallback forbidden')
    else:
        require(git('rev-parse','HEAD').decode().strip() == frozen['baseline_commit'],'HEAD changed before execute; review freeze')
        for item in pending:
            call_one_input(frozen,item,cache,attempts,args.stop_file)
    indexes,validation = {}, {}
    for label in STATES:
        indexes[label],validation[label] = make_index(states[label],old,cache)
        count = 0 if label == 'baseline' else 1
        require(validation[label]['changed_document_vectors'] == count,'Wrong changed document count')
        require(validation[label]['reused_document_vectors'] == frozen['baseline_document_count']-count,'Wrong reused vector count')
    rows = evaluate(frozen,states,indexes,cache)
    report = exposure_report(rows)
    if args.execute:
        guard_window(frozen,args.stop_file,charged_attempts=len(attempts))
        builder.write_sharded_payload(A / 'photo_prompt_semantic_index.json',indexes['proposal'],keep_stale_generations=True)
    actual = g.load_semantic_index(A / 'photo_prompt_semantic_index.json',states['proposal'])
    require(actual['entries'] == indexes['proposal']['entries'],'Physical index differs from expected complete entries')
    require(actual['bm25f'] == indexes['proposal']['bm25f'],'Physical BM25F differs')
    validation['physical_index'] = {'manifest_sha256':sha((A / 'photo_prompt_semantic_index.json').read_bytes()),'all_shards_verified_by_production_loader':True,'all_entries_equal':True,'full_bm25f_equal':True}
    validation['baseline_shards'] = [{k:v for k,v in entry.items() if k != 'source'} for entry in shard_checks]
    for name,value in [('ranking-results.json',rows),('collateral-exposure-comparison.json',report),('validation.json',validation)]:
        if args.replay:
            require(read_json(E / name) == value,'Saved replay mismatch: ' + name)
        else:
            write_json(E / name,value)
    if args.execute:
        validate_attempts(frozen,attempts,read_json(E / 'new-vector-cache.json'))
        plan.update(status='measured_pending_independent_acceptance',pending_texts=0,pending_inputs=[],calls_attempted=len(attempts),calls_completed=sum(a['status'] == 'completed' for a in attempts),actual_attempt_upper_usd=len(attempts)*frozen['per_attempt_upper_usd'],cumulative_tracked_upper_usd=frozen['previous_tracked_cost_upper_usd']+len(attempts)*frozen['per_attempt_upper_usd'])
        write_json(E / 'api-workload.json',plan)
    print(('Reproduced' if args.replay else 'Saved') + ' all 56 method/query/state rows and exact complete index; acceptance remains separate')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--execute',action='store_true')
    mode.add_argument('--replay',action='store_true')
    parser.add_argument('--stop-file',type=Path)
    args = parser.parse_args()
    if args.execute:
        with (W / '.data-evaluation.lock').open('a') as shared_lock, (E / '.evaluation.lock').open('a') as local_lock:
            fcntl.flock(shared_lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
            fcntl.flock(local_lock,fcntl.LOCK_EX | fcntl.LOCK_NB)
            run(args)
    else:
        run(args)


if __name__ == '__main__':
    main()
