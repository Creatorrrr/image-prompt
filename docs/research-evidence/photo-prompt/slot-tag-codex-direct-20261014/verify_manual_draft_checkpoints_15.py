"""Preserve500 additional disjoint delegated drafts; no semantic approval."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('checkpoint10_helpers',HERE/'verify_manual_draft_checkpoints_10_R02.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);h=old.helpers
seen=set()
for number in ['01','02','03','04-R02','05','06','07','08','09','10','11','12','13','14']:
 for row in json.loads((HERE/f'ROOT-MANUAL-DRAFT-CHECKPOINT-{number}.json').read_bytes())['coverage']:
  interval=set(range(*row['range']));assert not seen&interval;seen|=interval
assert len(seen)==8500
specifications=[
 ('/root/review_12250_13000',r'native_12250_09250_10250\.(\d{5})_(\d{5})\.json',9675,9750),
 ('/root/review_08250_09250',r'native-08250-(\d{5})-(\d{5})(?:-checkpoint)?\.json',7040,7120),
 ('/root/review_07250_08250',r'native-07250-(\d{5})-(\d{5})\.json',7690,7750),
 ('/root/native_evidence',r'native_extra_10250_11250\.(\d{5})_(\d{5})\.json',10500,10625),
 ('/root/review_09250_10500',r'native_extra_11250_12250\.(\d{5})_(\d{5})\.json',11300,11400),
 ('/root/review_11870_12250',r'native-11870-(\d{5})-(\d{5})-149v6-v1\.json',1615,1630),
 ('/root/review_06250_07250',r'native_extra_12250_13250_(\d{5})_(\d{5})\.json',12250,12295),
]
coverage=[];added=set()
for task,pattern,start,stop in specifications:
 local=set();notes=[];boundaries=[]
 for note in sorted(h.NOTES.iterdir()):
  match=re.fullmatch(pattern,note.name)
  if not match:continue
  first,last=map(int,match.groups())
  if task=='/root/review_12250_13000' and (first,last)==(9700,9725):continue
  trimmed=task=='/root/review_12250_13000' and (first,last)==(9650,9700)
  if not(first<stop and last>start and last<=stop and(first>=start or trimmed)):continue
  interval=set(range(max(first,start),min(last,stop)));assert not local&interval,(task,note.name);local|=interval
  value=json.loads(note.read_bytes());h.add(note)
  if task=='/root/review_12250_13000':
   for row in value['artifacts']:h.add(h.rootpath(row['path']),row.get('raw_sha256',row.get('sha256')))
   old.pin_nested_artifacts(value)
  elif task=='/root/review_06250_07250':
   assert value['complete_source_read'] and value['actual_current_whole_after_read_count']==last-first and value['formal_native_count']==0
   for name,item in value['file_pins'].items():h.add(h.rootpath(name),item['raw_sha256'])
   old.pin_nested_artifacts(value)
  elif task in {'/root/native_evidence','/root/review_11870_12250'}:old.pin_nested_artifacts(value)
  elif task=='/root/review_09250_10500':
   counts=value['counts'];assert all(counts[k]==50 for k in ['whole_original_exact5B_current','ownbindings','wholeafter']) and counts['native_qualified']==counts['source_accepted']==0
   p=HERE/value['checkpoint_file'];h.add(p,value['checkpoint_sha256']);checkpoint=json.loads(p.read_bytes())
   assert checkpoint['actual_whole_original_exact5B_current_read_count']==checkpoint['actual_own_binding_read_count']==checkpoint['actual_whole_proposed_after_read_count']==50
   h.add(HERE/checkpoint['packet_file'],checkpoint['packet_sha256']);component_seen=set()
   for component in checkpoint['components']:
    ints=set(range(*component['range']));assert not component_seen&ints;component_seen|=ints
    h.add(HERE/component['file'],component['sha256']);h.add(h.rootpath(component['literal_file']),component['literal_sha256'])
    reread=HERE/component['reread_note'];h.add(reread);old.pin_nested_artifacts(json.loads(reread.read_bytes()))
   assert component_seen==set(range(first,last))
   for name in checkpoint['precision_supplements']:h.add(HERE/name)
  elif task=='/root/review_08250_09250' and value.get('artifacts'):
   for name,row in value['artifacts'].items():h.add(h.rootpath(name),row['raw_sha256'])
  else:old.previous.pin_note(note,task)
  notes.append(str(note.relative_to(ROOT)));boundaries.append(dict(note_range=[first,last],counted_range=[max(first,start),min(last,stop)]))
 assert local==set(range(start,stop)),(task,sorted(set(range(start,stop))-local))
 assert not(seen|added)&local;added|=local
 coverage.append(dict(task=task,range=[start,stop],worker_attested_unique_source_reads=len(local),notes=notes,exact_count_boundaries=boundaries))
assert len(added)==500 and len(seen|added)==9000
supplements=[
 'worker-notes/native_extra_12250_13250_12254.literal-r02.json',
 'worker-notes/native_extra_12250_13250_parent-context-read01.json',
 'worker-notes/native_extra_11250_12250.catalog149-count-correction-001.json',
 'worker-notes/native_extra_11250_12250.catalog149-count-correction-002.json',
]
for name in supplements:
 p=HERE/name;h.add(p);old.pin_nested_artifacts(json.loads(p.read_bytes()))
plan=ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md';h.paths[str(plan.relative_to(ROOT))]=hashlib.sha256(plan.read_bytes()).hexdigest();h.add(Path(__file__))
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name,digest in protected.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
report=dict(schema='photo-root-manual-draft-checkpoint-verification/v1',actor='/root',previous_checkpoint='ROOT-MANUAL-DRAFT-CHECKPOINT-14.json',previous_disjoint_draft_candidates=8500,coverage=coverage,
 worker_attested_additional_unique_source_reads=500,cumulative_disjoint_native_draft_candidates=9000,files=dict(sorted(h.paths.items())),preserved_issue_queue_supplements=supplements,
 all_pinned_raw_hashes_verified=True,json_and_python_ast_valid=True,historical_ranges_exactly_disjoint=True,root_all_sources_personally_read_claimed=False,
 source_corrections_or_new_role_decisions_accepted=False,formal_native_proof_count_for_these_draft_ranges=0,operational_native_qualified_count=0,canonical_changed=False,
 new12250_boundary='45 whole original/current/exact5B/ownbinding/required closure and unchanged current-after reads with manual drafts. Prepared1000 is not actual1000. Only the45 exact frozen rows are counted; direct diagnostic overlap has no additional native approval credit.',
 catalog_boundary='Every note retains its actual source/container/catalog/fullspec read boundary. Readonly preparations and numeric corrections confer no meaning approval or catalog conversion.',
 known_unapproved_boundaries=[
 '9650:9700 aggregate contributes only9675:9700; its already counted9650:9675 remains excluded.9700:9750 aggregate is counted once, not its9700:9725 partial.',
 'The two complete50 management batches11300:11400 are counted once each, not again per component. Their native counts remain0. Catalog88 count is corrected to86 by immutable correction002; correction001 is explicitly superseded.',
 'Actual noncontact gap11341 remains a catalog-boundary HOLD. No contact-point tag is inferred from the old prefix. All exact original properties/owners/receivers and source/5B disagreements remain pending.',
 '12267/12268 actual retains/remains clauses versus original canonical color effects remain unresolved rather than converted to E0. The old/current mismatch and grammar/translation fixes require separate source choices.',
 'Wholeafter equality factoring reuses an actually read exact complete current source; it does not mean a new edited after or new native proof. Unfinished reads and live buffers are excluded.',
 'Separate root/peer diagnostic70 rereads and native first20/first50 rechecks are not added to these unique bulk draft counts. Root does not claim all delegated source reading personally.',
 'Hash, syntax, source shape, preparation and partial-fact counts do not prove semantic accuracy, native admission, operating tags, full149 retrieval or pixels.'
 ],protected_files=protected,gemini_calls=0,network_calls=0)
out=HERE/'ROOT-MANUAL-DRAFT-CHECKPOINT-15.json';assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
with out.open('x') as f:json.dump(report,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
names=sorted(set(h.paths)|{str(out.relative_to(ROOT))});subprocess.run(['git','add','--',*names],cwd=ROOT,check=True);subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines())<=set(names)
for name in names:assert subprocess.check_output(['git','show',':'+name],cwd=ROOT)==(ROOT/name).read_bytes(),name
print(json.dumps(dict(files=len(names),additional_direct_drafts=500,cumulative=9000,native_approvals=0)))
