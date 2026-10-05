"""Read authored data once and write a reproducible research-only inventory."""
from __future__ import annotations
import ast
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
SCRIPT = ROOT / 'skills/photo-prompt-image-generator/scripts/prompt_generator.py'

def norm(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', value).casefold()).strip()

def write(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    # Read literal manifests without running generation or making embedding calls.
    generator_raw = SCRIPT.read_bytes()
    tree = ast.parse(generator_raw.decode())
    constants = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in {'RESEARCH_EXTENSION_FILENAME', 'RESEARCH_EXTENSION_FILENAMES', 'VISUAL_OBLIGATION_EXTENSION_FILENAMES'}:
                if isinstance(node.value, ast.Tuple):
                    constants[target.id] = [constants[x.id] if isinstance(x, ast.Name) else ast.literal_eval(x) for x in node.value.elts]
                else:
                    constants[target.id] = ast.literal_eval(node.value)
    filenames = list(dict.fromkeys(['photo_prompt_tags.json', 'photo_prompt_quality_layers.json', 'photo_prompt_visual_obligations.json'] + constants['RESEARCH_EXTENSION_FILENAMES'] + constants['VISUAL_OBLIGATION_EXTENSION_FILENAMES']))
    captured = {name: (ASSETS / name).read_bytes() for name in filenames}
    authored, profiles = [], []
    for name, raw in captured.items():
        payload = json.loads(raw)
        for slot, entries in payload.get('slots', {}).items():
            for entry in entries:
                positive = [entry.get('ko', ''), entry.get('en', '')] + entry.get('aliases', []) + entry.get('paraphrases', []) + entry.get('keywords', [])
                authored.append({'file': name, 'slot': slot, **entry, '_positive_terms': [t for t in positive if isinstance(t, str)]})
        for profile in payload.get('profiles', []):
            profiles.append({'file': name, **profile})
    source = json.loads((HERE / 'SOURCE-KEYWORDS.json').read_text())
    rows = []
    for item in source['entries']:
        label = item['label']
        terms = [norm(t) for t in re.split(r' — | / |／', label) if len(norm(t)) > 1]
        terms += [norm(t) for t in re.split(r'·', terms[0]) if len(norm(t)) > 1]
        exact_candidates = []
        for entry in authored:
            matched = sorted(set(terms) & {norm(t) for t in entry['_positive_terms']})
            if matched:
                exact_candidates.append({k: entry.get(k) for k in ['file', 'slot', 'id', 'ko', 'en', 'concept_units', 'relations', 'affected_dimensions', 'affected_properties']} | {'matched_terms': matched})
        exact_profiles = []
        for profile in profiles:
            activation = profile.get('activation', {})
            matched = sorted(set(terms) & {norm(t) for t in activation.get('exact_terms', []) + activation.get('project_glossary_aliases', [])})
            if matched:
                exact_profiles.append({'file': profile['file'], 'id': profile['id'], 'definition': profile.get('semantics', {}).get('definition'), 'matched_terms': matched})
        rows.append({'number': item['number'], 'label': label, 'inventory_terms': terms, 'exact_candidate_label_matches': exact_candidates, 'exact_profile_label_matches': exact_profiles})
    unchanged = all(sha((ASSETS / name).read_bytes()) == sha(raw) for name, raw in captured.items()) and SCRIPT.read_bytes() == generator_raw
    if not unchanged:
        raise SystemExit('Authored sources changed during audit; rerun before using this inventory.')
    write('EXISTING-COVERAGE.json', {'schema_version': 'intellectual-existing-inventory/v1', 'method': 'Exact positive label/alias/paraphrase/keyword equality after NFKC and casefold. Compound splitting is inventory only. Excludes contrast and claim-limit text. This is NOT a semantic resolver or coverage score.', 'authored_record_count_before_deduplication': len(authored), 'distinct_slot_and_id_count': len({(e['slot'], e['id']) for e in authored}), 'authored_profile_record_count': len(profiles), 'terms_with_exact_candidate_label': sum(bool(r['exact_candidate_label_matches']) for r in rows), 'terms_with_exact_profile_label': sum(bool(r['exact_profile_label_matches']) for r in rows), 'rows': rows})
    # Preserve a full identity catalogue but retain full bodies only for reviewed
    # reuse references. The research builder must never clone the active corpus.
    decisions_path = HERE / 'TERM-DECISIONS.json'
    if not decisions_path.exists():
        raise SystemExit('Build the term decisions before refreshing the compact authored inventory.')
    reviewed = json.loads(decisions_path.read_text())['decisions']
    keep_ids = {r['id'] for d in reviewed for r in d['reuse']}
    keep_profiles = {'rembrandt_face_light_pattern', 'motivated_practical_mixed_interior_relation',
                     'blue_hour_ambient_practical_balance', 'rb_practical_pool', 'pv_profile_chin_support',
                     'pv_profile_figure_four', 'ae_profile_lip_press'}
    write('AUTHORING-INVENTORY.json', {'schema_version': 'intellectual-authored-inventory/v2',
        'capture_boundary': 'Full identity catalogue plus captured full records for reviewed reuse references. Not resolver exposure.',
        'candidate_catalog': [{k: e[k] for k in ['file', 'slot', 'id']} for e in authored],
        'profile_catalog': [{k: p[k] for k in ['file', 'id']} for p in profiles],
        'retained_candidates': [{k: v for k, v in e.items() if k != '_positive_terms'} for e in authored if e['id'] in keep_ids],
        'retained_profiles': [p for p in profiles if p['id'] in keep_profiles]})
    write('CHECKOUT-SNAPSHOT.json', {'date_kst': '2026-10-05', 'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(), 'dirty_records_at_audit': [x for x in subprocess.check_output(['git', 'status', '--porcelain=v1', '-z'], cwd=ROOT).decode().split('\0') if x], 'manifest_literals': constants, 'authored_source_sha256': {name: sha(raw) for name, raw in captured.items()}, 'generator_sha256': sha(generator_raw), 'stable_during_audit': unchanged, 'boundary': 'Read-only source inventory. No runtime assets, indexes, commits, or generation are changed.'})
    print(json.dumps({'source_terms': len(rows), 'exact_candidate_labels': sum(bool(r['exact_candidate_label_matches']) for r in rows), 'exact_profile_labels': sum(bool(r['exact_profile_label_matches']) for r in rows), 'distinct_slot_ids': len({(e['slot'], e['id']) for e in authored}), 'profile_records': len(profiles), 'authored_files': len(captured)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
