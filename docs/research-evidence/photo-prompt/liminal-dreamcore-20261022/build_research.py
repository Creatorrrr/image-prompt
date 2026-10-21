"""Build research artifacts only. This is not an operating corpus importer."""
from pathlib import Path
import csv
import json
import hashlib
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'


def read_tsv(name):
    with (HERE / name).open() as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_json(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    seeds = {int(r['id']): r for r in read_tsv('SEEDS.tsv')}
    sources = read_tsv('SOURCES.tsv')
    specs = read_tsv('SEMANTIC-SPEC.tsv')
    catalog = json.loads((ASSETS / 'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    cards, drafts = [], []
    for row in specs:
        n = int(row['id'])
        card_id = f'L{n:03}'
        owners = [] if row['components'] == '-' else [
            {'id': key, 'visible_property_en': value}
            for key, value in (s.split('=', 1) for s in row['components'].split(';'))
        ]
        relations = [] if row['relations'] == '-' else [
            dict(zip(('subject', 'predicate', 'object'), s.split('|')))
            for s in row['relations'].split(';')
        ]
        slots = row['slots'].split(',')
        eligible = row['mode'] in {'still', 'proxy', 'versioned'}
        gates = [
            {'id': f'{card_id}_owner_{o["id"]}', 'kind': 'visible_component',
             'owner': o['id'], 'requirement_en': o['visible_property_en'], 'scale': 'native'}
            for o in owners
        ] + [
            {'id': f'{card_id}_relation_{i+1}', 'kind': 'visible_relation',
             **relation, 'scale': 'native'}
            for i, relation in enumerate(relations)
        ]
        cards.append({
            'id': card_id, 'seed_id': n, 'term_ko': seeds[n]['ko'], 'term_en': seeds[n]['en'],
            'evidence_mode': row['mode'], 'priority': row['priority'],
            'owners': owners, 'relations': relations, 'planned_slots': slots,
            'confusion_boundaries_ko': row['confusions'].split(';'),
            'claim_limit_ko': row['claim_limit_ko'], 'source_ids': row['sources'].split(','),
            'source_claim_scope': 'term or adjacent context only; the scene realization is authored research',
            'realization_authorship': 'agent_authored_creative_proposal',
            'activation': 'no label-triggered obligations; explicit complete selection only',
            'still_candidate_draft': f'draft_{card_id}' if eligible else None,
            'render_gate_proposals': gates,
            'review_rule': 'all required owners and relations visible together; partial_is_fail; UNOBSERVABLE_NOT_PASS',
            'unobserved_claims': 'Not accepted as pixel facts; retained only in research context',
            'evidence_status': 'research_reviewed_not_native_qualified',
        })
        if eligible:
            # Only locally described visible properties enter the draft projection.
            # Term names, limits, source essays, and negatives stay outside positive text.
            phrase = '. '.join(o['visible_property_en'][0].upper() + o['visible_property_en'][1:] for o in owners) + '.'
            relation_prose = '; '.join(f'{r["subject"]} {r["predicate"].replace("_", " ")} {r["object"]}' for r in relations)
            drafts.append({
                'draft_id': f'draft_{card_id}', 'semantic_card_id': card_id,
                'registration_status': 'not_in_operating_manifest', 'runtime_importable': False,
                'positive_projection_en': phrase,
                'relation_projection_for_authoring': relation_prose,
                'translation_ko_status': 'term and limits authored; full positive prose translation required before import',
                'proposed_slot_views': [
                    {'slot': slot, 'allowed_dimensions_from_current_catalog': catalog[slot]['dimensions'],
                     'review_status': 'source_and_role_meaning_review_required'} for slot in slots
                ],
                'owner_graph': {'owners': owners, 'relations': relations},
                'planning_constraints': {
                    'independent_core_required': True, 'whole_source_effect_inventory_required': True,
                    'existing_owner_selection_required_if_mutating_existing_owner': True,
                    'role_tag_is_not_qualification': True,
                    'claim_limits_stay_outside_positive_projection': True,
                    'all_selected_variant_components_required': True,
                    'no_generated_owner_or_scope_permission': True,
                },
                'review_context_card_id': card_id,
                'native_evidence': None, 'embedding': None, 'retrieval_receipt': None,
                'pixel_review': None, 'requester_acceptance': None,
            })
    metadata = {
        'schema': 'liminal-research-package/v1', 'user_date': '2026-10-22',
        'reference_conversation_id': '6acda685-7d7c-83e8-874d-db3910ed868e',
        'runtime_importable': False,
        'counts': {'seeds': len(seeds), 'sources': len(sources), 'cards': len(cards), 'drafts': len(drafts),
                   'bilingual_realizations': len(read_tsv('REALIZATIONS.tsv')),
                   'evaluation_cases': len(read_tsv('EVALUATION-CASES.tsv')),
                   'existing_id_mappings': len(read_tsv('EXISTING-MAPPING.tsv'))},
        'evidence_modes': dict(Counter(c['evidence_mode'] for c in cards)),
        'priorities': dict(Counter(c['priority'] for c in cards)),
    }
    write_json('semantic-cards.json', {'metadata': metadata, 'cards': cards})
    write_json('candidate-drafts.json', {'metadata': metadata, 'drafts': drafts})
    write_json('sources.json', {'reviewed_on': '2026-10-22', 'sources': sources})
    realization_rows = read_tsv('REALIZATIONS.tsv')
    write_json('bilingual-realizations.json', {
        'schema': 'liminal-research-bilingual-realizations/v1', 'runtime_importable': False,
        'status': 'authored_proposals_not_native_qualified',
        'meaning_of_seed_ids': 'thematic source and comparison routes; not simultaneous adoption of every seed meaning',
        'realizations': realization_rows,
    })
    write_json('evaluation-cases.json', {
        'schema': 'liminal-research-evaluation-plan/v1', 'execution_status': 'NOT_RUN',
        'cohort_role': 'development and controls; not an independent holdout',
        'cases': read_tsv('EVALUATION-CASES.tsv'),
    })
    corpus, bindings, module_owner = {}, {}, {}
    for module in json.loads((ASSETS / 'photo_candidate_corpus_manifest.json').read_text())['modules']:
        data = json.loads((ASSETS / module['file']).read_text())
        corpus.update(data.get('candidates', {}))
        bindings.update(data.get('slot_bindings', {}))
        module_owner.update({cid: module['file'] for cid in data.get('candidates', {})})
    mapping_rows = []
    for row in read_tsv('EXISTING-MAPPING.tsv'):
        cid = row['candidate_id']
        record = corpus[cid]
        encoded = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        mapping_rows.append({**row, 'module': module_owner[cid],
                             'review_status': 'integration_triage_not_native_qualification',
                             'source_sha256': hashlib.sha256(encoded).hexdigest(),
                             'full_source_record': record,
                             'full_bindings': [b for b in bindings.values() if b['candidate_id'] == cid]})
    write_json('existing-source-mapping.json', {
        'schema': 'liminal-research-existing-map/v1', 'source_cid_count': len(corpus),
        'record_kinds': dict(Counter(r['record_kind'] for r in corpus.values())),
        'rows': mapping_rows,
    })
    lines = ['# 200개 키워드의 시각 의미와 반영 경로', '',
             '이 표의 실현은 연구자가 작성한 제안이다. 출처는 용어·인접 맥락의 근거이며 장면의 필수성이나 효과를 보증하지 않는다.', '',
             '`still`은 현재 형상, `proxy`는 외형 단서만, `versioned`는 출처 판본 한정, `advisory`는 해석·서사층, `sequence`는 연속 증거, `audio`는 음향을 뜻한다.', '',
             '| ID / 키워드 | 모드·우선순위 | 가시 소유자와 관계 / 반영 경로 | 혼동 경계 | 주장 한계 | 근거 |',
             '|---|---|---|---|---|---|']
    for c in cards:
        visual = '; '.join(f'{o["id"]}: {o["visible_property_en"]}' for o in c['owners'])
        visual += ' / ' + '; '.join(f'{r["subject"]} → {r["predicate"]} → {r["object"]}' for r in c['relations']) if c['relations'] else ''
        if not c['owners']:
            visual = '사진 하드 의무로 등록하지 않음; ' + ', '.join(c['planned_slots']) + '의 문맥 또는 별도 매체 연구'
        source_links = ', '.join(f'[{sid}]({next(s["url"] for s in sources if s["id"]==sid)})' for sid in c['source_ids'])
        lines.append(f'| {c["id"]} {c["term_ko"]}<br>{c["term_en"]} | {c["evidence_mode"]} / {c["priority"]} | {visual} | {"; ".join(c["confusion_boundaries_ko"])} | {c["claim_limit_ko"]} | {source_links} |')
    (HERE / 'KEYWORD-ATLAS.md').write_text('\n'.join(lines) + '\n')
    write_json('PACKAGE.json', metadata)
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
