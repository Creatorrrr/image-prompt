"""Preserve 600 additional exact disjoint worker-read drafts; confer no native qualification."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('checkpoint10_helpers',HERE/'verify_manual_draft_checkpoints_10_R02.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);h=old.helpers
seen=set()
for number in ['01','02','03','04-R02','05','06','07','08','09','10','11','12']:
 report=json.loads((HERE/f'ROOT-MANUAL-DRAFT-CHECKPOINT-{number}.json').read_bytes())
 for row in report['coverage']:
  interval=set(range(*row['range']));assert not seen&interval;seen|=interval
assert len(seen)==7400
specifications=[
 ('/root/review_12250_13000',r'native_12250_09250_10250\.(\d{5})_(\d{5})\.json',9525,9600),
 ('/root/review_05250_06250',r'native_05250_05250_06250\.(\d{5})_(\d{5})\.json',6150,6250),
 ('/root/review_08250_09250',r'native-08250-(\d{5})-(\d{5})(?:-checkpoint)?\.json',6915,6980),
 ('/root/review_07250_08250',r'native-07250-(\d{5})-(\d{5})\.json',7570,7630),
 ('/root/review_06250_07250',r'native_06250_08250_09250\.(\d{5})_(\d{5})\.json',8950,9150),
 ('/root/native_evidence',r'native_extra_10250_11250\.(\d{5})_(\d{5})\.json',10250,10350),
]
coverage=[];added=set()
for task,pattern,start,stop in specifications:
 local=set();notes=[];boundaries=[]
 for note in sorted(h.NOTES.iterdir()):
  match=re.fullmatch(pattern,note.name)
  if not match:continue
  first,last=map(int,match.groups())
  if task=='/root/review_12250_13000' and (first,last)==(9550,9575):continue
  trimmed=task=='/root/review_12250_13000' and (first,last,start)==(9500,9550,9525)
  if not(first<stop and last>start and last<=stop and(first>=start or trimmed)):continue
  interval=set(range(max(first,start),min(last,stop)));assert not local&interval,(task,note.name);local|=interval
  value=json.loads(note.read_bytes());h.add(note)
  if task=='/root/review_12250_13000':
   for row in value['artifacts']:
    assert set(row)in[{'path','sha256'},{'path','raw_sha256'}]
    h.add(h.rootpath(row['path']),row.get('raw_sha256',row.get('sha256')))
   old.pin_nested_artifacts(value)
  elif task in {'/root/review_06250_07250','/root/native_evidence'}:old.pin_nested_artifacts(value)
  elif task=='/root/review_08250_09250' and value.get('artifacts'):
   for name,row in value['artifacts'].items():h.add(h.rootpath(name),row['raw_sha256'])
  else:old.previous.pin_note(note,task)
  notes.append(str(note.relative_to(ROOT)));boundaries.append({'note_range':[first,last],'counted_range':[max(first,start),min(last,stop)]})
 assert local==set(range(start,stop)),(task,sorted(set(range(start,stop))-local))
 assert not(seen|added)&local;added|=local
 coverage.append({'task':task,'range':[start,stop],'worker_attested_unique_source_reads':len(local),'notes':notes,'exact_count_boundaries':boundaries})
assert len(added)==600 and len(seen|added)==8000
supplements=[
 'worker-notes/native-08250-original-property-lock-issuequeue-20261015-v1.json',
 'worker-notes/native_extra_10250_11250.exact-property-lock-HOLD-01.json',
 'worker-notes/native_12250_original_effect_lock_issuequeue_09250_09575_20261015.json',
 'worker-notes/native_extra_11250_12250.effect-address-HOLD-001.json',
 'worker-notes/native-07250-07597-field-anchor-revision-01.json',
 'ROOT-MANUAL-DRAFT-CHECKPOINT-13-CREATION-FAILED-ATTEMPT-01.json',
]
for relative in supplements:h.add(HERE/relative)
plan=ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'
h.paths[str(plan.relative_to(ROOT))]=hashlib.sha256(plan.read_bytes()).hexdigest();h.add(Path(__file__))
report={'schema':'photo-root-manual-draft-checkpoint-verification/v1','actor':'/root',
 'previous_checkpoint':'ROOT-MANUAL-DRAFT-CHECKPOINT-12.json','previous_disjoint_draft_candidates':7400,'coverage':coverage,
 'worker_attested_additional_unique_source_reads':600,'cumulative_disjoint_native_draft_candidates':8000,
 'files':dict(sorted(h.paths.items())),'preserved_issue_queue_supplements':supplements,
 'all_pinned_raw_hashes_verified':True,'json_and_python_ast_valid':True,'historical_ranges_exactly_disjoint':True,
 'root_all_sources_personally_read_claimed':False,'source_corrections_or_new_role_decisions_accepted':False,
 'formal_native_proof_count_for_these_draft_ranges':0,'operational_native_qualified_count':0,'canonical_changed':False,
 'fresh06250_read_boundary':'200 whole original/current/exact5B/own-binding/closure and current5B-after direct reads with manual drafts; new authored source-after reads0, formal0.',
 'fresh_native_evidence_boundary':'100 actual whole original/current/5B/ownbinding/closure/provenance and unchanged source-copy after rereads with manual pending meaning drafts. Preparation1000 is not1000 actual reads. Three early source-only formal suggestions are separately HOLD for exact original property/owner lock review.',
 'catalog_boundary':'Each note retains its exact earlier source-container catalog and149 review input, fullspec reading and actual provenance. No automatic catalog/source/proof hash or status conversion.',
 'known_unapproved_boundaries':[
  '9500:9550 aggregate counts only new9525:9550;9550:9575 partial is not added twice to9550:9600 aggregate.',
  'Original property/owner lock preservation is unverified for pending refinement proposals. Source prefix fit cannot authorize a new canonical effect/address. Exact issue queues remain unapproved.',
  '7597 field-local anchor correction is preserved separately; actual decorative-line effects remain in their positive ordinary source fields, not fabricated on a shorter relation-object field.',
  'Current/original versus exact5Bafter translation mismatches and controlled-origin hash mismatches remain explicit pending issues, not silently imported corrections.',
  'Footwear scope proposals and incomplete actual source applications remain unapproved. Existing first50-05 candidate1299 stays pending despite the separately prepared new06 literal.',
  'Prepared inputs, mutable buffers and partial native-proof checkpoints are excluded from these draft counts. Worker reads, syntax, hashes and fixture shapes do not certify final tags or operating qualification.',
 ],'gemini_calls':0,'network_calls':0}
out=HERE/'ROOT-MANUAL-DRAFT-CHECKPOINT-13.json'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
with out.open('x')as stream:json.dump(report,stream,ensure_ascii=False,sort_keys=True,indent=2);stream.write('\n')
names=sorted(set(h.paths)|{str(out.relative_to(ROOT))});subprocess.run(['git','add','--',*names],cwd=ROOT,check=True)
subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines())<=set(names)
for name in names:assert subprocess.check_output(['git','show',':'+name],cwd=ROOT)==(ROOT/name).read_bytes(),name
print(json.dumps({'files':len(names),'additional_direct_drafts':600,'cumulative':8000,'native_approvals':0}))
