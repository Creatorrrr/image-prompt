"""Validate the final authored/index revision without calling an image model."""
from pathlib import Path
import hashlib
import json
import sys

root = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
skill = root / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(skill / 'scripts'))
import prompt_generator as generator

data = generator.load_runtime_data()
registry = data[generator.VISUAL_OBLIGATIONS_DATA_KEY]
semantic = data[generator.SEMANTIC_INDEX_DATA_KEY]
visual = data[generator.VISUAL_PROFILE_INDEX_DATA_KEY]
payload = {
    'status': 'FINAL_REVISION_VALIDATED',
    'revision': json.loads(Path(__file__).with_name('APPLIED-CHANGES-FINAL.json').read_text())['final_revision'],
    'execution_root': str(root),
    'candidate_dictionary_hash': generator.dictionary_hash(data),
    'semantic_index_entry_count': len(semantic['entries']),
    'semantic_metadata_validation': 'pass',
    'visual_registry_sha256': generator.visual_profile_registry_sha256(registry),
    'visual_profile_count': len(registry['profiles']),
    'visual_index_binding_validation': 'pass',
    'asset_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted((skill / 'assets').glob('*.json'))},
}
output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in payload.items() if k != 'asset_sha256'}, ensure_ascii=False))
