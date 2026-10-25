from pathlib import Path
import gc,json,sys,shutil,time
import numpy as np
gc.disable()
O=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_bytes())
B=read(O/'release-base.json');N=Path(B['native']);STORE=O/'successor-store';STAGE=O/'successor-skill'
for rel,row in read(N/'manifest.json')['members'].items():
 dst=STAGE/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(N/rel,dst)
shutil.copyfile(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prepare_retry_context.py'),STAGE/'scripts/prepare_retry_context.py')
sys.path.insert(0,str(STAGE/'scripts'))
from photo_recall_generation import write,file_sha
from photo_runtime_sources import SnapshotPublisher
from photo_h_f2_generation import stage as seal_h
def materialize_runtime():
 import subprocess
 lock=read(N/'embedding-runtime.lock.json')
 runtime=STAGE/'.runtime'
 if runtime.is_symlink():runtime.unlink()
 runtime.mkdir(exist_ok=True)
 package=STAGE/lock['package']
 package.mkdir(parents=True,exist_ok=True)
 for rel,row in lock['files'].items():
  src=N/lock['package']/rel;dst=package/rel;dst.parent.mkdir(parents=True,exist_ok=True)
  if not dst.exists():
   result=subprocess.run(['/bin/cp','-c',str(src),str(dst)],capture_output=True)
   if result.returncode:shutil.copyfile(src,dst)
  assert not dst.is_symlink() and dst.stat().st_size==row['bytes'] and file_sha(dst)==row['sha256']
 env=Path(lock['python']).parents[1]
 link=STAGE/env
 if not link.exists():link.symlink_to(Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator')/env,target_is_directory=True)
 write(O/'staged-model-package.json',{'status':'pass','package':str(package),'immutable_files':len(lock['files']),'all_sha256_verified':True,'package_symlink':False,'python_environment_link_only':str(link)})


t=time.monotonic();materialize_runtime()
review=read(O/'code-change-review.json');assert file_sha(STAGE/'scripts/prepare_retry_context.py')==review['new_sha256']
manifest=read(N/'manifest.json');changed=[rel for rel,row in manifest['members'].items() if file_sha(STAGE/rel)!=row['sha256']]
assert changed==['scripts/prepare_retry_context.py'],changed
write(O/'rebased-source-preservation.json',{'status':'pass','changed_members':changed,'all_current_source_and_index_member_bytes_preserved':True,'preserved_member_count':len(manifest['members'])-1,'base':B['config']})
publication=SnapshotPublisher(STAGE,STORE).stage();write(O/'native-staged.json',publication);print('native staged',publication['generation_id'],flush=True)
G=Path(B['store'])/'h-f2-generations'/B['config']['generation_id'];m=read(G/'manifest.json')
inputs={'generation':str(G),'documents':str(G/'documents.json.gz'),'field_documents':str(G/'field-documents.json.gz'),'fields':str(G/'fields.json.gz'),'proofs':str(G/'document-proofs.json.gz'),'vectors':str(G/'vectors.f64'),'binding':m['binding'],'native_generation_id':publication['generation_id']}
gid=seal_h(STORE,inputs)
result={'status':'staged_verified','generation_id':gid,'native_generation_id':publication['generation_id'],'store':str(STORE),'new_CIDs':21,'new_positive_CIDs':18,'reviewed_source_updated_CIDs':0,'all_current_document_vectors_reused_exactly':m['RID_count'],'new_document_vectors':0,'scope':'Preserve current concurrent source including exact 21 native relation-repair records and sports update; apply reviewed one-file coordinator fix only.','kernel_code_unchanged':False,'reviewed_code_delta':changed,'CURRENT_writes':0,'elapsed_seconds':time.monotonic()-t}
write(O/'successor.json',result);print(json.dumps(result),flush=True)
