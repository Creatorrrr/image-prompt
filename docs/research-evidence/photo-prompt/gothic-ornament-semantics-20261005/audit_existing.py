"""Capture authored identities and bounded keyword matches without running retrieval."""
from __future__ import annotations
import ast, hashlib, json, re, subprocess, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
SCRIPT = ROOT / 'skills/photo-prompt-image-generator/scripts/prompt_generator.py'

def norm(value):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', value).casefold()).strip()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    script = SCRIPT.read_bytes()
    constants = {}
    names = {'RESEARCH_EXTENSION_FILENAME', 'RESEARCH_EXTENSION_FILENAMES', 'VISUAL_OBLIGATION_EXTENSION_FILENAMES'}
    for node in ast.parse(script.decode()).body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in names:
                if isinstance(node.value, ast.Tuple):
                    constants[target.id] = [constants[x.id] if isinstance(x, ast.Name) else ast.literal_eval(x) for x in node.value.elts]
                else:
                    constants[target.id] = ast.literal_eval(node.value)
    files = list(dict.fromkeys(['photo_prompt_tags.json', 'photo_prompt_quality_layers.json', 'photo_prompt_visual_obligations.json'] + constants['RESEARCH_EXTENSION_FILENAMES'] + constants['VISUAL_OBLIGATION_EXTENSION_FILENAMES']))
    captured = {name: (ASSETS / name).read_bytes() for name in files}
    candidates, profiles, meaning_rows = [], [], []
    for file, raw in captured.items():
        payload = json.loads(raw)
        for slot, records in payload.get('slots', {}).items():
            for entry in records:
                positive = [entry.get('ko', ''), entry.get('en', '')] + entry.get('aliases', []) + entry.get('keywords', []) + entry.get('paraphrases', [])
                candidates.append({'file': file, 'slot': slot, **entry, '_positive': [norm(x) for x in positive if isinstance(x, str)]})
        profiles.extend({'file': file, **p} for p in payload.get('profiles', []))
        meaning_rows.extend({'file': file, **p} for p in payload.get('visual_semantics', []) if isinstance(p, dict))
    source = json.loads((HERE / 'SOURCE-KEYWORDS.json').read_text())
    rows, related_ids, related_profile_ids, related_meaning_ids = [], set(), set(), set()
    for item in source['entries']:
        terms = [norm(x) for x in re.split(r' — | / |, ', item['label']) if len(norm(x)) > 2]
        exact_candidates, lexical_candidates, exact_profiles = [], [], []
        for entry in candidates:
            matched = sorted(set(terms) & set(entry['_positive']))
            lexical = sorted({t for t in terms if len(t) > 4 and any(t in x for x in entry['_positive'])})
            ref = {k: entry.get(k) for k in ['file', 'slot', 'id', 'ko', 'en', 'affected_dimensions', 'affected_properties']}
            if matched:
                exact_candidates.append(ref | {'matched_terms': matched})
                related_ids.add((entry['file'], entry['slot'], entry['id']))
            elif lexical:
                lexical_candidates.append(ref | {'matched_terms': lexical})
        lexical_candidates = lexical_candidates[:8]
        related_ids.update((e['file'], e['slot'], e['id']) for e in lexical_candidates)
        for profile in profiles:
            activation = profile.get('activation', {})
            positive = activation.get('exact_terms', []) + activation.get('project_glossary_aliases', [])
            matched = sorted(set(terms) & {norm(x) for x in positive if isinstance(x, str)})
            if matched:
                exact_profiles.append({'file': profile['file'], 'id': profile['id'], 'definition': profile.get('semantics', {}).get('definition'), 'matched_terms': matched})
                related_profile_ids.add((profile['file'], profile['id']))
        raw_meaning_leads = []
        for meaning in meaning_rows:
            positive = [meaning.get('primary_visual_proposition', '')] + meaning.get('source_keywords', [])
            matched = sorted({t for t in terms if len(t) > 4 and any(t in norm(x) for x in positive if isinstance(x, str))})
            if matched:
                raw_meaning_leads.append({'file': meaning['file'], 'id': meaning.get('id'), 'primary_visual_proposition': meaning.get('primary_visual_proposition'), 'candidate_ids': meaning.get('candidate_ids', []), 'matched_positive_terms': matched})
        raw_meaning_leads = raw_meaning_leads[:5]
        related_meaning_ids.update((e['file'], e['id']) for e in raw_meaning_leads)
        rows.append({'number': item['number'], 'label': item['label'], 'inventory_terms': terms, 'exact_candidates': exact_candidates, 'lexical_candidates_for_review': lexical_candidates, 'exact_profiles': exact_profiles, 'dictionary_visual_semantics_leads': raw_meaning_leads})
    unchanged = SCRIPT.read_bytes() == script and all((ASSETS / name).read_bytes() == raw for name, raw in captured.items())
    if not unchanged:
        raise SystemExit('Authored data changed during audit. Retry the read-only inventory.')
    dump('EXISTING-COVERAGE.json', {'status': 'AUTHORING_INVENTORY_ONLY', 'method': 'Positive labels/aliases/keywords/paraphrases only. Exact equality uses NFKC and casefold. Bounded substring matches are review leads, not semantic coverage or runtime exposure. Claim limits and contrast examples are excluded. Raw profiles and dictionary visual_semantics rows are inventoried separately; neither is a resolved runtime pack.', 'candidate_records': len(candidates), 'distinct_slot_ids': len({(e['slot'], e['id']) for e in candidates}), 'profile_records': len(profiles), 'dictionary_visual_semantics_records': len(meaning_rows), 'terms_with_exact_candidate_label': sum(bool(r['exact_candidates']) for r in rows), 'terms_with_exact_profile_label': sum(bool(r['exact_profiles']) for r in rows), 'rows': rows})
    dump('AUTHORING-INVENTORY.json', {'status': 'READ_ONLY_CAPTURE', 'candidate_catalog': [{k: e[k] for k in ['file', 'slot', 'id']} for e in candidates], 'profile_catalog': [{k: e[k] for k in ['file', 'id']} for e in profiles], 'review_candidates': [{k: v for k, v in e.items() if k != '_positive'} for e in candidates if (e['file'], e['slot'], e['id']) in related_ids], 'review_profiles': [p for p in profiles if (p['file'], p['id']) in related_profile_ids], 'review_dictionary_visual_semantics': [p for p in meaning_rows if (p['file'], p['id']) in related_meaning_ids]})
    dump('CHECKOUT-SNAPSHOT.json', {'date_kst': '2026-10-05', 'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(), 'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(), 'dirty_records_at_capture': [x for x in subprocess.check_output(['git', 'status', '--porcelain=v1', '-z'], cwd=ROOT).decode().split('\0') if x], 'manifest_literals': constants, 'authored_source_sha256': {name: digest(raw) for name, raw in captured.items()}, 'generator_sha256': digest(script), 'stable_during_capture': unchanged, 'boundary': 'No retrieval execution, no embeddings, no active asset/index/runtime mutation.'})
    print(json.dumps({'source_terms': len(rows), 'candidate_records': len(candidates), 'profile_records': len(profiles), 'authored_files': len(files), 'exact_candidate_labels': sum(bool(r['exact_candidates']) for r in rows), 'exact_profile_labels': sum(bool(r['exact_profiles']) for r in rows), 'retained_review_records': len(related_ids)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
