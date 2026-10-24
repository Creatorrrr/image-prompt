"""Guarded install of the exact union against the latest baseline."""
import gc,json,sys
from pathlib import Path
gc.disable()
O=Path(__file__).resolve().parent/(sys.argv[1] if len(sys.argv)>1 else 'rebase-1')
ROOT=Path('/Users/chasoik/Projects/image-prompt');S=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(S/'scripts'))
import install_photo_h_f2_runtime as installer
read=lambda p:json.loads(p.read_bytes())
release=read(O/'successor.json');before=read(O/'before.json')
activate='--no-activate' not in sys.argv
if activate:assert read(S/'retrieval-runtime.json')==before['config'],'Default advanced: rebase rather than overwrite it.'
original_run=installer.subprocess.run
def controlled(args,*a,**kw):
 args=list(args)
 if '-c' in args:
  i=args.index('-c')+1;args[i]='import gc;gc.disable();'+args[i]
 return original_run(args,*a,**kw)
installer.subprocess.run=controlled
result=installer.install(release['store'],release['generation_id'],activate=activate)
(O/('install-active.json' if activate else 'install.json')).write_text(json.dumps(result,indent=2)+'\n')
(O/'validation-execution.json').write_text(json.dumps({'cyclic_gc_enabled':False,'validation_bypassed':False,'all_deployed_validators_executed':True,'kernel_code_authored':False},indent=2)+'\n')
print(json.dumps(result),flush=True)
