from pathlib import Path
import json,subprocess,sys
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(p.read_bytes());write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
request=(O/'request.txt').read_text(); spans=read(O/'spans.json'); rows=[]
for span in spans:
 text=request[span['start']:span['end']]
 if span['span_id']=='reference':
  rows.append({**span,'text':text,'purpose':'reference_use','reason':'Reuse the same face/hair reference; transport and scope are not candidate topic terms.'})
 else:
  bounds=[(span['start'],3,'topic_reference','Exact anaphor links the prior user mecha topic without importing old staging.'),(3,request.index('좌우 반전'),'workflow','Candidate exposure and overbound writing conditions describe workflow defects, not scene objects.'),(request.index('좌우 반전'),span['end'],'visual','Retain explicit visible side, connection and contact-occlusion repair requirements in discovery.')]
  rows.extend({'span_id':span['span_id'],'start':a,'end':b,'text':request[a:b],'purpose':purpose,'reason':reason} for a,b,purpose,reason in bounds)
scope={'contract_version':'photo-request-query-scope/v1','segments':[{**{k:v for k,v in row.items() if k!='span_id'},'active_span_id':row['span_id']} for row in rows]}
write(O/'query-scope.json',scope)
for arm in 'abc':
 run=R/'generated/photo-runs'/('mecha-20261024-repair2-scoped-'+arm)
 cli=str(S/'precore/prepare_photo_run.py')
 cmd=[sys.executable,cli,'init','--run',str(run),'--request',str(O/'request.txt'),'--spans',str(O/'spans.json'),'--input-inventory',str(O/'inputs.json'),'--topic-context',str(O/'topic-context.json'),'--query-scope',str(O/'query-scope.json'),'--mode','image']
 subprocess.run(cmd,check=True)
 subprocess.run([sys.executable,cli,'controls','--run',str(run),'--context',str(R/'generated/photo-runs/mecha-20261024-repair2-a/creative_context.input.json')],check=True)
 w=read(run/'workflow.json');args=read(O/('retry-'+arm)/'args.json')
 args['decision']=str(O/('retry-'+arm)/'decision-v2.json');args['current_envelope']=w['artifacts']['request_envelope_input']['path'];args['output']=str(O/('retry-'+arm)/'projection-scoped')
 write(O/('retry-'+arm)/'args-scoped.json',args)
 print(arm,run,flush=True)
