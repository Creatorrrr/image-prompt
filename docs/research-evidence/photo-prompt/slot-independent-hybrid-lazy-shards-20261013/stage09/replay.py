"""Post-removal actual-context replay against the independently qualified ranks."""
from pathlib import Path
import json,sys,time,multiprocessing,resource
from concurrent.futures import ProcessPoolExecutor,as_completed
ROOT=Path(__file__).resolve().parents[5];sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
import photo_candidate_corpus as c,photo_global_retrieval as guards,photo_sharded_search as search,prompt_generator as g
from photo_search_reader import SearchReader,LazyRuntimeData
from bm25f_retrieval import reciprocal_rank_fusion
R=Path(__file__).parent;S=R.parent/'stage08';A=ROOT/'skills/photo-prompt-image-generator/assets';I=ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en'
controls=json.loads((I/'creative-controls.json').read_text());core=g.load_authorial_core_arg(I/'authorial-core.json',request_envelope=g.load_request_envelope_arg(I/'request-envelope.json'),creative_control_snapshot=controls)
reader=SearchReader(A);allowed=guards.eligible(LazyRuntimeData(reader).for_core(core),core,controls)[0];contexts={lang:json.loads((S/f'QUERY-SET-{lang}.json').read_text()) for lang in ('en','ko')};expected={(v['slot'],v['language']):v['lane_sha256'] for v in json.loads((S/'MATRIX.json').read_text())}
def one(pair):
 slot,lang=pair;row=contexts[lang]['slots'][slot];lh=search.lexical_rank(reader,row['binding']['query_fields'],allowed);vh,proof=search.cosine_rank(reader,row['vector'],allowed)
 actual={'bm25f':lh,'embedding':vh,'rrf':reciprocal_rank_fusion([[v['document_id'] for v in lh],[v['document_id'] for v in vh]],k=30)}
 assert c.digest(actual)==expected[pair],pair
 search.audit_cosine(reader,row['vector'],allowed,vh,proof)
 return {'slot':slot,'language':lang,'exact':True,'lane_sha256':c.digest(actual),'cache_peak_bytes':reader.metrics['cache_peak_bytes']}
results=[];start=time.perf_counter()
with ProcessPoolExecutor(max_workers=4,mp_context=multiprocessing.get_context('fork')) as pool:
 for future in as_completed([pool.submit(one,pair) for pair in sorted(expected)]):
  results.append(future.result())
  if len(results)%16==0:print(json.dumps({'replayed':len(results),'total':224}),flush=True)
(R/'POST-REMOVAL-REPLAY.json').write_bytes(c.canonical_bytes({'queries':len(results),'rank_differences':0,'new_provider_calls':0,'layout_id':reader.manifest['layout_id'],'results':results,'seconds':time.perf_counter()-start}))
