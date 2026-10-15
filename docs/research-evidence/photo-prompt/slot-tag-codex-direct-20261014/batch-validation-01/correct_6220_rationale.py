"""Root-requested explanation-only correction, retaining exact prior evidence."""
import json
import run as batch
batch.local_installation()
import audit_composed_prompt as audit
P=batch.OUT/'native6220-adoption-01';OLD=batch.OUT/'native6220-adoption-02';O=batch.OUT/'native6220-adoption-03';O.mkdir(exist_ok=False)
pack=batch.c.decode((P/'CANDIDATE-PACK.json').read_bytes());receipt=batch.c.decode((P/'ISSUED-RECEIPT.json').read_bytes())
before=batch.c.decode((OLD/'COMPOSED.json').read_bytes());after=batch.c.decode((OLD/'COMPOSED.json').read_bytes())
previous=after['semantic_clarification_decisions'][0]['rationale']
assert previous=='Preserve the frozen cup scene and decline optional interpretation.'
correct='Preserve the same existing whole image and its continuous contours/readable small surface details; decline unrelated optional interpretation.'
after['semantic_clarification_decisions'][0]['rationale']=correct
report=audit.audit_composed_prompt(pack,after,runtime_receipt=receipt,runtime_store=batch.OUT/'research-runtime-store')
for name,value in [('COMPOSED.json',after),('COMPOSE-AUDIT.json',report),('VERIFICATION.json',{
    'schema':'photo-root-reviewed-controlled6220-adoption/v3','source102_checkpoint':True,'native_adoptions':1,
    'candidate_id':'cand_afdb9168ea8c53ad921a8574ed5248d1','issued_receipt_replayed':True,
    'same_pack_receipt_core_prompt_and_selection':True,'pack_sha256':batch.c.digest(pack),'receipt_sha256':batch.c.digest(receipt),
    'previous_composed_sha256':batch.c.digest(before),'next_composed_sha256':batch.c.digest(after),
    'exact_only_change':{'pointer':'/semantic_clarification_decisions/0/rationale','before':previous,'after':correct},
    'compose_status':report['status'],'quality_status':report.get('quality_status'),'failures':report['failures'],'warnings':report.get('warnings',[]),
    'root_requested_explanation_correction':True,'previous02_preserved':True,'fresh_model_or_query_inputs':0,
    'native_source_approvals_created':0,'production_native_qualified_count':0,'operating_changes':0,'Gemini_calls':0,
    'image_quality_or_real_request_truth_proven':False})]:
    with (O/name).open('xb') as stream:stream.write(batch.c.canonical_bytes(value)+b'\n')
assert report['status']=='pass',report
print(json.dumps({'compose':report['status'],'quality':report.get('quality_status'),'warnings':len(report.get('warnings',[]))}),flush=True)
