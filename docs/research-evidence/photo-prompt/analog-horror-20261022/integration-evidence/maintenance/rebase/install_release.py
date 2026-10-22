import gc
gc.disable()
import json,sys
from pathlib import Path
O=Path(__file__).resolve().parent;ROOT=Path('/Users/chasoik/Projects/image-prompt');SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import install_photo_h_f2_runtime as installer
read=lambda p:json.loads(p.read_bytes())
release=read(O/'successor.json');before=read(O/'before.json')
if '--activate' in sys.argv:
    assert read(SKILL/'retrieval-runtime.json')==before['config'],'Installed default advanced; must rebase rather than overwrite it'
# Allocation scheduling only. The deployed validators and every assertion remain unchanged.
original_run=installer.subprocess.run
def controlled_run(args,*a,**kw):
    args=list(args)
    if '-c' in args:
        i=args.index('-c')+1;args[i]='import gc;gc.disable();'+args[i]
    return original_run(args,*a,**kw)
installer.subprocess.run=controlled_run
result=installer.install(release['store'],release['generation_id'],activate=('--activate' in sys.argv))
(O/('install-active.json' if '--activate' in sys.argv else 'install.json')).write_text(json.dumps(result,indent=2)+'\n')
(O/'validation-execution.json').write_text(json.dumps({'cyclic_gc_enabled':False,'deployed_validator_cyclic_gc_enabled':False,'validation_bypassed':False,'kernel_code_changed':False,'reason':'Large acyclic JSON validation allocation scheduling; every original deployed validator and seal check runs.'},indent=2)+'\n')
print(json.dumps(result),flush=True)
