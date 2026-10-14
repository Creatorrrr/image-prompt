"""Select five complete applications and preserve seven positive template kinds.

Explicit sparse preparation only; no proof, approval status, or read attestation.
The contiguous preparation helper is unchanged.
"""
import copy,gzip,hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
nr=prep.reviews;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def save(p,v):
 with p.open('xb') as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),sha256=c.digest(read(p)))
def prepare_sparse(name,rows,original,current,current_ref,order_ref,catalog_review,memo_ref,prior=None):
 order=nr.artifact(ROOT,order_ref);ids=[r['candidate_id'] for r in rows];ordinals=[r['ordinal'] for r in rows]
 assert len(order)==len(set(order))==18250 and set(order)==set(original['candidates'])==set(current['candidates'])
 assert len(ids)==len(set(ids)) and ordinals==sorted(set(ordinals)) and [order[o] for o in ordinals]==ids
 selection={};packets={};historical={};required={};closures={};bindings={};cache={};original_sha=c.digest(original);catalog_sha=c.digest(original['slot_catalog'])
 for row in rows:
  cid=row['candidate_id'];loc=row['locator'];packet={k:row['packet'][k] for k in ('file','file_sha256','sha256')}
  historical[cid]=nr.compiled_review(ROOT,R,loc,original,cid,packet,original_sha,catalog_sha,cache);selection[cid]=loc;packets[cid]=packet
  hashes=n.referenced_records(current['candidates'][cid],current);closures[cid]={key:copy.deepcopy(current['candidates'][key]) for key in hashes if c.ID.fullmatch(key)};bindings[cid]={key:copy.deepcopy(current['slot_bindings'][key]) for key in hashes if c.BINDING_ID.fullmatch(key)}
  if prior is None:
   previous=dict(artifact=ref(ROOT/loc['file']),pointer='/decisions/'+str(loc['item']-1),sha256=loc['row_sha256'])
  else:
   old=read(prior);i=next(i for i,r in enumerate(old['records']) if r['candidate_id']==cid);previous=dict(artifact=ref(prior),pointer='/records/'+str(i),sha256=c.digest(old['records'][i]))
  required[cid]=dict(prior_review=previous,memo_artifacts=[memo_ref],reason='Fresh exact current source judgement. Preserve old statuses/proofs as history. No approval from old kind, metadata, unfilled parameters, shape or hash. Exact unchanged proofs may be reused only with disclosed perCID source/catalog/closure equality and valid original review.')
 nr.verify_catalog(original['slot_catalog'],current['slot_catalog'],catalog_review,ROOT);prep.required_revisions(ROOT,required,ids)
 out=R/'native-inputs/prepared'/name;out.mkdir(exist_ok=False)
 inp=dict(schema=nr.INPUT,actor='/root',ids=ids,original_snapshot=ref(R/'SOURCE.json.gz'),current_snapshot=current_ref,order=order_ref,catalog_review=catalog_review,original_decisions=selection,original_packets=packets,required_revisions=required)
 save(out/'INPUT.json',inp)
 assignment=dict(schema=nr.ASSIGNMENT,actor='/root',task_name='/root/review_05250_06250',model='gpt-6.1-sol',reasoning_effort='high',ids=ids,ordinals=ordinals,input=ref(out/'INPUT.json'));nr.validate_assignment_identity(assignment);save(out/'ASSIGNMENT.json',assignment)
 packet=dict(schema=prep.PACKET,preparation_plan=memo_ref,assignment_sha256=c.digest(assignment),input_sha256=c.digest(inp),prepared_count=len(ids),actual_read_count=0,ids=ids,ordinals=ordinals,
  original_records={cid:original['candidates'][cid] for cid in ids},current_records={cid:current['candidates'][cid] for cid in ids},references=closures,reference_bindings=bindings,historical_compiled_rows=historical,
  historical_statuses={cid:r['status'] for cid,r in historical.items()},original_compiled_artifacts={cid:loc['file']+'#item='+str(loc['item']) for cid,loc in selection.items()})
 save(out/'PREPARED-PACKET.json',packet)
 receipt=dict(schema='photo-root-exact-sparse-preparation/v1',source=current_ref,assignment=ref(out/'ASSIGNMENT.json'),input=ref(out/'INPUT.json'),packet=ref(out/'PREPARED-PACKET.json'),
  exact_explicit_sparse_ordinals=True,production_inventory=18250,prepared_count=len(ids),actual_read_count=0,native_proofs_created=0,operating_changes=0,Gemini_calls=0,contiguous_helper_modified=False)
 save(out/'PREPARATION.json',receipt);return str(out.relative_to(ROOT))
def main():
 parent=R/'native-inputs/root-illumination-guard-source-plan-20';current=read(parent/'CURRENT-PROPOSAL.json.gz');original=read(R/'SOURCE.json.gz');before_snapshot=copy.deepcopy(current)
 assert c.digest(current)=='a3ac73e618b4443855c9cba07a0b0f9977c65cd19d0dcb92188ea2b208fddec7'
 approval=read(parent/'SOURCE-APPROVAL.json');plan=read(parent/'PLAN.json');catalog=nr.artifact(ROOT,plan['catalog_approval'])
 simple=R/'authored/native_05250_simple5-source-applications-source84-149-v1.json';assert hashlib.sha256(simple.read_bytes()).hexdigest()=='2a520e8f8a4e22fb98d5354271e60b403677bd317b580333d18277df23a05c94'
 proposed=read(simple)['records'];assert [r['ordinal'] for r in proposed]==[6131,6162,6191,6214,6220]
 diagnostic_ordinals=[12005,12023,12034,12050,12082,12156,12159]
 kind_rows=[]
 for ordinal in diagnostic_ordinals:
  p=R/f'authored/native_diag70_05250_recheck7.{ordinal}.memo-v1.json';v=read(p);cid=v['candidate_id'];before=current['candidates'][cid];alternative=v['unselected_minimal_alternatives'][1];after=alternative['whole_after']
  assert v['ordinal']==ordinal and v['whole_source_before']==before==alternative['whole_before']==original['candidates'][cid]
  assert before['record_kind']=='diagnostic' and after['record_kind']=='visual_option'
  assert {k:x for k,x in before.items() if k!='record_kind'}=={k:x for k,x in after.items() if k!='record_kind'}
  kind_rows.append(dict(ordinal=ordinal,candidate_id=cid,before=before,after=after,memo=ref(p),reason='Root preserves the complete affirmative/conditional source obligation and selects kind restoration only. '+v['why_prior_nonsemantic_basis_is_not_sufficient'],complete_positive_contract_selected=False,native_proof=None))
 simple_rows=[]
 for row in proposed:
  cid=row['candidate_id'];before=current['candidates'][cid];after=row['whole_proposed_after'];assert before==row['whole_current_before']==original['candidates'][cid]
  assert c.digest(before)==row['before_sha256'] and c.digest(after)==row['after_sha256']
  assert before['conditions']==after['conditions'] and before['provenance']==after['provenance'] and before['record_kind']==after['record_kind']
  if row['ordinal']==6220:assert before['effects']==after['effects']
  else:assert before['effects']['properties']==[] and set(before['effects']['dimensions'])<=set(after['effects']['dimensions'])
  simple_rows.append(dict(ordinal=row['ordinal'],candidate_id=cid,before=before,after=after,reason='Root selects the disclosed independently existing scene/whole-image application, retaining original conditions and permissions. '+row['reason'],native_proof=None))
 D=R/'native-inputs/root-simple5-diagnostic7-source-plan-21';D.mkdir(exist_ok=False)
 memo=dict(schema='photo-root-source-selection-and-kind-restoration/v1',actor='/root',parent_source=ref(parent/'CURRENT-PROPOSAL.json.gz'),simple5_proposal=ref(simple),
  simple5=simple_rows,diagnostic7=kind_rows,root_read_scope='Root directly read all5 complete actual current and proposed after sources plus individual meanings; root read all7 complete original source definitions, exact origins, compatibility rules, individual purpose/role/meaning comparisons and exact kind-only afters. Whole parent28-route and original5B/provenance reading is separately credited to the worker, not newly claimed by root.',
  diagnostic_boundary='Previous65 diagnostic proofs are shape-valid historical proposals, not root accepted. Seven additional nonsemantic rationales are withdrawn. Twelve restored positive templates remain pending full application/facts/roles. Remaining58 exact diagnostic source/proof pairs require explicit latest equality/revalidation before acceptance.',
  simple5_boundary='Five selected sources now have actual effects/PR and source intent for fresh native proof.6214 explicitly repairs stale KO/alias and selects quiet as visual atmosphere with setting/timing/atmosphere E;6220 retains original style/image_plane/image.detail and literal continuous/readable PR. No actual owner/preservation witness is asserted by source selection.',
  source_choices=5,kind_restorations=7,native_proofs_created=0,operating_changes=0,Gemini_calls=0)
 save(D/'ROOT-SOURCE-SELECTION.json',memo)
 for row in kind_rows+simple_rows:
  cid=row['candidate_id'];before=row['before'];after=row['after'];deltas=[]
  if row in kind_rows:deltas=[dict(pointer='/record_kind',before_exists=True,before='diagnostic',after_exists=True,after='visual_option',reason=row['reason'])]
  else:
   proposal=next(r for r in proposed if r['candidate_id']==cid)
   for d in proposal['exact_deltas']:
    assert d['operation'] in ('add','replace')
    deltas.append(dict(pointer=d['pointer'],before_exists=d['operation']=='replace',before=d['before'],after_exists=True,after=d['after'],reason=row['reason']))
  assert nr.apply_delta(before,deltas)==after
  current['candidates'][cid]=copy.deepcopy(after);approval['changes'].append(dict(candidate_id=cid,before=before,after=after,delta=deltas,reason=row['reason'],provenance=[ref(D/'ROOT-SOURCE-SELECTION.json')]+([row['memo']] if 'memo' in row else [ref(simple)])))
 approval['current_source_sha256']=c.digest(current);approval['reason']+=' Root selects5 bounded source applications and restores7 additional positive-template kinds. Unique source corrections96; no native/operating approval.'
 prep.approve_source(ROOT,original,current,approval);c.validate(current)
 assert len(approval['changes'])==96
 assert {cid for cid in current['candidates'] if current['candidates'][cid]!=before_snapshot['candidates'][cid]}=={r['candidate_id'] for r in kind_rows+simple_rows}
 assert Counter(r['record_kind'] for r in current['candidates'].values())['diagnostic']==58
 assert all(current[k]==before_snapshot[k] for k in ('slot_catalog','slot_bindings','policies'))
 with (D/'CURRENT-PROPOSAL.json.gz').open('xb') as f:f.write(gzip.compress(c.canonical_bytes(current),mtime=0))
 save(D/'SOURCE-APPROVAL.json',approval)
 diag_index=read(R/'authored/native_diag70_05250_locator-index-v1.json')['rows']
 diag=[dict(ordinal=r['ordinal'],candidate_id=r['candidate_id'],locator=r['original_compiled_locator'],packet=r['original_packet']) for r in diag_index]
 five=[dict(ordinal=r['ordinal'],candidate_id=r['candidate_id'],locator=r['provenance']['compiled_locator'],packet=r['provenance']['original_packet']) for r in proposed]
 output70=prepare_sparse('review05250-diagnostic70-149-02',diag,original,current,ref(D/'CURRENT-PROPOSAL.json.gz'),plan['order'],catalog['review'],ref(D/'ROOT-SOURCE-SELECTION.json'),R/'native_batches/review05250-diagnostic70-149-01/BATCH.json')
 output5=prepare_sparse('review05250-simple5-149-01',five,original,current,ref(D/'CURRENT-PROPOSAL.json.gz'),plan['order'],catalog['review'],ref(D/'ROOT-SOURCE-SELECTION.json'))
 value=dict(schema='photo-root-source96-sparse-preparation/v1',source=ref(D/'CURRENT-PROPOSAL.json.gz'),unique_source_changes=96,new_application_choices=5,new_kind_restorations=7,total_restored_positive_kinds=12,research_diagnostic_count=58,
  prepared=[output70,output5],actual_worker_read_count_from_preparation=0,native_proofs_created=0,operating_changes=0,Gemini_calls=0)
 save(D/'ROOT-PREPARATION-VERIFICATION.json',value);print(json.dumps(value))
if __name__=='__main__':main()
