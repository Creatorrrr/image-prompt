"""Mechanical immutable snapshots only; no semantic modes/roles/owners authored."""
import copy, hashlib, json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
GEN=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sys.path.insert(0,str(GEN/'scripts'))
import photo_candidate_corpus
import photo_semantic_evidence as ne
assert Path(ne.__file__).resolve()==GEN/'scripts/photo_semantic_evidence.py'
assert hashlib.sha256(Path(ne.__file__).read_bytes()).hexdigest()=='6833e00c03ee4aa1222ea1a9e7c5304d8a98d62ad1d3d0e3ff6a3d666bb313e9'
sys.path.insert(0,str(R))
import direct_review as dr
source = dr.source()
order = json.loads((R/'ORDER.json').read_text())
catalog = json.loads((R/'CATALOG-FINAL-149-V6.json').read_text())
assert dr.c.digest(catalog) == 'd9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
compiled, locators = {}, {}
for path in sorted((R/'decisions').glob('*.json')):
    raw = path.read_bytes()
    for item, row in enumerate(json.loads(raw)['decisions'], 1):
        cid = row['candidate_id']
        assert cid not in compiled
        compiled[cid] = row
        locators[cid] = dict(file=str(path.relative_to(dr.ROOT)), item=item,
            file_sha256=hashlib.sha256(raw).hexdigest(), row_sha256=dr.c.digest(row))
after = {}
for cid, before in source['candidates'].items():
    decision = compiled[cid]
    record = dr.corrected_record(before, decision['corrections'])
    record['record_kind'] = decision['recommended_kind']
    after[cid] = record
corpus = {**source, 'candidates': after}
records = []
for ordinal in range(6150, 6200):
    cid = order[ordinal]
    refs = ne.referenced_records(after[cid], corpus)
    records.append(dict(ordinal=ordinal, candidate_id=cid,
        source_before=source['candidates'][cid], after_existing5B=after[cid],
        before_full_record_sha256=dr.c.digest(source['candidates'][cid]),
        after_full_record_sha256=dr.c.digest(after[cid]),
        registered5B=compiled[cid], original_compiled_locator=locators[cid],
        required_reference_records={key:dict(source_before=source['candidates'][key],
            after_existing5B=after[key], registered5B=compiled[key],
            original_compiled_locator=locators[key]) for key in refs if dr.c.ID.fullmatch(key)},
        explicit_reference_bindings={key:source['slot_bindings'][key] for key in refs if dr.c.BINDING_ID.fullmatch(key)},
        own_existing_bindings={key:row for key,row in source['slot_bindings'].items() if row['candidate_id']==cid}))
doc = dict(schema='native-source-fact-draft-read-packet/v1', task='/root/review_05250_06250',
    model='gpt-6.1-sol', reasoning_effort='high', assigned_range=[5250,6250],
    packet_range=[6150,6200], prepared_count=50, actual_read_count=0, prepared_only=True,
    formal_root_input_assignment_pending=True, source_sha256=dr.c.digest(source),
    final149V6_sha256=dr.c.digest(catalog), records=records)
path=R/'authored/native_05250_05250_06250.06150_06200.packet.json'
with path.open('x') as out: out.write(json.dumps(doc, ensure_ascii=False, separators=(',',':'))+'\n')
print(json.dumps(dict(path=str(path.relative_to(R)), byte_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    prepared_only=50, actual_read_count=0, compiled_count=len(compiled),
    sizes=[(row['ordinal'],len(json.dumps(row['after_existing5B'],ensure_ascii=False)),len(row['required_reference_records']),len(row['explicit_reference_bindings']),len(row['own_existing_bindings'])) for row in records])))
