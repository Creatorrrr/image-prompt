"""Accept the exact twenty research judgments; preserve reuse and errata.

Consumer checks were run separately under the frozen generation. This helper
checks bindings and stages an explicit evidence allowlist, not operating data.
"""
import ast, copy, gzip, hashlib, importlib.abc, json, subprocess, sys
from pathlib import Path

ROOT = Path.cwd()
R = ROOT / 'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G = Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class DenyModels(importlib.abc.MetaPathFinder):
 def find_spec(self, fullname, path=None, target=None):
  if fullname.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama','requests','httpx'}:
   raise AssertionError('model/API import forbidden: ' + fullname)
sys.meta_path.insert(0, DenyModels()); sys.dont_write_bytecode = True
sys.path[:0] = [str(G/'scripts'), str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0, str(R)); import native_reviews as nr
sys.path[:0] = [str(G/'scripts'), str(G/'precore')]
def read(p):
 return json.loads(gzip.decompress(p.read_bytes()) if p.suffix == '.gz' else p.read_bytes())
def raw(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):
 return dict(file=str(p.relative_to(ROOT)), file_sha256=raw(p), sha256=c.digest(read(p)))
def save(p, v):
 with p.open('xb') as f: f.write(c.canonical_bytes(v) + b'\n')
def proof_bytes(p):
 text=p.read_text(); decoder=json.JSONDecoder(); cursor=text.index('[',text.index('"records"'))+1; result={}
 while True:
  while text[cursor].isspace() or text[cursor]==',': cursor+=1
  if text[cursor]==']': break
  start=cursor; row,end=decoder.raw_decode(text,cursor); segment=text[start:end]
  point=segment.index('"proof"')+len('"proof"'); point=segment.index(':',point)+1
  while segment[point].isspace(): point+=1
  _,last=decoder.raw_decode(segment,point)
  result[row['candidate_id']]=segment[point:last].encode(); cursor=end
 return result

D=R/'native-inputs/prepared/review06250-00000-00020-149-04'
O=R/'native_batches/review06250-00000-00020-149-04'
assert raw(O/'BATCH.json')=='7d38bd7e01b91bec137238c7e5870785239f50b88f45d120e2e8b848ab2da5f5'
v=nr.verify_batch(D/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json',root=ROOT,here=R)
assert v['statuses']=={'approved':20,'pending':0,'diagnostic_reviewed':0}
assert v['current_source_sha256']=='a3ac73e618b4443855c9cba07a0b0f9977c65cd19d0dcb92188ea2b208fddec7'
assert v['catalog_sha256']=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
assert sum(len(r['proof']['facts']) for r in v['records'].values())==64
assert sum(len(r['proof']['source_units']) for r in v['records'].values())==53
checks=read(R/'ROOT-FIRST20-04-CONSUMER-VERIFICATION-01.json')
assert checks['worker_suite_counts']==dict(new7_full_compact_oldbinding=28,reused13_full_compact_oldbinding=52,lighting_original_property_all_receivers_alias_ancestor=448,lighting_missing_wrong_scope_relation_context=344)
assert checks['independently_added_controls']==140 and checks['Gemini_calls']==0 and checks['model_API_import_attempts']==[]
for filename,pin in {
 'ROOT-FIRST20-LIGHTING04-CONSUMER-RERUN-01.json':'2373fc20c6c8dba0fc4105aa5e5cf65c1c82b38e482aeb3073908de3659a7fc1',
 'ROOT-FIRST20-REUSED13-CONSUMER-RERUN-01.json':'1be48443407d8c6c36b9245ff2064a2e5ad244e0fc652403aca45ef43b3c8427',
 'ROOT-FIRST20-04-EVIDENCE-CONTROLS-RERUN-01.json':'9b0cf3d0b2fb5eec850dc87a111935a73abe983dfaf1aa210caa9977b94f1a85',
}.items(): assert raw(R/filename)==pin
peer_path=R/'authored/native_05250_first20-peer04.review-v2.json';peer=read(peer_path)
assert raw(peer_path)=='cc2ef8b5e6a21b75cad2e4137bbfee0d72a52902c6cfc95bd43b5e74145556f5'
prior_peer=read(R/'authored/native_05250_first20-peer04.review-v1.json')
assert peer['record_assessments']==prior_peer['record_assessments'] and peer['blocking_findings']==[]
for item in peer['execution_code_review']['writer_scripts_read_whole']:
 assert 'sha256' not in item and item['hash_kind']=='raw_file_bytes_only_not_canonical_JSON'
 assert raw(ROOT/item['file'])==item['file_sha256']
audit1=read(R/'authored/native_05250_first20-peer04.actual-admission-v1.json')
audit2=read(R/'authored/native_05250_first20-peer04.actual-admission-v2.json')
# Only Python reference metadata differs. Preserve the actual execution receipts.
for key in audit1:
 if key not in {'fixture_functions_reused','metadata_erratum'}: assert audit1[key]==audit2[key],key
for row in peer['record_assessments']:
 actual=v['records'][row['candidate_id']]
 assert row['current_sha256']==c.digest(actual['source_after']) and row['proof_sha256']==c.digest(actual['proof'])
 assert row['peer_disposition']=='agree_conditional_source_native'
old7={3,4,5,9,16,17,18};reused13=old7|{8,10,13,14,15,19}
values04=proof_bytes(O/'BATCH.json')
values03=proof_bytes(R/'native_batches/review06250-00000-00020-149-03/BATCH.json')
values02=proof_bytes(R/'native_batches/review06250-00000-00020-149-02/BATCH.json')
for cid,row in v['records'].items():
 if row['ordinal'] in reused13: assert values04[cid]==values03[cid]
 if row['ordinal'] in old7: assert values04[cid]==values02[cid]
reason=('Root accepts twenty exact conditional research judgments against source84 and catalog149V6. '
 'Root previously read all20 complete original/current records, personally read all13 newly selected complete applications and fourteen alternatives plus fifteen complete role/neighbor specifications, and now directly reads all13 new native payloads with55 facts39 source units, preserving prior7 payloads9 facts14 units. '
 'Root reran actual frozen consumer80 full/compact/ownbinding combinations,448 original-property/receiver/alias/ancestor/whole controls and344 missing/wrong context guards, and added140 separate cross-dimension/unrelated-property controls. '
 'Peer independently reread all20 exact sources, original5B/ownbindings/empty closures, native facts/units/guards and relevant full149 specifications; its bounded90 cases include76 actual admission calls and14 pre-admission structural rejections, not a full independent matrix rerun. '
 'Peer v1 Python descriptor-digest metadata errors are preserved; v2 raw-file-only refs repair metadata without changing any semantic judgment or execution receipt and create no new checks, reads or signatures. '
 'Keep all actual original dimensions and selected exact properties/modes/values/operations/receivers/prerequisites/preservation. Whole receiver inventories, same-scene/source/path relations and exact laboratory/theme contexts remain mandatory. Dieselpunk manual aesthetic view preserves its same setting E. '
 'Raw13 proof values are reused from03; original7 are also byte-identical to accepted02. These are thirteen newly accepted candidate judgments in this20 set, not twenty new approvals or repeated bulk source reads. '
 'Controlled core tests do not establish real-request inventory or source-span truth, rendered pixels or expert evaluation. No production source/catalog/binding/runtime adoption, Gemini or embedding inference; operating139/native0 is unchanged. Stage5 all18250 and stages6–8 remain incomplete.')
acceptance=dict(schema=nr.ACCEPTANCE,actor='/root',**{k:v[k] for k in ['assignment_sha256','input_sha256','batch_sha256','note_sha256']},reviews={cid:dict(review_sha256=c.digest(row),status=row['status']) for cid,row in v['records'].items()},reason=reason)
save(O/'ROOT-ACCEPTANCE.json',acceptance);nr.verify_acceptance(ROOT,ref(O/'ROOT-ACCEPTANCE.json'),v)
paths=[]
for version in ['03','04']:
 paths.extend(p for p in (R/f'native_batches/review06250-00000-00020-149-{version}').rglob('*') if p.is_file() and '__pycache__' not in p.parts)
 paths.extend(p for p in (R/'authored').glob(f'native_06250_first20_149_{version}.*') if p.is_file())
 paths.append(R/f'worker-notes/native_06250_first20_149_{version}.final-read-and-controls01.json')
paths.extend(p for p in (R/'authored').glob('native_05250_first20-peer04.*') if p.is_file())
paths.extend(p for p in (R/'worker-notes').glob('native_05250_first20-peer04.*') if p.is_file())
paths.extend(R/name for name in ['check_first20_149_04_root_01.py','ROOT-FIRST20-LIGHTING04-CONSUMER-RERUN-01.json','ROOT-FIRST20-REUSED13-CONSUMER-RERUN-01.json','ROOT-FIRST20-04-EVIDENCE-CONTROLS-RERUN-01.json','ROOT-FIRST20-04-CONSUMER-VERIFICATION-01.json'])
paths.extend([Path(__file__).resolve(),ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
pins={}
for p in sorted(set(paths)):
 assert p.is_file(),p
 if p.suffix=='.json': read(p)
 if p.suffix=='.py': ast.parse(p.read_bytes())
 pins[str(p.relative_to(ROOT))]=raw(p)
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for path,pin in protected.items(): assert raw(ROOT/path)==pin
report=dict(schema='photo-root-first20-final149-research-integration/v2',actor='/root',accepted_batch=ref(O/'BATCH.json'),acceptance=ref(O/'ROOT-ACCEPTANCE.json'),assignment=ref(D/'ASSIGNMENT.json'),peer_review=ref(peer_path),research_approved_in_batch=20,newly_accepted_in_batch=13,previously_accepted_reused=7,research_pending_in_batch=0,canonical_facts=64,whole_source_units=53,root_actual_consumer_checks=checks['worker_suite_counts'],root_added_controls=140,read_and_evidence_boundary=reason,new_unique_bulk_source_read_credit=0,operating_native_qualified_count=0,operating_changes=0,Gemini_calls=0,all_remaining_stages_completed=False,files=pins,protected_files=protected)
output=R/'ROOT-FIRST20-149-INTEGRATION-02.json';save(output,report)
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
names=sorted(set(pins)|{str(output.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);subprocess.run(['git','diff','--cached','--check'],check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==set(names)
for path in names: assert subprocess.check_output(['git','show',':'+path])==(ROOT/path).read_bytes()
print(json.dumps(dict(files=len(names),research_approved=20,newly_accepted=13,reused_accepted=7,pending_in_batch=0,operating_changes=0,Gemini_calls=0)))
