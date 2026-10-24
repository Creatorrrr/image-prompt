#!/usr/bin/env python3
"""Read-only corpus discovery using the repository's actual positive projection."""
from pathlib import Path
import hashlib
import json
import re
import sys
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import photo_global_index as projection

QUERIES = {
    'marine_specific': r'해병|팔각모|오도봉고|황근출|marine corps|eight.point.{0,12}cap',
    'military_uniform': r'군복|전투복|camouflage|combat uniform|military uniform|fatigues',
    'footwear': r'군화|전투화|combat boots|lace.up boots|suede boots',
    'nameplate': r'명찰|name.?tape|name.?plate|red name',
    'dog_tags': r'군번줄|dog tags|identity tags',
    'salute': r'경례|salut',
    'attention': r'차렷|standing at attention',
    'arms_crossed': r'팔짱|arms crossed|crossed arms|forearms cross',
    'hands_behind': r'뒷짐|등 뒤에 모은|hands behind.{0,10}back|hands are behind',
    'red_lowerwear': r'각개빤|red briefs|red boxer|red shorts',
    'van': r'승합차|봉고|red van|red minibus|passenger van',
    'wrench': r'몽키스패너|adjustable wrench|adjustable spanner',
    'tray': r'식판|meal tray|compartment.{0,20}tray',
    'barracks': r'내무반|생활관|관물함|barracks|storage locker',
    'containers': r'컨테이너|shipping container|container tower',
    'cap_shadow': r'모자챙|cap brim|hat brim|shadow.{0,25}face',
    'low_angle': r'로우앵글|low.angle',
    'graphic_lines': r'집중선|속도선|speed lines|focus lines',
}


def run():
    manifest = json.loads((ASSETS / 'photo_candidate_corpus_manifest.json').read_text())
    records, files, bindings, hashes = {}, {}, {}, {}
    for mod in manifest['modules']:
        path = ASSETS / mod['file']
        raw = path.read_bytes()
        hashes[mod['file']] = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw)
        for cid, record in data.get('candidates', {}).items():
            records[cid], files[cid] = record, mod['file']
        for binding in data.get('slot_bindings', {}).values():
            bindings.setdefault(binding['candidate_id'], []).append(binding)
    positive = {cid: r for cid, r in records.items() if r['record_kind'] in projection.POSITIVE_KINDS}
    blobs = {cid: ' '.join(s for values in projection.fields(r).values() for s in values) for cid, r in positive.items()}
    results = {}
    for key, expr in QUERIES.items():
        matches = [cid for cid, text in blobs.items() if re.search(expr, text, re.I)]
        results[key] = {
            'expression': expr, 'count': len(matches), 'ids': matches,
            'full_record_examples': [
                {'id': cid, 'file': files[cid], 'record': records[cid], 'bindings': bindings.get(cid, []),
                 'record_sha256': hashlib.sha256(json.dumps(records[cid], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()}
                for cid in matches[:16]
            ],
        }
    end_drift = [name for name, digest in hashes.items() if hashlib.sha256((ASSETS / name).read_bytes()).hexdigest() != digest]
    result = {
        'method': 'Read manifest modules, all record fields and bindings; discovery uses photo_global_index.fields positive projection and POSITIVE_KINDS. Lexical discovery only; not actual search or exhaustive semantic deduplication.',
        'candidate_count': len(records), 'positive_candidate_count': len(positive),
        'positive_record_kinds': sorted(projection.POSITIVE_KINDS),
        'module_hashes': hashes, 'source_drift_during_read': end_drift, 'queries': results,
    }
    (HERE / 'corpus-positive-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'candidates': len(records), 'positive': len(positive), 'queries': {k:v['count'] for k,v in results.items()}, 'source_drift': end_drift}, ensure_ascii=False))


if __name__ == '__main__':
    run()
