import json,gzip,pathlib,hashlib
r=pathlib.Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014'); inp=r/'native-inputs/prepared/review11870-01250-01300-05/INPUT.json';x=json.loads(inp.read_text())
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(ref):
 p=pathlib.Path(ref['file']);assert h(p)==ref['file_sha256'];return json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_text())
o=load(x['original_snapshot']);c=load(x['current_snapshot']);records=[];files={str(inp):h(inp)}
for start in range(1250,1285,5):
 p=r/'native_batches/review11870-01250-01300-05'/f'CHECKPOINT-{start:05d}-{start+5:05d}-v1.json';batch=json.loads(p.read_text());files[str(p)]=h(p)
 for i,a in enumerate(batch['records']):
  cid=a['candidate_id'];dec=load(x['original_decisions'][cid]);pr=load(x['original_packets'][cid]);before=o['candidates'][cid];current=c['candidates'][cid];assert a['source_before']==before;assert a['source_after']==current
  records.append({'ordinal':a['ordinal'],'candidate_id':cid,'checkpoint':str(p),'checkpoint_pointer':f'/records/{i}','original':before,'current':current,'original_5B':dec['decisions'][x['original_decisions'][cid]['item']-1], 'original_packet_record':pr['records'][cid],'own_original_bindings':{k:v for k,v in o['slot_bindings'].items() if v.get('candidate_id')==cid},'own_current_bindings':{k:v for k,v in c['slot_bindings'].items() if v.get('candidate_id')==cid},'checkpoint_record':a})
y={'schema':'independent-semantic-peer-read-packet/v1','task':'/root/review_05250_06250','model':'gpt-6.1-sol','effort':'high','range':[1250,1285],'prepared_count':35,'actual_read_count':0,'input_raw_sha256':h(inp),'source09':x['current_snapshot'],'original_source':x['original_snapshot'],'catalog_canonical':'d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15','files':files,'records':records}
p=r/'authored/native_05250_peer05.01250_01285.read-packet-v1.json';assert not p.exists();p.write_text(json.dumps(y,ensure_ascii=False,indent=2)+'\n');print(p,h(p))
