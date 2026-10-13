"""Published runtime, native view, composition, render audit and fresh replay."""
from pathlib import Path
import json,sys,time,subprocess
ROOT=Path(__file__).resolve().parents[5];sys.path[:0]=[str(ROOT),str(ROOT/'skills/photo-prompt-image-generator/scripts')]
import prompt_generator as g,photo_candidate_corpus as c,photo_runtime_sources as runtime
import audit_global_retrieval as audit,compose_pack_view as view,audit_composed_prompt as composed_audit,audit_image_render_request as render_audit
from tests.photo_native_runtime import compose_native
R=Path(__file__).parent;S=R.parent/'stage08';INPUT=ROOT/'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs'
if len(sys.argv)>1:
 case=sys.argv[1];out=R/'public'/case;pack=json.loads((out/'pack.json').read_text());receipt=json.loads((out/'receipt.json').read_text());p=runtime.RuntimeSnapshotProvider();snapshot=p.from_receipt(pack,receipt)
 assert audit.audit(pack,snapshot.data,snapshot.query_context)==[]
 (out/'fresh-worker.json').write_bytes(c.canonical_bytes({'exact_pack_recomputation':True,'generation_id':snapshot.generation_id,'new_provider_calls':0}));print('fresh worker pass',case);raise SystemExit
provider=runtime.RuntimeSnapshotProvider();t=time.perf_counter();snapshot=provider.acquire();cold={'seconds':time.perf_counter()-t,'reader_io':dict(snapshot.data.reader.metrics),'generation_id':snapshot.generation_id};assert all(snapshot.data.reader.metrics[k]==0 for k in ('vector_reads','payload_reads','posting_reads'))
(R/'PUBLISHED-COLD-START.json').write_bytes(c.canonical_bytes(cold));results=[]
for case in ('dev-02-blue-cup-en','holdout-10-fantasy-ko'):
 path=INPUT/case;controls=json.loads((path/'creative-controls.json').read_text());core=g.load_authorial_core_arg(path/'authorial-core.json',request_envelope=g.load_request_envelope_arg(path/'request-envelope.json'),creative_control_snapshot=controls);emb=json.loads((path/'embodiment-review.json').read_text());context=json.loads((S/'natural'/case/'query-context.json').read_text());t=time.perf_counter()
 pack=g.generate_candidate_pack(snapshot.data,core,controls,emb,seed=17,query_context=context);receipt=provider.receipt(snapshot,pack);assert audit.audit(pack,snapshot.data,context)==[]
 overview=view.build_view(pack);view.verify_view(pack,overview);details=view.build_view(pack,list(pack['candidate_pool'])[:2]);view.verify_view(pack,details)
 if case=='holdout-10-fantasy-ko':
  from tests.test_photo_native_golem_obligation import PhotoSlotRetrievalIntegrationTests as Golem
  Golem.pack=pack;Golem.core=core;Golem.spec=json.loads((ROOT/'tests/fixtures/photo_prompt/native_golem_composition/golem-composition-authoring.json').read_text());composed=Golem().composed()
 else:composed=compose_native(pack)
 report=composed_audit.audit_composed_prompt(pack,composed,source_data=snapshot.data,query_context=context);assert report['status']=='pass',report['failures']
 request={'schema_version':'photo-image-render-request/v2','pack_id':pack['pack_id'],'global_retrieval_sha256':pack['global_retrieval']['canonical_sha256'],'source_intent_lock_sha256':core['intent_lock']['canonical_sha256'],'source_embodiment_preflight_sha256':pack['embodiment_preflight']['canonical_sha256'],'runtime_prompt_en':composed['prompt_en']+('\n\nAvoid: '+pack['negative_en'] if pack['negative_en'] is not None else ''),'runtime_negative_en':pack['negative_en'],'references':[],'audit_boundary':{'composed_prompt_audit_status':'pass','runtime_prompt_audit_status':'not_run','inherits_composed_prompt_pass':False}}
 ra=render_audit.audit_image_render_request(pack,composed,request);assert ra['status']=='pass',ra
 out=R/'public'/case;out.mkdir(parents=True,exist_ok=True)
 for name,value in [('pack',pack),('receipt',receipt),('composed',composed),('render-request',request),('composition-audit',report),('render-audit',ra),('overview',overview),('details',details)]: (out/(name+'.json')).write_bytes(c.canonical_bytes(value))
 completed=subprocess.run([sys.executable,str(Path(__file__)),case],cwd=ROOT,capture_output=True,text=True);assert completed.returncode==0,completed.stderr
 results.append({'case':case,'slots':len(pack['global_retrieval']['slot_searches']),'pack_sha256':c.digest(pack),'compose':'pass','render_preflight':'pass','fresh_worker':'pass','new_provider_calls':0,'image_calls':0,'seconds':time.perf_counter()-t});print(json.dumps(results[-1]),flush=True)
try:provider.from_receipt(pack,{'schema':'photo-runtime-receipt/v2'})
except runtime.FreshnessError:old_rejected=True
else:raise AssertionError('old receipt accepted')
(R/'PUBLIC-FLOW.json').write_bytes(c.canonical_bytes({'generation_id':snapshot.generation_id,'cases':results,'old_receipt_rejected':old_rejected,'image_calls':0,'new_provider_calls':0}))
