"""Select a same-image relation guard without inventing visibility or permission."""
import copy,gzip,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0] in {'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),sha256=c.digest(read(p)))
parent=R/'native-inputs/root-simple5-diagnostic7-source-plan-21';current=read(parent/'CURRENT-PROPOSAL.json.gz');original=read(R/'SOURCE.json.gz')
assert c.digest(current)=='b1c48c867ce0a94d5648b0bfb7935605e4d7708951b36268930ea26523746092'
p=R/'same-image-pr-review11870-01/SOURCE-PROPOSAL-v1.json';proposal=read(p)
assert c.digest(proposal)=='5b4b468242727cffffaa1075f56f69e4d3b74e8df8bbfdbb969c595a29726132'
cid=proposal['candidate_id'];before=current['candidates'][cid];after=proposal['after_full']
assert cid=='cand_2e72784a26885ceaa1d645d25bd9a468' and before==proposal['before_full']
assert c.digest(before)=='e9870bd290b1bd682d9d79001c29a4affa65a4618ce2ed0cd43d46b0d15cfd33'
assert c.digest(after)=='86a9180d68eda67e038a2a5950263585a1eac74f5c4c67f85b33d09cd8cf95ef'
for key in ['effects','provenance','record_kind']:assert before[key]==after[key]
assert {k:v for k,v in before['content'].items() if k!='application_contract'}=={k:v for k,v in after['content'].items() if k!='application_contract'}
assert after['content']['application_contract'].startswith(before['content']['application_contract'])
assert before['conditions']['native_guards']['rules']==after['conditions']['native_guards']['rules'][:-1]
n.validate_source_guards(after['conditions']['native_guards'])
reason=('Root selects the full unchanged physical-handoff application with one additional scalar frozen relation binding the same existing item to the same selected actual image. '
 'Keep the separate literal visible preservation obligation, all original E3/values/modes/operations/all actual receiver inventories and five existing guards. '
 'Presence, source-target names, unrelated images or fabricated source spans cannot supply actual image correspondence. The actual core input and spans require independent review before freezing. '
 'Root read the complete new source/proposal helper, exact App extension and guard, whole synthetic experiment implementation and integration design; prior original/current1299 whole-source reads remain prior evidence rather than new reads. '
 'Frozen v3 scalar relation execution is available; guard_support role evidence does not opt in to v3 and no such role shortcut is authorized. '
 'The separate one-E synthetic24-case experiment and four false-trusted-core probes do not qualify actual1299 E3 or final preservation. '
 'Mandatory permission envelope and final scalar PR consumer integration remain separate pending work, with all original permission constraints conjunctive. This source choice creates no proof or approval.')
D=R/'native-inputs/root-same-image-guard-source-plan-22';D.mkdir(exist_ok=False)
memo=dict(schema='photo-root-same-image-source-selection/v1',actor='/root',parent_source=ref(parent/'CURRENT-PROPOSAL.json.gz'),proposal=ref(p),candidate_id=cid,ordinal=1299,whole_before=before,whole_after=after,reason=reason,source_proof_or_approval_created=False,operating_changes=0,Gemini_calls=0)
save(D/'ROOT-SOURCE-SELECTION.json',memo)
approval=read(parent/'SOURCE-APPROVAL.json');entry=next(x for x in approval['changes'] if x['candidate_id']==cid)
assert entry['after']==before and entry['before']==original['candidates'][cid]
entry['after']=copy.deepcopy(after)
entry['delta']=[dict(pointer='/content/application_contract',before_exists=False,before=None,after_exists=True,after=after['content']['application_contract'],reason=reason),dict(pointer='/conditions',before_exists=True,before=entry['before']['conditions'],after_exists=True,after=after['conditions'],reason=reason),dict(pointer='/effects',before_exists=True,before=entry['before']['effects'],after_exists=True,after=after['effects'],reason=entry['reason'])]
entry['reason']+=' '+reason;entry['provenance'] += [ref(p),ref(D/'ROOT-SOURCE-SELECTION.json')]
current['candidates'][cid]=copy.deepcopy(after);approval['current_source_sha256']=c.digest(current);approval['reason']+=' Same1299 existing source receives explicit same-item/same-selected-image preservation condition; unique changed candidates remain96.'
prep.approve_source(ROOT,original,current,approval);c.validate(current);assert len(approval['changes'])==96
with (D/'CURRENT-PROPOSAL.json.gz').open('xb')as f:f.write(gzip.compress(c.canonical_bytes(current),mtime=0))
save(D/'SOURCE-APPROVAL.json',approval)
plan=read(R/'native-inputs/root-hands-exchange-source-plan-14/PLAN.json');prior_path=R/'native_batches/review11870-01299-149-06/BATCH.json';prior=read(prior_path)
assert len(prior['records'])==1 and prior['records'][0]['candidate_id']==cid and prior['records'][0]['status']=='pending' and prior['records'][0]['proof'] is None
plan.update(current_proposal=ref(D/'CURRENT-PROPOSAL.json.gz'),source_approval=ref(D/'SOURCE-APPROVAL.json'),catalog_approval=ref(R/'NATIVE-CATALOG-APPROVAL-149-V6.json'),reason=reason)
plan['required_revisions']={cid:dict(prior_review=dict(artifact=ref(prior_path),pointer='/records/0',sha256=c.digest(prior['records'][0])),memo_artifacts=[ref(D/'ROOT-SOURCE-SELECTION.json'),ref(p)],reason=reason)}
save(D/'PLAN.json',plan)
out,receipt=prep.write_inputs(ref(D/'PLAN.json'),'review11870-01299-149-07',actor='/root',root=ROOT,here=R)
report=dict(schema='photo-root-same-image-source-preparation/v1',source=ref(D/'CURRENT-PROPOSAL.json.gz'),prepared=str(out.relative_to(ROOT)),prepared_count=1,preparation_actual_read_count=0,unique_source_corrections=96,existing_guards_retained=5,new_relation_guards=1,original_E3_exact=True,native_proofs_created=0,operating_changes=0,Gemini_calls=0,remaining_permission_envelope_final_PR_integration=True)
save(D/'ROOT-PREPARATION-VERIFICATION.json',report);print(json.dumps(report))
