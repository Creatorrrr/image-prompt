"""Mechanical immutable snapshots only; no semantic modes/roles/owners authored."""
import copy, hashlib, json, sys
from pathlib import Path
R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R))
import direct_review as dr
import photo_semantic_evidence as ne
source = dr.source()
order = json.loads((R/'ORDER.json').read_text())
catalog = json.loads((R/'CATALOG-FINAL-142-V2.json').read_text())
assert dr.c.digest(catalog) == '0d7cab7b4add7279b0faa629bb5df72829da0c756adc6db21dcd7c09d56b971f'
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
for ordinal in range(5350, 5400):
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
    packet_range=[5350,5400], prepared_count=50, actual_read_count=0, prepared_only=True,
    formal_root_input_assignment_pending=True, source_sha256=dr.c.digest(source),
    final142V2_sha256=dr.c.digest(catalog), records=records)
path=R/'authored/native_05250_05250_06250.05350_05400.packet.json'
with path.open('x') as out: out.write(json.dumps(doc, ensure_ascii=False, separators=(',',':'))+'\n')
print(json.dumps(dict(path=str(path.relative_to(R)), byte_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
    prepared_only=50, actual_read_count=0, compiled_count=len(compiled),
    sizes=[(row['ordinal'],len(json.dumps(row['after_existing5B'],ensure_ascii=False)),len(row['required_reference_records']),len(row['explicit_reference_bindings']),len(row['own_existing_bindings'])) for row in records])))
