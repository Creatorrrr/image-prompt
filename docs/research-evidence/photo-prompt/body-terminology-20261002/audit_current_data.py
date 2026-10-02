"""Read-only corpus audit. Writes evidence here; never changes skill assets."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def norm(text):
    import unicodedata
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', text).casefold()).strip()

registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
corpus = pg.load_json(SKILL / 'assets/photo_prompt_tags.json')
profiles = registry['profiles']
body_categories = {'pose_geometry', 'facial_surface_landmark', 'upper_torso_surface_landmark',
    'adult_garment_body_boundary', 'adult_body_contour_relation', 'adult_posterior_surface_landmark',
    'classical_pose_geometry', 'body_composition_geometry', 'adult_silhouette_relation',
    'adult_body_build_relation', 'adult_regional_body_relation', 'facial_shape_relation'}
selected_profiles = [p for p in profiles if p['category'] in body_categories or p['id'] in
    {'pfe_lateral_chest', 'pfe_lower_chest', 'pfe_back_face', 'pfe_bodycon', 'sheer_garment_optical_layering'}]
slots = ['silhouette_proportion', 'body_framing', 'body_orientation', 'body_pose', 'face_shape_relation',
    'facial_hair', 'skin_finish', 'skin_condition', 'body_marking', 'garment_detail']
probe_terms = ['petite', 'stocky', 'wiry', 'slender build', 'compact adult frame', 'willowy',
    'muscular', 'vascular', 'broad shoulders', 'wide hips', 'gluteal projection', 'busty figure',
    '글래머 체형', 'hip dip', 'sideboob', 'underboob', 'nipple', 'camel toe', 'vellus hair', 'body hair',
    'stretch marks', 'cellulite', 'V-line', 'S-line', 'dad bod', 'thicc', 'prosthetic limb']
exact_owner = {}
for p in profiles:
    for term in p['activation'].get('exact_terms', []) + p['activation'].get('project_glossary_aliases', []):
        exact_owner.setdefault(norm(term), []).append(p['id'])
probe = []
for term in probe_terms:
    t = norm(term)
    positive_profiles = []
    for p in profiles:
        s = p['semantics']
        positive = [s.get('definition', ''), *s.get('paraphrase_examples', []),
            *p.get('concept_candidate', {}).get('concept_terms', [])]
        positive.extend(word for group in s.get('component_semantics', {}).get('groups', []) for word in group.get('any_terms', []))
        if any(t in norm(x) for x in positive):
            positive_profiles.append(p['id'])
    candidate_hits = []
    for slot, entries in corpus['slots'].items():
        for entry in entries:
            positive = [entry.get(k, '') for k in ('ko', 'en', 'embedding_text')]
            positive += entry.get('aliases', []) + entry.get('keywords', [])
            if any(t in norm(x) for x in positive):
                candidate_hits.append({'slot': slot, 'id': entry['id']})
    probe.append({'term': term, 'exact_term_owners': exact_owner.get(t, []),
        'positive_profile_text_hits': positive_profiles, 'candidate_positive_text_hits': candidate_hits})
source_paths = [SKILL / 'assets/photo_prompt_visual_obligations.json', SKILL / 'assets/photo_prompt_tags.json']
source_paths += [SKILL / 'assets' / name for name in pg.VISUAL_OBLIGATION_EXTENSION_FILENAMES]
source_paths += [SKILL / 'assets' / name for name in pg.RESEARCH_EXTENSION_FILENAMES]
source_paths += [SKILL / 'assets/photo_prompt_visual_profile_index.json', SKILL / 'assets/photo_prompt_semantic_index.json']
source_paths = sorted(set(p for p in source_paths if p.exists()))
audit = {
    'schema_version': 'body-terminology-current-data-audit/v1', 'checked_on': '2026-10-02',
    'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
    'branch': subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip(),
    'counts': {'visual_profiles': len(profiles), 'unique_profile_ids': len({p['id'] for p in profiles}),
        'candidate_entries': sum(len(v) for v in corpus['slots'].values()), 'candidate_slots': len(corpus['slots']),
        'selected_body_adjacent_profiles': len(selected_profiles)},
    'category_counts': dict(Counter(p['category'] for p in profiles)),
    'source_files': [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p), 'bytes': p.stat().st_size} for p in source_paths],
    'selected_profiles': selected_profiles,
    'selected_slot_candidates': {k: corpus['slots'].get(k, []) for k in slots},
    'term_probes': probe,
    'method_limits': ['Text probes are substring inventories only, not retrieval or eligibility results.',
        'An empty text probe does not prove conceptual absence: existing phrases may describe it without the label.',
        'No embeddings, frozen-core candidate pack, composed prompt, runtime or pixels were tested.',
        'Body-adjacent category selection is documented here; it is not a complete anatomy taxonomy.'],
}
(OUT / 'CURRENT-DATA-AUDIT.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'head': audit['head'], 'counts': audit['counts'], 'source_files': len(source_paths),
    'slot_counts': {k: len(v) for k, v in audit['selected_slot_candidates'].items()}}, ensure_ascii=False))
