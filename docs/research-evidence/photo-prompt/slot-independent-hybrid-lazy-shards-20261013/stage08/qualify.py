"""Offline full-scan qualification; no runtime dependency on this evaluator."""
from pathlib import Path
import copy,hashlib,json,resource,statistics,sys,time,multiprocessing
from concurrent.futures import ProcessPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
import prompt_generator as g,photo_candidate_corpus as c,photo_global_index as idx
import photo_slot_queries as q,photo_sharded_search as search,photo_global_retrieval as guard
import photo_slot_retrieval as slots,photo_native_pack as native,audit_global_retrieval as audit
from photo_search_reader import SearchReader,LazyRuntimeData
from photo_embedding_provider import load_env
from bm25f_retrieval import reciprocal_rank_fusion
from tests.photo_slot_oracle import full_scan,PreparedFullScan
R=Path(__file__).parent;A=ROOT/'skills/photo-prompt-image-generator/assets'
INPUTS=ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs'
CACHE=Path.home()/'.cache/image-prompt/photo-shared-runtime/query-embeddings'

def load_case(path):
 controls=json.loads((path/'creative-controls.json').read_text())
 core=g.load_authorial_core_arg(path/'authorial-core.json',request_envelope=g.load_request_envelope_arg(path/'request-envelope.json'),creative_control_snapshot=controls)
 return core,controls,json.loads((path/'embodiment-review.json').read_text())

def write(name,value):(R/name).write_bytes(c.canonical_bytes(value))

start=time.perf_counter();source=c.load(A);vectors=idx.load(A,source);lexical=idx.lexical(source);oracle=PreparedFullScan(lexical,vectors['entries'])
reader=SearchReader(A);core,controls,emb=load_case(INPUTS/'dev-02-blue-cup-en');data=LazyRuntimeData(reader).for_core(core)
allowed,bindings,contract=guard.eligible(data,core,controls);reports=[]
full_bytes=sum(row['bytes'] for row in reader.meta['vector_shards']);queries={}
for language in ('en','ko'):
 queries[language]=json.loads((R/f'QUERY-SET-{language}.json').read_text());q.validate_set(queries[language],core,controls,data['slot_catalog'],data['slot_catalog'])

def matrix_one(pair):
 slot,language=pair;row=queries[language]['slots'][slot]
 fields=row['binding']['query_fields'];before=dict(reader.metrics);t=time.perf_counter()
 lh=search.lexical_rank(reader,fields,allowed);vh,proof=search.cosine_rank(reader,row['vector'],allowed);seconds=time.perf_counter()-t
 actual={'bm25f':lh,'embedding':vh,'rrf':reciprocal_rank_fusion([[v['document_id'] for v in lh],[v['document_id'] for v in vh]],k=30)}
 io={k:reader.metrics[k]-before[k] for k in ('read_bytes','reads','vector_reads','vector_bytes','posting_reads','payload_reads')}
 expected=oracle.rank(fields,row['vector'],allowed)
 if actual!=expected:raise AssertionError('full-scan mismatch '+slot+' '+language)
 search.audit_cosine(reader,row['vector'],allowed,vh,proof)
 return ({'slot':slot,'language':language,'query_sha256':row['text_sha256'],'lane_sha256':c.digest(actual),'exact_equal':True,'pruning_proof_sha256':c.digest(proof),'visited_vector_shards':len(proof['visited_leaves']),'total_vector_shards':len(reader.meta['vector_shards']),'logical_vector_bytes':sum(reader.meta['vector_shards'][i]['bytes'] for i in proof['visited_leaves']),'logical_vector_byte_reduction':1-sum(reader.meta['vector_shards'][i]['bytes'] for i in proof['visited_leaves'])/full_bytes,'search_seconds':seconds,'io':io,'top5':[{'id':v['document_id'],'definition':(c.entry(source,v['document_id']).get('en') or c.entry(source,v['document_id']).get('definition') or (c.entry(source,v['document_id']).get('semantics') or {}).get('definition') or '')[:400]} for v in actual['rrf'][:5]],'cache_peak_bytes':reader.metrics['cache_peak_bytes']})

progress=R/'MATRIX-progress.json'
reports=json.loads(progress.read_text()) if progress.exists() else []
seen={(r['slot'],r['language']) for r in reports}
jobs=[(slot,language) for language in ('en','ko') for slot in sorted(queries[language]['slots']) if (slot,language) not in seen]
with ProcessPoolExecutor(max_workers=4,mp_context=multiprocessing.get_context('fork')) as pool:
 for future in as_completed([pool.submit(matrix_one,pair) for pair in jobs]):
  reports.append(future.result());write('MATRIX-progress.json',reports)
  if len(reports)%8==0:print(json.dumps({'matrix':len(reports),'total':224,'seconds':time.perf_counter()-start,'evaluation_workers':4}),flush=True)
reports.sort(key=lambda r:(r['language'],r['slot']))
write('MATRIX.json',reports)
# The unaccelerated original full scan remains the fixed latency comparator.
performance=[]
for slot,language in [('lighting','en'),('light_direction','ko'),('material','en'),('occasion_context','ko'),('color','en'),('body_pose','ko')]:
 row=queries[language]['slots'][slot];fields=row['binding']['query_fields'];t=time.perf_counter();expected=full_scan(lexical,vectors['entries'],fields,row['vector'],allowed);full_s=time.perf_counter()-t
 cold=SearchReader(A);t=time.perf_counter();lh=search.lexical_rank(cold,fields,allowed);vh,proof=search.cosine_rank(cold,row['vector'],allowed);lazy_s=time.perf_counter()-t
 if lh!=expected['bm25f'] or vh!=expected['embedding']:raise AssertionError('comparator mismatch')
 t=time.perf_counter();search.lexical_rank(cold,fields,allowed);search.cosine_rank(cold,row['vector'],allowed);warm_s=time.perf_counter()-t
 performance.append({'slot':slot,'language':language,'full_scan_seconds':full_s,'lazy_cold_search_seconds':lazy_s,'lazy_warm_search_seconds':warm_s,'cold_ratio':lazy_s/full_s,'warm_ratio':warm_s/full_s,'reader_startup_included':False,'vector_bytes':cold.metrics['vector_bytes'],'cache_peak_bytes':cold.metrics['cache_peak_bytes'],'visited_fraction':len(proof['visited_leaves'])/len(cold.meta['vector_shards'])})
 print(json.dumps({'performance':len(performance),'ratio':lazy_s/full_s}),flush=True)
write('PERFORMANCE.json',performance)
# Complete 112-slot execution and fair allocation, for both actual query sets.
for language in ('en','ko'):
 existing=R/('ALL-SLOTS-'+language+'.json')
 if existing.exists() and json.loads(existing.read_text())['pack']['global_retrieval']['index_sha256']==c.digest(reader.manifest):continue
 t=time.perf_counter();roles,binding,_=slots.retrieve(data,core,controls,queries[language],requested_slots=list(data['slot_catalog']),language=language)
 pack=native.finalize(native.WorkingPack({'global_retrieval':binding,'authorial_core':core,'creative_controls':controls},roles),data,binding['selected_candidate_ids'],queries[language])
 failures=audit.audit(pack,data,queries[language])
 if failures:raise AssertionError(failures)
 write('ALL-SLOTS-'+language+'.json',{'pack':pack,'seconds':time.perf_counter()-t,'status_counts':{state:sum(r['status']==state for r in roles.values()) for state in ('available','blocked','no_hits','budget_excluded','budget_partial')},'pool_size':len(pack['candidate_pool']),'role_refs':sum(len(r['candidate_refs']) for r in pack['role_views'].values()),'audit_failures':failures})
 print(json.dumps({'all_slots':language,'seconds':time.perf_counter()-t}),flush=True)
# All 20 frozen natural requests use fresh independent query sets, never old core vectors.
load_env(ROOT/'.env');natural=[];planned=0;paths=sorted(p for p in INPUTS.iterdir() if p.is_dir())
# Provider concurrency is four, before evaluation processes are forked.
for path in paths:
 nc,ncontrols,_=load_case(path);nd=LazyRuntimeData(reader).for_core(nc);active=slots.active_slots(nd,nc,ncontrols);planned+=len(active)
 out=R/'natural'/path.name;out.mkdir(parents=True,exist_ok=True);target=out/'query-context.json'
 if not target.exists():target.write_bytes(c.canonical_bytes(q.prepare(nc,ncontrols,nd['slot_catalog'],active,CACHE)))
 q.validate_set(json.loads(target.read_text()),nc,ncontrols,nd['slot_catalog'],active)
 print(json.dumps({'query_bank_case':path.name,'slots':len(active)}),flush=True)

def natural_one(path):
 core,controls,emb=load_case(path);data=LazyRuntimeData(reader).for_core(core);active=slots.active_slots(data,core,controls)
 context=json.loads((R/'natural'/path.name/'query-context.json').read_text())
 t=time.perf_counter();pack=g.generate_candidate_pack(data,core,controls,emb,seed=17,query_context=context)
 failures=audit.audit(pack,data,context)
 if failures:raise AssertionError(path.name+str(failures))
 # Recompute both lanes from source for each natural-query slot.
 allowed,_,_=guard.eligible(data,core,controls)
 for slot,trace in pack['global_retrieval']['slot_searches'].items():
  row=context['slots'][slot];expected=oracle.rank(row['binding']['query_fields'],row['vector'],allowed,limit=trace['lane_limit'])
  if expected['bm25f']!=trace['lanes']['bm25f']['ranks'] or expected['embedding']!=trace['lanes']['embedding']['ranks'] or expected['rrf']!=trace['rrf']:raise AssertionError(path.name+' '+slot)
 out=R/'natural'/path.name;out.mkdir(parents=True,exist_ok=True);(out/'query-context.json').write_bytes(c.canonical_bytes(context));(out/'pack.json').write_bytes(c.canonical_bytes(pack))
 required=pack.get('visual_obligations') or {};old=ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage07/packs'/f'{path.name}.json'
 oldpack=json.loads(old.read_text());oldpack=oldpack[0] if isinstance(oldpack,list) else oldpack;oldrequired=oldpack.get('visual_obligations') or {}
 preservation={k:required.get(k)==oldrequired.get(k) for k in ('obligations','required_hard_gates')}
 if not all(preservation.values()):raise AssertionError('hard obligation drift '+path.name)
 return ({'case':path.name,'slots':len(active),'new_provider_calls':sum(not r['cache_hit'] for r in context['slots'].values()),'provider_cache_hits':sum(r['cache_hit'] for r in context['slots'].values()),'seconds_local_search_audit_oracle':time.perf_counter()-t,'pack_sha256':c.digest(pack),'source_audit_failures':failures,'hard_obligation_preservation':preservation,'candidate_pool':len(pack['candidate_pool'])})


with ProcessPoolExecutor(max_workers=8,mp_context=multiprocessing.get_context('fork')) as pool:
 for future in as_completed([pool.submit(natural_one,path) for path in paths]):
  natural.append(future.result());write('NATURAL-progress.json',natural)
  print(json.dumps({'natural':len(natural),'case':natural[-1]['case'],'slots':natural[-1]['slots'],'evaluation_workers':8}),flush=True)
natural.sort(key=lambda r:r['case'])
write('NATURAL.json',natural)
summary={'matrix_queries':len(reports),'exact_rank_differences':0,'natural_requests':len(natural),'natural_slot_queries':planned,'new_provider_calls':224+sum(r['new_provider_calls'] for r in natural),'document_embedding_calls':0,'image_calls':0,'layout_id':reader.manifest['layout_id'],'corpus_sha256':reader.meta['corpus_sha256'],'metadata_bytes':reader.manifest['metadata']['bytes'],'median_logical_vector_byte_reduction':statistics.median(r['logical_vector_byte_reduction'] for r in reports),'strict_subset_fraction':sum(r['visited_vector_shards']<r['total_vector_shards'] for r in reports)/len(reports),'max_cold_latency_ratio':max(r['cold_ratio'] for r in performance),'cache_peak_bytes':reader.metrics['cache_peak_bytes'],'peak_rss_bytes_including_offline_oracle':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'seconds':time.perf_counter()-start}
write('QUALIFICATION.json',summary);print(json.dumps(summary),flush=True)
