"""A sealed, advisory research-context lane for H-F2; never a material source."""
import gzip
import hashlib
import json
import math
import re

import numpy as np
from bm25f_retrieval import rank_bm25f, tokenize_bm25f_text, validate_bm25f_index, normalize_bm25f_text
import photo_candidate_corpus as corpus
import photo_recall_first as rf

FILE = 'research-context-index.json.gz'
SCHEMA = 'photo-h-f2-research-context-index/v1'
POLICY = {'k1': 1.2, 'fields': {
    'term': {'weight': 4.0, 'b': 0.75},
    'context': {'weight': 1.5, 'b': 0.75},
    'boundary': {'weight': 0.5, 'b': 0.75},
    'tags': {'weight': 0.5, 'b': 0.75},
}}
CUES = frozenset({'fetish', 'fetishism', 'fetishist', 'fetishistic', 'fetishwear',
                  'fetish-inspired', '페티시', '페티시즘', '페티시스트', '페티시적인',
                  '페티시웨어', 'podophilia', 'trichophilia'})
PARTICLES = ('에서', '으로', '이란', '라는', '란', '의', '에', '을', '를', '은', '는', '이', '가', '와', '과')
EXPLICIT_NEGATION = re.compile(
    r'\b(?:no|not|without|exclude|excluding|avoid)\s+(?:any\s+)?fetish\w*\b'
    r'|(?:페티시\w*\s*(?:제외|없이|금지|아닌))', re.I)
CONTROL = re.compile(r'\bfetish\s*[:=]\s*[0-3](?:\.0+)?\b', re.I)


def text(row):
    return ('Term: ' + row['term'] + '\nAliases: ' + '; '.join(row['search_aliases'])
            + '\nContext: ' + row['context_ko'] + '\nBoundary: ' + row['boundary'])


def documents(rows):
    return {row['id']: {'term': [row['term'], *row['search_aliases']],
            'context': row['context_ko'], 'boundary': row['boundary'],
            'tags': ['fetish 페티시']} for row in rows}


def load(generation):
    manifest = generation.manifest
    descriptor = manifest.get('research_context')
    if descriptor is None:
        return None
    rf.require(descriptor.get('schema') == SCHEMA and descriptor.get('file') == FILE,
               'unknown research context index')
    rf.require(FILE in manifest['files'], 'unsealed research context index')
    with gzip.open(generation.root / FILE, 'rt', encoding='utf-8') as stream:
        data = json.load(stream)
    rf.require(data['schema'] == SCHEMA and data['binding'] == generation.binding,
               'research context space or schema changed')
    rows = data['rows']
    rf.require(len(rows) == descriptor['rows'] == 28 and len({r['id'] for r in rows}) == len(rows),
               'research context population changed')
    rf.require(corpus.digest(data) == descriptor['canonical_sha256'], 'research context data changed')
    validate_bm25f_index(data['lexical_index'], documents(rows), policy=POLICY)
    for row in rows:
        rf.require(row['tags'] == ['fetish'] and row['context_only'] is True
                   and row['native_approval'] is False and len(row['vector']) == 768,
                   'research context identity, scope or vector changed')
        rf.require(all(math.isfinite(v) for v in row['vector']), 'nonfinite context vector')
        proof = row['embedding_execution']
        rf.require(proof['provider_executed'] is True and proof['kind'] == 'document'
                   and proof['space'] == data['binding']['space']
                   and proof['installation_sha256'] == data['binding']['installation_hash']
                   and proof['input_sha256'] == hashlib.sha256(('title: none | text: ' + text(row)).encode()).hexdigest()
                   and proof['vector_sha256'] == corpus.digest(row['vector']),
                   'research context document embedding evidence changed')
    return data


def stems(query, rows):
    words = {word for row in rows for alias in row['search_aliases'] for word in alias.split()
             if re.fullmatch(r'[가-힣]+', word)}
    endings = '|'.join(PARTICLES)
    return sorted(word for word in words if re.search(
        rf'(?<![가-힣]){re.escape(word)}(?:{endings})(?![가-힣])', query))


def query(generation, data, query_text, vector, limit=3):
    """Use the original, already-verified H-F2 query vector; no model calls."""
    if data is None:
        return []
    clean = CONTROL.sub(' ', query_text)
    if EXPLICIT_NEGATION.search(clean):
        return []
    # The shared tokenizer keeps ASCII hyphens inside words. Normalize only
    # these explicit topic forms for the auxiliary lexical lane; the H-F2
    # material query and its embedding remain byte-for-byte unchanged.
    clean = re.sub(r'\bfetish-(?=(?:fashion|wear|styling)\b)', 'fetish ', clean, flags=re.I)
    words = stems(clean, data['rows'])
    tokens = set(tokenize_bm25f_text(clean)) | set(words)
    if not tokens.intersection(CUES):
        return []
    sparse = rank_bm25f(data['lexical_index'], {'query': clean, 'authored_alias_stems': words})
    if not sparse:
        return []
    matrix = np.asarray([r['vector'] for r in data['rows']], dtype='<f8')
    q = np.asarray(vector, dtype='<f8')
    rf.require(q.shape == (768,) and np.isfinite(q).all(), 'invalid context query vector')
    norms = np.linalg.norm(matrix, axis=1) * np.linalg.norm(q)
    rf.require((norms > 0).all(), 'zero context embedding norm')
    dense = matrix.dot(q) / norms
    by_id = {r['id']: r for r in data['rows']}
    lexical = {r['document_id']: (i + 1, r) for i, r in enumerate(sparse)}
    # Dense search reranks lexical witnesses, rather than admitting unrelated
    # contexts simply because every document contains the word fetish.
    dense_rank = {data['rows'][i]['id']: rank for rank, i in enumerate(
        sorted(range(len(data['rows'])), key=lambda i: (-float(dense[i]), data['rows'][i]['id'])), 1)}
    scores = {rid: 1 / (10 + lr) + 1 / (10 + dense_rank[rid]) for rid, (lr, _) in lexical.items()}
    result = []
    for rid in sorted(scores, key=lambda k: (-scores[k], k))[:limit]:
        source = by_id[rid]
        row = {k: source[k] for k in ('id', 'term', 'context_ko', 'boundary', 'tags',
               'source_file', 'source_sha256', 'context_only', 'native_approval')}
        row['retrieval'] = {'lexical_rank': lexical[rid][0], 'dense_rank': dense_rank[rid],
                            'rrf': round(scores[rid], 12), 'matched_terms': lexical[rid][1]['matched_terms']}
        result.append(row)
    return result


def audit(generation, packet):
    data = load(generation)
    if data is None:
        rf.require('research_contexts' not in packet, 'unsealed research context results')
        return
    expected = {slot: query(generation, data, q['text'], packet['queries'][slot]['row']['vector'])
                for slot, q in packet['query_set']['slots'].items()}
    rf.require(packet.get('research_contexts') == expected, 'research context results changed')

# A second, lexical-only advisory lane. The old index and ranking remain intact.
_legacy_load = load
_legacy_query = query
TS_FILE = 'tsundere-research-context-index.json.gz'
TS_SCHEMA = 'photo-h-f2-tsundere-research-context-index/v1'
TS_POLICY = {'k1': 1.2, 'fields': {
    'term': {'weight': 4.0, 'b': 0.75},
    'source_forms': {'weight': 3.0, 'b': 0.75},
    'related_examples': {'weight': 0.7, 'b': 0.75},
    'partial_related': {'weight': 1.0, 'b': 0.75},
    'description': {'weight': 1.0, 'b': 0.75},
}}
TS_LEXICON = ('傘', '渡す', '避け', '贈り物', '相手', '視線')
# A control value is not an explicit topic. Negation anywhere suppresses the
# new lane, deliberately favoring omission over leaking an excluded context.
TS_NEGATION = re.compile(
    r"\b(?:no|not|without|exclude|excluding|avoid|never|nonsexual|non-sexual)\b"
    r"|\b(?:isn|aren|don|doesn|didn|won|wouldn|shouldn|can|couldn)['’]t\b"
    r'|\b(?:bdsm|fetish|femdom|tsundere)[ -]free\b'
    r'|\bnon[- ](?:bdsm|fetish|femdom|tsundere)\b'
    r'|(?:제외|없[이는데어]|금지|아닌|않[는고아]|말고|비성적|빼고|아니[고며])'
    r'|(?:除[く外]|なし|ない|不要|禁止)', re.I)
TS_ADULT = re.compile(
    r'(?<![a-z])(?:bdsm|fetish(?:ism|istic)?|femdom|dominatrix|'
    r'brat[ -]tamer|erotic[ -]humiliation)(?![a-z])|'
    r'(?:페티시|페티쉬|성인\s*(?:역할극|페티시|성적)|성적\s*(?:긴장|취향|역할)|'
    r'관능적\s*(?:페티시|성적)|본디지|펨돔|도미나트릭스|브랫\s*테이머|ツンエロ|츤에로)', re.I)
TS_TOPIC = re.compile(r'츤|ツン|(?<![a-z])tsun(?:dere)?(?![a-z])', re.I)


def ts_documents(rows):
    return {r['id']: {'term': [r['source_term_label']],
            'source_forms': r['source_alternate_form_leads'],
            'related_examples': r['related_search_examples'],
            'partial_related': r.get('partial_related_search_leads', []),
            'description': [r['context_ko']]} for r in rows}


def ts_requires_adult_context(row):
    # Some otherwise general source rows mention an adult use as one example.
    # Do not expose the whole unredacted row without an explicit adult lookup.
    fields = [row['source_term_label'], row['context_ko'],
              *row['source_alternate_form_leads'], *row['related_search_examples'],
              *row.get('partial_related_search_leads', [])]
    return row['adult_research_context'] or any(TS_ADULT.search(s) for s in fields)


def ts_exact_witness_ids(rows, clean):
    # Without an explicit topic cue, only a whole-query source expression is a
    # witness. Description overlap and generic related examples never open the lane.
    queries = {normalize_bm25f_text(clean), normalize_bm25f_text(TS_ADULT.sub(' ', clean))} - {''}
    matches = set()
    for row in rows:
        if row['term_id'].startswith('P'):
            continue
        label = row['source_term_label']
        authored = [label, *re.split(r'[·・]', label), *row['source_alternate_form_leads'],
                    *row.get('partial_related_search_leads', [])]
        if queries.intersection(normalize_bm25f_text(item) for item in authored):
            matches.add(row['id'])
    return matches


def load(generation):
    legacy = _legacy_load(generation)
    desc = generation.manifest.get('tsundere_research_context')
    if desc is None:
        return legacy
    rf.require(desc.get('schema') == TS_SCHEMA and desc.get('file') == TS_FILE
               and TS_FILE in generation.manifest['files'], 'unsealed tsundere context')
    with gzip.open(generation.root / TS_FILE, 'rt', encoding='utf-8') as stream:
        data = json.load(stream)
    rf.require(data.get('schema') == TS_SCHEMA and data.get('binding') == generation.binding
               and corpus.digest(data) == desc.get('canonical_sha256'), 'tsundere context changed')
    rows = data['rows']
    ids = {r['term_id'] for r in rows}
    expected = ({f'T{table:02d}-{n:02d}' for table, n in data['table_ids']}
                | {f'P{i:03d}' for i in range(1, 71)}
                | {f'X{i:03d}' for i in range(1, 22)})
    rf.require(len(rows) == desc.get('rows') == 437 and len(ids) == 437
               and ids == expected and sum(t.startswith('T') for t in ids) == 346,
               'tsundere population changed')
    rf.require(all(r.get('context_only') is True and r.get('native_approval') is False
                   and r.get('automatic_activation') is False
                   and isinstance(r.get('adult_research_context'), bool)
                   and r.get('candidate_refs') == [] for r in rows),
               'tsundere context authority changed')
    validate_bm25f_index(data['lexical_index'], ts_documents(rows), policy=TS_POLICY, lexicon=TS_LEXICON)
    return {'_combined_research_context_v1': True, 'legacy': legacy, 'tsundere': data}


def query(generation, data, query_text, vector, limit=3):
    if not isinstance(data, dict) or data.get('_combined_research_context_v1') is not True:
        return _legacy_query(generation, data, query_text, vector, limit)
    result = _legacy_query(generation, data['legacy'], query_text, vector, limit)
    clean = CONTROL.sub(' ', query_text)
    if TS_NEGATION.search(clean):
        return result
    ts = data['tsundere']
    adult = bool(TS_ADULT.search(clean))
    topic = bool(TS_TOPIC.search(clean))
    witnesses = None if topic else ts_exact_witness_ids(ts['rows'], clean)
    if witnesses is not None and not witnesses:
        return result
    allowed = [r['id'] for r in ts['rows'] if (topic or r['id'] in witnesses)
               and (adult or not ts_requires_adult_context(r))]
    ranked = rank_bm25f(ts['lexical_index'], {'query': clean}, allowed_ids=allowed, limit=limit)
    rows = {r['id']: r for r in ts['rows']}
    for hit in ranked:
        row = dict(rows[hit['document_id']])
        row['source'] = ts['sources']['prose' if row['term_id'].startswith(('P', 'X')) else 'table']
        row['retrieval'] = {'lane': 'tsundere_research_context', 'lexical_score': hit['score'],
                            'matched_terms': hit['matched_terms'], 'adult_context_explicit': adult,
                            'adult_context_required': ts_requires_adult_context(row)}
        result.append(row)
    return result
