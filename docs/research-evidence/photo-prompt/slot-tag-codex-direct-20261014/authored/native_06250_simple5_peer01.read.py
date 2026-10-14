import json,gzip,sys,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'native-inputs/prepared/review05250-simple5-149-01';O=R/'native_batches/review05250-simple5-149-01'
p=json.loads((D/'PREPARED-PACKET.json').read_text());b=json.loads((O/'BATCH.json').read_text());i=json.loads((D/'INPUT.json').read_text());src=json.load(gzip.open(i['current_snapshot']['file']))
o=int(sys.argv[1]);r=next(x for x in b['records'] if x['ordinal']==o);cid=r['candidate_id']
v={'ordinal':o,'original':p['original_records'][cid],'current':p['current_records'][cid],'whole_batch_row':r,'whole5B':p['historical_compiled_rows'][cid],'own_bindings':{k:x for k,x in src['slot_bindings'].items() if x['candidate_id']==cid},'closure':p['references'][cid],'closure_bindings':p['reference_bindings'][cid]}
t=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'));assert len(t)<44000
f=R/f'authored/native_06250_simple5_peer01.{o}.read.json';assert not f.exists();f.write_text(t+'\n');print(t);print('READ_RAW_SHA',hashlib.sha256(f.read_bytes()).hexdigest(),'BYTES',f.stat().st_size)
