"""Offline diagnosis with exact issued query vectors; never resample or alter a run."""
import gc;gc.disable()
from pathlib import Path
import json,sys
O=Path(__file__).resolve().parent;R=Path('/Users/chasoik/Projects/image-prompt');STORE=Path.home()/'.cache/image-prompt/photo-shared-runtime/h-f2-installed'
gid=sys.argv[1];out=Path(sys.argv[2]);m=json.loads((STORE/'h-f2-generations'/gid/'manifest.json').read_bytes());sys.path.insert(0,str(STORE/'generations'/m['native_generation_id']/'scripts'))
from photo_h_f2_generation import Generation
import photo_recall_first as rf
G=Generation(STORE,gid,full=True);idx=G.index();cards=json.loads((O/'semantic-cards.json').read_text());new={c['candidate_id'] for c in cards if c['id'].startswith('R2V')};targets={a:next(c['candidate_id'] for c in cards if c['id']==sid) for a,sid in [('A','R2V01'),('B','R2V13'),('C','R2V15')]};rows=[];arms=[]
for arm,name in [('A','court-palace-20261023-r2-a'),('B','court-palace-20261023-r2-b'),('C','court-palace-20261023-r2-c/corrected-run')]:
 state=json.loads((R/'generated/photo-runs'/name/'workflow.json').read_bytes());p=json.loads(Path(state['artifacts']['h_f2_material']['path']).read_bytes());exposed=set(p['sources'])&new;target=targets[arm];armrows=[]
 for q,info in p['query_set']['slots'].items():
  e=p['queries'][q]['row'];rf.check_embedding(e,G.binding,info['text'],'query');res=idx.search(info['text'],e,G.binding);assert res['lane_calls']=={'BM25F':1,'local_cosine':1};order=res['order'];rank=next((i+1 for i,r in enumerate(order) if r['cid']==target),None);sampled={c['cid'] for c in p['goals'][q]['candidates']};row={'arm':arm,'query_id':q,'query':info['text'],'target_CID':target,'target_rank_in_probe':rank,'target_within_rank32':rank is not None and rank<=32,'target_in_original_sample':target in sampled,'new_R2_CIDs_in_original_sample':sorted(sampled&new),'new_R2_CIDs_in_probe_top32':[x['cid'] for x in order[:32] if x['cid'] in new]};rows.append(row);armrows.append(row)
 arms.append({'arm':arm,'actual_managed_generation':p['generation_id'],'queries':len(armrows),'actual_new_exposed':sorted(exposed),'actual_target_exposed':target in exposed,'best_target_probe_rank':min(r['target_rank_in_probe'] for r in armrows if r['target_rank_in_probe'] is not None)})
 print('probed',arm,flush=True)
out.write_text(json.dumps({'probe_generation':gid,'arms':arms,'queries':rows,'source':'exact issued frozen queries and proof-bound vectors; no new query encoding, managed retrieve, sampling or pack write','limit':'Probe ranks diagnose query matching/window exposure; they are not source adoption or pixel success. Original samples are retained only for the originally issued generation.'},ensure_ascii=False,indent=2)+'\n');print(json.dumps(arms),flush=True)
