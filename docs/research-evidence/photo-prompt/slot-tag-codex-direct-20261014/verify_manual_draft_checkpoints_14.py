"""Preserve 500 additional exact disjoint worker-read drafts; confer no native qualification."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('checkpoint10_helpers',HERE/'verify_manual_draft_checkpoints_10_R02.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);h=old.helpers
seen=set()
for number in ['01','02','03','04-R02','05','06','07','08','09','10','11','12','13']:
 report=json.loads((HERE/f'ROOT-MANUAL-DRAFT-CHECKPOINT-{number}.json').read_bytes())
 for row in report['coverage']:
  interval=set(range(*row['range']));assert not seen&interval;seen|=interval
assert len(seen)==8000
specifications=[
 ('/root/review_12250_13000',r'native_12250_09250_10250\.(\d{5})_(\d{5})\.json',9600,9675),
 ('/root/review_08250_09250',r'native-08250-(\d{5})-(\d{5})(?:-checkpoint)?\.json',6980,7040),
 ('/root/review_07250_08250',r'native-07250-(\d{5})-(\d{5})\.json',7630,7690),
 ('/root/review_06250_07250',r'native_06250_08250_09250\.(\d{5})_(\d{5})\.json',9150,9250),
 ('/root/native_evidence',r'native_extra_10250_11250\.(\d{5})_(\d{5})\.json',10350,10500),
 ('/root/review_09250_10500',r'native_extra_11250_12250\.(\d{5})_(\d{5})\.json',11250,11300),
 ('/root/review_11870_12250',r'native-11870-(\d{5})-(\d{5})-149v6-v1\.json',1610,1615),
]
coverage=[];added=set()
for task,pattern,start,stop in specifications:
 local=set();notes=[];boundaries=[]
 for note in sorted(h.NOTES.iterdir()):
  match=re.fullmatch(pattern,note.name)
  if not match:continue
  first,last=map(int,match.groups())
  if task=='/root/review_12250_13000' and (first,last)==(9600,9625):continue
  trimmed=False
  if not(first<stop and last>start and last<=stop and(first>=start or trimmed)):continue
  interval=set(range(max(first,start),min(last,stop)));assert not local&interval,(task,note.name);local|=interval
  value=json.loads(note.read_bytes());h.add(note)
  if task=='/root/review_12250_13000':
   for row in value['artifacts']:
    assert set(row)in[{'path','sha256'},{'path','raw_sha256'}]
    h.add(h.rootpath(row['path']),row.get('raw_sha256',row.get('sha256')))
   old.pin_nested_artifacts(value)
  elif task in {'/root/review_06250_07250','/root/native_evidence','/root/review_11870_12250'}:old.pin_nested_artifacts(value)
  elif task=='/root/review_09250_10500':
   assert value['actual_whole_original_exact5B_current_read_count']==50 and value['actual_own_binding_read_count']==50 and value['actual_whole_proposed_after_reread_count']==50
   assert value['management_batch_complete'] and value['native_qualified_count']==0
   h.add(HERE/value['checkpoint_file'],value['checkpoint_raw_sha256'])
   for component in value['component_files']:
    for label in ['draft','literal','reread_note']:h.add(HERE/component[label],component[label+'_sha256'])
   for label in ['packet','catalog_read_note','effect_address_hold_note']:
    item=value[label];h.add(HERE/item['path'],item['raw_sha256'])
   for item in value['supplements']:h.add(HERE/item['file'],item['raw_sha256'])
  elif task=='/root/review_08250_09250' and value.get('artifacts'):
   for name,row in value['artifacts'].items():h.add(h.rootpath(name),row['raw_sha256'])
  else:old.previous.pin_note(note,task)
  notes.append(str(note.relative_to(ROOT)));boundaries.append({'note_range':[first,last],'counted_range':[max(first,start),min(last,stop)]})
 assert local==set(range(start,stop)),(task,sorted(set(range(start,stop))-local))
 assert not(seen|added)&local;added|=local
 coverage.append({'task':task,'range':[start,stop],'worker_attested_unique_source_reads':len(local),'notes':notes,'exact_count_boundaries':boundaries})
assert len(added)==500 and len(seen|added)==8500
supplements=[
 'worker-notes/native_06250_08250_09250.final-1000-01.json',
 'authored/native_06250_08250_09250.property-lock-issuequeue-01.json',
 'authored/native_05250_05250_06250.simple-formal-readiness-149-v1.json',
 'worker-notes/native_05250_05250_06250.original-property-lock-issuequeue-20261015-v1.json',
]
for relative in supplements:h.add(HERE/relative)
plan=ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md'
h.paths[str(plan.relative_to(ROOT))]=hashlib.sha256(plan.read_bytes()).hexdigest();h.add(Path(__file__))
report={'schema':'photo-root-manual-draft-checkpoint-verification/v1','actor':'/root',
 'previous_checkpoint':'ROOT-MANUAL-DRAFT-CHECKPOINT-13.json','previous_disjoint_draft_candidates':8000,'coverage':coverage,
 'worker_attested_additional_unique_source_reads':500,'cumulative_disjoint_native_draft_candidates':8500,
 'files':dict(sorted(h.paths.items())),'preserved_issue_queue_supplements':supplements,
 'all_pinned_raw_hashes_verified':True,'json_and_python_ast_valid':True,'historical_ranges_exactly_disjoint':True,
 'root_all_sources_personally_read_claimed':False,'source_corrections_or_new_role_decisions_accepted':False,
 'formal_native_proof_count_for_these_draft_ranges':0,'operational_native_qualified_count':0,'canonical_changed':False,
 'fresh06250_read_boundary':'100 whole original/current/exact5B/own-binding/closure and current5B-after direct reads with manual drafts; new authored source-after reads0, formal0.',
 'fresh_native_evidence_boundary':'150 actual whole original/current/5B/ownbinding/closure/provenance and unchanged source-copy after rereads with manual pending meaning drafts. Preparation1000 is not1000 actual reads. Three early source-only formal suggestions are separately HOLD for exact original property/owner lock review.',
 'catalog_boundary':'Each note retains its exact earlier source-container catalog and149 review input, fullspec reading and actual provenance. No automatic catalog/source/proof hash or status conversion.',
 'known_unapproved_boundaries':[
  '9600:9625 partial is not added twice to9600:9650 aggregate;9650:9675 is used, later9650:9700 aggregate is excluded for this fixed interval.',
  'New11250:11300 complete50checkpoint is counted once, not its four-record author/reread subchunks. It contains pending old/current5B11295 branch-contact disagreement and first16 effect-address HOLDs.',
  'Actual source-after rereading includes unchanged source copies or exactcurrent5B copies where explicitly attested. It does not imply newly edited source, approved role tags or actual native qualification.',
  'Prepared1000 inputs, only-read1615:1620, new12250:13250 preparation and currentworking buffers are excluded. Diagnostic70 separate root/peer rereads and first50/first20 native rechecks are not added to unique bulk draft counts.',
  'Every historical catalog/source/proof hash and pending actual original-property/owner/receiver/translation/source-coverage issue remains; no prefix rename or automatic proof conversion is authorized.',
  'Footwear catalog, first20 source alternatives, lower-lash application and incomplete1299 visibility/framing scopes remain unapproved by this draft checkpoint.',
  'Root does not claim personal reading of all delegated sources. Hashes, literal quotes, syntax, source shape and prepared counts do not certify final meaning, native admission or operating tags.',
 ],'gemini_calls':0,'network_calls':0}
out=HERE/'ROOT-MANUAL-DRAFT-CHECKPOINT-14.json'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip()
with out.open('x')as stream:json.dump(report,stream,ensure_ascii=False,sort_keys=True,indent=2);stream.write('\n')
names=sorted(set(h.paths)|{str(out.relative_to(ROOT))});subprocess.run(['git','add','--',*names],cwd=ROOT,check=True)
subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines())<=set(names)
for name in names:assert subprocess.check_output(['git','show',':'+name],cwd=ROOT)==(ROOT/name).read_bytes(),name
print(json.dumps({'files':len(names),'additional_direct_drafts':500,'cumulative':8500,'native_approvals':0}))
