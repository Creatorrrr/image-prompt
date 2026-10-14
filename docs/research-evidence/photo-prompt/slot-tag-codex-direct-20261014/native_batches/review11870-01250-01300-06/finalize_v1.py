"""Exact authorized49-row reuse plus one manually repaired1255, canonical attestation and verifier."""
import json,hashlib,copy,sys
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');OLD=R/'native_batches/review11870-01250-01300-05';O=R/'native_batches/review11870-01250-01300-06';D=R/'native-inputs/prepared/review11870-01250-01300-06';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n,photo_candidate_realizations as real
sys.path.insert(0,str(R));import direct_review as dr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import native_reviews as nr
def load(p):return json.loads(p.read_text())
def pin(p):return {'file':str(p),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(load(p))}
def write(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n');return pin(p)
def row_bytes(p):
 raw=p.read_text();pos=raw.index('[',raw.index('"records"'))+1;out=[];dec=json.JSONDecoder()
 while True:
  while raw[pos].isspace()or raw[pos]==',':pos+=1
  if raw[pos]==']':break
  obj,size=dec.raw_decode(raw[pos:]);out.append((obj['candidate_id'],raw[pos:pos+size].encode()));pos+=size
 return out
A=load(D/'ASSIGNMENT.json');I=load(D/'INPUT.json');old=load(OLD/'BATCH.json');repair=load(O/'REPAIRED-1255-v1.json');checks=load(O/'CHECKS-1255-v1.json');assert checks['all_passed'];assert c.digest(repair)=='aacff0b64234dc0f5da148f9fa39b4aa29bc3b97243ed4f6a620fab50247b90e';records=copy.deepcopy(old['records']);records[5]=repair['record']
b={'schema':nr.BATCH,'task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment_sha256':c.digest(A),'input_sha256':c.digest(I),'prepared_count':50,'actual_read_count':50,'records':records};bp=O/'BATCH.json';write(bp,b)
comparisons=[]
for index,((cid,oldraw),(newcid,newraw))in enumerate(zip(row_bytes(OLD/'BATCH.json'),row_bytes(bp))):
 assert cid==newcid
 if index!=5:
  assert oldraw==newraw;assert c.canonical_bytes(old['records'][index])==c.canonical_bytes(records[index]);comparisons.append({'ordinal':records[index]['ordinal'],'candidate_id':cid,'raw_row_sha256':hashlib.sha256(newraw).hexdigest(),'canonical_row_sha256':c.digest(records[index]),'proof_sha256':None if records[index]['proof']is None else c.digest(records[index]['proof']),'unchanged_raw_row_bytes':True,'unchanged_native_signature':True})
assert len(comparisons)==49;assert [r['ordinal']for r in records if r['status']=='pending']==[1299]
note={k:b[k]for k in ['task_name','model','reasoning_effort','assignment_sha256','input_sha256','prepared_count','actual_read_count']};note.update(schema=nr.NOTE,batch_sha256=c.digest(b),whole_source_read_ids=[r['candidate_id']for r in records if r['source_reread_complete']],whole_dependency_read_ids=[r['candidate_id']for r in records if r['reference_reread_complete']]);np=O/'NOTE.json';write(np,note)
try:result=nr.verify_batch(str(D/'ASSIGNMENT.json'),str(bp),str(np));error=None
except Exception as exc:result=None;error=type(exc).__name__+': '+str(exc)
mods={}
for name,m in sorted(sys.modules.items()):
 if getattr(m,'__file__',None)and(name.startswith('photo_')or name=='prompt_generator'or Path(m.__file__).resolve().is_relative_to(G)):
  p=Path(m.__file__).resolve();assert p.is_relative_to(G),(name,p);mods[name]={'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
verification={'schema':'photo-native-targeted-repair-batch-verification/v1','task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'assignment':pin(D/'ASSIGNMENT.json'),'input':pin(D/'INPUT.json'),'batch':pin(bp),'note':pin(np),'result':result,'error':error,'module_paths_sha256':mods,'research_helpers':[{'file':str(Path(m.__file__)),'file_sha256':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()}for m in [nr,dr]],'raw_unchanged_49_rows':comparisons,'root_accepted':0,'operating':0,'boundary':'Actual exact06nr.verify_batch only.49whole source/proof/status/signature rows rawbyteidentical05; no new49read/semantic approval or resign.1255only newly reread/repaired/sealed and its fresh tests separate. Source09/catalog149/G unchanged. No source/Git/runtime/model/network edits.'};vp=O/'VERIFICATION-v1.json';write(vp,verification)
handoff={'schema':'photo-targeted-fresh-read-and-exact-reuse-handoff/v1','task_name':A['task_name'],'model':A['model'],'reasoning_effort':A['reasoning_effort'],'batch':pin(bp),'canonical_note':pin(np),'verification':pin(vp),'fresh1255':pin(O/'REPAIRED-1255-v1.json'),'fresh_controlled_checks':pin(O/'CHECKS-1255-v1.json'),'whole_prior_direct_read_provenance':pin(OLD/'RESEARCH-HANDOFF-v1.json'),'prepared_count':50,'attested_complete_read_count':50,'fresh_source_reread_count':1,'prior_direct_read_explicit_reuse_count':49,'other49_new_read_count':0,'other49_new_signature_count':0,'worker_sourceproof_count':49,'pending_ordinals':[1299],'root_acceptance_count':0,'operating':0,'actual1255_check_case_count':checks['case_count'],'actual1255_E_Rx_property_count':len(checks['expanded_properties']),'actual_controlled_proof_boundary':'66new controlled fullcompact cases, fiveactualproperties and3wholeE dimensions, bothP andsource-disjoint/callerchoice, ownbindinghuman+4denydomains, all4sourcequalifiedroles, actualalias/ancestorlocks. Fullsourceauthority fullcompactqualification all4roles equal eligible; missingauthorityreview_required retained, callerunselecteddiscoveryreview_required retained. Syntheticindependentcores only, no actualrequest/freeze/runtime/render/pixels.','immutable_scope':'05entireunacceptedbatch keptunchanged afterroot1255HOLD.06only1255duplicate nearEn deletion+ENordinarysubset+onehopApppartialref/placementrefs repair; selectedwholemeaning/current/E3groups/actualtargets/Rx/properties/modes/P/guards unchanged. Entireother49 rawrowbytes/signatures reused afterexact inputcomparison, including1299pending. Initialmetadata-heavyprinttruncation repaired by boundedwhole1255source+5B+full4spec print;49metadataexactreuse isnot49freshread.','next':'Resume separate1299-149-06 actualframeinventory/visibility/propertylock repro from READ-CHECKPOINT-v1, thenbulk1610.','source_code_Git_model_network_runtime_mutations':0};hp=O/'RESEARCH-HANDOFF-v1.json';write(hp,handoff)
print(json.dumps({'batch':pin(bp),'note':pin(np),'verification':pin(vp),'handoff':pin(hp),'statuses':result and result['statuses'],'shape_valid':result and result['shape_valid'],'error':error},ensure_ascii=False))
