"""Expand explicitly authored per-record decisions, with no semantic inference."""
import json
from pathlib import Path


def save(name, packet_name, decisions, corrections, *, kind_overrides=None):
    here = Path(__file__).resolve().parent
    packet = json.loads((here.parent / 'packets' / packet_name).read_text())
    catalog = json.loads((here.parent / 'CATALOG.json').read_text())
    rows = []
    for ordinal, status, meaning, properties, boundary in decisions:
        cid = packet['ids'][ordinal - packet['start']]
        record = packet['records'][cid]
        english = record['content']['en']
        for change in corrections.get(ordinal, []):
            if change['pointer'] == '/content/en':
                if english != change['before']:
                    raise ValueError('authored English correction no longer matches source')
                english = change['after']
        selected, facts = {}, []
        for declaration in properties.split(';') if properties else []:
            tag, dimension, target, prop, rationale = declaration.split('|')
            fact = {'pointer': '/content/en', 'quote': english,
                'dimension': dimension, 'target': target, 'property': prop}
            if tag not in selected:
                selected[tag] = {'slot_id': tag, 'semantic_role': catalog[tag]['semantic_role'],
                    'scope': 'whole_record', 'realization_ids': ['base'], 'rationale': rationale,
                    'evidence': []}
            selected[tag]['evidence'].append(fact)
            facts.append({**fact, 'realization_id': 'base'})
        rows.append({'candidate_id': cid, 'meaning_summary': meaning,
            'recommended_kind': (kind_overrides or {}).get(ordinal, 'visual_option'),
            'corrections': corrections.get(ordinal, []),
            'roles': list(selected.values()), 'facts': facts, 'rejected_boundaries': [boundary],
            'uncertainties': [], 'status': status, 'all_roles_considered': True})
    assert len(rows) == len({row['candidate_id'] for row in rows})
    (here / name).write_text(json.dumps({'decisions': rows}, ensure_ascii=False, indent=2) + '\n')
