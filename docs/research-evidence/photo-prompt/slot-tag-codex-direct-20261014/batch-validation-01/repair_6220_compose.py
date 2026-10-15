"""Add the omitted literal whole-image relation evidence; keep failed attempt."""
import hashlib,json
import run as batch
batch.local_installation()
import audit_composed_prompt as audit
P=batch.OUT/'native6220-adoption-01';O=batch.OUT/'native6220-adoption-02';O.mkdir(exist_ok=False)
read=lambda name:batch.c.decode((P/name).read_bytes())
pack=read('CANDIDATE-PACK.json');receipt=read('ISSUED-RECEIPT.json');composed=read('COMPOSED.json')
cid='cand_afdb9168ea8c53ad921a8574ed5248d1'
phrase='Clean, continuous photographic edges, with continuous object contours and readable small surface details preserved on the same whole image.'
rows=[*composed['candidate_interpretations'],*[r for r in composed['creative_augmentation_brief']['decisions'] if r.get('decision')=='transformed']]
row=next(r for r in rows if r['candidate_id']==cid)
assert row['prompt_evidence']==phrase and phrase in composed['prompt_en']
row['relation_evidence']={'effect_owner':phrase}
report=audit.audit_composed_prompt(pack,composed,runtime_receipt=receipt,runtime_store=batch.OUT/'research-runtime-store')
for name,value in [('COMPOSED.json',composed),('COMPOSE-AUDIT.json',report),('VERIFICATION.json',{
    'schema':'photo-root-reviewed-controlled6220-adoption/v2','source102_checkpoint':True,
    'candidate_id':cid,'native_adoptions':1,'issued_receipt_replayed':True,'compose_status':report['status'],
    'failures':report['failures'],'correction':'Add exact effect_owner whole-image relation evidence using the unchanged root-approved final phrase. No prompt/core/source/proof/effect/owner change.',
    'previous_failed_attempt':'native6220-adoption-01/COMPOSE-AUDIT.json',
    'unchanged_public_pack_sha256':batch.c.digest(pack),'unchanged_issued_receipt_sha256':batch.c.digest(receipt),
    'root_core_review':'native6220-proposal-04/ROOT-CORE-REVIEW.json',
    'source_proof_native_approvals_created':0,'production_native_qualified_count':0,'operating_changes':0,
    'new_model_or_embedding_inputs':0,'Gemini_calls':0,'pixels_or_independent_real_request_proven':False})]:
    with (O/name).open('xb') as stream:stream.write(batch.c.canonical_bytes(value)+b'\n')
assert report['status']=='pass',report
print(json.dumps({'candidate_id':cid,'compose':report['status'],'receipt_replayed':True}),flush=True)
