import json,pathlib,sys
r=pathlib.Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');x=json.loads((r/'authored/native_05250_peer05.01285_01295.read-packet-v1.json').read_text())
for a in x['records']:
 if int(sys.argv[1])<=a['ordinal']<int(sys.argv[2]):
  print('ORDINAL',a['ordinal'],'CID',a['candidate_id']); cp=a['checkpoint_record']; proof=cp['proof'];old=a['original_5B'];
  for label,value in [('original',a['original']),('current',a['current']),('ownbindings',a['own_current_bindings']),('old5B_semantic',{k:old[k] for k in ['corrections','facts','roles','meaning_summary','rejected_boundaries','uncertainties']}),('closure',{'candidate':cp['dependency_records'],'binding':cp['reference_bindings']}),('proof',{k:v for k,v in proof.items() if k!='review'}),('worker_rationale',cp['rationale'])]: print(label,json.dumps(value,ensure_ascii=False,separators=(',',':')))
