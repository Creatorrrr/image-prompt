"""Accept seven literal first20 research judgements, retaining thirteen unresolved source cases."""
import ast,gzip,hashlib,importlib.abc,json,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama'}:raise AssertionError('model/API import forbidden: '+fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
sys.path.insert(0,str(R));import native_reviews as nr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
def save(p,v):
 with p.open('x')as f:json.dump(v,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
D=R/'native-inputs/prepared/review06250-00000-00020-149-02';O=R/'native_batches/review06250-00000-00020-149-02';check=read(R/'ROOT-FIRST20-149-CONSUMER-CHECK-01.json');assert check['all_passed']and check['matrix_count']==28 and check['root_added_property_check_count']==72 and check['model_provider_Gemini_calls']==0
v=nr.verify_batch(D/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json',root=ROOT,here=R);assert v['statuses']=={'approved':7,'pending':13,'diagnostic_reviewed':0};approved=[x for x in v['records'].values()if x['status']=='approved'];assert [x['ordinal']for x in approved]==[3,4,5,9,16,17,18]
assert sum(len(x['proof']['facts'])for x in approved)==9 and sum(len(x['proof']['source_units'])for x in approved)==14
reason=('Root accepts research seven actual149 source65-bound judgements and thirteen honest pending source cases after personally reading all20 complete original/current sources, all7 actual native payloads9facts14units and9 full149 role/neighbor specs. '
 'Worker full20original5B/ownbinding/closure/exactlegacyprovenance and44fullspec reads are delegated evidence, not root personal new reads. '
 'Root reruns reviewed worker28 synthetic full/compact x binding matrices and independently adds72 every-actual-property/alias lock checks, including both precise effects for each lens. '
 'Preserve fantasy/fineart genre, image motionblur, lens exact50mm/standard and24mm/wideangle classifications, focused scene reading and laboratory place. '
 'No worldsystem, device introduction, physical action, sensor/FoV/DOF, private mind or new scene participants are inferred. '
 'No direct stronger KO fact is fabricated; wholeKO positive fields reference exact EN ordinary canonical facts. '
 'Historical144 approvals are not automatically re-signed. The worker authored these seven facts fresh and all previous snapshots remain. '
 'Thirteen source cases and fourteen alternatives remain pending/unselected, no new source/candidate kind or operating139/native0 change. Full stage5 all18250 and stages6–8 remain incomplete. No final149 hybrid search, actual requester/compose/runtime/render/pixels or expert/human semantic evaluation is claimed.')
acceptance={'schema':nr.ACCEPTANCE,'actor':'/root',**{k:v[k]for k in ['assignment_sha256','input_sha256','batch_sha256','note_sha256']},'reviews':{cid:{'review_sha256':c.digest(row),'status':row['status']}for cid,row in v['records'].items()},'reason':reason};save(O/'ROOT-ACCEPTANCE.json',acceptance);nr.verify_acceptance(ROOT,ref(O/'ROOT-ACCEPTANCE.json'),v)
paths=[p for p in O.rglob('*')if p.is_file()and '__pycache__'not in p.parts];paths.extend(p for p in (R/'authored').glob('native_06250_first20_149_02.*')if p.is_file());paths.extend([R/'worker-notes/native-06250-first20-149-02-final-20261015.json',R/'ROOT-FIRST20-149-CONSUMER-CHECK-01.json',R/'check_first20_149_root_01.py',Path(__file__).resolve(),ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
pins={}
for p in sorted(set(paths)):
 raw=p.read_bytes()
 if p.suffix=='.json':json.loads(raw)
 if p.suffix=='.py':ast.parse(raw)
 pins[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest()
assert not subprocess.check_output(['git','diff','--name-only','--','skills/photo-prompt-image-generator/assets','skills/photo-prompt-image-generator/scripts','tests'],text=True).strip()
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for path,h in protected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h
report={'schema':'photo-root-first20-final149-research-integration/v1','actor':'/root','accepted_batch':ref(O/'BATCH.json'),'acceptance':ref(O/'ROOT-ACCEPTANCE.json'),'assignment':ref(D/'ASSIGNMENT.json'),'worker_note':ref(O/'NOTE.json'),'worker_actual_source_reads':20,'research_approved':7,'research_pending':13,'new_unique_corpus_source_reads_claimed':0,'facts':9,'whole_source_units':14,'root_rerun_worker_matrices':28,'root_added_every_actual_property_alias_checks':72,'source_alternatives_count':14,'source_alternatives_selected':0,'read_and_evidence_boundary':reason,'operating_source_or_catalog_or_bindings_changed':False,'operating_native_qualified_count':0,'all_remaining_stages_completed':False,'Gemini_calls':0,'new_embedding_inference_calls':0,'files':pins,'protected_files':protected};output=R/'ROOT-FIRST20-149-INTEGRATION-01.json';save(output,report)
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();names=sorted(set(pins)|{str(output.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);subprocess.run(['git','diff','--cached','--check'],check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==set(names)
for path in names:assert subprocess.check_output(['git','show',':'+path])==(ROOT/path).read_bytes()
print(json.dumps({'files':len(names),'research_approved':7,'research_pending':13,'root_rerun_matrices':28,'root_added_checks':72,'source_choices':0,'operating_changes':0,'Gemini_calls':0}))
