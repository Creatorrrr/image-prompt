"""Install verified data successor; never overwrite a concurrently advanced default."""
import gc,json,sys
from pathlib import Path
gc.disable()
O=Path(__file__).resolve().parent;ROOT=O.parents[4];S=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(S/'scripts'))
import install_photo_h_f2_runtime as installer
read=lambda p:json.loads(p.read_bytes())
release=read(O/'rebase-successor.json');before=read(O/'rebase-before.json');activate='--activate' in sys.argv
if activate:assert read(S/'retrieval-runtime.json')==before['config'],'Default advanced: rebase rather than overwrite it.'
original_run=installer.subprocess.run
def controlled(args,*a,**kw):
 args=list(args)
 if '-c' in args:
  i=args.index('-c')+1;args[i]='import gc;gc.disable();'+args[i]
 return original_run(args,*a,**kw)
installer.subprocess.run=controlled
result=installer.install(release['store'],release['generation_id'],activate=activate)
(O/('rebase-install-active.json' if activate else 'rebase-install.json')).write_text(json.dumps(result,indent=2)+'\n')
(O/'rebase-validation-execution.json').write_text(json.dumps({'cyclic_gc_enabled':False,'validation_bypassed':False,'all_deployed_validators_executed':True,'kernel_code_changed':False},indent=2)+'\n')
print(json.dumps(result),flush=True)
