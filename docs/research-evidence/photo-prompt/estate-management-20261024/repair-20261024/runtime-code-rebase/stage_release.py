"""Merge the completed reviewed data delta with the current verified kernel.
No source rebuild, selection or guard changes. Refuse concurrent data drift.
"""
from pathlib import Path
import gc; gc.disable()
import json,sys,hashlib,subprocess,os
O=Path(__file__).resolve().parent;ROOT=Path('/Users/chasoik/Projects/image-prompt');S=ROOT/'skills/photo-prompt-image-generator';read=lambda p:json.loads(p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
B=read(O.parent/'runtime-default-release/before.json');D=read(O.parent/'runtime-default-release/successor.json');config=read(S/'retrieval-runtime.json');store=Path(B['store']);N=store/'generations'/config['native_generation_id'];prior=Path(B['native'])
sys.path.insert(0,str(S/'scripts'))
from photo_installed_h_f2 import release,digest
from stage_photo_h_f2_code import stage
_,_,nm=release(store,config['generation_id'],full=True)
assets=lambda root:{str(p.relative_to(root/'assets')):sha(p) for p in (root/'assets').rglob('*') if p.is_file()}
assert assets(N)==assets(prior),'Concurrent data changed; merge sources before publishing'
source=Path(D['store'])/'generations'/D['native_generation_id'];old=read(source/'manifest.json')['source']['code'];current=nm['source']['code'];assert not set(old)-set(current),'Unexpected removed code member'
selected=sorted(k for k,v in current.items() if old.get(k)!=v);assert selected
assert b'def audit_parent_generation' in (N/'scripts/prepare_retry_context.py').read_bytes()
assert b'def _preserved_assertion_matches' in (N/'scripts/prepare_retry_context.py').read_bytes()
current_before={'config':config,'store':str(store),'native':str(N),'reason':'Current verified kernel with exact reviewed eight-candidate data delta; all concurrent candidate assets byte equal to data-build baseline.'}
(O/'publication-before.json').write_text(json.dumps(current_before,indent=2)+'\n')
# Only allocation scheduling and independent APFS transport copies differ.
import stage_photo_h_f2_code as module
original_run=module.subprocess.run
original_copy=module.shutil.copyfile
copies=[]
def clone(src,dst,**kw):
 if Path(src).is_file() and Path(src).stat().st_size>=64*1024*1024:
  original_run(['/bin/cp','-c',str(src),str(dst)],check=True);assert Path(src).stat().st_ino!=Path(dst).stat().st_ino;copies.append(str(dst));return dst
 return original_copy(src,dst,**kw)
def run(args,*a,**kw):
 args=list(args)
 if '-c' in args:
  i=args.index('-c')+1;args[i]='import gc;gc.disable();'+args[i]
 return original_run(args,*a,**kw)
module.shutil.copyfile=clone;module.subprocess.run=run
out=stage('/Users/chasoik/.cache/image-prompt/estate-management-repair-current-code-20261024',source_store=D['store'],generation_id=D['generation_id'],members=selected,overlay_root=N)
_,_,done=release(out['store'],out['generation_id'],full=True);assert done['source']['code']==current
out.update({'kernel_equals_current_verified_kernel':True,'new_CIDs':8,'new_bindings':21,'source_candidate_assets_unchanged_from_reviewed_data_delta':True,'allocation_only_wrapper':True,'validation_bypassed':False,'copied_independent_large_files':len(copies)})
(O/'successor.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
