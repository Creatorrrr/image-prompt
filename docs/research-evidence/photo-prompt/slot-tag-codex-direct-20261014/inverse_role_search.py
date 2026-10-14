"""Stage 5C mechanical inverse role search, never semantic role adjudication.

No import performs inference. prepare_assets freezes a candidate-free bilingual
query plan. execute_queries is a separately gated, explicitly local-only action.
retrieve_assets searches the whole shared positive pool and writes evidence only.
These scene-free role queries do NOT establish runtime core-bound query proof.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SCRIPTS = REPO / 'skills/photo-prompt-image-generator/scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from local_execution_ledger import Ledger, canonical, digest, read, write_once

RECIPE = 'photo-direct-scene-free-inverse-role/v1'
SCOPE = 'whole_shared_positive_corpus'


def evidence_directory(path):
    path = Path(path).resolve()
    if HERE not in path.parents:
        raise ValueError('output must be an explicit dedicated descendant of this evidence directory')
    return path


def require_local(space):
    if space.get('provider') != 'embeddinggemma2-local' or space.get('dimensions') != 768:
        raise ValueError('explicit embeddinggemma2-local space required; no provider fallback')
    from photo_embedding_provider import validate_space
    from photo_local_embedding import installed_binding
    validate_space(space)
    installation = installed_binding()
    if installation['space'] != space:
        raise ValueError('installed embedding provider/space mismatch')
    return installation


def role_input(catalog, slot):
    """Use exact authored EN+KO boundaries together, without translating either.

    Candidate values, binding candidates and scene/core projections cannot enter
    this function. The same bilingual specification supplies both retrieval lanes.
    Human review must still decide whether source bilingual definitions agree.
    """
    from photo_slot_queries import specification
    spec = specification(catalog, slot)
    spec = {**spec, 'recipe': RECIPE}
    text = ('Photographic role mapping / 사진 역할 매핑\n'
            'The following is a role specification, with inclusion and exclusion boundaries.\n'
            '다음은 포함 및 제외 경계가 있는 역할 명세입니다.\n' +
            canonical(spec).decode())
    fields = {'global_context': '',
              'slot_focus': '\n'.join([spec['focus_en'], spec['focus_ko'],
                                        *spec['includes'], *spec['owners'], *spec['property_prefixes']])}
    binding = {'recipe': RECIPE, 'slot_id': slot, 'language': 'en+ko-authored',
               'slot_spec_sha256': digest(spec), 'query_fields': fields,
               'scene_context': None, 'core_bound_runtime_proof': False,
               'search_scope': SCOPE, 'tag_admission_filter': False}
    return {'slot_id': slot, 'text': text, 'text_sha256': hashlib.sha256(text.encode()).hexdigest(),
            'specification': spec, 'fields': fields, 'binding': binding}


def whole_pool(corpus, reader):
    from photo_global_index import POSITIVE_KINDS
    positive = sorted(cid for cid, row in corpus['candidates'].items()
                      if row['record_kind'] in POSITIVE_KINDS)
    ids = list(reader.meta['positive_ids'])
    shard_ids = [cid for shard in reader.meta['vector_shards'] for cid in shard['ids']]
    if (len(ids) != len(set(ids)) or sorted(ids) != positive
            or len(shard_ids) != len(set(shard_ids)) or sorted(shard_ids) != positive):
        raise ValueError('duplicate or dropped whole positive pool identity')
    if (digest(corpus) != reader.manifest['corpus_sha256']
            or digest(corpus) != reader.meta['corpus_sha256']
            or corpus['slot_catalog'] != reader.meta['slot_catalog']
            or corpus['slot_bindings'] != reader.meta['slot_bindings']):
        raise ValueError('source/index/catalog/binding mismatch')
    return positive


def source_file_hashes(assets):
    import photo_candidate_corpus as c
    manifest = Path(assets) / c.MANIFEST_NAME
    rows = read(manifest)['modules']
    paths = [manifest, *(Path(assets) / row['file'] for row in rows)]
    return {str(p.relative_to(assets)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def make_plan(corpus, reader, space, *, installation, source_files, expected_slot_count=139):
    positive = whole_pool(corpus, reader)
    catalog = corpus['slot_catalog']
    if len(catalog) != expected_slot_count:
        raise ValueError('current catalog slot coverage changed; review explicit expected count')
    if reader.manifest['space'] != space or installation['space'] != space:
        raise ValueError('query/index/installed embedding space mismatch')
    if space.get('provider') != 'embeddinggemma2-local':
        raise ValueError('no nonlocal provider admission')
    rows = [role_input(catalog, slot) for slot in sorted(catalog)]
    plan = {'schema': 'photo-direct-inverse-query-plan/v1', 'recipe': RECIPE,
            'purpose': 'scene-free role-mapping review; not runtime core-bound slot proof',
            'source_sha256': digest(corpus), 'source_files': source_files,
            'catalog_sha256': digest(catalog), 'binding_sha256': digest(corpus['slot_bindings']),
            'index_sha256': digest(reader.manifest),
            'index_source_sha256': reader.manifest['index_source_sha256'],
            'space': space, 'space_sha256': digest(space), 'installation': installation,
            'positive_count': len(positive), 'positive_ids_sha256': digest(positive),
            'expected_input_count': len(rows), 'queries': rows,
            'search_scope': SCOPE, 'tag_admission_filter': False,
            'lane_limit': 384, 'minimum_similarity': .30, 'rrf_k': 30}
    plan['canonical_sha256'] = digest(plan)
    return plan


def validate_plan(plan, corpus, reader, installation, source_files, *, expected_slot_count=139):
    expected = make_plan(corpus, reader, plan['space'], installation=installation,
                         source_files=source_files, expected_slot_count=expected_slot_count)
    if plan != expected:
        raise ValueError('query plan/source/index/space mutated; explicit new plan required')


def prepare_assets(assets, output):
    """Read/verify real sources and installed files; no model inference here."""
    import photo_candidate_corpus as c
    import photo_search_layout as layout
    from photo_search_reader import SearchReader
    output = evidence_directory(output)
    corpus = c.load(assets)
    reader = SearchReader(assets)
    try:
        space = reader.manifest['space']
        installation = require_local(space)
        verification = layout.verify(assets, corpus, reader.manifest)
        plan = make_plan(corpus, reader, space, installation=installation,
                         source_files=source_file_hashes(Path(assets)))
        # Record a complete verified source/index closure before freezing the plan.
        write_once(output / 'source-index-verification.json', verification)
        write_once(output / 'query-plan.json', plan)
        return plan
    finally:
        reader.close()


def validate_result(plan, row, query):
    from photo_embedding_provider import validate_execution, validate_vector
    request = {'schema': 'photo-local-embedding-request/v1', 'text': query['text'],
               'text_sha256': query['text_sha256'], 'space': plan['space'],
               'binding': {**query['binding'], 'inverse_plan_sha256': plan['canonical_sha256']}, 'kind': 'query'}
    if (row.get('request') != request or type(row.get('cache_hit')) is not bool
            or row.get('vector_sha256') != digest(row.get('vector'))):
        raise ValueError('embedding cache/request/vector binding mismatch')
    validate_vector(row['vector'], plan['space']['dimensions'])
    validate_execution(row['execution'], plan['space'], query['text'], row['vector'], 'query')


def execute_queries(assets, output, run_id, *, execution_enabled=False, before_start=None):
    """Root must enable and wire global counters before the one local provider call.

    No injectable executor exists in production: tests patch the provider function
    and supply explicit mock traces. A run ID or provider attempt is never retried.
    Document/build embedding execution is unsupported here; Ledger itself accepts
    kind=document for a future explicit integration using the same accounting.
    """
    if execution_enabled is not True or not callable(before_start):
        raise ValueError('explicit execution enablement and pre-call counter hook required')
    import photo_candidate_corpus as c
    import photo_search_layout as layout
    from photo_search_reader import SearchReader
    from photo_embedding_provider import embed_many
    output = evidence_directory(output)
    plan = read(output / 'query-plan.json')
    corpus = c.load(assets)
    reader = SearchReader(assets)
    try:
        installation = require_local(plan['space'])
        validate_plan(plan, corpus, reader, installation, source_file_hashes(Path(assets)))
        layout.verify(assets, corpus, reader.manifest)
        queries = plan['queries']
        ledger = Ledger(output / 'execution-ledger')
        ledger.plan(run_id, [q['text'] for q in queries],
                    binding={'inverse_plan_sha256': plan['canonical_sha256']}, space=plan['space'])
        ledger.start(run_id)
        receipts = []
        provider_reference = None
        try:
            # Publish started/unknown accounting before any provider execution.
            # A callback failure is also durable and cannot look like zero work.
            before_start({'run_id': run_id, 'expected_input_count': len(queries),
                          'ledger_directory': str(ledger.directory),
                          'inverse_plan_sha256': plan['canonical_sha256']})
            # A private run cache prevents embed_many's permissive failure retry
            # semantics from reusing a previous run's unresolved provider attempts.
            rows = embed_many([q['text'] for q in queries],
                              [{**q['binding'], 'inverse_plan_sha256': plan['canonical_sha256']} for q in queries],
                              output / 'execution-ledger' / run_id / 'provider-cache',
                              space=plan['space'], kind='query')
            provider_reference = write_once(output / 'execution-ledger' / run_id / 'provider-return.json',
                                            {'rows': rows})
            if len(rows) != len(queries):
                raise ValueError('provider result cardinality differs from exact planned count')
            for i, (query, row) in enumerate(zip(queries, rows, strict=True)):
                validate_result(plan, row, query)
                receipts.append({'input_index': i, 'validated': True, 'cache_hit': row['cache_hit'],
                                 'text_sha256': query['text_sha256'], 'trace_sha256': digest(row['execution'])})
            result = {'schema': 'photo-direct-inverse-query-results/v1',
                      'run_id': run_id, 'plan_sha256': plan['canonical_sha256'], 'rows': rows}
            reference = write_once(output / 'execution-ledger' / run_id / 'query-results.json', result)
            ledger.finish(run_id, state='complete', receipts=receipts, result_reference=reference)
            return result
        except BaseException as error:
            ledger.finish(run_id, state='failed', receipts=receipts, result_reference=provider_reference,
                          error_type=type(error).__name__)
            raise
    finally:
        reader.close()


def fusion(lanes, k=30):
    scores = {}
    counts = {}
    for lane in lanes:
        ids = [r['document_id'] for r in lane]
        if len(set(ids)) != len(ids):
            raise ValueError('duplicate candidate identity in retrieval lane')
        for rank, cid in enumerate(ids, 1):
            scores[cid] = scores.get(cid, 0.) + 1 / (k + rank)
            counts[cid] = counts.get(cid, 0) + 1
    return sorted([{'document_id': cid, 'score': round(score, 12), 'lane_count': counts[cid]}
                   for cid, score in scores.items()],
                  key=lambda r: (-r['score'], -r['lane_count'], r['document_id']))


def full_scan_oracle(corpus, reader, fields, vector, *, limit, minimum):
    """Independent source-rebuilt BM25F + all-vector scalar scan, no tree pruning."""
    from photo_global_index import lexical
    from bm25f_retrieval import rank_bm25f
    positive = whole_pool(corpus, reader)
    lexical_rows = rank_bm25f(lexical(corpus), fields, limit=limit, allowed_ids=positive)
    norm = math.sqrt(math.fsum(x * x for x in vector))
    cosine = []
    seen = []
    for leaf, shard in enumerate(reader.meta['vector_shards']):
        values = reader.block('vector', leaf)
        for offset, cid in enumerate(shard['ids']):
            seen.append(cid)
            reference = values[offset * 768:(offset + 1) * 768]
            score = math.fsum(a * b for a, b in zip(reference, vector, strict=True)) / (
                math.sqrt(math.fsum(x * x for x in reference)) * norm)
            if score >= minimum:
                cosine.append((cid, score))
    if len(seen) != len(set(seen)) or sorted(seen) != positive:
        raise ValueError('full scan oracle saw a dropped/duplicate pool')
    cosine.sort(key=lambda r: (-r[1], r[0]))
    return lexical_rows, [{'document_id': cid, 'score': round(score, 9)}
                          for cid, score in cosine[:limit]]


def search_one(corpus, reader, query, vector, *, limit=384, minimum=.30, oracle=False):
    import photo_sharded_search as search
    from audit_global_retrieval import lexical_replay, fusion as audit_fusion
    allowed = set(whole_pool(corpus, reader))
    before = dict(reader.metrics)
    lexical = search.lexical_rank(reader, query['fields'], allowed, limit)
    if lexical != lexical_replay(reader, query['fields'], allowed, limit):
        raise ValueError('BM25F lane replay mismatch')
    cosine, proof = search.cosine_rank(reader, vector, allowed, limit, minimum)
    search.audit_cosine(reader, vector, allowed, cosine, proof)
    for lane in (lexical, cosine):
        ids = [r['document_id'] for r in lane]
        if len(ids) != len(set(ids)) or not set(ids) <= allowed:
            raise ValueError('duplicate/diagnostic/foreign lane identity')
    combined = fusion([lexical, cosine])
    if combined != audit_fusion([lexical, cosine]):
        raise ValueError('independent RRF replay mismatch')
    oracle_record = {'state': 'not_requested', 'quality_claim': False}
    if oracle:
        ol, ov = full_scan_oracle(corpus, reader, query['fields'], vector, limit=limit, minimum=minimum)
        if ol != lexical or ov != cosine or fusion([ol, ov]) != combined:
            raise ValueError('independent full scan oracle mismatch')
        oracle_record = {'state': 'passed', 'positive_count': len(allowed),
                         'scope': 'all source positive documents and all stored vectors', 'quality_claim': False}
    source_ids = {}
    for row in combined:
        cid = row['document_id']
        record = reader.record(cid)
        if record != corpus['candidates'][cid]:
            raise ValueError('retrieved candidate/source mismatch')
        source_ids[cid] = {'source_ids': [p['source'] for p in record['provenance']],
                           'provenance': record['provenance'],
                           'authored_record_sha256': digest(record)}
    return {'slot_id': query['slot_id'], 'query_sha256': query['text_sha256'],
            'slot_spec_sha256': query['binding']['slot_spec_sha256'],
            'search_scope': SCOPE, 'tag_admission_filter': False, 'positive_count': len(allowed),
            'positive_ids_sha256': digest(sorted(allowed)),
            'lanes': {'bm25f': {'state': 'executed', 'ranks': lexical},
                      'embedding': {'state': 'executed', 'ranks': cosine}},
            'union_candidate_ids': sorted({r['document_id'] for r in lexical + cosine}),
            'rrf': combined, 'source_ids': source_ids, 'cosine_proof': proof,
            'reader_io_before': before, 'reader_io_after': dict(reader.metrics),
            'full_scan_oracle': oracle_record}


def retrieve_assets(assets, output, run_id, *, oracle_slots=(), progress=None):
    import photo_candidate_corpus as c
    import photo_search_layout as layout
    from photo_search_reader import SearchReader
    output = evidence_directory(output)
    plan = read(output / 'query-plan.json')
    ledger = Ledger(output / 'execution-ledger')
    run_directory = ledger._run(run_id)
    result_path = run_directory / 'query-results.json'
    result = read(result_path)
    ledger_outcome = read(result_path.parent / 'outcome.json')
    ledger_plan = read(run_directory / 'planned.json')
    ledger_start = read(run_directory / 'started.json')
    if (ledger_outcome['state'] != 'complete' or result['plan_sha256'] != plan['canonical_sha256']
            or result['run_id'] != run_id or ledger_outcome['run_id'] != run_id
            or ledger_plan['run_id'] != run_id or ledger_start['run_id'] != run_id
            or ledger_outcome['planned_sha256'] != digest(ledger_plan)
            or ledger_start['planned_sha256'] != digest(ledger_plan)
            or ledger_outcome['started_sha256'] != digest(ledger_start)
            or ledger_plan['binding'] != {'inverse_plan_sha256': plan['canonical_sha256']}
            or ledger_plan['space'] != plan['space'] or ledger_plan['kind'] != 'query'
            or ledger_plan['expected_input_count'] != plan['expected_input_count']
            or ledger_plan['input_sha256'] != [q['text_sha256'] for q in plan['queries']]
            or ledger_outcome['result_reference']['sha256'] != hashlib.sha256(result_path.read_bytes()).hexdigest()
            or len(result['rows']) != plan['expected_input_count']):
        raise ValueError('complete exact-plan inference result and receipt required')
    corpus = c.load(assets)
    reader = SearchReader(assets)
    try:
        validate_plan(plan, corpus, reader, require_local(plan['space']), source_file_hashes(Path(assets)))
        verification = layout.verify(assets, corpus, reader.manifest)
        if not set(oracle_slots) <= set(corpus['slot_catalog']):
            raise ValueError('unknown oracle slot')
        searches = []
        for query, row in zip(plan['queries'], result['rows'], strict=True):
            validate_result(plan, row, query)
            searches.append(search_one(corpus, reader, query, row['vector'],
                                       limit=plan['lane_limit'], minimum=plan['minimum_similarity'],
                                       oracle=query['slot_id'] in oracle_slots))
            if progress is not None:
                progress({'completed': len(searches), 'total': len(plan['queries']),
                          'slot_id': query['slot_id']})
        record = {'schema': 'photo-direct-inverse-search-results/v1', 'plan_sha256': plan['canonical_sha256'],
                  'run_id': run_id, 'source_sha256': plan['source_sha256'],
                  'catalog_sha256': plan['catalog_sha256'], 'binding_sha256': plan['binding_sha256'],
                  'index_sha256': plan['index_sha256'], 'index_source_sha256': plan['index_source_sha256'],
                  'space': plan['space'], 'space_sha256': plan['space_sha256'],
                  'source_index_verification': verification, 'searches': searches,
                  'reader_io_total': dict(reader.metrics),
                  'stage5c_complete': False, 'semantic_adjudication_complete': False,
                  'core_bound_runtime_proof': False}
        write_once(output / ('inverse-search-' + run_id + '.json'), record)
        return record
    finally:
        reader.close()
