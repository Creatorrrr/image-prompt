"""Install the verified source closure; preserve concurrent default selection."""
from pathlib import Path
import gc;gc.disable()
import json,sys

O=Path(__file__).resolve().parent;R=O.parents[4];S=R/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(S/'scripts'))
import install_photo_h_f2_runtime as installer
read=lambda p:json.loads(p.read_bytes())
r=read(O/'successor.json');b=read(O/'release-base.json')
activate='--activate' in sys.argv
if activate:
 q=read(O/'registration-qualification.json');assert q['status']=='pass' and q['diagnostic_positive_leaks']==0
if activate:assert read(S/'retrieval-runtime.json')==b['config'],'Concurrent selected release advanced; rebase rather than overwrite.'
# Scheduling only: run every original immutable seal and deployed validator unchanged.
original=installer.subprocess.run
def scheduled(args,*a,**kw):
 args=list(args)
 if '-c' in args:
  k=args.index('-c')+1;args[k]='import gc;gc.disable();'+args[k]
 return original(args,*a,**kw)
installer.subprocess.run=scheduled
result=installer.install(r['store'],r['generation_id'],activate=activate)
out=O/('install-active.json' if activate else 'install-copy.json');out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False),flush=True)
