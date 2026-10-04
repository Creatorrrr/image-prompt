#!/usr/bin/env python3
"""Freeze research inputs and lexical discovery; never edit runtime assets."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
SCRIPTS = ASSETS.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS))
import prompt_generator as pg

def normalize(s):
    return unicodedata.normalize('NFKC', str(s)).casefold().strip()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def main():
    reference = json.loads((HERE / 'REFERENCE-KEYWORDS.json').read_text())
    data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
    registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
    owner_by_candidate, owner_by_profile = {}, {}
    names = ['photo_prompt_tags.json', *pg.RESEARCH_EXTENSION_FILENAMES,
             'photo_prompt_visual_obligations.json', *pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES]
    source_paths = []
    for name in dict.fromkeys(names):
        path = ASSETS / name
        if not path.exists():
            continue
        source_paths.append(path)
        payload = json.loads(path.read_text())
        for slot, entries in payload.get('slots', {}).items():
            for entry in entries:
                owner_by_candidate.setdefault(f'{slot}.{entry["id"]}', []).append(str(path.relative_to(ROOT)))
        for profile in payload.get('profiles', []):
            owner_by_profile.setdefault(profile['id'], []).append(str(path.relative_to(ROOT)))
    catalogue = []
    for slot, entries in data['slots'].items():
        for entry in entries:
            key = f'{slot}.{entry["id"]}'
            catalogue.append({'key': key, 'slot': slot, 'source_files': owner_by_candidate.get(key, []),
                              'entry': entry})
    profiles = [{'id': p['id'], 'source_files': owner_by_profile.get(p['id'], []), 'profile': p}
                for p in registry['profiles']]
    probes = []
    for row in reference['rows']:
        ko, en = row['term'].split(' — ', 1)
        terms = [ko, *[x.strip() for x in en.split(' / ')]]
        if ', ' in en:
            terms.append(en.split(', ')[0])
        terms = [normalize(x) for x in terms if len(x) >= 3]
        candidate_hits = []
        for record in catalogue:
            entry = record['entry']
            exact_values = [entry.get('ko', ''), entry.get('en', ''),
                            *entry.get('aliases', []), *entry.get('keywords', [])]
            exact = [x for x in terms if x in {normalize(v) for v in exact_values}]
            text = normalize(json.dumps({k: entry.get(k) for k in ['ko','en','aliases','keywords','embedding_text','paraphrases','concept_units']}, ensure_ascii=False))
            lexical = [x for x in terms if x in text]
            if exact or lexical:
                candidate_hits.append({'key': record['key'], 'exact_inventory_terms': exact,
                                       'substring_occurrences': lexical, 'source_files': record['source_files']})
        profile_hits = []
        for record in profiles:
            p = record['profile']
            exact_values = p.get('activation', {}).get('exact_terms', [])
            exact = [x for x in terms if x in {normalize(v) for v in exact_values}]
            text = normalize(json.dumps(p.get('semantics', {}), ensure_ascii=False))
            lexical = [x for x in terms if x in text]
            if exact or lexical:
                profile_hits.append({'id': p['id'], 'exact_inventory_terms': exact,
                                     'substring_occurrences': lexical, 'source_files': record['source_files']})
        probes.append({'number': row['number'], 'term': row['term'], 'probe_terms': terms,
                       'candidate_hits': candidate_hits, 'profile_hits': profile_hits})
    source_paths += [SCRIPTS / name for name in ['prompt_generator.py','photo_candidate_semantics.py','photo_contracts.py','visual_profile_contracts.py','photo_camera_evidence.py','photo_visual_retrieval.py']]
    manifest = {'schema_version': 'seduction-source-snapshot/v1',
                'started_date_kst': '2026-10-04', 'snapshot_date_kst': '2026-10-05',
                'head': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(),
                'status': subprocess.check_output(['git','status','--porcelain=v1'], cwd=ROOT, text=True).splitlines(),
                'loaded_candidate_count': len(catalogue), 'loaded_profile_count': len(profiles),
                'slot_dimensions': data['candidate_semantic_policy']['slot_dimensions'],
                'files': [{'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                          for p in source_paths if p.exists()]}
    dump('SOURCE-SNAPSHOT.json', manifest)
    discovered_keys = {x['key'] for row in probes for x in row['candidate_hits']}
    discovered_profiles = {x['id'] for row in probes for x in row['profile_hits']}
    dump('CURRENT-INVENTORY.json', {
        'candidate_keys': [r['key'] for r in catalogue],
        'profile_ids': [r['id'] for r in profiles],
        'discovered_candidates': [r for r in catalogue if r['key'] in discovered_keys],
        'discovered_profiles': [r for r in profiles if r['id'] in discovered_profiles],
        'boundary': 'Lexically discovered records only; missing inventory hits do not establish a missing visual meaning.'})
    dump('CURRENT-DATA-AUDIT.json', {
        'schema_version':'seduction-current-data-audit/v1',
        'boundary':'Inventory comparison only. Substring occurrence is not semantic coverage, routing, exposure, adoption or native-pixel success.',
        'rows':probes})
    print(json.dumps({'candidates':len(catalogue),'profiles':len(profiles),'source_files':len(manifest['files']),
                      'reference_rows':len(probes),'inventory_hits':sum(bool(p['candidate_hits'] or p['profile_hits']) for p in probes)},ensure_ascii=False))

if __name__ == '__main__':
    main()
