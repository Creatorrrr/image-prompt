#!/usr/bin/env python3
"""Rebuild source-bound magical-girl research and candidate search views.

This does not verify research truth, authorize selection, or build an index.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'assets'
sys.path.insert(0, str(ROOT / 'scripts'))
import photo_candidate_retrieval_views as rv


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    registry_path = ASSETS / 'photo_magical_girl_semantics_20261107.json'
    registry = read(registry_path)
    rows = registry['rows']
    assert len(rows) == 301 and len({x['source_row_id'] for x in rows}) == 301
    research_views = []
    for index, row in enumerate(rows):
        cells = row['source_cells']
        label, definition = cells[0], cells[-1]
        research_views.append({
            'id': 'magical-girl-context-' + row['source_row_id'],
            'term_id': row['source_row_id'],
            'source_term_label': label,
            'context_ko': definition,
            'source_cells': cells,
            'source_quotes': [{'pointer': f'/rows/{index}/source_cells/{i}', 'quote': cell}
                              for i, cell in enumerate(cells)],
            'concept_ids': row['concept_ids'],
            'routes': row['routes'],
            'external_evidence': row['external_evidence'],
            'external_evidence_status': row['external_evidence_status'],
            'external_unresolved': row['external_unresolved'],
            'candidate_comparison_pointer': f'/rows/{index}/existing_candidate_comparisons',
            'candidate_review_status': row['existing_candidate_review_status'],
            'semantic_boundary_ko': row['semantic_boundary_ko'],
            'safety_and_scope': row['safety_and_scope'],
            'context_only': True,
            'native_approval': False,
        })
    write(ASSETS / 'photo_magical_girl_research_context_views_20261107.json', {
        'schema': 'magical-girl-research-context-views/v1',
        'source_registry': registry_path.name,
        'source_registry_sha256': file_sha(registry_path),
        'search_scope': 'Research context only; not a native candidate or positive retrieval module.',
        'views': research_views,
    })
    modules = ['photo_candidate_magical_girl_20261107.json',
               'photo_candidate_magical_girl_dark_20261107.json']
    records, source_hashes = {}, {}
    for name in modules:
        path = ASSETS / name
        module = read(path)
        assert not set(records).intersection(module['candidates'])
        records.update(module['candidates'])
        source_hashes[name] = file_sha(path)
    views = []
    for cid, record in sorted(records.items()):
        if record['record_kind'] == 'diagnostic':
            continue
        content = record['content']
        # Each generated candidate has one base realization. Do not invent
        # language for branches: require explicit authoring if this changes.
        assert rv.realization_ids(record) == ['base']
        aliases = content['aliases']
        assert aliases and all(isinstance(x, str) and x for x in aliases)
        base_quotes = [{'pointer': '/content/en', 'quote': content['en']},
                       {'pointer': '/content/ko', 'quote': content['ko']}]
        for kind in ('whole', 'context'):
            key = f'{cid}:base:{kind}'
            lookup_quotes = []
            if kind == 'whole':
                en, ko, quotes = content['en'], content['ko'], base_quotes
            else:
                terms = ' / '.join(aliases)
                en = f"Magical-girl visual option; source terms: {terms}. {content['en']}"
                ko = f"마법소녀 시각 선택지; 원문 용어: {terms}. {content['ko']}"
                quotes = base_quotes
                lookup_quotes = [
                    {'pointer': f'/content/aliases/{i}', 'quote': value}
                    for i, value in enumerate(aliases)
                ]
                if 'magical_girl' in content.get('tags', []):
                    lookup_quotes.append({'pointer': '/content/tags/' + str(content['tags'].index('magical_girl')),
                                          'quote': 'magical_girl'})
                assert all(rv.at_pointer(record, q['pointer']) == q['quote'] for q in lookup_quotes)
            views.append({
                'id': rv.view_id(cid, 'base', key), 'candidate_id': cid,
                'realization_id': 'base', 'key': key, 'kind': kind,
                'source_record_sha256': rv.digest(record), 'text_en': en,
                'text_ko': ko, 'source_quotes': quotes,
                'source_lookup_quotes': lookup_quotes,
                'native_approval': False,
            })
    module = {
        'schema': rv.SCHEMA, 'recipe': rv.RECIPE,
        'source_inventory_id': 'magical-girl-20261107',
        'coverage': {'source_modules_sha256': source_hashes,
                     'positive_realizations': sum(x['record_kind'] != 'diagnostic' for x in records.values()),
                     'diagnostics_excluded': sum(x['record_kind'] == 'diagnostic' for x in records.values()),
                     'context_views': len(views) // 2},
        'native_approval': False, 'views': views,
    }
    rv.validate(module, records)
    write(ASSETS / 'photo_candidate_retrieval_views_magical_girl_20261107.json', module)
    print(json.dumps({'research_views': len(research_views), **module['coverage'],
                      'candidate_search_views': len(views)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
