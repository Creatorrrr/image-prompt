from pathlib import Path
import json,hashlib,subprocess
R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';O=Path(__file__).parent;E=O/'coordinator';E.mkdir(exist_ok=True)
def wr(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
request='surreal 3 으로 테스트해줘.';(E/'request.txt').write_text(request)
wr(E/'spans.json',[{'span_id':'surreal_setting','start':0,'end':9,'text':'surreal 3'}])
wr(E/'query-scope.json',{'contract_version':'photo-request-query-scope/v1','segments':[{'active_span_id':'surreal_setting','start':0,'end':7,'text':'surreal','purpose':'visual','reason':'Explicit surreal topic; level is bound in controls.'},{'active_span_id':'surreal_setting','start':8,'end':9,'text':'3','purpose':'workflow','reason':'Explicit creative-control value bound in snapshot; not an extra object.'}]})
img=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
wr(E/'inputs.json',{'schema':'photo-request-input-inventory/v1','complete':True,'items':[{'id':'request','kind':'request_text','sha256':sha(E/'request.txt')},{'id':'portrait','kind':'reference_image','sha256':sha(img)}]})
wr(E/'creative_overrides.json',{'surreal':3})
rows=[]
for arm,parentarm in [('a','a'),('b','b2'),('c','c')]:
 child=R/'generated/photo-runs'/('surreal3-20261024-'+arm);parent=R/'generated/photo-runs'/('surreal-expansion-20261024-'+parentarm)
 if not (child/'workflow.json').exists():
  p=subprocess.run(['python3',str(S/'precore/prepare_photo_run.py'),'init','--run',str(child),'--request',str(E/'request.txt'),'--spans',str(E/'spans.json'),'--query-scope',str(E/'query-scope.json'),'--input-inventory',str(E/'inputs.json'),'--request-id','surreal3-20261024-'+arm,'--mode','image'],capture_output=True,text=True);print('init',arm,p.returncode,p.stdout,p.stderr,flush=True)
  if p.returncode:raise SystemExit(p.returncode)
 state=json.loads((child/'workflow.json').read_bytes());env=state['artifacts']['request_envelope_input'];m=json.loads((parent/'run_manifest.json').read_bytes());ledger=parent/'image_runs.ndjson'
 attempt=next(json.loads(x) for x in ledger.read_text().splitlines() if json.loads(x)['run_id']==m['ledger_run_id']);private=E/arm;private.mkdir(exist_ok=True);wr(private/'parent-attempt.json',attempt)
 decision={'schema_version':'photo-repair-decision/v1','current_source_span_ids':['surreal_setting'],'source_text':'surreal 3','preserved_dimensions':['concept','subject','event','reference_use','appearance'],'allowed_changes':['pose','body_geometry','expression','action','setting','relationship','style','framing','composition','lighting','camera','color','material','timing','atmosphere'],'requester_corrected_dimensions':[],'allowed_properties':[],'local_axes':['framing','lighting','camera','material'],'failed_gate_ids':[],'failure_class':'artistic_revision','additional_invocation_limit':1,'obligation_dimensions':{}}
 wr(private/'decision.json',decision);projection=O/'projections'/(arm+'-v3')
 p=subprocess.run(['python3',str(S/'scripts/prepare_retry_context.py'),'prepare','--run',str(parent),'--attempt',str(private/'parent-attempt.json'),'--ledger',str(ledger),'--current-envelope',env['path'],'--decision',str(private/'decision.json'),'--output',str(projection)],capture_output=True,text=True);(private/'projection-v3.log').write_text(p.stdout+p.stderr);print('project',arm,p.returncode,p.stdout,p.stderr,flush=True)
 rows.append({'arm':arm,'parent':str(parent),'run':str(child),'envelope':env,'projection':str(projection),'projection_status':p.returncode});wr(E/'bindings.json',rows)
 if p.returncode:raise SystemExit(p.returncode)
 p=subprocess.run(['python3',str(S/'scripts/photo_workflow.py'),'attach-retry','--run',str(child),'--proof',str(projection/'retry_proof.json')],capture_output=True,text=True);(private/'attach.log').write_text(p.stdout+p.stderr);print('attach',arm,p.returncode,p.stdout,p.stderr,flush=True)
 if p.returncode:raise SystemExit(p.returncode)
