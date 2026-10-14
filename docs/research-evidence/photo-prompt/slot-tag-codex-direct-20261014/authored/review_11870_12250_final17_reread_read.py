import json,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as dr
from photo_candidate_realizations import ids
PENDING=[12062,12072,12076,12086,12108,12113,12121,12122,12139,12142,12144,12165,12167,12171,12173,12179,12184]
p=json.loads((R/'packets/12000-250.json').read_text());d=dr.source()
assert dr.c.digest(d)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
for o in PENDING:
 c=p['ids'][o-12000];print('REREAD',o,c,'REALIZATIONS',ids(d['candidates'][c]));print(json.dumps(d['candidates'][c],ensure_ascii=False));print('COMPLETE_CLOSURE',json.dumps(dr.closure(d,c),ensure_ascii=False))
