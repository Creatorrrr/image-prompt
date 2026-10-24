"""Include the maintained retry verifier that audits each parent in its own seal."""
from pathlib import Path
import gc,json,sys,shutil,hashlib
gc.disable()
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(p.read_bytes());write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
prior=read(O/'rebase-1/successor.json');config=read(S/'retrieval-runtime.json');assert config['generation_id']==prior['generation_id']
out=O/'retry-compatible-release';out.mkdir(exist_ok=True)
store=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed');native=store/'generations'/config['native_generation_id']
write(out/'before.json',{'config':config,'store':str(store),'native':str(native),'h_f2':str(store/'h-f2-generations'/config['generation_id'])})
stage=O/'successor-skill';rel='scripts/prepare_retry_context.py';src=S/rel
sha=hashlib.sha256(src.read_bytes()).hexdigest();shutil.copyfile(src,stage/rel)
sys.path.insert(0,str(stage/'scripts'))
from photo_runtime_sources import SnapshotPublisher
from photo_h_f2_generation import stage as seal
import photo_candidate_corpus as c
a,b=c.load(native/'assets'),c.load(stage/'assets');assert a==b,'Candidate/source union changed during verifier overlay.'
pub=SnapshotPublisher(stage,O/'successor-store').stage();print('retry-compatible native staged',pub['generation_id'],flush=True)
g=Path(prior['store'])/'h-f2-generations'/prior['generation_id'];binding=read(g/'manifest.json')['binding']
inputs={'generation':str(g),'documents':str(g/'documents.json.gz'),'field_documents':str(g/'field-documents.json.gz'),'fields':str(g/'fields.json.gz'),'proofs':str(g/'document-proofs.json.gz'),'vectors':str(g/'vectors.f64'),'binding':binding,'native_generation_id':pub['generation_id']}
gid=seal(O/'successor-store',inputs)
result={**prior,'generation_id':gid,'native_generation_id':pub['generation_id'],'retry_verifier_sha256':sha,'retry_verifier_from_maintained_source':True,'candidate_policy_changed':False,'candidate_data_changed_since_rebase_1':False,'additional_code_members':[rel],'rebased_from':prior['generation_id'],'CURRENT_writes':0}
write(out/'successor.json',result);print(json.dumps(result),flush=True)
