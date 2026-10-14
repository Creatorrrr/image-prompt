"""Preserve395 further explicitly reported direct drafts; confer no approval."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('checkpoint10_primitives',HERE/'verify_manual_draft_checkpoints_10_R02.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);h=old.helpers
seen=set()
for num in ['01','02','03','04-R02','05','06','07','08','09','10']:
 v=json.loads((HERE/f'ROOT-MANUAL-DRAFT-CHECKPOINT-{num}.json').read_bytes())
 for row in v['coverage']:
  s=set(range(*row['range']));assert not seen&s;seen|=s
assert len(seen)==6320
specifications=[
 ('/root/review_12250_13000',r'native_12250_09250_10250\.(\d{5})_(\d{5})\.json',9355,9425),
 ('/root/review_05250_06250',r'native_05250_05250_06250\.(\d{5})_(\d{5})\.json',6000,6050),
 ('/root/review_08250_09250',r'native-08250-(\d{5})-(\d{5})(?:-checkpoint)?\.json',6795,6845),
 ('/root/review_07250_08250',r'native-07250-(\d{5})-(\d{5})\.json',7450,7505),
 ('/root/review_06250_07250',r'native_06250_08250_09250\.(\d{5})_(\d{5})\.json',8625,8750),
 ('/root/review_11870_12250',r'native-11870-(\d{5})-(\d{5})-(?:146v5|149v6)-v1\.json',1565,1610)]
coverage=[];added=set()
for task,pattern,start,stop in specifications:
 local=set();notes=[];boundaries=[]
 for note in sorted(h.NOTES.iterdir()):
  m=re.fullmatch(pattern,note.name)
  if not m:continue
  a,b=map(int,m.groups())
  if task=='/root/review_12250_13000' and note.name in {'native_12250_09250_10250.09350_09355.json','native_12250_09250_10250.09350_09375.json'}:continue
  if not (a<stop and b>start and b<=stop and (a>=start or (a,b,start)==(9350,9400,9355))):continue
  interval=set(range(max(a,start),min(b,stop)));assert not local&interval;local|=interval
  v=json.loads(note.read_bytes());h.add(note)
  if task=='/root/review_12250_13000':
   for row in v['artifacts']:
    assert set(row) in [{'path','sha256'},{'path','raw_sha256'}]
    h.add(h.rootpath(row['path']),row.get('raw_sha256',row.get('sha256')))
   old.pin_nested_artifacts(v)
  elif task in {'/root/review_06250_07250','/root/review_11870_12250'}:old.pin_nested_artifacts(v)
  elif task=='/root/review_08250_09250' and v.get('artifacts'):
   for name,row in v['artifacts'].items():h.add(h.rootpath(name),row['raw_sha256'])
  else:old.previous.pin_note(note,task)
  notes.append(str(note.relative_to(ROOT)));boundaries.append({'note_range':[a,b],'counted_range':[max(a,start),min(b,stop)]})
 assert local==set(range(start,stop)),(task,start,stop,sorted(set(range(start,stop))-local))
 assert not (seen|added)&local;added|=local
 coverage.append({'task':task,'range':[start,stop],'worker_attested_unique_source_reads':len(local),'notes':notes,'exact_count_boundaries':boundaries})
assert len(added)==395 and len(seen|added)==6715
h.add(Path(__file__));h.add(HERE/'verify_manual_draft_checkpoints_11.py');h.add(HERE/'ROOT-MANUAL-DRAFT-CHECKPOINT-11-FAILED-ATTEMPT-01.json')
report={'schema':'photo-root-manual-draft-checkpoint-verification/v1','actor':'/root','previous_checkpoint':'ROOT-MANUAL-DRAFT-CHECKPOINT-10.json','previous_disjoint_draft_candidates':6320,'coverage':coverage,'worker_attested_additional_unique_source_reads':395,'cumulative_disjoint_native_draft_candidates':6715,'files':dict(sorted(h.paths.items())),'all_pinned_raw_hashes_verified':True,'json_and_python_ast_valid':True,'historical_ranges_exactly_disjoint':True,'root_all_sources_personally_read_claimed':False,'source_corrections_or_new_role_decisions_accepted':False,'formal_native_proof_count_for_these_draft_ranges':0,'operational_native_qualified_count':0,'canonical_changed':False,'fresh06250_read_boundary':'125 actual source/current/exact5B/ownbindings/wholeclosure and wholecurrent5Bafter reads with manual drafts; new proposed source-after reads0, formal0.','catalog_boundary':'Each note retains exact144/146/149 research input and actual prior-reading provenance. New149 approval neither re-signs earlier proof nor converts statuses.','known_unapproved_boundaries':['9350:9400 aggregate includes five already counted9350:9355; only45 new9355:9400 are counted here. Earlier partial5/25 are not separately counted.','New prepared inputs and partial worker buffers are not counted.','Source alias-only misclassification corrections, translations, effects, actual owners and qualifiers remain pending unless separately approved.','Hashes, read counts and fixture checks never certify semantic truth or final native operation.'],'gemini_calls':0,'network_calls':0}
out=HERE/'ROOT-MANUAL-DRAFT-CHECKPOINT-11.json'
with out.open('x')as f:json.dump(report,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT).strip();names=sorted(set(h.paths)|{str(out.relative_to(ROOT))});subprocess.run(['git','add','--',*names],cwd=ROOT,check=True);subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
for name in names:assert subprocess.check_output(['git','show',':'+name],cwd=ROOT)==(ROOT/name).read_bytes(),name
print(json.dumps({'files':len(names),'additional_direct_drafts':395,'cumulative':6715,'native_approvals':0}))
