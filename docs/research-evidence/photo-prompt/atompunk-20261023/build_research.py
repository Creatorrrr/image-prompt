"""Create local research projections and a read-only corpus audit; never import drafts."""
import csv
import hashlib
import json
import re
from collections import Counter
from research_context import ASSETS, HERE, ROOT, CONVERSATION, DATE, seeds


def tsv(name):
    with (HERE / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def digest(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def parse_cards():
    cards, drafts = [], []
    for row in tsv('CARD-SPECS.tsv'):
        owners = [dict(zip(('id', 'visible_property_en'), x.strip().split('=', 1)))
                  for x in row['owners_en'].split(';') if x.strip()]
        relations = [dict(zip(('subject', 'predicate', 'object'),
                             [v.strip() for v in x.split('|')]))
                     for x in row['relations'].split(';') if x.strip()]
        card = {'id': row['id'], 'seed_ids': [f'A{int(i):03}' for i in row['seed_numbers'].split(',')],
                'mode': row['mode'], 'priority': row['priority'],
                'planned_slots': row['slots'].split(','), 'source_ids': row['sources'].split(','),
                'source_support': 'limited term/context support; authored scene proposal, not source-attested full object',
                'owners': owners, 'relations': relations,
                'positive_proposal_ko': row['positive_ko'],
                'confusion_boundaries_ko': row['confusion_ko'].split(';'),
                'claim_limit_ko': row['claim_limit_ko'],
                'status': 'research_draft_not_native_qualified',
                'activation': 'optional_postcore_only_after_complete_source_selection',
                'render_gate_proposals': [
                    {'id': f'{row["id"]}_owner_{o["id"]}', 'kind': 'component',
                     'owner': o['id'], 'requirement_en': o['visible_property_en']}
                    for o in owners] + [
                    {'id': f'{row["id"]}_relation_{i+1}', 'kind': 'relation', **r}
                    for i, r in enumerate(relations)],
                'pixel_rule': 'all selected requirements visible together; partial_is_fail; UNOBSERVABLE_NOT_PASS'}
        cards.append(card)
        if row['mode'] in {'still', 'proxy', 'versioned'}:
            # Deliberately not the corpus wire schema. Negatives and claims do not enter positive text.
            drafts.append({'draft_id': f'draft_{row["id"]}', 'semantic_card_id': row['id'],
                           'runtime_importable': False, 'registration_status': 'NOT_REGISTERED',
                           'positive_components_en': [o['visible_property_en'] for o in owners],
                           'positive_scene_ko': row['positive_ko'],
                           'positive_relations_for_authoring': relations,
                           'bilingual_review': 'REQUIRED_before_import; do not machine-concatenate into final prose',
                           'owner_graph': {'owners': owners, 'relations': relations},
                           'planned_slots': card['planned_slots'],
                           'adoption_triage': 'reuse_refine_new_context_defer_after_full_source_review',
                           'prerequisites': ['independent requester meaning and frozen core',
                                             'complete source and intrinsic effect review',
                                             'existing owner and requested open-dimension check',
                                             'literal bilingual source and role review'],
                           'native_source_proof': None, 'retrieval_receipt': None,
                           'image': None, 'pixel_review': None, 'requester_acceptance': None})
    return cards, drafts


def corpus_audit(seed_rows):
    manifest_file = ASSETS / 'photo_candidate_corpus_manifest.json'
    manifest = json.loads(manifest_file.read_text())
    candidates, bindings, owner_files, hashes = {}, {}, {}, {}
    for module in manifest['modules']:
        path = ASSETS / module['file']
        raw = path.read_bytes()
        hashes[module['file']] = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw)
        for key, record in data.get('candidates', {}).items():
            if key in candidates:
                raise ValueError(f'duplicate candidate {key}')
            candidates[key] = record
            owner_files[key] = module['file']
        for key, record in data.get('slot_bindings', {}).items():
            if key in bindings:
                raise ValueError(f'duplicate binding {key}')
            bindings[key] = record
    # Only positive primary fields: exclude embedding_text, tag commentary, bundles and confusion negatives.
    texts = {}
    for cid, record in candidates.items():
        content = record.get('content', {})
        texts[cid] = '\n'.join([str(content.get(k, '')) for k in ('en', 'ko')] +
                               [str(x) for x in content.get('aliases', [])]).casefold()
    hit_rows = []
    for seed in seed_rows:
        variants = [v.strip() for v in seed['en'].split(' / ')] + [seed['ko']]
        patterns = [re.compile(r'(?<![a-z0-9])' + re.escape(v.casefold()) + r'(?![a-z0-9])')
                    for v in variants if len(v) >= 2]
        matches = [cid for cid, text in texts.items() if any(p.search(text) for p in patterns)]
        hit_rows.append({'seed_id': seed['id'], 'term_en': seed['en'], 'term_ko': seed['ko'],
                         'tested_variants': [v for v in variants if len(v) >= 2], 'match_count': len(matches),
                         'candidate_ids': matches, 'meaning': 'lexical triage only, not relevance or retrieval exposure'})
    exact_ids = [cid for cid, r in candidates.items()
                 if 'punk_atompunk' in r.get('content', {}).get('tags', []) or
                 any(p.get('source') == 'bundle:atompunk' for p in r.get('provenance', []))]
    neighbor_ids = []
    for group in [('raypunk',), ('mid-century', 'midcentury'), ('beehive',), ('pencil skirt',),
                  ('jumpsuit',), ('cassette futurism',), ('cyborg',), ('chrome',), ('bikini',)]:
        found = [cid for cid, text in texts.items() if any(term in text for term in group)]
        neighbor_ids.extend(found[:2])
    decisions = {r['candidate_id']: r for r in tsv('EXISTING-DECISIONS.tsv')}
    selected = list(dict.fromkeys(exact_ids + neighbor_ids + list(decisions)))
    snapshots = []
    for cid in selected:
        related = [b for b in bindings.values() if b.get('candidate_id') == cid]
        snapshots.append({'candidate_id': cid, 'owner_file': owner_files[cid],
                          'source_sha256': digest(candidates[cid]),
                          'binding_set_sha256': digest(related),
                          'selection_basis': 'exact_atompunk_family' if cid in exact_ids else 'lexical_neighbor_unqualified',
                          'full_source_record': candidates[cid], 'full_bindings': related,
                          'adoption_status': 'REVIEW_REQUIRED; lexical neighbor does not prove reusable semantics',
                          'authored_triage_proposal': decisions.get(cid)})
    snapshot = {'schema': 'atompunk-research-corpus-snapshot/v1', 'date': DATE,
                'manifest_sha256': hashlib.sha256(manifest_file.read_bytes()).hexdigest(),
                'module_sha256': hashes,
                'counts': {'modules': len(manifest['modules']), 'candidates': len(candidates),
                           'bindings': len(bindings), 'exact_atompunk_records': len(exact_ids)},
                'record_kinds': dict(Counter(r['record_kind'] for r in candidates.values())),
                'primary_field_scan': ['content.en', 'content.ko', 'content.aliases'],
                'lexical_method': 'original slash-delimited English phrases and Korean label; minimum 2 characters; ASCII letter/digit boundary; exact spacing; no morphology or semantic expansion',
                'exclusions': ['embedding_text', 'keywords', 'tags', 'confusion_boundaries', 'provenance'],
                'exact_atompunk_ids': exact_ids,
                'zero_match_is_not_semantic_absence': True, 'retrieval_execution': 'NOT_RUN'}
    prior_path = HERE / 'CORPUS-SNAPSHOT.json'
    if prior_path.exists():
        previous = json.loads(prior_path.read_text())
        if previous['module_sha256'] != hashes or previous['manifest_sha256'] != snapshot['manifest_sha256']:
            raise ValueError('Corpus drift since first research audit; preserve it and capture a successor snapshot before rebuilding.')
    save('CORPUS-SNAPSHOT.json', snapshot)
    save('LEXICAL-AUDIT.json', {'metadata': snapshot, 'rows': hit_rows})
    save('existing-source-mapping.json', {'metadata': snapshot, 'records': snapshots})
    return snapshot, hit_rows


def main():
    seed_rows = seeds()
    cards, drafts = parse_cards()
    sources = tsv('SOURCES.tsv')
    catalog = json.loads((ASSETS / 'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    metadata = {'schema': 'atompunk-research/v1', 'date': DATE, 'timezone': 'Asia/Seoul',
                'reference_conversation_id': CONVERSATION,
                'runtime_importable': False, 'operating_assets_written': False,
                'counts': {'seeds': len(seed_rows), 'cards': len(cards), 'drafts': len(drafts),
                           'source_entries': len(sources), 'slots_in_catalog': len(catalog)},
                'source_entry_count_includes_access_limits': True,
                'modes': dict(Counter(c['mode'] for c in cards)),
                'priorities': dict(Counter(c['priority'] for c in cards)),
                'evidence_boundary': 'research integrity only; no retrieval, native source, image, pixel, or user qualification'}
    routes = []
    for seed in seed_rows:
        linked = [c for c in cards if seed['id'] in c['seed_ids']]
        if not linked:
            raise ValueError(f'Unrouted seed: {seed}')
        routes.append({**seed, 'card_ids': [c['id'] for c in linked],
                       'route_modes': sorted({c['mode'] for c in linked}),
                       'seed_is_not_full_card_equivalence': True,
                       'selection_note': 'select the actual described branch; grouped original labels are not synonyms'})
    save('keyword-routes.json', {'metadata': metadata, 'routes': routes})
    save('semantic-cards.json', {'metadata': metadata, 'cards': cards})
    save('candidate-drafts.json', {'metadata': metadata, 'drafts': drafts})
    save('sources.json', {'reviewed_on': DATE, 'sources': sources})
    save('bilingual-realizations.json', {
        'schema': 'atompunk-research-realizations/v1', 'runtime_importable': False,
        'execution_status': 'NOT_RUN', 'counting_note': 'These are scene combinations of the 88 drafts, not additional operating candidates.',
        'realizations': tsv('REALIZATIONS.tsv')})
    save('evaluation-cases.json', {
        'schema': 'atompunk-research-evaluation/v1', 'execution_status': 'NOT_RUN',
        'cohort_role': 'development_and_controls_not_independent_holdout',
        'cases': tsv('EVALUATION-CASES.tsv')})
    save('catalog-snapshot.json', {slot: catalog[slot] for slot in sorted({s for c in cards for s in c['planned_slots']})})
    snapshot, hits = corpus_audit(seed_rows)
    lines = ['# 원 대화 191개 항목의 처리 경로', '',
             '원문의 표 행을 보존했다. 한 행의 복수 명칭은 동의어 선언이 아니며 카드도 전체 의미의 동치가 아니다.', '',
             '| ID | 원문 항목 | 처리 | 카드 | 반영 시 주의 |', '|---|---|---|---|---|']
    for r in routes:
        limits = ' / '.join(c['claim_limit_ko'] for c in cards if c['id'] in r['card_ids'])
        lines.append(f'| {r["id"]} | {r["en"]} — {r["ko"]} | {", ".join(r["route_modes"])} | {", ".join(r["card_ids"])} | {limits} |')
    (HERE / 'KEYWORD-ATLAS.md').write_text('\n'.join(lines) + '\n')
    lines = ['# 상세 시각 의미 카드', '',
             '가시 실현은 연구자가 저술한 제안이다. 출처는 용어 또는 인접 맥락만 뒷받침하며 전체 장면의 고증·품질을 승인하지 않는다.', '',
             '표의 성분과 방향 관계는 선택된 분기 전체의 검토 항목이다. 일부가 가려지면 부분 또는 관찰 불가이며 전체 통과가 아니다.', '']
    source_map = {s['id']: s for s in sources}
    for c in cards:
        lines += [f'## {c["id"]} — {", ".join(c["seed_ids"])}', '',
                  f'{c["mode"]} / {c["priority"]} / 역할 제안: {", ".join(c["planned_slots"])}', '',
                  c['positive_proposal_ko'], '',
                  '성분: ' + '; '.join(f'{o["id"]} = {o["visible_property_en"]}' for o in c['owners']), '',
                  '관계: ' + '; '.join(f'{r["subject"]} → {r["predicate"]} → {r["object"]}' for r in c['relations']), '',
                  '혼동 경계: ' + '; '.join(c['confusion_boundaries_ko']), '',
                  '주장 한계: ' + c['claim_limit_ko'], '',
                  '근거: ' + ', '.join(f'[{s}]({source_map[s]["url"]}) ({source_map[s]["review_scope"]})' for s in c['source_ids']), '']
    (HERE / 'VISUAL-CARDS.md').write_text('\n'.join(lines) + '\n')
    save('PACKAGE-SUMMARY.json', {**metadata, 'corpus_counts': snapshot['counts'],
                                'lexical_zero_match_seeds': sum(r['match_count'] == 0 for r in hits)})
    print(json.dumps({'research_counts': metadata['counts'], 'modes': metadata['modes'],
                      'corpus_counts': snapshot['counts']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
