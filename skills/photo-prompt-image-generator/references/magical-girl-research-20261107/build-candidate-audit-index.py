#!/usr/bin/env python3
"""Build a reproducible source inventory; this is not semantic candidate review."""
import collections, gzip, hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1]
ASSETS = SKILL / 'assets'
manifest_path = ASSETS / 'photo_candidate_corpus_manifest.json'
manifest_raw = manifest_path.read_bytes()
manifest = json.loads(manifest_raw)
lead_rows = [json.loads(s) for s in (HERE / 'candidate-discovery-all.jsonl').read_text().splitlines()]
lead_index = collections.defaultdict(list)
for row in lead_rows:
    for hit in row['hits']:
        lead_index[(hit['module'], hit['candidate_id'])].append(row['term_id'])
bindings = collections.defaultdict(list)
for mod in manifest['modules']:
    if mod.get('kind') != 'slot_bindings':
        continue
    data = json.loads((ASSETS / mod['file']).read_text())
    for bid, rec in data['slot_bindings'].items():
        bindings[rec['candidate_id']].append({'module': mod['file'], 'binding_id': bid})
seen = set()
counts = collections.Counter()
output_path = HERE / 'candidate-corpus-audit-index.jsonl.gz'
with output_path.open('wb') as raw:
    with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=9) as out:
        for mod in manifest['modules']:
            if mod.get('kind') != 'candidates':
                continue
            counts['candidate_modules'] += 1
            for cid, rec in json.loads((ASSETS / mod['file']).read_text())['candidates'].items():
                key = (mod['file'], cid)
                if key in seen or rec.get('id') != cid:
                    raise ValueError(f'duplicate key or id mismatch: {key}')
                seen.add(key)
                canon = json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
                content = rec.get('content', {})
                obj = {'module': mod['file'], 'candidate_id': cid,
                       'whole_record_sha256': hashlib.sha256(canon).hexdigest(),
                       'record_kind': rec.get('record_kind'),
                       'conditions': rec.get('conditions', {}), 'effects': rec.get('effects', {}),
                       'content_field_names': sorted(content),
                       'binding_refs': bindings.get(cid, []),
                       'lexical_lead_row_ids': lead_index.get(key, []),
                       'semantic_review': 'not_implied_by_index'}
                out.write((json.dumps(obj, ensure_ascii=False, separators=(',', ':'))+'\n').encode())
                counts['candidate_records'] += 1
                counts['records_with_lexical_leads'] += bool(obj['lexical_lead_row_ids'])
missing = set(lead_index) - seen
if missing:
    raise ValueError(f'{len(missing)} lexical lead keys not present in current manifest')
meta = {'schema':'magical-girl-candidate-audit-index/v1',
        'manifest_sha256':hashlib.sha256(manifest_raw).hexdigest(),
        'lexical_discovery_sha256':hashlib.sha256((HERE/'candidate-discovery-all.jsonl').read_bytes()).hexdigest(),
        'index_sha256':hashlib.sha256(output_path.read_bytes()).hexdigest(),
        'counts':dict(counts),
        'scope':'All manifest candidate records; bindings indexed by candidate ID. Conditions and effects copied; complete content/activation/contracts remain in the cited source module. This inventory does not establish semantic review, candidate relevance, runtime installation, or image quality.'}
(HERE/'candidate-corpus-audit-index.meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(meta, ensure_ascii=False, indent=2))
