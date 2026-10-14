import json,pathlib,sys
r=pathlib.Path('docs/research-evidence/photo-prompt/slot-tag-codex-direct-20261014');x=json.loads((r/'authored/native_05250_peer05.01250_01285.read-packet-v1.json').read_text())
for a in x['records']:
 if int(sys.argv[1])<=a['ordinal']<int(sys.argv[2]):
  print('ORDINAL',a['ordinal'],'CID',a['candidate_id']);seen={}
  for k in ['original','current','original_packet_record','own_original_bindings','own_current_bindings','original_5B','checkpoint_record']:
   value=a[k]
   if k=='checkpoint_record':
    value=dict(value)
    for f in ['source_before','source_after']:
     if value[f] in [a['original'],a['current']]:value[f]={'exact_equal_read_field': 'original' if value[f]==a['original'] else 'current'}
   serialized=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
   if serialized in seen:print(k,'EXACT_JSON_EQUAL',seen[serialized])
   else:seen[serialized]=k;print(k,serialized)
