"""Bind independent provenance to the already recorded managed native attempt.

The managed native-result command creates the only ledger row. The same recorder
functions validate an enriched provenance input and build the manifest without
appending a second row for that one invocation.
"""
from pathlib import Path
import hashlib
import json
import sys

ARM = Path(__file__).resolve().parent
ROOT = Path('/Users/chasoik/Projects/image-prompt')
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
from record_image_run import build_entry, build_independent_manifest, parse_args

state = json.loads((ARM / 'run/workflow.json').read_text())
operation = state['operations'][-1]
flags = operation['record_args']
receipt = json.loads((ARM / 'candidate_pack.runtime-receipt.json').read_text())
source = json.loads((ARM / 'SOURCE-RECEIPT.json').read_text())
manifest_path = ARM / 'run_manifest.json'
args = parse_args(flags + [
    '--arm-id', 'arm-2',
    '--worktree-id', str(ARM),
    '--skill-sha256', source['skill_sources'][0]['sha256'],
    '--source-ref', 'photo-runtime-generation:' + receipt['generation_id'],
    '--candidate-pack-version', 'v6',
    '--independent-no-cross-arm-inputs',
    '--manifest', str(manifest_path),
])
enriched = build_entry(args)
ledger = Path(args.ledger)
rows = [json.loads(line) for line in ledger.read_text().splitlines() if line]
row = next(item for item in rows if item['run_id'] == enriched['run_id'])
assert all(enriched.get(key) == value for key, value in row.items())
manifest = build_independent_manifest(row, args)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2,
                                    sort_keys=True) + '\n')
proof = {
    'schema_version': 'soil-independent-manifest-binding/v1',
    'method': 'Existing record_image_run.parse_args/build_entry/build_independent_manifest; no second ledger append',
    'reason': 'Managed native-result already records the invocation but has no independent-manifest flags. Appending enriched fields with the same run identity would conflict.',
    'ledger_run_id': row['run_id'],
    'ledger_row_count': len(rows),
    'ledger_sha256': hashlib.sha256(ledger.read_bytes()).hexdigest(),
    'managed_row_preserved_exactly': True,
    'enriched_input_matches_every_managed_row_field': True,
    'actual_image_call_count': args.image_call_count,
    'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
}
(ARM / 'MANIFEST-BINDING.json').write_text(
    json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(proof))
