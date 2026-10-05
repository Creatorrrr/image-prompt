"""Read-only authored-data inventory; writes only this research directory."""
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
SCRIPT = ROOT / 'skills/photo-prompt-image-generator/scripts/prompt_generator.py'
sys.path.insert(0, str(SCRIPT.parent))
import prompt_generator as generator

def norm(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', value).casefold()).strip()

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def literal_list(name):
    return list(getattr(generator, name))

def main():
    source = json.loads((HERE / 'SOURCE-KEYWORDS.json').read_text())
    data = generator.load_json(ASSETS / 'photo_prompt_tags.json')
    registry = generator.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
    filenames = ['photo_prompt_tags.json', 'photo_prompt_visual_obligations.json', 'photo_prompt_quality_layers.json'] + literal_list('RESEARCH_EXTENSION_FILENAMES') + literal_list('VISUAL_OBLIGATION_EXTENSION_FILENAMES')
    hashes = {str((ASSETS / name).relative_to(ROOT)): hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() for name in dict.fromkeys(filenames) if (ASSETS / name).exists()}
    authored = []
    for name in dict.fromkeys(['photo_prompt_tags.json'] + literal_list('RESEARCH_EXTENSION_FILENAMES')):
        path = ASSETS / name
        if not path.exists():
            continue
        payload = json.loads(path.read_text())
        for slot, entries in payload.get('slots', {}).items():
            for entry in entries:
                authored.append({'file': str(path.relative_to(ROOT)), 'slot': slot, 'id': entry['id'], 'ko': entry.get('ko'), 'en': entry.get('en'), 'positive_terms': [entry.get('ko', ''), entry.get('en', '')] + entry.get('aliases', []) + entry.get('paraphrases', []) + entry.get('keywords', []), 'concept_units': entry.get('concept_units', []), 'relations': entry.get('relations', []), 'affected_dimensions': entry.get('affected_dimensions', []), 'affected_properties': entry.get('affected_properties', [])})
    rows = []
    for item in source['entries']:
        label = item['label'].replace('†', '')
        terms = [norm(t) for t in re.split(r' — |／| / ', label) if len(norm(t)) > 1]
        terms += [norm(t) for t in re.split(r'·', terms[0]) if len(norm(t)) > 1]
        terms = list(dict.fromkeys(terms))
        matched = []
        for entry in authored:
            exact = sorted(set(terms) & {norm(t) for t in entry['positive_terms'] if isinstance(t, str)})
            if exact:
                matched.append({k: entry[k] for k in ['file', 'slot', 'id', 'ko', 'en', 'concept_units', 'relations', 'affected_dimensions', 'affected_properties']} | {'lexical_match_terms': exact})
        profile_hits = []
        for profile in registry['profiles']:
            activation = profile.get('activation', {})
            exact = sorted(set(terms) & {norm(t) for t in activation.get('exact_terms', []) + activation.get('project_glossary_aliases', [])})
            if exact:
                profile_hits.append({'id': profile['id'], 'lexical_match_terms': exact, 'activation': activation, 'definition': profile.get('semantics', {}).get('definition')})
        rows.append({'number': item['number'], 'label': item['label'], 'search_terms': terms, 'exact_positive_candidate_label_matches': matched, 'exact_profile_term_matches': profile_hits, 'interpretation': 'Lexical inventory only. No hit does not prove missing visual meaning; a hit does not prove contextual applicability, retrieval exposure, adoption, or pixel success.'})
    write('EXISTING-COVERAGE.json', {'schema_version': 'cute-existing-coverage/v1', 'method': 'NFKC/casefold full-term comparison over positive labels, aliases, paraphrases and keywords; contrast, limitations and research prose excluded. Compound labels are split for inventory, not for activation.', 'merged_slot_count': len(data['slots']), 'merged_candidate_count': sum(len(v) for v in data['slots'].values()), 'merged_visual_profile_count': len(registry['profiles']), 'terms_with_exact_candidate_label': sum(bool(r['exact_positive_candidate_label_matches']) for r in rows), 'terms_with_exact_profile_label': sum(bool(r['exact_profile_term_matches']) for r in rows), 'rows': rows})
    status = subprocess.check_output(['git', 'status', '--porcelain=v1', '-z'], cwd=ROOT).decode().split('\0')
    write('CHECKOUT-SNAPSHOT.json', {'schema_version': 'cute-research-checkout/v1', 'date_kst': '2026-10-05', 'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(), 'dirty_records_at_audit': [r for r in status if r], 'authored_source_hashes': hashes, 'generator_sha256': hashlib.sha256(SCRIPT.read_bytes()).hexdigest(), 'boundary': 'Research inventory only. All preexisting work is excluded from this task edits.'})
    print(json.dumps({'terms': len(rows), 'candidate_label_matches': sum(bool(r['exact_positive_candidate_label_matches']) for r in rows), 'profile_label_matches': sum(bool(r['exact_profile_term_matches']) for r in rows), 'merged_candidates': sum(len(v) for v in data['slots'].values()), 'merged_profiles': len(registry['profiles'])}, ensure_ascii=False))

if __name__ == '__main__':
    main()
