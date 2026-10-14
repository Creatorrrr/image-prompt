import json,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(R));import direct_review as dr
from photo_candidate_realizations import ids
ORD=[12033,12040,12046,12058,12062,12066,12068,12072,12076,12080,12081,12084,12086,12089,12102,12103,12106,12108,12112,12113,12114,12116,12118,12120,12121,12122,12132,12133,12135,12136,12139,12142,12144,12153,12157,12158,12165,12167,12171,12172,12173,12175,12176,12177,12178,12179,12180,12184]
p=json.loads((R/'packets/12000-250.json').read_text());d=dr.source()
assert dr.c.digest(d)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b'
for o in ORD[int(sys.argv[1]):int(sys.argv[2])]:
 c=p['ids'][o-12000];print('REREAD',o,c,'REALIZATIONS',ids(d['candidates'][c]));print(json.dumps(d['candidates'][c],ensure_ascii=False));print('COMPLETE_CLOSURE',json.dumps(dr.closure(d,c),ensure_ascii=False))
