"""Read the current authored sources; write evidence only in this directory."""
from __future__ import annotations
import ast
import hashlib
import json
import pathlib
import re
import subprocess
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
GENERATOR = ROOT / 'skills/photo-prompt-image-generator/scripts/prompt_generator.py'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def constants():
    result = {}
    for node in ast.parse(GENERATOR.read_text()).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in {
                    'VISUAL_OBLIGATION_EXTENSION_FILENAMES',
                    'VISUAL_OBLIGATION_REGISTRY_FILENAME',
                    'RESEARCH_EXTENSION_FILENAMES', 'RESEARCH_EXTENSION_FILENAME',
                }:
                    try:
                        result[target.id] = ast.literal_eval(node.value)
                    except ValueError:
                        if isinstance(node.value, ast.Tuple):
                            result[target.id] = tuple(
                                result[item.id] if isinstance(item, ast.Name)
                                else ast.literal_eval(item) for item in node.value.elts
                            )
    return result

def run():
    c = constants()
    files = [c['VISUAL_OBLIGATION_REGISTRY_FILENAME'], *c['VISUAL_OBLIGATION_EXTENSION_FILENAMES']]
    profiles = []
    file_snapshots = []
    for name in files:
        path = ASSETS / name
        data = json.loads(path.read_text())
        file_snapshots.append({'path': str(path.relative_to(ROOT)), 'sha256': sha(path), 'count': len(data['profiles'])})
        for p in data['profiles']:
            profiles.append({'source_file': name, **p})
    candidates = []
    for name in c['RESEARCH_EXTENSION_FILENAMES']:
        path = ASSETS / name
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        file_snapshots.append({'path': str(path.relative_to(ROOT)), 'sha256': sha(path), 'slot_entry_count': sum(map(len, data.get('slots', {}).values()))})
        for slot, rows in data.get('slots', {}).items():
            candidates.extend({'source_file': name, 'slot': slot, **row} for row in rows)
    base = json.loads((ASSETS / 'photo_prompt_tags.json').read_text())
    for slot, rows in base.get('slots', {}).items():
        candidates.extend({'source_file': 'photo_prompt_tags.json', 'slot': slot, **row} for row in rows)
    file_snapshots.append({'path': 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json', 'sha256': sha(ASSETS / 'photo_prompt_tags.json')})
    p = json.loads((HERE / 'reference-thread.json').read_text())
    rows = []
    section = subsection = ''
    for line in p['thread']['preview'].splitlines():
        if line.startswith('## '):
            section, subsection = line[3:], ''
        elif line.startswith('### '):
            subsection = line[4:]
        elif line.startswith('| **'):
            cells = line.split('|')
            rows.append({'id': f'UC{len(rows)+1:03d}', 'section': section, 'subsection': subsection,
                         'label_ko': cells[1].strip('* '),
                         'conversation_description_ko': re.sub(r':chatgpt-content-reference\{[^}]+\}', '', cells[2]).strip(),
                         'provenance': 'referenced_conversation_unverified_description'})
    (HERE / 'keyword-inventory.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    families = {
        'joseon': ['동다리', '철릭', 'jeonbok', 'cheollik', 'dongdari'],
        'historical_cavalry': ['dolman', 'pelisse', 'hussar', 'zouave', 'czapka', 'plastron', '후사르', '펠리스', '주아브', '창기병'],
        'modern_military': ['AGSU', 'ASU', 'ACU', 'OCP', 'battle dress', 'battledress', '군복', 'military uniform'],
        'sailor': ['sailor collar', 'sailor uniform', '수병', '세일러 칼라'],
        'flight': ['flight suit', 'pilot uniform', '비행복', '조종사'],
        'court': ['swiss guard', 'livery', '스위스 근위대', '리버리', '시종복'],
        'police_fire': ['police uniform', 'police officer', '경찰', 'firefighter', '방화복', '소방'],
        'medical': ['nurse uniform', 'nurse costume', '간호복', 'scrub', '스크럽', 'lab coat', '백의', 'coverall'],
        'airline': ['JAL', '대한항공', 'Korean Air', 'kebaya', '케바야', 'cabin crew', '승무원'],
        'service': ['maid', '메이드', 'chef', '조리복', 'bellhop', '버니', 'bunny'],
        'school_academic': ['gakuran', '가쿠란', '세일러 교복', 'school uniform', '교복', 'academic gown', '학위복'],
        'religious': ['cassock', '카속', '수녀복', 'habit', 'kesa', '가사', 'miko', '미코', 'scapular'],
        'fiction': ['star trek', '스타 트렉', 'stormtrooper', 'clone trooper', 'nier', '2B', '9S', '보바통', 'quidditch', 'handmaid'],
        'transformations': ['corset', '코르셋', 'bodysuit', '바디수트', 'fraying', '헤짐', 'repair patch', '발광'],
    }
    def searchable(record):
        return json.dumps({k: record.get(k) for k in ['ko', 'en', 'aliases', 'keywords', 'embedding_text', 'concept_units', 'activation', 'semantics']}, ensure_ascii=False).casefold()
    def summary(record, kind):
        return {'kind': kind, 'source_file': record['source_file'], 'id': record['id'],
                'slot': record.get('slot'), 'label': record.get('ko') or record.get('semantics', {}).get('definition'),
                'exact_terms': record.get('activation', {}).get('exact_terms', []),
                'affected_dimensions': record.get('affected_dimensions', []),
                'affected_properties': record.get('affected_properties', []),
                'component_count': len(record.get('authored_components', {}).get('components', []))}
    family_hits = {}
    for family, terms in families.items():
        ph = [summary(x, 'profile') for x in profiles if any(t.casefold() in searchable(x) for t in terms)]
        ch = [summary(x, 'candidate') for x in candidates if any(t.casefold() in searchable(x) for t in terms)]
        family_hits[family] = {'query_terms': terms, 'profile_hits': ph, 'candidate_hits': ch}
    costume = json.loads((ASSETS / 'photo_prompt_costume_cosplay_extension.json').read_text())
    broad_ids = {'military_uniform_duty_system', 'school_uniform_institutional_system', 'cabin_crew_safety_role',
                 'clinical_nursing_duty_system', 'police_public_safety_duty_system', 'firefighter_protective_response_system'}
    audit = {'observed_on': '2026-10-04 Asia/Seoul', 'git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
             'method': 'static authored-file audit, no runtime or embedding retrieval',
             'limits': ['Substring hits are discovery leads, not verified coverage or retrieval success.',
                        'Working tree has concurrent changes; snapshot hashes define this audit only.'],
             'reference_row_count': len(rows), 'reference_section_counts': dict(Counter(x['section'] for x in rows)),
             'active_registry_file_count': len(files), 'active_profile_count': len(profiles),
             'candidate_record_count': len(candidates),
             'costume_candidate_count': sum(map(len, costume['slots'].values())),
             'costume_bundle_count': len(costume['visual_semantics']),
             'broad_profiles': [{k: p.get(k) for k in ['id', 'source_file', 'activation', 'semantics', 'composition_instruction']} for p in profiles if p['id'] in broad_ids],
             'family_lexical_leads': family_hits, 'source_snapshots': file_snapshots,
             'git_status_at_audit': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True)}
    (HERE / 'baseline-audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: audit[k] for k in ['reference_row_count', 'active_registry_file_count', 'active_profile_count', 'candidate_record_count', 'costume_candidate_count', 'costume_bundle_count']}, ensure_ascii=False))

if __name__ == '__main__':
    run()
