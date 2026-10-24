from pathlib import Path
import json,sys,datetime,traceback
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'))
from install_photo_h_f2_runtime import install
read=lambda p:json.loads(p.read_bytes())
b=read(O/'BASELINE.json');target=read(O/'code-successor.json');before=read(S/'retrieval-runtime.json');result={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'expected_base':b['config'],'observed_before':before,'target_generation':target['generation_id']}
if before!=b['config']:
 result.update(status='not_selected_concurrent_default_changed',CURRENT_writes=0,config_writes=0)
else:
 try:
  result['installation']=install(target['store'],target['generation_id'],activate=True);result['observed_after']=read(S/'retrieval-runtime.json');assert result['observed_after']['generation_id']==target['generation_id'];result.update(status='installed_and_selected',CURRENT_writes=0)
 except Exception as error:result.update(status='validation_or_concurrency_error',error=str(error),traceback=traceback.format_exc(),observed_after=read(S/'retrieval-runtime.json'))
(O/'default-selection.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
if result['status']!='installed_and_selected':sys.exit(1)
