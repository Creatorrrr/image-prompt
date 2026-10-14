"""Verify exact scoped preparation, without approving its source semantics/native execution."""
import ast,gzip,hashlib,json,subprocess
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def sha(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
parent=read(R/'native-inputs/root-noise-contract-source-plan-13/CURRENT-PROPOSAL.json.gz')
D=R/'native-inputs/root-hands-exchange-source-plan-14';current=read(D/'CURRENT-PROPOSAL.json.gz')
assert sha(current)=='8acdd741cdb846c8bb33b53ded16471363ece5747280b5b4893c25acdeed302d'
cid='cand_2e72784a26885ceaa1d645d25bd9a468'
assert [key for key in current['candidates']if current['candidates'][key]!=parent['candidates'][key]]==[cid]
assert all(current[key]==parent[key]for key in ['slot_catalog','slot_bindings','policies'])
assert sha(current['candidates'][cid])=='e9870bd290b1bd682d9d79001c29a4affa65a4618ce2ed0cd43d46b0d15cfd33'
P=R/'native-inputs/prepared/review11870-01299-149-06';receipt=read(P/'PREPARATION.json');assignment=read(P/'ASSIGNMENT.json')
assert receipt['prepared_count']==1 and receipt['actual_read_count']==0 and receipt['native_proof_written']is False
assert assignment['ids']==[cid]and assignment['ordinals']==[1299]and assignment['task_name']=='/root/review_11870_12250'
assert (assignment['model'],assignment['reasoning_effort'])==('gpt-6.1-sol','high')
for reference in receipt['documents'].values():
 path=ROOT/reference['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==reference['file_sha256']and sha(read(path))==reference['sha256']
paths=[p for folder in [D,P]for p in folder.iterdir()if p.is_file()]
paths.extend([R/'prepare_hands_exchange_root_01.py',Path(__file__).resolve(),ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
pins={}
for path in paths:
 raw=path.read_bytes()
 if path.suffix=='.json':json.loads(raw)
 if path.suffix=='.py':ast.parse(raw)
 pins[str(path.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest()
report={'schema':'photo-root-hands-exchange-preparation-verification/v1','actor':'/root','files':pins,
 'source_literal_selected_for_fresh_review':True,'original_source_changes_total':65,'changed_from_parent':[cid],
 'prepared_candidate_count':1,'actual_new_worker_reads_from_preparation':0,'native_proofs_created':0,
 'prior_first50_pending_status_changed':False,'source_choice_boundary':'Explicit physical-handoff editorial restriction is disclosed in EN/KO and selection memo. Other exchange interpretations are not claimed as preserved. This is not source-native approval or actual complete framing-inventory verification.',
 'catalog_bindings_policies_equal_parent':True,'operating_changes':0,'model_embedding_Gemini_calls':0}
output=R/'ROOT-HANDS-EXCHANGE-PREPARATION-01.json'
with output.open('x')as f:json.dump(report,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
names=sorted(set(pins)|{str(output.relative_to(ROOT))});subprocess.run(['git','add','--',*names],cwd=ROOT,check=True);subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name],cwd=ROOT)==(ROOT/name).read_bytes(),name
print(json.dumps({'staged_paths':len(names),'prepared':1,'new_native_proofs':0,'source_literal_selection_only':True}))
