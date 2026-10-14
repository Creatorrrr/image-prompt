"""Accept the exact repaired research batch, retaining its honest pending row and history."""
import ast,gzip,hashlib,importlib.abc,json,subprocess,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','litellm','ollama'}:raise AssertionError('model/API import forbidden: '+fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n
sys.path.insert(0,str(R));import native_reviews as nr
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
def save(p,v):
 with p.open('x')as f:json.dump(v,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
D=R/'native-inputs/prepared/review11870-01250-01300-06';O=R/'native_batches/review11870-01250-01300-06';peer=R/'authored/native_05250_peer06.01255.repair-peer-v1.json'
assert hashlib.sha256(peer.read_bytes()).hexdigest()=='e4af80017789eca2215730b890a19b24bf18227caee68264451c5e3089204be6'
checks=read(R/'ROOT-FIRST50-1255-CONSUMER-CHECK-01.json');assert checks['controlled_check_count']==66 and checks['literal_repair_assertions_passed']and checks['model_provider_Gemini_calls']==0
verified=nr.verify_batch(D/'ASSIGNMENT.json',O/'BATCH.json',O/'NOTE.json',root=ROOT,here=R)
assert verified['batch_sha256']=='1608aaf83463aaaf9150b49938e8b119c051aefa3b64139686e8ec23cc5f8203';assert verified['statuses']=={'approved':49,'pending':1,'diagnostic_reviewed':0};assert verified['actual_read_count']==50
reason=('Root accepts exact first50-06 research judgements49approved and1299pending after worker actual whole50reads, independent peer whole50/49proof review and targeted1255 repair review. '
 'Root personally reads six focal complete original/current sources and actual native payloads, plus13 relevant full149specs, not all50. '
 'Root found1255 stronger English own-side directfact, held05 and required exact one-row correction. Retain full Ko/App placement E and English partialreference, all three actual E groups/targets/Rx/values/P/guards. '
 'The other49 entire rows/proofs remain exact05bytes and prior reading/spec/consumer evidence is explicitly reused, not49newreads or re-signatures. '
 'Root reran reviewed worker66 actual-source fullcompact controlled assertions and wholebatch/literalchecks with OSnetwork/modelcalls denied; this is not a new independently authored66case suite. '
 '1299pending is honestly accepted as pending and separate new1299source/visibility/inventory issue is not resolved by this batch. '
 'No operating139catalog/native0 is changed; stage5all18250/latestpending0/final149hybrid and stages6–8 remain unfinished. No actual user-request/compose/runtime/render/pixels or expert/human approval is claimed.')
acceptance={'schema':nr.ACCEPTANCE,'actor':'/root',**{k:verified[k]for k in ['assignment_sha256','input_sha256','batch_sha256','note_sha256']},'reviews':{cid:{'review_sha256':c.digest(row),'status':row['status']}for cid,row in verified['records'].items()},'reason':reason}
save(O/'ROOT-ACCEPTANCE.json',acceptance);nr.verify_acceptance(ROOT,ref(O/'ROOT-ACCEPTANCE.json'),verified)
assert not (R/'native_batches/review11870-01250-01300-05/ROOT-ACCEPTANCE.json').exists()
paths=[]
for rel in ['native_batches/review11870-01250-01300-05','native_batches/review11870-01250-01300-06','native-inputs/first50-quote-repair-plan-17','native-inputs/prepared/review11870-01250-01300-06']:
 paths.extend(p for p in (R/rel).rglob('*')if p.is_file()and '__pycache__'not in p.parts)
for folder in ['authored','worker-notes']:
 for pattern in ['native_05250_peer05.*','native_05250_peer06.*']:
  paths.extend(p for p in (R/folder).glob(pattern)if p.is_file())
paths.extend(R/p for p in ['authored/native_1255_quote_reanchor_05_proposal_v1.json','ROOT-FIRST50-1255-GROUNDING-HOLD-01.json','ROOT-FIRST50-1255-CONSUMER-CHECK-01.json','prepare_first50_quote_repair_root_01.py','check_first50_1255_repair_root_01.py']);paths.extend([Path(__file__).resolve(),ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'])
pins={}
for p in sorted(set(paths)):
 raw=p.read_bytes()
 if p.suffix=='.json':json.loads(raw)
 if p.suffix=='.py':ast.parse(raw)
 pins[str(p.relative_to(ROOT))]=hashlib.sha256(raw).hexdigest()
assert not subprocess.check_output(['git','diff','--name-only','--','skills/photo-prompt-image-generator/assets','skills/photo-prompt-image-generator/scripts','tests'],text=True).strip()
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for p,h in protected.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
rows=list(verified['records'].values());approved=[x for x in rows if x['status']=='approved'];assert rows[-1]['ordinal']==1299 and rows[-1]['proof']is None
report={'schema':'photo-root-first50-149-research-integration/v1','actor':'/root','accepted_batch':ref(O/'BATCH.json'),'acceptance':ref(O/'ROOT-ACCEPTANCE.json'),'assignment':ref(D/'ASSIGNMENT.json'),'note':ref(O/'NOTE.json'),'worker_actual_unique_source_reads':50,'accepted_research_approved':49,'accepted_pending':1,'pending_ordinal':1299,'facts':sum(len(x['proof']['facts'])for x in approved),'source_units':sum(len(x['proof']['source_units'])for x in approved),'actual_RIDs':sum(len(x['proof']['effect_sets'])for x in approved),'manual_samefact_views':sum(len(x['proof'].get('manual_role_views',[]))for x in approved),'independent_peer_final':ref(peer),'root_controlled_actual_source_rerun':ref(R/'ROOT-FIRST50-1255-CONSUMER-CHECK-01.json'),'root_controlled_assertions':66,'other_whole_rows_unchanged':49,'new_other49_reads_or_signatures':0,'root_read_and_evidence_boundary':reason,'history_05_accepted':False,'operating_source_or_catalog_or_bindings_changed':False,'operating_native_qualified_count':0,'full_final149hybrid_search_completed':False,'stage5_and6_to8_completed':False,'Gemini_calls':0,'embedding_inference_calls':0,'files':pins,'protected_files':protected}
output=R/'ROOT-FIRST50-149-INTEGRATION-01.json';save(output,report)
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip();names=sorted(set(pins)|{str(output.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);subprocess.run(['git','diff','--cached','--check'],check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==set(names)
for p in names:assert subprocess.check_output(['git','show',':'+p])==(ROOT/p).read_bytes(),p
print(json.dumps({'files':len(names),'research_approved':49,'research_pending':1,'facts':report['facts'],'root_controlled_checks':66,'operating_changes':0,'Gemini_calls':0}))
