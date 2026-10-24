"""Run the unchanged managed workflow, deferring cyclic GC for its acyclic JSON work.
No command, validation, assertion, environment stripping or source hash is omitted.
Only the dispatcher's exact Python launcher gains gc.disable().
"""
from pathlib import Path
import gc,runpy,subprocess,sys
gc.disable()
R=Path(__file__).resolve().parents[5]
script=R/'skills/photo-prompt-image-generator/scripts/photo_workflow.py'
original_run=subprocess.run
def scheduled_run(args,*pos,**kw):
 if isinstance(args,(list,tuple)):
  child=list(args)
  if child and str(child[0]).endswith('/python') and '-c' in child:
   i=child.index('-c')+1
   if i<len(child) and isinstance(child[i],str) and child[i].startswith('import sys,runpy;from pathlib import Path;'):
    child[i]='import gc;gc.disable();'+child[i]
  args=child
 return original_run(args,*pos,**kw)
subprocess.run=scheduled_run
sys.path.insert(0,str(script.parent));sys.argv=[str(script),*sys.argv[1:]]
runpy.run_path(str(script),run_name='__main__')
