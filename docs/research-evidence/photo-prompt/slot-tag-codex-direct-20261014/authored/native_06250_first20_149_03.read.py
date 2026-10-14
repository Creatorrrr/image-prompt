"""Bounded lossless source display; prepares no facts/modes/owners/approval."""
import sys,json,gzip,hashlib,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=Path.cwd();G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations/50fd92afd9400f2272e12fcd6494cafdeea407b841f8a862d066c48f447e6839')
sys.path[:0]=[str(G/'scripts'),str(G/'precore'),str(R)]
import direct_review as dr
D=R/'native-inputs/prepared/review06250-00000-00020-149-03'
load=lambda p:json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
canon=lambda v:hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
I=load(D/'INPUT.json');P=load(D/'PREPARED-PACKET.json');O=load(R/'SOURCE.json.gz');S=load(ROOT/I['current_snapshot']['file'])
assert canon(O)=='125d3527c728fbdee9ebdc915dc21ae0d84c8e379dd928e0012ff9df039e701b';assert canon(S)=='609e72864631ffccd711d2a6601ac060bea0a92f86985c7633a3fbea59d82ae5';assert canon(S['slot_catalog'])=='d9f4db418e1b63cd100b4c7a9fbff4c8401e00dffeffd22e299a0b5087a82b15'
a,b=map(int,sys.argv[1:3]);assert 0<=a<b<=20
for n in range(a,b):
 cid=I['ids'][n];orig=P['original_records'][cid];cur=P['current_records'][cid];comp=P['historical_compiled_rows'][cid];assert orig==O['candidates'][cid] and cur==S['candidates'][cid]
 print('WHOLE',n,cid)
 vals={'original':orig,'exact5Bafter':dr.corrected_record(orig,comp['corrections']),'current':cur,'compiled_locator':I['original_decisions'][cid],'whole_compiled_row':comp,'original_ownbindings':[v for v in O['slot_bindings'].values() if v['candidate_id']==cid],'current_ownbindings':[v for v in S['slot_bindings'].values() if v['candidate_id']==cid],'references':P['references'][cid],'reference_bindings':P['reference_bindings'][cid]}
 seen={}
 for k,v in vals.items():
  h=canon(v)
  if h in seen:print(k,json.dumps({'exact_equal_to_already_displayed':seen[h],'canonical_sha256':h},ensure_ascii=False))
  else:print(k,json.dumps(v,ensure_ascii=False,separators=(',',':')));seen[h]=k
