"""Accept one exact bounded research proof after root semantic review; no activation."""
import hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];D=R/'native_batches/review11870-01267-05';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as native
sys.path.insert(0,str(R));import native_reviews as reviews
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(p.read_bytes())
def save(p,v):
 with p.open('xb') as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
b=read(D/'BATCH.json');assert c.digest(b)=='69dc627f61356ea9fc7022fe3c9af3962b205904e750fa73294a304d00b89491';row=b['records'][0];assert row['status']=='approved' and len(row['proof']['facts'])==11 and len(row['proof']['source_units'])==4
check=read(D/'CHECKS-v2.json');assert check['all_passed'] and len(check['full_compact_admission'])==18 and len(check['actual_old_binding_consumers'])==9 and len(check['actual_target_receiver_locks'])==6 and check['whole_lighting_closed_denied']
verified=reviews.verify_batch(str((R/'native-inputs/prepared/review11870-01267-05/ASSIGNMENT.json').relative_to(ROOT)),str((D/'BATCH.json').relative_to(ROOT)),str((D/'NOTE.json').relative_to(ROOT)),root=ROOT,here=R)
reason=('Root accepts this exact146V5 research judgement after complete original/current/prepared historical5B/binding/emptyclosure, all11facts4units/3roles/maps/guards/allactual effects and receivers and full selected/neighbor specs direct review. The bounded editorial application requires existing actual shrine-lantern light source, illumination carrier and selected spatial region; it applies the actual source-use and grid lighting effects with all actual source/region receivers. The selected region is not an already-grid prerequisite. No shrine architecture/faith/location/fog/scattering/physical surface is inferred. Original conditions, originalbinding and all lighting effects/locks remain cumulative. Worker18fullcompact/9oldbinding/6target-and-receiver locks/wholelighting check on frozen07143 are worker evidence reviewed by root, not root reruns. Root independently verifies batch and acceptance on frozen188c. No operating source/catalog/tag/native activation or final149 proof conversion, runtime request/search or pixel approval.')
a={'schema':reviews.ACCEPTANCE,'actor':'/root',**{k:verified[k] for k in ['assignment_sha256','input_sha256','batch_sha256','note_sha256']},'reviews':{cid:{'review_sha256':c.digest(r),'status':r['status']}for cid,r in verified['records'].items()},'reason':reason};save(D/'ROOT-ACCEPTANCE.json',a);reviews.verify_acceptance(ROOT,ref(D/'ROOT-ACCEPTANCE.json'),verified)
modules={}
for name,m in sys.modules.copy().items():
 if name.startswith('photo_') and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);modules[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
save(D/'ROOT-VERIFICATION-01.json',{'schema':'photo-root-bounded-lantern-grid-verification/v1','accepted':ref(D/'ROOT-ACCEPTANCE.json'),'worker_checks':ref(D/'CHECKS-v2.json'),'worker_frozen_generation':check['frozen_generation'],'root_frozen_generation':str(G),'root_modules':modules,'root_consumer_reruns':0,'operating_native_qualified_records':0,'Gemini_and_model_calls':0,'full_stages_complete':False});print('PASS research acceptance1 facts11 units4; operating0')
