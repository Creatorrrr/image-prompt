from pathlib import Path
import json,hashlib
ROOT=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sha=lambda b:hashlib.sha256(b).hexdigest()
request='신규 후보가 채택되지 않은 원인과 세 장면의 관계 구현 실패를 분석해서 개선해줘. 같은 세 컨셉과 첨부 이미지로 독립 서브에이전트 3개에서 다시 테스트하고, 신규 데이터가 실제 프롬프트와 이미지에 반영됐는지까지 검증해줘.'
(O/'requester-request.txt').write_text(request)
spans=[]
for key,quote,purpose in [('repair','관계 구현 실패를 분석해서 개선해줘','workflow'),('concept','같은 세 컨셉','topic_reference'),('reference','첨부 이미지','reference_use')]:
 a=request.index(quote);spans.append({'span_id':key,'start':a,'end':a+len(quote),'text':quote,'purpose':purpose})
prior=(O.parent/'integration-evidence/prior-requester-context.txt').read_text().strip();quote='수사물';a=prior.index(quote);s=next(v for v in spans if v['span_id']=='concept')
topic={'contract_version':'photo-request-topic-context/v1','links':[{'context_id':'prior-investigative-topic','active_span_id':'concept','request_quote':{k:s[k] for k in ('start','end','text')},'source_message':{'provenance':'requesting_user','locator':'chatgpt-conversation://6adc076c-0c60-83e8-a9a3-369c26c3ea65','text':prior,'sha256':sha(prior.encode())},'topic_quote':{'start':a,'end':a+len(quote),'text':quote},'review':{'polarity':'positive_topic','rationale':'The exact genre substring is the visual topic. The title suffix describes glossary work; complete actual prior requester text is retained.'}}]}
ref=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
failed={'a':['embodiment_contact_and_space'],'b':['embodiment_support_and_balance','embodiment_visibility_and_projection'],'c':['embodiment_contact_and_space']}
props={'a':[('action','investigator','contact.pencil_statement'),('composition','evidence','placement.shared_view')],'b':[('action','investigator','contact.camera_scale'),('body_geometry','crate','support.trolley'),('composition','seal','visibility.cut_ends')],'c':[('action','investigator','contact.photo_pen'),('relationship','investigator','gaze.map_point'),('action','attendant','contact.map_target')]}
for arm in 'abc':
 d=O/('arm-'+arm);d.mkdir(exist_ok=True)
 envelope={'contract_version':'photo-request-envelope/v1','provenance':'requesting_user','request_id':'investigative-repair-20261025-'+arm,'request_text':request,'request_sha256':sha(request.encode()),'active_spans':[{k:v for k,v in s.items() if k!='purpose'} for s in spans],'topic_context':topic,'query_scope':{'contract_version':'photo-request-query-scope/v1','segments':[{'active_span_id':s['span_id'],**{k:s[k] for k in ('start','end','text')},'purpose':s['purpose'],'reason':'Explicit repair execution, exact accepted-topic antecedent, and original appearance reference retain separate roles.'} for s in spans]}}
 write(d/'request-envelope.json',envelope)
 write(d/'input-inventory.json',{'schema':'photo-request-input-inventory/v1','complete':True,'items':[{'id':'request','kind':'request_text','sha256':sha(request.encode())},{'id':'reference','kind':'reference_image','sha256':sha(ref.read_bytes())},{'id':'prior_topic_request','kind':'text','sha256':sha(prior.encode())}]})
 decision={'schema_version':'photo-repair-decision/v1','current_source_span_ids':['repair'],'source_text':'관계 구현 실패를 분석해서 개선해줘','preserved_dimensions':['concept','subject','event','reference_use','appearance'],'allowed_changes':['pose','body_geometry','action','relationship','framing','composition','camera','lighting','material','timing'],'requester_corrected_dimensions':[],'allowed_properties':[{'dimension':v[0],'target':v[1],'property':v[2]} for v in props[arm]],'local_axes':['object_geometry','contact_geometry','local_pose','camera','framing','lighting','material','occlusion'],'failed_gate_ids':failed[arm],'failure_class':'pixel_realization_mismatch','additional_invocation_limit':1,'obligation_dimensions':{}}
 write(d/'repair-decision.json',decision)
 parent=ROOT/('generated/photo-runs/investigative-fiction-20261025-'+arm)
 rows=[json.loads(s) for s in (parent/'image_runs.ndjson').read_text().splitlines() if s.strip()];assert len(rows)==1
 write(d/'parent-attempt.json',rows[0])
 print(arm,'envelope',sha((d/'request-envelope.json').read_bytes()))
