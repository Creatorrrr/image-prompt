from pathlib import Path
import json,sys,time,traceback,datetime
P=Path(__file__).resolve().parent;O=P.parent;R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'))
from stage_photo_h_f2_code import stage
from install_photo_h_f2_runtime import install
read=lambda p:json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
result={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'CURRENT_writes':0}
try:
 deadline=time.monotonic()+1800
 while not (P/'successor.json').exists():
  if time.monotonic()>deadline:raise TimeoutError('data successor not ready')
  time.sleep(5)
 data=read(P/'successor.json');assert data['status']=='staged_verified'
 code=stage(P/'code-successor-store',source_store=data['store'],generation_id=data['generation_id'],members=['scripts/prepare_retry_context.py'],overlay_root=O/'code-overlay');write(P/'code-successor.json',code);print('code successor sealed',code['generation_id'],flush=True)
 result['installation']=install(code['store'],code['generation_id'],activate=False);write(P/'installation.json',result['installation']);print('installed without activation, deployed validators PASS',flush=True)
 baseline=read(P/'BASELINE.json');before=read(S/'retrieval-runtime.json');result['observed_before']=before;result['expected_before']=baseline['config']
 if before!=baseline['config']:
  result['status']='not_selected_concurrent_default_changed';result['config_writes']=0
 else:
  result['selection']=install(code['store'],code['generation_id'],activate=True);result['observed_after']=read(S/'retrieval-runtime.json');assert result['observed_after']['generation_id']==code['generation_id'];result['status']='installed_and_selected'
except Exception as error:result.update(status='publication_error',error=str(error),traceback=traceback.format_exc())
write(P/'publication-result.json',result);print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
if result['status']!='installed_and_selected':sys.exit(1)
