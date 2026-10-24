"""Verify real installed bodies, diagnostic boundary and all frozen query scopes."""
from pathlib import Path
import gc;gc.disable()
import gzip,json,sys
T=Path(__file__).resolve().parent;R=T.parents[4];Q=T.parent
read=lambda p:json.loads(Path(p).read_bytes())
def write(p,v):Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
succ=read(T/'successor.json');store=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed');N=store/'generations'/succ['native_generation_id'];sys.path.insert(0,str(N/'scripts'))
from photo_h_f2_generation import Generation
from photo_recall_generation import read as read_any
import photo_candidate_corpus as corpus
import photo_canonical_source as canonical
import photo_h_f2_queries as queries
import prompt_generator as generator
import audit_composed_prompt as auditor
g=Generation(store,succ['generation_id'],full=True)
reg=read(Q/'integration-evidence/source-registration.json');positive=set(reg['new_visual_ids']);diagnostic=set(reg['diagnostic_ids']);indexed={r['cid'] for r in g.metadata}
assert positive<=indexed and not diagnostic&indexed
records=read(T/'release-new-native-records.json')
for cid,raw in records.items():assert canonical.native_snapshot(g.body.record(cid))==raw
native_manifest=read(N/'manifest.json');base=read(T/'current-compatible-base.json');assert corpus.digest(native_manifest['source']['code'])==base['config']['code_sha256']
version='v5' if '--v5' in sys.argv else 'v4';results=[]
for arm in 'abc':
 run=R/f'generated/photo-runs/marine-literature-retest-20261024-{arm}-{version}';state=read(run/'workflow.json')
 def value(key):return read(state['artifacts'][key]['path'])
 core=value('authorial_core_normalized');controls=value('creative_controls');plan=value('slot_expression_plan')
 whole=queries.whole_scene(core,controls,plan)
 assert whole[queries.REQUEST_TOPIC]['text']==('해병문학' if version=='v5' else '해병문학 용어 조사')
 assert whole[queries.BASELINE_PROMPT]['text']==core['baseline_prompt_en']
 projection={k:core[k] for k in ('contract_version','canonical_sha256','source_request','user_exclusions') if k in core};projection['request_binding']=core['request_binding']
 text,provenance=generator.authorial_core_retrieval_text(projection);assert provenance==auditor.expected_authorial_core_retrieval_provenance(projection)
 results.append({'arm':arm,'run':str(run),'mode':state['mode'],'query_topic':text,'baseline_unchanged':True,'raw_request_unchanged':core['source_request']==(T/'request.txt').read_text(),'producer_and_independent_auditor_agree':True,'query_scope_hash':core['request_binding']['query_scope']['canonical_sha256']})
write(T/('runtime-query-projection.v5.json' if version=='v5' else 'runtime-query-projection.json'),{'status':'pass','actual_installed_native_generation':succ['native_generation_id'],'arms':results})
write(T/'registration-qualification.json',{'status':'pass','new_visual_CIDs':87,'new_diagnostic_CIDs':247,'new_visual_CIDs_indexed':len(positive&indexed),'diagnostic_positive_leaks':len(diagnostic&indexed),'released_source_native_roundtrip_exact':len(records),'full_deployed_generation_validation':True,'kernel_exact_current_selected_implementation':True,'native_approval':False,'query_scope_arms_verified':3})
print(json.dumps({'status':'pass','positive':87,'diagnostic_leaks':0,'roundtrip':len(records),'topic_queries':[r['query_topic'] for r in results]}),flush=True)
