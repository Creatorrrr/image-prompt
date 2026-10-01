"""Read-only frozen evidence helpers; no API calls or runtime writes."""
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
R = E.parents[3]
A = R / 'skills/photo-prompt-image-generator/assets'
W = R.parent / 'daylong-progress'
sys.path.insert(0, str(A.parent / 'scripts'))
import prompt_generator as g

REEF = 'slot:action:reef_flat_crest_forereef_wave_gradient'
STATES = ('baseline', 'old_corrected_labels', 'fresh_explicit_unit')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def objsha(value):
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())


def read_json(path):
    return json.loads(Path(path).read_text())


def write_json(path, value):
    """Durable atomic local evidence write; no secret values are accepted by callers."""
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
        require(sha((E / name).read_bytes()) == expected, 'Frozen evidence changed: ' + name)
    for name, expected in frozen['runtime_sources_sha256'].items():
        require(sha((R / name).read_bytes()) == expected, 'Runtime code changed: ' + name)
    # The historical trial is unpushed. Its provenance remains frozen, while
    # reproduction on a fresh published clone uses included exact snapshots.
    historical_ref = subprocess.run(
        ['git', 'rev-parse', '--verify', 'refs/heads/' + frozen['historical_trial']['branch']],
        cwd=R, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
    )
    if historical_ref.returncode == 0:
        require(historical_ref.stdout.decode().strip() == frozen['historical_trial']['tip'], 'Historical deferred branch moved')
    require(len(frozen['inventory']) == 17, 'Inventory count changed')
    queries = frozen['queries']
    require(len(queries) == 30 and len({q['id'] for q in queries}) == 30 and len({q['query'] for q in queries}) == 30, 'Probe uniqueness/count changed')
    historical_path = E / 'historical/frozen-inventory-queries.json'
    historical = read_json(historical_path)
    require(sha(historical_path.read_bytes()) == frozen['historical_trial']['source_file_sha256']['frozen-inventory-queries.json'], 'Original freeze hash mismatch')
    require([item['original_inventory_object'] for item in frozen['inventory']] == historical['inventory'], 'Original inventory objects changed')
    for item in frozen['inventory']:
        require(item['original_inventory_object_sha256'] == objsha(item['original_inventory_object']), 'Original inventory object hash mismatch')
    supplemental = read_json(E / 'historical/prior-action-probe-inventory.json')
    require([q['original_query'] for q in queries[:14]] == historical['queries'], 'Historical primary probes changed')
    require([q['original_record'] for q in queries[14:]] == supplemental['queries'], 'Historical supplemental probes changed')
    sources = {}
    for q in queries:
        source = (q['source_commit'], q['source_file'])
        if source not in sources:
            source_raw = (E / q['source_snapshot_file']).read_bytes()
            require(sha(source_raw) == q['source_sha256'], 'Original query inventory source hash mismatch')
            sources[source] = json.loads(source_raw)
        require(q['original_query'] in sources[source]['queries'], 'Original query missing from its pinned source')
        require(q['query'] == q['original_query']['query'], 'Query text changed')
        require(q['query_sha256'] == sha(q['query'].encode()), 'Query text hash changed')
        require(q['original_query_sha256'] == objsha(q['original_query']), 'Original query object changed')
        normalized = q['original_query']['target']
        if not normalized.startswith('slot:'):
            normalized = 'slot:' + normalized
        require(q['target'] == normalized and q['slot'] == q['original_query']['slot'], 'Probe scope changed')
    return frozen


def states_from_freeze(frozen):
    baseline = json.loads(gzip.decompress((E / 'baseline-merged-data.json.gz').read_bytes()))
    require(g.dictionary_hash(baseline) == frozen['baseline_dictionary_hash'], 'Baseline dictionary mismatch')
    states = {label: copy.deepcopy(baseline) for label in STATES}
    for item in frozen['inventory']:
        for label in STATES:
            rows = states[label]['slots'][item['slot']]
            position = next(i for i, row in enumerate(rows) if row['id'] == item['id'])
            require(rows[position] == item['before'], 'Baseline inventory mismatch')
            rows[position] = copy.deepcopy(item[label])
        if item['decision'] == 'keep':
            require(item['before'] == item['old_corrected_labels'] == item['fresh_explicit_unit'], 'Control modified')
        else:
            before, old, fresh = item['before'], item['old_corrected_labels'], item['fresh_explicit_unit']
            require({k: v for k, v in before.items() if k not in ('en', 'ko')} == {k: v for k, v in old.items() if k not in ('en', 'ko')}, 'Comparator exceeds exact label edits')
            require({k: v for k, v in fresh.items() if k != 'concept_units'} == old and fresh['concept_units'] == [old['en']], 'Fresh proposal exceeds exact explicit unit')
    require(sum(x['decision'] == 'fix' for x in frozen['inventory']) == 1, 'Wrong fix count')
    for label, data in states.items():
        require(g.dictionary_hash(data) == frozen['state_dictionary_hashes'][label], 'State hash mismatch: ' + label)
    return states


def validate_vector(record, text=None):
    require(record.get('model') == g.SEMANTIC_MODEL_ID and record.get('dimensions') == 768, 'Incompatible cache metadata')
    require(isinstance(record.get('text'), str) and (text is None or record['text'] == text), 'Cache input mismatch')
    vector = record.get('vector')
    require(isinstance(vector, list) and len(vector) == 768, 'Vector dimension mismatch')
    require(all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in vector), 'Nonfinite or nonnumeric vector')
    require(sum(v*v for v in vector) > 0, 'Zero-norm vector')


def load_reused_cache(frozen):
    cache = read_json(E / 'reused-vector-cache.json')
    require(set(cache) == set(frozen['reused_cache_provenance']), 'Frozen reused cache membership mismatch')
    sources = {}
    for h, record in cache.items():
        validate_vector(record)
        require(sha(record['text'].encode()) == h, 'Cache key mismatch')
        provenance = frozen['reused_cache_provenance'][h]
        source = (provenance['source_commit'], provenance['source_file'])
        if source not in sources:
            raw = (E / provenance['source_snapshot_file']).read_bytes()
            require(sha(raw) == provenance['source_sha256'], 'Original cache source hash mismatch')
            sources[source] = json.loads(raw)
        original = sources[source][provenance['original_cache_key']]
        require(original == record and objsha(record['vector']) == provenance['vector_sha256'], 'Original cached vector changed')
    require(len(cache) == 31, 'Need 30 cached probes and one comparator document')
    return cache


def load_baseline_index(frozen, baseline):
    manifest = read_json(E / 'baseline-index-manifest.json')
    entries = {}
    checks = []
    for descriptor in manifest['shards']:
        relative = str((A / descriptor['path']).relative_to(R))
        path = R / relative
        raw = path.read_bytes() if path.exists() else b''
        origin = 'existing_hash_verified_shard'
        if sha(raw) != descriptor['sha256']:
            raw = git('show', frozen['baseline_commit'] + ':' + relative)
            origin = 'pinned_baseline_git_object'
        require(sha(raw) == descriptor['sha256'], 'Baseline shard SHA mismatch: ' + relative)
        shard = json.loads(raw)['entries']
        require(len(shard) == descriptor['entry_count'] and not set(entries).intersection(shard), 'Baseline shard membership mismatch')
        entries.update(shard)
        checks.append({'path': relative, 'sha256': descriptor['sha256'], 'entry_count': len(shard), 'source': origin})
    require(set(entries) == set(manifest['entry_order']), 'Baseline manifest membership mismatch')
    index = {**manifest, 'entries': {key: entries[key] for key in manifest['entry_order']}}
    rows = g.iter_semantic_entries(baseline)
    require(len(entries) == len(rows) == frozen['baseline_document_count'], 'Document count mismatch')
    require([key for key, *_ in rows] == manifest['entry_order'], 'Full index order mismatch')
    for key, kind, row, slot in rows:
        entry = entries[key]
        require((entry['kind'], entry['slot'], entry['id'], entry['text']) == (kind, slot, row['id'], g.semantic_text_for_entry(row, slot, kind=kind)), 'Full index exact document mismatch: ' + key)
        validate_vector({'model': index['embedding_model'], 'dimensions': index['embedding_dimensions'], 'text': entry['text'], 'vector': entry['vector']})
    g.validate_semantic_index_metadata(index, baseline)
    require(g.semantic_bm25f_payload_from_index(index) == g.build_semantic_bm25f_payload(baseline), 'Baseline complete BM25F derivation mismatch')
    return index, checks


def guard_window(frozen, extra_stop=None, prospective_attempts=0):
    require(not (W / 'STOP').exists(), 'STOP requested; no new work permitted')
    if extra_stop is not None:
        require(not extra_stop.exists(), 'Additional STOP requested')
    ledger = read_json(W / 'ledger.json')
    deadline = min(dt.datetime.fromisoformat(frozen['deadline_utc'].replace('Z', '+00:00')), dt.datetime.fromisoformat(ledger['deadline_utc'].replace('Z', '+00:00')))
    require(dt.datetime.now(dt.timezone.utc) < deadline, 'Deadline reached')
    cost = max(float(ledger['tracked_project_cost_upper_usd']), frozen['previous_tracked_cost_upper_usd'])
    budget = min(float(ledger['hard_project_budget_usd']), frozen['project_budget_usd'])
    require(cost + prospective_attempts * frozen['per_attempt_upper_usd'] <= budget, 'Project budget would be exceeded')
    return {'ledger_tracked_upper_usd': cost, 'budget_usd': budget, 'deadline_utc': deadline.isoformat()}


def raw_proposal(frozen):
    raw = (E / 'baseline-raw-extension.json').read_bytes()
    item = next(x for x in frozen['inventory'] if x['decision'] == 'fix')
    before = json.dumps(item['before'], ensure_ascii=False).encode()
    after = json.dumps(item['fresh_explicit_unit'], ensure_ascii=False).encode()
    require(raw.count(before) == 1, 'Cannot identify one exact baseline source row')
    proposed = raw.replace(before, after, 1)
    expected = json.loads(raw)
    rows = expected['slots'][item['slot']]
    rows[next(i for i, row in enumerate(rows) if row['id'] == item['id'])] = item['fresh_explicit_unit']
    require(json.loads(proposed) == expected and sha(proposed) == frozen['proposed_raw_source_sha256'], 'Minimal raw proposal mismatch')
    return proposed
