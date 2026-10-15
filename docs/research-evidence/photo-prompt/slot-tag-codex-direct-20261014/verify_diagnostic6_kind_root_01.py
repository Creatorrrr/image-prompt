"""Verify exact kind-only recovery, preserving all unaccepted diagnostic history."""
import ast,gzip,hashlib,importlib.abc,json,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
nr=prep.reviews;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=raw(p),sha256=c.digest(read(p)))
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
D=R/'native-inputs/root-diagnostic6-kind-source-plan-23';parent=R/'native-inputs/root-same-image-guard-source-plan-22-R02'
current=read(D/'CURRENT-PROPOSAL.json.gz');previous=read(parent/'CURRENT-PROPOSAL.json.gz');original=read(R/'SOURCE.json.gz');selection=read(D/'ROOT-SOURCE-SELECTION.json')
assert c.digest(current)=='39ab970ec8a42550f6afb41163ae6e2e76c1403f60f76cb9e5a962e3197dd65c'
assert raw(D/'CURRENT-PROPOSAL.json.gz')=='10750f2cb7349dcacbf78bb79ea5801aebdd155df2af6864e824d8dc5d8d898e'
approval=read(D/'SOURCE-APPROVAL.json');prep.approve_source(ROOT,original,current,approval);c.validate(current)
assert len(approval['changes'])==102 and len({r['candidate_id']for r in approval['changes']})==102
assert len(current['candidates'])==18250 and len(current['slot_catalog'])==149
assert all(current[k]==previous[k]for k in ['slot_catalog','slot_bindings','policies'])
assert {cid for cid in current['candidates']if current['candidates'][cid]!=previous['candidates'][cid]}=={r['candidate_id']for r in selection['selected']}
assert [r['ordinal']for r in selection['selected']]==[12016,12041,12044,12055,12056,12369]
for row in selection['selected']:
 b,a=row['before'],row['after'];memo=nr.artifact(ROOT,row['memo'])
 assert b==previous['candidates'][row['candidate_id']]==original['candidates'][row['candidate_id']]
 assert a==current['candidates'][row['candidate_id']]==memo['unselected_minimal_alternatives'][1]['whole_after']
 assert b['record_kind']=='diagnostic' and a['record_kind']=='visual_option'
 assert {k:v for k,v in b.items()if k!='record_kind'}=={k:v for k,v in a.items()if k!='record_kind'}
 assert memo['recommend_prior_nonsemantic_proof_withdrawal_to_pending'] is True
assert sum(r['record_kind']=='diagnostic'for r in current['candidates'].values())==52
input_dir=R/'native-inputs/prepared/review05250-diagnostic70-149-03';assignment=read(input_dir/'ASSIGNMENT.json');nr.validate_assignment_identity(assignment);inp=nr.artifact(ROOT,assignment['input']);packet=read(input_dir/'PREPARED-PACKET.json')
assert len(assignment['ids'])==len(assignment['ordinals'])==packet['prepared_count']==70 and packet['actual_read_count']==0
assert nr.artifact(ROOT,inp['current_snapshot'])==current
for cid in assignment['ids']:
 assert packet['current_records'][cid]==current['candidates'][cid] and packet['original_records'][cid]==original['candidates'][cid]
 assert n.referenced_records(current['candidates'][cid],current)==packet['references'][cid]==packet['reference_bindings'][cid]=={}
assert not(R/'native_batches/review05250-diagnostic70-149-01/ROOT-ACCEPTANCE.json').exists()
assert not(R/'native_batches/review05250-diagnostic70-149-02/ROOT-ACCEPTANCE.json').exists()
paths=[Path(__file__).resolve(),R/'prepare_diagnostic6_kind_root_01.py',ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md']
for folder in [D,input_dir]:paths.extend(p for p in folder.rglob('*')if p.is_file())
for folder in [R/'authored',R/'worker-notes']:paths.extend(p for p in folder.glob('native_diag70_05250_recheck6.*')if p.is_file())
pins={}
for p in sorted(set(paths)):
 if p.suffix=='.json':read(p)
 if p.suffix=='.py':ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=raw(p)
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for path,pin in protected.items():assert raw(ROOT/path)==pin
report=dict(schema='photo-root-diagnostic6-kind-verification/v1',actor='/root',source=ref(D/'CURRENT-PROPOSAL.json.gz'),source_corrections_unique=102,kind_only_changes=6,restored_positive_templates_pending=18,research_diagnostic_count=52,diagnostic52_root_accepted=False,prepared_sparse=70,preparation_actual_reads=0,existing_batches_unchanged_and_unaccepted=True,whole_source_positive_meaning_preserved=True,root_read_and_evidence_boundary=selection['reason'],new_unique_bulk_read_credit=0,native_proofs_created=0,operating_changes=0,operating_native_qualified=0,Gemini_calls=0,files=pins,protected_files=protected)
out=R/'ROOT-DIAGNOSTIC6-KIND-PREPARATION-01.json';save(out,report)
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
names=sorted(set(pins)|{str(out.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);expected=set()
for name in names:
 previous=subprocess.run(['git','show','HEAD:'+name],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 if previous.returncode or previous.stdout!=(ROOT/name).read_bytes():expected.add(name)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==expected
subprocess.run(['git','diff','--cached','--check'],check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(cached_files=len(expected),source_corrections_unique=102,kind_restorations=6,total_positive_pending=18,diagnostic52_accepted=False,operating_changes=0)))
