"""Validate research artifacts and prototype syntax; do not run runtime or renders."""
import ast
from collections import Counter
import copy
import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
ASSETS = REPO / 'skills/photo-prompt-image-generator/assets'
SCRIPTS = ASSETS.parent / 'scripts'
sys.dont_write_bytecode = True
sys.path.insert(0, str(SCRIPTS))
from photo_candidate_semantics import (compile_extension_bundles, semantic_source,
                                      validate_bundle_references, validate_candidate_entries)
from visual_profile_contracts import compile_visual_profile, validate_hard_activation

def read(name):
    return json.loads((ROOT / name).read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Resolve only literals in the current loader's constants, without importing it.
constants = {}
def literal(node):
    if isinstance(node, ast.Name):
        return constants[node.id]
    if isinstance(node, (ast.Tuple, ast.List)):
        return [literal(x) for x in node.elts]
    return ast.literal_eval(node)
for node in ast.parse((SCRIPTS / 'prompt_generator.py').read_text()).body:
    if not isinstance(node, (ast.Assign, ast.AnnAssign)):
        continue
    try:
        value = literal(node.value)
    except (ValueError, KeyError, TypeError):
        continue
    for target in node.targets if isinstance(node, ast.Assign) else [node.target]:
        if isinstance(target, ast.Name):
            constants[target.id] = value

current_profiles = {}
for name in [constants['VISUAL_OBLIGATION_REGISTRY_FILENAME'],
             *constants['VISUAL_OBLIGATION_EXTENSION_FILENAMES']]:
    for profile in json.loads((ASSETS / name).read_text()).get('profiles', []):
        assert profile['id'] not in current_profiles, profile['id']
        current_profiles[profile['id']] = profile
base = json.loads((ASSETS / 'photo_prompt_tags.json').read_text())
current_entries = {}
for name in ['photo_prompt_tags.json', *constants['RESEARCH_EXTENSION_FILENAMES']]:
    for slot, entries in json.loads((ASSETS / name).read_text()).get('slots', {}).items():
        for entry in entries:
            current_entries.setdefault(slot, {})[entry['id']] = entry

keywords = read('KEYWORD-RESEARCH.json')
assert keywords['runtime_artifact'] is False
cards = keywords['cards']
assert len(cards) == 72 and len({x['id'] for x in cards}) == 72
assert Counter(x['group'] for x in cards) == {'hair_face': 17, 'body': 9, 'garment': 24, 'hardware': 22}
assert len({x['reference_term'] for x in cards}) == 72
for card in cards:
    assert len(card['visible_components']) >= 2 and card['required_relations']
    assert card['confusion_boundaries'] and card['render_gate_proposal']['partial_is_fail']
    for crosswalk in card['existing_profile_crosswalk']:
        assert crosswalk['profile_id'] in current_profiles
        assert crosswalk['current_definition'] == current_profiles[crosswalk['profile_id']]['semantics']['definition']

reference = read('SOURCE-RECEIPTS.json')
supplemental = read('SUPPLEMENTAL-SOURCES.json')
assert len(reference['cases']) == 102
assert len(reference['receipts']) == 96
assert len({x['requested_url'] for x in reference['receipts']}) == 96
assert len(supplemental['receipts']) == 9
all_sources = {x['source_id']: x for x in [*reference['receipts'], *supplemental['receipts']]}
case_ids = {x['case_id'] for x in reference['cases']}
for card in cards:
    for source in card['source_examples']:
        assert source['source_id'] in all_sources
        assert source['case_id'] is None or source['case_id'] in case_ids
        assert source['url'] == all_sources[source['source_id']]['requested_url']
image_count = 0
receipt_hash_count = 0
for source in all_sources.values():
    if source.get('cache_path') and source.get('sha256'):
        assert digest(Path(source['cache_path'])) == source['sha256'], source['source_id']
        receipt_hash_count += 1
    if source['status'] == 'retrieved_image':
        assert source['width'] > 0 and source['height'] > 0
        image_count += 1
assert image_count == 98
assert sum(x.get('visual_review_status') == 'source_original_reviewed' for x in all_sources.values()) == 34

proposals = read('CANDIDATE-PROTOTYPES.json')['proposals']
assert len(proposals) == 14
data = {'slots': {}, 'candidate_semantic_policy': copy.deepcopy(base['candidate_semantic_policy'])}
existing_ids = {entry_id for entries in current_entries.values() for entry_id in entries}
positive_forbidden = ['Miku', 'MEIKO', 'KAITO', 'Luka', 'Vocaloid', 'Fukase', 'NurseRobot', 'MAYU', 'Snow', 'https://']
for proposal in proposals:
    entry = proposal['entry']
    card = next(x for x in cards if x['id'] == proposal['research_card_id'])
    assert entry['id'] not in existing_ids
    slot = card['proposed_slot']
    assert slot in base['candidate_semantic_policy']['slot_dimensions']
    assert set(entry['affected_dimensions']) <= set(base['candidate_semantic_policy']['slot_dimensions'][slot])
    data['slots'].setdefault(slot, []).append(entry)
    assert proposal['profile_binding_plan']['proposed_profile_id'] not in current_profiles
    positive = ' '.join([entry['ko'], entry['en'], *entry['aliases'], *entry['paraphrases'], *entry['keywords'], entry['embedding_text']])
    assert not any(x.casefold() in positive.casefold() for x in positive_forbidden)
    surface = semantic_source(entry, slot, data['candidate_semantic_policy'])
    assert surface['concept_units'] == entry['concept_units']
    assert surface['relations'] == entry['relations']
    assert surface['adoption'] == 'optional'
validate_candidate_entries(data, {'appearance'})

samples = read('PROFILE-PROTOTYPES.json')['proposals']
assert len(samples) == 3
compiled = []
for sample in samples:
    profile = sample['profile']
    validate_hard_activation(profile['activation']['hard_activation'])
    result = compile_visual_profile(profile)
    assert len(result['required_evidence_fields']) == 3
    assert len(result['render_gates']) == 3
    assert all(x['review_scale'] == 'native' for x in result['render_gates'])
    compiled.append(result)
compile_extension_bundles(data, {'visual_semantics': [x['proposed_visual_semantics_bundle'] for x in samples]})
validate_bundle_references(data, compiled)
assert len(data['candidate_bundles']) == 3
assert all(b['adoption'] == 'optional' and b['profile_activation'] == 'independent_request_evidence_only'
           for b in data['candidate_bundles'])

leads = read('DESIGN-RELATION-LEADS.json')['leads']
assert len(leads) == 24
assert len(read('ABSTRACT-TERMS.json')['terms']) == 6
holdouts = read('PLANNED-HOLDOUTS.json')
pixels = read('PLANNED-PIXEL-CASES.json')
assert len(holdouts['cases']) == 36 and holdouts['execution_status'] == 'not_run'
assert len(pixels['cases']) == 8 and pixels['execution_status'] == 'not_run'

baseline = read('WORKSPACE-BASELINE.json')
modified = [name for name, sha in baseline['file_sha256'].items()
            if not (REPO / name).is_file() or digest(REPO / name) != sha]
summary = {
    'schema_version': 'vocaloid-research-validation/v1', 'runtime_artifact': False,
    'validated_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'PASS' if not modified else 'ARTIFACTS_PASS_BASELINE_DRIFT',
    'current_registered_visual_profiles': len(current_profiles),
    'current_ordinary_slot_entries': sum(len(x) for x in current_entries.values()),
    'current_ordinary_slots': len(current_entries),
    'reference_cases': 102, 'reference_unique_urls': 96,
    'downloaded_primary_images': image_count, 'source_original_reviewed_images': 34,
    'cached_source_bytes_hash_checked': receipt_hash_count,
    'keyword_cards': 72, 'authoring_decisions': keywords['decision_counts'],
    'additional_relation_leads': 24, 'abstract_terms': 6,
    'candidate_prototypes_syntax_and_scope_checked': 14,
    'profile_authored_component_examples_compiled': 3,
    'optional_bundle_examples_compiled': 3,
    'planned_holdouts': 36, 'planned_pixel_families': 8,
    'baseline_files_checked': len(baseline['file_sha256']),
    'baseline_files_changed': modified,
    'not_performed': ['runtime source integration', 'runtime registry/index load qualification',
                      'live BM25F/embedding retrieval evaluation', 'fresh embedding calls',
                      'generated image/native pixel qualification', 'commit', 'push'],
    'limits': 'Prototype compiler/schema checks certify structure only. They do not establish request adoption, full runtime compatibility, prompt evidence or generated pixels.',
}
(ROOT / 'VALIDATION-SUMMARY.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(summary, ensure_ascii=False, indent=2))
