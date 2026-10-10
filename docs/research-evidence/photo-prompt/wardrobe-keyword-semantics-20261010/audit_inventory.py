"""Read authored JSON only; this is lexical research, never runtime retrieval."""
from pathlib import Path
import collections
import csv
import hashlib
import json
import math
import re
import unicodedata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'

SLOTS = {
    '01': ['wardrobe_style', 'garment_detail', 'costume_style'],
    '02': ['wardrobe_style', 'garment_detail', 'prop'],
    '03': ['wardrobe_style', 'costume_style', 'garment_detail'],
    '04': ['wardrobe_style', 'garment_detail', 'silhouette_proportion'],
    '05': ['wardrobe_style', 'garment_detail'],
    '06': ['garment_detail', 'wardrobe_style'],
    '07': ['garment_detail', 'wardrobe_style'],
    '08': ['garment_detail', 'wardrobe_style', 'silhouette_proportion'],
    '09': ['garment_detail', 'wearable_accessory'],
    '10': ['surface_material', 'texture', 'garment_detail'],
    '11': ['garment_detail', 'wearable_accessory', 'surface_material', 'texture'],
    '12': ['color', 'color_grading', 'surface_material'],
    '13': ['garment_detail', 'wardrobe_style', 'wearable_accessory'],
    '14': ['footwear'],
    '15': ['wearable_accessory', 'prop'],
    '16': ['wearable_accessory', 'prop'],
    '17': ['aesthetic_trend', 'costume_style', 'wardrobe_style', 'genre', 'mood'],
    '18': ['location', 'space_condition', 'situation_context', 'capture_context'],
    '19': ['action', 'body_pose', 'hand_pose', 'garment_detail', 'expression', 'gaze_target'],
    '20': ['surface_material', 'texture', 'garment_detail'],
    '21': ['lighting', 'light_direction', 'light_shape', 'lens', 'composition', 'body_framing',
           'subject_framing', 'grain_profile', 'color', 'color_grading', 'capture_context'],
}
STOP = set('a an the of in on at to and or with from for by as is are this that same'.split())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(s):
    return ' '.join(re.findall(r'[a-z0-9가-힣]+', unicodedata.normalize('NFKC', str(s)).casefold()))


def strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [s for v in value for s in strings(v)]
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings(v)]
    return []


def tokens(value):
    return set(norm(value).split()) - STOP


def positive_text(entry, kind):
    if kind == 'candidate':
        fields = ['ko', 'en', 'aliases', 'keywords', 'paraphrases', 'concept_units', 'relations']
        return [s for f in fields for s in strings(entry.get(f))]
    semantics = entry.get('semantics') or {}
    result = strings(entry.get('activation', {}).get('exact_terms'))
    for k in ['definition', 'paraphrase_examples', 'visual_components']:
        result += strings(semantics.get(k))
    for component in entry.get('authored_components', {}).get('components', []):
        result += strings(component.get('match_terms')) + strings(component.get('evidence_terms'))
    return result


def main():
    seed = json.loads((HERE / 'inputs/wardrobe_keyword_catalog.json').read_text())
    manifest = json.loads((ASSETS / 'photo_prompt_source_manifest.json').read_text())
    rows = [{'file': 'photo_prompt_tags.json', 'kind': 'candidate', 'load_order': -1},
            {'file': 'photo_prompt_visual_obligations.json', 'kind': 'visual_profile', 'load_order': -1}]
    rows += sorted(manifest['sources'], key=lambda r: (r['kind'], r['load_order']))
    inventory, entries, payloads = [], [], {}
    for row in rows:
        path = ASSETS / row['file']
        if not path.exists():
            inventory.append({**row, 'present': False})
            continue
        data = json.loads(path.read_text())
        payloads[row['file']] = data
        inventory.append({**row, 'present': True, 'sha256': sha(path), 'bytes': path.stat().st_size,
                          'candidate_rows': sum(len(v) for v in data.get('slots', {}).values()),
                          'profile_rows': len(data.get('profiles', [])),
                          'bundle_rows': len(data.get('visual_semantics', []))})
        if row['kind'] == 'candidate':
            for slot, values in data.get('slots', {}).items():
                for index, entry in enumerate(values):
                    entries.append({'file': row['file'], 'kind': 'candidate', 'slot': slot,
                                    'id': entry['id'], 'pointer': f'/slots/{slot}/{index}', 'entry': entry})
        else:
            for index, entry in enumerate(data.get('profiles', [])):
                entries.append({'file': row['file'], 'kind': 'visual_profile', 'slot': None,
                                'id': entry['id'], 'pointer': f'/profiles/{index}', 'entry': entry})
    # Equivalent extension prose is considered only when it names an existing slot/ID.
    additions = collections.defaultdict(list)
    for filename, data in payloads.items():
        for slot, targets in (data.get('existing_slot_context_extensions') or {}).items():
            for target_id, content in targets.items():
                additions[(slot, target_id)] += strings(content.get('paraphrases'))
    for e in entries:
        labels = positive_text(e['entry'], e['kind'])
        if e['kind'] == 'candidate':
            labels += additions[(e['slot'], e['id'])]
        e['_labels'] = [norm(s) for s in labels if s]
        e['_tokens'] = tokens(' '.join(labels))
    df = collections.Counter(t for e in entries for t in e['_tokens'])
    count = len(entries)
    idf = {t: math.log(1 + (count + 1) / (n + 1)) for t, n in df.items()}

    def find(keyword, kind):
        q = tokens(keyword['keyword_en'])
        denominator = sum(idf.get(t, math.log(count + 1)) for t in q) or 1
        phrases = [norm(keyword['keyword_en']), norm(keyword['keyword_ko'])]
        eligible = SLOTS[keyword['category'][:2]]
        matches = []
        for e in entries:
            if e['kind'] != kind or (kind == 'candidate' and e['slot'] not in eligible):
                continue
            exact = [p for p in phrases if p and any(' ' + p + ' ' in ' ' + s + ' ' for s in e['_labels'])]
            overlap = q & e['_tokens']
            ratio = sum(idf.get(t, 1) for t in overlap) / denominator
            if not exact and (ratio < 0.5 or len(overlap) < min(2, len(q))):
                continue
            score = 5 * bool(exact) + ratio
            matches.append((score, e, exact, sorted(overlap)))
        matches.sort(key=lambda m: (-m[0], m[1]['file'], m[1]['id']))
        hits = []
        for score, e, exact, overlap in matches[:3]:
            hits.append({k: e[k] for k in ['file', 'kind', 'slot', 'id', 'pointer']})
            hits[-1].update({'match': 'positive_phrase_hit' if exact else 'token_overlap_only',
                             'matched_phrases': exact, 'matched_tokens': overlap,
                             'score': round(score, 4), 'semantics_reviewed': False,
                             'effects': e['entry'].get('affected_properties', []),
                             'row_sha256': hashlib.sha256(json.dumps(e['entry'], ensure_ascii=False,
                                                        sort_keys=True).encode()).hexdigest()})
        status = 'positive_phrase_hit' if any(h['match'] == 'positive_phrase_hit' for h in hits) else (
            'token_overlap_only' if hits else 'no_lexical_hit')
        return status, hits

    coverage = []
    for k in seed['keywords']:
        c_status, c_hits = find(k, 'candidate')
        p_status, p_hits = find(k, 'visual_profile')
        coverage.append({**k, 'suggested_existing_slots': SLOTS[k['category'][:2]],
                         'candidate_lexical_status': c_status, 'candidate_hits': c_hits,
                         'profile_lexical_status': p_status, 'profile_hits': p_hits,
                         'meaning_support': 'not_inferred', 'runtime_verified': False,
                         'native_pixels_verified': False})
    after = [{'file': r['file'], 'sha256': sha(ASSETS / r['file'])} for r in inventory if r['present']]
    assert all(a['sha256'] == next(r['sha256'] for r in inventory if r['file'] == a['file']) for a in after), 'Source drift during lexical audit'
    overview = {'scope': 'authored working checkout, registered extensions plus base sources; raw occurrences',
                'runtime_validation_performed': False, 'generated_indexes_used': False,
                'manifest_sha256': sha(ASSETS / 'photo_prompt_source_manifest.json'),
                'head': json.loads((HERE / 'validation/task-start-preservation.json').read_text())['head'],
                'source_files': inventory,
                'counts': {'registered_extensions': len(manifest['sources']),
                           'files_read': len(payloads), 'candidate_rows': sum(e['kind'] == 'candidate' for e in entries),
                           'profile_rows': sum(e['kind'] == 'visual_profile' for e in entries),
                           'bundle_rows': sum(r.get('bundle_rows', 0) for r in inventory),
                           'candidate_lexical_status': dict(collections.Counter(r['candidate_lexical_status'] for r in coverage)),
                           'profile_lexical_status': dict(collections.Counter(r['profile_lexical_status'] for r in coverage))},
                'comparison_method': 'NFKC normalized complete positive phrase or weighted token overlap; category-scoped candidate slots; no synonym, BM25F, embedding or activation inference'}
    (HERE / 'CURRENT-INVENTORY.json').write_text(json.dumps(overview, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'KEYWORD-COVERAGE.json').write_text(json.dumps({'schema_version': 'wardrobe-keyword-lexical-audit/v1', 'rows': coverage}, ensure_ascii=False, indent=2) + '\n')
    with (HERE / 'KEYWORD-COVERAGE.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'category', 'keyword_en', 'keyword_ko', 'usage_status', 'source_ids', 'candidate_lexical_status', 'candidate_refs', 'profile_lexical_status', 'profile_refs', 'meaning_support'])
        for r in coverage:
            writer.writerow([r['id'], r['category'], r['keyword_en'], r['keyword_ko'], r['usage_status'], '|'.join(r['source_ids']), r['candidate_lexical_status'], '|'.join(f"{h['file']}:{h['slot']}:{h['id']}" for h in r['candidate_hits']), r['profile_lexical_status'], '|'.join(f"{h['file']}:{h['id']}" for h in r['profile_hits']), 'not_inferred'])
    selected = {(h['file'], h['id'], h['slot']) for r in coverage for h in r['candidate_hits'] + r['profile_hits']}
    excerpts = [{k: e[k] for k in ['file', 'kind', 'slot', 'id', 'pointer', 'entry']} for e in entries if (e['file'], e['id'], e['slot']) in selected]
    (HERE / 'CURRENT-MATCHED-ROWS.json').write_text(json.dumps(excerpts, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(overview['counts'], ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
