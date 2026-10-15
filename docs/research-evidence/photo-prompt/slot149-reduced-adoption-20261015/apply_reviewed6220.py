"""Apply only the existing accepted6220 proof to a staged149 corpus.

No new review, proof, source meaning or dependency is authored here. This bounded
helper does not satisfy or alter the separate full native adoption gates.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
RESEARCH = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
SCRIPTS = ROOT / 'skills/photo-prompt-image-generator/scripts'
sys.path[:0] = [str(SCRIPTS), str(RESEARCH)]
import photo_candidate_corpus as c
import photo_scoped_slot_adoption as scoped
import native_reviews as reviews

CID = 'cand_afdb9168ea8c53ad921a8574ed5248d1'
INVENTORY = RESEARCH / 'ROOT-CURRENT149-APPROVAL-INVENTORY-04.json'
INVENTORY_RAW_SHA256 = '91019bfa7a4b80465637cf80970a030d5960a39495cfd624ade19ae5741e3b6e'
BATCH_NAME = 'review05250-simple5-149-01'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def accepted_inputs():
    """Verify exactly the accepted five-row batch; select only ordinal6220."""
    if sha(INVENTORY.read_bytes()) != INVENTORY_RAW_SHA256:
        raise ValueError('pinned root approval inventory04 changed')
    inventory = reviews.read_json(INVENTORY)
    items = [item for item in inventory['records'] if item['candidate_id'] == CID]
    if (len(items) != 1 or items[0]['ordinal'] != 6220 or inventory['whole_inventory'] != 18250
            or inventory['schema'] != 'photo-root-existing-current149-approval-inventory/v1'):
        raise ValueError('exact root selected6220 inventory row required')
    item = items[0]
    folder = RESEARCH / 'native_batches' / BATCH_NAME
    if item['batch']['file'] != str((folder / 'BATCH.json').relative_to(ROOT)):
        raise ValueError('unexpected accepted6220 batch')
    reviews.artifact(ROOT, item['batch'])
    verified = reviews.verify_batch(
        RESEARCH / 'native-inputs/prepared' / BATCH_NAME / 'ASSIGNMENT.json',
        folder / 'BATCH.json', folder / 'NOTE.json', root=ROOT, here=RESEARCH)
    reviews.verify_acceptance(ROOT, item['acceptance'], verified)
    row = verified['records'][CID]
    current = reviews.artifact(ROOT, inventory['current_source'])
    if (row['status'] != 'approved' or c.digest(row['proof']) != item['proof_sha256']
            or c.digest(row['source_after']) != item['source_sha256']
            or not scoped.exact(current['candidates'][CID], row['source_after'])
            or c.digest(current['slot_catalog']) != inventory['catalog_sha256']):
        raise ValueError('selected accepted6220 source/proof/current catalog differs')
    inp = reviews.read_json(RESEARCH / 'native-inputs/prepared' / BATCH_NAME / 'INPUT.json')
    original = reviews.artifact(ROOT, inp['original_snapshot'])
    return original, row, inventory


def build_proposal(source, original, row, inventory):
    """Preserve every other original source record and every staged relationship."""
    if (len(source['candidates']) != 18250 or len(source['slot_catalog']) != 149
            or not scoped.exact(source['candidates'], original['candidates'])):
        raise ValueError('exact18250 original staged source records required before selected6220')
    if (row['candidate_id'] != CID or row['ordinal'] != 6220 or row['status'] != 'approved'
            or not scoped.exact(source['candidates'][CID], row['source_before'])
            or c.digest(source['slot_catalog']) != inventory['catalog_sha256']):
        raise ValueError('exact accepted6220 original source/current149 catalog required')
    if (row['dependency_records'] or row['reference_bindings']
            or row['proof']['dependencies'] != {'base': []}
            or row['proof']['reference_sha256']):
        raise ValueError('selected6220 must remain dependency free')
    for field in ('id', 'record_kind', 'conditions', 'effects', 'provenance'):
        if not scoped.exact(row['source_before'][field], row['source_after'][field]):
            raise ValueError('selected source must preserve original ' + field)
    proposed = copy.deepcopy(source)
    selected = copy.deepcopy(row['source_after'])
    if 'role_evidence' in selected['content']:
        raise ValueError('source_after cannot contain an unverified proof')
    selected['content']['role_evidence'] = copy.deepcopy(row['proof'])
    proposed['candidates'][CID] = selected
    c.validate(proposed)
    if (any(not scoped.exact(source[field], proposed[field]) for field in
            ('slot_catalog', 'slot_bindings', 'policies'))
            or any(not scoped.exact(value, proposed['candidates'][cid])
                   for cid, value in source['candidates'].items() if cid != CID)):
        raise ValueError('unselected source or staged relation changed')
    return proposed


def apply_staged(assets, output):
    from photo_candidate_sources import SourceInventory
    assets, output = Path(assets).resolve(), Path(output).resolve()
    operating = (ROOT / 'skills/photo-prompt-image-generator/assets').resolve()
    if assets == operating or operating in assets.parents:
        raise ValueError('only staged assets may be modified')
    if output.exists() or output == assets or assets in output.parents:
        raise ValueError('report must be a fresh file outside staged assets')
    original, row, inventory = accepted_inputs()
    source = c.load(assets)
    proposed = build_proposal(source, original, row, inventory)
    files = SourceInventory.load(assets)
    raw = {name: (assets / name).read_bytes() for name, _ in files.rows}
    raw[c.MANIFEST_NAME] = (assets / c.MANIFEST_NAME).read_bytes()
    owners = [name for name, kind in files.rows if kind == 'candidates'
              and CID in c.decode(raw[name])['candidates']]
    if len(owners) != 1:
        raise ValueError('unique selected6220 candidate module owner required')
    owner = owners[0]
    payload = c.decode(raw[owner])
    replacements = {**payload['candidates'], CID: proposed['candidates'][CID]}
    after_raw = scoped._map_module(payload, raw[owner], replacements, 'candidates')
    before_values = scoped._map_entries(raw[owner].decode('utf-8'), 'candidates')
    after_values = scoped._map_entries(after_raw.decode('utf-8'), 'candidates')
    if any(before_values[cid] != after_values[cid] for cid in before_values if cid != CID):
        raise ValueError('unselected raw candidate record changed')
    if any((assets / name).read_bytes() != value for name, value in raw.items()):
        raise ValueError('staged source changed during selected6220 preview')
    temporary = (assets / owner).with_suffix('.selected6220.pending')
    if temporary.exists():
        raise ValueError('selected6220 temporary path already exists')
    temporary.write_bytes(after_raw)
    temporary.replace(assets / owner)
    if not scoped.exact(c.load(assets), proposed):
        raise ValueError('written selected6220 corpus differs from preview')
    if any((assets / name).read_bytes() != value for name, value in raw.items() if name != owner):
        raise ValueError('unselected staged file changed')
    report = {'schema': 'photo-scoped-reviewed-source-adoption/v1', 'candidate_id': CID,
        'ordinal': 6220, 'changed_file': owner, 'original_other_records_preserved': 18249,
        'bindings_policies_catalog_preserved': True, 'dependencies': 0,
        'source_sha256': c.digest(source), 'result_sha256': c.digest(proposed),
        'accepted_proof_sha256': c.digest(row['proof']),
        'inventory04_raw_sha256': INVENTORY_RAW_SHA256,
        'candidate_module_before_sha256': sha(raw[owner]),
        'candidate_module_after_sha256': sha(after_raw),
        'native_qualified_count_applied_here': 1, 'full_native_qualification': False,
        'new_reviews_created': 0}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', required=True, type=Path)
    parser.add_argument('--output', '--report', dest='output', required=True, type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(apply_staged(args.assets, args.output), sort_keys=True))


if __name__ == '__main__':
    main()
