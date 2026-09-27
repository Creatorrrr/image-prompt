"""Promote reviewed portrait data, retaining a hash-bound maintenance ledger."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import photo_candidate_semantics as cs

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    catalog = {x['id'].lower(): x for x in read(HERE / 'concept-catalog.json')['concepts']}
    korean = read(HERE / 'korean-relations.json')
    extension = copy.deepcopy(read(HERE / 'candidate-extension.proposed.json'))
    for rows in extension['slots'].values():
        for entry in rows:
            concept = catalog[entry['id'].split('_')[1]]
            # Bilingual discovery is advisory. The complete component remains
            # the semantic unit; labels never make the all-of profile hard.
            labels = [concept['label_ko'], *concept['terms_en']]
            component_number = int(entry['id'].rsplit('_', 1)[1]) - 1
            if concept['id'] in korean:
                entry['ko'] = korean[concept['id']][component_number]
                labels.append(entry['ko'])
            entry['aliases'] = labels
            entry['keywords'] = labels
            entry['embedding_text'] = ' | '.join([entry['en'], *labels])
    for bundle in extension['visual_semantics']:
        concept = catalog[bundle['id'].removeprefix('pc_bundle_')]
        bundle['source_keywords'] = [concept['label_ko'], *concept['terms_en']]
    profiles = copy.deepcopy(read(HERE / 'visual-profiles.proposed.json'))
    profiles['description'] = 'Narrow owner-scoped portrait composition relations; approximate discovery is advisory.'
    for profile in profiles['profiles']:
        concept_id = profile['id'].split('_')[1].upper()
        clauses = korean[concept_id]
        profile['activation']['exact_terms'].append('; '.join(clauses))
        for component, clause in zip(profile['authored_components']['components'], clauses):
            component['match_terms'].append(clause)
    record_id = 'portrait-composition-research-20260927'
    record = {
        'record_id': record_id,
        'authored_source_sha256': cs.digest(extension),
        'visual_profile_source_sha256': cs.digest(profiles),
        'maintenance_only': {
            'research_path': str(HERE.relative_to(ROOT)),
            'source_ledger_sha256': sha(HERE / 'sources.json'),
            'source_conversation_sha256': sha(HERE / 'source-conversation.json'),
            'catalog_sha256': sha(HERE / 'concept-catalog.json'),
            'proposal_sha256': sha(HERE / 'candidate-extension.proposed.json'),
            'profile_proposal_sha256': sha(HERE / 'visual-profiles.proposed.json'),
            'korean_relation_source_sha256': sha(HERE / 'korean-relations.json'),
            'counts': {'atoms': 156, 'optional_bundles': 42, 'profiles': 16, 'render_gates': 64},
            'included_concepts': [x['id'] for x in catalog.values() if x['id'].startswith(('PC', 'PX'))],
            'deferred_proposals': [x for x in catalog.values() if x['id'].startswith(('PS', 'PM'))],
            'decisions': [
                'Reuse existing broad photographic controls; new clauses declare specific owners, contact, focus or spatial relations.',
                'No exact same-slot English duplicates exist against the pre-integration merged dictionary.',
                'Bilingual labels aid optional retrieval and never activate all-of hard profiles by themselves.',
                'Bundles stay optional and cannot activate their associated profiles.',
                'Reflected-face sharpness is observable; physical focusing distance remains explanatory research only.',
                'Collection, trend popularity, actual relationship, attractiveness and biography are not single-image pixel claims.'
            ],
            'claim_boundary': 'Integration and index integrity are separate from exposure, adoption, rendering and requester judgment.'
        }
    }
    extension['maintenance_ref'] = {
        'contract_version': 'photo-extension-maintenance-ref/v1',
        'record_id': record_id,
        'sha256': cs.digest(record)
    }
    write(ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance' / (record_id + '.json'), record)
    write(SKILL / 'assets/photo_prompt_portrait_composition_extension.json', extension)
    write(SKILL / 'assets/photo_prompt_visual_obligations_portrait_composition.json', profiles)
    print(json.dumps(record['maintenance_only']['counts']))

if __name__ == '__main__':
    main()
