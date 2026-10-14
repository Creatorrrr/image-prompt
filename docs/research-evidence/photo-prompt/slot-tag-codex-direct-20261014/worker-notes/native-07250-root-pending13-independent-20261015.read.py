import json,pathlib,sys,copy
R=pathlib.Path(__file__).resolve().parents[1]
X=json.loads((R/'authored/root_pending13_source_proposals_native_v2.json').read_text())
for row in X['records']:
 if int(sys.argv[1])<=row['ordinal']<int(sys.argv[2]):
  z=copy.deepcopy(row)
  if z['original_source']==z['source_current']:z['source_current']={'exact_equal_to':'original_source'}
  for op in z['literal_application_options']:
   for d in op['exact_top_delta']:
    ptr=d['pointer'];v=op['source_after']
    for key in ptr.strip('/').split('/'):v=v[key]
    if d.get('after')==v:d['after']={'exact_equal_to':'source_after'+ptr}
    before=row['source_current']
    try:
     for key in ptr.strip('/').split('/'):before=before[key]
    except KeyError:continue
    if d.get('before')==before:d['before']={'exact_equal_to':'source_current'+ptr}
  print(json.dumps(z,ensure_ascii=False))
