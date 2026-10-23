"""Select the reviewed successor only while the active baseline is unchanged."""
from pathlib import Path
import json,sys,datetime,traceback
O=Path(sys.argv[1]).resolve();R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';sys.path.insert(0,str(S/'scripts'))
from install_photo_h_f2_runtime import install
read=lambda p:json.loads(p.read_bytes())
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
base=read(O/'sealed-base.json');s=read(O/'successor.json');cfg=S/'retrieval-runtime.json';before=read(cfg);result={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'expected_base':base['config'],'observed_before':before,'target_generation':s['generation_id']}
if before!=base['config']:
 result.update(status='not_selected_concurrent_default_changed',CURRENT_writes=0,config_writes=0)
 write(O/'default-selection.json',result);print(json.dumps(result));sys.exit(0)
try:
 result['installation']=install(s['store'],s['generation_id'],activate=True)
 result['observed_after']=read(cfg)
 assert result['observed_after']['generation_id']==s['generation_id']
 result.update(status='installed_and_selected',CURRENT_writes=0)
except Exception as e:
 result.update(status='not_selected_validation_or_concurrency_error',error=str(e),traceback=traceback.format_exc(),observed_after=read(cfg))
write(O/'default-selection.json',result);print(json.dumps(result,ensure_ascii=False,indent=2))
if result['status']!='installed_and_selected':sys.exit(1)
