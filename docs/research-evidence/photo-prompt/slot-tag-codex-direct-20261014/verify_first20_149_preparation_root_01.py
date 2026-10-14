"""Check exact preparation references and review-only boundaries before a narrow commit."""
import gzip,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def digest(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def check_refs(v):
 if isinstance(v,dict):
  if set(['file','file_sha256','sha256'])<=v.keys():
   p=ROOT/v['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==v['file_sha256'];assert digest(read(p))==v['sha256']
  for x in v.values():check_refs(x)
 elif isinstance(v,list):
  for x in v:check_refs(x)
d=R/'native-inputs/first20-catalog149-recheck-plan-15';p=R/'native-inputs/prepared/review06250-00000-00020-149-02';plan=read(d/'PLAN.json');check_refs(plan)
current=read(ROOT/plan['current_proposal']['file']);before=read(R/'native-inputs/root-hands-exchange-source-plan-14/CURRENT-PROPOSAL.json.gz');assert current==before
packet=read(p/'PREPARED-PACKET.json');receipt=read(p/'PREPARATION.json');assignment=read(p/'ASSIGNMENT.json');inp=read(p/'INPUT.json')
assert packet['ids']==assignment['ids']==inp['ids']==plan['assignment']['ids'];assert len(packet['ids'])==20
assert assignment['task_name']=='/root/review_06250_07250' and assignment['model']=='gpt-6.1-sol' and assignment['reasoning_effort']=='high'
assert receipt['prepared_count']==20 and receipt['actual_read_count']==0 and not receipt['native_batch_written'] and not receipt['native_proof_written'] and not receipt['root_acceptance_written'] and not receipt['canonical_applied']
assert packet['prepared_count']==20 and packet['actual_read_count']==0
assert digest(current['slot_catalog'])=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for path,h in protected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
files=[R/'prepare_first20_149_root_01.py',Path(__file__),*sorted(d.iterdir()),*sorted(p.iterdir())]
report=R/'ROOT-FIRST20-149-PREPARATION-01.json';v={'schema':'photo-root-preparation-verification/v1','actor':'/root','source_snapshot_unchanged':True,'prepared':20,'actual_new_semantic_reads_claimed':0,'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0,'protected_files':protected,'files':[{'file':str(f.relative_to(ROOT)),'file_sha256':hashlib.sha256(f.read_bytes()).hexdigest()}for f in files]}
with report.open('xb')as f:f.write(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()+b'\n')
files.append(report);subprocess.run(['git','add','--',*[str(f.relative_to(ROOT))for f in files]],check=True);subprocess.run(['git','diff','--cached','--check'],check=True)
staged=subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines();assert set(staged)=={str(f.relative_to(ROOT))for f in files}
for path in staged:assert subprocess.check_output(['git','show',':'+path])==(ROOT/path).read_bytes()
print(json.dumps({'files':len(files),'prepared':20,'source_changes':0,'native_proofs_created':0,'operating_changes':0}))
