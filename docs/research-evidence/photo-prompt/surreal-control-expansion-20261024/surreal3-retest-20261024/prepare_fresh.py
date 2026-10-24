from pathlib import Path
import json,hashlib,subprocess
R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';O=Path(__file__).parent;E=O/'fresh-coordinator';E.mkdir(exist_ok=True)
def wr(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
request='surreal 3 으로 테스트해줘.';prior='시각 의미 데이터와 후보 데이터에 반영해줘. 그 다음 스킬의 최신 버전을 사용하여 독립된 서브에이전트 3개에서 각각 서로 다른 컨셉으로 이번에 반영한 주제가 이미지에 실제로 반영되는지까지 테스트할 수 있는 주제에 어울리는 랜덤한 컨셉을 정하여 테스트케이스를 마련하고 첨부한 이미지를 활용하여 프롬프트 작성하고 이미지 생성하도록 하여 잘 반영되었는지 테스트해줘.'
(E/'request.txt').write_text(request);(E/'prior-request.txt').write_text(prior)
wr(E/'spans.json',[{'span_id':'surreal_setting','start':0,'end':9,'text':'surreal 3'}])
wr(E/'inputs.json',{'schema':'photo-request-input-inventory/v1','complete':True,'items':[{'id':'request','kind':'request_text','sha256':sha(E/'request.txt')},{'id':'portrait','kind':'reference_image','sha256':sha(Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg'))},{'id':'prior_request','kind':'text','sha256':sha(E/'prior-request.txt')}]})
wr(E/'overrides.json',{'surreal':3});rows=[]
for arm in 'abc':
 run=R/'generated/photo-runs'/('surreal3-fresh-20261024-'+arm)
 p=subprocess.run(['python3',str(S/'precore/prepare_photo_run.py'),'init','--run',str(run),'--request',str(E/'request.txt'),'--spans',str(E/'spans.json'),'--input-inventory',str(E/'inputs.json'),'--request-id','surreal3-fresh-20261024-'+arm,'--mode','image'],capture_output=True,text=True);print(arm,p.returncode,p.stdout,p.stderr)
 if p.returncode:raise SystemExit(p.returncode)
 w=json.loads((run/'workflow.json').read_text());rows.append({'arm':arm,'run':str(run),'envelope':w['artifacts']['request_envelope_input']})
wr(E/'bindings.json',rows);print(json.dumps(rows))
