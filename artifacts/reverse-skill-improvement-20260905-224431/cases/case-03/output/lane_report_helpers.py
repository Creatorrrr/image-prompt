from pathlib import Path
import json,datetime,hashlib
OUT=Path(__file__).resolve().parent
ROUTE=json.loads((OUT/'route.json').read_text())
SOURCE={'sha256':'a3e2b2dcf5d8aa7b8d78e564452f48c60e579db1282e090bd3dcaa9015e83aa9','frame':'969x1280'}
def new(lane):
 route=next(x for x in ROUTE['lanes'] if x['id']==lane)
 profile=json.loads((OUT/(lane+'.profile.json')).read_text())
 versions=[]
 for f in profile['files'][1:]:
  lines=f['content'].splitlines();versions.append({'id':next(x.split(':',1)[1].strip() for x in lines if x.startswith('id:')),'version':int(next(x.split(':',1)[1].strip() for x in lines if x.startswith('version:')))})
 return {'schema_version':'reverse-image-analysis-lane-report/v2','lane_id':lane,'route_fingerprint':ROUTE['route_fingerprint'],'source_artifact':SOURCE,'execution':{'mode':'sequential-fallback','independent_context':False,'context_note':'Coordinator context; prior lane report and draft remain in context. No independence claimed.'},'status':'complete','reviewed_modules':versions,'topic_dispositions':[],'findings':[],'control_requirements':[],'omission_checks':[],'handoffs':[],'conflicts':[]}
def finding(report,key,axis,obs,origin,obligations,role='primary',priority='P1',confidence='high',confounders=None):
 id=report['lane_id']+':'+key
 f={'id':id,'owner_key':key,'scale':'regional','axis':axis,'observation':obs,'source_evidence':[obs],'confidence':confidence,'causal_origin':origin,'materiality':'material','proposed_role':role,'default_drift_risk':'high','priority':priority,'confounders':confounders or [],'atomic_obligations':[]}
 for suffix,ax,res,regions,relation in obligations:
  f['atomic_obligations'].append({'id':id+':'+suffix,'axis':ax,'visible_result':res,'result_direction':res,'subject_or_region_ids':regions,'relation_kind':relation,'source_evidence':[res],'confidence':confidence,'causal_origin':origin,'attribution_status':'confounded' if confounders else 'resolved','materiality':'material','proposed_role':role,'target_strength':'strong' if priority=='P0' else 'moderate','confounders':confounders or []})
 report['findings'].append(f);return id

def topic(report,name,ids,disposition='analyzed',reason=None):
 d={'topic':name,'disposition':disposition,'finding_ids':ids}
 if reason:d['reason']=reason
 report['topic_dispositions'].append(d)
def save(report,started):
 p=OUT/(report['lane_id']+'.report.json');p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 event={'event':'sequential-lane-frozen','lane_id':report['lane_id'],'started_at':started,'ended_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'independent_context':False}
 with (OUT/'events.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
 print(event)
