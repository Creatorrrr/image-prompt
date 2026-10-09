"""Read-only authored-data inventory. Writes only this research directory.

Lexical mentions do not establish meaning equivalence or live retrieval.
No runtime acquisition, index building, embedding call or image call.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import stat
import subprocess
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.dont_write_bytecode = True
sys.path.insert(0, str(SKILL / 'scripts'))


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def norm(value):
    return re.sub(r'[\W_]+', ' ', unicodedata.normalize('NFKC', str(value)).casefold()).strip()


def snapshot(paths):
    result = {}
    for path in sorted(set(paths)):
        if path.is_file():
            data = path.read_bytes()
            result[str(path.relative_to(ROOT))] = {'sha256': hashlib.sha256(data).hexdigest(),
                'bytes': len(data), 'mode': stat.S_IMODE(path.stat().st_mode)}
    return result


def terms():
    result = []
    group = None
    for line in (HERE / 'seed-terms.txt').read_text().splitlines():
        if line.startswith('@'):
            key, label = line[1:].split('|', 1)
            group = {'id': key, 'label': label}
        elif line.strip():
            for raw in line.split(';'):
                pair = raw.split(' — ', 1)
                ko, en = pair[0], pair[1] if len(pair) > 1 else ''
                variants = [ko, en] + ko.split(' / ') + en.split(' / ')
                result.append({'id': f'AF{len(result)+1:03d}', 'section': group['id'],
                    'section_label': group['label'], 'source_term': raw, 'ko': ko, 'en': en,
                    'query_variants': list(dict.fromkeys(v for v in variants if v))})
    assert len(result) == 347, len(result)
    return result


def main():
    import prompt_generator as pg

    started = datetime.now(ZoneInfo('Asia/Seoul')).isoformat()
    manifest = json.loads((ASSETS / 'photo_prompt_source_manifest.json').read_text())
    paths = [ASSETS / s['file'] for s in manifest['sources']]
    paths += [ASSETS / n for n in ['photo_prompt_tags.json', 'photo_prompt_visual_obligations.json',
        'photo_prompt_source_manifest.json', 'photo_prompt_semantic_index.json', 'photo_prompt_visual_profile_index.json']]
    paths += list((SKILL / 'scripts').glob('*.py'))
    before = snapshot(paths)
    status = subprocess.check_output(['git', 'status', '--porcelain=v1', '-z'], cwd=ROOT).decode().split('\0')
    external = [s for s in status if s and 'autumn-fashion-20261009' not in s
        and '2026-10-09-autumn-fashion-visual-semantics-research.md' not in s]
    dirty_paths = [ROOT / s[3:] for s in external if s[:2] != '??']
    dirty_before = snapshot(dirty_paths)
    data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
    registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
    candidates = []
    for slot, entries in data['slots'].items():
        for entry in entries:
            fields = pg.semantic_bm25f_fields_for_entry(entry, slot)
            positive = norm(' '.join(v for k, values in fields.items() if k != 'slot_context' for v in values))
            candidates.append({'id': entry['id'], 'slot': slot, 'ko': entry.get('ko'), 'en': entry.get('en'),
                'positive': positive, 'concept_units': entry.get('concept_units', []),
                'relations': entry.get('relations', []), 'affected_dimensions': entry.get('affected_dimensions', []),
                'affected_properties': entry.get('affected_properties', [])})
    profiles = [{'id': p['id'], 'category': p.get('category'), 'positive': norm(pg.positive_visual_profile_text(p)),
        'definition': p.get('semantics', {}).get('definition'), 'activation': p.get('activation'),
        'concept_candidate': p.get('concept_candidate'), 'authored_components': p.get('authored_components')}
        for p in registry['profiles']]
    inventory = terms()
    for term in inventory:
        mentions = {'candidates': [], 'profiles': []}
        variants = [(raw, norm(raw)) for raw in term['query_variants'] if norm(raw)]
        for kind, rows in [('candidates', candidates), ('profiles', profiles)]:
            for row in rows:
                matched = [raw for raw, query in variants if f' {query} ' in f" {row['positive']} "]
                if matched:
                    mentions[kind].append({'id': row['id'], 'slot': row.get('slot'), 'matched': matched})
        term['positive_field_mentions'] = mentions
        term['coverage_claim'] = 'lexical_only_not_semantic_support'
    after = snapshot(paths)
    changed = [p for p in before if before[p] != after.get(p)]
    dirty_after = snapshot(dirty_paths)
    counts = {'slots': len(data['slots']), 'candidates': len(candidates),
        'semantic_documents': len(list(pg.iter_semantic_entries(data))), 'profiles': len(profiles),
        'bundles': len(data.get('candidate_bundles', []))}
    dump('source-snapshot.json', {'started_at_kst': started,
        'completed_at_kst': datetime.now(ZoneInfo('Asia/Seoul')).isoformat(),
        'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip(),
        'source_files': before, 'changed_during_load': changed, 'tracked_dirty_files': dirty_before,
        'tracked_dirty_changed_during_load': [p for p in dirty_before if dirty_before[p] != dirty_after.get(p)],
        'preexisting_git_status': external, 'compiled_counts': counts,
        'manifest_source_counts': dict(collections.Counter(s['kind'] for s in manifest['sources'])),
        'runtime_dispatch_executed': False, 'embedding_calls': 0, 'image_calls': 0,
        'scope': 'working_tree_including_existing_uncommitted_data; loader-only inventory, not full validator'})
    dump('term-inventory.json', {'conversation_id': '6ac7dd53-2098-83ee-8a3c-84c3a250f650', 'terms': inventory})
    selected = {}
    for kind, rows in [('candidates', candidates), ('profiles', profiles)]:
        ids = {h['id'] for t in inventory if len(t['positive_field_mentions'][kind]) <= 30
            for h in t['positive_field_mentions'][kind]}
        selected[kind] = [{k: v for k, v in row.items() if k != 'positive'} for row in rows if row['id'] in ids]
    dump('current-positive-records.json', selected)
    summary = {'counts': counts, 'terms': len(inventory), 'section_counts': dict(collections.Counter(t['section'] for t in inventory)),
        'terms_with_candidate_mentions': sum(bool(t['positive_field_mentions']['candidates']) for t in inventory),
        'terms_with_profile_mentions': sum(bool(t['positive_field_mentions']['profiles']) for t in inventory),
        'terms_with_any_mentions': sum(any(t['positive_field_mentions'].values()) for t in inventory),
        'changed_during_load': changed}
    dump('inventory-summary.json', summary)
    print(json.dumps(summary, ensure_ascii=False))
    if changed:
        raise SystemExit('Concurrent source changes observed; refresh inventory before relying on counts.')


if __name__ == '__main__':
    main()
