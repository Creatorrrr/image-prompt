"""Lossless serialization of fifty already individually authored and frozen manual decisions."""
import json,gzip,hashlib,sys,copy
from pathlib import Path
R=Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');D=R/'native-inputs/prepared/review11870-01250-01300-03';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/534cde26ba2156cf1760542d5be3a36e82b5457972d85f69d2a2fa8a7c0d50d2');sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
I=json.loads((D/'INPUT.json').read_text());A=json.loads((D/'ASSIGNMENT.json').read_text());P=json.loads((D/'PREPARED-PACKET.json').read_text());S=json.loads(gzip.decompress(Path(I['current_snapshot']['file']).read_bytes()));CAT=I['catalog_review']['after']
assert c.digest(I)=='db1f809df8dc01e11f9855d4c9554a767e5a1dcb2a1e60a7dfc0eb196c20630a'
assert c.digest(A)=='68e47bd6db1d0d1a7e62f8a692a9ce25e0aa402cd5a230887e7a2a8f0427effb'
assert c.digest(S)=='30924a72de7d3011af26b7ef7c0192ff12edd732131f3c18ed29748e805d5477'
assert c.digest(CAT)=='5bc5f6d185b6ef6e2d8d3a2bf6e4aa02d73e22143b0529a233fd5f98ddbed908'
rows=[];bindings=[]
for start in range(1250,1300,5):
 path=R/f'authored/native_11870_formal03_checkpoint_{start:05}_{start+5:05}.json';block=json.loads(path.read_text());assert block['input_sha256']==c.digest(I)and block['assignment_sha256']==c.digest(A);assert [x['ordinal']for x in block['records']]==list(range(start,start+5));rows.extend(copy.deepcopy(block['records']));bindings.append({'file':str(path),'sha256':c.digest(block),'file_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
assert [r['candidate_id']for r in rows]==A['ids']and [r['ordinal']for r in rows]==A['ordinals']
pending=[1253,1255,1256,1258,1264,1266,1267,1271,1273,1275,1278,1284,1285,1287,1295,1296,1299]
assert [r['ordinal']for r in rows if r['status']=='pending']==pending
assert sum(r['status']=='approved'for r in rows)==33
for r in rows:
 cid=r['candidate_id'];assert r['source_before']==P['original_records'][cid]and r['source_after']==P['current_records'][cid];assert r['source_reread_complete']and r['reference_reread_complete'];assert r['dependency_records']==r['reference_bindings']==P['references'][cid]==P['reference_bindings'][cid]=={}
 if r['proof'] is not None:
  before_proof_sha=c.digest(r['proof']);record=copy.deepcopy(r['source_after']);record['content']['role_evidence']=r['proof'];n.validate(record,CAT,catalog_sha256=c.digest(CAT),corpus=S);assert c.digest(r['proof'])==before_proof_sha
  actual={}
  for f in r['proof']['facts']:
   if f['mode']=='effect':actual.setdefault((f['realization_id'],f['target'],f['dimension'],f['property']),set()).add(c.digest([f['value'],f['operation'],sorted(f['receivers'])]))
  assert all(len(v)==1 for v in actual.values())
 else:assert r['status']=='pending'
out=R/'native_batches/review11870-01250-01300-03';out.mkdir(exist_ok=True);bp=out/'BATCH.json';np=out/'NOTE.json';assert not bp.exists()and not np.exists()
base={'task_name':'/root/review_11870_12250','model':'gpt-6.1-sol','reasoning_effort':'high','assignment_sha256':c.digest(A),'input_sha256':c.digest(I),'prepared_count':50,'actual_read_count':50}
batch={'schema':'photo-codex-native-review-batch/v1',**base,'records':rows};note={'schema':'photo-codex-native-review-note/v1',**base,'batch_sha256':c.digest(batch),'whole_source_read_ids':A['ids'],'whole_dependency_read_ids':A['ids']}
bp.write_text(json.dumps(batch,ensure_ascii=False,sort_keys=True,indent=2)+'\n');np.write_text(json.dumps(note,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print('BATCH',c.digest(batch),hashlib.sha256(bp.read_bytes()).hexdigest());print('NOTE',c.digest(note),hashlib.sha256(np.read_bytes()).hexdigest());print('50 individually authored rows,33 source proofs revalidated in-memory,17 explicit pending. No re-signing/root batch verification/registration/runtime/operating acceptance.')
