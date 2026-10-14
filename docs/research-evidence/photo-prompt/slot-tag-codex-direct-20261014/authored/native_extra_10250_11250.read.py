"""Lossless viewing: exact duplicate strings/objects refer to displayed source paths."""
import copy,json,sys
from pathlib import Path
R=Path(__file__).parent
packet=json.loads((R/'native_extra_10250_11250.inputs.json').read_text())
start,stop=map(int,sys.argv[1:3])
for row in packet['records'][start-10250:stop-10250]:
 out=copy.deepcopy(row);original=row['original']
 if row['original_equals_current']:out['current']={'exact_reference':'/original'}
 # All 5B fields are retained; only exact repeated quote strings use a path.
 for f in out['existing5B'].get('facts',[]):
  if f.get('quote')==original['content'].get('en'):f['quote']={'exact_reference':'/original/content/en'}
 for role in out['existing5B'].get('roles',[]):
  for f in role.get('evidence',[]):
   if f.get('quote')==original['content'].get('en'):f['quote']={'exact_reference':'/original/content/en'}
 for p in out['original_provenance_entries']:
  for match in p['matches']:
   for k,v in list(match['entry'].items()):
    if k in original['content'] and v==original['content'][k]:match['entry'][k]={'exact_reference':'/original/content/'+k}
 print(json.dumps(out,ensure_ascii=False,separators=(',',':')))
