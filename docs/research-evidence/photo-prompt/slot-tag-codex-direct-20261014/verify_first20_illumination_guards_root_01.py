"""Check exact existing-source guards and stage the research-only fresh input."""
import ast,gzip,hashlib,json,subprocess
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
cache={}
def refs(v):
 if isinstance(v,dict):
  if set(v)=={'file','file_sha256','sha256'}:
   p=ROOT/v['file']
   if p not in cache:cache[p]=(hashlib.sha256(p.read_bytes()).hexdigest(),digest(read(p)))
   assert cache[p]==(v['file_sha256'],v['sha256'])
  for x in v.values():refs(x)
 elif isinstance(v,list):
  for x in v:refs(x)
D=R/'native-inputs/root-illumination-guard-source-plan-20';P=R/'native-inputs/prepared/review06250-00000-00020-149-04'
current=read(D/'CURRENT-PROPOSAL.json.gz');parent=read(R/'native-inputs/root-first20-source-plan-19/CURRENT-PROPOSAL.json.gz');memo=read(D/'ROOT-SOURCE-SELECTION.json')
assert digest(current)=='a3ac73e618b4443855c9cba07a0b0f9977c65cd19d0dcb92188ea2b208fddec7'
rows=memo['records'];assert len(rows)==7 and {r['ordinal'] for r in rows}=={0,1,2,6,7,11,12}
assert {cid for cid in current['candidates'] if current['candidates'][cid]!=parent['candidates'][cid]}=={r['candidate_id'] for r in rows}
for row in rows:
 cid=row['candidate_id'];a=row['whole_after'];b=row['whole_before']
 assert a==current['candidates'][cid] and b==parent['candidates'][cid] and b['conditions']=={}
 assert all(a[k]==b[k] for k in ('id','record_kind','effects','provenance'))
 assert {k:v for k,v in a['content'].items() if k!='application_contract'}=={k:v for k,v in b['content'].items() if k!='application_contract'}
 assert a['content']['application_contract'].startswith(b['content']['application_contract'])
 guards=a['conditions']['native_guards'];assert guards['schema']=='photo-native-source-guards/v3'
 rule=next(x for x in guards['rules'] if x['id']=='every_receiver_already_illuminated_by_that_source')
 assert rule['kind']=='for_each_member' and rule['scope']=={'kind':'source_target','candidate_id':cid,'target':'illuminated_receivers'}
 sub=rule['rule'];assert sub['kind']=='frozen_entity_relation' and sub['left']=={'kind':'bound_member','variable':'receiver'} and sub['right']=={'kind':'source_target','candidate_id':cid,'target':'illuminating_light'}
 assert sub['property']=='lighting.received_from' and sub['value_type']=='entity.owner_id/v1'
 names={x['id'] for x in guards['rules']}
 if row['ordinal']==1:assert 'actual_lab_use_designation' in names
 if row['ordinal']==11:assert {'source_of_same_scene','receivers_of_same_scene'}<=names and set(a['effects']['dimensions'])=={'lighting','timing'}
 if row['ordinal']==12:assert {'existing_window_path','established_window_route','path_from_same_source','every_receiver_on_same_window_path'}<=names
assert all(current[k]==parent[k] for k in ('slot_catalog','slot_bindings','policies'))
assert len(read(D/'SOURCE-APPROVAL.json')['changes'])==84
assignment=read(P/'ASSIGNMENT.json');packet=read(P/'PREPARED-PACKET.json');receipt=read(P/'PREPARATION.json')
assert len(assignment['ids'])==20 and assignment['ordinals']==list(range(20)) and packet['ids']==assignment['ids']
assert receipt['prepared_count']==20 and receipt['actual_read_count']==0 and not receipt['native_proof_written'] and not receipt['canonical_applied']
for cid in assignment['ids']:assert packet['current_records'][cid]==current['candidates'][cid]
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name,h in protected.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
paths=[R/'prepare_first20_illumination_guards_root_01.py',Path(__file__),*sorted(D.iterdir()),*sorted(P.iterdir()),R/'authored/native_06250_first20_149_03.guard-source-proposals.json',R/'worker-notes/native_06250_first20_149_03.guard-source-proposals-read01.json',ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'];pins={}
for p in paths:
 if p.suffix in ('.json','.gz'):refs(read(p))
 elif p.suffix=='.py':ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
report=R/'ROOT-FIRST20-ILLUMINATION-GUARDS-01.json';value=dict(schema='photo-root-illumination-source-verification/v1',actor='/root',source_changes_total=84,refined_existing_CIDs=7,all_original_effects_exact=True,all_old_positive_fields_preserved=True,whole7_proposed_after_read_by_root=True,full_source_and_catalog_validation_passed_during_preparation=True,actual_worker_reads_from_preparation=0,native_approvals=0,operating_changes=0,Gemini_calls=0,files=pins,protected_files=protected)
with report.open('xb') as f:f.write(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n')
names=sorted(set(pins)|{str(report.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);subprocess.run(['git','diff','--cached','--check'],check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==set(names)
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(files=len(names),refined_existing_CIDs=7,new_native_approvals=0,operating_changes=0,Gemini_calls=0)))
