"""Root scoped149 research acceptance after direct focused and delegated whole review."""
import copy,hashlib,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];D=R/'native_batches/review08250-17437-06';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/188c56270ebc2c973defd3307d8fa43df60e55701baa30c45367a4e2e3efe2bb');sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as native
sys.path.insert(0,str(R));import native_reviews as reviews
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(p.read_bytes())
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
def normalize(v):
 if isinstance(v,str):return 'g06_'+v[4:] if v.startswith('g05_')else v
 if isinstance(v,list):return [normalize(x)for x in v]
 if isinstance(v,dict):return {k:normalize(x)for k,x in v.items()}
 return v
handoff=R/'worker-notes/native-08250-special17437-06-handoff-20261015.json';assert hashlib.sha256(handoff.read_bytes()).hexdigest()=='4599f3f16ae500a16b7bf9dbacc30209f64a9e0b759249951e5bc2357ae16fdd';H=read(handoff)
for a in H['artifacts']:assert hashlib.sha256(Path(a['file']).read_bytes()).hexdigest()==a['raw_sha256'],a['file']
b=read(D/'BATCH.json');assert c.digest(b)=='6b61c3b6f7e857bfe71c6716c9e011a29a703073b31953fa2b35dde075eed5a7';old=read(R/'native_batches/review08250-17437-05/BATCH.json')['records'][0];row=b['records'][0];assert row['source_after']==old['source_after'] and row['status']=='approved';before,after=normalize(old['proof']),row['proof'];audit=read(R/'authored/native_fresh_08250_17437_06_exact_audit.json');assert len(audit['exact_six_reference_repairs'])==6
for delta in audit['exact_six_reference_repairs']:
 idx=delta['source_unit_index'];assert before['source_units'][idx]==normalize(delta['before']);expected=copy.deepcopy(before['source_units'][idx]);expected['fact_refs']=expected['fact_refs'][:2];assert expected==after['source_units'][idx]==delta['after'];before['source_units'][idx]=expected
 instruction=delta['separate_actual_instruction_baseline_reference'];assert instruction in after['source_units'];assert 'smug haughty baseline remains legible' in instruction['quote'];assert len(instruction['fact_refs'])==2
before['catalog_sha256']=after['catalog_sha256'];before['roles']['body_pose']['spec_sha256']=after['roles']['body_pose']['spec_sha256'];before.pop('review');actual=copy.deepcopy(after);actual.pop('review');assert before==actual,'unexpected semantic difference beyond six gates/bodypose149 binding';assert len(after['facts'])==483 and len(after['source_units'])==786 and len(after['guard_supports'])==18;assert len([x for x in after['facts']if x['mode']=='effect'])==138 and all(not x['receivers']for x in after['facts']if x['mode']=='effect')
verified=reviews.verify_batch(str((R/'native-inputs/prepared/review08250-17437-06/ASSIGNMENT.json').relative_to(ROOT)),str((D/'BATCH.json').relative_to(ROOT)),str((D/'NOTE.json').relative_to(ROOT)),root=ROOT,here=R)
reason=('Root accepts this exact149V6 scoped research judgement using fresh sol/high whole original/current/actual5B/bindings/emptyclosure/18RIDs/483facts786units18supports/all204precision occurrences and12used+14neighbor fullspec review, plus prior independent peer whole review. Root directly read all6 complete gate before/afters and their actual separate full cheek instructions/baseline-reference units, exact retained common instruction, bodypose149 fullspec and losslessly factored18 unchanged poised-bearing facts. Root mechanically proves all other semantic source/proof payloads unchanged after explicit ID normalization and the reviewed bodypose spec binding. Six gates now reference only cheek presence/color; all canonical eye/expression/age/body/help/setback/recovery effects, actual owners, P/PR, qualifiers, profiles and guards remain. Worker1290admission/500locks/250profile/7shape/9guard/432role/36final-signed fullcompact checks are delegated frozen188c evidence, not root consumer reruns. Instrument clauses remain conditional: this proof qualifies no-tool application only; future concrete-tool applications require their own independently existing owned tool and are not certified. No native operating activation, full149 hybrid search, actual request/render/pixel or fullstage completion.')
a={'schema':reviews.ACCEPTANCE,'actor':'/root',**{k:verified[k]for k in ['assignment_sha256','input_sha256','batch_sha256','note_sha256']},'reviews':{cid:{'review_sha256':c.digest(v),'status':v['status']}for cid,v in verified['records'].items()},'reason':reason};save(D/'ROOT-ACCEPTANCE.json',a);reviews.verify_acceptance(ROOT,ref(D/'ROOT-ACCEPTANCE.json'),verified)
modules={}
for name,m in sys.modules.copy().items():
 if name.startswith('photo_')and getattr(m,'__file__',None):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);modules[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
save(D/'ROOT-VERIFICATION-01.json',{'schema':'photo-root-profile17437-six-gate-verification/v1','acceptance':ref(D/'ROOT-ACCEPTANCE.json'),'handoff':ref(handoff),'root_focused_read':'All6 actual complete gate repair pairs and separate full instructions/reference units, common exact18 instruction, wholebody149 spec and exact18 bearing-fact template. Root did not personally read all483facts786units204precision occurrences.','other_semantic_payload_exactly_preserved':True,'root_full_batch_and_acceptance_verified':True,'root_consumer_reruns':0,'root_frozen_modules':modules,'tool_bearing_application_qualified':False,'operating_native_qualified':0,'Gemini_and_model_calls':0,'stages_complete':False});print('PASS exact149 research1;483facts/786units/18supports; operating0')
