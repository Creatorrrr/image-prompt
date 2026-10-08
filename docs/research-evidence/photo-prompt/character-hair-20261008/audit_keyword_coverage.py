"""Read authored sources and write a research-only lexical crosswalk.

This is not the runtime matcher, an index builder, or a semantic absence test.
Run from anywhere. All outputs stay beside this script.
"""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import re
import unicodedata
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'


def normalize(value):
    return re.sub(r'[\W_]+', ' ', unicodedata.normalize('NFKC', str(value)).casefold()).strip()


def strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [s for item in value for s in strings(item)]
    return []


def source_rows():
    tags = json.loads((ASSETS / 'photo_prompt_tags.json').read_text())
    manifest = json.loads((ASSETS / 'photo_prompt_source_manifest.json').read_text())
    inventory = [('photo_prompt_tags.json', 'candidate', tags),
                 ('photo_prompt_visual_obligations.json', 'visual_profile',
                  json.loads((ASSETS / 'photo_prompt_visual_obligations.json').read_text()))]
    for row in manifest['sources']:
        path = ASSETS / row['file']
        if path.is_file():
            inventory.append((row['file'], row['kind'], json.loads(path.read_text())))
    candidates, profiles = [], []
    hashes = []
    for filename, kind, data in inventory:
        hashes.append({'file': filename, 'kind': kind,
                       'sha256': hashlib.sha256((ASSETS / filename).read_bytes()).hexdigest()})
        if kind == 'candidate':
            for slot, rows in data.get('slots', {}).items():
                for row in rows:
                    candidates.append({'source': filename, 'slot': slot, 'row': row})
        else:
            profiles.extend({'source': filename, 'row': row} for row in data.get('profiles', []))
    return candidates, profiles, hashes, manifest


def policy(term):
    n = int(term['id'][1:])
    category = term['category']
    if n in {57, 58, 59, 118, 119, 120, 121, 122, 123, 124, 125, 126,
             156, 162, 167, 168, 169, 170, 171, 172, 218, 220,
             244, 245, 246, 248, 249, 250, 251, 252, 253, 254, 255, 257,
             264, 265, 266, 267, 268, 274, 408, 409, 410, 411, 412, 413, 414, 415}:
        return 'process_or_installation_plus_visible_result', 'Separate process/installation meaning from visible result; a still photograph does not prove procedure, material origin, or product chemistry.'
    if n == 325:
        return 'clinical_term_with_appearance_projection', 'Retain clinical definition in research context; a white patch alone establishes appearance, not diagnosis or cause.'
    if n == 432:
        return 'nonvisual_context_only', 'Interest/topic has no mandatory hairstyle signature; do not create appearance obligations or infer actual interests.'
    if n in {421, 423, 424, 425, 426, 427, 428, 430, 431}:
        return 'broad_style_or_editorial_context', 'Use an optional realization family, not an exact universal haircut recipe, identity, behavior, or fixed intensity.'
    if n in {287} or 288 <= n <= 324 or 326 <= n <= 356:
        return 'color_variant_or_layout_family', 'Specify hue, relative lightness, saturation, region and boundary; names are not universal brand shade numbers or fixed RGB values.'
    if n in {433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 447, 448, 449, 450, 451, 452, 453, 454, 357}:
        return 'platform_or_fantasy_scope', 'Keep platform-specific shape/count/material/action/effect meanings separate; do not use personality or anatomical inference as evidence.'
    if category == '18' or n == 417:
        return 'accessory_attachment_relation', 'Bind the accessory to its hair carrier and visible attachment; an object near hair is not proof of wearing or fastening.'
    if category == '17':
        return 'localized_surface_state', 'Bind state to the affected region; stains, gloss or disorder do not prove event, hygiene, substance or cause without supplied context.'
    if category == '12':
        return 'hair_owned_color_parameter', 'Generic color words need a hair owner and region; they cannot change lighting, global grading, clothes or skin.'
    if category == '01':
        return 'regional_measurement_or_component', 'Bind owner, body landmark and view; do not impose whole-head length or infer hidden endpoints.'
    return 'observable_shape_or_topology', 'Decompose into local structure and directed relations; exact names need sense/context review and candidate hits stay advisory.'


def main():
    terms = list(csv.DictReader((OUT / 'reference/keyword-inventory.tsv').open(), delimiter='\t'))
    assert len(terms) == 454 and [r['id'] for r in terms] == [f'H{i:03d}' for i in range(1, 455)]
    candidates, profiles, hashes, manifest = source_rows()
    exact = collections.defaultdict(list)
    mentions = []
    for record in candidates:
        row = record['row']
        labels = strings(row.get('ko')) + strings(row.get('en')) + strings(row.get('aliases')) + strings(row.get('paraphrases'))
        ref = {'kind': 'candidate', 'id': row['id'], 'slot': record['slot'], 'source': record['source'],
               'has_concept_units': bool(row.get('concept_units')),
               'has_relations': bool(row.get('relations')), 'has_effects': bool(row.get('affected_properties'))}
        for label in set(map(normalize, labels)):
            if label:
                exact[label].append(ref)
        positive = ' '.join(labels + strings(row.get('keywords')) + strings(row.get('concept_units')) + strings(row.get('embedding_text')))
        mentions.append((normalize(positive), ref))
    for record in profiles:
        row = record['row']
        ref = {'kind': 'profile', 'id': row['id'], 'category': row.get('category'), 'source': record['source']}
        for label in set(map(normalize, strings(row.get('activation', {}).get('exact_terms')))):
            if label:
                exact[label].append(ref)
        sem = row.get('semantics', {})
        positive = ' '.join(strings(sem.get('definition')) + strings(sem.get('paraphrase_examples')) + strings(row.get('concept_candidate', {}).get('concept_terms')))
        mentions.append((normalize(positive), ref))
    output = []
    for term in terms:
        variants = {normalize(term['ko']), normalize(term['en'])}
        variants.update(normalize(s) for s in term['en'].split(' / '))
        exact_hits = { (ref['kind'], ref.get('slot', ''), ref['id']): ref
                       for variant in variants for ref in exact.get(variant, []) }
        mention_hits = {}
        for text, ref in mentions:
            if any(v and f' {v} ' in f' {text} ' for v in variants):
                mention_hits[(ref['kind'], ref.get('slot', ''), ref['id'])] = ref
        p, note = policy(term)
        hair_hits = [ref for ref in exact_hits.values() if ref.get('slot') in {'hair_style', 'hair_color', 'wearable_accessory'} or ref['kind'] == 'profile']
        output.append({**term, 'proposed_disposition': p, 'planning_note': note,
                       'normalized_forms': sorted(variants), 'whole_term_surface_matches': list(exact_hits.values()),
                       'hair_or_accessory_or_profile_surface_matches': hair_hits,
                       'bounded_positive_mention_count': len(mention_hits),
                       'bounded_positive_mentions_sample': list(mention_hits.values())[:12],
                       'coverage_verdict': 'surface_found_requires_semantic_review' if exact_hits else 'no_whole_term_surface_match_not_semantic_absence',
                       'runtime_retrieval_executed': False, 'definition_verified_by_this_audit': False})
    duplicates = []
    terms_by_en = collections.defaultdict(list)
    for term in terms:
        terms_by_en[normalize(term['en'])].append(term['id'])
    for surface, ids in terms_by_en.items():
        if len(ids) > 1:
            duplicates.append({'surface': surface, 'glossary_ids': ids, 'status': 'review_owner_and_namespace_before_aliasing'})
    hair_candidates = [r for r in candidates if r['slot'] in {'hair_style', 'hair_color'}]
    dedicated = [r for r in profiles if str(r['row'].get('category', '')).startswith('hair_')]
    summary = {'contract_version': 'character-hair-current-source-audit/v1',
               'source_scope': 'current working checkout, including pre-existing uncommitted sources; raw authored rows, not compiled runtime/index validation',
               'glossary_terms': len(terms), 'registered_extension_count': len(manifest['sources']),
               'candidate_rows': len(candidates), 'unique_candidate_slot_ids': len({(r['slot'], r['row']['id']) for r in candidates}),
               'profile_rows': len(profiles), 'unique_profile_ids': len({r['row']['id'] for r in profiles}),
               'hair_style_rows': sum(r['slot'] == 'hair_style' for r in candidates),
               'hair_color_rows': sum(r['slot'] == 'hair_color' for r in candidates),
               'base_dedicated_hair_profiles': [r['row']['id'] for r in dedicated],
               'hair_candidate_structure_counts': {field: sum(bool(r['row'].get(field)) for r in hair_candidates) for field in ('concept_units', 'relations', 'affected_dimensions', 'affected_properties')},
               'whole_term_surface_found': sum(bool(r['whole_term_surface_matches']) for r in output),
               'no_whole_term_surface_match': sum(not r['whole_term_surface_matches'] for r in output),
               'dispositions': dict(collections.Counter(r['proposed_disposition'] for r in output)),
               'aliases_with_multiple_glossary_ids': duplicates,
               'limitations': ['No BM25F or embedding ranking executed.', 'No hard activation, candidate selection, generated index integrity or native pixels verified.', 'A text match can be the wrong owner/sense or an alternative; no match can still have a structural equivalent.', 'Color/process/style policy categories are planning proposals, not ontology truth or primary-source verification.'],
               'source_hashes': hashes}
    (OUT / 'CURRENT-DATA-AUDIT.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'KEYWORD-CROSSWALK.json').write_text(json.dumps({'contract_version': 'character-hair-keyword-crosswalk/v1', 'status': 'research_draft_not_runtime', 'rows': output}, ensure_ascii=False, indent=2) + '\n')
    with (OUT / 'KEYWORD-CROSSWALK.tsv').open('w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['id', 'category', 'ko', 'en', 'disposition', 'whole_surface_count', 'bounded_mentions', 'candidate_ids', 'profile_ids'])
        for row in output:
            matches = row['whole_term_surface_matches']
            writer.writerow([row['id'], row['category'], row['ko'], row['en'], row['proposed_disposition'], len(matches), row['bounded_positive_mention_count'], ','.join(f"{r['slot']}:{r['id']}" for r in matches if r['kind'] == 'candidate'), ','.join(r['id'] for r in matches if r['kind'] == 'profile')])
    print(json.dumps({k: v for k, v in summary.items() if k not in {'source_hashes', 'limitations'}}, ensure_ascii=False))


if __name__ == '__main__':
    main()
