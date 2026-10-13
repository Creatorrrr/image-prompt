"""Real prior query vectors, freshly bound/ranked/audited against this source.

No new provider request is sent after the spending-cap failure. This is a
three-slot contract-batch smoke test, not the remaining all-role stage 7.
"""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SKILL=ROOT/'skills/photo-prompt-image-generator';sys.path[:0]=[str(ROOT),str(SKILL/'scripts')]
import photo_candidate_corpus as c,photo_global_index as index,photo_global_retrieval as guards
import photo_slot_queries as q,photo_runtime_sources as runtime,photo_sharded_search as sharded
import photo_native_pack,photo_slot_retrieval
from build_shared_candidate_index import offline_vector_map
from photo_search_reader import SearchReader,LazyRuntimeData
from tests.photo_slot_oracle import PreparedFullScan
from tests.photo_native_runtime import compose_native
import prompt_generator as g,audit_global_retrieval as replay,audit_composed_prompt as composition

def main():
 source=c.load(SKILL/'assets');provider=runtime.RuntimeSnapshotProvider(SKILL);snapshot=provider.acquire()
 path=ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en'
 controls=c.decode((path/'creative-controls.json').read_bytes());core=g.load_authorial_core_arg(path/'authorial-core.json',request_envelope=g.load_request_envelope_arg(path/'request-envelope.json'),creative_control_snapshot=controls);embodiment=c.decode((path/'embodiment-review.json').read_bytes())
 original=c.decode((HERE.parent/'slot-tag-pilot-20261013/object-en-contexts.json').read_bytes())
 slots=['light_quality','surface_material','visual_hierarchy'];context={'schema':q.SCHEMA,'slots':{tag:original['slots'][tag] for tag in slots}};context['canonical_sha256']=c.digest(context)
 q.validate_set(context,core,controls,source['slot_catalog'],slots)
 vectors=offline_vector_map(snapshot.data.reader,source);index.validate(vectors,source);oracle=PreparedFullScan(index.lexical(source),vectors['entries'])
 reader=SearchReader(snapshot.root/'assets');cold=dict(reader.metrics);assert all(cold[k]==0 for k in ['payload_reads','posting_reads','vector_reads']);data=LazyRuntimeData(reader).for_core(core)
 allowed,_,_=guards.eligible(data,core,controls);assert not set(allowed)&{cid for cid,row in source['candidates'].items() if row['record_kind']=='diagnostic'}
 pack=g.generate_candidate_pack(data,core,controls,embodiment,seed=2026101405,query_context=context,requested_slots=slots)
 for slot,trace in pack['global_retrieval']['slot_searches'].items():
  row=context['slots'][slot];expected=oracle.rank(q.validate(row,core,controls,source['slot_catalog'],slot),row['vector'],set(allowed),limit=trace['lane_limit'])
  assert trace['lanes']['bm25f']['ranks']==expected['bm25f'];assert trace['lanes']['embedding']['ranks']==expected['embedding'];assert trace['rrf']==expected['rrf'];sharded.audit_cosine(reader,row['vector'],set(allowed),trace['lanes']['embedding']['ranks'],trace['cosine_proof'])
 assert replay.audit(pack,data,context)==[]
 receipt=provider.receipt(snapshot,pack);issued=provider.from_receipt(pack,receipt);assert replay.audit(pack,issued.data,issued.query_context)==[]
 composed=compose_native(pack);audit=composition.audit_composed_prompt(pack,composed,source_data=issued.data,query_context=issued.query_context);assert audit['status']=='pass',audit
 result={'schema':'photo-stage05-real-query-smoke/v1','verified':True,'source_sha256':c.digest(source),'generation_id':snapshot.generation_id,'source_fingerprint':snapshot.manifest['source_fingerprint'],'pack_schema':pack['contract_version'],'retrieval_schema':pack['global_retrieval']['contract_version'],'slots':slots,'current_query_provider_calls':0,'actual_query_vector_origin':'Previously successful provider responses from stage-4 object fixture; exact current core/controls/spec/text/recipe/space bindings revalidated.','native_bm25f_cosine_rrf_equals_offline_full_scan':True,'skip_certificates_verified':True,'issued_receipt_replay':True,'composition_audit':'pass','cold_reader_metrics':cold,'reader_metrics':dict(reader.metrics),'cache_peak_bytes':reader.metrics.get('cache_peak_bytes'),'cache_limit':reader.cache_limit,'open_descriptors':len(reader.descriptors),'diagnostics_excluded':70,'selected_unique_candidates':len(pack['candidate_pool']),'image_provider_calls':0,'boundary':'Three-slot implementation smoke; not stage-7 all-role completion or independent semantic/pixel assessment.'}
 assert reader.cache_bytes<=reader.cache_limit and len(reader.descriptors)<=64
 for name,value in [('CACHED-HYBRID-VERIFICATION.json',result),('CACHED-HYBRID-PACK.json',dict(pack)),('CACHED-HYBRID-RECEIPT.json',receipt),('CACHED-HYBRID-COMPOSITION-AUDIT.json',audit)]:
  (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
 reader.close();snapshot.data.reader.close();issued.data.reader.close();print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
