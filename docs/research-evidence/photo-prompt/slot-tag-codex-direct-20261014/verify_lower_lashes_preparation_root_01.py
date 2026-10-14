"""Verify one literal source selection and its immutable review-only input."""
import ast,gzip,hashlib,json,subprocess
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def refs(v):
 if isinstance(v,dict):
  if {'file','file_sha256','sha256'}<=v.keys():
   p=ROOT/v['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==v['file_sha256'];assert digest(read(p))==v['sha256']
  for x in v.values():refs(x)
 elif isinstance(v,list):
  for x in v:refs(x)
D=R/'native-inputs/root-lower-lashes-source-plan-16-R02';P=R/'native-inputs/prepared/review05250-10352-149-01';parent=read(R/'native-inputs/root-hands-exchange-source-plan-14/CURRENT-PROPOSAL.json.gz');current=read(D/'CURRENT-PROPOSAL.json.gz');memo=read(D/'ROOT-SOURCE-SELECTION.json');cid=memo['candidate_id']
assert [k for k in current['candidates']if current['candidates'][k]!=parent['candidates'][k]]==[cid]
for k in set(current)-{'candidates'}:assert current[k]==parent[k]
before=parent['candidates'][cid];after=current['candidates'][cid];assert before==memo['whole_before'] and after==memo['whole_after']
assert {k:v for k,v in after['content'].items()if k!='application_contract'}==before['content'];assert all(after[k]==before[k]for k in after if k!='content')
assert digest(current)=='60bc1ace6319f7970732e50a470da9131ca9ab4c394781de79df03e5025c83ca'
assert digest(current['slot_catalog'])=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
receipt=read(P/'PREPARATION.json');assignment=read(P/'ASSIGNMENT.json');assert receipt['prepared_count']==1 and receipt['actual_read_count']==0 and not receipt['native_batch_written']and not receipt['native_proof_written']and not receipt['canonical_applied']and not receipt['root_acceptance_written']
assert assignment['ids']==[cid]and assignment['ordinals']==[10352]and assignment['task_name']=='/root/review_05250_06250'and assignment['model']=='gpt-6.1-sol'and assignment['reasoning_effort']=='high'
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for path,h in protected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
paths=[R/'prepare_lower_lashes_149_root_01.py',R/'prepare_lower_lashes_149_root_01_R02.py',Path(__file__),*sorted(D.iterdir()),*sorted(P.iterdir()),*sorted((R/'native-inputs/root-lower-lashes-source-plan-16').iterdir()),R/'authored/native_extra_10250_11250.10350_10375.source_proposals.json',R/'worker-notes/native_extra_10250_11250.formal-authoring-candidates-01.json']
pins={}
for p in paths:
 if p.suffix in ['.json','.gz']:refs(read(p))
 elif p.suffix=='.py':ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
report=R/'ROOT-LOWER-LASHES-PREPARATION-01.json';v={'schema':'photo-root-source-preparation-verification/v1','actor':'/root','selected_source_literal':cid,'ordinal':10352,'source_changes_total':66,'other_source_proposals_selected':0,'original_effect_conditions_provenance_exact':True,'catalog_bindings_policies_unchanged':True,'input_prepared':1,'root_full_source5B_binding_after_read_count':1,'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0,'failed_attempt':'Missing mandatory before:null rejected by strict delta validation; immutable R02 changes only that delta metadata.','files':pins,'protected_files':protected}
with report.open('xb')as f:f.write(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n')
names=sorted(set(pins)|{str(report.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);subprocess.run(['git','diff','--cached','--check'],check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==set(names)
for path in names:assert subprocess.check_output(['git','show',':'+path])==(ROOT/path).read_bytes()
print(json.dumps({'files':len(names),'selected_source_literals':1,'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0}))
