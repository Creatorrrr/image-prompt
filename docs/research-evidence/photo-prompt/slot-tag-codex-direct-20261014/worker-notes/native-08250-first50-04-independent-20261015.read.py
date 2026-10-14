"""Read-only input display. Exact factoring is not a semantic read counter."""
import copy,gzip,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
B=R/'native_batches/review11870-01250-01300-04'
P=R/'native-inputs/prepared/review11870-01250-01300-04'
batch=json.loads((B/'BATCH.json').read_text());packet=json.loads((P/'PREPARED-PACKET.json').read_text());inp=json.loads((P/'INPUT.json').read_text())
CACHE=R/'worker-notes/native-08250-first50-04-independent-20261015.display-cache.json'
state=json.loads(CACHE.read_text()) if CACHE.exists() else {'seen':{},'strings':[]}
def show(v,p):
    key=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    if len(key)>45 and key in state['seen']:return {'=exact':state['seen'][key]}
    if isinstance(v,str):
        out=v
        if len(v)>150:
            best=None
            for oldp,old in state['strings']:
                n=min(len(v),len(old));a=0
                while a<n and v[a]==old[a]:a+=1
                b=0
                while b<n-a and v[-b-1]==old[-b-1]:b+=1
                if best is None or a+b>best[0]:best=(a+b,oldp,a,len(old)-b,v[a:len(v)-b if b else len(v)],old)
            if best and best[0]>max(100,len(v)//2):
                _,oldp,a,b,repl,old=best;assert old[:a]+repl+old[b:]==v;out={'=delta':[oldp,a,b,repl]}
        state['strings'].append([p,v])
    elif isinstance(v,list):out=[show(x,p+'/'+str(i)) for i,x in enumerate(v)]
    elif isinstance(v,dict):out={k:show(x,p+'/'+k.replace('~','~0').replace('/','~1')) for k,x in v.items()}
    else:out=v
    if len(key)>45:state['seen'][key]=p
    return out
mode=sys.argv[1];ordinals=[int(x) for x in sys.argv[2:]]
sources={}
if mode=='source':
    for key in ['original_snapshot','current_snapshot']:
        raw=Path(inp[key]['file']).read_bytes();sources[key]=json.loads(gzip.decompress(raw) if raw[:2]==b'\x1f\x8b' else raw)
for ordinal in ordinals:
    row=batch['records'][ordinal-1250];assert row['ordinal']==ordinal;cid=row['candidate_id']
    if mode=='source':
        value={'candidate_id':cid,'ordinal':ordinal,'source_before':row['source_before'],'source_after':row['source_after'],'exact_delta':row['delta'],'whole_old5B':packet['historical_compiled_rows'][cid],'original_compiled_locator':row['original_compiled'],'own_bindings':{key:{bid:b for bid,b in source['slot_bindings'].items() if b['candidate_id']==cid} for key,source in sources.items()},'whole_dependencies':row['dependency_records'],'whole_reference_bindings':row['reference_bindings'],'worker_status':row['status'],'worker_rationale':row['rationale'],'worker_revision':row['revision']}
    elif mode=='proof':value=row['proof']
    else:raise ValueError('source/proof mode only')
    print(ordinal,mode,json.dumps(show(value,str(ordinal)+'/'+mode),ensure_ascii=False,separators=(',',':')))
CACHE.write_text(json.dumps(state,ensure_ascii=False)+'\n')
