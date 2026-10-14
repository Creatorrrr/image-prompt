"""Verify the selected existing-item/image guard and bounded frozen feasibility."""
import ast,gzip,hashlib,importlib.abc,json,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
forbidden=[]
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:
   forbidden.append(fullname);raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=raw(p),sha256=c.digest(read(p)))
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
D=R/'native-inputs/root-same-image-guard-source-plan-22-R02';parent=R/'native-inputs/root-simple5-diagnostic7-source-plan-21'
original=read(R/'SOURCE.json.gz');current=read(D/'CURRENT-PROPOSAL.json.gz');prior=read(parent/'CURRENT-PROPOSAL.json.gz');cid='cand_2e72784a26885ceaa1d645d25bd9a468'
assert c.digest(current)=='5ed4478da12e828918e4b65442c0444c00c3f639774a8900a88de5e3101af550'
prep.approve_source(ROOT,original,current,read(D/'SOURCE-APPROVAL.json'));c.validate(current)
assert {key for key in current['candidates'] if current['candidates'][key]!=prior['candidates'][key]}=={cid}
assert all(current[k]==prior[k]for k in ['slot_catalog','slot_bindings','policies'])
b=prior['candidates'][cid];a=current['candidates'][cid]
assert a['effects']==b['effects'] and a['provenance']==b['provenance']
assert a['content']['en']==b['content']['en'] and a['content']['ko']==b['content']['ko']
assert a['conditions']['native_guards']['rules'][:-1]==b['conditions']['native_guards']['rules']
assert len(b['conditions']['native_guards']['rules'])==5
input_dir=R/'native-inputs/prepared/review11870-01299-149-07';assignment=read(input_dir/'ASSIGNMENT.json');inp=prep.reviews.artifact(ROOT,assignment['input']);packet=read(input_dir/'PREPARED-PACKET.json')
assert assignment['ids']==[cid] and assignment['ordinals']==[1299] and packet['actual_read_count']==0
assert prep.reviews.artifact(ROOT,inp['current_snapshot'])==current and packet['current_records'][cid]==a
code_path=R/'same-image-pr-review11870-01/guard_experiment_v3.py';code=code_path.read_text()
before="p=O/'GUARD-EXPERIMENT-v3.json'";after="p=R/'ROOT-SAME-IMAGE-SYNTHETIC-RERUN-01.json'"
assert code.count(before)==1
space={'__name__':'root_bounded_guard_rerun','__file__':str(code_path)};exec(compile(code.replace(before,after),str(code_path),'exec'),space)
rerun=read(R/'ROOT-SAME-IMAGE-SYNTHETIC-RERUN-01.json')
assert len(rerun['actual_safety_cases'])==24 and len(rerun['actual_trusted_core_semantic_boundaries'])==4
assert all(not r['semantically_valid_independent_core_witness'] for r in rerun['actual_trusted_core_semantic_boundaries'])
assert not forbidden
reason=('Root selects and verifies only one existing-item/same-selected-image scalar relation guard plus the exact App extension. Every previous E3/receiver/operation/value/condition and five guards stays unchanged. '
 'Root read complete proposal/experiment helpers and integration design, factoring previously directly read original/current1299 full bodies. '
 'Root executes the reviewed one-E synthetic24 actual full/compact guard/PR/admission/consumer feasibility cases under frozen50fd92, preserving four false-trusted-core semantic-boundary probes separately. '
 'No claim that this one-E fixture validates actual1299 E3/all affected owners, actual input source-span truth, normalized core freeze, envelope permission, final after-state, native approval or pixels. '
 'First preparation was strictly rejected because metadata omitted prior EN/KO source changes. R02 retains that failure and exactly the same selected after, using a whole-content original-to-after delta. No unsafe source snapshot was written by the failed attempt. '
 'The new input has prepared1/actualread0/proof0. Actual1299 remains pending until source-authorized mandatory envelope/final PR integration and a fresh complete native judgment. Operating139/native0 is unchanged.')
paths=[Path(__file__).resolve(),R/'prepare_same_image_guard_root_01.py',R/'prepare_same_image_guard_root_R02.py',R/'ROOT-SAME-IMAGE-PREPARATION-FAILED-ATTEMPT-01.json',R/'ROOT-SAME-IMAGE-SYNTHETIC-RERUN-01.json',ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md']
for folder in [R/'same-image-pr-review11870-01',R/'native-inputs/root-same-image-guard-source-plan-22',D,input_dir,R/'native_batches/review11870-01299-149-06']:
 paths.extend(p for p in folder.rglob('*')if p.is_file()and '__pycache__'not in p.parts)
pins={}
for p in sorted(set(paths)):
 if p.suffix=='.json':read(p)
 if p.suffix=='.py':ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=raw(p)
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for path,pin in protected.items():assert raw(ROOT/path)==pin
report=dict(schema='photo-root-same-image-guard-preparation-verification/v1',actor='/root',source=ref(D/'CURRENT-PROPOSAL.json.gz'),assignment=ref(input_dir/'ASSIGNMENT.json'),root_rerun_synthetic_cases=24,root_rerun_false_trusted_core_boundary_probes=4,source1299_native_approved=False,actual_source_E3_consumer_validation_claimed=False,new_unique_bulk_reads=0,root_read_and_evidence_boundary=reason,original_E3_and_five_guards_preserved=True,unique_source_corrections=96,source_prepared=1,preparation_actual_reads=0,native_proofs_created=0,operating_changes=0,Gemini_calls=0,model_API_import_attempts=forbidden,files=pins,protected_files=protected)
output=R/'ROOT-SAME-IMAGE-GUARD-PREPARATION-01.json';save(output,report)
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
names=sorted(set(pins)|{str(output.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);expected=set()
for name in names:
 previous=subprocess.run(['git','show','HEAD:'+name],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 if previous.returncode or previous.stdout!=(ROOT/name).read_bytes():expected.add(name)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==expected
subprocess.run(['git','diff','--cached','--check'],check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(cached_files=len(expected),source_changes_unique=96,synthetic_cases=24,boundary_probes=4,actual1299_approved=False,operating_changes=0)))
