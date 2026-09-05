"""Preserve only one current case helper final from this case's exact session."""
import json,hashlib,sys
from pathlib import Path
session=Path('/Users/chasoik/.codex/sessions/2026/09/05/rollout-2026-09-05T23-05-13-01a071e3-3cc7-7c60-bd5e-5d0f19160672.jsonl')
name=sys.argv[1]; assert name in ['global_lane','spatial_lane','appearance_lane','color_lane','capture_lane','critic']
sender='/root/case_02_run/'+name
matches=[];started=[]
for line in session.open():
 o=json.loads(line);p=o.get('payload',{})
 if o.get('type')=='response_item':
  if 'spawn_agent' in str(p.get('name','')):
   try:a=json.loads(p.get('arguments',p.get('input','{}')))
   except (ValueError,TypeError):a={}
   if a.get('task_name')==name:started.append(o.get('timestamp'))
  for c in p.get('content',[]) if isinstance(p.get('content'),list) else []:
   if isinstance(c,dict) and isinstance(c.get('text'),str):
    s=c['text'];head=f'Message Type: FINAL_ANSWER\nTask name: /root/case_02_run\nSender: {sender}\nPayload:\n'
    if s.startswith(head):matches.append((o.get('timestamp'),s[len(head):]))
assert len(matches)==1,(name,len(matches))
time,raw=matches[0];parsed=json.loads(raw)
out=Path('output')
rawpath=out/(name+'.report.raw.json');rawpath.write_text(raw)
(out/(name+'.report.json')).write_text(json.dumps(parsed,ensure_ascii=False,indent=2)+'\n')
meta={'sender':sender,'case_session_id':'01a071e3-3cc7-7c60-bd5e-5d0f19160672','source':'exact current case session final payload only','spawn_utc':started,'received_utc':time,'report_raw_sha256':hashlib.sha256(raw.encode()).hexdigest(),'report_raw_bytes':len(raw.encode()),'normalized_report_sha256':hashlib.sha256((out/(name+'.report.json')).read_bytes()).hexdigest(),'normalization':'JSON pretty-print only; raw payload preserved separately'}
(out/(name+'.report-provenance.json')).write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps(meta))
