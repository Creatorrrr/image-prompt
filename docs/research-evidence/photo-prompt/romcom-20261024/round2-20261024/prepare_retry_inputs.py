from pathlib import Path
import json,copy,hashlib
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent
latest='신규 후보가 전혀 채택되지 않은 원인과 세 테스트의 실패 원인을 분석해서 스킬과 데이터를 개선하고, 같은 참조 이미지로 독립 서브에이전트 3개에서 다시 생성·검증해줘.'
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
for arm,run in [('a','final-run-v2'),('b','narrowed'),('c','corrected-authoring-run')]:
 parent=R/'generated/photo-runs'/f'romcom-20261024-{arm}'/run;state=json.loads((parent/'workflow.json').read_text());p=O/f'retry-{arm}';p.mkdir(exist_ok=True)
 env=json.loads((parent/state['artifacts']['request_envelope_input']['path']).read_text());old=env['request_text'];env['request_text']=old+'\n'+latest;env['request_id']=f'romcom-20261024-r2-{arm}';env['request_sha256']=hashlib.sha256(env['request_text'].encode()).hexdigest();s=env['request_text'].index('같은 참조 이미지로',len(old));env['active_spans'].append({'span_id':'repair_reference','start':s,'end':s+len('같은 참조 이미지로'),'text':'같은 참조 이미지로'});env['input_inventory']['items'][0]['sha256']=env['request_sha256'];write(p/'current-envelope.json',env)
 (p/'request.txt').write_text(env['request_text']);write(p/'spans.json',env['active_spans'])
 ledger=R/'generated/photo-runs'/f'romcom-20261024-{arm}'/'image_runs.ndjson';attempt=json.loads(ledger.read_text().splitlines()[-1]);write(p/'exact-ledger-row.json',attempt)
 core=json.loads((parent/state['artifacts']['authorial_core_normalized']['path']).read_text());review=json.loads((parent/state['artifacts']['visual_review']['path']).read_text());failed=[k for k,v in review['hard_gates'].items() if v['status']!='pass']
 preserved=set(core['intent_lock']['locked_dimensions'])|{'appearance'}
 changed={'action','pose','body_geometry','expression','composition','framing','camera','lighting','setting','count','timing'}
 d={'schema_version':'photo-repair-decision/v1','current_source_span_ids':['repair_reference'],'source_text':'같은 참조 이미지로','preserved_dimensions':sorted(preserved),'allowed_changes':sorted(changed),'requester_corrected_dimensions':[],'allowed_properties':[{'dimension':'action','target':'interaction','property':'contact'},{'dimension':'body_geometry','target':'participants','property':'support'},{'dimension':'pose','target':'participants','property':'arrangement'},{'dimension':'expression','target':'participants','property':'response'}],'local_axes':['camera','framing','lighting','contact_geometry','local_pose','object_geometry','occlusion'],'failed_gate_ids':failed,'failure_class':'artistic_revision' if not failed else 'pixel_realization_mismatch','additional_invocation_limit':1,'obligation_dimensions':{}}
 write(p/'repair-decision.json',d)
 write(p/'coordinator-inputs.json',{'parent_run':str(parent),'ledger':str(ledger),'concept_assignment':{'a':'flower-arranging rivalry','b':'winter-festival skating date','c':'post-rain cafe parasol encounter'}[arm],'analysis_scope':'Repeat the same conceptual family for comparison; staging remains author-owned and open.','defect_summary':{'a':'The image read as a pleasant shared-flower portrait; abundant arrangements or available substitutes weakened the claimed last-flower competition.','b':'The far screen-right skate was cut off: its blade and ice contact were unobservable.','c':'The operating hand gripped the pole above the crank; the actual crank was untouched.'}[arm]})
 print(arm,str(p))
