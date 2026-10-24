from pathlib import Path
import hashlib,json,subprocess
R=Path('/Users/chasoik/Projects/image-prompt'); O=Path(__file__).parent; E=O/'coordinator';E.mkdir(exist_ok=True)
def put(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
s='시각 의미 데이터와 후보 데이터에 반영해줘. 그 다음 스킬의 최신 버전을 사용하여 독립된 서브에이전트 3개에서 각각 서로 다른 컨셉으로 이번에 반영한 주제가 이미지에 실제로 반영되는지까지 테스트할 수 있는 주제에 어울리는 랜덤한 컨셉을 정하여 테스트케이스를 마련하고 첨부한 이미지를 활용하여 프롬프트 작성하고 이미지 생성하도록 하여 잘 반영되었는지 테스트해줘.'
(E/'request.txt').write_text(s)
prior='[$photo-prompt-image-generator](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md) 에서 surreal 설정값이 있는 걸로 알고 있는데 후보 데이터나 시각 의미 데이터에 그 설정값과 관련된 데이터가 충분히 있나?'
spans=[]
for id,q in [('concept','서로 다른 컨셉'),('topic','이번에 반영한 주제'),('reference','첨부한 이미지를 활용하여')]:
 a=s.index(q);spans.append(dict(span_id=id,start=a,end=a+len(q),text=q))
put(E/'spans.json',spans)
a=s.index('이번에 반영한 주제'); b=prior.index('surreal')
put(E/'topic-context.json',{'contract_version':'photo-request-topic-context/v1','links':[{'context_id':'surreal_antecedent','active_span_id':'topic','request_quote':{'start':a,'end':a+len('이번에 반영한 주제'),'text':'이번에 반영한 주제'},'source_message':{'provenance':'requesting_user','locator':'current-conversation:user:initial-surreal-question','text':prior,'sha256':hashlib.sha256(prior.encode()).hexdigest()},'topic_quote':{'start':b,'end':b+7,'text':'surreal'},'review':{'polarity':'positive_topic','rationale':'사용자의 최초 surreal 데이터 질문에 대한 리서치와 현재 반영 주제의 명시적 선행사.'}}]})
put(E/'query-scope.json',{'contract_version':'photo-request-query-scope/v1','segments':[{'active_span_id':p['span_id'],**{k:p[k] for k in ['start','end','text']},'purpose':{'concept':'visual','topic':'topic_reference','reference':'reference_use'}[p['span_id']],'reason':'Actual requester visual scope; execution instructions remain outside visual spans.'} for p in spans]})
img=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
put(E/'inputs.json',{'schema':'photo-request-input-inventory/v1','complete':True,'items':[{'id':'request','kind':'request_text','sha256':hashlib.sha256(s.encode()).hexdigest()},{'id':'portrait','kind':'reference_image','sha256':hashlib.sha256(img.read_bytes()).hexdigest()},{'id':'prior_user_topic','kind':'text','sha256':hashlib.sha256(prior.encode()).hexdigest()}]})
results=[]
for arm in 'abc':
 run=R/'generated/photo-runs'/('surreal-expansion-20261024-'+arm)
 p=subprocess.run(['python3',str(R/'skills/photo-prompt-image-generator/precore/prepare_photo_run.py'),'init','--run',str(run),'--request',str(E/'request.txt'),'--spans',str(E/'spans.json'),'--topic-context',str(E/'topic-context.json'),'--query-scope',str(E/'query-scope.json'),'--input-inventory',str(E/'inputs.json'),'--request-id','surreal-expansion-20261024-'+arm,'--mode','image'],capture_output=True,text=True)
 print(arm,p.returncode,p.stdout,p.stderr)
 if p.returncode:raise SystemExit(p.returncode)
 state=json.loads((run/'workflow.json').read_text())
 artifact=state['artifacts']['request_envelope_input'];env=Path(artifact['path'])
 assert hashlib.sha256(env.read_bytes()).hexdigest()==artifact['sha256']
 results.append({'arm':arm,'run':str(run),'envelope':str(env),'sha256':artifact['sha256']})
put(E/'delegation-bindings.json',results)
