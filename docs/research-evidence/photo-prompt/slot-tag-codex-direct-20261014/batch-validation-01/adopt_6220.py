"""Root-reviewed controlled native6220 adoption through the research generation."""
import copy,hashlib,json
from pathlib import Path
import run as batch
provider,space=batch.local_installation()
import prompt_generator as g
import photo_runtime_sources as runtime
import photo_slot_queries as queries
import audit_composed_prompt as audit

P=batch.OUT/'native6220-proposal-04';O=batch.OUT/'native6220-adoption-01';O.mkdir(exist_ok=False)
MESSAGE='native6220-proposal04 전체 normalized core/8assertions/request envelope/controls/embodiment 의미를 루트 검토했습니다. input의 반복부분은 normalized와 정확동일성으로 대조했고 차이는core/lock해시와표준request_binding·고정정책뿐입니다. controlled request 문장/P·PR 독립성, image role→image_A, other_A disjoint, style만open+두실제PR property anchor, baseline에clean_edges미포함이 적절하므로 이 exactproposal로 실제pack→issued receipt→6220 선택/adopt→finalcompose 검증 진행하세요. R에ROOT-CORE-REVIEW.json으로 이 메시지·exact6files hashes·정확범위를 보존. 주의finalprompt는rootproposed추가구절과core기존의미를 모두보존; 독립실제사용자/픽셀증명아님. source102checkpoint명시 유지.'
pins={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(P.glob('*.json'))};assert len(pins)==6
review={'schema':'photo-controlled-core-root-review/v1','reviewer':'/root','received_authorization_message':MESSAGE,
    'exact_six_files':pins,'scope':'Exact controlled proposal04 only, source102 research generation. No operating adoption, independent human acceptance or pixel truth.'}
review_path=P/'ROOT-CORE-REVIEW.json'
with review_path.open('xb') as stream:stream.write(batch.c.canonical_bytes(review)+b'\n')
def save(name,value):
    with (O/name).open('xb') as stream:stream.write(batch.c.canonical_bytes(value)+b'\n')
read=lambda name:batch.c.decode((P/name).read_bytes())
core=read('AUTHORIAL-CORE-NORMALIZED.json');controls=read('CREATIVE-CONTROLS.json');embodiment=read('EMBODIMENT-REVIEW.json')
verified=g.load_authorial_core_arg(str(P/'AUTHORIAL-CORE-INPUT.json'),request_envelope=read('REQUEST-ENVELOPE.json'),creative_control_snapshot=controls)
assert batch.c.digest(verified)==batch.c.digest(core)
runtime_provider=runtime.RuntimeSnapshotProvider(batch.OUT,batch.OUT/'research-runtime-store')
snapshot=runtime_provider.acquire()
assert snapshot.manifest['search_layout']['corpus_sha256']=='db0875e12046787f59461a346f76a53fb9f6102089a98cd0b467f9813996f6b0'
context=queries.prepare(core,controls,snapshot.data['slot_catalog'],['image_detail'],O/'query-cache',space=space)
save('QUERY-CONTEXT.json',context)
pack=g.generate_candidate_pack(snapshot.data,core,controls,embodiment,query_context=context,requested_slots=['image_detail'])
save('CANDIDATE-PACK.json',pack)
receipt=runtime_provider.receipt(snapshot,pack);save('ISSUED-RECEIPT.json',receipt)
runtime_provider.from_receipt(pack,receipt)
inventory=batch.c.decode((batch.R/'ROOT-CURRENT149-APPROVAL-INVENTORY-01.json').read_bytes())
cid=next(r['candidate_id'] for r in inventory['records'] if r['ordinal']==6220)
if cid not in pack['candidate_pool']:
    save('NOT-PRESENTED.json',{'candidate_id':cid,'reason':'The unchanged standard retrieval/budgets did not present6220. No force insertion or adoption was performed.',
        'presented':list(pack['candidate_pool']),'receipt_replayed':True,'source102_checkpoint':True})
    raise RuntimeError('approved6220 not presented by actual standard retrieval')
composed=batch.composition(pack)
phrase=read('PROPOSAL-SCOPE.json')['final_addition_phrase_proposed_by_root']
composed['prompt_en']+=' '+phrase
composed['chosen_candidate_ids']=[cid]
interpretation={'candidate_id':cid,'realization_id':'base',
    'artistic_interpretation':'Refine the existing whole photographic image while preserving its independently continuous contours and readable small surface details.',
    'transformation':'Apply only the reviewed clean_edges image.detail effect to the same existing image_A without changing depicted physical objects.',
    'prompt_evidence':phrase,'affected_properties':[{'dimension':'style','target':'image_A','property':'image.detail'}]}
composed['candidate_interpretations']=[interpretation]
for decision in composed['creative_augmentation_brief']['decisions']:
    if decision['candidate_id']==cid:
        decision.update(interpretation,decision='transformed',rationale='Use the exact reviewed clean-edge detail refinement on the same image, retaining both original preservation properties.',affected_dimensions=['style'])
        composed['candidate_interpretations']=[]
composed['embodiment_review']['review']['prompt_sha256']=hashlib.sha256(composed['prompt_en'].encode()).hexdigest()
save('COMPOSED.json',composed)
report=audit.audit_composed_prompt(pack,composed,runtime_receipt=receipt,runtime_store=batch.OUT/'research-runtime-store')
save('COMPOSE-AUDIT.json',report)
save('VERIFICATION.json',{'schema':'photo-root-reviewed-controlled6220-adoption/v1','source102_checkpoint':True,
    'research_generation_id':snapshot.generation_id,'candidate_id':cid,'native_adoptions':1,
    'issued_receipt_replayed':True,'compose_status':report['status'],'failures':report['failures'],
    'root_complete_core_review_file':str(review_path),'root_complete_core_review_sha256':batch.c.digest(review),
    'existing_independent_image_owner_and_two_PR_preserved':True,'new_owners_or_physical_objects_authored':0,
    'local_queries':1,'Gemini_calls':0,'operating_changes':0,'operating_native_qualified_count':0,
    'independent_real_request_or_pixels_proven':False})
assert report['status']=='pass',report
print(json.dumps({'native_candidate':cid,'compose':report['status'],'receipt_replayed':True}),flush=True)
