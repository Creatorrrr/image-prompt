"""Inventory existing accepted current149 judgments; never create approvals."""
import gzip,hashlib,importlib.abc,json,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0,str(R));import native_reviews as nr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),sha256=c.digest(read(p)))
source_path=R/'native-inputs/root-diagnostic6-kind-source-plan-23/CURRENT-PROPOSAL.json.gz';source=read(source_path)
assert c.digest(source)=='39ab970ec8a42550f6afb41163ae6e2e76c1403f60f76cb9e5a962e3197dd65c'
catalog=c.digest(source['slot_catalog']);assignments={}
for p in(R/'native-inputs/prepared').glob('*/ASSIGNMENT.json'):assignments.setdefault(c.digest(read(p)),[]).append(p)
accepted={};history=[];stale=[];older=[]
for acceptance_path in sorted((R/'native_batches').glob('*/ROOT-ACCEPTANCE.json')):
 folder=acceptance_path.parent;batch_path=folder/'BATCH.json';batch=read(batch_path)
 if not any(r['status']=='approved' and r['proof']['catalog_sha256']==catalog for r in batch['records']):
  older.append(dict(batch=ref(batch_path),reason='No approved row on exact current149 catalog. Historical acceptance is not transferred.'));continue
 choices=assignments[batch['assignment_sha256']];assert len(choices)==1
 assignment=choices[0];verified=nr.verify_batch(assignment,batch_path,folder/'NOTE.json',root=ROOT,here=R);nr.verify_acceptance(ROOT,ref(acceptance_path),verified)
 assert verified['catalog_sha256']==catalog and verified['policies_sha256']==c.digest(source['policies'])
 row_history=[]
 for cid,row in verified['records'].items():
  if row['status']!='approved':continue
  after=row['source_after'];hashes=n.referenced_records(after,source)
  closure={k:source['candidates'][k]for k in hashes if c.ID.fullmatch(k)};bindings={k:source['slot_bindings'][k]for k in hashes if c.BINDING_ID.fullmatch(k)}
  # Dependency rows can carry their separately reviewed proof. Compare their
  # complete source meanings after removing only that proof field.
  actual={}
  for key,record in row['dependency_records'].items():
   value=json.loads(c.canonical_bytes(record));value['content'].pop('role_evidence',None);actual[key]=value
  same=after==source['candidates'][cid] and actual==closure and row['reference_bindings']==bindings
  if not same:stale.append(dict(candidate_id=cid,ordinal=row['ordinal'],batch=str(batch_path.relative_to(ROOT)),reason='Current source or full reference/binding closure differs; no approval transfer.'));continue
  proof_hash=c.digest(row['proof']);item=dict(candidate_id=cid,ordinal=row['ordinal'],proof_sha256=proof_hash,source_sha256=c.digest(after),roles=sorted(row['proof']['roles']),batch=ref(batch_path),acceptance=ref(acceptance_path))
  if cid in accepted:assert accepted[cid]['proof_sha256']==proof_hash,'Conflicting existing accepted judgments need manual latest selection'
  else:accepted[cid]=item
  row_history.append(dict(candidate_id=cid,ordinal=row['ordinal'],proof_sha256=proof_hash))
 history.append(dict(assignment=ref(assignment),batch=ref(batch_path),acceptance=ref(acceptance_path),statuses=verified['statuses'],current_equal_approved_rows=row_history))
proofs=list(accepted.values());roles={}
for row in proofs:
 for tag in row['roles']:roles[tag]=roles.get(tag,0)+1
value=dict(schema='photo-root-existing-current149-approval-inventory/v1',actor='/root',current_source=ref(source_path),catalog_sha256=catalog,whole_inventory=18250,
 existing_root_accepted_current_equal_unique_candidates=len(proofs),records=sorted(proofs,key=lambda r:r['ordinal']),accepted_history=history,stale_untransferred_rows=stale,older_catalog_batches_not_transferred=older,role_candidate_counts=roles,
 remaining_without_existing_current_equal_root_approval=18250-len(proofs),new_approvals_created=0,automatic_latest_manifest_created=False,operating_native_qualified_count=0,operating_changes=0,Gemini_calls=0,
 boundary='Read-only inventory of exact already accepted positive research judgments on current149/source102, deduplicating identical proof values and rechecking whole source plus full closure/binding identity. No unaccepted draft/diagnostic batch is imported. This is not a complete latest18250 selection, semantic re-review, operational application, final hybrid retrieval or stage5–8 completion.')
out=R/'ROOT-CURRENT149-APPROVAL-INVENTORY-01.json'
with out.open('xb')as f:f.write(c.canonical_bytes(value)+b'\n')
print(json.dumps(dict(existing_current_equal_approved=len(proofs),accepted_current149_batches=len(history),stale_rows=len(stale),older_catalog_batches=len(older),operating_native=0,new_approvals=0)))
