"""Verify twelve exact source selections and preserve unaccepted diagnostic history."""
import ast, copy, gzip, hashlib, importlib.abc, json, subprocess, sys
from collections import Counter
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
nr=prep.reviews;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=raw(p),sha256=c.digest(read(p)))
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
def proof_values(p):
 text=p.read_text();decoder=json.JSONDecoder();i=text.index('[',text.index('"records"'))+1;values={}
 while True:
  while text[i].isspace() or text[i]==',':i+=1
  if text[i]==']':break
  row,end=decoder.raw_decode(text,i);segment=text[i:end];j=segment.index(':',segment.index('"proof"')+7)+1
  while segment[j].isspace():j+=1
  _,last=decoder.raw_decode(segment,j);values[row['candidate_id']]=segment[j:last].encode();i=end
 return values
D=R/'native-inputs/root-simple5-diagnostic7-source-plan-21';parent=R/'native-inputs/root-illumination-guard-source-plan-20'
before=read(parent/'CURRENT-PROPOSAL.json.gz');current=read(D/'CURRENT-PROPOSAL.json.gz');original=read(R/'SOURCE.json.gz');memo=read(D/'ROOT-SOURCE-SELECTION.json')
assert c.digest(before)=='a3ac73e618b4443855c9cba07a0b0f9977c65cd19d0dcb92188ea2b208fddec7'
assert c.digest(current)=='b1c48c867ce0a94d5648b0bfb7935605e4d7708951b36268930ea26523746092'
assert raw(D/'CURRENT-PROPOSAL.json.gz')=='0a6c07eba63f41df7f4b30db901dd45a8f6e71d9a0fdb51995c2e6b3906e613d'
assert len(current['candidates'])==18250 and current['slot_catalog']==before['slot_catalog'] and len(current['slot_catalog'])==149
assert all(current[k]==before[k] for k in ['slot_bindings','policies'])
approval=read(D/'SOURCE-APPROVAL.json');prep.approve_source(ROOT,original,current,approval);c.validate(current)
assert len(approval['changes'])==len({x['candidate_id'] for x in approval['changes']})==96
assert Counter(x['record_kind'] for x in current['candidates'].values())['diagnostic']==58
selected=memo['diagnostic7']+memo['simple5'];assert len(selected)==12
assert {cid for cid in current['candidates'] if current['candidates'][cid]!=before['candidates'][cid]}=={r['candidate_id'] for r in selected}
for row in memo['diagnostic7']:
 b,a=row['before'],row['after'];assert b==before['candidates'][row['candidate_id']] and a==current['candidates'][row['candidate_id']]
 assert b['record_kind']=='diagnostic' and a['record_kind']=='visual_option'
 assert {k:v for k,v in b.items() if k!='record_kind'}=={k:v for k,v in a.items() if k!='record_kind'}
for row in memo['simple5']:
 b,a=row['before'],row['after'];assert b==before['candidates'][row['candidate_id']] and a==current['candidates'][row['candidate_id']]
 assert b['conditions']==a['conditions'] and b['provenance']==a['provenance']
 if row['ordinal']==6220:assert b['effects']==a['effects']
 else:assert set(b['effects']['dimensions'])<=set(a['effects']['dimensions'])
for name,count in [('review05250-diagnostic70-149-02',70),('review05250-simple5-149-01',5)]:
 p=R/'native-inputs/prepared'/name;assignment=read(p/'ASSIGNMENT.json');inp=nr.artifact(ROOT,assignment['input']);packet=read(p/'PREPARED-PACKET.json')
 nr.validate_assignment_identity(assignment);nr.verify_catalog(original['slot_catalog'],current['slot_catalog'],inp['catalog_review'],ROOT)
 assert len(assignment['ids'])==packet['prepared_count']==count and packet['actual_read_count']==0
 assert nr.artifact(ROOT,inp['current_snapshot'])==current
 for cid in assignment['ids']:
  assert packet['current_records'][cid]==current['candidates'][cid]
  assert packet['original_records'][cid]==original['candidates'][cid]
  assert n.referenced_records(current['candidates'][cid],current)=={}
  assert packet['references'][cid]==packet['reference_bindings'][cid]=={}
O1=R/'native_batches/review05250-diagnostic70-149-01';O2=R/'native_batches/review05250-diagnostic70-149-02'
old=read(O1/'BATCH.json');new=read(O2/'BATCH.json')
assert raw(O1/'BATCH.json')=='895cd62700f3c0a9ba0b3c1652173d1052b0667f919d9897657da4c54786e97e'
assert raw(O2/'BATCH.json')=='d5401befa893cfad64ad1e88329230e747aadb5bc2ffb56c72bb0adbe13754ae'
v=nr.verify_batch(R/'native-inputs/prepared/review05250-diagnostic70-149-02/ASSIGNMENT.json',O2/'BATCH.json',O2/'NOTE.json',root=ROOT,here=R)
assert v['statuses']=={'diagnostic_reviewed':58,'approved':0,'pending':12}
oldby={r['candidate_id']:r for r in old['records']};oldvalues=proof_values(O1/'BATCH.json');newvalues=proof_values(O2/'BATCH.json')
reuse=[];withdraw=[];oldpending=[]
for cid,row in v['records'].items():
 prev=oldby[cid]
 if row['status']=='diagnostic_reviewed':
  assert row['source_after']==prev['source_after'] and row['dependency_records']==prev['dependency_records'] and row['reference_bindings']==prev['reference_bindings']
  assert row['proof']==prev['proof'] and newvalues[cid]==oldvalues[cid]
  assert not row['proof']['facts'] and not row['proof']['roles'];reuse.append(row['ordinal'])
 else:
  assert row['proof'] is None
  (withdraw if prev['proof'] else oldpending).append(row['ordinal'])
assert len(reuse)==58 and sorted(withdraw)==[12005,12023,12034,12050,12082,12156,12159] and len(oldpending)==5
assert not (O1/'ROOT-ACCEPTANCE.json').exists() and not (O2/'ROOT-ACCEPTANCE.json').exists()
hold=R/'ROOT-DIAGNOSTIC70-01-HOLD-07.json'
save(hold,dict(schema='photo-root-diagnostic-history-hold/v1',actor='/root',prior_batch=ref(O1/'BATCH.json'),latest_batch=ref(O2/'BATCH.json'),prior65_diagnostic_not_root_accepted=True,withdrawn_ordinals=sorted(withdraw),restored_positive_pending_ordinals=sorted(withdraw+oldpending),exact_unchanged_proof_byte_reuse_count=58,new_signature_count=0,new_unique_bulk_read_credit=0,latest58_diagnostic_not_root_accepted=True,additional_consistency_recheck_requested=[12016,12041,12044,12055,12056,12369],reason='Root preserves prior individual direct source reading but does not infer all remaining router/guard classifications from kind, missing parameters, empty effects or shape. Six further whole-source positive/conditional clauses require consistency review against restored templates. Neither historical batch is partially or wholly accepted; no source/proof is overwritten.'))
paths=[Path(__file__).resolve(),R/'prepare_simple5_and_diagnostic7_root_01.py',hold,ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md']
paths.extend(p for p in D.rglob('*') if p.is_file())
for name in ['review05250-diagnostic70-149-02','review05250-simple5-149-01']:
 paths.extend(p for p in (R/'native-inputs/prepared'/name).rglob('*') if p.is_file())
for folder in [O1,O2]:paths.extend(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
for folder,pattern in [(R/'authored','native_diag70_05250_recheck7.*'),(R/'worker-notes','native_diag70_05250_recheck7.*'),(R/'authored','native_05250_simple5-source-applications-source84-149-v1*'),(R/'worker-notes','native_05250_simple5-source-applications-source84-149-v1*'),(R/'authored','native_diag70_05250_source96-*')]:paths.extend(p for p in folder.glob(pattern) if p.is_file())
pins={}
for p in sorted(set(paths)):
 if p.suffix=='.json':read(p)
 if p.suffix=='.py':ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=raw(p)
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name,pin in protected.items():assert raw(ROOT/name)==pin
report=dict(schema='photo-root-source96-preparation-verification/v1',actor='/root',source=ref(D/'CURRENT-PROPOSAL.json.gz'),source_changes_unique=96,new_source_applications=5,new_kind_restorations=7,total_positive_kind_restorations=12,whole_inventory=18250,research_diagnostic_count=58,catalog_count=149,bindings_policies_unchanged=True,prepared_sparse_counts=[70,5],preparation_actual_read_claim=0,historical_diagnostic_batch_hold=ref(hold),latest_diagnostic_shape_statuses=v['statuses'],latest_diagnostic_root_accepted=False,root_read_scope=memo['root_read_scope'],operating_changes=0,operating_native_qualified=0,Gemini_calls=0,all_remaining_stages_complete=False,files=pins,protected_files=protected)
output=R/'ROOT-SIMPLE5-DIAGNOSTIC7-PREPARATION-01.json';save(output,report)
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
names=sorted(set(pins)|{str(output.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True)
expected=set()
for name in names:
 previous=subprocess.run(['git','show','HEAD:'+name],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 if previous.returncode or previous.stdout!=(ROOT/name).read_bytes():expected.add(name)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==expected
subprocess.run(['git','diff','--cached','--check'],check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(cached_files=len(expected),unique_source_changes=96,positive_kind_pending=12,diagnostic58_accepted=False,prepared_sparse=[70,5],Gemini_calls=0,operating_changes=0)))
