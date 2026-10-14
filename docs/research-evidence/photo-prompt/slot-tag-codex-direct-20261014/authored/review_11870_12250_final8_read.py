import json,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as dr
from photo_candidate_realizations import ids
PENDING=[12072,12108,12113,12121,12122,12142,12167,12171]
p=json.loads((R/'packets/12000-250.json').read_text());d=dr.source()
assert dr.c.digest(d)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
for o in PENDING:
 c=p['ids'][o-12000];print('FINAL8_REREAD',o,'RID',ids(d['candidates'][c]));print(json.dumps(d['candidates'][c],ensure_ascii=False));print('CLOSURE',json.dumps(dr.closure(d,c),ensure_ascii=False))
for slot in ['expression','hair_style','surface_material','garment_state','species_marker','mood']:
 print('FULL_SPEC',slot,json.dumps(d['slot_catalog'][slot],ensure_ascii=False))
