import base64, collections, datetime, hashlib, json, shutil
from pathlib import Path

def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(name): return json.loads(Path('output/'+name).read_bytes())
def save(name,obj): Path('output/'+name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def sha(data): return hashlib.sha256(data).hexdigest()
def dt(s): return datetime.datetime.fromisoformat(s.replace('Z','+00:00'))
def duration(a,b): return round((dt(b)-dt(a)).total_seconds(),3)

source=Path('source.jpg').read_bytes();prompt=Path('output/prompt.txt').read_bytes();render=Path('output/render.png').read_bytes()
freeze=read('prompt-freeze.json');attempt=read('generation-attempt-log.json');critic=read('critic-root.json');route=read('route.json')
assert sha(source)==critic['source_sha256']
assert sha(prompt)==freeze['prompt_sha256']==critic['prompt_sha256']
request=read('generation-request.raw.json');assert list(request)==['prompt'] and request['prompt'].encode()==prompt
assert read('generation-request.json')==request
assert base64.b64decode(read('generation-response.raw.json')['image_url'].split(',',1)[1])==render
assert attempt['attempt_count']==2 and attempt['transport_retry_count']==1 and attempt['quality_retry_count']==0
assert all(a['actual_tool_prompt_sha256']==sha(prompt) for a in attempt['attempts'])

snapshot_checks=[]
for directory,manifest in [('skill','skill-snapshot-manifest.json'),('skill-v2','skill-v2-snapshot-manifest.json'),('skill-v3','skill-v3-snapshot-manifest.json')]:
    entries=read(manifest)['files'];expected={x['path']:x['sha256'] for x in entries}
    actual={str(p.relative_to(directory)):sha(p.read_bytes()) for p in Path(directory).rglob('*') if p.is_file()}
    snapshot_checks.append({'directory':directory,'file_count':len(actual),
        'mismatches':[k for k in expected if actual.get(k)!=expected[k]],
        'unexpected_files':sorted(set(actual)-set(expected))})
integrity={'checked_utc':now(),'source_sha256':sha(source),'prompt_sha256':sha(prompt),'render_sha256':sha(render),
    'source_unchanged':sha(source)==read('run-start.json')['source_sha256'],
    'prompt_identical_to_critic_and_both_tool_calls':True,'raw_response_binary_equals_render':True,
    'snapshot_checks':snapshot_checks,'status':'ok' if all(not x['mismatches'] and not x['unexpected_files'] for x in snapshot_checks) else 'failed'}
save('input-output-integrity-final.json',integrity)

lanes=[]
for name in ['global_lane','spatial_lane','appearance_lane','color_lane','capture_lane']:
    p=read(name+'.report-provenance.json');r=read(name+'.report.json');ind=name in ['global_lane','spatial_lane']
    start=p['spawn_utc'][0] if ind else p['instruction_read_start_utc'];end=p['received_utc'] if ind else p['frozen_utc']
    lanes.append({'lane':name,'execution_mode':'delegated' if ind else 'sequential-fallback','independent_context':ind,
                  'started_utc':start,'ended_utc':end,'observed_wall_seconds':duration(start,end),
                  'time_scope':'spawn through received final report' if ind else p['analysis_wall_scope'],
                  'findings':len(r['findings']),'atomic_obligations':sum(len(f['atomic_obligations']) for f in r['findings']),
                  'raw_report_sha256':sha(Path('output/'+name+'.report.raw.json').read_bytes())})

# Retain only current-case, actual tool events; never inspect reasoning or other sessions.
session=Path('/Users/chasoik/.codex/sessions/2026/09/05/rollout-2026-09-05T23-05-13-01a071e3-3cc7-7c60-bd5e-5d0f19160672.jsonl')
call_counts=collections.Counter();command_events=0;image_events=0;integration_events=[]
for line in session.read_bytes().splitlines():
    row=json.loads(line);p=row.get('payload',{});item=p.get('item',{})
    if row.get('type')=='response_item' and p.get('type') in ('function_call','custom_tool_call'):
        call_counts[p.get('name','unknown')]+=1
        value=p.get('arguments',p.get('input',''))
        if row['timestamp']<'2026-09-05T15:00:00' and p.get('name')=='exec':
            if 'cat > output/build_plan.py' in value or 'cat > output/reconcile_plan.py' in value:
                integration_events.append({'timestamp':row['timestamp'],'call_id':p.get('call_id'),'scope':'first plan authoring file write' if 'build_plan.py' in value else 'obligation reconciliation file write'})
    if row.get('type')=='event_msg' and p.get('thread_id')=='01a071e3-3cc7-7c60-bd5e-5d0f19160672':
        command_events+=item.get('type')=='CommandExecution'
        image_events+=item.get('kind')=='image_gen.generation'
save('integration-observed-events.json',{'events':integration_events,'limitation':'Actual artifact-write dispatch timestamps; preceding analysis/authoring duration is not directly observable.'})
old=Path('output/critic-dispatch.json');backup=Path('output/critic-dispatch.initial.json')
if not backup.exists():shutil.copyfile(old,backup)
save('critic-dispatch.json',{'status':'review-complete','manifest':'critic-input-manifest.json','review':'critic-root.json',
     'reviewed_at':critic['reviewed_at'],'dispatch_timestamp':None,'dispatch_timestamp_limitation':'Not exposed in the captured current-case tool records. Initial empty dispatch capture is preserved.',
     'reviewer_mode':critic['independence_disclosure']})

source_dims=read('run-start.json')['source_dimensions'];render_meta=read('render-metadata.json');render_dims=render_meta['dimensions']
src_ratio=source_dims[0]/source_dims[1];out_ratio=render_dims[0]/render_dims[1]
size={'source_dimensions':source_dims,'delivered_dimensions':render_dims,'source_ratio':src_ratio,'delivered_ratio':out_ratio,
      'relative_ratio_error':abs(out_ratio-src_ratio)/src_ratio,'dimension_control':'not-exposed/unsupported',
      'requested_size_argument':None,'theoretical_adapter_note':'size-adapter-before-generation.json evaluates an unavailable model-specific setting only; it was not applied and is not a generator identity claim.',
      'frame_composition_evidence':'render-observations.json','acceptance_status':'unscored; no justified numerical tolerance'}
save('frame-delivery.json',size)

evaluation=read('color-evaluation.json')
color_note={'status':evaluation['status'],'comparison_scope':evaluation['comparison_scope'],'policy':None,
    'source_and_render_icc_profiles':'Both missing; assumed display-space relative measurements only.',
    'sampling':'Manual semantic correspondences, independent bounds, separate target midtone and context flat/shadow groups; retained medians/dispersion in color-probe.json.',
    'measured_garment_delta_L':{x['name']:x['total_render_minus_source']['lab_d65'][0] for x in evaluation['target_groups']},
    'dominant_residual_axis':evaluation['dominant_residual_axis'],'drift_class':evaluation['drift_class'],
    'interpretation':'Selected cardigan and tank patches are darker in delivered displayed pixels. Knit/fold, global response and low chroma make a calibrated intrinsic-color diagnosis unsupported. Hue angle movement is not interpreted as reliable at low chroma.',
    'no_controls_changed':True,'not_a_pass':True}
save('color-interpretation.json',color_note)

validation=read('pre-render-validation.json');integration=read('integration-decisions.json')
end=now();start=read('run-start.json')['session_start_utc']
report={
    'case':'case-02','raw_request':read('run-start.json')['raw_request'],'outcome':'one image delivered from the exact frozen standalone English prompt',
    'started_utc':start,'ended_utc':end,'observed_case_wall_seconds':duration(start,end),
    'isolation':'Case-only source and snapshot work; no sibling/parent artifacts, repo history or memory retrieval. Current exact case session tool events and helper final payloads were used for provenance.',
    'instruction_provenance':'v1 source analysis and unchanged module/lane views; final validations with skill-v3. v1/v2/v3 snapshots and observed transitions preserved.',
    'route':{'profile':route['analysis_profile'],'fingerprint':route['route_fingerprint'],'required_lanes':route['required_lane_ids'],'timing':read('route-timing.json')},
    'lane_execution':{'mode':'mixed','independence_claimed_for_all':False,'lanes':lanes,'failed_fresh_lane_spawns':1,'failed_spawn_evidence':'delegation-limit-events.json'},
    'integration':{'findings':sum(x['findings'] for x in lanes),'atomic_obligations':sum(x['atomic_obligations'] for x in lanes),
                   'invariants':len(read('plan.json')['render_contract']['invariants']),
                   'observed_events':integration_events,'review_packet_completed_utc':integration['completed_utc'],
                   'full_authoring_duration_seconds':None,'duration_limitation':'Only write dispatch and saved packet timestamps are directly observable; model authoring preceded the writes.'},
    'critic':{'status':critic['status'],'reviewer':critic['reviewer'],'independence_disclosure':critic['independence_disclosure'],
              'passes':1,'reviewed_at':critic['reviewed_at'],'started_at':None,'wall_seconds':None,'timing_limitation':'Reviewer completion time supplied; critic start not exposed.',
              'raw_sha256':sha(Path('output/critic-root.json').read_bytes())},
    'validation':{'pre_generation_status':validation['status'],'checks':[{'label':c['label'],'exit_code':c['exit_code'],'started_utc':c['started_utc'],'ended_utc':c['ended_utc'],'result':json.loads(c['stdout'])} for c in validation['checks']],
                  'source_aware_standalone_review':'pass','initial_route_failure':'route-validation-v1.json','initial_plan_errors':'plan-validation-draft.json',
                  'pending_critic_expected_failure':'bundle-validation-before-critic.json','regression_tests':'Not rerun here. Parent reported v3 311 tests + 267 subtests; tests are not pixel evidence.'},
    'freeze':freeze,'source':{'sha256':sha(source),'dimensions':source_dims},'render':render_meta,
    'request':{'tool':'image_gen__imagegen','fields':list(request),'conditioning':'text-only; both image reference fields omitted',
               'prompt_bytes_match_frozen':True,'raw_request_sha256':sha(Path('output/generation-request.raw.json').read_bytes()),
               'model':'not-exposed/unsupported','size':'not-exposed/unsupported','quality':'not-exposed/unsupported'},
    'generation':attempt,'frame_delivery':size,'color_evaluation':color_note,
    'pixel_evaluation':read('render-observations.json'),
    'event_counts':{'scope':'Current exact case session observed before this report completes; functions wrappers and native completed events count separately, not summed.',
                    'tool_dispatches_by_name':dict(call_counts),'completed_command_events':command_events,'image_generation_events':image_events,
                    'nonzero_command_events':len(read('failed-command-events.json')['events']),
                    'logical_lane_waves':1,'successful_fresh_context_lanes':2,'sequential_fallback_lanes':3,
                    'malformed_lane_retries':0,'full_reroutes':0,'schema_reconciliations':1,'critic_requested_repairs':0,
                    'generation_calls':2,'generation_no_delivery_failures':1,'identical_byte_transport_retries':1,'quality_retries':0,'delivered_images':1},
    'integrity':integrity,'user_judgment':'unscored'
}
save('run-report.json',report)
summary=f'''영문 프롬프트를 동결하고 해당 텍스트만으로 이미지 한 장을 생성했습니다.

- PROMPT: [prompt.txt]({Path('output/prompt.txt').resolve()}) — 597 words, SHA256 `{sha(prompt)}`
- 이미지: [render.png]({Path('output/render.png').resolve()}) — {render_dims[0]}×{render_dims[1]}, SHA256 `{sha(render)}`
- 원본 SHA256: `{sha(source)}`
- 검사: v3 번들·계획·독립형 문장 검사 PASS; 별도 source-aware critic PASS. 25 findings / 69 obligations / 40 invariants.
- 분석 실행: 독립 레인 2개 + thread-limit 후 sequential-fallback 3개. Critic은 case integrator와 분리된 Root이며 여러 사례의 공통 검토자입니다.
- 생성: 최초 1회 무전달 실패 후 동일 바이트 재시도 1회 성공. 전달 1장, 품질 재시도 0회. 모델·크기·품질 설정은 노출되지 않았습니다.
- 픽셀 한계: 몸이 더 중앙/수직이고, 카디건 짜임이 더 두껍고 선명하며, 메모가 작고 어둡습니다. 원본보다 옷이 어둡고 중간 몸통 노출 띠가 커졌습니다.
- 색 측정: assumed-display-space relative, acceptance policy 없음 → unscored. 선택한 패치의 ΔL*: 카디건 −16.109, 상의 −8.340, 반바지 −3.847. 수치는 원단 고유색의 증거가 아닙니다.
- 전체 기록: [run-report.json]({Path('output/run-report.json').resolve()}) · [raw request]({Path('output/generation-request.raw.json').resolve()}) · [raw result]({Path('output/generation-response.raw.json').resolve()})

원본과 입력 스냅샷 무결성: {integrity['status']}. 검증 PASS는 시각적 충실도 PASS를 의미하지 않습니다. 사용자 평가는 아직 없습니다.
'''
Path('output/result-summary.md').write_text(summary)
manifest=[]
for p in sorted(Path('output').rglob('*')):
    if p.is_file() and p.name!='artifact-manifest.json':manifest.append({'path':str(p.relative_to('output')),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
save('artifact-manifest.json',{'recorded_utc':now(),'files':manifest,'scope':'output files excluding this manifest itself'})
print(json.dumps({'status':report['outcome'],'ended_utc':end,'wall_seconds':report['observed_case_wall_seconds'],'integrity':integrity['status'],
                  'render':str(Path('output/render.png').resolve()),'source_ratio_relative_error':size['relative_ratio_error'],'report':str(Path('output/run-report.json').resolve())}))
