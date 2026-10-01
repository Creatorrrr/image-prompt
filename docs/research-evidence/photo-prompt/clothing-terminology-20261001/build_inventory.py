#!/usr/bin/env python3
"""Read-only runtime inventory audit; writes research artifacts in this directory only."""
import collections
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import prompt_generator as pg


def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def norm(value):
    # Strip Latin accents but recompose Hangul before matching syllables.
    value = unicodedata.normalize('NFKD', str(value)).casefold()
    value = unicodedata.normalize('NFC', ''.join(c for c in value if not unicodedata.combining(c)))
    return ' '.join(re.sub(r'[^a-z0-9가-힣]+', ' ', value).split())


def contains(text, term):
    return bool(term) and (' ' + term + ' ') in (' ' + text + ' ')


cached = json.loads((HERE / 'referenced-conversation-cached.json').read_text())
original = next(i['text'] for i in cached['items'] if i['type'] == 'agentMessage')
original = original[:original.index('## 4-5.')]
supplement = (HERE / 'referenced-conversation-supplement.txt').read_text()
supplement = supplement[supplement.index('4-5.'):supplement.index('Sections 6-7')]
combined = original + '\n' + supplement

rows = []
section = None
headings = {}
for line in combined.splitlines():
    h = re.match(r'^(?:## )?([1-5]-\d+)\.\s*(.*)', line)
    if h:
        section = h[1]
        headings[section] = h[2]
    if section is None:
        continue
    # The seed conversation, not an authoritative definition, supplies these labels.
    for m in re.finditer(r'([^,\n()|]+)\(([^()]+)\)', line):
        ko = m[1].split('**')[-1].strip(' .')
        en = m[2].split(',')[0].strip()
        if not re.search(r'[A-Za-z]', en):
            continue
        for alias in en.split(' / '):
            rows.append({'section': section, 'ko': ko, 'en': alias.strip(),
                         'origin': 'referenced_conversation', 'source_phrase': m[0].strip()})

# Korean-only enumerations and unlabeled terms explicitly present in the response.
extras = {
    '5-1': '길 깃 동정 고름 섶 무 배래 끝동 곁마기 회장 허리말기 대님 귀주머니 두루주머니 띠돈 끈목 매듭 주체 술'.split(),
    '3-2': ['PVC'],
    '2-3': ['자보'],
    '4-6': ['브로그'],
    '6': ['슬리브리스', '반만 넣어 입기'],
}
for sec, terms in extras.items():
    for term in terms:
        rows.append({'section': sec, 'ko': term, 'en': '', 'origin': 'referenced_conversation', 'source_phrase': term})

unique = {}
for row in rows:
    key = (row['section'], norm(row['en'] or row['ko']))
    unique.setdefault(key, row)
rows = list(unique.values())
for i, row in enumerate(rows, 1):
    row['id'] = f'KW{i:04d}'
    row['normalized_term'] = norm(row['en'] or row['ko'])
    row['primary_definition_status'] = 'seed_only_until_mapped_to_research_record'

assets = ROOT / 'skills/photo-prompt-image-generator/assets'
data = pg.load_json(assets / 'photo_prompt_tags.json')
registry = pg.load_visual_obligation_registry(assets / 'photo_prompt_visual_obligations.json')
profiles = registry['profiles']
candidates = []
for slot, values in data['slots'].items():
    for value in values:
        candidate = {'slot': slot, 'id': value['id']}
        candidate['identity_text'] = norm(' '.join(str(value.get(k, '')) for k in
            ('id', 'ko', 'en', 'aliases', 'keywords', 'concept_units')))
        candidates.append(candidate)

profile_entries = []
for profile in profiles:
    act = profile.get('activation', {})
    exact = [norm(t) for t in act.get('exact_terms', []) + act.get('project_glossary_aliases', [])]
    desc = norm(json.dumps({k: profile.get(k) for k in
        ('id', 'category', 'activation', 'semantics', 'authored_components')}, ensure_ascii=False))
    profile_entries.append({'id': profile['id'], 'exact_terms': exact, 'text': desc})

audit = []
for row in rows:
    needles = list(dict.fromkeys(filter(None, [norm(row['en']), norm(row['ko'])])))
    exact = [p['id'] for p in profile_entries if any(n in p['exact_terms'] for n in needles)]
    descriptive = [p['id'] for p in profile_entries if any(contains(p['text'], n) for n in needles)]
    cs = [{'slot': c['slot'], 'id': c['id']} for c in candidates
          if any(contains(c['identity_text'], n) for n in needles)]
    status = ('exact_profile_label' if exact else 'profile_text_mention' if descriptive
              else 'candidate_mention_only' if cs else 'no_normalized_lexical_hit')
    audit.append({'keyword_id': row['id'], 'section': row['section'], 'ko': row['ko'], 'en': row['en'],
                  'status': status, 'exact_profile_ids': exact,
                  'descriptive_profile_ids': descriptive, 'candidate_hits': cs,
                  'runtime_exposure': 'not_tested', 'candidate_adoption': 'not_tested',
                  'pixel_qualification': 'not_tested'})

files = ['skills/photo-prompt-image-generator/SKILL.md',
         'skills/photo-prompt-image-generator/scripts/prompt_generator.py']
files += ['skills/photo-prompt-image-generator/assets/' + f for f in
          ['photo_prompt_tags.json', 'photo_prompt_visual_obligations.json',
           'photo_prompt_visual_profile_index.json', 'photo_prompt_semantic_index.json']
          + list(pg.RESEARCH_EXTENSION_FILENAMES) + list(pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES)]
snapshot = {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in dict.fromkeys(files) if (ROOT / f).is_file()}
counts = collections.Counter(a['status'] for a in audit)
sections = {}
for sec in headings | {'6': '원문 혼동 및 착용 예시'}:
    entries = [a for a in audit if a['section'] == sec]
    sections[sec] = {'name': headings.get(sec, '원문 혼동 및 착용 예시'), 'seed_terms': len(entries),
                     'lexical_status': dict(collections.Counter(a['status'] for a in entries))}
dump('keyword-inventory.json', {'schema_version': 'clothing-keyword-inventory/research-v1',
    'conversation_id': cached['conversation_id'], 'truncation_recovered': True,
    'retrieval': ['read_thread first 20000 characters', 'rendered main DOM for 4-5 through 7'],
    'counting_rule': 'unique section plus normalized label; slash aliases split; repetitions across sections retained; Korean-only lists included; illustrative prose is not a full lexicon',
    'sections': sections, 'keywords': rows})
dump('current-data-audit.json', {'schema_version': 'clothing-data-audit/research-v1',
    'as_of': '2026-10-01 Asia/Seoul',
    'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'method': 'merged data from the actual load_json and load_visual_obligation_registry; accent and separator normalized phrase boundaries; no semantic similarity or candidate pack generation',
    'limits': ['Lexical presence is not a semantic definition, effective routing, ownership, completeness, exposure, adoption or pixel success.',
               'No lexical hit is a research priority, not proof that semantic retrieval cannot find the concept.',
               'Profile text can contain the term solely as a negative contrast.',
               'Exact label lookup can contain a different contextual sense.'],
    'merged_counts': {'slots': len(data['slots']), 'candidates': len(candidates),
                      'profiles': len(profiles), 'candidate_bundles': len(data.get('candidate_bundles', []))},
    'relevant_slots': {k: len(data['slots'][k]) for k in
                      ['costume_style', 'wardrobe_style', 'garment_detail', 'surface_material',
                       'wearable_accessory', 'footwear', 'silhouette_proportion']},
    'keyword_count': len(rows), 'lexical_summary': dict(counts), 'sections': sections,
    'source_hashes_before': snapshot, 'keywords': audit})
print(json.dumps({'keywords': len(rows), 'sections': sections, 'lexical_summary': dict(counts)}, ensure_ascii=False, indent=2))
