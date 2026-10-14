"""Preserve685 disjoint delegated direct-review drafts without native approval."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('checkpoint10_helpers',HERE/'verify_manual_draft_checkpoints_10_R02.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);h=old.helpers
seen=set()
for number in ['01','02','03','04-R02','05','06','07','08','09','10','11','12','13','14','15']:
 for row in json.loads((HERE/f'ROOT-MANUAL-DRAFT-CHECKPOINT-{number}.json').read_bytes())['coverage']:
  interval=set(range(*row['range']));assert not seen&interval;seen|=interval
assert len(seen)==9000
specifications=[
 ('/root/review_12250_13000',r'native_12250_09250_10250\.(\d{5})_(\d{5})\.json',9750,9850),
 ('/root/review_08250_09250',r'native-08250-(\d{5})-(\d{5})(?:-checkpoint)?\.json',7120,7250),
 ('/root/review_07250_08250',r'native-07250-(\d{5})-(\d{5})\.json',7750,7835),
 ('/root/native_evidence',r'native_extra_10250_11250\.(\d{5})_(\d{5})\.json',10625,10825),
 ('/root/review_09250_10500',r'native_extra_11250_12250\.(\d{5})_(\d{5})\.json',11400,11500),
 ('/root/review_11870_12250',r'native-11870-(\d{5})-(\d{5})-149v6-v1\.json',1630,1645),
 ('/root/review_06250_07250',r'native_extra_12250_13250_(\d{5})_(\d{5})\.json',12295,12350),
]
coverage=[];added=set()
for task,pattern,start,stop in specifications:
 available=[]
 for note in sorted(h.NOTES.iterdir()):
  match=re.fullmatch(pattern,note.name)
  if match:
   first,last=map(int,match.groups())
   if start<=first<last<=stop:available.append((first,last,note))
 # Prefer a complete attested aggregate over its overlapping partial notes.
 selected=[];cursor=start
 while cursor<stop:
  choices=[x for x in available if x[0]==cursor];assert choices,(task,cursor)
  first,last,note=max(choices,key=lambda x:x[1]);selected.append((first,last,note));cursor=last
 local=set();notes=[]
 for first,last,note in selected:
  interval=set(range(first,last));assert not local&interval;local|=interval
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
   h.add(HERE/checkpoint['packet_file'],checkpoint['packet_sha256']);components=set()
   for item in checkpoint['components']:
    ints=set(range(*item['range']));assert not components&ints;components|=ints
    h.add(HERE/item['file'],item['sha256']);h.add(h.rootpath(item['literal_file']),item['literal_sha256'])
    reread=HERE/item['reread_note'];h.add(reread);old.pin_nested_artifacts(json.loads(reread.read_bytes()))
   assert components==set(range(first,last))
   for name in checkpoint['precision_supplements']:h.add(HERE/name)
  elif task=='/root/review_08250_09250' and value.get('artifacts'):
   for name,row in value['artifacts'].items():h.add(h.rootpath(name),row['raw_sha256'])
  else:old.previous.pin_note(note,task)
  notes.append(str(note.relative_to(ROOT)))
 assert local==set(range(start,stop)) and not(seen|added)&local
 added|=local;coverage.append(dict(task=task,range=[start,stop],worker_attested_unique_source_reads=len(local),notes=notes))
assert len(added)==685 and len(seen|added)==9685
completion=HERE/'worker-notes/native-08250-06250-07250-completion-20261015-v1.json';h.add(completion,'188382fcfe8ff8f08a883ebc05d662fff1a37758f97c1ae03e38169a7a2ca2eb')
manifest=json.loads(completion.read_bytes());assert manifest['actual_unique_whole_manual_read_count']==manifest['frozen_authored_record_count']==1000 and manifest['complete_native_proof_count']==0
completed=set()
for item in manifest['files']:
 interval=set(range(*item['range']));assert not completed&interval;completed|=interval
 for key in ['authored','note']:h.add(h.rootpath(item[key]),item[key+'_raw_sha256'])
assert completed==set(range(6250,7250)) and completed<=seen|added
plan=ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md';h.paths[str(plan.relative_to(ROOT))]=hashlib.sha256(plan.read_bytes()).hexdigest();h.add(Path(__file__))
protected={'docs/analysis/2026-10-09-spring-fashion-integration-and-native-tests.md':'b3ee189d975790cb5ce29b38e9eaadfc6cff0964a4840cd24c09ec6b96963359','docs/research-evidence/photo-prompt/data-quality-links-20261007/history/README.md':'0856f394a083b760cfe99b5bc0113e0743af00c0ad9846fb904e77858712ee2b'}
for name,pin in protected.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==pin
report=dict(schema='photo-root-manual-draft-checkpoint-verification/v1',actor='/root',previous_checkpoint='ROOT-MANUAL-DRAFT-CHECKPOINT-15.json',previous_disjoint_draft_candidates=9000,coverage=coverage,
 worker_attested_additional_unique_source_reads=685,cumulative_disjoint_native_draft_candidates=9685,files=dict(sorted(h.paths.items())),all_pinned_raw_hashes_verified=True,json_and_python_ast_valid=True,historical_ranges_exactly_disjoint=True,
 root_all_sources_personally_read_claimed=False,source_corrections_or_new_role_decisions_accepted=False,formal_native_proof_count_for_these_draft_ranges=0,operational_native_qualified_count=0,canonical_changed=False,
 completed_worker_range=[6250,7250],completed_worker_native_approvals=0,
 known_unapproved_boundaries=[
  '9750:9800 and9800:9850 complete50 aggregates are each counted once; their contained first25 partial notes are excluded.',
  'The137 authored artifacts for6250:7250 prove attested exact1000 coverage, not1000 native proofs. Their actual earlier catalog/generation bindings stay unchanged. The new13250:14250 preparation is excluded from read counts.',
  '10799 nonexistent role ID was removed during worker after-reread with original literal/initial JSON history retained. Source/proof approval is not conferred by that correction.',
  '11870 failed note-path assertion and corrected freezer remain separate history. The completed5 draft is not counted as a failed extra read or source approval.',
  'Original property addresses/effects and all pending owner/receiver/mode/source5B discrepancies are preserved. Supported draft labels and automatic syntax/hash checks are not final semantic approval.',
  'Separate first20/simple5 native/peer rereviews and diagnostic rechecks overlap bulk and add no duplicate unique source-read credit.',
  'No final149 full-pool hybrid retrieval, actual request/compose/runtime/pixel or all18250 completion is claimed.'
 ],protected_files=protected,gemini_calls=0,network_calls=0)
out=HERE/'ROOT-MANUAL-DRAFT-CHECKPOINT-16.json'
with out.open('x')as f:json.dump(report,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
assert not subprocess.check_output(['git','diff','--cached','--name-only']).strip()
names=sorted(set(h.paths)|{str(out.relative_to(ROOT))});subprocess.run(['git','add','--',*names],check=True);expected=set()
for name in names:
 previous=subprocess.run(['git','show','HEAD:'+name],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
 if previous.returncode or previous.stdout!=(ROOT/name).read_bytes():expected.add(name)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==expected
subprocess.run(['git','diff','--cached','--check'],check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name])==(ROOT/name).read_bytes()
print(json.dumps(dict(pinned_files=len(names),cached_files=len(expected),additional_direct_drafts=685,cumulative=9685,native_approvals=0,operating_changes=0)))
