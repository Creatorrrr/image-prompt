"""Persist explicit reviewer decisions; never infer a verdict from data flags."""
import json,sys
from pathlib import Path
R=Path(__file__).parent
sample={r['sample_number']:r for r in map(json.loads,(R/'samples.jsonl').read_text().splitlines())}
M={'C':'clear','G':'weak','D':'distorted','Q':'uncertain'};T={'A':'appropriate','B':'broad','W':'wrong','U':'unassigned'};L={'C':'consistent','M':'missing_ko','D':'mismatch','N':'not_applicable','Q':'uncertain'}
rows=[]
for line in sys.stdin.read().strip().splitlines():
 if not line.strip():continue
 i,m,t,l,flags,expected,reason=line.split('|',6);i=int(i);source=sample[i]
 assert (t=='U')==(not bool(source['bindings'])),i
 rows.append({'sample_number':i,'candidate_id':source['candidate']['id'],'record_kind':source['candidate']['record_kind'],'record_sha256':source['record_sha256'],'meaning':M[m],'translation':L[l],'slot':T[t],'assigned_slots':[b['slot_id'] for b in source['bindings']],'suggested_semantic_slots':[] if expected=='-' else expected.split(','),'flags':[] if flags=='-' else flags.split(','),'reason':reason.strip(),'review_method':'Codex qualitative semantic reading; compact card plus selected deep source checks'})
assert len(rows)==len({r['sample_number'] for r in rows})
path=R/'reviews'/f'{min(r["sample_number"] for r in rows):04d}-{max(r["sample_number"] for r in rows):04d}.json'
assert not path.exists(),path
path.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print({'saved':len(rows),'range':[min(r['sample_number'] for r in rows),max(r['sample_number'] for r in rows)],'meaning':{k:sum(r['meaning']==k for r in rows) for k in M.values()}})
