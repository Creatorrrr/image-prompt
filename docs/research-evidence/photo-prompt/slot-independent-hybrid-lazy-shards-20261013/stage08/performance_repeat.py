"""Reader-cold/warm repeats; OS file cache is not forcibly cleared."""
from pathlib import Path
import gc,json,statistics,sys,time
ROOT=Path(__file__).resolve().parents[5];sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
import photo_candidate_corpus as c,photo_global_index as idx,photo_global_retrieval as guard,photo_sharded_search as search,prompt_generator as g
from photo_search_reader import SearchReader,LazyRuntimeData
from tests.photo_slot_oracle import full_scan
R=Path(__file__).parent;A=ROOT/'skills/photo-prompt-image-generator/assets';I=ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/dev-02-blue-cup-en'
source=c.load(A);vectors=idx.load(A,source);lexical=idx.lexical(source);controls=json.loads((I/'creative-controls.json').read_text());core=g.load_authorial_core_arg(I/'authorial-core.json',request_envelope=g.load_request_envelope_arg(I/'request-envelope.json'),creative_control_snapshot=controls)
base=SearchReader(A);allowed=guard.eligible(LazyRuntimeData(base).for_core(core),core,controls)[0];contexts={lang:json.loads((R/f'QUERY-SET-{lang}.json').read_text()) for lang in ('en','ko')};report=[]
for slot,lang in [('lighting','en'),('light_direction','ko'),('material','en'),('occasion_context','ko'),('color','en'),('body_pose','ko')]:
 row=contexts[lang]['slots'][slot];fields=row['binding']['query_fields'];trials=[]
 for repeat in range(3):
  t=time.perf_counter();expected=full_scan(lexical,vectors['entries'],fields,row['vector'],allowed);full_s=time.perf_counter()-t
  reader=SearchReader(A);t=time.perf_counter();lh=search.lexical_rank(reader,fields,allowed);vh,proof=search.cosine_rank(reader,row['vector'],allowed);cold_s=time.perf_counter()-t
  assert lh==expected['bm25f'] and vh==expected['embedding']
  t=time.perf_counter();search.lexical_rank(reader,fields,allowed);search.cosine_rank(reader,row['vector'],allowed);warm_s=time.perf_counter()-t
  trials.append({'full_scan_seconds':full_s,'reader_cold_search_seconds':cold_s,'reader_warm_search_seconds':warm_s,'cache_peak_bytes':reader.metrics['cache_peak_bytes']});reader.close();del reader;gc.collect()
 median=lambda key:statistics.median(r[key] for r in trials)
 report.append({'slot':slot,'language':lang,'trials':trials,'cold_ratio':median('reader_cold_search_seconds')/median('full_scan_seconds'),'warm_ratio':median('reader_warm_search_seconds')/median('full_scan_seconds')})
 print(json.dumps({'case':slot,'median_cold_ratio':report[-1]['cold_ratio']}),flush=True)
(R/'PERFORMANCE-REPEATED.json').write_bytes(c.canonical_bytes({'procedure':'three trials, medians per query; fresh empty Reader each cold trial; OS cache not cleared; metadata/startup and API time excluded from both search timers','implementation':'operator.getitem map preserves the identical math.fsum input sequence','cases':report,'max_median_cold_ratio':max(r['cold_ratio'] for r in report),'gate':1.2,'pass':all(r['cold_ratio']<=1.2 for r in report)}))
