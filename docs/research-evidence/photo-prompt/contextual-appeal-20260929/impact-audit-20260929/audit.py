#!/usr/bin/env python3
"""Read-only attribution and admission replay of seven retained generation arms.

No generation, query embedding, live network, or skill/data mutation is performed.
Only this audit directory receives new evidence files.
"""
from __future__ import annotations

import collections
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as g
import photo_contextual_appeal as ca


def read(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def inventory_ids(value):
    return {str(row[key]).split(':')[-1]
            for row in walk(value) for key in ('id', 'entry_id', 'source_candidate_id')
            if isinstance(row.get(key), str)}


DATA = g.load_json(ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json')
DATA[g.QUALITY_LAYERS_DATA_KEY] = g.load_json(ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json')
POLICY = g.candidate_pack_hybrid_policy(DATA)['adult_appeal']
EXT = read(ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_contextual_appeal_extension.json')
NEW = {row['id'] for rows in EXT['slots'].values() for row in rows}
ENRICHED = {key for rows in EXT['existing_slot_context_extensions'].values() for key in rows}
IDENTITY_SLOTS = {'subject', 'appearance_type', 'age', 'species', 'species_morphology', 'face', 'body_type', 'person_origin'}


def admission(pack, axis):
    core = pack['authorial_core']
    snapshot = pack['creative_controls']
    contract = pack['adult_appeal']
    lock = core['intent_lock']
    constraints = {'subject_category': snapshot['context']['subject_category'], 'preset_domains': [],
                   'adult_allowed': contract['eligibility']['status'] == 'eligible',
                   'intent_constraints': g.authorial_core_generation_constraints(core)}
    allowed = set(contract['dimension_scope']['axis_allowed_dimensions'][axis])
    exclusions = [g.candidate_pack_v5_relevance_tokens(v) for v in core.get('user_exclusions', [])]
    accepted = []
    blocked = []
    for slot, entries in DATA['slots'].items():
        for entry in entries:
            key = f"{slot}:{entry['id']}"
            dims = sorted(set(entry.get('affected_dimensions', [])) | set(POLICY.get('entry_dimensions', {}).get(key, [])))
            dims = dims or g.photo_candidate_semantics.slot_dimensions(slot, DATA.get('candidate_semantic_policy'))
            reasons = []
            if slot in IDENTITY_SLOTS:
                reasons.append('identity_slot')
            if reason := g.slot_block_reason(DATA, slot, constraints):
                reasons.append('slot_guard:' + str(reason))
            if not dims or not set(dims) <= allowed:
                reasons.append('outside_dimensions:' + ','.join(sorted(set(dims) - allowed)))
            if not g.property_effects_allowed(lock, dims, entry.get('affected_properties', [])):
                reasons.append('property_lock')
            if reason := g.entry_block_reason(entry, slot, constraints):
                reasons.append('entry_guard:' + str(reason))
            if not g.compatible_with_facet_guards(entry, {}, {}):
                reasons.append('facet_guard')
            fields = g.semantic_bm25f_fields_for_entry(entry, slot, kind='slot')
            texts = [str(v) for values in fields.values() for v in values]
            tokens = g.candidate_pack_v5_relevance_tokens(' '.join(texts))
            if any(group and group <= tokens for group in exclusions):
                reasons.append('user_exclusion')
            if reasons:
                if entry['id'] in NEW:
                    blocked.append({'id': entry['id'], 'slot': slot, 'reasons': reasons})
            else:
                accepted.append({'source_candidate_id': 'slot:' + key, 'entry_id': entry['id'],
                                 'slot': slot, 'search_fields': fields, 'visual_text': texts,
                                 'expression_scope': entry.get('expression_scope') or ca.expression_scope(slot)})
    return accepted, blocked


def main():
    report = {'method': 'Seven saved arms; exact prompt diff, candidate provenance, current admission replay. No new image calls or production packs.',
              'scope_limits': ['No old/new corpus controlled image comparison exists.',
                               'Adoption proves prompt provenance, not aesthetic improvement.',
                               'Mechanical admission does not prove scene applicability.',
                               'Blocked outputs have no pixels and are not aesthetic failures.'], 'arms': {}}
    dirs = [('research-integration-20260929', ['craft', 'sensory', 'mirror']),
            ('integrated-original-four-3-3-20260929-151603', ['water', 'moon', 'convenience', 'confession'])]
    for run, arms in dirs:
        for arm in arms:
            directory = ROOT / 'artifacts/photo-prompt-runs' / run / arm
            pack = read(directory / 'candidate_pack.json')
            pack = pack[0] if isinstance(pack, list) else pack
            core = read(directory / 'authorial_core.json')
            composed = read(directory / 'composed_prompt.json')
            chosen = composed['chosen_candidate_ids']
            chosen_entries = {key.split(':')[-1] for key in chosen}
            exposed = inventory_ids(pack)
            queries = ca.queries(pack['authorial_core'], pack['creative_controls']['definitions'],
                                 {a: row['requested_intensity'] for a, row in pack['adult_appeal']['axes'].items()},
                                 g.authorial_core_retrieval_text)
            query_matches = g.canonical_json_sha256(queries) == pack['adult_appeal']['contextual_retrieval']['query_sha256']
            assert query_matches, arm
            row = {'run': run, 'artifact_directory': str(directory.relative_to(ROOT)),
                   'input_hashes': {name: sha(directory / name) for name in ['authorial_core.json', 'candidate_pack.json', 'composed_prompt.json']},
                   'new_exposed_ids': sorted(exposed & NEW), 'enriched_exposed_ids': sorted(exposed & ENRICHED),
                   'chosen_candidate_ids': chosen, 'selected_new_ids': sorted(chosen_entries & NEW),
                   'selected_enriched_ids': sorted(chosen_entries & ENRICHED),
                   'baseline_equals_final': core['baseline_prompt_en'] == composed['prompt_en'],
                   'prompt_diff': list(difflib.unified_diff(core['baseline_prompt_en'].split('. '), composed['prompt_en'].split('. '),
                                                          fromfile='baseline', tofile='final', lineterm='')),
                   'candidate_interpretations': composed.get('candidate_interpretations'),
                   'locked_dimensions': core['intent_lock']['locked_dimensions'],
                   'semantic_anchors': core['intent_lock']['semantic_anchors'],
                   'contextual_review': composed.get('adult_appeal_brief', {}).get('contextual_review'),
                   'contextual_comparison': composed.get('adult_appeal_brief', {}).get('contextual_comparison'),
                   'reconstructed_query_hash_matches': query_matches,
                   'query_lengths_words': {a: {lane: len(text.split()) for lane, text in lanes.items()} for a, lanes in queries.items()},
                   'alternative_query_contains_corset': any('corset' in lanes['alternatives'].lower() for lanes in queries.values()),
                   'axes': {}}
            for axis in pack['adult_appeal']['axes']:
                accepted, blocked = admission(pack, axis)
                trace = pack['adult_appeal']['contextual_retrieval']['axes'][axis]
                assert len(accepted) == trace['eligible_corpus_count'], (arm, axis, len(accepted), trace)
                new_accepted = [r for r in accepted if r['entry_id'] in NEW]
                row['axes'][axis] = {'total_admitted': len(accepted), 'new_admitted': len(new_accepted),
                                     'new_admitted_by_slot': dict(collections.Counter(r['slot'] for r in new_accepted)),
                                     'new_blocked': len(blocked),
                                     'new_block_reasons': dict(collections.Counter(r for b in blocked for r in b['reasons'])),
                                     'new_blocked_rows': blocked,
                                     'production_returned_ids': [r['entry_id'] for r in pack['adult_appeal']['axes'][axis]['candidate_inventory']],
                                     'production_trace': trace}
            report['arms'][arm] = row

    entries = [r for rows in EXT['slots'].values() for r in rows]
    enriched_rows = [r for rows in EXT['existing_slot_context_extensions'].values() for r in rows.values()]
    report['supply'] = {'new_candidates': len(NEW), 'enriched_existing_candidates': len(ENRICHED),
                        'new_by_slot': {slot: len(rows) for slot, rows in EXT['slots'].items()},
                        'new_without_aliases': sum(not r.get('aliases') for r in entries),
                        'new_without_paraphrases': sum(not r.get('paraphrases') for r in entries),
                        'new_single_concept_equal_to_english_label': sum(r.get('concept_units') == [r.get('en')] for r in entries),
                        'enriched_with_searchable_paraphrases': sum(bool(r.get('paraphrases')) for r in enriched_rows)}
    selected_entries = {key.split(':')[-1] for arm in report['arms'].values() for key in arm['chosen_candidate_ids']}
    head_files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', 'HEAD', 'skills/photo-prompt-image-generator/assets'], cwd=ROOT, text=True).splitlines()
    old = {}
    for path in head_files:
        if not path.endswith('.json') or 'extension' not in Path(path).name:
            continue
        doc = json.loads(subprocess.check_output(['git', 'show', 'HEAD:' + path], cwd=ROOT, text=True))
        for slot, rows in doc.get('slots', {}).items():
            for entry in rows:
                if isinstance(entry, dict) and entry.get('id') in selected_entries:
                    old[entry['id']] = {'path': path, 'slot': slot, 'entry': entry}
    current = {r['id']: (slot, r) for slot, rows in DATA['slots'].items() for r in rows if r['id'] in selected_entries}
    report['selected_source_comparison_to_head_before_integration'] = {}
    for entry_id, (slot, entry) in current.items():
        prior = old.get(entry_id)
        keys = ('en', 'ko', 'aliases', 'paraphrases', 'concept_units', 'relations', 'affected_dimensions', 'affected_properties', 'contextual_usage')
        report['selected_source_comparison_to_head_before_integration'][entry_id] = {
            'found_before_integration': bool(prior), 'source_file': prior and prior['path'],
            'changed_fields': [key for key in keys if prior and prior['entry'].get(key) != entry.get(key)],
            'new_context_ids': [r['id'] for r in entry.get('contextual_usage', {}).get('contexts', [])]}
    snapshot = read(ROOT / 'artifacts/photo-prompt-runs/integrated-original-four-3-3-20260929-151603/source_snapshot.json')
    report['snapshot_files_checked'] = len(snapshot['files'])
    report['source_drift'] = [r['path'] for r in snapshot['files'] if sha(ROOT / r['path']) != r['sha256']]
    assert not report['source_drift']
    (HERE / 'attribution-and-admission.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'supply': report['supply'], 'source_drift': report['source_drift'],
                      'arms': {a: {k: r[k] for k in ['new_exposed_ids', 'selected_new_ids', 'selected_enriched_ids', 'baseline_equals_final', 'alternative_query_contains_corset']} | {'new_admitted': r['axes']['sensual_editorial']['new_admitted']} for a, r in report['arms'].items()},
                      'selected_source_deltas': report['selected_source_comparison_to_head_before_integration']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
