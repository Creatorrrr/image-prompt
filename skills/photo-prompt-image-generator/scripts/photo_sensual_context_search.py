#!/usr/bin/env python3
"""Search source-bound sensual research context, separately from H-F2 candidates.

This read-only lexical research tool never establishes candidate eligibility,
a person's identity, interest or consent, nor visual or pixel qualification.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
from bm25f_retrieval import build_bm25f_index, rank_bm25f

ASSETS = Path(__file__).resolve().parents[1] / 'assets'
CONTEXT = 'photo_sensual_research_context_views_20261108.json'
POLICY = {'k1': 1.2, 'fields': {'term': {'weight': 4.0, 'b': 0.75}, 'definition': {'weight': 1.0, 'b': 0.75}}}

def search(query: str, *, limit: int = 10, assets: Path = ASSETS) -> dict:
    if not isinstance(query, str) or not query.strip() or not 1 <= limit <= 50:
        raise ValueError('nonempty query and limit 1..50 required')
    assets = Path(assets)
    raw = (assets / CONTEXT).read_bytes()
    payload = json.loads(raw)
    if payload.get('schema') != 'photo-sensual-research-context/v1':
        raise ValueError('unexpected context schema')
    registry_name = payload['source_registry']
    if Path(registry_name).name != registry_name:
        raise ValueError('unsafe registry name')
    registry_bytes = (assets / registry_name).read_bytes()
    if hashlib.sha256(registry_bytes).hexdigest() != payload['source_registry_sha256']:
        raise ValueError('registry hash mismatch')
    registry = json.loads(registry_bytes)
    source = {row['id']: row for row in registry['source_term_inventory']}
    docs, rows, seen_terms = {}, {}, set()
    for row in payload['views']:
        rid, term_id = row['id'], row['term_id']
        if rid in rows or term_id in seen_terms or row.get('context_only') is not True or row.get('native_approval') is not False:
            raise ValueError('invalid context identity or authority')
        base = source[term_id]
        seen_terms.add(term_id)
        if row['source_term_label'] != base['term'] or row['context_ko'] != base['definition']:
            raise ValueError('context differs from source inventory')
        rows[rid] = row
        docs[rid] = {'term': [row['source_term_label']], 'definition': [row['context_ko']]}
    if seen_terms != set(source):
        raise ValueError('source coverage mismatch')
    index = build_bm25f_index(docs, policy=POLICY)
    hits = rank_bm25f(index, {'query': query}, allowed_ids=sorted(docs), limit=limit)
    def checked_related(row):
        result = []
        for ref in row.get('related_existing_examples', row.get('candidate_refs', [])):
            item = dict(ref)
            name = item.get('module', '')
            if Path(name).name != name:
                item['hash_status'] = 'unsafe_path'
            else:
                try:
                    data = json.loads((assets / name).read_bytes())['candidates'][item['candidate_id']]
                    raw_candidate = json.dumps(data, ensure_ascii=False, sort_keys=True,
                                               separators=(',', ':'), allow_nan=False).encode('utf-8')
                    item['hash_status'] = ('match' if hashlib.sha256(raw_candidate).hexdigest()
                                           == item['source_record_sha256'] else 'changed')
                except (OSError, ValueError, KeyError, TypeError):
                    item['hash_status'] = 'unavailable'
            for binding in item.get('binding_refs', []):
                name = binding.get('module', '')
                if Path(name).name != name:
                    binding['hash_status'] = 'unsafe_path'
                    continue
                try:
                    data = json.loads((assets / name).read_bytes())['slot_bindings'][binding['id']]
                    raw_binding = json.dumps(data, ensure_ascii=False, sort_keys=True,
                                             separators=(',', ':'), allow_nan=False).encode('utf-8')
                    binding['hash_status'] = ('match' if hashlib.sha256(raw_binding).hexdigest()
                                              == binding['binding_sha256'] else 'changed')
                except (OSError, ValueError, KeyError, TypeError):
                    binding['hash_status'] = 'unavailable'
            result.append(item)
        return result
    def checked_review(row):
        review = copy.deepcopy(row.get('coverage_review'))
        if review is None:
            return None
        review['candidate_refs'] = checked_related(review)
        for component in review.get('components', []) + review.get('followup_findings', []):
            component['candidate_refs'] = checked_related(component)
            if isinstance(component.get('followup_evidence'), dict):
                followup = component['followup_evidence']
                followup['candidate_refs'] = checked_related(followup)
        return review
    return {'schema':'photo-sensual-research-search/v1','query':query,
            'index':'in_memory_bm25f', 'source_count':len(rows),
            'source_context_sha256':hashlib.sha256(raw).hexdigest(),
            'source_registry_sha256':payload['source_registry_sha256'],
            'scope':'research context only; not H-F2 search, semantic qualification or candidate adoption',
            'native_approval':False,
            'results':[{'id':h['document_id'],'score':h['score'],'matched_terms':h['matched_terms'],
                        'term_id':rows[h['document_id']]['term_id'],
                        'term':rows[h['document_id']]['source_term_label'],
                        'context_ko':rows[h['document_id']]['context_ko'],
                        'candidate_ids':rows[h['document_id']]['candidate_ids'],
                        'related_existing_examples':checked_related(rows[h['document_id']]),
                        'coverage_review':checked_review(rows[h['document_id']]),
                        'additional_source_evidence':rows[h['document_id']].get('additional_source_evidence',[]),
                        'unreviewed_alias_lead_count':len(rows[h['document_id']].get('existing_alias_leads',[])),
                        'context_only':True,'native_approval':False} for h in hits]}

def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument('query'); parser.add_argument('--limit',type=int,default=10)
    args=parser.parse_args()
    print(json.dumps(search(args.query,limit=args.limit),ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
