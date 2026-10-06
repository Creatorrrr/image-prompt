#!/usr/bin/env python3
"""Reproduce all 12,589 ordered provenance records offline without publishing them.

Run from any directory with Python -B. Uses only committed originals, current
assets and supported loaders. Temporary hardlinks are read-only source views;
no DATA, index, runtime store, Git, provider or network operations are performed.
"""
from __future__ import annotations
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PHOTO = Path('skills/photo-prompt-image-generator')
PARENT_SHA256 = '16766165b960a59c706482ebfa7406531276fddbc74bc708fc06058f04b8ba56'
SUMMARY_SHA256 = 'ddb901fd18d5bab666a4aa8426371fbbfd91bbb260d3626adebc0a33b47e7504'
INDEX_PROOF_SHA256 = '4fe317fc5f9a5bb0b93c4fc67541a490b3bae6742bd2ee103cdc2ea19afab932'
CURRENT_BINDINGS_SHA256 = '7d88384f2ccebeb5e10ccf3c30e565df3b1a679ed96c07b08bc3500c3ae22014'
EXPECTED = {('ordinary', 'slot:composition:ri_daoist_robe_sky_readable_composition'),
            ('visual_profile', 'ri_daoist_robe_sky')}
COUNTS = {'ordinary': 10396, 'visual_profile': 2193}
INDEXES = {'ordinary': 'photo_prompt_semantic_index.json',
           'visual_profile': 'photo_prompt_visual_profile_index.json'}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def regular(name):
    name = Path(name)
    require(not name.is_absolute() and '..' not in name.parts, 'unsafe source path')
    path = ROOT / name
    require(not any(p.is_symlink() for p in (path, *path.parents)), 'symlink source path')
    require(path.is_file(), 'missing source: ' + str(name))
    return path


def verified_original(row):
    path = regular(row['source_path'])
    raw = path.read_bytes()
    require(row['mode'] in ('100644', '100755')
            and path.stat().st_mode & 0o7777 == int(row['mode'][-3:], 8)
            and len(raw) == row['bytes'] and digest(raw) == row['sha256']
            and hashlib.sha1(f'blob {len(raw)}\0'.encode() + raw).hexdigest() == row['git_blob'],
            'original identity drift: ' + row['path'])
    return path


def finite(vector):
    return (isinstance(vector, list) and len(vector) == 768
            and all(type(x) in (int, float) and math.isfinite(x) for x in vector)
            and any(x != 0 for x in vector))


def offline(event, args):
    if event.startswith(('socket.', 'subprocess.')) or event in ('os.system', 'os.exec', 'os.posix_spawn'):
        raise PermissionError('offline provenance reproduction forbids external operations')


def main():
    sys.dont_write_bytecode = True
    sys.addaudithook(offline)
    require(digest((HERE / 'INDEX-ENTRY-PROVENANCE.json').read_bytes()) == SUMMARY_SHA256, 'compact summary drift')
    require(digest((HERE / 'INDEX-PROOF.json').read_bytes()) == INDEX_PROOF_SHA256, 'reviewed index proof drift')
    summary = read(HERE / 'INDEX-ENTRY-PROVENANCE.json')
    require(summary['schema'] == 'photo-index-entry-provenance-summary/v1'
            and summary['source_pin'] == '6b0338ebe6ad3a9a5ee3c603fc742311ad921054'
            and summary['reproducer'] == Path(__file__).name, 'compact summary identity drift')
    parent_path = HERE / 'V31-PARENT-SOURCE.json'
    require(digest(parent_path.read_bytes()) == PARENT_SHA256, 'original parent manifest drift')
    parent = read(parent_path)
    require(parent['source_pin'] == '6b0338ebe6ad3a9a5ee3c603fc742311ad921054', 'original pin drift')
    rows = {row['path']: row for row in parent['members']}
    proof = read(HERE / 'V32-ROBE-SOURCE-PROOF.json')
    bindings = {key: proof[key] for key in ('source_files_after', 'active_shards_after')}
    require(digest(canonical(bindings)) == CURRENT_BINDINGS_SHA256, 'sealed current binding map drift')
    for name, expected in {**proof['source_files_after'], **proof['active_shards_after']}.items():
        require(digest(regular(name).read_bytes()) == expected, 'current source/shard drift: ' + name)
    sys.path.insert(0, str(ROOT / PHOTO / 'scripts'))
    import prompt_generator as pg
    from photo_source_manifest import SourceInventory
    from visual_profile_index_storage import load_visual_profile_index_payload

    reviewed = {(r['corpus'], r['key']): r for r in read(HERE / 'INDEX-PROOF.json')['receipt_bindings']}
    require(set(reviewed) == EXPECTED, 'reviewed vector scope drift')
    provenance, changed = [], []
    # Keep link names within the temporary loader root and on the same mount.
    with tempfile.TemporaryDirectory(prefix='.robe-provenance-', dir=ROOT) as temporary:
        before = Path(temporary)
        for name, row in rows.items():
            relative = Path(name)
            if relative.parent == PHOTO / 'assets' and relative.suffix == '.json':
                os.link(verified_original(row), before / relative.name)
        for filename in INDEXES.values():
            for shard in read(before / filename)['shards']:
                name = (PHOTO / 'assets' / shard['path']).as_posix()
                origin = verified_original(rows[name])
                target = before / shard['path']
                target.parent.mkdir(parents=True, exist_ok=True)
                os.link(origin, target)
        payloads, texts = {}, {}
        for label, assets in (('before', before), ('after', ROOT / PHOTO / 'assets')):
            inventory = SourceInventory.load(assets)
            inventory.validate()
            data = pg.load_json(assets / 'photo_prompt_tags.json', inventory=inventory)
            registry = pg.load_visual_obligation_registry(assets / 'photo_prompt_visual_obligations.json', inventory=inventory)
            payloads[label] = {
                'ordinary': pg.load_semantic_index_payload(assets / INDEXES['ordinary']),
                'visual_profile': load_visual_profile_index_payload(assets / INDEXES['visual_profile'])}
            pg.validate_semantic_index_metadata(payloads[label]['ordinary'], data)
            pg.validate_visual_profile_index_metadata(payloads[label]['visual_profile'], registry)
            texts[label] = {
                'ordinary': {key: pg.semantic_text_for_entry(entry, slot, kind=kind)
                             for key, kind, entry, slot in pg.iter_semantic_entries(data)},
                'visual_profile': {profile['id']: pg.visual_profile_semantic_text(profile)
                                   for profile in registry['profiles']}}
        for corpus, count in COUNTS.items():
            old, new = (payloads[side][corpus]['entries'] for side in ('before', 'after'))
            require(len(old) == len(new) == count and list(old) == list(new)
                    == list(texts['before'][corpus]) == list(texts['after'][corpus]), 'entry count/order drift')
            for key, entry in new.items():
                prior, pair = old[key], (corpus, key)
                require(prior['text'] == texts['before'][corpus][key]
                        and entry['text'] == texts['after'][corpus][key]
                        and finite(prior['vector']) and finite(entry['vector']), 'canonical text/vector drift: ' + key)
                if pair in EXPECTED:
                    require(prior['text'] != entry['text'] and prior['vector'] != entry['vector'], 'missing expected change')
                    # Both metadata validators above reconstruct text-derived
                    # BM25F payloads. Visual entries also store the text digest.
                    derived = {'bm25f_document'} if corpus == 'ordinary' else {'text_sha256'}
                    if corpus == 'visual_profile':
                        require(all(item['text_sha256'] == digest(item['text'].encode('utf-8'))
                                    for item in (prior, entry)), 'derived visual text digest drift')
                    allowed = {'text', 'vector'} | derived
                    require({k: v for k, v in prior.items() if k not in allowed}
                            == {k: v for k, v in entry.items() if k not in allowed},
                            'reviewed entry changed unrelated metadata: ' + key)
                    binding = reviewed[pair]
                    require(digest(canonical(prior['vector'])) == binding['old_vector_sha256']
                            and digest(canonical(entry['vector'])) == binding['new_vector_sha256']
                            and digest(entry['text'].encode()) == binding['input_utf8_sha256']
                            and len(entry['text'].encode()) == binding['input_utf8_bytes'], 'reviewed vector binding drift')
                else:
                    require(prior == entry, 'unreviewed entry/text/vector change: ' + key)
                record = {'corpus': corpus, 'key': key,
                          'text_sha256': digest(entry['text'].encode('utf-8')),
                          'text_utf8_bytes': len(entry['text'].encode('utf-8')),
                          'vector_sha256': digest(canonical(entry['vector'])),
                          'origin': 'independently_reviewed_user_return' if pair in EXPECTED else 'unchanged_6b0338_exact_cache'}
                provenance.append(record)
                if pair in EXPECTED:
                    changed.append(record)
    pretty = (json.dumps(provenance, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    require(len(provenance) == 12589 and summary['counts'] == {**COUNTS, 'total': 12589, 'unchanged_exact_entries': 12587, 'reviewed_changed_entries': 2}, 'summary count drift')
    require(changed == summary['changed_records'], 'changed provenance records drift')
    require(digest(canonical(provenance)) == summary['ordered_complete_provenance_sha256'], 'ordered complete provenance drift')
    require(digest(pretty) == summary['original_full_table_sha256']
            and len(pretty) == summary['original_full_table_bytes'], 'original full table reconstruction drift')
    print(json.dumps({'result': 'PASS', 'counts': summary['counts'],
                      'ordered_complete_provenance_sha256': digest(canonical(provenance)),
                      'original_full_table_sha256': digest(pretty)}, sort_keys=True))


if __name__ == '__main__':
    main()
