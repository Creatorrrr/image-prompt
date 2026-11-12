#!/usr/bin/env python3
"""Read-only search over the source conversation's tsundere research context.

Research lookup is separate from H-F2 and grants no candidate, visual, prompt,
identity, consent or native qualification. Source wording is not a dictionary.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from bm25f_retrieval import build_bm25f_index, rank_bm25f, normalize_bm25f_text

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
CONTEXT = 'photo_tsundere_research_context_views_20261112.json'
PROSE_CONTEXT = 'photo_tsundere_prose_context_20261112.json'
POLICY = {'k1': 1.2, 'fields': {
    'term': {'weight': 4.0, 'b': 0.75},
    'source_forms': {'weight': 3.0, 'b': 0.75},
    'related_examples': {'weight': 0.7, 'b': 0.75},
    'partial_related': {'weight': 1.0, 'b': 0.75},
    'description': {'weight': 1.0, 'b': 0.75},
}}
# These are segmentation aids, never identity or synonym claims.  They permit
# partial-match discovery in Japanese sentences without a general substring lane.
JAPANESE_SEARCH_LEXICON = ('傘', '渡す', '避け', '贈り物', '相手', '視線')

# A specific adult-context lookup is necessary: ordinary clothing, teasing,
# switch, brat, and other ambiguous terms are not by themselves adult context.
_EXPLICIT_ADULT = re.compile(
    r'(?<![a-z])(?:bdsm|fetish(?:ism|istic)?|femdom|dominatrix|'
    r'brat[ -]tamer|erotic[ -]humiliation)(?![a-z])|'
    r'(?:페티시|페티쉬|성인\s*(?:역할극|페티시|성적)|성적\s*(?:긴장|취향|역할)|'
    r'관능적\s*(?:페티시|성적)|본디지|펨돔|도미나트릭스|브랫\s*테이머|ツンエロ|츤에로)', re.IGNORECASE)


def _load(assets: Path) -> tuple[dict, str]:
    raw = (Path(assets) / CONTEXT).read_bytes()
    payload = json.loads(raw)
    if payload.get('schema') != 'photo-tsundere-research-context/v1':
        raise ValueError('unexpected context schema')
    rows = payload.get('views')
    if not isinstance(rows, list) or len(rows) != 346:
        raise ValueError('source row count mismatch')
    ids = set()
    for row in rows:
        tid = row.get('term_id')
        if (not re.fullmatch(r'T\d\d-\d\d', str(tid)) or tid in ids
                or row.get('id') != 'tsundere_context_' + tid.lower()
                or row.get('context_only') is not True
                or row.get('native_approval') is not False
                or row.get('automatic_activation') is not False
                or not isinstance(row.get('source_cells'), list)
                or len(row['source_cells']) < 2
                or row['source_cells'][0] != row.get('source_term_label')
                or ' | '.join(row['source_cells'][1:]) != row.get('context_ko')):
            raise ValueError('invalid source row identity, text, or authority')
        for name in ('source_alternate_form_leads', 'related_search_examples', 'partial_related_search_leads'):
            values = row.get(name, [])
            if not isinstance(values, list) or any(not isinstance(x, str) or not x for x in values):
                raise ValueError('invalid source form leads')
        if row.get('partial_related_search_leads') and not row.get('partial_related_search_boundary'):
            raise ValueError('partial related leads need a meaning boundary')
        ids.add(tid)
    return payload, hashlib.sha256(raw).hexdigest()


def _load_prose(assets: Path) -> tuple[dict, str]:
    raw = (Path(assets) / PROSE_CONTEXT).read_bytes()
    payload = json.loads(raw)
    rows = payload.get('views')
    if (payload.get('schema') != 'photo-tsundere-prose-context/v1'
            or payload.get('native_approval') is not False or not isinstance(rows, list)):
        raise ValueError('unexpected prose context schema or authority')
    seen = set()
    paragraph_ids = set()
    for row in rows:
        tid, loc = row.get('term_id'), row.get('source_location', {})
        cells = row.get('source_cells')
        if (not isinstance(tid, str) or not re.fullmatch(r'[PX]\d{3}', tid) or tid in seen
                or row.get('id') != 'tsundere_prose_' + tid.lower()
                or row.get('context_only') is not True or row.get('native_approval') is not False
                or row.get('automatic_activation') is not False
                or not isinstance(cells, list) or len(cells) != 2
                or cells[0] != row.get('source_term_label') or cells[1] != row.get('context_ko')
                or not isinstance(loc.get('start_codepoint'), int)
                or not isinstance(loc.get('end_codepoint_exclusive'), int)
                or not isinstance(loc.get('quoted_text'), str)):
            raise ValueError('invalid prose row identity or authority')
        text = cells[1]
        start, end = loc['start_codepoint'], loc['end_codepoint_exclusive']
        if (not 0 <= start <= end <= len(text) or text[start:end] != loc['quoted_text']
                or hashlib.sha256(text.encode('utf-8')).hexdigest() != loc.get('paragraph_sha256')):
            raise ValueError('prose quote does not match source paragraph')
        if row.get('unit_kind') == 'paragraph':
            paragraph_ids.add(tid)
        seen.add(tid)
    if paragraph_ids != {f'P{i:03d}' for i in range(1, 71)}:
        raise ValueError('prose source paragraph coverage mismatch')
    return payload, hashlib.sha256(raw).hexdigest()


def search(query: str, *, limit: int = 10, adult_context: bool = False,
           include_prose: bool = False, assets: Path = ASSETS) -> dict:
    if not isinstance(query, str) or not query.strip() or not 1 <= limit <= 50:
        raise ValueError('nonempty query and limit 1..50 required')
    if not isinstance(adult_context, bool) or not isinstance(include_prose, bool):
        raise ValueError('adult_context and include_prose must be boolean')
    payload, digest = _load(assets)
    explicit_adult = bool(adult_context or _EXPLICIT_ADULT.search(normalize_bm25f_text(query)))
    rows = {row['id']: row for row in payload['views']}
    prose = None
    prose_digest = None
    if include_prose:
        prose, prose_digest = _load_prose(assets)
        for row in prose['views']:
            if row['id'] in rows:
                raise ValueError('duplicate research context identity')
            # Preserve empty prose entries in the source snapshot, but do not
            # create a synthetic searchable keyword for an empty paragraph.
            if row['context_ko'].strip():
                rows[row['id']] = row
    docs = {rid: {'term': [row['source_term_label']],
                  'source_forms': row['source_alternate_form_leads'],
                  'related_examples': row['related_search_examples'],
                  'partial_related': row.get('partial_related_search_leads', []),
                  'description': [row['context_ko']]} for rid, row in rows.items()}
    index = build_bm25f_index(docs, policy=POLICY, lexicon=JAPANESE_SEARCH_LEXICON)
    allowed = [rid for rid, row in rows.items() if explicit_adult or not row['adult_research_context']]
    hits = rank_bm25f(index, {'query': query}, allowed_ids=allowed, limit=limit)
    return {'schema':'photo-tsundere-context-search/v1', 'query':query,
            'index':'in_memory_bm25f', 'source_count':len(rows),
            'source_context_sha256':digest, 'source_table_sha256':payload['source']['source_table_sha256'],
            **({'prose_context_sha256':prose_digest,
                'source_prose_sha256':prose['source']['sha256'],
                'prose_record_count':len(prose['views'])} if prose is not None else {}),
            'source_url':payload['source']['url'], 'adult_context_lookup':explicit_adult,
            'scope':'research only; no H-F2 candidate issuance, native approval or image qualification',
            'native_approval':False,
            'results':[{**rows[h['document_id']], 'score':h['score'], 'matched_terms':h['matched_terms']}
                       for h in hits]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument('query')
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--include-prose', action='store_true',
                        help='also search the separately source-bound prose context')
    parser.add_argument('--adult-context', action='store_true',
                        help='include separately marked adult research rows for an explicit context lookup')
    args = parser.parse_args()
    print(json.dumps(search(args.query, limit=args.limit, adult_context=args.adult_context, include_prose=args.include_prose),
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
