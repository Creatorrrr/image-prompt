#!/usr/bin/env python3
"""Frozen two-state, 14-query Korean active-use evaluator. Default: zero-call plan only.

--execute requires the exact source proposal, sends only frozen missing inputs
under a durable no-retry log, then writes the proposal index and 56 result rows.
--replay is zero-call/read-only, reproducing all saved rows and physical index.
There is no automatic acceptance or post-measurement tuning.
Separate explicit directly confirmed recovery can retry only the exact document as attempt3,
once, under a transparent15-total-attempt cap overlay. Original plans stay exact.
"""
import argparse
import datetime as dt
import copy
import evaluate_manual_recovery as prior
import fcntl
import json
import math
import os
from pathlib import Path
import urllib.error
import urllib.request
from cycle_common import (
    A, E, R, W, TARGET, STATES, g, git, load_baseline_index,
    load_freeze as load_original_freeze, load_reused_cache, objsha, raw_proposal, read_json, require,
    sha, states_from_freeze, validate_vector, write_json,
)
import build_semantic_index as builder
from bm25f_retrieval import rank_bm25f


ORIGINAL_FREEZE_SHA256 = '603d19882bc0192fc6263800beac14dad69adc666143bf45bc9cf6f561b1b1c1'
RETRY_INPUT_SHA256 = 'de27c0cfb460b3443c00c93917976460262568d6ef391284c83d40cdcbaf7d8a'


def load_freeze():
    """Apply only the directly confirmed recovery/cap overlay to immutable plans."""
    original=prior.load_freeze()
    require(sha((E/'manual-recovery-plan.json').read_bytes())=='5dc6d37a9c1e6041935eb21c28000f09bff475009bd96cfdb6eb63d7d1c73c6b','First recovery plan changed')
    raw=(E/'confirmed-recovery-plan.json').read_bytes()
    require(sha(raw)==(E/'confirmed-recovery-plan-sha256.txt').read_text().split()[0],'Confirmed recovery plan SHA mismatch')
    plan=json.loads(raw)
    require(plan['original_frozen_sha256']==ORIGINAL_FREEZE_SHA256,'Original experimental freeze changed')
    for name,digest in plan['artifact_sha256'].items():
        require(sha((E/name).read_bytes())==digest,'Confirmed recovery artifact changed: '+name)
    recovery=plan['recovery']
    history=read_json(E/'confirmed-recovery/prior-state/api-attempts.json')
    require(history==recovery['historical_attempts'] and len(history)==2,'Historical attempt records changed')
    require(history[0]==original['manual_recovery']['failed_attempt'],'First failure changed')
    require(history[1]['number']==2 and history[1]['status']=='attempt_started','Uncertain second attempt relabeled')
    require(objsha(history)==recovery['historical_attempts_sha256'],'Historical attempts digest changed')
    require(recovery['retry_attempt_number']==3 and recovery['retry_input_sha256']==RETRY_INPUT_SHA256,'Confirmed retry must be exact document attempt3')
    require(recovery['retry_input_kind']=='document' and recovery['retry_input_key']==TARGET,'Confirmed retry target changed')
    require(plan['original_maximum_paid_attempts']==original['maximum_paid_attempts']==14 and plan['original_maximum_additional_cost_usd']==original['maximum_additional_cost_usd']==.0229376,'Original cap history changed')
    require(plan['maximum_paid_attempts']==15 and plan['maximum_additional_cost_usd']==.024576,'Confirmed cap changed')
    require(plan['automatic_retries']==0 and plan['maximum_new_manual_retries']==1,'Confirmed retry allowance changed')
    require(plan['official_endpoint']=='https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent','Confirmed endpoint changed')
    proof=read_json(E/'confirmed-recovery/terminal-session-proof.json')
    require(proof['primary_terminal_evidence']['source']=='execution owner same-session check' and proof['primary_terminal_evidence']['observed_utc']=='2026-10-02T02:01:12Z' and proof['primary_terminal_evidence']['result']=='Unknown process id 42373','Owner terminal-session evidence missing')
    require(proof['global_process_inspection_claimed'] is False,'Terminal evidence must not claim global process inspection')
    require(proof['session_id']==42373 and proof['tool_result']=='write_stdin failed: Unknown process id 42373','Terminal session evidence missing')
    require(proof['elapsed_seconds_at_observation']>proof['transport_timeout_seconds']==45,'Previous request timeout not expired')
    require(proof['attempt2_started_utc']==history[1]['utc'] and proof['uncertain_status_preserved']=='attempt_started','Terminal proof rebound to another attempt')
    require(not any(proof[key]for key in ['live_new_vector_cache_exists','live_ranking_results_exist','live_collateral_results_exist','live_validation_result_exists']),'Prior result existed at recovery preparation')
    return {**original,'manual_recovery':recovery,'maximum_paid_attempts':15,'maximum_additional_cost_usd':.024576,'maximum_cumulative_tracked_upper_usd':1.2959744}


def require_initial_confirmed_retry_state(frozen,attempts):
    require(attempts==frozen['manual_recovery']['historical_attempts'],'Confirmed retry already consumed or history changed')
    started=dt.datetime.fromisoformat(attempts[1]['utc'])
    require((dt.datetime.now(dt.timezone.utc)-started).total_seconds()>45,'Previous transport window has not expired')
    for name in ['new-vector-cache.json','ranking-results.json','collateral-exposure-comparison.json','validation.json']:
        require(not (E/name).exists(),'Existing cache/result prevents confirmed retry: '+name)


def guard_window(frozen,extra_stop=None,charged_attempts=0,prospective_attempts=0):
    """Count immutable failures once; preserve independently increased live spend."""
    require(not (W/'STOP').exists(),'STOP requested')
    if extra_stop is not None:
        require(not extra_stop.exists(),'Additional STOP requested')
    ledger=read_json(W/'ledger.json')
    deadline=min(dt.datetime.fromisoformat(frozen['deadline_utc'].replace('Z','+00:00')),dt.datetime.fromisoformat(ledger['deadline_utc'].replace('Z','+00:00')))
    require(dt.datetime.now(dt.timezone.utc)<deadline,'Deadline reached')
    rate=frozen['per_attempt_upper_usd']
    credited=0
    matches=[c for c in ledger.get('cycles',[]) if c.get('cycle')==16]
    require(len(matches)<=1,'Duplicate current cycle ledger entry')
    if matches:
        cycle=matches[0]
        require(cycle['frozen_sha256']==ORIGINAL_FREEZE_SHA256 and cycle['baseline_commit']==frozen['baseline_commit'],'Live ledger cycle identity changed')
        credited=cycle.get('actual_attempts',0)
        require(isinstance(credited,int) and not isinstance(credited,bool) and 0<=credited<=charged_attempts,'Live ledger attempt credit is inconsistent')
        require(abs(cycle.get('actual_attempt_upper_usd',0)-credited*rate)<1e-12,'Live ledger charged amount is inconsistent')
        require(abs(cycle.get('cumulative_tracked_upper_usd',frozen['previous_tracked_cost_upper_usd'])-(frozen['previous_tracked_cost_upper_usd']+credited*rate))<1e-12,'Live ledger cumulative cycle amount changed')
    live=float(ledger['tracked_project_cost_upper_usd'])
    require(live+1e-12>=frozen['previous_tracked_cost_upper_usd']+credited*rate,'Live ledger total does not contain claimed cycle charge')
    cost=max(frozen['previous_tracked_cost_upper_usd']+charged_attempts*rate,live+(charged_attempts-credited)*rate)
    budget=min(float(ledger['hard_project_budget_usd']),frozen['project_budget_usd'])
    require(charged_attempts+prospective_attempts<=frozen['maximum_paid_attempts'],'Attempt cap would be exceeded')
    require(cost+prospective_attempts*rate<=budget,'Project budget would be exceeded')
    require((charged_attempts+prospective_attempts)*rate<=frozen['maximum_additional_cost_usd']+1e-12,'Cycle cost cap exceeded')
    return {'ledger_tracked_upper_usd':live,'ledger_cycle_attempts_already_credited':credited,'accounted_tracked_upper_usd':cost,'budget_usd':budget,'deadline_utc':deadline.isoformat()}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def cosine(left, right):
    return sum(a*b for a,b in zip(left,right)) / math.sqrt(sum(a*a for a in left) * sum(b*b for b in right))


def recovered_original_failure(frozen,attempts):
    recovery=frozen['manual_recovery']
    if len(attempts)<3 or attempts[:2]!=recovery['historical_attempts']:
        return False
    retry=attempts[2]
    return (retry['number']==3 and retry['sha256']==recovery['retry_input_sha256']
            and retry.get('manual_retry_of_attempt')==2
            and retry.get('manual_recovery_id')==recovery['id']
            and retry.get('manual_retry_of_attempt_sha256')==objsha(recovery['historical_attempts'][1])
            and retry.get('manual_recovery_history_sha256')==recovery['historical_attempts_sha256']
            and retry['status']=='completed')


def may_retry_confirmed_document(frozen,work,attempts,manual_retry):
    recovery=frozen['manual_recovery']
    return bool(manual_retry and attempts==recovery['historical_attempts']
                and work['sha256']==RETRY_INPUT_SHA256
                and work['kind']=='document' and work['key']==TARGET)


def require_continuation(frozen,attempts,permit_initial_manual_retry=False):
    history=frozen['manual_recovery']['historical_attempts']
    require(attempts[:2]==history,'Both historical attempts must remain immutable')
    if permit_initial_manual_retry and attempts==history:
        return
    recovered=recovered_original_failure(frozen,attempts)
    require(recovered and all(a['status']=='completed'for a in attempts[2:]),'Historical or new uncertain/failed attempt blocks continuation; exact manual attempt3 is required')


def safe_transport_diagnostics(error):
    reason = getattr(error, 'reason', None)
    number = getattr(reason, 'errno', None)
    return {'error_class': type(error).__name__,
            'reason_type': type(reason).__name__ if reason is not None else None,
            'reason_errno': number if isinstance(number, int) and not isinstance(number, bool) else None}


def validate_attempts(frozen,attempts,new_cache):
    recovery=frozen['manual_recovery'];history=recovery['historical_attempts']
    allowed={item['sha256']:item for item in frozen['approved_inputs']if item['sha256']in frozen['pending_input_sha256']}
    require(2<=len(attempts)<=15,'Attempt count outside confirmed bounded history/cap')
    require(attempts[:2]==history,'Historical attempt records changed or removed')
    require([a['number']for a in attempts]==list(range(1,len(attempts)+1)),'Attempt numbering mismatch')
    for number,attempt in enumerate(attempts,1):
        require(attempt['status']in {'attempt_started','failed_http_no_retry','failed_or_uncertain_no_retry','completed'},'Unknown attempt status')
        require(attempt['sha256']in allowed,'Attempted unfrozen/reused input')
        work=allowed[attempt['sha256']]
        require((attempt['kind'],attempt['key'])==(work['kind'],work['key']),'Attempt identity mismatch')
        require(attempt['input_utf8_bytes']==len(work['text'].encode()) and attempt['per_attempt_upper_usd']==frozen['per_attempt_upper_usd'],'Attempt input size/cost mismatch')
        if number<=2:
            continue
        markers={k for k in attempt if k.startswith('manual_')}
        if number==3:
            require(attempt['sha256']==RETRY_INPUT_SHA256 and attempt.get('manual_retry_of_attempt')==2,'Only exact document may be manual attempt3')
            require(markers=={'manual_retry_of_attempt','manual_recovery_id','manual_retry_of_attempt_sha256','manual_recovery_history_sha256'},'Attempt3 recovery metadata mismatch')
            require(attempt['manual_recovery_id']==recovery['id'] and attempt['manual_retry_of_attempt_sha256']==objsha(history[1]) and attempt['manual_recovery_history_sha256']==recovery['historical_attempts_sha256'],'Attempt3 history binding mismatch')
        else:
            require(not markers,'Only attempt3 may carry new recovery metadata')
            require(attempt['sha256']!=RETRY_INPUT_SHA256,'No further document retry permitted')
    require(len({a['sha256']for a in attempts[2:]})==len(attempts[2:]),'Duplicate completed/new input prohibited')
    require(set(new_cache)<=set(allowed),'New cache contains unapproved input')
    for h,record in new_cache.items():
        validate_vector(record,allowed[h]['text'])
        require(sha(record['text'].encode())==h,'Cache text hash mismatch')
        completed=[a for a in attempts if a['sha256']==h and a['status']=='completed']
        require(len(completed)==1 and completed[0]['vector_sha256']==objsha(record['vector']),'Cache lacks one exact completed attempt')
    for attempt in attempts:
        if attempt['status']=='completed':require(attempt['sha256']in new_cache,'Completed attempt has no durable cache')


def verify_execution_identity(frozen):
    # The earlier identity checker verifies the exact original proposal, complete
    # dictionary, both maintenance records, original frozen artifacts and HEAD.
    prior.verify_execution_identity(prior.load_freeze())
    require(load_freeze()==frozen,'Confirmed recovery plan or effective cap changed')


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


def call_one_input(frozen, work, cache, attempts, extra_stop, manual_retry=False):
    """One approved missing input, durable pre-send log, no retry or redirect."""
    h = sha(work['text'].encode())
    require(work in frozen['approved_inputs'] and h == work['sha256'], 'Unapproved API input')
    require(h in frozen['pending_input_sha256'] and h not in cache, 'Only exact frozen missing inputs may be sent')
    recovery_applies = may_retry_confirmed_document(frozen,work,attempts,manual_retry)
    require(not any(a['sha256'] == h for a in attempts) or recovery_applies,'Prior attempt cannot be retried without exact one-time manual recovery')
    require_continuation(frozen,attempts,permit_initial_manual_retry=recovery_applies)
    if recovery_applies:
        require_initial_confirmed_retry_state(frozen,attempts)
    require(read_json(E / 'api-attempts.json') == attempts,'Durable attempt ledger changed before request')
    durable_cache = read_json(E / 'new-vector-cache.json') if (E / 'new-vector-cache.json').exists() else {}
    validate_attempts(frozen,attempts,durable_cache)
    require(len(attempts) < frozen['maximum_paid_attempts'], 'Attempt cap reached')
    require(len(work['text'].encode()) <= frozen['token_limit_per_input'], 'Conservative byte/token cap exceeded')
    budget = guard_window(frozen, extra_stop, charged_attempts=len(attempts), prospective_attempts=1)
    verify_execution_identity(frozen)
    # Credential loading occurs only after execute and exact-input guards.
    key = transient_project_credential()
    # Recheck STOP/deadline/ledger immediately before the durable attempt.
    budget = guard_window(frozen, extra_stop, charged_attempts=len(attempts), prospective_attempts=1)
    record = {'number':len(attempts)+1,'kind':work['kind'],'key':work['key'],'sha256':h,'input_utf8_bytes':len(work['text'].encode()),'status':'attempt_started','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'per_attempt_upper_usd':frozen['per_attempt_upper_usd'],'budget_guard':budget}
    if recovery_applies:
        record.update(manual_retry_of_attempt=2,manual_recovery_id=frozen['manual_recovery']['id'],manual_retry_of_attempt_sha256=objsha(frozen['manual_recovery']['historical_attempts'][1]),manual_recovery_history_sha256=frozen['manual_recovery']['historical_attempts_sha256'])
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
    manual_retry = bool(getattr(args,'manual_retry_document_attempt_three',False))
    if manual_retry:
        require(args.execute and not args.replay,'Manual retry flag requires --execute')
        require(attempts == frozen['manual_recovery']['historical_attempts'],'Manual recovery already consumed or another attempt occurred')
    cache.update(new_cache)
    pending = [item for item in frozen['approved_inputs'] if item['sha256'] not in cache]
    require(set(item['sha256'] for item in pending) <= set(frozen['pending_input_sha256']),'Pending workload expanded')
    live_budget = guard_window(frozen,args.stop_file,charged_attempts=len(attempts),prospective_attempts=len(pending)) if not args.replay else None
    plan = {'status':'plan_only','model':g.SEMANTIC_MODEL_ID,'dimensions':768,'frozen_sha256':sha((E / 'frozen-inventory-queries.json').read_bytes()),'logical_inputs':len(frozen['approved_inputs']),'frozen_queries':len(frozen['queries']),'reused_exact_input_vectors':len(frozen['reused_cache_provenance']),'reused_query_vectors':sum(q['query_sha256'] in frozen['reused_cache_provenance'] for q in frozen['queries']),'new_proposal_documents':1,'pending_texts':len(pending),'pending_inputs':[{'kind':x['kind'],'key':x['key'],'sha256':x['sha256'],'utf8_bytes':len(x['text'].encode())} for x in pending],'pending_input_utf8_bytes':sum(len(x['text'].encode()) for x in pending),'maximum_calls':frozen['maximum_paid_attempts'],'automatic_retries':0,'nominal_pending_upper_usd':len(pending)*frozen['per_attempt_upper_usd'],'additional_conservative_upper_usd':frozen['maximum_additional_cost_usd'],'previous_tracked_cost_upper_usd':frozen['previous_tracked_cost_upper_usd'],'maximum_cumulative_tracked_upper_usd':frozen['previous_tracked_cost_upper_usd']+frozen['maximum_additional_cost_usd'],'project_budget_usd':frozen['project_budget_usd'],'deadline_utc':frozen['deadline_utc'],'planned_result_rows':56,'states':list(STATES),'price_usd_per_million_tokens':frozen['price_usd_per_million_tokens'],'token_limit_per_input':frozen['token_limit_per_input'],'price_source':'https://ai.google.dev/gemini-api/docs/pricing','token_limit_source':'https://ai.google.dev/gemini-api/docs/embeddings','live_budget_guard':live_budget,'budget_limit_note':'Tracked cleanup attempt upper bounds; unrelated account work is not reconciled with billing.'}
    plan.update(already_attempted_calls=len(attempts),failed_or_uncertain_attempts_charged=sum(a['status'] != 'completed' for a in attempts),maximum_manual_recovery_allowance=1,manual_recovery_authorized=True,manual_recovery_id=frozen['manual_recovery']['id'],confirmed_recovery_plan_sha256=sha((E/'confirmed-recovery-plan.json').read_bytes()),planned_total_attempts_including_historical_attempts=len(attempts)+len(pending),planned_total_attempt_upper_usd=(len(attempts)+len(pending))*frozen['per_attempt_upper_usd'],planned_cumulative_upper_usd=frozen['previous_tracked_cost_upper_usd']+(len(attempts)+len(pending))*frozen['per_attempt_upper_usd'])
    plan.update(original_maximum_calls=14,original_additional_upper_usd=.0229376,charged_historical_attempts=2,confirmed_effective_cap=15)
    if not args.execute and not args.replay:
        write_json(E / 'confirmed-recovery-workload.json',plan)
        write_json(E / 'confirmed-recovery-plan-validation.json',{'status':'zero_call_plan_validation','baseline_document_count':len(old['entries']),'baseline_shards':shard_checks,'baseline_exact_text_vector_bm25f_validation':True,'reused_cache_records':len(cache),'all_primary_targets_exact_existing_action':True,'source_runtime_index_written':False,'query_retrieval_measurements':0})
        print(json.dumps(plan,indent=2))
        return
    require(current == states['proposal'] and source.read_bytes() == raw_proposal(frozen),'Apply exact source proposal before execute/replay')
    require_continuation(frozen,attempts,permit_initial_manual_retry=manual_retry)
    if args.replay:
        require(not pending,'Replay missing vector; API fallback forbidden')
    else:
        require(git('rev-parse','HEAD').decode().strip() == frozen['baseline_commit'],'HEAD changed before execute; review freeze')
        for item in pending:
            call_one_input(frozen,item,cache,attempts,args.stop_file,manual_retry=manual_retry)
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
    parser.add_argument('--manual-retry-document-attempt-three',action='store_true',help='Consume the sole directly confirmed exact-document retry as attempt3; never retry anything else')
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
