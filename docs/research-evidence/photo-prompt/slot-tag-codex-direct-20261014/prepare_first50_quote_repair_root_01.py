"""One field-local proof repair input; all other exact reviewed inputs stay unchanged."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014';G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c,photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return {'file':str(p.relative_to(ROOT)),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sha256':c.digest(read(p))}
D=R/'native-inputs/first50-quote-repair-plan-17';D.mkdir(exist_ok=False);old=R/'native_batches/review11870-01250-01300-05/BATCH.json';batch=read(old);assert c.digest(batch)=='0666d0c5035fac8818e95d818014e158336d1c04d4226a34064eee9ad1c77e90'
cid=batch['records'][5]['candidate_id'];row=batch['records'][5];assert row['ordinal']==1255
fact=next(f for f in row['proof']['facts']if f['id']=='nearEn');assert fact['quote']=='near the subject' and fact['value']['value']=='near_same_holder_own_side'
reason=('Root full focal source/fact/unit review found1255 EN near the subject does not independently state the complete near_same_holder_own_side spatial value. '
 'Worker and independent peer acknowledged the field-local stronger-quote gap after the earlier peer45 report. '
 'Delete that unsupported direct duplicate nearEn only; keep full nearKo/nearApp actual placement E, original target held_object and receiver holder, set_value, all guards and presence P. '
 'EN ordinary holding and neutral facts remain; add a wholeEN one-hop partial_restatement to the directly grounded full nearApp. '
 'No source text, catalog, actual E/property/value/receiver/mode or condition is changed. '
 'All other49 rows, including1299 exactsource09pending, remain byte-identical to05; their actual prior direct reading/spec/counterfactual provenance is explicitly reused, not described as49new reads or proofs. '
 'The05 entire batch is unaccepted history, and the earlier35/10peer records are not silently rewritten. Root acceptance waits for the new1255 exactproof, actual-source fullcompact checks and corrected finalpeer conclusion.')
memo={'schema':'photo-root-native-field-local-quote-repair/v1','actor':'/root','prior_batch':ref(old),'candidate_id':cid,'ordinal':1255,'exact_unsupported_fact':fact,'decision':'hold05_until_explicit1255_grounding_repair','reason':reason,
 'root_read_scope':'Six focal full original/current source and actual payloads1253/1255/1262/1271/1296/1298, all their facts/units/maps/guards/views/roles, and13 relevant full149 role/boundary specs. No root claim to personally read all50 source or all49proofs. Worker all50 and independent peer coverage are separately credited.',
 'requirements':['Freshly directly reread whole1255 source/5B/binding/emptyclosure/completeproof/used149spec before literal repair.',
 'Keep exact source09/catalog149V6/frozen50fd92 and every other49 complete row byte-identical. Existing source reads/proofs may be explicitly retained because these entire inputs are unchanged; do not re-sign or promote statuses.',
 'Regenerate only1255 reviewed native contract seal after actual literal change; no effect/target/Rx/value/mode/property/presence/disjointness deletion or newdimension.',
 'Actual same-source1255 full/compact validation, native qualification with independent fullsourceauthority, admission/consumer and every actual property/Rx/alias/ancestor/whole/P/guard lock must pass; preserve normal protected-dimension denies.',
 'Bind newBATCH+NOTE to this fresh input and exactrootmemo; compare49whole unchanged rows to05. Preserve05 and previouspeer bytes. No operating/code/source/Git/model/network actions.'],
 'source_changes':0,'catalog_changes':0,'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0}
save(D/'ROOT-1255-QUOTE-HOLD.json',memo);plan=copy.deepcopy(read(R/'native-inputs/first50-catalog149-recheck-plan-10/PLAN.json'));assert len(plan['assignment']['ids'])==50 and plan['assignment']['task_name']=='/root/review_11870_12250';plan['reason']=reason;plan['required_revisions'][cid]={'prior_review':{'artifact':ref(old),'pointer':'/records/5','sha256':c.digest(row)},'memo_artifacts':[ref(D/'ROOT-1255-QUOTE-HOLD.json')],'reason':reason}
save(D/'PLAN.json',plan);out,receipt=prep.write_inputs(ref(D/'PLAN.json'),'review11870-01250-01300-06',actor='/root',root=ROOT,here=R)
save(D/'ROOT-PREPARATION-VERIFICATION.json',{'prepared':str(out.relative_to(ROOT)),'prior_batch':ref(old),'reopened_ordinal':1255,'prepared':50,'other_complete_rows_reuse':49,'other_source_catalog_binding_policy_inputs_unchanged':True,'prior_direct_reads_not_new_reads':True,'source_changes':0,'native_proofs_created':0,'operating_changes':0,'Gemini_calls':0})
print(json.dumps({'prepared':str(out),'reopened_ordinal':1255,'source_changes':0,'native_proofs_created':0,'other_complete_rows_explicit_reuse':49}))
