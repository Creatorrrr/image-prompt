"""Accept exactly two research judgements, preserving the rejected noise history."""
import ast, gzip, hashlib, importlib.abc, json, subprocess, sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama'}:raise AssertionError('model/API import forbidden: '+fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c, photo_semantic_evidence as n
sys.path.insert(0,str(R));import native_reviews as nr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
assert Path(nr.native.__file__).resolve().is_relative_to(G)
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def save(p,v):
 with p.open('x')as f:json.dump(v,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
checks=read(R/'ROOT-MOOD-NOISE-CONSUMER-CHECK-07.json');assert checks['all_passed']and checks['assertions_passed']==52 and checks['model_provider_Gemini_calls']==0
accepted=[]
for ordinal,revision in [(3107,'01'),(3169,'03')]:
 D=R/f'native-inputs/prepared/root-{ordinal:05d}-149-{revision}';O=R/f'native_batches/root-{ordinal:05d}-149-{revision}'
 verified=nr.verify_batch(D/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json',root=ROOT,here=R)
 reason=('Root accepts exactly this direct source/proof judgement for research after whole original/current/5B/binding/emptyclosure/positivefields/facts/units/used149spec reading and52 controlled full/compact checks across these two candidates. '
 '3107 KO uses a bounded partial reference without overclaiming all English mood qualifiers. 3169 retains original rendering.noise/image_plane/style effect, exact ISO3200 appearance value, actual independent image P and one same-canonical-fact grain role view. '
 'Actual original-property, alias/ancestor/parent/whole-dimension locks and real binding denials remain. Earlier unaccepted noise01 source/proof and its original-lock failure are preserved, not upgraded. '
 'This is no operating activation, full149 hybrid retrieval, actual user request, final compose/runtime receipt or image/pixel claim; fullstage5 and6–8 remain unfinished.')
 acceptance={'schema':nr.ACCEPTANCE,'actor':'/root',**{k:verified[k]for k in ['assignment_sha256','input_sha256','batch_sha256','note_sha256']},
 'reviews':{cid:{'review_sha256':c.digest(row),'status':row['status']}for cid,row in verified['records'].items()},'reason':reason}
 save(O/'ROOT-ACCEPTANCE.json',acceptance);nr.verify_acceptance(ROOT,ref(O/'ROOT-ACCEPTANCE.json'),verified)
 accepted.append({'ordinal':ordinal,'revision':revision,'acceptance':ref(O/'ROOT-ACCEPTANCE.json'),'batch':ref(O/'BATCH.json'),'assignment':ref(D/'ASSIGNMENT.json'),'note':ref(O/'NOTE.json')})
assert not (R/'native_batches/root-03169-149-01/ROOT-ACCEPTANCE.json').exists()
paths=[]
for relative in ['native-inputs/root-mood-noise-source-plan-11','native-inputs/root-noise-canonical-source-plan-12','native-inputs/root-noise-contract-source-plan-13',
                 'native-inputs/prepared/root-03107-149-01','native-inputs/prepared/root-03169-149-01','native-inputs/prepared/root-03169-149-02','native-inputs/prepared/root-03169-149-03',
                 'native_batches/root-03107-149-01','native_batches/root-03169-149-01','native_batches/root-03169-149-03']:
 paths.extend(path for path in (R/relative).rglob('*')if path.is_file())
paths.extend(R/name for name in ['prepare_mood_noise_root_01.py','review_mood_noise_root_01.py','prepare_noise_canonical_root_02.py','review_noise_canonical_root_02.py',
 'prepare_noise_contract_root_03.py','review_noise_canonical_root_03.py','ROOT-MOOD-NOISE-CONSUMER-CHECK-01.json','ROOT-MOOD-NOISE-CONSUMER-CHECK-07.json',
 'ROOT-MOOD-NOISE-CONSUMER-FAILED-ATTEMPT-01.json','ROOT-MOOD-NOISE-CONSUMER-FAILED-ATTEMPT-02.json','ROOT-MOOD-NOISE-CONSUMER-FAILED-ATTEMPT-05.json','ROOT-MOOD-NOISE-CONSUMER-FAILED-ATTEMPT-06.json',
 'authored/native_09250_02250_03250.formal-feasibility-001.json','worker-notes/native-09250-formal-feasibility-001.json','worker-notes/native-09250-self-discovery-queue-011.json'])
paths.extend(R/f'check_mood_noise_root_{i:02d}.py'for i in range(1,8));paths.append(Path(__file__).resolve())
paths.append(ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md')
pins={}
for path in sorted(set(paths)):
 raw=path.read_bytes()
 if path.suffix=='.json':json.loads(raw)
 if path.suffix=='.py':ast.parse(raw)
 pins[str(path.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest()
assert not subprocess.check_output(['git','diff','--name-only','--','skills/photo-prompt-image-generator/assets','skills/photo-prompt-image-generator/scripts','tests'],cwd=ROOT).strip()
for name,expected in {'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected
report={'schema':'photo-root-two-source-integration/v1','actor':'/root','accepted_research_reviews':accepted,'accepted_count':2,
 'final_research_source_proposal':ref(R/'native-inputs/root-noise-contract-source-plan-13/CURRENT-PROPOSAL.json.gz'),
 'research_source_corrections_total':64,'catalog_research_count':149,'controlled_actual_source_checks':ref(R/'ROOT-MOOD-NOISE-CONSUMER-CHECK-07.json'),
 'checks_passed':52,'files':pins,'root_personally_read_scope':'Exactly these two complete sources, old5B/bindings/emptyclosure/positive statements and proposals, all actual7 facts/7 units plus exact noise view and relevant fullspecs; other worker5-case feasibility items not claimed as root whole reads.',
 'unaccepted_history':['root-03169-149-01 property rename is HOLD: original rendering.noise lock bypass observed after the earlier44 bounded checks.',
 'root-03169-149-02 proof was not written: application_scope is not a whole primary positive field. Same literal text now uses native application_contract; no validator relaxation.',
 'Test import and record-interface fixture failures remain immutable; corrected harness changes no production source/permission.'],
 'operating_source_or_catalog_or_bindings_written':False,'production_or_test_code_changed':False,'operating_native_qualified_count':0,
 'hybrid_search_final149_completed':False,'actual_compose_runtime_pixels_claimed':False,'all_remaining_stages_completed':False,'Gemini_calls':0,'new_embedding_inference_calls':0}
output=R/'ROOT-MOOD-NOISE-INTEGRATION-01.json';save(output,report)
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
names=sorted(set(pins)|{str(output.relative_to(ROOT))});subprocess.run(['git','add','--',*names],cwd=ROOT,check=True)
subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name],cwd=ROOT)==(ROOT/name).read_bytes(),name
print(json.dumps({'accepted_research_reviews':2,'checks_passed':52,'staged_paths':len(names),'operating_changes':0,'Gemini_calls':0}))
