"""Select exact existing illumination relations; no proof or operating activation."""
import copy,gzip,hashlib,json,sys
from pathlib import Path
ROOT=Path.cwd();R=ROOT/'docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.dont_write_bytecode=True;sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
import photo_candidate_corpus as c
import photo_semantic_evidence as n
sys.path.insert(0,str(R));import prepare_native_inputs as prep
sys.path[:0]=[str(G/'scripts'),str(G/'precore')]
def read(p):return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
def save(p,v):
 with p.open('xb') as f:f.write(c.canonical_bytes(v)+b'\n')
def ref(p):return dict(file=str(p.relative_to(ROOT)),file_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),sha256=c.digest(read(p)))
def main():
 proposal=R/'authored/native_06250_first20_149_03.guard-source-proposals.json'
 assert hashlib.sha256(proposal.read_bytes()).hexdigest()=='3b293118696cf2e4f87aa33efd98b607438c06ea216160e34967b0314752e2f4'
 rows=read(proposal)['proposals'];assert len(rows)==7 and {r['ordinal'] for r in rows}=={0,1,2,6,7,11,12}
 parent=R/'native-inputs/root-first20-source-plan-19';current=read(parent/'CURRENT-PROPOSAL.json.gz');original=read(R/'SOURCE.json.gz');old=copy.deepcopy(current)
 assert c.digest(current)=='609e72864631ffccd711d2a6601ac060bea0a92f86985c7633a3fbea59d82ae5'
 approval=read(parent/'SOURCE-APPROVAL.json');D=R/'native-inputs/root-illumination-guard-source-plan-20';D.mkdir(exist_ok=False)
 reason=('Root selects the exact complete existing-carrier source/receiving-scope relation described in each already selected application. '
 'Explicit native guards bind each independently existing actual receiver to the actual selected source owner ID; a complete nonempty pre-discovery inventory is required, not a source-chosen subset. '
 'Keep every original canonical effect, operation and all receivers; actual source type/quality/phase remains E, not desired-value P. '
 'Lab use is independent contextual designation; golden-hour source and receivers belong to the same actual scene; soft-window path is independently existing and links that exact source to every receiver. '
 'No fixed neutral light role, main owner, missing endpoint, created object, lighting setup or scope fallback is authorized. '
 'Root directly read all7 complete proposed after records, exact original/current and relevant full role specs in this ongoing task. This source selection creates no native proof.')
 memo=dict(schema='photo-root-illumination-guard-source-selection/v1',actor='/root',parent_source=ref(parent/'CURRENT-PROPOSAL.json.gz'),proposal=ref(proposal),
  worker_whole_after_read=ref(R/'worker-notes/native_06250_first20_149_03.guard-source-proposals-read01.json'),reason=reason,
  records=[dict(ordinal=r['ordinal'],candidate_id=r['candidate_id'],whole_before=r['whole_before'],whole_after=r['whole_after']) for r in rows],
  delta_metadata='Worker proposal states exact before/after for existing conditions/App. Root writes strict before_exists/after_exists metadata and composes final original-to-current nonoverlapping deltas; no proposal semantics are inferred or changed.',
  preserved_native_approval_boundary='All newly selected sources require fresh whole-source native qualification and controlled actual-source full/compact tests. Existing7 and newly authored unchanged6 proofs may be reused only after exact source/catalog/closure equality, without new signatures or duplicate counts.',
  native_proofs_created=0,operating_changes=0,Gemini_calls=0)
 save(D/'ROOT-SOURCE-SELECTION.json',memo)
 for row in rows:
  cid=row['candidate_id'];before=row['whole_before'];after=row['whole_after'];assert before==current['candidates'][cid]
  assert c.digest(before)==row['before_sha256'] and c.digest(after)==row['after_sha256']
  assert before['conditions']=={} and after['conditions']['native_guards']['schema']=='photo-native-source-guards/v3'
  assert before['effects']==after['effects'] and before['provenance']==after['provenance'] and before['record_kind']==after['record_kind']
  assert {k:v for k,v in before['content'].items() if k!='application_contract'}=={k:v for k,v in after['content'].items() if k!='application_contract'}
  assert after['content']['application_contract'].startswith(before['content']['application_contract'])
  current['candidates'][cid]=copy.deepcopy(after)
  entry=next(e for e in approval['changes'] if e['candidate_id']==cid);assert entry['before']==original['candidates'][cid]
  entry['after']=copy.deepcopy(after)
  entry['delta']=[dict(pointer='/content/application_contract',before_exists=False,before=None,after_exists=True,after=after['content']['application_contract'],reason=reason),
                  dict(pointer='/effects',before_exists=True,before=entry['before']['effects'],after_exists=True,after=after['effects'],reason=entry['reason']),
                  dict(pointer='/conditions',before_exists=True,before=entry['before']['conditions'],after_exists=True,after=after['conditions'],reason=reason)]
  entry['reason']+=' '+reason;entry['provenance'] += [ref(proposal),ref(D/'ROOT-SOURCE-SELECTION.json')]
 approval['current_source_sha256']=c.digest(current);approval['reason']+=' Seven existing source choices refined with exact existing illumination/path/scene guards; unique changed CIDs remain84.'
 prep.approve_source(ROOT,original,current,approval);c.validate(current)
 assert len(approval['changes'])==84 and {cid for cid in current['candidates'] if current['candidates'][cid]!=old['candidates'][cid]}=={r['candidate_id'] for r in rows}
 assert all(current[k]==old[k] for k in ('slot_catalog','slot_bindings','policies'))
 with (D/'CURRENT-PROPOSAL.json.gz').open('xb') as f:f.write(gzip.compress(c.canonical_bytes(current),mtime=0))
 save(D/'SOURCE-APPROVAL.json',approval)
 plan=read(parent/'PLAN.json');plan.update(current_proposal=ref(D/'CURRENT-PROPOSAL.json.gz'),source_approval=ref(D/'SOURCE-APPROVAL.json'),reason=reason)
 for req in plan['required_revisions'].values():
  req['memo_artifacts'].append(ref(D/'ROOT-SOURCE-SELECTION.json'));req['reason']+=' '+reason
 save(D/'PLAN.json',plan)
 out,receipt=prep.write_inputs(ref(D/'PLAN.json'),'review06250-00000-00020-149-04',actor='/root',root=ROOT,here=R)
 value=dict(schema='photo-root-illumination-guard-preparation/v1',source=ref(D/'CURRENT-PROPOSAL.json.gz'),unique_source_changes=84,refined_existing_CIDs=7,
  unchanged_candidate_records=18243,original_effects_exact=True,old_positive_fields_preserved=True,original_scope_dimensions_preserved=True,
  native_proofs_created=0,operating_changes=0,Gemini_calls=0,prepared=str(out.relative_to(ROOT)),actual_worker_read_count=0)
 save(D/'ROOT-PREPARATION-VERIFICATION.json',value);print(json.dumps(value))
if __name__=='__main__':main()
