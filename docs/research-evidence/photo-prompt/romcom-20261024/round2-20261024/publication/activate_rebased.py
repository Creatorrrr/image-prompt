from pathlib import Path
import json,sys,traceback
P=Path(__file__).resolve().parent;S=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator');sys.path.insert(0,str(S/'scripts'))
from install_photo_h_f2_runtime import install
read=lambda p:json.loads(p.read_bytes())
result={}
try:
 proof=read(P/'rebaseline-selection.json');assert proof['current_source_files_exactly_equal_publication_baseline'] and proof['target_code_exactly_equal_current_selected_code'];assert read(S/'retrieval-runtime.json')==proof['expected_config'],'default changed again before activation'
 target=read(P/'code-successor.json');result['installation']=install(target['store'],target['generation_id'],activate=True);result.update(status='installed_and_selected',observed_after=read(S/'retrieval-runtime.json'),CURRENT_writes=0)
except Exception as error:result.update(status='not_selected',error=str(error),traceback=traceback.format_exc(),observed_after=read(S/'retrieval-runtime.json'))
(P/'activation-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
if result['status']!='installed_and_selected':sys.exit(1)
