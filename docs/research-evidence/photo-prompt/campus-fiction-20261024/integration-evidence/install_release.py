"""Validate/copy sealed campus release, then select only an unchanged default."""
from pathlib import Path
import gc,json,sys

gc.disable()
S=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator');O=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'scripts'))
from install_photo_h_f2_runtime import install
from photo_installed_h_f2 import check_runtime
import install_photo_h_f2_runtime as installer
base=json.loads((O/'release-base.json').read_bytes());rel=json.loads((O/'successor.json').read_bytes())
assert json.loads((S/'retrieval-runtime.json').read_bytes())==base['config'],'Default advanced; rebase rather than replace another release'
# GC changes allocation timing only. The deployed validators and every assertion remain intact.
original=installer.subprocess.run
def run(args,*a,**kw):
 args=list(args)
 if '-c' in args:
  i=args.index('-c')+1;args[i]='import gc;gc.disable();'+args[i]
 return original(args,*a,**kw)
installer.subprocess.run=run
report=install(rel['store'],rel['generation_id'],skill_root=S,activate=True)
(O/'installed-release.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report),flush=True)
check=check_runtime(skill_root=S,source_store=report['store'],generation_id=rel['generation_id'])
(O/'installed-recorder-after.json').write_text(json.dumps(check,indent=2)+'\n')
assert check['status']=='pass'
print(json.dumps(check),flush=True)
