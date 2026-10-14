"""Accept five exact conditional research proofs after direct and peer review."""
import ast,gzip,hashlib,importlib.abc,json,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
sys.path.insert(0,str(R));import native_reviews as nr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=raw(p),sha256=c.digest(read(p)))
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
D=R/'native-inputs/prepared/review05250-simple5-149-01';O=R/'native_batches/review05250-simple5-149-01'
assert raw(O/'BATCH.json')=='dc55d88fa6d26f56185ae13bb20ae1d345988b194eb6bccdc1276839afcd755e'
v=nr.verify_batch(D/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json',root=ROOT,here=R)
assert v['statuses']=={'approved':5,'pending':0,'diagnostic_reviewed':0}
assert v['current_source_sha256']=='b1c48c867ce0a94d5648b0bfb7935605e4d7708951b36268930ea26523746092'
assert sum(len(r['proof']['facts'])for r in v['records'].values())==20
assert sum(len(r['proof']['source_units'])for r in v['records'].values())==26
checks=read(R/'ROOT-SIMPLE5-CONSUMER-VERIFICATION-01.json')
assert checks['reviewed_writer_suite_actual_assertions']==589 and checks['full_compact_ownbinding_baselines']==20
assert checks['independently_added_cases']==48 and checks['independently_added_assertions']==96 and checks['model_API_import_attempts']==[]
assert c.digest(read(R/'ROOT-SIMPLE5-ACTUAL-CHECKS-RERUN-01.json'))==c.digest(read(O/'ACTUAL-CHECKS-v1.json'))
peer_path=R/'authored/native_06250_simple5_peer01.review.json';peer=read(peer_path)
assert raw(peer_path)=='5ccac0aad7baf3431a2fdbd953b0e22b8b4a83af8f24318f79f9ba5e26425739' and peer['blocking_findings']==[]
assert peer['peer_whole_source_proof_5B_ownbinding_closure_read_count']==5 and peer['controls']['new_independent_assertions']==168
for name,item in peer['file_pins'].items():assert raw(ROOT/name)==item['raw_sha256']
original=nr.artifact(ROOT,read(D/'INPUT.json')['original_snapshot']);source=nr.artifact(ROOT,read(D/'INPUT.json')['current_snapshot'])
for row in v['records'].values():
 assert row['source_before']==original['candidates'][row['candidate_id']] and row['source_after']==source['candidates'][row['candidate_id']]
 for unit in row['proof']['source_units']:
  value=row['source_after']
  for key in unit['pointer'].strip('/').split('/'):value=value[int(key)] if isinstance(value,list)else value[key]
  assert unit['quote']==value
reason=('Root accepts exact source96/catalog149V6 conditional research proofs for6131,6162,6191,6214,6220. '
 'Root directly read the complete original/current and selected before/afters during the source selection; now reads all20 actual native facts, all26 whole-source unit dispositions/reference rationales, complete effects/conditions/owner mappings/roles and ten complete used/neighbor role specifications. '
 'Whole App quote equality is factored against the already directly read exact complete selected App; no truncated or repeated duplicate receives new read credit. '
 'Worker preserves full original5B/ownbinding/empty closure/provenance and authors five fresh proofs. Independent peer reads all five whole records/proofs and adds168 actual assertions with10 full/compact ownbinding baselines; this is not a complete589-case peer rerun. '
 'Root reruns the reviewed589 actual assertions/20 full-compact binding baselines and adds48 separate cross-dimension exact-property/unrelated controls with96 assertions. Both additional suites reuse reviewed synthetic fixture constructors; they do not certify actual requester truth. '
 'Location qualifier/adjacency/purpose remains one setting E and creates no machine, players, portal or table entity.6214 preserves exact cafe-closing event phase, selected visually quiet atmosphere and corrected KO/alias, without a clock time/private mind claim. '
 '6220 retains original style/image_plane/image.detail E and whole-image relation, separate literal continuous-contour/readable-detail PR with independent source P/type. App units reference the exact EN/concept facts without cross-field ordinary-anchor invention. The connector token alone supplies no role. '
 'Every original condition, domain/primary tag gate, address/value/mode/operation/receiver and original lock remains. The two direct PR-mutation tests are raw actual-property controls, not a full joint candidate union or final after-state audit. '
 'No operating source/catalog/binding/runtime adoption, Gemini/model/embedding inference or image pixels. These five already overlap bulk direct reads and add no unique bulk credit. Stage5 all18250 and stages6–8 remain incomplete.')
acceptance=dict(schema=nr.ACCEPTANCE,actor='/root',**{k:v[k]for k in ['assignment_sha256','input_sha256','batch_sha256','note_sha256']},reviews={cid:dict(review_sha256=c.digest(row),status=row['status'])for cid,row in v['records'].items()},reason=reason)
save(O/'ROOT-ACCEPTANCE.json',acceptance);nr.verify_acceptance(ROOT,ref(O/'ROOT-ACCEPTANCE.json'),v)
paths=[p for p in O.rglob('*')if p.is_file()and '__pycache__'not in p.parts]
for pattern in ['native_05250_simple5-source96.*','native_06250_simple5_peer01.*']:paths.extend(p for p in(R/'authored').glob(pattern)if p.is_file())
paths.append(R/'worker-notes/native_06250_simple5_peer01.json')
paths.extend(R/name for name in ['ROOT-SIMPLE5-ACTUAL-CHECKS-RERUN-01.json','ROOT-SIMPLE5-COMPLETION-RERUN-01.json','ROOT-SIMPLE5-CONSUMER-VERIFICATION-01.json','check_simple5_149_root_01.py'])
paths.extend([Path(__file__).resolve(),ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md']);pins={}
for p in sorted(set(paths)):
 if p.suffix=='.json':read(p)
 if p.suffix=='.py':ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=raw(p)
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name,pin in protected.items():assert raw(ROOT/name)==pin
report=dict(schema='photo-root-simple5-research-integration/v1',actor='/root',accepted_batch=ref(O/'BATCH.json'),acceptance=ref(O/'ROOT-ACCEPTANCE.json'),peer=ref(peer_path),research_approved_in_batch=5,pending_in_batch=0,actual_native_facts=20,whole_source_units=26,root_rerun_assertions=589,root_added_assertions=96,root_added_cases=48,peer_added_assertions=168,root_read_and_evidence_boundary=reason,new_unique_bulk_read_credit=0,operating_native_qualified_count=0,operating_changes=0,Gemini_calls=0,all_remaining_stages_complete=False,files=pins,protected_files=protected)
output=R/'ROOT-SIMPLE5-149-INTEGRATION-01.json';save(output,report)
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
names=sorted(set(pins)|{str(output.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);expected=set()
for name in names:
 old=subprocess.run(['git','show','HEAD:'+name],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 if old.returncode or old.stdout!=(ROOT/name).read_bytes():expected.add(name)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==expected
subprocess.run(['git','diff','--cached','--check'],check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(cached_files=len(expected),research_approved=5,pending=0,root_rerun_assertions=589,root_added_assertions=96,operating_changes=0,Gemini_calls=0)))
