"""Preserve six unresolved affirmative contracts; no native proof or approval."""
import copy,gzip,hashlib,importlib.abc,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
class Deny(importlib.abc.MetaPathFinder):
 def find_spec(self,fullname,path=None,target=None):
  if fullname.split('.')[0]in{'torch','transformers','sentence_transformers','tensorflow','jax','mlx','google','openai','anthropic','requests','httpx'}:raise AssertionError(fullname)
sys.meta_path.insert(0,Deny());sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
sys.path.insert(0,str(R));import prepare_simple5_and_diagnostic7_root_01 as sparse
prep=sparse.prep;nr=sparse.nr;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=raw(p),sha256=c.digest(read(p)))
def save(p,v):
 with p.open('xb')as f:f.write(c.canonical_bytes(v)+b'\n')
parent=R/'native-inputs/root-same-image-guard-source-plan-22-R02';current=read(parent/'CURRENT-PROPOSAL.json.gz');previous=copy.deepcopy(current);original=read(R/'SOURCE.json.gz')
assert c.digest(current)=='5ed4478da12e828918e4b65442c0444c00c3f639774a8900a88de5e3101af550'
ordinals=[12016,12041,12044,12055,12056,12369];rows=[]
for ordinal in ordinals:
 path=R/f'authored/native_diag70_05250_recheck6.{ordinal}.memo-v1.json';memo=read(path);cid=memo['candidate_id'];alt=memo['unselected_minimal_alternatives'][1]
 assert alt['id']=='B_preserve_positive_contract_restore_kind_only'
 b,a=alt['whole_before'],alt['whole_after'];assert b==current['candidates'][cid]==original['candidates'][cid]==memo['whole_original']==memo['whole_current96']
 assert b['record_kind']=='diagnostic' and a['record_kind']=='visual_option'
 assert {k:v for k,v in b.items()if k!='record_kind'}=={k:v for k,v in a.items()if k!='record_kind'}
 assert nr.apply_delta(b,alt['delta'])==a
 rows.append(dict(ordinal=ordinal,candidate_id=cid,before=b,after=a,memo=ref(path),reason=memo['why_prior_all_nonsemantic_basis_is_insufficient'],pending_application=alt['remaining_gap']))
D=R/'native-inputs/root-diagnostic6-kind-source-plan-23';D.mkdir(exist_ok=False)
reason=('Root restores kind only for six exact source bodies whose positive/conditional obligations cannot be dismissed by router/guard metadata, empty E or unfilled concrete parameters. '
 'Keep head/gaze/facial cue selection and non-inference boundaries; three linked but non-equivalent performer/avatar/persona layers; universal explicitly declared adult scope with peer/colleague/partner/client/neighbor alternatives; baseline hair AND one explained state transition; separately evidenced agency/consequence/limit/recovery; both adult-life topic definitions and their independent age declaration. '
 'Root directly read all six complete original/current definitions, exact whole original node/provenance records, individual purpose/AND-OR/role-mode limits and B kind-only afters (three full afters and three complete non-kind equality-factored afters). '
 'Worker whole original5B/parent26/origin33/full25spec and actual validator-code reads are delegated evidence, not newly claimed root full parent/code reading. '
 'None of these restored templates is native approved. No concrete cue, age change, participant, three humans, hair transition, private mind, workplace or action is invented; no existing desired value is frozen merely to avoid effect review. '
 'A check-only narrowing is unselected. Remaining52 diagnostics require the same consistency review before any acceptance. No historical batch/proof is overwritten, automatically re-signed or partially accepted.')
selection=dict(schema='photo-root-positive-kind-restoration/v1',actor='/root',parent_source=ref(parent/'CURRENT-PROPOSAL.json.gz'),reason=reason,selected=rows,unique_source_changes_after=102,research_diagnostic_after=52,positive_templates_pending_after=18,native_proofs_created=0,native_approvals_created=0,operating_changes=0,Gemini_calls=0)
save(D/'ROOT-SOURCE-SELECTION.json',selection)
approval=read(parent/'SOURCE-APPROVAL.json')
for row in rows:
 current['candidates'][row['candidate_id']]=copy.deepcopy(row['after'])
 approval['changes'].append(dict(candidate_id=row['candidate_id'],before=row['before'],after=row['after'],delta=[dict(pointer='/record_kind',before_exists=True,before='diagnostic',after_exists=True,after='visual_option',reason=reason+' '+row['reason'])],reason=reason+' '+row['reason'],provenance=[row['memo'],ref(D/'ROOT-SOURCE-SELECTION.json')]))
approval['current_source_sha256']=c.digest(current);approval['reason']+=' Six further conditional source kinds restored, with complete original text retained and all native judgments pending. Unique changed candidates102.'
prep.approve_source(ROOT,original,current,approval);c.validate(current)
assert len(approval['changes'])==102 and sum(r['record_kind']=='diagnostic'for r in current['candidates'].values())==52
assert {cid for cid in current['candidates']if current['candidates'][cid]!=previous['candidates'][cid]}=={r['candidate_id']for r in rows}
assert all(current[k]==previous[k]for k in ['slot_catalog','slot_bindings','policies'])
with(D/'CURRENT-PROPOSAL.json.gz').open('xb')as f:f.write(gzip.compress(c.canonical_bytes(current),mtime=0))
save(D/'SOURCE-APPROVAL.json',approval)
index=read(R/'authored/native_diag70_05250_locator-index-v1.json')['rows'];chosen=[dict(ordinal=r['ordinal'],candidate_id=r['candidate_id'],locator=r['original_compiled_locator'],packet=r['original_packet'])for r in index]
catalog=read(R/'NATIVE-CATALOG-APPROVAL-149-V6.json');order_ref=read(parent/'PLAN.json')['order']
output=sparse.prepare_sparse('review05250-diagnostic70-149-03',chosen,original,current,ref(D/'CURRENT-PROPOSAL.json.gz'),order_ref,catalog['review'],ref(D/'ROOT-SOURCE-SELECTION.json'),R/'native_batches/review05250-diagnostic70-149-02/BATCH.json')
report=dict(schema='photo-root-diagnostic6-kind-preparation/v1',source=ref(D/'CURRENT-PROPOSAL.json.gz'),prepared=output,prepared_count=70,preparation_actual_read_count=0,research_diagnostic_count=52,restored_positive_pending_count=18,unique_source_changes=102,native_proofs_created=0,root_diagnostic_acceptances=0,operating_changes=0,Gemini_calls=0,remaining52_consistency_review_pending=True)
save(D/'ROOT-PREPARATION-VERIFICATION.json',report);print(json.dumps(report))
