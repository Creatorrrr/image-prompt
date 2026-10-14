"""Verify thirteen exact choices, unchanged seven proofs, and stage only input work."""
import ast,gzip,hashlib,json,subprocess
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
cache={}
def reference(v):
 if isinstance(v,dict):
  if set(v)=={'file','file_sha256','sha256'}:
   p=ROOT/v['file']
   if p not in cache:cache[p]=(hashlib.sha256(p.read_bytes()).hexdigest(),digest(read(p)))
   assert cache[p]==(v['file_sha256'],v['sha256'])
  for x in v.values():reference(x)
 elif isinstance(v,list):
  for x in v:reference(x)
D=R/'native-inputs/root-first20-source-plan-19';P=R/'native-inputs/prepared/review06250-00000-00020-149-03'
parent=read(R/'native-inputs/root-diagnostic-kind-source-plan-18/CURRENT-PROPOSAL.json.gz');current=read(D/'CURRENT-PROPOSAL.json.gz');memo=read(D/'ROOT-SOURCE-SELECTION.json')
assert digest(current)=='609e72864631ffccd711d2a6601ac060bea0a92f86985c7633a3fbea59d82ae5'
selected={r['candidate_id']:r for r in memo['selected']};assert len(selected)==13
assert {cid for cid in current['candidates'] if current['candidates'][cid]!=parent['candidates'][cid]}==set(selected)
for cid,row in selected.items():
 before=parent['candidates'][cid];after=current['candidates'][cid]
 assert before==row['whole_before'] and after==row['whole_after'] and before['effects']['properties']==[]
 assert {k:v for k,v in after.items() if k not in ('content','effects')}=={k:v for k,v in before.items() if k not in ('content','effects')}
 assert {k:v for k,v in after['content'].items() if k!='application_contract'}==before['content']
 assert set(before['effects']['dimensions'])<=set(after['effects']['dimensions'])
 if row['ordinal']==11:assert row['alternative_id']=='actual_natural_golden_hour' and set(after['effects']['dimensions'])=={'lighting','timing'}
 else:assert before['effects']['dimensions']==after['effects']['dimensions']
 if row['ordinal']==14:assert after['effects']=={'dimensions':['setting'],'properties':[{'dimension':'setting','target':'image','property':'setting.aesthetic_reading'}]}
assert all(current[k]==parent[k] for k in ('slot_catalog','slot_bindings','policies'))
assert len(read(D/'SOURCE-APPROVAL.json')['changes'])==84
old=read(R/'native_batches/review06250-00000-00020-149-02/BATCH.json');unchanged=[]
for row in old['records']:
 cid=row['candidate_id']
 if row['status']=='approved':
  assert cid not in selected and current['candidates'][cid]==parent['candidates'][cid]==row['source_after']
  assert row['proof']['catalog_sha256']==digest(current['slot_catalog']);unchanged.append(cid)
assert len(unchanged)==7
assignment=read(P/'ASSIGNMENT.json');inp=read(P/'INPUT.json');packet=read(P/'PREPARED-PACKET.json');receipt=read(P/'PREPARATION.json')
assert assignment['ids']==inp['ids']==packet['ids'] and len(assignment['ids'])==20 and assignment['ordinals']==list(range(20))
assert assignment['task_name']=='/root/review_06250_07250' and assignment['model']=='gpt-6.1-sol' and assignment['reasoning_effort']=='high'
assert receipt['prepared_count']==20 and receipt['actual_read_count']==0 and not receipt['native_proof_written'] and not receipt['canonical_applied']
for i,row in enumerate(old['records']):
 cid=row['candidate_id'];req=inp['required_revisions'][cid]
 assert req['prior_review']['pointer']=='/records/'+str(i) and req['prior_review']['sha256']==digest(row)
 assert packet['current_records'][cid]==current['candidates'][cid]
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name,h in protected.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
paths=[R/'prepare_first20_source_choices_root_01.py',Path(__file__),*sorted(D.iterdir()),*sorted(P.iterdir()),ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'];pins={}
for p in paths:
 if p.suffix in ('.json','.gz'):reference(read(p))
 elif p.suffix=='.py':ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
report=R/'ROOT-FIRST20-SOURCE-CHOICES-01.json';v=dict(schema='photo-root-source-choice-verification/v1',actor='/root',new_source_choices=13,source_changes_total=84,prepared_count=20,unchanged_existing_proof_pairs=unchanged,new_native_proofs=0,new_native_approvals=0,operating_changes=0,Gemini_calls=0,original_dimensions_preserved=True,original_properties_renamed=0,catalog_bindings_policies_unchanged=True,whole14_proposed_after_and15_relevant_full_specs_read_by_root=True,files=pins,protected_files=protected)
with report.open('xb') as f:f.write(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n')
names=sorted(set(pins)|{str(report.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);subprocess.run(['git','diff','--cached','--check'],check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==set(names)
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(files=len(names),source_choices=13,unchanged_proof_pairs=7,new_native_approvals=0,operating_changes=0,Gemini_calls=0)))
