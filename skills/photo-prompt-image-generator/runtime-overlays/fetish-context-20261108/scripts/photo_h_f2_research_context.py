"""A sealed, advisory research-context lane for H-F2; never a material source."""
import gzip
import hashlib
import json
import math
import re

import numpy as np
from bm25f_retrieval import rank_bm25f, tokenize_bm25f_text, validate_bm25f_index
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
