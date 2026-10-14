"""Attestation shape packaging only; existing direct reading/status/proofs unchanged."""
import sys,json,hashlib
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');O=R/'native_batches/review11870-01250-01300-04';D=R/'native-inputs/prepared/review11870-01250-01300-04'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/07143a62ae23201a5cceedf155a985e204256740da96fc083e703d8ac5e7ba07')
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n,photo_candidate_realizations as real
sys.path.insert(0,str(R));import direct_review as dr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import native_reviews as nr
b=json.loads((O/'BATCH.json').read_text());old=json.loads((O/'NOTE.json').read_text());a=json.loads((D/'ASSIGNMENT.json').read_text())
assert c.digest(b)=='4d55aef65775e0dc7f85e3446196195be8875b6700c590f3e5894620b0259c94'
assert c.digest(old)=='0bf5d3c2743c5ce814e37673158fc98ab2279bea9482988b65c5174211473173'
assert old['actual_direct_source_read_count']==b['actual_read_count']==50
assert [r['ordinal']for r in b['records']if r['status']=='pending']==[1257,1264,1267,1285,1299]
note={k:b[k]for k in ['task_name','model','reasoning_effort','assignment_sha256','input_sha256','prepared_count','actual_read_count']}
note.update(schema=nr.NOTE,batch_sha256=c.digest(b),whole_source_read_ids=[r['candidate_id']for r in b['records']if r['source_reread_complete']],whole_dependency_read_ids=[r['candidate_id']for r in b['records']if r['reference_reread_complete']])
np=O/'CANONICAL-NOTE-v1.json';assert not np.exists();np.write_text(json.dumps(note,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
try:result=nr.verify_batch(str(D/'ASSIGNMENT.json'),str(O/'BATCH.json'),str(np));error=None
except Exception as exc:result=None;error=type(exc).__name__+': '+str(exc)
def pin(p):
 raw=p.read_bytes();return {'file':str(p),'file_sha256':hashlib.sha256(raw).hexdigest(),'sha256':c.digest(json.loads(raw))}
mods={k:{'file':str(Path(m.__file__).resolve()),'file_sha256':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()}for k,m in sys.modules.items()if k.startswith(('photo_','visual_profile'))and getattr(m,'__file__',None)and Path(m.__file__).suffix=='.py'}
assert all(Path(v['file']).is_relative_to(G)for v in mods.values())
out={'schema':'photo-worker-canonical-attestation-shape-verification/v1','task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','boundary':'Mechanical exact NOTE-field packaging of existing frozen direct-reading attestation only. No extra source read, semantic acceptance, proof/status/signature/source/runtime change. Rich research NOTE remains immutable.','rich_research_note':pin(O/'NOTE.json'),'batch':pin(O/'BATCH.json'),'canonical_note':pin(np),'assignment':pin(D/'ASSIGNMENT.json'),'result':result,'error':error,'module_paths_sha256':mods,'research_helpers':[{'file':str(Path(m.__file__)),'file_sha256':hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest()}for m in [nr,dr]],'root_acceptance_count':0,'operating_count':0,'network_provider_Git':0}
op=O/'CANONICAL-NOTE-VERIFICATION-v1.json';assert not op.exists();op.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');print(json.dumps({'canonical_note':pin(np),'verification':pin(op),'result':result,'error':error},ensure_ascii=False))
