"""Hash-bound, read-only two-state krummholz DATA experiment helpers."""
from pathlib import Path
import copy
import datetime as dt
import gzip
import hashlib
import json
import math
import os
import subprocess
import sys

sys.dont_write_bytecode = True
E = Path(__file__).resolve().parent
R = next(parent for parent in E.parents if (parent / 'skills/photo-prompt-image-generator/scripts/prompt_generator.py').is_file())
A = R / 'skills/photo-prompt-image-generator/assets'
W = R.parent / 'daylong-progress'
sys.path.insert(0, str(A.parent / 'scripts'))
import prompt_generator as g

TARGET = 'slot:surface_material:treeline_wind_pruned_krummholz_surface'
ALIAS = '왜성변형수 바람형 패치'
STATES = ('baseline', 'proposal')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def objsha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('w', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    fd = os.open(path.parent, os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=R)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_freeze():
    raw = (E / 'frozen-inventory-queries.json').read_bytes()
    require(sha(raw) == (E / 'frozen-sha256.txt').read_text().split()[0], 'Freeze SHA mismatch')
    frozen = json.loads(raw)
    for name, expected in frozen['artifact_sha256'].items():
        require(sha((E / name).read_bytes()) == expected, 'Frozen artifact changed: ' + name)
    for name, expected in frozen['runtime_sources_sha256'].items():
        require(sha((R / name).read_bytes()) == expected, 'Runtime code changed: ' + name)
    if frozen.get('manual_recovery'):
        recovery = frozen['manual_recovery']
        original_raw = (E / recovery['original_failure_snapshot_file']).read_bytes()
        require(sha(original_raw) == recovery['original_failure_snapshot_sha256'], 'Original failure byte digest changed')
        require(json.loads(original_raw) == [recovery['failed_attempt']], 'Original failure snapshot/object mismatch')
        require(objsha(recovery['failed_attempt']) == recovery['failed_attempt_object_sha256'], 'Original failed-attempt object digest changed')
        require(recovery['retry_input_sha256'] == frozen['proposal_document']['sha256'], 'Manual retry target differs from proposal document')
        require(recovery['maximum_manual_retries'] == 1 and recovery['retry_attempt_number'] == 2, 'Manual recovery allowance changed')
    inventory = frozen['inventory']
    require(len(inventory) == 11 and len({row['id'] for row in inventory}) == 11, 'Inventory membership/count changed')
    require(all(row['slot'] == 'surface_material' for row in inventory), 'Inventory slot changed')
    require(sum(row['decision'] == 'fix' for row in inventory) == 1, 'Expected one alias proposal')
    scout = read_json(E / 'scout/frozen-proposal-and-unmeasured-probes.json')
    require(sha((E / 'scout/frozen-proposal-and-unmeasured-probes.json').read_bytes()) == frozen['scout_freeze_sha256'], 'Scout freeze mismatch')
    changed = next(row for row in inventory if row['decision'] == 'fix')
    require('slot:' + changed['slot'] + ':' + changed['id'] == TARGET, 'Wrong proposal row')
    require(changed['before'] == scout['before'] and changed['proposal'] == scout['proposed'], 'Proposal differs from unmeasured scout')
    require({k:v for k,v in changed['proposal'].items() if k != 'aliases'} == {k:v for k,v in changed['before'].items() if k != 'aliases'}, 'Changed a non-alias field')
    require(changed['proposal']['aliases'] == changed['before']['aliases'] + [ALIAS], 'Not exact append-only alias')
    queries = frozen['queries']
    require(len(queries) == len({q['id'] for q in queries}) == len({q['query'] for q in queries}) == 13, 'Query membership/count changed')
    require([q['original_query'] for q in queries[:8]] == scout['queries'], 'Original eight probes changed')
    require([q['query'] for q in queries[8:11]] == ['krummholz', '크룸홀츠', '왜성변형수'], 'Bare-name controls changed')
    sources = {}
    for q in queries:
        require(q['slot'] == 'surface_material', 'Query slot changed')
        require(q['query_sha256'] == sha(q['query'].encode()), 'Query text hash changed')
        require(q['original_query_sha256'] == objsha(q['original_query']), 'Query object hash changed')
        require(q['query'] == q['original_query']['query'], 'Copied query text changed')
        if q.get('source_snapshot_file'):
            name = q['source_snapshot_file']
            if name not in sources:
                source_raw = (E / name).read_bytes()
                require(sha(source_raw) == q['source_sha256'], 'Query provenance source SHA mismatch')
                sources[name] = json.loads(source_raw)
            require(q['original_query'] in sources[name]['queries'], 'Original query absent from copied source')
    inputs = frozen['approved_inputs']
    require(len(inputs) == 14 and len({x['sha256'] for x in inputs}) == 14, 'Input inventory changed')
    require(inputs == [{'kind':'document','key':TARGET,'text':frozen['proposal_document']['text'],'sha256':frozen['proposal_document']['sha256']}] + [{'kind':'query','key':q['id'],'text':q['query'],'sha256':q['query_sha256']} for q in queries], 'Input inventory exceeds exact document and queries')
    require(all(x['sha256'] == sha(x['text'].encode()) for x in inputs), 'Input hash mismatch')
    require(frozen['maximum_paid_attempts'] == 15 and frozen['automatic_retries'] == 0, 'Attempt policy changed')
    require(frozen['maximum_additional_cost_usd'] == 0.024576, 'Cost cap changed')
    require(frozen['states'] == list(STATES) and frozen['planned_result_rows'] == 52, 'Matrix changed')
    return frozen


def states_from_freeze(frozen):
    baseline = json.loads(gzip.decompress((E / 'baseline-merged-data.json.gz').read_bytes()))
    require(g.dictionary_hash(baseline) == frozen['baseline_dictionary_hash'], 'Baseline dictionary mismatch')
    states = {label:copy.deepcopy(baseline) for label in STATES}
    for item in frozen['inventory']:
        for label in STATES:
            rows = states[label]['slots'][item['slot']]
            position = next(i for i,row in enumerate(rows) if row['id'] == item['id'])
            require(rows[position] == item['before'], 'Baseline row mismatch')
            rows[position] = copy.deepcopy(item['before'] if label == 'baseline' else item['proposal'])
        if item['decision'] == 'keep':
            require(item['before'] == item['proposal'], 'Kept row changed')
    for label,data in states.items():
        require(g.dictionary_hash(data) == frozen['state_dictionary_hashes'][label], 'State dictionary hash mismatch')
    return states


def validate_vector(record, text=None):
    require(record.get('model') == g.SEMANTIC_MODEL_ID and record.get('dimensions') == 768, 'Incompatible cache model/dimensions')
    require(isinstance(record.get('text'), str) and (text is None or record['text'] == text), 'Cache exact text mismatch')
    vector = record.get('vector')
    require(isinstance(vector,list) and len(vector) == 768, 'Vector dimension mismatch')
    require(all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in vector), 'Nonfinite or nonnumeric vector')
    require(sum(v*v for v in vector) > 0, 'Zero-norm vector')


def load_reused_cache(frozen):
    cache = read_json(E / 'reused-vector-cache.json')
    require(set(cache) == set(frozen['reused_cache_provenance']), 'Reused cache membership mismatch')
    sources = {}
    for h,record in cache.items():
        validate_vector(record)
        require(sha(record['text'].encode()) == h, 'Cache text key mismatch')
        provenance = frozen['reused_cache_provenance'][h]
        name = provenance['source_snapshot_file']
        if name not in sources:
            raw = (E / name).read_bytes()
            require(sha(raw) == provenance['source_sha256'], 'Cache provenance source SHA mismatch')
            sources[name] = json.loads(raw)
        original = sources[name][provenance['original_cache_key']]
        require(original == record and objsha(record['vector']) == provenance['vector_sha256'], 'Copied cache differs from original')
    approved = {x['sha256']:x for x in frozen['approved_inputs']}
    require(set(cache) <= set(approved), 'Unapproved reused cache input')
    for h,record in cache.items():
        validate_vector(record, approved[h]['text'])
    require([x['sha256'] for x in frozen['approved_inputs'] if x['sha256'] not in cache] == frozen['pending_input_sha256'], 'Frozen missing input membership mismatch')
    return cache


def load_baseline_index(frozen, baseline):
    manifest = read_json(E / 'baseline-index-manifest.json')
    entries, checks = {}, []
    for descriptor in manifest['shards']:
        relative = str((A / descriptor['path']).relative_to(R))
        path = R / relative
        raw = path.read_bytes() if path.exists() else b''
        origin = 'existing_hash_verified_shard'
        if sha(raw) != descriptor['sha256']:
            # Only the verified published baseline commit is needed, never a
            # private branch or unpublished comparator. No fetch/pull occurs.
            raw = git('show', frozen['baseline_commit'] + ':' + relative)
            origin = 'published_baseline_git_object'
        require(sha(raw) == descriptor['sha256'], 'Baseline shard SHA mismatch: ' + relative)
        shard = json.loads(raw)['entries']
        require(len(shard) == descriptor['entry_count'] and not set(entries).intersection(shard), 'Shard membership mismatch')
        entries.update(shard)
        checks.append({'path':relative,'sha256':descriptor['sha256'],'entry_count':len(shard),'source':origin})
    require(set(entries) == set(manifest['entry_order']), 'Baseline index membership mismatch')
    index = {**manifest,'entries':{key:entries[key] for key in manifest['entry_order']}}
    rows = g.iter_semantic_entries(baseline)
    require(len(entries) == len(rows) == frozen['baseline_document_count'], 'Document count mismatch')
    require([key for key,*_ in rows] == manifest['entry_order'], 'Full index order mismatch')
    for key,kind,row,slot in rows:
        entry = entries[key]
        require((entry['kind'],entry['slot'],entry['id'],entry['text']) == (kind,slot,row['id'],g.semantic_text_for_entry(row,slot,kind=kind)), 'Index exact input mismatch: ' + key)
        validate_vector({'model':index['embedding_model'],'dimensions':index['embedding_dimensions'],'text':entry['text'],'vector':entry['vector']})
    g.validate_semantic_index_metadata(index, baseline)
    require(g.semantic_bm25f_payload_from_index(index) == g.build_semantic_bm25f_payload(baseline), 'Complete baseline BM25F mismatch')
    return index, checks


def guard_window(frozen, extra_stop=None, charged_attempts=0, prospective_attempts=0):
    require(not (W / 'STOP').exists(), 'STOP requested')
    if extra_stop is not None:
        require(not extra_stop.exists(), 'Additional STOP requested')
    ledger = read_json(W / 'ledger.json')
    deadline = min(dt.datetime.fromisoformat(frozen['deadline_utc'].replace('Z','+00:00')),dt.datetime.fromisoformat(ledger['deadline_utc'].replace('Z','+00:00')))
    require(dt.datetime.now(dt.timezone.utc) < deadline, 'Deadline reached')
    cycle_upper = frozen['previous_tracked_cost_upper_usd'] + charged_attempts * frozen['per_attempt_upper_usd']
    cost = max(float(ledger['tracked_project_cost_upper_usd']),cycle_upper)
    budget = min(float(ledger['hard_project_budget_usd']),frozen['project_budget_usd'])
    require(cost + prospective_attempts * frozen['per_attempt_upper_usd'] <= budget, 'Project budget would be exceeded')
    require((charged_attempts + prospective_attempts) * frozen['per_attempt_upper_usd'] <= frozen['maximum_additional_cost_usd'] + 1e-12, 'Cycle cost cap exceeded')
    return {'ledger_tracked_upper_usd':float(ledger['tracked_project_cost_upper_usd']),'accounted_tracked_upper_usd':cost,'budget_usd':budget,'deadline_utc':deadline.isoformat()}


def raw_proposal(frozen):
    raw = (E / 'baseline-raw-extension.json').read_bytes()
    item = next(x for x in frozen['inventory'] if x['decision'] == 'fix')
    before = json.dumps(item['before'],ensure_ascii=False).encode()
    after = json.dumps(item['proposal'],ensure_ascii=False).encode()
    require(raw.count(before) == 1, 'Cannot identify exact baseline row')
    proposed = raw.replace(before,after,1)
    expected = json.loads(raw)
    rows = expected['slots'][item['slot']]
    rows[next(i for i,row in enumerate(rows) if row['id'] == item['id'])] = item['proposal']
    require(json.loads(proposed) == expected and sha(proposed) == frozen['proposed_raw_source_sha256'], 'Minimal raw proposal mismatch')
    return proposed
