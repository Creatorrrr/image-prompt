"""Serialize the fifteen individually reread optional-member scope decisions from revision02 note."""
import json,sys,copy
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R));import direct_review as d
original=H/'review_05250_06250_13000_13250.json';out=H/'review_05250_06250_13000_13250_revision02.json'
base=json.loads(original.read_text());revised=copy.deepcopy(base);review=json.loads((R/'worker-notes/review_05250_06250-13000-13250-revision02.json').read_text());items={x['ordinal']:x for x in review['items']};data=d.source();packet=json.loads((R/'packets/13000-250.json').read_text());diff=[]
for index,row in enumerate(revised['decisions']):
 ordinal=13000+index
 if ordinal in items:
  before=copy.deepcopy(row);assert len(row['uncertainties'])==1 and row['uncertainties'][0]['kind']=='reference_evidence_pointer_limit'
  row['uncertainties']=[];row['status']='approved';row['rejected_boundaries'].append('Optional-member scope re-review: '+items[ordinal]['decision'])
  changed=[k for k in row if row[k]!=before[k]];assert set(changed)=={'uncertainties','status','rejected_boundaries'}
  diff.append(dict(ordinal=ordinal,candidate_id=row['candidate_id'],changed_fields=changed,before_uncertainties=before['uncertainties'],after_uncertainties=[],added_boundary=row['rejected_boundaries'][-1],roles_unchanged=True,facts_unchanged=True,corrections_unchanged=True))
 else:assert row==base['decisions'][index]
out.write_text(json.dumps(revised,ensure_ascii=False,indent=2)+'\n')
for i,row in enumerate(revised['decisions'],1):
 full={**d.binding(data,row['candidate_id']),**row,'schema':d.SCHEMA,'reviewer':'Codex','review_method':'codex_direct_source_read','independent_human_review':False,'packet_sha256':d.c.digest(packet),'authored_decision':dict(file=str(out.relative_to(d.ROOT)),item=i,sha256=d.c.digest(row))};d.validate_decision(full,data)
assert len(diff)==15
note=json.loads((R/'worker-notes/review_05250_06250-13000-13250.json').read_text());note['authored_paths']=[str(out.relative_to(d.ROOT)),str(Path(__file__).resolve().relative_to(d.ROOT))];note['unresolved_ordinals']=[13000+i for i,row in enumerate(revised['decisions']) if row['status']=='needs_boundary_review'];note['status_counts']={s:sum(row['status']==s for row in revised['decisions']) for s in sorted({row['status'] for row in revised['decisions']})};note['revision']='02 optional-member scope correction';note['prior_authored_preserved']=str(original.relative_to(d.ROOT));note['revision_basis_note']=str((R/'worker-notes/review_05250_06250-13000-13250-revision02.json').relative_to(d.ROOT));note['changed_candidate_count']=15;note['authored_diff']=diff;note['qualification_issues'].append('Revision02 supersedes prior reference_evidence_pointer_limit diagnoses in exactly 15 records: optional child-only semantics excluded from parent whole_record; no roles/facts added or changed. Profile conflicts 13110/13225 retained. Prior JSON/note remain unchanged. All 250 revised rows validate_decision passed; structural validation is not independent semantic approval.');note['final_ready']=True
# Old unresolved detail is historical, never silently label it current.
for k in list(note):
 if k not in ['unresolved_ordinals','authored_diff'] and ('pending' in k.lower() or 'unresolved' in k.lower()):note['prior_'+k]=note.pop(k)
(R/'worker-notes/review_05250_06250-13000-13250-revision02-final.json').write_text(json.dumps(note,ensure_ascii=False,indent=2)+'\n')
print('validated',len(revised['decisions']),'changed',len(diff),'statuses',note['status_counts'],'pending',note['unresolved_ordinals'])
