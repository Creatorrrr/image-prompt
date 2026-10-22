"""Pin the latest local executable skill members on the installed data baseline."""
import gc;gc.disable()
import hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path('/Users/chasoik/Projects/image-prompt');S=ROOT/'skills/photo-prompt-image-generator';O=Path(__file__).resolve().parent
sys.path.insert(0,str(S/'scripts'))
from photo_installed_h_f2 import default_store,release
import stage_photo_h_f2_code as staging
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 cfg=read(S/'retrieval-runtime.json');native,h,n=release(default_store(),cfg['generation_id'])
 current={str(p.relative_to(S)):sha(p) for d in ['scripts','precore'] for p in sorted((S/d).glob('*.py'))}
 selected=['scripts/photo_h_f2_query_scope.py']
 missing=sorted(set(n['source']['code'])-set(current))
 overlay=O/'latest-reviewed-overlay';overlay.mkdir(exist_ok=True)
 for r in selected:
  p=overlay/r;p.parent.mkdir(parents=True,exist_ok=True);assert p.is_file();current[r]=sha(p)
 write(O/'compatible-kernel-input.json',{'base_config':cfg,'base_native':str(native),'base_store':str(default_store()),'selected_members':selected,'selected_sha256':{r:current[r] for r in selected},'unchanged_members_preserved':len(n['source']['code'])-len(selected),'sealed_compatibility_members_not_in_checkout_retained':missing,'skill_sha256':sha(S/'SKILL.md'),'reason':'The sealed V4 implementation already contains the latest topic-context, neutral-negative and agency deltas. Port only the new reviewed capability-clause delta; preserve the canonical source/runtime implementation and all data. See latest-reviewed-delta.json. The rejected broad overlay was never activated.'})
 original_run=staging.subprocess.run
 def controlled_run(args,*a,**kw):
  args=list(args)
  if '-c' in args:
   i=args.index('-c')+1;args[i]='import gc;gc.disable();'+args[i]
  return original_run(args,*a,**kw)
 staging.subprocess.run=controlled_run
 result=staging.stage(O/'compatible-kernel-store',source_store=default_store(),generation_id=cfg['generation_id'],members=selected,overlay_root=overlay)
 write(O/'compatible-kernel-stage.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
